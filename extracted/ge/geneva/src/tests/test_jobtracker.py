# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
import asyncio
import contextlib
import tempfile
import uuid
from datetime import timezone
from pathlib import Path
from typing import Any, cast

import pytest
import ray
from ray.util.state import get_actor

from geneva.db import connect
from geneva.jobs.jobs import (
    GENEVA_JOBS_TABLE_NAME,
    JobMetric,
    JobRecord,
    JobStateManager,
    JobStatus,
)
from geneva.runners.ray.jobtracker import (
    JobTrackerConfig,
    _JobTracker,
    job_tracker_options,
)
from geneva.runners.ray.raycluster import RayCluster
from geneva.table import TableReference

pytestmark = pytest.mark.ray


@pytest.fixture(autouse=True)
def ray_cluster() -> None:
    ray.shutdown()
    ray.init(
        log_to_driver=True,
        logging_config=ray.LoggingConfig(
            encoding="TEXT", log_level="DEBUG", additional_log_standard_attrs=["name"]
        ),
    )
    yield
    ray.shutdown()


@pytest.fixture
async def temp_db_path() -> Any:
    """Create a temporary database directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
async def db_connection(temp_db_path) -> Any:
    """Create a Geneva database connection."""
    db = connect(temp_db_path)
    yield db
    db.close()


@pytest.fixture
async def jobs_table(db_connection) -> Any:
    """Create the geneva_jobs table with proper schema."""
    # Create the jobs table using JobStateManager to ensure proper schema
    job_manager = JobStateManager(db_connection)
    return job_manager.get_table()


@pytest.fixture
async def table_reference(temp_db_path) -> TableReference:
    """Create a TableReference for testing."""
    return TableReference(
        table_id=["test_table"],
        version=None,
        db_uri=str(temp_db_path),
        namespace_client_impl=None,
        namespace_client_properties=None,
    )


@pytest.fixture
async def async_db_connection(temp_db_path, jobs_table) -> Any:
    """Create an async LanceDB connection.

    Depends on ``jobs_table`` so the ``__system`` table (and the
    dir-namespace ``__manifest``) exists before this connection opens.
    Since pylance 9.0.0b16 (lance-format/lance#7687) a dir-namespace
    connection probes ``__manifest`` once at build and treats absence as
    permanent, so child-namespace reads fail on a connection opened
    against an empty root — production always creates the jobs table
    before opening this connection.
    """
    table_ref = TableReference(
        table_id=["test_table"],
        version=None,
        db_uri=str(temp_db_path),
    )
    async_conn = await table_ref.open_system_db_async()
    yield async_conn
    if hasattr(async_conn, "close"):
        close_result = async_conn.close()
        if hasattr(close_result, "__await__"):
            await close_result


def test_jobtracker_creation(table_reference) -> None:
    """Test JobTracker can be created with required fields."""
    job_id = str(uuid.uuid4())

    # Create JobTracker instance (without Ray remote for testing)
    tracker = job_tracker_options().remote(job_id, table_reference, enable_saves=False)

    ray.get(tracker.get_all.remote())


def test_large_hydration_timeout_is_ray_compatible() -> None:
    """A huge actor deadline never enters Ray's timeout conversion path."""
    config = JobTrackerConfig(hydration_timeout_secs=1e308)
    tracker = job_tracker_options().remote(
        "large-timeout",
        None,
        enable_saves=False,
        hydration_timeout_secs=config.hydration_timeout_secs,
    )
    ray.get(tracker.mark_job_done.remote())

    done, pending_ref = RayCluster._poll_tracker_done(tracker, timeout=5.0)

    assert done is True
    assert pending_ref is None


def test_jobtracker_batch_increment(table_reference) -> None:
    """Test batch_increment updates multiple metrics in one call."""
    job_id = str(uuid.uuid4())
    tracker = job_tracker_options().remote(job_id, table_reference, enable_saves=False)

    ray.get(tracker.batch_increment.remote({"m1": 3, "m2": 7, "m3": 0}))
    metrics = ray.get(tracker.get_all.remote())

    assert metrics["m1"]["n"] == 3
    assert metrics["m2"]["n"] == 7
    assert "m3" not in metrics


def test_jobtracker_finalize_rows_ignores_late_row_updates(table_reference) -> None:
    """Finalized row metrics should not be mutated by delayed updates."""
    job_id = str(uuid.uuid4())
    tracker = job_tracker_options().remote(job_id, table_reference, enable_saves=False)

    ray.get(
        [
            tracker.set_total.remote("rows_checkpointed", 17),
            tracker.set_total.remote("rows_ready_for_commit", 17),
            tracker.set_total.remote("rows_committed", 17),
        ]
    )
    ray.get(tracker.finalize_rows.remote(17, 17, 17))

    # Simulate delayed metric updates that arrive after finalization.
    ray.get(tracker.increment.remote("rows_committed", 17))
    ray.get(
        tracker.batch_increment.remote(
            {
                "rows_checkpointed": 1,
                "rows_ready_for_commit": 1,
                "rows_committed": 1,
                "non_row_metric": 3,
            }
        )
    )
    ray.get(tracker.set_total.remote("rows_committed", 999))
    ray.get(tracker.mark_done.remote("rows_committed"))

    metrics = ray.get(tracker.get_all.remote())
    assert metrics["rows_checkpointed"]["n"] == 17
    assert metrics["rows_checkpointed"]["total"] == 17
    assert metrics["rows_checkpointed"]["done"] is True
    assert metrics["rows_ready_for_commit"]["n"] == 17
    assert metrics["rows_ready_for_commit"]["total"] == 17
    assert metrics["rows_ready_for_commit"]["done"] is True
    assert metrics["rows_committed"]["n"] == 17
    assert metrics["rows_committed"]["total"] == 17
    assert metrics["rows_committed"]["done"] is True
    assert metrics["non_row_metric"]["n"] == 3


@pytest.mark.asyncio
async def test_save_metrics_with_mock_db(
    temp_db_path, async_db_connection, db_connection
) -> None:
    """Test _save_metrics with a real async database connection."""
    job_id = str(uuid.uuid4())

    # Create the jobs table
    jsm = JobStateManager(db_connection, GENEVA_JOBS_TABLE_NAME)

    # Add a test job record
    from datetime import datetime

    jobs_table = await async_db_connection.open_table(
        GENEVA_JOBS_TABLE_NAME, namespace_path=["__system"]
    )
    time = datetime(2025, 11, 7, 9, 46, 9, 599847, tzinfo=timezone.utc)
    await jobs_table.add(
        [
            {
                "job_id": job_id,
                "table_name": "test_table",
                "column_name": "test_column",
                "status": "RUNNING",
                "metrics": [],
                "launched_at": time,
                "updated_at": time,
                "completed_at": None,
                "config": "{}",
                "launched_by": "test",
                "manifest_id": None,
                "manifest_checksum": None,
                "events": [],
                "object_ref": None,
                "job_type": "BACKFILL",
            }
        ]
    )

    # Create JobTracker and manually set up the connection
    table_ref = TableReference(
        table_id=["test_table"],
        version=None,
        db_uri=str(temp_db_path),
    )

    tracker = job_tracker_options().remote(job_id, table_ref)

    # Manually set the database connection for testing
    tracker._db = async_db_connection
    tracker._jobs_table = jobs_table

    # Test _save_metrics
    test_metrics = {
        "task1": {"n": 50, "total": 100, "done": False, "desc": "Test task"}
    }

    await tracker._save_metrics.remote(test_metrics)

    jobs = jsm.list_jobs(table_name="test_table")
    jobs[0].updated_at = None
    assert jobs == [
        JobRecord(
            table_name="test_table",
            column_name="test_column",
            job_id=job_id,
            job_type="BACKFILL",
            object_ref=None,
            status="RUNNING",
            launched_at=time,
            updated_at=None,
            completed_at=None,
            config="{}",
            launched_by="test",
            manifest_id=None,
            manifest_checksum=None,
            metrics=[
                JobMetric(name="task1", n=50, total=100, done=False, desc="Test task")
            ],
            events=[],
        )
    ]


@pytest.mark.asyncio
async def test_full_workflow_with_db(temp_db_path, db_connection) -> None:
    """Test a complete workflow with real database operations."""
    job_id = str(uuid.uuid4())

    # Set up the database with jobs table
    job_manager = JobStateManager(db_connection)
    job_record = job_manager.launch("test_table", "test_column")

    # Override with our test job_id
    job_manager.get_table().update(
        where=f"job_id = '{job_record.job_id}'", values={"job_id": job_id}
    )

    # Create async connection for JobTracker
    table_ref = TableReference(
        table_id=["test_table"],
        version=None,
        db_uri=str(temp_db_path),
    )
    async_conn = await table_ref.open_system_db_async()
    jobs_table = await async_conn.open_table(
        GENEVA_JOBS_TABLE_NAME, namespace_path=["__system"]
    )

    tracker = job_tracker_options().remote(job_id, table_ref)
    tracker._db = async_conn
    tracker._jobs_table = jobs_table

    # Test complete workflow
    await tracker.set_total.remote("download", 1000)
    await tracker.set_desc.remote("download", "foo")

    # Simulate progress
    for i in range(0, 1001, 100):
        await tracker.set.remote("download", i)
        if i == 1000:
            break

    # mark done, then flush to db (saves are now async/background)
    await tracker.mark_done.remote("download")
    assert await tracker.flush.remote() is True

    # Verify final state
    progress = await tracker.get_progress.remote("download")
    assert progress["n"] == 1000
    assert progress["total"] == 1000
    assert progress["done"] is True
    assert progress["desc"] == "foo"

    # Verify metrics updated in database
    jobs = job_manager.get(job_id)
    assert len(jobs) == 1
    stored_metrics = {m.name: m for m in jobs[0].metrics}

    metric_data = stored_metrics["download"]
    assert metric_data.n == 1000
    assert metric_data.total == 1000
    assert metric_data.done is True

    # rows_skipped_on_error is seeded at 0 from tracker construction and
    # persisted alongside the job's other metrics.
    skipped = stored_metrics["rows_skipped_on_error"]
    assert skipped.n == 0
    assert skipped.total == 0
    assert skipped.done is False


@pytest.mark.asyncio
async def test_jobtracker_rehydrates_persisted_metrics(
    temp_db_path, db_connection
) -> None:
    job_id = str(uuid.uuid4())
    job_manager = JobStateManager(db_connection)
    job_manager.launch("test_table", "test_column", job_id=job_id)
    table_ref = TableReference(
        table_id=["test_table"], version=None, db_uri=str(temp_db_path)
    )

    first = _JobTracker(job_id=job_id, table_ref=table_ref)
    await first.set_total("processed", 10)
    await first.set_desc("processed", "Rows processed")
    await first.set("processed", 4)
    assert await first.flush() is True

    restarted = _JobTracker(job_id=job_id, table_ref=table_ref)
    metrics = await restarted.get_all()

    assert metrics["processed"] == {
        "n": 4,
        "total": 10,
        "done": False,
        "desc": "Rows processed",
    }


@pytest.mark.asyncio
async def test_rehydrated_metrics_survive_next_full_save(
    temp_db_path, db_connection
) -> None:
    job_id = str(uuid.uuid4())
    job_manager = JobStateManager(db_connection)
    job_manager.launch("test_table", "test_column", job_id=job_id)
    table_ref = TableReference(
        table_id=["test_table"], version=None, db_uri=str(temp_db_path)
    )

    first = _JobTracker(job_id=job_id, table_ref=table_ref)
    await first.set("before_restart", 7)
    assert await first.flush() is True

    restarted = _JobTracker(job_id=job_id, table_ref=table_ref)
    await restarted.set("after_restart", 3)
    assert await restarted.flush() is True

    stored = job_manager.get(job_id)[0]
    metrics = {metric.name: metric.n for metric in stored.metrics or []}
    assert metrics["before_restart"] == 7
    assert metrics["after_restart"] == 3


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (JobStatus.RUNNING, False),
        (JobStatus.DONE, True),
        (JobStatus.FAILED, True),
        (JobStatus.CANCELLED, True),
    ],
)
async def test_jobtracker_recovers_terminal_status(
    temp_db_path, db_connection, status: JobStatus, expected: bool
) -> None:
    job_id = str(uuid.uuid4())
    job_manager = JobStateManager(db_connection)
    job_manager.launch("test_table", "test_column", job_id=job_id)
    job_manager._set_status(job_id, status)
    table_ref = TableReference(
        table_id=["test_table"], version=None, db_uri=str(temp_db_path)
    )

    restarted = _JobTracker(job_id=job_id, table_ref=table_ref)

    assert await restarted.is_job_done() is expected


@pytest.mark.asyncio
async def test_rehydration_restores_rows_finalized(temp_db_path, db_connection) -> None:
    job_id = str(uuid.uuid4())
    job_manager = JobStateManager(db_connection)
    job_manager.launch("test_table", "test_column", job_id=job_id)
    table_ref = TableReference(
        table_id=["test_table"], version=None, db_uri=str(temp_db_path)
    )

    first = _JobTracker(job_id=job_id, table_ref=table_ref)
    await first.finalize_rows(11, 11, 11)

    restarted = _JobTracker(job_id=job_id, table_ref=table_ref)
    await restarted.increment("rows_committed", 5)
    metrics = await restarted.get_all()

    assert metrics["rows_checkpointed"]["n"] == 11
    assert metrics["rows_ready_for_commit"]["n"] == 11
    assert metrics["rows_committed"]["n"] == 11


@pytest.mark.asyncio
async def test_ray_actor_restart_rehydrates_metrics_and_status(
    temp_db_path, db_connection
) -> None:
    job_id = str(uuid.uuid4())
    job_manager = JobStateManager(db_connection)
    job_manager.launch("test_table", "test_column", job_id=job_id)
    table_ref = TableReference(
        table_id=["test_table"], version=None, db_uri=str(temp_db_path)
    )
    tracker = job_tracker_options(max_restarts=1, max_task_retries=0).remote(
        job_id, table_ref
    )
    actor_id = tracker._actor_id.hex()

    try:
        await tracker.set.remote("before_restart", 9)
        assert await tracker.flush.remote() is True
        job_manager._set_status(job_id, JobStatus.DONE)

        ray.kill(tracker, no_restart=False)

        for _ in range(100):
            state = get_actor(actor_id)
            if state is not None and state.num_restarts >= 1 and state.state == "ALIVE":
                break
            await asyncio.sleep(0.05)
        else:
            pytest.fail("JobTracker actor did not become available after restart")

        metrics = await tracker.get_all.remote()
        assert metrics["before_restart"]["n"] == 9
        assert await tracker.is_job_done.remote() is True
    finally:
        with contextlib.suppress(Exception):
            ray.kill(tracker, no_restart=True)


@pytest.mark.asyncio
async def test_is_job_done_refreshes_durable_status(
    temp_db_path, db_connection
) -> None:
    job_id = str(uuid.uuid4())
    job_manager = JobStateManager(db_connection)
    job_manager.launch("test_table", "test_column", job_id=job_id)
    table_ref = TableReference(
        table_id=["test_table"], version=None, db_uri=str(temp_db_path)
    )
    tracker = _JobTracker(job_id=job_id, table_ref=table_ref)

    assert await tracker.is_job_done() is False
    job_manager._set_status(job_id, JobStatus.FAILED)

    assert await tracker.is_job_done() is True


@pytest.mark.asyncio
async def test_rows_skipped_metric_seeded_at_zero_on_construction() -> None:
    """rows_skipped_on_error is materialized at 0 when a tracker is created."""
    table_ref = TableReference(
        table_id=["test_table"], version=None, db_uri="memory://"
    )
    tracker = _JobTracker(job_id="j", table_ref=table_ref, enable_saves=False)

    # Present at 0 immediately, before any row is processed.
    assert tracker.metrics["rows_skipped_on_error"] == {
        "n": 0,
        "total": 0,
        "done": False,
        "desc": "Rows skipped on error",
    }

    # Later skips accumulate on top of the seeded entry; a zero delta is a
    # no-op that leaves it at 0.
    await tracker.batch_increment({"rows_skipped_on_error": 0})
    assert tracker.metrics["rows_skipped_on_error"]["n"] == 0
    await tracker.batch_increment({"rows_skipped_on_error": 3})
    assert tracker.metrics["rows_skipped_on_error"]["n"] == 3


@pytest.mark.asyncio
async def test_save_metrics_infers_system_db_for_plain_table_reference(
    temp_db_path, db_connection
) -> None:
    """Plain table refs should write metrics to the inferred system DB."""
    job_id = str(uuid.uuid4())

    job_manager = JobStateManager(db_connection)
    job_record = job_manager.launch("test_table", "test_column")
    job_manager.get_table().update(
        where=f"job_id = '{job_record.job_id}'", values={"job_id": job_id}
    )

    table_ref = TableReference(
        table_id=["test_table"],
        version=None,
        db_uri=str(temp_db_path),
    )
    tracker = job_tracker_options().remote(job_id, table_ref)

    await tracker._save_metrics.remote(
        {"task1": {"n": 5, "total": 10, "done": False, "desc": "plain ref"}}
    )

    jobs = job_manager.get(job_id)
    assert len(jobs) == 1
    assert jobs[0].metrics == [
        JobMetric(name="task1", n=5, total=10, done=False, desc="plain ref")
    ]


def test_save_with_throttle_logic() -> None:
    """Test the throttling logic directly."""
    current_time = 0.0
    save_calls = []

    def mock_get_time() -> float:
        return current_time

    def mock_save(metrics) -> None:  # noqa: ARG001
        save_calls.append(current_time)

    # Simulate the throttle logic
    min_time_between_updates = 5.0
    last_updated = -float("inf")  # Initialize to allow first save

    def save_with_throttle(force: bool = False) -> None:
        nonlocal last_updated
        if not force and last_updated + min_time_between_updates > current_time:
            return
        last_updated = current_time
        mock_save({})

    # Test: First save at time 0
    current_time = 0.0
    save_with_throttle()
    assert len(save_calls) == 1

    # Test: Save at time 2 (within throttle) - should be blocked
    current_time = 2.0
    save_with_throttle()
    assert len(save_calls) == 1  # Still 1

    # Test: Save at time 6 (beyond throttle) - should save
    current_time = 6.0
    save_with_throttle()
    assert len(save_calls) == 2

    # Test: Force save at time 7 (within throttle) - should save anyway
    current_time = 7.0
    save_with_throttle(force=True)
    assert len(save_calls) == 3


def test_completion_forces_save_logic() -> None:
    """Test that completion forces save."""
    save_calls = []
    current_time = 0.0

    def mock_save(metrics) -> None:  # noqa: ARG001
        save_calls.append(current_time)

    min_time_between_updates = 100.0  # Very long throttle
    last_updated = -float("inf")

    def save_with_throttle(force: bool = False) -> None:
        nonlocal last_updated
        if not force and last_updated + min_time_between_updates > current_time:
            return
        last_updated = current_time
        mock_save({})

    # First save
    current_time = 0.0
    save_with_throttle()
    assert len(save_calls) == 1

    # Try to save within throttle window - should be blocked
    current_time = 1.0
    save_with_throttle(force=False)
    assert len(save_calls) == 1

    # Force save (like when completing) - should save
    save_with_throttle(force=True)
    assert len(save_calls) == 2


def test_set_and_increment_logic() -> None:
    """Test the set/increment logic for determining when to force save."""

    # Test increment that completes
    total = 100
    n = 90
    done = False
    if total and n >= total:
        done = True
    assert done is False

    # After increment
    n += 10
    if total and n >= total:
        done = True
    assert done is True

    # Test set that completes
    total = 100
    n = 0
    done = False
    n = 100
    if total and n >= total:
        done = True
    assert done is True

    # Test increment past total
    total = 100
    n = 0
    n += 150
    done = False
    if total and n >= total:
        done = True
    assert done is True


def test_zero_throttle() -> None:
    """Test that zero throttle allows all saves."""
    save_calls = []
    current_time = 0.0

    def mock_save(metrics) -> None:  # noqa: ARG001
        save_calls.append(current_time)

    min_time_between_updates = 0.0  # No throttling
    last_updated = -float("inf")

    def save_with_throttle(force: bool = False) -> None:
        nonlocal last_updated
        if not force and last_updated + min_time_between_updates > current_time:
            return
        last_updated = current_time
        mock_save({})

    # Multiple rapid saves - all should go through
    for i in range(5):
        current_time = i * 0.01
        save_with_throttle()

    assert len(save_calls) == 5


class _BlockingTracker(_JobTracker):
    """In-process JobTracker whose save blocks until ``release`` is set."""

    def _arm(self) -> None:
        self.calls: list[dict] = []
        self.save_started = asyncio.Event()
        self.release = asyncio.Event()
        self._hydrated = True

    async def _save_metrics(  # type: ignore[override]
        self, _metrics: dict[str, dict] | None = None
    ) -> None:
        metrics = self._snapshot_metrics() if _metrics is None else _metrics
        self.calls.append(dict(metrics))
        self.save_started.set()
        await self.release.wait()


class _FailingTracker(_JobTracker):
    """In-process JobTracker whose save always raises."""

    def _arm(self) -> None:
        self.attempts = 0
        self._hydrated = True

    async def _save_metrics(  # type: ignore[override]
        self, _metrics: dict[str, dict] | None = None
    ) -> None:
        self.attempts += 1
        raise RuntimeError("boom")


class _HydrationFailingTracker(_JobTracker):
    async def _load_persisted_state(self) -> tuple[dict[str, dict], Any | None]:
        self._db = cast("Any", object())
        self._jobs_table = cast("Any", object())
        raise RuntimeError("hydrate failed")


class _TransientHydrationTracker(_JobTracker):
    calls: int = 0

    async def _load_persisted_state(self) -> tuple[dict[str, dict], Any | None]:
        self.calls += 1
        if self.calls == 1:
            self._db = cast("Any", object())
            self._jobs_table = cast("Any", object())
            raise RuntimeError("transient hydrate failure")
        return {
            "persisted": {"n": 4, "total": 5, "done": False, "desc": "old"}
        }, JobStatus.RUNNING.value


class _BlockingHydrationTracker(_JobTracker):
    def _arm(self) -> None:
        self.load_started = asyncio.Event()
        self.release_load = asyncio.Event()

    async def _load_persisted_state(self) -> tuple[dict[str, dict], Any | None]:
        self.load_started.set()
        await self.release_load.wait()
        return {}, JobStatus.RUNNING.value


class _VersionSkewHydrationTracker(_JobTracker):
    async def _load_persisted_state(self) -> tuple[dict[str, dict], Any | None]:
        raise AttributeError("missing metrics column")


class _CapturingWriteTracker(_JobTracker):
    def _arm(self) -> None:
        self._hydrated = True
        self.writes: list[dict[str, dict]] = []

    async def _write_metrics(self, metrics: dict[str, dict]) -> None:
        self.writes.append({name: dict(metric) for name, metric in metrics.items()})


class _BlockingWriteTracker(_JobTracker):
    def _arm(self) -> None:
        self._hydrated = True
        self.write_started = asyncio.Event()
        self.release_write = asyncio.Event()
        self.writes: list[dict[str, dict]] = []

    async def _write_metrics(self, metrics: dict[str, dict]) -> None:
        self.writes.append({name: dict(metric) for name, metric in metrics.items()})
        if len(self.writes) == 1:
            self.write_started.set()
            await self.release_write.wait()


class _FakeJobsTable:
    uri = "memory://geneva_jobs"


class _BlockingJobsTableConnection:
    def __init__(self) -> None:
        self.open_calls = 0
        self.open_started = asyncio.Event()
        self.release_open = asyncio.Event()
        self.table = _FakeJobsTable()

    async def open_table(
        self, table_name: str, *, namespace_path: list[str]
    ) -> _FakeJobsTable:
        assert table_name == GENEVA_JOBS_TABLE_NAME
        assert namespace_path
        self.open_calls += 1
        self.open_started.set()
        await self.release_open.wait()
        return self.table


@pytest.mark.asyncio
async def test_jobs_table_initialization_is_single_flight(table_reference) -> None:
    tracker = _JobTracker(job_id="j", table_ref=table_reference)
    connection = _BlockingJobsTableConnection()
    tracker._db = cast("Any", connection)

    first = asyncio.create_task(tracker._get_jobs_table())
    await asyncio.wait_for(connection.open_started.wait(), timeout=2.0)
    second = asyncio.create_task(tracker._get_jobs_table())
    await asyncio.sleep(0)

    connection.release_open.set()
    first_table, second_table = await asyncio.wait_for(
        asyncio.gather(first, second), timeout=2.0
    )

    assert connection.open_calls == 1
    assert first_table is connection.table
    assert second_table is connection.table


@pytest.mark.asyncio
async def test_hydration_failure_never_saves_seed_only_snapshot(
    table_reference,
) -> None:
    tracker = _HydrationFailingTracker(job_id="j", table_ref=table_reference)

    with pytest.raises(RuntimeError, match="hydrate failed"):
        await tracker.set("new_metric", 1)

    assert tracker._hydrated is False
    assert tracker._save_task is None
    assert "new_metric" not in tracker.metrics
    assert tracker._db is None
    assert tracker._jobs_table is None


@pytest.mark.asyncio
async def test_hydration_retries_with_fresh_db_handles(table_reference) -> None:
    tracker = _TransientHydrationTracker(job_id="j", table_ref=table_reference)

    with pytest.raises(RuntimeError, match="transient hydrate failure"):
        await tracker.get_all()

    assert tracker._db is None
    assert tracker._jobs_table is None
    metrics = await tracker.get_all()
    assert metrics["persisted"]["n"] == 4
    assert tracker.calls == 2


@pytest.mark.asyncio
async def test_flush_timeout_includes_hydration(table_reference) -> None:
    tracker = _BlockingHydrationTracker(job_id="j", table_ref=table_reference)
    tracker._arm()
    start = asyncio.get_running_loop().time()

    assert await tracker.flush(timeout=0.05) is False

    assert asyncio.get_running_loop().time() - start < 0.5
    assert tracker.load_started.is_set()
    assert tracker._hydrated is False


@pytest.mark.asyncio
async def test_version_skew_disables_persistence_without_blocking_metrics(
    table_reference,
) -> None:
    tracker = _VersionSkewHydrationTracker(job_id="j", table_ref=table_reference)

    await tracker.set("new_metric", 3)

    assert tracker.enable_saves is False
    assert tracker.metrics["new_metric"]["n"] == 3
    assert tracker._save_task is None
    assert await tracker.flush() is True


@pytest.mark.asyncio
async def test_save_snapshot_is_taken_after_acquiring_lock(table_reference) -> None:
    tracker = _CapturingWriteTracker(job_id="j", table_ref=table_reference)
    tracker._arm()
    tracker.metrics["m"] = {"n": 1, "total": 10, "done": False, "desc": "m"}

    await tracker._save_lock.acquire()
    save_task = asyncio.create_task(tracker._save_metrics())
    await asyncio.sleep(0)
    tracker.metrics["m"]["n"] = 2
    tracker._save_lock.release()
    await save_task

    assert tracker.writes[-1]["m"]["n"] == 2


@pytest.mark.asyncio
async def test_flush_wins_over_in_flight_background_save(table_reference) -> None:
    tracker = _BlockingWriteTracker(job_id="j", table_ref=table_reference)
    tracker._arm()

    await tracker.set_total("m", 10)
    await asyncio.wait_for(tracker.write_started.wait(), timeout=2.0)
    await tracker.set("m", 10)
    flush_task = asyncio.create_task(tracker.flush(timeout=2.0))
    await asyncio.sleep(0)

    tracker.release_write.set()
    assert await flush_task is True

    assert tracker.writes[-1]["m"]["n"] == 10
    assert tracker._save_task is None
    assert tracker._save_pending is False


@pytest.mark.asyncio
async def test_forced_save_does_not_block_caller(table_reference) -> None:
    """A forced save runs in the background; the triggering call returns fast.

    Regression for the JobTracker wedge: previously the actor method awaited the
    DB write inline, so a hung save (e.g. cloud auth retry storm) blocked the
    single-concurrency actor mailbox forever.
    """
    tracker = _BlockingTracker(job_id="j", table_ref=table_reference)
    tracker._arm()

    await tracker.set_total("m", 1)
    # Reaching total forces a save. The save blocks in _save_metrics, but the
    # increment call itself must return promptly because the save is backgrounded.
    await asyncio.wait_for(tracker.increment("m", 1), timeout=2.0)

    await asyncio.wait_for(tracker.save_started.wait(), timeout=2.0)
    assert tracker._save_task is not None
    assert not tracker._save_task.done()

    # Other actor methods stay responsive while the save is still in flight.
    progress = await asyncio.wait_for(tracker.get_progress("m"), timeout=2.0)
    assert progress["n"] == 1
    await asyncio.wait_for(tracker.increment("other", 3), timeout=2.0)
    assert not tracker._save_task.done()

    # Release the save and let the background task finish.
    tracker.release.set()
    await asyncio.wait_for(tracker._save_task, timeout=2.0)
    # The save persisted the reached-total metric in the background.
    assert tracker.calls
    assert tracker.calls[-1]["m"]["n"] == 1


@pytest.mark.asyncio
async def test_saves_are_single_flight_and_coalesced(table_reference) -> None:
    """Saves queued while one is in flight collapse into a single follow-up."""
    tracker = _BlockingTracker(job_id="j", table_ref=table_reference)
    tracker._arm()

    await tracker.set_total("m", 10)
    await asyncio.wait_for(tracker.mark_done("m"), timeout=2.0)
    await asyncio.wait_for(tracker.save_started.wait(), timeout=2.0)
    in_flight = tracker._save_task

    # Many forced saves while the first is blocked: no new task, just dirty flag.
    await asyncio.wait_for(tracker.increment("m", 1), timeout=2.0)
    await asyncio.wait_for(tracker.mark_done("m"), timeout=2.0)
    assert tracker._save_task is in_flight
    assert tracker._save_pending is True

    tracker.release.set()
    await asyncio.wait_for(tracker._save_task, timeout=2.0)
    # Exactly one initial save + one coalesced follow-up, not one per call.
    assert len(tracker.calls) == 2


@pytest.mark.asyncio
async def test_failing_save_backs_off_without_blocking(table_reference) -> None:
    """Repeated save failures set bounded backoff instead of wedging the actor."""
    tracker = _FailingTracker(job_id="j", table_ref=table_reference)
    tracker._arm()

    await tracker.set_total("m", 1)
    # Triggering call still returns promptly even though the save fails.
    await asyncio.wait_for(tracker.increment("m", 1), timeout=2.0)

    for _ in range(200):
        if tracker._consecutive_save_failures >= 1:
            break
        await asyncio.sleep(0.01)

    assert tracker._consecutive_save_failures >= 1
    assert tracker._save_backoff_until > 0.0
    assert tracker.attempts >= 1

    # Stop the background retry loop (it would otherwise sleep through backoff).
    assert tracker._save_task is not None
    tracker._save_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await tracker._save_task


@pytest.mark.asyncio
async def test_flush_reports_failure(table_reference) -> None:
    """flush() returns False on a failing save instead of raising or hanging."""
    tracker = _FailingTracker(job_id="j", table_ref=table_reference)
    tracker._arm()
    await tracker.set_total("m", 5)

    assert await asyncio.wait_for(tracker.flush(timeout=1.0), timeout=2.0) is False
    assert tracker.attempts >= 1


def test_mark_done_always_forces() -> None:
    """Test that mark_done behavior always forces save."""
    # mark_done calls save_with_throttle(force=True)
    # So it should always save regardless of throttle

    save_calls = []
    current_time = 0.0

    def mock_save(metrics) -> None:  # noqa: ARG001
        save_calls.append(current_time)

    min_time_between_updates = 100.0
    last_updated = -float("inf")

    def save_with_throttle(force: bool = False) -> None:
        nonlocal last_updated
        if not force and last_updated + min_time_between_updates > current_time:
            return
        last_updated = current_time
        mock_save({})

    # Initial save
    current_time = 0.0
    save_with_throttle()
    assert len(save_calls) == 1

    # mark_done would call with force=True even within throttle window
    current_time = 1.0
    save_with_throttle(force=True)
    assert len(save_calls) == 2
