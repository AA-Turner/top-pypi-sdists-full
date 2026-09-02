"""Tests for orchestrate_step_async."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.orchestrator_commands import orchestrate_step_async


@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_function_in_background")
def test_orchestrate_step_async(mock_run):
    orchestrate_step_async()
    mock_run.assert_called_with(
        "agentic_devtools.cli.workflows.orchestrator_commands",
        "orchestrate_step_cmd",
        command_display_name="agdt-orchestrate-step",
    )
