#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Pick the FLATTEN input for posexplode / posexplode_outer over an array.

FLATTEN skips undefined array slots, and SQL-built arrays (ARRAY_CONSTRUCT,
F.array, createDataFrame) store a NULL element as an undefined slot. So by
default the array is rebuilt with TRANSFORM, turning each NULL into a JSON null
that FLATTEN keeps. That rebuild copies the whole array and fails once the
array is over the 128 MiB value cap (SNOW-4261008).

An NSS JSON scan stores a NULL element as a defined NULL_VALUE instead, which
FLATTEN keeps as is. When ``snowpark.connect.nss.posexplodeWithoutTransform`` is
on, an argument that is a plain field path into a column whose value is still
unmodified NSS scan data is flattened without the rebuild. Anything else keeps
TRANSFORM.

Which columns hold NSS data is tracked per column map in
``ColumnNameMap.nss_data_snowpark_columns``: the NSS read sets it, and
projections and withColumn recompute it for their outputs from the expressions
that produce them (``nss_data_output_flags``). It is never inherited by name,
because withColumn keeps the Snowpark name of a column it replaces.
"""

from __future__ import annotations

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from pyspark.errors.exceptions.base import AnalysisException

from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.utils.identifiers import (
    split_fully_qualified_spark_name,
)

_ARRAY_GENERATORS = {
    "explode": 1,
    "explode_outer": 1,
    "posexplode": 2,
    "posexplode_outer": 2,
}


def null_preserving_flatten_input_sql(arg_sql: str) -> str:
    return (
        f"transform({arg_sql}, x -> iff(x is null, parse_json('null'), to_variant(x)))"
    )


def is_nss_value_path(
    expr: expressions_proto.Expression, column_mapping: ColumnNameMap
) -> bool:
    """True when ``expr`` reads a value straight out of an NSS data column."""
    if not column_mapping.nss_data_snowpark_columns:
        return False
    parts = _field_path_parts(expr)
    if not parts:
        return False
    snowpark_name = _resolve_root_column(parts, column_mapping)
    return snowpark_name in column_mapping.nss_data_snowpark_columns


def nss_data_output_flags(
    expr: expressions_proto.Expression,
    input_mapping: ColumnNameMap,
    result_snowpark_columns: list[str],
) -> list[bool]:
    """For one projected expression, whether each of its output columns is NSS data.

    ``result_snowpark_columns`` are the expression's output column names as
    produced from ``input_mapping`` (before any final renaming).
    """
    n = len(result_snowpark_columns)
    if not input_mapping.nss_data_snowpark_columns or n == 0:
        return [False] * n
    kind = expr.WhichOneof("expr_type")
    if kind == "unresolved_star":
        star = expr.unresolved_star
        if star.HasField("unparsed_target"):
            target = star.unparsed_target
            if target.endswith(".*") and is_nss_value_path(
                _attribute(target[: -len(".*")]), input_mapping
            ):
                return [True] * n
        return [
            name in input_mapping.nss_data_snowpark_columns
            for name in result_snowpark_columns
        ]
    generator = expr.alias.expr if kind == "alias" else expr
    if generator.WhichOneof("expr_type") == "unresolved_function":
        fn = generator.unresolved_function
        width = _ARRAY_GENERATORS.get(fn.function_name.lower())
        # Array generators only: a map generator has one more output column.
        if width == n and len(fn.arguments) == 1:
            element_is_nss = is_nss_value_path(fn.arguments[0], input_mapping)
            return [False] * (n - 1) + [element_is_nss]
        return [False] * n
    if n == 1:
        return [is_nss_value_path(expr, input_mapping)]
    return [False] * n


def _attribute(name: str) -> expressions_proto.Expression:
    expr = expressions_proto.Expression()
    expr.unresolved_attribute.unparsed_identifier = name
    return expr


def _field_path_parts(expr: expressions_proto.Expression) -> list[str] | None:
    """Name parts of ``col``, ``col.a.b``, ``col["a"]``; None for anything that
    computes a new value."""
    kind = expr.WhichOneof("expr_type")
    if kind == "alias":
        return _field_path_parts(expr.alias.expr)
    if kind == "unresolved_extract_value":
        extraction = expr.unresolved_extract_value.extraction
        if (
            extraction.WhichOneof("expr_type") != "literal"
            or extraction.literal.WhichOneof("literal_type") != "string"
        ):
            return None
        child_parts = _field_path_parts(expr.unresolved_extract_value.child)
        if child_parts is None:
            return None
        return [*child_parts, extraction.literal.string]
    if kind == "unresolved_attribute":
        return (
            split_fully_qualified_spark_name(
                expr.unresolved_attribute.unparsed_identifier
            )
            or None
        )
    # Any other expression (function call, cast, F.array, UDF, ...) builds a new
    # value, and Snowflake decides how its NULL elements are stored: ARRAY_CONSTRUCT
    # writes an undefined slot, and a structured cast turns a defined NULL_VALUE
    # into one. FLATTEN skips undefined slots, so skipping TRANSFORM for such a
    # value would drop (pos, null) rows. Only a plain path keeps NSS's encoding.
    return None


def _resolve_root_column(parts: list[str], column_mapping: ColumnNameMap) -> str | None:
    # The first part may be a DataFrame alias, so also try "<alias>.<column>".
    for width in (1, 2):
        if len(parts) < width:
            break
        try:
            snowpark_name = (
                column_mapping.get_snowpark_column_name_from_spark_column_name(
                    ".".join(parts[:width]), allow_non_exists=True
                )
            )
        except AnalysisException:
            return None
        if snowpark_name is not None:
            return snowpark_name
    return None
