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
from dataclasses import dataclass
from datetime import datetime

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark._internal.utils import (
    TempObjectType,
    is_in_stored_procedure,
    random_name_for_temp_object,
)
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.row import Row
from snowflake.snowpark.types import (
    ArrayType,
    BooleanType,
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
    is_nss_enabled,
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
    discover_partition_columns_if_recursive,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    METADATA_FILENAME_COLUMN,
    add_filename_metadata_to_reader,
    populate_metadata,
)
from snowflake.snowpark_connect.relation.read.reader_config import (
    apply_drop_malformed_on_error,
    apply_permissive_on_error_json,
)
from snowflake.snowpark_connect.relation.read.source_resolution import (
    detach_infer_schema_options,
    generate_stage_path_groups_for_read,
)
from snowflake.snowpark_connect.relation.read.utils import (
    _load_file_with_copy_into,
    apply_metadata_exclusion_pattern,
    extract_relative_file_path,
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
from snowflake.snowpark_connect.utils.io_utils import (
    cached_file_format,
    first_db_schema_from_paths,
)
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


_json_file_format_allowed_options = {
    "COMPRESSION",
    "DATE_FORMAT",
    "TIMESTAMP_FORMAT",
    "FILE_EXTENSION",
    "STRIP_OUTER_ARRAY",
    "MULTI_LINE",
    "ENCODING",
    "NULL_IF",
    "REPLACE_INVALID_CHARACTERS",
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
    snowpark_options: dict[str, typing.Any],
) -> dict[str, typing.Any]:
    """
    Extract JSON file format options from Snowpark options.

    Args:
        snowpark_options: Dictionary of Snowpark options

    Returns:
        Dictionary of file format options that can be used with COPY INTO
    """
    file_format_options: dict[str, typing.Any] = dict()
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
    skip_parse_errors: bool = False,
    corrupt_record_column_name: str | None = None,
    strict_invalid_characters: bool = False,
) -> StructType:
    """
    Infer JSON schema by iterating rows from a DataFrame.

    When ``strict_invalid_characters`` is True (the user passed
    ``replaceInvalidCharacters=False``), an invalid-UTF-8 parse error is fatal
    and re-raised regardless of ``skip_parse_errors`` / Spark ``mode`` — the
    strict opt-out must be honored. Structurally malformed JSON is unaffected:
    it is still swallowed under PERMISSIVE (``skip_parse_errors=True``) as
    before.
    """
    inferred_schema = copy.deepcopy(initial_schema)
    columns_with_valid_contents = set()
    string_nodes_finalized = set[str]()

    schema_inference_df = (
        df
        if json_local_rows_to_infer_schema == -1
        else df.limit(json_local_rows_to_infer_schema)
    )
    try:
        for row in schema_inference_df.to_local_iterator():
            inferred_schema = merge_row_schema(
                inferred_schema,
                row,
                columns_with_valid_contents,
                string_nodes_finalized,
                drop_field_if_all_null,
            )
    except SnowparkSQLException as exc:
        # Strict opt-out: when replaceInvalidCharacters=False, an invalid-UTF-8
        # parse error is fatal regardless of skip_parse_errors / Spark mode.
        # Checked first so it short-circuits the PERMISSIVE swallow below. Only
        # the invalid-UTF-8 subclass is escalated — structurally malformed JSON
        # still follows the existing skip_parse_errors path.
        if strict_invalid_characters and _is_invalid_utf8_error(exc):
            raise
        if not skip_parse_errors or not _is_json_parse_error(exc):
            raise
        # PERMISSIVE/DROPMALFORMED: file has unparseable rows — fall back to
        # the initial schema from INFER_SCHEMA (which already skipped bad rows
        # via ON_ERROR=CONTINUE). We lose nested type refinement but avoid
        # erroring on malformed JSON during schema inference.
        logger.warning(
            "JSON schema inference encountered parse errors; "
            "falling back to initial inferred schema. Error: %s",
            exc,
        )
        if corrupt_record_column_name is not None:
            _ensure_corrupt_record_field(inferred_schema, corrupt_record_column_name)

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


def _find_corrupt_record_field(
    schema: StructType, corrupt_record_column_name: str
) -> StructField | None:
    expected_name = unquote_if_quoted(corrupt_record_column_name)
    for field in schema.fields:
        if unquote_if_quoted(field.name) == expected_name:
            return field
    return None


def _ensure_corrupt_record_field(
    schema: StructType, corrupt_record_column_name: str
) -> None:
    """Add Spark's corrupt-record field to inferred schemas when needed."""
    if _find_corrupt_record_field(schema, corrupt_record_column_name) is None:
        schema.fields = [
            StructField(
                quote_name_without_upper_casing(
                    unquote_if_quoted(corrupt_record_column_name)
                ),
                StringType(),
                True,
            )
        ] + list(schema.fields)


def _validate_corrupt_record_field(
    schema: StructType, corrupt_record_column_name: str
) -> None:
    """Validate Spark's corrupt-record field when a user schema includes it."""
    field = _find_corrupt_record_field(schema, corrupt_record_column_name)
    if field is None:
        return
    if not isinstance(field.datatype, StringType) or not field.nullable:
        exception = AnalysisException(
            "The field for corrupt records must be string type and nullable."
        )
        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
        raise exception


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


def _has_structured_complex_types(schema: StructType) -> bool:
    """Return True iff ``schema`` already contains a structured complex type.

    The structured INFER_SCHEMA fast path keys off this predicate. We treat any
    top-level field whose datatype is an ``ArrayType``, ``MapType`` or
    ``StructType`` with ``.structured == True`` as a positive signal that the
    backend resolved the JSON shape itself and the row-based slow path can be
    skipped.  ``getattr(..., "structured", False)`` is defensive against older
    Snowpark type variants that may lack the attribute.

    Exposed at module scope so unit tests can import it instead of duplicating
    the predicate (see ``tests/unit_tests/test_json_structured_type_fast_path.py``).
    """
    return any(
        isinstance(f.datatype, (ArrayType, MapType, StructType))
        and getattr(f.datatype, "structured", False)
        for f in schema.fields
    )


def _apply_schema_post_processing(
    schema: StructType, *, case_sensitive: bool, demote_timestamps: bool = True
) -> StructType:
    """Shared post-processing applied to the inferred schema before it is
    returned from ``_get_schema_for_copy_into_json``.

    Used by both the structured INFER_SCHEMA fast path and the local
    row-based slow path to ensure consistent schema clean-up.

    Order of operations:

    1. Strip the synthetic ``METADATA$FILENAME`` column.
    2. Optionally demote ``TimestampType`` (NTZ + LTZ both inherit) and
       ``DateType`` to ``StringType`` so the schema matches Spark's
       default ``inferTimestamp=false`` behaviour (see
       ``_demote_timestamp_to_string`` for the full rationale).
       Enabled by default for the fast path; disabled for the slow path
       where ``_infer_json_schema_from_rows`` already handles timestamps.
    3. ``validate_and_update_schema`` (NullType -> StringType, drop empty
       structs, etc.).
    4. Optional case-insensitive field dedup when
       ``spark.sql.caseSensitive`` is False.
    """
    if demote_timestamps:
        processed_schema = StructType(
            [
                StructField(
                    f.name,
                    _demote_timestamp_to_string(f.datatype),
                    f.nullable,
                )
                for f in schema.fields
                if f.name != METADATA_FILENAME_COLUMN
            ]
        )
    else:
        processed_schema = StructType(
            [f for f in schema.fields if f.name != METADATA_FILENAME_COLUMN]
        )
    processed_schema, _ = validate_and_update_schema(processed_schema)
    if not case_sensitive:
        processed_schema = _deduplicate_fields_case_insensitive(processed_schema)
    return processed_schema


# Backward-compatible alias so existing callers / tests that reference
# the old name continue to work during the transition.
_apply_fast_path_post_processing = _apply_schema_post_processing


def _demote_timestamp_to_string(t: DataType) -> DataType:
    """Spark's JSON reader does not auto-infer date/timestamp values from
    JSON string fields by default.  Verified against the Spark 3.5.x
    source tree:

    * ``JSONOptions`` exposes only ``inferTimestamp`` (default ``false``);
      there is **no** ``inferDate`` / ``preferDate`` / ``prefersDate``
      option for JSON.  ``preferDate`` exists on CSV (`CSVOptions`,
      default ``true``) and on XML, but it was never extended to JSON.
    * ``JsonInferSchema`` only inspects the ``inferTimestamp`` flag for
      ``VALUE_STRING`` tokens and can produce ``TimestampType`` /
      ``TimestampNTZType`` — it **never** produces ``DateType`` from a
      JSON string, regardless of any reader option.

    The SCOS slow path (``merge_row_schema``) matches this by leaving
    classified-from-Python-json values as ``StringType`` and explicitly
    demoting any pre-seeded ``TimestampType`` back to ``StringType``
    (see the ``elif isinstance(sf.datatype, TimestampType)`` branch
    around L1365).  The structured INFER_SCHEMA fast path needs the
    same demotion: Snowflake's typed-OBJECT inference auto-detects
    ISO-8601-shaped strings as ``DATE`` and ``TIMESTAMP_NTZ`` even on
    a JSON read, which a Spark client wouldn't have done.  Walk the
    type recursively and convert any ``DateType`` or ``TimestampType``
    (NTZ + LTZ variants both inherit from ``TimestampType``) to
    ``StringType``.

    NOTE: SAS does not yet honour the ``inferTimestamp`` reader option
    (it's commented out in ``reader_config.py``'s recognised-option
    whitelist), so this demotion is unconditional, matching the slow
    path.  When ``inferTimestamp`` is wired up in a future change,
    only the ``TimestampType`` branch becomes conditional — the
    ``DateType`` branch stays unconditional because Spark JSON never
    emits ``DateType`` from inference at all.
    """
    if isinstance(t, (DateType, TimestampType)):
        return StringType()
    if isinstance(t, ArrayType):
        if t.element_type is None:
            return t
        return ArrayType(_demote_timestamp_to_string(t.element_type))
    if isinstance(t, MapType):
        return MapType(t.key_type, _demote_timestamp_to_string(t.value_type))
    if isinstance(t, StructType):
        return StructType(
            [
                StructField(f.name, _demote_timestamp_to_string(f.datatype), f.nullable)
                for f in t.fields
            ]
        )
    return t


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


def _is_variant_fallback_schema(schema: StructType) -> bool:
    """Detect Snowflake INFER_SCHEMA's `$1 VARIANT` fallback schema.

    INFER_SCHEMA returns a single-field schema named ``$1`` with VariantType
    when it cannot extract structured columns from a JSON file (e.g. multi-line
    JSON read without ``multiLine=true``, or otherwise structurally malformed
    files). Snowpark normalizes both ``$1`` and ``"$1"`` field names to ``$1``,
    so the theoretical collision with a real JSON file containing only a
    single mixed-type field literally named ``$1`` cannot be distinguished
    here. Such files are exceedingly rare; users in that case can pass an
    explicit ``schema`` to bypass this check.
    """
    if len(schema.fields) != 1:
        return False
    field = schema.fields[0]
    return field.name == "$1" and isinstance(field.datatype, VariantType)


def _is_json_parse_error(exc: SnowparkSQLException) -> bool:
    error_code = getattr(exc, "sql_error_code", None)
    with suppress(TypeError, ValueError):
        if error_code is not None and int(error_code) == 100069:
            return True
    return "Error parsing JSON" in str(exc)


def _is_invalid_utf8_error(exc: SnowparkSQLException) -> bool:
    """Detect the *invalid-UTF-8* subclass of a JSON parse error.

    Snowflake error ``100069`` ("Error parsing JSON") is generic: it covers
    BOTH invalid UTF-8 bytes AND structurally malformed JSON. The strict
    ``replaceInvalidCharacters=False`` opt-out must re-raise ONLY the
    invalid-UTF-8 subclass, while leaving structural malformation to PERMISSIVE
    mode's malformed-row fallback. We therefore primarily key off the server
    message rather than the (generic) ``100069`` code.

    Defense in depth: when the SQL error code is available we additionally
    require it to be ``100069`` (the JSON-parse-error code) as a NECESSARY
    precondition, so an unrelated error that merely happens to mention "UTF8"
    in its text cannot be misclassified as a fatal invalid-character error.
    When the code is absent or unparseable, we fall back to the message match
    alone — losing the code attribute must not regress detection of a genuine
    invalid-UTF-8 error.

    The canonical server message form is ``"Invalid UTF8 detected in string"``
    (note: "UTF8" with no hyphen — observed in the CSV sibling path, see
    ``tests/expectation_tests/test_csv_permissive_tuning.py``). We also match
    hyphenated / alternate phrasings defensively. Matching is case-insensitive.
    """
    text = str(exc).lower()
    message_matches = (
        "invalid utf8" in text or "invalid utf-8" in text or "not a valid utf-8" in text
    )
    if not message_matches:
        return False
    # Necessary precondition: when a code is present and parseable, it must be
    # the JSON-parse-error code 100069. A present-but-different code disqualifies.
    error_code = getattr(exc, "sql_error_code", None)
    if error_code is not None:
        with suppress(TypeError, ValueError):
            return int(error_code) == 100069
    # Code absent or unparseable: fall back to the message match alone.
    return True


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
    mode: str = "PERMISSIVE",
    corrupt_record_column_name: str | None = None,
    strict_invalid_characters: bool = False,
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
        # Detach INFER_SCHEMA_OPTIONS so snowpark's in-place ``FILES``
        # resolution for this directory cannot leak into the next per-directory
        # group through the shared reader options (SNOW-3591574).
        infer_options = detach_infer_schema_options(snowpark_options)
        reader = add_filename_metadata_to_reader(
            session.read.options(infer_options), raw_options
        )
        df = reader.json(stage_files[0])

    if _is_variant_fallback_schema(df.schema):
        # INFER_SCHEMA returned only `$1 VARIANT`, meaning it could not extract
        # any structured columns from the file(s).  This typically happens when
        # the file is multi-line JSON read without `multiLine=true`, or is
        # otherwise structurally malformed.  Spark errors in this case;
        # surface a clean Spark-compatible error rather than silently
        # producing NULL rows downstream.
        exception = ValueError(
            "Failed to infer schema for JSON file(s). The file may be a "
            "multi-line JSON document; if so, retry with `multiLine=true`. "
            "Otherwise the file is malformed."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    # Fast path: when INFER_SCHEMA already returns structured types (e.g.
    # ARRAY(NUMBER), OBJECT(name TEXT)) because the backend parameter
    # ENABLE_STRUCTURED_TYPE_INFER_SCHEMA_FOR_JSON is enabled and
    # session._use_structured_type_infer_schema is True, df.schema
    # contains structured ArrayType/StructType/MapType. Skip the
    # expensive local row-based inference (_infer_json_schema_from_rows)
    # and the relax_types re-read entirely — the types from INFER_SCHEMA
    # are already precise.
    #
    # Skip the fast path, however, when the caller depends on options
    # whose semantics only the slow path can honour:
    #
    # * ``dropFieldIfAllNull=True`` — the slow path drops fields whose
    #   values are NULL across the sampled rows; INFER_SCHEMA never drops
    #   columns for nulls.
    # * Explicit user-set ``rowsToInferSchema`` — when the server's
    #   ``MAX_RECORDS_PER_FILE`` cap is in effect, the slow path's local
    #   row-merge (over up to ``jsonLocalRowsToInferSchema`` rows) is the
    #   only way to discover late-row keys and promote scalar types
    #   (e.g. int → float at row N+1). Without it the schema is locked to
    #   whatever the server saw in the capped sample.
    raw_options_lower = {k.lower() for k in raw_options}
    user_set_rows_to_infer = "rowstoinferschema" in raw_options_lower
    has_structured_types = _has_structured_complex_types(df.schema)
    # Note: ``strict_invalid_characters`` is intentionally NOT consulted on this
    # fast path. The fast path returns the INFER_SCHEMA types directly without a
    # local row scan, so there is no schema-inference site here that could
    # swallow an invalid-UTF-8 error. An invalid-UTF-8 row still aborts the read
    # later at COPY INTO, because the file format already carries
    # ``REPLACE_INVALID_CHARACTERS=FALSE`` (the strict opt-out) and the COPY step
    # enforces it. The leak the strict flag fixes is specific to the slow-path
    # row scan below.
    if (
        has_structured_types
        and not drop_field_if_all_null
        and not user_set_rows_to_infer
    ):
        return _apply_schema_post_processing(
            df.schema, case_sensitive=global_config.spark_sql_caseSensitive
        )

    # Slow path: local row-based schema inference.
    #
    # If df.schema came from structured INFER_SCHEMA the seed contains
    # typed OBJECT/ARRAY/MAP columns whose typed-cast COPY INTO would
    # silently drop or strict-reject keys not present in the server's
    # N-row sample (rejected with `220000 Typed object schema mismatch
    # in conversion`).  Collapse those nested complex columns to
    # VariantType first so the re-read loads JSON values permissively
    # and the merge_row_schema VariantType branch can rebuild the
    # structure across all sampled rows.
    #
    # When sampling is active, the inferred SQL also uses narrow types
    # from the sampled rows (e.g. NUMBER(2,0) from 10 rows).  Re-read
    # with widened types so _infer_json_schema_from_rows can scan
    # beyond the sampled range without overflowing narrow casts.
    if has_structured_types or relax_types_to_infer_schema:
        seed_schema = df.schema
        if has_structured_types:
            seed_schema = _convert_struct_type_to_variant(seed_schema)
        if relax_types_to_infer_schema:
            seed_schema = relax_json_types(seed_schema)

        normalized = StructType(
            [
                StructField(unquote_if_quoted(f.name), f.datatype, f.nullable)
                for f in seed_schema.fields
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
        skip_parse_errors=(mode.upper() != "FAILFAST"),
        corrupt_record_column_name=corrupt_record_column_name,
        strict_invalid_characters=strict_invalid_characters,
    )

    return _apply_schema_post_processing(
        inferred_schema,
        case_sensitive=global_config.spark_sql_caseSensitive,
        demote_timestamps=False,
    )


def map_read_json(
    rel: relation_proto.Relation,
    schema: StructType | None,
    session: snowpark.Session,
    paths: list[str],
    options: JsonReaderConfig,
    *,
    skip_partition_discovery: bool = False,
) -> DataFrameContainer:
    """
    Read a JSON file into a Snowpark DataFrame.

    [JSON lines](http://jsonlines.org/) file format is supported.

    We leverage the stage that is already created in the map_read function that
    calls this.
    """
    raw_options = rel.read.data_source.options
    has_explicit_corrupt_record_option = any(
        key.lower() == "columnnameofcorruptrecord" for key in raw_options
    )
    corrupt_record_column_name = (
        options.config.get("columnnameofcorruptrecord", "_corrupt_record")
        if has_explicit_corrupt_record_option
        else get_string_session_config_param("spark.sql.columnNameOfCorruptRecord")
    )
    if corrupt_record_column_name == "":
        corrupt_record_column_name = None
    # SPARK-35912: JSON file sources can always contain NULL values for any field
    # (missing keys are treated as null). Always convert non-nullable user schemas
    # to nullable, matching Spark's unconditional behavior.
    if schema is not None:
        if corrupt_record_column_name is not None:
            _validate_corrupt_record_field(schema, corrupt_record_column_name)
        schema = _make_schema_nullable(schema)

    if rel.read.is_streaming is True:
        # TODO: Structured streaming implementation.
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for JSON files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    # ── NSS (Native Spark Sandbox) branch ────────────────────────────────────
    # When enabled, delegate to STAGE_FILE_READER instead of COPY INTO. If the
    # caller supplied no schema, infer it via INFER_STAGE_FILE_SCHEMA (Spark's own
    # inference, so it matches the sandbox reader) and route the inferred schema
    # through the same path. INFER raises on empty (no columns) rather than falling
    # back to the COPY path, so an NSS gap surfaces loudly instead of silently.
    nss_enabled = is_nss_enabled()
    nss_columns = None
    nss_stage_path = nss_format_name = None
    if nss_enabled:
        # STAGE_FILE_READER's LOCATION is single-valued; a multi-path read would
        # silently return only paths[0]. Fail loudly until UNION-ALL support lands.
        if len(paths) > 1:
            exception = SnowparkConnectNotImplementedError(
                "NSS multi-path read not supported (v1): STAGE_FILE_READER accepts a "
                f"single LOCATION but {len(paths)} paths were given. Unset "
                "SCOS_NSS_ENABLED on the server to read multiple paths via COPY."
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        nss_format_name = get_string_session_config_param(
            "snowpark.connect.nss.json_format_name"
        )
        if not nss_format_name:
            from snowflake.snowpark_connect.nss.nss_file_format import (
                ensure_nss_temp_file_format,
            )

            nss_format_name = ensure_nss_temp_file_format(session, "json")
        # paths[0] arrives SQL-quoted (see _quote_stage_path); the NSS reader
        # re-quotes it, so strip one layer to avoid a doubled-quote syntax error.
        nss_stage_path = paths[0]
        if nss_stage_path.startswith("'") and nss_stage_path.endswith("'"):
            nss_stage_path = nss_stage_path[1:-1]
        if schema is None:
            # Infer the columns up front so they can be passed as DATA_SCHEMA to
            # STAGE_FILE_READER. Pass the read's mode + resolved corrupt-record
            # column (read .option -> spark.sql.columnNameOfCorruptRecord) so a
            # PERMISSIVE read's corrupt-record column is included / named correctly.
            from snowflake.snowpark_connect.nss.nss_infer_schema import (
                infer_via_stage_file_schema,
            )

            nss_multiline = str(options.config.get("multiline", "false")).lower()
            nss_mode = str(options.config.get("mode", "PERMISSIVE")).upper()
            nss_columns = infer_via_stage_file_schema(
                session,
                nss_stage_path,
                nss_format_name,
                get_string_session_config_param(
                    "snowpark.connect.nss.infer_stage_file_schema_fqn"
                ),
                nss_multiline,
                # thread the client's .option("samplingRatio", ...) into inference (Spark's
                # JsonInferSchema samples records); defaults to full-sample when unset.
                sampling_ratio=str(options.config.get("samplingratio", "1")),
                mode=nss_mode,
                corrupt_record_column=corrupt_record_column_name,
            )
        else:
            from snowflake.snowpark_connect.nss.nss_scan_options import (
                columns_from_spark_schema,
            )
            from snowflake.snowpark_connect.relation.read.map_read import (
                parse_data_source_schema_to_spark,
            )

            # TODO(SNOW-3717231): when an explicit schema is provided, still call an
            # INFER_STAGE_FILE_SCHEMA (with-schema) TVF so the backend returns the same
            # per-column response format as the schema-less case. The backend applies
            # different logic for the with-schema vs no-schema paths, and routing both
            # through infer keeps results consistent; the columns -> DATA_SCHEMA logic
            # below stays identical. Pending backend support — for now use the client's
            # Spark schema directly (its DataType.json(), no Snowpark round-trip).
            parsed_spark_schema = parse_data_source_schema_to_spark(rel)
            if parsed_spark_schema is None:
                # snowpark ``schema`` is non-None but the proto schema string is empty
                # — cannot build DATA_SCHEMA. Fail clearly rather than crash on
                # ``None.fields`` inside columns_from_spark_schema.
                exception = ValueError(
                    "NSS JSON read: an explicit schema was provided but the request "
                    "carried no parseable schema string."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception
            nss_columns = columns_from_spark_schema(parsed_spark_schema)

    if nss_enabled and nss_columns is not None:
        # STAGE_FILE_READER produces the file's data columns directly from
        # DATA_SCHEMA — no per-schema decoder UDTF.
        from snowflake.snowpark_connect.nss.nss_scan_options import (
            _unquote_name,
            filter_reader_options,
        )
        from snowflake.snowpark_connect.nss.nss_stage_file_reader import (
            nss_read_via_stage_file_reader,
        )

        # Filter to Spark JSON read options; ensure the resolved corrupt-record
        # column name (which may come from spark.sql.columnNameOfCorruptRecord,
        # not the read options) is passed so it matches the inferred column.
        nss_reader_options = filter_reader_options("json", dict(options.config))
        if corrupt_record_column_name:
            nss_reader_options["columnnameofcorruptrecord"] = corrupt_record_column_name

        # NSS read path (keyword kept out of the customer-visible log message)
        logger.info(f"reading JSON via STAGE_FILE_READER from {nss_stage_path}")
        df = nss_read_via_stage_file_reader(
            session=session,
            stage_path=nss_stage_path,
            file_format=nss_format_name,
            columns=nss_columns,
            reader_options=nss_reader_options,
            tvf_fqn=get_string_session_config_param(
                "snowpark.connect.nss.stage_file_reader_fqn"
            ),
        )

        # Column names are already known from nss_columns (the TVF output order), so derive the
        # Spark names from them rather than mapping back from Snowflake's uppercased df.columns.
        # (This doesn't avoid a describe round-trip — rename_columns_as_snowflake_standard reads
        # df.columns anyway — but it uses the authoritative original names.)
        spark_column_names = [_unquote_name(c.name) for c in nss_columns]
        renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
            df, rel.common.plan_id
        )
        return DataFrameContainer.create_with_column_mapping(
            dataframe=renamed_df,
            spark_column_names=spark_column_names,
            snowpark_column_names=snowpark_column_names,
            snowpark_column_types=None,
            can_be_cached=False,
        )
    # ── End NSS branch ────────────────────────────────────────────────────────

    else:
        snowpark_options = options.convert_to_snowpark_args()
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
        snowpark_options.pop("columnnameofcorruptrecord", None)
        mode_options = _json_mode_options(mode, snowpark_options)
        relax_types_to_infer_schema = (
            snowpark_options.pop("relaxtypestoinferschema", False)
            or _integral_types_conversion_enabled
        )
        apply_metadata_exclusion_pattern(snowpark_options)

        if len(paths) <= 0:
            exception = ValueError(f"No paths provided to read JSON files: {paths}")
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        copy_into_was_used = False
        if parallel_load_json_file and compression in ("auto", "none", "bz2"):
            # TODO: SNOW-3022765 Add read partitioned files support for reading bz2 file
            df = read_single_bz2_file(
                session,
                paths,
                split_size_mb,
                schema,
                json_local_rows_to_infer_schema,
                drop_field_if_all_null,
                mode_options.mode,
                compression != "none",
                file_encoding,
                relax_types_to_infer_schema,
            )
        else:
            # ``read_normal_json_files`` always lands the data in a temp
            # table via COPY INTO, so the container can skip its own
            # ``cache_result()`` materialization (see comment on the return
            # below). The bz2 branch returns a lazy DataFrame and still
            # benefits from the default materialization path.
            copy_into_was_used = True

            df = read_normal_json_files(
                session,
                paths,
                snowpark_options,
                raw_options,
                json_local_rows_to_infer_schema,
                drop_field_if_all_null,
                schema,
                relax_types_to_infer_schema,
                mode_options=mode_options,
                corrupt_record_column_name=corrupt_record_column_name,
                infer_schema_all_files=infer_schema_all_files,
                skip_partition_discovery=skip_partition_discovery,
            )

        spark_column_names = get_spark_column_names_from_snowpark_columns(
            df.columns,
            # JSON object fields are data/header names, not synthetic positional cN placeholders.
            apply_positional_normalization=False,
        )

        renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
            df, rel.common.plan_id
        )
        # Same rationale as in read_normal_json_files: keep user-supplied
        # types intact in the surfaced DataFrame schema; only widen when we
        # had to infer the schema ourselves.
        relax_types_for_output = relax_types_to_infer_schema and schema is None
        container = DataFrameContainer.create_with_column_mapping(
            dataframe=renamed_df,
            spark_column_names=spark_column_names,
            snowpark_column_names=snowpark_column_names,
            snowpark_column_types=[
                relax_json_types(f.datatype) if relax_types_for_output else f.datatype
                for f in df.schema.fields
            ],
        )
        if copy_into_was_used:
            # COPY INTO already materializes the result into a temp table, so
            # a subsequent ``cache_result()`` (triggered by df_cache_map's
            # materialization step) would create a redundant second temp
            # table. Suppress that materialization while still allowing the
            # container to be memoized in df_cache_map — using
            # ``can_be_cached=False`` would short-circuit df_cache_map
            # entirely and cause every downstream access on the same plan_id
            # to re-execute the COPY INTO.
            container = container.without_materialization()
        return container


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

    schema_was_inferred = schema is None
    if schema is None:
        schema = StructType([StructField(LINE_CONTENT, StructType([]))])
        # Strict ``replaceInvalidCharacters=False`` handling is intentionally
        # out of scope for the bz2 path: ``strict_invalid_characters`` is left
        # at its default (False), so this path stays lenient regardless of the
        # opt-out — matching pre-fix behavior. (The SNOW-3670779 fix targets the
        # normal-files slow path in ``read_normal_json_files``.)
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
    # Only widen inferred types; user-supplied schemas are a contract.
    if relax_types_to_infer_schema and schema_was_inferred:
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
    corrupt_record_column_name: str | None = None,
    *,
    load_as_variant: bool = False,
    failfast_mode: bool = False,
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
        load_as_variant: Empty ``StructType()`` catch-all; project ``$1::VARIANT AS value``.

    Returns:
        ``(target_columns, transformations)`` where *target_columns* is a list
        of quoted column names and *transformations* is a list of Snowpark
        Column objects with the appropriate casts.
    """
    from snowflake.snowpark.functions import sql_expr

    if load_as_variant:
        return [VALUE_COLUMN], [sql_expr("$1::VARIANT").alias(VALUE_COLUMN)]

    date_format = (
        file_format_options.get("DATE_FORMAT") if file_format_options else None
    )
    timestamp_format = (
        file_format_options.get("TIMESTAMP_FORMAT") if file_format_options else None
    )

    target_cols: list[str] = []
    transforms: list[snowpark.Column] = []

    for field in schema.fields:
        target_cols.append(field.name)
        if corrupt_record_column_name is not None and unquote_if_quoted(
            field.name
        ) == unquote_if_quoted(corrupt_record_column_name):
            # SNOW-3380163: COPY INTO exposes raw malformed JSON through
            # METADATA$CORRUPT_RECORD. Snowflake includes line terminators in
            # that slice; trim edge terminators to match Spark's raw record text.
            transforms.append(
                sql_expr(
                    "REGEXP_REPLACE(METADATA$CORRUPT_RECORD, '^[\\r\\n]+|[\\r\\n]+$', '')"
                ).alias(field.name)
            )
            continue
        source_expr = f"$1:{field.name}"
        cast_expr = _generate_json_path_reference(
            source_expr,
            field.datatype,
            date_format=date_format,
            timestamp_format=timestamp_format,
            copy_into=True,
            failfast_mode=failfast_mode,
        )
        transforms.append(sql_expr(cast_expr).alias(field.name))

    return target_cols, transforms


@dataclass(frozen=True)
class JsonModeOptions:
    mode: str
    copy_on_error: str | None


def _json_mode_options(mode: str, snowpark_options: dict) -> JsonModeOptions:
    mode_upper = mode.upper()
    if mode_upper == "PERMISSIVE":
        apply_permissive_on_error_json(snowpark_options)
        return JsonModeOptions(mode=mode_upper, copy_on_error="PERMISSIVE")
    if mode_upper == "DROPMALFORMED":
        apply_drop_malformed_on_error(snowpark_options)
        return JsonModeOptions(mode=mode_upper, copy_on_error="CONTINUE")
    if mode_upper == "FAILFAST":
        return JsonModeOptions(mode=mode_upper, copy_on_error="ABORT_STATEMENT")
    return JsonModeOptions(mode=mode_upper, copy_on_error=None)


def _copy_on_error_for_json_mode(mode_options: JsonModeOptions) -> str | None:
    if mode_options.mode == "PERMISSIVE":
        return "PARTIAL_RESULTS"
    return mode_options.copy_on_error


def read_normal_json_files(
    session: snowpark.Session,
    paths: list[str],
    snowpark_options: dict,
    raw_options: dict,
    json_local_rows_to_infer_schema: int,
    drop_field_if_all_null: bool,
    schema: StructType | None,
    relax_types_to_infer_schema: bool,
    mode_options: JsonModeOptions,
    corrupt_record_column_name: str | None,
    infer_schema_all_files: bool = True,
    *,
    skip_partition_discovery: bool = False,
) -> snowpark.DataFrame:
    # Read the normal JSON files, support metadata population
    needs_metadata = populate_metadata(raw_options)

    # Cisco catch-all JSON pipeline (empty StructType extension): load each
    # record as a single VARIANT column named "value". Mirrors the
    # jsonFileParallelLoading path (see construct_dataframe_by_schema_bulk) so
    # users can pass an empty schema in either mode and downstream
    # ``from_json(col("value"), ...)`` works the same way.
    load_as_variant = _is_empty_struct(schema)
    if load_as_variant:
        schema = StructType([StructField(VALUE_COLUMN, VariantType())])

    file_format_options = _parse_json_snowpark_options(snowpark_options)
    # Strict opt-out: when the user passes replaceInvalidCharacters=False, an
    # invalid-UTF-8 parse error during slow-path schema inference must be fatal
    # regardless of Spark `mode`. Read it from the full snowpark_options BEFORE
    # the reader_options filter below strips file-format keys (and
    # REPLACE_INVALID_CHARACTERS is a file-format option, so it would be gone
    # from reader_options). `is False` (identity) is deliberate: the value is a
    # real Python bool after config conversion; we want the strict path ONLY on
    # an explicit False, never on a missing key (defaults lenient) or a truthy
    # value.
    strict_invalid_characters = (
        snowpark_options.get("REPLACE_INVALID_CHARACTERS") is False
    )
    # Keep reader-level options separate from file format options.
    # ENFORCE_EXISTING_FILE_FORMAT cannot be used together with format type options.
    reader_options = {
        key: value
        for key, value in snowpark_options.items()
        if key.upper() not in _json_file_format_allowed_options
    }
    if "FORMAT_NAME" not in reader_options:
        reader_options["FORMAT_NAME"] = cached_file_format(
            session,
            "json",
            file_format_options,
            db_schema_fallback=first_db_schema_from_paths(paths),
        )
    reader_options["ENFORCE_EXISTING_FILE_FORMAT"] = True
    apply_metadata_exclusion_pattern(reader_options)

    reader = add_filename_metadata_to_reader(
        session.read.options(reader_options), raw_options
    )

    # Probe for Hive-style partition directories (lightweight LS on first path).
    partition_columns, partition_types = discover_partition_columns_if_recursive(
        session, paths[0], "json", skip_partition_discovery=skip_partition_discovery
    )

    logger.debug(
        f"Using COPY INTO for {len(paths)} JSON file(s)"
        f"{' with partition transforms' if partition_columns else ''}"
        f"{' with metadata' if needs_metadata else ''}."
    )
    temp_table_name = random_name_for_temp_object(TempObjectType.TABLE)
    stage_file_groups = generate_stage_path_groups_for_read(paths)
    for i, (stage_name, stage_files) in enumerate(stage_file_groups):
        if load_as_variant:
            copy_into_schema = schema
        else:
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
                mode=mode_options.mode,
                corrupt_record_column_name=(
                    corrupt_record_column_name
                    if mode_options.mode == "PERMISSIVE" and schema is None
                    else None
                ),
                strict_invalid_characters=strict_invalid_characters,
            )
        if len(stage_files) == 1:
            stage_file_paths = []
            copy_from_stage = stage_files[0]
        else:
            stage_file_paths = stage_files
            copy_from_stage = stage_name

        final_schema, _ = validate_and_update_schema(copy_into_schema)
        # Type relaxation widens narrow inferred types (e.g. NUMBER(2,0) ->
        # LongType) so the COPY INTO cast doesn't overflow on data outside the
        # sampled rows.  User-supplied schemas are an explicit contract: they
        # MUST flow through to the COPY INTO transformations and the
        # pre-created target table verbatim, so DecimalType(38,18) and
        # MapType(_, IntegerType) survive the load instead of being silently
        # widened to DoubleType / inner-LongType respectively.
        if relax_types_to_infer_schema and schema is None:
            final_schema = relax_json_types(final_schema)

        has_corrupt_record_field = (
            not load_as_variant
            and mode_options.mode == "PERMISSIVE"
            and corrupt_record_column_name is not None
            and _find_corrupt_record_field(final_schema, corrupt_record_column_name)
            is not None
        )
        reader_schema = None
        if has_corrupt_record_field:
            reader_schema = StructType(
                [
                    field
                    for field in final_schema.fields
                    if unquote_if_quoted(field.name)
                    != unquote_if_quoted(corrupt_record_column_name)
                ]
            )
        target_cols, typed_transforms = _build_json_typed_transformations(
            final_schema,
            session,
            file_format_options,
            corrupt_record_column_name if has_corrupt_record_field else None,
            load_as_variant=load_as_variant,
            failfast_mode=(mode_options.mode == "FAILFAST"),
        )

        _load_file_with_copy_into(
            reader=reader,
            session=session,
            target=temp_table_name,
            stage_file_paths=stage_file_paths,
            stage=copy_from_stage,
            schema=final_schema,
            file_format_options=file_format_options,
            file_format="json",
            on_error=_copy_on_error_for_json_mode(mode_options),
            partition_columns=partition_columns if partition_columns else None,
            partition_types=partition_types if partition_columns else None,
            needs_metadata=needs_metadata,
            target_columns=target_cols,
            transformations=typed_transforms,
            reader_schema_override=reader_schema,
            table_already_exists=(i > 0),
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

        # SNOW-3193229: a NullType placeholder on the way in is *not* a type
        # conflict -- it just means the prior pass had no concrete element type
        # yet (empty array, or freshly-introduced ArrayType placeholder while
        # walking nested array<array<...>>).  Treat it the same as ``schema is
        # None`` so we keep recursing into elements (dict -> StructType,
        # list -> ArrayType, scalar -> primitive).  The dict branch above
        # already does this for ``schema=NullType``; mirror the same guard
        # here so two layers of arrays don't collapse to ArrayType(StringType).
        if schema is not None and not isinstance(schema, NullType):
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
    # Numeric / boolean inference dispatch.
    #
    # Why this is *not* deferred to the catch-all map_simple_types() below:
    # Python's json.loads() returns arbitrary-precision int for any JSON number
    # without a fractional part. The catch-all path used type(content).__name__,
    # which maps "int" -> IntegerType regardless of magnitude. relax_json_types()
    # then only widens to LongType, so a 20-digit literal like
    # 92233720368547758070 silently overflowed to -10 when cast (Spark
    # JsonSuite "Primitive field and type inferring" expects DecimalType(20, 0)).
    #
    # bool MUST be checked before int because Python's bool is a subclass of int,
    # so isinstance(True, int) is True and would otherwise mis-infer as LongType.
    #
    # int branch is magnitude-aware: values inside the signed 64-bit range
    # ([-2^63, 2^63-1]) map directly to LongType (skipping the IntegerType
    # intermediate that caused the overflow). Anything outside that range maps
    # to DecimalType wide enough to hold all decimal digits, with a floor of 20
    # to match Spark's expected schema for the canonical 20-digit test value.
    #
    # float maps directly to DoubleType to avoid any future type-name lookup
    # drift in map_simple_types.
    elif isinstance(content, bool):
        current_schema = BooleanType()
    elif isinstance(content, int):
        if not (-(1 << 63) <= content <= (1 << 63) - 1):
            digits = len(str(abs(content)))
            current_schema = DecimalType(max(digits, 20), 0)
        else:
            current_schema = LongType()
    elif isinstance(content, float):
        current_schema = DoubleType()
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
                        (
                            None
                            if not isinstance(sf.datatype, StructType)
                            else sf.datatype
                        ),
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
                    # Note: ``columns_with_valid_contents`` is added inside the
                    # loop above only when an element is non-null. Empty lists
                    # and lists of all-NULL elements deliberately leave this
                    # column unmarked so ``dropFieldIfAllNull`` can drop it.
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
    for field in schema.fields:
        # Use _generate_json_path_reference to handle NULL values for missing/empty fields
        if root_column_name is not None:
            json_path_expr = _generate_json_path_reference(
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
            json_path_expr = _generate_json_path_reference(
                field.name, field.datatype, is_root=True
            )
        select_exprs.append(f"{json_path_expr} AS {field.name}")

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
    copy_into: bool = False,
    failfast_mode: bool = False,
) -> str:
    """
    Generate a JSON path reference with appropriate casting for nested fields.

    COPY INTO and bulk INSERT paths deliberately differ for scalar casts.
    COPY INTO passes ON_ERROR separately, so scalar expressions can stay as
    raw JSON paths and let COPY null type mismatches. Non-COPY paths
    (e.g. jsonFileParallelLoading/construct_dataframe_by_schema_bulk) do not
    have COPY ON_ERROR available, so they keep explicit TRY_CAST for scalars.
    For FAILFAST COPY INTO, structured types (StructType/ArrayType/MapType)
    use TRY_CAST ... PERMISSIVE to match Spark's field-level leniency: Spark
    FAILFAST only throws for corrupt records (unparseable JSON), not for
    struct-level schema drift (extra keys, sub-field type mismatches).
    Snowflake typed OBJECT/ARRAY columns are stricter and raise 220000 on any
    schema mismatch, so TRY_CAST PERMISSIVE bridges that gap for FAILFAST.
    For PERMISSIVE/DROPMALFORMED, ON_ERROR already handles this correctly.
    Date/Timestamp with custom formats use TRY_TO_DATE/TRY_TO_TIMESTAMP because
    COPY INTO file format options do not apply to VARIANT path extractions.

    Args:
        json_path: The JSON path to the field (e.g., "field_name:a.b.field")
        data_type: The DataType of the field
        is_root: Whether this is a root-level field (used in the legacy
            construct_dataframe_by_schema_bulk path)
        date_format: Optional Snowflake date format string (e.g., "YYYYMMDD")
        timestamp_format: Optional Snowflake timestamp format string
        copy_into: Whether this expression is used as a COPY INTO
            transformation with COPY ON_ERROR handling scalar mismatches.
        failfast_mode: Whether the read mode is FAILFAST. When True, structured
            types use TRY_CAST PERMISSIVE to avoid aborting on struct schema
            drift that Spark FAILFAST would handle silently.
    """
    if copy_into:
        if isinstance(data_type, (StructType, ArrayType, MapType)):
            if failfast_mode:
                return f"TRY_CAST({json_path} AS {_generate_snowflake_type_signature(data_type)} PERMISSIVE)"
            return json_path
        if isinstance(data_type, DateType) and date_format and date_format != "auto":
            return f"TRY_TO_DATE(TO_VARCHAR({json_path}), '{date_format}')"
        if (
            isinstance(data_type, TimestampType)
            and timestamp_format
            and timestamp_format != "auto"
        ):
            return f"TRY_TO_TIMESTAMP(TO_VARCHAR({json_path}), '{timestamp_format}')"
        return json_path

    if isinstance(data_type, (StructType, ArrayType, MapType)):
        return f"TRY_CAST({json_path} AS {_generate_snowflake_type_signature(data_type)} PERMISSIVE)"
    elif isinstance(data_type, DateType) and date_format and date_format != "auto":
        return f"TRY_TO_DATE(TO_VARCHAR({json_path}), '{date_format}')"
    elif (
        isinstance(data_type, TimestampType)
        and timestamp_format
        and timestamp_format != "auto"
    ):
        return f"TRY_TO_TIMESTAMP(TO_VARCHAR({json_path}), '{timestamp_format}')"
    if isinstance(data_type, StringType):
        return f"TO_VARCHAR({json_path})"
    if isinstance(data_type, VariantType):
        # SNOW-3585743: a JSON-path extraction is already a VARIANT value, and
        # any value is a valid VARIANT, so TRY_CAST(... AS VARIANT) is both
        # unnecessary and rejected by Snowflake with error 001065 ("Function
        # TRY_CAST cannot be used with arguments of types ... and VARIANT") --
        # TRY_CAST only supports string input and a fixed set of scalar target
        # types. TO_VARIANT is a no-op wrap that never fails.
        return json_path if is_root else f"TO_VARIANT({json_path})"
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
