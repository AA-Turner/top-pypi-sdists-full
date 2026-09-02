"""Tests for run_git_safe."""

from subprocess import CompletedProcess

import pytest

from agentic_devtools.cli.git.core import GitError, run_git_safe


class TestRunGitSafe:
    """Tests for run_git_safe."""

    def test_returns_completed_process_on_success_and_forwards_safe_options(self, mock_run_safe):
        """Successful git commands return the CompletedProcess and force shell=False."""
        expected = CompletedProcess(args=["git", "status"], returncode=0, stdout="clean", stderr="")
        mock_run_safe.return_value = expected

        result = run_git_safe(["status"], cwd="/repo/worktree")

        assert result is expected
        mock_run_safe.assert_called_once_with(
            ["git", "status"],
            capture_output=True,
            text=True,
            shell=False,
            cwd="/repo/worktree",
        )

    def test_raises_git_error_on_non_zero_exit_with_stderr(self, mock_run_safe):
        """A non-zero git result raises GitError carrying stderr and command details."""
        mock_run_safe.return_value = CompletedProcess(
            args=["git", "fetch", "origin"],
            returncode=128,
            stdout="",
            stderr=" fatal: auth failed \n",
        )

        with pytest.raises(GitError) as exc_info:
            run_git_safe(["fetch", "origin"])

        error = exc_info.value
        assert error.returncode == 128
        assert error.stderr == "fatal: auth failed"
        assert error.args_list == ["fetch", "origin"]
        assert str(error) == "git fetch origin failed with exit code 128: fatal: auth failed"

    def test_raises_git_error_with_no_stderr_message_form(self, mock_run_safe):
        """GitError omits the stderr suffix when stderr is empty."""
        mock_run_safe.return_value = CompletedProcess(args=["git", "status"], returncode=1, stdout="", stderr="")

        with pytest.raises(GitError, match="git status failed with exit code 1$"):
            run_git_safe(["status"])

    def test_wraps_os_error_as_git_error(self, mock_run_safe):
        """Process startup failures are translated into GitError for callers."""
        mock_run_safe.side_effect = FileNotFoundError(2, "No such file or directory", "git")

        with pytest.raises(GitError) as exc_info:
            run_git_safe(["status"], cwd="/missing/repo")

        error = exc_info.value
        assert error.returncode == 2
        assert error.stderr == "[Errno 2] No such file or directory: 'git'"
        assert error.args_list == ["status"]
