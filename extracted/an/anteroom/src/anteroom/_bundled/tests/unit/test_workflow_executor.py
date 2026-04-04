"""Tests for workflow executor worker (#888)."""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import WorkflowEngine
from anteroom.services.workflow_executor import WorkflowExecutorWorker
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import (
    claim_pending_runs,
    create_workflow_run,
    get_workflow_run,
    reset_stale_claims,
)


@pytest.fixture()
def db() -> Any:
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


@pytest.fixture()
def config() -> WorkflowConfig:
    return WorkflowConfig(executor_enabled=True, executor_poll_interval=1, max_concurrent_runs=3)


def _make_pending_run(db: Any, workflow_id: str = "test-wf", **kwargs: Any) -> dict[str, Any]:
    defaults = {
        "workflow_id": workflow_id,
        "workflow_version": "1.0",
        "target_kind": "generic",
        "target_ref": "test-target",
    }
    defaults.update(kwargs)
    return create_workflow_run(db, **defaults)


GATED_WORKFLOW = """\
kind: workflow
id: gated_pipeline
version: 0.1.0
inputs:
  issue_number:
    type: integer
    required: true
steps:
  - id: gate_issue_current
    type: gate
    condition: issue_is_current
    if_false: blocked_issue_not_open
"""


# ---------------------------------------------------------------------------
# Storage: claim_pending_runs
# ---------------------------------------------------------------------------


class TestClaimPendingRuns:
    def test_claim_empty(self, db: Any) -> None:
        result = claim_pending_runs(db, "worker-1", limit=5)
        assert result == []

    def test_claim_returns_pending_runs(self, db: Any) -> None:
        r1 = _make_pending_run(db)
        r2 = _make_pending_run(db)
        claimed = claim_pending_runs(db, "worker-1", limit=5)
        assert len(claimed) == 2
        ids = {r["id"] for r in claimed}
        assert r1["id"] in ids
        assert r2["id"] in ids
        for r in claimed:
            assert r["status"] == "claimed"
            assert r["claimed_by"] == "worker-1"

    def test_claim_respects_limit(self, db: Any) -> None:
        for _ in range(5):
            _make_pending_run(db)
        claimed = claim_pending_runs(db, "worker-1", limit=2)
        assert len(claimed) == 2

    def test_claim_skips_already_claimed(self, db: Any) -> None:
        _make_pending_run(db)
        _make_pending_run(db)
        first = claim_pending_runs(db, "worker-1", limit=1)
        assert len(first) == 1
        second = claim_pending_runs(db, "worker-2", limit=5)
        assert len(second) == 1
        assert second[0]["id"] != first[0]["id"]

    def test_concurrent_claim_no_duplicates(self, db: Any) -> None:
        _make_pending_run(db)
        c1 = claim_pending_runs(db, "worker-1", limit=1)
        c2 = claim_pending_runs(db, "worker-2", limit=1)
        # One wins, one gets nothing
        assert len(c1) + len(c2) == 1

    def test_claim_scoped_by_timestamp(self, db: Any) -> None:
        """Follow-up SELECT uses claimed_at to avoid reselecting stale claims."""
        r1 = _make_pending_run(db)
        # Manually set r1 as claimed by worker-1 with old timestamp
        db.execute(
            "UPDATE workflow_runs SET status='claimed', claimed_by='worker-1', claimed_at='2020-01-01T00:00:00'"
            " WHERE id=?",
            (r1["id"],),
        )
        db.commit()
        # Create a new pending run
        r2 = _make_pending_run(db)
        # Claim by same worker — should only get r2, not r1
        claimed = claim_pending_runs(db, "worker-1", limit=5)
        assert len(claimed) == 1
        assert claimed[0]["id"] == r2["id"]


# ---------------------------------------------------------------------------
# Storage: reset_stale_claims
# ---------------------------------------------------------------------------


class TestResetStaleClaims:
    def test_reset_stale(self, db: Any) -> None:
        r1 = _make_pending_run(db)
        # Claim it with an old timestamp
        db.execute(
            "UPDATE workflow_runs SET status='claimed', claimed_by='w1', claimed_at='2020-01-01T00:00:00' WHERE id=?",
            (r1["id"],),
        )
        db.commit()
        count = reset_stale_claims(db, stale_threshold_seconds=1)
        assert count == 1
        run = get_workflow_run(db, r1["id"])
        assert run["status"] == "pending"
        assert run["claimed_by"] is None

    def test_no_reset_fresh_claims(self, db: Any) -> None:
        _make_pending_run(db)
        claim_pending_runs(db, "w1", limit=1)
        count = reset_stale_claims(db, stale_threshold_seconds=3600)
        assert count == 0


# ---------------------------------------------------------------------------
# Storage: create_workflow_run with trigger params
# ---------------------------------------------------------------------------


class TestCreateWorkflowRunTrigger:
    def test_trigger_fields_stored(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="1.0",
            target_kind="generic",
            target_ref="t",
            trigger_source="web_api",
            trigger_meta={"schedule_id": "abc"},
        )
        assert run["trigger_source"] == "web_api"
        assert run["trigger_meta"] == {"schedule_id": "abc"}
        fetched = get_workflow_run(db, run["id"])
        assert fetched["trigger_source"] == "web_api"
        assert fetched["trigger_meta"] == {"schedule_id": "abc"}

    def test_trigger_fields_default_none(self, db: Any) -> None:
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="1.0",
            target_kind="generic",
            target_ref="t",
        )
        assert run["trigger_source"] is None
        assert run["trigger_meta"] is None


# ---------------------------------------------------------------------------
# Executor worker
# ---------------------------------------------------------------------------


class TestExecutorWorker:
    def test_init(self, config: WorkflowConfig) -> None:
        worker = WorkflowExecutorWorker(config, MagicMock(), MagicMock())
        assert worker.worker_id
        assert not worker.running
        assert worker.active_run_count == 0

    @pytest.mark.asyncio
    async def test_run_once_empty(self, db: Any, config: WorkflowConfig) -> None:
        worker = WorkflowExecutorWorker(config, MagicMock(), db)
        dispatched = await worker.run_once()
        assert dispatched == 0

    @pytest.mark.asyncio
    async def test_run_once_claims_and_dispatches(self, db: Any, config: WorkflowConfig) -> None:
        _make_pending_run(db)
        mock_engine = AsyncMock()
        mock_engine.execute_enqueued_run = AsyncMock()
        worker = WorkflowExecutorWorker(config, lambda: mock_engine, db)

        with patch("anteroom.services.workflow_engine.load_definition") as mock_load:
            mock_load.return_value = MagicMock()
            dispatched = await worker.run_once()

        assert dispatched == 1
        assert worker.active_run_count == 1

    @pytest.mark.asyncio
    async def test_run_once_respects_max_concurrent(self, db: Any) -> None:
        cfg = WorkflowConfig(executor_enabled=True, executor_poll_interval=1, max_concurrent_runs=1)
        for _ in range(3):
            _make_pending_run(db)

        never_finish = asyncio.Future()
        mock_engine = AsyncMock()
        mock_engine.execute_enqueued_run = AsyncMock(return_value=never_finish)
        worker = WorkflowExecutorWorker(cfg, lambda: mock_engine, db)

        with patch("anteroom.services.workflow_engine.load_definition") as mock_load:
            mock_load.return_value = MagicMock()
            d1 = await worker.run_once()
            d2 = await worker.run_once()

        assert d1 == 1
        assert d2 == 0  # Slot full

    @pytest.mark.asyncio
    async def test_backoff_on_failure(self, db: Any, config: WorkflowConfig) -> None:
        worker = WorkflowExecutorWorker(config, MagicMock(), db)
        worker._apply_backoff()
        assert worker._consecutive_failures == 1
        assert worker._current_interval > config.executor_poll_interval
        worker._reset_backoff()
        assert worker._consecutive_failures == 0

    @pytest.mark.asyncio
    async def test_recovery_on_startup(self, db: Any, config: WorkflowConfig) -> None:
        r1 = _make_pending_run(db)
        # Simulate stale claim
        db.execute(
            "UPDATE workflow_runs SET status='claimed', claimed_by='dead-worker', claimed_at='2020-01-01T00:00:00'"
            " WHERE id=?",
            (r1["id"],),
        )
        db.commit()

        worker = WorkflowExecutorWorker(config, MagicMock(), db)
        await worker._recover_on_startup()

        run = get_workflow_run(db, r1["id"])
        assert run["status"] == "pending"

    @pytest.mark.asyncio
    async def test_run_once_cleans_up_failed_tasks(self, db: Any, config: WorkflowConfig) -> None:
        """A task that raises is cleaned up from _active_tasks on next run_once."""
        worker = WorkflowExecutorWorker(config, MagicMock(), db)
        # Manually inject a failing task
        err_task: asyncio.Task[None] = asyncio.get_event_loop().create_future()  # type: ignore[assignment]
        err_task = asyncio.create_task(self._raise_error())
        await asyncio.sleep(0.01)
        worker._active_tasks.add(err_task)
        assert worker.active_run_count == 1
        await worker.run_once()
        assert worker.active_run_count == 0

    @staticmethod
    async def _raise_error() -> None:
        raise RuntimeError("boom")

    @pytest.mark.asyncio
    async def test_run_once_scheduler_enabled(self, db: Any) -> None:
        cfg = WorkflowConfig(
            executor_enabled=True,
            executor_poll_interval=1,
            max_concurrent_runs=3,
            scheduler_enabled=True,
        )
        mock_engine = MagicMock()
        worker = WorkflowExecutorWorker(cfg, lambda: mock_engine, db)

        with patch("anteroom.services.workflow_scheduler.check_and_enqueue", new_callable=AsyncMock) as mock_sched:
            mock_sched.return_value = ["run-1"]
            dispatched = await worker.run_once()
        assert dispatched == 0  # No pending runs, but scheduler was called
        mock_sched.assert_called_once()

    @pytest.mark.asyncio
    async def test_stale_heartbeat_recovery(self, db: Any, config: WorkflowConfig) -> None:
        from anteroom.services.workflow_storage import acquire_lock, create_workflow_run, update_workflow_run

        run = create_workflow_run(db, workflow_id="w", workflow_version="1", target_kind="g", target_ref="t")
        update_workflow_run(db, run["id"], status="running")
        acquire_lock(db, target_kind="g", target_ref="t", run_id=run["id"])
        # Set heartbeat to the past
        db.execute(
            "UPDATE workflow_runs SET heartbeat_at='2020-01-01T00:00:00' WHERE id=?",
            (run["id"],),
        )
        db.commit()

        worker = WorkflowExecutorWorker(config, MagicMock(), db)
        await worker._recover_on_startup()

        from anteroom.services.workflow_storage import get_workflow_run

        recovered = get_workflow_run(db, run["id"])
        assert recovered["status"] == "failed"
        assert recovered["stop_reason"] == "stale_heartbeat_reclaimed"

    @pytest.mark.asyncio
    async def test_run_forever_stops_after_max_failures(self, db: Any, config: WorkflowConfig) -> None:
        worker = WorkflowExecutorWorker(config, MagicMock(), db)

        call_count = 0

        async def failing_run_once() -> int:
            nonlocal call_count
            call_count += 1
            raise RuntimeError("fail")

        worker.run_once = failing_run_once  # type: ignore[assignment]

        # Patch asyncio.sleep globally to avoid real waits
        original_sleep = asyncio.sleep

        async def fast_sleep(delay: float) -> None:
            await original_sleep(0)

        with patch.object(asyncio, "sleep", side_effect=fast_sleep):
            await worker.run_forever()

        # run_forever exits via break after MAX_CONSECUTIVE_FAILURES
        # _running remains True (only stop() sets it False), but the loop has exited
        assert call_count >= 10  # MAX_CONSECUTIVE_FAILURES
        assert worker._consecutive_failures >= 10

    @pytest.mark.asyncio
    async def test_dispatch_run_marks_failed_on_exception(self, db: Any, config: WorkflowConfig) -> None:
        from anteroom.services.workflow_storage import create_workflow_run, get_workflow_run

        run = create_workflow_run(db, workflow_id="w", workflow_version="1", target_kind="g", target_ref="t")
        db.execute("UPDATE workflow_runs SET status='claimed', claimed_by='w1' WHERE id=?", (run["id"],))
        db.commit()

        mock_engine = AsyncMock()
        mock_engine.execute_enqueued_run = AsyncMock(side_effect=RuntimeError("engine crash"))
        worker = WorkflowExecutorWorker(config, lambda: mock_engine, db)

        with patch("anteroom.services.workflow_engine.load_definition", return_value=MagicMock()):
            await worker._dispatch_run(dict(run))

        updated = get_workflow_run(db, run["id"])
        assert updated["status"] == "failed"

    @pytest.mark.asyncio
    async def test_dispatch_run_registers_builtin_gates(self, db: Any, config: WorkflowConfig) -> None:
        from anteroom.services.workflow_storage import create_workflow_run, get_workflow_run

        run = create_workflow_run(
            db,
            workflow_id="gated_pipeline",
            workflow_version="0.1.0",
            target_kind="issue",
            target_ref="42",
            inputs={"issue_number": 42},
            definition_content=GATED_WORKFLOW,
        )
        db.execute("UPDATE workflow_runs SET status='claimed', claimed_by='w1' WHERE id=?", (run["id"],))
        db.commit()

        worker = WorkflowExecutorWorker(
            config,
            lambda: WorkflowEngine(db, config, create_default_registry()),
            db,
        )

        proc = AsyncMock()
        proc.communicate = AsyncMock(return_value=(b"OPEN\n", b""))
        proc.returncode = 0

        with patch("asyncio.create_subprocess_exec", return_value=proc):
            await worker._dispatch_run(dict(run))

        updated = get_workflow_run(db, run["id"])
        assert updated["status"] == "completed"

    @pytest.mark.asyncio
    async def test_start_stop(self, db: Any, config: WorkflowConfig) -> None:
        worker = WorkflowExecutorWorker(config, MagicMock(), db)
        worker.start()
        assert worker._task is not None
        worker.stop()
        assert not worker._running
        # Allow the cancelled task to clean up
        await asyncio.sleep(0.01)


# ---------------------------------------------------------------------------
# Config clamping
# ---------------------------------------------------------------------------


class TestWorkflowConfigExecutor:
    def test_poll_interval_clamped_low(self) -> None:
        cfg = WorkflowConfig(executor_poll_interval=0)
        assert cfg.executor_poll_interval == 1

    def test_poll_interval_clamped_high(self) -> None:
        cfg = WorkflowConfig(executor_poll_interval=999)
        assert cfg.executor_poll_interval == 60

    def test_max_concurrent_clamped_low(self) -> None:
        cfg = WorkflowConfig(max_concurrent_runs=0)
        assert cfg.max_concurrent_runs == 1

    def test_max_concurrent_clamped_high(self) -> None:
        cfg = WorkflowConfig(max_concurrent_runs=100)
        assert cfg.max_concurrent_runs == 20


# ---------------------------------------------------------------------------
# DB migration
# ---------------------------------------------------------------------------


class TestDbMigration:
    def test_fresh_db_has_claimed_status(self, db: Any) -> None:
        """Fresh databases support 'claimed' status in CHECK constraint."""
        run = _make_pending_run(db)
        db.execute(
            "UPDATE workflow_runs SET status='claimed', claimed_by='w1' WHERE id=?",
            (run["id"],),
        )
        db.commit()
        row = db.execute_fetchone("SELECT status FROM workflow_runs WHERE id=?", (run["id"],))
        assert row["status"] == "claimed"

    def test_fresh_db_has_trigger_columns(self, db: Any) -> None:
        """Fresh databases have trigger_source and trigger_meta_json columns."""
        run = create_workflow_run(
            db,
            workflow_id="test",
            workflow_version="1.0",
            target_kind="generic",
            target_ref="t",
            trigger_source="schedule",
        )
        row = db.execute_fetchone("SELECT trigger_source FROM workflow_runs WHERE id=?", (run["id"],))
        assert row["trigger_source"] == "schedule"


# ---------------------------------------------------------------------------
# Workflow resolution
# ---------------------------------------------------------------------------


class TestWorkflowResolution:
    def test_resolve_nonexistent(self) -> None:
        from anteroom.services.workflow_resolution import resolve_workflow_path

        assert resolve_workflow_path("nonexistent-workflow-xyz") is None

    def test_resolve_direct_path(self, tmp_path: Path) -> None:
        from anteroom.services.workflow_resolution import resolve_workflow_path

        p = tmp_path / "test.yaml"
        p.write_text("id: test\n")
        assert resolve_workflow_path(str(p)) == p

    def test_resolve_ignores_non_yaml(self, tmp_path: Path) -> None:
        from anteroom.services.workflow_resolution import resolve_workflow_path

        p = tmp_path / "test.txt"
        p.write_text("id: test\n")
        assert resolve_workflow_path(str(p)) is None

    def test_resolve_rejects_traversal(self) -> None:
        from anteroom.services.workflow_resolution import resolve_workflow_path

        assert resolve_workflow_path("../../etc/passwd") is None
        assert resolve_workflow_path("../secret.yaml") is None
        assert resolve_workflow_path("foo/bar") is None

    def test_resolve_filesystem_disabled(self, tmp_path: Path) -> None:
        from anteroom.services.workflow_resolution import resolve_workflow_path

        p = tmp_path / "test.yaml"
        p.write_text("id: test\n")
        assert resolve_workflow_path(str(p), allow_filesystem=True) == p
        assert resolve_workflow_path(str(p), allow_filesystem=False) is None
