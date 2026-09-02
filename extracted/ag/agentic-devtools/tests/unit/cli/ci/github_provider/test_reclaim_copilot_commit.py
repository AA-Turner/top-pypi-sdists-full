"""Tests for GitHubActionsProvider.reclaim_copilot_commit()."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.pipeline.exceptions import ForceWithLeaseError


class TestReclaimCopilotCommit:
    """Tests for reclaim_copilot_commit method."""

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_amends_and_force_pushes(self, mock_run_git) -> None:
        """Re-authors HEAD and force-pushes under the configured identity."""

        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "HEAD"]:
                return "abc123\n"
            return ""

        mock_run_git.side_effect = git_side_effect
        provider = GitHubActionsProvider(repo="owner/repo")

        provider.reclaim_copilot_commit(pr_number=1, head_branch="feature", head_sha="abc123")

        mock_run_git.assert_any_call(["fetch", "origin", "feature"])
        mock_run_git.assert_any_call(["checkout", "feature"])
        mock_run_git.assert_any_call(["commit", "--amend", "--reset-author", "--no-edit"])
        mock_run_git.assert_any_call(["push", "--force-with-lease", "origin", "HEAD:feature"])

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_when_head_moved(self, mock_run_git) -> None:
        """Raises RuntimeError when HEAD changed before the reclaim."""

        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "HEAD"]:
                return "def456\n"
            return ""

        mock_run_git.side_effect = git_side_effect
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="Head SHA changed before Copilot takeover"):
            provider.reclaim_copilot_commit(pr_number=1, head_branch="feature", head_sha="abc123")

        # The amend/push must not run once the safety check fails.
        assert ["commit", "--amend", "--reset-author", "--no-edit"] not in [
            c.args[0] for c in mock_run_git.call_args_list
        ]

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_force_with_lease_error_on_push_failure(self, mock_run_git) -> None:
        """Maps a failed force-push to ForceWithLeaseError."""

        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "HEAD"]:
                return "abc123\n"
            if args == ["push", "--force-with-lease", "origin", "HEAD:feature"]:
                raise RuntimeError("push rejected")
            return ""

        mock_run_git.side_effect = git_side_effect
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ForceWithLeaseError, match="Force-push-with-lease failed during Copilot takeover"):
            provider.reclaim_copilot_commit(pr_number=1, head_branch="feature", head_sha="abc123")
