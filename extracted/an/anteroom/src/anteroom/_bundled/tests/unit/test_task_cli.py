"""Tests for CLI task command handlers (#1312)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from anteroom.cli.task_cli import (
    handle_task_cancel,
    handle_task_list,
    handle_task_output,
    handle_task_show,
)


def _make_bg_manager(tasks: list[dict] | None = None, data_dir: Path | None = None) -> MagicMock:
    mgr = MagicMock()
    mgr.data_dir = data_dir or Path("/tmp/test")
    all_tasks = tasks or []
    mgr.list_tasks.return_value = all_tasks

    def _get(tid: str) -> dict | None:
        for t in all_tasks:
            if t["id"] == tid or t["id"].startswith(tid):
                return t
        return None

    mgr.get_task.side_effect = _get
    return mgr


class TestHandleTaskList:
    def test_empty_list(self) -> None:
        mgr = _make_bg_manager([])
        with patch("anteroom.cli.task_cli.console") as mock_console:
            handle_task_list(mgr, "conv-1")
            mock_console.print.assert_called()

    def test_shows_tasks(self) -> None:
        tasks = [
            {
                "id": "aaaa1111-2222-3333-4444-555555555555",
                "status": "completed",
                "command": "echo hello",
                "created_at": "2026-01-01T00:00:00",
            },
            {
                "id": "bbbb1111-2222-3333-4444-555555555555",
                "status": "running",
                "command": "sleep 60",
                "created_at": "2026-01-01T01:00:00",
            },
        ]
        mgr = _make_bg_manager(tasks)
        with patch("anteroom.cli.task_cli.console") as mock_console:
            handle_task_list(mgr, "conv-1")
            assert mock_console.print.called


class TestHandleTaskShow:
    def test_task_not_found(self) -> None:
        mgr = _make_bg_manager([])
        with patch("anteroom.cli.task_cli.console") as mock_console:
            handle_task_show(mgr, "nonexistent")
            printed = mock_console.print.call_args[0][0]
            assert "not found" in printed

    def test_shows_task_detail(self) -> None:
        tasks = [
            {
                "id": "aaaa1111-2222-3333-4444-555555555555",
                "status": "completed",
                "command": "echo hello",
                "created_at": "2026-01-01T00:00:00",
                "completed_at": "2026-01-01T00:01:00",
                "preview": "hello",
            }
        ]
        mgr = _make_bg_manager(tasks)
        with patch("anteroom.cli.task_cli.console") as mock_console:
            handle_task_show(mgr, "aaaa1111-2222-3333-4444-555555555555")
            assert mock_console.print.called


class TestHandleTaskOutput:
    def test_task_not_found(self) -> None:
        mgr = _make_bg_manager([])
        with patch("anteroom.cli.task_cli.console") as mock_console:
            handle_task_output(mgr, "nonexistent")
            printed = mock_console.print.call_args[0][0]
            assert "not found" in printed

    def test_no_output_available(self, tmp_path: Path) -> None:
        tasks = [
            {
                "id": "aaaa1111-2222-3333-4444-555555555555",
                "conversation_id": "conv-1",
                "status": "running",
                "command": "sleep 60",
            }
        ]
        mgr = _make_bg_manager(tasks, data_dir=tmp_path)
        with patch("anteroom.cli.task_cli.console") as mock_console:
            handle_task_output(mgr, "aaaa1111-2222-3333-4444-555555555555")
            printed = mock_console.print.call_args[0][0]
            assert "No output" in printed

    def test_shows_output(self, tmp_path: Path) -> None:
        task_id = "aaaa1111-2222-3333-4444-555555555555"
        conv_id = "conv-1"
        tasks = [
            {
                "id": task_id,
                "conversation_id": conv_id,
                "status": "completed",
                "command": "echo hello",
            }
        ]
        mgr = _make_bg_manager(tasks, data_dir=tmp_path)

        out_dir = tmp_path / "task_output" / conv_id
        out_dir.mkdir(parents=True)
        (out_dir / f"{task_id}.stdout").write_text("hello world\n")

        with patch("anteroom.cli.task_cli.console") as mock_console:
            handle_task_output(mgr, task_id)
            assert mock_console.print.called


class TestHandleTaskCancel:
    def test_task_not_found(self) -> None:
        mgr = _make_bg_manager([])
        with patch("anteroom.cli.task_cli.console") as mock_console:
            handle_task_cancel(mgr, "nonexistent")
            printed = mock_console.print.call_args[0][0]
            assert "not found" in printed

    def test_not_running(self) -> None:
        tasks = [
            {
                "id": "aaaa1111-2222-3333-4444-555555555555",
                "status": "completed",
                "command": "echo done",
            }
        ]
        mgr = _make_bg_manager(tasks)
        with patch("anteroom.cli.task_cli.console") as mock_console:
            handle_task_cancel(mgr, "aaaa1111-2222-3333-4444-555555555555")
            printed = mock_console.print.call_args[0][0]
            assert "not running" in printed

    def test_cancel_running(self) -> None:
        tasks = [
            {
                "id": "aaaa1111-2222-3333-4444-555555555555",
                "status": "running",
                "command": "sleep 60",
            }
        ]
        mgr = _make_bg_manager(tasks)
        with patch("anteroom.cli.task_cli.console"):
            handle_task_cancel(mgr, "aaaa1111-2222-3333-4444-555555555555")
            mgr.cancel_task.assert_called_once_with("aaaa1111-2222-3333-4444-555555555555")
