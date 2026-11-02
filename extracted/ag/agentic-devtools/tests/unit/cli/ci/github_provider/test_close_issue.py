"""Tests for GitHubActionsProvider.close_issue()."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


class TestCloseIssue:
    """Tests for the issue close used when reaping a no-change PR."""

    @pytest.mark.parametrize("reason", ["completed", "not_planned"])
    def test_patches_state_and_reason(self, reason: str) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="{}") as mock_api:
            provider.close_issue(1240, reason=reason)

        assert mock_api.call_args.args[0].endswith("/issues/1240")
        assert mock_api.call_args.kwargs["method"] == "PATCH"
        assert mock_api.call_args.kwargs["body"] == {"state": "closed", "state_reason": reason}

    def test_defaults_to_completed(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api", return_value="{}") as mock_api:
            provider.close_issue(1240)

        assert mock_api.call_args.kwargs["body"]["state_reason"] == "completed"

    def test_rejects_an_unknown_reason(self) -> None:
        provider = GitHubActionsProvider(repo="o/r")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api") as mock_api:
            with pytest.raises(ValueError, match="reason must be 'completed' or 'not_planned'"):
                provider.close_issue(1240, reason="duplicate")
        mock_api.assert_not_called()
