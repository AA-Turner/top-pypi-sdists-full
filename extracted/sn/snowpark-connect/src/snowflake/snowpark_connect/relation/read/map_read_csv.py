#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy
import logging
import os
import warnings
from typing import Any

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException, IllegalArgumentException

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark._internal.utils import (
    TempObjectType,
    random_name_for_temp_object,
)
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    DecimalType,
    DoubleType,
    IntegerType,
    LongType,
    MapType,
    StringType,
    StructField,
    StructType,
    _FractionalType,
    _IntegralType,
)
from snowflake.snowpark_connect.config import (
    get_boolean_session_config_param,
    get_string_session_config_param,
    str_to_bool,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.map_unresolved_function import (
    _find_common_type,
)
from snowflake.snowpark_connect.relation.read.map_read import CsvReaderConfig
from snowflake.snowpark_connect.relation.read.map_read_partitioned_file import (
    _add_partition_columns,
    _discover_partition_columns,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    METADATA_FILENAME_COLUMN,
    add_filename_metadata_to_reader,
    get_non_metadata_fields,
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
    normalized_file_source_column_merge_key,
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
    # SPARK-35912: File sources like CSV can always contain NULL values,
    # so Spark automatically converts non-nullable user schemas to nullable.
    # This is controlled by snowpark.connect.io.validations.mode:
    # - "lenient" (default): preserve original nullable settings
    # - "strict": convert all fields to nullable (Spark behavior)
    # Note: CSV and JSON reads support this config. Parquet may be added in the future.
    io_validations_mode = (
        get_string_session_config_param("snowpark.connect.io.validations.mode")
        .strip()
        .lower()
        or "lenient"
    )

    if schema is not None and io_validations_mode == "strict":
        schema = _make_schema_nullable(schema)

    # Validate lineSep option - must not be empty (SPARK-35912 compatible behavior)
    line_sep = options.config.get("linesep")
    if line_sep is not None and line_sep == "":
        exception = IllegalArgumentException(
            "requirement failed: 'lineSep' cannot be an empty string."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception

    if rel.read.is_streaming is True:
        # TODO: Structured streaming implementation.
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for CSV files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception
    else:
        # Read mode before convert_to_snowpark_args() pops it.
        mode = options.config.get("mode", "PERMISSIVE")

        # Deprecated: snowpark.connect.csv.continueOnError → use mode=DROPMALFORMED.
        if get_boolean_session_config_param("snowpark.connect.csv.continueOnError"):
            warnings.warn(
                "snowpark.connect.csv.continueOnError is deprecated. "
                "Use .option('mode', 'DROPMALFORMED') instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            mode = "DROPMALFORMED"

        converted_snowpark_options = options.convert_to_snowpark_args()
        parse_header = str_to_bool(
            str(converted_snowpark_options.get("PARSE_HEADER", "false"))
        )
        csv_file_format_options = _snowflake_csv_file_format_options(
            converted_snowpark_options, parse_header=parse_header
        )

        raw_options = rel.read.data_source.options
        partition_columns, partition_types = _discover_partition_columns(
            session, paths[0], "csv"
        )
        if not parse_header:
            if populate_metadata(raw_options):
                exception = AnalysisException(
                    "snowpark.populateFileMetadata is not supported when reading CSV "
                    "without a header row."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            if partition_columns:
                # COPY INTO needs MATCH_BY_COLUMN_NAME to load METADATA$FILENAME
                # for partition discovery, which requires PARSE_HEADER (a header row).
                exception = AnalysisException(
                    "Hive-style partitioned CSV paths are not supported when reading "
                    "CSV without a header row."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception

        merge_schema = str_to_bool(str(options.config.get("mergeschema", "false")))

        file_format = cached_file_format(session, "csv", csv_file_format_options)

        snowpark_reader_options = dict()
        snowpark_reader_options["FORMAT_NAME"] = file_format
        snowpark_reader_options["ENFORCE_EXISTING_FILE_FORMAT"] = True
        snowpark_reader_options["INFER_SCHEMA"] = converted_snowpark_options.get(
            "INFER_SCHEMA", False
        )
        snowpark_reader_options[
            "INFER_SCHEMA_OPTIONS"
        ] = converted_snowpark_options.get("INFER_SCHEMA_OPTIONS", {})

        # Always use ON_ERROR=CONTINUE for schema inference so that corrupted
        # records don't abort type detection (SNOW-3308282).
        # Gate behind ENABLE_SCOS_FEATURE until the parameter is available on
        # all deployments.
        enable_scos_feature = getattr(session, "_enable_scos_feature", False)
        if enable_scos_feature:
            snowpark_reader_options["INFER_SCHEMA_OPTIONS"]["ON_ERROR"] = "CONTINUE"

        # Map Spark mode to Snowflake ON_ERROR for COPY INTO (SNOW-3308282).
        # PERMISSIVE/DROPMALFORMED → ON_ERROR=CONTINUE (skip bad rows).
        # FAILFAST → no ON_ERROR (Snowflake default aborts on first error).
        if enable_scos_feature and mode.upper() in ("DROPMALFORMED", "PERMISSIVE"):
            apply_drop_malformed_on_error(snowpark_reader_options)

        # Use Try_cast to avoid schema inference errors
        if snowpark_reader_options.get("INFER_SCHEMA", False):
            snowpark_reader_options["TRY_CAST"] = True

        apply_metadata_exclusion_pattern(converted_snowpark_options)
        snowpark_reader_options["PATTERN"] = converted_snowpark_options.get(
            "PATTERN", None
        )

        relax_types_to_infer_schema = (
            converted_snowpark_options.pop("relaxtypestoinferschema", False)
            or _integral_types_conversion_enabled
        )
        infer_schema = options._get_config_setting("inferschema")
        enforce_schema = options._get_config_setting("enforceschema")

        needs_populate_metadata = populate_metadata(raw_options)
        use_include_metadata = bool(partition_columns) or needs_populate_metadata

        logical_data_schema = _resolve_csv_schemas(
            session=session,
            schema=schema,
            all_paths=paths,
            snowpark_reader_options=snowpark_reader_options,
            parse_header=parse_header,
            infer_schema=infer_schema,
            relax_types_to_infer_schema=relax_types_to_infer_schema,
            partition_columns=partition_columns,
            merge_schema=merge_schema,
            enforce_schema=enforce_schema,
        )
        csv_copy_file_format_options = copy.copy(csv_file_format_options)

        copy_reader_opts = dict(snowpark_reader_options)
        copy_reader_opts["INFER_SCHEMA"] = False
        copy_reader_opts.pop("TRY_CAST", None)
        copy_reader_opts["FORMAT_NAME"] = cached_file_format(
            session, "csv", csv_copy_file_format_options
        )

        reader = add_filename_metadata_to_reader(
            session.read.options(copy_reader_opts), raw_options
        )

        data_string_schema = StructType(
            [
                StructField(f.name, StringType(), nullable=True)
                for f in logical_data_schema.fields
            ]
        )

        on_error = (
            "CONTINUE"
            if snowpark_reader_options.get("ON_ERROR") == "CONTINUE"
            else None
        )
        temp_table_name = random_name_for_temp_object(TempObjectType.TABLE)
        total_files_processed = 0

        for stage_name, stage_files in generate_stage_path_groups(paths):
            copy_result = _load_file_with_copy_into(
                reader=reader,
                session=session,
                target=temp_table_name,
                stage_file_paths=stage_files if len(stage_files) > 1 else [],
                stage=stage_name if len(stage_files) > 1 else stage_files[0],
                schema=data_string_schema,
                file_format_options=csv_copy_file_format_options,
                file_format="csv",
                on_error=on_error,
                needs_metadata=use_include_metadata,
            )
            for row in copy_result or []:
                rows_loaded = getattr(row, "rows_loaded", 0) or 0
                errors_seen = getattr(row, "errors_seen", 0) or 0
                # Count a file as processed if Snowflake attempted to load it,
                # even when all rows were rejected. With ON_ERROR=CONTINUE a
                # file-level parse error can cause Snowflake to skip every row
                # while still "seeing" the file. Only files that never matched
                # the pattern remain uncounted, which is what the
                # "No data files matched" error below is meant to detect.
                if rows_loaded > 0 or errors_seen > 0:
                    total_files_processed += 1
            if on_error == "CONTINUE" and copy_result:
                row = copy_result[0]
                errors_seen = getattr(row, "errors_seen", 0) or 0
                if errors_seen:
                    rows_loaded = getattr(row, "rows_loaded", 0) or 0
                    logger.warning(
                        "CSV read: %s valid rows loaded, %s rows "
                        "skipped due to parse errors. Stage: %s",
                        rows_loaded,
                        errors_seen,
                        stage_name if len(stage_files) > 1 else stage_files[0],
                    )

        if total_files_processed == 0:
            raise AnalysisException(
                "Unable to load CSV files. No data files matched the "
                "specified pattern or all matched files are empty."
            )

        df = session.table(temp_table_name)
        if schema is not None or infer_schema:
            df = _try_cast_csv_columns_to_logical_types(
                df,
                logical_data_schema,
                include_metadata_filename=use_include_metadata,
            )

        if partition_columns:
            df = _add_partition_columns(df, partition_columns, partition_types)
        if use_include_metadata and not needs_populate_metadata:
            df = df.drop(METADATA_FILENAME_COLUMN)

        spark_column_names = get_spark_column_names_from_snowpark_columns(df.columns)

        renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
            df, rel.common.plan_id
        )
        return DataFrameContainer.create_with_column_mapping(
            dataframe=renamed_df,
            spark_column_names=spark_column_names,
            snowpark_column_names=snowpark_column_names,
            snowpark_column_types=[
                relax_csv_types(f.datatype)
                if relax_types_to_infer_schema
                else f.datatype
                for f in df.schema.fields
            ],
            can_be_cached=False,
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


def _snowflake_csv_file_format_options(
    converted_snowpark_options: dict[str, Any],
    *,
    parse_header: bool,
) -> dict[str, Any]:
    """Snowflake CSV ``FILE_FORMAT`` options shared by infer, read, and ``COPY INTO``.

    Copies allowlisted type options from the converted reader config, then sets
    ``SKIP_BLANK_LINES``, ``PARSE_HEADER`` from the logical header flag, and
    ``SKIP_HEADER = 0`` (required when ``PARSE_HEADER`` is true). The same dict is
    used for the cached infer format and for COPY ``format_type_options``.
    """
    opts: dict[str, Any] = {}
    for key, value in converted_snowpark_options.items():
        upper_key = key.upper()
        if upper_key not in _csv_file_format_allowed_options:
            continue
        if upper_key in ("PARSE_HEADER", "SKIP_HEADER"):
            continue
        opts[upper_key] = value
    opts["SKIP_BLANK_LINES"] = True
    opts["PARSE_HEADER"] = parse_header
    opts["SKIP_HEADER"] = 0
    return opts


def _widen_csv_inferred_types(a: DataType, b: DataType) -> DataType:
    """Widen two CSV-inferred scalar types to their common supertype.

    Delegates to :func:`_find_common_type` with ``widen_to_string=True`` so
    that incompatible types fall back to ``StringType`` instead of raising.
    CSV inference only produces flat scalar types so the nested-type branches
    of ``_find_common_type`` are never reached.
    """
    return _find_common_type([a, b], widen_to_string=True)


def _merge_inferred_csv_struct_schemas(
    left: StructType | None, right: StructType
) -> StructType:
    """Union columns across inferred CSV schemas (mergeSchema across stage groups)."""
    if left is None:
        return right
    key_to_field: dict[str, StructField] = {}
    order: list[str] = []
    for sf in left.fields:
        k = normalized_file_source_column_merge_key(sf.name)
        key_to_field[k] = sf
        order.append(k)
    for sf in right.fields:
        k = normalized_file_source_column_merge_key(sf.name)
        if k not in key_to_field:
            key_to_field[k] = sf
            order.append(k)
        else:
            ex = key_to_field[k]
            merged_type = _widen_csv_inferred_types(ex.datatype, sf.datatype)
            key_to_field[k] = StructField(
                ex.name, merged_type, ex.nullable or sf.nullable
            )
    return StructType([key_to_field[k] for k in order])


def _infer_csv_schema_for_stage_chunk(
    session: snowpark.Session,
    chunk_paths: list[str],
    snowpark_reader_options: dict[str, Any],
    *,
    relax_types_to_infer_schema: bool,
) -> StructType:
    """Run Snowpark CSV ``INFER_SCHEMA`` for one COPY chunk (same stage, ``FILES`` when needed).

    Always forces ``INFER_SCHEMA=True`` regardless of the caller's reader
    options because this function is the schema-discovery step — the user's
    ``inferSchema`` flag only controls whether inferred types are kept or
    coerced to ``StringType`` afterward.
    """
    infer_opts = copy.copy(snowpark_reader_options)
    infer_opts["INFER_SCHEMA"] = True
    if len(chunk_paths) == 1:
        infer_df = session.read.options(infer_opts).csv(chunk_paths[0])
    else:
        clean_paths = [p.strip("'") for p in chunk_paths]
        common = os.path.commonprefix(clean_paths)
        dir_idx = common.rfind("/")
        if dir_idx >= 0:
            common = common[: dir_idx + 1]
        common_stage_prefix = f"'{common}'"
        relative_files = [
            extract_relative_file_path(path, common_stage_prefix)
            for path in chunk_paths
        ]
        infer_opts["INFER_SCHEMA_OPTIONS"] = {
            **infer_opts.get("INFER_SCHEMA_OPTIONS", {}),
            "FILES": relative_files,
        }
        infer_df = session.read.options(infer_opts).csv(common_stage_prefix)
    inferred_fields = get_non_metadata_fields(infer_df.schema.fields)
    logical = StructType(
        [StructField(f.name, f.datatype, f.nullable) for f in inferred_fields]
    )
    if relax_types_to_infer_schema:
        logical = relax_csv_types(logical)
    return logical


def _csv_struct_all_string_fields(st: StructType) -> StructType:
    """Spark ``inferSchema=false``: treat every column as string while keeping Snowflake names."""
    return StructType([StructField(f.name, StringType(), True) for f in st.fields])


def _try_cast_csv_columns_to_logical_types(
    df: snowpark.DataFrame,
    logical_schema: StructType,
    *,
    include_metadata_filename: bool,
) -> snowpark.DataFrame:
    """Apply TRY_CAST per logical field after plain string COPY INTO."""
    exprs: list[Any] = []
    for sf in logical_schema.fields:
        exprs.append(
            snowpark_fn.try_cast(snowpark_fn.col(sf.name), sf.datatype).alias(sf.name)
        )
    if include_metadata_filename and METADATA_FILENAME_COLUMN in df.columns:
        exprs.append(snowpark_fn.col(METADATA_FILENAME_COLUMN))
    return df.select(exprs)


def _validate_user_schema_against_file(
    user_schema: StructType,
    file_schema: StructType,
    enforce_schema: bool,
) -> None:
    """Compare user-provided schema against inferred file schema by column names and count.

    When ``enforce_schema`` is ``True`` (default), mismatches produce a warning.
    When ``False``, mismatches raise an ``AnalysisException``.
    """
    user_names = [
        normalized_file_source_column_merge_key(f.name) for f in user_schema.fields
    ]
    file_names = [
        normalized_file_source_column_merge_key(f.name) for f in file_schema.fields
    ]

    mismatches: list[str] = []
    if len(user_names) != len(file_names):
        mismatches.append(
            f"Column count mismatch: schema has {len(user_names)} columns, "
            f"file has {len(file_names)} columns."
        )
    if set(user_names) != set(file_names):
        missing_in_file = set(user_names) - set(file_names)
        extra_in_file = set(file_names) - set(user_names)
        parts: list[str] = []
        if missing_in_file:
            parts.append(
                f"columns in schema but not in file: {sorted(missing_in_file)}"
            )
        if extra_in_file:
            parts.append(f"columns in file but not in schema: {sorted(extra_in_file)}")
        mismatches.append("Column name mismatch: " + "; ".join(parts))

    if not mismatches:
        return

    message = "CSV schema validation: " + " ".join(mismatches)
    if enforce_schema:
        logger.warning(message)
    else:
        exception = AnalysisException(message)
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception


def _resolve_csv_schemas(
    session: snowpark.Session,
    schema: StructType | None,
    all_paths: list[str],
    snowpark_reader_options: dict[str, Any],
    parse_header: bool,
    infer_schema: bool,
    relax_types_to_infer_schema: bool,
    partition_columns: list[str],
    merge_schema: bool,
    enforce_schema: bool,
) -> StructType:
    """Return the logical CSV data schema (names + types) for unified COPY.

    Schema layout and column names come from Snowflake CSV ``INFER_SCHEMA`` via
    Snowpark ``session.read.options(..., INFER_SCHEMA=True).csv(...)``.

    **Header row present** (``parse_header``): column names come from the file header
    (via inference). ``mergeSchema`` is honored **only when** ``inferSchema`` is
    true — if ``inferSchema`` is false, the schema is taken from the **first path
    only** (``mergeSchema`` is ignored). If ``inferSchema`` is true and
    ``mergeSchema`` is true and there are multiple paths, schemas from **all**
    path groups are merged; if ``mergeSchema`` is false, only the **first** path
    is inferred.

    **No header**: column names are Snowflake’s positional names (Spark-style
    ``_c0``, ``_c1``, …). The schema is inferred from the **first path only**
    to match Spark’s behavior of determining column count from the first row
    of the first file.

    Without ``inferSchema``, inferred types are coerced to ``StringType`` in the
    logical schema (Spark ``inferSchema=false``).

    ``FILE_FORMAT`` options for COPY are built in ``map_read_csv`` via
    :func:`_snowflake_csv_file_format_options`; ``PARSE_HEADER`` there drives
    ``MATCH_BY_COLUMN_NAME`` in :func:`_load_file_with_copy_into`.
    """
    partition_set = set(partition_columns)
    first_path = all_paths[0]

    if schema is not None:
        user_data_schema = StructType(
            [f for f in schema.fields if unquote_if_quoted(f.name) not in partition_set]
        )
        if parse_header and not enforce_schema:
            merged_file_schema: StructType | None = None
            for _stage, chunk in generate_stage_path_groups(all_paths):
                chunk_schema = _infer_csv_schema_for_stage_chunk(
                    session,
                    chunk,
                    snowpark_reader_options,
                    relax_types_to_infer_schema=False,
                )
                merged_file_schema = _merge_inferred_csv_struct_schemas(
                    merged_file_schema, chunk_schema
                )
            _validate_user_schema_against_file(
                user_data_schema, merged_file_schema, enforce_schema
            )
        return user_data_schema

    if parse_header:
        if merge_schema and len(all_paths) > 1:
            merged: StructType | None = None
            for _stage, chunk in generate_stage_path_groups(all_paths):
                chunk_schema = _infer_csv_schema_for_stage_chunk(
                    session,
                    chunk,
                    snowpark_reader_options,
                    relax_types_to_infer_schema=relax_types_to_infer_schema,
                )
                merged = _merge_inferred_csv_struct_schemas(merged, chunk_schema)
            if not infer_schema:
                merged = _csv_struct_all_string_fields(merged)
            return merged

        logical = _infer_csv_schema_for_stage_chunk(
            session,
            [first_path],
            snowpark_reader_options,
            relax_types_to_infer_schema=relax_types_to_infer_schema,
        )
        if not infer_schema:
            logical = _csv_struct_all_string_fields(logical)
        return logical

    # No header: positional names (_c0, …). Spark determines column count
    # from the first row of the first file, so we infer from the first path only.
    logical = _infer_csv_schema_for_stage_chunk(
        session,
        [first_path],
        snowpark_reader_options,
        relax_types_to_infer_schema=infer_schema and relax_types_to_infer_schema,
    )
    if not infer_schema:
        logical = _csv_struct_all_string_fields(logical)
    return logical


def relax_csv_types(t: DataType) -> DataType:
    """Widen numeric types to match OSS Spark's CSV schema inference rules.

    Snowpark's USE_RELAXED_TYPES (most_permissive_type) which incorrectly maps all numerics to DoubleType.
    We now handle relaxation ourselves for all clients, replacing USE_RELAXED_TYPES with these Spark-compatible rules.

    After applying relax_csv_types, converts to Spark CSV types:
    - IntegerType, ShortType, ByteType -> IntegerType
    - LongType -> LongType
    - DecimalType with scale > 0 -> DoubleType
    - DecimalType with precision > 18 -> DecimalType (too big for long)
    - DecimalType with precision > 9 -> LongType
    - DecimalType with precision <= 9 -> IntegerType
    - FloatType, DoubleType -> DoubleType
    """
    if isinstance(t, StructType):
        for sf in t.fields:
            sf.datatype = relax_csv_types(sf.datatype)
        return t
    elif isinstance(t, ArrayType):
        if t.element_type is not None:
            t.element_type = relax_csv_types(t.element_type)
        return t
    elif isinstance(t, MapType):
        t.key_type = relax_csv_types(t.key_type)
        t.value_type = relax_csv_types(t.value_type)
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
        if t.precision > 9:
            return LongType()
        return IntegerType()
    elif isinstance(t, _FractionalType):
        # FloatType, DoubleType -> DoubleType
        return DoubleType()

    return t


def _make_schema_nullable(schema: StructType) -> StructType:
    """
    Convert all fields in a schema to nullable for CSV reading.

    SPARK-35912: CSV file sources can always contain NULL values,
    so Spark automatically converts non-nullable user schemas to nullable.
    This matches that behavior when snowpark.connect.io.validations.mode="strict".

    Args:
        schema: The schema to convert.

    Returns:
        A new StructType with all fields set to nullable=True.
    """

    def _make_type_nullable(data_type: DataType) -> DataType:
        """Recursively make nested types nullable."""
        if isinstance(data_type, StructType):
            return StructType(
                [
                    StructField(f.name, _make_type_nullable(f.datatype), nullable=True)
                    for f in data_type.fields
                ]
            )
        elif isinstance(data_type, ArrayType):
            element_type = data_type.element_type
            if element_type is not None:
                return ArrayType(
                    _make_type_nullable(element_type),
                    contains_null=True,
                )
            return data_type
        elif isinstance(data_type, MapType):
            key_type = data_type.key_type
            value_type = data_type.value_type
            if key_type is not None and value_type is not None:
                return MapType(
                    _make_type_nullable(key_type),
                    _make_type_nullable(value_type),
                    value_contains_null=True,
                )
            return data_type
        return data_type

    return StructType(
        [
            StructField(f.name, _make_type_nullable(f.datatype), nullable=True)
            for f in schema.fields
        ]
    )
