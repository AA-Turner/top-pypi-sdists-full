"""Tests for CheckWorktreeExists."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.git.core import GitError
from agentic_devtools.cli.git.worktree import DetectionResult
from agentic_devtools.cli.workflows.worktree_setup import (
    check_worktree_exists,
)


class TestCheckWorktreeExists:
    """Tests for check_worktree_exists function."""

    @patch("agentic_devtools.cli.git.worktree.detect_existing_worktree")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_returns_path_when_worktree_exists(self, mock_parent, mock_main_repo, mock_detect):
        """Test returning path when worktree exists."""
        mock_parent.return_value = "/repos"
        mock_main_repo.return_value = "/repos/main"
        mock_detect.return_value = DetectionResult(status="resume", path="/repos/PROJECT-1234")

        result = check_worktree_exists("PROJECT-1234")

        assert "PROJECT-1234" in result

    @patch("agentic_devtools.cli.git.worktree.detect_existing_worktree")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_requires_explicit_registration_when_requested(self, mock_parent, mock_main_repo, mock_detect):
        """Explicit registration checks pass the fail-closed requirement to detection."""
        mock_parent.return_value = "/repos"
        mock_main_repo.return_value = "/repos/main"
        mock_detect.return_value = DetectionResult(status="not_found")

        result = check_worktree_exists("PROJECT-1234", require_registered=True)

        assert result is None
        mock_detect.assert_called_once_with(
            "PROJECT-1234",
            "/repos/main",
            require_porcelain=True,
            expected_path=None,
        )

    @patch("agentic_devtools.cli.git.worktree.detect_existing_worktree")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_requires_registration_at_expected_path(self, mock_parent, mock_main_repo, mock_detect):
        """Match post-create registration by path when the branch is arbitrary."""
        mock_parent.return_value = "/repos"
        mock_main_repo.return_value = "/repos/main"
        mock_detect.return_value = DetectionResult(status="resume", path="/repos/PR123")

        result = check_worktree_exists(
            "PR123",
            require_registered=True,
            expected_path="/repos/PR123",
        )

        assert result == "/repos/PR123"
        mock_detect.assert_called_once_with(
            "PR123",
            "/repos/main",
            require_porcelain=True,
            expected_path="/repos/PR123",
        )

    @patch("agentic_devtools.cli.git.worktree.detect_existing_worktree")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_returns_none_when_worktree_not_exists(self, mock_parent, mock_main_repo, mock_detect):
        """Test returning None when worktree doesn't exist."""
        mock_parent.return_value = "/repos"
        mock_main_repo.return_value = "/repos/main"
        mock_detect.return_value = DetectionResult(status="not_found")

        result = check_worktree_exists("PROJECT-1234")

        assert result is None

    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_returns_none_when_parent_not_found(self, mock_parent):
        """Test returning None when parent directory not found."""
        mock_parent.return_value = None

        result = check_worktree_exists("PROJECT-1234")

        assert result is None

    @patch("agentic_devtools.cli.git.worktree.detect_existing_worktree")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_raises_lookup_error_when_main_repo_root_unavailable(self, mock_parent, mock_main_repo, mock_detect):
        """Git metadata lookup failures must not be treated as a missing worktree."""
        mock_parent.return_value = "/repos"
        mock_main_repo.return_value = None

        with pytest.raises(GitError, match="unable to resolve main repository root"):
            check_worktree_exists("PROJECT-1234")

        mock_detect.assert_not_called()

    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value=None)
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_raises_lookup_error_when_registered_root_is_unavailable(self, mock_parent, mock_main_repo):
        """Required registration checks must not turn a root lookup failure into not_found."""
        mock_parent.return_value = "/repos"

        with pytest.raises(GitError, match="unable to resolve main repository root"):
            check_worktree_exists("PROJECT-1234", require_registered=True)

    @patch("agentic_devtools.cli.git.worktree.detect_existing_worktree")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_returns_none_when_not_valid_git_worktree(self, mock_parent, mock_main_repo, mock_detect):
        """Report a validation failure when git metadata marks the conventional path invalid."""
        mock_parent.return_value = "/repos"
        mock_main_repo.return_value = "/repos/main"
        mock_detect.return_value = DetectionResult(status="corrupt", path="/repos/PROJECT-1234")

        with pytest.raises(GitError, match="candidate /repos/PROJECT-1234 is invalid"):
            check_worktree_exists("PROJECT-1234")

    @patch("agentic_devtools.cli.git.worktree.detect_existing_worktree")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_preserves_registered_corruption_for_required_registration(self, mock_parent, mock_main_repo, mock_detect):
        """Report invalid registered metadata instead of treating it as missing."""
        mock_parent.return_value = "/repos"
        mock_main_repo.return_value = "/repos/main"
        mock_detect.return_value = DetectionResult(status="corrupt", path="/repos/PR123")

        with pytest.raises(GitError, match="candidate /repos/PR123 is invalid"):
            check_worktree_exists(
                "PR123",
                require_registered=True,
                expected_path="/repos/PR123",
            )

    @patch("agentic_devtools.cli.git.worktree.detect_existing_worktree")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_propagates_sanitized_git_metadata_lookup_failure(self, mock_parent, mock_main_repo, mock_detect):
        """Git metadata lookup errors must remain distinguishable from missing worktrees."""
        mock_parent.return_value = "/repos"
        mock_main_repo.return_value = "/repos/main"
        mock_detect.side_effect = GitError(128, "fatal", ["worktree", "list", "--porcelain"])

        with pytest.raises(GitError, match="fatal"):
            check_worktree_exists("PROJECT-1234")

    @pytest.mark.parametrize("error", [FileNotFoundError(), OSError()])
    @patch("agentic_devtools.cli.git.worktree.detect_existing_worktree")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    def test_propagates_non_git_lookup_errors(self, mock_parent, mock_main_repo, mock_detect, error):
        """Non-Git metadata lookup errors remain distinguishable from missing worktrees."""
        mock_parent.return_value = "/repos"
        mock_main_repo.return_value = "/repos/main"
        mock_detect.side_effect = error

        with pytest.raises(type(error)):
            check_worktree_exists("PROJECT-1234")

    @patch("agentic_devtools.cli.git.worktree.detect_existing_worktree")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root")
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_repos_parent_dir")
    @patch("agentic_devtools.cli.workflows.worktree_setup.os.path.exists")
    def test_returns_none_when_path_exists_but_git_metadata_is_missing(
        self, mock_exists, mock_parent, mock_main_repo, mock_detect
    ):
        """A leftover directory with a .git entry must not resume without git worktree metadata."""
        mock_parent.return_value = "/repos"
        mock_main_repo.return_value = "/repos/main"
        mock_exists.side_effect = [True, True]
        mock_detect.return_value = DetectionResult(status="not_found")

        result = check_worktree_exists("PROJECT-1234")

        assert result is None
