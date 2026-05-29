"""``python -m matrice_common.debug`` — run the debugger CLI.

See :mod:`matrice_common.debug` for the full set of commands and flags.
"""

from __future__ import annotations

import sys

from .cli import main


if __name__ == "__main__":
    sys.exit(main() or 0)
