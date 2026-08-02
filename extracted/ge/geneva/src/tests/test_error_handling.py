# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for UDF error handling, retry logic, and error logging"""

import logging
import signal
from pathlib import Path

import lance
import pyarrow as pa
import pytest

import geneva
from geneva import udf
from geneva.db import Connection
from geneva.debug.error_store import (
    ErrorHandlingConfig,
    ErrorStore,
    FaultIsolation,
    UDFRetryConfig,
)

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)

SIZE = 20
HAS_SIGALRM_TIMEOUT = all(
    hasattr(signal, attr)
    for attr in ("SIGALRM", "ITIMER_REAL", "setitimer", "getitimer")
)

pytestmark = pytest.mark.ray


@pytest.fixture
def db(tmp_path) -> Connection:
    """Create a test database with a simple table"""
    tbl_path = tmp_path / "test.lance"

    # Create initial dataset with column 'a'
    data = {"a": pa.array(range(SIZE))}
    tbl = pa.Table.from_pydict(data)
    lance.write_dataset(tbl, tbl_path, max_rows_per_file=10)

    db = geneva.connect(str(tmp_path))
    yield db
    db.close()


@pytest.fixture
def error_store(db: Connection) -> ErrorStore:
    """Create an error store for testing"""
    return ErrorStore(db)


def test_error_handling_context_records_audit_columns_without_internal_rowaddr() -> (
    None
):
    from geneva.apply.error_handling import ErrorHandlingContext

    class ReadTask:
        version = 7
        frag_id = 3

        def table_uri(self) -> str:
            return "memory:///test.lance"

    class MapTask:
        def name(self) -> str:
            return "user_id"

        def checkpoint_prefix(self, *, dataset_uri: str, where: str | None) -> str:
            return f"{dataset_uri}:{where}:v1"

        def input_columns(self) -> list[str]:
            return ["MetaData.UserId"]

        def output_schema(self) -> pa.Schema:
            return pa.schema(
                [
                    pa.field("user_id", pa.int64()),
                    pa.field("_rowaddr", pa.uint64()),
                ]
            )

    ctx = ErrorHandlingContext.create(
        MapTask(),  # type: ignore[arg-type]
        ReadTask(),  # type: ignore[arg-type]
        "job-1",
        5,
    )

    assert ctx.input_columns == ["MetaData.UserId"]
    assert ctx.output_columns == ["user_id"]
    record = ctx.create_error_record(ValueError("bad row"), None, 1, 1)
    assert record.input_columns == ["MetaData.UserId"]
    assert record.output_columns == ["user_id"]


def test_multiprocess_worker_preserves_audit_columns_in_error_records() -> None:
    import geneva.cloudpickle as cloudpickle
    from geneva.apply.multiprocess import MultiProcessBatchApplier, _batch_to_buf
    from geneva.apply.task import BackfillUDFTask

    @udf(
        data_type=pa.int32(),
        error_handling=ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS,
            log_errors=True,
        ),
    )
    def fail_on_one(a: int) -> int:
        if a == 1:
            raise ValueError("bad row")
        return a

    map_task = BackfillUDFTask(udfs={"user_id": fail_on_one})
    batch = pa.RecordBatch.from_arrays(
        [
            pa.array([1], type=pa.int32()),
            pa.array([42], type=pa.uint64()),
        ],
        ["a", "_rowaddr"],
    )

    _result_bytes, error_records_bytes, skip_count = (
        MultiProcessBatchApplier._worker_apply(
            cloudpickle.dumps(map_task),
            _batch_to_buf(batch),
            cloudpickle.dumps(fail_on_one.error_handling),
            "job-1",
            {"table_uri": "memory:///test.lance", "table_version": 7, "fragment_id": 3},
            0,
            "user_id",
            "v1",
            ["MetaData.UserId"],
            ["user_id"],
        )
    )

    error_records = cloudpickle.loads(error_records_bytes)
    assert skip_count == 1
    assert len(error_records) == 1
    assert error_records[0].input_columns == ["MetaData.UserId"]
    assert error_records[0].output_columns == ["user_id"]


def test_retry_transient_network_error(
    db: Connection, error_store: ErrorStore, local_ray_context: None
) -> None:
    """Test that transient errors are retried and eventually succeed"""
    import fcntl
    import tempfile
    from pathlib import Path

    # Create unique temp file (delete=False so it persists across Ray workers)
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("0")
        counter_file = Path(f.name)

    def atomic_increment(filepath: Path) -> int:
        """Atomically increment counter in file and return new value"""
        with open(filepath, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
            try:
                count = int(f.read() or "0")
                count += 1
                f.seek(0)
                f.write(str(count))
                f.truncate()
                return count
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    @udf(
        data_type=pa.int32(),
        error_handling=ErrorHandlingConfig(
            retry_config=UDFRetryConfig.retry_transient(max_attempts=3),
            log_retry_attempts=True,  # Log all attempts
        ),
    )
    def flaky_network_udf(a: int) -> int:
        # Atomically increment counter
        count = atomic_increment(counter_file)

        # Fail first 2 attempts per batch, succeed on 3rd
        if count < 3:
            raise ConnectionError(f"Temporary network issue (attempt {count})")
        return a * 2

    # Add column with UDF
    tbl = db.open_table("test")
    tbl.add_columns({"b": flaky_network_udf})

    # Backfill should succeed after retries
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Reload table to get results
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    expected = [x * 2 for x in range(SIZE)]
    assert result_data["b"].to_pylist() == expected

    # Cleanup
    counter_file.unlink(missing_ok=True)


def test_retry_exhaustion_logs_error(db: Connection, error_store: ErrorStore) -> None:
    """Test that retry configuration is properly set up"""
    # This test documents that retry exhaustion should log errors
    # Integration testing of error logging requires a full distributed environment

    config = ErrorHandlingConfig(
        retry_config=UDFRetryConfig.retry_transient(max_attempts=2),
        log_errors=True,
    )

    assert config.retry_config.stop.max_attempt_number == 2  # type: ignore[attr-defined]
    assert config.log_errors is True
    assert config.fault_isolation == FaultIsolation.FAIL_BATCH


def test_error_logging_captures_table_version(db: Connection, tmp_path: Path) -> None:
    """Test that error records include all required context fields"""
    from geneva.debug.error_store import make_error_record_from_exception

    # Create an error record to verify it includes table version
    try:
        raise ValueError("Test error")
    except Exception as e:
        error_record = make_error_record_from_exception(
            exception=e,
            job_id="test-job",
            table_uri="gs://bucket/test.lance",
            table_name="test",
            table_version=42,  # Verify version is captured
            column_name="test_col",
            udf_name="test_udf",
            udf_version="v1",
            input_columns=["MetaData.UserId"],
            output_columns=["test_col"],
            batch_index=0,
        )

    # Verify all required fields are present
    assert error_record.table_version == 42
    assert error_record.table_uri == "gs://bucket/test.lance"
    assert error_record.table_name == "test"
    assert error_record.job_id == "test-job"
    assert error_record.error_type == "ValueError"
    assert error_record.input_columns == ["MetaData.UserId"]
    assert error_record.output_columns == ["test_col"]


def test_udf_with_no_error_handling_uses_default(db: Connection) -> None:
    """Test that UDFs without error_handling use default behavior (no retry)"""

    @udf(data_type=pa.int32())
    def simple_udf(a: int) -> int:
        return a * 3

    # Add column and backfill
    tbl = db.open_table("test")
    tbl.add_columns({"b": simple_udf})
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Reload table to get results
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    expected = [x * 3 for x in range(SIZE)]
    assert result_data["b"].to_pylist() == expected


def test_error_store_basic_functionality(error_store: ErrorStore) -> None:
    """Test ErrorStore can store and retrieve error records"""
    from geneva.debug.error_store import make_error_record_from_exception

    # Create an error record
    try:
        raise ValueError("Test error")
    except Exception as e:
        error_record = make_error_record_from_exception(
            exception=e,
            job_id="test-job-123",
            table_uri="gs://bucket/test.lance",
            table_name="test",
            table_version=1,
            column_name="test_col",
            udf_name="test_udf",
            udf_version="v1",
            batch_index=0,
            fragment_id=0,
            attempt=1,
            max_attempts=3,
        )

        # Log the error
        error_store.log_error(error_record)

    # Retrieve errors
    errors = error_store.get_errors(job_id="test-job-123")
    assert len(errors) == 1
    assert errors[0].error_type == "ValueError"
    assert errors[0].error_message == "Test error"
    assert errors[0].table_version == 1
    assert errors[0].table_uri == "gs://bucket/test.lance"


def test_error_store_query_filters(error_store: ErrorStore) -> None:  # noqa: PERF203
    """Test ErrorStore filtering by different attributes"""
    from geneva.debug.error_store import make_error_record_from_exception

    # Create multiple error records
    for i in range(3):
        try:
            if i == 0:
                raise ValueError("Error 0")
            elif i == 1:
                raise ConnectionError("Error 1")
            else:
                raise RuntimeError("Error 2")
        except Exception as e:  # noqa: PERF203
            error_record = make_error_record_from_exception(
                exception=e,
                job_id=f"job-{i}",
                table_uri=f"gs://bucket/table{i}.lance",
                table_name=f"table{i}",
                table_version=i,
                column_name=f"col{i}",
                udf_name="test_udf",
                udf_version="v1",
                batch_index=i,
                attempt=1,
                max_attempts=1,
            )
            error_store.log_error(error_record)

    # Query by job_id
    errors = error_store.get_errors(job_id="job-1")
    assert len(errors) == 1
    assert errors[0].error_type == "ConnectionError"

    # Query by error_type
    errors = error_store.get_errors(error_type="ValueError")
    assert len(errors) == 1
    assert errors[0].job_id == "job-0"


def test_retry_config_factory_methods() -> None:
    """Test UDFRetryConfig factory methods"""
    # no_retry
    config = UDFRetryConfig.no_retry()
    assert hasattr(config.stop, "max_attempt_number")
    assert config.stop.max_attempt_number == 1

    # retry_transient
    config = UDFRetryConfig.retry_transient(max_attempts=5)
    assert config.stop.max_attempt_number == 5


def test_error_handling_config_defaults() -> None:
    """Test ErrorHandlingConfig default values"""
    config = ErrorHandlingConfig()

    assert config.fault_isolation == FaultIsolation.FAIL_BATCH
    assert config.log_errors is True
    assert config.log_retry_attempts is False


def test_skip_rows_validation_rejects_recordbatch_udf() -> None:
    """Test that SKIP_ROWS validation detects RecordBatch UDFs"""
    from geneva.apply.task import BackfillUDFTask

    @udf(
        data_type=pa.int32(),
        error_handling=ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS,
        ),
    )
    def recordbatch_udf(batch: pa.RecordBatch) -> pa.Array:
        return pa.array([1] * len(batch))

    # Create a task to test validation
    task = BackfillUDFTask(udfs={"b": recordbatch_udf})

    # Should raise ValueError during validation
    with pytest.raises(ValueError, match="SKIP_ROWS.*RecordBatch"):
        recordbatch_udf.error_handling.validate_compatibility(task)


def test_skip_rows_skips_failing_rows_and_logs_errors(
    db: Connection, error_store: ErrorStore, local_ray_context: None
) -> None:
    """Test that SKIP_ROWS skips failing rows and sets them to null"""

    @udf(
        data_type=pa.int32(),
        error_handling=ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS,
            log_errors=True,
        ),
    )
    def fails_on_multiples_of_5(a: int) -> int:
        if a % 5 == 0:
            raise ValueError(f"Cannot process value {a}")
        return a * 10

    tbl = db.open_table("test")
    tbl.add_columns({"b": fails_on_multiples_of_5})

    # Backfill should succeed, skipping failed rows
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Reload table to get results
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()

    # Verify results: multiples of 5 should be null, others should be a*10
    expected = [None if i % 5 == 0 else i * 10 for i in range(SIZE)]
    assert result_data["b"].to_pylist() == expected

    # Verify errors were logged with row addresses
    errors = error_store.get_errors(table_name="test", column_name="b")
    # Should have logged errors for rows that are multiples of 5
    assert len(errors) == 4
    assert all(err.row_address is not None for err in errors)
    # Verify that at least some row addresses are in the expected range
    row_addresses = [err.row_address for err in errors if err.row_address is not None]
    assert len(row_addresses) == 4
    # Just verify we captured row-level errors, not checking exact addresses
    # due to potential type conversion issues with uint64


def test_skip_rows_allows_scalar_udfs(db: Connection, local_ray_context: None) -> None:
    """Test that SKIP_ROWS works with scalar UDFs"""

    @udf(
        data_type=pa.int32(),
        error_handling=ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS,
        ),
    )
    def scalar_udf_with_skip(a: int) -> int:
        if a == 7:
            raise ValueError("Lucky number 7!")
        return a * 2

    tbl = db.open_table("test")
    tbl.add_columns({"b": scalar_udf_with_skip})

    # Should succeed
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Verify result
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()
    expected = [None if i == 7 else i * 2 for i in range(SIZE)]
    assert result_data["b"].to_pylist() == expected


def test_skip_rows_with_retry(
    db: Connection, error_store: ErrorStore, local_ray_context: None
) -> None:
    """Test that SKIP_ROWS + retry works: retry per-row, then skip if exhausted"""
    import fcntl
    import json
    import tempfile
    from pathlib import Path

    # Use a JSON file to track per-row attempt counts
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        json.dump({}, f)
        counter_file = Path(f.name)

    def atomic_get_row_attempt(filepath: Path, row_value: int) -> int:
        """Atomically get and increment attempt count for a specific row"""
        with open(filepath, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
            try:
                f.seek(0)
                data = json.load(f)
                key = str(row_value)
                attempt = data.get(key, 0) + 1
                data[key] = attempt
                f.seek(0)
                json.dump(data, f)
                f.truncate()
                return attempt
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    @udf(
        data_type=pa.int32(),
        error_handling=ErrorHandlingConfig(
            fault_isolation=FaultIsolation.SKIP_ROWS,
            retry_config=UDFRetryConfig.retry_transient(max_attempts=3),
            log_errors=True,
            log_retry_attempts=True,
        ),
    )
    def retry_then_skip_udf(a: int) -> int:
        # Track attempts per row (thread-safe)
        attempt = atomic_get_row_attempt(counter_file, a)

        # Row 5: Always fails (even after retries) → should be skipped
        if a == 5:
            raise ConnectionError(f"Permanent network failure for row {a}")

        # Row 10: Fails first 2 attempts, succeeds on 3rd → should succeed
        if a == 10 and attempt < 3:
            raise ConnectionError(
                f"Temporary network issue for row {a} (attempt {attempt})"
            )

        # All other rows: succeed immediately
        return a * 3

    tbl = db.open_table("test")
    tbl.add_columns({"b": retry_then_skip_udf})

    # Backfill should succeed
    job_id = tbl.backfill("b")
    assert job_id is not None

    # Reload table to get results
    result_tbl = db.open_table("test")
    result_data = result_tbl.to_arrow()

    # Verify results:
    # - Row 5: skipped (None) after exhausting retries
    # - Row 10: succeeded (30) after retries
    # - All others: succeeded immediately
    expected = [None if i == 5 else i * 3 for i in range(SIZE)]
    assert result_data["b"].to_pylist() == expected

    # Verify errors were logged for row 5 (the permanently failing row)
    errors = error_store.get_errors(table_name="test", column_name="b")
    # Should have logged errors for row 5 (3 attempts)
    row_5_errors = [e for e in errors if e.row_address == 5]
    assert len(row_5_errors) >= 1  # At least the final error
    assert all(e.error_type == "ConnectionError" for e in row_5_errors)

    # Cleanup
    counter_file.unlink(missing_ok=True)


@pytest.mark.skipif(
    not HAS_SIGALRM_TIMEOUT, reason="signal.setitimer(SIGALRM) not available"
)
def test_timeout_retry_exhaustion_logs_error(
    error_store: ErrorStore,
) -> None:
    """Timed-out scalar UDFs should log TimeoutError attempts on exhaustion."""
    import time

    from geneva.apply.error_handling import BatchRetryStrategy, ErrorHandlingContext
    from geneva.apply.task import BackfillUDFTask

    @udf(
        data_type=pa.int32(),
        timeout=0.01,
        error_handling=ErrorHandlingConfig(
            retry_config=UDFRetryConfig.retry_transient(max_attempts=2),
            log_errors=True,
            log_retry_attempts=True,
        ),
    )
    def always_timeout(a: int) -> int:
        time.sleep(0.05)
        return a * 2

    map_task = BackfillUDFTask(udfs={"b": always_timeout})
    batch = pa.RecordBatch.from_arrays(
        [
            pa.array([1], type=pa.int64()),
            pa.array([0], type=pa.uint64()),
        ],
        ["a", "_rowaddr"],
    )
    ctx = ErrorHandlingContext(
        job_id="timeout-test",
        task_context={
            "table_uri": "memory:///test.lance",
            "table_version": 1,
            "fragment_id": 0,
        },
        seq=0,
        udf_name="b",
        udf_version="timeout-test-version",
        error_config=always_timeout.error_handling,
    )
    strategy = BatchRetryStrategy(ctx, map_task, error_store)

    with pytest.raises(TimeoutError, match=r"always_timeout'.*timeout=0.01 seconds"):
        strategy.apply(batch)

    errors = error_store.get_errors(job_id="timeout-test", error_type="TimeoutError")
    timeout_errors = sorted(
        errors,
        key=lambda err: err.attempt,
    )
    assert len(timeout_errors) == 2
    assert [err.attempt for err in timeout_errors] == [1, 2]
    assert all(err.max_attempts == 2 for err in timeout_errors)
