"""Unit tests for completion notification enrichment (#1315).

Covers:
- BackgroundTaskManager._collect emits task_completed with duration_seconds
- DetachedSubagentManager._collect emits agent_run_completed with summary and duration_seconds
- BackgroundTaskManager.poll_completed returns records with duration_seconds
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from anteroom.db import init_db
from anteroom.services.background_tasks import BackgroundTaskManager, _compute_duration
from anteroom.services.detached_subagent_manager import DetachedSubagentManager

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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
    from anteroom.services.storage import create_conversation

    conv = create_conversation(db, title="test")
    return conv["id"]


@pytest.fixture()
async def bg_manager(db: Any, data_dir: Path, event_bus: AsyncMock) -> AsyncGenerator[BackgroundTaskManager, None]:
    mgr = BackgroundTaskManager(db=db, data_dir=data_dir, event_bus=event_bus)
    yield mgr
    await mgr.shutdown()


@pytest.fixture()
async def detached_manager(db: Any, event_bus: AsyncMock) -> AsyncGenerator[DetachedSubagentManager, None]:
    mgr = DetachedSubagentManager(db=db, event_bus=event_bus)
    yield mgr
    await mgr.shutdown()


# ---------------------------------------------------------------------------
# BackgroundTaskManager — task_completed event includes duration_seconds
# ---------------------------------------------------------------------------


class TestBgTaskCompletedEventIncludesDuration:
    @pytest.mark.asyncio
    async def test_task_completed_event_includes_duration_seconds(
        self, bg_manager: BackgroundTaskManager, event_bus: AsyncMock, conv_id: str
    ) -> None:
        """task_completed event payload must contain duration_seconds >= 0."""
        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_proc:
            proc = AsyncMock()
            proc.pid = 99
            proc.communicate = AsyncMock(return_value=(b"hello", b""))
            proc.returncode = 0
            mock_proc.return_value = proc

            bg_manager.start_task(conv_id, "echo hello")
            # Wait for the collector to finish
            await asyncio.sleep(0.1)
            for _ in range(20):
                if not bg_manager._tasks:
                    break
                await asyncio.sleep(0.05)

        assert event_bus.publish.called
        # Find the task_completed call
        completed_calls = [
            call for call in event_bus.publish.call_args_list if call[0][1].get("type") == "task_completed"
        ]
        assert len(completed_calls) >= 1
        data = completed_calls[0][0][1]["data"]
        assert "duration_seconds" in data
        assert isinstance(data["duration_seconds"], float)
        assert data["duration_seconds"] >= 0.0

    @pytest.mark.asyncio
    async def test_timeout_task_completed_event_includes_duration_seconds(
        self, bg_manager: BackgroundTaskManager, event_bus: AsyncMock, conv_id: str
    ) -> None:
        """Timed-out tasks also emit task_completed with duration_seconds."""
        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_proc:
            proc = AsyncMock()
            proc.pid = 100
            proc.returncode = -1

            async def _slow_communicate() -> tuple[bytes, bytes]:
                raise asyncio.TimeoutError

            proc.communicate = _slow_communicate
            proc.kill = AsyncMock()
            proc.wait = AsyncMock()
            mock_proc.return_value = proc

            with patch("anteroom.services.background_tasks.asyncio.wait_for", side_effect=asyncio.TimeoutError):
                bg_manager.start_task(conv_id, "sleep 9999", timeout=0.01)
                await asyncio.sleep(0.2)
                for _ in range(20):
                    if not bg_manager._tasks:
                        break
                    await asyncio.sleep(0.05)

        completed_calls = [
            call for call in event_bus.publish.call_args_list if call[0][1].get("type") == "task_completed"
        ]
        assert len(completed_calls) >= 1
        data = completed_calls[0][0][1]["data"]
        assert "duration_seconds" in data
        assert data["duration_seconds"] >= 0.0


# ---------------------------------------------------------------------------
# DetachedSubagentManager — agent_run_completed event includes summary and duration
# ---------------------------------------------------------------------------


class TestDetachedRunCompletedEventPayload:
    @pytest.mark.asyncio
    async def test_agent_run_completed_event_includes_summary_and_duration(
        self, detached_manager: DetachedSubagentManager, event_bus: AsyncMock, conv_id: str
    ) -> None:
        """agent_run_completed payload must have summary, duration_seconds, and tool_calls_count."""
        fake_result = {
            "output": "Analysis complete. Found 3 issues.",
            "tool_calls_made": ["read_file", "grep"],
            "model_used": "gpt-4o",
            "truncated": False,
            "error": None,
        }

        # Use the real _collect path with a patched _run_subagent
        with patch("anteroom.tools.subagent._run_subagent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = fake_result

            mock_ai = AsyncMock()
            mock_tools = AsyncMock()
            detached_manager.start(
                conv_id,
                "Analyze the codebase",
                ai_service=mock_ai,
                tool_registry=mock_tools,
            )
            await asyncio.sleep(0.1)
            for _ in range(20):
                if not detached_manager._tasks:
                    break
                await asyncio.sleep(0.05)

        completed_calls = [
            call for call in event_bus.publish.call_args_list if call[0][1].get("type") == "agent_run_completed"
        ]
        assert len(completed_calls) >= 1
        data = completed_calls[0][0][1]["data"]

        assert "summary" in data
        assert data["summary"] == fake_result["output"][:200]

        assert "duration_seconds" in data
        assert isinstance(data["duration_seconds"], float)
        assert data["duration_seconds"] >= 0.0

        assert "tool_calls_count" in data
        assert data["tool_calls_count"] == 2


# ---------------------------------------------------------------------------
# BackgroundTaskManager.poll_completed returns duration_seconds
# ---------------------------------------------------------------------------


class TestPollCompletedReturnsDuration:
    @pytest.mark.asyncio
    async def test_poll_completed_returns_duration_seconds(
        self, bg_manager: BackgroundTaskManager, conv_id: str
    ) -> None:
        """poll_completed results must include duration_seconds computed from timestamps."""
        with patch(
            "anteroom.services.background_tasks.asyncio.create_subprocess_shell", new_callable=AsyncMock
        ) as mock_proc:
            proc = AsyncMock()
            proc.pid = 101
            proc.communicate = AsyncMock(return_value=(b"ok", b""))
            proc.returncode = 0
            mock_proc.return_value = proc

            # Initialize the poll cursor
            bg_manager.poll_completed()

            bg_manager.start_task(conv_id, "echo ok")
            await asyncio.sleep(0.1)
            for _ in range(20):
                if not bg_manager._tasks:
                    break
                await asyncio.sleep(0.05)

        results = bg_manager.poll_completed()
        assert len(results) >= 1
        task = results[0]
        assert "duration_seconds" in task
        assert isinstance(task["duration_seconds"], float)
        assert task["duration_seconds"] >= 0.0


# ---------------------------------------------------------------------------
# _compute_duration helper
# ---------------------------------------------------------------------------


class TestComputeDuration:
    def test_valid_timestamps_return_positive_duration(self) -> None:
        started = "2026-01-01T10:00:00.000000+00:00"
        completed = "2026-01-01T10:00:05.500000+00:00"
        result = _compute_duration(started, completed)
        assert abs(result - 5.5) < 0.01

    def test_missing_started_returns_zero(self) -> None:
        assert _compute_duration(None, "2026-01-01T10:00:05.000000+00:00") == 0.0

    def test_missing_completed_returns_zero(self) -> None:
        assert _compute_duration("2026-01-01T10:00:00.000000+00:00", None) == 0.0

    def test_invalid_timestamps_return_zero(self) -> None:
        assert _compute_duration("not-a-date", "also-not-a-date") == 0.0
