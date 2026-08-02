# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import json
import logging
import os
import time
import urllib
import urllib.parse
import uuid
from collections.abc import Iterator
from typing import Any, Optional, cast

import attrs
import lance
import lance.file
import pyarrow as pa
import ray
import ray.actor
import ray.util.queue
from yarl import URL

from geneva.apply.memory import release_unused_process_memory
from geneva.checkpoint import CheckpointStore
from geneva.db import NamespaceConfig, _directory_namespace_storage_properties
from geneva.fragment_writer import get_fragment_file_writer
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
    """

    key: str


def _buffer_and_sort_batches(
    num_rows: int,
    frag_id: int,
    filler_schema: pa.Schema | None,
    store: CheckpointStore,
    queue: ray.util.queue.Queue,
    *,
    _timing: dict[str, int] | None = None,
    _batch_stats: dict[str, int] | None = None,
    keys_only: bool = False,
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
                yield _PendingCheckpoint(item[1])
        finally:
            if _timing is not None:
                _timing["queue_wait_ms"] += int(queue_wait_ms)
        return

    assert filler_schema is not None, "filler_schema is required unless keys_only"
    accumulation_queue: SequenceQueue[pa.RecordBatch | _PendingCheckpoint] = (
        SequenceQueue()
    )
    sealed = False

    def _materialize(item: pa.RecordBatch | _PendingCheckpoint) -> pa.RecordBatch:
        nonlocal checkpoint_read_ms
        if isinstance(item, _PendingCheckpoint):
            read_start = time.perf_counter()
            data = store[item.key]
            checkpoint_read_ms += int((time.perf_counter() - read_start) * 1000)
            return data
        return item

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
                    if gap_end > gap_start:
                        fill_start = (frag_id << 32) | gap_start
                        fill_end = (frag_id << 32) | gap_end
                        filler = _make_filler_batch(fill_start, fill_end, filler_schema)
                        accumulation_queue.put(gap_start, gap_end - gap_start, filler)
                        break
                try:
                    wait_start = time.perf_counter()
                    batch: tuple[int, str] = queue.get()
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

                checkpoint_key = batch[1]
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
                        batch[0], span, _PendingCheckpoint(checkpoint_key)
                    )
                else:
                    # Legacy/malformed key: must read eagerly so we can
                    # learn the row count for SequenceQueue accounting.
                    read_start = time.perf_counter()
                    stored = store[checkpoint_key]
                    checkpoint_read_ms += int((time.perf_counter() - read_start) * 1000)
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
                materialized = _materialize(pending)
                if isinstance(pending, _PendingCheckpoint) and _batch_stats is not None:
                    _batch_stats["num_batches"] += 1
                    _batch_stats["total_rows"] += int(materialized.num_rows)
                    _batch_stats["total_bytes"] += _record_batch_size_bytes(
                        materialized
                    )
                yield materialized
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
        # Long-lived writer processes touch many fragments back-to-back, and
        # Arrow's mempool + libc's malloc retain freed pages without explicit
        # trim. Per-fragment is the natural unit: small enough that one
        # fragment's drift can't grow unbounded, large enough that the trim's
        # arena walk cost is amortized over a real chunk of work.
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
) -> Iterator[pa.RecordBatch]:
    """
    This aligns the batches to the physical rows layout.

    It will fill in the _rowaddr gaps within a batch with new rows with the _rowaddr
    index values and None values for the other columns.  It will also fill the _rowaddr
    gaps between batches with the _rowaddr index values and None values for the other
    cols.
    """

    if num_logical_rows > num_physical_rows:
        raise ValueError(
            "Logical rows should be greater than or equal to physical rows"
        )

    next_batch_rowaddr = 0

    schema = None

    align_ms = 0
    it = iter(batches)
    while True:
        try:
            raw_batch = next(it)
        except StopIteration:
            break

        t0 = time.perf_counter()
        batch = _fill_rowaddr_gaps(raw_batch)
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
            # global row id has frag_id in high bits
            fill_start = frag_id << 32 | next_batch_rowaddr
            fill_end = frag_id << 32 | incoming_local_rowaddr
            t_fill = time.perf_counter()
            filler = _make_filler_batch(fill_start, fill_end, schema)
            align_ms += int((time.perf_counter() - t_fill) * 1000)
            yield filler
            next_batch_rowaddr = incoming_local_rowaddr

        align_ms += int((t1 - t0) * 1000)
        next_batch_rowaddr = incoming_local_rowaddr + batch.num_rows
        yield batch

    if schema is None:
        raise ValueError("No batches found")

    # fill the rest of the rows at the end
    if next_batch_rowaddr < num_physical_rows:
        fill_start = frag_id << 32 | next_batch_rowaddr
        fill_end = frag_id << 32 | num_physical_rows
        t0 = time.perf_counter()
        yield _make_filler_batch(fill_start, fill_end, schema)
        align_ms += int((time.perf_counter() - t0) * 1000)

    if _timing is not None:
        _timing["align_ms"] += int(align_ms)


@ray.remote(num_cpus=1)  # type: ignore[misc]
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

    _store: CheckpointStore = attrs.field(init=False)

    def __repr__(self) -> str:
        """Crash-safe repr Ray uses as the per-line log prefix.

        Ray stamps ``repr(self)`` onto every log line this actor emits, so the
        full attrs repr would splat the writer config onto every line. Keep it
        to a short fragment identifier.
        """
        try:
            return f"FragmentWriter(fragment_id={self.fragment_id})"
        except Exception:
            return "FragmentWriter"

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
                    dataset_uri=self.uri,
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
        import functools
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

        # Collect the matched checkpoint references (keys only — no data read) and
        # build one lazy cursor per file, ordered/activated by the peeked key
        # range. 0-row and all-unmatched fragments simply yield no cursors, so the
        # merge becomes a pass-through of the old column.
        cursors: list[_RunCursor] = []
        for ref in _buffer_and_sort_batches(
            num_logical_rows,
            self.fragment_id,
            None,  # filler_schema unused in keys_only mode
            self._store,
            self.checkpoint_keys,
            _timing=_timing,
            keys_only=True,
        ):
            assert isinstance(ref, _PendingCheckpoint)
            start = _parse_range_start_from_key(ref.key)
            cursors.append(
                _RunCursor(
                    start if start is not None else 0,
                    functools.partial(self._store.__getitem__, ref.key),
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
        # For deferred carry-forward the checkpoints hold only
        # the WHERE-matched rows; fill the unmatched rows by streaming the OLD
        # output column instead of null. The merge consumes the matched
        # checkpoints as lazy per-file references (not materialized here) and
        # streams them against the old column, so the matched set is never fully
        # resident. The result yields the live (logical) rows, aligned to the
        # physical layout below (filling deleted-row gaps with nulls), so this
        # works for fragments with deletes too.
        if self.defer_carry_forward and self.where is not None:
            it = self._carry_forward_merge(
                num_logical_rows=num_logical_rows,
                tranche_rows=DEFAULT_CARRY_FORWARD_TRANCHE_ROWS,
                _timing=timings,
            )
        else:
            # Non-keys_only never yields _PendingCheckpoint; narrow for the writer.
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
                ),
            )

        it = _align_batches_to_physical_layout(
            num_physical_rows,
            num_logical_rows,
            self.fragment_id,
            it,
            _timing=timings,
        )

        # Filter batches to only include columns in the target schema.
        # This removes any source table columns that weren't selected in the
        # materialized view (e.g., if source has [id, title, width] but view
        # only selects [title], this removes id and width).
        it = _filter_columns_to_schema(it, self.column_names)
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
