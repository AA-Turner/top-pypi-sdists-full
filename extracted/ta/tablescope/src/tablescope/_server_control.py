"""Process-wide handle for stopping the running tablescope server.

The CLI serves the marimo notebook in the *same* process as the uvicorn
server, so a widget message handler (which runs in that process) can ask the
server to shut down by flipping a flag on the live `uvicorn.Server`. The CLI
registers the server here; the widget calls `request_shutdown()` when the
frontend's stop button is clicked.

If tablescope is used as a plain library (no CLI server), nothing is
registered and `request_shutdown()` reports that there is nothing to stop.
"""

from __future__ import annotations

from typing import Any

# The live uvicorn.Server, set by the CLI before it serves. Left as Any to
# avoid importing uvicorn here (it stays a CLI-time dependency).
_server: Any | None = None


def register_server(server: Any) -> None:
    """Record the running server so the widget can later stop it."""
    global _server
    _server = server


def request_shutdown() -> bool:
    """Ask the registered server to shut down gracefully.

    Returns True if a server was registered and asked to stop, False if there
    was nothing to stop (e.g. running as a library, not via the CLI).
    `uvicorn.Server.run()` watches `should_exit` and returns cleanly when set,
    so this triggers the same graceful shutdown as Ctrl+C.
    """
    if _server is None:
        return False
    _server.should_exit = True
    return True
