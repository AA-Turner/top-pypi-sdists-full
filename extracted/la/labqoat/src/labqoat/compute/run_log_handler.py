"""Preserve Python logging severity and exception evidence under task-local run authority."""

import logging
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Literal

from labqoat.compute.run_telemetry import RunTelemetry
from labqoat.training.run_log_record import RunLogRecord


class RunLogHandler(logging.Handler):
    """Route one Python record directly to each bound input without reprinting it to stdout."""

    def __init__(self, sinks: ContextVar[tuple[RunTelemetry, ...]]) -> None:
        """Bind the worker's explicit context without changing global logger configuration."""
        super().__init__(logging.DEBUG)
        self._sinks = sinks

    def emit(self, record: logging.LogRecord) -> None:
        """Keep a producer timestamp and traceback for every bounded fragment of a record."""
        sinks = self._sinks.get()
        if not sinks:
            return
        message = record.getMessage()
        if record.exc_info:
            message += "\n" + logging.Formatter().formatException(record.exc_info)
        for start in range(0, len(message), 16000):
            entry = RunLogRecord(
                message[start : start + 16000],
                level=self.level_name(record.levelno),
                stream="logging",
                logger=record.name[:256],
                produced_at=datetime.fromtimestamp(record.created, UTC),
            )
            for sink in sinks:
                sink.logs.log_record(entry)

    @staticmethod
    def level_name(number: int) -> Literal["critical", "error", "warning", "info", "debug"]:
        """Map numeric Python severities to their standard threshold without inspecting message text."""
        levels: tuple[tuple[int, Literal["critical", "error", "warning", "info"]], ...] = (
            (50, "critical"),
            (40, "error"),
            (30, "warning"),
            (20, "info"),
        )
        for threshold, name in levels:
            if number >= threshold:
                return name
        return "debug"
