"""Tests for orchestrate_hierarchy_async."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.orchestrator_commands import orchestrate_hierarchy_async


@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_function_in_background")
def test_orchestrate_hierarchy_async(mock_run):
    orchestrate_hierarchy_async()
    mock_run.assert_called_with(
        "agentic_devtools.cli.workflows.orchestrator_commands",
        "orchestrate_hierarchy_cmd",
        command_display_name="agdt-orchestrate-hierarchy",
    )
