"""Tests for Retry-After parsing."""

import pytest

from agentic_devtools.cli.ci.dispatcher_policy import MAX_RETRY_WINDOW_SECONDS, _retry_after_seconds


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, None),
        ("", None),
        ("invalid", None),
        ("120", 120),
        ("Sat, 03 Jan 1970 00:16:40 GMT", 172800),
        ("9" * 400, MAX_RETRY_WINDOW_SECONDS + 1),
    ],
)
def test_parses_numeric_or_http_date_retry_after(value, expected):
    assert _retry_after_seconds(value, 1000) == expected
