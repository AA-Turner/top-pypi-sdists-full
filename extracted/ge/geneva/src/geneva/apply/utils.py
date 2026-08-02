# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import hashlib
import itertools
import json
import logging
import random
import re
import time
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Any, Optional, TypeVar

import more_itertools
import pyarrow as pa
import pyarrow.compute as pc
from lance.file import LanceFileSession
from yarl import URL

from geneva.apply.task import DEFAULT_CHECKPOINT_ROWS, MapTask
from geneva.checkpoint import CheckpointStore
from geneva.checkpoint_utils import hash_source_files
from geneva.transformer import BACKFILL_SELECTED

if TYPE_CHECKING:
    from lance_namespace import LanceNamespace

_LOG = logging.getLogger(__name__)
T = TypeVar("T")
_SRCFILES_PREFIX_RE = re.compile(r"^.+_uri-[^_]+_srcfiles-(?P<srcfiles>[^_]+)$")


def _iter_with_next_duration(values: Iterator[T]) -> Iterator[tuple[int, T]]:
    """Yield ``(duration_ms, value)`` where duration is spent in ``next(values)``."""
    while True:
        start = time.perf_counter()
        try:
            value = next(values)
        except StopIteration:
            return
        yield int((time.perf_counter() - start) * 1000), value


def _legacy_map_task_key(map_task: MapTask) -> str:
    """Best-effort reconstruction of pre-range map task key."""
    try:
        return map_task.legacy_map_task_key(where=getattr(map_task, "where", None))
    except Exception:
        return "unknown"


def _legacy_fragment_dedupe_key(uri: str, frag_id: int, map_task: MapTask) -> str:
    key = f"{uri}:{frag_id}:{_legacy_map_task_key(map_task)}"
    return hashlib.sha256(key.encode()).hexdigest()


def _srcfiles_hash_from_checkpoint_key(key: str) -> str | None:
    """Extract the `_srcfiles-...` hash from a fragment/range checkpoint key."""
    prefix, sep, _ = key.rpartition("_frag-")
    if not sep:
        return None
    match = _SRCFILES_PREFIX_RE.match(prefix)
    if match is None:
        return None
    return match.group("srcfiles")


def _checkpoint_key_matches_source_files(
    key: str, current_data_files: frozenset[str]
) -> bool:
    """Return whether a checkpoint key's source-file hash matches current files."""
    srcfiles_hash = _srcfiles_hash_from_checkpoint_key(key)
    return srcfiles_hash is not None and srcfiles_hash == hash_source_files(
        current_data_files
    )


def _parse_checkpoint_ranges_for_fragment(
    *,
    checkpoint_store: CheckpointStore,
    prefixes: list[str],
    frag_id: int,
) -> list[tuple[int, int]]:
    """
    Collect checkpointed row ranges for a fragment.

    This is a thin wrapper over `_iter_checkpoint_ranges_for_fragment` that
    discards the checkpoint keys and returns only the covered ranges.
    Callers typically feed the result into `_merge_ranges` and
    `_compute_missing_ranges` during `plan_read` to avoid re-scanning rows that
    have already been checkpointed.

    Returns:
        A list of ranges `[start, end)` (0-based, fragment-local; start inclusive,
        end exclusive).
    """
    # `_iter_checkpoint_ranges_for_fragment` yields (key, start, end). We only
    # need the numeric ranges here.
    return [
        r[1:]
        for r in _iter_checkpoint_ranges_for_fragment(
            checkpoint_store=checkpoint_store, prefixes=prefixes, frag_id=frag_id
        )
    ]


def _parse_checkpoint_range_key(
    key: str,
) -> tuple[str, int, int, int] | None:
    """Parse a checkpoint range key into (prefix, frag_id, start, end)."""
    if "_frag-" not in key or "_range-" not in key:
        return None
    try:
        prefix, frag_and_range = key.rsplit("_frag-", 1)
        frag_str, range_str = frag_and_range.split("_range-", 1)
        start_str, end_str = range_str.split("-", 1)
        frag_id = int(frag_str)
        start = int(start_str)
        end = int(end_str)
    except Exception:
        return None
    if end <= start:
        return None
    return (prefix, frag_id, start, end)


def _index_checkpoint_ranges(
    *,
    checkpoint_store: CheckpointStore,
    prefixes: list[str] | None = None,
) -> tuple[set[str], dict[str, dict[int, list[tuple[int, int]]]]]:
    """List all checkpoint keys once and index range checkpoints by prefix/fragment.

    When *prefixes* is provided, the store may scope listing to the current
    backfill identity. This is a server-side LIST reduction for hierarchical
    layout and a client-side filter for flat layout.
    """
    all_keys: set[str] = set()
    ranges_by_prefix: dict[str, dict[int, list[tuple[int, int]]]] = {}
    seen: set[str] = set()
    list_prefixes = prefixes if prefixes is not None else [""]
    for list_prefix in list_prefixes:
        for key in checkpoint_store.list_keys(prefix=list_prefix):
            if key in seen:
                continue
            seen.add(key)
            all_keys.add(key)
            parsed = _parse_checkpoint_range_key(key)
            if parsed is None:
                continue
            prefix, frag_id, start, end = parsed
            ranges_by_prefix.setdefault(prefix, {}).setdefault(frag_id, []).append(
                (start, end)
            )
    return all_keys, ranges_by_prefix


def _iter_checkpoint_ranges_for_fragment(
    *,
    checkpoint_store: CheckpointStore,
    prefixes: list[str],
    frag_id: int,
) -> list[tuple[str, int, int]]:
    """
    Enumerate per-batch checkpoints for a fragment.

    We intentionally *list and parse existing checkpoint keys* rather than
    probing at fixed steps of `checkpoint_size`. This makes `plan_read`
    resilient to:
    - legacy checkpoints (task-level or different naming),
    - future adaptive checkpoint sizes (varying batch lengths),
    - partial progress where only some batches exist.

    Expected key format (suffix):
        "..._frag-{frag_id}_range-{start}-{end}"

    Where `start`/`end` are 0-based, fragment-local row offsets and represent
    `[start, end)` (start inclusive, end exclusive). Any key that doesn't match
    this format is ignored.

    Returns:
        A list of tuples `(key, start, end)` for matching checkpoints.
    """

    ranges: list[tuple[str, int, int]] = []
    # We only care about checkpoints that were written for this fragment.
    marker = f"_frag-{frag_id}_range-"

    # `CheckpointStore` may contain keys from multiple datasets / tasks, so we
    # restrict listing to the relevant key prefixes. We de-duplicate across
    # prefixes because callers may include multiple compatible prefix shapes
    # (e.g., legacy keys without srcfiles hashes).
    seen: set[str] = set()
    for prefix in prefixes:
        # Narrow listing to keys for this specific fragment/range shape. This
        # avoids scanning unrelated fragment checkpoints that share the same
        # dataset/task prefix.
        for key in checkpoint_store.list_keys(prefix=f"{prefix}{marker}"):
            if key in seen:
                continue
            seen.add(key)
            try:
                parsed = _parse_checkpoint_range_key(key)
                if parsed is None:
                    raise ValueError("malformed checkpoint key")
                parsed_prefix, parsed_frag_id, start, end = parsed
                # Double-check we matched the requested fragment/prefix.
                if parsed_prefix != prefix or parsed_frag_id != frag_id:
                    continue
                ranges.append((key, start, end))
            except Exception as exc:
                # Be permissive: ignore malformed / legacy keys instead of failing
                # planning. This avoids a single bad key blocking progress.
                _LOG.debug(
                    "Skipping malformed checkpoint key %s: %s",
                    key,
                    exc,
                    exc_info=True,
                )

    return ranges


def _merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merge overlapping or adjacent ranges.

    Input ranges are interpreted as `[start, end)` offsets (0-based, start
    inclusive, end exclusive). After sorting by `start`, we coalesce any range
    whose start is `<=` the previous end. This treats adjacent ranges (e.g.,
    [0,5) and [5,7)) as continuous coverage.

    Returns:
        A sorted, non-overlapping list of merged ranges.
    """
    if not ranges:
        return []
    # Sort so we can sweep left-to-right.
    ranges = sorted(ranges, key=lambda r: r[0])
    merged = [ranges[0]]
    for s, e in ranges[1:]:
        last_s, last_e = merged[-1]
        # Overlap or adjacency => extend the previous coverage window.
        if s <= last_e:
            merged[-1] = (last_s, max(last_e, e))
        else:
            # Gap => start a new coverage window.
            merged.append((s, e))
    return merged


def _compute_missing_ranges(
    *,
    total_rows: int,
    task_size: int,
    covered: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """
    Compute read-task ranges that are not covered by checkpoints.

    Args:
        total_rows: Total number of rows in the fragment.
        task_size: Desired read-task size. Each returned task has
            `limit <= task_size` unless `task_size <= 0`.
        covered: Sorted, merged checkpoint coverage ranges `[start, end)`.

    Returns:
        A list of `(offset, limit)` pairs describing missing regions to scan.
        Here `offset` is the fragment-local row start, and `limit` is the
        number of rows to read for that task.
    """

    # First compute complement gaps of `covered` within [0, total_rows).
    gaps: list[tuple[int, int]] = []
    cur = 0
    for s, e in covered:
        if cur < s:
            gaps.append((cur, s))
        cur = max(cur, e)
    if cur < total_rows:
        gaps.append((cur, total_rows))

    # Then split each gap into one or more tasks of size `task_size`.
    tasks: list[tuple[int, int]] = []
    for start, end in gaps:
        remaining = end - start
        if task_size <= 0:
            # Degenerate / test case: treat the whole gap as a single task.
            tasks.append((start, remaining))
            continue
        while remaining > task_size:
            # Full-sized tasks.
            tasks.append((start, task_size))
            start += task_size
            remaining -= task_size
        if remaining > 0:
            # Final tail task (shorter than task_size).
            tasks.append((start, remaining))

    return tasks


def _count_udf_rows(batch: pa.RecordBatch | list[dict[str, Any]]) -> int:
    """
    Count the number of rows that will execute a UDF within the provided batch.

    The BACKFILL_SELECTED column (when present) identifies the subset of rows
    whose UDF should be evaluated. When the column is absent we assume all rows
    execute the UDF.
    """
    if isinstance(batch, pa.RecordBatch):
        if BACKFILL_SELECTED in batch.schema.names:
            mask = batch[BACKFILL_SELECTED]
            # pyarrow.compute.sum skips nulls by default, treating them as zero.
            summed = pc.sum(mask)
            value = summed.as_py() if hasattr(summed, "as_py") else summed
            return int(value or 0)
        return int(batch.num_rows)

    if not batch:
        return 0

    # this is the blob case where the batch is a list of dicts
    count = 0
    for row in batch:
        if not isinstance(row, dict):
            count += 1
            continue
        selected = row.get(BACKFILL_SELECTED, True)
        if selected:
            count += 1
    return count


def _staged_data_file_is_complete(
    file_session: "LanceFileSession",
    staging_path: str,
    expected_rows: int | None,
) -> bool:
    """Return True if a staged file is a usable basis for skipping a fragment.

    A crash can leave a 0-byte or partially-written staged file behind, so file
    existence alone is not enough. Field-ids can't be checked (a standalone data
    file doesn't carry the dataset's logical field-ids), so validate on
    openability and row count: the file must open, and (when known) its row
    count must equal ``expected_rows``, else be non-empty.
    """
    try:
        reader = file_session.open_reader(staging_path)
        num_rows = reader.metadata().num_rows
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as e:  # noqa: BLE001
        # Lance opens via pyo3 and panics (a BaseException, not Exception) on a
        # 0-byte or corrupt file, so catch broadly.
        _LOG.debug(f"Staged file {staging_path} is not a readable Lance file: {e}")
        return False
    if expected_rows is not None:
        return num_rows == expected_rows
    return num_rows > 0


def _check_fragment_data_file_exists(
    uri: str,
    frag_id: int,
    map_task: MapTask,
    checkpoint_store: CheckpointStore,
    dataset_version: int | str | None = None,
    src_files_hash: str | None = None,
    current_output_field_ids: frozenset[int] | None = None,
    current_data_files: frozenset[str] | None = None,
    namespace: Optional["LanceNamespace"] = None,
    table_id: Optional[list[str]] = None,
    storage_options: Optional[dict[str, str]] = None,
    checkpoint_keys: set[str] | None = None,
    expected_rows: int | None = None,
    base_dirs: dict[int, str] | None = None,
) -> tuple[str, int | None] | None:
    """
    Check if a fragment data file already exists in staging or target locations.

    Returns ``(file_path, base_id)`` if the fragment can be skipped, or
    ``None`` if it cannot.  ``base_id`` is the storage base the staged file
    was written to (from the checkpoint payload; None = dataset root).
    Returning the payload fields avoids a redundant ``checkpoint_store[key]``
    read by the caller.

    When *checkpoint_keys* is provided, it is used for the ``in`` membership
    check instead of ``checkpoint_store.__contains__`` (which does a blob stat
    per call).  This avoids per-fragment blob I/O when the caller has already
    indexed all checkpoint keys into an in-memory set.

    ``base_dirs`` maps base id -> data-file directory for multi-base
    datasets; the staging probe for a payload carrying a ``base_id`` runs
    against that base's directory instead of ``{uri}/data``.
    """
    # Import here to avoid circular imports
    from geneva.runners.ray.pipeline import _get_fragment_dedupe_key

    # Helper: membership check using in-memory set when available
    def _key_exists(key: str) -> bool:
        if checkpoint_keys is not None:
            return key in checkpoint_keys
        return key in checkpoint_store

    # Get the fragment's checkpoint key
    dedupe_key = _get_fragment_dedupe_key(
        uri,
        frag_id,
        map_task,
        dataset_version=dataset_version,
        src_files_hash=src_files_hash,
    )
    if not _key_exists(dedupe_key):
        # Backward compatibility for pre-change checkpoint keys.
        dedupe_key = _legacy_fragment_dedupe_key(uri, frag_id, map_task)

    # Check if fragment is already checkpointed
    if not _key_exists(dedupe_key):
        return None

    try:
        # Get the stored file path from checkpoint
        checkpointed_data = checkpoint_store[dedupe_key]
        if "file" not in checkpointed_data.schema.names:
            return None

        file_list = checkpointed_data["file"].to_pylist()
        file_path = "".join(str(f) for f in file_list if f is not None)
        if not file_path:
            return None

        staged_base_id: int | None = None
        if "base_id" in checkpointed_data.schema.names:
            raw_base_id = checkpointed_data["base_id"][0].as_py()
            staged_base_id = int(raw_base_id) if raw_base_id is not None else None

        if (
            current_output_field_ids is not None
            and "output_field_ids" in checkpointed_data.schema.names
        ):
            stored_json = checkpointed_data["output_field_ids"][0].as_py()
            if stored_json is None:
                return None
            stored_field_ids = frozenset(json.loads(stored_json))
            if stored_field_ids != current_output_field_ids:
                _LOG.info(
                    f"Fragment {frag_id} output field IDs changed; "
                    "invalidating checkpoint"
                )
                return None

        if current_data_files is not None and file_path not in current_data_files:
            _LOG.info(
                f"Fragment {frag_id} checkpoint file not in current data files; "
                "invalidating checkpoint"
            )
            return None
        if current_data_files is not None:
            # The caller already validated the file against current fragment
            # metadata, so we do not need an extra staging/target existence probe.
            return file_path, staged_base_id

        from geneva.db import open_lance_dataset

        dataset = open_lance_dataset(
            uri,
            table_id=table_id,
            storage_options=storage_options,
            namespace_client=namespace,
        )

        staged_base_dir = (
            base_dirs.get(staged_base_id)
            if base_dirs is not None and staged_base_id is not None
            else None
        )
        if staged_base_id is not None and staged_base_dir is None:
            _LOG.info(
                f"Fragment {frag_id} checkpoint references unknown base "
                f"{staged_base_id}; invalidating checkpoint"
            )
            return None

        if staged_base_dir is not None:
            session_root = staged_base_dir
            if URL(session_root).scheme == "":
                session_root = f"file://{session_root}"
            staging_path = file_path
            # Namespace deployments carry no table_ref.storage_options; the
            # multi-base wrapper resolved credentials for its base stores at
            # wrap time, so reuse them for the base staging probe.
            probe_storage_options = storage_options
            if probe_storage_options is None:
                probe_storage_options = getattr(
                    checkpoint_store, "base_storage_options", None
                )
            session_kwargs: dict = {"storage_options": probe_storage_options}
        else:
            base_url = URL(uri)
            if base_url.scheme == "":
                base_url = URL(f"file://{uri}")
            session_root = str(base_url)
            staging_path = f"data/{file_path}"
            session_kwargs = {"namespace_client": namespace, "table_id": table_id}
        try:
            file_session = LanceFileSession(session_root, **session_kwargs)
            if file_session.contains(staging_path):
                # Existence is not enough: a crash can leave an empty or partial
                # staged file. Reprocess unless it is a complete output.
                if _staged_data_file_is_complete(
                    file_session, staging_path, expected_rows
                ):
                    _LOG.info(
                        f"Fragment {frag_id} data file exists in staging: "
                        f"{session_root}/{staging_path}"
                    )
                    return file_path, staged_base_id
                _LOG.info(
                    f"Fragment {frag_id} staged file {staging_path} is empty or "
                    "incomplete; invalidating checkpoint"
                )
                return None
        except Exception as e:
            _LOG.debug(f"Failed to check staging location {staging_path}: {e}")

        try:
            fragment = dataset.get_fragment(frag_id)
            if fragment is not None:
                # Check if any data files in the fragment match our expected file
                for data_file in fragment.data_files():
                    if data_file.path == file_path:
                        _LOG.info(
                            f"Fragment {frag_id} data file exists in target: "
                            f"{data_file.path}"
                        )
                        return file_path, getattr(data_file, "base_id", None)
        except Exception as e:
            _LOG.debug(f"Failed to check target location for fragment {frag_id}: {e}")

    except Exception as e:
        _LOG.debug(f"Failed to check fragment data file for {frag_id}: {e}")

    return None


def _num_tasks(
    *,
    uri: str,
    read_version: int | None = None,
    task_size: int = DEFAULT_CHECKPOINT_ROWS,
    namespace_client: Optional["LanceNamespace"] = None,
    table_id: Optional[list[str]] = None,
    storage_options: dict[str, str] | None = None,
) -> int:
    if task_size <= 0:
        return 1

    # Open dataset with namespace if available
    from geneva.db import open_lance_dataset

    dataset = open_lance_dataset(
        uri,
        table_id=table_id,
        version=read_version,
        namespace_client=namespace_client,
        storage_options=storage_options,
    )

    return sum(-(-frag.count_rows() // task_size) for frag in dataset.get_fragments())


def _buffered_shuffle(it: Iterator[T], buffer_size: int) -> Iterator[T]:
    """Shuffle an iterator using a buffer of size buffer_size
    not perfectly random, but good enough for spreading out IO
    """
    # Initialize the buffer with the first buffer_size items from the iterator
    buffer = []
    # Fill the buffer with up to buffer_size items initially
    try:
        for _ in range(buffer_size):
            item = next(it)
            buffer.append(item)
    except StopIteration:
        pass

    while True:
        # Select a random item from the buffer
        index = random.randint(0, len(buffer) - 1)
        item = buffer[index]

        # Try to replace the selected item with a new one from the iterator
        try:
            next_item = next(it)
            buffer[index] = next_item
            # Yield the item AFTER replacing it in the buffer
            # this way the buffer is always contiguous so we can
            # simply yield the buffer at the end
            yield item
        except StopIteration:
            yield from buffer
            break


R = TypeVar("R")


def diversity_aware_shuffle(
    it: Iterator[T],
    key: Callable[[T], R],
    *,
    diversity_goal: int = 4,
    buffer_size: int = 1024,
) -> Iterator[T]:
    """A shuffle iterator that is aware of the diversity of the data
    being shuffled. The key function should return a value that is
    is used to determine the diversity of the data. The diversity_goal
    is the number of unique values that should be in the buffer at any
    given time. if the buffer is full, the items is yielded in a round-robin
    fashion. This is useful for shuffling tasks that are diverse, but

    This algorithm is bounded in memory by the buffer_size, so it is reasonably
    efficient for large datasets.
    """

    # NOTE: this is similar to itertools.groupby, but with a buffering limit

    buffer: dict[R, list[T]] = {}
    buffer_total_size = 0

    peekable_it = more_itertools.peekable(it)

    def _maybe_consume_from_iter() -> bool:
        nonlocal buffer_total_size
        item = peekable_it.peek(default=None)
        if item is None:
            return False
        key_val = key(item)
        if key_val not in buffer and len(buffer) < diversity_goal:
            buffer[key_val] = []
        else:
            return False

        # if the buffer still has room, add the item
        if buffer_total_size < buffer_size:
            buffer[key_val].append(item)
            buffer_total_size += 1
        else:
            return False

        next(peekable_it)
        return True

    while _maybe_consume_from_iter():
        ...

    production_counter = 0

    def _next_key() -> T | None:
        nonlocal buffer_total_size, production_counter
        if not buffer_total_size:
            return None

        # TODO: add warning about buffer size not big enough for diversity_goal
        buffer_slot = production_counter % len(buffer)
        key_val = next(itertools.islice(buffer.keys(), buffer_slot, buffer_slot + 1))
        assert key_val in buffer
        key_buffer = buffer[key_val]

        buffer_total_size -= 1
        item = key_buffer.pop(0)
        if not key_buffer:
            del buffer[key_val]

        # try to fill the removed buffer slot
        _maybe_consume_from_iter()
        production_counter += 1
        return item

    while (item := _next_key()) is not None:
        yield item


def detect_backfill_mismatches(
    table,
    col_name: str,
    udf,
    read_version: int | None,
) -> tuple[bool, bool]:
    """Detect UDF version and srcfiles mismatches for a backfill column.

    Parameters
    ----------
    table
        The Geneva ``Table`` instance.
    col_name
        Target column name.
    udf
        Resolved UDF (may be ``None`` if no UDF is associated).
    read_version
        Table version to read from.

    Returns
    -------
    tuple[bool, bool]
        ``(udf_mismatch, srcfiles_mismatch)``
    """
    udf_mismatch = False
    srcfiles_mismatch = False

    if udf is None:
        return udf_mismatch, srcfiles_mismatch

    col_schema = table._ltbl.schema
    col_field = col_schema.field(col_name)
    checkpoint_store = table.get_reference().open_checkpoint_store()

    # Multi-base tables keep fragment checkpoints in each fragment's storage
    # base; wrap so mismatch detection sees the base-routed keys (mirrors
    # Table.cleanup_checkpoints). Without this, has_udf_version_mismatch /
    # has_srcfiles_hash_mismatch list an empty table root and silently skip
    # recomputation of stale rows.
    try:
        from geneva.utils.multi_base import (
            FragmentBasePlacement,
            maybe_wrap_checkpoint_store_for_bases,
        )

        # to_lance: fresh — base placement needs the live manifest, once per call
        placement = FragmentBasePlacement.from_dataset(table.to_lance())
        checkpoint_store = maybe_wrap_checkpoint_store_for_bases(
            checkpoint_store, placement, include_unused_bases=True
        )
    except Exception:
        _LOG.debug(
            "mismatch detection: failed to resolve multi-base roots",
            exc_info=True,
        )

    from geneva.table import _get_udf_name_from_field

    udf_name = _get_udf_name_from_field(col_field)
    # Compare against the token embedded in the key (override or version), which
    # is what the store's has_udf_version_mismatch reads back from the key.
    udf_version = udf.checkpoint_version
    if udf_name and udf_version:
        try:
            udf_mismatch = checkpoint_store.has_udf_version_mismatch(
                col_name, udf_version
            )
        except Exception as e:
            _LOG.debug("Error checking checkpoint UDF versions: %s", e)

    # Check for srcfiles mismatch (indicates input column data changed)
    if not udf_mismatch and udf.input_columns:
        try:
            from geneva.checkpoint_utils import hash_source_files
            from geneva.db import open_lance_dataset
            from geneva.runners.ray.pipeline import (
                _get_relevant_field_ids,
                get_source_data_files,
            )

            dataset = open_lance_dataset(
                table.uri,
                version=read_version,
                storage_options=table._storage_options,
            )
            input_field_ids = _get_relevant_field_ids(dataset, udf.input_columns)
            if input_field_ids:
                fragments = list(dataset.get_fragments())
                if fragments:
                    current_src_files = get_source_data_files(
                        fragments[0], input_field_ids
                    )
                    current_hash = hash_source_files(current_src_files)
                    srcfiles_mismatch = checkpoint_store.has_srcfiles_hash_mismatch(
                        col_name, current_hash
                    )
        except Exception as e:
            _LOG.debug("Error checking srcfiles hash: %s", e)

    return udf_mismatch, srcfiles_mismatch


def resolve_backfill_where(
    col_name: str,
    col_field,
    where: str | None,
    udf_mismatch: bool,
    srcfiles_mismatch: bool,
    *,
    default_where: str | None = None,
) -> str | None:
    """Resolve the effective WHERE filter for a backfill operation.

    Extracts the WHERE-decision-tree logic from ``backfill_async()`` so it can
    be reused by the dry-run / plan path.

    Parameters
    ----------
    col_name
        Target column name.
    col_field
        ``pyarrow.Field`` for the column (used for struct-type check).
    where
        User-supplied WHERE filter (``None`` means "use default").
    udf_mismatch
        Whether a UDF version mismatch was detected.
    srcfiles_mismatch
        Whether a srcfiles hash mismatch was detected.
    default_where
        Optional caller-supplied default filter. Multi-output UDF groups use
        this to backfill the whole sibling group when any output column is NULL.

    Returns
    -------
    str | None
        The effective WHERE filter to apply.
    """
    has_mismatch = udf_mismatch or srcfiles_mismatch
    user_provided_where = where is not None

    if user_provided_where and has_mismatch:
        mismatch_type = "UDF version" if udf_mismatch else "input column data"
        _LOG.warning(
            "Column %s has %s changes but explicit where filter provided. "
            "Some rows computed with old UDF/data may not be reprocessed. "
            "Use where='1=1' to force reprocessing all rows.",
            col_name,
            mismatch_type,
        )
    elif where is None:
        if has_mismatch:
            mismatch_type = "UDF version" if udf_mismatch else "input column data"
            _LOG.info(
                "%s changed for column %s, processing all rows",
                mismatch_type.capitalize(),
                col_name,
            )
        elif pa.types.is_struct(col_field.type):
            # Struct columns: IS NULL doesn't work effectively because a struct
            # with NULL fields is not the same as a NULL struct. Skip the filter
            # and process all rows (less efficient but correct).
            pass
        else:
            where = default_where or f"{col_name} IS NULL"

    return where
