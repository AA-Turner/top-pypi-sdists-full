# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from collections.abc import Iterator

import pyarrow as pa

import geneva.apply as apply_mod
from geneva.apply import CheckpointingApplier
from geneva.apply.adaptive import (
    AdaptiveCheckpointSizer,
    AdaptiveReadTask,
    BatchSizeTracker,
)
from geneva.apply.applier import BatchApplier
from geneva.apply.task import (
    DEFAULT_CHECKPOINT_ROWS,
    BackfillUDFTask,
    MapTask,
    ReadTask,
)
from geneva.transformer import BACKFILL_SELECTED, udf


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


class _ControlledTimingApplier(BatchApplier):
    def __init__(self, *, udf_ms_per_batch: int = 1000) -> None:
        self.udf_ms_per_batch = udf_ms_per_batch
        self.udf_processing_time_ms = 0
        self.read_io_time_ms = 0

    def reset_run_state(self) -> None:
        self.udf_processing_time_ms = 0
        self.read_io_time_ms = 0

    def run(
        self,
        read_task: ReadTask,
        map_task: MapTask,
        error_logger: object,
    ) -> Iterator[pa.RecordBatch]:
        self.reset_run_state()
        del error_logger
        for batch in read_task.to_batches(batch_size=map_task.batch_size()):
            self.udf_processing_time_ms += self.udf_ms_per_batch
            yield map_task.apply(batch)


@udf(data_type=pa.int32(), min_checkpoint_size=2, max_checkpoint_size=3)
def _double(a: int) -> int:
    return a * 2


def test_adaptive_checkpoint_sizer_clamps_size() -> None:
    sizer = AdaptiveCheckpointSizer(max_size=100, min_size=1, target_seconds=10.0)
    assert sizer.current_size == 1

    sizer.record(duration_seconds=20.0, rows=100)
    assert sizer.current_size == 50

    sizer.record(duration_seconds=1.0, rows=100)
    assert sizer.current_size == 100

    sizer.record(duration_seconds=1000.0, rows=1)
    assert sizer.current_size == 1


def test_adaptive_read_task_honors_caller_scan_batch_size() -> None:
    """``AdaptiveReadTask`` must use ``max(batch_size, sizer.max_size)``
    for the inner Lance scan.

    A naive implementation discards the caller's kwarg and scans at
    ``self.sizer.max_size``, which for a UDF declaring only
    ``checkpoint_size=64`` (no ``max_checkpoint_size`` override)
    resolves to 64 — ignoring a caller that asked for a coarser scan.
    The bench masked this because it set
    ``GENEVA_BENCH_MAX_CHECKPOINT_SIZE``.
    """

    class _RecordingTask(ReadTask):
        def __init__(self) -> None:
            self.batch_sizes: list[int] = []

        def to_batches(
            self,
            *,
            batch_size: int = DEFAULT_CHECKPOINT_ROWS,
        ) -> Iterator[pa.RecordBatch]:
            self.batch_sizes.append(int(batch_size))
            yield pa.record_batch(
                [
                    pa.array(list(range(4))),
                    pa.array(list(range(4)), type=pa.uint64()),
                ],
                names=["a", "_rowaddr"],
            )

        def checkpoint_key(self) -> str:
            return "rec"

        def dest_frag_id(self) -> int:
            return 0

        def dest_offset(self) -> int:
            return 0

        def num_rows(self) -> int:
            return 4

        def table_uri(self) -> str:
            return "memory://rec"

    # Sizer ceiling is small (64), caller passes a much larger
    # ``batch_size``. Inner scan must see the *larger* value so the
    # scan granularity follows the caller's hint, not the sizer.
    inner = _RecordingTask()
    sizer = AdaptiveCheckpointSizer(max_size=64, min_size=1, target_seconds=10.0)
    adaptive = AdaptiveReadTask(inner, sizer=sizer, size_tracker=BatchSizeTracker())
    list(adaptive.to_batches(batch_size=4096))
    assert inner.batch_sizes == [4096], (
        f"AdaptiveReadTask discarded the caller's scan batch_size: "
        f"inner saw {inner.batch_sizes} (expected [4096])"
    )

    # Symmetric case: sizer ceiling is larger than caller's hint.
    # Inner scan should use the sizer ceiling so we don't yield
    # batches larger than the sizer is allowed to record.
    inner2 = _RecordingTask()
    sizer2 = AdaptiveCheckpointSizer(max_size=8192, min_size=1, target_seconds=10.0)
    adaptive2 = AdaptiveReadTask(inner2, sizer=sizer2, size_tracker=BatchSizeTracker())
    list(adaptive2.to_batches(batch_size=64))
    assert inner2.batch_sizes == [8192], (
        f"AdaptiveReadTask should clamp to sizer ceiling when caller's "
        f"batch_size is smaller: inner saw {inner2.batch_sizes} "
        f"(expected [8192])"
    )


def test_adaptive_read_task_slices_and_tracks_sizes() -> None:
    batch = pa.record_batch(
        [pa.array(list(range(10))), pa.array(list(range(10)), type=pa.uint64())],
        names=["a", "_rowaddr"],
    )
    task = _DummyReadTask([batch])
    sizer = AdaptiveCheckpointSizer(max_size=4, min_size=1, target_seconds=10.0)
    tracker = BatchSizeTracker()
    adaptive = AdaptiveReadTask(task, sizer=sizer, size_tracker=tracker)

    it = adaptive.to_batches(batch_size=4)
    first = next(it)
    assert first.num_rows == 1
    sizer.record(duration_seconds=1.0, rows=1)

    second = next(it)
    assert second.num_rows == 4
    sizer.record(duration_seconds=20.0, rows=4)

    third = next(it)
    assert third.num_rows == 2
    sizer.record(duration_seconds=1.0, rows=2)

    fourth = next(it)
    assert fourth.num_rows == 3

    sizes = [tracker.pop() for _ in range(4)]
    assert sizes == [1, 4, 2, 3]


def test_checkpointing_applier_adapts_batch_sizes(monkeypatch) -> None:
    map_task = BackfillUDFTask(
        udfs={"b": _double},
        override_batch_size=4,
        explicit_checkpoint_size=True,
    )

    batch = pa.record_batch(
        [
            pa.array(list(range(8))),
            pa.array([True] * 8),
            pa.array(list(range(8)), type=pa.uint64()),
        ],
        names=["a", BACKFILL_SELECTED, "_rowaddr"],
    )
    read_task = _DummyReadTask([batch])

    # Very slow wall-clock samples should not affect adaptive sizing when
    # udf_processing_time_ms is available.
    times = iter([0.0, 100.0, 100.0, 200.0, 200.0, 300.0, 300.0, 400.0, 400.0])
    monkeypatch.setattr(apply_mod.time, "monotonic", lambda: next(times))

    applier = CheckpointingApplier(
        checkpoint_uri="memory",
        map_task=map_task,
        batch_applier=_ControlledTimingApplier(udf_ms_per_batch=1000),
        batch_checkpoint_flush_interval_seconds=0,
    )
    checkpoints, direct_result, _ = applier.run(read_task)
    assert direct_result is None

    assert [checkpoint.span for checkpoint in checkpoints] == [3, 3, 2]
    assert [
        applier.checkpoint_store[checkpoint.checkpoint_key].num_rows
        for checkpoint in checkpoints
    ] == [3, 3, 2]


def test_backfill_task_overrides_adaptive_bounds() -> None:
    task = BackfillUDFTask(
        udfs={"b": _double},
        override_batch_size=4,
        min_checkpoint_size=1,
        max_checkpoint_size=4,
    )
    assert task.adaptive_checkpoint_bounds() == (1, 4)


def test_udf_default_min_checkpoint_size() -> None:
    @udf(data_type=pa.int32())
    def _identity(a: int) -> int:
        return a

    task = BackfillUDFTask(udfs={"b": _identity}, override_batch_size=4)
    min_size, _ = task.adaptive_checkpoint_bounds()
    assert min_size == 1
