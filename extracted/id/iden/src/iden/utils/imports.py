r"""Implement some utility functions to manage optional dependencies."""

from __future__ import annotations

__all__ = [
    "check_safetensors",
    "check_yaml",
    "is_safetensors_available",
    "is_yaml_available",
    "safetensors_available",
    "yaml_available",
]

from importlib.util import find_spec
from typing import TYPE_CHECKING, Any

from coola.utils.imports import decorator_package_available

if TYPE_CHECKING:
    from collections.abc import Callable

#######################
#     safetensors     #
#######################


def is_safetensors_available() -> bool:
    r"""Indicate if the ``safetensors`` package is installed or not.

    Returns:
        ``True`` if ``safetensors`` is available otherwise ``False``.

    Example usage:

    ```pycon
    >>> from iden.utils.imports import is_safetensors_available
    >>> is_safetensors_available()

    ```
    """
    return find_spec("safetensors") is not None


def check_safetensors() -> None:
    r"""Check if the ``safetensors`` package is installed.

    Raises:
        RuntimeError: if the ``safetensors`` package is not installed.

    Example usage:

    ```pycon
    >>> from iden.utils.imports import check_safetensors
    >>> check_safetensors()

    ```
    """
    if not is_safetensors_available():
        msg = (
            "`safetensors` package is required but not installed. "
            "You can install `safetensors` package with the command:\n\n"
            "pip install safetensors\n"
        )
        raise RuntimeError(msg)


def safetensors_available(fn: Callable[..., Any]) -> Callable[..., Any]:
    r"""Implement a decorator to execute a function only if
    ``safetensors`` package is installed.

    Args:
        fn: Specifies the function to execute.

    Returns:
        A wrapper around ``fn`` if ``safetensors`` package is installed,
            otherwise ``None``.

    Example usage:

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


################
#     yaml     #
################


def is_yaml_available() -> bool:
    r"""Indicate if the ``yaml`` package is installed or not.

    Returns:
        ``True`` if ``yaml`` is available otherwise ``False``.

    Example usage:

    ```pycon
    >>> from iden.utils.imports import is_yaml_available
    >>> is_yaml_available()

    ```
    """
    return find_spec("yaml") is not None


def check_yaml() -> None:
    r"""Check if the ``yaml`` package is installed.

    Raises:
        RuntimeError: if the ``yaml`` package is not installed.

    Example usage:

    ```pycon
    >>> from iden.utils.imports import check_yaml
    >>> check_yaml()

    ```
    """
    if not is_yaml_available():
        msg = (
            "`yaml` package is required but not installed. "
            "You can install `yaml` package with the command:\n\n"
            "pip install pyyaml\n"
        )
        raise RuntimeError(msg)


def yaml_available(fn: Callable[..., Any]) -> Callable[..., Any]:
    r"""Implement a decorator to execute a function only if ``yaml``
    package is installed.

    Args:
        fn: Specifies the function to execute.

    Returns:
        A wrapper around ``fn`` if ``yaml`` package is installed,
            otherwise ``None``.

    Example usage:

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
