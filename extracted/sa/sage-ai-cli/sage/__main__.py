"""Entry point for ``python -m sage`` / ``py -m sage`` / ``sage`` (via sage.bat).

Cross-platform startup (UTF-8 streams + Windows ANSI escapes + locale override)
lives in ``sage.main`` so it runs for every entry point, including the
pip-installed ``sage`` console script and the API server.
"""

from __future__ import annotations

from sage.main import app

if __name__ == "__main__":
    app()
