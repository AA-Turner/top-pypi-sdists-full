import sys
from sage.cli_core import app

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("run")
    app()
