"""Daikin Onecta API rate-limit information."""

from __future__ import annotations

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
    def from_headers(cls, headers: Mapping[str, str], previous: RateLimit | None = None) -> RateLimit:
        """Create rate-limit state from Daikin response headers.

        Quota headers are sometimes omitted from error responses. Preserve the
        last reported quota values when a response does not provide them, but
        keep Retry-After scoped to the current response.
        """
        previous = previous or cls()

        def quota_header(name: str, previous_value: int | None) -> int | None:
            """Return a quota header or its last reported value."""
            value = _header_int(headers, name)
            return previous_value if value is None else value

        return cls(
            minute_limit=quota_header("X-RateLimit-Limit-minute", previous.minute_limit),
            day_limit=quota_header("X-RateLimit-Limit-day", previous.day_limit),
            minute_remaining=quota_header("X-RateLimit-Remaining-minute", previous.minute_remaining),
            day_remaining=quota_header("X-RateLimit-Remaining-day", previous.day_remaining),
            retry_after=_header_int(headers, "Retry-After"),
            reset=quota_header("RateLimit-Reset", previous.reset),
        )
