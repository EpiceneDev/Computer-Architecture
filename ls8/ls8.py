
"""Main."""

import sys
from cpu3 import *

cpu3 = CPU()

# if len(sys.argv) != 2:
#     print("Input in this order: file.py filename", file=sys.stderr)
#     sys.exit(1)
# else:
#     cpu.load(sys.argv)
cpu3.load(sys.argv)

cpu3.run()