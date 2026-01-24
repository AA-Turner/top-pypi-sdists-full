#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pandas
import pyarrow as pa
import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyarrow import Table
from pyspark.sql.pandas.types import _dedup_names

from snowflake.snowpark import types as sf_types
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.type_mapping import map_snowpark_types_to_pyarrow_types
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def is_streaming(rel: relation_proto.Relation) -> bool:
    """
    Check if the relation is a streaming relation.

    A streaming relation is a relation that is the result of a streaming
    operation. This is used to determine if the relation should be shown
    immediately or if it should be stored in the session state for later use.
    """
    """Check if the relation is a streaming relation."""
    try:
        match rel.WhichOneof("rel_type"):
            case "read":
                return rel.read.is_streaming is True
            case "project":
                return is_streaming(rel.project.input)
            case "filter":
                return is_streaming(rel.filter.input)
            case "join":
                return is_streaming(rel.join.left) or is_streaming(rel.join.right)
            case "set_op":
                return is_streaming(rel.set_op.input)
            case "sort":
                return is_streaming(rel.sort.input)
            case "limit":
                return is_streaming(rel.limit.input)
            case "aggregate":
                return is_streaming(rel.aggregate.input)
            case "sample":
                return is_streaming(rel.sample.input)
            case "offset":
                return is_streaming(rel.offset.input)
            case "deduplicate":
                return is_streaming(rel.deduplicate.input)
            case "subquery_alias":
                return is_streaming(rel.subquery_alias.input)
            case "repartition":
                return is_streaming(rel.repartition.input)
            case "to_df":
                return is_streaming(rel.to_df.input)
            case "with_columns_renamed":
                return is_streaming(rel.with_columns_renamed.input)
            case "show_string":
                return is_streaming(rel.show_string.input)
            case "drop":
                return is_streaming(rel.drop.input)
            case "tail":
                return is_streaming(rel.tail.input)
            case "with_columns":
                return is_streaming(rel.with_columns.input)
            case "hint":
                return is_streaming(rel.hint.input)
            case "unpivot":
                return is_streaming(rel.unpivot.input)
            case "to_schema":
                return is_streaming(rel.to_schema.input)
            case "repartition_by_expression":
                return is_streaming(rel.repartition_by_expression.input)
            case "map_partitions":
                return is_streaming(rel.map_partitions.input)
            case "collect_metrics":
                return is_streaming(rel.collect_metrics.input)
            case "parse":
                return is_streaming(rel.parse.input)
            case "group_map":
                return is_streaming(rel.group_map.input)
            case "co_group_map":
                return is_streaming(rel.co_group_map.input)
            case "with_watermark":
                return is_streaming(rel.with_watermark.input)
            case "apply_in_pandas_with_state":
                return is_streaming(rel.apply_in_pandas.input)
            case "html_string":
                return is_streaming(rel.html_string.input)
            case "cached_remote_relation":
                exception = SnowparkConnectNotImplementedError(
                    "Cached remote relation not implemented"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            case "common_inline_user_defined_table_function":
                return is_streaming(rel.common_inline_user_defined_table_function.input)
            case "fill_na":
                return is_streaming(rel.fill_na.input)
            case "drop_na":
                return is_streaming(rel.drop_na.input)
            case "replace":
                return is_streaming(rel.replace.input)
            case "stat":
                return is_streaming(rel.stat.input)
            case "summary":
                return is_streaming(rel.summary.input)
            case "crosstab":
                return is_streaming(rel.crosstab.input)
            case "describe":
                return is_streaming(rel.describe.input)
            case "cov":
                return is_streaming(rel.cov.input)
            case "corr":
                return is_streaming(rel.corr.input)
            case "approx_quantile":
                return is_streaming(rel.approx_quantile.input)
            case "freq_items":
                return is_streaming(rel.freq_items.input)
            case "sample_by":
                return is_streaming(rel.sample_by.input)
            case _:
                return False
    except AttributeError:
        # This is a leaf node with no `input`.
        return False


def pandas_to_arrow_batches_bytes(pandas_df: pandas.DataFrame) -> bytes:
    """
    Serialize a pandas DataFrame as Pyarrow encoded bytes.
    """
    # Pyarrow doesn't support duplicate column names, so we need to deduplicate them.
    # It is important that the schema is passed in whatever message we send back to the
    # client, otherwise the names will not be correct.
    pandas_df.columns = _dedup_names(pandas_df.columns)
    sink = pa.BufferOutputStream()
    batch = pa.RecordBatch.from_pandas(pandas_df, schema=None)
    with pa.ipc.new_stream(sink, batch.schema) as writer:
        writer.write_batch(batch)
    return sink.getvalue().to_pybytes()


def arrow_table_to_arrow_bytes(
    table: pa.Table, snowpark_schema: sf_types.StructType, spark_columns: list
) -> bytes:
    """
    Serialize a pyarrow.table as Pyarrow encoded bytes according to provided snowpark schema.
    """
    assert table.num_rows > 0, "Table must have at least one row"

    pa_schema = pa.schema(
        map_snowpark_types_to_pyarrow_types(
            snowpark_schema, pa.struct(table.schema), rename_struct_columns=True
        )
    )
    table = _cast_arrow_table(table, pa_schema, spark_columns)
    # note that we don't need to track the original column name, since this helper function only needs to generate arrow
    # data bytes. When the arrow bytes are returned to spark connect client, an explicit schema would be passed along,
    # which contains expected column name. E.g.,
    #   return [
    #         proto_base.ExecutePlanResponse(
    #             session_id=request.session_id,
    #             operation_id=SERVER_SIDE_SESSION_ID,
    #             arrow_batch=proto_base.ExecutePlanResponse.ArrowBatch(
    #                 row_count=row_count,
    #                 data=arrow_bytes, # arrow bytes generated by this helper function
    #             ),
    #             schema=schema,    # schema containing correct column name
    #         ),
    #   ]
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, table.schema) as writer:
        writer.write_table(table)
    arrow_bytes = sink.getvalue().to_pybytes()
    return arrow_bytes


def _cast_arrow_table(table: Table, pa_schema: pa.Schema, spark_columns: list) -> Table:
    # 1. rename column names to 0,1,2, etc. to avoid unmatching names due to undesired factors like quotes.
    # 2. casting is required here because sometimes arrow table does use expected data type. E.g., for LongType,
    #       pyarrow table uses decimal128(38,0), which converts to Decimal instead of Long on client side.
    table = table.rename_columns([str(i) for i in range(table.num_columns)])
    table = table.cast(pa_schema, safe=False)
    table = table.rename_columns(spark_columns)
    return table


def pandas_empty_table_to_arrow_bytes(
    pandas_df: pandas.DataFrame,
    snowpark_schema: sf_types.StructType,
    spark_columns: list,
) -> bytes:
    """
    Serialize an empty pandas DataFrame as Pyarrow encoded bytes according to provided snowpark schema and spark columns.
    """
    pandas_df.columns = _dedup_names(pandas_df.columns)
    table = pa.Table.from_pandas(pandas_df)
    pa_schema = pa.schema(
        map_snowpark_types_to_pyarrow_types(
            snowpark_schema,
            pa.struct(table.schema),
            rename_struct_columns=True,
            for_empty_table=True,
        )
    )
    table = _cast_arrow_table(table, pa_schema, spark_columns)
    return pandas_to_arrow_batches_bytes(table.to_pandas())
