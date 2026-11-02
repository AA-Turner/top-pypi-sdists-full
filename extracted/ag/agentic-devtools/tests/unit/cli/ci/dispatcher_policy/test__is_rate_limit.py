"""Tests for confirmed throttle API rate-limit classification."""

import pytest

from agentic_devtools.cli.ci.dispatcher_policy import _is_rate_limit


@pytest.mark.parametrize(
    ("status", "headers", "message", "expected"),
    [
        (429, {}, "", True),
        (403, {"retry-after": "120"}, "Forbidden", True),
        (403, {"x-ratelimit-remaining": "0"}, "Forbidden", True),
        (403, {}, "API rate limit exceeded", True),
        (403, {}, "secondary rate limit", True),
        (403, {"x-ratelimit-remaining": "42"}, "Resource not accessible", False),
        (403, {"x-ratelimit-remaining": "invalid"}, "Resource not accessible", False),
        (None, {}, "permission denied", False),
        (500, {}, "server unavailable", False),
    ],
)
def test_classifies_only_confirmed_rate_limits(status, headers, message, expected):
    assert _is_rate_limit(status, headers, message) is expected
