"""Unit tests for BackgroundTaskManager (#1311)."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.db import init_db
from anteroom.services.background_tasks import BackgroundTaskManager


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    return init_db(tmp_path / "test.db")


@pytest.fixture()
def data_dir(tmp_path: Path) -> Path:
    d = tmp_path / "data"
    d.mkdir()
    return d


@pytest.fixture()
def event_bus() -> AsyncMock:
    bus = AsyncMock()
    bus.publish = AsyncMock()
    return bus


@pytest.fixture()
def conv_id(db: Any) -> str:
    """Create a conversation so FK constraints pass."""
    from anteroom.services.storage import create_conversation

    conv = create_conversation(db, title="test")
    return conv["id"]


@pytest.fixture()
async def manager(db: Any, data_dir: Path, event_bus: AsyncMock) -> AsyncGenerator[BackgroundTaskManager, None]:
    mgr = BackgroundTaskManager(db=db, data_dir=data_dir, event_bus=event_bus)
    yield mgr
    await mgr.shutdown()


class TestStartTask:
    @pytest.mark.asyncio
    async def test_start_task_creates_db_record(self, manager: BackgroundTaskManager, db: Any, conv_id: str) -> None:
        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_proc:
            proc = AsyncMock()
            proc.pid = 12345
            proc.communicate = AsyncMock(return_value=(b"output", b""))
            proc.returncode = 0
            mock_proc.return_value = proc

            result = manager.start_task(conv_id, "echo hello")

        assert result["task_id"]
        assert result["status"] == "running"

        task = manager.get_task(result["task_id"])
        assert task is not None
        assert task["command"] == "echo hello"
        assert task["conversation_id"] == conv_id
        assert task["status"] == "running"

    @pytest.mark.asyncio
    async def test_start_task_returns_immediately(self, manager: BackgroundTaskManager, conv_id: str) -> None:
        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_proc:
            proc = AsyncMock()
            proc.pid = 123
            proc.communicate = AsyncMock(return_value=(b"", b""))
            proc.returncode = 0
            mock_proc.return_value = proc

            result = manager.start_task(conv_id, "sleep 100")

        # Should return without waiting for the command to finish
        assert result["status"] == "running"

    @pytest.mark.asyncio
    async def test_task_completion_updates_db(self, manager: BackgroundTaskManager, db: Any, conv_id: str) -> None:
        proc = AsyncMock()
        proc.pid = 123
        proc.communicate = AsyncMock(return_value=(b"done", b""))
        proc.returncode = 0

        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            mock_create.return_value = proc
            result = manager.start_task(conv_id, "echo done")

            # Let the collector coroutine run
            await asyncio.sleep(0.1)

        task = manager.get_task(result["task_id"])
        assert task is not None
        assert task["status"] == "completed"
        assert task["exit_code"] == 0
        assert task["stdout_preview"] == "done"

    @pytest.mark.asyncio
    async def test_task_completion_publishes_event(
        self, manager: BackgroundTaskManager, event_bus: MagicMock, conv_id: str
    ) -> None:
        proc = AsyncMock()
        proc.pid = 123
        proc.communicate = AsyncMock(return_value=(b"ok", b""))
        proc.returncode = 0

        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            mock_create.return_value = proc
            manager.start_task(conv_id, "echo ok")
            await asyncio.sleep(0.1)

        # Should have published task_started and task_completed
        calls = [c[0] for c in event_bus.publish.call_args_list]
        event_types = [c[1].get("type") for c in calls]
        assert "task_started" in event_types
        assert "task_completed" in event_types

    @pytest.mark.asyncio
    async def test_failed_task_captures_exit_code(self, manager: BackgroundTaskManager, conv_id: str) -> None:
        proc = AsyncMock()
        proc.pid = 123
        proc.communicate = AsyncMock(return_value=(b"", b"error"))
        proc.returncode = 1

        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            mock_create.return_value = proc
            result = manager.start_task(conv_id, "false")
            await asyncio.sleep(0.1)

        task = manager.get_task(result["task_id"])
        assert task is not None
        assert task["status"] == "failed"
        assert task["exit_code"] == 1
        assert task["stderr_preview"] == "error"


class TestGetAndList:
    def test_get_task_returns_none_for_missing(self, manager: BackgroundTaskManager) -> None:
        assert manager.get_task("nonexistent") is None

    @pytest.mark.asyncio
    async def test_list_tasks_filters_by_conversation(self, manager: BackgroundTaskManager, conv_id: str) -> None:
        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            proc = AsyncMock()
            proc.pid = 1
            proc.communicate = AsyncMock(return_value=(b"", b""))
            proc.returncode = 0
            mock_create.return_value = proc

            manager.start_task(conv_id, "cmd1")

        tasks = manager.list_tasks(conv_id)
        assert len(tasks) == 1
        assert tasks[0]["command"] == "cmd1"

    @pytest.mark.asyncio
    async def test_list_tasks_filters_by_status(self, manager: BackgroundTaskManager, conv_id: str) -> None:
        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            proc = AsyncMock()
            proc.pid = 1
            proc.communicate = AsyncMock(return_value=(b"", b""))
            proc.returncode = 0
            mock_create.return_value = proc

            manager.start_task(conv_id, "cmd1")
            await asyncio.sleep(0.1)  # Let it complete

        running = manager.list_tasks(conv_id, status="running")
        completed = manager.list_tasks(conv_id, status="completed")
        assert len(running) == 0
        assert len(completed) == 1


class TestCancel:
    @pytest.mark.asyncio
    async def test_cancel_task_updates_status(self, manager: BackgroundTaskManager, conv_id: str) -> None:
        proc = AsyncMock()
        proc.pid = 123
        # Make communicate hang so we can cancel
        proc.communicate = AsyncMock(side_effect=asyncio.CancelledError)
        proc.returncode = -9

        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            mock_create.return_value = proc
            result = manager.start_task(conv_id, "sleep 999")

        assert manager.cancel_task(result["task_id"]) is True
        task = manager.get_task(result["task_id"])
        assert task is not None
        assert task["status"] == "cancelled"

    def test_cancel_nonexistent_returns_false(self, manager: BackgroundTaskManager) -> None:
        assert manager.cancel_task("nonexistent") is False


class TestConcurrencyCaps:
    @pytest.mark.asyncio
    async def test_concurrent_task_cap_enforced(self, manager: BackgroundTaskManager, conv_id: str) -> None:
        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            proc = AsyncMock()
            proc.pid = 1
            # Never complete — stays running
            proc.communicate = AsyncMock(side_effect=asyncio.CancelledError)
            proc.returncode = -1
            mock_create.return_value = proc

            for i in range(5):
                manager.start_task(conv_id, f"cmd{i}")

            with pytest.raises(ValueError, match="Too many background tasks"):
                manager.start_task(conv_id, "cmd-overflow")


class TestCountRunning:
    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Hangs in CI — mocked CancelledError leaks into event loop. See #1376")
    async def test_count_running_reflects_active_tasks(self, manager: BackgroundTaskManager, conv_id: str) -> None:
        assert manager.count_running() == 0

        proc = AsyncMock()
        proc.pid = 1
        proc.communicate = AsyncMock(side_effect=asyncio.CancelledError)
        proc.returncode = -1

        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            mock_create.return_value = proc
            manager.start_task(conv_id, "sleep 999")
            manager.start_task(conv_id, "sleep 998")

        assert manager.count_running() == 2

    @pytest.mark.asyncio
    async def test_count_running_decreases_after_completion(self, manager: BackgroundTaskManager, conv_id: str) -> None:
        proc = AsyncMock()
        proc.pid = 1
        proc.communicate = AsyncMock(return_value=(b"ok", b""))
        proc.returncode = 0

        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            mock_create.return_value = proc
            manager.start_task(conv_id, "echo done")
            await asyncio.sleep(0.1)

        assert manager.count_running() == 0


class TestPollCompleted:
    @pytest.mark.asyncio
    async def test_poll_completed_returns_new_completions(self, manager: BackgroundTaskManager, conv_id: str) -> None:
        # First poll initializes the timestamp
        assert manager.poll_completed() == []

        proc = AsyncMock()
        proc.pid = 123
        proc.communicate = AsyncMock(return_value=(b"ok", b""))
        proc.returncode = 0

        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            mock_create.return_value = proc
            manager.start_task(conv_id, "echo ok")
            await asyncio.sleep(0.1)

        completed = manager.poll_completed()
        assert len(completed) == 1
        assert completed[0]["status"] == "completed"

        # Second poll should return nothing new
        assert manager.poll_completed() == []


class TestStdoutPreview:
    @pytest.mark.asyncio
    async def test_stdout_preview_truncated_to_2kb(self, manager: BackgroundTaskManager, conv_id: str) -> None:
        large_output = b"x" * 5000
        proc = AsyncMock()
        proc.pid = 123
        proc.communicate = AsyncMock(return_value=(large_output, b""))
        proc.returncode = 0

        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_create:
            mock_create.return_value = proc
            result = manager.start_task(conv_id, "big output")
            await asyncio.sleep(0.1)

        task = manager.get_task(result["task_id"])
        assert task is not None
        assert len(task["stdout_preview"]) == 2048
