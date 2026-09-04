#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy
import os
import shutil
import uuid
from collections.abc import Callable, Iterable
from contextlib import suppress
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq
import pyspark.sql.connect.proto.base_pb2 as proto_base
import pyspark.sql.connect.proto.commands_pb2 as commands_proto
import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.relations_pb2 as relation_proto
from pyspark.errors.exceptions.base import AnalysisException
from pyspark.errors.exceptions.connect import IllegalArgumentException

from snowflake import snowpark
from snowflake.snowpark import Window
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.functions import (
    col,
    lit,
    object_construct,
    object_construct_keep_null,
    random,
    row_number,
    when,
)
from snowflake.snowpark.types import (
    ArrayType,
    BinaryType,
    BooleanType,
    ByteType,
    DataType,
    DateType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    MapType,
    ShortType,
    StringType,
    StructField,
    StructType,
    TimestampType,
    TimeType,
    VariantType,
    _NumericType,
)
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import (
    SessionConfig,
    get_iceberg_target_file_size_for_writes,
    get_parquet_metadata_generation_enabled,
    get_success_file_generation_enabled,
    global_config,
    is_column_nullability_tracking_enabled,
    raise_if_unsupported_data_source,
    sessions_config,
    str_to_bool,
)
from snowflake.snowpark_connect.constants import SPARK_VERSION
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.integral_types_support import (
    _overflow_guard_needed,
    apply_integral_overflow_with_ansi_check,
)
from snowflake.snowpark_connect.expression.map_expression import map_expression
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.relation.iceberg_branch_dml import (
    IcebergRefDmlTarget,
    append_dataframe_to_ref_dml_target,
    overwrite_dataframe_to_ref_dml_target,
    overwrite_partitions_dataframe_to_ref_dml_target,
    reject_ref_dml_table_creation,
    resolve_iceberg_ref_dml_target,
)
from snowflake.snowpark_connect.relation.io_utils import (
    convert_file_prefix_path,
    get_compression_for_source_and_options,
    is_cloud_path,
)
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.neo4j_utils import (
    transform_neo4j_to_jdbc_options,
)
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_internal_columns,
)
from snowflake.snowpark_connect.relation.read.reader_config import (
    CsvWriterConfig,
    validate_json_charset_name,
)
from snowflake.snowpark_connect.relation.stage_locator import get_paths_from_stage
from snowflake.snowpark_connect.relation.utils import (
    assert_sf_connector_auth_options_match,
    assert_sf_connector_warehouse_matches,
    comparable_col_name,
    generate_spark_compatible_filename,
    qualify_dbtable_with_sf_options,
    random_string,
)
from snowflake.snowpark_connect.type_mapping import (
    map_pyspark_types_to_pyarrow_types,
    map_snowpark_to_pyspark_types,
    snowpark_to_iceberg_type,
)
from snowflake.snowpark_connect.type_support import is_integral_types_conversion_enabled
from snowflake.snowpark_connect.utils.context import (
    get_spark_session_id,
    should_skip_file_read_cache_result,
)
from snowflake.snowpark_connect.utils.iceberg_partition_utils import (
    V2PartitionSpec,
    build_iceberg_partition_exprs,
    parse_v2_partition_specs,
    render_partition_transform,
    resolve_v2_partition_specs,
)
from snowflake.snowpark_connect.utils.identifiers import (
    is_in_cld_context,
    should_use_cld_identifier_rules,
    spark_multipart_name_to_snowflake,
    spark_to_sf_single_id,
    split_fully_qualified_spark_name,
)
from snowflake.snowpark_connect.utils.io_utils import (
    PartitionSpec,
    get_overwrite_condition,
    get_partition_spec,
    get_table_type,
    get_transform_overwrite_condition,
)
from snowflake.snowpark_connect.utils.schema_utils import force_nullable_schema
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.sql_quoting import escape_sql_comment
from snowflake.snowpark_connect.utils.table_metadata_cache import (
    get_or_create_table_metadata_cache,
)
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
    telemetry,
)
from snowflake.snowpark_connect.utils.udf_cache import register_cached_sproc

_column_order_for_write = "name"

# Available values for TARGET_FILE_SIZE
#   reference:https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table
TARGET_FILE_SIZE_ACCEPTABLE_VALUES = ("AUTO", "16MB", "32MB", "64MB", "128MB")

_FILE_READ_FORMATS = frozenset(("parquet", "csv", "json", "text"))

# Iceberg format version supported by Snowflake
_SUPPORTED_ICEBERG_FORMAT_VERSIONS = (1, 2, 3)
# Milliseconds per day
_MS_PER_DAY = 86_400_000


def _input_is_file_read(rel: relation_proto.Relation) -> bool:
    """
    Return True when `rel` is a data-source read of a local/staged file. This currently only checks the
    direct child of this relation, and returns False if a read occurs deeper within a query plan.
    """
    if (
        rel.WhichOneof("rel_type") != "read"
        or rel.read.WhichOneof("read_type") != "data_source"
    ):
        return False
    fmt = rel.read.data_source.format if rel.read.data_source.HasField("format") else ""
    return fmt.lower() in _FILE_READ_FORMATS


# TODO: We will revise/refactor this after changes for all formats are finalized.
def clean_params(params):
    """
    Clean params for write operation. This, for now, allows us to use the same parameter code that
    read operations use.
    """
    # INFER_SCHEMA does not apply to writes
    if "INFER_SCHEMA" in params["format_type_options"]:
        del params["format_type_options"]["INFER_SCHEMA"]


def get_param_from_options(
    params,
    options,
    source,
    *,
    should_write_to_single_file: bool = False,
    has_partitioning_columns: bool = False,
):
    match source:
        case "csv":
            config = CsvWriterConfig(options)
            snowpark_args = config.convert_to_snowpark_args()

            if "header" in options:
                params["header"] = str_to_bool(options["header"])
            params["single"] = False

            params["format_type_options"] = snowpark_args
            clean_params(params)
        case "json":
            params["format_type_options"]["FILE_EXTENSION"] = source
            # SPARK-23723: validate the user-supplied JSON write encoding
            # eagerly so the caller sees a fast, actionable error
            # (UnsupportedCharsetException for unknown names like "UTF-128")
            # instead of a silent fallback to UTF-8 inside Snowflake's COPY
            # INTO. We do NOT enforce the read-only SPARK-24190 multiLine
            # denyList — that restriction is a property of line-by-line JSON
            # parsing and has no meaning on the write path.
            #
            # Snowflake's JSON unload (COPY INTO LOCATION TYPE=JSON) does not
            # expose an encoding/charset option: per the docs, "for unloading
            # data, UTF-8 is the only supported character set". When the user
            # asks for anything else we accept the request (after validation)
            # but log a clear warning so they know the on-disk bytes will be
            # UTF-8 regardless. The Snowflake-side gap (lack of a JSON unload
            # ENCODING formatTypeOption) is tracked under the JSON OSS IO
            # Test Coverage Gap epic SNOW-3246417; that's the parent epic
            # this PR contributes to and is the right place to surface the
            # server gap to the Snowflake unload team.
            if "encoding" in options:
                canonical = validate_json_charset_name(options["encoding"])
                # validate_json_charset_name returns codecs.lookup(...).name.upper(),
                # which canonicalises every UTF-8 alias ("UTF-8", "UTF8", "utf_8",
                # "U8", "cp65001", ...) to the single string "UTF-8", so a plain
                # equality check is sufficient.
                if canonical != "UTF-8":
                    logger.warning(
                        "JSON write encoding=%r requested but Snowflake's JSON "
                        "unload only emits UTF-8 (see Snowflake COPY INTO "
                        "LOCATION docs). The output files will be UTF-8 "
                        "encoded; the encoding option has been validated but "
                        "is otherwise a no-op on write.",
                        canonical,
                    )
        case "parquet":
            params["header"] = True
        case "text":
            config = CsvWriterConfig(options)
            params["format_type_options"]["FILE_EXTENSION"] = "txt"
            params["format_type_options"]["ESCAPE_UNENCLOSED_FIELD"] = "NONE"
            # Handle both camelCase (lineSep) and lowercase (linesep) option names
            if "lineSep" in options or "linesep" in options:
                params["format_type_options"]["RECORD_DELIMITER"] = config.get(
                    "linesep"
                )

    # Respect single-file intent across all supported file formats.
    # For CSV we default to single=False above, then override here when needed.
    if should_write_to_single_file and not has_partitioning_columns:
        params["single"] = True

    if (
        source in ("csv", "parquet", "json") and "nullValue" in options
    ):  # TODO: Null value handling if not specified
        params["format_type_options"]["NULL_IF"] = options["nullValue"]


def _spark_to_snowflake(multipart_id: str) -> str:
    if should_use_cld_identifier_rules():
        return spark_multipart_name_to_snowflake(multipart_id)
    return ".".join(
        spark_to_sf_single_id(part)
        for part in split_fully_qualified_spark_name(multipart_id)
    )


def _validate_table_exist_and_of_type(
    snowpark_table_name: str,
    session: snowpark.Session,
    table_type: str,
    table_schema_or_error: DataType | SnowparkSQLException,
) -> None:
    if not isinstance(table_schema_or_error, DataType):
        exception = AnalysisException(
            f"[TABLE_OR_VIEW_NOT_FOUND] The table or view `{snowpark_table_name}` cannot be found."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception
    _validate_table_type(snowpark_table_name, session, table_type)


def _validate_table_type(
    snowpark_table_name: str,
    session: snowpark.Session,
    table_type: str,
) -> None:
    actual_type = get_table_type(snowpark_table_name, session)
    if table_type == "iceberg":
        if actual_type not in ("ICEBERG", "TABLE"):
            exception = AnalysisException(
                f"Table {snowpark_table_name} is not an iceberg table"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
    elif table_type == "fdn":
        if actual_type not in ("NORMAL", "TABLE"):
            exception = AnalysisException(
                f"Table {snowpark_table_name} is not a FDN table"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
    else:
        raise ValueError(
            f"Invalid table_type: {table_type}. Must be 'iceberg' or 'fdn'"
        )


def _is_create_table_mode_v2(mode: commands_proto.WriteOperationV2.Mode) -> bool:
    # Modes where Spark forwards .using(provider) to the writer.
    return mode in (
        commands_proto.WriteOperationV2.MODE_CREATE,
        commands_proto.WriteOperationV2.MODE_REPLACE,
        commands_proto.WriteOperationV2.MODE_CREATE_OR_REPLACE,
    )


def _is_existing_write_table_mode_v2(
    mode: commands_proto.WriteOperationV2.Mode,
) -> bool:
    # These valid iceberg write modes inferred from the catalog
    return mode in (
        commands_proto.WriteOperationV2.MODE_APPEND,
        commands_proto.WriteOperationV2.MODE_OVERWRITE,
        commands_proto.WriteOperationV2.MODE_OVERWRITE_PARTITIONS,
        commands_proto.WriteOperationV2.MODE_REPLACE,
        commands_proto.WriteOperationV2.MODE_CREATE_OR_REPLACE,
    )


def _is_iceberg_write_v2_target(
    session: snowpark.Session,
    snowpark_table_name: str,
    provider: str,
    mode: commands_proto.WriteOperationV2.Mode,
    is_cld: bool,
) -> bool:
    # Spark only honors the .using(provider) hint for the create-family modes.
    # Its Connect server threads `writeOperation.getProvider` through to
    # `w.using(...)` solely for MODE_CREATE / MODE_REPLACE / MODE_CREATE_OR_REPLACE
    # (SparkConnectPlanner.handleWriteOperationV2, SparkConnectPlanner.scala:2773-2796);
    # for MODE_APPEND / MODE_OVERWRITE / MODE_OVERWRITE_PARTITIONS the provider is
    # dropped, and the core DataFrameWriterV2 never reads it on those paths
    # (DataFrameWriterV2.scala:149-193 — only create()/internalReplace() consult it).
    # So for the pure mutations the existing table's catalog type is authoritative,
    # and a contradictory .using("iceberg") on an FDN table must NOT force iceberg.
    if provider.lower() == "iceberg" and _is_create_table_mode_v2(mode):
        return True
    if not _is_existing_write_table_mode_v2(mode):
        return False
    if is_cld:
        return True
    return get_table_type(snowpark_table_name, session) == "ICEBERG"


def _write_v2_dml_routing(
    dml_target: IcebergRefDmlTarget,
    *,
    is_iceberg: bool,
) -> tuple[str, bool]:
    """Return Snowpark table SQL and branch-DML flag for writeTo V2.

    Session ``spark.wap.branch`` resolves to ``AT (BRANCH => ...)`` during target
    resolution, but Spark applies WAP only on Iceberg tables. FDN writes keep the
    base table name and skip branch DML helpers.
    """
    snowpark_table_name = (
        dml_target.base_snowflake_sql
        if not is_iceberg
        else dml_target.dml_snowflake_sql
    )
    use_branch_dml = is_iceberg and dml_target.uses_branch_dml
    return snowpark_table_name, use_branch_dml


def _iceberg_write_col_key(name: str) -> str:
    """Column name key for Iceberg merge matching (see _validate_schema_for_append)."""
    raw = name.upper() if not global_config.spark_sql_caseSensitive else name
    return unquote_if_quoted(raw)


def _iceberg_merge_schema_enabled(
    options: dict[str, str], session_config: SessionConfig
) -> bool:
    """Resolve mergeSchema from write options or Spark session config."""
    for k, v in options.items():
        # Normalize to bare lowercase so all variants match:
        # "mergeSchema", "merge-schema", "merge_schema", "MERGESCHEMA", etc.
        kl = k.lower().replace("-", "").replace("_", "")
        if kl == "mergeschema":
            return str_to_bool(str(v))
    return str_to_bool(session_config.get("spark.sql.iceberg.merge-schema", "false"))


def _session_config_for_write() -> SessionConfig:
    return sessions_config[get_spark_session_id()]


def _alter_iceberg_add_column(
    session: snowpark.Session,
    snowpark_table_name: str,
    field: StructField,
) -> None:
    """Run ALTER ICEBERG TABLE ... ADD COLUMN IF NOT EXISTS for one column."""
    col_sql = quote_name_without_upper_casing(unquote_if_quoted(field.name))
    iceberg_t = snowpark_to_iceberg_type(field.datatype)
    stmt = (
        f"ALTER ICEBERG TABLE {snowpark_table_name} "
        f"ADD COLUMN IF NOT EXISTS {col_sql} {iceberg_t}"
    )
    try:
        result = session.sql(stmt).collect()
        logger.info(
            "Iceberg schema evolution: added column %s %s to %s — result: %s",
            col_sql,
            iceberg_t,
            snowpark_table_name,
            result,
        )
    except SnowparkSQLException as e:
        exc = AnalysisException(
            "Iceberg mergeSchema could not add columns to the table (often "
            "external-catalog or permission restrictions). Evolve the Iceberg "
            f"schema in the catalog or use a Snowflake-managed Iceberg table. "
            f"Underlying error: {e.message}"
        )
        attach_custom_error_code(exc, ErrorCodes.INVALID_OPERATION)
        raise exc from e


def _raise_optional_into_required(
    data_field_name: str, table_field_name: str, snowpark_table_name: str
) -> None:
    """Mirror Iceberg: writing an optional (nullable) source into a required target."""
    exception = AnalysisException(
        f"[INCOMPATIBLE_DATA_FOR_TABLE.NULLABLE_COLUMN_OR_FIELD] "
        f"Cannot write incompatible dataset to table with schema "
        f"{snowpark_table_name}: "
        f"Cannot write optional field '{data_field_name}' to required "
        f"(non-nullable) field '{table_field_name}'."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
    raise exception


def _raise_missing_required(table_field_name: str, snowpark_table_name: str) -> None:
    """Mirror Iceberg: a required target column absent from the source schema."""
    exception = AnalysisException(
        f"[INCOMPATIBLE_DATA_FOR_TABLE.CANNOT_FIND_DATA] "
        f"Cannot write incompatible data for the table {snowpark_table_name}: "
        f"Cannot find data for the required (non-nullable) output column "
        f"'{table_field_name}'."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
    raise exception


def _evolve_iceberg_schema_if_needed(
    session: snowpark.Session,
    snowpark_table_name: str,
    table_struct: StructType,
    input_df: snowpark.DataFrame,
    check_nullability: bool,
    check_ordering: bool,
) -> snowpark.DataFrame:
    """Merge-aware Iceberg schema: validate overlaps, ALTER new columns, pad missing columns.

    Validates the source against the target BEFORE any ALTER, so a rejected write
    leaves the table untouched (mirrors Iceberg's validateOrMergeWriteSchema).
    check_nullability has no default so every caller opts in explicitly; V1
    passes False.

    When ``check_ordering`` is True, the data's original column order is
    validated against the *computed* merged schema (existing table columns
    followed by newly added columns) BEFORE any ALTER runs, so an out-of-order
    write is rejected without mutating the table — matching Iceberg, where the
    ordering check fires even under mergeSchema.

    ``check_ordering`` is required (no default) so every caller makes an explicit
    choice: the V2 writer passes the value resolved via
    ``_resolve_iceberg_check_ordering`` (public default True, per Iceberg's
    ``check-ordering``), while the V1 path passes False until it resolves the
    option itself.
    """
    data_struct = input_df.schema
    table_by_key = {comparable_col_name(f.name): f for f in table_struct.fields}
    data_by_key = {comparable_col_name(f.name): f for f in data_struct.fields}

    new_keys = set(data_by_key) - set(table_by_key)
    shared_keys = set(table_by_key) & set(data_by_key)
    missing_keys = set(table_by_key) - set(data_by_key)

    # Validate before ALTER so a failure never half-evolves the table.
    for k in shared_keys:
        t_field = table_by_key[k]
        d_field = data_by_key[k]
        if check_nullability and not t_field.nullable and d_field.nullable:
            _raise_optional_into_required(
                d_field.name, t_field.name, snowpark_table_name
            )
        t_dt = t_field.datatype
        d_dt = d_field.datatype
        _validate_schema_for_append(
            t_dt,
            d_dt,
            snowpark_table_name,
            compare_structs=isinstance(t_dt, StructType)
            and isinstance(d_dt, StructType),
            check_nullability=check_nullability,
            check_ordering=check_ordering,
        )

    # Validate ordering against the merged schema before mutating the table.
    # ALTER ... ADD COLUMN appends new columns at the end, so the merged order
    # is the existing table columns followed by the new columns in data order.
    if check_ordering:
        new_fields_in_data_order = [
            f for f in data_struct.fields if comparable_col_name(f.name) in new_keys
        ]
        merged_fields = list(table_struct.fields) + new_fields_in_data_order
        _check_top_level_field_ordering(
            merged_fields,
            data_struct.fields,
            snowpark_table_name,
            comparable_col_name,
        )

    # Top-level only; nested required fields omitted from source are not caught
    # here (nullable→required below does recurse). Minor asymmetry vs Spark.
    # Also over-rejects required cols with Iceberg write-defaults: StructField
    # doesn't expose them, so we can't tell "fill default" from "missing required".
    if check_nullability:
        for k in missing_keys:
            if not table_by_key[k].nullable:
                _raise_missing_required(table_by_key[k].name, snowpark_table_name)

    for k in new_keys:
        _alter_iceberg_add_column(session, snowpark_table_name, data_by_key[k])

    # Prefer the live schema from Snowflake: it has the correct stored identifier
    # format (e.g. unquoted "AGE" for managed tables vs quoted '"age"' for CLD).
    # Fall back to manual construction only when the fetch returns an empty
    # StructType, which happens for CLD (catalog-linked) tables where Snowpark
    # cannot lazily introspect the external-catalog schema.
    refreshed = session.table(snowpark_table_name).schema
    if not isinstance(refreshed, StructType) or not refreshed.fields:
        # CLD fallback: build from the known original fields + newly added fields.
        # ALTER TABLE ADD COLUMN appends at the end; names are quoted the same
        # way _alter_iceberg_add_column used so identifiers match Snowflake's.
        if new_keys:
            new_struct_fields = [
                StructField(
                    quote_name_without_upper_casing(
                        unquote_if_quoted(data_by_key[k].name)
                    ),
                    data_by_key[k].datatype,
                    data_by_key[k].nullable,
                )
                for k in new_keys
            ]
            refreshed = StructType(list(table_struct.fields) + new_struct_fields)
        else:
            refreshed = table_struct

    select_cols: list[snowpark.Column] = []
    for table_field in refreshed.fields:
        key = comparable_col_name(table_field.name)
        if key in data_by_key:
            df_field = data_by_key[key]
            src = df_field.name
            cast_col = _build_cast_column(
                col(src),
                df_field.datatype,
                table_field.datatype,
                rename_fields=not global_config.spark_sql_caseSensitive,
            )
            select_cols.append(cast_col.alias(table_field.name))
        else:
            select_cols.append(
                lit(None).cast(table_field.datatype).alias(table_field.name)
            )

    return input_df.select(select_cols)


def _prepare_iceberg_write_dataframe(
    session: snowpark.Session,
    input_df: snowpark.DataFrame,
    snowpark_table_name: str,
    table_schema_or_error: DataType | SnowparkSQLException | None,
    merge_schema: bool,
    check_nullability: bool,
    check_ordering: bool,
) -> tuple[snowpark.DataFrame, DataType | SnowparkSQLException | None]:
    """Evolve Iceberg schema if mergeSchema is enabled, return (df, refreshed_schema).

    check_nullability has no default so every caller opts in explicitly; V1
    passes False.

    ``check_ordering`` is required (no default) so every caller makes an explicit
    choice: the V2 writer passes the value resolved via
    ``_resolve_iceberg_check_ordering`` (public default True), while the V1 path
    passes False until it resolves the option itself.
    """
    if not merge_schema or not isinstance(table_schema_or_error, StructType):
        return input_df, table_schema_or_error
    evolved_df = _evolve_iceberg_schema_if_needed(
        session,
        snowpark_table_name,
        table_schema_or_error,
        input_df,
        check_nullability=check_nullability,
        check_ordering=check_ordering,
    )
    # Use the evolved DataFrame's schema as the refreshed schema rather than
    # re-fetching from Snowflake: session.table(name).schema returns an empty
    # StructType for CLD (catalog-linked) tables, and evolved_df.schema is
    # already correct by construction from _evolve_iceberg_schema_if_needed.
    # It's already reshaped to the table, so the caller's re-validation is a
    # no-op (nullability was checked pre-ALTER).
    return evolved_df, evolved_df.schema


def _validate_table_does_not_exist(
    snowpark_table_name: str,
    table_schema_or_error: DataType | SnowparkSQLException,
) -> None:
    if isinstance(table_schema_or_error, DataType):
        exception = AnalysisException(f"Table {snowpark_table_name} already exists")
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception


def _infer_dynamic_partition_cols_from_spec(
    spec_col_names: list[str],
    spark_column_names: list[str],
    case_sensitive: bool,
) -> list[str] | None:
    """Resolve partition columns for a dynamic-partition overwrite when the
    user did not call ``.partitionBy(...)``.

    Returns the matched DataFrame-side column names if **all** spec columns
    can be matched to the input DataFrame, otherwise ``None``. The caller
    is expected to surface a clear error when ``None`` is returned, rather
    than letting it propagate to ``get_snowpark_column_names_from_spark_column_names``
    (which would crash with ``TypeError: 'NoneType' object is not iterable``,
    SNOW-3471809).
    """
    matched_cols: list[str] = []
    if case_sensitive:
        df_cols_set = set(spark_column_names)
        for spec_col in spec_col_names:
            if spec_col in df_cols_set:
                matched_cols.append(spec_col)
    else:
        df_cols_lower = {c.lower(): c for c in spark_column_names}
        for spec_col in spec_col_names:
            lower_name = spec_col.lower()
            if lower_name in df_cols_lower:
                matched_cols.append(df_cols_lower[lower_name])

    if matched_cols and len(matched_cols) == len(spec_col_names):
        return matched_cols
    return None


def _validate_partition_columns_match_spec(
    partition_cols: list[str],
    table_partition_spec: PartitionSpec,
) -> None:
    """
    Checks if all given partition_columns are present in the partition_spec.
    All columns from the spec should be in partition_cols, in the same order.
    """
    if table_partition_spec is None:
        if partition_cols:
            exception = IllegalArgumentException(
                "The provided partitioning does not match the table partitioning: "
                f"provided [{', '.join(partition_cols)}] but table has no partition columns."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        return

    table_partition_cols = [
        spark_to_sf_single_id(unquote_if_quoted(c), is_column=True)
        for c in table_partition_spec.columns()
    ]
    provided_partition_cols = [
        spark_to_sf_single_id(unquote_if_quoted(c), is_column=True)
        for c in partition_cols
    ]

    if should_use_cld_identifier_rules():
        partition_cols_match = [c.lower() for c in provided_partition_cols] == [
            c.lower() for c in table_partition_cols
        ]
    else:
        partition_cols_match = provided_partition_cols == table_partition_cols
    if not partition_cols_match:
        exception = IllegalArgumentException(
            "The provided partitioning does not match the table partitioning: "
            f"provided [{', '.join(partition_cols)}] vs table [{', '.join(table_partition_spec.columns())}]."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception


def _validate_no_partition_cols_on_fdn(
    partitioning_columns: Iterable[expressions_proto.Expression],
    snowpark_table_name: str | None = None,
    actual_type: str | None = None,
) -> None:
    """Reject ``partitionedBy`` on standard (FDN) Snowflake tables.

    FDN tables have no user-defined partitioning — Snowflake auto-organizes
    rows into micro-partitions — so a Spark partition spec has no equivalent.
    We raise instead of silently ignoring so users don't assume a partition
    layout that was never applied.

    Applied uniformly across every DataFrameWriterV2 mode. Previously only
    MODE_CREATE_OR_REPLACE rejected this while create / replace / append /
    overwrite silently ignored it; rejecting everywhere makes the behavior
    consistent (SNOW-3406172, Make DataFrameWriterV2 Spark-compatible).
    Iceberg targets support partitioning and never reach this path.

    ``partitioning_columns`` is the raw ``WriteOperationV2.partitioning_columns``
    proto field; we only test it for emptiness, so identity columns and
    transform expressions (``days(col)``, etc.) are rejected alike.

    When ``actual_type`` is the unresolved ``"TABLE"`` sentinel (a target the
    current role cannot see, misclassified as FDN — SNOW-3813783) we append an
    access hint; confirmed FDN/standard tables keep the bare message.
    """
    if partitioning_columns:
        message = "Standard Snowflake tables do not support partition columns"
        if actual_type == "TABLE":
            table_ref = f" '{snowpark_table_name}'" if snowpark_table_name else ""
            message += (
                f". If{table_ref or ' the target'} is an Iceberg table, ensure the "
                "current role has access to it (USAGE on the database and schema, "
                "and a privilege such as SELECT on the table)"
            )
        exception = SnowparkConnectNotImplementedError(message)
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception


def map_write(request: proto_base.ExecutePlanRequest):
    write_op = request.plan.command.write_operation
    # SNOW-3917754: reject an unsupported format (e.g. .format("delta")) before any
    # planning or IO-write telemetry, so rejected writes don't skew adoption metrics.
    raise_if_unsupported_data_source(write_op.source, get_or_create_snowpark_session())
    telemetry.report_io_write(write_op.source, dict(write_op.options))
    if write_op.path and write_op.options.get("path"):
        raise AnalysisException(
            "There is a 'path' option set and save() is called with a path parameter. "
            "Either remove the path option, or call save() without the parameter."
        )

    write_mode = None
    match write_op.mode:
        case commands_proto.WriteOperation.SaveMode.SAVE_MODE_APPEND:
            write_mode = "append"
        case commands_proto.WriteOperation.SaveMode.SAVE_MODE_ERROR_IF_EXISTS:
            write_mode = "errorifexists"
        case commands_proto.WriteOperation.SaveMode.SAVE_MODE_OVERWRITE:
            # the dataframe API doesn't seem to respect spark.sql.sources.partitionOverwriteMode
            # overwrite-mode is used instead
            overwrite_mode = write_op.options.get("overwrite-mode", "static")
            if overwrite_mode.lower() == "dynamic" and write_op.source == "iceberg":
                # Dynamic partition overwrite - partition columns will be inferred
                # from the table spec if not explicitly provided via partitionBy()
                write_mode = "overwrite_partitions"
            elif (
                write_op.options.get("truncate", "").lower() == "true"
                or write_op.options.get("truncate_table", "").lower() == "on"
            ):
                # Opt-in via `.option("truncate", "true")` (Spark JDBC convention, value
                # follows Boolean.parseBoolean — "true"/"false") or
                # `.option("truncate_table", "ON")` (Spark-Snowflake connector
                # convention, value is "ON"/"OFF"): TRUNCATE + INSERT to preserve table
                # identity (grants, comments, policies, tags, dependencies).
                write_mode = "truncate"
            else:
                write_mode = "overwrite"
        case commands_proto.WriteOperation.SaveMode.SAVE_MODE_IGNORE:
            write_mode = "ignore"

    # Set a context flag to indicate to a nested file read operation whether it should materialize
    # to a temp table with cache_result. If the write operation currently being processed is trying to save
    # to a table already, then we can skip the temp table CTAS. See SNOW-3262791 for details.
    with should_skip_file_read_cache_result(
        write_op.HasField("table") and _input_is_file_read(write_op.input)
    ):
        # Drop both internal scaffolding (__DUMMY) and qualified-access-only metadata
        # (USING-join source columns) before writing — neither is part of the visible
        # schema. SNOW-2443454.
        result = map_relation(write_op.input).without_hidden_columns()
    (
        input_df,
        snowpark_column_names,
        spark_column_names,
        qualifiers,
    ) = handle_column_names(result, write_op.source)

    # Create updated container with transformed dataframe, then filter METADATA$FILENAME columns
    updated_result = DataFrameContainer.create_with_column_mapping(
        dataframe=input_df,
        spark_column_names=spark_column_names,
        snowpark_column_names=snowpark_column_names,
        column_metadata=result.column_map.column_metadata,
        column_qualifiers=qualifiers,
        parent_column_name_map=result.column_map.get_parent_column_name_map(),
        table_name=result.table_name,
        alias=result.alias,
        partition_hint=result.partition_hint,
    )
    updated_result = without_internal_columns(updated_result)
    input_df = updated_result.dataframe

    session: snowpark.Session = get_or_create_snowpark_session()

    # Check for partition hint early to determine precedence over single option
    partition_hint = (
        result.partition_hint if hasattr(result, "partition_hint") else None
    )

    # Snowflake saveAsTable doesn't support format
    if (
        write_op.HasField("table")
        and write_op.HasField("source")
        and write_op.source in _FILE_READ_FORMATS
    ):
        write_op.source = ""

    normalized_write_options = {k.lower(): v for k, v in write_op.options.items()}
    # `replaceWhere` is intentionally ignored for non-Delta file formats to match
    # OSS Spark behavior (see tests/expectation_tests/test_repro_snow_3295590.py,
    # JIRA SNOW-3295590).
    user_set_single_option = "single" in normalized_write_options
    should_write_to_single_file = str_to_bool(
        normalized_write_options.get("single", "false")
    )
    user_set_max_file_size_option = (
        "snowflake_max_file_size" in normalized_write_options
    )
    force_single_for_coalesce_one = (
        partition_hint == 1
        and not write_op.partitioning_columns
        and not user_set_single_option
        and not user_set_max_file_size_option
    )
    if force_single_for_coalesce_one:
        # Spark users commonly expect coalesce(1).write(...) to produce one file.
        # Apply this only for non-partitioned writes, and only when users did not
        # explicitly provide single/max-file-size options.
        should_write_to_single_file = True

    # Support Snowflake-specific snowflake_max_file_size option. This is NOT a spark option.
    max_file_size = None
    if (
        "snowflake_max_file_size" in normalized_write_options
        and int(normalized_write_options["snowflake_max_file_size"]) > 0
    ):
        max_file_size = int(normalized_write_options["snowflake_max_file_size"])
    elif should_write_to_single_file:
        # providing default size as 1GB for single file write
        max_file_size = 1073741824
    match write_op.source:
        case "csv" | "parquet" | "json" | "text":
            # Text format requires exactly one non-partition column of StringType
            if write_op.source == "text":
                partition_col_names = list(write_op.partitioning_columns)
                snowpark_partition_cols = set(
                    updated_result.column_map.get_snowpark_column_names_from_spark_column_names(
                        partition_col_names
                    )
                )
                snowpark_non_partition_cols = [
                    col
                    for col in updated_result.column_map.get_snowpark_columns()
                    if col not in snowpark_partition_cols
                ]
                # Check for all columns used as partition first (matches Spark error)
                if (
                    len(snowpark_non_partition_cols) == 0
                    and len(partition_col_names) > 0
                ):
                    exception = AnalysisException(
                        "[ALL_PARTITION_COLUMNS_NOT_ALLOWED] Cannot use all columns for partition columns."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                    raise exception
                if len(snowpark_non_partition_cols) != 1:
                    exception = AnalysisException(
                        f"[UNSUPPORTED_DATA_TYPE_FOR_DATASOURCE] Text data source supports "
                        f"only a single column, and you have {len(snowpark_non_partition_cols)} columns."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                    raise exception
                # Get the type of the non-partition column
                text_col_name = unquote_if_quoted(snowpark_non_partition_cols[0])
                col_type = [
                    f
                    for f in input_df.schema.fields
                    if unquote_if_quoted(f.name) == text_col_name
                ][0].datatype
                if not isinstance(col_type, StringType):
                    exception = AnalysisException(
                        f"[UNSUPPORTED_DATA_TYPE_FOR_DATASOURCE] The Text datasource doesn't "
                        f'support the column `{text_col_name}` of the type "{col_type.simpleString().upper()}".'
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                    raise exception

            # TODO: Extend SaveMode.Ignore support to csv, json, and text formats.
            #  The path-existence check logic already implemented for parquet
            #  (see the "ignore" block below) is format-agnostic and can be
            #  reused directly for these formats.
            if write_mode == "ignore" and write_op.source != "parquet":
                exception = SnowparkConnectNotImplementedError(
                    f"Write mode {write_mode} is not supported for {write_op.source}"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception

            if not write_op.path:
                exception = AnalysisException(
                    "path is not specified. Please provide a valid path for the write operation."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception

            write_path = get_paths_from_stage(
                [write_op.path],
                session=session,
            )[0]

            # Handle ignore mode for parquet: if the path already exists,
            # silently skip the write.  Per Spark's SaveMode.Ignore semantics,
            # existing data must not be changed.
            if write_mode == "ignore":
                is_local_path = not is_cloud_path(write_op.path)
                path_exists = False
                if is_local_path:
                    path_exists = os.path.exists(write_op.path) and (
                        os.path.isfile(write_op.path)
                        or (os.path.isdir(write_op.path) and os.listdir(write_op.path))
                    )
                else:
                    with suppress(SnowparkSQLException):
                        list_command = f"LIST '{write_path}/'"
                        result = session.sql(list_command).collect()
                        if result:
                            path_exists = True
                if path_exists:
                    return

            # Handle error/errorifexists mode - check if file exists before writing
            if write_mode in (None, "error", "errorifexists"):
                is_local_path = not is_cloud_path(write_op.path)

                if is_local_path:
                    # Check if local path exists
                    if os.path.exists(write_op.path) and (
                        os.path.isfile(write_op.path)
                        or (os.path.isdir(write_op.path) and os.listdir(write_op.path))
                    ):
                        exception = AnalysisException(
                            f"Path {write_op.path} already exists."
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.INVALID_OPERATION
                        )
                        raise exception
                else:
                    # Check if stage/cloud path exists by listing files
                    # If the path does not exist, SnowparkSQLException is suppressed (expected for error mode).
                    with suppress(SnowparkSQLException):
                        # TODO: Optimize this check by using a more efficient way to check if the path exists.
                        list_command = f"LIST '{write_path}/'"
                        result = session.sql(list_command).collect()
                        if result:
                            exception = AnalysisException(
                                f"Path {write_op.path} already exists."
                            )
                            attach_custom_error_code(
                                exception, ErrorCodes.INVALID_OPERATION
                            )
                            raise exception

            # Generate Spark-compatible filename with proper extension
            extension = write_op.source if write_op.source != "text" else "txt"

            compression = get_compression_for_source_and_options(
                write_op.source, write_op.options, from_read=False
            )
            if compression is not None:
                write_op.options["compression"] = compression

            # Generate Spark-compatible filename or prefix
            # we need a random prefix to support "append" mode
            # otherwise copy into with overwrite=False will fail if the file already exists
            overwrite = (
                write_op.mode
                == commands_proto.WriteOperation.SaveMode.SAVE_MODE_OVERWRITE
            )

            if overwrite:
                # Trailing slash is required as calling remove with just write_path would remove everything in the
                # stage path with the same prefix.

                # SNOW-3477215: Spark's DataFrameWriter lets users override
                # spark.sql.sources.partitionOverwriteMode per-write via
                # .option("partitionOverwriteMode", ...). Honor that here for
                # csv/parquet/json/text; iceberg has its own "overwrite-mode" path above.
                # Note: Keys in normalized_write_options are already lowercased (line 538),
                # and we lowercase the value below, so this is fully case-insensitive.
                per_write_mode = normalized_write_options.get("partitionoverwritemode")
                partition_overwrite_mode = (
                    per_write_mode
                    if per_write_mode is not None
                    else global_config.get(
                        "spark.sql.sources.partitionOverwriteMode", "static"
                    )
                ).lower()
                # Spark only supports "static" and "dynamic"; anything else is invalid.
                if partition_overwrite_mode not in ("static", "dynamic"):
                    exception = IllegalArgumentException(
                        f"Invalid partitionOverwriteMode: '{partition_overwrite_mode}'. "
                        "Supported values are 'static' and 'dynamic'."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
                if (
                    write_op.partitioning_columns
                    and partition_overwrite_mode == "dynamic"
                ):
                    partitioning_columns = write_op.partitioning_columns
                    snowpark_partitioning_columns = [
                        quote_name_without_upper_casing(partition_column)
                        for partition_column in partitioning_columns
                    ]
                    distinct_values = (
                        input_df.select(*snowpark_partitioning_columns)
                        .distinct()
                        .collect()
                    )
                    partition_paths = set()
                    for row in distinct_values:
                        paths = []
                        for key, value in zip(partitioning_columns, row):
                            if value is None:
                                value = "__HIVE_DEFAULT_PARTITION__"
                            paths.append(f"{key}={value}")
                        if paths:
                            partition_paths.add("/".join(paths))

                    for partition_path in partition_paths:
                        # There is no concurrent remove of the directory hence it has to be done sequentially
                        remove_command = (
                            f"REMOVE '{write_path}' PATTERN = '.*/{partition_path}.*'"
                        )
                        session.sql(remove_command).collect()
                        logger.info(
                            f"Successfully cleared partition directory: {write_path}/{partition_path}"
                        )
                else:
                    remove_command = f"REMOVE '{write_path}'"
                    session.sql(remove_command).collect()
                    logger.info(f"Successfully cleared directory: {write_path}")

            # write_path keeps any user-provided trailing "/" intact -- it is
            # required by the REMOVE/LIST commands above (REMOVE is a prefix
            # match, so REMOVE '@stage/path' would also wipe '@stage/path2/').
            # When we *join* a filename onto the location passed to COPY, drop
            # the trailing "/" so we don't emit "@stage/path//file" (SNOW-3566222).
            write_location_base = write_path.rstrip("/")

            if should_write_to_single_file and not write_op.partitioning_columns:
                # Single file: generate complete filename with extension
                spark_filename = generate_spark_compatible_filename(
                    task_id=0,
                    attempt_number=0,
                    compression=compression,
                    format_ext=extension,
                )
                temp_file_prefix_on_stage = f"{write_location_base}/{spark_filename}"
            elif write_op.partitioning_columns:
                # When PARTITION BY is used, Snowflake treats the location as a base
                # directory and creates col=value/ subdirs under it. Appending a
                # filename prefix would create a spurious intermediate folder.
                temp_file_prefix_on_stage = write_path
            else:
                # Multiple files: generate prefix without extension (Snowflake will add extensions)
                spark_filename_prefix = generate_spark_compatible_filename(
                    task_id=0,
                    attempt_number=0,
                    compression=None,
                    format_ext="",  # No extension for prefix
                )
                temp_file_prefix_on_stage = (
                    f"{write_location_base}/{spark_filename_prefix}"
                )

            parameters = {
                "location": temp_file_prefix_on_stage,
                "file_format_type": write_op.source
                if write_op.source != "text"
                else "csv",
                "format_type_options": {
                    "COMPRESSION": compression,
                },
            }
            # Download from the base write path to ensure we fetch whatever Snowflake produced.
            # Using the base avoids coupling to exact filenames/prefixes.
            download_stage_path = write_path

            # Apply max_file_size for both single and multi-file scenarios
            # This helps control when Snowflake splits files into multiple parts
            if max_file_size:
                parameters["max_file_size"] = max_file_size
            rewritten_df: snowpark.DataFrame = rewrite_df(
                input_df, write_op.source, dict(write_op.options)
            )
            get_param_from_options(
                parameters,
                write_op.options,
                write_op.source,
                should_write_to_single_file=should_write_to_single_file,
                has_partitioning_columns=bool(write_op.partitioning_columns),
            )
            if write_op.partitioning_columns:
                # Build Spark-style directory structure: col1=value1/col2=value2/...
                # Example produced expression (Snowflake SQL):
                #   'department=' || TO_VARCHAR("department") || '/' || 'region=' || TO_VARCHAR("region")
                partitioning_column_names = [
                    updated_result.column_map.get_canonical_spark_name(name)
                    for name in write_op.partitioning_columns
                ]

                if (
                    len(
                        set(updated_result.column_map.get_spark_columns())
                        - set(partitioning_column_names)
                    )
                    == 0
                ):
                    exception = AnalysisException(
                        "[ALL_PARTITION_COLUMNS_NOT_ALLOWED] Cannot use all columns for partition columns."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                    raise exception
                partition_expr_parts: list[str] = []
                for col_name in partitioning_column_names:
                    if write_op.source == "json":
                        quoted = f"{rewritten_df.columns[0]}['{col_name}']"
                        segment = f"'{col_name}=' || COALESCE(TO_VARCHAR({quoted}), '__HIVE_DEFAULT_PARTITION__')"
                    else:
                        quoted = f'"{col_name}"'
                        segment = f"'{col_name}=' || COALESCE(TO_VARCHAR({quoted}), '__HIVE_DEFAULT_PARTITION__')"
                    partition_expr_parts.append(segment)
                parameters["partition_by"] = " || '/' || ".join(partition_expr_parts)
                # When using PARTITION BY, Snowflake writes into subdirectories under the base path.
                # Download from the base write path to preserve partition directories locally.
                download_stage_path = write_path

            # When repartition(n) is used WITHOUT partitionBy, split into n COPY INTO calls
            # so we produce n output files with Spark-compatible names.
            # When partitionBy IS active, skip this: Snowflake's PARTITION BY controls
            # the directory layout, and appending per-part prefixes to the location would
            # create spurious intermediate folders. Snowflake already produces ~1 file per
            # partition automatically via its hash-based partitioning logic (one
            # COPY_INTO call -> N output files, one per partition value).
            #
            # SNOW-3389612 Sub-fix A: empty DataFrame + header=true CSV write.
            # Snowflake's `COPY INTO LOCATION` skips empty unloads entirely (no
            # output file), but Spark writes a header-only file. Detect the
            # zero-row case and synthesize the header line directly so the
            # round-trip read sees the schema.
            #
            # Use ``limit(1).count()`` instead of ``count()`` so non-empty
            # writes only round-trip a single bounded query (cheap on any
            # warehouse) rather than running a full aggregate over the
            # entire DataFrame on the hot path.
            empty_csv_header_only_synthesized = False
            if (
                write_op.source == "csv"
                and parameters.get("header") is True
                and not write_op.partitioning_columns
                and rewritten_df.limit(1).count() == 0
            ):
                _write_csv_header_only_file(rewritten_df, session, parameters)
                empty_csv_header_only_synthesized = True

            # partition directory, matching the common repartition(1)+partitionBy idiom.
            repartition_for_writes_enabled = (
                global_config.snowflake_repartition_for_writes
            )
            if empty_csv_header_only_synthesized:
                pass  # header-only file already written above
            elif (
                repartition_for_writes_enabled
                and partition_hint
                and partition_hint > 0
                and not write_op.partitioning_columns
            ):
                # Assign each row a synthetic file number via ROW_NUMBER() over a
                # randomized order, then modulo partition_hint. Using proper Snowpark
                # window functions allows the flattening logic to correctly detect window
                # functions and prevent invalid SQL generation.
                #
                # This MUST be materialized once before the per-file COPYs run. The
                # expression is non-deterministic (ORDER BY RANDOM()), so a lazy DataFrame
                # would make each per-partition COPY statement inline and re-roll an
                # independent assignment (SNOW-3699974):
                #   (1) Correctness: a row's bucket would differ between statements, so the
                #       n filters below would NOT form a partition -- rows get silently
                #       dropped and duplicated (the per-file total still sums to the input
                #       count, so it hides from row-count checks).
                #   (2) Performance: every one of the n COPYs would re-scan and globally
                #       re-sort the entire input.
                # Sorting by the file number clusters the materialized table so each
                # per-file COPY prunes to ~1/n of it. We materialize into an explicit
                # temporary table dropped in a finally (rather than cache_result) so this
                # materialization -- which can be very large -- is released as soon as the
                # unload completes instead of lingering for the whole session lifetime.
                file_num_col = "_sas_file_num"
                materialized_table = random_string(10, "sas_repartition_unload_")
                (
                    rewritten_df.withColumn(
                        file_num_col,
                        row_number().over(Window.order_by(random())) % partition_hint,
                    )
                    .sort(col(file_num_col))
                    .write.save_as_table(materialized_table, table_type="temporary")
                )

                # Since we write per-partition with distinct prefixes, download from the base write path.
                download_stage_path = write_path

                # We need to create a new set of parameters with single=True
                shared_uuid = str(uuid.uuid4())
                part_params = copy.deepcopy(dict(parameters))
                part_params["single"] = True

                try:
                    partitioned_df = session.table(materialized_table)
                    # Submit all per-file COPYs asynchronously (block=False) and then wait,
                    # so the n single-file unloads run concurrently on the warehouse instead
                    # of strictly serially (previously one multi-minute blocking COPY at a
                    # time -- the root cause of the ~hours-long unloads in SNOW-3699974).
                    # The output (exactly n files with Spark-compatible names) is unchanged.
                    async_jobs = []
                    for part_idx in range(partition_hint):
                        # Preserve Spark-like filename prefix per partition so downloaded basenames
                        # match the expected Spark pattern (with possible Snowflake counters appended).
                        per_part_prefix = generate_spark_compatible_filename(
                            task_id=part_idx,
                            attempt_number=0,
                            compression=compression,
                            format_ext=extension,
                            shared_uuid=shared_uuid,
                        )
                        part_params[
                            "location"
                        ] = f"{write_location_base}/{per_part_prefix}"
                        async_jobs.append(
                            partitioned_df.filter(col(file_num_col) == lit(part_idx))
                            .drop(file_num_col)
                            .write.copy_into_location(block=False, **part_params)
                        )
                    # Block until every COPY has finished; the first failure propagates.
                    try:
                        for async_job in async_jobs:
                            async_job.result()
                    except Exception:
                        # On the first failure the remaining COPYs may still be
                        # running. Cancel them before the finally drops the source
                        # table, otherwise in-flight COPYs fail against the dropped
                        # table with noisy "object does not exist" errors.
                        for async_job in async_jobs:
                            with suppress(Exception):
                                async_job.cancel()
                        raise
                finally:
                    session.sql(f"DROP TABLE IF EXISTS {materialized_table}").collect()
            else:
                rewritten_df.write.copy_into_location(**parameters)

            is_local_path = not is_cloud_path(write_op.path)
            if is_local_path:
                store_files_locally(
                    download_stage_path,
                    write_op.path,
                    overwrite,
                    session,
                )

            _generate_metadata_files(
                write_op.source,
                write_op.path,
                download_stage_path,
                input_df.schema,
                session,
                parameters,
                is_local_path,
            )
        case "jdbc":
            from snowflake.snowpark_connect.relation.write.map_write_jdbc import (
                map_write_jdbc,
            )

            options = dict(write_op.options)
            if write_mode is None:
                write_mode = "errorifexists"
            map_write_jdbc(result, session, options, write_mode)
        case "org.neo4j.spark.DataSource":
            from snowflake.snowpark_connect.relation.write.map_write_jdbc import (
                map_write_jdbc,
            )

            options = dict(write_op.options)
            # Transform Neo4j Spark Connector options to JDBC options
            # See neo4j_utils.py for pros/cons of this approach
            jdbc_options = transform_neo4j_to_jdbc_options(options, "write")
            if write_mode is None:
                write_mode = "append"  # Default to append for Neo4j
            map_write_jdbc(result, session, jdbc_options, write_mode)
        case "iceberg":
            table_name = (
                write_op.path
                if write_op.path is not None and write_op.path != ""
                else write_op.table.table_name
            )
            dml_target = resolve_iceberg_ref_dml_target(
                table_name, _spark_to_snowflake, dml_op=write_mode
            )
            snowpark_table_name = dml_target.dml_snowflake_sql
            schema_table_name = dml_target.base_snowflake_sql
            partition_cols = (
                list(write_op.partitioning_columns)
                if write_op.partitioning_columns
                else None
            )
            partition_cols_for_iceberg_config = (
                updated_result.column_map.get_snowpark_column_names_from_spark_column_names(
                    partition_cols
                )
                if partition_cols
                else None
            )
            if (
                partition_cols_for_iceberg_config
                and not global_config.spark_sql_caseSensitive
            ):
                partition_cols_for_iceberg_config = [
                    spark_to_sf_single_id(unquote_if_quoted(c), is_column=True)
                    for c in partition_cols_for_iceberg_config
                ]

            is_cld = is_in_cld_context()
            cld_create_options = dict(write_op.options)
            iceberg_config = _build_iceberg_config(
                options=cld_create_options,
                partition_cols=partition_cols_for_iceberg_config,
                is_cld=is_cld,
            )
            resolved_iceberg_version = (
                iceberg_config.get("iceberg_version") if iceberg_config else None
            )
            session_conf = _session_config_for_write()
            merge_schema = _iceberg_merge_schema_enabled(
                cld_create_options, session_conf
            )

            is_insert_into = (
                write_op.table.save_method
                == commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_INSERT_INTO
            )
            # Fetch once here; all write_mode branches consume it so we avoid
            # a second round-trip in the common case.
            table_schema_or_error = _get_table_schema_or_error(
                schema_table_name, session
            )
            if is_insert_into and not isinstance(table_schema_or_error, DataType):
                # SNOW-3717449: Spark's insertInto requires the target table to
                # already exist; unlike saveAsTable it never creates it. Match
                # Spark's TABLE_OR_VIEW_NOT_FOUND instead of silently creating.
                exception = AnalysisException(
                    f"[TABLE_OR_VIEW_NOT_FOUND] The table or view "
                    f"`{snowpark_table_name}` cannot be found."
                )
                attach_custom_error_code(exception, ErrorCodes.TABLE_NOT_FOUND)
                raise exception

            match write_mode:
                case None | "error" | "errorifexists":
                    if dml_target.has_ref:
                        reject_ref_dml_table_creation(dml_target, "create")
                    _validate_table_does_not_exist(
                        schema_table_name, table_schema_or_error
                    )
                    writer = _get_writer_for_table_creation(input_df)
                    if is_cld:
                        # CLD requires explicit CREATE ICEBERG TABLE syntax.
                        # We must use append mode after table creation because
                        # errorifexists would fail (table now exists).
                        _create_cld_iceberg_table(
                            session,
                            writer._dataframe,
                            schema_table_name,
                            options=cld_create_options,
                            partition_cols=partition_cols_for_iceberg_config,
                            iceberg_version=resolved_iceberg_version,
                        )
                        writer.saveAsTable(
                            table_name=schema_table_name,
                            mode="append",
                            column_order=_column_order_for_write,
                            table_exists=True,
                        )
                    else:
                        writer.saveAsTable(
                            table_name=schema_table_name,
                            mode="errorifexists",
                            column_order=_column_order_for_write,
                            iceberg_config=iceberg_config,
                        )
                case "append":
                    if isinstance(table_schema_or_error, DataType):  # Table exists
                        _validate_table_type(schema_table_name, session, "iceberg")
                    elif dml_target.has_ref:
                        reject_ref_dml_table_creation(dml_target, "append")
                    elif is_cld:
                        # CLD requires explicit CREATE ICEBERG TABLE syntax.
                        # Table doesn't exist, so create it first.
                        _create_cld_iceberg_table(
                            session,
                            _get_writer_for_table_creation(input_df)._dataframe,
                            snowpark_table_name,
                            options=cld_create_options,
                            partition_cols=partition_cols_for_iceberg_config,
                            iceberg_version=resolved_iceberg_version,
                        )
                        # Re-fetch schema after table creation
                        table_schema_or_error = _get_table_schema_or_error(
                            schema_table_name, session
                        )
                    input_df, table_schema_or_error = _prepare_iceberg_write_dataframe(
                        session,
                        input_df,
                        schema_table_name,
                        table_schema_or_error,
                        merge_schema,
                        # V1 doesn't support check-nullability (V2-only).
                        check_nullability=False,
                        # V1 writer does not yet resolve the check-ordering option;
                        # disable enforcement here to preserve existing V1 behavior.
                        check_ordering=False,
                    )
                    if is_cld:
                        # CLD tables don't use iceberg_config
                        writer = _validate_schema_and_get_writer(
                            input_df,
                            "append",
                            schema_table_name,
                            table_schema_or_error,
                        )
                        if dml_target.uses_branch_dml:
                            append_dataframe_to_ref_dml_target(
                                session, writer._dataframe, dml_target
                            )
                        else:
                            writer.saveAsTable(
                                table_name=snowpark_table_name,
                                mode="append",
                                column_order=_column_order_for_write,
                                # Write-path fix (not identifier casing): after
                                # _prepare_iceberg_write_dataframe the table already
                                # exists; without table_exists=True Snowpark re-attempts
                                # CREATE and append fails (merge-gate test_spark_write_*).
                                table_exists=isinstance(
                                    table_schema_or_error, DataType
                                ),
                            )
                    else:
                        writer = _validate_schema_and_get_writer(
                            input_df,
                            "append",
                            schema_table_name,
                            table_schema_or_error,
                        )
                        if dml_target.uses_branch_dml:
                            append_dataframe_to_ref_dml_target(
                                session, writer._dataframe, dml_target
                            )
                        else:
                            writer.saveAsTable(
                                table_name=snowpark_table_name,
                                mode="append",
                                column_order=_column_order_for_write,
                                iceberg_config=iceberg_config,
                                table_exists=isinstance(
                                    table_schema_or_error, DataType
                                ),
                            )
                case "ignore":
                    if not isinstance(
                        table_schema_or_error, DataType
                    ):  # Table not exists
                        if dml_target.has_ref:
                            reject_ref_dml_table_creation(dml_target, "create")
                        elif is_cld:
                            # CLD requires explicit CREATE ICEBERG TABLE syntax.
                            # We must use append mode after table creation because
                            # ignore mode would skip the insert (table now exists).
                            _create_cld_iceberg_table(
                                session,
                                _get_writer_for_table_creation(input_df)._dataframe,
                                schema_table_name,
                                options=cld_create_options,
                                partition_cols=partition_cols_for_iceberg_config,
                                iceberg_version=resolved_iceberg_version,
                            )
                            _get_writer_for_table_creation(input_df).saveAsTable(
                                table_name=schema_table_name,
                                mode="append",
                                column_order=_column_order_for_write,
                                # Table was just created above; tell Snowpark not
                                # to CREATE again (same rationale as append path).
                                table_exists=True,
                            )
                        else:
                            _get_writer_for_table_creation(input_df).saveAsTable(
                                table_name=schema_table_name,
                                mode="ignore",
                                column_order=_column_order_for_write,
                                iceberg_config=iceberg_config,
                            )
                case "overwrite":
                    table_exists = isinstance(table_schema_or_error, DataType)
                    if table_exists:
                        _validate_table_type(schema_table_name, session, "iceberg")

                    if table_exists and is_insert_into:
                        # SNOW-3717449: insertInto(overwrite) overwrites rows in
                        # place via INSERT OVERWRITE INTO (mode="truncate" +
                        # table_exists=True), preserving the table's external
                        # volume / iceberg version / comment / grants instead of
                        # rebuilding it. saveAsTable(overwrite) still rebuilds (may
                        # change schema) via the else branch. Mirrors V2
                        # MODE_OVERWRITE (SNOW-3310119).
                        _validate_schema_and_get_writer(
                            input_df,
                            "append",
                            schema_table_name,
                            table_schema_or_error,
                        ).saveAsTable(
                            table_name=snowpark_table_name,
                            table_exists=True,
                            mode="truncate",
                            column_order=_column_order_for_write,
                        )
                    elif is_cld and not table_exists:
                        if dml_target.has_ref:
                            reject_ref_dml_table_creation(dml_target, "create")
                        # CLD requires explicit CREATE ICEBERG TABLE syntax.
                        # After creating the table, use overwrite mode to insert data.
                        # Note: CLD tables don't use iceberg_config because the external
                        # volume and catalog are managed by the catalog-linked database.
                        writer = _get_writer_for_table_creation(input_df)
                        _create_cld_iceberg_table(
                            session,
                            writer._dataframe,
                            snowpark_table_name,
                            options=cld_create_options,
                            partition_cols=partition_cols_for_iceberg_config,
                            iceberg_version=resolved_iceberg_version,
                        )
                        writer.saveAsTable(
                            table_name=snowpark_table_name,
                            mode="overwrite",
                            column_order=_column_order_for_write,
                        )
                    else:
                        if not table_exists and dml_target.has_ref:
                            reject_ref_dml_table_creation(dml_target, "create")
                        writer = (
                            _validate_schema_and_get_writer(
                                input_df,
                                "overwrite",
                                schema_table_name,
                                table_schema_or_error if table_exists else None,
                            )
                            if table_exists
                            else _get_writer_for_table_creation(input_df)
                        )
                        _overwrite_iceberg_with_fallback(
                            writer=writer,
                            snowpark_table_name=snowpark_table_name,
                            iceberg_config=iceberg_config,
                            session=session,
                            input_df=input_df,
                        )
                case "overwrite_partitions":
                    _validate_table_exist_and_of_type(
                        schema_table_name, session, "iceberg", table_schema_or_error
                    )

                    table_partition_spec = get_partition_spec(
                        schema_table_name, session
                    )

                    # SNOW-3471809: handle "no readable partition spec" cases
                    # before the inference / validation block. Without this
                    # branch, `effective_partition_cols` flows in as ``None``
                    # to `get_snowpark_column_names_from_spark_column_names`
                    # (and to `_validate_partition_columns_match_spec`'s
                    # list comprehension), which both iterate the arg and
                    # crash with ``'NoneType' object is not iterable``.
                    #
                    # Three real paths land here:
                    #   (a) The table is genuinely unpartitioned — Managed
                    #       Iceberg's `SHOW ICEBERG TABLES` reports
                    #       `current_partition_spec_id IS NULL`, so
                    #       `get_partition_spec` returns None. Spark's
                    #       semantics on `dynamic` overwrite of an
                    #       unpartitioned table degrade to a full overwrite.
                    #   (b) The table is on a Catalog-Linked Database
                    #       (Glue / Unity) and the partition spec isn't
                    #       readable from Snowflake metadata even though
                    #       the underlying Iceberg manifest carries one.
                    #       Silently full-overwriting here would wipe
                    #       partitions that aren't in the input DataFrame,
                    #       so we surface the ambiguity instead.
                    #   (c) The customer passed `.partitionBy(...)` on a
                    #       table that has no partition columns — the
                    #       existing `_validate_partition_columns_match_spec`
                    #       diagnostic still fires for that case.
                    if table_partition_spec is None or not table_partition_spec.fields:
                        if is_cld:
                            exception = AnalysisException(
                                "Dynamic partition overwrite (overwrite-mode='dynamic') "
                                f"on catalog-linked Iceberg table '{snowpark_table_name}': "
                                "the table's partition spec could not be determined "
                                "from Snowflake metadata. Pass the partition columns "
                                "explicitly via .partitionBy(<cols>) so partitions "
                                "outside the input DataFrame are not silently "
                                "overwritten."
                            )
                            attach_custom_error_code(
                                exception, ErrorCodes.INVALID_INPUT
                            )
                            raise exception
                        if partition_cols:
                            # Preserve case (c)'s existing error message
                            # (IllegalArgumentException with INVALID_INPUT).
                            _validate_partition_columns_match_spec(
                                partition_cols, table_partition_spec
                            )
                        # Managed / non-CLD path: Snowflake reliably reports
                        # the partition spec for Managed Iceberg, so a missing
                        # spec means the table is unpartitioned. Mirror
                        # Spark's "dynamic on unpartitioned == full overwrite"
                        # semantics.
                        _overwrite_iceberg_with_fallback(
                            writer=_validate_schema_and_get_writer(
                                input_df,
                                "overwrite",
                                schema_table_name,
                                table_schema_or_error,
                            ),
                            snowpark_table_name=snowpark_table_name,
                            iceberg_config=iceberg_config,
                            session=session,
                            input_df=input_df,
                        )
                        return

                    # If partition columns not explicitly provided via partitionBy(),
                    # infer them from the table's partition spec
                    spec_col_names = [
                        field.name for field in table_partition_spec.fields
                    ]
                    effective_partition_cols = partition_cols
                    if not partition_cols:
                        effective_partition_cols = (
                            _infer_dynamic_partition_cols_from_spec(
                                spec_col_names,
                                list(spark_column_names),
                                global_config.spark_sql_caseSensitive,
                            )
                        )

                    # SNOW-3471809: surface a clear error when the table IS
                    # partitioned but inference failed to find any matching
                    # DataFrame column. Without this guard, the downstream
                    # ``get_snowpark_column_names_from_spark_column_names``
                    # would iterate ``None`` and raise ``TypeError``.
                    if not effective_partition_cols:
                        exception = AnalysisException(
                            "Dynamic partition overwrite (overwrite-mode='dynamic') "
                            f"on Iceberg table '{snowpark_table_name}': could not "
                            "determine partition columns. The table is partitioned by "
                            f"{spec_col_names!r}, but no matching columns were found "
                            f"in the input DataFrame columns {list(spark_column_names)!r}. "
                            "Pass .partitionBy(<cols>) explicitly to disambiguate."
                        )
                        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                        raise exception

                    _validate_partition_columns_match_spec(
                        effective_partition_cols, table_partition_spec
                    )

                    _validate_data_columns_present_in_table(
                        table_schema_or_error,
                        input_df.schema,
                        schema_table_name,
                    )
                    partition_column_names = updated_result.column_map.get_snowpark_column_names_from_spark_column_names(
                        effective_partition_cols
                    )
                    distinct_partitions_df = input_df.select(
                        *partition_column_names
                    ).distinct()
                    overwrite_condition = get_overwrite_condition(
                        distinct_partitions_df,
                        partition_column_names,
                    )
                    if overwrite_condition is not None:
                        _validate_schema_and_get_writer(
                            input_df,
                            "overwrite",
                            schema_table_name,
                            table_schema_or_error,
                        ).saveAsTable(
                            table_name=snowpark_table_name,
                            table_exists=True,
                            mode="overwrite",
                            column_order=_column_order_for_write,
                            overwrite_condition=overwrite_condition,
                            iceberg_config=iceberg_config,
                        )
                case _:
                    exception = SnowparkConnectNotImplementedError(
                        f"Write mode {write_mode} is not supported"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception
        case _:
            snowpark_table_name = _spark_to_snowflake(write_op.table.table_name)
            save_method = write_op.table.save_method

            if (
                write_op.source in ("snowflake", "net.snowflake.spark.snowflake")
                and write_op.table.save_method
                == commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_UNSPECIFIED
            ):
                save_method = (
                    commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_SAVE_AS_TABLE
                )

                # Normalize option keys to lowercase — the Snowflake Connector for Spark
                # treats all option names as case-insensitive (sfDatabase, SFDATABASE, etc.)
                sf_options = {k.lower(): v for k, v in write_op.options.items()}

                # Raise if sfUser/sfRole/sfWarehouse differ from the current session;
                # we never issue USE statements that would mutate the shared session.
                assert_sf_connector_auth_options_match(session, sf_options)
                assert_sf_connector_warehouse_matches(session, sf_options)

                if len(write_op.table.table_name) == 0:
                    # dbtable lookup must use the lowercased options dict
                    dbtable_name = sf_options.get("dbtable", "")
                    if len(dbtable_name) == 0:
                        exception = SnowparkConnectNotImplementedError(
                            "Save command is not supported without a table name"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.UNSUPPORTED_OPERATION
                        )
                        raise exception
                    else:
                        # Qualify with sfDatabase/sfSchema (falling back to the
                        # session context) so that an unqualified dbtable name
                        # resolves to the correct location without issuing USE.
                        dbtable_name = qualify_dbtable_with_sf_options(
                            dbtable_name, sf_options, session
                        )
                        snowpark_table_name = _spark_to_snowflake(dbtable_name)

            if (
                save_method
                == commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_SAVE_AS_TABLE
            ):
                match write_mode:
                    case "overwrite":
                        # SNOW-3590931: `_validate_schema_and_get_writer`
                        # returns immediately for `overwrite` without
                        # inspecting the target schema (CREATE OR REPLACE
                        # replaces it), so the prior
                        # ``_get_table_schema_or_error`` describe round-trip
                        # was wasted overhead (~200 ms RTT).
                        # ``_validate_table_type`` already resolves table
                        # type via ``snowflake.core`` (defaulting to
                        # ``"TABLE"`` for missing targets and rejecting
                        # iceberg targets), so we keep it and drop the
                        # describe.
                        _validate_table_type(snowpark_table_name, session, "fdn")

                        write_mode = "overwrite"
                        _validate_schema_and_get_writer(
                            input_df,
                            write_mode,
                            snowpark_table_name,
                        ).saveAsTable(
                            table_name=snowpark_table_name,
                            mode=write_mode,
                            copy_grants=True,
                            column_order=_column_order_for_write,
                        )
                    case "truncate":
                        # Snowpark mode="truncate" on an existing table
                        # delegates to INSERT OVERWRITE INTO via
                        # snowflake_plan.py. Unlike the default overwrite path
                        # (CREATE OR REPLACE), this preserves the table object
                        # (COMMENT, grants, masking/row-access policies, tags)
                        # and avoids dropping downstream dependencies (views,
                        # streams, dynamic tables) that reference it by name.
                        # Verified empirically in test_truncate_option with
                        # SHOW CREATE TABLE before/after. If the target does
                        # not exist, Snowpark falls back to CREATE OR REPLACE
                        # TABLE AS SELECT. Column matching is by name
                        # (column_order="name"); SCOS's
                        # _validate_schema_for_append rejects schema
                        # mismatches (e.g., renamed columns) with
                        # AnalysisException before Snowpark is reached.
                        table_schema_or_error = _get_table_schema_or_error(
                            snowpark_table_name, session
                        )
                        if isinstance(table_schema_or_error, DataType):  # Table exists
                            _validate_table_type(snowpark_table_name, session, "fdn")

                        _validate_schema_and_get_writer(
                            input_df,
                            write_mode,
                            snowpark_table_name,
                            table_schema_or_error,
                        ).saveAsTable(
                            table_name=snowpark_table_name,
                            mode=write_mode,
                            column_order=_column_order_for_write,
                        )
                    case "append":
                        table_schema_or_error = _get_table_schema_or_error(
                            snowpark_table_name, session
                        )
                        if isinstance(table_schema_or_error, DataType):  # Table exists
                            _validate_table_type(snowpark_table_name, session, "fdn")

                        _validate_schema_and_get_writer(
                            input_df,
                            write_mode,
                            snowpark_table_name,
                            table_schema_or_error,
                        ).saveAsTable(
                            table_name=snowpark_table_name,
                            mode=write_mode,
                            column_order=_column_order_for_write,
                        )
                    case _:
                        try:
                            _validate_schema_and_get_writer(
                                input_df, write_mode, snowpark_table_name
                            ).saveAsTable(
                                table_name=snowpark_table_name,
                                mode=write_mode,
                                column_order=_column_order_for_write,
                            )
                        except SnowparkSQLException as e:
                            if "already exists" in str(e) and e.sql_error_code == 1998:
                                exception = AnalysisException(str(e))
                                attach_custom_error_code(
                                    exception, ErrorCodes.INVALID_OPERATION
                                )
                                raise exception from e
                            raise
            elif (
                save_method
                == commands_proto.WriteOperation.SaveTable.TableSaveMethod.TABLE_SAVE_METHOD_INSERT_INTO
            ):
                _validate_schema_and_get_writer(
                    input_df, write_mode, snowpark_table_name
                ).saveAsTable(
                    table_name=snowpark_table_name,
                    mode=write_mode or "append",
                    column_order=_column_order_for_write,
                )
            else:
                exception = SnowparkConnectNotImplementedError(
                    f"Save command not supported: {save_method}"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception


def _write_v2_mode_label(write_op) -> str | None:
    """Best-effort human label for a WriteOperationV2 mode (e.g. ``append``).

    Used only for telemetry (report_iceberg_wap dml_op); never affects routing.
    """
    try:
        field = write_op.DESCRIPTOR.fields_by_name["mode"]
        name = field.enum_type.values_by_number[write_op.mode].name
        return name.removeprefix("MODE_").lower() or None
    except Exception:
        return None


def map_write_v2(request: proto_base.ExecutePlanRequest):
    write_op = request.plan.command.write_operation_v2

    # SNOW-3917754: reject an unsupported provider (e.g. .using("delta")) before
    # any planning work. Only create-family modes forward .using(provider) in
    # Spark (see _is_create_table_mode_v2), so scope the check to match.
    if _is_create_table_mode_v2(write_op.mode):
        raise_if_unsupported_data_source(
            write_op.provider, get_or_create_snowpark_session()
        )

    dml_target = resolve_iceberg_ref_dml_target(
        write_op.table_name, _spark_to_snowflake, dml_op=_write_v2_mode_label(write_op)
    )
    snowpark_table_name = dml_target.dml_snowflake_sql
    schema_table_name = dml_target.base_snowflake_sql
    # SNOW-2443454: strip both internal and qualified-access-only metadata
    # (USING-join source columns) up front to match the v1 path and avoid
    # leaking them into the written table's schema.
    result = map_relation(write_op.input).without_hidden_columns()
    (
        input_df,
        snowpark_column_names,
        spark_column_names,
        qualifiers,
    ) = handle_column_names(result, "table")

    # Create updated container with transformed dataframe, then filter METADATA$FILENAME columns
    updated_result = DataFrameContainer.create_with_column_mapping(
        dataframe=input_df,
        spark_column_names=spark_column_names,
        snowpark_column_names=snowpark_column_names,
        column_metadata=result.column_map.column_metadata,
        column_qualifiers=qualifiers,
        parent_column_name_map=result.column_map.get_parent_column_name_map(),
        table_name=result.table_name,
        alias=result.alias,
        partition_hint=result.partition_hint,
    )
    updated_result = without_internal_columns(updated_result)
    input_df = updated_result.dataframe

    session: snowpark.Session = get_or_create_snowpark_session()

    if write_op.table_name is None or write_op.table_name == "":
        exception = SnowparkConnectNotImplementedError(
            "Write operation V2 only support table writing now"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    is_cld = is_in_cld_context()
    is_iceberg = _is_iceberg_write_v2_target(
        session,
        schema_table_name,
        write_op.provider,
        write_op.mode,
        is_cld,
    )
    table_type = "iceberg" if is_iceberg else "fdn"
    snowpark_table_name, use_branch_dml = _write_v2_dml_routing(
        dml_target, is_iceberg=is_iceberg
    )

    # Mirrors Spark case insensitivity
    write_options_v2 = {k.lower(): v for k, v in write_op.options.items()}
    check_nullability = (
        _resolve_iceberg_check_nullability(write_options_v2) if is_iceberg else False
    )
    # SNOW-3310108: enforce column ordering by default for Iceberg V2 writes
    # (matches Iceberg check-ordering=true). Customers writing reordered columns
    # must pass option("check-ordering", "false") to restore the prior behaviour.
    check_ordering = (
        _resolve_iceberg_check_ordering(write_options_v2) if is_iceberg else False
    )

    # FDN tables have no user-defined partitioning; reject partitionedBy
    # uniformly across all write modes (SNOW-3310107). Iceberg targets honor it.
    if not is_iceberg:
        # SNOW-3813783: resolve the type for existing-table modes so an unresolved
        # target (missing, or an RBAC-hidden Iceberg table) yields an access hint
        # rather than the bare FDN message. Cache hit; skipped for create modes.
        actual_type = (
            get_table_type(snowpark_table_name, session)
            if _is_existing_write_table_mode_v2(write_op.mode)
            else None
        )
        _validate_no_partition_cols_on_fdn(
            write_op.partitioning_columns, snowpark_table_name, actual_type
        )

    # Iceberg: parse partitionedBy (identity + years/months/days/hours/bucket
    # transforms) once. partition_specs carries the source columns (used as the
    # overwritePartitions fallback below); partition_exprs are the rendered
    # Snowflake PARTITION BY strings used by the non-CLD iceberg_config path.
    # The CLD CREATE ICEBERG TABLE path instead consumes partition_specs_cld
    # (column resolved, transform kept structured), because it re-quotes each
    # element and would corrupt a pre-rendered string like DAY("TS")
    # (SNOW-3310107).
    partition_specs = (
        parse_v2_partition_specs(write_op.partitioning_columns)
        if is_iceberg and write_op.partitioning_columns
        else []
    )
    partition_exprs = (
        build_iceberg_partition_exprs(
            partition_specs, updated_result.column_map, is_cld
        )
        if partition_specs
        else None
    )
    partition_specs_cld = (
        resolve_v2_partition_specs(partition_specs, updated_result.column_map, is_cld)
        if partition_specs
        else None
    )

    iceberg_config = (
        _build_iceberg_config(
            options=dict(write_op.table_properties),
            partition_cols=partition_exprs,
            is_cld=is_cld,
        )
        if is_iceberg
        else None
    )
    merge_schema = (
        _iceberg_merge_schema_enabled(
            {**dict(write_op.table_properties), **dict(write_op.options)},
            _session_config_for_write(),
        )
        if is_iceberg
        else False
    )

    # V2 CREATE / CREATE_OR_REPLACE / REPLACE on a CLD-backed iceberg target
    # cannot use Snowpark's iceberg_config DDL path: CLDs reject the implicit
    # CREATE TABLE ... iceberg_config = (...) form, and the column-quoting
    # rule that path uses (`"ID" INTEGER`) violates CLD's case rule for
    # case-insensitive catalogs (Glue, Unity), producing "Invalid identifier
    # ID" at CREATE time even after the CATALOG=SNOWFLAKE injection fix
    # (SNOW-3471806). Mirror the V1 errorifexists CLD branch via
    # `_create_cld_iceberg_table_then_load`: emit explicit
    # `CREATE ICEBERG TABLE` (which routes columns through the CLD-aware
    # `spark_to_sf_single_id`), then load the rows via Snowpark against the
    # now-existing table.
    cld_create_options = dict(write_op.table_properties)

    # Some properties are extracted as named scalars and popped (comment,
    # format-version, max-snapshot-age.ms); the remainder is forwarded to
    # `_create_cld_iceberg_table` as the `options` bag. That includes
    # `base_location` / `location` and the storage-property keys consumed by
    # `_build_storage_serialization_policy_clause` /
    # `_build_target_file_size_clause` (`storage_serialization_policy`,
    # `iceberg.storage_serialization_policy`, `write.target-file-size`,
    # `target_file_size`).
    table_comment = cld_create_options.pop("comment", None)
    cld_create_options.pop("format-version", None)
    cld_create_options.pop("iceberg.format-version", None)
    cld_create_options.pop("max-snapshot-age.ms", None)
    cld_create_options.pop("iceberg.max-snapshot-age.ms", None)
    table_format_version = (
        iceberg_config.get("iceberg_version") if iceberg_config else None
    )
    # `max-snapshot-age.ms` maps to DATA_RETENTION_TIME_IN_DAYS. Only create/replace
    # valid for modes
    # DATA_RETENTION_TIME_IN_DAYS is not supported for CLD tables.
    _reject_max_snapshot_age_for_cld(
        is_cld=is_cld,
        table_properties=dict(write_op.table_properties),
    )
    table_data_retention_days = (
        _extract_max_snapshot_age_days(dict(write_op.table_properties))
        if is_iceberg
        and not is_cld
        and write_op.mode
        in (
            commands_proto.WriteOperationV2.MODE_CREATE,
            commands_proto.WriteOperationV2.MODE_REPLACE,
            commands_proto.WriteOperationV2.MODE_CREATE_OR_REPLACE,
        )
        else None
    )

    match write_op.mode:
        case commands_proto.WriteOperationV2.MODE_CREATE:
            if dml_target.has_ref:
                reject_ref_dml_table_creation(dml_target, "create")
            table_schema_or_error = _get_table_schema_or_error(
                schema_table_name, session
            )
            _validate_table_does_not_exist(schema_table_name, table_schema_or_error)
            writer = _get_writer_for_table_creation(input_df)
            if is_cld and is_iceberg:
                _create_cld_iceberg_table_then_load(
                    session,
                    writer,
                    schema_table_name,
                    options=cld_create_options,
                    partition_specs=partition_specs_cld,
                    comment=table_comment,
                    iceberg_version=table_format_version,
                )
            else:
                writer.saveAsTable(
                    table_name=schema_table_name,
                    mode="errorifexists",
                    column_order=_column_order_for_write,
                    iceberg_config=iceberg_config,
                    comment=table_comment,
                    data_retention_time=table_data_retention_days,
                )

        case commands_proto.WriteOperationV2.MODE_APPEND:
            table_schema_or_error = _get_table_schema_or_error(
                schema_table_name, session
            )
            if not isinstance(table_schema_or_error, DataType) and dml_target.has_ref:
                reject_ref_dml_table_creation(dml_target, "append")
            _validate_table_exist_and_of_type(
                schema_table_name, session, table_type, table_schema_or_error
            )
            if is_iceberg:
                input_df, table_schema_or_error = _prepare_iceberg_write_dataframe(
                    session,
                    input_df,
                    schema_table_name,
                    table_schema_or_error,
                    merge_schema,
                    check_nullability=check_nullability,
                    check_ordering=check_ordering,
                )
            # Nullability is validated pre-ALTER inside
            # _prepare_iceberg_write_dataframe, so a rejected write never mutates
            # the table. Iceberg instead lets the commit fail and roll back; we
            # reach the same net behavior by checking first, without a transaction.
            # This post-ALTER check is therefore a no-op when we evolved, and only
            # does real work on the non-merge path.
            writer = _validate_schema_and_get_writer(
                input_df,
                "append",
                schema_table_name,
                table_schema_or_error,
                check_nullability=check_nullability,
                check_ordering=check_ordering,
            )
            if use_branch_dml:
                append_dataframe_to_ref_dml_target(
                    session, writer._dataframe, dml_target
                )
            else:
                writer.saveAsTable(
                    table_name=snowpark_table_name,
                    mode="append",
                    column_order=_column_order_for_write,
                    iceberg_config=iceberg_config,
                    # Write-path fix (SNOW-3968447): schema was already resolved
                    # via _get_table_schema_or_error; without table_exists=True
                    # Snowpark re-issues show tables like on every append.
                    table_exists=isinstance(table_schema_or_error, DataType),
                )

        case commands_proto.WriteOperationV2.MODE_OVERWRITE:
            table_schema_or_error = _get_table_schema_or_error(
                schema_table_name, session
            )
            _validate_table_exist_and_of_type(
                schema_table_name, session, table_type, table_schema_or_error
            )
            # SNOW-3310119 / mergeSchema: V2 overwrite preserves the table
            # definition, so evolve the Iceberg schema (ALTER + NULL-pad) the
            # same way append does before the INSERT OVERWRITE.
            if is_iceberg:
                input_df, table_schema_or_error = _prepare_iceberg_write_dataframe(
                    session,
                    input_df,
                    schema_table_name,
                    table_schema_or_error,
                    merge_schema,
                    check_nullability=check_nullability,
                    check_ordering=check_ordering,
                )
            # SNOW-3310119: V2 overwrite preserves the table definition (schema,
            # partitioning, properties) and only replaces rows — unlike replace()
            # / createOrReplace(), which rebuild the definition. Use append-style
            # schema handling so a DataFrame whose schema does not match the
            # existing table fails fast with a clean AnalysisException, and
            # write via an atomic INSERT OVERWRITE (table_exists=True) rather
            # than a CREATE OR REPLACE.
            writer = _validate_schema_and_get_writer(
                input_df,
                "append",
                schema_table_name,
                table_schema_or_error,
                check_nullability=check_nullability,
                check_ordering=check_ordering,
            )

            overwrite_cond = None
            if write_op.HasField("overwrite_condition"):
                overwrite_cond = _map_overwrite_condition(
                    write_op.overwrite_condition,
                    updated_result,
                    input_df,
                )

            if overwrite_cond is not None:
                # CLD (unmanaged) Iceberg tables reject the atomic
                # overwrite_condition transaction (091586); the helper falls
                # back to a non-atomic DELETE + APPEND for those tables while
                # leaving FDN and managed Iceberg on the fast atomic path.
                _overwrite_with_condition_and_cld_fallback(
                    writer=writer,
                    snowpark_table_name=snowpark_table_name,
                    overwrite_condition=overwrite_cond,
                    session=session,
                    is_iceberg=is_iceberg,
                    iceberg_config=iceberg_config,
                )
            else:
                # Reached when the V2 command carries no overwrite condition
                # (e.g. df.writeTo(t).overwrite(None)); a real condition such as
                # overwrite(lit(True)) goes through the conditional branch above.
                # Replace every row but keep the table definition intact via an
                # INSERT OVERWRITE (table_exists=True + mode="truncate"), never a
                # CREATE OR REPLACE.
                writer.saveAsTable(
                    table_name=snowpark_table_name,
                    table_exists=True,
                    mode="truncate",
                    column_order=_column_order_for_write,
                )

        case commands_proto.WriteOperationV2.MODE_OVERWRITE_PARTITIONS:
            table_schema_or_error = _get_table_schema_or_error(
                schema_table_name, session
            )
            if not isinstance(table_schema_or_error, StructType):
                exception = AnalysisException(
                    f"[TABLE_OR_VIEW_NOT_FOUND] The table or view `{dml_target.spark_table_name}` cannot be found."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception
            # overwritePartitions preserves the table definition and replaces
            # only the matching partitions, so honor mergeSchema like append:
            # ALTER new columns onto the Iceberg table and pad missing ones with
            # NULL before resolving partitions and writing.
            if is_iceberg:
                input_df, table_schema_or_error = _prepare_iceberg_write_dataframe(
                    session,
                    input_df,
                    schema_table_name,
                    table_schema_or_error,
                    merge_schema,
                    check_nullability=check_nullability,
                    check_ordering=check_ordering,
                )
            # Iceberg: build a per-partition overwrite condition from the table's
            # partition spec. FDN tables have no user-defined partitioning, so
            # the condition stays None and the write falls through to a full overwrite.
            overwrite_condition = None
            if is_iceberg:
                table_partition_spec = get_partition_spec(schema_table_name, session)

                if table_partition_spec and table_partition_spec.fields:
                    # The table's persisted partition spec is the source of truth
                    # (preferred over the request's partitionedBy). Handles identity
                    # and transforms; the helper gates unsupported transforms (bucket,
                    # truncate, void, unknown) rather than silently producing wrong
                    # results / data loss.
                    _validate_data_columns_present_in_table(
                        table_schema_or_error,
                        input_df.schema,
                        schema_table_name,
                    )
                    if merge_schema:
                        # The pre-evolution column_map is stale after schema
                        # evolution. Build a fresh map keyed by unquoted evolved
                        # names so get_transform_overwrite_condition can resolve
                        # partition columns for both identity and transform specs.
                        evolved_actual = [f.name for f in input_df.schema.fields]
                        evolved_unquoted = [
                            unquote_if_quoted(n) for n in evolved_actual
                        ]
                        col_map_for_condition = ColumnNameMap(
                            spark_column_names=evolved_unquoted,
                            snowpark_column_names=evolved_actual,
                        )
                    else:
                        col_map_for_condition = updated_result.column_map
                    overwrite_condition = get_transform_overwrite_condition(
                        input_df,
                        table_partition_spec,
                        col_map_for_condition,
                        table_schema_or_error,
                    )
                    # Empty input has no partitions to overwrite — skip the
                    # write entirely so existing data is not truncated.
                    if overwrite_condition is not None:
                        if use_branch_dml:
                            writer = _validate_schema_and_get_writer(
                                input_df,
                                "append",
                                schema_table_name,
                                table_schema_or_error,
                                check_nullability=check_nullability,
                                check_ordering=check_ordering,
                            )
                            overwrite_partitions_dataframe_to_ref_dml_target(
                                session,
                                writer._dataframe,
                                dml_target,
                                overwrite_condition,
                            )
                        else:
                            _overwrite_partitions_with_unmanaged_fallback(
                                input_df,
                                snowpark_table_name,
                                table_schema_or_error,
                                overwrite_condition,
                                session,
                                check_nullability=check_nullability,
                                check_ordering=check_ordering,
                            )
                    return

                # No persisted spec: fall back to this request's partitionedBy columns
                # (identity raw-value matching — for an existing unpartitioned table a
                # request-side transform is irrelevant to which partitions to replace).
                # partition_specs is None for the common overwritePartitions call (no
                # partitionedBy in the request); treat that as "no columns".
                effective_partition_cols = [
                    spec.column for spec in (partition_specs or [])
                ]

                if effective_partition_cols:
                    _validate_data_columns_present_in_table(
                        table_schema_or_error,
                        input_df.schema,
                        schema_table_name,
                    )
                    if merge_schema:
                        # mergeSchema realigned input_df to the table's column
                        # identifiers, so the pre-evolution column_map is stale.
                        # Resolve partition columns against the aligned schema
                        # (case-insensitive) instead.
                        df_by_key = {
                            _iceberg_write_col_key(f.name): f.name
                            for f in input_df.schema.fields
                        }
                        partition_column_names = []
                        for c in effective_partition_cols:
                            resolved = df_by_key.get(_iceberg_write_col_key(c))
                            if resolved is None:
                                exc = AnalysisException(
                                    f"Partition column '{c}' not found in DataFrame "
                                    f"after schema evolution for table "
                                    f"{dml_target.spark_table_name}."
                                )
                                attach_custom_error_code(exc, ErrorCodes.INVALID_INPUT)
                                raise exc
                            partition_column_names.append(resolved)
                    else:
                        partition_column_names = updated_result.column_map.get_snowpark_column_names_from_spark_column_names(
                            effective_partition_cols
                        )
                    distinct_partitions_df = input_df.select(
                        *partition_column_names
                    ).distinct()

                    overwrite_condition = get_overwrite_condition(
                        distinct_partitions_df,
                        partition_column_names,
                    )
                    # Empty input has no partitions to overwrite — skip the
                    # write entirely so existing data is not truncated.
                    if overwrite_condition is not None:
                        if use_branch_dml:
                            writer = _validate_schema_and_get_writer(
                                input_df,
                                "append",
                                schema_table_name,
                                table_schema_or_error,
                                check_nullability=check_nullability,
                                check_ordering=check_ordering,
                            )
                            overwrite_partitions_dataframe_to_ref_dml_target(
                                session,
                                writer._dataframe,
                                dml_target,
                                overwrite_condition,
                            )
                        else:
                            _overwrite_partitions_with_unmanaged_fallback(
                                input_df,
                                snowpark_table_name,
                                table_schema_or_error,
                                overwrite_condition,
                                session,
                                check_nullability=check_nullability,
                                check_ordering=check_ordering,
                            )
                    return

            # No partition spec on table: full overwrite
            writer = _validate_schema_and_get_writer(
                input_df,
                "truncate",
                schema_table_name,
                table_schema_or_error,
                check_nullability=check_nullability,
                check_ordering=check_ordering,
            )
            if use_branch_dml:
                overwrite_dataframe_to_ref_dml_target(
                    session, writer._dataframe, dml_target
                )
            else:
                writer.saveAsTable(
                    table_name=snowpark_table_name,
                    table_exists=True,
                    mode="truncate",
                    column_order=_column_order_for_write,
                )

        case commands_proto.WriteOperationV2.MODE_REPLACE:
            if dml_target.has_ref:
                reject_ref_dml_table_creation(dml_target, "replace")
            table_schema_or_error = _get_table_schema_or_error(
                schema_table_name, session
            )
            _validate_table_exist_and_of_type(
                schema_table_name, session, table_type, table_schema_or_error
            )
            writer = _validate_schema_and_get_writer(
                input_df, "replace", schema_table_name, table_schema_or_error
            )
            if is_iceberg and is_cld:
                # CLD iceberg REPLACE: existing CLD table rejects `CREATE OR
                # REPLACE` (Snowpark's default for mode="overwrite") and the
                # iceberg_config form on .saveAsTable also rejects the
                # uppercased quoted column names. Drop and re-create via
                # explicit CLD-aware DDL, then append. We checked above that
                # the table exists and is iceberg.
                session.sql(f"DROP TABLE IF EXISTS {schema_table_name}").collect()
                _create_cld_iceberg_table_then_load(
                    session,
                    writer,
                    schema_table_name,
                    options=cld_create_options,
                    partition_specs=partition_specs_cld,
                    comment=table_comment,
                    iceberg_version=table_format_version,
                )
            elif is_iceberg:
                _overwrite_iceberg_with_fallback(
                    writer=writer,
                    snowpark_table_name=schema_table_name,
                    iceberg_config=iceberg_config,
                    session=session,
                    input_df=input_df,
                    comment=table_comment,
                    data_retention_time_days=table_data_retention_days,
                )
            else:
                writer.saveAsTable(
                    table_name=schema_table_name,
                    mode="overwrite",
                    column_order=_column_order_for_write,
                    comment=table_comment,
                    data_retention_time=table_data_retention_days,
                )

        case commands_proto.WriteOperationV2.MODE_CREATE_OR_REPLACE:
            if dml_target.has_ref:
                reject_ref_dml_table_creation(dml_target, "createOrReplace")
            writer = _validate_schema_and_get_writer(
                input_df, "create_or_replace", schema_table_name
            )
            if is_iceberg and is_cld:
                # CLD iceberg CREATE_OR_REPLACE: same constraints as REPLACE
                # above. The table may or may not already exist; either way
                # drop-if-exists + explicit CREATE ICEBERG TABLE produces
                # the correct column casing on Glue / Unity catalogs.
                session.sql(f"DROP TABLE IF EXISTS {schema_table_name}").collect()
                _create_cld_iceberg_table_then_load(
                    session,
                    writer,
                    schema_table_name,
                    options=cld_create_options,
                    partition_specs=partition_specs_cld,
                    comment=table_comment,
                    iceberg_version=table_format_version,
                )
            elif is_iceberg:
                _overwrite_iceberg_with_fallback(
                    writer=writer,
                    snowpark_table_name=schema_table_name,
                    iceberg_config=iceberg_config,
                    session=session,
                    input_df=input_df,
                    comment=table_comment,
                    data_retention_time_days=table_data_retention_days,
                )
            else:
                writer.saveAsTable(
                    table_name=schema_table_name,
                    mode="overwrite",
                    column_order=_column_order_for_write,
                    comment=table_comment,
                    data_retention_time=table_data_retention_days,
                )

        case _:
            exception = SnowparkConnectNotImplementedError(
                f"Write mode {commands_proto.WriteOperationV2.Mode.Name(write_op.mode)} is not supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def _get_table_schema_or_error(
    snowpark_table_name: str, snowpark_session: snowpark.Session
) -> DataType | SnowparkSQLException:
    cache = get_or_create_table_metadata_cache(snowpark_session)

    def lookup() -> DataType | SnowparkSQLException:
        try:
            return snowpark_session.table(snowpark_table_name).schema
        except SnowparkSQLException as e:
            return e

    return cache.get_table_schema(snowpark_table_name, lookup)


def _get_writer_for_table_creation(df: snowpark.DataFrame) -> snowpark.DataFrameWriter:
    # When creating a new table, if case sensitivity is not enabled, we need to rename the columns
    # to upper case so they are case-insensitive in Snowflake.
    if not global_config.spark_sql_caseSensitive:
        new_cols = []
        needs_rename = False
        for field in df.schema.fields:
            col_name = field.name
            # Uppercasing is fine, regardless of whether the original name was quoted or not.
            # In Snowflake these are equivalent "COL" == COL == col == coL
            if col_name != col_name.upper():
                new_cols.append(col(col_name).alias(col_name.upper()))
                needs_rename = True
            else:
                new_cols.append(col(col_name))
        if needs_rename:
            df = df.select(new_cols)
    # Spark doesn't preserve nullability in table creation so the resulting table has
    # all columns nullable.
    force_nullable_schema(df)
    return df.write


def _validate_schema_and_get_writer(
    input_df: snowpark.DataFrame,
    write_mode: str,
    snowpark_table_name: str,
    table_schema_or_error: DataType | SnowparkSQLException | None = None,
    check_nullability: bool = False,
    check_ordering: bool = False,
) -> snowpark.DataFrameWriter:
    if write_mode is not None and write_mode.lower() in (
        "replace",
        "create_or_replace",
        "overwrite",
    ):
        return _get_writer_for_table_creation(input_df)

    table_schema = None
    if table_schema_or_error is not None:
        if isinstance(table_schema_or_error, SnowparkSQLException):
            msg = table_schema_or_error.message
            if "SQL compilation error" in msg and "does not exist" in msg:
                pass
            else:
                attach_custom_error_code(
                    table_schema_or_error, ErrorCodes.INTERNAL_ERROR
                )
                raise table_schema_or_error
        elif isinstance(table_schema_or_error, DataType):
            table_schema = table_schema_or_error
    else:
        try:
            table_schema = (
                get_or_create_snowpark_session().table(snowpark_table_name).schema
            )
        except SnowparkSQLException as e:
            msg = e.message
            if "SQL compilation error" in msg and "does not exist" in msg:
                pass
            else:
                attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
                raise e

    if table_schema is None:
        # If table does not exist, we can skip the schema validation
        return _get_writer_for_table_creation(input_df)

    _validate_schema_for_append(
        table_schema,
        input_df.schema,
        snowpark_table_name,
        check_nullability=check_nullability,
        check_ordering=check_ordering,
    )

    # If table exists, rename/cast columns to match the existing table schema using a
    # single select() instead of per-column withColumnRenamed/withColumn to avoid
    # generating deeply nested SQL.
    if not global_config.spark_sql_caseSensitive:
        select_cols = []
        needs_rewrite = False
        table_field_by_key = {
            unquote_if_quoted(f.name).upper(): f for f in table_schema.fields
        }
        for field in input_df.schema.fields:
            col_name = field.name
            matching_field = table_field_by_key.get(unquote_if_quoted(col_name).upper())
            target_name = (
                matching_field.name
                if matching_field is not None and matching_field.name != col_name
                else col_name
            )
            needs_cast = (
                matching_field is not None and field.datatype != matching_field.datatype
            )

            if needs_cast:
                cast_col = _build_cast_column(
                    col(col_name),
                    field.datatype,
                    matching_field.datatype,
                    rename_fields=True,
                )
                select_cols.append(cast_col.alias(target_name))
                needs_rewrite = True
            elif target_name != col_name:
                select_cols.append(col(col_name).alias(target_name))
                needs_rewrite = True
            else:
                select_cols.append(col(col_name))
        if needs_rewrite:
            input_df = input_df.select(select_cols)
    else:
        # Case-sensitive mode: cast mismatched types to match the existing table schema
        select_cols = []
        needs_rewrite = False
        table_field_by_key = {unquote_if_quoted(f.name): f for f in table_schema.fields}
        for field in input_df.schema.fields:
            col_name = field.name
            matching_field = table_field_by_key.get(unquote_if_quoted(col_name))
            needs_cast = (
                matching_field is not None and field.datatype != matching_field.datatype
            )
            if needs_cast:
                cast_col = _build_cast_column(
                    col(col_name),
                    field.datatype,
                    matching_field.datatype,
                )
                select_cols.append(cast_col.alias(col_name))
                needs_rewrite = True
            else:
                select_cols.append(col(col_name))
        if needs_rewrite:
            input_df = input_df.select(select_cols)
    return input_df.write


def _is_atomic_type(t: DataType) -> bool:
    return not isinstance(t, (StructType, ArrayType, MapType))


def _store_assignment_policy() -> str:
    """Return spark.sql.storeAssignmentPolicy normalized to uppercase."""
    return global_config.get("spark.sql.storeAssignmentPolicy", "LEGACY").upper()


def _store_assignment_is_legacy() -> bool:
    return _store_assignment_policy() == "LEGACY"


def _resolve_iceberg_check_nullability(write_options: dict) -> bool:
    """Return whether to enforce nullability for this Iceberg write.

    An explicit ``check-nullability`` option is always honored. When omitted,
    the implicit default follows ``snowpark.connect.nullability.trackColumns``
    rather than Iceberg's hardcoded ``true``: with tracking off (SCOS's default),
    SCOS declines to surface real column nullability to the client, so enforcing
    Iceberg's default would police a contract it does not track. Enable
    ``trackColumns`` (or pass ``check-nullability=true``) for Spark-faithful
    enforcement. The write-time check itself reads the underlying Snowpark
    schema, not the widened client-facing ``df.schema``.
    """
    raw = write_options.get("check-nullability")
    if raw is not None:
        return str_to_bool(raw)
    return is_column_nullability_tracking_enabled()


def _resolve_iceberg_check_ordering(write_options: dict[str, str]) -> bool:
    """Return whether to enforce column ordering for this Iceberg write.

    Matches Iceberg's SparkWriteOptions.CHECK_ORDERING behaviour:
    per-write option "check-ordering" defaults to true.
    """
    raw = write_options.get("check-ordering")
    if raw is not None:
        return str_to_bool(raw)
    return True


def _use_try_cast(source_type: DataType, target_type: DataType) -> bool:
    """Use TRY_CAST for string→scalar casts when storeAssignmentPolicy is LEGACY.

    PySpark with LEGACY policy allows any valid Cast and uses
    Cast(ansiEnabled=false), where invalid values become NULL.
    We match this with TRY_CAST. With ANSI policy (default), PySpark
    rejects these mismatches at analysis time via canANSIStoreAssign.
    """
    return (
        isinstance(source_type, StringType)
        and _is_atomic_type(target_type)
        and not isinstance(target_type, VariantType)
        and not isinstance(target_type, StringType)
        and _store_assignment_is_legacy()
    )


def _build_cast_column(
    source_col: snowpark.Column,
    source_type: DataType,
    target_type: DataType,
    rename_fields: bool = False,
) -> snowpark.Column:
    """Build the appropriate cast expression for a column in the write path.

    Uses TRY_CAST when storeAssignmentPolicy is LEGACY and source is
    StringType targeting a scalar type (invalid values become NULL).
    """
    if _use_try_cast(source_type, target_type):
        return source_col.try_cast(target_type)
    # Route unstructured complex targets (VARIANT / unstructured ARRAY / OBJECT)
    # through the VARIANT bridge. Snowflake stores VARIANT arrays/objects into
    # ARRAY/OBJECT columns without an explicit element/field type.
    coerced = _coerce_to_unstructured_complex_target(
        source_col, source_type, target_type
    )
    if coerced is not None:
        return coerced
    # Runtime overflow wrap mirrors Spark's CheckOverflowInTableInsert: raise
    # [CAST_OVERFLOW] under ANSI/STRICT when a wider-integral or fractional
    # source would overflow the integral target. LEGACY retains silent widening.
    if not _store_assignment_is_legacy() and _overflow_guard_needed(
        source_type, target_type
    ):
        return apply_integral_overflow_with_ansi_check(
            source_col, target_type, ansi_enabled=True
        )
    if isinstance(target_type, StructType) and rename_fields:
        return source_col.cast(target_type, rename_fields=True)
    return source_col.cast(target_type)


def _is_unstructured_array(t: DataType) -> bool:
    return isinstance(t, ArrayType) and getattr(t, "element_type", None) is None


def _is_unstructured_object(t: DataType) -> bool:
    # Snowpark represents an unstructured Snowflake OBJECT column as an empty
    # StructType (StructType([])). Some older paths may also produce
    # MapType(None, None, structured=False); accept both.
    if isinstance(t, StructType) and len(t.fields) == 0:
        return True
    return (
        isinstance(t, MapType)
        and getattr(t, "key_type", None) is None
        and getattr(t, "value_type", None) is None
    )


def _coerce_to_unstructured_complex_target(
    source_col: snowpark.Column,
    source_type: DataType,
    target_type: DataType,
) -> snowpark.Column | None:
    """Return a cast Column when the target is an unstructured complex Snowflake type
    (VARIANT, unstructured ARRAY, unstructured OBJECT) and the source differs; else None.

    Snowflake accepts a VARIANT value that is an array / object into an ARRAY / OBJECT
    column respectively, so we always bridge via VARIANT for unstructured ARRAY and
    OBJECT targets. This keeps the coercion path simple and avoids needing to express
    an element-less Snowpark ArrayType cast.
    """
    if source_type == target_type:
        return None
    # If the source type is unknown (e.g. a typer-opaque expression / UDF
    # return), fall back to a VARIANT bridge when the target is an unstructured
    # complex column. This keeps implicit-cast behavior consistent for UPDATE /
    # MERGE assignment RHS expressions whose type cannot be inferred.
    target_is_unstructured_complex = (
        isinstance(target_type, VariantType)
        or _is_unstructured_array(target_type)
        or _is_unstructured_object(target_type)
    )
    if source_type is None and target_is_unstructured_complex:
        return source_col.cast(VariantType())
    if isinstance(target_type, VariantType):
        return source_col.cast(VariantType())
    if _is_unstructured_array(target_type) and isinstance(source_type, ArrayType):
        return source_col.cast(VariantType())
    if _is_unstructured_object(target_type) and isinstance(source_type, StructType):
        return source_col.cast(VariantType())
    if _is_unstructured_object(target_type) and isinstance(source_type, MapType):
        # Only accept MapType sources whose keys are strings.
        if not isinstance(source_type.key_type, StringType):
            return None
        return source_col.cast(VariantType())
    return None


def _check_top_level_field_ordering(
    target_fields: list[StructField],
    data_fields: list[StructField],
    snowpark_table_name: str,
    comparable_fn: Callable[[str], str],
) -> None:
    """Raise if ``data_fields`` are not in the same relative order as ``target_fields``.

    Only the positions of columns that appear in the data are checked, so a
    data schema that omits columns (NULL-padded on a mergeSchema write) or
    appends brand-new columns (added at the end of the merged schema) still
    validates, as long as the shared columns preserve the target's relative
    order. This mirrors Iceberg's check-ordering, which fires even under
    mergeSchema (SparkWriteBuilder validates the merged schema before
    committing the ALTER).
    """
    target_positions = {comparable_fn(f.name): i for i, f in enumerate(target_fields)}
    last_pos = -1
    last_data_field_name = None
    for data_field in data_fields:
        pos = target_positions.get(comparable_fn(data_field.name))
        if pos is None:
            # Column not present in the target ordering (e.g. a data column
            # that is neither in the table nor being merged). Ordering has no
            # meaning for it here; column-set validation handles it elsewhere.
            continue
        if pos <= last_pos:
            exception = AnalysisException(
                f"[INCOMPATIBLE_DATA_FOR_TABLE.INCOMPATIBLE_SCHEMA] "
                f"Cannot write incompatible dataset to table with schema "
                f"{snowpark_table_name}: "
                f"field '{data_field.name}' is out of order, before "
                f"'{last_data_field_name}'"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
        last_pos = pos
        last_data_field_name = data_field.name


def _validate_schema_for_append(
    table_schema: DataType,
    data_schema: DataType,
    snowpark_table_name: str,
    compare_structs: bool = False,
    check_nullability: bool = False,
    check_ordering: bool = False,
):
    """Validate that data_schema can be appended to table_schema.

    ANSI/STRICT modes consult _validate_store_assignment_field for atomic pairs;
    LEGACY uses the permissive atomic fallback. When check_nullability is True,
    raises if a nullable source field maps to a non-nullable target (like Iceberg).
    When check_ordering is True, raises if the data schema's column order does
    not match the table schema's column order (matching Iceberg behaviour).
    """
    policy = _store_assignment_policy()
    match (table_schema, data_schema):
        case (_, _) if table_schema == data_schema:
            return

        case (_, _) if _is_unstructured_object(table_schema) and isinstance(
            data_schema, StructType
        ):
            # Unstructured Snowflake OBJECT target accepts any Spark StructType source.
            return

        case (_, MapType() as data_map) if _is_unstructured_object(table_schema):
            # Unstructured Snowflake OBJECT target accepts a Spark MapType source
            # only when the map key is a StringType — OBJECT keys are strings.
            if not isinstance(data_map.key_type, StringType):
                exception = AnalysisException(
                    f"[INCOMPATIBLE_DATA_FOR_TABLE.CANNOT_SAFELY_CAST] Cannot write incompatible data for the table "
                    f"{snowpark_table_name}: Cannot safely cast {data_schema.simple_string()} to OBJECT "
                    f"(Snowflake OBJECT keys must be strings)."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception
            return

        case (StructType() as table_struct, StructType() as data_struct):

            def _comparable_col_name(col: str) -> str:
                # Nested struct comparison keeps quotes intact; top-level column
                # matching unquotes so e.g. `"Id"` matches `Id`.
                if compare_structs:
                    return (
                        col.upper()
                        if not global_config.spark_sql_caseSensitive
                        else col
                    )
                return comparable_col_name(col)

            def invalid_struct_schema():
                exception = AnalysisException(
                    f"Cannot resolve columns for the existing table {snowpark_table_name} ({table_schema.simple_string()}) with the data schema ({data_schema.simple_string()})."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception

            if len(table_struct.fields) != len(data_struct.fields):
                exception = AnalysisException(
                    f"The column number of the existing table {snowpark_table_name} ({table_schema.simple_string()}) doesn't match the data schema ({data_schema.simple_string()})."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception

            table_field_names = {
                _comparable_col_name(field.name) for field in table_struct.fields
            }
            data_field_names = {
                _comparable_col_name(field.name) for field in data_struct.fields
            }

            if table_field_names != data_field_names:
                invalid_struct_schema()

            if check_ordering:
                _check_top_level_field_ordering(
                    table_struct.fields,
                    data_struct.fields,
                    snowpark_table_name,
                    _comparable_col_name,
                )

            table_field_by_key = {
                _comparable_col_name(f.name): f for f in table_struct.fields
            }
            for data_field in data_struct.fields:
                matching_table_field = table_field_by_key.get(
                    _comparable_col_name(data_field.name)
                )

                if matching_table_field is None:
                    invalid_struct_schema()
                else:
                    if (
                        check_nullability
                        and not matching_table_field.nullable
                        and data_field.nullable
                    ):
                        _raise_optional_into_required(
                            data_field.name,
                            matching_table_field.name,
                            snowpark_table_name,
                        )
                    _validate_schema_for_append(
                        matching_table_field.datatype,
                        data_field.datatype,
                        snowpark_table_name,
                        compare_structs=True,
                        check_nullability=check_nullability,
                        check_ordering=check_ordering,
                    )

            return

        case (StringType(), _) if not isinstance(
            data_schema, (StructType, ArrayType, MapType)
        ):
            return

        case (_, _) if (
            _is_atomic_type(table_schema)
            and _is_atomic_type(data_schema)
            and not _store_assignment_is_legacy()
        ):
            # Must precede the numeric/numeric arm so narrowing (Long→Int
            # under STRICT) is rejected instead of silently accepted.
            # Lazy import: map_sql imports from this module at top level.
            from snowflake.snowpark_connect.relation.map_sql import (
                _validate_store_assignment_field,
            )

            if not _validate_store_assignment_field(data_schema, table_schema, policy):
                exception = AnalysisException(
                    f"[INCOMPATIBLE_DATA_FOR_TABLE.CANNOT_SAFELY_CAST] "
                    f"Cannot write incompatible data for the table {snowpark_table_name}: "
                    f"Cannot safely cast {data_schema.simple_string()} "
                    f"to {table_schema.simple_string()}"
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception
            return

        case (_, _) if isinstance(table_schema, _NumericType) and isinstance(
            data_schema, _NumericType
        ):
            return

        case (_, _) if (
            _is_atomic_type(table_schema)
            and _is_atomic_type(data_schema)
            and _store_assignment_is_legacy()
        ):
            return

        case (ArrayType() as table_array, ArrayType() as data_array) if (
            _is_unstructured_array(table_array)
        ):
            # Unstructured Snowflake ARRAY target accepts any Spark array source.
            return

        case (ArrayType() as table_array, ArrayType() as data_array):
            # Recurse on the element type only. Element nullability
            # (contains_null) is intentionally not checked: Snowflake-backed
            # Iceberg cannot create a non-nullable array element (DDL error
            # 093208), so a required-element target can't exist and there is
            # nothing to diverge from.
            _validate_schema_for_append(
                table_array.element_type,
                data_array.element_type,
                snowpark_table_name,
                check_nullability=check_nullability,
                check_ordering=check_ordering,
            )

        case (MapType() as table_map, MapType() as data_map):
            # Recurse on key/value types only. Value nullability
            # (value_contains_null) is not checked for the same reason as array
            # elements above: a non-nullable map value is unrepresentable in
            # Snowflake (093208).
            _validate_schema_for_append(
                table_map.key_type,
                data_map.key_type,
                snowpark_table_name,
                check_nullability=check_nullability,
                check_ordering=check_ordering,
            )
            _validate_schema_for_append(
                table_map.value_type,
                data_map.value_type,
                snowpark_table_name,
                check_nullability=check_nullability,
                check_ordering=check_ordering,
            )

        case (TimestampType(), _) if isinstance(data_schema, (DateType, TimestampType)):
            return
        case (DateType(), _) if isinstance(data_schema, (DateType, TimestampType)):
            return
        case (VariantType(), _):
            return
        case (_, _):

            def _safe_simple(t: DataType) -> str:
                try:
                    return t.simple_string()
                except Exception:
                    return repr(t)

            exception = AnalysisException(
                f"[INCOMPATIBLE_DATA_FOR_TABLE.CANNOT_SAFELY_CAST] Cannot write incompatible data for the table {snowpark_table_name}: Cannot safely cast {_safe_simple(data_schema)} to {_safe_simple(table_schema)}"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception


def _validate_data_columns_present_in_table(
    table_schema: StructType,
    data_schema: StructType,
    snowpark_table_name: str,
) -> None:
    if not global_config.spark_sql_caseSensitive:
        table_col_names = {
            unquote_if_quoted(f.name).upper() for f in table_schema.fields
        }
        data_col_names = {unquote_if_quoted(f.name).upper() for f in data_schema.fields}
    else:
        table_col_names = {unquote_if_quoted(f.name) for f in table_schema.fields}
        data_col_names = {unquote_if_quoted(f.name) for f in data_schema.fields}

    for table_field in table_schema.fields:
        comparable_name = (
            unquote_if_quoted(table_field.name).upper()
            if not global_config.spark_sql_caseSensitive
            else unquote_if_quoted(table_field.name)
        )
        if comparable_name not in data_col_names:
            exception = AnalysisException(
                f"[INCOMPATIBLE_DATA_FOR_TABLE.CANNOT_FIND_DATA] Cannot write incompatible data for the table "
                f"`{snowpark_table_name}`: Cannot find data for the output column `{unquote_if_quoted(table_field.name)}`."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception

    for data_field in data_schema.fields:
        comparable_name = (
            unquote_if_quoted(data_field.name).upper()
            if not global_config.spark_sql_caseSensitive
            else unquote_if_quoted(data_field.name)
        )
        if comparable_name not in table_col_names:
            exception = AnalysisException(
                f"[INCOMPATIBLE_DATA_FOR_TABLE.EXTRA_COLUMNS] Cannot write incompatible data for the table "
                f"`{snowpark_table_name}`: Cannot write extra columns `{unquote_if_quoted(data_field.name)}`."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception


def _validate_target_file_size(target_file_size: str | None):
    # validate target file size is in the acceptable values
    if target_file_size is None:
        return

    if target_file_size not in TARGET_FILE_SIZE_ACCEPTABLE_VALUES:
        exception = AnalysisException(
            f"Invalid value '{target_file_size}' for TARGET_FILE_SIZE. Allowed values: {', '.join(TARGET_FILE_SIZE_ACCEPTABLE_VALUES)}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
        raise exception


def _snowpark_type_to_iceberg_ddl(
    t: DataType, use_number_for_integrals: bool | None = None
) -> str:
    """Convert a Snowpark type to Snowflake DDL string for CREATE ICEBERG TABLE.

    For structured types (ARRAY, MAP, OBJECT), this function recursively builds
    typed DDL strings that match Snowflake's Iceberg table requirements.

    When snowpark.connect.integralTypesEmulation is enabled, integral types are
    mapped to NUMBER(precision, 0) to maintain Spark compatibility.

    Args:
        t: The Snowpark DataType to convert.
        use_number_for_integrals: Whether to use NUMBER(p,0) for integral types.
            If None (default), the value is determined once from config at the
            top level and passed down to recursive calls to avoid repeated lock
            acquisition.
    """
    # Determine integral type mapping once at top level, then pass to recursive calls
    if use_number_for_integrals is None:
        use_number_for_integrals = is_integral_types_conversion_enabled()

    if isinstance(t, StringType):
        return "VARCHAR"
    elif isinstance(t, IntegerType):
        return "NUMBER(10, 0)" if use_number_for_integrals else "INT"
    elif isinstance(t, LongType):
        return "NUMBER(19, 0)" if use_number_for_integrals else "BIGINT"
    elif isinstance(t, ShortType):
        return "NUMBER(5, 0)" if use_number_for_integrals else "SMALLINT"
    elif isinstance(t, ByteType):
        return "NUMBER(3, 0)" if use_number_for_integrals else "TINYINT"
    elif isinstance(t, DoubleType):
        return "DOUBLE"
    elif isinstance(t, FloatType):
        return "FLOAT"
    elif isinstance(t, DecimalType):
        return f"DECIMAL({t.precision},{t.scale})"
    elif isinstance(t, DateType):
        return "DATE"
    elif isinstance(t, TimestampType):
        # Handle timestamp timezone variants: NTZ, LTZ, TZ
        tz = getattr(t, "tz", "default")
        if tz == "ltz":
            return "TIMESTAMP_LTZ"
        elif tz == "tz":
            return "TIMESTAMP_TZ"
        else:  # 'ntz' or 'default'
            return "TIMESTAMP_NTZ"
    elif isinstance(t, BooleanType):
        return "BOOLEAN"
    elif isinstance(t, BinaryType):
        return "BINARY"
    elif isinstance(t, ArrayType):
        # Snowflake Iceberg requires typed ARRAY: ARRAY(<element_type>)
        element_type = _snowpark_type_to_iceberg_ddl(
            t.element_type, use_number_for_integrals
        )
        return f"ARRAY({element_type})"
    elif isinstance(t, MapType):
        # Snowflake Iceberg requires typed MAP: MAP(<key_type>, <value_type>)
        key_type = _snowpark_type_to_iceberg_ddl(t.key_type, use_number_for_integrals)
        value_type = _snowpark_type_to_iceberg_ddl(
            t.value_type, use_number_for_integrals
        )
        return f"MAP({key_type}, {value_type})"
    elif isinstance(t, StructType):
        # Snowflake Iceberg OBJECT(<key> <type>, ...) — render field names via
        # _cld_ddl_identifier (quoted + case-folded) for the same reason as
        # top-level columns (SNOW-3649315).
        fields = []
        for field in t.fields:
            field_name = _cld_ddl_identifier(field.name)
            field_type = _snowpark_type_to_iceberg_ddl(
                field.datatype, use_number_for_integrals
            )
            null_constraint = "" if field.nullable else " NOT NULL"
            fields.append(f"{field_name} {field_type}{null_constraint}")
        return f"OBJECT({', '.join(fields)})"
    elif isinstance(t, TimeType):
        return "TIME"
    elif isinstance(t, VariantType):
        return "VARIANT"
    else:
        # Types that fall back to VARCHAR include:
        # - YearMonthIntervalType/DayTimeIntervalType: No direct Iceberg equivalent
        # - GeographyType/GeometryType: Snowflake-specific spatial types not in Iceberg spec
        # - VectorType: Snowflake-specific ML type not in Iceberg spec
        # - NullType: Metadata-only type, no storage representation
        logger.warning(
            "Snowpark type %r has no direct Iceberg DDL equivalent; falling back to VARCHAR. "
            "Data may require explicit casting when read back.",
            type(t).__name__,
        )
        return "VARCHAR"


def _build_base_location_clause(
    options: dict | None = None,
    explicit: str | None = None,
) -> str:
    """Return the ``BASE_LOCATION = '<value>'`` fragment (no padding), or ``''``.

    Resolution order: ``explicit`` (caller-supplied, e.g. a Spark
    ``LOCATION`` clause) > write options (``base_location`` /
    ``iceberg.base_location`` / ``location``) > session config
    ``snowpark.connect.iceberg.base_location``. SCOS does not synthesize a
    default — when nothing is supplied, Snowflake either auto-derives from
    ``BASE_LOCATION_PREFIX`` on the catalog integration or rejects the DDL.
    SNOW-3471787.
    """
    value = explicit
    if not value and options:
        value = (
            options.get("base_location")
            or options.get("iceberg.base_location")
            or options.get("location")
        )
    if not value:
        value = sessions_config.get(get_spark_session_id(), {}).get(
            "snowpark.connect.iceberg.base_location"
        )
    if not value:
        return ""
    escaped = str(value).strip().replace("'", "''")
    if not escaped:
        return ""
    return f"BASE_LOCATION = '{escaped}'"


def _build_storage_serialization_policy_clause(options: dict | None = None) -> str:
    """Return the ``STORAGE_SERIALIZATION_POLICY = '<value>'`` fragment (no
    padding) for a CLD ``CREATE ICEBERG TABLE``, or ``''`` when unset.

    Reads the DataFrameWriter table properties ``storage_serialization_policy``
    / ``iceberg.storage_serialization_policy``. SCOS does not validate the
    value (``COMPATIBLE`` / ``OPTIMIZED``) — Snowflake validates it server-side,
    matching the managed ``iceberg_config`` path (SNOW-3310116).
    """
    if not options:
        return ""
    value = options.get("storage_serialization_policy") or options.get(
        "iceberg.storage_serialization_policy"
    )
    if not value:
        return ""
    escaped = str(value).strip().replace("'", "''")
    if not escaped:
        return ""
    return f"STORAGE_SERIALIZATION_POLICY = '{escaped}'"


def _build_target_file_size_clause(options: dict | None = None) -> str:
    """Return the ``TARGET_FILE_SIZE = '<value>'`` fragment (no padding) for a
    CLD ``CREATE ICEBERG TABLE``, or ``''`` when unset.

    Reads the DataFrameWriter table properties ``write.target-file-size`` /
    ``target_file_size`` and validates against the same allow-list as the
    managed path (:func:`_validate_target_file_size`). Unlike the managed
    ``iceberg_config`` path, no ``spark.sql.files.maxPartitionBytes`` fallback
    is applied — only an explicit per-table property is threaded, so a CLD
    write never acquires a ``TARGET_FILE_SIZE`` the user did not request
    (SNOW-3310116).
    """
    if not options:
        return ""
    value = options.get("write.target-file-size") or options.get("target_file_size")
    if not value:
        return ""
    _validate_target_file_size(value)
    escaped = str(value).strip().replace("'", "''")
    return f"TARGET_FILE_SIZE = '{escaped}'"


def _create_cld_iceberg_table_then_load(
    session: snowpark.Session,
    writer: snowpark.DataFrameWriter,
    snowpark_table_name: str,
    options: dict | None,
    partition_specs: list[V2PartitionSpec] | None = None,
    comment: str | None = None,
    iceberg_version: int | None = None,
) -> None:
    """Emit explicit ``CREATE ICEBERG TABLE`` for a CLD target, then append
    rows via Snowpark against the now-existing table.

    Mirrors the V1 CLD create path (which calls
    :func:`_create_cld_iceberg_table` inline) and is used by the V2
    ``MODE_CREATE`` / ``MODE_REPLACE`` / ``MODE_CREATE_OR_REPLACE`` arms;
    V1 itself still calls the inner DDL helper directly. The DDL step is
    what makes column casing CLD-correct on Glue / Unity case-insensitive
    catalogs: :func:`_create_cld_iceberg_table` routes each
    ``writer._dataframe`` field name through :func:`_cld_ddl_identifier`,
    which double-quotes the name (injection-safe, SNOW-3649315) and, on the
    default case-insensitive path, lower-cases it so the quoted identifier
    matches the catalog's case-folded storage (a quoted upper-case ``"ID"``
    is otherwise rejected with 004510). The load step then appends against
    the now-existing table, so Snowpark does not need to issue any DDL of
    its own (which would otherwise reintroduce the uppercase-quoted columns
    the CLD rejects).

    The load step is hard-coded to ``mode="append"`` on purpose. Any other
    mode (e.g. ``"overwrite"``) routes back through Snowpark's
    replace / DDL path that this helper exists to bypass on CLDs, and is
    not supported by any caller — all V2 REPLACE / CREATE_OR_REPLACE arms
    explicitly ``DROP TABLE IF EXISTS`` before invoking this helper.

    NB: callers must pass a writer obtained from
    :func:`_get_writer_for_table_creation` so ``writer._dataframe`` is
    already in the create-time shape (force-nullable schema, optional
    upper-cased column aliases on non-case-sensitive sessions).
    """
    _create_cld_iceberg_table(
        session,
        writer._dataframe,
        snowpark_table_name,
        options=options,
        partition_specs=partition_specs,
        comment=comment,
        iceberg_version=iceberg_version,
    )
    writer.saveAsTable(
        table_name=snowpark_table_name,
        mode="append",
        column_order=_column_order_for_write,
    )


def _cld_ddl_identifier(name: str) -> str:
    """Render a column/field identifier for a CLD ``CREATE ICEBERG TABLE`` DDL.

    Always double-quotes the name (escaping embedded ``"`` by doubling) so that
    names with spaces or other special characters can't break or inject into
    the DDL (SNOW-3649315).

    On the default case-insensitive path the name is lower-cased first.
    Catalog-linked databases over case-insensitive external catalogs (Glue,
    Unity) store identifiers lower-cased and reject a quoted upper-case name
    such as ``"ID"`` with ``004510`` ("Only lowercase and double-quoted
    identifier names are allowed"). Lower-casing makes the quoted name match
    the catalog's stored, case-folded identifier. It is skipped when
    ``spark.sql.caseSensitive`` is set, preserving the caller's explicit
    casing (which is the only case where mixed-case is intended, and which the
    catalog may then legitimately reject).

    This mirrors the case policy of the canonical CLD identifier transformer
    ``spark_to_sf_single_id`` / ``transform_identifier_for_snowflake`` (same
    ``spark.sql.caseSensitive`` gate) but additionally *always* double-quotes.
    That transformer returns ordinary names bare (case-insensitive, catalog-
    safe) yet also leaves special-character names unquoted — unsafe in
    hand-built DDL — so it cannot be reused directly here (SNOW-3649315).
    """
    bare = unquote_if_quoted(name)
    if not global_config.spark_sql_caseSensitive:
        bare = bare.lower()
    return quote_name_without_upper_casing(bare)


def _create_cld_iceberg_table(
    session: snowpark.Session,
    df: snowpark.DataFrame,
    table_name: str,
    options: dict | None = None,
    partition_cols: list[str] | None = None,
    partition_specs: list[V2PartitionSpec] | None = None,
    iceberg_version: int | None = None,
    comment: str | None = None,
) -> None:
    """Issue CREATE ICEBERG TABLE for a Catalog-Linked Database.

    CLDs require the explicit CREATE ICEBERG TABLE syntax. All identifiers
    (columns, partition cols, nested OBJECT fields) are quoted via
    quote_name_without_upper_casing to prevent broken DDL from names with
    special characters.

    Partitioning arrives one of two ways. ``partition_cols`` is a list of bare
    identity column names (the V1 path / SQL DDL path). ``partition_specs``
    carries DataFrameWriterV2 transforms (``DAY``/``BUCKET``/...): each spec's
    column is quoted on its own and the transform keyword is wrapped around the
    quoted identifier, so the keyword is never swept into the quoted name
    (SNOW-3310107). At most one of the two is set.
    """
    # Render identifiers via _cld_ddl_identifier: double-quoted (injection-safe,
    # SNOW-3649315) and lower-cased on the case-insensitive path so case-
    # insensitive Glue/Unity catalogs accept them.
    columns = []
    for field in df.schema.fields:
        col_name = _cld_ddl_identifier(field.name)
        col_type = _snowpark_type_to_iceberg_ddl(field.datatype)
        columns.append(f"{col_name} {col_type}")

    columns_ddl = ", ".join(columns)
    parts = [f"CREATE ICEBERG TABLE {table_name} ({columns_ddl})"]

    if partition_specs:
        rendered = [
            render_partition_transform(
                spec.transform,
                spec.num_buckets,
                quote_name_without_upper_casing(unquote_if_quoted(spec.column)),
            )
            for spec in partition_specs
        ]
        parts.append(f"PARTITION BY ({', '.join(rendered)})")
    elif partition_cols:
        safe_parts = [_cld_ddl_identifier(c) for c in partition_cols]
        parts.append(f"PARTITION BY ({', '.join(safe_parts)})")

    if iceberg_version is not None:
        parts.append(f"ICEBERG_VERSION = {iceberg_version}")

    base_location = _build_base_location_clause(options=options)
    if base_location:
        parts.append(base_location)

    storage_serialization_policy = _build_storage_serialization_policy_clause(options)
    if storage_serialization_policy:
        parts.append(storage_serialization_policy)

    target_file_size = _build_target_file_size_clause(options)
    if target_file_size:
        parts.append(target_file_size)

    if comment:
        parts.append(f"COMMENT = '{escape_sql_comment(comment)}'")

    ddl = " ".join(parts)
    session.sql(ddl).collect()


def _build_iceberg_config(
    options: dict,
    partition_cols: list[str] | None = None,
    is_cld: bool = False,
) -> dict | None:
    config: dict = {}

    ev = options.get("external_volume") or options.get("iceberg.external_volume")
    if not ev:
        ev = sessions_config.get(get_spark_session_id(), {}).get(
            "snowpark.connect.iceberg.external_volume", None
        )
    if ev:
        config["external_volume"] = ev

    for key in ("catalog", "base_location", "storage_serialization_policy"):
        val = options.get(key) or options.get(f"iceberg.{key}")
        if val:
            config[key] = val

    # Don't set default CATALOG for Catalog-Linked Databases (CLDs).
    # CLDs infer the catalog from the database's linked external catalog,
    # and Snowflake rejects the CATALOG property with error 094104.
    if "catalog" not in config and not is_cld:
        config["catalog"] = "SNOWFLAKE"

    if "base_location" not in config:
        location = options.get("location")
        if location and location != "":
            config["base_location"] = location

    tfs = options.get("write.target-file-size") or options.get("target_file_size")
    if not tfs:
        # SNOW-3674169: Fall back to the bucketed value derived from
        # spark.sql.files.maxPartitionBytes, if the user has set it. An
        # explicit per-table tableProperty above always wins.
        tfs = get_iceberg_target_file_size_for_writes()
    if tfs:
        _validate_target_file_size(tfs)
        config["target_file_size"] = tfs

    iceberg_version = _extract_iceberg_format_version(options)
    if iceberg_version is not None:
        config["iceberg_version"] = iceberg_version

    if partition_cols:
        config["partition_by"] = partition_cols

    # For CLDs, return empty dict (not None) so Snowpark creates an ICEBERG table.
    # Snowpark's logic: is_iceberg = iceberg_config is not None
    # Empty dict {} is truthy for "is not None" but falsy for bool(), so we
    # need explicit handling.
    if is_cld:
        return config  # May be empty dict, but that's fine for CLDs
    return config if config else None


def _extract_iceberg_format_version(options: dict) -> int | None:
    """Pull Spark Iceberg's ``format-version`` table property out of an
    options dict and convert it to the integer Snowpark wants for the
    ``iceberg_version`` key of ``iceberg_config``.

    Accepts the canonical Spark Iceberg key ``format-version`` as well as
    the iceberg-prefixed alias ``iceberg.format-version``. Returns ``None``
    when neither key is present (so callers don't override the Snowpark
    default of ``2`` unintentionally). An explicit ``None`` value for
    either key is treated as absent (also returns ``None``) — Spark
    Iceberg's own behavior for a missing property — so callers don't have
    to pre-filter their options dicts. Raises ``AnalysisException`` with
    ``INVALID_INPUT`` when the value cannot be parsed as an integer or
    when the resulting integer is outside ``{1, 2, 3}``.

    Numeric ``str`` and ``int`` values are both accepted; PySpark's
    ``WriteOperationV2.table_properties`` carries string values, but the
    legacy V1 ``.option("format-version", 2)`` call can deliver an ``int``
    from a notebook caller, so we accept both.
    """
    raw = options.get("format-version")
    if raw is None:
        raw = options.get("iceberg.format-version")
    if raw is None:
        return None
    try:
        version = int(raw)
    except (TypeError, ValueError):
        exception = AnalysisException(
            "Iceberg 'format-version' table property must be an integer in "
            f"{set(_SUPPORTED_ICEBERG_FORMAT_VERSIONS)}; got {raw!r}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if version not in _SUPPORTED_ICEBERG_FORMAT_VERSIONS:
        exception = AnalysisException(
            "Iceberg 'format-version' table property must be one of "
            f"{_SUPPORTED_ICEBERG_FORMAT_VERSIONS}; got {version}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    return version


def _reject_max_snapshot_age_for_cld(is_cld: bool, table_properties: dict) -> None:
    """Raise ``AnalysisException`` when ``max-snapshot-age.ms`` is specified
    for a CLD (Catalog-Linked Database) Iceberg table. ``max-snapshot-age.ms``
    is only supported for non-CLD iceberg tables.
    """
    if not is_cld:
        return
    if (
        "max-snapshot-age.ms" in table_properties
        or "iceberg.max-snapshot-age.ms" in table_properties
    ):
        exception = AnalysisException(
            "The 'max-snapshot-age.ms' table property is not supported for "
            "Catalog-Linked Database (CLD) Iceberg tables."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception


def _extract_max_snapshot_age_days(options: dict) -> int | None:
    """Convert Spark Iceberg's ``max-snapshot-age.ms`` table property to the
    integer days value Snowflake expects for ``DATA_RETENTION_TIME_IN_DAYS``.

    Accepts the canonical key ``max-snapshot-age.ms`` and the iceberg-prefixed
    alias ``iceberg.max-snapshot-age.ms``.  Returns ``None`` when neither key
    is present so callers don't override Snowflake's default unintentionally.

    The value must be an exact whole-day multiple (a multiple of
    ``_MS_PER_DAY`` = 86 400 000 ms).  Non-multiples, negative values, and
    non-numeric strings raise ``AnalysisException`` with ``INVALID_INPUT``
    rather than silently truncating; Snowflake's edition-specific upper bound
    (90 days for Enterprise, 1 day for Standard) is enforced server-side.
    A value of 0 is valid and disables Time Travel.
    """
    if "max-snapshot-age.ms" in options:
        raw = options["max-snapshot-age.ms"]
    elif "iceberg.max-snapshot-age.ms" in options:
        raw = options["iceberg.max-snapshot-age.ms"]
    else:
        return None
    try:
        ms = int(raw)
    except (TypeError, ValueError):
        exception = AnalysisException(
            "Iceberg 'max-snapshot-age.ms' table property must be a non-negative "
            f"integer number of milliseconds; got {raw!r}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if ms < 0:
        exception = AnalysisException(
            "Iceberg 'max-snapshot-age.ms' table property must be a non-negative "
            f"integer number of milliseconds; got {ms}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if ms % _MS_PER_DAY != 0:
        exception = AnalysisException(
            f"Iceberg 'max-snapshot-age.ms' must be an exact multiple of "
            f"{_MS_PER_DAY} ms (1 day) because Snowflake's "
            f"DATA_RETENTION_TIME_IN_DAYS only accepts whole days; "
            f"got {ms} ms ({ms / _MS_PER_DAY:.4f} days)."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    return ms // _MS_PER_DAY


def _is_external_catalog_error(exc: SnowparkSQLException) -> bool:
    """Return ``True`` when *exc* indicates the table belongs to an external
    catalog and therefore cannot be overwritten via CREATE OR REPLACE."""

    # Snowflake SQL error codes that indicate an external catalog table cannot be
    # overwritten via CREATE OR REPLACE (CTAS).  When we encounter these during an
    # iceberg overwrite we fall back to TRUNCATE + APPEND which preserves the
    # existing table definition (and its catalog integration).
    #   091378 – "Column specifications are only allowed for Iceberg tables using
    #            the Snowflake catalog or Iceberg tables created within a
    #            catalog-linked database."
    #   093664 – "CTAS is not supported for this table type."
    _EXTERNAL_CATALOG_OVERWRITE_ERROR_CODES = {91378, 93664}
    error_code = getattr(exc, "sql_error_code", None)
    if (
        error_code is not None
        and int(error_code) in _EXTERNAL_CATALOG_OVERWRITE_ERROR_CODES
    ):
        return True
    # Belt-and-suspenders: also match on message substrings in case the
    # numeric code is not surfaced in exception object.
    msg = str(exc)
    return (
        "Column specifications are only allowed for Iceberg tables using the Snowflake catalog"
        in msg
        or "CTAS is not supported for this table type" in msg
        or "CREATE ICEBERG TABLE with COPY GRANTS is not supported in Catalog-Linked Databases"
        in msg
    )


def _is_unmanaged_transaction_error(exc: SnowparkSQLException) -> bool:
    """Return ``True`` when *exc* indicates an unmanaged (external-catalog /
    catalog-linked-database) Iceberg table was modified inside a multi-statement
    transaction, which Snowflake rejects.

    Snowpark's ``overwrite_condition`` performs an *atomic* (transaction-wrapped)
    targeted delete+insert. Unmanaged Iceberg tables do not allow that, surfacing:
      091586 – "Unmanaged Iceberg tables cannot be modified within a
               multi-statement transaction."
    We catch it to fall back to a non-atomic targeted DELETE + APPEND.
    """
    error_code = getattr(exc, "sql_error_code", None)
    if error_code is not None and int(error_code) == 91586:
        return True
    return "cannot be modified within a multi-statement transaction" in str(exc)


def _overwrite_with_condition_and_cld_fallback(
    writer: snowpark.DataFrameWriter,
    snowpark_table_name: str,
    overwrite_condition: snowpark.Column,
    session: snowpark.Session,
    is_iceberg: bool,
    iceberg_config: dict | None = None,
) -> None:
    """Shared core for condition-targeted overwrites with a non-atomic fallback
    for unmanaged (CLD / external-catalog) Iceberg tables.

    Used by overwrite with a condition and overwrite partitions.

    The normal path is Snowpark's ``overwrite_condition``, an *atomic*
    DELETE+INSERT wrapped in a transaction. CLD tables reject multi-statement
    transactions (Snowflake error 091586), so on that error we fall back to a
    non-atomic DELETE + APPEND. For non-iceberg (FDN) tables or any non-091586
    error, the ``SnowparkSQLException`` is wrapped in an ``AnalysisException``
    with table context and re-raised (``is_iceberg=False`` disables the CLD
    fallback path entirely).

    The fallback is not atomic: if the APPEND fails after the DELETE commits,
    the matched rows are left absent until the next successful write (same
    trade-off as ``_overwrite_iceberg_with_fallback``).
    """
    extra = {"iceberg_config": iceberg_config} if iceberg_config is not None else {}
    try:
        writer.saveAsTable(
            table_name=snowpark_table_name,
            table_exists=True,
            mode="overwrite",
            column_order=_column_order_for_write,
            overwrite_condition=overwrite_condition,
            **extra,
        )
    except SnowparkSQLException as exc:
        if not (is_iceberg and _is_unmanaged_transaction_error(exc)):
            exception = AnalysisException(
                f"Failed to overwrite table {snowpark_table_name} with condition: "
                f"{exc.message or str(exc)}"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception from exc

        # CLD (unmanaged) Iceberg tables reject the atomic DELETE+INSERT
        # transaction (Snowflake error 091586: "Unmanaged Iceberg tables cannot
        # be modified within a multi-statement transaction"). Fall back to a
        # non-atomic targeted DELETE followed by an APPEND.
        #
        # The rejected atomic write is compiled as BEGIN TRANSACTION; DELETE;
        # INSERT; COMMIT run as separate statements. BEGIN succeeded and the
        # DELETE then failed, so the transaction is left OPEN on the session;
        # without this ROLLBACK the fallback DML below runs inside that same
        # transaction and hits 091586 again.
        logger.warning(
            "Unmanaged (CLD) Iceberg table %s rejected the atomic "
            "overwrite-with-condition write (Snowflake error 091586 — "
            "unmanaged tables cannot be modified within a multi-statement "
            "transaction). Falling back to a non-atomic DELETE + APPEND. "
            "If the APPEND fails after the DELETE commits, the matched rows "
            "will be absent until the next successful write.",
            snowpark_table_name,
        )
        session.sql("ROLLBACK").collect()
        session.table(snowpark_table_name).delete(overwrite_condition)
        writer.saveAsTable(
            table_name=snowpark_table_name,
            table_exists=True,
            mode="append",
            column_order=_column_order_for_write,
            **extra,
        )


def _overwrite_partitions_with_unmanaged_fallback(
    input_df: snowpark.DataFrame,
    snowpark_table_name: str,
    table_schema_or_error: StructType,
    overwrite_condition: snowpark.Column,
    session: snowpark.Session,
    iceberg_config: dict | None = None,
    check_nullability: bool = False,
    check_ordering: bool = True,
) -> None:
    """Apply a partition-targeted overwrite, with a non-atomic fallback for
    unmanaged (external-catalog / CLD) Iceberg tables.

    The normal path is Snowpark's ``overwrite_condition``, an *atomic*
    delete+insert wrapped in a transaction. Unmanaged Iceberg tables reject
    multi-statement transactions (091586), so on that error we fall back to a
    non-atomic equivalent: a single ``DELETE`` of the matching partitions, then
    an ``append``. This preserves dynamic-partition semantics (only the matching
    partitions are replaced) — unlike the full-table TRUNCATE fallback used for
    plain overwrite. The fallback is not atomic: if the append fails after the
    delete, the targeted partitions are left empty (same tradeoff as
    ``_overwrite_iceberg_with_fallback``); schema validation is performed here
    via ``_validate_schema_for_append`` (SNOW-3310108), so the caller does not
    need to validate separately.
    """
    # Partition overwrite is an INSERT OVERWRITE into an existing table, so the
    # writer must match the table's stored identifiers — never impose fresh
    # casing. "overwrite" mode would uppercase names via
    # _get_writer_for_table_creation, breaking quoted-lowercase columns like
    # '"age"' (CLD / external-catalog Iceberg or externally-created tables) and
    # skipping schema validation + type-cast alignment. "append" validates,
    # aligns to the live schema, and casts to the table's column types — correct
    # for both the mergeSchema and non-mergeSchema cases. Threading
    # check_nullability through the validating append path enforces Iceberg's
    # nullability check (Iceberg applies it to overwritePartitions too).
    writer = _validate_schema_and_get_writer(
        input_df,
        "append",
        snowpark_table_name,
        table_schema_or_error,
        check_nullability=check_nullability,
        check_ordering=check_ordering,
    )
    _overwrite_with_condition_and_cld_fallback(
        writer=writer,
        snowpark_table_name=snowpark_table_name,
        overwrite_condition=overwrite_condition,
        session=session,
        is_iceberg=True,  # this function is only called for Iceberg tables
        iceberg_config=iceberg_config,
    )


def _overwrite_iceberg_with_fallback(
    writer: snowpark.DataFrameWriter,
    snowpark_table_name: str,
    iceberg_config: dict | None,
    session: snowpark.Session,
    input_df: snowpark.DataFrame | None = None,
    comment: str | None = None,
    data_retention_time_days: int | None = None,
) -> None:
    """Try a normal Snowpark ``mode='overwrite'`` (CREATE OR REPLACE).

    Used only by the *rebuild* modes — ``MODE_REPLACE`` and
    ``MODE_CREATE_OR_REPLACE`` — which intentionally replace the table
    definition. ``MODE_OVERWRITE`` no longer routes here (it preserves the
    definition via INSERT OVERWRITE; see ``map_write_v2``).

    For Snowflake-managed iceberg this is an atomic CREATE OR REPLACE. If the
    table belongs to an external catalog (Glue, Polaris, …) the CREATE OR
    REPLACE is rejected; we fall back to a single **atomic** ``INSERT
    OVERWRITE INTO`` that replaces every row of the existing table in one
    statement. Either the new snapshot is fully committed or the old one is
    preserved — matching Spark's V2 replace/createOrReplace atomicity
    contract.

    Schema evolution is not supported for external catalog tables via this
    path - the column set is owned by the external catalog. The schema is
    validated up front (fail-fast, before any DML), and if the INSERT
    OVERWRITE fails for any other reason the error propagates so the table's
    existing data is left intact.
    """
    try:
        writer.saveAsTable(
            table_name=snowpark_table_name,
            mode="overwrite",
            column_order=_column_order_for_write,
            iceberg_config=iceberg_config,
            copy_grants=True,
            comment=comment,
            data_retention_time=data_retention_time_days,
        )
    except SnowparkSQLException as e:
        if not _is_external_catalog_error(e):
            raise

        logger.info(
            "Overwrite failed for external-catalog iceberg table %s; "
            "falling back to atomic INSERT OVERWRITE.",
            snowpark_table_name,
        )

        # Validate that the DataFrame schema is compatible with the target
        # table before issuing any DML. INSERT OVERWRITE is atomic, but a
        # schema mismatch should fail fast with a clear error.
        if input_df is not None:
            table_schema = session.table(snowpark_table_name).schema
            _validate_schema_for_append(
                table_schema, input_df.schema, snowpark_table_name
            )

        # SNOW-3517523: Atomic full overwrite. Under the hood Snowpark compiles
        # ``mode='truncate'`` + ``table_exists=True`` into a single
        # ``INSERT OVERWRITE INTO`` statement (NOT a literal TRUNCATE), which
        # Snowflake commits atomically: the old snapshot survives if the write
        # fails. ``table_exists=True`` is required so Snowpark does not attempt
        # a CREATE OR REPLACE (CTAS), which external catalogs reject. We keep
        # ``column_order='name'`` for name-based column matching, same as the
        # managed path above.
        #
        # Deliberately NO TRUNCATE+APPEND fallback here: that path is
        # non-atomic and can silently empty the table if the APPEND fails. Any
        # failure of the INSERT OVERWRITE below must propagate (hard error) so
        # the existing data is preserved.
        # iceberg_config intentionally omitted: the old TRUNCATE+APPEND path
        # passed it to recreate table-creation parameters on each write, but
        # INSERT OVERWRITE INTO operates on the existing table and does not
        # accept table-creation parameters. Snowflake uses the table's existing
        # catalog configuration (external volume, catalog integration)
        # automatically.
        writer.saveAsTable(
            table_name=snowpark_table_name,
            table_exists=True,
            mode="truncate",
            column_order=_column_order_for_write,
        )

        # The INSERT OVERWRITE above swaps rows only; it cannot carry the
        # table `comment` the way the rejected CREATE OR REPLACE would have.
        # Apply it separately via ALTER. Best-effort: the external catalog
        # may reject SET COMMENT just as it rejected CREATE OR REPLACE — the
        # data write is already committed, so a comment failure must not fail
        # the whole replace (it only leaves the comment unset, matching the
        # prior behavior).
        if comment:
            try:
                session.sql(
                    f"ALTER ICEBERG TABLE {snowpark_table_name} "
                    f"SET COMMENT = '{escape_sql_comment(comment)}'"
                ).collect()
            except SnowparkSQLException as comment_exc:
                logger.warning(
                    "Could not set comment on external-catalog iceberg table "
                    "%s after INSERT OVERWRITE: %s",
                    snowpark_table_name,
                    comment_exc,
                )


def _is_complex_structured_type(dt: DataType) -> bool:
    """Return True if the datatype is a structured complex type (ARRAY, MAP, STRUCT)."""
    if isinstance(dt, (ArrayType, MapType, StructType)):
        return getattr(dt, "structured", False)
    return False


def _rewrite_df_for_parquet(input_df: snowpark.DataFrame) -> snowpark.DataFrame:
    """
    Cast structured complex-type columns to VARIANT before COPY INTO.

    Snowflake's COPY INTO cannot serialize structured types (ARRAY(T), MAP(K,V),
    STRUCT) directly to Parquet — it fails with "Cannot determine equivalent
    parquet data type".  Casting to VARIANT converts the data to semi-structured
    form that Snowflake *can* write to Parquet.

    On read, the FLATTEN-based schema discovery in map_read_parquet.py detects
    VARIANT columns, infers the nested schema, and casts back to structured types.
    """
    new_cols = []
    needs_rewrite = False
    for co in input_df.columns:
        field_dt = input_df.schema[co].datatype
        if _is_complex_structured_type(field_dt):
            new_cols.append(col(co).cast(VariantType()).alias(co))
            needs_rewrite = True
        else:
            new_cols.append(col(co))

    if not needs_rewrite:
        return input_df

    return input_df.select(new_cols)


def _resolve_ignore_null_fields(options: dict | None) -> bool:
    """
    Resolve the Spark JSON write option ``ignoreNullFields`` from the user-provided
    options dict in a case-insensitive way (SNOW-3295619).

    Spark's default is ``true`` — null-valued fields are omitted from each output
    JSON object. Returning ``True`` here means the caller should use
    OBJECT_CONSTRUCT (which drops null keys); ``False`` means
    OBJECT_CONSTRUCT_KEEP_NULL (which preserves them).

    Reference: https://spark.apache.org/docs/3.5.6/sql-data-sources-json.html
    """
    if not options:
        return True
    for key, value in options.items():
        if key.lower() == "ignorenullfields":
            return str_to_bool(str(value))
    return True


def _build_json_value_expr(
    col_expr: snowpark.Column,
    dtype: DataType,
    keep_null: bool,
) -> snowpark.Column:
    """
    Build the OBJECT_CONSTRUCT[_KEEP_NULL] expression for one column value,
    recursively unpacking nested StructType columns so the ``ignoreNullFields``
    toggle (SNOW-3295619) applies at every level.

    For nested structured OBJECT(...) types, OBJECT_CONSTRUCT[_KEEP_NULL] cannot
    consume the column directly — Snowflake rejects it with "Function
    OBJECT_CONSTRUCT does not support OBJECT(...) argument type". Recursively
    unpacking the fields sidesteps this and also gives us the right semantics
    when the user asks for nested nulls to be dropped or kept.

    A null struct value must serialize as JSON ``null`` (matching Spark), not as
    an object built from its null fields. Unpacking a null struct would yield
    ``{}`` (drop-null) or ``{"x":null,...}`` (keep-null), so guard the
    constructed object with a null check that collapses a null struct to SQL
    NULL. The caller's top-level OBJECT_CONSTRUCT[_KEEP_NULL] then drops or keeps
    that null exactly as Spark's ``ignoreNullFields`` dictates.

    Structured ARRAY/MAP columns cannot be consumed by OBJECT_CONSTRUCT either
    (Snowflake rejects "ARRAY(OBJECT(...)) argument type"), so cast them to
    VARIANT — matching the pre-existing write path. Applying ``ignoreNullFields``
    to structs nested inside array elements / map values would require
    transform/map_values recursion and is tracked as a follow-up (SNOW-3295619).
    """
    if isinstance(dtype, StructType):
        construct_fn = object_construct_keep_null if keep_null else object_construct
        kv_pairs: list[snowpark.Column] = []
        for field in dtype.fields:
            kv_pairs.append(lit(field.name))
            kv_pairs.append(
                _build_json_value_expr(col_expr[field.name], field.datatype, keep_null)
            )
        return when(col_expr.is_null(), lit(None)).otherwise(construct_fn(*kv_pairs))
    if _is_complex_structured_type(dtype):
        return col_expr.cast(VariantType())
    return col_expr


def rewrite_df(
    input_df: snowpark.DataFrame,
    source: str,
    options: dict | None = None,
) -> snowpark.DataFrame:
    """
    Rewrite dataframe if needed.
        json: construct the dataframe to 1 column in json format
            1. Append columns which represents the column name
            2. Use object_construct (or object_construct_keep_null when the
               Spark ``ignoreNullFields`` write option is false — SNOW-3295619)
               to aggregate the dataframe into 1 column. Recurses into nested
               StructType columns so the toggle applies at every level.
        csv:
            Use "" to replace empty string
    """
    match source:
        case "json":
            keep_null = not _resolve_ignore_null_fields(options)
            construct_fn = object_construct_keep_null if keep_null else object_construct
            rand_salt = random_string(10, "_")
            rewritten_df = input_df.with_columns(
                [co + rand_salt for co in input_df.columns],
                [lit(unquote_if_quoted(co)) for co in input_df.columns],
            )
            schema = input_df.schema
            construct_key_values: list[snowpark.Column] = []
            for co in input_df.columns:
                construct_key_values.append(col(co + rand_salt))
                construct_key_values.append(
                    _build_json_value_expr(col(co), schema[co].datatype, keep_null)
                )
            return rewritten_df.select(construct_fn(*construct_key_values))
        case "csv":
            options = options or {}
            empty_value = next(
                (v for k, v in options.items() if k.lower() == "emptyvalue"),
                None,
            )
            # SNOW-3389610: when the user sets `emptyValue`, pre-project
            # "" -> the user's token. Otherwise, keep the existing default of
            # "" -> the literal '""' so an empty string round-trips back as
            # an empty string (distinguishable from NULL via NULL_IF). NULL
            # is preserved either way (handled by NULL_IF on the Snowflake
            # side via `nullValue` -> `NULL_IF`).
            empty_replacement = (
                lit(empty_value) if empty_value is not None else lit('""')
            )
            new_cols = []
            for co in input_df.columns:
                if isinstance(input_df.schema[co].datatype, StringType):
                    new_col = col(co)
                    new_col = when(
                        new_col.isNotNull() & (new_col == ""), empty_replacement
                    ).otherwise(new_col)
                    new_cols.append(new_col.alias(co))
                else:
                    new_cols.append(col(co))
            return input_df.select(new_cols)
        case "parquet":
            return _rewrite_df_for_parquet(input_df)
        case _:
            return input_df


def _map_overwrite_condition(
    condition_proto,
    container: DataFrameContainer,
    input_df: snowpark.DataFrame,
) -> snowpark.Column:
    # saveAsTable(overwrite_condition=...) generates SQL against the target
    # table, so column references must use target-table identifiers (produced
    # by spark_to_sf_single_id) rather than the internal Snowpark names that
    # live in the container's column map.
    spark_names = container.column_map.get_spark_columns()
    table_snowpark_names = [
        spark_to_sf_single_id(name, is_column=True) for name in spark_names
    ]
    condition_column_map = ColumnNameMap(
        spark_column_names=spark_names,
        snowpark_column_names=table_snowpark_names,
    )
    typer = ExpressionTyper(input_df)
    _, typed_col = map_expression(condition_proto, condition_column_map, typer)
    return typed_col.col


def handle_column_names(
    container: DataFrameContainer, source: str
) -> tuple[snowpark.DataFrame, list[str], list[str], list | None]:
    """
    Handle column names before write so they match spark schema.

    Returns:
        A 4-tuple of (dataframe, snowpark_column_names, spark_column_names, qualifiers).

    Raises:
        AnalysisException: If the column map contains duplicate Spark column names
            (COLUMN_ALREADY_EXISTS), matching Spark's behaviour for star-expansion +
            explicit alias conflicts (SNOW-3372861).
    """
    df = container.dataframe
    column_map = container.column_map

    if source == "jdbc":
        # don't change column names for jdbc sources as we directly use spark column names for writing to the destination tables.
        return (
            df,
            column_map.get_snowpark_columns(),
            column_map.get_spark_columns(),
            column_map.get_qualifiers(),
        )

    snowpark_column_names: list[str] = []
    spark_column_names: list[str] = []
    qualifiers: list | None = None
    if column_map.columns:
        raw_pairs = [
            (column, quote_name_without_upper_casing(column.spark_name))
            for column in column_map.columns
        ]

        # Raise COLUMN_ALREADY_EXISTS for duplicate names, matching Spark's behaviour.
        # Delegate normalisation to ColumnNameMap so case-sensitivity is handled
        # consistently with the rest of the column-name pipeline (upper when
        # case-insensitive, identity when case-sensitive).
        seen: set[str] = set()
        for column, _quoted_name in raw_pairs:
            key = column_map._normalized_spark_name(column.spark_name)
            if key in seen:
                exception = AnalysisException(
                    f"[COLUMN_ALREADY_EXISTS] The column `{column.spark_name}` already exists. "
                    "Consider to choose another name or rename the existing column."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                raise exception
            seen.add(key)

        spark_column_names = [column.spark_name for column, _ in raw_pairs]
        snowpark_column_names = [quoted_name for _, quoted_name in raw_pairs]
        df = df.select(
            [
                col(column.snowpark_name).alias(snowpark_column_name)
                for column, snowpark_column_name in raw_pairs
            ]
        )
        qualifiers = column_map.get_qualifiers()

    return df, snowpark_column_names, spark_column_names, qualifiers


def _generate_metadata_files(
    source: str,
    write_path: str,
    stage_path: str,
    schema: StructType,
    session: snowpark.Session,
    parameters: dict,
    is_local_path: bool,
) -> None:
    """
    Generate marker and metadata files after write completes.

    Handles _SUCCESS marker files and Parquet _common_metadata generation
    for both local and cloud/stage paths.

    Args:
        source: Write format (csv, parquet, json, etc.)
        write_path: Original write path (local or cloud)
        stage_path: Stage path where files were written
        schema: DataFrame schema
        session: Snowpark session
        parameters: Write parameters
        is_local_path: Whether writing to local filesystem
    """
    generate_success = get_success_file_generation_enabled()
    generate_parquet_metadata = (
        source == "parquet" and get_parquet_metadata_generation_enabled()
    )

    if is_local_path:
        # Local path: write files directly
        if generate_success:
            _write_success_file_locally(write_path)
        if generate_parquet_metadata:
            _write_parquet_metadata_files_locally(write_path, schema)
    else:
        # Cloud/stage path: upload via stage operations
        if generate_success:
            _write_success_file_to_stage(stage_path, session, parameters)
        if generate_parquet_metadata:
            _upload_common_metadata_to_stage(stage_path, schema, session)


def _write_success_file_locally(directory_path: str) -> None:
    """
    Write a _SUCCESS marker file to a local directory.
    """
    try:
        success_file = Path(directory_path) / "_SUCCESS"
        success_file.touch()
        logger.debug(f"Created _SUCCESS file at {directory_path}")
    except Exception as e:
        logger.warning(f"Failed to create _SUCCESS file at {directory_path}: {e}")


def _write_csv_header_only_file(
    rewritten_df: snowpark.DataFrame,
    session: snowpark.Session,
    parameters: dict[str, Any],
) -> None:
    """SNOW-3389612 Sub-fix A.

    When `df.write.option("header", True).csv(path)` is called on an empty
    DataFrame, Spark writes a single header-only file (column names + newline,
    no data rows). Snowflake's COPY INTO LOCATION skips empty unloads
    entirely, leaving the target stage with no output file at all, so the
    subsequent read sees an empty schema instead of the original columns.

    To match Spark, synthesize the header file: build a 1-row DataFrame whose
    row IS the column names, and write it with header=False. The output file
    will contain a single line with the column names — functionally
    identical to a header-only file.
    """
    column_names = [f.name for f in rewritten_df.schema.fields]
    header_row_df = session.create_dataframe(
        [tuple(column_names)],
        schema=StructType([StructField(c, StringType()) for c in column_names]),
    )
    header_params = copy.deepcopy(parameters)
    # We ARE the header line — don't have Snowflake prepend another one.
    header_params["header"] = False
    # Empty + partitionBy is degenerate; the call site already excludes that
    # case, so this is just defensive.
    header_params.pop("partition_by", None)
    header_row_df.write.copy_into_location(**header_params)


def _write_success_file_to_stage(
    stage_path: str,
    session: snowpark.Session,
    parameters: dict,
) -> None:
    """
    Write a _SUCCESS marker file to a stage location.
    """
    try:
        # Create a dummy dataframe with one row containing "SUCCESS"
        success_df = session.create_dataframe([["SUCCESS"]]).to_df(["STATUS"])
        success_params = copy.deepcopy(parameters)

        success_params.pop("partition_by", None)

        success_params["location"] = f"{stage_path}/_SUCCESS"
        success_params["single"] = True
        success_params["header"] = True

        # Set CSV format with explicit no compression for _SUCCESS file
        success_params["file_format_type"] = "csv"
        success_params["format_type_options"] = {
            "COMPRESSION": "NONE",
        }

        success_df.write.copy_into_location(**success_params)

        logger.debug(f"Created _SUCCESS file at {stage_path}")
    except Exception as e:
        logger.warning(f"Failed to create _SUCCESS file at {stage_path}: {e}")


def _get_metadata_upload_sproc() -> str:
    """
    Get the cached metadata upload stored procedure.

    Returns:
        Fully qualified name of the cached stored procedure
    """
    sproc_body = """import base64
import tempfile
import os

def upload_file(session, file_content_b64: str, file_name: str, target_stage: str):
    import base64
    import tempfile
    import os

    # Decode base64 content
    file_content = base64.b64decode(file_content_b64)

    # Create temp directory and write file with exact name
    temp_dir = tempfile.mkdtemp()
    tmp_file_path = os.path.join(temp_dir, file_name)

    with open(tmp_file_path, 'wb') as f:
        f.write(file_content)

    try:
        # Use session.file.put() - works for both internal and external stages in sproc context
        result = session.file.put(
            tmp_file_path,
            target_stage,
            auto_compress=False,
            overwrite=True
        )

        # Extract status from result
        if result and len(result) > 0:
            status = result[0].status if hasattr(result[0], 'status') else str(result[0])
        else:
            status = "uploaded"

        return "Uploaded " + file_name + " Status: " + status
    finally:
        # Clean up temp files
        try:
            os.unlink(tmp_file_path)
            os.rmdir(temp_dir)
        except (OSError, IOError):
            pass"""

    # Use the cached sproc system for better performance and schema/database change handling
    return register_cached_sproc(
        sproc_body=sproc_body,
        handler_name="upload_file",
        input_arg_types=["STRING", "STRING", "STRING"],
        return_type="STRING",
        runtime_version="3.11",
        packages=["snowflake-snowpark-python"],
    )


def _upload_file_to_stage_via_sproc(
    local_file_path: Path, stage_path: str, session: snowpark.Session
) -> None:
    """
    Upload a file to a stage using the reusable stored procedure. We cannot directly use session.file.put() as it doesn't support external stages.

    Args:
        local_file_path: Local file to upload
        stage_path: Target stage path (e.g., @STAGE_NAME/path)
        session: Snowpark session
    """
    import base64

    sproc_name = _get_metadata_upload_sproc()

    with open(local_file_path, "rb") as f:
        file_content = f.read()

    file_content_b64 = base64.b64encode(file_content).decode("utf-8")
    file_name = "_common_metadata"
    session.call(sproc_name, file_content_b64, file_name, stage_path)

    logger.debug(f"Uploaded {file_name} to {stage_path} via stored procedure")


def _upload_common_metadata_to_stage(
    stage_path: str, snowpark_schema: StructType, session: snowpark.Session
) -> None:
    """
    Generate and upload _common_metadata file to a stage.

    Converts Snowpark → PySpark → Spark JSON, creates PyArrow schema with Spark metadata,
    then uploads to stage via temporary stored procedure (supports internal and external stages).

    Args:
        stage_path: Stage path where to upload _common_metadata (e.g., @STAGE/path)
        snowpark_schema: DataFrame schema (already in memory)
        session: Snowpark session for uploading
    """
    try:
        import tempfile

        spark_only_schema = _create_spark_schema_from_snowpark(snowpark_schema)

        with tempfile.NamedTemporaryFile(
            suffix="_common_metadata", delete=False
        ) as tmp_file:
            tmp_path = Path(tmp_file.name)
            pq.write_metadata(spark_only_schema, tmp_path)
            _upload_file_to_stage_via_sproc(tmp_path, stage_path, session)
            tmp_path.unlink()

        logger.debug(f"Created _common_metadata at {stage_path}")

    except ImportError:
        logger.warning(
            "PyArrow is required to generate Parquet metadata files. "
            "Install with: pip install pyarrow"
        )
    except Exception as e:
        logger.warning(f"Failed to create _common_metadata file: {e}")


def _create_spark_schema_from_snowpark(snowpark_schema: StructType) -> pa.Schema:
    """
    Create PyArrow schema with Spark metadata from Snowpark schema.
    """
    # Unquote field names (Snowpark may have quoted names like "ab")
    unquoted_fields = []
    for field in snowpark_schema.fields:
        unquoted_name = unquote_if_quoted(field.name)
        unquoted_fields.append(
            snowpark.types.StructField(
                unquoted_name, field.datatype, field.nullable, _is_column=False
            )
        )
    unquoted_snowpark_schema = snowpark.types.StructType(
        unquoted_fields, structured=snowpark_schema.structured
    )
    pyspark_schema = map_snowpark_to_pyspark_types(unquoted_snowpark_schema)
    spark_schema_json = pyspark_schema.json()

    spark_metadata = {
        b"org.apache.spark.version": SPARK_VERSION.encode("utf-8"),
        b"org.apache.spark.sql.parquet.row.metadata": spark_schema_json.encode("utf-8"),
    }

    # Convert PySpark to PyArrow for the physical schema structure
    # NOTE: Spark reads schema from the JSON metadata above, NOT from the Parquet schema!
    # However, correct Parquet types are needed as fallback if JSON parsing fails,
    # and for compatibility with non-Spark tools (PyArrow, Dask, Presto, etc.)
    arrow_fields = []
    for field in pyspark_schema.fields:
        pa_type = map_pyspark_types_to_pyarrow_types(field.dataType)
        arrow_fields.append(pa.field(field.name, pa_type, nullable=field.nullable))

    return pa.schema(arrow_fields, metadata=spark_metadata)


def _write_parquet_metadata_files_locally(
    write_path: str, snowpark_schema: StructType
) -> None:
    """
    Generate _common_metadata file for local Parquet datasets.

    Only generates _common_metadata (not _metadata) for consistency with cloud paths,
    where downloading all files for row group statistics would be inefficient.
    """
    try:
        local_path = Path(write_path)
        spark_only_schema = _create_spark_schema_from_snowpark(snowpark_schema)
        pq.write_metadata(spark_only_schema, local_path / "_common_metadata")

        logger.debug(f"Created _common_metadata at {write_path}")

    except ImportError:
        logger.warning(
            "PyArrow is required to generate Parquet metadata files. "
            "Install with: pip install pyarrow"
        )
    except Exception as e:
        logger.warning(f"Failed to create _common_metadata file: {e}")


def store_files_locally(
    stage_path: str, target_path: str, overwrite: bool, session: snowpark.Session
) -> None:
    target_path = convert_file_prefix_path(target_path)
    real_path = (
        Path(target_path).expanduser()
        if target_path.startswith("~/")
        else Path(target_path)
    )
    if overwrite and os.path.isdir(target_path):
        _truncate_directory(real_path)
    # Per Snowflake docs: "The command does not preserve stage directory structure when transferring files to your client machine"
    # https://docs.snowflake.com/en/sql-reference/sql/get
    # Preserve directory structure under stage_path by listing files and
    # downloading each into its corresponding local subdirectory when partition subdirs exist.
    # Otherwise, fall back to a direct GET which flattens.

    # TODO(SNOW-2326973): This can be parallelized further. Its not done here because it only affects
    # write to local storage.

    ls_dataframe = session.sql(f"LS {stage_path}")
    ls_iterator = ls_dataframe.toLocalIterator()

    # Build a normalized base prefix from stage_path to compute relatives
    # Example: stage_path='@MY_STAGE/prefix' -> base_prefix='my_stage/prefix/'
    base_prefix = stage_path.lstrip("@").rstrip("/") + "/"
    base_prefix_lower = base_prefix.lower()

    # Group by parent directory under the base prefix, then issue a GET per directory.
    # This gives a small parallelism advantage if we have many files per partition directory.
    parent_dirs: set[str] = set()
    for row in ls_iterator:
        name: str = row[0]
        name_lower = name.lower()
        rel_start = name_lower.find(base_prefix_lower)
        relative = name[rel_start + len(base_prefix) :] if rel_start != -1 else name
        parent_dir = os.path.dirname(relative)
        if parent_dir and parent_dir != ".":
            parent_dirs.add(parent_dir)

    # If no parent directories were discovered (non-partitioned unload prefix), use direct GET.
    if not parent_dirs:
        snowpark.file_operation.FileOperation(session).get(stage_path, str(real_path))
        return

    file_op = snowpark.file_operation.FileOperation(session)
    for parent_dir in sorted(parent_dirs):
        local_dir = real_path / parent_dir
        if os.path.isfile(local_dir):
            temp_file_name = f"{local_dir}.tmp"
            os.rename(local_dir, temp_file_name)
            os.makedirs(local_dir, exist_ok=True)
            shutil.move(temp_file_name, f"{local_dir}/{local_dir.name}")
        else:
            os.makedirs(local_dir, exist_ok=True)

        src_dir = f"@{base_prefix}{parent_dir}"
        file_op.get(src_dir, str(local_dir))


def _truncate_directory(directory_path: Path) -> None:
    if not directory_path.exists():
        exception = FileNotFoundError(
            f"The specified directory {directory_path} does not exist."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    # Iterate over all the files and directories in the specified directory
    for file in directory_path.iterdir():
        # Check if it is a file or directory and remove it
        if file.is_file() or file.is_symlink():
            file.unlink()
        elif file.is_dir():
            shutil.rmtree(file)
