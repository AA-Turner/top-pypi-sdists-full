"""Unit tests for matrx_graph.workers primitives.

These tests exercise the in-memory parts of the queue module. Queue
round-trip against real Postgres is covered by the Phase 2 integration
tests (skipped unless MATRX_GRAPH_TEST_DB=1).
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_graph.workers import (
    FailureClass,
    Job,
    classify_failure,
    retry_delay_seconds,
)


def test_job_model_defaults():
    job = Job(job_id="j1", run_id="r1", kind="start")
    assert job.inputs == {}
    assert job.resume_value == {}
    assert job.max_steps == 1000
    assert job.attempt == 0
    assert job.max_attempts == 3
    assert job.checkpoint_id is None
    assert job.claimed_by is None


def test_job_model_requires_run_id():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Job.model_validate({"job_id": "j1", "kind": "start"})


def test_job_model_validates_kind():
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        Job(job_id="j1", run_id="r1", kind="other")  # type: ignore[arg-type]


def test_job_json_roundtrip():
    job = Job(
        job_id="j1",
        run_id="r1",
        kind="resume",
        checkpoint_id="cp-1",
        resume_value={"answer": "blue"},
        inputs={"x": 1},
        max_steps=500,
        attempt=2,
    )
    dumped = job.model_dump(mode="json")
    re_parsed = Job.model_validate(dumped)
    assert re_parsed == job


def test_job_model_is_frozen():
    job = Job(job_id="j1", run_id="r1", kind="start")
    with pytest.raises(Exception):
        job.run_id = "other"  # type: ignore[misc]


class _HttpError(RuntimeError):
    def __init__(self, status_code: int) -> None:
        super().__init__(f"HTTP {status_code}")
        self.status_code = status_code


@pytest.mark.parametrize("status", [408, 425, 429, 500, 502, 503, 504])
def test_failure_classifier_retries_only_transient_http(status: int):
    disposition = classify_failure(_HttpError(status))
    assert disposition.failure_class is FailureClass.RETRYABLE
    assert disposition.reason == f"http_{status}"


@pytest.mark.parametrize("status", [400, 401, 403, 404, 409, 422])
def test_failure_classifier_dead_letters_terminal_http(status: int):
    disposition = classify_failure(_HttpError(status))
    assert disposition.failure_class is FailureClass.TERMINAL
    assert disposition.reason == f"http_{status}"


def test_failure_classifier_defaults_programming_errors_terminal():
    assert classify_failure(ValueError("bad workflow config")).retryable is False
    assert classify_failure(TimeoutError("provider timed out")).retryable is True
    transport_error = type("TransportError", (RuntimeError,), {})
    assert classify_failure(transport_error("socket closed")).retryable is True


def test_failure_classifier_follows_wrapped_exception_chain():
    try:
        try:
            raise ConnectionError("connection reset")
        except ConnectionError as exc:
            raise RuntimeError("wrapped") from exc
    except RuntimeError as wrapped:
        disposition = classify_failure(wrapped)
    assert disposition.failure_class is FailureClass.RETRYABLE
    assert disposition.reason == "ConnectionError"


def test_retry_delay_is_exponential_jittered_and_bounded(monkeypatch):
    monkeypatch.setattr("matrx_utils.backoff.random.uniform", lambda _a, _b: 1.0)
    assert retry_delay_seconds(1) == 30
    assert retry_delay_seconds(2) == 60
    assert retry_delay_seconds(3) == 120
    assert retry_delay_seconds(99) == 300
    with pytest.raises(ValueError, match="attempt must be"):
        retry_delay_seconds(0)


def test_claim_tokens_are_unique_even_for_one_worker_process():
    from matrx_graph.workers.queue import _claim_token

    first = _claim_token("worker-a")
    second = _claim_token("worker-a")
    assert first.startswith("worker-a:")
    assert second.startswith("worker-a:")
    assert first != second


async def test_complete_retains_terminal_row_and_fences_owner(monkeypatch):
    from matrx_graph.db import _registry
    from matrx_graph.workers.queue import complete

    calls: list[tuple[dict[str, object], dict[str, object]]] = []

    class _Model:
        @classmethod
        async def update_where(cls, filters, **updates):
            calls.append((filters, updates))
            return SimpleNamespace(rows_affected=1)

        @classmethod
        async def delete_where(cls, **_filters):
            pytest.fail("terminal queue rows must never be deleted")

    monkeypatch.setattr(_registry, "get_model", lambda _key: _Model)
    await complete(
        "00000000-0000-0000-0000-000000000001",
        claimed_by="worker-a",
    )

    filters, updates = calls[0]
    assert filters["claimed_by"] == "worker-a"
    assert updates["claimed_at"] is None
    assert updates["claimed_by"] is None
    assert updates["last_error"] == {
        "queue_state": "succeeded",
        "type": "terminal_success",
    }


async def test_terminal_failure_dead_letters_immediately(monkeypatch):
    from matrx_graph.db import _registry
    from matrx_graph.workers.queue import fail

    calls: list[tuple[dict[str, object], dict[str, object]]] = []

    class _Model:
        @classmethod
        async def update_where(cls, filters, **updates):
            calls.append((filters, updates))
            return SimpleNamespace(rows_affected=1)

    monkeypatch.setattr(_registry, "get_model", lambda _key: _Model)
    await fail(
        "00000000-0000-0000-0000-000000000002",
        error={"type": "ValueError", "message": "bad config"},
        retryable=False,
        attempt=1,
        claimed_by="worker-a",
    )

    filters, updates = calls[0]
    assert filters["claimed_by"] == "worker-a"
    assert updates["last_error"]["queue_state"] == "dead_letter"
    assert updates["last_error"]["retryable"] is False


async def test_fail_without_attempt_reads_row_and_dead_letters_when_exhausted(monkeypatch):
    """A caller that omits attempt/max_attempts must get the ROW's real
    counters — a fixed attempt=1 default silently resurrected exhausted jobs
    (the infinite-retry class fail() exists to kill). Exhausted → dead_letter,
    far-future visible_at, retry_exhausted marker."""
    from datetime import UTC, datetime, timedelta

    from matrx_graph.db import _registry
    from matrx_graph.workers.queue import fail

    calls: list[tuple[dict[str, object], dict[str, object]]] = []

    class _Model:
        @classmethod
        async def get_or_none(cls, **_filters):
            return SimpleNamespace(attempt=3, max_attempts=3)  # exhausted row

        @classmethod
        async def update_where(cls, filters, **updates):
            calls.append((filters, updates))
            return SimpleNamespace(rows_affected=1)

    monkeypatch.setattr(_registry, "get_model", lambda _key: _Model)
    await fail(
        "00000000-0000-0000-0000-000000000003",
        error={"type": "Boom", "message": "x"},
        # attempt / max_attempts deliberately omitted — must be read from the row
    )

    _filters, updates = calls[0]
    assert updates["last_error"]["queue_state"] == "dead_letter"
    assert updates["last_error"]["retry_exhausted"] is True
    assert updates["visible_at"] > datetime.now(UTC) + timedelta(days=365 * 50)
    assert updates["claimed_at"] is None and updates["claimed_by"] is None


async def test_fail_without_attempt_reads_row_and_retries_when_budget_remains(monkeypatch):
    from datetime import UTC, datetime, timedelta

    from matrx_graph.db import _registry
    from matrx_graph.workers.queue import fail

    calls: list[tuple[dict[str, object], dict[str, object]]] = []

    class _Model:
        @classmethod
        async def get_or_none(cls, **_filters):
            return SimpleNamespace(attempt=1, max_attempts=3)  # budget remains

        @classmethod
        async def update_where(cls, filters, **updates):
            calls.append((filters, updates))
            return SimpleNamespace(rows_affected=1)

    monkeypatch.setattr(_registry, "get_model", lambda _key: _Model)
    await fail(
        "00000000-0000-0000-0000-000000000004",
        error={"type": "Boom", "message": "x"},
    )

    _filters, updates = calls[0]
    assert updates["last_error"]["queue_state"] == "pending"
    assert updates["last_error"]["retryable"] is True
    # A retry is scheduled with bounded backoff, never a far-future dead-letter.
    assert updates["visible_at"] < datetime.now(UTC) + timedelta(hours=1)


async def test_runner_reconciles_expired_leases_before_claiming(monkeypatch):
    from matrx_graph.workers import runner as runner_module
    from matrx_graph.workers.runner import WorkerRunner

    reconciliations: list[bool] = []

    async def _reap():
        reconciliations.append(True)
        return 0

    async def _unused_job_runner(_job, _app):
        pytest.fail("stopped runner must not claim work")

    async def _unused_factory(_job):
        pytest.fail("stopped runner must not build app context")

    monkeypatch.setattr(runner_module, "reap_expired_leases", _reap)
    runner = WorkerRunner(
        job_runner=_unused_job_runner,
        app_context_factory=_unused_factory,
    )
    runner.stop()
    await runner.run_forever()
    assert reconciliations == [True]


async def test_runner_survives_transient_job_claim_failure(monkeypatch, caplog):
    from matrx_graph.workers import runner as runner_module
    from matrx_graph.workers.runner import WorkerRunner

    claims = 0
    captured: list[tuple[BaseException, str]] = []

    async def _reap():
        return 0

    async def _claim_one(**_kwargs):
        nonlocal claims
        claims += 1
        if claims == 1:
            raise TimeoutError("workflow.job claim timed out")
        runner.stop()
        return None

    async def _capture_error(exc, *, kind, **_kwargs):
        captured.append((exc, kind))

    async def _unused_job_runner(_job, _app):
        pytest.fail("no job should be dispatched")

    async def _unused_factory(_job):
        pytest.fail("no app context should be built")

    monkeypatch.setattr(runner_module, "reap_expired_leases", _reap)
    monkeypatch.setattr(runner_module, "claim_one", _claim_one)
    monkeypatch.setattr(runner_module, "capture_error", _capture_error)
    runner = WorkerRunner(
        job_runner=_unused_job_runner,
        app_context_factory=_unused_factory,
        poll_interval_seconds=0,
    )

    await runner.run_forever()

    assert claims == 2
    assert captured and captured[0][1] == "workflow_job_claim_failed"
    assert "job claim failed; retrying" in caplog.text


async def test_runner_classifies_and_fences_terminal_failure(monkeypatch):
    from matrx_graph.workers import runner as runner_module
    from matrx_graph.workers.runner import WorkerRunner

    captured: dict[str, object] = {}

    async def _run_job(_job, _app):
        raise ValueError("invalid workflow definition")

    async def _app_factory(_job):
        return object()

    async def _fail(job_id, **kwargs):
        captured.update(job_id=job_id, **kwargs)

    monkeypatch.setattr(runner_module, "fail", _fail)
    runner = WorkerRunner(job_runner=_run_job, app_context_factory=_app_factory)
    job = Job(
        job_id="00000000-0000-0000-0000-000000000003",
        run_id="00000000-0000-0000-0000-000000000004",
        kind="start",
        attempt=2,
        claimed_by="worker-a",
    )
    await runner._process(job)

    assert captured["retryable"] is False
    assert captured["attempt"] == 2
    assert captured["claimed_by"] == "worker-a"


async def test_single_job_factory_failure_is_settled_not_orphaned(monkeypatch):
    from matrx_graph.workers import runner as runner_module

    job = Job(
        job_id="00000000-0000-0000-0000-000000000005",
        run_id="00000000-0000-0000-0000-000000000006",
        kind="start",
        attempt=1,
        claimed_by="worker-a",
    )
    captured: dict[str, object] = {}

    async def _claim_one(**_kwargs):
        return job

    async def _factory(_job):
        raise TimeoutError("context database timed out")

    async def _unused_runner(_job, _app):
        pytest.fail("job runner must not execute after factory failure")

    async def _fail(job_id, **kwargs):
        captured.update(job_id=job_id, **kwargs)

    monkeypatch.setattr(runner_module, "claim_one", _claim_one)
    monkeypatch.setattr(runner_module, "fail", _fail)
    with pytest.raises(TimeoutError, match="context database"):
        await runner_module.run_single_job(_unused_runner, _factory)

    assert captured["job_id"] == job.job_id
    assert captured["retryable"] is True
    assert captured["claimed_by"] == "worker-a"


async def test_worker_survives_failure_state_write_error(monkeypatch, caplog):
    from matrx_graph.workers import runner as runner_module
    from matrx_graph.workers.runner import WorkerRunner

    async def _run_job(_job, _app):
        raise ValueError("bad workflow")

    async def _app_factory(_job):
        return object()

    async def _fail(_job_id, **_kwargs):
        raise ConnectionError("database unavailable")

    monkeypatch.setattr(runner_module, "fail", _fail)
    runner = WorkerRunner(job_runner=_run_job, app_context_factory=_app_factory)
    job = Job(
        job_id="00000000-0000-0000-0000-000000000007",
        run_id="00000000-0000-0000-0000-000000000008",
        kind="start",
        attempt=1,
        claimed_by="worker-a",
    )
    await runner._process(job)

    assert "leaving the claim for lease reconciliation" in caplog.text


# ── Bounded parallelism (2026-09-17) ────────────────────────────────────────
#
# The runner used to be strictly serial: claim → await the whole job → claim.
# One slow job held every other workflow on the platform. These four tests are
# forcing functions for the fix — each one FAILS against the serial loop, and
# three of them fail against a plausible-looking wrong parallel loop too.


def _queue_of(jobs, runner_ref):
    """A claim_one that hands out `jobs` once, then stops the runner and
    reports an empty queue."""
    remaining = list(jobs)

    async def _claim_one(**_kwargs):
        if remaining:
            return remaining.pop(0)
        runner_ref["runner"].stop()
        return None

    return _claim_one


def _job(n: int) -> Job:
    return Job(
        job_id=f"00000000-0000-0000-0000-00000000010{n}",
        run_id=f"00000000-0000-0000-0000-00000000020{n}",
        kind="start",
        attempt=1,
        claimed_by=f"worker-a:{n}",
    )


@pytest.fixture
def quiet_queue(monkeypatch):
    """Neutralize every queue write so these tests measure the LOOP only."""
    from matrx_graph.workers import runner as runner_module

    async def _noop(*_args, **_kwargs):
        return None

    async def _reap():
        return 0

    monkeypatch.setattr(runner_module, "reap_expired_leases", _reap)
    monkeypatch.setattr(runner_module, "complete", _noop)
    monkeypatch.setattr(runner_module, "fail", _noop)
    monkeypatch.setattr(runner_module, "renew_lease", _noop)
    monkeypatch.setattr(runner_module, "capture_error", _noop)
    return runner_module


async def test_concurrent_jobs_finish_in_one_slow_job_s_time(quiet_queue, monkeypatch):
    """FORCING FUNCTION: five jobs, five slots — all five run AT ONCE.

    Deterministic (no wall-clock): every job waits on a 5-party barrier, which
    only releases when all five are in flight together. Against the serial
    loop the first job waits forever and the bounded wait_for fails the test.
    """
    import asyncio

    from matrx_graph.workers.runner import WorkerRunner

    finished: list[str] = []
    barrier = asyncio.Barrier(5)

    async def _run_job(job, _app):
        await barrier.wait()
        finished.append(job.job_id)

    async def _app_factory(_job):
        return object()

    ref: dict[str, WorkerRunner] = {}
    monkeypatch.setattr(quiet_queue, "claim_one", _queue_of([_job(i) for i in range(5)], ref))
    runner = WorkerRunner(
        job_runner=_run_job,
        app_context_factory=_app_factory,
        poll_interval_seconds=0,
        max_concurrent=5,
    )
    ref["runner"] = runner

    await asyncio.wait_for(runner.run_forever(), timeout=10)

    assert len(finished) == 5


async def test_the_bound_is_respected(quiet_queue, monkeypatch):
    """The semaphore is a REAL ceiling: never more than max_concurrent at once."""
    import asyncio

    from matrx_graph.workers.runner import WorkerRunner

    live = 0
    peak = 0

    async def _run_job(_job, _app):
        nonlocal live, peak
        live += 1
        peak = max(peak, live)
        try:
            await asyncio.sleep(0.05)
        finally:
            live -= 1

    async def _app_factory(_job):
        return object()

    ref: dict[str, WorkerRunner] = {}
    monkeypatch.setattr(quiet_queue, "claim_one", _queue_of([_job(i) for i in range(8)], ref))
    runner = WorkerRunner(
        job_runner=_run_job,
        app_context_factory=_app_factory,
        poll_interval_seconds=0,
        max_concurrent=3,
    )
    ref["runner"] = runner
    await runner.run_forever()

    assert peak == 3, f"peak concurrency was {peak}, expected the bound 3"


async def test_a_failing_job_does_not_touch_its_neighbours(quiet_queue, monkeypatch):
    """One job blowing up settles ONLY its own queue row; the others finish."""
    import asyncio

    from matrx_graph.workers.runner import WorkerRunner

    failed_job_ids: list[str] = []
    completed_job_ids: list[str] = []
    finished: list[str] = []

    async def _fail(job_id, **_kwargs):
        failed_job_ids.append(job_id)

    async def _complete(job_id, **_kwargs):
        completed_job_ids.append(job_id)

    monkeypatch.setattr(quiet_queue, "fail", _fail)
    monkeypatch.setattr(quiet_queue, "complete", _complete)

    async def _run_job(job, _app):
        if job.job_id.endswith("2"):
            raise ValueError("this workflow definition is invalid")
        await asyncio.sleep(0.05)
        finished.append(job.job_id)

    async def _app_factory(_job):
        return object()

    ref: dict[str, WorkerRunner] = {}
    monkeypatch.setattr(quiet_queue, "claim_one", _queue_of([_job(i) for i in range(4)], ref))
    runner = WorkerRunner(
        job_runner=_run_job,
        app_context_factory=_app_factory,
        poll_interval_seconds=0,
        max_concurrent=4,
    )
    ref["runner"] = runner
    await runner.run_forever()

    assert len(failed_job_ids) == 1 and failed_job_ids[0].endswith("2")
    assert len(finished) == 3
    assert sorted(completed_job_ids) == sorted(finished)


async def test_stop_drains_in_flight_jobs(quiet_queue, monkeypatch):
    """stop() takes no NEW work and lets the running jobs finish."""
    import asyncio

    from matrx_graph.workers.runner import WorkerRunner

    finished: list[str] = []
    started = asyncio.Event()

    async def _run_job(job, _app):
        started.set()
        await asyncio.sleep(0.25)
        finished.append(job.job_id)

    async def _app_factory(_job):
        return object()

    jobs = [_job(i) for i in range(3)]
    claimed: list[str] = []

    async def _claim_one(**_kwargs):
        if jobs:
            job = jobs.pop(0)
            claimed.append(job.job_id)
            return job
        await asyncio.sleep(0.01)
        return None

    monkeypatch.setattr(quiet_queue, "claim_one", _claim_one)
    runner = WorkerRunner(
        job_runner=_run_job,
        app_context_factory=_app_factory,
        poll_interval_seconds=0,
        max_concurrent=3,
        stop_grace_seconds=5.0,
    )

    loop_task = asyncio.create_task(runner.run_forever())
    await started.wait()
    await asyncio.sleep(0.02)
    in_flight_at_stop = runner.in_flight_count
    runner.stop()
    await loop_task

    assert in_flight_at_stop >= 1
    # Every job that was in flight when stop() fired ran to completion.
    assert len(finished) == in_flight_at_stop
    # And nothing new was claimed after the stop.
    assert len(claimed) == in_flight_at_stop


async def test_stop_cancels_a_job_that_outlives_the_grace(quiet_queue, monkeypatch):
    """The drain is BOUNDED — a job that will not end is canceled, loudly."""
    import asyncio

    from matrx_graph.workers.runner import WorkerRunner

    cancelled = asyncio.Event()
    started = asyncio.Event()

    async def _run_job(_job, _app):
        started.set()
        try:
            await asyncio.sleep(30)
        except asyncio.CancelledError:
            cancelled.set()
            raise

    async def _app_factory(_job):
        return object()

    jobs = [_job(0)]

    async def _claim_one(**_kwargs):
        if jobs:
            return jobs.pop(0)
        await asyncio.sleep(0.01)
        return None

    monkeypatch.setattr(quiet_queue, "claim_one", _claim_one)
    runner = WorkerRunner(
        job_runner=_run_job,
        app_context_factory=_app_factory,
        poll_interval_seconds=0,
        max_concurrent=2,
        stop_grace_seconds=0.05,
    )

    loop_task = asyncio.create_task(runner.run_forever())
    # Stop only once the job is really in flight (a fixed sleep raced the claim
    # under machine load, so stop() could land before any job existed).
    await asyncio.wait_for(started.wait(), timeout=10)
    runner.stop()
    await asyncio.wait_for(loop_task, timeout=10)

    assert cancelled.is_set()


async def test_each_concurrent_job_sees_only_its_own_app_context(quiet_queue, monkeypatch):
    """FORCING FUNCTION for the contextvar leak.

    Concurrent jobs install an ambient AppContext (aidream's worker does, at
    the tail of every job). Each job task must observe ITS OWN and nothing
    else — and the loop itself must be left clean. Under the old serial
    ``await self._process(job)`` the context was set in the LOOP's context and
    outlived the job; this test pins that it cannot.
    """
    import asyncio

    from matrx_connect.context.app_context import set_app_context, try_get_app_context

    from matrx_graph.workers.runner import WorkerRunner

    observed: dict[str, list[str]] = {}

    async def _app_factory(job):
        return SimpleNamespace(user_id=f"user-for-{job.job_id[-1]}")

    async def _run_job(job, app):
        set_app_context(app)
        seen: list[str] = []
        for _ in range(5):
            await asyncio.sleep(0.01)
            current = try_get_app_context()
            seen.append(getattr(current, "user_id", None))
        observed[job.job_id] = seen

    ref: dict[str, WorkerRunner] = {}
    monkeypatch.setattr(quiet_queue, "claim_one", _queue_of([_job(i) for i in range(4)], ref))
    runner = WorkerRunner(
        job_runner=_run_job,
        app_context_factory=_app_factory,
        poll_interval_seconds=0,
        max_concurrent=4,
    )
    ref["runner"] = runner
    await runner.run_forever()

    assert len(observed) == 4
    for job_id, seen in observed.items():
        mine = f"user-for-{job_id[-1]}"
        assert seen == [mine] * 5, f"job {job_id} saw a neighbour's context: {seen}"
    # The claim loop's own context was never contaminated.
    assert try_get_app_context() is None


async def test_a_worker_that_may_run_no_jobs_is_refused():
    from matrx_graph.workers.runner import WorkerRunner

    async def _unused(*_a, **_k):
        return None

    with pytest.raises(ValueError, match="max_concurrent must be >= 1"):
        WorkerRunner(
            job_runner=_unused,
            app_context_factory=_unused,
            max_concurrent=0,
        )
