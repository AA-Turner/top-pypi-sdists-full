"""`python -m efterlev` entry point.

Lets `efterlev.quickstart` (and any other in-process invoker) shell out
to the CLI without depending on the `efterlev` script being on PATH.
The pipx / uv-tool installs both put the script on PATH so the user-
facing `efterlev <cmd>` invocation continues to work; this module is
strictly for the internal subprocess-call case.
"""

from __future__ import annotations

from efterlev.cli.main import app

if __name__ == "__main__":
    app()
