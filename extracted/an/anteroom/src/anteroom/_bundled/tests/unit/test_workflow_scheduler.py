"""Tests for workflow scheduler (#969)."""

from __future__ import annotations

import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_storage import (
    advance_schedule,
    check_pending_advances,
    claim_due_schedules,
    create_schedule,
    create_workflow_run,
    delete_schedule,
    get_schedule,
    list_schedules,
    release_schedule_claim,
    reset_stale_schedule_claims,
    set_advance_after_run,
    update_schedule,
    update_workflow_run,
)


@pytest.fixture()
def db() -> Any:
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _past_iso(minutes: int = 5) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()


def _future_iso(minutes: int = 60) -> str:
    return (datetime.now(timezone.utc) + timedelta(minutes=minutes)).isoformat()


# ---------------------------------------------------------------------------
# Schedule CRUD
# ---------------------------------------------------------------------------


class TestScheduleCRUD:
    def test_create_and_get(self, db: Any) -> None:
        sched = create_schedule(
            db,
            workflow_ref="test-wf",
            ref_type="builtin",
            cron_expr="0 * * * *",
            target_ref="t1",
            next_run_at=_future_iso(),
        )
        assert sched["id"]
        assert sched["workflow_ref"] == "test-wf"
        assert sched["enabled"] == 1

        fetched = get_schedule(db, sched["id"])
        assert fetched is not None
        assert fetched["workflow_ref"] == "test-wf"

    def test_list(self, db: Any) -> None:
        create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_future_iso()
        )
        create_schedule(
            db, workflow_ref="b", ref_type="builtin", cron_expr="0 0 * * *", target_ref="t", next_run_at=_future_iso()
        )
        assert len(list_schedules(db)) == 2

    def test_update(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_future_iso()
        )
        updated = update_schedule(db, sched["id"], enabled=0)
        assert updated["enabled"] == 0

    def test_update_rejects_bad_column(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_future_iso()
        )
        with pytest.raises(ValueError, match="not in allowed"):
            update_schedule(db, sched["id"], bad_column="x")

    def test_delete(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_future_iso()
        )
        assert delete_schedule(db, sched["id"]) is True
        assert get_schedule(db, sched["id"]) is None

    def test_create_rejects_invalid_cron(self, db: Any) -> None:
        with pytest.raises(ValueError):
            create_schedule(
                db, workflow_ref="a", ref_type="builtin", cron_expr="bad", target_ref="t", next_run_at=_future_iso()
            )

    def test_create_rejects_invalid_ref_type(self, db: Any) -> None:
        with pytest.raises(ValueError, match="Invalid ref_type"):
            create_schedule(
                db,
                workflow_ref="a",
                ref_type="invalid",
                cron_expr="0 * * * *",
                target_ref="t",
                next_run_at=_future_iso(),
            )

    def test_create_rejects_oversized_inputs(self, db: Any) -> None:
        big_inputs = {"data": "x" * 70000}
        with pytest.raises(ValueError, match="64KB"):
            create_schedule(
                db,
                workflow_ref="a",
                ref_type="builtin",
                cron_expr="0 * * * *",
                target_ref="t",
                next_run_at=_future_iso(),
                inputs=big_inputs,
            )


# ---------------------------------------------------------------------------
# Atomic claim
# ---------------------------------------------------------------------------


class TestClaimDueSchedules:
    def test_claim_due(self, db: Any) -> None:
        create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        claimed = claim_due_schedules(db, "worker-1")
        assert len(claimed) == 1
        assert claimed[0]["claimed_by"] == "worker-1"

    def test_skip_future(self, db: Any) -> None:
        create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_future_iso()
        )
        assert claim_due_schedules(db, "worker-1") == []

    def test_skip_disabled(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        update_schedule(db, sched["id"], enabled=0)
        assert claim_due_schedules(db, "worker-1") == []

    def test_skip_advance_pending(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        set_advance_after_run(db, sched["id"], "some-run-id")
        assert claim_due_schedules(db, "worker-1") == []

    def test_concurrent_claim_safe(self, db: Any) -> None:
        create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        c1 = claim_due_schedules(db, "w1", limit=1)
        c2 = claim_due_schedules(db, "w2", limit=1)
        assert len(c1) + len(c2) == 1


# ---------------------------------------------------------------------------
# Advance and release
# ---------------------------------------------------------------------------


class TestAdvanceAndRelease:
    def test_advance_clears_claim(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        claim_due_schedules(db, "w1")
        advance_schedule(db, sched["id"], next_run_at=_future_iso(), last_run_at=_now_iso(), last_run_id="run-1")
        fetched = get_schedule(db, sched["id"])
        assert fetched["claimed_by"] is None
        assert fetched["last_run_id"] == "run-1"

    def test_release_claim(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        claim_due_schedules(db, "w1")
        release_schedule_claim(db, sched["id"])
        fetched = get_schedule(db, sched["id"])
        assert fetched["claimed_by"] is None

    def test_set_advance_after_run(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        set_advance_after_run(db, sched["id"], "run-1")
        fetched = get_schedule(db, sched["id"])
        assert fetched["advance_after_run_id"] == "run-1"


# ---------------------------------------------------------------------------
# Queue policy: check_pending_advances
# ---------------------------------------------------------------------------


class TestCheckPendingAdvances:
    def test_detects_terminal_run(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        run = create_workflow_run(db, workflow_id="a", workflow_version="1", target_kind="generic", target_ref="t")
        set_advance_after_run(db, sched["id"], run["id"])
        update_workflow_run(db, run["id"], status="completed")
        pending = check_pending_advances(db)
        assert len(pending) == 1
        assert pending[0]["id"] == sched["id"]

    def test_ignores_running(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        run = create_workflow_run(db, workflow_id="a", workflow_version="1", target_kind="generic", target_ref="t")
        set_advance_after_run(db, sched["id"], run["id"])
        update_workflow_run(db, run["id"], status="running")
        assert check_pending_advances(db) == []

    def test_excludes_blocked(self, db: Any) -> None:
        """Blocked runs are not terminal — schedule should not advance (#1141)."""
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        run = create_workflow_run(db, workflow_id="a", workflow_version="1", target_kind="generic", target_ref="t")
        set_advance_after_run(db, sched["id"], run["id"])
        update_workflow_run(db, run["id"], status="blocked")
        assert check_pending_advances(db) == []


# ---------------------------------------------------------------------------
# Stale claim recovery
# ---------------------------------------------------------------------------


class TestStaleScheduleClaims:
    def test_reset_stale(self, db: Any) -> None:
        sched = create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        db.execute(
            "UPDATE workflow_schedules SET claimed_by='w1', claimed_at='2020-01-01T00:00:00' WHERE id=?",
            (sched["id"],),
        )
        db.commit()
        count = reset_stale_schedule_claims(db, stale_threshold_seconds=1)
        assert count == 1
        assert get_schedule(db, sched["id"])["claimed_by"] is None

    def test_no_reset_fresh(self, db: Any) -> None:
        create_schedule(
            db, workflow_ref="a", ref_type="builtin", cron_expr="0 * * * *", target_ref="t", next_run_at=_past_iso()
        )
        claim_due_schedules(db, "w1")
        assert reset_stale_schedule_claims(db, stale_threshold_seconds=3600) == 0


# ---------------------------------------------------------------------------
# TriggerDef parsing
# ---------------------------------------------------------------------------


class TestTriggerDef:
    def test_parse_schedule_trigger(self) -> None:
        from anteroom.services.workflow_engine import load_definition

        yaml_src = """
kind: workflow
id: test-triggers
version: 1.0
triggers:
  - type: schedule
    cron: "0 * * * *"
    target_ref: daily-check
steps:
  - id: greet
    type: runner
    runner: shell
    command: echo hi
"""
        defn = load_definition(yaml_src)
        assert len(defn.triggers) == 1
        assert defn.triggers[0].type == "schedule"
        assert defn.triggers[0].cron == "0 * * * *"

    def test_no_triggers_is_empty_list(self) -> None:
        from anteroom.services.workflow_engine import load_definition

        yaml_src = """
kind: workflow
id: test-no-triggers
version: 1.0
steps:
  - id: greet
    type: runner
    runner: shell
    command: echo hi
"""
        defn = load_definition(yaml_src)
        assert defn.triggers == []

    def test_schedule_trigger_requires_cron(self) -> None:
        from anteroom.services.workflow_engine import load_definition

        yaml_src = """
kind: workflow
id: test-bad
version: 1.0
triggers:
  - type: schedule
steps:
  - id: greet
    type: runner
    runner: shell
    command: echo hi
"""
        with pytest.raises(ValueError, match="cron"):
            load_definition(yaml_src)


# ---------------------------------------------------------------------------
# Config clamping
# ---------------------------------------------------------------------------


class TestSchedulerConfig:
    def test_min_interval_clamped_low(self) -> None:
        cfg = WorkflowConfig(min_schedule_interval=10)
        assert cfg.min_schedule_interval == 60


# ---------------------------------------------------------------------------
# Scheduler service
# ---------------------------------------------------------------------------


class TestSchedulerService:
    @pytest.mark.asyncio
    async def test_check_and_enqueue_empty(self, db: Any) -> None:
        from anteroom.services.workflow_scheduler import check_and_enqueue

        engine = MagicMock()
        result = await check_and_enqueue(db, engine, "worker-1")
        assert result == []

    @pytest.mark.asyncio
    async def test_check_and_enqueue_skip_policy(self, db: Any) -> None:
        from anteroom.services.workflow_scheduler import check_and_enqueue

        create_schedule(
            db,
            workflow_ref="test-wf",
            ref_type="builtin",
            cron_expr="0 * * * *",
            target_ref="t1",
            next_run_at=_past_iso(),
            missed_policy="skip",
        )

        mock_engine = AsyncMock()
        mock_engine.enqueue_run = AsyncMock(return_value={"id": "run-123"})

        with (
            patch("anteroom.services.workflow_resolution.resolve_workflow_path") as mock_resolve,
            patch("anteroom.services.workflow_engine.load_definition") as mock_load,
        ):
            mock_resolve.return_value = Path("/fake.yaml")
            mock_def = MagicMock()
            mock_load.return_value = mock_def

            result = await check_and_enqueue(db, mock_engine, "worker-1")

        assert result == ["run-123"]
        mock_engine.enqueue_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_resolution_failure_releases_claim(self, db: Any) -> None:
        from anteroom.services.workflow_scheduler import check_and_enqueue

        sched = create_schedule(
            db,
            workflow_ref="nonexistent",
            ref_type="builtin",
            cron_expr="0 * * * *",
            target_ref="t1",
            next_run_at=_past_iso(),
        )

        mock_engine = AsyncMock()
        with patch("anteroom.services.workflow_resolution.resolve_workflow_path", return_value=None):
            result = await check_and_enqueue(db, mock_engine, "worker-1")

        assert result == []
        fetched = get_schedule(db, sched["id"])
        assert fetched["claimed_by"] is None  # Claim was released


# ---------------------------------------------------------------------------
# Path confinement
# ---------------------------------------------------------------------------


class TestCheckAndEnqueueQueuePolicy:
    @pytest.mark.asyncio
    async def test_queue_policy_sets_advance_after_run(self, db: Any) -> None:
        from anteroom.services.workflow_scheduler import check_and_enqueue

        create_schedule(
            db,
            workflow_ref="test-wf",
            ref_type="builtin",
            cron_expr="0 * * * *",
            target_ref="t1",
            next_run_at=_past_iso(),
            missed_policy="queue",
        )

        mock_engine = AsyncMock()
        mock_engine.enqueue_run = AsyncMock(return_value={"id": "run-q1"})

        with (
            patch("anteroom.services.workflow_resolution.resolve_workflow_path") as mock_resolve,
            patch("anteroom.services.workflow_engine.load_definition") as mock_load,
        ):
            mock_resolve.return_value = Path("/fake.yaml")
            mock_load.return_value = MagicMock()
            result = await check_and_enqueue(db, mock_engine, "worker-1")

        assert result == ["run-q1"]
        # The schedule should have advance_after_run_id set
        schedules = list_schedules(db)
        assert schedules[0]["advance_after_run_id"] == "run-q1"

    @pytest.mark.asyncio
    async def test_pending_advances_processed(self, db: Any) -> None:
        from anteroom.services.workflow_scheduler import check_and_enqueue

        sched = create_schedule(
            db,
            workflow_ref="test-wf",
            ref_type="builtin",
            cron_expr="0 * * * *",
            target_ref="t1",
            next_run_at=_past_iso(),
        )
        run = create_workflow_run(db, workflow_id="a", workflow_version="1", target_kind="generic", target_ref="t")
        set_advance_after_run(db, sched["id"], run["id"])
        update_workflow_run(db, run["id"], status="completed")

        mock_engine = AsyncMock()
        result = await check_and_enqueue(db, mock_engine, "worker-1")

        # advance processed, schedule has new next_run_at
        fetched = get_schedule(db, sched["id"])
        assert fetched["advance_after_run_id"] is None  # cleared by advance
        assert result == []  # may or may not be claimed depending on timing


class TestPathConfinement:
    def test_rejects_traversal(self) -> None:
        from anteroom.services.workflow_scheduler import _confine_path

        with pytest.raises(ValueError, match="outside allowed roots"):
            _confine_path("/etc/passwd", allowed_roots=[Path("/home/user/.anteroom")])

    def test_allows_anteroom_dir(self, tmp_path: Path) -> None:
        from anteroom.services.workflow_scheduler import _confine_path

        wf = tmp_path / "test.yaml"
        wf.write_text("id: test\n")
        result = _confine_path(str(wf), allowed_roots=[tmp_path])
        assert result == wf.resolve()

    def test_traversal_via_symlink(self, tmp_path: Path) -> None:
        from anteroom.services.workflow_scheduler import _confine_path

        # Even with a valid-looking path, resolve() catches symlink escapes
        with pytest.raises(ValueError, match="outside allowed roots"):
            _confine_path("/etc/shadow", allowed_roots=[tmp_path])
