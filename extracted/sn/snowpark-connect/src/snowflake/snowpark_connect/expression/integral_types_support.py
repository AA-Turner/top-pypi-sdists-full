#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from pyspark.errors.exceptions.base import ArithmeticException

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark.column import Column
from snowflake.snowpark.types import (
    ByteType,
    DataType,
    DecimalType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    ShortType,
    StringType,
)
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.expression.error_utils import raise_error_helper


def get_integral_type_bounds(typ: DataType) -> tuple[int, int]:
    if isinstance(typ, ByteType):
        return (-128, 127)
    elif isinstance(typ, ShortType):
        return (-32768, 32767)
    elif isinstance(typ, IntegerType):
        return (-2147483648, 2147483647)
    elif isinstance(typ, LongType):
        return (-9223372036854775808, 9223372036854775807)
    else:
        raise ValueError(f"Unsupported integral type: {typ}")


def _is_integral_overflow(col: Column, data_type: DataType) -> Column:
    """ABS(2*x + 1) > 2*max + 1 — equivalent to (x < min) | (x > max) for
    two's-complement ranges, but references col only once instead of twice."""
    _, max_val = get_integral_type_bounds(data_type)
    threshold = 2 * max_val + 1
    return snowpark_fn.abs(
        col * snowpark_fn.lit(2) + snowpark_fn.lit(1)
    ) > snowpark_fn.lit(threshold)


def apply_integral_overflow(
    col: Column, to_type: DataType, force: bool = False
) -> Column:
    if not force and not global_config.snowpark_connect_handleIntegralOverflow:
        return col.cast(to_type)

    min_val, max_val = get_integral_type_bounds(to_type)
    range_size = max_val - min_val + 1

    # Double-MOD trick: MOD(MOD(x, n) + n, n) always returns a value in
    # [0, n-1] regardless of the sign of x, and — crucially — references
    # `col` only once.  The old CASE-WHEN approach referenced `col` 6×,
    # causing O(6^depth) SQL blowup when overflow checks were nested
    # (e.g. chained integer additions of CASE expressions).
    offset_value = col - snowpark_fn.lit(min_val)
    inner_mod = snowpark_fn.function("MOD")(offset_value, snowpark_fn.lit(range_size))
    wrapped_offset = snowpark_fn.function("MOD")(
        inner_mod + snowpark_fn.lit(range_size),
        snowpark_fn.lit(range_size),
    )
    wrapped_result = wrapped_offset + snowpark_fn.lit(min_val)

    return wrapped_result.cast(to_type)


def apply_fractional_to_integral_cast(col: Column, to_type: DataType) -> Column:
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return col.cast(to_type)

    min_val, max_val = get_integral_type_bounds(to_type)

    clamped = (
        snowpark_fn.when(col > snowpark_fn.lit(max_val), snowpark_fn.lit(max_val))
        .when(col < snowpark_fn.lit(min_val), snowpark_fn.lit(min_val))
        .otherwise(col)
    )

    return clamped.cast(to_type)


# SNOW-2677699: tiny predicate used by the INSERT column-projection wrap
# (map_sql.py:_insert_into_table and map_write.py:_build_cast_column).
_INTEGRAL_TYPES = (
    ByteType,
    ShortType,
    IntegerType,
    LongType,
)
_FRACTIONAL_TYPES = (
    FloatType,
    DoubleType,
    DecimalType,
)
_INTEGRAL_ORDER = {cls: i for i, cls in enumerate(_INTEGRAL_TYPES)}


def _overflow_guard_needed(src: DataType, tgt: DataType) -> bool:
    """Return True when storing `src` into integral `tgt` can overflow.

    Called at INSERT time under ANSI/STRICT. Three cases trigger the wrap:
      - src is a wider integral than tgt (Long→Int, Int→Byte, …).
      - src is any fractional (Float/Double/Decimal) and tgt is integral.
    Returns False for same-type, narrower→wider integral, string/null/date,
    or non-integral targets.
    """
    if not isinstance(tgt, _INTEGRAL_TYPES):
        return False
    if isinstance(src, _FRACTIONAL_TYPES):
        return True
    if isinstance(src, _INTEGRAL_TYPES):
        src_idx = _INTEGRAL_ORDER[type(src)]
        tgt_idx = _INTEGRAL_ORDER[type(tgt)]
        return src_idx > tgt_idx
    return False


def apply_integral_overflow_with_ansi_check(
    col: Column, to_type: DataType, ansi_enabled: bool
) -> Column:
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return col.cast(to_type)

    if not ansi_enabled:
        return apply_integral_overflow(col, to_type)

    type_name = to_type.typeName().upper()
    raise_error = raise_error_helper(to_type, ArithmeticException)

    return snowpark_fn.when(
        _is_integral_overflow(col, to_type),
        raise_error(
            snowpark_fn.lit("[CAST_OVERFLOW] The value "),
            col.cast(StringType()),
            snowpark_fn.lit(
                f" of the type BIGINT cannot be cast to {type_name} due to an overflow. Use `try_cast` to tolerate overflow and return NULL instead."
            ),
        ),
    ).otherwise(col.cast(to_type))


def apply_interval_to_integral_overflow(
    col: Column,
    to_type: DataType,
    source_type_name: str,
    target_type_name: str,
    value_repr: Column,
) -> Column:
    """Cast a (BIGINT-widened) ANSI interval value to an integral type.

    Unlike numeric narrowing, Spark raises CAST_OVERFLOW for interval -> integral
    overflow in BOTH ANSI-enabled and ANSI-disabled modes (it never wraps or
    returns NULL), so this path always raises when the value is out of range.

    ``source_type_name`` is the interval's SQL type (e.g. ``INTERVAL HOUR TO
    SECOND``), ``target_type_name`` is the integral target's SQL type (e.g.
    ``INT``), and ``value_repr`` renders the interval value (e.g. ``INTERVAL
    '23:59:59' HOUR TO SECOND``) so the message matches Spark.
    """
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return col.cast(to_type)

    raise_error = raise_error_helper(to_type, ArithmeticException)

    return snowpark_fn.when(
        _is_integral_overflow(col, to_type),
        raise_error(
            snowpark_fn.lit("[CAST_OVERFLOW] The value "),
            value_repr,
            snowpark_fn.lit(
                f' of the type "{source_type_name}" cannot be cast to '
                f'"{target_type_name}" due to an overflow. Use `try_cast` to '
                "tolerate overflow and return NULL instead. If necessary set "
                '"spark.sql.ansi.enabled" to "false" to bypass this error.'
            ),
        ),
    ).otherwise(col.cast(to_type))


def apply_fractional_to_integral_cast_with_ansi_check(
    col: Column, to_type: DataType, ansi_enabled: bool
) -> Column:
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return col.cast(to_type)

    if not ansi_enabled:
        return apply_fractional_to_integral_cast(col, to_type)

    type_name = to_type.typeName().upper()
    raise_error = raise_error_helper(to_type, ArithmeticException)

    return snowpark_fn.when(
        _is_integral_overflow(col, to_type),
        raise_error(
            snowpark_fn.lit("[CAST_OVERFLOW] The value "),
            col.cast(StringType()),
            snowpark_fn.lit(
                f" of the type DOUBLE cannot be cast to {type_name} "
                f"due to an overflow. Use `try_cast` to tolerate overflow and return NULL instead."
            ),
        ),
    ).otherwise(col.cast(to_type))


def apply_arithmetic_overflow_with_ansi_check(
    result_col: Column, result_type: DataType, ansi_enabled: bool, operation_name: str
) -> Column:
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return result_col.cast(result_type)

    if not ansi_enabled:
        return apply_integral_overflow(result_col, result_type)

    raise_error = raise_error_helper(result_type, ArithmeticException)

    return snowpark_fn.when(
        _is_integral_overflow(result_col, result_type),
        raise_error(
            snowpark_fn.lit(
                f"[ARITHMETIC_OVERFLOW] {operation_name} overflow. "
                f"Use 'try_{operation_name.lower()}' to tolerate overflow and return NULL instead. "
                f'If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
            ),
        ),
    ).otherwise(result_col.cast(result_type))


def apply_unary_overflow(value_col: Column, result_type: DataType) -> Column:
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return (value_col * snowpark_fn.lit(-1)).cast(result_type)

    min_val, _ = get_integral_type_bounds(result_type)
    return snowpark_fn.when(
        value_col == snowpark_fn.lit(min_val),
        snowpark_fn.lit(min_val).cast(result_type),
    ).otherwise((value_col * snowpark_fn.lit(-1)).cast(result_type))


def apply_unary_overflow_with_ansi_check(
    value_col: Column, result_type: DataType, ansi_enabled: bool, operation_name: str
) -> Column:
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return (value_col * snowpark_fn.lit(-1)).cast(result_type)

    if not ansi_enabled:
        return apply_unary_overflow(value_col, result_type)

    min_val, _ = get_integral_type_bounds(result_type)

    raise_error = raise_error_helper(result_type, ArithmeticException)

    return snowpark_fn.when(
        value_col == snowpark_fn.lit(min_val),
        raise_error(
            snowpark_fn.lit(
                f"[ARITHMETIC_OVERFLOW] {operation_name} overflow. "
                f'If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
            ),
        ),
    ).otherwise((value_col * snowpark_fn.lit(-1)).cast(result_type))


def apply_abs_overflow(value_col: Column, result_type: DataType) -> Column:
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return snowpark_fn.abs(value_col).cast(result_type)

    min_val, _ = get_integral_type_bounds(result_type)
    return snowpark_fn.when(
        value_col == snowpark_fn.lit(min_val),
        snowpark_fn.lit(min_val).cast(result_type),
    ).otherwise(snowpark_fn.abs(value_col).cast(result_type))


def apply_abs_overflow_with_ansi_check(
    value_col: Column, result_type: DataType, ansi_enabled: bool
) -> Column:
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return snowpark_fn.abs(value_col).cast(result_type)

    if not ansi_enabled:
        return apply_abs_overflow(value_col, result_type)

    min_val, _ = get_integral_type_bounds(result_type)

    raise_error = raise_error_helper(result_type, ArithmeticException)

    return snowpark_fn.when(
        value_col == snowpark_fn.lit(min_val),
        raise_error(
            snowpark_fn.lit(
                "[ARITHMETIC_OVERFLOW] abs overflow. "
                'If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
            ),
        ),
    ).otherwise(snowpark_fn.abs(value_col).cast(result_type))
