r"""Implement some utility functions to manage optional dependencies."""

from __future__ import annotations

__all__ = ["check_joblib", "is_joblib_available", "joblib_available", "raise_error_joblib_missing"]

from importlib.util import find_spec
from typing import TYPE_CHECKING, Any, NoReturn

from coola.utils.imports import decorator_package_available

if TYPE_CHECKING:
    from collections.abc import Callable


def check_joblib() -> None:
    r"""Check if the ``joblib`` package is installed.

    Raises:
        RuntimeError: if the ``joblib`` package is not installed.

    Example:
        ```pycon
        >>> from iden.utils.imports import check_joblib
        >>> check_joblib()

        ```
    """
    if not is_joblib_available():
        raise_error_joblib_missing()


def is_joblib_available() -> bool:
    r"""Indicate if the ``joblib`` package is installed or not.

    Returns:
        ``True`` if ``joblib`` is available otherwise ``False``.

    Example:
        ```pycon
        >>> from iden.utils.imports import is_joblib_available
        >>> is_joblib_available()

        ```
    """
    return find_spec("joblib") is not None


def joblib_available(fn: Callable[..., Any]) -> Callable[..., Any]:
    r"""Implement a decorator to execute a function only if ``joblib``
    package is installed.

    Args:
        fn: The function to execute.

    Returns:
        A wrapper around ``fn`` if ``joblib`` package is installed,
            otherwise ``None``.

    Example:
        ```pycon
        >>> from iden.utils.imports import joblib_available
        >>> @joblib_available
        ... def my_function(n: int = 0) -> int:
        ...     return 42 + n
        ...
        >>> my_function()

        ```
    """
    return decorator_package_available(fn, is_joblib_available)


def raise_error_joblib_missing() -> NoReturn:
    r"""Raise a RuntimeError to indicate the ``joblib`` package is
    missing."""
    msg = (
        "'joblib' package is required but not installed. "
        "The 'joblib' package can be installed with the command:\n\n"
        "pip install joblib\n"
    )
    raise RuntimeError(msg)
