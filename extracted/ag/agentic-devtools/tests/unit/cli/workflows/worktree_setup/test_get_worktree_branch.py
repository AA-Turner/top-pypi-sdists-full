"""Tests for GetWorktreeBranch."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.workflows.worktree_setup import (
    get_worktree_branch,
)


class TestGetWorktreeBranch:
    """Tests for get_worktree_branch function."""

    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_returns_branch_name(self, mock_run):
        """Test returns current branch name for worktree path."""
        mock_run.return_value = MagicMock(returncode=0, stdout="feature/PROJECT-1234/review\n")

        result = get_worktree_branch("/repos/PROJECT-1234")

        assert result == "feature/PROJECT-1234/review"
        mock_run.assert_called_once_with(
            ["git", "-C", "/repos/PROJECT-1234", "branch", "--show-current"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_returns_none_on_detached_head(self, mock_run):
        """Test returns None when worktree has detached HEAD."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")

        result = get_worktree_branch("/repos/PROJECT-1234")

        assert result is None

    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_returns_none_on_git_error(self, mock_run):
        """Test returns None on git command failure."""
        mock_run.return_value = MagicMock(returncode=128, stdout="")

        result = get_worktree_branch("/repos/PROJECT-1234")

        assert result is None

    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run", side_effect=OSError)
    def test_returns_none_on_os_error(self, _mock_run):
        """Test returns None when subprocess execution raises OSError."""
        result = get_worktree_branch("/repos/PROJECT-1234")

        assert result is None
