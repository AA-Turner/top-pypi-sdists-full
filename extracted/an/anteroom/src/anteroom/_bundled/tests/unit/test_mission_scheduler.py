"""Unit tests for MissionSchedulerWorker (#1045)."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest

from anteroom.db import init_db
from anteroom.services import mission_storage as ms
from anteroom.services.mission_adapters import AdapterStatus, MissionAdapterRegistry
from anteroom.services.mission_scheduler import MissionSchedulerWorker

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    return init_db(tmp_path / "test.db")


@pytest.fixture()
def registry() -> MissionAdapterRegistry:
    return MissionAdapterRegistry()


def _make_adapter(
    create_status: AdapterStatus | None = None,
    status_status: AdapterStatus | None = None,
) -> AsyncMock:
    adapter = AsyncMock()
    adapter.create.return_value = create_status or AdapterStatus(state="completed", summary="done", adapter_ref="ref-1")
    adapter.status.return_value = status_status or AdapterStatus(state="completed", summary="done")
    adapter.cancel.return_value = AdapterStatus(state="cancelled")
    return adapter


def _active_session_with_item(
    db: Any,
    *,
    adapter_type: str = "test",
    lane: str | None = None,
    concurrency_group: str | None = None,
    hold_requested: bool = False,
    lane_limits: dict[str, int] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    session = ms.create_session(db, title="s", status="active", lane_limits=lane_limits)
    item = ms.create_item(
        db,
        session_id=session["id"],
        summary="task",
        adapter_type=adapter_type,
        lane=lane,
        concurrency_group=concurrency_group,
        hold_requested=hold_requested,
    )
    return session, item


# ---------------------------------------------------------------------------
# Phase A — Eligibility
# ---------------------------------------------------------------------------


class TestEligibility:
    @pytest.mark.asyncio
    async def test_deps_satisfied_item_is_eligible(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter()
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active")
        dep = ms.create_item(db, session_id=session["id"], summary="dep", status="completed", adapter_type="test")
        item = ms.create_item(db, session_id=session["id"], summary="child", adapter_type="test")
        ms.add_dependency(db, item_id=item["id"], depends_on_id=dep["id"])

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        # Noop adapter returns completed, so item goes to completed (create-time terminal)
        assert refreshed["status"] == "completed"

    @pytest.mark.asyncio
    async def test_deps_unsatisfied_item_not_launched(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter()
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active")
        # dep uses a different adapter ("other") so we can verify child wasn't launched via "test"
        dep = ms.create_item(db, session_id=session["id"], summary="dep", adapter_type="other")  # still pending
        item = ms.create_item(db, session_id=session["id"], summary="child", adapter_type="test")
        ms.add_dependency(db, item_id=item["id"], depends_on_id=dep["id"])

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        # Child should still be pending because dep is not completed
        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "pending"
        # Dep was eligible but its adapter ("other") is not registered, so it got blocked
        # The child's adapter should never have been called
        adapter.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_held_item_not_launched(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter()
        registry.register("test", adapter)
        _active_session_with_item(db, adapter_type="test", hold_requested=True)

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        adapter.create.assert_not_called()


# ---------------------------------------------------------------------------
# Phase B — Launch (create-time branching)
# ---------------------------------------------------------------------------


class TestLaunchCreateTimeTerminal:
    @pytest.mark.asyncio
    async def test_create_returns_completed_item_directly_completed(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        adapter = _make_adapter(create_status=AdapterStatus(state="completed", summary="instant", adapter_ref="ref-c"))
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "completed"
        # Should never have been "active"
        events = ms.list_events(db, session["id"], item_id=item["id"])
        event_types = [e["event_type"] for e in events]
        assert "item_launched" not in event_types
        assert "item_completed" in event_types

    @pytest.mark.asyncio
    async def test_create_returns_failed_item_directly_failed(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(create_status=AdapterStatus(state="failed", summary="boom", adapter_ref="ref-f"))
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "failed"
        events = ms.list_events(db, session["id"], item_id=item["id"])
        event_types = [e["event_type"] for e in events]
        assert "item_launched" not in event_types
        assert "item_failed" in event_types

    @pytest.mark.asyncio
    async def test_create_returns_cancelled_item_directly_cancelled(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        adapter = _make_adapter(create_status=AdapterStatus(state="cancelled", summary="nope", adapter_ref="ref-x"))
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "dropped"  # "cancelled" maps to "dropped" for items


class TestLaunchCreateTimeInFlight:
    @pytest.mark.asyncio
    async def test_create_returns_pending_item_becomes_active(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="pending", summary="queued", adapter_ref="ref-p"),
            status_status=AdapterStatus(state="pending"),
        )
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "active"
        events = ms.list_events(db, session["id"], item_id=item["id"])
        event_types = [e["event_type"] for e in events]
        assert "item_launched" in event_types

    @pytest.mark.asyncio
    async def test_create_returns_running_item_becomes_active(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="running", summary="going", adapter_ref="ref-r"),
            status_status=AdapterStatus(state="running"),
        )
        registry.register("test", adapter)
        _session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "active"

    @pytest.mark.asyncio
    async def test_create_returns_unrecognized_state_treated_as_inflight(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="mystery", summary="???", adapter_ref="ref-m"),
            status_status=AdapterStatus(state="running"),
        )
        registry.register("test", adapter)
        _session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "active"


class TestSessionContextProvenance:
    @pytest.mark.asyncio
    async def test_context_carries_spec_provenance(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="pending", adapter_ref="ref-p"),
            status_status=AdapterStatus(state="running"),
        )
        registry.register("test", adapter)

        session = ms.create_session(
            db,
            title="S",
            status="active",
            source_fqn="@ns/spec/auth",
            referenced_artifacts=[{"fqn": "@ns/spec/auth", "version": 2}],
        )
        ms.create_item(
            db,
            session_id=session["id"],
            summary="Build auth",
            adapter_type="test",
            adapter_config={"spec_fqn": "@ns/spec/auth", "task_id": "t1"},
        )

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        adapter.create.assert_called_once()
        call_kwargs = adapter.create.call_args.kwargs
        ctx = call_kwargs["context"]
        assert ctx["spec_fqn"] == "@ns/spec/auth"
        assert ctx["task_id"] == "t1"
        assert ctx["task_summary"] == "Build auth"
        assert ctx["artifact_refs"] == [{"fqn": "@ns/spec/auth", "version": 2}]


class TestAdapterNotFound:
    @pytest.mark.asyncio
    async def test_missing_adapter_blocks_item(self, db: Any, registry: MissionAdapterRegistry) -> None:
        # No adapter registered for "missing"
        session, item = _active_session_with_item(db, adapter_type="missing")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "blocked"
        events = ms.list_events(db, session["id"], item_id=item["id"])
        assert any(e["event_type"] == "adapter_not_found" for e in events)


# ---------------------------------------------------------------------------
# Phase C — Poll active executions
# ---------------------------------------------------------------------------


class TestPollActive:
    @pytest.mark.asyncio
    async def test_poll_completed_item_completed(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="running", adapter_ref="ref-a"),
        )
        # First status call (Phase C of run 1) returns running; second returns completed
        adapter.status.side_effect = [
            AdapterStatus(state="running"),
            AdapterStatus(state="completed", summary="all done"),
        ]
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        # First run: launch -> active, poll -> still running
        await worker.run_once()
        assert ms.get_item(db, item["id"])["status"] == "active"  # type: ignore[index]

        # Second run: poll -> completed
        await worker.run_once()
        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "completed"

    @pytest.mark.asyncio
    async def test_poll_failed_item_failed(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="running", adapter_ref="ref-b"),
        )
        adapter.status.side_effect = [
            AdapterStatus(state="running"),
            AdapterStatus(state="failed", summary="error"),
        ]
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()  # launch + poll (still running)
        await worker.run_once()  # poll (failed)

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "failed"


# ---------------------------------------------------------------------------
# Hold semantics
# ---------------------------------------------------------------------------


class TestHoldSemantics:
    @pytest.mark.asyncio
    async def test_hold_at_boundary_active_becomes_blocked(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="running", adapter_ref="ref-h"),
        )
        # First status call returns running, second returns completed
        adapter.status.side_effect = [
            AdapterStatus(state="running"),
            AdapterStatus(state="completed", summary="done"),
        ]
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()  # launch -> active, poll -> still running
        assert ms.get_item(db, item["id"])["status"] == "active"  # type: ignore[index]

        # Set hold after launch
        ms.update_item(db, item["id"], hold_requested=1)

        await worker.run_once()  # poll -> terminal but held -> blocked
        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "blocked"
        events = ms.list_events(db, session["id"], item_id=item["id"])
        assert any(e["event_type"] == "item_held_at_boundary" for e in events)

    @pytest.mark.asyncio
    async def test_hold_prevents_launch(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter()
        registry.register("test", adapter)
        _session, item = _active_session_with_item(db, adapter_type="test", hold_requested=True)

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "pending"
        adapter.create.assert_not_called()


# ---------------------------------------------------------------------------
# Phase D — Session completion
# ---------------------------------------------------------------------------


class TestSessionCompletion:
    @pytest.mark.asyncio
    async def test_all_completed_session_completed(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(create_status=AdapterStatus(state="completed", summary="ok", adapter_ref="ref-1"))
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active")
        ms.create_item(db, session_id=session["id"], summary="a", adapter_type="test")
        ms.create_item(db, session_id=session["id"], summary="b", adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_session(db, session["id"])
        assert refreshed is not None
        assert refreshed["status"] == "completed"

    @pytest.mark.asyncio
    async def test_item_failed_session_failed(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(create_status=AdapterStatus(state="failed", summary="nope", adapter_ref="ref-f"))
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active")
        ms.create_item(db, session_id=session["id"], summary="a", adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_session(db, session["id"])
        assert refreshed is not None
        assert refreshed["status"] == "failed"


# ---------------------------------------------------------------------------
# Lane limits and concurrency groups
# ---------------------------------------------------------------------------


class TestLaneLimits:
    @pytest.mark.asyncio
    async def test_lane_limit_prevents_excess_launches(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="running", adapter_ref="ref-l"),
            status_status=AdapterStatus(state="running"),
        )
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active", lane_limits={"ci": 1})
        ms.create_item(db, session_id=session["id"], summary="a", adapter_type="test", lane="ci")
        item_b = ms.create_item(db, session_id=session["id"], summary="b", adapter_type="test", lane="ci")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        # Only one should be active; the other stays pending
        refreshed_b = ms.get_item(db, item_b["id"])
        assert refreshed_b is not None
        assert refreshed_b["status"] == "pending"
        assert adapter.create.call_count == 1

    @pytest.mark.asyncio
    async def test_concurrency_group_limit(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="running", adapter_ref="ref-cg"),
            status_status=AdapterStatus(state="running"),
        )
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active")
        ms.create_item(db, session_id=session["id"], summary="a", adapter_type="test", concurrency_group="deploy")
        item_b = ms.create_item(
            db, session_id=session["id"], summary="b", adapter_type="test", concurrency_group="deploy"
        )

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed_b = ms.get_item(db, item_b["id"])
        assert refreshed_b is not None
        assert refreshed_b["status"] == "pending"
        assert adapter.create.call_count == 1


# ---------------------------------------------------------------------------
# Startup recovery
# ---------------------------------------------------------------------------


class TestStartupRecovery:
    @pytest.mark.asyncio
    async def test_recovery_terminal_item_reconciled(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            status_status=AdapterStatus(state="completed", summary="done"),
        )
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active")
        item = ms.create_item(db, session_id=session["id"], summary="stuck", adapter_type="test", status="active")
        ms.create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref="ref-r")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker._recover_on_startup()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "completed"
        events = ms.list_events(db, session["id"], item_id=item["id"])
        assert any(e["event_type"] == "recovery_reconciled" for e in events)

    @pytest.mark.asyncio
    async def test_recovery_unknown_state_item_failed(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            status_status=AdapterStatus(state="unknown_garbage"),
        )
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active")
        item = ms.create_item(db, session_id=session["id"], summary="stuck", adapter_type="test", status="active")
        ms.create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref="ref-r")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker._recover_on_startup()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "failed"

    @pytest.mark.asyncio
    async def test_recovery_no_execution_item_failed(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter()
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active")
        item = ms.create_item(db, session_id=session["id"], summary="stuck", adapter_type="test", status="active")
        # No execution record

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker._recover_on_startup()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "failed"

    @pytest.mark.asyncio
    async def test_recovery_still_running_stays_active(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            status_status=AdapterStatus(state="running"),
        )
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active")
        item = ms.create_item(db, session_id=session["id"], summary="running", adapter_type="test", status="active")
        ms.create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref="ref-r")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker._recover_on_startup()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "active"

    @pytest.mark.asyncio
    async def test_recovery_status_exception_is_transient(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter()
        adapter.status = AsyncMock(side_effect=RuntimeError("network down"))
        registry.register("test", adapter)
        session = ms.create_session(db, title="s", status="active")
        item = ms.create_item(db, session_id=session["id"], summary="stuck", adapter_type="test", status="active")
        ms.create_execution(db, item_id=item["id"], attempt_number=1, status="running", adapter_ref="ref-t")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker._recover_on_startup()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "active"  # stays active, not failed


# ---------------------------------------------------------------------------
# Backoff
# ---------------------------------------------------------------------------


class TestBackoff:
    def test_consecutive_failures_increase_interval(self, db: Any, registry: MissionAdapterRegistry) -> None:
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry, poll_interval=5.0)
        assert worker._current_interval == 5.0

        worker._apply_backoff()
        assert worker._current_interval == 10.0  # 5 * 2^1
        assert worker._consecutive_failures == 1

        worker._apply_backoff()
        assert worker._current_interval == 20.0  # 5 * 2^2
        assert worker._consecutive_failures == 2

    def test_backoff_caps_at_max(self, db: Any, registry: MissionAdapterRegistry) -> None:
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry, poll_interval=5.0)
        for _ in range(20):
            worker._apply_backoff()
        assert worker._current_interval <= 300.0

    def test_reset_backoff(self, db: Any, registry: MissionAdapterRegistry) -> None:
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry, poll_interval=5.0)
        worker._apply_backoff()
        worker._apply_backoff()
        worker._reset_backoff()
        assert worker._consecutive_failures == 0
        assert worker._current_interval == 5.0


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------


class TestIdempotency:
    @pytest.mark.asyncio
    async def test_run_once_twice_no_state_change(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(create_status=AdapterStatus(state="completed", summary="done", adapter_ref="ref-i"))
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()
        # Session should now be completed
        assert ms.get_session(db, session["id"])["status"] == "completed"  # type: ignore[index]

        # Second run — nothing should change, no errors
        call_count_before = adapter.create.call_count
        await worker.run_once()
        assert adapter.create.call_count == call_count_before

    @pytest.mark.asyncio
    async def test_empty_sessions_no_error(self, db: Any, registry: MissionAdapterRegistry) -> None:
        # No sessions at all
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()  # Should not raise


# ---------------------------------------------------------------------------
# Start / stop lifecycle
# ---------------------------------------------------------------------------


class TestLifecycle:
    @pytest.mark.asyncio
    async def test_start_stop(self, db: Any, registry: MissionAdapterRegistry) -> None:
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry, poll_interval=0.1)
        worker.start()
        # Yield to the event loop so run_forever actually starts
        await asyncio.sleep(0)
        assert worker.running is True
        worker.stop()
        assert worker.running is False
