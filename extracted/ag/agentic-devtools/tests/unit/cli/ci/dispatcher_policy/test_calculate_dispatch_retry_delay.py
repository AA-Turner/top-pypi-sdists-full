"""Tests for dispatcher retry delay selection."""

import pytest

from agentic_devtools.cli.ci.dispatcher_policy import calculate_dispatch_retry_delay


def test_uses_fallback_when_quota_remains_even_if_primary_reset_is_near() -> None:
    delay = calculate_dispatch_retry_delay(
        {
            "Retry-After": "",
            "X-RateLimit-Remaining": "42",
            "X-RateLimit-Reset": "1001",
        },
        now=1000,
    )

    assert delay == 60


@pytest.mark.parametrize(
    ("headers", "expected_delay"),
    [
        ({"Retry-After": "not-a-date"}, 60),
        ({"Retry-After": "²"}, 60),
        ({"X-RateLimit-Remaining": "0"}, 60),
        ({"X-RateLimit-Remaining": "invalid", "X-RateLimit-Reset": "1001"}, 60),
        ({"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "invalid"}, 60),
        ({"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1001"}, 2),
    ],
)
def test_handles_invalid_retry_metadata_and_exhausted_quota(headers: dict[str, str], expected_delay: int) -> None:
    delay = calculate_dispatch_retry_delay(headers, now=1000)

    assert delay == expected_delay


def test_ignores_non_string_header_values() -> None:
    delay = calculate_dispatch_retry_delay({"Retry-After": None, "X-RateLimit-Reset": 1001}, now=1000)  # type: ignore[dict-item]

    assert delay == 60


@pytest.mark.parametrize(
    ("headers", "expected_delay"),
    [
        ({"Retry-After": "172800"}, 172800),
        ({"Retry-After": "Sat, 03 Jan 1970 00:16:40 GMT"}, 172800),
        ({"X-RateLimit-Reset": "173800", "X-RateLimit-Remaining": "0"}, 172801),
    ],
)
def test_does_not_shorten_provider_deadline_to_the_wake_ttl(headers, expected_delay):
    assert calculate_dispatch_retry_delay(headers, now=1000) == expected_delay
