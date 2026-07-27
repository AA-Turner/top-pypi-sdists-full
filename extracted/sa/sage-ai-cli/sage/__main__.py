"""Entry point for ``python -m sage`` / ``py -m sage`` / ``sage`` (via sage.bat).

Cross-platform startup (UTF-8 streams + Windows ANSI escapes + locale override)
lives in ``sage.main`` so it runs for every entry point, including the
pip-installed ``sage`` console script and the API server.
"""

from __future__ import annotations

import os

# Auto-configure NO_COLOR environment variables if run within antigravity sandbox
if "ANTIGRAVITY_PROJECT_ID" in os.environ:
    os.environ["NO_COLOR"] = "1"
    os.environ["SAGE_NO_COLOR"] = "1"

from sage.cli_core import app

if __name__ == "__main__":
    app()
