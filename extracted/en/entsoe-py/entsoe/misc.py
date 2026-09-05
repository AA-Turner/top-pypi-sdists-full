import pandas as pd
from dateutil import rrule
from itertools import tee


def year_blocks(start, end):
    """
    Create pairs of start and end with max a year in between, to deal with usage restrictions on the API

    Parameters
    ----------
    start : dt.datetime | pd.Timestamp
    end : dt.datetime | pd.Timestamp

    Returns
    -------
    ((pd.Timestamp, pd.Timestamp))
    """
    rule = rrule.YEARLY

    res = []
    for day in rrule.rrule(rule, dtstart=start, until=end):
        res.append(pd.Timestamp(day))
    res.append(end)
    res = sorted(set(res))
    res = pairwise(res)
    return res


def month_blocks(start, end):
    """
    Generates UTC time blocks where each block is exactly <= 1 ISO calendar month
    (P1M) relative to its start time, eliminating unnecessary short slices.

    """
    start_ts = pd.to_datetime(start, utc=True)
    end_ts = pd.to_datetime(end, utc=True)

    if start_ts >= end_ts:
        return []

    blocks = []
    current_start = start_ts

    while current_start < end_ts:
        # Step forward by exactly 1 calendar month (handles leap years/varying month lengths safely)
        next_end = min(current_start + pd.DateOffset(months=1), end_ts)
        blocks.append((current_start, next_end))
        current_start = next_end

    return blocks

def day_blocks(start, end):
    """
    Create pairs of start and end with max a day in between, to deal with usage restrictions on the API

    Parameters
    ----------
    start : dt.datetime | pd.Timestamp
    end : dt.datetime | pd.Timestamp

    Returns
    -------
    ((pd.Timestamp, pd.Timestamp))
    """
    rule = rrule.DAILY

    res = []
    for day in rrule.rrule(rule, dtstart=start, until=end):
        res.append(pd.Timestamp(day))
    res.append(end)
    res = sorted(set(res))
    res = pairwise(res)
    return res


def pairwise(iterable):
    """
    Create pairs to iterate over
    eg. [A, B, C, D] -> ([A, B], [B, C], [C, D])

    Parameters
    ----------
    iterable : iterable

    Returns
    -------
    iterable
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
