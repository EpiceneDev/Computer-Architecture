
"""Main."""

import sys
from cpu import *

cpu = CPU()

# if len(sys.argv) != 2:
#     print("Input in this order: file.py filename", file=sys.stderr)
#     sys.exit(1)
# else:
#     cpu.load(sys.argv[1])
cpu.load(sys.argv)

cpu.run()