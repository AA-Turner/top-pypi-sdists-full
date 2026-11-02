"""Tests for primary-quota reset selection."""

import pytest

from agentic_devtools.cli.ci.dispatcher_policy import _primary_reset


@pytest.mark.parametrize(
    ("headers", "expected"),
    [
        ({}, None),
        ({"x-ratelimit-remaining": "invalid"}, None),
        ({"x-ratelimit-remaining": "42", "x-ratelimit-reset": "900"}, None),
        ({"x-ratelimit-remaining": "0"}, None),
        ({"x-ratelimit-remaining": "0", "x-ratelimit-reset": "invalid"}, None),
        ({"x-ratelimit-remaining": "0", "x-ratelimit-reset": "900"}, 900),
    ],
)
def test_uses_only_exhausted_primary_quota_reset(headers, expected):
    assert _primary_reset(headers) == expected
