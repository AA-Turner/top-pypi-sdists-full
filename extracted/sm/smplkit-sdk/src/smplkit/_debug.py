"""Internal debug logging for the smplkit SDK.

Controlled by the ``SMPLKIT_DEBUG`` environment variable.  When enabled
(``SMPLKIT_DEBUG=1``, ``true``, or ``yes``, case-insensitive), the SDK
emits timestamped diagnostic lines to stderr covering every meaningful
internal operation.

Debug output goes directly to ``sys.stderr.write()`` — never through
``logging.getLogger()`` — to avoid interfering with the managed logging
framework the SDK controls.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone


def _parse_debug_env(value: str) -> bool:
    """Return True if *value* is a truthy SMPLKIT_DEBUG setting."""
    return value.strip().lower() in {"1", "true", "yes"}


_DEBUG_ENABLED: bool = _parse_debug_env(os.environ.get("SMPLKIT_DEBUG", ""))


def enable_debug() -> None:
    """Enable debug output (called when config file or constructor sets debug=True)."""
    global _DEBUG_ENABLED
    _DEBUG_ENABLED = True


def is_debug_enabled() -> bool:
    """Return True if SMPLKIT_DEBUG is enabled."""
    return _DEBUG_ENABLED


def debug(subsystem: str, message: str) -> None:
    """Emit a debug line to stderr if SMPLKIT_DEBUG is enabled.

    Format::

        [smplkit:{subsystem}] {ISO-8601 timestamp} {message}

    This is a no-op when SMPLKIT_DEBUG is not set (zero overhead in
    production).
    """
    if not _DEBUG_ENABLED:
        return
    ts = datetime.now(timezone.utc).isoformat()
    sys.stderr.write(f"[smplkit:{subsystem}] {ts} {message}\n")
