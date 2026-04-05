"""Tests for bash_task_output tool handler (#1312)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from anteroom.tools.bash import handle_task_output


def _make_bg_manager(task: dict | None = None, data_dir: Path | None = None) -> MagicMock:
    mgr = MagicMock()
    mgr.data_dir = data_dir or Path("/tmp/test")
    mgr.get_task.return_value = task
    return mgr


class TestHandleTaskOutput:
    @pytest.mark.asyncio
    async def test_no_bg_manager(self) -> None:
        result = await handle_task_output(task_id="t1", _bg_manager=None)
        assert "error" in result

    @pytest.mark.asyncio
    async def test_task_not_found(self) -> None:
        mgr = _make_bg_manager(task=None)
        result = await handle_task_output(task_id="t1", _bg_manager=mgr)
        assert "error" in result
        assert "not found" in result["error"]

    @pytest.mark.asyncio
    async def test_read_stdout(self, tmp_path: Path) -> None:
        task_id = "task-abc"
        conv_id = "conv-123"
        task = {"id": task_id, "conversation_id": conv_id, "status": "completed"}
        mgr = _make_bg_manager(task=task, data_dir=tmp_path)

        out_dir = tmp_path / "task_output" / conv_id
        out_dir.mkdir(parents=True)
        (out_dir / f"{task_id}.stdout").write_text("hello world\n")

        result = await handle_task_output(task_id=task_id, _bg_manager=mgr)
        assert result["content"] == "hello world\n"
        assert result["stream"] == "stdout"
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_read_stderr(self, tmp_path: Path) -> None:
        task_id = "task-abc"
        conv_id = "conv-123"
        task = {"id": task_id, "conversation_id": conv_id, "status": "failed"}
        mgr = _make_bg_manager(task=task, data_dir=tmp_path)

        out_dir = tmp_path / "task_output" / conv_id
        out_dir.mkdir(parents=True)
        (out_dir / f"{task_id}.stderr").write_text("error: something failed\n")

        result = await handle_task_output(task_id=task_id, stream="stderr", _bg_manager=mgr)
        assert "error: something failed" in result["content"]
        assert result["stream"] == "stderr"

    @pytest.mark.asyncio
    async def test_tail_lines(self, tmp_path: Path) -> None:
        task_id = "task-abc"
        conv_id = "conv-123"
        task = {"id": task_id, "conversation_id": conv_id, "status": "running"}
        mgr = _make_bg_manager(task=task, data_dir=tmp_path)

        out_dir = tmp_path / "task_output" / conv_id
        out_dir.mkdir(parents=True)
        (out_dir / f"{task_id}.stdout").write_text("line1\nline2\nline3\nline4\nline5\n")

        result = await handle_task_output(task_id=task_id, tail_lines=2, _bg_manager=mgr)
        assert "line4\n" in result["content"]
        assert "line5\n" in result["content"]
        assert "line1\n" not in result["content"]

    @pytest.mark.asyncio
    async def test_empty_output(self, tmp_path: Path) -> None:
        task_id = "task-abc"
        conv_id = "conv-123"
        task = {"id": task_id, "conversation_id": conv_id, "status": "completed"}
        mgr = _make_bg_manager(task=task, data_dir=tmp_path)

        result = await handle_task_output(task_id=task_id, _bg_manager=mgr)
        assert result["content"] == ""
        assert result["lines"] == 0
