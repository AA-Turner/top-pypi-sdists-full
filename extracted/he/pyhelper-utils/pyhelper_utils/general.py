from __future__ import annotations

import datetime
import re
from collections.abc import Callable
from functools import wraps
from logging import Logger
from time import sleep
from typing import Any


def tts(ts: Any) -> int:
    """
    Convert time string to seconds.

    Args:
        ts (str): time string to convert, can be and int followed by s/m/h
            if only numbers was sent return int(ts)

    Example:
        >>> tts(ts="1h")
        3600
        >>> tts(ts="3600")
        3600

    Returns:
        int: Time in seconds
    """
    if time_and_unit_match := re.match(r"(?P<time>\d+)(?P<unit>\w)", str(ts)):
        time_and_unit = time_and_unit_match.groupdict()
    else:
        return int(ts)

    _time = int(time_and_unit["time"])
    _unit = time_and_unit["unit"].lower()
    if _unit == "s":
        return _time
    elif _unit == "m":
        return _time * 60
    elif _unit == "h":
        return _time * 60 * 60
    else:
        return int(ts)


def ignore_exceptions(
    retry: int = 0,
    retry_interval: int = 1,
    return_on_error: Any = None,
    logger: Logger | None = None,
    raise_final_exception: bool = False,
) -> Any:
    """
    Decorator to ignore exceptions with support for retry.

    Args:
        retry (int): Number of retry if the underline function throw exception.
        retry_interval (int): Number of seconds to wait between retries.
        return_on_error (Any): Return value if the underline function throw exception.
        logger (Logger): logger to use, if not passed no logs will be displayed.
        raise_final_exception (bool): whether to raise the final exception.


    Returns:
        any: the underline function return value.
    """

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as ex:  # noqa: BLE001
                for idx in range(retry):
                    try:
                        sleep(retry_interval)
                        return func(*args, **kwargs)
                    except Exception:
                        if idx + 1 < retry:
                            continue
                        if raise_final_exception:
                            raise
                if logger:
                    logger.error(f"{func.__name__} error: {ex}")
                return return_on_error

        return inner

    return wrapper


def stt(seconds: int) -> str:
    """
    Convert seconds to human readable time string.

    Args:
        seconds (int): seconds to convert

    Returns:
        str: Human readable time string

    Example:
        >>> stt(seconds=3600)
        '1 hour'
        >>> stt(seconds=3600*24)
        '1 day'
        >>> stt((60*60*14+65))
        '14 hours and 1 minute and 5 seconds'
    """
    time_str = ""
    total_seconds = datetime.timedelta(seconds=seconds)
    days = total_seconds.days
    remaining_seconds = total_seconds.seconds
    hour, remainder = divmod(remaining_seconds, 3600)
    minute, second = divmod(remainder, 60)
    if days:
        time_str += f"{days} {'days' if days > 1 else 'day'}"

    if hour:
        if days:
            time_str += " and "
        time_str += f"{hour} {'hours' if hour > 1 else 'hour'}"

    if minute:
        if hour or days:
            time_str += " and "
        time_str += f"{minute} {'minutes' if minute > 1 else 'minute'}"

    if second:
        if hour or minute:
            time_str += " and "
        time_str += f"{second} {'seconds' if second > 1 else 'second'}"

    return time_str
