"""Retry utilities for provider resilience.

Provides:
- Exponential backoff with jitter
- Rate limit awareness
- Circuit breaker pattern
- Transient error detection
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, TypeVar

import httpx

T = TypeVar("T")


# HTTP status codes that indicate transient errors (worth retrying)
TRANSIENT_STATUS_CODES = {
    408,  # Request Timeout
    429,  # Too Many Requests (rate limited)
    500,  # Internal Server Error
    502,  # Bad Gateway
    503,  # Service Unavailable
    504,  # Gateway Timeout
}

# Status codes that indicate permanent failures (don't retry)
PERMANENT_STATUS_CODES = {
    400,  # Bad Request
    401,  # Unauthorized
    403,  # Forbidden
    404,  # Not Found
    422,  # Unprocessable Entity
}


def is_transient_error(exc: Exception) -> bool:
    """Check if an exception represents a transient/retryable error."""
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in TRANSIENT_STATUS_CODES
    if isinstance(exc, (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.ConnectError)):
        return True
    if isinstance(exc, httpx.RemoteProtocolError):
        return True
    if isinstance(exc, ConnectionError):
        return True
    return False


def is_rate_limited(exc: Exception) -> bool:
    """Check if the error is specifically a rate limit."""
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code == 429
    return False


def get_retry_after(exc: Exception) -> float | None:
    """Extract Retry-After header value if present."""
    if isinstance(exc, httpx.HTTPStatusError):
        retry_after = exc.response.headers.get("Retry-After")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass
    return None


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""

    max_attempts: int = 3
    base_delay: float = 0.5  # Initial delay in seconds
    max_delay: float = 30.0  # Maximum delay between retries
    exponential_base: float = 2.0  # Multiplier for exponential backoff
    jitter: float = 0.1  # Random jitter factor (0.1 = ±10%)

    def calculate_delay(self, attempt: int, retry_after: float | None = None) -> float:
        """Calculate delay before next retry with exponential backoff and jitter."""
        if retry_after is not None:
            # Respect server's Retry-After header
            return min(retry_after, self.max_delay)

        # Exponential backoff: base_delay * (exponential_base ^ attempt)
        delay = self.base_delay * (self.exponential_base**attempt)
        delay = min(delay, self.max_delay)

        # Add jitter to prevent thundering herd
        jitter_range = delay * self.jitter
        delay += random.uniform(-jitter_range, jitter_range)

        return max(0, delay)


@dataclass
class CircuitBreaker:
    """Simple circuit breaker to prevent hammering failing services."""

    failure_threshold: int = 5  # Failures before opening circuit
    recovery_timeout: float = 60.0  # Seconds before trying again

    _failures: int = field(default=0, init=False)
    _last_failure_time: float = field(default=0.0, init=False)
    _state: str = field(default="closed", init=False)  # closed, open, half-open

    def record_success(self) -> None:
        """Record a successful call."""
        self._failures = 0
        self._state = "closed"

    def record_failure(self) -> None:
        """Record a failed call."""
        self._failures += 1
        self._last_failure_time = time.monotonic()
        if self._failures >= self.failure_threshold:
            self._state = "open"

    def can_proceed(self) -> bool:
        """Check if we should attempt a call."""
        if self._state == "closed":
            return True
        if self._state == "open":
            # Check if recovery timeout has passed
            elapsed = time.monotonic() - self._last_failure_time
            if elapsed >= self.recovery_timeout:
                self._state = "half-open"
                return True
            return False
        # half-open: allow one attempt
        return True

    def is_open(self) -> bool:
        """Check if circuit is open (blocking calls)."""
        return self._state == "open" and not self.can_proceed()


# Default configurations
DEFAULT_RETRY_CONFIG = RetryConfig()
AGGRESSIVE_RETRY_CONFIG = RetryConfig(max_attempts=5, base_delay=1.0)
FAST_FAIL_CONFIG = RetryConfig(max_attempts=2, base_delay=0.2, max_delay=2.0)


def with_retry(
    config: RetryConfig = DEFAULT_RETRY_CONFIG,
    circuit_breaker: CircuitBreaker | None = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator that adds retry logic with exponential backoff.

    Usage:
        @with_retry()
        def make_api_call():
            ...

        @with_retry(config=AGGRESSIVE_RETRY_CONFIG)
        def important_call():
            ...
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            if circuit_breaker and circuit_breaker.is_open():
                raise RuntimeError(
                    f"Circuit breaker open for {func.__name__}. Service may be unavailable."
                )

            last_exception: Exception | None = None

            for attempt in range(config.max_attempts):
                try:
                    result = func(*args, **kwargs)
                    if circuit_breaker:
                        circuit_breaker.record_success()
                    return result
                except KeyboardInterrupt:
                    raise
                except Exception as exc:
                    last_exception = exc

                    if not is_transient_error(exc):
                        # Permanent error, don't retry
                        raise

                    if circuit_breaker:
                        circuit_breaker.record_failure()

                    if attempt < config.max_attempts - 1:
                        retry_after = get_retry_after(exc)
                        delay = config.calculate_delay(attempt, retry_after)
                        time.sleep(delay)

            # All retries exhausted
            if last_exception:
                raise last_exception
            raise RuntimeError("Retry failed without exception")

        return wrapper

    return decorator


def retry_generator(
    gen_func: Callable[..., Iterator[T]],
    config: RetryConfig = DEFAULT_RETRY_CONFIG,
) -> Callable[..., Iterator[T]]:
    """Wrap a generator function with retry logic.

    Retries the entire generator if it fails during iteration.
    Note: This restarts from the beginning on failure.

    Usage:
        @retry_generator
        def stream_tokens():
            for token in api.stream():
                yield token
    """

    @wraps(gen_func)
    def wrapper(*args: Any, **kwargs: Any) -> Iterator[T]:
        last_exception: Exception | None = None

        for attempt in range(config.max_attempts):
            try:
                yield from gen_func(*args, **kwargs)
                return
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                last_exception = exc

                if not is_transient_error(exc):
                    raise

                if attempt < config.max_attempts - 1:
                    retry_after = get_retry_after(exc)
                    delay = config.calculate_delay(attempt, retry_after)
                    time.sleep(delay)

        if last_exception:
            raise last_exception

    return wrapper


class RateLimiter:
    """Simple token bucket rate limiter."""

    def __init__(
        self,
        requests_per_minute: int = 60,
        burst_size: int | None = None,
    ):
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size or requests_per_minute
        self._tokens = float(self.burst_size)
        self._last_update = time.monotonic()
        self._refill_rate = requests_per_minute / 60.0  # tokens per second

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self._last_update
        self._tokens = min(self.burst_size, self._tokens + elapsed * self._refill_rate)
        self._last_update = now

    def acquire(self, timeout: float = 30.0) -> bool:
        """Acquire a token, blocking if necessary.

        Returns True if token acquired, False if timeout exceeded.
        """
        deadline = time.monotonic() + timeout

        while True:
            self._refill()

            if self._tokens >= 1.0:
                self._tokens -= 1.0
                return True

            # Calculate wait time for next token
            wait_time = (1.0 - self._tokens) / self._refill_rate

            if time.monotonic() + wait_time > deadline:
                return False

            time.sleep(min(wait_time, 0.1))  # Sleep in small increments

    def try_acquire(self) -> bool:
        """Try to acquire a token without blocking."""
        self._refill()
        if self._tokens >= 1.0:
            self._tokens -= 1.0
            return True
        return False


# Provider-specific rate limiters (can be shared across instances)
_rate_limiters: dict[str, RateLimiter] = {}


def get_rate_limiter(provider: str, requests_per_minute: int = 60) -> RateLimiter:
    """Get or create a rate limiter for a provider."""
    if provider not in _rate_limiters:
        _rate_limiters[provider] = RateLimiter(requests_per_minute)
    return _rate_limiters[provider]
