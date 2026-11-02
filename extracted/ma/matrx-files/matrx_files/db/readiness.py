from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DatabaseReadiness:
    ready: bool
    checked_at: float
    error_type: str | None = None


_lock = asyncio.Lock()
_cached: DatabaseReadiness | None = None


async def probe_database_readiness(
    *, max_age_seconds: float = 5.0, timeout_seconds: float = 5.0
) -> DatabaseReadiness:
    """Probe the matrx-files database, caching the result briefly.

    Bounded: a readiness probe that hangs is a monitor that never alarms. On
    2026-09-25 this probe queued behind a wedged pool lock for 4.5 hours while
    ``/files-service/health`` kept answering 200; now it answers ``not_ready``
    with ``error_type=TimeoutError`` inside ``timeout_seconds``.
    """
    global _cached
    now = time.monotonic()
    if _cached is not None and now - _cached.checked_at <= max_age_seconds:
        return _cached

    async with _lock:
        now = time.monotonic()
        if _cached is not None and now - _cached.checked_at <= max_age_seconds:
            return _cached
        try:
            from matrx_files.db import ensure_bound
            from matrx_files.db.models_files import Files

            ensure_bound()
            async with asyncio.timeout(timeout_seconds):
                await Files.exists()
            _cached = DatabaseReadiness(ready=True, checked_at=now)
        except Exception as exc:  # noqa: BLE001 - readiness reports every dependency failure
            _cached = DatabaseReadiness(
                ready=False,
                checked_at=now,
                error_type=type(exc).__name__,
            )
        return _cached


def clear_readiness_cache() -> None:
    """Clear the cached readiness result for tests and controlled reconfiguration."""
    global _cached
    _cached = None
