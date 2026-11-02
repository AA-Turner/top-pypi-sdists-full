"""Tests for Daikin Onecta rate-limit parsing."""

from daikin_onecta import RateLimit


def test_rate_limit_from_headers() -> None:
    """Parse all supported Daikin rate-limit headers."""
    rate_limit = RateLimit.from_headers(
        {
            "X-RateLimit-Limit-minute": "20",
            "X-RateLimit-Limit-day": "200",
            "X-RateLimit-Remaining-minute": "7",
            "X-RateLimit-Remaining-day": "123",
            "Retry-After": "42",
            "RateLimit-Reset": "99",
        }
    )

    assert rate_limit.minute_limit == 20
    assert rate_limit.day_limit == 200
    assert rate_limit.minute_remaining == 7
    assert rate_limit.day_remaining == 123
    assert rate_limit.retry_after == 42
    assert rate_limit.reset == 99


def test_rate_limit_ignores_invalid_headers() -> None:
    """Invalid or absent headers should not break a request."""
    rate_limit = RateLimit.from_headers({"Retry-After": "invalid"})

    assert rate_limit.retry_after is None
    assert rate_limit.minute_limit is None
