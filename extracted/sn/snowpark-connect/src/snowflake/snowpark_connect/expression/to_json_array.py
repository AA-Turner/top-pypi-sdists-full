#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""``to_json`` of an array: a NULL element is JSON ``null`` (SNOW-4222754).

Snowflake ``TO_JSON(TO_VARIANT(array))`` writes the token ``undefined`` for a SQL
NULL element. Spark's ``JacksonGenerator.writeArrayData`` writes ``null``.

When the innermost element type is numeric, boolean or binary, the token is
replaced in the text of the whole array, but only where it follows ``[`` or ``,``.
Numbers and booleans can't contain ``undefined``. Binary text under
``BINARY_OUTPUT_FORMAT`` HEX or BASE64 can contain those letters but never ``[``
or ``,``, and in compact JSON a NULL slot always follows one of them. Date and
timestamp text follows the session's ``DATE_OUTPUT_FORMAT`` and
``TIMESTAMP_*_OUTPUT_FORMAT``, so it may contain the word, as may a string or a
string inside a struct, map or variant. For those, each element is written by
``TO_JSON(TO_VARIANT(element))`` and a NULL element by ``null``. Nested arrays are
walked the same way. Both paths give the same text for every element that is
not NULL.
"""

from __future__ import annotations

from collections import defaultdict

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark import Column, Session
from snowflake.snowpark.types import (
    ArrayType,
    BinaryType,
    BooleanType,
    DataType,
    _NumericType,
)

_ANCHORED_REPLACE_LEAF_TYPES = (_NumericType, BooleanType, BinaryType)


def _leaf_type(dtype: DataType) -> DataType:
    while isinstance(dtype, ArrayType):
        dtype = dtype.element_type
    return dtype


def _element_sql(var: str, dtype: DataType, depth: int) -> str:
    if not isinstance(dtype, ArrayType):
        # TO_JSON is NULL only for a SQL NULL; a VARIANT JSON null is 'null'.
        return f"COALESCE(TO_JSON(TO_VARIANT({var})), 'null')"
    # ``var`` is a lambda argument, so repeating it costs nothing at compile
    # time. IS_NULL_VALUE catches a JSON null inside a semi-structured array.
    is_null = f"({var} IS NULL OR IS_NULL_VALUE(TO_VARIANT({var})))"
    return f"IFF({is_null}, 'null', {array_json_sql(var, dtype, depth)})"


def array_json_sql(sql: str, dtype: ArrayType, depth: int = 0) -> str:
    """JSON text of an array. ``sql`` appears once; a NULL array gives NULL.

    ``TRANSFORM(NULL, ...)`` is NULL, so the ``||`` chain is NULL too. An empty
    array gives ``[]``. The ``::ARRAY`` cast lets ``ARRAY_TO_STRING`` accept the
    structured ``ARRAY(VARCHAR)`` that ``TRANSFORM`` returns.
    """
    var = f"__sj{depth}"
    element = _element_sql(var, dtype.element_type, depth + 1)
    return (
        f"'[' || ARRAY_TO_STRING(TRANSFORM(({sql}), {var} -> {element})::ARRAY, ',')"
        " || ']'"
    )


def to_json_array_column(col: Column, dtype: ArrayType) -> Column:
    if isinstance(_leaf_type(dtype), _ANCHORED_REPLACE_LEAF_TYPES):
        # A per-element TRANSFORM costs 4x to 15x the execution time of this.
        text = snowpark_fn.to_json(snowpark_fn.to_variant(col))
        text = snowpark_fn.replace(text, "[undefined", "[null")
        return snowpark_fn.replace(text, ",undefined", ",null")
    analyzer = Session.get_active_session()._analyzer
    sql = analyzer.analyze(col._expression, defaultdict())
    return snowpark_fn.sql_expr(array_json_sql(sql, dtype))
