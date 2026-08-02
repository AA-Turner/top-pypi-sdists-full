# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import time
from collections.abc import Iterator

import pyarrow as pa
import pyarrow.compute as pc

from geneva.apply import CheckpointingApplier, _count_udf_rows
from geneva.apply.task import (
    DEFAULT_CHECKPOINT_ROWS,
    BackfillUDFTask,
    ReadTask,
)
from geneva.transformer import BACKFILL_SELECTED, udf


def test_count_udf_rows_recordbatch_with_and_without_mask() -> None:
    batch_with_mask = pa.record_batch(
        [
            pa.array([1, 2, 3]),
            pa.array([True, False, True]),
        ],
        names=["a", BACKFILL_SELECTED],
    )
    assert _count_udf_rows(batch_with_mask) == 2

    batch_no_mask = pa.record_batch([pa.array([10, 20])], names=["a"])
    assert _count_udf_rows(batch_no_mask) == 2


def test_count_udf_rows_list_of_dicts() -> None:
    rows = [
        {"a": 1, BACKFILL_SELECTED: True},
        {"a": 2, BACKFILL_SELECTED: False},
        {"a": 3},  # defaults to selected
    ]
    assert _count_udf_rows(rows) == 2


class _DummyReadTask(ReadTask):
    def __init__(self, batches: list[pa.RecordBatch]) -> None:
        self._batches = batches

    def to_batches(
        self,
        *,
        batch_size: int = DEFAULT_CHECKPOINT_ROWS,
    ) -> Iterator[pa.RecordBatch]:
        yield from self._batches

    def checkpoint_key(self) -> str:
        return "dummy"

    def dest_frag_id(self) -> int:
        return 0

    def dest_offset(self) -> int:
        return 0

    def num_rows(self) -> int:
        return sum(batch.num_rows for batch in self._batches)

    def table_uri(self) -> str:
        return "memory://dummy"


class _EmptyReadTask(ReadTask):
    """ReadTask that represents rows but yields no batches."""

    def __init__(self, *, num_rows: int, offset: int = 0, frag_id: int = 0) -> None:
        self._num_rows = num_rows
        self._offset = offset
        self._frag_id = frag_id
        self.version = None
        self.where = None

    def to_batches(
        self,
        *,
        batch_size: int = DEFAULT_CHECKPOINT_ROWS,
    ) -> Iterator[pa.RecordBatch]:
        if False:  # pragma: no cover
            yield  # type: ignore[misc]

    def checkpoint_key(self) -> str:
        return "empty"

    def dest_frag_id(self) -> int:
        return self._frag_id

    def dest_offset(self) -> int:
        return self._offset

    def num_rows(self) -> int:
        return self._num_rows

    def table_uri(self) -> str:
        return "memory://dummy"


@udf(data_type=pa.int32())
def _double(a: int) -> int:
    return a * 2


def test_checkpointing_applier_reports_cnt_udf_computed() -> None:
    map_task = BackfillUDFTask(udfs={"b": _double})

    batches = [
        pa.record_batch(
            [
                pa.array([1, 2]),
                pa.array([True, True]),
                pa.array([0, 1], type=pa.uint64()),
            ],
            names=["a", BACKFILL_SELECTED, "_rowaddr"],
        ),
        pa.record_batch(
            [
                pa.array([3, 4]),
                pa.array([True, False]),
                pa.array([2, 3], type=pa.uint64()),
            ],
            names=["a", BACKFILL_SELECTED, "_rowaddr"],
        ),
    ]
    read_task = _DummyReadTask(batches)

    applier = CheckpointingApplier(checkpoint_uri="memory", map_task=map_task)
    checkpoints, direct_result, cnt_udf_computed = applier.run(read_task)
    assert direct_result is None

    assert cnt_udf_computed == 3
    total_rows = sum(
        applier.checkpoint_store[result.checkpoint_key].num_rows
        for result in checkpoints
    )
    assert total_rows == 4

    # No task-level aggregate checkpoint; only per-map-batch entries
    assert all(
        result.checkpoint_key in applier.checkpoint_store for result in checkpoints
    )


def test_empty_read_task_writes_completion_checkpoint() -> None:
    map_task = BackfillUDFTask(udfs={"b": _double})
    applier = CheckpointingApplier(checkpoint_uri="memory", map_task=map_task)
    read_task = _EmptyReadTask(num_rows=5, offset=10, frag_id=0)

    checkpoints, direct_result, cnt_udf_computed = applier.run(read_task)
    assert direct_result is None
    assert cnt_udf_computed == 0
    assert len(checkpoints) == 1

    expected_key = map_task.checkpoint_key(
        dataset_uri=read_task.table_uri(),
        dataset_version=None,
        frag_id=read_task.dest_frag_id(),
        start=read_task.dest_offset(),
        end=read_task.dest_offset() + read_task.num_rows(),
        where=None,
    )
    assert expected_key in applier.checkpoint_store
    assert applier.checkpoint_store[expected_key].num_rows == 5
    assert applier.status(read_task) is True

    before_keys = set(applier.checkpoint_store.list_keys())
    checkpoints2, direct_result, _ = applier.run(read_task)
    assert direct_result is None
    after_keys = set(applier.checkpoint_store.list_keys())
    assert before_keys == after_keys
    assert len(checkpoints2) == 1


@udf(data_type=pa.int32())
def _sleep_double_record_batch(rb: pa.RecordBatch) -> pa.Array:
    time.sleep(0.02)
    return pc.multiply(rb["a"], 2)


def test_checkpointing_applier_tracks_timing_metrics() -> None:
    map_task = BackfillUDFTask(udfs={"b": _sleep_double_record_batch})
    read_task = _DummyReadTask(
        [
            pa.record_batch(
                [
                    pa.array([1, 2]),
                    pa.array([True, True]),
                    pa.array([0, 1], type=pa.uint64()),
                ],
                names=["a", BACKFILL_SELECTED, "_rowaddr"],
            )
        ]
    )

    applier = CheckpointingApplier(checkpoint_uri="memory", map_task=map_task)
    applier.run(read_task)

    assert isinstance(applier.batch_checkpointing_time_ms, int)
    assert applier.batch_checkpointing_time_ms >= 0
    assert applier.batch_applier.udf_processing_time_ms >= 10  # type: ignore[attr-defined]
