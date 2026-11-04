# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Driver-side guarantees for a job's final record (GEN-979).

* the JobTracker's throttled metrics are persisted before the final status
  write, on success and on failure,
* a failed pipeline still hands its buffered progress deltas to the tracker,
* a job cancelled while its driver runs stays CANCELLED.
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import TYPE_CHECKING, Any

import lance
import pyarrow as pa
import pytest
import ray.exceptions

import geneva
import geneva.runners.ray.pipeline as ray_pipeline
from geneva import fail_fast
from geneva.apply.task import BackfillUDFTask
from geneva.checkpoint import CheckpointStore
from geneva.jobs import JobStateManager, JobStatus
from geneva.jobs.config import JobConfig
from geneva.runners.ray import sparse_pipeline
from geneva.runners.ray.pipeline import (
    FINAL_STATUS_TIMEOUT_S,
    ColumnAddPipelineJob,
    _flush_job_tracker,
    run_ray_add_column_remote,
)
from geneva.runners.sparse_update import SparseUpdateResult
from geneva.table import TableReference

if TYPE_CHECKING:
    from pathlib import Path


@geneva.udf(data_type=pa.int64())
def _plus_one(a: int) -> int:
    return a + 1


class _RemoteMethod:
    def __init__(self, calls: list[str], name: str) -> None:
        self._calls = calls
        self._name = name

    def remote(self, *args: object) -> str:
        self._calls.append(self._name)
        return self._name


class _FakeTracker:
    """JobTracker handle that records the calls the driver makes."""

    def __init__(self, calls: list[str]) -> None:
        self.flush = _RemoteMethod(calls, "tracker.flush")
        self.mark_job_done = _RemoteMethod(calls, "tracker.mark_job_done")


def _record_status_writes(monkeypatch: pytest.MonkeyPatch, calls: list[str]) -> None:
    for name in ("set_running", "set_completed", "set_failed"):
        original = getattr(JobStateManager, name)

        def record(
            self: JobStateManager,
            *args: Any,
            _original: Any = original,
            _name: str = name,
            **kwargs: Any,
        ) -> None:
            calls.append(f"hist.{_name}")
            _original(self, *args, **kwargs)

        monkeypatch.setattr(JobStateManager, name, record)


def _sparse_result() -> SparseUpdateResult:
    return SparseUpdateResult(
        base_version=1,
        committed_version=2,
        rows_total=2,
        rows_matched=1,
        rows_written=1,
        fragments_total=1,
        fragments_touched=1,
        fragment_equiv_rows=2,
    )


@pytest.fixture
def driver_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """A real table and job record, a fake tracker, and recorded call order."""
    db = geneva.connect(str(tmp_path))
    tbl = db.create_table("t", pa.table({"a": pa.array([1, 2], type=pa.int64())}))
    tbl.add_columns({"b": _plus_one})
    job_id = db._history.launch("t", "b").job_id
    calls: list[str] = []
    monkeypatch.setattr(ray_pipeline.ray, "get", lambda ref, timeout=None: True)
    _record_status_writes(monkeypatch, calls)
    return {
        "db_uri": str(tmp_path),
        "table": tbl,
        "job_id": job_id,
        "tracker": _FakeTracker(calls),
        "calls": calls,
    }


def _run_sparse_driver(env: dict[str, Any]) -> object:
    return run_ray_add_column_remote._function(
        env["table"].get_reference(),
        "b",
        job_id=env["job_id"],
        job_tracker=env["tracker"],
        update_mode="sparse_rows",
        where="a > 1",
    )


def _job(env: dict[str, Any]) -> Any:
    return geneva.connect(env["db_uri"])._history.get(env["job_id"])[0]


def test_driver_persists_metrics_before_marking_done(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        sparse_pipeline, "run_ray_sparse_update", lambda *a, **k: _sparse_result()
    )

    _run_sparse_driver(driver_env)

    assert driver_env["calls"] == [
        "hist.set_running",
        "tracker.flush",
        "hist.set_completed",
        "tracker.mark_job_done",
    ]
    job = _job(driver_env)
    assert job.status == JobStatus.DONE.value
    assert job.completed_at is not None


def test_driver_persists_metrics_before_marking_failed(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*args: object, **kwargs: object) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(sparse_pipeline, "run_ray_sparse_update", fail)

    with pytest.raises(RuntimeError, match="boom"):
        _run_sparse_driver(driver_env)

    assert driver_env["calls"] == [
        "hist.set_running",
        "tracker.flush",
        "hist.set_failed",
        "tracker.mark_job_done",
    ]
    job = _job(driver_env)
    assert job.status == JobStatus.FAILED.value
    assert job.completed_at is not None
    assert job.events == ["Job failed: RuntimeError: boom"]


def test_failed_metrics_flush_does_not_block_failed_status(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*args: object, **kwargs: object) -> None:
        raise RuntimeError("boom")

    def tracker_timeout(ref: object, timeout: float | None = None) -> None:
        raise ray.exceptions.GetTimeoutError("tracker save timed out")

    monkeypatch.setattr(sparse_pipeline, "run_ray_sparse_update", fail)
    monkeypatch.setattr(ray_pipeline.ray, "get", tracker_timeout)

    with pytest.raises(RuntimeError, match="boom"):
        _run_sparse_driver(driver_env)

    job = _job(driver_env)
    assert job.status == JobStatus.FAILED.value
    assert job.completed_at is not None


def test_job_cancelled_while_driver_runs_stays_cancelled(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    def cancel_then_finish(*args: object, **kwargs: object) -> SparseUpdateResult:
        # The cancel comes from another client while the driver is working.
        geneva.connect(driver_env["db_uri"])._history.set_cancelled(
            driver_env["job_id"]
        )
        return _sparse_result()

    monkeypatch.setattr(sparse_pipeline, "run_ray_sparse_update", cancel_then_finish)

    _run_sparse_driver(driver_env)

    job = _job(driver_env)
    assert job.status == JobStatus.CANCELLED.value
    assert job.events == [
        "Job cancelled",
        "Job completed with status DONE (job already CANCELLED; status unchanged)",
    ]
    # completed_at is the cancel request; updated_at is when the driver finished.
    assert job.completed_at < job.updated_at


def test_flush_job_tracker_waits_with_a_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []
    waits: list[tuple[object, float | None]] = []

    def record_get(ref: object, timeout: float | None = None) -> bool:
        waits.append((ref, timeout))
        return True

    monkeypatch.setattr(ray_pipeline.ray, "get", record_get)

    _flush_job_tracker(_FakeTracker(calls))

    assert calls == ["tracker.flush"]
    assert waits == [("tracker.flush", FINAL_STATUS_TIMEOUT_S)]


def test_flush_job_tracker_swallows_errors(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    def actor_died(ref: object, timeout: float | None = None) -> None:
        raise ray.exceptions.RayActorError()

    monkeypatch.setattr(ray_pipeline.ray, "get", actor_died)

    with caplog.at_level(logging.WARNING):
        _flush_job_tracker(_FakeTracker([]))

    assert "Failed to persist final job metrics" in caplog.text


def test_flush_job_tracker_without_tracker_is_a_noop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unexpected(*args: object, **kwargs: object) -> None:
        raise AssertionError("ray.get should not be called")

    monkeypatch.setattr(ray_pipeline.ray, "get", unexpected)

    _flush_job_tracker(None)


class _RecordingBuffer:
    def __init__(self, error: Exception | None = None) -> None:
        self.flushes: list[bool] = []
        self._error = error

    def flush(self, *, force: bool = False) -> None:
        self.flushes.append(force)
        if self._error is not None:
            raise self._error


def _pipeline_job() -> ColumnAddPipelineJob:
    return ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": _plus_one}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=TableReference(table_id=["t"], version=None, db_uri="db://example"),
        input_plan=iter(()),
        job_id="job-1",
    )


def test_failed_pipeline_flushes_buffered_metrics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    job = _pipeline_job()
    buffer = _RecordingBuffer()
    job._metric_buffer = buffer  # type: ignore[assignment]

    def fail(self: ColumnAddPipelineJob) -> None:
        raise RuntimeError("fragment write failed")

    monkeypatch.setattr(ColumnAddPipelineJob, "_run", fail)

    with pytest.raises(RuntimeError, match="fragment write failed"):
        job.run()

    assert buffer.flushes == [True]


def test_failing_metrics_flush_keeps_the_pipeline_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    job = _pipeline_job()
    buffer = _RecordingBuffer(error=RuntimeError("tracker unreachable"))
    job._metric_buffer = buffer  # type: ignore[assignment]

    def fail(self: ColumnAddPipelineJob) -> None:
        raise ValueError("planning failed")

    monkeypatch.setattr(ColumnAddPipelineJob, "_run", fail)

    with pytest.raises(ValueError, match="planning failed"):
        job.run()

    assert buffer.flushes == [True]


def test_successful_pipeline_adds_no_extra_flush(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    job = _pipeline_job()
    buffer = _RecordingBuffer()
    job._metric_buffer = buffer  # type: ignore[assignment]
    monkeypatch.setattr(ColumnAddPipelineJob, "_run", lambda self: None)

    job.run()

    assert buffer.flushes == []


@pytest.mark.ray
def test_failed_backfill_records_end_time_and_final_metrics(
    tmp_path: Path, local_ray_context: None
) -> None:
    failing_row = 95
    lance.write_dataset(
        pa.table({"a": pa.array(range(100), type=pa.int64())}),
        tmp_path / "test.lance",
        max_rows_per_file=10,
    )
    db = geneva.connect(str(tmp_path))

    @geneva.udf(data_type=pa.int64(), on_error=fail_fast(), version=uuid.uuid4().hex)
    def fail_late(a: int) -> int:
        if a == failing_row:
            # Give the other applier time to finish tasks before the job fails.
            time.sleep(3)
            raise ValueError("bad row")
        return a

    tbl = db.open_table("test")
    tbl.add_columns({"b": fail_late})
    job_id = uuid.uuid4().hex
    with pytest.raises(Exception, match="bad row"):
        tbl.backfill(
            "b",
            job_id=job_id,
            concurrency=2,
            # Only the final flush can persist progress made during the run.
            job_tracker_min_update_interval_secs=3600,
        )

    job = db.get_job(job_id)
    assert job.status == JobStatus.FAILED.value
    assert job.completed_at is not None
    assert job.completed_at >= job.launched_at
    metrics = {m.name: m for m in job.metrics or []}
    assert metrics["tasks_completed"].n > 0
