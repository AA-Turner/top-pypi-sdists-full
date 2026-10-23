#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Project a CSV float/double column to Java toString text (SNOW-4222765)."""

from __future__ import annotations

from snowflake.snowpark import Column
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.types import DataType, DoubleType, FloatType
from snowflake.snowpark_connect.utils.udf_cache import register_cached_java_udf

# Snowpark's schema reports both Spark float and double as DoubleType once the
# write select has run (Snowflake FLOAT is double). The names are captured in
# handle_column_names, while the plan schema still says FloatType, and passed
# into rewrite_df. They are not stored on the module: a CSV rewrite that was
# not given this write's names cannot inherit a previous float and narrow a
# double of the same name. Both sides are compared unquoted. Snowpark lists a
# quoted all-uppercase alias such as "F1" as bare F1. The compare stays exact,
# so "f" and "F" under caseSensitive stay distinct.

_DOUBLE_HANDLER = (
    "com.snowflake.snowpark_connect.udfs.JavaFloatingFormatUdfs.double_to_string"
)
_FLOAT_HANDLER = (
    "com.snowflake.snowpark_connect.udfs.JavaFloatingFormatUdfs.float_to_string"
)


def unquoted_csv_float_names(names: frozenset[str] | None) -> frozenset[str]:
    """Unquote float names once for a write.

    ``csv_java_floating_column`` compares against this set on every column,
    so the unquoting stays here rather than inside that call.
    """
    return frozenset(unquote_if_quoted(name) for name in (names or ()))


def csv_java_floating_column(
    column: Column,
    datatype: DataType,
    column_name: str | None = None,
    float_names: frozenset[str] | None = None,
) -> Column:
    """Render ``column`` with ``Double.toString`` or ``Float.toString``.

    Caller has already decided the CSV Java-format flag is on and that
    ``datatype`` is FloatType or DoubleType. A null cell stays null: the
    handler is not called on null inputs, and it returns null if it is.
    ``column_name`` is the post-rename Snowpark name. A Spark float that
    Snowflake has already widened to double is still formatted with
    ``Float.toString`` when that name is in ``float_names``.

    ``float_names`` is the set captured for this write, already unquoted
    (see ``unquoted_csv_float_names``). Omitted or empty means there is no
    Spark float to narrow: a double keeps ``Double.toString``.
    """
    names = float_names or frozenset()
    use_float = isinstance(datatype, FloatType) or (
        column_name is not None and unquote_if_quoted(column_name) in names
    )
    if not isinstance(datatype, (FloatType, DoubleType)) and not use_float:
        return column
    handler = _FLOAT_HANDLER if use_float else _DOUBLE_HANDLER
    render = register_cached_java_udf(handler, ["DOUBLE"], "STRING")
    return render(column)
