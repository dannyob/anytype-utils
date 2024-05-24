# anytype-utils
Command-line utilities for Anytype in Python, including an unofficial API
library based on the internal Anytype Hearts middleware.

You need to have the desktop Anytype app running to use this API!

WARNING! I am not connected to the Anytype project. Using this API could render
your space or your app inoperable!

If you want something stable and safe, please wait for the Anyteam's official
API.

Initiation on the command line:
```sh
. bin/u-activate
make deps
make install

# First find the port on which to talk to Anytype Heart (should be running whenever you are using Anytype).
# Works on Mac and Linux
declare -x ANYTYPE_PORT=$(lsof -i -P -n | grep "anytype.*LISTEN" | sed -e 's/.*://' -e 's/ .*//g' | sort -n | head -n1)
```

A sample Python program
```python
import os
from pprint import pp
from anytype import Client

# First we connect to the local middleware
# that runs behind the Anytype desktop app
# (defaults to localhost:$ANYTYPE_PORT)
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

There's a [list of the
commands](https://github.com/anyproto/anytype-heart/blob/main/docs/proto.md#anytype-ClientCommands)
on the Anytype Heart repo.

Valid arguments are listed in the Request field descriptions. The Anytype
Hearts' Middleware API is used as the backend to Anytype's various client apps.
