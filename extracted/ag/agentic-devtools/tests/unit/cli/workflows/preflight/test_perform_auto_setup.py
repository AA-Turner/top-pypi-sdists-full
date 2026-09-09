"""Tests for PerformAutoSetup."""

from unittest.mock import patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli.workflows.preflight import (
    perform_auto_setup,
)


@pytest.fixture
def temp_state_dir(tmp_path):
    """Fixture to redirect state writes to a temp directory."""
    with patch("agentic_devtools.state.get_state_dir", return_value=tmp_path):
        yield tmp_path


class TestPerformAutoSetup:
    """Tests for perform_auto_setup function."""

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_starts_background_task_successfully(self, mock_start_background, capsys):
        """Test successful background task start."""
        mock_start_background.return_value = "task-12345"

        result = perform_auto_setup(
            issue_key="PROJECT-1234",
            branch_prefix="feature",
            workflow_name="work-on-jira-issue",
        )

        assert result is True
        mock_start_background.assert_called_once_with(
            issue_key="PROJECT-1234",
            branch_prefix="feature",
            branch_name=None,
            use_existing_branch=False,
            workflow_name="work-on-jira-issue",
            user_request=None,
            additional_params=None,
            auto_execute_command=None,
            auto_execute_timeout=1800,
            interactive=False,
            model=None,
        )
        captured = capsys.readouterr()
        assert "task-12345" in captured.out
        assert "Background task started" in captured.out

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_passes_user_request_to_background(self, mock_start_background, capsys):
        """Test that user_request is passed to background task."""
        mock_start_background.return_value = "task-67890"

        perform_auto_setup(
            issue_key="PROJECT-5678",
            branch_prefix="bugfix",
            workflow_name="create-jira-issue",
            user_request="Create a new feature for testing",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["user_request"] == "Create a new feature for testing"

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_passes_additional_params_to_background(self, mock_start_background, capsys):
        """Test that additional_params are passed to background task."""
        mock_start_background.return_value = "task-abc"

        perform_auto_setup(
            issue_key="PROJECT-9999",
            branch_prefix="feature",
            workflow_name="create-jira-issue",
            additional_params={"parent_key": "PROJECT-1000"},
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["additional_params"] == {"parent_key": "PROJECT-1000"}

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_handles_exception_gracefully(self, mock_start_background, capsys):
        """Test that exceptions are caught and return False."""
        mock_start_background.side_effect = Exception("Connection failed")

        result = perform_auto_setup(
            issue_key="PROJECT-1234",
            branch_prefix="feature",
            workflow_name="work-on-jira-issue",
        )

        assert result is False
        captured = capsys.readouterr()
        assert "Failed to start background task" in captured.out
        assert "Connection failed" in captured.out

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_prints_next_steps_instructions(self, mock_start_background, capsys):
        """Test that next steps instructions are printed."""
        mock_start_background.return_value = "task-xyz"

        perform_auto_setup(
            issue_key="PROJECT-1234",
            branch_prefix="feature",
            workflow_name="work-on-jira-issue",
        )

        captured = capsys.readouterr()
        assert "NEXT STEPS" in captured.out
        assert "agdt-task-log" in captured.out
        assert "agdt-task-wait" in captured.out
        assert "Copilot session will start automatically" in captured.out

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_langchain_prints_background_review_instructions(self, mock_start_background, capsys):
        """LangChain auto-setup should point users to task monitoring instead of Copilot."""
        mock_start_background.return_value = "task-langchain"

        perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="pull-request-review",
            starts_copilot_session=False,
        )

        captured = capsys.readouterr()
        assert "LangChain review pipeline will continue automatically" in captured.out
        assert "No Copilot session is planned for this run" in captured.out
        assert "agdt-task-log" in captured.out
        assert "Copilot session will start automatically" not in captured.out

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_passes_auto_execute_command_to_background(self, mock_start_background, capsys):
        """Test that auto_execute_command is passed through to the background task."""
        mock_start_background.return_value = "task-exec"

        perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="pull-request-review",
            auto_execute_command=["agdt-initiate-pull-request-review-workflow", "--pr-id", "99"],
            auto_execute_timeout=120,
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_command"] == [
            "agdt-initiate-pull-request-review-workflow",
            "--pr-id",
            "99",
        ]
        assert call_kwargs["auto_execute_timeout"] == 120

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_appends_terminal_flag_to_auto_execute_command_when_terminal_mode_selected(
        self, mock_start_background, capsys
    ):
        """Dedicated terminal mode should be preserved for nested workflow execution."""
        mock_start_background.return_value = "task-exec"
        auto_execute_command = ["agdt-initiate-work-on-jira-issue-workflow", "--issue-key", "PROJECT-1234"]

        perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="work-on-jira-issue",
            terminal=True,
            auto_execute_command=auto_execute_command,
        )

        assert mock_start_background.call_args.kwargs["auto_execute_command"] == [
            "agdt-initiate-work-on-jira-issue-workflow",
            "--issue-key",
            "PROJECT-1234",
            "--copilot-terminal",
        ]
        assert auto_execute_command == ["agdt-initiate-work-on-jira-issue-workflow", "--issue-key", "PROJECT-1234"]

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_does_not_append_duplicate_terminal_flag_to_auto_execute_command(self, mock_start_background, capsys):
        """Existing terminal flags should be preserved without duplication."""
        mock_start_background.return_value = "task-exec"

        perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="work-on-jira-issue",
            terminal=True,
            auto_execute_command=["agdt-initiate-work-on-jira-issue-workflow", "--terminal"],
        )

        assert mock_start_background.call_args.kwargs["auto_execute_command"] == [
            "agdt-initiate-work-on-jira-issue-workflow",
            "--terminal",
        ]

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_passes_interactive_false_to_background(self, mock_start_background, capsys):
        """Test that interactive=False is passed to the background task."""
        mock_start_background.return_value = "task-pipeline"

        perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="pull-request-review",
            interactive=False,
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["interactive"] is False

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_passes_headless_to_background(self, mock_start_background, capsys):
        """Test that headless mode is passed to the background task."""
        mock_start_background.return_value = "task-headless"

        result = perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="work-on-jira-issue",
            headless=True,
        )

        assert result is True
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["headless"] is True
        captured = capsys.readouterr()
        assert "headless Copilot session" in captured.out

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_passes_interactive_false_by_default(self, mock_start_background, capsys):
        """Test that interactive defaults to False when not specified."""
        mock_start_background.return_value = "task-default"

        perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="work-on-jira-issue",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["interactive"] is False

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_passes_terminal_mode_to_background(self, mock_start_background, capsys):
        """Dedicated terminal selection is forwarded to worktree setup."""
        mock_start_background.return_value = "task-terminal"

        perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="work-on-jira-issue",
            terminal=True,
        )

        mock_start_background.assert_called_once()
        assert mock_start_background.call_args.kwargs["terminal"] is True

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_terminal_mode_prints_dedicated_terminal_next_steps(self, mock_start_background, capsys):
        """Dedicated terminal auto-setup messaging should not claim VS Code launches."""
        mock_start_background.return_value = "task-terminal"

        perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="work-on-jira-issue",
            terminal=True,
        )

        captured = capsys.readouterr()
        assert "dedicated terminal window" in captured.out
        assert "VS Code integrated terminal" not in captured.out

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_headless_overrides_terminal_mode(self, mock_start_background, capsys):
        """Headless auto-setup should suppress dedicated terminal launches."""
        mock_start_background.return_value = "task-headless"

        perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="work-on-jira-issue",
            headless=True,
            terminal=True,
        )

        call_kwargs = mock_start_background.call_args.kwargs
        assert call_kwargs["headless"] is True
        assert "terminal" not in call_kwargs
        captured = capsys.readouterr()
        assert "headless Copilot session" in captured.out
        assert "dedicated terminal window" not in captured.out

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_saves_task_id_to_state(self, mock_start_background, temp_state_dir):
        """Test that background.task_id is saved to state after spawning the background task.

        This is the bug fix test: previously perform_auto_setup only printed the task ID
        but did not persist it to state, causing agdt-task-wait (without --id) to fail
        with "Error: No task ID specified".
        """
        mock_start_background.return_value = "task-auto-set-check"

        perform_auto_setup(
            issue_key="PROJECT-1234",
            workflow_name="work-on-jira-issue",
        )

        assert state.get_value("background.task_id") == "task-auto-set-check"

    def test_auto_execute_timeout_default_is_none(self):
        """Verify the default value of auto_execute_timeout is None (sentinel)."""
        import inspect

        sig = inspect.signature(perform_auto_setup)
        default = sig.parameters["auto_execute_timeout"].default
        assert default is None

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_passes_model_to_background(self, mock_start_background, capsys):
        """Test that model parameter is forwarded to start_worktree_setup_background."""
        mock_start_background.return_value = "task-model"

        perform_auto_setup(
            issue_key="TEST-1",
            workflow_name="pull-request-review",
            model="gpt-4o",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["model"] == "gpt-4o"

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_model_defaults_to_none(self, mock_start_background, capsys):
        """Test that model defaults to None when not specified."""
        mock_start_background.return_value = "task-no-model"

        perform_auto_setup(
            issue_key="TEST-1",
            workflow_name="work-on-jira-issue",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["model"] is None

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_pr_review_workflow_uses_600s_timeout(self, mock_start_background, temp_state_dir):
        """Test that pull-request-review workflow uses 600s timeout by default."""
        mock_start_background.return_value = "task-pr-review"

        perform_auto_setup(
            issue_key="TEST-1",
            workflow_name="pull-request-review",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 600

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_apply_suggestions_workflow_uses_300s_timeout(self, mock_start_background, temp_state_dir):
        """Test that apply-pull-request-review-suggestions workflow uses 300s timeout."""
        mock_start_background.return_value = "task-apply"

        perform_auto_setup(
            issue_key="TEST-2",
            workflow_name="apply-pull-request-review-suggestions",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 300

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_explicit_timeout_overrides_workflow_default(self, mock_start_background, temp_state_dir):
        """Test that an explicit auto_execute_timeout overrides the workflow default."""
        mock_start_background.return_value = "task-override"

        perform_auto_setup(
            issue_key="TEST-3",
            workflow_name="pull-request-review",
            auto_execute_timeout=120,
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 120

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_explicit_60s_timeout_overrides_workflow_default(self, mock_start_background, temp_state_dir):
        """Test that an explicit 60s timeout is preserved for mapped workflows."""
        mock_start_background.return_value = "task-override-60"

        perform_auto_setup(
            issue_key="TEST-3B",
            workflow_name="pull-request-review",
            auto_execute_timeout=60,
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 60

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_unmapped_workflow_uses_1800s_default(self, mock_start_background, temp_state_dir):
        """Test that an unmapped workflow name results in the 1800s default timeout."""
        mock_start_background.return_value = "task-unmapped"

        perform_auto_setup(
            issue_key="TEST-4",
            workflow_name="work-on-jira-issue",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 1800

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_state_timeout_overrides_workflow_default(self, mock_start_background, temp_state_dir):
        """Test that a state-configured timeout overrides the workflow default."""
        mock_start_background.return_value = "task-state-override"
        state.set_value("worktree_setup.auto_execute_timeout", "1200")

        perform_auto_setup(
            issue_key="TEST-5",
            workflow_name="work-on-jira-issue",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 1200

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_integer_state_timeout_overrides_workflow_default(self, mock_start_background, temp_state_dir):
        """Test that an integer state timeout overrides the workflow default."""
        mock_start_background.return_value = "task-int-state-override"
        state.set_value("worktree_setup.auto_execute_timeout", 1200)

        perform_auto_setup(
            issue_key="TEST-5A",
            workflow_name="work-on-jira-issue",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 1200

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_invalid_state_timeout_uses_workflow_default(self, mock_start_background, temp_state_dir):
        """Test that an invalid state timeout falls back to the workflow default."""
        mock_start_background.return_value = "task-invalid-state-override"
        state.set_value("worktree_setup.auto_execute_timeout", "not-a-timeout")

        perform_auto_setup(
            issue_key="TEST-6",
            workflow_name="pull-request-review",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 600

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_signed_non_integer_state_timeout_uses_workflow_default(self, mock_start_background, temp_state_dir):
        """Test that a signed non-integer state timeout falls back to default."""
        mock_start_background.return_value = "task-signed-invalid-state-override"
        state.set_value("worktree_setup.auto_execute_timeout", "+abc")

        perform_auto_setup(
            issue_key="TEST-6A",
            workflow_name="pull-request-review",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 600

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_negative_state_timeout_uses_workflow_default(self, mock_start_background, temp_state_dir):
        """Test that a negative state timeout falls back to the workflow default."""
        mock_start_background.return_value = "task-negative-state-override"
        state.set_value("worktree_setup.auto_execute_timeout", "-1")

        perform_auto_setup(
            issue_key="TEST-7",
            workflow_name="pull-request-review",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 600

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_float_state_timeout_uses_workflow_default(self, mock_start_background, temp_state_dir):
        """Test that a float state timeout falls back to the workflow default."""
        mock_start_background.return_value = "task-float-state-override"
        state.set_value("worktree_setup.auto_execute_timeout", 1.5)

        perform_auto_setup(
            issue_key="TEST-8",
            workflow_name="pull-request-review",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 600

    @patch("agentic_devtools.cli.workflows.worktree_setup.start_worktree_setup_background")
    def test_boolean_state_timeout_uses_workflow_default(self, mock_start_background, temp_state_dir):
        """Test that a boolean state timeout falls back to the workflow default."""
        mock_start_background.return_value = "task-boolean-state-override"
        state.set_value("worktree_setup.auto_execute_timeout", True)

        perform_auto_setup(
            issue_key="TEST-9",
            workflow_name="pull-request-review",
        )

        mock_start_background.assert_called_once()
        call_kwargs = mock_start_background.call_args[1]
        assert call_kwargs["auto_execute_timeout"] == 600
