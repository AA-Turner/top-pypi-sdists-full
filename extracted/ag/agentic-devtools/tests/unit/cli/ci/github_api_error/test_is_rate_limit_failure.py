"""Tests for GitHub API rate-limit classification."""

import pytest

from agentic_devtools.cli.ci.github_api_error import is_rate_limit_failure


@pytest.mark.parametrize(
    ("stderr", "status", "retry_after", "remaining", "expected"),
    [
        ("API rate limit exceeded", 403, None, 1, True),
        ("secondary rate limit", None, None, None, True),
        ("", 429, None, None, True),
        ("", 403, 30, 1, True),
        ("", None, None, 0, True),
        ("", 403, None, 1, False),
        ("", 404, None, 0, False),
    ],
)
def test_classifies_rate_limit_evidence(
    stderr: str,
    status: int | None,
    retry_after: int | None,
    remaining: int | None,
    expected: bool,
) -> None:
    assert is_rate_limit_failure(stderr, status, retry_after, remaining) is expected


@pytest.mark.parametrize("status", [403, 404, 422])
def test_bare_permanent_status_is_not_a_cooldown(status: int) -> None:
    assert is_rate_limit_failure(f"{status} Request rejected", status, None, None) is False
