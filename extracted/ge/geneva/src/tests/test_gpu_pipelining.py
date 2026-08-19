# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for the GPU-pipelining BatchApplier.

Covers ``CollocatedPipelinedApplier``, which plugs into
``CheckpointingApplier`` in place of ``SimpleApplier``. Verifies the
read + optional preprocess + compute pipeline produces identical
results to the baseline applier.
"""

from __future__ import annotations

import random
import threading
import time
import weakref
from typing import TYPE_CHECKING
from unittest.mock import patch

import pyarrow as pa
import pytest
from ray_pipeline_test_utils import (
    MockedRayWriterHarness,
    attach_started_writer_future,
    make_fragment_write_result,
    make_fragment_writer_manager,
    make_fragment_writer_session,
)
from yarl import URL

from geneva import CheckpointStore, connect, udf
from geneva.apply import CheckpointingApplier, plan_read
from geneva.apply.task import (
    DEFAULT_CHECKPOINT_ROWS,
    BackfillUDFTask,
    ReadTask,
)
from geneva.debug.logger import NoOpErrorLogger
from geneva.runners.ray.loader import CollocatedPipelinedApplier
from geneva.table import TableReference

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator
    from pathlib import Path


# --- UDF fixtures -----------------------------------------------------------


@udf(input_columns=["a"])
def double_scalar(a: int) -> int:
    return a * 2


@udf(input_columns=["a"])
def boom(a: int) -> int:
    raise RuntimeError("kaboom")


# Module-level lock guarding the class-level counters below. ``+=`` on
# a Python int is load + add + store at the bytecode level — not atomic
# across the reader threads that run preprocess() concurrently.
_COUNTER_LOCK = threading.Lock()


class _DoubleWithPreprocess:
    """Stateful UDF with a preprocess() step — mirrors the
    preprocess-overlap pipelining shape (preprocess + __call__).

    Counters are class-level so tests can read them after the run.
    Updates are guarded by ``_COUNTER_LOCK`` since ``+=`` isn't atomic
    across reader threads.
    """

    preprocess_rowcount: int = 0
    compute_rowcount: int = 0

    def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        with _COUNTER_LOCK:
            type(self).preprocess_rowcount += batch.num_rows
        precomputed = pa.array([x.as_py() * 2 for x in batch["a"]], type=pa.int64())
        return pa.RecordBatch.from_arrays(
            [*list(batch.columns), precomputed],
            names=[*list(batch.schema.names), "_pre"],
        )

    def __call__(self, a: int, _pre: int) -> int:
        with _COUNTER_LOCK:
            type(self).compute_rowcount += 1
        assert _pre == a * 2
        return _pre


double_with_preprocess = udf(
    input_columns=["a", "_pre"],
    data_type=pa.int64(),
)(_DoubleWithPreprocess)


_READ_AHEAD_FIRST_ENTERED = threading.Event()
_READ_AHEAD_RELEASE_FIRST = threading.Event()
_RANDOM_DELAY_LOCK = threading.Lock()
_RANDOM_DELAY_BY_FIRST_ROW: dict[int, float] = {}
_RANDOM_DELAY_COMPLETION_ORDER: list[int] = []


class _BlockingFirstPreprocessForReadAhead:
    """Preprocess fixture that blocks only the first input batch."""

    def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        first = int(batch["a"][0].as_py())
        if first == 0:
            _READ_AHEAD_FIRST_ENTERED.set()
            if not _READ_AHEAD_RELEASE_FIRST.wait(timeout=5.0):
                raise TimeoutError("timed out waiting to release first batch")
        precomputed = pa.array([x.as_py() * 2 for x in batch["a"]], type=pa.int64())
        return pa.RecordBatch.from_arrays(
            [*list(batch.columns), precomputed],
            names=[*list(batch.schema.names), "_pre"],
        )

    def __call__(self, a: int, _pre: int) -> int:
        assert _pre == a * 2
        return _pre


class _RandomDelayPreprocessForReadAhead:
    """Preprocess fixture with deterministic random per-batch delays."""

    def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
        first = int(batch["a"][0].as_py())
        with _RANDOM_DELAY_LOCK:
            delay_s = _RANDOM_DELAY_BY_FIRST_ROW.get(first, 0.0)
        time.sleep(delay_s)
        with _RANDOM_DELAY_LOCK:
            _RANDOM_DELAY_COMPLETION_ORDER.append(first)
        precomputed = pa.array([x.as_py() * 2 for x in batch["a"]], type=pa.int64())
        return pa.RecordBatch.from_arrays(
            [*list(batch.columns), precomputed],
            names=[*list(batch.schema.names), "_pre"],
        )

    def __call__(self, a: int, _pre: int) -> int:
        assert _pre == a * 2
        return _pre


@pytest.fixture
def tbl_ref(tmp_path: Path) -> TableReference:
    return TableReference(table_id=["tbl"], version=None, db_uri=str(tmp_path))


# --- Helpers ----------------------------------------------------------------


def _make_table(tmp_path: Path, n_rows: int = 32):  # noqa: ANN202
    db = connect(tmp_path)
    return db.create_table("tbl", pa.table({"a": list(range(n_rows))}))


def _run_applier(
    tmp_path: Path,
    tbl_ref: TableReference,
    batch_applier,
    *,
    n_rows: int = 32,
    udf_instance=double_scalar,
    col: str = "doubled",
) -> pa.RecordBatch:
    tbl = _make_table(tmp_path, n_rows=n_rows)
    plans = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=n_rows)[0])
    # Concatenate result batches from all plans in offset order so the
    # test assertions line up with the input column.
    store = CheckpointStore.from_uri(str(URL(str(tmp_path)) / "ckp"))
    applier = CheckpointingApplier(
        map_task=BackfillUDFTask(
            udfs={col: udf_instance},
            min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
            max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        ),
        checkpoint_uri=store.root,
        batch_applier=batch_applier,
        error_logger=NoOpErrorLogger(),
    )
    batches: list[pa.RecordBatch] = []
    for plan in sorted(plans, key=lambda p: p.offset):
        results, _direct, _cnt = applier.run(plan)
        batches.extend(store[r.checkpoint_key] for r in results)
    return pa.Table.from_batches(batches).combine_chunks().to_batches()[0]


# --- Collocated mode --------------------------------------------------------


def test_collocated_applier_produces_same_output_as_baseline(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    applier = CollocatedPipelinedApplier(
        num_readers=4,
        prefetch_depth=8,
        job_id="test-collocated",
    )
    batch = _run_applier(tmp_path, tbl_ref, applier)
    assert batch.schema.field("doubled").type == pa.int64()
    assert batch["doubled"].to_pylist() == [i * 2 for i in range(32)]
    assert batch["_rowaddr"].to_pylist() == list(range(32))


def test_collocated_applier_with_preprocess_fan_out(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Verifies the preprocess() hook runs and its output feeds __call__.

    Reader threads process batches out-of-order. Production backfill
    writes by ``_rowaddr`` so order doesn't matter for correctness;
    this test sorts by ``_rowaddr`` before checking values.
    """
    _DoubleWithPreprocess.preprocess_rowcount = 0
    _DoubleWithPreprocess.compute_rowcount = 0

    applier = CollocatedPipelinedApplier(
        num_readers=4,
        prefetch_depth=8,
        job_id="test-collocated-preproc",
    )
    batch = _run_applier(
        tmp_path,
        tbl_ref,
        applier,
        udf_instance=double_with_preprocess,
        col="doubled",
    )
    rows = sorted(
        zip(
            batch["_rowaddr"].to_pylist(),
            batch["doubled"].to_pylist(),
            strict=True,
        )
    )
    assert [r[0] for r in rows] == list(range(32))
    assert [r[1] for r in rows] == [i * 2 for i in range(32)]
    # Both stages saw every row. Counters are class-level and the
    # reader threads run in-process, so the driver sees the writes.
    assert _DoubleWithPreprocess.preprocess_rowcount == 32
    assert _DoubleWithPreprocess.compute_rowcount == 32


def test_collocated_applier_propagates_udf_error(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    applier = CollocatedPipelinedApplier(
        num_readers=2, prefetch_depth=4, job_id="test-collocated-err"
    )
    # CheckpointingApplier.run wraps exceptions in a RuntimeError("Error
    # running task ..."); the original UDF error is chained via __cause__.
    with pytest.raises(RuntimeError) as excinfo:
        _run_applier(tmp_path, tbl_ref, applier, udf_instance=boom)
    assert excinfo.value.__cause__ is not None
    assert "kaboom" in str(excinfo.value.__cause__)


def test_collocated_applier_metrics_populate(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    applier = CollocatedPipelinedApplier(
        num_readers=2, prefetch_depth=4, job_id="test-collocated-metrics"
    )
    _run_applier(tmp_path, tbl_ref, applier)
    assert applier.total_rows == 32
    assert applier.udf_processing_time_ms >= 0
    assert applier.read_io_time_ms >= 0


def test_collocated_applier_early_consumer_exit_does_not_hang(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Regression: aborting the generator mid-stream must not deadlock.

    Simulates a skip-threshold trip or user-cancellation by iterating
    the BatchApplier's generator once and then closing it. Preprocess
    threads blocked on an empty raw_queue must be released by the
    shutdown path; otherwise the close() call (or the surrounding
    ``with`` block) would hang indefinitely.
    """
    from geneva.apply.task import ScanTask  # noqa: PLC0415

    tbl = _make_table(tmp_path, n_rows=64)
    plans = list(plan_read(tbl.uri, tbl_ref, ["a"], batch_size=8)[0])
    assert plans, "expected at least one scan task"
    plan: ScanTask = plans[0]
    map_task = BackfillUDFTask(
        udfs={"doubled": double_with_preprocess},
        min_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
        max_checkpoint_size=DEFAULT_CHECKPOINT_ROWS,
    )

    applier = CollocatedPipelinedApplier(
        num_readers=4, prefetch_depth=2, job_id="test-collocated-early-exit"
    )
    gen = applier.run(plan, map_task, NoOpErrorLogger())
    first = next(gen)
    assert first is not None
    # Close the generator — equivalent to raising GeneratorExit on the
    # next yield, which runs the ``finally`` that drains + sentinels.
    gen.close()
    applier.shutdown()


def test_collocated_applier_yields_batches_in_input_order_under_race(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """``CollocatedPipelinedApplier`` must deliver batches to the apply
    loop in reader-emitted order, even when K preprocess threads race
    them out of completion order.

    The apply-loop's ``next_start`` running counter assumes input
    order — without it, mis-paired ``[start, end)`` ranges silently
    drop or scramble rows downstream (the deletion-test row drop and
    the adaptive-sizing partial-fill bug both shared this root cause).

    The race is deterministic: ``preprocess()`` sleeps an amount that
    *decreases* with the first row in each batch, so earlier batches
    finish later under K=4 workers. Without the ``SequenceQueue``
    reorder, the yield order would invert; with it, the apply loop
    sees batches in reader-emitted order.

    Synthetic ``_FakeReadTask`` is what makes the race reproducible:
    it emits an exact, known number of batches, so all K=4 preprocess
    workers have something to do. If the plan collapsed to a single
    batch the "stays in input order" assertion would be vacuous —
    exactly the coverage gap this regression test is meant to close.
    """
    import time as _time

    from geneva.apply.task import ReadTask as _ReadTask

    del tbl_ref  # synthetic ReadTask; no on-disk table needed
    _ = tmp_path

    class _OutOfOrderPreprocess:
        """Stateful UDF whose preprocess timing inverts with row index."""

        def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
            # batch covers rows [N, N+batch_size). Sleep proportional
            # to (max_row - first_row), so the first batch sleeps
            # longest and finishes last.
            first = int(batch["a"][0].as_py())
            _time.sleep(max(0.0, (32 - first) * 0.005))
            precomputed = pa.array([x.as_py() * 2 for x in batch["a"]], type=pa.int64())
            return pa.RecordBatch.from_arrays(
                [*list(batch.columns), precomputed],
                names=[*list(batch.schema.names), "_pre"],
            )

        def __call__(self, a: int, _pre: int) -> int:
            return _pre

    out_of_order_udf = udf(input_columns=["a", "_pre"], data_type=pa.int64())(
        _OutOfOrderPreprocess
    )

    n_batches = 4
    rows_per_batch = 8
    fake_batches: list[pa.RecordBatch] = []
    for b in range(n_batches):
        first = b * rows_per_batch
        fake_batches.append(
            pa.RecordBatch.from_arrays(
                [
                    pa.array(
                        list(range(first, first + rows_per_batch)),
                        type=pa.int64(),
                    ),
                    pa.array(
                        list(range(first, first + rows_per_batch)),
                        type=pa.int64(),
                    ),
                ],
                names=["a", "_rowaddr"],
            )
        )

    class _FakeReadTask(_ReadTask):
        def __init__(self, batches: list[pa.RecordBatch]) -> None:
            self._batches = batches

        def to_batches(
            self,
            *,
            batch_size: int = 0,
        ) -> Iterator[pa.RecordBatch]:
            del batch_size
            yield from self._batches

        def checkpoint_key(self) -> str:
            return "fake"

        def dest_frag_id(self) -> int:
            return 0

        def dest_offset(self) -> int:
            return 0

        def num_rows(self) -> int:
            return sum(b.num_rows for b in self._batches)

        def table_uri(self) -> str:
            return "memory://fake"

    applier = CollocatedPipelinedApplier(
        num_readers=4,
        prefetch_depth=8,
        job_id="test-out-of-order",
    )
    map_task = BackfillUDFTask(udfs={"doubled": out_of_order_udf})

    yielded_first_rowaddrs: list[int] = [
        int(batch["_rowaddr"][0].as_py())
        for batch in applier.run(
            _FakeReadTask(fake_batches), map_task, NoOpErrorLogger()
        )
        if "_rowaddr" in batch.schema.names and batch.num_rows > 0
    ]

    # Sanity: the test must actually drive multiple batches through the
    # SequenceQueue, otherwise the ordering assertion below is vacuous.
    # An earlier version of this test used a real Lance plan and
    # silently coalesced to a single batch.
    assert len(yielded_first_rowaddrs) == n_batches, (
        f"expected {n_batches} batches yielded, got {yielded_first_rowaddrs}"
    )

    # The SequenceQueue keeps yields in the order the reader emitted
    # batches — even though the longest preprocess sleep was on the
    # first batch and would have finished last in arrival-order land.
    assert yielded_first_rowaddrs == sorted(yielded_first_rowaddrs), (
        "CollocatedPipelinedApplier yielded batches out of reader-emitted "
        f"order: {yielded_first_rowaddrs}. The SequenceQueue reorder is "
        "supposed to restore input order even when K preprocess workers "
        "complete out of order."
    )


def test_collocated_applier_preserves_order_under_random_delay_stress(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """Random preprocess delays should not leak OOO completion order to apply."""
    from geneva.apply.task import ReadTask as _ReadTask

    del tbl_ref  # synthetic ReadTask; no on-disk table needed
    _ = tmp_path

    n_batches = 24
    rows_per_batch = 2
    first_rows = [b * rows_per_batch for b in range(n_batches)]
    fake_batches = [
        pa.RecordBatch.from_arrays(
            [
                pa.array(
                    list(range(first, first + rows_per_batch)),
                    type=pa.int64(),
                ),
                pa.array(
                    list(range(first, first + rows_per_batch)),
                    type=pa.int64(),
                ),
            ],
            names=["a", "_rowaddr"],
        )
        for first in first_rows
    ]

    class _FakeReadTask(_ReadTask):
        def __init__(self, batches: list[pa.RecordBatch]) -> None:
            self._batches = batches

        def to_batches(
            self,
            *,
            batch_size: int = 0,
        ) -> Iterator[pa.RecordBatch]:
            del batch_size
            yield from self._batches

        def checkpoint_key(self) -> str:
            return "fake"

        def dest_frag_id(self) -> int:
            return 0

        def dest_offset(self) -> int:
            return 0

        def num_rows(self) -> int:
            return sum(b.num_rows for b in self._batches)

        def table_uri(self) -> str:
            return "memory://fake"

    random_delay_udf = udf(input_columns=["a", "_pre"], data_type=pa.int64())(
        _RandomDelayPreprocessForReadAhead
    )
    map_task = BackfillUDFTask(udfs={"doubled": random_delay_udf})

    for seed in (7, 19, 31):
        rng = random.Random(seed)
        delay_ranks = list(range(n_batches))
        rng.shuffle(delay_ranks)
        delays = {
            first: rank * 0.001
            for first, rank in zip(first_rows, delay_ranks, strict=True)
        }
        # Force the first batch to be the slowest in each seeded run while
        # leaving the remaining batches randomly delayed. Later batches
        # therefore complete preprocess before row 0 and exercise the
        # SequenceQueue's out-of-order replay path.
        delays[first_rows[0]] = 0.05
        delays[first_rows[1]] = 0.0
        with _RANDOM_DELAY_LOCK:
            _RANDOM_DELAY_BY_FIRST_ROW.clear()
            _RANDOM_DELAY_BY_FIRST_ROW.update(delays)
            _RANDOM_DELAY_COMPLETION_ORDER.clear()

        applier = CollocatedPipelinedApplier(
            num_readers=6,
            prefetch_depth=6,
            job_id=f"test-random-delay-{seed}",
        )
        yielded_first_rowaddrs = [
            int(batch["_rowaddr"][0].as_py())
            for batch in applier.run(
                _FakeReadTask(fake_batches), map_task, NoOpErrorLogger()
            )
            if "_rowaddr" in batch.schema.names and batch.num_rows > 0
        ]
        with _RANDOM_DELAY_LOCK:
            completion_order = list(_RANDOM_DELAY_COMPLETION_ORDER)

        assert len(completion_order) == n_batches
        assert completion_order != sorted(completion_order), (
            "random-delay stress test did not force out-of-order preprocess "
            f"completion for seed {seed}: {completion_order}"
        )
        assert yielded_first_rowaddrs == first_rows, (
            "CollocatedPipelinedApplier leaked preprocess completion order to "
            f"the apply loop for seed {seed}: {yielded_first_rowaddrs}"
        )


def test_collocated_applier_bounds_read_ahead_when_first_preprocess_stalls(
    tmp_path: Path, tbl_ref: TableReference
) -> None:
    """A stuck early preprocess batch must backpressure upstream reads.

    ``raw_queue`` and ``processed_queue`` are individually bounded, but
    out-of-order completions used to be drained into an unbounded
    ``SequenceQueue``. That made the local queue backpressure ineffective:
    while seq=0 was stuck, seq=1..N could keep reading blob/image batches
    and pile up in the reorder buffer.
    """
    from geneva.apply.task import ReadTask as _ReadTask

    del tbl_ref  # synthetic ReadTask; no on-disk table needed
    _ = tmp_path

    class _CountingReadTask(_ReadTask):
        def __init__(self, batches: list[pa.RecordBatch]) -> None:
            self._batches = batches
            self._read_count = 0

        @property
        def read_count(self) -> int:
            return self._read_count

        def to_batches(
            self,
            *,
            batch_size: int = 0,
        ) -> Iterator[pa.RecordBatch]:
            del batch_size
            for batch in self._batches:
                self._read_count += 1
                yield batch

        def checkpoint_key(self) -> str:
            return "fake"

        def dest_frag_id(self) -> int:
            return 0

        def dest_offset(self) -> int:
            return 0

        def num_rows(self) -> int:
            return sum(b.num_rows for b in self._batches)

        def table_uri(self) -> str:
            return "memory://fake"

    def _wait_until(predicate: Callable[[], bool], timeout_s: float = 5.0) -> bool:
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline:
            if predicate():
                return True
            time.sleep(0.01)
        return False

    _READ_AHEAD_FIRST_ENTERED.clear()
    _READ_AHEAD_RELEASE_FIRST.clear()
    blocking_udf = udf(input_columns=["a", "_pre"], data_type=pa.int64())(
        _BlockingFirstPreprocessForReadAhead
    )

    n_batches = 12
    rows_per_batch = 2
    image_payload = b"x" * (32 * 1024)
    fake_batches: list[pa.RecordBatch] = []
    for b in range(n_batches):
        first = b * rows_per_batch
        values = list(range(first, first + rows_per_batch))
        fake_batches.append(
            pa.RecordBatch.from_arrays(
                [
                    pa.array(values, type=pa.int64()),
                    pa.array([image_payload] * rows_per_batch, type=pa.binary()),
                    pa.array(values, type=pa.int64()),
                ],
                names=["a", "image", "_rowaddr"],
            )
        )

    prefetch_depth = 4
    read_task = _CountingReadTask(fake_batches)
    applier = CollocatedPipelinedApplier(
        num_readers=4,
        prefetch_depth=prefetch_depth,
        job_id="test-bounded-read-ahead",
    )
    map_task = BackfillUDFTask(udfs={"doubled": blocking_udf})

    yielded_first_rowaddrs: list[int] = []
    errors: list[BaseException] = []

    def _consume() -> None:
        try:
            yielded_first_rowaddrs.extend(
                int(batch["_rowaddr"][0].as_py())
                for batch in applier.run(read_task, map_task, NoOpErrorLogger())
            )
        except BaseException as exc:  # noqa: BLE001
            errors.append(exc)

    consumer = threading.Thread(target=_consume, name="test-pipelining-consumer")
    consumer.start()
    try:
        # The batch starting at row 0 waits here; later batches preprocess
        # quickly and reach ``processed_queue`` first. That forces out-of-order
        # arrivals while seq=0 keeps the reorder buffer from draining.
        assert _wait_until(lambda: _READ_AHEAD_FIRST_ENTERED.is_set() or bool(errors))
        assert errors == []
        assert _wait_until(lambda: read_task.read_count >= prefetch_depth), (
            "test did not fill the configured read-ahead window"
        )
        time.sleep(0.25)
        assert read_task.read_count <= prefetch_depth, (
            "reader advanced past the global in-flight cap while seq=0 was "
            f"blocked: read {read_task.read_count}, cap {prefetch_depth}"
        )
    finally:
        _READ_AHEAD_RELEASE_FIRST.set()

    consumer.join(timeout=5.0)
    assert not consumer.is_alive(), "pipelined applier did not finish"
    assert errors == []
    assert yielded_first_rowaddrs == [b * rows_per_batch for b in range(n_batches)]


class _TrimReadTask(ReadTask):
    """Synthetic ReadTask yielding a fixed batch list."""

    def __init__(self, batches: list[pa.RecordBatch]) -> None:
        self._batches = batches
        self.requested_batch_sizes: list[int] = []

    def to_batches(self, *, batch_size: int = 0) -> Iterator[pa.RecordBatch]:
        self.requested_batch_sizes.append(batch_size)
        yield from self._batches

    def checkpoint_key(self) -> str:
        return "trim"

    def dest_frag_id(self) -> int:
        return 0

    def dest_offset(self) -> int:
        return 0

    def num_rows(self) -> int:
        return sum(b.num_rows for b in self._batches)

    def table_uri(self) -> str:
        return "memory://trim"


def _trim_batch(value: int) -> pa.RecordBatch:
    return pa.record_batch(
        {
            "a": pa.array([value], type=pa.int64()),
            "_rowaddr": pa.array([value], type=pa.uint64()),
        }
    )


class _WeakRefReadTask(ReadTask):
    """ReadTask that materializes batches lazily and only tracks them weakly.

    ``_TrimReadTask`` holds its batch list for the whole run, which would keep
    every input batch alive no matter what the applier does. This one lets the
    applier be the sole owner, so a weakref says exactly when the pipeline let
    go of a batch.
    """

    def __init__(self, n_batches: int) -> None:
        self._n_batches = n_batches
        self.batch_refs: list[weakref.ReferenceType[pa.RecordBatch]] = []

    def to_batches(self, *, batch_size: int = 0) -> Iterator[pa.RecordBatch]:
        del batch_size
        for value in range(self._n_batches):
            batch = _trim_batch(value)
            self.batch_refs.append(weakref.ref(batch))
            yield batch

    def checkpoint_key(self) -> str:
        return "weakref-trim"

    def dest_frag_id(self) -> int:
        return 0

    def dest_offset(self) -> int:
        return 0

    def num_rows(self) -> int:
        return self._n_batches

    def table_uri(self) -> str:
        return "memory://weakref-trim"


def _count_inputs_alive_at_trim(
    monkeypatch: pytest.MonkeyPatch,
    n_batches: int,
    consume: Callable[[Iterator[pa.RecordBatch]], None],
) -> tuple[list[int], _WeakRefReadTask]:
    """Drive the applier over ``n_batches`` via ``consume``, recording how many
    input batches were still reachable at each trim."""
    read_task = _WeakRefReadTask(n_batches)
    alive_at_trim: list[int] = []

    def _probe() -> None:
        alive_at_trim.append(sum(ref() is not None for ref in read_task.batch_refs))

    monkeypatch.setattr(
        "geneva.runners.ray.loader.release_unused_process_memory",
        _probe,
    )

    map_task = BackfillUDFTask(udfs={"doubled": double_scalar})
    applier = CollocatedPipelinedApplier(
        num_readers=1,
        prefetch_depth=1,
        job_id="test-trim-liveness",
    )
    consume(applier.run(read_task, map_task, NoOpErrorLogger()))
    return alive_at_trim, read_task


def test_pipelined_post_drain_trim_sees_no_input_batch_alive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No input batch may still be reachable when the post-drain trim fires.

    The trim used to run inside the drain frame, which still bound the last
    batch, the in-flight queue item and the reorder queue — so neither Arrow
    nor libc could hand those pages back. For a task shorter than the trim
    interval that is the only trim it gets, and adaptive slices make it worse
    by pinning a parent batch larger than the slice.
    """
    monkeypatch.setenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", "1000")

    def _drain(it: Iterator[pa.RecordBatch]) -> None:
        assert len(list(it)) == 3

    alive_at_trim, read_task = _count_inputs_alive_at_trim(
        monkeypatch, n_batches=3, consume=_drain
    )

    # Interval 1000 over 3 batches: the post-drain trim is the only one.
    assert len(read_task.batch_refs) == 3
    assert alive_at_trim == [0]


def test_pipelined_trim_sees_no_input_batch_alive_after_abandoned_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Abandoning the iterator mid-task must free the inputs before the trim.

    Cancellation retains more than the last batch: the reorder queue and the
    partially consumed queue item are live too, and closing the generator is
    the only thing that clears them.
    """
    monkeypatch.setenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", "1000")

    def _take_one(it: Iterator[pa.RecordBatch]) -> None:
        next(it)
        it.close()  # type: ignore[attr-defined]

    alive_at_trim, read_task = _count_inputs_alive_at_trim(
        monkeypatch, n_batches=8, consume=_take_one
    )

    assert read_task.batch_refs  # the reader got at least one batch out
    assert alive_at_trim == [0]


def _run_pipelined_counting_trims(
    monkeypatch: pytest.MonkeyPatch,
    n_batches: int,
) -> tuple[int, int]:
    """Run the pipelined applier over ``n_batches``; return
    ``(yielded, trim_calls)``."""
    trims = 0

    def _record_trim() -> None:
        nonlocal trims
        trims += 1

    monkeypatch.setattr(
        "geneva.runners.ray.loader.release_unused_process_memory",
        _record_trim,
    )

    read_task = _TrimReadTask([_trim_batch(i) for i in range(n_batches)])
    map_task = BackfillUDFTask(udfs={"doubled": double_scalar})
    applier = CollocatedPipelinedApplier(
        num_readers=2,
        prefetch_depth=16,
        job_id="test-memory-trim",
    )
    results = list(applier.run(read_task, map_task, NoOpErrorLogger()))
    return len(results), trims


@pytest.mark.parametrize("checkpoint_size", [1, 64, 8192])
def test_pipelined_reader_honors_requested_batch_size(checkpoint_size: int) -> None:
    """The reader requests exactly the UDF's declared ``checkpoint_size``.

    That request is what sets how many rows Lance materializes per scan,
    so the reader must forward it unmodified rather than substituting a
    size of its own.
    """

    def _double(a: int) -> int:
        return a * 2

    sized_udf = udf(input_columns=["a"], checkpoint_size=checkpoint_size)(_double)

    read_task = _TrimReadTask([_trim_batch(i) for i in range(3)])
    map_task = BackfillUDFTask(udfs={"doubled": sized_udf})
    applier = CollocatedPipelinedApplier(
        num_readers=2, prefetch_depth=16, job_id="test-batch-size"
    )

    list(applier.run(read_task, map_task, NoOpErrorLogger()))

    assert read_task.requested_batch_sizes == [checkpoint_size]


def test_pipelined_reader_trims_memory_every_eight_batches(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The reader thread must trim on the same cadence as SimpleApplier.

    Without this the GPU-pipelined path pays full glibc page retention for
    the whole scan while the simple and writer paths do not.

    9 batches at the default interval of 8: one in-loop trim, plus the
    post-drain trim every task gets.
    """
    monkeypatch.delenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", raising=False)

    yielded, trims = _run_pipelined_counting_trims(monkeypatch, n_batches=9)

    assert yielded == 9
    assert trims == 2


def test_pipelined_short_task_still_trims_on_drain(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A task shorter than the trim interval never reaches the in-loop check,
    so the post-drain trim is its only one.

    The applier is reused across ReadTasks; without this a job made of short
    tasks would strand every task's scan arenas in the actor.
    """
    monkeypatch.delenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", raising=False)

    yielded, trims = _run_pipelined_counting_trims(monkeypatch, n_batches=3)

    assert yielded == 3
    assert trims == 1


def test_pipelined_reader_memory_trim_can_be_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_APPLIER_MEMORY_TRIM_INTERVAL", "0")

    yielded, trims = _run_pipelined_counting_trims(monkeypatch, n_batches=9)

    assert yielded == 9
    assert trims == 0


def test_fragment_writer_session_defers_writer_start_until_seal() -> None:
    """Session creation and ingest only cache work; seal starts the writer."""
    from geneva.runners.ray.pipeline import FragmentWriterManager

    harness = MockedRayWriterHarness()
    with (
        harness.patch(),
        patch("geneva.runners.ray.pipeline.ray.get"),
        patch("geneva.runners.ray.pipeline.ray.wait") as wait_mock,
    ):
        sess = make_fragment_writer_session()
        assert not sess.started
        assert harness.queues == []
        assert harness.writer.options.call_count == 0

        sess.ingest_task(10, "key-10", 10)
        sess.ingest_task(0, "key-0", 10)

        assert not sess.started
        assert sess.cached_tasks == [(10, "key-10", 10), (0, "key-0", 10)]
        assert sess.enqueued == 2
        assert harness.queues == []
        assert harness.writer.options.call_count == 0
        assert sess.poll_ready() == []
        assert list(sess.drain()) == []
        wait_mock.assert_not_called()

        manager = make_fragment_writer_manager(sessions={sess.frag_id: sess})
        with patch.object(FragmentWriterManager, "_record_fragment") as record_mock:
            manager.poll_all()
        record_mock.assert_not_called()
        wait_mock.assert_not_called()
        assert not sess.started
        assert harness.queues == []
        assert harness.writer.options.call_count == 0

        sess.seal()

    assert sess.started
    assert len(harness.queues) == 1
    assert harness.writer.options.call_count == 1
    assert harness.put_args() == [(10, "key-10", 10), (0, "key-0", 10), (-1, "", 0)]
    # The deferred seal hands everything over in one batch, which is what keeps
    # the sentinel behind its checkpoints.
    assert harness.batch_calls() == [
        [(10, "key-10", 10), (0, "key-0", 10), (-1, "", 0)]
    ]


def test_fragment_writer_manager_poll_all_batches_started_sessions() -> None:
    """Multiple started writer sessions share one non-blocking ray.wait poll."""
    from geneva.runners.ray.pipeline import FragmentWriterManager

    refs = [object(), object()]
    sessions = {}
    for frag_id, ref in enumerate(refs):
        sess = make_fragment_writer_session(frag_id=frag_id)
        attach_started_writer_future(sess, ref)
        sessions[frag_id] = sess

    manager = make_fragment_writer_manager(sessions=sessions)

    with (
        patch(
            "geneva.runners.ray.pipeline.ray.wait",
            return_value=([], refs),
        ) as wait_mock,
        patch("geneva.runners.ray.pipeline.ray.get") as get_mock,
        patch.object(FragmentWriterManager, "_record_fragment") as record_mock,
    ):
        manager.poll_all()

    wait_mock.assert_called_once()
    waited_refs = wait_mock.call_args.args[0]
    assert set(waited_refs) == set(refs)
    assert wait_mock.call_args.kwargs == {"num_returns": len(refs), "timeout": 0.0}
    get_mock.assert_not_called()
    record_mock.assert_not_called()


def test_fragment_writer_manager_poll_all_records_all_ready_sessions() -> None:
    """All ready writer results returned by one poll are consumed immediately."""
    from geneva.runners.ray.pipeline import FragmentWriterManager

    refs = [object(), object()]
    sessions = {}
    results = {}
    for frag_id, ref in enumerate(refs):
        sess = make_fragment_writer_session(frag_id=frag_id)
        attach_started_writer_future(sess, ref)
        sessions[frag_id] = sess
        results[ref] = make_fragment_write_result(
            frag_id=frag_id,
            rows_written=frag_id + 10,
            buffer_sort_ms=frag_id + 20,
            align_ms=frag_id + 30,
            write_ms=frag_id + 40,
            queue_wait_ms=frag_id + 50,
            checkpoint_read_ms=frag_id + 60,
            avg_batch_num_rows=frag_id + 70,
            avg_batch_size=frag_id + 80,
        )

    manager = make_fragment_writer_manager(
        sessions=sessions,
        commit_granularity=3,
    )

    with (
        patch(
            "geneva.runners.ray.pipeline.ray.wait",
            return_value=(refs, []),
        ) as wait_mock,
        patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=lambda ref: results[ref],
        ),
        patch.object(FragmentWriterManager, "_record_fragment") as record_mock,
    ):
        manager.poll_all()

    wait_mock.assert_called_once()
    assert wait_mock.call_args.kwargs == {"num_returns": len(refs), "timeout": 0.0}
    assert [call.args[:4] for call in record_mock.call_args_list] == [
        (0, results[refs[0]].new_file, 3, 10),
        (1, results[refs[1]].new_file, 3, 11),
    ]
    assert [call.kwargs for call in record_mock.call_args_list] == [
        {
            "buffer_sort_ms": 20,
            "align_ms": 30,
            "write_ms": 40,
            "queue_wait_ms": 50,
            "checkpoint_read_ms": 60,
            "avg_batch_num_rows": 70,
            "avg_batch_size": 80,
        },
        {
            "buffer_sort_ms": 21,
            "align_ms": 31,
            "write_ms": 41,
            "queue_wait_ms": 51,
            "checkpoint_read_ms": 61,
            "avg_batch_num_rows": 71,
            "avg_batch_size": 81,
        },
    ]
    assert all(not sess.inflight for sess in sessions.values())
    assert [sess.completed for sess in sessions.values()] == [1, 1]


def test_fragment_writer_session_consume_ready_future_propagates_local_error() -> None:
    """Only Ray-side writer future failures should be converted to fragment failure."""
    fut = object()
    sess = make_fragment_writer_session()
    attach_started_writer_future(sess, fut)

    with (
        patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=ValueError("driver bug"),
        ),
        patch("geneva.runners.ray.pipeline.ray.kill"),
        pytest.raises(ValueError, match="driver bug"),
    ):
        sess.consume_ready_future(fut)

    assert not sess.failed
    assert fut in sess.inflight


def test_fragment_writer_session_consume_ready_future_marks_ray_task_error_failed() -> (
    None
):
    """Remote writer exceptions still fail the fragment without crashing the manager."""
    import ray

    fut = object()
    sess = make_fragment_writer_session()
    attach_started_writer_future(sess, fut)
    ray_error = ray.exceptions.RayTaskError(
        "FragmentWriter.write",
        "writer traceback",
        RuntimeError("writer failed"),
    )

    with (
        patch(
            "geneva.runners.ray.pipeline.ray.get",
            side_effect=ray_error,
        ),
        patch("geneva.runners.ray.pipeline.ray.kill"),
    ):
        assert sess.consume_ready_future(fut) is None

    assert sess.failed
    assert sess.failure_reason == "RayTaskError: writer traceback"
    assert sess.failure_exc is ray_error
    assert fut not in sess.inflight


def test_fragment_writer_session_restart_before_start_preserves_cached_tasks() -> None:
    """A pre-start restart keeps the lazy replay log intact for seal."""
    harness = MockedRayWriterHarness()
    with (
        harness.patch(),
        patch("geneva.runners.ray.pipeline.ray.get"),
    ):
        sess = make_fragment_writer_session()
        sess.ingest_task(0, "key-0", 10)
        sess.ingest_task(10, "key-10", 10)
        sess._restart()

        assert not sess.started
        assert sess._restart_count == 0
        assert sess.cached_tasks == [(0, "key-0", 10), (10, "key-10", 10)]
        assert harness.queue_cls is not None
        harness.queue_cls.assert_not_called()
        harness.writer.options.assert_not_called()

        sess.seal()

    assert sess.started
    assert harness.put_args() == [(0, "key-0", 10), (10, "key-10", 10), (-1, "", 0)]


def test_fragment_writer_session_replays_full_log_on_each_started_restart() -> None:
    """Each started ``_restart`` must replay every cached task.

    Regression for the ``cached_tasks, old_tasks = [], self.cached_tasks``
    bug. The old ``_restart`` extracted the replay log into a local
    variable AND emptied ``self.cached_tasks``. The first restart
    replayed correctly; the second saw an empty list, replayed
    nothing, and the new writer read only the seal sentinel. That
    triggered the gap-fill path and produced a full all-NULL output
    fragment over the placeholder.
    """
    harness = MockedRayWriterHarness()
    with (
        harness.patch(),
        patch("geneva.runners.ray.pipeline.ray.get"),
        patch("geneva.runners.ray.pipeline.ray.kill"),
    ):
        sess = make_fragment_writer_session()
        sess.ingest_task(0, "key-0", 10)
        sess.ingest_task(10, "key-10", 10)
        sess.seal()

        expected_puts = [(0, "key-0", 10), (10, "key-10", 10), (-1, "", 0)]

        assert harness.put_args(0) == expected_puts
        assert harness.batch_calls(0) == [expected_puts]

        # First restart: queue receives both items + the seal sentinel.
        sess._restart()
        assert harness.put_args(1) == expected_puts
        assert harness.batch_calls(1) == [expected_puts]
        assert sess.cached_tasks == [(0, "key-0", 10), (10, "key-10", 10)], (
            "cached_tasks must survive a restart so a second restart "
            "can also replay every item."
        )

        # Second restart on the same session: must replay the same items again.
        # Each replay is one batch, so the sentinel cannot overtake the items
        # it is replayed with.
        sess._restart()
        assert harness.put_args(2) == expected_puts
        assert harness.batch_calls(2) == [expected_puts]
        assert sess.cached_tasks == [(0, "key-0", 10), (10, "key-10", 10)]


def test_require_pipelining_for_preprocess_raises_when_disabled() -> None:
    """A preprocess() UDF used without enable_gpu_pipelining must fail
    early with a message pointing at the env var, not deep in the
    apply path with a confusing missing-column KeyError."""
    from geneva.runners.ray.pipeline import _require_pipelining_for_preprocess

    pre_udf = udf(input_columns=["a", "_pre"], data_type=pa.int64())(
        _DoubleWithPreprocess
    )()

    with pytest.raises(ValueError, match=r"enable_gpu_pipelining"):
        _require_pipelining_for_preprocess(pre_udf, enable_gpu_pipelining=False)

    # Pipelining on: no error.
    _require_pipelining_for_preprocess(pre_udf, enable_gpu_pipelining=True)

    # No preprocess: no error regardless of pipelining.
    _require_pipelining_for_preprocess(double_scalar, enable_gpu_pipelining=False)
    _require_pipelining_for_preprocess(double_scalar, enable_gpu_pipelining=True)


def test_copytable_task_has_preprocess_delegates_to_column_udfs() -> None:
    """``CopyTableTask`` (matview/UDTF refresh) must report
    ``has_preprocess()`` consistently with its column UDFs.

    Regression: ``CopyTableTask`` used to inherit ``MapTask``'s False
    default while admission read ``udf.has_preprocess()`` directly on
    the UDF object. The two layers disagreed by ``1 + K`` CPUs/actor on
    matview refresh — admission could over-reject jobs ``setup_actor``
    would have fit. Delegate to ``column_udfs`` so admission and
    runtime stay in sync.
    """
    from geneva.apply.task import CopyTableTask
    from geneva.query import ExtractedTransform

    pre_udf = udf(input_columns=["a", "_pre"], data_type=pa.int64())(
        _DoubleWithPreprocess
    )()
    schema = pa.schema([pa.field("a", pa.int64())])

    task_with_pre = CopyTableTask(
        column_udfs=[ExtractedTransform(output_index=0, output_name="x", udf=pre_udf)],
        view_name="v",
        schema=schema,
    )
    task_plain = CopyTableTask(
        column_udfs=[
            ExtractedTransform(output_index=0, output_name="x", udf=double_scalar)
        ],
        view_name="v",
        schema=schema,
    )
    task_empty = CopyTableTask(column_udfs=[], view_name="v", schema=schema)

    assert task_with_pre.has_preprocess() is True
    assert task_plain.has_preprocess() is False
    assert task_empty.has_preprocess() is False


def test_filter_to_source_columns_keeps_dotted_struct_paths() -> None:
    """Preprocess source-column filter must respect dotted struct paths.

    Regression for the ``set(schema.names)`` predicate at the
    preprocess()-pipelining filter site. ``schema.names`` only contains
    top-level field names, so a struct ``info<left, right>`` showed up
    as ``"info"``, never ``"info.left"`` — and a UDF combining
    ``preprocess()`` with ``input_columns=["info.left", "_pp_rgb"]``
    would have ``info.left`` silently stripped from the projection,
    leaving ``preprocess()`` to KeyError on the missing column.
    """
    from geneva.runners.ray.pipeline import _filter_to_source_columns

    schema = pa.schema(
        [
            pa.field("image", pa.binary()),
            pa.field(
                "info",
                pa.struct(
                    [
                        pa.field("left", pa.int64()),
                        pa.field("right", pa.int64()),
                    ]
                ),
            ),
        ]
    )

    cols = ["info.left", "_pp_rgb", "image", "info.missing"]
    kept = _filter_to_source_columns(cols, schema)

    # Real source columns survive (top-level + dotted); preprocess-
    # produced and unknown-subfield names drop.
    assert kept == ["info.left", "image"]
