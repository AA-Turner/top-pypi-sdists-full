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


@pytest.fixture()
def stub_writer() -> Any:
    captured: list[Any] = []
    writer = MagicMock()
    writer.enabled = True
    writer.emit.side_effect = captured.append
    writer.captured = captured  # type: ignore[attr-defined]
    return writer


@pytest.fixture()
async def manager_with_audit(
    db: Any,
    event_bus: AsyncMock,
    stub_writer: Any,
) -> AsyncGenerator[DetachedSubagentManager, None]:
    from anteroom.config import SubagentConfig

    mgr = DetachedSubagentManager(
        db=db,
        event_bus=event_bus,
        config=SubagentConfig(max_concurrent=2, max_total=5),
        audit_writer=stub_writer,
    )
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

    @pytest.mark.asyncio
    async def test_completion_payload_includes_description(
        self, manager: DetachedSubagentManager, event_bus: AsyncMock, conv_id: str
    ) -> None:
        """agent_run_completed SSE payload must include description when provided.

        This is the backend-to-SSE contract test: verifies that description
        set at enqueue time is echoed into the completion event so the web
        chip renderer can prefer it over summary (#1461).
        """
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            manager.start(
                conv_id,
                "test prompt",
                description="my custom label",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        completed_calls = [
            c[0][1] for c in event_bus.publish.call_args_list if c[0][1].get("type") == "agent_run_completed"
        ]
        assert completed_calls, "agent_run_completed event was not published"
        payload = completed_calls[-1]["data"]
        assert payload.get("description") == "my custom label", (
            f"Expected description in completion payload; got {payload!r}"
        )

    @pytest.mark.asyncio
    async def test_completion_payload_omits_description_when_not_provided(
        self, manager: DetachedSubagentManager, event_bus: AsyncMock, conv_id: str
    ) -> None:
        """agent_run_completed SSE payload must not include description key when not set."""
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            manager.start(conv_id, "test prompt", ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        completed_calls = [
            c[0][1] for c in event_bus.publish.call_args_list if c[0][1].get("type") == "agent_run_completed"
        ]
        assert completed_calls, "agent_run_completed event was not published"
        payload = completed_calls[-1]["data"]
        assert "description" not in payload, f"description should not appear in payload when not set; got {payload!r}"


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
    @pytest.mark.parametrize("max_concurrent", [1, 2, 4])
    async def test_cap_enforced_from_config(
        self,
        db: Any,
        event_bus: AsyncMock,
        conv_id: str,
        max_concurrent: int,
    ) -> None:
        from anteroom.config import SubagentConfig

        mgr = DetachedSubagentManager(
            db=db,
            event_bus=event_bus,
            config=SubagentConfig(max_concurrent=max_concurrent, max_total=20),
        )
        try:
            with patch(
                "anteroom.tools.subagent._run_subagent",
                new_callable=AsyncMock,
                side_effect=asyncio.CancelledError,
            ):
                for _ in range(max_concurrent):
                    mgr.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
                with pytest.raises(ValueError, match="Too many detached agents for this conversation"):
                    mgr.start(conv_id, "overflow", ai_service=MagicMock(), tool_registry=MagicMock())
        finally:
            await mgr.shutdown()


class TestBackwardCompatConstruction:
    @pytest.mark.asyncio
    async def test_construction_without_config_or_audit_writer(
        self, db: Any, event_bus: AsyncMock, conv_id: str
    ) -> None:
        """Legacy call site — e.g., cli/agent_cli.py:15 — must keep working."""
        mgr = DetachedSubagentManager(db=db)
        try:
            with patch(
                "anteroom.tools.subagent._run_subagent",
                new_callable=AsyncMock,
                return_value=_mock_run_subagent_result(),
            ):
                result = mgr.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
                await asyncio.sleep(0.1)
            run = mgr.get_run(result["run_id"])
            assert run is not None
            assert run["status"] == "completed"
        finally:
            await mgr.shutdown()


class TestAuditEmission:
    @pytest.mark.asyncio
    async def test_spawned_emitted_on_start(
        self, manager_with_audit: DetachedSubagentManager, stub_writer: Any, conv_id: str
    ) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            result = manager_with_audit.start(
                conv_id,
                "test",
                model="claude-sonnet-4-6",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        events = [e.event_type for e in stub_writer.captured]
        assert "subagent.spawned" in events
        spawn = next(e for e in stub_writer.captured if e.event_type == "subagent.spawned")
        assert spawn.details["run_id"] == result["run_id"]
        assert spawn.details["conversation_id"] == conv_id
        assert spawn.details["model"] == "claude-sonnet-4-6"

    @pytest.mark.asyncio
    async def test_completed_emitted_on_success(
        self, manager_with_audit: DetachedSubagentManager, stub_writer: Any, conv_id: str
    ) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            manager_with_audit.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        events = [e.event_type for e in stub_writer.captured]
        assert "subagent.completed" in events
        done = next(e for e in stub_writer.captured if e.event_type == "subagent.completed")
        assert done.severity == "info"
        assert "duration_ms" in done.details
        assert "tool_calls" in done.details

    @pytest.mark.asyncio
    async def test_failed_emitted_on_error_result(
        self, manager_with_audit: DetachedSubagentManager, stub_writer: Any, conv_id: str
    ) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(error="boom"),
        ):
            manager_with_audit.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        events = [e.event_type for e in stub_writer.captured]
        assert "subagent.failed" in events
        fail = next(e for e in stub_writer.captured if e.event_type == "subagent.failed")
        assert fail.severity == "warning"

    @pytest.mark.asyncio
    async def test_cancelled_emitted_on_cancel(
        self, manager_with_audit: DetachedSubagentManager, stub_writer: Any, conv_id: str
    ) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            side_effect=asyncio.CancelledError,
        ):
            result = manager_with_audit.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            assert manager_with_audit.cancel(result["run_id"]) is True
            await asyncio.sleep(0.1)

        events = [e.event_type for e in stub_writer.captured]
        assert "subagent.cancelled" in events
        cancel = next(e for e in stub_writer.captured if e.event_type == "subagent.cancelled")
        assert cancel.severity == "warning"

    @pytest.mark.asyncio
    async def test_retry_emits_spawned_with_parent_linkage(
        self, manager_with_audit: DetachedSubagentManager, stub_writer: Any, conv_id: str
    ) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(error="transient"),
        ):
            result = manager_with_audit.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        stub_writer.captured.clear()  # isolate retry emissions

        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            retry_result = manager_with_audit.retry(
                result["run_id"],
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        spawn = next(e for e in stub_writer.captured if e.event_type == "subagent.spawned")
        assert spawn.details["run_id"] == retry_result["run_id"]
        assert spawn.details["parent_run_id"] == result["run_id"]

    @pytest.mark.asyncio
    async def test_operator_cancel_emits_exactly_once(
        self, manager_with_audit: DetachedSubagentManager, stub_writer: Any, conv_id: str
    ) -> None:
        """Operator-initiated cancel must not double-emit subagent.cancelled."""

        async def slow_collector(*args: Any, **kwargs: Any) -> dict[str, Any]:
            await asyncio.sleep(10)  # will be cancelled
            return {"output": "never"}  # pragma: no cover

        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            side_effect=slow_collector,
        ):
            result = manager_with_audit.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            # Let the collector actually start running
            await asyncio.sleep(0.05)
            assert manager_with_audit.cancel(result["run_id"]) is True
            # Give the collector's except CancelledError branch a chance to run
            await asyncio.sleep(0.1)

        cancelled_events = [e for e in stub_writer.captured if e.event_type == "subagent.cancelled"]
        assert len(cancelled_events) == 1, (
            f"expected exactly one subagent.cancelled emission, got {len(cancelled_events)}: "
            f"{[e.details for e in cancelled_events]}"
        )

    @pytest.mark.asyncio
    async def test_shutdown_still_emits_cancelled_without_operator(
        self, db: Any, event_bus: AsyncMock, stub_writer: Any, conv_id: str
    ) -> None:
        """Non-operator cancellation (e.g., shutdown) must still produce an audit entry."""
        from anteroom.config import SubagentConfig

        mgr = DetachedSubagentManager(
            db=db,
            event_bus=event_bus,
            config=SubagentConfig(max_concurrent=2, max_total=5),
            audit_writer=stub_writer,
        )

        async def slow_collector(*args: Any, **kwargs: Any) -> dict[str, Any]:
            await asyncio.sleep(10)
            return {"output": "never"}  # pragma: no cover

        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            side_effect=slow_collector,
        ):
            mgr.start(conv_id, "test", ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.05)
            await mgr.shutdown()

        cancelled_events = [e for e in stub_writer.captured if e.event_type == "subagent.cancelled"]
        assert len(cancelled_events) == 1


class TestModelPersistence:
    @pytest.mark.asyncio
    async def test_model_persisted_in_metadata(self, manager: DetachedSubagentManager, conv_id: str) -> None:
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            result = manager.start(
                conv_id,
                "test",
                model="claude-haiku-4-5",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        run = manager.get_run(result["run_id"])
        assert run is not None
        meta = run.get("metadata") or {}
        assert meta.get("model") == "claude-haiku-4-5"

    @pytest.mark.asyncio
    async def test_retry_defaults_to_original_model(self, manager: DetachedSubagentManager, conv_id: str) -> None:
        """Retry with no explicit model override must preserve the original model (#1459)."""
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(error="transient"),
        ):
            result = manager.start(
                conv_id,
                "test",
                model="claude-haiku-4-5",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        captured_models: list[Any] = []

        async def _capture(*args: Any, **kwargs: Any) -> dict[str, Any]:
            captured_models.append(kwargs.get("model"))
            return _mock_run_subagent_result()

        with patch("anteroom.tools.subagent._run_subagent", new_callable=AsyncMock, side_effect=_capture):
            retry_result = manager.retry(
                result["run_id"],
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        # retry() forwards the original model to _run_subagent
        assert captured_models == ["claude-haiku-4-5"]

        # retry() persists the original model in new run's metadata
        new_run = manager.get_run(retry_result["run_id"])
        assert new_run is not None
        assert (new_run.get("metadata") or {}).get("model") == "claude-haiku-4-5"

    @pytest.mark.asyncio
    async def test_retry_explicit_model_override_wins(self, manager: DetachedSubagentManager, conv_id: str) -> None:
        """Explicit model=... on retry overrides the original (even model=None clears it)."""
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(error="transient"),
        ):
            result = manager.start(
                conv_id,
                "test",
                model="claude-haiku-4-5",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        captured_models: list[Any] = []

        async def _capture(*args: Any, **kwargs: Any) -> dict[str, Any]:
            captured_models.append(kwargs.get("model"))
            return _mock_run_subagent_result()

        with patch("anteroom.tools.subagent._run_subagent", new_callable=AsyncMock, side_effect=_capture):
            manager.retry(
                result["run_id"],
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
                model="claude-sonnet-4-6",
            )
            await asyncio.sleep(0.1)

        assert captured_models == ["claude-sonnet-4-6"]


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


class TestDescriptionField:
    """Tests for the optional description field on detached runs (#1461)."""

    @pytest.mark.asyncio
    async def test_start_persists_description_in_metadata(
        self, manager: DetachedSubagentManager, db: Any, conv_id: str
    ) -> None:
        """description='Review test gaps' → stored in metadata_json."""
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            result = manager.start(
                conv_id,
                "do something",
                description="Review test gaps",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        run = manager.get_run(result["run_id"])
        assert run is not None
        meta = run.get("metadata") or {}
        assert meta.get("description") == "Review test gaps"

    @pytest.mark.asyncio
    async def test_start_without_description_persists_none(
        self, manager: DetachedSubagentManager, db: Any, conv_id: str
    ) -> None:
        """No description → metadata has no description key or None."""
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            result = manager.start(
                conv_id,
                "do something",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        run = manager.get_run(result["run_id"])
        assert run is not None
        meta = run.get("metadata") or {}
        assert meta.get("description") is None

    @pytest.mark.asyncio
    async def test_retry_preserves_description_from_original(
        self, manager: DetachedSubagentManager, db: Any, conv_id: str
    ) -> None:
        """Retry of a run that had a description carries it forward."""
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(error="boom"),
        ):
            result = manager.start(
                conv_id,
                "do something",
                description="My task label",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        original_id = result["run_id"]
        run = manager.get_run(original_id)
        assert run is not None
        assert run["status"] == "failed"

        ai = MagicMock()
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            retry_result = manager.retry(
                original_id,
                ai_service=ai,
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        new_run = manager.get_run(retry_result["run_id"])
        assert new_run is not None
        meta = new_run.get("metadata") or {}
        assert meta.get("description") == "My task label"

    @pytest.mark.asyncio
    async def test_retry_without_original_description_falls_back(
        self, manager: DetachedSubagentManager, db: Any, conv_id: str
    ) -> None:
        """Retry of a run without description gracefully has no description."""
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(error="boom"),
        ):
            result = manager.start(
                conv_id,
                "do something",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        original_id = result["run_id"]

        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            retry_result = manager.retry(
                original_id,
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        new_run = manager.get_run(retry_result["run_id"])
        assert new_run is not None
        meta = new_run.get("metadata") or {}
        assert meta.get("description") is None

    @pytest.mark.asyncio
    async def test_retry_completion_sse_includes_description(
        self, manager: DetachedSubagentManager, event_bus: AsyncMock, db: Any, conv_id: str
    ) -> None:
        """agent_run_completed SSE event for a retry MUST include description (#1461).

        Regression: the retry path previously built the SSE payload inline and
        omitted description, causing the web chip to fall back to summary instead
        of the stable label carried forward from the original run.
        """
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(error="boom"),
        ):
            result = manager.start(
                conv_id,
                "do something",
                description="retry label",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        original_id = result["run_id"]
        event_bus.publish.reset_mock()

        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            manager.retry(original_id, ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        completed_calls = [
            c[0][1] for c in event_bus.publish.call_args_list if c[0][1].get("type") == "agent_run_completed"
        ]
        assert completed_calls, "agent_run_completed was not published for retry"
        payload = completed_calls[-1]["data"]
        assert payload.get("description") == "retry label", (
            f"retry agent_run_completed must carry description; got {payload!r}"
        )

    @pytest.mark.asyncio
    async def test_retry_completion_sse_omits_description_when_original_had_none(
        self, manager: DetachedSubagentManager, event_bus: AsyncMock, db: Any, conv_id: str
    ) -> None:
        """agent_run_completed SSE event for a retry omits description when original had none."""
        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(error="boom"),
        ):
            result = manager.start(
                conv_id,
                "do something",
                ai_service=MagicMock(),
                tool_registry=MagicMock(),
            )
            await asyncio.sleep(0.1)

        original_id = result["run_id"]
        event_bus.publish.reset_mock()

        with patch(
            "anteroom.tools.subagent._run_subagent",
            new_callable=AsyncMock,
            return_value=_mock_run_subagent_result(),
        ):
            manager.retry(original_id, ai_service=MagicMock(), tool_registry=MagicMock())
            await asyncio.sleep(0.1)

        completed_calls = [
            c[0][1] for c in event_bus.publish.call_args_list if c[0][1].get("type") == "agent_run_completed"
        ]
        assert completed_calls, "agent_run_completed was not published for retry"
        payload = completed_calls[-1]["data"]
        assert "description" not in payload, (
            f"description must not appear in retry SSE payload when original had none; got {payload!r}"
        )


class TestGetRunLabel:
    """Tests for the get_run_label() storage helper (#1461)."""

    def test_get_run_label_prefers_description(self) -> None:
        """Run with both title + metadata description → returns description."""
        from anteroom.services.storage import get_run_label

        run = {
            "id": "abc",
            "title": "do something useful and long",
            "metadata": {"description": "My concise label", "prompt": "do something useful and long"},
        }
        assert get_run_label(run) == "My concise label"

    def test_get_run_label_falls_back_to_title(self) -> None:
        """Run with no description → returns title."""
        from anteroom.services.storage import get_run_label

        run = {
            "id": "abc",
            "title": "prompt derived title",
            "metadata": {"prompt": "prompt derived title"},
        }
        assert get_run_label(run) == "prompt derived title"

    def test_get_run_label_empty_description_falls_back(self) -> None:
        """Empty description in metadata → returns title."""
        from anteroom.services.storage import get_run_label

        run = {
            "id": "abc",
            "title": "prompt derived",
            "metadata": {"description": "", "prompt": "prompt derived"},
        }
        assert get_run_label(run) == "prompt derived"

    def test_get_run_label_no_metadata(self) -> None:
        """Run with no metadata → returns title."""
        from anteroom.services.storage import get_run_label

        run = {"id": "abc", "title": "bare title"}
        assert get_run_label(run) == "bare title"

    def test_get_run_label_metadata_as_json_string(self) -> None:
        """metadata stored as JSON string is parsed correctly."""
        import json

        from anteroom.services.storage import get_run_label

        run = {
            "id": "abc",
            "title": "fallback title",
            "metadata": json.dumps({"description": "Parsed label"}),
        }
        assert get_run_label(run) == "Parsed label"
