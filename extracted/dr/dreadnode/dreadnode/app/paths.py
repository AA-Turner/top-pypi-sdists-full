"""Canonical on-disk paths for Dreadnode persistent state.

Everything the SDK writes to a user's machine lives under
``~/.dreadnode/``. This module centralises the subpaths so MCP servers,
capability subprocess workers, TUI/SDK self-logs, and future components
can share a single convention — and a single directory to tail or ship
when troubleshooting.

Tests override the base directory by monkeypatching :data:`LOGS_DIR`
(or :data:`DREADNODE_HOME`) on this module; helpers read the attribute
dynamically at call time.
"""

import contextlib
from pathlib import Path

DREADNODE_HOME: Path = Path.home() / ".dreadnode"
"""Root directory for Dreadnode state (config, caches, sessions, logs)."""

LOGS_DIR: Path = DREADNODE_HOME / "logs"
"""Shared directory for runtime logs across components.

Filenames encode the producing component and its context so a flat ``ls``
is self-describing:

* subprocess workers — ``worker-<capability>-<worker>.log``
* MCP servers (planned)  — ``mcp-<capability>-<server>.log``
* TUI / SDK self-logs (planned) — ``tui.log`` / ``sdk.log``

User-initiated exports from the TUI console screen share this directory
so everything we write lands in one place.
"""


def worker_log_path(capability: str, worker_name: str) -> Path:
    """Path for a subprocess worker's combined stdout/stderr log."""
    return LOGS_DIR / f"worker-{capability}-{worker_name}.log"


def mcp_log_path(capability: str, server_name: str) -> Path:
    """Path for an MCP server's captured stderr log.

    Stdout carries the MCP protocol itself, so only stderr is teed here —
    which is where servers print startup errors, debug traces, and crashes.
    """
    return LOGS_DIR / f"mcp-{capability}-{server_name}.log"


def rotate_log(log_path: Path) -> None:
    """Rotate ``log_path`` to ``<path>.prev`` before a fresh open.

    Gives operators one level of crash history — the log just before the
    most recent (re)start survives as ``<path>.prev`` — without letting an
    unbounded archive accumulate. Missing files and rotation errors are
    silently ignored since the caller will log the fresh open itself and
    we never want rotation to block a worker or server from starting.
    """
    with contextlib.suppress(OSError):
        if log_path.exists():
            log_path.replace(log_path.with_suffix(log_path.suffix + ".prev"))
