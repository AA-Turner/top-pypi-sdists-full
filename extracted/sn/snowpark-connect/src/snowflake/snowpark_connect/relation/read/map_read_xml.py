#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import os
from concurrent.futures import ThreadPoolExecutor

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import IllegalArgumentException

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark._internal.type_utils import convert_sp_to_sf_type
from snowflake.snowpark._internal.xml_schema_inference import merge_struct_types
from snowflake.snowpark.exceptions import (
    SnowparkDataframeReaderException,
    SnowparkSQLException,
)
from snowflake.snowpark.functions import sql_expr
from snowflake.snowpark.types import ArrayType, DataType, StructField, StructType
from snowflake.snowpark_connect.config import get_string_session_config_param
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.io_utils import (
    get_stage_url_prefix,
    is_external_cloud_url,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    add_filename_metadata_to_reader,
)
from snowflake.snowpark_connect.relation.read.reader_config import XmlReaderConfig
from snowflake.snowpark_connect.relation.read.source_resolution import (
    is_directory_stage_path,
)
from snowflake.snowpark_connect.relation.read.utils import (
    apply_metadata_exclusion_pattern,
    get_spark_column_names_from_snowpark_columns,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.relation.utils import random_string
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)

# MAX_CONCURRENCY_LEVEL is set to 8 by default and can be increase to a maximum of 32,
# if issue more than MAX_CONCURRENCY_LEVEL number of queries at the same time,
# outstanding queries will be queued to execute.
# to maximize the resource of warehouse, we set XML_READ_MAX_PARALLEL to 32 by default
XML_READ_MAX_PARALLEL = 32

"""
This module reads XML files with Spark parity by:
1. Using user-provided schema or Snowpark's XML schema inference (inferSchema=True
   infers full types; inferSchema=False infers structure with all-StringType leaves)
2. Enforcing case-sensitive field name matching (Spark behavior)
3. Reconstructing data with proper structured types

Key differences between Spark and Snowpark's XML readers, addressed by this module:
- Spark XML is strictly CASE-SENSITIVE for field matching; Snowpark is case-insensitive
- Spark defaults rowTag to "ROW" if not provided; Snowpark throws exception
- Spark returns proper structured types for nested XML; Snowpark returns JSON strings
"""


def map_read_xml(
    rel: relation_proto.Relation,
    schema: StructType | None,
    session: snowpark.Session,
    paths: list[str],
    options: XmlReaderConfig,
    *,
    is_recursive: bool = True,
) -> DataFrameContainer:
    """
    Read XML files into a Snowpark DataFrame.

    Args:
        rel: Protobuf relation from Spark Connect protocol
        schema: User-provided schema, or None to use Snowpark's built-in schema inference
        session: Snowpark session
        paths: Stage paths to XML files
        options: XmlReaderConfig with Spark->Snowpark option translations
        is_recursive: When ``False``, only depth-0 ``.xml`` files are listed per path
            (Spark ``recursiveFileLookup=false`` parity, SNOW-3566246). Defaults to
            ``True`` so nested XML is included when the option is absent.

    Returns:
        DataFrameContainer with proper column mappings

    Raises:
        SnowparkConnectNotImplementedError: If streaming requested

    Notes:
        We leverage the stage that is already created in the map_read function that calls this.
    """

    # [SPARK PARITY] Validate XML options eagerly, matching Spark's behavior
    _validate_xml_options(options)

    if rel.read.is_streaming:
        # TODO: Structured streaming implementation.
        exception = SnowparkConnectNotImplementedError(
            "Streaming is not supported for XML files."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    snowpark_options = options.convert_to_snowpark_args()
    raw_options = rel.read.data_source.options

    # [SPARK PARITY] Handle rowTag - Spark defaults to "ROW" if not provided
    row_tag = snowpark_options.get("rowtag")
    if not row_tag:
        row_tag = "ROW"
        logger.info("XML reader: rowTag not provided, using default 'ROW'")
    snowpark_options.pop("rowtag", None)
    snowpark_options["rowTag"] = row_tag

    # Handle rowValidationXSDPath - upload local XSD files to stage
    # Snowpark's UDTF cannot access local files, so XSD must be on a stage
    xsd_path = snowpark_options.get("rowvalidationxsdpath")
    if xsd_path and not xsd_path.startswith("@"):
        # Local XSD file - upload to same stage as XML data
        local_xsd = xsd_path[7:] if xsd_path.startswith("file://") else xsd_path
        if os.path.isfile(local_xsd):
            data_path = paths[0].strip("'")
            stage_name = data_path.split("/")[0]
            logger.info(f"Uploading local XSD file {local_xsd} to {stage_name}/")

            session.file.put(
                local_xsd, f"{stage_name}/", auto_compress=False, overwrite=True
            )
            snowpark_options[
                "rowvalidationxsdpath"
            ] = f"{stage_name}/{os.path.basename(local_xsd)}"

    if schema is not None:
        snowpark_options["inferschema"] = False
        # Internal flag to tell Snowpark to skip the XML schema inference pass regardless of
        # inferSchema=True or False, maintaining 1-pass reading when user schema is provided.
        snowpark_options["_xml_skip_inference"] = True

    apply_metadata_exclusion_pattern(snowpark_options)

    # if there are dir in the paths, extend them to list of file
    paths = _get_all_xml_file_paths(paths, session, recursive=is_recursive)

    effective_schema = schema
    has_multi_files = len(paths) > 1

    def _read_xml_file(
        path: str,
    ) -> tuple[snowpark.DataFrame, StructType | None]:
        """Each thread gets its own DataFrameReader so that
        _xml_inferred_schema is never clobbered by another thread."""
        local_reader = add_filename_metadata_to_reader(
            session.read.options(snowpark_options), raw_options
        )
        file_df = local_reader.xml(path)
        return file_df, local_reader._xml_inferred_schema

    try:
        # Read XML paths in parallel, then union all results by column name.
        max_workers = min(len(paths), XML_READ_MAX_PARALLEL)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(_read_xml_file, paths))

        df = None
        for file_df, inferred_schema in results:
            if schema is None and inferred_schema is not None:
                if effective_schema is None:
                    effective_schema = inferred_schema
                else:
                    effective_schema = merge_struct_types(
                        effective_schema, inferred_schema
                    )

            if has_multi_files:
                file_df = _cast_all_to_variant(file_df)
            df = (
                file_df
                if df is None
                else df.union_all_by_name(file_df, allow_missing_columns=True)
            )

        # [SPARK PARITY] Transform data to match user schema and case sensitivity
        if df is not None and effective_schema is not None:
            # SNOW-3245148: Pass nullValue option to schema application to match Spark behavior.
            # Values matching nullValue (or whitespace-only) are converted to NULL before
            # type casting, preventing cast errors like "Failed to cast variant value to FIXED".
            # Only enabled in "strict" mode to avoid breaking changes.
            null_value = options.get("nullvalue") or ""
            io_mode = (
                get_string_session_config_param("snowpark.connect.io.validations.mode")
                .strip()
                .lower()
                or "lenient"
            )
            df = _apply_xml_schema(df, effective_schema, null_value, io_mode)

    except SnowparkDataframeReaderException as e:
        # [SPARK PARITY] Return empty DataFrame if rowTag not found
        if "Cannot find the row tag" in str(e):
            logger.info(
                f"XML reader: rowTag '{row_tag}' not found, returning empty DataFrame"
            )
            empty_schema = effective_schema or StructType([])
            df = _create_empty_dataframe_with_schema(empty_schema, session)
        else:
            raise

    if df is None:
        empty_schema = effective_schema or StructType([])
        df = _create_empty_dataframe_with_schema(empty_schema, session)

    spark_column_names = get_spark_column_names_from_snowpark_columns(df.columns)
    renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
        df, rel.common.plan_id
    )
    fields = (
        effective_schema.fields if effective_schema is not None else df.schema.fields
    )
    snowpark_column_types = [emulate_integral_types(f.datatype) for f in fields]

    return DataFrameContainer.create_with_column_mapping(
        dataframe=renamed_df,
        spark_column_names=spark_column_names,
        snowpark_column_names=snowpark_column_names,
        snowpark_column_types=snowpark_column_types,
    )


# =============================================================================
# SPARK PARITY HELPERS
# These functions modify Snowpark behavior to match Spark exactly.
# =============================================================================


def _validate_xml_options(options: XmlReaderConfig) -> None:
    """
    [SPARK PARITY] Validate XML options eagerly, matching Spark's client-side validation.

    See: org.apache.spark.sql.catalyst.xml.XmlOptions (Spark 4.0)
         com.databricks.spark.xml.XmlOptions (spark-xml package)
    """
    row_tag = options.get("rowtag")
    value_tag = options.get("valuetag")
    attribute_prefix = options.get("attributeprefix")
    root_tag = options.get("roottag")

    # 1. rowTag must not be empty
    if row_tag is not None and row_tag == "":
        exception = IllegalArgumentException(
            "requirement failed: 'rowTag' option should not be empty string."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception

    # 2. valueTag must not be empty
    if value_tag is not None and value_tag == "":
        exception = IllegalArgumentException(
            "requirement failed: 'valueTag' option should not be empty string."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception

    # 3. rowTag must not contain angle brackets
    if row_tag is not None and ("<" in row_tag or ">" in row_tag):
        exception = IllegalArgumentException(
            "requirement failed: 'rowTag' should not include angle brackets"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception

    # 4. rootTag must not contain angle brackets
    if root_tag is not None and ("<" in root_tag or ">" in root_tag):
        exception = IllegalArgumentException(
            "requirement failed: 'rootTag' should not include angle brackets"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception

    # 5. valueTag and attributePrefix must not be the same
    if (
        value_tag is not None
        and attribute_prefix is not None
        and value_tag == attribute_prefix
    ):
        exception = IllegalArgumentException(
            "requirement failed: 'valueTag' and 'attributePrefix' options should not be the same."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception


def _apply_xml_schema(
    snowpark_df: snowpark.DataFrame,
    schema: StructType,
    null_value: str = "",
    io_mode: str = "lenient",
) -> snowpark.DataFrame:
    """
    Cast Snowpark XML output to match the given schema:
    - Maps Snowpark column names to user or inferred schema field names
    - Applies case-sensitive matching where missing columns become NULL
    - Normalizes single-element arrays
    - In strict mode: Pre-processes nullValue matches and whitespace-only values to NULL

    Args:
        snowpark_df: Input DataFrame from XML reader
        schema: Target schema to apply
        null_value: Value to treat as NULL (from nullValue option, default "")
        io_mode: IO validations mode ("strict" or "lenient", default "lenient")
    """
    snowpark_columns = set(snowpark_df.columns)
    select_exprs = []

    for field in schema.fields:
        field_name = field._name
        snowpark_col = _resolve_column_name(field_name, snowpark_columns)

        # [SPARK PARITY] Case-sensitive matching - return NULL if column doesn't exist
        if snowpark_col is None:
            sf_type = convert_sp_to_sf_type(field.datatype)
            select_exprs.append(sql_expr(f"NULL::{sf_type}").alias(f'"{field_name}"'))
            continue

        normalized = _normalize_nested_schema(
            snowpark_col, field.datatype, null_value, io_mode
        )
        sf_type = convert_sp_to_sf_type(field.datatype)
        # [SNOW-3245148] In strict mode, normalize returns expression that converts
        # nullValue matches and whitespace-only values to NULL, so casting will succeed.
        select_exprs.append(
            sql_expr(f"({normalized})::{sf_type}").alias(f'"{field_name}"')
        )

    return snowpark_df.select(*select_exprs)


def _normalize_nested_schema(
    col_path: str, datatype: DataType, null_value: str = "", io_mode: str = "lenient"
) -> str:
    """
    Recursively normalize VARIANT data so it can cast to the expected structured type.

    Args:
        col_path: SQL path to column (e.g., 'reviews' or 'reviews:review')
        datatype: Expected datatype from user schema
        null_value: Value to treat as NULL (from nullValue option)
        io_mode: IO validations mode ("strict" or "lenient", default "lenient")

    Returns:
        SQL expression string with array normalization applied where needed

    Note:
    - ArrayType: wrap single-element objects in ARRAY_CONSTRUCT; use TRANSFORM to
      recurse into each element so nested structs/arrays are also normalized.
    - OBJECT_CONSTRUCT returns OBJECT type, which CANNOT cast to structured OBJECT(...)
    - OBJECT_CONSTRUCT_KEEP_NULL(...)::VARIANT returns VARIANT, which CAN cast to structured types
    - [SNOW-3245148] In strict mode, pre-process nullValue matches to NULL before casting
    """
    if isinstance(datatype, ArrayType):
        arr_expr = f"IFF(IS_ARRAY({col_path}), {col_path}, ARRAY_CONSTRUCT({col_path}))"
        element_type = datatype.element_type
        if isinstance(element_type, (StructType, ArrayType)):
            inner = _normalize_nested_schema("__e", element_type, null_value, io_mode)
            return f"TRANSFORM({arr_expr}, __e -> {inner})"
        return arr_expr

    elif isinstance(datatype, StructType):
        # Rebuild struct with OBJECT_CONSTRUCT_KEEP_NULL for proper casting
        field_exprs = []
        for field in datatype.fields:
            field_name = field._name
            nested_path = f"{col_path}['{field_name}']"
            normalized = _normalize_nested_schema(
                nested_path, field.datatype, null_value, io_mode
            )
            field_exprs.append(f"'{field_name}', {normalized}")
        # ::VARIANT suffix is KEY - allows casting to structured OBJECT(...)
        reconstructed = f"OBJECT_CONSTRUCT_KEEP_NULL({', '.join(field_exprs)})::VARIANT"
        # [SPARK PARITY] Preserve NULL if original struct is NULL (element missing in XML)
        return f"IFF({col_path} IS NULL, NULL, {reconstructed})"

    else:
        # [SNOW-3245148] In strict mode, pre-process leaf values to NULL for:
        # 1. Values matching nullValue option (after trimming)
        # 2. Whitespace-only values (which can't be cast to numeric types)
        # This ensures proper NULL handling before type casting, matching Spark behavior.
        # In lenient mode (default), return the value as-is for backward compatibility.
        if io_mode == "strict":
            escaped_null_value = null_value.replace("'", "''")
            # Convert VARIANT to VARCHAR for comparison, then check if:
            # - After TRIM, it matches the nullValue
            # - After TRIM, it's empty (whitespace-only case)
            # If either condition is true, return NULL; otherwise return original VARIANT
            return (
                f"IFF("
                f"TRIM({col_path}::VARCHAR) = '{escaped_null_value}' "
                f"OR TRIM({col_path}::VARCHAR) = '', "
                f"NULL, "
                f"{col_path}"
                f")"
            )
        else:
            return col_path


def _create_empty_dataframe_with_schema(
    schema: StructType,
    session: snowpark.Session,
) -> snowpark.DataFrame:
    """
    [SPARK PARITY] Create empty DataFrame when rowTag not found.

    Why needed: Spark returns empty DataFrame with user's schema if rowTag
    doesn't exist in XML. Snowpark throws "Cannot find the row tag" error.
    """
    quoted_schema = _quote_top_level_schema_fields(schema)
    return session.create_dataframe([], schema=quoted_schema)


def _quote_top_level_schema_fields(schema: StructType) -> StructType:
    """
    [SPARK PARITY] Quote top-level field names to preserve case in Snowflake.

    Why needed: Snowflake uppercases unquoted identifiers (title -> TITLE).
    Spark preserves original case. By quoting, we get: "title" -> title.

    Only top-level fields need quoting (table columns). Nested fields inside
    OBJECT columns don't need quoting as they're stored as JSON from Snowpark's XML reader.
    """
    return StructType(
        [
            StructField(
                f'"{field._name}"',
                field.datatype,
                field.nullable,
            )
            for field in schema.fields
        ],
        structured=schema.structured,
    )


def _get_all_xml_file_paths(
    paths: list[str],
    session: snowpark.Session,
    *,
    recursive: bool = True,
) -> list[str]:
    paths = [str(p) for p in paths]
    paths = [p[1:-1] if p.startswith("'") and p.endswith("'") else p for p in paths]
    stage_url_cache: dict[str, str | None] = {}
    # Cache cloned temp stage references per original stage name so that
    # multiple XML paths on the same external stage reuse a single clone
    # instead of issuing redundant CREATE TEMP STAGE ... CLONE DDLs.
    xml_clone_cache: dict[str, str | None] = {}
    result = []
    for path in paths:
        try:

            ls_result = session.sql(f"LS {path}").collect()
            if not ls_result:
                result.append(path)
                continue

            stage_name = path[1:].split("/", 1)[0]
            is_external_stage = is_external_cloud_url(ls_result[0][0])
            if stage_name not in stage_url_cache:
                stage_url = (
                    get_stage_url_prefix(stage_name, session)
                    if is_external_stage
                    else stage_name
                )
                stage_url_cache[stage_name] = stage_url
            else:
                stage_url = stage_url_cache[stage_name]
            if is_external_stage and not stage_url:
                result.append(path)
                continue

            # The XML UDTF sandbox cannot resolve credentials on named
            # persistent external stages. Re-wire to a session-scoped temp
            # stage so the UDTF can read files without data movement.
            if is_external_stage:
                if stage_name not in xml_clone_cache:
                    xml_clone_cache[stage_name] = _clone_xml_external_stage(
                        stage_name, session
                    )
                temp_stage = xml_clone_cache[stage_name]
                if temp_stage is not None:
                    original_suffix = (
                        path[1:].split("/", 1)[1] if "/" in path[1:] else None
                    )
                    parts = [temp_stage]
                    if original_suffix is not None:
                        parts.append(original_suffix)
                    path = "/".join(parts)
                    stage_name = temp_stage.lstrip("@")

            files = [res[0] for res in ls_result]
            res = _generate_list_of_files(
                stage_name,
                path,
                files,
                stage_url or stage_name,
                recursive=recursive,
            )
            result.extend(res)

        except Exception:
            # if failed, we still pass in whatever user give us to try finish the read
            result.append(path)
    if not result:
        exception = IllegalArgumentException("Path does not contain valid XML file")
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception
    return result


def _clone_xml_external_stage(
    stage_name: str,
    session: snowpark.Session,
) -> str | None:
    """Clone an external stage to a session-scoped temp stage for XML reads.

    The XML UDTF sandbox cannot resolve credentials on named external
    stages.  Cloning to a temp stage preserves all properties (URL,
    credentials, storage integration), making it accessible to the XML UDTF,
    and incurring no data movement costs.

    Returns the fully-qualified temp stage reference (e.g. ``@DB.SCHEMA.name``)
    or ``None`` if the clone fails.
    """
    clone_stage_name = random_string(5, "spark_connect_xml_stage_ext_")
    try:
        session.sql(
            f"CREATE OR REPLACE TEMP STAGE {clone_stage_name} CLONE {stage_name}"
        ).collect()
    except SnowparkSQLException:
        logger.warning("CLONE failed for stage %s, skipping rewrite", stage_name)
        return None
    except Exception:
        logger.error("Unexpected error cloning stage %s", stage_name, exc_info=True)
        return None

    db = unquote_if_quoted(session.get_current_database())
    schema = unquote_if_quoted(session.get_current_schema())
    return f"@{db}.{schema}.{clone_stage_name}"


def _generate_list_of_files(
    stage_name: str,
    path: str,
    files: list[str],
    stage_url: str,
    *,
    recursive: bool = True,
) -> list[str]:
    """Return ``.xml`` files under ``path``, mapped back to stage paths.

    When ``recursive`` is false, only direct-child ``.xml`` files are included.
    When true, any ``.xml`` file under the directory prefix is included.
    """
    result: list[str] = []
    stage_token = f"@{stage_name}"
    path_suffix = path[len(stage_token) :]
    listed_roots = [stage_url]
    if not is_external_cloud_url(stage_url):
        # LS on fully-qualified internal stages can return rows rooted at the
        # unqualified stage name (for example, my_stage/...) while the input path
        # uses DB.SCHEMA.MY_STAGE. Include both forms for matching.
        listed_roots = [stage_name]
        stage_leaf_name = stage_name.split(".")[-1]
        if stage_leaf_name.lower() != stage_name.lower():
            listed_roots.append(stage_leaf_name)
    dir_roots = [(root, f"{root}{path_suffix}") for root in listed_roots]

    path_without_at = path[1:]
    path_without_at_lower = path_without_at.lower()
    for file in files:
        file_lower = file.lower()
        matched_pair = next(
            (pair for pair in dir_roots if file_lower.startswith(pair[1].lower())),
            None,
        )
        if file_lower == path_without_at_lower or any(
            file_lower == dir_root.lower() for _, dir_root in dir_roots
        ):
            result.append(path)
            continue

        if matched_pair is None:
            continue
        matched_root, matched_dir_root = matched_pair
        file_name = file[len(matched_dir_root) :]  # part after dir root
        if not file_name.lower().endswith(".xml"):
            continue
        # Depth-0 only when recursiveFileLookup=false (Spark parity, SNOW-3566246).
        if not recursive and "/" in file_name.lstrip("/"):
            continue

        # Map back to stage path format under original input path
        result.append(
            f"@{_replace_prefix_case_insensitive(file, matched_root, stage_name)}"
        )
    # If user did not specify a directory (no trailing slash) and no XML matched,
    # preserve the original path as fallback so downstream read can handle it.
    if not result and not is_directory_stage_path(path):
        return [path]
    return result


def _replace_prefix_case_insensitive(
    source: str,
    prefix: str,
    replacement: str,
) -> str:
    """Replace a prefix while ignoring case, preserving the source suffix."""
    if source.lower().startswith(prefix.lower()):
        return f"{replacement}{source[len(prefix):]}"
    return source


def _cast_all_to_variant(df: snowpark.DataFrame) -> snowpark.DataFrame:
    return df.select([df[c].cast("VARIANT").alias(c) for c in df.columns])


def _resolve_column_name(field_name: str, snowpark_columns: set[str]) -> str | None:
    # inferSchema=False produces "'field_name'"
    candidate = f"\"'{field_name}'\""
    if candidate in snowpark_columns:
        return candidate

    # inferSchema=True produces '"field_name"'
    candidate = f'"{field_name}"'
    if candidate in snowpark_columns:
        return candidate

    if field_name in snowpark_columns:
        return f'"{field_name}"'

    return None
