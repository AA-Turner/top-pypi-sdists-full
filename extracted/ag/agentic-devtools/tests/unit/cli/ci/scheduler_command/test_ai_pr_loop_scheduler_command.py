"""Tests for ai_pr_loop_scheduler_command CLI entry point."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.scheduler import SchedulerResult


class TestAiPrLoopSchedulerCommand:
    """Tests for the scheduler CLI entry point."""

    @patch.dict("os.environ", {"DRY_RUN": "", "GITHUB_STEP_SUMMARY": ""}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler_command.shutil.which", return_value="/usr/bin/gh")
    @patch("agentic_devtools.cli.ci.scheduler_command.GitHubActionsProvider")
    @patch("agentic_devtools.cli.ci.scheduler_command.run_scheduler")
    def test_outputs_json_schema(self, mock_run, mock_provider_cls, mock_which, capsys) -> None:
        from agentic_devtools.cli.ci.scheduler_command import ai_pr_loop_scheduler_command

        mock_run.return_value = SchedulerResult(
            run_mode="live",
            batch_size=1,
            pool_size=1,
            eligible_count=5,
            dispatched_count=1,
            dispatched_prs=[2020],
            cursor_before=2019,
            cursor_after=2020,
            cursor_persisted=True,
        )

        ai_pr_loop_scheduler_command()

        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["run_mode"] == "live"
        assert output["batch_size"] == 1
        assert output["pool_size"] == 1
        assert output["eligible_count"] == 5
        assert output["dispatched_count"] == 1
        assert output["dispatched_prs"] == [2020]
        assert output["cursor_before"] == 2019
        assert output["cursor_after"] == 2020
        assert output["cursor_persisted"] is True
        assert output["had_dispatch_error"] is False

    @patch("agentic_devtools.cli.ci.scheduler_command.shutil.which", return_value=None)
    def test_exits_10_when_gh_missing(self, mock_which) -> None:
        from agentic_devtools.cli.ci.scheduler_command import ai_pr_loop_scheduler_command

        with pytest.raises(SystemExit) as exc_info:
            ai_pr_loop_scheduler_command()
        assert exc_info.value.code == 10

    @patch.dict("os.environ", {"DRY_RUN": "true", "GITHUB_STEP_SUMMARY": ""}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler_command.shutil.which", return_value="/usr/bin/gh")
    @patch("agentic_devtools.cli.ci.scheduler_command.GitHubActionsProvider")
    @patch("agentic_devtools.cli.ci.scheduler_command.run_scheduler")
    def test_dry_run_from_env(self, mock_run, mock_provider_cls, mock_which, capsys) -> None:
        from agentic_devtools.cli.ci.scheduler_command import ai_pr_loop_scheduler_command

        mock_run.return_value = SchedulerResult(
            run_mode="dry_run",
            batch_size=1,
            pool_size=1,
            eligible_count=3,
            dispatched_count=2,
            dispatched_prs=[2020, 2021],
            cursor_before=None,
            cursor_after=2021,
            cursor_persisted=False,
        )

        ai_pr_loop_scheduler_command()

        mock_run.assert_called_once()
        _, kwargs = mock_run.call_args
        assert kwargs["dry_run"] is True

    @patch.dict("os.environ", {"DRY_RUN": "", "GITHUB_STEP_SUMMARY": ""}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler_command.shutil.which", return_value="/usr/bin/gh")
    @patch("agentic_devtools.cli.ci.scheduler_command.GitHubActionsProvider")
    @patch("agentic_devtools.cli.ci.scheduler_command.run_scheduler")
    def test_step_summary_skipped_when_empty_path(self, mock_run, mock_provider_cls, mock_which, capsys) -> None:
        from agentic_devtools.cli.ci.scheduler_command import ai_pr_loop_scheduler_command

        mock_run.return_value = SchedulerResult(
            run_mode="live",
            batch_size=1,
            pool_size=1,
            eligible_count=0,
            dispatched_count=0,
            dispatched_prs=[],
            cursor_before=None,
            cursor_after=None,
            cursor_persisted=False,
        )

        # Should not raise even with empty GITHUB_STEP_SUMMARY
        ai_pr_loop_scheduler_command()

    @patch.dict("os.environ", {"DRY_RUN": ""}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler_command.shutil.which", return_value="/usr/bin/gh")
    @patch("agentic_devtools.cli.ci.scheduler_command.GitHubActionsProvider")
    @patch("agentic_devtools.cli.ci.scheduler_command.run_scheduler")
    def test_step_summary_written_when_path_set(self, mock_run, mock_provider_cls, mock_which, tmp_path) -> None:
        from agentic_devtools.cli.ci.scheduler_command import ai_pr_loop_scheduler_command

        summary_file = tmp_path / "summary.md"
        summary_file.write_text("")

        mock_run.return_value = SchedulerResult(
            run_mode="live",
            batch_size=2,
            pool_size=1,
            eligible_count=5,
            dispatched_count=2,
            dispatched_prs=[2020, 2021],
            cursor_before=2019,
            cursor_after=2021,
            cursor_persisted=True,
        )

        with patch.dict("os.environ", {"GITHUB_STEP_SUMMARY": str(summary_file)}):
            ai_pr_loop_scheduler_command()

        content = summary_file.read_text()
        assert "Round-Robin Scheduler" in content
        assert "| Dispatched | 2 |" in content
        assert "| Mode | live |" in content
        assert "#2020" in content
        assert "#2021" in content
        assert "| Eligible (fetched) | 5 |" in content

    @patch.dict("os.environ", {"DRY_RUN": ""}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler_command.shutil.which", return_value="/usr/bin/gh")
    @patch("agentic_devtools.cli.ci.scheduler_command.GitHubActionsProvider")
    @patch("agentic_devtools.cli.ci.scheduler_command.run_scheduler")
    def test_step_summary_uses_would_dispatch_in_dry_run(
        self, mock_run, mock_provider_cls, mock_which, tmp_path
    ) -> None:
        from agentic_devtools.cli.ci.scheduler_command import ai_pr_loop_scheduler_command

        summary_file = tmp_path / "summary.md"
        summary_file.write_text("")

        mock_run.return_value = SchedulerResult(
            run_mode="dry_run",
            batch_size=2,
            pool_size=5,
            eligible_count=5,
            dispatched_count=2,
            dispatched_prs=[2020, 2021],
            cursor_before=2019,
            cursor_after=2021,
            cursor_persisted=False,
        )

        with patch.dict("os.environ", {"GITHUB_STEP_SUMMARY": str(summary_file)}):
            ai_pr_loop_scheduler_command()

        content = summary_file.read_text()
        assert "| Would Dispatch | 2 |" in content

    @patch.dict("os.environ", {"DRY_RUN": "", "GITHUB_STEP_SUMMARY": ""}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler_command.shutil.which", return_value="/usr/bin/gh")
    @patch("agentic_devtools.cli.ci.scheduler_command.GitHubActionsProvider")
    @patch("agentic_devtools.cli.ci.scheduler_command.run_scheduler")
    @patch("agentic_devtools.cli.ci.scheduler_command.logger")
    def test_exits_1_on_scheduler_error(self, mock_logger, mock_run, mock_provider_cls, mock_which) -> None:
        from agentic_devtools.cli.ci.scheduler_command import ai_pr_loop_scheduler_command

        mock_run.side_effect = RuntimeError("Fatal error")

        with pytest.raises(SystemExit) as exc_info:
            ai_pr_loop_scheduler_command()
        assert exc_info.value.code == 1
        mock_logger.exception.assert_called_once_with("Scheduler failed: %s", mock_run.side_effect)

    @patch.dict("os.environ", {"DRY_RUN": ""}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler_command.shutil.which", return_value="/usr/bin/gh")
    @patch("agentic_devtools.cli.ci.scheduler_command.GitHubActionsProvider")
    @patch("agentic_devtools.cli.ci.scheduler_command.run_scheduler")
    def test_step_summary_oserror_is_non_fatal(self, mock_run, mock_provider_cls, mock_which, tmp_path, capsys) -> None:
        from agentic_devtools.cli.ci.scheduler_command import ai_pr_loop_scheduler_command

        mock_run.return_value = SchedulerResult(
            run_mode="live",
            batch_size=1,
            pool_size=1,
            eligible_count=1,
            dispatched_count=1,
            dispatched_prs=[2020],
            cursor_before=None,
            cursor_after=2020,
            cursor_persisted=False,
        )

        # Point to a directory (not a file) to trigger OSError on open()
        bad_path = str(tmp_path / "nonexistent_dir" / "summary.md")

        with patch.dict("os.environ", {"GITHUB_STEP_SUMMARY": bad_path}):
            ai_pr_loop_scheduler_command()

        # Should still produce JSON output despite OSError
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["dispatched_count"] == 1

    @patch.dict("os.environ", {"DRY_RUN": "", "GITHUB_STEP_SUMMARY": ""}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler_command.shutil.which", return_value="/usr/bin/gh")
    @patch("agentic_devtools.cli.ci.scheduler_command.GitHubActionsProvider")
    @patch("agentic_devtools.cli.ci.scheduler_command.run_scheduler")
    @patch("agentic_devtools.cli.ci.scheduler_command.json.dumps", side_effect=TypeError("not serializable"))
    def test_json_serialization_error_is_logged(
        self, mock_dumps, mock_run, mock_provider_cls, mock_which, caplog
    ) -> None:
        from agentic_devtools.cli.ci.scheduler_command import ai_pr_loop_scheduler_command

        mock_run.return_value = SchedulerResult(
            run_mode="live",
            batch_size=1,
            pool_size=1,
            eligible_count=0,
            dispatched_count=0,
            dispatched_prs=[],
            cursor_before=None,
            cursor_after=None,
            cursor_persisted=False,
        )

        with caplog.at_level("ERROR"):
            ai_pr_loop_scheduler_command()

        assert "Failed to serialize scheduler output" in caplog.text

    @patch.dict("os.environ", {"DRY_RUN": "", "GITHUB_STEP_SUMMARY": ""}, clear=False)
    @patch("agentic_devtools.cli.ci.scheduler_command.shutil.which", return_value="/usr/bin/gh")
    @patch("agentic_devtools.cli.ci.scheduler_command.GitHubActionsProvider")
    @patch("agentic_devtools.cli.ci.scheduler_command.run_scheduler")
    def test_exits_1_when_had_dispatch_error(self, mock_run, mock_provider_cls, mock_which, capsys, caplog) -> None:
        from agentic_devtools.cli.ci.scheduler_command import ai_pr_loop_scheduler_command

        mock_run.return_value = SchedulerResult(
            run_mode="live",
            batch_size=2,
            pool_size=1,
            eligible_count=2,
            dispatched_count=1,
            dispatched_prs=[2020],
            cursor_before=None,
            cursor_after=2020,
            cursor_persisted=False,
            had_dispatch_error=True,
        )

        with caplog.at_level("ERROR"):
            with pytest.raises(SystemExit) as exc_info:
                ai_pr_loop_scheduler_command()

        assert exc_info.value.code == 1
        # JSON output should still be written before exit
        captured = capsys.readouterr()
        output = json.loads(captured.out)
        assert output["had_dispatch_error"] is True
        # Error message should be logged
        assert "One or more dispatch attempts failed" in caplog.text
