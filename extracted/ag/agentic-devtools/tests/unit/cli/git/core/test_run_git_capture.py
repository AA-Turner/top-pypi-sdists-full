"""Tests for run_git_capture."""

from subprocess import CompletedProcess

import pytest

from agentic_devtools.cli.git.core import GitError, run_git_capture


class TestRunGitCapture:
    """Tests for run_git_capture."""

    def test_returns_result_on_success_and_forwards_safe_options(self, mock_run_safe):
        """Successful probe commands return their CompletedProcess."""
        expected = CompletedProcess(args=["git", "rev-parse", "HEAD"], returncode=0, stdout="abc", stderr="")
        mock_run_safe.return_value = expected

        result = run_git_capture(["rev-parse", "HEAD"], cwd="/repo/worktree")

        assert result is expected
        mock_run_safe.assert_called_once_with(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            shell=False,
            cwd="/repo/worktree",
        )

    def test_returns_non_zero_result_without_raising(self, mock_run_safe):
        """Failed probe commands are returned for caller inspection."""
        expected = CompletedProcess(args=["git", "diff", "--quiet"], returncode=1, stdout="", stderr="changed")
        mock_run_safe.return_value = expected

        result = run_git_capture(["diff", "--quiet"])

        assert result is expected
        assert result.returncode == 1

    def test_wraps_os_error_as_git_error(self, mock_run_safe):
        """Execution failures still raise GitError so callers can block cleanly."""
        mock_run_safe.side_effect = OSError("cwd disappeared")

        with pytest.raises(GitError) as exc_info:
            run_git_capture(["rev-parse", "HEAD"], cwd="/repo/worktree")

        error = exc_info.value
        assert error.returncode == 1
        assert error.stderr == "cwd disappeared"
        assert error.args_list == ["rev-parse", "HEAD"]
