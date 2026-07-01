import asyncio
import functools
import logging
import random
import time
from typing import Awaitable, Callable, Tuple, Type, TypeVar, Union


logger = logging.getLogger(__name__)

E = TypeVar("E", bound=BaseException)


def retry(
    expected_exception: Union[Type[E], Tuple[Type[E], ...]] = BaseException,
    *,
    attempts: int = 2,
    backoff: Union[int, float] = 0,
    exponential_backoff: bool = False,
    ignore_exceptions: bool = False,
    jitter: Union[int, float] = 0,
    maximum_backoff: Union[int, float] = 0,
    on_exception: Union[Awaitable, Callable, None] = None,
):
    """Retry decorator for synchronous and asynchronous functions.

    Arguments:
        expected_exception:
            exception or tuple of exceptions (default BaseException).
    
    Keyword arguments:
        attempts:
            how much times the function will be retried, value -1 is infinite (default 2).
        backoff:
            time interval between the attemps (default 0).
        exponential_backoff:
            current_backoff = backoff * 2 ** retries (default False).
        ignore_exceptions:
            only log error but not raise exception if attempts exceeds (default False).
        jitter:
            maximum value of deviation from the current_backoff (default 0).
        maximum_backoff:
            current_backoff = min(current_backoff, maximum_backoff) (default 0).
        on_exception:
            function that called or await on error occurs (default None).
            Be aware if a decorating function is synchronous on_exception function must be 
            synchronous too and accordingly for asynchronous function on_exception must be
            asynchronous.
    """

    if exponential_backoff:
        assert backoff > 0, "with exponential_backoff backoff must be greater than 0."
        if maximum_backoff:
            assert maximum_backoff > backoff, "maximum_backoff must be greater than backoff."
    else:
        assert backoff >= 0, "backoff must be greater than or equal 0."
        assert not maximum_backoff, \
            "maximum_backoff do not makes sense without exponential_backoff."

    assert jitter <= backoff, "jitter must be less than or equal backoff."
    
    def decorator(function):

        def handle_error(exception: Exception, count: int) -> Tuple[int, float]:
            logger.warning(f"Retry decorator catch error in {function.__name__}: {repr(exception)}")

            count += 1
            if attempts == -1 or count >= attempts:
                if ignore_exceptions:
                    current_backoff = 0
                    return count, current_backoff
                raise exception

            current_backoff = backoff
            if exponential_backoff:
                current_backoff = backoff * 2 ** (count - 1)
            if jitter:
                deviation = jitter * random.random() * random.choice((-1, 1))
                current_backoff = current_backoff + deviation
            if maximum_backoff:
                current_backoff = min(current_backoff, maximum_backoff)

            return count, current_backoff

        def attemps_exceeds():
            logger.error(f"Retry decorator exceeds attemps in {function.__name__}")

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            count = 0
            while attempts == -1 or count < attempts:
                try:
                    return function(*args, **kwargs)
                except expected_exception as e:
                    count, current_backoff = handle_error(e, count)
                    if on_exception:
                        on_exception()
                    time.sleep(current_backoff)
            attemps_exceeds()

        @functools.wraps(function)
        async def async_wrapper(*args, **kwargs):
            count = 0
            while attempts == -1 or count < attempts:
                try:
                    return await function(*args, **kwargs)
                except expected_exception as e:
                    count, current_backoff = handle_error(e, count)
                    if on_exception:
                        await on_exception()
                    await asyncio.sleep(current_backoff)
            attemps_exceeds()

        if asyncio.iscoroutinefunction(function):
            if on_exception:
                assert asyncio.iscoroutinefunction(on_exception), \
                    "on_exception must be async as decorating function"
            return async_wrapper
        else:
            if on_exception:
                assert not asyncio.iscoroutinefunction(on_exception), \
                    "on_exception must be sync as decorating function"
                assert callable(function), "on_exception must be callable"
            return wrapper

    return decorator
