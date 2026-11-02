"""Tests for GitHubActionsProvider.rebase_onto_base."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.pipeline.exceptions import (
    ForceWithLeaseError,
    RebaseConflictError,
)


class TestRebaseOntoBase:
    """Tests for rebase_onto_base method."""

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_successful_rebase_and_push(self, mock_run_git) -> None:
        expected_head = "a" * 40
        updated_head = "b" * 40
        head_reads = 0

        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return expected_head + "\n"
            if args == ["rev-parse", "refs/remotes/origin/feature"]:
                return expected_head + "\n"
            if args == ["rev-list", "--count", "origin/feature..origin/main"]:
                return "1\n"
            if args == ["rev-parse", "HEAD"]:
                nonlocal head_reads
                head_reads += 1
                return (expected_head if head_reads == 1 else updated_head) + "\n"
            return ""

        mock_run_git.side_effect = git_side_effect
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")

        mock_run_git.assert_any_call(
            [
                "fetch",
                "origin",
                "+refs/heads/main:refs/remotes/origin/main",
                "+refs/heads/feature:refs/remotes/origin/feature",
            ]
        )
        mock_run_git.assert_any_call(["checkout", "feature"])
        mock_run_git.assert_any_call(["rebase", "origin/main"])
        mock_run_git.assert_any_call(
            [
                "push",
                f"--force-with-lease=refs/heads/feature:{expected_head}",
                "origin",
                "HEAD:refs/heads/feature",
            ]
        )
        assert result == updated_head

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_skips_when_remote_head_mismatches_expected_head(self, mock_run_git) -> None:
        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "refs/remotes/origin/feature"]:
                return "def456\n"
            return ""

        mock_run_git.side_effect = git_side_effect
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")

        assert result is None
        mock_run_git.assert_any_call(
            [
                "fetch",
                "origin",
                "+refs/heads/main:refs/remotes/origin/main",
                "+refs/heads/feature:refs/remotes/origin/feature",
            ]
        )
        assert ["checkout", "feature"] not in [call.args[0] for call in mock_run_git.call_args_list]

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_skips_when_branch_is_no_longer_behind(self, mock_run_git) -> None:
        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "refs/remotes/origin/feature"]:
                return "abc123\n"
            if args == ["rev-list", "--count", "origin/feature..origin/main"]:
                return "0\n"
            return ""

        mock_run_git.side_effect = git_side_effect
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")

        assert result is None
        assert ["checkout", "feature"] not in [call.args[0] for call in mock_run_git.call_args_list]
        assert ["rebase", "origin/main"] not in [call.args[0] for call in mock_run_git.call_args_list]
        assert not any(call.args[0][0] == "push" for call in mock_run_git.call_args_list)

    @patch.object(GitHubActionsProvider, "_resolve_rebase_conflicts_via_sdk")
    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_rebase_conflict_error_when_unresolvable(self, mock_run_git, mock_resolve) -> None:
        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "refs/remotes/origin/feature"]:
                return "abc123\n"
            if args == ["rev-list", "--count", "origin/feature..origin/main"]:
                return "1\n"
            if args == ["rev-parse", "HEAD"]:
                return "abc123\n"
            if args == ["rebase", "origin/main"]:
                raise RuntimeError("conflict")
            if args == ["rebase", "--abort"]:
                return ""
            return ""

        mock_run_git.side_effect = git_side_effect
        mock_resolve.return_value = False
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RebaseConflictError, match="could not be auto-resolved"):
            provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")

    @patch.object(GitHubActionsProvider, "_resolve_rebase_conflicts_via_sdk")
    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_rebase_conflict_error_when_abort_fails(self, mock_run_git, mock_resolve) -> None:
        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "refs/remotes/origin/feature"]:
                return "abc123\n"
            if args == ["rev-list", "--count", "origin/feature..origin/main"]:
                return "1\n"
            if args == ["rev-parse", "HEAD"]:
                return "abc123\n"
            if args == ["rebase", "origin/main"]:
                raise RuntimeError("conflict")
            if args == ["rebase", "--abort"]:
                raise RuntimeError("abort failed")
            return ""

        mock_run_git.side_effect = git_side_effect
        mock_resolve.return_value = False
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RebaseConflictError, match="abort failed"):
            provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_does_not_overwrite_head_changed_after_comparison(self, mock_run_git) -> None:
        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "refs/remotes/origin/feature"]:
                return "abc123\n"
            if args == ["rev-list", "--count", "origin/feature..origin/main"]:
                return "1\n"
            if args == ["rev-parse", "HEAD"]:
                return "abc123\n"
            if args == [
                "push",
                "--force-with-lease=refs/heads/feature:abc123",
                "origin",
                "HEAD:refs/heads/feature",
            ]:
                raise RuntimeError("push rejected")
            return ""

        mock_run_git.side_effect = git_side_effect
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(ForceWithLeaseError, match="push rejected"):
            provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")
        mock_run_git.assert_any_call(
            ["push", "--force-with-lease=refs/heads/feature:abc123", "origin", "HEAD:refs/heads/feature"]
        )

    @patch.object(GitHubActionsProvider, "_resolve_rebase_conflicts_via_sdk")
    @patch.object(GitHubActionsProvider, "_run_git")
    def test_successful_rebase_after_conflict_resolution(self, mock_run_git, mock_resolve) -> None:
        call_count = {"rebase": 0}

        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "refs/remotes/origin/feature"]:
                return "abc123\n"
            if args == ["rev-list", "--count", "origin/feature..origin/main"]:
                return "1\n"
            if args == ["rev-parse", "HEAD"]:
                return "abc123\n"
            if args == ["rebase", "origin/main"]:
                call_count["rebase"] += 1
                if call_count["rebase"] == 1:
                    raise RuntimeError("conflict")
            return ""

        mock_run_git.side_effect = git_side_effect
        mock_resolve.return_value = True
        provider = GitHubActionsProvider(repo="owner/repo")

        provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")

        mock_run_git.assert_any_call(
            ["push", "--force-with-lease=refs/heads/feature:abc123", "origin", "HEAD:refs/heads/feature"]
        )

    @patch.object(GitHubActionsProvider, "_resolve_rebase_conflicts_via_sdk")
    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_rebase_conflict_when_resolve_raises(self, mock_run_git, mock_resolve) -> None:
        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "refs/remotes/origin/feature"]:
                return "abc123\n"
            if args == ["rev-list", "--count", "origin/feature..origin/main"]:
                return "1\n"
            if args == ["rev-parse", "HEAD"]:
                return "abc123\n"
            if args == ["rebase", "origin/main"]:
                raise RuntimeError("conflict")
            if args == ["rebase", "--abort"]:
                return ""
            return ""

        mock_run_git.side_effect = git_side_effect
        mock_resolve.side_effect = RuntimeError("SDK failure")
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RebaseConflictError, match="could not be auto-resolved"):
            provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_when_checked_out_head_differs_from_snapshot(self, mock_run_git) -> None:
        def git_side_effect(args):
            if args == ["rev-parse", "abc123"]:
                return "abc123\n"
            if args == ["rev-parse", "refs/remotes/origin/feature"]:
                return "abc123\n"
            if args == ["rev-list", "--count", "origin/feature..origin/main"]:
                return "1\n"
            if args == ["rev-parse", "HEAD"]:
                return "def456\n"
            return ""

        mock_run_git.side_effect = git_side_effect
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="Head SHA changed before rebase"):
            provider.rebase_onto_base(pr_number=1, base_branch="main", head_branch="feature", head_sha="abc123")
