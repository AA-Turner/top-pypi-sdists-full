"""Tests for drain_commit_rescan."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.github import browser_apply_autofix
from agentic_devtools.cli.github.browser_apply_autofix import drain_commit_rescan


class TestDrainCommitRescan:
    """Tests for drain_commit_rescan (per-suggestion commit loop)."""

    def test_dry_run_counts_without_committing(self) -> None:
        page = object()
        with (
            patch.object(browser_apply_autofix, "count_commit_suggestion_buttons", return_value=2),
            patch.object(browser_apply_autofix, "_commit_last_suggestion") as mock_commit,
            patch.object(browser_apply_autofix, "_wait_for_settle") as mock_settle,
        ):
            result = drain_commit_rescan(page, dry_run=True)
        assert result == {"candidates": 2, "commits": 0, "iterations": 1, "dry_run": True}
        mock_commit.assert_not_called()
        mock_settle.assert_not_called()

    def test_dry_run_with_no_candidates(self) -> None:
        page = object()
        with (
            patch.object(browser_apply_autofix, "count_commit_suggestion_buttons", return_value=0),
            patch.object(browser_apply_autofix, "_commit_last_suggestion"),
            patch.object(browser_apply_autofix, "_wait_for_settle"),
        ):
            result = drain_commit_rescan(page, dry_run=True)
        assert result == {"candidates": 0, "commits": 0, "iterations": 1, "dry_run": True}

    def test_commits_one_per_iteration_until_drained(self) -> None:
        page = object()
        with (
            patch.object(browser_apply_autofix, "count_commit_suggestion_buttons", side_effect=[2, 1, 0]),
            patch.object(browser_apply_autofix, "_commit_last_suggestion") as mock_commit,
            patch.object(browser_apply_autofix, "_wait_for_settle") as mock_settle,
        ):
            result = drain_commit_rescan(page, dry_run=False, message="m")
        assert result == {"candidates": 2, "commits": 2, "iterations": 3, "dry_run": False}
        assert mock_commit.call_count == 2
        mock_commit.assert_called_with(page, "m")
        assert mock_settle.call_count == 2

    def test_respects_max_iterations_cap(self) -> None:
        page = object()
        with (
            patch.object(browser_apply_autofix, "count_commit_suggestion_buttons", return_value=3),
            patch.object(browser_apply_autofix, "_commit_last_suggestion"),
            patch.object(browser_apply_autofix, "_wait_for_settle"),
        ):
            result = drain_commit_rescan(page, dry_run=False, max_iterations=2)
        assert result == {"candidates": 2, "commits": 2, "iterations": 2, "dry_run": False}

    def test_cap_hit_logs_warning_when_suggestions_remain(self) -> None:
        page = object()
        with (
            patch.object(browser_apply_autofix, "count_commit_suggestion_buttons", return_value=3),
            patch.object(browser_apply_autofix, "_commit_last_suggestion"),
            patch.object(browser_apply_autofix, "_wait_for_settle"),
            patch.object(browser_apply_autofix.logger, "warning") as mock_warn,
        ):
            drain_commit_rescan(page, dry_run=False, max_iterations=2)
        mock_warn.assert_called_once()
        assert "max_iterations cap" in mock_warn.call_args[0][0]

    def test_cap_hit_no_warning_when_all_drained_after_last_commit(self) -> None:
        page = object()
        with (
            patch.object(browser_apply_autofix, "count_commit_suggestion_buttons", side_effect=[2, 1, 0]),
            patch.object(browser_apply_autofix, "_commit_last_suggestion"),
            patch.object(browser_apply_autofix, "_wait_for_settle"),
            patch.object(browser_apply_autofix.logger, "warning") as mock_warn,
        ):
            result = drain_commit_rescan(page, dry_run=False, max_iterations=2)
        assert result == {"candidates": 2, "commits": 2, "iterations": 2, "dry_run": False}
        mock_warn.assert_not_called()

    def test_zero_max_iterations(self) -> None:
        page = object()
        with (
            patch.object(browser_apply_autofix, "count_commit_suggestion_buttons") as mock_count,
            patch.object(browser_apply_autofix, "_commit_last_suggestion"),
            patch.object(browser_apply_autofix, "_wait_for_settle"),
        ):
            result = drain_commit_rescan(page, dry_run=False, max_iterations=0)
        assert result == {"candidates": 0, "commits": 0, "iterations": 0, "dry_run": False}
        mock_count.assert_not_called()
