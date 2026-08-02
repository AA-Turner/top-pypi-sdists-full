# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Sparse row update path for low-selectivity filtered backfills.

Instead of treating a
filtered backfill as a fragment-aligned column-file replacement, this path
treats the matched rows as the unit of work: the planner reads only selected
rows, the task runs the UDF only on those rows, and the committer publishes
replacement rows with an atomic deletion-vector + append
(``LanceOperation.Update``) so read and write cost is proportional to matched
rows, not touched fragments.

The two backfill modes split at job planning time. Sparse mode decomposes by
fragment RANGE so the work fans out across the cluster::

    fragment mode:  ScanTask -> BackfillUDFTask -> FragmentWriter -> DataReplacement
    sparse mode:    split fragments into ranges -> sparse_update_range -> Update commit

Each ``sparse_update_range`` is independent: ONE scan over its range discovers
that range's matched rows (so there is no separate planning scan), runs the UDF,
writes the range's replacement rows in one ``write_fragments``, and builds a
deletion vector per matched fragment -- all returned as metadata. The driver
assembles those into the atomic ``Update`` commit, once or every
``commit_granularity`` fragments. Sparse mode does not preserve fragment layout
or physical row addresses; progress is tracked by the driver's produced-set
(the fragment ids it has appended, dropped when a compaction rewrites them), so
it needs no stable row ids and no done-markers.
"""

from __future__ import annotations

import typing

import attrs
import lance
import numpy as np
import pyarrow as pa

from geneva.committer import get_committer
from geneva.utils.commit_conflict import is_retryable_commit_conflict

if typing.TYPE_CHECKING:
    from collections.abc import Iterator

    from geneva.transformer import UDF

SPARSE_UPDATE_MODE = "sparse_rows"

# Target bytes held by a single streamed read batch; bounds peak memory.
DEFAULT_BATCH_BYTES = 32 * 1024 * 1024

# lance write_fragments defaults -- used as a fallback when the source table's own
# per-fragment sizes can't be determined, so appended fragments are otherwise
# capped to the table's fragmentation, not these.
_LANCE_DEFAULT_ROWS_PER_FILE = 1024 * 1024
_LANCE_DEFAULT_BYTES_PER_FILE = 90 * 1024 * 1024 * 1024  # 90 GiB


class SparseScopeError(ValueError):
    """Raised when a table/UDF/filter cannot satisfy the sparse-update contract.

    Sparse mode rejects up front rather than silently falling back to the fragment
    path -- a silent fallback would make an expensive fragment rewrite look like a
    successful sparse update.
    """


@attrs.define
class SparseUpdateResult:
    """Outcome + amplification metrics for a sparse row update.

    The amplification fields make the improvement locally verifiable: sparse
    mode reads/writes ``rows_matched`` rows, whereas the fragment-preserving
    path reads/writes every row of every touched fragment
    (``fragment_equiv_rows``). ``amplification_saved`` is their ratio.
    """

    base_version: int
    committed_version: int | None
    rows_total: int
    rows_matched: int
    rows_written: int
    fragments_total: int
    fragments_touched: int
    fragment_equiv_rows: int
    fragments_failed: int = 0

    @property
    def amplification_saved(self) -> float:
        if self.rows_matched == 0:
            return 1.0
        return self.fragment_equiv_rows / self.rows_matched

    @property
    def selectivity(self) -> float:
        if self.rows_total == 0:
            return 0.0
        return self.rows_matched / self.rows_total


class SparseUpdateError(RuntimeError):
    """Raised when one or more fragment ranges failed during a sparse update.

    A failed range commits nothing (no half-applied state, so there are no orphaned
    hidden rows), and the ranges that succeeded ARE
    committed -- but the job must not report success while leaving matched rows
    un-updated. Re-running re-scans the still-matching rows and re-applies the
    UDF; an idempotent UDF makes re-processing any already-committed replacement
    harmless (re-deleted by address and re-appended, no duplication). ``result``
    carries the partial metrics
    (``committed_version``, ``fragments_failed``) for programmatic callers.
    """

    def __init__(self, message: str, result: SparseUpdateResult) -> None:
        super().__init__(message)
        self.result = result


def lance_field_id(ds: lance.LanceDataset, column: str) -> int:
    """Return the Lance field id for a top-level column name."""
    return ds.lance_schema.field(column).id()  # pyright: ignore[reportAttributeAccessIssue]


def validate_sparse_scope(
    ds: lance.LanceDataset,
    udf: UDF | None,
    where: str | None,
    output_column: str,
) -> None:
    """Admission check for the sparse fill. Raises SparseScopeError on violation.

    Any ``where`` predicate is allowed: the driver excludes the whole fragments it
    has appended from later rounds, so an arbitrary, non-self-excluding filter does
    not skip rows -- no stable row ids needed. A concurrent compaction that rewrites
    an appended fragment just re-exposes its rows, which an idempotent UDF
    re-processes harmlessly. Requires a non-empty filter and an existing output
    column. The UDF is assumed 1:1 (one row in, one row out) -- backfill only routes
    scalar/array/record-batch UDFs here, so a one-to-many transform never reaches
    this check.
    """
    if where is None or not where.strip():
        raise SparseScopeError("sparse update requires a non-empty `where` predicate")
    if output_column not in ds.schema.names:
        raise SparseScopeError(
            f"sparse update targets existing output column {output_column!r}, "
            f"which is not in the table schema {ds.schema.names}"
        )


def _estimate_batch_rows(
    ds: lance.LanceDataset, rows_total: int, batch_bytes: int
) -> int:
    """Rows per streamed batch that hold ~``batch_bytes``, from the average
    on-disk row size. Keeps peak memory bounded by one batch regardless of how
    large the matched set is (and small for big-blob rows)."""
    if rows_total <= 0:
        return 1024
    on_disk = sum(
        (df.file_size_bytes or 0)
        for frag in ds.get_fragments()
        for df in frag.data_files()
    )
    avg_row = max(1, on_disk // rows_total)
    return max(1, min(batch_bytes // avg_row, 1_000_000))


_AUTO_COMMIT_GRANULARITY_FLOOR = 64


def resolve_commit_granularity(configured: int | None, num_fragments: int) -> int:
    """Fragments per ``Update`` commit. Auto-scale when unset so we never commit
    one manifest over tens of thousands of fragments (a single huge Update is
    itself a bottleneck). Mirrors the carry-forward planner's resolver."""
    if configured is not None:
        return max(1, int(configured))
    return max(_AUTO_COMMIT_GRANULARITY_FLOOR, (max(0, num_fragments) + 19) // 20)


def _chunk_fragments(frag_ids: list[int], size: int) -> list[list[int]]:
    """Split fragment ids into contiguous ranges of at most ``size``."""
    size = max(1, size)
    return [frag_ids[i : i + size] for i in range(0, len(frag_ids), size)]


@attrs.define
class RangeSparseResult:
    """Sparse update output for a RANGE of fragments: metadata only, no commit.

    The driver assembles ``new_fragments`` + ``updated_fragments`` from every
    range into one atomic ``LanceOperation.Update``.
    """

    touched_frag_ids: list[int]  # source fragments in the range that had matches
    rows_matched: int
    new_fragments: list  # replacement-row fragments for the whole range
    updated_fragments: list  # touched source fragments, each with its new DV
    removed_fragment_ids: list[int]  # fragments where every row matched
    error: str | None = None  # set when the range failed; nothing committed
    source_frag_ids: list[int] = attrs.field(factory=list)  # the whole range covered


def _field_has_blob(field: pa.Field) -> bool:
    """True if the field (incl. struct/list leaves) is lance blob-encoded."""
    if b"lance-encoding:blob" in (field.metadata or {}):
        return True
    t = field.type
    if pa.types.is_struct(t):
        return any(_field_has_blob(t.field(i)) for i in range(t.num_fields))
    if pa.types.is_list(t) or pa.types.is_large_list(t):
        return _field_has_blob(t.value_field)
    return False


def _blob_columns(schema: pa.Schema) -> list[str]:
    """Top-level column names carrying a lance blob-encoded field."""
    return [f.name for f in schema if _field_has_blob(f)]


_U64 = (1 << 64) - 1


def _mix64(x: int) -> int:
    """splitmix64 finalizer: decorrelates the range anchor from its stride.

    Fragment ranges start at multiples of the commit granularity, so a raw
    ``anchor % n_bases`` collapses to one base whenever the granularity is a
    multiple of ``n_bases`` (e.g. 400-fragment ranges over 25 bases -> every
    range hits base 1). Mixing the anchor first spreads the distinct anchor
    values uniformly regardless of the stride, while staying deterministic.
    """
    x = (x + 0x9E3779B97F4A7C15) & _U64
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & _U64
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & _U64
    return (x ^ (x >> 31)) & _U64


def _target_base_for_range(ds: lance.LanceDataset, source_ids: list[int]) -> str | None:
    """Registered non-primary base to receive this range's replacement fragments.

    Sparse replacements are new appended fragments; with no ``target_bases`` they
    land in the dataset root (the primary storage account), concentrating every
    repair write's ingress on one account. On a multi-base table, spread them
    across the registered non-primary bases by a hash of the range's first source
    fragment id — deterministic (stable across actors/retries so the same range
    always targets the same base) yet decorrelated from the commit-granularity
    stride (a raw modulo would collapse to one base when the range size is a
    multiple of the base count). Returns the reference for
    ``write_fragments(target_bases=...)`` (the base name when present, else its
    path URI), or ``None`` for a single-base dataset / a pylance without
    multi-base support, preserving the current root-append behavior.
    """
    base_paths_fn = getattr(getattr(ds, "_ds", None), "base_paths", None)
    if base_paths_fn is None:
        return None
    # Every entry of base_paths() is a valid target: it returns only the
    # registered (added) bases -- the primary dataset root is never among them.
    # Do NOT filter on ``is_dataset_root``; that flag is a data-LAYOUT hint (data
    # under ``{base}/data`` vs ``{base}`` directly) that a secondary base may
    # legitimately carry, not a "this is the primary root" marker -- filtering it
    # would drop real bases and silently fall back to root. Mirrors
    # resolve_dataset_bases / FragmentBasePlacement.from_dataset.
    bases = list(base_paths_fn().values())
    if not bases:
        return None
    bases.sort(key=lambda bp: (getattr(bp, "id", None) or 0, str(bp.path)))
    anchor = source_ids[0] if source_ids else 0
    chosen = bases[_mix64(anchor) % len(bases)]
    return chosen.name or str(chosen.path)


def sparse_update_range(
    ds: lance.LanceDataset,
    frag_ids: list[int],
    udf: UDF,
    where: str,
    output_column: str,
    batch_rows: int,
    *,
    dv_concurrency: int = 8,
) -> RangeSparseResult:
    """Batched sparse update for a RANGE of fragments, without committing.

    ONE scan over the range (``scanner(fragments=...)``) both DISCOVERS the
    range's matched rows and feeds the UDF -- so there is no separate planning
    scan; each range finds its own matches. Replacements stream to ONE
    ``write_fragments`` (a few right-sized fragments, not one tiny fragment per
    source fragment). Deletion vectors for the range's matched fragments are
    built in a thread pool -- the calls are independent and release the GIL, so
    this is the dominant phase and parallelizes well. Returns metadata for the
    driver to assemble into a ``LanceOperation.Update``.

    This is the unit the Ray path fans out: each actor owns a fragment range, so
    the planning scan is distributed away and the per-fragment apply/write debt
    (tiny fragments) is gone. A range of one fragment is the degenerate case.

    For an ``IS NULL`` fill the UDF must produce non-null output: a row it leaves
    NULL still matches the filter, so it would be re-appended on a retry and never
    converge (there is no durable identity to dedupe against).
    """
    frags = [f for fid in frag_ids if (f := ds.get_fragment(fid)) is not None]
    source_ids = [f.fragment_id for f in frags]
    if not frags:
        return RangeSparseResult([], 0, [], [], [], source_frag_ids=source_ids)
    names = list(ds.schema.names)
    blob_cols = _blob_columns(ds.schema)
    blob_handling = "all_binary" if blob_cols else None
    addr_chunks: list[pa.Array] = []
    counter = {"n": 0}

    def replacements() -> Iterator[pa.RecordBatch]:
        scanner_kwargs: dict[str, typing.Any] = {
            "fragments": frags,
            "columns": names,
            "filter": where,
            "batch_size": batch_rows,
            "batch_readahead": 1,
            "blob_handling": blob_handling,
            "with_row_address": True,
        }
        if blob_cols:
            # all_binary alone materializes every scanned row's payload before
            # the filter; forcing blobs late defers it to matched rows only.
            scanner_kwargs["late_materialization"] = blob_cols
        scanner = ds.scanner(**scanner_kwargs)
        for batch in scanner.to_batches():
            addr_col = batch.column(batch.schema.get_field_index("_rowaddr"))
            addr_chunks.append(addr_col)
            core = batch.select(names)
            counter["n"] += core.num_rows
            udf_out = udf(core, use_applier=True)
            if isinstance(udf_out, pa.ChunkedArray):
                udf_out = udf_out.combine_chunks()
            yield pa.record_batch(
                [
                    udf_out if f.name == output_column else core.column(f.name)
                    for f in ds.schema
                ],
                schema=ds.schema,
            )

    # Cap appended fragments at this range's largest source fragment (by rows and
    # bytes), not lance's larger defaults -- else a deliberately small-fragmented
    # table (wide/blob rows) gets appended fragments far bigger than the rest.
    src_rows = max((f.physical_rows for f in frags), default=0)
    src_bytes = max(
        (sum(df.file_size_bytes or 0 for df in f.data_files()) for f in frags),
        default=0,
    )
    # Multi-base: route replacement fragments to a registered base (spread across
    # bases) so repair-write ingress fans out instead of piling on the primary
    # account. None on single-base datasets -> append to root as before. The base
    # account is carried in the base URI (abfss), so no base_store_params here;
    # write_fragments inherits any the dataset was opened with.
    target_base = _target_base_for_range(ds, source_ids)
    target_base_kwargs: dict[str, typing.Any] = (
        {"target_bases": [target_base]} if target_base is not None else {}
    )
    reader = pa.RecordBatchReader.from_batches(ds.schema, replacements())
    # write-guard-ok: sparse-path durable write, not yet routed through an indirection
    new_fragments = lance.fragment.write_fragments(
        reader,
        ds,
        mode="append",
        max_rows_per_group=batch_rows,
        max_rows_per_file=src_rows or _LANCE_DEFAULT_ROWS_PER_FILE,
        max_bytes_per_file=src_bytes or _LANCE_DEFAULT_BYTES_PER_FILE,
        **target_base_kwargs,
    )
    if counter["n"] == 0:
        return RangeSparseResult([], 0, [], [], [], source_frag_ids=source_ids)

    # Group matched rows by source fragment, keeping each row's local offset.
    # _rowaddr is global: high 32 bits = fragment id, low 32 bits = row offset.
    rowaddr = pa.chunked_array(addr_chunks).combine_chunks().to_numpy()
    frag_of = (rowaddr >> 32).astype(np.int64).tolist()
    off_of = (rowaddr & 0xFFFFFFFF).astype(np.int64).tolist()
    offsets_by_frag: dict[int, list[int]] = {}
    for fid_v, off_v in zip(frag_of, off_of, strict=True):
        offsets_by_frag.setdefault(fid_v, []).append(off_v)
    touched = sorted(offsets_by_frag)

    # The per-fragment DV is the dominant phase; the delete calls are independent
    # and release the GIL during the native scan, so a thread pool overlaps them.
    from concurrent.futures import ThreadPoolExecutor

    workers = max(1, min(dv_concurrency, len(touched)))

    # Delete the rows we matched BY ADDRESS, not by re-evaluating the predicate.
    # Re-evaluating would (a) mishandle blob columns (a NULL blob reads NULL under
    # the scan but as a zero descriptor under a predicate delete) and (b) for an
    # arbitrary predicate, delete produced replacement rows that a compaction has
    # merged into this fragment. Deleting the exact scanned offsets keeps the
    # deletion vector consistent with what we appended.
    def _build_dv(fid: int) -> tuple[int, object | None]:
        # write-guard-ok: sparse-path durable write, not yet routed
        return fid, lance.LanceFragment(ds, fid).delete_rows(offsets_by_frag[fid])

    with ThreadPoolExecutor(max_workers=workers) as ex:
        metas = list(ex.map(_build_dv, touched))
    updated = [m for _, m in metas if m is not None]
    removed = [fid for fid, m in metas if m is None]
    return RangeSparseResult(
        touched,
        counter["n"],
        new_fragments,
        updated,
        removed,
        source_frag_ids=source_ids,
    )


@attrs.define
class SparseCommitManager:
    """Accumulate ``RangeSparseResult``s and commit them as atomic
    ``LanceOperation.Update``s -- a deletion vector per touched fragment plus the
    appended replacement fragments -- every ``commit_granularity`` fragments (so a
    single Update never spans tens of thousands), retrying on version conflicts.
    Progress tracking is the driver's job (the produced-set), not this committer's.
    """

    ds: lance.LanceDataset
    output_field_id: int
    commit_granularity: int | None = None
    storage_options: dict | None = None
    max_conflict_retries: int = 10

    _version: int = attrs.field(init=False, default=0)
    _committed: int | None = attrs.field(init=False, default=None)
    _new: list = attrs.field(init=False, factory=list)
    _updated: list = attrs.field(init=False, factory=list)
    _removed: list = attrs.field(init=False, factory=list)
    _since_commit: int = attrs.field(init=False, default=0)
    # Fragment ids this manager has appended (the produced-set). Every appended
    # fragment is wholly replacement rows, so the driver excludes them whole from
    # later rounds -- no per-row addresses, and nothing to remap across compaction.
    produced_frags: set[int] = attrs.field(init=False, factory=set)
    # Successful Update commits this manager has made. The driver compares this to
    # the dataset's version delta to tell whether a concurrent compaction landed
    # during the round (and so whether it must re-scan).
    commit_count: int = attrs.field(init=False, default=0)
    # Fragment ids known before the next commit -- the baseline for detecting which
    # fragments a commit appended. Carried across chunked commits so we don't
    # re-attribute earlier chunks' appends. Recomputed after a conflict rebase.
    _known_frags: set | None = attrs.field(init=False, default=None)

    def __attrs_post_init__(self) -> None:
        self._version = self.ds.version

    @property
    def committed_version(self) -> int | None:
        return self._committed

    def ingest_range(self, result: RangeSparseResult) -> None:
        """Accumulate a whole range's results. ``_since_commit`` counts touched
        source fragments so ``commit_granularity`` still bounds each commit's
        manifest size regardless of range size."""
        if result.rows_matched == 0:
            return
        self._removed.extend(result.removed_fragment_ids)
        self._updated.extend(result.updated_fragments)
        self._new.extend(result.new_fragments)
        self._since_commit += len(result.touched_frag_ids)
        if self.commit_granularity and self._since_commit >= self.commit_granularity:
            self.flush()

    def flush(self) -> None:
        if not (self._new or self._updated or self._removed):
            return
        op = lance.LanceOperation.Update(
            removed_fragment_ids=self._removed,
            updated_fragments=self._updated,
            new_fragments=self._new,
            fields_modified=[self.output_field_id],
        )
        committed = self._commit(op)
        self._committed = committed.version
        self._version = committed.version
        self.commit_count += 1
        self._new.clear()
        self._updated.clear()
        self._removed.clear()
        self._since_commit = 0

    def _commit(self, op: lance.LanceOperation.BaseOperation) -> lance.LanceDataset:
        # Retry version conflicts by reopening at the latest version (the same loop
        # the carry-forward committer uses). The commit is atomic, so the fragments
        # that appear between the read version and the committed version are exactly
        # the ones this Update appended -- record their ids as produced.
        for attempt in range(self.max_conflict_retries + 1):
            try:
                if self._known_frags is None:
                    self._known_frags = {f.fragment_id for f in self.ds.get_fragments()}
                committed = get_committer().commit(
                    self.ds, op, read_version=self._version
                )
                committed_frags = committed.get_fragments()
                self.produced_frags.update(
                    f.fragment_id
                    for f in committed_frags
                    if f.fragment_id not in self._known_frags
                )
                self._known_frags = {f.fragment_id for f in committed_frags}
                return committed
            except OSError as e:  # noqa: PERF203 -- retry cost is trivial vs a commit
                last = attempt == self.max_conflict_retries
                if last or not is_retryable_commit_conflict(e):
                    raise
                self.ds = lance.dataset(
                    self.ds.uri, storage_options=self.storage_options
                )
                self._version = self.ds.version
                self._known_frags = None  # rebase: recompute the baseline on retry
        # Unreachable: the final attempt either returns or re-raises above.
        raise AssertionError("sparse commit retry loop exited without returning")
