"""Tests for agentic_devtools.cli.issue_template.async_commands.render_issue_async."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools import state
from agentic_devtools.cli.issue_template import async_commands

_ASYNC_MOD = "agentic_devtools.cli.issue_template.async_commands"


class TestRenderIssueAsync:
    """Tests for the render_issue_async and render_issue_async_cli functions."""

    def test_missing_issue_key_exits_nonzero(
        self,
        mock_background_and_state: dict,
    ) -> None:
        """Missing issue_key causes non-zero exit."""
        with (
            patch(f"{_ASYNC_MOD}.get_state_dir", return_value=mock_background_and_state["state_dir"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            async_commands.render_issue_async()
        assert exc_info.value.code == 1

    def test_spawns_background_task(
        self,
        mock_background_and_state: dict,
    ) -> None:
        """Spawns a background task when issue_key is set."""
        state.set_value("issue_key", "TEST-42")
        with patch(f"{_ASYNC_MOD}.get_state_dir", return_value=mock_background_and_state["state_dir"]):
            async_commands.render_issue_async()

        mock_background_and_state["mock_popen"].assert_called_once()

    def test_immediate_stdout_contains_output_path(
        self,
        mock_background_and_state: dict,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Immediate stdout contains output path."""
        state.set_value("issue_key", "TEST-42")
        with patch(f"{_ASYNC_MOD}.get_state_dir", return_value=mock_background_and_state["state_dir"]):
            async_commands.render_issue_async()

        captured = capsys.readouterr()
        assert "issue.md" in captured.out

    def test_template_flag_stored_in_state(
        self,
        mock_background_and_state: dict,
    ) -> None:
        """--template flag value is stored in state."""
        state.set_value("issue_key", "TEST-42")
        with patch(f"{_ASYNC_MOD}.get_state_dir", return_value=mock_background_and_state["state_dir"]):
            async_commands.render_issue_async(template="/path/to/custom.md")

        assert state.get_value("issue_template.template_path") == "/path/to/custom.md"

    def test_template_none_leaves_state_unchanged(
        self,
        mock_background_and_state: dict,
    ) -> None:
        """template=None leaves any existing template path in state unchanged."""
        state.set_value("issue_key", "TEST-42")
        state.set_value("issue_template.template_path", "/old/path.md")

        with patch(f"{_ASYNC_MOD}.get_state_dir", return_value=mock_background_and_state["state_dir"]):
            async_commands.render_issue_async(template=None)

        assert state.get_value("issue_template.template_path") == "/old/path.md"

    def test_jira_issue_key_fallback(
        self,
        mock_background_and_state: dict,
    ) -> None:
        """Falls back to jira.issue_key when issue_key is not set."""
        state.set_value("jira.issue_key", "PROJ-123")
        with patch(f"{_ASYNC_MOD}.get_state_dir", return_value=mock_background_and_state["state_dir"]):
            async_commands.render_issue_async()

        mock_background_and_state["mock_popen"].assert_called_once()


class TestRenderIssueAsyncCli:
    """Tests for the render_issue_async_cli CLI entry point."""

    def test_parses_template_flag(
        self,
        mock_background_and_state: dict,
    ) -> None:
        """--template flag is parsed and forwarded."""
        state.set_value("issue_key", "TEST-42")

        with (
            patch(f"{_ASYNC_MOD}.get_state_dir", return_value=mock_background_and_state["state_dir"]),
            patch("sys.argv", ["agdt-render-issue", "--template", "/my/template.md"]),
        ):
            async_commands.render_issue_async_cli()

        assert state.get_value("issue_template.template_path") == "/my/template.md"

    def test_no_template_flag(
        self,
        mock_background_and_state: dict,
    ) -> None:
        """No --template flag still works."""
        state.set_value("issue_key", "TEST-42")

        with (
            patch(f"{_ASYNC_MOD}.get_state_dir", return_value=mock_background_and_state["state_dir"]),
            patch("sys.argv", ["agdt-render-issue"]),
        ):
            async_commands.render_issue_async_cli()

        mock_background_and_state["mock_popen"].assert_called_once()
