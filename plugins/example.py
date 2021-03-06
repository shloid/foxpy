# This is an example plugin.
# It's recommended you base your plugin off of this.
# This also shows basic usage of FoxPlug, the class for making Fox plugins.

import sys
from plugins.plugin import FoxPlug
from util import Util
FoxPlug = FoxPlug()
util = Util()

# I highly recommend putting this code at the top of plugins (after imports, of course)
if __name__ == "__main__":
    FoxPlug.plugin_error(3)
    sys.exit()

FoxPlug.plugin_error(0, "example.py started!")
print("Hello, world!")
