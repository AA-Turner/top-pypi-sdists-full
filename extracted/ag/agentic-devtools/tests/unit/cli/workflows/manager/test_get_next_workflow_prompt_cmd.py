"""Tests for get_next_workflow_prompt_cmd function."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.workflows.manager import (
    PromptStatus,
    get_next_workflow_prompt_cmd,
)


class TestGetNextWorkflowPromptCmd:
    """Tests for get_next_workflow_prompt_cmd function."""

    def test_prints_status_header(self, capsys):
        """Should print the WORKFLOW PROMPT STATUS header to stdout."""
        mock_result = MagicMock()
        mock_result.status = PromptStatus.NO_WORKFLOW
        mock_result.step = None
        mock_result.content = "No workflow is active."

        with patch(
            "agentic_devtools.cli.workflows.manager.get_next_workflow_prompt",
            return_value=mock_result,
        ):
            get_next_workflow_prompt_cmd()

        captured = capsys.readouterr()
        assert "WORKFLOW PROMPT STATUS" in captured.out

    def test_prints_prompt_content(self, capsys):
        """Should print the content from the prompt result."""
        mock_result = MagicMock()
        mock_result.status = PromptStatus.NO_WORKFLOW
        mock_result.step = None
        mock_result.content = "Unique-prompt-content-for-test"

        with patch(
            "agentic_devtools.cli.workflows.manager.get_next_workflow_prompt",
            return_value=mock_result,
        ):
            get_next_workflow_prompt_cmd()

        captured = capsys.readouterr()
        assert "Unique-prompt-content-for-test" in captured.out

    def test_calls_get_next_workflow_prompt(self):
        """Should call get_next_workflow_prompt exactly once."""
        mock_result = MagicMock()
        mock_result.status = PromptStatus.NO_WORKFLOW
        mock_result.step = None
        mock_result.content = "No workflow."

        with patch(
            "agentic_devtools.cli.workflows.manager.get_next_workflow_prompt",
            return_value=mock_result,
        ) as mock_fn:
            get_next_workflow_prompt_cmd()

        mock_fn.assert_called_once()

    def test_success_with_step_prints_save_notice(self, tmp_path, capsys):
        """SUCCESS result with a step prints the temp prompt save notice."""
        mock_result = MagicMock()
        mock_result.status = PromptStatus.SUCCESS
        mock_result.step = "delegate"
        mock_result.content = "delegate body"

        with (
            patch(
                "agentic_devtools.cli.workflows.manager.get_next_workflow_prompt",
                return_value=mock_result,
            ),
            patch(
                "agentic_devtools.cli.workflows.manager.get_workflow_state",
                return_value={"active": "pull-request-review", "step": "delegate"},
            ),
            patch(
                "agentic_devtools.cli.workflows.manager.get_temp_output_dir",
                return_value=tmp_path,
            ),
        ):
            get_next_workflow_prompt_cmd()

        captured = capsys.readouterr()
        assert "temp-pull-request-review-delegate-prompt.md" in captured.out
