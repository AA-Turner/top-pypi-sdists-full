"""A ONE-SHOT FIRES ONCE, AND A ONE-SHOT THAT FAILED IS NEVER SILENT.

Live 2026-09-16 07:48 UTC: the one-shot schedule "learn" fired, its run failed
in 26 ms ("has neither agent_id nor mandate_key; schedule was paused"), and the
runner switched the task off. Then nothing: the trigger kept ``last_fired_at =
NULL`` and ``next_due_at = 2026-09-16 07:48`` for twelve days, so every reader
saw a job that was due and had never run; the task carried no suspension record,
so the super-admin attention dock (``scheduler.system_schedule_alarms``: only
``suspended`` / enabled-``overdue`` / a failed streak of 2+) listed nothing; and
the repeat guard, which escalates at 3 failures, never escalates a schedule that
only ever gets ONE run. Nobody was told.

Two defects, one class — the run's terminal path decides what a person can see:

1. The trigger roll-forward lived on the success path alone. Every path where the
   handler finalizes the run itself (invalid configuration, the host runner
   raising, no runner, a run ceiling) returned before it — and for a one-shot
   whose task was still ENABLED that is worse than stale: the trigger is still due,
   so the scanner claims it again on the next tick. A "once" job ran again.
2. A scheduler-initiated pause stamped no ``metadata.auto_suspended`` and called
   no escalation sink, and a failed one-shot never reached any guard ceiling.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

import matrx_scheduler
from matrx_scheduler import queries
from matrx_scheduler.models import AgentRunInput, AgentRunResult
from matrx_scheduler.runner import run_claimed_task

ORG = "33333333-3333-4333-8333-333333333333"
USER = "22222222-2222-4222-8222-222222222222"
TASK = "11111111-1111-4111-8111-111111111111"
TRIGGER = "55555555-5555-4555-8555-555555555555"


class _Sink:
    def __init__(self) -> None:
        self.alarms: list[Any] = []

    async def __call__(self, alarm: Any) -> None:
        self.alarms.append(alarm)


def _seed(fake_supabase, *, trigger_type: str, agent_id: str | None) -> datetime:
    due = datetime.now(UTC) - timedelta(minutes=5)
    config = {"at": due.isoformat()} if trigger_type == "one-shot" else {"seconds": 3600}
    fake_supabase.rows["sch_task"].append(
        {
            "id": TASK,
            "user_id": USER,
            "organization_id": ORG,
            "kind": "agent",
            "title": "learn",
            "queue": "default",
            "surfaces": ["any"],
            "enabled": True,
            "deleted_at": None,
            "expires_at": None,
            "next_due_at": due,
            "last_run_at": None,
            "metadata": {},
        }
    )
    fake_supabase.rows["sch_agent_task"].append(
        {
            "id": TASK,
            "agent_id": agent_id,
            "mandate_key": None,
            "prompt": "openai",
            "variables": {},
            "persistent_conversation_id": None,
            "max_runtime_seconds": 600,
            "auth_mode": "ask",
            "max_concurrent": 1,
            "organization_id": ORG,
        }
    )
    fake_supabase.rows["sch_trigger"].append(
        {
            "id": TRIGGER,
            "task_id": TASK,
            "user_id": USER,
            "organization_id": ORG,
            "type": trigger_type,
            "config": config,
            "enabled": True,
            "deleted_at": None,
            "next_due_at": due,
            "last_fired_at": None,
            "metadata": {},
        }
    )
    return due


def _configure(fake_supabase, *, agent_runner, sink: _Sink) -> None:
    matrx_scheduler.configure_db(models=fake_supabase.db_models())
    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="server",
        agent_runner=agent_runner,
        lease_seconds=30,
        escalation_sink=sink,
    )


async def _fire_once(fake_supabase) -> None:
    """Exactly what one scanner tick does for one due task."""
    due = await queries.find_due_tasks()
    assert [h.task.id for h in due] == [TASK], "the seeded task must be due"
    hydrated = due[0]
    run = await queries.claim_task(
        hydrated.task, hydrated.trigger, hydrated.agent_task, lease_seconds=30
    )
    assert run is not None
    await run_claimed_task(hydrated, run)


def _row(fake_supabase, table: str) -> dict[str, Any]:
    return fake_supabase.rows[table][0]


@pytest.mark.asyncio
async def test_a_one_shot_whose_host_runner_raised_does_not_fire_again(fake_supabase) -> None:
    calls = 0

    async def agent_runner(_inp: AgentRunInput) -> AgentRunResult:
        nonlocal calls
        calls += 1
        raise RuntimeError("provider exploded")

    sink = _Sink()
    _configure(fake_supabase, agent_runner=agent_runner, sink=sink)
    _seed(fake_supabase, trigger_type="one-shot", agent_id="agent-1")

    await _fire_once(fake_supabase)

    assert calls == 1
    assert _row(fake_supabase, "sch_run")["status"] == "failed"
    # Fired once, so the next tick finds nothing — before the fix the task was
    # still enabled with a due trigger and the scanner claimed it again.
    assert await queries.find_due_tasks() == []
    assert _row(fake_supabase, "sch_task")["enabled"] is False
    assert _row(fake_supabase, "sch_trigger")["last_fired_at"] is not None
    # And the failure is loud: a suspension record the dock reads, and the owner sink.
    suspended = _row(fake_supabase, "sch_task")["metadata"].get("auto_suspended")
    assert suspended and "one-time schedule" in suspended["reason"]
    assert "provider exploded" in suspended["reason"]
    assert len(sink.alarms) >= 1 and sink.alarms[0].task_id == TASK


@pytest.mark.asyncio
async def test_the_learn_case_a_misconfigured_one_shot_is_recorded_and_told(fake_supabase) -> None:
    async def agent_runner(_inp: AgentRunInput) -> AgentRunResult:
        raise AssertionError("a schedule with no agent must never reach the host runner")

    sink = _Sink()
    _configure(fake_supabase, agent_runner=agent_runner, sink=sink)
    due = _seed(fake_supabase, trigger_type="one-shot", agent_id=None)

    await _fire_once(fake_supabase)

    run = _row(fake_supabase, "sch_run")
    assert run["status"] == "failed"
    assert "neither agent_id nor mandate_key" in run["error_message"]
    task = _row(fake_supabase, "sch_task")
    trigger = _row(fake_supabase, "sch_trigger")
    assert task["enabled"] is False
    # The trigger says it FIRED (the "learn" row read last_fired_at NULL for 12
    # days) and keeps its instant, so a deliberate re-enable retries it once.
    assert trigger["last_fired_at"] is not None
    assert trigger["next_due_at"] == due
    suspended = task["metadata"].get("auto_suspended")
    assert suspended, "a scheduler-initiated pause with no suspension record is invisible"
    assert "no agent or Mandate" in suspended["reason"]
    assert sink.alarms and sink.alarms[0].task_id == TASK
    assert len({a.signature for a in sink.alarms}) == 1, "one cause, one chip"


@pytest.mark.asyncio
async def test_a_misconfigured_interval_schedule_is_paused_out_loud(fake_supabase) -> None:
    async def agent_runner(_inp: AgentRunInput) -> AgentRunResult:
        raise AssertionError("never dispatched")

    sink = _Sink()
    _configure(fake_supabase, agent_runner=agent_runner, sink=sink)
    _seed(fake_supabase, trigger_type="interval", agent_id=None)

    await _fire_once(fake_supabase)

    task = _row(fake_supabase, "sch_task")
    assert task["enabled"] is False
    assert task["metadata"].get("auto_suspended"), "paused with no record = silent"
    assert sink.alarms and sink.alarms[0].task_id == TASK


@pytest.mark.asyncio
async def test_a_successful_one_shot_is_spent_and_raises_nothing(fake_supabase) -> None:
    async def agent_runner(_inp: AgentRunInput) -> AgentRunResult:
        return AgentRunResult(success=True, result_summary="done")

    sink = _Sink()
    _configure(fake_supabase, agent_runner=agent_runner, sink=sink)
    _seed(fake_supabase, trigger_type="one-shot", agent_id="agent-1")

    await _fire_once(fake_supabase)

    assert _row(fake_supabase, "sch_run")["status"] == "success"
    task = _row(fake_supabase, "sch_task")
    trigger = _row(fake_supabase, "sch_trigger")
    assert task["enabled"] is False
    assert trigger["next_due_at"] is None
    assert trigger["last_fired_at"] is not None
    assert "auto_suspended" not in task["metadata"]
    assert sink.alarms == []
    assert await queries.find_due_tasks() == []
