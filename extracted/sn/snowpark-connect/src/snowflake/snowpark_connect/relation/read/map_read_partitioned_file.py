#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import collections
import re
from collections.abc import Callable
from copy import deepcopy
from typing import Any, Literal

from snowflake import snowpark
from snowflake.snowpark import (
    DataFrame,
    DataFrameReader,
    Session,
    functions as snowpark_fn,
)
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark.column import METADATA_FILENAME
from snowflake.snowpark.functions import col, lit
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    DoubleType,
    IntegerType,
    MapType,
    StringType,
    StructField,
    StructType,
)
from snowflake.snowpark_connect.config import external_table_location, str_to_bool
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.utils import normalize_stage_path
from snowflake.snowpark_connect.type_mapping import map_type_to_snowflake_type
from snowflake.snowpark_connect.utils.context import (
    get_spark_session_id,
    register_request_external_table,
)
from snowflake.snowpark_connect.utils.io_utils import cached_file_format

FileFormat = Literal["parquet", "csv", "json", "text"]

# Supported file extensions for partition discovery
SUPPORTED_FILE_EXTENSIONS = {
    "parquet": [".parquet"],
    "csv": [".csv", ".txt", ".tsv"],
    "json": [".json", ".jsonl", ".ndjson"],
    "text": [".txt", ".text"],
}

STRUCTURED_TYPE_PATTERN = re.compile(r"\([^)]*\)")


def _add_partition_columns(
    df: DataFrame,
    partition_columns: list[str],
    partition_types: dict[str, DataType],
) -> DataFrame:
    """Add partition columns extracted from METADATA$FILENAME to a DataFrame."""
    col_names = []
    col_exprs = []
    for col_name in partition_columns:
        quoted_col_name = quote_name_without_upper_casing(col_name)
        escaped_col_name = re.escape(col_name)
        regex_pattern = rf"{escaped_col_name}=([^/]+)"
        raw_value = snowpark_fn.regexp_extract(METADATA_FILENAME, regex_pattern, 1)
        value_or_null = (
            snowpark_fn.when(raw_value == "", None)
            .when(raw_value == "__HIVE_DEFAULT_PARTITION__", None)
            .otherwise(raw_value)
        )
        col_names.append(quoted_col_name)
        col_exprs.append(snowpark_fn.cast(value_or_null, partition_types[col_name]))
    if col_names:
        df = df.with_columns(col_names, col_exprs)
    return df


def _read_partitioned_file_with_partitions(
    session: Session,
    reader: DataFrameReader,
    file_format: FileFormat,
    path: str,
    schema: StructType | None,
    snowpark_options: dict[str, Any],
    raw_options: dict[str, Any],
) -> tuple[DataFrame, list[str], bool]:
    """
    Reads files and adds partition columns from subdirectories (Hive-style partitioning).
    Returns a tuple of read DataFrame, list of partition columns and a boolean indicating if DataFrame was read from external table.

    Args:
        session: The Snowpark session.
        reader: The DataFrameReader to use.
        file_format: The format of the files to read ("parquet", "csv", "json", "text").
        path: The path to read from.
        schema: Optional schema to use.
        snowpark_options: Options to pass to the reader.
        raw_options: Raw options for additional configurations.

    Returns:
        A tuple of (DataFrame, list[str], bool) where the list represents partition columns and bool indicates if external table was used.
    """
    partition_columns, inferred_types = _discover_partition_columns(
        session, path, file_format
    )

    def _get_df() -> DataFrame:
        if not partition_columns:
            return read_file(reader, file_format, path)
        else:
            # Add METADATA$FILENAME only if the reader doesn't already have it
            # (it may have been added by add_filename_metadata_to_reader earlier).
            metadata_reader = reader
            if not getattr(reader, "_metadata_cols", None):
                metadata_reader = reader.with_metadata(METADATA_FILENAME)
            df = read_file(metadata_reader, file_format, path)
            df = _add_partition_columns(df, partition_columns, inferred_types)

            if str_to_bool(raw_options.get("snowpark.populateFileMetadata", "false")):
                return df

            return df.drop(METADATA_FILENAME)

    # TODO: SNOW-3017120 Add support for external tables for csv and json
    if file_format == "parquet" and use_external_table(session, path):
        if schema is None:
            schema = _get_df().schema
        return (
            read_partitioned_file_from_external_table(
                session,
                schema,
                external_table_location(),
                path[1:-1],
                file_format,
                partition_columns,
                inferred_types,
                snowpark_options,
            ),
            partition_columns,
            True,
        )
    else:
        return _get_df(), partition_columns, False


def _read_file_with_partitions(
    session: Session,
    reader: DataFrameReader,
    file_format: FileFormat,
    path: str,
    schema: StructType | None,
    snowpark_options: dict[str, Any],
    raw_options: dict[str, Any],
    relax_types_to_infer_schema: bool = False,
) -> tuple[DataFrame, bool]:
    df, partition_columns, uses_external_table = _read_partitioned_file_with_partitions(
        session, reader, file_format, path, schema, snowpark_options, raw_options
    )

    if relax_types_to_infer_schema and file_format == "json":
        from snowflake.snowpark_connect.relation.read.map_read_json import (
            relax_json_types,
        )

        relaxed_schema = relax_json_types(df.schema)
        # Build the re-read schema excluding METADATA$FILENAME and partition
        # columns.  Partition columns are extracted from METADATA$FILENAME via
        # regexp_extract (not from JSON content), so they must be re-applied
        # after the re-read to support externally-written Hive partitioned data.
        partition_col_names = set(partition_columns)
        normalized = StructType(
            [
                StructField(
                    unquote_if_quoted(f.name),
                    f.datatype,
                    nullable=f.nullable,
                )
                for f in relaxed_schema.fields
                if unquote_if_quoted(f.name) != "METADATA$FILENAME"
                and unquote_if_quoted(f.name) not in partition_col_names
            ]
        )

        if partition_columns:
            # Preserve partition column types from the relaxed schema
            partition_types = {
                unquote_if_quoted(f.name): f.datatype
                for f in relaxed_schema.fields
                if unquote_if_quoted(f.name) in partition_col_names
            }
            metadata_reader = reader
            if not getattr(reader, "_metadata_cols", None):
                metadata_reader = reader.with_metadata(METADATA_FILENAME)
            df = metadata_reader.schema(normalized).json(path)
            df = _add_partition_columns(df, partition_columns, partition_types)
            if not str_to_bool(
                raw_options.get("snowpark.populateFileMetadata", "false")
            ):
                df = df.drop(METADATA_FILENAME)
        else:
            df = reader.schema(normalized).json(path)

    return df, uses_external_table


def read_file(
    reader: DataFrameReader,
    file_format: FileFormat,
    path: str,
) -> DataFrame:
    """
    Read a file using the appropriate reader method based on file format.

    Args:
        reader: The DataFrameReader to use.
        file_format: The format of the file ("parquet", "csv", "json", "text").
        path: The path to the file.

    Returns:
        A DataFrame with the file contents.
    """
    match file_format:
        case "parquet":
            return reader.parquet(path)
        case "csv" | "text":
            return reader.csv(path)
        case "json":
            return reader.json(path)
        case _:
            raise ValueError(f"Unsupported file format: {file_format}")


def use_external_table(session: Session, path: str) -> bool:
    """
    Check if an external table should be used for reading the file.

    Args:
        session: The Snowpark session.
        path: The path to check.

    Returns:
        True if an external table should be used, False otherwise.
    """
    external_table_path = external_table_location()
    stripped_path = path[1:-1]

    is_external_table_path_defined = external_table_path is not None
    is_stage = stripped_path.startswith("@")

    return (
        is_external_table_path_defined
        and is_stage
        and _is_external_stage(session, stripped_path)
    )


def _is_external_stage(session: Session, path: str) -> bool:
    """Check if the stage is an external stage."""
    try:
        stage_description = (
            session.sql(f"DESCRIBE STAGE {path.split('/')[0][1:]}")
            .filter(col('"property"') == lit("URL"))
            .collect()
        )
        return stage_description[0]["property_value"] != ""
    except Exception:
        return False


def _get_count_of_non_partition_path_parts(path: str) -> int:
    """Count the number of path parts before the first partition column."""
    count = 0
    for element in normalize_stage_path(path).split("/")[1:]:
        if "=" in element:
            break
        count += 1
    return count


def read_partitioned_file_from_external_table(
    session: Session,
    schema: StructType,
    external_table_path: str,
    path: str,
    file_format: FileFormat,
    partition_columns: list[str],
    inferred_types: dict[str, DataType],
    snowpark_options: dict[str, Any],
) -> snowpark.DataFrame:
    """
    Read partitioned files from an external table.

    This function creates an external table with the appropriate schema and partition columns,
    and reads from it. Works with all supported file formats (parquet, csv, json, text).

    Args:
        session: The Snowpark session.
        schema: The schema of the data.
        external_table_path: The path to the external table database/schema.
        path: The path to the data files.
        file_format: The format of the files.
        partition_columns: List of partition column names.
        inferred_types: Dictionary mapping column names to their inferred types.
        snowpark_options: Options for the file format.

    Returns:
        A DataFrame with the partitioned data.
    """
    skip_path_parts = _get_count_of_non_partition_path_parts(path)
    snowpark_partition_columns = ", ".join(
        [quote_name_without_upper_casing(col) for col in partition_columns]
    )
    snowpark_typed_partition_columns = ", ".join(
        [
            f"{quote_name_without_upper_casing(col)} {map_type_to_snowflake_type(inferred_types[col])} as (split_part(split_part(METADATA$FILENAME, '/', {i + skip_path_parts}), '=', 2)::{map_type_to_snowflake_type(inferred_types[col])})"
            for col, i in zip(partition_columns, range(len(partition_columns)))
        ]
    )
    snowpark_schema_columns = ",".join(
        [
            f"{field.name} {_map_snowpark_type_to_simplified_snowflake_type(field.datatype)} as (value:{field.name}::{_map_snowpark_type_to_simplified_snowflake_type(field.datatype)})"
            for field in schema.fields
            if unquote_if_quoted(field.name) not in snowpark_partition_columns
            and unquote_if_quoted(field.name) != "METADATA$FILENAME"
        ]
    )

    table_name = f"{external_table_path}.{quote_name_without_upper_casing(path + get_spark_session_id())}"
    snowpark_options_copy = deepcopy(snowpark_options)
    # These options are only used in the Snowpark Python reader, but not the actual emitted SQL.
    snowpark_options_copy.pop("PATTERN", None)
    snowpark_options_copy.pop("FORMAT_NAME", None)
    snowpark_options_copy.pop("ENFORCE_EXISTING_FILE_FORMAT", None)
    file_format_name = cached_file_format(session, file_format, snowpark_options_copy)
    session.sql(
        f"""
        CREATE OR REPLACE EXTERNAL TABLE {table_name} (
            {snowpark_typed_partition_columns},
            {snowpark_schema_columns}
        )
        PARTITION BY ({snowpark_partition_columns})
        WITH LOCATION = {path}
        FILE_FORMAT = {file_format_name}
        PATTERN = '{snowpark_options.get('PATTERN', '.*')}'
        AUTO_REFRESH = false
        """
    ).collect()
    register_request_external_table(table_name)
    map_fields_list = [
        f"{field.name}::{_map_snowpark_type_to_snowflake(field.datatype)} as {field.name}"
        if isinstance(field.datatype, (StructType, MapType, ArrayType))
        else field.name
        for field in schema.fields
    ]
    # Ensure partition columns appear in the SELECT even when the user schema
    # omits them.  The external table definition includes them (via
    # snowpark_typed_partition_columns), but the SELECT above only iterates
    # schema.fields.
    schema_field_names = {unquote_if_quoted(f.name) for f in schema.fields}
    for part_col in partition_columns:
        if part_col not in schema_field_names:
            map_fields_list.append(quote_name_without_upper_casing(part_col))
    map_fields = ", ".join(map_fields_list)
    return session.sql(f"SELECT {map_fields} FROM {table_name}")


def _map_snowpark_type_to_simplified_snowflake_type(datatype: DataType) -> str:
    """Map a Snowpark DataType to a simplified Snowflake type string."""
    if isinstance(datatype, StructType):
        return "OBJECT"
    elif isinstance(datatype, MapType):
        return "VARIANT"
    else:
        return STRUCTURED_TYPE_PATTERN.sub("", map_type_to_snowflake_type(datatype))


def _map_snowpark_type_to_snowflake(datatype: DataType) -> str:
    """Map a Snowpark DataType to a Snowflake type string with full structure."""
    if isinstance(datatype, StructType):
        object_fields = ", ".join(
            [
                f"{field.name} {_map_snowpark_type_to_snowflake(field.datatype)}"
                for field in datatype.fields
            ]
        )
        return f"OBJECT({object_fields})"
    else:
        return map_type_to_snowflake_type(datatype)


def _extract_partitions_from_path(path: str) -> dict[str, str]:
    """Extracts partition key-value pairs from a path."""
    partitions = {}
    for segment in path.split("/"):
        if "=" in segment:
            col_name, value = _parse_partition_column(segment)
            if col_name and value:
                partitions[col_name] = value
    return partitions


def _is_data_file(file_path: str, file_format: FileFormat) -> bool:
    """
    Check if a file path is a data file based on its extension.

    Args:
        file_path: The path to the file.
        file_format: The format to check against.

    Returns:
        True if the file is a data file of the specified format.
    """
    extensions = SUPPORTED_FILE_EXTENSIONS.get(file_format, [])
    lower_path = file_path.lower()
    return any(lower_path.endswith(ext) for ext in extensions)


def _discover_partition_columns(
    session: Session, stage_path: str, file_format: FileFormat = "parquet"
) -> tuple[list[str], dict[str, DataType]]:
    """
    Discovers partition columns by analyzing subdirectory structure.

    Supports all file formats by checking for appropriate file extensions.

    Args:
        session: The Snowpark session.
        stage_path: The path to the stage to analyze.
        file_format: The format of the files ("parquet", "csv", "json", "text").

    Returns:
        A tuple of (ordered_columns, inferred_types) where ordered_columns is
        a list of partition column names in order and inferred_types maps
        column names to their inferred DataTypes.
    """
    partition_columns_values = collections.defaultdict(set)
    dir_level_to_column_name = {}
    base_partitions = _extract_partitions_from_path(stage_path)

    # Normalize for segment counting so that '@stage/dir/' produces the same
    # segment count as '@stage/dir'.
    count_path = normalize_stage_path(stage_path)
    path_segments_to_skip = len(count_path.split("/"))
    if count_path.startswith("@"):
        path_segments_to_skip = 1
        stage_parts = count_path.split("/", 2)
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
                # Check if this is a partition directory (contains '=' but is not a data file)
                if "=" in part and not _is_data_file(part, file_format):
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

            # Check if this is a data file of the specified format
            if _is_data_file(file_path, file_format):
                unique_partition_key_paths.add(", ".join(keys))

        if len(unique_partition_key_paths) > 1:
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
    """Infer the DataType for a partition column based on its values."""

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
