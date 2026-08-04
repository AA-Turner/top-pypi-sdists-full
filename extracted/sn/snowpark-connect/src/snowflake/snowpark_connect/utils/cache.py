#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import os
import threading
from collections import defaultdict
from collections.abc import Callable
from typing import Dict, Tuple

import pandas

from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

# global cache mapping  (sessionID, planID) -> cached snowpark dataframe container.
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
# Spark Connect's persist() is lazy: it marks the plan for caching but does no work
# until the first action. We mirror that by recording (session_id, plan_id) on
# persist() and resolving + materializing (cache_result) on the first ExecutePlan
# resolution (see map_relation). Entries are removed when materialized or on unpersist.
_pending_persist_lock = threading.RLock()
_pending_persist: set[Tuple[str, any]] = set()


def pending_persist_add(key: Tuple[str, any]) -> None:
    with _pending_persist_lock:
        _pending_persist.add(key)


def pending_persist_discard(key: Tuple[str, any]) -> bool:
    """Remove the key from the pending set, returning True if it was present."""
    with _pending_persist_lock:
        if key in _pending_persist:
            _pending_persist.discard(key)
            return True
        return False


def df_cache_map_get(key: Tuple[str, any]) -> DataFrameContainer | None:
    with _cache_map_lock:
        return df_cache_map.get(key)


def df_cache_map_put_if_absent(
    key: Tuple[str, any],
    compute_fn: Callable[[], DataFrameContainer | pandas.DataFrame],
) -> DataFrameContainer | pandas.DataFrame:
    """
    Put a DataFrame container into the cache map if the key is absent. Optionally, as side effect, materialize
    the DataFrame content in a temporary table.

    Args:
        key (Tuple[str, int]): The key to insert into the cache map (session_id, plan_id).
        compute_fn (Callable[[], DataFrameContainer | pandas.DataFrame]): A function to compute the DataFrame container if the key is absent.

    Returns:
        DataFrameContainer | pandas.DataFrame: The cached or newly computed DataFrame container.
    """

    def _object_to_cache(
        container: DataFrameContainer,
    ) -> DataFrameContainer:

        if container.can_be_materialized:
            df = container.dataframe
            cached_result = df.cache_result()
            return DataFrameContainer(
                dataframe=cached_result,
                column_map=container.column_map,
                table_name=container.table_name,
                alias=container.alias,
                cached_schema_getter=lambda: df.schema,
            )
        return container

    with _cache_map_lock:
        if key in df_cache_map:
            return df_cache_map[key]

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
    with _cache_map_lock:
        if key in df_cache_map:
            return df_cache_map[key]

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
            df_cache_map[key] = cached_result
            return df_cache_map[key]
    else:
        # This is not expected, but we will just log a warning
        logger.warning(
            "Unexpected pandas dataframe returned for caching. Ignoring the cache call."
        )
        return result


def df_cache_map_pop(key: Tuple[str, any]) -> None:
    with _cache_map_lock:
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
