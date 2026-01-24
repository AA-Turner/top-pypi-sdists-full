#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import collections
import re
from collections.abc import Callable
from typing import Any

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark import (
    DataFrame,
    DataFrameReader,
    Session,
    functions as snowpark_fn,
)
from snowflake.snowpark._internal.analyzer import analyzer_utils
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from snowflake.snowpark.column import METADATA_FILENAME
from snowflake.snowpark.types import (
    DataType,
    DoubleType,
    IntegerType,
    StringType,
    StructType,
)
from snowflake.snowpark_connect.config import external_table_location
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.map_read_partitioned_parquet import (
    read_partitioned_parquet_from_external_table,
    use_external_table,
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
            session, reader, paths[0], schema, snowpark_options
        )
        can_be_cached = not read_using_external_table
    else:
        is_merge_schema = options.config.get("mergeschema")
        df, read_using_external_table = _read_parquet_with_partitions(
            session, reader, paths[0], schema, snowpark_options
        )
        can_be_cached = not read_using_external_table
        schema_cols = df.columns
        for p in paths[1:]:
            reader._user_schema = None
            partition_df, read_using_external_table = _read_parquet_with_partitions(
                session, reader, p, schema, snowpark_options
            )
            df = df.union_all_by_name(
                partition_df,
                allow_missing_columns=True,
            )
            can_be_cached = can_be_cached and not read_using_external_table

        if not is_merge_schema:
            df = df.select(*schema_cols)

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
) -> tuple[DataFrame, bool]:
    """
    Reads parquet files and adds partition columns from subdirectories.
    Returns a tuple of read DataFrame and a boolean indicating if DataFrame was read from external table.
    """

    partition_columns, inferred_types = _discover_partition_columns(session, path)

    def _get_df() -> DataFrame:
        if not partition_columns:
            return reader.parquet(path)
        else:
            # In case of too big overhead we can always optimize by using option: MAX_FILE_COUNT and allow user to define how many files should be scanned
            df = reader.with_metadata(METADATA_FILENAME).parquet(path)

            for col_name in partition_columns:
                quoted_col_name = quote_name_without_upper_casing(col_name)
                escaped_col_name = re.escape(col_name)
                regex_pattern = rf"{escaped_col_name}=([^/]+)"

                raw_value = snowpark_fn.regexp_extract(
                    METADATA_FILENAME, regex_pattern, 1
                )
                value_or_null = (
                    snowpark_fn.when(raw_value == "", None)
                    .when(raw_value == "__HIVE_DEFAULT_PARTITION__", None)
                    .otherwise(raw_value)
                )

                df = df.with_column(
                    quoted_col_name,
                    snowpark_fn.cast(value_or_null, inferred_types[col_name]),
                )
            return df.drop(METADATA_FILENAME)

    if use_external_table(session, path):
        if schema is None:
            schema = _get_df().schema
        return (
            read_partitioned_parquet_from_external_table(
                session,
                schema,
                external_table_location(),
                path[1:-1],
                partition_columns,
                inferred_types,
                snowpark_options,
            ),
            True,
        )
    else:
        # TODO: SNOW-2736756 support user schema
        assert schema is None, "Read PARQUET does not support user schema"
        return _get_df(), False


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


def _extract_partitions_from_path(path: str) -> dict[str, str]:
    """Extracts partition key-value pairs from a path."""
    partitions = {}
    for segment in path.split("/"):
        if "=" in segment:
            col_name, value = _parse_partition_column(segment)
            if col_name and value:
                partitions[col_name] = value
    return partitions


def _discover_partition_columns(
    session: Session, stage_path: str
) -> tuple[list[str], dict[str, DataType]]:
    """Discovers partition columns by analyzing subdirectory structure."""

    partition_columns_values = collections.defaultdict(set)
    dir_level_to_column_name = {}
    base_partitions = _extract_partitions_from_path(stage_path)

    path_segments_to_skip = len(stage_path.strip("/").split("/"))
    if stage_path.startswith("@"):
        path_segments_to_skip = 1
        stage_parts = stage_path.split("/", 2)
        if len(stage_parts) > 2:
            additional_segments = len(stage_parts[2].strip("/").split("/"))
            path_segments_to_skip += additional_segments

    ls_result = session.sql(f"LS {stage_path}").collect()
    if ls_result:
        file_names = [row[0] for row in ls_result]
        unique_partition_key_paths = set()
        for file_path in file_names:
            path_parts = file_path.strip("/").split("/")
            path_segments_to_analyze = path_parts[path_segments_to_skip:]
            keys = list()

            for i, part in enumerate(path_segments_to_analyze):
                if "=" in part and not part.endswith(".parquet"):
                    key, value = part.split("=", 1)
                    keys.append(key)

                    if key in base_partitions:
                        continue

                    if i not in dir_level_to_column_name:
                        dir_level_to_column_name[i] = key
                    elif dir_level_to_column_name[i] != key:
                        exception = ValueError(
                            f"Conflicting partition column names detected: '{dir_level_to_column_name[i]}' and '{key}' "
                            f"at the same directory level"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_OPERATION
                        )
                        raise exception

                    partition_columns_values[key].add(value)

            if file_path.endswith(".parquet"):
                unique_partition_key_paths.add(", ".join(keys))

        if len(unique_partition_key_paths) != 1:
            incorrect_partition_message = "\n".join(
                [
                    f"Partition column name list #{i + 1}: {partitions}"
                    for i, partitions in enumerate(unique_partition_key_paths)
                ]
            )
            error_message = f"""
Conflicting partition column names detected:

{incorrect_partition_message}

For partitioned table directories, data files should only live in leaf directories.
And directories at the same level should have the same partition column name."""
            exception = ValueError(error_message)
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
    seen_columns = set()
    for level in sorted(dir_level_to_column_name.keys()):
        col_name = dir_level_to_column_name[level]
        if col_name in seen_columns:
            exception = ValueError(
                f"Found partition column '{col_name}' at multiple directory levels. "
                f"A partition column can only appear at a single level."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
        seen_columns.add(col_name)

    ordered_columns = [
        dir_level_to_column_name[level]
        for level in sorted(dir_level_to_column_name.keys())
    ]

    inferred_types = {
        col_name: _infer_partition_column_type(partition_columns_values[col_name])
        for col_name in ordered_columns
    }

    return ordered_columns, inferred_types


def _infer_partition_column_type(values: set[str]) -> DataType:
    def _is_castable(value: str, type_: Callable) -> bool:
        try:
            type_(value)
            return True
        except ValueError:
            return False

    values = list(filter(lambda v: v != "__HIVE_DEFAULT_PARTITION__", values))
    if values and all(_is_castable(value, int) for value in values):
        return IntegerType()
    if values and all(_is_castable(value, float) for value in values):
        return DoubleType()
    return StringType()


def _parse_partition_column(name: str) -> tuple[str, str]:
    """Extracts column name and partition value from a path segment."""
    col_name, partition_value = name.split("=", maxsplit=1)

    return col_name, partition_value
