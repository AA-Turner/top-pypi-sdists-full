"""Tests for nest_async_command in nest/async_commands.py."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.speckit.nest.async_commands import nest_async_command

_MOD = "agentic_devtools.cli.speckit.nest.async_commands"


class TestNestAsyncCommand:
    """Tests for the nest_async_command CLI entry point."""

    def test_calls_run_function_in_background_with_dry_run(self) -> None:
        """Test that nest_async_command spawns a background task for --dry-run."""
        with (
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch(f"{_MOD}.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-nest", "--dry-run"]),
        ):
            mock_run.return_value = MagicMock(id="test-task-id")
            nest_async_command()

        mock_run.assert_called_once()
        kwargs = mock_run.call_args[1]
        assert kwargs["module_path"] == "agentic_devtools.cli.speckit.nest.commands"
        assert kwargs["function_name"] == "nest_command"
        assert kwargs["func_kwargs"]["dry_run"] is True

    def test_calls_run_function_in_background_with_execute(self) -> None:
        """Test that --execute is forwarded to the background task."""
        with (
            patch(f"{_MOD}.nest_command", return_value="approved-plan-hash") as preview,
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch(f"{_MOD}.print_task_tracking_info"),
            patch("builtins.input", return_value="yes"),
            patch("sys.argv", ["agdt-speckit-nest", "--execute"]),
        ):
            mock_run.return_value = MagicMock(id="test-task-id")
            nest_async_command()

        preview.assert_called_once()
        kwargs = mock_run.call_args[1]
        assert kwargs["func_kwargs"]["execute"] is True
        assert kwargs["func_kwargs"]["dry_run"] is False
        assert kwargs["func_kwargs"]["expected_plan_fingerprint"] == "approved-plan-hash"

    def test_help_mentions_execute_confirmation_gate(self, capsys: pytest.CaptureFixture[str]) -> None:
        """CLI help documents the preview and confirmation requirement for --execute."""
        with patch("sys.argv", ["agdt-speckit-nest", "--help"]):
            with pytest.raises(SystemExit):
                nest_async_command()

        out = capsys.readouterr().out
        assert "require an affirmative prompt" in out
        assert "response, then queue the migration" in out
        assert "asks for confirmation" in out

    def test_cancels_execute_when_confirmation_is_negative(self, capsys: pytest.CaptureFixture[str]) -> None:
        """A non-affirmative answer must not start a migration task."""
        with (
            patch(f"{_MOD}.nest_command"),
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch("builtins.input", return_value="no"),
            patch("sys.argv", ["agdt-speckit-nest", "--execute"]),
        ):
            nest_async_command()

        mock_run.assert_not_called()
        assert "Migration cancelled." in capsys.readouterr().err

    def test_cancels_execute_when_confirmation_is_unavailable(self, capsys: pytest.CaptureFixture[str]) -> None:
        """An unavailable stdin must fail closed without starting a task."""
        with (
            patch(f"{_MOD}.nest_command"),
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch("builtins.input", side_effect=EOFError),
            patch("sys.argv", ["agdt-speckit-nest", "--execute"]),
        ):
            nest_async_command()

        mock_run.assert_not_called()
        assert "confirmation was not available" in capsys.readouterr().err

    def test_preserves_nonzero_exit_when_plan_preview_fails(self) -> None:
        """A failed preview preserves its nonzero exit status."""
        with (
            patch(f"{_MOD}.nest_command", side_effect=SystemExit(1)),
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch("builtins.input") as prompt,
            patch("sys.argv", ["agdt-speckit-nest", "--execute"]),
        ):
            with pytest.raises(SystemExit, match="1"):
                nest_async_command()

        mock_run.assert_not_called()
        prompt.assert_not_called()

    def test_does_not_queue_when_preview_produces_no_plan(self) -> None:
        """A preview with no computed plan must not prompt or queue execution."""
        with (
            patch(f"{_MOD}.nest_command", return_value=None),
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch("builtins.input") as prompt,
            patch("sys.argv", ["agdt-speckit-nest", "--execute"]),
        ):
            nest_async_command()

        mock_run.assert_not_called()
        prompt.assert_not_called()

    def test_zero_exit_preview_does_not_queue_execution(self) -> None:
        """A zero-exit preview stop must return without queueing a task."""
        with (
            patch(f"{_MOD}.nest_command", side_effect=SystemExit(0)),
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch("builtins.input") as prompt,
            patch("sys.argv", ["agdt-speckit-nest", "--execute"]),
        ):
            nest_async_command()

        mock_run.assert_not_called()
        prompt.assert_not_called()

    def test_scope_flag_is_forwarded(self) -> None:
        """Test that --scope passes the integer to func_kwargs as scope."""
        with (
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch(f"{_MOD}.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-nest", "--scope", "42"]),
        ):
            mock_run.return_value = MagicMock(id="t")
            nest_async_command()

        assert mock_run.call_args[1]["func_kwargs"]["scope"] == 42

    def test_issue_alias_takes_precedence_over_scope(self) -> None:
        """Test that --issue wins when both --issue and --scope are provided."""
        with (
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch(f"{_MOD}.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-nest", "--scope", "10", "--issue", "99"]),
        ):
            mock_run.return_value = MagicMock(id="t")
            nest_async_command()

        assert mock_run.call_args[1]["func_kwargs"]["scope"] == 99

    def test_issue_alias_used_without_scope(self) -> None:
        """Test that --issue alone populates scope."""
        with (
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch(f"{_MOD}.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-nest", "--issue", "77"]),
        ):
            mock_run.return_value = MagicMock(id="t")
            nest_async_command()

        assert mock_run.call_args[1]["func_kwargs"]["scope"] == 77

    def test_no_scope_defaults_to_none(self) -> None:
        """Test that omitting both --scope and --issue results in scope=None."""
        with (
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch(f"{_MOD}.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-nest"]),
        ):
            mock_run.return_value = MagicMock(id="t")
            nest_async_command()

        assert mock_run.call_args[1]["func_kwargs"]["scope"] is None

    def test_owner_and_repo_flags_are_forwarded(self) -> None:
        """Test that --owner and --repo are forwarded correctly."""
        with (
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch(f"{_MOD}.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-nest", "--owner", "myorg", "--repo", "myrepo"]),
        ):
            mock_run.return_value = MagicMock(id="t")
            nest_async_command()

        fk = mock_run.call_args[1]["func_kwargs"]
        assert fk["owner"] == "myorg"
        assert fk["repo"] == "myrepo"

    def test_specs_root_flag_is_forwarded(self) -> None:
        """Test that --specs-root is forwarded to the background task."""
        with (
            patch(f"{_MOD}.run_function_in_background") as mock_run,
            patch(f"{_MOD}.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-nest", "--specs-root", "/some/path"]),
        ):
            mock_run.return_value = MagicMock(id="t")
            nest_async_command()

        assert mock_run.call_args[1]["func_kwargs"]["specs_root"] == "/some/path"

    def test_invalid_scope_exits(self) -> None:
        """Test that a non-integer --scope value causes argparse to exit."""
        with (
            patch(f"{_MOD}.run_function_in_background"),
            patch(f"{_MOD}.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-nest", "--scope", "abc"]),
        ):
            with pytest.raises(SystemExit):
                nest_async_command()

    def test_zero_scope_exits(self) -> None:
        """Test that --scope 0 causes argparse to exit."""
        with (
            patch(f"{_MOD}.run_function_in_background"),
            patch(f"{_MOD}.print_task_tracking_info"),
            patch("sys.argv", ["agdt-speckit-nest", "--scope", "0"]),
        ):
            with pytest.raises(SystemExit):
                nest_async_command()

    def test_print_task_tracking_info_called(self) -> None:
        """Test that print_task_tracking_info is called with the task object."""
        fake_task = MagicMock(id="task-xyz")
        with (
            patch(f"{_MOD}.run_function_in_background", return_value=fake_task),
            patch(f"{_MOD}.print_task_tracking_info") as mock_print,
            patch("sys.argv", ["agdt-speckit-nest"]),
        ):
            nest_async_command()

        mock_print.assert_called_once_with(fake_task)
