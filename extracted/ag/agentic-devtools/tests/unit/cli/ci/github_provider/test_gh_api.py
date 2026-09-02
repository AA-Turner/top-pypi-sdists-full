"""Tests for github_provider._gh_api()."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import _gh_api
from agentic_devtools.cli.ci.retry import RetryableError


class _Result:
    returncode = 0
    stdout = "{}"
    stderr = ""


@patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_Result())
def test_gh_api_adds_headers_to_command(mock_run_safe) -> None:
    _gh_api(
        "/repos/owner/repo/copilot/coding-agent/tasks",
        method="POST",
        body={"problem_statement": "test"},
        headers={"X-GitHub-Api-Version": "2022-11-28"},
    )

    cmd = mock_run_safe.call_args.args[0]
    assert "-H" in cmd
    assert "X-GitHub-Api-Version: 2022-11-28" in cmd
    assert "--include" in cmd


@patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=_Result())
def test_gh_api_can_skip_included_headers_for_raw_body_calls(mock_run_safe) -> None:
    response = _gh_api("/repos/o/r/contents/file.txt", include_headers=False)

    cmd = mock_run_safe.call_args.args[0]
    assert "--include" not in cmd
    assert response == "{}"


def test_gh_api_extracts_rate_limit_headers() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = "HTTP/1.1 403 Forbidden\nRetry-After: 120\nX-RateLimit-Remaining: 0\n\n"
    result.stderr = ""
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RetryableError) as exc_info:
            _gh_api("/repos/o/r", credential_identity="COPILOT_GITHUB_TOKEN")
    assert exc_info.value.retry_after == 120
    assert exc_info.value.remaining == 0
    assert exc_info.value.credential_identity == "COPILOT_GITHUB_TOKEN"


def test_gh_api_aggregates_duplicate_rate_limit_headers_conservatively() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = (
        "HTTP/1.1 403 Forbidden\nRetry-After: 60, 120\nX-RateLimit-Reset: 100, 500\nX-RateLimit-Remaining: 1, 0\n\n"
    )
    result.stderr = ""
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RetryableError) as exc_info:
            _gh_api("/repos/o/r", credential_identity="COPILOT_GITHUB_TOKEN")
    assert exc_info.value.retry_after == 120
    assert exc_info.value.reset_timestamp == 500
    assert exc_info.value.remaining == 0


def test_gh_api_keeps_plain_forbidden_non_retryable() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = "HTTP/1.1 403 Forbidden\n\n"
    result.stderr = "HTTP 403: permission denied"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RuntimeError):
            _gh_api("/repos/o/r")


def test_gh_api_keeps_reset_only_forbidden_non_retryable() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = "HTTP/1.1 403 Forbidden\nX-RateLimit-Reset: 500\nX-RateLimit-Remaining: 1\n\n"
    result.stderr = "HTTP 403: resource not accessible by integration"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RuntimeError):
            _gh_api("/repos/o/r")


def test_gh_api_ignores_bare_status_digits_in_unrelated_error_text() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = ""
    result.stderr = "GraphQL: failed lookup for https://github.com/o/r/issues/503"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RuntimeError, match="GitHub API error"):
            _gh_api("/repos/o/r")


def test_gh_api_retries_on_bare_midline_server_status() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = ""
    result.stderr = "Request failed: 503 Service Unavailable"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RetryableError, match="server error"):
            _gh_api("/repos/o/r")


def test_gh_api_does_not_retry_structured_404_with_issue_url_digits() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = "HTTP/1.1 404 Not Found\n\n"
    result.stderr = "Not found: https://github.com/o/r/issues/503"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RuntimeError):
            _gh_api("/repos/o/r")


def test_gh_api_does_not_treat_issue_url_429_as_rate_limit() -> None:
    result = _Result()
    result.returncode = 1
    result.stdout = ""
    result.stderr = "lookup failed: https://github.com/o/r/issues/429"
    with patch("agentic_devtools.cli.ci.github_provider.run_safe", return_value=result):
        with pytest.raises(RuntimeError, match="GitHub API error"):
            _gh_api("/repos/o/r")
