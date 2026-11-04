# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import time
from collections.abc import Iterator

import pyarrow as pa
import pytest

import geneva.apply as apply_mod
from geneva.apply import CheckpointingApplier
from geneva.apply.adaptive import (
    AdaptiveCheckpointSizer,
    AdaptiveReadTask,
    BatchSizeTracker,
)
from geneva.apply.applier import BatchApplier
from geneva.apply.simple import SimpleApplier
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


_SLOW_UDF_SECONDS_PER_ROW = 0.05


@udf(data_type=pa.int32())
def _slow_scalar(a: int) -> int:
    time.sleep(_SLOW_UDF_SECONDS_PER_ROW)
    return a * 2


@udf(data_type=pa.int32())
def _slow_record_batch(batch: pa.RecordBatch) -> pa.Array:
    time.sleep(_SLOW_UDF_SECONDS_PER_ROW * batch.num_rows)
    return pa.array([v * 2 for v in batch["a"].to_pylist()], type=pa.int32())


def test_adaptive_checkpoint_sizer_clamps_size() -> None:
    sizer = AdaptiveCheckpointSizer(
        max_size=100, min_size=1, initial_size=60, target_seconds=10.0
    )
    assert sizer.current_size == 60

    sizer.record(duration_seconds=20.0, rows=100)
    assert sizer.current_size == 50

    sizer.record(duration_seconds=1.0, rows=100)
    assert sizer.current_size == 100

    sizer.record(duration_seconds=1000.0, rows=1)
    assert sizer.current_size == 1


def test_adaptive_checkpoint_sizer_caps_growth_per_measurement(caplog) -> None:
    """One fast-looking batch may only double the size; shrinking is immediate.

    A batch whose UDF ran on few of its rows measures far faster than the next
    batch may be. Jumping straight to the maximum on that evidence can hand a
    slow UDF a batch many times its target duration.
    """
    caplog.set_level(logging.INFO, logger="geneva.apply.adaptive")
    sizer = AdaptiveCheckpointSizer(max_size=256, min_size=16, target_seconds=10.0)
    assert sizer.current_size == 16

    sizes = []
    for _ in range(5):
        rows = sizer.current_size
        sizer.record(duration_seconds=0.001, rows=rows)
        sizes.append(sizer.current_size)
    assert sizes == [32, 64, 128, 256, 256]

    sizer.record(duration_seconds=1000.0, rows=256)
    assert sizer.current_size == 16

    messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "geneva.apply.adaptive"
    ]
    assert "clamped_by=growth" in messages[0]
    assert "clamped_by=max" in messages[3]


def test_unconfigured_backfill_sizer_starts_above_floor() -> None:
    """An unconfigured UDF must not start in the one-row absorbing state."""

    @udf(data_type=pa.int32())
    def _identity(a: int) -> int:
        return a

    task = BackfillUDFTask(udfs={"b": _identity})
    applier = CheckpointingApplier(checkpoint_uri="memory", map_task=task)

    sizer = applier._get_or_create_sizer()

    assert sizer.current_size == min(sizer.min_size + 1, sizer.max_size)
    assert 1 < sizer.current_size <= sizer.max_size


def test_slow_udf_periodically_probes_back_to_initial_size() -> None:
    """A 30 s/row UDF must escape the floor without probing past its seed."""

    initial_size = 4
    sizer = AdaptiveCheckpointSizer(
        max_size=9,
        min_size=1,
        initial_size=initial_size,
        target_seconds=10.0,
    )

    def record_slow_batch() -> None:
        rows = sizer.current_size
        sizer.record(duration_seconds=30.0 * rows, rows=rows)

    def wait_for_probe() -> int:
        for _ in range(16):
            record_slow_batch()
            if sizer.current_size > sizer.min_size:
                return sizer.current_size
        raise AssertionError("slow UDF remained pinned at one row after 16 samples")

    # The first slow batch collapses from the configured seed to the floor.
    record_slow_batch()
    assert sizer.current_size == 1

    # Failed probes return to the floor, but the next probe keeps advancing
    # toward the effective initial seed instead of restarting at two rows.
    probes = [wait_for_probe()]
    while probes[-1] < initial_size:
        record_slow_batch()
        assert sizer.current_size == 1
        probes.append(wait_for_probe())

    assert probes == [2, 3, initial_size]
    assert all(sizer.min_size < size <= initial_size for size in probes)
    assert all(size <= sizer.max_size for size in probes)


def test_invalid_measurements_do_not_advance_floor_probe() -> None:
    sizer = AdaptiveCheckpointSizer(
        max_size=4,
        min_size=1,
        initial_size=2,
        target_seconds=10.0,
    )

    for _ in range(15):
        sizer.record(duration_seconds=30.0, rows=1)
    assert sizer.current_size == 1

    for duration in (float("nan"), float("inf"), 0.0, -1.0):
        sizer.record(duration_seconds=duration, rows=1)
        assert sizer.current_size == 1
    sizer.record(duration_seconds=30.0, rows=0)
    sizer.record(duration_seconds=30.0, rows=-1)
    assert sizer.current_size == 1

    sizer.record(duration_seconds=30.0, rows=1)
    assert sizer.current_size == 2


def test_exact_floor_measurements_trigger_probe_on_sixteenth_sample() -> None:
    sizer = AdaptiveCheckpointSizer(
        max_size=4,
        min_size=1,
        initial_size=2,
        target_seconds=10.0,
    )

    for _ in range(15):
        sizer.record(duration_seconds=10.0, rows=1)
    assert sizer.current_size == 1

    sizer.record(duration_seconds=10.0, rows=1)
    assert sizer.current_size == 2


def test_fixed_range_never_probes_or_logs(caplog) -> None:
    caplog.set_level(logging.INFO, logger="geneva.apply.adaptive")
    sizer = AdaptiveCheckpointSizer(
        max_size=3,
        min_size=3,
        initial_size=3,
        target_seconds=10.0,
    )

    for _ in range(32):
        sizer.record(duration_seconds=30.0, rows=1)

    assert sizer.current_size == 3
    assert not [
        record for record in caplog.records if record.name == "geneva.apply.adaptive"
    ]


def test_explicit_initial_size_is_authoritative_and_clamped() -> None:
    within_bounds = AdaptiveCheckpointSizer(max_size=5, min_size=1, initial_size=3)
    above_max = AdaptiveCheckpointSizer(max_size=5, min_size=1, initial_size=9)
    below_min = AdaptiveCheckpointSizer(max_size=5, min_size=1, initial_size=0)

    assert within_bounds.current_size == 3
    assert above_max.current_size == 5
    assert below_min.current_size == 1


def test_floor_probe_can_exceed_explicit_initial_at_minimum() -> None:
    sizer = AdaptiveCheckpointSizer(
        max_size=5,
        min_size=1,
        initial_size=1,
        target_seconds=10.0,
    )
    assert sizer.current_size == 1

    probes = []
    for _ in range(48):
        rows = sizer.current_size
        sizer.record(duration_seconds=30.0 * rows, rows=rows)
        if sizer.current_size > sizer.min_size:
            probes.append(sizer.current_size)

    assert probes == [2, 2, 2]


def test_adaptive_checkpoint_size_transitions_are_logged(
    caplog,
) -> None:
    """Every actual size transition exposes its inputs and decision at INFO."""

    caplog.set_level(logging.INFO, logger="geneva.apply.adaptive")
    sizer = AdaptiveCheckpointSizer(
        max_size=4,
        min_size=1,
        initial_size=2,
        target_seconds=10.0,
    )

    # Exercise all measurement clamp outcomes.
    sizer.record(duration_seconds=1.0, rows=2)  # 2 -> 4 (max)
    sizer.record(duration_seconds=20.0, rows=4)  # 4 -> 2 (none)
    sizer.record(duration_seconds=100.0, rows=2)  # 2 -> 1 (min)
    # The transition to the floor is the first of 16 consecutive floor-clamped
    # measurements. Fifteen more must emit exactly one floor probe transition.
    for _ in range(15):
        sizer.record(duration_seconds=30.0, rows=1)

    records = [
        record
        for record in caplog.records
        if record.name == "geneva.apply.adaptive" and record.levelno == logging.INFO
    ]
    assert len(records) == 4

    expected = [
        (2, 1.0, 2, 4, "max", "measurement"),
        (4, 20.0, 4, 2, "none", "measurement"),
        (2, 100.0, 2, 1, "min", "measurement"),
        (1, 30.0, 1, 2, "min", "floor_probe"),
    ]
    for record, (rows, duration, old_size, new_size, clamp, reason) in zip(
        records, expected, strict=True
    ):
        message = record.getMessage()
        assert f"rows={rows}" in message
        assert "duration_seconds=" in message
        assert str(duration) in message
        assert f"old_size={old_size}" in message
        assert f"new_size={new_size}" in message
        assert f"clamped_by={clamp}" in message
        assert f"reason={reason}" in message


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
    # Measures 10 rows' worth; growth is limited to double the current size.
    sizer.record(duration_seconds=1.0, rows=1)

    second = next(it)
    assert second.num_rows == 2
    sizer.record(duration_seconds=1.0, rows=2)

    third = next(it)
    assert third.num_rows == 4
    sizer.record(duration_seconds=20.0, rows=4)

    fourth = next(it)
    assert fourth.num_rows == 2

    sizes = [tracker.pop() for _ in range(4)]
    assert sizes == [1, 2, 4, 2]


def _sparse_input(as_rows: bool) -> pa.RecordBatch | list[dict]:
    """12 rows with every fourth selected (rows 0, 4 and 8)."""
    selected = [True, False, False, False] * 3
    if as_rows:
        return [
            {"a": i, BACKFILL_SELECTED: sel, "_rowaddr": i}
            for i, sel in enumerate(selected)
        ]
    return pa.record_batch(
        [
            pa.array(range(12)),
            pa.array(selected),
            pa.array(range(12), type=pa.uint64()),
        ],
        names=["a", BACKFILL_SELECTED, "_rowaddr"],
    )


@pytest.mark.parametrize(
    ("max_size", "expected"),
    [(8, [5, 7]), (4, [4, 4, 4])],
    ids=["by_selected_rows", "capped_by_max_size"],
)
def test_adaptive_read_task_slices_by_selected_rows(
    max_size: int, expected: list[int]
) -> None:
    """A slice holds ``current_size`` selected rows, within ``max_size`` rows."""
    sizer = AdaptiveCheckpointSizer(max_size=max_size, min_size=2, initial_size=2)
    tracker = BatchSizeTracker()
    adaptive = AdaptiveReadTask(
        _DummyReadTask([_sparse_input(as_rows=False)]),  # type: ignore[list-item]
        sizer=sizer,
        size_tracker=tracker,
    )

    slices = list(adaptive.to_batches(batch_size=max_size))

    assert [len(s) for s in slices] == expected
    assert [tracker.pop() for _ in slices] == expected


def test_adaptive_read_task_cuts_list_batches_by_total_rows() -> None:
    """List-of-dict batches reach the UDF unfiltered, so selected rows don't
    stretch their slices."""
    sizer = AdaptiveCheckpointSizer(max_size=8, min_size=2, initial_size=2)
    adaptive = AdaptiveReadTask(
        _DummyReadTask([_sparse_input(as_rows=True)]),  # type: ignore[list-item]
        sizer=sizer,
    )

    assert [len(s) for s in adaptive.to_batches(batch_size=8)] == [2] * 6


def test_adaptive_read_task_treats_null_selection_as_unselected() -> None:
    batch = pa.record_batch(
        [
            pa.array(range(4)),
            pa.array([True, None, True, None], type=pa.bool_()),
            pa.array(range(4), type=pa.uint64()),
        ],
        names=["a", BACKFILL_SELECTED, "_rowaddr"],
    )
    sizer = AdaptiveCheckpointSizer(max_size=4, min_size=2, initial_size=2)
    adaptive = AdaptiveReadTask(_DummyReadTask([batch]), sizer=sizer)

    assert [s.num_rows for s in adaptive.to_batches(batch_size=4)] == [3, 1]


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


@pytest.mark.parametrize(
    "slow_udf", [_slow_scalar, _slow_record_batch], ids=["scalar", "record_batch"]
)
def test_unselected_slice_does_not_resize_next_slice(monkeypatch, slow_udf) -> None:
    """A slice the UDF never ran on must not size the next slice.

    The UDF does no work on a slice with no selected rows, so its measured time
    is ~0. Recording it once sized the next slice at max_checkpoint_size, which
    for a slow UDF on fully selected rows means a long run with no checkpoint.
    """
    # Dense 2-row slices take ~0.1 s of UDF time, so this target sizes them at
    # the 2-row floor.
    monkeypatch.setattr(apply_mod, "DEFAULT_CHECKPOINT_INTERVAL_SECONDS", 0.1)
    map_task = BackfillUDFTask(
        udfs={"b": slow_udf},
        override_batch_size=2,
        explicit_checkpoint_size=True,
        min_checkpoint_size=2,
        max_checkpoint_size=8,
    )

    selected = [True, True, False, False] + [True] * 8
    batch = pa.record_batch(
        [
            pa.array(range(len(selected)), type=pa.int64()),
            pa.array(selected),
            pa.array(range(len(selected)), type=pa.uint64()),
        ],
        names=["a", BACKFILL_SELECTED, "_rowaddr"],
    )

    applier = CheckpointingApplier(
        checkpoint_uri="memory",
        map_task=map_task,
        batch_applier=SimpleApplier(),
        batch_checkpoint_flush_interval_seconds=0,
    )
    checkpoints, direct_result, udf_rows = applier.run(_DummyReadTask([batch]))

    assert direct_result is None
    assert udf_rows == sum(selected)
    # The two unselected rows ride along with the next two selected ones; no
    # dense slice reaches the 8-row maximum.
    assert [checkpoint.udf_rows for checkpoint in checkpoints] == [2] * 5
    assert [checkpoint.span for checkpoint in checkpoints] == [2, 4, 2, 2, 2]


@pytest.mark.parametrize(
    "slow_udf", [_slow_scalar, _slow_record_batch], ids=["scalar", "record_batch"]
)
def test_sparse_slices_do_not_grow_the_next_dense_slice(monkeypatch, slow_udf) -> None:
    """Slices with few selected rows must not size a dense slice past the target.

    The UDF runs only on selected rows, so a sparse slice finishes fast. Sizing
    by all of its rows grew the size over a few sparse slices, and the dense
    slice after them ran several times the target with no checkpoint.
    """
    # 2 selected rows take ~0.1 s of UDF time, so this target allows 2 per slice.
    monkeypatch.setattr(apply_mod, "DEFAULT_CHECKPOINT_INTERVAL_SECONDS", 0.1)
    map_task = BackfillUDFTask(
        udfs={"b": slow_udf},
        override_batch_size=2,
        explicit_checkpoint_size=True,
        min_checkpoint_size=2,
        max_checkpoint_size=8,
    )

    selected = [True, False, False, False] * 4 + [True] * 8
    batch = pa.record_batch(
        [
            pa.array(range(len(selected)), type=pa.int64()),
            pa.array(selected),
            pa.array(range(len(selected)), type=pa.uint64()),
        ],
        names=["a", BACKFILL_SELECTED, "_rowaddr"],
    )

    applier = CheckpointingApplier(
        checkpoint_uri="memory",
        map_task=map_task,
        batch_applier=SimpleApplier(),
        batch_checkpoint_flush_interval_seconds=0,
    )
    checkpoints, direct_result, udf_rows = applier.run(_DummyReadTask([batch]))

    assert direct_result is None
    assert udf_rows == sum(selected)
    # Every slice holds the 2 selected rows the target allows; unselected rows
    # ride along, up to max_checkpoint_size rows in total.
    assert [checkpoint.udf_rows for checkpoint in checkpoints] == [2] * 6
    assert [checkpoint.span for checkpoint in checkpoints] == [5, 8, 5, 2, 2, 2]


def test_table_backfill_exercises_adaptive_checkpoint_sizes(
    db, local_ray_context
) -> None:
    """A real backfill with unequal bounds must use more than one batch size."""

    del local_ray_context

    @udf(data_type=pa.int32(), num_cpus=1)
    def _report_batch_size(batch: pa.RecordBatch) -> pa.Array:
        return pa.array([batch.num_rows] * batch.num_rows, type=pa.int32())

    table = db.create_table(
        "adaptive_checkpoint_sizes",
        pa.table({"a": pa.array(range(24), type=pa.int32())}),
    )
    table.add_columns({"observed_batch_size": _report_batch_size})

    table.backfill(
        "observed_batch_size",
        concurrency=1,
        checkpoint_size=4,
        min_checkpoint_size=2,
        max_checkpoint_size=8,
        task_size=24,
        batch_checkpoint_flush_interval_seconds=0,
    )

    table.checkout_latest()
    observed = table.to_arrow().column("observed_batch_size").to_pylist()
    assert observed[:4] == [4] * 4
    assert 8 in observed
    assert all(size in {4, 8} for size in observed)


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
