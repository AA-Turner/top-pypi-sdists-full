"""A leg this worker starts itself keeps every guarantee of the queue (lane 11 round 5 follow-up).

THE USE CASE: a physio clinic's "When a Patient is Booked, create a Visit" fires on the
workflow worker. Its first leg runs in this process (that is the only place the owner's
standing rule exists — an in-memory token), but it must not be a bare task:

* the run has its ``workflow.job`` row, leased to THIS worker, BEFORE the leg starts — so if
  the process dies, lease reclaim finds it and another worker runs it; that recovered leg
  carries no token, so its write follows the approval setting, and says so;
* the leg takes one of the worker's ``max_concurrent`` slots — no free slot, nothing starts
  here (the caller queues the job normally);
* a stopping runner starts nothing.

THE DOUBLE: the queue table (an in-memory stand-in for ``workflow.job`` with the same claim /
lease / reap / settle semantics). ``WorkerRunner``, ``start_claimed``, ``_process``, the
lease renewer, the standing-leg token and ``standing_rule`` are real.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

import matrx_graph.workers.runner as runner_module
from matrx_graph.db.trigger_proof import (
    RESUMED_LEG,
    StandingLeg,
    current_standing_leg,
    standing_leg,
    standing_rule,
)
from matrx_graph.workers.queue import Job
from matrx_graph.workers.runner import WorkerRunner

RUN = "6f1e2d3c-4b5a-4968-8776-655443322110"
OWNER = "5b0d7c1e-3f6a-4a52-9d8e-2c4b6e8f1a37"
LEG = StandingLeg(run_id=RUN, trigger_id="c1d2e3f4-a5b6-4c7d-8e9f-0a1b2c3d4e5f",
                  change_id="11111111-2222-4333-8444-555555555553", owner_id=OWNER,
                  definition_hash="h")


class _Queue:
    """workflow.job, in memory: a row is claimed (claimed_by + lease) or free."""

    def __init__(self) -> None:
        self.rows: dict[str, dict[str, Any]] = {}
        self.process_alive = True

    async def enqueue_claimed(self, *, run_id, kind, inputs=None, max_steps=1000,
                              worker_id=None, visibility_timeout_seconds=600):  # noqa: ANN001
        job_id = f"job-{len(self.rows) + 1}"
        token = f"worker-1:{job_id}"
        self.rows[job_id] = {"run_id": run_id, "kind": kind, "inputs": inputs or {},
                             "claimed_by": token, "attempt": 1,
                             "lease_until": datetime.now(UTC)
                             + timedelta(seconds=visibility_timeout_seconds),
                             "done": False}
        return Job(job_id=job_id, run_id=run_id, kind=kind, inputs=inputs or {},
                   max_steps=max_steps, attempt=1, claimed_by=token)

    async def claim_one(self, *, worker_id=None, visibility_timeout_seconds=600,
                        capabilities=None):  # noqa: ANN001
        for job_id, row in self.rows.items():
            if row["claimed_by"] is None and not row["done"]:
                row["claimed_by"] = f"worker-2:{job_id}"
                row["attempt"] += 1
                row["lease_until"] = datetime.now(UTC) + timedelta(seconds=600)
                return Job(job_id=job_id, run_id=row["run_id"], kind=row["kind"],
                           inputs=row["inputs"], attempt=row["attempt"],
                           claimed_by=row["claimed_by"])
        return None

    async def reap_expired_leases(self, *, grace_seconds: int = 120) -> int:
        reaped = 0
        for row in self.rows.values():
            if row["claimed_by"] and not row["done"] and row["lease_until"] < datetime.now(UTC):
                row["claimed_by"] = None
                reaped += 1
        return reaped

    async def complete(self, job_id, *, claimed_by=None):  # noqa: ANN001
        if self.process_alive and self.rows[job_id]["claimed_by"] == claimed_by:
            self.rows[job_id]["done"] = True

    async def fail(self, job_id, **_kw):  # noqa: ANN001
        # A process that died cannot write its own failure: only the lease expiry is left.
        if self.process_alive:
            self.rows[job_id]["claimed_by"] = None

    async def renew_lease(self, job_id, *, claimed_by=None, **_kw):  # noqa: ANN001
        return self.rows[job_id]["claimed_by"] == claimed_by


@pytest.fixture
def queue(monkeypatch):
    q = _Queue()
    for name in ("enqueue_claimed", "claim_one", "reap_expired_leases", "complete", "fail",
                 "renew_lease"):
        monkeypatch.setattr(runner_module, name, getattr(q, name))

    async def _quiet(*_a, **_kw):
        return None

    monkeypatch.setattr(runner_module, "capture_error", _quiet)
    return q


async def _app(job):  # noqa: ANN001
    return object()


async def _running(runner: WorkerRunner) -> asyncio.Task:
    task = asyncio.create_task(runner.run_forever())
    for _ in range(100):
        if runner._slots is not None:
            break
        await asyncio.sleep(0.005)
    return task


async def test_a_killed_leg_is_recovered_and_its_write_follows_the_approval_setting(
    queue, monkeypatch
):
    # The rule as it would behave switched on (it ships OFF — round 8); the recovered leg must
    # still lose it.
    from matrx_graph.db import trigger_proof

    monkeypatch.setattr(trigger_proof, "STANDING_RULE_ENABLED", True)
    seen: dict[str, Any] = {}
    stuck = asyncio.Event()

    async def first_leg(job, app):  # noqa: ANN001
        # The job row exists and is leased to this worker BEFORE the leg does anything.
        row = queue.rows[job.job_id]
        seen["leased_before_start"] = (row["claimed_by"] == job.claimed_by,
                                       row["lease_until"] > datetime.now(UTC))
        seen["token_in_first_leg"] = current_standing_leg()
        await stuck.wait()  # dies here — before its first step

    runner = WorkerRunner(job_runner=first_leg, app_context_factory=_app,
                          poll_interval_seconds=0.01, stop_grace_seconds=0.01)
    loop = await _running(runner)
    started = await runner.start_claimed(run_id=RUN, inputs={"trigger": {}}, max_steps=5,
                                         context=lambda: standing_leg(LEG))
    assert started is True
    for _ in range(100):
        if "token_in_first_leg" in seen:
            break
        await asyncio.sleep(0.005)
    assert seen["leased_before_start"] == (True, True), seen
    assert seen["token_in_first_leg"] == LEG

    # THE PROCESS DIES: nothing it would have written gets written; its lease runs out.
    queue.process_alive = False
    runner.stop()
    await loop
    [row] = queue.rows.values()
    assert row["claimed_by"] is not None and not row["done"], "the dead process settled its job"
    row["lease_until"] = datetime.now(UTC) - timedelta(seconds=1)
    queue.process_alive = True

    # RECOVERY: another worker reaps the expired lease and runs the job — without the token.
    async def recovered_leg(job, app):  # noqa: ANN001
        seen["token_in_recovery"] = current_standing_leg()
        verdict = await standing_rule(job.run_id, owner_id=OWNER, write_node_id="make_visit")
        seen["write"] = (verdict.trigger, verdict.why_not)

    recovery = WorkerRunner(job_runner=recovered_leg, app_context_factory=_app,
                            poll_interval_seconds=0.01, stop_grace_seconds=1)
    loop2 = await _running(recovery)
    for _ in range(200):
        if "write" in seen:
            break
        await asyncio.sleep(0.005)
    recovery.stop()
    await loop2
    assert seen["token_in_recovery"] is None
    assert seen["write"] == (None, RESUMED_LEG), seen
    assert row["done"] is True


async def test_no_free_slot_starts_nothing_here(queue):
    hold = asyncio.Event()

    async def busy(job, app):  # noqa: ANN001
        await hold.wait()

    runner = WorkerRunner(job_runner=busy, app_context_factory=_app, max_concurrent=1,
                          poll_interval_seconds=0.01, stop_grace_seconds=0.01)
    loop = await _running(runner)
    assert await runner.start_claimed(run_id=RUN, inputs={}, max_steps=5) is True
    assert await runner.start_claimed(run_id=RUN, inputs={}, max_steps=5) is False
    assert len(queue.rows) == 1, "a leg past max_concurrent created a job"
    hold.set()
    runner.stop()
    await loop


async def test_a_runner_that_is_not_running_starts_nothing(queue):
    async def never(job, app):  # noqa: ANN001
        raise AssertionError("a stopped runner ran a leg")

    runner = WorkerRunner(job_runner=never, app_context_factory=_app)
    assert await runner.start_claimed(run_id=RUN, inputs={}, max_steps=5) is False
    assert queue.rows == {}
