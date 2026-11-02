"""Install and restore scoped Python logging capture for a physical worker."""

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

from labqoat.compute.run_log_filter import RunLogFilter
from labqoat.compute.run_log_handler import RunLogHandler
from labqoat.compute.run_telemetry import RunTelemetry


class LoggingRouting:
    """Preserve existing handlers and levels while capturing task-owned records exactly once."""

    def __init__(self, sinks: ContextVar[tuple[RunTelemetry, ...]]) -> None:
        """Prepare capture adapters without modifying process logging."""
        self._handler = RunLogHandler(sinks)
        self._filter = RunLogFilter(sinks)

    @contextmanager
    def installed(self) -> Iterator[None]:
        """Capture existing non-propagating loggers as well as future ordinary child loggers."""
        root = logging.getLogger()
        loggers = [root, *self._loggers()]
        targets = [logger for logger in loggers if logger is root or not logger.propagate]
        console = {
            handler for logger in loggers for handler in logger.handlers if type(handler) is logging.StreamHandler
        }
        level = root.level
        quieted: list[logging.Logger] = []
        if not root.handlers and level == logging.WARNING:
            root.setLevel(logging.INFO)
            quieted = self._quiet()
        for handler in console:
            handler.addFilter(self._filter)
        for logger in targets:
            logger.addHandler(self._handler)
        try:
            yield
        finally:
            for logger in targets:
                logger.removeHandler(self._handler)
            for handler in console:
                handler.removeFilter(self._filter)
            root.setLevel(level)
            for logger in quieted:
                logger.setLevel(logging.NOTSET)
            self._handler.close()

    @staticmethod
    def _quiet() -> list[logging.Logger]:
        """Per-request lines from HTTP libraries are not the author's output unless they configured them."""
        chatty = [logging.getLogger(name) for name in ("httpx", "httpcore", "urllib3")]
        unset = [logger for logger in chatty if logger.level == logging.NOTSET]
        for logger in unset:
            logger.setLevel(logging.WARNING)
        return unset

    @staticmethod
    def _loggers() -> list[logging.Logger]:
        """Snapshot registered loggers; placeholders do not own handlers."""
        return [item for item in logging.Logger.manager.loggerDict.values() if isinstance(item, logging.Logger)]
