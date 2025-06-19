import random
import time
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Generator, Optional, Tuple, Type, Union


class Backoff(ABC):
    """
    Backoff is an abstract class that dictates a retry strategy.
    It contains an abstract method `backoff` that returns a calculated delay based on the provided
    attempt.
    """

    def __init__(self, start: float, maximum: float):
        """
        Defines a new backoff retry strategy.

        :param start: the scaling factor for any calculated delays.  Must be >= 0.
        :param maximum: defines a cap on the calculated delays to prevent prohibitively long waits
                        that could time out.
        """
        if start < 0:
            raise ValueError("start must be >= 0")
        self.start = start
        self.maximum = maximum

    @abstractmethod
    def backoff(self, attempt: int) -> float:
        pass

    def delays(self) -> Generator[float, None, None]:
        """
        Generates a duration of time to delay for each successive call based on the configured
        backoff strategy.

        :return: a generator that yields the next delay duration.
        """
        retries = 0
        max_retries = 100  # Safety limit to prevent infinite loops

        while retries < max_retries:
            duration = self.backoff(retries)
            # duration might be 0 when start == 0.
            # In that case, retry once immediately, and then on maximum.
            if duration >= self.maximum or duration <= 0:
                break
            yield duration
            retries += 1

        yield self.maximum


def retry_with_backoff(
    backoff: "Backoff",
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]],
    should_retry: Optional[Callable[[Exception], bool]] = None,
) -> Callable[[Callable], Callable]:
    """
    A decorator to retry a function based on the :param:`backoff` provided
    if any of the provided :param:`exceptions` are raised and the :param:`should_retry`
    condition is met.

    :param backoff: the retry strategy to employ.
    :param exceptions: the exceptions that should trigger the retry. Can be further customized by
                       defining a custom attribute `retryable` on the exception class. The retries
                       are abandoned if retryable returns False.
    :param should_retry: Optional callable to further determine whether to retry on an exception.
                         Takes an exception and returns a boolean. If `None`, all given exceptions
                          are retried.
    :return: The same result the decorated function returns.
    """

    def _retry(func: Callable) -> Callable:
        @wraps(func)
        def _impl(*args: Any, **kwargs: Any) -> Any:
            delays = backoff.delays()
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as exception:
                    # If the exception is marked as NOT retryable, stop now.
                    retryable = getattr(exception, "retryable", True)
                    if not retryable:
                        raise exception
                    # If a custom should_retry function is provided, call it to determine
                    # if we should retry or not. Otherwise, default to the retryable value.
                    current_should_retry = should_retry or (lambda _: retryable)
                    if not current_should_retry(exception):
                        raise exception
                    try:
                        delay = next(delays)
                    except StopIteration:
                        raise exception
                    time.sleep(delay)

        return _impl

    return _retry


class ExponentialBackoff(Backoff):
    """
    A backoff strategy with an exponentially increasing delay in between attempts.
    """

    def exponential(self, attempt: int) -> float:
        # Prevent overflow by using float arithmetic and limiting attempt size
        if attempt > 1000:  # Safety limit to prevent overflow
            return self.maximum
        return min(self.maximum, pow(2.0, float(attempt)) * self.start)

    def backoff(self, attempt: int) -> float:
        return self.exponential(attempt)


class ExponentialBackoffJitter(ExponentialBackoff):
    """
    An exponential backoff strategy with an added jitter that randomly spreads out the delays
    uniformly while ensuring monotonically increasing delays.
    """

    def backoff(self, attempt: int) -> float:
        base_delay = self.exponential(max(0, attempt - 1))
        added_delay = self.exponential(max(0, attempt)) - base_delay
        # Add jitter between 50% and 100% of the base delay to ensure monotonically increasing
        # delays while still providing randomization
        jitter_factor = random.uniform(0.5, 1.0)
        return base_delay + (added_delay * jitter_factor)
