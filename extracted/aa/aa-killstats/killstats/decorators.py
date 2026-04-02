"""
Decorators
"""

# Standard Library
import time

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger

# AA Killstats
from killstats import __title__
from killstats.providers import AppLogger

logger = AppLogger(get_extension_logger(__name__), __title__)


def log_timing(logs):
    """
    A decorator that measures the execution time of a function and logs it.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 3)
            logs.debug(
                "TIME: %s run for %s seconds with args: %s",
                func.__name__,
                elapsed_time,
                args,
            )
            return result

        return wrapper

    return decorator
