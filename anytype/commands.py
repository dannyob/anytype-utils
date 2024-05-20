import pb.protos.service.service_pb2_grpc as service
import pb.protos.commands_pb2 as commands
import google.protobuf.json_format as jf
import os
import re


# FIXME: This is simple version of this function; should use the actual class
# structure of commands.Rpc to split the term.
def funcnameToRpcObject(funcname: str):
    match = re.match(r"([A-Z][a-z]*)([A-Z].*)", funcname)
    if not match:
        raise ValueError("Input string doesn't match the expected format.")
    first_word, rest_of_string = match.groups()
    return (first_word, rest_of_string)


class Client:
    def _send(self, call, request, auth=True):
        if self.token and auth:
            return jf.MessageToDict(call(request, metadata=[("token", self.token)]))
        else:
            return jf.MessageToDict(call(request))

    def _callRpc(self, funcname, auth=True, **kwargs):
        obj, call = funcnameToRpcObject(funcname)
        request = commands.Rpc.__dict__[obj].__dict__[call].Request(**kwargs)
        return self._send(self.stub.__dict__[funcname], request, auth)

    def __init__(self, connection):
        self.channel = service.grpc.insecure_channel(connection)
        self.stub = service.ClientCommandsStub(self.channel)
        self.token = None

    def AppGetVersion(self, **kwargs):
        return self._callRpc("AppGetVersion", auth=False, **kwargs)

    def WalletCreateSession(self, **kwargs):
        if "mnemonic" not in kwargs:
            if "ANYTYPE_PW" in os.environ:
                kwargs["mnemonic"] = os.getenv("ANYTYPE_PW")
            else:
                raise "WalletCreateSession needs an Anytype passphrase"
        response = self._callRpc("WalletCreateSession", auth=False, **kwargs)
        self.token = response["token"]  # TODO error handling
        return response

    def ObjectOpen(self, **kwargs):
        return self._callRpc("ObjectOpen", **kwargs)
