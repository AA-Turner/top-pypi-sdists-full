"""THE RUN LEASE — a live handler is never expired, a stopped handler never
loses its work, and a handler that outlives its lease is stopped, not zombied.

Live 2026-09-13 04:20 UTC: the approved keyword facet backfill (Max runtime
1800s) was claimed for a 31-minute lease that nothing renewed. At 04:51 the
sweep stamped the run ``failed / lease expired`` with ``result_metadata=NULL``
and ``sch_task.last_run_at`` untouched — while the handler kept running for
hours as a zombie (AI calls attributed to the run continued past 04:58), with a
final report the ledger could no longer accept. The repeat guard, which judges
"never succeeded" by ``result_metadata.units_done``, saw NOTHING of the 638
keywords it had classified. Every case here is that night, under a short lease.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

import matrx_scheduler
from matrx_scheduler import lease as lease_mod
from matrx_scheduler import queries
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


def _configure(fake_supabase, *, tool_runner, lease_seconds: int, sink: _Sink | None = None):
    matrx_scheduler.configure_db(models=fake_supabase.db_models())
    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="test",
        tool_runner=tool_runner,
        lease_seconds=lease_seconds,
        failure_sink=sink,
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


async def _claim(fake_supabase, hydrated: HydratedTask, lease_seconds: int):
    fake_supabase.rows["sch_task"].append(
        {"id": TASK, "user_id": USER, "organization_id": ORG, "enabled": True, "last_run_at": None}
    )
    run = await queries.claim_task(
        hydrated.task, None, hydrated.agent_task, lease_seconds=lease_seconds
    )
    assert run is not None
    return run


def _run_row(fake_supabase) -> dict[str, Any]:
    return fake_supabase.rows["sch_run"][0]


def _task_row(fake_supabase) -> dict[str, Any]:
    return fake_supabase.rows["sch_task"][0]


@pytest.fixture(autouse=True)
def fast_heartbeat(monkeypatch) -> None:
    # The floor exists so a tiny production lease cannot hot-loop; tests run on
    # sub-second leases and need the heartbeat to actually fire.
    monkeypatch.setattr(lease_mod, "MIN_HEARTBEAT_INTERVAL_SECONDS", 0.02)


# ── 1. A live handler is never expired ─────────────────────────────────────


@pytest.mark.asyncio
async def test_a_live_handler_outlives_its_lease_and_is_not_expired(fake_supabase) -> None:
    """The 2026-09-13 night in miniature: the handler needs several leases'
    worth of time. The heartbeat must keep the claim alive under a sweeping
    scanner, and the run must land as success with its work counted."""
    seen_lease: list[Any] = []

    async def handler(inp: ToolRunInput) -> AgentRunResult:
        lease = current_run_lease()
        seen_lease.append(lease)
        for unit in range(1, 4):
            await asyncio.sleep(0.25)  # one "pass"; the lease is 1s, so 3 passes = 0.75s
            assert await lease.progress(units_done=unit * 200, metadata={"pass": unit})
        return AgentRunResult.bounded_work(units_done=600, failures=[], summary="passes=3")

    _configure(fake_supabase, tool_runner=handler, lease_seconds=1)
    hydrated = _task(max_runtime_seconds=30)
    run = await _claim(fake_supabase, hydrated, lease_seconds=1)
    first_expiry = _run_row(fake_supabase)["claim_expires_at"]

    async def sweeping_scanner() -> int:
        swept = 0
        for _ in range(12):
            await asyncio.sleep(0.1)
            swept += await queries.sweep_expired_leases()
        return swept

    swept, _ = await asyncio.gather(sweeping_scanner(), run_claimed_task(hydrated, run))

    row = _run_row(fake_supabase)
    assert swept == 0, "a heartbeating run was expired by the sweep"
    assert row["status"] == "success", row
    assert row["result_metadata"]["units_done"] == 600
    assert row["claim_expires_at"] > first_expiry, "the heartbeat never renewed the lease"
    assert seen_lease and seen_lease[0].renewals >= 1
    assert seen_lease[0].bounded is True
    assert _task_row(fake_supabase)["last_run_at"] is not None


# ── 2. Progress is on the row BEFORE any terminal write ────────────────────


@pytest.mark.asyncio
async def test_progress_lands_on_the_row_while_the_run_is_still_in_flight(fake_supabase) -> None:
    gate = asyncio.Event()
    observed: dict[str, Any] = {}

    async def handler(inp: ToolRunInput) -> AgentRunResult:
        lease = current_run_lease()
        await lease.progress(units_done=638, metadata={"passes": 3})
        observed["mid_run"] = dict(_run_row(fake_supabase))
        gate.set()
        return AgentRunResult.bounded_work(units_done=638, failures=[], summary="ok")

    _configure(fake_supabase, tool_runner=handler, lease_seconds=5)
    hydrated = _task(max_runtime_seconds=30)
    run = await _claim(fake_supabase, hydrated, lease_seconds=5)
    await run_claimed_task(hydrated, run)
    assert gate.is_set()
    mid = observed["mid_run"]
    assert mid["status"] == "running"
    assert mid["result_metadata"]["units_done"] == 638
    assert mid["result_metadata"]["passes"] == 3
    assert mid["result_metadata"]["stopped_early"] is None


# ── 3. A handler stops CLEANLY before the deadline ─────────────────────────


@pytest.mark.asyncio
async def test_a_multi_pass_handler_stops_cleanly_before_the_run_ceiling(fake_supabase) -> None:
    """Max runtime 1s, passes of 0.4s: after one or two passes the lease says the
    third cannot finish. The handler stops ITSELF — not cancelled, no unit
    left half-done — and the row names the ceiling with the work counted."""
    cancelled = False
    passes = 0

    async def handler(inp: ToolRunInput) -> AgentRunResult:
        nonlocal cancelled, passes
        lease = current_run_lease()
        stop: str | None = None
        try:
            while passes < 10:
                stop = lease.stop_reason()
                if stop is not None:
                    break
                await asyncio.sleep(0.4)
                passes += 1
                await lease.progress(units_done=passes * 200)
        except asyncio.CancelledError:
            cancelled = True
            raise
        return AgentRunResult.bounded_work(
            units_done=passes * 200, failures=[], summary=f"passes={passes}", stop_reason=stop
        )

    _configure(fake_supabase, tool_runner=handler, lease_seconds=5)
    hydrated = _task(max_runtime_seconds=1)
    run = await _claim(fake_supabase, hydrated, lease_seconds=5)
    await run_claimed_task(hydrated, run)

    row = _run_row(fake_supabase)
    assert cancelled is False, "the handler was killed instead of stopping cleanly"
    assert 1 <= passes <= 2, passes
    assert row["status"] == "success", row
    assert row["result_metadata"]["units_done"] == passes * 200
    assert "run ceiling" in (row["result_metadata"]["stopped_early"] or "")
    assert "Max runtime" in (row["result_metadata"]["stopped_early"] or "")
    assert "STOPPED_EARLY" in row["result_summary"]
    assert row.get("error_message") is None, "a clean stop is not an error"


# ── 4. A hung handler is stopped at the deadline, work preserved ───────────


@pytest.mark.asyncio
async def test_a_hung_handler_is_cancelled_at_the_deadline_with_progress_preserved(
    fake_supabase,
) -> None:
    cancelled = asyncio.Event()

    async def handler(inp: ToolRunInput) -> AgentRunResult:
        lease = current_run_lease()
        await lease.progress(units_done=200, metadata={"passes": 1})
        try:
            await asyncio.sleep(3600)  # hung on a provider that never answers
        except asyncio.CancelledError:
            cancelled.set()
            raise
        return AgentRunResult(success=True)

    _configure(fake_supabase, tool_runner=handler, lease_seconds=5)
    hydrated = _task(max_runtime_seconds=1)
    run = await _claim(fake_supabase, hydrated, lease_seconds=5)
    await asyncio.wait_for(run_claimed_task(hydrated, run), timeout=5)

    assert cancelled.is_set(), "the hung handler was left running"
    row = _run_row(fake_supabase)
    assert row["status"] == "success"  # 200 units landed; the stop is named
    assert row["result_metadata"]["units_done"] == 200
    assert row["result_metadata"]["passes"] == 1
    assert "run ceiling reached" in row["result_metadata"]["stopped_early"]
    assert row["claim_token"] is None and row["finished_at"] is not None
    assert _task_row(fake_supabase)["last_run_at"] is not None


@pytest.mark.asyncio
async def test_a_hung_handler_with_no_work_is_a_failed_run(fake_supabase) -> None:
    async def handler(inp: ToolRunInput) -> AgentRunResult:
        await asyncio.sleep(3600)
        return AgentRunResult(success=True)

    sink = _Sink()
    _configure(fake_supabase, tool_runner=handler, lease_seconds=5, sink=sink)
    hydrated = _task(max_runtime_seconds=1)
    run = await _claim(fake_supabase, hydrated, lease_seconds=5)
    await asyncio.wait_for(run_claimed_task(hydrated, run), timeout=5)
    row = _run_row(fake_supabase)
    assert row["status"] == "failed"
    assert "run ceiling reached" in row["error_message"]
    assert row["result_metadata"]["units_done"] == 0
    assert sink.failures and sink.failures[0]["run_id"] == run.id


# ── 5. A lost lease stops the zombie ───────────────────────────────────────


@pytest.mark.asyncio
async def test_a_lost_lease_cancels_the_handler_instead_of_zombieing(fake_supabase) -> None:
    cancelled = asyncio.Event()
    started = asyncio.Event()

    async def handler(inp: ToolRunInput) -> AgentRunResult:
        lease = current_run_lease()
        await lease.progress(units_done=400)
        started.set()
        try:
            await asyncio.sleep(3600)
        except asyncio.CancelledError:
            cancelled.set()
            raise
        return AgentRunResult(success=True)

    _configure(fake_supabase, tool_runner=handler, lease_seconds=1)
    hydrated = _task(max_runtime_seconds=60)
    run = await _claim(fake_supabase, hydrated, lease_seconds=1)
    driver = asyncio.create_task(run_claimed_task(hydrated, run))
    await asyncio.wait_for(started.wait(), timeout=2)
    # Another claimer (or the sweep) takes the row: the token is no longer ours.
    row = _run_row(fake_supabase)
    row["claim_token"] = "someone-else"
    await asyncio.wait_for(driver, timeout=5)

    assert cancelled.is_set(), "the handler kept running after its lease was lost"
    assert row["claim_token"] == "someone-else", "we wrote over the new owner's row"
    assert _task_row(fake_supabase)["last_run_at"] is not None, "the task ran; say so"


# ── 6. The sweep preserves progress and goes through the chokepoint ────────


@pytest.mark.asyncio
async def test_the_sweep_preserves_progress_names_the_stop_and_stamps_the_task(
    fake_supabase,
) -> None:
    """An orphaned lease is an INTERRUPTION since 2026-09-14: the work stays on
    the row, the task is stamped, and a continuation carries the fire — the
    failure sink never hears a deploy (``test_run_continuation.py``)."""
    sink = _Sink()
    _configure(fake_supabase, tool_runner=None, lease_seconds=1, sink=sink)
    now = datetime.now(UTC)
    fake_supabase.rows["sch_task"].append(
        {"id": TASK, "user_id": USER, "organization_id": ORG, "enabled": True, "last_run_at": None}
    )
    fake_supabase.rows["sch_agent_task"].append(
        SchAgentTask(id=TASK, prompt="", variables={}, max_runtime_seconds=14400).model_dump()
    )
    fake_supabase.rows["sch_run"].append(
        {
            "id": "9b9e455b-b017-4852-859b-636cca464422",
            "task_id": TASK,
            "user_id": USER,
            "organization_id": ORG,
            "status": "running",
            "due_at": now,
            "claimed_at": now - timedelta(minutes=31),
            "claim_token": "tok",
            "claim_expires_at": now - timedelta(seconds=3),
            # What RunLease.progress had written after three passes, then the process died.
            "result_metadata": {"units_done": 638, "passes": 3, "stopped_early": None},
            "metadata": {"claim_protocol": 2},
        }
    )

    swept = await queries.sweep_expired_leases()

    assert swept == 1
    row = _run_row(fake_supabase)
    assert row["status"] == "interrupted", row
    assert row["result_metadata"]["units_done"] == 638, "expiry erased the work"
    assert row["result_metadata"]["passes"] == 3
    assert "lease expired" in row["result_metadata"]["stopped_early"]
    assert "638" in row["result_metadata"]["stopped_early"]
    assert row["claim_token"] is None and row["finished_at"] is not None
    assert _task_row(fake_supabase)["last_run_at"] is not None, "the task ran for 31 minutes"
    assert not sink.failures, "a worker that died is not a failed schedule"
    assert [r["status"] for r in fake_supabase.rows["sch_run"]] == ["interrupted", "queued"]


@pytest.mark.asyncio
async def test_the_sweep_closes_a_tokenless_legacy_row(fake_supabase) -> None:
    _configure(fake_supabase, tool_runner=None, lease_seconds=1)
    now = datetime.now(UTC)
    fake_supabase.rows["sch_task"].append(
        {"id": TASK, "user_id": USER, "organization_id": ORG, "enabled": True}
    )
    fake_supabase.rows["sch_run"].append(
        {
            "id": "r1",
            "task_id": TASK,
            "status": "claimed",
            "claim_token": None,
            "claim_expires_at": now - timedelta(seconds=1),
            "result_metadata": None,
        }
    )
    assert await queries.sweep_expired_leases() == 1
    assert _run_row(fake_supabase)["status"] == "failed"
    assert _run_row(fake_supabase)["result_metadata"]["units_done"] == 0


# ── 7. Worker shutdown preserves progress ──────────────────────────────────


@pytest.mark.asyncio
async def test_a_shutdown_cancel_preserves_progress(fake_supabase) -> None:
    started = asyncio.Event()

    async def handler(inp: ToolRunInput) -> AgentRunResult:
        lease = current_run_lease()
        await lease.progress(units_done=1000, metadata={"passes": 5})
        started.set()
        await asyncio.sleep(3600)
        return AgentRunResult(success=True)

    _configure(fake_supabase, tool_runner=handler, lease_seconds=5)
    hydrated = _task(max_runtime_seconds=60)
    run = await _claim(fake_supabase, hydrated, lease_seconds=5)
    driver = asyncio.create_task(run_claimed_task(hydrated, run))
    await asyncio.wait_for(started.wait(), timeout=2)
    driver.cancel()
    with pytest.raises(asyncio.CancelledError):
        await driver

    row = _run_row(fake_supabase)
    # A deploy is an interruption, never a verdict: the work stays on the row and
    # a continuation carries the fire (test_run_continuation.py).
    assert row["status"] == "interrupted", row
    assert row["result_metadata"]["units_done"] == 1000
    assert row["result_metadata"]["passes"] == 5
    assert "runner cancelled" in row["result_metadata"]["stopped_early"]
    assert row.get("error_message") is None


# ── 8. Outside the scheduler the lease is unbounded and harmless ───────────


@pytest.mark.asyncio
async def test_outside_a_scheduled_run_the_lease_is_unbounded() -> None:
    lease = current_run_lease()
    assert lease.bounded is False
    assert lease.stop_reason() is None
    assert lease.stop_reason(10_000_000) is None
    assert await lease.progress(units_done=5) is True
    assert lease.units_done == 5


# ── 9. The handler's own affordability arithmetic ──────────────────────────


def test_stop_reason_uses_the_last_unit_duration_with_margin() -> None:
    lease = lease_mod.RunLease(
        run_id="r", task_id="t", claim_token="k", lease_seconds=600, max_runtime_seconds=1800
    )
    now = lease.started_at + timedelta(seconds=1700)  # 100s left
    assert lease.stop_reason(estimated_seconds=50, now=now) is None
    reason = lease.stop_reason(estimated_seconds=120, now=now)
    assert reason and "run ceiling" in reason and "Max runtime" in reason
    assert lease.stop_reason(now=lease.started_at + timedelta(seconds=1801))
    lease.longest_unit_seconds = 80  # 80 * 1.5 = 120 > 100
    assert lease.stop_reason(now=now)


@pytest.mark.asyncio
async def test_a_renewal_that_hangs_does_not_let_a_live_run_expire(
    fake_supabase, monkeypatch
) -> None:
    """Break (found 2026-09-14): the heartbeat awaited ``lease.renew()`` with no
    bound. One renewal stuck on a pooled connection that never answers froze the
    heartbeat forever — no further renewal, no error, no log — while the handler
    kept working, so the sweep expired a LIVE run. The renewal is now bounded and
    retried well inside the lease."""
    real_renew = queries.renew_run_lease
    calls = 0

    async def renew_that_hangs_once(run_id: str, token: str, lease_seconds: int) -> bool:
        nonlocal calls
        calls += 1
        if calls == 1:
            await asyncio.Event().wait()  # never answers
        return await real_renew(run_id, token, lease_seconds)

    monkeypatch.setattr(queries, "renew_run_lease", renew_that_hangs_once)

    async def handler(inp: ToolRunInput) -> AgentRunResult:
        await asyncio.sleep(2.6)  # longer than the 2s lease
        return AgentRunResult.bounded_work(units_done=200, failures=[], summary="one long pass")

    _configure(fake_supabase, tool_runner=handler, lease_seconds=2)
    hydrated = _task(max_runtime_seconds=60)
    run = await _claim(fake_supabase, hydrated, lease_seconds=2)

    async def sweeping_scanner() -> int:
        swept = 0
        for _ in range(28):
            await asyncio.sleep(0.1)
            swept += await queries.sweep_expired_leases()
        return swept

    swept, _ = await asyncio.gather(sweeping_scanner(), run_claimed_task(hydrated, run))

    row = _run_row(fake_supabase)
    assert swept == 0, "a live run was expired because one renewal hung"
    assert row["status"] == "success", row
    assert calls >= 2, "the heartbeat never retried after the hung renewal"


def test_bounded_work_names_a_lease_stop_without_calling_it_an_error() -> None:
    r = AgentRunResult.bounded_work(
        units_done=638, failures=[], summary="passes=3", stop_reason="run ceiling: 40s left"
    )
    assert r.success is True
    assert r.error_message is None
    assert "run ceiling" in (r.stopped_early or "")
    assert "STOPPED_EARLY: run ceiling" in (r.result_summary or "")
