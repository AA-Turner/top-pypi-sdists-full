r"""Implement some utility functions to manage optional dependencies."""

from __future__ import annotations

__all__ = [
    "check_cloudpickle",
    "check_joblib",
    "check_safetensors",
    "check_yaml",
    "cloudpickle_available",
    "is_cloudpickle_available",
    "is_joblib_available",
    "is_safetensors_available",
    "is_yaml_available",
    "joblib_available",
    "raise_error_cloudpickle_missing",
    "raise_error_joblib_missing",
    "raise_error_safetensors_missing",
    "raise_error_yaml_missing",
    "safetensors_available",
    "yaml_available",
]

from importlib.util import find_spec
from typing import TYPE_CHECKING, Any, NoReturn

from coola.utils.imports import decorator_package_available

if TYPE_CHECKING:
    from collections.abc import Callable


#######################
#     cloudpickle     #
#######################


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


##################
#     joblib     #
##################


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


#######################
#     safetensors     #
#######################


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


################
#     yaml     #
################


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
