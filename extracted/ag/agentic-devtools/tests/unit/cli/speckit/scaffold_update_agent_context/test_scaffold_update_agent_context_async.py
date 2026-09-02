"""Tests for ``scaffold_update_agent_context_async``."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_update_agent_context import scaffold_update_agent_context_async


class TestScaffoldUpdateAgentContextAsync:
    """scaffold_update_agent_context_async runs scaffold_update_agent_context_command in the background."""

    def test_spawns_background_task(self) -> None:
        mock_task = object()
        with (
            pytest.MonkeyPatch.context() as monkeypatch,
            patch(
                "agentic_devtools.cli.speckit.scaffold_update_agent_context.run_function_in_background",
                return_value=mock_task,
            ) as mock_bg,
            patch("agentic_devtools.cli.speckit.scaffold_update_agent_context.print_task_tracking_info") as mock_print,
        ):
            monkeypatch.setattr("sys.argv", ["agdt-speckit-scaffold-update-agent-context", "copilot"])
            scaffold_update_agent_context_async()

        mock_bg.assert_called_once_with(
            module_path="agentic_devtools.cli.speckit.scaffold_update_agent_context",
            function_name="scaffold_update_agent_context_command",
            command_display_name="agdt-speckit-scaffold-update-agent-context",
            func_kwargs={"argv": ["copilot"]},
        )
        mock_print.assert_called_once_with(mock_task)
