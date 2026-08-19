# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for the background cluster-status refresher and its driver-loop wiring.

* the drain path performs no synchronous listing (it only reads a snapshot),
* the refresher publishes timestamped snapshots with bounded, reported
  staleness and degrades gracefully on failure,
* the task-failure OOM-evidence path still fetches pod status fresh.
"""

from __future__ import annotations

import inspect
import logging
import threading
import time
import uuid
from collections import Counter
from typing import TYPE_CHECKING, Any, NoReturn

import pyarrow as pa
import pytest
import ray.exceptions

import geneva.runners.ray.pipeline as ray_pipeline
from geneva import FatalWorkerOOMError, udf
from geneva.apply.task import BackfillUDFTask
from geneva.checkpoint import CheckpointStore
from geneva.jobs.config import JobConfig
from geneva.runners.ray.actor_pool import ActorPoolTaskError, PollTimeoutError
from geneva.runners.ray.pipeline import (
    ColumnAddPipelineJob,
    ScheduledReadTask,
    _ClusterStatusRefresher,
    _ClusterStatusSnapshot,
)
from geneva.table import TableReference

if TYPE_CHECKING:
    from collections.abc import Callable

_LOG = logging.getLogger(__name__)


def _wait_until(
    predicate: Callable[[], bool], timeout: float = 5.0, interval: float = 0.01
) -> bool:
    """Poll ``predicate`` until true or ``timeout`` elapses."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(interval)
    return predicate()


# ============================================================================
# _ClusterStatusRefresher unit tests
# ============================================================================


def test_refresher_publishes_snapshot_and_bounds_staleness() -> None:
    """The daemon publishes fresh, timestamped snapshots on its cadence."""
    calls = 0

    def fetch() -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return {"cnt_ray_nodes": calls}

    refresher = _ClusterStatusRefresher(fetch, lambda s: None, interval=0.02)
    assert refresher.latest() is None

    refresher.start()
    try:
        assert _wait_until(lambda: refresher.latest() is not None)
        first = refresher.latest()
        assert first is not None
        assert first.status is not None
        assert "cnt_ray_nodes" in first.status
        assert first.age_seconds(now=first.captured_at) == pytest.approx(0.0)
        assert first.age_seconds(now=first.captured_at + 2.0) == pytest.approx(2.0)

        assert _wait_until(
            lambda: (
                (s := refresher.latest()) is not None
                and s.captured_at > first.captured_at
            )
        )
    finally:
        refresher.stop()


def test_refresher_latest_does_not_block_on_slow_fetch() -> None:
    """Reading the snapshot never blocks on an in-flight listing."""
    fetch_started = threading.Event()

    def slow_fetch() -> dict[str, Any]:
        fetch_started.set()
        time.sleep(1.0)
        return {"cnt_ray_nodes": 1}

    refresher = _ClusterStatusRefresher(slow_fetch, lambda s: None, interval=0.02)
    refresher.start()
    try:
        assert fetch_started.wait(timeout=2.0)
        for _ in range(50):
            t0 = time.monotonic()
            refresher.latest()
            assert time.monotonic() - t0 < 0.1
    finally:
        refresher.stop()


def test_refresher_keeps_last_snapshot_and_survives_failures(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A failing fetch keeps the last good snapshot, logs debug, never crashes."""
    state = {"n": 0}

    def flaky_fetch() -> dict[str, Any]:
        state["n"] += 1
        if state["n"] == 1:
            return {"cnt_ray_nodes": 42}
        raise RuntimeError("k8s api down")

    refresher = _ClusterStatusRefresher(flaky_fetch, lambda s: None, interval=0.02)
    with caplog.at_level(logging.DEBUG, logger=ray_pipeline._LOG.name):
        refresher.start()
        try:
            assert _wait_until(lambda: refresher.latest() is not None)
            good = refresher.latest()
            assert good is not None
            assert good.status == {"cnt_ray_nodes": 42}
            assert _wait_until(lambda: state["n"] >= 4)
            assert refresher._caller.is_alive()
            assert refresher.latest() is good
        finally:
            refresher.stop()

    assert any("cluster status refresh failed" in rec.message for rec in caplog.records)


def test_refresher_retains_snapshot_when_fetch_returns_none() -> None:
    """A None fetch (degraded listing) keeps the last snapshot; its age grows."""
    state = {"n": 0}

    def fetch() -> dict[str, Any] | None:
        state["n"] += 1
        return {"cnt_ray_nodes": 7} if state["n"] == 1 else None

    refresher = _ClusterStatusRefresher(fetch, lambda s: None, interval=0.02)
    refresher.start()
    try:
        assert _wait_until(lambda: refresher.latest() is not None)
        good = refresher.latest()
        assert good is not None
        assert _wait_until(lambda: state["n"] >= 4)
        assert refresher.latest() is good
    finally:
        refresher.stop()


def test_stop_discards_in_flight_fetch_result() -> None:
    """A fetch that outlives stop() is discarded: no apply, no snapshot."""
    fetch_started = threading.Event()
    release_fetch = threading.Event()
    applied: list[dict[str, Any]] = []

    def blocked_fetch() -> dict[str, Any]:
        fetch_started.set()
        release_fetch.wait(timeout=30.0)
        return {"cnt_ray_nodes": 1}

    refresher = _ClusterStatusRefresher(blocked_fetch, applied.append, interval=0.01)
    refresher.start()
    assert fetch_started.wait(timeout=2.0)

    refresher.stop(timeout=0.05)
    assert refresher._caller.is_alive()

    release_fetch.set()
    refresher._caller.join(timeout=2.0)
    assert not refresher._caller.is_alive()
    assert applied == []
    assert refresher.latest() is None


def test_refresher_applies_status_before_publishing() -> None:
    """Each published snapshot was first applied with the same status."""
    applied: list[dict[str, Any]] = []

    def fetch() -> dict[str, Any]:
        return {"cnt_ray_nodes": 3}

    refresher = _ClusterStatusRefresher(fetch, applied.append, interval=0.02)
    refresher.start()
    try:
        assert _wait_until(lambda: refresher.latest() is not None)
        snap = refresher.latest()
        assert snap is not None
        assert applied
        assert applied[0] == snap.status
    finally:
        refresher.stop()


def test_refresher_stop_joins_thread_and_is_idempotent() -> None:
    """Stop tears the thread down cleanly; a second stop is a no-op."""
    calls = 0

    def fetch() -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return {}

    refresher = _ClusterStatusRefresher(fetch, lambda s: None, interval=0.01)
    refresher.start()
    assert _wait_until(lambda: calls > 0)

    refresher.stop()
    assert not refresher._caller.is_alive()
    settled = calls
    time.sleep(0.1)
    assert calls == settled  # no ticks after stop

    refresher.stop()  # idempotent


def test_snapshot_age_uses_supplied_clock() -> None:
    """age_seconds is monotonic-clock based and accepts an injected ``now``."""
    snap = _ClusterStatusSnapshot(captured_at=100.0, status={"x": 1})
    assert snap.age_seconds(now=103.5) == pytest.approx(3.5)


# ============================================================================
# Driver-loop integration: no synchronous listing on the hot path
# ============================================================================


@udf(data_type=pa.int32(), version=uuid.uuid4().hex)
def _passthrough_udf(a: int) -> int:
    return a


def _make_job(job_id: str) -> ColumnAddPipelineJob:
    tbl_ref = TableReference(table_id=["tbl"], version=None, db_uri="db://example")
    return ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": _passthrough_udf}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(()),
        job_id=job_id,
    )


class _FakeDataset:
    uri = "memory://dataset"
    version = 1


def _result_tuple(task: object) -> tuple:
    """A drain result matching pool.drain_ready's 13-tuple element contract."""
    return (task, [], None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


def _install_run_fakes(
    monkeypatch: pytest.MonkeyPatch, pool: object, fwm_cls: type
) -> None:
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "setup_inputplans",
        lambda self: (iter(()), Counter(), 0),
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "setup_writertracker",
        lambda self, planned_frag_count: (_FakeDataset(), 1),
    )
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_ensure_driver_checkpoint_identity_sidecar",
        lambda self, dataset_uri: None,
    )
    monkeypatch.setattr(ColumnAddPipelineJob, "setup_actorpool", lambda self: pool)
    monkeypatch.setattr(ray_pipeline, "FragmentWriterManager", fwm_cls)
    monkeypatch.setattr(ray_pipeline, "_emit_otel_metrics", lambda *a, **k: None)


def test_refresh_cluster_status_returns_none_on_degraded_listing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A degraded listing (error keys, not an exception) surfaces as None and is
    not pushed to the tracker."""
    job = _make_job("job-degraded-listing")
    published: list[dict[str, Any]] = []
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_publish_cluster_status",
        lambda self, status: published.append(status),
    )

    monkeypatch.setattr(
        ray_pipeline,
        "_ray_status",
        lambda: {
            "cnt_ray_nodes": 0,
            "cnt_geneva_workers_active": 0,
            "cnt_geneva_workers_pending": 0,
            "geneva_workers_error": RuntimeError("state api down"),
        },
    )
    assert job._refresh_cluster_status() is None
    assert published == []

    clean = {
        "cnt_ray_nodes": 3,
        "cnt_geneva_workers_active": 2,
        "cnt_geneva_workers_pending": 1,
    }
    monkeypatch.setattr(ray_pipeline, "_ray_status", lambda: clean)
    assert job._refresh_cluster_status() == clean
    assert published == [clean]


def test_driver_loop_performs_no_synchronous_cluster_listing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The result loop never lists cluster status on its own thread, on either
    the drain or stall branch; only the pre-loop and post-loop refreshes run on
    the driver thread (hence the <= 2 below)."""
    main_thread = threading.current_thread()
    lock = threading.Lock()
    calls_by_thread: Counter[bool] = Counter()

    def fake_ray_status() -> dict[str, Any]:
        with lock:
            calls_by_thread[threading.current_thread() is main_thread] += 1
        return {"cnt_ray_nodes": 1}

    monkeypatch.setattr(ray_pipeline, "_ray_status", fake_ray_status)
    # Fire the background refresher aggressively so a surviving inline call
    # would be glaring.
    monkeypatch.setattr(ray_pipeline, "REFRESH_EVERY_SECONDS", 0.005)

    n_results = 40
    n_timeouts = 3

    class _FakePool:
        _num_actors = 0

        def __init__(self) -> None:
            self.remaining = n_results
            self.timeouts = n_timeouts

        def submission_capacity(self) -> int:
            return 0

        def submit(self, _fn: object, _value: object) -> None:
            return None

        def has_next(self) -> bool:
            return self.timeouts > 0 or self.remaining > 0

        def drain_ready(self, timeout: float) -> list:
            time.sleep(0.002)  # let the loop span real wall-time
            if self.timeouts > 0:
                self.timeouts -= 1
                raise PollTimeoutError
            self.remaining -= 1
            return [_result_tuple(object())]

        def broadcast(self, _method: str) -> None:
            return None

        def shutdown(self) -> None:
            return None

    ingested = {"n": 0}

    class _FakeFwm:
        _reconciled_written_fragments_total = 0
        _reconciled_rows_committed_total = 0

        def __init__(self, *args: object, **kwargs: object) -> None:
            return None

        def ingest_task(self, task: object, checkpoints: object) -> None:
            ingested["n"] += 1

        def poll_all(self) -> None:
            return None

        def cleanup(self) -> None:
            return None

        def finalize_metrics(self) -> None:
            return None

        def commit_backfill_completion_marker(
            self, job_id: str, output_column: str
        ) -> None:
            return None

    _install_run_fakes(monkeypatch, _FakePool(), _FakeFwm)

    job = _make_job("job-no-sync-listing")
    job.run()

    assert ingested["n"] == n_results
    assert calls_by_thread[True] <= 2, (
        f"driver thread performed {calls_by_thread[True]} synchronous listings; "
        "the drain path must not list cluster status inline"
    )
    assert calls_by_thread[False] >= 1


def test_task_failure_still_fetches_fresh_pod_statuses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OOM-evidence classification fetches pod status fresh at failure time,
    never from the possibly-stale background snapshot."""
    pod_statuses = [
        {
            "name": "ray-worker",
            "phase": "Failed",
            "ready": False,
            "node_type": "worker",
            "node_name": "node-1",
            "waiting_reasons": Counter(),
            "init_waiting_reasons": Counter(),
            "pulling_count": 0,
            "gpu_requested": False,
            "node_is_gpu": False,
            "oom_evidence": Counter({"state.reason=OOMKilled": 1}),
        }
    ]
    fresh_fetch_calls = 0
    background_calls = 0

    def fresh_pod_statuses(self: ColumnAddPipelineJob) -> list:
        nonlocal fresh_fetch_calls
        fresh_fetch_calls += 1
        return pod_statuses

    def fake_ray_status() -> dict[str, Any]:
        nonlocal background_calls
        background_calls += 1
        return {}

    seen_submission_capacities: list[int] = []

    def reject_failure(*args: object, **kwargs: object) -> bool:
        capacity = kwargs["submission_capacity"]
        assert isinstance(capacity, int)
        seen_submission_capacities.append(capacity)
        return False

    monkeypatch.setattr(
        ColumnAddPipelineJob, "_get_k8s_pod_statuses", fresh_pod_statuses
    )
    monkeypatch.setattr(ray_pipeline, "_ray_status", fake_ray_status)
    monkeypatch.setattr(
        ColumnAddPipelineJob,
        "_handle_fatal_task_failure",
        reject_failure,  # force the fatal re-raise deterministically
    )

    actor_exc = ray.exceptions.ActorUnavailableError("actor unavailable", None)

    class _FailingPool:
        _num_actors = 0

        def submission_capacity(self) -> int:
            return 1

        def submit(self, _fn: object, _value: object) -> None:
            return None

        def has_next(self) -> bool:
            return True

        def drain_ready(self, timeout: float) -> NoReturn:
            raise ActorPoolTaskError(ScheduledReadTask(object()), actor_exc)

        def shutdown(self) -> None:
            return None

    class _FakeFwm:
        def __init__(self, *args: object, **kwargs: object) -> None:
            return None

    _install_run_fakes(monkeypatch, _FailingPool(), _FakeFwm)

    job = _make_job("job-fresh-on-failure")
    with pytest.raises(FatalWorkerOOMError):
        job.run()

    assert fresh_fetch_calls >= 1
    assert seen_submission_capacities == [1]


def test_result_loop_body_has_no_synchronous_refresh_call() -> None:
    """Regression guard: the loop body contains no cluster-status refresh call."""
    src = inspect.getsource(ColumnAddPipelineJob.run)
    start = src.index("while pool.has_next()")
    # Anchor on the teardown call (unique, cannot appear mid-loop) rather than
    # the first ``finally:``, which an inner try/finally could shadow.
    end = src.index("refresher.stop()", start)
    loop_body = src[start:end]

    assert "_refresh_cluster_status(" not in loop_body
    assert "_try_refresh_cluster_status" not in loop_body
    # Catch a direct state-API listing regardless of any helper rename.
    assert "_ray_status(" not in loop_body
    assert not hasattr(ColumnAddPipelineJob, "_try_refresh_cluster_status")
