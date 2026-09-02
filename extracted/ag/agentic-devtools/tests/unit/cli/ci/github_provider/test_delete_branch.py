"""Tests for GitHubActionsProvider.delete_branch() method."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


class TestDeleteBranch:
    """Tests for GitHubActionsProvider.delete_branch()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_delete_branch_calls_correct_endpoint(self, mock_run_safe) -> None:
        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.delete_branch("feature/my-branch")

        args = mock_run_safe.call_args[0][0]
        assert "/repos/owner/repo/git/refs/heads/feature%2Fmy-branch" in " ".join(args)
        assert "DELETE" in args

    @pytest.mark.parametrize(
        ("branch", "encoded_branch"),
        [
            ("main", "main"),
            ("copilot/fix/issue-123", "copilot%2Ffix%2Fissue-123"),
        ],
    )
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_delete_branch_encodes_branch_name(
        self,
        mock_run_safe,
        branch: str,
        encoded_branch: str,
    ) -> None:
        class _Result:
            returncode = 0
            stdout = ""
            stderr = ""

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.delete_branch(branch)

        args = mock_run_safe.call_args[0][0]
        assert f"/repos/owner/repo/git/refs/heads/{encoded_branch}" in " ".join(args)
        assert "DELETE" in args

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_delete_branch_raises_on_failure(self, mock_run_safe) -> None:
        class _Result:
            returncode = 1
            stdout = ""
            stderr = "Reference does not exist"

        mock_run_safe.return_value = _Result()

        provider = GitHubActionsProvider(repo="owner/repo")
        with pytest.raises(RuntimeError):
            provider.delete_branch("nonexistent-branch")
