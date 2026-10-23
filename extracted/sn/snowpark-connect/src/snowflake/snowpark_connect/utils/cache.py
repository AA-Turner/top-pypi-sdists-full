#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import os
import threading
from collections import defaultdict
from collections.abc import Callable
from contextlib import contextmanager
from typing import Dict, Tuple

import pandas

from snowflake.snowpark_connect.dataframe_container import (
    DataFrameContainer,
    MaterializationPolicy,
)
from snowflake.snowpark_connect.utils.context import get_request_window_chain_tables
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

# global cache mapping (sessionID, planID) -> cached snowpark dataframe container.
# Uploaded local relations (artifact cache/<hash>) use (sessionID, "<hash>").
# Every other key uses the int plan id: df_cache_map_clear_session_plans keeps str keys.
df_cache_map: Dict[Tuple[str, any], DataFrameContainer] = {}

# reentrant lock for thread safety
_cache_map_lock = threading.RLock()

# Cross-request memo for map_relation results (lazy DataFrameContainer).
# Per-session dict; accumulates during AnalyzePlan calls, cleared at the end
# of each ExecutePlan RPC in server.py's finally block.
_analyze_memo_lock = threading.RLock()
_analyze_memo: Dict[str, Dict[int, DataFrameContainer]] = defaultdict(dict)
_ANALYZE_MEMO_DISABLED = os.environ.get(
    "SNOWPARK_CONNECT_ANALYZE_MEMO_DISABLED", ""
).lower() in ("1", "true", "yes")


def analyze_memo_get(key: Tuple[str, int]) -> DataFrameContainer | None:
    if _ANALYZE_MEMO_DISABLED:
        return None
    session_id, plan_id = key
    with _analyze_memo_lock:
        session_map = _analyze_memo.get(session_id)
        if session_map is None or plan_id not in session_map:
            return None
        return session_map[plan_id]


def analyze_memo_put(key: Tuple[str, int], value: DataFrameContainer) -> None:
    if _ANALYZE_MEMO_DISABLED:
        return
    session_id, plan_id = key
    with _analyze_memo_lock:
        _analyze_memo[session_id][plan_id] = value


def analyze_memo_pop(key: Tuple[str, int]) -> None:
    session_id, plan_id = key
    with _analyze_memo_lock:
        session_map = _analyze_memo.get(session_id)
        if session_map is None:
            return
        session_map.pop(plan_id, None)
        if len(session_map) == 0:
            del _analyze_memo[session_id]


def analyze_memo_clear_session(session_id: str) -> None:
    with _analyze_memo_lock:
        _analyze_memo.pop(session_id, None)


# Plans the client asked to persist/cache but which have not been materialized yet.
# Spark Connect's persist() is lazy: it marks the plan for caching but does no work until
# the first action. We mirror that by recording (session_id, plan_id) on persist() and
# resolving + materializing (cache_result) on the first ExecutePlan resolution.
_pending_persist_lock = threading.RLock()
_pending_persist: set[Tuple[str, any]] = set()

# Keys this thread is currently resolving on behalf of a persist request.
#
# This is a re-entrancy guard, and it is load-bearing rather than bookkeeping. The
# lazy-persist branch resolves the underlying relation by recursing into ``map_relation``
# with the same ``rel``; while that recursion is in flight the request must not be taken
# again, or the nested call enters the same branch and recurses until RecursionError --
# which breaks any fresh ``.cache()`` + action on every engine, not just NSS. Consuming the
# key up front used to provide this incidentally; claiming it provides it deliberately, and
# keeps the request recoverable when the write fails.
#
# **Thread-local on purpose.** A process-global set would also hide the request from an
# independent request resolving the same plan on another thread, and that request would
# then return the lazy container -- no cache at all, which is worse than duplicate work.
# Scoping the guard to the resolving thread means a concurrent request still claims and
# materializes; the loser's publish is dropped by the ``is_materialized`` re-check below.
_resolving = threading.local()


def _resolving_keys() -> set:
    keys = getattr(_resolving, "keys", None)
    if keys is None:
        keys = set()
        _resolving.keys = keys
    return keys


def pending_persist_add(key: Tuple[str, any]) -> None:
    with _pending_persist_lock:
        _pending_persist.add(key)


def pending_persist_peek(key: Tuple[str, any]) -> bool:
    """Is there a persist request for this key that this thread could act on?"""
    if key in _resolving_keys():
        return False
    with _pending_persist_lock:
        return key in _pending_persist


def pending_persist_claim(key: Tuple[str, any]) -> bool:
    """Take the request for the duration of one resolution on this thread.

    The claim is not a consumption: a failed materialization releases it without
    discarding, so a retried action can still honour the persist.
    """
    if key in _resolving_keys():
        return False
    with _pending_persist_lock:
        if key not in _pending_persist:
            return False
    _resolving_keys().add(key)
    return True


def pending_persist_release(key: Tuple[str, any], *, completed: bool) -> None:
    """Release this thread's claim, consuming the request only on success."""
    _resolving_keys().discard(key)
    if completed:
        with _pending_persist_lock:
            _pending_persist.discard(key)


@contextmanager
def claimed_persist(key: Tuple[str, any]):
    """Hold a persist claim for one resolution, consuming it only on clean exit.

    Yields True when this thread took the request, False when there was nothing to take
    (no request, or this thread is already resolving the same key). Both ``map_relation``
    call sites go through here so the claim/release lifetime is written once -- the
    try/finally is the part that must not drift, since releasing without ``completed`` is
    what keeps a failed write recoverable, and failing to release at all would wedge the
    key as permanently unclaimable.
    """
    claimed = pending_persist_claim(key)
    if not claimed:
        yield False
        return
    completed = False
    try:
        yield True
        completed = True
    finally:
        pending_persist_release(key, completed=completed)


def pending_persist_discard(key: Tuple[str, any]) -> bool:
    """Drop any request for this key outright -- unpersist, not completion."""
    with _pending_persist_lock:
        if key in _pending_persist:
            _pending_persist.discard(key)
            return True
        return False


# ── Not handled here, deliberately: concurrent persist of the SAME plan ──────────────
#
# Two requests resolving one plan_id at the same time can still interleave badly:
#
#   * an action that finishes late consumes a persist request recorded by a newer
#     ``.cache()`` after an unpersist/re-persist, because requests are not individually
#     identified;
#   * a ``cache_result()`` that began before an unpersist, or before a session-cache clear
#     (``config.py``, e.g. on a ``spark.sql.caseSensitive`` change), still publishes its
#     table afterwards, so a cancelled or stale-configuration snapshot can be reinstalled.
#
# An earlier revision of this change carried per-request tokens and per-key invalidation
# generations to close these. That machinery was removed: it was larger than the defect it
# addressed, it lives on a path every read takes, and review found fresh correctness bugs
# inside it faster than it closed the originals. The deterministic single-threaded holes --
# which are the ones with user impact and the ones ``df.cache()`` actually hits -- are fixed
# above and tested. These two races are tracked separately (SNOW-4231637 follow-up) rather
# than half-solved here. Note this path already documents an accepted duplicate-write race
# below, so tolerating a narrow concurrent-persist gap is consistent with what is here, not
# a new kind of compromise.


def _entry_is_materialized(entry) -> bool:
    """True only for a map entry already backed by a temp table."""
    return isinstance(entry, DataFrameContainer) and entry.is_materialized


def df_cache_map_is_materialized(key: Tuple[str, any]) -> bool:
    """Is this key's entry backed by a temp table?

    The persist handler needs this rather than "is the key present": an NSS read is
    inserted by ``map_read`` with ``without_materialization()``, so a present entry is
    often a lazy ``STAGE_FILE_READER`` query. Treating presence as materialization made
    ``df.cache()`` a silent no-op whenever anything resolved the plan first -- a schema
    inspection, ``df.columns``, or an earlier action (SNOW-4231637).
    """
    with _cache_map_lock:
        return _entry_is_materialized(df_cache_map.get(key))


def df_cache_map_force_materialize(
    key: Tuple[str, any],
) -> DataFrameContainer | pandas.DataFrame | None:
    """Materialize the key's existing entry in place, for an ExecutePlan cache hit.

    ``map_relation`` returns a cache hit before it reaches the lazy-persist branch, so a
    pending persist against an already-memoized plan would otherwise never be honoured.
    """
    entry = df_cache_map_get(key)
    if entry is None:
        return None
    return df_cache_map_put_if_absent(key, lambda: entry, force_materialize=True)


def df_cache_map_get(key: Tuple[str, any]) -> DataFrameContainer | None:
    with _cache_map_lock:
        return df_cache_map.get(key)


def df_cache_map_put_if_absent(
    key: Tuple[str, any],
    compute_fn: Callable[[], DataFrameContainer | pandas.DataFrame],
    force_materialize: bool = False,
) -> DataFrameContainer | pandas.DataFrame:
    """
    Put a DataFrame container into the cache map if the key is absent. Optionally, as side effect, materialize
    the DataFrame content in a temporary table.

    Args:
        key (Tuple[str, int]): The key to insert into the cache map (session_id, plan_id).
        compute_fn (Callable[[], DataFrameContainer | pandas.DataFrame]): A function to compute the DataFrame container if the key is absent.
        force_materialize (bool): The caller explicitly asked for a cache (``df.cache()`` /
            ``persist()``), so materialize even a container that opts out of *incidental*
            materialization. Only ``map_relation``'s lazy-persist branch passes this.

    Returns:
        DataFrameContainer | pandas.DataFrame: The cached or newly computed DataFrame container.
    """

    def _object_to_cache(container: DataFrameContainer) -> DataFrameContainer:
        # ``can_be_materialized`` answers "may this be materialized *incidentally*, when
        # df_cache_map happens to memoize it?", which is a different question from "did the
        # caller explicitly ask for a cache?". NSS reads answer the first False on purpose
        # (SNOW-3717231), and that silently swallowed the second until force_materialize
        # separated them (SNOW-4231637).
        if container.is_materialized:
            # Already table-backed -- a COPY INTO read, or a container this function
            # produced earlier. ``force_materialize`` may override "do not materialize me
            # incidentally", but it must not override "there is nothing left to do": the
            # COPY branches suppress a *redundant second* temp table, and writing one is a
            # full result copy on the default non-NSS path (SNOW-4231637).
            return container
        if container.must_not_materialize:
            # The container says a temp table is not worth writing at all -- a
            # ``local_relation`` literal, or a read whose result ``saveAsTable`` is about
            # to persist anyway (SNOW-3262791). ``force_materialize`` overrides "not
            # incidentally"; it does not override "not ever".
            #
            # This replaces a check on whether NSS was enabled. That check worked only
            # because the containers the override exists for happen to exist solely under
            # NSS, so it answered "is NSS on?" as a proxy for "is this a lazy read?" --
            # and left the real question to be rediscovered whenever the flag is
            # decommissioned. The container answers it directly instead.
            return container
        if not (container.can_be_materialized or force_materialize):
            return container
        df = container.dataframe
        # The plan may read window-chain tables that are dropped when this
        # request ends, so then resolve the schema now and keep it by value.
        schema = df.schema if get_request_window_chain_tables() else None
        cached_result = df.cache_result()
        # Imported here: column_name_handler -> config -> ... imports this module.
        from snowflake.snowpark_connect.column_name_handler import ColumnNameMap

        column_map = container.column_map
        if isinstance(column_map, ColumnNameMap):
            # Values now come from a temp table; don't rely on table storage
            # keeping the NSS null-element encoding that posexplode's
            # no-TRANSFORM path needs (SNOW-4261008).
            column_map = column_map.without_nss_data()
        materialized = DataFrameContainer(
            dataframe=cached_result,
            column_map=column_map,
            table_name=container.table_name,
            alias=container.alias,
            cached_schema_getter=(
                (lambda: schema) if schema is not None else (lambda: df.schema)
            ),
            # Carried deliberately, field by field. Materializing must not change what the
            # plan means, and this path now receives containers that previously passed
            # through untouched, so anything dropped here is a silent behaviour change:
            #   partition_hint   -- coalesce(1)/repartition(N); the single-file write rule
            #                       and mapPartitions' batch path both key off it
            #   dataframe_hint   -- hint("directed") must survive a cache
            #   aggregate_metadata / sort_exprs -- still describe the same rows
            #   can_be_cached    -- it was True to get here; keep it true of the result
            # Deliberately NOT carried:
            #   cached_local_relation_arrow_table -- a LocalRelation round-trip shortcut
            #       holding pre-deserialized Arrow. The cached frame reads a temp table
            #       instead, so carrying it would let a later read bypass that table.
            partition_hint=container.partition_hint,
            dataframe_hint=container.dataframe_hint,
            can_be_cached=container.can_be_cached,
            aggregate_metadata=container._aggregate_metadata,
            sort_exprs=container.sort_exprs,
            # The state travels ON the entry. A key-indexed marker could outlive, or be
            # overwritten independently of, the container it described -- which is exactly
            # how an explicit cache() got silently dropped (SNOW-4231637).
            # Successful materialization IS the ALREADY state -- the loop closes here
            # rather than setting a separate "done" bit that could drift from the entry.
            materialization_policy=MaterializationPolicy.ALREADY,
        )
        materialized._known_row_count = container.known_row_count
        return materialized

    def _materialize_existing(
        existing: DataFrameContainer,
    ) -> DataFrameContainer | pandas.DataFrame:
        """Ensure the key's CURRENT entry is materialized, and return that entry.

        Deliberately ignores ``existing`` beyond its arrival: the caller sampled it before
        taking the lock, so by now another thread may have published a materialized
        container under the same key. Returning the sampled argument would hand a caller
        that explicitly asked for a cache a lazy frame instead (SNOW-4231637), so every
        return here comes from ``df_cache_map``.
        """
        with _cache_map_lock:
            current = df_cache_map.get(key)
            if _entry_is_materialized(current):
                # Already backed by a temp table; a second cache_result() would write
                # another copy for no benefit.
                return current
            to_materialize = current if current is not None else existing
        if not isinstance(to_materialize, DataFrameContainer):
            return to_materialize
        # cache_result() deliberately runs outside ``_cache_map_lock``: it is a temp-table
        # write and that lock is shared by every session in the process.
        cached = _object_to_cache(to_materialize)
        with _cache_map_lock:
            # Re-check: a concurrent caller may have published a materialized entry while
            # the write above was in flight. Last-writer-wins would be fine between two
            # materialized entries, but never prefer ours if theirs is already good.
            current = df_cache_map.get(key)
            if _entry_is_materialized(current):
                return current
            df_cache_map[key] = cached
            return df_cache_map[key]

    def _resolve_existing(
        existing: DataFrameContainer | pandas.DataFrame,
    ) -> DataFrameContainer | pandas.DataFrame:
        """Honour ``force_materialize`` against an entry some other caller inserted.

        It means "ensure this key ends up materialized", not "materialize only if I am the
        inserter" -- and for the persist branch an existing unmaterialized entry is the
        normal case rather than a race: its compute_fn re-enters ``map_relation`` for the
        same plan_id and the read path caches the key itself with the default False.
        """
        if not force_materialize:
            return existing
        if not isinstance(existing, DataFrameContainer):
            logger.warning(
                "Explicit persist ignored for %s: cached value is not a DataFrameContainer.",
                key,
            )
            return existing
        return _materialize_existing(existing)

    with _cache_map_lock:
        existing = df_cache_map.get(key)
    if existing is not None:
        return _resolve_existing(existing)

    # the compute_fn is not guaranteed to be called only once, but it's acceptable based upon the following analysis:
    # there are in total 5 occurrences of passing compute_fn callback falling into two categories:
    # 2 occurrences as lambda that needs to be computed:
    #     1) server::AnalyzePlan case "persist"
    #     2) server::AddArtifacts case "read"
    # 3 occurrences as lambda that simply returns pre-computed dataframe without any computation:
    #     1) map_relation case "local_relation"
    #     2) map_relation case "sample"
    #     3) map_read case "data_source"
    # based upon the analysis of the code, the chance of concurrently calling compute_fn for the same key is very low and if it happens
    # repeating the computation will not affect the result.
    # This is a trade-off between implementation simplicity and fine-grained locking.
    result = compute_fn()

    if isinstance(result, DataFrameContainer) and not result.can_be_cached:
        return result

    # check cache again, since recursive call in compute_fn could've already cached the result.
    # we want return it, instead of saving it again. This is important if materialize = True
    # because materialization is expensive operation that we don't want to do twice.
    #
    # This is the re-check that fires for the persist branch, so it is also where
    # force_materialize has to be honoured or an explicit cache() is dropped;
    # The entry's own ``is_materialized`` keeps the "don't do it twice" property.
    with _cache_map_lock:
        existing = df_cache_map.get(key)
    if existing is not None:
        return _resolve_existing(existing)

    # only cache DataFrameContainer, but not pandas result.
    # Pandas result is only returned when df.show() is called, where we convert
    # a dataframe to a string representation.
    # We don't expect map_relation would return pandas df here because that would
    # be equivalent to calling df.show().cache(), which is not allowed.
    if isinstance(result, DataFrameContainer):
        # The _object_to_cache function is not guaranteed to be called only once.
        # In rare multithreading cases, this may result in duplicate temporary table
        # creation because df.cache_result() materializes the DataFrame into a temp table each time.
        # This is acceptable because correctness is not affected, the likelihood is very low, and
        # it simplifies the implementation by avoiding fine-grained locking.
        cached_result = _object_to_cache(result)
        with _cache_map_lock:
            # Re-check before publishing. An incidental writer that passed the absent-key
            # check above can finish *after* an explicit-persist caller has installed a
            # table-backed entry; an unconditional assignment then downgrades a completed
            # cache to a lazy frame, and every later action goes back to raw-file
            # execution. One explicit caller is enough to hit this (SNOW-4231637).
            current = df_cache_map.get(key)
            if _entry_is_materialized(current) and not _entry_is_materialized(
                cached_result
            ):
                return current
            df_cache_map[key] = cached_result
            return df_cache_map[key]
    else:
        # This is not expected, but we will just log a warning
        logger.warning(
            "Unexpected pandas dataframe returned for caching. Ignoring the cache call."
        )
        return result


def df_cache_map_pop(key: Tuple[str, any]) -> None:
    # No companion bookkeeping to keep in step: materialization state lives on the entry,
    # so dropping the entry drops the state with it.
    with _cache_map_lock:
        df_cache_map.pop(key, None)


def df_cache_map_clear_session(session_id: str) -> None:
    """Drop every ``df_cache_map`` entry for one Spark session, including
    uploaded local relations. For a config change use
    ``df_cache_map_clear_session_plans``."""
    with _cache_map_lock:
        for key in list(df_cache_map):
            if key[0] == session_id:
                df_cache_map.pop(key, None)


def df_cache_map_clear_session_plans(session_id: str) -> None:
    """Drop one Spark session's ``(session_id, plan_id)`` entries, keeping its
    uploaded local relations.

    Required when session-scoped runtime configs (e.g. ``spark.sql.caseSensitive``)
    change: ``df_cache_map`` keys only ``(session_id, plan_id)`` and NSS reads bake
    the effective SPARK_CONF into ``STAGE_FILE_READER`` at first resolution. A large
    ``createDataFrame`` is uploaded once as artifact ``cache/<hash>`` and kept under
    ``(session_id, "<hash>")``; the client never re-uploads it, so it cannot be
    rebuilt and must survive.
    """
    with _cache_map_lock:
        for key in list(df_cache_map):
            if key[0] == session_id and not isinstance(key[1], str):
                df_cache_map.pop(key, None)


# Per-session cache: (session_id, sql_proto_bytes) -> DataFrameContainer.
# Keyed on the serialized bytes of the SQL sub-message (query + args, no plan_id),
# so the same spark.sql(text) call reuses the plan across all 4 RPCs that follow it.
_sql_plan_cache_lock = threading.RLock()
_sql_plan_cache: Dict[Tuple[str, bytes], DataFrameContainer] = {}
_SQL_PLAN_CACHE_DISABLED = os.environ.get(
    "SNOWPARK_CONNECT_SQL_PLAN_CACHE_DISABLED", ""
).lower() in ("1", "true", "yes")


def sql_plan_cache_get(key: Tuple[str, bytes]) -> DataFrameContainer | None:
    if _SQL_PLAN_CACHE_DISABLED:
        return None
    with _sql_plan_cache_lock:
        return _sql_plan_cache.get(key)


def sql_plan_cache_put(key: Tuple[str, bytes], value: DataFrameContainer) -> None:
    if _SQL_PLAN_CACHE_DISABLED:
        return
    with _sql_plan_cache_lock:
        _sql_plan_cache[key] = value


def sql_plan_cache_clear_session(session_id: str) -> None:
    with _sql_plan_cache_lock:
        keys = [k for k in _sql_plan_cache if k[0] == session_id]
        for k in keys:
            del _sql_plan_cache[k]
