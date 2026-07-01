"""
cvc.core.time — timezone-aware clock for CVC (Phase 1A native port).

Provides a single :func:`now` helper that returns a timezone-aware
``datetime`` based on the user's configured IANA timezone (e.g.
``Asia/Kolkata``).

Resolution order:
    1. ``CVC_TIMEZONE`` env var
    2. ``HERMES_TIMEZONE`` env var (legacy compatibility)
    3. ``timezone`` key in ``~/.cvc/config.yaml``
    4. Falls back to the server's local time (``datetime.now().astimezone()``)

Invalid timezone values log a warning and fall back safely — CVC never
crashes due to a bad timezone string.

Cached state is resolved once, reused on every call. Call
:func:`reset_cache` to force re-resolution (e.g. after config changes).
"""

from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from cvc.core.logging import get_cvc_home

__all__ = ["now", "get_timezone", "reset_cache"]


logger = logging.getLogger(__name__)

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python 3.8 fallback
    from backports.zoneinfo import ZoneInfo  # type: ignore[no-redef]


# Cached state — resolved once, reused on every call.
_cached_tz: Optional[ZoneInfo] = None
_cached_tz_name: Optional[str] = None
_cache_resolved: bool = False


def _resolve_timezone_name() -> str:
    """Read the configured IANA timezone string (or empty string).

    This does file I/O when falling through to ``config.yaml``, so callers
    should cache the result rather than calling on every :func:`now`.
    """
    # 1. Environment variables (highest priority — set by Supervisor, etc.)
    for env_name in ("CVC_TIMEZONE", "HERMES_TIMEZONE"):
        tz_env = os.getenv(env_name, "").strip()
        if tz_env:
            return tz_env

    # 2. config.yaml ``timezone`` key
    try:
        import yaml
        config_path = get_cvc_home() / "config.yaml"
        if config_path.exists():
            with open(config_path, encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            tz_cfg = cfg.get("timezone", "")
            if isinstance(tz_cfg, str) and tz_cfg.strip():
                return tz_cfg.strip()
    except Exception:
        pass

    return ""


def _get_zoneinfo(name: str) -> Optional[ZoneInfo]:
    """Validate and return a :class:`ZoneInfo`, or ``None`` if invalid."""
    if not name:
        return None
    try:
        return ZoneInfo(name)
    except Exception as exc:  # KeyError, ValueError, etc.
        logger.warning(
            "Invalid timezone '%s': %s. Falling back to server local time.",
            name, exc,
        )
        return None


def get_timezone() -> Optional[ZoneInfo]:
    """Return the user's configured :class:`ZoneInfo`, or ``None`` (server-local).

    Resolved once and cached. Call :func:`reset_cache` after config changes.
    """
    global _cached_tz, _cached_tz_name, _cache_resolved
    if not _cache_resolved:
        _cached_tz_name = _resolve_timezone_name()
        _cached_tz = _get_zoneinfo(_cached_tz_name)
        _cache_resolved = True
    return _cached_tz


def reset_cache() -> None:
    """Force the next :func:`get_timezone` call to re-read config."""
    global _cached_tz, _cached_tz_name, _cache_resolved
    _cached_tz = None
    _cached_tz_name = None
    _cache_resolved = False


def now() -> datetime:
    """Return the current time as a timezone-aware :class:`datetime`.

    If a valid timezone is configured, returns wall-clock time in that
    zone. Otherwise returns the server's local time (via
    ``astimezone()``).
    """
    tz = get_timezone()
    if tz is not None:
        return datetime.now(tz)
    return datetime.now().astimezone()
