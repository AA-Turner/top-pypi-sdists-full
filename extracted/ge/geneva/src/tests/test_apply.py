# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import hashlib
import json
import logging
import threading
import time
from collections import Counter
from collections.abc import Iterator
from concurrent.futures import Future
from itertools import islice
from pathlib import Path
from typing import Any, NamedTuple, NoReturn

import lance
import pyarrow as pa
import pyarrow.compute as pc
import pytest
from lance.blob import BlobArray, BlobType
from yarl import URL

import geneva.apply as apply_module
import geneva.runners.ray.pipeline as pipeline_module
from geneva import CheckpointStore, Columns, connect, udf
from geneva.apply import (
    CheckpointingApplier,
    DirectFragmentWriteConfig,
    DirectFragmentWriteResult,
    MapBatchCheckpoint,
    _check_fragment_data_file_exists,
    _find_output_data_file_in_fragment,
    _legacy_fragment_dedupe_key,
    plan_read,
)
from geneva.apply.applier import BatchApplier
from geneva.apply.blob_range import InMemoryBlobFile
from geneva.apply.multiprocess import (
    _LIST_DICT_MARKER,
    MultiProcessBatchApplier,
    _batch_to_buf,
    _buf_to_batch,
    _picklable_worker_error,
    _restore_extension_types,
    _strip_extension_types,
)
from geneva.apply.task import (
    DEFAULT_CHECKPOINT_ROWS,
    BackfillUDFTask,
    ReadTask,
    ScanTask,
)
from geneva.apply.utils import (
    _compute_resume_ranges,
    _index_checkpoint_ranges,
    _parse_checkpoint_range_key,
)
from geneva.checkpoint import (
    CheckpointConfig,
    FlatLanceCheckpointStore,
    HierarchicalLanceCheckpointStore,
    InMemoryCheckpointStore,
    _parse_udf_version_from_fragment_checkpoint_key,
)
from geneva.checkpoint_utils import hash_source_files, hash_string
from geneva.debug.error_store import ErrorStore
from geneva.debug.logger import TableErrorLogger
from geneva.jobs.config import JobConfig
from geneva.runners.ray.jobtracker import (
    METRIC_CHECKPOINT_FRAGMENT_WRITES,
    METRIC_DIRECT_FRAGMENT_WRITES,
)
from geneva.runners.ray.pipeline import (
    ColumnAddPipelineJob,
    FragmentWriterManager,
    _get_fragment_dedupe_key,
    _get_relevant_field_ids,
    get_source_data_files,
)
from geneva.runners.ray.writer import FragmentWriteFailedError, FragmentWriter
from geneva.table import TableReference
from geneva.transformer import BACKFILL_SELECTED, UnpackedUDF
from geneva.utils.object_store_retry import is_retryable_object_store_error
from geneva.utils.parse_rust_debug import (
    extract_field_ids,
    extract_field_ids_and_column_indices,
)

_LOG = logging.getLogger(__name__)


@pytest.fixture
def tbl_ref(tmp_path) -> TableReference:
    return TableReference(table_id=["tbl"], version=None, db_uri=str(tmp_path))


class _NoopRemote:
    def remote(self, *args: object, **kwargs: object) -> None:
        return None


class _NoopJobTracker:
    def __init__(self) -> None:
        self.increment = _NoopRemote()
        self.batch_increment = _NoopRemote()
        self.set_total = _NoopRemote()
        self.set_desc = _NoopRemote()
        self.mark_done = _NoopRemote()


class _RecorderRemote:
    def __init__(self) -> None:
        self.calls: list[tuple[object, ...]] = []

    def remote(self, *args: object, **kwargs: object) -> None:
        self.calls.append((*args, kwargs))


class _RecordingJobTracker:
    def __init__(self) -> None:
        self.increment = _RecorderRemote()
        self.batch_increment = _RecorderRemote()
        self.set = _RecorderRemote()
        self.set_total = _RecorderRemote()
        self.set_desc = _RecorderRemote()
        self.mark_done = _RecorderRemote()


class _DummyMapTask:
    def checkpoint_prefix(
        self,
        *,
        dataset_uri: str,
        where: str | None = None,
        column: str | None = None,
        src_files_hash: str | None = None,
    ) -> str:
        return "dummy"

    def name(self) -> str:
        return "dummy"

    def output_schema(self) -> pa.Schema:
        return pa.schema([pa.field("one", pa.int64())])


class _DummyWriterSession:
    failed = False
    failure_reason = None

    def __init__(
        self,
        *,
        sealed: bool,
        inflight: dict[object, int] | None = None,
        failed: bool = False,
        failure_reason: str | None = None,
    ) -> None:
        self.sealed = sealed
        self.inflight = inflight or {}
        self.failed = failed
        self.failure_reason = failure_reason
        self.cached_tasks: list[tuple[int, str, int]] = []
        self.seal_calls = 0
        self.drain_calls = 0
        self.check_seal_ack_calls = 0
        self.shutdown_force_values: list[bool] = []

    def seal(self) -> None:
        self.seal_calls += 1
        self.sealed = True

    def check_seal_ack(self) -> None:
        self.check_seal_ack_calls += 1

    def drain(self) -> Iterator[Any]:
        self.drain_calls += 1
        return iter(())

    def shutdown(self, *, force_queue: bool = False) -> None:
        self.shutdown_force_values.append(force_queue)


def _make_fragment_writer_manager() -> FragmentWriterManager:
    return FragmentWriterManager(
        dst_read_version=7,
        ds_uri="memory:///dst.lance",
        job_tracker=None,
        map_task=_DummyMapTask(),
        checkpoint_store=object(),  # type: ignore[arg-type]
        where=None,
        commit_granularity=999,
        expected_tasks={},
        skipped_fragments={},
    )


class _DummyReadTask(ReadTask):
    def __init__(
        self,
        *,
        frag_id: int,
        rows: int,
        offset: int = 0,
        table_uri: str = "memory://dummy",
        batches: list[pa.RecordBatch] | None = None,
    ) -> None:
        self._frag_id = frag_id
        self._rows = rows
        self._offset = offset
        self._table_uri = table_uri
        self._batches = batches or []

    def to_batches(
        self, *, batch_size=DEFAULT_CHECKPOINT_ROWS
    ) -> Iterator[pa.RecordBatch]:
        yield from self._batches

    def checkpoint_key(self) -> str:
        return f"dummy-{self._frag_id}-{self._offset}-{self._rows}"

    def dest_frag_id(self) -> int:
        return self._frag_id

    def dest_offset(self) -> int:
        return self._offset

    def num_rows(self) -> int:
        return self._rows

    def table_uri(self) -> str:
        return self._table_uri


class _NoPayloadReadFlatLanceCheckpointStore(FlatLanceCheckpointStore):
    def __getitem__(self, item: str) -> pa.RecordBatch:
        raise AssertionError(f"checkpoint payload read for {item}")


class _NoPayloadReadHierarchicalLanceCheckpointStore(HierarchicalLanceCheckpointStore):
    def __getitem__(self, item: str) -> pa.RecordBatch:
        raise AssertionError(f"checkpoint payload read for {item}")


def _src_files_hash_for_cols(tbl, cols: list[str]) -> str:
    dataset = tbl.to_lance()
    relevant_field_ids = _get_relevant_field_ids(dataset, cols)
    frag = dataset.get_fragment(0)
    return hash_source_files(get_source_data_files(frag, relevant_field_ids))


def _direct_write_config(tbl, *output_columns: str) -> DirectFragmentWriteConfig:
    dataset = tbl.to_lance()
    field_ids, column_indices = extract_field_ids_and_column_indices(
        dataset.lance_schema,
        list(output_columns),
        dataset.data_storage_version,
    )
    output_field_ids = set(field_ids)
    db_uri = dataset.uri.rsplit("/", 1)[0]
    return DirectFragmentWriteConfig(
        ds_uri=dataset.uri,
        column_names=list(output_columns),
        field_ids=field_ids,
        column_indices=column_indices,
        data_storage_version=dataset.data_storage_version,
        output_field_ids=frozenset(output_field_ids),
        read_version=dataset.version,
        namespace_impl="dir",
        namespace_properties={"root": db_uri},
        table_id=[tbl.name],
    )


class _NoPlannerCheckpointProbeStore(InMemoryCheckpointStore):
    def __contains__(self, item: str) -> bool:
        raise AssertionError(f"planner should not probe checkpoint key {item}")

    def list_keys(self, prefix: str = "") -> Iterator[str]:
        raise AssertionError(f"planner should not list checkpoint prefix {prefix}")


def test_create_plan(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    plans = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=16)[0])
    assert len(plans) == 1
    plan = plans[0]
    assert plan.uri == tbl.uri
    assert plan.offset == 0
    assert plan.limit == 3


def test_unpacked_udf_task_writes_sibling_columns() -> None:
    class Pair(NamedTuple):
        left: int
        right: int

    @udf
    def pair(a: int) -> Columns[Pair]:
        return Pair(a + 1, a + 2)

    unpacked = UnpackedUDF(pair)
    task = BackfillUDFTask(
        {"left": pair},
        unpack_fields=unpacked.fields,
        checkpoint_column="left",
    )
    batch = pa.record_batch(
        [
            pa.array([10, 20], type=pa.int64()),
            pa.array([0, 1], type=pa.uint64()),
        ],
        names=["a", "_rowaddr"],
    )

    output = task.apply(batch)

    assert output.schema.names == ["left", "right", "_rowaddr"]
    assert output["left"].to_pylist() == [11, 21]
    assert output["right"].to_pylist() == [12, 22]


def test_carry_forward_reads_blob_old_values() -> None:
    """A filtered re-backfill of a blob output column carries each unmatched
    row's old value forward. Lance reads a blob column back as lazy ``BlobFile``
    handles in a ``list[dict]`` batch, so the carry-forward merge must read those
    handles to bytes: matched rows take the newly computed value, unmatched rows
    keep their old blob bytes."""

    @udf(data_type=pa.large_binary(), field_metadata={"lance-encoding:blob": "true"})
    def make_blob(value: int) -> bytes:
        return f"new-{value}".encode()

    # "blob" is the output (carry-forward) column; the UDF reads "value".
    task = BackfillUDFTask({"blob": make_blob}, checkpoint_column="blob")

    # The scanner delivers the old blob column as BlobFile handles. Row 0 matches
    # the filter (recomputed); row 1 is unmatched and carries its old blob.
    batch = [
        {
            "value": 1,
            "blob": InMemoryBlobFile(b"old-1"),
            "_rowaddr": 0,
            BACKFILL_SELECTED: True,
        },
        {
            "value": 2,
            "blob": InMemoryBlobFile(b"old-2"),
            "_rowaddr": 1,
            BACKFILL_SELECTED: False,
        },
    ]

    output = task.apply(batch)

    assert output["blob"].to_pylist() == [b"new-1", b"old-2"]
    assert output["_rowaddr"].to_pylist() == [0, 1]


def test_create_plan_with_diverse_shuffle(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    ds = lance.write_dataset(
        pa.table({"a": range(1024)}),
        tmp_path / "tbl",
        max_rows_per_file=16,
    )

    plans = list(
        plan_read(ds.uri, tbl_ref, ["a"], batch_size=1, task_shuffle_diversity=4)[0]
    )
    assert len(plans) == 1024
    plan = plans[0]
    assert plan.uri == ds.uri
    assert plan.offset == 0
    assert plan.limit == 1


@udf(input_columns=["a"])
def one(*args, **kwargs) -> int:
    return 1


def test_applier(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    plans = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=16)[0])
    assert len(plans) == 1
    plan = plans[0]
    assert plan.uri == tbl.uri
    assert plan.offset == 0
    assert plan.limit == 3

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
    )
    results, direct_result, cnt_udf_computed = applier.run(plan)
    assert direct_result is None
    assert len(results) == 1
    batch = store[results[0].checkpoint_key]
    assert len(batch) == 3
    assert batch.to_pydict() == {"one": [1, 1, 1], "_rowaddr": [0, 1, 2]}
    assert cnt_udf_computed == 3


def test_applier_direct_fragment_write_for_single_full_fragment(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [None, None, None]}))

    plan = next(iter(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=0)[0]))
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"b": one},
            override_batch_size=0,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
        direct_fragment_write=_direct_write_config(tbl, "b"),
    )

    checkpoints, direct_result, cnt_udf_computed = applier.run(plan)

    assert checkpoints == []
    assert direct_result is not None
    assert direct_result.checkpoint_written is True
    assert direct_result.rows_written == 3
    assert cnt_udf_computed == 3

    keys = list(store.list_keys())
    assert not any("_range-" in key for key in keys)
    dedupe_key = _get_fragment_dedupe_key(tbl.uri, 0, applier.map_task, tbl.version)
    assert keys == [dedupe_key]
    checkpoint_batch = store[dedupe_key]
    assert checkpoint_batch["file"][0].as_py() == direct_result.new_file.path


def test_applier_direct_fragment_write_for_multiple_batches_before_flush(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [None, None, None]}))

    plan = _DummyReadTask(
        frag_id=0,
        rows=3,
        batches=[
            pa.record_batch(
                [
                    pa.array([1, 2], type=pa.int64()),
                    pa.array([0, 1], type=pa.uint64()),
                ],
                names=["a", "_rowaddr"],
            ),
            pa.record_batch(
                [
                    pa.array([3], type=pa.int64()),
                    pa.array([2], type=pa.uint64()),
                ],
                names=["a", "_rowaddr"],
            ),
        ],
    )
    plan.fragment_logical_rows = 3
    plan.fragment_physical_rows = 3
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"b": one},
            override_batch_size=2,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
        direct_fragment_write=_direct_write_config(tbl, "b"),
    )

    checkpoints, direct_result, cnt_udf_computed = applier.run(plan)

    assert checkpoints == []
    assert direct_result is not None
    assert direct_result.rows_written == 3
    assert cnt_udf_computed == 3
    keys = list(store.list_keys())
    assert not any("_range-" in key for key in keys)


def test_applier_direct_fragment_write_falls_back_after_checkpoint_flush(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [None, None, None]}))

    plan = _DummyReadTask(
        frag_id=0,
        rows=3,
        batches=[
            pa.record_batch(
                [
                    pa.array([1, 2], type=pa.int64()),
                    pa.array([0, 1], type=pa.uint64()),
                ],
                names=["a", "_rowaddr"],
            ),
            pa.record_batch(
                [
                    pa.array([3], type=pa.int64()),
                    pa.array([2], type=pa.uint64()),
                ],
                names=["a", "_rowaddr"],
            ),
        ],
    )
    plan.fragment_logical_rows = 3
    plan.fragment_physical_rows = 3
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"b": one},
            override_batch_size=2,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
        direct_fragment_write=_direct_write_config(tbl, "b"),
        batch_checkpoint_flush_interval_seconds=0,
    )

    checkpoints, direct_result, cnt_udf_computed = applier.run(plan)

    assert direct_result is None
    assert checkpoints
    assert cnt_udf_computed == 3
    assert any("_range-" in checkpoint.checkpoint_key for checkpoint in checkpoints)


def test_applier_direct_fragment_write_falls_back_for_delete_fragments(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [None, None, None]}))
    tbl.delete("a = 2")

    plan = next(iter(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=0)[0]))
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"b": one},
            override_batch_size=0,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
        direct_fragment_write=_direct_write_config(tbl, "b"),
    )

    checkpoints, direct_result, cnt_udf_computed = applier.run(plan)

    assert direct_result is None
    assert checkpoints
    assert cnt_udf_computed == 2
    assert any("_range-" in checkpoint.checkpoint_key for checkpoint in checkpoints)


class _StatusCodeError(RuntimeError):
    def __init__(self, message: str, status_code: int) -> None:
        super().__init__(message)
        self.status_code = status_code


@pytest.mark.parametrize(
    ("exc", "expected"),
    [
        pytest.param(
            RuntimeError("Failed to get AWS credentials: HttpTimeoutError"),
            True,
            id="aws-timeout-message",
        ),
        pytest.param(
            OSError("gcs object store temporarily unavailable"),
            True,
            id="gcs-temporary-unavailable",
        ),
        pytest.param(
            RuntimeError("azure object store connection reset by peer"),
            True,
            id="azure-connection-reset",
        ),
        pytest.param(
            RuntimeError(
                'azure object store error: response error "ServerBusy", after 0 retries'
            ),
            True,
            id="azure-server-busy-code",
        ),
        pytest.param(
            RuntimeError(
                "LanceError(IO): azure object store error: The server is busy."
            ),
            True,
            id="azure-server-busy-message",
        ),
        pytest.param(
            RuntimeError(
                "LanceError(IO): object store multipart upload error: Missing part 7"
            ),
            True,
            id="lance-multipart-missing-part",
        ),
        pytest.param(
            _StatusCodeError("object store too many requests", 429),
            True,
            id="http-429",
        ),
        pytest.param(
            _StatusCodeError("object store service unavailable", 503),
            True,
            id="http-503",
        ),
        pytest.param(
            _StatusCodeError("rate limited", 429),
            False,
            id="http-429-without-object-store-context",
        ),
        pytest.param(
            RuntimeError("table was not found"),
            False,
            id="table-not-found",
        ),
        pytest.param(
            ValueError("table does not exist"),
            False,
            id="table-does-not-exist",
        ),
        pytest.param(
            _StatusCodeError("unauthorized", 401),
            False,
            id="http-401",
        ),
        pytest.param(
            _StatusCodeError("forbidden", 403),
            False,
            id="http-403",
        ),
        pytest.param(
            _StatusCodeError("not found", 404),
            False,
            id="http-404",
        ),
        pytest.param(
            RuntimeError("Error running task: invalid schema"),
            False,
            id="invalid-schema",
        ),
        pytest.param(
            TimeoutError("timed out while calling external udf"),
            False,
            id="udf-timeout-without-object-store-context",
        ),
        pytest.param(
            ConnectionError("connection reset by peer from openai"),
            False,
            id="udf-connection-error-without-object-store-context",
        ),
    ],
)
def test_retryable_object_store_error_classification(
    exc: BaseException, expected: bool
) -> None:
    assert is_retryable_object_store_error(exc) is expected


def test_retryable_object_store_error_detects_nested_timeout() -> None:
    inner = ValueError(
        "LanceError(IO): provider connector timeout; connection reset by peer"
    )
    outer = RuntimeError("Error running task ScanTask(...)")
    outer.__cause__ = inner

    assert is_retryable_object_store_error(outer) is True


def test_retryable_object_store_error_prefers_nested_non_retryable_error() -> None:
    inner = _StatusCodeError("forbidden", 403)
    outer = RuntimeError("temporary timeout opening object store")
    outer.__cause__ = inner

    assert is_retryable_object_store_error(outer) is False


def test_retryable_object_store_error_does_not_false_match_eof_substring() -> None:
    exc = RuntimeError("geoff reported an invalid schema")

    assert is_retryable_object_store_error(exc) is False


def test_setup_inputplans_counts_readtasks_for_expected_tasks(
    tbl_ref: TableReference,
) -> None:
    task = _DummyReadTask(frag_id=0, rows=10)
    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            override_batch_size=4,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter([task]),
        job_id="job-expected-tasks",
        job_tracker=_NoopJobTracker(),
    )

    plans, tasks_by_frag, total_tasks = job.setup_inputplans()

    assert tasks_by_frag == {0: 1}
    assert total_tasks == 1
    assert len(list(plans)) == 1


def test_setup_inputplans_counts_multiple_readtasks_per_fragment(
    tbl_ref: TableReference,
) -> None:
    tasks = [
        _DummyReadTask(frag_id=0, rows=5, offset=0),
        _DummyReadTask(frag_id=0, rows=7, offset=5),
    ]
    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            override_batch_size=2,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=iter(tasks),
        job_id="job-multi-tasks",
        job_tracker=_NoopJobTracker(),
    )

    _, tasks_by_frag, total_tasks = job.setup_inputplans()

    assert tasks_by_frag == {0: 2}
    assert total_tasks == 2


def test_setup_inputplans_keeps_compact_plan_lazy(
    tbl_ref: TableReference,
) -> None:
    consumed = 0
    tasks = [
        _DummyReadTask(frag_id=0, rows=5, offset=0),
        _DummyReadTask(frag_id=0, rows=7, offset=5),
    ]

    def task_gen() -> Iterator[ReadTask]:
        nonlocal consumed
        for task in tasks:
            consumed += 1
            yield task

    plan = apply_module._LanceReadPlanIterator(
        task_gen(),
        total=2,
        total_rows=12,
        tasks_by_frag={0: 2},
        checkpoint_identity_contexts=(("memory://source", None),),
    )
    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            override_batch_size=2,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=plan,
        job_id="job-lazy-plan",
        job_tracker=_NoopJobTracker(),
    )

    plans, tasks_by_frag, total_tasks = job.setup_inputplans()

    assert consumed == 0
    assert job._total_rows == 12
    assert job._checkpoint_identity_contexts == (("memory://source", None),)
    assert tasks_by_frag == {0: 2}
    assert total_tasks == 2
    assert next(plans) is tasks[0]
    assert consumed == 1


def test_setup_inputplans_rejects_preconsumed_compact_plan(
    tbl_ref: TableReference,
) -> None:
    task = _DummyReadTask(frag_id=0, rows=1)
    plan = apply_module._LanceReadPlanIterator(
        iter((task,)),
        total=1,
        total_rows=1,
        tasks_by_frag={0: 1},
        checkpoint_identity_contexts=(("memory://source", None),),
    )
    assert next(plan) is task
    job = ColumnAddPipelineJob(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            override_batch_size=1,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=CheckpointStore.from_uri("memory"),
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=plan,
        job_id="job-preconsumed-plan",
        job_tracker=_NoopJobTracker(),
    )

    with pytest.raises(ValueError, match="must not be consumed"):
        job.setup_inputplans()


def test_fragment_scan_plan_counts_tasks_without_materializing(
    tbl_ref: TableReference,
) -> None:
    total_rows = 1_000_000_000
    fragment_plan = apply_module._FragmentScanPlan(
        template=ScanTask(
            uri="memory://table",
            table_ref=tbl_ref,
            columns=["a"],
            frag_id=7,
            offset=0,
            limit=0,
            fragment_physical_rows=total_rows,
            fragment_logical_rows=total_rows,
        ),
        runs=((0, total_rows),),
        task_size=1,
    )

    assert fragment_plan.task_count == total_rows
    first_tasks = list(islice(fragment_plan.tasks(), 3))
    assert [(task.offset, task.limit) for task in first_tasks] == [
        (0, 1),
        (1, 1),
        (2, 1),
    ]


def test_read_task_feeder_is_bounded_and_prioritizes_retries() -> None:
    tasks = [_DummyReadTask(frag_id=0, rows=1, offset=offset) for offset in range(10)]
    consumed = 0

    def task_gen() -> Iterator[ReadTask]:
        nonlocal consumed
        for task in tasks:
            consumed += 1
            yield task

    feeder = pipeline_module._ReadTaskFeeder(
        task_gen(),
        Counter({0: 10}),
        expected_total_tasks=10,
        expected_total_rows=10,
    )

    primed = [feeder.pop_next() for _ in range(4)]
    assert consumed == 4
    assert all(item is not None and item[1] for item in primed)

    retry = pipeline_module.ScheduledReadTask(
        _DummyReadTask(frag_id=0, rows=1, offset=99), attempt=2
    )
    feeder.retry_tasks.append(retry)
    assert feeder.pop_next() == (retry, False)
    assert consumed == 4
    assert feeder.pop_next() == (pipeline_module.ScheduledReadTask(tasks[4]), True)
    assert consumed == 5


def test_read_task_feeder_rejects_metadata_underflow() -> None:
    task = _DummyReadTask(frag_id=0, rows=1)
    feeder = pipeline_module._ReadTaskFeeder(
        iter((task,)),
        Counter({0: 2}),
        expected_total_tasks=2,
        expected_total_rows=2,
    )

    assert feeder.pop_next() is not None
    with pytest.raises(ValueError, match="ended before its metadata"):
        feeder.pop_next()


def test_job_tracker_metric_buffer_batches_task_progress() -> None:
    tracker = _RecordingJobTracker()
    metric_buffer = pipeline_module._JobTrackerMetricBuffer(
        tracker,  # type: ignore[arg-type]
        max_events=100,
        flush_interval_s=3600,
    )

    for _ in range(10_000):
        metric_buffer.add("tasks_completed", 1)
    metric_buffer.flush(force=True)

    calls = tracker.batch_increment.calls
    assert len(calls) == 100
    assert sum(call[0]["tasks_completed"] for call in calls) == 10_000


def test_job_tracker_metric_buffer_bounds_slow_inflight_rpc(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _SlowRemote:
        def __init__(self) -> None:
            self.calls: list[dict[str, int]] = []
            self.result: object = pipeline_module.ray.ObjectRef.from_random()

        def remote(self, payload: dict[str, int]) -> object:
            self.calls.append(payload)
            return self.result

    class _SlowTracker:
        batch_increment = _SlowRemote()

    tracker = _SlowTracker()
    monkeypatch.setattr(
        pipeline_module.ray,
        "wait",
        lambda refs, timeout=0: ([], refs),
    )
    metric_buffer = pipeline_module._JobTrackerMetricBuffer(
        tracker,  # type: ignore[arg-type]
        max_events=1,
        flush_interval_s=0,
    )

    for _ in range(10_000):
        metric_buffer.add("tasks_completed", 1)

    assert tracker.batch_increment.calls == [{"tasks_completed": 1}]
    assert metric_buffer._pending == {"tasks_completed": 9_999}

    # Simulate the one outstanding RPC completing, then drain the fixed-size
    # pending metric map.
    metric_buffer._inflight = None
    tracker.batch_increment.result = None
    metric_buffer.flush(force=True)
    assert tracker.batch_increment.calls[-1] == {"tasks_completed": 9_999}


def test_writer_session_bounds_pending_enqueue_refs(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _PutRemote:
        def __init__(self) -> None:
            self.calls = 0

        def remote(self, item: object) -> str:
            self.calls += 1
            return f"ref-{self.calls}"

    class _Queue:
        class _Actor:
            put_nowait = _PutRemote()

        actor = _Actor()

    drained: list[list[object]] = []
    monkeypatch.setattr(pipeline_module, "WRITER_ENQUEUE_ACK_BATCH_SIZE", 3)
    monkeypatch.setattr(
        pipeline_module.ray,
        "get",
        lambda refs: drained.append(list(refs)),
    )
    session = pipeline_module.FragmentWriterSession(
        frag_id=0,
        ds_uri="memory://table",
        output_columns=["one"],
        checkpoint_store=object(),  # type: ignore[arg-type]
        where=None,
    )
    session.queue = _Queue()  # type: ignore[assignment]

    for offset in range(7):
        session._enqueue_unbounded((offset, f"checkpoint-{offset}", 1))

    assert drained == [
        ["ref-1", "ref-2", "ref-3"],
        ["ref-4", "ref-5", "ref-6"],
    ]
    assert session._pending_enqueue_refs == ["ref-7"]


def test_fragment_task_keys_are_released_at_terminal_state() -> None:
    manager = _make_fragment_writer_manager()
    task = _DummyReadTask(frag_id=0, rows=1)
    session = _DummyWriterSession(sealed=False)
    manager.sessions[0] = session  # type: ignore[assignment]
    manager.remaining_tasks[0] = 1

    manager.ingest_task(task, [])

    assert manager._task_key_was_ingested(0, task.checkpoint_key())
    manager._mark_partial_task_key_ingested(0, task.checkpoint_key())
    assert session.seal_calls == 1

    request = pipeline_module._FragmentRecordRequest(
        frag_id=0,
        new_file=object(),
        commit_granularity=999,
        rows_written=1,
        direct_write=False,
        checkpoint_already_written=True,
        fragment_checkpointing_ms=0,
        buffer_sort_ms=0,
        align_ms=0,
        write_ms=0,
        queue_wait_ms=0,
        checkpoint_read_ms=0,
        avg_batch_num_rows=0,
        avg_batch_size=0,
        dedupe_key="fragment-0",
        checkpoint_batch=None,
        purge_keys=[],
    )
    manager._finish_fragment_record(
        pipeline_module._CompletedFragmentRecord(request, checkpointing_ms=0)
    )

    assert 0 in manager._recorded_fragment_ids
    manager.ingest_task(task, [])

    assert 0 not in manager._ingested_task_keys
    assert 0 not in manager._partial_ingested_task_keys
    assert manager.remaining_tasks[0] == 0
    assert session.seal_calls == 1


def test_applier_synthesizes_checkpoints_when_no_batches() -> None:
    task = _DummyReadTask(frag_id=0, rows=5, offset=0)
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            override_batch_size=2,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri="memory",
    )

    checkpoints, direct_result, cnt_udf_computed = applier.run(task)
    assert direct_result is None

    assert cnt_udf_computed == 0
    assert [checkpoint.span for checkpoint in checkpoints] == [2, 2, 1]
    assert [
        applier.checkpoint_store[checkpoint.checkpoint_key].num_rows
        for checkpoint in checkpoints
    ] == [2, 2, 1]


@udf(data_type=pa.large_binary(), input_columns=["a"])
def _emit_kilobyte(a: int) -> bytes:
    """Test UDF that emits a fixed 1 KiB payload per row."""
    return b"x" * 1024


class _StaticBatchApplier(BatchApplier):
    def __init__(self, batches: list[pa.RecordBatch]) -> None:
        self._batches = batches
        self._yielded = 0
        self._lock = threading.Lock()

    @property
    def yielded(self) -> int:
        with self._lock:
            return self._yielded

    def run(
        self,
        read_task: ReadTask,
        map_task: Any,
        error_logger: Any,
    ) -> Iterator[pa.RecordBatch]:
        for batch in self._batches:
            with self._lock:
                self._yielded += 1
            yield batch


def _large_binary_output_batches(
    num_batches: int = 4,
    rows_per_batch: int = 2,
) -> list[pa.RecordBatch]:
    return [
        pa.record_batch(
            [
                pa.array([b"x" * 1024] * rows_per_batch, type=pa.large_binary()),
                pa.array(
                    list(range(i * rows_per_batch, (i + 1) * rows_per_batch)),
                    type=pa.uint64(),
                ),
            ],
            names=["out", "_rowaddr"],
        )
        for i in range(num_batches)
    ]


def _byte_target_dummy_task(num_batches: int = 4, rows_per_batch: int = 2) -> ...:
    """Return a dummy task that yields several small input batches.

    Total rows is ``num_batches * rows_per_batch``; the UDF applied on top
    emits a 1 KiB large_binary value per row, so each output batch holds
    roughly ``rows_per_batch * 1024`` bytes plus framing.
    """
    batches = [
        pa.record_batch(
            [
                pa.array(
                    list(range(i * rows_per_batch, (i + 1) * rows_per_batch)),
                    type=pa.int64(),
                ),
                pa.array(
                    list(range(i * rows_per_batch, (i + 1) * rows_per_batch)),
                    type=pa.uint64(),
                ),
            ],
            names=["a", "_rowaddr"],
        )
        for i in range(num_batches)
    ]
    total_rows = num_batches * rows_per_batch
    task = _DummyReadTask(frag_id=0, rows=total_rows, batches=batches)
    task.fragment_logical_rows = total_rows
    task.fragment_physical_rows = total_rows
    return task


def test_applier_pending_byte_target_flushes_per_batch() -> None:
    """A tight byte target forces a flush after each output batch.

    Regression for GEN-507: without a byte-aware flush trigger, large_binary
    UDF output could accumulate without bound until the time-based flush
    fired, exhausting worker memory before the first checkpoint was written.
    """
    task = _byte_target_dummy_task()
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"out": _emit_kilobyte},
            override_batch_size=2,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri="memory",
        # Never time-flush; the byte target is the only intermediate trigger.
        batch_checkpoint_flush_interval_seconds=60.0,
        # Each output batch holds ~2 KiB of large_binary; a 1 KiB target
        # means every appended batch alone exceeds the budget.
        checkpoint_pending_bytes_target=1024,
    )

    checkpoints, direct_result, _ = applier.run(task)

    assert direct_result is None
    assert len(checkpoints) == 4


def test_applier_pending_byte_target_zero_disables_byte_trigger() -> None:
    """A byte target of 0 preserves the legacy (rows + time only) behavior."""
    task = _byte_target_dummy_task()
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"out": _emit_kilobyte},
            override_batch_size=2,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri="memory",
        batch_checkpoint_flush_interval_seconds=60.0,
        checkpoint_pending_bytes_target=0,
    )

    checkpoints, direct_result, _ = applier.run(task)

    assert direct_result is None
    # All batches merge into one final flush at task end.
    assert len(checkpoints) == 1


def test_applier_pending_byte_target_loose_target_merges() -> None:
    """A byte target larger than the total output produces a single flush."""
    task = _byte_target_dummy_task()
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"out": _emit_kilobyte},
            override_batch_size=2,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri="memory",
        batch_checkpoint_flush_interval_seconds=60.0,
        # ~64 KiB target — comfortably larger than total ~8 KiB output.
        checkpoint_pending_bytes_target=64 * 1024,
    )

    checkpoints, direct_result, _ = applier.run(task)

    assert direct_result is None
    assert len(checkpoints) == 1


def test_applier_checkpoint_producer_queue_backpressures_by_bytes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_batches = _large_binary_output_batches()
    batch_applier = _StaticBatchApplier(output_batches)
    task = _DummyReadTask(frag_id=0, rows=8)
    task.fragment_logical_rows = 8
    task.fragment_physical_rows = 8
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"out": _emit_kilobyte},
            override_batch_size=2,
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri="memory",
        batch_checkpoint_flush_interval_seconds=60.0,
        checkpoint_pending_bytes_target=int(output_batches[0].nbytes) + 1,
        batch_applier=batch_applier,
    )

    original_write_checkpoint_batch = CheckpointingApplier._write_checkpoint_batch
    write_started = threading.Event()
    release_write = threading.Event()

    def blocking_write_checkpoint_batch(
        self: CheckpointingApplier,
        checkpoint_key: str,
        batch: pa.RecordBatch,
    ) -> None:
        if self is applier and not write_started.is_set():
            write_started.set()
            if not release_write.wait(timeout=5.0):
                raise TimeoutError("timed out waiting to unblock checkpoint write")
        original_write_checkpoint_batch(self, checkpoint_key, batch)

    monkeypatch.setattr(
        CheckpointingApplier, "_write_checkpoint_batch", blocking_write_checkpoint_batch
    )

    done = threading.Event()
    errors: list[BaseException] = []
    results: list[
        tuple[list[MapBatchCheckpoint], DirectFragmentWriteResult | None, int]
    ] = []

    def run_applier() -> None:
        try:
            results.append(applier.run(task))
        except BaseException as exc:
            errors.append(exc)
        finally:
            done.set()

    worker = threading.Thread(target=run_applier, name="checkpoint-backpressure-test")
    worker.start()
    try:
        assert write_started.wait(timeout=5.0)

        deadline = time.monotonic() + 5.0
        while batch_applier.yielded < 3 and time.monotonic() < deadline:
            time.sleep(0.01)

        # The third batch has been produced and is blocked on the byte budget.
        # Without producer-side backpressure the fourth batch would be yielded
        # while the consumer is still blocked in the first checkpoint write.
        assert batch_applier.yielded == 3
        time.sleep(0.2)
        assert batch_applier.yielded == 3

        release_write.set()
        worker.join(timeout=5.0)

        assert not worker.is_alive()
        if errors:
            raise errors[0]

        checkpoints, direct_result, _ = results[0]
        assert direct_result is None
        assert len(checkpoints) == 2
        assert batch_applier.yielded == 4
    finally:
        release_write.set()
        worker.join(timeout=5.0)


def test_checkpoint_subranges_cover_gaps(tmp_path: Path) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 3]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        override_batch_size=4,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    applier = CheckpointingApplier(map_task=map_task, checkpoint_uri=store.root)

    class _Task(ScanTask):
        pass

    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=4,
        version=tbl.version,
        where=None,
        with_row_address=True,
    )

    batch = pa.record_batch(
        [pa.array([1, 3]), pa.array([0, 3], type=pa.uint64())],
        names=["a", "_rowaddr"],
    )

    result = applier._checkpoint_single_batch(
        task,
        batch,
        dataset_uri=tbl.uri,
        dataset_version=tbl.version,
        where=None,
        udf_rows=None,
        start=0,
        checkpoint_size=4,
    )

    assert result.offset == 0
    # span should expand to checkpoint_size (=4) even with gaps, capped by task_end
    assert result.span == 4
    assert store[result.checkpoint_key].num_rows == 2


def test_applier_chain_spans_respects_task_end(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3, 4, 5]}))

    plan = next(iter(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=5)[0]))
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            override_batch_size=2,
            min_checkpoint_size=2,
            max_checkpoint_size=2,
        ),
        checkpoint_uri=store.root,
        batch_checkpoint_flush_interval_seconds=0,
    )

    results, direct_result, _ = applier.run(plan)
    assert direct_result is None

    assert [r.offset for r in results] == [0, 2, 4]
    assert [r.span for r in results] == [2, 2, 1]


def test_plan_read_recommits_checkpointed_ranges_over_preexisting_output(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    # Output column 'one' has a committed data file, but full per-batch
    # coverage with NO fragment dedupe marker means this job's output never
    # landed -- the file predates the job and may hold stale values (the
    # filtered-repair case). Skipping would silently no-op the job, so the
    # fragment is replanned as one whole-fragment commit task that reuses the
    # checkpoints. A fragment genuinely committed by this job is still skipped
    # via its dedupe marker (written durably before the commit).
    db = connect(tmp_path)
    tbl = db.create_table(
        "tbl", pa.table({"a": [1, 2, 3, 4, 5, 6], "one": [1, 1, 1, 1, 1, 1]})
    )
    dataset = tbl.to_lance()

    map_task = BackfillUDFTask(
        udfs={"one": one},
        override_batch_size=2,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))

    # Pre-populate checkpoints for [0,2), [2,4), [4,6)
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    for start in (0, 2, 4):
        end = start + 2
        key = map_task.checkpoint_key(
            dataset_uri=tbl.uri,
            dataset_version=dataset.version,
            frag_id=0,
            start=start,
            end=end,
            where=None,
            src_files_hash=src_files_hash,
        )
        store[key] = pa.record_batch([], names=[])

    tasks, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=2,
        map_task=map_task,
        checkpoint_store=store,
    )

    # One whole-fragment task to commit the checkpointed output; not skipped.
    assert [(t.offset, t.limit) for t in tasks] == [(0, 6)]
    assert pipeline_args["skipped_stats"]["rows"] == 0


def test_plan_read_skip_checkpoint_index_scan_does_not_list_or_probe(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    map_task = BackfillUDFTask(
        udfs={"a2": double_a},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    store = _NoPlannerCheckpointProbeStore()

    tasks, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=2,
        map_task=map_task,
        checkpoint_store=store,
        _skip_checkpoint_index_scan=True,
    )

    task_list = list(tasks)
    assert [(task.offset, task.limit) for task in task_list] == [(0, 2), (2, 1)]
    assert {task.src_files_hash for task in task_list} == {
        _src_files_hash_for_cols(tbl, ["a"])
    }
    assert pipeline_args["skipped_stats"] == {"fragments": 0, "rows": 0}


def test_skip_checkpoint_index_scan_preserves_exact_task_checkpoint_reuse(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def fail_if_called(a: int) -> int:
        raise AssertionError(f"UDF should not run for cached row {a}")

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"b": fail_if_called},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    tasks, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=3,
        map_task=map_task,
        checkpoint_store=store,
        _skip_checkpoint_index_scan=True,
    )
    task = next(iter(tasks))

    assert task.src_files_hash == _src_files_hash_for_cols(tbl, ["a"])

    applier = CheckpointingApplier(
        map_task=map_task,
        checkpoint_uri=store.root,
    )
    task_key = applier._checkpoint_key_for_task(task)
    store[task_key] = pa.record_batch(
        [
            pa.array([10, 20, 30], type=pa.int64()),
            pa.array([0, 1, 2], type=pa.uint64()),
        ],
        names=["b", "_rowaddr"],
    )

    checkpoints, direct_result, cnt_udf_computed = applier.run(task)

    assert direct_result is None
    assert [checkpoint.checkpoint_key for checkpoint in checkpoints] == [task_key]
    assert cnt_udf_computed == 3


def test_plan_read_replans_fully_checkpointed_uncommitted_fragment(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Per-batch checkpoints fully cover a fragment but the output was never
    committed (no data file for the output column). Skipping would leave the
    column NULL forever, so the fragment is replanned; the applier reuses the
    per-batch checkpoints, so the commit happens without recomputing the UDF.
    The repair-shaped sibling above (pre-existing output data file, same
    orphaned-coverage state) replans the same way."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3, 4, 5, 6]}))
    tbl.add_columns({"one": one})  # 'one' in schema, never committed in fragment
    dataset = tbl.to_lance()

    map_task = BackfillUDFTask(
        udfs={"one": one},
        override_batch_size=2,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))

    # Full per-batch coverage [0,2),[2,4),[4,6) -- but no committed output and
    # no fragment-level dedupe key (exactly the crash-orphaned shape).
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    for start in (0, 2, 4):
        end = start + 2
        key = map_task.checkpoint_key(
            dataset_uri=tbl.uri,
            dataset_version=dataset.version,
            frag_id=0,
            start=start,
            end=end,
            where=None,
            src_files_hash=src_files_hash,
        )
        store[key] = pa.record_batch([], names=[])

    tasks, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=2,
        map_task=map_task,
        checkpoint_store=store,
    )

    # Must NOT skip: the fragment is replanned so its output gets committed.
    task_list = list(tasks)
    assert task_list, "fragment was wrongly skipped despite uncommitted output"
    assert {t.dest_frag_id() for t in task_list} == {0}
    assert pipeline_args["skipped_stats"]["rows"] == 0


def test_plan_read_replan_does_not_split_checkpoint_spans(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Replanning a fully-checkpointed-but-uncommitted fragment must not split
    an existing per-batch ``_range-`` checkpoint. Even with a recovery task_size
    (2) smaller than the existing checkpoint span (4), the replan emits a single
    whole-fragment task so the writer reassembles each checkpoint at its own
    boundary. Re-chunking at task_size (offsets 0,2,4,6) would split a span-4 key
    across tasks and the writer would overshoot its SequenceQueue and hang (see
    test_wedged_by_overshooting_span in test_sequence_queue.py).
    """
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": list(range(8))}))
    tbl.add_columns({"one": one})  # uncommitted -> hits the replan branch
    dataset = tbl.to_lance()

    map_task = BackfillUDFTask(
        udfs={"one": one},
        override_batch_size=4,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    # Existing per-batch checkpoints with span 4 -> full coverage of [0,8).
    for start in (0, 4):
        key = map_task.checkpoint_key(
            dataset_uri=tbl.uri,
            dataset_version=dataset.version,
            frag_id=0,
            start=start,
            end=start + 4,
            where=None,
            src_files_hash=src_files_hash,
        )
        store[key] = pa.record_batch([], names=[])

    # Recovery at a smaller task_size (2 < the span-4 checkpoints) must NOT
    # split the keys.
    tasks, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        task_size=2,
        map_task=map_task,
        checkpoint_store=store,
    )

    # One whole-fragment task -- not re-chunked at task_size=2 (which would have
    # produced offsets 0,2,4,6 and split the span-4 keys at offsets 2 and 6).
    assert [(t.offset, t.limit) for t in tasks] == [(0, 8)]


def test_plan_read_builds_gaps_and_chunks(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """A partially covered fragment is tiled in full: covered runs become
    tasks too (reconstructed from the store, no recompute), because the
    fragment is rewritten in full and the writer needs checkpoints for every
    row. Planning only the gap used to null-fill the covered ranges at seal.
    """
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": list(range(10))}))

    map_task = BackfillUDFTask(
        udfs={"one": one},
        override_batch_size=2,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))

    # Checkpoints cover [0,5) and [7,10), leaving gap [5,7)
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    for start, end in [(0, 5), (7, 10)]:
        key = map_task.checkpoint_key(
            dataset_uri=tbl.uri,
            dataset_version=tbl.version,
            frag_id=0,
            start=start,
            end=end,
            where=None,
            src_files_hash=src_files_hash,
        )
        store[key] = pa.record_batch([], names=[])

    tasks, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=3,  # task_size
        map_task=map_task,
        checkpoint_store=store,
    )

    # Covered run [0,5) tiled at task_size, gap [5,7), covered run [7,10).
    assert [(t.offset, t.limit) for t in tasks] == [
        (0, 3),
        (3, 2),
        (5, 2),
        (7, 3),
    ]


def test_plan_read_propagates_src_data_files_to_tasks(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": list(range(4))}))

    map_task = BackfillUDFTask(
        udfs={"one": one},
        override_batch_size=2,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))

    tasks, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=4,
        map_task=map_task,
        checkpoint_store=store,
    )

    task_list = list(tasks)
    assert len(task_list) == 1
    src_data_files = pipeline_args["src_data_files_by_dst"][0]
    assert src_data_files
    assert task_list[0].src_data_files == src_data_files


def test_plan_read_chunks_large_gap(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": list(range(20))}))

    map_task = BackfillUDFTask(
        udfs={"one": one},
        override_batch_size=2,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))

    # Covered [0,2) and [10,20); gap [2,10) length 8.
    # task_size=3 -> gap chunks [2,5), [5,8), [8,10); covered runs are tiled
    # too (reused from checkpoints) so the writer sees every row.
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    for start, end in [(0, 2), (10, 20)]:
        key = map_task.checkpoint_key(
            dataset_uri=tbl.uri,
            dataset_version=tbl.version,
            frag_id=0,
            start=start,
            end=end,
            where=None,
            src_files_hash=src_files_hash,
        )
        store[key] = pa.record_batch([], names=[])

    tasks, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=3,
        map_task=map_task,
        checkpoint_store=store,
    )

    task_list = list(tasks)
    offsets_limits = [(t.offset, t.limit) for t in task_list]
    assert offsets_limits == [
        (0, 2),  # covered run, reused
        (2, 3),
        (5, 3),
        (8, 2),
        (10, 3),  # covered run, reused
        (13, 3),
        (16, 3),
        (19, 1),
    ]


def test_applier_checkpoints_each_map_batch(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3, 4, 5]}))

    plans = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=5)[0])
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))

    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            override_batch_size=2,
            min_checkpoint_size=2,
            max_checkpoint_size=2,
        ),
        checkpoint_uri=store.root,
        batch_checkpoint_flush_interval_seconds=0,
    )

    results, direct_result, cnt_udf = applier.run(plans[0])
    assert direct_result is None

    assert [r.offset for r in results] == [0, 2, 4]
    assert [r.span for r in results] == [2, 2, 1]
    assert cnt_udf == 5

    # Only per-map-batch checkpoints are stored (no task-level aggregate)


def test_applier_concats_checkpoints_with_time_flush(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3, 4, 5]}))

    plans = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=5)[0])
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))

    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            override_batch_size=2,
            min_checkpoint_size=2,
            max_checkpoint_size=2,
        ),
        checkpoint_uri=store.root,
    )

    results, direct_result, cnt_udf = applier.run(plans[0])
    assert direct_result is None

    assert len(results) == 1
    assert results[0].offset == 0
    assert results[0].span == 5
    assert store[results[0].checkpoint_key].num_rows == 5
    assert cnt_udf == 5


def test_checkpoint_key_format(tmp_path: Path, tbl_ref: TableReference) -> None:
    @udf(version="v0", input_columns=["a"])
    def times_two(a: int) -> int:
        return a * 2

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3, 4]}))

    where = "a > 1"
    read_version = tbl.version

    map_task = BackfillUDFTask(
        udfs={"b": times_two},
        where=where,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    plans = list(
        plan_read(
            tbl.uri,
            tbl_ref,
            ["a"],
            batch_size=2,
            where=where,
            read_version=read_version,
            map_task=map_task,
        )[0]
    )

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(map_task=map_task, checkpoint_uri=store.root)

    results, direct_result, cnt_udf_computed = applier.run(plans[0])
    assert direct_result is None
    assert len(results) == 1
    key = results[0].checkpoint_key

    where_hash = hashlib.md5(where.encode()).hexdigest()
    uri_hash = hashlib.md5(tbl.uri.encode()).hexdigest()
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    prefix = (
        f"udf-{times_two.name}_ver-{times_two.version}"
        f"_col-b_where-{where_hash}_uri-{uri_hash}_srcfiles-{src_files_hash}"
    )
    expected_key = (
        f"{prefix}_frag-{plans[0].dest_frag_id()}_"
        f"range-{plans[0].dest_offset()}-{plans[0].dest_offset() + plans[0].num_rows()}"
    )

    assert key == expected_key
    assert key in store
    # First batch has a values [1,2]; only 2 satisfies where
    assert cnt_udf_computed == 1


def test_plan_read_with_legacy_checkpoint_and_partial(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """
    Legacy fragment checkpoints are still honored even when srcfiles hashes are
    available. Partial old batch checkpoints should not skip.
    """
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))
    tbl.add(pa.table({"a": [4, 5, 6]}))  # second fragment

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    # Insert legacy fragment-level checkpoint for fragment 0
    legacy_frag_key = _legacy_fragment_dedupe_key(tbl.uri, 0, map_task)
    store[legacy_frag_key] = pa.RecordBatch.from_pydict({"file": ["fragment0.lance"]})
    assert legacy_frag_key in store
    staging_dir = Path(URL(tbl.uri).path) / "data"
    staging_dir.mkdir(exist_ok=True)
    # Valid 3-row staged file (matches fragment 0); a 0-byte touch is now
    # rejected as a stale leftover (GEN-530).
    from lance.file import LanceFileWriter

    _w = LanceFileWriter(str(staging_dir / "fragment0.lance"))
    _w.write_batch(pa.table({"one": [1, 1, 1]}))
    _w.close()

    # Insert an old-format partial batch checkpoint for fragment 1 (should be ignored)
    store["fragment_1_batch_0_50:old"] = pa.RecordBatch.from_pydict(
        {"file": ["partial_batch"]}
    )

    # Legacy checkpoint should be detectable
    assert _check_fragment_data_file_exists(
        tbl.uri, 0, map_task, store, dataset_version=tbl.version
    )

    plans, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=16,
        map_task=map_task,
        checkpoint_store=store,
    )

    task_list = list(plans)

    # fragment 0 should be skipped via legacy checkpoint
    # fragment 1 should still have tasks
    assert "skipped_fragments" in pipeline_args
    assert 0 in pipeline_args["skipped_fragments"]
    frag_ids = {t.dest_frag_id() for t in task_list}
    assert 1 in frag_ids
    assert len(task_list) > 0


def test_applier_with_where(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3, 4, 5, 6, 7, 8]}))

    plans = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=3, where="a%2=0")[0])

    assert len(plans) == 3  # 1-3, 4-6, and 7-8
    plan = plans[0]
    assert plan.uri == tbl.uri
    assert plan.offset == 0
    assert plan.limit == 3

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
    )

    # Lance forces us to eithe write the entire column or write an entire row.  This
    # applier writes the whole col.  So we actually do all the scans and filter at udf
    # execution time.  When the udf is not executed we return None.

    expected = [
        {"one": [None, 1, None], "_rowaddr": [0, 1, 2]},
        {"one": [1, None, 1], "_rowaddr": [3, 4, 5]},
        {"one": [None, 1], "_rowaddr": [6, 7]},
    ]

    expected_counts = [1, 2, 1]
    for i, plan in enumerate(plans):
        results, direct_result, cnt_udf_computed = applier.run(plan)
        assert direct_result is None
        assert len(results) == 1
        batch = store[results[0].checkpoint_key]
        assert batch.to_pydict() == expected[i]
        assert cnt_udf_computed == expected_counts[i]


def test_applier_with_where2(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3, 4, 5, 6, 7, 8]}))

    plans = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=1, where="a%2=0")[0])

    assert len(plans) == 8  # 1-3, 4-6, and 7-8
    plan = plans[0]
    assert plan.uri == tbl.uri
    assert plan.offset == 0
    assert plan.limit == 1

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
    )

    expected = [
        {"one": [None], "_rowaddr": [0]},
        {"one": [1], "_rowaddr": [1]},
        {"one": [None], "_rowaddr": [2]},
        {"one": [1], "_rowaddr": [3]},
        {"one": [None], "_rowaddr": [4]},
        {"one": [1], "_rowaddr": [5]},
        {"one": [None], "_rowaddr": [6]},
        {"one": [1], "_rowaddr": [7]},
    ]

    expected_counts = [0, 1, 0, 1, 0, 1, 0, 1]
    for i, plan in enumerate(plans):
        results, direct_result, cnt_udf_computed = applier.run(plan)
        assert direct_result is None
        assert len(results) == 1
        batch = store[results[0].checkpoint_key]
        assert batch.to_pydict() == expected[i]
        assert cnt_udf_computed == expected_counts[i]


def test_applier_with_incremental(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)
    tbl = db.create_table(
        "tbl",
        pa.table(
            {
                "a": [1, 2, 3, 4, 5, 6, 7, 8],
                "one": [
                    None,
                    1,
                    None,
                    1,
                    None,
                    1,
                    None,
                    1,
                ],
            }
        ),
    )

    # apply a update plan that covers the rest
    plans = list(
        plan_read(
            tbl.uri,
            tbl_ref,
            ["a", "one"],  # input col and carry forward the output cols
            batch_size=1,
            carry_forward_cols=["one"],
            where="one is Null",
        )[0]
    )
    _LOG.debug(plans)

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
    )

    expected = [
        {"one": [1], "_rowaddr": [0]},
        {"one": [1], "_rowaddr": [1]},
        {"one": [1], "_rowaddr": [2]},
        {"one": [1], "_rowaddr": [3]},
        {"one": [1], "_rowaddr": [4]},
        {"one": [1], "_rowaddr": [5]},
        {"one": [1], "_rowaddr": [6]},
        {"one": [1], "_rowaddr": [7]},
    ]

    expected_counts = [1, 0, 1, 0, 1, 0, 1, 0]
    for i, plan in enumerate(plans):
        results, direct_result, cnt_udf_computed = applier.run(plan)
        assert direct_result is None
        assert len(results) == 1
        batch = store[results[0].checkpoint_key]
        assert batch.to_pydict() == expected[i]
        assert cnt_udf_computed == expected_counts[i]


@udf()
def errors_on_three(a: int) -> int:
    if a == 3:
        raise ValueError("This is an error")
    return 1


def test_applier_error_logging(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    plans = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=16)[0])
    assert len(plans) == 1
    plan = plans[0]
    assert plan.uri == tbl.uri
    assert plan.offset == 0
    assert plan.limit == 3

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    error_store = ErrorStore(db, "test_errors")
    error_logger = TableErrorLogger(error_store=error_store, table_ref=tbl_ref)
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": errors_on_three},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
        error_logger=error_logger,
    )
    with pytest.raises(RuntimeError):
        applier.run(plan)

    # Verify error was logged to error store
    errors = error_store.get_errors()
    assert len(errors) == 1
    error = errors[0]
    assert error.error_message == "This is an error"
    assert error.batch_index == 0


def test_error_store(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)
    error_store = ErrorStore(db, "test_errors")
    logger = TableErrorLogger(error_store=error_store, table_ref=tbl_ref)
    logger._store.get_errors()


def test_plan_with_where(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)

    tbl = db.create_table("t", pa.table({"a": range(100)}))
    tbl.add(pa.table({"a": range(100, 200)}))
    tbl.add(pa.table({"a": range(200, 300)}))
    tbl.add(pa.table({"a": range(300, 400)}))

    fragments = tbl.get_fragments()
    assert len(fragments) == 4

    # even though we have a filter, we still have to read all the fragments
    # batch size 0 means one task per  fragment
    tasks = list(
        plan_read(
            tbl.uri, tbl_ref, ["a"], where="a > 100 AND a % 2 == 0", batch_size=0
        )[0]
    )
    # there are only 3 tasks because we skip the first fragment due to the where clause.
    assert len(tasks) == 3


def test_plan_with_row_address(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)

    tbl = db.create_table("tbl", pa.table({"a": range(100)}))

    fragments = tbl.get_fragments()
    assert len(fragments) == 1

    tasks = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=1000)[0])
    assert len(tasks) == 1

    for batch in tasks[0].to_batches():
        assert "_rowaddr" in batch.column_names


def test_plan_with_num_frags(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)

    tbl = db.create_table("t", pa.table({"a": range(100)}))
    tbl.add(pa.table({"a": range(100, 200)}))
    tbl.add(pa.table({"a": range(200, 300)}))
    tbl.add(pa.table({"a": range(300, 400)}))

    fragments = tbl.get_fragments()
    assert len(fragments) == 4

    # even though we have a filter, we still have to read all the fragments
    tasks = list(plan_read(tbl.uri, tbl_ref, ["a"], num_frags=2)[0])
    # there are only 2 tasks because we set num_frags=2
    assert len(tasks) == 2


def test_plan_with_skip_frags(tmp_path: Path, tbl_ref: TableReference) -> None:
    db = connect(tmp_path)

    tbl = db.create_table("t", pa.table({"a": range(100)}))
    tbl.add(pa.table({"a": range(100, 200)}))
    tbl.add(pa.table({"a": range(200, 300)}))
    tbl.add(pa.table({"a": range(300, 400)}))

    fragments = tbl.get_fragments()
    assert len(fragments) == 4

    # skip_frags=2 skips the first 2 fragments, returns remaining 2
    tasks = list(plan_read(tbl.uri, tbl_ref, ["a"], skip_frags=2)[0])
    assert len(tasks) == 2

    # Verify the tasks correspond to the correct fragments (fragments 2 and 3)
    frag_ids = {t.dest_frag_id() for t in tasks}
    expected_frag_ids = {fragments[2].fragment_id, fragments[3].fragment_id}
    assert frag_ids == expected_frag_ids


def test_plan_with_skip_frags_and_num_frags(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)

    tbl = db.create_table("t", pa.table({"a": range(100)}))
    tbl.add(pa.table({"a": range(100, 200)}))
    tbl.add(pa.table({"a": range(200, 300)}))
    tbl.add(pa.table({"a": range(300, 400)}))

    fragments = tbl.get_fragments()
    assert len(fragments) == 4

    # skip_frags=1, num_frags=2 → fragments 1 and 2 only
    tasks = list(plan_read(tbl.uri, tbl_ref, ["a"], skip_frags=1, num_frags=2)[0])
    assert len(tasks) == 2

    frag_ids = {t.dest_frag_id() for t in tasks}
    expected_frag_ids = {fragments[1].fragment_id, fragments[2].fragment_id}
    assert frag_ids == expected_frag_ids


def test_plan_with_skip_frags_beyond_end(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)

    tbl = db.create_table("t", pa.table({"a": range(100)}))
    tbl.add(pa.table({"a": range(100, 200)}))

    fragments = tbl.get_fragments()
    assert len(fragments) == 2

    # skip_frags beyond total fragments → no tasks
    tasks = list(plan_read(tbl.uri, tbl_ref, ["a"], skip_frags=5)[0])
    assert len(tasks) == 0


def test_udf_with_arrow_params(tmp_path: Path, tbl_ref: TableReference) -> None:
    @udf(data_type=pa.int32())
    def batch_udf(a: pa.Array, b: pa.Array) -> pa.Array:
        assert a == pa.array([1, 2, 3])
        assert b == pa.array([4, 5, 6])
        return pc.cast(pc.add(a, b), pa.int32())

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [4, 5, 6]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"c": batch_udf},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
    )
    results, direct_result, cnt_udf_computed = applier.run(
        next(plan_read(tbl.uri, tbl_ref, ["a", "b"], batch_size=16)[0])
    )
    assert direct_result is None
    assert len(results) == 1
    batch = store[results[0].checkpoint_key]
    assert batch == pa.RecordBatch.from_pydict(
        {
            "c": pa.array([5, 7, 9], type=pa.int32()),
            "_rowaddr": pa.array([0, 1, 2], pa.uint64()),
        },
    )
    assert cnt_udf_computed == 3


def test_udf_with_arrow_struct(tmp_path: Path, tbl_ref: TableReference) -> None:
    struct_type = pa.struct([("rpad", pa.string()), ("lpad", pa.string())])

    @udf(data_type=struct_type)
    def struct_udf(a: pa.Array, b: pa.Array) -> pa.Array:
        assert a == pa.array([1, 2, 3])
        assert b == pa.array([4, 5, 6])
        rpad = pc.ascii_rpad(pc.cast(a, target_type="string"), 4, padding="0")
        lpad = pc.ascii_lpad(pc.cast(a, target_type="string"), 4, padding="0")
        return pc.make_struct(rpad, lpad, field_names=["rpad", "lpad"])

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [4, 5, 6]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"c": struct_udf},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
    )
    results, direct_result, cnt_udf_computed = applier.run(
        next(plan_read(tbl.uri, tbl_ref, ["a", "b"], batch_size=16)[0])
    )
    assert direct_result is None
    assert len(results) == 1
    batch = store[results[0].checkpoint_key]
    # Build the expected RecordBatch
    # The function calls produce ["1000", "2000", "3000"] for rpad
    # and ["0001", "0002", "0003"] for lpad
    expected_batch = pa.RecordBatch.from_arrays(
        [
            pa.StructArray.from_arrays(
                [
                    pa.array(["1000", "2000", "3000"]),
                    pa.array(["0001", "0002", "0003"]),
                ],
                names=["rpad", "lpad"],
            ),
            pa.array([0, 1, 2], pa.uint64()),
        ],
        ["c", "_rowaddr"],
    )

    assert batch == expected_batch
    assert cnt_udf_computed == 3


def test_plan_read_supports_struct_field_projection(tmp_path: Path) -> None:
    # Create a dataset with a struct column
    struct_type = pa.struct([("left", pa.string()), ("right", pa.string())])
    tbl = pa.table(
        {
            "info": pa.array(
                [
                    {"left": "alpha", "right": "one"},
                    {"left": "beta", "right": "two"},
                ],
                type=struct_type,
            )
        }
    )

    ds_path = tmp_path / "ds.lance"
    lance.write_dataset(tbl, ds_path, max_rows_per_file=16)

    tbl_ref = TableReference(table_id=["ds"], version=None, db_uri=str(tmp_path))

    # columns includes a dotted struct field
    plan, _ = plan_read(str(ds_path), tbl_ref, columns=["info.left"], batch_size=1024)

    task = next(iter(plan))
    batches = list(task.to_batches())
    assert len(batches) == 1
    batch = batches[0]
    # Should project only the requested sub-field plus row address
    assert "info.left" in batch.schema.names
    assert "info" not in batch.schema.names


def test_plan_read_with_udf_projects_struct_field(tmp_path: Path) -> None:
    struct_type = pa.struct([("left", pa.string()), ("right", pa.string())])
    tbl = pa.table(
        {
            "info": pa.array(
                [
                    {"left": "alpha", "right": "one"},
                    {"left": "beta", "right": "two"},
                ],
                type=struct_type,
            )
        }
    )

    ds_path = tmp_path / "ds_udf.lance"
    lance.write_dataset(tbl, ds_path, max_rows_per_file=16)

    tbl_ref = TableReference(table_id=["ds_udf"], version=None, db_uri=str(tmp_path))

    @udf(data_type=pa.string(), input_columns=["info.left"])
    def left_upper(left: pa.Array) -> pa.Array:  # pyright: ignore[reportReturnType]
        return pc.utf8_upper(left)

    map_task = BackfillUDFTask(
        udfs={"c": left_upper},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    plan, _ = plan_read(
        str(ds_path),
        tbl_ref,
        columns=["info.left"],
        batch_size=1024,
        map_task=map_task,
    )

    task = next(iter(plan))
    batches = list(task.to_batches())
    assert len(batches) == 1
    names = set(batches[0].schema.names)
    assert "info.left" in names
    assert "info" not in names


def test_plan_read_canonicalizes_case_insensitive_struct_field(
    tmp_path: Path,
) -> None:
    struct_type = pa.struct([("UserId", pa.int32()), ("Other", pa.string())])
    tbl = pa.table(
        {
            "MetaData": pa.array(
                [
                    {"UserId": 1, "Other": "a"},
                    {"UserId": 2, "Other": "b"},
                ],
                type=struct_type,
            )
        }
    )

    ds_path = tmp_path / "ds_case_udf.lance"
    lance.write_dataset(tbl, ds_path, max_rows_per_file=16)

    tbl_ref = TableReference(
        table_id=["ds_case_udf"], version=None, db_uri=str(tmp_path)
    )

    @udf(data_type=pa.int32(), input_columns=["metadata.userid"])
    def plus_one(user_id: pa.Array) -> pa.Array:  # pyright: ignore[reportReturnType]
        return pc.add(user_id, 1)

    map_task = BackfillUDFTask(
        udfs={"score": plus_one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    plan, _ = plan_read(
        str(ds_path),
        tbl_ref,
        columns=["metadata.userid"],
        batch_size=1024,
        map_task=map_task,
    )

    task = next(iter(plan))
    assert isinstance(task, ScanTask)
    assert task.columns == ["MetaData.UserId"]
    batch = next(iter(task.to_batches()))
    assert batch.schema.names[:1] == ["MetaData.UserId"]
    assert plus_one(batch).to_pylist() == [2, 3]


def test_validate_backfill_args_rejects_nested_output_target(tmp_path: Path) -> None:
    from geneva.runners.ray.pipeline import validate_backfill_args

    db = connect(tmp_path)
    struct_type = pa.struct([("user_id", pa.int64())])
    table = db.create_table(
        "nested_output_target",
        pa.table({"metadata": pa.array([{"user_id": 1}], type=struct_type)}),
    )

    with pytest.raises(
        ValueError,
        match="Nested backfill output target .* top-level virtual columns",
    ):
        validate_backfill_args(table, "metadata.user_id")


def test_udf_with_arrow_array(tmp_path: Path, tbl_ref: TableReference) -> None:
    array_type = pa.list_(pa.int64())

    @udf(data_type=array_type)
    def array_udf(a: pa.Array, b: pa.Array) -> pa.Array:
        assert a == pa.array([1, 2, 3])
        assert b == pa.array([4, 5, 6])
        arr = [
            [val] * cnt for val, cnt in zip(a.to_pylist(), b.to_pylist(), strict=True)
        ]
        c = pa.array(arr, type=pa.list_(pa.int64()))
        return c

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "b": [4, 5, 6]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"c": array_udf},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
    )
    results, direct_result, cnt_udf_computed = applier.run(
        next(plan_read(tbl.uri, tbl_ref, ["a", "b"], batch_size=16)[0])
    )
    assert direct_result is None
    assert len(results) == 1
    batch = store[results[0].checkpoint_key]

    # Build the expected RecordBatch
    expected_c = pa.array(
        [[1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3, 3]], type=pa.list_(pa.int64())
    )

    expected_batch = pa.RecordBatch.from_arrays(
        [expected_c, pa.array([0, 1, 2], pa.uint64())], ["c", "_rowaddr"]
    )
    assert batch == expected_batch
    assert cnt_udf_computed == 3


def test_compute_checkpoint_end_is_logical_on_delete_fragments(
    tbl_ref: TableReference,
) -> None:
    """On fragments with deletion vectors, checkpoint ``end`` must come from
    the batch's row count (logical span), not ``_rowaddr`` (physical).

    Deriving it from the physical rowaddr produced ``_range-`` keys claiming
    more logical rows than the blob contains; recovery/replacement/resume
    then skipped recomputing rows no blob held, and the writer null-filled
    them as if they were deleted (the delete-fragment orphan-null bug).
    """
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(udfs={"one": one}),
        checkpoint_uri="memory",
    )

    def make_task(physical: int, logical: int) -> ScanTask:
        return ScanTask(
            uri="db://example/tbl",
            table_ref=tbl_ref,
            columns=["a"],
            frag_id=0,
            offset=0,
            limit=logical,
            fragment_physical_rows=physical,
            fragment_logical_rows=logical,
        )

    # 512 live rows whose physical addresses drift ahead by 20 deleted slots.
    batch = pa.RecordBatch.from_arrays(
        [
            pa.array(range(512), type=pa.int64()),
            pa.array([i + 20 for i in range(512)], type=pa.uint64()),
        ],
        names=["one", "_rowaddr"],
    )

    # Delete fragment: end = start + rows, physical drift ignored.
    end = applier._compute_checkpoint_end(
        make_task(2048, 2000), batch, start=0, checkpoint_size=512
    )
    assert end == 512

    # No deletes: the rowaddr-based end is preserved (legacy sparse batches).
    end = applier._compute_checkpoint_end(
        make_task(2048, 2048), batch, start=0, checkpoint_size=512
    )
    assert end == 532  # last physical rowaddr + 1

    # Task-end clamp still applies on delete fragments.
    end = applier._compute_checkpoint_end(
        make_task(600, 500), batch, start=100, checkpoint_size=512
    )
    assert end == 500


def test_checkpoint_ranges_truthful_on_delete_fragment(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """End-to-end through the applier: every ``_range-START-END`` checkpoint
    written for a deletion-vector fragment must contain exactly END-START
    rows, with contiguous logical ranges tiling the fragment."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": list(range(4000))}))
    tbl.delete("a % 100 = 7")  # 1% deleted -> physical != logical

    frag = tbl.to_lance().get_fragment(0)
    logical = frag.count_rows()
    assert frag.physical_rows == 4000
    assert logical == 3960

    map_task = BackfillUDFTask(
        udfs={"one": one},
        override_batch_size=256,
        min_checkpoint_size=256,
        max_checkpoint_size=256,
    )
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    tasks, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        task_size=1024,
        map_task=map_task,
        checkpoint_store=store,
    )
    applier = CheckpointingApplier(
        map_task=map_task,
        checkpoint_uri=store.root,
        checkpoint_pending_bytes_target=1,  # flush each slice separately
    )

    cursor = 0
    for task in tasks:
        checkpoints, _, _ = applier.run(task)
        for c in checkpoints:
            suffix = c.checkpoint_key.rsplit("_range-", 1)[1]
            ks, ke = (int(x) for x in suffix.split("-"))
            blob = store[c.checkpoint_key]
            assert ks == cursor, f"range start {ks} != expected {cursor}"
            assert ke - ks == blob.num_rows, (
                f"key {c.checkpoint_key} claims {ke - ks} rows, "
                f"blob has {blob.num_rows}"
            )
            cursor = ke
    assert cursor == logical


def test_compute_resume_ranges_tiles_covered_and_missing_runs() -> None:
    """Every row is planned exactly once, split at coverage boundaries so each
    task is either fully covered (reused from checkpoints) or fully missing
    (recomputed)."""
    ranges = _compute_resume_ranges(
        total_rows=10, task_size=3, covered=[(0, 5), (7, 10)]
    )
    assert ranges == [(0, 3), (3, 2), (5, 2), (7, 3)]
    # Full tiling: covers [0, 10) exactly once.
    assert sum(limit for _, limit in ranges) == 10

    # No coverage: plain task_size tiling.
    assert _compute_resume_ranges(total_rows=7, task_size=3, covered=[]) == [
        (0, 3),
        (3, 3),
        (6, 1),
    ]

    # Coverage extending past the fragment is clipped.
    assert _compute_resume_ranges(total_rows=6, task_size=10, covered=[(4, 9)]) == [
        (0, 4),
        (4, 2),
    ]

    # Degenerate task size: one task per run.
    assert _compute_resume_ranges(total_rows=10, task_size=0, covered=[(2, 4)]) == [
        (0, 2),
        (2, 2),
        (4, 6),
    ]


# Tests for fragment-level checkpoint functionality


def test_parse_checkpoint_range_key_valid() -> None:
    prefix = "udf-test_frag-x_ver-1_col-a_where-abc_uri-def"
    key = f"{prefix}_frag-12_range-3-10"
    parsed = _parse_checkpoint_range_key(key)
    assert parsed == (prefix, 12, 3, 10)


@pytest.mark.parametrize(
    "key",
    [
        "no-frag-or-range",
        "prefix_frag-1_range-10-10",  # empty range
        "prefix_frag-1_range-10-5",  # inverted range
        "prefix_frag-abc_range-0-1",  # invalid frag id
        "prefix_frag-1_range-foo-2",  # invalid start
        "prefix_range-0-1",  # missing frag marker
        "prefix_frag-1_range-0-1-extra",  # trailing junk
    ],
)
def test_parse_checkpoint_range_key_invalid(key: str) -> None:
    assert _parse_checkpoint_range_key(key) is None


def test_parse_udf_version_from_fragment_checkpoint_key() -> None:
    key = (
        "udf-name_col-output_ver-in-name_ver-v2_col-output"
        "_where-aa_uri-bb_srcfiles-cc_frag-12"
    )

    assert _parse_udf_version_from_fragment_checkpoint_key(key, "output") == "v2"
    assert (
        _parse_udf_version_from_fragment_checkpoint_key(f"{key}_range-0-10", "output")
        is None
    )
    wrong_column_key = (
        "udf-name_col-output_ver-v2_col-other_where-aa_uri-bb_srcfiles-cc_frag-12"
    )
    assert (
        _parse_udf_version_from_fragment_checkpoint_key(wrong_column_key, "output")
        is None
    )
    assert _parse_udf_version_from_fragment_checkpoint_key(key, "other") is None


def test_index_checkpoint_ranges_in_memory_store() -> None:
    store = CheckpointStore.from_uri("memory")
    prefix_a = "udf-a_ver-1_col-x_where-h_uri-u"
    prefix_b = "udf-b_ver-2_col-y_where-h_uri-u"

    valid_keys = [
        f"{prefix_a}_frag-0_range-0-10",
        f"{prefix_a}_frag-0_range-10-20",
        f"{prefix_a}_frag-2_range-5-9",
        f"{prefix_b}_frag-1_range-0-4",
    ]
    invalid_keys = [
        "garbage",
        f"{prefix_a}_frag-0_range-5-5",
        f"{prefix_a}_frag-foo_range-0-1",
        f"{prefix_a}_range-0-1",
    ]

    batch = pa.RecordBatch.from_pydict({"a": [1]})
    for key in valid_keys + invalid_keys:
        store[key] = batch

    all_keys, ranges_by_prefix = _index_checkpoint_ranges(checkpoint_store=store)

    assert all_keys == set(valid_keys + invalid_keys)
    assert sorted(ranges_by_prefix[prefix_a][0]) == [(0, 10), (10, 20)]
    assert ranges_by_prefix[prefix_a][2] == [(5, 9)]
    assert ranges_by_prefix[prefix_b][1] == [(0, 4)]


@pytest.mark.parametrize(
    "store_cls",
    [
        _NoPayloadReadFlatLanceCheckpointStore,
        _NoPayloadReadHierarchicalLanceCheckpointStore,
    ],
)
def test_store_udf_mismatch_uses_checkpoint_keys_without_payload_reads(
    tmp_path: Path,
    store_cls: type[FlatLanceCheckpointStore | HierarchicalLanceCheckpointStore],
) -> None:
    store = store_cls(str(tmp_path / store_cls.__name__))
    batch = pa.RecordBatch.from_pydict({"file": ["fragment_0.lance"]})
    current_prefix = (
        "udf-old_name_ver-in-name_ver-current_col-output_where-aa_uri-bb_srcfiles-cc"
    )
    wrong_column_prefix = (
        "udf-name_col-output_ver-stale_col-other_where-aa_uri-bb_srcfiles-cc"
    )
    stale_range_prefix = "udf-old_name_ver-stale_col-output_where-aa_uri-bb_srcfiles-cc"
    stale_fragment_prefix = (
        "udf-even_older_name_ver-stale_col-output_where-aa_uri-bb_srcfiles-cc"
    )

    store[f"{current_prefix}_frag-0"] = batch
    store[f"{wrong_column_prefix}_frag-0"] = batch
    store[f"{stale_range_prefix}_frag-0_range-0-10"] = batch

    assert not store.has_udf_version_mismatch("output", "current")

    store[f"{stale_fragment_prefix}_frag-1"] = batch

    assert store.has_udf_version_mismatch("output", "current")


@pytest.mark.parametrize(
    "store_cls",
    [
        _NoPayloadReadFlatLanceCheckpointStore,
        _NoPayloadReadHierarchicalLanceCheckpointStore,
    ],
)
def test_store_udf_mismatch_treats_unparseable_fragment_key_as_mismatch(
    tmp_path: Path,
    store_cls: type[FlatLanceCheckpointStore | HierarchicalLanceCheckpointStore],
) -> None:
    store = store_cls(str(tmp_path / store_cls.__name__))
    key = "udf-legacy_col-output_where-aa_uri-bb_srcfiles-cc_frag-0"
    store[key] = pa.RecordBatch.from_pydict({"file": ["fragment_0.lance"]})

    assert store.has_udf_version_mismatch("output", "current")


def test_check_fragment_data_file_exists_no_checkpoint(tmp_path: Path) -> None:
    """Test _check_fragment_data_file_exists when fragment is not checkpointed."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])

    # Fragment 0 should not exist in checkpoint store yet
    exists = _check_fragment_data_file_exists(
        tbl.uri, 0, map_task, store, src_files_hash=src_files_hash
    )
    assert not exists


def test_check_fragment_data_file_exists_with_staging_file(tmp_path: Path) -> None:
    """Test _check_fragment_data_file_exists when fragment file exists in staging."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])

    # Create a checkpoint entry for fragment 0
    dedupe_key = _get_fragment_dedupe_key(
        tbl.uri, 0, map_task, src_files_hash=src_files_hash
    )
    fake_file_path = "test_fragment_0.lance"
    store[dedupe_key] = pa.RecordBatch.from_pydict({"file": [fake_file_path]})

    # Create the staging file as a valid, non-empty Lance data file. A 0-byte
    # touch is now rejected as a stale/incomplete leftover (GEN-530), so the
    # staged file must actually be readable to count as skippable.
    from lance.file import LanceFileWriter

    staging_dir = Path(URL(tbl.uri).path) / "data"
    staging_dir.mkdir(exist_ok=True)
    staging_file = staging_dir / fake_file_path
    writer = LanceFileWriter(str(staging_file))
    writer.write_batch(pa.table({"one": [1, 1, 1]}))
    writer.close()

    # Should return True since a valid file exists in staging
    exists = _check_fragment_data_file_exists(
        tbl.uri, 0, map_task, store, src_files_hash=src_files_hash
    )
    assert exists


def test_check_fragment_data_file_exists_rejects_empty_staged_file_gen530(
    tmp_path: Path,
) -> None:
    """GEN-530: a 0-byte/unreadable staged file must NOT count as a skippable
    checkpoint -- trusting it on mere existence leaves the fragment NULL."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    dedupe_key = _get_fragment_dedupe_key(
        tbl.uri, 0, map_task, src_files_hash=src_files_hash
    )
    fake_file_path = "stale_fragment_0.lance"
    store[dedupe_key] = pa.RecordBatch.from_pydict({"file": [fake_file_path]})

    # Crash-recovery leftover: the file exists but is empty (0 bytes).
    staging_dir = Path(URL(tbl.uri).path) / "data"
    staging_dir.mkdir(exist_ok=True)
    (staging_dir / fake_file_path).touch()

    # Existence is not enough -- the empty file is not a valid output, so the
    # fragment must not be skipped.
    assert (
        _check_fragment_data_file_exists(
            tbl.uri, 0, map_task, store, src_files_hash=src_files_hash
        )
        is None
    )


def test_check_fragment_data_file_exists_rejects_row_count_mismatch_gen530(
    tmp_path: Path,
) -> None:
    """GEN-530: a staged file whose row count does not match the fragment is a
    partial/stale leftover and must not be skipped."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    dedupe_key = _get_fragment_dedupe_key(
        tbl.uri, 0, map_task, src_files_hash=src_files_hash
    )
    fake_file_path = "partial_fragment_0.lance"
    store[dedupe_key] = pa.RecordBatch.from_pydict({"file": [fake_file_path]})

    from lance.file import LanceFileWriter

    staging_dir = Path(URL(tbl.uri).path) / "data"
    staging_dir.mkdir(exist_ok=True)
    # Valid Lance file, but only 1 row -- fragment 0 has 3 (partial write).
    writer = LanceFileWriter(str(staging_dir / fake_file_path))
    writer.write_batch(pa.table({"one": [1]}))
    writer.close()

    # Row count (1) != fragment rows (3) -> partial leftover -> not skippable.
    assert (
        _check_fragment_data_file_exists(
            tbl.uri, 0, map_task, store, src_files_hash=src_files_hash, expected_rows=3
        )
        is None
    )
    # Without expected_rows, a non-empty file is accepted (back-compat).
    assert (
        _check_fragment_data_file_exists(
            tbl.uri, 0, map_task, store, src_files_hash=src_files_hash
        )
        is not None
    )


def test_plan_read_skips_fragment_with_deletes_when_staged_file_is_physical(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """A fragment with deletions whose staged output is physically aligned
    (filled to physical_rows, as the writer produces) must still be skipped on
    resume. Guards against comparing the staged file against the smaller logical
    (post-deletion) count, which would reject the writer's own output and
    silently disable resume-from-staged for any deletion-bearing fragment."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": list(range(10))}))
    tbl.delete("a < 3")  # physical_rows=10, num_deletions=3, count_rows()=7

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    tbl.add_columns({"a2": double_a})  # lazy: no fragment covers a2 yet

    frag = tbl.to_lance().get_fragment(0)
    assert frag.num_deletions == 3
    assert frag.physical_rows == 10
    assert frag.count_rows() == 7

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"a2": double_a},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    dedupe_key = _get_fragment_dedupe_key(
        tbl.uri, 0, map_task, src_files_hash=src_files_hash
    )
    fake_file = "del_frag0.lance"
    store[dedupe_key] = pa.RecordBatch.from_pydict({"file": [fake_file]})

    # Writer fills staged files to physical_rows (10), not the logical 7.
    from lance.file import LanceFileWriter

    staging_dir = Path(URL(tbl.uri).path) / "data"
    staging_dir.mkdir(exist_ok=True)
    writer = LanceFileWriter(str(staging_dir / fake_file))
    writer.write_batch(pa.table({"a2": [0] * frag.physical_rows}))
    writer.close()

    _, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=16,
        map_task=map_task,
        checkpoint_store=store,
    )

    # The physical-aligned staged file is a complete output -> fragment skipped.
    assert 0 in pipeline_args["skipped_fragments"]


def test_check_fragment_data_file_exists_with_cloud_url() -> None:
    """Test _check_fragment_data_file_exists with cloud URLs."""
    # Create a mock checkpoint store
    store = {}
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    # Test with S3 URL - should not crash but return False since no real file
    s3_uri = "s3://test-bucket/dataset"
    exists = _check_fragment_data_file_exists(s3_uri, 0, map_task, store)
    assert not exists

    # Test with GCS URL - should not crash but return False since no real file
    gcs_uri = "gs://test-bucket/dataset"
    exists = _check_fragment_data_file_exists(gcs_uri, 0, map_task, store)
    assert not exists


def test_find_output_data_file_requires_full_output_field_coverage() -> None:
    class _FakeFragment:
        def __init__(self, data_files: list[object]) -> None:
            self._data_files = data_files

        def data_files(self) -> list[object]:
            return self._data_files

    partial_match = type("FakeDataFile", (), {"fields": [3, 5]})()
    full_match = type("FakeDataFile", (), {"fields": [5, 6, 7]})()
    frag = _FakeFragment([partial_match, full_match])

    assert _find_output_data_file_in_fragment(frag, frozenset({5, 6})) is full_match
    assert _find_output_data_file_in_fragment(frag, frozenset({5, 8})) is None


def test_plan_read_validates_checkpoint_payload_before_skipping_committed_fragment(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "a2": [2, 4, 6]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"a2": double_a},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    dataset = tbl.to_lance()
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    dedupe_key = _get_fragment_dedupe_key(
        tbl.uri,
        0,
        map_task,
        dataset_version=dataset.version,
        src_files_hash=src_files_hash,
    )
    expected_path = next(
        df.path
        for df in dataset.get_fragment(0).data_files()
        if set(df.fields) >= set(extract_field_ids(dataset.lance_schema, "a2"))
    )
    store[dedupe_key] = pa.RecordBatch.from_pydict(
        {
            "file": [expected_path],
            "output_field_ids": [
                json.dumps(sorted(extract_field_ids(dataset.lance_schema, "a2")))
            ],
        }
    )

    checkpoint_probe_calls: list[tuple[object, ...]] = []
    original_probe = apply_module._check_fragment_data_file_exists

    def _record_checkpoint_probe(*args: object, **kwargs: object) -> str | None:
        checkpoint_probe_calls.append(args)
        return original_probe(*args, **kwargs)

    monkeypatch.setattr(
        apply_module,
        "_check_fragment_data_file_exists",
        _record_checkpoint_probe,
    )

    plans, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=16,
        map_task=map_task,
        checkpoint_store=store,
    )

    assert list(plans) == []
    skipped_fragments = pipeline_args["skipped_fragments"]
    assert 0 in skipped_fragments
    data_file, row_count = skipped_fragments[0]
    assert row_count == 3
    assert checkpoint_probe_calls
    assert set(data_file.fields) >= set(extract_field_ids(dataset.lance_schema, "a2"))


def test_plan_read_does_not_skip_committed_fragment_with_stale_checkpoint_payload(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "a2": [2, 4, 6]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"a2": double_a},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    dataset = tbl.to_lance()
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    dedupe_key = _get_fragment_dedupe_key(
        tbl.uri,
        0,
        map_task,
        dataset_version=dataset.version,
        src_files_hash=src_files_hash,
    )
    store[dedupe_key] = pa.RecordBatch.from_pydict({"file": ["stale-file.lance"]})

    checkpoint_probe_calls = 0

    def _stale_checkpoint_payload(*args: object, **kwargs: object) -> None:
        nonlocal checkpoint_probe_calls
        checkpoint_probe_calls += 1
        return None

    monkeypatch.setattr(
        apply_module,
        "_check_fragment_data_file_exists",
        _stale_checkpoint_payload,
    )

    plans, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=16,
        map_task=map_task,
        checkpoint_store=store,
    )

    task_list = list(plans)
    assert checkpoint_probe_calls == 1
    assert len(task_list) == 1
    assert pipeline_args["skipped_fragments"] == {}


def test_plan_read_counts_full_fragment_rows_for_committed_incremental_fragments(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "a2": [2, 4, 6]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"a2": double_a},
        where="a2 IS NULL",
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    dataset = tbl.to_lance()
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    dedupe_key = _get_fragment_dedupe_key(
        tbl.uri,
        0,
        map_task,
        dataset_version=dataset.version,
        src_files_hash=src_files_hash,
    )
    expected_path = next(
        df.path
        for df in dataset.get_fragment(0).data_files()
        if set(df.fields) >= set(extract_field_ids(dataset.lance_schema, "a2"))
    )
    store[dedupe_key] = pa.RecordBatch.from_pydict(
        {
            "file": [expected_path],
            "output_field_ids": [
                json.dumps(sorted(extract_field_ids(dataset.lance_schema, "a2")))
            ],
        }
    )

    plans, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=16,
        map_task=map_task,
        checkpoint_store=store,
    )

    assert list(plans) == []
    assert pipeline_args["skipped_fragments"][0][1] == 3
    assert pipeline_args["skipped_stats"]["rows"] == 3


@pytest.mark.parametrize("use_legacy_key", [False, True], ids=["primary", "legacy"])
def test_plan_read_falls_back_when_checkpoint_indexing_fails(
    tmp_path: Path,
    tbl_ref: TableReference,
    monkeypatch: pytest.MonkeyPatch,
    use_legacy_key: bool,
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "a2": [2, 4, 6]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"a2": double_a},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    dataset = tbl.to_lance()
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    if use_legacy_key:
        checkpoint_key = _legacy_fragment_dedupe_key(tbl.uri, 0, map_task)
    else:
        checkpoint_key = _get_fragment_dedupe_key(
            tbl.uri,
            0,
            map_task,
            dataset_version=dataset.version,
            src_files_hash=src_files_hash,
        )
    expected_path = next(
        df.path
        for df in dataset.get_fragment(0).data_files()
        if set(df.fields) >= set(extract_field_ids(dataset.lance_schema, "a2"))
    )
    store[checkpoint_key] = pa.RecordBatch.from_pydict(
        {
            "file": [expected_path],
            "output_field_ids": [
                json.dumps(sorted(extract_field_ids(dataset.lance_schema, "a2")))
            ],
        }
    )

    def _raise_index_error(*args: object, **kwargs: object) -> NoReturn:
        raise RuntimeError("checkpoint listing unavailable")

    checkpoint_probe_calls = 0

    original_probe = apply_module._check_fragment_data_file_exists

    def _record_checkpoint_probe(*args: object, **kwargs: object) -> str | None:
        nonlocal checkpoint_probe_calls
        checkpoint_probe_calls += 1
        return original_probe(*args, **kwargs)

    monkeypatch.setattr(apply_module, "_index_checkpoint_ranges", _raise_index_error)
    monkeypatch.setattr(
        apply_module,
        "_check_fragment_data_file_exists",
        _record_checkpoint_probe,
    )

    plans, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=16,
        map_task=map_task,
        checkpoint_store=store,
    )

    assert list(plans) == []
    assert checkpoint_probe_calls == 1
    assert pipeline_args["skipped_fragments"][0][1] == 3


def test_plan_read_with_skipped_fragments(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Test that plan_read correctly identifies and skips fragments."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))
    tbl.add(pa.table({"a": [4, 5, 6]}))  # Add second fragment

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])

    # Create checkpoint for fragment 0 only
    dedupe_key = _get_fragment_dedupe_key(
        tbl.uri, 0, map_task, src_files_hash=src_files_hash
    )
    fake_file_path = "fragment_0.lance"
    store[dedupe_key] = pa.RecordBatch.from_pydict({"file": [fake_file_path]})

    # Create a valid 3-row staging file for fragment 0; a 0-byte touch is now
    # rejected as a stale leftover (GEN-530).
    from lance.file import LanceFileWriter

    staging_dir = Path(URL(tbl.uri).path) / "data"
    staging_dir.mkdir(exist_ok=True)
    staging_file = staging_dir / fake_file_path
    _w = LanceFileWriter(str(staging_file))
    _w.write_batch(pa.table({"one": [1, 1, 1]}))
    _w.close()

    # Plan read with checkpoint information
    plans, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=16,
        map_task=map_task,
        checkpoint_store=store,
    )

    # Should still have tasks for fragment 1 (not checkpointed)
    task_list = list(plans)
    assert len(task_list) > 0  # Fragment 1 should have tasks

    # Check that skipped_fragments contains fragment 0
    assert "skipped_fragments" in pipeline_args
    skipped_fragments = pipeline_args["skipped_fragments"]
    assert 0 in skipped_fragments
    assert 1 not in skipped_fragments  # Fragment 1 should not be skipped

    # Verify the DataFile uses the dataset's data_storage_version
    data_file, row_count = skipped_fragments[0]
    assert data_file.file_major_version == 2
    assert data_file.file_minor_version == 1  # Lance defaults to 2.1
    assert row_count > 0


@pytest.mark.parametrize("data_storage_version", ["2.0", "2.1"])
def test_plan_read_skipped_fragment_uses_dataset_version(
    tmp_path: Path, tbl_ref: TableReference, data_storage_version: str
) -> None:
    """Skipped-fragment DataFile must match the dataset's data_storage_version."""
    # Create dataset with explicit data_storage_version
    data = pa.table({"a": [1, 2, 3]})
    ds_path = str(tmp_path / "tbl.lance")
    lance.write_dataset(data, ds_path, data_storage_version=data_storage_version)
    lance.write_dataset(
        pa.table({"a": [4, 5, 6]}),
        ds_path,
        mode="append",
    )

    db = connect(tmp_path)
    tbl = db.open_table("tbl")

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    tbl.add_columns({"a2": double_a})

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"a2": double_a},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])

    # Checkpoint fragment 0
    dedupe_key = _get_fragment_dedupe_key(
        tbl.uri, 0, map_task, src_files_hash=src_files_hash
    )
    fake_file = "fragment_0.lance"
    store[dedupe_key] = pa.RecordBatch.from_pydict({"file": [fake_file]})
    # Stage a valid Lance data file whose row count matches fragment 0 (3 rows).
    # A 0-byte touch is now rejected as a stale leftover (GEN-530).
    from lance.file import LanceFileWriter

    staging_dir = Path(URL(tbl.uri).path) / "data"
    staging_dir.mkdir(exist_ok=True)
    _staged_writer = LanceFileWriter(str(staging_dir / fake_file))
    _staged_writer.write_batch(pa.table({"a2": [2, 4, 6]}))
    _staged_writer.close()

    _, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=16,
        map_task=map_task,
        checkpoint_store=store,
    )

    skipped = pipeline_args["skipped_fragments"]
    assert 0 in skipped
    df, row_count = skipped[0]
    major, minor = data_storage_version.split(".")
    assert df.file_major_version == int(major)
    assert df.file_minor_version == int(minor)
    assert row_count > 0


def test_plan_read_no_checkpointing_params(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Test that plan_read works normally when no checkpointing params are provided."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    # Plan read without checkpoint information
    plans, pipeline_args = plan_read(tbl.uri, tbl_ref, ["a"], batch_size=16)

    # Should have tasks for all fragments
    task_list = list(plans)
    assert len(task_list) == 1

    # Should have empty skipped_fragments
    assert "skipped_fragments" in pipeline_args
    skipped_fragments = pipeline_args["skipped_fragments"]
    assert len(skipped_fragments) == 0


def test_plan_read_caches_dataset_version(
    tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    class _FakeFragment:
        def __init__(self, fragment_id: int, rows: int) -> None:
            self.fragment_id = fragment_id
            self.physical_rows = rows
            self.num_deletions = 0

    class _FakeDataset:
        def __init__(self) -> None:
            self._version_reads = 0
            self._fragments = [_FakeFragment(0, 3), _FakeFragment(1, 2)]

        @property
        def version(self) -> int:
            self._version_reads += 1
            return 17

        def get_fragments(self) -> list[_FakeFragment]:
            return self._fragments

    fake_dataset = _FakeDataset()

    monkeypatch.setattr(apply_module.lance, "dataset", lambda uri: fake_dataset)

    plans, _ = plan_read("memory://fake", tbl_ref, ["a"], batch_size=2)

    task_list = list(plans)
    assert [task.version for task in task_list] == [17, 17, 17]
    assert fake_dataset._version_reads == 1


def test_plan_read_uses_logical_rows_for_fragments_with_deletes(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [0, 1, 2, 3]}))
    tbl.delete("a % 2 == 1")

    plans, pipeline_args = plan_read(tbl.uri, tbl_ref, ["a"], batch_size=1)

    task_list = list(plans)
    assert len(task_list) == 2
    assert [task.offset for task in task_list] == [0, 1]
    assert len(pipeline_args["skipped_fragments"]) == 0


def test_plan_read_len_matches_actual_filtered_tasks(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "a2": [2, 4, 6]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    plans, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=16,
        map_task=BackfillUDFTask(
            udfs={"a2": double_a},
            where="a2 IS NULL",
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=InMemoryCheckpointStore(),
        default_where_generated=True,
    )

    assert len(plans) == 0
    task_list = list(plans)
    assert len(task_list) == 0


def test_plan_read_skips_generated_default_where_filter_count(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    tbl.add_columns({"a2": double_a})
    dataset = tbl.to_lance()
    frag_type = type(dataset.get_fragment(0))
    original_count_rows = frag_type.count_rows
    filter_calls: list[str] = []

    def _count_rows(self, *args: object, **kwargs: object) -> int:
        filter_expr = kwargs.get("filter")
        if args:
            filter_expr = args[0]
        if filter_expr is not None:
            filter_calls.append(str(filter_expr))
        return original_count_rows(self, *args, **kwargs)

    monkeypatch.setattr(frag_type, "count_rows", _count_rows)

    plans, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=16,
        map_task=BackfillUDFTask(
            udfs={"a2": double_a},
            where="a2 IS NULL",
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=InMemoryCheckpointStore(),
        default_where_generated=True,
    )

    assert len(list(plans)) == 1
    assert filter_calls == []


def test_plan_read_skips_explicit_where_filter_count_when_no_output_file(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Explicit where clauses skip the per-fragment count when the output
    column has no committed data file. The synth null-filler is a no-op
    against an already-null column, so workers can do the filtering safely.
    """
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    tbl.add_columns({"a2": double_a})
    dataset = tbl.to_lance()
    frag_type = type(dataset.get_fragment(0))
    original_count_rows = frag_type.count_rows
    filter_calls: list[str] = []

    def _count_rows(self, *args: object, **kwargs: object) -> int:
        filter_expr = kwargs.get("filter")
        if args:
            filter_expr = args[0]
        if filter_expr is not None:
            filter_calls.append(str(filter_expr))
        return original_count_rows(self, *args, **kwargs)

    monkeypatch.setattr(frag_type, "count_rows", _count_rows)

    plans, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=16,
        map_task=BackfillUDFTask(
            udfs={"a2": double_a},
            where="a2 IS NULL",
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=InMemoryCheckpointStore(),
        default_where_generated=False,
    )

    assert len(list(plans)) == 1
    assert filter_calls == []


def test_plan_read__skip_populated_filter_count_opt_in(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """With `_skip_populated_filter_count=True`, fragments with populated
    output column data also take the fast path — no `count_rows(filter=...)`
    on the driver. Worker carry-forward keeps existing values safe.
    """
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "a2": [2, 4, 6]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    dataset = tbl.to_lance()
    frag_type = type(dataset.get_fragment(0))
    original_count_rows = frag_type.count_rows
    filter_calls: list[str] = []

    def _count_rows(self, *args: object, **kwargs: object) -> int:
        filter_expr = kwargs.get("filter")
        if args:
            filter_expr = args[0]
        if filter_expr is not None:
            filter_calls.append(str(filter_expr))
        return original_count_rows(self, *args, **kwargs)

    monkeypatch.setattr(frag_type, "count_rows", _count_rows)

    plans, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=16,
        map_task=BackfillUDFTask(
            udfs={"a2": double_a},
            where="a2 IS NULL",
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=InMemoryCheckpointStore(),
        default_where_generated=True,
        _skip_populated_filter_count=True,
    )

    # Even though the fragment has populated a2 data, the opt-in flag skips
    # the count and emits a task. Worker carry-forward preserves the
    # existing values.
    assert len(list(plans)) == 1
    assert filter_calls == []


def test_plan_read_parallel_filter_count(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`_plan_filter_count_concurrency>1` dispatches per-fragment
    `count_rows(filter=where)` through a thread pool. Each populated
    fragment still gets exactly one count call, and the resulting plan
    matches the serial path.
    """
    import threading

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3, 4], "a2": [2, 4, 6, 8]}))
    tbl.add(pa.table({"a": [5, 6, 7, 8], "a2": [10, 12, 14, 16]}))
    tbl.add(pa.table({"a": [9, 10, 11, 12], "a2": [18, 20, 22, 24]}))
    tbl.add(pa.table({"a": [13, 14, 15, 16], "a2": [26, 28, 30, 32]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    dataset = tbl.to_lance()
    fragments = dataset.get_fragments()
    assert len(fragments) == 4

    frag_type = type(fragments[0])
    original_count_rows = frag_type.count_rows
    filter_calls: list[tuple[str, int]] = []
    main_thread_id = threading.get_ident()

    def _count_rows(self, *args: object, **kwargs: object) -> int:
        filter_expr = kwargs.get("filter")
        if args:
            filter_expr = args[0]
        if filter_expr is not None:
            filter_calls.append((str(filter_expr), threading.get_ident()))
        return original_count_rows(self, *args, **kwargs)

    monkeypatch.setattr(frag_type, "count_rows", _count_rows)

    plans, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=16,
        map_task=BackfillUDFTask(
            udfs={"a2": double_a},
            where="a2 IS NULL",
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=InMemoryCheckpointStore(),
        default_where_generated=True,
        _plan_filter_count_concurrency=4,
    )

    # All fragments are fully populated → filter matches zero rows → no
    # tasks. The prefetch must have run count_rows once per fragment.
    assert list(plans) == []
    assert [expr for expr, _ in filter_calls] == ["a2 IS NULL"] * 4
    # The prefetch should run count_rows on worker threads, not the
    # driver. This guards against accidentally collapsing back to a
    # single-threaded executor.
    assert all(tid != main_thread_id for _, tid in filter_calls)


def test_plan_read_serial_filter_count_when_concurrency_one(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`_plan_filter_count_concurrency=1` (the direct-caller default)
    keeps the synchronous in-loop `count_rows` path. The thread pool is
    only engaged when explicitly configured for parallel planning.
    """
    import threading

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "a2": [2, 4, 6]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    dataset = tbl.to_lance()
    frag_type = type(dataset.get_fragment(0))
    original_count_rows = frag_type.count_rows
    call_threads: list[int] = []
    main_thread_id = threading.get_ident()

    def _count_rows(self, *args: object, **kwargs: object) -> int:
        filter_expr = kwargs.get("filter")
        if args:
            filter_expr = args[0]
        if filter_expr is not None:
            call_threads.append(threading.get_ident())
        return original_count_rows(self, *args, **kwargs)

    monkeypatch.setattr(frag_type, "count_rows", _count_rows)

    plans, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=16,
        map_task=BackfillUDFTask(
            udfs={"a2": double_a},
            where="a2 IS NULL",
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=InMemoryCheckpointStore(),
        default_where_generated=True,
    )

    assert list(plans) == []
    assert len(call_threads) == 1
    assert call_threads[0] == main_thread_id


def test_plan_read_leaf_mode_skips_planner_filter_count(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``_skip_planner_filter_count`` (leaf mode) never runs the per-fragment
    ``count_rows(filter=where)`` on the driver and emits a read task for every
    fragment, leaving the filter to be applied at read time on the workers —
    even for fragments that match zero rows.
    """
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3, 4], "a2": [2, 4, 6, 8]}))
    tbl.add(pa.table({"a": [5, 6, 7, 8], "a2": [10, 12, 14, 16]}))
    tbl.add(pa.table({"a": [9, 10, 11, 12], "a2": [18, 20, 22, 24]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    dataset = tbl.to_lance()
    fragments = dataset.get_fragments()
    assert len(fragments) == 3

    # Any filtered count_rows on the driver is a leaf-mode violation.
    frag_type = type(fragments[0])
    original_count_rows = frag_type.count_rows

    def _count_rows(self, *args: object, **kwargs: object) -> int:
        filter_expr = kwargs.get("filter", args[0] if args else None)
        if filter_expr is not None:
            raise AssertionError(
                "leaf mode must not run count_rows(filter=...) on the driver"
            )
        return original_count_rows(self, *args, **kwargs)

    monkeypatch.setattr(frag_type, "count_rows", _count_rows)

    plans, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        # ``a2`` is fully populated, so this filter matches zero rows — yet
        # leaf mode still emits tasks because it never checks.
        where="a2 IS NULL",
        batch_size=16,
        map_task=BackfillUDFTask(
            udfs={"a2": double_a},
            where="a2 IS NULL",
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=InMemoryCheckpointStore(),
        default_where_generated=True,
        _skip_planner_filter_count=True,
    )

    task_list = list(plans)
    # One task per fragment, each carrying the filter for the worker to apply.
    assert {t.frag_id for t in task_list} == {f.fragment_id for f in fragments}
    assert all(t.where == "a2 IS NULL" for t in task_list)


def test_plan_read_parallel_filter_count_skips_checkpointed_fragments(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    """On a resumed backfill, fragments with valid checkpoints are
    skipped in the main loop via the `checkpoint_exists` branch before
    `count_rows` is reached. The parallel prefetch must mirror that
    short-circuit; otherwise it wastes Lance scans on fragments whose
    counts are never read.
    """
    import threading

    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "a2": [2, 4, 6]}))
    tbl.add(pa.table({"a": [4, 5, 6], "a2": [8, 10, 12]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    map_task = BackfillUDFTask(
        udfs={"a2": double_a},
        where="a2 IS NULL",
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    # Plant a legacy fragment-level checkpoint for fragment 0 so the
    # main loop will short-circuit it. The on-disk staging file is what
    # `_check_fragment_data_file_exists` validates.
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    legacy_key_frag0 = _legacy_fragment_dedupe_key(tbl.uri, 0, map_task)
    store[legacy_key_frag0] = pa.RecordBatch.from_pydict({"file": ["fragment0.lance"]})
    staging_dir = tmp_path / "data"
    staging_dir.mkdir(exist_ok=True)
    (staging_dir / "fragment0.lance").touch()

    dataset = tbl.to_lance()
    frag_type = type(dataset.get_fragment(0))
    original_count_rows = frag_type.count_rows
    filter_calls: list[tuple[int, int]] = []
    main_thread_id = threading.get_ident()

    def _count_rows(self, *args: object, **kwargs: object) -> int:
        filter_expr = kwargs.get("filter")
        if args:
            filter_expr = args[0]
        if filter_expr is not None:
            filter_calls.append((self.fragment_id, threading.get_ident()))
        return original_count_rows(self, *args, **kwargs)

    monkeypatch.setattr(frag_type, "count_rows", _count_rows)

    plans, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=16,
        map_task=map_task,
        checkpoint_store=store,
        default_where_generated=True,
        _plan_filter_count_concurrency=4,
    )

    list(plans)

    # Fragment 0: its legacy dedupe key is in `checkpoint_keys`, so the
    # prefetch must skip it. If its checkpoint payload later turns out
    # to be stale, the main loop falls back to a synchronous count_rows
    # on the driver thread — but the prefetch must NOT scan it on a
    # worker thread.
    # Fragment 1: no checkpoint → prefetched on a worker thread.
    frag0_threads = [tid for fid, tid in filter_calls if fid == 0]
    frag1_threads = [tid for fid, tid in filter_calls if fid == 1]
    assert all(tid == main_thread_id for tid in frag0_threads), (
        "fragment 0 was prefetched despite being in checkpoint_keys"
    )
    assert frag1_threads, "fragment 1 should have been prefetched"
    assert all(tid != main_thread_id for tid in frag1_threads)
    assert len(frag1_threads) == 1, "fragment 1 should be counted exactly once"


def test_plan_read_generated_default_where_keeps_output_file_safety(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "a2": [2, 4, 6]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    dataset = tbl.to_lance()
    frag_type = type(dataset.get_fragment(0))
    original_count_rows = frag_type.count_rows
    filter_calls: list[str] = []

    def _count_rows(self, *args: object, **kwargs: object) -> int:
        filter_expr = kwargs.get("filter")
        if args:
            filter_expr = args[0]
        if filter_expr is not None:
            filter_calls.append(str(filter_expr))
        return original_count_rows(self, *args, **kwargs)

    monkeypatch.setattr(frag_type, "count_rows", _count_rows)

    plans, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=16,
        map_task=BackfillUDFTask(
            udfs={"a2": double_a},
            where="a2 IS NULL",
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=InMemoryCheckpointStore(),
        default_where_generated=True,
    )

    assert list(plans) == []
    assert filter_calls == ["a2 IS NULL"]


def test_plan_read_skips_hash_and_dedupe_for_empty_checkpoint_index(
    tmp_path: Path, tbl_ref: TableReference, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    tbl.add_columns({"a2": double_a})

    def _unexpected_hash(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("empty checkpoint path should not hash source files")

    def _unexpected_dedupe(*args: object, **kwargs: object) -> NoReturn:
        raise AssertionError("empty checkpoint path should not build dedupe keys")

    monkeypatch.setattr(apply_module, "hash_source_files", _unexpected_hash)
    monkeypatch.setattr(pipeline_module, "_get_fragment_dedupe_key", _unexpected_dedupe)

    plans, _ = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=16,
        map_task=BackfillUDFTask(
            udfs={"a2": double_a},
            where="a2 IS NULL",
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_store=InMemoryCheckpointStore(),
        default_where_generated=True,
    )

    assert len(list(plans)) == 1


def test_plan_read_generated_default_where_preserves_partial_checkpoint_gaps(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3, 4, 5, 6]}))

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    tbl.add_columns({"a2": double_a})
    dataset = tbl.to_lance()
    map_task = BackfillUDFTask(
        udfs={"a2": double_a},
        where="a2 IS NULL",
        override_batch_size=2,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    store = InMemoryCheckpointStore()
    src_files_hash = _src_files_hash_for_cols(tbl, ["a"])
    for start, end in [(0, 2), (2, 4)]:
        key = map_task.checkpoint_key(
            dataset_uri=tbl.uri,
            dataset_version=dataset.version,
            frag_id=0,
            start=start,
            end=end,
            where="a2 IS NULL",
            src_files_hash=src_files_hash,
        )
        store[key] = pa.record_batch([], names=[])

    tasks, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        where="a2 IS NULL",
        batch_size=2,
        map_task=map_task,
        checkpoint_store=store,
        default_where_generated=True,
    )

    task_list = list(tasks)
    # Covered runs [0,2) and [2,4) are planned too (merged and tiled at
    # task_size, reused from checkpoints); only [4,6) is recomputed.
    assert [(task.offset, task.limit) for task in task_list] == [
        (0, 2),
        (2, 2),
        (4, 2),
    ]
    assert pipeline_args["skipped_stats"]["rows"] == 0


def test_plan_read_hierarchical_does_not_reuse_stale_srcfiles_fragment_checkpoint(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))
    dataset = tbl.to_lance()

    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    store = HierarchicalLanceCheckpointStore(str(tmp_path / "ckp"))
    stale_src_hash = hash_source_files(frozenset({"old-source-file.lance"}))
    current_src_hash = _src_files_hash_for_cols(tbl, ["a"])
    assert stale_src_hash != current_src_hash

    stale_key = _get_fragment_dedupe_key(
        tbl.uri,
        0,
        map_task,
        dataset_version=dataset.version,
        src_files_hash=stale_src_hash,
    )
    current_key = _get_fragment_dedupe_key(
        tbl.uri,
        0,
        map_task,
        dataset_version=dataset.version,
        src_files_hash=current_src_hash,
    )
    store[stale_key] = pa.RecordBatch.from_pydict({"file": ["stale.lance"]})
    scoped_prefix = map_task.checkpoint_prefix(
        dataset_uri=tbl.uri,
        where=None,
        column=None,
        src_files_hash=None,
    )
    assert set(store.list_keys(prefix=scoped_prefix)) == {stale_key}
    assert current_key not in store

    tasks, pipeline_args = plan_read(
        tbl.uri,
        tbl_ref,
        ["a"],
        batch_size=16,
        map_task=map_task,
        checkpoint_store=store,
    )

    task_list = list(tasks)
    assert len(task_list) == 1
    assert pipeline_args["skipped_fragments"] == {}


def test_validate_checkpoint_data_files_uses_key_srcfiles_without_payload(
    tmp_path: Path,
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))
    store = InMemoryCheckpointStore()
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    current_files = frozenset({"current-source.lance"})
    current_hash = hash_source_files(current_files)
    stale_hash = hash_source_files(frozenset({"old-source.lance"}))
    current_key = _get_fragment_dedupe_key(
        tbl.uri, 0, map_task, src_files_hash=current_hash
    )
    stale_key = _get_fragment_dedupe_key(
        tbl.uri, 0, map_task, src_files_hash=stale_hash
    )
    store[current_key] = pa.RecordBatch.from_pydict({"file": ["fragment_0.lance"]})
    store[stale_key] = pa.RecordBatch.from_pydict({"file": ["fragment_0.lance"]})

    assert pipeline_module._validate_checkpoint_data_files(
        store, current_key, current_files
    )
    assert not pipeline_module._validate_checkpoint_data_files(
        store, stale_key, current_files
    )


@pytest.mark.ray
def test_fragment_writer_manager_with_skipped_fragments(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Test that FragmentWriterManager correctly handles skipped fragments."""
    import lance.fragment
    import ray

    # Start Ray if not already started
    if not ray.is_initialized():
        ray.init(local_mode=True, ignore_reinit_error=True)

    try:
        db = connect(tmp_path)
        tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

        store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
        map_task = BackfillUDFTask(
            udfs={"one": one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        )

        # Create a mock skipped fragment data file
        skipped_data_file = lance.fragment.DataFile(
            "skipped_fragment.lance",
            [],  # field_ids
            [],  # field_id_to_column_indices
            2,  # major_version
            0,  # minor_version
        )

        skipped_fragments = {0: (skipped_data_file, 3)}

        # Create FragmentWriterManager with skipped fragments
        fwm = FragmentWriterManager(
            dst_read_version=tbl.version,
            ds_uri=tbl.uri,
            job_tracker=None,
            map_task=map_task,
            checkpoint_store=store,
            where=None,
            commit_granularity=1,
            expected_tasks={1: 1},  # Only fragment 1 has expected tasks
            skipped_fragments=skipped_fragments,
        )

        # Check that skipped fragment is immediately in to_commit
        assert len(fwm.to_commit) == 1
        frag_id, data_file, row_count = fwm.to_commit[0]
        assert frag_id == 0
        assert data_file == skipped_data_file
        assert row_count >= 0  # Row count should be determined

    finally:
        if ray.is_initialized():
            ray.shutdown()


@pytest.mark.ray
def test_fragment_writer_manager_no_skipped_fragments(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Test that FragmentWriterManager works normally with no skipped fragments."""
    import ray

    # Start Ray if not already started
    if not ray.is_initialized():
        ray.init(local_mode=True, ignore_reinit_error=True)

    try:
        db = connect(tmp_path)
        tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

        store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
        map_task = BackfillUDFTask(
            udfs={"one": one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        )

        # Create FragmentWriterManager with no skipped fragments
        fwm = FragmentWriterManager(
            dst_read_version=tbl.version,
            ds_uri=tbl.uri,
            map_task=map_task,
            checkpoint_store=store,
            where=None,
            job_tracker=None,
            commit_granularity=1,
            expected_tasks={0: 1},  # Fragment 0 has expected tasks
            skipped_fragments={},  # No skipped fragments
        )

        # Should have no items in to_commit initially
        assert len(fwm.to_commit) == 0

    finally:
        if ray.is_initialized():
            ray.shutdown()


@pytest.mark.ray
def test_fragment_writer_manager_mixed_fragments(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Test FragmentWriterManager with both skipped and normal fragments."""
    import lance.fragment
    import ray

    # Start Ray if not already started
    if not ray.is_initialized():
        ray.init(local_mode=True, ignore_reinit_error=True)

    try:
        db = connect(tmp_path)
        tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))
        tbl.add(pa.table({"a": [4, 5, 6]}))  # Add second fragment

        store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
        map_task = BackfillUDFTask(
            udfs={"one": one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        )

        # Create a mock skipped fragment data file for fragment 0
        skipped_data_file = lance.fragment.DataFile(
            "skipped_fragment_0.lance",
            [],  # field_ids
            [],  # field_id_to_column_indices
            2,  # major_version
            0,  # minor_version
        )

        skipped_fragments = {0: (skipped_data_file, 3)}

        # Create FragmentWriterManager with mixed fragments
        fwm = FragmentWriterManager(
            dst_read_version=tbl.version,
            ds_uri=tbl.uri,
            map_task=map_task,
            checkpoint_store=store,
            where=None,
            job_tracker=None,
            commit_granularity=1,
            expected_tasks={1: 1},  # Only fragment 1 has expected tasks to process
            skipped_fragments=skipped_fragments,
        )

        # Should have 1 item in to_commit (the skipped fragment)
        assert len(fwm.to_commit) == 1
        frag_id, data_file, row_count = fwm.to_commit[0]
        assert frag_id == 0
        assert data_file == skipped_data_file

        # Fragment 1 should still be tracked in remaining_tasks
        assert 1 in fwm.remaining_tasks
        assert fwm.remaining_tasks[1] == 1

    finally:
        if ray.is_initialized():
            ray.shutdown()


def test_fragment_writer_manager_dedupes_fragment_records(tmp_path: Path) -> None:
    """Ensure duplicate fragment records don't double count or re-enqueue."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    fwm = FragmentWriterManager(
        dst_read_version=tbl.version,
        ds_uri=tbl.uri,
        job_tracker=None,
        map_task=map_task,
        checkpoint_store=store,
        where=None,
        commit_granularity=999,
        expected_tasks={0: 1},
        skipped_fragments={},
    )

    data_file = lance.fragment.DataFile(
        "fragment_0.lance",
        [],
        [],
        2,
        0,
    )
    fwm.rows_input_by_frag[0] = 3

    fwm._record_fragment(0, data_file, commit_granularity=999, rows_written=3)
    fwm._record_fragment(0, data_file, commit_granularity=999, rows_written=3)
    fwm._drain_pending_fragment_records()

    assert len(fwm.to_commit) == 1
    assert fwm._reconciled_rows_ready_total == 3


def test_fragment_writer_manager_hierarchical_srcfiles_share_backfill_dir(
    tmp_path: Path,
) -> None:
    db = connect(tmp_path / "db")
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))
    root = tmp_path / "ckp"
    store = HierarchicalLanceCheckpointStore(str(root))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    src_files_0 = frozenset({"src-frag-0-a.lance"})
    src_files_1 = frozenset({"src-frag-1-a.lance"})
    src_hash_0 = hash_source_files(src_files_0)
    src_hash_1 = hash_source_files(src_files_1)
    assert src_hash_0 != src_hash_1

    fwm = FragmentWriterManager(
        dst_read_version=tbl.version,
        ds_uri=tbl.uri,
        job_tracker=None,
        map_task=map_task,
        checkpoint_store=store,
        where=None,
        commit_granularity=999,
        expected_tasks={0: 1, 1: 1},
        skipped_fragments={},
        src_data_files_by_dst={0: src_files_0, 1: src_files_1},
    )
    fwm.rows_input_by_frag[0] = 3
    fwm.rows_input_by_frag[1] = 3

    fwm._record_fragment(
        0,
        lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0),
        commit_granularity=999,
        rows_written=3,
    )
    fwm._record_fragment(
        1,
        lance.fragment.DataFile("fragment_1.lance", [], [], 2, 0),
        commit_granularity=999,
        rows_written=3,
    )
    fwm._drain_pending_fragment_records()

    bf_identity = map_task.checkpoint_prefix(
        dataset_uri=tbl.uri,
        where=None,
        column=None,
        src_files_hash=None,
    ).split("_uri-", 1)[0]
    bf = hash_string(bf_identity)
    assert sorted(p.name for p in root.iterdir() if p.name.startswith("bf=")) == [
        f"bf={bf}"
    ]
    assert len(list(root.rglob("_identity.json"))) == 1
    assert (
        root
        / f"bf={bf}"
        / "fragments"
        / f"fs={hash_string('0')[:2]}"
        / f"0_src-{src_hash_0}.lance"
    ).exists()
    assert (
        root
        / f"bf={bf}"
        / "fragments"
        / f"fs={hash_string('1')[:2]}"
        / f"1_src-{src_hash_1}.lance"
    ).exists()

    key_0 = _get_fragment_dedupe_key(
        tbl.uri,
        0,
        map_task,
        dataset_version=tbl.version,
        src_files_hash=src_hash_0,
    )
    key_1 = _get_fragment_dedupe_key(
        tbl.uri,
        1,
        map_task,
        dataset_version=tbl.version,
        src_files_hash=src_hash_1,
    )
    assert set(store.list_keys()) == {key_0, key_1}
    assert "src_data_files" not in store[key_0].schema.names
    assert "src_data_files" not in store[key_1].schema.names


def test_fragment_writer_manager_record_force_releases_idle_session() -> None:
    fwm = _make_fragment_writer_manager()
    sess = _DummyWriterSession(sealed=True)
    fwm.sessions[0] = sess  # type: ignore[assignment]

    fwm.rows_input_by_frag[0] = 3

    fwm._record_fragment(
        0,
        lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0),
        commit_granularity=999,
        rows_written=3,
        checkpoint_already_written=True,
    )

    assert sess.shutdown_force_values == [True]
    assert 0 not in fwm.sessions
    assert len(fwm.to_commit) == 1


@pytest.mark.parametrize(
    "store_cls",
    [FlatLanceCheckpointStore, HierarchicalLanceCheckpointStore],
)
def test_fragment_writer_manager_purges_batch_checkpoints_after_fragment_record(
    tmp_path: Path,
    store_cls: type[FlatLanceCheckpointStore | HierarchicalLanceCheckpointStore],
) -> None:
    """Recording a fragment hard-deletes its now-redundant batch checkpoints."""
    db = connect(tmp_path / "db")
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))
    root = tmp_path / "ckp"
    store = store_cls(str(root))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    batch_keys = [
        map_task.checkpoint_key(
            dataset_uri=tbl.uri,
            frag_id=0,
            start=0,
            end=2,
            dataset_version=tbl.version,
        ),
        map_task.checkpoint_key(
            dataset_uri=tbl.uri,
            frag_id=0,
            start=2,
            end=3,
            dataset_version=tbl.version,
        ),
    ]
    batch = pa.RecordBatch.from_pydict({"one": [1]})
    for key in batch_keys:
        store[key] = batch

    def _range_lance_paths() -> list[Path]:
        return [
            path
            for path in root.rglob("*.lance")
            if "_range-" in path.as_posix() or "/ranges/" in path.as_posix()
        ]

    assert _range_lance_paths()

    class _CachedSession:
        def __init__(self) -> None:
            self.cached_tasks = [(idx, key, 0) for idx, key in enumerate(batch_keys)]
            self.sealed = False
            self.inflight: dict[object, int] = {}

        def shutdown(self, *, force_queue: bool = False) -> None:
            pass

    fwm = FragmentWriterManager(
        dst_read_version=tbl.version,
        ds_uri=tbl.uri,
        job_tracker=None,
        map_task=map_task,
        checkpoint_store=store,
        where=None,
        commit_granularity=999,
        expected_tasks={0: 1},
        skipped_fragments={},
    )
    fwm.sessions[0] = _CachedSession()  # type: ignore[assignment]
    fwm.rows_input_by_frag[0] = 3

    dedupe_key = _get_fragment_dedupe_key(
        tbl.uri,
        0,
        map_task,
        dataset_version=tbl.version,
    )

    fwm._record_fragment(
        0,
        lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0),
        commit_granularity=999,
        rows_written=3,
    )
    fwm._drain_pending_fragment_records()

    assert dedupe_key in store
    for key in batch_keys:
        assert key not in store
    assert not _range_lance_paths()


class _RecordingCheckpointStore:
    def __init__(self, *, fail_writes: bool = False) -> None:
        self.fail_writes = fail_writes
        self.writes: list[tuple[str, pa.RecordBatch]] = []
        self.purges: list[list[str]] = []

    def uri(self) -> str:
        return "memory://checkpoint"

    def __setitem__(self, key: str, value: pa.RecordBatch) -> None:
        if self.fail_writes:
            raise RuntimeError("checkpoint boom")
        self.writes.append((key, value))

    def purge_many(self, keys: list[str]) -> None:
        self.purges.append(list(keys))


class _ManualFragmentRecordExecutor:
    def __init__(self) -> None:
        self.submissions: list[
            tuple[object, tuple[object, ...], dict[str, object], Future]
        ] = []
        self.shutdown_calls: list[bool] = []

    def submit(self, fn, *args, **kwargs) -> Future:
        future: Future = Future()
        self.submissions.append((fn, args, kwargs, future))
        return future

    def shutdown(self, *, wait: bool = True) -> None:
        self.shutdown_calls.append(wait)


def _make_recording_fragment_writer_manager(
    store: _RecordingCheckpointStore,
) -> FragmentWriterManager:
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    return FragmentWriterManager(
        dst_read_version=7,
        ds_uri="memory:///dst.lance",
        job_tracker=None,
        map_task=map_task,
        checkpoint_store=store,  # type: ignore[arg-type]
        where=None,
        commit_granularity=999,
        expected_tasks={},
        skipped_fragments={},
    )


def _complete_fragment_record_submission(
    executor: _ManualFragmentRecordExecutor,
    index: int,
) -> None:
    fn, args, kwargs, future = executor.submissions[index]
    try:
        future.set_result(fn(*args, **kwargs))
    except BaseException as exc:
        future.set_exception(exc)


def test_fragment_writer_manager_async_record_gates_to_commit() -> None:
    store = _RecordingCheckpointStore()
    executor = _ManualFragmentRecordExecutor()
    fwm = _make_recording_fragment_writer_manager(store)
    fwm._fragment_record_executor = executor  # type: ignore[assignment]
    fwm.rows_input_by_frag[0] = 3
    data_file = lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0)

    fwm._record_fragment(0, data_file, commit_granularity=999, rows_written=3)

    assert fwm.to_commit == []
    assert store.writes == []
    assert len(executor.submissions) == 1

    _complete_fragment_record_submission(executor, 0)
    assert fwm.to_commit == []

    fwm._drain_pending_fragment_records()

    assert len(store.writes) == 1
    assert fwm.to_commit == [(0, data_file, 3)]


def test_fragment_writer_manager_async_record_copies_purge_keys_before_work() -> None:
    store = _RecordingCheckpointStore()
    executor = _ManualFragmentRecordExecutor()
    fwm = _make_recording_fragment_writer_manager(store)
    fwm._fragment_record_executor = executor  # type: ignore[assignment]
    fwm.rows_input_by_frag[0] = 3

    sess = _DummyWriterSession(sealed=False)
    sess.cached_tasks = [(0, "batch-key-a", 3)]
    fwm.sessions[0] = sess  # type: ignore[assignment]

    data_file = lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0)
    fwm._record_fragment(0, data_file, commit_granularity=999, rows_written=3)

    sess.cached_tasks = [(0, "batch-key-b", 3)]
    _complete_fragment_record_submission(executor, 0)
    fwm._drain_pending_fragment_records()

    assert store.purges == [["batch-key-a"]]
    assert store.writes
    assert fwm.to_commit == [(0, data_file, 3)]


def test_fragment_writer_manager_poll_all_commits_record_without_writer_futures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = _RecordingCheckpointStore()
    executor = _ManualFragmentRecordExecutor()
    fwm = _make_recording_fragment_writer_manager(store)
    fwm._fragment_record_executor = executor  # type: ignore[assignment]
    fwm.rows_input_by_frag[0] = 3
    data_file = lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0)

    fwm._record_fragment(0, data_file, commit_granularity=999, rows_written=3)
    _complete_fragment_record_submission(executor, 0)

    commit_calls: list[tuple[int, bool]] = []

    def fake_commit(
        self: FragmentWriterManager,
        commit_granularity: int,
        robust: bool = False,
    ) -> None:
        commit_calls.append((commit_granularity, robust))

    monkeypatch.setattr(
        pipeline_module.FragmentWriterManager,
        "_commit_if_n_fragments",
        fake_commit,
    )

    fwm.poll_all()

    assert fwm.to_commit == [(0, data_file, 3)]
    assert commit_calls == [(999, False)]


def test_fragment_writer_manager_async_record_cap_drains_pending() -> None:
    store = _RecordingCheckpointStore()
    executor = _ManualFragmentRecordExecutor()
    fwm = _make_recording_fragment_writer_manager(store)
    fwm._fragment_record_executor = executor  # type: ignore[assignment]
    fwm._fragment_record_max_pending = 1
    fwm.rows_input_by_frag[0] = 3
    fwm.rows_input_by_frag[1] = 4

    file0 = lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0)
    file1 = lance.fragment.DataFile("fragment_1.lance", [], [], 2, 0)
    fwm._record_fragment(0, file0, commit_granularity=999, rows_written=3)

    errors: list[BaseException] = []

    def record_second() -> None:
        try:
            fwm._record_fragment(1, file1, commit_granularity=999, rows_written=4)
        except BaseException as exc:
            errors.append(exc)

    worker = threading.Thread(target=record_second)
    worker.start()
    time.sleep(0.1)

    assert worker.is_alive()
    assert len(executor.submissions) == 1

    _complete_fragment_record_submission(executor, 0)
    worker.join(timeout=2)

    assert not worker.is_alive()
    assert errors == []
    assert len(executor.submissions) == 2
    assert fwm.to_commit == [(0, file0, 3)]


def test_fragment_writer_manager_async_record_failure_blocks_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = _RecordingCheckpointStore(fail_writes=True)
    executor = _ManualFragmentRecordExecutor()
    fwm = _make_recording_fragment_writer_manager(store)
    fwm._fragment_record_executor = executor  # type: ignore[assignment]
    fwm.rows_input_by_frag[0] = 3

    fwm._record_fragment(
        0,
        lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0),
        commit_granularity=1,
        rows_written=3,
    )
    _complete_fragment_record_submission(executor, 0)

    commit_calls: list[tuple[tuple[object, ...], dict[str, object]]] = []

    def fake_commit(*args, **kwargs) -> None:
        commit_calls.append((args, kwargs))

    monkeypatch.setattr(pipeline_module.lance.LanceDataset, "commit", fake_commit)

    with pytest.raises(RuntimeError, match="checkpoint boom"):
        fwm._commit_if_n_fragments(1)

    assert fwm.to_commit == []
    assert 0 not in fwm._recording_fragment_ids
    assert commit_calls == []


def test_fragment_writer_manager_cleanup_shuts_executor_on_record_failure() -> None:
    store = _RecordingCheckpointStore(fail_writes=True)
    executor = _ManualFragmentRecordExecutor()
    fwm = _make_recording_fragment_writer_manager(store)
    fwm._fragment_record_executor = executor  # type: ignore[assignment]
    fwm.rows_input_by_frag[0] = 3

    fwm._record_fragment(
        0,
        lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0),
        commit_granularity=999,
        rows_written=3,
    )
    _complete_fragment_record_submission(executor, 0)

    with pytest.raises(RuntimeError, match="checkpoint boom"):
        fwm.cleanup()

    assert executor.shutdown_calls == [True]
    assert 0 not in fwm._recording_fragment_ids


def test_fragment_writer_manager_cleanup_force_releases_sealed_idle_session() -> None:
    fwm = _make_fragment_writer_manager()
    sess = _DummyWriterSession(sealed=True)
    fwm.sessions[0] = sess  # type: ignore[assignment]

    fwm.cleanup()

    assert sess.drain_calls == 0
    assert sess.shutdown_force_values == [True]
    assert 0 not in fwm.sessions


def test_fragment_writer_manager_cleanup_preserves_failed_session_path() -> None:
    fwm = _make_fragment_writer_manager()
    sess = _DummyWriterSession(
        sealed=True,
        failed=True,
        failure_reason="write failed",
    )
    fwm.sessions[0] = sess  # type: ignore[assignment]

    with pytest.raises(FragmentWriteFailedError, match="write failed"):
        fwm.cleanup()

    assert sess.drain_calls == 0
    assert sess.shutdown_force_values == [False]
    assert fwm.failed_fragments == {0: "write failed"}


def test_fragment_writer_manager_cleanup_drains_sealed_inflight_session() -> None:
    fwm = _make_fragment_writer_manager()
    sess = _DummyWriterSession(sealed=True, inflight={object(): 0})
    fwm.sessions[0] = sess  # type: ignore[assignment]

    fwm.cleanup()

    assert sess.seal_calls == 0
    assert sess.drain_calls == 1
    assert sess.shutdown_force_values == [False]
    assert 0 not in fwm.sessions


def test_fragment_writer_manager_cleanup_seals_and_drains_unsealed_session() -> None:
    fwm = _make_fragment_writer_manager()
    sess = _DummyWriterSession(sealed=False)
    fwm.sessions[0] = sess  # type: ignore[assignment]

    fwm.cleanup()

    assert sess.seal_calls == 1
    assert sess.drain_calls == 1
    assert sess.shutdown_force_values == [False]
    assert 0 not in fwm.sessions


def test_fragment_writer_manager_dedupes_duplicate_task_ingest(tmp_path: Path) -> None:
    """Ensure replayed read-task results are not ingested twice."""
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    fwm = FragmentWriterManager(
        dst_read_version=tbl.version,
        ds_uri=tbl.uri,
        job_tracker=None,
        map_task=map_task,
        checkpoint_store=store,
        where=None,
        commit_granularity=999,
        expected_tasks={0: 1},
        skipped_fragments={},
    )

    class _DummySession:
        failed = False
        failure_reason = None

        def __init__(self) -> None:
            self.sealed = False
            self.ingested: list[tuple[int, str, int]] = []

        def ingest_task(self, offset: int, checkpoint_key: str, num_rows: int) -> None:
            self.ingested.append((offset, checkpoint_key, num_rows))

        def seal(self) -> None:
            self.sealed = True

    sess = _DummySession()
    fwm.sessions[0] = sess

    task = ScanTask(
        uri=tbl.uri,
        table_ref=tbl.get_reference(),
        columns=["a"],
        frag_id=0,
        offset=0,
        limit=3,
        version=tbl.version,
        with_row_address=True,
    )
    checkpoints = [
        MapBatchCheckpoint(
            checkpoint_key="frag-0_range-0-3",
            offset=0,
            num_rows=3,
            span=3,
            udf_rows=3,
        )
    ]

    fwm.ingest_task(task, checkpoints)
    fwm.ingest_task(task, checkpoints)

    assert sess.ingested == [(0, "frag-0_range-0-3", 3)]
    assert fwm._reconciled_rows_checkpointed_total == 3
    assert fwm.rows_input_by_frag[0] == 3
    assert fwm.remaining_tasks[0] == 0
    assert sess.sealed is True


def test_fragment_writer_manager_ingests_direct_fragment_result(
    tmp_path: Path,
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "one": [None, None, None]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    fwm = FragmentWriterManager(
        dst_read_version=tbl.version,
        ds_uri=tbl.uri,
        job_tracker=None,
        map_task=map_task,
        checkpoint_store=store,
        where=None,
        commit_granularity=999,
        expected_tasks={0: 1},
        skipped_fragments={},
    )

    task = _DummyReadTask(frag_id=0, rows=3)
    result = DirectFragmentWriteResult(
        frag_id=0,
        new_file=lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0),
        rows_written=3,
        checkpoint_written=True,
        fragment_checkpointing_ms=11,
        write_ms=7,
        avg_batch_num_rows=3,
        avg_batch_size=24,
    )

    fwm.ingest_direct_fragment_result(task, result)

    assert 0 not in fwm.sessions
    assert len(fwm.to_commit) == 1
    assert fwm._reconciled_rows_checkpointed_total == 3
    assert fwm._reconciled_rows_ready_total == 3
    assert fwm.remaining_tasks[0] == 0


def test_fragment_writer_manager_tracks_direct_vs_checkpoint_fragments(
    tmp_path: Path,
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "one": [None, None, None]}))

    tracker = _RecordingJobTracker()
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    fwm = pipeline_module.FragmentWriterManager(
        dst_read_version=tbl.version,
        ds_uri=tbl.uri,
        job_tracker=tracker,
        map_task=map_task,
        checkpoint_store=store,
        where=None,
        commit_granularity=999,
        expected_tasks={0: 1, 1: 1},
        skipped_fragments={},
    )

    direct_task = _DummyReadTask(frag_id=0, rows=3)
    direct_result = DirectFragmentWriteResult(
        frag_id=0,
        new_file=lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0),
        rows_written=3,
        checkpoint_written=True,
    )
    fwm.ingest_direct_fragment_result(direct_task, direct_result)

    fwm._record_fragment(
        1,
        lance.fragment.DataFile("fragment_1.lance", [], [], 2, 0),
        999,
        3,
    )
    fwm._drain_pending_fragment_records()

    metric_calls = [
        call[0]
        for call in tracker.batch_increment.calls
        if call and isinstance(call[0], dict)
    ]
    assert any(
        metric.get(METRIC_DIRECT_FRAGMENT_WRITES) == 1
        and metric.get(METRIC_CHECKPOINT_FRAGMENT_WRITES) == 0
        for metric in metric_calls
    )
    assert any(
        metric.get(METRIC_DIRECT_FRAGMENT_WRITES) == 0
        and metric.get(METRIC_CHECKPOINT_FRAGMENT_WRITES) == 1
        for metric in metric_calls
    )


def test_fragment_writer_manager_dedupes_direct_fragment_result(
    tmp_path: Path,
) -> None:
    db = connect(tmp_path)
    tbl = db.create_table("tbl", pa.table({"a": [1, 2, 3], "one": [None, None, None]}))

    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    fwm = FragmentWriterManager(
        dst_read_version=tbl.version,
        ds_uri=tbl.uri,
        job_tracker=None,
        map_task=map_task,
        checkpoint_store=store,
        where=None,
        commit_granularity=999,
        expected_tasks={0: 1},
        skipped_fragments={},
    )

    task = _DummyReadTask(frag_id=0, rows=3)
    result = DirectFragmentWriteResult(
        frag_id=0,
        new_file=lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0),
        rows_written=3,
        checkpoint_written=True,
        fragment_checkpointing_ms=11,
        write_ms=7,
        avg_batch_num_rows=3,
        avg_batch_size=24,
    )

    fwm.ingest_direct_fragment_result(task, result)
    fwm.ingest_direct_fragment_result(task, result)

    assert len(fwm.to_commit) == 1
    assert fwm._reconciled_rows_checkpointed_total == 3
    assert fwm._reconciled_rows_ready_total == 3
    assert fwm.rows_input_by_frag[0] == 3
    assert fwm.remaining_tasks[0] == 0


def test_direct_fragment_write_passes_storage_options(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    task = _DummyReadTask(frag_id=0, rows=3)
    storage_options = {"account_name": "acct", "account_key": "secret"}
    batch = pa.RecordBatch.from_pydict(
        {
            "one": [1, 2, 3],
            "_rowaddr": [0, 1, 2],
        }
    )

    seen: dict[str, object] = {}

    def _fake_write_fragment_file(
        *args: object, **kwargs: object
    ) -> tuple[object, int, int]:
        seen["storage_options"] = kwargs.get("storage_options")
        return lance.fragment.DataFile("fragment_0.lance", [], [], 2, 0), 3, 7

    monkeypatch.setattr(
        "geneva.runners.ray.writer.write_fragment_file",
        _fake_write_fragment_file,
    )

    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={"one": one},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri="memory",
        direct_fragment_write=DirectFragmentWriteConfig(
            ds_uri="s3://bucket/table",
            column_names=["one"],
            field_ids=[1],
            column_indices=[0],
            data_storage_version="2.1",
            storage_options=storage_options,
        ),
    )

    result = applier._write_direct_fragment_result(task, batch, udf_rows=3)

    assert seen["storage_options"] == storage_options
    assert result.rows_written == 3


def test_plan_copy_skips_zero_row_fragments_for_whole_fragment_tasks() -> None:
    class _FakeFragment:
        fragment_id = 7
        physical_rows = 5

        def count_rows(self) -> int:
            return 0

    class _FakeDataset:
        def get_fragments(self) -> list[object]:
            return [_FakeFragment()]

    class _FakeTableRef:
        table_id = ["tbl"]

        def open(self) -> "_FakeTableRef":
            return self

        def to_lance(self) -> _FakeDataset:
            return _FakeDataset()

    tasks, num_tasks = apply_module._plan_copy(
        _FakeTableRef(),
        _FakeTableRef(),
        ["a"],
        task_size=0,
    )

    assert num_tasks == 0
    assert list(tasks) == []


def test_plan_copy_keeps_large_fragment_tasks_lazy() -> None:
    total_rows = 1_000_000_000

    class _FakeFragment:
        fragment_id = 7
        physical_rows = total_rows

        def count_rows(self) -> int:
            return total_rows

    class _FakeDataset:
        def get_fragments(self) -> list[object]:
            return [_FakeFragment()]

    class _FakeTableRef:
        table_id = ["tbl"]
        table_uri = "memory://table"

        def open(self) -> "_FakeTableRef":
            return self

        def to_lance(self) -> _FakeDataset:
            return _FakeDataset()

    tasks, num_tasks = apply_module._plan_copy(
        _FakeTableRef(),  # type: ignore[arg-type]
        _FakeTableRef(),  # type: ignore[arg-type]
        ["a"],
        task_size=1,
    )

    assert num_tasks == total_rows
    assert tasks.total_rows == total_rows  # type: ignore[attr-defined]
    assert tasks.tasks_by_frag == {7: total_rows}  # type: ignore[attr-defined]
    first_tasks = list(islice(tasks, 3))
    assert [(task.offset, task.limit) for task in first_tasks] == [
        (0, 1),
        (1, 1),
        (2, 1),
    ]


def test_worker_rebuilt_checkpoint_stores_preserve_nested_session_root_subdir(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Actor-side store rebuilds must use the table-relative checkpoint subdir."""

    monkeypatch.delenv("GENEVA_CHECKPOINT_SUBDIR", raising=False)
    monkeypatch.setattr(
        CheckpointConfig,
        "get",
        classmethod(
            lambda cls: cls(
                store_layout="hierarchical",
                hierarchical_subdir="_ckp/custom",
            )
        ),
    )

    db = connect(tmp_path)
    db.create_table("t", pa.table({"id": [1]}))
    store = db.open_table("t").get_reference().open_checkpoint_store()
    assert isinstance(store, HierarchicalLanceCheckpointStore)
    assert store.session_root_subdir == "_ckp/custom"

    checkpoint_kwargs = {
        "checkpoint_namespace_client_impl": store.namespace_client_impl,
        "checkpoint_namespace_client_properties": store.namespace_client_properties,
        "checkpoint_table_id": store.table_id,
        "checkpoint_storage_options": store.storage_options,
        "checkpoint_session_root_subdir": store.session_root_subdir,
        "checkpoint_write_identity_sidecar": False,
    }
    prefix = "udf-foo_ver-1_col-c_where-aa_uri-bb_srcfiles-cc"
    store.ensure_identity_sidecar(prefix)

    applier = CheckpointingApplier(
        map_task=_DummyMapTask(),
        namespace_client_impl=store.namespace_client_impl,
        namespace_client_properties=store.namespace_client_properties,
        checkpoint_table_id=store.table_id,
        storage_options=store.storage_options,
        checkpoint_session_root_subdir=store.session_root_subdir,
        checkpoint_uri=store.uri(),
        checkpoint_write_identity_sidecar=False,
    )

    writer_cls = FragmentWriter.__ray_actor_class__
    writer = writer_cls(
        "memory:///dst.lance",
        ["one"],
        store.uri(),
        0,
        object(),
        **checkpoint_kwargs,
    )

    batch = pa.RecordBatch.from_pydict({"x": [1]})
    applier_key = f"{prefix}_frag-0_range-0-100"
    writer_key = f"{prefix}_frag-0_range-100-200"
    assert isinstance(applier.checkpoint_store, HierarchicalLanceCheckpointStore)
    assert applier.checkpoint_store.write_identity_sidecar is False
    assert isinstance(writer._store, HierarchicalLanceCheckpointStore)
    assert writer._store.write_identity_sidecar is False

    applier.checkpoint_store[applier_key] = batch
    writer._store[writer_key] = batch

    correct_root = tmp_path / "t.lance" / "_ckp" / "custom"
    wrong_root = tmp_path / "t.lance" / "custom"
    assert sorted(applier.checkpoint_store.list_keys(prefix)) == [
        applier_key,
        writer_key,
    ]
    bf = hash_string(prefix.split("_uri-", 1)[0])
    range_dir = (
        correct_root / f"bf={bf}" / "ranges" / f"fs={hash_string('0')[:2]}" / "0_src-cc"
    )
    assert list(range_dir.rglob("*.lance"))
    assert not list(wrong_root.rglob("*.lance"))


def test_driver_identity_sidecar_uses_planned_task_uri_for_copy_recovery(
    tmp_path: Path,
    tbl_ref: TableReference,
) -> None:
    """MV copy recovery lists range checkpoints by source task URI."""

    store = HierarchicalLanceCheckpointStore(str(tmp_path / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"one": one},
        override_batch_size=4,
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )
    source_uri = "memory:///source.lance"
    destination_uri = "memory:///destination.lance"
    task = _DummyReadTask(frag_id=0, rows=4, table_uri=source_uri)
    consumed = 0

    def task_gen() -> Iterator[ReadTask]:
        nonlocal consumed
        consumed += 1
        yield task

    plan = apply_module._LanceReadPlanIterator(
        task_gen(),
        total=1,
        total_rows=4,
        tasks_by_frag={0: 1},
        checkpoint_identity_contexts=((source_uri, None),),
    )
    job = ColumnAddPipelineJob(
        map_task=map_task,
        checkpoint_store=store,
        error_store=None,
        config=JobConfig(),
        dst=tbl_ref,
        input_plan=plan,
        job_id="job-copy-identity",
        job_tracker=_NoopJobTracker(),
    )

    job.setup_inputplans()
    job._ensure_driver_checkpoint_identity_sidecar(destination_uri)
    assert consumed == 0

    source_prefix = map_task.checkpoint_prefix(
        dataset_uri=source_uri,
        where=None,
        column=None,
        src_files_hash=None,
    )
    key = map_task.checkpoint_key(
        dataset_uri=source_uri,
        frag_id=0,
        start=0,
        end=4,
        where=None,
        src_files_hash=None,
    )
    worker_store = HierarchicalLanceCheckpointStore(
        store.uri(),
        write_identity_sidecar=False,
    )
    worker_store[key] = pa.RecordBatch.from_pydict({"x": [1, 2, 3, 4]})

    reader = HierarchicalLanceCheckpointStore(
        store.uri(),
        write_identity_sidecar=False,
    )
    assert list(reader.list_keys(prefix=source_prefix)) == [key]


def test_fragment_writer_uses_precomputed_metadata(tmp_path: Path, monkeypatch) -> None:
    """Ensure writer avoids opening dataset when metadata is provided."""
    from collections import deque

    tbl_path = tmp_path / "tbl.lance"
    ds = lance.write_dataset(pa.table({"a": [1, 2, 3]}), tbl_path)
    frag = ds.get_fragment(0)
    assert frag is not None

    num_physical_rows = frag.physical_rows
    num_logical_rows = frag.count_rows()

    store = CheckpointStore.from_uri(str(tmp_path / "ckp"))
    checkpoint_key = "fragment_0_batch_0"
    rowaddr = pa.array([0, 1, 2], type=pa.uint64())
    batch = pa.record_batch([pa.array([10, 11, 12]), rowaddr], names=["a", "_rowaddr"])
    store[checkpoint_key] = batch

    class _Queue:
        def __init__(self, items) -> None:
            self._items = deque(items)

        def get(self) -> tuple[int, str, int]:
            return self._items.popleft()

    queue = _Queue([(0, checkpoint_key, 3), (-1, "", 0)])

    base_schema = ds.schema
    fields = [base_schema.field("a"), pa.field("_rowaddr", pa.uint64())]
    filler_schema = pa.schema(fields)
    field_ids, column_indices = extract_field_ids_and_column_indices(
        ds.lance_schema, ["a"], ds.data_storage_version
    )

    def _boom(*args, **kwargs) -> NoReturn:
        raise AssertionError("lance.dataset should not be called")

    monkeypatch.setattr(lance, "dataset", _boom)

    writer_cls = FragmentWriter.__ray_actor_class__
    writer = writer_cls(
        ds.uri,
        ["a"],
        store.uri(),
        0,
        queue,
        read_version=ds.version,
        filler_schema=filler_schema,
        field_ids=field_ids,
        column_indices=column_indices,
        num_physical_rows=num_physical_rows,
        num_logical_rows=num_logical_rows,
        data_storage_version=ds.data_storage_version,
    )

    result = writer.write()
    assert result.frag_id == 0
    assert result.rows_written == num_physical_rows


def test_fragment_writer_falls_back_to_open_dataset(
    tmp_path: Path, monkeypatch
) -> None:
    """Ensure writer opens dataset when metadata is missing."""
    from collections import deque

    tbl_path = tmp_path / "tbl.lance"
    ds = lance.write_dataset(pa.table({"a": [1, 2, 3]}), tbl_path)

    store = CheckpointStore.from_uri(str(tmp_path / "ckp"))
    checkpoint_key = "fragment_0_batch_0"
    rowaddr = pa.array([0, 1, 2], type=pa.uint64())
    batch = pa.record_batch([pa.array([10, 11, 12]), rowaddr], names=["a", "_rowaddr"])
    store[checkpoint_key] = batch

    class _Queue:
        def __init__(self, items) -> None:
            self._items = deque(items)

        def get(self) -> tuple[int, str, int]:
            return self._items.popleft()

    queue = _Queue([(0, checkpoint_key, 3), (-1, "", 0)])

    call_count = {"n": 0}
    original_dataset = lance.dataset

    def _wrapped(*args, **kwargs) -> Any:
        call_count["n"] += 1
        return original_dataset(*args, **kwargs)

    monkeypatch.setattr(lance, "dataset", _wrapped)

    writer_cls = FragmentWriter.__ray_actor_class__
    writer = writer_cls(
        ds.uri,
        ["a"],
        store.uri(),
        0,
        queue,
        read_version=ds.version,
        filler_schema=None,
        field_ids=None,
        num_physical_rows=None,
        num_logical_rows=None,
    )

    result = writer.write()
    assert result.frag_id == 0
    assert result.rows_written == 3
    assert call_count["n"] == 1


@pytest.mark.parametrize(
    ("version_str", "expected"),
    [("2.0", (2, 0)), ("2.1", (2, 1)), ("3.0", (3, 0))],
)
def test_parse_data_storage_version(
    version_str: str, expected: tuple[int, int]
) -> None:
    from geneva.utils import parse_data_storage_version

    assert parse_data_storage_version(version_str) == expected


@pytest.mark.parametrize("data_storage_version", ["2.0", "2.1"])
def test_collect_skipped_fragments_uses_dataset_version(
    tmp_path: Path, data_storage_version: str
) -> None:
    """_collect_skipped_fragments must create DataFile with the dataset's version."""
    from geneva.runners.ray.pipeline import _collect_skipped_fragments

    # Create a 2-fragment dataset with explicit data_storage_version
    ds_path = str(tmp_path / "ds.lance")
    lance.write_dataset(
        pa.table({"a": [1, 2, 3]}),
        ds_path,
        data_storage_version=data_storage_version,
    )
    lance.write_dataset(
        pa.table({"a": [4, 5, 6]}),
        ds_path,
        mode="append",
    )

    db = connect(tmp_path)
    tbl = db.open_table("ds")

    @udf(data_type=pa.int64())
    def double_a(a: int) -> int:
        return a * 2

    tbl.add_columns({"a2": double_a})

    ds = lance.dataset(ds_path)
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    map_task = BackfillUDFTask(
        udfs={"a2": double_a},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    # Checkpoint fragment 0 — use the same dedupe key that _collect_skipped_fragments
    # computes internally (no src_files_hash, no dataset_version)
    dedupe_key = _get_fragment_dedupe_key(ds.uri, 0, map_task)
    fake_file = "fragment_0.lance"
    store[dedupe_key] = pa.RecordBatch.from_pydict({"file": [fake_file]})

    skipped, stats = _collect_skipped_fragments(
        dst_dataset=ds,
        dst_frags_with_checkpoint={0},
        map_task=map_task,
        checkpoint_store=store,
    )

    assert 0 in skipped
    df, row_count = skipped[0]
    major, minor = data_storage_version.split(".")
    assert df.file_major_version == int(major)
    assert df.file_minor_version == int(minor)
    assert row_count > 0


# ---------------------------------------------------------------------------
# Helpers for extension-type / multiprocess tests
# ---------------------------------------------------------------------------


def _make_blob_batch(n_rows: int = 3) -> pa.RecordBatch:
    """Create a RecordBatch with a ``_rowaddr`` column and a BlobType column."""
    blob_arr = BlobArray.from_pylist([f"data_{i}".encode() for i in range(n_rows)])
    return pa.record_batch(
        {
            "_rowaddr": pa.array(list(range(n_rows)), type=pa.uint64()),
            "blob_col": blob_arr,
        }
    )


def _make_standard_batch(n_rows: int = 3) -> pa.RecordBatch:
    """Create a simple RecordBatch with no extension types."""
    return pa.record_batch(
        {
            "_rowaddr": pa.array(list(range(n_rows)), type=pa.uint64()),
            "value": pa.array(list(range(n_rows)), type=pa.int64()),
        }
    )


# ---------------------------------------------------------------------------
# Test Group 1: _strip_extension_types / _restore_extension_types
# ---------------------------------------------------------------------------


def test_strip_extension_types_no_extension_columns() -> None:
    """Standard batch passes through unchanged (same object)."""
    batch = _make_standard_batch()
    result = _strip_extension_types(batch)
    assert result is batch  # identity — no copy


def test_strip_extension_types_with_blob_column() -> None:
    """BlobType column is replaced with its struct storage type."""
    batch = _make_blob_batch()
    stripped = _strip_extension_types(batch)

    # The blob column should now be the storage struct type
    blob_field = stripped.schema.field("blob_col")
    assert not isinstance(blob_field.type, pa.ExtensionType)
    assert pa.types.is_struct(blob_field.type)

    # Metadata should contain the extension type name.  Lance only defines
    # BlobType with extension_name "lance.blob.v2" — there is no v1 variant.
    # _get_extension_type uses startswith("lance.blob") so future versions
    # (e.g. v3) would be handled without code changes.
    assert blob_field.metadata is not None
    assert blob_field.metadata[b"__ext_type_name"] == b"lance.blob.v2"
    assert b"__ext_type_serialized" in blob_field.metadata

    # Non-extension column is unchanged
    assert stripped.schema.field("_rowaddr").type == pa.uint64()


def test_restore_extension_types_roundtrip() -> None:
    """Strip then restore preserves type and data values."""
    batch = _make_blob_batch()
    stripped = _strip_extension_types(batch)
    restored = _restore_extension_types(stripped)

    # Type must be restored
    assert isinstance(restored.schema.field("blob_col").type, BlobType)

    # Data must be preserved
    assert (
        restored.column("blob_col").to_pylist() == batch.column("blob_col").to_pylist()
    )
    assert restored.column("_rowaddr") == batch.column("_rowaddr")

    # Metadata markers must be cleaned up
    restored_meta = restored.schema.field("blob_col").metadata
    assert restored_meta is None or b"__ext_type_name" not in restored_meta


def test_strip_restore_with_nulls() -> None:
    """Null values in a BlobType column survive the roundtrip."""
    blob_arr = BlobArray.from_pylist([b"hello", None, b"world"])
    batch = pa.record_batch(
        {
            "_rowaddr": pa.array([0, 1, 2], type=pa.uint64()),
            "blob_col": blob_arr,
        }
    )
    restored = _restore_extension_types(_strip_extension_types(batch))

    assert isinstance(restored.schema.field("blob_col").type, BlobType)
    py_vals = restored.column("blob_col").to_pylist()
    assert py_vals[1] is None
    assert py_vals[0] is not None
    assert py_vals[2] is not None


def test_strip_restore_with_multiple_extension_columns() -> None:
    """Two BlobType columns are both correctly stripped and restored."""
    blob_a = BlobArray.from_pylist([b"a1", b"a2"])
    blob_b = BlobArray.from_pylist([b"b1", b"b2"])
    batch = pa.record_batch(
        {
            "_rowaddr": pa.array([0, 1], type=pa.uint64()),
            "blob_a": blob_a,
            "blob_b": blob_b,
        }
    )

    stripped = _strip_extension_types(batch)
    assert not isinstance(stripped.schema.field("blob_a").type, pa.ExtensionType)
    assert not isinstance(stripped.schema.field("blob_b").type, pa.ExtensionType)

    restored = _restore_extension_types(stripped)
    assert isinstance(restored.schema.field("blob_a").type, BlobType)
    assert isinstance(restored.schema.field("blob_b").type, BlobType)
    assert restored.column("blob_a").to_pylist() == batch.column("blob_a").to_pylist()
    assert restored.column("blob_b").to_pylist() == batch.column("blob_b").to_pylist()


def test_strip_restore_with_mixed_columns() -> None:
    """Only the extension column is affected; int and string columns are untouched."""
    blob_arr = BlobArray.from_pylist([b"x"])
    batch = pa.record_batch(
        {
            "_rowaddr": pa.array([0], type=pa.uint64()),
            "name": pa.array(["alice"], type=pa.utf8()),
            "blob_col": blob_arr,
            "score": pa.array([42], type=pa.int32()),
        }
    )

    restored = _restore_extension_types(_strip_extension_types(batch))
    assert restored.schema.field("name").type == pa.utf8()
    assert restored.schema.field("score").type == pa.int32()
    assert isinstance(restored.schema.field("blob_col").type, BlobType)
    assert restored.column("name").to_pylist() == ["alice"]
    assert restored.column("score").to_pylist() == [42]


def test_strip_restore_preserves_existing_metadata() -> None:
    """Pre-existing field metadata survives the roundtrip."""
    blob_arr = BlobArray.from_pylist([b"hi"])
    field = pa.field(
        "blob_col",
        BlobType(),
        metadata={b"lance-encoding:blob": b"true", b"custom_key": b"custom_val"},
    )
    batch = pa.RecordBatch.from_arrays(
        [pa.array([0], type=pa.uint64()), blob_arr],
        schema=pa.schema([pa.field("_rowaddr", pa.uint64()), field]),
    )

    restored = _restore_extension_types(_strip_extension_types(batch))
    meta = restored.schema.field("blob_col").metadata
    assert meta[b"lance-encoding:blob"] == b"true"
    assert meta[b"custom_key"] == b"custom_val"
    # Internal markers should be cleaned
    assert b"__ext_type_name" not in meta


# ---------------------------------------------------------------------------
# Test Group 2: _batch_to_buf / _buf_to_batch IPC round-trip
# ---------------------------------------------------------------------------


def test_ipc_roundtrip_standard_batch() -> None:
    """Regression: standard batch survives IPC round-trip unchanged."""
    batch = _make_standard_batch(5)
    buf = _batch_to_buf(batch)
    batches = _buf_to_batch(buf, coalesce=False)
    assert len(batches) == 1
    result = batches[0]
    assert result.schema == batch.schema
    assert result.to_pydict() == batch.to_pydict()


def test_ipc_roundtrip_blob_batch() -> None:
    """Blob batch survives IPC round-trip with extension type preserved."""
    batch = _make_blob_batch(4)
    buf = _batch_to_buf(batch)
    batches = _buf_to_batch(buf, coalesce=False)
    assert len(batches) == 1
    result = batches[0]

    assert isinstance(result.schema.field("blob_col").type, BlobType)
    assert result.column("blob_col").to_pylist() == batch.column("blob_col").to_pylist()
    assert result.column("_rowaddr").to_pylist() == batch.column("_rowaddr").to_pylist()


def test_ipc_roundtrip_blob_batch_coalesce() -> None:
    """Blob batch survives IPC round-trip with coalesce=True."""
    batch = _make_blob_batch(3)
    buf = _batch_to_buf(batch)
    result = _buf_to_batch(buf, coalesce=True)
    assert isinstance(result, pa.RecordBatch)
    assert isinstance(result.schema.field("blob_col").type, BlobType)
    assert result.column("blob_col").to_pylist() == batch.column("blob_col").to_pylist()


def test_ipc_roundtrip_empty_blob_batch() -> None:
    """Zero-row batch with blob schema survives IPC round-trip."""
    blob_arr = BlobArray.from_pylist([])
    batch = pa.record_batch(
        {
            "_rowaddr": pa.array([], type=pa.uint64()),
            "blob_col": blob_arr,
        }
    )
    buf = _batch_to_buf(batch)

    batches = _buf_to_batch(buf, coalesce=False)
    if batches:
        assert batches[0].num_rows == 0

    result = _buf_to_batch(buf, coalesce=True)
    assert result.num_rows == 0


def test_ipc_roundtrip_mixed_columns() -> None:
    """Batch with both blob and standard columns survives IPC."""
    blob_arr = BlobArray.from_pylist([b"one", b"two"])
    batch = pa.record_batch(
        {
            "_rowaddr": pa.array([0, 1], type=pa.uint64()),
            "label": pa.array(["a", "b"], type=pa.utf8()),
            "blob_col": blob_arr,
            "count": pa.array([10, 20], type=pa.int64()),
        }
    )
    buf = _batch_to_buf(batch)
    result = _buf_to_batch(buf, coalesce=True)

    assert isinstance(result.schema.field("blob_col").type, BlobType)
    assert result.schema.field("label").type == pa.utf8()
    assert result.schema.field("count").type == pa.int64()
    assert result.to_pydict()["label"] == ["a", "b"]
    assert result.to_pydict()["count"] == [10, 20]


# ---------------------------------------------------------------------------
# Test Group 3: MultiProcessBatchApplier integration
# ---------------------------------------------------------------------------


def test_multiprocess_applier_standard_batch() -> None:
    """Regression: standard batches through MultiProcessBatchApplier."""
    from geneva.debug.logger import NoOpErrorLogger

    @udf(data_type=pa.int64(), input_columns=["value"])
    def double_value(value: int) -> int:
        return value * 2

    n_rows = 6
    batch = pa.record_batch(
        {
            "_rowaddr": pa.array(list(range(n_rows)), type=pa.uint64()),
            "value": pa.array(list(range(n_rows)), type=pa.int64()),
        }
    )

    read_task = _DummyReadTask(frag_id=0, rows=n_rows, batches=[batch])
    map_task = BackfillUDFTask(udfs={"result": double_value})

    applier = MultiProcessBatchApplier(num_processes=2, job_id="test")
    results = list(applier.run(read_task, map_task, NoOpErrorLogger()))

    assert len(results) >= 1
    combined = pa.concat_tables([pa.table(b) for b in results]).to_pydict()
    assert combined["result"] == [0, 2, 4, 6, 8, 10]


def _multiprocess_trim_batches(n: int) -> list[pa.RecordBatch]:
    return [
        pa.record_batch(
            {
                "_rowaddr": pa.array([i], type=pa.uint64()),
                "value": pa.array([i], type=pa.int64()),
            }
        )
        for i in range(n)
    ]


@udf(data_type=pa.int64(), input_columns=["value"])
def _trim_double(value: int) -> int:
    return value * 2


def _run_multiprocess_counting_trims(
    monkeypatch: pytest.MonkeyPatch,
    n_batches: int,
) -> tuple[int, int]:
    """Run the multiprocess applier; return ``(yielded, parent trim calls)``."""
    from geneva.debug.logger import NoOpErrorLogger

    trims = 0

    def _record_trim() -> None:
        nonlocal trims
        trims += 1

    monkeypatch.setattr(
        "geneva.apply.memory.release_unused_process_memory",
        _record_trim,
    )

    batches = _multiprocess_trim_batches(n_batches)
    read_task = _DummyReadTask(frag_id=0, rows=n_batches, batches=batches)
    map_task = BackfillUDFTask(udfs={"result": _trim_double})

    applier = MultiProcessBatchApplier(num_processes=2, job_id="test")
    results = list(applier.run(read_task, map_task, NoOpErrorLogger()))
    return len(results), trims


def test_multiprocess_applier_parent_trims_memory_every_eight_batches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The parent process churns scan batches and IPC buffers even though the
    UDF runs in the pool, so it trims on the SimpleApplier cadence."""
    monkeypatch.delenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", raising=False)

    yielded, trims = _run_multiprocess_counting_trims(monkeypatch, n_batches=9)

    assert yielded == 9
    assert trims == 1


def test_multiprocess_applier_parent_memory_trim_can_be_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", "0")

    yielded, trims = _run_multiprocess_counting_trims(monkeypatch, n_batches=9)

    assert yielded == 9
    assert trims == 0


def test_multiprocess_applier_parent_trim_counter_spans_read_tasks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """One applier serves many ReadTasks, so the parent's trim counter must
    survive ``run``. Five 5-batch tasks are 25 batches: three trims, not zero.

    A per-run counter never reaches the interval on tasks this short, so the
    parent would hold scan and IPC arenas for the whole job.
    """
    from geneva.debug.logger import NoOpErrorLogger

    monkeypatch.delenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", raising=False)

    trims = 0

    def _record_trim() -> None:
        nonlocal trims
        trims += 1

    monkeypatch.setattr(
        "geneva.apply.memory.release_unused_process_memory",
        _record_trim,
    )

    map_task = BackfillUDFTask(udfs={"result": _trim_double})
    applier = MultiProcessBatchApplier(num_processes=2, job_id="test")

    yielded = 0
    for frag_id in range(5):
        batches = _multiprocess_trim_batches(5)
        read_task = _DummyReadTask(frag_id=frag_id, rows=5, batches=batches)
        yielded += len(list(applier.run(read_task, map_task, NoOpErrorLogger())))

    assert yielded == 25
    assert trims == 3
    # 25 % 8 == 1: the remainder carries into the next task rather than
    # being discarded at the task boundary.
    assert applier.trim_counter.batches_since_trim == 1


def test_worker_trim_memory_fires_on_interval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Pool workers keep their own counter; they run the UDF, so they are
    where decode buffers accumulate."""
    from geneva.apply import multiprocess as mp_applier

    trims = 0

    def _record_trim() -> None:
        nonlocal trims
        trims += 1

    monkeypatch.delenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", raising=False)
    monkeypatch.setattr(mp_applier._WORKER_TRIM_COUNTER, "batches_since_trim", 0)
    monkeypatch.setattr(
        "geneva.apply.memory.release_unused_process_memory",
        _record_trim,
    )

    for _ in range(16):
        mp_applier._worker_trim_memory()
    assert trims == 2

    monkeypatch.setenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", "0")
    for _ in range(16):
        mp_applier._worker_trim_memory()
    assert trims == 2


class _FakeFuture:
    """Minimal stand-in for a multiprocess ``AsyncResult``.

    ``ready_after`` makes the future flip to ready once ``wait`` has been
    called that many times, standing in for a slow batch that does return.
    """

    def __init__(self, ready: bool, ready_after: int | None = None) -> None:
        self._ready = ready
        self._ready_after = ready_after
        self.waits = 0

    def wait(self, timeout: float | None = None) -> None:
        self.waits += 1
        if self._ready_after is not None and self.waits >= self._ready_after:
            self._ready = True

    def ready(self) -> bool:
        return self._ready


def test_await_head_ready_tolerates_out_of_order_completion() -> None:
    """A younger future finishing first is normal on a healthy pool (GEN-857).

    With more than one worker, ``apply_async`` hands out tasks in order but
    they complete in whatever order the work finishes. Pre-fix this was taken
    as proof the head's worker had died and failed the job outright.
    """
    import time

    applier = MultiProcessBatchApplier(num_processes=4, job_id="test")
    # Head is slow; two younger batches are already done.
    futs = [
        _FakeFuture(ready=False, ready_after=3),
        _FakeFuture(ready=True),
        _FakeFuture(ready=True),
    ]

    applier._await_head_ready(futs, time.monotonic(), stall_timeout_s=100)

    assert futs[0].ready()


def test_await_head_ready_tolerates_slow_batch() -> None:
    """A batch slower than the poll interval is not a crash on its own.

    Only the stall bound may condemn a batch, and it is measured from the last
    completed batch, not from how long this one has taken.
    """
    import time

    applier = MultiProcessBatchApplier(num_processes=2, job_id="test")
    slow = _FakeFuture(ready=False, ready_after=5)

    applier._await_head_ready([slow], time.monotonic(), stall_timeout_s=100)

    assert slow.ready()
    assert slow.waits == 5


def test_await_head_ready_stall_backstop() -> None:
    """A head that never returns escalates after the stall bound."""
    import time

    from geneva.errors import FatalWorkerCrashError

    applier = MultiProcessBatchApplier(num_processes=1, job_id="test")
    # last_progress far in the past => stall bound already exceeded.
    with pytest.raises(FatalWorkerCrashError, match="stalled"):
        applier._await_head_ready(
            [_FakeFuture(ready=False)], time.monotonic() - 1000, stall_timeout_s=1
        )


def test_await_head_ready_returns_when_head_ready() -> None:
    """A ready head returns immediately without raising."""
    import time

    applier = MultiProcessBatchApplier(num_processes=1, job_id="test")
    applier._await_head_ready(
        [_FakeFuture(ready=True)], time.monotonic(), stall_timeout_s=1
    )


def test_multiprocess_applier_survives_out_of_order_batches() -> None:
    """Uneven batch durations must not be reported as a worker crash (GEN-857).

    The first batch is deliberately slow so several younger batches finish
    ahead of it across four workers. Pre-fix, that alone raised
    ``FatalWorkerCrashError`` and escalated a healthy job to the Ray layer.
    """
    from geneva.debug.logger import NoOpErrorLogger

    @udf(data_type=pa.int64(), input_columns=["value"])
    def slow_first_batch(value: int) -> int:
        import time as _time

        if value == 0:
            _time.sleep(2.0)
        return value * 2

    n_batches = 16
    batches = [
        pa.record_batch(
            {
                "_rowaddr": pa.array([i], type=pa.uint64()),
                "value": pa.array([i], type=pa.int64()),
            }
        )
        for i in range(n_batches)
    ]
    read_task = _DummyReadTask(frag_id=0, rows=n_batches, batches=batches)
    map_task = BackfillUDFTask(udfs={"result": slow_first_batch})

    applier = MultiProcessBatchApplier(num_processes=4, job_id="test")
    results = list(applier.run(read_task, map_task, NoOpErrorLogger()))

    combined = pa.concat_tables([pa.table(b) for b in results]).to_pydict()
    assert combined["result"] == [i * 2 for i in range(n_batches)]


def test_multiprocess_applier_raises_on_worker_crash(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A fork child that dies mid-task surfaces as FatalWorkerCrashError within
    a bounded time, instead of wedging forever (GEN-576).

    Pre-fix, ``_process_future_result`` called ``fut.get()`` with no timeout;
    the orphaned future of the dead worker never completed and the applier hung
    indefinitely.
    """
    import os
    import signal
    import time

    from geneva.debug.logger import NoOpErrorLogger
    from geneva.errors import FatalWorkerCrashError

    # The stall bound is the detector, so shorten it rather than wait out the
    # 600s production default.
    monkeypatch.setenv("GENEVA_APPLIER_WORKER_STALL_TIMEOUT_S", "15")

    @udf(data_type=pa.int64(), input_columns=["value"])
    def crash_on_sentinel(value: int) -> int:
        if value == 999:
            # This child crash is intentional. Suppress both pytest's
            # faulthandler output and the CI core dump reserved for unexpected
            # parent-interpreter crashes.
            import faulthandler
            import resource

            faulthandler.disable()
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
            os.kill(os.getpid(), signal.SIGSEGV)
        return value * 2

    # Eight single-row batches; batch 1 carries the poison sentinel. With two
    # workers, the crashing batch orphans its future while later batches finish.
    batches = [
        pa.record_batch(
            {
                "_rowaddr": pa.array([i], type=pa.uint64()),
                "value": pa.array([999 if i == 1 else i], type=pa.int64()),
            }
        )
        for i in range(8)
    ]
    read_task = _DummyReadTask(frag_id=0, rows=8, batches=batches)
    map_task = BackfillUDFTask(udfs={"result": crash_on_sentinel})

    applier = MultiProcessBatchApplier(num_processes=2, job_id="test")

    start = time.monotonic()
    with pytest.raises(FatalWorkerCrashError):
        list(applier.run(read_task, map_task, NoOpErrorLogger()))
    assert time.monotonic() - start < 60, "should fail fast, not wedge"


def test_multiprocess_applier_blob_batch() -> None:
    """Blob-containing batch through MultiProcessBatchApplier.

    The UDF receives a RecordBatch where the blob column has its BlobType
    extension type intact.  It extracts the inline data length.
    """
    from geneva.debug.logger import NoOpErrorLogger

    @udf(data_type=pa.int64())
    def blob_data_len(batch: pa.RecordBatch) -> pa.Array:
        # The blob column should be a BlobType extension array.
        # Access the underlying struct's "data" field to get the binary data.
        blob_col = batch.column("blob_col")
        storage = blob_col.storage if hasattr(blob_col, "storage") else blob_col
        data_arr = storage.field("data")
        return pa.array(
            [len(v.as_py()) if v.is_valid else 0 for v in data_arr],
            type=pa.int64(),
        )

    batch = _make_blob_batch(4)
    read_task = _DummyReadTask(frag_id=0, rows=4, batches=[batch])
    map_task = BackfillUDFTask(udfs={"data_len": blob_data_len})

    applier = MultiProcessBatchApplier(num_processes=2, job_id="test")
    results = list(applier.run(read_task, map_task, NoOpErrorLogger()))

    assert len(results) >= 1
    combined = pa.concat_tables([pa.table(b) for b in results]).to_pydict()
    expected_lens = [len(f"data_{i}".encode()) for i in range(4)]
    assert combined["data_len"] == expected_lens


def test_multiprocess_applier_multiple_blob_batches() -> None:
    """Multiple blob batches exercise the backpressure path."""
    from geneva.debug.logger import NoOpErrorLogger

    @udf(data_type=pa.int64())
    def blob_size(batch: pa.RecordBatch) -> pa.Array:
        blob_col = batch.column("blob_col")
        storage = blob_col.storage if hasattr(blob_col, "storage") else blob_col
        data_arr = storage.field("data")
        return pa.array(
            [len(v.as_py()) if v.is_valid else 0 for v in data_arr],
            type=pa.int64(),
        )

    batches = [_make_blob_batch(3) for _ in range(5)]
    total_rows = sum(b.num_rows for b in batches)
    read_task = _DummyReadTask(frag_id=0, rows=total_rows, batches=batches)
    map_task = BackfillUDFTask(udfs={"size": blob_size})

    applier = MultiProcessBatchApplier(num_processes=2, job_id="test")
    results = list(applier.run(read_task, map_task, NoOpErrorLogger()))

    combined = pa.concat_tables([pa.table(b) for b in results]).to_pydict()
    assert len(combined["size"]) == total_rows
    # Each batch has data_0, data_1, data_2 → lengths 6, 6, 6
    assert all(v == 6 for v in combined["size"])


def test_multiprocess_applier_blob_batch_with_error_handling() -> None:
    """Blob batch through the _worker_apply error-handling code path.

    When a UDF has an ``error_handling`` config, MultiProcessBatchApplier
    routes through ``_worker_apply`` instead of ``_apply_with_stream_buf``.
    Both paths deserialise via ``_buf_to_batch`` and must restore extension
    types.
    """
    from geneva.debug.error_store import ErrorHandlingConfig, UDFRetryConfig
    from geneva.debug.logger import NoOpErrorLogger

    @udf(
        data_type=pa.int64(),
        error_handling=ErrorHandlingConfig(
            retry_config=UDFRetryConfig.no_retry(),
            log_errors=False,
        ),
    )
    def blob_len_eh(batch: pa.RecordBatch) -> pa.Array:
        blob_col = batch.column("blob_col")
        storage = blob_col.storage if hasattr(blob_col, "storage") else blob_col
        data_arr = storage.field("data")
        return pa.array(
            [len(v.as_py()) if v.is_valid else 0 for v in data_arr],
            type=pa.int64(),
        )

    batch = _make_blob_batch(4)
    read_task = _DummyReadTask(frag_id=0, rows=4, batches=[batch])
    map_task = BackfillUDFTask(udfs={"data_len": blob_len_eh})

    applier = MultiProcessBatchApplier(num_processes=2, job_id="test")
    results = list(applier.run(read_task, map_task, NoOpErrorLogger()))

    assert len(results) >= 1
    combined = pa.concat_tables([pa.table(b) for b in results]).to_pydict()
    expected_lens = [len(f"data_{i}".encode()) for i in range(4)]
    assert combined["data_len"] == expected_lens


# ---------------------------------------------------------------------------
# Test Group 4: Edge cases and error paths
# ---------------------------------------------------------------------------


def test_restore_extension_types_no_markers() -> None:
    """Batch without extension markers passes through unchanged (same object)."""
    batch = _make_standard_batch()
    result = _restore_extension_types(batch)
    assert result is batch  # identity — no copy


def test_get_extension_type_unknown_raises() -> None:
    """_get_extension_type raises ValueError for an unrecognised type name."""
    from geneva.apply.multiprocess import _get_extension_type

    with pytest.raises(ValueError, match="Unknown Arrow extension type"):
        _get_extension_type("acme.custom_type", pa.int32(), b"")


def test_ipc_roundtrip_blob_batch_multiple_cycles() -> None:
    """Blob batch survives two consecutive serialize-deserialize cycles."""
    batch = _make_blob_batch(3)
    buf1 = _batch_to_buf(batch)
    mid = _buf_to_batch(buf1, coalesce=True)
    buf2 = _batch_to_buf(mid)
    result = _buf_to_batch(buf2, coalesce=True)

    assert isinstance(result.schema.field("blob_col").type, BlobType)
    assert result.column("blob_col").to_pylist() == batch.column("blob_col").to_pylist()


# ---------------------------------------------------------------------------
# Test Group 5: list[dict] blob batch serialization
# ---------------------------------------------------------------------------


def test_list_dict_batch_to_buf_roundtrip() -> None:
    """list[dict] blob batches survive _batch_to_buf/_buf_to_batch round-trip."""
    batch = [{"_rowaddr": 0, "data": b"hello"}, {"_rowaddr": 1, "data": b"world"}]
    buf = _batch_to_buf(batch)
    assert buf.startswith(_LIST_DICT_MARKER)

    result = _buf_to_batch(buf, coalesce=False)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] == batch

    coalesced = _buf_to_batch(buf, coalesce=True)
    assert coalesced == batch


def test_list_dict_batch_size_tracking() -> None:
    """MultiProcessBatchApplier tracks len(batch) for list[dict] batches."""
    batch = [{"_rowaddr": i, "val": i} for i in range(5)]
    assert not isinstance(batch, pa.RecordBatch)
    assert len(batch) == 5


# ---------------------------------------------------------------------------
# Test Group 6: _picklable_worker_error
# ---------------------------------------------------------------------------


def test_picklable_worker_error_simple() -> None:
    """_picklable_worker_error converts exception to RuntimeError with message."""
    exc = ValueError("test error")
    result = _picklable_worker_error(exc)
    assert isinstance(result, RuntimeError)
    assert "ValueError: test error" in str(result)


def test_picklable_worker_error_chain() -> None:
    """_picklable_worker_error preserves the exception chain."""
    root = OSError("disk full")
    mid = RuntimeError("write failed")
    mid.__cause__ = root
    result = _picklable_worker_error(mid)
    assert isinstance(result, RuntimeError)
    msg = str(result)
    assert "RuntimeError: write failed" in msg
    assert "OSError: disk full" in msg
    assert "caused by" in msg


def test_picklable_worker_error_no_cycle() -> None:
    """_picklable_worker_error handles self-referencing exception chains."""
    exc = ValueError("loop")
    exc.__cause__ = exc
    result = _picklable_worker_error(exc)
    assert isinstance(result, RuntimeError)
    assert "ValueError: loop" in str(result)


def test_has_udf_version_mismatch_reads_keys_only() -> None:
    """The UDF-version check decides from key names without reading checkpoints.

    The version token lives in the key's ``_ver-`` segment, so detection must
    not open any checkpoint (GEN-606). A store that raises on ``__getitem__``
    proves no content read happens for either the match or mismatch case. The
    check now lives on the store API (``has_udf_version_mismatch``, GEN-614).
    """
    from geneva.checkpoint_utils import format_checkpoint_prefix

    class NoReadStore(InMemoryCheckpointStore):
        def __getitem__(self, item: str) -> pa.RecordBatch:
            raise AssertionError(f"unexpected checkpoint read: {item}")

    def frag_key(version: str, *, frag: int) -> str:
        prefix = format_checkpoint_prefix(
            udf_name="embed",
            udf_version=version,
            column="c",
            where=None,
            dataset_uri="memory://t",
        )
        return f"{prefix}_frag-{frag}"

    store = NoReadStore()
    batch = pa.record_batch({"file": ["f"]})
    store[frag_key("v1", frag=0)] = batch
    store[frag_key("v1", frag=1)] = batch
    # Per-batch range key for a different version must be ignored (no token).
    store[f"{frag_key('v9', frag=0)}_range-0-10"] = batch

    # Same version: no mismatch, and the range key is not treated as one.
    assert store.has_udf_version_mismatch("c", "v1") is False
    # Different version: mismatch detected purely from the key.
    assert store.has_udf_version_mismatch("c", "v2") is True


def test_has_udf_version_mismatch_legacy_key_assumes_mismatch() -> None:
    """A key with no parseable version token is treated as a mismatch."""
    store = InMemoryCheckpointStore()
    store["udf-embed_col-c_where-h_uri-u_frag-0"] = pa.record_batch({"file": ["f"]})

    assert store.has_udf_version_mismatch("c", "v1") is True
