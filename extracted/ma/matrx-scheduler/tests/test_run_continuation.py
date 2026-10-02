"""A run interrupted by a process shutdown CONTINUES — it is never failed for it.

Live 2026-09-14 (`sch_run e6daa2aa…`): the approved keyword facet backfill
started 04:20:01, committed 8 passes (1,593 keywords), and at 05:32:55 the
deploy train replaced the workflow-worker ECS task. The worker never ran its
drain (the ECS bootstrap shell swallowed SIGTERM; see
``aidream/services/runtime/tests/test_deploy_drain.py``), its last lease renewal
was 05:30:02, and at 05:40:02 the replacement worker's sweep stamped the run
``failed / lease expired``. Nothing resumed it: 2,407 of the day's approved
4,000 keywords were simply not done, and 200 queue rows sat ``running``.

A deploy is the most predictable death a run can suffer (Temporal retries an
activity whose worker died; Sidekiq pushes an in-flight job back on TERM;
Celery ``acks_late`` redelivers it). The runner now does the same, for every
task:

* a shutdown cancel, or an orphaned lease found by the sweep, closes the run
  ``interrupted`` — a distinct terminal state, neither success nor failure —
  with every unit it reported preserved;
* a continuation run is queued due NOW, carrying the fire's remaining run
  ceiling and the units already done;
* the repeat guard does not count it;
* continuations per fire are bounded by a knob, and exhausting them is a real,
  loud failure.

Each case below FAILED on the pre-change runner (``failed``/``success`` rows, no
continuation) and passes on the new one.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

import matrx_scheduler
from matrx_scheduler import lease as lease_mod
from matrx_scheduler import queries, repeat_guard
from matrx_scheduler.lease import current_run_lease
from matrx_scheduler.models import AgentRunResult, HydratedTask, SchAgentTask, SchTask, ToolRunInput
from matrx_scheduler.runner import run_claimed_task

ORG = "33333333-3333-4333-8333-333333333333"
USER = "22222222-2222-2222-2222-222222222222"
TASK = "11111111-1111-1111-1111-111111111111"


class _Sink:
    def __init__(self) -> None:
        self.failures: list[dict[str, Any]] = []

    async def __call__(self, payload: dict[str, Any]) -> None:
        self.failures.append(payload)


def _configure(
    fake_supabase,
    *,
    tool_runner,
    lease_seconds: int,
    sink: _Sink | None = None,
    continuation_limit: int | None = None,
) -> None:
    matrx_scheduler.configure_db(models=fake_supabase.db_models())
    extra: dict[str, Any] = {}
    if continuation_limit is not None:

        async def _limit() -> int:
            return continuation_limit

        extra["continuation_limit"] = _limit
    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="test",
        tool_runner=tool_runner,
        lease_seconds=lease_seconds,
        failure_sink=sink,
        **extra,
    )


def _task(max_runtime_seconds: int) -> HydratedTask:
    task = SchTask(
        id=TASK,
        user_id=USER,
        organization_id=ORG,
        kind="tool",
        title="facet backfill (test)",
        surfaces=["test"],
        next_due_at=datetime.now(UTC),
    )
    agent_task = SchAgentTask(
        id=TASK,
        prompt="",
        variables={"tool_name": "facet_backfill", "args": {}},
        max_runtime_seconds=max_runtime_seconds,
    )
    return HydratedTask(task=task, agent_task=agent_task, trigger=None)


def _seed_task(fake_supabase, hydrated: HydratedTask) -> None:
    row = hydrated.task.model_dump()
    row.update({"enabled": True, "last_run_at": None, "metadata": {}})
    fake_supabase.rows["sch_task"].append(row)
    assert hydrated.agent_task is not None
    fake_supabase.rows["sch_agent_task"].append(hydrated.agent_task.model_dump())


async def _claim(fake_supabase, hydrated: HydratedTask, lease_seconds: int):
    _seed_task(fake_supabase, hydrated)
    run = await queries.claim_task(
        hydrated.task, None, hydrated.agent_task, lease_seconds=lease_seconds
    )
    assert run is not None
    return run


def _runs(fake_supabase, status: str) -> list[dict[str, Any]]:
    return [r for r in fake_supabase.rows["sch_run"] if r.get("status") == status]


@pytest.fixture(autouse=True)
def fast_heartbeat(monkeypatch) -> None:
    monkeypatch.setattr(lease_mod, "MIN_HEARTBEAT_INTERVAL_SECONDS", 0.02)


# ── 1. THE GUARD: a shutdown cancel mid-run continues ───────────────────────


@pytest.mark.asyncio
async def test_a_shutdown_cancel_mid_run_queues_a_claimable_continuation(fake_supabase) -> None:
    started = asyncio.Event()

    async def handler(inp: ToolRunInput) -> AgentRunResult:
        lease = current_run_lease()
        await lease.progress(units_done=1593, metadata={"passes": 8})
        started.set()
        await asyncio.sleep(3600)  # pass 9, mid-classification, when the deploy lands
        return AgentRunResult(success=True)

    sink = _Sink()
    _configure(fake_supabase, tool_runner=handler, lease_seconds=5, sink=sink)
    hydrated = _task(max_runtime_seconds=14400)
    run = await _claim(fake_supabase, hydrated, lease_seconds=5)
    driver = asyncio.create_task(run_claimed_task(hydrated, run))
    await asyncio.wait_for(started.wait(), timeout=2)
    driver.cancel()  # what stop_scanner does to an in-flight run on SIGTERM
    with pytest.raises(asyncio.CancelledError):
        await driver

    # The interrupted run: its own distinct terminal state, work preserved.
    original = next(r for r in fake_supabase.rows["sch_run"] if r["id"] == run.id)
    assert original["status"] == "interrupted", original
    assert original["claim_token"] is None and original["finished_at"] is not None
    assert original["result_metadata"]["units_done"] == 1593
    assert original["result_metadata"]["passes"] == 8
    assert "interrupted" in (original["result_metadata"]["stopped_early"] or "")
    assert not sink.failures, "an interruption is not a failure; the failure sink must not hear it"

    # The continuation: queued, due now, carrying the fire's remaining budget.
    queued = _runs(fake_supabase, "queued")
    assert len(queued) == 1, fake_supabase.rows["sch_run"]
    cont = queued[0]
    assert cont["task_id"] == TASK
    assert cont["due_at"] <= datetime.now(UTC)
    marker = cont["metadata"]["continuation"]
    assert marker["of_run_id"] == run.id
    assert marker["fire_run_id"] == run.id
    assert marker["index"] == 1
    assert marker["carried_units_done"] == 1593
    assert 0 < marker["remaining_runtime_seconds"] <= 14400

    # Claimable through the scanner's own queued-run path.
    found = await queries.find_queued_runs()
    assert [r.id for r, _h in found] == [cont["id"]]
    promoted = await queries.claim_queued_run(found[0][0], 5, 14400)
    assert promoted is not None and promoted.status == "claimed"

    # The repeat guard neither counts it as a failure nor as a success.
    assert await repeat_guard.check_task_failure_streak(TASK) is None
    assert fake_supabase.rows["sch_task"][0]["enabled"] is True


@pytest.mark.asyncio
async def test_the_continuation_runs_under_the_fires_remaining_ceiling(fake_supabase) -> None:
    seen: dict[str, Any] = {}

    async def handler(inp: ToolRunInput) -> AgentRunResult:
        lease = current_run_lease()
        seen["max_runtime"] = lease.max_runtime_seconds
        return AgentRunResult.bounded_work(units_done=200, failures=[], summary="one pass")

    _configure(fake_supabase, tool_runner=handler, lease_seconds=5)
    hydrated = _task(max_runtime_seconds=14400)
    _seed_task(fake_supabase, hydrated)
    now = datetime.now(UTC)
    fake_supabase.rows["sch_run"].append(
        {
            "id": "cont-1",
            "task_id": TASK,
            "trigger_id": None,
            "user_id": USER,
            "organization_id": ORG,
            "status": "queued",
            "due_at": now,
            "metadata": {
                "claim_protocol": 2,
                "continuation": {
                    "of_run_id": "orig",
                    "fire_run_id": "orig",
                    "index": 1,
                    "carried_units_done": 1593,
                    "remaining_runtime_seconds": 9600,
                },
            },
            "created_at": now,
        }
    )
    [(queued, hyd)] = await queries.find_queued_runs()
    promoted = await queries.claim_queued_run(queued, 5, 14400)
    assert promoted is not None
    await run_claimed_task(hyd, promoted)
    assert seen["max_runtime"] == 9600, "a continuation must not get a fresh full ceiling"
    row = next(r for r in fake_supabase.rows["sch_run"] if r["id"] == "cont-1")
    assert row["status"] == "success"


# ── 1b. Every shutdown caller waits for the interruption writes ──────────────


@pytest.mark.asyncio
async def test_every_stop_scanner_caller_waits_for_the_interruption_writes() -> None:
    """Break (2026-09-14): the worker's signal handler starts ``stop_scanner`` and
    its teardown ``finally`` calls it again. The second call returned at once —
    the scanner task was already cleared — so the host finished tearing down and
    the event loop closed on top of the cancelled runs' interruption writes."""
    from matrx_scheduler import scanner

    wrote = asyncio.Event()

    async def scanner_loop() -> None:
        await asyncio.sleep(3600)

    async def in_flight_run() -> None:
        try:
            await asyncio.sleep(3600)
        except asyncio.CancelledError:
            await asyncio.sleep(0.2)  # the shielded interrupt + continuation writes
            wrote.set()
            raise

    scanner._task = asyncio.create_task(scanner_loop())
    run = asyncio.create_task(in_flight_run())
    scanner._in_flight.add(run)
    await asyncio.sleep(0)

    signal_drain = asyncio.create_task(
        scanner.stop_scanner(in_flight_timeout=0.05, finalize_timeout=2)
    )
    await asyncio.sleep(0.01)
    await scanner.stop_scanner(in_flight_timeout=0.05, finalize_timeout=2)  # teardown's call

    assert wrote.is_set(), "teardown returned before the interrupted run wrote its continuation"
    await signal_drain
    assert run.cancelled()


# ── 2. The orphaned-lease sweep continues too (the SIGKILL path) ────────────


def _orphan(now: datetime, *, continuation: dict[str, Any] | None = None) -> dict[str, Any]:
    meta: dict[str, Any] = {"claim_protocol": 2}
    if continuation is not None:
        meta["continuation"] = continuation
    return {
        "id": "e6daa2aa-a6f1-4361-9d57-60ebe9243490",
        "task_id": TASK,
        "trigger_id": None,
        "user_id": USER,
        "organization_id": ORG,
        "status": "running",
        "surface": "test",
        "queue": None,
        "due_at": now - timedelta(minutes=80),
        "claimed_at": now - timedelta(minutes=80),
        "claim_token": "tok",
        "claim_expires_at": now - timedelta(seconds=3),
        "result_metadata": {"units_done": 1593, "passes": 8, "stopped_early": None},
        "metadata": meta,
        "created_at": now - timedelta(minutes=80),
    }


@pytest.mark.asyncio
async def test_an_orphaned_lease_is_interrupted_and_continued_not_failed(fake_supabase) -> None:
    sink = _Sink()
    _configure(fake_supabase, tool_runner=None, lease_seconds=600, sink=sink)
    hydrated = _task(max_runtime_seconds=14400)
    _seed_task(fake_supabase, hydrated)
    now = datetime.now(UTC)
    fake_supabase.rows["sch_run"].append(_orphan(now))

    swept = await queries.sweep_expired_leases()

    assert swept == 1
    row = fake_supabase.rows["sch_run"][0]
    assert row["status"] == "interrupted", row
    assert row["result_metadata"]["units_done"] == 1593, "the sweep erased the work"
    assert not sink.failures
    [cont] = _runs(fake_supabase, "queued")
    marker = cont["metadata"]["continuation"]
    assert marker["of_run_id"] == row["id"] and marker["index"] == 1
    # 80 of 240 minutes were used: the continuation carries the other ~160.
    assert 9000 <= marker["remaining_runtime_seconds"] <= 9700
    assert fake_supabase.rows["sch_task"][0]["last_run_at"] is not None
    assert await repeat_guard.check_task_failure_streak(TASK) is None


@pytest.mark.asyncio
async def test_continuations_per_fire_are_bounded_and_exhaustion_is_a_loud_failure(
    fake_supabase,
) -> None:
    sink = _Sink()
    _configure(
        fake_supabase, tool_runner=None, lease_seconds=600, sink=sink, continuation_limit=1
    )
    hydrated = _task(max_runtime_seconds=14400)
    _seed_task(fake_supabase, hydrated)
    now = datetime.now(UTC)
    fake_supabase.rows["sch_run"].append(
        _orphan(
            now,
            continuation={
                "of_run_id": "first",
                "fire_run_id": "first",
                "index": 1,
                "carried_units_done": 400,
                "remaining_runtime_seconds": 14000,
            },
        )
    )

    assert await queries.sweep_expired_leases() == 1

    row = fake_supabase.rows["sch_run"][0]
    assert row["status"] == "failed", "a fire that keeps dying must reach a human"
    assert "max_continuations_per_fire" in row["error_message"]
    assert not _runs(fake_supabase, "queued"), "the cap was ignored"
    assert sink.failures and sink.failures[0]["run_id"] == row["id"]
