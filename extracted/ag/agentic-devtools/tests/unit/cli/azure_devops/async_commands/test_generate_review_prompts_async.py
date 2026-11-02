"""Tests for generate_review_prompts_async function."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops import async_commands
from agentic_devtools.cli.azure_devops.async_commands import generate_review_prompts_async


class TestGenerateReviewPromptsAsync:
    """Tests for generate_review_prompts_async function."""

    def test_function_exists(self):
        """Verify generate_review_prompts_async is importable and callable."""
        assert callable(generate_review_prompts_async)

    def test_dispatches_to_prompt_workflow_module(self):
        with (
            patch.object(async_commands, "get_value", return_value="123"),
            patch.object(async_commands, "run_function_in_background", return_value="task") as run_background,
            patch.object(async_commands, "print_task_tracking_info"),
        ):
            generate_review_prompts_async()

        run_background.assert_called_once_with(
            "agentic_devtools.cli.azure_devops.review_prompt_workflow",
            "generate_review_prompts_from_state",
            command_display_name="generate-review-prompts",
        )
