"""Abstract base class for pluggable logging framework adapters."""

from __future__ import annotations

import abc
from typing import Callable


class LoggingAdapter(abc.ABC):
    """Contract for pluggable logging framework integration.

    Adapters bridge the smplkit logging runtime to a specific logging
    framework (e.g., stdlib ``logging``, loguru). Implement this
    interface to add support for a new logging framework.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Human-readable adapter name for diagnostics (e.g., 'stdlib-logging')."""

    @abc.abstractmethod
    def discover(self) -> list[tuple[str, int | None, int]]:
        """Scan the runtime for existing loggers.

        Returns a list of (logger_name, explicit_level_or_None, effective_level) tuples.

        - explicit_level_or_None: the raw numeric level set on the logger, or None if
          the logger has no explicit level (inherits from parent / framework default).
        - effective_level: the resolved numeric level the framework uses for this logger,
          accounting for inheritance. Always non-None.
        """

    @abc.abstractmethod
    def apply_level(self, logger_name: str, level: int) -> None:
        """Set the level on a specific logger.

        Args:
            logger_name: The logger name.
            level: Python numeric level (e.g., 10=DEBUG, 20=INFO, 30=WARNING).
        """

    @abc.abstractmethod
    def install_hook(self, on_new_logger: Callable[[str, int | None, int], None]) -> None:
        """Install continuous discovery hook.

        The callback should be invoked with (logger_name, explicit_level_or_None,
        effective_level) whenever a new logger is created in the framework.
        explicit_level_or_None is None when the logger has no explicitly set level.

        May be a no-op if the framework doesn't support creation interception.
        """

    @abc.abstractmethod
    def uninstall_hook(self) -> None:
        """Remove the hook installed by install_hook(). Called on client close()."""
