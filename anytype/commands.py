import pb.protos.service.service_pb2_grpc as service
import pb.protos.commands_pb2 as commands
import google.protobuf.json_format as jf
import os
from os.path import commonprefix


def obj_prefix_dict(commands, objects):
    """This terrifying function takes a list of gRPC commands (which take the
    form of ObjectVerb, like "AppGetVersion" and "BlockSearch") and a list of
    object anmes (which have the form of "App" and "Block"), and returns a
    mapping from the full command to the its object-name prefix.

    We need this, because request and responses are stored under their object
    namespace at pb.protos.commands_pb2.<object>.<verb>.Response|Request, while
    gRPC commands are called at service.ClientCommandsStub().<commands>. We
    find the commands, then construct a mapping to objects and verb."""
    return {
        rpc_command:  # go through every command as a key, and find the dict value:
        max(
            [
                prefix
                for prefix in set(  # find the longest prefix
                    [
                        commonprefix(
                            [rpc_command, rpc_object]
                        )  # out of all common prefixes
                        for rpc_object in objects
                    ]
                )  # between the command and all the objects
                if prefix in objects
            ],  # but only if those prefixes are actual object names
            default=[],
        )  # if there is not a match then `max` should default to []
        for rpc_command in commands
    }


class Client:
    # These are the objects that rpc requests structures are stored under,
    # They take the form commands.Rpc.App.GetVersion, etc.
    # this just filters them to only exclude DESCRIPTOR, __slots__ etc
    rpc_objects = set(
        [
            i
            for i in commands.Rpc.__dict__.keys()
            if len(i) > 1 and i[0].isupper() and i[1].islower()
        ]
    )

    def _send(self, call, request, auth=True):
        """Makes an rpc call @call with @request.
        Adds a auth token if needed and available.
        Returns a Python dict based on the response."""
        if self.token and auth:
            return jf.MessageToDict(call(request, metadata=[("token", self.token)]))
        else:
            return jf.MessageToDict(call(request))

    def _callRpc(self, rpc_command, auth=True, **kwargs):
        """Constructs a request and sends a call based on the name of the command.
        Breaks the command into object and verb to locate the correct Request object.
        then provides _send with the correct call method of stub.
        Some commands don't require authorisation, but this needs to be flagged separately."""
        obj = self.rpc_command_to_obj[rpc_command]
        verb = rpc_command[len(obj) :]
        request = commands.Rpc.__dict__[obj].__dict__[verb].Request(**kwargs)
        return self._send(self.stub.__dict__[rpc_command], request, auth)

    def __init__(self, connection):
        self.channel = service.grpc.insecure_channel(connection)
        self.stub = service.ClientCommandsStub(self.channel)
        self.rpc_commands = self.stub.__dict__.keys()
        # We can only construct the object prefix list after we construct the stub
        self.rpc_command_to_obj = obj_prefix_dict(self.rpc_commands, Client.rpc_objects)
        self.token = None

    def __getattr__(self, method):
        """If a nonexistent method is called, see if it matches a rpc command.
        If it does, then do call that commands."""

        def do_command(self=self, **kwargs):
            nonlocal method
            return self._callRpc(method, **kwargs)

        if method in self.rpc_commands:
            return do_command
        else:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{method}'"
            )

    def WalletCreateSession(self, **kwargs):
        if "mnemonic" not in kwargs:
            if "ANYTYPE_PW" in os.environ:
                kwargs["mnemonic"] = os.getenv("ANYTYPE_PW")
            else:
                raise "WalletCreateSession needs an Anytype passphrase"
        response = self._callRpc("WalletCreateSession", auth=False, **kwargs)
        self.token = response["token"]  # TODO error handling
        return response

    def AppGetVersion(self, **kwargs):
        return self._callRpc("AppGetVersion", auth=False, **kwargs)
