# ruff: noqa: PERF203
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# multi-process applier

import io
import logging
import os
import time
from collections.abc import Iterator
from typing import Any, Literal

import attrs
import multiprocess
import pyarrow as pa

import geneva.cloudpickle as cloudpickle
from geneva.apply.applier import BatchApplier
from geneva.apply.error_handling import (
    BatchStrategy,
    ErrorHandlingContext,
    get_error_handling_config,
    make_skip_budget_tracker,
)
from geneva.apply.memory import (
    BatchTrimCounter,
    get_applier_memory_trim_interval,
)
from geneva.apply.task import MapTask, ReadTask
from geneva.apply.utils import _iter_with_next_duration
from geneva.debug.logger import ErrorLogger
from geneva.errors import FatalWorkerCrashError

_LOG = logging.getLogger(__name__)

# --- Dead-worker detection -------------------------------------------------
#
# ``multiprocess.Pool`` silently reaps and replaces a worker that dies
# mid-task, and the dead task's future never completes (bpo-22393), so an
# unbounded wait on it wedges the applier forever. The stall timeout is what
# bounds it: results are consumed strictly FIFO, so a head future still
# unretired after it means the applier has stopped making progress, and
# ``_await_head_ready`` escalates.
#
# Note the narrowness of that. ``_await_head_ready`` waits only on ``futs[0]``
# and ``last_progress`` advances only when a head is consumed, so the bound
# shows that no *head* was retired -- not that the pool produced nothing.
# Younger futures may well have completed behind an orphaned head. What
# follows for calibration: the timeout has to clear the longest healthy single
# batch, not the longest gap between completions. Set under that, it condemns
# a slow-but-fine head, which the policy below then bisects and null-fills.
#
# It is deliberately the *only* signal. Two faster ones have been tried, and
# both mistook healthy work for a death:
#
#  - Completion order (#869). ``apply_async`` hands tasks out in order but
#    they finish in whatever order the work takes, so with several workers a
#    younger batch completing first is routine on a healthy pool and says
#    nothing about liveness (GEN-857).
#  - Pool membership. A PID missing from the private ``_pool`` list does prove
#    a worker died, but not *which* task it held -- or that it held one at
#    all, since a worker can be killed while idle or just after publishing a
#    result. Nothing in the pool records task-to-worker ownership, and the
#    parent only samples membership once a head is already slow, so the loss
#    cannot be tied to the batch being waited on. Any bound built on it ends
#    up charging a healthy slow batch for an unrelated death.
#
# They failed the same way, so the bar is worth stating: a false positive is
# not a retry. Absent a user policy that matches it, ``FatalWorkerCrashError``
# reaches ``_default_worker_loss_policy`` (``runners/ray/pipeline.py``), which
# resolves it to ``Skip``: the task is bisected and rows that keep failing are
# left null while the job reports DONE. See
# ``test_multiprocess_child_crash_isolates_only_failed_row``. Condemning a
# healthy batch therefore costs data, so a signal has to show the pool
# *cannot* produce it -- slowness is not enough.
#
# A fast path needs the worker to record which task it picked up before
# running it (GEN-857 follow-up); a crash-aware executor
# (``ProcessPoolExecutor`` raises ``BrokenProcessPool`` here) is the other
# option noted in #869.

# Cadence for re-checking the stall bound while blocked on a result. Not a
# latency floor: ``_await_head_ready`` blocks on the future's own event, so a
# result is picked up as soon as it lands.
_POOL_POLL_INTERVAL_S = 1.0

# Bound after which a head future that has not been retired is treated as
# orphaned. Any override has to stay above the longest healthy batch, since a
# head slower than this is condemned. Set with
# ``GENEVA_APPLIER_WORKER_STALL_TIMEOUT_S``.
_DEFAULT_WORKER_STALL_TIMEOUT_S = 600.0
_WORKER_STALL_TIMEOUT_ENV = "GENEVA_APPLIER_WORKER_STALL_TIMEOUT_S"

# Metadata keys used to preserve PyArrow extension type identity through IPC
# serialization.  Extension types (e.g. lance.blob.v2) are stripped to their
# storage representation before serialization and restored after deserialization.
_EXT_TYPE_NAME_KEY = b"__ext_type_name"
_EXT_TYPE_SERIALIZED_KEY = b"__ext_type_serialized"

# Prefix marker for cloudpickle-serialized list[dict] batches.
# Blob-encoded columns cause LanceDB to yield list[dict] instead of
# pa.RecordBatch.  These cannot go through Arrow IPC, so we use
# cloudpickle with this marker to distinguish the format.
_LIST_DICT_MARKER = b"\x00GLIST\x00"

# Cache for resolved extension types so we only do the lazy import once.
_KNOWN_EXT_TYPES: dict[str, pa.ExtensionType] = {}

# Per-process batch counter driving the periodic allocator trim. Module-level
# rather than applier-owned because the applier instance never reaches a pool
# worker — workers receive only a pickled MapTask and a batch buffer — so each
# process keeps its own copy.
_WORKER_TRIM_COUNTER = BatchTrimCounter()


def _worker_trim_memory() -> None:
    """Release allocator arenas in this worker every N batches.

    Called on entry, when the previous batch's Arrow and UDF buffers have
    already been dropped but glibc may still be holding their pages.
    """
    _WORKER_TRIM_COUNTER.record_batch(get_applier_memory_trim_interval())


def _get_extension_type(
    ext_name: str,
    storage_type: pa.DataType,
    serialized: bytes,
) -> pa.ExtensionType:
    """Look up (or lazily import) a PyArrow extension type by name.

    PyArrow extension types (e.g. ``lance.blob.v2``) are not preserved
    through IPC serialization.  This function resolves the original type
    class from the ``ext_name`` stored in field metadata so that
    [`_restore_extension_types`][_restore_extension_types] can re-wrap storage arrays.

    Currently supported extension types:

    - ``lance.blob.*`` — Lance ``BlobType`` (backed by a struct storage
      type with ``data`` and ``offsets`` fields).  Registered by importing
      ``lance.blob``.

    If you hit the ``ValueError`` below, a new extension type has appeared
    that this function doesn't know about yet.  To fix it:

    1. Add an ``elif ext_name.startswith(...)`` branch that imports the
       module registering the type.
    2. Call ``TypeClass.__arrow_ext_deserialize__(storage_type, serialized)``
       to reconstruct it.
    3. Add a corresponding test in ``test_apply.py``.

    Parameters
    ----------
        ext_name
            The ``extension_name`` string stored in field metadata
            (e.g. ``"lance.blob.v2"``).
        storage_type
            The Arrow storage type of the column after the
            extension wrapper was stripped.
        serialized
            The bytes produced by
            ``ExtensionType.__arrow_ext_serialize__()`` at strip time.

    Raises
    ------
        ValueError
            If *ext_name* doesn't match any known extension type
            family.
    """
    if ext_name in _KNOWN_EXT_TYPES:
        return _KNOWN_EXT_TYPES[ext_name]

    # Trigger registration for known extension type families.  Importing the
    # module has the side-effect of calling pa.register_extension_type().
    # TODO: add branches here when Lance or other libraries introduce new
    #       extension types that need to survive IPC (e.g. lance.geometry).
    if ext_name.startswith("lance.blob"):
        from lance.blob import BlobType

        ext_type = BlobType.__arrow_ext_deserialize__(storage_type, serialized)
    else:
        raise ValueError(
            f"Unknown Arrow extension type: {ext_name!r}. "
            "Cannot restore after IPC deserialization.  Ensure the library "
            "that defines this type is imported before deserialization."
        )

    _KNOWN_EXT_TYPES[ext_name] = ext_type
    return ext_type


def _strip_extension_types(batch: pa.RecordBatch) -> pa.RecordBatch:
    """Replace extension-typed columns with their storage representation.

    Extension type identity is saved in field metadata so that
    [`_restore_extension_types`][_restore_extension_types] can re-wrap them
    after deserialization. Returns *batch* unchanged when no extension columns
    are present.
    """
    ext_indices = [
        i
        for i, field in enumerate(batch.schema)
        if isinstance(field.type, pa.ExtensionType)
    ]
    if not ext_indices:
        return batch

    columns = list(batch.columns)
    fields = list(batch.schema)

    for i in ext_indices:
        field = fields[i]
        ext_type = field.type
        meta = dict(field.metadata or {})
        # Stash the extension type identity so _restore_extension_types can
        # reconstruct it after IPC deserialization.
        #   _EXT_TYPE_NAME_KEY: UTF-8 encoded extension name, e.g. b"lance.blob.v2".
        #     Used by _get_extension_type to look up the correct type class.
        #   _EXT_TYPE_SERIALIZED_KEY: opaque bytes from __arrow_ext_serialize__().
        #     Passed to TypeClass.__arrow_ext_deserialize__() to reconstruct
        #     any type-specific parameters (currently empty for BlobType).
        meta[_EXT_TYPE_NAME_KEY] = ext_type.extension_name.encode()
        meta[_EXT_TYPE_SERIALIZED_KEY] = ext_type.__arrow_ext_serialize__()
        fields[i] = pa.field(
            field.name, ext_type.storage_type, nullable=field.nullable, metadata=meta
        )
        columns[i] = columns[i].storage  # type: ignore[attr-defined]

    return pa.RecordBatch.from_arrays(columns, schema=pa.schema(fields))


def _restore_extension_types(batch: pa.RecordBatch) -> pa.RecordBatch:
    """Re-wrap storage columns whose metadata marks them as extension types.

    Reverses the transformation applied by
    [`_strip_extension_types`][_strip_extension_types]. Returns *batch*
    unchanged when no marked columns are present.
    """
    ext_indices = [
        i
        for i, field in enumerate(batch.schema)
        if field.metadata and _EXT_TYPE_NAME_KEY in field.metadata
    ]
    if not ext_indices:
        return batch

    columns = list(batch.columns)
    fields = list(batch.schema)

    for i in ext_indices:
        field = fields[i]
        meta: dict[bytes, bytes] = dict(field.metadata)  # type: ignore[arg-type]
        ext_name = meta.pop(_EXT_TYPE_NAME_KEY).decode()
        ext_serialized = meta.pop(_EXT_TYPE_SERIALIZED_KEY)

        ext_type = _get_extension_type(ext_name, field.type, ext_serialized)
        columns[i] = pa.ExtensionArray.from_storage(ext_type, columns[i])
        fields[i] = pa.field(
            field.name, ext_type, nullable=field.nullable, metadata=meta or None
        )

    return pa.RecordBatch.from_arrays(columns, schema=pa.schema(fields))


def _buf_to_batch(
    data: bytes | memoryview,
    *,
    coalesce: bool = False,
) -> list[pa.RecordBatch] | pa.RecordBatch:
    """
    Convert a buffer to a record batch (or list[dict] for blob batches).

    Extension types that were stripped by [`_batch_to_buf`][_batch_to_buf] are restored
    automatically using the metadata markers left in the schema.

    Buffers that start with `_LIST_DICT_MARKER` are cloudpickle-
    serialized ``list[dict]`` blobs (see [`_batch_to_buf`][_batch_to_buf]).
    """
    raw = bytes(data) if isinstance(data, memoryview) else data
    if raw.startswith(_LIST_DICT_MARKER):
        batch_list: list[dict[str, Any]] = cloudpickle.loads(
            raw[len(_LIST_DICT_MARKER) :]
        )
        return batch_list if coalesce else [batch_list]  # type: ignore[return-value]

    buf = io.BytesIO(data)
    with pa.ipc.open_stream(buf) as f:
        t = f.read_all()
    if not coalesce:
        return [_restore_extension_types(b) for b in t.to_batches()]
    batches = t.combine_chunks().to_batches()
    if not batches:
        return pa.RecordBatch.from_pylist([], schema=t.schema)
    return _restore_extension_types(batches[0])


def _batch_to_buf(
    batch: pa.RecordBatch | list[dict[str, Any]],
) -> bytes:
    """
    Convert a record batch (or blob list[dict]) to a buffer.

    PyArrow extension types (e.g. Lance ``BlobType``) are replaced with their
    storage representation before IPC serialization so that they survive the
    round-trip to child processes.  Metadata markers are added so that
    [`_buf_to_batch`][_buf_to_batch] can restore them.

    Blob-encoded columns cause LanceDB to yield ``list[dict]`` instead of
    ``pa.RecordBatch``.  These are serialized via cloudpickle with a
    `_LIST_DICT_MARKER` prefix so [`_buf_to_batch`][_buf_to_batch] can
    distinguish the format.
    """
    if isinstance(batch, list):
        return _LIST_DICT_MARKER + cloudpickle.dumps(batch)

    batch = _strip_extension_types(batch)
    buf = io.BytesIO()
    with pa.ipc.new_stream(buf, schema=batch.schema) as f:
        f.write_batch(batch)
    buf.seek(0)
    return buf.getvalue()


def _picklable_worker_error(exc: Exception) -> RuntimeError:
    """Convert a worker exception into a picklable RuntimeError.

    Multiprocess pool workers must return picklable results.  When the
    original exception carries unpicklable objects in its traceback (e.g.
    native Azure SDK handles, Lance FFI objects), the pool raises a
    ``MaybeEncodingError`` that hides the real failure.  This helper
    preserves the full exception chain as a plain string.
    """
    parts: list[str] = []
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        parts.append(f"{type(current).__module__}.{type(current).__name__}: {current}")
        current = current.__cause__ or current.__context__
    return RuntimeError(" | caused by ".join(parts))


def _apply_with_stream_buf(
    apply: bytes,
    buf: bytes,
) -> bytes:
    """
    Apply a function to a record batch using a stream buffer.
    """
    _worker_trim_memory()
    try:
        func = cloudpickle.loads(apply)
        out_buf = io.BytesIO()
        out_batches = [func(batch) for batch in _buf_to_batch(buf)]
        # Note: output batches are UDF results (standard Arrow types like int64,
        # string, etc.) so they don't need _strip_extension_types before IPC.
        with pa.ipc.new_stream(out_buf, schema=out_batches[0].schema) as f:
            for batch in out_batches:
                f.write_batch(batch)

        return out_buf.getvalue()
    except Exception as e:
        raise _picklable_worker_error(e) from None


@attrs.define
class MultiProcessBatchApplier(BatchApplier):
    """
    A multi-process applier that applies a function to each element in the batch.
    """

    num_processes: int = attrs.field(validator=attrs.validators.ge(1))

    method: Literal["fork", "spawn"] = attrs.field(default="fork")

    job_id: str = attrs.field(default="unknown")
    enforce_skip_threshold: bool = attrs.field(default=True)
    udf_processing_time_ms: int = attrs.field(default=0, init=False)
    read_io_time_ms: int = attrs.field(default=0, init=False)
    skip_count: int = attrs.field(default=0, init=False)
    total_rows: int = attrs.field(default=0, init=False)
    # The parent still churns scan batches and IPC buffers even though the UDF
    # runs in the pool; workers trim themselves in _worker_trim_memory. Spans
    # ReadTasks by design, so it is not cleared by reset_run_state — the parent
    # is the only process here that outlives a task, since pool workers are
    # recreated per run and return their arenas to the OS on exit.
    trim_counter: BatchTrimCounter = attrs.field(factory=BatchTrimCounter, init=False)

    def reset_run_state(self) -> None:
        self.udf_processing_time_ms = 0
        self.read_io_time_ms = 0
        self.skip_count = 0
        self.total_rows = 0

    @staticmethod
    def _worker_apply(
        map_task_bytes: bytes,
        buf: bytes,
        error_config_bytes: bytes | None,
        job_id: str,
        task_context: dict,
        seq: int,
        udf_name: str,
        udf_version: str,
        input_columns: list[str] | None,
        output_columns: list[str] | None,
    ) -> tuple[bytes, bytes, int]:
        """Worker process: Apply strategy to batch with error handling

        This function runs in worker subprocesses. It deserializes the task,
        reconstructs the error handling strategy, and applies it to batches.

        Security Note:
            cloudpickle.loads() is safe here because this worker function only
            runs in subprocesses created by multiprocess.Pool from the same
            parent process. The serialized data originates from trusted code in
            the parent process, not from external/untrusted sources.

        Parameters
        ----------
            map_task_bytes
                Pickled MapTask
            buf
                Serialized RecordBatch(es)
            error_config_bytes
                Pickled ErrorHandlingConfig (or None)
            job_id
                Job identifier
            task_context
                Table context (uri, version, fragment_id)
            seq
                Batch sequence number
            udf_name
                UDF name for logging
            udf_version
                UDF version for logging
            input_columns
                Canonical source field paths for audit records
            output_columns
                User-visible output field paths for audit records

        Returns
        -------
            tuple[bytes, bytes]
                (result_batch_bytes, error_records_bytes)
                Both are serialized for return to main process
        """
        _worker_trim_memory()
        try:
            # Safe: deserializing trusted data from parent process
            map_task = cloudpickle.loads(map_task_bytes)
            error_config = (
                cloudpickle.loads(error_config_bytes) if error_config_bytes else None
            )

            # Create error handling context
            ctx = ErrorHandlingContext(
                job_id=job_id,
                task_context=task_context,
                seq=seq,
                udf_name=udf_name,
                udf_version=udf_version,
                input_columns=input_columns,
                output_columns=output_columns,
                error_config=error_config,
            )

            # Create strategy (no error_logger in worker process)
            strategy = BatchStrategy.from_context(ctx, map_task, error_logger=None)

            batches = _buf_to_batch(buf, coalesce=False)
            out_batches = []
            all_error_records = []

            # Ensure batches is always a list
            if isinstance(batches, pa.RecordBatch):
                batches = [batches]

            # Apply strategy to each batch - no branching!
            total_skip_count = 0
            for batch in batches:
                result_batch, error_records, skip_count = strategy.apply(batch)
                out_batches.append(result_batch)
                all_error_records.extend(error_records)
                total_skip_count += skip_count

            out_buf = io.BytesIO()
            with pa.ipc.new_stream(out_buf, schema=out_batches[0].schema) as f:
                for batch in out_batches:
                    f.write_batch(batch)

            # Serialize error records and skip count
            error_records_bytes = cloudpickle.dumps(all_error_records)

            return (
                out_buf.getvalue(),
                error_records_bytes,
                total_skip_count,
            )
        except Exception as e:
            raise _picklable_worker_error(e) from None

    @staticmethod
    def _worker_stall_timeout_s() -> float:
        """Resolve the per-future stall bound from the environment."""
        raw = os.environ.get(_WORKER_STALL_TIMEOUT_ENV)
        if raw is None:
            return _DEFAULT_WORKER_STALL_TIMEOUT_S
        try:
            return float(raw)
        except ValueError:
            _LOG.warning(
                "invalid %s=%r; using default %.0fs",
                _WORKER_STALL_TIMEOUT_ENV,
                raw,
                _DEFAULT_WORKER_STALL_TIMEOUT_S,
            )
            return _DEFAULT_WORKER_STALL_TIMEOUT_S

    def _await_head_ready(
        self,
        futs: list,
        last_progress: float,
        stall_timeout_s: float,
    ) -> None:
        """Block until ``futs[0]`` is ready, or raise once the head stalls.

        Applies the stall bound described under *Dead-worker detection* at the
        top of this module. *last_progress* is when a head was last retired,
        not when a batch last completed, so exceeding the bound means this
        future is not arriving: raise ``FatalWorkerCrashError`` and let the Ray
        layer act on it instead of wedging forever.
        """
        while True:
            # Blocks on the future's own event, so a ready result returns
            # immediately; the timeout only sets the stall-check cadence.
            futs[0].wait(timeout=_POOL_POLL_INTERVAL_S)
            if futs[0].ready():
                return

            if time.monotonic() - last_progress > stall_timeout_s:
                raise FatalWorkerCrashError(
                    f"multiprocess worker stalled (job {self.job_id}): the "
                    f"in-flight batch has not returned in {stall_timeout_s:.0f}s"
                )

    def _process_future_result(
        self,
        fut,
        ctx: ErrorHandlingContext,
        error_logger: ErrorLogger,
        all_error_records: list,
    ) -> tuple[pa.RecordBatch | list[pa.RecordBatch], int]:
        """Process a single future result with error handling.

        Returns
        -------
        tuple[pa.RecordBatch | list[pa.RecordBatch], int]
            (result_batch, skip_count)
        """
        start = time.perf_counter()
        skip_count = 0
        try:
            result = fut.get()
            if ctx.error_config:
                # Unpack result, error records, and skip count
                result_bytes, error_records_bytes, skip_count = result
                error_records = cloudpickle.loads(error_records_bytes)
                all_error_records.extend(error_records)
                out = _buf_to_batch(result_bytes, coalesce=True)
            else:
                out = _buf_to_batch(result, coalesce=True)
        except Exception as e:
            # Log error with full context
            if ctx.error_config and ctx.error_config.log_errors:
                error_record = ctx.create_error_record(
                    exception=e,
                    row_address=None,
                    attempt=1,
                    max_attempts=1,
                )
                error_logger.log_error(error_record)
            raise
        else:
            # Only count successful executions; failed UDFs should not contribute.
            self.udf_processing_time_ms += int((time.perf_counter() - start) * 1000)
            return (out, skip_count)

    def run(
        self,
        read_task: ReadTask,
        map_task: MapTask,
        error_logger: ErrorLogger,
    ) -> Iterator[pa.RecordBatch]:
        self.reset_run_state()
        error_config = get_error_handling_config(map_task)
        skip_tracker = (
            make_skip_budget_tracker(error_config)
            if self.enforce_skip_threshold
            else None
        )
        mp_ctx = (
            multiprocess.context.ForkContext()
            if self.method == "fork"
            else multiprocess.context.SpawnContext()
        )

        with mp_ctx.Pool(self.num_processes) as pool:
            # don't pull new batches until the previous ones are done
            # this way we reduce the number of batches in memory
            all_error_records = []  # Collect all errors for bulk write
            should_log_errors = None  # Track from first batch's context

            stall_timeout_s = self._worker_stall_timeout_s()
            memory_trim_interval = get_applier_memory_trim_interval()

            def _run_with_backpressure():  # noqa: ANN202
                nonlocal should_log_errors
                futs = []
                ctxs = []
                batch_sizes = []  # Track batch sizes for skip counting
                # Time of the last completed batch; drives the stall bound in
                # _await_head_ready.
                last_progress = time.monotonic()

                batch_iter = read_task.to_batches(batch_size=map_task.batch_size())
                for seq, (read_ms, batch) in enumerate(
                    _iter_with_next_duration(iter(batch_iter))
                ):
                    self.read_io_time_ms += read_ms
                    # Create error context for this batch
                    ctx = ErrorHandlingContext.create(
                        map_task, read_task, self.job_id, seq
                    )
                    ctxs.append(ctx)
                    batch_rows = (
                        batch.num_rows
                        if isinstance(batch, pa.RecordBatch)
                        else len(batch)
                    )
                    batch_sizes.append(batch_rows)

                    # Track error logging config from first batch
                    if should_log_errors is None:
                        should_log_errors = (
                            ctx.error_config and ctx.error_config.log_errors
                        )
                    data = _batch_to_buf(batch)

                    # Choose worker function based on error handling config
                    if ctx.error_config:
                        # Use error handling worker - returns tuple with error records
                        map_task_data = cloudpickle.dumps(map_task)
                        error_config_data = cloudpickle.dumps(ctx.error_config)
                        futs.append(
                            pool.apply_async(
                                MultiProcessBatchApplier._worker_apply,
                                args=(
                                    map_task_data,
                                    data,
                                    error_config_data,
                                    self.job_id,
                                    ctx.task_context,
                                    seq,
                                    ctx.udf_name,
                                    ctx.udf_version,
                                    ctx.input_columns,
                                    ctx.output_columns,
                                ),
                            )
                        )
                    else:
                        # Use simple worker - legacy behavior without error handling
                        udf_data = cloudpickle.dumps(map_task.apply)
                        futs.append(
                            pool.apply_async(
                                _apply_with_stream_buf, args=(udf_data, data)
                            )
                        )

                    # don't start waiting till we have primed the queue
                    if len(futs) >= self.num_processes + 1:
                        self._await_head_ready(futs, last_progress, stall_timeout_s)
                        ctx = ctxs.pop(0)
                        fut = futs.pop(0)
                        batch_size = batch_sizes.pop(0)
                        result, skip_count = self._process_future_result(
                            fut,
                            ctx,
                            error_logger,
                            all_error_records,
                        )
                        last_progress = time.monotonic()
                        self.total_rows += batch_size
                        self.skip_count += skip_count
                        if skip_tracker is not None and batch_size > 0:
                            skip_tracker.record_batch(batch_size, skip_count)
                        yield result
                        self.trim_counter.record_batch(memory_trim_interval)

                while futs:
                    self._await_head_ready(futs, last_progress, stall_timeout_s)
                    ctx = ctxs.pop(0)
                    fut = futs.pop(0)
                    batch_size = batch_sizes.pop(0)
                    result, skip_count = self._process_future_result(
                        fut,
                        ctx,
                        error_logger,
                        all_error_records,
                    )
                    last_progress = time.monotonic()
                    self.total_rows += batch_size
                    self.skip_count += skip_count
                    if skip_tracker is not None and batch_size > 0:
                        skip_tracker.record_batch(batch_size, skip_count)
                    yield result
                    self.trim_counter.record_batch(memory_trim_interval)

            yielded = False
            try:
                for item in _run_with_backpressure():
                    yielded = True
                    if isinstance(item, list):
                        yield from item
                    else:
                        yield item
            finally:
                # Flush collected error records even if SkipThresholdExceededError
                # (or any other exception) fires mid-run, so records from batches
                # processed before the threshold are not silently discarded.
                if should_log_errors and all_error_records:
                    error_logger.log_errors(all_error_records)

            if not yielded:
                return
