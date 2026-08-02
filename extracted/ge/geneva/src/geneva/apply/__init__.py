# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import os
import queue
import threading
import time
from collections.abc import Iterator, Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, TypeVar, cast

import attrs
import lance
import pyarrow as pa
from .utils import (
    _buffered_shuffle,
    _check_fragment_data_file_exists,
    _compute_missing_ranges,
    _count_udf_rows,
    _index_checkpoint_ranges,
    _iter_checkpoint_ranges_for_fragment,
    _legacy_fragment_dedupe_key,
    _merge_ranges,
    diversity_aware_shuffle,
)

from geneva import telemetry
from geneva.apply.adaptive import (
    AdaptiveCheckpointSizer,
    AdaptiveReadTask,
    BatchSizeTracker,
)
from geneva.apply.applier import BatchApplier
from geneva.apply.blob_checkpoint import (
    BlobCheckpointOptimizationUnsupportedError,
    blob_v2_checkpoint_data_file_name,
    default_fragment_data_dir,
    prepare_blob_v2_checkpoint_batch,
    schema_supports_blob_v2_checkpoints,
    storage_version_supports_blob_v2_checkpoints,
)
from geneva.apply.simple import SimpleApplier
from geneva.apply.task import (
    DEFAULT_CHECKPOINT_ROWS,
    CopyTask,
    MapTask,
    ReadTask,
    ScanTask,
)
from geneva.checkpoint import (
    CheckpointStore,
    HierarchicalLanceCheckpointStore,
    unwrap_default_checkpoint_store,
)
from geneva.checkpoint_utils import hash_source_files
from geneva.db import NamespaceConfig
from geneva.debug.logger import ErrorLogger, NoOpErrorLogger
from geneva.table import TableReference
from geneva.utils import make_null_array, parse_data_storage_version, redact_dict_values
from geneva.utils.byte_budget_queue import (
    ByteBudgetedQueue,
    _ByteBudgetedQueueItem,
)
from geneva.utils.schema import resolve_arrow_field_path

_LOG = logging.getLogger(__name__)

DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS = 10.0
DEFAULT_CHECKPOINT_INTERVAL_SECONDS = 10.0

# Byte budget for the checkpoint flusher's in-RAM backlog. Acts as an OOM
# safety net for UDFs whose output column is large_binary / blob:
# ``checkpoint_size`` (rows) and ``flush_interval`` (time) are both safe for
# small fixed-width outputs but can permit hundreds of GB of pending output for
# blob-producing UDFs. When the running sum of ``pending[i].batch.nbytes``
# exceeds this value, the consumer flushes immediately regardless of row count
# or elapsed time; the producer queue also uses this value for byte-aware
# backpressure. 0 disables both byte triggers and restores the legacy
# (rows + time only) behavior.
DEFAULT_CHECKPOINT_PENDING_BYTES_TARGET = int(
    os.environ.get("GENEVA_CHECKPOINT_PENDING_BYTES_TARGET", str(1 << 30))
)

_CHECKPOINT_FLUSH_SENTINEL = object()
_CHECKPOINT_QUEUE_PUT_TIMEOUT_SECONDS = 0.1


def _canonical_read_column(schema: pa.Schema, col: str) -> str:
    try:
        return resolve_arrow_field_path(schema, col).canonical_path
    except (KeyError, ValueError):
        return col


def _canonical_read_columns(
    schema: pa.Schema | None, columns: list[str] | None
) -> list[str]:
    if columns is None:
        return []
    if schema is None:
        return list(columns)
    return [_canonical_read_column(schema, col) for col in columns]


@attrs.define(frozen=True)
class MapBatchCheckpoint:
    """Metadata for a single checkpointed map-task batch.

    Notes
    -----
        `offset` and `span` define the coverage window in the planner's
        fragment-local offset domain: `[offset, offset + span)`.

        `span` is the amount of progress this checkpoint represents in the
        planner's *logical* offset domain (the same domain used by `ScanTask`
        offset/limit and by writer ordering). It corresponds to the `_range-`
        suffix in `checkpoint_key` and may be larger than the batch's physical
        row count when `_rowaddr` is sparse (e.g., `where` filters or deletes).

        `num_rows` is the physical number of materialized rows stored in the
        checkpointed `RecordBatch` (`batch.num_rows`). This is useful for
        introspection/metrics/debugging, but must not be used as "coverage" when
        `_rowaddr` has gaps.

        `udf_rows` is the count of logical input rows that were actually handed
        to the UDF for this checkpointed batch. This can differ from `num_rows`
        for filtered / sparse tasks, and it is used for progress accounting
        rather than for checkpoint coverage.
    """

    checkpoint_key: str
    offset: int
    num_rows: int  # Physical rows in the stored RecordBatch (may be < span).
    span: int  # Logical coverage/progress in the planner offset domain.
    udf_rows: int


@attrs.define(frozen=True)
class DirectFragmentWriteConfig:
    ds_uri: str
    column_names: list[str]
    field_ids: list[int]
    column_indices: list[int]
    data_storage_version: str
    storage_options: dict[str, str] | None = attrs.field(
        default=None, repr=redact_dict_values
    )
    output_field_ids: frozenset[int] | None = None
    read_version: int | None = None
    namespace_impl: str | None = None
    namespace_properties: dict[str, str] | None = attrs.field(
        default=None, repr=redact_dict_values
    )
    table_id: list[str] | None = None
    # Multi-base placement: base id -> data-file directory, and fragment id ->
    # base id, so directly-written output files land in the fragment's base.
    base_data_dirs: dict[int, str] | None = None
    frag_to_base: dict[int, int] | None = None

    def placement_for_frag(self, frag_id: int) -> tuple[str | None, int | None]:
        """(data_dir, base_id) for a fragment; (None, None) = dataset root."""
        if self.base_data_dirs is None or self.frag_to_base is None:
            return None, None
        base_id = self.frag_to_base.get(frag_id)
        if base_id is None:
            return None, None
        data_dir = self.base_data_dirs.get(base_id)
        if data_dir is None:
            return None, None
        return data_dir, base_id


@attrs.define(frozen=True)
class DirectFragmentWriteResult:
    frag_id: int
    new_file: lance.fragment.DataFile
    rows_written: int
    checkpoint_written: bool = True
    fragment_checkpointing_ms: int = 0
    buffer_sort_ms: int = 0
    align_ms: int = 0
    write_ms: int = 0
    queue_wait_ms: int = 0
    checkpoint_read_ms: int = 0
    avg_batch_num_rows: int = 0
    avg_batch_size: int = 0


def get_fragment_dedupe_key(
    uri: str,
    frag_id: int,
    map_task: MapTask,
    dataset_version: int | str | None = None,
    src_files_hash: str | None = None,
) -> str:
    prefix = map_task.checkpoint_prefix(
        dataset_uri=uri,
        where=getattr(map_task, "where", None),
        column=None,
        src_files_hash=src_files_hash,
    )
    return f"{prefix}_frag-{frag_id}"


def blob_v2_checkpoint_data_file_name_for_fragment(
    uri: str,
    frag_id: int,
    map_task: MapTask,
    dataset_version: int | str | None = None,
    src_files_hash: str | None = None,
) -> str:
    dedupe_key = get_fragment_dedupe_key(
        uri,
        frag_id,
        map_task,
        dataset_version=dataset_version,
        src_files_hash=src_files_hash,
    )
    return blob_v2_checkpoint_data_file_name(dedupe_key)


@attrs.define(frozen=True)
class _PlanReadResult:
    tasks: Iterator[ReadTask]
    total_tasks: int
    skipped_fragments: dict[int, tuple[lance.fragment.DataFile, int]]
    skipped_stats: dict[str, int]
    src_data_files_by_dst: dict[int, frozenset[str]]


@attrs.define(frozen=True)
class _PendingBatchCheckpoint:
    """A mapped batch waiting to be flushed by the checkpoint writer thread.

    `start` / `end` are planner fragment-local offsets in the same logical
    offset domain used by `MapBatchCheckpoint.offset/span`. They are not row
    indexes within `batch`; they describe the coverage window that this batch
    contributes toward the task's checkpointed progress.
    """

    batch: pa.RecordBatch
    start: int
    end: int
    udf_rows: int


def _concat_record_batches(batches: list[pa.RecordBatch]) -> pa.RecordBatch:
    """Concatenate adjacent checkpoint batches into one physical write.

    Order matters: callers must pass batches in task output order. The
    checkpoint flusher relies on this to preserve the monotonic mapping between
    the concatenated `RecordBatch` and the merged `[start, end)` coverage
    window.

    The current callers preserve that order:
    - `SimpleApplier.run()` yields mapped batches in read-task order.
    - `MultiProcessBatchApplier.run()` submits work concurrently but yields
      results in submission order (FIFO), not completion order.
    """
    if not batches:
        raise ValueError("cannot concatenate empty batch list")
    if len(batches) == 1:
        return batches[0]

    table = pa.Table.from_batches(batches).combine_chunks()
    if table.num_rows <= 0:
        schema = batches[0].schema
        return pa.record_batch(
            [pa.array([], type=field.type) for field in schema], schema=schema
        )

    return pa.record_batch(
        [table.column(i).combine_chunks() for i in range(table.num_columns)],
        schema=table.schema,
    )


@attrs.define
class _CheckpointFlushConsumer:
    """Own the checkpoint flusher thread state for one running read task.

    This class is the sole consumer for ``checkpoint_queue``. The producer
    lives in ``CheckpointingApplier._run()`` and enqueues
    ``_PendingBatchCheckpoint`` items as the ``BatchApplier`` yields mapped
    batches in input order. ``CollocatedPipelinedApplier`` enforces the
    input-order invariant via its GPU-input ``SequenceQueue``;
    ``SimpleApplier`` and ``MultiProcessBatchApplier`` yield in
    submission order natively. Each flush concatenates ``self.pending``
    and emits one checkpoint covering the full ``[first.start, last.end)``
    range (logical offset domain, matching ``MapBatchCheckpoint.span``).
    """

    owner: "CheckpointingApplier"
    task: ReadTask
    checkpoint_queue: ByteBudgetedQueue[object]
    sink: list[MapBatchCheckpoint]
    direct_sink: list[DirectFragmentWriteResult]
    errors: list[Exception]
    dataset_uri: str
    dataset_version: int | str | None
    where: str | None
    src_files_hash: str | None

    pending: list[_ByteBudgetedQueueItem[_PendingBatchCheckpoint]] = attrs.field(
        factory=list, init=False
    )
    pending_bytes: int = attrs.field(default=0, init=False)
    flush_interval: float = attrs.field(init=False)
    pending_bytes_target: int = attrs.field(default=0, init=False)
    next_flush_deadline: float | None = attrs.field(default=None, init=False)
    flushed_batch_checkpoints: bool = attrs.field(default=False, init=False)

    def __attrs_post_init__(self) -> None:
        self.flush_interval = max(
            0.0, float(self.owner.batch_checkpoint_flush_interval_seconds)
        )
        self.pending_bytes_target = max(
            0, int(self.owner.checkpoint_pending_bytes_target)
        )

    def _pending_items(self) -> list[_PendingBatchCheckpoint]:
        return [lease.item for lease in self.pending]

    def _release_pending(self) -> None:
        for lease in self.pending:
            lease.release()
        self.pending.clear()
        self.pending_bytes = 0

    def _maybe_upgrade_pending_to_direct_fragment(self) -> bool:
        if (
            self.flushed_batch_checkpoints
            or self.owner.direct_fragment_write is None
            or self.owner._should_use_blob_v2_checkpoints(self.task)
            or not self.owner._is_full_fragment_task(self.task)
            or not self.pending
        ):
            return False

        pending_items = self._pending_items()
        merged_batch = _concat_record_batches([item.batch for item in pending_items])
        merged_start = int(pending_items[0].start)
        merged_end = int(pending_items[-1].end)
        task_start = int(self.task.dest_offset())
        task_end = task_start + int(self.task.num_rows())
        if merged_start != task_start or merged_end != task_end:
            return False

        fragment_rows = int(getattr(self.task, "fragment_physical_rows", 0) or 0)
        if not self.owner._batch_covers_full_fragment(
            merged_batch,
            frag_id=self.task.dest_frag_id(),
            fragment_rows=fragment_rows,
        ):
            return False

        merged_udf_rows = sum(item.udf_rows for item in pending_items)
        self.direct_sink.append(
            self.owner._write_direct_fragment_result(
                self.task,
                merged_batch,
                udf_rows=merged_udf_rows,
            )
        )
        self._release_pending()
        return True

    def _flush_pending(self, *, final: bool = False) -> None:
        if not self.pending:
            return

        # The direct-fragment-write fast path can only fire when the
        # final flush sees exactly the full task in pending. Try it
        # first; on success ``pending`` is cleared by the upgrade
        # helper.
        if final and self._maybe_upgrade_pending_to_direct_fragment():
            return

        pending_items = self._pending_items()
        merged_batch = _concat_record_batches([item.batch for item in pending_items])
        merged_start = pending_items[0].start
        merged_end = pending_items[-1].end
        if merged_end < merged_start:
            merged_end = merged_start
        merged_udf_rows = sum(item.udf_rows for item in pending_items)

        try:
            checkpoint_batch = self.owner._prepare_checkpoint_batch_for_write(
                self.task,
                merged_batch,
                start=merged_start,
                src_files_hash=self.src_files_hash,
            )
            result = self.owner._build_batch_checkpoint_result(
                self.task,
                checkpoint_batch,
                dataset_uri=self.dataset_uri,
                dataset_version=self.dataset_version,
                where=self.where,
                udf_rows=merged_udf_rows,
                start=merged_start,
                end=merged_end,
                src_files_hash=self.src_files_hash,
            )
            self.owner._write_checkpoint_batch(result.checkpoint_key, checkpoint_batch)
            self.sink.append(result)
            self.flushed_batch_checkpoints = True
        finally:
            self._release_pending()

    def run(self) -> None:
        """Consume checkpoint batches and flush them on time or task end.

        Each iteration either appends the next ``_PendingBatchCheckpoint`` to
        ``self.pending`` (merged into one checkpoint at flush time, see
        ``_flush_pending``) or triggers a flush — when the queue goes idle
        long enough to hit ``flush_interval``, when a freshly-arrived item
        crosses the deadline, or when the producer sends the terminal
        sentinel.

        The producer is required to enqueue items in input order
        (``BatchApplier.run`` contract); ``_flush_pending``
        concatenates ``self.pending`` directly with no reordering.
        """
        try:
            while True:
                timeout: float | None = None
                if (
                    self.pending
                    and self.flush_interval > 0
                    and self.next_flush_deadline is not None
                ):
                    timeout = max(0.0, self.next_flush_deadline - time.perf_counter())
                try:
                    lease = (
                        self.checkpoint_queue.get(timeout=timeout)
                        if timeout is not None
                        else self.checkpoint_queue.get()
                    )
                except queue.Empty:
                    self._flush_pending()
                    self.next_flush_deadline = None
                    continue

                item = lease.item
                if item is _CHECKPOINT_FLUSH_SENTINEL:
                    lease.release()
                    break
                # The producer only enqueues _PendingBatchCheckpoint items plus
                # the terminal sentinel above.
                if not isinstance(item, _PendingBatchCheckpoint):
                    lease.release()
                    raise TypeError(f"unexpected checkpoint queue item: {type(item)}")

                pending_lease = cast(
                    "_ByteBudgetedQueueItem[_PendingBatchCheckpoint]", lease
                )
                self.pending.append(pending_lease)
                self.pending_bytes += int(pending_lease.size_bytes)
                if self.flush_interval <= 0:
                    self._flush_pending()
                    self.next_flush_deadline = None
                    continue

                if (
                    self.pending_bytes_target > 0
                    and self.pending_bytes > self.pending_bytes_target
                ):
                    _LOG.debug(
                        "flushing pending checkpoint buffer at %d bytes "
                        "(target=%d, rows=%d)",
                        self.pending_bytes,
                        self.pending_bytes_target,
                        sum(p.item.batch.num_rows for p in self.pending),
                    )
                    self._flush_pending()
                    self.next_flush_deadline = None
                    continue

                if self.next_flush_deadline is None:
                    self.next_flush_deadline = time.perf_counter() + self.flush_interval
                elif time.perf_counter() >= self.next_flush_deadline:
                    self._flush_pending()
                    self.next_flush_deadline = None

            self._flush_pending(final=True)
        except Exception as exc:
            self._release_pending()
            self.errors.append(exc)


class _CountingReadTask(ReadTask):
    """Proxy ReadTask that counts rows selected for UDF execution."""

    def __init__(self, inner: ReadTask) -> None:
        self._inner = inner
        self.cnt_udf_computed: int = 0
        self.udf_rows_history: list[int] = []

    def to_batches(
        self,
        *,
        batch_size: int = DEFAULT_CHECKPOINT_ROWS,
    ) -> Iterator[pa.RecordBatch | list[dict]]:
        for batch in self._inner.to_batches(batch_size=batch_size):
            count = _count_udf_rows(batch)
            self.cnt_udf_computed += count
            self.udf_rows_history.append(count)
            yield batch

    def checkpoint_key(self) -> str:
        return self._inner.checkpoint_key()

    def dest_frag_id(self) -> int:
        return self._inner.dest_frag_id()

    def dest_offset(self) -> int:
        return self._inner.dest_offset()

    def num_rows(self) -> int:
        return self._inner.num_rows()

    def table_uri(self) -> str:
        return self._inner.table_uri()

    def __getattr__(self, item: str) -> Any:
        return getattr(self._inner, item)


@attrs.define
class CheckpointingApplier:
    """
    Read a ``ReadTask``, apply a ``MapTask``, and checkpoint its output batches.

    Checkpoint writes are performed by a small in-process flusher loop. When
    ``batch_checkpoint_flush_interval_seconds`` is greater than zero, mapped
    batches are queued and the flusher concatenates any pending batches before
    writing them to the checkpoint store. This reduces object-store PUT count
    at the cost of waiting up to the configured flush interval before a batch
    is persisted.

    Setting ``batch_checkpoint_flush_interval_seconds=0`` disables the
    asynchronous time-based flush behavior and falls back to the known-stable
    synchronous path: every mapped batch is written immediately with no
    time-based buffering. This provides an explicit fallback if the async
    flusher causes instability in a given workload.

    The checkpointed output allows a job to resume from the same point if it
    is interrupted.
    """

    checkpoint_uri: str = attrs.field()
    map_task: MapTask = attrs.field()
    batch_checkpoint_flush_interval_seconds: float = attrs.field(
        default=DEFAULT_BATCH_CHECKPOINT_FLUSH_INTERVAL_SECONDS
    )
    # Byte cap on the in-RAM backlog maintained by the checkpoint flusher.
    # Protects against OOMs when the UDF output column is ``large_binary`` /
    # blob: row-count and time-based flush triggers can otherwise let queued
    # plus pending output grow to hundreds of GB per applier. 0 disables the
    # byte trigger/backpressure; default reads
    # ``GENEVA_CHECKPOINT_PENDING_BYTES_TARGET``.
    checkpoint_pending_bytes_target: int = attrs.field(
        default=DEFAULT_CHECKPOINT_PENDING_BYTES_TARGET
    )

    error_logger: ErrorLogger = attrs.field(default=NoOpErrorLogger())
    batch_applier: BatchApplier = attrs.field(
        factory=SimpleApplier,
        converter=attrs.converters.default_if_none(factory=SimpleApplier),
    )
    direct_fragment_write: DirectFragmentWriteConfig | None = attrs.field(default=None)

    namespace_client_impl: str | None = attrs.field(default=None)
    namespace_client_properties: dict[str, str] | None = attrs.field(
        default=None, repr=redact_dict_values
    )
    checkpoint_table_id: list[str] | None = attrs.field(default=None)
    storage_options: dict[str, str] | None = attrs.field(
        default=None, repr=redact_dict_values
    )
    checkpoint_session_root_subdir: str | None = attrs.field(default=None)
    checkpoint_write_identity_sidecar: bool = attrs.field(default=True)
    # Multi-base placement: per-base checkpoint roots + fragment routing map,
    # so batch checkpoints land in the destination fragment's storage base.
    checkpoint_base_uris: dict[int, str] | None = attrs.field(default=None)
    checkpoint_frag_to_base: dict[int, int] | None = attrs.field(default=None)
    checkpoint_base_storage_options: dict[str, str] | None = attrs.field(
        default=None, repr=redact_dict_values
    )

    checkpoint_store: CheckpointStore = attrs.field(init=False)
    _shared_sizer: AdaptiveCheckpointSizer | None = attrs.field(
        default=None, init=False, repr=False
    )
    batch_checkpointing_time_ms: int = attrs.field(default=0, init=False)
    checkpoint_load_time_ms: int = attrs.field(default=0, init=False)
    checkpoint_exists_time_ms: int = attrs.field(default=0, init=False)
    checkpoint_list_time_ms: int = attrs.field(default=0, init=False)
    last_failed_timing_snapshot: dict[str, int] = attrs.field(factory=dict, init=False)
    _blob_checkpoint_namespace_client_value: Any | None = attrs.field(
        default=None, init=False, repr=False
    )
    _blob_checkpoint_namespace_client_loaded: bool = attrs.field(
        default=False, init=False, repr=False
    )

    def __attrs_post_init__(self) -> None:
        self.checkpoint_store = CheckpointStore.from_uri(
            self.checkpoint_uri,
            namespace_client_impl=self.namespace_client_impl,
            namespace_client_properties=self.namespace_client_properties,
            table_id=self.checkpoint_table_id,
            storage_options=self.storage_options,
            session_root_subdir=self.checkpoint_session_root_subdir,
            write_identity_sidecar=self.checkpoint_write_identity_sidecar,
            base_checkpoint_uris=self.checkpoint_base_uris,
            frag_to_base=self.checkpoint_frag_to_base,
            base_storage_options=self.checkpoint_base_storage_options,
        )

    def _get_or_create_sizer(self) -> AdaptiveCheckpointSizer:
        """Return the shared adaptive sizer, creating it on first call.

        The sizer is shared across ReadTasks within the same ApplierActor
        so that its learned ``current_size`` carries over from one fragment
        to the next, avoiding a per-fragment ramp-up cost.
        """
        if self._shared_sizer is not None:
            return self._shared_sizer

        checkpoint_size = self.map_task.batch_size() or DEFAULT_CHECKPOINT_ROWS
        min_override, max_override = self.map_task.adaptive_checkpoint_bounds()
        max_explicit = max_override is not None
        min_size = 1 if min_override is None else int(min_override)
        max_size = checkpoint_size if max_override is None else int(max_override)
        initial_size = self.map_task.initial_checkpoint_size()

        if max_size <= 0:
            max_size = checkpoint_size
        if not max_explicit and checkpoint_size > 0 and max_size > checkpoint_size:
            max_size = checkpoint_size
        if min_size <= 0:
            min_size = 1
        if min_size > max_size:
            min_size = max_size

        target_secs = self.map_task.checkpoint_interval_seconds()
        if target_secs is None or target_secs <= 0:
            target_secs = DEFAULT_CHECKPOINT_INTERVAL_SECONDS

        self._shared_sizer = AdaptiveCheckpointSizer(
            max_size=max_size,
            min_size=min_size,
            initial_size=initial_size,
            target_seconds=target_secs,
        )
        return self._shared_sizer

    @property
    def output_schema(self) -> pa.Schema:
        return self.map_task.output_schema()

    def _src_files_hash_for_task(
        self, task: ReadTask, src_files_hash: str | None = None
    ) -> str | None:
        if src_files_hash is not None:
            return src_files_hash
        src_data_files = getattr(task, "src_data_files", None)
        if src_data_files is None:
            return None
        return hash_source_files(src_data_files)

    def _checkpoint_key_for_task(self, task: ReadTask) -> str:
        start = task.dest_offset()
        end = start + task.num_rows()

        try:
            dataset_uri = task.table_uri()
        except Exception:
            dataset_uri = "unknown"

        dataset_version = getattr(task, "version", None)
        where = getattr(task, "where", None)
        src_files_hash = self._src_files_hash_for_task(
            task, getattr(task, "src_files_hash", None)
        )

        return self.map_task.checkpoint_key(
            dataset_uri=dataset_uri or "",
            dataset_version=dataset_version,
            frag_id=task.dest_frag_id(),
            start=start,
            end=end,
            where=where,
            src_files_hash=src_files_hash,
        )

    def _is_full_fragment_task(self, task: ReadTask) -> bool:
        fragment_logical_rows = getattr(task, "fragment_logical_rows", None)
        fragment_physical_rows = getattr(task, "fragment_physical_rows", None)
        if fragment_logical_rows is None or fragment_physical_rows is None:
            return False
        return (
            int(task.dest_offset()) == 0
            and int(task.num_rows()) == int(fragment_logical_rows)
            and int(fragment_physical_rows) == int(fragment_logical_rows)
        )

    def _batch_covers_full_fragment(
        self,
        batch: pa.RecordBatch,
        *,
        frag_id: int,
        fragment_rows: int,
    ) -> bool:
        if batch.num_rows != int(fragment_rows):
            return False
        if "_rowaddr" not in batch.schema.names:
            return False
        if batch.num_rows == 0:
            return True
        rowaddr = batch["_rowaddr"]
        first = rowaddr[0].as_py()
        last = rowaddr[-1].as_py()
        if first is None or last is None:
            return False
        expected_start = int(frag_id) << 32
        expected_end = expected_start + int(fragment_rows) - 1
        # Lance single-fragment scans yield row addresses in fragment order with
        # no gaps when physical_rows == logical_rows. Given that invariant, the
        # combination of exact row count plus first/last rowaddr is sufficient to
        # prove this batch covers the whole fragment.
        return int(first) == expected_start and int(last) == expected_end

    def _write_direct_fragment_result(
        self,
        task: ReadTask,
        batch: pa.RecordBatch,
        *,
        udf_rows: int,
    ) -> DirectFragmentWriteResult:
        if self.direct_fragment_write is None:
            raise ValueError("direct_fragment_write config is required")

        from geneva.fragment_writer import get_fragment_file_writer
        from geneva.runners.ray.writer import (
            build_fragment_checkpoint_batch,
            write_fragment_file,
        )

        config = self.direct_fragment_write
        data_dir, base_id = config.placement_for_frag(task.dest_frag_id())
        new_file, rows_written, write_ms = get_fragment_file_writer().write(
            write_fragment_file,
            config.ds_uri,
            iter([batch]),
            column_names=config.column_names,
            field_ids=config.field_ids,
            column_indices=config.column_indices,
            data_storage_version=config.data_storage_version,
            storage_options=config.storage_options,
            namespace_impl=config.namespace_impl,
            namespace_properties=config.namespace_properties,
            table_id=config.table_id,
            data_dir=data_dir,
            base_id=base_id,
        )

        dedupe_key = get_fragment_dedupe_key(
            config.ds_uri,
            task.dest_frag_id(),
            self.map_task,
            dataset_version=config.read_version,
            src_files_hash=self._src_files_hash_for_task(
                task, getattr(task, "src_files_hash", None)
            ),
        )
        checkpoint_batch = build_fragment_checkpoint_batch(
            file_path=new_file.path,
            output_field_ids=config.output_field_ids,
            udf_version=self.map_task.udf_version(),
            base_id=base_id,
        )
        ckpt_start = time.perf_counter()
        self.checkpoint_store[dedupe_key] = checkpoint_batch
        fragment_checkpointing_ms = int((time.perf_counter() - ckpt_start) * 1000)

        # The direct-write path only fires when no batch checkpoints have been
        # flushed for this task (see _maybe_upgrade_pending_to_direct_fragment),
        # so there are no batch keys for this run to clean up here.  Orphaned
        # batch keys from a previous attempt are swept by
        # Table.cleanup_checkpoints.

        return DirectFragmentWriteResult(
            frag_id=task.dest_frag_id(),
            new_file=new_file,
            rows_written=int(rows_written),
            checkpoint_written=True,
            fragment_checkpointing_ms=fragment_checkpointing_ms,
            write_ms=int(write_ms),
            avg_batch_num_rows=int(batch.num_rows),
            avg_batch_size=int(batch.nbytes),  # type: ignore[attr-defined]
        )

    def _compute_checkpoint_end(
        self,
        task: ReadTask,
        batch: pa.RecordBatch,
        *,
        start: int,
        checkpoint_size: int,
    ) -> int:
        task_end = task.dest_offset() + task.num_rows()
        if "_rowaddr" in batch.schema.names and batch.num_rows > 0:
            rowaddrs = batch["_rowaddr"]
            last_row_offset = int(rowaddrs[-1].as_py() & 0xFFFFFFFF)
        else:
            last_row_offset = start - 1

        end = max(start + checkpoint_size, last_row_offset + 1)
        end = min(task_end, end)
        if end < start:
            end = start
        return int(end)

    def _build_batch_checkpoint_result(
        self,
        task: ReadTask,
        batch: pa.RecordBatch,
        *,
        dataset_uri: str,
        dataset_version: int | str | None,
        where: str | None,
        udf_rows: int | None,
        start: int,
        end: int,
        src_files_hash: str | None = None,
    ) -> MapBatchCheckpoint:
        checkpoint_key = self.map_task.checkpoint_key(
            dataset_uri=dataset_uri or "",
            dataset_version=dataset_version,
            frag_id=task.dest_frag_id(),
            start=start,
            end=end,
            where=where,
            src_files_hash=src_files_hash,
        )
        udf_rows_val = int(udf_rows) if udf_rows is not None else _count_udf_rows(batch)
        return MapBatchCheckpoint(
            checkpoint_key=checkpoint_key,
            offset=int(start),
            num_rows=int(batch.num_rows),
            span=int(end - start),
            udf_rows=int(udf_rows_val),
        )

    def _should_use_blob_v2_checkpoints(self, task: ReadTask) -> bool:
        config = self.direct_fragment_write
        if config is None or not storage_version_supports_blob_v2_checkpoints(
            config.data_storage_version
        ):
            return False
        try:
            return schema_supports_blob_v2_checkpoints(self.output_schema)
        except BlobCheckpointOptimizationUnsupportedError:
            _LOG.debug(
                "Blob-v2 checkpoint optimization unsupported for task %s schema",
                task,
                exc_info=True,
            )
            return False

    def _blob_checkpoint_data_file_name(
        self,
        task: ReadTask,
        *,
        src_files_hash: str | None,
    ) -> str:
        config = self.direct_fragment_write
        if config is None:
            raise ValueError("direct_fragment_write config is required")
        return blob_v2_checkpoint_data_file_name_for_fragment(
            config.ds_uri,
            task.dest_frag_id(),
            self.map_task,
            dataset_version=config.read_version,
            src_files_hash=src_files_hash,
        )

    def _get_blob_checkpoint_namespace_client(self) -> Any | None:
        if self._blob_checkpoint_namespace_client_loaded:
            return self._blob_checkpoint_namespace_client_value
        self._blob_checkpoint_namespace_client_loaded = True
        config = self.direct_fragment_write
        if (
            config is None
            or not config.namespace_impl
            or not config.namespace_properties
            or not config.table_id
        ):
            return None
        self._blob_checkpoint_namespace_client_value = NamespaceConfig(
            namespace_client_impl=config.namespace_impl,
            namespace_client_properties=config.namespace_properties,
        ).connect_namespace_client(use_worker_props=True)
        return self._blob_checkpoint_namespace_client_value

    def _prepare_checkpoint_batch_for_write(
        self,
        task: ReadTask,
        batch: pa.RecordBatch,
        *,
        start: int,
        src_files_hash: str | None,
    ) -> pa.RecordBatch:
        if not self._should_use_blob_v2_checkpoints(task):
            return batch
        config = self.direct_fragment_write
        if config is None:
            return batch

        data_dir, _base_id = config.placement_for_frag(task.dest_frag_id())
        return prepare_blob_v2_checkpoint_batch(
            batch,
            data_dir=default_fragment_data_dir(config.ds_uri, data_dir),
            data_file_name=self._blob_checkpoint_data_file_name(
                task,
                src_files_hash=src_files_hash,
            ),
            range_start=start,
            storage_options=config.storage_options,
            namespace_client=self._get_blob_checkpoint_namespace_client(),
            table_id=config.table_id,
        )

    def _write_checkpoint_batch(
        self, checkpoint_key: str, batch: pa.RecordBatch
    ) -> None:
        # Use perf_counter for metrics so tests that monkeypatch time.monotonic
        # for adaptive checkpoint sizing don't need to account for additional
        # timing calls.
        ckpt_start = time.perf_counter()
        self.checkpoint_store[checkpoint_key] = batch
        self.batch_checkpointing_time_ms += int(
            (time.perf_counter() - ckpt_start) * 1000
        )

    def _make_pending_batch_checkpoint(
        self,
        task: ReadTask,
        batch: pa.RecordBatch,
        *,
        start: int,
        checkpoint_size: int,
        udf_rows: int | None,
    ) -> _PendingBatchCheckpoint:
        end = self._compute_checkpoint_end(
            task, batch, start=start, checkpoint_size=checkpoint_size
        )
        udf_rows_val = int(udf_rows) if udf_rows is not None else _count_udf_rows(batch)
        return _PendingBatchCheckpoint(
            batch=batch, start=int(start), end=int(end), udf_rows=int(udf_rows_val)
        )

    def _checkpoint_single_batch(
        self,
        task: ReadTask,
        batch: pa.RecordBatch,
        *,
        dataset_uri: str,
        dataset_version: int | str | None,
        where: str | None,
        udf_rows: int | None,
        start: int,
        checkpoint_size: int,
        src_files_hash: str | None = None,
    ) -> MapBatchCheckpoint:
        """Write one batch using the legacy one-checkpoint-per-task-key format.

        This is still used when reading older checkpoints from
        `_load_checkpointed_results()`: if a task key already points directly to
        a stored `RecordBatch` (rather than the newer checkpoint metadata
        table), we synthesize a `MapBatchCheckpoint` from that payload so mixed
        old/new checkpoint stores remain resumable.
        """
        end = self._compute_checkpoint_end(
            task, batch, start=start, checkpoint_size=checkpoint_size
        )
        checkpoint_batch = self._prepare_checkpoint_batch_for_write(
            task,
            batch,
            start=start,
            src_files_hash=src_files_hash,
        )
        result = self._build_batch_checkpoint_result(
            task,
            checkpoint_batch,
            dataset_uri=dataset_uri,
            dataset_version=dataset_version,
            where=where,
            udf_rows=udf_rows,
            start=start,
            end=end,
            src_files_hash=src_files_hash,
        )
        self._write_checkpoint_batch(result.checkpoint_key, checkpoint_batch)
        return result

    def _load_checkpointed_results(
        self, task: ReadTask
    ) -> tuple[list[MapBatchCheckpoint], int] | None:
        task_key = self._checkpoint_key_for_task(task)

        exists_start = time.perf_counter()
        task_key_exists = task_key in self.checkpoint_store
        self.checkpoint_exists_time_ms += int(
            (time.perf_counter() - exists_start) * 1000
        )

        if task_key_exists:
            ckpt_start = time.perf_counter()
            cached = self.checkpoint_store[task_key]
            self.checkpoint_load_time_ms += int(
                (time.perf_counter() - ckpt_start) * 1000
            )
            try:
                schema_names = cached.schema.names
            except Exception:
                schema_names = []

            if "checkpoint_key" in schema_names:
                ck = cached.column("checkpoint_key")
                offsets = cached.column("offset")
                num_rows = cached.column("num_rows")
                spans = cached.column("span")
                udf_rows = cached.column("udf_rows")

                results = [
                    MapBatchCheckpoint(
                        checkpoint_key=str(ck[idx].as_py()),
                        offset=int(offsets[idx].as_py()),
                        num_rows=int(num_rows[idx].as_py()),
                        span=int(spans[idx].as_py()),
                        udf_rows=int(udf_rows[idx].as_py()),
                    )
                    for idx in range(cached.num_rows)
                ]

                total_udf = sum(r.udf_rows for r in results)
                _LOG.info("Using cached result for %s", task_key)
                return results, total_udf
            else:
                # Legacy single-batch checkpoint stored directly under task key
                _LOG.info("Using legacy cached result for %s", task_key)
                dataset_uri = getattr(task, "table_uri", lambda: "unknown")()
                dataset_version = getattr(task, "version", None)
                where = getattr(task, "where", None)

                result = self._checkpoint_single_batch(
                    task,
                    cached,
                    dataset_uri=dataset_uri,
                    dataset_version=dataset_version,
                    where=where,
                    udf_rows=None,
                    start=task.dest_offset(),
                    checkpoint_size=self.map_task.batch_size()
                    or DEFAULT_CHECKPOINT_ROWS,
                    src_files_hash=self._src_files_hash_for_task(
                        task, getattr(task, "src_files_hash", None)
                    ),
                )
                return [result], result.udf_rows

        # Reconstruct from per-batch checkpoints if the task range is fully covered
        src_files_hash = self._src_files_hash_for_task(
            task, getattr(task, "src_files_hash", None)
        )
        base_prefix = self.map_task.checkpoint_prefix(
            dataset_uri=task.table_uri(),
            where=getattr(task, "where", None),
            column=None,
            src_files_hash=src_files_hash,
        )
        prefixes = [base_prefix]

        list_start = time.perf_counter()
        ranges = _iter_checkpoint_ranges_for_fragment(
            checkpoint_store=self.checkpoint_store,
            prefixes=prefixes,
            frag_id=task.dest_frag_id(),
        )
        self.checkpoint_list_time_ms += int((time.perf_counter() - list_start) * 1000)

        if not ranges:
            return None

        task_start = task.dest_offset()
        task_end = task_start + task.num_rows()

        # Select ranges overlapping the task window
        ranges = [
            (k, max(s, task_start), min(e, task_end))
            for k, s, e in ranges
            if e > task_start and s < task_end
        ]
        ranges.sort(key=lambda r: r[1])

        cur = task_start
        results: list[MapBatchCheckpoint] = []
        for key, s, e in ranges:
            if s > cur:
                return None  # gap
            span = e - cur
            if span <= 0:
                continue
            ckpt_start = time.perf_counter()
            batch = self.checkpoint_store[key]
            self.checkpoint_load_time_ms += int(
                (time.perf_counter() - ckpt_start) * 1000
            )
            results.append(
                MapBatchCheckpoint(
                    checkpoint_key=key,
                    offset=cur,
                    num_rows=int(batch.num_rows),
                    span=span,
                    udf_rows=_count_udf_rows(batch),
                )
            )
            cur = max(cur, e)
            if cur >= task_end:
                break

        if cur < task_end:
            return None

        total_udf = sum(r.udf_rows for r in results)
        return results, total_udf

    def _run(
        self, task: ReadTask
    ) -> tuple[list[MapBatchCheckpoint], DirectFragmentWriteResult | None, int]:
        _LOG.info("Running task %s", task)

        self.batch_checkpointing_time_ms = 0
        self.checkpoint_load_time_ms = 0
        self.checkpoint_exists_time_ms = 0
        self.checkpoint_list_time_ms = 0
        reset = getattr(self.batch_applier, "reset_run_state", None)
        if callable(reset):
            reset()
        elif hasattr(self.batch_applier, "udf_processing_time_ms"):
            # Best-effort reset for older appliers.
            self.batch_applier.udf_processing_time_ms = 0  # type: ignore[attr-defined]

        if cached := self._load_checkpointed_results(task):
            checkpoints, total_udf = cached
            return checkpoints, None, total_udf

        try:
            dataset_uri = task.table_uri()
        except Exception:
            dataset_uri = "unknown"

        dataset_version = getattr(task, "version", None)
        where = getattr(task, "where", None)
        src_files_hash = self._src_files_hash_for_task(
            task, getattr(task, "src_files_hash", None)
        )

        results: list[MapBatchCheckpoint] = []
        checkpoint_size = self.map_task.batch_size() or DEFAULT_CHECKPOINT_ROWS
        size_tracker = BatchSizeTracker()
        sizer = self._get_or_create_sizer()
        adaptive_task: ReadTask = AdaptiveReadTask(
            task,
            sizer=sizer,
            size_tracker=size_tracker,
        )
        proxy_task = _CountingReadTask(adaptive_task)
        batches = self.batch_applier.run(
            proxy_task,
            self.map_task,
            error_logger=self.error_logger,
        )

        next_start = task.dest_offset()

        had_any_batch = False
        idx = 0
        input_batches = iter(batches)

        queued_results: list[MapBatchCheckpoint] = []
        direct_results: list[DirectFragmentWriteResult] = []
        writer_errors: list[Exception] = []
        checkpoint_queue: ByteBudgetedQueue[object] = ByteBudgetedQueue(
            self.checkpoint_pending_bytes_target
        )
        flush_consumer = _CheckpointFlushConsumer(
            owner=self,
            task=task,
            checkpoint_queue=checkpoint_queue,
            sink=queued_results,
            direct_sink=direct_results,
            errors=writer_errors,
            dataset_uri=dataset_uri,
            dataset_version=dataset_version,
            where=where,
            src_files_hash=src_files_hash,
        )
        checkpoint_writer = threading.Thread(
            target=flush_consumer.run,
            name="geneva-checkpoint-writer",
            daemon=True,
        )
        checkpoint_writer.start()

        udf_metric_available = hasattr(self.batch_applier, "udf_processing_time_ms")
        prev_udf_ms = (
            int(getattr(self.batch_applier, "udf_processing_time_ms", 0) or 0)
            if udf_metric_available
            else None
        )

        try:
            while True:
                batch_start = time.monotonic()
                try:
                    batch = next(input_batches)
                except StopIteration:
                    break
                batch_elapsed = time.monotonic() - batch_start
                had_any_batch = True
                if writer_errors:
                    raise RuntimeError(
                        "checkpoint writer thread failed while processing task"
                    ) from writer_errors[0]

                udf_rows = (
                    proxy_task.udf_rows_history[idx]
                    if idx < len(proxy_task.udf_rows_history)
                    else None
                )
                batch_checkpoint_size = size_tracker.pop() or checkpoint_size
                # ``start`` is the running logical offset within the
                # task; ``_compute_checkpoint_end`` derives ``end``
                # from (start + checkpoint_size) clamped to
                # last_row_offset + 1 and the task's logical end.
                # Both live in the planner's logical offset domain
                # — see ``MapBatchCheckpoint.span``.
                #
                # The pipelined ``CollocatedPipelinedApplier`` uses a
                # ``SequenceQueue`` keyed by reader-emitted seq_no to
                # put batches back in input order before the apply
                # loop sees them, so this running counter advances in
                # input order even when K preprocess workers race the
                # GPU input. Without that ordering invariant the
                # counter would mispair ``[start, end)`` with batch
                # contents.
                pending = self._make_pending_batch_checkpoint(
                    task,
                    batch,
                    start=next_start,
                    checkpoint_size=batch_checkpoint_size,
                    udf_rows=udf_rows,
                )
                while True:
                    if writer_errors:
                        raise RuntimeError(
                            "checkpoint writer thread failed while processing task"
                        ) from writer_errors[0]
                    try:
                        checkpoint_queue.put(
                            pending,
                            int(pending.batch.nbytes),
                            timeout=_CHECKPOINT_QUEUE_PUT_TIMEOUT_SECONDS,
                        )
                        break
                    except queue.Full:
                        continue

                next_start = pending.end
                idx += 1

                udf_elapsed = batch_elapsed
                if udf_metric_available and prev_udf_ms is not None:
                    current_udf_ms = int(
                        getattr(self.batch_applier, "udf_processing_time_ms", 0) or 0
                    )
                    delta_udf_ms = current_udf_ms - prev_udf_ms
                    if delta_udf_ms > 0:
                        udf_elapsed = delta_udf_ms / 1000.0
                    prev_udf_ms = current_udf_ms
                num_rows = (
                    batch.num_rows if isinstance(batch, pa.RecordBatch) else len(batch)
                )
                sizer.record(duration_seconds=udf_elapsed, rows=num_rows)
        finally:
            checkpoint_queue.put_unmetered(_CHECKPOINT_FLUSH_SENTINEL)
            checkpoint_writer.join()

        if writer_errors:
            raise RuntimeError(
                "Error writing batch checkpoints asynchronously"
            ) from writer_errors[0]
        results.extend(queued_results)
        direct_result = direct_results[0] if direct_results else None
        if direct_result is not None and results:
            raise RuntimeError(
                "checkpoint flush consumer produced both batch checkpoints and "
                "a direct fragment result"
            )

        # If the read task yields no batches (e.g., `where` filters everything
        # out), we still need to persist completion checkpoints. Otherwise the
        # task is not idempotent: status()/_load_cached_results() would always
        # treat it as unfinished and retries would reschedule the same empty
        # work. We also need to enqueue *logical rows* for the writer, since the
        # writer waits for batches whose total num_rows matches the fragment's
        # logical row count. To satisfy both, we synthesize null-filled batches
        # in checkpoint_size chunks that cover the entire task window.
        if not had_any_batch:
            task_start = task.dest_offset()
            task_end = task_start + task.num_rows()
            frag_id = task.dest_frag_id()

            if task_end > task_start:
                schema = self.map_task.output_schema()
                # Partition the task window into checkpoint-sized subranges so the
                # number of synthetic checkpoints matches planning estimates.
                start = task_start
                while start < task_end:
                    end = min(start + checkpoint_size, task_end)
                    span = int(end - start)

                    arrays: list[pa.Array] = []
                    has_rowaddr = "_rowaddr" in schema.names
                    # Precompute rowaddr if needed.
                    if has_rowaddr:
                        row_addrs = pa.array(
                            [(frag_id << 32) | i for i in range(start, end)],
                            type=pa.uint64(),
                        )
                    for field in schema:
                        if field.name == "_rowaddr" and has_rowaddr:
                            arrays.append(row_addrs)
                        else:
                            # Use make_null_array for proper struct null handling
                            arrays.append(make_null_array(span, field.type))

                    filler_batch = pa.record_batch(arrays, schema=schema)
                    checkpoint_batch = self._prepare_checkpoint_batch_for_write(
                        task,
                        filler_batch,
                        start=start,
                        src_files_hash=src_files_hash,
                    )
                    completion = self._build_batch_checkpoint_result(
                        task,
                        checkpoint_batch,
                        dataset_uri=dataset_uri or "",
                        dataset_version=dataset_version,
                        where=where,
                        udf_rows=0,
                        start=start,
                        end=end,
                        src_files_hash=src_files_hash,
                    )
                    self._write_checkpoint_batch(
                        completion.checkpoint_key,
                        checkpoint_batch,
                    )
                    results.append(completion)
                    start = end

        total_udf_computed = proxy_task.cnt_udf_computed
        return results, direct_result, total_udf_computed

    def _timing_snapshot(self) -> dict[str, int]:
        return {
            "udf_processing_time_ms": int(
                getattr(self.batch_applier, "udf_processing_time_ms", 0) or 0
            ),
            "read_io_time_ms": int(
                getattr(self.batch_applier, "read_io_time_ms", 0) or 0
            ),
            "batch_checkpointing_time_ms": int(
                getattr(self, "batch_checkpointing_time_ms", 0) or 0
            ),
            "checkpoint_load_time_ms": int(
                getattr(self, "checkpoint_load_time_ms", 0) or 0
            ),
            "checkpoint_exists_time_ms": int(
                getattr(self, "checkpoint_exists_time_ms", 0) or 0
            ),
            "checkpoint_list_time_ms": int(
                getattr(self, "checkpoint_list_time_ms", 0) or 0
            ),
        }

    def run(
        self, task: ReadTask
    ) -> tuple[list[MapBatchCheckpoint], DirectFragmentWriteResult | None, int]:
        try:
            out = self._run(task)
            self.last_failed_timing_snapshot = {}
            return out
        except Exception as e:
            snapshot = self._timing_snapshot()
            self.last_failed_timing_snapshot = snapshot
            logging.exception(
                "Error running task %s: %s (partial timing snapshot=%s)",
                task,
                e,
                snapshot,
            )
            raise RuntimeError(f"Error running task {task}") from e

    def status(self, task: ReadTask) -> bool:
        # Reuse cached results reconstruction path for completion check
        return self._load_checkpointed_results(task) is not None


def _find_output_data_file_in_fragment(
    frag: lance.LanceFragment,
    output_field_ids: frozenset[int] | None,
) -> lance.fragment.DataFile | None:
    """Find a data file in the fragment that covers the output columns.

    This uses in-memory fragment metadata (from the manifest) so it requires
    no blob I/O.  Returns the matching [`DataFile`][DataFile] or ``None``.
    """
    if output_field_ids is None:
        return None
    for df in frag.data_files():
        if output_field_ids <= set(df.fields):
            return df
    return None


def _prefetch_filter_row_counts(
    fragments: list[lance.LanceFragment],
    where: str,
    max_workers: int,
) -> dict[int, int]:
    """Run ``count_rows(filter=where)`` on fragments in parallel.

    The serial driver loop in :func:`_plan_read` calls this once per
    fragment that isn't on the fast path. Each call is a Lance scan
    that reads filter columns from object storage, so the cost scales
    with fragment count × storage latency. Parallelizing brings ~30 min
    of serial planning on tens of thousands of fragments down to ~1 min.

    ``count_rows`` releases the GIL during native scan work, so threads
    overlap I/O effectively. Returns ``{fragment_id: matching_rows}``.
    """
    if not fragments:
        return {}
    workers = max(1, min(max_workers, len(fragments)))
    counts: dict[int, int] = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        future_to_frag = {ex.submit(f.count_rows, filter=where): f for f in fragments}
        for fut in as_completed(future_to_frag):
            f = future_to_frag[fut]
            counts[f.fragment_id] = fut.result()
    return counts


def _plan_read(
    uri: str,
    table_ref: TableReference,
    columns: list[str],
    *,
    read_version: int | None = None,
    task_size: int = DEFAULT_CHECKPOINT_ROWS,
    where: str | None = None,
    num_frags: int | None = None,
    skip_frags: int = 0,
    map_task: MapTask | None = None,
    checkpoint_store: CheckpointStore | None = None,
    default_where_generated: bool = False,
    _skip_populated_filter_count: bool = False,
    _skip_planner_filter_count: bool = False,
    _skip_checkpoint_index_scan: bool = False,
    _plan_filter_count_concurrency: int = 1,
    blob_read_strategy: str | None = None,
    blob_read_buffer_size: int | None = None,
    job_tracker: Any = None,
) -> _PlanReadResult:
    """Make Plan for Reading Data from a Dataset
    We want a ScanTask for each fragment in the dataset even if they are filtered
    out. This should make the checkpointing recovery easier to manage.

    Returns a tuple of (ReadTask iterator, skipped_fragments dict, skipped_stats dict,
    src_data_files_by_dst). skipped_stats contains {'fragments': count, 'rows': count}
    for progress tracking.
    """
    # Live planning progress -> JobTracker (best-effort; see report_plan_progress).
    # Open dataset with namespace if available
    from geneva.db import open_lance_dataset
    from geneva.runners.ray.jobtracker import report_plan_progress

    dataset = open_lance_dataset(
        uri,
        namespace_config=table_ref.namespace_config,
        table_id=table_ref.table_id,
        storage_options=table_ref.storage_options,
        use_worker_props=True,
    )
    namespace = table_ref.namespace_config.connect_namespace_client(
        use_worker_props=True
    )

    if read_version is not None:
        dataset = dataset.checkout_version(read_version)
    dataset_version = dataset.version

    # Multi-base datasets: staged output files may live in a fragment's
    # storage base rather than ``{uri}/data``. Manifest-only lookup; empty
    # for single-base datasets.
    from geneva.utils.multi_base import resolve_dataset_bases

    base_data_dirs: dict[int, str] | None = {
        base_id: base.data_dir
        for base_id, base in resolve_dataset_bases(dataset).items()
    }
    if not base_data_dirs:
        base_data_dirs = None

    from geneva.apply.blob_range import (
        blob_columns_in_schema,
        normalize_blob_read_strategy,
        plan_struct_blob_decomposition,
    )

    dataset_schema = getattr(dataset, "schema", None)
    scan_columns = _canonical_read_columns(dataset_schema, columns)
    map_input_cols = map_task.input_columns() if map_task is not None else None
    canonical_map_input_cols = (
        _canonical_read_columns(dataset_schema, map_input_cols)
        if map_input_cols is not None
        else None
    )

    normalized_blob_read_strategy = normalize_blob_read_strategy(blob_read_strategy)
    range_blob_columns: frozenset[str] | None = None
    selected_only_blob_columns: frozenset[str] | None = None
    struct_blob_decomp: tuple[Any, ...] | None = None
    should_plan_range_blob_reads = (
        normalized_blob_read_strategy == "range" or map_task is not None
    )
    if normalized_blob_read_strategy != "legacy" and should_plan_range_blob_reads:
        blob_scan_candidates = scan_columns
        if canonical_map_input_cols is not None:
            map_input_col_set = set(canonical_map_input_cols)
            blob_scan_candidates = [
                col for col in scan_columns if col in map_input_col_set
            ]
        # Detect both dotted/top-level blob columns and whole-struct columns that
        # contain a nested blob leaf. The latter are decomposed so the coalesced
        # range reader still fetches their blob bytes (instead of the legacy
        # all_binary path that issues ~one GetBlob per blob).
        input_blob_cols = blob_columns_in_schema(dataset.schema, blob_scan_candidates)
        decomp_plans = [
            plan
            for col in blob_scan_candidates
            if (plan := plan_struct_blob_decomposition(dataset.schema, col)) is not None
        ]
        # Map each decomposed struct's nested blob leaves so detection and the
        # selected-only fix can reason about them by their root struct column.
        nested_blob_leaves: set[str] = set()
        nested_root_by_leaf: dict[str, str] = {}
        for plan in decomp_plans:
            for leaf in plan.blob_paths():
                nested_blob_leaves.add(leaf)
                nested_root_by_leaf[leaf] = plan.column

        if input_blob_cols or nested_blob_leaves:
            # Materialize requested blob carry-forward columns on the range path,
            # including nested blob leaves under decomposed struct projections.
            scan_decomp_plans = [
                plan
                for col in scan_columns
                if (plan := plan_struct_blob_decomposition(dataset.schema, col))
                is not None
            ]
            scan_nested_leaves: set[str] = set()
            for plan in scan_decomp_plans:
                scan_nested_leaves.update(plan.blob_paths())
            range_blob_columns = blob_columns_in_schema(
                dataset.schema, scan_columns
            ) | frozenset(scan_nested_leaves)
            if scan_decomp_plans:
                struct_blob_decomp = tuple(scan_decomp_plans)
            if map_task is not None:
                output_columns = set(map_task.output_schema().names)
                output_columns.discard("_rowaddr")
                # Keep this in sync with BackfillUDFTask.apply's
                # carry_forward_set. The worker drops carry-forward output
                # columns before invoking the UDF; this planner-side set marks
                # input-only blob columns that can be skipped on filtered rows.
                selected_top_level = input_blob_cols - output_columns
                # A nested blob leaf is input-only ONLY if its ROOT struct is not
                # an output column. Comparing dotted leaves against struct-level
                # output names would wrongly skip a nested output blob's bytes on
                # non-matched rows, dropping carry-forward data.
                selected_nested = {
                    leaf
                    for leaf in nested_blob_leaves
                    if nested_root_by_leaf[leaf] not in output_columns
                }
                selected_only_blob_columns = frozenset(
                    selected_top_level | selected_nested
                )

    skipped_fragments = {}
    skipped_stats = {"fragments": 0, "rows": 0}
    tasks = []
    src_data_files_by_dst: dict[int, frozenset[str]] = {}
    checkpoint_keys: set[str] | None = None
    ranges_by_prefix: dict[str, dict[int, list[tuple[int, int]]]] | None = None
    get_source_data_files = None
    get_fragment_dedupe_key = None
    relevant_field_ids = None
    if map_task is not None:
        input_cols = canonical_map_input_cols
        if input_cols is not None:
            from geneva.runners.ray.pipeline import _get_relevant_field_ids

            relevant_field_ids = _get_relevant_field_ids(dataset, input_cols)
        from geneva.runners.ray.pipeline import (
            get_source_data_files as _get_source_data_files,
        )

        get_source_data_files = _get_source_data_files
    # Track output-column field IDs so we can validate fragment-level checkpoints
    # against the *current* output data files. This is important for cases like
    # test_rebackfill: when a column is dropped and re-added, the output column's
    # data files change even though the input-column src_files_hash can remain the
    # same. Without checking output files, we might wrongly reuse a checkpoint and
    # skip recomputation.
    output_field_ids: frozenset[int] | None = None
    use_blob_v2_assembly = False
    output_schema_has_blob_v2_checkpoints = False
    if map_task is not None:
        try:
            output_schema_has_blob_v2_checkpoints = schema_supports_blob_v2_checkpoints(
                map_task.output_schema()
            )
        except BlobCheckpointOptimizationUnsupportedError:
            output_schema_has_blob_v2_checkpoints = False
        use_blob_v2_assembly = (
            output_schema_has_blob_v2_checkpoints
            and storage_version_supports_blob_v2_checkpoints(
                dataset.data_storage_version
            )
        )
    if map_task is not None:
        try:
            from geneva.utils.parse_rust_debug import extract_field_ids

            output_field_id_set: set[int] = set()
            for field in map_task.output_schema():
                if field.name == "_rowaddr":
                    continue
                try:
                    output_field_id_set.update(
                        extract_field_ids(
                            dataset.lance_schema,
                            field.name,
                            omit_special_leaf_children=use_blob_v2_assembly,
                        )
                    )
                except Exception:  # noqa: PERF203
                    _LOG.debug(
                        "Output column %s not found in schema, skipping", field.name
                    )
            if output_field_id_set:
                output_field_ids = frozenset(output_field_id_set)
        except Exception:  # noqa: PERF203
            output_field_ids = None

    has_map_checkpoint_store = map_task is not None and checkpoint_store is not None
    map_task_without_checkpoint_store = (
        map_task is not None and checkpoint_store is None
    )
    if has_map_checkpoint_store and not _skip_checkpoint_index_scan:
        assert map_task is not None
        assert checkpoint_store is not None
        checkpoint_index_prefixes = None
        # Layout dispatch must see through the multi-base wrapper; the scoped
        # prefixes flow through the wrapper's list_keys to every child store.
        if isinstance(
            unwrap_default_checkpoint_store(checkpoint_store),
            HierarchicalLanceCheckpointStore,
        ):
            checkpoint_index_prefix = map_task.checkpoint_prefix(
                dataset_uri=uri,
                where=where,
                column=None,
                src_files_hash=None,
            )
            checkpoint_index_prefixes = [checkpoint_index_prefix]
        report_plan_progress(job_tracker, desc="Scanning checkpoints")
        _cp_scan_span = telemetry.open_span("checkpoint_index_scan")
        try:
            checkpoint_keys, ranges_by_prefix = _index_checkpoint_ranges(
                checkpoint_store=checkpoint_store,
                prefixes=checkpoint_index_prefixes,
            )
        except Exception:
            _LOG.warning(
                "Failed to index checkpoint keys; falling back to direct store probes",
                exc_info=True,
            )
            checkpoint_keys = None
            ranges_by_prefix = None
        telemetry.close_span(_cp_scan_span)
    empty_checkpoint_index = checkpoint_keys == set() and ranges_by_prefix == {}
    should_compute_src_files_hash = map_task_without_checkpoint_store or (
        has_map_checkpoint_store
        and (_skip_checkpoint_index_scan or not empty_checkpoint_index)
    )
    use_checkpoint_gap_planning = (
        has_map_checkpoint_store
        and not _skip_checkpoint_index_scan
        and not empty_checkpoint_index
    )
    if (
        has_map_checkpoint_store
        and not _skip_checkpoint_index_scan
        and not empty_checkpoint_index
    ):
        from geneva.runners.ray.pipeline import (
            _get_fragment_dedupe_key as _get_fragment_dedupe_key_fn,
        )

        get_fragment_dedupe_key = _get_fragment_dedupe_key_fn

    # get_fragments has an unsupported filter method, so we do filtering deeper in.
    effective_offset = skip_frags
    all_fragments = dataset.get_fragments()

    # Parallel prefetch of `count_rows(filter=where)` for fragments that
    # need it. Each call is a Lance scan against object storage (~tens of
    # ms); doing them serially in the main loop dominates planning time
    # on large tables (e.g. 30 min for 38k fragments). Threading is safe
    # because Lance releases the GIL during scan I/O.
    prefetched_filter_counts: dict[int, int] = {}
    if (
        where is not None
        and not _skip_planner_filter_count
        and _plan_filter_count_concurrency > 1
    ):
        # Mirror the main loop's dedupe short-circuit so the prefetch
        # doesn't scan fragments that will be skipped via `continue` at
        # the `checkpoint_exists` branch. Uses the in-memory
        # `checkpoint_keys` set; stale-dedupe cases (where the payload
        # validation later fails) fall back to the synchronous
        # `count_rows` in the main loop.
        dedupe_skip_enabled = (
            map_task is not None
            and checkpoint_keys is not None
            and not empty_checkpoint_index
            and get_source_data_files is not None
            and get_fragment_dedupe_key is not None
            and not _skip_checkpoint_index_scan
        )
        fragments_needing_count: list[lance.LanceFragment] = []
        for idx, frag in enumerate(all_fragments):
            if idx < effective_offset:
                continue
            if num_frags is not None and (idx - effective_offset) >= num_frags:
                break
            if dedupe_skip_enabled:
                assert get_source_data_files is not None
                assert get_fragment_dedupe_key is not None
                assert map_task is not None
                assert checkpoint_keys is not None
                src_files = get_source_data_files(frag, relevant_field_ids)
                src_files_hash = hash_source_files(src_files)
                dedupe_key = get_fragment_dedupe_key(
                    uri,
                    frag.fragment_id,
                    map_task,
                    dataset_version=dataset_version,
                    src_files_hash=src_files_hash,
                )
                if dedupe_key in checkpoint_keys:
                    continue
                legacy_key = _legacy_fragment_dedupe_key(
                    uri, frag.fragment_id, map_task
                )
                if legacy_key in checkpoint_keys:
                    continue
            if output_field_ids is not None:
                existing = _find_output_data_file_in_fragment(frag, output_field_ids)
                fast_path_safe = existing is None or _skip_populated_filter_count
            else:
                fast_path_safe = False
            if not fast_path_safe:
                fragments_needing_count.append(frag)
        if fragments_needing_count:
            report_plan_progress(job_tracker, desc="Counting rows")
            _prefetch_span = telemetry.open_span(
                "prefetch_counts",
                {"fragments": len(fragments_needing_count)},
            )
            prefetch_start = time.perf_counter()
            prefetched_filter_counts = _prefetch_filter_row_counts(
                fragments_needing_count,
                where,
                _plan_filter_count_concurrency,
            )
            _LOG.info(
                "plan_read: prefetched filter counts for %d fragments "
                "in %.1fs (concurrency=%d)",
                len(fragments_needing_count),
                time.perf_counter() - prefetch_start,
                _plan_filter_count_concurrency,
            )
            telemetry.close_span(_prefetch_span)

    _build_span = telemetry.open_span("build_tasks", {"fragments": len(all_fragments)})
    # Fragment counter: ticks through the (potentially long) per-fragment loop so
    # the live plan line reads "building tasks n/M" instead of a frozen timer.
    _plan_total = len(all_fragments)
    _plan_tick = max(1, _plan_total // 200)
    report_plan_progress(job_tracker, desc="Building tasks", n=0, total=_plan_total)
    for idx, frag in enumerate(all_fragments):
        if idx % _plan_tick == 0:
            report_plan_progress(job_tracker, n=idx + 1)
        if idx < effective_offset:
            continue
        _LOG.info(
            f"Processing fragment {idx} (fragment_id={frag.fragment_id}), "
            f"num_frags={num_frags}, skip_frags={skip_frags}"
        )
        if num_frags is not None and (idx - effective_offset) >= num_frags:
            _LOG.info(
                f"Breaking loop: idx {idx} - offset {effective_offset} "
                f">= num_frags {num_frags}"
            )
            break

        src_files_hash = None
        if map_task is not None:
            assert get_source_data_files is not None
            src_files = get_source_data_files(frag, relevant_field_ids)
            src_data_files_by_dst[frag.fragment_id] = src_files
            if should_compute_src_files_hash:
                src_files_hash = hash_source_files(src_files)

        # Compute dedupe key first so we can use the in-memory checkpoint_keys
        # set to avoid per-fragment blob I/O.
        dedupe_present = False
        dedupe_key: str | None = None
        if (
            has_map_checkpoint_store
            and not empty_checkpoint_index
            and not _skip_checkpoint_index_scan
        ):
            assert map_task is not None
            assert checkpoint_store is not None
            assert get_fragment_dedupe_key is not None
            dedupe_key = get_fragment_dedupe_key(
                uri,
                frag.fragment_id,
                map_task,
                dataset_version=dataset_version,
                src_files_hash=src_files_hash,
            )
            if checkpoint_keys is not None and dedupe_key in checkpoint_keys:
                dedupe_present = True
            else:
                legacy_key = _legacy_fragment_dedupe_key(
                    uri, frag.fragment_id, map_task
                )
                if checkpoint_keys is not None:
                    dedupe_present = legacy_key in checkpoint_keys
                    if dedupe_present:
                        dedupe_key = legacy_key
                else:
                    if dedupe_key in checkpoint_store:
                        dedupe_present = True
                    else:
                        dedupe_present = legacy_key in checkpoint_store
                        if dedupe_present:
                            dedupe_key = legacy_key

        # `_find_output_data_file_in_fragment` is a manifest lookup (no I/O);
        # the where-filter fast path below relies on it being populated.
        # The `_check_fragment_data_file_exists` blob I/O is still gated on
        # `dedupe_present` to keep the cold path cheap.
        checkpoint_exists = False
        existing_data_file: lance.fragment.DataFile | None = None
        checked_file_path: str | None = None
        checked_base_id: int | None = None
        current_data_files: frozenset[str] | None = None
        if output_field_ids is not None:
            existing_data_file = _find_output_data_file_in_fragment(
                frag, output_field_ids
            )
        if dedupe_present and has_map_checkpoint_store:
            assert map_task is not None
            assert checkpoint_store is not None
            if existing_data_file is not None:
                current_data_files = frozenset(df.path for df in frag.data_files())
            # Validate the checkpoint payload against current fragment state
            # before skipping. expected_rows is physical_rows, not the logical
            # (post-deletion) count: the writer fills staged files to the
            # physical layout, so a complete staged file has physical_rows rows.
            checked = _check_fragment_data_file_exists(
                uri,
                frag.fragment_id,
                map_task,
                checkpoint_store,
                dataset_version=dataset_version,
                src_files_hash=src_files_hash,
                current_output_field_ids=output_field_ids,
                current_data_files=current_data_files,
                namespace=namespace,
                table_id=table_ref.table_id,
                storage_options=table_ref.storage_options,
                checkpoint_keys=checkpoint_keys,
                expected_rows=frag.physical_rows,
                base_dirs=base_data_dirs,
            )
            if checked is not None:
                checked_file_path, checked_base_id = checked
            checkpoint_exists = checked is not None
        _LOG.debug(
            "Fragment %d (fragment_id=%d): checkpoint_exists=%s",
            idx,
            frag.fragment_id,
            checkpoint_exists,
        )

        frag_has_deletions = frag.num_deletions > 0
        frag_logical_rows = (
            frag.count_rows() if frag_has_deletions else frag.physical_rows
        )

        if checkpoint_exists:
            _LOG.debug(
                "Skipping fragment %d - data file already exists",
                frag.fragment_id,
            )

            # A fragment-level checkpoint means the committed output file already
            # covers the fragment's current logical row domain. Even when the job
            # is running with an implicit incremental filter such as "col IS NULL",
            # reusing that committed fragment should still count the fragment's
            # rows toward checkpointed/ready totals.
            skipped_rows = frag_logical_rows

            skipped_stats["fragments"] += 1
            skipped_stats["rows"] += skipped_rows

            # These should not be None here due to the checkpoint_exists check above
            assert map_task is not None
            assert checkpoint_store is not None
            assert dedupe_key is not None

            # Try to use the already-found in-memory data file first
            if existing_data_file is not None:
                skipped_fragments[frag.fragment_id] = (
                    existing_data_file,
                    skipped_rows,
                )
                continue

            # Use the file path already retrieved by _check_fragment_data_file_exists
            # to avoid a redundant checkpoint_store[key] read.
            from geneva.utils.parse_rust_debug import (
                extract_field_ids_and_column_indices,
            )

            assert checked_file_path is not None
            file_path = checked_file_path
            omit_special_leaf_children = False
            if storage_version_supports_blob_v2_checkpoints(
                dataset.data_storage_version
            ):
                try:
                    omit_special_leaf_children = schema_supports_blob_v2_checkpoints(
                        map_task.output_schema()
                    )
                except BlobCheckpointOptimizationUnsupportedError:
                    omit_special_leaf_children = False

            # The checkpointed files should only contain the columns being transformed
            # For UDF tasks, determine the field_ids and column_indices for output
            # Use extract_field_ids_and_column_indices to correctly handle 2.1 format
            # where non-leaf fields (list/struct parents) have column_index = -1
            if hasattr(map_task, "udfs") and map_task.udfs:  # type: ignore[attr-defined]
                output_names = [
                    field.name
                    for field in map_task.output_schema()
                    if field.name != "_rowaddr"
                ]
                column_names_for_ids = []
                for col in output_names:
                    try:
                        extract_field_ids_and_column_indices(
                            dataset.lance_schema,
                            [col],
                            dataset.data_storage_version,
                            omit_special_leaf_children=omit_special_leaf_children,
                        )
                    except ValueError:  # noqa: PERF203
                        _LOG.warning(
                            f"Column {col} not found in schema for "
                            f"checkpointed fragment {frag.fragment_id}, skipping"
                        )
                    else:
                        column_names_for_ids.append(col)
            else:
                # Fallback: use all columns (this shouldn't happen for UDF tasks)
                column_names_for_ids = columns

            field_ids, column_indices = extract_field_ids_and_column_indices(
                dataset.lance_schema,
                column_names_for_ids,
                dataset.data_storage_version,
                omit_special_leaf_children=omit_special_leaf_children,
            )

            # Create a DataFile object for this existing file. base_id records
            # which storage base the staged file was written to (from the
            # checkpoint payload); dropping it would commit a pointer that
            # resolves against the dataset root.
            dsv_major, dsv_minor = parse_data_storage_version(
                dataset.data_storage_version
            )
            data_file_from_checkpoint = lance.fragment.DataFile(
                file_path,
                field_ids,
                column_indices,
                dsv_major,
                dsv_minor,
                base_id=checked_base_id,
            )
            skipped_fragments[frag.fragment_id] = (
                data_file_from_checkpoint,
                skipped_rows,
            )
            continue

        # ScanTask offset/limit are in the fragment's logical-row domain. We can use
        # physical_rows as a fast path when there are no deletes, but fragments with
        # deletion vectors must plan in logical rows to avoid creating tasks for
        # deleted positions.
        frag_rows = frag_logical_rows
        # Fast-path conditions for skipping `count_rows(filter=...)`:
        #   1. No existing output data: synthetic null-filler can't clobber
        #      something that's already null.
        #   2. _skip_populated_filter_count: trust worker carry-forward to
        #      preserve populated values; trades the driver count for one
        #      redundant fragment rewrite per zero-match populated fragment.
        # Both require a map_task — the carry-forward path only runs in the
        # backfill applier, not raw reads / `plan_backfill` dry-runs.
        fast_path_safe = output_field_ids is not None and (
            existing_data_file is None or _skip_populated_filter_count
        )
        # In leaf mode (``_skip_planner_filter_count``) we never run the
        # per-fragment ``count_rows(filter=where)`` on the driver. The filter
        # is already carried on every ScanTask, so each worker re-applies it
        # at read time and a zero-match chunk simply yields no rows. Emitting a
        # task for every fragment trades a small amount of empty-task overhead
        # for eliminating the planning-phase scan entirely — the right call
        # when the filter isn't index-served (a full scan per fragment).
        if where and not fast_path_safe and not _skip_planner_filter_count:
            if frag.fragment_id in prefetched_filter_counts:
                filtered_frag_rows = prefetched_filter_counts[frag.fragment_id]
            else:
                filtered_frag_rows = frag.count_rows(filter=where)
            if filtered_frag_rows == 0:
                _LOG.debug(
                    "frag %d filtered by %r has no rows, skipping.",
                    frag.fragment_id,
                    where,
                )
                continue
        else:
            filtered_frag_rows = frag_rows

        _LOG.debug(
            "plan_read fragment: %s has %d rows, filtered to %d rows",
            frag,
            frag_rows,
            filtered_frag_rows,
        )

        # the ranges that we need to backfill, the tuple is (offset, num_rows),
        # which means we need to backfill the range [offset, offset + num_rows)
        gaps: list[tuple[int, int]]
        if not use_checkpoint_gap_planning:
            gaps = [
                (offset, min(task_size, frag_rows - offset))
                for offset in range(
                    0, frag_rows, task_size if task_size > 0 else frag_rows
                )
            ]
        else:
            assert map_task is not None
            assert checkpoint_store is not None
            prefixes = [
                map_task.checkpoint_prefix(
                    dataset_uri=uri,
                    where=where,
                    column=None,
                    src_files_hash=src_files_hash,
                ),
            ]
            if ranges_by_prefix is not None:
                covered = _merge_ranges(
                    [
                        item
                        for prefix in prefixes
                        for item in ranges_by_prefix.get(prefix, {}).get(
                            frag.fragment_id, []
                        )
                    ]
                )
            else:
                range_entries = _iter_checkpoint_ranges_for_fragment(
                    checkpoint_store=checkpoint_store,
                    prefixes=prefixes,
                    frag_id=frag.fragment_id,
                )
                covered = _merge_ranges(
                    [(start, end) for _key, start, end in range_entries]
                )
            if not checkpoint_exists and dedupe_present:
                if covered:
                    _LOG.info(
                        "Ignoring %d checkpoint ranges for fragment %s because "
                        "no data file exists for this fragment",
                        len(covered),
                        frag.fragment_id,
                    )
                covered = []

            fully_covered = (
                covered
                and covered[0][0] <= 0
                and covered[-1][1] >= frag_rows
                and len(covered) == 1
            )
            if fully_covered and existing_data_file is None:
                # Fully checkpointed per-batch but no committed output data file
                # (e.g. a crash between the last batch checkpoint and the
                # fragment commit). Skipping would leave the column NULL forever,
                # so replan to commit -- the applier reuses the per-batch
                # checkpoints, so the UDF is not recomputed. (existing_data_file
                # is None catches the no-fragment-checkpoint case the
                # dedupe_present guard above misses.)
                #
                # Emit one whole-fragment task, not task_size chunks: a task
                # narrower than an existing ``_range-START-END`` checkpoint would
                # split that key across tasks, handing the writer the same key at
                # multiple offsets. The writer re-derives span from the key
                # suffix, overshoots its SequenceQueue, and hangs. A
                # whole-fragment task keeps each checkpoint at its own boundary.
                _LOG.info(
                    "Fragment %s fully checkpointed but output not committed; "
                    "replanning as a single task to commit (reuses checkpoints, "
                    "no recompute)",
                    frag.fragment_id,
                )
                gaps = [(0, frag_rows)]
            elif fully_covered:
                # All rows already covered and committed -- genuinely done.
                _LOG.info(
                    "Skipping fragment %s entirely (all rows checkpointed)",
                    frag.fragment_id,
                )
                skipped_stats["rows"] += frag_rows
                skipped_stats["fragments"] += 1
                continue
            else:
                gaps = _compute_missing_ranges(
                    total_rows=frag_rows,
                    task_size=task_size,
                    covered=covered,
                )

        for offset, span in gaps:
            limit = span
            _LOG.debug(
                "scan task: idx=%d fragid=%d offset=%d limit=%d where=%r",
                idx,
                frag.fragment_id,
                offset,
                limit,
                where,
            )

            tasks.append(
                ScanTask(
                    uri=uri,
                    table_ref=table_ref,
                    version=dataset_version,
                    columns=scan_columns,
                    frag_id=frag.fragment_id,
                    offset=offset,
                    limit=limit,
                    where=where,
                    with_row_address=True,
                    range_blob_columns=range_blob_columns,
                    selected_only_blob_columns=selected_only_blob_columns,
                    struct_blob_decomp=struct_blob_decomp,
                    blob_read_strategy=normalized_blob_read_strategy,
                    blob_read_buffer_size=blob_read_buffer_size,
                    src_files_hash=src_files_hash,
                    src_data_files=src_data_files_by_dst.get(frag.fragment_id),
                    fragment_physical_rows=frag.physical_rows,
                    fragment_logical_rows=frag_logical_rows,
                )
            )

    telemetry.close_span(_build_span)
    report_plan_progress(job_tracker, n=_plan_total)

    _LOG.info(
        "Plan complete: %d scan tasks, %d skipped fragments (%d skipped rows)",
        len(tasks),
        skipped_stats["fragments"],
        skipped_stats["rows"],
    )

    return _PlanReadResult(
        tasks=iter(tasks),
        total_tasks=len(tasks),
        skipped_fragments=skipped_fragments,
        skipped_stats=skipped_stats,
        src_data_files_by_dst=src_data_files_by_dst,
    )


T = TypeVar("T")  # Define type variable "T"


@attrs.define
class _LanceReadPlanIterator(Iterator[T]):
    it: Iterator[T]
    total: int

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        return next(self.it)

    def __len__(self) -> int:
        return self.total


def plan_read(
    uri: str,
    table_ref: TableReference,
    columns: list[str],
    *,
    read_version: int | None = None,
    task_size: int | None = None,
    batch_size: int = DEFAULT_CHECKPOINT_ROWS,
    where: str | None = None,
    shuffle_buffer_size: int = 0,
    task_shuffle_diversity: int | None = None,
    num_frags: int | None = None,
    skip_frags: int = 0,
    map_task: MapTask | None = None,
    checkpoint_store: CheckpointStore | None = None,
    default_where_generated: bool = False,
    _skip_populated_filter_count: bool = False,
    _skip_planner_filter_count: bool = False,
    _skip_checkpoint_index_scan: bool = False,
    _plan_filter_count_concurrency: int = 1,
    blob_read_strategy: str | None = None,
    blob_read_buffer_size: int | None = None,
    job_tracker: Any = None,
    **unused_kwargs,
) -> tuple[Iterator[ReadTask], Mapping]:
    """
    Make Plan for Reading Data from a Dataset

    Parameters
    ----------
    num_frags:
        max number of fragments to scan for sampling use cases.
        None means process all fragments.
    skip_frags:
        number of fragments to skip before processing (default 0).
        Combined with ``num_frags`` this allows batching through a
        large dataset.
    """
    # `batch_size` historically controlled read-task sizing in these planners.
    # Keep it as a backwards-compatible alias for `task_size`.
    if (
        task_size is not None
        and batch_size != DEFAULT_CHECKPOINT_ROWS
        and batch_size != task_size
    ):
        _LOG.warning(
            "plan_read(batch_size=%s) overrides task_size=%s; "
            "use task_size going forward.",
            batch_size,
            task_size,
        )
    effective_task_size = batch_size if task_size is None else task_size

    plan_result = _plan_read(
        uri,
        table_ref,
        columns=columns,
        read_version=read_version,
        task_size=effective_task_size,
        where=where,
        num_frags=num_frags,
        skip_frags=skip_frags,
        map_task=map_task,
        checkpoint_store=checkpoint_store,
        default_where_generated=default_where_generated,
        _skip_populated_filter_count=_skip_populated_filter_count,
        _skip_planner_filter_count=_skip_planner_filter_count,
        _skip_checkpoint_index_scan=_skip_checkpoint_index_scan,
        _plan_filter_count_concurrency=_plan_filter_count_concurrency,
        blob_read_strategy=blob_read_strategy,
        blob_read_buffer_size=blob_read_buffer_size,
        job_tracker=job_tracker,
    )
    it = plan_result.tasks
    # same as no shuffle
    if shuffle_buffer_size > 1 and task_shuffle_diversity is None:
        it = _buffered_shuffle(it, buffer_size=shuffle_buffer_size)
    elif task_shuffle_diversity is not None:
        buffer_size = max(4 * task_shuffle_diversity, shuffle_buffer_size)
        it = diversity_aware_shuffle(
            it,
            key=lambda task: task.checkpoint_key(),
            diversity_goal=task_shuffle_diversity,
            buffer_size=buffer_size,
        )

    unused_kwargs["skipped_fragments"] = plan_result.skipped_fragments
    unused_kwargs["skipped_stats"] = plan_result.skipped_stats
    unused_kwargs["src_data_files_by_dst"] = plan_result.src_data_files_by_dst

    return _LanceReadPlanIterator(
        it,
        plan_result.total_tasks,
    ), unused_kwargs


def _plan_copy(
    src: TableReference,
    dst: TableReference,
    columns: list[str] | dict[str, str],
    *,
    task_size: int = DEFAULT_CHECKPOINT_ROWS,
    only_fragment_ids: set[int] | None = None,
    src_data_files_by_dst: dict[int, frozenset[str]] | None = None,
    job_tracker: Any = None,
) -> tuple[Iterator[CopyTask], int]:
    """Make Plan for Reading Data from a Dataset

    For materialized views, this iterates over DESTINATION fragments and creates
    CopyTasks for all of them. This destination-driven approach correctly handles
    cases where source fragments are consolidated into fewer destination fragments
    (e.g., due to filters or shuffle operations).

    Parameters
    ----------
        only_fragment_ids
            If provided, only create tasks for the specified
            destination fragment IDs. Used for incremental refresh to process
            only specific fragments.
    """
    from geneva.runners.ray.jobtracker import report_plan_progress

    # Read from DESTINATION dataset (destination-driven approach for materialized views)
    # to_lance: fresh — commit/merge path needs a live manifest
    dst_dataset = dst.open().to_lance()

    # Fragment counter: the count_rows() pass below is the per-fragment planning
    # work for a copy/refresh, so tick it through the live plan line.
    _frags = list(dst_dataset.get_fragments())
    _plan_total = len(_frags)
    _plan_tick = max(1, _plan_total // 200)
    report_plan_progress(job_tracker, desc="Counting fragments", n=0, total=_plan_total)
    num_tasks = 0
    for _idx, frag in enumerate(_frags):
        if _idx % _plan_tick == 0:
            report_plan_progress(job_tracker, n=_idx + 1)
        # Skip fragments that don't match the filter
        if only_fragment_ids is not None and frag.fragment_id not in only_fragment_ids:
            continue
        frag_rows = frag.count_rows()
        if frag_rows <= 0:
            continue
        if task_size <= 0:
            num_tasks += 1
        else:
            # ceil_div
            num_tasks += -(frag_rows // -task_size)
    report_plan_progress(job_tracker, n=_plan_total)

    def task_gen() -> Iterator[CopyTask]:
        for frag in dst_dataset.get_fragments():
            # Skip fragments that don't match the filter
            if (
                only_fragment_ids is not None
                and frag.fragment_id not in only_fragment_ids
            ):
                continue
            frag_rows = frag.count_rows()
            if frag_rows <= 0:
                continue
            src_files_hash = None
            if src_data_files_by_dst is not None:
                src_files = src_data_files_by_dst.get(frag.fragment_id)
                if src_files is not None:
                    src_files_hash = hash_source_files(src_files)
            if task_size <= 0:
                offsets_and_limits = [(0, 0)]
            else:
                offsets_and_limits = [
                    (offset, min(task_size, frag_rows - offset))
                    for offset in range(0, frag_rows, task_size)
                ]
            for offset, limit in offsets_and_limits:
                yield CopyTask(
                    src=src,
                    dst=dst,
                    columns=columns,
                    frag_id=frag.fragment_id,
                    offset=offset,
                    limit=limit,
                    src_files_hash=src_files_hash,
                    src_data_files=(
                        None
                        if src_data_files_by_dst is None
                        else src_data_files_by_dst.get(frag.fragment_id)
                    ),
                    fragment_physical_rows=frag.physical_rows,
                    fragment_logical_rows=frag_rows,
                )

    return (task_gen(), num_tasks)


def plan_copy(
    src: TableReference,
    dst: TableReference,
    columns: list[str] | dict[str, str],
    *,
    task_size: int | None = None,
    batch_size: int = DEFAULT_CHECKPOINT_ROWS,
    shuffle_buffer_size: int = 0,
    task_shuffle_diversity: int | None = None,
    only_fragment_ids: set[int] | None = None,
    src_data_files_by_dst: dict[int, frozenset[str]] | None = None,
    job_tracker: Any = None,
    **unused_kwargs,
) -> Iterator[CopyTask]:
    # `batch_size` historically controlled read-task sizing in these planners.
    # Keep it as a backwards-compatible alias for `task_size`.
    if (
        task_size is not None
        and batch_size != DEFAULT_CHECKPOINT_ROWS
        and batch_size != task_size
    ):
        _LOG.warning(
            "plan_copy(batch_size=%s) overrides task_size=%s; "
            "use task_size going forward.",
            batch_size,
            task_size,
        )
    effective_task_size = batch_size if task_size is None else task_size

    (it, num_tasks) = _plan_copy(
        src,
        dst,
        columns,
        task_size=effective_task_size,
        only_fragment_ids=only_fragment_ids,
        src_data_files_by_dst=src_data_files_by_dst,
        job_tracker=job_tracker,
    )
    # same as no shuffle
    if shuffle_buffer_size > 1 and task_shuffle_diversity is None:
        it = _buffered_shuffle(it, buffer_size=shuffle_buffer_size)
    elif task_shuffle_diversity is not None:
        buffer_size = max(4 * task_shuffle_diversity, shuffle_buffer_size)
        it = diversity_aware_shuffle(
            it,
            key=lambda task: task.checkpoint_key(),
            diversity_goal=task_shuffle_diversity,
            buffer_size=buffer_size,
        )

    return _LanceReadPlanIterator(it, num_tasks)
