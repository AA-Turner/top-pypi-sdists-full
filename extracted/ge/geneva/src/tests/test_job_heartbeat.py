# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Driver heartbeats tell a live job driver from a dead one (GEN-970)."""

from __future__ import annotations

import contextlib
import json
import logging
import os
import signal
import socket
import subprocess
import sys
import threading
import time
import uuid
from datetime import timedelta
from typing import TYPE_CHECKING, Any

import attrs
import lance
import pyarrow as pa
import pytest
from lance.file import LanceFileSession

import geneva
import geneva.jobs.jobs as jobs_module
import geneva.runners.ray.pipeline as ray_pipeline
from geneva.jobs import DriverHeartbeat, DriverLiveness, JobStateManager
from geneva.jobs.heartbeat import (
    DEFAULT_HEARTBEAT_INTERVAL_S,
    DEFAULT_LEASE_INTERVALS,
    DRIVER_EXITED,
    DRIVER_RUNNING,
    HEARTBEAT_INTERVAL_ENV,
    HEARTBEAT_LEASE_ENV,
    DriverHeartbeatWriter,
    HeartbeatStore,
    heartbeat_interval_s,
    heartbeat_lease_s,
    heartbeat_path,
    heartbeat_storage_options,
    set_driver_phase,
)
from geneva.runners.ray import sparse_pipeline
from geneva.runners.ray.pipeline import run_ray_add_column_remote
from geneva.runners.sparse_update import SparseUpdateResult
from geneva.utils import dt_now_utc

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from pathlib import Path

_FAST_INTERVAL_S = 0.05
_WAIT_S = 10.0


@geneva.udf(data_type=pa.int64())
def _plus_one(a: int) -> int:
    return a + 1


def _wait_for(predicate: Callable[[], bool], timeout: float = _WAIT_S) -> None:
    deadline = time.monotonic() + timeout
    while not predicate():
        if time.monotonic() > deadline:
            raise AssertionError("condition not met in time")
        time.sleep(0.01)


def _heartbeat(**overrides: Any) -> DriverHeartbeat:
    now = dt_now_utc()
    values: dict[str, Any] = {
        "job_id": "job-1",
        "state": DRIVER_RUNNING,
        "started_at": now,
        "written_at": now,
        "interval_s": 30.0,
        "lease_s": 120.0,
        "seq": 1,
    }
    values.update(overrides)
    return DriverHeartbeat(**values)


@pytest.fixture
def hist(tmp_path: Path) -> JobStateManager:
    return geneva.connect(str(tmp_path))._history


@pytest.fixture
def fast_heartbeats(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(HEARTBEAT_INTERVAL_ENV, str(_FAST_INTERVAL_S))


class _MemoryStore:
    """Heartbeat store that keeps writes in memory, optionally failing some."""

    def __init__(self, failures: int = 0) -> None:
        self.writes: list[DriverHeartbeat] = []
        self._failures = failures

    def write(self, heartbeat: DriverHeartbeat) -> None:
        if self._failures > 0:
            self._failures -= 1
            raise OSError("object store unavailable")
        self.writes.append(heartbeat)


class _HangingStore:
    """Heartbeat store whose writes block until released."""

    def __init__(self) -> None:
        self.release = threading.Event()
        self.entered = threading.Event()

    def write(self, heartbeat: DriverHeartbeat) -> None:
        self.entered.set()
        self.release.wait()


def _writer(store: object, job_id: str = "job-1") -> DriverHeartbeatWriter:
    return DriverHeartbeatWriter(
        store,  # type: ignore[arg-type]
        job_id,
        interval_s=_FAST_INTERVAL_S,
        lease_s=_FAST_INTERVAL_S * DEFAULT_LEASE_INTERVALS,
    )


def test_heartbeat_json_round_trip_ignores_unknown_fields() -> None:
    heartbeat = _heartbeat(phase="Executing backfill", host="h", pid=7)
    record = json.loads(heartbeat.to_json())
    assert record["schema_version"] == 1
    record["added_by_a_newer_geneva"] = True

    assert DriverHeartbeat.from_json(json.dumps(record).encode()) == heartbeat


def test_heartbeat_liveness_follows_the_lease() -> None:
    heartbeat = _heartbeat(lease_s=120.0)
    written = heartbeat.written_at

    assert heartbeat.liveness(written + timedelta(seconds=119)) is (
        DriverLiveness.ALIVE
    )
    assert heartbeat.liveness(written + timedelta(seconds=121)) is (
        DriverLiveness.STALE
    )


def test_exited_heartbeat_is_exited_at_any_age() -> None:
    heartbeat = _heartbeat(state=DRIVER_EXITED)

    assert heartbeat.liveness(heartbeat.written_at) is DriverLiveness.EXITED
    assert heartbeat.liveness(heartbeat.written_at + timedelta(days=30)) is (
        DriverLiveness.EXITED
    )


def test_heartbeat_path_keeps_job_ids_in_one_object() -> None:
    assert heartbeat_path("abc-123") == "_heartbeats/abc-123.json"
    assert heartbeat_path("a/b") == "_heartbeats/a%2Fb.json"


class _FlakySession:
    """File session whose uploads fail, e.g. with expired credentials."""

    def __init__(self, *, fail: bool) -> None:
        self.fail = fail
        self.uploads: list[str] = []

    def upload_file(self, local: str, remote: str) -> None:
        if self.fail:
            raise OSError("ExpiredToken")
        self.uploads.append(remote)


def test_store_reopens_its_session_after_a_failed_write() -> None:
    sessions: list[_FlakySession] = []

    def open_session() -> _FlakySession:
        session = _FlakySession(fail=not sessions)
        sessions.append(session)
        return session

    store = HeartbeatStore(open_session)  # type: ignore[arg-type]
    with pytest.raises(OSError, match="ExpiredToken"):
        store.write(_heartbeat())
    store.write(_heartbeat())

    assert len(sessions) == 2
    assert sessions[1].uploads == ["_heartbeats/job-1.json"]


def test_missing_heartbeat_reads_as_none(hist: JobStateManager) -> None:
    assert hist.get_heartbeat("never-ran") is None


def test_driver_liveness_by_job_and_heartbeat(hist: JobStateManager) -> None:
    job_id = hist.launch("t", "c").job_id
    hist.set_running(job_id)
    store: HeartbeatStore = hist._heartbeats

    assert hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.UNKNOWN

    store.write(_heartbeat(job_id=job_id))
    assert hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.ALIVE

    old = dt_now_utc() - timedelta(hours=1)
    store.write(_heartbeat(job_id=job_id, started_at=old, written_at=old))
    assert hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.STALE

    store.write(_heartbeat(job_id=job_id, state=DRIVER_EXITED))
    assert hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.EXITED

    hist.set_failed(job_id, "boom")
    assert hist.driver_liveness(hist.get(job_id)[0]) is None


_LONG_AGO = dt_now_utc() - timedelta(hours=1)


@pytest.mark.parametrize(
    "previous",
    [
        _heartbeat(state=DRIVER_EXITED),
        _heartbeat(started_at=_LONG_AGO, written_at=_LONG_AGO),
    ],
    ids=["exited", "killed"],
)
def test_rerun_does_not_inherit_the_previous_runs_heartbeat(
    hist: JobStateManager, previous: DriverHeartbeat
) -> None:
    job_id = hist.launch("t", "c").job_id
    hist.set_running(job_id)
    hist._heartbeats.write(attrs.evolve(previous, job_id=job_id))
    hist.set_failed(job_id, "boom")

    # Re-run under the same id; its driver has written no heartbeat yet.
    hist.launch("t", "c", job_id=job_id)
    hist.set_running(job_id)

    assert hist.get_heartbeat(job_id) is None
    assert hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.UNKNOWN


def test_deleting_a_missing_heartbeat_is_a_noop(hist: JobStateManager) -> None:
    hist._heartbeats.delete("never-ran")


def test_failing_to_clear_an_old_heartbeat_does_not_block_the_run(
    hist: JobStateManager,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    def unavailable(job_id: str) -> None:
        raise OSError("object store unavailable")

    job_id = hist.launch("t", "c").job_id
    monkeypatch.setattr(hist._heartbeats, "delete", unavailable)
    with caplog.at_level(logging.WARNING, logger="geneva.jobs.jobs"):
        hist.set_running(job_id)

    assert hist.get(job_id)[0].status == "RUNNING"
    assert "Failed to clear the previous driver heartbeat" in caplog.text


def test_heartbeat_requests_time_out_within_a_beat() -> None:
    assert heartbeat_storage_options(30.0) == {
        "timeout": "24000ms",
        "client_max_retries": "0",
    }
    # Very short intervals keep a usable floor.
    assert heartbeat_storage_options(0.05)["timeout"] == "1000ms"
    # Processes that only read heartbeats may have them disabled.
    assert heartbeat_storage_options(0) == heartbeat_storage_options(
        DEFAULT_HEARTBEAT_INTERVAL_S
    )


def test_jobs_table_session_carries_heartbeat_timeouts(
    hist: JobStateManager, monkeypatch: pytest.MonkeyPatch
) -> None:
    sessions: list[dict[str, Any]] = []

    def open_session(*args: Any, **kwargs: Any) -> LanceFileSession:
        sessions.append(kwargs)
        return LanceFileSession(*args, **kwargs)

    monkeypatch.setattr(jobs_module, "LanceFileSession", open_session)
    monkeypatch.setenv(HEARTBEAT_INTERVAL_ENV, "10")

    assert hist.get_heartbeat("never-ran") is None
    assert len(sessions) == 1
    options = sessions[0]["storage_options"]
    assert options["timeout"] == "8000ms"
    assert options["client_max_retries"] == "0"


@pytest.fixture
def unresponsive_endpoint() -> Iterator[str]:
    """An HTTP endpoint that accepts connections and never responds."""
    server = socket.create_server(("127.0.0.1", 0))
    server.settimeout(0.1)
    held: list[socket.socket] = []
    stop = threading.Event()

    def accept() -> None:
        while not stop.is_set():
            with contextlib.suppress(TimeoutError):
                held.append(server.accept()[0])

    thread = threading.Thread(target=accept, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.getsockname()[1]}"
    stop.set()
    thread.join()
    for conn in held:
        conn.close()
    server.close()


def test_hung_write_does_not_hold_back_the_next_beat(
    unresponsive_endpoint: str,
) -> None:
    interval_s = 1.0
    options = {
        "aws_endpoint": unresponsive_endpoint,
        "allow_http": "true",
        "aws_access_key_id": "test",
        "aws_secret_access_key": "test",
        "aws_region": "us-east-1",
        **heartbeat_storage_options(interval_s),
    }
    store = HeartbeatStore(
        lambda: LanceFileSession("s3://bucket/jobs.lance", storage_options=options)
    )
    attempts: list[int] = []
    write = store.write

    def counted_write(heartbeat: DriverHeartbeat) -> None:
        attempts.append(heartbeat.seq)
        write(heartbeat)

    store.write = counted_write  # type: ignore[method-assign]
    writer = DriverHeartbeatWriter(
        store, "job-1", interval_s=interval_s, lease_s=interval_s * 4
    )
    writer.start()
    try:
        # The second beat only starts once the first, hung, write gives up.
        _wait_for(lambda: len(attempts) >= 2)
    finally:
        writer.stop(timeout=_WAIT_S)

    assert attempts[:2] == [1, 2]


@pytest.mark.usefixtures("fast_heartbeats")
def test_driver_heartbeat_beats_without_jobs_table_commits(
    hist: JobStateManager,
) -> None:
    job_id = hist.launch("t", "c").job_id
    hist.set_running(job_id)
    version = hist.get_table(True).version

    writer = hist.start_driver_heartbeat(job_id)
    assert writer is not None
    _wait_for(lambda: (hist.get_heartbeat(job_id) or _heartbeat(seq=0)).seq >= 3)
    writer.stop()

    heartbeat = hist.get_heartbeat(job_id)
    assert heartbeat is not None
    assert heartbeat.state == DRIVER_EXITED
    assert heartbeat.interval_s == _FAST_INTERVAL_S
    assert heartbeat.lease_s == _FAST_INTERVAL_S * DEFAULT_LEASE_INTERVALS
    assert heartbeat.pid is not None
    assert heartbeat.host
    assert hist.get_table(True).version == version


def test_writer_reports_the_current_phase() -> None:
    store = _MemoryStore()
    writer = _writer(store)
    writer.start()
    set_driver_phase("job-1", "Job planning")
    set_driver_phase("another-job", "Executing backfill")
    _wait_for(lambda: any(w.phase == "Job planning" for w in store.writes))
    writer.stop()

    assert store.writes[0].state == DRIVER_RUNNING
    assert store.writes[-1].state == DRIVER_EXITED
    assert store.writes[-1].phase == "Job planning"
    assert [w.seq for w in store.writes] == list(range(1, len(store.writes) + 1))


def test_emit_phase_reaches_the_driver_heartbeat() -> None:
    store = _MemoryStore()
    writer = _writer(store)
    writer.start()
    ray_pipeline._emit_phase(None, "job-1", "Executing backfill")
    _wait_for(lambda: any(w.phase == "Executing backfill" for w in store.writes))
    writer.stop()

    # A stopped driver no longer takes phases.
    set_driver_phase("job-1", "late phase")
    assert store.writes[-1].phase == "Executing backfill"


def test_writer_keeps_beating_through_write_failures(
    caplog: pytest.LogCaptureFixture,
) -> None:
    store = _MemoryStore(failures=3)
    writer = _writer(store)
    with caplog.at_level(logging.INFO, logger="geneva.jobs.heartbeat"):
        writer.start()
        _wait_for(lambda: len(store.writes) >= 1)
        writer.stop()

    warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert len(warnings) == 1
    assert "1 consecutive failures" in warnings[0].getMessage()
    assert "recovered after 3 failed writes" in caplog.text
    assert store.writes[-1].state == DRIVER_EXITED


def test_writer_reports_when_a_heartbeat_last_landed() -> None:
    store = _MemoryStore(failures=2)
    writer = _writer(store)
    assert writer.seconds_since_written() is None
    assert not writer.wait_written(0)

    writer.start()
    try:
        assert writer.wait_written(_WAIT_S)
        assert store.writes, "reported landed before a write succeeded"
        since = writer.seconds_since_written()
        assert since is not None
        assert since < _WAIT_S
    finally:
        writer.stop()
    assert (writer.interval_s, writer.lease_s) == (
        _FAST_INTERVAL_S,
        _FAST_INTERVAL_S * DEFAULT_LEASE_INTERVALS,
    )


def test_listeners_hear_each_heartbeat_that_lands() -> None:
    store = _MemoryStore(failures=2)
    writer = _writer(store)
    heard: list[float] = []
    writer.add_listener(heard.append)

    def broken(written: float) -> None:
        raise RuntimeError("listener bug")

    writer.add_listener(broken)
    before = time.monotonic()
    writer.start()
    try:
        _wait_for(lambda: len(heard) >= 2)
    finally:
        writer.stop()

    assert len(heard) == len(store.writes)  # failed writes are not heard
    assert before <= heard[0] <= heard[1]


def test_stop_is_bounded_when_the_store_hangs(
    caplog: pytest.LogCaptureFixture,
) -> None:
    store = _HangingStore()
    writer = _writer(store)
    writer.start()
    assert store.entered.wait(_WAIT_S)

    started = time.monotonic()
    with caplog.at_level(logging.WARNING, logger="geneva.jobs.heartbeat"):
        writer.stop(timeout=0.1)
    store.release.set()

    assert time.monotonic() - started < 5
    assert "did not stop within" in caplog.text


def test_stop_before_start_is_a_noop() -> None:
    _writer(_MemoryStore()).stop()


def test_heartbeats_can_be_disabled(
    hist: JobStateManager, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(HEARTBEAT_INTERVAL_ENV, "0")
    job_id = hist.launch("t", "c").job_id

    assert hist.start_driver_heartbeat(job_id) is None
    assert hist.get_heartbeat(job_id) is None


@pytest.mark.parametrize("raw", ["", "soon", "-5"])
def test_unusable_interval_falls_back_to_default(
    monkeypatch: pytest.MonkeyPatch, raw: str
) -> None:
    monkeypatch.setenv(HEARTBEAT_INTERVAL_ENV, raw)
    assert heartbeat_interval_s() == DEFAULT_HEARTBEAT_INTERVAL_S


def test_lease_defaults_to_several_intervals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(HEARTBEAT_LEASE_ENV, raising=False)
    assert heartbeat_lease_s(30.0) == 30.0 * DEFAULT_LEASE_INTERVALS

    monkeypatch.setenv(HEARTBEAT_LEASE_ENV, "600")
    assert heartbeat_lease_s(30.0) == 600.0


def test_lease_shorter_than_the_interval_is_ignored(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(HEARTBEAT_LEASE_ENV, "10")
    assert heartbeat_lease_s(30.0) == 30.0 * DEFAULT_LEASE_INTERVALS


_DRIVER_SCRIPT = """
import sys, time
import geneva
hist = geneva.connect(sys.argv[1])._history
hist.start_driver_heartbeat(sys.argv[2])
time.sleep(600)
"""


def test_killed_driver_becomes_stale(hist: JobStateManager, tmp_path: Path) -> None:
    job_id = hist.launch("t", "c").job_id
    hist.set_running(job_id)
    env = {**os.environ, HEARTBEAT_INTERVAL_ENV: str(_FAST_INTERVAL_S)}
    driver = subprocess.Popen(  # noqa: S603 - fixed script, test-only
        [sys.executable, "-c", _DRIVER_SCRIPT, str(tmp_path), job_id], env=env
    )
    try:
        _wait_for(
            lambda: hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.ALIVE,
            timeout=60,
        )
        driver.send_signal(signal.SIGKILL)
        driver.wait(_WAIT_S)
    finally:
        if driver.poll() is None:
            driver.kill()

    _wait_for(lambda: hist.driver_liveness(hist.get(job_id)[0]) is DriverLiveness.STALE)
    heartbeat = hist.get_heartbeat(job_id)
    assert heartbeat is not None
    assert heartbeat.state == DRIVER_RUNNING
    assert heartbeat.pid == driver.pid


# --- driver wiring ---------------------------------------------------------


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
def driver_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, fast_heartbeats: None
) -> dict[str, Any]:
    db = geneva.connect(str(tmp_path))
    tbl = db.create_table("t", pa.table({"a": pa.array([1, 2], type=pa.int64())}))
    tbl.add_columns({"b": _plus_one})
    job_id = db._history.launch("t", "b").job_id
    return {"db_uri": str(tmp_path), "table": tbl, "job_id": job_id}


def _reader(env: dict[str, Any]) -> JobStateManager:
    return geneva.connect(env["db_uri"])._history


def _run_sparse_driver(env: dict[str, Any]) -> object:
    return run_ray_add_column_remote._function(
        env["table"].get_reference(),
        "b",
        job_id=env["job_id"],
        update_mode="sparse_rows",
        where="a > 1",
    )


def test_driver_heartbeats_while_running_and_marks_its_exit(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    seen: list[DriverLiveness | None] = []

    def work(*args: object, **kwargs: object) -> SparseUpdateResult:
        reader = _reader(driver_env)
        _wait_for(lambda: reader.get_heartbeat(driver_env["job_id"]) is not None)
        seen.append(reader.driver_liveness(reader.get(driver_env["job_id"])[0]))
        return _sparse_result()

    monkeypatch.setattr(sparse_pipeline, "run_ray_sparse_update", work)

    _run_sparse_driver(driver_env)

    assert seen == [DriverLiveness.ALIVE]
    heartbeat = _reader(driver_env).get_heartbeat(driver_env["job_id"])
    assert heartbeat is not None
    assert heartbeat.state == DRIVER_EXITED


def test_failed_driver_marks_its_exit(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*args: object, **kwargs: object) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(sparse_pipeline, "run_ray_sparse_update", fail)

    with pytest.raises(RuntimeError, match="boom"):
        _run_sparse_driver(driver_env)

    heartbeat = _reader(driver_env).get_heartbeat(driver_env["job_id"])
    assert heartbeat is not None
    assert heartbeat.state == DRIVER_EXITED


def test_heartbeat_failure_does_not_fail_the_driver(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    def no_heartbeat(self: JobStateManager, job_id: str) -> None:
        raise OSError("object store unavailable")

    monkeypatch.setattr(JobStateManager, "start_driver_heartbeat", no_heartbeat)
    monkeypatch.setattr(
        sparse_pipeline, "run_ray_sparse_update", lambda *a, **k: _sparse_result()
    )

    _run_sparse_driver(driver_env)

    job = _reader(driver_env).get(driver_env["job_id"])[0]
    assert job.status == "DONE"


def test_rerun_without_heartbeats_does_not_read_as_the_failed_run(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    job_id = driver_env["job_id"]
    reader = _reader(driver_env)
    reader._heartbeats.write(_heartbeat(job_id=job_id, state=DRIVER_EXITED))
    reader.set_failed(job_id, "previous run failed")
    monkeypatch.setenv(HEARTBEAT_INTERVAL_ENV, "0")
    seen: list[DriverLiveness | None] = []

    def work(*args: object, **kwargs: object) -> SparseUpdateResult:
        seen.append(reader.driver_liveness(reader.get(job_id)[0]))
        return _sparse_result()

    monkeypatch.setattr(sparse_pipeline, "run_ray_sparse_update", work)

    _run_sparse_driver(driver_env)

    assert seen == [DriverLiveness.UNKNOWN]


@pytest.mark.ray
def test_backfill_driver_on_ray_leaves_an_exited_heartbeat(
    tmp_path: Path, local_ray_context: None
) -> None:
    lance.write_dataset(
        pa.table({"a": pa.array(range(20), type=pa.int64())}),
        tmp_path / "test.lance",
        max_rows_per_file=10,
    )
    db = geneva.connect(str(tmp_path))
    tbl = db.open_table("test")
    tbl.add_columns({"b": _plus_one})
    job_id = uuid.uuid4().hex

    tbl.backfill("b", job_id=job_id)

    heartbeat = db._history.get_heartbeat(job_id)
    assert heartbeat is not None
    assert heartbeat.state == DRIVER_EXITED
    assert heartbeat.ray_job_id
    assert heartbeat.ray_node_id
    assert heartbeat.phase == "Executing backfill"
    assert db._history.driver_liveness(db.get_job(job_id)) is None
