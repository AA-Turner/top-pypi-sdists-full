"""Tests for setup_worktree_cmd."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.workflows.commands import setup_worktree_cmd
from agentic_devtools.cli.workflows.worktree_setup import WorktreeSetupResult


class TestSetupWorktreeCmd:
    """Tests for the setup-only worktree command."""

    @patch("agentic_devtools.cli.workflows.worktree_setup.setup_worktree_in_background_sync")
    def test_sets_up_worktree_without_starting_copilot(self, mock_setup, capsys):
        """The command forwards PR worktree parameters and reports the prepared path."""
        mock_setup.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/DFLY-1234",
            branch_name="feature/DFLY-1234-review",
        )
        mock_setup.side_effect = lambda **_: (
            print("setup output"),
            mock_setup.return_value,
        )[1]

        result = setup_worktree_cmd(
            _argv=[
                "--issue-key",
                "DFLY-1234",
                "--branch-name",
                "feature/DFLY-1234-review",
                "--use-existing-branch",
            ]
        )

        assert result.success is True
        mock_setup.assert_called_once_with(
            issue_key="DFLY-1234",
            branch_prefix="feature",
            branch_name="feature/DFLY-1234-review",
            use_existing_branch=True,
            workflow_name="setup-worktree",
            auto_execute_command=None,
            start_copilot_session=False,
        )
        output = json.loads(capsys.readouterr().out)
        assert output == {
            "status": "success",
            "success": True,
            "worktree_path": "/repos/DFLY-1234",
            "branch_name": "feature/DFLY-1234-review",
        }

    @patch("agentic_devtools.cli.workflows.worktree_setup.setup_worktree_in_background_sync")
    def test_forwards_default_branch_name_for_existing_branch(self, mock_setup):
        """The existing-branch flag uses the computed branch when no name is provided."""
        mock_setup.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/DFLY-1234",
            branch_name="review/DFLY-1234/implementation",
        )

        setup_worktree_cmd(
            _argv=[
                "--issue-key",
                "DFLY-1234",
                "--branch-prefix",
                "review",
                "--use-existing-branch",
            ]
        )

        mock_setup.assert_called_once_with(
            issue_key="DFLY-1234",
            branch_prefix="review",
            branch_name="review/DFLY-1234/implementation",
            use_existing_branch=True,
            workflow_name="setup-worktree",
            auto_execute_command=None,
            start_copilot_session=False,
        )

    @patch("agentic_devtools.cli.workflows.worktree_setup.setup_worktree_in_background_sync")
    def test_reports_unsuccessful_setup_result(self, mock_setup, capsys):
        """A returned unsuccessful result is reported and exits non-zero."""
        mock_setup.return_value = WorktreeSetupResult(
            success=False,
            worktree_path="/repos/DFLY-1234",
            branch_name="feature/DFLY-1234/implementation",
            error_message="setup failed",
        )

        with pytest.raises(SystemExit) as exc_info:
            setup_worktree_cmd(_argv=["--issue-key", "DFLY-1234"])

        assert exc_info.value.code == 1
        output = json.loads(capsys.readouterr().out)
        assert output["status"] == "failure"
        assert output["error"] == "setup failed"

    @patch("agentic_devtools.cli.workflows.worktree_setup.setup_worktree_in_background_sync")
    def test_reports_setup_failure(self, mock_setup, capsys):
        """A setup exception is reported as a failure and returns a non-zero exit."""
        mock_setup.side_effect = RuntimeError("target setup failed")

        with pytest.raises(SystemExit) as exc_info:
            setup_worktree_cmd(_argv=["--issue-key", "DFLY-1234"])

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert captured.err == ""
        output = json.loads(captured.out)
        assert output == {
            "status": "failure",
            "success": False,
            "worktree_path": "",
            "branch_name": "feature/DFLY-1234/implementation",
            "error": "target setup failed",
        }

    @patch("agentic_devtools.cli.workflows.worktree_setup.setup_worktree_in_background_sync")
    def test_forwards_setup_output_when_setup_raises(self, mock_setup, capsys):
        """Setup output is forwarded to stderr when setup raises."""

        def raise_after_output(**_):
            print("setup output")
            raise RuntimeError("target setup failed")

        mock_setup.side_effect = raise_after_output

        with pytest.raises(SystemExit) as exc_info:
            setup_worktree_cmd(_argv=["--issue-key", "DFLY-1234"])

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert captured.err == "setup output\n"
        output = json.loads(captured.out)
        assert output == {
            "status": "failure",
            "success": False,
            "worktree_path": "",
            "branch_name": "feature/DFLY-1234/implementation",
            "error": "target setup failed",
        }
