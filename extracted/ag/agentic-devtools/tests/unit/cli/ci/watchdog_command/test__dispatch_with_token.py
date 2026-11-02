"""Tests for _dispatch_with_token()."""

from unittest.mock import patch

from agentic_devtools.cli.ci.retry import RetryableError
from agentic_devtools.cli.ci.watchdog_command import _dispatch_with_token


class TestDispatchWithToken:
    """Dispatch wrapper status mapping."""

    def test_returns_success_when_dispatch_api_call_succeeds(self) -> None:
        with patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value=""):
            status, message = _dispatch_with_token("wf.yml", "o/r", "main", "token")

        assert status == 0
        assert message == ""

    def test_returns_authorization_status_for_401_403_failures(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            side_effect=RuntimeError("HTTP 403: Resource not accessible by personal access token"),
        ):
            status, message = _dispatch_with_token("wf.yml", "o/r", "main", "token")

        assert status == 1
        assert "403" in message

    def test_returns_generic_failure_for_non_authorization_errors(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            side_effect=RuntimeError("workflow dispatch failed"),
        ):
            status, message = _dispatch_with_token("wf.yml", "o/r", "main", "token")

        assert status == 2
        assert "workflow dispatch failed" in message

    def test_returns_generic_failure_for_retryable_errors(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            side_effect=RetryableError("HTTP 503 service unavailable"),
        ):
            status, message = _dispatch_with_token("wf.yml", "o/r", "main", "token")

        assert status == 2
        assert "503" in message

    def test_treats_rate_limited_retryable_403_as_non_authorization_failure(self) -> None:
        with patch(
            "agentic_devtools.cli.ci.watchdog_command._gh_api",
            side_effect=RetryableError("GitHub API rate limited (HTTP 403)"),
        ):
            status, message = _dispatch_with_token("wf.yml", "o/r", "main", "token")

        assert status == 2
        assert "rate limited" in message
