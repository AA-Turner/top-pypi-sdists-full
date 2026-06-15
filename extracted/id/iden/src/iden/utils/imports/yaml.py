r"""Implement some utility functions to manage optional dependencies."""

from __future__ import annotations

__all__ = ["check_yaml", "is_yaml_available", "raise_error_yaml_missing", "yaml_available"]

from importlib.util import find_spec
from typing import TYPE_CHECKING, Any, NoReturn

from coola.utils.imports import decorator_package_available

if TYPE_CHECKING:
    from collections.abc import Callable


def check_yaml() -> None:
    r"""Check if the ``yaml`` package is installed.

    Raises:
        RuntimeError: if the ``yaml`` package is not installed.

    Example:
        ```pycon
        >>> from iden.utils.imports import check_yaml
        >>> check_yaml()

        ```
    """
    if not is_yaml_available():
        raise_error_yaml_missing()


def is_yaml_available() -> bool:
    r"""Indicate if the ``yaml`` package is installed or not.

    Returns:
        ``True`` if ``yaml`` is available otherwise ``False``.

    Example:
        ```pycon
        >>> from iden.utils.imports import is_yaml_available
        >>> is_yaml_available()

        ```
    """
    return find_spec("yaml") is not None


def yaml_available(fn: Callable[..., Any]) -> Callable[..., Any]:
    r"""Implement a decorator to execute a function only if ``yaml``
    package is installed.

    Args:
        fn: The function to execute.

    Returns:
        A wrapper around ``fn`` if ``yaml`` package is installed,
            otherwise ``None``.

    Example:
        ```pycon
        >>> from iden.utils.imports import yaml_available
        >>> @yaml_available
        ... def my_function(n: int = 0) -> int:
        ...     return 42 + n
        ...
        >>> my_function()

        ```
    """
    return decorator_package_available(fn, is_yaml_available)


def raise_error_yaml_missing() -> NoReturn:
    r"""Raise a RuntimeError to indicate the ``yaml`` package is
    missing."""
    msg = (
        "'yaml' package is required but not installed. "
        "The 'yaml' package can be installed with the command:\n\n"
        "pip install pyyaml\n"
    )
    raise RuntimeError(msg)
