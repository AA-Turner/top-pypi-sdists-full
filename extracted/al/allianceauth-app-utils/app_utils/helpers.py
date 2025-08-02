"""General purpose helpers."""

import hashlib
import os
import random
import string
from typing import Any, Callable, Optional

from django.core.cache import cache


def chunks(lst, size):
    """Yield successive sized chunks from lst."""
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def default_if_none(value, default):
    """Return default if value is None."""
    if value is None:
        return default
    return value


# old: get_swagger_spec_path
def swagger_spec_path() -> str:
    """returns the path to the current esi swagger spec file"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "swagger.json")


def random_string(char_count: int) -> str:
    """returns a random string of given length"""
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(char_count)
    )


class AttrDict(dict):
    """Enhanced dict that allows property access to its keys.

    Example:

    .. code-block:: python

        >> my_dict = AttrDict({"color": "red", "size": "medium"})
        >> my_dict["color"]
        "red"
        >> my_dict.color
        "red"

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


def humanize_number(value, magnitude: Optional[str] = None, precision: int = 1) -> str:
    """Return the value in humanized format, e.g. `1234` becomes `1.2k`

    Args:
        magnitude: fix the magnitude to format the number, e.g. `"b"`
        precision: number of digits to round for
    """
    value = float(value)
    power_map = {"t": 12, "b": 9, "m": 6, "k": 3, "": 0}
    if magnitude not in power_map:
        if value >= 10**12:
            magnitude = "t"
        elif value >= 10**9:
            magnitude = "b"
        elif value >= 10**6:
            magnitude = "m"
        elif value >= 10**3:
            magnitude = "k"
        else:
            magnitude = ""
    return f"{value / 10 ** power_map[magnitude]:,.{precision}f}{magnitude}"


def throttle(func: Callable, context_id: str, timeout: Optional[int]) -> Any:
    """Call a function, but limit repeated calls with a timeout, e.g. once per day.

    When a repeated call falls within the timeout the call will simply be ignored.

    Args:
        func: the function to be called
        context_id: a string representing the context for applying the throttle,\
            e.g. a combination of feature name and user ID
        timeout: timeout in seconds between each repeated call of the function

    Returns:
        Return cached value of called function func

    """
    hashed_id = hashlib.md5(str(context_id).encode("utf-8")).hexdigest()
    key = f"APP_UTILS_THROTTLED_{hashed_id}"
    return cache.get_or_set(key, func, timeout)
