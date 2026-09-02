"""
Entry-point shim for the deprecated `arcade-ai` package.

The `arcade-ai` PyPI package has been renamed to `arcade-mcp`.
This shim prints a prominent deprecation notice and then delegates
to the real `arcade` CLI that is installed alongside `arcade-mcp`.
"""

import subprocess
import sys


_DEPRECATION_NOTICE = """
╔══════════════════════════════════════════════════════════════════════════╗
║                         ⚠  PACKAGE DEPRECATED  ⚠                        ║
║                                                                          ║
║  'arcade-ai' has been renamed to 'arcade-mcp'.                          ║
║  This package will no longer receive updates.                           ║
║                                                                          ║
║  Migrate using whichever tool you used to install:                      ║
║                                                                          ║
║  pip:                                                                    ║
║    pip uninstall arcade-ai && pip install arcade-mcp                    ║
║                                                                          ║
║  uv (global tool):                                                       ║
║    uv tool uninstall arcade-ai && uv tool install arcade-mcp            ║
║                                                                          ║
║  uv (project dependency):                                                ║
║    uv remove arcade-ai && uv add arcade-mcp                             ║
║                                                                          ║
║  After migrating, use the 'arcade' command as usual.                    ║
║  Docs: https://docs.arcade.dev                                           ║
╚══════════════════════════════════════════════════════════════════════════╝
"""


def main() -> None:
    print(_DEPRECATION_NOTICE, file=sys.stderr)
    try:
        result = subprocess.run(["arcade"] + sys.argv[1:])
        sys.exit(result.returncode)
    except FileNotFoundError:
        print(
            "ERROR: The 'arcade' command was not found.\n"
            "Install arcade-mcp to get it:\n\n"
            "    pip install arcade-mcp\n",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
