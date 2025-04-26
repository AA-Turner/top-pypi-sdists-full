r"""Contain interval utility functions."""

from __future__ import annotations

__all__ = [
    "find_time_unit",
    "interval_to_strftime_format",
    "interval_to_timedelta",
    "time_unit_to_strftime_format",
]

import re
from datetime import timedelta

STRFTIME_FORMAT = {
    "ns": "%Y-%m-%d %H:%M:%S.%f",
    "us": "%Y-%m-%d %H:%M:%S.%f",
    "ms": "%Y-%m-%d %H:%M:%S.%f",
    "s": "%Y-%m-%d %H:%M:%S",
    "m": "%Y-%m-%d %H:%M",
    "h": "%Y-%m-%d %H:%M",
    "d": "%Y-%m-%d",
    "w": "%Y week %W",
    "mo": "%Y-%m",
    "q": "%Y-%m",
    "y": "%Y",
}

TIME_UNIT_TO_INTERVAL_REGEX = {
    "ns": "[0-9]+ns([0-9]|$)",
    "us": "[0-9]+us([0-9]|$)",
    "ms": "[0-9]+ms([0-9]|$)",
    "s": "[0-9]+s([0-9]|$)",
    "m": "[0-9]+m([0-9]|$)",
    "h": "[0-9]+h([0-9]|$)",
    "d": "[0-9]+d([0-9]|$)",
    "w": "[0-9]+w([0-9]|$)",
    "mo": "[0-9]+mo([0-9]|$)",
    "q": "[0-9]+q([0-9]|$)",
    "y": "[0-9]+y([0-9]|$)",
}


def find_time_unit(interval: str) -> str:
    r"""Find the time unit associated to a ``polars`` interval.

    Args:
        interval: The ``polars`` interval to analyze.

    Returns:
        The found time unit.

    Raises:
        RuntimeError: if no valid time unit can be found.

    Example usage:

    ```pycon

    >>> from grizz.utils.interval import find_time_unit
    >>> find_time_unit("3d12h4m")
    m
    >>> find_time_unit("3y5mo")
    mo

    ```
    """
    for unit, regex in TIME_UNIT_TO_INTERVAL_REGEX.items():
        if re.compile(regex).search(interval) is not None:
            return unit

    msg = f"could not find the time unit of {interval}"
    raise RuntimeError(msg)


def interval_to_strftime_format(interval: str) -> str:
    r"""Return the default strftime format for a given interval.

    Args:
        interval: The ``polars`` interval to analyze.

    Returns:
        The default strftime format.

    Example usage:

    ```pycon

    >>> from grizz.utils.interval import interval_to_strftime_format
    >>> interval_to_strftime_format("1h")
    %Y-%m-%d %H:%M
    >>> interval_to_strftime_format("3y1mo")
    %Y-%m

    ```
    """
    return time_unit_to_strftime_format(time_unit=find_time_unit(interval))


def interval_to_timedelta(interval: str) -> timedelta:
    r"""Convert a interval to a timedelta object.

    Args:
        interval: The input interval.

    Returns:
        The timedelta object generated from the interval.

    Example usage:

    ```pycon

    >>> from grizz.utils.interval import interval_to_timedelta
    >>> interval_to_timedelta("5d1h42m")
    datetime.timedelta(days=5, seconds=6120)

    ```
    """

    def extract(regex: str, interval: str) -> float | None:
        res = re.compile(regex).search(interval)
        if res is None:
            return 0.0
        return float(re.compile("[0-9]+").search(res[0])[0])

    days = extract(TIME_UNIT_TO_INTERVAL_REGEX["w"], interval)
    microseconds = extract(TIME_UNIT_TO_INTERVAL_REGEX["ns"], interval) * 0.001
    return timedelta(
        days=extract(TIME_UNIT_TO_INTERVAL_REGEX["d"], interval) + 7 * days,
        hours=extract(TIME_UNIT_TO_INTERVAL_REGEX["h"], interval),
        minutes=extract(TIME_UNIT_TO_INTERVAL_REGEX["m"], interval),
        seconds=extract(TIME_UNIT_TO_INTERVAL_REGEX["s"], interval),
        milliseconds=extract(TIME_UNIT_TO_INTERVAL_REGEX["ms"], interval),
        microseconds=extract(TIME_UNIT_TO_INTERVAL_REGEX["us"], interval) + microseconds,
    )


def time_unit_to_strftime_format(time_unit: str) -> str:
    r"""Return the default strftime format for a given time unit.

    Args:
        time_unit: The time unit.

    Returns:
        The default strftime format.

    Example usage:

    ```pycon

    >>> from grizz.utils.interval import time_unit_to_strftime_format
    >>> time_unit_to_strftime_format("h")
    %Y-%m-%d %H:%M
    >>> time_unit_to_strftime_format("mo")
    %Y-%m

    ```
    """
    template = STRFTIME_FORMAT.get(time_unit.lower(), None)
    if template is None:
        msg = (
            f"Incorrect time unit {time_unit}. The valid time units are: "
            f"{list(STRFTIME_FORMAT.keys())}"
        )
        raise RuntimeError(msg)
    return template
