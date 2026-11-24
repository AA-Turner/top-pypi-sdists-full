"""A CLAIM NEVER COLLIDES: ONE ACTIVE RUN PER TASK, ZERO UNIQUE-VIOLATION ERRORS.

Live 2026-11-13: "Mandate reference patrol" (sch_task a7c1e2d3-…0609, cron every
4 h) ran for hours as a continuation chain. Its fire stayed due the whole time,
so every scanner tick (5 s) tried to claim it with a plain INSERT and lost on
``sch_run_unique_active_per_task`` — ~670 Postgres ERROR lines an hour, every
hour, from the workers.

Two guards, both here:
  * a task that already holds an active run is not a due candidate;
  * the claim itself is ``INSERT … ON CONFLICT … DO NOTHING``: concurrent
    claimers get exactly one run, the losers a plain None, and the database
    sees no unique violation at all.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

import pytest

import matrx_scheduler
from matrx_scheduler import queries
from matrx_scheduler.models import SchTask

ORG = "33333333-3333-4333-8333-333333333333"
USER = "22222222-2222-4222-8222-222222222222"
TASK = "11111111-1111-4111-8111-111111111111"
TRIGGER = "55555555-5555-4555-8555-555555555555"


def _configure(fake_supabase) -> None:
    matrx_scheduler.configure_db(models=fake_supabase.db_models())
    matrx_scheduler.configure(supabase_client=fake_supabase, surface="server", lease_seconds=30)


def _seed_due_task(fake_supabase) -> datetime:
    due = datetime.now(UTC) - timedelta(hours=2)
    fake_supabase.rows["sch_task"].append(
        {
            "id": TASK,
            "user_id": USER,
            "organization_id": ORG,
            "kind": "tool",
            "title": "Reference patrol",
            "queue": "default",
            "surfaces": ["server"],
            "enabled": True,
            "deleted_at": None,
            "expires_at": None,
            "next_due_at": due,
            "last_run_at": None,
            "metadata": {},
        }
    )
    fake_supabase.rows["sch_trigger"].append(
        {
            "id": TRIGGER,
            "task_id": TASK,
            "user_id": USER,
            "organization_id": ORG,
            "type": "cron",
            "config": {"expression": "0 */4 * * *", "tz": "UTC"},
            "enabled": True,
            "deleted_at": None,
            "next_due_at": due,
            "last_fired_at": None,
            "metadata": {},
        }
    )
    return due


def _task(due: datetime) -> SchTask:
    return SchTask(
        id=TASK,
        user_id=USER,
        organization_id=ORG,
        kind="tool",
        title="Reference patrol",
        surfaces=["server"],
        next_due_at=due,
    )


def _active_runs(fake_supabase) -> list[dict]:
    return [
        r
        for r in fake_supabase.rows["sch_run"]
        if r["task_id"] == TASK and r["status"] in queries.ACTIVE_RUN_STATUSES
    ]


@pytest.mark.asyncio
async def test_two_concurrent_claimers_get_exactly_one_run_and_no_violation(fake_supabase) -> None:
    _configure(fake_supabase)
    due = _seed_due_task(fake_supabase)

    results = await asyncio.gather(
        *(queries.claim_task(_task(due), None, None, lease_seconds=30) for _ in range(2)),
        return_exceptions=True,
    )

    assert not [r for r in results if isinstance(r, BaseException)], results
    assert sum(r is not None for r in results) == 1
    assert len(_active_runs(fake_supabase)) == 1
    assert fake_supabase.unique_violations == 0


@pytest.mark.asyncio
async def test_a_task_whose_run_is_still_going_is_not_a_due_candidate(fake_supabase) -> None:
    _configure(fake_supabase)
    due = _seed_due_task(fake_supabase)
    assert [h.task.id for h in await queries.find_due_tasks()] == [TASK]

    first = await queries.claim_task(_task(due), None, None, lease_seconds=30)
    assert first is not None

    # The fire is still due (the long run has not settled), but the scan skips it.
    assert await queries.find_due_tasks() == []

    # Once the run settles, the task is a candidate again: the fire is not lost.
    for row in _active_runs(fake_supabase):
        row["status"] = "success"
    assert [h.task.id for h in await queries.find_due_tasks()] == [TASK]
    assert fake_supabase.unique_violations == 0


@pytest.mark.asyncio
async def test_many_scanner_ticks_over_a_long_run_never_hit_the_index(fake_supabase) -> None:
    """The live shape: one long run, many ticks on several workers."""
    from matrx_scheduler import scanner

    _configure(fake_supabase)
    due = _seed_due_task(fake_supabase)
    assert await queries.claim_task(_task(due), None, None, lease_seconds=30) is not None

    dispatched: list[str] = []
    original = scanner._dispatch_run
    scanner._dispatch_run = lambda hydrated, run: dispatched.append(run.id)
    try:
        for _ in range(10):
            await asyncio.gather(scanner._tick_schedules(), scanner._tick_schedules())
    finally:
        scanner._dispatch_run = original

    assert dispatched == []
    assert len(_active_runs(fake_supabase)) == 1
    assert fake_supabase.unique_violations == 0
