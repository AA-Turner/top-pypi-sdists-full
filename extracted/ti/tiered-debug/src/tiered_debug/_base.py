"""Base implementation for tiered debug logging.

The `TieredDebug` class provides multi-level debug logging with
configurable stack tracing for accurate caller reporting. It supports
logging at levels 1-5, with level 1 always logged and levels 2-5
conditional on the configured debug level. Designed for projects like
ElasticKeeper and ElasticCheckpoint, it allows flexible logger
configuration and stack level adjustments.

Examples:
    >>> from tiered_debug._base import TieredDebug
    >>> debug = TieredDebug(level=2)
    >>> debug.level
    2
    >>> import logging
    >>> handler = logging.StreamHandler()
    >>> debug.add_handler(
    ...     handler, logging.Formatter("%(message)s")
    ... )
    >>> debug.lv1("Always logged")
    >>> debug.lv3("Not logged")  # Ignored (level 3 > 2)
"""

# pylint: disable=R0913,R0917,W0212
import logging
import sys
from contextlib import contextmanager
from functools import lru_cache
from typing import Any, Dict, Iterator, Literal, Optional

import platform

DebugLevel = Literal[1, 2, 3, 4, 5]
"""Type hint for debug level (1-5)."""

DEFAULTS = {"debug": 1, "stack": 3}
"""Default values for debug level (1) and stack level (3)."""


class TieredDebug:
    """Tiered debug logging with configurable levels and stack tracing.

    Supports debug logging at levels 1-5, with level 1 always logged and
    levels 2-5 conditional on the configured debug level. Allows custom
    stack levels for accurate caller reporting and flexible logger
    configuration via handlers.

    Args:
        level: Debug level (1-5, default 1). (int)
        stacklevel: Stack level for caller reporting (1-9, default 3). (int)
        logger_name: Name for the logger (default "tiered_debug._base"). (str)

    Attributes:
        level: Current debug level (1-5). (int)
        stacklevel: Current stack level for caller reporting (1-9). (int)
        logger: Configured logger instance. (logging.Logger)

    Examples:
        >>> debug = TieredDebug(level=2)
        >>> debug.level
        2
        >>> import logging
        >>> handler = logging.StreamHandler()
        >>> debug.add_handler(
        ...     handler, logging.Formatter("%(message)s")
        ... )
        >>> debug.lv1("Level 1 message")
        >>> debug.lv3("Level 3 message")  # Not logged
    """

    def __init__(
        self,
        level: int = DEFAULTS["debug"],
        stacklevel: int = DEFAULTS["stack"],
        logger_name: str = "tiered_debug._base",
    ) -> None:
        """Initialize a TieredDebug instance with specified settings."""
        self._logger = logging.getLogger(logger_name)
        self._level = self.check_val(level, "debug")
        self._stacklevel = self.check_val(stacklevel, "stack")

    @property
    def level(self) -> int:
        """Get the current debug level (1-5).

        Returns:
            int: Current debug level.

        Examples:
            >>> debug = TieredDebug(level=3)
            >>> debug.level
            3
        """
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        """Set the debug level, validating it is between 1 and 5.

        Args:
            value: Debug level to set (1-5). (int)
        """
        self._level = self.check_val(value, "debug")

    @property
    def stacklevel(self) -> int:
        """Get the current stack level for caller reporting (1-9).

        Returns:
            int: Current stack level.

        Examples:
            >>> debug = TieredDebug(stacklevel=4)
            >>> debug.stacklevel
            4
        """
        return self._stacklevel

    @stacklevel.setter
    def stacklevel(self, value: int) -> None:
        """Set the stack level, validating it is between 1 and 9.

        Args:
            value: Stack level to set (1-9). (int)
        """
        self._stacklevel = self.check_val(value, "stack")

    @property
    def logger(self) -> logging.Logger:
        """Get the configured logger instance.

        Returns:
            logging.Logger: Logger instance for this TieredDebug object.

        Examples:
            >>> debug = TieredDebug()
            >>> isinstance(debug.logger, logging.Logger)
            True
        """
        return self._logger

    def check_val(self, val: int, kind: str) -> int:
        """Validate and return a debug or stack level, or default if invalid.

        Args:
            val: Value to validate. (int)
            kind: Type of value ("debug" or "stack"). (str)

        Returns:
            int: Validated value or default if invalid.

        Raises:
            ValueError: If kind is neither "debug" nor "stack".

        Examples:
            >>> debug = TieredDebug()
            >>> debug.check_val(3, "debug")
            3
            >>> debug.check_val(0, "debug")  # Invalid, returns default
            1
        """
        if kind == "debug":
            valid = 1 <= val <= 5
        elif kind == "stack":
            valid = 1 <= val <= 9
        else:
            raise ValueError(f"Invalid kind: {kind}. Must be 'debug' or 'stack'")

        if not valid:
            self.logger.warning(
                f"Invalid {kind} level: {val}. Using default: {DEFAULTS[kind]}"
            )
            return DEFAULTS[kind]
        return val

    def add_handler(
        self,
        handler: logging.Handler,
        formatter: Optional[logging.Formatter] = None,
    ) -> None:
        """Add a handler to the logger if not already present.

        Args:
            handler: Handler to add to the logger. (logging.Handler)
            formatter: Optional formatter for the handler. (logging.Formatter)

        Examples:
            >>> debug = TieredDebug()
            >>> import logging
            >>> handler = logging.StreamHandler()
            >>> debug.add_handler(handler)
            >>> handler in debug.logger.handlers
            True
        """
        if handler not in self.logger.handlers:
            if formatter:
                handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            self.logger.addHandler(handler)
        else:
            self.logger.info("Handler already attached to logger, skipping")

    @lru_cache(maxsize=1)
    def _select_frame_getter(self) -> Any:
        """Select the appropriate frame getter based on Python implementation.

        Returns:
            Callable: sys._getframe for CPython, inspect.currentframe otherwise.

        Examples:
            >>> debug = TieredDebug()
            >>> import platform
            >>> if platform.python_implementation() == "CPython":
            ...     assert debug._select_frame_getter() is sys._getframe
        """
        return (
            sys._getframe
            if platform.python_implementation() == "CPython"
            else sys.modules["inspect"].currentframe
        )

    def _get_logger_name(self, stack_level: int) -> str:
        """Get the module name from the call stack at the specified level.

        Args:
            stack_level: Stack level to inspect (1-9). (int)

        Returns:
            str: Module name or "unknown" if not found.

        Examples:
            >>> debug = TieredDebug()
            >>> debug._get_logger_name(1)
            '__main__'
        """
        try:
            frame = self._select_frame_getter()(stack_level)
            return frame.f_globals.get("__name__", "unknown")
        except (ValueError, AttributeError):
            return "unknown"

    @contextmanager
    def change_level(self, level: int) -> Iterator[None]:
        """Temporarily change the debug level within a context.

        Args:
            level: Debug level to set temporarily (1-5). (int)

        Examples:
            >>> debug = TieredDebug(level=2)
            >>> with debug.change_level(4):
            ...     assert debug.level == 4
            >>> debug.level
            2
        """
        original_level = self.level
        self.level = level
        try:
            yield
        finally:
            self.level = original_level

    def log(
        self,
        level: DebugLevel,
        msg: str,
        *args,
        exc_info: Optional[bool] = None,
        stack_info: Optional[bool] = None,
        stacklevel: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a message at the specified debug level.

        Args:
            level: Debug level for the message (1-5). (DebugLevel)
            msg: Message to log, optionally with format specifiers. (str)
            *args: Arguments for message formatting.
            exc_info: Include exception info if True. (bool)
            stack_info: Include stack trace if True. (bool)
            stacklevel: Stack level for caller reporting (1-9). (int)
            extra: Extra metadata dictionary. (Dict[str, Any])

        Raises:
            ValueError: If level is not between 1 and 5.
            TypeError: If extra is not a dictionary or None.

        Examples:
            >>> debug = TieredDebug(level=2)
            >>> import logging
            >>> debug.add_handler(logging.StreamHandler())
            >>> debug.log(1, "Level 1 message: %s", "test")
            >>> debug.log(3, "Level 3 message")  # Not logged
        """
        if not 1 <= level <= 5:
            raise ValueError("Debug level must be 1-5")

        if level > self.level:
            return

        if exc_info is None:
            exc_info = False

        if stack_info is None:
            stack_info = False

        if extra is not None and not isinstance(extra, dict):
            raise TypeError("extra must be a dictionary or None")

        if extra is None:
            extra = {}

        effective_stacklevel = self.stacklevel if stacklevel is None else stacklevel
        effective_stacklevel = self.check_val(effective_stacklevel, "stack")

        logger_name = self._get_logger_name(effective_stacklevel)
        logger = logging.getLogger(logger_name)

        logger.debug(
            f"DEBUG{level} {msg}",
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=effective_stacklevel,
            extra=extra,
        )

    def lv1(
        self,
        msg: str,
        *args,
        exc_info: Optional[bool] = None,
        stack_info: Optional[bool] = None,
        stacklevel: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a message at debug level 1 (always logged).

        Args:
            msg: Message to log, optionally with format specifiers. (str)
            *args: Arguments for message formatting.
            exc_info: Include exception info if True. (bool)
            stack_info: Include stack trace if True. (bool)
            stacklevel: Stack level for caller reporting (1-9). (int)
            extra: Extra metadata dictionary. (Dict[str, Any])

        Raises:
            TypeError: If extra is not a dictionary or None.

        Examples:
            >>> debug = TieredDebug(level=2)
            >>> import logging
            >>> debug.add_handler(logging.StreamHandler())
            >>> debug.lv1("Level 1 message: %s", "test")
        """
        self.log(
            1,
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def lv2(
        self,
        msg: str,
        *args,
        exc_info: Optional[bool] = None,
        stack_info: Optional[bool] = None,
        stacklevel: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a message at debug level 2 (logged if level >= 2).

        Args:
            msg: Message to log, optionally with format specifiers. (str)
            *args: Arguments for message formatting.
            exc_info: Include exception info if True. (bool)
            stack_info: Include stack trace if True. (bool)
            stacklevel: Stack level for caller reporting (1-9). (int)
            extra: Extra metadata dictionary. (Dict[str, Any])

        Raises:
            TypeError: If extra is not a dictionary or None.

        Examples:
            >>> debug = TieredDebug(level=2)
            >>> import logging
            >>> debug.add_handler(logging.StreamHandler())
            >>> debug.lv2("Level 2 message: %s", "test")
        """
        self.log(
            2,
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def lv3(
        self,
        msg: str,
        *args,
        exc_info: Optional[bool] = None,
        stack_info: Optional[bool] = None,
        stacklevel: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a message at debug level 3 (logged if level >= 3).

        Args:
            msg: Message to log, optionally with format specifiers. (str)
            *args: Arguments for message formatting.
            exc_info: Include exception info if True. (bool)
            stack_info: Include stack trace if True. (bool)
            stacklevel: Stack level for caller reporting (1-9). (int)
            extra: Extra metadata dictionary. (Dict[str, Any])

        Raises:
            TypeError: If extra is not a dictionary or None.

        Examples:
            >>> debug = TieredDebug(level=3)
            >>> import logging
            >>> debug.add_handler(logging.StreamHandler())
            >>> debug.lv3("Level 3 message: %s", "test")
        """
        self.log(
            3,
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def lv4(
        self,
        msg: str,
        *args,
        exc_info: Optional[bool] = None,
        stack_info: Optional[bool] = None,
        stacklevel: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a message at debug level 4 (logged if level >= 4).

        Args:
            msg: Message to log, optionally with format specifiers. (str)
            *args: Arguments for message formatting.
            exc_info: Include exception info if True. (bool)
            stack_info: Include stack trace if True. (bool)
            stacklevel: Stack level for caller reporting (1-9). (int)
            extra: Extra metadata dictionary. (Dict[str, Any])

        Raises:
            TypeError: If extra is not a dictionary or None.

        Examples:
            >>> debug = TieredDebug(level=4)
            >>> import logging
            >>> debug.add_handler(logging.StreamHandler())
            >>> debug.lv4("Level 4 message: %s", "test")
        """
        self.log(
            4,
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    def lv5(
        self,
        msg: str,
        *args,
        exc_info: Optional[bool] = None,
        stack_info: Optional[bool] = None,
        stacklevel: Optional[int] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a message at debug level 5 (logged if level >= 5).

        Args:
            msg: Message to log, optionally with format specifiers. (str)
            *args: Arguments for message formatting.
            exc_info: Include exception info if True. (bool)
            stack_info: Include stack trace if True. (bool)
            stacklevel: Stack level for caller reporting (1-9). (int)
            extra: Extra metadata dictionary. (Dict[str, Any])

        Raises:
            TypeError: If extra is not a dictionary or None.

        Examples:
            >>> debug = TieredDebug(level=5)
            >>> import logging
            >>> debug.add_handler(logging.StreamHandler())
            >>> debug.lv5("Level 5 message: %s", "test")
        """
        self.log(
            5,
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )
