# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Submitter finalization survives tracker loss without trusting another attempt."""

from __future__ import annotations

import threading
import time
from concurrent.futures import Future
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest
import ray.exceptions

import geneva
from geneva.runners.ray import pipeline, raycluster
from geneva.runners.ray.jobstate import RayJobState
from geneva.runners.ray.raycluster import RayCluster

if TYPE_CHECKING:
    from pathlib import Path

    from geneva.jobs.jobs import JobRecord


@pytest.fixture
def ray_api(monkeypatch: pytest.MonkeyPatch) -> Mock:
    # Keep the fake connection local to its consumers. Patching the real
    # ray.is_initialized also fools Ray's logging filter into accessing a
    # nonexistent core_worker after an earlier test has shut Ray down.
    api = Mock(exceptions=ray.exceptions)
    api.is_initialized.return_value = True
    monkeypatch.setattr(pipeline, "ray", api)
    monkeypatch.setattr(raycluster, "ray", api)
    return api


@pytest.fixture
def cluster(monkeypatch: pytest.MonkeyPatch) -> RayCluster:
    # These finalization tests do not use Kubernetes clients.
    monkeypatch.setattr(RayCluster, "__attrs_post_init__", lambda self: None)
    return RayCluster(name="test-cluster", namespace="test")


@pytest.fixture
def attempt(tmp_path: Path) -> RayJobState:
    # Exercise non-default system namespaces through the real TableReference
    # connection path, rather than assuming a directory for the history table.
    db = geneva.connect(str(tmp_path), system_namespace=["tenant", "system"])
    table = db.create_table("t", [{"a": 1}])
    job_id = db._history.launch("t", "a").job_id
    db._history.set_running(job_id)
    db._history.set_object_ref(job_id, b"driver")
    state = RayJobState(db._history, job_id, table.get_reference())
    state.object_ref = b"driver"
    return state


def test_saved_record_reopens_fresh_history_in_system_namespace(
    attempt: RayJobState, tmp_path: Path
) -> None:
    assert attempt.saved_record().status == "RUNNING"
    other = geneva.connect(str(tmp_path), system_namespace=["tenant", "system"])
    other._history.update_metrics(
        attempt.job_id,
        {"rows_committed": {"n": 3, "total": 3, "done": True, "desc": "rows"}},
    )
    other._history.set_completed(attempt.job_id)
    saved = attempt.saved_record(refresh=True)
    assert saved.status == "DONE"
    assert saved.metrics[0].n == 3


@pytest.mark.parametrize("replacement_ref", [None, b"replacement"])
def test_saved_record_rejects_replacement_attempt(
    attempt: RayJobState, replacement_ref: bytes | None
) -> None:
    hist = attempt.history
    hist.launch("t", "a", job_id=attempt.job_id, reset_object_ref=True)
    if replacement_ref is not None:
        hist.set_object_ref(attempt.job_id, replacement_ref)
    hist.set_completed(attempt.job_id)
    assert attempt.saved_record(refresh=True) is None


def test_slow_saved_lookup_is_bounded_and_single_flight() -> None:
    release = threading.Event()
    entered = threading.Event()
    table_ref = Mock()

    def blocked_open() -> Mock:
        entered.set()
        assert release.wait(5)
        return Mock()

    table_ref.open_db.side_effect = blocked_open
    state = RayJobState(Mock(), "job", table_ref)
    state.object_ref = b"ref"
    start = time.monotonic()
    try:
        assert state.saved_record(timeout=0.01) is None
        assert entered.wait(1)
        assert state.saved_record(timeout=0.01, refresh=True) is None
        assert time.monotonic() - start < 1
        assert table_ref.open_db.call_count == 1
    finally:
        release.set()


def test_saved_metrics_remain_available_during_slow_refresh(
    attempt: RayJobState,
) -> None:
    saved = attempt.saved_record()
    assert saved.status == "RUNNING"
    release = threading.Event()
    table_ref = Mock()
    db = Mock()
    db._history.get.return_value = [saved]

    def slow_open() -> Mock:
        assert release.wait(5)
        return db

    table_ref.open_db.side_effect = slow_open
    attempt.table_ref = table_ref
    attempt._saved_at -= 2  # Expire the display cache.
    try:
        assert attempt.saved_record(timeout=0.01).status == "RUNNING"
    finally:
        release.set()


def test_cluster_discards_progress_read_started_before_finalization(
    attempt: RayJobState,
    cluster: RayCluster,
    ray_api: Mock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured, release, old_read_finished = (threading.Event() for _ in range(3))
    original_get = attempt.history.get

    def read(job_id: str) -> list[JobRecord]:
        rows = original_get(job_id)
        if not captured.is_set():
            assert rows[0].status == "RUNNING"
            captured.set()
            assert release.wait(5)
            old_read_finished.set()
        else:
            # The fresh read must not overlap the older progress lookup.
            assert old_read_finished.is_set()
        return rows

    db = Mock()
    db._history.get.side_effect = read
    attempt.table_ref = Mock()
    attempt.table_ref.open_db.return_value = db
    assert attempt.saved_record(timeout=0.01) is None
    assert captured.wait(1)
    attempt.history.set_completed(attempt.job_id)

    ref = object()
    cluster.register_tracked_job(attempt.job_id, ref, Mock(), job_state=attempt)
    ray_api.wait.return_value = ([ref], [])
    ray_api.get.return_value = None
    monkeypatch.setattr(
        cluster, "_poll_tracker_done", Mock(side_effect=ray.exceptions.ActorDiedError())
    )
    # Let finalization encounter the pending RUNNING read before it completes.
    timer = threading.Timer(0.1, release.set)
    timer.start()
    try:
        assert cluster._wait_for_tracked_jobs(poll_interval=0) is False
        assert db._history.get.call_count == 2
        assert original_get(attempt.job_id)[0].status == "DONE"
    finally:
        release.set()
        timer.join()


@pytest.mark.parametrize(
    "error",
    [ray.exceptions.ActorDiedError(), ray.exceptions.OutOfMemoryError("tracker OOM")],
)
def test_lost_tracker_uses_saved_metrics_without_warning_spam(
    attempt: RayJobState,
    ray_api: Mock,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    error: Exception,
) -> None:
    attempt.history.update_metrics(
        attempt.job_id,
        {"rows_committed": {"n": 3, "total": 3, "done": True, "desc": "rows"}},
    )
    ray_api.get.side_effect = error
    sync = Mock()
    monkeypatch.setattr(pipeline.RayJobFuture, "_sync_bars", sync)
    future = pipeline.RayJobFuture(
        job_id=attempt.job_id,
        ray_obj_ref=object(),
        job_tracker=Mock(),
        job_state=attempt,
    )
    future.status(timeout=1)
    future.status(timeout=1)
    assert ray_api.get.call_count == (
        1 if isinstance(error, ray.exceptions.ActorDiedError) else 2
    )
    assert sync.call_args.args[0]["rows_committed"]["n"] == 3
    assert caplog.text.count("using saved metrics") == 1


@pytest.mark.parametrize("saved_status", ["DONE", "FAILED", "RUNNING", "replacement"])
@pytest.mark.parametrize("probe_hangs", [False, True])
def test_cluster_confirms_saved_attempt_after_tracker_loss(
    attempt: RayJobState,
    cluster: RayCluster,
    ray_api: Mock,
    monkeypatch: pytest.MonkeyPatch,
    saved_status: str,
    probe_hangs: bool,
) -> None:
    hist = attempt.history
    if saved_status == "replacement":
        hist.set_object_ref(attempt.job_id, b"other-attempt")
        hist.set_completed(attempt.job_id)
    elif saved_status != "RUNNING":
        hist.set_completed(attempt.job_id, saved_status)
    ref = object()
    cluster.register_tracked_job(attempt.job_id, ref, Mock(), job_state=attempt)
    ray_api.wait.return_value = ([ref], [])
    ray_api.get.return_value = None
    probe = (
        Mock(return_value=(None, object()))
        if probe_hangs
        else Mock(side_effect=ray.exceptions.ActorDiedError())
    )
    monkeypatch.setattr(cluster, "_poll_tracker_done", probe)
    assert cluster._wait_for_tracked_jobs(poll_interval=0) is (saved_status != "DONE")
    assert probe.call_count == (6 if probe_hangs else 1)
    # Fallback must never rewrite the durable status, including DONE.
    assert hist.get(attempt.job_id)[0].status == (
        "DONE" if saved_status == "replacement" else saved_status
    )


@pytest.mark.parametrize("wait_path", ["result", "cluster_exit"])
@pytest.mark.parametrize("callback_started", [False, True])
def test_normal_waits_finish_pending_failure_write(
    attempt: RayJobState,
    cluster: RayCluster,
    ray_api: Mock,
    monkeypatch: pytest.MonkeyPatch,
    wait_path: str,
    callback_started: bool,
) -> None:
    release, entered = threading.Event(), threading.Event()
    original = attempt.history.set_failed

    def delayed_write(*args, **kwargs) -> None:
        entered.set()
        assert release.wait(5)
        original(*args, **kwargs)

    write = Mock(side_effect=delayed_write)
    monkeypatch.setattr(attempt.history, "set_failed", write)
    error = ray.exceptions.WorkerCrashedError()
    if callback_started:
        attempt.record_failure(error)
        assert entered.wait(1)
    ray_api.get.side_effect = error
    ref = object()
    # Release storage while the normal caller is waiting, without polling the
    # saved status after result/exit to hide a premature return.
    timer = threading.Timer(0.1, release.set)
    timer.start()
    try:
        if wait_path == "result":
            future = pipeline.RayJobFuture(
                job_id=attempt.job_id, ray_obj_ref=ref, job_state=attempt
            )
            with pytest.raises(ray.exceptions.WorkerCrashedError):
                future.result()
        else:
            cluster.register_tracked_job(attempt.job_id, ref, job_state=attempt)
            ray_api.wait.return_value = ([ref], [])
            assert cluster._wait_for_tracked_jobs() is True
        assert attempt.history.get(attempt.job_id)[0].status == "FAILED"
        assert write.call_count == 1
    finally:
        release.set()
        timer.join()


def test_failure_write_wait_is_bounded(
    attempt: RayJobState, monkeypatch: pytest.MonkeyPatch
) -> None:
    release = threading.Event()
    monkeypatch.setattr(attempt.history, "set_failed", lambda *a, **kw: release.wait(5))
    start = time.monotonic()
    try:
        attempt.finish_failure(ray.exceptions.WorkerCrashedError(), timeout=0.01)
        assert time.monotonic() - start < 1
    finally:
        release.set()


def test_failed_jobs_share_cluster_failure_write_wait_budget(
    cluster: RayCluster, ray_api: Mock
) -> None:
    release = threading.Event()
    states = []
    refs = [object() for _ in range(3)]
    error = ray.exceptions.WorkerCrashedError()
    for i, ref in enumerate(refs):
        history = Mock()
        history.set_failed.side_effect = lambda *a, **kw: release.wait(5)
        state = RayJobState(history, f"job-{i}")
        state.object_ref = b"driver"
        state.record_failure(error)
        cluster.register_tracked_job(state.job_id, ref, job_state=state)
        states.append(state)
    cluster.wait_timeout = 0.05
    ray_api.wait.return_value = (refs, [])
    ray_api.get.side_effect = error
    finished: Future[bool] = Future()

    def finalize() -> None:
        try:
            finished.set_result(cluster._wait_for_tracked_jobs())
        except BaseException as exc:
            finished.set_exception(exc)

    worker = threading.Thread(target=finalize, daemon=True)
    worker.start()
    try:
        # Storage stays blocked until after shutdown returns. Give the caller
        # scheduling slack, but never wait for the default five seconds per job.
        assert finished.result(timeout=0.5) is True
        assert all(state._failure_started for state in states)
        assert all(not state._failure_done.is_set() for state in states)
    finally:
        release.set()
        worker.join(timeout=1)
        for state in states:
            assert state._failure_done.wait(1)
