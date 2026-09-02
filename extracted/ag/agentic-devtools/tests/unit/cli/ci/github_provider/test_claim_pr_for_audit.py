"""Tests for GitHubActionsProvider.claim_pr_for_audit() method."""

import json
from unittest.mock import patch

from agentic_devtools.cli.audit.models import ClaimResult
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data) if isinstance(data, (dict, list)) else data
        stderr = ""

    return _Result()


class TestClaimPrForAudit:
    """Tests for GitHubActionsProvider.claim_pr_for_audit()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_claimed_when_label_absent(self, mock_run_safe) -> None:
        # First call: GET labels (no matching label)
        # Second call: POST to add label
        mock_run_safe.side_effect = [
            _mock_run_safe_response([{"name": "bug"}, {"name": "enhancement"}]),
            _mock_run_safe_response([{"name": "audit-in-progress"}]),
        ]

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.claim_pr_for_audit(pr_number=42, label="audit-in-progress")

        assert result == ClaimResult.CLAIMED

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_already_claimed_when_label_present(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response([{"name": "audit-in-progress"}, {"name": "bug"}])

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.claim_pr_for_audit(pr_number=42, label="audit-in-progress")

        assert result == ClaimResult.ALREADY_CLAIMED
