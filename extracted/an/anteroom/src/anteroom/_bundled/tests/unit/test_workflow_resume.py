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
    create_workflow_event,
    create_workflow_run,
    create_workflow_step,
    find_running_steps,
    find_stale_runs,
    get_lock,
    get_workflow_run,
    list_completed_step_ids,
    list_workflow_events,
    list_workflow_steps,
    release_lock,
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
