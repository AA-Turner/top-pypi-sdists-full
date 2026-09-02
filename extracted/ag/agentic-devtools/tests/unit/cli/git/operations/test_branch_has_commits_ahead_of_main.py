"""Tests for agentic_devtools.cli.git.operations.branch_has_commits_ahead_of_main."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.git import operations
from agentic_devtools.cli.git.core import GitError


class TestBranchHasCommitsAheadOfMain:
    """Tests for branch_has_commits_ahead_of_main function."""

    def test_returns_true_when_ahead(self, mock_run_safe):
        """Test returns True when branch is ahead of main."""
        with patch.object(operations, "get_current_branch", return_value="feature/test"):
            mock_run_safe.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),  # rev-parse origin/main
                MagicMock(returncode=0, stdout="3\n", stderr=""),  # 3 commits ahead
            ]
            result = operations.branch_has_commits_ahead_of_main()
            assert result is True

    def test_returns_false_when_not_ahead(self, mock_run_safe):
        """Test returns False when branch is not ahead."""
        with patch.object(operations, "get_current_branch", return_value="feature/test"):
            mock_run_safe.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),  # rev-parse origin/main
                MagicMock(returncode=0, stdout="0\n", stderr=""),  # 0 commits ahead
            ]
            result = operations.branch_has_commits_ahead_of_main()
            assert result is False

    def test_returns_false_when_on_main(self, mock_run_safe):
        """Test returns False when already on main branch."""
        with patch.object(operations, "get_current_branch", return_value="main"):
            result = operations.branch_has_commits_ahead_of_main()
            assert result is False

    def test_fallback_to_main_without_origin(self, mock_run_safe):
        """Test falls back to main when origin/main doesn't exist."""
        with patch.object(operations, "get_current_branch", return_value="feature/test"):
            mock_run_safe.side_effect = [
                MagicMock(returncode=1, stdout="", stderr="not found"),  # origin/main fails
                MagicMock(returncode=0, stdout="", stderr=""),  # main succeeds
                MagicMock(returncode=0, stdout="2\n", stderr=""),  # 2 commits ahead
            ]
            result = operations.branch_has_commits_ahead_of_main()
            assert result is True

    def test_returns_false_when_main_not_found(self, mock_run_safe):
        """Test returns False when neither origin/main nor main exists."""
        with patch.object(operations, "get_current_branch", return_value="feature/test"):
            mock_run_safe.side_effect = [
                MagicMock(returncode=1, stdout="", stderr="not found"),  # origin/main fails
                MagicMock(returncode=1, stdout="", stderr="not found"),  # main also fails
            ]
            result = operations.branch_has_commits_ahead_of_main()
            assert result is False

    def test_returns_false_on_rev_list_error(self, mock_run_safe):
        """Test returns False when rev-list fails."""
        with patch.object(operations, "get_current_branch", return_value="feature/test"):
            mock_run_safe.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),  # rev-parse succeeds
                MagicMock(returncode=1, stdout="", stderr="error"),  # rev-list fails
            ]
            result = operations.branch_has_commits_ahead_of_main()
            assert result is False

    def test_returns_false_on_invalid_count(self, mock_run_safe):
        """Test returns False when count is not a valid integer."""
        with patch.object(operations, "get_current_branch", return_value="feature/test"):
            mock_run_safe.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),  # rev-parse succeeds
                MagicMock(returncode=0, stdout="invalid\n", stderr=""),  # invalid count
            ]
            result = operations.branch_has_commits_ahead_of_main()
            assert result is False

    def test_origin_main_not_fresh_compares_against_local_main_only(self, mock_run_safe):
        """When origin_main_fresh is False, compare against local main without probing origin/main."""
        with patch.object(operations, "get_current_branch", return_value="feature/test"):
            mock_run_safe.side_effect = [
                MagicMock(returncode=0, stdout="", stderr=""),  # rev-parse main
                MagicMock(returncode=0, stdout="1\n", stderr=""),  # 1 commit ahead of local main
            ]

            result = operations.branch_has_commits_ahead_of_main(origin_main_fresh=False)

            assert result is True
            commands = [call.args[0] for call in mock_run_safe.call_args_list]
            assert commands == [
                ["git", "rev-parse", "--verify", "main"],
                ["git", "rev-list", "--count", "main..HEAD"],
            ]

    def test_origin_main_not_fresh_returns_false_when_local_main_missing(self, mock_run_safe):
        """When origin_main_fresh is False, a missing local main returns False."""
        with patch.object(operations, "get_current_branch", return_value="feature/test"):
            mock_run_safe.return_value = MagicMock(returncode=1, stdout="", stderr="not found")

            result = operations.branch_has_commits_ahead_of_main(origin_main_fresh=False)

            assert result is False
            mock_run_safe.assert_called_once()


class TestBranchHasCommitsAheadOfMainCwd:
    """Tests for the cwd-aware path (cwd=... uses run_git_capture, non-exiting)."""

    _OPS = "agentic_devtools.cli.git.operations"

    def _dispatch(self, mapping):
        def side(args, cwd=None):
            key = tuple(args[:3])
            for prefix, result in mapping.items():
                if key[: len(prefix)] == prefix:
                    return result
            return MagicMock(returncode=0, stdout="", stderr="")

        return side

    def test_returns_false_when_on_main(self):
        """Returns False without any ref check when HEAD is 'main'."""
        with patch(f"{self._OPS}.run_git_capture", return_value=MagicMock(returncode=0, stdout="main")):
            assert operations.branch_has_commits_ahead_of_main(cwd="/wt") is False

    def test_fresh_prefers_origin_main(self):
        """Prefers origin/main when fetch was fresh and origin/main exists."""
        mapping = {
            ("rev-parse", "--abbrev-ref"): MagicMock(returncode=0, stdout="feature/42/x"),
            ("rev-parse", "--verify", "origin/main"): MagicMock(returncode=0, stdout=""),
            ("rev-list", "--count"): MagicMock(returncode=0, stdout="2"),
        }
        with patch(f"{self._OPS}.run_git_capture", side_effect=self._dispatch(mapping)):
            assert operations.branch_has_commits_ahead_of_main(origin_main_fresh=True, cwd="/wt") is True

    def test_fresh_falls_back_to_local_main(self):
        """Falls back to local main when origin/main is missing."""
        mapping = {
            ("rev-parse", "--abbrev-ref"): MagicMock(returncode=0, stdout="feature/42/x"),
            ("rev-parse", "--verify", "origin/main"): MagicMock(returncode=1, stdout=""),
            ("rev-parse", "--verify", "main"): MagicMock(returncode=0, stdout=""),
            ("rev-list", "--count"): MagicMock(returncode=0, stdout="1"),
        }
        with patch(f"{self._OPS}.run_git_capture", side_effect=self._dispatch(mapping)):
            assert operations.branch_has_commits_ahead_of_main(origin_main_fresh=True, cwd="/wt") is True

    def test_fresh_no_ref_returns_false(self):
        """Returns False when neither origin/main nor local main exists."""
        mapping = {
            ("rev-parse", "--abbrev-ref"): MagicMock(returncode=0, stdout="feature/42/x"),
            ("rev-parse", "--verify", "origin/main"): MagicMock(returncode=1, stdout=""),
            ("rev-parse", "--verify", "main"): MagicMock(returncode=1, stdout=""),
        }
        with patch(f"{self._OPS}.run_git_capture", side_effect=self._dispatch(mapping)):
            assert operations.branch_has_commits_ahead_of_main(origin_main_fresh=True, cwd="/wt") is False

    def test_not_fresh_uses_local_main_only(self):
        """When origin_main_fresh=False, only local main is checked."""
        mapping = {
            ("rev-parse", "--abbrev-ref"): MagicMock(returncode=0, stdout="feature/42/x"),
            ("rev-parse", "--verify", "main"): MagicMock(returncode=0, stdout=""),
            ("rev-list", "--count"): MagicMock(returncode=0, stdout="3"),
        }
        with patch(f"{self._OPS}.run_git_capture", side_effect=self._dispatch(mapping)):
            assert operations.branch_has_commits_ahead_of_main(origin_main_fresh=False, cwd="/wt") is True

    def test_not_fresh_local_missing_returns_false(self):
        """Returns False when local main is missing in not-fresh mode."""
        mapping = {
            ("rev-parse", "--abbrev-ref"): MagicMock(returncode=0, stdout="feature/42/x"),
            ("rev-parse", "--verify", "main"): MagicMock(returncode=1, stdout=""),
        }
        with patch(f"{self._OPS}.run_git_capture", side_effect=self._dispatch(mapping)):
            assert operations.branch_has_commits_ahead_of_main(origin_main_fresh=False, cwd="/wt") is False

    def test_rev_list_error_raises_giterror(self):
        """Raises GitError when rev-list fails in cwd mode."""
        mapping = {
            ("rev-parse", "--abbrev-ref"): MagicMock(returncode=0, stdout="feature/42/x"),
            ("rev-parse", "--verify", "origin/main"): MagicMock(returncode=0, stdout=""),
            ("rev-list", "--count"): MagicMock(returncode=1, stdout="", stderr="probe failed"),
        }
        with patch(f"{self._OPS}.run_git_capture", side_effect=self._dispatch(mapping)):
            with pytest.raises(GitError, match="git rev-list --count origin/main\\.\\.HEAD failed with exit code 1"):
                operations.branch_has_commits_ahead_of_main(cwd="/wt")

    def test_rev_list_non_numeric_returns_false(self):
        """Returns False when rev-list output is not a valid integer."""
        mapping = {
            ("rev-parse", "--abbrev-ref"): MagicMock(returncode=0, stdout="feature/42/x"),
            ("rev-parse", "--verify", "origin/main"): MagicMock(returncode=0, stdout=""),
            ("rev-list", "--count"): MagicMock(returncode=0, stdout="notanumber"),
        }
        with patch(f"{self._OPS}.run_git_capture", side_effect=self._dispatch(mapping)):
            assert operations.branch_has_commits_ahead_of_main(cwd="/wt") is False
