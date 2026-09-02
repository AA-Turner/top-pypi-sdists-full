"""Tests for ``scaffold_tasks_async``."""

from unittest.mock import patch

from agentic_devtools.cli.speckit import scaffold_tasks


def test_scaffold_tasks_async_calls_background() -> None:
    with (
        patch("agentic_devtools.cli.speckit.scaffold_tasks.run_function_in_background") as mock_bg,
        patch("agentic_devtools.cli.speckit.scaffold_tasks.print_task_tracking_info") as mock_print,
    ):
        scaffold_tasks.scaffold_tasks_async(["--json"])
    mock_bg.assert_called_once()
    mock_print.assert_called_once()
