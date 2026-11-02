"""Tests for audit_trio_async."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.orchestrator_commands import audit_trio_async


@patch("agentic_devtools.cli.workflows.orchestrator_commands.run_function_in_background")
def test_audit_trio_async(mock_run):
    audit_trio_async()
    mock_run.assert_called_with(
        "agentic_devtools.cli.workflows.orchestrator_commands",
        "audit_trio_cmd",
        command_display_name="agdt-audit-trio",
    )
