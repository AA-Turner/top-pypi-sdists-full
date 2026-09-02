"""Thread-safe phase timing for the device scan."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager

import structlog

logger = structlog.get_logger(__name__)


class PhaseTimer:
    """Collect named phase durations from concurrent scan workers."""

    def __init__(self, clock: Callable[[], float] = time.perf_counter) -> None:
        self._clock = clock
        self._durations_ms: dict[str, int] = {}
        self._lock = threading.Lock()

    @contextmanager
    def phase(self, name: str) -> Iterator[None]:
        """Time one phase and record it even when the phase raises."""
        started_at = self._clock()
        try:
            yield
        finally:
            duration_ms = max(0, int((self._clock() - started_at) * 1000))
            self.record(name, duration_ms)

    def record(self, name: str, duration_ms: int) -> None:
        """Record a phase duration."""
        with self._lock:
            self._durations_ms[name] = duration_ms
        logger.info(
            "scan_phase_complete",
            phase=name,
            duration_ms=duration_ms,
        )

    def durations_ms(self) -> dict[str, int]:
        """Return a stable snapshot of all recorded durations."""
        with self._lock:
            return dict(sorted(self._durations_ms.items()))
