import logging
import time
from functools import wraps

from beartype.roar import (
    BeartypeCallHintPepParamException,
)

logger = logging.getLogger("picsellia")


def exception_handler(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BeartypeCallHintPepParamException as e:
            raise TypeError(str(e)) from e

    inner: func

    return inner


def retry(exceptions, total_tries=5, initial_wait=0.5, backoff_factor=2):
    """
    calling the decorated function applying an exponential backoff.
    Arguments:
        exceptions: Exception(s) that trigger a retry, can be a tuple
        total_tries: Total tries
        initial_wait: Time to first retry
        backoff_factor: Backoff multiplier (e.g. value of 2 will double the delay each retry).
    """

    def retry_decorator(f):
        @wraps(f)
        def func_with_retries(*args, **kwargs):
            _tries, _delay = total_tries, initial_wait
            while True:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    _tries -= 1
                    if _tries <= 0:
                        raise
                    logger.info(
                        f"Exception caught: {e}. Retrying again in {_delay}s. {_tries} max retry left."
                    )
                    time.sleep(_delay)
                    _delay *= backoff_factor

        return func_with_retries

    return retry_decorator
