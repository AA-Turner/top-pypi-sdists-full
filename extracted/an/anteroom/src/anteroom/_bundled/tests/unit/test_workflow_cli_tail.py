"""Tests for workflow tail, worktree, and delta CLI handlers (#1236)."""

from __future__ import annotations

import argparse
from pathlib import Path
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# _handle_tail
# ---------------------------------------------------------------------------


class TestHandleTail:
    def test_displays_events(self) -> None:
        from anteroom.cli.workflow_cli import _handle_tail

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123", step_id=None, last=20, stderr=False, stdout=False)

        run = {"id": "abc12345-full-uuid", "status": "running", "inputs": None}
        events = [
            {"event_type": "transcript_stdout", "payload": {"content": "hello"}, "id": 1},
            {"event_type": "transcript_stderr", "payload": {"content": "oops"}, "id": 2},
        ]

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345-full-uuid"),
            patch("anteroom.cli.workflow_cli.console") as mock_console,
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_storage.list_transcript_events", return_value=events),
        ):
            _handle_tail(mock_db, args)
        assert mock_console.print.call_count >= 1

    def test_no_events_message(self) -> None:
        from anteroom.cli.workflow_cli import _handle_tail

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123", step_id=None, last=20, stderr=False, stdout=False)

        run = {"id": "abc12345-full-uuid", "status": "running", "inputs": None}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345-full-uuid"),
            patch("anteroom.cli.workflow_cli.console") as mock_console,
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_storage.list_transcript_events", return_value=[]),
        ):
            _handle_tail(mock_db, args)
        output = " ".join(str(c) for c in mock_console.print.call_args_list)
        assert "No transcript events" in output

    def test_stderr_flag_filters(self) -> None:
        from anteroom.cli.workflow_cli import _handle_tail

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123", step_id=None, last=20, stderr=True, stdout=False)

        run = {"id": "abc12345-full-uuid", "status": "running", "inputs": None}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345-full-uuid"),
            patch("anteroom.cli.workflow_cli.console"),
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_storage.list_transcript_events", return_value=[]) as mock_list,
        ):
            _handle_tail(mock_db, args)
        _, kwargs = mock_list.call_args
        assert kwargs.get("event_types") == ["transcript_stderr"]

    def test_stdout_flag_filters(self) -> None:
        from anteroom.cli.workflow_cli import _handle_tail

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123", step_id=None, last=20, stderr=False, stdout=True)

        run = {"id": "abc12345-full-uuid", "status": "running", "inputs": None}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345-full-uuid"),
            patch("anteroom.cli.workflow_cli.console"),
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_storage.list_transcript_events", return_value=[]) as mock_list,
        ):
            _handle_tail(mock_db, args)
        _, kwargs = mock_list.call_args
        assert kwargs.get("event_types") == ["transcript_stdout"]

    def test_no_filter_shows_all(self) -> None:
        from anteroom.cli.workflow_cli import _handle_tail

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123", step_id=None, last=20, stderr=False, stdout=False)

        run = {"id": "abc12345-full-uuid", "status": "running", "inputs": None}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345-full-uuid"),
            patch("anteroom.cli.workflow_cli.console"),
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_storage.list_transcript_events", return_value=[]) as mock_list,
        ):
            _handle_tail(mock_db, args)
        _, kwargs = mock_list.call_args
        assert kwargs.get("event_types") is None


# ---------------------------------------------------------------------------
# _has_unmerged_entries
# ---------------------------------------------------------------------------


class TestHasUnmergedEntries:
    def test_clean(self) -> None:
        from anteroom.cli.workflow_cli import _has_unmerged_entries

        assert _has_unmerged_entries("") is False

    def test_dirty_no_conflicts(self) -> None:
        from anteroom.cli.workflow_cli import _has_unmerged_entries

        assert _has_unmerged_entries("M  src/file.py\n?? new.txt") is False

    def test_uu_conflict(self) -> None:
        from anteroom.cli.workflow_cli import _has_unmerged_entries

        assert _has_unmerged_entries("UU src/file.py") is True

    def test_aa_conflict(self) -> None:
        from anteroom.cli.workflow_cli import _has_unmerged_entries

        assert _has_unmerged_entries("AA src/file.py") is True

    def test_dd_conflict(self) -> None:
        from anteroom.cli.workflow_cli import _has_unmerged_entries

        assert _has_unmerged_entries("DD src/file.py") is True

    def test_mixed_with_conflict(self) -> None:
        from anteroom.cli.workflow_cli import _has_unmerged_entries

        assert _has_unmerged_entries("M  src/a.py\nDU src/b.py\n?? c.txt") is True

    def test_au_ua_du_ud(self) -> None:
        from anteroom.cli.workflow_cli import _has_unmerged_entries

        for code in ("AU", "UA", "DU", "UD"):
            assert _has_unmerged_entries(f"{code} file.py") is True


# ---------------------------------------------------------------------------
# _handle_worktree
# ---------------------------------------------------------------------------


class TestHandleWorktree:
    def test_no_issue_number(self) -> None:
        from anteroom.cli.workflow_cli import _handle_worktree

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123")
        run = {"id": "abc12345", "status": "running", "inputs": {}}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345"),
            patch("anteroom.cli.workflow_cli.console") as mock_console,
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
        ):
            _handle_worktree(mock_db, args)
        output = " ".join(str(c) for c in mock_console.print.call_args_list)
        assert "issue_number" in output

    def test_no_state_found(self) -> None:
        from anteroom.cli.workflow_cli import _handle_worktree

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123")
        run = {"id": "abc12345", "status": "running", "inputs": {"issue_number": 42}}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345"),
            patch("anteroom.cli.workflow_cli.console") as mock_console,
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_state.read_issue_state", return_value=None),
        ):
            _handle_worktree(mock_db, args)
        output = " ".join(str(c) for c in mock_console.print.call_args_list)
        assert "No issue state" in output

    def test_conflicted_worktree(self, tmp_path: Path) -> None:
        from anteroom.cli.workflow_cli import _handle_worktree

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123")
        run = {"id": "abc12345", "status": "running", "inputs": {"issue_number": 42}}
        state = {"worktree_path": str(tmp_path), "branch": "issue-42-fix"}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345"),
            patch("anteroom.cli.workflow_cli.console"),
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_state.read_issue_state", return_value=state),
            patch("anteroom.cli.workflow_cli.subprocess") as mock_subprocess,
            patch("anteroom.cli.workflow_cli.Table") as mock_table_cls,
        ):
            status_mock = MagicMock()
            status_mock.stdout = "UU src/file.py\nM  src/other.py"
            status_mock.returncode = 0
            ahead_mock = MagicMock()
            ahead_mock.stdout = "2\t1"
            ahead_mock.returncode = 0
            mock_subprocess.run.side_effect = [status_mock, ahead_mock]
            mock_subprocess.TimeoutExpired = TimeoutError

            _handle_worktree(mock_db, args)
        rows = [str(c) for c in mock_table_cls.return_value.add_row.call_args_list]
        status_row = [r for r in rows if "Status" in r]
        assert any("conflicted" in r for r in status_row)

    def test_dirty_worktree(self, tmp_path: Path) -> None:
        from anteroom.cli.workflow_cli import _handle_worktree

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123")
        run = {"id": "abc12345", "status": "running", "inputs": {"issue_number": 42}}
        state = {"worktree_path": str(tmp_path), "branch": "issue-42-fix"}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345"),
            patch("anteroom.cli.workflow_cli.console"),
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_state.read_issue_state", return_value=state),
            patch("anteroom.cli.workflow_cli.subprocess") as mock_subprocess,
            patch("anteroom.cli.workflow_cli.Table") as mock_table_cls,
        ):
            status_mock = MagicMock()
            status_mock.stdout = "M  src/file.py\n?? newfile.txt"
            status_mock.returncode = 0
            ahead_mock = MagicMock()
            ahead_mock.stdout = "0\t0"
            ahead_mock.returncode = 0
            mock_subprocess.run.side_effect = [status_mock, ahead_mock]
            mock_subprocess.TimeoutExpired = TimeoutError

            _handle_worktree(mock_db, args)
        rows = [str(c) for c in mock_table_cls.return_value.add_row.call_args_list]
        status_row = [r for r in rows if "Status" in r]
        assert any("dirty" in r for r in status_row)
        assert any("2 files" in r for r in status_row)

    def test_clean_worktree(self, tmp_path: Path) -> None:
        from anteroom.cli.workflow_cli import _handle_worktree

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123")
        run = {"id": "abc12345", "status": "running", "inputs": {"issue_number": 42}}
        state = {"worktree_path": str(tmp_path), "branch": "issue-42-fix"}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345"),
            patch("anteroom.cli.workflow_cli.console"),
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_state.read_issue_state", return_value=state),
            patch("anteroom.cli.workflow_cli.subprocess") as mock_subprocess,
            patch("anteroom.cli.workflow_cli.Table") as mock_table_cls,
        ):
            status_mock = MagicMock()
            status_mock.stdout = ""
            status_mock.returncode = 0
            ahead_mock = MagicMock()
            ahead_mock.stdout = "0\t0"
            ahead_mock.returncode = 0
            mock_subprocess.run.side_effect = [status_mock, ahead_mock]
            mock_subprocess.TimeoutExpired = TimeoutError

            _handle_worktree(mock_db, args)
        rows = [str(c) for c in mock_table_cls.return_value.add_row.call_args_list]
        status_row = [r for r in rows if "Status" in r]
        assert any("clean" in r for r in status_row)

    def test_displays_state(self, tmp_path: Path) -> None:
        from anteroom.cli.workflow_cli import _handle_worktree

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123")
        run = {"id": "abc12345", "status": "running", "inputs": {"issue_number": 42}}
        state = {"worktree_path": str(tmp_path), "branch": "issue-42-fix"}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345"),
            patch("anteroom.cli.workflow_cli.console") as mock_console,
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_state.read_issue_state", return_value=state),
            patch("anteroom.cli.workflow_cli.subprocess") as mock_subprocess,
        ):
            # Mock git status as clean
            status_mock = MagicMock()
            status_mock.stdout = ""
            status_mock.returncode = 0
            ahead_mock = MagicMock()
            ahead_mock.stdout = "2\t1"
            ahead_mock.returncode = 0
            mock_subprocess.run.side_effect = [status_mock, ahead_mock]
            mock_subprocess.TimeoutExpired = TimeoutError

            _handle_worktree(mock_db, args)
        assert mock_console.print.call_count >= 1


# ---------------------------------------------------------------------------
# _handle_delta
# ---------------------------------------------------------------------------


class TestHandleDelta:
    def test_displays_events(self) -> None:
        from anteroom.cli.workflow_cli import _handle_delta

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123", since_event=0)

        run = {"id": "abc12345", "status": "running", "inputs": None}
        events = [
            {"id": 1, "event_type": "step_started", "step_id": "build", "payload": {"status": "running"}},
            {"id": 2, "event_type": "transcript_stdout", "step_id": "build", "payload": {"content": "building"}},
        ]

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345"),
            patch("anteroom.cli.workflow_cli.console") as mock_console,
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_storage.list_events_since", return_value=events),
        ):
            _handle_delta(mock_db, args)
        assert mock_console.print.call_count >= 2

    def test_no_events_message(self) -> None:
        from anteroom.cli.workflow_cli import _handle_delta

        mock_db = MagicMock()
        args = argparse.Namespace(run_id="abc123", since_event=99)

        run = {"id": "abc12345", "status": "running", "inputs": None}

        with (
            patch("anteroom.cli.workflow_cli._resolve_run_id_or_print", return_value="abc12345"),
            patch("anteroom.cli.workflow_cli.console") as mock_console,
            patch("anteroom.services.workflow_storage.get_workflow_run", return_value=run),
            patch("anteroom.services.workflow_storage.list_events_since", return_value=[]),
        ):
            _handle_delta(mock_db, args)
        output = " ".join(str(c) for c in mock_console.print.call_args_list)
        assert "No new events" in output
