# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Control-plane loss must terminate a job instead of resetting its budgets."""

from __future__ import annotations

import os
import threading
import time
from concurrent.futures import Future
from functools import partial
from types import SimpleNamespace
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pyarrow as pa
import pytest
import ray

import geneva
from geneva.jobs import JobStatus
from geneva.runners.ray import pipeline
from geneva.runners.ray.jobtracker import job_tracker_options

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


@pytest.mark.parametrize(
    "error",
    [
        ray.exceptions.OutOfMemoryError("driver killed by memory monitor"),
        ray.exceptions.WorkerCrashedError(),
        ray.exceptions.NodeDiedError("driver node lost"),
    ],
)
def test_driver_loss_persists_failed_without_waiting_on_job(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, error: Exception
) -> None:
    db = geneva.connect(str(tmp_path))
    hist = db._history
    job = hist.launch("t", "b")
    hist.set_running(job.job_id)
    saved = threading.Event()
    original = hist.set_failed

    def record_failure(job_id: str, message: str, **kwargs) -> None:
        original(job_id, message, **kwargs)
        saved.set()

    monkeypatch.setattr(hist, "set_failed", record_failure)
    monkeypatch.setattr(pipeline.cloudpickle, "dumps", lambda ref: b"ref")
    result: Future = Future()
    ref = SimpleNamespace(future=lambda: result)
    assert pipeline._submit_ray_job(hist, job.job_id, lambda: ref) is ref

    # No caller polls done() or result(); the submitting process observes the
    # OOM independently of the dead driver's Python exception handler.
    result.set_exception(error)
    assert saved.wait(5)
    stored = hist.get(job.job_id)[0]
    assert stored.status == JobStatus.FAILED.value
    assert stored.completed_at is not None
    assert type(error).__name__ in stored.events[-1]


@pytest.mark.parametrize(
    "error", [None, ray.exceptions.RayTaskError("driver", "trace", ValueError("bad"))]
)
def test_driver_observer_leaves_normal_finalization_to_driver(
    monkeypatch: pytest.MonkeyPatch, error: Exception | None
) -> None:
    hist = Mock()
    result: Future = Future()
    ref = SimpleNamespace(future=lambda: result)
    monkeypatch.setattr(pipeline.cloudpickle, "dumps", lambda ref: b"ref")
    pipeline._submit_ray_job(hist, "job", lambda: ref)
    if error is None:
        result.set_result(None)
    else:
        result.set_exception(error)
    hist.set_failed.assert_not_called()


def test_driver_loss_does_not_overwrite_cancellation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = geneva.connect(str(tmp_path))
    hist = db._history
    job = hist.launch("t", "b")
    hist.set_cancelled(job.job_id)
    saved = threading.Event()
    original = hist.set_failed

    def record_failure(job_id: str, message: str, **kwargs) -> None:
        original(job_id, message, **kwargs)
        saved.set()

    monkeypatch.setattr(hist, "set_failed", record_failure)
    monkeypatch.setattr(pipeline.cloudpickle, "dumps", lambda ref: b"ref")
    result: Future = Future()
    pipeline._submit_ray_job(
        hist, job.job_id, lambda: SimpleNamespace(future=lambda: result)
    )
    result.set_exception(ray.exceptions.OutOfMemoryError("driver OOM"))
    assert saved.wait(5)
    assert hist.get(job.job_id)[0].status == JobStatus.CANCELLED.value


@pytest.mark.parametrize("kind", ["add_column", "refresh", "bulk_load"])
def test_dispatch_inherits_tracker_restart_budget_and_invalidates_old_driver(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    db = geneva.connect(str(tmp_path))
    tbl = db.create_table("t", pa.table({"a": [1]}))
    hist = db._history
    job_id = hist.launch("t", "a").job_id
    hist.set_object_ref(job_id, b"previous-driver")
    tracker_factory = Mock()
    monkeypatch.setattr(pipeline, "job_tracker_options", tracker_factory)
    monkeypatch.setattr(pipeline, "head_pin_options", dict)

    def submit(*args, **kwargs) -> object:
        assert hist.get(job_id)[0].object_ref is None
        return object()

    monkeypatch.setattr(pipeline, "_submit_ray_job", submit)
    remote = Mock()
    monkeypatch.setattr(pipeline, f"run_ray_{kind}_remote", remote)
    dispatch = getattr(pipeline, f"dispatch_run_ray_{kind}")
    if kind == "add_column":
        dispatch(tbl.get_reference(), "a", job_id=job_id)
    elif kind == "bulk_load":
        dispatch(tbl.get_reference(), "source.parquet", "a", ["b"], job_id=job_id)
    else:
        dispatch(tbl.get_reference(), job_id=job_id)
    assert "max_restarts" not in tracker_factory.call_args.kwargs


@pytest.fixture(scope="module")
def single_node_ray(request: pytest.FixtureRequest) -> Iterator[None]:
    ray.shutdown()
    ray.init(
        num_cpus=2,
        object_store_memory=80 * 1024**2,
        include_dashboard=False,
        _system_config=getattr(request, "param", {}),
    )
    yield
    ray.shutdown()


@pytest.mark.ray
def test_refresh_dispatch_records_worker_loss(
    single_node_ray: None, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class CrashingTableRef:
        table_name = "t"
        table_uri = "unused"

        def open_db(self) -> geneva.Connection:
            return geneva.connect(str(tmp_path))

        def open(self) -> None:
            self.open_db()._history.set_running("refresh-crash")
            os._exit(1)

    monkeypatch.setattr(pipeline, "head_pin_options", dict)
    job = pipeline.dispatch_run_ray_refresh(
        CrashingTableRef(), job_id="refresh-crash", enable_job_tracker_saves=False
    )
    try:
        with pytest.raises(ray.exceptions.WorkerCrashedError):
            ray.get(job.ray_obj_ref, timeout=30)
        hist = geneva.connect(str(tmp_path))._history
        deadline = time.monotonic() + 5
        while hist.get(job.job_id)[0].status != JobStatus.FAILED.value:
            assert time.monotonic() < deadline, "refresh driver loss was not persisted"
            time.sleep(0.05)
    finally:
        ray.kill(job.job_tracker)


@pytest.mark.parametrize("save_replacement_ref", [False, True])
def test_old_driver_failure_does_not_fail_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, save_replacement_ref: bool
) -> None:
    hist = geneva.connect(str(tmp_path))._history
    job_id = hist.launch("t", "b").job_id
    hist.set_running(job_id)
    entered, release, saved = (threading.Event() for _ in range(3))
    original = hist.set_failed

    def delayed_failure(*args, **kwargs) -> None:
        entered.set()
        assert release.wait(5)
        original(*args, **kwargs)
        saved.set()

    monkeypatch.setattr(hist, "set_failed", delayed_failure)
    monkeypatch.setattr(pipeline.cloudpickle, "dumps", lambda ref: b"ref")
    result: Future = Future()
    pipeline._submit_ray_job(
        hist, job_id, lambda: SimpleNamespace(future=lambda: result)
    )
    result.set_exception(ray.exceptions.WorkerCrashedError())
    try:
        assert entered.wait(5)
        # Dispatch invalidates the old ref before the replacement starts,
        # even if the replacement's ref has not yet been persisted.
        hist.launch("t", "b", job_id=job_id, reset_object_ref=True)
        hist.set_running(job_id)
        if save_replacement_ref:
            hist.set_object_ref(job_id, b"replacement")
    finally:
        release.set()
    assert saved.wait(5)
    hist.set_completed(job_id)
    assert hist.get(job_id)[0].status == JobStatus.DONE.value


def test_observer_is_not_attached_without_a_persisted_attempt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    hist = geneva.connect(str(tmp_path))._history
    job_id = hist.launch("t", "b").job_id
    hist.set_running(job_id)
    watch = Mock()

    def fail_persist(*args) -> None:
        raise RuntimeError("storage unavailable")

    monkeypatch.setattr(hist, "set_object_ref", fail_persist)
    monkeypatch.setattr(pipeline.cloudpickle, "dumps", lambda ref: b"ref")
    ref = SimpleNamespace(future=watch)
    assert pipeline._submit_ray_job(hist, job_id, lambda: ref) is ref
    watch.assert_not_called()


@pytest.mark.ray
@pytest.mark.parametrize("kind", ["add_column", "refresh", "bulk_load"])
def test_driver_worker_death_is_not_replayed(
    single_node_ray: None, tmp_path: Path, kind: str
) -> None:
    class CrashingTableRef:
        table_name = "t"
        table_uri = "unused"

        def __init__(self, attempts: Path) -> None:
            self.attempts = attempts

        def open(self) -> None:
            with self.attempts.open("a") as log:
                log.write("attempt\n")
            os._exit(1)

    attempts = tmp_path / "attempts"
    table_ref = CrashingTableRef(attempts)
    remote = getattr(pipeline, f"run_ray_{kind}_remote")
    if kind == "add_column":
        ref = remote.remote(table_ref, "b")
    elif kind == "bulk_load":
        ref = remote.remote(table_ref, "source.parquet", "a", ["b"])
    else:
        ref = remote.remote(table_ref)
    with pytest.raises(ray.exceptions.WorkerCrashedError):
        ray.get(ref, timeout=60)
    assert attempts.read_text().splitlines() == ["attempt"]


@pytest.mark.ray
def test_tracker_restarts_exactly_twice(single_node_ray: None) -> None:
    tracker = job_tracker_options().remote("job", None, enable_saves=False)
    pid = ray.get(tracker.__ray_call__.remote(lambda _: os.getpid()), timeout=30)
    for _ in range(2):
        ray.kill(tracker, no_restart=False)
        deadline = time.monotonic() + 30
        while True:
            try:
                new_pid = ray.get(
                    tracker.__ray_call__.remote(lambda _: os.getpid()), timeout=1
                )
                if new_pid != pid:
                    pid = new_pid
                    break
            except (
                ray.exceptions.GetTimeoutError,
                ray.exceptions.ActorUnavailableError,
            ):
                pass
            assert time.monotonic() < deadline, "tracker failed to restart"
            time.sleep(0.05)
        ray.get(tracker.get_all.remote(), timeout=5)
    ray.kill(tracker, no_restart=False)
    deadline = time.monotonic() + 30
    while True:
        try:
            ray.get(tracker.get_all.remote(), timeout=1)
        except ray.exceptions.ActorDiedError:
            break
        except (ray.exceptions.GetTimeoutError, ray.exceptions.ActorUnavailableError):
            pass
        assert time.monotonic() < deadline, "tracker exceeded its restart budget"
        time.sleep(0.05)


@pytest.mark.ray
@pytest.mark.parametrize(
    "single_node_ray",
    [{"memory_usage_threshold": 0.000001, "memory_monitor_refresh_ms": 100}],
    indirect=True,
)
def test_memory_monitor_terminates_driver_and_tracker(
    single_node_ray: None, tmp_path: Path
) -> None:
    # Force Ray's real memory monitor above its threshold without allocating
    # large buffers or relying on a cgroup/kernel OOM. Keep a sibling tracker
    # alive in the owner group: disabling driver retries alone is insufficient.
    class BlockingTableRef:
        table_name = "t"
        table_uri = "unused"

        def open(self) -> None:
            time.sleep(120)

    db = geneva.connect(str(tmp_path))
    hist = db._history
    tracker = job_tracker_options().remote("tracker", None, enable_saves=False)
    for kind in ("add_column", "refresh", "bulk_load"):
        job = hist.launch("t", kind)
        hist.set_running(job.job_id)
        remote = getattr(pipeline, f"run_ray_{kind}_remote")
        args = [BlockingTableRef()]
        if kind == "add_column":
            args.append("b")
        elif kind == "bulk_load":
            args.extend(["source.parquet", "a", ["b"]])
        ref = pipeline._submit_ray_job(
            hist, job.job_id, partial(remote.remote, *args, job_tracker=tracker)
        )
        with pytest.raises(ray.exceptions.OutOfMemoryError):
            ray.get(ref, timeout=30)
        deadline = time.monotonic() + 5
        while hist.get(job.job_id)[0].status != JobStatus.FAILED.value:
            assert time.monotonic() < deadline, "driver loss was not persisted"
            time.sleep(0.05)
    with pytest.raises(
        (ray.exceptions.ActorDiedError, ray.exceptions.OutOfMemoryError)
    ):
        ray.get(tracker.get_all.remote(), timeout=30)
