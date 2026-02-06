#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy
import logging
from typing import Any

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)
from snowflake.snowpark._internal.utils import (
    TempObjectType,
    random_name_for_temp_object,
)
from snowflake.snowpark.dataframe_reader import DataFrameReader
from snowflake.snowpark.types import (
    DataType,
    DecimalType,
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
    _FractionalType,
    _IntegralType,
)
from snowflake.snowpark_connect.config import global_config, str_to_bool
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.map_read import CsvReaderConfig
from snowflake.snowpark_connect.relation.read.map_read_partitioned_file import (
    _read_file_with_partitions,
    _read_partitioned_file_with_partitions,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    add_filename_metadata_to_reader,
    get_non_metadata_fields,
)
from snowflake.snowpark_connect.relation.read.utils import (
    apply_metadata_exclusion_pattern,
    extract_relative_file_path,
    extract_stage_from_path,
    get_spark_column_names_from_snowpark_columns,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import (
    _integral_types_conversion_enabled,
    emulate_integral_types,
)
from snowflake.snowpark_connect.utils.io_utils import cached_file_format
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)

logger = logging.getLogger("snowflake_connect_server")


def map_read_csv(
    rel: relation_proto.Relation,
    schema: snowpark.types.StructType | None,
    session: snowpark.Session,
    paths: list[str],
    options: CsvReaderConfig,
) -> DataFrameContainer:
    """
    Read a CSV file into a Snowpark DataFrame.

    We leverage the stage that is already created in the map_read function that
    calls this.
    """

    if rel.read.is_streaming is True:
        # TODO: Structured streaming implementation.
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for CSV files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    else:
        converted_snowpark_options = options.convert_to_snowpark_args()
        parse_header = converted_snowpark_options.get("PARSE_HEADER", False)
        file_format_options = _parse_csv_snowpark_options(converted_snowpark_options)
        file_format = cached_file_format(session, "csv", file_format_options)

        snowpark_reader_options = dict()
        snowpark_reader_options["FORMAT_NAME"] = file_format
        snowpark_reader_options["ENFORCE_EXISTING_FILE_FORMAT"] = True
        snowpark_reader_options["INFER_SCHEMA"] = converted_snowpark_options.get(
            "INFER_SCHEMA", False
        )
        snowpark_reader_options[
            "INFER_SCHEMA_OPTIONS"
        ] = converted_snowpark_options.get("INFER_SCHEMA_OPTIONS", {})

        # Use Try_cast to avoid schema inference errors
        if snowpark_reader_options.get("INFER_SCHEMA", False):
            snowpark_reader_options["TRY_CAST"] = True

        apply_metadata_exclusion_pattern(converted_snowpark_options)
        snowpark_reader_options["PATTERN"] = converted_snowpark_options.get(
            "PATTERN", None
        )

        raw_options = rel.read.data_source.options

        if schema is None or (
            parse_header
            and str(raw_options.get("enforceSchema", "True")).lower() == "false"
        ):  # Schema has to equals to header's format
            reader = add_filename_metadata_to_reader(
                session.read.options(snowpark_reader_options), raw_options
            )
        else:
            reader = add_filename_metadata_to_reader(
                session.read.options(snowpark_reader_options).schema(schema),
                raw_options,
            )

        result_can_be_cached = True

        if str_to_bool(raw_options.get("snowpark.populateFileMetadata", "false")):
            # TODO: SNOW-3002469 copy into approach does not support metadata columns today, so we fallback to the UNION ALL approach.
            # Use partitioned file reading to support Hive-style partitioning
            df, read_using_external_table = _read_csv_with_partitions(
                session,
                reader,
                paths[0],
                schema,
                snowpark_reader_options,
                file_format_options,
                raw_options,
                parse_header,
            )
            result_can_be_cached = (
                result_can_be_cached and not read_using_external_table
            )
            # Note: UNION ALL operates sequentially which can be a bottleneck for large datasets.
            for p in paths[1:]:
                partition_df, read_using_external_table = _read_csv_with_partitions(
                    session,
                    reader,
                    p,
                    schema,
                    snowpark_reader_options,
                    file_format_options,
                    raw_options,
                    parse_header,
                )
                df = df.union_all(partition_df)
                result_can_be_cached = (
                    result_can_be_cached and not read_using_external_table
                )
        else:
            # Use copy into approach for parallel loading.
            if len(paths) == 1:
                # Try to read with partitions (Hive-style partitioning)
                df, read_using_external_table = _read_csv_with_partitions(
                    session,
                    reader,
                    paths[0],
                    schema,
                    snowpark_reader_options,
                    file_format_options,
                    raw_options,
                    parse_header,
                )
                result_can_be_cached = (
                    result_can_be_cached and not read_using_external_table
                )

            if len(paths) > 1:
                # Note: this assumes that all paths are exact filenames, not directories. It will fail early if any path is a directory.
                # When reading a direct path to partitioned file, partitions are not included in the final result.
                logger.debug(
                    f"Using COPY INTO FILES optimization for {len(paths)} files."
                )
                result_can_be_cached = False  # to avoid caching the result.
                # Generate a temporary table name
                temp_table_name = random_name_for_temp_object(TempObjectType.TABLE)
                df = session.table(temp_table_name)
                stage_file_groups = _generate_stage_path_groups(paths)
                for stage, stage_files in stage_file_groups:
                    # Get schema from the first file
                    copy_into_schema = _get_schema_for_copy_into(
                        reader=reader,
                        session=session,
                        schema=schema,
                        first_path=stage_files[0],
                        file_format_options=file_format_options,
                        snowpark_reader_options=snowpark_reader_options,
                        raw_options=raw_options,
                        parse_header=parse_header,
                    )
                    if len(stage_files) == 1:
                        _load_csv_with_copy_into(
                            reader=reader,
                            target=temp_table_name,
                            paths=[],
                            stage=stage_files[0],
                            schema=copy_into_schema,
                            file_format_options=file_format_options,
                        )
                    else:
                        _load_csv_with_copy_into(
                            reader=reader,
                            target=temp_table_name,
                            paths=stage_files,
                            stage=stage,
                            schema=copy_into_schema,
                            file_format_options=file_format_options,
                        )

        if schema is None and not str_to_bool(
            str(raw_options.get("inferSchema", raw_options.get("inferschema", "false")))
        ):
            df = df.select(
                [snowpark_fn.col(c).cast("STRING").alias(c) for c in df.schema.names]
            )

        spark_column_names = get_spark_column_names_from_snowpark_columns(df.columns)

        renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
            df, rel.common.plan_id
        )
        return DataFrameContainer.create_with_column_mapping(
            dataframe=renamed_df,
            spark_column_names=spark_column_names,
            snowpark_column_names=snowpark_column_names,
            snowpark_column_types=[
                _emulate_integral_types_for_csv(f.datatype) for f in df.schema.fields
            ],
            can_be_cached=result_can_be_cached,
        )


_csv_file_format_allowed_options = {
    "COMPRESSION",
    "RECORD_DELIMITER",
    "FIELD_DELIMITER",
    "MULTI_LINE",
    "FILE_EXTENSION",
    "PARSE_HEADER",
    "SKIP_HEADER",
    "SKIP_BLANK_LINES",
    "DATE_FORMAT",
    "TIME_FORMAT",
    "TIMESTAMP_FORMAT",
    "BINARY_FORMAT",
    "ESCAPE",
    "ESCAPE_UNENCLOSED_FIELD",
    "TRIM_SPACE",
    "FIELD_OPTIONALLY_ENCLOSED_BY",
    "NULL_IF",
    "ERROR_ON_COLUMN_COUNT_MISMATCH",
    "REPLACE_INVALID_CHARACTERS",
    "EMPTY_FIELD_AS_NULL",
    "SKIP_BYTE_ORDER_MARK",
    "ENCODING",
}


def _parse_csv_snowpark_options(snowpark_options: dict[str, Any]) -> dict[str, Any]:
    file_format_options = dict()
    for key, value in snowpark_options.items():
        upper_key = key.upper()
        if upper_key in _csv_file_format_allowed_options:
            file_format_options[upper_key] = value

    # This option has to be removed, because we cannot use at the same time predefined file format and parse_header option
    # Such combination causes snowpark to raise SQL compilation error: Invalid file format "PARSE_HEADER" is only allowed for CSV INFER_SCHEMA and MATCH_BY_COLUMN_NAME
    parse_header = file_format_options.get("PARSE_HEADER", False)
    if parse_header:
        file_format_options["SKIP_HEADER"] = 1
        del file_format_options["PARSE_HEADER"]

    # Match Spark behavior: always skip blank lines
    file_format_options["SKIP_BLANK_LINES"] = True

    return file_format_options


def _read_csv_with_partitions(
    session: snowpark.Session,
    reader: DataFrameReader,
    path: str,
    schema: StructType | None,
    snowpark_reader_options: dict[str, Any],
    file_format_options: dict[str, Any],
    raw_options: dict,
    parse_header: bool,
) -> tuple[snowpark.DataFrame, bool]:
    """
    Reads CSV files and adds partition columns from subdirectories (Hive-style partitioning).

    Returns a tuple of read DataFrame and a boolean indicating if DataFrame was read from external table.

    Args:
        session: The Snowpark session.
        reader: The DataFrameReader to use.
        path: The path to read from.
        schema: Optional schema to use.
        snowpark_reader_options: Options for the Snowpark reader.
        file_format_options: Options for the file format.
        raw_options: Raw options from the read request.
        parse_header: Whether to parse the CSV header.

    Returns:
        A tuple of (DataFrame, bool) where the bool indicates if external table was used.
    """
    filename = path.strip("/").split("/")[-1]

    # Case 1: Schema is provided by user
    if schema is not None:
        (
            df,
            partition_columns,
            read_using_external_table,
        ) = _read_partitioned_file_with_partitions(
            session=session,
            reader=reader,
            file_format="csv",
            path=path,
            schema=schema,
            snowpark_options=snowpark_reader_options,
            raw_options=raw_options,
        )

        if not read_using_external_table:
            non_metadata_fields = get_non_metadata_fields(df.schema.fields)
            # Validate schema field count matches
            if not columns_length_equals(
                len(non_metadata_fields), len(partition_columns), len(schema.fields)
            ):
                exception = Exception(f"csv load from {filename} failed.")
                attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
                raise exception

            # If enforceSchema=False, validate header names match schema names
            if str(raw_options.get("enforceSchema", "True")).lower() == "false":
                for i in range(len(schema.fields)):
                    if (
                        schema.fields[i].name != non_metadata_fields[i].name
                        and f'"{schema.fields[i].name}"' != non_metadata_fields[i].name
                    ):
                        exception = Exception(
                            "CSV header does not conform to the schema"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_OPERATION
                        )
                        raise exception

        return df, read_using_external_table

    # Case 2: No schema provided - get headers for column names
    headers = get_header_names(
        session,
        path,
        file_format_options,
        snowpark_reader_options,
        raw_options,
        parse_header,
    )

    if len(headers) > 0:
        # Case 2a: No schema, inferSchema=False => create StringType schema from headers
        if (
            not str_to_bool(
                str(
                    raw_options.get(
                        "inferSchema", raw_options.get("inferschema", "false")
                    )
                )
            )
            and schema is None
        ):
            effective_schema = StructType(
                [StructField(h, StringType(), True) for h in headers]
            )
            reader = reader.schema(effective_schema)

            return _read_file_with_partitions(
                session=session,
                reader=reader,
                file_format="csv",
                path=path,
                schema=effective_schema,
                snowpark_options=snowpark_reader_options,
                raw_options=raw_options,
            )
        else:
            # Case 2b: No schema, inferSchema=True => read and validate/rename columns
            (
                df,
                partition_columns,
                read_using_external_table,
            ) = _read_partitioned_file_with_partitions(
                session=session,
                reader=reader,
                file_format="csv",
                path=path,
                schema=None,
                snowpark_options=snowpark_reader_options,
                raw_options=raw_options,
            )
            partition_columns = [
                quote_name_without_upper_casing(col) for col in partition_columns
            ]
            non_metadata_fields = get_non_metadata_fields(df.schema.fields)

            # Validate header count matches inferred schema
            if not columns_length_equals(
                len(non_metadata_fields), len(partition_columns), len(headers)
            ):
                exception = Exception(
                    f"CSV header: {headers} does not conform to the schema"
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception

            # Rename columns if names don't match headers
            if any(
                non_metadata_fields[i].name != headers[i] for i in range(len(headers))
            ):
                df = df.select(
                    [
                        snowpark_fn.col(non_metadata_fields[i].name).alias(headers[i])
                        for i in range(len(headers))
                        if headers[i] not in partition_columns
                    ]
                    + partition_columns
                )
        return df, read_using_external_table

    # Case 3: Fallback - no headers (shouldn't normally reach here)
    return _read_file_with_partitions(
        session=session,
        reader=reader,
        file_format="csv",
        path=path,
        schema=None,
        snowpark_options=snowpark_reader_options,
        raw_options=raw_options,
    )


def columns_length_equals(
    non_metadata_columns: int, partition_columns: int, expected_columns: int
) -> bool:
    columns_without_partitions_equals_expected_columns = (
        non_metadata_columns - partition_columns == expected_columns
    )
    column_count_equals = non_metadata_columns == expected_columns

    return columns_without_partitions_equals_expected_columns or column_count_equals


def _deduplicate_column_names_pyspark_style(
    column_names: list[str], case_sensitive: bool
) -> list[str]:
    """
    Deduplicate column names following PySpark's behavior in CSVUtils.scala::makeSafeHeader by appending
    global position index to all occurrences of duplicated names.

    Examples with case_sensitive=False:
        ['ab', 'AB'] -> ['ab0', 'AB1']
        ['ab', 'ab'] -> ['ab0', 'ab1']
        ['a', 'b', 'A', 'c', 'B'] -> ['a0', 'b1', 'A2', 'c', 'B4']  (positions: a=0,2; b=1,4; c=3)

    Examples with case_sensitive=True:
        ['ab', 'AB'] -> ['ab', 'AB']  (no duplicates, different case)
        ['ab', 'ab'] -> ['ab0', 'ab1']  (exact duplicates at positions 0, 1)
        ['a', 'b', 'A', 'c', 'B'] -> ['a', 'b', 'A', 'c', 'B']  (no duplicates)

    Edge cases:
        ['a0', 'a0'] -> ['a00', 'a01']  (appends position even if name already has digits)
        ['a', '', 'b'] -> ['a', '_c1', 'b']  (empty names become _c<position>)
    """
    seen = set()
    duplicates = set()

    for name in column_names:
        # filter out nulls and apply case transformation
        if not name:
            continue
        key = name if case_sensitive else name.lower()
        if key in seen:
            duplicates.add(key)
        else:
            seen.add(key)

    result = []
    for index, value in enumerate(column_names):
        # Empty/null, append _c<index>
        if value is None or value == "":
            result.append(f"_c{index}")
        # Case-insensitive duplicate, append index
        elif not case_sensitive and value.lower() in duplicates:
            result.append(f"{value}{index}")
        # Case-sensitive duplicate, append index
        elif case_sensitive and value in duplicates:
            result.append(f"{value}{index}")
        else:
            result.append(value)

    return result


def get_header_names(
    session: snowpark.Session,
    path: list[str],
    file_format_options: dict,
    snowpark_read_options: dict,
    raw_options: dict,
    parse_header: bool,
) -> list[str]:
    no_header_file_format_options = copy.copy(file_format_options)
    no_header_file_format_options["PARSE_HEADER"] = False
    no_header_file_format_options.pop("SKIP_HEADER", None)

    file_format = cached_file_format(session, "csv", no_header_file_format_options)
    no_header_snowpark_read_options = copy.copy(snowpark_read_options)
    no_header_snowpark_read_options["FORMAT_NAME"] = file_format
    no_header_snowpark_read_options.pop("INFER_SCHEMA", None)

    # If we don't set this, snowpark will try to infer the schema for all rows in the csv file.
    # Since there's no easy way to just read the header from the csv, we use this approach where we force the df reader to infer the schema for 10 rows and
    # and we are only interested in the first row to get the header names and discard the inferred schema.
    no_header_snowpark_read_options["INFER_SCHEMA_OPTIONS"] = {
        "MAX_RECORDS_PER_FILE": 1,
    }

    header_df = session.read.options(no_header_snowpark_read_options).csv(path).limit(1)
    collected_data = header_df.collect()

    if len(collected_data) == 0:
        error_msg = f"Path does not exist or contains no data: {path}"
        user_pattern = raw_options.get("pathGlobFilter", None)
        if user_pattern:
            error_msg += f" (with pathGlobFilter: {user_pattern})"

        exception = AnalysisException(error_msg)
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    header_data = collected_data[0]
    num_columns = len(header_df.schema.fields)

    if not parse_header:
        # parse_header=False, use default _c0, _c1, _c2... naming for columns
        return [f'"_c{i}"' for i in range(num_columns)]

    # parse_header=True: Read first row as column names and deduplicate
    raw_column_names = [
        header_data[i] if header_data[i] is not None else "" for i in range(num_columns)
    ]

    case_sensitive = global_config.spark_sql_caseSensitive
    deduplicated_names = _deduplicate_column_names_pyspark_style(
        raw_column_names, case_sensitive
    )

    return [f'"{name}"' for name in deduplicated_names]


def _emulate_integral_types_for_csv(t: DataType) -> DataType:
    """
    CSV requires different type handling to match OSS Spark CSV schema inference.

    After applying emulate_integral_types, converts to Spark CSV types:
    - IntegerType, ShortType, ByteType -> IntegerType
    - LongType -> LongType
    - DecimalType with scale > 0 -> DoubleType
    - DecimalType with precision > 18 -> DecimalType (too big for long)
    - DecimalType with precision > 9 -> LongType
    - DecimalType with precision <= 9 -> IntegerType
    - FloatType, DoubleType -> DoubleType
    """
    if not _integral_types_conversion_enabled:
        return t

    # First apply standard integral type conversion
    t = emulate_integral_types(t)

    if isinstance(t, LongType):
        return LongType()

    elif isinstance(t, _IntegralType):
        # ByteType, ShortType, IntegerType -> IntegerType
        return IntegerType()

    elif isinstance(t, DecimalType):
        # DecimalType with scale > 0 means it has decimal places -> DoubleType
        if t.scale > 0:
            return DoubleType()
        # DecimalType with scale = 0 is integral
        if t.precision > 18:
            # Too big for long, keep as DecimalType
            return DecimalType(t.precision, 0)
        elif t.precision > 9:
            return LongType()
        else:
            return IntegerType()

    elif isinstance(t, _FractionalType):
        # FloatType, DoubleType -> DoubleType
        return DoubleType()

    return t


def _generate_stage_path_groups(paths: list[str]) -> list[tuple[str, list[str]]]:
    """
    Group paths by their stage.

    Args:
        paths: List of file paths (stage paths, cloud URLs, etc.)

    Returns:
        A list of tuples (stage, paths) where each tuple represents a group. Each group contains at most MAX_FILES_PER_COPY_INTO files.

    Example:
        Input: ["'@stage/file1.csv'", "'@stage/file2.csv'"]
        Output: [("'@stage'", ["'@stage/file1.csv'", "'@stage/file2.csv'"])]
    """
    # First, group paths by stage
    stage_path_dict: dict[str, list[str]] = {}
    for path in paths:
        stage = extract_stage_from_path(path)
        if stage not in stage_path_dict:
            stage_path_dict[stage] = []
        stage_path_dict[stage].append(path)

    result: list[tuple[str, list[str]]] = []

    for stage, stage_paths in stage_path_dict.items():
        for chunk in _split_into_chunks(stage_paths, MAX_FILES_PER_COPY_INTO):
            result.append((stage, chunk))

    return result


# Maximum number of files allowed in COPY INTO with FILES parameter
MAX_FILES_PER_COPY_INTO = 1000


def _split_into_chunks(items: list, chunk_size: int) -> list[list]:
    """
    Split a list into chunks of specified size.

    Args:
        items: The list to split.
        chunk_size: Maximum size of each chunk.

    Returns:
        A list of chunks, each with at most chunk_size items.
    """
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def _get_schema_for_copy_into(
    reader: DataFrameReader,
    session: snowpark.Session,
    schema: StructType | None,
    first_path: str,
    file_format_options: dict,
    snowpark_reader_options: dict,
    raw_options: dict,
    parse_header: bool,
) -> StructType:
    """
    Get schema for COPY INTO operation by reading the first file.

    This function determines the schema to use for COPY INTO:
    1. If user provided a schema, use it directly (no I/O needed)
    2. Otherwise, read the first file to infer the schema (handles headers, types, etc.)

    Args:
        reader: The DataFrameReader to use for reading.
        session: The Snowpark session.
        schema: User-provided schema, or None if not provided.
        first_path: The first file path to read.
        file_format_options: File format options for CSV.
        snowpark_reader_options: Snowpark reader options.
        raw_options: Raw options from the read request.
        parse_header: Whether to parse the header row.

    Returns:
        StructType schema to use for COPY INTO.
    """
    # Case 1: User provided schema - use it directly (cheapest, no I/O)
    if schema is not None:
        return schema

    # Case 2: Read the first file to infer the schema
    df, _ = _read_csv_with_partitions(
        session,
        reader,
        first_path,
        schema,
        snowpark_reader_options,
        file_format_options,
        raw_options,
        parse_header,
    )
    return df.schema


def _load_csv_with_copy_into(
    reader: DataFrameReader,
    target: str,
    paths: list[str],
    stage: str,
    schema: StructType,
    file_format_options: dict[str, Any],
) -> None:
    """
    Load multiple CSV files from the same stage using COPY INTO with FILES parameter for parallel execution.

    Args:
        reader: The DataFrameReader with configured options (including metadata settings).
        TODO: SNOW-3002469 copy_into_table does not enable INCLUDE_METADATA even though add_filename_metadata_to_reader
        has been called before.
        target: The name of the temporary table to load the data into.
        paths: List of full stage paths like ['@stage/file1.csv', '@stage/file2.csv'] to load.
        stage: The common stage name like '@stage_name'.
        schema: The StructType schema for the table.
        file_format_options: File format options for CSV.
    """
    # Extract just the file paths relative to the stage for the FILES parameter
    relative_files = [extract_relative_file_path(path, stage) for path in paths]

    logger.debug(
        f"Using COPY INTO for parallel CSV loading: {len(relative_files)} files from {stage}"
    )

    # Use Snowpark's copy_into_table API with the files parameter for parallel loading
    reader.schema(schema).csv(stage).copy_into_table(
        target,
        files=relative_files,
        format_type_options=file_format_options,
        force=True,
    )
