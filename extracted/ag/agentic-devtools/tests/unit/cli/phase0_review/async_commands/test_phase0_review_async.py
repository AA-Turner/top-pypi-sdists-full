"""Tests for async_commands.phase0_review_async."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.phase0_review.async_commands import phase0_review_async


def test_phase0_review_async_spawns_and_prints_tracking():
    task = MagicMock()
    with (
        patch(
            "agentic_devtools.cli.phase0_review.async_commands.run_function_in_background",
            return_value=task,
        ) as run,
        patch("agentic_devtools.cli.phase0_review.async_commands.print_task_tracking_info") as tracking,
    ):
        phase0_review_async()
    run.assert_called_once_with(
        module_path="agentic_devtools.cli.phase0_review.commands",
        function_name="phase0_review_command",
        command_display_name="agdt-phase0-review",
    )
    tracking.assert_called_once_with(task, "Reviewing Phase 0 issue.md")
