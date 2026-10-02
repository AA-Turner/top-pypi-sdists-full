"""Emit a warning at most once per distinct key for the life of the process.

The SDK must never crash or spam the host app, so every failure on the user's
path degrades quietly: a span is dropped, a call runs untraced, a payload is
stubbed. Silent is safe but undebuggable: a user who suddenly has no traces, or
sees a stubbed payload, has no signal as to why. Logging on every call from a
hot path is its own problem. A one-time warning per distinct issue restores the
signal without the flood.

Keys should identify the specific degradation (e.g. include the failing
trace-function key) so each distinct issue warns once, not just the first one
seen.
"""

import contextlib
import logging
import os
import threading

logger = logging.getLogger("bitfab")

_warned: set[str] = set()
_lock = threading.Lock()


def _reset_lock_after_fork() -> None:
    global _lock
    _lock = threading.Lock()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_lock_after_fork)


def warn(message: str) -> None:
    """Log a ``bitfab:`` warning."""
    with contextlib.suppress(Exception):
        logger.warning("bitfab: %s", message)


def warn_once(key: str, message: str) -> None:
    """Log a ``bitfab:`` warning at most once per distinct ``key``."""
    with _lock:
        if key in _warned:
            return
        _warned.add(key)
    warn(message)


def _reset_warn_once() -> None:
    """Test-only: clear the dedup set so a warning can fire again."""
    with _lock:
        _warned.clear()
