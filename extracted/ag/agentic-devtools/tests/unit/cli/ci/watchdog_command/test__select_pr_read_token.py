"""Tests for _select_pr_read_token()."""

import os
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.retry import RetryableError
from agentic_devtools.cli.ci.watchdog_command import _select_pr_read_token


class TestSelectPrReadToken:
    """Credential probe fallback policy for redispatch stop conditions."""

    def test_uses_first_capable_token(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"SPECKIT_PR_TOKEN": "speckit", "GITHUB_TOKEN": "ambient"},
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value="[]") as gh_api,
        ):
            token = _select_pr_read_token("o/r")

        assert token == "speckit"
        gh_api.assert_called_once()

    def test_skips_authorization_failure_and_uses_fallback(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"SPECKIT_PR_TOKEN": "speckit", "GITHUB_TOKEN": "ambient"},
                clear=True,
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                side_effect=[RuntimeError("HTTP 403"), "[]"],
            ),
        ):
            token = _select_pr_read_token("o/r")

        assert token == "ambient"

    def test_rejects_non_authorization_probe_failure(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"SPECKIT_PR_TOKEN": "speckit", "GITHUB_TOKEN": "ambient"},
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", side_effect=RuntimeError("network down")),
        ):
            with pytest.raises(RuntimeError, match="inventory probe failed"):
                _select_pr_read_token("o/r")

    def test_rejects_retryable_probe_failure(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"SPECKIT_PR_TOKEN": "speckit", "GITHUB_TOKEN": "ambient"},
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", side_effect=RetryableError("HTTP 503")),
        ):
            with pytest.raises(RuntimeError, match="inventory probe failed"):
                _select_pr_read_token("o/r")

    def test_rejects_malformed_probe_response(self) -> None:
        with (
            patch.dict(os.environ, {"SPECKIT_PR_TOKEN": "speckit"}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value='{"bad":1}'),
        ):
            with pytest.raises(RuntimeError, match="malformed response"):
                _select_pr_read_token("o/r")

    def test_rejects_non_json_probe_response(self) -> None:
        with (
            patch.dict(os.environ, {"SPECKIT_PR_TOKEN": "speckit"}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value="not-json"),
        ):
            with pytest.raises(RuntimeError, match="malformed response"):
                _select_pr_read_token("o/r")

    def test_errors_when_no_candidate_can_read_prs(self) -> None:
        with patch.dict(os.environ, {"SPECKIT_PR_TOKEN": "", "GITHUB_TOKEN": ""}, clear=True):
            with pytest.raises(RuntimeError, match="No credential can read repository pull requests"):
                _select_pr_read_token("o/r")
