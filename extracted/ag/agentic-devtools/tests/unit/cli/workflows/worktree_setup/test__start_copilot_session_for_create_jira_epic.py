"""Tests for _start_copilot_session_for_create_jira_epic."""

import os
from unittest.mock import patch

from agentic_devtools.cli.workflows.worktree_setup import (
    _start_copilot_session_for_create_jira_epic,
)


class TestStartCopilotSessionForCreateJiraEpic:
    """Tests for _start_copilot_session_for_create_jira_epic function."""

    @patch(
        "agentic_devtools.cli.workflows.worktree_setup._start_copilot_session_for_workflow",
        return_value=True,
    )
    @patch("agentic_devtools.state.get_state_dir")
    def test_delegates_to_generic_helper(self, mock_state_dir, mock_generic, tmp_path):
        """Verify the wrapper calls _start_copilot_session_for_workflow with correct args."""
        state_dir = tmp_path / ".agdt" / "workflows" / "_unscoped"
        state_dir.mkdir(parents=True)
        mock_state_dir.return_value = state_dir

        _start_copilot_session_for_create_jira_epic(str(tmp_path), interactive=True)

        mock_generic.assert_called_once()
        call_kwargs = mock_generic.call_args[1]
        assert call_kwargs["worktree_path"] == str(tmp_path)
        assert call_kwargs["prompt_file_relative_path"].endswith("temp-create-jira-epic-initiate-prompt.md")
        assert call_kwargs["workflow_name"] == "create-jira-epic"
        assert call_kwargs["interactive"] is True

    @patch(
        "agentic_devtools.cli.workflows.worktree_setup._start_copilot_session_for_workflow",
        return_value=True,
    )
    @patch("agentic_devtools.state.get_state_dir")
    def test_prompt_file_relative_path_resolves_from_state_dir(self, mock_state_dir, mock_generic, tmp_path):
        """Verify the prompt file path is relative to the worktree root."""
        state_dir = tmp_path / ".agdt" / "workflows" / "_unscoped"
        state_dir.mkdir(parents=True)
        mock_state_dir.return_value = state_dir

        _start_copilot_session_for_create_jira_epic(str(tmp_path))

        call_kwargs = mock_generic.call_args[1]
        expected_relative = os.path.relpath(
            str(state_dir / "temp-create-jira-epic-initiate-prompt.md"),
            str(tmp_path),
        )
        assert call_kwargs["prompt_file_relative_path"] == expected_relative

    @patch("agentic_devtools.cli.workflows.worktree_setup._start_copilot_session_for_workflow")
    @patch("agentic_devtools.state.get_state_dir")
    def test_returns_generic_helper_result(self, mock_state_dir, mock_generic, tmp_path):
        """Verify the wrapper returns the bool from the generic helper."""
        mock_state_dir.return_value = tmp_path

        mock_generic.return_value = True
        assert _start_copilot_session_for_create_jira_epic(str(tmp_path)) is True

        mock_generic.return_value = False
        assert _start_copilot_session_for_create_jira_epic(str(tmp_path)) is False

    @patch(
        "agentic_devtools.cli.workflows.worktree_setup._start_copilot_session_for_workflow",
        return_value=True,
    )
    @patch("agentic_devtools.state.get_state_dir")
    def test_interactive_defaults_to_false(self, mock_state_dir, mock_generic, tmp_path):
        """Verify interactive defaults to False when not specified."""
        mock_state_dir.return_value = tmp_path

        _start_copilot_session_for_create_jira_epic(str(tmp_path))

        call_kwargs = mock_generic.call_args[1]
        assert call_kwargs["interactive"] is False
