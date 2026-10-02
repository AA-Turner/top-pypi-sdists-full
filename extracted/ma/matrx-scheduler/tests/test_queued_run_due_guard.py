"""The scanner must never select or claim queued work before its due time."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

import matrx_scheduler
from matrx_scheduler import queries
from matrx_scheduler.models import SchRun


@pytest.fixture
def scheduler_backend(fake_supabase):
    """Wire the production query functions to the package's in-memory ORM seam."""
    matrx_scheduler.configure_db(models=fake_supabase.db_models())
    matrx_scheduler.configure(supabase_client=fake_supabase, surface="test")
    return fake_supabase


def _task_row(task_id: str) -> dict[str, object]:
    return {
        "id": task_id,
        "user_id": "11111111-1111-1111-1111-111111111111",
        "organization_id": "33333333-3333-3333-3333-333333333333",
        "kind": "ping",
        "title": f"task {task_id}",
        "queue": "default",
        "surfaces": ["test"],
        "enabled": True,
    }


def _queued_run_row(run_id: str, task_id: str, due_at: datetime) -> dict[str, object]:
    return {
        "id": run_id,
        "task_id": task_id,
        "user_id": "11111111-1111-1111-1111-111111111111",
        "organization_id": "33333333-3333-3333-3333-333333333333",
        "status": "queued",
        "due_at": due_at,
        "metadata": {},
    }


@pytest.mark.asyncio
async def test_find_queued_runs_returns_only_due_rows_before_limit(scheduler_backend):
    """A future row is excluded from the candidates before ordering and limiting."""
    now = datetime.now(UTC)
    scheduler_backend.rows["sch_task"].extend([_task_row("ready-task"), _task_row("future-task")])
    scheduler_backend.rows["sch_run"].extend(
        [
            _queued_run_row("ready-run", "ready-task", now - timedelta(minutes=1)),
            _queued_run_row("future-run", "future-task", now + timedelta(days=1)),
        ]
    )

    queued = await queries.find_queued_runs(limit=2)

    assert [run.id for run, _ in queued] == ["ready-run"]


@pytest.mark.asyncio
async def test_find_queued_runs_never_fires_an_archived_schedule(scheduler_backend):
    """A queued run whose task was moved to Trash (deleted_at set) never fires."""
    now = datetime.now(UTC)
    archived = {**_task_row("archived-task"), "deleted_at": now - timedelta(minutes=5)}
    scheduler_backend.rows["sch_task"].extend([_task_row("live-task"), archived])
    scheduler_backend.rows["sch_run"].extend(
        [
            _queued_run_row("live-run", "live-task", now - timedelta(minutes=1)),
            _queued_run_row("archived-run", "archived-task", now - timedelta(minutes=1)),
        ]
    )

    queued = await queries.find_queued_runs()

    assert [run.id for run, _ in queued] == ["live-run"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("offset", "is_claimed"),
    [(-timedelta(minutes=1), True), (timedelta(days=1), False)],
    ids=["due-row-is-claimed", "future-row-is-refused"],
)
async def test_claim_queued_run_requires_a_due_row(scheduler_backend, offset, is_claimed):
    """The atomic update rejects future work instead of merely trusting its scan snapshot."""
    row = _queued_run_row("claim-run", "claim-task", datetime.now(UTC) + offset)
    scheduler_backend.rows["sch_run"].append(row)

    claimed = await queries.claim_queued_run(SchRun(**row), lease_seconds=30, max_runtime_seconds=60)

    assert (claimed is not None) is is_claimed
    assert scheduler_backend.rows["sch_run"][0]["status"] == (
        "claimed" if is_claimed else "queued"
    )


@pytest.mark.asyncio
async def test_claim_queued_run_refuses_row_rescheduled_after_scan(scheduler_backend):
    """A row due during the scan is rechecked when the claim is persisted."""
    now = datetime.now(UTC)
    scheduler_backend.rows["sch_task"].append(_task_row("rescheduled-task"))
    row = _queued_run_row("rescheduled-run", "rescheduled-task", now - timedelta(minutes=1))
    scheduler_backend.rows["sch_run"].append(row)

    scanned_run, _ = (await queries.find_queued_runs())[0]
    row["due_at"] = now + timedelta(days=1)

    claimed = await queries.claim_queued_run(scanned_run, lease_seconds=30, max_runtime_seconds=60)

    assert claimed is None
    assert row["status"] == "queued"
