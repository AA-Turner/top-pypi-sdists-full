"""
Background retention loop for the event spine.

Runs as a daemon thread inside the gateway process. Every 6 hours it:
  1. Rotates ``current.jsonl`` → dated file (if any content present)
  2. Purges daily JSONL files older than the configured retention window

This keeps the spine from growing unboundedly while preserving enough
history for the Time Portal, Emotional Arc, and Entity Graph features.

Lifecycle
=========
- :func:`start` boots the thread; idempotent.
- :func:`stop` joins it (called from FastAPI shutdown event).
- :func:`run_once` is exposed for manual triggering via the admin API
  (``POST /api/events/rotate`` / ``POST /api/events/purge``).

Configuration
=============
Retention settings come from ``~/.cvc/config.yaml`` under ``events:``:

    events:
      retention_days: 365         # default 365
      rotate_interval_hours: 6    # default 6

Missing config = use defaults. The defaults match
``cvc.events.spine.DEFAULT_RETENTION_DAYS = 365``.

Thread-safety
=============
The thread uses an :class:`threading.Event` for shutdown signalling.
:func:`run_once` holds the spine's append lock during rotation/purge,
so it's safe to call from multiple threads simultaneously.
"""
from __future__ import annotations

import logging
import threading
import time
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger("cvc.events.retention")

_DEFAULT_ROTATE_INTERVAL_HOURS = 6
_DEFAULT_RETENTION_DAYS = 365

_thread: Optional[threading.Thread] = None
_stop_event: Optional[threading.Event] = None
_started = False
_lock = threading.Lock()

# Last run stats — surfaced via /api/events/info and /api/events/config.
_last_run: dict[str, Any] = {
    "at": None,
    "rotated_files": [],
    "purged_count": 0,
    "duration_ms": 0,
    "ok": True,
    "error": None,
}


def _read_config() -> tuple[int, int]:
    """Read (retention_days, rotate_interval_hours) from ``~/.cvc/config.yaml``.

    Returns defaults if config missing or unparseable.
    """
    try:
        import yaml
        cfg_path = Path.home() / ".cvc" / "config.yaml"
        if not cfg_path.exists():
            return _DEFAULT_RETENTION_DAYS, _DEFAULT_ROTATE_INTERVAL_HOURS
        data = yaml.safe_load(cfg_path.read_text()) or {}
        events_cfg = data.get("events") or {}
        days = int(events_cfg.get("retention_days") or _DEFAULT_RETENTION_DAYS)
        hours = int(events_cfg.get("rotate_interval_hours") or _DEFAULT_ROTATE_INTERVAL_HOURS)
        if days < 1:
            days = _DEFAULT_RETENTION_DAYS
        if hours < 1:
            hours = _DEFAULT_ROTATE_INTERVAL_HOURS
        return days, hours
    except Exception as exc:  # noqa: BLE001 — config is best-effort
        logger.debug("retention: failed to read config, using defaults: %s", exc)
        return _DEFAULT_RETENTION_DAYS, _DEFAULT_ROTATE_INTERVAL_HOURS


def get_config() -> dict[str, Any]:
    """Return current retention config + last-run stats (for dashboard)."""
    days, hours = _read_config()
    return {
        "retention_days": days,
        "rotate_interval_hours": hours,
        "running": _started and _thread is not None and _thread.is_alive(),
        "last_run": dict(_last_run),
    }


def run_once(retention_days: Optional[int] = None) -> dict[str, Any]:
    """Rotate + purge once. Returns stats.

    Args:
        retention_days: Override the configured retention (used by admin API
            and tests). Falls back to config when None.
    """
    started_at = time.time()
    if retention_days is None:
        retention_days, _ = _read_config()
    stats: dict[str, Any] = {
        "at": started_at,
        "rotated_files": [],
        "purged_count": 0,
        "duration_ms": 0,
        "ok": True,
        "error": None,
    }
    try:
        # Lazy import so loading this module doesn't pull the spine on
        # systems where the spine hasn't been initialised yet.
        from cvc.events.spine import rotate_if_needed, purge_older_than

        rotated = rotate_if_needed() or []
        purged = purge_older_than(days=retention_days)
        stats["rotated_files"] = [str(p) for p in rotated]
        stats["purged_count"] = int(purged)
        logger.info(
            "retention: ok rotated=%d purged=%d retention_days=%d",
            len(rotated), purged, retention_days,
        )
    except Exception as exc:  # noqa: BLE001 — must not crash the thread
        stats["ok"] = False
        stats["error"] = str(exc)
        logger.warning("retention: run_once failed: %s", exc)
    stats["duration_ms"] = int((time.time() - started_at) * 1000)
    # Update module-level last-run state for get_config().
    _last_run.update(stats)
    return stats


def _loop(interval_hours: int, stop_event: threading.Event) -> None:
    """The actual thread body. Sleeps for ``interval_hours`` between runs."""
    # First run after a short delay — let the gateway warm up first.
    initial_delay_s = 60.0
    if stop_event.wait(timeout=initial_delay_s):
        return
    while not stop_event.is_set():
        try:
            run_once()
        except Exception as exc:  # noqa: BLE001
            logger.exception("retention loop tick failed: %s", exc)
        # Sleep in small chunks so stop() reacts quickly.
        interval_s = interval_hours * 3600.0
        chunk_s = 30.0
        elapsed = 0.0
        while elapsed < interval_s and not stop_event.is_set():
            stop_event.wait(timeout=min(chunk_s, interval_s - elapsed))
            elapsed += chunk_s


def start() -> bool:
    """Boot the background retention thread. Idempotent.

    Returns True if the thread is running after this call (either we
    started it, or it was already running).
    """
    global _thread, _stop_event, _started
    with _lock:
        if _started and _thread is not None and _thread.is_alive():
            return True
        _, interval_hours = _read_config()
        _stop_event = threading.Event()
        _thread = threading.Thread(
            target=_loop,
            args=(interval_hours, _stop_event),
            name="cvc-events-retention",
            daemon=True,
        )
        _thread.start()
        _started = True
        logger.info("retention: thread started (interval=%dh)", interval_hours)
        return True


def stop(timeout_s: float = 5.0) -> bool:
    """Signal the retention thread to stop and join it.

    Returns True if the thread exited within ``timeout_s``.
    """
    global _thread, _stop_event, _started
    with _lock:
        if not _started or _thread is None or _stop_event is None:
            return True
        _stop_event.set()
        _thread.join(timeout=timeout_s)
        exited = not _thread.is_alive()
        _started = False
        _thread = None
        _stop_event = None
        if exited:
            logger.info("retention: thread stopped cleanly")
        else:
            logger.warning("retention: thread did not stop within %.1fs", timeout_s)
        return exited


def is_running() -> bool:
    """Whether the background thread is currently active."""
    return _started and _thread is not None and _thread.is_alive()