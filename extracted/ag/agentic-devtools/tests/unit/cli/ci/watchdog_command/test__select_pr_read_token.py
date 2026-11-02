"""Tests for _select_pr_read_token()."""

import os
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.retry import RetryableError
from agentic_devtools.cli.ci.watchdog_command import _select_pr_read_token


class TestSelectPrReadToken:
    """Credential probe policy for redispatch stop conditions."""

    def test_uses_default_workflow_token(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token"},
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value="[]") as gh_api,
        ):
            token = _select_pr_read_token("o/r")

        assert token == "workflow-token"
        gh_api.assert_called_once()

    def test_does_not_use_legacy_token_after_authorization_failure(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token", "SPECKIT_PR_TOKEN": "legacy"},
                clear=True,
            ),
            patch(
                "agentic_devtools.cli.ci.watchdog_command._gh_api",
                side_effect=RuntimeError("HTTP 403"),
            ),
        ):
            with pytest.raises(RuntimeError, match="inventory probe failed"):
                _select_pr_read_token("o/r")

    def test_rejects_non_authorization_probe_failure(self) -> None:
        with (
            patch.dict(
                os.environ,
                {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token"},
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
                {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token"},
                clear=True,
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", side_effect=RetryableError("HTTP 503")),
        ):
            with pytest.raises(RuntimeError, match="inventory probe failed"):
                _select_pr_read_token("o/r")

    def test_rejects_malformed_probe_response(self) -> None:
        with (
            patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token"}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value='{"bad":1}'),
        ):
            with pytest.raises(RuntimeError, match="malformed response"):
                _select_pr_read_token("o/r")

    def test_rejects_non_json_probe_response(self) -> None:
        with (
            patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "workflow-token"}, clear=True),
            patch("agentic_devtools.cli.ci.watchdog_command._gh_api", return_value="not-json"),
        ):
            with pytest.raises(RuntimeError, match="malformed response"):
                _select_pr_read_token("o/r")

    def test_errors_when_no_candidate_can_read_prs(self) -> None:
        with patch.dict(os.environ, {"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": ""}, clear=True):
            with pytest.raises(RuntimeError, match="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT is required"):
                _select_pr_read_token("o/r")
