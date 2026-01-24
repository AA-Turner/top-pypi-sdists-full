#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from pyspark.errors.exceptions.base import ArithmeticException

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark.column import Column
from snowflake.snowpark.types import (
    ByteType,
    DataType,
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


def apply_integral_overflow(col: Column, to_type: DataType) -> Column:
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return col.cast(to_type)

    min_val, max_val = get_integral_type_bounds(to_type)
    range_size = max_val - min_val + 1

    offset_value = col - snowpark_fn.lit(min_val)
    wrapped_offset = snowpark_fn.function("MOD")(
        offset_value, snowpark_fn.lit(range_size)
    )

    wrapped_offset = snowpark_fn.when(
        wrapped_offset < 0, wrapped_offset + snowpark_fn.lit(range_size)
    ).otherwise(wrapped_offset)

    wrapped_result = wrapped_offset + snowpark_fn.lit(min_val)

    return snowpark_fn.when(
        (col >= snowpark_fn.lit(min_val)) & (col <= snowpark_fn.lit(max_val)),
        col.cast(to_type),
    ).otherwise(wrapped_result.cast(to_type))


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


def apply_integral_overflow_with_ansi_check(
    col: Column, to_type: DataType, ansi_enabled: bool
) -> Column:
    if not global_config.snowpark_connect_handleIntegralOverflow:
        return col.cast(to_type)

    if not ansi_enabled:
        return apply_integral_overflow(col, to_type)

    min_val, max_val = get_integral_type_bounds(to_type)
    type_name = to_type.typeName().upper()

    raise_error = raise_error_helper(to_type, ArithmeticException)

    return snowpark_fn.when(
        (col < snowpark_fn.lit(min_val)) | (col > snowpark_fn.lit(max_val)),
        raise_error(
            snowpark_fn.lit("[CAST_OVERFLOW] The value "),
            col.cast(StringType()),
            snowpark_fn.lit(
                f" of the type BIGINT cannot be cast to {type_name} due to an overflow. Use `try_cast` to tolerate overflow and return NULL instead."
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

    min_val, max_val = get_integral_type_bounds(to_type)
    type_name = to_type.typeName().upper()

    raise_error = raise_error_helper(to_type, ArithmeticException)

    return snowpark_fn.when(
        (col < snowpark_fn.lit(min_val)) | (col > snowpark_fn.lit(max_val)),
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

    min_val, max_val = get_integral_type_bounds(result_type)

    raise_error = raise_error_helper(result_type, ArithmeticException)

    return snowpark_fn.when(
        (result_col < snowpark_fn.lit(min_val))
        | (result_col > snowpark_fn.lit(max_val)),
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
