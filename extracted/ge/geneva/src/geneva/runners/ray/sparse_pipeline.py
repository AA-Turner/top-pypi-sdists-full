# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Distributed sparse row update, fanned out by fragment range.

Splits all fragments into ranges and fans the ranges out across a Ray actor pool,
committing the results with ``SparseCommitManager``. Mirrors the chunker's direct
``ActorPool`` usage (a dedicated actor + ``map_unordered``). The unit is a
``SparseRangeTask`` (a fragment range), not a single fragment -- so there is NO
driver-side planning scan: each actor scans its own range to discover its matches.

Each actor loads the UDF once and runs ``sparse_update_range`` for every range
it is handed: ONE scan over the range, run the UDF, write the range's replacement
fragments in one ``write_fragments`` + a deletion vector per matched fragment, and
return metadata only. The driver assembles those into chunked atomic ``Update``
commits.
"""

from __future__ import annotations

import functools
import logging
import typing

from geneva.apply.task import SparseRangeTask
from geneva.runners.ray.actor_pool import ActorPool
from geneva.runners.sparse_update import (
    DEFAULT_BATCH_BYTES,
    RangeSparseResult,
    SparseCommitManager,
    SparseUpdateError,
    SparseUpdateResult,
    _chunk_fragments,
    _estimate_batch_rows,
    lance_field_id,
    resolve_commit_granularity,
    validate_sparse_scope,
)

if typing.TYPE_CHECKING:
    import lance

    from geneva.table import TableReference
    from geneva.transformer import UDF

_LOG = logging.getLogger(__name__)


def _make_sparse_actor() -> typing.Any:
    """Lazily define the SparseActor (defers ``import ray`` until needed)."""
    import ray
    from tenacity import (
        Retrying,
        retry_if_exception,
        stop_after_attempt,
        wait_exponential_jitter,
    )

    from geneva.runners.ray.pipeline import _picklable_remote_error
    from geneva.runners.sparse_update import sparse_update_range
    from geneva.utils import object_store_retry

    @ray.remote
    class SparseActor:
        """Runs a fragment RANGE's sparse update, with the same
        robustness as the carry-forward ApplierActor: the UDF and the dataset are
        opened once per actor (not per range -- avoids re-reading a huge manifest),
        transient object-store errors are retried with backoff, and a terminal
        failure is returned as an error result (carrying the range it covered) so
        the driver counts + skips that range rather than aborting the job."""

        def __init__(self, udf: UDF) -> None:
            self._udf = udf
            self._ds_cache: dict = {}  # (uri, version) -> dataset, opened once

        def _dataset(self, task: SparseRangeTask) -> lance.LanceDataset:
            key = (task.uri, task.version)
            ds = self._ds_cache.get(key)
            if ds is None:
                # to_lance: fresh — sparse write path needs a live manifest
                ds = task.table_ref_for_read().open().to_lance()
                self._ds_cache[key] = ds
            return ds

        def run(self, task: SparseRangeTask) -> object:
            ds = self._dataset(task)
            max_retries, base, mx = object_store_retry.get_applier_retry_settings()
            retrier = Retrying(
                retry=retry_if_exception(
                    object_store_retry.is_retryable_object_store_error
                ),
                stop=stop_after_attempt(max_retries + 1),
                wait=wait_exponential_jitter(initial=base, max=mx),
                reraise=True,
            )
            try:
                for attempt in retrier:
                    with attempt:
                        return sparse_update_range(
                            ds,
                            task.frag_ids,
                            self._udf,
                            task.where,
                            task.output_column,
                            task.batch_rows,
                        )
            except Exception as exc:  # noqa: BLE001 -- terminal: isolate the range
                return RangeSparseResult(
                    [],
                    0,
                    [],
                    [],
                    [],
                    error=str(_picklable_remote_error(exc)),
                    source_frag_ids=task.frag_ids,
                )

    return SparseActor


def run_ray_sparse_update(
    table_ref: TableReference,
    udf: UDF,
    where: str,
    output_column: str,
    *,
    read_version: int | None = None,
    concurrency: int = 8,
    commit_granularity: int | None = None,
    batch_bytes: int = DEFAULT_BATCH_BYTES,
    job_tracker: typing.Any = None,
    job_id: str = "local",
) -> SparseUpdateResult:
    """Re-derive work from the live dataset each round and fan it out, until a
    round finds no new matches.

    ``read_version`` pins only the admission snapshot, not a read fence: each round
    reads the LATEST dataset (so it can follow a concurrent compaction), which means
    sparse fills all currently-matching rows -- including any appended after the call.
    A historical ``read_version`` is rejected up front (sparse cannot honor an old
    snapshot); with no concurrent writer this is identical to carry-forward.

    Re-derive work each round: ``process = current fragments minus produced``. Each
    round splits the unprocessed fragments into ranges, fans them out across a Ray
    actor pool (each actor scans its own range -- no driver-side planning scan),
    and commits the results. A range that fails is recorded and not retried.

    The produced-set is the set of fragment ids this run has appended -- every such
    fragment is wholly replacement rows, so excluding it whole needs no per-row
    addresses. Its size is O(appended fragments), not O(matched rows). When a
    concurrent compaction rewrites an appended fragment, its id disappears and is
    dropped from the set; the rewritten fragment is re-scanned and its rows
    re-processed. That is safe because the produced-set is a best-effort EFFICIENCY
    aid, not a correctness mechanism: geneva assumes UDFs are idempotent and
    delete-by-address uses freshly scanned addresses, so re-processing a row is
    value-correct (no duplication) and merely wastes a recompute -- which is why we
    track fragments, not stable row ids.
    """
    import attrs
    import lance

    if read_version is not None and table_ref.version != read_version:
        table_ref = attrs.evolve(table_ref, version=read_version)
    table = table_ref.open()
    # to_lance: fresh — driver Update commit needs a live manifest
    ds = table.to_lance()
    validate_sparse_scope(ds, udf, where, output_column)

    uri = ds.uri
    base_version = ds.version
    # Row total from fragment metadata, NOT count_rows() -- on a stable-row-id
    # table count_rows full-scans (no count pushdown), which at 40B rows is a
    # huge needless scan on the driver just for a metric + the batch estimate.
    base_frags = ds.get_fragments()
    fragments_total = len(base_frags)
    rows_total = sum(f.physical_rows for f in base_frags)
    batch_rows = _estimate_batch_rows(ds, rows_total, batch_bytes)
    output_fid = lance_field_id(ds, output_column)

    actor_cls = _make_sparse_actor()
    actor_factory = functools.partial(actor_cls.remote, udf)

    if job_tracker is not None:
        job_tracker.set_total.remote("fragments", fragments_total)
        job_tracker.set_desc.remote("fragments", "fragments updated")
        job_tracker.set.remote("fragments", 0)
        job_tracker.set_desc.remote("rows_committed", "rows updated")

    produced_frags: set[int] = set()
    failed_frags: set[int] = set()
    rows_matched = 0
    fragment_equiv_rows = 0
    touched: set[int] = set()
    committed_version: int | None = None

    while True:
        cur = lance.dataset(uri, storage_options=table_ref.storage_options)
        cur_frags = cur.get_fragments()
        # Drop produced fragments a compaction has rewritten (their ids are gone);
        # the rewritten fragment falls back into candidates and its rows re-process.
        produced_frags &= {f.fragment_id for f in cur_frags}
        cur_version = cur.version
        candidates = [
            f.fragment_id
            for f in cur_frags
            if f.fragment_id not in produced_frags and f.fragment_id not in failed_frags
        ]
        if not candidates:
            break

        granularity = resolve_commit_granularity(commit_granularity, len(candidates))
        round_ref = attrs.evolve(table_ref, version=cur_version)
        tasks = [
            SparseRangeTask(
                uri=uri,
                table_ref=round_ref,
                frag_ids=rng,
                where=where,
                output_column=output_column,
                version=cur_version,
                batch_rows=batch_rows,
            )
            for rng in _chunk_fragments(candidates, granularity)
        ]
        manager = SparseCommitManager(
            cur, output_fid, granularity, storage_options=table_ref.storage_options
        )
        num_actors = max(1, min(concurrency, len(tasks)))
        pool = ActorPool(actor_factory, num_actors, job_tracker=job_tracker)
        try:
            for res in pool.map_unordered(
                lambda actor, task: actor.run.remote(task), tasks
            ):
                if job_tracker is not None:
                    job_tracker.increment.remote("fragments", len(res.source_frag_ids))
                if res.error is not None:
                    failed_frags.update(res.source_frag_ids)
                    _LOG.error(
                        "sparse update: range of %d fragments failed: %s",
                        len(res.source_frag_ids),
                        res.error,
                    )
                    continue
                if res.rows_matched == 0:
                    continue
                rows_matched += res.rows_matched
                touched.update(res.touched_frag_ids)
                fragment_equiv_rows += sum(
                    f.physical_rows
                    for fid in res.touched_frag_ids
                    if (f := cur.get_fragment(fid)) is not None
                )
                manager.ingest_range(res)
                if job_tracker is not None:
                    job_tracker.increment.remote("rows_committed", res.rows_matched)
            manager.flush()
        finally:
            pool.shutdown()
        committed_version = manager.committed_version or committed_version
        produced_frags |= manager.produced_frags
        # Re-scan only if a compaction advanced the version beyond our own commits;
        # otherwise this round processed the whole snapshot in one pass (the
        # appended replacements were never in its candidate set). Keeps a
        # no-compaction run to a single fan-out, not a redundant confirm pass.
        latest = lance.dataset(uri, storage_options=table_ref.storage_options).version
        if manager.commit_count == 0 or latest - cur_version == manager.commit_count:
            break

    if job_tracker is not None:
        job_tracker.mark_done.remote("fragments")
    _LOG.info(
        "sparse update (distributed): matched %d/%d rows across %d/%d fragments "
        "(%.1fx amplification saved)",
        rows_matched,
        rows_total,
        len(touched),
        fragments_total,
        (fragment_equiv_rows / rows_matched) if rows_matched else 1.0,
    )
    result = SparseUpdateResult(
        base_version=base_version,
        committed_version=committed_version,
        rows_total=rows_total,
        rows_matched=rows_matched,
        rows_written=rows_matched,
        fragments_total=fragments_total,
        fragments_touched=len(touched),
        fragment_equiv_rows=fragment_equiv_rows,
        fragments_failed=len(failed_frags),
    )
    # Don't let range failures pass as a successful job. Succeeded ranges are
    # committed (a failed range commits nothing, so there is no half-applied
    # state); surfacing the failure lets the caller see it and re-run.
    if failed_frags:
        raise SparseUpdateError(
            f"sparse update: {len(failed_frags)} fragment(s) failed and were NOT "
            f"updated; committed at version {committed_version}. Re-run to retry "
            f"the failed fragments.",
            result,
        )
    return result
