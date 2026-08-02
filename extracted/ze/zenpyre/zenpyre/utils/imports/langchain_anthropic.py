r"""Contain utilities for optional langchain_anthropic dependency."""

from __future__ import annotations

__all__ = [
    "check_langchain_anthropic",
    "is_langchain_anthropic_available",
    "langchain_anthropic_available",
    "raise_langchain_anthropic_missing_error",
]

from functools import lru_cache
from typing import TYPE_CHECKING, Any, NoReturn, TypeVar

from coola.utils.imports import (
    decorator_package_available,
    package_available,
    raise_package_missing_error,
)

if TYPE_CHECKING:
    from collections.abc import Callable

F = TypeVar("F", bound="Callable[..., Any]")


def check_langchain_anthropic() -> None:
    r"""Check if the ``langchain_anthropic`` package is installed.

    Raises:
        RuntimeError: if the ``langchain_anthropic`` package is not installed.

    Example:
        ```pycon
        >>> from zenpyre.utils.imports import check_langchain_anthropic
        >>> check_langchain_anthropic()

        ```
    """
    if not is_langchain_anthropic_available():
        raise_langchain_anthropic_missing_error()


@lru_cache(1)
def is_langchain_anthropic_available() -> bool:
    r"""Indicate if the ``langchain_anthropic`` package is installed or
    not.

    Returns:
        ``True`` if ``langchain_anthropic`` is available otherwise ``False``.

    Example:
        ```pycon
        >>> from zenpyre.utils.imports import is_langchain_anthropic_available
        >>> is_langchain_anthropic_available()

        ```
    """
    return package_available("langchain_anthropic")


def langchain_anthropic_available(fn: F) -> F:
    r"""Implement a decorator to execute a function only if
    ``langchain_anthropic`` package is installed.

    Args:
        fn: The function to execute.

    Returns:
        A wrapper around ``fn`` if ``langchain_anthropic`` package is installed,
            otherwise ``None``.

    Example:
        ```pycon
        >>> from zenpyre.utils.imports import langchain_anthropic_available
        >>> @langchain_anthropic_available
        ... def my_function(n: int = 0) -> int:
        ...     return 42 + n
        ...
        >>> my_function()

        ```
    """
    return decorator_package_available(fn, is_langchain_anthropic_available)


def raise_langchain_anthropic_missing_error() -> NoReturn:
    r"""Raise a RuntimeError to indicate the ``langchain_anthropic``
    package is missing."""
    raise_package_missing_error("langchain_anthropic", "langchain-anthropic")
