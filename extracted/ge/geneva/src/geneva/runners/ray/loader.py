# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""GPU pipelining BatchApplier — read + preprocess + UDF in one actor.

Plugs into ``CheckpointingApplier`` in place of ``SimpleApplier``;
retries, checkpoints, and fragment-writer wiring are unchanged.
"""

import contextlib
import logging
import queue
import threading
import time
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import attrs
import pyarrow as pa

from geneva.apply.applier import BatchApplier
from geneva.apply.error_handling import (
    BatchStrategy,
    ErrorHandlingContext,
    get_error_handling_config,
    make_skip_budget_tracker,
)
from geneva.apply.task import MapTask, ReadTask
from geneva.debug.logger import ErrorLogger
from geneva.utils.sequence_queue import SequenceQueue

_LOG = logging.getLogger(__name__)


def _close_iterator(iterator: object) -> None:
    close = getattr(iterator, "close", None)
    if callable(close):
        close()


class _EndOfStream:
    """End-of-stream sentinel. A class (not ``object()``) so isinstance
    survives pickle round-trip through Ray plasma."""

    __slots__ = ()


_END_OF_STREAM = _EndOfStream()


@attrs.define
class _StreamError:
    """Carried through a queue to propagate reader/preprocess exceptions."""

    exc: BaseException


def _apply_one_batch(
    batch: pa.RecordBatch,
    seq: int,
    read_task: ReadTask,
    map_task: MapTask,
    job_id: str,
    error_logger: ErrorLogger,
) -> tuple[pa.RecordBatch, list[Any], int, int, int]:
    """Run the UDF on one batch. Returns
    ``(result, errors, skip_count, elapsed_ms, batch_rows)``."""
    ctx = ErrorHandlingContext.create(map_task, read_task, job_id, seq)
    strategy = BatchStrategy.from_context(ctx, map_task, error_logger)
    start = time.perf_counter()
    result_batch, error_records, skip_count = strategy.apply(batch)
    elapsed_ms = int((time.perf_counter() - start) * 1000)
    if error_records:
        error_logger.log_errors(error_records)
    batch_rows = batch.num_rows if isinstance(batch, pa.RecordBatch) else len(batch)
    return result_batch, error_records, skip_count, elapsed_ms, batch_rows


# =============================================================================
# Collocated mode — single actor, in-process threads
# =============================================================================


@attrs.define
class CollocatedPipelinedApplier(BatchApplier):
    """Three-stage in-process pipeline inside one Ray actor:

    1. Reader thread pulls from ``task.to_batches()`` into
       ``raw_queue``, tagging each batch with a monotonic ``seq_no``.
    2. K preprocess threads pop from ``raw_queue``, run
       ``udf.preprocess()``, push to ``processed_queue``. Skipped when
       the UDF has no preprocess — reader pushes straight to
       ``processed_queue``.
    3. Main thread drains ``processed_queue`` into a ``SequenceQueue``,
       pops in ``seq_no`` order, runs the UDF, yields.

    Step 3's reorder is load-bearing: without it, a slow preprocess on
    an early batch lets later batches arrive first and
    ``CheckpointingApplier``'s ``next_start`` counter mispairs
    checkpoint ``[start, end)`` ranges with batch contents (silent
    data loss — past manifestations: deletion-test row drop, adaptive-
    sizing partial-fill bug).

    ``prefetch_depth`` bounds the total number of batches read from
    upstream but not yet applied, including batches sitting in raw/
    processed queues, running preprocess, or buffered for in-order
    replay. Stage exceptions propagate through the queues via
    ``_StreamError`` and re-raise on the main thread.
    """

    num_readers: int = attrs.field(default=8)
    prefetch_depth: int = attrs.field(default=16)
    job_id: str = attrs.field(default="unknown")
    enforce_skip_threshold: bool = attrs.field(default=False)

    # Metrics exposed for CheckpointingApplier to collect.
    udf_processing_time_ms: int = attrs.field(default=0, init=False)
    read_io_time_ms: int = attrs.field(default=0, init=False)
    skip_count: int = attrs.field(default=0, init=False)
    total_rows: int = attrs.field(default=0, init=False)

    def reset_run_state(self) -> None:
        self.udf_processing_time_ms = 0
        self.read_io_time_ms = 0
        self.skip_count = 0
        self.total_rows = 0

    def run(
        self,
        read_task: ReadTask,
        map_task: MapTask,
        error_logger: ErrorLogger,
    ) -> Iterator[pa.RecordBatch]:
        self.reset_run_state()
        has_preprocess = map_task.has_preprocess()

        error_config = get_error_handling_config(map_task)
        skip_tracker = (
            make_skip_budget_tracker(error_config)
            if self.enforce_skip_threshold
            else None
        )

        batch_size = map_task.batch_size()

        raw_queue: queue.Queue = queue.Queue(maxsize=max(1, self.prefetch_depth))
        processed_queue: queue.Queue = queue.Queue(maxsize=max(1, self.prefetch_depth))

        stop_event = threading.Event()
        prefetch_slots = threading.BoundedSemaphore(max(1, self.prefetch_depth))
        # Reader-side metrics: local accumulator, published once at end.
        reader_metrics: dict[str, int] = {"read_io_time_ms": 0}
        poll_s = 0.1  # short enough for prompt shutdown, no steady-state cost

        class _PrefetchSlotGuard:
            """Own one prefetch slot until the batch is applied downstream.

            The reader reserves a slot before it materializes an upstream batch.
            If the batch is successfully enqueued, ownership transfers to the
            downstream stage and that stage must call ``release_prefetch_slot``.
            Otherwise the context manager releases the slot on exit.
            """

            def __init__(self) -> None:
                self.acquired = False
                self._transferred = False

            def __enter__(self) -> "_PrefetchSlotGuard":
                while not stop_event.is_set():
                    if prefetch_slots.acquire(timeout=poll_s):
                        self.acquired = True
                        break
                return self

            def __exit__(self, *exc_info: object) -> None:
                if self.acquired and not self._transferred:
                    release_prefetch_slot()
                    self.acquired = False

            def transfer_to_downstream(self) -> None:
                self._transferred = True

        def reserve_prefetch_slot() -> _PrefetchSlotGuard:
            return _PrefetchSlotGuard()

        def release_prefetch_slot() -> None:
            prefetch_slots.release()

        def _put_with_stop(q: queue.Queue, item: object) -> bool:
            """Blocking put that polls ``stop_event``; True on success.

            Used for every sentinel and ``_StreamError`` push: under
            backpressure ``put_nowait`` would drop the item — losing
            an EOS deadlocks the main-thread drain, losing a
            ``_StreamError`` swallows the failure silently.
            """
            while not stop_event.is_set():
                try:
                    q.put(item, timeout=poll_s)
                except queue.Full:  # noqa: PERF203
                    continue
                else:
                    return True
            return False

        # Workaround for the per-FFI-hop heap leak (GEN-473): small scan
        # batch sizes leak hundreds of MB per ScanTask. 4096 is the
        # smallest size where the lancedb wrapper releases. Big batches
        # are forwarded as-is — slicing back to batch_size would just pin
        # the parent buffer alive for the lifetime of the slowest slice.
        scan_batch_min = 4096
        scan_batch_size = max(batch_size, scan_batch_min)

        def _reader_thread() -> None:
            """Pull batches from Lance, tag each with a monotonic
            seq_no. ``read_io_time_ms`` excludes backpressure-blocked
            puts so it reflects scan work, not consumer waits."""
            dest_queue = raw_queue if has_preprocess else processed_queue
            local_read_ms = 0
            seq_no = 0
            batch_iter = None
            try:
                batch_iter = read_task.to_batches(batch_size=scan_batch_size)
                while not stop_event.is_set():
                    with reserve_prefetch_slot() as slot:
                        if not slot.acquired:
                            return
                        start_read = time.perf_counter()
                        try:
                            big_batch = next(batch_iter)
                        except StopIteration:
                            break
                        read_ms = int((time.perf_counter() - start_read) * 1000)
                        if not _put_with_stop(dest_queue, (seq_no, big_batch)):
                            return
                        slot.transfer_to_downstream()
                        local_read_ms += read_ms
                        seq_no += 1
            except BaseException as e:  # noqa: BLE001
                _LOG.warning(
                    "Reader thread error (propagating via queue): %s",
                    e,
                    exc_info=True,
                )
                _put_with_stop(dest_queue, _StreamError(e))
            finally:
                if batch_iter is not None:
                    _close_iterator(batch_iter)
                reader_metrics["read_io_time_ms"] = local_read_ms
                # One EOS per raw_queue consumer (or one to processed_queue
                # if the preprocess stage is skipped).
                if has_preprocess:
                    for _ in range(max(1, self.num_readers)):
                        _put_with_stop(raw_queue, _END_OF_STREAM)
                else:
                    _put_with_stop(processed_queue, _END_OF_STREAM)

        def _preprocess_worker() -> None:
            """Pop, preprocess, push (seq_no preserved). Emits exactly
            one ``_END_OF_STREAM`` on exit so the main thread can
            count terminators across all K workers."""
            try:
                while not stop_event.is_set():
                    try:
                        item = raw_queue.get(timeout=poll_s)
                    except queue.Empty:
                        continue
                    if isinstance(item, _EndOfStream):
                        return
                    if isinstance(item, _StreamError):
                        _put_with_stop(processed_queue, item)
                        return
                    seq_no, batch = item
                    try:
                        out = map_task.preprocess_batch(batch)
                    except BaseException as e:  # noqa: BLE001
                        release_prefetch_slot()
                        _LOG.warning(
                            "Preprocess worker error (propagating via queue): %s",
                            e,
                            exc_info=True,
                        )
                        _put_with_stop(processed_queue, _StreamError(e))
                        return
                    if not _put_with_stop(processed_queue, (seq_no, out)):
                        release_prefetch_slot()
                        return
            finally:
                _put_with_stop(processed_queue, _END_OF_STREAM)

        reader = threading.Thread(
            target=_reader_thread,
            name="geneva-collocated-reader",
            daemon=True,
        )
        reader.start()

        pool: ThreadPoolExecutor | None = None
        if has_preprocess:
            pool = ThreadPoolExecutor(
                max_workers=max(1, self.num_readers),
                thread_name_prefix="geneva-preprocess",
            )
            for _ in range(max(1, self.num_readers)):
                pool.submit(_preprocess_worker)

        # One sentinel per producer of processed_queue.
        pending_sentinels = max(1, self.num_readers) if has_preprocess else 1

        # See class docstring for why this reorder is load-bearing.
        order_queue: SequenceQueue[pa.RecordBatch] = SequenceQueue()
        try:
            seq = 0
            while pending_sentinels > 0 or not order_queue.is_empty():
                # Drain anything ready in input order before blocking.
                while True:
                    next_batch = order_queue.pop()
                    if next_batch is None:
                        break
                    try:
                        (
                            result_batch,
                            _err,
                            skip_count,
                            elapsed_ms,
                            batch_rows,
                        ) = _apply_one_batch(
                            next_batch,
                            seq,
                            read_task,
                            map_task,
                            self.job_id,
                            error_logger,
                        )
                    finally:
                        release_prefetch_slot()
                    self.udf_processing_time_ms += elapsed_ms
                    self.total_rows += batch_rows
                    self.skip_count += skip_count
                    if skip_tracker is not None and batch_rows > 0:
                        skip_tracker.record_batch(batch_rows, skip_count)
                    seq += 1
                    yield result_batch

                if pending_sentinels <= 0:
                    # All producers done and order_queue drained.
                    break

                item = processed_queue.get()
                if isinstance(item, _EndOfStream):
                    pending_sentinels -= 1
                    continue
                if isinstance(item, _StreamError):
                    stop_event.set()
                    raise item.exc

                seq_no, batch = item
                # size=1: seq numbers are dense; row counts tracked separately.
                order_queue.put(seq_no, 1, batch)
        finally:
            # stop_event unblocks any stage poll-waiting on a queue.
            # Drain to free blocked puts immediately.
            stop_event.set()
            with contextlib.suppress(queue.Empty):
                while True:
                    raw_queue.get_nowait()
            with contextlib.suppress(queue.Empty):
                while True:
                    processed_queue.get_nowait()
            if pool is not None:
                pool.shutdown(wait=True, cancel_futures=True)
            reader.join(timeout=2.0)
            if reader.is_alive():
                # Daemon thread won't block exit but we don't want to
                # silently leak a Lance scanner handle.
                _LOG.warning(
                    "Reader thread did not exit within 2 s of stop_event; "
                    "leaving as daemon"
                )
            self.read_io_time_ms += reader_metrics["read_io_time_ms"]

    def shutdown(self) -> None:
        """No-op. All thread state is owned by ``run`` and torn down in
        its ``finally`` block; this hook exists for ApplierActor
        teardown symmetry."""
