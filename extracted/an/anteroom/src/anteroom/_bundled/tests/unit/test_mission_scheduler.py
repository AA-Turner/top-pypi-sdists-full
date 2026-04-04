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


class TestSessionVisibility:
    @pytest.mark.asyncio
    async def test_pending_session_items_are_not_launched(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter()
        registry.register("test", adapter)
        session = ms.create_session(db, title="pending", status="pending")
        item = ms.create_item(db, session_id=session["id"], summary="task", adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "pending"
        adapter.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_active_session_items_are_launched(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter()
        registry.register("test", adapter)
        _session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        refreshed = ms.get_item(db, item["id"])
        assert refreshed is not None
        assert refreshed["status"] == "completed"
        adapter.create.assert_called_once()


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
# Phase B — attempt_number derivation
# ---------------------------------------------------------------------------


class TestAttemptNumberDerivation:
    @pytest.mark.asyncio
    async def test_first_launch_attempt_number_is_1(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(create_status=AdapterStatus(state="completed", summary="ok", adapter_ref="ref-1"))
        registry.register("test", adapter)
        _session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        execs = ms.list_executions_by_item(db, item["id"])
        assert len(execs) == 1
        assert execs[0]["attempt_number"] == 1

    @pytest.mark.asyncio
    async def test_retry_launch_increments_attempt_number(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(create_status=AdapterStatus(state="completed", summary="ok", adapter_ref="ref-2"))
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        # Simulate a previous failed execution
        ms.create_execution(db, item_id=item["id"], attempt_number=1, status="failed")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        execs = ms.list_executions_by_item(db, item["id"])
        assert len(execs) == 2
        assert execs[1]["attempt_number"] == 2

    @pytest.mark.asyncio
    async def test_multiple_retries_increment_correctly(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(create_status=AdapterStatus(state="completed", summary="ok", adapter_ref="ref-3"))
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        ms.create_execution(db, item_id=item["id"], attempt_number=1, status="failed")
        ms.create_execution(db, item_id=item["id"], attempt_number=2, status="failed")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()

        execs = ms.list_executions_by_item(db, item["id"])
        assert len(execs) == 3
        assert execs[2]["attempt_number"] == 3


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


class TestStaleRecovery:
    """Tests for _handle_stale_recovery (#1257)."""

    @pytest.mark.asyncio
    async def test_poll_emits_stale_event(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="pending", summary="started", adapter_ref="ref-1"),
            status_status=AdapterStatus(state="running", summary="stale_heartbeat_reclaimed"),
        )
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        # Launch
        await worker.run_once()
        # Poll — adapter reports running with stale_heartbeat summary
        await worker.run_once()

        events = ms.list_events(db, session_id=session["id"])
        stale_events = [e for e in events if e["event_type"] == "item_stale_recovered"]
        assert len(stale_events) >= 1

    @pytest.mark.asyncio
    async def test_recover_item_emits_stale_event(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="pending", summary="started", adapter_ref="ref-1"),
            status_status=AdapterStatus(state="running", summary="stale_heartbeat in adapter"),
        )
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        # Launch
        await worker.run_once()
        # Simulate startup recovery
        await worker._recover_on_startup()

        events = ms.list_events(db, session_id=session["id"])
        stale_events = [e for e in events if e["event_type"] == "item_stale_recovered"]
        assert len(stale_events) >= 1

    @pytest.mark.asyncio
    async def test_no_stale_event_without_marker(self, db: Any, registry: MissionAdapterRegistry) -> None:
        adapter = _make_adapter(
            create_status=AdapterStatus(state="pending", summary="started", adapter_ref="ref-1"),
            status_status=AdapterStatus(state="running", summary="all good"),
        )
        registry.register("test", adapter)
        session, item = _active_session_with_item(db, adapter_type="test")

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)
        await worker.run_once()
        await worker.run_once()

        events = ms.list_events(db, session_id=session["id"])
        stale_events = [e for e in events if e["event_type"] == "item_stale_recovered"]
        assert len(stale_events) == 0


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


# ---------------------------------------------------------------------------
# Phase D — External reality reconciliation (#1306)
# ---------------------------------------------------------------------------


def _setup_failed_workflow_item(
    db: Any,
    *,
    issue_number: int | None = 42,
    adapter_type: str = "workflow",
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None]:
    """Create a session with a failed workflow-backed item.

    Returns (session, item, workflow_run | None).
    """
    from anteroom.services import workflow_storage as ws

    session = ms.create_session(db, title="test", status="active")
    item = ms.create_item(
        db,
        session_id=session["id"],
        summary="Task",
        adapter_type=adapter_type,
        status="active",
    )

    run: dict[str, Any] | None = None
    if adapter_type == "workflow":
        inputs = {"issue_number": issue_number} if issue_number is not None else {}
        run = ws.create_workflow_run(
            db,
            workflow_id="test-wf",
            workflow_version="1",
            target_kind="issue",
            target_ref=str(issue_number or 0),
            inputs=inputs,
        )
        exc = ms.create_execution(
            db,
            item_id=item["id"],
            attempt_number=1,
            status="failed",
            adapter_ref=run["id"],
        )
        ms.update_execution(db, exc["id"], finished_at="2025-01-01T00:00:00Z")
    else:
        ms.create_execution(
            db,
            item_id=item["id"],
            attempt_number=1,
            status="failed",
        )

    # Move item to failed
    db.execute("UPDATE mission_items SET status = 'failed' WHERE id = ?", (item["id"],))
    db.commit()

    return session, ms.get_item(db, item["id"]), run  # type: ignore[return-value]


class TestExternalReconciliation:
    """Phase D external reality reconciliation (#1306)."""

    @pytest.mark.asyncio
    async def test_finalize_reconciles_failed_item_when_issue_closed(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        from unittest.mock import patch

        session, item, _ = _setup_failed_workflow_item(db, issue_number=1180)
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)

        with patch(
            "anteroom.services.external_checks.check_external_completion",
            return_value=(True, "Issue #1180 closed externally"),
        ):
            await worker.run_once()

        updated = ms.get_item(db, item["id"])
        assert updated is not None
        assert updated["status"] == "completed"
        updated_session = ms.get_session(db, session["id"])
        assert updated_session is not None
        assert updated_session["status"] == "completed"

    @pytest.mark.asyncio
    async def test_finalize_reconciles_failed_item_when_pr_merged(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        """Mirrors the #1180/#1305 acceptance scenario."""
        from unittest.mock import patch

        session, item, _ = _setup_failed_workflow_item(db, issue_number=1180)
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)

        with patch(
            "anteroom.services.external_checks.check_external_completion",
            return_value=(True, "Issue #1180 closed; merged closing PR(s): #1305"),
        ):
            await worker.run_once()

        updated = ms.get_item(db, item["id"])
        assert updated is not None
        assert updated["status"] == "completed"
        events = ms.list_events(db, session["id"], event_type="item_reconciled")
        assert len(events) == 1
        assert "#1305" in events[0]["detail"]["reason"]

    @pytest.mark.asyncio
    async def test_finalize_skips_external_check_when_no_issue_number(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        from unittest.mock import patch

        session, item, _ = _setup_failed_workflow_item(db, issue_number=None)
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)

        with patch(
            "anteroom.services.external_checks.check_external_completion",
        ) as mock_check:
            await worker.run_once()
            mock_check.assert_not_called()

        updated = ms.get_item(db, item["id"])
        assert updated is not None
        assert updated["status"] == "failed"

    @pytest.mark.asyncio
    async def test_finalize_skips_external_check_for_non_workflow_adapter(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        from unittest.mock import patch

        adapter = _make_adapter(
            status_status=AdapterStatus(state="failed", summary="fail"),
        )
        registry.register("noop", adapter)
        session, item, _ = _setup_failed_workflow_item(db, adapter_type="noop")
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)

        with patch(
            "anteroom.services.external_checks.check_external_completion",
        ) as mock_check:
            await worker.run_once()
            mock_check.assert_not_called()

    @pytest.mark.asyncio
    async def test_finalize_session_completes_after_external_reconciliation(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        from unittest.mock import patch

        session, item, _ = _setup_failed_workflow_item(db, issue_number=42)
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)

        with patch(
            "anteroom.services.external_checks.check_external_completion",
            return_value=(True, "Issue #42 closed externally"),
        ):
            await worker.run_once()

        updated_session = ms.get_session(db, session["id"])
        assert updated_session is not None
        assert updated_session["status"] == "completed"
        session_events = ms.list_events(db, session["id"], event_type="session_completed")
        assert len(session_events) == 1

    @pytest.mark.asyncio
    async def test_finalize_session_still_fails_when_external_check_returns_false(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        from unittest.mock import patch

        session, item, _ = _setup_failed_workflow_item(db, issue_number=42)
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)

        with patch(
            "anteroom.services.external_checks.check_external_completion",
            return_value=(False, None),
        ):
            await worker.run_once()

        updated = ms.get_item(db, item["id"])
        assert updated is not None
        assert updated["status"] == "failed"
        updated_session = ms.get_session(db, session["id"])
        assert updated_session is not None
        assert updated_session["status"] == "failed"

    @pytest.mark.asyncio
    async def test_finalize_handles_external_check_failure_gracefully(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        from unittest.mock import patch

        session, item, _ = _setup_failed_workflow_item(db, issue_number=42)
        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)

        with patch(
            "anteroom.services.external_checks.check_external_completion",
            side_effect=RuntimeError("gh not found"),
        ):
            await worker.run_once()

        # Graceful degradation: item stays failed, no crash
        updated = ms.get_item(db, item["id"])
        assert updated is not None
        assert updated["status"] == "failed"

    @pytest.mark.asyncio
    async def test_finalize_reconciles_item_with_live_execution(
        self, db: Any, registry: MissionAdapterRegistry
    ) -> None:
        """force_reconcile_item cancels a live execution before reconciling."""
        from unittest.mock import patch

        session = ms.create_session(db, title="test", status="active")
        item = ms.create_item(
            db,
            session_id=session["id"],
            summary="Task",
            adapter_type="workflow",
            status="active",
        )

        from anteroom.services import workflow_storage as ws

        run = ws.create_workflow_run(
            db,
            workflow_id="test-wf",
            workflow_version="1",
            target_kind="issue",
            target_ref="42",
            inputs={"issue_number": 42},
        )
        ms.create_execution(
            db,
            item_id=item["id"],
            attempt_number=1,
            status="running",
            adapter_ref=run["id"],
        )
        # Item is active with a running execution — but issue is closed.
        # force_reconcile_item should cancel the execution first.
        db.execute("UPDATE mission_items SET status = 'failed' WHERE id = ?", (item["id"],))
        db.commit()

        worker = MissionSchedulerWorker(db=db, adapter_registry=registry)

        with patch(
            "anteroom.services.external_checks.check_external_completion",
            return_value=(True, "Issue #42 closed externally"),
        ):
            await worker.run_once()

        updated = ms.get_item(db, item["id"])
        assert updated is not None
        assert updated["status"] == "completed"
