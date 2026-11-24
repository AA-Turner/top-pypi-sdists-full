"""A TASK WITH NO LIVE TRIGGER IS NEVER FIRED BY THE SCHEDULED PASS.

Live 2026-11-01: "Podcast run reconciliation" (sch_task a7c1e2d3-…0331, approved
by Arman every 10 minutes) was re-enabled after a governance pause while its only
trigger stayed suspended. ``sch_task.next_due_at`` still held a past instant, so
every scanner tick (5 s) found the task due, claimed it with ``trigger=None`` and
— with no trigger to roll forward — left it due again: 14,864 runs in 24 hours,
each with ``trigger_id IS NULL``.

The trigger is the clock. Without an enabled one, a task runs only on demand
(a queued "Run now" or a continuation, both the scanner's queued-run pass); the
scheduled pass must not claim it. Such a task is a DARK schedule and
``find_dark_tasks`` reports it.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

import matrx_scheduler
from matrx_scheduler import queries

ORG = "33333333-3333-4333-8333-333333333333"
USER = "22222222-2222-4222-8222-222222222222"
TASK = "11111111-1111-4111-8111-111111111111"
TRIGGER = "55555555-5555-4555-8555-555555555555"


def _seed(fake_supabase, *, trigger_enabled: bool | None) -> None:
    due = datetime.now(UTC) - timedelta(hours=22)
    fake_supabase.rows["sch_task"].append(
        {
            "id": TASK,
            "user_id": USER,
            "organization_id": ORG,
            "kind": "tool",
            "title": "Podcast run reconciliation",
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
    if trigger_enabled is not None:
        fake_supabase.rows["sch_trigger"].append(
            {
                "id": TRIGGER,
                "task_id": TASK,
                "user_id": USER,
                "organization_id": ORG,
                "type": "cron",
                "config": {"expression": "*/10 * * * *", "tz": "UTC"},
                "enabled": trigger_enabled,
                "deleted_at": None,
                "next_due_at": due,
                "last_fired_at": None,
                "metadata": {},
            }
        )


def _configure(fake_supabase) -> None:
    matrx_scheduler.configure_db(models=fake_supabase.db_models())
    matrx_scheduler.configure(supabase_client=fake_supabase, surface="server", lease_seconds=30)


@pytest.mark.asyncio
async def test_a_due_task_whose_only_trigger_is_disabled_is_not_fired(fake_supabase) -> None:
    _configure(fake_supabase)
    _seed(fake_supabase, trigger_enabled=False)
    assert await queries.find_due_tasks() == []


@pytest.mark.asyncio
async def test_a_due_task_with_no_trigger_at_all_is_not_fired_by_the_scheduled_pass(fake_supabase) -> None:
    _configure(fake_supabase)
    _seed(fake_supabase, trigger_enabled=None)
    assert await queries.find_due_tasks() == []


@pytest.mark.asyncio
async def test_a_due_task_with_a_live_trigger_still_fires(fake_supabase) -> None:
    _configure(fake_supabase)
    _seed(fake_supabase, trigger_enabled=True)
    due = await queries.find_due_tasks()
    assert [h.task.id for h in due] == [TASK]
    assert due[0].trigger is not None and due[0].trigger.id == TRIGGER


@pytest.mark.asyncio
async def test_clockless_due_tasks_never_crowd_out_a_live_one(fake_supabase) -> None:
    """The filter is in the query: 25 clockless tasks, sorted first by their stale instant, must not
    fill the 20-row limit and starve a task whose clock is live."""
    _configure(fake_supabase)
    _seed(fake_supabase, trigger_enabled=True)
    stale = datetime.now(UTC) - timedelta(days=30)
    for n in range(25):
        fake_supabase.rows["sch_task"].append(
            dict(fake_supabase.rows["sch_task"][0], id=f"00000000-0000-4000-8000-{n:012d}", next_due_at=stale)
        )
    due = await queries.find_due_tasks()
    assert [h.task.id for h in due] == [TASK]


@pytest.mark.asyncio
async def test_a_soft_deleted_trigger_is_no_clock(fake_supabase) -> None:
    _configure(fake_supabase)
    _seed(fake_supabase, trigger_enabled=True)
    fake_supabase.rows["sch_trigger"][0]["deleted_at"] = datetime.now(UTC)
    assert await queries.find_due_tasks() == []
