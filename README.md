# anytype-utils
Command-line utilities for Anytype

The story so far:

Initiation on the command line:
```sh
. bin/u-activate
make grpc

# find the port on which to talk to Anytype Heart (should be running whenever you are using Anytype).
# Works on Mac and Linux
declare -x ANYTYPE_PORT=$(lsof -i -P -n | grep "anytype.*LISTEN" | sed -e 's/.*://' -e 's/ .*//g' | sort -n | head -n1)
declare -x ANYTYPE_PW=<your passphrase>
```

A sample Python program
```python
import os
from pprint import pp
from anytype.commands import Client

port = os.getenv("ANYTYPE_PORT")

# First we connect to the local middleware
# that runs behind the Anytype desktop app
c = Client(f"localhost:{port}")

print(c.AppGetVersion())
# You'll get something like:
# {'error': {}, 'version': 'v0.33.2', 'details': 'build on 2024-04-25 13:28:54 +0000 UTC at #4ec64b016e2be3a5229dc865452c066f653e209c'}

# Now we unlock using our passphrase -- this function
# will use the ANYTYPE_PW environment variable, or
# WalletCreateSession(mnemonic = <your passphrase here>)
c.WalletCreateSession()

pp(c.ObjectSearch(fullText=""))

```

