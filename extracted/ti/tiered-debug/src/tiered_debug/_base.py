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
import platform
import sys
from collections.abc import Callable, Generator, Mapping
from contextlib import contextmanager
from types import TracebackType
from typing import TYPE_CHECKING, Any, Literal, TypeAlias

_SysExcInfoType: TypeAlias = tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None]
_ExcInfoType: TypeAlias = bool | _SysExcInfoType | BaseException | None

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

    # Type stubs for dynamic methods (visible to type checkers)
    if TYPE_CHECKING:
        lv1: Callable[..., None]  # pyright: ignore[reportUninitializedInstanceVariable]
        lv2: Callable[..., None]  # pyright: ignore[reportUninitializedInstanceVariable]
        lv3: Callable[..., None]  # pyright: ignore[reportUninitializedInstanceVariable]
        lv4: Callable[..., None]  # pyright: ignore[reportUninitializedInstanceVariable]
        lv5: Callable[..., None]  # pyright: ignore[reportUninitializedInstanceVariable]

    def __init__(
        self,
        level: int = DEFAULTS["debug"],
        stacklevel: int = DEFAULTS["stack"],
        logger_name: str = "tiered_debug._base",
    ) -> None:
        """Initialize a TieredDebug instance with specified settings."""
        self.logger: logging.Logger = logging.getLogger(logger_name)
        self._level: int = self.check_val(level, "debug")
        self._stacklevel: int = self.check_val(stacklevel, "stack")

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
        formatter: logging.Formatter | None = None,
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
            self.logger.info("Handler added to logger")
        else:
            self.logger.info("Handler already attached to logger, skipping")

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
            sys._getframe  # pyright: ignore[reportPrivateUsage]
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
        except (ValueError, AttributeError) as e:
            self.logger.debug(f"Failed to access frame at level {stack_level}: {e}")
            return "unknown"

    @contextmanager
    def change_level(self, level: int) -> Generator[None, None, None]:
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
        self.level = self.check_val(level, "debug")
        try:
            yield
        finally:
            self.level = original_level

    def log(
        self,
        level: DebugLevel,
        msg: Any,
        *args: Any,
        exc_info: _ExcInfoType = None,
        stack_info: bool | None = False,
        stacklevel: int | None = None,
        extra: Mapping[str, object] | None = None,
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

        if stack_info is None:
            stack_info = False

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


def _make_lv_method(level: int) -> Any:
    """Create a level-specific logging method.

    Args:
        level: Debug level (1-5).

    Returns:
        Callable: Method bound to the given level.
    """
    doc_template = """Log a message at debug level {level}.

    Args:
        msg: Message to log, optionally with format specifiers. (str)
        *args: Arguments for message formatting.
        exc_info: Include exception info if True. (bool)
        stack_info: Include stack trace if True. (bool)
        stacklevel: Stack level for caller reporting (1-9). (int)
        extra: Extra metadata dictionary. (Dict[str, Any])
    """

    def lv_method(
        # We ignore these types because we're dynamically adding these methods
        self,  # pyright: ignore[reportMissingParameterType,reportUnknownParameterType]
        msg: Any,
        *args: Any,
        exc_info: _ExcInfoType = None,
        stack_info: bool | None = False,
        stacklevel: int | None = None,
        extra: Mapping[str, object] | None = None,
    ) -> None:
        """Log a message at debug level {level}."""
        # UnknownMemberType because it's dynamically added
        self.log(  # pyright: ignore[reportUnknownMemberType]
            level,
            msg,
            *args,
            exc_info=exc_info,
            stack_info=stack_info,
            stacklevel=stacklevel,
            extra=extra,
        )

    lv_method.__name__ = f"lv{level}"
    lv_method.__qualname__ = f"TieredDebug.lv{level}"
    lv_method.__doc__ = doc_template.format(level=level)
    # Unknown because we're dynamically addding methods to the class.
    return lv_method  # pyright: ignore[reportUnknownVariableType]


# Dynamically generate lv1 through lv5 methods
for _lvl in range(1, 6):
    setattr(TieredDebug, f"lv{_lvl}", _make_lv_method(_lvl))
