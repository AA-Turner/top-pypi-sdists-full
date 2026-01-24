#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import threading
from collections.abc import Callable
from typing import Dict, Tuple

import pandas

from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

# global cache mapping  (sessionID, planID) -> cached snowpark dataframe container.
df_cache_map: Dict[Tuple[str, any], DataFrameContainer] = {}

# reentrant lock for thread safety
_cache_map_lock = threading.RLock()


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
