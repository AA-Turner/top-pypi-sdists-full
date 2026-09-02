"""Tests for _cleanup_failed_worktree_setup."""

import subprocess
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.workflows.worktree_setup import (
    WorktreeSetupResult,
    _cleanup_failed_worktree_setup,
)


class TestCleanupFailedWorktreeSetup:
    """Tests for _cleanup_failed_worktree_setup function."""

    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_cleanup_success_for_owned_worktree(self, mock_run, mock_root, capsys):
        """Test that cleanup removes an explicitly owned worktree."""
        mock_run.return_value = MagicMock(returncode=0)
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
        )

        _cleanup_failed_worktree_setup(result)

        mock_run.assert_called_once()
        assert "Cleanup attempted" in capsys.readouterr().out

    @patch("agentic_devtools.cli.copilot.trust.remove_trusted_folder", return_value=True)
    @patch("agentic_devtools.cli.workflows.worktree_setup.os.path.exists", return_value=False)
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_removes_trust_added_by_failed_setup(self, mock_run, mock_root, mock_exists, mock_remove_trust):
        """Remove an invocation-owned trust entry after worktree cleanup succeeds."""
        mock_run.return_value = MagicMock(returncode=0)
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
            copilot_trust_added=True,
        )

        _cleanup_failed_worktree_setup(result)

        mock_remove_trust.assert_called_once_with("/repos/PROJECT-1234")

    @patch("agentic_devtools.cli.copilot.trust.remove_trusted_folder")
    @patch("agentic_devtools.cli.workflows.worktree_setup.os.path.exists", return_value=True)
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_keeps_trust_when_worktree_cleanup_did_not_remove_path(
        self, mock_run, mock_root, mock_exists, mock_remove_trust
    ):
        """Keep trust when cleanup reports success but the worktree path remains."""
        mock_run.return_value = MagicMock(returncode=0)
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
            copilot_trust_added=True,
        )

        _cleanup_failed_worktree_setup(result)

        mock_remove_trust.assert_not_called()

    @patch("agentic_devtools.cli.copilot.trust.remove_trusted_folder")
    @patch("agentic_devtools.cli.workflows.worktree_setup.os.path.exists", return_value=True)
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_skips_branch_deletion_when_path_persists_after_success(
        self, mock_run, mock_root, mock_exists, mock_remove_trust, capsys
    ):
        """Do not delete the branch when the worktree path remains despite a zero exit code."""
        mock_run.return_value = MagicMock(returncode=0)
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
            created_branch=True,
        )

        _cleanup_failed_worktree_setup(result)

        mock_run.assert_called_once()
        assert "Manual recovery may be required" in capsys.readouterr().err

    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_branch_cleanup_failure_is_reported(self, mock_run, mock_root, capsys):
        """Test that failed cleanup of an owned branch remains best effort."""
        mock_run.side_effect = [MagicMock(returncode=0), MagicMock(returncode=1, stderr="branch cleanup failed")]
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
            created_branch=True,
        )

        _cleanup_failed_worktree_setup(result)

        assert "Manual recovery may be required for branch" in capsys.readouterr().err

    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_owned_branch_cleanup_succeeds(self, mock_run, mock_root):
        """Test that an owned branch is removed after its worktree."""
        mock_run.side_effect = [MagicMock(returncode=0), MagicMock(returncode=0)]
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
            created_branch=True,
        )

        _cleanup_failed_worktree_setup(result)

        assert mock_run.call_count == 2

    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_cleanup_failure_preserves_original_failure(self, mock_run, mock_root, capsys):
        """Test that cleanup errors are reported without masking setup failure."""
        mock_run.return_value = MagicMock(returncode=1, stderr="cleanup failed")
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
        )

        _cleanup_failed_worktree_setup(result)

        assert "retain the original target setup script failure" in capsys.readouterr().err

    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch(
        "agentic_devtools.cli.workflows.worktree_setup.subprocess.run",
        side_effect=OSError("git unavailable"),
    )
    def test_cleanup_launcher_exception_is_best_effort(self, mock_run, mock_root, capsys):
        """Test that cleanup launcher exceptions are bounded and non-fatal."""
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
        )

        _cleanup_failed_worktree_setup(result)

        assert "Manual recovery may be required" in capsys.readouterr().err

    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch(
        "agentic_devtools.cli.workflows.worktree_setup.subprocess.run",
        side_effect=subprocess.TimeoutExpired(["git", "worktree", "remove"], 30),
    )
    def test_worktree_remove_timeout_is_reported_and_returns(self, mock_run, mock_root, capsys):
        """Test that a stalled git worktree remove is bounded and reported without masking the setup failure."""
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
        )

        _cleanup_failed_worktree_setup(result)

        captured = capsys.readouterr()
        assert "retain the original target setup script failure" in captured.err
        assert "timed out" in captured.err

    @patch("agentic_devtools.cli.copilot.trust.remove_trusted_folder", return_value=True)
    @patch("agentic_devtools.cli.workflows.worktree_setup.os.path.exists", return_value=False)
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch(
        "agentic_devtools.cli.workflows.worktree_setup.subprocess.run",
        side_effect=subprocess.TimeoutExpired(["git", "worktree", "remove"], 30),
    )
    def test_removes_trust_when_timed_out_worktree_is_gone(self, mock_run, mock_root, mock_exists, mock_remove_trust):
        """Remove owned trust when timed-out worktree removal already removed the path."""
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
            copilot_trust_added=True,
        )

        _cleanup_failed_worktree_setup(result)

        mock_remove_trust.assert_called_once_with("/repos/PROJECT-1234")

    @patch("agentic_devtools.cli.copilot.trust.remove_trusted_folder", return_value=True)
    @patch(
        "agentic_devtools.cli.workflows.worktree_setup.os.path.exists",
        side_effect=[True, False, False, False],
    )
    @patch("time.sleep")
    @patch("time.monotonic", side_effect=[0, 1])
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch(
        "agentic_devtools.cli.workflows.worktree_setup.subprocess.run",
        side_effect=subprocess.TimeoutExpired(["git", "worktree", "remove"], 30),
    )
    def test_waits_for_delayed_worktree_removal_before_removing_trust(
        self, mock_run, mock_root, mock_monotonic, mock_sleep, mock_exists, mock_remove_trust
    ):
        """Wait briefly when a timed-out removal is still completing asynchronously."""
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
            copilot_trust_added=True,
        )

        _cleanup_failed_worktree_setup(result)

        mock_sleep.assert_called_once_with(1)
        mock_remove_trust.assert_called_once_with("/repos/PROJECT-1234")

    @patch("agentic_devtools.cli.copilot.trust.remove_trusted_folder")
    @patch("agentic_devtools.cli.workflows.worktree_setup.os.path.exists", return_value=True)
    @patch("time.sleep")
    @patch("time.monotonic", side_effect=[0, 11])
    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch(
        "agentic_devtools.cli.workflows.worktree_setup.subprocess.run",
        side_effect=subprocess.TimeoutExpired(["git", "worktree", "remove"], 30),
    )
    def test_keeps_trust_when_timed_out_worktree_remains(
        self, mock_run, mock_root, mock_monotonic, mock_sleep, mock_exists, mock_remove_trust
    ):
        """Keep owned trust when the timed-out worktree remains for recovery."""
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
            copilot_trust_added=True,
        )

        _cleanup_failed_worktree_setup(result)

        mock_sleep.assert_not_called()
        mock_remove_trust.assert_not_called()

    @patch("agentic_devtools.cli.workflows.worktree_setup.get_main_repo_root", return_value="/repos/main")
    @patch("agentic_devtools.cli.workflows.worktree_setup.subprocess.run")
    def test_branch_cleanup_timeout_is_reported_and_returns(self, mock_run, mock_root, capsys):
        """Test that a stalled git branch -D is bounded and reported without masking the setup failure."""
        mock_run.side_effect = [
            MagicMock(returncode=0),
            subprocess.TimeoutExpired(["git", "branch", "-D"], 30),
        ]
        result = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234",
            created_worktree=True,
            created_branch=True,
        )

        _cleanup_failed_worktree_setup(result)

        captured = capsys.readouterr()
        assert "retain the original target setup script failure" in captured.err
        assert "timed out" in captured.err
