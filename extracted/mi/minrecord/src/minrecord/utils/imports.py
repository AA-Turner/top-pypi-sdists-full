r"""Implement some utility functions to manage optional dependencies."""

from __future__ import annotations

__all__ = [
    "check_objectory",
    "is_objectory_available",
    "objectory_available",
    "raise_error_objectory_missing",
]

from typing import TYPE_CHECKING, Any, NoReturn

from coola.utils.imports import decorator_package_available, package_available

if TYPE_CHECKING:
    from collections.abc import Callable


#####################
#     objectory     #
#####################


def is_objectory_available() -> bool:
    r"""Indicate if the ``objectory`` package is installed or not.

    Returns:
        ``True`` if ``objectory`` is available otherwise ``False``.

    Example:
        ```pycon
        >>> from minrecord.utils.imports import is_objectory_available
        >>> is_objectory_available()

        ```
    """
    return package_available("objectory")


def check_objectory() -> None:
    r"""Check if the ``objectory`` package is installed.

    Raises:
        RuntimeError: if the ``objectory`` package is not installed.

    Example:
        ```pycon
        >>> from minrecord.utils.imports import check_objectory
        >>> check_objectory()

        ```
    """
    if not is_objectory_available():
        raise_error_objectory_missing()


def objectory_available(fn: Callable[..., Any]) -> Callable[..., Any]:
    r"""Implement a decorator to execute a function only if ``objectory``
    package is installed.

    Args:
        fn: The function to execute.

    Returns:
        A wrapper around ``fn`` if ``objectory`` package is installed,
            otherwise ``None``.

    Example:
        ```pycon
        >>> from minrecord.utils.imports import objectory_available
        >>> @objectory_available
        ... def my_function(n: int = 0) -> int:
        ...     return 42 + n
        ...
        >>> my_function()

        ```
    """
    return decorator_package_available(fn, is_objectory_available)


def raise_error_objectory_missing() -> NoReturn:
    r"""Raise a RuntimeError to indicate the ``objectory`` package is
    missing."""
    msg = (
        "'objectory' package is required but not installed. "
        "You can install 'objectory' package with the command:\n\n"
        "pip install objectory\n"
    )
    raise RuntimeError(msg)
