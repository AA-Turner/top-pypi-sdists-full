"""Tests for the create_epic_async routed CLI entry point (issue #2117)."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli import jira
from agentic_devtools.cli.jira.async_commands import create_epic_async


class TestCreateEpicAsync:
    """create_epic_async delegates to the create_epic_router routing layer."""

    def test_delegates_to_router(self):
        with patch("agentic_devtools.cli.jira.create_epic_router.route_create_epic") as route:
            create_epic_async()
        route.assert_called_once_with()

    def test_no_file_no_state_is_missing_input(self, temp_state_dir, clear_state_before, capsys):
        # With no positional file and no legacy state, routing rejects with exit 2.
        with patch("sys.argv", ["agdt-create-epic"]):
            with pytest.raises(SystemExit) as exc:
                create_epic_async()
        assert exc.value.code == 2
        assert "create_epic.validation_error" in capsys.readouterr().err

    def test_legacy_state_spawns_background_task(self, temp_state_dir, clear_state_before):
        jira.set_jira_value("project_key", "PROJECT")
        jira.set_jira_value("summary", "Epic")
        jira.set_jira_value("epic_name", "Name")
        with (
            patch("sys.argv", ["agdt-create-epic"]),
            patch("agentic_devtools.cli.jira.create_epic_router.run_function_in_background") as spawn,
            patch("agentic_devtools.cli.jira.create_epic_router.print_task_tracking_info"),
        ):
            create_epic_async()
        assert spawn.call_args[0][1] == "run_legacy_mode"
