"""Runtime ID management for tracking execution contexts.

This module provides a decorator-based system for generating and managing random
runtime IDs throughout the execution context of your application.
"""
import functools
import inspect
import logging
import os
import random
from contextvars import ContextVar
from typing import TypeVar, ParamSpec, Callable, Any

P = ParamSpec('P')
R = TypeVar('R')

_RUNTIME_ID_CTX: ContextVar[str | None] = ContextVar("token__runtime__id", default=None)
_RUNTIME_DEPTH_CTX: ContextVar[int] = ContextVar("token__runtime__depth", default=0)


class RuntimeIdException(Exception):
    """Exception raised when runtime ID operations fail."""

class RuntimeIdLogFilter(logging.Filter):
    """Logging filter that injects the current runtime ID into log records."""

    def __init__(self, record_attr_name: str = "runtime_id"):
        """Initialize the log filter.

        Args:
            record_attr_name (str): The name of the attribute to inject into the LogRecord.

        Raises:
            ValueError: If record_attr_name is not a valid Python identifier.
        """
        super().__init__()

        if not isinstance(record_attr_name, str) or not record_attr_name.isidentifier():
            raise ValueError('record_attr_name must be a valid Python identifier')

        self._record_attr_name = record_attr_name

    def filter(self, record: logging.LogRecord) -> bool:
        setattr(record, self._record_attr_name, get_runtime_id())
        return True



def _get_random_string(length: int, characters: str) -> str:
    return ''.join(random.choices(characters, k=length))


def runtime_id(
    method: Callable[P, R] | None = None,
    *,
    length: int = 8,
    prefix_process_id: bool = False,
    prefix: str | None = None,
    characters: str = "0123456789abcdefghijklmnopqrstuvwxyz",
    max_depth: int = 3,
    sep: str = ":",
) -> Any:
    """Decorator to generate and manage a random runtime ID for the execution context.

    This decorator sets a context-local runtime ID variable. If an ID already exists
    in the context (nested call), a new segment is appended to the existing ID.
    If no ID exists, a new root ID is generated.

    Args:
        method (Callable, optional): The function to decorate.
        length (int, optional): The length of the random string segment generated for this call. Defaults to 8.
        prefix_process_id (bool, optional): If True and this is the root ID, prepends the OS Process ID.
        prefix (str | None, optional): A static string to prepend to the root ID.
        characters (str, optional): The pool of characters used to generate the random string.
        max_depth (int, optional): The maximum allowed nesting depth.
        sep (str, optional): The separator used between ID segments.

    Returns:
        Callable: The wrapped function.

    Raises:
        ValueError: If configuration arguments are invalid.
        RuntimeIdException: When the max_depth value is exceeded.

    Examples:
        Basic usage:
            >>> @runtime_id()
            ... def my_func():
            ...     print(get_runtime_id())
            # Output: a1b2c3d4

        With configuration:
            >>> @runtime_id(length=4, prefix="APP", prefix_process_id=True)
            ... def my_func():
            ...     print(get_runtime_id())
            # Output: 12345:APP:a1b2

        Nesting:
            >>> @runtime_id
            ... def parent():
            ...     child()
            >>> @runtime_id
            ... def child():
            ...     print(get_runtime_id())
            # Output: roothash:childhash
    """
    if method is None:
        return functools.partial(  # pyright: ignore[reportReturnType]
            runtime_id,
            length=length,
            prefix_process_id=prefix_process_id,
            prefix=prefix,
            characters=characters,
            max_depth=max_depth,
            sep=sep
        )

    if not isinstance(length, int) or length <= 0:
        raise ValueError('length must be an integer greater than 0')
    if not isinstance(max_depth, int) or max_depth <= 0:
        raise ValueError('max_depth must be an integer greater than 0')
    if not isinstance(characters, str) or len(characters) < 1:
        raise ValueError('characters must be a non-empty string')
    if not isinstance(sep, str) or len(sep) < 1:
        raise ValueError('sep must be a non-empty string')
    if not isinstance(prefix_process_id, bool):
        raise ValueError('prefix_process_id must be a boolean')
    if prefix is not None and (not isinstance(prefix, str) or len(prefix) < 1):
        raise ValueError('prefix must be None or a non-empty string')


    def _push_ids() -> tuple:  # pyright: ignore[reportMissingTypeArgument]
        rid = get_runtime_id()

        if rid is None:
            rid = ""
            depth = 0

            if prefix_process_id:
                rid += str(os.getpid()) + sep
            if prefix:
                rid += prefix + sep
        else:
            depth = _RUNTIME_DEPTH_CTX.get()

            if depth >= max_depth:
                raise RuntimeIdException(f"Max depth of {max_depth} is reached. Current id {rid}, depth {depth}")

            rid += sep

        rid += _get_random_string(length, characters)

        return (
            _RUNTIME_ID_CTX.set(rid),
            _RUNTIME_DEPTH_CTX.set(depth + 1)
        )

    def _pop_ids(tokens: tuple) -> None:  # pyright: ignore[reportMissingTypeArgument]
        _RUNTIME_ID_CTX.reset(tokens[0])
        _RUNTIME_DEPTH_CTX.reset(tokens[1])


    if inspect.iscoroutinefunction(method):
        @functools.wraps(method)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            tokens = _push_ids()

            try:
                return await method(*args, **kwargs)
            finally:
                _pop_ids(tokens)

        wrapper_method = async_wrapper
    else:
        @functools.wraps(method)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            tokens = _push_ids()

            try:
                return method(*args, **kwargs)
            finally:
                _pop_ids(tokens)

        wrapper_method = wrapper

    return wrapper_method


def get_runtime_id() -> str | None:
    """Retrieves the current Runtime ID from the context."""
    return _RUNTIME_ID_CTX.get()

def require_runtime_id() -> str:
    """Retrieves the ID or raises an exception if not set."""
    rid = get_runtime_id()

    if rid is None:
        raise RuntimeIdException('RuntimeId is required but it was not set.')

    return rid
