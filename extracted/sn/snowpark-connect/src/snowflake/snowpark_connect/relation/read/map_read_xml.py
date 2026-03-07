#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import os

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import IllegalArgumentException

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark._internal.type_utils import convert_sp_to_sf_type
from snowflake.snowpark.exceptions import SnowparkDataframeReaderException
from snowflake.snowpark.functions import sql_expr
from snowflake.snowpark.types import ArrayType, DataType, StructField, StructType
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    add_filename_metadata_to_reader,
)
from snowflake.snowpark_connect.relation.read.reader_config import XmlReaderConfig
from snowflake.snowpark_connect.relation.read.utils import (
    apply_metadata_exclusion_pattern,
    get_spark_column_names_from_snowpark_columns,
    rename_columns_as_snowflake_standard,
)
from snowflake.snowpark_connect.type_support import emulate_integral_types
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)

"""
This module reads XML files with Spark parity by:
1. Requiring user-provided schema (schema inference is not yet supported)
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
) -> DataFrameContainer:
    """
    Read XML files into a Snowpark DataFrame.

    Args:
        rel: Protobuf relation from Spark Connect protocol
        schema: User-provided schema (REQUIRED - inference not supported)
        session: Snowpark session
        paths: Stage paths to XML files
        options: XmlReaderConfig with Spark->Snowpark option translations

    Returns:
        DataFrameContainer with proper column mappings

    Raises:
        SnowparkConnectNotImplementedError: If streaming or schema inference requested

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

    if schema is None:
        # TODO: Schema inference is not yet supported.
        exception = SnowparkConnectNotImplementedError(
            "XML schema inference is not yet supported. "
            "Please provide a schema using .schema() before .load(). "
            "Example: spark.read.format('xml').option('rowTag', 'book').schema(user_schema).load(path)"
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

    apply_metadata_exclusion_pattern(snowpark_options)
    reader = add_filename_metadata_to_reader(
        session.read.options(snowpark_options), raw_options
    )

    # Convert paths from StagePathStr to plain str, needed for UDTF-based XML reader
    paths = [str(p) for p in paths]
    paths = [p[1:-1] if p.startswith("'") and p.endswith("'") else p for p in paths]

    try:
        df = reader.xml(paths[0])
        for p in paths[1:]:
            df = df.union_all_by_name(reader.xml(p), allow_missing_columns=True)

        # [SPARK PARITY] Transform data to match user schema and case sensitivity
        df = _apply_user_schema(df, schema)

    except SnowparkDataframeReaderException as e:
        # [SPARK PARITY] Return empty DataFrame if rowTag not found
        if "Cannot find the row tag" in str(e):
            logger.info(
                f"XML reader: rowTag '{row_tag}' not found, returning empty DataFrame"
            )
            df = _create_empty_dataframe_with_schema(schema, session)
        else:
            raise

    spark_column_names = get_spark_column_names_from_snowpark_columns(df.columns)
    renamed_df, snowpark_column_names = rename_columns_as_snowflake_standard(
        df, rel.common.plan_id
    )
    snowpark_column_types = [emulate_integral_types(f.datatype) for f in schema.fields]

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


def _apply_user_schema(
    snowpark_df: snowpark.DataFrame,
    user_schema: StructType,
) -> snowpark.DataFrame:
    """
    Cast Snowpark XML output to match user-provided Spark schema:
    - Maps Snowpark column names to user schema field names
    - Applies case-sensitive matching where missing columns become NULL
    - Normalizes single-element arrays
    """
    snowpark_columns = set(snowpark_df.columns)
    select_exprs = []

    for field in user_schema.fields:
        field_name = unquote_if_quoted(field.name)
        snowpark_col = f"\"'{field_name}'\""

        # [SPARK PARITY] Case-sensitive matching - return NULL if column doesn't exist
        if snowpark_col not in snowpark_columns:
            sf_type = convert_sp_to_sf_type(field.datatype)
            select_exprs.append(sql_expr(f"NULL::{sf_type}").alias(f'"{field_name}"'))
            continue

        normalized = _normalize_single_element_arrays(snowpark_col, field.datatype)
        sf_type = convert_sp_to_sf_type(field.datatype)
        select_exprs.append(
            sql_expr(f"({normalized})::{sf_type}").alias(f'"{field_name}"')
        )

    return snowpark_df.select(*select_exprs)


def _normalize_single_element_arrays(col_path: str, datatype: DataType) -> str:
    """
    This function wraps single-element objects in ARRAY_CONSTRUCT where schema expects arrays.
    Uses recursive descent to handle nested structures.

    Args:
        col_path: SQL path to column (e.g., 'reviews' or 'reviews:review')
        datatype: Expected datatype from user schema

    Returns:
        SQL expression string with array normalization applied where needed

    Note:
    - OBJECT_CONSTRUCT returns OBJECT type, which CANNOT cast to structured OBJECT(...)
    - OBJECT_CONSTRUCT_KEEP_NULL(...)::VARIANT returns VARIANT, which CAN cast to structured types
    """
    if isinstance(datatype, ArrayType):
        return f"IFF(IS_ARRAY({col_path}), {col_path}, ARRAY_CONSTRUCT({col_path}))"

    elif isinstance(datatype, StructType):
        # Rebuild struct with OBJECT_CONSTRUCT_KEEP_NULL for proper casting
        field_exprs = []
        for field in datatype.fields:
            field_name = unquote_if_quoted(field.name)
            nested_path = f"{col_path}['{field_name}']"
            normalized = _normalize_single_element_arrays(nested_path, field.datatype)
            field_exprs.append(f"'{field_name}', {normalized}")
        # ::VARIANT suffix is KEY - allows casting to structured OBJECT(...)
        reconstructed = f"OBJECT_CONSTRUCT_KEEP_NULL({', '.join(field_exprs)})::VARIANT"
        # [SPARK PARITY] Preserve NULL if original struct is NULL (element missing in XML)
        return f"IFF({col_path} IS NULL, NULL, {reconstructed})"

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
                f'"{unquote_if_quoted(field.name)}"',
                field.datatype,
                field.nullable,
            )
            for field in schema.fields
        ],
        structured=schema.structured,
    )
