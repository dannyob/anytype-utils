# anytype-utils
Command-line utilities for Anytype

The story so far:

Initiation on the command line:
```sh
. bin/u-activate
bin/update-grpc
declare -x ANYTYPE_PORT=$(lsof -i -P -n | grep "anytype.*LISTEN" | sed -e 's/.*://' -e 's/ .*//g' | sort -n | head -n1)
declare -x ANYTYPE_PW=<your passphrase>
```

A sample Python program
```python
import os
from anytype.commands import Client

port = os.getenv("ANYTYPE_PORT")

# First we connect to the local middleware
# that runs behind the Anytype desktop app
c = Client.connect(f"localhost:{port}")

# Now we unlock using our passphrase -- this function
# will use the ANYTYPE_PW environment variable, or
# WalletCreateSession(mnemonic = <your passphrase here>)
c.WalletCreateSession()
```

