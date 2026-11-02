"""Lane K1b (2026-10-21): a copy that is told "not ours" never strands its run, and a copy that really lost its job
stops at once — whoever notices first.

- B1: on a job's LAST attempt the reaper dead-letters (never requeues) an expired lease. After a database outage that
  outlasted the lease, the live copy then read "not ours", cancelled itself and skipped its terminal write — and no
  copy ever claims a dead-lettered job, so the run was stranded. Now the live copy takes the job back and finishes.
  A job the reaper REQUEUED (another copy may run it) still stops the old copy.
- B2: the work's own ``check`` (it reads the job row more often than the renewal) raised ``JobLeaseLost`` inside one
  node; run-ahead swallowed it and the copy kept checkpointing and routing until the next renewal. Now marking the
  lease lost cancels the copy's owner task at once.
- M1: a renewal that lands just after ``complete()`` commits is not a lost lease.
- M4: a copy with no claim token read every later claim as its own.

The job row lives in an in-memory stand-in of ``WfJob`` that answers the queue's real queries.
"""

from __future__ import annotations

import asyncio
import types
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from matrx_graph.db import _registry
from matrx_graph.workers import job_lease
from matrx_graph.workers import queue as queue_mod
from matrx_graph.workers import runner as runner_mod

JOB = "c1d89868-ef16-4d9b-82e6-dd5279775886"
RUN = "8749d414-0000-4c39-9a5e-00000000k1bb"


class _Jobs:
    """One wf_job row, filtered and updated the way the ORM does for the lookups the queue uses."""

    def __init__(self, **row):
        self.row = {"id": JOB, "attempt": 3, "max_attempts": 3, **row}

    def _match(self, filters):
        for key, want in filters.items():
            name, _, op = key.partition("__")
            have = self.row.get(name)
            if op == "isnull":
                if (have is None) != bool(want):
                    return False
            elif op == "gt":
                if have is None or not have > want:
                    return False
            elif op == "lt":
                if have is None or not have < want:
                    return False
            elif have != want:
                return False
        return True

    def filter(self, *_compare, **filters):
        jobs = self

        class _Q:
            async def all(self, use_cache=True):  # noqa: ARG002
                return [dict(jobs.row)] if jobs._match(filters) else []

            async def update(self, **updates):
                if not jobs._match(filters):
                    return SimpleNamespace(updated_rows=[])
                jobs.row.update(updates)
                return SimpleNamespace(updated_rows=[dict(jobs.row)])

        return _Q()

    async def update_where(self, filters, **updates):
        if not self._match(filters):
            return SimpleNamespace(rows_affected=0)
        self.row.update(updates)
        return SimpleNamespace(rows_affected=1)


def _dead_lettered_by_the_reaper() -> dict:
    return {"claimed_at": None, "claimed_by": None, "visible_at": datetime.now(UTC) + timedelta(days=36_500),
            "last_error": {"queue_state": "dead_letter", "type": "lease_expired", "retry_exhausted": True}}


def _requeued_by_the_reaper() -> dict:
    return {"claimed_at": None, "claimed_by": None, "visible_at": datetime.now(UTC),
            "last_error": {"queue_state": "pending", "type": "lease_expired"}}


@pytest.fixture
def jobs(monkeypatch):
    store = _Jobs(claimed_at=datetime.now(UTC), claimed_by="worker-1:A", visible_at=datetime.now(UTC) + timedelta(minutes=10),
                  last_error=None)
    monkeypatch.setattr(_registry, "get_model", lambda _key: store)

    async def capture_error(*_a, **_k):
        return None

    real_sleep = asyncio.sleep
    monkeypatch.setattr(runner_mod, "capture_error", capture_error)
    monkeypatch.setattr(runner_mod, "asyncio", types.SimpleNamespace(sleep=lambda s: real_sleep(0.02),
                                                                       Task=asyncio.Task, CancelledError=asyncio.CancelledError))
    return store


def _copy(jobs: _Jobs, *, work_seconds: float, reaper_turns_row_into: dict):
    """One copy of the run as the worker runs it: the runner's real renewal loop beside the work; part way the reaper
    rewrites the row (the outage outlasted the lease). Returns (outcome, lease)."""

    async def main():
        out: dict = {}
        me = asyncio.current_task()
        lease = job_lease.JobLease(job_id=JOB, run_id=RUN, claimed_by="worker-1:A", owner=me, visibility_timeout=600)
        stub = types.SimpleNamespace(_visibility_timeout=30)
        renewer = asyncio.create_task(runner_mod.WorkerRunner._renew_loop(stub, JOB, claimed_by="worker-1:A", lease=lease, owner=me))
        try:
            await asyncio.sleep(0.03)
            jobs.row.update(reaper_turns_row_into)
            await asyncio.sleep(work_seconds)
            await job_lease.JobLease.check(lease)
            out["outcome"] = "finished"
        except asyncio.CancelledError:
            out["outcome"] = "cancelled"
        finally:
            renewer.cancel()
        return out["outcome"], lease

    return asyncio.run(main())


def test_a_false_dead_letter_on_the_last_attempt_is_taken_back_and_the_run_finishes(jobs):
    outcome, lease = _copy(jobs, work_seconds=0.2, reaper_turns_row_into=_dead_lettered_by_the_reaper())
    assert outcome == "finished", "the live copy stopped on a dead-lettered job: nothing would ever end its run"
    assert not lease.lost
    assert jobs.row["claimed_by"] == "worker-1:A" and jobs.row["claimed_at"] is not None, "the job was not taken back"
    assert jobs.row["last_error"]["type"] == "false_dead_taken_back"


def test_a_requeued_job_still_stops_the_old_copy(jobs):
    outcome, lease = _copy(jobs, work_seconds=0.2, reaper_turns_row_into=_requeued_by_the_reaper())
    assert outcome == "cancelled", "a copy whose job was requeued (another copy may run it) kept going"
    assert lease.lost


def test_a_job_another_worker_claimed_is_never_taken_back(jobs):
    claimed = {"claimed_at": datetime.now(UTC), "claimed_by": "worker-2:B", "visible_at": datetime.now(UTC) + timedelta(minutes=10),
               "last_error": None}
    outcome, lease = _copy(jobs, work_seconds=0.2, reaper_turns_row_into=claimed)
    assert outcome == "cancelled" and lease.lost
    assert jobs.row["claimed_by"] == "worker-2:B"


def test_the_work_noticing_the_loss_first_stops_the_whole_copy_at_once(jobs):
    """B2: the node's own check raises inside a child task (run-ahead never reads its result); the copy's owner task
    must be cancelled right then, not at the next renewal."""

    async def main():
        me = asyncio.current_task()
        lease = job_lease.JobLease(job_id=JOB, run_id=RUN, claimed_by="worker-1:A", owner=me)
        jobs.row.update(_requeued_by_the_reaper())
        with job_lease.holding(lease):
            node = asyncio.create_task(job_lease.check())  # a node in run-ahead: nobody awaits its result
        try:
            await asyncio.sleep(5)  # the copy would go on to checkpoint and route
            return "kept going", node
        except asyncio.CancelledError:
            return "stopped", node

    outcome, node = asyncio.run(main())
    assert outcome == "stopped"
    assert node.done()


def test_a_renewal_landing_after_the_settle_is_not_a_loss(jobs):
    async def main():
        me = asyncio.current_task()
        lease = job_lease.JobLease(job_id=JOB, run_id=RUN, claimed_by="worker-1:A", owner=me)
        lease.settling = True
        jobs.row.update({"claimed_at": None, "claimed_by": None, "last_error": {"queue_state": "succeeded"}})
        kept = await lease.not_ours("the queue reaped or settled the job")
        await asyncio.sleep(0)
        return kept, lease

    kept, lease = asyncio.run(main())
    assert kept and not lease.lost


def test_a_copy_without_a_claim_token_sees_another_claim(jobs):
    jobs.row.update({"claimed_at": datetime.now(UTC), "claimed_by": "worker-2:B"})
    lease = job_lease.JobLease(job_id=JOB, run_id=RUN, claimed_by=None)
    assert asyncio.run(lease.still_held()) is False
