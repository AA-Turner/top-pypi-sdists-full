"""
Rate limiting utilities for connector SDK.

This module provides classes and functions to handle rate limiting when making
requests to third-party APIs. It supports batching requests, respecting rate limits,
and handling rate limit headers.
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, TypeVar

import httpx

RequestType = TypeVar("RequestType")  # Input request type
ResponseType = TypeVar("ResponseType")  # Response type

logger = logging.getLogger(__name__)

REQUESTS_PER_WINDOW_CEILING = 0.2
LIMIT_CEILING = 0.2
MAXIMUM_RETRIES = 5

STATIC_RATE_LIMIT_DICTIONARY = [
    "rate limit exceeded",
    "too many requests",
    "quota exceeded",
    "exceeded your rate limit",
    "request limit reached",
]


class RateLimitStrategy(Enum):
    """
    Strategy setting for handling rate limits.

    FIXED - Fixed rate limiting based on predefined limits
    ADAPTIVE - Adaptive rate limiting based on response headers/etc.
    """

    FIXED = "fixed"
    ADAPTIVE = "adaptive"


@dataclass
class RateLimitExtractorResponse:
    """Response from a rate limit extractor."""

    # Remaining requests in the current time window
    remaining: int

    # Total requests allowed in the current time window
    limit: int

    # Reset time in seconds (from the API if available)
    reset: int | None = None

    # Time window in seconds config (from the API if available)
    window_seconds: int | None = None

    # Observed requests (from the API if available)
    observed: str | None = None

    # Requests per window directly config (from the API if available)
    requests_per_window: int | None = None


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""

    # App ID
    app_id: str

    # Maximum number of requests per time window
    requests_per_window: int

    # Time window in seconds
    window_seconds: int

    # Maximum retries
    maximum_retries: int = MAXIMUM_RETRIES

    # Strategy for rate limiting
    strategy: RateLimitStrategy = RateLimitStrategy.FIXED

    # Maximum batch size for requests
    max_batch_size: int | None = None

    # Function to extract rate limit info from response
    rate_limit_extractor: Callable[[Any], RateLimitExtractorResponse] | None = None

    # Initial delay between batches in seconds
    initial_delay: float = 0.0

    # Maximum delay between batches in seconds
    max_delay: float = 60.0

    # Backoff factor for exponential backoff
    backoff_factor: float = 1.5

    @classmethod
    def default(cls, app_id: str) -> "RateLimitConfig":
        """Get the default rate limit config."""
        return cls(
            app_id=app_id,
            requests_per_window=30,
            window_seconds=60,
            strategy=RateLimitStrategy.FIXED,
            max_batch_size=15,
        )

    def overwrite(self, **kwargs: Any) -> None:
        """Overwrite the default values with the provided kwargs."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class RateLimitExtractor(ABC):
    """Abstract base class for extracting rate limit information from response."""

    @abstractmethod
    def extract(self, response: Any) -> RateLimitExtractorResponse:
        pass


class RateLimiter(Generic[RequestType, ResponseType]):
    """
    Rate limiter for API requests.

    This class helps manage the rate of requests to third-party APIs by batching
    requests, respecting rate limits, and handling rate limit headers.
    """

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.request_times: list[float] = []
        self.current_delay = config.initial_delay

        # Set default max_batch_size if not provided
        if self.config.max_batch_size is None:
            self.config.max_batch_size = self.config.requests_per_window

    def _update_request_times(self) -> None:
        """Update the list of request times, removing expired ones."""
        current_time = time.time()
        self.request_times = [
            t for t in self.request_times if current_time - t < self.config.window_seconds
        ]

    def _can_make_request(self) -> bool:
        """Check if a request can be made without exceeding the rate limit."""
        self._update_request_times()
        return len(self.request_times) < self.config.requests_per_window

    def _wait_time_needed(self) -> float:
        """Calculate the time to wait before making the next request."""
        if self._can_make_request():
            return 0.0

        self._update_request_times()
        if not self.request_times:
            return 0.0

        oldest_request = min(self.request_times)
        return oldest_request + self.config.window_seconds - time.time()

    def _update_rate_limits(self, response: Any) -> None:
        """
        Update rate limits based on response.
        """
        if (
            self.config.strategy == RateLimitStrategy.ADAPTIVE
            and self.config.rate_limit_extractor is not None
        ):
            rate_limit_info = self.config.rate_limit_extractor(response)

            # Update the configuration based on the rate limit information
            if rate_limit_info.requests_per_window is not None:
                self.config.requests_per_window = rate_limit_info.requests_per_window

            if rate_limit_info.window_seconds is not None:
                self.config.window_seconds = rate_limit_info.window_seconds

            # If reset time is available, check it
            if rate_limit_info.reset is not None:
                current_time = time.time()
                time_until_reset = rate_limit_info.reset - current_time

                # If reset is within the max delay, adjust the delay
                if (
                    time_until_reset > 0
                    and time_until_reset < self.config.max_delay
                    and rate_limit_info.remaining < rate_limit_info.limit * LIMIT_CEILING
                ):
                    self.current_delay = time_until_reset
                    return

            # If we're approaching the limit, increase the delay
            if (
                rate_limit_info.remaining
                < self.config.requests_per_window * REQUESTS_PER_WINDOW_CEILING
            ):
                self.current_delay = min(
                    self.current_delay * self.config.backoff_factor, self.config.max_delay
                )
            else:
                # If we're not close to the limit, reduce the delay
                self.current_delay = max(
                    self.current_delay / self.config.backoff_factor, self.config.initial_delay
                )

            self.debug_log(
                f"Updated rate limits: {self.config.requests_per_window} requests per {self.config.window_seconds} seconds, current delay: {self.current_delay}"
            )

    def _handle_rate_limit_exceeded(self) -> None:
        """Handle the case when rate limit is exceeded."""
        if self.config.strategy == RateLimitStrategy.FIXED:
            # If on FIXED strategy, we set the current delay to the configured window seconds
            # Since we cannot adapt to the API's rate limits and this is a static way to handle it
            self.debug_log(
                f"Rate limit exceeded; setting delay to {self.config.window_seconds} seconds"
            )
            self.current_delay = self.config.window_seconds

        self.current_delay = min(
            self.current_delay * self.config.backoff_factor, self.config.max_delay
        )

    def debug_log(self, message: str):
        """Log the current rate limit status."""
        print(f"[RateLimiter/{self.config.app_id}] {message}")

    async def execute_requests(
        self,
        requests: list[RequestType],
        request_handler: Callable[[RequestType], ResponseType | asyncio.Future[ResponseType]],
    ) -> list[ResponseType]:
        """
        Execute requests with rate limiting.
        """
        responses: list[ResponseType] = []

        # Handle empty requests list
        if not requests:
            return responses

        # Calc batch size
        batch_size = max(
            1,
            min(
                self.config.max_batch_size or self.config.requests_per_window,
                self.config.requests_per_window,
            ),
        )

        # Process requests in batches
        self.debug_log(f"Executing {len(requests)} requests in {batch_size} batches")

        for i in range(0, len(requests), batch_size):
            batch = requests[i : i + batch_size]
            batch_responses = []

            for request in batch:
                retry_count = 0

                while retry_count <= self.config.maximum_retries:
                    wait_time = self._wait_time_needed()
                    if wait_time > 0:
                        self.debug_log(f"Waiting {wait_time} seconds before making request")
                        await asyncio.sleep(wait_time)

                    try:
                        result = request_handler(request)

                        # Handle both synchronous and asynchronous results
                        if asyncio.iscoroutine(result) or isinstance(result, asyncio.Future):
                            response = await result
                        else:
                            response = result

                        # Record the time
                        self.request_times.append(time.time())

                        # Update rate limits
                        self._update_rate_limits(response)

                        # Add response to batch responses
                        batch_responses.append(response)
                        self.debug_log(
                            f"Request {len(responses) + len(batch_responses)} of {len(requests)} completed"
                        )
                        break  # Success, exit retry loop

                    except Exception as e:
                        # Handle rate limit errors
                        error_str = str(e).lower()
                        if any(
                            keyword in error_str for keyword in STATIC_RATE_LIMIT_DICTIONARY
                        ) or (
                            isinstance(e, httpx.HTTPStatusError)
                            and e.response.status_code == httpx.codes.TOO_MANY_REQUESTS
                        ):
                            self._handle_rate_limit_exceeded()
                            self.debug_log(
                                f"Rate limit exceeded; current delay: {self.current_delay}"
                            )

                            retry_count += 1
                            if retry_count > self.config.maximum_retries:
                                raise Exception(
                                    f"Maximum retries ({self.config.maximum_retries}) reached"
                                ) from e

                            # Retry the request after a delay
                            await asyncio.sleep(self.current_delay)
                        else:
                            # Re-raise other exceptions
                            raise

            responses.extend(batch_responses)

            # Wait between batches
            if i + batch_size < len(requests) and self.current_delay > 0:
                await asyncio.sleep(self.current_delay)

        return responses
