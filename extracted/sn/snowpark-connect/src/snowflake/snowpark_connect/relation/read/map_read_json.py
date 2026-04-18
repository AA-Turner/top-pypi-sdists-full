#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import concurrent.futures
import copy
import json
import os
import typing
import uuid
from contextlib import suppress
from datetime import datetime

import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark._internal.utils import (
    TempObjectType,
    is_in_stored_procedure,
    random_name_for_temp_object,
)
from snowflake.snowpark.row import Row
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    DateType,
    DecimalType,
    DoubleType,
    LongType,
    MapType,
    NullType,
    StringType,
    StructField,
    StructType,
    TimestampType,
    VariantType,
    _FractionalType,
    _IntegralType,
)
from snowflake.snowpark_connect.config import (
    get_string_session_config_param,
    global_config,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.date_time_format_mapping import (
    convert_java_datetime_format_for_fileformat,
    convert_java_datetime_format_to_python,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.map_read import JsonReaderConfig
from snowflake.snowpark_connect.relation.read.map_read_csv import _make_schema_nullable
from snowflake.snowpark_connect.relation.read.map_read_partitioned_file import (
    _discover_partition_columns,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    METADATA_FILENAME_COLUMN,
    add_filename_metadata_to_reader,
    populate_metadata,
)
from snowflake.snowpark_connect.relation.read.reader_config import (
    apply_drop_malformed_on_error,
)
from snowflake.snowpark_connect.relation.read.utils import (
    _load_file_with_copy_into,
    apply_metadata_exclusion_pattern,
    extract_relative_file_path,
    generate_stage_path_groups,
    get_spark_column_names_from_snowpark_columns,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.relation.stage_locator import (
    separate_stage_and_file_from_path,
)
from snowflake.snowpark_connect.type_mapping import (
    cast_to_match_snowpark_type,
    map_simple_types,
    map_type_to_snowflake_type,
    merge_different_types,
)
from snowflake.snowpark_connect.type_support import (
    _integral_types_conversion_enabled,
    emulate_integral_types,
)
from snowflake.snowpark_connect.utils.bz2_file_loader import (
    LINE_CONTENT,
    VALUE_COLUMN,
    load_bz2_file,
)
from snowflake.snowpark_connect.utils.io_utils import cached_file_format
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)


def _append_node_in_trace_stack(trace_stack: str, node: str) -> str:
    return f"{trace_stack}:{node}"


def _get_max_workers() -> int:
    is_running_in_stored_proc = is_in_stored_procedure()
    if is_running_in_stored_proc:
        # We are having issues in which the read is not giving correct number of rows
        # in storedprocs when the number of workers are more than 1
        # as a temporary fix we will make max_workers to 1
        max_workers = 1
    else:
        # We can have more workers than CPU count, this is an IO-intensive task
        max_workers = min(16, os.cpu_count() * 2)
    return max_workers


def _get_io_validations_mode() -> str:
    """Get the IO validations mode from session config.

    Returns:
        "strict" or "lenient" (default)
    """
    return (
        get_string_session_config_param("snowpark.connect.io.validations.mode")
        .strip()
        .lower()
        or "lenient"
    )


_json_file_format_allowed_options = {
    "COMPRESSION",
    "DATE_FORMAT",
    "TIMESTAMP_FORMAT",
    "FILE_EXTENSION",
    "STRIP_OUTER_ARRAY",
    "MULTI_LINE",
    "ENCODING",
    "NULL_IF",
}


# Tokens that exist in Snowflake format but not in Java SimpleDateFormat.
# If a format string contains any of these, it's likely already in Snowflake format.
_SNOWFLAKE_SPECIFIC_TOKENS = frozenset(
    {
        "HH24",
        "HH12",
        "MI",  # Snowflake minutes (Java uses mm)
        "FF",
        "FF1",
        "FF2",
        "FF3",
        "FF4",
        "FF5",
        "FF6",
        "FF7",
        "FF8",
        "FF9",
        "TZH",
        "TZM",
        "TZD",
        "MON",  # Snowflake abbreviated month (Java uses MMM)
        "DY",  # Snowflake day abbreviation (Java uses E/EE/EEE)
    }
)


def _is_likely_snowflake_format(format_value: str) -> bool:
    """Check if a format string appears to already be in Snowflake format.

    This helps avoid double-conversion when users pass Snowflake format strings
    instead of Java SimpleDateFormat strings.
    """
    upper_format = format_value.upper()
    return any(token in upper_format for token in _SNOWFLAKE_SPECIFIC_TOKENS)


def _try_convert_java_datetime_format(
    format_value: str,
    converter: typing.Callable[[str], str],
    format_type: str = "datetime",
) -> str:
    """Try to convert a Java datetime format string using the provided converter.

    If conversion fails or if the format appears to already be in Snowflake format,
    return the original format value.

    Args:
        format_value: The Java format string to convert
        converter: The conversion function to use
        format_type: Type of format for logging (e.g., "date", "timestamp")

    Returns:
        Converted format string, or original if conversion fails or not needed
    """
    # Skip conversion if the format already appears to be in Snowflake format
    if _is_likely_snowflake_format(format_value):
        return format_value

    try:
        return converter(format_value)
    except (ValueError, KeyError) as e:
        logger.warning(
            f"Failed to convert Java {format_type} format '{format_value}': {e}. "
            "Using original format."
        )
        return format_value


def _parse_json_snowpark_options(
    snowpark_options: dict[str, typing.Any]
) -> dict[str, typing.Any]:
    """
    Extract JSON file format options from Snowpark options.

    Args:
        snowpark_options: Dictionary of Snowpark options

    Returns:
        Dictionary of file format options that can be used with COPY INTO
    """
    file_format_options = dict()
    for key, value in snowpark_options.items():
        upper_key = key.upper()
        if upper_key in _json_file_format_allowed_options:
            # Convert Java/Spark date and timestamp format strings to Snowflake equivalents.
            # Spark uses Java SimpleDateFormat patterns (e.g. yyyyMMdd) while
            # Snowflake uses its own tokens (YYYYMMDD).
            # Skip conversion for "auto" - it's a special Snowflake keyword for auto-detection.
            if (
                upper_key in ("DATE_FORMAT", "TIMESTAMP_FORMAT")
                and value
                and str(value).lower() != "auto"
            ):
                value = _try_convert_java_datetime_format(
                    value,
                    convert_java_datetime_format_for_fileformat,
                    "date" if upper_key == "DATE_FORMAT" else "timestamp",
                )
            file_format_options[upper_key] = value

    return file_format_options


def _infer_json_schema_from_rows(
    df: snowpark.DataFrame,
    initial_schema: StructType,
    json_local_rows_to_infer_schema: int,
    drop_field_if_all_null: bool,
) -> StructType:
    """
    Infer JSON schema by iterating rows from a DataFrame.
    """
    inferred_schema = copy.deepcopy(initial_schema)
    columns_with_valid_contents = set()
    string_nodes_finalized = set[str]()

    schema_inference_df = (
        df
        if json_local_rows_to_infer_schema == -1
        else df.limit(json_local_rows_to_infer_schema)
    )
    for row in schema_inference_df.to_local_iterator():
        inferred_schema = merge_row_schema(
            inferred_schema,
            row,
            columns_with_valid_contents,
            string_nodes_finalized,
            drop_field_if_all_null,
        )

    # Any VariantType fields still remaining had null values in every sampled
    # row, so no concrete type could be determined.  Fall back to StringType
    # (matches PySpark behavior for permanently-null columns).
    for sf in inferred_schema.fields:
        if isinstance(sf.datatype, VariantType):
            sf.datatype = StringType()

    if drop_field_if_all_null:
        inferred_schema.fields = [
            sf
            for sf in inferred_schema.fields
            if unquote_if_quoted(sf.name) in columns_with_valid_contents
        ]

    return inferred_schema


def _convert_struct_type_to_variant(schema: StructType) -> StructType:
    """Replace nested complex types (StructType, ArrayType, MapType) with VariantType.

    COPY INTO requires exact struct field matching across all rows, but JSON data
    often has varying keys in nested objects (e.g., different vulnerability IDs per row).
    Loading nested fields as Variant avoids schema mismatch errors while still
    preserving the data for downstream typed construction.
    """
    simplified_fields = []
    for f in schema.fields:
        if isinstance(f.datatype, (StructType, ArrayType, MapType)):
            simplified_fields.append(StructField(f.name, VariantType(), f.nullable))
        else:
            simplified_fields.append(f)
    return StructType(simplified_fields)


def _deduplicate_fields_case_insensitive(schema: StructType) -> StructType:
    """Merge schema fields that differ only in case, matching PySpark behaviour.

    Snowflake's INFER_SCHEMA treats JSON keys case-sensitively, so scanning
    files with ``{"CITY": ...}`` and ``{"city": ...}`` produces *both* ``CITY``
    (unquoted/uppercase) and ``"city"`` (quoted/lowercase) as separate fields.

    PySpark (with the default ``spark.sql.caseSensitive=false``) merges such
    fields into a single lowercase column.  JSON value extraction, however,
    remains case-sensitive, so rows whose keys don't match the chosen casing
    yield NULLs — e.g. a row with ``"CITY"`` will show NULL under the ``city``
    column.  We replicate the same semantics here:

    1. Group fields by their lowercased name.
    2. If no case conflict exists, keep the original field untouched.
    3. On conflict, prefer the *lowercase* variant if present (quoted to
       prevent Snowpark's ``StructField`` from auto-uppercasing it).
       If no lowercase variant exists, keep the first field seen — this
       mirrors PySpark's non-deterministic "pick one" behaviour.
    """
    seen: dict[str, tuple[StructField, bool]] = {}
    for field in schema.fields:
        raw_name = unquote_if_quoted(field.name)
        key = raw_name.lower()
        if key not in seen:
            seen[key] = (field, False)
        elif raw_name == key:
            seen[key] = (field, True)
        else:
            seen[key] = (seen[key][0], True)
    result_fields = []
    for key, (field, had_conflict) in seen.items():
        if had_conflict:
            raw_winner = unquote_if_quoted(field.name)
            if raw_winner == key:
                quoted_key = f'"{key}"'
                result_fields.append(
                    StructField(quoted_key, field.datatype, field.nullable)
                )
            else:
                result_fields.append(field)
        else:
            result_fields.append(field)
    return StructType(result_fields)


def _get_schema_for_copy_into_json(
    session: snowpark.Session,
    schema: StructType | None,
    stage_name: str,
    stage_files: list[str],
    snowpark_options: dict,
    raw_options: dict,
    json_local_rows_to_infer_schema: int,
    drop_field_if_all_null: bool,
    relax_types_to_infer_schema: bool = False,
    infer_schema_all_files: bool = True,
) -> StructType:
    """
    Get merged schema for COPY INTO by scanning all files via INFER_SCHEMA.

    For multiple files, uses Snowpark's INFER_SCHEMA with the FILES option to
    discover columns across all files in a single call, matching PySpark's
    behavior of always merging JSON schemas.

    Args:
        session: The Snowpark session.
        schema: User-provided schema, or None if not provided.
        stage_name: Quoted stage name like "'@stage_name'".
        stage_files: List of quoted stage file paths.
        snowpark_options: Snowpark options for reading.
        raw_options: Raw options from the read request.
        json_local_rows_to_infer_schema: Number of rows to use for schema inference.
        drop_field_if_all_null: Whether to drop fields that are all null.
        relax_types_to_infer_schema: Whether to widen numeric types for overflow safety.
        infer_schema_all_files: If True, scan all files for schema. If False, read first file only.

    Returns:
        StructType schema covering all columns across all files.
    """
    if schema is not None:
        return schema

    if infer_schema_all_files and len(stage_files) > 1:
        # Compute the common directory prefix so reader.json() scopes its
        # scan to the right subdirectory instead of the bare stage root
        # (e.g. '@~/abc123/' instead of '@~').  This avoids picking up
        # unrelated files from other parallel tests on the session stage.
        clean_paths = [p.strip("'") for p in stage_files]
        common = os.path.commonprefix(clean_paths)
        # Truncate to the last '/' so we get a directory, not a partial filename
        dir_idx = common.rfind("/")
        if dir_idx >= 0:
            common = common[: dir_idx + 1]
        common_stage_prefix = f"'{common}'"

        relative_files = [
            extract_relative_file_path(path, common_stage_prefix)
            for path in stage_files
        ]
        infer_options = dict(snowpark_options)
        existing_infer_opts = infer_options.get("INFER_SCHEMA_OPTIONS", {})
        infer_options["INFER_SCHEMA_OPTIONS"] = {
            **existing_infer_opts,
            "FILES": relative_files,
        }
        reader = add_filename_metadata_to_reader(
            session.read.options(infer_options), raw_options
        )
        df = reader.json(common_stage_prefix)
    else:
        reader = add_filename_metadata_to_reader(
            session.read.options(snowpark_options), raw_options
        )
        df = reader.json(stage_files[0])

    # When sampling is active, the inferred SQL uses narrow types from the
    # sampled rows (e.g. NUMBER(2,0) from 10 rows).  Re-read with widened
    # types so _infer_json_schema_from_rows can scan beyond the sampled
    # range without overflowing narrow casts.
    if relax_types_to_infer_schema:
        relaxed_schema = relax_json_types(df.schema)
        normalized = StructType(
            [
                StructField(unquote_if_quoted(f.name), f.datatype, f.nullable)
                for f in relaxed_schema.fields
                if unquote_if_quoted(f.name) != METADATA_FILENAME_COLUMN
            ]
        )

        path = (
            common_stage_prefix
            if (infer_schema_all_files and len(stage_files) > 1)
            else stage_files[0]
        )
        df = reader.schema(normalized).json(path)

    inferred_schema = _infer_json_schema_from_rows(
        df=df,
        initial_schema=df.schema,
        json_local_rows_to_infer_schema=json_local_rows_to_infer_schema,
        drop_field_if_all_null=drop_field_if_all_null,
    )

    validated_schema, _ = validate_and_update_schema(inferred_schema)
    # Strip METADATA$FILENAME — it is a pseudo-column injected by
    # with_metadata() for schema inference, not an actual data field.
    validated_schema = StructType(
        [f for f in validated_schema.fields if f.name != METADATA_FILENAME_COLUMN]
    )
    if not global_config.spark_sql_caseSensitive:
        validated_schema = _deduplicate_fields_case_insensitive(validated_schema)
    return validated_schema


def map_read_json(
    rel: relation_proto.Relation,
    schema: StructType | None,
    session: snowpark.Session,
    paths: list[str],
    options: JsonReaderConfig,
) -> DataFrameContainer:
    """
    Read a JSON file into a Snowpark DataFrame.

    [JSON lines](http://jsonlines.org/) file format is supported.

    We leverage the stage that is already created in the map_read function that
    calls this.
    """
    # SPARK-35912: File sources like JSON can always contain NULL values,
    # so Spark automatically converts non-nullable user schemas to nullable.
    # This is controlled by snowpark.connect.io.validations.mode:
    # - "lenient" (default): preserve original nullable settings
    # - "strict": convert all fields to nullable (Spark behavior)
    io_validations_mode = _get_io_validations_mode()

    if schema is not None and io_validations_mode == "strict":
        schema = _make_schema_nullable(schema)

    if rel.read.is_streaming is True:
        # TODO: Structured streaming implementation.
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for JSON files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    else:
        snowpark_options = options.convert_to_snowpark_args()
        raw_options = rel.read.data_source.options
        snowpark_options["infer_schema"] = True

        json_local_rows_to_infer_schema = snowpark_options.pop(
            "jsonlocalrowstoinferschema", 1000
        )
        drop_field_if_all_null = snowpark_options.pop("dropfieldifallnull", False)
        snowpark_options.pop("processinbulk", None)
        snowpark_options.pop("batchsize", None)
        infer_schema_all_files = snowpark_options.pop("inferschemaallfiles", True)
        parallel_load_json_file = snowpark_options.pop("jsonfileparallelloading", False)
        file_encoding = snowpark_options.pop("encoding", "utf-8")
        compression = snowpark_options.get("compression", "auto")
        split_size_mb = snowpark_options.pop("splitsizemb", 2)
        mode = snowpark_options.pop("mode", "PERMISSIVE")
        if mode.upper() == "DROPMALFORMED" and getattr(
            session, "_enable_scos_feature", False
        ):
            apply_drop_malformed_on_error(snowpark_options)
        relax_types_to_infer_schema = (
            snowpark_options.pop("relaxtypestoinferschema", False)
            or _integral_types_conversion_enabled
        )
        apply_metadata_exclusion_pattern(snowpark_options)

        if len(paths) <= 0:
            exception = ValueError(f"No paths provided to read JSON files: {paths}")
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        result_can_be_cached = True
        if parallel_load_json_file and compression in (
            "auto",
            "AUTO",
            "none",
            "NONE",
            "bz2",
            "BZ2",
        ):
            # TODO: SNOW-3022765 Add read partitioned files support for reading bz2 file
            df = read_single_bz2_file(
                session,
                paths,
                split_size_mb,
                schema,
                json_local_rows_to_infer_schema,
                drop_field_if_all_null,
                mode,
                compression not in ("none", "NONE"),
                file_encoding,
                relax_types_to_infer_schema,
            )
        else:
            # Determine if COPY INTO will be used (to set can_be_cached flag)
            # COPY INTO is used when: no metadata requested and no partitions
            if len(paths) > 1 and not populate_metadata(raw_options):
                result_can_be_cached = False

            df = read_normal_json_files(
                session,
                paths,
                snowpark_options,
                raw_options,
                json_local_rows_to_infer_schema,
                drop_field_if_all_null,
                schema,
                relax_types_to_infer_schema,
                infer_schema_all_files,
                mode=mode,
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
                relax_json_types(f.datatype)
                if relax_types_to_infer_schema
                else f.datatype
                for f in df.schema.fields
            ],
            can_be_cached=result_can_be_cached,
        )


def read_single_bz2_file(
    session: snowpark.Session,
    paths: list[str],
    split_size_mb: int,
    schema: StructType | None,
    json_local_rows_to_infer_schema: int,
    drop_field_if_all_null: bool,
    mode: str,
    compressed: bool,
    file_encoding: str,
    relax_types_to_infer_schema: bool = False,
) -> snowpark.DataFrame:
    # Read the single bz2 file, not support metadata population for now
    stage_name, file_path = separate_stage_and_file_from_path(paths[0])
    df = load_bz2_file(
        session,
        stage_name,
        file_path,
        split_size_mb=split_size_mb,
        mode=mode,
        compressed=compressed,
        encoding=file_encoding,
    )
    if len(paths) > 1:
        for p in paths[1:]:
            stage_name, file_path = separate_stage_and_file_from_path(p)
            df = df.union_all(
                load_bz2_file(
                    session,
                    stage_name,
                    file_path,
                    split_size_mb=split_size_mb,
                    mode=mode,
                    compressed=compressed,
                    encoding=file_encoding,
                )
            )
    df = df.select(LINE_CONTENT)

    if schema is None:
        schema = StructType([StructField(LINE_CONTENT, StructType([]))])
        schema = _infer_json_schema_from_rows(
            df=df,
            initial_schema=schema,
            json_local_rows_to_infer_schema=json_local_rows_to_infer_schema,
            drop_field_if_all_null=drop_field_if_all_null,
        )

        real_schema = StructType([])
        for sf in schema.fields[0].datatype.fields:
            real_schema.add(sf)
        schema = real_schema

    schema, _ = validate_and_update_schema(schema)
    if relax_types_to_infer_schema:
        schema = relax_json_types(schema)

    return construct_dataframe_by_schema_bulk(
        schema,
        df,
        session,
        LINE_CONTENT,
    )


def _build_json_typed_transformations(
    schema: StructType,
    session: snowpark.Session,
    file_format_options: dict[str, typing.Any] | None = None,
) -> tuple[list[str], list["snowpark.Column"]]:
    """Build COPY INTO transformations that cast JSON fields to typed columns.

    Instead of loading as VARIANT and post-processing with INSERT INTO SELECT,
    this generates transformations applied directly during COPY INTO so that
    data lands in the target table with correct types in a single step.

    Args:
        schema: The target schema with fully typed fields (including nested
            StructType, ArrayType, MapType).
        session: The Snowpark session (used to check TRY_CAST PERMISSIVE support).
        file_format_options: Dictionary of file format options (DATE_FORMAT, TIMESTAMP_FORMAT).

    Returns:
        ``(target_columns, transformations)`` where *target_columns* is a list
        of quoted column names and *transformations* is a list of Snowpark
        Column objects with the appropriate casts.
    """
    from snowflake.snowpark.functions import sql_expr

    date_format = (
        file_format_options.get("DATE_FORMAT") if file_format_options else None
    )
    timestamp_format = (
        file_format_options.get("TIMESTAMP_FORMAT") if file_format_options else None
    )

    f_generate = (
        _generate_json_path_reference
        if session._has_structured_try_cast
        else _generate_json_path_reference_legacy
    )

    target_cols: list[str] = []
    transforms: list[snowpark.Column] = []

    for field in schema.fields:
        target_cols.append(field.name)
        cast_expr = f_generate(
            f"$1:{field.name}",
            field.datatype,
            date_format=date_format,
            timestamp_format=timestamp_format,
        )
        transforms.append(sql_expr(cast_expr).alias(field.name))

    return target_cols, transforms


def _spark_mode_to_on_error(mode: str) -> str | None:
    """Map Spark JSON read mode to Snowflake COPY INTO ON_ERROR value.

    Spark modes:
    - PERMISSIVE (default): use Snowflake default (no explicit ON_ERROR)
    - DROPMALFORMED: continue on errors, filter out all-NULL rows afterward
    - FAILFAST: abort on first error

    # TODO: SNOW-3293434 enable copy on error permissive mode
    """
    upper = mode.upper()
    if upper == "FAILFAST":
        return "ABORT_STATEMENT"
    if upper == "DROPMALFORMED":
        return "CONTINUE"
    return None


def read_normal_json_files(
    session: snowpark.Session,
    paths: list[str],
    snowpark_options: dict,
    raw_options: dict,
    json_local_rows_to_infer_schema: int,
    drop_field_if_all_null: bool,
    schema: StructType | None,
    relax_types_to_infer_schema: bool,
    infer_schema_all_files: bool = True,
    mode: str = "PERMISSIVE",
) -> snowpark.DataFrame:
    # Read the normal JSON files, support metadata population

    needs_metadata = populate_metadata(raw_options)

    file_format_options = _parse_json_snowpark_options(snowpark_options)
    # Keep reader-level options separate from file format options.
    # ENFORCE_EXISTING_FILE_FORMAT cannot be used together with format type options.
    reader_options = {
        key: value
        for key, value in snowpark_options.items()
        if key.upper() not in _json_file_format_allowed_options
    }
    if "FORMAT_NAME" not in reader_options:
        reader_options["FORMAT_NAME"] = cached_file_format(
            session, "json", file_format_options
        )
    reader_options["ENFORCE_EXISTING_FILE_FORMAT"] = True
    apply_metadata_exclusion_pattern(reader_options)

    reader = add_filename_metadata_to_reader(
        session.read.options(reader_options), raw_options
    )

    # Probe for Hive-style partition directories (lightweight LS on first path).
    partition_columns, partition_types = _discover_partition_columns(
        session, paths[0], "json"
    )

    logger.debug(
        f"Using COPY INTO for {len(paths)} JSON file(s)"
        f"{' with partition transforms' if partition_columns else ''}"
        f"{' with metadata' if needs_metadata else ''}."
    )
    temp_table_name = random_name_for_temp_object(TempObjectType.TABLE)
    stage_file_groups = generate_stage_path_groups(paths)
    for stage_name, stage_files in stage_file_groups:
        copy_into_schema = _get_schema_for_copy_into_json(
            session=session,
            schema=schema,
            stage_name=stage_name,
            stage_files=stage_files,
            snowpark_options=reader_options,
            raw_options=raw_options,
            json_local_rows_to_infer_schema=json_local_rows_to_infer_schema,
            drop_field_if_all_null=drop_field_if_all_null,
            relax_types_to_infer_schema=relax_types_to_infer_schema,
            infer_schema_all_files=infer_schema_all_files,
        )
        if len(stage_files) == 1:
            stage_file_paths = []
            copy_from_stage = stage_files[0]
        else:
            stage_file_paths = stage_files
            copy_from_stage = stage_name

        final_schema, _ = validate_and_update_schema(copy_into_schema)
        if relax_types_to_infer_schema:
            final_schema = relax_json_types(final_schema)

        target_cols, typed_transforms = _build_json_typed_transformations(
            final_schema, session, file_format_options
        )

        on_error = _spark_mode_to_on_error(mode)
        _load_file_with_copy_into(
            reader=reader,
            session=session,
            target=temp_table_name,
            stage_file_paths=stage_file_paths,
            stage=copy_from_stage,
            schema=final_schema,
            file_format_options=file_format_options,
            file_format="json",
            on_error=on_error,
            partition_columns=partition_columns if partition_columns else None,
            partition_types=partition_types if partition_columns else None,
            needs_metadata=needs_metadata,
            target_columns=target_cols,
            transformations=typed_transforms,
        )

    return session.table(temp_table_name)


def should_drop_field(field: StructField) -> bool:
    if isinstance(field.datatype, StructType):
        # "a" : {} => drop the field
        if len(field.datatype.fields) == 0:
            return True
    elif (
        isinstance(field.datatype, ArrayType)
        and field.datatype.element_type is not None
        and isinstance(field.datatype.element_type, StructType)
    ):
        if len(field.datatype.element_type.fields) == 0:
            # "a" : [{}] => drop the field
            return True
    return False


# Validate the schema to ensure it is valid for Snowflake
# Handles these cases:
#   1. Drops StructField([])
#   2. Drops ArrayType(StructType([]))
#   3. ArrayType() -> ArrayType(StringType())
#   4. NullType -> StringType (Snowflake cannot represent NullType in typed tables)
def validate_and_update_schema(schema: StructType | None) -> (StructType | None, bool):
    if not isinstance(schema, StructType):
        return schema, False
    new_fields = []
    fields_changed = False
    for sf in schema.fields:
        if should_drop_field(sf):
            fields_changed = True
            continue
        if isinstance(sf.datatype, NullType):
            sf = StructField(sf.name, StringType(), sf.nullable)
            fields_changed = True
            new_fields.append(sf)
        elif isinstance(sf.datatype, StructType):
            # If the schema is a struct, validate the child schema
            if len(sf.datatype.fields) == 0:
                # No fields in the struct, drop the field
                fields_changed = True
                continue
            child_field = StructField(sf.name, sf.datatype, sf.nullable)
            # Recursively validate the child schema
            child_field.datatype, child_field_changes = validate_and_update_schema(
                sf.datatype
            )
            if should_drop_field(child_field):
                fields_changed = True
                continue
            new_fields.append(child_field)
            fields_changed = fields_changed or child_field_changes
        elif isinstance(sf.datatype, ArrayType):
            # If the schema is an array, validate the element schema
            if sf.datatype.element_type is not None and isinstance(
                sf.datatype.element_type, StructType
            ):
                # If the element schema is a struct, validate the element schema
                if len(sf.datatype.element_type.fields) == 0:
                    # No fields in the struct, drop the field
                    fields_changed = True
                    continue
                else:
                    # Recursively validate the element schema
                    element_schema, element_field_changes = validate_and_update_schema(
                        sf.datatype.element_type
                    )
                    if element_field_changes:
                        sf.datatype.element_type = element_schema
                        fields_changed = True
                    if should_drop_field(sf):
                        fields_changed = True
                        continue
            elif sf.datatype.element_type is None:
                fields_changed = True
                sf.datatype.element_type = StringType()
            new_fields.append(sf)
        else:
            new_fields.append(sf)
    if fields_changed:
        schema.fields = new_fields
    return schema, fields_changed


def merge_json_schema(
    content: typing.Any,
    schema: StructType | None,
    trace_stack: str,
    string_nodes_finalized: set[str],
    drop_field_if_all_null: bool = False,
) -> DataType:
    """
    Merge the JSON content's schema into an existing schema structure.

    This function recursively processes JSON content (dict, list, or primitive values) and merges
    its inferred schema with an existing schema if provided. It handles nested structures like
    objects (StructType) and arrays (ArrayType), and can optionally drop fields that are always null.

    Args:
        content: The JSON content to infer schema from. Can be a dict, list, primitive value, or None.
        schema: The existing schema to merge with, or None if inferring from scratch.
        trace_stack: A string representing the current position in the schema hierarchy,
                          used for tracking/debugging nested structures.
        string_nodes_finalized: A set of strings representing the nodes that have been finalized as strings.
        drop_field_if_all_null: If True, fields that only contain null values will be excluded
                          from the resulting schema. Defaults to False.

    Returns:
        The merged schema as a DataType. Returns NullType if content is None and no existing
        schema is provided. For dicts, returns StructType; for lists, returns ArrayType;
        for primitives, returns the appropriate primitive type (StringType, IntegerType, etc.).
    """
    if content is None:
        if schema is not None:
            return schema
        return NullType()

    if trace_stack in string_nodes_finalized:
        return StringType()

    if isinstance(content, dict):
        additional_schemas = list[StructField]()

        existed_schema = {}
        if schema is not None and not isinstance(schema, NullType):
            if schema.type_name() == "struct":
                for sf in schema.fields:
                    existed_schema[sf.name] = sf.datatype
            else:
                string_nodes_finalized.add(trace_stack)
                return StringType()

        for k, v in content.items():
            col_name = f'"{unquote_if_quoted(k)}"'
            existed_data_type = existed_schema.get(col_name, None)
            next_level_schema = merge_json_schema(
                v,
                existed_data_type,
                _append_node_in_trace_stack(trace_stack, col_name),
                string_nodes_finalized,
                drop_field_if_all_null,
            )

            if not drop_field_if_all_null or not isinstance(
                next_level_schema, NullType
            ):
                # Drop field if it's always null
                if col_name in existed_schema:
                    existed_schema[col_name] = next_level_schema
                else:
                    additional_schemas.append(StructField(col_name, next_level_schema))

        current_schema = StructType()
        if schema is not None and schema.type_name() == "struct":
            # Keep the order of columns in the schema
            for sf in schema.fields:
                col_name = f'"{unquote_if_quoted(sf.name)}"'
                if (
                    not drop_field_if_all_null
                    or existed_schema.get(col_name, NullType()) != NullType()
                ):
                    current_schema.add(
                        StructField(col_name, existed_schema.get(col_name, NullType()))
                    )

        for additional_schema in additional_schemas:
            current_schema.add(additional_schema)

    elif isinstance(content, list):
        # ArrayType(*) need to have element schema inside, it would be NullType() as placeholder and keep updating while enumerating
        inner_schema = NullType()
        next_level_trace_stack = _append_node_in_trace_stack(trace_stack, "$array")

        if schema is not None:
            if schema.type_name() in ("list", "array"):
                inner_schema = schema.element_type
            else:
                string_nodes_finalized.add(trace_stack)
                return StringType()

        if next_level_trace_stack in string_nodes_finalized:
            inner_schema = StringType()
        else:
            if len(content) > 0:
                for v in content:
                    inner_schema = merge_json_schema(
                        v,
                        inner_schema,
                        next_level_trace_stack,
                        string_nodes_finalized,
                        drop_field_if_all_null,
                    )
                    if isinstance(inner_schema, StringType):
                        string_nodes_finalized.add(next_level_trace_stack)
                        break
            if isinstance(inner_schema, NullType) and drop_field_if_all_null:
                return NullType()
        current_schema = ArrayType(inner_schema)
    else:
        current_schema = map_simple_types(type(content).__name__)

    if (
        schema is not None
        and schema != NullType()
        and current_schema is not None
        and current_schema != NullType()
        and schema.type_name() != current_schema.type_name()
    ):
        # SNOW-3245123/SNOW-3245124: Preserve ArrayType/StructType/MapType when
        # encountering empty content (empty list [], empty dict {}, empty string,
        # or whitespace). Non-empty content proceeds with normal type inference.
        if isinstance(schema, (ArrayType, StructType, MapType)) and (
            (isinstance(content, list) and not content)
            or (isinstance(content, dict) and not content)
            or (isinstance(content, str) and not content.strip())
        ):
            current_schema = schema  # Preserve existing complex type for empty content
        else:
            current_schema = merge_different_types(schema, current_schema)

    if isinstance(current_schema, StructType) or isinstance(current_schema, ArrayType):
        current_schema.structured = True

    if isinstance(current_schema, StringType):
        string_nodes_finalized.add(trace_stack)
    return current_schema


def merge_row_schema(
    schema: StructType | None,
    row: Row,
    columns_with_valid_contents: set[str],
    string_nodes_finalized: set[str],
    drop_field_if_all_null: bool = False,
) -> StructType | NullType:
    """
    Merge the schema inferred from a single row with the existing schema.

    This function updates the schema by examining each row of data and merging
    type information. It handles nested structures (StructType, MapType, ArrayType)
    and attempts to parse JSON strings to infer deeper schema structures.

    Args:
        schema: The current schema to merge with
        row: A single row of data to examine
        columns_with_valid_contents: Set to track columns that have non-null values
        string_nodes_finalized: Set to track nodes that have been finalized as strings
        drop_field_if_all_null: If True, fields that are always null will be dropped

    Returns:
        The merged schema as a StructType, or NullType if the row is None and no schema exists
    """

    if row is None:
        if schema is not None:
            return schema
        return NullType()

    new_schema = StructType()
    for sf in schema.fields:
        col_name = unquote_if_quoted(sf.name)
        if col_name in string_nodes_finalized:
            columns_with_valid_contents.add(col_name)
        elif isinstance(sf.datatype, (StructType, MapType, StringType)):
            next_level_content = row[col_name]
            next_level_trace_stack = _append_node_in_trace_stack(col_name, col_name)
            if next_level_content is not None:
                with suppress(json.JSONDecodeError):
                    if isinstance(next_level_content, datetime):
                        next_level_content = str(next_level_content)
                    next_level_content = json.loads(next_level_content)
                # SNOW-3245124: Preserve existing StructType/MapType when
                # encountering empty content (empty dict {}, None, empty string,
                # or whitespace). Non-empty content proceeds with normal type inference.
                if isinstance(sf.datatype, (StructType, MapType)) and (
                    (isinstance(next_level_content, dict) and not next_level_content)
                    or next_level_content is None
                    or (
                        isinstance(next_level_content, str)
                        and not next_level_content.strip()
                    )
                ):
                    pass  # Preserve existing structured type for empty content
                elif isinstance(next_level_content, dict):
                    sf.datatype = merge_json_schema(
                        next_level_content,
                        None
                        if not isinstance(sf.datatype, StructType)
                        else sf.datatype,
                        next_level_trace_stack,
                        string_nodes_finalized,
                        drop_field_if_all_null,
                    )
                else:
                    sf.datatype = StringType()
                    string_nodes_finalized.add(col_name)
                columns_with_valid_contents.add(col_name)

        elif isinstance(sf.datatype, VariantType):
            # VariantType columns (from COPY INTO with simplified schema) hold raw
            # JSON strings that can be objects, arrays, or primitives.  Determine
            # the actual type from the data so subsequent rows use the proper branch.
            next_level_content = row[col_name]
            if next_level_content is not None:
                with suppress(json.JSONDecodeError):
                    next_level_content = json.loads(next_level_content)
                # Snowflake Variant columns represent JSON null as the string
                # 'null', which json.loads parses to Python None.  Treat this
                # the same as a true null: skip the row and keep VariantType
                # so a later row with real data can determine the correct type.
                if next_level_content is None:
                    pass
                elif isinstance(next_level_content, dict):
                    trace = _append_node_in_trace_stack(col_name, col_name)
                    sf.datatype = merge_json_schema(
                        next_level_content,
                        None,
                        trace,
                        string_nodes_finalized,
                        drop_field_if_all_null,
                    )
                    columns_with_valid_contents.add(col_name)
                elif isinstance(next_level_content, list):
                    trace = _append_node_in_trace_stack(col_name, "array")
                    inner_schema = None
                    for v in next_level_content:
                        if v is not None:
                            columns_with_valid_contents.add(col_name)
                        inner_schema = merge_json_schema(
                            v,
                            inner_schema,
                            trace,
                            string_nodes_finalized,
                            drop_field_if_all_null,
                        )
                        if isinstance(inner_schema, StringType):
                            string_nodes_finalized.add(trace)
                            break
                    sf.datatype = ArrayType(
                        inner_schema if inner_schema else StringType()
                    )
                    columns_with_valid_contents.add(col_name)
                else:
                    sf.datatype = StringType()
                    string_nodes_finalized.add(col_name)
                    columns_with_valid_contents.add(col_name)

        elif isinstance(sf.datatype, ArrayType):
            content = row[col_name]
            if content is not None:
                with suppress(Exception):
                    decoded_content = json.loads(content)
                    if isinstance(decoded_content, list):
                        content = decoded_content
                # SNOW-3245123: Preserve ArrayType when encountering empty content
                # (empty list [], empty string, whitespace). Non-empty non-list
                # content converts to StringType.
                if isinstance(sf.datatype, ArrayType) and (
                    (isinstance(content, list) and not content)
                    or (isinstance(content, str) and not content.strip())
                ):
                    pass  # Preserve existing ArrayType for empty content
                elif (
                    not isinstance(content, list) or col_name in string_nodes_finalized
                ):
                    sf.datatype = StringType()
                    string_nodes_finalized.add(col_name)
                else:
                    next_level_trace_stack = _append_node_in_trace_stack(
                        col_name, "array"
                    )
                    if next_level_trace_stack in string_nodes_finalized:
                        sf.datatype.element_type = StringType()
                    else:
                        inner_schema = sf.datatype.element_type
                        for v in content:
                            if v is not None:
                                columns_with_valid_contents.add(col_name)
                            inner_schema = merge_json_schema(
                                v,
                                inner_schema,
                                next_level_trace_stack,
                                string_nodes_finalized,
                                drop_field_if_all_null,
                            )
                            if isinstance(inner_schema, StringType):
                                string_nodes_finalized.add(next_level_trace_stack)
                                break
                        sf.datatype.element_type = inner_schema
        elif isinstance(sf.datatype, TimestampType):
            sf.datatype = StringType()
            columns_with_valid_contents.add(col_name)
            string_nodes_finalized.add(col_name)
        elif row[col_name] is not None:
            columns_with_valid_contents.add(col_name)

        if isinstance(sf.datatype, StructType) or isinstance(sf.datatype, ArrayType):
            sf.datatype.structured = True
        new_schema.add(sf)

    return new_schema


def insert_data_chunk(
    session: snowpark.Session,
    data: list[Row],
    schema: StructType,
    table_name: str,
) -> None:
    df = session.create_dataframe(
        data=data,
        schema=schema,
    )

    df.write.mode("append").save_as_table(
        table_name, table_type="temp", table_exists=True
    )


def _is_empty_struct(schema: StructType) -> bool:
    """This schema is essentially matching everything under the root and treating it as a single VARIANT column"""
    return isinstance(schema, StructType) and (
        schema.fields is None or len(schema.fields) == 0
    )


def construct_dataframe_by_schema_bulk(
    schema: StructType,
    df_source: snowpark.DataFrame,
    session: snowpark.Session,
    root_column_name: str = None,
) -> snowpark.DataFrame:
    """
    Bulk process JSON data.
    """
    if _is_empty_struct(schema):
        # We are gathering the whole row in a single, all encompassing column,
        root_column_name = None
        # of type Variant with no schema enforced
        schema = StructType([StructField(VALUE_COLUMN, VariantType())])
        df_source = df_source.withColumnRenamed(LINE_CONTENT, VALUE_COLUMN)

    # Step 1: Create temporary view from source DataFrame
    source_view = f"__sas_json_source_view_{uuid.uuid4().hex}"
    df_source.create_or_replace_temp_view(source_view)

    # When root_column_name is None, field references are direct column
    # identifiers on the source view.  If the user-provided schema contains
    # fields that don't exist in the JSON data (PERMISSIVE mode), referencing
    # them would cause "invalid identifier".  Collect existing column names so
    # we can emit NULL for missing fields instead.
    source_column_names: set[str] | None = None
    if root_column_name is None:
        source_column_names = {unquote_if_quoted(c) for c in df_source.columns}

    # Step 2: Create target table with correct schema
    target_table = f"__sas_json_target_{uuid.uuid4().hex}"

    create_ddl = _generate_create_table_ddl(target_table, schema)
    session.sql(create_ddl).collect()

    # Step 3: Generate SELECT with CAST expressions
    select_exprs = []
    use_structured_try_cast = session._has_structured_try_cast
    f_generate_json_path_reference = (
        _generate_json_path_reference
        if use_structured_try_cast
        else _generate_json_path_reference_legacy
    )
    for field in schema.fields:
        # Use _generate_json_path_reference to handle NULL values for missing/empty fields
        if root_column_name is not None:
            json_path_expr = f_generate_json_path_reference(
                f"{root_column_name}:{field.name}", field.datatype
            )
        else:
            # PERMISSIVE mode: if the source view lacks this column, emit
            # NULL instead of referencing the non-existent identifier.
            field_name_unquoted = unquote_if_quoted(field.name)
            if (
                source_column_names is not None
                and field_name_unquoted not in source_column_names
            ):
                select_exprs.append(f"NULL AS {field.name}")
                continue
            json_path_expr = f_generate_json_path_reference(
                field.name, field.datatype, is_root=True
            )
        # TODO(SNOW-3122222): Remove the legacy `else` branch once 10.6 is fully rolled out
        if use_structured_try_cast:
            select_exprs.append(f"{json_path_expr} AS {field.name}")
        else:
            # Generate Snowflake type signature for casting
            sf_type_sig = _generate_snowflake_type_signature(field.datatype)
            if isinstance(field.datatype, StringType):
                select_exprs.append(f"TO_VARCHAR({json_path_expr}) AS {field.name}")
            elif not isinstance(field.datatype, (StructType, ArrayType, MapType)):
                select_exprs.append(
                    f"TRY_CAST(TO_VARCHAR({json_path_expr}) AS {sf_type_sig}) AS {field.name}"
                )
            else:
                select_exprs.append(f"{json_path_expr}::{sf_type_sig} AS {field.name}")

    # Step 4: Apply select expression and copy into target table
    sql_query = f"""
        INSERT INTO {target_table}
        (
            SELECT {', '.join(select_exprs)}
            FROM {source_view}
        )
    """

    session.sql(sql_query).collect()

    return session.table(target_table)


def _generate_create_table_ddl(table_name: str, schema: StructType) -> str:
    """
    Generate CREATE TABLE DDL with typed columns for bulk JSON processing.

    Example output:
      CREATE TEMP TABLE my_table (
        "id" INT,
        "metadata" OBJECT(field1 INT, field2 VARCHAR),
        "items" ARRAY(INT)
      )
    """
    columns_ddl = []
    for field in schema.fields:
        col_type_sig = _generate_snowflake_type_signature(field.datatype)
        columns_ddl.append(f"{field.name} {col_type_sig}")

    return f"CREATE TEMP TABLE {table_name} ({', '.join(columns_ddl)})"


def _generate_snowflake_type_signature(data_type: DataType) -> str:
    """
    Generate Snowflake type signature for structured type casting.

    Delegates to ``map_type_to_snowflake_type(structured=True)`` for most
    types.  Adds special handling for integral types that need explicit
    precision (e.g. NUMBER(19,0) for Scala/Java client round-trips).

    Examples:
      IntegerType() → "INT"
      StructType([...]) → "OBJECT(field1 INT, field2 VARCHAR, ...)"
      ArrayType(IntegerType()) → "ARRAY(INT)"
    """
    if isinstance(data_type, _IntegralType):
        precision = getattr(data_type, "_precision", None)
        if precision is not None:
            return f"NUMBER({precision},0)"
        # For Scala/Java clients, use NUMBER(19,0) so that on readback
        # column_name_handler's emulate_integral_types sees precision=19
        # and maps to LongType rather than DecimalType(38,0).
        if _integral_types_conversion_enabled:
            return "NUMBER(19,0)"
    return map_type_to_snowflake_type(data_type, structured=True)


def _generate_json_path_reference(
    json_path: str,
    data_type: DataType,
    is_root: bool = False,
    date_format: str | None = None,
    timestamp_format: str | None = None,
) -> str:
    """
    Generate a JSON path reference with appropriate casting for nested fields.

    This function performs permissive casting on structured types (STRUCT, ARRAY, MAP).

    TRY_CAST returns NULL on errors that prevent parsing the entire structure.

    Examples:
        Simple field: "field_name:a.b.field"
        Integer field: "field_name:a.b.field::INT"
        Array field: "TRY_CAST(field_name:a.b.tags AS ARRAY(TEXT) PERMISSIVE)"
        Map field: "TRY_CAST(field_name:a.b.metadata AS MAP(TEXT, TEXT) PERMISSIVE)"
        Nested struct: "TRY_CAST(field_name:a.b.field1 AS OBJECT(<type information here>))"

    Args:
        json_path: The JSON path to the field (e.g., "field_name:a.b.field")
        data_type: The DataType of the field
        is_root: Whether this is a root-level field
        date_format: Optional Snowflake date format string (e.g., "YYYYMMDD")
        timestamp_format: Optional Snowflake timestamp format string
    """
    if isinstance(data_type, (StructType, ArrayType, MapType)):
        return f"TRY_CAST({json_path} AS {_generate_snowflake_type_signature(data_type)} PERMISSIVE)"
    elif isinstance(data_type, StringType):
        return f"TO_VARCHAR({json_path})"
    elif isinstance(data_type, DateType) and date_format and date_format != "auto":
        # Use TRY_TO_DATE with explicit format for custom date formats
        return f"TRY_TO_DATE(TO_VARCHAR({json_path}), '{date_format}')"
    elif (
        isinstance(data_type, TimestampType)
        and timestamp_format
        and timestamp_format != "auto"
    ):
        # Use TRY_TO_TIMESTAMP with explicit format for custom timestamp formats
        return f"TRY_TO_TIMESTAMP(TO_VARCHAR({json_path}), '{timestamp_format}')"
    else:
        return (
            json_path
            if is_root
            else f"TRY_CAST(TO_VARCHAR({json_path}) AS {_generate_snowflake_type_signature(data_type)})"
        )


def _generate_json_path_reference_legacy(
    json_path: str,
    data_type: DataType,
    is_root: bool = False,
    date_format: str | None = None,
    timestamp_format: str | None = None,
) -> str:
    """
    Generate a JSON path reference with appropriate casting for nested fields.

    This is a legacy function necessary to support casting recursive fields of a parsed values
    prior to the availability of TRY_CAST(... PERMISSIVE) on the server side.
    TODO(SNOW-3122222): This function should be removed once the rollout of 10.6 is fully confirmed.

    This function recursively builds OBJECT_CONSTRUCT_KEEP_NULL expressions for
    nested structures, with proper casting for arrays and maps.

    Examples:
        Simple field: "field_name:a.b.field"
        Integer field: "field_name:a.b.field::INT"
        Array field: "field_name:a.b.tags::ARRAY(TEXT)"
        Map field: "field_name:a.b.metadata::MAP(TEXT, TEXT)"
        Nested struct: "OBJECT_CONSTRUCT_KEEP_NULL('field1', field_name:a.b.field1, ...)"

    Args:
        json_path: The JSON path to the field (e.g., "field_name:a.b.field")
        data_type: The DataType of the field
        is_root: Whether this is a root-level field
        date_format: Optional Snowflake date format string (not used in legacy)
        timestamp_format: Optional Snowflake timestamp format string (not used in legacy)
    """

    variant_suffix = "::VARIANT" if not is_root else ""
    if isinstance(data_type, StructType):
        # Build OBJECT_CONSTRUCT_KEEP_NULL for nested structures
        field_exprs = []
        for field in data_type.fields:
            field_name = unquote_if_quoted(field.name)
            nested_col_name = json_path + (":" if is_root else ".") + field.name
            nested_expr = _generate_json_path_reference_legacy(
                nested_col_name, field.datatype
            )
            field_exprs.append(f"'{field_name}', {nested_expr}")

        return f"OBJECT_CONSTRUCT_KEEP_NULL({', '.join(field_exprs)}){variant_suffix}"

    elif isinstance(data_type, ArrayType):
        # Cast to typed array
        element_type_sig = _generate_snowflake_type_signature(data_type.element_type)
        return f"{json_path}::ARRAY({element_type_sig}){variant_suffix}"

    elif isinstance(data_type, MapType):
        # Cast to typed map
        key_type_sig = _generate_snowflake_type_signature(data_type.key_type)
        value_type_sig = _generate_snowflake_type_signature(data_type.value_type)
        return f"{json_path}::MAP({key_type_sig}, {value_type_sig}){variant_suffix}"

    elif isinstance(data_type, StringType):
        return f"TO_VARCHAR({json_path})"

    elif isinstance(data_type, DateType) and date_format and date_format != "auto":
        # Use TRY_TO_DATE with explicit format for custom date formats
        return f"TRY_TO_DATE(TO_VARCHAR({json_path}), '{date_format}')"

    elif (
        isinstance(data_type, TimestampType)
        and timestamp_format
        and timestamp_format != "auto"
    ):
        # Use TRY_TO_TIMESTAMP with explicit format for custom timestamp formats
        return f"TRY_TO_TIMESTAMP(TO_VARCHAR({json_path}), '{timestamp_format}')"

    else:
        return (
            json_path
            if is_root
            else f"TRY_CAST(TO_VARCHAR({json_path}) AS {_generate_snowflake_type_signature(data_type)})"
        )


def construct_dataframe_by_schema(
    schema: StructType,
    rows: typing.Iterator[Row],
    session: snowpark.Session,
    snowpark_options: dict,
    batch_size: int = 1000,
) -> snowpark.DataFrame:
    table_name = "__sas_json_read_temp_" + uuid.uuid4().hex

    current_data = []
    progress = 0

    # Initialize the temp table
    session.create_dataframe([], schema=schema).write.mode("append").save_as_table(
        table_name, table_type="temp", table_exists=False
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=_get_max_workers()) as exc:
        for row in rows:
            current_data.append(construct_row_by_schema(row, schema, snowpark_options))
            if len(current_data) >= batch_size:
                progress += len(current_data)
                exc.submit(
                    insert_data_chunk,
                    session,
                    copy.deepcopy(current_data),
                    schema,
                    table_name,
                )

                logger.info(f"JSON reader: finished processing {progress} rows")
                current_data.clear()

        if len(current_data) > 0:
            progress += len(current_data)
            exc.submit(
                insert_data_chunk,
                session,
                copy.deepcopy(current_data),
                schema,
                table_name,
            )
            logger.info(f"JSON reader: finished processing {progress} rows")

    return session.table(table_name)


def construct_row_by_schema(
    content: typing.Any, schema: DataType, snowpark_options: dict
) -> None | DataType:
    if content is None:
        return None
    elif isinstance(schema, StructType):
        result = {}
        if isinstance(content, (dict, Row)):
            for sf in schema.fields:
                col_name = unquote_if_quoted(sf.name)
                quoted_col_name = (
                    f'"{col_name}"' if isinstance(content, Row) else col_name
                )
                result[quoted_col_name] = construct_row_by_schema(
                    (content.as_dict() if isinstance(content, Row) else content).get(
                        col_name, None
                    ),
                    sf.datatype,
                    snowpark_options,
                )
        elif isinstance(content, str):
            with suppress(json.JSONDecodeError):
                decoded_content = json.loads(content)
                # JSON null ('null' string) → treat as null struct
                if decoded_content is None:
                    return None
                if isinstance(decoded_content, dict):
                    content = decoded_content
            for sf in schema.fields:
                col_name = unquote_if_quoted(sf.name)
                result[col_name] = construct_row_by_schema(
                    content.get(col_name, None), sf.datatype, snowpark_options
                )
        else:
            exception = SnowparkConnectNotImplementedError(
                f"JSON construct {str(content)} to StructType failed"
            )
            attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
            raise exception
        return result
    elif isinstance(schema, ArrayType):
        result = []
        inner_schema = schema.element_type
        if isinstance(content, str):
            content = json.loads(content)
        if content is None:
            return None
        if inner_schema is not None:
            for ele in content:
                result.append(
                    construct_row_by_schema(ele, inner_schema, snowpark_options)
                )
        return result
    elif isinstance(schema, DateType):
        # Convert Java date format to Python strptime format for local processing
        date_format = snowpark_options.get("DATE_FORMAT")
        if date_format and date_format != "auto":
            date_format = _try_convert_java_datetime_format(
                date_format, convert_java_datetime_format_to_python, "date"
            )
        return cast_to_match_snowpark_type(schema, content, date_format)

    return cast_to_match_snowpark_type(schema, content)


def relax_json_types(t: DataType) -> DataType:
    """Widen numeric types to match OSS Spark's JSON schema inference rules.

    Recursively applies to nested types (ArrayType, StructType, MapType):
    - All integral types (ByteType, ShortType, IntegerType, LongType) -> LongType
    - DecimalType with scale > 0 -> DoubleType
    - DecimalType with scale = 0 -> LongType (if precision <= 18) or DecimalType
    - FloatType, DoubleType -> DoubleType
    """
    if isinstance(t, StructType):
        for sf in t.fields:
            sf.datatype = relax_json_types(sf.datatype)
        return t
    elif isinstance(t, ArrayType):
        if t.element_type is not None:
            t.element_type = relax_json_types(t.element_type)
        return t
    elif isinstance(t, MapType):
        t.key_type = relax_json_types(t.key_type)
        t.value_type = relax_json_types(t.value_type)
        return t

    # First apply standard integral type conversion
    t = emulate_integral_types(t)

    if isinstance(t, _IntegralType):
        # All integral types -> LongType for JSON
        return LongType()
    elif isinstance(t, DecimalType):
        # DecimalType with scale > 0 means it has decimal places -> DoubleType
        if t.scale > 0:
            return DoubleType()
        # DecimalType with scale = 0 is integral
        if t.precision > 18:
            # Too big for long, keep as DecimalType
            return DecimalType(t.precision, 0)
        return LongType()
    elif isinstance(t, _FractionalType):
        # FloatType, DoubleType -> DoubleType
        return DoubleType()

    return t
