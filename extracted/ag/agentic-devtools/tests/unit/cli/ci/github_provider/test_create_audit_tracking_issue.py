"""Tests for GitHubActionsProvider.create_audit_tracking_issue()."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_run_safe_response(data: dict) -> object:
    class _Result:
        returncode = 0
        stdout = json.dumps(data)
        stderr = ""

    return _Result()


class TestCreateAuditTrackingIssue:
    """Tests for create_audit_tracking_issue behavior."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_creates_issue_with_speckit_token(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({"number": 2042})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            issue_number = provider.create_audit_tracking_issue(batch_id="1234567890", pr_numbers=[10, 11])

        assert issue_number == 2042
        call = mock_run_safe.call_args
        cmd = call.args[0]
        assert "/repos/swai-factory/agentic-devtools/issues" in cmd
        assert call.kwargs["env"]["GH_TOKEN"] == "token-value"

    def test_raises_when_speckit_token_missing(self) -> None:
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError, match="SPECKIT_PR_TOKEN"):
                provider.create_audit_tracking_issue(batch_id="1234567890", pr_numbers=[10])

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_raises_when_issue_number_missing_from_response(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response({})
        provider = GitHubActionsProvider(repo="swai-factory/agentic-devtools")

        with patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "token-value"}, clear=True):
            with pytest.raises(RuntimeError, match="missing issue number"):
                provider.create_audit_tracking_issue(batch_id="1234567890", pr_numbers=[10])
