"""Tests for retro_spec async_commands module."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.retro_spec.async_commands import retro_spec_async_command


class TestRetroSpecAsyncCommand:
    """Tests for the retro_spec_async_command CLI entry point."""

    def test_calls_run_function_in_background(self) -> None:
        """Test that retro_spec_async_command spawns a background task."""
        with (
            patch("agentic_devtools.cli.speckit.retro_spec.async_commands.run_function_in_background") as mock_run,
            patch("agentic_devtools.cli.speckit.retro_spec.async_commands.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-retro-spec", "--issue", "142", "--dry-run"]),
        ):
            mock_run.return_value.id = "test-task-id"
            retro_spec_async_command()

        mock_run.assert_called_once()
        kwargs = mock_run.call_args[1]
        assert kwargs["module_path"] == "agentic_devtools.cli.speckit.retro_spec.commands"
        assert kwargs["function_name"] == "retro_spec_command"
        assert kwargs["func_kwargs"]["issue_number"] == 142
        assert kwargs["func_kwargs"]["dry_run"] is True

    def test_help_describes_dry_run_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that --dry-run help text matches current behavior."""
        with patch("sys.argv", ["agdt-speckit-retro-spec", "--help"]):
            with pytest.raises(SystemExit):
                retro_spec_async_command()

        help_text = capsys.readouterr().out
        assert "Print the generated spec without writing files or creating" in help_text
        assert "commits." in help_text

    @pytest.mark.parametrize("issue", ["0", "-1"])
    def test_rejects_non_positive_issue_number(self, issue: str) -> None:
        """Zero and negative issue numbers fail before task creation."""
        with (
            patch("agentic_devtools.cli.speckit.retro_spec.async_commands.run_function_in_background"),
            patch("agentic_devtools.cli.speckit.retro_spec.async_commands.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-retro-spec", "--issue", issue]),
        ):
            with pytest.raises(SystemExit):
                retro_spec_async_command()
