"""Tests for workflow resume, heartbeat, crash recovery, and cancel."""

from __future__ import annotations

import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services import workflow_hooks
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import (
    acquire_lock,
    cancel_pending_approval_requests,
    create_approval_request,
    create_human_decision,
    create_workflow_event,
    create_workflow_run,
    create_workflow_step,
    expire_pending_decisions,
    find_running_steps,
    find_stale_runs,
    get_lock,
    get_workflow_run,
    list_completed_step_ids,
    list_workflow_events,
    list_workflow_steps,
    release_lock,
    reset_steps_from,
    update_workflow_run,
    update_workflow_step,
)

GENERIC_WORKFLOW = """\
kind: workflow
id: test_resume
version: 0.1.0
inputs: {}
steps:
  - id: step_a
    type: runner
    runner: shell
    command: "echo step A"
    timeout: 10
  - id: step_b
    type: runner
    runner: shell
    command: "echo step B"
    timeout: 10
  - id: step_c
    type: runner
    runner: shell
    command: "echo step C"
    timeout: 10
"""

GATE_TOGGLE_WORKFLOW = """\
kind: workflow
id: test_gate_toggle
version: 0.1.0
inputs: {}
steps:
  - id: step_a
    type: runner
    runner: shell
    command: "echo step A"
    timeout: 10
  - id: gate_toggle
    type: gate
    condition: toggle_gate
    if_false: gate_not_ready
  - id: step_b
    type: runner
    runner: shell
    command: "echo step B"
    timeout: 10
"""

# Mutable toggle for gate condition
_gate_toggle_value = False


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


@pytest.fixture()
def engine(db: Any) -> WorkflowEngine:
    config = WorkflowConfig(heartbeat_interval=1, stale_threshold=2)
    registry = create_default_registry()
    return WorkflowEngine(db, config, registry)


@pytest.fixture(autouse=True)
def _register_test_gates():
    global _gate_toggle_value
    _gate_toggle_value = False

    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    async def toggle_gate(run: Any, step: Any, inputs: Any) -> bool:
        return _gate_toggle_value

    register_gate_condition("always_pass", always_pass)
    register_gate_condition("toggle_gate", toggle_gate)
    yield


# ---------------------------------------------------------------------------
# Storage: find_stale_runs, find_running_steps, list_completed_step_ids
# ---------------------------------------------------------------------------


class TestStaleRunDetection:
    def test_find_stale_runs_with_old_heartbeat(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        old_time = (datetime.now(timezone.utc) - timedelta(seconds=120)).isoformat()
        update_workflow_run(db, run["id"], status="running", heartbeat_at=old_time)

        stale = find_stale_runs(db, stale_threshold_seconds=60)
        assert len(stale) == 1
        assert stale[0]["id"] == run["id"]

    def test_find_stale_runs_ignores_fresh(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        fresh_time = datetime.now(timezone.utc).isoformat()
        update_workflow_run(db, run["id"], status="running", heartbeat_at=fresh_time)

        stale = find_stale_runs(db, stale_threshold_seconds=60)
        assert len(stale) == 0

    def test_find_stale_runs_null_heartbeat(self, db: Any) -> None:
        """Null heartbeat_at is treated as stale."""
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        update_workflow_run(db, run["id"], status="running")

        stale = find_stale_runs(db, stale_threshold_seconds=60)
        assert len(stale) == 1

    def test_find_stale_runs_ignores_non_running(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        update_workflow_run(db, run["id"], status="paused")

        stale = find_stale_runs(db, stale_threshold_seconds=60)
        assert len(stale) == 0


class TestFindRunningSteps:
    def test_finds_running_steps(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        step = create_workflow_step(
            db,
            run_id=run["id"],
            step_id="s1",
            step_type="runner",
        )
        update_workflow_step(db, step["id"], status="running")
        running = find_running_steps(db, run["id"])
        assert len(running) == 1
        assert running[0]["step_id"] == "s1"

    def test_ignores_completed_steps(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        step = create_workflow_step(
            db,
            run_id=run["id"],
            step_id="s1",
            step_type="runner",
        )
        update_workflow_step(db, step["id"], status="completed")
        running = find_running_steps(db, run["id"])
        assert len(running) == 0


class TestListCompletedStepIds:
    def test_returns_completed_ids(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        s1 = create_workflow_step(db, run_id=run["id"], step_id="s1", step_type="runner")
        s2 = create_workflow_step(db, run_id=run["id"], step_id="s2", step_type="runner")
        update_workflow_step(db, s1["id"], status="completed")
        update_workflow_step(db, s2["id"], status="running")

        completed = list_completed_step_ids(db, run["id"])
        assert completed == {"s1"}


# ---------------------------------------------------------------------------
# Engine: recover_interrupted_runs
# ---------------------------------------------------------------------------


class TestRecoverInterruptedRuns:
    @pytest.mark.asyncio
    async def test_marks_stale_runs_failed(self, db: Any, engine: WorkflowEngine) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        old_time = (datetime.now(timezone.utc) - timedelta(seconds=120)).isoformat()
        update_workflow_run(db, run["id"], status="running", heartbeat_at=old_time)
        acquire_lock(db, target_kind="task", target_ref="t1", run_id=run["id"])

        recovered = await engine.recover_interrupted_runs()
        assert len(recovered) == 1

        refreshed = get_workflow_run(db, run["id"])
        assert refreshed["status"] == "failed"
        assert refreshed["stop_reason"] == "stale_heartbeat_reclaimed"

    @pytest.mark.asyncio
    async def test_releases_locks(self, db: Any, engine: WorkflowEngine) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        old_time = (datetime.now(timezone.utc) - timedelta(seconds=120)).isoformat()
        update_workflow_run(db, run["id"], status="running", heartbeat_at=old_time)
        acquire_lock(db, target_kind="task", target_ref="t1", run_id=run["id"])

        await engine.recover_interrupted_runs()
        assert get_lock(db, target_kind="task", target_ref="t1") is None

    @pytest.mark.asyncio
    async def test_marks_running_steps_interrupted(self, db: Any, engine: WorkflowEngine) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        old_time = (datetime.now(timezone.utc) - timedelta(seconds=120)).isoformat()
        update_workflow_run(db, run["id"], status="running", heartbeat_at=old_time)
        acquire_lock(db, target_kind="task", target_ref="t1", run_id=run["id"])
        step = create_workflow_step(
            db,
            run_id=run["id"],
            step_id="active_step",
            step_type="runner",
        )
        update_workflow_step(db, step["id"], status="running")

        await engine.recover_interrupted_runs()

        steps = list_workflow_steps(db, run["id"])
        active = [s for s in steps if s["step_id"] == "active_step"]
        assert active[0]["status"] == "interrupted"
        assert active[0]["completed_at"] is not None

    @pytest.mark.asyncio
    async def test_emits_event(self, db: Any, engine: WorkflowEngine) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        old_time = (datetime.now(timezone.utc) - timedelta(seconds=120)).isoformat()
        update_workflow_run(db, run["id"], status="running", heartbeat_at=old_time)
        acquire_lock(db, target_kind="task", target_ref="t1", run_id=run["id"])

        await engine.recover_interrupted_runs()

        events = list_workflow_events(db, run["id"])
        failed_events = [e for e in events if e["event_type"] == "run_failed"]
        assert len(failed_events) == 1
        assert failed_events[0]["payload"]["reason"] == "stale_heartbeat_reclaimed"


# ---------------------------------------------------------------------------
# Engine: resume_run
# ---------------------------------------------------------------------------


class TestResumeRun:
    @pytest.mark.asyncio
    async def test_resume_skips_completed_steps(self, db: Any, engine: WorkflowEngine) -> None:
        """Resume skips completed steps and executes remaining."""
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        assert run["status"] == "completed"

        # Manually mark as paused to simulate resume scenario
        update_workflow_run(db, run["id"], status="paused", stop_reason="test")

        # Mark only step_a and step_b as completed in a way resume recognizes
        # (they're already completed from the initial run)
        completed = list_completed_step_ids(db, run["id"])
        assert "step_a" in completed
        assert "step_b" in completed
        assert "step_c" in completed

        # Resume — all steps already completed, should complete immediately
        result = await engine.resume_run(run["id"], defn)
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_resume_rejects_non_resumable(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        # Run is completed — not resumable
        with pytest.raises(ValueError, match="not resumable"):
            await engine.resume_run(run["id"], defn)

    @pytest.mark.asyncio
    async def test_resume_with_from_step_override(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        update_workflow_run(db, run["id"], status="paused", stop_reason="test", attempt_count=1)

        # Resume from step_c — skips step_a and step_b
        result = await engine.resume_run(run["id"], defn, from_step="step_c")
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_resume_invalid_from_step_raises(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        update_workflow_run(db, run["id"], status="paused", stop_reason="test", attempt_count=1)

        with pytest.raises(ValueError, match="not found in workflow"):
            await engine.resume_run(run["id"], defn, from_step="nonexistent")

    @pytest.mark.asyncio
    async def test_resume_emits_run_resumed_event(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        update_workflow_run(db, run["id"], status="paused", stop_reason="test", attempt_count=1)

        await engine.resume_run(run["id"], defn)

        events = list_workflow_events(db, run["id"])
        resumed = [e for e in events if e["event_type"] == "run_resumed"]
        assert len(resumed) == 1

    @pytest.mark.asyncio
    async def test_resume_does_not_redeliver_hooks_by_default(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(GENERIC_WORKFLOW)
        defn.notifications = {
            "hooks": [{"transport": "webhook", "url": "https://example.com/hook", "events": ["run_resumed"]}]
        }
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        update_workflow_run(db, run["id"], status="paused", stop_reason="test", attempt_count=1)

        delivered: list[tuple[str, dict[str, Any]]] = []

        async def _capture(url: str, payload: dict[str, Any], timeout: float = 5.0) -> None:
            delivered.append((url, payload))

        engine._definition_loader = SimpleNamespace(get=lambda workflow_id: defn)

        with patch.object(workflow_hooks, "deliver_webhook", new=AsyncMock(side_effect=_capture)):
            await engine.resume_run(run["id"], defn)
            await engine._drain_hooks()

        assert delivered == []

    @pytest.mark.asyncio
    async def test_resume_skips_non_resumed_hooks_during_rerun_by_default(
        self, db: Any, engine: WorkflowEngine
    ) -> None:
        defn = load_definition(GENERIC_WORKFLOW)
        defn.notifications = {
            "hooks": [{"transport": "webhook", "url": "https://example.com/hook", "events": ["run_started"]}]
        }
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        update_workflow_run(db, run["id"], status="paused", stop_reason="test", attempt_count=1)

        delivered: list[tuple[str, dict[str, Any]]] = []

        async def _capture(url: str, payload: dict[str, Any], timeout: float = 5.0) -> None:
            delivered.append((url, payload))

        engine._definition_loader = SimpleNamespace(get=lambda workflow_id: defn)

        with patch.object(workflow_hooks, "deliver_webhook", new=AsyncMock(side_effect=_capture)):
            await engine.resume_run(run["id"], defn)
            await engine._drain_hooks()

        assert delivered == []

    @pytest.mark.asyncio
    async def test_resume_redelivers_hooks_when_opted_in(self, db: Any, engine: WorkflowEngine) -> None:
        defn = load_definition(GENERIC_WORKFLOW)
        defn.notifications = {
            "hooks": [
                {
                    "transport": "webhook",
                    "url": "https://example.com/hook",
                    "events": ["run_resumed"],
                    "deliver_on_rerun": True,
                }
            ]
        }
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        update_workflow_run(db, run["id"], status="paused", stop_reason="test", attempt_count=1)

        delivered: list[tuple[str, dict[str, Any]]] = []
        original_publish_event = engine._publish_event

        async def _capture(url: str, payload: dict[str, Any], timeout: float = 5.0) -> None:
            delivered.append((url, payload))

        async def _capture_publish_event(
            run_id: str,
            event_type: str,
            payload: dict[str, Any] | None = None,
            *,
            definition: Any | None = None,
        ) -> None:
            event_payload = dict(payload or {})
            run_record = get_workflow_run(db, run_id)
            attempt = 1
            if run_record is not None:
                attempt = int(run_record.get("attempt_count") or 0) + 1
            event_payload["attempt"] = attempt
            await original_publish_event(
                run_id,
                event_type,
                event_payload,
                definition=(defn if definition is None else definition),
            )

        with patch.object(workflow_hooks, "deliver_webhook", new=AsyncMock(side_effect=_capture)):
            with patch.object(engine, "_publish_event", new=AsyncMock(side_effect=_capture_publish_event)):
                await engine.resume_run(run["id"], defn)
                await engine._drain_hooks()

        events = list_workflow_events(db, run["id"])
        resumed = [event for event in events if event["event_type"] == "run_resumed"]
        assert len(resumed) == 1
        resumed_payload = resumed[0].get("payload") or {}
        assert resumed_payload["prior_status"] == "paused"
        assert set(resumed_payload["skip_completed"]) == {"step_a", "step_b", "step_c"}

        assert len(delivered) == 1
        url, payload = delivered[0]
        assert url == "https://example.com/hook"
        assert payload["event_type"] == "run_resumed"
        assert payload["attempt"] == 2
        assert set(payload["skip_completed"]) == {"step_a", "step_b", "step_c"}
        assert payload["prior_status"] == "paused"

    @pytest.mark.asyncio
    async def test_resume_failed_run(self, db: Any, engine: WorkflowEngine) -> None:
        """A failed run can be resumed — the failed step is re-executed."""
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        # Simulate a failure after some steps completed
        update_workflow_run(db, run["id"], status="failed", stop_reason="step_failed:step_c")

        result = await engine.resume_run(run["id"], defn)
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_resume_failed_run_event_includes_prior_status(self, db: Any, engine: WorkflowEngine) -> None:
        """run_resumed event includes prior_status when resuming from failed."""
        defn = load_definition(GENERIC_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="t1")
        update_workflow_run(db, run["id"], status="failed", stop_reason="step_failed:step_c")

        await engine.resume_run(run["id"], defn)

        events = list_workflow_events(db, run["id"])
        resumed = [e for e in events if e["event_type"] == "run_resumed"]
        assert len(resumed) >= 1
        payload = resumed[-1].get("payload") or {}
        assert payload.get("prior_status") == "failed"


# ---------------------------------------------------------------------------
# Blocked run resume (#1141)
# ---------------------------------------------------------------------------


class TestResumeBlockedRun:
    @pytest.mark.asyncio
    async def test_resume_blocked_gate_passes(self, db: Any, engine: WorkflowEngine) -> None:
        """Gate blocks, fix condition, resume -> completes."""
        global _gate_toggle_value
        _gate_toggle_value = False
        defn = load_definition(GATE_TOGGLE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="blocked-pass")
        assert run["status"] == "blocked"

        _gate_toggle_value = True
        result = await engine.resume_run(run["id"], defn)
        assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_resume_blocked_gate_still_fails(self, db: Any, engine: WorkflowEngine) -> None:
        """Resume without fixing condition -> re-blocks."""
        global _gate_toggle_value
        _gate_toggle_value = False
        defn = load_definition(GATE_TOGGLE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="blocked-refail")
        assert run["status"] == "blocked"

        result = await engine.resume_run(run["id"], defn)
        assert result["status"] == "blocked"

    @pytest.mark.asyncio
    async def test_resume_blocked_gate_step_reevaluated(self, db: Any, engine: WorkflowEngine) -> None:
        """Gate step is re-executed, not skipped, on resume of blocked run."""
        global _gate_toggle_value
        _gate_toggle_value = False
        defn = load_definition(GATE_TOGGLE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="blocked-reeval")
        assert run["status"] == "blocked"

        # Count gate step records before resume
        steps_before = [s for s in list_workflow_steps(db, run["id"]) if s["step_id"] == "gate_toggle"]
        count_before = len(steps_before)

        _gate_toggle_value = True
        result = await engine.resume_run(run["id"], defn)
        assert result["status"] == "completed"

        # Gate step should have been re-evaluated (new step record created)
        steps_after = [s for s in list_workflow_steps(db, run["id"]) if s["step_id"] == "gate_toggle"]
        assert len(steps_after) > count_before

    @pytest.mark.asyncio
    async def test_cancel_blocked_run_immediate(self, db: Any) -> None:
        """request_cancel on a blocked run transitions immediately to cancelled."""
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="blocked-cancel",
        )
        update_workflow_run(db, run["id"], status="blocked")
        updated = await WorkflowEngine.request_cancel(db, run["id"])
        assert updated["status"] == "cancelled"

    @pytest.mark.asyncio
    async def test_cancel_blocked_releases_lock(self, db: Any) -> None:
        """Lock is released when a blocked run is cancelled."""
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="blocked-lock",
        )
        acquire_lock(db, target_kind="task", target_ref="blocked-lock", run_id=run["id"])
        update_workflow_run(db, run["id"], status="blocked")
        await WorkflowEngine.request_cancel(db, run["id"])
        assert get_lock(db, target_kind="task", target_ref="blocked-lock") is None


# ---------------------------------------------------------------------------
# Cancel
# ---------------------------------------------------------------------------


class TestCancel:
    def test_cancel_paused_run(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="t1",
        )
        update_workflow_run(db, run["id"], status="paused")
        acquire_lock(db, target_kind="task", target_ref="t1", run_id=run["id"])

        # Cancel
        update_workflow_run(db, run["id"], status="cancelled")
        release_lock(db, run_id=run["id"])
        create_workflow_event(
            db,
            run_id=run["id"],
            event_type="run_cancelled",
            payload={"cancelled_from_status": "paused"},
        )

        refreshed = get_workflow_run(db, run["id"])
        assert refreshed["status"] == "cancelled"
        assert get_lock(db, target_kind="task", target_ref="t1") is None


# ---------------------------------------------------------------------------
# Replay-from-step (#1106)
# ---------------------------------------------------------------------------


def _setup_completed_run(db: Any, defn_yaml: str = GENERIC_WORKFLOW) -> tuple[dict[str, Any], Any]:
    """Create a paused run with step_a and step_b completed."""
    defn = load_definition(defn_yaml)
    run = create_workflow_run(
        db,
        workflow_id=defn.id,
        workflow_version=defn.version,
        target_kind="task",
        target_ref="replay-test",
        definition_hash=defn.content_hash,
        definition_content=defn_yaml,
    )
    update_workflow_run(db, run["id"], status="paused")
    # Create completed step records
    for sid in ("step_a", "step_b"):
        step = create_workflow_step(db, run_id=run["id"], step_id=sid, step_type="runner", runner_type="shell")
        update_workflow_step(
            db,
            step["id"],
            status="completed",
            result_status="success",
            result_summary="done",
            raw_output_path="/tmp/out",
            duration_ms=100,
            started_at="2026-01-01T00:00:00",
            completed_at="2026-01-01T00:01:00",
            idempotency_key="idem-1",
        )
    return run, defn


class TestReplayFromStep:
    """Tests for resume_run with from_step (replay-from-step semantics, #1106)."""

    @pytest.mark.asyncio
    async def test_step_results_pruned(self, db: Any, engine: WorkflowEngine) -> None:
        """step_results should only contain completed steps BEFORE from_step."""
        run, defn = _setup_completed_run(db)
        await engine.resume_run(run["id"], defn, from_step="step_b")
        events = list_workflow_events(db, run["id"])
        resumed = [e for e in events if e["event_type"] == "run_resumed"]
        assert len(resumed) == 1
        payload = resumed[0]["payload"]
        assert "step_a" in payload["skip_completed"]
        assert "step_b" not in payload["skip_completed"]

    @pytest.mark.asyncio
    async def test_db_steps_reset(self, db: Any, engine: WorkflowEngine) -> None:
        """Steps at/after from_step are reset to pending with cleared metadata."""
        run, defn = _setup_completed_run(db)
        await engine.resume_run(run["id"], defn, from_step="step_b")

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert len(replay) == 1
        pruned = replay[0]["payload"]["pruned_step_ids"]
        assert "step_b" in pruned
        assert "step_c" in pruned
        assert "step_a" not in pruned

    @pytest.mark.asyncio
    async def test_approval_requests_expired(self, db: Any, engine: WorkflowEngine) -> None:
        """Pending approval requests are expired during replay."""
        run, defn = _setup_completed_run(db)
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="step_b",
            tool_name="bash",
            tool_args={"command": "test"},
            risk_tier="EXECUTE",
        )
        await engine.resume_run(run["id"], defn, from_step="step_b")

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert replay[0]["payload"]["expired_approvals"] == 1

    @pytest.mark.asyncio
    async def test_decisions_expired(self, db: Any, engine: WorkflowEngine) -> None:
        """Pending human decisions are expired during replay."""
        run, defn = _setup_completed_run(db)
        create_human_decision(
            db,
            run_id=run["id"],
            step_id="step_b",
            prompt="Choose",
            options=[{"id": "opt1", "label": "Opt 1", "outcome": "continue"}],
        )
        await engine.resume_run(run["id"], defn, from_step="step_b")

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert replay[0]["payload"]["expired_decisions"] == 1

    @pytest.mark.asyncio
    async def test_gate_skipped_waiting_for_approval(self, db: Any, engine: WorkflowEngine) -> None:
        """waiting_for_approval gate is skipped when from_step jumps past it."""
        run, defn = _setup_completed_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_approval", current_step_id="step_a")
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="step_a",
            tool_name="bash",
            tool_args={"command": "test"},
            risk_tier="EXECUTE",
        )
        # from_step=step_b, step_a is in completed => gate is before replay => skip
        result = await engine.resume_run(run["id"], defn, from_step="step_b")
        assert result["status"] in ("completed", "failed")

    @pytest.mark.asyncio
    async def test_gate_skipped_waiting_for_input(self, db: Any, engine: WorkflowEngine) -> None:
        """waiting_for_input gate is skipped when from_step jumps past it."""
        run, defn = _setup_completed_run(db)
        update_workflow_run(db, run["id"], status="waiting_for_input", current_step_id="step_a")
        create_human_decision(
            db,
            run_id=run["id"],
            step_id="step_a",
            prompt="Choose",
            options=[{"id": "opt1", "label": "Opt 1", "outcome": "continue"}],
        )
        result = await engine.resume_run(run["id"], defn, from_step="step_b")
        assert result["status"] in ("completed", "failed")

    @pytest.mark.asyncio
    async def test_replay_event_payload(self, db: Any, engine: WorkflowEngine) -> None:
        """replay_from_step event has full payload."""
        run, defn = _setup_completed_run(db)
        update_workflow_run(db, run["id"], current_step_id="step_b")
        await engine.resume_run(run["id"], defn, from_step="step_b", actor="test_actor")

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert len(replay) == 1
        p = replay[0]["payload"]
        assert p["from_step"] == "step_b"
        assert p["actor"] == "test_actor"
        assert p["prior_current_step"] == "step_b"
        assert "step_b" in p["pruned_step_ids"]
        assert "step_c" in p["pruned_step_ids"]
        assert "step_a" not in p["pruned_step_ids"]
        assert p["prior_status"] == "paused"

    @pytest.mark.asyncio
    async def test_actor_in_resumed_event(self, db: Any, engine: WorkflowEngine) -> None:
        """run_resumed event includes from_step and actor when replaying."""
        run, defn = _setup_completed_run(db)
        await engine.resume_run(run["id"], defn, from_step="step_b", actor="cli_operator")

        events = list_workflow_events(db, run["id"])
        resumed = [e for e in events if e["event_type"] == "run_resumed"]
        assert len(resumed) == 1
        p = resumed[0]["payload"]
        assert p["from_step"] == "step_b"
        assert p["actor"] == "cli_operator"

    @pytest.mark.asyncio
    async def test_replay_from_first_step(self, db: Any, engine: WorkflowEngine) -> None:
        """Replaying from step_a replays all three steps."""
        run, defn = _setup_completed_run(db)
        await engine.resume_run(run["id"], defn, from_step="step_a")

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert len(replay) == 1
        assert set(replay[0]["payload"]["pruned_step_ids"]) == {"step_a", "step_b", "step_c"}

    @pytest.mark.asyncio
    async def test_replay_from_last_step(self, db: Any, engine: WorkflowEngine) -> None:
        """Replaying from step_c only replays that step."""
        run, defn = _setup_completed_run(db)
        await engine.resume_run(run["id"], defn, from_step="step_c")

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert len(replay) == 1
        assert replay[0]["payload"]["pruned_step_ids"] == ["step_c"]

    @pytest.mark.asyncio
    async def test_terminal_run_rejected(self, db: Any, engine: WorkflowEngine) -> None:
        """Completed runs reject replay."""
        defn = load_definition(GENERIC_WORKFLOW)
        run = create_workflow_run(
            db,
            workflow_id=defn.id,
            workflow_version=defn.version,
            target_kind="task",
            target_ref="replay-terminal",
            definition_hash=defn.content_hash,
        )
        update_workflow_run(db, run["id"], status="completed")
        with pytest.raises(ValueError, match="not resumable"):
            await engine.resume_run(run["id"], defn, from_step="step_a")

    @pytest.mark.asyncio
    async def test_default_actor_is_operator(self, db: Any, engine: WorkflowEngine) -> None:
        """Default actor is 'operator'."""
        run, defn = _setup_completed_run(db)
        await engine.resume_run(run["id"], defn, from_step="step_b")

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert replay[0]["payload"]["actor"] == "operator"

    @pytest.mark.asyncio
    async def test_no_replay_event_without_from_step(self, db: Any, engine: WorkflowEngine) -> None:
        """Normal resume does not emit replay_from_step event."""
        run, defn = _setup_completed_run(db)
        await engine.resume_run(run["id"], defn)

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert len(replay) == 0

    @pytest.mark.asyncio
    async def test_no_actor_in_resumed_without_from_step(self, db: Any, engine: WorkflowEngine) -> None:
        """Normal resume does not include from_step/actor in run_resumed payload."""
        run, defn = _setup_completed_run(db)
        await engine.resume_run(run["id"], defn)

        events = list_workflow_events(db, run["id"])
        resumed = [e for e in events if e["event_type"] == "run_resumed"]
        assert len(resumed) == 1
        p = resumed[0]["payload"]
        assert "from_step" not in p
        assert "actor" not in p

    @pytest.mark.asyncio
    async def test_replay_with_failed_run(self, db: Any, engine: WorkflowEngine) -> None:
        """Failed runs can be replayed."""
        run, defn = _setup_completed_run(db)
        update_workflow_run(db, run["id"], status="failed", stop_reason="step_failed")
        await engine.resume_run(run["id"], defn, from_step="step_b")

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert len(replay) == 1
        assert replay[0]["payload"]["prior_status"] == "failed"

    @pytest.mark.asyncio
    async def test_invalid_from_step_rejected(self, db: Any, engine: WorkflowEngine) -> None:
        """Nonexistent from_step raises ValueError."""
        run, defn = _setup_completed_run(db)
        with pytest.raises(ValueError, match="not found in workflow definition"):
            await engine.resume_run(run["id"], defn, from_step="nonexistent")

    @pytest.mark.asyncio
    async def test_no_stale_approvals_no_event_count(self, db: Any, engine: WorkflowEngine) -> None:
        """When no pending approvals exist, expired_approvals is 0."""
        run, defn = _setup_completed_run(db)
        await engine.resume_run(run["id"], defn, from_step="step_b")

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert replay[0]["payload"]["expired_approvals"] == 0
        assert replay[0]["payload"]["expired_decisions"] == 0

    @pytest.mark.asyncio
    async def test_blocked_run_gate_skipped_when_before_from_step(self, db: Any, engine: WorkflowEngine) -> None:
        """Blocked gate before from_step should stay in completed, not be discarded.

        When a run is blocked at step_a and from_step=step_b, step_a is placed
        in completed by the from_step logic.  The blocked-run discard must NOT
        remove it, otherwise the gate would be re-evaluated instead of skipped.
        """
        run, defn = _setup_completed_run(db)
        # Simulate a blocked run whose blocking gate is step_a (before from_step=step_b)
        update_workflow_run(db, run["id"], status="blocked", current_step_id="step_a")
        result = await engine.resume_run(run["id"], defn, from_step="step_b")
        # The run should complete normally: step_a was skipped, step_b and step_c ran
        assert result["status"] in ("completed", "failed")

        events = list_workflow_events(db, run["id"])
        replay = [e for e in events if e["event_type"] == "replay_from_step"]
        assert len(replay) == 1
        # step_a must be in skip_completed (not discarded)
        resumed = [e for e in events if e["event_type"] == "run_resumed"]
        assert len(resumed) == 1
        assert "step_a" in resumed[0]["payload"]["skip_completed"]


# ---------------------------------------------------------------------------
# Storage: replay helpers (#1106)
# ---------------------------------------------------------------------------


class TestResetStepsFrom:
    def test_resets_steps_in_set(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="reset-1",
        )
        step = create_workflow_step(db, run_id=run["id"], step_id="s1", step_type="runner", runner_type="shell")
        update_workflow_step(
            db,
            step["id"],
            status="completed",
            result_status="success",
            result_summary="done",
            raw_output_path="/tmp/out",
            duration_ms=100,
            started_at="2026-01-01T00:00:00",
            completed_at="2026-01-01T00:01:00",
            idempotency_key="idem-1",
        )
        count = reset_steps_from(db, run["id"], {"s1"})
        assert count == 1
        steps = list_workflow_steps(db, run["id"])
        s = steps[0]
        assert s["status"] == "pending"
        assert s["result_status"] is None
        assert s["result_summary"] is None
        assert s["result_artifacts"] is None
        assert s["raw_output_path"] is None
        assert s["duration_ms"] is None
        assert s["started_at"] is None
        assert s["completed_at"] is None
        assert s.get("idempotency_key") is None

    def test_leaves_steps_outside_set(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="reset-2",
        )
        s1 = create_workflow_step(db, run_id=run["id"], step_id="s1", step_type="runner")
        s2 = create_workflow_step(db, run_id=run["id"], step_id="s2", step_type="runner")
        update_workflow_step(db, s1["id"], status="completed", result_status="success")
        update_workflow_step(db, s2["id"], status="completed", result_status="success")

        reset_steps_from(db, run["id"], {"s2"})
        steps = {s["step_id"]: s for s in list_workflow_steps(db, run["id"])}
        assert steps["s1"]["status"] == "completed"
        assert steps["s2"]["status"] == "pending"

    def test_empty_set_returns_zero(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="reset-3",
        )
        count = reset_steps_from(db, run["id"], set())
        assert count == 0

    def test_nonexistent_step_ids_no_error(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="reset-4",
        )
        count = reset_steps_from(db, run["id"], {"nonexistent"})
        assert count == 0

    def test_clears_approval_and_decision_ids(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="reset-5",
        )
        step = create_workflow_step(db, run_id=run["id"], step_id="s1", step_type="runner")
        update_workflow_step(
            db,
            step["id"],
            status="completed",
            result_status="success",
            approval_request_id="apr-1",
            decision_id="dec-1",
        )
        reset_steps_from(db, run["id"], {"s1"})
        steps = list_workflow_steps(db, run["id"])
        assert steps[0].get("approval_request_id") is None
        assert steps[0].get("decision_id") is None


class TestCancelPendingApprovalRequests:
    def test_expires_pending_approvals(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="apr-1",
        )
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="s1",
            tool_name="bash",
            tool_args={"cmd": "x"},
            risk_tier="EXECUTE",
        )
        count = cancel_pending_approval_requests(db, run["id"])
        assert count == 1
        from anteroom.services.workflow_storage import get_pending_approval

        assert get_pending_approval(db, run["id"]) is None

    def test_sets_resolved_by_and_resolved_at(self, db: Any) -> None:
        """cancel_pending_approval_requests must stamp resolved_by and resolved_at."""
        from anteroom.services.workflow_storage import get_approval_request

        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="apr-1b",
        )
        req = create_approval_request(
            db,
            run_id=run["id"],
            step_id="s1",
            tool_name="bash",
            tool_args={"cmd": "x"},
            risk_tier="EXECUTE",
        )
        cancel_pending_approval_requests(db, run["id"])
        updated = get_approval_request(db, req["id"])
        assert updated is not None
        assert updated["status"] == "expired"
        assert updated["resolved_by"] == "replay"
        assert updated["resolved_at"] is not None

    def test_ignores_resolved_approvals(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="apr-2",
        )
        from anteroom.services.workflow_storage import resolve_approval_request

        req = create_approval_request(
            db,
            run_id=run["id"],
            step_id="s1",
            tool_name="bash",
            tool_args={"cmd": "x"},
            risk_tier="EXECUTE",
        )
        resolve_approval_request(db, req["id"], status="approved")
        count = cancel_pending_approval_requests(db, run["id"])
        assert count == 0

    def test_no_pending_returns_zero(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="apr-3",
        )
        count = cancel_pending_approval_requests(db, run["id"])
        assert count == 0

    def test_multiple_pending_all_expired(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="apr-4",
        )
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="s1",
            tool_name="bash",
            tool_args={"cmd": "x"},
            risk_tier="EXECUTE",
        )
        create_approval_request(
            db,
            run_id=run["id"],
            step_id="s2",
            tool_name="bash",
            tool_args={"cmd": "y"},
            risk_tier="EXECUTE",
        )
        count = cancel_pending_approval_requests(db, run["id"])
        assert count == 2


class TestExpirePendingDecisions:
    def test_expires_pending_decisions(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="dec-1",
        )
        create_human_decision(
            db,
            run_id=run["id"],
            step_id="s1",
            prompt="Choose",
            options=[{"id": "a", "label": "A", "outcome": "continue"}],
        )
        count = expire_pending_decisions(db, run["id"])
        assert count == 1
        from anteroom.services.workflow_storage import get_pending_decision

        assert get_pending_decision(db, run["id"]) is None

    def test_clears_selected_option(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="dec-2",
        )
        dec = create_human_decision(
            db,
            run_id=run["id"],
            step_id="s1",
            prompt="Choose",
            options=[{"id": "a", "label": "A", "outcome": "continue"}],
        )
        expire_pending_decisions(db, run["id"])
        from anteroom.services.workflow_storage import get_human_decision

        updated = get_human_decision(db, dec["id"])
        assert updated is not None
        assert updated["status"] == "expired"
        assert updated["selected_option"] is None

    def test_sets_resolved_at(self, db: Any) -> None:
        """expire_pending_decisions must stamp resolved_at for auditability."""
        from anteroom.services.workflow_storage import get_human_decision

        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="dec-2b",
        )
        dec = create_human_decision(
            db,
            run_id=run["id"],
            step_id="s1",
            prompt="Choose",
            options=[{"id": "a", "label": "A", "outcome": "continue"}],
        )
        expire_pending_decisions(db, run["id"])
        updated = get_human_decision(db, dec["id"])
        assert updated is not None
        assert updated["resolved_at"] is not None

    def test_ignores_resolved_decisions(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="dec-3",
        )
        from anteroom.services.workflow_storage import resolve_human_decision

        dec = create_human_decision(
            db,
            run_id=run["id"],
            step_id="s1",
            prompt="Choose",
            options=[{"id": "a", "label": "A", "outcome": "continue"}],
        )
        resolve_human_decision(db, dec["id"], selected_option="a")
        count = expire_pending_decisions(db, run["id"])
        assert count == 0

    def test_no_pending_returns_zero(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="dec-4",
        )
        count = expire_pending_decisions(db, run["id"])
        assert count == 0

    def test_multiple_pending_all_expired(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="0.1.0",
            target_kind="task",
            target_ref="dec-5",
        )
        create_human_decision(
            db,
            run_id=run["id"],
            step_id="s1",
            prompt="Choose",
            options=[{"id": "a", "label": "A", "outcome": "continue"}],
        )
        create_human_decision(
            db,
            run_id=run["id"],
            step_id="s2",
            prompt="Choose",
            options=[{"id": "b", "label": "B", "outcome": "continue"}],
        )
        count = expire_pending_decisions(db, run["id"])
        assert count == 2


# ---------------------------------------------------------------------------
# Generic runner preflight
# ---------------------------------------------------------------------------


COMPENSATE_WORKFLOW = """\
kind: workflow
id: test_compensate_resume
version: 0.1.0
inputs: {}
steps:
  - id: deploy
    type: runner
    runner: shell
    command: "echo deploy"
    timeout: 10
    compensate:
      type: runner
      runner: shell
      command: "echo rollback"
  - id: verify
    type: runner
    runner: shell
    command: "echo verify"
    timeout: 10
"""


class TestStaleHeartbeatCompensationResume:
    @pytest.mark.asyncio
    async def test_resume_stale_reclaimed_during_compensation_enters_compensation_mode(
        self, db: Any, engine: WorkflowEngine
    ) -> None:
        """Runs paused with stale_heartbeat_reclaimed_during_compensation resume in compensation mode."""
        defn = load_definition(COMPENSATE_WORKFLOW)

        # Start a run so steps get created, then manually transition to
        # paused-during-compensation to simulate stale heartbeat reclaim.
        run = await engine.start_run(defn, target_kind="task", target_ref="comp1")

        # The run completed normally.  Force it into the state that the
        # stale-heartbeat recovery path produces: paused with the new
        # stop_reason.
        update_workflow_run(
            db,
            run["id"],
            status="paused",
            stop_reason="stale_heartbeat_reclaimed_during_compensation",
            attempt_count=1,
        )

        await engine.resume_run(run["id"], defn)

        # The engine should have entered the compensation branch, which
        # emits a run_resumed event with resume_phase="compensation".
        events = list_workflow_events(db, run["id"])
        resumed_events = [e for e in events if e["event_type"] == "run_resumed"]
        compensation_resumed = [
            e for e in resumed_events if (e.get("payload") or {}).get("resume_phase") == "compensation"
        ]
        assert len(compensation_resumed) >= 1, (
            f"Expected compensation resume event, got resume events: {resumed_events}"
        )

    @pytest.mark.asyncio
    async def test_process_interrupted_during_compensation_still_resumes_compensation(
        self, db: Any, engine: WorkflowEngine
    ) -> None:
        """Existing process_interrupted_during_compensation path still works after the gate change."""
        defn = load_definition(COMPENSATE_WORKFLOW)
        run = await engine.start_run(defn, target_kind="task", target_ref="comp2")

        update_workflow_run(
            db,
            run["id"],
            status="paused",
            stop_reason="process_interrupted_during_compensation",
            attempt_count=1,
        )

        await engine.resume_run(run["id"], defn)

        events = list_workflow_events(db, run["id"])
        resumed_events = [e for e in events if e["event_type"] == "run_resumed"]
        compensation_resumed = [
            e for e in resumed_events if (e.get("payload") or {}).get("resume_phase") == "compensation"
        ]
        assert len(compensation_resumed) >= 1, (
            f"Expected compensation resume event, got resume events: {resumed_events}"
        )


class TestRunnerPreflight:
    @pytest.mark.asyncio
    async def test_missing_working_dir_fails(self) -> None:
        from anteroom.services.workflow_runners import execute_opaque_runner

        result = await execute_opaque_runner(
            mode="shell",
            command="echo test",
            working_dir="/nonexistent/path/that/does/not/exist",
            timeout=10,
        )
        assert result.status == "failed"
        assert "does not exist" in result.summary
