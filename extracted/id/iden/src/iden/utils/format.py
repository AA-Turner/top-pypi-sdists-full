r"""Contain utility functions to compute formatted strings."""

from __future__ import annotations

__all__ = ["human_time"]

import datetime


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
