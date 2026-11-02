"""Daikin Onecta API rate-limit information."""

from collections.abc import Mapping
from dataclasses import dataclass


def _header_int(headers: Mapping[str, str], name: str) -> int | None:
    """Return an integer response header when it contains a valid value."""
    value = headers.get(name)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


@dataclass(frozen=True, slots=True)
class RateLimit:
    """Rate-limit state returned by the Daikin Onecta API."""

    minute_limit: int | None = None
    day_limit: int | None = None
    minute_remaining: int | None = None
    day_remaining: int | None = None
    retry_after: int | None = None
    reset: int | None = None

    @classmethod
    def from_headers(cls, headers: Mapping[str, str]) -> RateLimit:
        """Create rate-limit state from Daikin response headers."""
        return cls(
            minute_limit=_header_int(headers, "X-RateLimit-Limit-minute"),
            day_limit=_header_int(headers, "X-RateLimit-Limit-day"),
            minute_remaining=_header_int(headers, "X-RateLimit-Remaining-minute"),
            day_remaining=_header_int(headers, "X-RateLimit-Remaining-day"),
            retry_after=_header_int(headers, "Retry-After"),
            reset=_header_int(headers, "RateLimit-Reset"),
        )
