# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""A job must survive losing commits on the geneva_jobs table (GEN-1012).

Every job's bookkeeping is a commit on one shared ``geneva_jobs`` table. Under
load a write can lose the commit race on every one of Lance's internal retries,
and lancedb then raises the conflict as a ``RuntimeError``. These tests replay
that error, verbatim from a production job record, against a real local jobs
table:

* jobs-table writes retry it, since nothing landed and each write is safe to
  repeat,
* a driver whose ``set_running`` keeps losing still does the job's work,
* a driver whose data committed is not turned into a failure because its
  final status write kept losing,
* a rerun of an ended job does not work under its old status,
* the attempt's submitter saves the final status its driver could not, fenced
  on its own attempt so it never touches a replacement,
* remote polling stops once the driver is gone without a final status.
"""

from __future__ import annotations

import base64
import json
import logging
import math
import os
import tempfile
from concurrent.futures import Future
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

import pyarrow as pa
import pytest
import ray.exceptions

import geneva
import geneva.jobs.remote as remote_module
import geneva.runners.ray.pipeline as ray_pipeline
import geneva.utils as geneva_utils
from geneva.jobs import JobStateManager, JobStatus
from geneva.jobs.heartbeat import DRIVER_EXITED, heartbeat_path
from geneva.jobs.remote import RemoteJob
from geneva.runners.ray import sparse_pipeline
from geneva.runners.ray.jobstate import RayJobState
from geneva.runners.ray.pipeline import (
    run_ray_add_column_remote,
    run_ray_bulk_load_remote,
    run_ray_refresh_remote,
)
from geneva.runners.sparse_update import SparseUpdateResult

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

# As recorded on a 1X job that died at set_running (lancedb 0.37 / lance 10.0.0).
COMMIT_EXHAUSTED = (
    "lance error: Commit conflict for version 715144: "
    "Failed to commit the transaction after 20 retries."
)


@geneva.udf(data_type=pa.int64())
def _plus_one(a: int) -> int:
    return a + 1


class _JobsTableFaults:
    """Makes chosen writes to the jobs table lose the commit race.

    ``lose(match, times)`` makes the next ``times`` writes for which
    ``match(op, kwargs)`` is true raise the commit-exhausted error without
    touching the table, as a write that lost every internal retry does.
    """

    def __init__(self) -> None:
        self._rules: list[list[Any]] = []
        self.lost: list[str] = []

    def lose(
        self,
        match: Callable[[str, dict[str, Any]], bool],
        times: float = math.inf,
    ) -> None:
        self._rules.append([match, times])

    def recover(self) -> None:
        """Let every later write land."""
        self._rules.clear()

    def check(self, op: str, kwargs: dict[str, Any]) -> None:
        for rule in self._rules:
            match, remaining = rule
            if remaining > 0 and match(op, kwargs):
                rule[1] = remaining - 1
                self.lost.append(op)
                raise RuntimeError(COMMIT_EXHAUSTED)


class _LosingTable:
    """Jobs-table handle whose writes consult :class:`_JobsTableFaults`."""

    def __init__(self, table: Any, faults: _JobsTableFaults) -> None:
        self._table = table
        self._faults = faults

    def __getattr__(self, name: str) -> Any:
        return getattr(self._table, name)

    def update(self, *args: Any, **kwargs: Any) -> Any:
        self._faults.check("update", kwargs)
        return self._table.update(*args, **kwargs)

    def add(self, *args: Any, **kwargs: Any) -> Any:
        self._faults.check("add", kwargs)
        return self._table.add(*args, **kwargs)


def _status_write(status: JobStatus) -> Callable[[str, dict[str, Any]], bool]:
    def match(op: str, kwargs: dict[str, Any]) -> bool:
        return op == "update" and kwargs["values"].get("status") == status.value

    return match


def _field_write(field: str) -> Callable[[str, dict[str, Any]], bool]:
    def match(op: str, kwargs: dict[str, Any]) -> bool:
        return op == "update" and field in kwargs["values"]

    return match


def _append(op: str, kwargs: dict[str, Any]) -> bool:
    return op == "add"


@pytest.fixture
def faults(monkeypatch: pytest.MonkeyPatch) -> _JobsTableFaults:
    """Route every jobs-table handle through the fault injector; retry fast."""
    injector = _JobsTableFaults()
    original = JobStateManager.get_table

    def get_table(self: JobStateManager, checkout_latest: bool = False) -> Any:
        return _LosingTable(original(self, checkout_latest), injector)

    monkeypatch.setattr(JobStateManager, "get_table", get_table)
    monkeypatch.setattr(geneva_utils, "RETRY_LANCE_INITIAL_SECS", 0.0)
    monkeypatch.setattr(geneva_utils, "RETRY_LANCE_MAX_SECS", 0.0)
    return injector


@pytest.fixture
def env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """A real table with a virtual column and a launched job."""
    db = geneva.connect(str(tmp_path))
    tbl = db.create_table("t", pa.table({"a": pa.array([1, 2], type=pa.int64())}))
    tbl.add_columns({"b": _plus_one})
    job_id = db._history.launch("t", "b").job_id
    monkeypatch.setattr(ray_pipeline.ray, "get", lambda ref, timeout=None: True)
    return {"db_uri": str(tmp_path), "table": tbl, "job_id": job_id, "db": db}


def _job(env: dict[str, Any]) -> Any:
    return geneva.connect(env["db_uri"])._history.get(env["job_id"])[0]


# --- retry classification ---------------------------------------------------


def test_retry_lance_retries_lancedb_commit_conflict(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(geneva_utils, "RETRY_LANCE_INITIAL_SECS", 0.0)
    monkeypatch.setattr(geneva_utils, "RETRY_LANCE_MAX_SECS", 0.0)
    attempts = {"n": 0}

    @geneva_utils.retry_lance
    def write() -> str:
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise RuntimeError(COMMIT_EXHAUSTED)
        return "ok"

    assert write() == "ok"
    assert attempts["n"] == 3


def test_retry_lance_gives_up_on_a_commit_conflict_that_never_clears(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The retry is bounded by the usual attempt budget."""
    monkeypatch.setattr(geneva_utils, "RETRY_LANCE_INITIAL_SECS", 0.0)
    monkeypatch.setattr(geneva_utils, "RETRY_LANCE_MAX_SECS", 0.0)
    attempts = {"n": 0}

    @geneva_utils.retry_lance
    def write() -> None:
        attempts["n"] += 1
        raise RuntimeError(COMMIT_EXHAUSTED)

    with pytest.raises(RuntimeError, match="Failed to commit the transaction"):
        write()
    assert attempts["n"] == geneva_utils.RETRY_LANCE_ATTEMPTS


# --- each jobs-table write survives losing a few races ------------------------


def test_launch_retries_a_lost_append(faults: _JobsTableFaults, tmp_path: Path) -> None:
    db = geneva.connect(str(tmp_path))
    db.create_table("t", pa.table({"a": pa.array([1], type=pa.int64())}))
    faults.lose(_append, times=2)

    job = db._history.launch("t", "b")

    assert faults.lost == ["add", "add"]
    rows = db._history.list_jobs("t", status=None)
    assert [r.job_id for r in rows] == [job.job_id]


def test_set_running_retries_a_lost_commit(
    faults: _JobsTableFaults, env: dict[str, Any]
) -> None:
    faults.lose(_status_write(JobStatus.RUNNING), times=2)

    env["db"]._history.set_running(env["job_id"])

    assert len(faults.lost) == 2
    assert _job(env).status == JobStatus.RUNNING.value


def test_set_completed_retries_a_lost_commit(
    faults: _JobsTableFaults, env: dict[str, Any]
) -> None:
    env["db"]._history.set_running(env["job_id"])
    faults.lose(_status_write(JobStatus.DONE), times=2)

    env["db"]._history.set_completed(env["job_id"])

    job = _job(env)
    assert len(faults.lost) == 2
    assert job.status == JobStatus.DONE.value
    assert job.completed_at is not None
    assert job.events == ["Job completed with status DONE"]


def test_set_failed_retries_a_lost_commit(
    faults: _JobsTableFaults, env: dict[str, Any]
) -> None:
    env["db"]._history.set_running(env["job_id"])
    faults.lose(_status_write(JobStatus.FAILED), times=2)

    env["db"]._history.set_failed(env["job_id"], "boom")

    job = _job(env)
    assert job.status == JobStatus.FAILED.value
    assert job.events == ["Job failed: boom"]


def test_add_event_retries_a_lost_commit_without_duplicating(
    faults: _JobsTableFaults, env: dict[str, Any]
) -> None:
    faults.lose(_field_write("events"), times=2)

    env["db"]._history.add_event(env["job_id"], "Job planning")

    assert _job(env).events == ["Job planning"]


def test_update_metrics_retries_a_lost_commit(
    faults: _JobsTableFaults, env: dict[str, Any]
) -> None:
    faults.lose(_field_write("metrics"), times=2)

    env["db"]._history.update_metrics(
        env["job_id"], {"rows": {"n": 5, "total": 10, "done": False, "desc": "rows"}}
    )

    assert [m.name for m in _job(env).metrics] == ["rows"]


def test_set_object_ref_retries_a_lost_commit(
    faults: _JobsTableFaults, env: dict[str, Any]
) -> None:
    faults.lose(_field_write("object_ref"), times=2)

    env["db"]._history.set_object_ref(env["job_id"], b"ref")

    assert _job(env).object_ref is not None


# --- drivers: losing bookkeeping writes never fails the job -------------------


class _RemoteMethod:
    def remote(self, *args: object) -> None:
        return None


class _FakeTracker:
    flush = _RemoteMethod()
    mark_job_done = _RemoteMethod()


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


def _backfill_sparse(env: dict[str, Any]) -> object:
    return run_ray_add_column_remote._function(
        env["table"].get_reference(),
        "b",
        job_id=env["job_id"],
        job_tracker=_FakeTracker(),
        attempt=env.get("attempt"),
        update_mode="sparse_rows",
        where="a > 1",
    )


def _backfill(env: dict[str, Any]) -> object:
    return run_ray_add_column_remote._function(
        env["table"].get_reference(),
        "b",
        job_id=env["job_id"],
        udf=_plus_one,
        job_tracker=_FakeTracker(),
        attempt=env.get("attempt"),
    )


def _refresh(env: dict[str, Any]) -> object:
    return run_ray_refresh_remote._function(
        env["table"].get_reference(),
        job_id=env["job_id"],
        job_tracker=_FakeTracker(),
        attempt=env.get("attempt"),
    )


def _bulk_load(env: dict[str, Any]) -> object:
    return run_ray_bulk_load_remote._function(
        env["table"].get_reference(),
        "unused://source",
        "a",
        ["b"],
        job_id=env["job_id"],
        job_tracker=_FakeTracker(),
        attempt=env.get("attempt"),
    )


# Each driver: the module and function holding its data work, and how to run it.
DRIVERS: dict[str, tuple[Any, str, Callable[[dict[str, Any]], object]]] = {
    "backfill-sparse": (sparse_pipeline, "run_ray_sparse_update", _backfill_sparse),
    "backfill": (ray_pipeline, "run_ray_add_column", _backfill),
    "refresh": (ray_pipeline, "run_ray_copy_table", _refresh),
    "bulk-load": (ray_pipeline, "run_ray_bulk_load", _bulk_load),
}


def _stub_work(
    monkeypatch: pytest.MonkeyPatch,
    driver: str,
    work: list[str],
    error: Exception | None = None,
) -> Callable[[dict[str, Any]], object]:
    """Replace the driver's data work with a stub; return the driver runner."""
    module, attr, run = DRIVERS[driver]

    def stub(*args: object, **kwargs: object) -> SparseUpdateResult:
        if error is not None:
            raise error
        work.append(driver)
        return _sparse_result()

    monkeypatch.setattr(module, attr, stub)
    return run


@pytest.mark.parametrize("driver", sorted(DRIVERS))
def test_driver_does_the_work_when_set_running_never_lands(
    driver: str,
    faults: _JobsTableFaults,
    env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    work: list[str] = []
    run = _stub_work(monkeypatch, driver, work)
    faults.lose(_status_write(JobStatus.RUNNING))

    run(env)

    assert work == [driver]
    job = _job(env)
    assert job.status == JobStatus.DONE.value
    assert not any(e.startswith("Job failed") for e in job.events or [])


def _end_earlier_run(env: dict[str, Any], status: JobStatus) -> None:
    """Leave the job's row as an earlier run under the same id ended it."""
    history = env["db"]._history
    history.set_running(env["job_id"])
    if status is JobStatus.FAILED:
        history.set_failed(env["job_id"], "earlier run")
    else:
        history.set_completed(env["job_id"])


@pytest.mark.parametrize("ended", [JobStatus.DONE, JobStatus.FAILED])
@pytest.mark.parametrize("driver", sorted(DRIVERS))
def test_rerun_of_an_ended_job_does_no_work_until_marked_running(
    driver: str,
    ended: JobStatus,
    faults: _JobsTableFaults,
    env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """While the row says the job ended, cleanup treats its table as free and
    may resume compaction, so a rerun must not work under that row."""
    _end_earlier_run(env, ended)
    work: list[str] = []
    run = _stub_work(monkeypatch, driver, work)
    faults.lose(_status_write(JobStatus.RUNNING))

    with pytest.raises(Exception, match="Failed to commit the transaction"):
        run(env)

    assert work == []
    assert _job(env).status == ended.value


def test_rerun_does_no_work_when_its_status_cannot_be_read(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """If set_running is lost and the row can't be read, the driver can't tell
    a new job from a rerun of an ended one, so it does not start."""
    work: list[str] = []
    run = _stub_work(monkeypatch, "backfill-sparse", work)
    faults.lose(_status_write(JobStatus.RUNNING))
    original_get = JobStateManager.get
    unreadable = {"on": True}

    def get(self: JobStateManager, job_id: str) -> Any:
        if unreadable["on"]:
            raise OSError("storage unavailable")
        return original_get(self, job_id)

    monkeypatch.setattr(JobStateManager, "get", get)

    with pytest.raises(Exception, match="Failed to commit the transaction"):
        run(env)

    unreadable["on"] = False
    assert work == []


def test_rerun_of_a_running_job_works_when_set_running_never_lands(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A row that already says RUNNING, as a dead driver of the same id left
    it, is not read as ended, so the replacement driver still works."""
    env["db"]._history.set_running(env["job_id"])
    work: list[str] = []
    run = _stub_work(monkeypatch, "backfill-sparse", work)
    faults.lose(_status_write(JobStatus.RUNNING))

    run(env)

    assert work == ["backfill-sparse"]
    assert _job(env).status == JobStatus.DONE.value


@pytest.mark.parametrize("driver", sorted(DRIVERS))
def test_driver_succeeds_when_its_final_status_write_never_lands(
    driver: str,
    faults: _JobsTableFaults,
    env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """The work committed, so the job is a success; its row stays RUNNING
    rather than being turned into a failure."""
    work: list[str] = []
    run = _stub_work(monkeypatch, driver, work)
    faults.lose(_status_write(JobStatus.DONE))

    with caplog.at_level(logging.WARNING):
        run(env)

    assert work == [driver]
    job = _job(env)
    assert job.status == JobStatus.RUNNING.value
    assert not any(e.startswith("Job failed") for e in job.events or [])
    assert env["job_id"] in caplog.text


@pytest.mark.parametrize("driver", sorted(DRIVERS))
def test_driver_records_a_real_failure_through_lost_commits(
    driver: str,
    faults: _JobsTableFaults,
    env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A job whose own work fails is still marked FAILED when the failure
    write loses a few races."""
    run = _stub_work(monkeypatch, driver, [], error=RuntimeError("udf exploded"))
    faults.lose(_status_write(JobStatus.FAILED), times=2)

    with pytest.raises(Exception, match="udf exploded"):
        run(env)

    job = _job(env)
    assert job.status == JobStatus.FAILED.value
    assert job.events[-1].endswith("udf exploded")


# --- the submitter saves a final status its driver could not ----------------
#
# The submitter holds its attempt's verified result, the Ray task's outcome,
# and the attempt's durable identity, the object_ref it saved on the row. So it
# repairs the row only while the row still belongs to that attempt.

_ATTEMPT = b"attempt-1"


def _strand(
    faults: _JobsTableFaults,
    env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    status: JobStatus,
    error: Exception | None = None,
) -> RayJobState:
    """Run an attempt whose final ``status`` write never lands, then let writes
    land again. Returns the submitter's state for that attempt."""
    history = env["db"]._history
    history.set_object_ref(env["job_id"], _ATTEMPT)
    run = _stub_work(monkeypatch, "backfill-sparse", [], error=error)
    faults.lose(_status_write(status))
    if error is None:
        run(env)
    else:
        with pytest.raises(Exception, match=str(error)):
            run(env)
    faults.recover()
    assert _job(env).status == JobStatus.RUNNING.value
    state = RayJobState(history, env["job_id"], env["table"].get_reference())
    state.object_ref = _ATTEMPT
    return state


def _replace(env: dict[str, Any]) -> None:
    """Start a replacement attempt under the same job id."""
    history = env["db"]._history
    history.launch("t", "b", job_id=env["job_id"], reset_object_ref=True)
    history.set_object_ref(env["job_id"], b"attempt-2")
    history.set_running(env["job_id"])


def _task_error(message: str) -> ray.exceptions.RayTaskError:
    """What the submitter's Ray future raises when the driver raised."""
    return ray.exceptions.RayTaskError(
        "run_ray_add_column_remote", "", RuntimeError(message)
    )


def test_submitter_saves_done_that_its_driver_could_not(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    state = _strand(faults, env, monkeypatch, JobStatus.DONE)

    state.record_result(None)

    assert state.wait_result_recorded(5.0)
    job = _job(env)
    assert job.status == JobStatus.DONE.value
    assert job.completed_at is not None


def test_submitter_saves_failed_that_its_driver_could_not(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    error = RuntimeError("udf exploded")
    state = _strand(faults, env, monkeypatch, JobStatus.FAILED, error=error)

    state.record_result(_task_error("udf exploded"))

    assert state.wait_result_recorded(5.0)
    job = _job(env)
    assert job.status == JobStatus.FAILED.value
    assert job.events[-1] == "Job failed: RuntimeError: udf exploded"


def test_submitter_does_not_repair_a_replacement_started_before_it(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    state = _strand(faults, env, monkeypatch, JobStatus.DONE)
    _replace(env)

    state.record_result(None)

    assert state.wait_result_recorded(5.0)
    job = _job(env)
    assert job.status == JobStatus.RUNNING.value
    assert job.object_ref == base64.b64encode(b"attempt-2").decode()


def test_submitter_does_not_repair_a_replacement_started_after_its_check(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The reviewer's interleaving: the replacement starts after the repair has
    read the row as its own, before it writes."""
    state = _strand(faults, env, monkeypatch, JobStatus.DONE)
    original_get = JobStateManager.get
    reads = {"n": 0}

    def get_then_replace(self: JobStateManager, job_id: str) -> Any:
        rows = original_get(self, job_id)
        reads["n"] += 1
        if reads["n"] == 1:
            _replace(env)
        return rows

    monkeypatch.setattr(JobStateManager, "get", get_then_replace)

    state.record_result(None)

    assert state.wait_result_recorded(5.0)
    monkeypatch.setattr(JobStateManager, "get", original_get)
    job = _job(env)
    assert job.status == JobStatus.RUNNING.value
    assert job.object_ref == base64.b64encode(b"attempt-2").decode()


def test_submitter_writes_nothing_when_the_driver_saved_its_status(
    env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    history = env["db"]._history
    history.set_object_ref(env["job_id"], _ATTEMPT)
    _stub_work(monkeypatch, "backfill-sparse", [])(env)
    assert _job(env).status == JobStatus.DONE.value
    version = history.get_table(True).version
    state = RayJobState(history, env["job_id"], env["table"].get_reference())
    state.object_ref = _ATTEMPT

    state.record_result(None)

    assert state.wait_result_recorded(5.0)
    assert history.get_table(True).version == version


def test_submitter_without_an_attempt_identity_does_not_repair(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without a saved object_ref it can't tell its attempt from a replacement."""
    state = _strand(faults, env, monkeypatch, JobStatus.DONE)
    state.object_ref = None

    state.record_result(None)

    assert state.wait_result_recorded(5.0)
    assert _job(env).status == JobStatus.RUNNING.value


# Futures for _FakeObjectRef, kept outside it so the ref itself pickles.
_FUTURES: dict[str, Future[Any]] = {}


class _FakeObjectRef:
    def __init__(self, key: str) -> None:
        self.key = key

    def future(self) -> Future[Any]:
        return _FUTURES[self.key]


class _ResultSpy(RayJobState):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.results: list[BaseException | None] = []

    def record_result(self, error: BaseException | None) -> None:
        self.results.append(error)


@pytest.mark.parametrize("fails", [False, True])
def test_submit_hands_every_attempt_result_to_the_submitter(
    env: dict[str, Any], fails: bool
) -> None:
    key = f"{env['job_id']}-{fails}"
    _FUTURES[key] = Future()
    history = env["db"]._history
    spy = _ResultSpy(history, env["job_id"])

    ray_pipeline._submit_ray_job(
        history, env["job_id"], lambda attempt: _FakeObjectRef(key), state=spy
    )
    error = _task_error("boom") if fails else None
    if error is None:
        _FUTURES.pop(key).set_result({"rows_processed": 1})
    else:
        _FUTURES.pop(key).set_exception(error)

    assert spy.results == [error]


# --- remote polling ends once the driver is gone ------------------------------


def test_remote_poll_stops_when_the_driver_exited_without_a_status(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """With no final status and an exited driver, polling stops with an error
    instead of waiting forever, and claims nothing about the outcome."""
    _strand(faults, env, monkeypatch, JobStatus.DONE)
    remote = RemoteJob.from_job(env["db"], env["job_id"])

    with pytest.raises(RuntimeError, match="driver exited"):
        remote._poll_until_done(
            timeout=5.0, refresh_secs=0.01, exit_grace_s=0.05, bars=Mock()
        )

    assert _job(env).status == JobStatus.RUNNING.value


def test_remote_done_ends_a_sync_wait_when_the_driver_exited_without_a_status(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sync backfill waits on ``done()``; it must end too, and ``result()``
    then raises rather than reporting success."""
    _strand(faults, env, monkeypatch, JobStatus.DONE)
    monkeypatch.setattr(remote_module, "DRIVER_EXIT_GRACE_S", 0.0)
    remote = RemoteJob.from_job(env["db"], env["job_id"])

    assert remote.done() is True
    with pytest.raises(RuntimeError, match="driver exited"):
        remote.result(timeout=5.0, bars=Mock())


def test_remote_poll_waits_while_the_driver_runs(env: dict[str, Any]) -> None:
    history = env["db"]._history
    history.set_running(env["job_id"])
    writer = history.start_driver_heartbeat(env["job_id"])
    assert writer is not None
    assert writer.wait_written(5.0)
    remote = RemoteJob.from_job(env["db"], env["job_id"])
    try:
        with pytest.raises(TimeoutError):
            remote._poll_until_done(
                timeout=0.2, refresh_secs=0.01, exit_grace_s=0.0, bars=Mock()
            )
    finally:
        writer.stop()


def _write_raw_heartbeat(history: JobStateManager, record: dict[str, Any]) -> None:
    """Write a heartbeat object exactly as given, as a delayed write would."""
    with tempfile.TemporaryDirectory() as tmp:
        local = os.path.join(tmp, "heartbeat.json")
        with open(local, "w") as f:
            json.dump(record, f)
        history._heartbeats._get_session().upload_file(
            local, heartbeat_path(record["job_id"])
        )


def test_late_exit_heartbeat_does_not_complete_a_replacement(
    env: dict[str, Any],
) -> None:
    """The reviewer's reproducer: an earlier driver's exit heartbeat, claiming
    DONE, lands after a replacement under the same id has started."""
    history, job_id = env["db"]._history, env["job_id"]
    history.set_object_ref(job_id, b"attempt-1")
    history.set_running(job_id)
    history.set_completed(job_id)
    _replace(env)
    _write_raw_heartbeat(
        history,
        {
            "job_id": job_id,
            "state": DRIVER_EXITED,
            "started_at": "2026-11-10T12:00:00+00:00",
            "written_at": "2026-11-10T12:30:00+00:00",
            "interval_s": 30.0,
            "lease_s": 120.0,
            "seq": 61,
            "schema_version": 1,
            "outcome": JobStatus.DONE.value,
        },
    )

    observed = env["db"].get_job(job_id)

    assert (observed.status, _job(env).status) == ("RUNNING", "RUNNING")


# --- attempt tokens bind the driver's outcome to its attempt ------------------
#
# The submitter saves a fresh attempt token as the row's object_ref before it
# submits the driver, and passes the token to the driver. The driver records
# its outcome under that token, a plain object write with no commit race, and
# fences its own final status write on it. Readers apply only the outcome
# recorded under the token the row names now.


def _as_submitted(env: dict[str, Any], attempt: bytes) -> None:
    """Save ``attempt`` as the row's attempt and hand it to the driver."""
    env["db"]._history.set_object_ref(env["job_id"], attempt)
    env["attempt"] = attempt


def test_submit_saves_the_attempt_before_submitting_and_passes_it_on(
    env: dict[str, Any],
) -> None:
    history = env["db"]._history
    seen: dict[str, Any] = {}

    def submit(attempt: bytes | None) -> _FakeObjectRef:
        seen["attempt"] = attempt
        seen["row_ref"] = _job(env).object_ref
        _FUTURES["submit-order"] = Future()
        return _FakeObjectRef("submit-order")

    state = RayJobState(history, env["job_id"])
    ray_pipeline._submit_ray_job(history, env["job_id"], submit, state=state)

    attempt = seen["attempt"]
    assert attempt
    assert seen["row_ref"] == base64.b64encode(attempt).decode()
    assert state.object_ref == attempt
    _FUTURES.pop("submit-order").set_result(None)


def test_submit_without_a_saved_attempt_stops_and_can_be_retried(
    faults: _JobsTableFaults, env: dict[str, Any]
) -> None:
    faults.lose(_field_write("object_ref"))
    history = env["db"]._history
    spy = _ResultSpy(history, env["job_id"])
    seen: list[bytes] = []

    def submit(attempt: bytes) -> _FakeObjectRef:
        seen.append(attempt)
        _FUTURES["recovered-attempt"] = Future()
        return _FakeObjectRef("recovered-attempt")

    with pytest.raises(geneva.JobNotSubmittedError, match="was not submitted") as error:
        ray_pipeline._submit_ray_job(history, env["job_id"], submit, state=spy)

    assert str(error.value.__cause__) == COMMIT_EXHAUSTED
    assert seen == []
    assert spy.results == []
    assert spy.object_ref is None
    assert _job(env).status == JobStatus.PENDING.value

    faults.recover()
    ray_pipeline._submit_ray_job(history, env["job_id"], submit, state=spy)
    assert seen == [spy.object_ref]
    assert _job(env).object_ref == base64.b64encode(seen[0]).decode()
    _FUTURES.pop("recovered-attempt").set_result(None)
    assert spy.results == [None]


def test_tracker_cleanup_failure_preserves_not_submitted_error(
    env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    history = env["db"]._history
    monkeypatch.setattr(
        history, "set_object_ref", Mock(side_effect=RuntimeError("persist failed"))
    )
    monkeypatch.setattr(
        ray_pipeline.ray, "kill", Mock(side_effect=RuntimeError("tracker gone"))
    )
    submit = Mock()

    with pytest.raises(geneva.JobNotSubmittedError) as error:
        ray_pipeline._submit_ray_job(history, env["job_id"], submit, job_tracker=Mock())

    assert str(error.value.__cause__) == "persist failed"
    submit.assert_not_called()


@pytest.mark.parametrize("kind", ["add_column", "refresh", "bulk_load"])
@pytest.mark.parametrize("replacement", [False, True])
def test_dispatch_token_failure_does_not_submit_or_fail_a_replacement(
    env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    kind: str,
    replacement: bool,
) -> None:
    original = JobStateManager.set_object_ref

    def fail_save(self: JobStateManager, job_id: str, attempt: bytes) -> None:
        if replacement:
            history = geneva.connect(env["db_uri"])._history
            original(history, job_id, b"replacement")
            history.set_running(job_id)
        raise RuntimeError(COMMIT_EXHAUSTED)

    monkeypatch.setattr(JobStateManager, "set_object_ref", fail_save)
    tracker_factory = Mock()
    tracker = tracker_factory.remote.return_value
    monkeypatch.setattr(
        ray_pipeline, "job_tracker_options", Mock(return_value=tracker_factory)
    )
    monkeypatch.setattr(ray_pipeline, "head_pin_options", dict)
    remote = Mock()
    monkeypatch.setattr(ray_pipeline, f"run_ray_{kind}_remote", remote)
    kill = Mock()
    close = Mock()
    monkeypatch.setattr(ray_pipeline.ray, "kill", kill)
    monkeypatch.setattr(ray_pipeline.telemetry, "close_span", close)

    dispatch = getattr(ray_pipeline, f"dispatch_run_ray_{kind}")
    args: list[Any] = [env["table"].get_reference()]
    if kind == "add_column":
        args.append("b")
    elif kind == "bulk_load":
        args.extend(["source.parquet", "a", ["b"]])
    with pytest.raises(geneva.JobNotSubmittedError, match="was not submitted") as error:
        dispatch(*args, job_id=env["job_id"])

    assert isinstance(error.value, geneva.JobNotSubmittedError)
    remote.options.return_value.remote.assert_not_called()
    kill.assert_called_once_with(tracker, no_restart=True)
    close.assert_called_once()
    assert close.call_args.args[1] is error.value
    job = _job(env)
    assert job.status == (
        JobStatus.RUNNING.value if replacement else JobStatus.PENDING.value
    )
    assert job.object_ref == (
        base64.b64encode(b"replacement").decode() if replacement else None
    )


@pytest.mark.parametrize("driver", sorted(DRIVERS))
def test_driver_outcome_completes_the_job_when_its_done_write_never_lands(
    driver: str,
    faults: _JobsTableFaults,
    env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _as_submitted(env, _ATTEMPT)
    run = _stub_work(monkeypatch, driver, [])
    faults.lose(_status_write(JobStatus.DONE))

    run(env)

    assert _job(env).status == JobStatus.RUNNING.value
    faults.recover()
    observed = env["db"].get_job(env["job_id"])
    assert observed.status == JobStatus.DONE.value
    assert _job(env).status == JobStatus.DONE.value


@pytest.mark.parametrize("driver", sorted(DRIVERS))
def test_driver_outcome_fails_the_job_when_its_failed_write_never_lands(
    driver: str,
    faults: _JobsTableFaults,
    env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _as_submitted(env, _ATTEMPT)
    run = _stub_work(monkeypatch, driver, [], error=RuntimeError("udf exploded"))
    faults.lose(_status_write(JobStatus.FAILED))

    with pytest.raises(Exception, match="udf exploded"):
        run(env)

    assert _job(env).status == JobStatus.RUNNING.value
    faults.recover()
    observed = env["db"].get_job(env["job_id"])
    assert observed.status == JobStatus.FAILED.value
    assert observed.events[-1] == "Job failed: RuntimeError: udf exploded"


def test_driver_outcome_is_returned_while_the_table_rejects_the_repair(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Remote polling ends on the recorded outcome even before the row can be
    repaired; a later read repairs it."""
    _as_submitted(env, _ATTEMPT)
    run = _stub_work(monkeypatch, "backfill-sparse", [])
    faults.lose(_status_write(JobStatus.DONE))
    run(env)
    remote = RemoteJob.from_job(env["db"], env["job_id"])

    record = remote._poll_until_done(timeout=5.0, refresh_secs=0.01, bars=Mock())

    assert record.status == JobStatus.DONE.value
    assert _job(env).status == JobStatus.RUNNING.value
    faults.recover()
    env["db"].get_job(env["job_id"])
    assert _job(env).status == JobStatus.DONE.value


def test_an_earlier_attempts_outcome_never_completes_a_replacement(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    _as_submitted(env, _ATTEMPT)
    run = _stub_work(monkeypatch, "backfill-sparse", [])
    faults.lose(_status_write(JobStatus.DONE))
    run(env)
    faults.recover()
    _replace(env)

    observed = env["db"].get_job(env["job_id"])

    assert (observed.status, _job(env).status) == ("RUNNING", "RUNNING")
    assert _job(env).object_ref == base64.b64encode(b"attempt-2").decode()


def test_outcome_repair_never_finishes_a_replacement_started_mid_repair(
    faults: _JobsTableFaults, env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A replacement starting after the reader found the earlier attempt's
    outcome, before it writes, is left RUNNING."""
    _as_submitted(env, _ATTEMPT)
    run = _stub_work(monkeypatch, "backfill-sparse", [])
    faults.lose(_status_write(JobStatus.DONE))
    run(env)
    faults.recover()
    original = JobStateManager.read_attempt_outcome
    replaced = {"done": False}

    def read_then_replace(self: JobStateManager, job_id: str, attempt: bytes) -> Any:
        outcome = original(self, job_id, attempt)
        if not replaced["done"]:
            replaced["done"] = True
            _replace(env)
        return outcome

    monkeypatch.setattr(JobStateManager, "read_attempt_outcome", read_then_replace)

    observed = env["db"].get_job(env["job_id"])

    monkeypatch.setattr(JobStateManager, "read_attempt_outcome", original)
    assert (observed.status, _job(env).status) == ("RUNNING", "RUNNING")
    assert _job(env).object_ref == base64.b64encode(b"attempt-2").decode()


def test_a_superseded_driver_does_not_finish_the_replacement(
    env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """The driver's own final write is fenced on its attempt, so a driver
    whose job was relaunched under the same id leaves the replacement alone."""
    _as_submitted(env, _ATTEMPT)

    def work_then_get_replaced(*args: object, **kwargs: object) -> SparseUpdateResult:
        _replace(env)
        return _sparse_result()

    monkeypatch.setattr(
        sparse_pipeline, "run_ray_sparse_update", work_then_get_replaced
    )

    _backfill_sparse(env)

    job = env["db"].get_job(env["job_id"])
    assert job.status == JobStatus.RUNNING.value
    assert job.object_ref == base64.b64encode(b"attempt-2").decode()


@pytest.mark.ray
def test_real_backfill_records_its_outcome_under_the_rows_attempt(
    tmp_path: Path, local_ray_context: None
) -> None:
    """Through real Ray dispatch: the row names the attempt token the driver
    was given, and that driver recorded its outcome under it."""
    db = geneva.connect(str(tmp_path))
    tbl = db.create_table("t", pa.table({"a": pa.array([1, 2, 3], type=pa.int64())}))
    tbl.add_columns({"b": _plus_one})
    job_id = "real-backfill"

    tbl.backfill("b", job_id=job_id, concurrency=1)

    job = db.get_job(job_id)
    assert job.status == JobStatus.DONE.value
    assert job.object_ref
    outcome = db._history.read_attempt_outcome(job_id, base64.b64decode(job.object_ref))
    assert outcome is not None
    assert outcome.status == JobStatus.DONE.value
