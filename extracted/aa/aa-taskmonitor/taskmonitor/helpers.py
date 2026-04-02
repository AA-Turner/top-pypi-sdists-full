"""Helpers for Task Monitor."""

# pylint: disable = protected-access

import datetime as dt
import functools


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def dict_sort_keys(dct: dict) -> dict:
    """Return a copy of this dictionary with sorted keys."""
    return dict(sorted(dct.items(), key=lambda x: x[0].lower()))


def truncate_list(lst: list) -> list:
    """Truncate nested elements and return as new list.

    Dicts will be replaced by `{}`

    Lists, tuple and sets wil be replaced by `[]`
    """
    return [_replace_nested_element(item) for item in lst]


def truncate_dict(dct: dict) -> dict:
    """Truncate nested values and return as new dict.

    Example:
    `{"a": {"aa": 1, ...}, "b": [1, 2, ...]}`-> `{"a": {}, "b": []}`
    """
    return {key: _replace_nested_element(value) for key, value in dct.items()}


def _replace_nested_element(value):
    if isinstance(value, dict):
        return {}
    if isinstance(value, (list, tuple, set)):
        return []
    return value


def truncate_result(value):
    """Truncate nested items in results and return as new value."""
    if isinstance(value, dict):
        return truncate_dict(value)
    if isinstance(value, (list, tuple, set)):
        return compress_list(truncate_list(value))
    return value


def compress_list(lst: list) -> list:
    """Compress list to empty list of it contains of empty containers only.

    Example: `[ {}, {} ]` -> `[]`
    """
    for item in lst:
        if item is False or item:
            return lst
    return []


def memcached(timeout: int = 30):
    """Cache result of decorated function in memory until timeout.

    Args:
    - timeout: Seconds until cache becomes stale
    """

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                my_cache = wrapper._cache
            except AttributeError:
                my_cache = None
            if (
                not my_cache
                or (dt.datetime.utcnow() - my_cache["timestamp"]).total_seconds()
                > timeout
            ):
                wrapper._cache = my_cache = {
                    "timestamp": dt.datetime.utcnow(),
                    "result": func(*args, **kwargs),
                }
            return my_cache["result"]

        return wrapper

    return actual_decorator
