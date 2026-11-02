"""Tests for orchestrate_finalize_async."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.orchestrator_commands import orchestrate_finalize_async


@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_function_in_background")
def test_orchestrate_finalize_async(mock_run):
    orchestrate_finalize_async()
    mock_run.assert_called_with(
        "agentic_devtools.cli.workflows.orchestrator_commands",
        "orchestrate_finalize_cmd",
        command_display_name="agdt-orchestrate-finalize",
    )
