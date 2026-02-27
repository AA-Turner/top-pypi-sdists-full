#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from typing import Any

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark import DataFrame, DataFrameReader, Session
from snowflake.snowpark._internal.analyzer import analyzer_utils
from snowflake.snowpark.types import StructType, TimestampTimeZone, TimestampType
from snowflake.snowpark_connect.config import (
    get_boolean_session_config_param,
    global_config,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.map_read_partitioned_file import (
    _read_file_with_partitions,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    add_filename_metadata_to_reader,
)
from snowflake.snowpark_connect.relation.read.reader_config import ReaderWriterConfig
from snowflake.snowpark_connect.relation.read.utils import (
    apply_metadata_exclusion_pattern,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.io_utils import cached_file_format
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def map_read_parquet(
    rel: relation_proto.Relation,
    schema: StructType | None,
    session: snowpark.Session,
    paths: list[str],
    options: ReaderWriterConfig,
) -> DataFrameContainer:
    """Read a Parquet file into a Snowpark DataFrame."""

    if rel.read.is_streaming is True:
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for Parquet files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    converted_snowpark_options = options.convert_to_snowpark_args()
    file_format_options = _parse_parquet_snowpark_options(converted_snowpark_options)
    raw_options = rel.read.data_source.options
    assert len(paths) > 0, "Read PARQUET expects at least one path"

    snowpark_options = {
        # Setting these two options prevents a significant number of additional CREATE TEMPORARY
        # FILE FORMAT and DROP FILE FORMAT queries. If FORMAT_NAME is not set, the Snowpark DF reader
        # will eagerly issue a CREATE TEMPORARY FILE FORMAT when inferring the schema of the result;
        # if ENFORCE_EXISTING_FILE_FORMAT is not set, an additional CREATE ... command will be
        # issued when the lazy DF is materialized by a cache_result call.
        "FORMAT_NAME": converted_snowpark_options.get(
            "FORMAT_NAME",
            cached_file_format(session, "parquet", file_format_options),
        ),
        "ENFORCE_EXISTING_FILE_FORMAT": True,
    }

    if "PATTERN" in converted_snowpark_options:
        snowpark_options["PATTERN"] = converted_snowpark_options.get("PATTERN")

    apply_metadata_exclusion_pattern(snowpark_options)

    reader = add_filename_metadata_to_reader(
        session.read.options(snowpark_options), raw_options
    )

    if len(paths) == 1:
        df, read_using_external_table = _read_parquet_with_partitions(
            session, reader, paths[0], schema, snowpark_options, raw_options
        )
        can_be_cached = not read_using_external_table
    else:
        is_merge_schema = options.config.get("mergeschema")
        df, read_using_external_table = _read_parquet_with_partitions(
            session, reader, paths[0], schema, snowpark_options, raw_options
        )
        can_be_cached = not read_using_external_table
        schema_cols = df.columns
        for p in paths[1:]:
            reader._user_schema = None
            partition_df, read_using_external_table = _read_parquet_with_partitions(
                session, reader, p, schema, snowpark_options, raw_options
            )
            df = df.union_all_by_name(
                partition_df,
                allow_missing_columns=True,
            )
            can_be_cached = can_be_cached and not read_using_external_table

        if not is_merge_schema:
            df = df.select(*schema_cols)

    infer_ntz = get_boolean_session_config_param(
        "spark.sql.parquet.inferTimestampNTZ.enabled"
    )
    if not infer_ntz:
        df = _cast_ntz_to_ltz(df)

    renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
        df, rel.common.plan_id
    )
    return DataFrameContainer.create_with_column_mapping(
        dataframe=renamed_df,
        spark_column_names=[analyzer_utils.unquote_if_quoted(c) for c in df.columns],
        snowpark_column_names=snowpark_column_names,
        snowpark_column_types=[
            emulate_integral_types(f.datatype) for f in df.schema.fields
        ],
        can_be_cached=can_be_cached,
    )


def _read_parquet_with_partitions(
    session: Session,
    reader: DataFrameReader,
    path: str,
    schema: StructType | None,
    snowpark_options: dict[str, Any],
    raw_options: dict[str, Any],
) -> tuple[DataFrame, bool]:
    """
    Reads parquet files and adds partition columns from subdirectories.
    Returns a tuple of read DataFrame and a boolean indicating if DataFrame was read from external table.

    This function delegates to the generalized _read_file_with_partitions function.
    """

    return _read_file_with_partitions(
        session=session,
        reader=reader,
        file_format="parquet",
        path=path,
        schema=schema,
        snowpark_options=snowpark_options,
        raw_options=raw_options,
    )


def _cast_ntz_to_ltz(df: DataFrame) -> DataFrame:
    """When inferTimestampNTZ.enabled is false, reinterpret TIMESTAMP_NTZ columns as UTC instants.

    A simple CAST(ntz AS TIMESTAMP_LTZ) interprets the NTZ value in the session
    timezone, which preserves the wall-clock time. We need CONVERT_TIMEZONE which
    treats NTZ as UTC, matching Spark's behavior of reading all Parquet timestamps
    as UTC-based instants regardless of isAdjustedToUTC.
    """
    from snowflake.snowpark.functions import builtin, col, lit

    convert_tz = builtin("CONVERT_TIMEZONE")
    session_tz = global_config.spark_sql_session_timeZone
    ltz_type = TimestampType(TimestampTimeZone.LTZ)
    for field in df.schema.fields:
        if (
            isinstance(field.datatype, TimestampType)
            and field.datatype.tz == TimestampTimeZone.NTZ
        ):
            df = df.with_column(
                field.name,
                convert_tz(lit("UTC"), lit(session_tz), col(field.name)).cast(ltz_type),
            )
    return df


_parquet_file_format_allowed_options = {
    "COMPRESSION",
    "SNAPPY_COMPRESSION",
    "BINARY_AS_TEXT",
    "TRIM_SPACE",
    "USE_LOGICAL_TYPE",
    "USE_VECTORIZED_SCANNER",
    "REPLACE_INVALID_CHARACTERS",
    "NULL_IF",
}


def _parse_parquet_snowpark_options(snowpark_options: dict[str, Any]) -> dict[str, Any]:
    file_format_options = dict()
    for key, value in snowpark_options.items():
        upper_key = key.upper()
        if upper_key in _parquet_file_format_allowed_options:
            file_format_options[upper_key] = value
    return file_format_options
