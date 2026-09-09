"""Tests for _run_redispatch_stop_conditions()."""

import json
from datetime import UTC, datetime
from unittest.mock import patch

from agentic_devtools.cli.ci.retry import RetryableError
from agentic_devtools.cli.ci.watchdog_command import _run_redispatch_stop_conditions


class TestRunRedispatchStopConditions:
    """Stop-condition evaluation delegated from ai-pr-loop-redispatch.yml."""

    def test_enables_dispatch_when_conditions_pass(self, capsys) -> None:
        now = datetime(2026, 9, 2, 12, 0, 0, tzinfo=UTC)
        with (
            patch("agentic_devtools.cli.ci.watchdog_command._select_pr_read_token", return_value="token"),
            patch("agentic_devtools.cli.ci.watchdog_command._eligible_open_pr_count", return_value=3),
            patch("agentic_devtools.cli.ci.watchdog_command._latest_merged_at", return_value="2026-09-02T10:00:00Z"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._write_github_output") as write_output,
        ):
            _run_redispatch_stop_conditions("o/r", "main")

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is True
        assert payload["eligible_open_pr_count"] == 3
        write_output.assert_called_once_with({"should_dispatch": True})

    def test_disables_dispatch_when_no_eligible_open_prs(self, capsys) -> None:
        with (
            patch("agentic_devtools.cli.ci.watchdog_command._select_pr_read_token", return_value="token"),
            patch("agentic_devtools.cli.ci.watchdog_command._eligible_open_pr_count", return_value=0),
            patch("agentic_devtools.cli.ci.watchdog_command._write_github_output") as write_output,
        ):
            _run_redispatch_stop_conditions("o/r", "main")

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is False
        write_output.assert_called_once_with({"should_dispatch": False})

    def test_fails_closed_when_token_selection_fails(self, capsys) -> None:
        with (
            patch(
                "agentic_devtools.cli.ci.watchdog_command._select_pr_read_token",
                side_effect=RuntimeError("No credential can read repository pull requests."),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._write_github_output") as write_output,
        ):
            _run_redispatch_stop_conditions("o/r", "main")

        output_lines = capsys.readouterr().out.splitlines()
        assert output_lines[0].startswith("::error::")
        payload = json.loads(output_lines[-1])
        assert payload["should_dispatch"] is False
        write_output.assert_called_once_with({"should_dispatch": False})

    def test_fails_closed_when_inventory_retryable_error_occurs(self, capsys) -> None:
        with (
            patch(
                "agentic_devtools.cli.ci.watchdog_command._eligible_open_pr_count",
                side_effect=RetryableError("HTTP 503"),
            ),
            patch("agentic_devtools.cli.ci.watchdog_command._select_pr_read_token", return_value="token"),
            patch("agentic_devtools.cli.ci.watchdog_command._write_github_output") as write_output,
        ):
            _run_redispatch_stop_conditions("o/r", "main")

        output_lines = capsys.readouterr().out.splitlines()
        assert output_lines[0].startswith("::error::")
        payload = json.loads(output_lines[-1])
        assert payload["should_dispatch"] is False
        write_output.assert_called_once_with({"should_dispatch": False})

    def test_disables_dispatch_when_latest_merge_is_unavailable(self, capsys) -> None:
        with (
            patch("agentic_devtools.cli.ci.watchdog_command._select_pr_read_token", return_value="token"),
            patch("agentic_devtools.cli.ci.watchdog_command._eligible_open_pr_count", return_value=2),
            patch("agentic_devtools.cli.ci.watchdog_command._latest_merged_at", return_value=None),
            patch("agentic_devtools.cli.ci.watchdog_command._write_github_output") as write_output,
        ):
            _run_redispatch_stop_conditions("o/r", "main")

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is False
        write_output.assert_called_once_with({"should_dispatch": False})

    def test_disables_dispatch_for_stale_main(self, capsys) -> None:
        now = datetime(2026, 9, 3, 12, 0, 0, tzinfo=UTC)
        with (
            patch("agentic_devtools.cli.ci.watchdog_command._select_pr_read_token", return_value="token"),
            patch("agentic_devtools.cli.ci.watchdog_command._eligible_open_pr_count", return_value=2),
            patch("agentic_devtools.cli.ci.watchdog_command._latest_merged_at", return_value="2026-09-01T00:00:00Z"),
            patch("agentic_devtools.cli.ci.watchdog_command._utc_now", return_value=now),
            patch("agentic_devtools.cli.ci.watchdog_command._write_github_output") as write_output,
        ):
            _run_redispatch_stop_conditions("o/r", "main")

        payload = json.loads(capsys.readouterr().out.splitlines()[-1])
        assert payload["should_dispatch"] is False
        write_output.assert_called_once_with({"should_dispatch": False})

    def test_fails_closed_when_merged_timestamp_is_invalid(self, capsys) -> None:
        with (
            patch("agentic_devtools.cli.ci.watchdog_command._select_pr_read_token", return_value="token"),
            patch("agentic_devtools.cli.ci.watchdog_command._eligible_open_pr_count", return_value=2),
            patch("agentic_devtools.cli.ci.watchdog_command._latest_merged_at", return_value="bad"),
            patch("agentic_devtools.cli.ci.watchdog_command._write_github_output") as write_output,
        ):
            _run_redispatch_stop_conditions("o/r", "main")

        output_lines = capsys.readouterr().out.splitlines()
        assert output_lines[0].startswith("::error::Merged pull-request inventory returned an invalid merge date")
        payload = json.loads(output_lines[-1])
        assert payload["should_dispatch"] is False
        write_output.assert_called_once_with({"should_dispatch": False})
