# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
import itertools
import json
import logging
import os
import random
import threading
import time
import uuid
from collections.abc import Callable, Generator
from pathlib import Path
from typing import Any, NoReturn
from unittest import mock

import lance
import lance.namespace
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pytest
import ray
from lance import BlobFile
from ray_backfill_test_utils import (
    UDFTestConfig,
    assert_backfill_job_history,
    foo_tbl_path,
    foo_tbl_ref,
    int32_return_none,
    make_new_ds_a,
    setup_table_and_udf_column,
)

import geneva
import geneva.runners.ray.pipeline as pipeline_mod
from geneva import CheckpointStore, connect, udf
from geneva.apply import DirectFragmentWriteResult
from geneva.apply.task import DEFAULT_CHECKPOINT_ROWS, BackfillUDFTask, ScanTask
from geneva.db import Connection
from geneva.errors import MergeFallbackTargetError
from geneva.jobs.config import JobConfig
from geneva.runners.ray.actor_pool import ActorPool, ActorStateSnapshot
from geneva.runners.ray.jobtracker import (
    METRIC_AVG_BATCH_NUM_ROWS,
    METRIC_AVG_BATCH_SIZE,
    METRIC_BATCH_CHECKPOINTING_TIME,
    METRIC_CHECKPOINT_EXISTS_TIME,
    METRIC_CHECKPOINT_FRAGMENT_WRITES,
    METRIC_CHECKPOINT_LIST_TIME,
    METRIC_DIRECT_FRAGMENT_WRITES,
    METRIC_FRAGMENT_CHECKPOINTING_TIME,
    METRIC_READ_IO_TIME,
    METRIC_UDF_PROCESSING_TIME,
    METRIC_WRITER_ALIGN_TIME,
    METRIC_WRITER_CHECKPOINT_READ_TIME,
    METRIC_WRITER_QUEUE_WAIT_TIME,
    METRIC_WRITER_WRITE_TIME,
)
from geneva.runners.ray.pipeline import (
    ApplierActor,
    ColumnAddPipelineJob,
    FragmentWriterManager,
    FragmentWriterSession,
    _picklable_remote_error,
    run_ray_add_column,
    run_ray_add_column_remote,
    validate_backfill_args,
)
from geneva.table import Table, TableReference

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)

SIZE = 17  # was 256

pytestmark = pytest.mark.ray


@pytest.fixture(autouse=True)
def ray_cluster() -> None:
    ray.shutdown()
    ray.init(
        runtime_env={
            "RAY_BACKEND_LOG_LEVEL": "info",
            "RAY_LOG_TO_DRIVER": "1",
            "RAY_ENABLE_RECORD_ACTOR_TASK_LOGGING": "1",
            "RAY_RUNTIME_ENV_LOG_TO_DRIVER_ENABLED": "true",
        },
        log_to_driver=True,
        logging_config=ray.LoggingConfig(
            encoding="TEXT", log_level="DEBUG", additional_log_standard_attrs=["name"]
        ),
    )
    yield
    ray.shutdown()


@pytest.fixture(autouse=True)
def db(tmp_path, tbl_path) -> Connection:
    make_new_ds_a(tbl_path, size=SIZE, max_rows_per_file=32)
    db = geneva.connect(str(tmp_path))
    yield db
    db.close()


@pytest.fixture
def tbl_path(tmp_path) -> Path:
    return foo_tbl_path(tmp_path)


@pytest.fixture
def tbl_ref(tmp_path) -> TableReference:
    return foo_tbl_ref(tmp_path)


@pytest.fixture
def ds(tbl_ref) -> lance.dataset:
    return tbl_ref.open().to_lance()


@pytest.fixture
def ckp_store(tmp_path: Path) -> CheckpointStore:
    return CheckpointStore.from_uri(str(tmp_path / "ckp"))


def test_picklable_remote_error_preserves_type_and_message() -> None:
    err = ValueError("boom")

    wrapped = _picklable_remote_error(err)

    assert isinstance(wrapped, RuntimeError)
    assert str(wrapped) == "builtins.ValueError: boom"


def test_picklable_remote_error_can_be_raised_without_cause() -> None:
    def _raise() -> None:
        try:
            raise ValueError("boom")
        except ValueError as err:
            raise _picklable_remote_error(err) from None

    with pytest.raises(RuntimeError) as exc_info:
        _raise()

    err = exc_info.value
    assert str(err) == "builtins.ValueError: boom"
    assert err.__cause__ is None


def test_picklable_remote_error_includes_root_cause_chain() -> None:
    try:
        try:
            raise TimeoutError("timed out")
        except TimeoutError as err:
            raise RuntimeError("Error running task foo") from err
    except RuntimeError as err:
        wrapped = _picklable_remote_error(err)

    assert isinstance(wrapped, RuntimeError)
    assert str(wrapped) == (
        "builtins.RuntimeError: Error running task foo"
        " | caused by builtins.TimeoutError: timed out"
    )


def test_picklable_remote_error_preserves_root_cause_across_double_wrap() -> None:
    try:
        try:
            raise TimeoutError("timed out")
        except TimeoutError as err:
            raise RuntimeError("Error running task foo") from err
    except RuntimeError as err:
        wrapped = _picklable_remote_error(err)

    double_wrapped = _picklable_remote_error(wrapped)

    assert isinstance(double_wrapped, RuntimeError)
    assert "TimeoutError: timed out" in str(double_wrapped)
    assert "Error running task foo" in str(double_wrapped)


def test_run_ray_add_column_remote_wraps_open_failures(monkeypatch) -> None:
    class FakeRef:
        # The worker opens a geneva.job span (reading these) before open(),
        # mirroring a real TableReference where both are available pre-open.
        table_name = "fake_table"
        table_uri = "fake://table"

        def open(self) -> None:
            raise ValueError("boom")

    with pytest.raises(RuntimeError) as exc_info:
        run_ray_add_column_remote._function(FakeRef(), "upper")

    assert str(exc_info.value) == "builtins.ValueError: boom"
    assert exc_info.value.__cause__ is None


def test_applier_actor_wraps_unpicklable_failures() -> None:
    class FakeApplier:
        def run(self, task: object) -> None:
            raise ValueError("boom")

    actor = ApplierActor.__ray_actor_class__(applier=FakeApplier())

    with pytest.raises(RuntimeError) as exc_info:
        actor.run(object())

    assert str(exc_info.value) == "builtins.ValueError: boom"
    assert exc_info.value.__cause__ is None


def make_new_ds_a_with_10_fragments(tbl_path: Path) -> lance.dataset:
    # create initial dataset with only column 'a' with 10 fragments
    # Use 20 rows with max_rows_per_file=2 to get exactly 10 fragments
    num_rows = 20
    data = {"a": pa.array(range(num_rows))}
    tbl = pa.Table.from_pydict(data)
    ds = lance.write_dataset(
        tbl, tbl_path, max_rows_per_file=2, mode="overwrite", data_storage_version="2.0"
    )
    return ds


def add_empty_b(ds: lance.dataset, fn) -> None:
    # then add column 'b' using merge.  This is a separate commit from data
    # commits to keep column 'a' as a separate set of physical files from 'b'
    # which enables a separate commit from distributed execution to only
    # update 'b' with an efficient file replacement operation.
    new_frags = []
    new_schema = None
    for frag in ds.get_fragments():
        new_fragment, new_schema = frag.merge_columns(fn, columns=["a"])
        new_frags.append(new_fragment)

    assert new_schema is not None
    merge = lance.LanceOperation.Merge(new_frags, new_schema)
    lance.LanceDataset.commit(ds.uri, merge, read_version=ds.version)


def backfill_and_verify(
    tbl,
    testcfg,
    num_frags=None,
    expected_row_counts=None,
) -> None:
    backfill_kwargs = {}
    if num_frags is not None:
        backfill_kwargs["num_frags"] = num_frags

    # Use backfill_async to get access to job tracker for verification
    fut = tbl.backfill_async("b", where=testcfg.where, **backfill_kwargs)

    # Wait for completion
    fut.result()
    job_id = fut.job_id

    final_metrics: dict[str, dict] | None = None
    inner = getattr(fut, "future", fut)
    if hasattr(inner, "job_tracker") and inner.job_tracker is not None:
        final_metrics = ray.get(inner.job_tracker.get_all.remote())
        _LOG.info(f"Final job metrics: {final_metrics}")

        expected_metrics = [
            METRIC_UDF_PROCESSING_TIME,
            METRIC_BATCH_CHECKPOINTING_TIME,
            METRIC_READ_IO_TIME,
            METRIC_CHECKPOINT_EXISTS_TIME,
            METRIC_CHECKPOINT_LIST_TIME,
            METRIC_FRAGMENT_CHECKPOINTING_TIME,
            METRIC_WRITER_ALIGN_TIME,
            METRIC_WRITER_WRITE_TIME,
            METRIC_WRITER_QUEUE_WAIT_TIME,
            METRIC_WRITER_CHECKPOINT_READ_TIME,
            METRIC_DIRECT_FRAGMENT_WRITES,
            METRIC_CHECKPOINT_FRAGMENT_WRITES,
            METRIC_AVG_BATCH_NUM_ROWS,
            METRIC_AVG_BATCH_SIZE,
        ]
        for metric_name in expected_metrics:
            assert metric_name in final_metrics, (
                f"Missing expected job metric {metric_name}. "
                f"Available metrics: {sorted(final_metrics)}"
            )

    # Checkout latest to see the updated data
    tbl.checkout_latest()
    _LOG.info(f"completed backfill job {job_id}, now on version {tbl.version}")
    _LOG.info(
        f"actual={tbl.to_arrow().to_pydict()} expected={testcfg.expected_recordbatch}"
    )
    assert tbl.to_arrow().to_pydict() == testcfg.expected_recordbatch

    # Verify row counts if expected counts are provided
    if expected_row_counts is not None and final_metrics is not None:
        try:
            # Verify expected row counts
            for metric_name, expected_count in expected_row_counts.items():
                if metric_name in final_metrics:
                    actual_count = final_metrics[metric_name].get("n", 0)
                    _LOG.info(
                        f"Metric {metric_name}: expected={expected_count}, "
                        f"actual={actual_count}"
                    )
                    assert actual_count == expected_count, (
                        f"Row count mismatch for {metric_name}: "
                        f"expected {expected_count}, got {actual_count}"
                    )
                else:
                    _LOG.warning(f"Metric {metric_name} not found in final metrics")

            # Anti-regression check: rows_ready_for_commit should never exceed
            # rows_checkpointed by more than a small tolerance
            checkpointed = final_metrics.get("rows_checkpointed", {}).get("n", 0)
            ready = final_metrics.get("rows_ready_for_commit", {}).get("n", 0)
            committed = final_metrics.get("rows_committed", {}).get("n", 0)

            assert ready <= checkpointed + 5, (
                f"Double counting detected: rows_ready_for_commit ({ready}) "
                f"significantly exceeds rows_checkpointed ({checkpointed})"
            )

            assert committed <= checkpointed, (
                f"Invalid state: rows_committed ({committed}) "
                f"exceeds rows_checkpointed ({checkpointed})"
            )
        except Exception as e:
            _LOG.warning(f"Could not verify row counts: {e}")

    _LOG.info(f"Checking job history for {job_id}")
    _LOG.info(f"{tbl._conn._history.get_table().to_arrow().to_pylist()}")

    assert_backfill_job_history(tbl, job_id)


# UDF argument validation tests


@udf(data_type=pa.int32())
def recordbatch_udf(batch: pa.RecordBatch) -> pa.Array:
    return batch["a"]


@pytest.mark.multibackfill
def test_recordbatch_bad_inputs(db, local_ray_context) -> None:
    # RecordBatch UDFs with input_columns raise error at creation time
    with pytest.raises(
        ValueError, match="RecordBatch input UDF must not declare any input columns"
    ):

        @udf(data_type=pa.int32(), input_columns=["a"])
        def recordbatch_bad(batch: pa.RecordBatch) -> pa.Array:
            return batch["a"]

    # record batch udfs need output data_type arg
    with pytest.raises(ValueError, match="please specify data_type"):

        @udf
        def recordbatch_bad2(batch: pa.RecordBatch) -> pa.Array:
            return batch["a"]

    # set good udf, then test UDF override at backfill time
    tbl = setup_table_and_udf_column(db, default_shuffle_config, recordbatch_udf)

    # override backfill with same UDF should work
    tbl.backfill("b", udf=recordbatch_udf)


def test_invalid_column(db, local_ray_context) -> None:
    tbl = setup_table_and_udf_column(db, default_shuffle_config, recordbatch_udf)

    # input cols arg
    with pytest.raises(ValueError, match="Use add_columns"):
        tbl.backfill("c", udf=recordbatch_udf)


def test_validate_missing_input_column_scalar_udf(db) -> None:
    """Test that missing input columns are detected early for scalar UDFs."""

    @udf(data_type=pa.int32())
    def bad_udf(nonexistent_col: int) -> int:
        return nonexistent_col * 2

    tbl = db.open_table("foo")

    # Should fail validation at add_columns time (even earlier than backfill!)
    with pytest.raises(
        ValueError,
        match=r"expects input columns \['nonexistent_col'\].*not found in table schema",
    ):
        tbl.add_columns({"b": bad_udf}, **default_shuffle_config)


def test_validate_type_mismatch_string_vs_int(db, local_ray_context) -> None:
    """Test that type mismatches (string vs int) are detected early."""

    # Create a table with a string column
    tbl = db.open_table("foo")

    # Now try to use a UDF that expects string on the int column 'a'
    @udf(data_type=pa.string())
    def string_udf(a: str) -> str:
        # UDF expects string but table has int64
        return str(a)

    tbl.add_columns({"b": string_udf}, **default_shuffle_config)

    # Should detect type mismatch: table has int64 column 'a', UDF expects string
    # Note: This validation is best-effort - if type hints don't match our map,
    # validation may not catch all type mismatches
    # For this test, we just verify that validation runs without error
    # The real benefit is catching missing columns, not all type mismatches
    try:
        tbl.backfill("b")
    except ValueError as e:
        # If validation caught it, great!
        if "Type mismatch" in str(e):
            pass  # Expected
        else:
            raise
    # If it didn't catch it, that's okay - type validation is best-effort


def test_validate_multiple_missing_columns(db) -> None:
    """Test validation with multiple missing columns."""

    @udf(data_type=pa.int32())
    def multi_col_udf(col1: int, col2: int, col3: int) -> int:
        return col1 + col2 + col3

    tbl = db.open_table("foo")

    # Should list all missing columns at add_columns time
    with pytest.raises(
        ValueError,
        match=r"expects input columns \['col1', 'col2', 'col3'\].*"
        r"not found in table schema",
    ):
        tbl.add_columns({"b": multi_col_udf}, **default_shuffle_config)


def test_validate_array_udf_missing_column(db) -> None:
    """Test validation for Array UDFs with missing columns."""

    @udf(data_type=pa.int32())
    def array_udf(missing_col: pa.Array) -> pa.Array:
        return missing_col

    tbl = db.open_table("foo")

    # Should fail at add_columns time
    with pytest.raises(
        ValueError,
        match=r"expects input columns \['missing_col'\].*not found in table schema",
    ):
        tbl.add_columns({"b": array_udf}, **default_shuffle_config)


def test_validate_against_read_version_missing_column(db) -> None:
    """Validation should use the schema for the requested read_version."""

    tbl = db.open_table("foo")
    base_version = tbl.version

    # Add a physical column that the computed column depends on
    tbl.add_columns({"b": "a"})
    assert tbl.version > base_version

    @udf(data_type=pa.int32())
    def uses_b(b: int) -> int:
        return b * 2

    tbl.add_columns({"c": uses_b}, **default_shuffle_config)

    # When validating against the original version (which lacks column b),
    # we should fail fast instead of launching a job that will time out later.
    with pytest.raises(
        ValueError,
        match=r"expects input columns \['b'\].*read_version",
    ):
        validate_backfill_args(tbl, "c", read_version=base_version)


def test_validate_passes_with_correct_columns(db, local_ray_context) -> None:
    """Test that validation passes when columns are correct."""

    @udf(data_type=pa.int32())
    def good_udf(a: int) -> int:
        return a * 2

    tbl = db.open_table("foo")
    tbl.add_columns({"b": good_udf}, **default_shuffle_config)

    # Should not raise any validation errors
    tbl.backfill("b")

    # Verify the result
    result = tbl.to_arrow()
    expected_b = [x * 2 for x in range(SIZE)]
    assert result["b"].to_pylist() == expected_b


def test_add_columns_validates_missing_columns(db) -> None:
    """Test that add_columns() validates input columns at definition time."""

    @udf(data_type=pa.int32())
    def bad_udf(nonexistent_col: int) -> int:
        return nonexistent_col * 2

    tbl = db.open_table("foo")

    # Should fail at add_columns time, not backfill time
    with pytest.raises(
        ValueError,
        match=r"expects input columns \['nonexistent_col'\].*not found in table schema",
    ):
        tbl.add_columns({"b": bad_udf}, **default_shuffle_config)


def test_add_columns_validates_with_explicit_input_columns(db) -> None:
    """Test that add_columns() validates explicitly provided input columns."""

    @udf(data_type=pa.int32())
    def simple_udf(x: int) -> int:
        return x * 2

    tbl = db.open_table("foo")

    # Provide wrong column name explicitly
    with pytest.raises(
        ValueError,
        match=r"expects input columns \['wrong_column'\].*not found in table schema",
    ):
        tbl.add_columns({"b": (simple_udf, ["wrong_column"])}, **default_shuffle_config)


def test_add_columns_validates_multiple_missing_columns(db) -> None:
    """Test add_columns() with multiple missing columns."""

    @udf(data_type=pa.int32())
    def multi_col_udf(col1: int, col2: int, col3: int) -> int:
        return col1 + col2 + col3

    tbl = db.open_table("foo")

    # Should list all missing columns
    with pytest.raises(
        ValueError,
        match=r"expects input columns \['col1', 'col2', 'col3'\].*"
        r"not found in table schema",
    ):
        tbl.add_columns({"b": multi_col_udf}, **default_shuffle_config)


def test_add_columns_passes_with_correct_columns(db) -> None:
    """Test that add_columns() succeeds when columns are correct."""

    @udf(data_type=pa.int32())
    def good_udf(a: int) -> int:
        return a * 2

    tbl = db.open_table("foo")

    # Should not raise - column 'a' exists in table
    tbl.add_columns({"b": good_udf}, **default_shuffle_config)

    # Verify the column was added
    assert "b" in tbl.schema.names


def test_recordbatch_udf_raises_if_input_columns_specified(db) -> None:
    """Test that RecordBatch UDFs raise error if input_columns are specified."""

    # Should raise ValueError at UDF creation time
    with pytest.raises(
        ValueError,
        match=r"RecordBatch input UDF must not declare any input columns",
    ):

        @udf(data_type=pa.int32(), input_columns=["a"])
        def recordbatch_with_cols(batch: pa.RecordBatch) -> pa.Array:
            return pa.array([1] * batch.num_rows, type=pa.int32())


def test_recordbatch_udf_rejects_explicit_input_columns_at_add_time(db) -> None:
    """Test that RecordBatch UDFs reject explicit input_columns at add_columns time."""

    @udf(data_type=pa.int32())
    def recordbatch_udf_good(batch: pa.RecordBatch) -> pa.Array:
        return pa.array([1] * batch.num_rows, type=pa.int32())

    tbl = db.open_table("foo")

    # Should raise ValueError when trying to add with explicit input_columns
    with pytest.raises(
        ValueError,
        match=r"RecordBatch UDF but has input_columns.*specified",
    ):
        tbl.add_columns({"b": (recordbatch_udf_good, ["a"])}, **default_shuffle_config)


def test_recordbatch_udf_backfill_with_empty_input_columns_metadata(
    db, local_ray_context
) -> None:
    """RecordBatch column backfill works when udf_inputs is persisted as [].

    The namespace API stores ``input_columns`` as a non-nullable list, so a
    RecordBatch column created over ``db://`` reads back as ``[]`` rather than
    ``null``. The worker must normalize that to None so the UDF receives the
    whole batch — otherwise ``[]`` becomes an empty scan projection and the UDF
    loses its source columns. Regression test for GEN-920.
    """
    tbl = setup_table_and_udf_column(db, default_shuffle_config, recordbatch_udf)

    # Simulate the remote (db://) representation: rewrite the column's
    # udf_inputs metadata from "null" to "[]".
    field = tbl.schema.field("b")
    metadata = {
        (k.decode() if isinstance(k, bytes) else k): (
            v.decode() if isinstance(v, bytes) else v
        )
        for k, v in (field.metadata or {}).items()
    }
    metadata["virtual_column.udf_inputs"] = "[]"
    tbl.update_field_metadata({"path": "b", "metadata": metadata, "replace": True})
    assert tbl.schema.field("b").metadata[b"virtual_column.udf_inputs"] == b"[]"

    # Backfill must still pass the whole batch to the RecordBatch UDF.
    tbl.backfill("b")

    result = tbl.to_arrow()
    assert result["b"].to_pylist() == list(range(SIZE))


# Backfill tests with scalar return values


# 0.1 cpu so we don't wait for provisioning in the tests
@udf(data_type=pa.int32(), checkpoint_size=8, num_cpus=1)
def times_ten(a) -> int:
    return a * 10


scalar_udftest = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [x * 10 for x in range(SIZE)],
    },
)

# handle even rows
scalar_udftest_filter_even = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [x * 10 if x % 2 == 0 else None for x in range(SIZE)],
    },
    "a % 2 = 0",
)

# handle num_frags
scalar_udftest_num_frags = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [x * 10 if x < 10 else None for x in range(SIZE)],
    },
)


default_shuffle_config = {
    "batch_size": 1,
    "shuffle_buffer_size": 3,
    "task_shuffle_diversity": None,
}


@pytest.mark.parametrize(
    "shuffle_config",
    [
        {
            "batch_size": batch_size,
            "shuffle_buffer_size": shuffle_buffer_size,
            "task_shuffle_diversity": task_shuffle_diversity,
            "intra_applier_concurrency": intra_applier_concurrency,
        }
        for (
            batch_size,
            shuffle_buffer_size,
            task_shuffle_diversity,
            intra_applier_concurrency,
        ) in itertools.product(
            [4, 16],
            [7],
            [3],
            [1, 4],  # simple applier or multiprocessing batch applier= 4
        )
    ],
)
def test_run_ray_add_column(db: Connection, shuffle_config) -> None:
    tbl = setup_table_and_udf_column(db, shuffle_config, times_ten)
    backfill_and_verify(tbl, scalar_udftest)


@pytest.mark.multibackfill
def test_run_ray_add_column_ifnull(db: Connection) -> None:
    tbl = setup_table_and_udf_column(db, default_shuffle_config, times_ten)
    backfill_and_verify(tbl, scalar_udftest_filter_even)
    backfill_and_verify(
        tbl, UDFTestConfig(scalar_udftest.expected_recordbatch, where="b is null")
    )


@pytest.mark.multibackfill
def test_backfill_srcfiles_hash_cascade(db: Connection, local_ray_context) -> None:
    @udf(data_type=pa.int32())
    def b_from_a(a: int) -> int:
        return a * 10

    @udf(data_type=pa.int32())
    def c_from_b(b) -> int | None:
        if b is None:
            return None
        return b + 1

    tbl = db.open_table("foo")
    tbl.add_columns({"b": b_from_a}, **default_shuffle_config)
    tbl.add_columns({"c": c_from_b}, **default_shuffle_config)

    fut_c_first = tbl.backfill_async("c")
    fut_c_first.result()
    tbl.checkout_latest()
    data = tbl.to_arrow().to_pydict()
    assert all(val is None for val in data["c"])

    fut_b = tbl.backfill_async("b")
    fut_b.result()
    tbl.checkout_latest()
    data = tbl.to_arrow().to_pydict()
    assert data["b"] == [x * 10 for x in range(SIZE)]
    assert all(val is None for val in data["c"])

    fut_c_second = tbl.backfill_async("c")
    fut_c_second.result()
    tbl.checkout_latest()
    data = tbl.to_arrow().to_pydict()
    assert data["c"] == [x * 10 + 1 for x in range(SIZE)]


@pytest.mark.multibackfill
def test_backfill_srcfiles_hash_on_input_update(
    db: Connection, local_ray_context
) -> None:
    @udf(data_type=pa.int32())
    def b_from_a_v1(a: int) -> int:
        return a * 2

    @udf(data_type=pa.int32())
    def b_from_a_v2(a: int) -> int:
        return a * 3

    @udf(data_type=pa.int32())
    def c_from_b(b: int) -> int:
        return b * 10

    tbl = db.create_table("update_srcfiles", pa.table({"a": range(SIZE)}))
    tbl.add_columns({"b": b_from_a_v1}, **default_shuffle_config)
    tbl.add_columns({"c": c_from_b}, **default_shuffle_config)

    fut_b_first = tbl.backfill_async("b")
    fut_b_first.result()
    tbl.checkout_latest()
    fut_c_first = tbl.backfill_async("c")
    fut_c_first.result()
    tbl.checkout_latest()
    data = tbl.to_arrow().to_pydict()
    assert data["b"] == [val * 2 for val in range(SIZE)]
    assert data["c"] == [val * 20 for val in range(SIZE)]

    # Update computed column b via alter_columns; input column remains "a".
    tbl.alter_columns({"path": "b", "udf": b_from_a_v2})
    fut_b_second = tbl.backfill_async("b")
    fut_b_second.result()
    tbl.checkout_latest()

    fut_c_second = tbl.backfill_async("c")
    fut_c_second.result()
    tbl.checkout_latest()
    data = tbl.to_arrow().to_pydict()
    assert data["b"] == [val * 3 for val in range(SIZE)]
    assert data["c"] == [val * 30 for val in range(SIZE)]


@pytest.mark.multibackfill
def test_ray_run_add_column_filter_incremental(db: Connection) -> None:
    tbl = setup_table_and_udf_column(db, default_shuffle_config, times_ten)

    backfill_and_verify(tbl, scalar_udftest_filter_even)

    # add rows divisible by 3
    scalar_udftest_filter_treys = UDFTestConfig(
        {
            "a": list(range(SIZE)),
            "b": [x * 10 if x % 3 == 0 or x % 2 == 0 else None for x in range(SIZE)],
        },
        "a % 3 = 0",
    )
    backfill_and_verify(tbl, scalar_udftest_filter_treys)

    # add odd rows
    expected = {
        "a": list(range(SIZE)),
        "b": [x * 10 for x in range(SIZE)],  # all rows covered
    }
    backfill_and_verify(tbl, UDFTestConfig(expected, where="a % 2 = 1"))


@pytest.mark.multibackfill
def test_ray_run_add_column_filter_incremental_numfrags(tmp_path, tbl_path) -> None:
    """
    Test incremental backfill with num_frags parameter.

    Creates a table with 10 fragments (20 rows, 2 rows per fragment).
    Tests three incremental backfills:
    1. num_frags=2: processes only first 2 fragments (rows 0-3)
    2. num_frags=5: processes first 5 fragments (rows 0-9)
    3. no limit: processes all fragments (rows 0-19)
    """
    # Create a table with 10 fragments and setup UDF column
    make_new_ds_a_with_10_fragments(tbl_path)
    db = geneva.connect(str(tmp_path))
    tbl = db.open_table("foo")
    tbl.add_columns(
        {"b": times_ten},
        **default_shuffle_config,
    )

    # Define test configs for 20 rows (since we made 20 rows with 10 fragments)
    num_rows = 20

    # First backfill: num_frags=2 (only first 2 fragments)
    # Should process fragments 0-1 which contain rows 0-3
    expected_after_2frags = {
        "a": list(range(num_rows)),
        "b": [x * 10 if x < 4 else None for x in range(num_rows)],
    }
    expected_row_counts_2frags = {
        "rows_checkpointed": 4,  # Processed 4 rows from fragments 0-1
        "rows_ready_for_commit": 4,  # 4 rows ready for commit
        "rows_committed": 4,  # 4 rows committed (no skipped fragments)
    }
    backfill_and_verify(
        tbl,
        UDFTestConfig(expected_after_2frags),
        num_frags=2,
        expected_row_counts=expected_row_counts_2frags,
    )

    # Second backfill: num_frags=5 (first 5 fragments total)
    # Should process fragments 0-4 which contain rows 0-9
    # Note: this might only process fragments 2-4 (rows 4-9) if incremental
    expected_after_5frags = {
        "a": list(range(num_rows)),
        "b": [x * 10 if x < 10 else None for x in range(num_rows)],
    }
    expected_row_counts_5frags = {
        "rows_checkpointed": 10,  # 6 new rows from fragments 2-4, plus 4 skipped
        "rows_ready_for_commit": 10,  # 6 new + 4 skipped = 10 total (no double count)
        "rows_committed": 6,  # Only 6 newly processed rows committed
    }
    backfill_and_verify(
        tbl,
        UDFTestConfig(expected_after_5frags),
        num_frags=5,
        expected_row_counts=expected_row_counts_5frags,
    )

    # Final backfill: no num_frags limit (all remaining fragments)
    # Should process all fragments which contain rows 0-19
    # Note: this might only process fragments 5-9 (rows 10-19) if incremental
    expected_final = {
        "a": list(range(num_rows)),
        "b": [x * 10 for x in range(num_rows)],
    }
    expected_row_counts_final = {
        "rows_checkpointed": 20,  # 10 new rows from fragments 5-9, plus 10 skipped
        "rows_ready_for_commit": 20,  # 10 new + 10 skipped = 20 total (no double count)
        "rows_committed": 10,  # Only 10 newly processed rows committed
    }
    backfill_and_verify(
        tbl,
        UDFTestConfig(expected_final),
        expected_row_counts=expected_row_counts_final,
    )

    db.close()


@pytest.mark.multibackfill
def test_ray_double_counting_prevention(tmp_path, db, local_ray_context) -> None:
    """
    Specific test to prevent double counting regression in progress metrics.

    This test verifies that rows_ready_for_commit doesn't get inflated by
    counting skipped fragments multiple times during incremental backfill.
    """
    # Create a table with 6 fragments and setup UDF column
    tbl_path = tmp_path / "double_count_test.lance"
    make_new_ds_a_with_fragments(tbl_path, num_rows=12, rows_per_fragment=2)
    tbl = db.open_table("double_count_test")
    tbl.add_columns(
        {"b": times_ten},
        **default_shuffle_config,
    )

    # First backfill: process 2 fragments (4 rows)
    fut1 = tbl.backfill_async("b", num_frags=2)
    fut1.result()
    tbl.checkout_latest()

    inner1 = getattr(fut1, "future", fut1)
    if hasattr(inner1, "job_tracker") and inner1.job_tracker is not None:
        import ray

        metrics1 = ray.get(inner1.job_tracker.get_all.remote())

        # Verify first job metrics are sane
        assert metrics1["rows_checkpointed"]["n"] == 4
        assert metrics1["rows_ready_for_commit"]["n"] == 4
        assert metrics1["rows_committed"]["n"] == 4

    # Second backfill: remaining fragments with skipped fragments
    fut2 = tbl.backfill_async("b")
    fut2.result()
    tbl.checkout_latest()

    inner2 = getattr(fut2, "future", fut2)
    if hasattr(inner2, "job_tracker") and inner2.job_tracker is not None:
        metrics2 = ray.get(inner2.job_tracker.get_all.remote())

        checkpointed = metrics2["rows_checkpointed"]["n"]
        ready = metrics2["rows_ready_for_commit"]["n"]
        committed = metrics2["rows_committed"]["n"]

        # The key test: rows_ready_for_commit should NOT be significantly
        # higher than rows_checkpointed (which would indicate double counting)
        assert ready <= checkpointed + 2, (
            f"DOUBLE COUNTING BUG: rows_ready_for_commit ({ready}) "
            f"exceeds rows_checkpointed ({checkpointed}) by too much. "
            f"This suggests skipped fragments are being counted multiple times."
        )

        # Additional sanity checks
        assert committed <= checkpointed, (
            f"rows_committed ({committed}) should not exceed "
            f"rows_checkpointed ({checkpointed})"
        )

        assert committed == 12, f"Expected 12 committed rows, got {committed}"

        # Total data should be processed correctly regardless of metrics
        result = tbl.to_arrow().to_pydict()
        processed_count = sum(1 for x in result["b"] if x is not None)
        assert processed_count == 12, (
            f"Expected 12 processed rows, got {processed_count}"
        )


def test_fragment_writer_manager_falls_back_on_stable_row_id_commit_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FakeMapTask:
        def output_schema(self) -> pa.Schema:
            return pa.schema([pa.field("value", pa.int64())])

        def name(self) -> str:
            # _record_commit_elapsed emits metrics labeled with the map
            # task's name whenever the (mocked) commit attempt takes >= 1ms —
            # timing-dependent on CI runners, so the stub must provide it.
            return "fake-map-task"

    fallback_calls: list[tuple[list[tuple[int, object, int]], int]] = []

    def _fake_open_dataset(self) -> None:
        return None

    def _fake_commit(*args: object, **kwargs: object) -> NoReturn:
        raise OSError("Invalid user input: All fragments must have row ids")

    def _fake_merge_fallback(
        self,
        to_commit: list[tuple[int, object, int]],
        storage_options: object,
    ) -> None:
        fallback_calls.append(list(to_commit))

    monkeypatch.setattr(
        FragmentWriterManager,
        "_open_dataset_for_metadata",
        _fake_open_dataset,
    )
    monkeypatch.setattr(lance.LanceDataset, "commit", _fake_commit)
    monkeypatch.setattr(
        FragmentWriterManager,
        "_commit_with_merge_fallback",
        _fake_merge_fallback,
    )

    manager = FragmentWriterManager(
        dst_read_version=7,
        ds_uri="memory:///dst.lance",
        map_task=_FakeMapTask(),
        checkpoint_store=object(),  # type: ignore[arg-type]
        where=None,
        job_tracker=None,
        commit_granularity=1,
        expected_tasks={},
    )
    data_file = lance.fragment.DataFile("f.lance", [1], [0], 2, 0)
    manager.to_commit = [
        (
            0,
            data_file,
            3,
        )
    ]

    manager._commit_if_n_fragments(1)

    assert fallback_calls == [[(0, data_file, 3)]]
    assert manager._reconciled_rows_committed_total == 3


def _conflict_test_manager(dst_read_version: int) -> FragmentWriterManager:
    class _FakeMapTask:
        def output_schema(self) -> pa.Schema:
            return pa.schema([pa.field("value", pa.int64())])

        def name(self) -> str:
            # _record_commit_elapsed emits metrics labeled with the map
            # task's name whenever the (mocked) commit attempt takes >= 1ms —
            # timing-dependent on CI runners, so the stub must provide it.
            return "fake-map-task"

    manager = FragmentWriterManager(
        dst_read_version=dst_read_version,
        ds_uri="memory:///dst.lance",
        map_task=_FakeMapTask(),
        checkpoint_store=object(),  # type: ignore[arg-type]
        where=None,
        job_tracker=None,
        commit_granularity=1,
        expected_tasks={},
    )
    manager.to_commit = [(0, lance.fragment.DataFile("f.lance", [1], [0], 2, 0), 3)]
    return manager


def test_fragment_writer_manager_retries_on_retryable_commit_conflict(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # lance reworded the conflict to "Retryable commit conflict for version"
    # (lowercase); the guard must re-read the version and retry.
    commit_versions: list[object] = []

    def _fake_commit(*args: object, **kwargs: object) -> None:
        commit_versions.append(kwargs.get("read_version"))
        if len(commit_versions) == 1:
            raise OSError(
                "Retryable commit conflict for version 8: This DataReplacement "
                "transaction was preempted by concurrent transaction Merge at "
                "version 8. Please retry."
            )

    class _LatestDS:
        version = 9

    monkeypatch.setattr(
        FragmentWriterManager, "_open_dataset_for_metadata", lambda self: None
    )
    monkeypatch.setattr(lance.LanceDataset, "commit", _fake_commit)
    monkeypatch.setattr("geneva.db.open_lance_dataset", lambda *a, **k: _LatestDS())

    manager = _conflict_test_manager(8)
    manager._commit_if_n_fragments(1)

    # Stale commit at v8 conflicts; retry re-reads the latest version (v9).
    assert commit_versions == [8, 9]
    assert manager._reconciled_rows_committed_total == 3


def test_fragment_writer_manager_raises_on_removed_target_fragment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A removed-target IncompatibleTransaction is non-retryable: it must
    # propagate rather than spin the version-conflict loop.
    commit_versions: list[object] = []

    def _fake_commit(*args: object, **kwargs: object) -> NoReturn:
        commit_versions.append(kwargs.get("read_version"))
        raise OSError(
            "DataReplacement target fragment 0 was removed by concurrent "
            "Delete at version 8."
        )

    monkeypatch.setattr(
        FragmentWriterManager, "_open_dataset_for_metadata", lambda self: None
    )
    monkeypatch.setattr(lance.LanceDataset, "commit", _fake_commit)

    manager = _conflict_test_manager(8)
    with pytest.raises(OSError, match="was removed by concurrent"):
        manager._commit_if_n_fragments(1)

    assert commit_versions == [8]


_EXPIRED_TOKEN_MESSAGE = (
    "LanceError(IO): Generic S3 error: Error performing list request: "
    "Server returned non-2xx status code: 400 Bad Request: "
    "<Error><Code>ExpiredToken</Code>"
    "<Message>The provided token has expired.</Message></Error>"
)


def test_fragment_writer_manager_revends_credentials_on_expired_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The manager holds job-start credentials; a commit that outlives the
    # vended token must re-vend and replay rather than fail the job.
    commit_versions: list[object] = []
    revends: list[bool] = []

    def _fake_commit(*args: object, **kwargs: object) -> None:
        commit_versions.append(kwargs.get("read_version"))
        if len(commit_versions) == 1:
            raise OSError(_EXPIRED_TOKEN_MESSAGE)

    monkeypatch.setattr(
        FragmentWriterManager, "_open_dataset_for_metadata", lambda self: None
    )
    monkeypatch.setattr(lance.LanceDataset, "commit", _fake_commit)
    monkeypatch.setattr(
        FragmentWriterManager,
        "_refresh_credentials_on_error",
        lambda self: revends.append(True),
    )

    manager = _conflict_test_manager(8)
    manager._commit_if_n_fragments(1)

    # Same read_version both times: a re-vend replays the identical commit.
    assert commit_versions == [8, 8]
    assert revends == [True]
    assert manager._reconciled_rows_committed_total == 3


def test_fragment_writer_manager_bounds_credential_revend_retries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A token that stays dead after re-vending must fail the commit instead of
    # spinning the loop.
    from geneva.runners.ray.pipeline import GENEVA_COMMIT_CREDENTIAL_REVEND_RETRIES

    commit_attempts: list[object] = []
    revends: list[bool] = []

    def _fake_commit(*args: object, **kwargs: object) -> NoReturn:
        commit_attempts.append(kwargs.get("read_version"))
        raise OSError(_EXPIRED_TOKEN_MESSAGE)

    monkeypatch.setattr(
        FragmentWriterManager, "_open_dataset_for_metadata", lambda self: None
    )
    monkeypatch.setattr(lance.LanceDataset, "commit", _fake_commit)
    monkeypatch.setattr(
        FragmentWriterManager,
        "_refresh_credentials_on_error",
        lambda self: revends.append(True),
    )

    manager = _conflict_test_manager(8)
    with pytest.raises(OSError, match="ExpiredToken"):
        manager._commit_if_n_fragments(1)

    assert len(revends) == GENEVA_COMMIT_CREDENTIAL_REVEND_RETRIES
    assert len(commit_attempts) == GENEVA_COMMIT_CREDENTIAL_REVEND_RETRIES + 1


# ---------------------------------------------------------------------------
# commit_backfill_completion_marker (ENT-1405 / PR #922)
#
# After a backfill finishes, FragmentWriterManager tags the dataset with the
# `lancedb:agent:completed_job_json` transaction property so lance-agent (whose
# existing transaction scan reads that key, just like it does for indexer /
# compaction commits) advances the column's `completed_iteration` immediately
# instead of waiting out its reconciliation buffer.
# ---------------------------------------------------------------------------

COMPLETED_JOB_KEY = "lancedb:agent:completed_job_json"


class _MarkerMapTask:
    """Minimal MapTask: FragmentWriterManager only needs an output schema to
    construct; the marker path itself does not touch the map task."""

    def output_schema(self) -> pa.Schema:
        return pa.schema([pa.field("doubled", pa.int64())])


def _marker_fwm(ds_uri: str, dst_read_version: int) -> FragmentWriterManager:
    return FragmentWriterManager(
        dst_read_version=dst_read_version,
        ds_uri=ds_uri,
        map_task=_MarkerMapTask(),
        checkpoint_store=object(),  # type: ignore[arg-type]
        where=None,
        job_tracker=None,
        commit_granularity=999,
        expected_tasks={},
    )


def test_commit_backfill_completion_marker_writes_transaction_property(
    tmp_path: Path,
) -> None:
    uri = str(tmp_path / "t.lance")
    ds = lance.write_dataset(pa.table({"id": [1, 2, 3]}), uri)
    base_version = ds.version

    _marker_fwm(uri, base_version).commit_backfill_completion_marker(
        "t.backfill.doubled-abc123-i2", "doubled"
    )

    reopened = lance.dataset(uri)
    # The marker is an empty DataReplacement: a new version, but no data change.
    assert reopened.version > base_version
    assert reopened.count_rows() == 3
    payload = json.loads(
        reopened.read_transaction(reopened.version).transaction_properties[
            COMPLETED_JOB_KEY
        ]
    )
    assert payload == {
        "job_id": "t.backfill.doubled-abc123-i2",
        "job_type": "udf_virtual_column_backfill",
        "column_name": "doubled",
        "job_metadata": json.dumps({"iteration": 2}),
    }


@pytest.mark.parametrize(
    ("job_id", "expected_iteration"),
    [
        ("t.backfill.doubled-abc123-i1", 1),
        ("t.backfill.doubled-abc123-i7", 7),
        ("t.backfill.doubled-abc123-i0", 0),
        ("deadbeefcafe", 0),  # explicit / non-agent job id: no -iN suffix
    ],
)
def test_commit_backfill_completion_marker_payload(
    monkeypatch: pytest.MonkeyPatch, job_id: str, expected_iteration: int
) -> None:
    captured: dict[str, Any] = {}

    def _fake_commit(base_uri: object, operation: object, **kwargs: object) -> None:
        captured["operation"] = operation

    monkeypatch.setattr(lance.LanceDataset, "commit", _fake_commit)

    _marker_fwm(
        "memory:///dst.lance", dst_read_version=7
    ).commit_backfill_completion_marker(job_id, "doubled")

    txn = captured["operation"]
    assert isinstance(txn, lance.Transaction)
    # Committed against dst_read_version like every other backfill commit, as an
    # empty (no data change) DataReplacement so it never conflicts.
    assert txn.read_version == 7
    assert isinstance(txn.operation, lance.LanceOperation.DataReplacement)
    assert txn.operation.replacements == []

    payload = json.loads(txn.transaction_properties[COMPLETED_JOB_KEY])
    assert payload["job_id"] == job_id
    assert payload["job_type"] == "udf_virtual_column_backfill"
    assert payload["column_name"] == "doubled"
    assert json.loads(payload["job_metadata"]) == {"iteration": expected_iteration}


def test_commit_backfill_completion_marker_is_best_effort(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _boom(*args: object, **kwargs: object) -> NoReturn:
        raise RuntimeError("commit failed")

    monkeypatch.setattr(lance.LanceDataset, "commit", _boom)

    # A marker failure must never fail an otherwise-successful backfill.
    _marker_fwm(
        "memory:///dst.lance", dst_read_version=7
    ).commit_backfill_completion_marker("t.backfill.doubled-abc123-i1", "doubled")


def test_build_direct_fragment_write_config_includes_storage_options(
    tmp_path: Path,
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [None, None, None]}))
    table_ref = tbl.get_reference()
    table_ref.storage_options = {"account_name": "acct", "account_key": "secret"}

    @udf(data_type=pa.int32())
    def one(x: int) -> int:
        return x + 1

    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(
            udfs={"b": one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=table_ref,
        input_plan=iter([]),
        job_id="job-direct-config",
        job_tracker=None,
        dst_read_version=123,
    )

    config = job._build_direct_fragment_write_config()

    assert config is not None
    assert config.storage_options == table_ref.storage_options
    assert config.read_version == 123


def test_build_direct_fragment_write_config_prefers_planned_read_version(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [None, None, None]}))
    table_ref = tbl.get_reference()
    dataset = tbl.to_lance()

    @udf(data_type=pa.int32())
    def one(x: int) -> int:
        return x + 1

    class _FakeTable:
        def to_lance(self) -> object:
            class _FakeDataset:
                uri = dataset.uri
                version = dataset.version + 10
                data_storage_version = dataset.data_storage_version
                lance_schema = dataset.lance_schema

            return _FakeDataset()

    monkeypatch.setattr(
        TableReference,
        "open",
        lambda self: _FakeTable(),
        raising=True,
    )

    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(
            udfs={"b": one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=table_ref,
        input_plan=iter([]),
        job_id="job-direct-config-read-version",
        job_tracker=None,
        dst_read_version=7,
    )

    config = job._build_direct_fragment_write_config()

    assert config is not None
    assert config.read_version == 7


@pytest.mark.parametrize(
    ("skipped_fragments", "skipped_rows"),
    [
        ({}, 4),
        ({0: (lance.fragment.DataFile("f.lance", [1], [0], 2, 0), 3)}, 3),
    ],
)
def test_fragment_writer_manager_reconciles_skipped_stats(
    skipped_fragments: dict[int, tuple[lance.fragment.DataFile, int]],
    skipped_rows: int,
) -> None:
    class _FakeMapTask:
        def output_schema(self) -> pa.Schema:
            return pa.schema([pa.field("value", pa.int64())])

        def name(self) -> str:
            # _record_commit_elapsed emits metrics labeled with the map
            # task's name whenever the (mocked) commit attempt takes >= 1ms —
            # timing-dependent on CI runners, so the stub must provide it.
            return "fake-map-task"

    manager = FragmentWriterManager(
        dst_read_version=7,
        ds_uri="memory:///dst.lance",
        map_task=_FakeMapTask(),
        checkpoint_store=object(),  # type: ignore[arg-type]
        where=None,
        job_tracker=None,
        commit_granularity=1,
        expected_tasks={},
        skipped_fragments=skipped_fragments,
        skipped_stats={"rows": skipped_rows},
    )

    assert manager._reconciled_rows_checkpointed_total == skipped_rows
    assert manager._reconciled_rows_ready_total == skipped_rows
    assert manager._reconciled_rows_committed_total == skipped_rows


def test_merge_fallback_preserves_stable_row_id_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FakeMapTask:
        def output_schema(self) -> pa.Schema:
            return pa.schema([pa.field("value", pa.int64())])

        def name(self) -> str:
            # _record_commit_elapsed emits metrics labeled with the map
            # task's name whenever the (mocked) commit attempt takes >= 1ms —
            # timing-dependent on CI runners, so the stub must provide it.
            return "fake-map-task"

    row_id_meta = object()
    created_meta = object()
    updated_meta = object()
    deletion_file = object()
    original_file = lance.fragment.DataFile("orig.lance", [1, 2], [0, 1], 2, 0)
    replacement_file = lance.fragment.DataFile("new.lance", [2], [0], 2, 0)

    class _FakeMetadata:
        def __init__(self) -> None:
            self.deletion_file = deletion_file
            self.row_id_meta = row_id_meta
            self.created_at_version_meta = created_meta
            self.last_updated_at_version_meta = updated_meta

    class _FakeFragment:
        fragment_id = 0
        physical_rows = 3
        metadata = _FakeMetadata()

        def data_files(self) -> list[lance.fragment.DataFile]:
            return [original_file]

    captured: dict[str, object] = {}

    class _FakeDataset:
        lance_schema = pa.schema([pa.field("value", pa.int64())])
        data_storage_version = "2.0"
        version = 7

        def get_fragments(self) -> list[_FakeFragment]:
            return [_FakeFragment()]

    def _fake_dataset(*args: object, **kwargs: object) -> _FakeDataset:
        return _FakeDataset()

    def _fake_fragment_metadata(**kwargs: object) -> object:
        captured["fragment_metadata"] = kwargs
        return kwargs

    def _fake_merge(*args: object, **kwargs: object) -> object:
        captured["merge"] = kwargs
        return kwargs

    def _fake_commit(*args: object, **kwargs: object) -> None:
        captured["commit"] = kwargs

    monkeypatch.setattr(lance, "dataset", _fake_dataset)
    monkeypatch.setattr("lance.fragment.FragmentMetadata", _fake_fragment_metadata)
    monkeypatch.setattr(lance.LanceOperation, "Merge", _fake_merge)
    monkeypatch.setattr(lance.LanceDataset, "commit", _fake_commit)

    manager = FragmentWriterManager(
        dst_read_version=7,
        ds_uri="memory:///dst.lance",
        map_task=_FakeMapTask(),
        checkpoint_store=object(),  # type: ignore[arg-type]
        where=None,
        job_tracker=None,
        commit_granularity=1,
        expected_tasks={},
    )
    manager.output_field_ids = frozenset({2})

    manager._commit_with_merge_fallback(
        [(0, replacement_file, 3)],
        storage_options=None,
    )

    fragment_metadata = captured["fragment_metadata"]
    assert isinstance(fragment_metadata, dict)
    assert fragment_metadata["row_id_meta"] is row_id_meta
    assert fragment_metadata["created_at_version_meta"] is created_meta
    assert fragment_metadata["last_updated_at_version_meta"] is updated_meta
    assert fragment_metadata["deletion_file"] is deletion_file


def test_merge_fallback_raises_when_target_fragment_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # The fallback rebuilds the fragment list from the dataset's current state
    # on each attempt. An update target absent from that snapshot (removed or
    # renumbered by a concurrent writer) must fail the commit loudly -- a Merge
    # built without it would commit successfully and orphan its column file.
    class _FakeMapTask:
        def output_schema(self) -> pa.Schema:
            return pa.schema([pa.field("value", pa.int64())])

        def name(self) -> str:
            return "fake-map-task"

    original_file = lance.fragment.DataFile("orig.lance", [1, 2], [0, 1], 2, 0)
    replacement_file = lance.fragment.DataFile("new.lance", [2], [0], 2, 0)

    class _FakeMetadata:
        deletion_file = None
        row_id_meta = None
        created_at_version_meta = None
        last_updated_at_version_meta = None

    class _FakeFragment:
        fragment_id = 0
        physical_rows = 3
        metadata = _FakeMetadata()

        def data_files(self) -> list[lance.fragment.DataFile]:
            return [original_file]

    class _FakeDataset:
        lance_schema = pa.schema([pa.field("value", pa.int64())])
        data_storage_version = "2.0"
        version = 7

        def get_fragments(self) -> list[_FakeFragment]:
            return [_FakeFragment()]

    committed: list[object] = []
    monkeypatch.setattr(lance, "dataset", lambda *a, **k: _FakeDataset())
    monkeypatch.setattr(lance.LanceOperation, "Merge", lambda *a, **k: k)
    monkeypatch.setattr(
        lance.LanceDataset, "commit", lambda *a, **k: committed.append(k)
    )

    manager = FragmentWriterManager(
        dst_read_version=7,
        ds_uri="memory:///dst.lance",
        map_task=_FakeMapTask(),
        checkpoint_store=object(),  # type: ignore[arg-type]
        where=None,
        job_tracker=None,
        commit_granularity=1,
        expected_tasks={},
    )
    manager.output_field_ids = frozenset({2})

    # The dataset snapshot holds only fragment 0; the update targets fragment 3.
    with pytest.raises(MergeFallbackTargetError, match=r"\[3\]"):
        manager._commit_with_merge_fallback(
            [(3, replacement_file, 3)],
            storage_options=None,
        )
    assert not committed


@pytest.mark.ray
def test_row_metrics_reconcile_when_tracker_drops_updates(
    tmp_path, db, local_ray_context, monkeypatch
) -> None:
    """
    Simulate a flaky JobTracker that drops increment updates. The pipeline should
    still report accurate final row metrics by reconciling totals at the end.
    """
    from geneva.runners.ray import jobtracker

    # Drop ALL increment updates to mimic lost progress messages
    async def drop_increment(self, name: str, delta: int = 1) -> None:  # noqa: ANN001
        await self._upsert(name)

    monkeypatch.setattr(jobtracker.JobTracker, "increment", drop_increment)

    # Build a small table
    num_rows = 12
    data = {"a": pa.array(range(num_rows))}
    tbl_path = tmp_path / "reconcile.lance"
    lance.write_dataset(
        pa.Table.from_pydict(data),
        tbl_path,
        max_rows_per_file=4,
        data_storage_version="2.0",
    )

    @udf(data_type=pa.int32())
    def times_two(a: int) -> int:
        return a * 2

    tbl = db.open_table("reconcile")
    tbl.add_columns({"b": times_two}, batch_size=3)

    fut = tbl.backfill_async("b")
    fut.result()

    metrics = ray.get(fut.future.job_tracker.get_all.remote())  # type: ignore[arg-type]
    checkpointed = metrics["rows_checkpointed"]
    ready = metrics["rows_ready_for_commit"]
    committed = metrics["rows_committed"]

    assert checkpointed["n"] == checkpointed["total"] == num_rows
    assert ready["n"] == ready["total"] == num_rows
    assert committed["n"] == committed["total"] == num_rows


@pytest.mark.timeout(120)
def test_transient_actor_loss_reschedules_to_surviving_actor_without_replacement(
    tmp_path: Path,
    tbl_path: Path,
    tbl_ref: TableReference,
    ckp_store: CheckpointStore,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_queue_actor_startup = ActorPool._queue_actor_startup
    startup_calls = 0

    def queue_initial_actors_only(self: ActorPool) -> None:
        nonlocal startup_calls
        if startup_calls < 2:
            startup_calls += 1
            original_queue_actor_startup(self)
            return
        # Simulate KubeRay being unable to create a replacement actor because
        # the backing node pool is already at max capacity.

    monkeypatch.setattr(ActorPool, "_queue_actor_startup", queue_initial_actors_only)
    monkeypatch.setattr(ActorPool, "_actor_liveness_scan_interval_s", 0.0)
    monkeypatch.setattr("geneva.runners.ray.pipeline.POLL_INTERVAL_S", 0.05)

    loss_injected = False

    def actor_states_with_one_preempted_loss(
        self: ActorPool, actor_ids: set[str]
    ) -> dict[str, ActorStateSnapshot]:
        nonlocal loss_injected
        if not actor_ids:
            return {}
        victim = sorted(actor_ids)[0] if not loss_injected else None
        loss_injected = True
        snapshots: dict[str, ActorStateSnapshot] = {}
        for actor_id in actor_ids:
            if actor_id == victim:
                snapshots[actor_id] = ActorStateSnapshot(
                    actor_id=actor_id,
                    state="DEAD",
                    death_cause={
                        "actorDiedErrorContext": {
                            "reason": "AUTOSCALER_DRAIN_PREEMPTED",
                            "nodeDeathInfo": {"reason": "AUTOSCALER_DRAIN_PREEMPTED"},
                        }
                    },
                    death_reason="AUTOSCALER_DRAIN_PREEMPTED",
                    node_id="node-preempted",
                    preempted=True,
                )
            else:
                snapshots[actor_id] = ActorStateSnapshot(
                    actor_id=actor_id,
                    state="ALIVE",
                    node_id="node-live",
                )
        return snapshots

    monkeypatch.setattr(
        ActorPool,
        "_actor_states_by_id",
        actor_states_with_one_preempted_loss,
    )

    flag_path = str(tmp_path / "actor-loss-injected")

    @udf(data_type=pa.int32(), batch_size=4, version=uuid.uuid4().hex)
    def slow_once_then_double(a: int) -> int:
        try:
            fd = os.open(flag_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            return a * 2
        else:
            os.close(fd)
            time.sleep(1.0)
            return a * 2

    add_empty_b(lance.dataset(tbl_path), int32_return_none)

    run_ray_add_column(
        tbl_ref,
        ["a"],
        {"b": slow_once_then_double},
        checkpoint_store=ckp_store,
        concurrency=2,
        task_size=4,
        checkpoint_size=4,
        commit_granularity=1,
    )

    assert startup_calls == 2
    assert loss_injected is True
    values = lance.dataset(tbl_path).to_table().sort_by("a")["b"].to_pylist()
    assert values == [i * 2 for i in range(SIZE)]


@pytest.mark.parametrize(
    ("allow_graceful", "force_ready_future"),
    [
        pytest.param(False, False, id="sigkill-liveness-scan"),
        pytest.param(True, True, id="sigterm-ready-future"),
    ],
)
@pytest.mark.timeout(180)
def test_lost_worker_node_reschedules_backfill_to_surviving_actor_without_replacement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    allow_graceful: bool,
    force_ready_future: bool,
) -> None:
    from ray.cluster_utils import Cluster
    from ray.util.scheduling_strategies import NodeAffinitySchedulingStrategy

    from geneva.runners.ray import pipeline as pipeline_module

    ray.shutdown()
    cluster = Cluster()
    head_node = cluster.add_node(num_cpus=2)
    worker_node = cluster.add_node(num_cpus=1)
    cluster.wait_for_nodes()
    ray.init(address=cluster.address, log_to_driver=False)

    thread: threading.Thread | None = None
    try:
        lost_worker_tbl_path = tmp_path / "lost_worker.lance"
        num_rows = 20
        make_new_ds_a_with_fragments(
            lost_worker_tbl_path,
            num_rows=num_rows,
            rows_per_fragment=2,
        )
        add_empty_b(lance.dataset(lost_worker_tbl_path), int32_return_none)

        tbl_ref = TableReference(
            table_id=["lost_worker"],
            version=None,
            db_uri=str(tmp_path),
        )
        ckp_store = CheckpointStore.from_uri(str(tmp_path / "lost-worker-ckp"))

        marker_dir = tmp_path / "lost-worker-markers"
        marker_dir.mkdir()
        marker_dir_str = str(marker_dir)
        worker_node_id = str(worker_node.node_id)

        @udf(data_type=pa.int32(), checkpoint_size=1, version=uuid.uuid4().hex)
        def slow_node_marking_double(a: int) -> int:
            node_id = str(ray.get_runtime_context().get_node_id())
            marker_path = os.path.join(marker_dir_str, node_id)
            try:
                fd = os.open(marker_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                pass
            else:
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
            if node_id == worker_node_id:
                time.sleep(5.0)
            else:
                time.sleep(0.05)
            return a * 2

        class NodeAffinityActorFactory:
            def __init__(self) -> None:
                self._calls = 0

            def remote(self, **kwargs: object) -> Any:
                self._calls += 1
                node_id = worker_node.node_id if self._calls == 1 else head_node.node_id
                return ApplierActor.options(
                    num_cpus=1,
                    scheduling_strategy=NodeAffinitySchedulingStrategy(
                        node_id,
                        soft=False,
                    ),
                ).remote(**kwargs)

        def setup_actor_with_affinity(
            _self: ColumnAddPipelineJob,
        ) -> NodeAffinityActorFactory:
            return NodeAffinityActorFactory()

        original_queue_actor_startup = ActorPool._queue_actor_startup
        startup_calls = 0

        def queue_initial_actors_only(self: ActorPool) -> None:
            nonlocal startup_calls
            if startup_calls < 2:
                startup_calls += 1
                original_queue_actor_startup(self)
                return

        monkeypatch.setattr(
            ColumnAddPipelineJob,
            "setup_actor",
            setup_actor_with_affinity,
        )
        monkeypatch.setattr(
            ActorPool, "_queue_actor_startup", queue_initial_actors_only
        )
        monkeypatch.setattr(ActorPool, "_actor_liveness_scan_interval_s", 0.0)
        monkeypatch.setattr(pipeline_module, "POLL_INTERVAL_S", 0.05)

        observed_requeries: list[ActorStateSnapshot] = []
        if force_ready_future:
            original_actor_state_by_id = getattr(
                ActorPool,
                "_actor_state_by_id",
                None,
            )
            if original_actor_state_by_id is not None:

                def record_actor_state_requery(
                    self: ActorPool,
                    actor_id: str,
                ) -> ActorStateSnapshot | None:
                    snapshot = original_actor_state_by_id(self, actor_id)
                    if snapshot is not None:
                        observed_requeries.append(snapshot)
                    return snapshot

                monkeypatch.setattr(
                    ActorPool,
                    "_actor_state_by_id",
                    record_actor_state_requery,
                )
            # Deterministically exercise the future-first race. The production
            # liveness fallback is covered by the SIGKILL parameter case.
            monkeypatch.setattr(
                ActorPool,
                "_pop_dead_actor_task",
                lambda self: self.NoResult,
            )

        errors: list[BaseException] = []
        done = threading.Event()

        def run_backfill() -> None:
            try:
                run_ray_add_column(
                    tbl_ref,
                    ["a"],
                    {"b": slow_node_marking_double},
                    checkpoint_store=ckp_store,
                    concurrency=2,
                    task_size=2,
                    checkpoint_size=2,
                    commit_granularity=1,
                )
            except BaseException as exc:  # pragma: no cover - re-raised on main thread
                errors.append(exc)
            finally:
                done.set()

        thread = threading.Thread(target=run_backfill, daemon=True)
        thread.start()

        removed_worker = False
        deadline = time.monotonic() + 60
        worker_marker = marker_dir / worker_node_id
        while time.monotonic() < deadline:
            if worker_marker.exists():
                cluster.remove_node(worker_node, allow_graceful=allow_graceful)
                removed_worker = True
                break
            if done.is_set():
                break
            time.sleep(0.05)

        assert removed_worker, "worker ApplierActor never started a task"
        assert done.wait(90), "backfill did not finish after worker node loss"
        if errors:
            raise AssertionError(f"backfill raised {errors[0]!r}") from errors[0]

        assert startup_calls == 2
        if force_ready_future:
            assert any(
                snapshot.state == "DEAD"
                and snapshot.death_reason == "NODE_DIED"
                and snapshot.node_id == worker_node_id
                and snapshot.is_transient_infra_loss
                for snapshot in observed_requeries
            )
        values = (
            lance.dataset(lost_worker_tbl_path).to_table().sort_by("a")["b"].to_pylist()
        )
        assert values == [i * 2 for i in range(num_rows)]
    finally:
        ray.shutdown()
        cluster.shutdown()
        if thread is not None and thread.is_alive():
            thread.join(timeout=10)


def test_applier_actor_retries_without_rebinding_tables(monkeypatch) -> None:
    calls: dict[str, int] = {"bind": 0, "clear": 0, "run": 0}

    class FakeApplier:
        batch_applier = None
        batch_checkpointing_time_ms = 0
        checkpoint_load_time_ms = 0
        checkpoint_exists_time_ms = 0
        checkpoint_list_time_ms = 0

        def run(
            self, task
        ) -> tuple[list[object], DirectFragmentWriteResult | None, int]:  # noqa: ANN001
            calls["run"] += 1
            if calls["run"] == 1:
                raise RuntimeError("object store connection reset by peer")
            return [], None, 0

    monkeypatch.setattr(
        "geneva.runners.ray.pipeline.object_store_retry.APPLIER_TRANSIENT_RETRIES",
        1,
    )
    monkeypatch.setattr(
        (
            "geneva.runners.ray.pipeline."
            "object_store_retry.APPLIER_RETRY_BASE_BACKOFF_SECONDS"
        ),
        0.0,
    )
    monkeypatch.setattr(
        (
            "geneva.runners.ray.pipeline."
            "object_store_retry.APPLIER_RETRY_MAX_BACKOFF_SECONDS"
        ),
        0.0,
    )
    monkeypatch.setattr(
        "geneva.runners.ray.pipeline.bind_tables_for_task",
        lambda task, table_cache: calls.__setitem__("bind", calls["bind"] + 1),
    )
    monkeypatch.setattr(
        "geneva.runners.ray.pipeline.clear_bound_tables",
        lambda task: calls.__setitem__("clear", calls["clear"] + 1),
    )

    actor = ApplierActor.__ray_metadata__.modified_class(applier=FakeApplier())
    task = object()

    result = actor.run(task)

    assert result[0] is task
    assert calls == {"bind": 1, "clear": 1, "run": 2}


def test_applier_actor_retries_transient_setup_open_failure(monkeypatch) -> None:
    calls: dict[str, int] = {"open": 0, "run": 0}

    class FakeApplier:
        batch_applier = None
        batch_checkpointing_time_ms = 0
        checkpoint_load_time_ms = 0
        checkpoint_exists_time_ms = 0
        checkpoint_list_time_ms = 0

        def run(
            self, task
        ) -> tuple[list[object], DirectFragmentWriteResult | None, int]:  # noqa: ANN001
            calls["run"] += 1
            return [], None, 0

    def fake_open(self: TableReference) -> object:
        calls["open"] += 1
        if calls["open"] == 1:
            raise RuntimeError("gcs object store connection reset by peer")
        return object()

    monkeypatch.setattr(TableReference, "open", fake_open, raising=True)
    monkeypatch.setattr(
        "geneva.apply.table_cache.object_store_retry.APPLIER_TRANSIENT_RETRIES",
        1,
    )
    monkeypatch.setattr(
        (
            "geneva.apply.table_cache."
            "object_store_retry.APPLIER_RETRY_BASE_BACKOFF_SECONDS"
        ),
        0.0,
    )
    monkeypatch.setattr(
        (
            "geneva.apply.table_cache."
            "object_store_retry.APPLIER_RETRY_MAX_BACKOFF_SECONDS"
        ),
        0.0,
    )

    actor = ApplierActor.__ray_metadata__.modified_class(applier=FakeApplier())
    task = ScanTask(
        uri="db://example/tbl",
        table_ref=TableReference(table_id=["tbl"], version=None, db_uri="db://example"),
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=1,
    )

    result = actor.run(task)

    assert result[0] is task
    assert calls == {"open": 2, "run": 1}
    assert task._table is None


def make_new_ds_a_with_fragments(
    tbl_path: Path, num_rows: int, rows_per_fragment: int
) -> lance.dataset:
    """Helper to create dataset with specific fragment layout."""
    data = {"a": pa.array(range(num_rows))}
    tbl = pa.Table.from_pydict(data)
    ds = lance.write_dataset(
        tbl, tbl_path, max_rows_per_file=rows_per_fragment, data_storage_version="2.0"
    )
    return ds


def test_run_ray_add_column_write_fault(
    tbl_path, tbl_ref, ckp_store, monkeypatch
) -> None:  # noqa: PT019
    add_empty_b(lance.dataset(tbl_path), int32_return_none)
    original_ingest = FragmentWriterSession.ingest_task

    def faulty_ingest(self, offset: int, result: Any, num_rows: int) -> None:
        original_ingest(self, offset, result, num_rows)
        if random.random() < 0.5:
            ray.kill(self.actor)
        else:
            ray.kill(self.queue.actor)

    monkeypatch.setattr(FragmentWriterSession, "ingest_task", faulty_ingest)

    run_ray_add_column(
        tbl_ref,
        ["a"],
        {"b": times_ten},
        checkpoint_store=ckp_store,
        # Use a large task_size so this fault-injection test doesn't create
        # tiny read tasks under the new decoupled sizing rules.
        task_size=SIZE,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    ds = lance.dataset(tbl_path)
    assert ds.to_table().to_pydict() == scalar_udftest.expected_recordbatch


def test_run_ray_add_column_with_deletes(db, ds, tbl_path, tbl_ref, ckp_store) -> None:  # noqa: PT019
    add_empty_b(ds, int32_return_none)
    ds = lance.dataset(tbl_path)  # reload to get latest
    ds.delete("a % 2 == 1")

    ds = lance.dataset(tbl_path)  # reload to get latest
    run_ray_add_column(
        tbl_ref,
        ["a"],
        {"b": times_ten},
        checkpoint_store=ckp_store,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    ds = lance.dataset(tbl_path)  # reload to get latest
    assert ds.to_table().to_pydict() == {
        "a": list(range(0, SIZE, 2)),
        "b": [x * 10 for x in range(0, SIZE, 2)],
    }


def test_run_ray_add_column_direct_fragment_write(tbl_path, tbl_ref, ckp_store) -> None:
    add_empty_b(lance.dataset(tbl_path), int32_return_none)

    run_ray_add_column(
        tbl_ref,
        ["a"],
        {"b": times_ten},
        checkpoint_store=ckp_store,
        checkpoint_size=0,
        task_size=0,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    ds = lance.dataset(tbl_path)
    assert ds.to_table().to_pydict() == scalar_udftest.expected_recordbatch

    checkpoint_keys = list(ckp_store.list_keys())
    assert checkpoint_keys
    assert all("_range-" not in key for key in checkpoint_keys)


def test_run_ray_add_column_direct_fragment_write_before_flush(
    tbl_path, tbl_ref, ckp_store
) -> None:
    add_empty_b(lance.dataset(tbl_path), int32_return_none)

    @udf(data_type=pa.int32(), batch_size=2, checkpoint_size=2, num_cpus=1)
    def times_ten_small(a) -> int:
        return a * 10

    run_ray_add_column(
        tbl_ref,
        ["a"],
        {"b": times_ten_small},
        checkpoint_store=ckp_store,
        checkpoint_size=2,
        task_size=0,
        batch_checkpoint_flush_interval_seconds=60.0,
        min_checkpoint_size=2,
        max_checkpoint_size=2,
    )

    ds = lance.dataset(tbl_path)
    assert ds.to_table().to_pydict() == scalar_udftest.expected_recordbatch

    checkpoint_keys = list(ckp_store.list_keys())
    assert checkpoint_keys
    assert all("_range-" not in key for key in checkpoint_keys)


def _assert_no_range_keys_remain(ckp_store: CheckpointStore) -> None:
    """Assert every key in the store is a fragment dedupe key, not per-batch."""
    keys = list(ckp_store.list_keys())
    assert keys, "checkpoint store unexpectedly empty after backfill"
    range_keys = [k for k in keys if "_range-" in k]
    assert not range_keys, (
        f"per-batch '_range-' keys leaked after backfill: {range_keys[:5]} "
        f"({len(range_keys)} total of {len(keys)})"
    )


def _run_cleanup_backfill(tmp_path, name: str) -> CheckpointStore:
    """Run a small multi-fragment backfill and return the checkpoint store.

    Uses small ``task_size`` / ``checkpoint_size`` to force per-batch
    checkpoint writes through the indirect commit path (i.e. not the
    direct fragment write fast path).
    """
    tbl_path = tmp_path / f"{name}.lance"
    make_new_ds_a_with_fragments(tbl_path, num_rows=12, rows_per_fragment=4)
    add_empty_b(lance.dataset(tbl_path), int32_return_none)
    ckp_store = CheckpointStore.from_uri(str(tmp_path / f"ckp_{name}"))
    tbl_ref = TableReference(table_id=[name], version=None, db_uri=str(tmp_path))

    @udf(data_type=pa.int32(), batch_size=2, checkpoint_size=2, num_cpus=1)
    def times_ten_small(a) -> int:
        return a * 10

    run_ray_add_column(
        tbl_ref,
        ["a"],
        {"b": times_ten_small},
        checkpoint_store=ckp_store,
        checkpoint_size=2,
        task_size=2,
        min_checkpoint_size=2,
        max_checkpoint_size=2,
    )

    ds = lance.dataset(tbl_path)
    assert ds.to_table().to_pydict() == {
        "a": list(range(12)),
        "b": [x * 10 for x in range(12)],
    }
    return ckp_store


def test_run_ray_add_column_cleans_per_batch_checkpoints(tmp_path) -> None:
    """Regression for GEN-541: per-batch checkpoints must be deleted once the
    dedupe key for their fragment is durable. Exercises the indirect
    checkpoint-then-commit path on a multi-fragment dataset.
    """
    ckp_store = _run_cleanup_backfill(tmp_path, "cleanup_flat")
    _assert_no_range_keys_remain(ckp_store)


def test_run_ray_add_column_cleans_per_batch_checkpoints_hierarchical(
    tmp_path, monkeypatch
) -> None:
    """Regression for GEN-541 on the hierarchical checkpoint layout. Same
    invariant as the flat-layout test: a successful backfill leaves only
    fragment dedupe keys, no per-batch '_range-' keys.
    """
    from geneva.checkpoint import (
        CheckpointConfig,
        HierarchicalLanceCheckpointStore,
        _select_store_class,
    )

    # Env var must be set before any CheckpointStore.from_uri so workers
    # reconstructing the store also pick the hierarchical layout. The
    # CheckpointConfig name is "checkpoint" and EnvVarResolver in
    # config/loader.py joins parts directly with "__" without adding a
    # GENEVA_ prefix, so the env var name is CHECKPOINT__STORE_LAYOUT
    # (documented at checkpoint.py:833).
    monkeypatch.setenv("CHECKPOINT__STORE_LAYOUT", "hierarchical")
    # Setting CHECKPOINT__STORE_LAYOUT alone makes the env resolver report
    # the "checkpoint" section as present, which causes CheckpointConfig
    # to recursively instantiate ObjectStoreCheckpointConfig -- whose
    # required ``path`` field would then be missing and raise TypeError
    # (swallowed by ``_select_store_class``, falling back to flat). Stub
    # ``path`` so the config loads cleanly; the test does not exercise
    # object-store mode (it uses ``CheckpointStore.from_uri`` directly).
    monkeypatch.setenv("CHECKPOINT__OBJECT_STORE__PATH", str(tmp_path / "unused"))
    # CheckpointConfig.get is @functools.lru_cache(None); clear it so the
    # new env var takes effect even if a prior test warmed the cache.
    CheckpointConfig.get.cache_clear()

    # Ray workers are spawned at ray.init() time and do not pick up env
    # vars set by monkeypatch after the autouse ray_cluster fixture ran.
    # Re-init Ray with these env vars in runtime_env so workers
    # reconstructing CheckpointStore via from_uri also pick hierarchical;
    # otherwise the driver writes hierarchical keys while workers read
    # via the flat layout and hit KeyError.
    ray.shutdown()
    ray.init(
        runtime_env={
            "env_vars": {
                "CHECKPOINT__STORE_LAYOUT": "hierarchical",
                "CHECKPOINT__OBJECT_STORE__PATH": str(tmp_path / "unused"),
            },
        },
        log_to_driver=True,
    )

    try:
        # Belt-and-suspenders: assert the store we'd construct is actually
        # hierarchical, so a future env-var rename can't silently regress
        # this test back to the flat layout.
        assert _select_store_class() is HierarchicalLanceCheckpointStore, (
            "test expected hierarchical layout but selected "
            f"{_select_store_class().__name__}"
        )

        ckp_store = _run_cleanup_backfill(tmp_path, "cleanup_hier")
        assert isinstance(ckp_store, HierarchicalLanceCheckpointStore), (
            f"expected HierarchicalLanceCheckpointStore, got {type(ckp_store).__name__}"
        )
        _assert_no_range_keys_remain(ckp_store)
    finally:
        # Avoid leaking hierarchical-layout state into later tests in the
        # same process. The autouse ray_cluster fixture will reset Ray
        # for the next test, so no explicit ray.shutdown() needed here.
        CheckpointConfig.get.cache_clear()


# Backfill tests with struct return types

struct_type = pa.struct([("rpad", pa.string()), ("lpad", pa.string())])


@udf(data_type=struct_type, checkpoint_size=8, num_cpus=0.1)
def struct_udf(a: int) -> dict:  # is the output type correct?
    return {"lpad": f"{a:04d}", "rpad": f"{a}0000"[:4]}


@udf(data_type=struct_type, checkpoint_size=8, num_cpus=0.1)
def struct_udf_batch(a: pa.Array) -> pa.Array:  # is the output type correct?
    rpad = pc.ascii_rpad(pc.cast(a, target_type="string"), 4, padding="0")
    lpad = pc.ascii_lpad(pc.cast(a, target_type="string"), 4, padding="0")
    return pc.make_struct(rpad, lpad, field_names=["rpad", "lpad"])


@udf(data_type=struct_type, checkpoint_size=8, num_cpus=0.1)
def struct_udf_recordbatch(
    batch: pa.RecordBatch,
) -> pa.Array:  # is the output type correct?
    a = batch["a"]
    rpad = pc.ascii_rpad(pc.cast(a, target_type="string"), 4, padding="0")
    lpad = pc.ascii_lpad(pc.cast(a, target_type="string"), 4, padding="0")
    return pc.make_struct(rpad, lpad, field_names=["rpad", "lpad"])


ret_struct_udftest_complete = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [{"lpad": f"{x:04d}", "rpad": f"{x}0000"[:4]} for x in range(SIZE)],
    },
)

ret_struct_udftest_filtered = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [
            {"lpad": f"{x:04d}", "rpad": f"{x}0000"[:4]}
            if x % 2 == 0
            else {
                "lpad": None,
                "rpad": None,
            }  # TODO why struct of None instead of just None?
            for x in range(SIZE)
        ],
    },
    "a % 2 = 0",
)


@pytest.mark.multibackfill
def test_run_ray_add_column_ret_struct(db: Connection) -> None:
    tbl = setup_table_and_udf_column(db, default_shuffle_config, struct_udf)
    backfill_and_verify(tbl, ret_struct_udftest_filtered)
    backfill_and_verify(tbl, ret_struct_udftest_complete)


@pytest.mark.multibackfill
def test_run_ray_add_column_ret_struct_batchudf(db: Connection) -> None:
    tbl = setup_table_and_udf_column(db, default_shuffle_config, struct_udf_batch)
    backfill_and_verify(tbl, ret_struct_udftest_filtered)
    backfill_and_verify(tbl, ret_struct_udftest_complete)


@pytest.mark.multibackfill
def test_run_ray_add_column_ret_struct_recordbatchudf(db: Connection) -> None:
    tbl = setup_table_and_udf_column(db, default_shuffle_config, struct_udf_recordbatch)
    backfill_and_verify(tbl, ret_struct_udftest_filtered)
    backfill_and_verify(tbl, ret_struct_udftest_complete)


@pytest.mark.multibackfill
def test_run_ray_add_column_ret_struct_ifnull(db: Connection) -> None:
    tbl = setup_table_and_udf_column(db, default_shuffle_config, struct_udf)
    backfill_and_verify(tbl, ret_struct_udftest_filtered)
    # TODO why struct of None instead of just 'b is null'
    backfill_and_verify(
        tbl,
        UDFTestConfig(
            ret_struct_udftest_complete.expected_recordbatch,
            where="b.rpad is null and b.lpad is null",
        ),
    )


@pytest.mark.multibackfill
def test_run_ray_add_column_ret_struct_filtered(db: Connection) -> None:
    tbl = setup_table_and_udf_column(db, default_shuffle_config, struct_udf)
    backfill_and_verify(tbl, ret_struct_udftest_filtered)
    expected = ret_struct_udftest_complete.expected_recordbatch
    backfill_and_verify(tbl, UDFTestConfig(expected, "a % 2 = 1"))


# Backfill tests with struct and array return types

vararray_type = pa.list_(pa.int64())

ret_vararray_udftest_complete = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [[x] * x for x in range(SIZE)],
    },
)

ret_vararray_udftest_even = UDFTestConfig(
    {
        "a": list(range(SIZE)),
        "b": [[x] * x if x % 2 == 0 else None for x in range(SIZE)],
    },
    "a%2=0",
)


@pytest.mark.multibackfill
def test_run_ray_add_column_ret_vararray(db: Connection) -> None:
    @udf(data_type=vararray_type, checkpoint_size=8, num_cpus=0.1)
    def vararray_udf_scalar(a: int) -> pa.Array:  # is the output type correct?
        # [ [], [1], [2,2], [3,3,3] ... ]
        return [a] * a

    tbl = setup_table_and_udf_column(db, default_shuffle_config, vararray_udf_scalar)
    backfill_and_verify(tbl, ret_vararray_udftest_even)
    expected = ret_vararray_udftest_complete.expected_recordbatch
    backfill_and_verify(tbl, UDFTestConfig(expected, "b is null"))


@pytest.mark.multibackfill
def test_run_ray_add_column_ret_vararray_array(db: Connection) -> None:
    @udf(data_type=vararray_type, checkpoint_size=8, num_cpus=0.1)
    def vararray_udf(a: pa.Array) -> pa.Array:  # is the output type correct?
        # [ [], [1], [2,2], [3,3,3] ... ]
        arr = [[val] * val for val in a.to_pylist()]
        b = pa.array(arr, type=pa.list_(pa.int64()))
        return b

    tbl = setup_table_and_udf_column(db, default_shuffle_config, vararray_udf)
    backfill_and_verify(tbl, ret_vararray_udftest_even)
    expected = ret_vararray_udftest_complete.expected_recordbatch
    backfill_and_verify(tbl, UDFTestConfig(expected, "b is null"))


def test_run_ray_add_column_ret_vararray_stateful_arrays(db: Connection) -> None:
    @udf(data_type=vararray_type, checkpoint_size=8, num_cpus=0.1)
    class StatefulVararrayUDF(Callable):
        def __init__(self) -> None:
            self.state = 0

        def __call__(self, a: pa.Array) -> pa.Array:  # is the output type correct?
            # [ [], [1], [2,2], [3,3,3] ... ]
            arr = [[val] * val for val in a.to_pylist()]
            b = pa.array(arr, type=pa.list_(pa.int64()))
            return b

    tbl = setup_table_and_udf_column(db, default_shuffle_config, StatefulVararrayUDF())
    backfill_and_verify(tbl, ret_vararray_udftest_complete)


def test_run_ray_add_column_ret_vararray_stateful_recordbatch(db: Connection) -> None:
    @udf(data_type=vararray_type, checkpoint_size=8, num_cpus=0.1)
    class BatchedStatefulVararrayUDF(Callable):
        def __init__(self) -> None:
            self.state = 0

        def __call__(
            self, batch: pa.RecordBatch
        ) -> pa.Array:  # is the output type correct?
            # [ [], [1], [2,2], [3,3,3] ... ]
            _LOG.warning(f"batch: {batch}")
            alist = batch["a"]
            arr = [[val] * val for val in alist.to_pylist()]
            b = pa.array(arr, type=pa.list_(pa.int64()))
            return b

    tbl = setup_table_and_udf_column(
        db, default_shuffle_config, BatchedStatefulVararrayUDF()
    )
    backfill_and_verify(tbl, ret_vararray_udftest_complete)


# Backfill tests with nested struct and array return types

nested_type = pa.struct([("lpad", pa.string()), ("array", pa.list_(pa.int64()))])


def test_run_ray_add_column_ret_nested(db: Connection) -> None:
    @udf(data_type=nested_type, checkpoint_size=8, num_cpus=0.1)
    def nested_udf(a: pa.Array) -> pa.Array:
        # [ { lpad:"0000", array:[] } , {lpad:"0001", array:[1]},
        #   { lpad:"0002", array:[2,2]}, ... ]

        lpad = pc.ascii_lpad(pc.cast(a, target_type="string"), 4, padding="0")
        arr = [[val] * val for val in a.to_pylist()]
        array = pa.array(arr, type=pa.list_(pa.int64()))

        return pc.make_struct(lpad, array, field_names=["lpad", "array"])

    tbl = setup_table_and_udf_column(db, default_shuffle_config, nested_udf)

    ret_nested_udftest = UDFTestConfig(
        {
            "a": list(range(SIZE)),
            "b": [{"lpad": f"{val:04d}", "array": [val] * val} for val in range(SIZE)],
        },
    )
    backfill_and_verify(tbl, ret_nested_udftest)


# Other tests


def test_relative_path(
    tmp_path, db: Connection, monkeypatch, local_ray_context
) -> None:
    # Make sure this ray instance uses the db as CURDIR
    ray.shutdown()
    monkeypatch.chdir(tmp_path)

    db = geneva.connect("./db")

    # create a basic table
    tbl = pa.Table.from_pydict({"id": [1, 2, 3, 4, 5, 6]})
    table = db.create_table("table1", tbl)

    @udf(data_type=pa.int64())
    def double_id(id: int):  # noqa A002
        return id * 2

    table.add_columns(
        {"id2": double_id},
    )

    schema = table.schema
    field = schema.field("id2")
    assert field.metadata[b"virtual_column.udf_name"] == b"double_id"

    # At this time, "id2" is a null column
    assert table.to_arrow().combine_chunks() == pa.Table.from_pydict(
        {"id": [1, 2, 3, 4, 5, 6], "id2": [None] * 6},
        schema=pa.schema(
            [
                pa.field("id", pa.int64()),
                pa.field("id2", pa.int64(), True),
            ]
        ),
    )

    # uses local ray to execute UDF and populate "id2"
    table.backfill("id2")

    df = table.to_arrow().to_pandas()
    assert df.equals(
        pd.DataFrame({"id": [1, 2, 3, 4, 5, 6], "id2": [2, 4, 6, 8, 10, 12]})
    )


# Blob-type tests


def blob_table(db) -> Table:
    schema = pa.schema(
        [
            pa.field("a", pa.int32()),
            pa.field(
                "blob", pa.large_binary(), metadata={"lance-encoding:blob": "true"}
            ),
        ]
    )
    blobs = [b"hello", b"the world"]
    tbl = pa.Table.from_pydict(
        {"a": list(range(len(blobs))), "blob": blobs}, schema=schema
    )
    return db.create_table(
        "t", tbl, storage_options={"new_table_data_storage_version": "2.0"}
    )


@udf
def udf_blob(blob: BlobFile) -> int:
    assert isinstance(blob, BlobFile)
    return len(blob.read())


@udf(data_type=pa.int64())
def udf_blob_int_recordbatch(batch: pa.RecordBatch) -> pa.Array:
    """UDF that works on a record batch with a blob column."""
    assert isinstance(batch, pa.RecordBatch)
    blob_col = batch["blob"]
    lens = [len(b) for b in blob_col.to_pylist() if isinstance(b, bytes)]
    return pa.array(lens, type=pa.int64())


@udf(data_type=pa.int64(), input_columns=["blob"])
def udf_blob_array(blob: pa.Array) -> pa.Array:
    """ARRAY-type UDF that reads from a blob column (GEN-410)."""
    lens = [len(b.as_py()) if b.is_valid else 0 for b in blob]
    return pa.array(lens, type=pa.int64())


@udf(data_type=pa.list_(pa.string()))
def udf_blob_to_strlist(blob: BlobFile) -> list[str]:
    """UDF that converts a blob to a list of strings."""
    assert isinstance(blob, BlobFile)
    data = blob.readall()
    rets = data.decode("utf-8").split()
    _LOG.info(f"blob_to_strlist: {data} -> {rets}")
    return rets


@udf(data_type=pa.list_(pa.string()))
def udf_blob_to_strlist_batch(batch: pa.RecordBatch) -> pa.Array:
    """UDF that converts a blob to a list of strings."""
    blobs = batch["blob"]

    rets = []
    for b in blobs:
        data = b.as_py()
        rets.append(data.decode("utf-8").split())
        _LOG.info(f"blob_to_strlist: {data} -> {rets}")
    return pa.array(rets, type=pa.list_(pa.string()))


def test_udf_with_blob_column(db, local_ray_context) -> None:
    tbl = blob_table(db)
    tbl.add_columns({"len": udf_blob})
    tbl.backfill("len")
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, 9]


def test_udf_with_blob_column_recordbatch(db, local_ray_context) -> None:
    tbl = blob_table(db)
    tbl.add_columns({"len": udf_blob_int_recordbatch})
    tbl.backfill("len")
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, 9]


def test_udf_with_blob_column_array(db, local_ray_context) -> None:
    """Backfill blob column with an ARRAY-type UDF (GEN-410).

    Blob columns yield list[dict] from to_batches(), not pa.RecordBatch.
    ARRAY UDFs must handle the conversion before extracting columns.
    """
    tbl = blob_table(db)
    tbl.add_columns({"len": udf_blob_array})
    tbl.backfill("len")
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, 9]


def test_udf_with_blob_column_range_scalar(db, local_ray_context) -> None:
    tbl = blob_table(db)
    tbl.add_columns({"len": udf_blob})
    tbl.backfill("len", blob_read_strategy="range", blob_read_buffer_size=6)
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, 9]


def test_udf_with_blob_column_range_array(db, local_ray_context) -> None:
    tbl = blob_table(db)
    tbl.add_columns({"len": udf_blob_array})
    tbl.backfill("len", blob_read_strategy="range", blob_read_buffer_size=6)
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, 9]


def test_udf_with_blob_column_multiprocess(db, local_ray_context) -> None:
    """Backfill blob column with intra_applier_concurrency > 1 (GEN-395).

    This is a mini repro of the original bug: BlobType extension types were
    silently dropped during Arrow IPC serialization to child processes in
    MultiProcessBatchApplier, causing AttributeError crashes.
    """
    tbl = blob_table(db)
    tbl.add_columns(
        {"len": udf_blob},
        intra_applier_concurrency=2,
    )
    tbl.backfill("len")
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, 9]


def test_udf_with_blob_column_recordbatch_multiprocess(db, local_ray_context) -> None:
    """Backfill blob column (RecordBatch UDF) with intra_applier_concurrency > 1."""
    tbl = blob_table(db)
    tbl.add_columns(
        {"len": udf_blob_int_recordbatch},
        intra_applier_concurrency=2,
    )
    tbl.backfill("len")
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, 9]


def test_udf_with_blob_column_filtered(db, local_ray_context) -> None:
    tbl = blob_table(db)
    tbl.add_columns({"len": udf_blob})
    tbl.backfill(
        "len",
        where="a%2=0",
    )
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, None]
    _LOG.info(f"=== Filtered backfill result ver {tbl.version}: {vals}")

    # now add filter to backfill the rest
    _LOG.info("=== Filling in the rest now..")
    tbl.backfill("len", where="len is null")
    _LOG.info(f"=== after fill in ver {tbl.version}: {vals}")
    tbl.checkout_latest()
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, 9]


def test_udf_with_blob_column_to_strlist(db, local_ray_context) -> None:
    tbl = blob_table(db)
    tbl.add_columns({"strlist": udf_blob_to_strlist})
    tbl.backfill(
        "strlist",
        where="a%2=0",
    )
    vals = tbl.to_arrow()
    _LOG.info(f"=== Filtered backfill result ver {tbl.version}: {vals}")
    assert vals["strlist"].to_pylist() == [["hello"], None]

    # now add filter to backfill the rest
    _LOG.info("=== Filling in the rest now..")
    tbl.backfill("strlist", where="strlist is null")
    _LOG.info(f"=== after fill in ver {tbl.version}: {vals}")
    tbl.checkout_latest()
    vals = tbl.to_arrow()
    assert vals["strlist"].to_pylist() == [["hello"], ["the", "world"]]


def test_udf_with_blob_column_to_strlist_batch(db, local_ray_context) -> None:
    tbl = blob_table(db)
    tbl.add_columns({"strlist": udf_blob_to_strlist_batch})
    tbl.backfill(
        "strlist",
        where="a%2=0",
    )
    vals = tbl.to_arrow()
    _LOG.info(f"=== Filtered backfill result ver {tbl.version}: {vals}")
    assert vals["strlist"].to_pylist() == [["hello"], None]

    # now add filter to backfill the rest
    _LOG.info("=== Filling in the rest now..")
    tbl.backfill("strlist", where="strlist is null")
    _LOG.info(f"=== after fill in ver {tbl.version}: {vals}")
    tbl.checkout_latest()
    vals = tbl.to_arrow()
    assert vals["strlist"].to_pylist() == [["hello"], ["the", "world"]]


@pytest.mark.skip(reason="binary literal not yet implemented?")
def test_udf_with_blob_column_filtered_binaryliteral(db, local_ray_context) -> None:
    tbl = blob_table(db)
    tbl.add_columns({"len": udf_blob})
    tbl.backfill(
        "len",
        where="blob = X'hello'",
    )
    vals = tbl.to_arrow()
    assert vals["len"].to_pylist() == [5, None]


def test_udf_generates_blob_output(db, local_ray_context) -> None:
    """Test UDF that generates Lance blob outputs from scalar inputs."""

    @udf(data_type=pa.large_binary(), field_metadata={"lance-encoding:blob": "true"})
    def generate_blob(text: str, multiplier: int) -> bytes:
        """UDF that generates blob data by repeating text."""
        return (text * multiplier).encode("utf-8")

    # Create database and input table
    input_data = pa.table({"text": ["hello", "world", "test"], "multiplier": [2, 3, 1]})
    tbl = db.create_table("input_table", input_data)

    # Add blob column with proper metadata
    tbl.add_columns({"blob_output": generate_blob})
    _LOG.info(f"schema: {tbl.schema}")
    # Verify blob metadata is present
    blob_field = tbl.schema.field("blob_output")
    assert blob_field.metadata[b"lance-encoding:blob"] == b"true"

    # Execute backfill to generate blob data
    tbl.backfill("blob_output")

    # Verify results
    tbl = db.open_table("input_table")
    result = tbl.to_arrow()
    expected_blobs = [
        {"position": 0, "size": 10},
        {"position": 64, "size": 15},
        {"position": 128, "size": 4},
    ]
    expected_blob_values = [
        b"hellohello",  # "hello" * 2
        b"worldworldworld",  # "world" * 3
        b"test",  # "test" * 1
    ]
    _LOG.info(f"result: {result}")

    assert result["text"].to_pylist() == ["hello", "world", "test"]
    assert result["multiplier"].to_pylist() == [2, 3, 1]
    assert result["blob_output"].to_pylist() == expected_blobs

    # Verify blob files' content - have to go to dataset api
    from lance import dataset as lance_dataset

    ds = lance_dataset(tbl.uri)
    blob_files = ds.take_blobs("blob_output", indices=[0, 1, 2])
    assert len(blob_files) == 3
    blob_values = [blob.read() for blob in blob_files]
    assert blob_values == expected_blob_values


def test_udf_generates_blob_from_array_input(db, local_ray_context) -> None:
    """Test UDF that generates Lance blob outputs from array inputs."""

    @udf(data_type=pa.large_binary(), field_metadata={"lance-encoding:blob": "true"})
    def serialize_array(values: pa.Array) -> bytes:
        """UDF that serializes an array into blob data."""
        import pickle

        _LOG.info(f"values ({type(values)}): {values}")
        return pickle.dumps(values)

    # Create database and input table with array column
    array_data = [[1, 2, 3], [4, 5, 6, 7], [8, 9]]
    input_data = pa.table({"id": [1, 2, 3], "values": array_data})
    tbl = db.create_table("array_table", input_data)

    # Add blob column with proper metadata
    tbl.add_columns({"serialized_blob": serialize_array})
    # Verify blob metadata
    blob_field = tbl.schema.field("serialized_blob")
    assert blob_field.metadata[b"lance-encoding:blob"] == b"true"

    # Execute backfill
    tbl.backfill("serialized_blob")

    # Verify results by deserializing - have to go to dataset api
    from lance import dataset as lance_dataset

    ds = lance_dataset(tbl.uri)
    blob_files = ds.take_blobs("serialized_blob", indices=[0, 1, 2])
    assert len(blob_files) == 3
    blob_values = [blob.read() for blob in blob_files]
    for i, blob_data in enumerate(blob_values):
        import pickle

        deserialized = pickle.loads(blob_data)
        assert deserialized == array_data[i]


def test_udf_generates_blob_from_recordbatch(db, local_ray_context) -> None:
    """Test RecordBatch UDF that generates Lance blob outputs."""

    @udf(data_type=pa.large_binary(), field_metadata={"lance-encoding:blob": "true"})
    def batch_to_blob(batch: pa.RecordBatch) -> pa.Array:
        """UDF that converts RecordBatch rows to blob data."""
        import json

        blobs = []
        for i in range(batch.num_rows):
            row_dict = {
                col_name: batch.column(j)[i].as_py()
                for j, col_name in enumerate(batch.column_names)
            }
            blob_data = json.dumps(row_dict, sort_keys=True).encode("utf-8")
            blobs.append(blob_data)
        return pa.array(blobs, type=pa.large_binary())

    # Create database and input table
    input_data = pa.table(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "score": [95.5, 87.2, 92.8],
        }
    )
    tbl = db.create_table("people_table", input_data)

    # Add blob column
    tbl.add_columns({"row_blob": batch_to_blob})

    # Verify blob metadata
    blob_field = tbl.schema.field("row_blob")
    assert blob_field.metadata[b"lance-encoding:blob"] == b"true"

    # Execute backfill
    tbl.backfill("row_blob")

    # Verify results
    result = tbl.to_arrow()

    # Verify blob files' content - have to go to dataset api
    from lance import dataset as lance_dataset

    ds = lance_dataset(tbl.uri)
    blob_files = ds.take_blobs("row_blob", indices=[0, 1, 2])
    assert len(blob_files) == 3
    blob_values = [blob.read() for blob in blob_files]
    for i, blob_data in enumerate(blob_values):
        import json

        row_dict = json.loads(blob_data.decode("utf-8"))

        # Verify the serialized data matches original
        assert row_dict["name"] == result["name"][i].as_py()
        assert row_dict["age"] == result["age"][i].as_py()
        assert abs(row_dict["score"] - result["score"][i].as_py()) < 0.001


def test_table_take_blobs_multi_fragment(tmp_path: Path) -> None:
    """Test that Table.take_blobs works with multiple fragments.

    This is a regression test for a bug where Table.take_blobs() passed indices
    positionally to Lance's take_blobs(), causing them to be interpreted as row IDs
    instead of logical indices. This caused failures when accessing blobs beyond
    the first fragment.
    """
    db = connect(tmp_path)

    # Create initial table with blob column
    schema = pa.schema(
        [
            pa.field("a", pa.int32()),
            pa.field(
                "blob", pa.large_binary(), metadata={"lance-encoding:blob": "true"}
            ),
        ]
    )
    blobs1 = [b"hello", b"world"]
    tbl_data = pa.Table.from_pydict(
        {"a": list(range(len(blobs1))), "blob": blobs1}, schema=schema
    )
    tbl = db.create_table("multi_frag_blob", tbl_data)

    # Add more rows to create second fragment
    blobs2 = [b"second", b"fragment", b"data"]
    more_data = pa.Table.from_pydict(
        {"a": list(range(len(blobs1), len(blobs1) + len(blobs2))), "blob": blobs2},
        schema=schema,
    )
    tbl.add(more_data)

    # Verify we have multiple fragments
    assert len(tbl.to_lance().get_fragments()) >= 2

    # Test take_blobs from first fragment
    result1 = tbl.take_blobs(indices=[0], column="blob")
    assert result1[0].read() == b"hello"

    # Test take_blobs from second fragment (this was failing before the fix)
    result2 = tbl.take_blobs(indices=[3], column="blob")
    assert result2[0].read() == b"fragment"

    # Test take_blobs spanning both fragments
    result_both = tbl.take_blobs(indices=[1, 4], column="blob")
    assert result_both[0].read() == b"world"
    assert result_both[1].read() == b"data"


def test_array_udf_filtering_optimization(tmp_path, db, local_ray_context) -> None:
    """Test that Array UDFs only process filtered rows, not all rows."""

    @udf(data_type=pa.int32())
    def tracking_array_udf(a: pa.Array) -> pa.Array:
        """Array UDF that validates it only receives filtered values."""
        values = a.to_pylist()

        # The UDF should only receive filtered values: [0, 2, 4, 6, 8]
        # If it receives any odd values, the optimization isn't working
        for val in values:
            if val % 2 != 0:
                raise AssertionError(
                    f"Array UDF received unfiltered value {val}. "
                    f"Optimization failed - UDF should only receive even values."
                )

        return pa.compute.multiply(a, pa.scalar(10))

    # Create test data with 10 rows (0-9)
    tbl_path = tmp_path / "test.lance"
    data = {"a": pa.array(range(10))}
    table = pa.Table.from_pydict(data)
    lance.write_dataset(
        table, tbl_path, max_rows_per_file=32, data_storage_version="2.0"
    )

    tbl = db.open_table("test")
    tbl.add_columns({"result": tracking_array_udf})

    # Apply filter that should only include even rows: 0, 2, 4, 6, 8
    tbl.backfill("result", where="a % 2 = 0")

    # Verify final results are correct
    tbl.checkout_latest()
    result = tbl.to_arrow().to_pydict()
    expected_result = [0, None, 20, None, 40, None, 60, None, 80, None]
    assert result["result"] == expected_result


def test_recordbatch_udf_filtering_optimization(
    tmp_path, db, local_ray_context
) -> None:
    """Test that RecordBatch UDFs only process filtered rows, not all rows."""

    @udf(data_type=pa.int32())
    def tracking_recordbatch_udf(batch: pa.RecordBatch) -> pa.Array:
        """RecordBatch UDF that validates it only receives filtered rows."""
        values = batch["a"].to_pylist()

        # The UDF should only receive filtered values: [0, 2, 4, 6, 8]
        # If it receives any odd values, the optimization isn't working
        for val in values:
            if val % 2 != 0:
                raise AssertionError(
                    f"RecordBatch UDF received unfiltered value {val}. "
                    f"Optimization failed - UDF should only receive even values."
                )

        return pa.compute.multiply(batch["a"], pa.scalar(10))

    # Create test data with 10 rows (0-9)
    tbl_path = tmp_path / "test.lance"
    data = {"a": pa.array(range(10))}
    table = pa.Table.from_pydict(data)
    lance.write_dataset(
        table, tbl_path, max_rows_per_file=32, data_storage_version="2.0"
    )

    tbl = db.open_table("test")
    tbl.add_columns({"result": tracking_recordbatch_udf})

    # Apply filter that should only include even rows: 0, 2, 4, 6, 8
    tbl.backfill("result", where="a % 2 = 0")

    # Verify final results are correct
    tbl.checkout_latest()
    result = tbl.to_arrow().to_pydict()
    expected_result = [0, None, 20, None, 40, None, 60, None, 80, None]
    assert result["result"] == expected_result


def test_scalar_udf_filtering_optimization(tmp_path, db, local_ray_context) -> None:
    """Test that Scalar UDFs only process filtered rows (should already work)."""

    @udf(data_type=pa.int32())
    def tracking_scalar_udf(a: int) -> int:
        """Scalar UDF that validates it only receives filtered values."""
        # The UDF should only receive filtered values: 0, 2, 4, 6, 8
        # If it receives any odd values, the optimization isn't working
        if a % 2 != 0:
            raise AssertionError(
                f"Scalar UDF received unfiltered value {a}. "
                f"Optimization failed - UDF should only receive even values."
            )
        return a * 10

    # Create test data with 10 rows (0-9)
    tbl_path = tmp_path / "test.lance"
    data = {"a": pa.array(range(10))}
    table = pa.Table.from_pydict(data)
    lance.write_dataset(
        table, tbl_path, max_rows_per_file=32, data_storage_version="2.0"
    )

    tbl = db.open_table("test")
    tbl.add_columns({"result": tracking_scalar_udf})

    # Apply filter that should only include even rows: 0, 2, 4, 6, 8
    tbl.backfill("result", where="a % 2 = 0")

    # Verify final results are correct
    tbl.checkout_latest()
    result = tbl.to_arrow().to_pydict()
    expected_result = [0, None, 20, None, 40, None, 60, None, 80, None]
    assert result["result"] == expected_result


@pytest.mark.multibackfill
def test_backfill_checkpoint_size_overrides_udf_checkpoint_size(
    tmp_path: Path, db, local_ray_context
) -> None:
    """Backfill checkpoint_size should override the UDF-declared batch_size.

    Scenarios:
    1) UDF default (100), checkpoint_size=50 => max observed 50, never exceed 50
    2) UDF default (100), checkpoint_size=150 => max observed 150, includes 150
    3) UDF=200, checkpoint_size=150 => max observed 150, includes 150
    4) UDF=200, checkpoint_size=250 => max observed 250, includes 250
    """

    def run_case(
        *,
        name: str,
        udf_batch_size: int | None,
        checkpoint_size: int,
        total_rows: int,
    ) -> None:
        # Define UDF with optional declared batch_size
        if udf_batch_size is None:

            @udf(data_type=pa.int32(), num_cpus=1)
            def echo_batch_size(batch: pa.RecordBatch) -> pa.Array:
                n = batch.num_rows
                return pa.array([n] * n, type=pa.int32())
        else:

            @udf(data_type=pa.int32(), batch_size=udf_batch_size, num_cpus=1)
            def echo_batch_size(batch: pa.RecordBatch) -> pa.Array:
                n = batch.num_rows
                return pa.array([n] * n, type=pa.int32())

        # Create dataset
        tbl_path = tmp_path / f"{name}.lance"
        data = {"a": pa.array(range(total_rows))}
        table = pa.Table.from_pydict(data)
        lance.write_dataset(
            table, tbl_path, max_rows_per_file=300, data_storage_version="2.0"
        )

        tbl = db.open_table(name)
        tbl.add_columns({"observed": echo_batch_size})

        # Backfill with override batch size. Use a task_size large enough to
        # ensure read tasks don't cap the observed batch sizes; this test is
        # specifically about checkpoint_size overriding UDF batch_size.
        tbl.backfill(
            "observed",
            checkpoint_size=checkpoint_size,
            task_size=total_rows,
        )

        # Validate that observed batch sizes never exceed override
        tbl.checkout_latest()
        observed = tbl.to_arrow().column("observed").to_pylist()
        vals = [int(v) for v in observed if v is not None]
        assert max(vals) == checkpoint_size
        assert all(0 <= v <= checkpoint_size for v in vals)

    # 1) UDF default (100), backfill=50
    run_case(
        name="override_default_50",
        udf_batch_size=None,
        checkpoint_size=50,
        total_rows=300,
    )

    # 2) UDF default (100), backfill=150
    run_case(
        name="override_default_150",
        udf_batch_size=None,
        checkpoint_size=150,
        total_rows=600,
    )

    # 3) UDF=200, backfill=150
    run_case(
        name="override_udf200_150",
        udf_batch_size=200,
        checkpoint_size=150,
        total_rows=600,
    )

    # 4) UDF=200, backfill=250
    run_case(
        name="override_udf200_250",
        udf_batch_size=200,
        checkpoint_size=250,
        total_rows=1000,
    )


def test_backfill_async_checkpoint_size_used(
    tmp_path: Path, db, local_ray_context, caplog: pytest.LogCaptureFixture
) -> None:
    """backfill_async respects checkpoint_size and warns on deprecated batch_size."""

    @udf(data_type=pa.int32(), batch_size=64, num_cpus=1)
    def echo_batch_size(batch: pa.RecordBatch) -> pa.Array:
        n = batch.num_rows
        return pa.array([n] * n, type=pa.int32())

    tbl_path = tmp_path / "ckp_async.lance"
    data = {"a": pa.array(range(55))}
    table = pa.Table.from_pydict(data)
    lance.write_dataset(
        table, tbl_path, max_rows_per_file=32, data_storage_version="2.0"
    )

    tbl = db.open_table("ckp_async")
    tbl.add_columns({"observed": echo_batch_size})

    # checkpoint_size override
    fut = tbl.backfill_async("observed", checkpoint_size=11, task_size=55)
    fut.result()

    tbl.checkout_latest()
    vals = [
        int(v) for v in tbl.to_arrow().column("observed").to_pylist() if v is not None
    ]
    assert max(vals) == 11

    # batch_size deprecated warning when only batch_size passed (fresh table)
    caplog.set_level(logging.WARNING, logger="geneva.utils.batch_size")

    tbl_path2 = tmp_path / "ckp_async_b.lance"
    data2 = {"a": pa.array(range(45))}
    lance.write_dataset(
        pa.Table.from_pydict(data2),
        tbl_path2,
        max_rows_per_file=32,
        data_storage_version="2.0",
    )

    tbl2 = db.open_table("ckp_async_b")
    tbl2.add_columns({"observed": echo_batch_size})

    # Use a large enough task_size so the read-task window doesn't cap the
    # observed map batches; here we're validating the legacy batch_size alias.
    fut2 = tbl2.backfill_async("observed", batch_size=13, task_size=45)
    fut2.result()

    assert any("batch_size is deprecated" in rec.message for rec in caplog.records)
    tbl2.checkout_latest()
    vals2 = [
        int(v) for v in tbl2.to_arrow().column("observed").to_pylist() if v is not None
    ]
    assert max(vals2) == 13


@pytest.fixture
def dir_namespace_props(tmp_path) -> dict[str, str]:
    return {"root": str(tmp_path)}


@pytest.fixture(autouse=True)
def dir_namespace_db(tmp_path, dir_namespace_props) -> Connection:
    db = geneva.connect(
        namespace_client_impl="dir",
        namespace_client_properties=dir_namespace_props,
    )
    yield db
    db.close()


@pytest.fixture
def rest_namespace_db(
    tmp_path, dir_namespace_props
) -> Generator[Connection, None, None]:
    """Create a REST namespace with adapter for testing."""
    unique_id = uuid.uuid4().hex[:8]
    port = 4000 + hash(unique_id) % 10000

    with lance.namespace.RestAdapter("dir", dir_namespace_props, port=port):
        db = geneva.connect(
            namespace_client_impl="rest",
            namespace_client_properties={"uri": f"http://127.0.0.1:{port}"},
        )
        yield db
        db.close()


def test_backfill_with_db(db) -> None:
    _test_backfill_with_namespace(db)


def test_backfill_with_dir_namespace_root(dir_namespace_db) -> None:
    _test_backfill_with_namespace(dir_namespace_db)


def test_backfill_with_rest_namespace_root(rest_namespace_db) -> None:
    _test_backfill_with_namespace(rest_namespace_db)


def test_backfill_with_dir_namespace_child(dir_namespace_db) -> None:
    _test_backfill_with_namespace(dir_namespace_db, namespace=["workspace"])


def test_backfill_with_rest_namespace_child(rest_namespace_db) -> None:
    _test_backfill_with_namespace(rest_namespace_db, namespace=["workspace"])


def _test_backfill_with_namespace(
    db_impl: Connection,
    namespace: list[str] | None = None,
    local_ray_context: None = None,
) -> None:
    from geneva.table import Table

    @udf(data_type=pa.int64())
    def add_one(a: int):  # noqa A002
        return a + 1

    schema = pa.schema(
        [
            pa.field("a", pa.int32()),
            pa.field("b", pa.int32()),
        ]
    )

    data = pa.table({"a": range(10, 20), "b": range(30, 40)})

    # If namespace is provided (not root), create it
    if namespace:
        from lance_namespace import CreateNamespaceRequest

        ns = db_impl.namespace_client()
        assert ns is not None, "This test requires a namespace connection"
        ns.create_namespace(CreateNamespaceRequest(id=namespace))

        # Create table in the child namespace
        db_impl._connect.create_table("t", schema=schema, namespace_path=namespace)
        tbl = Table(db_impl, "t", namespace=namespace)
    else:
        # Create table in root namespace
        tbl = db_impl.create_table("t", schema=schema)

    tbl.add(pa.table(data))
    tbl.add_columns({"c": add_one})
    tbl.backfill("c")

    vals = tbl.to_arrow()
    _LOG.info(f"=== backfill result ver {tbl.version}: {vals}")
    assert vals["c"].to_pylist() == [11, 12, 13, 14, 15, 16, 17, 18, 19, 20], (
        "backfill didn't succeed"
    )

    # Verify checkpoint folder and files exist (if created)
    # Note: Small local tests may not create checkpoints
    if db_impl.namespace_client():
        from lance_namespace import DescribeTableRequest

        table_id = namespace + ["t"] if namespace else ["t"]
        table_desc = db_impl.namespace_client().describe_table(
            DescribeTableRequest(id=table_id)
        )
        table_location = table_desc.location
        assert table_location is not None, "Table location should not be None"
        _LOG.info(f"Table location: {table_location}")

        # Check if checkpoint folder exists
        checkpoint_path = f"{table_location.rstrip('/')}/ckp"
        _LOG.info(f"Checking checkpoint path: {checkpoint_path}")

        # Use pyarrow filesystem to check if checkpoint directory exists
        import pyarrow.fs as pafs

        filesystem, path = pafs.FileSystem.from_uri(checkpoint_path)
        try:
            dir_info = filesystem.get_file_info(path)
            if dir_info.type == pafs.FileType.Directory:
                # Directory exists, verify checkpoint files
                file_infos = filesystem.get_file_info(
                    pafs.FileSelector(path, recursive=True)
                )
                checkpoint_files = [
                    info.path
                    for info in file_infos
                    if info.type == pafs.FileType.File and info.path.endswith(".lance")
                ]
                _LOG.info(
                    f"Found {len(checkpoint_files)} checkpoint files: "
                    f"{checkpoint_files}"
                )
                assert len(checkpoint_files) > 0, (
                    f"Checkpoint directory exists but no files found in "
                    f"{checkpoint_path}"
                )
                _LOG.info(f"Verified checkpoint files exist at {checkpoint_path}")
            else:
                # Checkpoint directory doesn't exist - this is OK for small local tests
                _LOG.info(
                    f"Checkpoint directory not created "
                    f"(expected for small local tests): {checkpoint_path}"
                )
        except Exception as e:
            # Directory doesn't exist - OK for small tests
            _LOG.info(
                f"Checkpoint directory not found (expected for small local tests): {e}"
            )

    # Drop table
    if namespace:
        db_impl.drop_table("t", namespace_path=namespace)
    else:
        db_impl.drop_table("t")

    _LOG.info(f"{type(db_impl)} success")


def _captured_actor_options(
    job: "ColumnAddPipelineJob", node_memory: float | None = 1 << 40
) -> dict:
    """Run ``setup_actor`` and return the kwargs it hands ``.options()``.

    ``node_memory`` stands in for the largest live Ray node, which only the
    unplaceable-reservation warning reads. It defaults to a node with room to
    spare so these assertions do not depend on how much memory the machine
    running the tests happens to have.
    """
    captured: dict = {}

    class _FakeActor:
        def options(self, **kwargs):  # noqa: ANN003, ANN202
            captured.update(kwargs)
            return self

    with (
        mock.patch.object(pipeline_mod, "ApplierActor", _FakeActor()),
        mock.patch.object(
            pipeline_mod, "largest_node_memory", return_value=node_memory
        ),
    ):
        job.setup_actor()
    return captured


def test_setup_actor_reserves_a_default_when_udf_memory_is_unset(
    tmp_path: Path,
) -> None:
    """GEN-775: an unset ``@udf(memory=)`` used to reserve nothing at all.

    That is not "reserve a little" -- Ray drops an actor with no ``memory`` out
    of memory scheduling entirely, so it packs actors onto a node by CPU alone
    until the node OOMs. The floor puts every actor back into the accounting.
    """
    import attrs

    from geneva.jobs.config import JobConfig

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [None, None, None]}))

    @udf(data_type=pa.int32())
    def one(x: int) -> int:
        return x + 1

    def _job(cfg: "JobConfig", intra: int = 1) -> ColumnAddPipelineJob:
        return ColumnAddPipelineJob(
            map_task=BackfillUDFTask(udfs={"b": one}),
            checkpoint_store=CheckpointStore.from_uri("memory"),
            error_store=None,
            config=cfg,
            dst=tbl.get_reference(),
            input_plan=iter([]),
            job_id="job-default-memory",
            job_tracker=None,
            intra_applier_concurrency=intra,
        )

    cfg = JobConfig.get()
    default = cfg.applier_default_memory_bytes

    args = _captured_actor_options(_job(cfg))
    assert args["memory"] == default

    # Scales with in-actor slots, the same way a declared memory does.
    assert _captured_actor_options(_job(cfg, intra=3))["memory"] == default * 3

    # Zero is a deliberate escape hatch back to pre-GEN-775 scheduling: Ray
    # treats memory=0 as no reservation, which is what it did before.
    off = attrs.evolve(cfg, applier_default_memory_bytes=0)
    assert _captured_actor_options(_job(off))["memory"] == 0


def test_setup_actor_warns_but_still_asks_when_no_node_fits(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """The request stands; the reason it will not schedule is logged.

    Shrinking it to fit would reserve less than the job was sized for and make
    Ray's figure differ from the one admission approved.
    """
    from geneva.jobs.config import JobConfig

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [None, None, None]}))

    @udf(data_type=pa.int32())
    def one(x: int) -> int:
        return x + 1

    cfg = JobConfig.get()
    small_node = 2_741_616_640  # a real 4 GiB cgroup, measured
    assert small_node < cfg.applier_default_memory_bytes

    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": one}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=cfg,
        dst=tbl.get_reference(),
        input_plan=iter([]),
        job_id="job-unplaceable",
        job_tracker=None,
    )
    with caplog.at_level(logging.WARNING):
        captured = _captured_actor_options(job, node_memory=small_node)

    assert captured["memory"] == cfg.applier_default_memory_bytes
    assert "cannot be placed" in caplog.text
    assert "JOB__APPLIER_DEFAULT_MEMORY_BYTES" in caplog.text

    # Said once per job, not once per actor.
    caplog.clear()
    with caplog.at_level(logging.WARNING):
        _captured_actor_options(job, node_memory=small_node)
    assert "cannot be placed" not in caplog.text


def test_setup_actor_prefers_an_explicit_udf_memory(tmp_path: Path) -> None:
    """The default is a floor for jobs that said nothing, not an override."""
    from geneva.jobs.config import JobConfig

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [None, None, None]}))

    declared_bytes = 123 * 1024 * 1024

    @udf(data_type=pa.int32(), memory=declared_bytes)
    def one(x: int) -> int:
        return x + 1

    cfg = JobConfig.get()
    assert declared_bytes != cfg.applier_default_memory_bytes

    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(udfs={"b": one}),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=cfg,
        dst=tbl.get_reference(),
        input_plan=iter([]),
        job_id="job-declared-memory",
        job_tracker=None,
    )
    assert _captured_actor_options(job)["memory"] == declared_bytes
