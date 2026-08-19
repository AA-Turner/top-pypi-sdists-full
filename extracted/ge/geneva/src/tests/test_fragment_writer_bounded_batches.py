# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Bounded FragmentWriter input batching for GEN-780."""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock, patch

import pyarrow as pa
import pytest
from geneva_faults import CheckpointFaultPolicy, FlakyCheckpointStore

from geneva.checkpoint import CheckpointStore, stamp_checkpoint_num_rows
from geneva.runners.ray.pipeline import _SEAL_SENTINEL
from geneva.runners.ray.writer import (
    FragmentWriter,
    _align_batches_to_physical_layout,
    _buffer_and_sort_batches,
    _read_checkpoint_batches,
)

if TYPE_CHECKING:
    from collections.abc import Iterator


class _RangeCheckpointStore(CheckpointStore):
    """A store that makes accidental full checkpoint materialization fail."""

    def __init__(self, batch: pa.RecordBatch) -> None:
        self.batch = batch
        self.reads: list[tuple[int, int]] = []
        self.deleted: list[str] = []

    def __contains__(self, item: str) -> bool:
        return item.startswith("ckpt_range-")

    def __getitem__(self, item: str) -> pa.RecordBatch:
        raise AssertionError("bounded replay must not materialize the whole checkpoint")

    def __setitem__(self, key: str, value: pa.RecordBatch) -> None:
        raise NotImplementedError

    def read_range(self, key: str, start: int, num_rows: int) -> pa.RecordBatch:
        self.reads.append((start, num_rows))
        return self.batch.slice(start, num_rows)

    def list_keys(self, prefix: str = "") -> Iterator[str]:
        return iter(())

    def uri(self) -> str:
        return "memory:///"

    def delete(self, key: str) -> None:
        self.deleted.append(key)


class _ListQueue:
    def __init__(self, items: list[tuple[int, str, int]]) -> None:
        self.items = deque(items)

    def get(self) -> tuple[int, str, int]:
        return self.items.popleft()


def test_checkpoint_wrapper_delegates_bounded_range_reads() -> None:
    """Fault wrappers must preserve the inner store's true bounded-read path."""
    batch = pa.RecordBatch.from_pydict({"value": list(range(6))})
    inner = _RangeCheckpointStore(batch)
    wrapped = FlakyCheckpointStore(inner, CheckpointFaultPolicy())

    result = wrapped.read_range("ckpt_range-0-6", 2, 3)

    assert result.column("value").to_pylist() == [2, 3, 4]
    assert inner.reads == [(2, 3)]


def test_bounded_checkpoint_iteration_reads_only_on_demand() -> None:
    """The next checkpoint tranche is not resident before its consumer asks."""
    batch = pa.RecordBatch.from_pydict({"value": list(range(8))})
    store = _RangeCheckpointStore(batch)
    replay = iter(
        _read_checkpoint_batches(
            store,
            "ckpt_range-0-8",
            8,
            max_rows_per_batch=3,
        )
    )

    assert store.reads == []
    assert next(replay).column("value").to_pylist() == [0, 1, 2]
    assert store.reads == [(0, 3)]
    assert next(replay).column("value").to_pylist() == [3, 4, 5]
    assert store.reads == [(0, 3), (3, 3)]
    assert next(replay).column("value").to_pylist() == [6, 7]
    assert store.reads == [(0, 3), (3, 3), (6, 3)]
    with pytest.raises(StopIteration):
        next(replay)


def test_bounded_replay_range_reads_checkpoint_in_smaller_tranches() -> None:
    batch = pa.record_batch(
        [
            pa.array(range(8), type=pa.int64()),
            pa.array(range(8), type=pa.uint64()),
        ],
        names=["value", "_rowaddr"],
    )
    store = _RangeCheckpointStore(batch)
    queue = _ListQueue([(0, "ckpt_range-0-8", 8), _SEAL_SENTINEL])

    replay = list(
        _buffer_and_sort_batches(
            8,
            0,
            batch.schema,
            store,
            queue,  # type: ignore[arg-type]
            expect_full_coverage=True,
            max_rows_per_batch=3,
        )
    )

    assert [item.num_rows for item in replay] == [3, 3, 2]
    assert store.reads == [(0, 3), (3, 3), (6, 3)]
    assert pa.Table.from_batches(replay).column("value").to_pylist() == list(range(8))


def test_bounded_replay_counts_checkpoint_once_across_range_reads() -> None:
    """Range reads advance liveness without changing checkpoint-count semantics."""
    batch = pa.record_batch(
        [
            pa.array(range(6), type=pa.int64()),
            pa.array(range(6), type=pa.uint64()),
        ],
        names=["value", "_rowaddr"],
    )
    store = _RangeCheckpointStore(batch)
    queue = _ListQueue([(0, "ckpt_range-0-6", 6), _SEAL_SENTINEL])
    progress_events: list[dict[str, int]] = []

    def _progress(_phase: str, **deltas: int) -> None:
        progress_events.append(deltas)

    replay = list(
        _buffer_and_sort_batches(
            6,
            0,
            batch.schema,
            store,
            queue,  # type: ignore[arg-type]
            _progress=_progress,
            expect_full_coverage=True,
            max_rows_per_batch=3,
        )
    )

    assert [item.num_rows for item in replay] == [3, 3]
    # Two data reads plus the exact-boundary EOF probe must each advance the
    # liveness sequence, while the diagnostic counter remains per checkpoint.
    assert store.reads == [(0, 3), (3, 3), (6, 3)]
    assert len(progress_events) == 4  # queue item + three range reads
    assert sum(event.get("checkpoints_read", 0) for event in progress_events) == 1


def test_bounded_batches_still_produce_one_complete_fragment() -> None:
    """The recovery cap bounds input batches, not the final fragment row count."""
    batch = pa.record_batch(
        [
            pa.array(range(8), type=pa.int64()),
            pa.array(range(8), type=pa.uint64()),
        ],
        names=["value", "_rowaddr"],
    )
    store = _RangeCheckpointStore(batch)
    queue = _ListQueue([(0, "ckpt_range-0-8", 8), _SEAL_SENTINEL])
    captured_batches: list[pa.RecordBatch] = []

    class _CapturingFragmentFileWriter:
        calls = 0

        def write(
            self,
            _write_fn: Any,
            _uri: str,
            batches: Iterator[pa.RecordBatch],
            **_kwargs: Any,
        ) -> tuple[Any, int, int]:
            self.calls += 1
            captured_batches.extend(batches)
            return (
                MagicMock(path="fragment-0.lance"),
                sum(item.num_rows for item in captured_batches),
                0,
            )

    fragment_file_writer = _CapturingFragmentFileWriter()
    writer_cls = FragmentWriter.__ray_metadata__.modified_class
    with (
        patch.object(CheckpointStore, "from_uri", return_value=store),
        patch(
            "geneva.runners.ray.writer.get_fragment_file_writer",
            return_value=fragment_file_writer,
        ),
    ):
        writer = writer_cls(
            uri="memory://test",
            column_names=["value"],
            checkpoint_uri="memory:///",
            fragment_id=0,
            checkpoint_keys=queue,
            data_storage_version="2.0",
            filler_schema=batch.schema,
            field_ids=[1],
            column_indices=[0],
            num_physical_rows=8,
            num_logical_rows=8,
            max_rows_per_batch=3,
        )
        result = writer.write()

    assert fragment_file_writer.calls == 1
    assert [item.num_rows for item in captured_batches] == [3, 3, 2]
    assert pa.Table.from_batches(captured_batches).column("value").to_pylist() == list(
        range(8)
    )
    assert result.frag_id == 0
    assert result.rows_written == 8


@pytest.mark.parametrize("use_stamped_count", [False, True])
def test_bounded_replay_rejects_extra_tail_at_exact_tranche_boundary(
    use_stamped_count: bool,
) -> None:
    """Range replay must not accept only an expected prefix of a longer file."""
    batch = pa.record_batch(
        [
            pa.array(range(7), type=pa.int64()),
            pa.array(range(7), type=pa.uint64()),
        ],
        names=["value", "_rowaddr"],
    )
    expected_rows = 6
    if use_stamped_count:
        batch = stamp_checkpoint_num_rows(batch, expected_rows)
        expected_rows = -1
    store = _RangeCheckpointStore(batch)

    with pytest.raises(ValueError, match=r"holds 7 rows, expected 6"):
        list(
            _read_checkpoint_batches(
                store,
                "ckpt_range-0-6",
                expected_rows,
                max_rows_per_batch=3,
            )
        )

    assert store.reads == [(0, 3), (3, 3), (6, 3)]
    assert store.deleted == ["ckpt_range-0-6"]


def test_bounded_replay_caps_physical_gap_fill_batches() -> None:
    """Deleted-row gaps cannot expand a small recovery tranche back to OOM size."""
    sparse = pa.record_batch(
        [
            pa.array([10, 20, 30], type=pa.int64()),
            pa.array([0, 4, 8], type=pa.uint64()),
        ],
        names=["value", "_rowaddr"],
    )

    aligned = list(
        _align_batches_to_physical_layout(
            num_physical_rows=9,
            num_logical_rows=3,
            frag_id=0,
            batches=iter([sparse]),
            expect_full_coverage=True,
            max_rows_per_batch=3,
        )
    )

    assert [batch.num_rows for batch in aligned] == [1, 3, 1, 3, 1]
    assert all(batch.num_rows <= 3 for batch in aligned)
    table = pa.Table.from_batches(aligned)
    assert table.column("_rowaddr").to_pylist() == list(range(9))
    assert table.column("value").to_pylist() == [
        10,
        None,
        None,
        None,
        20,
        None,
        None,
        None,
        30,
    ]
