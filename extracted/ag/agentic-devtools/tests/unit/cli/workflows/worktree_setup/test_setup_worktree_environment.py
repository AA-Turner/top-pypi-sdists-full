"""Tests for SetupWorktreeEnvironment."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.workflows.worktree_setup import (
    WorktreeSetupResult,
    WorktreeSetupScriptResult,
    setup_worktree_environment,
)

_INJECT_GIT = "agentic_devtools.cli.workflows.worktree_setup.inject_git_path_settings"
_INJECT_PYTHON = "agentic_devtools.cli.workflows.worktree_setup.inject_python_path_settings"
_INJECT_TASK = "agentic_devtools.cli.workflows.worktree_setup.inject_task_permission_settings"


class TestSetupWorktreeEnvironment:
    """Tests for setup_worktree_environment function."""

    def test_rejects_negative_target_setup_timeout(self):
        """Reject a negative target setup timeout before creating a worktree."""
        with pytest.raises(ValueError, match="target_setup_timeout must be non-negative"):
            setup_worktree_environment(issue_key="PROJECT-1234", target_setup_timeout=-1)

    @patch(_INJECT_GIT)
    @patch(_INJECT_PYTHON)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.run_worktree_setup_script")
    @patch("agentic_devtools.cli.workflows.worktree_setup.open_vscode_workspace")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_full_setup_success(
        self, mock_create, mock_vscode, mock_script, mock_inject_task, mock_inject_python, mock_inject_git
    ):
        """Test successful full environment setup."""
        mock_create.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234/implementation",
        )
        mock_vscode.return_value = True

        result = setup_worktree_environment(
            issue_key="PROJECT-1234",
            branch_prefix="feature",
            open_vscode=True,
        )

        assert result.success is True
        assert result.worktree_path == "/repos/PROJECT-1234"
        assert result.branch_name == "feature/PROJECT-1234/implementation"
        assert result.vscode_opened is True
        mock_script.assert_called_once_with("/repos/PROJECT-1234", timeout_seconds=60)
        mock_inject_git.assert_called_once_with("/repos/PROJECT-1234")
        mock_inject_task.assert_called_once_with("/repos/PROJECT-1234")

    @patch(_INJECT_GIT)
    @patch(_INJECT_PYTHON)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.run_worktree_setup_script")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_passes_target_setup_timeout(
        self, mock_create, mock_script, mock_inject_task, mock_inject_python, mock_inject_git
    ):
        """Forward the configured timeout to the target setup script."""
        mock_create.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234/implementation",
        )

        result = setup_worktree_environment(
            issue_key="PROJECT-1234",
            open_vscode=False,
            target_setup_timeout=120,
        )

        assert result.success is True
        mock_script.assert_called_once_with("/repos/PROJECT-1234", timeout_seconds=120)

    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_setup_fails_when_worktree_fails(self, mock_create):
        """Test setup failure when worktree creation fails."""
        mock_create.return_value = WorktreeSetupResult(
            success=False,
            worktree_path="",
            branch_name="",
            error_message="Git error",
        )

        result = setup_worktree_environment(issue_key="PROJECT-1234")

        assert result.success is False
        assert "Git error" in result.error_message

    @patch(_INJECT_GIT)
    @patch(_INJECT_PYTHON)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.run_worktree_setup_script")
    @patch("agentic_devtools.cli.workflows.worktree_setup.open_vscode_workspace")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_setup_without_vscode(
        self, mock_create, mock_vscode, mock_script, mock_inject_task, mock_inject_python, mock_inject_git
    ):
        """Test setup without opening VS Code."""
        mock_create.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234/implementation",
        )

        result = setup_worktree_environment(
            issue_key="PROJECT-1234",
            open_vscode=False,
        )

        assert result.success is True
        assert result.vscode_opened is False
        mock_vscode.assert_not_called()
        mock_script.assert_called_once_with("/repos/PROJECT-1234", timeout_seconds=60)
        mock_inject_git.assert_called_once_with("/repos/PROJECT-1234")
        mock_inject_task.assert_called_once_with("/repos/PROJECT-1234")

    @patch(_INJECT_GIT)
    @patch(_INJECT_PYTHON)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.run_worktree_setup_script")
    @patch("agentic_devtools.cli.workflows.worktree_setup.open_vscode_workspace", return_value=False)
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_vscode_opened_is_false_when_vscode_unavailable(
        self, mock_create, mock_vscode, mock_script, mock_inject_task, mock_inject_python, mock_inject_git
    ):
        """Test that vscode_opened is False when VS Code is not available."""
        mock_create.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234/implementation",
        )

        result = setup_worktree_environment(
            issue_key="PROJECT-1234",
            open_vscode=True,
        )

        assert result.success is True
        assert result.vscode_opened is False
        mock_inject_git.assert_called_once_with("/repos/PROJECT-1234")
        mock_inject_task.assert_called_once_with("/repos/PROJECT-1234")

    @patch(_INJECT_PYTHON)
    @patch(_INJECT_GIT)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.run_worktree_setup_script")
    @patch("agentic_devtools.cli.workflows.worktree_setup.open_vscode_workspace")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_inject_python_path_settings_called_with_worktree_path(
        self, mock_create, mock_vscode, mock_script, mock_inject_task, mock_inject_git, mock_inject_python
    ):
        """inject_python_path_settings is called with the worktree path on success."""
        mock_create.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234/implementation",
        )
        mock_vscode.return_value = True

        setup_worktree_environment(issue_key="PROJECT-1234", open_vscode=True)

        mock_inject_python.assert_called_once_with("/repos/PROJECT-1234")
        mock_inject_task.assert_called_once_with("/repos/PROJECT-1234")

    @patch(_INJECT_PYTHON)
    @patch(_INJECT_GIT)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_inject_python_path_settings_not_called_when_worktree_fails(
        self, mock_create, mock_inject_task, mock_inject_git, mock_inject_python
    ):
        """inject_python_path_settings is NOT called when worktree creation fails."""
        mock_create.return_value = WorktreeSetupResult(
            success=False,
            worktree_path="",
            branch_name="",
            error_message="Git error",
        )

        setup_worktree_environment(issue_key="PROJECT-1234")

        mock_inject_python.assert_not_called()
        mock_inject_task.assert_not_called()

    @patch(_INJECT_GIT)
    @patch(_INJECT_PYTHON)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.run_worktree_setup_script")
    @patch("agentic_devtools.cli.workflows.worktree_setup.open_vscode_workspace")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_target_setup_failure_prevents_vscode(
        self, mock_create, mock_vscode, mock_script, mock_inject_task, mock_inject_python, mock_inject_git
    ):
        """Test that a target setup failure is returned and VS Code is not opened."""
        mock_create.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234/implementation",
        )
        mock_script.return_value = WorktreeSetupScriptResult(
            status="failed",
            exit_code=1,
            error_message="provider setup failed",
            category="exit",
        )

        result = setup_worktree_environment(issue_key="PROJECT-1234", open_vscode=True)

        assert result.success is False
        assert result.worktree_path == "/repos/PROJECT-1234"
        assert result.branch_name == "feature/PROJECT-1234/implementation"
        assert result.target_setup_status == "failed"
        assert result.target_setup_exit_code == "1"
        assert result.target_setup_error == "exit: provider setup failed"
        mock_vscode.assert_not_called()

    @patch(_INJECT_GIT)
    @patch(_INJECT_PYTHON)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.run_worktree_setup_script")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_invalid_target_setup_status_is_failure(
        self, mock_create, mock_script, mock_inject_task, mock_inject_python, mock_inject_git
    ):
        """Test that an invalid script result status cannot report setup success."""
        mock_create.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234/implementation",
        )
        mock_script.return_value = WorktreeSetupScriptResult(status="unexpected")

        result = setup_worktree_environment(issue_key="PROJECT-1234", open_vscode=False)

        assert result.success is False
        assert result.target_setup_status == "failed"
        assert result.target_setup_exit_code == "blocked"
        assert "invalid status" in (result.target_setup_error or "")

    @patch(_INJECT_GIT)
    @patch(_INJECT_PYTHON)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.run_worktree_setup_script")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_target_setup_failure_message_remains_bounded_after_category_prefix(
        self, mock_create, mock_script, mock_inject_task, mock_inject_python, mock_inject_git
    ):
        """Test target-setup state and raised diagnostics stay within the documented bound."""
        mock_create.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234/implementation",
        )
        mock_script.return_value = WorktreeSetupScriptResult(
            status="failed",
            exit_code=1,
            error_message="x" * 4096,
            category="exit",
        )

        result = setup_worktree_environment(issue_key="PROJECT-1234", open_vscode=False)

        assert result.success is False
        assert len(result.target_setup_error or "") == 4096
        assert (result.target_setup_error or "").startswith("exit:")
        assert len(result.error_message or "") == 4096

    @patch(_INJECT_GIT)
    @patch(_INJECT_PYTHON)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.run_worktree_setup_script")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_defers_task_permission_injection_when_requested(
        self, mock_create, mock_script, mock_inject_task, mock_inject_python, mock_inject_git
    ):
        """Deferred setup leaves task permission injection for the caller."""
        mock_create.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234/implementation",
        )

        result = setup_worktree_environment(
            issue_key="PROJECT-1234",
            open_vscode=False,
            defer_task_permission_settings=True,
        )

        assert result.success is True
        mock_inject_git.assert_called_once_with("/repos/PROJECT-1234")
        mock_inject_python.assert_called_once_with("/repos/PROJECT-1234")
        mock_inject_task.assert_not_called()
        mock_script.assert_called_once_with("/repos/PROJECT-1234", timeout_seconds=60)

    @patch(_INJECT_GIT)
    @patch(_INJECT_PYTHON)
    @patch(_INJECT_TASK)
    @patch("agentic_devtools.cli.workflows.worktree_setup.run_worktree_setup_script")
    @patch("agentic_devtools.cli.workflows.worktree_setup.create_worktree")
    def test_defers_path_settings_injection_when_requested(
        self, mock_create, mock_script, mock_inject_task, mock_inject_python, mock_inject_git
    ):
        """Deferred setup leaves workspace PATH injection for the caller."""
        mock_create.return_value = WorktreeSetupResult(
            success=True,
            worktree_path="/repos/PROJECT-1234",
            branch_name="feature/PROJECT-1234/implementation",
        )

        result = setup_worktree_environment(
            issue_key="PROJECT-1234",
            open_vscode=False,
            defer_path_settings=True,
            defer_task_permission_settings=True,
        )

        assert result.success is True
        mock_inject_git.assert_not_called()
        mock_inject_python.assert_not_called()
        mock_inject_task.assert_not_called()
        mock_script.assert_called_once_with("/repos/PROJECT-1234", timeout_seconds=60)
