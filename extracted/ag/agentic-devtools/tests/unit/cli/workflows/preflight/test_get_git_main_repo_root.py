"""Tests for GetGitMainRepoRoot."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.preflight import get_git_main_repo_root


class TestGetGitMainRepoRoot:
    """Tests for get_git_main_repo_root function."""

    def test_returns_main_checkout_root(self):
        """Test that it returns the parent of the shared git directory."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "/home/user/repos/my-repo/.git\n"

            result = get_git_main_repo_root()

            assert result == "/home/user/repos/my-repo"

    def test_returns_none_on_failure(self):
        """Test that it returns None when git cannot provide the common directory."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 128

            result = get_git_main_repo_root()

            assert result is None

    def test_returns_common_directory_when_not_a_dot_git_directory(self):
        """Test that it preserves an unusual common-directory result."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "/home/user/repos/shared\n"

            result = get_git_main_repo_root()

            assert result == "/home/user/repos/shared"
