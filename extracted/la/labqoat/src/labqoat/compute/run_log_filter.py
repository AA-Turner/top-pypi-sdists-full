"""Prevent existing console handlers from duplicating captured application records."""

import logging
from contextvars import ContextVar

from labqoat.compute.run_telemetry import RunTelemetry


class RunLogFilter(logging.Filter):
    """Keep ordinary process logging intact whenever no invocation owns the current task."""

    def __init__(self, sinks: ContextVar[tuple[RunTelemetry, ...]]) -> None:
        """Retain the worker's invocation context."""
        super().__init__()
        self._sinks = sinks

    def filter(self, record: logging.LogRecord) -> bool:
        """Suppress console duplicates only while a run receives structured records."""
        return not self._sinks.get()
