r"""Implement some utility functions to manage optional dependencies."""

from __future__ import annotations

__all__ = [
    "check_cloudpickle",
    "cloudpickle_available",
    "is_cloudpickle_available",
    "raise_error_cloudpickle_missing",
]

from importlib.util import find_spec
from typing import TYPE_CHECKING, Any, NoReturn

from coola.utils.imports import decorator_package_available

if TYPE_CHECKING:
    from collections.abc import Callable


def check_cloudpickle() -> None:
    r"""Check if the ``cloudpickle`` package is installed.

    Raises:
        RuntimeError: if the ``cloudpickle`` package is not installed.

    Example:
        ```pycon
        >>> from iden.utils.imports import check_cloudpickle
        >>> check_cloudpickle()

        ```
    """
    if not is_cloudpickle_available():
        raise_error_cloudpickle_missing()


def is_cloudpickle_available() -> bool:
    r"""Indicate if the ``cloudpickle`` package is installed or not.

    Returns:
        ``True`` if ``cloudpickle`` is available otherwise ``False``.

    Example:
        ```pycon
        >>> from iden.utils.imports import is_cloudpickle_available
        >>> is_cloudpickle_available()

        ```
    """
    return find_spec("cloudpickle") is not None


def cloudpickle_available(fn: Callable[..., Any]) -> Callable[..., Any]:
    r"""Implement a decorator to execute a function only if
    ``cloudpickle`` package is installed.

    Args:
        fn: The function to execute.

    Returns:
        A wrapper around ``fn`` if ``cloudpickle`` package is installed,
            otherwise ``None``.

    Example:
        ```pycon
        >>> from iden.utils.imports import cloudpickle_available
        >>> @cloudpickle_available
        ... def my_function(n: int = 0) -> int:
        ...     return 42 + n
        ...
        >>> my_function()

        ```
    """
    return decorator_package_available(fn, is_cloudpickle_available)


def raise_error_cloudpickle_missing() -> NoReturn:
    r"""Raise a RuntimeError to indicate the ``cloudpickle`` package is
    missing."""
    msg = (
        "'cloudpickle' package is required but not installed. "
        "The 'cloudpickle' package can be installed with the command:\n\n"
        "pip install cloudpickle\n"
    )
    raise RuntimeError(msg)
