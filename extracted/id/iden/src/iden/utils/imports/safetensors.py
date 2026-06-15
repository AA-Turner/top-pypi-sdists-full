r"""Implement some utility functions to manage optional dependencies."""

from __future__ import annotations

__all__ = [
    "check_safetensors",
    "is_safetensors_available",
    "raise_error_safetensors_missing",
    "safetensors_available",
]

from importlib.util import find_spec
from typing import TYPE_CHECKING, Any, NoReturn

from coola.utils.imports import decorator_package_available

if TYPE_CHECKING:
    from collections.abc import Callable


def check_safetensors() -> None:
    r"""Check if the ``safetensors`` package is installed.

    Raises:
        RuntimeError: if the ``safetensors`` package is not installed.

    Example:
        ```pycon
        >>> from iden.utils.imports import check_safetensors
        >>> check_safetensors()

        ```
    """
    if not is_safetensors_available():
        raise_error_safetensors_missing()


def is_safetensors_available() -> bool:
    r"""Indicate if the ``safetensors`` package is installed or not.

    Returns:
        ``True`` if ``safetensors`` is available otherwise ``False``.

    Example:
        ```pycon
        >>> from iden.utils.imports import is_safetensors_available
        >>> is_safetensors_available()

        ```
    """
    return find_spec("safetensors") is not None


def safetensors_available(fn: Callable[..., Any]) -> Callable[..., Any]:
    r"""Implement a decorator to execute a function only if
    ``safetensors`` package is installed.

    Args:
        fn: The function to execute.

    Returns:
        A wrapper around ``fn`` if ``safetensors`` package is installed,
            otherwise ``None``.

    Example:
        ```pycon
        >>> from iden.utils.imports import safetensors_available
        >>> @safetensors_available
        ... def my_function(n: int = 0) -> int:
        ...     return 42 + n
        ...
        >>> my_function()

        ```
    """
    return decorator_package_available(fn, is_safetensors_available)


def raise_error_safetensors_missing() -> NoReturn:
    r"""Raise a RuntimeError to indicate the ``safetensors`` package is
    missing."""
    msg = (
        "'safetensors' package is required but not installed. "
        "The 'safetensors' package can be installed with the command:\n\n"
        "pip install safetensors\n"
    )
    raise RuntimeError(msg)
