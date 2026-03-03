"""Startup profiling utilities for chronos dev mode."""

from __future__ import annotations

from collections.abc import Callable
from contextlib import asynccontextmanager, contextmanager
from time import perf_counter


class StartupProfiler:
    """Collect named duration metrics in seconds."""

    def __init__(
        self,
        *,
        metadata: dict[str, str] | None = None,
        now: Callable[[], float] | None = None,
    ) -> None:
        self.metadata = metadata or {}
        self._now = now or perf_counter
        self._starts: dict[str, float] = {}
        self._durations: dict[str, float] = {}

    def start(self, name: str) -> None:
        """Start a named timer."""
        self._starts[name] = self._now()

    def stop(self, name: str) -> float:
        """Stop a named timer and return elapsed seconds.

        Raises:
            ValueError: If no start time exists for `name`.
        """
        started = self._starts.pop(name, None)
        if started is None:
            raise ValueError(f"Timer '{name}' was never started")
        elapsed = max(0.0, self._now() - started)
        self.record(name, elapsed)
        return elapsed

    def record(self, name: str, seconds: float) -> None:
        """Record (accumulate) a duration for a metric name."""
        self._durations[name] = self._durations.get(name, 0.0) + max(0.0, seconds)

    @contextmanager
    def time(self, name: str):
        """Context manager that records elapsed time for `name`."""
        self.start(name)
        try:
            yield
        finally:
            self.stop(name)

    @asynccontextmanager
    async def atime(self, name: str):
        """Async context manager that records elapsed time for `name`."""
        self.start(name)
        try:
            yield
        finally:
            self.stop(name)

    def durations(self) -> dict[str, float]:
        """Return a copy of all recorded durations in seconds."""
        return dict(self._durations)

    def sorted_durations(
        self,
        *,
        exclude: set[str] | None = None,
    ) -> list[tuple[str, float]]:
        """Return durations sorted descending by elapsed time."""
        exclude = exclude or set()
        rows = [(name, value) for name, value in self._durations.items() if name not in exclude]
        rows.sort(key=lambda item: item[1], reverse=True)
        return rows
