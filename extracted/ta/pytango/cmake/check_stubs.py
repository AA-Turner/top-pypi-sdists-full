"""Basic check to see if stub file was generated and installed.

For use during continuous integration testing.
"""

import sys
from pathlib import Path

import tango

if __name__ == "__main__":
    pyi_path = Path(tango.__file__).parent / "_tango.pyi"
    if not pyi_path.is_file():
        print(f"Error: typing stub file is missing: {pyi_path}")
        sys.exit(1)
    else:
        print(f"Typing stub file exists: {pyi_path}")
