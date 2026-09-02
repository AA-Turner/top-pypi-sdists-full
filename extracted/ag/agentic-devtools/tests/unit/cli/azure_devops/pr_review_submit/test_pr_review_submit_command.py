"""Tests for pr_review_submit_command."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.azure_devops.pr_review_submit import pr_review_submit_command

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_submit"


class TestPrReviewSubmitCommand:
    def test_missing_pr_exits_2(self):
        with (
            patch(f"{_MODULE}.get_pull_request_id", return_value=None),
            patch("sys.argv", ["cmd"]),
            pytest.raises(SystemExit) as exc,
        ):
            pr_review_submit_command()
        assert exc.value.code == 2

    def test_dry_run_runs_inline(self):
        with (
            patch(f"{_MODULE}.set_value") as set_value,
            patch(f"{_MODULE}.pr_review_submit", return_value=0) as worker,
            patch("sys.argv", ["cmd", "--pr", "5", "--dry-run"]),
            pytest.raises(SystemExit) as exc,
        ):
            pr_review_submit_command()
        assert exc.value.code == 0
        worker.assert_called_once_with(pull_request_id=5, dry_run=True)
        # --dry-run must NOT mutate global state (would leave worktree stuck in dry-run mode)
        for call in set_value.call_args_list:
            assert call.args[0] != "dry_run", f"set_value must not be called with 'dry_run'; got {call}"

    def test_inline_runs_worker(self):
        with (
            patch(f"{_MODULE}.set_value"),
            patch(f"{_MODULE}.pr_review_submit", return_value=1) as worker,
            patch("sys.argv", ["cmd", "--pr", "5", "--inline"]),
            pytest.raises(SystemExit) as exc,
        ):
            pr_review_submit_command()
        assert exc.value.code == 1
        worker.assert_called_once_with(pull_request_id=5, dry_run=None)

    def test_default_spawns_background(self):
        task = MagicMock()
        with (
            patch(f"{_MODULE}.set_value"),
            patch(f"{_MODULE}.get_pull_request_id", return_value=5),
            patch(f"{_MODULE}.run_function_in_background", return_value=task) as spawn,
            patch(f"{_MODULE}.print_task_tracking_info") as tracking,
            patch("sys.argv", ["cmd"]),
        ):
            pr_review_submit_command()
        spawn.assert_called_once_with(_MODULE, "pr_review_submit", command_display_name="agdt-pr-review-submit")
        tracking.assert_called_once()
