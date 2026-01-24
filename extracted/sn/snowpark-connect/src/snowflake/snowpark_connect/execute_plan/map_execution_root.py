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
from snowflake.connector.cursor import SnowflakeCursor
from snowflake.connector.errors import NotSupportedError
from snowflake.snowpark._internal.analyzer.snowflake_plan import PlanQueryType
from snowflake.snowpark._internal.utils import (
    create_or_update_statement_params_with_query_tag,
)
from snowflake.snowpark_connect.constants import SERVER_SIDE_SESSION_ID
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.execute_plan.utils import (
    arrow_table_to_arrow_bytes,
    pandas_empty_table_to_arrow_bytes,
    pandas_to_arrow_batches_bytes,
)
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_internal_columns,
)
from snowflake.snowpark_connect.type_mapping import (
    map_snowpark_types_to_pyarrow_types,
    snowpark_to_proto_type,
)

QueryResult = namedtuple("QueryResult", ["query_id", "arrow_schema", "spark_schema"])


def _build_execute_plan_response(
    row_count: int, data_bytes: bytes, schema, request: proto_base.ExecutePlanRequest
):
    return proto_base.ExecutePlanResponse(
        session_id=request.session_id,
        operation_id=SERVER_SIDE_SESSION_ID,
        arrow_batch=proto_base.ExecutePlanResponse.ArrowBatch(
            row_count=row_count,
            data=data_bytes,
        ),
        schema=schema,
    )


def sproc_connector_fetch_arrow_batches_fix(self) -> Iterator[Table]:
    self.check_can_use_arrow_resultset()
    if self._prefetch_hook is not None:
        self._prefetch_hook()
    if self._query_result_format != "arrow":
        exception = NotSupportedError()
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    return self._result_set._fetch_arrow_batches()


# TODO: SNOW-2039432 use to_arrow_batches once it is fixed in sproc-python-connector
# We need to do this monkey patching because sproc python connector has a bug where it does not call _prefetch_hook()
# inside fetch_arrow_batches() which causes TCM, notebook and stored procs to throw error on df.collect()
SnowflakeCursor.fetch_arrow_batches = sproc_connector_fetch_arrow_batches_fix

SKIP_LEVELS_TWO = (
    2  # limit traceback to return up to 2 stack trace entries from traceback object tb
)


# TODO: SNOW-2039432 use to_arrow_batches once it is fixed in sproc-python-connector
# TODO: SNOW-2057291 remove once df.to_arrow() starts accepting to_iter parameter
def to_arrow_batch_iter(result_df: snowpark.DataFrame) -> Iterator[Table]:
    return result_df.session._conn.execute(
        result_df._plan,
        to_pandas=False,
        to_iter=True,
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


def map_execution_root(
    request: proto_base.ExecutePlanRequest,
) -> Iterator[proto_base.ExecutePlanResponse | QueryResult]:
    result: DataFrameContainer | pandas.DataFrame = map_relation(request.plan.root)
    if isinstance(result, pandas.DataFrame):
        pandas_df = result
        data_bytes = pandas_to_arrow_batches_bytes(pandas_df)
        row_count = len(pandas_df)
        schema = None
        yield _build_execute_plan_response(row_count, data_bytes, schema, request)
    elif result.has_zero_columns():
        # 0-column dataframes can still have rows
        row_count = result.dataframe.count()
        data_bytes = pandas_to_arrow_batches_bytes(
            pandas.DataFrame(index=range(row_count))
        )
        schema = None
        yield _build_execute_plan_response(row_count, data_bytes, schema, request)
    else:
        filtered_result = without_internal_columns(result)
        filtered_result_df = filtered_result.dataframe
        snowpark_schema = filtered_result_df.schema
        schema = snowpark_to_proto_type(
            snowpark_schema, filtered_result.column_map, filtered_result_df
        )
        spark_columns = filtered_result.column_map.get_spark_columns()
        if tcm.TCM_MODE:
            # TCM result handling:
            # - small result (only one batch): just return the executePlanResponse
            # - large result (more than one batch): return a tuple with query UUID, arrow schema, and spark schema.
            # If TCM_RETURN_QUERY_ID_FOR_SMALL_RESULT is true, all results will be treated as large result.
            is_large_result = False
            second_batch = False
            first_arrow_table = None
            with filtered_result_df.session.query_history() as qh:
                for arrow_table in to_arrow_batch_iter(filtered_result_df):
                    if second_batch:
                        is_large_result = True
                        break
                    first_arrow_table = arrow_table
                    second_batch = True
                queries_cnt = len(
                    filtered_result_df._plan.execution_queries[PlanQueryType.QUERIES]
                )
                # get query uuid from the last query; this may not be the last queries in query history because snowpark
                # may run some post action queries, e.g., drop temp table.
                query_id = qh.queries[queries_cnt - 1].query_id
            if first_arrow_table is None:
                # empty arrow batch iterator
                pandas_df = filtered_result_df.to_pandas()
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
                    map_snowpark_types_to_pyarrow_types(
                        snowpark_schema,
                        pa.struct(first_arrow_table.schema),
                        rename_struct_columns=True,
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
            arrow_table_iter = to_arrow_batch_iter(filtered_result_df)
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
                pandas_df = filtered_result_df.to_pandas()
                data_bytes = pandas_empty_table_to_arrow_bytes(
                    pandas_df, snowpark_schema, spark_columns
                )
                yield _build_execute_plan_response(0, data_bytes, schema, request)
