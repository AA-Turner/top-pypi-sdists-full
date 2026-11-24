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


def test_rate_limit_preserves_quota_values_when_headers_are_missing() -> None:
    """Keep the last reported quota values when a response omits the headers."""
    previous = RateLimit(
        minute_limit=20,
        day_limit=200,
        minute_remaining=7,
        day_remaining=123,
        retry_after=42,
        reset=99,
    )

    rate_limit = RateLimit.from_headers({}, previous)

    assert rate_limit.minute_limit == 20
    assert rate_limit.day_limit == 200
    assert rate_limit.minute_remaining == 7
    assert rate_limit.day_remaining == 123
    assert rate_limit.retry_after is None
    assert rate_limit.reset == 99


def test_rate_limit_zero_remaining_overrides_previous_value() -> None:
    """Do not treat a zero remaining quota as an omitted header."""
    previous = RateLimit(day_remaining=12)

    rate_limit = RateLimit.from_headers({"X-RateLimit-Remaining-day": "0"}, previous)

    assert rate_limit.day_remaining == 0
