from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum
from typing import Any

import httpx
from pydantic import BaseModel

from connector_sdk_types.generated.models.rate_limit_mode import RateLimitMode

__all__ = [
    "RateLimitPolicySource",
    "RateLimitStrategy",
    "RateLimitExtractorResponse",
    "RateLimitExtractor",
    "RateLimitConfig",
    "RateLimitConfigBase",
    "REQUESTS_PER_WINDOW_CEILING",
    "LIMIT_CEILING",
    "MAXIMUM_RETRIES",
    "STATIC_RATE_LIMIT_DICTIONARY",
]

REQUESTS_PER_WINDOW_CEILING = 0.2
LIMIT_CEILING = 0.2
MAXIMUM_RETRIES = 5
FIXED_DECAY_FLOOR = 0.1  # Delays below this (seconds) are snapped to initial_delay for FIXED decay


STATIC_RATE_LIMIT_DICTIONARY = [
    "rate limit exceeded",
    "too many requests",
    "quota exceeded",
    "exceeded your rate limit",
    "request limit reached",
]


class RateLimitPolicySource(str, Enum):
    """ """

    CALLER = "caller"
    CAPABILITY = "capability"
    CONNECTOR = "connector"
    SDK = "sdk"


class RateLimitStrategy(str, Enum):
    """
    Strategy setting for handling rate limits.

    FIXED - Fixed rate limiting based on predefined limits
    ADAPTIVE - Adaptive rate limiting based on response headers/etc.
    """

    FIXED = "fixed"
    ADAPTIVE = "adaptive"


class RateLimitExtractorResponse(BaseModel):
    """Response from a rate limit extractor (3rd Party API information)."""

    remaining: int
    """
    The remaining requests in the current time window.
    """
    limit: int
    """
    The total requests allowed in the current time window.
    """
    reset: int | None = None
    """
    The reset time in seconds (from the API if available).
    """
    window_seconds: int | None = None
    """
    The time window in seconds config (from the API if available).
    """
    observed: str | None = None
    """
    The observed requests (from the API if available).
    """
    requests_per_window: int | None = None
    """
    The requests per window directly configured (from the API if available).
    """


class RateLimitExtractor(ABC):
    """Abstract base class for extracting rate limit information from response."""

    @abstractmethod
    def extract(self, response: Any) -> RateLimitExtractorResponse:
        """Extract rate limit information from response."""
        raise NotImplementedError


class RateLimitConfigBase(BaseModel):
    """Base configuration for rate limiting."""

    requests_per_window: int
    """
    The maximum number of requests per time window.
    """
    window_seconds: int
    """
    The time window in seconds for the rate limit.
    """
    maximum_retries: int = MAXIMUM_RETRIES
    """
    The maximum number of retries for the rate limit.
    """
    strategy: RateLimitStrategy = RateLimitStrategy.FIXED
    """
    The strategy for rate limiting.
    """
    max_batch_size: int | None = None
    """
    The maximum batch size for requests.
    """
    initial_delay: float = 0.0
    """
    The initial delay between batches in seconds.
    """
    max_delay: float = 60.0
    """
    The maximum delay between batches in seconds.
    """
    backoff_factor: float = 1.5
    """
    Exponential backoff factor for the delay between batches.
    """
    max_concurrent: int = 1
    """
    The maximum number of concurrent requests.
    """
    mode: RateLimitMode | None = None
    """
    The rate limit mode determines the behavior of the rate limiter.
    None = SDK auto-selects (write → RETRY_ONLY, read → ENFORCE)
    """


class RateLimitConfig(RateLimitConfigBase):
    """Configuration for rate limiting."""

    config_id: str
    """
    The config_id is used to identify the rate limit tier in the rate limit state.
    It is typically the connector name (e.g. "github") or a descriptive suffix (e.g. "github-rest", "github-graphql").
    """

    rate_limit_extractor: Callable[[httpx.Response], RateLimitExtractorResponse] | None = None
    """
    A function to extract rate limit information from the response.
    """

    rate_limit_error_check: Callable[[Exception], bool] | None = None
    """
    A function to check if an error is a rate limit error.
    If truthy, the error is retried up to `maximum_retries` times.
    """

    transient_error_check: Callable[[Exception], bool] | None = None
    """
    A function to check if an error is a transient error.
    If truthy, the error is retried up to `maximum_retries` times.
    """

    @classmethod
    def default(cls, config_id: str) -> "RateLimitConfig":
        """Get the default rate limit config."""
        return cls(
            config_id=config_id,
            requests_per_window=30,
            window_seconds=60,
            strategy=RateLimitStrategy.FIXED,
            max_batch_size=15,
            max_concurrent=1,
        )

    def overwrite(self, **kwargs: Any) -> None:
        """Overwrite the default values with the provided kwargs."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
