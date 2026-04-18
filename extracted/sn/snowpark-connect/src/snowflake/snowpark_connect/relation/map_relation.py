#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy

import pandas
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.cache import (
    analyze_memo_get,
    analyze_memo_put,
    df_cache_map_get,
    df_cache_map_put_if_absent,
)
from snowflake.snowpark_connect.utils.context import (
    _STARTING_SQL_PLAN_ID,
    get_plan_id_map,
    get_spark_session_id,
    is_analyze_plan_request,
    not_resolving_fun_args,
    push_operation_scope,
    set_is_aggregate_function,
    set_plan_id_map,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)

# Spark doesn't have proto for NaturalJoin as Spark DF doesn't have API for it.
# BUT spark supports NATURAL JOIN via SQL
NATURAL_JOIN_TYPE_BASE = 22


def _is_server_generated_plan_id(plan_id: int) -> bool:
    """Server-generated plan IDs (from SQL parsing) start at _STARTING_SQL_PLAN_ID
    and are reset by clear_context_data() at the start of every RPC, so they
    collide across requests.  Client-generated plan IDs (from PySpark LogicalPlan)
    are monotonically increasing and never reset."""
    return plan_id >= _STARTING_SQL_PLAN_ID


def map_relation(
    rel: relation_proto.Relation, reuse_parsed_plan: bool = True
) -> DataFrameContainer | pandas.DataFrame:
    """Map a Spark Protobuf Relation message to a DataFrameContainer or pandas DataFrame.

    NOTE: We return a pandas DataFrame object when the return value of the operation is a
    scalar value. The client expects these as an Arrow buffer with this return value packed
    into a single cell. Rather than do what Spark does (which is put the data back into
    Spark and then convert it to an Arrow buffer), we leave the value we have already extracted
    from Snowflake here in the TCM as a pandas DataFrame and convert it to an Arrow Buffer.

    Args:
        rel (relation_proto.Relation): The Spark Protobuf Relation message to map.
        reuse_parsed_plan (bool, optional): If True, reuses previously parsed container from cache
            to avoid redundant operations.

    Returns:
        DataFrameContainer | pandas.DataFrame: The DataFrameContainer or pandas DataFrame
        that corresponds to the input Spark Protobuf Relation message.
    """
    # TODO: from snowflake_connect_server.relation import map_extension
    from snowflake.snowpark_connect.relation import (
        map_aggregate,
        map_catalog,
        map_cogroup_map,
        map_column_ops,
        map_crosstab,
        map_extension,
        map_join,
        map_local_relation,
        map_map_partitions,
        map_row_ops,
        map_sample_by,
        map_show_string,
        map_sql,
        map_stats,
        map_subquery_alias,
        map_udtf,
        read,
    )

    if reuse_parsed_plan and rel.HasField("common") and rel.common.HasField("plan_id"):
        # TODO: remove get_session_id() when we host SAS in Snowflake server
        # Check for cached relation
        cache_entry = df_cache_map_get((get_spark_session_id(), rel.common.plan_id))
        if cache_entry is not None:
            if isinstance(cache_entry, DataFrameContainer):
                set_plan_id_map(rel.common.plan_id, cache_entry)
            return cache_entry

        if is_analyze_plan_request() and not _is_server_generated_plan_id(
            rel.common.plan_id
        ):
            memo_hit = analyze_memo_get((get_spark_session_id(), rel.common.plan_id))
            if memo_hit is not None:
                set_plan_id_map(rel.common.plan_id, memo_hit)
                return memo_hit

        # If df is not cached, check if we have parsed the plan
        cached_container = get_plan_id_map(rel.common.plan_id)
        if cached_container is not None:
            cached_df = cached_container.dataframe
            result = copy.copy(cached_df)
            # Create new container without triggering schema access
            result_container = DataFrameContainer(
                result,
                column_map=copy.deepcopy(cached_container.column_map),
                table_name=copy.deepcopy(cached_container.table_name),
                alias=cached_container.alias,
                cached_schema_getter=lambda: cached_df.schema,
                partition_hint=cached_container.partition_hint,
            )
            # If we don't make a copy of the df._output, the expression IDs for attributes in Snowpark DataFrames will differ from those stored in the cache,
            # leading to errors during query execution.
            result._output = cached_df._output
            return result_container

    if rel.WhichOneof("rel_type") is not None:
        logger.debug(rel.WhichOneof("rel_type").upper())
    else:
        # This happens when the relation is empty, usually because the incoming message
        # type was incorrectly routed here.
        exception = SnowparkConnectNotImplementedError("No Relation Type")
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    result: DataFrameContainer | pandas.DataFrame
    operation = rel.WhichOneof("rel_type")
    with push_operation_scope(operation):
        match operation:
            case "aggregate":
                set_is_aggregate_function(("default", True))
                match rel.aggregate.group_type:
                    case relation_proto.Aggregate.GroupType.GROUP_TYPE_GROUPBY:
                        result = map_aggregate.map_group_by_aggregate(rel)
                    case relation_proto.Aggregate.GroupType.GROUP_TYPE_ROLLUP:
                        result = map_aggregate.map_rollup_aggregate(rel)
                    case relation_proto.Aggregate.GroupType.GROUP_TYPE_CUBE:
                        result = map_aggregate.map_cube_aggregate(rel)
                    case relation_proto.Aggregate.GroupType.GROUP_TYPE_PIVOT:
                        result = map_aggregate.map_pivot_aggregate(rel)
                    case other:
                        exception = SnowparkConnectNotImplementedError(
                            f"AGGREGATE {other}"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.UNSUPPORTED_OPERATION
                        )
                        raise exception
            case "approx_quantile":
                result = map_stats.map_approx_quantile(rel)
            case "as_of_join":
                exception = SnowparkConnectNotImplementedError("AS_OF_JOIN")
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            case "catalog":  # TODO: order these alphabetically
                result = map_catalog.map_catalog(rel.catalog)
            case "collect_metrics":
                # no-op, Snowflake doesn't support metrics
                result = map_relation(rel.collect_metrics.input)
            case "common_inline_user_defined_table_function":
                result = map_udtf.map_common_inline_user_defined_table_function(
                    rel.common_inline_user_defined_table_function
                )
            case "corr":
                result = map_stats.map_corr(rel)
            case "cov":
                result = map_stats.map_cov(rel)
            case "crosstab":
                result = map_crosstab.map_crosstab(rel)
            case "deduplicate":
                result = map_row_ops.map_deduplicate(rel)
            case "describe":
                result = map_stats.map_describe(rel)
            case "drop":
                result = map_column_ops.map_drop(rel)
            case "drop_na":
                result = map_row_ops.map_dropna(rel)
            case "extension":
                # Extensions can be passed as function args, and we need to reset the context here.
                # Matters only for resolving alias expressions in the extensions rel.
                with not_resolving_fun_args():
                    result = map_extension.map_extension(rel)
            case "fill_na":
                result = map_row_ops.map_fillna(rel)
            case "filter":
                result = map_row_ops.map_filter(rel)
            case "freq_items":
                result = map_stats.map_freq_items(rel)
            case "hint":
                result = map_relation(rel.hint.input)
                if rel.hint.name:
                    result.dataframe_hint = rel.hint.name
            case "html_string":
                result = map_show_string.map_repr_html(rel)
            case "join":
                result = map_join.map_join(rel)
            case "limit":
                result = map_row_ops.map_limit(rel)
            case "local_relation":
                result = map_local_relation.map_local_relation(
                    rel
                ).without_materialization()
                df_cache_map_put_if_absent(
                    (get_spark_session_id(), rel.common.plan_id), lambda: result
                )
            case "cached_local_relation":
                cached_df = df_cache_map_get(
                    (get_spark_session_id(), rel.cached_local_relation.hash)
                )
                if cached_df is None:
                    exception = ValueError(
                        f"Local relation with hash {rel.cached_local_relation.hash} not found in cache."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
                    raise exception
                result = cached_df
            case "map_partitions":
                result = map_map_partitions.map_map_partitions(rel)
            case "offset":
                result = map_row_ops.map_offset(rel)
            case "project":
                result = map_column_ops.map_project(rel)
            case "range":
                result = map_local_relation.map_range(rel)
            case "read":
                result = read.map_read(rel)
            case "repartition":
                # Preserve partition hint for file output control
                # This handles both repartition(n) with shuffle=True and coalesce(n) with shuffle=False
                result = map_relation(rel.repartition.input)
                if rel.repartition.num_partitions > 0:
                    result.partition_hint = rel.repartition.num_partitions
            case "repartition_by_expression":
                # This is a no-op operation in SAS as Snowpark doesn't have the concept of partitions.
                # All the data in the dataframe will be treated as a single partition, and this will not
                # have any side effects.
                result = map_relation(rel.repartition_by_expression.input)
                # Only preserve partition hint if num_partitions is explicitly specified and > 0
                # Column-based repartitioning without count should clear any existing partition hints
                if rel.repartition_by_expression.num_partitions > 0:
                    result.partition_hint = rel.repartition_by_expression.num_partitions
                else:
                    # Column-based repartitioning clears partition hint (resets to default behavior)
                    result.partition_hint = None
            case "replace":
                result = map_row_ops.map_replace(rel)
            case "sample":
                sampled_df_not_evaluated = map_row_ops.map_sample(rel)
                df_cache_map_put_if_absent(
                    (get_spark_session_id(), rel.common.plan_id),
                    lambda: sampled_df_not_evaluated,
                )

                # We will retrieve from cache and return that, because insertion to cache
                # triggers evaluation.
                result = df_cache_map_get((get_spark_session_id(), rel.common.plan_id))
            case "sample_by":
                result = map_sample_by.map_sample_by(rel)
            case "set_op":
                match rel.set_op.set_op_type:
                    case relation_proto.SetOperation.SetOpType.SET_OP_TYPE_INTERSECT:
                        result = map_row_ops.map_intersect(rel)
                    case relation_proto.SetOperation.SetOpType.SET_OP_TYPE_UNION:
                        result = map_row_ops.map_union(rel)
                    case relation_proto.SetOperation.SetOpType.SET_OP_TYPE_EXCEPT:
                        result = map_row_ops.map_except(rel)
                    case other:
                        exception = SnowparkConnectNotImplementedError(
                            f"SET_OP {other}"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.UNSUPPORTED_OPERATION
                        )
                        raise exception
            case "show_string":
                result = map_show_string.map_show_string(rel)
            case "sort":
                result = map_column_ops.map_sort(
                    rel.sort
                )  # TODO: follow this pattern elsewhere.
            case "sql":
                result = map_sql.map_sql(rel)
            case "subquery_alias":
                result = map_subquery_alias.map_alias(rel)
            case "summary":
                result = map_stats.map_summary(rel)
            case "tail":
                result = map_row_ops.map_tail(rel)
            case "to_df":
                result = map_column_ops.map_to_df(rel)
            case "to_schema":
                result = map_column_ops.map_to_schema(rel)
            case "unpivot":
                result = map_column_ops.map_unpivot(rel)
            case "with_columns":
                result = map_column_ops.map_with_columns(rel)
            case "with_columns_renamed":
                result = map_column_ops.map_with_columns_renamed(rel)
            case "with_relations":
                exception = SnowparkConnectNotImplementedError("WITH_RELATIONS")
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            case "group_map":
                result = map_column_ops.map_group_map(rel)
            case "co_group_map":
                result = map_cogroup_map.map_co_group_map(rel)
            case other:
                exception = SnowparkConnectNotImplementedError(
                    f"Other Relation {other}"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception

        # Store container in plan cache
        if isinstance(result, DataFrameContainer):
            set_plan_id_map(rel.common.plan_id, result)
            if is_analyze_plan_request() and not _is_server_generated_plan_id(
                rel.common.plan_id
            ):
                analyze_memo_put((get_spark_session_id(), rel.common.plan_id), result)

        return result
