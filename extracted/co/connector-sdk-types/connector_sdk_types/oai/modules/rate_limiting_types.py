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


class RateLimitExtractor(ABC):
    """Abstract base class for extracting rate limit information from response."""

    @abstractmethod
    def extract(self, response: Any) -> RateLimitExtractorResponse:
        """Extract rate limit information from response."""
        raise NotImplementedError


class RateLimitConfigBase(BaseModel):
    """Base configuration for rate limiting."""

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
    # Initial delay between batches in seconds
    initial_delay: float = 0.0
    # Maximum delay between batches in seconds
    max_delay: float = 60.0
    # Backoff factor for exponential backoff
    backoff_factor: float = 1.5
    # Concurrency configuration (maximum number of concurrent requests)
    max_concurrent: int = 1
    # Rate limit mode. None = SDK auto-selects (write → RETRY_ONLY, read → ENFORCE)
    mode: RateLimitMode | None = None


class RateLimitConfig(RateLimitConfigBase):
    """Configuration for rate limiting."""

    # App ID of the current connector.
    # Deprecated: prefer config_id for connectors with multiple rate limit tiers.
    # app_id is kept for backwards compatibility and as the fallback when config_id is not set.
    app_id: str

    # Optional per-tier identifier, e.g. "github-rest" or "github-graphql".
    # When set, used in place of app_id for rate limit state keying so each tier's
    # state survives independently across page calls.
    config_id: str | None = None

    @property
    def effective_config_id(self) -> str:
        """config_id if set, otherwise app_id. Use this as the key for state passthrough."""
        return self.config_id if self.config_id is not None else self.app_id

    # Function to extract rate limit info from response
    rate_limit_extractor: Callable[[httpx.Response], RateLimitExtractorResponse] | None = None

    # Function to check if an error is a rate limit error, overrides default is_rate_limit_error
    rate_limit_error_check: Callable[[Exception], bool] | None = None

    # Function to check if an error is a transient error, overrides default is_transient_error
    transient_error_check: Callable[[Exception], bool] | None = None

    @classmethod
    def default(cls, app_id: str) -> "RateLimitConfig":
        """Get the default rate limit config."""
        return cls(
            app_id=app_id,
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
