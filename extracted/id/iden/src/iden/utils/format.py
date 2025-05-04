r"""Contain utility functions to compute formatted strings."""

from __future__ import annotations

__all__ = ["human_time", "str_kwargs"]

import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping


def human_time(seconds: float) -> str:
    r"""Return a number of seconds in an easier format to read
    ``hh:mm:ss``.

    If the number of seconds is bigger than 1 day, this representation
    also encodes the number of days.

    Args:
        seconds: The number of seconds.

    Returns:
        The number of seconds in a string format (``hh:mm:ss``).

    Example usage:

    ```pycon

    >>> from iden.utils.format import human_time
    >>> human_time(1.2)
    '0:00:01.200000'
    >>> human_time(61.2)
    '0:01:01.200000'
    >>> human_time(3661.2)
    '1:01:01.200000'

    ```
    """
    return str(datetime.timedelta(seconds=seconds))


def str_kwargs(mapping: Mapping) -> str:
    r"""Return a string of the input mapping.

    This function is designed to be used in ``__repr__`` and
    ``__str__`` methods.

    Args:
        mapping: The mapping.

    Returns:
        The generated string.

    Example usage:

    ```pycon

    >>> from iden.utils.format import str_kwargs
    >>> str_kwargs({"key1": 1})
    ', key1=1'
    >>> str_kwargs({"key1": 1, "key2": 2})
    ', key1=1, key2=2'

    ```
    """
    args = ", ".join([f"{key}={value}" for key, value in mapping.items()])
    if args:
        args = ", " + args
    return args
