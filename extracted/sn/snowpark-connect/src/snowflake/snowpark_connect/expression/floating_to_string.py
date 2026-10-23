#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Spark float/double text (SNOW-4193976).

Spark's cast to string uses ``Float.toString`` / ``Double.toString``.
``format_string`` / ``printf`` ``%s`` does too, via ``java.util.Formatter``.
Snowflake ``TO_VARCHAR`` does not. The JDK handlers live in
``JavaFloatingFormatUdfs``; the CSV writer can call the same class.
"""

from __future__ import annotations

import math

from snowflake.snowpark import Column, functions as snowpark_fn
from snowflake.snowpark._internal.analyzer.expression import Literal
from snowflake.snowpark.types import DataType, DoubleType, FloatType, StringType
from snowflake.snowpark_connect.config import is_cast_spark_floating_to_string_enabled
from snowflake.snowpark_connect.utils.context import is_lambda_being_resolved
from snowflake.snowpark_connect.utils.udf_cache import register_cached_java_udf

_DOUBLE_HANDLER = (
    "com.snowflake.snowpark_connect.udfs.JavaFloatingFormatUdfs.double_to_string"
)
_FLOAT_HANDLER = (
    "com.snowflake.snowpark_connect.udfs.JavaFloatingFormatUdfs.float_to_string"
)

# Python ``%`` conversions that consume a value argument. ``%s`` is rewritten
# to Java toString before the Python UDF sees it. Anything else is left alone.
_PYTHON_CONVERSIONS = set("diouxXeEfFgGcrsa")


def legacy_floating_to_string(col: Column) -> Column:
    """BASE text: ``TO_VARCHAR``, plus ``.0`` when ``col = floor(col)``.

    Snowflake treats NaN, infinity, and signed zero as equal to ``floor`` of
    themselves, so this arm also rewrites those strings. Null stays null
    because ``IFF`` of null takes the else branch, which is itself null.
    """
    str_val = col.cast(StringType())
    return snowpark_fn.iff(
        col == snowpark_fn.floor(col),
        snowpark_fn.concat(snowpark_fn.floor(col), snowpark_fn.lit(".0")),
        str_val,
    )


def spark_floating_to_string(
    col: Column, datatype: DataType, *, in_lambda: bool = False
) -> Column:
    """Stringify ``col`` the way Spark casts that floating type.

    Flag off returns :func:`legacy_floating_to_string`. A Spark float that
    Snowflake has already widened to double is narrowed again so the handler
    matches ``Float.toString``.

    ``in_lambda`` is set when this expression is pasted into ``TRANSFORM`` or
    ``MAP_ENTRIES``. Snowflake rejects a Java UDF there (error 001157), and a
    SQL UDF whose body only calls that handler is rejected the same way, so
    those elements stay on the floor rule.
    """
    if in_lambda or not is_cast_spark_floating_to_string_enabled():
        return legacy_floating_to_string(col)
    # A numeric token -0.0 is positive zero by the time a Java UDF sees it.
    # The sign bit survives a string cast, which is what the column path uses.
    if _is_negative_zero(getattr(col, "_expression", None)):
        return snowpark_fn.lit("-0.0")
    handler = _FLOAT_HANDLER if isinstance(datatype, FloatType) else _DOUBLE_HANDLER
    render = register_cached_java_udf(handler, ["DOUBLE"], "STRING")
    return render(col)


def format_string_floating_arguments(
    fmt: Column,
    arguments: list[Column] | None,
    types: list[DataType],
) -> list[Column]:
    """Replace float/double arguments consumed by a literal ``%s``.

    Other conversions stay numeric so ``%f`` still reaches the Python
    formatter. A non-literal format, or a pattern this scanner does not
    understand, is returned unchanged. ``None`` is not a caller today
    (``format_string`` passes ``snowpark_args[1:]``), and it returns ``[]``
    instead of raising on ``list(None)``.
    """
    if arguments is None:
        return []
    # Inside a user lambda the Java UDF is rejected (001157), so the
    # arguments go to the formatter unchanged, as with the flag off.
    if (
        not arguments
        or not is_cast_spark_floating_to_string_enabled()
        or is_lambda_being_resolved()
    ):
        return list(arguments)
    literal = _string_literal(fmt)
    if literal is None:
        return list(arguments)
    indexes = _percent_s_argument_indexes(literal)
    if not indexes:
        return list(arguments)
    rewritten = list(arguments)
    for index in indexes:
        if index >= len(rewritten) or index >= len(types):
            continue
        datatype = types[index]
        if isinstance(datatype, (FloatType, DoubleType)):
            rewritten[index] = spark_floating_to_string(rewritten[index], datatype)
    return rewritten


def _is_negative_zero(expr: object) -> bool:
    """True when ``expr`` is a float literal -0.0, or a cast/alias of one."""
    for _ in range(4):
        if isinstance(expr, Literal) and isinstance(expr.value, float):
            return expr.value == 0.0 and math.copysign(1.0, expr.value) < 0
        if type(expr).__name__ in {"Cast", "Alias"}:
            expr = getattr(expr, "child", None)
            continue
        return False
    return False


def _string_literal(column: Column) -> str | None:
    expr = getattr(column, "_expression", None)
    if isinstance(expr, Literal) and isinstance(expr.value, str):
        return expr.value
    return None


def _percent_s_argument_indexes(fmt: str) -> list[int] | None:
    """Value-argument indexes consumed by ``%s``.

    ``None`` means the pattern has a feature we do not rewrite (a mapping
    key or an unknown conversion). ``%%`` consumes nothing. A ``*`` width or
    precision consumes an argument that is not the value.
    """
    indexes: list[int] = []
    i = 0
    n = len(fmt)
    arg = 0
    while i < n:
        if fmt[i] != "%":
            i += 1
            continue
        i += 1
        if i >= n:
            return None
        if fmt[i] == "%":
            i += 1
            continue
        if fmt[i] == "(":
            return None
        while i < n and fmt[i] in "#0- +":
            i += 1
        if i < n and fmt[i] == "*":
            arg += 1
            i += 1
        else:
            while i < n and fmt[i].isdigit():
                i += 1
        if i < n and fmt[i] == ".":
            i += 1
            if i < n and fmt[i] == "*":
                arg += 1
                i += 1
            else:
                while i < n and fmt[i].isdigit():
                    i += 1
        if i < n and fmt[i] in "hlL":
            i += 1
        if i >= n:
            return None
        conversion = fmt[i]
        i += 1
        if conversion == "s":
            indexes.append(arg)
        elif conversion not in _PYTHON_CONVERSIONS:
            return None
        arg += 1
    return indexes
