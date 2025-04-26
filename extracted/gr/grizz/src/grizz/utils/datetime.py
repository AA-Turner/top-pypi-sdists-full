r"""Contain utility functions for datetime and date objects."""

from __future__ import annotations

__all__ = ["find_end_datetime", "to_datetime"]


from datetime import date, datetime, timedelta, timezone

from grizz.utils.interval import interval_to_timedelta


def find_end_datetime(start: datetime | date, interval: str | timedelta, periods: int) -> datetime:
    r"""Find the upper bound of the datetime range from the lower bound
    of the datetime range, the interval, and the number of periods.

    Args:
        start: The lower bound of the datetime range.
        interval: The interval of the range periods, specified as a
            Python timedelta object or using the Polars duration
            string language.
        periods: The number of periods after the start.

    Returns:
        The upper bound of the datetime range.

    Notes:
        ``interval`` is created according to the following string
            language:

            - 1ns (1 nanosecond)
            - 1us (1 microsecond)
            - 1ms (1 millisecond)
            - 1s (1 second)
            - 1m (1 minute)
            - 1h (1 hour)
            - 1d (1 calendar day)
            - 1w (1 calendar week)

    Example usage:

    ```pycon

    >>> from datetime import timedelta, datetime, timezone
    >>> from grizz.utils.datetime import find_end_datetime
    >>> find_end_datetime(
    ...     start=datetime(year=2020, month=5, day=12, hour=4, tzinfo=timezone.utc),
    ...     interval=timedelta(hours=1),
    ...     periods=42,
    ... )
    datetime.datetime(2020, 5, 13, 22, 0, tzinfo=datetime.timezone.utc)

    ```
    """
    start = to_datetime(start)
    if isinstance(interval, str):
        interval = interval_to_timedelta(interval)
    return start + interval * periods


def to_datetime(dt: datetime | date) -> datetime:
    r"""Convert a ``date`` object to a ``datetime`` object.

    Args:
        dt: The ``date`` object to convert.

    Returns:
        The ``datetime`` object.

    Example usage:

    ```pycon

    >>> from datetime import datetime, date, timezone
    >>> from grizz.utils.datetime import to_datetime
    >>> to_datetime(datetime(year=2020, month=5, day=12, hour=4, tzinfo=timezone.utc))
    datetime.datetime(2020, 5, 12, 4, 0, tzinfo=datetime.timezone.utc)
    >>> to_datetime(date(year=2020, month=5, day=12))
    datetime.datetime(2020, 5, 12, 0, 0, tzinfo=datetime.timezone.utc)

    ```
    """
    if isinstance(dt, datetime):
        return dt
    return datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc)
