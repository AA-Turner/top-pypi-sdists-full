#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import copy
import math
import re
import typing
from collections.abc import MutableMapping, MutableSequence
from contextlib import contextmanager
from contextvars import ContextVar
from decimal import Decimal
from functools import reduce
from typing import Tuple

import jpype
import pandas
import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.relations_pb2 as relation_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto
import sqlglot
from google.protobuf.any_pb2 import Any
from pyspark.errors.exceptions.base import (
    AnalysisException,
    NumberFormatException,
    UnsupportedOperationException,
)
from sqlglot.expressions import ColumnDef, DataType, FileFormatProperty, Identifier

import snowflake.snowpark.functions as snowpark_fn
import snowflake.snowpark_connect.proto.snowflake_expression_ext_pb2 as snowflake_exp_proto
import snowflake.snowpark_connect.proto.snowflake_relation_ext_pb2 as snowflake_proto
from snowflake import snowpark
from snowflake.snowpark import Session, types as snowpark_types
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark._internal.type_utils import convert_sp_to_sf_type
from snowflake.snowpark._internal.utils import is_sql_select_statement, quote_name
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.functions import when_matched, when_not_matched
from snowflake.snowpark.types import (
    ArrayType,
    ByteType,
    DateType,
    DayTimeIntervalType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    MapType,
    NullType,
    ShortType,
    StringType,
    StructType,
    TimestampType,
    VariantType,
    YearMonthIntervalType,
    _AtomicType,
    _NumericType,
)
from snowflake.snowpark_connect.config import (
    check_table_supports_operation,
    emulate_partition_overwrite_for_fdn_tables,
    get_boolean_session_config_param,
    get_return_dml_metadata_enabled,
    global_config,
    is_dynamic_partition_overwrite_enabled,
    is_iceberg_sql_extensions_enabled,
    record_table_metadata,
    sessions_config,
    set_config_param,
    should_create_temporary_view_in_snowflake,
    unset_config_param,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.integral_types_support import (
    _overflow_guard_needed,
    apply_integral_overflow_with_ansi_check,
    get_integral_type_bounds,
)
from snowflake.snowpark_connect.expression.map_cast import sanity_check
from snowflake.snowpark_connect.expression.map_expression import (
    ColumnNameMap,
    map_single_column_expression,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.relation.catalogs.utils import (
    CURRENT_CATALOG_NAME,
    _get_current_temp_objects,
)
from snowflake.snowpark_connect.relation.iceberg_sql_branch_tag_suffix import (
    try_parse_iceberg_branch_tag_suffix,
)
from snowflake.snowpark_connect.relation.iceberg_sql_time_travel import (
    resolve_relation_time_travel,
)
from snowflake.snowpark_connect.relation.iceberg_tag_ddl import (
    translate_create_or_replace_tag,
    translate_drop_tag,
)
from snowflake.snowpark_connect.relation.map_relation import (
    NATURAL_JOIN_TYPE_BASE,
    map_relation,
)
from snowflake.snowpark_connect.relation.read.map_read_table import post_process_df

# Import from utils for consistency
from snowflake.snowpark_connect.relation.utils import (
    comparable_col_name,
    is_aggregate_function,
)
from snowflake.snowpark_connect.relation.write.map_write import (
    _build_base_location_clause,
    _coerce_to_unstructured_complex_target,
    _extract_iceberg_format_version,
    _is_unstructured_array,
    _is_unstructured_object,
    _store_assignment_is_legacy,
    _store_assignment_policy,
)
from snowflake.snowpark_connect.snowflake_session import (
    SQL_PASS_THROUGH_MARKER,
    calculate_checksum,
)
from snowflake.snowpark_connect.type_mapping import (
    map_snowpark_to_pyspark_types,
    map_type_to_snowflake_type,
    snowpark_to_proto_type,
)
from snowflake.snowpark_connect.utils.context import (
    _accessing_temp_object,
    gen_sql_plan_id,
    get_is_processing_aliased_relation,
    get_spark_session_id,
    get_sql_plan,
    push_evaluating_sql_scope,
    push_processed_view,
    push_processing_aliased_relation_scope,
    push_sql_scope,
    set_plan_id_map,
    set_sql_args,
    set_sql_plan_name,
)
from snowflake.snowpark_connect.utils.jvm_udf_utils import UdfKind
from snowflake.snowpark_connect.utils.scala_udf_utils import (
    _build_scala_udf_sql_input_params,
)
from snowflake.snowpark_connect.utils.schema_utils import force_nullable_schema
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.spark_session_cache import get_spark_session_cache
from snowflake.snowpark_connect.utils.sql_quoting import escape_sql_comment
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
    telemetry,
)
from snowflake.snowpark_connect.utils.udf_helper import LazySnowparkUdf

from .. import column_name_handler
from ..expression.map_sql_expression import (
    _window_specs,
    as_java_list,
    as_java_map,
    map_logical_plan_expression,
    sql_parser,
)
from ..type_support import emulate_decimal_type, is_integral_types_conversion_enabled
from ..typed_column import TypedColumn
from ..utils.identifiers import (
    is_in_cld_context,
    record_multipart_backtick_flags,
    spark_to_sf_single_id,
    spark_to_sf_single_id_with_unquoting,
    split_fully_qualified_spark_name,
    split_fully_qualified_spark_name_with_quoting,
)
from ..utils.io_utils import (
    PartitionSpec,
    get_overwrite_condition,
    get_partition_spec,
    get_table_type,
)
from ..utils.temporary_view_helper import (
    create_snowflake_temporary_view,
    get_temp_view,
    register_temp_view,
    store_temporary_view_as_dataframe,
    unregister_snowflake_temp_view,
)
from .catalogs import SNOWFLAKE_CATALOG

_ctes = ContextVar[dict[str, relation_proto.Relation]]("_ctes", default={})
_cte_definitions = ContextVar[dict[str, any]]("_cte_definitions", default={})
_having_condition = ContextVar[expressions_proto.Expression | None](
    "_having_condition", default=None
)
_query_block_join_hint: ContextVar[str | None] = ContextVar(
    "_query_block_join_hint", default=None
)


# Captures the table identifier in ``ALTER TABLE [IF EXISTS] <name> ...``.
# The naive ``snowflake_sql.split()[2]`` extraction at the SQL fallback
# call site returned ``"IF"`` for the ``IF EXISTS`` form, which then
# defeated ``_execute_alter``'s managed-Iceberg lookup (``get_table_type``
# returns ``"TABLE"`` for an unknown identifier, so we'd ship a plain
# ``ALTER TABLE`` against an Iceberg target and trip ``091367``).
# Felix on PR #4162.
_ALTER_TABLE_NAME_RE = re.compile(
    r"^\s*ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(\S+)",
    re.IGNORECASE,
)

# Lowercased keys of ``relation.catalogs.CATALOGS``. Hardcoded (rather than
# computed from ``CATALOGS.keys()``) to avoid a top-level import of
# ``relation.catalogs`` from this module; must stay in sync with that dict.
_KNOWN_CATALOG_NAMES = frozenset({"snowflake_catalog", "spark_catalog"})


def _extract_alter_table_name(snowflake_sql: str) -> str:
    """Return the target table FQN from an ``ALTER TABLE ...`` statement.

    Tolerates the optional ``IF EXISTS`` clause and dotted / quoted
    identifiers so ``_execute_alter`` always sees the real table name
    when deciding whether to promote to ``ALTER ICEBERG TABLE``.
    Returns ``""`` when the SQL doesn't match — callers must treat that
    as "skip the catalog probe" rather than blindly looking up ``""``.
    """
    m = _ALTER_TABLE_NAME_RE.match(snowflake_sql)
    return m.group(1) if m else ""


def _execute_alter(session: Session, sql: str, table_name: str) -> None:
    """Execute ALTER TABLE, promoting to ALTER ICEBERG TABLE on Iceberg targets.

    Snowflake rejects ``ALTER TABLE ...`` against Iceberg tables (error
    091367 / 42601: *"is an Iceberg table. Iceberg tables should use
    ALTER ICEBERG TABLE commands"*). Two cases need the promote:

    * **CLD session** — every target is an Iceberg CLD table; promote
      upfront from the session-level hint (``is_in_cld_context()``) and
      skip the catalog round-trip.
    * **Non-CLD session targeting a managed Iceberg table** — probe the
      table type via :func:`get_table_type` and promote when Snowflake
      reports ``ICEBERG``. ``get_table_type`` already suppresses lookup
      failures and returns ``"TABLE"`` for the FDN default, so a missing
      table or transient catalog error degrades to "send plain
      ALTER TABLE" and surfaces the real error from Snowflake instead
      of masking it. SNOW-2118744.
    """
    needs_iceberg_keyword = is_in_cld_context() or (
        bool(table_name) and get_table_type(table_name, session).upper() == "ICEBERG"
    )
    if needs_iceberg_keyword:
        sql = sql.replace("ALTER TABLE ", "ALTER ICEBERG TABLE ", 1)
    session.sql(sql).collect()


@contextmanager
def _push_query_block_hint(hint_name: str | None):
    token = _query_block_join_hint.set(hint_name)
    try:
        yield
    finally:
        _query_block_join_hint.reset(token)


def _map_value_to_literal_proto(
    value: typing.Any, typ: snowpark_types.DataType
) -> expressions_proto.Expression.Literal:
    if isinstance(typ, snowpark_types.NullType):
        return expressions_proto.Expression.Literal(null=value)
    if isinstance(typ, snowpark_types.BinaryType):
        return expressions_proto.Expression.Literal(binary=value)
    if isinstance(typ, snowpark_types.BooleanType):
        return expressions_proto.Expression.Literal(boolean=value)
    if isinstance(typ, snowpark_types.ByteType):
        return expressions_proto.Expression.Literal(byte=value)
    if isinstance(typ, snowpark_types.ShortType):
        return expressions_proto.Expression.Literal(short=value)
    if isinstance(typ, snowpark_types.IntegerType):
        return expressions_proto.Expression.Literal(integer=value)
    if isinstance(typ, snowpark_types.LongType):
        return expressions_proto.Expression.Literal(long=value)
    if isinstance(typ, snowpark_types.FloatType):
        return expressions_proto.Expression.Literal(float=value)
    if isinstance(typ, snowpark_types.DoubleType):
        return expressions_proto.Expression.Literal(double=value)
    if isinstance(typ, snowpark_types.DecimalType):
        return expressions_proto.Expression.Literal(
            decimal=expressions_proto.Expression.Literal.Decimal(
                value=value,
                precision=typ.precision,
                scale=typ.scale,
            )
        )
    if isinstance(typ, snowpark_types.ArrayType):
        element_type_proto = types_proto.DataType(
            **snowpark_to_proto_type(typ.element_type)
        )

        return expressions_proto.Expression.Literal(
            array=expressions_proto.Expression.Literal.Array(
                element_type=element_type_proto,
                elements=[
                    _map_value_to_literal_proto(el, typ.element_type) for el in value
                ],
            )
        )

    if isinstance(typ, snowpark_types.StructType):
        struct_type_proto = types_proto.DataType(**snowpark_to_proto_type(typ))

        return expressions_proto.Expression.Literal(
            struct=expressions_proto.Expression.Literal.Struct(
                struct_type=struct_type_proto,
                elements=[
                    _map_value_to_literal_proto(v, typ.fields[i].datatype)
                    for i, v in enumerate(value.values())
                ],
            )
        )

    return expressions_proto.Expression.Literal(string=str(value))


def _is_sql_select_statement_helper(sql_string: str) -> bool:
    """
    Determine if a SQL string is a SELECT or CTE query statement, even when it starts with comments or whitespace.
    """
    if not sql_string:
        return False

    trimmed = sql_string.lstrip()

    while trimmed:
        if trimmed.startswith("--"):
            newline_pos = trimmed.find("\n")
            if newline_pos == -1:
                return False
            trimmed = trimmed[newline_pos + 1 :].lstrip()
            continue
        elif trimmed.startswith("/*"):
            end_pos = trimmed.find("*/")
            if end_pos == -1:
                return False
            trimmed = trimmed[end_pos + 2 :].lstrip()
            continue
        break

    if not trimmed:
        return False

    return is_sql_select_statement(trimmed)


@contextmanager
def _push_cte_scope():
    """
    Creates a new CTE scope when evaluating nested WITH clauses.
    """
    cur_ctes = _ctes.get()
    cur_definitions = _cte_definitions.get()
    cte_token = _ctes.set(cur_ctes.copy())
    def_token = _cte_definitions.set(cur_definitions.copy())
    try:
        yield
    finally:
        _ctes.reset(cte_token)
        _cte_definitions.reset(def_token)


def _process_cte_relations(cte_relations):
    """
    Process CTE relations and register them in the current CTE scope.

    This function extracts CTE definitions from CTE relations,
    maps them to protobuf representations, and stores them for later reference.

    Args:
        cte_relations: Java list of CTE relations (tuples of name and SubqueryAlias)
    """
    for cte in as_java_list(cte_relations):
        name = str(cte._1())
        # Store the original CTE definition for re-evaluation
        _cte_definitions.get()[name] = cte._2()
        # Process CTE definition with a unique plan_id to ensure proper column naming
        # Clear HAVING condition before processing each CTE to prevent leakage between CTEs
        saved_having = _having_condition.get()
        _having_condition.set(None)
        try:
            cte_plan_id = gen_sql_plan_id()
            # Isolate plan names from CTE definition processing so they don't
            # leak into the parent scope.  Without this, set_sql_plan_name
            # inside the SubqueryAlias case registers the CTE name with the
            # *definition* plan_id.  Later, ORDER BY / WHERE / GROUP BY
            # expressions that use qualified references (e.g. t.a) would
            # resolve to this stale definition plan_id instead of falling
            # through to qualifier-based column matching, causing
            # RESOLVED_REFERENCE_COLUMN_NOT_FOUND errors (SNOW-2206240).
            with push_sql_scope():
                cte_proto = map_logical_plan_relation(cte._2(), cte_plan_id)
            _ctes.get()[name] = cte_proto
        finally:
            _having_condition.set(saved_having)


@contextmanager
def _with_cte_scope(cte_relations):
    """
    Context manager that creates a CTE scope and processes CTE relations.

    This combines _push_cte_scope() and _process_cte_relations() to handle
    the common pattern of processing CTEs within a new scope.

    Args:
        cte_relations: Java list of CTE relations (tuples of name and SubqueryAlias)
    """
    with _push_cte_scope():
        _process_cte_relations(cte_relations)
        yield


@contextmanager
def _push_window_specs_scope():
    """
    Creates a new window specs  scope when evaluating nested  clauses.
    """
    cur = _window_specs.get()
    token = _window_specs.set(cur.copy())
    try:
        yield
    finally:
        _window_specs.reset(token)


def _find_pos_args(node, positions: list[int]):
    if str(node.nodeName()) == "PosParameter":
        positions.append(node.pos())
    else:
        for child in as_java_list(node.children()):
            _find_pos_args(child, positions)
        if hasattr(node, "expressions"):
            for child in as_java_list(node.expressions()):
                _find_pos_args(child, positions)


def parse_pos_args(
    logical_plan,
    pos_args: MutableSequence[expressions_proto.Expression.Literal],
) -> dict[int, expressions_proto.Expression]:
    # Spark Connect gives us positional parameters as a regular list,
    # while Spark parser refers to them by their character indexes in the query.
    # Therefore, we need to find all positional parameters, sort their locations,
    # and match them to the list from Spark Connect.
    if not pos_args:
        return {}

    positions: list[int] = []
    _find_pos_args(logical_plan, positions)
    return dict(zip(sorted(positions), pos_args))


def execute_logical_plan(logical_plan) -> DataFrameContainer:
    proto = map_logical_plan_relation(logical_plan)
    telemetry.report_parsed_sql_plan(proto)
    with push_evaluating_sql_scope():
        return map_relation(proto)


def _spark_to_snowflake(multipart_id: jpype.JObject) -> str:
    """Transform a Spark multipart identifier to its Snowflake form.

    Design (PR #4052 follow-up — single-session/single-catalog model):

    SCOS exposes a single Spark session pinned to a single Snowflake
    database at attach time, and we do not silently switch databases
    mid-session. That database is either a Catalog-Linked Database (CLD)
    or a regular Snowflake database, and its CLD-ness is the **only**
    ground truth we need: every identifier in a request, regardless of
    how many parts it has, follows the same set of identifier rules
    determined by `_current_cld_context` (set once on session attach in
    `utils/session.py`, reset at every RPC entry).

    Why not classify by inspecting `parts[0]` for 3-part names?

    * Spark/Iceberg overloads 3-part identifiers — `db.tbl.metadata_table`
      (e.g. `mydb.mytbl.data_files`, `.history`, `.snapshots`) is the
      Iceberg metadata-table form, and `parts[0]` is the *schema*, not
      the catalog. Treating `parts[0]` as a database name and probing
      its CLD-ness via `SHOW DATABASES LIKE 'mydb'` would silently use
      non-CLD rules for what is actually a CLD-resident metadata query
      (the database doesn't exist; the lookup fails to is_cld=False).
    * SCOS doesn't support multi-catalog references in a single session
      anyway, so there is no meaningful "this multipart targets a
      different catalog from the session" classification to make.

    Per-part backtick handling: we look up the unquoted parts tuple in
    the request-level `_multipart_backtick_flags` map (populated during
    the AST walk in `case "UnresolvedRelation":` from the JVM Origin
    substring). The map is keyed by the full parts tuple — never by
    leaf name — so a backtick-quoted column `foo` cannot affect an
    unquoted table `foo` elsewhere in the request (Felix's PR #4052
    review on cld_context.py:113). If there is no entry for these
    parts, every part defaults to "not backtick-quoted".
    """
    from ..utils.identifiers import get_multipart_backtick_flags

    parts = [str(part) for part in as_java_list(multipart_id)]
    flags = get_multipart_backtick_flags(tuple(parts))
    if flags is None or len(flags) != len(parts):
        flags = (False,) * len(parts)
    return ".".join(
        spark_to_sf_single_id(part, is_backtick_quoted=flag)
        for part, flag in zip(parts, flags)
    )


def _get_original_identifier_from_origin(rel) -> str | None:
    """
    Extract the original identifier text from a parsed relation's Origin.

    The Origin object contains the original SQL text and character positions,
    allowing us to recover the exact identifier as written (including backticks).

    Args:
        rel: A parsed logical plan node (e.g., UnresolvedRelation)

    Returns:
        The original identifier string if available, None otherwise.
        For backtick-quoted identifiers, this includes the backticks.
    """
    try:
        origin = rel.origin()
        start_idx = origin.startIndex()
        stop_idx = origin.stopIndex()
        sql_text = origin.sqlText()

        if start_idx.isDefined() and stop_idx.isDefined() and sql_text.isDefined():
            start = start_idx.get()
            stop = stop_idx.get()
            original_sql = sql_text.get()
            return original_sql[start : stop + 1]
    except Exception as e:
        logger.debug(f"Could not extract origin identifier: {e}")
    return None


def _rename_columns(
    df: snowpark.DataFrame, user_specified_columns, column_map: ColumnNameMap
) -> snowpark.DataFrame:
    user_columns = [str(col._1()) for col in as_java_list(user_specified_columns)]

    if user_columns:
        columns = list(zip(df.columns, user_columns))
    else:
        columns = list(column_map.snowpark_to_spark_map().items())

    if columns:
        return df.select(
            [
                snowpark_fn.col(orig).alias(
                    spark_to_sf_single_id(user_col, is_column=True)
                )
                for orig, user_col in columns
            ]
        )
    return df


def _apply_decimal_schema_emulation(df: snowpark.DataFrame) -> snowpark.DataFrame:
    """Apply casts to emulate decimal types in the DataFrame schema for CTAS/CVAS operations."""
    if not is_integral_types_conversion_enabled():
        return df

    if not any(
        isinstance(field.datatype, snowpark_types._IntegralType)
        for field in df.schema.fields
    ):
        return df

    projections = []
    for field in df.schema.fields:
        # only cast integral types, there is no need to cast complex types like structs, arrays, maps, etc.
        # as they should be already properly typed
        if isinstance(field.datatype, snowpark_types._IntegralType):
            target_type = emulate_decimal_type(field.datatype)
            projections.append(
                snowpark_fn.col(field.name).cast(target_type).alias(field.name)
            )
        else:
            projections.append(snowpark_fn.col(field.name))

    return df.select(projections)


def _create_table_as_select(logical_plan, mode: str) -> None:
    # TODO: for as select create tables we'd map multi layer identifier here
    name = get_relation_identifier_name(logical_plan.name())
    full_table_identifier = get_relation_identifier_name(
        logical_plan.name(), is_multi_part=True
    )
    comment = logical_plan.tableSpec().comment()
    data_source = _extract_table_provider(logical_plan)

    container = execute_logical_plan(logical_plan.query())
    df = container.dataframe
    df = _apply_decimal_schema_emulation(df)
    columns = container.column_map.snowpark_to_spark_map().items()
    if columns:
        df = df.select(
            [
                snowpark_fn.col(orig_column).alias(
                    spark_to_sf_single_id(user_column, is_column=True)
                )
                for orig_column, user_column in columns
            ]
        )

    # Spark doesn't preserve nullability in CTAS so the resulting table has
    # all columns nullable.
    force_nullable_schema(df)

    write_kwargs = {
        "comment": None if comment.isEmpty() else comment.get(),
        "mode": mode,
    }
    if data_source == "iceberg":
        write_kwargs["iceberg_config"] = _build_managed_iceberg_config_for_sql(
            logical_plan
        )
    df.write.save_as_table(name, **write_kwargs)

    # Record table metadata for CREATE TABLE AS SELECT
    # These are typically considered v2 tables and support RENAME COLUMN
    record_table_metadata(
        table_identifier=full_table_identifier,
        table_type="v2",
        data_source=data_source,
        supports_column_rename=True,
    )


def _spark_dml_metadata_dataframe(
    shape: str, inserted: int, updated: int, deleted: int
) -> pandas.DataFrame:
    affected = inserted + updated + deleted
    if shape == "insert":
        return pandas.DataFrame(
            [{"num_affected_rows": affected, "num_inserted_rows": inserted}]
        )
    if shape == "delete":
        return pandas.DataFrame([{"num_affected_rows": deleted}])
    if shape == "update":
        return pandas.DataFrame([{"num_affected_rows": updated}])
    if shape == "merge":
        return pandas.DataFrame(
            [
                {
                    "num_affected_rows": affected,
                    "num_updated_rows": updated,
                    "num_deleted_rows": deleted,
                    "num_inserted_rows": inserted,
                }
            ]
        )
    return pandas.DataFrame()


def _cast_partition_value_to_desired_type(
    value: str | None, target_type: snowpark_types.DataType
) -> None:
    """Validate a SQL partition literal against its target column type.

    SNOW-2677699: port of Spark's PartitioningUtils.castPartValueToDesiredType
    so malformed partition literals are rejected at analysis time rather than
    at Snowflake runtime. Byte/Short are range-checked inline since
    sanity_check keeps Snowflake's broader runtime behavior for those types.
    """
    if value is None:
        return
    if isinstance(target_type, (ByteType, ShortType)):
        lower, upper = get_integral_type_bounds(target_type)
        try:
            parsed = int(value)
            if not lower <= parsed <= upper:
                raise ValueError(value)
        except ValueError as e:
            exception = NumberFormatException(
                f"Cannot cast partition value '{value}' to "
                f"{target_type.simple_string()}"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception from e
        return
    sanity_check(target_type, value, StringType(), from_type_cast=True)


def _resolvable_nullability(from_nullable: bool, to_nullable: bool) -> bool:
    # Port of Spark Cast.resolvableNullability: a nullable source requires a
    # nullable target (we can't safely erase nulls).
    return (not from_nullable) or to_nullable


# Port of Spark 3.5.3 UpCastRule.scala:27-33.
_NUMERIC_PRECEDENCE_INDEX: dict[type, int] = {
    cls: i
    for i, cls in enumerate(
        (ByteType, ShortType, IntegerType, LongType, FloatType, DoubleType)
    )
}

# Port of Spark DecimalType.forType for IntegralType.
_INTEGRAL_TO_DECIMAL_FORM: dict[type, DecimalType] = {
    ByteType: DecimalType(3, 0),
    ShortType: DecimalType(5, 0),
    IntegerType: DecimalType(10, 0),
    LongType: DecimalType(20, 0),
}


def _legal_numeric_precedence(
    src: snowpark_types.DataType, tgt: snowpark_types.DataType
) -> bool:
    """Port of Spark 3.5.3 UpCastRule.legalNumericPrecedence.

    True iff src is strictly narrower than tgt in the numeric widening chain
    [Byte, Short, Int, Long, Float, Double]. Non-chain types (Decimal,
    String, etc.) return False.
    """
    src_idx = _NUMERIC_PRECEDENCE_INDEX.get(type(src), -1)
    tgt_idx = _NUMERIC_PRECEDENCE_INDEX.get(type(tgt), -1)
    return src_idx >= 0 and src_idx < tgt_idx


def _decimal_is_wider_than(dec: DecimalType, other: snowpark_types.DataType) -> bool:
    """Port of Spark 3.5.3 DecimalType.isWiderThan (DecimalType.scala:69-78).

    True iff `other` can be cast into `dec` without precision or range loss.
    Float/Double are not IntegralType → returns False; widening from
    Float/Double is handled by _legal_numeric_precedence instead.
    """
    if isinstance(other, DecimalType):
        return (dec.precision - dec.scale) >= (
            other.precision - other.scale
        ) and dec.scale >= other.scale
    dec_form = _INTEGRAL_TO_DECIMAL_FORM.get(type(other))
    if dec_form is not None:
        return _decimal_is_wider_than(dec, dec_form)
    return False


def _decimal_is_tighter_than(dec: DecimalType, other: snowpark_types.DataType) -> bool:
    """Port of Spark 3.5.3 DecimalType.isTighterThan (DecimalType.scala:84-94).

    For IntegralType `other`, requires strict precision < integer-decimal
    precision AND scale == 0 (Spark's extra integer-overflow guard).
    """
    if isinstance(other, DecimalType):
        return (dec.precision - dec.scale) <= (
            other.precision - other.scale
        ) and dec.scale <= other.scale
    int_dec = _INTEGRAL_TO_DECIMAL_FORM.get(type(other))
    if int_dec is not None:
        return dec.precision < int_dec.precision and dec.scale == 0
    return False


def _has_snowflake_passthrough(tgt: snowpark_types.DataType) -> bool:
    """Short-circuit for Snowflake-only targets with no Spark equivalent.

    Unstructured complex types carry no element metadata (element_type=None /
    empty fields) so we can't recurse into them — defer to Snowflake's cast.
    Only the target side needs checking: Spark DataFrame schemas are always
    fully typed, so unstructured types only appear when reading a
    Snowflake-native column.
    """
    return (
        isinstance(tgt, VariantType)
        or _is_unstructured_array(tgt)
        or _is_unstructured_object(tgt)
    )


def _can_up_cast(src: snowpark_types.DataType, tgt: snowpark_types.DataType) -> bool:
    """Port of Spark 3.5.3 UpCastRule.canUpCast (UpCastRule.scala:40-77).

    STRICT store-assignment rules: True iff src can upcast to tgt without
    truncation, precision loss, or possible runtime failure.

    Deliberately omitted vs. upstream: TimestampNTZType arms (Snowpark has no
    NTZ split), (CalendarIntervalType, StringType) (Snowpark has no
    CalendarInterval — not covered by (_AtomicType, StringType) because
    CalendarIntervalType is not an AtomicType in Spark), and
    UserDefinedType.acceptsType (no Snowpark UDT equivalent).
    """
    if _has_snowflake_passthrough(tgt):
        return True

    match (src, tgt):
        case _ if src == tgt:
            return True
        case (_NumericType(), DecimalType()) if _decimal_is_wider_than(tgt, src):
            return True
        case (DecimalType(), _NumericType()) if _decimal_is_tighter_than(src, tgt):
            return True
        case _ if _legal_numeric_precedence(src, tgt):
            return True
        case (DateType(), TimestampType()):
            return True
        case (_AtomicType(), StringType()):
            return True
        case (NullType(), _):
            return True
        case (TimestampType(), LongType()) | (LongType(), TimestampType()):
            return True
        case (ArrayType(), ArrayType()):
            return _resolvable_nullability(
                src.contains_null, tgt.contains_null
            ) and _can_up_cast(src.element_type, tgt.element_type)
        case (MapType(), MapType()):
            return (
                _resolvable_nullability(
                    src.value_contains_null, tgt.value_contains_null
                )
                and _can_up_cast(src.key_type, tgt.key_type)
                and _can_up_cast(src.value_type, tgt.value_type)
            )
        case (StructType(), StructType()) if len(src.fields) == len(tgt.fields):
            return all(
                _resolvable_nullability(sf.nullable, tf.nullable)
                and _can_up_cast(sf.datatype, tf.datatype)
                for sf, tf in zip(src.fields, tgt.fields)
            )
        case (DayTimeIntervalType(), DayTimeIntervalType()):
            return True
        case (YearMonthIntervalType(), YearMonthIntervalType()):
            return True
        case _:
            return False


def _validate_store_assignment_field(
    src: snowpark_types.DataType,
    tgt: snowpark_types.DataType,
    policy: str | None,
) -> bool:
    """Policy dispatcher. LEGACY accepts all; STRICT/ANSI/unknown delegate
    to the matching Spark rule. `policy=None` is treated as LEGACY.

    Arguments use Spark's (from, to) convention — target-first callers must swap.
    """
    effective_policy = (policy or "LEGACY").upper()
    if effective_policy == "LEGACY":
        return True
    if effective_policy == "STRICT":
        return _can_up_cast(src, tgt)
    return _can_ansi_store_assign(src, tgt)


def _can_ansi_store_assign(
    src: snowpark_types.DataType, tgt: snowpark_types.DataType
) -> bool:
    """SNOW-2677699: port of Spark 3.5.3 Cast.canANSIStoreAssign.

    SAS accepts Snowflake-only VARIANT / unstructured ARRAY / OBJECT on either
    side (no Spark equivalent).
    """
    if _has_snowflake_passthrough(tgt):
        return True

    match (src, tgt):
        case _ if src == tgt:
            return True
        case (NullType(), _):
            return True
        case (_NumericType(), _NumericType()):
            return True
        case (_AtomicType(), StringType()):
            return True
        case (DateType() | TimestampType(), DateType() | TimestampType()):
            return True
        case (ArrayType(), ArrayType()):
            return _resolvable_nullability(
                src.contains_null, tgt.contains_null
            ) and _can_ansi_store_assign(src.element_type, tgt.element_type)
        case (MapType(), MapType()):
            return (
                _resolvable_nullability(
                    src.value_contains_null, tgt.value_contains_null
                )
                and _can_ansi_store_assign(src.key_type, tgt.key_type)
                and _can_ansi_store_assign(src.value_type, tgt.value_type)
            )
        case (StructType(), StructType()) if len(src.fields) == len(tgt.fields):
            return all(
                _resolvable_nullability(src_field.nullable, tgt_field.nullable)
                and _can_ansi_store_assign(src_field.datatype, tgt_field.datatype)
                for src_field, tgt_field in zip(src.fields, tgt.fields)
            )
        case _:
            return False


def _validate_insert_schema_by_position(
    effective_target_schema: StructType,
    data_schema: StructType,
    snowpark_table_name: str,
) -> None:
    """SNOW-2677699: policy-aware SQL INSERT schema validation.

    Mirrors Spark's TableOutputResolver.canWrite dispatch:
      LEGACY → skip compatibility check.
      ANSI   → _can_ansi_store_assign.
      STRICT → _can_up_cast.
    """
    if len(data_schema.fields) != len(effective_target_schema.fields):
        exception = AnalysisException(
            f"The column number of the existing table {snowpark_table_name} "
            f"({effective_target_schema.simple_string()}) doesn't match the "
            f"data schema ({data_schema.simple_string()})."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception
    policy = _store_assignment_policy()
    for src, tgt in zip(data_schema.fields, effective_target_schema.fields):
        if not _validate_store_assignment_field(src.datatype, tgt.datatype, policy):
            exception = AnalysisException(
                f"[INCOMPATIBLE_DATA_FOR_TABLE.CANNOT_SAFELY_CAST] "
                f"Cannot write incompatible data for the table {snowpark_table_name}: "
                f"Cannot safely cast `{tgt.name}` "
                f'"{src.datatype.simple_string().upper()}" '
                f'to "{tgt.datatype.simple_string().upper()}".'
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception


def _insert_into_table(logical_plan, session: Session) -> int | None:
    def _inserted_row_count_from_collect(raw_rows: list) -> int:
        if not raw_rows:
            return 0
        row = raw_rows[0]
        d = row.asDict(recursive=True) if hasattr(row, "asDict") else {}
        total = 0
        for k, v in d.items():
            lk = str(k).lower()
            if "inserted" in lk:
                total += int(v) if v is not None else 0
        return total

    df_container = execute_logical_plan(logical_plan.query())
    df = df_container.dataframe
    queries = df.queries["queries"]
    if len(queries) != 1:
        exception = SnowparkConnectNotImplementedError(
            f"Unexpected number of queries: {len(queries)}"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    name = get_relation_identifier_name(logical_plan.table(), True)

    user_columns = [
        spark_to_sf_single_id(str(col), is_column=True)
        for col in as_java_list(logical_plan.userSpecifiedCols())
    ]
    cols_str = "(" + ", ".join(user_columns) + ")" if user_columns else ""

    # Extract partition spec if any
    partition_spec = logical_plan.partitionSpec()
    partition_map = as_java_map(partition_spec)

    partition_columns = {}
    for entry in partition_map.entrySet():
        col_name = str(entry.getKey())
        value_option = entry.getValue()
        if value_option.isDefined():
            partition_columns[col_name] = value_option.get()

    target_table = session.table(name)
    target_schema = target_table.schema
    is_iceberg_table = get_table_type(name, session) == "ICEBERG"
    table_partition_spec = None
    if is_iceberg_table and logical_plan.overwrite():
        # we need the table's partition spec to validate and perform the overwrite operation
        table_partition_spec = get_partition_spec(name, session)

    if partition_columns and logical_plan.overwrite() and is_iceberg_table:
        # confirm that partition_columns are in the table's partition spec
        if table_partition_spec is not None:
            _confirm_partition_columns_are_in_spec(
                list(partition_columns.keys()), table_partition_spec
            )

    # Add partition columns to the dataframe
    partition_col_positions = {}
    if partition_columns:
        """
        Spark sends them in the partition spec and the values won't be present in the values array.
        As snowflake does not support static partitions in INSERT INTO statements,
        we need to add the partition columns to the dataframe as literal columns.

        ex: INSERT INTO TABLE test_table PARTITION (ds='2021-01-01', hr=10) VALUES ('k1', 100), ('k2', 200), ('k3', 300)

        Spark sends: VALUES ('k1', 100), ('k2', 200), ('k3', 300) with partition spec (ds='2021-01-01', hr=10)
        Snowflake expects: VALUES ('k1', 100, '2021-01-01', 10), ('k2', 200, '2021-01-01', 10), ('k3', 300, '2021-01-01', 10)

        We need to add the partition columns to the dataframe as literal columns.

        ex: df = df.withColumn('ds', snowpark_fn.lit('2021-01-01'))
            df = df.withColumn('hr', snowpark_fn.lit(10))

        Then the final query will be:
        INSERT INTO TABLE test_table VALUES ('k1', 100, '2021-01-01', 10), ('k2', 200, '2021-01-01', 10), ('k3', 300, '2021-01-01', 10)

        Spark uses positional matching for columns, so partition values must be put in the correct position.
        """

        target_column_positions = {
            comparable_col_name(col.name): i
            for i, col in enumerate(target_schema.fields)
        }

        for partition_col, partition_value in partition_columns.items():
            match_key = comparable_col_name(partition_col)
            if match_key not in target_column_positions:
                exception = AnalysisException(
                    f"{partition_col} is not a valid partition column in table {name}."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception

            pos = target_column_positions[match_key]
            new_snowpark_name = spark_to_sf_single_id(partition_col)
            target_field = target_schema.fields[pos]
            # SNOW-2677699: partition values arrive as raw strings from the
            # Spark parser; cast to the target column type so df.schema
            # reflects stored types and bad literals are rejected at analysis
            # time (matching Spark).
            _cast_partition_value_to_desired_type(
                partition_value, target_field.datatype
            )
            partition_col_positions[pos] = (
                snowpark_fn.lit(partition_value)
                .cast(target_field.datatype)
                .alias(new_snowpark_name),
                partition_col,
                new_snowpark_name,
            )

        # the merged projection containing source columns and static partition columns inserted in the correct position
        columns_for_insert = []
        spark_names = []
        snowpark_names = []
        source_columns = [c for c in df_container.column_map.columns if c.is_visible]
        source_columns.reverse()
        total_cols = len(source_columns) + len(partition_columns)
        for position in range(total_cols):
            if position in partition_col_positions:
                pcol, spark_name, new_snowpark_name = partition_col_positions[position]
                columns_for_insert.append(pcol)
                spark_names.append(spark_name)
                snowpark_names.append(new_snowpark_name)
            elif source_columns:
                scol = source_columns.pop()
                new_snowpark_name = spark_to_sf_single_id(scol.spark_name)
                columns_for_insert.append(
                    snowpark_fn.col(scol.snowpark_name).alias(new_snowpark_name)
                )
                spark_names.append(scol.spark_name)
                snowpark_names.append(new_snowpark_name)

        # apply projection with partition values
        df = df.select(*columns_for_insert)

        # update container so that we have a proper column map
        df_container = DataFrameContainer.create_with_column_mapping(
            dataframe=df,
            spark_column_names=spark_names,
            snowpark_column_names=snowpark_names,
        )

    # at this point the input dataframe should have all columns in the correct order
    expected_number_of_columns = (
        len(user_columns) if user_columns else len(target_schema.fields)
    )
    if expected_number_of_columns != len(df.schema.fields):
        reason = (
            "too many data columns"
            if len(df.schema.fields) > expected_number_of_columns
            else "not enough data columns"
        )
        exception = AnalysisException(
            f'[INSERT_COLUMN_ARITY_MISMATCH.{reason.replace(" ", "_").upper()}] Cannot write to {name}, the reason is {reason}:\n'
            f'Table columns: {", ".join(target_schema.names)}.\n'
            f'Data columns: {", ".join(df.schema.names)}.'
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    # Build the effective target schema for positional validation. If the user
    # specified a column list, reorder target fields to match; otherwise use the
    # table schema as-is.
    if user_columns:
        normalized_user = [comparable_col_name(c) for c in user_columns]
        # SNOW-2677699: reject INSERT INTO t (a, a) VALUES (...) — without
        # this guard, positional validation silently maps both values to the
        # same target slot.
        if len(set(normalized_user)) != len(normalized_user):
            exception = AnalysisException(
                f"Duplicate column references in INSERT column list for table "
                f"{name}: {', '.join(user_columns)}."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception

        target_by_name = {comparable_col_name(f.name): f for f in target_schema.fields}
        effective_target_fields = []
        for user_col, match_key in zip(user_columns, normalized_user):
            if match_key not in target_by_name:
                exception = AnalysisException(
                    f"Cannot resolve column `{user_col}` in table {name}. "
                    f"Table columns: {', '.join(target_schema.names)}."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception
            effective_target_fields.append(target_by_name[match_key])
        effective_target_schema = StructType(effective_target_fields)
    else:
        effective_target_schema = target_schema

    _validate_insert_schema_by_position(effective_target_schema, df.schema, name)

    try:
        # Modify df with type conversions and struct field name mapping
        is_not_legacy = not _store_assignment_is_legacy()
        modified_columns = []
        for source_field, target_field in zip(
            df.schema.fields, effective_target_schema.fields
        ):
            col_name = source_field.name

            # Handle different type conversions
            if isinstance(
                target_field.datatype, snowpark.types.DecimalType
            ) and isinstance(
                source_field.datatype,
                (snowpark.types.FloatType, snowpark.types.DoubleType),
            ):
                # Add CASE WHEN to convert NaN to NULL for DECIMAL targets
                # Only apply this to floating-point source columns
                col_expr = (
                    snowpark_fn.when(
                        snowpark_fn.equal_nan(snowpark_fn.col(col_name)),
                        snowpark_fn.lit(None),
                    )
                    .otherwise(snowpark_fn.col(col_name))
                    .alias(col_name)
                )
            else:
                unstructured_coerced = _coerce_to_unstructured_complex_target(
                    snowpark_fn.col(col_name),
                    source_field.datatype,
                    target_field.datatype,
                )
                if unstructured_coerced is not None:
                    # Unstructured complex target (VARIANT / ARRAY / OBJECT):
                    # bridge via VARIANT so Snowflake stores the value with the
                    # right type. Must be checked before the StructType branch
                    # below, because an unstructured OBJECT is represented as
                    # StructType([]) in Snowpark.
                    col_expr = unstructured_coerced.alias(col_name)
                elif (
                    isinstance(target_field.datatype, snowpark.types.StructType)
                    and source_field.datatype != target_field.datatype
                ):
                    # Cast struct with field name mapping (e.g., col1,col2 -> i1,i2)
                    # This fixes INSERT INTO table with struct literals like (2, 3)
                    col_expr = (
                        snowpark_fn.col(col_name)
                        .cast(target_field.datatype, rename_fields=True)
                        .alias(col_name)
                    )
                else:
                    col_expr = snowpark_fn.col(col_name)

            # Overflow wrap must live inside this loop because the enclosing
            # try/except Exception: pass would swallow errors from any
            # post-loop .select().
            if is_not_legacy and _overflow_guard_needed(
                source_field.datatype, target_field.datatype
            ):
                col_expr = apply_integral_overflow_with_ansi_check(
                    col_expr, target_field.datatype, ansi_enabled=True
                ).alias(col_name)

            modified_columns.append(col_expr)

        df = df.select(modified_columns)
    except Exception:
        pass

    if not logical_plan.overwrite():
        queries = df.queries["queries"]
        final_query = queries[0]
        collected = session.sql(
            f"INSERT INTO {name} {cols_str} {final_query}",
        ).collect()
        return (
            _inserted_row_count_from_collect(collected)
            if get_return_dml_metadata_enabled()
            else None
        )

    # for FDN, we can optionally support partition overwrites if any partition_columns are given
    is_allowed_fdn_overwrite = (
        partition_columns and emulate_partition_overwrite_for_fdn_tables()
    ) or (not partition_columns and not is_dynamic_partition_overwrite_enabled())

    if not is_iceberg_table and not is_allowed_fdn_overwrite:
        exception = SnowparkConnectNotImplementedError(
            f"Cannot perform partition overwrite on Snowflake table {name}. Set 'snowpark.connect.sql.emulatePartitionOverwritesForSnowflakeTables' to True to enable partial support."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    is_dynamic_overwrite = (
        # an iceberg table with a known partition spec
        (
            is_iceberg_table
            and is_dynamic_partition_overwrite_enabled()
            and table_partition_spec
            and table_partition_spec.columns()
        )
        # or user-defined partition columns
        or partition_columns
    )

    # both dynamic and static overwrites can be handled the same,
    # by this point the input has been augmented
    if is_dynamic_overwrite:
        input_column_names = df_container.column_map.get_snowpark_columns()
        input_partition_cols = []
        target_partition_columns = []
        if is_iceberg_table:
            # confirm that we have the partition spec, and that it doesn't contain non-identity transforms
            if table_partition_spec is None:
                # we can't proceed without a partition spec
                exception = AnalysisException(
                    f"Could not find partition spec for table {name}."
                )
                attach_custom_error_code(
                    exception, ErrorCodes.ICEBERG_PARTITION_SPEC_NOT_FOUND
                )
                raise exception

            if table_partition_spec.uses_transform():
                # TODO (SNOW-3046385): add support for transforms
                raise SnowparkConnectNotImplementedError(
                    "Non-identity transforms are not supported for partition overwrites"
                )

            # for dynamic overwrites, we need to extract all distinct partition values from the input data
            # Spark uses positional matching, we don't care about names here
            # the partition spec is the source of truth about partition columns, so we use all the columns
            # that are defined there
            input_partition_cols = [
                input_column_names[pos]
                for pos in table_partition_spec.partition_column_positions()
            ]
            target_partition_columns = table_partition_spec.columns()
        elif partition_col_positions:
            # for FDN tables, we have to use partition_col_positions, since we don't have a partition spec
            # this means that we only use the columns that the user includes in the PARTITION clause,
            input_partition_cols = [
                c
                for pos, c in enumerate(input_column_names)
                if pos in partition_col_positions
            ]
            target_partition_columns = [
                c
                for pos, c in enumerate(target_table.columns)
                if pos in partition_col_positions
            ]

        distinct_partitions_df = df.select(*input_partition_cols).distinct()

        overwrite_condition = get_overwrite_condition(
            distinct_partitions_df, target_partition_columns
        )
        df.write.saveAsTable(
            table_name=name,
            table_exists=True,
            mode="overwrite",
            overwrite_condition=overwrite_condition,
        )
        if get_return_dml_metadata_enabled():
            return session.table(name).count()
        return None

    # full overwrite
    queries = df.queries["queries"]
    final_query = queries[0]
    collected = session.sql(
        f"INSERT OVERWRITE INTO {name} {cols_str} {final_query}",
    ).collect()
    return (
        _inserted_row_count_from_collect(collected)
        if get_return_dml_metadata_enabled()
        else None
    )


def _confirm_partition_columns_are_in_spec(
    partition_columns: list[str], partition_spec: PartitionSpec
) -> None:
    """
    Checks if all given partition_columns are present in the partition_spec.
    If any column is not present, the function raises an exception.
    Column ordering is not relevant.
    """
    # normalize partition field names to account for case sensitivity
    allowed_partition_columns = {
        spark_to_sf_single_id(c) for c in partition_spec.columns()
    }
    for pc in partition_columns:
        if spark_to_sf_single_id(pc) not in allowed_partition_columns:
            exception = AnalysisException(
                f"[NON_PARTITION_COLUMN] PARTITION clause cannot contain the non-partition column: `{pc}`."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception


def _spark_field_to_sql(field: jpype.JObject, is_column: bool) -> str:
    # Column names will be uppercased according to "spark.sql.caseSensitive".
    # Struct fields will be left as is. This should allow users to use the same names
    # in spark and Snowflake in most cases.
    if is_column:
        name = spark_to_sf_single_id(str(field.name()), is_column=True)
    else:
        name = quote_name_without_upper_casing(str(field.name()))
    data_type_str = _spark_datatype_to_sql(field.dataType())
    # TODO: Support comments
    return f"{name} {data_type_str}"


_SPARK_INTEGRAL_SIMPLE_STRING_TO_SNOWPARK_TYPE_MAP = {
    "tinyint": ByteType(),
    "smallint": ShortType(),
    "int": IntegerType(),
    "bigint": LongType(),
}


def _spark_datatype_to_sql(data_type: jpype.JObject) -> str:
    match data_type.typeName():
        case "array":
            element_type_str = _spark_datatype_to_sql(data_type.elementType())
            return f"ARRAY({element_type_str})"
        case "map":
            key_type_str = _spark_datatype_to_sql(data_type.keyType())
            value_type_str = _spark_datatype_to_sql(data_type.valueType())
            return f"MAP({key_type_str}, {value_type_str})"
        case "struct":
            field_types_str = ", ".join(
                _spark_field_to_sql(f, False) for f in data_type.fields()
            )
            return f"OBJECT({field_types_str})"
        case _:
            snowpark_integral_data_type = (
                _SPARK_INTEGRAL_SIMPLE_STRING_TO_SNOWPARK_TYPE_MAP.get(
                    data_type.simpleString().lower()
                )
            )
            if snowpark_integral_data_type:
                return emulate_decimal_type(snowpark_integral_data_type).simple_string()

            return data_type.sql()


def _get_field_by_name(
    struct_type: StructType, name: str
) -> snowpark_types.StructField | None:
    target_key = comparable_col_name(name)
    return next(
        (
            field
            for field in struct_type.fields
            if comparable_col_name(field.name) == target_key
        ),
        None,
    )


def _field_not_found_exception(
    path_parts: list[str], field_path: list[str]
) -> Exception:
    exception = AnalysisException(
        f"[FIELD_NOT_FOUND] Cannot add nested field `{'.'.join(path_parts)}` "
        f"because `{'.'.join(field_path)}` is not a structured column."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
    return exception


def _add_nested_field_to_structured_sql(
    struct_type: StructType,
    remaining_path_parts: list[str],
    spark_data_type: jpype.JObject,
    full_path_parts: list[str],
) -> str:
    field_name = remaining_path_parts[0]
    existing_field = _get_field_by_name(struct_type, field_name)

    if len(remaining_path_parts) == 1:
        if existing_field is not None:
            exception = AnalysisException(
                f"[COLUMN_ALREADY_EXISTS] The nested field `{'.'.join(full_path_parts)}` already exists."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception

        existing_fields_sql = [
            f"{field.case_sensitive_name} "
            f"{map_type_to_snowflake_type(field.datatype, structured=True)}"
            for field in struct_type.fields
        ]
        new_field_sql = (
            f"{quote_name_without_upper_casing(field_name)} "
            f"{_spark_datatype_to_sql(spark_data_type)}"
        )
        return f"OBJECT({', '.join(existing_fields_sql + [new_field_sql])})"

    if existing_field is None or not isinstance(existing_field.datatype, StructType):
        field_path = full_path_parts[
            : len(full_path_parts) - len(remaining_path_parts) + 1
        ]
        raise _field_not_found_exception(full_path_parts, field_path)

    fields_sql = []
    for field in struct_type.fields:
        field_name_sql = field.case_sensitive_name
        if comparable_col_name(field.name) == comparable_col_name(field_name):
            field_type_sql = _add_nested_field_to_structured_sql(
                existing_field.datatype,
                remaining_path_parts[1:],
                spark_data_type,
                full_path_parts,
            )
        else:
            field_type_sql = map_type_to_snowflake_type(field.datatype, structured=True)
        fields_sql.append(f"{field_name_sql} {field_type_sql}")
    return f"OBJECT({', '.join(fields_sql)})"


def _nested_struct_add_unsupported_on_cld(
    table_name: str,
    col_name_parts: list[str],
) -> SnowparkConnectNotImplementedError:
    """Build the shared SNOW-3471827 actionable error for
    ``ALTER TABLE ... ADD COLUMNS (<nested>.<field> ...)`` on Snowflake
    catalog-linked Iceberg tables (Glue / Unity Iceberg REST).

    Called from two sites:
    1. the ``is_in_cld_context()`` short-circuit (preferred — fires
       before we hand the DDL to Snowflake at all), and
    2. ``_raise_if_cld_nested_add_sql_error`` (the
       ``SnowparkSQLException`` fallback inside the managed Iceberg
       helper), for the case where the request-level CLD flag wasn't
       seeded and we only learn about the gap when Snowflake rejects
       the rebuild DDL against a catalog-linked database.

    Both sites need the *same* customer-facing message so users see
    one stable error regardless of which path the request took.
    """
    nested_path = ".".join(col_name_parts)
    exception = SnowparkConnectNotImplementedError(
        "Nested struct schema evolution "
        f"(ALTER TABLE ... ADD COLUMNS ({nested_path} ...)) "
        "is not supported on Snowflake catalog-linked "
        f"Iceberg tables ('{table_name}'). The external "
        "catalog (e.g. AWS Glue, Unity Iceberg REST) owns "
        "the struct schema and Snowflake CLD can only "
        "mirror it. Workarounds: (a) add the nested field "
        "via the external catalog directly (e.g. AWS Glue's "
        "UpdateTable API or the Iceberg REST endpoint) and "
        "Snowflake CLD will pick it up on the next metadata "
        "refresh, or (b) recreate the table as a Managed "
        "Iceberg table — which supports nested struct "
        "evolution via ALTER TABLE ... ALTER COLUMN."
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    return exception


def _nested_struct_add_unsupported_on_non_iceberg(
    table_name: str,
    col_name_parts: list[str],
) -> SnowparkConnectNotImplementedError:
    """Build the actionable error for dotted ADD COLUMN against a
    non-Iceberg Snowflake table.

    Snowflake's plain ``ALTER TABLE ... ADD COLUMN`` rejects dotted
    column references with ``001003 / 42000 syntax error ... unexpected
    '.'``, which gives the customer no hint that the operation simply
    isn't supported. We surface that explicitly here.
    """
    nested_path = ".".join(col_name_parts)
    exception = SnowparkConnectNotImplementedError(
        "Nested struct schema evolution "
        f"(ALTER TABLE ... ADD COLUMNS ({nested_path} ...)) "
        f"is not supported on table '{table_name}' because it "
        "is not an Iceberg table. Snowflake only exposes "
        "nested-struct ADD COLUMN via "
        "ALTER ICEBERG TABLE ... ALTER COLUMN ... SET DATA TYPE "
        "on Managed Iceberg tables. Workarounds: (a) recreate "
        "the table as a Managed Iceberg table, or (b) drop "
        "and rebuild the struct column with the desired "
        "fields using ALTER TABLE ... DROP/ADD COLUMN."
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    return exception


def _table_name_on_catalog_linked_db(table_name: str, session: Session) -> bool:
    """Best-effort: is ``table_name`` on a Snowflake catalog-linked database?"""
    if is_in_cld_context():
        return True
    parts = split_fully_qualified_spark_name(table_name)
    if not parts:
        return False
    db_name = parts[0].strip('"').upper()
    if not db_name:
        return False
    try:
        rows = session.sql(
            "SELECT CATALOG_NAME FROM SNOWFLAKE.INFORMATION_SCHEMA.DATABASES "
            "WHERE DATABASE_NAME = ? AND CATALOG_NAME IS NOT NULL",
            params=[db_name],
        ).collect()
        return len(rows) > 0
    except Exception:
        return False


def _should_translate_nested_add_sql_error_to_cld(
    e: SnowparkSQLException,
    table_name: str,
    session: Session,
) -> bool:
    """True when ``e`` is a CLD nested-add rejection, not a DDL builder bug."""
    if not _table_name_on_catalog_linked_db(table_name, session):
        return False
    code = getattr(e, "sql_error_code", None)
    return code in (1003, 93678, 4508)


def _raise_if_cld_nested_add_sql_error(
    e: SnowparkSQLException,
    table_name: str,
    col_name_parts: list[str],
    session: Session,
) -> None:
    if _should_translate_nested_add_sql_error_to_cld(e, table_name, session):
        raise _nested_struct_add_unsupported_on_cld(table_name, col_name_parts) from e
    raise e


def _looks_like_cld_lowercase_identifier_error(e: SnowparkSQLException) -> bool:
    """Best-effort match: is the Snowflake 4510 ``Invalid identifier``
    error pointing at the catalog-linked-database case-insensitive
    identifier restriction?

    Snowflake error text for this case currently looks like:
    ``Invalid identifier <NAME>. Only lowercase and double-quoted
    identifier names are allowed for case insensitive catalog like
    AWS Glue, Unity etc. in catalog-linked databases.``

    We match on the diagnostic phrasing (``catalog-linked database`` +
    either ``lowercase`` or ``case insensitive catalog``) rather than
    on the exact identifier, so future wording tweaks still hit the
    friendlier path. Returns ``False`` on any unexpected shape so
    unrelated 4510s propagate intact.
    """
    msg = (getattr(e, "message", None) or str(e) or "").lower()
    return "catalog-linked database" in msg and (
        "lowercase" in msg or "case insensitive catalog" in msg
    )


def _execute_managed_iceberg_nested_add_column(
    session: Session,
    table_name: str,
    path_parts: list[str],
    spark_data_type: jpype.JObject,
) -> None:
    if len(path_parts) < 2:
        exception = SnowparkConnectNotImplementedError(
            "Nested Iceberg ADD COLUMN requires a nested field path"
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    table_schema = session.table(table_name).schema
    top_level_field = _get_field_by_name(table_schema, path_parts[0])
    if top_level_field is None or not isinstance(top_level_field.datatype, StructType):
        raise _field_not_found_exception(path_parts, path_parts[:1])

    new_type_sql = _add_nested_field_to_structured_sql(
        top_level_field.datatype,
        path_parts[1:],
        spark_data_type,
        path_parts,
    )
    column_name = top_level_field.case_sensitive_name
    session.sql(
        f"ALTER ICEBERG TABLE {table_name} ALTER COLUMN {column_name} "
        f"SET DATA TYPE {new_type_sql}"
    ).collect()


def _normalize_identifiers(node):
    """
    Fix spark-quoted identifiers parsed with sqlglot.

    sqlglot detects quoted spark identifiers which makes them quoted in the Snowflake SQL string.
    This behaviour is not consistent with Spark, where non-column identifiers are case insensitive.
    The identifiers are uppercased to match Snowflake's behaviour when spark.sql.caseSensitive is false.
    """
    if not isinstance(node, Identifier):
        return node
    elif not global_config.spark_sql_caseSensitive:
        return Identifier(this=node.this.upper(), quoted=True)
    else:
        return Identifier(this=node.this, quoted=True)


def _remove_file_format_property(node):
    """
    Fix spark-quoted identifiers parsed with sqlglot.

    sqlglot detects quoted spark identifiers which makes them quoted in the Snowflake SQL string.
    This behaviour is not consistent with Spark, where non-column identifiers are case insensitive.
    The identifiers need to be uppercased to match Snowflake's behaviour.
    """
    if isinstance(node, FileFormatProperty):
        return None
    return node


def _remove_column_data_type(node):
    """
    Fix spark-quoted identifiers parsed with sqlglot.

    sqlglot detects quoted spark identifiers which makes them quoted in the Snowflake SQL string.
    This behaviour is not consistent with Spark, where non-column identifiers are case insensitive.
    The identifiers need to be uppercased to match Snowflake's behaviour.
    """
    if isinstance(node, DataType) and isinstance(node.parent, ColumnDef):
        return None
    return node


def _get_condition_from_action(action, column_mapping, typer):
    condition = None
    if action.condition().isDefined():
        (_, condition_typed_col,) = map_single_column_expression(
            map_logical_plan_expression(action.condition().get()),
            column_mapping,
            typer,
        )
        condition = condition_typed_col.col
    return condition


def _get_assignments_from_action(
    action,
    column_mapping_source,
    column_mapping_target,
    typer_source,
    typer_target,
    target_schema=None,
):
    assignments = dict()
    target_type_by_name = {}
    if target_schema is not None:
        target_type_by_name = {
            unquote_if_quoted(f.name).upper(): f.datatype for f in target_schema.fields
        }

    def _maybe_coerce(col_obj, source_type, assignment_key):
        if not target_type_by_name:
            return col_obj
        target_type = target_type_by_name.get(unquote_if_quoted(assignment_key).upper())
        if target_type is None:
            return col_obj
        coerced = _coerce_to_unstructured_complex_target(
            col_obj, source_type, target_type
        )
        return coerced if coerced is not None else col_obj

    if (
        action.getClass().getSimpleName() == "InsertAction"
        or action.getClass().getSimpleName() == "UpdateAction"
    ):
        incoming_assignments = as_java_list(action.assignments())
        for assignment in incoming_assignments:
            _, key_typ_col = map_single_column_expression(
                map_logical_plan_expression(assignment.key()),
                column_mapping=column_mapping_target,
                typer=typer_target,
            )
            key_name = typer_target.df.select(key_typ_col.col).columns[0]

            _, val_typ_col = map_single_column_expression(
                map_logical_plan_expression(assignment.value()),
                column_mapping=column_mapping_source,
                typer=typer_source,
            )

            assignments[key_name] = _maybe_coerce(
                val_typ_col.col, val_typ_col.typ, key_name
            )
    elif (
        action.getClass().getSimpleName() == "InsertStarAction"
        or action.getClass().getSimpleName() == "UpdateStarAction"
    ):
        if len(column_mapping_source.columns) != len(column_mapping_target.columns):
            exception = ValueError(
                "source and target must have the same number of columns for InsertStarAction or UpdateStarAction"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
            raise exception
        # Build source-type lookup so star-actions can also coerce into
        # unstructured complex target columns.
        source_type_by_name = {}
        if typer_source is not None and typer_source.df is not None:
            source_type_by_name = {
                unquote_if_quoted(f.name).upper(): f.datatype
                for f in typer_source.df.schema.fields
            }
        for i, col in enumerate(column_mapping_target.columns):
            if assignments.get(col.snowpark_name) is not None:
                exception = SnowparkConnectNotImplementedError(
                    "UpdateStarAction or InsertStarAction is not supported with duplicate columns."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            src_name = column_mapping_source.columns[i].snowpark_name
            src_col = snowpark_fn.col(src_name)
            src_type = source_type_by_name.get(unquote_if_quoted(src_name).upper())
            if src_type is not None:
                assignments[col.snowpark_name] = _maybe_coerce(
                    src_col, src_type, col.snowpark_name
                )
            else:
                assignments[col.snowpark_name] = src_col
    return assignments


_SET_COMMAND_SCHEMA = (
    '{"type":"struct","fields":['
    '{"name":"key","type":"string","nullable":false,"metadata":{}},'
    '{"name":"value","type":"string","nullable":false,"metadata":{}}'
    "]}"
)


def _execute_create_namespace(
    session: snowpark.Session,
    name: str,
    if_not_exists: bool,
) -> None:
    """Run ``CREATE SCHEMA`` for Spark's ``CreateNamespace`` DDL.

    When ``if_not_exists`` is true, swallow Snowflake error 2002 (object already
    exists) so ``CREATE NAMESPACE IF NOT EXISTS`` matches Spark's no-op semantics
    on catalog-linked databases that don't honor ``IF NOT EXISTS`` upstream.

    Translate Snowflake error 4510 on case-insensitive catalog-linked databases
    into an actionable ``AnalysisException`` (SNOW-3471833).
    """
    previous_name = session.connection.schema
    if_not_exists_sql = "IF NOT EXISTS " if if_not_exists else ""
    try:
        session.sql(f"CREATE SCHEMA {if_not_exists_sql}{name}").collect()
    except SnowparkSQLException as e:
        # SNOW-3471833: Snowflake catalog-linked databases
        # backed by case-insensitive external catalogs (Unity
        # Iceberg REST, AWS Glue) only accept lowercase or
        # double-quoted schema identifiers. SCOS upper-cases
        # unquoted Spark identifiers by default
        # (``_spark_to_snowflake`` in
        # ``get_relation_identifier_name``), so a
        # vanilla ``CREATE NAMESPACE`` from Spark turns into
        # ``CREATE SCHEMA CLDUNITY.UPPER_NAME`` which fails
        # at the platform with
        # ``004510 / 42601 Invalid identifier <NAME>.
        # Only lowercase and double-quoted identifier
        # names are allowed for case insensitive catalog...``.
        # Surface an actionable AnalysisException that
        # points the customer at the two workarounds rather
        # than letting them chase a phantom syntax bug.
        if getattr(
            e, "sql_error_code", None
        ) == 4510 and _looks_like_cld_lowercase_identifier_error(e):
            exception = AnalysisException(
                "CREATE NAMESPACE failed on a Snowflake "
                "catalog-linked database. Catalog-linked "
                "databases backed by case-insensitive external "
                "catalogs (Unity Iceberg REST, AWS Glue) require "
                "schema identifiers to be lowercase or "
                f"double-quoted. SCOS evaluated '{name}' from "
                "your Spark SQL, which Snowflake's "
                "case-insensitive identifier rules upper-case "
                "before the catalog sees it, and the external "
                "catalog rejected the result. Workarounds: "
                "(a) use a lowercase schema name in your "
                "Spark SQL (e.g. ``CREATE NAMESPACE "
                "catalog.mynamespace``), or (b) quote the "
                "identifier with backticks in Spark SQL "
                "(e.g. ``CREATE NAMESPACE catalog.`MyNs```) "
                "so SCOS forwards it double-quoted. Underlying "
                f"Snowflake error: {e}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception from e
        # SNOW-3471774: Snowflake catalog-linked databases
        # (Glue / Unity Iceberg REST) don't always honor
        # ``IF NOT EXISTS`` on schema creation — the underlying
        # external catalog can surface a hard
        # ``002002 / 42710 Object already exists`` even when
        # the customer's ``CREATE NAMESPACE IF NOT EXISTS``
        # should be a no-op. Spark's reference behavior is
        # "exists => success". Honor that here when
        # ``if_not_exists`` is true.
        if if_not_exists and getattr(e, "sql_error_code", None) == 2002:
            logger.info(
                "CREATE NAMESPACE IF NOT EXISTS %s: target already "
                "exists, treating as no-op (Snowflake error 2002).",
                name,
            )
        else:
            raise
    if previous_name is not None:
        session.sql(f"USE SCHEMA {quote_name(previous_name)}").collect()


def _translate_create_view_snowpark_error(
    e: SnowparkSQLException, view_name: str
) -> None:
    """Re-raise ``CREATE VIEW`` Snowflake errors with Spark-compatible types.

    Snowflake rejects ``CREATE OR REPLACE VIEW`` when a TABLE with the same
    name exists (1998). On catalog-linked databases, ``CREATE VIEW`` surfaces
    93678 — translate that when the session is in CLD context.
    """
    if "already exists" in str(e) and e.sql_error_code == 1998:
        exception = AnalysisException(str(e))
        attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
        raise exception from e
    if getattr(e, "sql_error_code", None) == 93678 and is_in_cld_context():
        exception = AnalysisException(
            "CREATE VIEW is not supported on Snowflake "
            "catalog-linked databases (Glue / Unity "
            "Iceberg REST). The target namespace "
            f"'{view_name}' is backed by an external Iceberg "
            "catalog which does not expose Snowflake "
            "views. Workarounds: (a) create the view "
            "in a regular Snowflake database and "
            "reference the CLD table from there, or "
            "(b) materialize the view contents into a "
            "managed Iceberg table."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception from e
    raise e


def _relation_time_travel_extensions_disabled_exception() -> AnalysisException:
    """Build the SNOW-3471774 error when ``spark.sql.extensions`` is unset."""
    exception = AnalysisException(
        "SQL time travel ('VERSION AS OF' / 'TIMESTAMP AS OF') "
        "is gated on the 'spark.sql.extensions' config naming "
        "the Iceberg Spark SQL extensions class. SCOS implements "
        "time travel natively (no extra JAR install is required), "
        "but the customer-visible support contract still requires "
        "the flag so Snowpark Connect can distinguish "
        "Spark-native time travel from the bare ``RelationTimeTravel`` "
        "plan node Spark 3.3+ also produces on non-Iceberg tables. "
        "Set it on the SCOS server (e.g. in spark-defaults.conf "
        "or via the SPARK_CONF_spark__sql__extensions env var) to: "
        "'org.apache.iceberg.spark.extensions."
        "IcebergSparkSessionExtensions'. This is a static config — "
        "``spark.conf.set()`` from the client is rejected on "
        "purpose by Spark's config rules."
    )
    attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
    return exception


def map_sql_to_pandas_df(
    sql_string: str,
    named_args: MutableMapping[str, expressions_proto.Expression.Literal],
    pos_args: MutableSequence[expressions_proto.Expression.Literal],
) -> tuple[pandas.DataFrame, str] | tuple[None, None]:
    """
    Convert a sql string into a pandas DataFrame and its json schema.
    returns a tuple of empty Pandas DataFrame and schema string in case of DDL statements.
    returns a tuple of None for SELECT queries to enable lazy evaluation
    """

    snowpark_connect_sql_passthrough, sql_string = is_valid_passthrough_sql(sql_string)

    if not snowpark_connect_sql_passthrough:
        logical_plan = sql_parser().parsePlan(sql_string)
        parsed_pos_args = parse_pos_args(logical_plan, pos_args)
        set_sql_args(named_args, parsed_pos_args)

        session = get_or_create_snowpark_session()

        rows: list | None = None

        while (
            class_name := str(logical_plan.getClass().getSimpleName())
        ) == "UnresolvedHint":
            logical_plan = logical_plan.child()

        # TODO: Add support for temporary views for SQL cases such as ShowViews, ShowColumns ect. (Currently the cases are not compatible with Spark, returning raw Snowflake rows)
        match class_name:
            case "AddColumns":
                # Handle ALTER TABLE ... ADD COLUMNS (col_name data_type) -> ADD COLUMN col_name data_type
                table_name = get_relation_identifier_name(logical_plan.table(), True)

                # Get column definitions from logical plan
                columns_to_add = logical_plan.columnsToAdd()
                # Build Snowflake SQL from logical plan attributes
                for col in as_java_list(columns_to_add):
                    # Follow the same pattern as AlterColumn for column name extraction
                    col_name_parts = [str(part) for part in as_java_list(col.name())]
                    if len(col_name_parts) > 1:
                        if is_in_cld_context():
                            # SNOW-3471827: Snowflake catalog-linked
                            # databases (Glue / Unity Iceberg REST) don't
                            # expose the rebuild-the-struct-type DDL that
                            # ``_execute_managed_iceberg_nested_add_column``
                            # uses on Managed Iceberg, so nested struct
                            # column additions are a platform gap. Surface
                            # an actionable message rather than letting
                            # the customer hit an opaque Snowflake error.
                            raise _nested_struct_add_unsupported_on_cld(
                                table_name, col_name_parts
                            )
                        # SNOW-3471774: catalog API may return mixed-case; normalize.
                        if get_table_type(table_name, session).upper() == "ICEBERG":
                            try:
                                _execute_managed_iceberg_nested_add_column(
                                    session,
                                    table_name,
                                    col_name_parts,
                                    col.dataType(),
                                )
                            except SnowparkSQLException as e:
                                _raise_if_cld_nested_add_sql_error(
                                    e, table_name, col_name_parts, session
                                )
                            continue
                        # SNOW-3471827: Dotted column names only make
                        # sense as nested-struct paths, and Snowflake's
                        # plain ``ALTER TABLE ... ADD COLUMN`` does not
                        # accept the dotted syntax (it would compile-error
                        # with ``001003 / 42000 syntax error ... unexpected
                        # '.'``). For non-Iceberg tables this combination
                        # has no Snowflake-side translation, so we surface
                        # a Spark-flavored NotImplementedError instead of
                        # forwarding the dotted DDL and letting the
                        # parser bark at column 60-something.
                        raise _nested_struct_add_unsupported_on_non_iceberg(
                            table_name, col_name_parts
                        )
                    col_name = ".".join(
                        spark_to_sf_single_id(part, is_column=True)
                        for part in col_name_parts
                    )
                    col_type = _spark_datatype_to_sql(col.dataType())
                    snowflake_sql = (
                        f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}"
                    )
                    # Use helper to handle Iceberg tables automatically
                    _execute_alter(session, snowflake_sql, table_name)
            case "AlterColumn":
                # Handle ALTER TABLE ... CHANGE COLUMN (translate to ALTER TABLE ... ALTER COLUMN)
                table_name = get_relation_identifier_name(logical_plan.table(), True)
                column_obj = logical_plan.column()

                # Extract actual column name
                column_name = ".".join(
                    spark_to_sf_single_id(part, is_column=True)
                    for part in as_java_list(column_obj.name())
                )

                if not global_config.spark_sql_caseSensitive:
                    case_insensitive_name = next(
                        (
                            f.name
                            for f in session.table(table_name).schema.fields
                            if f.name.lower() == column_name.lower()
                        ),
                        None,
                    )
                    if case_insensitive_name:
                        column_name = case_insensitive_name

                # Build ALTER COLUMN command from logical plan attributes
                alter_parts = []

                # Check for comment change - Scala Some() vs None
                comment_obj = logical_plan.comment()
                if (
                    comment_obj is not None
                    and str(comment_obj.getClass().getSimpleName()) == "Some"
                ):
                    comment = escape_sql_comment(str(comment_obj.get()))
                    alter_parts.append(f"COMMENT '{comment}'")

                # Check for dataType change - handle Scala Some/None
                data_type_obj = logical_plan.dataType()
                if (
                    data_type_obj is not None
                    and str(data_type_obj.getClass().getSimpleName()) == "Some"
                ):
                    # Extract the actual data type from Scala Some()
                    actual_data_type = data_type_obj.get()
                    data_type = _spark_datatype_to_sql(actual_data_type)
                    alter_parts.append(f"TYPE {data_type}")

                if alter_parts:
                    alter_clause = ", ".join(alter_parts)
                    snowflake_sql = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} {alter_clause}"
                    # Use helper to handle Iceberg tables automatically
                    _execute_alter(session, snowflake_sql, table_name)
                else:
                    exception = ValueError(
                        f"No alter operations found in AlterColumn logical plan for table {table_name}, column {column_name}"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_SQL_SYNTAX)
                    raise exception
            case "CreateNamespace":
                name = get_relation_identifier_name(logical_plan.name(), True)
                _execute_create_namespace(session, name, logical_plan.ifNotExists())
            case "CreateOrReplaceTag":
                # Iceberg Spark SQL Extension DDL:
                #   ALTER TABLE <t> CREATE [OR REPLACE] TAG <name> [IF NOT EXISTS]
                #       [AS OF VERSION <id>] [RETAIN <N> DAYS]
                #   ALTER TABLE <t> REPLACE TAG <name> [AS OF VERSION <id>]
                #       [RETAIN <N> DAYS]
                # Translated to Snowflake's ``CREATE VERSION_TAG`` /
                # ``CREATE OR REPLACE VERSION_TAG`` on
                # ``ALTER ICEBERG TABLE``. Variants that aren't yet
                # confirmed-supported by Snowflake (AS OF VERSION,
                # RETAIN, bare REPLACE) raise UNSUPPORTED_OPERATION
                # with explicit pointers — see ``iceberg_tag_ddl``.
                table_name = _spark_to_snowflake(logical_plan.table())
                snowflake_sql = translate_create_or_replace_tag(
                    logical_plan, table_name
                )
                session.sql(snowflake_sql).collect()
            case "CreateTable" | "ReplaceTable":
                if class_name == "ReplaceTable":
                    replace_table = " OR REPLACE "
                    if_not_exists = ""
                else:
                    replace_table = ""
                    if_not_exists = (
                        "IF NOT EXISTS " if logical_plan.ignoreIfExists() else ""
                    )

                name = get_relation_identifier_name(logical_plan.name())
                full_table_identifier = get_relation_identifier_name(
                    logical_plan.name(), is_multi_part=True
                )
                columns = ", ".join(
                    _spark_field_to_sql(f, True)
                    for f in logical_plan.tableSchema().fields()
                )
                comment_opt = logical_plan.tableSpec().comment()
                comment = (
                    f"COMMENT = '{escape_sql_comment(str(comment_opt.get()))}'"
                    if comment_opt.isDefined()
                    else ""
                )

                data_source = _extract_table_provider(logical_plan)

                # NOTE: We are intentionally ignoring any FORMAT=... parameters here.
                # For USING iceberg, generate CREATE ICEBERG TABLE (required for CLDs)
                table_keyword = "ICEBERG TABLE" if data_source == "iceberg" else "TABLE"
                iceberg_clauses = _build_create_iceberg_table_clauses(
                    data_source=data_source,
                    logical_plan=logical_plan,
                )
                session.sql(
                    f"CREATE {replace_table} {table_keyword} {if_not_exists}{name} "
                    f"({columns}) {iceberg_clauses}{comment}"
                ).collect()

                # Record table metadata for Spark compatibility
                # Tables created with explicit schema are considered v1 tables
                # v1 tables with certain data sources don't support RENAME COLUMN in OSS Spark
                supports_rename = data_source not in (
                    "parquet",
                    "csv",
                    "json",
                    "orc",
                    "avro",
                )
                record_table_metadata(
                    table_identifier=full_table_identifier,
                    table_type="v1",
                    data_source=data_source,
                    supports_column_rename=supports_rename,
                )
            case "CreateTableAsSelect":
                mode = "ignore" if logical_plan.ignoreIfExists() else "errorifexists"
                _create_table_as_select(logical_plan, mode=mode)
            case "CreateTableLikeCommand":
                source = get_relation_identifier_name(logical_plan.sourceTable())
                name = get_relation_identifier_name(logical_plan.targetTable())
                if_not_exists = "IF NOT EXISTS " if logical_plan.ifNotExists() else ""
                session.sql(
                    f"CREATE TABLE {if_not_exists}{name} LIKE {source}"
                ).collect()
            case "CreateTempViewUsing":
                parsed_sql = sqlglot.parse_one(sql_string, dialect="spark")

                spark_view_name = next(parsed_sql.find_all(sqlglot.exp.Table)).name

                # extract ONLY top-level column definitions (not nested struct fields)
                column_defs = []
                schema_node = next(parsed_sql.find_all(sqlglot.exp.Schema), None)
                if schema_node:
                    for expr in schema_node.expressions:
                        if isinstance(expr, sqlglot.exp.ColumnDef):
                            column_defs.append(expr)

                num_columns = len(column_defs)
                if num_columns > 0:
                    null_list_parts = []
                    for col_def in column_defs:
                        col_name = spark_to_sf_single_id(col_def.name, is_column=True)
                        col_type = col_def.kind
                        if col_type:
                            null_list_parts.append(
                                f"CAST(NULL AS {col_type.sql(dialect='snowflake')}) AS {col_name}"
                            )
                        else:
                            null_list_parts.append(f"NULL AS {col_name}")
                    null_list = ", ".join(null_list_parts)
                else:
                    null_list = "*"

                empty_select = (
                    f" AS SELECT {null_list} WHERE 1 = 0"
                    if logical_plan.options().isEmpty()
                    and logical_plan.children().isEmpty()
                    else ""
                )

                transformed_sql = (
                    parsed_sql.transform(_normalize_identifiers)
                    .transform(_remove_column_data_type)
                    .transform(_remove_file_format_property)
                )
                snowflake_sql = transformed_sql.sql(dialect="snowflake")
                session.sql(f"{snowflake_sql}{empty_select}").collect()
                snowflake_view_name = spark_to_sf_single_id_with_unquoting(
                    spark_view_name
                )
                temp_view = get_temp_view(snowflake_view_name)
                if temp_view is not None and not logical_plan.replace():
                    exception = AnalysisException(
                        f"[TEMP_TABLE_OR_VIEW_ALREADY_EXISTS] Cannot create the temporary view `{spark_view_name}` because it already exists."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                    raise exception
                else:
                    register_temp_view(
                        spark_to_sf_single_id_with_unquoting(spark_view_name),
                        True,
                        None,
                        logical_plan.replace(),
                    )
            case "CreateView":
                current_schema = session.connection.schema
                if (
                    str(logical_plan.child().getClass().getSimpleName())
                    == "PlanWithUnresolvedIdentifier"
                ):
                    object_name: str = str(
                        logical_plan.child().identifierExpr().value()
                    )
                else:
                    object_name: str = as_java_list(logical_plan.child().nameParts())[0]
                _accessing_temp_object.set(False)
                df_container = execute_logical_plan(logical_plan.query())
                df = _apply_decimal_schema_emulation(df_container.dataframe)
                if _accessing_temp_object.get():
                    exception = AnalysisException(
                        f"[INVALID_TEMP_OBJ_REFERENCE] Cannot create the persistent object `{CURRENT_CATALOG_NAME}`.`{current_schema}`.`{object_name}` "
                        "of the type VIEW because it references to a temporary object of the type VIEW. Please "
                        f"make the temporary object persistent, or make the persistent object `{CURRENT_CATALOG_NAME}`.`{current_schema}`.`{object_name}` temporary."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                    raise exception

                name = get_relation_identifier_name(logical_plan.child())
                comment = logical_plan.comment()

                df = _rename_columns(
                    df, logical_plan.userSpecifiedColumns(), df_container.column_map
                )

                # TODO: Support logical_plan.replace() == False
                try:
                    df.create_or_replace_view(
                        name,
                        comment=escape_sql_comment(str(comment.get()))
                        if comment.isDefined()
                        else None,
                    )
                except SnowparkSQLException as e:
                    _translate_create_view_snowpark_error(e, name)
            case "CreateViewCommand":
                with push_processed_view(logical_plan.name().identifier()):
                    df_container = execute_logical_plan(logical_plan.plan())
                    df = _apply_decimal_schema_emulation(df_container.dataframe)
                    user_specified_spark_column_names = [
                        str(col._1())
                        for col in as_java_list(logical_plan.userSpecifiedColumns())
                    ]
                    df_container = DataFrameContainer.create_with_column_mapping(
                        dataframe=df,
                        spark_column_names=user_specified_spark_column_names
                        if user_specified_spark_column_names
                        else df_container.column_map.get_spark_columns(),
                        snowpark_column_names=df_container.column_map.get_snowpark_columns(),
                        parent_column_name_map=df_container.column_map,
                    )

                    is_global = isinstance(
                        logical_plan.viewType(),
                        jpype.JClass(
                            "org.apache.spark.sql.catalyst.analysis.GlobalTempView$"
                        ),
                    )

                    def get_cached_view_name() -> str:
                        if is_global:
                            view_name = [
                                global_config.spark_sql_globalTempDatabase,
                                logical_plan.name().quotedString(),
                            ]
                        else:
                            view_name = [logical_plan.name().quotedString()]
                        view_name = [
                            spark_to_sf_single_id_with_unquoting(part)
                            for part in view_name
                        ]
                        return ".".join(view_name)

                    def get_snowflake_view_name() -> list[str]:
                        snowpark_view_name = str(logical_plan.name().identifier())
                        snowpark_view_name = spark_to_sf_single_id(snowpark_view_name)
                        return (
                            [
                                global_config.spark_sql_globalTempDatabase,
                                snowpark_view_name,
                            ]
                            if is_global
                            else [snowpark_view_name]
                        )

                    snowflake_view_name = get_snowflake_view_name()
                    cached_view_name = get_cached_view_name()

                    tmp_views = _get_current_temp_objects()
                    tmp_views.add(
                        (
                            CURRENT_CATALOG_NAME,
                            session.connection.schema,
                            str(logical_plan.name().identifier()),
                        )
                    )

                    def _create_snowflake_temporary_view():
                        if df_container.has_zero_columns():
                            exception = SnowparkConnectNotImplementedError(
                                "Cannot create view with zero columns"
                            )
                            attach_custom_error_code(
                                exception, ErrorCodes.UNSUPPORTED_OPERATION
                            )
                            raise exception

                        comment = logical_plan.comment()
                        maybe_comment = (
                            escape_sql_comment(str(comment.get()))
                            if comment.isDefined()
                            else None
                        )

                        renamed_df = _rename_columns(
                            df,
                            logical_plan.userSpecifiedColumns(),
                            df_container.column_map,
                        )

                        create_snowflake_temporary_view(
                            renamed_df,
                            snowflake_view_name,
                            cached_view_name,
                            logical_plan.replace(),
                            maybe_comment,
                        )

                    if should_create_temporary_view_in_snowflake():
                        _create_snowflake_temporary_view()
                    else:
                        user_specified_spark_column_names = [
                            str(col._1())
                            for col in as_java_list(logical_plan.userSpecifiedColumns())
                        ]
                        spark_column_names = (
                            user_specified_spark_column_names
                            if user_specified_spark_column_names
                            else df_container.column_map.get_spark_columns()
                        )
                        store_temporary_view_as_dataframe(
                            df_container,
                            spark_column_names,
                            df_container.column_map.get_snowpark_columns(),
                            cached_view_name,
                            snowflake_view_name,
                            logical_plan.replace(),
                        )
            case "DescribeColumn":
                name = get_relation_identifier_name_without_uppercasing(
                    logical_plan.column()
                )
                stored_temp_view = get_temp_view(name)
                if stored_temp_view:
                    return (
                        SNOWFLAKE_CATALOG._list_columns_from_dataframe_container(
                            stored_temp_view
                        ),
                        "",
                    )
                # todo double check if this is correct
                name = get_relation_identifier_name(logical_plan.column())
                rows = session.sql(f"DESCRIBE TABLE {name}").collect()
            case "DescribeNamespace":
                name = get_relation_identifier_name(logical_plan.namespace(), True)
                rows = session.sql(f"DESCRIBE SCHEMA {name}").collect()
                if not rows:
                    rows = None
            case "DescribeRelation":
                name = get_relation_identifier_name_without_uppercasing(
                    logical_plan.relation(), True
                )
                stored_temp_view = get_temp_view(name)
                if stored_temp_view:
                    return (
                        SNOWFLAKE_CATALOG._list_columns_from_dataframe_container(
                            stored_temp_view
                        ),
                        "",
                    )

                name = get_relation_identifier_name(logical_plan.relation(), True)
                rows = session.sql(f"DESCRIBE TABLE {name}").collect()
                if not rows:
                    rows = None
            case "DescribeQueryCommand":
                # Handle DESCRIBE QUERY <sql> commands
                # Since Snowflake doesn't support DESCRIBE QUERY syntax, we use DataFrame schema analysis
                # This gets the schema without executing the query (similar to Spark's DESCRIBE QUERY)
                # Get the inner query plan and convert it to SQL
                inner_query_plan = logical_plan.plan()
                df_container = execute_logical_plan(inner_query_plan)
                df = df_container.dataframe
                schema = df.schema

                # Get original Spark column names using the column map from the original DataFrame
                spark_columns = df_container.column_map.get_spark_columns()
                data = []
                for i, field in enumerate(schema.fields):
                    # Use original Spark column name from column map
                    col_name = spark_columns[i]

                    # Convert Snowpark data type to PySpark data type and get simpleString
                    pyspark_type = map_snowpark_to_pyspark_types(field.datatype)
                    data_type_str = pyspark_type.simpleString()

                    data.append(
                        {
                            "col_name": col_name,
                            "data_type": data_type_str,
                            "comment": None,  # Snowflake schema doesn't include comments
                        }
                    )
                return pandas.DataFrame(data), ""
            case "DropFunctionCommand":
                func_name = logical_plan.identifier().funcName().lower()
                input_types, snowpark_name = [], ""
                cache = get_spark_session_cache()
                udf_entry = cache.udfs.get(func_name)
                udtf_entry = cache.udtfs.get(func_name)
                if udf_entry is not None:
                    input_types, snowpark_name = (
                        udf_entry.input_types,
                        udf_entry.name,
                    )
                    cache.udfs.drop(func_name)
                elif udtf_entry is not None:
                    input_types, snowpark_name = (
                        udtf_entry[0].input_types,
                        udtf_entry[0].name,
                    )
                    cache.udtfs.drop(func_name)
                else:
                    if not logical_plan.ifExists():
                        exception = ValueError(
                            f"Function {func_name} not found among registered UDFs or UDTFs."
                        )
                        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                        raise exception
                # Only issue the Snowflake DROP when DDL was actually emitted.
                # For LazySnowparkUdf use _materialized (handles zero-arg UDFs
                # where input_types stays [] even after DDL is emitted).
                # For all other UxFs, non-empty input_types means DDL was emitted.
                _lazy_materialized = (
                    isinstance(udf_entry, LazySnowparkUdf) and udf_entry._materialized
                )
                if snowpark_name != "" and (_lazy_materialized or input_types):
                    if isinstance(udf_entry, LazySnowparkUdf):
                        # Drop every physical variant registered under this logical name.
                        # A lazy UDF emits one Snowflake function per distinct call-site
                        # type signature (_name_to_types tracks them all).
                        if_exists_clause = (
                            "IF EXISTS " if logical_plan.ifExists() else ""
                        )
                        for (
                            variant_name,
                            variant_types,
                        ) in udf_entry._name_to_types.items():
                            sql_params, _ = _build_scala_udf_sql_input_params(
                                variant_types
                            )
                            arg_str = f"({', '.join(p.data_type for p in sql_params)})"
                            session.sql(
                                f"DROP FUNCTION {if_exists_clause}{variant_name}{arg_str}"
                            ).collect()
                    elif udf_entry is not None and udf_entry.kind is UdfKind.SCALA_UDF:
                        # Eager Scala UDF: single physical function, same type-string rules.
                        sql_params, _ = _build_scala_udf_sql_input_params(input_types)
                        argument_string = (
                            f"({', '.join(p.data_type for p in sql_params)})"
                        )
                        session.sql(
                            f"DROP FUNCTION {'IF EXISTS' if logical_plan.ifExists() else ''} {snowpark_name}{argument_string}"
                        ).collect()
                    else:
                        argument_string = f"({', '.join(convert_sp_to_sf_type(arg) for arg in input_types)})"
                        session.sql(
                            f"DROP FUNCTION {'IF EXISTS' if logical_plan.ifExists() else ''} {snowpark_name}{argument_string}"
                        ).collect()
            case "DropNamespace":
                name = get_relation_identifier_name(logical_plan.namespace(), True)
                if_exists = "IF EXISTS " if logical_plan.ifExists() else ""
                session.sql(f"DROP SCHEMA {if_exists}{name}").collect()
            case "DropTable":
                # Spark resolves DROP TABLE to a shadowing temp view before the
                # physical table, and never drops a permanent view (Snowflake
                # rejects that, which we surface as AnalysisException).
                temporary_view_name = get_relation_identifier_name_without_uppercasing(
                    logical_plan.child()
                )
                name = get_relation_identifier_name(logical_plan.child())
                if not unregister_snowflake_temp_view(
                    session, temporary_view_name, name, logical_plan.ifExists()
                ):
                    if_exists = "IF EXISTS " if logical_plan.ifExists() else ""
                    try:
                        session.sql(f"DROP TABLE {if_exists}{name}").collect()
                    except SnowparkSQLException as e:
                        if "not specified type 'TABLE'" in str(e):
                            exception = AnalysisException(str(e))
                            attach_custom_error_code(
                                exception, ErrorCodes.INVALID_OPERATION
                            )
                            raise exception from e
                        raise
            case "DropTag":
                # Iceberg Spark SQL Extension DDL:
                #   ALTER TABLE <t> DROP TAG [IF EXISTS] <name>
                # Translated to Snowflake's ``DROP VERSION_TAG`` on
                # ``ALTER ICEBERG TABLE``. See ``iceberg_tag_ddl``.
                table_name = _spark_to_snowflake(logical_plan.table())
                snowflake_sql = translate_drop_tag(logical_plan, table_name)
                session.sql(snowflake_sql).collect()
            case "DropView":
                # DROP VIEW drops a temp view (in-memory or Snowflake-backed) or
                # a permanent view; a name resolving to a TABLE raises
                # AnalysisException to match Spark.
                temporary_view_name = get_relation_identifier_name_without_uppercasing(
                    logical_plan.child()
                )
                name = get_relation_identifier_name(logical_plan.child())
                if not unregister_snowflake_temp_view(
                    session, temporary_view_name, name, logical_plan.ifExists()
                ):
                    if_exists = "IF EXISTS " if logical_plan.ifExists() else ""
                    try:
                        session.sql(f"DROP VIEW {if_exists}{name}").collect()
                    except SnowparkSQLException as e:
                        if "not specified type 'VIEW'" in str(e):
                            exception = AnalysisException(str(e))
                            attach_custom_error_code(
                                exception, ErrorCodes.INVALID_OPERATION
                            )
                            raise exception from e
                        raise
            case "ExplainCommand":
                inner_plan = logical_plan.logicalPlan()
                logical_plan_name = inner_plan.nodeName()

                # Handle EXPLAIN DESCRIBE QUERY commands
                if logical_plan_name == "DescribeQueryCommand":
                    # For EXPLAIN DESCRIBE QUERY, we should return an explanation of the describe operation itself
                    # NOT execute the inner query to get its SQL
                    query_plan = inner_plan.plan()
                    plan_description = (
                        f"Describe query plan for: {query_plan.nodeName()}"
                    )
                    rows = [snowpark.Row(plan=plan_description)]
                elif logical_plan_name == "DescribeRelation":
                    # For EXPLAIN DESCRIBE RELATION, we should return an explanation of the describe operation itself
                    # NOT execute the inner query to get its SQL
                    relation = inner_plan.relation()
                    plan_description = (
                        f"Describe relation plan for: {relation.commandName()}"
                    )
                    rows = [snowpark.Row(plan=plan_description)]
                elif logical_plan_name == "DescribeColumn":
                    # For EXPLAIN DESCRIBE COLUMN, we should return an explanation of the describe operation itself
                    # NOT execute the inner query to get its SQL
                    column = inner_plan.column()
                    plan_description = f"Describe column plan for: [{column.name()}]"
                    rows = [snowpark.Row(plan=plan_description)]
                elif logical_plan_name in (
                    "Project",
                    "Aggregate",
                    "Sort",
                    "UnresolvedWith",
                    "UnresolvedHaving",
                    "Distinct",
                ):
                    expr = execute_logical_plan(
                        logical_plan.logicalPlan()
                    ).dataframe.queries["queries"][0]
                    final_sql = f"EXPLAIN USING TEXT {expr}"
                    rows = session.sql(final_sql).collect()
                elif (
                    logical_plan_name == "InsertIntoStatement"
                    or logical_plan_name == "CreateView"
                ):
                    expr = execute_logical_plan(
                        logical_plan.logicalPlan().query()
                    ).dataframe.queries["queries"][0]
                    final_sql = f"EXPLAIN USING TEXT {expr}"
                    rows = session.sql(final_sql).collect()
                else:
                    # TODO: Support other logical plans
                    exception = SnowparkConnectNotImplementedError(
                        f"{logical_plan_name} is not supported yet with EXPLAIN."
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception
            case "InsertIntoStatement":
                num_inserted = _insert_into_table(logical_plan, session)
                if get_return_dml_metadata_enabled():
                    return (
                        _spark_dml_metadata_dataframe(
                            "insert", num_inserted or 0, 0, 0
                        ),
                        "",
                    )
            case "MergeIntoTable":
                source_df_container = map_relation(
                    map_logical_plan_relation(logical_plan.sourceTable())
                )
                source_df = source_df_container.dataframe
                plan_id = gen_sql_plan_id()
                target_df_container = map_relation(
                    map_logical_plan_relation(logical_plan.targetTable(), plan_id)
                )
                target_df = target_df_container.dataframe

                if (
                    logical_plan.targetTable().getClass().getSimpleName()
                    == "UnresolvedRelation"
                ):
                    target_table_name = _spark_to_snowflake(
                        logical_plan.targetTable().multipartIdentifier()
                    )
                else:
                    target_table_name = _spark_to_snowflake(
                        logical_plan.targetTable().child().multipartIdentifier()
                    )

                target_table = session.table(target_table_name)
                target_table_columns = target_table.columns
                target_df_spark_names = [
                    c.spark_name for c in target_df_container.column_map.columns
                ]
                if target_table_columns:
                    target_df = target_df.select(
                        [
                            snowpark_fn.col(target_df_col.snowpark_name).alias(
                                target_table_col
                            )
                            for target_table_col, target_df_col in zip(
                                target_table_columns,
                                target_df_container.column_map.columns,
                            )
                        ]
                    )
                target_df_container = DataFrameContainer.create_with_column_mapping(
                    dataframe=target_df,
                    spark_column_names=target_df_spark_names,
                    snowpark_column_names=target_table_columns,
                )

                set_plan_id_map(plan_id, target_df_container)

                joined_df_before_condition: snowpark.DataFrame = source_df.join(
                    target_df
                )

                column_mapping_for_conditions = column_name_handler.JoinColumnNameMap(
                    source_df_container.column_map,
                    target_df_container.column_map,
                )
                typer_for_expressions = ExpressionTyper(joined_df_before_condition)

                (_, merge_condition_typed_col,) = map_single_column_expression(
                    map_logical_plan_expression(logical_plan.mergeCondition()),
                    column_mapping=column_mapping_for_conditions,
                    typer=typer_for_expressions,
                )

                clauses = []

                for matched_action in as_java_list(logical_plan.matchedActions()):
                    condition = _get_condition_from_action(
                        matched_action,
                        column_mapping_for_conditions,
                        typer_for_expressions,
                    )
                    if matched_action.getClass().getSimpleName() == "DeleteAction":
                        clauses.append(when_matched(condition).delete())
                    elif (
                        matched_action.getClass().getSimpleName() == "UpdateAction"
                        or matched_action.getClass().getSimpleName()
                        == "UpdateStarAction"
                    ):
                        assignments = _get_assignments_from_action(
                            matched_action,
                            source_df_container.column_map,
                            target_df_container.column_map,
                            ExpressionTyper(source_df),
                            ExpressionTyper(target_df),
                            target_schema=target_df.schema,
                        )
                        clauses.append(when_matched(condition).update(assignments))

                for not_matched_action in as_java_list(
                    logical_plan.notMatchedActions()
                ):
                    condition = _get_condition_from_action(
                        not_matched_action,
                        column_mapping_for_conditions,
                        typer_for_expressions,
                    )
                    if (
                        not_matched_action.getClass().getSimpleName() == "InsertAction"
                        or not_matched_action.getClass().getSimpleName()
                        == "InsertStarAction"
                    ):
                        assignments = _get_assignments_from_action(
                            not_matched_action,
                            source_df_container.column_map,
                            target_df_container.column_map,
                            ExpressionTyper(source_df),
                            ExpressionTyper(target_df),
                            target_schema=target_df.schema,
                        )
                        clauses.append(when_not_matched(condition).insert(assignments))

                if not as_java_list(logical_plan.notMatchedBySourceActions()).isEmpty():
                    exception = SnowparkConnectNotImplementedError(
                        "Snowflake does not support 'not matched by source' actions in MERGE statements."
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception

                merge_res = target_table.merge(
                    source_df, merge_condition_typed_col.col, clauses
                )
                if get_return_dml_metadata_enabled():
                    return (
                        _spark_dml_metadata_dataframe(
                            "merge",
                            merge_res.rows_inserted,
                            merge_res.rows_updated,
                            merge_res.rows_deleted,
                        ),
                        "",
                    )
            case "DeleteFromTable":
                df_container = map_relation(
                    map_logical_plan_relation(logical_plan.table())
                )
                name = get_relation_identifier_name(logical_plan.table(), True)
                table = session.table(name)
                table_columns = table.columns
                df = df_container.dataframe
                spark_names = [c.spark_name for c in df_container.column_map.columns]
                if table_columns:
                    df = df.select(
                        [
                            snowpark_fn.col(df_col.snowpark_name).alias(table_col)
                            for table_col, df_col in zip(
                                table_columns,
                                df_container.column_map.columns,
                            )
                        ]
                    )
                df_container = DataFrameContainer.create_with_column_mapping(
                    dataframe=df,
                    spark_column_names=spark_names,
                    snowpark_column_names=table_columns,
                )
                df = df_container.dataframe
                (
                    condition_column_name,
                    condition_typed_col,
                ) = map_single_column_expression(
                    map_logical_plan_expression(logical_plan.condition()),
                    df_container.column_map,
                    ExpressionTyper(df),
                )
                del_res = table.delete(condition_typed_col.col)
                if get_return_dml_metadata_enabled():
                    return (
                        _spark_dml_metadata_dataframe(
                            "delete", 0, 0, del_res.rows_deleted
                        ),
                        "",
                    )
            case "UpdateTable":
                df_container = map_relation(
                    map_logical_plan_relation(logical_plan.table())
                )
                name = get_relation_identifier_name(logical_plan.table(), True)
                tbl = session.table(name)
                table_columns = tbl.columns
                df = df_container.dataframe
                spark_names = []
                for table_col, df_col in zip(
                    table_columns, df_container.column_map.columns
                ):
                    df = df.with_column_renamed(
                        df_col.snowpark_name,
                        table_col,
                    )
                    spark_names.append(df_col.spark_name)
                df_container = DataFrameContainer.create_with_column_mapping(
                    dataframe=df,
                    spark_column_names=spark_names,
                    snowpark_column_names=table_columns,
                )
                df = df_container.dataframe
                typer = ExpressionTyper(df)
                # Build a case-normalized lookup of target column types so that
                # assignments into VARIANT / unstructured ARRAY / OBJECT columns
                # can be cast via the shared helper.
                target_type_by_name = {
                    unquote_if_quoted(f.name).upper(): f.datatype
                    for f in tbl.schema.fields
                }
                assignments = {}
                for assignment in as_java_list(logical_plan.assignments()):
                    _, key_typ_col = map_single_column_expression(
                        map_logical_plan_expression(assignment.key()),
                        column_mapping=df_container.column_map,
                        typer=typer,
                    )
                    key_name = key_typ_col.col.get_name()
                    _, val_typ_col = map_single_column_expression(
                        map_logical_plan_expression(assignment.value()),
                        column_mapping=df_container.column_map,
                        typer=typer,
                    )
                    assignment_col = val_typ_col.col
                    target_datatype = target_type_by_name.get(
                        unquote_if_quoted(key_name).upper()
                    )
                    if target_datatype is not None:
                        coerced = _coerce_to_unstructured_complex_target(
                            assignment_col,
                            val_typ_col.typ,
                            target_datatype,
                        )
                        if coerced is not None:
                            assignment_col = coerced
                    assignments[key_name] = assignment_col
                cond_opt = logical_plan.condition()
                if cond_opt.isDefined():
                    _, condition_typed_col = map_single_column_expression(
                        map_logical_plan_expression(cond_opt.get()),
                        df_container.column_map,
                        typer,
                    )
                    upd_res = tbl.update(assignments, condition_typed_col.col)
                else:
                    upd_res = tbl.update(assignments)
                if get_return_dml_metadata_enabled():
                    return (
                        _spark_dml_metadata_dataframe(
                            "update", 0, upd_res.rows_updated, 0
                        ),
                        "",
                    )
            case "RenameColumn":
                full_table_identifier = get_relation_identifier_name(
                    logical_plan.table(), True
                )

                # Check Spark compatibility for RENAME COLUMN operation
                if not check_table_supports_operation(
                    full_table_identifier, "rename_column"
                ):
                    exception = AnalysisException(
                        f"ALTER TABLE RENAME COLUMN is not supported for table '{full_table_identifier}'. "
                        f"This table was created as a v1 table with a data source that doesn't support column renaming. "
                        f"To enable this operation, set 'snowpark.connect.enable_snowflake_extension_behavior' to 'true'."
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception

                column_obj = logical_plan.column()
                old_column_name = ".".join(
                    spark_to_sf_single_id(str(part), is_column=True)
                    for part in as_java_list(column_obj.name())
                )
                if not global_config.spark_sql_caseSensitive:
                    case_insensitive_name = next(
                        (
                            f.name
                            for f in session.table(full_table_identifier).schema.fields
                            if f.name.lower() == old_column_name.lower()
                        ),
                        None,
                    )
                    if case_insensitive_name:
                        old_column_name = case_insensitive_name
                new_column_name = spark_to_sf_single_id(
                    str(logical_plan.newName()), is_column=True
                )

                # Pass through to Snowflake
                snowflake_sql = f"ALTER TABLE {full_table_identifier} RENAME COLUMN {old_column_name} TO {new_column_name}"
                # Use helper to handle Iceberg tables automatically
                _execute_alter(session, snowflake_sql, full_table_identifier)
            case "RenameTable":
                name = get_relation_identifier_name(logical_plan.child(), True)
                new_name = _spark_to_snowflake(logical_plan.newName())

                try:
                    session.sql(f"ALTER TABLE {name} RENAME TO {new_name}").collect()
                except Exception as e:
                    # This is a trick to rename iceberg tables without having to first sacrifice a query to determine
                    # whether the source table is an iceberg table.
                    # TODO(SNOW-2118744): such keyword is required for other ALTER TABLE commands against Iceberg tables
                    # too.
                    if str(e).find("is an Iceberg table") >= 0:
                        session.sql(
                            f"ALTER ICEBERG TABLE {name} RENAME TO {new_name}"
                        ).collect()
                    else:
                        attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
                        raise e
            case "ReplaceTableAsSelect":
                _create_table_as_select(logical_plan, mode="overwrite")
            case "ResetCommand":
                key = logical_plan.config().get()
                unset_config_param(get_spark_session_id(), key, session)
            case "SetCatalogAndNamespace":
                # TODO: add catalog setting here
                name = get_relation_identifier_name(logical_plan.child(), True)
                session.sql(f"USE SCHEMA {name}").collect()
            case "SetCommand":
                kv_result_tuple = logical_plan.kv().get()
                key = kv_result_tuple._1()
                val = kv_result_tuple._2().get()
                set_config_param(get_spark_session_id(), key, val, session)
                return (
                    pandas.DataFrame([{"key": key, "value": val}]),
                    _SET_COMMAND_SCHEMA,
                )
            case "SetNamespaceCommand":
                name = _spark_to_snowflake(logical_plan.namespace())
                session.sql(f"USE SCHEMA {name}").collect()
            case "SetNamespaceLocation" | "SetNamespaceProperties":
                exception = SnowparkConnectNotImplementedError(
                    "Altering databases is not currently supported."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception
            case "ShowCreateTable":
                # Handle SHOW CREATE TABLE command
                # Spark: SHOW CREATE TABLE table_name
                # Snowflake: SELECT get_ddl('table', 'table_name')
                table_relation = logical_plan.child()
                table_name = _spark_to_snowflake(table_relation.multipartIdentifier())

                # Convert to Snowflake get_ddl function
                snowflake_sql = f"SELECT get_ddl('table', '{table_name}') AS ddl"
                rows = session.sql(snowflake_sql).collect()

            case "ShowCurrentNamespaceCommand":
                name = session.get_current_schema()
                unquoted_name = unquote_if_quoted(name)
                sql = f"SHOW SCHEMAS LIKE '{unquoted_name}'"
                rows = session.sql(sql).collect()
                if not rows:
                    rows = None
            case "ShowNamespaces":
                from snowflake.snowpark_connect.relation.catalogs.utils import (
                    get_current_catalog,
                )

                name = get_relation_identifier_name(logical_plan.namespace(), True)
                pattern = None
                if logical_plan.pattern().isDefined():
                    pattern = logical_plan.pattern().get()

                rows = None
                result_df = None
                if name:
                    unquoted_name = unquote_if_quoted(name)
                    lower_name = unquoted_name.lower()
                    if lower_name in _KNOWN_CATALOG_NAMES:
                        # ``SHOW NAMESPACES IN <catalog_alias>``: both
                        # ``spark_catalog`` and ``snowflake_catalog`` are
                        # aliases for the current catalog, so list its
                        # namespaces. listDatabases(pattern) filters by
                        # schema name only, not by a db.schema glob, so
                        # pass the pattern through.
                        result_df = get_current_catalog().listDatabases(pattern)
                    else:
                        # ``SHOW NAMESPACES IN <db>`` where ``<db>`` is a
                        # Snowflake database name. ``listDatabases`` always
                        # scopes to the current database, so issue
                        # ``SHOW SCHEMAS IN DATABASE`` directly.
                        # ``quote_name`` escapes embedded quotes so user
                        # identifiers can't break out of the SQL string.
                        rows = session.sql(
                            f"SHOW SCHEMAS IN DATABASE {quote_name(unquoted_name)}"
                        ).collect()
                        if pattern:
                            rows = _filter_tables_by_pattern(rows, pattern)
                        if not rows:
                            rows = None
                else:
                    result_df = get_current_catalog().listDatabases(pattern)

                if result_df is not None:
                    # Default ``itertuples`` returns named tuples whose
                    # ``_fields`` are the DataFrame's column names, so the
                    # downstream ``pandas.DataFrame(rows)`` keeps proper
                    # column names instead of falling back to ``'0', '1', …``.
                    rows = (
                        list(result_df.itertuples(index=False))
                        if not result_df.empty
                        else None
                    )
            case "ShowTables" | "ShowTableExtended":
                name = get_relation_identifier_name(logical_plan.namespace(), True)

                # Get the pattern for filtering
                pattern = None
                if class_name == "ShowTables" and logical_plan.pattern().isDefined():
                    pattern = logical_plan.pattern().get()
                elif (
                    class_name == "ShowTableExtended"
                    and len(logical_plan.pattern()) != 0
                ):
                    pattern = logical_plan.pattern()

                # Execute SHOW TABLES command
                if name:
                    rows = session.sql(f"SHOW TABLES IN {name}").collect()
                else:
                    rows = session.sql("SHOW TABLES").collect()

                # Return empty DataFrame with proper schema if no results
                if not rows:
                    if class_name == "ShowTableExtended":
                        return (
                            pandas.DataFrame(
                                {
                                    "namespace": [""],
                                    "tableName": [""],
                                    "isTemporary": [""],
                                    "information": [""],
                                }
                            ),
                            "",
                        )
                    else:
                        return (
                            pandas.DataFrame(
                                {
                                    "namespace": [""],
                                    "tableName": [""],
                                    "isTemporary": [""],
                                }
                            ),
                            "",
                        )

                # Apply pattern filtering if pattern is provided
                # This is workaround to filter using Python regex.
                if pattern and rows:
                    rows = _filter_tables_by_pattern(rows, pattern)

                if (
                    rows
                    and global_config.snowpark_connect_enable_partition_specs_in_show_tables
                ):
                    return (
                        _enrich_show_tables_with_partition_spec(rows, name, session),
                        "",
                    )
            case "ShowViews":
                name = get_relation_identifier_name(logical_plan.namespace(), True)

                # Get the pattern for filtering
                pattern = (
                    logical_plan.pattern().get()
                    if logical_plan.pattern().isDefined()
                    else None
                )

                # Execute SHOW VIEWS command
                if name:
                    rows = session.sql(f"SHOW VIEWS IN {name}").collect()
                else:
                    rows = session.sql("SHOW VIEWS").collect()

                # Apply pattern filtering if pattern is provided
                if pattern and rows:
                    rows = _filter_tables_by_pattern(rows, pattern)
            case "ShowColumns":
                name = get_relation_identifier_name_without_uppercasing(
                    logical_plan.child(), True
                )
                stored_temp_view = get_temp_view(name)
                if stored_temp_view:
                    return (
                        SNOWFLAKE_CATALOG._list_columns_from_dataframe_container(
                            stored_temp_view
                        ),
                        "",
                    )

                # Handle Spark SQL: SHOW COLUMNS IN table_name FROM database_name
                # Convert to Snowflake SQL: SHOW COLUMNS IN TABLE database_name.table_name

                # Extract table name from ShowColumns logical plan
                # The child() is an UnresolvedTable object, use the existing helper function
                table_relation = logical_plan.child()
                db_and_table_name = as_java_list(table_relation.multipartIdentifier())
                multi_part_len = len(db_and_table_name)
                table_name = _spark_to_snowflake(table_relation.multipartIdentifier())

                db_name = None
                # Get database name if specified in namespace
                if logical_plan.namespace().isDefined():
                    db_namespace = logical_plan.namespace().get()
                    db_name = _spark_to_snowflake(db_namespace)

                # Build the Snowflake SHOW COLUMNS command
                if db_name and multi_part_len == 1:
                    # Full qualified table name: db.table
                    full_table_name = f"{db_name}.{table_name}"
                    snowflake_cmd = f"SHOW COLUMNS IN TABLE {full_table_name}"
                else:
                    if db_name and multi_part_len == 2:
                        # Check db_name is same as in the full table name
                        if (
                            spark_to_sf_single_id(str(db_and_table_name[0])).casefold()
                            != db_name.casefold()
                        ):
                            exception = AnalysisException(
                                f"database name is not matching:{db_name} and {db_and_table_name[0]}"
                            )
                            attach_custom_error_code(
                                exception, ErrorCodes.INVALID_OPERATION
                            )
                            raise exception

                            # Just table name
                    snowflake_cmd = f"SHOW COLUMNS IN TABLE {table_name}"

                rows = session.sql(snowflake_cmd).collect()
            case "TruncateTable":
                name = get_relation_identifier_name(logical_plan.table(), True)
                session.sql(f"TRUNCATE TABLE {name}").collect()

            case command if (
                command.startswith("Alter")
                or command.startswith("Create")
                or command.startswith("Drop")
                or command.startswith("Rename")
                or command.startswith("Replace")
                or command.startswith("Set")
                or command.startswith("Truncate")
                or command.startswith("AddColumns")
            ):
                parsed_sql = sqlglot.parse_one(sql_string, dialect="spark").transform(
                    _normalize_identifiers
                )
                snowflake_sql = parsed_sql.sql(dialect="snowflake")
                if snowflake_sql.upper().startswith("ALTER TABLE "):
                    table_name = _extract_alter_table_name(snowflake_sql)
                    _execute_alter(session, snowflake_sql, table_name)
                else:
                    session.sql(snowflake_sql).collect()
            case command if command.startswith("Describe") or command.startswith(
                "Show"
            ):
                parsed_sql = sqlglot.parse_one(sql_string, dialect="spark").transform(
                    _normalize_identifiers
                )
                snowflake_sql = parsed_sql.sql(dialect="snowflake")
                if command.startswith("Show"):
                    if snowflake_sql.startswith("SHOW TBLPROPERTIES"):
                        # Snowflake doesn't support TBLPROPERTIES, EXTENDED.
                        return pandas.DataFrame({"": [""]}), ""

                rows = session.sql(snowflake_sql).collect()
            case "RefreshTable":
                table_name_unquoted = ".".join(
                    str(part)
                    for part in as_java_list(logical_plan.child().multipartIdentifier())
                )
                SNOWFLAKE_CATALOG.refreshTable(table_name_unquoted)
            case "RepairTable":
                # No-Op: Snowflake doesn't have explicit partitions to repair.
                table_relation = logical_plan.child()
                db_and_table_name = as_java_list(table_relation.multipartIdentifier())
                multi_part_len = len(db_and_table_name)

                if multi_part_len == 1:
                    table_name = db_and_table_name[0]
                    db_name = None
                    full_table_name = table_name
                else:
                    db_name = db_and_table_name[0]
                    table_name = db_and_table_name[1]
                    full_table_name = db_name + "." + table_name

                df = SNOWFLAKE_CATALOG.tableExists(table_name, db_name)

                table_exist = df.iloc[0, 0]

                if not table_exist:
                    exception = AnalysisException(
                        f"[TABLE_OR_VIEW_NOT_FOUND] Table not found `{full_table_name}`."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_OPERATION)
                    raise exception
            case "UnresolvedWith":
                child = logical_plan.child()
                child_class = str(child.getClass().getSimpleName())
                match child_class:
                    case "InsertIntoStatement":
                        with _with_cte_scope(logical_plan.cteRelations()):
                            num_inserted = _insert_into_table(
                                child, get_or_create_snowpark_session()
                            )
                        if get_return_dml_metadata_enabled():
                            return (
                                _spark_dml_metadata_dataframe(
                                    "insert", num_inserted or 0, 0, 0
                                ),
                                "",
                            )
                    case _:
                        # TODO: SNOW-3007195, we can optimize by skipping execution using finer-grained child_class checks.
                        execute_logical_plan(logical_plan)
                        return None, None
            case _:
                execute_logical_plan(logical_plan)
                return None, None
    else:
        # spark.sql("select or cte+select") queries should be executed lazily.
        # This returns an empty dataframe and empty schema.
        # if is_sql_select_statement(_trim_sql_string(sql_string)):
        if _is_sql_select_statement_helper(sql_string):
            return None, None
        session = snowpark.Session.get_active_session()
        rows = session.sql(sql_string).collect()
    if rows:
        return pandas.DataFrame(rows), ""
    return pandas.DataFrame(), '{"type": "struct", "fields": []}'


def get_sql_passthrough() -> bool:
    return get_boolean_session_config_param("snowpark.connect.sql.passthrough")


def is_valid_passthrough_sql(sql_stmt: str) -> Tuple[bool, str]:
    """
    Checks if :param sql_stmt: should be executed as SQL pass-through. SQL pass-through can be detected in 1 of 2 ways:
    1) :param sql_stmt: is created through SnowflakeSession and has correct marker + checksum
    2) Spark config parameter "snowpark.connect.sql.passthrough" is set (legacy mode, to be deprecated)
    """

    # check for new style, SnowflakeSession based SQL pass-through
    sql_parts = sql_stmt.split(" ", 2)
    if len(sql_parts) == 3:
        marker, checksum, sql = sql_parts
        if marker == SQL_PASS_THROUGH_MARKER and checksum == calculate_checksum(sql):
            return True, sql

    # SQL pass-through based on the config
    return get_sql_passthrough(), sql_stmt


def change_default_to_public(name: str) -> str:
    """
    Change the namespace to PUBLIC when given name is DEFAULT
    :param name: Given namespace
    :return: if name is DEFAULT return PUBLIC otherwise name
    """
    if name.startswith('"'):
        if name.upper() == '"DEFAULT"':
            return name.replace("DEFAULT", "PUBLIC")
    elif name.upper() == "DEFAULT":
        return "PUBLIC"
    return name


def _preprocess_identifier_calls(sql_query: str) -> str:
    """
    Pre-process SQL query to resolve IDENTIFIER() calls before Spark parsing.

    Transforms: IDENTIFIER('abs')(c2) -> abs(c2)
    Transforms: IDENTIFIER('COAL' || 'ESCE')(NULL, 1) -> COALESCE(NULL, 1)

    This preserves all function arguments in their original positions, eliminating
    the need to reconstruct them at the expression level.
    """
    import re

    # Pattern to match IDENTIFIER(...) followed by optional function call arguments
    # This captures both the identifier expression and any trailing arguments
    # Note: We need to be careful about whitespace preservation
    identifier_pattern = r"IDENTIFIER\s*\(\s*([^)]+)\s*\)(\s*)(\([^)]*\))?"

    def resolve_identifier_match(match):
        identifier_expr_str = match.group(1).strip()
        whitespace = match.group(2) if match.group(2) else ""
        function_args = match.group(3) if match.group(3) else ""

        try:
            # Handle string concatenation FIRST: IDENTIFIER('COAL' || 'ESCE')
            # (Must check this before simple strings since it also starts/ends with quotes)
            if "||" in identifier_expr_str:
                # Parse basic string concatenation with proper quote handling
                parts = []
                split_parts = identifier_expr_str.split("||")
                for part in split_parts:
                    part = part.strip()
                    if part.startswith("'") and part.endswith("'"):
                        unquoted = part[1:-1]  # Remove quotes from each part
                        parts.append(unquoted)
                    else:
                        # Non-string parts - return original for safety
                        return match.group(0)
                resolved_name = "".join(parts)  # Concatenate the unquoted parts

            # Handle simple string literals: IDENTIFIER('abs')
            elif identifier_expr_str.startswith("'") and identifier_expr_str.endswith(
                "'"
            ):
                resolved_name = identifier_expr_str[1:-1]  # Remove quotes

            else:
                # Complex expressions not supported yet - return original
                return match.group(0)

            # Return resolved function call with preserved arguments and whitespace
            if function_args:
                # Function call case: IDENTIFIER('abs')(c1) -> abs(c1)
                result = f"{resolved_name}{function_args}"
            else:
                # Column reference case: IDENTIFIER('c1') FROM -> c1 FROM (preserve whitespace)
                result = f"{resolved_name}{whitespace}"
            return result

        except Exception:
            # Return original to avoid breaking the query
            return match.group(0)

    # Apply the transformation
    processed_query = re.sub(
        identifier_pattern, resolve_identifier_match, sql_query, flags=re.IGNORECASE
    )

    return processed_query


def map_sql(
    rel: relation_proto.Relation,
) -> DataFrameContainer:
    """
    Map a SQL string to a DataFrame.

    The SQL string is executed and the resulting DataFrame is returned.

    In passthough mode as True, SAS calls session.sql() and not calling Spark Parser.
    This is to mitigate any issue not covered by spark logical plan to protobuf conversion.
    """
    snowpark_connect_sql_passthrough, sql_stmt = is_valid_passthrough_sql(rel.sql.query)

    if not snowpark_connect_sql_passthrough:
        # No raw-SQL pre-scan for quoted identifiers: scanning the SQL text
        # with a regex incorrectly matches inside quoted string literals and
        # comments (Felix's PR #4052 review on map_sql.py:519). Per-identifier
        # backtick state is recovered from the JVM parser's Origin substring
        # at each `case "UnresolvedRelation":` site instead, which by
        # construction can't see inside string literals.

        # Changed from parseQuery to parsePlan as Spark parseQuery() call generating wrong logical plan for
        # query like this: SELECT cast('3.4' as decimal(38, 18)) UNION SELECT 'foo'
        # As such other place in this file we use parsePlan.
        # Main difference between parsePlan() and parseQuery() is, parsePlan() can be called for any SQL statement, while
        # parseQuery() can only be called for query statements.
        logical_plan = sql_parser().parsePlan(sql_stmt)

        parsed_pos_args = parse_pos_args(logical_plan, rel.sql.pos_args)
        set_sql_args(rel.sql.args, parsed_pos_args)

        return execute_logical_plan(logical_plan)
    else:
        session = snowpark.Session.get_active_session()
        # Remove trailing semicolons and whitespace to prevent "unexpected ';'" errors when performing operations
        # on the resulting DataFrame
        # Example: session.sql("SELECT 1;").show() would fail without this sanitization.
        sql_stmt = sql_stmt.rstrip().rstrip(";")
        sql_df = session.sql(sql_stmt)

        if not rel.common.HasField("plan_id"):
            plan_id = gen_sql_plan_id()
            rel.common.plan_id = plan_id

        return post_process_df(sql_df, rel.common.plan_id)


def map_logical_plan_relation(
    rel, plan_id: int | None = None
) -> relation_proto.Relation:
    if plan_id is None:
        plan_id = gen_sql_plan_id()
    session = get_or_create_snowpark_session()

    class_name = str(rel.getClass().getSimpleName())
    match class_name:
        case "Aggregate":
            with push_sql_scope():
                input = map_logical_plan_relation(rel.child())

                # For LCA support in GROUP BY, we need to extract aliases from the aggregate expressions
                # In Spark SQL, when you write "SELECT a as k, COUNT(b) FROM table GROUP BY k",
                # the aliases are defined in the aggregateExpressions, not in a separate Project node
                alias_map = {}

                # Extract aliases from the aggregate expressions (SELECT clause)
                alias_map = {}
                for agg_expr in as_java_list(rel.aggregateExpressions()):
                    if str(agg_expr.getClass().getSimpleName()) == "Alias":
                        alias_map[str(agg_expr.name())] = agg_expr.child()

                def substitute_lca_in_grouping_expr(expr):
                    """Substitute LCA references with original expressions and handle ordinal references"""
                    expr_class = str(expr.getClass().getSimpleName())

                    # Handle ordinal references (e.g., GROUP BY 1, GROUP BY 2)
                    # Note: Quoted column names like GROUP BY "1" come through as UnresolvedAttribute,
                    # while unquoted ordinals like GROUP BY 1 come through as Literal with integer type
                    if expr_class == "Literal":
                        # Check if this is an integer literal (ordinal reference)
                        if hasattr(expr, "dataType") and str(
                            expr.dataType().typeName()
                        ) in ["integer", "long"]:
                            ordinal_pos = expr.value()
                            agg_expressions = as_java_list(rel.aggregateExpressions())

                            # Validate ordinal is in valid range (1-based indexing)
                            if isinstance(ordinal_pos, int) and 1 <= ordinal_pos <= len(
                                agg_expressions
                            ):
                                # Return the expression from the SELECT clause at the ordinal position
                                target_expr = agg_expressions[
                                    ordinal_pos - 1
                                ]  # Convert to 0-based index

                                # If the target expression is an alias, return the underlying expression
                                if (
                                    str(target_expr.getClass().getSimpleName())
                                    == "Alias"
                                ):
                                    return target_expr.child()
                                else:
                                    return target_expr
                            # If ordinal is out of range, let it fall through to generate an error later

                    # Handle named LCA references (existing logic)
                    # This handles cases like GROUP BY "1" (quoted column names)
                    if expr_class != "UnresolvedAttribute":
                        return expr

                    attr_parts = as_java_list(expr.nameParts())
                    if len(attr_parts) == 1:
                        attr_name = str(attr_parts[0])
                        if attr_name in alias_map:
                            # Check if the alias references an aggregate function
                            # If so, don't substitute because you can't GROUP BY an aggregate
                            aliased_expr = alias_map[attr_name]
                            aliased_expr_class = str(
                                aliased_expr.getClass().getSimpleName()
                            )
                            if aliased_expr_class == "UnresolvedFunction":
                                func_name = str(aliased_expr.nameParts().head())
                                if is_aggregate_function(func_name):
                                    return expr
                            return aliased_expr
                        return expr

                    return expr

                group_type = snowflake_proto.Aggregate.GROUP_TYPE_GROUPBY

                grouping_sets: list[snowflake_proto.Aggregate.GroupingSets] = []

                group_expression_list = as_java_list(rel.groupingExpressions())
                for exp in group_expression_list:
                    match str(exp.getClass().getSimpleName()):
                        case "Rollup":
                            group_type = snowflake_proto.Aggregate.GROUP_TYPE_ROLLUP
                        case "Cube":
                            group_type = snowflake_proto.Aggregate.GROUP_TYPE_CUBE
                        case "GroupingSets":
                            if not exp.userGivenGroupByExprs().isEmpty():
                                exception = SnowparkConnectNotImplementedError(
                                    "User-defined group by expressions are not supported"
                                )
                                attach_custom_error_code(
                                    exception, ErrorCodes.UNSUPPORTED_OPERATION
                                )
                                raise exception
                            group_type = (
                                snowflake_proto.Aggregate.GROUP_TYPE_GROUPING_SETS
                            )
                            grouping_sets = [
                                snowflake_proto.Aggregate.GroupingSets(
                                    grouping_set=[
                                        map_logical_plan_expression(e)
                                        for e in as_java_list(grouping_set)
                                    ]
                                )
                                for grouping_set in as_java_list(exp.groupingSets())
                            ]

                if group_type != snowflake_proto.Aggregate.GROUP_TYPE_GROUPBY:
                    if len(group_expression_list) != 1:
                        exception = SnowparkConnectNotImplementedError(
                            "Multiple grouping expressions are not supported"
                        )
                        attach_custom_error_code(
                            exception, ErrorCodes.UNSUPPORTED_OPERATION
                        )
                        raise exception
                    if group_type == snowflake_proto.Aggregate.GROUP_TYPE_GROUPING_SETS:
                        group_expression_list = []  # TODO: exp.userGivenGroupByExprs()?
                    else:
                        group_expression_list = as_java_list(
                            group_expression_list[0].children()
                        )

                grouping_expressions = [
                    map_logical_plan_expression(substitute_lca_in_grouping_expr(e))
                    for e in group_expression_list
                ]

                aggregate_expressions = [
                    map_logical_plan_expression(e)
                    for e in as_java_list(rel.aggregateExpressions())
                ]

                any_proto = Any()
                any_proto.Pack(
                    snowflake_proto.Extension(
                        aggregate=snowflake_proto.Aggregate(
                            input=input,
                            group_type=group_type,
                            grouping_expressions=grouping_expressions,
                            aggregate_expressions=aggregate_expressions,
                            grouping_sets=grouping_sets,
                            having_condition=_having_condition.get(),
                        )
                    )
                )
                proto = relation_proto.Relation(extension=any_proto)
        case "Distinct":
            proto = relation_proto.Relation(
                deduplicate=relation_proto.Deduplicate(
                    input=map_logical_plan_relation(rel.child())
                )
            )
        case "Except":
            proto = relation_proto.Relation(
                set_op=relation_proto.SetOperation(
                    left_input=map_logical_plan_relation(rel.left()),
                    right_input=map_logical_plan_relation(rel.right()),
                    set_op_type=relation_proto.SetOperation.SET_OP_TYPE_EXCEPT,
                    is_all=rel.isAll(),
                )
            )
        case "Filter":
            proto = relation_proto.Relation(
                filter=relation_proto.Filter(
                    input=map_logical_plan_relation(rel.child()),
                    condition=map_logical_plan_expression(rel.condition()),
                )
            )
        case "GlobalLimit":
            # TODO: What's a global limit and what's a local limit?
            proto = map_logical_plan_relation(rel.child())
        case "Intersect":
            proto = relation_proto.Relation(
                set_op=relation_proto.SetOperation(
                    left_input=map_logical_plan_relation(rel.left()),
                    right_input=map_logical_plan_relation(rel.right()),
                    set_op_type=relation_proto.SetOperation.SET_OP_TYPE_INTERSECT,
                    is_all=rel.isAll(),
                )
            )
        case "Join":
            join_type_sql = str(rel.joinType().sql())
            join_type_name = f"JOIN_TYPE_{join_type_sql.replace(' ', '_')}"
            condition = rel.condition()

            left = map_logical_plan_relation(rel.left())
            right = map_logical_plan_relation(rel.right())

            active_hint = _query_block_join_hint.get()
            if active_hint:
                hinted_left = relation_proto.Relation(
                    hint=relation_proto.Hint(input=left, name=active_hint)
                )
                hinted_left.common.plan_id = gen_sql_plan_id()
                left = hinted_left

            join_condition = (
                map_logical_plan_expression(condition.get())
                if condition.isDefined()
                else None
            )

            if "_NATURAL" in join_type_name:
                join_type_name = join_type_name.replace("_NATURAL", "")
                natural_join_base_offset = NATURAL_JOIN_TYPE_BASE
            else:
                natural_join_base_offset = 0

            if "_USING" in join_type_name:
                using_columns = as_java_list(rel.joinType().usingColumns())
                join_type_name = join_type_name.replace("_USING", "")
            else:
                using_columns = []

            proto = relation_proto.Relation(
                join=relation_proto.Join(
                    left=left,
                    right=right,
                    join_condition=join_condition,
                    join_type=getattr(relation_proto.Join.JoinType, join_type_name)
                    + natural_join_base_offset,
                    using_columns=using_columns,
                )
            )
        case "LocalLimit":
            limit_expr = rel.limitExpr()
            limit_expr_class = str(limit_expr.getClass().getSimpleName())

            if limit_expr_class == "Literal":
                limit_dtype = str(limit_expr.dataType().getClass().getSimpleName())
                if limit_dtype not in ("IntegerType$", "ShortType$", "LongType$"):
                    limit_expr_sql = limit_expr.sql()
                    spark_type = limit_dtype.replace("Type$", "").upper()
                    exception = AnalysisException(
                        f'[INVALID_LIMIT_LIKE_EXPRESSION.DATA_TYPE] The limit like expression "{limit_expr_sql}" is invalid. The expression has a "{spark_type}" type, which is not allowed. Please use a value of "INT" type.'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                limit_val = limit_expr.value()
            else:
                expr_proto = map_logical_plan_expression(limit_expr)
                session = snowpark.Session.get_active_session()
                m = ColumnNameMap([], [])
                expr = map_single_column_expression(
                    expr_proto, m, ExpressionTyper.dummy_typer(session)
                )
                limit_val = session.range(1).select(expr[1].col).collect()[0][0]

            if limit_val is None:
                limit_expr_sql = limit_expr.sql()
                exception = AnalysisException(
                    f'[INVALID_LIMIT_LIKE_EXPRESSION.IS_NULL] The limit like expression "{limit_expr_sql}" is invalid. The expression is a NULL value, which is not allowed. Please use a non-null value.'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            proto = relation_proto.Relation(
                limit=relation_proto.Limit(
                    input=map_logical_plan_relation(rel.child()),
                    limit=limit_val,
                )
            )
        case "Offset":
            proto = relation_proto.Relation(
                offset=relation_proto.Offset(
                    input=map_logical_plan_relation(rel.child()),
                    offset=rel.offsetExpr().value(),
                )
            )
        case "OneRowRelation":
            proto = relation_proto.Relation(project=relation_proto.Project())
        case "Pivot":
            pivot_column = map_logical_plan_expression(rel.pivotColumn())
            session = snowpark.Session.get_active_session()
            m = ColumnNameMap([], [])

            pivot_columns = (
                [
                    col
                    for col in pivot_column.unresolved_function.arguments
                    if col.HasField("unresolved_attribute")
                ]
                if pivot_column.HasField("unresolved_function")
                else [pivot_column]
            )

            typer = ExpressionTyper.dummy_typer(session)

            expression_protos: list[expressions_proto.Expression] = []
            expressions: list[TypedColumn] = []
            aliases: list[str] = []

            for pivot_value in as_java_list(rel.pivotValues()):
                expr_proto = map_logical_plan_expression(pivot_value)
                alias, expr = map_single_column_expression(expr_proto, m, typer)

                expression_protos.append(expr_proto)
                expressions.append(expr)
                aliases.append(alias)

            resolved_pivot_values_row = (
                session.range(1)
                .select(*[expr.col for expr in expressions])
                .collect()[0]
            )
            resolved_pivot_values = [value for value in resolved_pivot_values_row]

            pivot_values = []
            for expr_proto, expr, alias, value in zip(
                expression_protos, expressions, aliases, resolved_pivot_values
            ):
                literals_proto = (
                    [
                        _map_value_to_literal_proto(v, expr.typ.fields[i].datatype)
                        for i, v in enumerate(value)
                    ]
                    if isinstance(expr.typ, snowpark.types.StructType)
                    else [_map_value_to_literal_proto(value, expr.typ)]
                )

                if len(pivot_columns) != len(literals_proto):
                    raise AnalysisException(
                        f"[PIVOT_VALUE_DATA_TYPE_MISMATCH] Number of pivot columns ({len(pivot_columns)}) does not match number of values ({len(literals_proto)})"
                    )

                current_pivot_value_proto = (
                    snowflake_proto.Aggregate.Pivot.PivotValue(
                        values=literals_proto, alias=alias
                    )
                    if expr_proto.HasField("alias")
                    else snowflake_proto.Aggregate.Pivot.PivotValue(
                        values=literals_proto
                    )
                )

                pivot_values.append(current_pivot_value_proto)

            aggregate_expressions = [
                map_logical_plan_expression(e) for e in as_java_list(rel.aggregates())
            ]

            any_proto = Any()
            any_proto.Pack(
                snowflake_proto.Extension(
                    aggregate=snowflake_proto.Aggregate(
                        input=map_logical_plan_relation(rel.child()),
                        group_type=relation_proto.Aggregate.GroupType.GROUP_TYPE_PIVOT,
                        aggregate_expressions=aggregate_expressions,
                        having_condition=_having_condition.get(),
                        pivot=snowflake_proto.Aggregate.Pivot(
                            pivot_columns=pivot_columns,
                            pivot_values=pivot_values,
                        ),
                    )
                )
            )
            proto = relation_proto.Relation(extension=any_proto)
        case "PlanWithUnresolvedIdentifier":
            expr_proto = map_logical_plan_expression(rel.identifierExpr())
            session = snowpark.Session.get_active_session()
            m = ColumnNameMap([], [], None)
            expr = map_single_column_expression(
                expr_proto, m, ExpressionTyper.dummy_typer(session)
            )
            value = session.range(1).select(expr[1].col).collect()[0][0]

            proto = relation_proto.Relation(
                read=relation_proto.Read(
                    named_table=relation_proto.Read.NamedTable(
                        unparsed_identifier=value,
                    )
                )
            )
        case "Project":
            with push_sql_scope():
                input = map_logical_plan_relation(rel.child())
                expressions = [
                    map_logical_plan_expression(e)
                    for e in as_java_list(rel.projectList())
                ]
            proto = relation_proto.Relation(
                project=relation_proto.Project(
                    input=input,
                    expressions=expressions,
                )
            )
        case "RelationTimeTravel":
            # ``SELECT * FROM tbl VERSION AS OF <id>`` and
            # ``SELECT * FROM tbl TIMESTAMP AS OF <ts>`` are gated on the
            # Iceberg Spark SQL Extensions being enabled (matches Iceberg's
            # own documented surface). Spark 3.3+'s native parser also
            # produces ``RelationTimeTravel`` for this syntax, but SCOS
            # only meaningfully supports time travel against Iceberg-
            # backed tables, so we keep the customer-visible support
            # contract tight: it lights up exactly when the Iceberg
            # extension class is wired into ``spark.sql.extensions``.
            #
            # SNOW-3471774: the customer-visible message previously
            # implied that the Iceberg extensions PACKAGE has to be pip-
            # installed (``pip install 'snowpark-connect[iceberg]'``).
            # That is misleading — SCOS implements ``VERSION AS OF`` /
            # ``TIMESTAMP AS OF`` natively in ``iceberg_sql_time_travel.py``
            # and does NOT depend on the OSS Iceberg JAR. The only
            # missing piece is the config flag itself. The message now
            # reflects that, and also tells customers exactly how to set
            # the flag (which is a static config — has to be set in the
            # server-side ``spark-defaults.conf`` or via
            # ``SPARK_CONF_<key>`` env, not via ``spark.conf.set()``
            # from the client).
            if not is_iceberg_sql_extensions_enabled():
                raise _relation_time_travel_extensions_disabled_exception()

            base = rel.relation()
            base_class = str(base.getClass().getSimpleName())
            if base_class != "UnresolvedRelation":
                exception = AnalysisException(
                    "Iceberg SQL time travel can only be applied to a base "
                    f"table reference; got {base_class!r}. Reference the "
                    "table directly (e.g. 'SELECT * FROM db.tbl VERSION AS "
                    "OF <id>') rather than a subquery or CTE."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception

            name = str(base.name())

            # Preserve per-part backtick state from the underlying
            # UnresolvedRelation so downstream identifier transformation
            # honors the original quoting — same logic as the standalone
            # ``case "UnresolvedRelation":`` site. Origin substring is the
            # source of truth (regex-over-raw-SQL would be confused by
            # quoted string literals; Felix's PR #4052 review).
            origin_text = _get_original_identifier_from_origin(base)
            if origin_text and "`" in origin_text:
                (
                    origin_parts,
                    origin_flags,
                ) = split_fully_qualified_spark_name_with_quoting(origin_text)
                jvm_parts = tuple(
                    str(p) for p in as_java_list(base.multipartIdentifier())
                )
                if (
                    any(origin_flags)
                    and len(origin_parts) == len(jvm_parts)
                    and tuple(origin_parts) == jvm_parts
                ):
                    record_multipart_backtick_flags(jvm_parts, tuple(origin_flags))

            if not get_is_processing_aliased_relation():
                set_sql_plan_name(name, plan_id)

            (
                snapshot_id,
                as_of_timestamp_millis,
                version_tag,
            ) = resolve_relation_time_travel(rel)

            # Emit the same Read.DataSource proto shape that
            # ``spark.read.format("iceberg").option(...).load(name)``
            # produces, so the existing ``map_read_table`` extractor and
            # ``get_table_from_name`` plumbing handle the rest. Keeping
            # the SQL exit shape identical to the DataFrame exit shape
            # means there is exactly one Snowpark surface call site for
            # Iceberg time travel.
            iceberg_options: dict[str, str] = {}
            if snapshot_id is not None:
                iceberg_options["snapshot-id"] = str(snapshot_id)
            if as_of_timestamp_millis is not None:
                iceberg_options["as-of-timestamp"] = str(as_of_timestamp_millis)
            if version_tag is not None:
                iceberg_options["tag"] = version_tag

            proto = relation_proto.Relation(
                read=relation_proto.Read(
                    data_source=relation_proto.Read.DataSource(
                        format="iceberg",
                        paths=[name],
                        options=iceberg_options,
                    )
                )
            )
        case "Sort":
            # Process the input first
            input_proto = map_logical_plan_relation(rel.child())

            # Check if child is a Project - if so, build an alias map for ORDER BY resolution
            # This handles: SELECT o.date AS order_date ... ORDER BY o.date
            child_class = str(rel.child().getClass().getSimpleName())
            alias_map = {}

            if child_class == "Project":
                # Extract aliases from SELECT clause
                for proj_expr in list(as_java_list(rel.child().projectList())):
                    if str(proj_expr.getClass().getSimpleName()) == "Alias":
                        alias_name = str(proj_expr.name())
                        child_expr = proj_expr.child()

                        # Store mapping from original expression to alias name
                        # Use string representation for matching
                        expr_str = str(child_expr)
                        alias_map[expr_str] = alias_name

                        # Also handle UnresolvedAttribute specifically to get the qualified name
                        if (
                            str(child_expr.getClass().getSimpleName())
                            == "UnresolvedAttribute"
                        ):
                            # Get the qualified name like "o.date"
                            name_parts = list(as_java_list(child_expr.nameParts()))
                            qualified_name = ".".join(str(part) for part in name_parts)
                            if qualified_name not in alias_map:
                                alias_map[qualified_name] = alias_name

            # Process ORDER BY expressions, substituting aliases where needed
            order_list = []
            for order_expr in as_java_list(rel.order()):
                # Get the child expression from the SortOrder
                child_expr = order_expr.child()
                expr_class = str(child_expr.getClass().getSimpleName())

                # Check if this expression matches any aliased expression
                expr_str = str(child_expr)
                substituted = False

                if expr_str in alias_map:
                    # Found a match - substitute with alias reference
                    alias_name = alias_map[expr_str]
                    # Create new UnresolvedAttribute for the alias
                    UnresolvedAttribute = jpype.JClass(
                        "org.apache.spark.sql.catalyst.analysis.UnresolvedAttribute"
                    )
                    new_attr = UnresolvedAttribute.quoted(alias_name)

                    # Create new SortOrder with substituted expression
                    SortOrder = jpype.JClass(
                        "org.apache.spark.sql.catalyst.expressions.SortOrder"
                    )
                    new_order = SortOrder(
                        new_attr,
                        order_expr.direction(),
                        order_expr.nullOrdering(),
                        order_expr.sameOrderExpressions(),
                    )
                    order_list.append(map_logical_plan_expression(new_order).sort_order)
                    substituted = True
                elif expr_class == "UnresolvedAttribute":
                    # Try matching on qualified name
                    name_parts = list(as_java_list(child_expr.nameParts()))
                    qualified_name = ".".join(str(part) for part in name_parts)
                    if qualified_name in alias_map:
                        alias_name = alias_map[qualified_name]
                        UnresolvedAttribute = jpype.JClass(
                            "org.apache.spark.sql.catalyst.analysis.UnresolvedAttribute"
                        )
                        new_attr = UnresolvedAttribute.quoted(alias_name)

                        SortOrder = jpype.JClass(
                            "org.apache.spark.sql.catalyst.expressions.SortOrder"
                        )
                        new_order = SortOrder(
                            new_attr,
                            order_expr.direction(),
                            order_expr.nullOrdering(),
                            order_expr.sameOrderExpressions(),
                        )
                        order_list.append(
                            map_logical_plan_expression(new_order).sort_order
                        )
                        substituted = True

                if not substituted:
                    # No substitution needed - use original
                    order_list.append(
                        map_logical_plan_expression(order_expr).sort_order
                    )

            proto = relation_proto.Relation(
                sort=relation_proto.Sort(
                    input=input_proto,
                    order=order_list,
                )
            )
        case "SubqueryAlias":
            alias = str(rel.alias())
            # If the child is an UnresolvedRelation, we want to preserve the original plan id and save only aliased one
            child_class = str(rel.child().getClass().getSimpleName())
            process_aliased_relation = child_class == "UnresolvedRelation"
            with _push_query_block_hint(None):
                with push_processing_aliased_relation_scope(process_aliased_relation):
                    proto = relation_proto.Relation(
                        subquery_alias=relation_proto.SubqueryAlias(
                            input=map_logical_plan_relation(rel.child()),
                            alias=alias,
                        )
                    )

            # UDTFs do not work when processed with plan id, use alias (see SNOW-3163639)
            if child_class != "UnresolvedTableValuedFunction":
                set_sql_plan_name(alias, plan_id)
        case "Union":
            children = as_java_list(rel.children())
            assert len(children) == 2, len(children)

            proto = relation_proto.Relation(
                set_op=relation_proto.SetOperation(
                    left_input=map_logical_plan_relation(children[0]),
                    right_input=map_logical_plan_relation(children[1]),
                    set_op_type=relation_proto.SetOperation.SET_OP_TYPE_UNION,
                    is_all=True,
                    by_name=rel.byName(),
                    allow_missing_columns=rel.allowMissingCol(),
                )
            )
        case "Unpivot":
            value_column_names = [e for e in as_java_list(rel.valueColumnNames())]
            variable_column_name = rel.variableColumnName()

            # Check for multi-column UNPIVOT which Snowflake doesn't support
            if len(value_column_names) > 1:
                exception = UnsupportedOperationException(
                    f"Multi-column UNPIVOT is not supported. Snowflake SQL does not support unpivoting "
                    f"multiple value columns ({', '.join(value_column_names)}) in a single operation. "
                    f"Workaround: Use separate UNPIVOT operations for each value column and join the results, "
                    f"or restructure your query to unpivot columns individually."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception

            values = []
            values_groups = as_java_list(rel.values().get())

            # Check if we have multi-column groups in the IN clause
            if values_groups and len(as_java_list(values_groups[0])) > 1:
                group_sizes = [len(as_java_list(group)) for group in values_groups]
                exception = UnsupportedOperationException(
                    f"Multi-column UNPIVOT is not supported. Snowflake SQL does not support unpivoting "
                    f"multiple columns together in groups. Found groups with {max(group_sizes)} columns. "
                    f"Workaround: Unpivot each column separately and then join/union the results as needed."
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception

            for e1 in values_groups:
                for e in as_java_list(e1):
                    values.append(map_logical_plan_expression(e))

            # Need to find ids which are not part of values and remaining cols of df
            input_rel = map_logical_plan_relation(rel.child())
            result = map_relation(input_rel)
            input_df: snowpark.DataFrame = result.dataframe
            column_map = result.column_map
            typer = ExpressionTyper(input_df)
            unpivot_spark_names = []
            for v in values:
                spark_name, typed_column = map_single_column_expression(
                    v, column_map, typer
                )
                unpivot_spark_names.append(spark_name)

            id_cols = []
            for column in input_df.columns:
                spark_column = (
                    column_map.get_spark_column_name_from_snowpark_column_name(column)
                )
                if spark_column not in unpivot_spark_names:
                    id_cols.append(
                        expressions_proto.Expression(
                            unresolved_attribute=expressions_proto.Expression.UnresolvedAttribute(
                                unparsed_identifier=spark_column
                            )
                        )
                    )

            proto = relation_proto.Relation(
                unpivot=relation_proto.Unpivot(
                    input=input_rel,
                    ids=id_cols,
                    values=relation_proto.Unpivot.Values(values=values),
                    variable_column_name=variable_column_name,
                    value_column_name=value_column_names[0],
                )
            )
        case "UnresolvedHaving":
            # Store the having condition in context and process the child aggregate
            child_relation = rel.child()
            if str(child_relation.getClass().getSimpleName()) != "Aggregate":
                exception = SnowparkConnectNotImplementedError(
                    "UnresolvedHaving can only be applied to Aggregate relations"
                )
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
                raise exception

            # Store having condition in a context variable for the Aggregate case to pick up
            having_condition = map_logical_plan_expression(rel.havingCondition())

            # Store in thread-local context (similar to how _ctes works)
            token = _having_condition.set(having_condition)

            try:
                # Recursively call map_logical_plan_relation on the child Aggregate
                # The Aggregate case will pick up the having condition from context
                proto = map_logical_plan_relation(child_relation, plan_id)
            finally:
                _having_condition.reset(token)
        case "UnresolvedHint":
            hint_name = str(rel.name())
            params = as_java_list(rel.parameters())
            with _push_query_block_hint(hint_name):
                child_proto = map_logical_plan_relation(rel.child())
            proto = relation_proto.Relation(
                hint=relation_proto.Hint(
                    input=child_proto,
                    name=hint_name,
                    parameters=[map_logical_plan_expression(e) for e in params],
                )
            )
        case "UnresolvedInlineTable":
            names = [str(name) for name in as_java_list(rel.names())]
            rows = (
                relation_proto.Relation(
                    common=relation_proto.RelationCommon(
                        plan_id=gen_sql_plan_id(),
                    ),
                    project=relation_proto.Project(
                        expressions=(
                            expressions_proto.Expression(
                                alias=expressions_proto.Expression.Alias(
                                    expr=map_logical_plan_expression(val),
                                    name=[name],
                                )
                            )
                            for name, val in zip(names, as_java_list(row))
                        ),
                    ),
                )
                for row in as_java_list(rel.rows())
            )

            proto = reduce(
                lambda left, right: relation_proto.Relation(
                    common=relation_proto.RelationCommon(
                        plan_id=gen_sql_plan_id(),
                    ),
                    set_op=relation_proto.SetOperation(
                        left_input=left,
                        right_input=right,
                        set_op_type=relation_proto.SetOperation.SET_OP_TYPE_UNION,
                        is_all=True,
                    ),
                ),
                rows,
            )
        case "UnresolvedRelation":
            name = str(rel.name())

            # If the original identifier text (recovered from the parser's
            # Origin substring — never from a regex over the raw SQL, so we
            # can't be confused by quoted string literals or comments) has
            # any backtick-quoted parts, record per-part flags keyed by the
            # unquoted parts tuple. `_spark_to_snowflake` reads those flags
            # back positionally during identifier rendering. Keyed by the
            # full parts tuple, so a backtick column `foo` and an unquoted
            # table `foo` are tracked independently.
            origin_text = _get_original_identifier_from_origin(rel)
            if origin_text and "`" in origin_text:
                (
                    origin_parts,
                    origin_flags,
                ) = split_fully_qualified_spark_name_with_quoting(origin_text)
                jvm_parts = tuple(
                    str(p) for p in as_java_list(rel.multipartIdentifier())
                )
                if (
                    any(origin_flags)
                    and len(origin_parts) == len(jvm_parts)
                    and tuple(origin_parts) == jvm_parts
                ):
                    record_multipart_backtick_flags(jvm_parts, tuple(origin_flags))

            if not get_is_processing_aliased_relation():
                set_sql_plan_name(name, plan_id)

            cte_proto = _ctes.get().get(name)
            if cte_proto is not None:
                if (
                    session.cte_optimization_enabled
                ):  # do not use get_cte_optimization_enabled() here, it will return None if user has not set it
                    """
                    the optimization serves two purposes:
                    1. avoid re-computing the same logic plan when the CTE is referenced multiple times
                    2. have the same plan id for the CTE such that snowpark CTE optimization can identify the same plan and eliminate the repeated nodes
                    """
                    proto = copy.deepcopy(cte_proto)
                else:
                    # The name corresponds to a `WITH` alias rather than a table.
                    # TODO: We currently evaluate the query each time its alias is used;
                    # we should eventually start using `WITH` in Snowflake SQL.
                    # Each CTE reference should get completely fresh evaluation to prevent ambiguity
                    # when the same CTE is joined multiple times. Instead of reusing the same cte_proto,
                    # re-evaluate the CTE definition to get fresh column identifiers.

                    # Re-evaluate the CTE definition to get fresh column identifiers
                    cte_definition = _cte_definitions.get().get(name)
                    if cte_definition is not None:
                        # Get the original column names for consistency across CTE references
                        original_container = map_relation(cte_proto)
                        original_spark_columns = (
                            original_container.column_map.get_spark_columns()
                        )

                        # Re-evaluate the CTE definition with a fresh plan_id
                        # Clear HAVING condition to prevent leakage from outer CTEs
                        saved_having = _having_condition.get()
                        _having_condition.set(None)
                        try:
                            fresh_plan_id = gen_sql_plan_id()
                            fresh_cte_proto = map_logical_plan_relation(
                                cte_definition, fresh_plan_id
                            )
                        finally:
                            _having_condition.set(saved_having)

                        # Use SubqueryColumnAliases to ensure consistent column names across CTE references
                        # This is crucial for CTEs that reference other CTEs
                        any_proto = Any()
                        any_proto.Pack(
                            snowflake_proto.Extension(
                                subquery_column_aliases=snowflake_proto.SubqueryColumnAliases(
                                    input=fresh_cte_proto,
                                    aliases=original_spark_columns,
                                )
                            )
                        )
                        column_aliased_proto = relation_proto.Relation(
                            extension=any_proto
                        )
                        column_aliased_proto.common.plan_id = gen_sql_plan_id()

                        # Wrap in SubqueryAlias with the CTE name
                        proto = relation_proto.Relation(
                            subquery_alias=relation_proto.SubqueryAlias(
                                input=column_aliased_proto,
                                alias=name,
                            )
                        )
                        proto.common.plan_id = gen_sql_plan_id()
                    else:
                        # Fallback to stored CTE if definition not found
                        proto = cte_proto
            else:
                # Iceberg branch/tag suffix: when extensions are on, a trailing
                # branch_<name> or tag_<name> segment takes precedence over a
                # literal table with that name (no catalog lookup yet).
                branch_tag_suffix = (
                    try_parse_iceberg_branch_tag_suffix(name)
                    if is_iceberg_sql_extensions_enabled()
                    else None
                )
                if branch_tag_suffix is not None:
                    base_name, iceberg_options = branch_tag_suffix
                    proto = relation_proto.Relation(
                        read=relation_proto.Read(
                            data_source=relation_proto.Read.DataSource(
                                format="iceberg",
                                paths=[base_name],
                                options=iceberg_options,
                            )
                        )
                    )
                else:
                    tmp_views = _get_current_temp_objects()
                    current_schema = session.connection.schema
                    from_table = (
                        CURRENT_CATALOG_NAME,
                        current_schema,
                        name,
                    )
                    if from_table in tmp_views:
                        _accessing_temp_object.set(True)
                    proto = relation_proto.Relation(
                        read=relation_proto.Read(
                            named_table=relation_proto.Read.NamedTable(
                                unparsed_identifier=name,
                            )
                        )
                    )
        case "UnresolvedSubqueryColumnAliases":
            child = map_logical_plan_relation(rel.child())
            aliases = [str(a) for a in as_java_list(rel.outputColumnNames())]
            any_proto = Any()
            any_proto.Pack(
                snowflake_proto.Extension(
                    subquery_column_aliases=snowflake_proto.SubqueryColumnAliases(
                        input=child,
                        aliases=aliases,
                    )
                )
            )
            proto = relation_proto.Relation(extension=any_proto)
        case "UnresolvedTableValuedFunction":
            name = ".".join(str(part) for part in as_java_list(rel.name())).lower()
            args = [
                map_logical_plan_expression(exp)
                for exp in as_java_list(rel.functionArgs())
            ]

            match name:
                case "range":
                    m = ColumnNameMap([], [], None)
                    session = snowpark.Session.get_active_session()
                    args = (
                        session.range(1)
                        .select(
                            [
                                map_single_column_expression(arg, m, None)[1].col
                                for arg in args
                            ]
                        )
                        .collect()[0]
                    )

                    def _parse_value(argument, place):
                        if isinstance(argument, (Decimal, float)):
                            return int(argument)
                        elif isinstance(argument, str):
                            try:
                                value = float(argument)
                                if value < 0:
                                    return math.ceil(value)
                                return math.floor(float(argument))
                            except ValueError:
                                raise AnalysisException(
                                    f'[UNEXPECTED_INPUT_TYPE] Parameter {place} of function `range` requires the "BIGINT" type, however "{argument}" has the type "STRING"'
                                )
                        return argument

                    start, step = 0, 1
                    match args:
                        case [_]:
                            [end] = args
                            end = _parse_value(end, 1)
                        case [_, _]:
                            [start, end] = args
                            start = _parse_value(start, 1)
                            end = _parse_value(end, 2)
                        case [_, _, _]:
                            [start, end, step] = args
                            start = _parse_value(start, 1)
                            end = _parse_value(end, 2)
                            step = _parse_value(step, 3)

                    proto = relation_proto.Relation(
                        range=relation_proto.Range(
                            start=start,
                            end=end,
                            step=step,
                        )
                    )
                case udtf_name if get_spark_session_cache().udtfs.has(udtf_name):
                    # TODO: Table arguments are now expressions, too, so we shouldn't need to handle them here;
                    # instead, handle SubqueryExpression.SUBQUERY_TYPE_TABLE_ARG in relation.map_extension.
                    table_args = []
                    non_table_args = []
                    for i, arg in enumerate(args):
                        extension = snowflake_exp_proto.ExpExtension()
                        if (
                            arg.extension.Unpack(extension)
                            and extension.subquery_expression.subquery_type
                            == snowflake_exp_proto.SubqueryExpression.SUBQUERY_TYPE_TABLE_ARG
                        ):
                            table_args.append(
                                snowflake_proto.TableArgumentInfo(
                                    table_argument=extension.subquery_expression.input,
                                    table_argument_idx=i,
                                )
                            )
                        else:
                            non_table_args.append(arg)

                    if table_args:
                        any_proto = Any()
                        any_proto.Pack(
                            snowflake_proto.Extension(
                                udtf_with_table_arguments=snowflake_proto.UDTFWithTableArguments(
                                    function_name=name,
                                    arguments=non_table_args,
                                    table_arguments=table_args,
                                )
                            )
                        )
                        proto = relation_proto.Relation(extension=any_proto)
                    else:
                        proto = relation_proto.Relation(
                            project=relation_proto.Project(
                                expressions=[
                                    expressions_proto.Expression(
                                        unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                                            function_name=name,
                                            arguments=args,
                                        )
                                    )
                                ],
                            ),
                        )
                case other:
                    proto = relation_proto.Relation(
                        project=relation_proto.Project(
                            expressions=[
                                expressions_proto.Expression(
                                    unresolved_function=expressions_proto.Expression.UnresolvedFunction(
                                        function_name=name,
                                        arguments=args,
                                    )
                                )
                            ],
                        ),
                    )
        case "UnresolvedWith":
            with _with_cte_scope(rel.cteRelations()):
                proto = map_logical_plan_relation(rel.child())
        case "LateralJoin":
            left = map_logical_plan_relation(rel.left())
            right = map_logical_plan_relation(rel.right().plan())
            any_proto = Any()
            any_proto.Pack(
                snowflake_proto.Extension(
                    lateral_join=snowflake_proto.LateralJoin(
                        left=left,
                        right=right,
                    )
                )
            )
            proto = relation_proto.Relation(extension=any_proto)
        case "WithWindowDefinition":
            map_obj = as_java_map(rel.windowDefinitions())
            with _push_window_specs_scope():
                for key, window_spec in map_obj.items():
                    _window_specs.get()[key] = window_spec
                proto = map_logical_plan_relation(rel.child())
        case "Generate":
            child_class = str(rel.child().getClass().getSimpleName())

            if child_class == "SubqueryAlias":
                alias = str(rel.child().alias())

                existing_plan_id = get_sql_plan(alias)

                # Process the inner child with the determined plan_id
                inner_child = map_logical_plan_relation(
                    rel.child().child(), plan_id=existing_plan_id
                )
                input_relation = relation_proto.Relation(
                    subquery_alias=relation_proto.SubqueryAlias(
                        input=inner_child,
                        alias=alias,
                    )
                )
            else:
                input_relation = map_logical_plan_relation(rel.child())
            generator_output_list = as_java_list(rel.generatorOutput())
            qualifier = rel.qualifier().get() if rel.qualifier().isDefined() else None
            function_name = rel.generator().name().toString()
            func_arguments = [
                map_logical_plan_expression(e)
                for e in list(as_java_list(rel.generator().children()))
            ]
            unresolved_fun_proto = expressions_proto.Expression.UnresolvedFunction(
                function_name=function_name, arguments=func_arguments
            )

            aliased_proto = expressions_proto.Expression(
                unresolved_function=unresolved_fun_proto,
            )
            if generator_output_list.size() > 0:
                aliased_proto = expressions_proto.Expression(
                    alias=expressions_proto.Expression.Alias(
                        expr=aliased_proto,
                        name=[attribute.name() for attribute in generator_output_list],
                    )
                )

            # TODO: Fix the bug in snowpark where if we select posexplode with *, it would return columns
            # generated by posexplode two times plus all the other columns
            # Ideal way should have been to do this
            # unresolved_star_expr = expressions_proto.Expression(
            #     unresolved_attribute=expressions_proto.Expression.UnresolvedAttribute(
            #         unparsed_identifier="*",
            #     )
            # )
            # generator_dataframe_proto.project.expressions.append(
            #     unresolved_star_expr
            # )

            # This is a workaround to fix the bug in snowpark where if we select posexplode with *, it would return wrong columns
            input_container = map_relation(input_relation)
            spark_columns = input_container.column_map.get_spark_columns()
            column_expressions = [
                expressions_proto.Expression(
                    unresolved_attribute=expressions_proto.Expression.UnresolvedAttribute(
                        unparsed_identifier=spark_column
                    )
                )
                for spark_column in spark_columns
            ]

            generator_dataframe_proto = relation_proto.Relation(
                project=relation_proto.Project(
                    input=input_relation,
                    expressions=[aliased_proto, *column_expressions],
                )
            )
            if qualifier is not None and qualifier.lower() != "as":
                # SNOW-2845305: Spark's `LATERAL VIEW <fn>(args) <alias>`
                # qualifies the generator's output columns with `<alias>` while
                # leaving the carried child columns' qualifiers untouched. The
                # projection above places the generator outputs first, then the
                # carried children — so we wrap it in a QualifyLeadingColumns
                # extension that adds `<alias>` to every column except the
                # trailing `len(column_expressions)` carried (unqualified)
                # columns. Previously, we wrapped generator outputs in
                # `struct(col) AS <alias>`, which caused Snowflake to return
                # them as VARIANT/OBJECT and erased the original element type
                # (e.g., IntegerType -> StringType), breaking downstream
                # references. Applying the alias as a pure qualifier preserves
                # the underlying types.
                any_proto = Any()
                any_proto.Pack(
                    snowflake_proto.Extension(
                        qualify_leading_columns=snowflake_proto.QualifyLeadingColumns(
                            input=generator_dataframe_proto,
                            num_trailing_unqualified_columns=len(column_expressions),
                            qualifier=qualifier,
                        )
                    )
                )
                generator_dataframe_proto = relation_proto.Relation(extension=any_proto)
            proto = generator_dataframe_proto
        case other:
            exception = SnowparkConnectNotImplementedError(
                f"Unimplemented relation: {other}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

    proto.common.plan_id = plan_id

    return proto


def _get_relation_identifier(name_obj) -> str:
    # IDENTIFIER(<table_name>), or IDENTIFIER(<method name>)
    expr_proto = map_logical_plan_expression(name_obj.identifierExpr())
    session = snowpark.Session.get_active_session()
    m = ColumnNameMap([], [], None)
    expr = map_single_column_expression(
        expr_proto, m, ExpressionTyper.dummy_typer(session)
    )
    return spark_to_sf_single_id(session.range(1).select(expr[1].col).collect()[0][0])


def _create_temp_view_name(parts) -> str:
    return ".".join(
        quote_name_without_upper_casing(str(part)) for part in as_java_list(parts)
    )


def get_relation_identifier_name_without_uppercasing(
    name_obj, is_multi_part: bool = False
) -> str:
    if name_obj.getClass().getSimpleName() in (
        "PlanWithUnresolvedIdentifier",
        "ExpressionWithUnresolvedIdentifier",
    ):
        return _get_relation_identifier(name_obj)
    elif is_multi_part:
        try:
            # Try multipartIdentifier first for full catalog.database.table
            return _create_temp_view_name(name_obj.multipartIdentifier())
        except AttributeError:
            # Fallback to nameParts if multipartIdentifier not available
            return _create_temp_view_name(name_obj.nameParts())
    else:
        return _create_temp_view_name(name_obj.nameParts())


def get_relation_identifier_name(name_obj, is_multi_part: bool = False) -> str:
    if name_obj.getClass().getSimpleName() in (
        "PlanWithUnresolvedIdentifier",
        "ExpressionWithUnresolvedIdentifier",
    ):
        return _get_relation_identifier(name_obj)
    else:
        if is_multi_part:
            try:
                # Try multipartIdentifier first for full catalog.database.table
                name = _spark_to_snowflake(name_obj.multipartIdentifier())
            except AttributeError:
                # Fallback to nameParts if multipartIdentifier not available
                name = _spark_to_snowflake(name_obj.nameParts())
        else:
            name = _spark_to_snowflake(name_obj.nameParts())

    return name


def _convert_spark_pattern_to_regex(pattern: str) -> str:
    """
    Convert Spark LIKE pattern to Python regex pattern.

    In Spark LIKE patterns:
    - '*' matches 0 or more characters (equivalent to '.*' in regex)
    - '|' is used to separate multiple patterns (equivalent to '|' in regex)
    - Everything else works like regular regex patterns

    Args:
        pattern: Spark LIKE pattern string

    Returns:
        Python regex pattern string
    """
    if not pattern:
        return ""

    # Split by '|' to handle multiple patterns
    patterns = pattern.split("|")
    regex_patterns = []

    for p in patterns:
        p = p.strip()
        # Replace * with .* for wildcard matching, but preserve other regex characters
        # We need to be careful to only replace standalone * not part of other patterns
        converted = p.replace("*", ".*")
        regex_patterns.append(converted)

    # Join patterns with | for OR matching
    return "|".join(regex_patterns)


def _filter_tables_by_pattern(tables: list, pattern: str) -> list:
    """
    Filter table list by Spark LIKE pattern.

    Args:
        tables: List of table rows from Snowflake SHOW TABLES
        pattern: Spark LIKE pattern

    Returns:
        Filtered list of tables matching the pattern
    """
    if not pattern or not tables:
        return tables

    regex_pattern = _convert_spark_pattern_to_regex(pattern)
    if not regex_pattern:
        return tables

    # Compile regex for case-insensitive matching (as per Spark docs)
    compiled_regex = re.compile(regex_pattern, re.IGNORECASE)

    filtered_tables = []
    for table in tables:
        # Table name is typically the second column in SHOW TABLES output
        table_name = table[1] if len(table) > 1 else str(table[0])
        if compiled_regex.search(table_name):
            filtered_tables.append(table)

    return filtered_tables


def _enrich_show_tables_with_partition_spec(
    rows: list, namespace: str | None, session
) -> pandas.DataFrame:
    """
    Enrich SHOW TABLES rows with a partition_specs column.
    For Iceberg tables, fetches partition specs via SHOW ICEBERG TABLES.
    Non-Iceberg tables get None.
    """
    df = pandas.DataFrame(rows)

    has_iceberg = "is_iceberg" in df.columns and (df["is_iceberg"] == "Y").any()
    if not has_iceberg:
        df["partition_specs"] = None
        return df

    try:
        if namespace:
            iceberg_rows = session.sql(f"SHOW ICEBERG TABLES IN {namespace}").collect()
        else:
            iceberg_rows = session.sql("SHOW ICEBERG TABLES").collect()
    except Exception:
        df["partition_specs"] = None
        return df

    spec_lookup: dict[str, str | None] = {}
    for row in iceberg_rows:
        table_name = row["name"]
        spec_lookup[table_name] = row["partition_specs"]

    df["partition_specs"] = df["name"].map(lambda n: spec_lookup.get(n))
    return df


def _extract_table_location(logical_plan) -> str | None:
    """Read ``tableSpec().location()`` off the logical plan; ``None`` when unset.

    ``location`` is declared ``Option[String]`` on ``TableSpecBase`` (never
    null), so we read the ``Option`` shape directly rather than guarding
    accessor errors. See Spark v3.5.3 (the version pinned via
    ``snowpark-connect-deps``):
    https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/plans/logical/v2Commands.scala#L1406-L1413
    """
    location = logical_plan.tableSpec().location()
    return str(location.get()) if location.isDefined() else None


def _extract_table_provider(logical_plan: typing.Any) -> str:
    """Return Spark's table provider from ``tableSpec().provider()``, lower-cased.

    ``provider`` is declared ``Option[String]`` on ``TableSpecBase``
    (``Some("iceberg")`` for ``USING iceberg``; ``None`` when no ``USING``
    clause). Absent provider degrades to ``"default"`` so the non-Iceberg
    path is preserved. See Spark v3.5.3 (the version pinned via
    ``snowpark-connect-deps``):
    https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/plans/logical/v2Commands.scala#L1406-L1413
    """
    provider = logical_plan.tableSpec().provider()
    return str(provider.get()).lower() if provider.isDefined() else "default"


def _extract_identity_partition_columns(logical_plan: typing.Any) -> list[str]:
    """Read identity partition columns off a ``CreateTable`` / ``ReplaceTable``
    logical plan (``PARTITIONED BY (col1, col2)``).

    Spark exposes partition specs as a ``Seq[Transform]``
    (``org.apache.spark.sql.connector.expressions.Transform``). For the literal
    column-name form these are ``IdentityTransform``s whose single reference's
    ``fieldNames()[0]`` is the column name. Non-identity transforms
    (``years()``, ``months()``, ``days()``, ``hours()``, ``bucket()``,
    ``truncate()``) are dropped from this clause — they need JVM-side
    Spark→Snowflake transform mapping and are tracked outside SNOW-3589401.

    Both call sites pass a V2 create-table plan, so ``partitioning()`` and the
    ``Transform`` / ``NamedReference`` accessors are guaranteed by Spark's
    stable connector API — we pattern-match on their shape rather than
    defensively swallowing errors.
    """
    partitioning = logical_plan.partitioning()
    if partitioning is None:
        return []
    # ``partitioning()`` is a Scala ``Seq`` at runtime; ``seqAsJavaList`` makes
    # it jpype-iterable. Unit tests pass a plain Python ``list``, which is
    # already iterable — only the JVM ``Seq`` shape needs converting.
    transforms = (
        partitioning if isinstance(partitioning, list) else as_java_list(partitioning)
    )
    cols: list[str] = []
    for transform in transforms:
        transform_name = str(transform.name())
        if transform_name != "identity":
            # WARN (not debug) so customers using SQL `PARTITIONED BY
            # (years(ts))` / `bucket(N, c)` etc. on a CLD iceberg target get
            # a visible signal that the transform was dropped from the
            # resulting DDL — otherwise the silent drop is only noticed at
            # write time. AnalysisException would be too aggressive.
            logger.warning(
                "Dropping non-identity partition transform %r from "
                "CREATE ICEBERG TABLE DDL on CLD target — only identity "
                "transforms are emitted today (years / months / days / "
                "hours / bucket / truncate are tracked outside SNOW-3589401)",
                transform_name,
            )
            continue
        references = transform.references()
        if not references or len(references) == 0:
            continue
        field_names = references[0].fieldNames()
        if not field_names or len(field_names) == 0:
            continue
        cols.append(str(field_names[0]))
    return cols


def _extract_table_properties(logical_plan: typing.Any) -> dict[str, str]:
    """Read ``TBLPROPERTIES (...)`` off a ``CreateTable`` / ``ReplaceTable``
    logical plan as a plain Python ``dict``.

    ``properties`` is declared ``Map[String, String]`` on ``TableSpecBase``
    (never null; empty when there are no properties). Via jpype it surfaces
    as a Scala ``Map`` whose ``iterator()`` yields ``Tuple2[String, String]``
    (``_1()`` / ``_2()`` = key / value) — we read that shape directly. See
    Spark v3.5.3 (the version pinned via ``snowpark-connect-deps``):
    https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/plans/logical/v2Commands.scala#L1406-L1413

    Used by :func:`_build_create_iceberg_table_clauses` to map Spark
    Iceberg's ``format-version`` table property to Snowflake's
    ``ICEBERG_VERSION = N`` clause (SNOW-3589401).
    """
    props = logical_plan.tableSpec().properties()
    result: dict[str, str] = {}
    props_iterator = props.iterator()
    while props_iterator.hasNext():
        pair = props_iterator.next()
        result[str(pair._1())] = str(pair._2())
    return result


def _build_create_iceberg_table_clauses(
    data_source: str,
    logical_plan,
) -> str:
    """Build the post-column DDL clauses for ``CREATE ICEBERG TABLE``.

    Threads five optional clauses, in the order Snowflake's
    `CREATE ICEBERG TABLE <https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table>`_
    grammar lays them out — so that customer-facing DDL stays stable and
    diff-friendly:

    1. ``PARTITION BY (col1, col2)`` — from Spark's
       ``PARTITIONED BY (col)`` clause. Identity transforms only; see
       :func:`_extract_identity_partition_columns`.
    2. ``ICEBERG_VERSION = N`` — from Spark Iceberg's
       ``TBLPROPERTIES ('format-version'='2')``. Validated via
       :func:`_extract_iceberg_format_version` (must be ``1``, ``2``,
       or ``3``; invalid input raises ``AnalysisException`` at this
       boundary, not deep inside Snowflake's DDL parser).
    3. ``EXTERNAL_VOLUME = '...'`` — for non-CLD managed Iceberg only, from
       ``snowpark.connect.iceberg.external_volume``.
    4. ``CATALOG = 'SNOWFLAKE'`` — for non-CLD managed Iceberg only. Horizon
       exposes Snowflake-managed Iceberg through REST, but the underlying
       Snowflake catalog is still ``SNOWFLAKE``.
    5. ``BASE_LOCATION = '...'`` — from Spark's ``LOCATION`` clause or
       the ``snowpark.connect.iceberg.base_location`` session config.
       SCOS does **not** synthesize a default — see
       :func:`_build_base_location_clause`. SNOW-3471787.

    Returns the fragment with a trailing space so the call site can
    concatenate without managing whitespace, or ``""`` when nothing
    applies.
    """
    if data_source != "iceberg":
        return ""

    parts: list[str] = []
    is_cld = is_in_cld_context()

    partition_cols = _extract_identity_partition_columns(logical_plan)
    if partition_cols:
        partition_ids = ", ".join(
            spark_to_sf_single_id(unquote_if_quoted(c), is_column=True)
            for c in partition_cols
        )
        parts.append(f"PARTITION BY ({partition_ids})")

    properties = _extract_table_properties(logical_plan)
    iceberg_version = _extract_iceberg_format_version(properties)

    if not is_cld:
        external_volume = _build_managed_iceberg_external_volume_clause()
        if external_volume:
            parts.append(external_volume)

    if iceberg_version is not None:
        parts.append(f"ICEBERG_VERSION = {iceberg_version}")

    if not is_cld:
        # Spark SQL DDL does not route through Snowpark's ``iceberg_config``
        # write path, so add the managed-Iceberg catalog clause explicitly.
        # Horizon exposes these same Snowflake-managed Iceberg tables via REST,
        # but the underlying Snowflake table catalog is still SNOWFLAKE.
        parts.append("CATALOG = 'SNOWFLAKE'")

    explicit = _extract_table_location(logical_plan)
    base_location_clause = _build_base_location_clause(explicit=explicit)
    if base_location_clause:
        parts.append(base_location_clause)

    if not parts:
        return ""
    return " ".join(parts) + " "


def _build_managed_iceberg_external_volume_clause() -> str:
    value = sessions_config.get(get_spark_session_id(), {}).get(
        "snowpark.connect.iceberg.external_volume"
    )
    if not value:
        return ""
    escaped = str(value).strip().replace("'", "''")
    if not escaped:
        return ""
    return f"EXTERNAL_VOLUME = '{escaped}'"


def _resolve_managed_iceberg_base_location_for_sql(
    logical_plan: typing.Any,
) -> str | None:
    explicit_location = _extract_table_location(logical_plan)
    if explicit_location:
        return explicit_location

    value = sessions_config.get(get_spark_session_id(), {}).get(
        "snowpark.connect.iceberg.base_location"
    )
    if not value:
        return None
    stripped = str(value).strip()
    return stripped or None


def _build_managed_iceberg_config_for_sql(
    logical_plan: typing.Any,
) -> dict[str, typing.Any]:
    config: dict[str, typing.Any] = {"catalog": "SNOWFLAKE"}
    external_volume = sessions_config.get(get_spark_session_id(), {}).get(
        "snowpark.connect.iceberg.external_volume"
    )
    if external_volume:
        config["external_volume"] = external_volume

    base_location = _resolve_managed_iceberg_base_location_for_sql(logical_plan)
    if base_location:
        config["base_location"] = base_location

    properties = _extract_table_properties(logical_plan)
    iceberg_version = _extract_iceberg_format_version(properties)
    if iceberg_version is not None:
        config["iceberg_version"] = iceberg_version

    partition_cols = _extract_identity_partition_columns(logical_plan)
    if partition_cols:
        config["partition_by"] = [
            spark_to_sf_single_id(unquote_if_quoted(c), is_column=True)
            for c in partition_cols
        ]

    return config
