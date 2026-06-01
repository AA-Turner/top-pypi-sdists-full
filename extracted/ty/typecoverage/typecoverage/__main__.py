"""
Module runner for ``python -m typecoverage``.
Uses the same CLI as ``typecoverage`` when installed as a package.
"""

import sys

from .core import parse_and_run

if __name__ == "__main__":
    sys.exit(parse_and_run())