from pprint import pp
from anytype.utils import Client

# First we connect to the local middleware that runs behind the Anytype desktop app.
# It will default to using using ANYTYPE_PORT -- see [README](./README.md) for details.
# Otherwise "localhost:{port}" as an argument will do.
c = Client()
# Check that we can get a version (this RPC call does not need authentication)
print(c.AppGetVersion())

# Get an authentication token -- this uses ANYTYPE_PW as your passphrase
c.WalletCreateSession()

# Print all the objects (well, most of them -- I haven't checked)
pp(c.ObjectSearch(fullText=""))
