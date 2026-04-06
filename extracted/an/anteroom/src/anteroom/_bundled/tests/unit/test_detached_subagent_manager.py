"""Unit tests for DetachedSubagentManager (#1314)."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.db import init_db
from anteroom.services.detached_subagent_manager import DetachedSubagentManager


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    return init_db(tmp_path / "test.db")


@pytest.fixture()
def conv_id(db: Any) -> str:
    from anteroom.services.storage import create_conversation

    conv = create_conversation(db, title="test")
    return conv["id"]


@pytest.fixture()
def event_bus() -> AsyncMock:
    bus = AsyncMock()
    bus.publish = AsyncMock()
    return bus


@pytest.fixture()
async def manager(db: Any, event_bus: AsyncMock) -> AsyncGenerator[DetachedSubagentManager, None]:
    mgr = DetachedSubagentManager(db=db, event_bus=event_bus)
    yield mgr
    await mgr.shutdown()


def _mock_run_subagent_result(output: str = "done", error: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "output": output,
        "elapsed_seconds": 1.5,
        "tool_calls_made": ["read_file", "bash"],
        "model_used": "test-model",
        "truncated": False,
    }
    if error:
        result["error"] = error
    return result


class TestStartAndComplete:
    @pytest.mark.asyncio
    async def test_start_creates_agent_run_record(
        self, manager: DetachedSubagentManager, db: Any, conv_id: str
    ) -> None:
        ai = MagicMock()
        ai.config = MagicMock()

        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            result = manager.start(conv_id, "test prompt", ai_service=ai, tool_registry=MagicMock())

        assert result["run_id"]
        assert result["status"] == "running"

        run = manager.get_run(result["run_id"])
        assert run is not None
        assert run["kind"] == "detached_subagent"
        assert run["status"] == "running"

    @pytest.mark.asyncio
    async def test_completion_updates_db(self, manager: DetachedSubagentManager, db: Any, conv_id: str) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            result = manager.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        run = manager.get_run(result["run_id"])
        assert run is not None
        assert run["status"] == "completed"
        assert run["duration_ms"] is not None

    @pytest.mark.asyncio
    async def test_failed_run_records_error(self, manager: DetachedSubagentManager, db: Any, conv_id: str) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(error="Something failed"),
        ):
            result = manager.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        run = manager.get_run(result["run_id"])
        assert run is not None
        assert run["status"] == "failed"

    @pytest.mark.asyncio
    async def test_completion_publishes_event(
        self, manager: DetachedSubagentManager, event_bus: AsyncMock, conv_id: str
    ) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            manager.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        calls = [c[0] for c in event_bus.publish.call_args_list]
        event_types = [c[1].get("type") for c in calls]
        assert "agent_run_started" in event_types
        assert "agent_run_completed" in event_types


class TestCancel:
    @pytest.mark.asyncio
    async def test_cancel_running_run(self, manager: DetachedSubagentManager, conv_id: str) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            side_effect=asyncio.CancelledError,
        ):
            result = manager.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())

        assert manager.cancel(result["run_id"]) is True
        run = manager.get_run(result["run_id"])
        assert run is not None
        assert run["status"] == "cancelled"

    def test_cancel_nonexistent_returns_false(self, manager: DetachedSubagentManager) -> None:
        assert manager.cancel("nonexistent") is False


class TestRetry:
    @pytest.mark.asyncio
    async def test_retry_creates_new_run_with_linkage(
        self, manager: DetachedSubagentManager, db: Any, conv_id: str
    ) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(error="transient"),
        ):
            result = manager.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        # Original should be failed
        original = manager.get_run(result["run_id"])
        assert original is not None
        assert original["status"] == "failed"

        # Retry
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            retry_result = manager.retry(result["run_id"], ai_service=MagicMock(), tool_registry=MagicMock())

        assert retry_result["run_id"] != result["run_id"]
        assert retry_result["parent_run_id"] == result["run_id"]
        assert retry_result["status"] == "running"

    @pytest.mark.asyncio
    async def test_retry_running_raises(self, manager: DetachedSubagentManager, conv_id: str) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            side_effect=asyncio.CancelledError,
        ):
            result = manager.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())

        with pytest.raises(ValueError, match="Can only retry"):
            manager.retry(result["run_id"], ai_service=MagicMock(), tool_registry=MagicMock())


class TestConcurrencyCaps:
    @pytest.mark.asyncio
    async def test_cap_enforced(self, manager: DetachedSubagentManager, conv_id: str) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            side_effect=asyncio.CancelledError,
        ):
            for _ in range(3):
                manager.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())

            with pytest.raises(ValueError, match="Too many detached agents"):
                manager.start(conv_id, "overflow", ai_service=MagicMock(), tool_registry=MagicMock())


class TestListAndPoll:
    @pytest.mark.asyncio
    async def test_list_runs_filters_by_conversation(self, manager: DetachedSubagentManager, conv_id: str) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            manager.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())

        runs = manager.list_runs(conv_id)
        assert len(runs) == 1
        assert runs[0]["kind"] == "detached_subagent"

    @pytest.mark.asyncio
    async def test_poll_completed_returns_new(self, manager: DetachedSubagentManager, conv_id: str) -> None:
        assert manager.poll_completed() == []

        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            manager.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        completed = manager.poll_completed()
        assert len(completed) == 1
        assert completed[0]["status"] == "completed"

        # Second poll returns nothing
        assert manager.poll_completed() == []


class TestGetRunNone:
    def test_get_run_nonexistent(self, manager: DetachedSubagentManager) -> None:
        assert manager.get_run("nonexistent") is None
