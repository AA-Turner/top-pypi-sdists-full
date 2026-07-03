#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from collections import namedtuple
from typing import Iterator

import pandas
import pyarrow as pa
import pyspark.sql.connect.proto.base_pb2 as proto_base
import pyspark.sql.connect.proto.types_pb2 as proto_types
from pyarrow import Table

import snowflake.snowpark_connect.tcm as tcm
from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.snowflake_plan import PlanQueryType
from snowflake.snowpark._internal.utils import (
    create_or_update_statement_params_with_query_tag,
)
from snowflake.snowpark.types import DayTimeIntervalType
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.execute_plan.utils import (
    _is_agg_function_with_single_row_result,
    arrow_table_to_arrow_bytes,
    pandas_empty_table_to_arrow_bytes,
    pandas_to_arrow_batches_bytes,
)
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_hidden_columns,
)
from snowflake.snowpark_connect.type_mapping import (
    SnowparkToArrowMapper,
    snowpark_to_proto_type,
)
from snowflake.snowpark_connect.utils.context import set_execute_root_plan_id
from snowflake.snowpark_connect.utils.request_utils import get_or_generate_operation_id

QueryResult = namedtuple("QueryResult", ["query_id", "arrow_schema", "spark_schema"])


def _build_execute_plan_response(
    row_count: int, data_bytes: bytes, schema, request: proto_base.ExecutePlanRequest
):
    return proto_base.ExecutePlanResponse(
        session_id=request.session_id,
        operation_id=get_or_generate_operation_id(request),
        arrow_batch=proto_base.ExecutePlanResponse.ArrowBatch(
            row_count=row_count,
            data=data_bytes,
        ),
        schema=schema,
    )


SKIP_LEVELS_TWO = (
    2  # limit traceback to return up to 2 stack trace entries from traceback object tb
)


def _widen_second_only_interval_columns(
    result_df: snowpark.DataFrame,
    snowpark_schema: snowpark.types.StructType,
) -> snowpark.DataFrame:
    """Work around a Snowflake/snowpark arrow-fetch limitation for SECOND-only
    day-time intervals.

    Fetching a top-level ``INTERVAL SECOND`` column (``DayTimeIntervalType(SECOND,
    SECOND)``, Snowflake scale 12) via ``to_arrow`` collapses the value to 0 — it
    affects interval literals, string casts, and numeric casts alike. Casting the
    column to ``DAY TO SECOND`` preserves the exact value (a day-time interval's
    value is independent of its field range; the range only governs display, which
    the client renders from the proto schema). The caller keeps the reported
    schema from the original DataFrame, so widening only affects the fetched Arrow
    data and is invisible to the client.

    The already-resolved ``snowpark_schema`` is passed in so this adds no extra
    ``DESCRIBE`` round-trip, and ``result_df`` is returned unchanged (no extra
    projection) when no SECOND-only interval column is present.
    """
    needs_widening = [
        isinstance(f.datatype, DayTimeIntervalType)
        and f.datatype.start_field == DayTimeIntervalType.SECOND
        for f in snowpark_schema.fields
    ]
    if not any(needs_widening):
        return result_df

    day_to_second = DayTimeIntervalType(
        DayTimeIntervalType.DAY, DayTimeIntervalType.SECOND
    )
    projection = []
    for name, widen in zip(snowpark_schema.names, needs_widening):
        col = result_df.col(name)
        projection.append(col.cast(day_to_second).alias(name) if widen else col)
    return result_df.select(projection)


# TODO: SNOW-2039432 use to_arrow_batches once it is fixed in sproc-python-connector
# TODO: SNOW-2057291 remove once df.to_arrow() starts accepting to_iter parameter
def to_arrow_batch_iter(
    result_df: snowpark.DataFrame, *, to_iter: bool = True
) -> Iterator[Table]:
    result = result_df.session._conn.execute(
        result_df._plan,
        to_pandas=False,
        to_iter=to_iter,
        to_arrow=True,
        block=True,
        _statement_params=create_or_update_statement_params_with_query_tag(
            result_df._statement_params,
            result_df.session.query_tag,
            SKIP_LEVELS_TWO,
            collect_stacktrace=result_df.session.conf.get(
                "collect_stacktrace_in_query_tag"
            ),
        ),
    )
    if to_iter:
        return result
    else:
        # when to_iter is false, a single pyarrow table is returned, to not break downstream logic
        # an iterator of list of result is returned
        return iter([result])


def map_execution_root(
    request: proto_base.ExecutePlanRequest,
) -> Iterator[proto_base.ExecutePlanResponse | QueryResult]:
    to_iter = not _is_agg_function_with_single_row_result(request.plan.root)
    if request.plan.root.HasField("common") and request.plan.root.common.HasField(
        "plan_id"
    ):
        set_execute_root_plan_id(request.plan.root.common.plan_id)
    result: DataFrameContainer | pandas.DataFrame = map_relation(request.plan.root)
    if isinstance(result, pandas.DataFrame):
        pandas_df = result
        data_bytes = pandas_to_arrow_batches_bytes(pandas_df)
        row_count = len(pandas_df)
        schema = None
        yield _build_execute_plan_response(row_count, data_bytes, schema, request)
    elif result.has_zero_columns():
        # 0-column dataframes can still have rows.
        # SNOW-3242008: Use known_row_count when available to avoid a Snowflake query.
        row_count = (
            result.known_row_count
            if result.known_row_count is not None
            else result.dataframe.count()
        )
        data_bytes = pandas_to_arrow_batches_bytes(
            pandas.DataFrame(index=range(row_count))
        )
        schema = None
        yield _build_execute_plan_response(row_count, data_bytes, schema, request)
    else:
        # SNOW-2443454: strip both internal scaffolding (__DUMMY) and
        # qualified-access-only columns (USING-join source columns) at the
        # execute boundary — neither is part of the user-visible schema.
        filtered_result = without_hidden_columns(result)
        filtered_result_df = filtered_result.dataframe
        snowpark_schema = filtered_result_df.schema
        schema = snowpark_to_proto_type(
            snowpark_schema, filtered_result.column_map, filtered_result_df
        )
        spark_columns = filtered_result.column_map.get_spark_columns()

        # SNOW-3595418: SECOND-only day-time interval columns fetch as 0 via
        # to_arrow. Widen them for the fetch only; the reported schema above is
        # kept from the original (3,3) type, so this is invisible to the client.
        # No-op (returns the same DataFrame) when no such column is present.
        fetch_df = _widen_second_only_interval_columns(
            filtered_result_df, snowpark_schema
        )

        # SNOW-3242008: Performance optimization for DDL sql_command results.
        # When a DDL statement (USE DATABASE, ALTER SESSION SET, etc.) is executed,
        # the result ("Statement executed successfully.") round-trips through the
        # client as a LocalRelation. Without this short-circuit, we'd create a
        # Snowpark DataFrame and execute a VALUES query against Snowflake just to
        # return this static data. Instead, we return the already-deserialized Arrow
        # table directly from memory, saving a Snowflake warehouse round trip.
        cached_local_table = filtered_result.cached_local_relation_arrow_table
        if cached_local_table is not None:
            if cached_local_table.num_rows > 0:
                data_bytes = arrow_table_to_arrow_bytes(
                    cached_local_table, snowpark_schema, spark_columns
                )
                yield _build_execute_plan_response(
                    cached_local_table.num_rows, data_bytes, schema, request
                )
            else:
                pandas_df = cached_local_table.to_pandas()
                data_bytes = pandas_empty_table_to_arrow_bytes(
                    pandas_df, snowpark_schema, spark_columns
                )
                yield _build_execute_plan_response(0, data_bytes, schema, request)
            return

        if tcm.TCM_MODE:
            # TCM result handling:
            # - small result (only one batch): just return the executePlanResponse
            # - large result (more than one batch): return a tuple with query UUID, arrow schema, and spark schema.
            # If TCM_RETURN_QUERY_ID_FOR_SMALL_RESULT is true, all results will be treated as large result.
            is_large_result = False
            second_batch = False
            first_arrow_table = None
            with fetch_df.session.query_history() as qh:
                for arrow_table in to_arrow_batch_iter(fetch_df, to_iter=to_iter):
                    if second_batch:
                        is_large_result = True
                        break
                    first_arrow_table = arrow_table
                    second_batch = True
                queries_cnt = len(
                    fetch_df._plan.execution_queries[PlanQueryType.QUERIES]
                )
                # get query uuid from the last query; this may not be the last queries in query history because snowpark
                # may run some post action queries, e.g., drop temp table.
                query_id = qh.queries[queries_cnt - 1].query_id
            if first_arrow_table is None:
                # empty arrow batch iterator
                pandas_df = fetch_df.to_pandas()
                data_bytes = pandas_empty_table_to_arrow_bytes(
                    pandas_df, snowpark_schema, spark_columns
                )
                yield _build_execute_plan_response(0, data_bytes, schema, request)
            elif not tcm.TCM_RETURN_QUERY_ID_FOR_SMALL_RESULT and not is_large_result:
                data_bytes = arrow_table_to_arrow_bytes(
                    first_arrow_table, snowpark_schema, spark_columns
                )
                yield _build_execute_plan_response(
                    first_arrow_table.num_rows, data_bytes, schema, request
                )
            else:
                # return query id and serialized schemas
                arrow_schema = pa.schema(
                    SnowparkToArrowMapper().map_schema(
                        snowpark_schema, pa.struct(first_arrow_table.schema)
                    )
                )
                serialized_arrow_schema = arrow_schema.serialize().to_pybytes()
                spark_schema = proto_types.DataType(**schema)
                yield QueryResult(
                    query_id,
                    serialized_arrow_schema,
                    spark_schema.SerializeToString(),
                )
        else:
            # SNOW-3453333: to_iter must be propagated to ensure correctness
            # In some cases, setting to_iter=False may improve performance by removing
            # streaming overhead, but doing so can cause errors when the size of the
            # data being retrieved exceeds SNOWFLAKE_GRPC_MAX_MESSAGE_SIZE, which
            # we configure to be 128MB by default. This is not checked in CI due to
            # the potential for slowdowns and flakiness.
            arrow_table_iter = to_arrow_batch_iter(fetch_df, to_iter=to_iter)
            batch_count = 0
            for arrow_table in arrow_table_iter:
                if arrow_table.num_rows > 0:
                    batch_count += 1
                    data_bytes = arrow_table_to_arrow_bytes(
                        arrow_table, snowpark_schema, spark_columns
                    )
                    yield _build_execute_plan_response(
                        arrow_table.num_rows, data_bytes, schema, request
                    )
                else:
                    break

            # Empty result needs special processing
            if batch_count == 0:
                pandas_df = fetch_df.to_pandas()
                data_bytes = pandas_empty_table_to_arrow_bytes(
                    pandas_df, snowpark_schema, spark_columns
                )
                yield _build_execute_plan_response(0, data_bytes, schema, request)
