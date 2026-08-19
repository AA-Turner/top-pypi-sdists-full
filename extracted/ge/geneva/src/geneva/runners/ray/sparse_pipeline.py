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
from time import monotonic

import attrs

from geneva.apply.task import SparseRangeTask
from geneva.errors import FatalWorkerOOMError, FatalWorkerTransientError
from geneva.runners.ray.actor_pool import (
    _MAP_STALL_TIMEOUT_S,
    ActorPool,
    ActorPoolTaskError,
)
from geneva.runners.ray.oom_recovery_budget import (
    OOMRecoveryBudgetTracker,
    init_oom_recovery_metrics,
    read_task_oom_range_key,
    record_oom_recovery_attempt,
)
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


def _sparse_task_identity(task: SparseRangeTask) -> tuple:
    """Identity of one exact sparse range/batch attempt in a driver wave."""
    return (
        task.uri,
        task.version,
        tuple(task.frag_ids),
        task.where,
        task.output_column,
        task.batch_rows,
    )


def _sparse_task_oom_range_key(task: SparseRangeTask) -> str:
    """Budget key including both sparse range and streamed batch footprint."""
    return f"{read_task_oom_range_key(task)};batch_rows={task.batch_rows}"


def _split_sparse_oom_task(task: SparseRangeTask) -> list[SparseRangeTask]:
    """Halve one explicit sparse footprint dimension, range before batch."""
    frag_ids = list(task.frag_ids)
    if len(frag_ids) > 1:
        midpoint = len(frag_ids) // 2
        return [
            attrs.evolve(task, frag_ids=frag_ids[:midpoint]),
            attrs.evolve(task, frag_ids=frag_ids[midpoint:]),
        ]

    batch_rows = max(1, int(task.batch_rows))
    if batch_rows > 1:
        return [attrs.evolve(task, batch_rows=max(1, batch_rows // 2))]
    return [task]


def _is_strictly_smaller_sparse_task(
    replacement: SparseRangeTask,
    parent: SparseRangeTask,
) -> bool:
    """Return whether a replacement strictly reduces its parent footprint."""
    parent_ids = tuple(parent.frag_ids)
    replacement_ids = tuple(replacement.frag_ids)
    if not replacement_ids or replacement.batch_rows > parent.batch_rows:
        return False
    if not set(replacement_ids).issubset(parent_ids):
        return False
    return len(replacement_ids) < len(parent_ids) or (
        replacement_ids == parent_ids and replacement.batch_rows < parent.batch_rows
    )


def _strictly_partitions_sparse_task(
    replacements: list[SparseRangeTask],
    parent: SparseRangeTask,
) -> bool:
    """Require an exact, ordered partition and a smaller footprint per child."""
    replacement_ids = [
        frag_id for replacement in replacements for frag_id in replacement.frag_ids
    ]
    return replacement_ids == list(parent.frag_ids) and all(
        _is_strictly_smaller_sparse_task(replacement, parent)
        for replacement in replacements
    )


def _replace_sparse_task(
    tasks: list[SparseRangeTask],
    failed: SparseRangeTask,
    replacements: list[SparseRangeTask],
) -> list[SparseRangeTask]:
    """Replace the exact failed attempt while preserving other unfinished work."""
    failed_identity = _sparse_task_identity(failed)
    replaced = False
    pending: list[SparseRangeTask] = []
    for task in tasks:
        if not replaced and _sparse_task_identity(task) == failed_identity:
            pending.extend(replacements)
            replaced = True
        else:
            pending.append(task)
    if not replaced:
        raise RuntimeError(
            "sparse OOM recovery lost the failed range/batch identity: "
            f"{failed_identity!r}"
        )
    return pending


def _normalize_sparse_actor_failure(exc: Exception) -> Exception:
    """Classify an actor-level sparse failure for driver recovery."""
    # Imported lazily because pipeline imports this module lazily for sparse jobs.
    from geneva.runners.ray.pipeline import (
        _get_current_k8s_pod_statuses,
        _normalize_fatal_worker_error,
    )

    return _normalize_fatal_worker_error(
        exc,
        pod_statuses=_get_current_k8s_pod_statuses(),
    )


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
                remote_error = _picklable_remote_error(exc)
                return RangeSparseResult(
                    [],
                    0,
                    [],
                    [],
                    [],
                    error=str(remote_error),
                    source_frag_ids=task.frag_ids,
                    fatal_worker_oom=isinstance(remote_error, FatalWorkerOOMError),
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
    and commits the results. An ordinary range error is recorded and not retried.
    A classified worker OOM closes the current pool, strictly shrinks the failed
    unfinished range (or its streamed batch size), and retries unfinished work on
    fresh actors under the driver-local OOM budget. Completed results stay in the
    same commit manager and are never resubmitted. Transient actor loss preserves
    its existing same-work retry semantics.

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

    oom_budget_tracker = OOMRecoveryBudgetTracker.from_config()
    init_oom_recovery_metrics(job_tracker)

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
        pending_tasks = tasks
        # ActorPool._map owns this deadline in the single-pool path. Recovery
        # rebuilds the pool between waves, so retain one deadline here as well:
        # repeated transient actor loss is not progress and must not reset it.
        stall_deadline = monotonic() + _MAP_STALL_TIMEOUT_S
        while pending_tasks:
            wave_tasks = pending_tasks
            completed_ranges: set[tuple[int, ...]] = set()
            next_tasks: list[SparseRangeTask] | None = None
            num_actors = max(1, min(concurrency, len(wave_tasks)))
            pool = ActorPool(
                actor_factory,
                num_actors,
                job_tracker=job_tracker,
                # ActorPool's same-size internal resubmit would hide the failed
                # SparseRangeTask from the driver. Surface actor loss so OOM can
                # shrink and transient loss can explicitly preserve same-work retry.
                resubmit_on_actor_failure=False,
            )
            try:
                for res in pool.map_unordered(
                    lambda actor, task: actor.run.remote(task), wave_tasks
                ):
                    if res.fatal_worker_oom:
                        result_range = tuple(res.source_frag_ids)
                        failed_task = next(
                            (
                                task
                                for task in wave_tasks
                                if tuple(task.frag_ids) == result_range
                            ),
                            None,
                        )
                        if failed_task is None:
                            raise RuntimeError(
                                "classified sparse OOM result did not match its "
                                f"driver range: {result_range!r}"
                            )
                        # Route the typed, task-attributed failure through the
                        # same driver recovery as actor loss. Raising here also
                        # closes this pool, so even a surviving actor is not reused.
                        raise ActorPoolTaskError(
                            task=failed_task,
                            cause=FatalWorkerOOMError(
                                res.error or "sparse worker reported OOM"
                            ),
                        )
                    stall_deadline = monotonic() + _MAP_STALL_TIMEOUT_S
                    # Results identify the exact disjoint fragment range in this
                    # wave. Once consumed, its metadata is retained in ``manager``
                    # (and may already be committed), so a later actor loss must
                    # never resubmit it.
                    completed_ranges.add(tuple(res.source_frag_ids))
                    if job_tracker is not None:
                        job_tracker.increment.remote(
                            "fragments", len(res.source_frag_ids)
                        )
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
            except ActorPoolTaskError as pool_exc:
                # Preserve every consumed success before this wave is retried or
                # aborted. Otherwise sub-granularity results are lost on a fatal
                # recovery decision and their replacement files become orphaned.
                manager.flush()
                unfinished = [
                    task
                    for task in wave_tasks
                    if tuple(task.frag_ids) not in completed_ranges
                ]
                failed_task = pool_exc.task
                if not isinstance(failed_task, SparseRangeTask):
                    raise
                # Prove that the pool's failed task still belongs to this exact
                # wave before making any recovery decision.
                if not any(
                    _sparse_task_identity(task) == _sparse_task_identity(failed_task)
                    for task in unfinished
                ):
                    raise RuntimeError(
                        "sparse actor failure did not match unfinished driver work: "
                        f"{_sparse_task_identity(failed_task)!r}"
                    ) from pool_exc

                fatal_exc = _normalize_sparse_actor_failure(pool_exc.cause)
                if isinstance(fatal_exc, FatalWorkerTransientError):
                    if monotonic() >= stall_deadline:
                        raise TimeoutError(
                            "Sparse ActorPool stalled: no result produced in "
                            f"{_MAP_STALL_TIMEOUT_S}s while retrying transient "
                            "actor loss"
                        ) from None
                    # This was ActorPool's previous behavior: retry the same
                    # unfinished work after node/preemption loss. The explicit
                    # new pool keeps actor-loss classification visible without
                    # changing the task footprint.
                    next_tasks = unfinished
                    _LOG.warning(
                        "transient sparse actor loss: retrying %d unfinished "
                        "range(s) unchanged on fresh actors",
                        len(next_tasks),
                    )
                elif isinstance(fatal_exc, FatalWorkerOOMError):
                    if not oom_budget_tracker.config.enabled:
                        raise fatal_exc from pool_exc.cause
                    replacements = _split_sparse_oom_task(failed_task)
                    shrunk = _strictly_partitions_sparse_task(
                        replacements,
                        failed_task,
                    )
                    reducible = (
                        len(failed_task.frag_ids) > 1 or failed_task.batch_rows > 1
                    )
                    if reducible and not shrunk:
                        raise FatalWorkerOOMError(
                            "sparse OOM recovery failed to strictly shrink "
                            "unfinished work "
                            f"(frag_ids={failed_task.frag_ids}; "
                            f"batch_rows={failed_task.batch_rows}; "
                            f"replacements="
                            f"{[(r.frag_ids, r.batch_rows) for r in replacements]})"
                        ) from fatal_exc
                    try:
                        attempt_info = record_oom_recovery_attempt(
                            oom_budget_tracker,
                            job_tracker=job_tracker,
                            job_id=job_id,
                            range_key=_sparse_task_oom_range_key(failed_task),
                            oom_exc=fatal_exc,
                            shrunk=shrunk,
                        )
                    except FatalWorkerOOMError as budget_exc:
                        raise budget_exc from fatal_exc
                    next_tasks = _replace_sparse_task(
                        unfinished,
                        failed_task,
                        replacements,
                    )
                    if shrunk:
                        # Strictly smaller work is structural progress even though
                        # this wave did not produce a completed range.
                        stall_deadline = monotonic() + _MAP_STALL_TIMEOUT_S
                    if attempt_info is not None:
                        _LOG.warning(
                            "fatal worker OOM on sparse range of %d fragment(s) "
                            "with batch_rows=%d: retrying as %s on fresh actors "
                            "(shrunk=%s; oom budget: total=%d/%d, "
                            "same_range=%d/%d)",
                            len(failed_task.frag_ids),
                            failed_task.batch_rows,
                            [
                                (len(task.frag_ids), task.batch_rows)
                                for task in replacements
                            ],
                            shrunk,
                            attempt_info.total_count,
                            attempt_info.total_limit,
                            attempt_info.same_range_count,
                            attempt_info.same_range_limit,
                        )
                else:
                    # Ordinary returned range errors still use RangeSparseResult;
                    # preserve the existing actor-level non-OOM exception here.
                    raise
            finally:
                # Every recovery wave gets newly constructed actors. This also
                # abandons in-flight, unconsumed results: because the driver never
                # ingested their metadata, they were never committed and are safe
                # to recompute from ``unfinished``.
                pool.shutdown()

            pending_tasks = next_tasks or []

        manager.flush()
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
