from abc import ABC, abstractmethod
from typing import Set

DEFAULT_RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}


class RetryStrategy(ABC):
    """
    Abstract base class for retry strategies.

    All retry strategies must implement two methods:
    - should_retry: Determines if a request should be retried
    - get_delay: Calculates the delay before the next retry attempt

    Attributes:
        max_retries: Maximum number of retry attempts
    """

    max_retries: int

    @abstractmethod
    def should_retry(self, attempt: int, status_code: int) -> bool:
        """
        Determine if a request should be retried.

        Args:
            attempt: Current attempt number (1-based)
            status_code: HTTP status code from the failed request

        Returns:
            True if the request should be retried, False otherwise
        """
        pass

    @abstractmethod
    def get_delay(self, attempt: int) -> float:
        """
        Calculate the delay before the next retry attempt.

        Args:
            attempt: Current attempt number (1-based)

        Returns:
            Delay in seconds before the next retry
        """
        pass


class ExponentialBackoffRetry(RetryStrategy):
    """
    Retry strategy with exponential backoff.

    The delay between retries increases exponentially with each attempt,
    helping to reduce load on the server while still retrying failed requests.

    The delay is calculated as: initial_delay * (backoff_factor ^ (attempt - 1))
    and is capped at max_delay.

    Args:
        max_retries: Maximum number of retry attempts. Defaults to 3.
        initial_delay: Initial delay in seconds before first retry. Defaults to 0.2.
        max_delay: Maximum delay cap in seconds. Defaults to 60.0.
        backoff_factor: Multiplier for exponential growth. Defaults to 2.0.
        retryable_status_codes: Set of HTTP status codes that trigger retries.
            Defaults to {408, 429, 500, 502, 503, 504}.

    Example:
        >>> strategy = ExponentialBackoffRetry(max_retries=3, initial_delay=0.2)
        >>> # Attempt 1: 0.2s, Attempt 2: 0.4s, Attempt 3: 0.8s
    """

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay: float = 0.2,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        retryable_status_codes: Set[int] = None,
    ):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor

        if retryable_status_codes is None:
            retryable_status_codes = DEFAULT_RETRYABLE_STATUS_CODES

        self.retryable_status_codes = retryable_status_codes

    def should_retry(self, attempt: int, status_code: int) -> bool:
        if attempt >= self.max_retries:
            return False

        return status_code in self.retryable_status_codes

    def get_delay(self, attempt: int) -> float:
        delay = self.initial_delay * (self.backoff_factor ** (attempt - 1))
        return min(delay, self.max_delay)


class LinearRetry(RetryStrategy):
    """
    Retry strategy with constant delay between attempts.

    Each retry waits the same fixed delay, providing predictable retry timing.
    This is simpler than exponential backoff and useful when the server can
    handle consistent retry rates.

    Args:
        max_retries: Maximum number of retry attempts. Defaults to 3.
        delay: Fixed delay in seconds between retries. Defaults to 1.0.
        retryable_status_codes: Set of HTTP status codes that trigger retries.
            Defaults to {408, 429, 500, 502, 503, 504}.

    Example:
        >>> strategy = LinearRetry(max_retries=3, delay=1.0)
        >>> # All attempts wait 1.0s between retries
    """

    def __init__(
        self,
        max_retries: int = 3,
        delay: float = 1.0,
        retryable_status_codes: Set[int] = None,
    ):
        self.max_retries = max_retries
        self.delay = delay

        if retryable_status_codes is None:
            retryable_status_codes = DEFAULT_RETRYABLE_STATUS_CODES

        self.retryable_status_codes = retryable_status_codes

    def should_retry(self, attempt: int, status_code: int) -> bool:
        if attempt >= self.max_retries:
            return False

        return status_code in self.retryable_status_codes

    def get_delay(self, attempt: int) -> float:
        return self.delay


class NoRetry(RetryStrategy):
    """
    Retry strategy that disables all retry attempts.

    Use this strategy when you want requests to fail immediately without
    any retry attempts. This is useful for operations where retrying doesn't
    make sense or when you want to handle failures explicitly.

    Attributes:
        max_retries: Always set to 0, no retries will be attempted.

    Example:
        >>> strategy = NoRetry()
        >>> # Request will fail immediately on any error
    """

    max_retries: int = 0

    def should_retry(self, attempt: int, status_code: int) -> bool:
        return False

    def get_delay(self, attempt: int) -> float:
        return 0.0


def create_default_retry_strategy() -> RetryStrategy:
    """
    Create a default retry strategy with sensible defaults.

    Returns an ExponentialBackoffRetry instance configured with:
    - max_retries=3
    - initial_delay=0.2 seconds
    - backoff_factor=2.0

    Returns:
        RetryStrategy: An ExponentialBackoffRetry instance with default settings.
    """
    return ExponentialBackoffRetry(
        max_retries=3,
        initial_delay=0.2,
        backoff_factor=2.0,
    )
