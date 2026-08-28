"""Shared helpers for the ``MATRICE_FORCE_WALLCLOCK_STREAM_TIME`` override.

DRIFT-005: upstream the ml-codebases ``deploy.py`` ``_patch_stream_time``
monkey-patch into py_analytics so the inference-engine container can force
wall-clock stream_time via an env var instead of patching SDK internals at
runtime.

Background: RTP-derived ``capture_timestamp_ns`` can be a relative value (not
Unix epoch), so stream_time fields computed from it can render as dates near
1970. When ``MATRICE_FORCE_WALLCLOCK_STREAM_TIME`` is set to a truthy value the
incident ``stream_time`` and the fire timestamp are instead stamped with the
current wall-clock (UTC) time. Default OFF preserves the existing
frame/RTP-derived behavior exactly.

The wall-clock source is injectable via :func:`set_wallclock_now_provider` so
unit tests can pin a deterministic "now" instead of relying on the real clock.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Callable, Optional

# Values that enable the override (case-insensitive, whitespace-stripped).
_TRUTHY = {"1", "true", "yes", "on", "y", "t"}

# Wall-clock output formats, byte-identical to the historical deploy.py patch.
INCIDENT_STREAM_TIME_FMT = "%Y-%m-%d-%H:%M:%S.%f UTC"
FIRE_TIMESTAMP_FMT = "%Y:%m:%d %H:%M:%S"

# Env var that gates the override.
ENV_FLAG = "MATRICE_FORCE_WALLCLOCK_STREAM_TIME"


def _default_now() -> datetime:
    return datetime.now(timezone.utc)


_now_provider: Callable[[], datetime] = _default_now


def set_wallclock_now_provider(provider: Optional[Callable[[], datetime]]) -> None:
    """Override the wall-clock source. Pass ``None`` to restore the real clock.

    Intended for tests that need a deterministic "now"; production leaves it at
    the default (:func:`datetime.now`).
    """
    global _now_provider
    _now_provider = provider or _default_now


def wallclock_now() -> datetime:
    """Return the current wall-clock time from the (possibly injected) source."""
    return _now_provider()


def force_wallclock_stream_time() -> bool:
    """True when ``MATRICE_FORCE_WALLCLOCK_STREAM_TIME`` is set to a truthy value."""
    return str(os.environ.get(ENV_FLAG, "")).strip().lower() in _TRUTHY


def wallclock_incident_stream_time() -> str:
    """Wall-clock stream_time in the incident-message format."""
    return wallclock_now().strftime(INCIDENT_STREAM_TIME_FMT)


def wallclock_fire_timestamp() -> str:
    """Wall-clock timestamp in the fire-detection human-text format."""
    return wallclock_now().strftime(FIRE_TIMESTAMP_FMT)
