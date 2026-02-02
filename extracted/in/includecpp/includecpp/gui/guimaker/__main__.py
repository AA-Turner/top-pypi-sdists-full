"""
CSSL GUI Builder - Direct module execution.
Usage: python -m includecpp.gui.guimaker [optional_file.cssl]
"""

import sys
from . import run_guimaker

file_path = sys.argv[1] if len(sys.argv) > 1 else ""
run_guimaker(file_path)
