"""Tests for refresh_comment_command."""

from contextlib import contextmanager
from unittest.mock import patch

import pytest

from agentic_devtools.cli.azure_devops.pr_review_refresh import refresh_comment_command
from agentic_devtools.file_locking import FileLockError

_M = "agentic_devtools.cli.azure_devops.pr_review_refresh"

_RESULT = {"refreshed": True, "reason": "updated", "approved": 1, "needsWork": 2, "reviewed": 3}
_SKIP = {"refreshed": False, "reason": "throttled", "approved": 0, "needsWork": 0, "reviewed": 0}


@contextmanager
def _noop_lock(pull_request_id, *args, **kwargs):
    yield object()


@contextmanager
def _raising_lock(pull_request_id, *args, **kwargs):
    raise FileLockError("held")
    yield  # pragma: no cover


class TestRefreshCommentCommand:
    def test_missing_pr_exits_2(self):
        with (
            patch(f"{_M}.get_pull_request_id", return_value=None),
            patch("sys.argv", ["cmd"]),
            pytest.raises(SystemExit) as exc,
        ):
            refresh_comment_command()
        assert exc.value.code == 2

    def test_refreshed_prints_summary(self, capsys):
        with (
            patch(f"{_M}.is_dry_run", return_value=False),
            patch(f"{_M}.pipeline_lock", new=_noop_lock),
            patch(f"{_M}.refresh_core", return_value=_RESULT) as core,
            patch("sys.argv", ["cmd", "--pr", "5"]),
        ):
            refresh_comment_command()
        out = capsys.readouterr().out
        assert "refreshed" in out
        assert "3 reviewed" in out
        assert core.call_args.kwargs["dry_run"] is False

    def test_skipped_prints_reason(self, capsys):
        with (
            patch(f"{_M}.is_dry_run", return_value=False),
            patch(f"{_M}.pipeline_lock", new=_noop_lock),
            patch(f"{_M}.refresh_core", return_value=_SKIP),
            patch("sys.argv", ["cmd", "--pr", "5"]),
        ):
            refresh_comment_command()
        assert "skipped (throttled)" in capsys.readouterr().out

    def test_dry_run_flag_passes_through(self):
        with (
            patch(f"{_M}.pipeline_lock", new=_noop_lock),
            patch(f"{_M}.refresh_core", return_value=_RESULT) as core,
            patch("sys.argv", ["cmd", "--pr", "5", "--dry-run"]),
        ):
            refresh_comment_command()
        assert core.call_args.kwargs["dry_run"] is True

    def test_lock_contention_exits_1(self):
        with (
            patch(f"{_M}.is_dry_run", return_value=False),
            patch(f"{_M}.pipeline_lock", new=_raising_lock),
            patch("sys.argv", ["cmd", "--pr", "5"]),
            pytest.raises(SystemExit) as exc,
        ):
            refresh_comment_command()
        assert exc.value.code == 1

    def test_every_n_zero_exits_2(self):
        with (
            patch("sys.argv", ["cmd", "--pr", "5", "--every-n", "0"]),
            pytest.raises(SystemExit) as exc,
        ):
            refresh_comment_command()
        assert exc.value.code == 2

    def test_every_n_negative_exits_2(self):
        with (
            patch("sys.argv", ["cmd", "--pr", "5", "--every-n", "-1"]),
            pytest.raises(SystemExit) as exc,
        ):
            refresh_comment_command()
        assert exc.value.code == 2

    def test_min_interval_negative_exits_2(self):
        with (
            patch("sys.argv", ["cmd", "--pr", "5", "--min-interval", "-1"]),
            pytest.raises(SystemExit) as exc,
        ):
            refresh_comment_command()
        assert exc.value.code == 2
