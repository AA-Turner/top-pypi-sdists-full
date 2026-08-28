# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import json
import logging
import os
import time
import urllib
import urllib.parse
import uuid
from collections.abc import Callable, Iterator
from typing import Any, Optional, cast

import attrs
import lance
import lance.file
import pyarrow as pa
import pyarrow.compute as pc
import ray
import ray.actor
import ray.util.queue
from yarl import URL

from geneva.apply.memory import release_unused_process_memory
from geneva.checkpoint import (
    CheckpointStore,
    read_checkpoint_num_rows,
    strip_checkpoint_num_rows,
)
from geneva.db import NamespaceConfig, _directory_namespace_storage_properties
from geneva.errors import CheckpointCoverageError, ShortFragmentWriteError
from geneva.fragment_writer import get_fragment_file_writer
from geneva.runners.ray.naming import ray_name
from geneva.utils import (
    get_null_value_for_type,
    make_null_array,
    parse_data_storage_version,
    redact_dict_values,
)
from geneva.utils.parse_rust_debug import extract_field_ids_and_column_indices
from geneva.utils.schema import resolve_arrow_field_path
from geneva.utils.sequence_queue import SequenceQueue

_LOG = logging.getLogger(__name__)

# Row count per tranche when streaming the OLD output column for deferred
# carry-forward. Each tranche materializes that many old blob values
# at once, AND drives one coalesced range read, so too-small wastes round-trips
# on large blobs (64 rows x 150 KB = ~16k reads/fragment at 100M scale) while
# too-large grows the resident set. 1024 balances both for typical image blobs;
# tune per workload via the env var. (Row count is a crude proxy for bytes —
# see the follow-up to make this a byte-target knob.)
DEFAULT_CARRY_FORWARD_TRANCHE_ROWS = int(
    os.environ.get("GENEVA_CARRY_FORWARD_TRANCHE_ROWS", "1024")
)


class FragmentWriteFailedError(RuntimeError):
    """One or more fragments failed to write and the job must not report success.

    The healthy fragments' commits are preserved and the failed fragments'
    checkpoints survive, so a re-run picks up where this job left off.
    """


@attrs.define(frozen=True)
class FragmentWriteResult:
    frag_id: int
    new_file: lance.fragment.DataFile
    rows_written: int
    checkpoint_written: bool = False
    fragment_checkpointing_ms: int = 0
    buffer_sort_ms: int = 0
    align_ms: int = 0
    write_ms: int = 0
    queue_wait_ms: int = 0
    checkpoint_read_ms: int = 0
    avg_batch_num_rows: int = 0
    avg_batch_size: int = 0


@attrs.define(frozen=True)
class WriterProgress:
    """Monotonic liveness snapshot served by ``FragmentWriter.progress()``.

    ``seq`` bumps on every unit of work (checkpoint read, batch written); the
    drain loop treats a frozen ``seq`` (not an unresolved write future) as
    the stall signal.
    """

    seq: int = 0
    phase: str = "init"  # "start" | "sort" | "write" | "finalize"
    checkpoints_read: int = 0
    batches_out: int = 0
    rows_out: int = 0


def _record_batch_size_bytes(batch: pa.RecordBatch) -> int:
    return int(batch.nbytes)  # type: ignore[attr-defined]


def build_fragment_checkpoint_batch(
    *,
    file_path: str,
    src_data_files: frozenset[str] | None = None,
    output_field_ids: frozenset[int] | None = None,
    udf_version: str | None = None,
    base_id: int | None = None,
) -> pa.RecordBatch:
    checkpoint_data: dict[str, list[object]] = {"file": [file_path]}
    if src_data_files is not None:
        checkpoint_data["src_data_files"] = [json.dumps(sorted(src_data_files))]
    if output_field_ids is not None:
        checkpoint_data["output_field_ids"] = [json.dumps(sorted(output_field_ids))]
    if udf_version is not None:
        checkpoint_data["udf_version"] = [udf_version]
    if base_id is not None:
        # Storage base holding the staged file (multi-base datasets). Absent
        # for files staged under the dataset root.
        checkpoint_data["base_id"] = [base_id]
    return pa.RecordBatch.from_pydict(checkpoint_data)


def _fill_rowaddr_gaps(batch: pa.RecordBatch) -> pa.RecordBatch:
    """
    This fills the gaps in the _rowaddr column of the batch.
    It assumes that the _rowaddr column is present and sorted.
    It will fill in the gaps with None values for other columns.

    example: start with rowaddr [1, 3], values [10, 30]
    returns rowaddr [1, 2, 3], values [10, None, 30]
    """
    if "_rowaddr" not in batch.schema.names:
        raise ValueError(
            "No _rowaddr column found in the batch,"
            " please make sure the scanner is configured with with_row_address=True"
        )

    rowaddr: pa.Array = batch["_rowaddr"]

    rowaddr_start = rowaddr[0].as_py()
    rowaddr_end = rowaddr[-1].as_py()

    num_physical_rows_in_range = rowaddr_end - rowaddr_start + 1

    if num_physical_rows_in_range == batch.num_rows:
        return batch

    # TODO: this is inefficient in python, do it in rust
    data_dict = {
        "_rowaddr": pa.array(range(rowaddr_start, rowaddr_end + 1), type=pa.uint64()),
    }
    for name in batch.schema.names:
        if name == "_rowaddr":
            continue

        arr = batch[name]

        # Build list with gaps filled with appropriate null values.
        #
        # IMPORTANT: We use explicit list collection rather than a
        # generator/iterator approach for creating PyArrow arrays. This ensures
        # PyArrow constructs arrays with proper buffer structure for
        # variable-width types (strings, binary, lists).
        #
        # Variable-width types require multiple buffers:
        # - Strings: validity bitmap + offsets buffer + data buffer
        # - Lists: validity bitmap + offsets buffer + child array buffers
        #
        # When creating arrays from iterators, PyArrow may apply optimizations
        # that create malformed arrays incompatible with LanceDB's buffer
        # validation. LanceDB/Rust requires proper buffer structure even for
        # null-heavy arrays.
        #
        # Using explicit list collection ensures consistent, predictable array
        # construction that passes LanceDB validation when written to Lance
        # format.
        #
        # For struct types, we currently emit structs whose child fields are
        # null (instead of null structs). Lance 2.1 accepts either form, but we
        # mirror Lance 2.0 behavior because downstream Geneva tests and
        # pipelines rely on observing null-at-field granularity.
        null_value = get_null_value_for_type(arr.type)
        result_list = []
        next_idx = rowaddr_start
        for val, row_addr in zip(
            batch[name].to_pylist(), rowaddr.to_pylist(), strict=False
        ):
            while next_idx < row_addr:
                result_list.append(null_value)
                next_idx += 1
            result_list.append(val)
            next_idx += 1

        # Create array using pa.table() to ensure proper buffer structure
        # for variable-width types (strings, binary, lists).
        # See task.py for similar fix and explanation.
        temp_table = pa.table(
            {"_temp": result_list},
            schema=pa.schema([("_temp", arr.type)]),
        )
        data_dict[name] = temp_table.column("_temp").combine_chunks()  # type: ignore[assignment]

    return batch.from_pydict(data_dict, schema=batch.schema)


def _parse_span_from_key(checkpoint_key: str) -> int | None:
    """Extract the row-span size from a ``_range-START-END`` key suffix.

    Returns the span (``end - start``) when the key carries the suffix
    and parses cleanly, or ``None`` for legacy/malformed keys.  Knowing
    the span up front lets the writer enqueue an out-of-order
    checkpoint as a small key reference rather than loading the full
    record batch into memory.
    """
    if "_range-" not in checkpoint_key:
        return None
    try:
        suffix = checkpoint_key.rsplit("_range-", 1)[1]
        start_str, end_str = suffix.split("-", 1)
        start = int(start_str)
        end = int(end_str)
        if end > start:
            return end - start
    except Exception as exc:
        _LOG.debug(
            "Failed to parse span from checkpoint key %s: %s",
            checkpoint_key,
            exc,
            exc_info=True,
        )
    return None


def _parse_range_start_from_key(checkpoint_key: str) -> int | None:
    """Extract the START offset from a ``_range-START-END`` key suffix.

    Lets the deferred carry-forward merge order matched checkpoint files and
    activate them lazily by their range *without reading the data*. Returns
    ``None`` for legacy/malformed keys (the caller then treats the run as always
    active, reading it eagerly).
    """
    if "_range-" not in checkpoint_key:
        return None
    try:
        suffix = checkpoint_key.rsplit("_range-", 1)[1]
        return int(suffix.split("-", 1)[0])
    except Exception:
        return None


@attrs.define(frozen=True)
class _PendingCheckpoint:
    """Lightweight reference to a checkpoint blob in the store.

    Held in the writer's ``SequenceQueue`` instead of the full
    ``pa.RecordBatch`` so out-of-order arrivals don't pin GBs of UDF
    output in memory while waiting for the next-expected position.
    The data is fetched from the store at pop time.

    ``expected_rows`` is the producer's recorded ``MapBatchCheckpoint.num_rows``
    (the materialized physical row count); the read-back is validated against it
    to catch a short/truncated checkpoint file. ``-1`` means the producer count
    was not threaded through the queue (e.g. partial-recovery re-ingest); the
    validation then falls back to the count stamped in the batch's schema
    metadata, or is skipped for a legacy unstamped checkpoint.
    """

    key: str
    expected_rows: int = -1


def _validate_checkpoint_rows(
    store: CheckpointStore, key: str, batch: pa.RecordBatch, expected_rows: int
) -> None:
    """Reject a short/truncated checkpoint file read back from the store.

    The producer records the materialized row count for each batch checkpoint. If
    the read-back batch holds fewer rows the file was only partially written, and
    null-filling the missing tail would silently persist NULLs. Delete the poisoned
    key so a resume recomputes the batch instead of re-reading the short file, then
    raise so the fragment write fails loudly.

    When ``expected_rows`` is ``-1`` the producer count is unknown; fall back to
    the count stamped in the batch's schema metadata (written by the producer, and
    preserved by slice/round-trip even when the file landed short). A legacy
    checkpoint with neither count cannot be validated and is accepted as-is.
    """
    _validate_checkpoint_row_count(
        store,
        key,
        actual_rows=batch.num_rows,
        expected_rows=expected_rows,
        metadata_batch=batch,
    )


def _validate_checkpoint_row_count(
    store: CheckpointStore,
    key: str,
    *,
    actual_rows: int,
    expected_rows: int,
    metadata_batch: pa.RecordBatch | None,
) -> None:
    """Validate an aggregate row count after one or more bounded reads."""
    if expected_rows < 0 and metadata_batch is not None:
        stamped = read_checkpoint_num_rows(metadata_batch)
        if stamped is not None:
            expected_rows = stamped
    if expected_rows < 0 or actual_rows == expected_rows:
        return
    try:
        store.delete(key)
    except Exception:
        _LOG.exception("Failed to invalidate short checkpoint %s", key)
    raise ValueError(
        f"checkpoint {key} holds {actual_rows} rows, expected {expected_rows}; "
        "the checkpoint file is short/truncated and has been invalidated so a "
        "resume recomputes it"
    )


def _read_checkpoint_batches(
    store: CheckpointStore,
    key: str,
    expected_rows: int,
    *,
    max_rows_per_batch: int | None,
    _on_read: Callable[[pa.RecordBatch, int, bool, bool], None] | None = None,
) -> Iterator[pa.RecordBatch]:
    """Read one checkpoint, optionally as true bounded Lance ranges.

    A recovered writer supplies ``max_rows_per_batch``. In that mode this must
    use :meth:`CheckpointStore.read_range` rather than loading the full batch and
    slicing it: Arrow slices retain the original backing buffers and therefore do
    not reduce the writer's resident working set.
    """
    if max_rows_per_batch is None:
        read_start = time.perf_counter()
        batch = store[key]
        elapsed_ms = int((time.perf_counter() - read_start) * 1000)
        _validate_checkpoint_rows(store, key, batch, expected_rows)
        if _on_read is not None:
            _on_read(batch, elapsed_ms, True, True)
        yield batch
        return

    if max_rows_per_batch <= 0:
        raise ValueError("max_rows_per_batch must be positive")

    offset = 0
    first_batch: pa.RecordBatch | None = None
    while True:
        read_start = time.perf_counter()
        batch = store.read_range(key, offset, max_rows_per_batch)
        elapsed_ms = int((time.perf_counter() - read_start) * 1000)
        if first_batch is None:
            first_batch = batch
        # Preserve the schema-bearing empty batch for a genuine zero-row
        # checkpoint. An empty tail read is only a termination signal.
        if batch.num_rows == 0:
            if _on_read is not None:
                _on_read(batch, elapsed_ms, offset == 0, offset == 0)
            if offset == 0:
                yield batch
            break

        if _on_read is not None:
            _on_read(batch, elapsed_ms, True, offset == 0)
        yield batch
        offset += batch.num_rows

        stamped_rows = (
            read_checkpoint_num_rows(first_batch) if first_batch is not None else None
        )
        target_rows = expected_rows if expected_rows >= 0 else stamped_rows
        if target_rows is not None and offset >= target_rows:
            if offset == target_rows and batch.num_rows == max_rows_per_batch:
                # Exact tranche boundaries need an EOF probe. Otherwise a
                # checkpoint with an unexpected extra tail (for example 7 rows
                # with expected=6 and cap=3) would be silently accepted after
                # reading only the expected prefix. Count an invalid tail with
                # bounded reads, but never yield it to the fragment writer.
                while True:
                    probe_start = time.perf_counter()
                    probe = store.read_range(key, offset, max_rows_per_batch)
                    probe_ms = int((time.perf_counter() - probe_start) * 1000)
                    if _on_read is not None:
                        _on_read(probe, probe_ms, False, False)
                    if probe.num_rows == 0:
                        break
                    offset += probe.num_rows
                    if probe.num_rows < max_rows_per_batch:
                        break
            break
        if batch.num_rows < max_rows_per_batch:
            break

    _validate_checkpoint_row_count(
        store,
        key,
        actual_rows=offset,
        expected_rows=expected_rows,
        metadata_batch=first_batch,
    )


def _bump_checkpoint_read_progress(
    progress: Callable[..., None] | None, *, first_read: bool
) -> None:
    """Advance liveness per range read but count each checkpoint only once."""
    if progress is None:
        return
    if first_read:
        progress("sort", checkpoints_read=1)
    else:
        progress("sort")


def _buffer_and_sort_batches(
    num_rows: int,
    frag_id: int,
    filler_schema: pa.Schema | None,
    store: CheckpointStore,
    queue: ray.util.queue.Queue,
    *,
    _timing: dict[str, int] | None = None,
    _batch_stats: dict[str, int] | None = None,
    _progress: Callable[..., None] | None = None,
    keys_only: bool = False,
    expect_full_coverage: bool = False,
    max_rows_per_batch: int | None = None,
) -> Iterator[pa.RecordBatch | _PendingCheckpoint]:
    """
    buffer batches from the queue, which is yields a tuple of
    * serial number of the batch -- currently the offset of the batch
    * the data key dict of the batch

    serial number can arrive out of order, so we need to buffer them
    until we have the next expected serial number. In most cases, the
    serial number is the offset of the batch, and we keep track of the
    expected serial number in the variable `next_position` (tracked by
    `SequenceQueue`).

    The SequenceQueue ordering is based on the ReadTask offsets (the same domain
    as ``ScanTask.offset`` / ``ScanTask.limit``). For Lance fragments with deletes,
    this corresponds to the fragment's **logical** row offsets (i.e., after
    deletions). Physical gaps are recovered later using the `_rowaddr` column in
    `_align_batches_to_physical_layout`.

    Memory note: when a checkpoint key carries the ``_range-START-END``
    suffix the row span is known up front, so the writer enqueues a
    small ``_PendingCheckpoint`` reference and defers the
    ``store[key]`` read until the item is ready to yield.  This keeps
    the writer's working set bounded to ~references rather than the
    full UDF output, which matters when many out-of-order checkpoints
    pile up under multi-applier workloads.  Legacy/malformed keys
    without the suffix fall back to the eager-read path so we can
    learn ``stored.num_rows`` for ``SequenceQueue`` accounting.

    ``expect_full_coverage``: every row must be covered by a checkpoint
    span by seal time, so a coverage gap raises
    :class:`CheckpointCoverageError` instead of silently null-filling
    rows whose UDF output was dropped upstream (GEN-744 follow-up). The
    backfill pipeline always satisfies this — WHERE filters are applied
    as a selection column, so checkpoint spans tile every task window —
    and ``FragmentWriter.write`` passes True. The flag-off gap filling
    is kept for direct callers that feed partial coverage on purpose.
    """
    queue_wait_ms = 0
    checkpoint_read_ms = 0

    if keys_only:
        # Deferred carry-forward needs only the matched checkpoint *references*,
        # not materialized data: drain the queue collecting one ``_PendingCheckpoint``
        # per matched file until the seal sentinel. Order and gaps don't matter
        # here — the downstream ``MatchStream`` orders runs by their peeked key
        # range and reads each file lazily, and a missing matched checkpoint just
        # leaves those rows at their carried-forward old value. Reuses the same
        # seal-sentinel / actor-death handling as the materializing path.
        try:
            sealed = False
            while not sealed:
                try:
                    wait_start = time.perf_counter()
                    item = queue.get()
                    queue_wait_ms += int((time.perf_counter() - wait_start) * 1000)
                except (
                    ray.exceptions.ActorDiedError,  # type: ignore[attr-defined]
                    ray.exceptions.ActorUnavailableError,  # type: ignore[attr-defined]
                ):
                    _LOG.exception(
                        "Writer failed to read from checkpoint queue, exiting"
                    )
                    ray.actor.exit_actor()
                    return
                if item[0] < 0:  # in-band seal sentinel
                    sealed = True
                    break
                if _progress is not None:
                    _progress("sort")
                yield _PendingCheckpoint(item[1], item[2])
        finally:
            if _timing is not None:
                _timing["queue_wait_ms"] += int(queue_wait_ms)
        return

    assert filler_schema is not None, "filler_schema is required unless keys_only"
    accumulation_queue: SequenceQueue[pa.RecordBatch | _PendingCheckpoint] = (
        SequenceQueue()
    )
    sealed = False

    def _note_checkpoint_read(
        batch: pa.RecordBatch,
        elapsed_ms: int,
        contributes_batch: bool,
        first_read: bool,
    ) -> None:
        nonlocal checkpoint_read_ms
        checkpoint_read_ms += elapsed_ms
        _bump_checkpoint_read_progress(_progress, first_read=first_read)
        if contributes_batch and _batch_stats is not None:
            _batch_stats["num_batches"] += 1
            _batch_stats["total_rows"] += int(batch.num_rows)
            _batch_stats["total_bytes"] += _record_batch_size_bytes(batch)

    def _materialize(
        item: pa.RecordBatch | _PendingCheckpoint,
    ) -> Iterator[pa.RecordBatch]:
        if isinstance(item, _PendingCheckpoint):
            yield from _read_checkpoint_batches(
                store,
                item.key,
                item.expected_rows,
                max_rows_per_batch=max_rows_per_batch,
                _on_read=_note_checkpoint_read,
            )
        else:
            yield item

    try:
        while accumulation_queue.next_position() < num_rows:
            # Pump the input until we have the next batch
            while (
                accumulation_queue.next_position() < num_rows
                and accumulation_queue.is_empty()
            ):
                if sealed:
                    gap_start = accumulation_queue.next_position()
                    gap_end = accumulation_queue.next_buffered_position()
                    if gap_end is None:
                        gap_end = num_rows
                    gap_end = min(int(gap_end), int(num_rows))
                    if gap_end > gap_start and expect_full_coverage:
                        raise CheckpointCoverageError(
                            frag_id, gap_start=gap_start, gap_end=gap_end
                        )
                    if gap_end > gap_start:
                        fill_start = (frag_id << 32) | gap_start
                        fill_end = (frag_id << 32) | gap_end
                        filler = _make_filler_batch(fill_start, fill_end, filler_schema)
                        accumulation_queue.put(gap_start, gap_end - gap_start, filler)
                        break
                try:
                    wait_start = time.perf_counter()
                    batch: tuple[int, str, int] = queue.get()
                    queue_wait_ms += int((time.perf_counter() - wait_start) * 1000)
                except (
                    ray.exceptions.ActorDiedError,  # type: ignore[attr-defined]
                    ray.exceptions.ActorUnavailableError,  # type: ignore[attr-defined]
                ):
                    _LOG.exception(
                        "Writer failed to read from checkpoint queue, exiting"
                    )
                    ray.actor.exit_actor()
                    return  # Unreachable, but makes pyright happy

                # A negative offset is used as an in-band signal that no more
                # checkpoints will be enqueued for this fragment.
                if batch[0] < 0:
                    sealed = True
                    continue
                if _progress is not None:
                    _progress("sort")

                checkpoint_key = batch[1]
                expected_rows = batch[2]
                next_expected = accumulation_queue.next_position()
                if batch[0] < next_expected:
                    # Identifies the producer of duplicate/overlapping
                    # coverage (GEN-744 acceptance: key + positions).
                    _LOG.warning(
                        "Checkpoint %s arrived at offset %d behind the queue "
                        "cursor %d; already-covered rows will be dropped or "
                        "trimmed",
                        checkpoint_key,
                        batch[0],
                        next_expected,
                    )
                # Note: For deletes, checkpoint spans are in the logical-row
                # domain (after deletes). Physical alignment is handled
                # downstream via _rowaddr.
                span = _parse_span_from_key(checkpoint_key)
                if span is not None:
                    # Checkpoint recovery can enqueue a straddling checkpoint
                    # at an offset inside its key range; only the tail from
                    # the offset still contributes rows. Claiming the key's
                    # full span would overshoot the queue cursor past later
                    # checkpoints and stall the drain (GEN-744).
                    range_start = _parse_range_start_from_key(checkpoint_key)
                    if range_start is not None:
                        span = range_start + span - batch[0]
                    if span <= 0:
                        _LOG.warning(
                            "Skipping checkpoint %s enqueued at offset %d: "
                            "its range is entirely behind the offset",
                            checkpoint_key,
                            batch[0],
                        )
                        continue
                    # Defer the heavy read: just enqueue a small reference.
                    # batch_stats counters that need stored.num_rows /
                    # batch bytes are deferred to materialize-at-pop too.
                    accumulation_queue.put(
                        batch[0],
                        span,
                        _PendingCheckpoint(checkpoint_key, expected_rows),
                    )
                elif max_rows_per_batch is not None and expected_rows >= 0:
                    # Recovery can also bound legacy keys when the producer's
                    # materialized row count provides SequenceQueue accounting.
                    accumulation_queue.put(
                        batch[0],
                        expected_rows,
                        _PendingCheckpoint(checkpoint_key, expected_rows),
                    )
                else:
                    # Legacy/malformed key: must read eagerly so we can
                    # learn the row count for SequenceQueue accounting.
                    read_start = time.perf_counter()
                    stored = store[checkpoint_key]
                    checkpoint_read_ms += int((time.perf_counter() - read_start) * 1000)
                    _validate_checkpoint_rows(
                        store, checkpoint_key, stored, expected_rows
                    )
                    if _progress is not None:
                        _progress("sort", checkpoints_read=1)
                    if _batch_stats is not None:
                        _batch_stats["num_batches"] += 1
                        _batch_stats["total_rows"] += int(stored.num_rows)
                        _batch_stats["total_bytes"] += _record_batch_size_bytes(stored)
                    accumulation_queue.put(batch[0], stored.num_rows, stored)

            # Return the next batch (and any other freed batches).  Pending
            # references are materialized here, just before yield.
            while not accumulation_queue.is_empty():
                pending = accumulation_queue.pop()
                if pending is None:
                    continue
                yield from _materialize(pending)
    finally:
        if _timing is not None:
            _timing["queue_wait_ms"] += int(queue_wait_ms)
            _timing["checkpoint_read_ms"] += int(checkpoint_read_ms)


def _make_filler_batch(
    fill_start: int,
    fill_end: int,
    schema: pa.Schema,
) -> pa.RecordBatch:
    """
    make a batch that fills the range [fill_start, fill_end) with null values
    for all columns except _rowaddr, which will be filled with the range.
    Note: fill_end is exclusive, so the batch will have (fill_end - fill_start) rows.

    For struct types, creates structs whose child fields are null (not null
    structs). The Lance 2.1 writer handles either encoding, but Geneva's
    historical expectations (written against Lance 2.0) assume per-field nulls,
    so we preserve that behavior for now.
    """
    _LOG.info(f"Filling range: {fill_start} -- {fill_end}")
    rowaddr_arr = pa.array(range(fill_start, fill_end), type=pa.uint64())
    # Use make_null_array() to create proper null arrays for each type.
    #
    # For non-struct types, this uses pa.nulls() which creates arrays with
    # proper buffer structure for variable-width types (strings, binary, lists).
    #
    # For struct types, make_null_array() generates structs whose child fields
    # are null so that downstream consumers keep seeing Lance 2.0-style
    # semantics. Revisit if we decide null structs are acceptable everywhere.
    n = fill_end - fill_start
    data_dict = {
        name: make_null_array(n, schema.field(name).type)
        for name in schema.names
        if name != "_rowaddr"
    }
    data_dict["_rowaddr"] = rowaddr_arr
    return pa.RecordBatch.from_pydict(data_dict, schema=schema)


def _make_filler_batches(
    fill_start: int,
    fill_end: int,
    schema: pa.Schema,
    max_rows_per_batch: int | None,
) -> Iterator[pa.RecordBatch]:
    """Yield a filler range without exceeding the recovered writer row cap."""
    if max_rows_per_batch is None:
        yield _make_filler_batch(fill_start, fill_end, schema)
        return
    if max_rows_per_batch <= 0:
        raise ValueError("max_rows_per_batch must be positive")
    cursor = fill_start
    while cursor < fill_end:
        chunk_end = min(fill_end, cursor + max_rows_per_batch)
        yield _make_filler_batch(cursor, chunk_end, schema)
        cursor = chunk_end


def _split_batch_by_physical_span(
    batch: pa.RecordBatch,
    max_rows_per_batch: int | None,
) -> Iterator[pa.RecordBatch]:
    """Split before gap filling so one sparse batch cannot expand past the cap."""
    if max_rows_per_batch is None or batch.num_rows <= 1:
        yield batch
        return
    if max_rows_per_batch <= 0:
        raise ValueError("max_rows_per_batch must be positive")

    rowaddrs = cast("list[int]", batch["_rowaddr"].to_pylist())
    begin = 0
    span_start = rowaddrs[0]
    for pos in range(1, batch.num_rows):
        if rowaddrs[pos] - span_start + 1 <= max_rows_per_batch:
            continue
        yield batch.slice(begin, pos - begin)
        begin = pos
        span_start = rowaddrs[pos]
    yield batch.slice(begin)


def _filter_columns_to_schema(
    batches: Iterator[pa.RecordBatch],
    target_column_names: list[str],
) -> Iterator[pa.RecordBatch]:
    """
    Filter batches to only include columns that are in the target schema.

    This is necessary because the input batches may contain columns from the
    source table that are not part of the materialized view's selected columns.
    For example, if the source table has [id, title, width, height] but the
    materialized view only selects [title], the batches from the UDF application
    will still contain all source columns. We must filter to only the target
    columns before writing to Lance.

    IMPORTANT: This must be done AFTER all UDF processing and gap filling, but
    BEFORE writing to Lance, to ensure the written data matches the target schema.

    Parameters
    ----------
    batches : Iterator[pa.RecordBatch]
        Input batches that may contain extra columns
    target_column_names : list[str]
        Names of columns that should be in the output (including _rowaddr)

    Yields
    ------
    pa.RecordBatch
        Batches filtered to only contain target columns, in the order specified
        by target_column_names
    """
    for batch in batches:
        # Filter to only columns in target schema, preserving order
        # Always include _rowaddr if present
        columns_to_keep = [
            col for col in target_column_names if col in batch.schema.names
        ]
        if "_rowaddr" in batch.schema.names and "_rowaddr" not in columns_to_keep:
            columns_to_keep.append("_rowaddr")

        # Select only the columns we want, which creates a new batch
        filtered_batch = batch.select(columns_to_keep)
        yield filtered_batch


def write_fragment_file(
    uri: str,
    batches: Iterator[pa.RecordBatch],
    *,
    column_names: list[str],
    field_ids: list[int],
    column_indices: list[int],
    data_storage_version: str,
    filter_columns: bool = True,
    namespace_impl: str | None = None,
    namespace_properties: dict[str, str] | None = None,
    table_id: list[str] | None = None,
    storage_options: dict[str, str] | None = None,
    data_dir: str | None = None,
    base_id: int | None = None,
    data_file_name: str | None = None,
) -> tuple[lance.fragment.DataFile, int, int]:
    """Stage one fragment output file and return its ``DataFile``.

    ``data_dir``/``base_id`` place the file in a specific storage base of a
    multi-base dataset; by default the file lands under ``{uri}/data`` (the
    dataset root, ``base_id`` absent).
    """
    import more_itertools

    batches_to_write = (
        _filter_columns_to_schema(batches, column_names) if filter_columns else batches
    )
    # Strip the resume-only row-count stamp so it doesn't leak into the committed
    # fragment's file schema (the writer derives that schema from these batches).
    batches_to_write = (strip_checkpoint_num_rows(b) for b in batches_to_write)
    peekable_batches = more_itertools.peekable(batches_to_write)

    if data_file_name is None:
        data_file_name = f"{uuid.uuid4()}.lance"
    elif "/" in data_file_name or data_file_name in ("", ".", ".."):
        raise ValueError(f"invalid data file name: {data_file_name!r}")
    resolved_data_dir = data_dir if data_dir else str(URL(uri) / "data")
    path = str(URL(resolved_data_dir) / data_file_name)
    if not urllib.parse.urlparse(resolved_data_dir).scheme:
        path = f"file://{os.path.abspath(path)}"

    try:
        schema = peekable_batches.peek().schema
    except StopIteration as exc:
        raise ValueError("No batches found") from exc

    namespace_client = None
    resolved_storage_options = storage_options
    if namespace_impl and namespace_properties and table_id:
        namespace_client = NamespaceConfig(
            namespace_client_impl=namespace_impl,
            namespace_client_properties=namespace_properties,
        ).connect_namespace_client(use_worker_props=True)
        assert namespace_client is not None
        if resolved_storage_options is None:
            from lance_namespace import DescribeTableRequest

            response = namespace_client.describe_table(
                DescribeTableRequest(id=table_id)
            )
            resolved_storage_options = response.storage_options

    rows_written = 0
    writer_write_ms = 0
    writer_cm = lance.file.LanceFileWriter(
        path,
        schema,
        storage_options=resolved_storage_options,
        namespace_client=namespace_client,
        table_id=table_id,
        version=data_storage_version,
    )
    t0 = time.perf_counter()
    writer = writer_cm.__enter__()
    writer_write_ms += int((time.perf_counter() - t0) * 1000)
    exc_info: tuple[object | None, object | None, object | None] = (None, None, None)
    try:
        for batch in peekable_batches:
            t1 = time.perf_counter()
            writer.write_batch(batch)
            writer_write_ms += int((time.perf_counter() - t1) * 1000)
            rows_written += batch.num_rows
    except BaseException as exc:
        exc_info = (type(exc), exc, exc.__traceback__)
        raise
    finally:
        t1 = time.perf_counter()
        writer_cm.__exit__(*exc_info)
        writer_write_ms += int((time.perf_counter() - t1) * 1000)
        # Release allocator drift accumulated across this fragment's batches.
        # Arrow's mempool and libc's malloc retain freed pages without an
        # explicit trim, and a fragment's batches can strand a lot of them.
        #
        # This bounds RSS *within* a fragment, not across many: a
        # FragmentWriter actor is spawned per fragment and killed when its
        # session shuts down (``pipeline.py`` ``_session_for_frag`` /
        # ``ray.kill``), so drift the trim misses is reclaimed by the OS when
        # the actor dies. Appliers are the long-lived side — they serve every
        # ReadTask of a job, which is why their trim counter is applier-owned.
        release_unused_process_memory()

    dsv_major, dsv_minor = parse_data_storage_version(data_storage_version)
    data_file = lance.fragment.DataFile(
        data_file_name,
        field_ids,
        column_indices,
        dsv_major,
        dsv_minor,
        base_id=base_id,
    )
    return data_file, rows_written, int(writer_write_ms)


def _align_batches_to_physical_layout(
    num_physical_rows: int,
    num_logical_rows: int,
    frag_id: int,
    batches: Iterator[pa.RecordBatch],
    *,
    _timing: dict[str, int] | None = None,
    expect_full_coverage: bool = False,
    max_rows_per_batch: int | None = None,
) -> Iterator[pa.RecordBatch]:
    """
    This aligns the batches to the physical rows layout.

    It will fill in the _rowaddr gaps within a batch with new rows with the _rowaddr
    index values and None values for the other columns.  It will also fill the _rowaddr
    gaps between batches with the _rowaddr index values and None values for the other
    cols.

    ``expect_full_coverage``: every live row must arrive from upstream, so
    dropped output raises instead of committing nulls. On fragments without
    deletes (``num_physical_rows == num_logical_rows``) any filler is
    immediately fatal. On fragments with deletion vectors filler is
    legitimate for deleted rows, so the guard is a row-count invariant
    instead: the stream must deliver exactly ``num_logical_rows`` real
    (non-filler, non-trimmed-duplicate) rows, i.e. filler covers only the
    ``num_physical_rows - num_logical_rows`` deleted slots.
    """

    if num_logical_rows > num_physical_rows:
        raise ValueError(
            "Logical rows should be greater than or equal to physical rows"
        )

    fail_on_fill = expect_full_coverage and num_physical_rows == num_logical_rows
    real_rows_total = 0

    next_batch_rowaddr = 0

    schema = None

    align_ms = 0

    def _timed_fill(
        fill_start: int, fill_end: int, fill_schema: pa.Schema
    ) -> Iterator[pa.RecordBatch]:
        nonlocal align_ms
        fillers = iter(
            _make_filler_batches(fill_start, fill_end, fill_schema, max_rows_per_batch)
        )
        while True:
            t_fill = time.perf_counter()
            try:
                filler = next(fillers)
            except StopIteration:
                return
            align_ms += int((time.perf_counter() - t_fill) * 1000)
            yield filler

    it = (
        bounded
        for raw in batches
        for bounded in _split_batch_by_physical_span(raw, max_rows_per_batch)
    )
    while True:
        try:
            raw_batch = next(it)
        except StopIteration:
            break

        t0 = time.perf_counter()
        batch = _fill_rowaddr_gaps(raw_batch)
        if fail_on_fill and batch.num_rows != raw_batch.num_rows:
            gap_start = int(raw_batch["_rowaddr"][0].as_py()) & 0xFFFFFFFF
            gap_end = int(raw_batch["_rowaddr"][-1].as_py()) & 0xFFFFFFFF
            raise CheckpointCoverageError(frag_id, gap_start=gap_start, gap_end=gap_end)
        if expect_full_coverage:
            # Real rows this batch contributes: upstream rows minus any
            # already-written prefix the trim below will drop.
            raw_first = int(raw_batch["_rowaddr"][0].as_py()) & 0xFFFFFFFF
            if raw_first >= next_batch_rowaddr:
                real_rows_total += raw_batch.num_rows
            else:
                local = pc.bit_wise_and(
                    raw_batch["_rowaddr"], pa.scalar(0xFFFFFFFF, type=pa.uint64())
                )
                kept = pc.sum(
                    pc.greater_equal(
                        local, pa.scalar(next_batch_rowaddr, type=pa.uint64())
                    ).cast(pa.int64())
                ).as_py()
                real_rows_total += int(kept or 0)
        t1 = time.perf_counter()
        # skim the schema from the stream
        # we expect at least one batch, otherwise the whole fragment has been
        # deleted and the metadata would have been deleted by lance so we wouldn't
        # be here because no writer would be created
        if schema is None:
            schema = batch.schema

        incoming_local_rowaddr = batch["_rowaddr"][0].as_py() & 0xFFFFFFFF
        if incoming_local_rowaddr < next_batch_rowaddr:
            # Overlapping coverage (e.g. checkpoints written by runs with
            # different task grids): the leading rows were already emitted.
            # Trim them; skip the batch entirely when nothing new remains.
            skip = next_batch_rowaddr - incoming_local_rowaddr
            _LOG.warning(
                "Batch for fragment %s starts at row %d but rows up to %d "
                "were already written; trimming %d overlapping row(s)",
                frag_id,
                incoming_local_rowaddr,
                next_batch_rowaddr,
                min(skip, batch.num_rows),
            )
            if skip >= batch.num_rows:
                align_ms += int((t1 - t0) * 1000)
                continue
            batch = batch.slice(skip)
            incoming_local_rowaddr = next_batch_rowaddr
        if incoming_local_rowaddr != next_batch_rowaddr:
            if fail_on_fill:
                raise CheckpointCoverageError(
                    frag_id,
                    gap_start=next_batch_rowaddr,
                    gap_end=incoming_local_rowaddr,
                )
            # global row id has frag_id in high bits
            fill_start = frag_id << 32 | next_batch_rowaddr
            fill_end = frag_id << 32 | incoming_local_rowaddr
            yield from _timed_fill(fill_start, fill_end, schema)
            next_batch_rowaddr = incoming_local_rowaddr

        align_ms += int((t1 - t0) * 1000)
        next_batch_rowaddr = incoming_local_rowaddr + batch.num_rows
        yield batch

    if schema is None:
        raise ValueError("No batches found")

    if expect_full_coverage and real_rows_total != num_logical_rows:
        raise CheckpointCoverageError(
            frag_id,
            detail=(
                f"Fragment {frag_id} received {real_rows_total} output row(s) "
                f"for {num_logical_rows} live row(s); refusing to null-fill "
                "the difference. Re-run the backfill to compute the missing "
                "rows."
            ),
        )

    # fill the rest of the rows at the end
    if next_batch_rowaddr < num_physical_rows:
        if fail_on_fill:
            raise CheckpointCoverageError(
                frag_id,
                gap_start=next_batch_rowaddr,
                gap_end=num_physical_rows,
            )
        fill_start = frag_id << 32 | next_batch_rowaddr
        fill_end = frag_id << 32 | num_physical_rows
        yield from _timed_fill(fill_start, fill_end, schema)

    if _timing is not None:
        _timing["align_ms"] += int(align_ms)


# max_concurrency=2: write() runs on one thread, the progress() probe on the other.
@ray.remote(num_cpus=1, max_concurrency=2)  # type: ignore[misc]
@attrs.define
class FragmentWriter:  # pyright: ignore[reportRedeclaration]
    uri: str
    column_names: list[str]
    checkpoint_uri: str
    fragment_id: int

    checkpoint_keys: ray.util.queue.Queue

    where: str | None = None
    data_storage_version: str | None = None
    read_version: int | None = None
    namespace_config: Optional[NamespaceConfig] = attrs.field(default=None, repr=False)
    table_id: Optional[list[str]] = None
    storage_options: Optional[dict[str, str]] = attrs.field(
        default=None, repr=redact_dict_values
    )
    checkpoint_namespace_client_impl: Optional[str] = None
    checkpoint_namespace_client_properties: Optional[dict[str, str]] = attrs.field(
        default=None, repr=False
    )
    checkpoint_table_id: Optional[list[str]] = None
    checkpoint_storage_options: Optional[dict[str, str]] = attrs.field(
        default=None, repr=redact_dict_values
    )
    checkpoint_session_root_subdir: Optional[str] = None
    checkpoint_write_identity_sidecar: bool = True
    # Multi-base placement: per-base checkpoint roots + fragment routing map
    # (mirrors CheckpointingApplier so the writer reads batch checkpoints from
    # this fragment's base, with table-root fallback for pre-upgrade keys).
    checkpoint_base_uris: Optional[dict[int, str]] = None
    checkpoint_frag_to_base: Optional[dict[int, int]] = None
    checkpoint_base_storage_options: Optional[dict[str, str]] = attrs.field(
        default=None, repr=redact_dict_values
    )
    # Where this fragment's staged output data file goes. None = dataset root.
    data_file_dir: Optional[str] = None
    data_file_base_id: Optional[int] = None
    data_file_name: Optional[str] = None
    blob_v2_checkpoint_assembly: bool = False
    # Manually add a repr for filler_schema bc otherwise Ray logs the entire schema
    # (not fully sure why) when repr is called.
    filler_schema: pa.Schema | None = attrs.field(
        default=None,
        repr=lambda s: f"<Schema with {len(s)} fields>" if s else "<Schema: None>",
    )
    field_ids: list[int] | None = None
    column_indices: list[int] | None = None
    num_physical_rows: int | None = None
    num_logical_rows: int | None = None
    # GEN-624: when set, the matched checkpoints are sparse (matched rows only)
    # and the unmatched rows are filled by streaming the OLD output column from
    # the fragment at ``read_version`` — instead of null-filling. This is the
    # write half of deferred carry-forward (see BackfillUDFTask.defer_carry_forward).
    defer_carry_forward: bool = False
    # GEN-638: blob-read config mirrored from the applier's ScanTask.
    # _old_column_stream now derives blob eligibility from the dataset schema
    # instead (the applier config is empty for a deferred-CF blob *output*
    # column), so range_blob_columns / selected_only_blob_columns /
    # struct_blob_decomp / blob_read_strategy are retained for compatibility but
    # no longer gate the old-column read. Only blob_read_buffer_size is still
    # consumed (the coalesced range reader's byte budget). See _old_column_stream.
    range_blob_columns: frozenset[str] | None = None
    selected_only_blob_columns: frozenset[str] | None = None
    struct_blob_decomp: tuple[Any, ...] | None = None
    blob_read_strategy: str | None = None
    blob_read_buffer_size: int | None = None
    # GEN-780: set only after a classified writer OOM. This is a row-based
    # working-set boundary, not an estimator: checkpoint files are range-read,
    # carry-forward is streamed, and aligned/filler batches honor the same cap.
    max_rows_per_batch: int | None = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.gt(0)),
    )
    # Dashboard-only labels so this actor's Ray repr names the job and table it
    # writes for; see ``__repr__``.
    job_id: str | None = None
    table_name: str | None = None

    _store: CheckpointStore = attrs.field(init=False)
    # Written by write(), read by the probe thread: a lone reference swap of a
    # frozen snapshot is race-free under the GIL, so no lock is needed.
    _latest_progress: WriterProgress = attrs.field(init=False, factory=WriterProgress)

    def progress(self) -> WriterProgress:
        """Liveness snapshot; served concurrently while ``write()`` runs."""
        return self._latest_progress

    def __repr__(self) -> str:
        """Crash-safe repr Ray uses as the per-line log prefix.

        Ray stamps ``repr(self)`` onto every log line this actor emits and shows
        it in the dashboard's actor list, so the full attrs repr would splat the
        writer config onto every line. Keep it to the fragment plus the fields
        that tie the actor back to its ``_geneva_jobs`` row.
        """
        try:
            return ray_name(
                "writer",
                table=self.table_name,
                column=",".join(self.column_names) if self.column_names else None,
                job_id=self.job_id,
                detail=f"frag={self.fragment_id}",
            )
        except Exception:
            return "writer"

    def __attrs_post_init__(self) -> None:
        self._store = CheckpointStore.from_uri(
            self.checkpoint_uri,
            namespace_client_impl=self.checkpoint_namespace_client_impl,
            namespace_client_properties=self.checkpoint_namespace_client_properties,
            table_id=self.checkpoint_table_id,
            storage_options=self.checkpoint_storage_options,
            session_root_subdir=self.checkpoint_session_root_subdir,
            write_identity_sidecar=self.checkpoint_write_identity_sidecar,
            base_checkpoint_uris=self.checkpoint_base_uris,
            frag_to_base=self.checkpoint_frag_to_base,
            base_storage_options=self.checkpoint_base_storage_options,
        )

    def _old_column_stream(
        self,
        dataset: "lance.LanceDataset",
        columns: list[str],
        tranche_rows: int,
    ) -> Iterator[pa.RecordBatch]:
        """Stream the OLD output column for this fragment in physical order.

        Yields ``columns`` plus ``_rowaddr`` in ``tranche_rows`` chunks so only a
        bounded number of old blob values are resident at once.

        Blob (and struct-with-nested-blob) carry-forward columns must be
        materialized to bytes here. The new (WHERE-matched) side of the merge
        holds materialized ``large_binary`` and ``pc.if_else`` requires both
        branches to share a type, so streaming the old side as
        ``struct<position,size>`` descriptors (what Lance's plain scanner returns
        for a blob column) raises ``ArrowTypeError``. Eligibility is derived from
        the columns actually being read against ``dataset.schema`` — NOT from the
        applier-mirrored config, which is empty for a deferred-CF blob *output*
        column (the applier strips those columns from its scan, and its range
        planner only fires on *input* blobs). Blob-eligible columns are routed
        through ``range_blob_batches`` (coalesced byte ranges); the plain scanner
        is used only when no column is a blob, and a blob column whose range read
        is unsupported fails loudly rather than silently yielding descriptors.
        """
        from geneva.apply.blob_range import (
            RangeBlobReadUnsupportedError,
            blob_columns_in_schema,
            column_has_blob_leaf,
            plan_struct_blob_decomposition,
            range_blob_batches,
        )

        # Detect blob columns (top-level/dotted) and struct columns whose nested
        # blob leaf must be range-materialized, straight from the schema of the
        # columns being read. Mirrors the planner's detection in
        # geneva.apply.__init__ but scoped to the writer's output columns, so it
        # is correct even for blob outputs the applier never scanned.
        schema = dataset.schema
        decomp_plans = tuple(
            plan
            for col in columns
            if (plan := plan_struct_blob_decomposition(schema, col)) is not None
        )
        nested_blob_leaves: set[str] = set()
        for plan in decomp_plans:
            nested_blob_leaves.update(plan.blob_paths())
        range_blob_columns = blob_columns_in_schema(schema, columns) | frozenset(
            nested_blob_leaves
        )

        if range_blob_columns:
            try:
                yield from range_blob_batches(
                    dataset=dataset,
                    columns=columns,
                    frag_id=self.fragment_id,
                    offset=0,
                    limit=0,
                    version=self.read_version,
                    where=None,
                    with_row_address=True,
                    range_blob_columns=range_blob_columns,
                    # Carry-forward reads OUTPUT columns we must fully
                    # materialize; never treat them as input-only / skip-on-
                    # unmatched (that path is for filtered UDF *inputs*).
                    selected_only_blob_columns=None,
                    blob_read_buffer_size=self.blob_read_buffer_size,
                    storage_options=self.storage_options,
                    batch_size=max(1, int(tranche_rows)),
                    struct_blob_decomp=decomp_plans or None,
                )
                return
            except RangeBlobReadUnsupportedError:
                # A blob column cannot fall back to the plain scanner — that
                # yields struct<position,size> descriptors, not bytes, which
                # crash the if_else merge and corrupt the carried-forward data
                # file. Fail loudly instead of silently writing descriptors.
                _LOG.error(
                    "Range blob read unsupported for fragment %s carry-forward "
                    "of %s; cannot materialize blob bytes",
                    self.fragment_id,
                    sorted(range_blob_columns),
                )
                raise

        # Defense in depth: detection above covers top-level blobs and one-level
        # struct blobs — the shapes the range reader can decompose. A blob it
        # cannot reach (e.g. list<blob>, or a struct blob nested 2+ levels deep)
        # leaves range_blob_columns empty and would otherwise fall to the scanner
        # below and stream struct<position,size> descriptors — re-introducing the
        # crash/corruption for an unsupported shape. Fail loudly instead.
        unsupported_blob_cols = [c for c in columns if column_has_blob_leaf(schema, c)]
        if unsupported_blob_cols:
            raise RangeBlobReadUnsupportedError(
                f"carry-forward of blob column(s) {sorted(unsupported_blob_cols)} "
                f"is unsupported for fragment {self.fragment_id}: the blob is "
                "nested in a shape the range reader cannot materialize "
                "(e.g. list<blob>, or a struct blob nested 2+ levels deep); "
                "the scanner fallback would yield descriptors instead of bytes"
            )

        # No blob columns: the plain Lance scanner returns real values safely.
        frag = dataset.get_fragment(self.fragment_id)
        if frag is None:
            raise ValueError(f"Fragment {self.fragment_id} not found for carry-forward")
        scanner = frag.scanner(
            columns=columns,
            with_row_address=True,
            batch_size=max(1, int(tranche_rows)),
        )
        yield from scanner.to_batches()

    def _carry_forward_merge(
        self,
        *,
        num_logical_rows: int,
        tranche_rows: int,
        _timing: dict[str, int] | None = None,
        _progress: Callable[..., None] | None = None,
    ) -> Iterator[pa.RecordBatch]:
        """Overlay the WHERE-matched output onto a stream of the OLD output column.

        The matched checkpoints are consumed as lazy per-file references
        (``keys_only``) and ``k``-way merged against the old column by
        ``MatchStream``, so the matched set is never fully resident — only files
        overlapping the current old-column window are read. The old column is
        streamed at ``read_version``; unmatched rows keep their previous value.
        Yields the live (logical) rows in physical-rowaddr order; the caller
        aligns to the physical layout (which fills any deleted-row gaps).
        """
        import itertools

        from geneva.db import open_lance_dataset
        from geneva.runners.ray.stream_merge import (
            MatchStream,
            _RunCursor,
            stream_merge_carry_forward,
        )

        dataset = open_lance_dataset(
            self.uri,
            namespace_config=self.namespace_config,
            table_id=self.table_id,
            version=self.read_version,
            storage_options=self.storage_options,
            use_worker_props=True,
        )
        cols = [c for c in self.column_names if c != "_rowaddr"]
        old_stream = self._old_column_stream(dataset, cols, tranche_rows)
        max_rows_per_batch = getattr(self, "max_rows_per_batch", None)

        # Collect the matched checkpoint references (keys only — no data read) and
        # build one lazy cursor per file, ordered/activated by the peeked key
        # range. 0-row and all-unmatched fragments simply yield no cursors, so the
        # merge becomes a pass-through of the old column.
        cursors: list[_RunCursor] = []

        def _note_checkpoint_read(
            _batch: pa.RecordBatch,
            elapsed_ms: int,
            _contributes_batch: bool,
            first_read: bool,
        ) -> None:
            if _timing is not None:
                _timing["checkpoint_read_ms"] += elapsed_ms
            _bump_checkpoint_read_progress(_progress, first_read=first_read)

        for ref in _buffer_and_sort_batches(
            num_logical_rows,
            self.fragment_id,
            None,  # filler_schema unused in keys_only mode
            self._store,
            self.checkpoint_keys,
            _timing=_timing,
            _progress=_progress,
            keys_only=True,
        ):
            assert isinstance(ref, _PendingCheckpoint)
            start = _parse_range_start_from_key(ref.key)
            cursors.append(
                _RunCursor(
                    start if start is not None else 0,
                    _read_checkpoint_batches(
                        self._store,
                        ref.key,
                        ref.expected_rows,
                        max_rows_per_batch=max_rows_per_batch,
                        _on_read=_note_checkpoint_read,
                    ),
                )
            )

        # MatchStream needs the matched schema (output columns + ``_rowaddr``);
        # take it from the old-column stream, which carries the same output
        # columns. Peeking the first tranche also lets an empty fragment short out.
        old_iter = iter(old_stream)
        try:
            first_old = next(old_iter)
        except StopIteration:
            return
        old_full = itertools.chain([first_old], old_iter)
        match_stream = MatchStream(first_old.schema, cursors)
        yield from stream_merge_carry_forward(
            match_index=match_stream, old_column_stream=old_full
        )

    # frag id, new_file, rows_written
    def write(self) -> FragmentWriteResult:
        _LOG.debug(
            f"Writing fragment {self.fragment_id} to {self.uri} with columns"
            f" {self.column_names} where '{self.where}' version={self.read_version}"
        )
        num_physical_rows = self.num_physical_rows
        num_logical_rows = self.num_logical_rows
        filler_schema = self.filler_schema
        field_ids = self.field_ids
        column_indices = self.column_indices

        data_storage_version = self.data_storage_version

        if (
            num_physical_rows is None
            or num_logical_rows is None
            or filler_schema is None
            or field_ids is None
            or column_indices is None
            or data_storage_version is None
        ):
            from geneva.db import open_lance_dataset

            dataset = open_lance_dataset(
                self.uri,
                namespace_config=self.namespace_config,
                table_id=self.table_id,
                version=self.read_version,
                storage_options=self.storage_options,
                use_worker_props=True,
            )

            if data_storage_version is None:
                data_storage_version = dataset.data_storage_version

            frag = dataset.get_fragment(self.fragment_id)
            if frag is None:
                _LOG.warning(
                    "Fragment %s not found in dataset %s", self.fragment_id, self.uri
                )
                raise ValueError(f"Fragment {self.fragment_id} not found")
            if num_physical_rows is None:
                num_physical_rows = frag.physical_rows  # num rows before deletions
            if num_logical_rows is None:
                num_logical_rows = frag.count_rows()  # num rows including deletions

            if filler_schema is None:
                base_schema = dataset.schema
                fields: list[pa.Field] = []
                for name in self.column_names:
                    try:
                        resolved = resolve_arrow_field_path(base_schema, name)
                    except (KeyError, ValueError):
                        continue
                    fields.append(resolved.as_projected_field())
                fields.append(pa.field("_rowaddr", pa.uint64()))
                filler_schema = pa.schema(fields)

            if field_ids is None or column_indices is None:
                field_ids, column_indices = extract_field_ids_and_column_indices(
                    dataset.lance_schema,
                    self.column_names,
                    data_storage_version,
                    omit_special_leaf_children=self.blob_v2_checkpoint_assembly,
                )

        assert data_storage_version is not None
        assert num_physical_rows is not None
        assert num_logical_rows is not None
        assert filler_schema is not None
        assert field_ids is not None
        assert column_indices is not None

        progress_seq = 0
        progress_counters = {"checkpoints_read": 0, "batches_out": 0, "rows_out": 0}

        def _bump(phase: str, **deltas: int) -> None:
            nonlocal progress_seq
            progress_seq += 1
            for key, delta in deltas.items():
                progress_counters[key] += delta
            self._latest_progress = WriterProgress(
                seq=progress_seq, phase=phase, **progress_counters
            )

        _bump("start")

        # we always write files that physically align with the fragment
        timings: dict[str, int] = {
            "align_ms": 0,
            "queue_wait_ms": 0,
            "checkpoint_read_ms": 0,
        }
        batch_stats: dict[str, int] = {
            "num_batches": 0,
            "total_rows": 0,
            "total_bytes": 0,
        }
        max_rows_per_batch = getattr(self, "max_rows_per_batch", None)
        # For deferred carry-forward the checkpoints hold only
        # the WHERE-matched rows; fill the unmatched rows by streaming the OLD
        # output column instead of null. The merge consumes the matched
        # checkpoints as lazy per-file references (not materialized here) and
        # streams them against the old column, so the matched set is never fully
        # resident. The result yields the live (logical) rows, aligned to the
        # physical layout below (filling deleted-row gaps with nulls), so this
        # works for fragments with deletes too.
        if self.defer_carry_forward and self.where is not None:
            carry_forward_tranche_rows = DEFAULT_CARRY_FORWARD_TRANCHE_ROWS
            if max_rows_per_batch is not None:
                carry_forward_tranche_rows = min(
                    carry_forward_tranche_rows, max_rows_per_batch
                )
            it = self._carry_forward_merge(
                num_logical_rows=num_logical_rows,
                tranche_rows=carry_forward_tranche_rows,
                _timing=timings,
                _progress=_bump,
            )
        else:
            # Non-keys_only never yields _PendingCheckpoint; narrow for the writer.
            #
            # expect_full_coverage holds for this path even with a WHERE
            # filter: backfill scans apply the filter as a selection column
            # (``with_where_as_bool_column``), so completed tasks emit
            # checkpoints whose ``_range-`` spans tile the whole task window
            # (zero-match tasks synthesize completion checkpoints). A gap at
            # seal therefore always means dropped checkpoints — null-filling
            # it would silently lose UDF output (and, with a filter,
            # overwrite carried-forward values).
            it = cast(
                "Iterator[pa.RecordBatch]",
                _buffer_and_sort_batches(
                    num_logical_rows,
                    self.fragment_id,
                    filler_schema,
                    self._store,
                    self.checkpoint_keys,
                    _timing=timings,
                    _batch_stats=batch_stats,
                    _progress=_bump,
                    expect_full_coverage=True,
                    max_rows_per_batch=max_rows_per_batch,
                ),
            )

        # Full coverage holds for both sources feeding the alignment: the
        # checkpoint-materialization path (see the expect_full_coverage note
        # above) and the deferred carry-forward merge, which yields every
        # live row by construction (matched rows from checkpoints, the rest
        # carried forward from the old column).
        it = _align_batches_to_physical_layout(
            num_physical_rows,
            num_logical_rows,
            self.fragment_id,
            it,
            _timing=timings,
            expect_full_coverage=True,
            max_rows_per_batch=max_rows_per_batch,
        )

        # Filter batches to only include columns in the target schema.
        # This removes any source table columns that weren't selected in the
        # materialized view (e.g., if source has [id, title, width] but view
        # only selects [title], this removes id and width).
        it = _filter_columns_to_schema(it, self.column_names)

        def _instrumented(
            batches: Iterator[pa.RecordBatch],
        ) -> Iterator[pa.RecordBatch]:
            # Bump after yield so it counts batches the writer consumed, not
            # produced (the footer flush after "finalize" emits no more bumps).
            for batch in batches:
                yield batch
                _bump("write", batches_out=1, rows_out=batch.num_rows)
            _bump("finalize")

        it = _instrumented(it)
        new_datafile, written, writer_write_ms = get_fragment_file_writer().write(
            write_fragment_file,
            self.uri,
            it,
            column_names=self.column_names,
            field_ids=field_ids,
            column_indices=column_indices,
            data_storage_version=data_storage_version,
            filter_columns=False,
            table_id=self.table_id,
            storage_options=self.storage_options,
            data_dir=self.data_file_dir,
            base_id=self.data_file_base_id,
            data_file_name=self.data_file_name,
            namespace_impl=(
                self.namespace_config.namespace_client_impl
                if self.namespace_config is not None
                else "dir"
            ),
            namespace_properties=(
                self.namespace_config.namespace_client_properties
                if self.namespace_config is not None
                else {
                    "root": self.uri,
                    **_directory_namespace_storage_properties(self.storage_options),
                }
            ),
        )

        # The aligned stream fills to the physical layout, so a complete write emits
        # exactly num_physical_rows. Fewer is a short write -- committing it makes the
        # table unreadable (row count disagrees with the manifest). Fail loud before the
        # fragment is recorded.
        if num_physical_rows is not None and written != num_physical_rows:
            raise ShortFragmentWriteError(
                f"fragment {self.fragment_id}: wrote {written} rows but the aligned "
                f"physical layout has {num_physical_rows}; refusing to commit a short "
                f"data file"
            )

        align_ms = int(timings.get("align_ms", 0) or 0)
        queue_wait_ms = int(timings.get("queue_wait_ms", 0) or 0)
        checkpoint_read_ms = int(timings.get("checkpoint_read_ms", 0) or 0)
        num_batches = int(batch_stats.get("num_batches", 0) or 0)
        total_batch_rows = int(batch_stats.get("total_rows", 0) or 0)
        total_batch_bytes = int(batch_stats.get("total_bytes", 0) or 0)
        avg_batch_num_rows = (
            int(round(total_batch_rows / num_batches)) if num_batches else 0
        )
        avg_batch_size = (
            int(round(total_batch_bytes / num_batches)) if num_batches else 0
        )
        return FragmentWriteResult(
            frag_id=self.fragment_id,
            new_file=new_datafile,
            rows_written=written,
            align_ms=align_ms,
            write_ms=int(writer_write_ms),
            queue_wait_ms=queue_wait_ms,
            checkpoint_read_ms=checkpoint_read_ms,
            avg_batch_num_rows=avg_batch_num_rows,
            avg_batch_size=avg_batch_size,
        )


FragmentWriter: ray.actor.ActorClass = cast("ray.actor.ActorClass", FragmentWriter)
