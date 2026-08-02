r"""Contain utilities for optional persista dependency."""

from __future__ import annotations

__all__ = [
    "check_persista",
    "is_persista_available",
    "persista_available",
    "raise_persista_missing_error",
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


def check_persista() -> None:
    r"""Check if the ``persista`` package is installed.

    Raises:
        RuntimeError: if the ``persista`` package is not installed.

    Example:
        ```pycon
        >>> from zenpyre.utils.imports import check_persista
        >>> check_persista()

        ```
    """
    if not is_persista_available():
        raise_persista_missing_error()


@lru_cache(1)
def is_persista_available() -> bool:
    r"""Indicate if the ``persista`` package is installed or not.

    Returns:
        ``True`` if ``persista`` is available otherwise ``False``.

    Example:
        ```pycon
        >>> from zenpyre.utils.imports import is_persista_available
        >>> is_persista_available()

        ```
    """
    return package_available("persista")


def persista_available(fn: F) -> F:
    r"""Implement a decorator to execute a function only if ``persista``
    package is installed.

    Args:
        fn: The function to execute.

    Returns:
        A wrapper around ``fn`` if ``persista`` package is installed,
            otherwise ``None``.

    Example:
        ```pycon
        >>> from zenpyre.utils.imports import persista_available
        >>> @persista_available
        ... def my_function(n: int = 0) -> int:
        ...     return 42 + n
        ...
        >>> my_function()

        ```
    """
    return decorator_package_available(fn, is_persista_available)


def raise_persista_missing_error() -> NoReturn:
    r"""Raise a RuntimeError to indicate the ``persista`` package is
    missing."""
    raise_package_missing_error("persista", "persista")
