"""Recorded sessions hosted in the service: class RecorderHost composed of its parts.
Front door for the old `probe.service.recorders`: names read live, a patch reaches every piece binding the name."""

from __future__ import annotations

from probe.foundation.front_door.front_door import serve_pieces

# Every piece loads here, in load order, as the old module ran whole on import (static, so the
# test gate's import graph sees this door use them).
import probe.service.sessions.recorders.recording as _piece_recording  # noqa: F401
import probe.service.sessions.recorders.threads as _piece_threads  # noqa: F401
import probe.service.sessions.recorders.capture_off as _piece_capture_off  # noqa: F401
import probe.service.sessions.recorders.gaps as _piece_gaps  # noqa: F401
import probe.service.sessions.recorders.tap as _piece_tap  # noqa: F401
import probe.service.sessions.recorders.restarts as _piece_restarts  # noqa: F401
import probe.service.sessions.recorders.recorders as _piece_recorders  # noqa: F401

#: The old module's pieces, in load order: a write through the door reaches these only.
_PIECES = (
    "probe.service.sessions.recorders.recording",
    "probe.service.sessions.recorders.threads",
    "probe.service.sessions.recorders.capture_off",
    "probe.service.sessions.recorders.gaps",
    "probe.service.sessions.recorders.tap",
    "probe.service.sessions.recorders.restarts",
    "probe.service.sessions.recorders.recorders",
)

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.service.sessions.recorders.recording
    "Any": "probe.service.sessions.recorders.recording",
    "DEFERRED_KEY": "probe.service.sessions.recorders.recording",
    "ENDED_STEP": "probe.service.sessions.recorders.recording",
    "PAUSED_STEP": "probe.service.sessions.recorders.recording",
    "Path": "probe.service.sessions.recorders.recording",
    "RECORD_STEP": "probe.service.sessions.recorders.recording",
    "Recording": "probe.service.sessions.recorders.recording",
    "dataclass": "probe.service.sessions.recorders.recording",
    "field": "probe.service.sessions.recorders.recording",
    "threading": "probe.service.sessions.recorders.recording",
    "time": "probe.service.sessions.recorders.recording",
    # probe.service.sessions.recorders.threads
    "AFTER_EXIT_TRIES": "probe.service.sessions.recorders.threads",
    "Callable": "probe.service.sessions.recorders.threads",
    "FIRST_RETRY_S": "probe.service.sessions.recorders.threads",
    "Family": "probe.service.sessions.recorders.threads",
    "HANDOVER_AHEAD_S": "probe.service.sessions.recorders.threads",
    "HEALTHY_RUN_S": "probe.service.sessions.recorders.threads",
    "MAX_RETRY_S": "probe.service.sessions.recorders.threads",
    "RETRY_ENV": "probe.service.sessions.recorders.threads",
    "STOPPED_RETRIES": "probe.service.sessions.recorders.threads",
    "ThreadsMixin": "probe.service.sessions.recorders.threads",
    "_first_retry": "probe.service.sessions.recorders.threads",
    "capture_gate": "probe.service.sessions.recorders.threads",
    "contextlib": "probe.service.sessions.recorders.threads",
    "os": "probe.service.sessions.recorders.threads",
    "procid": "probe.service.sessions.recorders.threads",
    # probe.service.sessions.recorders.capture_off
    "CLAIM_EVERY_S": "probe.service.sessions.recorders.capture_off",
    "CLAIM_MAX_S": "probe.service.sessions.recorders.capture_off",
    "CaptureOffMixin": "probe.service.sessions.recorders.capture_off",
    # probe.service.sessions.recorders.gaps
    "GapsMixin": "probe.service.sessions.recorders.gaps",
    # probe.service.sessions.recorders.tap
    "KIMI_LIST": "probe.service.sessions.recorders.tap",
    "KIMI_MANAGED": "probe.service.sessions.recorders.tap",
    "MAX_ENV": "probe.service.sessions.recorders.tap",
    "MIN_PYTHON": "probe.service.sessions.recorders.tap",
    "SETTLE_S": "probe.service.sessions.recorders.tap",
    "TAPS_NAME": "probe.service.sessions.recorders.tap",
    "TapMixin": "probe.service.sessions.recorders.tap",
    "_KIMI_TAP": "probe.service.sessions.recorders.tap",
    "_SIBLING": "probe.service.sessions.recorders.tap",
    "_VERSION": "probe.service.sessions.recorders.tap",
    "_codex_cache": "probe.service.sessions.recorders.tap",
    "_has_tap": "probe.service.sessions.recorders.tap",
    "_kimi_installed": "probe.service.sessions.recorders.tap",
    "_numbers": "probe.service.sessions.recorders.tap",
    "_pin": "probe.service.sessions.recorders.tap",
    "_replacement": "probe.service.sessions.recorders.tap",
    "_settled": "probe.service.sessions.recorders.tap",
    "installed_tap": "probe.service.sessions.recorders.tap",
    "json": "probe.service.sessions.recorders.tap",
    "paths": "probe.service.sessions.recorders.tap",
    "re": "probe.service.sessions.recorders.tap",
    "sys": "probe.service.sessions.recorders.tap",
    # probe.service.sessions.recorders.restarts
    "RECORDERS_NAME": "probe.service.sessions.recorders.restarts",
    "RECORDERS_VERSION": "probe.service.sessions.recorders.restarts",
    "RESUME_SPREAD_S": "probe.service.sessions.recorders.restarts",
    "RestartsMixin": "probe.service.sessions.recorders.restarts",
    "random": "probe.service.sessions.recorders.restarts",
    # probe.service.sessions.recorders.recorders
    "PAUSE_JOIN_S": "probe.service.sessions.recorders.recorders",
    "RecorderHost": "probe.service.sessions.recorders.recorders",
    "asyncio": "probe.service.sessions.recorders.recorders",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
