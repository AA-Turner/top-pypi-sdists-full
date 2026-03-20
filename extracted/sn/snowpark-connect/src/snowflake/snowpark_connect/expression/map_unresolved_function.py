#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import datetime
import functools
import inspect
import math
import operator
import random
import re
import string
import sys
import tempfile
import time
import uuid
from collections import defaultdict
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Context, Decimal
from functools import partial, reduce
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote, unquote

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
from google.protobuf.message import Message
from pyspark.errors.exceptions.base import (
    AnalysisException,
    ArithmeticException,
    ArrayIndexOutOfBoundsException,
    DateTimeException,
    IllegalArgumentException,
    NumberFormatException,
    ParseException,
    SparkRuntimeException,
)
from pyspark.sql.types import _parse_datatype_json_string

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark import Column, Session
from snowflake.snowpark._internal.analyzer.datatype_mapper import to_sql
from snowflake.snowpark._internal.analyzer.expression import Literal
from snowflake.snowpark._internal.analyzer.unary_expression import Alias
from snowflake.snowpark._internal.type_utils import convert_sp_to_sf_type
from snowflake.snowpark.types import (
    ArrayType,
    BinaryType,
    BooleanType,
    ByteType,
    DataType,
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
    StructField,
    StructType,
    TimestampTimeZone,
    TimestampType,
    TimeType,
    VariantType,
    YearMonthIntervalType,
    _AnsiIntervalType,
    _FractionalType,
    _IntegralType,
    _NumericType,
)
from snowflake.snowpark_connect.column_name_handler import (
    ColumnNameMap,
    set_schema_getter,
)
from snowflake.snowpark_connect.column_qualifier import ColumnQualifier
from snowflake.snowpark_connect.config import (
    get_boolean_session_config_param,
    get_timestamp_type,
    global_config,
)
from snowflake.snowpark_connect.constants import (
    DUPLICATE_KEY_FOUND_ERROR_TEMPLATE,
    STRUCTURED_TYPES_ENABLED,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.function_defaults import (
    inject_function_defaults,
)
from snowflake.snowpark_connect.expression.integral_types_support import (
    apply_abs_overflow_with_ansi_check,
    apply_arithmetic_overflow_with_ansi_check,
    apply_integral_overflow,
    apply_unary_overflow_with_ansi_check,
    get_integral_type_bounds,
)
from snowflake.snowpark_connect.expression.literal import get_literal_field_and_name
from snowflake.snowpark_connect.expression.map_cast import (
    CAST_FUNCTIONS,
    SYMBOL_FUNCTIONS,
    map_cast,
    timestamp_to_spark_string,
)
from snowflake.snowpark_connect.expression.map_unresolved_star import (
    map_unresolved_star_as_single_column,
    map_unresolved_star_struct,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.relation.catalogs.utils import CURRENT_CATALOG_NAME
from snowflake.snowpark_connect.relation.utils import is_aggregate_function
from snowflake.snowpark_connect.type_mapping import (
    map_json_schema_to_snowpark,
    map_pyspark_types_to_snowpark_types,
    map_snowpark_to_pyspark_types,
    map_spark_timestamp_format_expression,
    map_type_string_to_snowpark_type,
    map_type_to_snowflake_type,
)
from snowflake.snowpark_connect.typed_column import (
    TypedColumn,
    TypedColumnWithDeferredCast,
    TypedColumnWithDeferredWindowBuilder,
)
from snowflake.snowpark_connect.utils.context import (
    add_sql_aggregate_function,
    get_current_grouping_columns,
    get_is_aggregate_function,
    get_is_evaluating_sql,
    get_is_in_udtf_context,
    get_spark_version,
    is_window_enabled,
    push_udtf_context,
    resolving_fun_args,
    resolving_lambda_function,
    set_is_aggregate_function,
)
from snowflake.snowpark_connect.utils.jvm_udf_utils import to_json
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
    telemetry,
)
from snowflake.snowpark_connect.utils.udf_cache import (
    cached_udaf,
    cached_udf,
    cached_udtf,
    register_cached_java_udf,
    register_cached_sql_udf,
)
from snowflake.snowpark_connect.utils.variant_utils import scala_udf_arg_to_variant
from snowflake.snowpark_connect.utils.xxhash64 import (
    DEFAULT_SEED,
    xxhash64_double,
    xxhash64_float,
    xxhash64_int,
    xxhash64_long,
    xxhash64_string,
)

MAX_UINT64 = 2**64 - 1
MAX_INT64 = 2**63 - 1
MIN_INT64 = -(2**63)
MAX_UINT32 = 2**32 - 1
MAX_32BIT_SIGNED_INT = 2_147_483_647
MIN_32BIT_SIGNED_INT = -2_147_483_648

# Interval arithmetic precision limits
MAX_DAY_TIME_DAYS = 106751991  # Maximum days for day-time intervals
MAX_10_DIGIT_LIMIT = 1000000000  # 10-digit limit (1 billion) for interval operands

# date field name constants
_YEAR_FIELDS = ("year", "y", "years", "yr", "yrs")
_MONTH_FIELDS = ("month", "mon", "mons", "months")
_DAY_FIELDS = ("day", "d", "days")
_HOUR_FIELDS = ("hour", "h", "hours", "hr", "hrs")
_MINUTE_FIELDS = ("minute", "m", "min", "mins", "minutes")
_SECOND_FIELDS = ("second", "s", "sec", "seconds", "secs")
_DAYOFWEEK_FIELDS = ("dayofweek", "weekday", "dow", "dw")

NUMBER_FORMAT_DIGITS = "99,999,999,999,999,999,999,999,999,999,999,999,990"

NAN, INFINITY = float("nan"), float("inf")


class ULongLong(_IntegralType):
    """Unsigned long long integer data type. This maps to the BIGINT data type in Snowflake."""


@dataclass
class OperandInfo:
    """Holds operand information for type precision calculations."""

    typed_column: TypedColumn
    unresolved_expr_type: str | None = None
    arg_name: str | None = None

    @property
    def typ(self) -> DataType:
        return self.typed_column.typ

    @property
    def col(self) -> Column:
        return self.typed_column.col

    @property
    def is_literal(self) -> bool:
        return self.unresolved_expr_type == "literal"


def _does_number_overflow(value, type_) -> bool:
    # Tuples of inclusive min, max numbers for given types
    min_max_values = {
        ByteType(): (-128, 127),
        ShortType(): (-32768, 32767),
        IntegerType(): (-2147483648, 2147483647),
        LongType(): (MIN_INT64, MAX_INT64),
        ULongLong(): (-18446744073709551615, 18446744073709551615),
    }
    if type_ not in min_max_values:
        # Should we raise Exception in this case?
        return False
    min_v, max_v = min_max_values[type_]
    return value < min_v or value > max_v


def _validate_numeric_args(
    function_name: str, typed_args: list, snowpark_args: list
) -> list:
    """Validates that the first two arguments are numeric types. Follows spark and casts strings to double.

    Args:
        function_name: Name of the function being validated (for error message)
        typed_args: List of TypedColumn arguments to check
        snowpark_args: List of Column objects that may be modified

    Returns:
        Modified snowpark_args with string columns cast to DoubleType

    Raises:
        TypeError: If arguments cannot be converted to numeric types
    """
    if len(typed_args) < 2:
        exception = ValueError(f"{function_name} requires at least 2 arguments")
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception

    modified_args = list(snowpark_args)

    # Looping so that we can adjust for fewer/more arguments in the future if needed.
    for i in range(2):
        arg_type = typed_args[i].typ

        match arg_type:
            case _NumericType():
                continue
            case StringType():
                # Cast strings to doubles following Spark
                # https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/analysis/TypeCoercion.scala#L204
                modified_args[i] = snowpark_fn.try_cast(snowpark_args[i], DoubleType())
            case _:
                exception = TypeError(
                    f"Data type mismatch: {function_name} requires numeric types, but got {typed_args[0].typ} and {typed_args[1].typ}."
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

    return modified_args


def unwrap_literal(exp: expressions_proto.Expression):
    """Workaround for Snowpark functions generating invalid SQL when used with fn.lit (SNOW-1871954)"""
    return get_literal_field_and_name(exp.literal)[0]


def _resolve_foldable_string_expression(
    arg_col: Column,
    arg_name: str,
    spark_function_name: str,
    session: Session,
) -> Optional[str]:
    if isinstance(arg_col._expression, Literal):
        literal_value = arg_col._expression.value
        return None if literal_value is None else str(literal_value)

    try:
        value = (
            session.create_dataframe([(1,)])
            .select(arg_col.cast(StringType()))
            .collect()[0][0]
        )
    except Exception:
        exception = AnalysisException(
            f"""[DATATYPE_MISMATCH.NON_FOLDABLE_INPUT] Cannot resolve "{spark_function_name}" due to data type mismatch: the input argument should be a foldable "STRING" expression; however, got "{arg_name}"."""
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        raise exception

    return value


def _coerce_for_comparison(
    left: TypedColumn, right: TypedColumn
) -> tuple[Column, Column]:
    if left.typ == right.typ:
        return left.col, right.col

    # To avoid handling both (A, B) and (B, A), swap them in the second case, then swap back at the end.
    if type(left.typ).__name__ > type(right.typ).__name__:
        left, right = right, left
        swap = True
    else:
        swap = False

    left_col = left.col
    right_col = right.col

    match (left.typ, right.typ):
        case (BooleanType(), IntegerType()):
            left_col = left_col.cast(LongType())
        case (BooleanType(), LongType()):
            left_col = left_col.cast(LongType())
        case (BooleanType(), FloatType()):
            left_col = left_col.cast(IntegerType()).cast(FloatType())
        case (BooleanType(), DoubleType()):
            left_col = left_col.cast(IntegerType()).cast(DoubleType())
        case (BooleanType(), StringType()):
            right_col = right_col.try_cast(BooleanType())
        case (IntegerType(), StringType()):
            right_col = right_col.try_cast(LongType())
        case (LongType(), StringType()):
            right_col = right_col.try_cast(LongType())
        case (FloatType(), StringType()):
            right_col = right_col.try_cast(FloatType())
        case (DoubleType(), StringType()):
            right_col = right_col.try_cast(DoubleType())
        case (DecimalType(), StringType()):
            right_col = right_col.try_cast(DoubleType())
        case (BinaryType(), StringType()):
            # Convert binary to string for comparison
            left_col = snowpark_fn.to_varchar(left_col, "UTF-8")
        case (StringType(), BinaryType()):
            # Convert binary to string for comparison
            right_col = snowpark_fn.to_varchar(right_col, "UTF-8")

    if swap:
        return right_col, left_col
    else:
        return left_col, right_col


def _struct_comparison(
    left: TypedColumn,
    right: TypedColumn,
    op: str,
) -> Column:
    """
    Compare two struct columns using Spark's null handling semantics.

    In Spark, for struct comparison with null fields:
    - null is treated as "smallest" for ordering purposes
    - struct{a: 1} > struct{a: null} is TRUE (non-null > null)
    - struct{a: null} < struct{a: 1} is TRUE (null < non-null)

    Snowflake's default comparison returns NULL when any field is null.
    We need to implement field-by-field comparison with proper null handling.
    """
    left_struct = left.typ
    right_struct = right.typ

    if not isinstance(left_struct, StructType) or not isinstance(
        right_struct, StructType
    ):
        raise ValueError("Both arguments must be StructType")

    left_fields = left_struct.fields
    right_fields = right_struct.fields

    if len(left_fields) != len(right_fields):
        raise ValueError("Structs must have the same number of fields")

    left_col = left.col
    right_col = right.col

    result = None

    for i, (l_field, r_field) in enumerate(zip(left_fields, right_fields)):
        l_val = left_col[l_field.name]
        r_val = right_col[r_field.name]
        l_is_null = l_val.is_null()
        r_is_null = r_val.is_null()

        left_null_only = l_is_null & ~r_is_null
        right_null_only = ~l_is_null & r_is_null
        neither_null = ~l_is_null & ~r_is_null

        if isinstance(l_field.datatype, StructType) and isinstance(
            r_field.datatype, StructType
        ):
            l_dt = l_field.datatype
            r_dt = r_field.datatype
            nested_left = TypedColumn(l_val, lambda lt=l_dt: [lt])
            nested_right = TypedColumn(r_val, lambda rt=r_dt: [rt])
            nested_greater = _struct_comparison(nested_left, nested_right, ">")
            nested_less = _struct_comparison(nested_left, nested_right, "<")
            left_field_greater = right_null_only | (neither_null & nested_greater)
            left_field_less = left_null_only | (neither_null & nested_less)
        else:
            l_field_type = l_field.datatype
            r_field_type = r_field.datatype
            l_typed = TypedColumn(l_val, lambda lt=l_field_type: [lt])
            r_typed = TypedColumn(r_val, lambda rt=r_field_type: [rt])
            _check_interval_string_comparison(
                op, [l_typed, r_typed], [l_field.name, r_field.name]
            )
            left_field_greater = right_null_only | (neither_null & (l_val > r_val))
            left_field_less = left_null_only | (neither_null & (l_val < r_val))

        base = snowpark_fn if i == 0 else result

        if op in (">", ">="):
            cond1, cond2 = left_field_greater, left_field_less
        elif op in ("<", "<="):
            cond1, cond2 = left_field_less, left_field_greater
        else:
            raise ValueError(f"Unsupported operator: {op}")

        result = base.when(cond1, True).when(cond2, False)

    if op in (">", "<"):
        result = result.otherwise(False)
    else:  # >= or <=
        result = result.otherwise(True)

    return result


def _preprocess_not_equals_expression(exp: expressions_proto.Expression) -> str:
    """
    Transform NOT(col1 = col2) expressions to col1 != col2 for Snowflake compatibility.

    Snowflake has issues with NOT (col1 = col2) in subqueries, so we rewrite
    not(==(a, b)) to a != b by modifying the protobuf expression early.

    Returns:
        The (potentially modified) function name as a lowercase string.
    """
    function_name = exp.unresolved_function.function_name.lower()

    # Snowflake has issues with NOT (col1 = col2) in subqueries.
    # Transform not(==(a, b)) to a!=b by modifying the protobuf early.
    if (
        function_name in ("not", "!")
        and len(exp.unresolved_function.arguments) == 1
        and exp.unresolved_function.arguments[0].WhichOneof("expr_type")
        == "unresolved_function"
        and exp.unresolved_function.arguments[0].unresolved_function.function_name
        == "=="
    ):
        inner_eq_func = exp.unresolved_function.arguments[0].unresolved_function
        inner_args = list(inner_eq_func.arguments)

        exp.unresolved_function.function_name = "!="
        exp.unresolved_function.ClearField("arguments")
        exp.unresolved_function.arguments.extend(inner_args)

        function_name = "!="

    return function_name


def map_unresolved_function(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], TypedColumn]:
    from snowflake.snowpark_connect.expression.map_expression import map_expression

    session = Session.get_active_session()

    args_types = list(
        map(lambda a: a.WhichOneof("expr_type"), exp.unresolved_function.arguments)
    )
    # Functions that accept lambda parameters are handled separately to keep the resolution of other functions simple.
    # Lambda parameter types often depend on the types of other arguments passed to the function.
    if "lambda_function" in args_types:
        return _resolve_function_with_lambda(exp, column_mapping, typer)
    if get_is_aggregate_function()[1]:
        set_is_aggregate_function(
            (exp.unresolved_function.function_name, get_is_aggregate_function()[1])
        )

    # Check if this is a UDTF call and set context before resolving arguments
    function_name = exp.unresolved_function.function_name.lower()
    is_udtf_call = function_name in session._udtfs

    # Inject default parameters for functions that need them (especially for Scala clients)
    inject_function_defaults(exp.unresolved_function)

    # Transform NOT(col = col) to col != col for Snowflake compatibility
    function_name = _preprocess_not_equals_expression(exp)

    def _resolve_args_expressions(exp: expressions_proto.Expression):
        def _resolve_fn_arg(exp):
            with resolving_fun_args():
                return map_expression(exp, column_mapping, typer)

        def _unalias_column(tc: TypedColumn) -> TypedColumn:
            # This is required to avoid SQL compilation errors when aliases are used inside subexpressions.
            # We unwrap such aliases and use a child expression for snowpark's evaluation.
            if hasattr(tc.col, "_expression"):
                col_exp = tc.col._expression
                if isinstance(col_exp, Alias):
                    return TypedColumn(Column(col_exp.child), lambda: tc.types)
            return tc

        resolved = [_resolve_fn_arg(arg) for arg in exp.unresolved_function.arguments]
        resolved_without_alias = [
            (names, _unalias_column(tc)) for names, tc in resolved
        ]
        not_empty = list(filter(lambda x: not x[1].is_empty(), resolved_without_alias))
        return zip(*not_empty) if not_empty else ([], [])

    if is_udtf_call:
        with push_udtf_context():
            resolved_snowpark_args: tuple[list[str], list[TypedColumn]] = (
                _resolve_args_expressions(exp)
                if len(exp.unresolved_function.arguments) > 0
                else ([], [])
            )
    else:
        resolved_snowpark_args: tuple[list[str], list[TypedColumn]] = (
            _resolve_args_expressions(exp)
            if len(exp.unresolved_function.arguments) > 0
            else ([], [])
        )

    snowpark_arg_names, snowpark_typed_args = resolved_snowpark_args

    snowpark_arg_names: List[str] = [n for names in snowpark_arg_names for n in names]
    snowpark_args: List[Column] = [arg.col for arg in snowpark_typed_args]

    # default function name
    spark_function_name = (
        f"({snowpark_arg_names[0]} {exp.unresolved_function.function_name} {snowpark_arg_names[1]})"
        if exp.unresolved_function.function_name in SYMBOL_FUNCTIONS
        else f"{exp.unresolved_function.function_name}({', '.join(snowpark_arg_names)})"
    )
    spark_col_names = []
    spark_sql_ansi_enabled = global_config.spark_sql_ansi_enabled
    spark_sql_legacy_allow_hash_on_map_type = (
        global_config.spark_sql_legacy_allowHashOnMapType
    )

    function_name = exp.unresolved_function.function_name.lower()
    telemetry.report_function_usage(function_name)
    result_type: Optional[DataType | List[DateType]] = None
    qualifier_parts: List[str] = []

    # Check if this is an aggregate function (used by GROUP BY ALL implementation)
    if is_aggregate_function(function_name):
        add_sql_aggregate_function()

    def _type_with_typer(col: Column) -> TypedColumn:
        """If you can, avoid using this function. Typer most likely has to call GS to resovle type which is expensive."""
        return TypedColumn(col, lambda: typer.type(col))

    def _resolve_aggregate_exp(
        result_exp: Column, default_result_type: DataType
    ) -> TypedColumn:
        if is_window_enabled():
            # defer casting to capture whole window expression
            return TypedColumnWithDeferredCast(
                result_exp, lambda: [default_result_type]
            )
        else:
            return TypedColumn(
                snowpark_fn.cast(result_exp, default_result_type),
                lambda: [default_result_type],
            )

    def _validate_arity(
        valid_arity: int | list[int] | tuple[Optional[int], Optional[int]],
    ) -> None:
        """
        Validates that the number of arguments passed to a function matches the expected arity.
        Args:
            valid_arity: Can be:
                - An integer specifying the exact required number of arguments
                - A list of integers specifying valid argument counts
                - A tuple (min_arity, None) specifying a minimum number of arguments
                - A tuple (None, max_arity) specifying a maximum number of arguments
        Raises:
            AnalysisException: If the number of actual arguments doesn't match the expected arity
        """
        arity = len(snowpark_args)
        match valid_arity:
            case expected if isinstance(expected, int):
                invalid = arity != expected
                expected_arity = expected
            case (min_arity, None):
                invalid = arity < min_arity
                expected_arity = f"> {min_arity-1}"
            case (None, max_arity):
                invalid = arity > max_arity
                expected_arity = f"< {max_arity+1}"
            case _:
                invalid = arity not in valid_arity
                expected_arity = str(valid_arity)

        if invalid:
            exception = AnalysisException(
                f"[WRONG_NUM_ARGS.WITHOUT_SUGGESTION] The `{function_name}` requires {expected_arity} parameters but the actual number is {arity}."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
            raise exception

    def _like_util(column, patterns, mode, negate=False):
        """
        Utility function to handle LIKE and NOT LIKE operations.

        :param column: The column to apply the LIKE operation on.
        :param patterns: A list of patterns to match against.
        :param mode: 'any' for LIKE ANY, 'all' for LIKE ALL.
        :param negate: True for NOT LIKE, False for LIKE.
        :return: A Snowpark condition.
        """
        if len(patterns) == 0:
            exception = ParseException("Expected something between '(' and ')'")
            attach_custom_error_code(exception, ErrorCodes.INVALID_SQL_SYNTAX)
            raise exception
        if mode not in ["any", "all"]:
            exception = ValueError("Mode must be 'any' or 'all'.")
            attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
            raise exception

        if mode == "any":
            condition = snowpark_fn.lit(False)
            for pattern in patterns:
                if negate:
                    condition |= snowpark_fn.not_(column.like(pattern))
                else:
                    condition |= column.like(pattern)
        else:  # mode == "all"
            condition = snowpark_fn.lit(True)
            for pattern in patterns:
                if negate:
                    condition &= snowpark_fn.not_(column.like(pattern))
                else:
                    condition &= column.like(pattern)

        return condition

    def _check_percentile_percentage_value(perc: float) -> Column:
        if perc is None:
            exception = AnalysisException("The percentage must not be null.")
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        if not 0.0 <= perc <= 1.0:
            exception = AnalysisException("The percentage must be between [0.0, 1.0].")
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        return snowpark_fn.lit(perc)

    def _check_percentile_percentage(exp: expressions_proto.Expression) -> Column:
        return _check_percentile_percentage_value(unwrap_literal(exp))

    def _unwrap_array_literals(
        arg: expressions_proto.Expression,
    ) -> list:
        if arg.HasField("literal"):
            return [
                get_literal_field_and_name(elem)[0]
                for elem in arg.literal.array.elements
            ]
        array_func = arg.unresolved_function
        assert array_func.function_name == "array", array_func
        return [unwrap_literal(elem) for elem in array_func.arguments]

    def _handle_structured_aggregate_result(
        aggregate_func, typed_arg: TypedColumn, expected_types: list[DataType]
    ) -> TypedColumn:
        """Handle aggregate results that may have been converted from structured types to VARIANT"""
        # Check if we need to apply the structured type workaround
        STRUCTURED_INCOMPATIBLE_AGGREGATES = {"min", "max"}
        if (
            aggregate_func.__name__ in STRUCTURED_INCOMPATIBLE_AGGREGATES
            and not is_window_enabled()
            and isinstance(typed_arg.typ, (ArrayType, MapType, StructType))
        ):
            # Apply the workaround: cast to VARIANT, apply aggregate, then cast back
            variant_arg = snowpark_fn.to_variant(typed_arg.col)
            result = aggregate_func(variant_arg)

            return TypedColumn(result.cast(typed_arg.typ), lambda: expected_types)
        else:
            # No structured type conversion needed
            result = aggregate_func(typed_arg.col)
            return TypedColumn(result, lambda: expected_types)

    def _create_xpath_expression(udf_method, udf_return_type):
        """Helper to create xpath UDF expressions."""
        xpath_udf = register_cached_java_udf(
            f"com.snowflake.snowpark_connect.udfs.XPathUdfs.{udf_method}",
            ["STRING", "STRING"],
            udf_return_type,
        )

        return xpath_udf(*snowpark_args)

    def _cast_and_handle_nan_xpath_expression(xpath_udf_expression, cast_type):
        """Handle NaN by returning 0 and casting to given to result_type.

        Since xpath_number by default may return NaN, we need to handle it and
        return 0 instead for certain return types (Int, Long, Short).
        """
        return snowpark_fn.when(
            snowpark_fn.equal_nan(xpath_udf_expression), snowpark_fn.lit(0)
        ).otherwise(snowpark_fn.cast(xpath_udf_expression, cast_type))

    match function_name:
        case func_name if func_name.lower() in session._udfs:
            # In Spark, UDFs can override built-in functions
            udf = session._udfs[func_name.lower()]
            udf_args = [
                scala_udf_arg_to_variant(arg, tc.typ)
                if udf.is_scala
                else snowpark_fn.cast(arg, VariantType())
                for arg, tc in zip(snowpark_args, snowpark_typed_args)
            ]
            if udf.attach_schema_json:
                schema_json = to_json(
                    [t.typ for t in snowpark_typed_args], escape_quotes=False
                )
                udf_args.append(snowpark_fn.lit(schema_json))
            result_exp = snowpark_fn.call_udf(udf.name, *udf_args)
            if udf.cast_to_original_return_type:
                result_exp = snowpark_fn.cast(result_exp, udf.original_return_type)
                result_type = udf.original_return_type
            else:
                result_type = udf.return_type
        case func_name if (
            get_is_evaluating_sql() and func_name.lower() in session._udtfs
        ):
            udtf, spark_col_names = session._udtfs[func_name.lower()]
            result_exp = snowpark_fn.call_table_function(
                udtf.name,
                *(snowpark_fn.cast(arg, VariantType()) for arg in snowpark_args),
            )
            result_type = [f.datatype for f in udtf.output_schema]
        case "!=":
            _check_interval_string_comparison(
                "!=", snowpark_typed_args, snowpark_arg_names
            )
            # Make the function name same as spark connect. a != b translate's to not(a=b)
            spark_function_name = (
                f"(NOT ({snowpark_arg_names[0]} = {snowpark_arg_names[1]}))"
            )
            left, right = _coerce_for_comparison(
                snowpark_typed_args[0], snowpark_typed_args[1]
            )
            result_exp = TypedColumn(left != right, lambda: [BooleanType()])
        case "%" | "mod":
            if spark_sql_ansi_enabled:
                result_exp = snowpark_args[0] % snowpark_args[1]
            else:
                # when divisor is zero return None instead of error.
                result_exp = snowpark_fn.when(
                    snowpark_args[1] == 0, snowpark_fn.lit(None)
                ).otherwise(snowpark_args[0] % snowpark_args[1])
            result_type = _get_mod_return_type(
                OperandInfo(
                    snowpark_typed_args[0], args_types[0], snowpark_arg_names[0]
                ),
                OperandInfo(
                    snowpark_typed_args[1], args_types[1], snowpark_arg_names[1]
                ),
            )
            result_exp = TypedColumn(
                result_exp.cast(result_type), lambda: [result_type]
            )
        case "*":
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (DecimalType(), NullType()) | (NullType(), DecimalType()):
                    decimal_arg = (
                        snowpark_typed_args[0]
                        if isinstance(snowpark_typed_args[0].typ, DecimalType)
                        else snowpark_typed_args[1]
                    )
                    p1, s1 = _get_type_precision(
                        OperandInfo(
                            decimal_arg,
                        )
                    )
                    result_type, _ = _get_decimal_multiplication_result_type(
                        p1, s1, p1, s1
                    )
                    result_exp = snowpark_fn.lit(None)
                case (DecimalType(), t) | (t, DecimalType()) if isinstance(
                    t, (DecimalType, _IntegralType)
                ):
                    p1, s1 = _get_type_precision(
                        OperandInfo(
                            snowpark_typed_args[0],
                            args_types[0],
                            snowpark_arg_names[0],
                        )
                    )
                    p2, s2 = _get_type_precision(
                        OperandInfo(
                            snowpark_typed_args[1],
                            args_types[1],
                            snowpark_arg_names[1],
                        )
                    )
                    (
                        result_type,
                        overflow_possible,
                    ) = _get_decimal_multiplication_result_type(p1, s1, p2, s2)
                    result_exp = _arithmetic_operation(
                        snowpark_typed_args[0],
                        snowpark_typed_args[1],
                        lambda x, y: x * y,
                        overflow_possible,
                        global_config.spark_sql_ansi_enabled,
                        result_type,
                        "multiply",
                    )
                case (NullType(), NullType()):
                    result_type = DoubleType()
                    result_exp = snowpark_fn.lit(None)
                case (StringType(), StringType()):
                    if spark_sql_ansi_enabled:
                        exception = AnalysisException(
                            f'[DATATYPE_MISMATCH.BINARY_OP_WRONG_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: the binary operator requires the input type ("DOUBLE" or "DECIMAL"), not "STRING".'
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
                    else:
                        result_type = DoubleType()
                        result_exp = snowpark_args[0].try_cast(
                            result_type
                        ) * snowpark_args[1].try_cast(result_type)
                case (StringType(), _IntegralType()):
                    if spark_sql_ansi_enabled:
                        result_type = LongType()
                        result_exp = (
                            snowpark_args[0].cast(result_type) * snowpark_args[1]
                        )
                    else:
                        result_type = DoubleType()
                        result_exp = (
                            snowpark_args[0].try_cast(result_type) * snowpark_args[1]
                        )
                case (StringType(), _FractionalType()):
                    result_type = DoubleType()
                    if spark_sql_ansi_enabled:
                        result_exp = (
                            snowpark_args[0].cast(result_type) * snowpark_args[1]
                        )
                    else:
                        result_exp = (
                            snowpark_args[0].try_cast(result_type) * snowpark_args[1]
                        )
                case (_IntegralType(), StringType()):
                    if spark_sql_ansi_enabled:
                        result_type = LongType()
                        result_exp = snowpark_args[0] * snowpark_args[1].cast(
                            result_type
                        )
                    else:
                        result_type = DoubleType()
                        result_exp = snowpark_args[0] * snowpark_args[1].try_cast(
                            result_type
                        )
                case (_FractionalType(), StringType()):
                    result_type = DoubleType()
                    if spark_sql_ansi_enabled:
                        result_exp = snowpark_args[0] * snowpark_args[1].cast(
                            result_type
                        )
                    else:
                        result_exp = snowpark_args[0] * snowpark_args[1].try_cast(
                            result_type
                        )
                case (StringType(), t) | (t, StringType()) if isinstance(
                    t, _AnsiIntervalType
                ):
                    if isinstance(snowpark_typed_args[0].typ, StringType):
                        result_type = type(
                            t
                        )()  # YearMonthIntervalType() or DayTimeIntervalType()
                        result_exp = snowpark_args[1] * snowpark_args[0].try_cast(
                            LongType()
                        )
                        spark_function_name = (
                            f"({snowpark_arg_names[1]} * {snowpark_arg_names[0]})"
                        )
                    else:
                        result_type = type(
                            t
                        )()  # YearMonthIntervalType() or DayTimeIntervalType()
                        result_exp = snowpark_args[0] * snowpark_args[1].try_cast(
                            LongType()
                        )
                        spark_function_name = (
                            f"({snowpark_arg_names[0]} * {snowpark_arg_names[1]})"
                        )
                case (
                    (_NumericType() as t, NullType())
                    | (NullType(), _NumericType() as t)
                ):
                    result_type = t
                    result_exp = snowpark_fn.lit(None)
                case (NullType(), t) | (t, NullType()) if isinstance(
                    t, _AnsiIntervalType
                ):
                    result_type = (
                        YearMonthIntervalType()
                        if isinstance(t, YearMonthIntervalType)
                        else DayTimeIntervalType()
                    )
                    result_exp = snowpark_fn.lit(None)
                    if isinstance(snowpark_typed_args[0].typ, NullType):
                        spark_function_name = (
                            f"({snowpark_arg_names[1]} * {snowpark_arg_names[0]})"
                        )
                    else:
                        spark_function_name = (
                            f"({snowpark_arg_names[0]} * {snowpark_arg_names[1]})"
                        )
                case (DecimalType(), t) | (t, DecimalType()) if isinstance(
                    t, _AnsiIntervalType
                ):
                    result_type = (
                        YearMonthIntervalType()
                        if isinstance(t, YearMonthIntervalType)
                        else DayTimeIntervalType()
                    )
                    if isinstance(snowpark_typed_args[0].typ, DecimalType):
                        result_exp = snowpark_args[1] * snowpark_args[0]
                        spark_function_name = (
                            f"({snowpark_arg_names[1]} * {snowpark_arg_names[0]})"
                        )
                    else:
                        result_exp = snowpark_args[0] * snowpark_args[1]
                        spark_function_name = (
                            f"({snowpark_arg_names[0]} * {snowpark_arg_names[1]})"
                        )
                case (t, _NumericType()) if isinstance(t, _AnsiIntervalType):
                    result_type = (
                        YearMonthIntervalType()
                        if isinstance(t, YearMonthIntervalType)
                        else DayTimeIntervalType()
                    )
                    result_exp = snowpark_args[0] * snowpark_args[1]
                case (_NumericType(), t) if isinstance(t, _AnsiIntervalType):
                    result_type = (
                        YearMonthIntervalType()
                        if isinstance(t, YearMonthIntervalType)
                        else DayTimeIntervalType()
                    )
                    result_exp = snowpark_args[1] * snowpark_args[0]
                    spark_function_name = (
                        f"({snowpark_arg_names[1]} * {snowpark_arg_names[0]})"
                    )
                case (_NumericType(), _NumericType()):
                    result_type = _find_common_type(
                        [arg.typ for arg in snowpark_typed_args]
                    )
                    if isinstance(result_type, _IntegralType):
                        raw_result = snowpark_args[0].cast(result_type) * snowpark_args[
                            1
                        ].cast(result_type)
                        result_exp = apply_arithmetic_overflow_with_ansi_check(
                            raw_result, result_type, spark_sql_ansi_enabled, "multiply"
                        )
                    else:
                        result_exp = snowpark_args[0].cast(result_type) * snowpark_args[
                            1
                        ].cast(result_type)
                case _:
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{spark_function_name}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
        case "+":
            spark_function_name = _get_spark_function_name(
                snowpark_typed_args[0],
                snowpark_typed_args[1],
                snowpark_arg_names,
                exp,
                spark_function_name,
                "+",
            )
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (TimestampType(), NullType()) | (NullType(), TimestampType()):
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{spark_function_name}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                case (DateType(), NullType()) | (NullType(), DateType()):
                    result_type = DateType()
                    result_exp = snowpark_fn.lit(None).cast(result_type)
                case (NullType(), _) | (_, NullType()):
                    result_type, _ = _get_add_sub_result_type(
                        OperandInfo(
                            snowpark_typed_args[0],
                            args_types[0],
                            snowpark_arg_names[0],
                        ),
                        OperandInfo(
                            snowpark_typed_args[1],
                            args_types[1],
                            snowpark_arg_names[1],
                        ),
                        spark_function_name,
                    )
                    result_exp = snowpark_args[0] + snowpark_args[1]
                    result_exp = result_exp.cast(result_type)
                case (DateType(), t) | (t, DateType()):
                    date_param_index = (
                        0 if isinstance(snowpark_typed_args[0].typ, DateType) else 1
                    )
                    t_param_index = 1 - date_param_index
                    if isinstance(t, (IntegerType, ShortType, ByteType)):
                        result_type = DateType()
                        result_exp = snowpark_args[0] + snowpark_args[1]
                    elif isinstance(t, (DayTimeIntervalType, YearMonthIntervalType)):
                        result_type = (
                            TimestampType()
                            if isinstance(
                                snowpark_typed_args[t_param_index].typ,
                                DayTimeIntervalType,
                            )
                            else DateType()
                        )
                        result_exp = (
                            snowpark_args[date_param_index]
                            + snowpark_args[t_param_index]
                        )
                    elif (
                        hasattr(
                            snowpark_typed_args[t_param_index].col._expr1, "pretty_name"
                        )
                        and "INTERVAL"
                        == snowpark_typed_args[t_param_index].col._expr1.pretty_name
                    ):
                        result_type = TimestampType()
                        result_exp = (
                            snowpark_args[date_param_index]
                            + snowpark_args[t_param_index]
                        )
                    else:
                        exception = AnalysisException(
                            f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 2 requires the ("INT" or "SMALLINT" or "TINYINT") type, however "{snowpark_arg_names[t_param_index]}" has the type "{t}".',
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
                case (TimestampType(), t) | (t, TimestampType()):
                    timestamp_param_index = (
                        0
                        if isinstance(snowpark_typed_args[0].typ, TimestampType)
                        else 1
                    )
                    t_param_index = 1 - timestamp_param_index
                    if isinstance(t, (DayTimeIntervalType, YearMonthIntervalType)):
                        result_type = TimestampType()
                        result_exp = (
                            snowpark_args[timestamp_param_index]
                            + snowpark_args[t_param_index]
                        )
                    elif (
                        hasattr(
                            snowpark_typed_args[t_param_index].col._expr1, "pretty_name"
                        )
                        and "INTERVAL"
                        == snowpark_typed_args[t_param_index].col._expr1.pretty_name
                    ):
                        result_type = TimestampType()
                        result_exp = (
                            snowpark_args[timestamp_param_index]
                            + snowpark_args[t_param_index]
                        )
                    else:
                        raise AnalysisException(
                            f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 2 requires the ("INTERVAL") type for timestamp operations, however "{snowpark_arg_names[t_param_index]}" has the type "{t}".',
                        )
                case (StringType(), StringType()):
                    if spark_sql_ansi_enabled:
                        exception = AnalysisException(
                            f'[DATATYPE_MISMATCH.BINARY_OP_WRONG_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: the binary operator requires the input type ("NUMERIC" or "INTERVAL DAY TO SECOND" or "INTERVAL YEAR TO MONTH" or "INTERVAL"), not "STRING".'
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
                    else:
                        result_type = DoubleType()
                        result_exp = snowpark_fn.try_cast(
                            snowpark_args[0], result_type
                        ) + snowpark_fn.try_cast(snowpark_args[1], result_type)
                case (StringType(), _NumericType() as t):
                    if spark_sql_ansi_enabled:
                        result_type = (
                            DoubleType()
                            if isinstance(t, _FractionalType)
                            else LongType()
                        )
                        result_exp = (
                            snowpark_args[0].cast(result_type) + snowpark_args[1]
                        )
                    else:
                        result_type = DoubleType()
                        result_exp = (
                            snowpark_fn.try_cast(snowpark_args[0], result_type)
                            + snowpark_args[1]
                        )
                case (_NumericType() as t, StringType()):
                    if spark_sql_ansi_enabled:
                        result_type = (
                            DoubleType()
                            if isinstance(t, _FractionalType)
                            else LongType()
                        )
                        result_exp = snowpark_args[0] + snowpark_args[1].cast(
                            result_type
                        )
                    else:
                        result_type = DoubleType()
                        result_exp = snowpark_args[0] + snowpark_fn.try_cast(
                            snowpark_args[1], result_type
                        )
                case (DecimalType(), t) | (t, DecimalType()) if isinstance(
                    t, (BinaryType, TimestampType)
                ):
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{spark_function_name}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                case (t1, t2) | (t2, t1) if isinstance(
                    t1, _AnsiIntervalType
                ) and isinstance(t2, _AnsiIntervalType) and type(t1) == type(t2):
                    # Both operands are the same interval type
                    result_type = type(t1)(
                        min(t1.start_field, t2.start_field),
                        max(t1.end_field, t2.end_field),
                    )
                    result_exp = snowpark_args[0] + snowpark_args[1]
                case (StringType(), t) | (t, StringType()) if isinstance(
                    t, YearMonthIntervalType
                ):
                    # String + YearMonthInterval: Spark tries to cast string to double first, throws error if it fails
                    result_type = StringType()
                    raise_error = _raise_error_helper(StringType(), AnalysisException)
                    if isinstance(snowpark_typed_args[0].typ, StringType):
                        # Try to cast string to double, if it fails (returns null), raise exception
                        cast_result = snowpark_fn.try_cast(snowpark_args[0], "double")
                        result_exp = snowpark_fn.when(
                            cast_result.is_null(),
                            raise_error(
                                snowpark_fn.lit(
                                    f'The value \'{snowpark_args[0]}\' of the type {snowpark_typed_args[0].typ} cannot be cast to "DOUBLE" because it is malformed. Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                                )
                            ),
                        ).otherwise(cast_result + snowpark_args[1])
                    else:
                        cast_result = snowpark_fn.try_cast(snowpark_args[1], "double")
                        result_exp = snowpark_fn.when(
                            cast_result.is_null(),
                            raise_error(
                                snowpark_fn.lit(
                                    f'The value \'{snowpark_args[0]}\' of the type {snowpark_typed_args[0].typ} cannot be cast to "DOUBLE" because it is malformed. Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                                )
                            ),
                        ).otherwise(snowpark_args[0] + cast_result)
                case (StringType(), t) | (t, StringType()) if isinstance(
                    t, DayTimeIntervalType
                ):
                    # String + DayTimeInterval: try to parse string as timestamp, return NULL if it fails
                    # For time-only strings (like '10:00:00'), prepend current date to make it a full timestamp
                    result_type = StringType()
                    if isinstance(snowpark_typed_args[0].typ, StringType):
                        # Check if string looks like time-only (HH:MM:SS or HH:MM pattern)
                        # If so, prepend current date; otherwise use as-is
                        time_only_pattern = snowpark_fn.function("regexp_like")(
                            snowpark_args[0], r"^\d{1,2}:\d{2}(:\d{2})?$"
                        )
                        timestamp_expr = snowpark_fn.when(
                            time_only_pattern,
                            snowpark_fn.function("try_to_timestamp_ntz")(
                                snowpark_fn.function("concat")(
                                    snowpark_fn.function("to_char")(
                                        snowpark_fn.function("current_date")(),
                                        "YYYY-MM-DD",
                                    ),
                                    snowpark_fn.lit(" "),
                                    snowpark_args[0],
                                )
                            ),
                        ).otherwise(
                            snowpark_fn.function("try_to_timestamp_ntz")(
                                snowpark_args[0]
                            )
                        )
                        result_exp = timestamp_expr + snowpark_args[1]
                    else:
                        # interval + string case
                        time_only_pattern = snowpark_fn.function("regexp_like")(
                            snowpark_args[1], r"^\d{1,2}:\d{2}(:\d{2})?$"
                        )
                        timestamp_expr = snowpark_fn.when(
                            time_only_pattern,
                            snowpark_fn.function("try_to_timestamp_ntz")(
                                snowpark_fn.function("concat")(
                                    snowpark_fn.function("to_char")(
                                        snowpark_fn.function("current_date")(),
                                        "'YYYY-MM-DD'",
                                    ),
                                    snowpark_fn.lit(" "),
                                    snowpark_args[1],
                                )
                            ),
                        ).otherwise(
                            snowpark_fn.function("try_to_timestamp_ntz")(
                                snowpark_args[1]
                            )
                        )
                        result_exp = snowpark_args[0] + timestamp_expr
                    spark_function_name = (
                        f"{snowpark_arg_names[0]} + {snowpark_arg_names[1]}"
                    )

                case _:
                    result_type, overflow_possible = _get_add_sub_result_type(
                        OperandInfo(
                            snowpark_typed_args[0],
                            args_types[0],
                            snowpark_arg_names[0],
                        ),
                        OperandInfo(
                            snowpark_typed_args[1],
                            args_types[1],
                            snowpark_arg_names[1],
                        ),
                        spark_function_name,
                    )

                    result_exp = _arithmetic_operation(
                        snowpark_typed_args[0],
                        snowpark_typed_args[1],
                        lambda x, y: x + y,
                        overflow_possible,
                        global_config.spark_sql_ansi_enabled,
                        result_type,
                        "add",
                    )

        case "-":
            spark_function_name = _get_spark_function_name(
                snowpark_typed_args[0],
                snowpark_typed_args[1],
                snowpark_arg_names,
                exp,
                spark_function_name,
                "-",
            )
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (TimestampType(), NullType()) | (NullType(), TimestampType()):
                    result_type = DayTimeIntervalType(
                        DayTimeIntervalType.DAY, DayTimeIntervalType.SECOND
                    )
                    result_exp = snowpark_fn.lit(None).cast(result_type)
                case (DateType(), NullType()) | (NullType(), DateType()):
                    result_type = DateType()
                    result_exp = snowpark_fn.lit(None).cast(result_type)
                case (NullType(), _) | (_, NullType()):
                    result_type, _ = _get_add_sub_result_type(
                        OperandInfo(
                            snowpark_typed_args[0],
                            args_types[0],
                            snowpark_arg_names[0],
                        ),
                        OperandInfo(
                            snowpark_typed_args[1],
                            args_types[1],
                            snowpark_arg_names[1],
                        ),
                        spark_function_name,
                    )
                    result_exp = snowpark_args[0] - snowpark_args[1]
                    result_exp = result_exp.cast(result_type)
                case (DateType(), DateType()):
                    result_type = DayTimeIntervalType(
                        DayTimeIntervalType.DAY, DayTimeIntervalType.DAY
                    )
                    result_exp = snowpark_fn.interval_day_time_from_parts(
                        snowpark_args[0] - snowpark_args[1]
                    )
                case (DateType(), DayTimeIntervalType()) | (
                    DateType(),
                    YearMonthIntervalType(),
                ):
                    result_type = (
                        TimestampType()
                        if isinstance(snowpark_typed_args[1].typ, DayTimeIntervalType)
                        else DateType()
                    )
                    result_exp = snowpark_args[0] - snowpark_args[1]
                case (DateType(), StringType()):
                    if (
                        hasattr(snowpark_typed_args[1].col._expr1, "pretty_name")
                        and "INTERVAL" == snowpark_typed_args[1].col._expr1.pretty_name
                    ):
                        result_type = TimestampType()
                        result_exp = snowpark_args[0] - snowpark_args[1]
                    else:
                        input_type = (
                            DateType() if spark_sql_ansi_enabled else DoubleType()
                        )
                        if isinstance(input_type, DateType):
                            result_type = DayTimeIntervalType(
                                DayTimeIntervalType.DAY, DayTimeIntervalType.DAY
                            )
                            result_exp = snowpark_fn.interval_day_time_from_parts(
                                snowpark_args[0] - snowpark_args[1].cast(input_type)
                            )
                        else:
                            # If ANSI is disabled, cast to DoubleType and return long (legacy behavior)
                            result_type = LongType()
                            result_exp = snowpark_args[0] - snowpark_args[1].cast(
                                input_type
                            )
                case (TimestampType(), DayTimeIntervalType()) | (
                    TimestampType(),
                    YearMonthIntervalType(),
                ):
                    result_type = TimestampType()
                    result_exp = snowpark_args[0] - snowpark_args[1]
                case (TimestampType(), StringType()):
                    if (
                        hasattr(snowpark_typed_args[1].col._expr1, "pretty_name")
                        and "INTERVAL" == snowpark_typed_args[1].col._expr1.pretty_name
                    ):
                        result_type = TimestampType()
                        result_exp = snowpark_args[0] - snowpark_args[1]
                    else:
                        raise AnalysisException(
                            f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 2 requires the ("INTERVAL") type for timestamp operations, however "{snowpark_arg_names[1]}" has the type "{snowpark_typed_args[1].typ}".',
                        )
                case (StringType(), DateType()):
                    result_type = DayTimeIntervalType(
                        DayTimeIntervalType.DAY, DayTimeIntervalType.DAY
                    )
                    result_exp = snowpark_fn.interval_day_time_from_parts(
                        snowpark_args[0].cast(DateType()) - snowpark_args[1]
                    )
                case (DateType(), (IntegerType() | ShortType() | ByteType())):
                    result_type = DateType()
                    result_exp = snowpark_args[0] - snowpark_args[1]
                case (DateType(), _):
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 2 requires the ("INT" or "SMALLINT" or "TINYINT") type, however "{snowpark_arg_names[1]}" has the type "{snowpark_typed_args[1].typ}".',
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                case (_, DateType()):
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 1 requires the "DATE" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".',
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                case (StringType(), StringType()):
                    if spark_sql_ansi_enabled:
                        exception = AnalysisException(
                            f'[DATATYPE_MISMATCH.BINARY_OP_WRONG_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: the binary operator requires the input type ("NUMERIC" or "INTERVAL DAY TO SECOND" or "INTERVAL YEAR TO MONTH" or "INTERVAL"), not "STRING".'
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
                    else:
                        result_type = DoubleType()
                        result_exp = snowpark_fn.try_cast(
                            snowpark_args[0], result_type
                        ) - snowpark_fn.try_cast(snowpark_args[1], result_type)
                case (StringType(), _NumericType() as t):
                    if spark_sql_ansi_enabled:
                        result_type = (
                            DoubleType()
                            if isinstance(t, _FractionalType)
                            else LongType()
                        )
                        result_exp = (
                            snowpark_args[0].cast(result_type) - snowpark_args[1]
                        )
                    else:
                        result_type = DoubleType()
                        result_exp = (
                            snowpark_fn.try_cast(snowpark_args[0], result_type)
                            - snowpark_args[1]
                        )
                case (_NumericType() as t, StringType()):
                    if spark_sql_ansi_enabled:
                        result_type = (
                            DoubleType()
                            if isinstance(t, _FractionalType)
                            else LongType()
                        )
                        result_exp = snowpark_args[0] - snowpark_args[1].cast(
                            result_type
                        )
                    else:
                        result_type = DoubleType()
                        result_exp = snowpark_args[0] - snowpark_fn.try_cast(
                            snowpark_args[1], result_type
                        )
                case (DecimalType(), t) | (t, DecimalType()) if isinstance(
                    t, (BinaryType, TimestampType)
                ):
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{spark_function_name}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                case (StringType(), t) if isinstance(t, _AnsiIntervalType):
                    # String - Interval: try to parse string as timestamp, return NULL if it fails
                    result_type = StringType()
                    result_exp = (
                        snowpark_fn.function("try_to_timestamp")(snowpark_args[0])
                        - snowpark_args[1]
                    )
                    spark_function_name = (
                        f"{snowpark_arg_names[0]} - {snowpark_arg_names[1]}"
                    )
                case _:
                    result_type, overflow_possible = _get_add_sub_result_type(
                        OperandInfo(
                            snowpark_typed_args[0],
                            args_types[0],
                            snowpark_arg_names[0],
                        ),
                        OperandInfo(
                            snowpark_typed_args[1],
                            args_types[1],
                            snowpark_arg_names[1],
                        ),
                        spark_function_name,
                    )
                    result_exp = _arithmetic_operation(
                        snowpark_typed_args[0],
                        snowpark_typed_args[1],
                        lambda x, y: x - y,
                        overflow_possible,
                        global_config.spark_sql_ansi_enabled,
                        result_type,
                        "subtract",
                    )

        case "/":
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (DecimalType(), NullType()):
                    p1, s1 = _get_type_precision(OperandInfo(snowpark_typed_args[0]))
                    result_type, _ = _get_decimal_division_result_type(p1, s1, p1, s1)
                    result_exp = snowpark_fn.lit(None).cast(result_type)
                case (DecimalType(), t) | (t, DecimalType()) if isinstance(
                    t, (DecimalType, _IntegralType)
                ):
                    p1, s1 = _get_type_precision(
                        OperandInfo(
                            snowpark_typed_args[0],
                            args_types[0],
                            snowpark_arg_names[0],
                        )
                    )
                    p2, s2 = _get_type_precision(
                        OperandInfo(
                            snowpark_typed_args[1],
                            args_types[1],
                            snowpark_arg_names[1],
                        )
                    )
                    result_type, overflow_possible = _get_decimal_division_result_type(
                        p1, s1, p2, s2
                    )

                    result_exp = _arithmetic_operation(
                        snowpark_typed_args[0],
                        snowpark_typed_args[1],
                        lambda x, y: _divnull(x, y),
                        overflow_possible,
                        global_config.spark_sql_ansi_enabled,
                        result_type,
                        "divide",
                    )
                case (NullType(), NullType()):
                    result_type = DoubleType()
                    result_exp = snowpark_fn.lit(None)
                case (StringType(), StringType()):
                    if spark_sql_ansi_enabled:
                        exception = AnalysisException(
                            f'[DATATYPE_MISMATCH.BINARY_OP_WRONG_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: the binary operator requires the input type ("DOUBLE" or "DECIMAL"), not "STRING".'
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
                    else:
                        result_type = DoubleType()
                        result_exp = _divnull(
                            snowpark_args[0].try_cast(result_type),
                            snowpark_args[1].try_cast(result_type),
                        )
                case (StringType(), _IntegralType()):
                    result_type = DoubleType()
                    if spark_sql_ansi_enabled:
                        result_exp = _divnull(
                            snowpark_args[0].cast(LongType()),
                            snowpark_args[1].cast(result_type),
                        )
                    else:
                        result_exp = _divnull(
                            snowpark_args[0].try_cast(result_type), snowpark_args[1]
                        )
                    result_exp = result_exp.cast(result_type)
                case (StringType(), _FractionalType()):
                    result_type = DoubleType()
                    if spark_sql_ansi_enabled:
                        result_exp = _divnull(
                            snowpark_args[0].cast(result_type), snowpark_args[1]
                        )
                    else:
                        result_exp = _divnull(
                            snowpark_args[0].try_cast(result_type), snowpark_args[1]
                        )
                case (_IntegralType(), StringType()):
                    result_type = DoubleType()
                    if spark_sql_ansi_enabled:
                        result_exp = _divnull(
                            snowpark_args[0].cast(result_type),
                            snowpark_args[1].cast(LongType()),
                        )
                    else:
                        result_exp = _divnull(
                            snowpark_args[0], snowpark_args[1].try_cast(result_type)
                        )
                    result_exp = result_exp.cast(result_type)
                case (_FractionalType(), StringType()):
                    result_type = DoubleType()
                    if spark_sql_ansi_enabled:
                        result_exp = _divnull(
                            snowpark_args[0], snowpark_args[1].cast(result_type)
                        )
                    else:
                        result_exp = _divnull(
                            snowpark_args[0], snowpark_args[1].try_cast(result_type)
                        )
                case (t, StringType()) if isinstance(t, _AnsiIntervalType):
                    result_type = (
                        YearMonthIntervalType()
                        if isinstance(t, YearMonthIntervalType)
                        else DayTimeIntervalType()
                    )
                    result_exp = snowpark_args[0] / snowpark_args[1].try_cast(
                        LongType()
                    )
                    spark_function_name = (
                        f"({snowpark_arg_names[0]} / {snowpark_arg_names[1]})"
                    )
                case (_NumericType(), NullType()) | (NullType(), _NumericType()):
                    result_type = DoubleType()
                    result_exp = snowpark_fn.lit(None)
                case (t, NullType()) if isinstance(t, _AnsiIntervalType):
                    # Only allow interval / null, not null / interval
                    result_type = (
                        YearMonthIntervalType()
                        if isinstance(t, YearMonthIntervalType)
                        else DayTimeIntervalType()
                    )
                    result_exp = snowpark_fn.lit(None)
                    spark_function_name = (
                        f"({snowpark_arg_names[0]} / {snowpark_arg_names[1]})"
                    )
                case (DecimalType(), t) | (t, DecimalType()) if isinstance(
                    t, _AnsiIntervalType
                ):
                    result_type = (
                        YearMonthIntervalType()
                        if isinstance(t, YearMonthIntervalType)
                        else DayTimeIntervalType()
                    )
                    if isinstance(snowpark_typed_args[0].typ, DecimalType):
                        result_exp = snowpark_args[1] / snowpark_args[0]
                        spark_function_name = (
                            f"({snowpark_arg_names[1]} / {snowpark_arg_names[0]})"
                        )
                    else:
                        result_exp = snowpark_args[0] / snowpark_args[1]
                        spark_function_name = (
                            f"({snowpark_arg_names[0]} / {snowpark_arg_names[1]})"
                        )
                case (t, _NumericType()) if isinstance(t, _AnsiIntervalType):
                    result_type = (
                        YearMonthIntervalType()
                        if isinstance(t, YearMonthIntervalType)
                        else DayTimeIntervalType()
                    )
                    result_exp = snowpark_args[0] / snowpark_args[1]
                case (_NumericType(), _NumericType()):
                    result_type = DoubleType()
                    result_exp = _divnull(
                        snowpark_args[0].cast(result_type),
                        snowpark_args[1].cast(result_type),
                    )
                case _:
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{spark_function_name}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
        case "~":
            spark_function_name = f"~{snowpark_arg_names[0]}"
            if not isinstance(snowpark_typed_args[0].typ, _IntegralType):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 1 requires the "INTEGRAL" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ.simpleString().upper()}".;'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            result_exp = TypedColumn(
                snowpark_fn.bitnot(snowpark_args[0]),
                lambda: snowpark_typed_args[0].types,
            )
        case "<":
            if (
                isinstance(snowpark_typed_args[0].typ, DecimalType)
                and isinstance(snowpark_typed_args[1].typ, BooleanType)
                or isinstance(snowpark_typed_args[0].typ, BooleanType)
                and isinstance(snowpark_typed_args[1].typ, DecimalType)
            ):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{snowpark_arg_names[0]} < {snowpark_arg_names[1]}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").;'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            # Use struct comparison for StructType to handle null field values correctly
            if isinstance(snowpark_typed_args[0].typ, StructType) and isinstance(
                snowpark_typed_args[1].typ, StructType
            ):
                result_exp = TypedColumn(
                    _struct_comparison(
                        snowpark_typed_args[0], snowpark_typed_args[1], "<"
                    ),
                    lambda: [BooleanType()],
                )
            else:
                # Check for interval-string comparisons
                _check_interval_string_comparison(
                    "<", snowpark_typed_args, snowpark_arg_names
                )
                left, right = _coerce_for_comparison(
                    snowpark_typed_args[0], snowpark_typed_args[1]
                )
                result_exp = TypedColumn(left < right, lambda: [BooleanType()])
        case "<=":
            if (
                isinstance(snowpark_typed_args[0].typ, DecimalType)
                and isinstance(snowpark_typed_args[1].typ, BooleanType)
                or isinstance(snowpark_typed_args[0].typ, BooleanType)
                and isinstance(snowpark_typed_args[1].typ, DecimalType)
            ):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{snowpark_arg_names[0]} <= {snowpark_arg_names[1]}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").;'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            # Use struct comparison for StructType to handle null field values correctly
            if isinstance(snowpark_typed_args[0].typ, StructType) and isinstance(
                snowpark_typed_args[1].typ, StructType
            ):
                result_exp = TypedColumn(
                    _struct_comparison(
                        snowpark_typed_args[0], snowpark_typed_args[1], "<="
                    ),
                    lambda: [BooleanType()],
                )
            else:
                # Check for interval-string comparisons
                _check_interval_string_comparison(
                    "<=", snowpark_typed_args, snowpark_arg_names
                )
                left, right = _coerce_for_comparison(
                    snowpark_typed_args[0], snowpark_typed_args[1]
                )
                result_exp = TypedColumn(left <= right, lambda: [BooleanType()])
        case "<=>":
            # eqNullSafe
            rarg_name = snowpark_arg_names[1]
            typ = snowpark_typed_args[1].typ
            if typ == DoubleType() or typ == FloatType():
                if rarg_name == "nan":
                    rarg_name = "NaN"

            spark_function_name = f"({snowpark_arg_names[0]} <=> {rarg_name})"
            left, right = _coerce_for_comparison(
                snowpark_typed_args[0], snowpark_typed_args[1]
            )
            result_exp = TypedColumn(left.eqNullSafe(right), lambda: [BooleanType()])
        case "==" | "=":
            # Check for interval-string comparisons
            _check_interval_string_comparison(
                "=", snowpark_typed_args, snowpark_arg_names
            )
            spark_function_name = f"({snowpark_arg_names[0]} = {snowpark_arg_names[1]})"
            left, right = _coerce_for_comparison(
                snowpark_typed_args[0], snowpark_typed_args[1]
            )
            result_exp = TypedColumn(left == right, lambda: [BooleanType()])
        case ">":
            if (
                isinstance(snowpark_typed_args[0].typ, DecimalType)
                and isinstance(snowpark_typed_args[1].typ, BooleanType)
                or isinstance(snowpark_typed_args[0].typ, BooleanType)
                and isinstance(snowpark_typed_args[1].typ, DecimalType)
            ):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{snowpark_arg_names[0]} > {snowpark_arg_names[1]}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").;'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            # Use struct comparison for StructType to handle null field values correctly
            if isinstance(snowpark_typed_args[0].typ, StructType) and isinstance(
                snowpark_typed_args[1].typ, StructType
            ):
                result_exp = TypedColumn(
                    _struct_comparison(
                        snowpark_typed_args[0], snowpark_typed_args[1], ">"
                    ),
                    lambda: [BooleanType()],
                )
            else:
                # Check for interval-string comparisons
                _check_interval_string_comparison(
                    ">", snowpark_typed_args, snowpark_arg_names
                )
                left, right = _coerce_for_comparison(
                    snowpark_typed_args[0], snowpark_typed_args[1]
                )
                result_exp = TypedColumn(left > right, lambda: [BooleanType()])
        case ">=":
            if (
                isinstance(snowpark_typed_args[0].typ, DecimalType)
                and isinstance(snowpark_typed_args[1].typ, BooleanType)
                or isinstance(snowpark_typed_args[0].typ, BooleanType)
                and isinstance(snowpark_typed_args[1].typ, DecimalType)
            ):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{snowpark_arg_names[0]} >= {snowpark_arg_names[1]}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").;'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            # Use struct comparison for StructType to handle null field values correctly
            if isinstance(snowpark_typed_args[0].typ, StructType) and isinstance(
                snowpark_typed_args[1].typ, StructType
            ):
                result_exp = TypedColumn(
                    _struct_comparison(
                        snowpark_typed_args[0], snowpark_typed_args[1], ">="
                    ),
                    lambda: [BooleanType()],
                )
            else:
                # Check for interval-string comparisons
                _check_interval_string_comparison(
                    ">=", snowpark_typed_args, snowpark_arg_names
                )
                left, right = _coerce_for_comparison(
                    snowpark_typed_args[0], snowpark_typed_args[1]
                )
                result_exp = TypedColumn(left >= right, lambda: [BooleanType()])
        case "&":
            spark_function_name = f"({snowpark_arg_names[0]} & {snowpark_arg_names[1]})"
            result_type = _validate_and_get_bitwise_result_type(
                snowpark_typed_args, spark_function_name
            )
            result_exp = snowpark_args[0].bitwiseAnd(snowpark_args[1])
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "|":
            spark_function_name = f"({snowpark_arg_names[0]} | {snowpark_arg_names[1]})"
            result_type = _validate_and_get_bitwise_result_type(
                snowpark_typed_args, spark_function_name
            )
            result_exp = snowpark_args[0].bitwiseOR(snowpark_args[1])
        case "^":
            spark_function_name = f"({snowpark_arg_names[0]} ^ {snowpark_arg_names[1]})"
            result_type = _validate_and_get_bitwise_result_type(
                snowpark_typed_args, spark_function_name
            )
            result_exp = snowpark_args[0].bitwiseXOR(snowpark_args[1])
        case "abs":
            input_type = snowpark_typed_args[0].typ
            if isinstance(input_type, StringType):
                result_exp = snowpark_fn.abs(
                    snowpark_fn.cast(snowpark_args[0], DoubleType())
                )
                result_type = DoubleType()
            elif isinstance(input_type, _IntegralType):
                result_exp = apply_abs_overflow_with_ansi_check(
                    snowpark_args[0], input_type, spark_sql_ansi_enabled
                )
                result_type = input_type
            else:
                result_exp = snowpark_fn.abs(snowpark_args[0])
                result_type = input_type
        case "acos":
            spark_function_name = f"ACOS({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.when(
                    (snowpark_args[0] < -1) | (snowpark_args[0] > 1), NAN
                ).otherwise(snowpark_fn.acos(snowpark_args[0])),
                lambda: [DoubleType()],
            )
        case "acosh":
            spark_function_name = f"ACOSH({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.when((snowpark_args[0] < 1), NAN).otherwise(
                    snowpark_fn.acosh(snowpark_args[0])
                ),
                lambda: [DoubleType()],
            )
        case "add_months":
            result_exp = TypedColumn(
                _try_to_cast(
                    "try_to_date",
                    snowpark_fn.add_months(
                        snowpark_fn.to_date(snowpark_args[0]), snowpark_args[1]
                    ),
                    snowpark_args[0],
                ),
                lambda: [DateType()],
            )
        case "aes_decrypt":
            result_exp = TypedColumn(
                _aes_helper(
                    "DECRYPT",
                    snowpark_args[0],
                    snowpark_args[1],
                    snowpark_args[4],
                    snowpark_args[2],
                    snowpark_args[3],
                ),
                lambda: [BinaryType()],
            )
        case "aes_encrypt":
            result_exp = TypedColumn(
                _aes_helper(
                    "ENCRYPT",
                    snowpark_args[0],
                    snowpark_args[1],
                    snowpark_args[5],
                    snowpark_args[2],
                    snowpark_args[3],
                ),
                lambda: [BinaryType()],
            )
        case "and":
            spark_function_name = (
                f"({snowpark_arg_names[0]} AND {snowpark_arg_names[1]})"
            )
            result_exp = TypedColumn(
                snowpark_args[0] & snowpark_args[1], lambda: [BooleanType()]
            )
        case "any":
            if not isinstance(snowpark_typed_args[0].typ, (BooleanType, NullType)):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 1 requires the "BOOLEAN" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ.simpleString().upper()}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            result_exp = TypedColumn(
                snowpark_fn.max(snowpark_args[0]),
                lambda: [BooleanType()],
            )
        case "any_value" | "anyvalue":
            match snowpark_args:
                case [col, ignore_nulls_]:
                    result_exp = snowpark_fn.when(
                        ignore_nulls_ == snowpark_fn.lit(True),
                        snowpark_fn.min(col),
                    ).otherwise(snowpark_fn.any_value(col))
                case [col]:
                    result_exp = snowpark_fn.any_value(col)
                case _:
                    exception = ValueError(
                        f"Unexpected number of args for function any_value. Expected 1 or 2, received {len(snowpark_args)}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception

            spark_function_name = f"any_value({snowpark_arg_names[0]})"
            result_exp = TypedColumn(result_exp, lambda: snowpark_typed_args[0].types)
        case "approx_count_distinct":
            match snowpark_args:
                case [data]:
                    result_exp = TypedColumn(
                        snowpark_fn.approx_count_distinct(data),
                        lambda: [LongType()],
                    )
                case [_, _]:
                    exception = SnowparkConnectNotImplementedError(
                        "'rsd' parameter is not supported"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception
        case "approx_percentile" | "percentile_approx":
            # SNOW-1955784: Support accuracy parameter
            # Use percentile_disc to return actual values from dataset (matches PySpark behavior)

            def _pyspark_approx_percentile(column: Column, percentage: float) -> Column:
                """
                PySpark-compatible percentile that returns actual values from dataset.
                - PySpark's approx_percentile returns the "smallest value in the ordered col values
                  such that no more than percentage of col values is less than or equal to that value"
                - This means it MUST return an actual value from the original dataset
                - Snowflake's approx_percentile() may interpolate between values, breaking compatibility
                - percentile_disc() returns discrete values (actual dataset values), matching PySpark
                """
                # Even though the Spark function accepts a Column for percentage, it will fail unless it's a literal.
                # Therefore, we can do error checking right here.
                if not 0.0 <= percentage <= 1.0:
                    exception = AnalysisException(
                        "percentage must be between [0.0, 1.0]"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                result = snowpark_fn.function("percentile_disc")(
                    snowpark_fn.lit(percentage)
                ).within_group(column)
                return result

            column_type = snowpark_typed_args[0].typ

            if isinstance(snowpark_typed_args[1].typ, ArrayType):
                # Snowpark doesn't accept a list of percentile values.
                # This is a workaround to fetch percentile arguments and invoke the snowpark_fn.approx_percentile serially.
                percentile_values = _unwrap_array_literals(
                    exp.unresolved_function.arguments[1]
                )
                percentile_results = [
                    _pyspark_approx_percentile(snowpark_args[0], p)
                    for p in percentile_values
                ]
                result_type = ArrayType(element_type=column_type, contains_null=False)
                result_exp = snowpark_fn.array_construct(*percentile_results)
                result_exp = _resolve_aggregate_exp(result_exp, result_type)
            else:
                # Handle single percentile
                percentage = unwrap_literal(exp.unresolved_function.arguments[1])
                result_exp = _pyspark_approx_percentile(snowpark_args[0], percentage)
                result_exp = _resolve_aggregate_exp(result_exp, column_type)
        case "array":
            if len(snowpark_args) == 0:
                result_exp = snowpark_fn.cast(
                    snowpark_fn.array_construct(), ArrayType(NullType())
                )
                result_type = ArrayType(NullType())
            else:
                arg_types = [t for tc in snowpark_typed_args for t in tc.types]
                if spark_sql_ansi_enabled:
                    element_type = next(
                        (typ for typ in arg_types if not isinstance(typ, NullType)),
                        NullType(),
                    )
                else:
                    element_type = _find_common_type(arg_types)
                coerced_args = []
                for typed_arg, arg_type in zip(snowpark_typed_args, arg_types):
                    col_val = typed_arg.column(to_semi_structure=True)
                    if isinstance(element_type, StringType) and isinstance(
                        arg_type, TimestampType
                    ):
                        col_val = timestamp_to_spark_string(col_val)
                    coerced_args.append(col_val)
                result_exp = snowpark_fn.array_construct(*coerced_args)
                result_exp = TypedColumn(
                    snowpark_fn.cast(result_exp, ArrayType(element_type)),
                    lambda: [ArrayType(element_type)],
                )
                result_type = ArrayType(element_type)
        case "array_append":
            result_exp = TypedColumn(
                snowpark_fn.array_append(snowpark_args[0], snowpark_args[1]),
                lambda: snowpark_typed_args[0].types,
            )
        case "array_compact":
            result_exp = TypedColumn(
                snowpark_fn.array_compact(snowpark_args[0]),
                lambda: snowpark_typed_args[0].types,
            )
        case "array_contains":
            array_type = snowpark_typed_args[0].typ
            if not isinstance(array_type, ArrayType):
                exception = AnalysisException(
                    f"Expected argument '{snowpark_arg_names[0]}' to have an ArrayType."
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            def _compatible_types(type1: DataType, type2: DataType) -> bool:
                if type1 == type2:
                    return True

                if any(
                    isinstance(type1, t) and isinstance(type2, t)
                    for t in [_NumericType, TimestampType, StringType]
                ):
                    return True

                if isinstance(type1, ArrayType) and isinstance(type2, ArrayType):
                    return _compatible_types(type1.element_type, type2.element_type)

                return False

            if not _compatible_types(
                array_type.element_type, snowpark_typed_args[1].typ
            ):
                exception = AnalysisException(
                    '[DATATYPE_MISMATCH.ARRAY_FUNCTION_DIFF_TYPES] Cannot resolve "array_contains(arr, val)" due to data type mismatch: Input to `array_contains` should have been "ARRAY" followed by a value with same element type'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            value = (
                snowpark_fn.cast(snowpark_args[1], array_type.element_type)
                if array_type.structured
                else snowpark_fn.to_variant(snowpark_args[1])
            )

            result_exp = TypedColumn(
                snowpark_fn.array_contains(value, snowpark_args[0]),
                lambda: [BooleanType()],
            )
        case "array_distinct":
            result_exp = TypedColumn(
                snowpark_fn.array_distinct(snowpark_args[0]),
                lambda: snowpark_typed_args[0].types,
            )
        case "array_except":
            result_exp = TypedColumn(
                snowpark_fn.array_except(*snowpark_args),
                lambda: snowpark_typed_args[0].types,
            )
        case "array_insert":
            data = snowpark_args[0]
            spark_index = snowpark_args[1]
            el = snowpark_args[2]

            snow_index = (
                snowpark_fn.when(
                    spark_index < (snowpark_fn.array_size(data) * snowpark_fn.lit(-1)),
                    spark_index + 1,
                )
                .when(spark_index < 0, snowpark_fn.array_size(data) + spark_index + 1)
                # Trigger an exception by using a string instead of an integer.
                .when(
                    spark_index == 0,
                    snowpark_fn.lit(
                        "[snowpark_connect::INVALID_INDEX_OF_ZERO] The index 0 is invalid. An index shall be either < 0 or > 0 (the first element has index 1)."
                    ),
                )
                .otherwise(spark_index - 1)
            )

            input_array_type = snowpark_typed_args[0].types[0]
            array_type_containing_nulls = ArrayType(
                input_array_type.element_type,
                structured=input_array_type.structured,
                contains_null=True,
            )
            if not input_array_type.contains_null:
                # array_insert always returns an array which can contain null regardless of the input
                data = snowpark_fn.cast(data, array_type_containing_nulls)
            result_exp = TypedColumn(
                snowpark_fn.array_insert(data, snow_index, el),
                lambda: [array_type_containing_nulls],
            )
        case "array_intersect":
            result_exp = TypedColumn(
                snowpark_fn.array_intersection(*snowpark_args),
                lambda: snowpark_typed_args[0].types,
            )
        case "array_join":
            match snowpark_args:
                case [data, delimiter]:
                    data = snowpark_fn.cast(data, VariantType())
                    data = snowpark_fn.function("filter")(
                        data, snowpark_fn.sql_expr("x -> x IS NOT NULL")
                    )
                    result_exp = snowpark_fn.array_to_string(data, delimiter)
                case [data, delimiter, _]:
                    null_replacement = unwrap_literal(
                        exp.unresolved_function.arguments[2]
                    )
                    data = snowpark_fn.cast(data, VariantType())
                    data = snowpark_fn.function("transform")(
                        data,
                        snowpark_fn.sql_expr(f"x -> IFNULL(x,'{null_replacement}')"),
                    )
                    result_exp = snowpark_fn.array_to_string(data, delimiter)
                case _:
                    exception = ValueError(
                        f"Invalid number of arguments to {function_name}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            result_exp = TypedColumn(result_exp, lambda: [StringType()])
        case "array_max":
            result_exp = TypedColumn(
                snowpark_fn.array_max(snowpark_args[0]),
                lambda: [snowpark_typed_args[0].typ.element_type],
            )
        case "array_min":
            result_exp = TypedColumn(
                snowpark_fn.array_min(snowpark_args[0]),
                lambda: [snowpark_typed_args[0].typ.element_type],
            )
        case "array_position":
            result_exp = snowpark_fn.when(
                snowpark_fn.is_null(snowpark_args[0])
                | snowpark_fn.is_null(snowpark_args[1]),
                snowpark_fn.lit(None),
            ).otherwise(
                snowpark_fn.coalesce(
                    snowpark_fn.array_position(snowpark_args[1], snowpark_args[0]),
                    snowpark_fn.lit(-1),
                )
                + 1
            )
            result_exp = TypedColumn(result_exp, lambda: [LongType()])
        case "array_prepend":
            result_exp = TypedColumn(
                snowpark_fn.array_prepend(snowpark_args[0], snowpark_args[1]),
                lambda: snowpark_typed_args[0].types,
            )
        case "array_remove":
            array_type = snowpark_typed_args[0].typ
            assert isinstance(
                array_type, ArrayType
            ), f"Expected argument '{snowpark_arg_names[0]}' to have an ArrayType."
            result_exp = snowpark_fn.array_remove(snowpark_args[0], snowpark_args[1])
            if array_type.structured and array_type.element_type is not None:
                result_exp = snowpark_fn.cast(result_exp, array_type)
            result_exp = TypedColumn(result_exp, lambda: snowpark_typed_args[0].types)
        case "array_repeat":
            elem, count = snowpark_args[0], snowpark_args[1]
            elem_type = snowpark_typed_args[0].typ
            result_type = ArrayType(elem_type)

            fallback_to_udf = True

            if isinstance(count._expression, Literal):
                count_value = count._expression.value
                fallback_to_udf = False

                if count_value is None:
                    result_exp = snowpark_fn.lit(None).cast(result_type)
                elif count_value <= 0:
                    result_exp = snowpark_fn.array_construct().cast(result_type)
                elif count_value <= 16:
                    # count_value is small enough to initialize the array directly in memory
                    elem_variant = snowpark_fn.cast(elem, VariantType())
                    result_exp = snowpark_fn.array_construct(
                        *([elem_variant] * count_value)
                    ).cast(result_type)
                else:
                    fallback_to_udf = True

            if fallback_to_udf:

                @cached_udf(
                    input_types=[VariantType(), LongType()],
                    return_type=ArrayType(),
                )
                def _array_repeat(elem, n):
                    if n is None:
                        return None
                    if n < 0:
                        return []
                    return [elem] * n

                elem_variant = snowpark_fn.cast(elem, VariantType())

                result_exp = (
                    snowpark_fn.when(
                        count.is_null(), snowpark_fn.lit(None).cast(result_type)
                    )
                    .when(count <= 0, snowpark_fn.array_construct().cast(result_type))
                    .otherwise(
                        snowpark_fn.cast(
                            _array_repeat(elem_variant, count), result_type
                        )
                    )
                )
        case "array_size":
            # When array_size function is called it utilizes Size class
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/collectionOperations.scala#L166
            # which has dataType = Integer
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/collectionOperations.scala#L115
            result_type = IntegerType()

            array_type = snowpark_typed_args[0].typ
            if isinstance(array_type, NullType):
                result_exp = snowpark_fn.lit(None)
            elif not isinstance(array_type, ArrayType):
                exception = AnalysisException(
                    f"Expected argument '{snowpark_arg_names[0]}' to have an ArrayType."
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            else:
                result_exp = snowpark_fn.array_size(*snowpark_args)
            result_exp = result_exp.cast(result_type)
        case "cardinality":
            # When cardinality function is called it utilizes Size class
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/analysis/FunctionRegistry.scala#L691
            # which has dataType = Integer
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/collectionOperations.scala#L115
            result_type = IntegerType()
            null_value = (
                snowpark_fn.lit(None) if spark_sql_ansi_enabled else snowpark_fn.lit(-1)
            )

            arg_type = snowpark_typed_args[0].typ
            if isinstance(arg_type, NullType):
                result_exp = null_value
            elif isinstance(arg_type, (ArrayType, MapType)):
                result_exp = snowpark_fn.when(
                    snowpark_fn.is_null(*snowpark_args), null_value
                ).otherwise(snowpark_fn.size(*snowpark_args))
            else:
                exception = AnalysisException(
                    f"Expected argument '{snowpark_arg_names[0]}' to have an ArrayType or MapType, but got {arg_type.simpleString()}."
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            result_exp = result_exp.cast(result_type)
        case "array_sort":
            result_exp = TypedColumn(
                snowpark_fn.array_sort(*snowpark_args),
                lambda: snowpark_typed_args[0].types,
            )
        case "array_union":
            result_exp = snowpark_fn.array_distinct(
                snowpark_fn.array_cat(*snowpark_args)
            )
            result_exp = TypedColumn(result_exp, lambda: snowpark_typed_args[0].types)
        case "arrays_overlap":
            array1, array2 = snowpark_args

            array1_is_not_empty = snowpark_fn.array_size(array1) > 0
            array2_is_not_empty = snowpark_fn.array_size(array2) > 0

            array1_contains_nulls = snowpark_fn.array_contains(
                snowpark_fn.lit(None), array1
            )
            array2_contains_nulls = snowpark_fn.array_contains(
                snowpark_fn.lit(None), array2
            )

            filter_function = snowpark_fn.function("FILTER")
            is_not_null_filter = snowpark_fn.sql_expr("x -> x IS NOT NULL")

            array1_no_nulls = filter_function(array1, is_not_null_filter)
            array2_no_nulls = filter_function(array2, is_not_null_filter)

            arrays_overlap = snowpark_fn.arrays_overlap(
                array1_no_nulls, array2_no_nulls
            )

            result_exp = (
                snowpark_fn.when(
                    arrays_overlap == snowpark_fn.lit(True), arrays_overlap
                )
                .when(
                    array1_is_not_empty
                    & array2_is_not_empty
                    & (array1_contains_nulls | array2_contains_nulls),
                    snowpark_fn.lit(None),
                )
                .otherwise(snowpark_fn.lit(False))
            )
            result_exp = TypedColumn(result_exp, lambda: [BooleanType()])
        case "arrays_zip":
            # Snowflake's ARRAYS_ZIP returns struct fields named "$1", "$2", etc.
            # Use TRANSFORM + OBJECT_CONSTRUCT to rename fields, then CAST to structured type.

            # If any argument is NULL, return NULL
            if any(isinstance(ta.typ, NullType) for ta in snowpark_typed_args):
                result_exp = snowpark_fn.lit(None)
                result_type = ArrayType(NullType())
            else:
                array_arg_info = [
                    (name, typed_arg.typ.element_type)
                    for name, typed_arg in zip(snowpark_arg_names, snowpark_typed_args)
                    if isinstance(typed_arg.typ, ArrayType)
                ]

                field_mappings = ", ".join(
                    f"'{name}', elem:\"${i+1}\""
                    for i, name in enumerate([n for n, _ in array_arg_info])
                )
                result_exp = snowpark_fn.arrays_zip(*snowpark_args)
                result_exp = snowpark_fn.function("transform")(
                    result_exp,
                    snowpark_fn.sql_expr(
                        f"elem -> object_construct_keep_null({field_mappings})"
                    ),
                )

                struct_fields = [
                    StructField(name, elem_type, nullable=True)
                    for name, elem_type in array_arg_info
                ]
                result_type = ArrayType(StructType(struct_fields, structured=True))
                result_exp = snowpark_fn.cast(result_exp, result_type)
            result_exp = _type_with_typer(result_exp)
        case "asc":
            result_exp = TypedColumn(
                snowpark_fn.asc(snowpark_args[0]), lambda: snowpark_typed_args[0].types
            )
        case "ascii":
            # Snowflake's ascii function doesn't match PySpark's however the unicode function does.
            unicode_function = snowpark_fn.function("unicode")
            result_exp = unicode_function(snowpark_args[0])
            result_type = IntegerType()
        case "asin":
            spark_function_name = f"ASIN({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                (snowpark_args[0] < -1) | (snowpark_args[0] > 1), NAN
            ).otherwise(snowpark_fn.asin(snowpark_args[0]))
            result_exp = TypedColumn(result_exp, lambda: [DoubleType()])
        case "asinh":
            spark_function_name = f"ASINH({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.asinh(snowpark_args[0]), lambda: [DoubleType()]
            )
        case "assert_true":
            result_type = NullType()
            raise_error = _raise_error_helper(result_type)

            match snowpark_args:
                case [expr]:
                    result_exp = snowpark_fn.when(
                        expr, snowpark_fn.lit(None)
                    ).otherwise(raise_error(snowpark_fn.lit("assertion failed")))
                case [expr, message]:
                    result_exp = snowpark_fn.when(
                        expr, snowpark_fn.lit(None)
                    ).otherwise(raise_error(snowpark_fn.cast(message, StringType())))
                case _:
                    exception = AnalysisException(
                        f"[WRONG_NUM_ARGS.WITHOUT_SUGGESTION] The `assert_true` requires 1 or 2 parameters but the actual number is {len(snowpark_args)}."
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
        case "atan":
            spark_function_name = f"ATAN({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.atan(snowpark_args[0]), lambda: [DoubleType()]
            )
        case "atan2":
            spark_function_name = (
                f"ATAN2({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
            )
            result_exp = TypedColumn(
                snowpark_fn.atan2(snowpark_args[0], snowpark_args[1]),
                lambda: [DoubleType()],
            )
        case "atanh":
            spark_function_name = f"ATANH({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                (snowpark_args[0] < -1) | (snowpark_args[0] > 1), NAN
            ).otherwise(snowpark_fn.atanh(snowpark_args[0]))
            result_exp = TypedColumn(result_exp, lambda: [DoubleType()])
        case "avg" | "mean":
            spark_function_name = f"avg({snowpark_arg_names[0]})"
            input_type = snowpark_typed_args[0].typ
            if isinstance(input_type, DecimalType):
                result_type = _bounded_decimal(
                    input_type.precision + 4, input_type.scale + 4
                )
            else:
                result_type = DoubleType()

            avg_exp = snowpark_fn.avg(snowpark_args[0])
            if (
                isinstance(input_type, DecimalType)
                and result_type.precision - result_type.scale
                < input_type.precision - input_type.scale
            ):
                if is_window_enabled():
                    avg_input = snowpark_args[0]
                    rt = result_type
                    ansi = spark_sql_ansi_enabled

                    def _build_window_avg(window):
                        raw_avg = snowpark_fn.sum(avg_input).over(
                            window
                        ) / snowpark_fn.count(avg_input).over(window)
                        return _cast_with_decimal_overflow_check(raw_avg, rt, ansi)

                    result_exp = TypedColumnWithDeferredWindowBuilder(
                        avg_exp, lambda: [result_type], _build_window_avg
                    )
                else:
                    result_exp = TypedColumn(
                        _cast_with_decimal_overflow_check(
                            avg_exp, result_type, spark_sql_ansi_enabled
                        ),
                        lambda: [result_type],
                    )
            else:
                result_exp = _resolve_aggregate_exp(avg_exp, result_type)
        case "base64":
            # Validate that input is StringType or BinaryType
            input_type = snowpark_typed_args[0].typ
            if not isinstance(input_type, (StringType, BinaryType)):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "base64({snowpark_arg_names[0]})" due to data type mismatch: Parameter 1 requires the "BINARY" type, however "{snowpark_arg_names[0]}" has the type "{input_type.simpleString().upper()}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            base64_encoding_function = snowpark_fn.function("base64_encode")
            result_exp = TypedColumn(
                base64_encoding_function(snowpark_args[0]), lambda: [StringType()]
            )
        case "bin":

            @cached_udf(
                input_types=[VariantType()],
                return_type=StringType(),
            )
            def _to_bin_udf(intval):
                try:
                    intval = int(intval)
                except (ValueError, TypeError):
                    return None

                return format(intval if intval >= 0 else (1 << 64) + intval, "b")

            result_exp = TypedColumn(
                _to_bin_udf(snowpark_fn.cast(snowpark_args[0], VariantType())),
                lambda: [StringType()],
            )
        case "bit_and":
            bit_and_agg_function = snowpark_fn.function("BITAND_AGG")
            result_exp = bit_and_agg_function(snowpark_args[0])
            result_type = _evaluate_bit_operation_result_type(
                snowpark_typed_args[0].typ,
                snowpark_arg_names[0],
                IntegerType(),
                spark_function_name,
            )

        case "bit_count":
            if not isinstance(
                snowpark_typed_args[0].typ, (_IntegralType, BooleanType, NullType)
            ):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 1 requires the ("INTEGRAL" or "BOOLEAN") type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ.simpleString().upper()}"'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            @cached_udf(
                input_types=[VariantType()],
                return_type=LongType(),
            )
            def _bit_count_udf(intval):
                try:
                    return int(intval).bit_count()
                except (ValueError, TypeError):
                    return None

            result_exp = _bit_count_udf(
                snowpark_fn.cast(snowpark_args[0], VariantType())
            )
            result_type = IntegerType()
        case "bit_get" | "getbit":
            snowflake_compat = get_boolean_session_config_param(
                "snowpark.connect.enable_snowflake_extension_behavior"
            )
            col, pos = snowpark_args
            if snowflake_compat:
                result_exp = snowpark_fn.function("GETBIT")(col, pos)
            else:
                raise_error = _raise_error_helper(LongType())
                result_exp = snowpark_fn.when(
                    (snowpark_fn.lit(0) <= pos) & (pos <= snowpark_fn.lit(63))
                    | snowpark_fn.is_null(pos),
                    snowpark_fn.function("GETBIT")(col, pos),
                ).otherwise(
                    raise_error(
                        snowpark_fn.concat(
                            snowpark_fn.lit(
                                "Invalid bit position: ",
                            ),
                            snowpark_fn.cast(
                                pos,
                                StringType(),
                            ),
                            snowpark_fn.lit(
                                " exceeds the bit upper limit",
                            ),
                        )
                    )
                )
            result_type = ByteType()
        case "bit_length":
            bit_length_function = snowpark_fn.function("bit_length")
            result_exp = bit_length_function(snowpark_args[0])
            result_type = IntegerType()
        case "bit_or":
            bit_or_agg_function = snowpark_fn.function("BITOR_AGG")
            result_exp = bit_or_agg_function(snowpark_args[0])
            result_type = _evaluate_bit_operation_result_type(
                snowpark_typed_args[0].typ,
                snowpark_arg_names[0],
                IntegerType(),
                spark_function_name,
            )
        case "bit_xor":
            bit_xor_agg_function = snowpark_fn.function("BITXOR_AGG")
            result_exp = bit_xor_agg_function(snowpark_args[0])
            result_type = _evaluate_bit_operation_result_type(
                snowpark_typed_args[0].typ,
                snowpark_arg_names[0],
                IntegerType(),
                spark_function_name,
            )
        case "bitmap_bit_position":
            arg = snowpark_args[0]

            arg_as_integer = snowpark_fn.when(arg < 0, snowpark_fn.ceil(arg)).otherwise(
                snowpark_fn.floor(arg)
            )

            result_exp = TypedColumn(
                snowpark_fn.bitmap_bit_position(arg_as_integer),
                lambda: [LongType()],
            )
        case "bitmap_bucket_number":
            result_exp = TypedColumn(
                snowpark_fn.bitmap_bucket_number(snowpark_args[0]),
                lambda: [LongType()],
            )
        case "bitmap_construct_agg":

            class BitmapConstructAggUDAF:
                BITMAP_SIZE = 4096

                def __init__(self) -> None:
                    self._bitmap = bytearray(self.BITMAP_SIZE)

                @property
                def aggregate_state(self) -> bytearray:
                    return self._bitmap

                def accumulate(self, bitmap_bit_position: Optional[int]) -> None:
                    if bitmap_bit_position is not None:
                        byte_pos = (bitmap_bit_position >> 3) % self.BITMAP_SIZE
                        bit_pos = 1 << (bitmap_bit_position % 8)
                        self._bitmap[byte_pos] |= bit_pos

                def merge(self, other_bitmap: bytearray) -> None:
                    for i in range(self.BITMAP_SIZE):
                        self._bitmap[i] |= other_bitmap[i]

                def finish(self) -> bytearray:
                    return self._bitmap

            _bitmap_construct_agg_udaf = cached_udaf(
                BitmapConstructAggUDAF,
                input_types=[IntegerType()],
                return_type=BinaryType(),
            )

            result_exp = _bitmap_construct_agg_udaf(snowpark_args[0])
            result_type = BinaryType()
        case "bitmap_count":

            @cached_udf(input_types=[BinaryType()], return_type=LongType())
            def _bitmap_count(bitmap: Optional[bytes]) -> Optional[int]:
                if bitmap is None:
                    return None

                return functools.reduce(
                    lambda acc, el: acc + bin(el).count("1"), list(bitmap), 0
                )

            # Spark returns long type
            # https://github.com/apache/spark/blob/branch-3.5/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/bitmapExpressions.scala#L130
            result_exp = _bitmap_count(snowpark_args[0])
            result_type = LongType()
        case "bitmap_or_agg":

            class BitmapOrAggUDAF:
                BITMAP_SIZE = 4096

                def __init__(self) -> None:
                    self._bitmap = bytearray(self.BITMAP_SIZE)

                @property
                def aggregate_state(self) -> bytearray:
                    return self._bitmap

                def accumulate(self, input_bitmap: Optional[bytes]) -> None:
                    if input_bitmap is not None:
                        input_array = bytearray(input_bitmap)
                        if len(input_array) < self.BITMAP_SIZE:
                            input_array.extend(
                                b"\x00" * (self.BITMAP_SIZE - len(input_array))
                            )

                        for i in range(self.BITMAP_SIZE):
                            self._bitmap[i] |= input_array[i]

                def merge(self, other_bitmap: bytearray) -> None:
                    for i in range(self.BITMAP_SIZE):
                        self._bitmap[i] |= other_bitmap[i]

                def finish(self) -> bytearray:
                    return self._bitmap

            _bitmap_or_agg_udaf = cached_udaf(
                BitmapOrAggUDAF,
                input_types=[BinaryType()],
                return_type=BinaryType(),
            )

            result_exp = _bitmap_or_agg_udaf(snowpark_args[0])
            result_type = BinaryType()
        case "bool_and" | "every":
            if not isinstance(snowpark_typed_args[0].typ, (BooleanType, NullType)):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 1 requires the \'BOOLEAN\' type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ.simpleString().upper()}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            bool_and_agg_function = snowpark_fn.function("booland_agg")
            result_exp = TypedColumn(
                bool_and_agg_function(*snowpark_args), lambda: [BooleanType()]
            )

        case "bool_or" | "some":
            if not isinstance(snowpark_typed_args[0].typ, (BooleanType, NullType)):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 1 requires the "BOOLEAN" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ.simpleString().upper()}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            bool_or_agg_function = snowpark_fn.function("boolor_agg")
            result_exp = TypedColumn(
                bool_or_agg_function(*snowpark_args), lambda: [BooleanType()]
            )
        case "bround":
            # Limitation: overflow exceptions are currently only supported when literals are given to bround
            scale = (
                unwrap_literal(exp.unresolved_function.arguments[1])
                if len(snowpark_args) > 1
                else 0
            )
            if spark_sql_ansi_enabled and (
                len(exp.unresolved_function.arguments) == 2
                and exp.unresolved_function.arguments[0].WhichOneof("expr_type")
                == "literal"
                and exp.unresolved_function.arguments[1].WhichOneof("expr_type")
                == "literal"
            ):

                def local_bround(value, scale):
                    """Local implementation of round for testing if literals would overflow."""
                    return round(
                        Decimal(value, context=Context(rounding=ROUND_HALF_EVEN)), scale
                    )

                if _does_number_overflow(
                    local_bround(
                        snowpark_args[0]._expression.value,
                        snowpark_args[1]._expression.value,
                    ),
                    snowpark_typed_args[0].typ,
                ):
                    exception = ArithmeticException(
                        '[ARITHMETIC_OVERFLOW] Overflow. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                    )
                    attach_custom_error_code(exception, ErrorCodes.ARITHMETIC_ERROR)
                    raise exception

            match snowpark_typed_args[0].typ:
                # https://github.com/apache/spark/blob/15c68493b3690e206f5f5406afb4ad3ce2104b4d/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/mathExpressions.scala#L1504
                case DecimalType(precision=p, scale=s):
                    least_num_digits = p - s + 1
                    if scale < 0:
                        new_precision = max(least_num_digits, -scale + 1)
                        return_type = DecimalType(
                            min(new_precision, DecimalType._MAX_PRECISION), 0
                        )
                    else:
                        new_precision = min(s, scale) + least_num_digits
                        return_type = DecimalType(
                            min(new_precision, DecimalType._MAX_PRECISION),
                            min(s, scale),
                        )
                    result_exp = snowpark_fn.bround(
                        snowpark_args[0], snowpark_fn.lit(scale)
                    ).cast(return_type)
                    result_exp = TypedColumn(result_exp, lambda: [return_type])
                case _:
                    # TODO: Snowflake's bround only supports decimal, not floating point types.
                    # If fixing this in Snowflake takes some time, we should change to use a UDF here for float.
                    # For now, this is just an approximation by casting to Decimal and casting back.
                    scale_for_decimal = 0 if scale < 0 else min(scale + 2, 38)
                    result_exp = snowpark_fn.cast(
                        snowpark_fn.bround(
                            snowpark_fn.to_decimal(
                                snowpark_args[0], 38, scale_for_decimal
                            ),
                            snowpark_fn.lit(scale),
                        ),
                        snowpark_typed_args[0].typ,
                    )
                    result_type = snowpark_typed_args[0].typ
        case "btrim" | "trim":
            args = [
                (
                    _to_char(typed_arg.col)
                    if isinstance(typed_arg.typ, BinaryType)
                    else typed_arg.col
                )
                for typed_arg in snowpark_typed_args
            ]
            result_exp = TypedColumn(snowpark_fn.trim(*args), lambda: [StringType()])
            if len(args) == 2 and function_name == "trim":
                spark_function_name = (
                    f"TRIM(BOTH {snowpark_arg_names[1]} FROM {snowpark_arg_names[0]})"
                )
        case "cbrt":
            spark_function_name = f"CBRT({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                snowpark_args[0] < 0,
                -snowpark_fn.pow(-snowpark_args[0], snowpark_fn.lit(1 / 3)),
            ).otherwise(snowpark_fn.pow(snowpark_args[0], snowpark_fn.lit(1 / 3)))
            result_exp = TypedColumn(result_exp, lambda: [DoubleType()])
        case "ceil" | "ceiling":
            if len(snowpark_args) == 1:
                fn_name = (
                    function_name.upper() if function_name == "ceil" else function_name
                )
                spark_function_name = f"{fn_name}({snowpark_arg_names[0]})"
                result_type = _get_ceil_floor_return_type(snowpark_typed_args[0].typ)
                result_exp = snowpark_fn.cast(
                    snowpark_fn.ceil(snowpark_args[0]), result_type
                )
                match snowpark_typed_args[0].typ:
                    case IntegerType():
                        result_exp = (
                            snowpark_fn.when(
                                snowpark_args[0]
                                > snowpark_fn.lit(MAX_32BIT_SIGNED_INT),
                                snowpark_fn.lit(None),
                            )
                            .when(
                                snowpark_args[0]
                                < snowpark_fn.lit(MIN_32BIT_SIGNED_INT),
                                snowpark_fn.lit(None),
                            )
                            .otherwise(result_exp)
                        )
                    case NullType():
                        result_exp = snowpark_fn.lit(None)
                    case _:
                        result_exp = (
                            snowpark_fn.when(
                                snowpark_args[0] >= snowpark_fn.lit(MAX_INT64),
                                snowpark_fn.lit(MAX_INT64),
                            )
                            .when(
                                snowpark_args[0] <= snowpark_fn.lit(MIN_INT64),
                                snowpark_fn.lit(MIN_INT64),
                            )
                            .otherwise(result_exp)
                        )

                result_exp = TypedColumn(
                    result_exp.cast(result_type), lambda: [result_type]
                )
            elif (
                # Limitation: type exception is currently only supported when literals are given to ceil(ing)
                len(snowpark_args)
                == 2
            ):
                fn_name = function_name.lower()
                if not isinstance(
                    snowpark_typed_args[1].typ, IntegerType
                ) and not isinstance(snowpark_typed_args[1].typ, LongType):
                    exception = AnalysisException(
                        f"The 'scale' parameter of function '{function_name}' needs to be a int literal."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
                spark_function_name = (
                    f"{fn_name}({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
                )

                scale_value = int(snowpark_arg_names[1])
                result_type = _get_ceil_floor_return_type(
                    snowpark_typed_args[0].typ,
                    target_scale=scale_value,
                )
                result_exp = snowpark_fn.ceil(
                    snowpark_args[0] * pow(10.0, snowpark_args[1])
                ) / pow(10.0, snowpark_args[1])
                result_exp = result_exp.cast(result_type)
                result_exp = TypedColumn(result_exp, lambda: [result_type])
            else:
                exception = AnalysisException(
                    f"[WRONG_NUM_ARGS.WITHOUT_SUGGESTION] The `{function_name}` requires 2 parameters but the actual number is {len(snowpark_args)}."
                )
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception
        case "chr" | "char":
            result_exp = snowpark_fn.when(
                (snowpark_args[0] > 256), snowpark_fn.char(snowpark_args[0] % 256)
            ).otherwise(snowpark_fn.char(snowpark_args[0]))
            result_exp = TypedColumn(result_exp, lambda: [StringType()])
        case "coalesce":
            _validate_arity((1, None))
            match len(snowpark_args):
                case 1:
                    result_exp = TypedColumn(
                        snowpark_args[0], lambda: snowpark_typed_args[0].types
                    )
                case _:
                    result_type = _find_common_type(
                        [arg.typ for arg in snowpark_typed_args]
                    )
                    # Skip redundant no-op CASTs when the argument type
                    # already matches the common result type.
                    #
                    # Exception: always cast _IntegralType (LongType,
                    # IntegerType, etc.) because Snowpark's _precision does
                    # not reflect the actual Snowflake column precision.
                    # Example: COUNT() returns NUMBER(18,0) in Snowflake but
                    # Snowpark reports LongType(_precision=19).  Without the
                    # CAST, Snowflake widens COALESCE(NUMBER(38,0),
                    # NUMBER(19,0)) to NUMBER(38,0) instead of the expected
                    # NUMBER(19,0).  The CAST normalises the Snowflake
                    # precision to match Snowpark's type model.
                    coerced_args = [
                        arg
                        if (
                            snowpark_typed_args[i].typ == result_type
                            and not isinstance(result_type, _IntegralType)
                        )
                        else arg.cast(result_type)
                        for i, arg in enumerate(snowpark_args)
                    ]
                    result_exp = snowpark_fn.coalesce(*coerced_args)
        case "collect_list" | "array_agg":
            # TODO: SNOW-1967177 - Support structured types in array_agg
            result_exp = snowpark_fn.array_agg(
                snowpark_typed_args[0].column(to_semi_structure=True)
            )
            result_exp = _resolve_aggregate_exp(
                result_exp, ArrayType(snowpark_typed_args[0].typ)
            )
            spark_function_name = f"collect_list({snowpark_arg_names[0]})"
        case "collect_set":
            # Convert to a semi-structured type. TODO SNOW-1953065 - Support structured types in array_unique_agg.
            result_exp = snowpark_fn.array_unique_agg(
                snowpark_typed_args[0].column(to_semi_structure=True)
            )
            result_exp = _resolve_aggregate_exp(
                result_exp, ArrayType(snowpark_typed_args[0].typ)
            )
        case "concat":
            if len(snowpark_args) == 0:
                result_exp = TypedColumn(snowpark_fn.lit(""), lambda: [StringType()])
            else:
                arg_types = [arg.typ for arg in snowpark_typed_args]
                has_array = any(isinstance(t, ArrayType) for t in arg_types)
                has_non_array = any(not isinstance(t, ArrayType) for t in arg_types)
                if has_array and has_non_array:
                    types_message = " or ".join([f'"{t}"' for t in arg_types])
                    exception = AnalysisException(
                        f"pyspark.errors.exceptions.captured.AnalysisException: [DATATYPE_MISMATCH.DATA_DIFF_TYPES] "
                        f"Cannot resolve expression due to data type mismatch: Input to `{function_name}` should all be the same type, "
                        f"but it's ({types_message})."
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                result_type = _find_common_type(
                    arg_types,
                    func_name=function_name,
                    widen_to_string=True,
                )
                if isinstance(result_type, StringType):
                    snowpark_args = [
                        _decode_column(arg.typ, arg.col) for arg in snowpark_typed_args
                    ]
                elif not isinstance(result_type, BinaryType) and not isinstance(
                    result_type, ArrayType
                ):
                    result_type = StringType()

                if len(snowpark_args) == 1:
                    result_exp = TypedColumn(snowpark_args[0], lambda: [result_type])
                elif isinstance(result_type, ArrayType):
                    result_exp = functools.reduce(
                        lambda acc, tc: snowpark_fn.array_cat(
                            acc, tc.column(to_semi_structure=True)
                        ),
                        snowpark_typed_args[2:],
                        snowpark_fn.array_cat(
                            snowpark_typed_args[0].column(to_semi_structure=True),
                            snowpark_typed_args[1].column(to_semi_structure=True),
                        ),
                    ).cast(result_type)
                else:
                    result_exp = TypedColumn(
                        snowpark_fn.concat(*snowpark_args), lambda: [result_type]
                    )
        case "concat_ws":
            delimiter = unwrap_literal(exp.unresolved_function.arguments[0])
            result_exp = snowpark_fn._concat_ws_ignore_nulls(
                delimiter, *snowpark_args[1:]
            )
            result_exp = TypedColumn(result_exp, lambda: [StringType()])
        case "contains":
            arg1, arg2 = snowpark_args[0], snowpark_args[1]

            if isinstance(snowpark_typed_args[0].typ, BinaryType) != isinstance(
                snowpark_typed_args[1].typ, BinaryType
            ):
                arg1 = (
                    _to_char(arg1)
                    if isinstance(snowpark_typed_args[0].typ, BinaryType)
                    else arg1
                )
                arg2 = (
                    _to_char(arg2)
                    if isinstance(snowpark_typed_args[1].typ, BinaryType)
                    else arg2
                )

            result_exp = TypedColumn(arg1.contains(arg2), lambda: [BooleanType()])
        case "conv":
            # Limitation: overflow exceptions are currently only supported when literals are given to conv
            if (
                spark_sql_ansi_enabled
                and exp.unresolved_function.arguments[0].WhichOneof("expr_type")
                == "literal"
                and exp.unresolved_function.arguments[1].WhichOneof("expr_type")
                == "literal"
            ):
                if _does_number_overflow(
                    Decimal(
                        int(
                            str(snowpark_args[0]._expression.value),
                            int(snowpark_args[1]._expression.value),
                        ),
                    ),
                    ULongLong(),
                ):
                    exception = ArithmeticException(
                        '[ARITHMETIC_OVERFLOW] Overflow in function conv(). If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                    )
                    attach_custom_error_code(exception, ErrorCodes.ARITHMETIC_ERROR)
                    raise exception

            # Check if from_base and to_base are literals for SQL optimization
            from_base_is_literal = (
                exp.unresolved_function.arguments[1].WhichOneof("expr_type")
                == "literal"
            )
            to_base_is_literal = (
                exp.unresolved_function.arguments[2].WhichOneof("expr_type")
                == "literal"
            )

            use_sql_optimization = False
            if from_base_is_literal and to_base_is_literal:
                from_base_val = int(snowpark_args[1]._expression.value)
                to_base_val = int(snowpark_args[2]._expression.value)

                if from_base_val == 10 and to_base_val == 16:
                    # Decimal to Hex: use native SQL TO_VARCHAR with hex format
                    val_col = snowpark_args[0]
                    result_exp = snowpark_fn.iff(
                        snowpark_fn.is_null(val_col),
                        None,
                        snowpark_fn.coalesce(
                            snowpark_fn.ltrim(
                                snowpark_fn.to_varchar(
                                    snowpark_fn.try_cast(snowpark_args[0], LongType()),
                                    "XXXXXXXXXXXXXXXX",
                                ),
                                snowpark_fn.lit(" "),
                            ),
                            snowpark_fn.lit("0"),
                        ),
                    )
                    result_exp = TypedColumn(result_exp, lambda: [StringType()])
                    use_sql_optimization = True
                elif from_base_val == 16 and to_base_val == 10:
                    # Hex to Decimal: use native SQL TO_NUMBER with hex format
                    val_col = snowpark_fn.cast(snowpark_args[0], StringType())
                    result_exp = snowpark_fn.to_varchar(
                        snowpark_fn.iff(
                            snowpark_fn.is_null(val_col),
                            None,
                            snowpark_fn.coalesce(
                                snowpark_fn.function("try_to_number")(
                                    val_col,
                                    snowpark_fn.repeat(
                                        snowpark_fn.lit("X"),
                                        snowpark_fn.length(val_col),
                                    ),
                                ),
                                snowpark_fn.lit("0"),
                            ),
                        )
                    )
                    result_exp = TypedColumn(result_exp, lambda: [StringType()])
                    use_sql_optimization = True

            # Fallback to Python UDF for other bases or non-literal bases
            if not use_sql_optimization:

                @cached_udf(
                    input_types=[
                        StringType(),
                        LongType(),
                        LongType(),
                    ],
                    return_type=StringType(),
                )
                def _to_conv_udf(val, from_base, to_base):
                    try:
                        if val is None:
                            return None
                        num = int(val, base=from_base)
                        if num == 0:
                            return "0"
                        is_negative = num < 0
                        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                        result = ""
                        num = abs(num)
                        while num > 0:
                            result = digits[num % to_base] + result
                            num //= to_base
                        return "-" + result if is_negative else result
                    except (ValueError, TypeError):
                        return "0"

                result_exp = _to_conv_udf(
                    snowpark_fn.cast(snowpark_args[0], StringType()),
                    snowpark_fn.cast(snowpark_args[1], LongType()),
                    snowpark_fn.cast(snowpark_args[2], LongType()),
                )
                result_exp = TypedColumn(result_exp, lambda: [StringType()])

        case "convert_timezone":
            if len(snowpark_args) == 3:
                result_exp = snowpark_fn.convert_timezone(
                    snowpark_args[1], snowpark_args[2], snowpark_args[0]
                )
            else:
                spark_function_name = f"convert_timezone(current_timezone(), {', '.join(snowpark_arg_names)})"
                result_exp = snowpark_fn.convert_timezone(*snowpark_args)

            result_type = TimestampType(TimestampTimeZone.NTZ)
            result_exp = result_exp.cast(result_type)

        case "corr":
            col1_type = snowpark_typed_args[0].typ
            col2_type = snowpark_typed_args[1].typ
            if not isinstance(col1_type, _NumericType) or not isinstance(
                col2_type, _NumericType
            ):
                result_exp = snowpark_fn.corr(
                    snowpark_fn.lit(None), snowpark_fn.lit(None)
                )
            else:
                result_exp = snowpark_fn.corr(*snowpark_args)
            result_exp = TypedColumn(result_exp, lambda: [DoubleType()])
        case "cos":
            spark_function_name = f"COS({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.cos(snowpark_args[0])
            result_exp = TypedColumn(result_exp, lambda: [DoubleType()])
        case "cosh":
            spark_function_name = f"COSH({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.cosh(snowpark_args[0])
            result_exp = TypedColumn(result_exp, lambda: [DoubleType()])
        case "cot":
            spark_function_name = f"COT({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.function("cot")(snowpark_args[0])
            result_exp = TypedColumn(result_exp, lambda: [DoubleType()])
        case "count":
            result_type = LongType()

            if exp.unresolved_function.is_distinct:
                result_exp = snowpark_fn.count_distinct(*snowpark_args)
                spark_function_name = spark_function_name.replace(
                    "count(", "count(DISTINCT ", 1
                )
            else:
                if (
                    exp.unresolved_function.arguments[0].HasField("expression_string")
                    and exp.unresolved_function.arguments[
                        0
                    ].expression_string.expression
                    == "*"
                ) or (
                    exp.unresolved_function.arguments[0].HasField("unresolved_star")
                    and (
                        not exp.unresolved_function.arguments[
                            0
                        ].unresolved_star.HasField("unparsed_target")
                    )
                ):
                    spark_function_name = "count(1)"
                    result_exp = snowpark_fn.count(
                        snowpark_fn.col("*", _is_qualified_name=True)
                    )
                else:
                    result_exp = snowpark_fn.call_function("COUNT", *snowpark_args)
            result_exp = _resolve_aggregate_exp(result_exp, result_type)
        case "count_if":
            result_type = LongType()
            result_exp = snowpark_fn.call_function("COUNT_IF", snowpark_args[0])
            result_exp = _resolve_aggregate_exp(result_exp, result_type)
        case "count_min_sketch":
            _validate_arity(4)

            column, col_name, typed_col = None, None, None
            eps = None
            confidence = None
            seed = None

            def extract_literal_from_column(col):
                """Extract literal value from a Snowpark column"""
                try:
                    return col._expression.value
                except AttributeError:
                    return None

            # Process arguments that can be both named and positional parameters
            number_of_args = len(snowpark_args)
            for i in range(0, number_of_args):
                arg_name = snowpark_arg_names[i]
                arg_value = snowpark_args[i]
                arg_typed_col = snowpark_typed_args[i]

                literal_value = extract_literal_from_column(arg_value)

                if "__column__" in arg_name:
                    col_name = arg_name.split("__column__", 1)[-1]
                    column = arg_value
                    typed_col = arg_typed_col
                elif arg_name == "epsilon":
                    eps = literal_value
                elif arg_name == "confidence":
                    confidence = literal_value
                elif arg_name == "seed":
                    seed = literal_value
                elif i == 0:
                    column = arg_value
                    col_name = arg_name
                    typed_col = arg_typed_col
                elif i == 1:
                    eps = literal_value
                elif i == 2:
                    confidence = literal_value
                elif i == 3:
                    seed = literal_value

            if column is None or eps is None or confidence is None or seed is None:
                exception = ValueError(
                    "The required parameters for count_min_sketch have not been set."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception

            width = math.ceil(2.0 / eps)
            depth = math.ceil(-math.log1p(-confidence) / math.log(2))
            seed = int(seed)

            def _java_random_next_ints(seed_val, count):
                MULTIPLIER = 0x5DEECE66D
                ADDEND = 0xB
                MASK = (1 << 48) - 1
                INT_MAX = (1 << 31) - 1
                state = (seed_val ^ MULTIPLIER) & MASK
                result = []
                for _ in range(count):
                    state = (state * MULTIPLIER + ADDEND) & MASK
                    r = state >> 17
                    while r == INT_MAX:
                        state = (state * MULTIPLIER + ADDEND) & MASK
                        r = state >> 17
                    result.append(r)
                return result

            hash_a = _java_random_next_ints(seed, depth)
            PRIME_MODULUS = (1 << 31) - 1

            class CountMinSketchUDAF:
                def __init__(self) -> None:
                    self.depth = depth
                    self.width = width
                    self.hash_a = hash_a
                    self.table = [[0] * width for _ in range(depth)]
                    self.total_count = 0

                @property
                def aggregate_state(self):
                    return self.table, self.total_count

                def accumulate(self, value):
                    if value is None:
                        return
                    item = int(value)
                    for i in range(self.depth):
                        h = (self.hash_a[i] * item) & 0xFFFFFFFFFFFFFFFF
                        h_signed = h if h < (1 << 63) else h - (1 << 64)
                        h = (h + (h_signed >> 32)) & 0xFFFFFFFFFFFFFFFF
                        h = h & PRIME_MODULUS
                        self.table[i][h % self.width] += 1
                    self.total_count += 1

                def merge(self, other_state):
                    if other_state is None:
                        return
                    other_table, other_count = other_state
                    for i in range(self.depth):
                        for j in range(self.width):
                            self.table[i][j] += other_table[i][j]
                    self.total_count += other_count

                def finish(self):
                    import struct

                    header = struct.pack(
                        ">iqii",
                        1,
                        self.total_count,
                        self.depth,
                        self.width,
                    )
                    hash_values = struct.pack(
                        ">" + "q" * self.depth,
                        *self.hash_a,
                    )
                    table_values = struct.pack(
                        ">" + "q" * (self.depth * self.width),
                        *[v for row in self.table for v in row],
                    )
                    return header + hash_values + table_values

            CountMinSketchUDAF.__name__ = f"CountMinSketchUDAF_{depth}_{width}_{seed}"
            CountMinSketchUDAF.__qualname__ = CountMinSketchUDAF.__name__

            count_min_sketch_udaf = cached_udaf(
                CountMinSketchUDAF,
                return_type=BinaryType(),
                input_types=[typed_col.typ],
            )
            result_exp = count_min_sketch_udaf(column)
            result_type = BinaryType()
            spark_function_name = (
                f"count_min_sketch({col_name}, {eps}, {confidence}, {seed})"
            )
        case "covar_pop":
            col1_type = snowpark_typed_args[0].typ
            col2_type = snowpark_typed_args[1].typ
            if not isinstance(col1_type, _NumericType) or not isinstance(
                col2_type, _NumericType
            ):
                exception = TypeError(
                    f"Data type mismatch: covar_pop requires numeric types, "
                    f"but got {col1_type} and {col2_type}."
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            result_exp = snowpark_fn.covar_pop(
                snowpark_args[0],
                snowpark_args[1],
            )
            result_type = DoubleType()
        case "covar_samp":
            col1_type = snowpark_typed_args[0].typ
            col2_type = snowpark_typed_args[1].typ
            if not isinstance(col1_type, _NumericType) or not isinstance(
                col2_type, _NumericType
            ):
                exception = TypeError(
                    f"Data type mismatch: covar_samp requires numeric types, "
                    f"but got {col1_type} and {col2_type}."
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            result_exp = snowpark_fn.covar_samp(snowpark_args[0], snowpark_args[1])
            result_type = DoubleType()
        case "crc32":
            if (
                not isinstance(snowpark_typed_args[0].typ, BinaryType)
                and not isinstance(snowpark_typed_args[0].typ, StringType)
                and not isinstance(snowpark_typed_args[0].typ, VariantType)
            ):
                exception = AnalysisException(
                    f"[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve crc32({snowpark_args[0]}) due to data type mismatch: Input requires the BINARY type, however {snowpark_args[0]} has the type {snowpark_typed_args[0].typ}."
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            # UDF to calculate the unsigned CRC32 value of data in bytes. Returns the CRC32 value
            # as a 32-bit INT, or None if the input is None.
            @cached_udf(
                input_types=[snowpark_typed_args[0].typ],
                return_type=LongType(),
            )
            def _crc32(data):
                import zlib

                if data is None:
                    return None

                if isinstance(data, bytes) or isinstance(data, bytearray):
                    crc32_value = zlib.crc32(data)
                else:
                    crc32_value = zlib.crc32(data.encode("utf-8"))

                return crc32_value

            result_exp = _crc32(snowpark_args[0])
            result_type = LongType()

        case "csc":
            spark_function_name = f"CSC({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                snowpark_fn.is_null(snowpark_args[0]), snowpark_fn.lit(NAN)
            ).otherwise(
                snowpark_fn.coalesce(
                    _divnull(snowpark_fn.lit(1.0), snowpark_fn.sin(snowpark_args[0])),
                    snowpark_fn.lit(INFINITY),
                )
            )
            # TODO: can we resolve the return type?
            result_exp = _type_with_typer(result_exp)
        case "cume_dist":
            result_exp = TypedColumn(snowpark_fn.cume_dist(), lambda: [DoubleType()])
        case "current_catalog":
            result_exp = snowpark_fn.lit(CURRENT_CATALOG_NAME)
            result_type = StringType()
        case (
            "current_database" | "current_schema"
        ):  # schema is an alias for database in Spark SQL
            result_exp = TypedColumn(
                snowpark_fn.current_schema(), lambda: [StringType()]
            )
            spark_function_name = "current_database()"
        case "current_date" | "curdate":
            if len(snowpark_args) > 0:
                exception = AnalysisException(
                    f"[WRONG_NUM_ARGS.WITHOUT_SUGGESTION] The `{function_name}` requires 0 parameters but the actual number is {len(snowpark_args)}."
                )
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception
            result_exp = TypedColumn(snowpark_fn.current_date(), lambda: [DateType()])
            spark_function_name = "current_date()"
        case "current_timestamp" | "now":
            result_type = TimestampType(TimestampTimeZone.LTZ)
            result_exp = snowpark_fn.to_timestamp_ltz(snowpark_fn.current_timestamp())
        case "current_timezone":
            result_exp = snowpark_fn.lit(global_config.spark_sql_session_timeZone)
            result_type = StringType()
        case "current_user" | "user":
            result_exp = TypedColumn(snowpark_fn.current_user(), lambda: [StringType()])
            spark_function_name = "current_user()"
        case "date_add" | "dateadd":
            if len(snowpark_args) != 2:
                # SQL supports a 3-argument call that gets mapped to timestamp_add -
                # however, if the first argument is invalid, we end up here.
                exception = AnalysisException("date_add takes 2 arguments")
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception
            arg_2 = snowpark_typed_args[1].typ
            if isinstance(arg_2, StringType) and spark_sql_ansi_enabled:
                raise_error = _raise_error_helper(
                    DateType(), error_class=NumberFormatException
                )
                result_exp = snowpark_fn.when(
                    snowpark_fn.cast(snowpark_args[1], IntegerType())
                    == snowpark_args[1],
                    _try_to_cast(
                        "try_to_date",
                        snowpark_fn.cast(
                            snowpark_fn.date_add(*snowpark_args), DateType()
                        ),
                        snowpark_args[0],
                    ),
                ).otherwise(
                    raise_error(
                        snowpark_fn.lit(
                            '[CAST_INVALID_INPUT] The value of the type "STRING" cannot be cast to "INT" because it is malformed. Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                        ),
                    )
                )
            else:
                if isinstance(arg_2, StringType):
                    with suppress(Exception):
                        if str(int(snowpark_arg_names[1])) == snowpark_arg_names[1]:
                            arg_2 = IntegerType()

                if not isinstance(arg_2, (_IntegralType, NullType)):
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "date_add({snowpark_arg_names[0]}, {snowpark_arg_names[1]})" due to data type mismatch: Parameter 2 requires the ("INT" or "SMALLINT" or "TINYINT" or "NULL") type, however "{snowpark_arg_names[1]}" has the type "{str(arg_2)}".'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception

                result_exp = _try_to_cast(
                    "try_to_date",
                    snowpark_fn.cast(snowpark_fn.date_add(*snowpark_args), DateType()),
                    snowpark_args[0],
                )
            result_exp = TypedColumn(result_exp, lambda: [DateType()])
            spark_function_name = (
                f"date_add({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
            )
        case "date_diff" | "datediff":
            if len(snowpark_args) != 2:
                # SQL supports a 3-argument call that gets mapped to timestamp_diff -
                # however, if the first argument is invalid, we end up here.
                exception = AnalysisException("date_diff takes 2 arguments")
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception
            result_col = snowpark_fn.datediff("day", snowpark_args[1], snowpark_args[0])
            if isinstance(
                snowpark_typed_args[0].typ, (DateType, TimeType, TimestampType)
            ) and isinstance(
                snowpark_typed_args[1].typ, (DateType, TimeType, TimestampType)
            ):
                result_exp = result_col
            else:
                result_exp = _try_to_cast(
                    "try_to_date",
                    result_col,
                    snowpark_args[0],
                    snowpark_args[1],
                )
            # Spark 3.5.3: DateDiff defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L2400
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "date_format":
            assert (
                len(exp.unresolved_function.arguments) == 2
            ), "date_format takes 2 arguments"

            # Check if format parameter is NULL
            format_literal = unwrap_literal(exp.unresolved_function.arguments[1])
            if format_literal is None:
                # If format is NULL, return NULL for all rows
                result_exp = snowpark_fn.lit(None)
            else:
                format_lit = snowpark_fn.lit(
                    map_spark_timestamp_format_expression(
                        exp.unresolved_function.arguments[1],
                        snowpark_typed_args[0].typ,
                    )
                )
                result_exp = snowpark_fn.date_format(
                    snowpark_args[0],
                    format_lit,
                )

                if format_literal == "EEEE":
                    # TODO: SNOW-2356874, for weekday, Snowflake only supports abbreviated name, e.g. "Fri". Patch spark "EEEE" until
                    #  snowflake supports full weekday name.
                    result_exp = (
                        snowpark_fn.when(result_exp == "Mon", "Monday")
                        .when(result_exp == "Tue", "Tuesday")
                        .when(result_exp == "Wed", "Wednesday")
                        .when(result_exp == "Thu", "Thursday")
                        .when(result_exp == "Fri", "Friday")
                        .when(result_exp == "Sat", "Saturday")
                        .when(result_exp == "Sun", "Sunday")
                        .otherwise(result_exp)
                    )
            result_exp = TypedColumn(result_exp, lambda: [StringType()])
        case "date_from_unix_date":
            result_exp = snowpark_fn.date_add(
                snowpark_fn.to_date(snowpark_fn.lit("1970-01-01")), snowpark_args[0]
            )
            result_exp = TypedColumn(result_exp, lambda: [DateType()])
        case "date_sub":
            arg_2 = snowpark_typed_args[1].typ
            if isinstance(arg_2, StringType) and spark_sql_ansi_enabled:
                raise_error = _raise_error_helper(
                    DateType(), error_class=NumberFormatException
                )
                result_exp = snowpark_fn.when(
                    snowpark_fn.cast(snowpark_args[1], IntegerType())
                    == snowpark_args[1],
                    _try_to_cast(
                        "try_to_date",
                        snowpark_fn.to_date(
                            snowpark_fn.date_sub(snowpark_args[0], snowpark_args[1])
                        ),
                        snowpark_args[0],
                    ),
                ).otherwise(
                    raise_error(
                        snowpark_fn.lit(
                            '[CAST_INVALID_INPUT] The value of the type "STRING" cannot be cast to "INT" because it is malformed. Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                        ),
                    )
                )
            else:
                if isinstance(arg_2, StringType):
                    with suppress(Exception):
                        if str(int(snowpark_arg_names[1])) == snowpark_arg_names[1]:
                            arg_2 = IntegerType()

                if not isinstance(arg_2, (_IntegralType, NullType)):
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "date_sub({snowpark_arg_names[0]}, {snowpark_arg_names[1]})" due to data type mismatch: Parameter 2 requires the ("INT" or "SMALLINT" or "TINYINT" or "NULL") type, however "{snowpark_arg_names[1]}" has the type "{str(arg_2)}".'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                result_exp = _try_to_cast(
                    "try_to_date",
                    snowpark_fn.to_date(
                        snowpark_fn.date_sub(snowpark_args[0], snowpark_args[1])
                    ),
                    snowpark_args[0],
                )
            result_exp = TypedColumn(result_exp, lambda: [DateType()])
            spark_function_name = (
                f"date_sub({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
            )
        case "date_trunc":
            date_part = unwrap_literal(exp.unresolved_function.arguments[0]).lower()

            allowed_date_parts = {
                "year",
                "yyyy",
                "yy",
                "month",
                "mon",
                "mm",
                "day",
                "dd",
                "microsecond",
                "millisecond",
                "second",
                "minute",
                "hour",
                "week",
                "quarter",
            }

            truncated_date = (
                snowpark_fn.date_trunc(
                    date_part, snowpark_fn.to_timestamp(snowpark_args[1])
                )
                if date_part in allowed_date_parts
                else snowpark_fn.lit(None)
            )

            result_exp = _try_to_cast(
                "try_to_date",
                snowpark_fn.cast(
                    truncated_date,
                    TimestampType(),
                ),
                snowpark_args[1],
            )

            result_type = TimestampType()
        case "dayofmonth" | "day":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.dayofmonth(
                    snowpark_fn.builtin("try_to_date")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.dayofmonth(
                    snowpark_fn.to_date(snowpark_args[0])
                )
            # Spark 3.5.3: DayOfMonth extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "dayofweek":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.dayofweek(
                    snowpark_fn.builtin("try_to_date")(snowpark_args[0])
                ) + snowpark_fn.lit(1)
            else:
                result_exp = snowpark_fn.dayofweek(
                    snowpark_fn.to_date(snowpark_args[0])
                ) + snowpark_fn.lit(1)
            # Spark 3.5.3: DayOfWeek extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "dayofyear":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.dayofyear(
                    snowpark_fn.builtin("try_to_date")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.dayofyear(
                    snowpark_fn.to_date(snowpark_args[0])
                )
            # Spark 3.5.3: DayOfYear extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "date_part" | "datepart" | "extract":
            field_lit: str | None = unwrap_literal(exp.unresolved_function.arguments[0])

            if field_lit is None:
                result_exp = snowpark_fn.lit(None)
                result_type = DoubleType()
            else:
                field_lit = field_lit.lower()
                result_exp = snowpark_fn.date_part(field_lit, snowpark_args[1])

                # Determine the source type to apply correct return types
                source_type = snowpark_typed_args[1].typ

                # Validate field compatibility with interval types
                # YearMonthIntervalType can only extract: YEAR, MONTH
                if isinstance(source_type, YearMonthIntervalType):
                    if field_lit not in _YEAR_FIELDS + _MONTH_FIELDS:
                        exception = AnalysisException(
                            f'[INVALID_EXTRACT_FIELD] Cannot extract `{field_lit.upper()}` from "{snowpark_arg_names[1]}".'
                        )
                        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                        raise exception
                # DayTimeIntervalType can only extract: DAY, HOUR, MINUTE, SECOND
                elif isinstance(source_type, DayTimeIntervalType):
                    if (
                        field_lit
                        not in _DAY_FIELDS
                        + _HOUR_FIELDS
                        + _MINUTE_FIELDS
                        + _SECOND_FIELDS
                    ):
                        exception = AnalysisException(
                            f'[INVALID_EXTRACT_FIELD] Cannot extract `{field_lit.upper()}` from "{snowpark_arg_names[1]}".'
                        )
                        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                        raise exception

                # Spark 3.5.3: DatePart.parseExtractField delegates to GetDateField/GetTimeField expressions
                # which define dataType = IntegerType (except SECOND which uses DecimalType(8,6))
                # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L2783
                result_type = IntegerType()

                # Special handling for dayofweek: adjust from Snowflake's 0-6 to Spark's 1-7
                if field_lit in _DAYOFWEEK_FIELDS:
                    result_exp += 1

                if field_lit in _SECOND_FIELDS:
                    result_type = DecimalType(8, 6)
                    s_part = snowpark_fn.cast(result_exp, DoubleType())
                    ns_part = snowpark_fn.cast(
                        snowpark_fn.date_part("ns", snowpark_args[1]), DoubleType()
                    )
                    result_exp = s_part + (ns_part / snowpark_fn.lit(1e9))

                # Interval-specific: MONTH, HOUR, MINUTE return ByteType (not IntegerType as is in Date/Timestamp)
                # See https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/intervalExpressions.scala
                if isinstance(
                    source_type, (YearMonthIntervalType, DayTimeIntervalType)
                ):
                    if field_lit in _MONTH_FIELDS + _HOUR_FIELDS + _MINUTE_FIELDS:
                        result_type = ByteType()

                result_exp = snowpark_fn.cast(result_exp, result_type)

            if function_name in ("datepart", "extract"):
                spark_function_name = f"{function_name}({snowpark_arg_names[0]} FROM {snowpark_arg_names[1]})"
        case "decode":
            result_exp = _decode_column(snowpark_typed_args[0].typ, *snowpark_args)
            result_type = StringType()
        case "degrees":
            spark_function_name = f"DEGREES({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.degrees(snowpark_args[0])
            result_type = DoubleType()
        case "dense_rank":
            result_exp = snowpark_fn.dense_rank()
            # IntegerType per Spark's DenseRank case class which extends AggregateWindowFunction, which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/34d9413ca161f4531544565976a46c6da7d371cd/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/windowExpressions.scala#L626
            result_exp = _resolve_aggregate_exp(result_exp, IntegerType())
        case "desc":
            result_exp = TypedColumn(
                snowpark_fn.desc(snowpark_args[0]), lambda: snowpark_typed_args[0].types
            )
        case "div":
            # Only called from SQL, either as `a div b` or `div(a, b)`
            # Convert it into `(a - a % b) / b`.
            if isinstance(snowpark_typed_args[0].typ, YearMonthIntervalType):
                if isinstance(snowpark_typed_args[1].typ, YearMonthIntervalType):
                    dividend_total = _calculate_total_months(snowpark_args[0])
                    divisor_total = _calculate_total_months(snowpark_args[1])

                    # Handle division by zero interval
                    if not spark_sql_ansi_enabled:
                        result_exp = snowpark_fn.when(
                            divisor_total == 0, snowpark_fn.lit(None)
                        ).otherwise(snowpark_fn.trunc(dividend_total / divisor_total))
                    else:
                        result_exp = snowpark_fn.trunc(dividend_total / divisor_total)
                    result_type = LongType()
                else:
                    raise AnalysisException(
                        f"""[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "({snowpark_arg_names[0]} div {snowpark_arg_names[1]})" due to data type mismatch: the left and right operands of the binary operator have incompatible types ({snowpark_typed_args[0].typ} and {snowpark_typed_args[1].typ}).;"""
                    )
            elif isinstance(snowpark_typed_args[0].typ, DayTimeIntervalType):
                if isinstance(snowpark_typed_args[1].typ, DayTimeIntervalType):
                    dividend_total = _calculate_total_seconds(snowpark_args[0])
                    divisor_total = _calculate_total_seconds(snowpark_args[1])

                    # Handle division by zero interval
                    if not spark_sql_ansi_enabled:
                        result_exp = snowpark_fn.when(
                            divisor_total == 0, snowpark_fn.lit(None)
                        ).otherwise(snowpark_fn.trunc(dividend_total / divisor_total))
                    else:
                        result_exp = snowpark_fn.trunc(dividend_total / divisor_total)
                    result_type = LongType()
                else:
                    raise AnalysisException(
                        f"""[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "({snowpark_arg_names[0]} div {snowpark_arg_names[1]})" due to data type mismatch: the left and right operands of the binary operator have incompatible types ({snowpark_typed_args[0].typ} and {snowpark_typed_args[1].typ}).;"""
                    )
            else:
                result_exp = snowpark_fn.cast(
                    (snowpark_args[0] - snowpark_args[0] % snowpark_args[1])
                    / snowpark_args[1],
                    LongType(),
                )
                if not spark_sql_ansi_enabled:
                    result_exp = snowpark_fn.when(
                        snowpark_args[1] == 0, snowpark_fn.lit(None)
                    ).otherwise(result_exp)
                result_type = LongType()
        case "e":
            spark_function_name = "E()"
            result_type = DoubleType()
            result_exp = snowpark_fn.lit(math.e, datatype=result_type)
        case "element_at":
            spark_index = snowpark_args[1]
            data = snowpark_typed_args[0].col
            typ = snowpark_typed_args[0].typ
            match typ:
                case ArrayType():
                    result_type = typ.element_type
                    # Convert Spark 1-based index to Snowflake 0-based index
                    # Trigger an exception by using a string instead of an integer when index == 0
                    snow_index = (
                        snowpark_fn.when(
                            spark_index < 0,
                            snowpark_fn.array_size(data) + spark_index,
                        )
                        .when(
                            spark_index == 0,
                            snowpark_fn.lit(
                                "[snowpark_connect::invalid_index_of_zero] The index 0 is invalid. An index shall be either < 0 or > 0 (the first element has index 1)."
                            ),
                        )
                        .otherwise(spark_index - 1)
                    )
                    result_exp = snowpark_fn.element_at(data, snow_index)
                case MapType():
                    result_exp = snowpark_fn.element_at(data, spark_index)
                    result_type = typ.value_type
                case _:
                    exception = SnowparkConnectNotImplementedError(
                        f"Unsupported type {typ} for element_at function"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception
        case "elt":
            n = snowpark_args[0]
            values = snowpark_fn.array_construct(*snowpark_args[1:])

            if spark_sql_ansi_enabled:
                raise_error = _raise_error_helper(
                    StringType(), error_class=ArrayIndexOutOfBoundsException
                )
                values_size = snowpark_fn.lit(len(snowpark_args) - 1)

                result_exp = (
                    snowpark_fn.when(snowpark_fn.is_null(n), snowpark_fn.lit(None))
                    .when(
                        (snowpark_fn.lit(1) <= n) & (n <= values_size),
                        snowpark_fn.cast(
                            snowpark_fn.get(
                                values, snowpark_fn.nvl(n - 1, snowpark_fn.lit(0))
                            ),
                            StringType(),
                        ),
                    )
                    .otherwise(
                        raise_error(
                            snowpark_fn.lit("[INVALID_ARRAY_INDEX] The index "),
                            snowpark_fn.cast(n, StringType()),
                            snowpark_fn.lit(" is out of bounds."),
                        )
                    )
                )
            else:
                result_exp = snowpark_fn.when(
                    snowpark_fn.is_null(n), snowpark_fn.lit(None)
                ).otherwise(
                    snowpark_fn.get(values, snowpark_fn.nvl(n - 1, snowpark_fn.lit(0)))
                )

            result_exp = snowpark_fn.cast(result_exp, StringType())
            result_type = StringType()
        case "encode":

            @cached_udf(
                input_types=[StringType(), StringType()],
                return_type=BinaryType(),
            )
            def _encode(s: str, f: str):
                if None in (s, f):
                    return None
                if f.lower() == "utf-16":
                    return (b"\xfe\xff" if s else b"") + s.encode("utf-16be")
                return s.encode(f)

            result_exp = _encode(*snowpark_args)
            result_type = BinaryType()
        case "endswith":
            result_exp = snowpark_args[0].endswith(snowpark_args[1])
            result_type = BooleanType()
        case "equal_null":
            result_exp = snowpark_fn.equal_null(*snowpark_args)
            result_type = BooleanType()
        case "exp":
            spark_function_name = f"EXP({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.exp(*snowpark_args)
            result_type = DoubleType()
        case "explode" | "explode_outer":
            input_type = snowpark_typed_args[0].typ
            fn = (
                snowpark_fn.explode
                if function_name == "explode"
                else snowpark_fn.explode_outer
            )
            match input_type:
                case ArrayType():
                    spark_col_names = ["col"]
                    result_type = input_type.element_type
                    result_exp = fn(snowpark_args[0])
                case _:
                    # Check if the type has map-like attributes before accessing them
                    if hasattr(input_type, "key_type") and hasattr(
                        input_type, "value_type"
                    ):
                        spark_col_names = ["key", "value"]
                        result_exp = fn(snowpark_args[0])
                        result_type = [input_type.key_type, input_type.value_type]
                    else:
                        # Throw proper error for types without key_type/value_type attributes
                        exception = AnalysisException(
                            f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{function_name}({snowpark_arg_names[0]})" due to data type mismatch: Parameter 1 requires the ("ARRAY" or "MAP") type, however "{snowpark_arg_names[0]}" has the type "{str(input_type)}".'
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
        case "expm1":
            spark_function_name = f"EXPM1({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.exp(*snowpark_args) - 1
            result_type = DoubleType()
        case "factorial":
            arg = snowpark_args[0]

            # For floating-point types, truncate by casting to LongType first
            if isinstance(snowpark_typed_args[0].typ, _FractionalType):
                arg = snowpark_fn.floor(arg)

            result_exp = snowpark_fn.when(
                (arg >= snowpark_fn.lit(0)) & (arg <= snowpark_fn.lit(20)),
                snowpark_fn.factorial(arg),
            ).otherwise(snowpark_fn.lit(None))

            result_type = LongType()
        case "find_in_set":
            element_sep = snowpark_fn.lit(",")
            array = snowpark_fn.cast(
                snowpark_fn.split(snowpark_args[1], element_sep),
                ArrayType(StringType()),
            )

            result_exp = snowpark_fn.when(
                snowpark_fn.contains(snowpark_args[0], snowpark_fn.lit(",")),
                snowpark_fn.lit(None),
            ).otherwise(snowpark_fn.array_position(snowpark_args[0], array))

            any_arg_is_null = snowpark_args[0].is_null() | snowpark_args[1].is_null()

            result_exp = snowpark_fn.when(
                any_arg_is_null, snowpark_fn.lit(None)
            ).otherwise(
                snowpark_fn.call_function(
                    "nvl2", result_exp, result_exp + 1, snowpark_fn.lit(0)
                )
            )
            # Spark 3.5.3: FindInSet defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/stringExpressions.scala#L969
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "first" | "first_value":
            if not is_window_enabled():
                # AGGREGATE CONTEXT: NON-DETERMINISTIC BEHAVIOR
                # When first() is used as an aggregate function (without window/ORDER BY),
                # it exhibits non-deterministic behavior - returns "any value it sees first" from each group.
                # This is explicitly documented in PySpark as non-deterministic behavior.

                # According to PySpark docs, ignore_nulls can be a Column - but it doesn't make sense and doesn't work.
                # So assume it's a literal.
                args = exp.unresolved_function.arguments
                ignore_nulls = unwrap_literal(args[1]) if len(args) > 1 else False

                # Since first() is non-deterministic and just returns "some value" from the group,
                # ANY_VALUE is the perfect match for this behavior
                if ignore_nulls:
                    # TODO(SNOW-1955766): When ignoring nulls, we need to completely exclude null values from aggregation
                    # Since Snowflake's ANY_VALUE doesn't support ignore_nulls parameter yet (SNOW-1955766),
                    # we fall back to MIN() which naturally ignores nulls and gives us "some value" from the group
                    # This is semantically equivalent to first(..., ignore_nulls=True) for non-deterministic behavior
                    result_exp = snowpark_fn.min(snowpark_args[0])
                else:
                    result_exp = snowpark_fn.any_value(snowpark_args[0])

                spark_function_name = f"{function_name}({snowpark_arg_names[0]})"
            else:
                # WINDOW CONTEXT: DETERMINISTIC BEHAVIOR
                # When first() is used as a window function with ORDER BY,
                # it exhibits deterministic behavior - returns the first value according to the specified ordering.
                # This delegates to first_value() window function which is deterministic.
                result_exp = _resolve_first_value(exp, snowpark_args)
            result_exp = TypedColumn(result_exp, lambda: snowpark_typed_args[0].types)
        case "flatten":
            # SNOW-1890247 - Update this when SQL provides a structured version of flatten
            result_exp = snowpark_fn.cast(
                snowpark_fn.array_flatten(
                    snowpark_fn.cast(snowpark_args[0], VariantType())
                ),
                snowpark_typed_args[0].typ.element_type,
            )
            # TODO: do we need to resolve integral types to LongType?
            result_type = snowpark_typed_args[0].typ.element_type
        case "floor":
            if len(snowpark_args) == 1:
                spark_function_name = f"FLOOR({snowpark_arg_names[0]})"
                result_type = _get_ceil_floor_return_type(snowpark_typed_args[0].typ)
                if isinstance(snowpark_typed_args[0].typ, DecimalType):
                    result_exp = snowpark_fn.cast(
                        snowpark_fn.floor(snowpark_args[0]), result_type
                    )
                else:
                    typ = snowpark_typed_args[0].typ
                    if isinstance(typ, (_FractionalType, StringType)):
                        try_to_cast_to_double = snowpark_fn.try_cast(
                            snowpark_args[0], DoubleType()
                        )
                        base_expression = _bounded_long_floor_expr(
                            try_to_cast_to_double
                        )
                        # Handle NaN: result is 0
                        result_exp = snowpark_fn.when(
                            snowpark_fn.equal_nan(try_to_cast_to_double),
                            snowpark_fn.lit(0),
                        ).otherwise(base_expression)
                    else:
                        base_expression = _bounded_long_floor_expr(snowpark_args[0])
                        result_exp = base_expression
                result_exp = TypedColumn(
                    result_exp.cast(result_type), lambda: [result_type]
                )
            elif len(snowpark_args) == 2:
                if not isinstance(
                    snowpark_typed_args[1].typ, IntegerType
                ) and not isinstance(snowpark_typed_args[1].typ, LongType):
                    exception = AnalysisException(
                        "The 'scale' parameter of function 'floor' needs to be a int literal."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
                spark_function_name = (
                    f"floor({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
                )

                scale_value = int(snowpark_arg_names[1])
                result_type = _get_ceil_floor_return_type(
                    snowpark_typed_args[0].typ,
                    target_scale=scale_value,
                )
                result_exp = snowpark_fn.floor(
                    snowpark_args[0] * pow(10.0, snowpark_args[1])
                ) / pow(10.0, snowpark_args[1])
                result_exp = result_exp.cast(result_type)
                if scale_value <= 0:
                    result_exp = TypedColumn(result_exp, lambda: [result_type])
                else:
                    result_exp = TypedColumn(result_exp, lambda: [result_type])
            else:
                exception = AnalysisException(
                    f"[WRONG_NUM_ARGS.WITHOUT_SUGGESTION] The `floor` requires 2 parameters but the actual number is {len(snowpark_args)}."
                )
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception
        case "format_number":
            col, scale = snowpark_args
            col_type = snowpark_typed_args[0].typ
            scale_type = snowpark_typed_args[1].typ

            if not isinstance(col_type, _NumericType):
                exception = TypeError(
                    f'Data type mismatch: Parameter 1 of format_number requires  the "NUMERIC" type, however was {col_type}.'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            if not isinstance(scale_type, (_IntegralType, StringType)):
                exception = TypeError(
                    f'Parameter 2 requires the ("INT" or "STRING") type, however "{scale}" has the type "{scale_type}"'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            if not isinstance(col_type, DecimalType):
                col = col.cast(DecimalType(38, 18))
                input_scale = 18

            else:
                input_scale = col_type.scale

            # If scale is a string, call the Java UDF for string pattern format
            # to match Spark's behavior
            if isinstance(scale_type, StringType):
                format_number_udf = register_cached_java_udf(
                    "com.snowflake.snowpark_connect.udfs.FormatNumberUdf.format_number",
                    ["STRING", "STRING"],
                    "STRING",
                    packages=["com.snowflake:snowpark:1.15.0"],
                )

                result_exp = format_number_udf(col.cast(StringType()), scale)
            else:
                # Optimized path for literal numeric scale values
                # This path doesn't use snowpark_fn to determine format pattern as
                # we can unpack the literal value and use it directly.
                if exp.unresolved_function.arguments[1].HasField("literal"):
                    unwrapped_scale = unwrap_literal(
                        exp.unresolved_function.arguments[1]
                    )
                    to_fill_with_zeros = unwrapped_scale - input_scale
                    scale_value = min(unwrapped_scale, input_scale)

                    if scale_value < 0:
                        result_exp = snowpark_fn.lit(None)
                    else:
                        rounded_col = snowpark_fn.call_function(
                            "ROUND",
                            col,
                            snowpark_fn.lit(scale_value),
                            snowpark_fn.lit("HALF_TO_EVEN"),
                        )

                        if scale_value <= 0:
                            format_pattern = NUMBER_FORMAT_DIGITS
                        else:
                            num_chars_to_left_strip = (
                                scale_value + (scale_value + 1) // 3
                            )
                            format_pattern = (
                                NUMBER_FORMAT_DIGITS[num_chars_to_left_strip:]
                                + "."
                                + "0" * scale_value
                            )

                        formatted = snowpark_fn.ltrim(
                            snowpark_fn.to_varchar(rounded_col, format_pattern)
                        )

                        if to_fill_with_zeros > 0:
                            result_exp = snowpark_fn.concat(
                                formatted, snowpark_fn.lit("0" * to_fill_with_zeros)
                            )
                        else:
                            result_exp = formatted

                # If second argument is numeric column, we need to use snowpark_fn to determine format pattern
                else:
                    to_fill_with_zeros = scale - snowpark_fn.lit(input_scale)

                    capped_scale = snowpark_fn.least(
                        scale,
                        snowpark_fn.lit(input_scale),
                    )

                    rounded_col = snowpark_fn.call_function(
                        "ROUND",
                        col,
                        capped_scale,
                        snowpark_fn.lit("HALF_TO_EVEN"),
                    )

                    num_chars_to_left_strip = capped_scale + snowpark_fn.floor(
                        (capped_scale + snowpark_fn.lit(1)) / snowpark_fn.lit(3)
                    )

                    nines_part = snowpark_fn.substring(
                        snowpark_fn.lit(NUMBER_FORMAT_DIGITS),
                        num_chars_to_left_strip + snowpark_fn.lit(1),
                        snowpark_fn.lit(
                            len(NUMBER_FORMAT_DIGITS) - num_chars_to_left_strip
                        ),
                    )

                    format_pattern = snowpark_fn.when(
                        capped_scale > 0,
                        snowpark_fn.concat(
                            nines_part,
                            snowpark_fn.lit("."),
                            snowpark_fn.repeat(snowpark_fn.lit("0"), capped_scale),
                        ),
                    ).otherwise(nines_part)

                    formatted = snowpark_fn.ltrim(
                        snowpark_fn.to_varchar(rounded_col, format_pattern)
                    )

                    # Append zeros if needed
                    formatted_with_zeros = snowpark_fn.when(
                        to_fill_with_zeros > 0,
                        snowpark_fn.concat(
                            formatted,
                            snowpark_fn.repeat(
                                snowpark_fn.lit("0"), to_fill_with_zeros
                            ),
                        ),
                    ).otherwise(formatted)

                    # Handle negative scale (should return NULL)
                    result_exp = snowpark_fn.when(
                        scale < 0, snowpark_fn.lit(None)
                    ).otherwise(formatted_with_zeros)

            if isinstance(col_type, (FloatType, DoubleType)):
                result_exp = snowpark_fn.when(
                    snowpark_fn.equal_nan(snowpark_args[0]),
                    snowpark_fn.lit("NaN"),
                ).otherwise(result_exp)

            result_type = StringType()
        case "format_string" | "printf":

            @cached_udf(
                input_types=[StringType(), ArrayType()],
                return_type=StringType(),
            )
            def _format_string(fmt: str, args: list) -> Optional[str]:
                mapped_args = map(lambda x: "null" if x is None else x, args)

                try:
                    return fmt % tuple(mapped_args)
                except TypeError:
                    return None

            result_exp = _format_string(
                snowpark_args[0], snowpark_fn.array_construct(*snowpark_args[1:])
            )
            result_type = StringType()
        case "from_csv":
            snowpark_args = [
                typed_arg.column(to_semi_structure=True)
                for typed_arg in snowpark_typed_args
            ]

            @cached_udf(
                return_type=VariantType(),
                input_types=[StringType(), StringType(), StructType()],
            )
            def _from_csv(csv_data: str, schema: str, options: Optional[dict]):
                if csv_data is None:
                    return None

                if csv_data == "":
                    # Return dict with None values for empty string
                    schemas = schema.split(",")
                    results = {}
                    for sc in schemas:
                        parts = [i for i in sc.split(" ") if len(i) != 0]
                        assert len(parts) == 2, f"{sc} is not a valid schema"
                        results[parts[0]] = None
                    return results

                max_chars_per_column = -1
                sep = ","

                python_to_snowflake_type = {
                    "str": "STRING",
                    "bool": "BOOLEAN",
                    "dict": "OBJECT",
                    "list": "ARRAY",
                }

                if options is not None:
                    if not isinstance(options, dict):
                        raise TypeError(
                            "[snowpark_connect::invalid_input] [INVALID_OPTIONS.NON_MAP_FUNCTION] Invalid options: Must use the `map()` function for options."
                        )

                    max_chars_per_column = options.get(
                        "maxCharsPerColumn", max_chars_per_column
                    )
                    max_chars_per_column = int(max_chars_per_column)
                    sep = options.get("sep", sep)
                    for k, v in options.items():
                        if not isinstance(k, str) or not isinstance(v, str):
                            k_type = python_to_snowflake_type.get(
                                type(k).__name__, type(k).__name__.upper()
                            )
                            v_type = python_to_snowflake_type.get(
                                type(v).__name__, type(v).__name__.upper()
                            )
                            raise TypeError(
                                f'[snowpark_connect::type_mismatch] [INVALID_OPTIONS.NON_STRING_TYPE] Invalid options: A type of keys and values in `map()` must be string, but got "MAP<{k_type}, {v_type}>".'
                            )

                csv_data = csv_data.split(sep)
                schemas = schema.split(",")
                assert len(csv_data) == len(
                    schemas
                ), "length of data and schema mismatch"

                def _parse_one_schema(sc):
                    parts = [i for i in sc.split(" ") if len(i) != 0]
                    assert len(parts) == 2, f"{sc} is not a valid schema"
                    return parts[0], parts[1]

                results = {}
                for i in range(len(csv_data)):
                    alias, datatype = _parse_one_schema(schemas[i])
                    results[alias] = csv_data[i]
                    if (
                        max_chars_per_column != -1
                        and len(str(csv_data[i])) > max_chars_per_column
                    ):
                        raise ValueError(
                            f"[snowpark_connect::invalid_input] Max chars per column exceeded {max_chars_per_column}: {str(csv_data[i])}"
                        )

                return results

            spark_function_name = f"from_csv({snowpark_arg_names[0]})"
            result_type = map_type_string_to_snowpark_type(snowpark_arg_names[1])

            if len(snowpark_arg_names) > 2 and snowpark_arg_names[2].startswith(
                "named_struct"
            ):
                exception = TypeError(
                    "[INVALID_OPTIONS.NON_MAP_FUNCTION] Invalid options: Must use the `map()` function for options."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception

            match snowpark_args:
                case [csv_data, schemas]:
                    csv_result = _from_csv(
                        snowpark_fn.cast(csv_data, StringType()),
                        schemas,
                        snowpark_fn.lit(None),
                    )
                case [csv_data, schemas, options]:
                    csv_result = _from_csv(
                        snowpark_fn.cast(csv_data, StringType()), schemas, options
                    )
                case _:
                    exception = ValueError("Unrecognized from_csv parameters")
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception

            result_exp = snowpark_fn.when(
                snowpark_args[0].is_null(), snowpark_fn.lit(None)
            ).otherwise(snowpark_fn.cast(csv_result, result_type))
        case "from_json":
            # TODO: support options parameter.
            # The options map (e.g., map('timestampFormat', 'dd/MM/yyyy')) is validated
            # but not currently used. To implement:
            # 1. Extract options from snowpark_args[2]
            # 2. Pass format options to JSON parsing/coercion logic
            # 3. Apply custom formats when casting timestamp/date fields
            if len(snowpark_args) > 2:
                if not isinstance(snowpark_typed_args[2].typ, MapType):
                    exception = AnalysisException(
                        "[INVALID_OPTIONS.NON_MAP_FUNCTION] Invalid options: Must use the `map()` function for options."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
                if not isinstance(
                    snowpark_typed_args[2].typ.key_type, StringType
                ) or not isinstance(snowpark_typed_args[2].typ.value_type, StringType):
                    exception = AnalysisException(
                        f"""[INVALID_OPTIONS.NON_STRING_TYPE] Invalid options: A type of keys and values in `map()` must be string, but got "{snowpark_typed_args[2].typ.simpleString().upper()}"."""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception

            spark_function_name = f"from_json({snowpark_arg_names[0]})"
            lit_schema = unwrap_literal(exp.unresolved_function.arguments[1])

            try:
                spark_schema = _parse_datatype_json_string(lit_schema)
                result_type = map_pyspark_types_to_snowpark_types(spark_schema)
            except ValueError as e:
                # it's valid to fall into here in some cases, so only logger.debug not logger.error
                logger.debug("Failed to parse datatype json string: %s", e)
                result_type = map_type_string_to_snowpark_type(lit_schema)

            # Validate that all MapTypes in the schema have StringType keys.
            # JSON specification only supports string keys, so from_json cannot parse
            # into MapType with non-string keys (e.g., IntegerType, LongType).
            # Spark enforces this and raises INVALID_JSON_MAP_KEY_TYPE error.
            def _validate_map_key_types(data_type: DataType) -> None:
                """Recursively validate that all MapType instances have StringType keys."""
                if isinstance(data_type, MapType):
                    if not isinstance(data_type.key_type, StringType):
                        exception = AnalysisException(
                            f"[INVALID_JSON_MAP_KEY_TYPE] Input schema {lit_schema} can only contain STRING as a key type for a MAP."
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
                    # Check the value type recursively
                    _validate_map_key_types(data_type.value_type)
                elif isinstance(data_type, ArrayType):
                    _validate_map_key_types(data_type.element_type)
                elif isinstance(data_type, StructType):
                    for field in data_type.fields:
                        _validate_map_key_types(field.datatype)

            _validate_map_key_types(result_type)

            # if the result is a map, the column is named "entries"
            if isinstance(result_type, MapType):
                spark_function_name = "entries"

            # TODO(SNOW-3122222) TODO Remove the legacy `else` branch once 10.6 is fully rolled out
            if session._has_structured_try_cast:
                expr = snowpark_args[0]._expression
                # TODO(SNOW-3083544): Snowpark does not yet support the PERMISSIVE flag, so we need to manually perform SQL resolution here.
                if isinstance(expr, Literal):
                    # The `Literal` class does not support generation through _expression.sql, so we need to add a special case for it.
                    arg_sql = to_sql(expr.value, expr.datatype)
                else:
                    arg_sql = session._analyzer.analyze(expr, defaultdict())
                # If the original element is NULL, the result of the cast will also be NULL.
                # Schema checking of fields (dropping extra fields, NULLing missing fields) is handled by the server.
                sf_type = convert_sp_to_sf_type(result_type)
                result_exp = snowpark_fn.sql_expr(
                    f"TRY_CAST(TRY_PARSE_JSON({arg_sql}) AS {sf_type} PERMISSIVE)"
                )
                if isinstance(result_type, StructType):
                    # If the top-level expected return type is a struct, Spark will implicitly retain nulls for all fields.
                    # The top-level return of the TRY_CAST will only be NULL if the input was a scalar, so we handle this case by doing
                    # a dummy TRY_CAST on an empty object.
                    result_exp = snowpark_fn.ifnull(
                        result_exp,
                        snowpark_fn.sql_expr(
                            f"TRY_CAST(OBJECT_CONSTRUCT() AS {sf_type} PERMISSIVE)"
                        ),
                    )
                if isinstance(result_type, ArrayType) and isinstance(
                    result_type.element_type, StructType
                ):
                    result_exp = snowpark_fn.ifnull(
                        result_exp,
                        # If the top-level expected return type is an array, Spark will implicitly wrap a scalar value if the type matches.
                        snowpark_fn.sql_expr(
                            f"TRY_CAST(TO_ARRAY(TRY_PARSE_JSON({arg_sql})) AS {sf_type} PERMISSIVE)"
                        ),
                    )
            else:
                # try to parse first, since spark returns null for invalid json
                result_exp = snowpark_fn.call_function(
                    "try_parse_json", snowpark_args[0]
                )

                # Check if the original input is NULL - if so, return NULL for the entire result
                original_input_is_null = snowpark_args[0].is_null()

                # helper function to make sure we have the expected array element type
                def _element_type_matches(
                    array_exp: Column, element_type: DataType
                ) -> Column:
                    if isinstance(element_type, StructType) or isinstance(
                        element_type, MapType
                    ):
                        # we need to confirm that all elements are objects, we don't care about the schema here
                        return snowpark_fn.call_function(
                            "reduce",
                            array_exp,
                            snowpark_fn.lit(True),
                            snowpark_fn.sql_expr(
                                "(acc, e) -> acc and (strip_null_value(e) is null or is_object(e))"
                            ),
                        )

                    if isinstance(element_type, ArrayType):
                        # we need to recursively go down and check nested arrays
                        # then bubble up the result
                        analyzer = Session.get_active_session()._analyzer
                        fn_sql = analyzer.analyze(
                            _element_type_matches(
                                snowpark_fn.col("x"), element_type.element_type
                            )._expression,
                            defaultdict(),
                        )

                        return snowpark_fn.call_function(
                            "reduce",
                            snowpark_fn.call_function(
                                "transform",
                                array_exp,
                                snowpark_fn.sql_expr(
                                    f"x -> (strip_null_value(x) is null or is_array(x)) and {fn_sql}"
                                ),
                            ),
                            snowpark_fn.lit(True),
                            snowpark_fn.sql_expr("(acc, e) -> acc and nvl(e, true)"),
                        )

                    # let's optimistically assume that any simple type can be coerced to the expected type automatically
                    return snowpark_fn.lit(True)

                # Snowflake limitation: Casting semi-structured data to structured types fails
                # if the source doesn't have the exact "shape" (e.g., missing struct fields).
                # This function constructs an expression that coerces the parsed JSON to match
                # the expected type structure, filling in NULLs for missing fields.
                #
                # For complex types (StructType, ArrayType, MapType), this recursively ensures
                # nested structures match the schema. For MapType with complex values, it uses
                # a pure SQL REDUCE approach to avoid UDF-in-lambda errors.
                def _coerce_to_type(
                    exp: Column, t: DataType, top_level: bool = True
                ) -> Column:
                    if isinstance(t, StructType):
                        key_values = []
                        for field in t.fields:
                            key_values.append(snowpark_fn.lit(field.name))
                            key_values.append(
                                _coerce_to_type(
                                    snowpark_fn.get(exp, snowpark_fn.lit(field.name)),
                                    field.datatype,
                                    False,
                                )
                            )
                        # spark will not return null for top level structs, so we need to handle that
                        if top_level:
                            return snowpark_fn.object_construct_keep_null(*key_values)
                        else:
                            return snowpark_fn.when(
                                snowpark_fn.as_object(exp).is_null(),
                                snowpark_fn.lit(None),
                            ).otherwise(
                                snowpark_fn.object_construct_keep_null(*key_values)
                            )
                    elif isinstance(t, ArrayType):
                        # Handle array wrapping behavior for top-level structs
                        if top_level and isinstance(t.element_type, StructType):
                            # Spark can wrap a single value in an array if the element type is a struct
                            arr_exp = snowpark_fn.to_array(exp)
                        else:
                            # For other types, return null for non-array values
                            arr_exp = snowpark_fn.as_array(exp)

                        # Get coercion SQL for the array element type using placeholder column "x"
                        analyzer = Session.get_active_session()._analyzer
                        fn_sql = analyzer.analyze(
                            _coerce_to_type(
                                snowpark_fn.col("x"), t.element_type, False
                            )._expression,
                            defaultdict(),
                        )

                        # Apply TRANSFORM to coerce each element, or return null if types don't match
                        return snowpark_fn.when(
                            _element_type_matches(arr_exp, t.element_type),
                            snowpark_fn.call_function(
                                "transform",
                                arr_exp,
                                snowpark_fn.sql_expr(f"x -> {fn_sql}"),
                            ),
                        ).otherwise(snowpark_fn.lit(None))
                    elif isinstance(t, MapType):
                        obj_exp = snowpark_fn.as_object(exp)

                        # If value type is simple (no nested complex types), no coercion needed
                        if not isinstance(
                            t.value_type, (StructType, ArrayType, MapType)
                        ):
                            return obj_exp

                        # For maps with complex value types, we need to coerce each value.
                        # Strategy: Use pure SQL REDUCE with stateful accumulator to avoid:
                        # 1. UDF-in-lambda errors (which break nested maps)
                        # 2. Column scoping issues (outer columns aren't accessible in lambdas)
                        #
                        # The state is a 2-element array: [result_map, original_map]
                        # This allows the lambda to access the original map's values while building the result.

                        analyzer = Session.get_active_session()._analyzer

                        # Get the coercion SQL for the value type using a placeholder column
                        fn_sql = analyzer.analyze(
                            _coerce_to_type(
                                snowpark_fn.col("v"), t.value_type, False
                            )._expression,
                            defaultdict(),
                        )

                        # Replace placeholder "V" with reference to original map via state array
                        # In lambda: state[1] = original_map, k = current_key
                        fn_sql_with_value = fn_sql.replace(
                            '"V"', "strip_null_value(GET(state[1], k))"
                        )

                        # Build REDUCE lambda: (state, k) -> [updated_result, original_map]
                        lambda_expr = (
                            f"(state, k) -> ARRAY_CONSTRUCT("
                            f"object_insert(state[0], k, ({fn_sql_with_value})::variant, true), "
                            f"state[1])"
                        )

                        # Execute REDUCE with initial state = [{}, original_map]
                        reduce_result = snowpark_fn.call_function(
                            "reduce",
                            snowpark_fn.call_function("object_keys", obj_exp),
                            snowpark_fn.array_construct(
                                snowpark_fn.object_construct(),  # state[0]: empty result map
                                obj_exp,  # state[1]: original map
                            ),
                            snowpark_fn.sql_expr(lambda_expr),
                        )

                        # Extract the result map (state[0]) from the final state
                        return snowpark_fn.get(reduce_result, snowpark_fn.lit(0))
                    else:
                        return snowpark_fn.try_cast(snowpark_fn.to_varchar(exp), t)

                # Apply the coercion to handle invalid JSON (creates struct with NULL fields)
                coerced_exp = _coerce_to_type(result_exp, result_type)

                # If the original input was NULL, return NULL instead of a struct
                result_exp = snowpark_fn.when(
                    original_input_is_null, snowpark_fn.lit(None)
                ).otherwise(snowpark_fn.cast(coerced_exp, result_type))

        case "from_unixtime":

            def raise_analysis_exception(
                input_arg_name,
                input_arg_type: DataType,
                format: str = "yyyy-MM-dd HH:mm:ss",
            ):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "from_unixtime({input_arg_name}, {format})" due to data type mismatch: Parameter 1 requires the "BIGINT" type, however "{input_arg_name}" has the type "{input_arg_type}"'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            # Strip decimal part of the number to ensure proper result after calling snowflake counterparts
            match snowpark_typed_args[0].typ:
                case _FractionalType():
                    unix_time = snowpark_fn.cast(
                        snowpark_fn.trunc(snowpark_args[0]), IntegerType()
                    )
                case StringType():
                    unix_time = snowpark_fn.cast(
                        snowpark_fn.function("try_to_number")(
                            snowpark_fn.regexp_replace(snowpark_args[0], r"\..*$", "")
                        ),
                        IntegerType(),
                    )
                case _:
                    unix_time = snowpark_args[0]
            time_format = (
                IntegerType()
                if isinstance(snowpark_typed_args[0].typ, (_FractionalType, StringType))
                else snowpark_typed_args[0].typ
            )
            match exp.unresolved_function.arguments:
                case [_]:
                    if not isinstance(
                        snowpark_typed_args[0].typ, (_NumericType, StringType)
                    ):
                        raise_analysis_exception(
                            snowpark_arg_names[0], snowpark_typed_args[0].typ
                        )

                    result_exp = snowpark_fn.to_char(
                        _try_to_cast(
                            "try_to_timestamp",
                            snowpark_fn.to_timestamp(unix_time),
                            unix_time,
                        ),
                        snowpark_fn.lit("YYYY-MM-DD HH24:MI:SS"),
                    )
                    spark_function_name = (
                        f"from_unixtime({snowpark_arg_names[0]}, yyyy-MM-dd HH:mm:ss)"
                    )
                case [_, _]:
                    try:
                        timestamp_format = map_spark_timestamp_format_expression(
                            exp.unresolved_function.arguments[1],
                            time_format,
                        )
                        if not isinstance(
                            snowpark_typed_args[0].typ, (_NumericType, StringType)
                        ):
                            raise_analysis_exception(
                                snowpark_arg_names[0],
                                snowpark_typed_args[0].typ,
                                timestamp_format,
                            )

                        result_exp = snowpark_fn.to_char(
                            _try_to_cast(
                                "try_to_timestamp",
                                snowpark_fn.to_timestamp(unix_time),
                                unix_time,
                            ),
                            timestamp_format,
                        )
                    except AnalysisException as e:
                        attach_custom_error_code(e, ErrorCodes.INVALID_INPUT)
                        raise e
                    except Exception:
                        # The second argument must either be a string or none. It can't be a column.
                        # So if it's anything that isn't a literal, we catch the error and just return NULL
                        result_exp = snowpark_fn.lit(None)
                case _:
                    exception = AnalysisException(
                        f"[WRONG_NUM_ARGS.WITHOUT_SUGGESTION] The `from_unixtime` requires [1, 2] parameters but the actual number is {len(snowpark_args)}."
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            result_type = StringType()
        case "from_utc_timestamp":
            target_tz = _map_from_spark_tz(snowpark_args[1])
            result_exp = _try_to_cast(
                "try_to_timestamp",
                snowpark_fn.from_utc_timestamp(snowpark_args[0], target_tz).cast(
                    TimestampType()
                ),
                snowpark_args[0],
            )
            result_type = TimestampType()
        case "get":
            if exp.unresolved_function.arguments[1].HasField("literal"):
                index = unwrap_literal(exp.unresolved_function.arguments[1])
                if index < 0:
                    result_exp = snowpark_fn.lit(None)
                else:
                    result_exp = snowpark_fn.get(*snowpark_args)
            else:
                result_exp = snowpark_fn.when(
                    snowpark_args[1] < 0,
                    snowpark_fn.lit(None),
                ).otherwise(snowpark_fn.get(*snowpark_args))
            result_exp = TypedColumn(
                result_exp, lambda: [snowpark_typed_args[0].typ.element_type]
            )
        case "get_json_object":
            json_str = snowpark_args[0]
            json_path = unwrap_literal(exp.unresolved_function.arguments[1])

            def _extract_json_path(col_: Column, path_: str) -> Column:
                """
                TRY_PARSE_JSON + GET_PATH: parses JSON once instead of twice (CHECK_JSON + JSON_EXTRACT_PATH_TEXT).
                """

                parsed = snowpark_fn.try_parse_json(col_)
                extracted = snowpark_fn.get_path(parsed, snowpark_fn.lit(path_))

                return extracted.cast(StringType())

            if not json_path:
                result_exp = snowpark_fn.lit(None)
            else:
                path_start_with_dollar_dot = False
                # Snowflake JSON paths do not start with '$.', which is required in Spark
                if json_path.startswith("$."):
                    json_path = json_path[2:]
                    path_start_with_dollar_dot = True
                elif json_path.startswith("$["):
                    # Special case: $[d] (bracket notation at root level)
                    # Example: $[0] from ["a","b","c"] should return "a"
                    json_path = json_path[1:]  # Remove just the $, keep the [
                elif json_path == "$":
                    json_path = ""

                # Spark behavior: $.0 (dot notation with digit) returns NULL
                # But $[0] (bracket notation) should work for array access
                if path_start_with_dollar_dot and json_path and json_path[0].isdigit():
                    match = re.match(r"^(\d+)($|\.|\[)", json_path)
                    if match:
                        result_exp = snowpark_fn.lit(None)
                    else:
                        result_exp = _extract_json_path(json_str, json_path)
                else:
                    result_exp = _extract_json_path(json_str, json_path)
            result_type = StringType()
        case "greatest":
            all_structs = all(
                isinstance(a.typ, StructType) for a in snowpark_typed_args
            )
            if all_structs:
                # For struct types, we need to use struct comparison with null as smallest
                # Implement pairwise comparison to find the greatest
                result = snowpark_typed_args[0]
                for i in range(1, len(snowpark_typed_args)):
                    current_arg = snowpark_typed_args[i]
                    # If current_arg > result (with null as smallest), use current_arg
                    is_greater = _struct_comparison(current_arg, result, ">")
                    result = TypedColumn(
                        snowpark_fn.when(is_greater, current_arg.col).otherwise(
                            result.col
                        ),
                        lambda r=result: r.types,
                    )
                result_exp = result
            else:
                greatest_ignore_nulls = snowpark_fn.function("greatest_ignore_nulls")
                result_exp = greatest_ignore_nulls(*snowpark_args)
                result_exp = TypedColumn(
                    result_exp,
                    lambda: [_find_common_type([a.typ for a in snowpark_typed_args])],
                )
        case "grouping" | "grouping_id":
            # grouping_id is not an alias for grouping in PySpark, but Snowflake's implementation handles both
            current_grouping_cols = get_current_grouping_columns()
            if function_name == "grouping_id":
                if not snowpark_args:
                    # grouping_id() with empty args means use all grouping columns
                    spark_function_name = "grouping_id()"
                    snowpark_args = [
                        column_mapping.get_snowpark_column_name_from_spark_column_name(
                            spark_col
                        )
                        for spark_col in current_grouping_cols
                    ]
                else:
                    # Verify that grouping arguments match current grouping columns
                    spark_col_args = [
                        column_mapping.get_spark_column_name_from_snowpark_column_name(
                            sp_col.getName()
                        )
                        for sp_col in snowpark_args
                    ]
                    if current_grouping_cols != spark_col_args:
                        exception = AnalysisException(
                            f"[GROUPING_ID_COLUMN_MISMATCH] Columns of grouping_id: {spark_col_args} doesnt match "
                            f"Grouping columns: {current_grouping_cols}"
                        )
                        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
                        raise exception
            if function_name == "grouping_id":
                result_exp = snowpark_fn.grouping_id(*snowpark_args)
                # Spark 3.5.3: GroupingID.dataType defaults to LongType (config-dependent)
                # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/grouping.scala#L265
                result_type = LongType()
            else:
                result_exp = snowpark_fn.grouping(*snowpark_args)
                # Spark 3.5.3: Grouping defines dataType = ByteType
                # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/grouping.scala#L213
                result_type = ByteType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "hash":
            # TODO: See the spark-compatibility-issues.md explanation, this is quite different from Spark.
            # MapType columns as input should raise an exception as they are not hashable.
            snowflake_compat = get_boolean_session_config_param(
                "snowpark.connect.enable_snowflake_extension_behavior"
            )
            # Snowflake's hash function does allow MAP types, but Spark does not. Therefore, if we have the expansion flag enabled
            # we want to let it pass through and hash MAP types.
            # Also allow if the legacy config spark.sql.legacy.allowHashOnMapType is set to true
            if not snowflake_compat and not spark_sql_legacy_allow_hash_on_map_type:
                for arg in snowpark_typed_args:
                    if any(isinstance(t, MapType) for t in arg.types):
                        exception = AnalysisException(
                            '[DATATYPE_MISMATCH.HASH_MAP_TYPE] Cannot resolve "hash(value)" due to data type mismatch: '
                            'Input to the function `hash` cannot contain elements of the "MAP" type. '
                            'In Spark, same maps may have different hashcode, thus hash expressions are prohibited on "MAP" elements. '
                            'To restore previous behavior set "spark.sql.legacy.allowHashOnMapType" to "true".'
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
            result_exp = snowpark_fn.hash(*snowpark_args)
            # Spark 3.5.3: Murmur3Hash defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/hash.scala#L617
            result_type = IntegerType()
            # Spark returns a 32bit value when Snowflakes hash generates 64bit. We have to perform integral overflow to ensure that the value is within the range.
            result_exp = apply_integral_overflow(result_exp, result_type, force=True)
        case "hex":
            data = snowpark_fn.cast(snowpark_args[0], VariantType())

            # We need as many 'X' as there are digits. The longest possible 'long' type has 16 digits.
            format_string = "FMXXXXXXXXXXXXXXXX"

            # Hex supports string, binary, integer/long.
            # We can use TO_CHAR for numbers and HEX_ENCODE for string and binary
            result_exp = (
                snowpark_fn.when(
                    snowpark_fn.is_integer(data),
                    snowpark_fn.to_char(
                        # The cast to integer is done because to_char in snowflake doesn't take
                        # two arguments for certain other types.
                        snowpark_fn.cast(data, LongType()),
                        format_string,
                    ),
                )
                .when(
                    snowpark_fn.is_double(data),
                    snowpark_fn.to_char(
                        # While float/double aren't officially supported in the spark documentation, they work.
                        # They are treated as integer, but after floor.
                        snowpark_fn.cast(snowpark_fn.floor(data), LongType()),
                        format_string,
                    ),
                )
                .otherwise(snowpark_fn.function("HEX_ENCODE")(*snowpark_args))
            )
            result_type = StringType()
        case "histogram_numeric":
            aggregate_input_typ = snowpark_typed_args[0].typ

            if isinstance(aggregate_input_typ, DecimalType):
                # mimic bug from Spark 3.5.3.
                # In 3.5.5 it's fixed and this exception shouldn't be thrown
                exception = ValueError(
                    "class org.apache.spark.sql.types.Decimal cannot be cast to class java.lang.Number (org.apache.spark.sql.types.Decimal is in unnamed module of loader 'app'; java.lang.Number is in module java.base of loader 'bootstrap')"
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
                raise exception

            histogram_return_type = ArrayType(
                StructType(
                    [
                        StructField("x", aggregate_input_typ, _is_column=False),
                        StructField("y", DoubleType(), _is_column=False),
                    ]
                )
            )

            class HistogramNumericUDAF:
                """
                Most of the code was taken from Spark implementation: https://github.com/apache/spark/blob/master/sql/catalyst/src/main/java/org/apache/spark/sql/util/NumericHistogram.java#L36
                This UDAF is executed on multiple nodes, we have no control over the order of execution, hence there
                will be differences between Spark and Snowflake implementations. Function creates approximation so the
                result should be either way good enough.
                """

                def __init__(self) -> None:

                    # init the RNG for breaking ties in histogram merging. A fixed seed is specified here
                    # to aid testing, but can be eliminated to use a time-based seed (which would
                    # make the algorithm non-deterministic).
                    self.random_seed = (31183 ^ 0x5DEECE66D) & ((1 << 48) - 1)
                    self.random_multiplier = 0x5DEECE66D
                    self.random_addend = 0xB
                    self.random_mask = (1 << 48) - 1
                    self.n_bins = 0
                    self.n_used_bins = 0
                    self.bins = []
                    self.typ = None

                @property
                def aggregate_state(self):
                    return (self.n_bins, self.n_used_bins, self.bins, self.typ)

                def accumulate(self, value, n_bins: int):
                    if self.n_bins == 0:
                        self.n_bins = n_bins
                        self.bins = []
                        self.n_used_bins = 0

                    if value is None:
                        return

                    self.typ = type(value)
                    parsed_value = self.parse_value(value)

                    self.add(parsed_value)

                def parse_value(self, value):
                    """
                    Converts input value into the proper numeric type so that algorithm can be executed.
                    Supported Snowflake types are:
                    * DATE
                    * NUMBER
                    * FLOAT
                    * TIMESTAMP_LTZ
                    * TIMESTAMP_NTZ
                    * TIMESTAMP_TZ
                    All these types are supported in the spark function histogram_numeric.
                    """

                    parsed_value = 0.0
                    if isinstance(value, datetime.datetime):
                        parsed_value = value.timestamp()
                    elif isinstance(value, datetime.date):
                        epoch = datetime.date(1970, 1, 1)
                        delta = value - epoch
                        parsed_value = delta.days
                    elif isinstance(value, (int, float)):
                        parsed_value = value
                    elif isinstance(value, Decimal):
                        parsed_value = float(value)
                    return parsed_value

                def finish(self):
                    return [
                        {"x": self.map_output(bin[0]), "y": bin[1]} for bin in self.bins
                    ]

                def map_output(self, value):
                    if self.typ == datetime.datetime:
                        return datetime.datetime.fromtimestamp(value)
                    elif self.typ == datetime.date:
                        epoch = datetime.date(1970, 1, 1)
                        delta = datetime.timedelta(days=value)
                        return epoch + delta
                    elif self.typ == int:
                        return int(value)
                    elif self.typ == float:
                        return float(value)
                    elif self.typ == Decimal:
                        return Decimal(value)
                    else:
                        return None

                def _next(self, bits: int) -> int:
                    self.random_seed = (
                        self.random_seed * self.random_multiplier + self.random_addend
                    ) & self.random_mask
                    return self.random_seed >> (48 - bits)

                def _next_double(self) -> float:
                    a = self._next(26)
                    b = self._next(27)
                    return ((a << 27) + b) / float(1 << 53)

                def merge(self, other: tuple):
                    if other is None:
                        return

                    o_n_bins, o_n_used_bins, other_bins, o_typ = other

                    if self.typ is None:
                        self.typ = o_typ

                    if self.n_bins == 0 or self.n_used_bins == 0:
                        self.n_bins = o_n_bins
                        self.n_used_bins = o_n_used_bins
                        self.bins = [(o_bin[0], o_bin[1]) for o_bin in other_bins]
                    else:
                        tmp_bins = [(s_bin[0], s_bin[1]) for s_bin in self.bins]
                        tmp_bins.extend((o_bin[0], o_bin[1]) for o_bin in other_bins)
                        tmp_bins.sort(
                            key=lambda x: (x[0] is not None, math.isnan(x[0]), x[0])
                        )
                        self.bins = tmp_bins
                        self.n_used_bins += o_n_used_bins
                        self.trim()

                def add(self, v):
                    """
                    Adds a new data point to the histogram approximation. Make sure you have
                    called either allocate() or merge() first. This method implements Algorithm #1
                    from Ben-Haim and Tom-Tov, "A Streaming Parallel Decision Tree Algorithm", JMLR 2010.
                    """

                    # Binary search to find the closest bucket that v should go into.
                    # 'bin' should be interpreted as the bin to shift right in order to accomodate
                    # v. As a result, bin is in the range [0,N], where N means that the value v is
                    # greater than all the N bins currently in the histogram. It is also possible that
                    # a bucket centered at 'v' already exists, so this must be checked in the next step.
                    bin = 0
                    left, right = 0, self.n_used_bins
                    while left < right:
                        bin = (left + right) // 2
                        if self.bins[bin][0] > v:
                            right = bin
                        elif self.bins[bin][0] < v:
                            left = bin + 1
                        else:
                            break

                    # If we found an exact bin match for value v, then just increment that bin's count.
                    # Otherwise, we need to insert a new bin and trim the resulting histogram back to size.
                    # A possible optimization here might be to set some threshold under which 'v' is just
                    # assumed to be equal to the closest bin -- if fabs(v-bins[bin].x) < THRESHOLD, then
                    # just increment 'bin'. This is not done now because we don't want to make any
                    # assumptions about the range of numeric data being analyzed.
                    if bin < self.n_used_bins and self.bins[bin][0] == v:
                        bin_x, bin_y = self.bins[bin]
                        self.bins[bin] = (bin_x, bin_y + 1)
                    else:
                        self.bins.insert(bin + 1, (v, 1.0))
                        self.n_used_bins += 1
                        if self.n_used_bins > self.n_bins:
                            # Trim the bins down to the correct number of bins.
                            self.trim()

                def trim(self):
                    """
                    Trims a histogram down to 'nbins' bins by iteratively merging the closest bins.
                    If two pairs of bins are equally close to each other, decide uniformly at random which
                    pair to merge, based on a PRNG.
                    """
                    while self.n_used_bins > self.n_bins:
                        # Find the closest pair of bins in terms of x coordinates. Break ties randomly.
                        smallest_diff = self.bins[1][0] - self.bins[0][0]
                        smallest_loc = 0
                        count = 1

                        for i in range(1, self.n_used_bins - 1):
                            diff = self.bins[i + 1][0] - self.bins[i][0]
                            if diff < smallest_diff:
                                smallest_diff = diff
                                smallest_loc = i
                                count = 1
                            elif diff == smallest_diff:
                                count += 1
                                if self._next_double() <= 1.0 / count:
                                    smallest_loc = i

                        # Merge the two closest bins into their average x location, weighted by their heights.
                        # The height of the new bin is the sum of the heights of the old bins.
                        bin1 = self.bins[smallest_loc]
                        bin2 = self.bins[smallest_loc + 1]
                        total_y = bin1[1] + bin2[1]
                        new_x = (bin1[0] * bin1[1] + bin2[0] * bin2[1]) / total_y

                        self.bins[smallest_loc] = (new_x, total_y)

                        # Shift the remaining bins left one position
                        self.bins.pop(smallest_loc + 1)
                        self.n_used_bins -= 1

            _histogram_numeric_udaf = cached_udaf(
                HistogramNumericUDAF,
                return_type=VariantType(),
                input_types=[aggregate_input_typ, IntegerType()],
            )

            result_exp = _resolve_aggregate_exp(
                _histogram_numeric_udaf(
                    snowpark_args[0], snowpark_fn.lit(snowpark_args[1])
                ),
                histogram_return_type,
            )
        case "hll_sketch_agg":
            # check if input type is correct
            if type(snowpark_typed_args[0].typ) not in [
                IntegerType,
                LongType,
                StringType,
                BinaryType,
            ]:
                type_str = snowpark_typed_args[0].typ.simpleString().upper()
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 1 requires the ("INT" or "BIGINT" or "STRING" or "BINARY") type, however "{snowpark_arg_names[0]}" has the type "{type_str}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            match snowpark_args:
                case [sketch]:
                    spark_function_name = (
                        f"{function_name}({snowpark_arg_names[0]}, 12)"
                    )
                    result_exp = snowpark_fn.call_function(
                        "DATASKETCHES_HLL_ACCUMULATE", sketch, snowpark_fn.lit(12)
                    )
                case [sketch, lgConfigK]:
                    result_exp = snowpark_fn.call_function(
                        "DATASKETCHES_HLL_ACCUMULATE", sketch, lgConfigK
                    )
            result_type = BinaryType()
        case "hll_sketch_estimate":
            result_exp = snowpark_fn.call_function(
                "DATASKETCHES_HLL_ESTIMATE", snowpark_args[0]
            ).cast(LongType())
            result_type = LongType()
        case "hll_union_agg":
            raise_error = _raise_error_helper(BinaryType())
            args = exp.unresolved_function.arguments
            allow_different_lgConfigK = len(args) == 2 and unwrap_literal(args[1])
            spark_function_name = f"{function_name}({snowpark_arg_names[0]}, {str(allow_different_lgConfigK).lower()})"
            hll_union_agg_res = snowpark_fn.call_function(
                "DATASKETCHES_HLL_COMBINE", snowpark_args[0]
            )
            # lgConfigK is stored in the 4th byte of the sketch
            lgConfigK_count = snowpark_fn.count_distinct(
                snowpark_fn.substr(snowpark_args[0], 4, 1)
            )
            result_exp = (
                snowpark_fn.when(
                    snowpark_fn.lit(allow_different_lgConfigK), hll_union_agg_res
                )
                .when(lgConfigK_count == 1, hll_union_agg_res)
                .otherwise(
                    raise_error(
                        snowpark_fn.lit(
                            "[HLL_UNION_DIFFERENT_LG_K] Sketches have different `lgConfigK` values. Set the `allowDifferentLgConfigK` parameter to true to call `hll_union_agg` with different `lgConfigK` values."
                        )
                    )
                )
            )

            result_type = BinaryType()
        case "hll_union":
            fn = register_cached_sql_udf(
                ["binary", "binary"],
                "binary",
                """
                SELECT CASE
                    WHEN arg0 IS NULL OR arg1 IS NULL THEN NULL
                    ELSE DATASKETCHES_HLL_COMBINE(x)
                END FROM (
                    SELECT arg0 as x
                    UNION ALL
                    SELECT arg1 as x)
                """,
            )
            raise_error = _raise_error_helper(BinaryType())
            args = exp.unresolved_function.arguments
            allow_different_lgConfigK = len(args) == 3 and unwrap_literal(args[2])
            spark_function_name = f"{function_name}({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, {str(allow_different_lgConfigK).lower()})"
            hll_union_res = fn(snowpark_args[0], snowpark_args[1])
            result_exp = (
                snowpark_fn.when(snowpark_fn.is_null(snowpark_args[0]), hll_union_res)
                .when(snowpark_fn.is_null(snowpark_args[1]), hll_union_res)
                .when(snowpark_fn.lit(allow_different_lgConfigK), hll_union_res)
                .when(
                    # lgConfigK is stored in the 4th byte of the sketch
                    snowpark_fn.substr(snowpark_args[0], 4, 1).cast(BinaryType())
                    == snowpark_fn.substr(snowpark_args[1], 4, 1).cast(BinaryType()),
                    hll_union_res,
                )
                .otherwise(
                    raise_error(
                        snowpark_fn.lit(
                            "[HLL_UNION_DIFFERENT_LG_K] Sketches have different `lgConfigK` values. Set the `allowDifferentLgConfigK` parameter to true to call `hll_union` with different `lgConfigK` values."
                        )
                    )
                )
            )

            result_type = BinaryType()
        case "hour":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.hour(
                    snowpark_fn.builtin("try_to_timestamp")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.hour(
                    snowpark_fn.to_timestamp(snowpark_args[0])
                )
            # Spark 3.5.3: Hour extends GetTimeField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L397
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "hypot":
            spark_function_name = (
                f"HYPOT({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
            )
            result_exp = snowpark_fn.sqrt(
                snowpark_args[0] * snowpark_args[0]
                + snowpark_args[1] * snowpark_args[1]
            )
            result_type = DoubleType()
        case "ilike":
            # Snowpark is not supporting ilike, so using Snowflake builtin function
            ilike = snowpark_fn.builtin("ilike")
            result_exp = ilike(snowpark_args[0], snowpark_args[1])
            result_type = BooleanType()
        case "in":
            spark_function_name = f"({snowpark_arg_names[0] if not snowpark_arg_names[0] in ['True', 'False'] else snowpark_arg_names[0].lower()} IN ({', '.join(snowpark_arg_names[1:])}))"
            # Type checking for IN operator
            left_type = snowpark_typed_args[0].typ
            right_types = [arg.typ for arg in snowpark_typed_args[1:]]

            # Check if all types are the same or compatible
            all_types = [left_type] + right_types
            type_names = []

            for typ in all_types:
                try:
                    spark_type = map_snowpark_to_pyspark_types(typ)
                    type_names.append(f'"{spark_type.simpleString().upper()}"')
                except Exception:
                    type_names.append(f'"{typ.simple_string().upper()}"')

            # Check for type mismatches
            type_mismatched = False
            try:
                if not all(
                    _find_common_type([left_type, right_type]) is not None
                    for right_type in right_types
                ):
                    type_mismatched = True
            except Exception:
                type_mismatched = True

            if type_mismatched:
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.DATA_DIFF_TYPES] Cannot resolve "{spark_function_name}" due to data type mismatch: '
                    f'Input to `in` should all be the same type, but it\'s [{", ".join(type_names)}].'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            try:
                result_exp = snowpark_args[0].in_(snowpark_args[1:])
            except TypeError:
                left_col = snowpark_typed_args[0]
                left_coerced, right_coerced = _coerce_for_comparison(
                    left_col, snowpark_typed_args[1]
                )
                result_exp = left_coerced == right_coerced
                for right_col in snowpark_typed_args[2:]:
                    left_coerced, right_coerced = _coerce_for_comparison(
                        left_col, right_col
                    )
                    result_exp = result_exp | (left_coerced == right_coerced)

            result_type = BooleanType()
        case "initcap":
            result_exp = snowpark_fn.initcap(snowpark_args[0], snowpark_fn.lit(" "))
            result_type = StringType()
        case "inline" | "inline_outer":
            input_type = snowpark_typed_args[0].typ

            if (
                not isinstance(input_type, ArrayType)
                or input_type.element_type is None
                or isinstance(input_type.element_type, NullType)
            ):
                try:
                    type_str = input_type.simpleString().upper()
                except Exception:
                    type_str = str(input_type)

                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "inline({snowpark_arg_names[0]})" due to data type mismatch: Parameter 1 requires the "ARRAY<STRUCT>" type, however "{snowpark_arg_names[0]}" has the type {type_str}.'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            is_outer = function_name == "inline_outer"

            field_names = [f.name for f in input_type.element_type.fields]

            class Inline:
                def process(self, arr, size, is_outer):
                    if (arr is None or len(arr) == 0) and is_outer:
                        yield tuple([None] * size)
                    elif arr is None:
                        yield
                    else:
                        for el in arr:
                            if el is None:
                                yield tuple([None] * size)
                            else:
                                yield tuple(el.get(k) for k in field_names)

            inline_udtf = cached_udtf(
                Inline,
                output_schema=input_type.element_type,
                input_types=[ArrayType(), LongType(), BooleanType()],
            )

            spark_col_names = list(field_names)
            result_type = list(f.datatype for f in input_type.element_type.fields)
            result_exp = snowpark_fn.call_table_function(
                inline_udtf.name,
                snowpark_typed_args[0].column(to_semi_structure=True),
                snowpark_fn.lit(len(result_type)),
                snowpark_fn.lit(is_outer),
            )
        case "input_file_name":
            # Return the filename metadata column for file-based DataFrames
            # If METADATA$FILENAME doesn't exist (e.g., for DataFrames created from local data),
            # return empty string to match Spark's behavior
            from snowflake.snowpark_connect.relation.read.metadata_utils import (
                METADATA_FILENAME_COLUMN,
            )

            available_columns = column_mapping.get_snowpark_columns()
            if METADATA_FILENAME_COLUMN in available_columns:
                result_exp = snowpark_fn.col(METADATA_FILENAME_COLUMN)
            else:
                # Return empty when METADATA$FILENAME column doesn't exist, matching Spark behavior
                result_exp = snowpark_fn.lit("").cast(StringType())
            result_type = StringType()
            spark_function_name = "input_file_name()"
        case "instr":
            result_exp = snowpark_fn.charindex(snowpark_args[1], snowpark_args[0])
            # Spark 3.5.3: StringInstr defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/stringExpressions.scala#L1332
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "isnan":
            arg_type = snowpark_typed_args[0].typ
            if not isinstance(arg_type, (_NumericType, StringType, NullType)):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "isnan({snowpark_arg_names[0]})" due to data type mismatch: '
                    f'Parameter 1 requires the ("DOUBLE" or "FLOAT") type, however "{snowpark_arg_names[0]}" has the type "{arg_type.simpleString()}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            elif isinstance(arg_type, StringType):
                res_isnan = snowpark_fn.upper(
                    snowpark_fn.trim(snowpark_args[0])
                ) == snowpark_fn.lit("NAN")
                if spark_sql_ansi_enabled:
                    try_res = snowpark_fn.function("try_to_number")(snowpark_args[0])
                    raise_error = _raise_error_helper(
                        BooleanType(), NumberFormatException
                    )
                    result_exp = (
                        snowpark_fn.when(
                            snowpark_args[0].isNull(), snowpark_fn.lit(False)
                        )
                        .when(
                            try_res.is_null() & snowpark_fn.not_(res_isnan),
                            raise_error(
                                snowpark_fn.concat(
                                    snowpark_fn.lit("[CAST_INVALID_INPUT] The value '"),
                                    snowpark_args[0],
                                    snowpark_fn.lit(
                                        '\' of the type "STRING" cannot be cast to "DOUBLE" because it is malformed. Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                                    ),
                                )
                            ),
                        )
                        .otherwise(res_isnan)
                    )
                else:
                    result_exp = snowpark_fn.when(
                        snowpark_args[0].isNull(), snowpark_fn.lit(False)
                    ).otherwise(res_isnan)
            elif isinstance(arg_type, (DecimalType, _IntegralType, NullType)):
                result_exp = snowpark_fn.lit(False)
            else:
                result_exp = snowpark_fn.when(
                    snowpark_args[0].isNull(), snowpark_fn.lit(False)
                ).otherwise(snowpark_fn.equal_nan(snowpark_args[0]))
            result_type = BooleanType()
        case "isnotnull":
            spark_function_name = f"({snowpark_arg_names[0]} IS NOT NULL)"
            result_exp = snowpark_args[0].isNotNull()
            result_type = BooleanType()
        case "isnull":
            spark_function_name = f"({snowpark_arg_names[0]} IS NULL)"
            result_exp = snowpark_args[0].isNull()
            result_type = BooleanType()
        case "java_method" | "reflect":
            class_name, method_name = snowpark_args[0], snowpark_args[1]
            method_args = snowpark_typed_args[2:]

            arg_types: list[DataType] = [arg.typ for arg in method_args]

            allowed_arg_types = {
                BooleanType(),
                ByteType(),
                IntegerType(),
                LongType(),
                FloatType(),
                DoubleType(),
                StringType(),
            }
            for arg_idx, arg_type in enumerate(arg_types):
                if arg_type not in allowed_arg_types:
                    spark_type = map_snowpark_to_pyspark_types(arg_type)

                    exception = AnalysisException(
                        f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: """
                        f"""Parameter {arg_idx+3} requires the ("BOOLEAN" or "TINYINT" or "SMALLINT" or "INT" or "BIGINT" or "FLOAT" or "DOUBLE" or "STRING") type, """
                        f"""however "{snowpark_arg_names[arg_idx+2]}" has the type "{spark_type.simpleString()}"."""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception

            arg_values = snowpark_fn.cast(
                snowpark_fn.array_construct(
                    *[arg.column(to_semi_structure=True) for arg in method_args]
                ),
                ArrayType(StringType()),
            )

            java_method_udf = register_cached_java_udf(
                "com.snowflake.snowpark_connect.udfs.JavaMethodUdf.java_method",
                ["STRING", "STRING", "ARRAY(STRING)", "ARRAY(STRING)"],
                "STRING",
                packages=["com.snowflake:snowpark:1.15.0"],
            )

            # This can never be executed outside a sandboxed UDF due to security reasons
            result_exp = java_method_udf(
                class_name,
                method_name,
                arg_values,
                snowpark_fn.lit([arg_type.simple_string() for arg_type in arg_types]),
            )

            result_type = StringType()
        case "json_array_length":
            if not isinstance(
                snowpark_typed_args[0].typ, StringType
            ) and not isinstance(snowpark_typed_args[0].typ, NullType):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "json_array_length({",".join(snowpark_arg_names)})" due to data type mismatch: Parameter 1 requires the "STRING" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ.simpleString().upper()}"."""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            arr_exp = snowpark_fn.function("TRY_PARSE_JSON")(snowpark_args[0])
            result_exp = snowpark_fn.array_size(arr_exp)
            # Spark 3.5.3: LengthOfJsonArray defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/jsonExpressions.scala#L865
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "json_object_keys":
            if not isinstance(
                snowpark_typed_args[0].typ, StringType
            ) and not isinstance(snowpark_typed_args[0].typ, NullType):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "json_object_keys({",".join(snowpark_arg_names)})" due to data type mismatch: Parameter 1 requires the "STRING" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ.simpleString().upper()}"."""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            obj_exp = snowpark_fn.function("TRY_PARSE_JSON")(
                snowpark_args[0], snowpark_fn.lit("d")
            )
            result_exp = snowpark_fn.object_keys(obj_exp).cast(
                ArrayType(StringType(), True)
            )
            result_exp = snowpark_fn.when(
                snowpark_fn.is_object(obj_exp),
                result_exp,
            ).otherwise(snowpark_fn.lit(None))
            result_type = ArrayType(StringType())
        case "json_tuple":
            analyzer = Session.get_active_session()._analyzer
            json = snowpark_fn.function("TRY_PARSE_JSON")(
                snowpark_args[0], snowpark_fn.lit("d")
            )
            fields = exp.unresolved_function.arguments[1:]
            fields = [unwrap_literal(f) for f in fields]
            fields = [
                snowpark_fn.to_json(snowpark_fn.get(json, snowpark_fn.lit(f)))
                for f in fields
            ]
            fields = [analyzer.analyze(f._expression, defaultdict()) for f in fields]
            result_exp = snowpark_fn.sql_expr(", ".join(fields))
            spark_col_names = [f"c{i}" for i in range(len(fields))]
            # TODO: will this always be a string?
            result_type = [StringType() for _ in range(len(fields))]
        case "kurtosis":
            # SNOW-2177354
            if isinstance(snowpark_typed_args[0].typ, _NumericType):
                # In Snowflake we calculate kurtosis using the sample excess kurtosis formula.
                # In Spark they use the population excess kurtosis formula.
                # The difference between these two requires some rearranging
                # which leads to the math shown below (in population_excess_kurtosis)
                # Kurtosis is also calculated on a minimum of 4 values and it also requires a non-zero variance
                # as variance is the denominator in some of the calculations. We return null on all zero variance
                # datasets. Spark returns -1.5 on 3 values and -2 on 2 values so we simply do the same here.
                # Formulas can be found at: https://www.macroption.com/kurtosis-formula/
                row_count = snowpark_fn.count(snowpark_args[0])
                sample_excess_kurtosis = (
                    snowpark_fn.when(
                        snowpark_fn.variance(snowpark_args[0]) == 0,
                        snowpark_fn.lit(None),
                    )
                    .when(row_count >= 4, snowpark_fn.kurtosis(snowpark_args[0]))
                    .when(row_count == 3, snowpark_fn.lit(-1.5))
                    .when(row_count == 2, snowpark_fn.lit(-2))
                    .otherwise(snowpark_fn.lit(None))
                )
                population_excess_kurtosis = (
                    snowpark_fn.when(
                        sample_excess_kurtosis.isNull(), snowpark_fn.lit(None)
                    )
                    .when(row_count == 3, snowpark_fn.lit(-1.5))
                    .when(row_count == 2, snowpark_fn.lit(-2))
                    .otherwise(
                        (
                            (
                                sample_excess_kurtosis
                                + (3 * (row_count - 1) * (row_count - 1))
                                / ((row_count - 2) * (row_count - 3))
                            )
                            * (
                                ((row_count - 3) * (row_count - 2))
                                / (row_count * (row_count - 1) * (row_count + 1))
                            )
                        )
                        * row_count
                        - 3
                    )
                )
                result_exp = _resolve_aggregate_exp(
                    population_excess_kurtosis,
                    DoubleType(),
                )
            else:
                result_exp = snowpark_fn.kurtosis(snowpark_fn.lit(None))
            result_type = DoubleType()
        case "lag":
            offset = unwrap_literal(exp.unresolved_function.arguments[1])
            default = snowpark_args[2] if len(snowpark_args) > 2 else None
            default_name = (
                "NULL"
                if default is None
                else map_expression(
                    exp.unresolved_function.arguments[2], column_mapping, typer
                )[0][0]
            )
            result_exp = snowpark_fn.lag(snowpark_args[0], offset, default)
            result_exp = TypedColumn(result_exp, lambda: snowpark_typed_args[0].types)
            spark_function_name = (
                f"lag({snowpark_arg_names[0]}, {offset}, {default_name})"
            )
        case "last" | "last_value":
            if not is_window_enabled():
                # AGGREGATE CONTEXT: NON-DETERMINISTIC BEHAVIOR
                # When last() is used as an aggregate function (without window/ORDER BY),
                # it exhibits non-deterministic behavior - returns "any value it sees last" from each group.
                # This is explicitly documented in PySpark as non-deterministic behavior.

                # According to PySpark docs, ignore_nulls can be a Column - but it doesn't make sense and doesn't work.
                # So assume it's a literal.
                args = exp.unresolved_function.arguments
                ignore_nulls = unwrap_literal(args[1]) if len(args) > 1 else False

                # Since last() is non-deterministic and just returns "some value" from the group,
                # ANY_VALUE is the perfect match for this behavior
                if ignore_nulls:
                    # TODO(SNOW-1955766): When ignoring nulls, we need to completely exclude null values from aggregation
                    # Since Snowflake's ANY_VALUE doesn't support ignore_nulls parameter yet (SNOW-1955766),
                    # we fall back to MAX() which naturally ignores nulls and gives us "some value" from the group
                    # This is semantically equivalent to last(..., ignore_nulls=True) for non-deterministic behavior
                    result_exp = snowpark_fn.max(snowpark_args[0])
                else:
                    result_exp = snowpark_fn.any_value(snowpark_args[0])
                spark_function_name = f"{function_name}({snowpark_arg_names[0]})"
            else:
                # WINDOW CONTEXT: DETERMINISTIC BEHAVIOR
                # When last() is used as a window function with ORDER BY,
                # it exhibits deterministic behavior - returns the last value according to the specified ordering.
                # This delegates to last_value() window function which is deterministic.
                result_exp = _resolve_last_value(exp, snowpark_args)
            result_exp = TypedColumn(result_exp, lambda: snowpark_typed_args[0].types)
        case "last_day":
            match snowpark_typed_args[0].typ:
                case DateType():
                    result_exp = snowpark_args[0]
                case TimestampType():
                    result_exp = snowpark_fn.to_date(snowpark_args[0])
                case StringType():
                    result_exp = (
                        snowpark_fn.builtin("try_to_date")(
                            snowpark_args[0],
                            snowpark_fn.lit(
                                map_spark_timestamp_format_expression(
                                    exp.unresolved_function.arguments[1],
                                    snowpark_typed_args[0].typ,
                                )
                            ),
                        )
                        if len(snowpark_args) > 1
                        else snowpark_fn.builtin("try_to_date")(*snowpark_args)
                    )
                case _:
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "last_day({snowpark_arg_names[0]}" due to data type mismatch: Parameter 1 requires the "DATE" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0]}".'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception

            result_exp = snowpark_fn.last_day(result_exp)
            result_type = DateType()
        case "lead":
            offset = unwrap_literal(exp.unresolved_function.arguments[1])
            default = snowpark_args[2] if len(snowpark_args) > 2 else None
            default_name = (
                "NULL"
                if default is None
                else map_expression(
                    exp.unresolved_function.arguments[2], column_mapping, typer
                )[0][0]
            )
            result_exp = snowpark_fn.lead(snowpark_args[0], offset, default)
            result_exp = TypedColumn(result_exp, lambda: snowpark_typed_args[0].types)
            spark_col_names = [
                f"lead({snowpark_arg_names[0]}, {offset}, {default_name})"
            ]
        case "least":
            result_exp = snowpark_fn.function("LEAST_IGNORE_NULLS")(*snowpark_args)
            result_exp = TypedColumn(result_exp, lambda: snowpark_typed_args[0].types)
        case "left":
            if not spark_sql_ansi_enabled and (
                len(snowpark_args) != 2
                or not isinstance(snowpark_typed_args[1].typ, _IntegralType)
            ):
                result_exp = snowpark_fn.lit(None)
            else:
                result_exp = snowpark_fn.when(
                    snowpark_args[1] <= 0, snowpark_fn.lit("")
                ).otherwise(snowpark_fn.left(*snowpark_args))
            result_type = StringType()
        case "length" | "char_length" | "character_length" | "len":
            if exp.unresolved_function.arguments[0].HasField("literal"):
                # Only update the name if it has the literal field.
                # If it doesn't, it means it's binary data.
                arg_value = repr(unwrap_literal(exp.unresolved_function.arguments[0]))
                # repr is used to display proper column names when newlines or tabs are included in the string
                # However, this breaks with the usage of nested emojis.
                arg_value = arg_value[1:-1] if arg_value != "None" else "NULL"
                spark_function_name = (
                    f"{exp.unresolved_function.function_name}({arg_value})"
                )
            result_exp = snowpark_fn.length(snowpark_args[0])
            result_type = IntegerType()
        case "levenshtein":
            match snowpark_args:
                case [arg1, arg2]:
                    result_exp = snowpark_fn.editdistance(arg1, arg2)
                case [arg1, arg2, _]:
                    max_distance = unwrap_literal(exp.unresolved_function.arguments[2])

                    if max_distance >= 0:
                        # snowpark implementation
                        # a maximum distance can be specified. If the distance exceeds this value, the computation halts and returns the maximum distance.
                        # we are passing max_distance + 1 to make it compatible to spark
                        result_exp = snowpark_fn.editdistance(
                            arg1, arg2, max_distance + 1
                        )
                        result_exp = snowpark_fn.when(
                            result_exp >= max_distance + 1, snowpark_fn.lit(-1)
                        ).otherwise(result_exp)
                    else:
                        result_exp = snowpark_fn.when(
                            snowpark_fn.is_null(arg1) | snowpark_fn.is_null(arg2),
                            snowpark_fn.lit(None),
                        ).otherwise(snowpark_fn.lit(-1))
                case _:
                    exception = ValueError(
                        f"Invalid number of arguments to {function_name}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            # Spark 3.5.3: Levenshtein defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/stringExpressions.scala#L2186
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "like":
            result_exp = snowpark_fn.call_function("like", *snowpark_args)
            result_type = BooleanType()
            spark_function_name = (
                f"{snowpark_arg_names[0]} LIKE {snowpark_arg_names[1]}"
            )
        case "likeall":
            result_exp = _like_util(snowpark_args[0], snowpark_args[1:], mode="all")
            result_type = BooleanType()
        case "likeany":
            result_exp = _like_util(snowpark_args[0], snowpark_args[1:], mode="any")
            result_type = BooleanType()
        case "ln":
            result_exp = snowpark_fn.when(
                snowpark_args[0] <= 0, snowpark_fn.lit(None)
            ).otherwise(snowpark_fn.ln(snowpark_args[0]))
            result_type = DoubleType()
        case "localtimestamp":
            result_type = TimestampType(TimestampTimeZone.NTZ)
            result_exp = snowpark_fn.to_timestamp_ntz(
                snowpark_fn.builtin("localtimestamp")()
            )
        case "locate":
            substr = unwrap_literal(exp.unresolved_function.arguments[0])
            value = snowpark_args[1]
            start_pos = unwrap_literal(exp.unresolved_function.arguments[2])

            if start_pos > 0:
                result_exp = snowpark_fn.locate(substr, value, start_pos)
            else:
                result_exp = snowpark_fn.when(
                    snowpark_fn.is_null(value),
                    snowpark_fn.lit(None),
                ).otherwise(snowpark_fn.lit(0))
            result_type = IntegerType()
        case "log":
            # This handles a SQL case where log can be called with a single element and no second element will be automatically padded.
            if len(snowpark_args) == 1:
                spark_function_name = f"LOG(E(), {snowpark_arg_names[0]})"
                result_exp = snowpark_fn.when(
                    snowpark_args[0] <= 0, snowpark_fn.lit(None)
                ).otherwise(snowpark_fn.ln(snowpark_args[0]))
                result_type = DoubleType()
            else:
                spark_function_name = (
                    f"LOG({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
                )
                result_exp = (
                    snowpark_fn.when(
                        snowpark_args[0] == 1,
                        snowpark_fn.when(snowpark_args[1] == 1, NAN).otherwise(
                            INFINITY
                        ),
                    )
                    .when(
                        (snowpark_args[1] <= 0) | (snowpark_args[0] == 0),
                        snowpark_fn.lit(None),
                    )
                    .otherwise(snowpark_fn.log(snowpark_args[0], snowpark_args[1]))
                )
                result_type = DoubleType()
        case "log10":
            spark_function_name = f"LOG10({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                snowpark_args[0] <= 0, snowpark_fn.lit(None)
            ).otherwise(snowpark_fn.log(10.0, snowpark_args[0]))
            result_type = DoubleType()
        case "log1p":
            spark_function_name = f"LOG1P({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                snowpark_args[0] <= -1, snowpark_fn.lit(None)
            ).otherwise(snowpark_fn.ln(snowpark_args[0] + snowpark_fn.lit(1.0)))
            result_type = DoubleType()
        case "log2":
            spark_function_name = f"LOG2({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                snowpark_args[0] <= 0, snowpark_fn.lit(None)
            ).otherwise(snowpark_fn.log(2.0, snowpark_args[0]))
            result_type = DoubleType()
        case "lower" | "lcase":
            result_exp = snowpark_fn.lower(snowpark_args[0])
            result_type = StringType()
        case "lpad" | "rpad":
            first_typed_arg = snowpark_typed_args[0]
            first_arg = snowpark_args[0]
            pad_value = snowpark_fn.lit(" ")
            args_names = f"{snowpark_arg_names[0]}, {snowpark_arg_names[1]},  "

            if len(snowpark_args) == 3:
                third_typed_arg = snowpark_typed_args[2]
                pad_value = third_typed_arg.col
                args_names = f"{snowpark_arg_names[0]}, {snowpark_arg_names[1]}, {snowpark_arg_names[2]}"

                if isinstance(first_typed_arg.typ, BinaryType) ^ isinstance(
                    third_typed_arg.typ, BinaryType
                ):
                    if isinstance(third_typed_arg.typ, BinaryType):
                        pad_value = _to_char(third_typed_arg.col)
                    if isinstance(first_typed_arg.typ, BinaryType):
                        first_arg = _to_char(first_typed_arg.col)

            elif isinstance(first_typed_arg.typ, BinaryType):
                pad_value = snowpark_fn.lit(b"\x00")
                args_names = f"{snowpark_arg_names[0]}, {snowpark_arg_names[1]}, X'00'"

            spark_function_name = f"{function_name}({args_names})"

            if not spark_sql_ansi_enabled and (
                len(snowpark_args) < 2
                or not isinstance(snowpark_typed_args[1].typ, _IntegralType)
            ):
                result_exp = snowpark_fn.lit(None)
            else:
                args = [first_arg, snowpark_args[1], pad_value]
                result_exp = (
                    snowpark_fn.lpad(*args)
                    if function_name == "lpad"
                    else snowpark_fn.rpad(*args)
                )

            result_type = StringType()
        case "ltrim" | "rtrim":
            function_name_argument = (
                "TRAILING" if function_name == "rtrim" else "LEADING"
            )
            if len(snowpark_args) == 2:
                # Only possible using SQL
                spark_function_name = f"TRIM({function_name_argument} {snowpark_arg_names[1]} FROM {snowpark_arg_names[0]})"
            result_exp = snowpark_fn.ltrim(*snowpark_args)
            result_type = StringType()
            if isinstance(snowpark_typed_args[0].typ, BinaryType):
                argument_name = snowpark_arg_names[0]
                if exp.unresolved_function.arguments[0].HasField("literal"):
                    argument_name = f"""X'{exp.unresolved_function.arguments[0].literal.binary.hex()}'"""
                if len(snowpark_args) == 1:
                    spark_function_name = f"{function_name}({argument_name})"
                    trim_value = snowpark_fn.lit(b"\x20")
                if len(snowpark_args) == 2:
                    # Only possible using SQL
                    trim_arg = snowpark_arg_names[1]
                    if isinstance(
                        snowpark_typed_args[1].typ, BinaryType
                    ) and exp.unresolved_function.arguments[1].HasField("literal"):
                        trim_arg = f"""X'{exp.unresolved_function.arguments[1].literal.binary.hex()}'"""
                        trim_value = snowpark_args[1]
                    else:
                        trim_value = snowpark_fn.lit(None)
                    function_name_argument = (
                        "TRAILING" if function_name == "rtrim" else "LEADING"
                    )
                    spark_function_name = f"TRIM({function_name_argument} {trim_arg} FROM {argument_name})"
                result_exp = _trim_helper(
                    snowpark_args[0], trim_value, snowpark_fn.lit(function_name)
                )
                result_type = BinaryType()
            else:
                if function_name == "ltrim":
                    result_exp = snowpark_fn.ltrim(*snowpark_args)
                    result_type = StringType()
                elif function_name == "rtrim":
                    result_exp = snowpark_fn.rtrim(*snowpark_args)
                    result_type = StringType()
        case "make_date":
            y = snowpark_args[0].cast(LongType())
            m = snowpark_args[1].cast(LongType())
            d = snowpark_args[2].cast(LongType())
            dash = snowpark_fn.lit("-")
            snowpark_function = "to_date" if spark_sql_ansi_enabled else "try_to_date"
            date_str_exp = snowpark_fn.concat(y, dash, m, dash, d)
            result_exp = snowpark_fn.builtin(snowpark_function)(date_str_exp)
            result_type = DateType()
        case "make_dt_interval":
            # Pad argument names for display purposes
            padded_arg_names = snowpark_arg_names.copy()
            while len(padded_arg_names) < 3:  # days, hours, minutes are integers
                padded_arg_names.append("0")
            if len(padded_arg_names) < 4:  # seconds can be decimal
                padded_arg_names.append("0.000000")

            spark_function_name = f"make_dt_interval({', '.join(padded_arg_names)})"
            result_exp = snowpark_fn.interval_day_time_from_parts(*snowpark_args)
            result_type = DayTimeIntervalType()
        case "make_timestamp" | "make_timestamp_ltz" | "make_timestamp_ntz":
            y, m, d, h, mins = map(lambda col: col.cast(LongType()), snowpark_args[:5])
            y_abs = snowpark_fn.abs(y)
            s = snowpark_args[5].cast(DoubleType())
            # 'seconds = 60' is valid
            s_shifted = snowpark_fn.when(s == 60, 0).otherwise(s)
            s_floor = snowpark_fn.floor(s)
            nanos = snowpark_fn.round(
                snowpark_fn.round(s - s_floor, 6) * 1_000_000_000
            ).cast(LongType())

            dash = snowpark_fn.lit("-")
            space = snowpark_fn.lit(" ")
            colon = snowpark_fn.lit(":")
            parse_function = (
                "to_timestamp" if spark_sql_ansi_enabled else "try_to_timestamp"
            )
            str_exp = snowpark_fn.concat(
                y_abs, dash, m, dash, d, space, h, colon, mins, colon, s_shifted
            )
            parsed_str_exp = snowpark_fn.builtin(parse_function)(str_exp)

            match function_name:
                case "make_timestamp":
                    make_function_name = "timestamp_tz_from_parts"
                    result_type = get_timestamp_type()
                case "make_timestamp_ltz":
                    make_function_name = "timestamp_ltz_from_parts"
                    result_type = TimestampType(TimestampTimeZone.LTZ)
                case "make_timestamp_ntz":
                    make_function_name = "timestamp_ntz_from_parts"
                    result_type = TimestampType(TimestampTimeZone.NTZ)

            make_timestamp_res = (
                snowpark_fn.timestamp_tz_from_parts(
                    y,
                    m,
                    d,
                    h,
                    mins,
                    s_floor,
                    nanos,
                    snowpark_args[6],
                ).cast(result_type)
                if len(snowpark_args) == 7
                else snowpark_fn.function(make_function_name)(
                    y, m, d, h, mins, s_floor, nanos
                ).cast(result_type)
            )

            result_exp = snowpark_fn.when(
                snowpark_fn.is_null(parsed_str_exp), snowpark_fn.lit(None)
            ).otherwise(make_timestamp_res)
        case "make_ym_interval":
            # Pad argument names for display purposes
            padded_arg_names = snowpark_arg_names.copy()
            while len(padded_arg_names) < 2:  # years, months
                padded_arg_names.append("0")

            spark_function_name = f"make_ym_interval({', '.join(padded_arg_names)})"
            result_exp = snowpark_fn.interval_year_month_from_parts(*snowpark_args)
            result_type = YearMonthIntervalType()
        case "map":
            allow_duplicate_keys = (
                global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            )

            key_type = _find_common_type(
                list(map(lambda x: x.typ, snowpark_typed_args[::2]))
            )
            value_type = _find_common_type(
                list(map(lambda x: x.typ, snowpark_typed_args[1::2]))
            )
            num_args = len(snowpark_args)
            if num_args == 0:
                result_exp = snowpark_fn.cast(
                    snowpark_fn.object_construct(), MapType(NullType(), NullType())
                )
                result_type = MapType(NullType(), NullType())
            elif (num_args % 2) == 1:
                exception = AnalysisException(
                    f"[WRONG_NUM_ARGS.WITHOUT_SUGGESTION] The `map` requires 2n (n > 0) parameters but the actual number is {num_args}"
                )
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception
            elif key_type is None or isinstance(key_type, NullType):
                exception = SparkRuntimeException(
                    "[NULL_MAP_KEY] Cannot use null as map key."
                )
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception
            else:
                value_type = value_type if value_type else NullType()

                # initialize map with empty object
                result_exp = snowpark_fn.object_construct()
                # insert key-value pairs, null values are converted to json null
                for i in range(0, num_args, 2):
                    result_exp = snowpark_fn.object_insert(
                        result_exp,
                        snowpark_fn.when(
                            snowpark_fn.is_null(snowpark_args[i]),
                            # udf execution on XP seems to be lazy, so this should only run when there is a null key
                            # otherwise there should be no udf env setup or execution
                            _raise_error_helper(VariantType())(
                                snowpark_fn.lit(
                                    "[NULL_MAP_KEY] Cannot use null as map key."
                                )
                            ),
                        ).otherwise(snowpark_args[i]),
                        snowpark_fn.nvl(
                            snowpark_fn.cast(snowpark_args[i + 1], VariantType()),
                            snowpark_fn.parse_json(snowpark_fn.lit("null")),
                        ),
                        snowpark_fn.lit(allow_duplicate_keys),
                    )

                result_type = MapType(key_type, value_type)
                result_exp = snowpark_fn.cast(
                    result_exp,
                    result_type,
                )
        case "map_concat":
            allow_duplicate_keys = (
                global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            )

            def _map_concat(allow_dups, arg_array):
                new_map = {}
                for m in arg_array:
                    if m is None:
                        # return none if any of the input maps are none
                        return None
                    for key, value in m.items():
                        if key in new_map and not allow_dups:
                            raise ValueError(
                                f"[snowpark_connect::invalid_operation] {DUPLICATE_KEY_FOUND_ERROR_TEMPLATE.format(key=key)}"
                            )
                        else:
                            new_map[key] = value
                return new_map

            map_concat_udf = cached_udf(
                _map_concat,
                input_types=[BooleanType(), ArrayType()],
                return_type=VariantType(),
            )

            key_type = _find_common_type(
                list(map(lambda x: x.typ.key_type, snowpark_typed_args[::2]))
            )
            value_type = _find_common_type(
                list(map(lambda x: x.typ.value_type, snowpark_typed_args[1::2]))
            )

            input_args = [snowpark_fn.cast(arg, StructType()) for arg in snowpark_args]

            result_exp = snowpark_fn.cast(
                map_concat_udf(
                    snowpark_fn.lit(allow_duplicate_keys),
                    snowpark_fn.array_construct(*input_args),
                ),
                MapType(key_type, value_type),
            )
            result_type = MapType(key_type, value_type)
        case "map_contains_key":
            if isinstance(snowpark_typed_args[0].typ, NullType):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.MAP_FUNCTION_DIFF_TYPES] Cannot resolve "map_contains_key({snowpark_arg_names[0]}, {snowpark_arg_names[1]})" due to data type mismatch: Input to `map_contains_key` should have been "MAP" followed by a value with same key type, but it's ["VOID", "INT"]."""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            if isinstance(snowpark_typed_args[1].typ, NullType):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.NULL_TYPE] Cannot resolve "map_contains_key({snowpark_arg_names[0]}, {snowpark_arg_names[1]})" due to data type mismatch: Null typed values cannot be used as arguments of `map_contains_key`."""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            args = (
                [snowpark_args[1], snowpark_args[0]]
                if isinstance(snowpark_typed_args[0].typ, MapType)
                else snowpark_args
            )
            result_exp = snowpark_fn.map_contains_key(*args)
            result_type = BooleanType()
        case "map_entries":
            if not isinstance(snowpark_typed_args[0].typ, MapType):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "map_entries({snowpark_arg_names[0]})" due to data type mismatch: Parameter 1 requires the "MAP" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".;"""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            key_type = snowpark_typed_args[0].typ.key_type
            value_type = snowpark_typed_args[0].typ.value_type

            arg_type = snowpark_typed_args[0].typ
            if not isinstance(arg_type, MapType):
                exception = TypeError(
                    f"map_entries requires a MapType argument, got {arg_type}"
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            # SNOW-2040715
            @cached_udf(input_types=[arg_type], return_type=ArrayType(StructType()))
            def _map_entries(obj: dict):
                if obj is None:
                    raise TypeError(
                        f"[snowpark_connect::type_mismatch] Expected MapType but received {obj} instead."
                    )
                return [{"key": key, "value": value} for key, value in obj.items()]

            result_type = ArrayType(
                StructType(
                    [
                        StructField("key", key_type, _is_column=False),
                        StructField("value", value_type, _is_column=False),
                    ]
                )
            )
            result_exp = snowpark_fn.when(
                snowpark_fn.function("map_size")(snowpark_args[0]).isNull(),
                snowpark_fn.lit(None),
            ).otherwise(
                snowpark_fn.cast(
                    _map_entries(snowpark_args[0]),
                    result_type,
                )
            )
        case "map_from_arrays":
            keys_type = snowpark_typed_args[0].typ
            values_type = snowpark_typed_args[1].typ
            if not isinstance(keys_type, ArrayType) or not isinstance(
                values_type, ArrayType
            ):
                exception = TypeError(
                    f"map_from_arrays requires two arguments of type ArrayType, got {keys_type} and {values_type}"
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            key_type = keys_type.element_type if keys_type.structured else VariantType()
            value_type = (
                values_type.element_type if values_type.structured else VariantType()
            )

            allow_duplicate_keys = (
                global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            )

            def _map_from_arrays(allow_dups, keys, values):
                if keys is None or values is None:
                    return None
                if len(keys) != len(values):
                    raise ValueError(
                        "[snowpark_connect::internal_error] The key array and value array of must have the same length"
                    )

                if not allow_dups and len(set(keys)) != len(keys):
                    seen = set()
                    for key in keys:
                        if key in seen:
                            raise ValueError(
                                f"[snowpark_connect::invalid_operation] {DUPLICATE_KEY_FOUND_ERROR_TEMPLATE.format(key=key)}"
                            )
                        seen.add(key)
                # will overwrite the last occurrence if there are duplicates.
                return dict(zip(keys, values))

            _map_from_arrays_udf = cached_udf(
                _map_from_arrays,
                return_type=VariantType(),
                input_types=[BooleanType(), ArrayType(), ArrayType()],
            )
            result_exp = snowpark_fn.cast(
                _map_from_arrays_udf(
                    snowpark_fn.lit(allow_duplicate_keys),
                    snowpark_fn.cast(snowpark_args[0], ArrayType()),
                    snowpark_fn.cast(snowpark_args[1], ArrayType()),
                ),
                MapType(key_type, value_type),
            )
            result_type = MapType(key_type, value_type)
        case "map_from_entries":
            if not isinstance(snowpark_typed_args[0].typ, ArrayType):
                exception = TypeError(
                    f"map_from_entries requires an argument of type ArrayType, got {snowpark_typed_args[0].typ}"
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            entry_type = snowpark_typed_args[0].typ.element_type

            match entry_type:
                case None:
                    # workaround for spark sql struct(key, value) - entry_type is None
                    # TODO: can we get correct types once we integrate spark's sql parser?
                    # VariantType is not supported for structured map keys
                    key_type = StringType()
                    value_type = VariantType()
                    # default field names
                    key_field = "col1"
                    value_field = "col2"
                case _ if isinstance(entry_type, StructType) and entry_type.structured:
                    key_type = entry_type.fields[0].datatype
                    value_type = entry_type.fields[1].datatype
                    [key_field, value_field] = entry_type.names
                case _ if isinstance(entry_type, StructType) and len(
                    entry_type.fields
                ) >= 2:
                    # Handle unstructured StructType with explicit field names (e.g., from arrays_zip)
                    key_type = entry_type.fields[0].datatype
                    value_type = entry_type.fields[1].datatype
                    [key_field, value_field] = entry_type.names[:2]
                case _:
                    exception = TypeError(
                        f"map_from_entries requires an array of StructType, got array of {entry_type}"
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception

            last_win_dedup = global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"

            # Check if any entry has a NULL key
            has_null_key = (
                snowpark_fn.function("array_size")(
                    snowpark_fn.function("filter")(
                        snowpark_args[0],
                        snowpark_fn.sql_expr(f"e -> e:{key_field} IS NULL"),
                    )
                )
                > 0
            )

            # Create error UDF for NULL keys (same pattern as map function)
            null_key_error = _raise_error_helper(VariantType())(
                snowpark_fn.lit("[NULL_MAP_KEY] Cannot use null as map key.")
            )

            # Create the reduce operation
            reduce_result = snowpark_fn.function("reduce")(
                snowpark_args[0],
                snowpark_fn.object_construct(),
                snowpark_fn.sql_expr(
                    # value_field is cast to variant because object_insert doesn't allow structured types,
                    # and structured types are not coercible to variant
                    # TODO: allow structured types in object_insert?
                    f"(acc, e) -> object_insert(acc, e:{key_field}, e:{value_field}::variant, {last_win_dedup})"
                ),
            )

            # Use conditional logic: if there are NULL keys, throw error; otherwise proceed with reduce
            result_exp = snowpark_fn.cast(
                snowpark_fn.when(has_null_key, null_key_error).otherwise(reduce_result),
                MapType(key_type, value_type),
            )
            result_type = MapType(key_type, value_type)
        case "map_keys":
            arg_type = snowpark_typed_args[0].typ
            if not isinstance(arg_type, MapType):
                exception = TypeError(
                    f"map_keys requires a MapType argument, got {arg_type}"
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            if arg_type.structured:
                result_exp = snowpark_fn.map_keys(snowpark_args[0])
            else:
                # snowpark's map_keys function is not compatible with snowflake's OBJECT type
                result_exp = snowpark_fn.object_keys(snowpark_args[0])
            result_type = ArrayType(arg_type.key_type, contains_null=False)
        case "map_values":
            # TODO: implement in Snowflake/Snowpark
            # technically this could be done with a lateral join, but it's probably not worth the effort
            arg_type = snowpark_typed_args[0].typ
            if not isinstance(arg_type, (MapType, NullType)):
                exception = AnalysisException(
                    f"map_values requires a MapType argument, got {arg_type}"
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            def _map_values(obj: dict) -> list:
                if obj is None:
                    return None
                return list(obj.values())

            map_values = cached_udf(
                _map_values, return_type=ArrayType(), input_types=[StructType()]
            )

            # Handle NULL input directly at expression level
            if isinstance(arg_type, NullType):
                # If input is NULL literal, return NULL
                result_exp = snowpark_fn.lit(None)
                result_type = ArrayType(NullType())
            else:
                result_exp = snowpark_fn.when(
                    snowpark_args[0].is_null(), snowpark_fn.lit(None)
                ).otherwise(
                    snowpark_fn.cast(
                        map_values(snowpark_fn.cast(snowpark_args[0], StructType())),
                        ArrayType(arg_type.value_type),
                    )
                )
                result_type = ArrayType(arg_type.value_type)
        case "mask":

            number_of_args = len(snowpark_args)
            result_exp = snowpark_args[0]  # First arg is always the input string

            # Initialize with default values
            upper_char = snowpark_fn.lit("X")
            lower_char = snowpark_fn.lit("x")
            digit_char = snowpark_fn.lit("n")
            other_char = snowpark_fn.lit(None)

            upper_char_arg_name = "X"
            lower_char_arg_name = "x"
            digit_char_arg_name = "n"
            other_char_arg_name = "NULL"

            # Process remaining arguments
            literal_values = [None]
            for i in range(1, number_of_args):
                arg_name = snowpark_arg_names[i]
                arg_value = snowpark_args[i]

                # For named arguments and literals, we want to extract the actual literal value
                if isinstance(arg_value, snowpark.Column):
                    # Try to get literal value if it's a literal
                    try:
                        literal_value = arg_value._expression.value
                        if literal_value is None:
                            literal_value = "NULL"
                        literal_values.append(literal_value)
                    except AttributeError:
                        literal_value = arg_name
                        literal_values.append(None)

                # Check if this is a named argument
                if arg_name == "upperChar":
                    upper_char = arg_value
                    upper_char_arg_name = literal_value
                elif arg_name == "lowerChar":
                    lower_char = arg_value
                    lower_char_arg_name = literal_value
                elif arg_name == "digitChar":
                    digit_char = arg_value
                    digit_char_arg_name = literal_value
                elif arg_name == "otherChar":
                    other_char = arg_value
                    other_char_arg_name = literal_value
                # Handle positional arguments
                elif i == 1:
                    upper_char = arg_value
                    upper_char_arg_name = literal_value
                elif i == 2:
                    lower_char = arg_value
                    lower_char_arg_name = literal_value
                elif i == 3:
                    digit_char = arg_value
                    digit_char_arg_name = literal_value
                elif i == 4:
                    other_char = arg_value
                    other_char_arg_name = literal_value

            spark_function_name = f"mask({snowpark_arg_names[0]}, {upper_char_arg_name}, {lower_char_arg_name}, {digit_char_arg_name}, {other_char_arg_name})"

            # Sanity check for arguments
            col_arg_names = [None, "upperChar", "lowerChar", "digitChar", "otherChar"]
            for i in range(1, number_of_args):
                arg_name = snowpark_arg_names[i]
                arg_type = snowpark_typed_args[i].typ
                if isinstance(snowpark_typed_args[i].typ, NullType) or (
                    isinstance(literal_values[i], str) and len(literal_values[i]) == 1
                ):
                    pass
                elif not isinstance(arg_type, StringType):
                    exception = AnalysisException(
                        f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter {i + 1} requires the "STRING" type, however "{arg_name}" has the type "{arg_type.simpleString().upper()}".;"""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                elif (
                    exp.unresolved_function.arguments[i].WhichOneof("expr_type")
                    != "literal"
                ):
                    exception = AnalysisException(
                        f"""[DATATYPE_MISMATCH.NON_FOLDABLE_INPUT] Cannot resolve "{spark_function_name}" due to data type mismatch: the input {col_arg_names[i]} should be a foldable "STRING" expression; however, got "{arg_name}"."""
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
                elif len(arg_name) != 1:
                    exception = AnalysisException(
                        f"""[DATATYPE_MISMATCH.INPUT_SIZE_NOT_ONE] Cannot resolve "{spark_function_name}" due to data type mismatch: Length of {col_arg_names[i]} should be 1."""
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception

            random_tag_suffix = "".join(random.sample(string.ascii_uppercase, 6))
            tags = [
                s + random_tag_suffix
                for s in ["TAGUPPER", "TAGLOWER", "TAGDIGIT", "TAGOTHER"]
            ]
            patterns = ["[A-Z]", "[a-z]", r"\d", "[^A-Z]"]
            replacements = [upper_char, lower_char, digit_char, other_char]

            # To avoid replacement character collisions we need to replace them with unique tags first.
            for tag, pattern, replacement_char in zip(tags, patterns, replacements):
                result_exp = snowpark_fn.when(
                    ~snowpark_fn.is_null(replacement_char),
                    snowpark_fn.regexp_replace(result_exp, pattern, tag),
                ).otherwise(result_exp)

            for tag, replacement_char in zip(tags, replacements):
                result_exp = snowpark_fn.when(
                    ~snowpark_fn.is_null(replacement_char),
                    snowpark_fn.regexp_replace(result_exp, tag, replacement_char),
                ).otherwise(result_exp)
            result_type = StringType()
        case "max":
            result_exp = _handle_structured_aggregate_result(
                snowpark_fn.max, snowpark_typed_args[0], snowpark_typed_args[0].types
            )
        case "max_by":
            result_exp = TypedColumn(
                snowpark_fn.max_by(*snowpark_args),
                lambda: snowpark_typed_args[0].types,
            )
        case "md5":
            snowflake_compat = get_boolean_session_config_param(
                "snowpark.connect.enable_snowflake_extension_behavior"
            )

            # MD5 in Spark only accepts BinaryType or types that can be implicitly cast to it (StringType)
            if not snowflake_compat:
                if not isinstance(snowpark_typed_args[0].typ, (BinaryType, StringType)):
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "md5({snowpark_arg_names[0]})" due to data type mismatch: '
                        f'Parameter 1 requires the "BINARY" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
            result_exp = snowpark_fn.md5(snowpark_args[0])
            result_type = StringType(32)
        case "median":
            result_exp = _resolve_aggregate_exp(
                snowpark_fn.median(snowpark_args[0]), DoubleType()
            )
        case "min":
            result_exp = _handle_structured_aggregate_result(
                snowpark_fn.min, snowpark_typed_args[0], snowpark_typed_args[0].types
            )
        case "min_by":
            result_exp = TypedColumn(
                snowpark_fn.min_by(*snowpark_args),
                lambda: snowpark_typed_args[0].types,
            )
        case "minute":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.minute(
                    snowpark_fn.builtin("try_to_timestamp")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.minute(
                    snowpark_fn.to_timestamp(snowpark_args[0])
                )
            # Spark 3.5.3: Minute extends GetTimeField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L397
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "mode":
            result_exp = TypedColumn(
                snowpark_fn.mode(snowpark_args[0]),
                lambda: snowpark_typed_args[0].types,
            )
        case "monotonically_increasing_id":
            result_exp = snowpark_fn.monotonically_increasing_id()
            result_type = LongType()
        case "distributed_sequence_id":
            # PySpark's distributed_sequence_id generates consecutive IDs starting from 0
            # Use row_number() over monotonically_increasing_id() to ensure consecutiveness, then subtract 1
            from snowflake.snowpark import Window

            window_spec = Window.order_by(snowpark_fn.monotonically_increasing_id())
            result_exp = snowpark_fn.row_number().over(window_spec) - 1
            result_type = LongType()
        case "month":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.month(
                    snowpark_fn.builtin("try_to_date")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.month(snowpark_fn.to_date(snowpark_args[0]))
            # Spark 3.5.3: Month extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "months_between":
            # Pyspark months_between returns a floating point number with a higher precision than Snowpark
            # and has a third optional argument (roundOff: bool = True), which allows to increase the precision even more.
            # The difference is visible after a few decimal places, but in order to have a 100% compatibility, extending the Snowpark's API is required.

            spark_function_name = f"months_between({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, {'true' if len(snowpark_args) == 2 else str(snowpark_arg_names[2]).lower()})"
            result_exp = _try_to_cast(
                "try_to_date",
                snowpark_fn.cast(
                    snowpark_fn.months_between(
                        snowpark_fn.cast(snowpark_args[0], get_timestamp_type()),
                        snowpark_fn.cast(snowpark_args[1], get_timestamp_type()),
                    ),
                    DoubleType(),
                ),
                snowpark_args[0],
                snowpark_args[1],
            )
            result_type = DoubleType()
        case "named_struct":
            # Handle star expansion - create field name-value pairs
            expanded_typed_args: list[TypedColumn] = []

            for arg in exp.unresolved_function.arguments:
                if arg.unresolved_star.HasField("unparsed_target"):
                    (
                        star_names,
                        expanded_star_args_list,
                    ) = map_unresolved_star_struct(arg, column_mapping, typer)
                    expanded_typed_args.extend(expanded_star_args_list)
                else:
                    # resolve regular argument normally
                    arg_names, arg_typed_column = map_expression(
                        arg, column_mapping, typer
                    )
                    if hasattr(arg_typed_column.col, "_expression"):
                        col_exp = arg_typed_column.col._expression
                        if isinstance(col_exp, Alias):
                            arg_typed_column = TypedColumn(
                                Column(col_exp.child),
                                lambda arg_tc=arg_typed_column: arg_tc.types,
                            )

                    expanded_typed_args.append(arg_typed_column)

            if len(expanded_typed_args) % 2 != 0:
                exception = ValueError(
                    "Number of arguments must be even (a list of key-value pairs)."
                )
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception

            # field types for the schema
            field_names = []
            field_types = []
            for i in range(0, len(expanded_typed_args), 2):
                field_name_col = expanded_typed_args[i].col
                field_name = (
                    field_name_col._expression.value
                    if hasattr(field_name_col, "_expression")
                    else str(field_name_col)
                )
                field_names.append(field_name)

                field_value_typed_col = expanded_typed_args[i + 1]
                field_type = (
                    field_value_typed_col.types[0]
                    if field_value_typed_col.types
                    else None
                )
                field_types.append(field_type)

            # Before calling object_construct_keep_null, convert struct field values to variants
            # to handle nested structs properly
            converted_args = []
            for i, typed_arg in enumerate(expanded_typed_args):
                arg = typed_arg.col
                if i % 2 == 1:  # This is a field value (odd indices)
                    field_type = field_types[i // 2]
                    if isinstance(field_type, (StructType, ArrayType)):
                        # Convert struct to variant to avoid OBJECT_CONSTRUCT_KEEP_NULL error
                        converted_args.append(snowpark_fn.to_variant(arg))
                    else:
                        converted_args.append(arg)
                else:  # This is a field name (even indices)
                    converted_args.append(arg)

            result_exp = snowpark_fn.object_construct_keep_null(*converted_args)

            # Create schema
            schema = StructType(
                [
                    StructField(name, typ, _is_column=False)
                    for name, typ in zip(field_names, field_types)
                ]
            )
            result_exp = snowpark_fn.cast(result_exp, schema)

            # Add struct marker only when in UDTF context to distinguish named_struct from map
            if get_is_in_udtf_context():
                result_exp = snowpark_fn.object_insert(
                    snowpark_fn.to_variant(result_exp),
                    snowpark_fn.lit("__struct_marker__"),
                    snowpark_fn.lit(True),
                )
            result_type = schema
        case "nanvl":
            arg1_is_nan = snowpark_fn.equal_nan(snowpark_args[0])
            result_exp = snowpark_fn.when(arg1_is_nan, snowpark_args[1]).otherwise(
                snowpark_args[0]
            )
            result_type = DoubleType()
        case "negative" | "unary_minus":
            arg_type = snowpark_typed_args[0].typ
            if function_name == "unary_minus":
                spark_function_name = f"(- {snowpark_arg_names[0]})"
            else:
                spark_function_name = f"negative({snowpark_arg_names[0]})"
            if isinstance(arg_type, _IntegralType):
                result_exp = apply_unary_overflow_with_ansi_check(
                    snowpark_args[0], arg_type, spark_sql_ansi_enabled, "negative"
                )
            elif (
                isinstance(arg_type, _NumericType)
                or isinstance(arg_type, YearMonthIntervalType)
                or isinstance(arg_type, DayTimeIntervalType)
            ):
                # Instead of using snowpark_fn.negate which can generate invalid SQL for nested minus operations,
                # use a direct multiplication by -1 which generates cleaner SQL
                result_exp = snowpark_args[0] * snowpark_fn.lit(-1)
            elif isinstance(arg_type, StringType):
                if spark_sql_ansi_enabled:
                    exception = NumberFormatException(
                        f'The value \'{snowpark_args[0]}\' of the type {arg_type} cannot be cast to "DOUBLE" because it is malformed. Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
                    raise exception
                else:
                    result_exp = snowpark_fn.lit(None)
            elif isinstance(arg_type, NullType):
                result_exp = snowpark_fn.lit(None)
            else:
                exception = AnalysisException(
                    f"[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve {spark_function_name} due to data type mismatch: "
                    f'Parameter 1 requires the ("NUMERIC") type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0]}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            result_type = (
                snowpark_typed_args[0].types
                if isinstance(arg_type, _NumericType)
                or isinstance(arg_type, YearMonthIntervalType)
                or isinstance(arg_type, DayTimeIntervalType)
                else DoubleType()
            )
        case "next_day":
            dates = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
            date = unwrap_literal(exp.unresolved_function.arguments[1])
            if date is None or date.lower() not in dates:
                if spark_sql_ansi_enabled:
                    exception = IllegalArgumentException(
                        """Illegal input for day of week. If necessary set "spark.sql.ansi.enabled" to false to bypass this error."""
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
                else:
                    result_exp = snowpark_fn.lit(None)
            else:
                result_exp = _try_to_cast(
                    "try_to_date",
                    snowpark_fn.next_day(snowpark_args[0], snowpark_args[1]),
                    snowpark_args[0],
                )
            result_type = DateType()
        case "not" | "!":
            spark_function_name = f"(NOT {snowpark_arg_names[0]})"
            result_exp = ~snowpark_args[0]
            result_type = BooleanType()
        case "notlikeany":
            result_exp = _like_util(
                snowpark_args[0], snowpark_args[1:], mode="any", negate=True
            )
            result_type = BooleanType()
        case "notlikeall":
            result_exp = _like_util(
                snowpark_args[0], snowpark_args[1:], mode="all", negate=True
            )
            result_type = BooleanType()
        case "nth_value":
            args = exp.unresolved_function.arguments
            n = unwrap_literal(args[1])
            ignore_nulls = unwrap_literal(args[2]) if len(args) > 2 else False
            result_exp = TypedColumn(
                snowpark_fn.nth_value(snowpark_args[0], n, ignore_nulls),
                lambda: snowpark_typed_args[0].types,
            )
            spark_function_name = f"nth_value({snowpark_arg_names[0]}, {n}){' ignore nulls' if ignore_nulls else ''}"
        case "ntile":
            result_exp = snowpark_fn.ntile(snowpark_args[0])
            # IntegerType per Spark's NTile case class which extends AggregateWindowFunction, which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/34d9413ca161f4531544565976a46c6da7d371cd/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/windowExpressions.scala#L626
            result_exp = _resolve_aggregate_exp(result_exp, IntegerType())
        case "nullif":
            result_exp = TypedColumn(
                snowpark_fn.call_function("nullif", *snowpark_args),
                lambda: snowpark_typed_args[0].types,
            )
        case "nvl" | "ifnull":
            _validate_arity(2)
            result_type = _find_common_type([arg.typ for arg in snowpark_typed_args])
            result_exp = snowpark_fn.nvl(
                *[col.cast(result_type) for col in snowpark_args]
            )
        case "nvl2":
            _validate_arity(3)
            result_type = _find_common_type(
                [arg.typ for arg in snowpark_typed_args[1:]]
            )
            result_exp = snowpark_fn.call_function(
                "nvl2",
                snowpark_args[0],
                *[col.cast(result_type) for col in snowpark_args[1:]],
            )
        case "octet_length":
            if isinstance(snowpark_typed_args[0].typ, (ArrayType, MapType)):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "octet_length({snowpark_arg_names[0]})" due to data type mismatch: Parameter 1 requires the ("STRING" or "BINARY") type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}"."""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            result_exp = snowpark_fn.octet_length(snowpark_args[0])
            if isinstance(snowpark_typed_args[0].typ, _FractionalType):
                # All decimal types have to have 3 characters at a minimum.
                result_exp = snowpark_fn.when(
                    result_exp < snowpark_fn.lit(3), snowpark_fn.lit(3)
                ).otherwise(result_exp)
            # Spark 3.5.3: OctetLength defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/stringExpressions.scala#L2116
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "or":
            spark_function_name = (
                f"({snowpark_arg_names[0]} OR {snowpark_arg_names[1]})"
            )
            result_exp = snowpark_args[0] | snowpark_args[1]
            result_type = BooleanType()
        case "overlay":
            length = snowpark_fn.when(
                snowpark_args[3] < 0, snowpark_fn.length(snowpark_args[1])
            ).otherwise(snowpark_args[3])
            result_exp = snowpark_fn.concat(
                snowpark_fn.substring(snowpark_args[0], 1, snowpark_args[2] - 1),
                snowpark_args[1],
                snowpark_fn.substring(snowpark_args[0], snowpark_args[2] + length),
            )
            result_type = StringType()
        case "parse_url":
            url, part_to_extract = snowpark_args[0], snowpark_args[1]
            key = snowpark_args[2] if len(snowpark_args) > 2 else snowpark_fn.lit(None)

            result_exp = snowpark_fn.call_function("parse_url", url)
            split_part = snowpark_fn.function("split_part")

            host = snowpark_fn.get(result_exp, snowpark_fn.lit("host"))
            path = snowpark_fn.get(result_exp, snowpark_fn.lit("path"))
            scheme = snowpark_fn.get(result_exp, snowpark_fn.lit("scheme"))

            result_exp = (
                snowpark_fn.when(
                    snowpark_fn.upper(part_to_extract) != part_to_extract,
                    snowpark_fn.lit(None),
                )
                .when(
                    part_to_extract == snowpark_fn.lit("PROTOCOL"),
                    scheme,
                )
                .when(
                    part_to_extract == snowpark_fn.lit("REF"),
                    snowpark_fn.get(result_exp, snowpark_fn.lit("fragment")),
                )
                .when(
                    part_to_extract == snowpark_fn.lit("AUTHORITY"),
                    snowpark_fn.nvl(
                        snowpark_fn.concat_ws(
                            snowpark_fn.lit(":"),
                            host,
                            snowpark_fn.get(result_exp, snowpark_fn.lit("port")),
                        ),
                        host,
                    ),
                )
                .when(
                    part_to_extract == snowpark_fn.lit("QUERY"),
                    snowpark_fn.when(
                        key.is_null(),
                        snowpark_fn.get(result_exp, snowpark_fn.lit("query")),
                    ).otherwise(
                        snowpark_fn.get(
                            snowpark_fn.get(result_exp, snowpark_fn.lit("parameters")),
                            key,
                        )
                    ),
                )
                .when(
                    (part_to_extract == snowpark_fn.lit("FILE"))
                    & ~(scheme == snowpark_fn.lit("mailto")),
                    snowpark_fn.concat(
                        snowpark_fn.lit("/"),
                        snowpark_fn.trim(
                            snowpark_fn.nvl(
                                snowpark_fn.concat_ws(
                                    snowpark_fn.lit("?"),
                                    path,
                                    snowpark_fn.get(
                                        result_exp, snowpark_fn.lit("query")
                                    ),
                                ),
                                path,
                            ),
                            snowpark_fn.lit("/"),
                        ),
                    ),
                )
                .when(
                    part_to_extract == snowpark_fn.lit("USERINFO"),
                    snowpark_fn.when(
                        snowpark_fn.contains(host, snowpark_fn.lit("@")),
                        split_part(
                            host,
                            snowpark_fn.lit("@"),
                            snowpark_fn.lit(0),
                        ),
                    ).otherwise(snowpark_fn.lit(None)),
                )
                .when(
                    (part_to_extract == snowpark_fn.lit("PATH"))
                    & ~(scheme == snowpark_fn.lit("mailto")),
                    snowpark_fn.concat(snowpark_fn.lit("/"), path),
                )
                .when(
                    part_to_extract == snowpark_fn.lit("HOST"),
                    split_part(host, snowpark_fn.lit("@"), snowpark_fn.lit(-1)),
                )
                .otherwise(snowpark_fn.lit(None))
            )

            result_exp = snowpark_fn.cast(result_exp, StringType())
            result_type = StringType()
        case "percent_rank":
            result_exp = snowpark_fn.percent_rank()
            result_exp = TypedColumn(result_exp, lambda: [DoubleType()])
        case "percentile":
            column_value = (
                snowpark_fn.function("try_to_number")(snowpark_args[0])
                if isinstance(snowpark_typed_args[0].typ, StringType)
                else snowpark_args[0]
            )
            column_type = (
                DoubleType()
                if isinstance(snowpark_typed_args[0].typ, StringType)
                else snowpark_typed_args[0].typ
            )

            if not isinstance(snowpark_typed_args[0].typ, (_NumericType, StringType)):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{function_name}({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, {snowpark_arg_names[2]})" due to data type mismatch: Parameter 1 requires the "NUMERIC" type, however "value" has the type "{snowpark_typed_args[0].typ}".;"""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            elif len(snowpark_args) == 3:

                class PercentileUDAF:
                    import math
                    from typing import Any, List, Tuple

                    def __init__(self) -> None:
                        from collections import Counter

                        self.dist_dict = Counter()
                        self.percentages = []

                    @property
                    def aggregate_state(self):
                        return (self.dist_dict, self.percentages)

                    def accumulate(self, value, percentages, frequency: int):

                        if frequency < 0:
                            raise ValueError(
                                f"[snowpark_connect::invalid_input] Negative values found in {frequency}"
                            )

                        if not self.percentages:
                            self.percentages = percentages

                            if any(
                                percentage < 0 or percentage > 1
                                for percentage in self.percentages
                            ):
                                raise ValueError(
                                    "[snowpark_connect::invalid_input] The percentage must be between [0.0, 1.0]"
                                )

                        if value is None:
                            return

                        self.dist_dict[value] = self.dist_dict.get(value, 0) + frequency

                    def finish(self):

                        if not self.dist_dict:
                            return None

                        sorted_counts = sorted(
                            self.dist_dict.items(),
                            key=lambda item: (math.isnan(item[0]), item[0]),
                        )

                        accumulated = 0
                        for i in range(len(sorted_counts)):
                            key, count = sorted_counts[i]
                            accumulated = accumulated + count
                            sorted_counts[i] = (key, accumulated)

                        if len(self.percentages) == 1:
                            return self.get_percentile(
                                sorted_counts, self.percentages[0]
                            )

                        return [
                            self.get_percentile(sorted_counts, percentage)
                            for percentage in self.percentages
                        ]

                    def get_percentile(
                        self,
                        accumulated_counts: List[Tuple[Any, int]],
                        percentile: float,
                    ) -> float:
                        """
                        accumulated_counts: List of tuples (key, cumulative_count),
                                            sorted by key or as appropriate.
                        percentile: value between 0 and 1.
                        Algorithm based on Spark code: https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/aggregate/percentiles.scala#L194
                        """
                        if not accumulated_counts:
                            raise ValueError(
                                "[snowpark_connect::internal_error] accumulated_counts cannot be empty"
                            )

                        total_count = accumulated_counts[-1][1]
                        position = (total_count - 1) * percentile

                        lower = math.floor(position)
                        higher = math.ceil(position)

                        counts_array = [count for _, count in accumulated_counts]

                        import bisect

                        lower_index = bisect.bisect_left(counts_array, lower + 1)
                        higher_index = bisect.bisect_left(counts_array, higher + 1)

                        lower_key = accumulated_counts[lower_index][0]

                        if higher == lower:
                            # no interpolation needed because position has no fractional part
                            return lower_key

                        higher_key = accumulated_counts[higher_index][0]
                        if higher_key == lower_key:
                            # no interpolation needed, both keys are same
                            return lower_key

                        return (higher - position) * lower_key + (
                            position - lower
                        ) * higher_key

                    def merge(self, other: tuple):
                        if other is None:
                            return

                        o_dist_dict, o_percentages = other
                        if len(o_percentages) != 0:
                            self.percentages = o_percentages

                        self.dist_dict = self.dist_dict + o_dist_dict

                _percentile_udaf = cached_udaf(
                    PercentileUDAF,
                    return_type=VariantType(),
                    input_types=[
                        column_type,
                        ArrayType(DoubleType()),
                        IntegerType(),
                    ],
                )
                percentage = snowpark_args[1]
                if isinstance(snowpark_typed_args[1].typ, ArrayType):
                    result_type = ArrayType(
                        element_type=DoubleType(), contains_null=False
                    )
                else:
                    percentage = snowpark_fn.array_construct(percentage).cast(
                        ArrayType(DoubleType())
                    )
                    result_type = DoubleType()

                result_exp = _resolve_aggregate_exp(
                    _percentile_udaf(column_value, percentage, snowpark_args[2]),
                    result_type,
                )
            elif isinstance(snowpark_typed_args[1].typ, ArrayType):
                # Snowpark doesn't accept a list of percentile values.
                # This is a workaround to fetch percentile arguments and invoke the snowpark_fn.approx_percentile serially.
                percentile_values = _unwrap_array_literals(
                    exp.unresolved_function.arguments[1]
                )
                result_exp = snowpark_fn.array_construct(
                    *[
                        snowpark_fn.function("percentile_cont")(
                            _check_percentile_percentage_value(p)
                        ).within_group(column_value)
                        for p in percentile_values
                    ]
                )
                result_type = ArrayType(element_type=DoubleType(), contains_null=False)
                result_exp = _resolve_aggregate_exp(result_exp, result_type)
                spark_function_name = f"{function_name}({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, 1)"
            else:
                result_exp = snowpark_fn.function("percentile_cont")(
                    _check_percentile_percentage(exp.unresolved_function.arguments[1])
                ).within_group(column_value)
                result_exp = _resolve_aggregate_exp(result_exp, DoubleType())
                spark_function_name = f"{function_name}({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, 1)"
        case "percentile_cont" | "percentiledisc":
            if function_name == "percentiledisc":
                function_name = "percentile_disc"
            order_by_col = snowpark_args[0]
            args = exp.unresolved_function.arguments
            if len(args) != 3:
                exception = AssertionError(
                    f"{function_name} expected 3 args but got {len(args)}"
                )
                attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
                raise exception
            # literal value 0.0 - 1.0
            percentage_arg = args[1]
            sort_direction = args[2].sort_order.direction
            direction_str = ""  # defaultValue
            if (
                sort_direction
                == expressions_proto.Expression.SortOrder.SORT_DIRECTION_DESCENDING
            ):
                direction_str = "DESC"

            # Apply sort direction to the order_by column
            if direction_str == "DESC":
                order_by_col_with_direction = order_by_col.desc()
            else:
                order_by_col_with_direction = order_by_col.asc()

            result_exp = snowpark_fn.function(function_name)(
                _check_percentile_percentage(percentage_arg)
            ).within_group(order_by_col_with_direction)
            result_exp = (
                TypedColumn(
                    snowpark_fn.cast(result_exp, FloatType()), lambda: [DoubleType()]
                )
                if not is_window_enabled()
                else TypedColumnWithDeferredCast(result_exp, lambda: [DoubleType()])
            )

            direction_part = f" {direction_str}" if direction_str else ""
            spark_function_name = f"{function_name}({unwrap_literal(percentage_arg)}) WITHIN GROUP (ORDER BY {snowpark_arg_names[0]}{direction_part})"
        case "pi":
            spark_function_name = "PI()"
            result_type = DoubleType()
            result_exp = snowpark_fn.lit(math.pi, datatype=result_type)
        case "pmod":
            dividend_operand = OperandInfo(
                snowpark_typed_args[0], args_types[0], snowpark_arg_names[0]
            )
            divisor_operand = OperandInfo(
                snowpark_typed_args[1], args_types[1], snowpark_arg_names[1]
            )
            result_type = _get_mod_return_type(dividend_operand, divisor_operand)
            if result_type:
                if not isinstance(dividend_operand.typ, _NumericType) or not isinstance(
                    divisor_operand.typ, _NumericType
                ):
                    result_exp = snowpark_fn.lit(None)
                else:
                    a, b = snowpark_args
                    if spark_sql_ansi_enabled:
                        result_exp = snowpark_fn.when(a < 0, (a % b + b) % b).otherwise(
                            a % b
                        )
                    else:
                        result_exp = (
                            snowpark_fn.when(b == 0, snowpark_fn.lit(None))
                            .when(a < 0, (a % b + b) % b)
                            .otherwise(a % b)
                        )
                result_exp = snowpark_fn.cast(result_exp, result_type)
                result_exp = TypedColumn(result_exp, lambda: [result_type])
            else:
                exception = AnalysisException(
                    f"""pyspark.errors.exceptions.captured.AnalysisException: [DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{spark_function_name}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{dividend_operand.typ}" and "{divisor_operand.typ}")."""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
        case "posexplode" | "posexplode_outer":
            input_type = snowpark_typed_args[0].typ
            is_nullable = function_name == "posexplode_outer"
            if isinstance(input_type, ArrayType):

                class PosExplode:
                    def process(self, arr, function_name):
                        if not arr:
                            if function_name == "posexplode":
                                yield
                            else:
                                yield (None, None)
                        else:
                            yield from enumerate(arr)

                posexplode_udtf = cached_udtf(
                    PosExplode,
                    output_schema=StructType(
                        [
                            StructField(
                                "pos", IntegerType(), is_nullable, _is_column=False
                            ),
                            StructField(
                                "col", input_type.element_type, True, _is_column=False
                            ),
                        ]
                    ),
                    input_types=[input_type, StringType()],
                )

                spark_col_names = ["pos", "col"]
                result_type = [IntegerType(), input_type.element_type]
            elif isinstance(input_type, MapType):

                class PosExplode:
                    def process(self, m, function_name):
                        if not m:
                            if function_name == "posexplode":
                                yield
                            else:
                                yield (None, None, None)
                        else:
                            for i, (key, value) in enumerate(m.items()):
                                yield (i, key, value)

                posexplode_udtf = cached_udtf(
                    PosExplode,
                    output_schema=StructType(
                        [
                            StructField(
                                "pos",
                                LongType(),
                                is_nullable,
                                _is_column=False,
                            ),
                            StructField(
                                "key",
                                input_type.key_type,
                                is_nullable,
                                _is_column=False,
                            ),
                            StructField(
                                "value",
                                input_type.value_type,
                                True,
                                _is_column=False,
                            ),
                        ]
                    ),
                    input_types=[input_type, StringType()],
                )

                spark_col_names = ["pos", "key", "value"]
                result_type = [
                    LongType(),
                    input_type.key_type,
                    input_type.value_type,
                ]
            else:
                exception = TypeError(
                    f"Data type mismatch: {function_name} requires an array or map input, but got {input_type}."
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            result_exp = snowpark_fn.call_table_function(
                posexplode_udtf.name, snowpark_args[0], snowpark_fn.lit(function_name)
            )
        case "position":
            substr, base_str = snowpark_args[0], snowpark_args[1]
            start_pos = (
                snowpark_args[2] if len(snowpark_args) > 2 else snowpark_fn.lit(1)
            )

            result_exp = snowpark_fn.when(
                snowpark_fn.is_null(start_pos), snowpark_fn.lit(0)
            ).otherwise(snowpark_fn.position(substr, base_str, start_pos))
            # Spark 3.5.3: StringLocate defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/stringExpressions.scala#L1431
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)

            if len(snowpark_args) == 2:
                spark_function_name = (
                    f"position({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, 1)"
                )

        case "positive":
            arg_type = snowpark_typed_args[0].typ
            spark_function_name = f"(+ {snowpark_arg_names[0]})"
            if (
                isinstance(arg_type, _NumericType)
                or isinstance(arg_type, YearMonthIntervalType)
                or isinstance(arg_type, DayTimeIntervalType)
            ):
                result_exp = snowpark_args[0]
            elif isinstance(arg_type, StringType):
                if spark_sql_ansi_enabled:
                    exception = NumberFormatException(
                        f'The value \'{snowpark_args[0]}\' of the type {arg_type} cannot be cast to "DOUBLE" because it is malformed. Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
                    raise exception
                else:
                    result_exp = snowpark_fn.lit(None)
            elif isinstance(arg_type, NullType):
                result_exp = snowpark_fn.lit(None)
            else:
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "(+ {snowpark_arg_names[0]}" due to data type mismatch: '
                    f'Parameter 1 requires the ("NUMERIC") type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0]}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            result_type = (
                snowpark_typed_args[0].types
                if isinstance(arg_type, _NumericType)
                or isinstance(arg_type, YearMonthIntervalType)
                or isinstance(arg_type, DayTimeIntervalType)
                else DoubleType()
            )
        case "pow" | "power":
            spark_function_name = f"{function_name if function_name == 'pow' else function_name.upper()}({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
            if not spark_sql_ansi_enabled:
                snowpark_args = _validate_numeric_args(
                    function_name, snowpark_typed_args, snowpark_args
                )
            result_exp = snowpark_fn.when(
                snowpark_fn.equal_nan(snowpark_fn.cast(snowpark_args[0], FloatType()))
                | snowpark_fn.equal_nan(
                    snowpark_fn.cast(snowpark_args[1], FloatType())
                ),
                NAN,
            ).otherwise(snowpark_fn.pow(snowpark_args[0], snowpark_args[1]))
            result_type = DoubleType()
        case "product":
            col = snowpark_args[0]
            count_if = snowpark_fn.function("count_if")

            sign = snowpark_fn.when(
                count_if(col < 0) % 2 == 0, snowpark_fn.lit(1)
            ).otherwise(snowpark_fn.lit(-1))

            # Log-Sum-Exp trick
            log_sum_exp = snowpark_fn.exp(
                snowpark_fn.sum(
                    snowpark_fn.ln(
                        snowpark_fn.abs(
                            snowpark_fn.when(col != 0, col).otherwise(
                                snowpark_fn.lit(None)
                            )
                        )
                    )
                )
            )

            result_exp = snowpark_fn.when(
                count_if(col == 0.0) > 0, snowpark_fn.lit(0)
            ).otherwise(sign * log_sum_exp)

            result_type = DoubleType()
        case "quarter":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.quarter(
                    snowpark_fn.builtin("try_to_date")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.quarter(snowpark_fn.to_date(snowpark_args[0]))
            # Spark 3.5.3: Quarter extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "radians":
            spark_function_name = f"RADIANS({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.radians(*snowpark_args)
            result_type = DoubleType()
        case "raise_error":
            result_type = StringType()
            raise_error = _raise_error_helper(result_type)
            result_exp = raise_error(*snowpark_args)
        case "rand" | "random":
            # Snowpark random() generates a 64 bit signed integer, but pyspark is [0.0, 1.0).
            # TODO: Seems like more validation of the arguments is appropriate.
            args = exp.unresolved_function.arguments
            if len(args) > 0:
                if not isinstance(
                    snowpark_typed_args[0].typ, (IntegerType, LongType, NullType)
                ):
                    exception = AnalysisException(
                        f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 1 requires the ("INT" or "BIGINT") type, however {snowpark_arg_names[0]} has the type "{snowpark_typed_args[0].typ}"""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                result_exp = snowpark_fn.random(unwrap_literal(args[0]))
            else:
                result_exp = snowpark_fn.random()

            # Adjust from a 64 bit integer to the pyspark range of [0.0, 1.0).
            # The result_exp is a signed int64 number, so the range is [-2**63, 2**63-1]. We add 2**63 (aka subtract
            # MIN_INT64) to shift this number into the range [0, 2**64-1], which is the uint64 range: [0, MAX_UNIT64]
            # However, in the end result, we want the range to exclude 1.0, hence, we divide by MAX_UNIT64 + 1.
            # The float conversion below is necessary, because snowpark python uses int64 for integers, but we are
            # shifting into unit64 and hence are out of the range of int64.
            result_exp = (result_exp - float(MIN_INT64)) / (float(MAX_UINT64) + 1)
            # TODO SNOW-2034495: can we resolve this type?
            # result_type = DecimalType(26, 6)
            result_exp = _type_with_typer(result_exp)
        case "randn":
            args = exp.unresolved_function.arguments

            result_exp = snowpark_fn.function("NORMAL")(
                snowpark_fn.lit(0.0),
                snowpark_fn.lit(1.0),
                (
                    snowpark_fn.random(unwrap_literal(args[0]))
                    if args
                    else snowpark_fn.random()
                ),
            )
            result_type = DoubleType()
        case "rank":
            result_exp = snowpark_fn.rank()
            # IntegerType per Spark's Rank case class which extends AggregateWindowFunction, which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/34d9413ca161f4531544565976a46c6da7d371cd/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/windowExpressions.scala#L626
            result_exp = _resolve_aggregate_exp(result_exp, IntegerType())
        case "reduce":
            # Call aggregator provided as a snowpark argument
            result_exp = snowpark_args[0]
            result_type = snowpark_typed_args[0].typ
        case "regexp_count":
            # Spark counts an empty pattern as length(input) + 1
            result_exp = (
                snowpark_fn.when(snowpark_fn.is_null(snowpark_args[0]), None)
                .when(snowpark_args[1] == "", snowpark_fn.length(snowpark_args[0]) + 1)
                .otherwise(snowpark_fn.regexp_count(snowpark_args[0], snowpark_args[1]))
            )
            # Spark 3.5.3: RegExpCount defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/regexpExpressions.scala#L1078
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "regexp_extract":
            # Pyspark returns null for a null input, Snowpark coalesces this to an empty string.
            # We check the input to get the same behaviour.
            # If pattern doesn't match string, return empty string
            #    Else if the matched group returns null, throw exception
            result_exp = (
                snowpark_fn.when(snowpark_fn.is_null(snowpark_args[0]), None)
                .when(
                    snowpark_fn.is_null(
                        snowpark_fn.call_function(
                            "regexp_substr",
                            snowpark_args[0],
                            snowpark_args[1],
                            snowpark_fn.lit(1),
                            snowpark_fn.lit(1),
                            snowpark_fn.lit("c"),
                            snowpark_fn.lit(0),
                        )
                    ),
                    "",
                )
                .when(
                    snowpark_fn.is_null(
                        snowpark_fn.call_function(
                            "regexp_substr",
                            snowpark_args[0],
                            snowpark_args[1],
                            snowpark_fn.lit(1),
                            snowpark_fn.lit(1),
                            snowpark_fn.lit("c"),
                            snowpark_args[2],
                        ),
                    ),
                    _raise_error_helper(StringType())(
                        snowpark_fn.lit(
                            "[INVALID_PARAMETER_VALUE.REGEX_GROUP_INDEX] The value of parameter(s) `idx` in `regexp_extract` is invalid."
                        )
                    ),
                )
                .otherwise(
                    snowpark_fn.regexp_extract(
                        snowpark_args[0], snowpark_args[1], snowpark_args[2]
                    )
                )
            )
            result_type = StringType()
        case "regexp_extract_all":
            if len(snowpark_args) == 2:
                idx = snowpark_fn.lit(1)
                spark_function_name = spark_function_name[:-1] + ", 1)"
            else:
                idx = snowpark_args[2]
            # Snowflake's regexp_extract_all has more arguments, so we need to fill out default values
            # If pattern doesn't match string, return empty string
            #    Else if the matched group returns null, throw exception
            result_exp = (
                snowpark_fn.when(snowpark_fn.is_null(snowpark_args[0]), None)
                .when(
                    snowpark_fn.is_null(
                        snowpark_fn.call_function(
                            "regexp_substr",
                            snowpark_args[0],
                            snowpark_args[1],
                            snowpark_fn.lit(1),
                            snowpark_fn.lit(1),
                            snowpark_fn.lit("c"),
                            snowpark_fn.lit(0),
                        ),
                    ),
                    [],
                )
                .when(
                    snowpark_fn.is_null(
                        snowpark_fn.call_function(
                            "regexp_substr",
                            snowpark_args[0],
                            snowpark_args[1],
                            snowpark_fn.lit(1),
                            snowpark_fn.lit(1),
                            snowpark_fn.lit("c"),
                            idx,
                        )
                    ),
                    _raise_error_helper(ArrayType(StringType()))(
                        snowpark_fn.lit(
                            "[INVALID_PARAMETER_VALUE.REGEX_GROUP_INDEX] The value of parameter(s) `idx` in `regexp_extract_all` is invalid."
                        )
                    ),
                )
                .otherwise(
                    snowpark_fn.cast(
                        snowpark_fn.call_function(
                            "regexp_extract_all",
                            snowpark_args[0],
                            snowpark_args[1],
                            snowpark_fn.lit(1),
                            snowpark_fn.lit(1),
                            snowpark_fn.lit("c"),
                            idx,
                        ),
                        ArrayType(StringType()),
                    )
                )
            )
            result_type = ArrayType(StringType())
        case "regexp_instr":
            # Spark seems to ignore the group index argument, so we don't use it here.
            # Spark matches certain patterns to an empty string. We can emulate this with rlike.
            result_exp = (
                snowpark_fn.when(snowpark_fn.is_null(snowpark_args[0]), None)
                .when(
                    (snowpark_args[0] == "")
                    & (snowpark_args[0].rlike(snowpark_args[1])),
                    1,
                )
                .otherwise(
                    snowpark_fn.call_function(
                        "regexp_instr",
                        snowpark_args[0],
                        snowpark_args[1],
                    )
                )
            )
            # Spark 3.5.3: RegExpInStr defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/regexpExpressions.scala#L1078
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
            # if idx was not specified, it defaults to 0 in the column name
            if len(snowpark_args) == 2:
                spark_function_name = spark_function_name[:-1] + ", 0)"
        case "regexp_replace":
            spark_function_name = spark_function_name[:-1] + ", 1)"
            result_exp = snowpark_fn.regexp_replace(*snowpark_args)
            result_type = StringType()
        case "regexp_substr":
            # in some cases Snowflake returns an empty string instead of null
            # but that also counts as no match, for example regexp_substr('', '$')
            result_exp = result_exp = snowpark_fn.call_function(
                "nullif",
                snowpark_fn.call_function("regexp_substr", *snowpark_args),
                "",
            )
            result_type = StringType()
        case "regr_avgx":
            updated_args = _validate_numeric_args(
                function_name, snowpark_typed_args, snowpark_args
            )
            input_type = snowpark_typed_args[1].typ
            if isinstance(input_type, DecimalType):
                result_type = _bounded_decimal(
                    input_type.precision + 4, input_type.scale + 4
                )
            else:
                result_type = DoubleType()

            result_exp = _resolve_aggregate_exp(
                snowpark_fn.regr_avgx(*updated_args),
                result_type,
            )
        case "regr_avgy":
            updated_args = _validate_numeric_args(
                function_name, snowpark_typed_args, snowpark_args
            )
            input_type = snowpark_typed_args[0].typ
            if isinstance(input_type, DecimalType):
                result_type = _bounded_decimal(
                    input_type.precision + 4, input_type.scale + 4
                )
            else:
                result_type = DoubleType()

            result_exp = _resolve_aggregate_exp(
                snowpark_fn.regr_avgy(*updated_args),
                result_type,
            )
        case "regr_count":
            updated_args = _validate_numeric_args(
                function_name, snowpark_typed_args, snowpark_args
            )
            result_exp = snowpark_fn.regr_count(*updated_args)
            result_type = LongType()
        case "regr_intercept":
            updated_args = _validate_numeric_args(
                function_name, snowpark_typed_args, snowpark_args
            )
            result_exp = snowpark_fn.regr_intercept(*updated_args)
            result_type = DoubleType()
        case "regr_r2":
            updated_args = _validate_numeric_args(
                function_name, snowpark_typed_args, snowpark_args
            )
            result_exp = snowpark_fn.regr_r2(*updated_args)
            result_type = DoubleType()
        case "regr_slope":
            updated_args = _validate_numeric_args(
                function_name, snowpark_typed_args, snowpark_args
            )
            result_exp = snowpark_fn.regr_slope(*updated_args)
            result_type = DoubleType()
        case "regr_sxx":
            updated_args = _validate_numeric_args(
                function_name, snowpark_typed_args, snowpark_args
            )
            result_exp = snowpark_fn.regr_sxx(*updated_args)
            result_type = DoubleType()
        case "regr_sxy":
            updated_args = _validate_numeric_args(
                function_name, snowpark_typed_args, snowpark_args
            )
            result_exp = snowpark_fn.regr_sxy(*updated_args)
            result_type = DoubleType()
        case "regr_syy":
            updated_args = _validate_numeric_args(
                function_name, snowpark_typed_args, snowpark_args
            )
            result_exp = snowpark_fn.regr_syy(*updated_args)
            result_type = DoubleType()
        case "repeat":
            result_exp = snowpark_fn.repeat(*snowpark_args)
            result_type = StringType()
        case "replace":
            result_exp = snowpark_fn.replace(*snowpark_args)
            result_type = StringType()
            if len(snowpark_args) == 2:
                spark_function_name = (
                    f"replace({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, )"
                )
        case "reverse":
            match snowpark_typed_args[0].typ:
                case ArrayType():
                    result_exp = snowpark_fn.function("array_reverse")(snowpark_args[0])
                    result_type = snowpark_typed_args[0].typ
                case _:
                    result_exp = snowpark_fn.reverse(snowpark_args[0])
                    result_type = StringType()
        case "right":
            if not spark_sql_ansi_enabled and (
                len(snowpark_args) != 2
                or not isinstance(snowpark_typed_args[1].typ, _IntegralType)
            ):
                result_exp = snowpark_fn.lit(None)
            else:
                right_expr = snowpark_fn.right(*snowpark_args)
                if isinstance(snowpark_typed_args[0].typ, TimestampType):
                    # Spark format is always displayed as YYY-MM-DD HH:mm:ss.FF6
                    # When microseconds are equal to 0 .FF6 part is removed
                    # When microseconds are equal to 0 at the end, they are removed i.e. .123000 -> .123 when displayed

                    formated_timestamp = snowpark_fn.to_varchar(
                        snowpark_args[0], "YYYY-MM-DD HH:MI:SS.FF6"
                    )
                    right_expr = snowpark_fn.right(
                        snowpark_fn.regexp_replace(
                            snowpark_fn.regexp_replace(formated_timestamp, "0+$", ""),
                            "\\.$",
                            "",
                        ),
                        snowpark_args[1],
                    )

                result_exp = snowpark_fn.when(
                    snowpark_args[1] <= 0, snowpark_fn.lit("")
                ).otherwise(right_expr)
            result_type = StringType()
        case "rint":
            result_exp = snowpark_fn.cast(
                snowpark_fn.round(snowpark_args[0]), DoubleType()
            )
            result_type = DoubleType()
        case "rlike" | "regexp" | "regexp_like":
            # Snowflake's regexp/rlike implicitly anchors the pattern to the beginning and end of the string.
            # Spark matches any substring, so we use regexp_instr to emulate this, except empty inputs,
            # which need to be checked with regexp/rlike.
            # We also handle:
            # - the case where the pattern is an empty string, which Spark treats as .*
            # - the case where the pattern uses embedded flag expressions (such as '(?i)', which Spark treats as case-insensitive)
            begin_flag_pyspark = "(?"
            flag_pyspark_regex_pattern = r"\(\?([a-z]+)\)"
            regex_pattern = (
                snowpark_fn.when(snowpark_args[1] == "", ".*")
                .when(
                    snowpark_args[1].startswith(begin_flag_pyspark),
                    snowpark_fn.regexp_replace(
                        snowpark_args[1], flag_pyspark_regex_pattern
                    ),
                )
                .otherwise(snowpark_args[1])
            )
            regex_params = snowpark_fn.when(
                snowpark_args[1].startswith(begin_flag_pyspark),
                snowpark_fn.array_to_string(
                    snowpark_fn.call_function(
                        "regexp_substr_all",
                        snowpark_args[1],
                        flag_pyspark_regex_pattern,
                        1,
                        1,
                        "e",
                        1,
                    ),
                    snowpark_fn.lit(""),
                ),
            ).otherwise("c")
            result_exp = (
                snowpark_fn.when(snowpark_fn.is_null(snowpark_args[0]), None)
                .when(
                    snowpark_args[0] == "",
                    snowpark_fn.call_function(
                        "rlike", snowpark_args[0], regex_pattern, regex_params
                    ),
                )
                .otherwise(
                    snowpark_fn.call_function(
                        "regexp_instr",
                        snowpark_args[0],
                        regex_pattern,
                        1,
                        1,
                        0,
                        regex_params,
                    )
                    > 0
                )
            )
            result_type = BooleanType()
            spark_function_name = (
                f"{function_name.upper()}({', '.join(snowpark_arg_names)})"
            )
        case "round":
            target_scale = 0
            # Limitation: overflow exceptions are currently only supported when literals are given to round
            if spark_sql_ansi_enabled and (
                len(exp.unresolved_function.arguments) == 2
                and exp.unresolved_function.arguments[0].WhichOneof("expr_type")
                == "literal"
                and exp.unresolved_function.arguments[1].WhichOneof("expr_type")
                == "literal"
            ):

                def local_round(value, scale):
                    """Local implementation of round for testing if literals would overflow."""
                    return round(
                        Decimal(value, context=Context(rounding=ROUND_HALF_UP)), scale
                    )

                if _does_number_overflow(
                    local_round(
                        snowpark_args[0]._expression.value,
                        snowpark_args[1]._expression.value,
                    ),
                    snowpark_typed_args[0].typ,
                ):
                    exception = ArithmeticException(
                        '[ARITHMETIC_OVERFLOW] Overflow. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                    )
                    attach_custom_error_code(exception, ErrorCodes.ARITHMETIC_ERROR)
                    raise exception
            if len(snowpark_args) == 1:
                spark_function_name = f"{function_name}({snowpark_arg_names[0]}, 0)"
                result_exp = snowpark_fn.round(snowpark_args[0], snowpark_fn.lit(0))
            else:
                result_exp = snowpark_fn.round(
                    snowpark_args[0],
                    snowpark_args[1],
                )
                target_scale = unwrap_literal(exp.unresolved_function.arguments[1]) or 0
            if isinstance(snowpark_typed_args[0].typ, DecimalType):
                first_arg = exp.unresolved_function.arguments[0]
                # I derived these formulas by looking at Spark's output.
                scale = max(0, min(snowpark_typed_args[0].typ.scale, target_scale))
                precision = (
                    snowpark_typed_args[0].typ.precision
                    - snowpark_typed_args[0].typ.scale
                    + 1
                    + min(snowpark_typed_args[0].typ.scale, target_scale)
                )
                if (
                    first_arg.HasField("literal")
                    and first_arg.literal.HasField("decimal")
                    and first_arg.literal.decimal.value is not None
                ):
                    # It seems like Spark always gives a buffer of 1 for decimals. So if we have 1234.56
                    # Spark will give a precision of 5. (Assuming scale is 0 here). Thus, on all positive numbers,
                    # we take the length of the portion before the decimal and add 1. For all negative numbers, they'll
                    # automatically include a negative sign in the length, meaning the 1 is pre-added.
                    # For the case of 0.0001, we get a precision of just the scale. Since 0. seemingly counts as nothing.
                    # Thus, we also do not add 1 in that case.
                    is_negative = (
                        0
                        if float(first_arg.literal.decimal.value.split(".")[0]) <= 0
                        else 1
                    )
                    precision = (
                        len(first_arg.literal.decimal.value.split(".")[0])
                        + is_negative
                        + scale
                    )
                result_type = _bounded_decimal(precision, scale)
            elif isinstance(snowpark_typed_args[0].typ, NullType):
                result_type = DoubleType()
            else:
                result_type = snowpark_typed_args[0].typ
        case "row_number":
            result_exp = snowpark_fn.row_number()
            # IntegerType per Spark's RowNumberLike case class which extends AggregateWindowFunction, which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/34d9413ca161f4531544565976a46c6da7d371cd/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/windowExpressions.scala#L626
            result_exp = _resolve_aggregate_exp(result_exp, IntegerType())
        case "schema_of_csv":
            # Validate that the input is a foldable STRING expression
            if (
                exp.unresolved_function.arguments[0].WhichOneof("expr_type")
                != "literal"
            ):
                exception = AnalysisException(
                    "[DATATYPE_MISMATCH.NON_FOLDABLE_INPUT] Cannot resolve "
                    f'"schema_of_csv({snowpark_arg_names[0]})" due to data type mismatch: '
                    'the input csv should be a foldable "STRING" expression; however, '
                    f'got "{snowpark_arg_names[0]}".'
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception

            if isinstance(snowpark_typed_args[0].typ, StringType):
                if exp.unresolved_function.arguments[0].literal.string == "":
                    exception = AnalysisException(
                        "[DATATYPE_MISMATCH.NON_FOLDABLE_INPUT] Cannot resolve "
                        f'"schema_of_csv({snowpark_arg_names[0]})" due to data type mismatch: '
                        'the input csv should be a foldable "STRING" expression; however, '
                        f'got "{snowpark_arg_names[0]}".'
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

            snowpark_args = [
                typed_arg.column(to_semi_structure=True)
                for typed_arg in snowpark_typed_args
            ]

            @cached_udf(
                return_type=StringType(),
                input_types=[StringType(), StructType()],
            )
            def _schema_of_csv(data: str, options: Optional[dict]):
                from contextlib import suppress

                sep = ","
                if options is not None and isinstance(options, dict):
                    sep = options.get("sep") or sep

                def _get_type(v: str):
                    if v.lower() in ["true", "false"]:
                        return "BOOLEAN"

                    with suppress(Exception):  # int
                        y = int(v)
                        if str(y) == v:
                            if y < -2147483648 or y > 2147483647:
                                return "BIGINT"
                            return "INT"

                    with suppress(Exception):  # double
                        y = float(v)
                        return "DOUBLE"

                    for _format in ["%H:%M", "%H:%M:%S"]:
                        with suppress(Exception):
                            time.strptime(v, _format)
                            return "TIMESTAMP"

                    return "STRING"

                fields = []
                for i, v in enumerate(data.split(sep)):
                    col_name = f"_c{i}"
                    fields.append(f"{col_name}: {_get_type(v)}")

                return f"STRUCT<{', '.join(fields)}>"

            spark_function_name = f"schema_of_csv({snowpark_arg_names[0]})"

            match snowpark_args:
                case [csv_data]:
                    result_exp = _schema_of_csv(csv_data, snowpark_fn.lit(None))
                case [csv_data, options]:
                    result_exp = _schema_of_csv(csv_data, options)
                case _:
                    exception = ValueError("Unrecognized from_csv parameters")
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            result_type = StringType()
        case "schema_of_json":

            @cached_udf(
                input_types=[StringType()],
                return_type=StringType(),
            )
            def _infer_schema(json_str: str) -> str:
                import json

                def _struct_key(k: str) -> str:
                    escaped = k.replace("`", "``")
                    if escaped.strip() != k:
                        return f"`{escaped}`"
                    return escaped

                def _infer_pyspark_type(value) -> str:
                    if isinstance(value, str):
                        return "STRING"
                    elif isinstance(value, bool):
                        return "BOOLEAN"
                    elif isinstance(value, int):
                        return "BIGINT"
                    elif isinstance(value, float):
                        return "DOUBLE"
                    elif isinstance(value, list):
                        if not value:
                            return "ARRAY<STRING>"
                        element_types = [_infer_pyspark_type(elem) for elem in value]
                        common_type = _find_common_type(element_types)
                        return f"ARRAY<{common_type}>"
                    elif isinstance(value, dict):
                        if not value:
                            return "STRUCT<>"
                        return (
                            "STRUCT<"
                            + ", ".join(
                                f"{_struct_key(k)}: {value_typ}"
                                for k, v in value.items()
                                if k
                                and (value_typ := _infer_pyspark_type(v)) != "STRUCT<>"
                            )
                            + ">"
                        )
                    elif value is None:
                        return "STRING"
                    else:
                        return "STRING"

                def _find_common_type(types: list[str]) -> str:
                    if not types:
                        return "STRING"

                    if all(t == types[0] for t in types):
                        return types[0]

                    type_hierarchy = {
                        "BOOLEAN": 1,
                        "BIGINT": 2,
                        "DOUBLE": 3,
                        "STRING": 4,
                    }

                    if all(t.startswith("ARRAY<") and t.endswith(">") for t in types):
                        element_types = [
                            t[6:-1] for t in types
                        ]  # Remove "ARRAY<" and ">"
                        common_element_type = _find_common_type(element_types)
                        return f"ARRAY<{common_element_type}>"

                    if all(t.startswith("STRUCT<") and t.endswith(">") for t in types):
                        field_types = defaultdict(list)

                        for struct_type in types:
                            # Extract the content between STRUCT< and >
                            fields_str = struct_type[7:-1]

                            if not fields_str:  # Empty struct
                                continue

                            for field in fields_str.split(", "):
                                name, type_str = field.split(": ", 1)
                                field_types[name].append(type_str)

                        common_fields = []
                        for name, field_type_list in field_types.items():
                            common_field_type = _find_common_type(field_type_list)
                            common_fields.append(f"{name}: {common_field_type}")

                        if not common_fields:
                            return "STRUCT<>"

                        return "STRUCT<" + ", ".join(common_fields) + ">"

                    # If we have mixed types (some array, some struct, some primitive)
                    # or multiple primitive types, apply type promotion

                    # First, handle only basic types
                    basic_types = [t for t in types if t in type_hierarchy]
                    if basic_types:
                        max_type = max(
                            basic_types, key=lambda t: type_hierarchy.get(t, 0)
                        )
                        # If we only have basic types, return the promoted type
                        if len(basic_types) == len(types):
                            return max_type

                    # If we have a mix of basic and complex types, or multiple complex types
                    # Default to STRING as it can represent any type
                    return "STRING"

                try:
                    if not json_str.strip():
                        return "STRING"
                    obj = json.loads(json_str)
                    return _infer_pyspark_type(obj)
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"[snowpark_connect::invalid_input] Invalid JSON: {e}"
                    )

            if (
                exp.unresolved_function.arguments[0].WhichOneof("expr_type")
                != "literal"
            ):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.NON_FOLDABLE_INPUT] Cannot resolve "schema_of_json({",".join(snowpark_arg_names)})" due to data type mismatch: the input json should be a foldable "STRING" expression; however, got "{",".join(snowpark_arg_names)}"."""
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception
            result_exp = _infer_schema(snowpark_args[0])
            result_type = StringType()
        case "sec":
            spark_function_name = f"SEC({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                snowpark_fn.is_null(snowpark_args[0]), snowpark_fn.lit(NAN)
            ).otherwise(
                snowpark_fn.coalesce(
                    _divnull(snowpark_fn.lit(1.0), snowpark_fn.cos(snowpark_args[0])),
                    snowpark_fn.lit(INFINITY),
                )
            )
            result_type = DoubleType()
        case "second":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.second(
                    snowpark_fn.builtin("try_to_timestamp")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.second(
                    snowpark_fn.to_timestamp(snowpark_args[0])
                )
            # Spark 3.5.3: Second extends GetTimeField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L397
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "sentences":
            sentences_udf = register_cached_java_udf(
                "com.snowflake.snowpark_connect.udfs.SentencesUdf.sentences",
                ["STRING", "STRING", "STRING"],
                "VARIANT",
                packages=["com.snowflake:snowpark:1.15.0"],
            )

            result_exp = snowpark_fn.cast(
                sentences_udf(*snowpark_args), ArrayType(ArrayType(StringType()))
            )
            result_type = ArrayType(ArrayType(StringType()))
        case "sequence":
            all_integral = all(
                isinstance(arg.typ, _IntegralType) for arg in snowpark_typed_args
            )
            if not all_integral:
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.SEQUENCE_WRONG_INPUT_TYPES] Cannot resolve "sequence({snowpark_arg_names[0]}, {snowpark_arg_names[1]})" due to data type mismatch: `sequence` uses the wrong parameter type. The parameter type must conform to:
                        1. The start and stop expressions must resolve to the same type.
                        2. Otherwise, if start and stop expressions resolve to the "INTEGRAL" type, then the step expression must resolve to the same type.
                    """
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            result_type = _find_common_type([arg.typ for arg in snowpark_typed_args])
            result_exp = snowpark_fn.cast(
                snowpark_fn.sequence(*snowpark_args),
                ArrayType(result_type, contains_null=False),
            )
            result_exp = TypedColumn(result_exp, lambda: [ArrayType(result_type)])
        case "sha":
            sha_function = snowpark_fn.function("SHA1_HEX")
            result_exp = sha_function(snowpark_args[0])
            result_type = StringType(40)
        case "sha1":
            result_exp = snowpark_fn.sha1(snowpark_args[0])
            result_type = StringType(40)
        case "sha2":
            bit_values = [0, 224, 256, 384, 512]
            num_bits = unwrap_literal(exp.unresolved_function.arguments[1])
            if num_bits is None:
                if spark_sql_ansi_enabled:
                    exception = NumberFormatException(
                        f"""[CAST_INVALID_INPUT] The value {snowpark_arg_names[0]} of the type "{snowpark_typed_args[0].typ}" cannot be cast to "INT" because it is malformed. Correct the value as per the syntax, or change its target type."""
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
                    raise exception
                result_exp = snowpark_fn.lit(None)
                result_type = StringType()
            elif num_bits not in bit_values:
                exception = IllegalArgumentException(
                    f"""requirement failed: numBits {num_bits} is not in the permitted values (0, 224, 256, 384, 512)"""
                )
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception
            else:
                # 0 equivalent to 256 in PySpark, but is not allowed in Snowpark
                num_bits = 256 if num_bits == 0 else num_bits

                result_exp = snowpark_fn.sha2(snowpark_args[0], num_bits)
                result_type = StringType(128)
        case "shiftleft":
            expr, n = snowpark_args
            is_long = isinstance(snowpark_typed_args[0].typ, LongType)
            mask = 63 if is_long else 31
            masked_n = n.bitwiseAnd(snowpark_fn.lit(mask))

            expr_long = snowpark_fn.cast(expr, LongType())
            shifted = snowpark_fn.bitshiftleft(expr_long, masked_n)

            if is_long:
                result_type = LongType()
                result_exp = snowpark_fn.when(
                    shifted > snowpark_fn.lit(MAX_INT64),
                    shifted - snowpark_fn.lit(MAX_UINT64 + 1),
                ).otherwise(shifted)
            else:
                masked = shifted.bitwiseAnd(snowpark_fn.lit(MAX_UINT32))
                result_type = IntegerType()
                result_exp = snowpark_fn.when(
                    masked > snowpark_fn.lit(MAX_32BIT_SIGNED_INT),
                    masked - snowpark_fn.lit(MAX_UINT32 + 1),
                ).otherwise(masked)
        case "shiftright":
            expr, n = snowpark_args
            is_long = isinstance(snowpark_typed_args[0].typ, LongType)
            mask = 63 if is_long else 31
            masked_n = n.bitwiseAnd(snowpark_fn.lit(mask))

            expr_long = snowpark_fn.cast(expr, LongType())
            result_exp = snowpark_fn.bitshiftright(expr_long, masked_n)
            result_type = LongType() if is_long else IntegerType()
        case "shiftrightunsigned":
            expr, n = snowpark_args
            is_long = isinstance(snowpark_typed_args[0].typ, LongType)
            mask = 63 if is_long else 31
            masked_n = n.bitwiseAnd(snowpark_fn.lit(mask))

            unsigned_max = MAX_UINT64 if is_long else MAX_UINT32

            expr_long = snowpark_fn.cast(expr, LongType())
            expr_unsigned = snowpark_fn.when(
                expr_long < snowpark_fn.lit(0),
                expr_long + snowpark_fn.lit(unsigned_max + 1),
            ).otherwise(expr_long)

            shifted = snowpark_fn.bitshiftright(expr_unsigned, masked_n)

            if is_long:
                result_type = LongType()
                result_exp = snowpark_fn.when(
                    shifted > snowpark_fn.lit(MAX_INT64),
                    shifted - snowpark_fn.lit(unsigned_max + 1),
                ).otherwise(shifted)
            else:
                result_type = IntegerType()
                result_exp = snowpark_fn.when(
                    shifted > snowpark_fn.lit(MAX_32BIT_SIGNED_INT),
                    shifted - snowpark_fn.lit(unsigned_max + 1),
                ).otherwise(shifted)
        case "shuffle":
            arg_type = snowpark_typed_args[0].typ

            @cached_udf(
                input_types=[ArrayType()],
                return_type=ArrayType(),
            )
            def _shuffle_udf(array: list) -> list:
                import random

                random.shuffle(array)

                return array

            result_exp = snowpark_fn.cast(
                _shuffle_udf(snowpark_fn.cast(snowpark_args[0], ArrayType())),
                arg_type,
            )
            result_type = arg_type
        case "signum" | "sign":
            fn_name = function_name.upper()
            # Somehow, SIGNUM is upper case, but sign is lower case in PySpark.
            if fn_name == "SIGN":
                fn_name = "sign"

            spark_function_name = f"{fn_name}({snowpark_arg_names[0]})"

            if isinstance(snowpark_typed_args[0].typ, YearMonthIntervalType):
                # Use SQL expression for zero year-month interval comparison
                result_exp = (
                    snowpark_fn.when(
                        snowpark_args[0]
                        > snowpark_fn.sql_expr("INTERVAL '0-0' YEAR TO MONTH"),
                        snowpark_fn.lit(1.0),
                    )
                    .when(
                        snowpark_args[0]
                        < snowpark_fn.sql_expr("INTERVAL '0-0' YEAR TO MONTH"),
                        snowpark_fn.lit(-1.0),
                    )
                    .otherwise(snowpark_fn.lit(0.0))
                )
            elif isinstance(snowpark_typed_args[0].typ, DayTimeIntervalType):
                # Use SQL expression for zero day-time interval comparison
                result_exp = (
                    snowpark_fn.when(
                        snowpark_args[0]
                        > snowpark_fn.sql_expr("INTERVAL '0 0:0:0' DAY TO SECOND"),
                        snowpark_fn.lit(1.0),
                    )
                    .when(
                        snowpark_args[0]
                        < snowpark_fn.sql_expr("INTERVAL '0 0:0:0' DAY TO SECOND"),
                        snowpark_fn.lit(-1.0),
                    )
                    .otherwise(snowpark_fn.lit(0.0))
                )
            else:
                result_exp = snowpark_fn.when(
                    snowpark_args[0] == NAN, snowpark_fn.lit(NAN)
                ).otherwise(
                    snowpark_fn.cast(snowpark_fn.sign(snowpark_args[0]), DoubleType())
                )
            result_type = DoubleType()
        case "sin":
            spark_function_name = f"SIN({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.sin(snowpark_args[0])
            result_type = DoubleType()
        case "sinh":
            spark_function_name = f"SINH({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.sinh(snowpark_args[0])
            result_type = DoubleType()
        case "size":
            # When size function is called size has type integer in Spark
            # https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/collectionOperations.scala#L123
            result_type = IntegerType()

            v = snowpark_fn.cast(snowpark_args[0], VariantType())
            null_value = (
                snowpark_fn.lit(None) if spark_sql_ansi_enabled else snowpark_fn.lit(-1)
            )
            result_exp = (
                (
                    snowpark_fn.when(
                        snowpark_fn.is_array(v),
                        snowpark_fn.array_size(v),
                    )
                    .when(
                        snowpark_fn.is_object(v),
                        snowpark_fn.array_size(snowpark_fn.object_keys(v)),
                    )
                    .when(
                        snowpark_fn.is_null(v),
                        null_value,
                    )
                    .otherwise(snowpark_fn.lit(None))
                )
                .cast(result_type)
                .alias(f"SIZE({snowpark_args[0]})")
            )
        case "skewness":
            # SNOW-2177354
            if isinstance(snowpark_typed_args[0].typ, _NumericType):
                # In Snowflake we calculate skew using the sample skew formula.
                # In Spark they use the population skew formula.
                # The difference between these two requires some rearranging
                # which leads to the math shown below (in population_skewness)
                # Skew is also calculated on a minimum of 3 values and it also requires a non-zero stddev
                # as stddev is the denominator in some of the calculations. We return null on all zero stddev
                # datasets. Spark returns 0 on 2 values so we simply do the same here.
                # Formulas can be found at: https://www.macroption.com/skewness-formula/
                row_count = snowpark_fn.count(snowpark_args[0])
                sample_skewness = (
                    snowpark_fn.when(
                        snowpark_fn.stddev(snowpark_args[0]) == 0, snowpark_fn.lit(None)
                    )
                    .when(
                        (row_count >= 3),
                        snowpark_fn.skew(snowpark_args[0]),
                    )
                    .when(row_count == 2, snowpark_fn.lit(0))
                    .otherwise(snowpark_fn.lit(None))
                )
                population_skewness = (
                    snowpark_fn.when(sample_skewness.isNull(), snowpark_fn.lit(None))
                    .when(row_count == 2, snowpark_fn.lit(0))
                    .otherwise(
                        sample_skewness
                        * (row_count - 2)
                        / (
                            snowpark_fn.sqrt(row_count - 1)
                            * snowpark_fn.sqrt(row_count)
                        )
                    )
                )
                result_exp = population_skewness
            else:
                result_exp = snowpark_fn.skew(snowpark_fn.lit(None))
            result_type = DoubleType()
        case "slice":
            raise_error = _raise_error_helper(snowpark_typed_args[0].typ)
            spark_index = snowpark_args[1]
            arr_size = snowpark_fn.array_size(snowpark_args[0])
            slice_len = snowpark_args[2]
            result_exp = (
                snowpark_fn.when(
                    spark_index == 0,
                    raise_error(
                        snowpark_fn.lit(
                            "[snowpark_connect::invalid_index_of_zero_in_slice] Unexpected value for start in function slice: SQL array indices start at 1."
                        ),
                    ),
                )
                .when(
                    spark_index < 0,
                    snowpark_fn.array_slice(
                        snowpark_args[0],
                        arr_size + spark_index,
                        arr_size + spark_index + slice_len,
                    ),
                )
                .otherwise(
                    snowpark_fn.array_slice(
                        snowpark_args[0], spark_index - 1, spark_index + slice_len - 1
                    )
                )
            )
            result_exp = TypedColumn(result_exp, lambda: snowpark_typed_args[0].types)
        case "sort_array":
            if len(snowpark_args) == 2 and not isinstance(
                snowpark_typed_args[1].typ, BooleanType
            ):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 2 requires the "BOOLEAN" type, however "{snowpark_arg_names[1]}" has the type "{snowpark_typed_args[1].typ.simpleString().upper()}"'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            sort_asc = (
                unwrap_literal(exp.unresolved_function.arguments[1])
                if len(snowpark_args) == 2
                else True
            )
            result_exp = snowpark_fn.sort_array(
                *snowpark_args,
                nulls_first=sort_asc,
            )
            spark_function_name = (
                f"sort_array({snowpark_arg_names[0]}, {str(sort_asc).lower()})"
            )
            result_exp = TypedColumn(result_exp, lambda: snowpark_typed_args[0].types)
        case "soundex":
            value = snowpark_args[0]
            regexp_like_fn = snowpark_fn.function("REGEXP_LIKE")

            result_exp = (
                snowpark_fn.when(snowpark_fn.is_null(value), snowpark_fn.lit(None))
                .when(
                    snowpark_fn.trim(value) == "", snowpark_fn.lit("")
                )  # When string contains only whitespaces
                .when(
                    regexp_like_fn(value, "^[^a-zA-Z].*"), value
                )  # When string doesn't start with a letter
                .otherwise(snowpark_fn.soundex(snowpark_fn.upper(value)))
            )
            result_type = StringType()
        case "space":
            result_exp = snowpark_fn.builtin("space")(*snowpark_args)
            result_type = StringType()
        case "spark_partition_id":
            result_exp = snowpark_fn.lit(0)
            # Spark 3.5.3: SparkPartitionID defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/partitionTransforms.scala#L47
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "split":
            result_type = ArrayType(StringType())

            @cached_udf(
                input_types=[StringType(), StringType(), IntegerType()],
                return_type=result_type,
            )
            def _split(
                input: Optional[str], pattern: Optional[str], limit: Optional[int]
            ) -> Optional[list[str]]:
                if input is None or pattern is None:
                    return None

                import re

                try:
                    compiled_pattern = re.compile(pattern)
                except re.error:
                    raise ValueError(
                        f"[snowpark_connect::invalid_input] Failed to split string, provided pattern: {pattern} is invalid"
                    )

                if limit == 1:
                    return [input]

                if not input:
                    return [""]

                # A default of -1 is passed in PySpark, but RE needs it to be 0 to provide all splits.
                # In PySpark, the limit also indicates the max size of the resulting array, but in RE
                # the remainder is returned as another element.
                maxsplit = limit - 1 if limit > 0 else 0

                if len(pattern) == 0:
                    return list(input) if limit <= 0 else list(input)[:limit]

                match pattern:
                    case "|":
                        split_result = compiled_pattern.split(input, 0)
                        input_limit = limit + 1 if limit > 0 else len(split_result)
                        return (
                            split_result
                            if input_limit == 0
                            else split_result[1:input_limit]
                        )
                    case "$":
                        return [input, ""] if maxsplit >= 0 else [input]
                    case "^":
                        return [input]
                    case _:
                        return compiled_pattern.split(input, maxsplit)

            def split_string(str_: Column, pattern: Column, limit: Column):
                native_split = _split(str_, pattern, limit)
                # When pattern is a literal and doesn't contain any regex special characters
                # And when limit is less than or equal to 0
                # Native Snowflake Split function is used to optimise performance
                if isinstance(pattern._expression, Literal):
                    pattern_value = pattern._expression.value

                    if pattern_value is None:
                        return snowpark_fn.lit(None)

                    # Optimization: treat escaped regex that resolves to a pure literal delimiter
                    # - Single char: "\\."
                    # - Multi char: e.g., "\\.505\\."
                    if re.fullmatch(r"(?:\\.)+", pattern_value):
                        literal_delim = re.sub(r"\\(.)", r"\1", pattern_value)
                        return snowpark_fn.when(
                            limit <= 0,
                            snowpark_fn.split(
                                str_, snowpark_fn.lit(literal_delim)
                            ).cast(result_type),
                        ).otherwise(native_split)

                    is_regexp = re.match(
                        ".*[\\[\\.\\]\\*\\?\\+\\^\\$\\{\\}\\|\\(\\)\\\\].*",
                        pattern_value,
                    )
                    is_empty = len(pattern_value) == 0

                    if not is_empty and not is_regexp:
                        return snowpark_fn.when(
                            limit <= 0,
                            snowpark_fn.split(str_, pattern).cast(result_type),
                        ).otherwise(native_split)

                return native_split

            match snowpark_args:
                case [str_, pattern]:
                    spark_function_name = (
                        f"split({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, -1)"
                    )
                    result_exp = split_string(str_, pattern, snowpark_fn.lit(-1))
                case [str_, pattern, limit]:  # noqa: F841
                    result_exp = split_string(str_, pattern, limit)
                case _:
                    exception = ValueError(
                        f"Invalid number of arguments to {function_name}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
        case "split_part":
            # Check for index 0 and throw error to match PySpark behavior
            raise_error = _raise_error_helper(StringType(), SparkRuntimeException)
            result_exp = snowpark_fn.when(
                snowpark_args[2] == 0,
                raise_error(
                    snowpark_fn.lit(
                        "[INVALID_INDEX_OF_ZERO] The index 0 is invalid. An index shall be either < 0 or > 0 (the first element has index 1)."
                    )
                ),
            ).otherwise(snowpark_fn.call_function("split_part", *snowpark_args))
            result_type = StringType()
        case "sqrt":
            spark_function_name = f"SQRT({snowpark_arg_names[0]})"
            sqrt_arg = snowpark_args[0]
            if isinstance(snowpark_typed_args[0].typ, StringType):
                sqrt_arg = snowpark_fn.try_cast(snowpark_args[0], DoubleType())
            elif not isinstance(snowpark_typed_args[0].typ, _NumericType):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "SQRT({snowpark_arg_names[0]})" due to data type mismatch: Parameter 1 requires the "DOUBLE" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}"."""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            result_exp = (
                snowpark_fn.when(sqrt_arg < 0, NAN)
                .when(sqrt_arg.isNull(), snowpark_fn.lit(None))
                .otherwise(snowpark_fn.sqrt(sqrt_arg))
            )
            result_type = DoubleType()
        case "stack":
            # In the stack function, we always want to produce `num_rows` amount of rows. The amount of columns
            # will depend on the input specified. All arguments in the input (apart from the first one that specifies
            # `num_rows`) must be the same type.
            if len(exp.unresolved_function.arguments) <= 1:
                exception = AnalysisException(
                    f"""
                    [WRONG_NUM_ARGS.WITHOUT_SUGGESTION] The `stack` requires > 1 parameters but the actual number is {len(exp.unresolved_function.arguments)}.
                    """
                )
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception
            num_rows = unwrap_literal(exp.unresolved_function.arguments[0])
            if not isinstance(snowpark_typed_args[0].typ, IntegerType):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{snowpark_arg_names[0]}" due to data type mismatch: Parameter 1 requires the "INT" type, however "{num_rows}" has the type "{snowpark_typed_args[0].typ}"."""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            num_arguments = len(snowpark_args) - 1
            num_cols = math.ceil(num_arguments / num_rows)
            spark_col_names = [f"col{i}" for i in range(num_cols)]
            spark_col_types = [arg.typ for arg in snowpark_typed_args[1:]]

            for i, arg in enumerate(spark_col_types):
                if arg != spark_col_types[i % num_cols] and not isinstance(
                    arg, NullType
                ):
                    exception = AnalysisException(
                        f"""[DATATYPE_MISMATCH.STACK_COLUMN_DIFF_TYPES] Cannot resolve "stack({snowpark_arg_names[0]})" due to data type mismatch: The data type of the column ({snowpark_arg_names[0]}) do not have the same type."""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                if isinstance(arg, NullType):
                    spark_col_types[i] = VariantType()
                    snowpark_args[i + 1] = snowpark_fn.cast(
                        snowpark_args[i + 1], VariantType()
                    )

            schema = StructType(
                [
                    StructField(spark_col_name, spark_col_types, True)
                    for spark_col_name, spark_col_types in zip(
                        spark_col_names, spark_col_types
                    )
                ]
            )

            class Stack:
                def process(self, num_rows, col_count, *cols):
                    from itertools import zip_longest

                    def clean(val):
                        return None if getattr(val, "is_sql_null", False) else val

                    cols = tuple(clean(v) for v in cols)

                    total_needed = num_rows * col_count
                    # total spots we need to occupy is amount of rows (num_rows) multiplied by the number of columns
                    # which was previously calculated as the ceiling of the length of all arguments (minus 1) divided by the amount of rows.
                    if len(cols) < total_needed:
                        cols = cols + (None,) * (total_needed - len(cols))
                    it = iter(cols)
                    yield from zip_longest(*[it] * col_count, fillvalue=None)

            stack_udtf = cached_udtf(
                Stack,
                output_schema=schema,
                input_types=[IntegerType(), IntegerType()] + spark_col_types,
            )

            result_exp = snowpark_fn.call_table_function(
                stack_udtf.name,
                snowpark_args[0],
                snowpark_fn.lit(num_cols),
                *snowpark_args[1:],
            )
            result_type = spark_col_types[0:num_cols]
        case "startswith":
            result_exp = snowpark_args[0].startswith(snowpark_args[1])
            result_type = BooleanType()
        case "stddev":
            stddev_argument = snowpark_args[0]
            if not isinstance(snowpark_typed_args[0].typ, _NumericType):
                if isinstance(snowpark_typed_args[0].typ, StringType):
                    stddev_argument = snowpark_fn.try_cast(
                        snowpark_args[0], DoubleType()
                    )
                else:
                    exception = AnalysisException(
                        f"""AnalysisException: [DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "stddev({snowpark_arg_names[0]}" due to data type mismatch: Parameter 1 requires the "DOUBLE" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".;"""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
            result_exp = snowpark_fn.stddev(stddev_argument)
            result_type = DoubleType()
        case "stddev_pop":
            stddev_pop_argument = snowpark_args[0]
            if not isinstance(snowpark_typed_args[0].typ, _NumericType):
                if isinstance(snowpark_typed_args[0].typ, StringType):
                    stddev_pop_argument = snowpark_fn.try_cast(
                        snowpark_args[0], DoubleType()
                    )
                else:
                    exception = AnalysisException(
                        f"""AnalysisException: [DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "stddev_pop({snowpark_arg_names[0]}" due to data type mismatch: Parameter 1 requires the "DOUBLE" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".;"""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
            result_exp = snowpark_fn.stddev_pop(stddev_pop_argument)
            result_type = DoubleType()
        case "stddev_samp" | "std":
            stddev_samp_argument = snowpark_args[0]
            if not isinstance(snowpark_typed_args[0].typ, _NumericType):
                if isinstance(snowpark_typed_args[0].typ, StringType):
                    stddev_samp_argument = snowpark_fn.try_cast(
                        snowpark_args[0], DoubleType()
                    )
                else:
                    exception = AnalysisException(
                        f"""AnalysisException: [DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "stddev_samp({snowpark_arg_names[0]}" due to data type mismatch: Parameter 1 requires the "DOUBLE" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".;"""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
            result_exp = snowpark_fn.stddev_samp(stddev_samp_argument)
            result_type = DoubleType()
        case "str_to_map":
            value, pair_delim_, kv_delim_ = snowpark_args

            allow_duplicate_keys = (
                global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            )

            @cached_udf(
                input_types=[BooleanType(), StringType(), StringType(), StringType()],
                return_type=VariantType(),
            )
            def _str_to_map(
                allow_dups: bool,
                s: Optional[str],
                pair_delim: Optional[str],
                kv_delim: Optional[str],
            ) -> Optional[dict]:
                if any(x is None for x in (s, pair_delim, kv_delim)):
                    return None

                if s == "":
                    return {"": None}

                import re

                pairs = re.split(pair_delim, s)
                kv_pairs = [re.split(kv_delim, pair) for pair in pairs]

                result_map = {}

                for kv_pair in kv_pairs:
                    if len(kv_pair) == 0:
                        continue
                    elif len(kv_pair) == 1:
                        key = kv_pair[0]
                        val = None
                    elif len(kv_pair) == 2:
                        key, val = kv_pair
                    else:
                        # More than 2 elements: first is key, rest joined as value
                        key = kv_pair[0]
                        val = kv_delim.join(kv_pair[1:])

                    if key in result_map and not allow_dups:
                        raise ValueError(
                            f"[snowpark_connect::invalid_input] {DUPLICATE_KEY_FOUND_ERROR_TEMPLATE.format(key=key)}"
                        )

                    result_map[key] = val

                return result_map

            result_exp = snowpark_fn.cast(
                _str_to_map(
                    snowpark_fn.lit(allow_duplicate_keys), value, pair_delim_, kv_delim_
                ),
                MapType(StringType(), StringType()),
            )
            result_type = MapType(StringType(), StringType())
        case "struct":
            if (
                len(exp.unresolved_function.arguments) == 1
                and exp.unresolved_function.arguments[0].WhichOneof("expr_type")
                == "unresolved_star"
            ):
                (_, result_exp) = map_unresolved_star_as_single_column(
                    exp.unresolved_function.arguments[0], column_mapping, typer
                )
            else:

                def _f_name(index: int, resolved_name: str) -> str:
                    match exp.unresolved_function.arguments[index].WhichOneof(
                        "expr_type"
                    ):
                        case "alias":
                            # aliases are used for field names in struct schema
                            return exp.unresolved_function.arguments[index].alias.name[
                                0
                            ]
                        case "unresolved_attribute":
                            return resolved_name
                        case "unresolved_named_lambda_variable":
                            return exp.unresolved_function.arguments[
                                index
                            ].unresolved_named_lambda_variable.name_parts[0]

                    return f"col{index + 1}"

                fields_cols = list(zip(snowpark_arg_names, snowpark_typed_args))
                field_types = [
                    StructField(_f_name(idx, name), col.typ, _is_column=False)
                    for idx, (name, col) in enumerate(fields_cols)
                ]
                result_exp = snowpark_fn.object_construct_keep_null(
                    *[
                        name_with_col
                        for idx, (name, typed_col) in enumerate(fields_cols)
                        for name_with_col in (
                            snowpark_fn.lit(_f_name(idx, name)),
                            typed_col.column(to_semi_structure=True),
                        )
                    ]
                )
                result_type = StructType(field_types)
                result_exp = snowpark_fn.cast(result_exp, result_type)
                spark_field_names = ", ".join(
                    resolved_name for (resolved_name, _) in fields_cols
                )
                spark_function_name = f"struct({spark_field_names})"
        case "substring" | "substr":
            # Semantic difference: Spark and Snowflake handle negative positions differently
            # when abs(negative_pos) > string_length.
            #
            # Both support negative positions (counting from end), converting them to positive
            # positions using: actual_pos = length + pos + 1
            #
            # However, when this computed position < 1:
            # - Snowflake: returns empty string
            # - Spark: clamps position to 1 AND adjusts the length by (computed_pos - 1)
            #
            # Example: substr("param", -6, 2) where length=5
            #   computed_pos = 5 + (-6) + 1 = 0
            #   Spark: pos=1, len=max(2 + 0 - 1, 0) = max(1, 0) = 1 → returns "p"
            #   Snowflake: would return empty string
            if len(snowpark_args) >= 2:
                string_arg = snowpark_args[0]
                pos_arg = snowpark_args[1]

                if len(snowpark_args) == 3:
                    length_arg = snowpark_args[2]

                    # Optimization: when pos and length are positive integer literals,
                    # Spark and Snowflake behave identically — skip the CASE/WHEN
                    # boundary checks and emit simple substring(col, pos, len).
                    if (
                        isinstance(pos_arg._expression, Literal)
                        and isinstance(pos_arg._expression.value, int)
                        and pos_arg._expression.value > 0
                        and isinstance(length_arg._expression, Literal)
                        and isinstance(length_arg._expression.value, int)
                        and length_arg._expression.value >= 0
                    ):
                        result_exp = snowpark_fn.substring(
                            string_arg, pos_arg, length_arg
                        )
                    else:
                        # Full boundary-checking logic for dynamic or non-positive arguments.
                        # Spark and Snowflake differ when abs(negative_pos) > string_length:
                        # Spark clamps position to 1 and adjusts length; Snowflake returns empty.
                        string_length = snowpark_fn.length(string_arg)

                        # For negative positions: compute actual position = length + pos + 1
                        # For position 0: treat as position 1
                        # For positive positions: use as-is
                        computed_pos = (
                            snowpark_fn.when(
                                pos_arg < 0,
                                string_length + pos_arg + snowpark_fn.lit(1),
                            )
                            .when(pos_arg == 0, snowpark_fn.lit(1))
                            .otherwise(pos_arg)
                        )

                        # When computed_pos < 1 (only from very negative positions), clamp to 1 and adjust length
                        adjusted_length = snowpark_fn.when(
                            computed_pos < 1,
                            snowpark_fn.greatest(
                                length_arg + computed_pos - snowpark_fn.lit(1),
                                snowpark_fn.lit(0),
                            ),
                        ).otherwise(length_arg)
                        clamped_pos = snowpark_fn.when(
                            computed_pos < 1, snowpark_fn.lit(1)
                        ).otherwise(computed_pos)

                        result_exp = snowpark_fn.substring(
                            string_arg, clamped_pos, adjusted_length
                        )
                else:
                    # For 2-arg version, also handle position 0
                    adjusted_pos = snowpark_fn.when(
                        pos_arg == 0, snowpark_fn.lit(1)
                    ).otherwise(pos_arg)
                    result_exp = snowpark_fn.substring(string_arg, adjusted_pos)
            else:
                result_exp = snowpark_fn.substring(*snowpark_args)
            # Result type matches the input type (StringType or BinaryType)
            result_type = (
                snowpark_typed_args[0].typ if snowpark_typed_args else StringType()
            )
        case "substring_index":
            value, delim, count = snowpark_args

            value = snowpark_fn.split(value, delim)
            array_size = snowpark_fn.array_size(value)

            value = (
                snowpark_fn.when(count == 0, snowpark_fn.array_construct())
                .when(
                    count > 0, snowpark_fn.array_slice(value, snowpark_fn.lit(0), count)
                )
                .otherwise(snowpark_fn.array_slice(value, count, array_size))
            )

            result_exp = snowpark_fn.array_to_string(value, delim)
            result_type = StringType()
        case "sum":
            sum_fn = snowpark_fn.sum
            input_type = snowpark_typed_args[0].typ
            if exp.unresolved_function.is_distinct:
                spark_function_name = f"sum(DISTINCT {snowpark_arg_names[0]})"
                sum_fn = snowpark_fn.sum_distinct

            arg = snowpark_args[0]
            if isinstance(input_type, StringType):
                arg = snowpark_fn.cast(arg, DoubleType())

            if isinstance(input_type, DecimalType):
                result_type = _bounded_decimal(
                    input_type.precision + 10, input_type.scale
                )
            elif isinstance(input_type, _IntegralType):
                result_type = LongType()
            else:
                result_type = DoubleType()

            if isinstance(input_type, _IntegralType) and not is_window_enabled():
                raw_sum = sum_fn(arg)
                wrapped_sum = apply_arithmetic_overflow_with_ansi_check(
                    raw_sum, result_type, spark_sql_ansi_enabled, "add"
                )
                result_exp = _resolve_aggregate_exp(
                    wrapped_sum,
                    result_type,
                )
            else:
                result_exp = _resolve_aggregate_exp(
                    sum_fn(arg),
                    result_type,
                )
        case "tan":
            spark_function_name = f"TAN({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.tan(snowpark_args[0])
            result_type = DoubleType()
        case "tanh":
            spark_function_name = f"TANH({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.tanh(snowpark_args[0])
            result_type = DoubleType()
        case "timestamp_add":
            # Added to DataFrame functions in 4.0.0 - but can be called from SQL in 3.5.3.
            spark_function_name = f"timestampadd({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, {snowpark_arg_names[2]})"

            typ = snowpark_typed_args[2].typ
            result_type = (
                typ
                if isinstance(typ, TimestampType)
                else TimestampType(snowpark.types.TimestampTimeZone.LTZ)
            )

            result_exp = snowpark_fn.cast(
                snowpark_fn.dateadd(
                    unwrap_literal(exp.unresolved_function.arguments[0]),
                    snowpark_args[1],
                    snowpark_args[2],
                ),
                result_type,
            )
        case "timestamp_diff":
            # Added to DataFrame functions in 4.0.0 - but can be called from SQL in 3.5.3.
            spark_function_name = f"timestampdiff({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, {snowpark_arg_names[2]})"
            result_exp = snowpark_fn.datediff(
                unwrap_literal(exp.unresolved_function.arguments[0]),
                snowpark_args[1],
                snowpark_args[2],
            )
            result_exp = TypedColumn(result_exp, lambda: [LongType()])
        case "timestamp_micros":
            result_exp = snowpark_fn.cast(
                snowpark_fn.to_timestamp(snowpark_args[0], 6),
                TimestampType(snowpark.types.TimestampTimeZone.LTZ),
            )
            result_type = TimestampType(snowpark.types.TimestampTimeZone.LTZ)
        case "timestamp_millis":
            if isinstance(snowpark_typed_args[0].typ, NullType):
                result_exp = snowpark_fn.lit(None)
            elif not isinstance(snowpark_typed_args[0].typ, _IntegralType):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "timestamp_millis({snowpark_arg_names[0]}" due to data type mismatch: Parameter 1 requires the "INTEGRAL" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            else:
                result_exp = snowpark_fn.cast(
                    snowpark_fn.to_timestamp(snowpark_args[0] * 1_000, 6),
                    TimestampType(snowpark.types.TimestampTimeZone.LTZ),
                )
            result_type = TimestampType(snowpark.types.TimestampTimeZone.LTZ)
        case "timestamp_seconds":
            # Spark allows seconds to be fractional. Snowflake does not allow that
            # even though the documentation explicitly says that it does.
            # As a workaround, use integer milliseconds instead of fractional seconds.
            if isinstance(snowpark_typed_args[0].typ, NullType):
                result_exp = snowpark_fn.lit(None)
            elif not isinstance(snowpark_typed_args[0].typ, _NumericType):
                exception = AnalysisException(
                    f"""AnalysisException: [DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{function_name}({snowpark_arg_names[0]})" due to data type mismatch: Parameter 1 requires the "NUMERIC" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".;"""
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            else:
                result_exp = snowpark_fn.cast(
                    snowpark_fn.to_timestamp(
                        snowpark_fn.cast(snowpark_args[0] * 1_000_000, LongType()), 6
                    ),
                    TimestampType(snowpark.types.TimestampTimeZone.LTZ),
                )
            result_type = TimestampType(snowpark.types.TimestampTimeZone.LTZ)
        case "to_char" | "to_varchar":
            # The structure of the Spark format string must match: [MI|S] [$] [0|9|G|,]* [.|D] [0|9]* [$] [PR|MI|S]
            # Note the grammar above was retrieved from an error message from PySpark, but it is not entirely accurate.
            # - "MI", and "S" may only be used once at the beginning or end of the format string.
            # - "$" may only be used once before all digits in the number format (but after "MI" or "S").
            # - There must be a "0" or "9" to both the left and right of a comma (,) or "G".
            # - The format string must not be empty, and there must be at least one "0", or "9" in the format string.
            # PySpark itself checks the format string for validity before it gets to SAS, so we can make the assumption that all
            # of the above are true.

            # TRANSLATE SPARK FORMAT STRING TO EQUIVALENT SNOWFLAKE FORMAT STRING
            spark_fmt = snowpark_args[1]
            spark_fmt_value = _resolve_foldable_string_expression(
                arg_col=spark_fmt,
                arg_name=snowpark_arg_names[1],
                spark_function_name=function_name,
                session=session,
            )

            if spark_fmt_value is not None:
                PR_used = spark_fmt_value.endswith("PR")
                MI_at_start = spark_fmt_value.startswith("MI")
                S_at_start = spark_fmt_value.startswith("S")
                MI_at_end = spark_fmt_value.endswith("MI")
                S_at_end = spark_fmt_value.endswith("S")

                snowpark_fmt_value = spark_fmt_value.replace("PR", "")
                snowpark_fmt_value = snowpark_fmt_value.replace("MI", "")
                snowpark_fmt_value = snowpark_fmt_value.replace("S", "")

                currency_used = snowpark_fmt_value.startswith("$")
                snowpark_fmt_value = snowpark_fmt_value.replace("$", "")

                snowpark_fmt_value = snowpark_fmt_value.replace(".", "D")

                decimal_used = "D" in snowpark_fmt_value
                if decimal_used:
                    before_decimal, after_decimal = snowpark_fmt_value.split("D", 1)
                else:
                    before_decimal, after_decimal = snowpark_fmt_value, ""

                before_decimal_empty = before_decimal == ""
                after_demical_empty = after_decimal == ""

                first_digit_match = re.match(r"^(0|9)", before_decimal)
                first_digit = first_digit_match.group(1) if first_digit_match else ""
                before_decimal = re.sub("[09]", first_digit, before_decimal)

                if decimal_used:
                    decimal_separator = "" if after_demical_empty else "D"
                    snowpark_fmt_value = (
                        f"{before_decimal}"
                        f"{decimal_separator}"
                        f"{after_decimal.replace('9', '0')}"
                    )
                else:
                    # When a number is 0, Spark does not print the digit when the "9"
                    # format element is used and is not followed by a decimal point.
                    # Snowflake does print the digit. We use "B" to match Spark.
                    snowpark_fmt_value = f"B{before_decimal}"

                # Snowflake inserts a leading sign space by default. Add explicit "S"
                # then strip '+' later so Spark-like positive formatting is preserved.
                snowpark_fmt_value = f"{snowpark_fmt_value}S"
                snowpark_fmt = snowpark_fn.lit(snowpark_fmt_value)

                # FORMAT THE NUMBER AND POST-PROCESS TO MATCH SPARK
                formatted = snowpark_fn.to_char(
                    snowpark_fn.abs(snowpark_args[0]), snowpark_fmt
                )
                formatted = snowpark_fn.replace(formatted, "+")

                if currency_used:
                    formatted = snowpark_fn.concat(snowpark_fn.lit("$"), formatted)

                positive_sign = (
                    snowpark_fn.lit("+")
                    if (S_at_start or S_at_end)
                    else snowpark_fn.lit(" ")
                )

                if MI_at_start or S_at_start:
                    formatted = snowpark_fn.when(
                        snowpark_args[0] < 0,
                        snowpark_fn.concat(snowpark_fn.lit("-"), formatted),
                    ).otherwise(snowpark_fn.concat(positive_sign, formatted))
                elif MI_at_end or S_at_end:
                    formatted = snowpark_fn.when(
                        snowpark_args[0] < 0,
                        snowpark_fn.concat(formatted, snowpark_fn.lit("-")),
                    ).otherwise(snowpark_fn.concat(formatted, positive_sign))

                # Edge case where Spark prints a 0 before the decimal point.
                if MI_at_start and (not currency_used) and before_decimal_empty:
                    formatted = snowpark_fn.regexp_replace(formatted, r" \.", "0.")

                if PR_used:
                    # Spark wraps negatives in <> and left-aligns positives with 2 spaces.
                    formatted = snowpark_fn.when(
                        snowpark_args[0] < 0,
                        snowpark_fn.concat(
                            snowpark_fn.lit("<"),
                            formatted,
                            snowpark_fn.lit(">"),
                        ),
                    ).otherwise(snowpark_fn.concat(formatted, snowpark_fn.lit("  ")))

                # Edge case: decimal used with no trailing placeholders.
                if decimal_used and after_demical_empty:
                    result_exp = snowpark_fn.concat(formatted, snowpark_fn.lit(" "))
                else:
                    result_exp = formatted
            else:
                result_exp = snowpark_fn.lit(None)
            result_type = StringType()
        case "to_csv":
            snowpark_args = [
                typed_arg.column(to_semi_structure=True)
                for typed_arg in snowpark_typed_args
            ]

            timezone_conf = global_config.get("spark.sql.session.timeZone")

            # Objects do not preserve keys order in Snowflake, so we need to pass them in the array
            # Not all the types are preserved in Snowflake Object, timestamps and dates are converted to strings
            # to properly format them types have to be passed as argument
            @cached_udf(
                input_types=[VariantType(), ArrayType(), ArrayType(), VariantType()],
                return_type=StringType(),
                packages=["jpype1"],
            )
            def _to_csv(
                col: dict, keys: list, types: list, options: Optional[dict]
            ) -> str:
                import datetime

                import jpype

                if options is not None:
                    if not isinstance(options, dict):
                        raise TypeError(
                            "[snowpark_connect::invalid_input] [INVALID_OPTIONS.NON_MAP_FUNCTION] Invalid options: Must use the `map()` function for options."
                        )

                    python_to_snowflake_type = {
                        "str": "STRING",
                        "bool": "BOOLEAN",
                        "dict": "OBJECT",
                        "list": "ARRAY",
                    }

                    for k, v in options.items():
                        if not isinstance(k, str) or not isinstance(v, str):
                            k_type = python_to_snowflake_type.get(
                                type(k).__name__, type(k).__name__.upper()
                            )
                            v_type = python_to_snowflake_type.get(
                                type(v).__name__, type(v).__name__.upper()
                            )
                            raise TypeError(
                                f'[snowpark_connect::type_mismatch] [INVALID_OPTIONS.NON_STRING_TYPE] Invalid options: A type of keys and values in `map()` must be string, but got "MAP<{k_type}, {v_type}>".'
                            )

                options = options or {}
                lowercased_options = {
                    key.lower(): value for key, value in options.items()
                }

                sep = lowercased_options.get("sep") or (
                    lowercased_options.get("delimiter") or ","
                )
                quote = lowercased_options.get("quote") or '"'
                quote_all = lowercased_options.get("quoteall", "false")
                escape = lowercased_options.get("escape") or "\\"

                ignore_leading_white_space = lowercased_options.get(
                    "ignoreleadingwhitespace", "true"
                )
                ignore_trailing_white_space = lowercased_options.get(
                    "ignoretrailingwhitespace", "true"
                )
                null_value = lowercased_options.get("nullvalue") or ""
                empty_value = lowercased_options.get("emptyvalue") or '""'
                char_to_escape_quote_escaping = (
                    lowercased_options.get("chartoescapequoteescaping") or escape
                )

                date_format = lowercased_options.get("dateformat") or "yyyy-MM-dd"
                timestamp_format = (
                    lowercased_options.get("timestampformat")
                    or "yyyy-MM-dd'T'HH:mm:ss[.SSS][XXX]"
                )
                timestamp_NTZ_format = (
                    lowercased_options.get("timestampntzformat")
                    or "yyyy-MM-dd'T'HH:mm:ss[.SSS]"
                )

                def to_boolean(value: str) -> bool:
                    return value.lower() == "true"

                quote_all = to_boolean(quote_all)
                ignore_leading_white_space = to_boolean(ignore_leading_white_space)
                ignore_trailing_white_space = to_boolean(ignore_trailing_white_space)

                def escape_str(value: str) -> str:
                    escape_quote = escape + quote if escape != quote else escape
                    return (
                        value.replace(escape, char_to_escape_quote_escaping + escape)
                        .replace(quote, escape_quote)
                        .replace("\r", "\\r")
                    )

                def escape_and_quote_string(value) -> str:
                    if quote_all:
                        return f"{quote}{escape_str(str(value))}{quote}"
                    return str(value)

                time_types = ("date", "timestamp", "timestamp_ntz")
                maps_timestamps = any(
                    python_type in time_types for python_type in types
                )

                # Multiple execution of the UDF are done within the same process, that's why we need to check if the JVM was not already started
                if maps_timestamps and not jpype.isJVMStarted():
                    jpype.startJVM()

                if maps_timestamps:
                    ZonedDateTime = jpype.JClass("java.time.ZonedDateTime")
                    ZoneId = jpype.JClass("java.time.ZoneId")
                    DateTimeFormatter = jpype.JClass(
                        "java.time.format.DateTimeFormatter"
                    )
                    Instant = jpype.JClass("java.time.Instant")
                    LocalDate = jpype.JClass("java.time.LocalDate")
                    LocalDateTime = jpype.JClass("java.time.LocalDateTime")
                    timestamp_formatter = DateTimeFormatter.ofPattern(timestamp_format)
                    timestamp_ntz_formatter = DateTimeFormatter.ofPattern(
                        timestamp_NTZ_format
                    )
                    date_formatter = DateTimeFormatter.ofPattern(date_format)

                result = []
                for key, python_type in zip(keys, types):
                    value = col.get(key)
                    if value is None:
                        result.append(escape_and_quote_string(null_value))
                    elif python_type in ("date", "timestamp", "timestamp_ntz"):
                        match python_type:
                            case "date":
                                value = datetime.datetime.strptime(value, "%Y-%m-%d")
                                local_date = LocalDate.of(
                                    value.year, value.month, value.day
                                )
                                formatted_date = date_formatter.format(local_date)
                                result.append(escape_and_quote_string(formatted_date))
                            case "timestamp":
                                try:
                                    value = datetime.datetime.strptime(
                                        value, "%Y-%m-%d %H:%M:%S.%f %z"
                                    )
                                except ValueError:
                                    # Fallback to the format without microseconds
                                    value = datetime.datetime.strptime(
                                        value, "%Y-%m-%d %H:%M:%S %z"
                                    )
                                instant = Instant.ofEpochMilli(
                                    int(value.timestamp() * 1000)
                                )
                                zdt = ZonedDateTime.ofInstant(
                                    instant, ZoneId.of(timezone_conf)
                                )
                                str_value = timestamp_formatter.format(zdt)
                                result.append(escape_and_quote_string(str_value))
                            case "timestamp_ntz":
                                try:
                                    value = datetime.datetime.strptime(
                                        value, "%Y-%m-%d %H:%M:%S.%f"
                                    )
                                except ValueError:
                                    # Fallback to the format without microseconds
                                    value = datetime.datetime.strptime(
                                        value, "%Y-%m-%d %H:%M:%S"
                                    )
                                timestamp_ntz = LocalDateTime.of(
                                    value.year,
                                    value.month,
                                    value.day,
                                    value.hour,
                                    value.minute,
                                    value.second,
                                    value.microsecond * 1000,
                                )
                                str_value = timestamp_ntz_formatter.format(
                                    timestamp_ntz
                                )
                                result.append(escape_and_quote_string(str_value))
                            case _:
                                raise ValueError(
                                    f"[snowpark_connect::type_mismatch] Unable to determine type for value: {python_type}"
                                )
                    elif isinstance(value, str):
                        strip_value = (
                            value.lstrip() if ignore_leading_white_space else value
                        )
                        strip_value = (
                            strip_value.rstrip()
                            if ignore_trailing_white_space
                            else strip_value
                        )
                        if strip_value == "":
                            result.append(escape_and_quote_string(empty_value))
                        elif (
                            any(c in value for c in (sep, "\r", "\n", quote))
                            or quote_all
                        ):
                            strip_value = escape_str(strip_value)
                            result.append(quote + strip_value + quote)
                        else:
                            result.append(escape_and_quote_string(strip_value))
                    elif isinstance(value, bool):
                        result.append(escape_and_quote_string(str(value).lower()))
                    else:
                        result.append(escape_and_quote_string(str(value)))

                return sep.join(result)

            spark_function_name = f"to_csv({snowpark_arg_names[0]})"

            if len(snowpark_arg_names) > 1 and snowpark_arg_names[1].startswith(
                "named_struct"
            ):
                exception = TypeError(
                    "[INVALID_OPTIONS.NON_MAP_FUNCTION] Invalid options: Must use the `map()` function for options."
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception

            def get_snowpark_type_name(snowpark_type: DataType) -> str:
                return (
                    (
                        "timestamp"
                        if not snowpark_type.tz == snowpark.types.TimestampTimeZone.NTZ
                        else "timestamp_ntz"
                    )
                    if snowpark_type == TimestampType()
                    else snowpark_type.type_name().lower()
                )

            field_names = snowpark_fn.array_construct(
                *[
                    snowpark_fn.lit(value)
                    for value in snowpark_typed_args[0].typ.fieldNames
                ]
            )
            field_types = snowpark_fn.array_construct(
                *[
                    snowpark_fn.lit(get_snowpark_type_name(value.datatype))
                    for value in snowpark_typed_args[0].typ.fields
                ]
            )
            match snowpark_args:
                case [csv_data]:
                    result_exp = _to_csv(
                        csv_data, field_names, field_types, snowpark_fn.lit(None)
                    )
                case [csv_data, options]:
                    result_exp = _to_csv(csv_data, field_names, field_types, options)
                case _:
                    exception = ValueError("Unrecognized from_csv parameters")
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            result_type = StringType()
        case "to_date":
            if not spark_sql_ansi_enabled:
                function_name = "try_to_date"
            match snowpark_typed_args[0].typ:
                case DateType():
                    result_exp = snowpark_args[0]
                case TimestampType():
                    result_exp = snowpark_fn.to_date(snowpark_args[0])
                case StringType():
                    result_exp = (
                        snowpark_fn.builtin(function_name)(
                            snowpark_args[0],
                            snowpark_fn.lit(
                                map_spark_timestamp_format_expression(
                                    exp.unresolved_function.arguments[1],
                                    snowpark_typed_args[0].typ,
                                )
                            ),
                        )
                        if len(snowpark_args) > 1
                        else snowpark_fn.builtin(function_name)(*snowpark_args)
                    )
                case NullType():
                    result_exp = snowpark_fn.lit(None)
                case _:
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "to_date({snowpark_arg_names[0]}" due to data type mismatch: Parameter 1 requires the ("STRING" or "DATE" or "TIMESTAMP" or "TIMESTAMP_NTZ") type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception

            result_type = DateType()
        case "to_json":
            if len(snowpark_args) > 1:
                if not isinstance(snowpark_typed_args[1].typ, MapType):
                    exception = AnalysisException(
                        "[INVALID_OPTIONS.NON_MAP_FUNCTION] Invalid options: Must use the `map()` function for options."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
                if not isinstance(
                    snowpark_typed_args[1].typ.key_type, StringType
                ) or not isinstance(snowpark_typed_args[1].typ.value_type, StringType):
                    exception = AnalysisException(
                        f"""[INVALID_OPTIONS.NON_STRING_TYPE] Invalid options: A type of keys and values in `map()` must be string, but got "{snowpark_typed_args[1].typ.simpleString().upper()}"."""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
            result_exp = snowpark_fn.to_json(snowpark_fn.to_variant(snowpark_args[0]))
            result_type = StringType()
        case "to_number":
            precision, scale = resolve_to_number_precision_and_scale(exp)
            to_number = snowpark_fn.function("to_number")
            result_exp = resolve_to_number_expression(
                to_number, snowpark_args[0], snowpark_args[1], precision, scale
            )
            result_type = DecimalType(precision, scale)
        case "to_timestamp":
            input_is_literal = (
                len(exp.unresolved_function.arguments) > 0
                and exp.unresolved_function.arguments[0].WhichOneof("expr_type")
                == "literal"
            )
            if not spark_sql_ansi_enabled:
                function_name = "try_to_timestamp"
            match (snowpark_typed_args, exp.unresolved_function.arguments):
                case ([e], _):
                    result_exp = snowpark_fn.when(
                        snowpark_fn.function(function_name)(
                            snowpark_fn.cast(e.col, StringType())
                        ).isNull(),
                        snowpark_fn.lit(None),
                    ).otherwise(snowpark_fn.to_timestamp(e.col))
                case ([e, _], _) if type(e.typ) in (DateType, TimestampType):
                    result_exp = snowpark_fn.when(
                        snowpark_fn.function(function_name)(
                            snowpark_fn.cast(e.col, StringType())
                        ).isNull(),
                        snowpark_fn.lit(None),
                    ).otherwise(snowpark_fn.to_timestamp(e.col))
                case ([e, _], [_, fmt]):
                    if input_is_literal:
                        _timestamp_format_sanity_check(
                            snowpark_arg_names[0], snowpark_arg_names[1]
                        )
                    result_exp = snowpark_fn.when(
                        snowpark_fn.function(function_name)(
                            snowpark_fn.cast(e.col, StringType()),
                            snowpark_fn.lit(
                                map_spark_timestamp_format_expression(fmt, e.typ)
                            ),
                        ).isNull(),
                        snowpark_fn.lit(None),
                    ).otherwise(
                        snowpark_fn.to_timestamp(
                            e.col,
                            snowpark_fn.lit(
                                map_spark_timestamp_format_expression(fmt, e.typ)
                            ),
                        )
                    )
                case _:
                    exception = ValueError(
                        f"Invalid number of arguments to {function_name}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            result_exp = snowpark_fn.cast(result_exp, get_timestamp_type())
            result_type = get_timestamp_type()

        case "to_timestamp_ltz":
            match (snowpark_typed_args, exp.unresolved_function.arguments):
                case ([e], _):
                    result_exp = snowpark_fn.builtin("to_timestamp_ltz")(e.col)
                case ([e, _], _) if type(e.typ) in (DateType, TimestampType):
                    result_exp = snowpark_fn.builtin("to_timestamp_ltz")(e.col)
                case ([e, _], [_, fmt]):
                    result_exp = snowpark_fn.builtin("to_timestamp_ltz")(
                        e.col,
                        snowpark_fn.lit(
                            map_spark_timestamp_format_expression(fmt, e.typ)
                        ),
                    )
                case _:
                    exception = ValueError(
                        f"Invalid number of arguments to {function_name}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            result_exp = snowpark_fn.cast(
                result_exp, TimestampType(snowpark.types.TimestampTimeZone.LTZ)
            )
            result_type = TimestampType(snowpark.types.TimestampTimeZone.LTZ)

        case "to_timestamp_ntz":
            match (snowpark_typed_args, exp.unresolved_function.arguments):
                case ([e], _):
                    result_exp = snowpark_fn.builtin("to_timestamp_ntz")(e.col)
                case ([e, _], _) if isinstance(e.typ, DateType):
                    result_exp = snowpark_fn.convert_timezone(
                        snowpark_fn.lit("UTC"),
                        snowpark_fn.builtin("to_timestamp_ntz")(e.col),
                    )
                case ([e, _], _) if isinstance(e.typ, TimestampType):
                    result_exp = snowpark_fn.builtin("to_timestamp_ntz")(e.col)
                case ([e, _], [_, fmt]):
                    result_exp = snowpark_fn.builtin("to_timestamp_ntz")(
                        e.col,
                        snowpark_fn.lit(
                            map_spark_timestamp_format_expression(fmt, e.typ)
                        ),
                    )
                case _:
                    exception = ValueError(
                        f"Invalid number of arguments to {function_name}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            result_exp = snowpark_fn.cast(
                result_exp, TimestampType(snowpark.types.TimestampTimeZone.NTZ)
            )
            result_type = TimestampType(snowpark.types.TimestampTimeZone.NTZ)

        case "to_unix_timestamp":
            # to_unix_timestamp in PySpark has an optional format string.
            # In Snowpark, the timestamp is not optional.
            # It is observed that the server receives the optional format string if the timestamp is specified,
            # In case of to_unix_timestamp function in SQL it's possible only one argument.
            # so there are either  1 or 2 arguments.
            match exp.unresolved_function.arguments:
                case [_, _] | [_] if isinstance(snowpark_typed_args[0].typ, NullType):
                    result_exp = snowpark_fn.lit(None).cast(LongType())
                case [_, _] | [_] if isinstance(
                    snowpark_typed_args[0].typ,
                    (
                        DateType,
                        TimestampType,
                    ),
                ):
                    result_exp = snowpark_fn.when(
                        snowpark_fn.is_null(snowpark_args[0]),
                        snowpark_fn.lit(None).cast(LongType()),
                    ).otherwise(snowpark_fn.unix_timestamp(snowpark_args[0]))
                case [_, unresolved_format]:
                    snowpark_timestamp = snowpark_args[0]
                    result_exp = _to_unix_timestamp(
                        snowpark_timestamp,
                        snowpark_fn.lit(
                            map_spark_timestamp_format_expression(
                                unresolved_format, snowpark_typed_args[0].typ
                            )
                        ),
                    )
                case [_]:
                    result_exp = _to_unix_timestamp(
                        snowpark_args[0],
                        snowpark_fn.lit("YYYY-MM-DD HH24:MI:SS"),
                    )
                case _:
                    exception = SnowparkConnectNotImplementedError(
                        "to_unix_timestamp expected 1 or 2 arguments."
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception

            if len(exp.unresolved_function.arguments) == 1:
                spark_function_name = f"to_unix_timestamp({snowpark_arg_names[0]}, {'yyyy-MM-dd HH:mm:ss'})"
            result_type = LongType()

        case "to_utc_timestamp":
            result_type = TimestampType()
            result_exp = _try_to_cast(
                "try_to_timestamp",
                snowpark_fn.cast(
                    snowpark_fn.to_utc_timestamp(
                        snowpark_args[0], _map_from_spark_tz(snowpark_args[1])
                    ),
                    result_type,
                ),
                snowpark_args[0],
            )
        case "transform":
            analyzer = Session.get_active_session()._analyzer
            body_str = analyzer.analyze(snowpark_args[1]._expression, defaultdict())
            lambda_exp = snowpark_fn.sql_expr(f"el -> {body_str}")
            result_exp = snowpark_fn.function("transform")(snowpark_args[0], lambda_exp)
            result_exp = TypedColumn(
                result_exp, lambda: [ArrayType(snowpark_typed_args[1].typ)]
            )

            spark_function_name = f"{exp.unresolved_function.function_name}({snowpark_arg_names[0]}, lambdafunction({snowpark_arg_names[1]}, namedlambdavariable()))"

        case "translate":
            src_alphabet = unwrap_literal(exp.unresolved_function.arguments[1])
            target_alphabet = unwrap_literal(exp.unresolved_function.arguments[2])

            # In Spark the target alphabet is truncated if it's too long, but in Snowpark an exception is thrown.
            if len(target_alphabet) > len(src_alphabet):
                target_alphabet = target_alphabet[: len(src_alphabet)]

            # In Spark, if a character appears multiple times in src_alphabet,
            # only the first mapping is used. Deduplicate while preserving order.
            deduped_src = []
            deduped_target = []
            for i, char in enumerate(src_alphabet):
                if char not in deduped_src:
                    deduped_src.append(char)
                    if i < len(target_alphabet):
                        deduped_target.append(target_alphabet[i])
            src_alphabet = "".join(deduped_src)
            target_alphabet = "".join(deduped_target)

            result_exp = snowpark_fn.translate(
                snowpark_args[0],
                snowpark_fn.lit(src_alphabet),
                snowpark_fn.lit(target_alphabet),
            )
            result_type = StringType()
        case "trunc":
            part = unwrap_literal(exp.unresolved_function.arguments[1])
            part = None if part is None else part.lower()

            allowed_parts = {
                "year",
                "yyyy",
                "yy",
                "month",
                "mon",
                "mm",
                "week",
                "quarter",
            }

            if part not in allowed_parts:
                result_exp = snowpark_fn.lit(None)
            else:
                result_exp = _try_to_cast(
                    "try_to_date",
                    snowpark_fn.cast(
                        snowpark_fn.date_trunc(
                            part, snowpark_fn.to_timestamp(snowpark_args[0])
                        ),
                        DateType(),
                    ),
                    snowpark_args[0],
                )
            result_type = DateType()
        case "try_add":
            # Handle interval arithmetic with overflow detection
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (DateType(), t) | (t, DateType()) if isinstance(
                    t, YearMonthIntervalType
                ):
                    result_type = DateType()
                    result_exp = snowpark_args[0] + snowpark_args[1]
                case (DateType(), t) | (t, DateType()) if isinstance(
                    t, DayTimeIntervalType
                ):
                    result_type = TimestampType()
                    result_exp = snowpark_args[0] + snowpark_args[1]
                case (TimestampType(), t) | (t, TimestampType()) if isinstance(
                    t, (DayTimeIntervalType, YearMonthIntervalType)
                ):
                    result_type = (
                        snowpark_typed_args[0].typ
                        if isinstance(snowpark_typed_args[0].typ, TimestampType)
                        else snowpark_typed_args[1].typ
                    )
                    result_exp = snowpark_args[0] + snowpark_args[1]
                case (t1, t2) if (
                    isinstance(t1, YearMonthIntervalType)
                    and isinstance(t2, (_NumericType, StringType))
                ) or (
                    isinstance(t2, YearMonthIntervalType)
                    and isinstance(t1, (_NumericType, StringType))
                ):
                    # YearMonthInterval + numeric/string or numeric/string + YearMonthInterval should throw error
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "try_add({snowpark_arg_names[0]}, {snowpark_arg_names[1]})" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                case (t1, t2) if isinstance(t1, YearMonthIntervalType) and isinstance(
                    t2, YearMonthIntervalType
                ):
                    result_type = YearMonthIntervalType(
                        min(t1.start_field, t2.start_field),
                        max(t1.end_field, t2.end_field),
                    )

                    # For year-month intervals, throw ArithmeticException if operands reach 10+ digits OR result exceeds 9 digits
                    total1 = _calculate_total_months(snowpark_args[0])
                    total2 = _calculate_total_months(snowpark_args[1])
                    ten_digit_limit = snowpark_fn.lit(MAX_10_DIGIT_LIMIT)

                    precision_violation = (
                        # Check if either operand already reaches 10 digits (parsing limit)
                        (snowpark_fn.abs(total1) >= ten_digit_limit)
                        | (snowpark_fn.abs(total2) >= ten_digit_limit)
                        | (
                            (total1 > 0)
                            & (total2 > 0)
                            & (total1 >= ten_digit_limit - total2)
                        )
                        | (
                            (total1 < 0)
                            & (total2 < 0)
                            & (total1 <= -ten_digit_limit - total2)
                        )
                    )

                    raise_error = _raise_error_helper(result_type, ArithmeticException)
                    result_exp = snowpark_fn.when(
                        precision_violation,
                        raise_error(
                            snowpark_fn.lit(
                                "Year-Month Interval result exceeds Snowflake interval precision limit"
                            )
                        ),
                    ).otherwise(snowpark_args[0] + snowpark_args[1])
                case (t1, t2) if isinstance(t1, DayTimeIntervalType) and isinstance(
                    t2, DayTimeIntervalType
                ):
                    result_type = DayTimeIntervalType(
                        min(t1.start_field, t2.start_field),
                        max(t1.end_field, t2.end_field),
                    )
                    # Check for Snowflake's day limit (106751991 days is the cutoff)
                    days1 = snowpark_fn.date_part("day", snowpark_args[0])
                    days2 = snowpark_fn.date_part("day", snowpark_args[1])
                    max_days = snowpark_fn.lit(
                        MAX_DAY_TIME_DAYS
                    )  # Snowflake's actual limit
                    min_days = snowpark_fn.lit(-MAX_DAY_TIME_DAYS)

                    # Check if either operand exceeds the day limit - throw error like Spark does
                    operand_limit_violation = (snowpark_fn.abs(days1) > max_days) | (
                        snowpark_fn.abs(days2) > max_days
                    )

                    # Check if result would exceed day limit (but operands are valid) - return NULL
                    result_overflow = (
                        # Check if result would exceed day limit (positive overflow)
                        ((days1 > 0) & (days2 > 0) & (days1 > max_days - days2))
                        | ((days1 < 0) & (days2 < 0) & (days1 < min_days - days2))
                    )

                    raise_error = _raise_error_helper(result_type, ArithmeticException)
                    result_exp = (
                        snowpark_fn.when(
                            operand_limit_violation,
                            raise_error(
                                snowpark_fn.lit(
                                    "Day-Time Interval operand exceeds Snowflake interval precision limit"
                                )
                            ),
                        )
                        .when(result_overflow, snowpark_fn.lit(None))
                        .otherwise(snowpark_args[0] + snowpark_args[1])
                    )
                case _:
                    result_exp, result_type = _try_arithmetic_helper(
                        OperandInfo(
                            snowpark_typed_args[0],
                            args_types[0],
                            snowpark_arg_names[0],
                        ),
                        OperandInfo(
                            snowpark_typed_args[1],
                            args_types[1],
                            snowpark_arg_names[1],
                        ),
                        0,
                    )
                    if result_type is not None:
                        result_exp = TypedColumn(
                            result_exp, lambda rt=result_type: [rt]
                        )
                    else:
                        result_exp = _type_with_typer(result_exp)
        case "try_aes_decrypt":
            result_exp = _aes_helper(
                "TRY_DECRYPT",
                snowpark_args[0],
                snowpark_args[1],
                snowpark_args[4],
                snowpark_args[2],
                snowpark_args[3],
            )
            result_type = BinaryType()
        case "try_avg":
            # Snowflake raises an error when a value that cannot be cast into a numeric is passed to AVG. Spark treats these as NULL values and
            # does not throw an error. Additionally, Spark returns NULL when this calculation results in an overflow, whereas Snowflake raises a "TypeError".
            # Matching Spark behavior on both is handled within try_sum_implementation.

            # If we add together all of the numbers and divide by the size of the column we will know if there will be an overflow.
            # However, even the intermediate sum cannot lead to overflow, not just the end result. Therefore, we can just check if the
            # sum of the column will cause an overflow by using the try_sum implementation. Additionally, The AVG calculation can never overflow
            # without the intermediate sum overflowing. Therefore, it is sufficient to rely on intemediate sum overflow and divide after without
            # additional checking.

            match (snowpark_typed_args[0].typ):
                case DecimalType():
                    result_exp, result_type = _try_sum_helper(
                        snowpark_typed_args[0].typ,
                        snowpark_args[0],
                        calculating_avg=True,
                    )
                case _IntegralType():
                    # Cannot call try_cast on Number type, however, Double can always hold Number type, therefore we can just call cast.
                    # Column must be cast to DoubleType prior to summation to match Spark's behavior. For any non-Decimal type, the overflow limit
                    # matches that of a Double.
                    cleaned = snowpark_fn.cast(snowpark_args[0], DoubleType())
                    result_exp, result_type = _try_sum_helper(
                        DoubleType(), cleaned, calculating_avg=True
                    )
                case _:
                    # For the column sum to be non null, there must be > 0 non null rows in the input column. Since we only want to count the
                    # rows included in the calculation, we try cast to DoubleType first, as unsuitable values will be nulled out. DecimalType
                    # remains as is and should not be cast to a Double to match Spark behavior.

                    # However, in ANSI mode, we want to throw an error rather than gracefully handling a cast of non-numeric data. Therefore, we call
                    # cast in this case instead of try_cast.
                    if spark_sql_ansi_enabled:
                        cleaned = snowpark_fn.cast(snowpark_args[0], DoubleType())
                    else:
                        cleaned = _try_cast_helper(snowpark_args[0], DoubleType())
                    result_exp, result_type = _try_sum_helper(
                        DoubleType(), cleaned, calculating_avg=True
                    )
        case "try_divide":
            # Handle interval division with overflow detection
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (t1, t2) if isinstance(t1, _AnsiIntervalType) and isinstance(
                    t2, (_NumericType, StringType)
                ):
                    # Interval / numeric/string
                    result_type = t1
                    interval_arg = snowpark_args[0]
                    divisor = (
                        snowpark_args[1]
                        if isinstance(t2, _NumericType)
                        else snowpark_fn.cast(snowpark_args[1], "double")
                    )

                    # Check for division by zero first
                    zero_check = divisor == 0

                    if isinstance(result_type, YearMonthIntervalType):
                        # For year-month intervals, check if result exceeds 32-bit signed integer limit
                        result_type = YearMonthIntervalType()
                        total_months = _calculate_total_months(interval_arg)
                        max_months = snowpark_fn.lit(MAX_32BIT_SIGNED_INT)
                        overflow_check = (
                            snowpark_fn.abs(total_months / divisor) > max_months
                        )
                        result_exp = (
                            snowpark_fn.when(zero_check, snowpark_fn.lit(None))
                            .when(overflow_check, snowpark_fn.lit(None))
                            .otherwise(interval_arg / divisor)
                        )
                    else:  # DayTimeIntervalType
                        # For day-time intervals, check if result exceeds day limit
                        result_type = DayTimeIntervalType()
                        total_days = _calculate_total_days(interval_arg)
                        max_days = snowpark_fn.lit(MAX_DAY_TIME_DAYS)
                        overflow_check = (
                            snowpark_fn.abs(total_days / divisor) > max_days
                        )
                        result_exp = (
                            snowpark_fn.when(zero_check, snowpark_fn.lit(None))
                            .when(overflow_check, snowpark_fn.lit(None))
                            .otherwise(interval_arg / divisor)
                        )
                case (NullType(), t) | (t, NullType()):
                    result_exp = snowpark_fn.lit(None)
                    result_type = FloatType()
                case (_IntegralType(), _IntegralType()):
                    # TRY_CAST can never be called between a NUMBER(38, 0) and a DoubleType due to precision loss. Therefore,
                    # we must use CAST instead, which is why this case cannot be combined with the String/Variant case. However,
                    # an IntegerType can always safely cast to a DoubleType, so there is no danger in using CAST.
                    left_double, right_double = snowpark_fn.cast(
                        snowpark_args[0], DoubleType()
                    ), snowpark_fn.cast(snowpark_args[1], DoubleType())
                    result_exp = snowpark_fn.when(
                        snowpark_args[1] == 0, snowpark_fn.lit(None)
                    ).otherwise(left_double / right_double)
                    result_type = DoubleType()
                case (
                    (DecimalType(), _IntegralType())
                    | (
                        _IntegralType(),
                        DecimalType(),
                    )
                    | (DecimalType(), DecimalType())
                ):
                    p1, s1 = _get_type_precision(
                        OperandInfo(
                            snowpark_typed_args[0],
                            args_types[0],
                            snowpark_arg_names[0],
                        )
                    )
                    p2, s2 = _get_type_precision(
                        OperandInfo(
                            snowpark_typed_args[1],
                            args_types[1],
                            snowpark_arg_names[1],
                        )
                    )
                    result_type, overflow_possible = _get_decimal_division_result_type(
                        p1, s1, p2, s2
                    )

                    result_exp = _arithmetic_operation(
                        snowpark_typed_args[0],
                        snowpark_typed_args[1],
                        lambda x, y: _divnull(x, y),
                        overflow_possible,
                        False,
                        result_type,
                        "divide",
                    )
                case (_NumericType(), _NumericType()):
                    result_exp = snowpark_fn.when(
                        snowpark_args[1] == 0, snowpark_fn.lit(None)
                    ).otherwise(snowpark_args[0] / snowpark_args[1])
                    result_exp = _type_with_typer(result_exp)
                case (
                    (StringType(), _)
                    | (_, StringType())
                    | (VariantType(), _)
                    | (
                        _,
                        VariantType(),
                    )
                ):
                    cleaned_left, cleaned_right = _try_cast_helper(
                        snowpark_args[0], DoubleType()
                    ), _try_cast_helper(snowpark_args[1], DoubleType())

                    result_exp = snowpark_fn.when(
                        cleaned_right == 0, snowpark_fn.lit(None)
                    ).otherwise(cleaned_left / cleaned_right)
                    result_exp = _type_with_typer(result_exp)
                case (_, _):
                    exception = AnalysisException(
                        f"Incompatible types: {snowpark_typed_args[0].typ}, {snowpark_typed_args[1].typ}"
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception

        case "try_element_at":
            # For structured ArrayType and MapType columns, Snowflake raises an error when an index is out of bounds or a key does not exist.
            # We avoid this error explicitly here by checking the size of the array or the existence of the key regardless of the column type.
            # This is consistent with Spark behaviors over ArrayType and MapType (structured or not in Snowflake).
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (ArrayType(), _IntegralType()):
                    array_size = snowpark_fn.array_size(snowpark_args[0])
                    spark_index = snowpark_args[1]

                    # Spark uses 1-based indexing, Snowflake uses 0-based indexing. Spark also allows negative indexing.
                    # Spark Connect raises an error when index == 0.
                    result_exp = (
                        snowpark_fn.when(
                            spark_index == 0,
                            snowpark_fn.lit(
                                "[snowpark_connect::INVALID_INDEX_OF_ZERO] The index 0 is invalid. An index shall be either < 0 or > 0 (the first element has index 1)."
                            ),
                        )
                        .when(
                            (-array_size <= spark_index) & (spark_index < 0),
                            snowpark_fn.get(snowpark_args[0], array_size + spark_index),
                        )
                        .when(
                            (0 < spark_index) & (spark_index <= array_size),
                            snowpark_fn.get(snowpark_args[0], spark_index - 1),
                        )
                        .otherwise(snowpark_fn.lit(None))
                    )
                    result_type = snowpark_typed_args[0].typ.element_type
                case (MapType(), StringType()):
                    result_exp = snowpark_fn.when(
                        snowpark_fn.map_contains_key(
                            snowpark_args[1], snowpark_args[0]
                        ),
                        snowpark_fn.get(snowpark_args[0], snowpark_args[1]),
                    ).otherwise(snowpark_fn.lit(None))
                    result_type = snowpark_typed_args[0].typ.value_type
                case _:
                    # Currently we do not handle VariantType columns as the first argument here.
                    # Spark will not support VariantType until 4.0.0, revisit this when the support is added.
                    exception = AnalysisException(
                        f"Expected either (ArrayType, IntegralType) or (MapType, StringType), got {snowpark_typed_args[0].typ}, {snowpark_typed_args[1].typ}."
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
        case "try_multiply":
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (t1, t2) if isinstance(t1, _AnsiIntervalType) and isinstance(
                    t2, (_NumericType, StringType)
                ):
                    # Interval * numeric/string
                    result_type = t1
                    interval_arg = snowpark_args[0]
                    multiplier = (
                        snowpark_args[1]
                        if isinstance(t2, _NumericType)
                        else snowpark_fn.cast(snowpark_args[1], "double")
                    )

                    if isinstance(result_type, YearMonthIntervalType):
                        # For year-month intervals, check if result exceeds 32-bit signed integer limit
                        result_type = YearMonthIntervalType()
                        total_months = _calculate_total_months(interval_arg)
                        max_months = snowpark_fn.lit(MAX_32BIT_SIGNED_INT)
                        overflow_check = (
                            snowpark_fn.abs(total_months * multiplier) > max_months
                        )
                        result_exp = snowpark_fn.when(
                            overflow_check, snowpark_fn.lit(None)
                        ).otherwise(interval_arg * multiplier)
                    else:  # DayTimeIntervalType
                        # For day-time intervals, check if result exceeds day limit
                        result_type = DayTimeIntervalType()
                        total_days = _calculate_total_days(interval_arg)
                        max_days = snowpark_fn.lit(MAX_DAY_TIME_DAYS)
                        overflow_check = (
                            snowpark_fn.abs(total_days * multiplier) > max_days
                        )
                        result_exp = snowpark_fn.when(
                            overflow_check, snowpark_fn.lit(None)
                        ).otherwise(interval_arg * multiplier)

                case (t1, t2) if isinstance(t2, _AnsiIntervalType) and isinstance(
                    t1, (_NumericType, StringType)
                ):
                    # numeric/string * Interval
                    result_type = t2
                    interval_arg = snowpark_args[1]
                    multiplier = (
                        snowpark_args[0]
                        if isinstance(t1, _NumericType)
                        else snowpark_fn.cast(snowpark_args[0], "double")
                    )

                    if isinstance(result_type, YearMonthIntervalType):
                        # For year-month intervals, check if result exceeds 32-bit signed integer limit
                        result_type = YearMonthIntervalType()
                        total_months = _calculate_total_months(interval_arg)
                        max_months = snowpark_fn.lit(MAX_32BIT_SIGNED_INT)
                        overflow_check = (
                            snowpark_fn.abs(total_months * multiplier) > max_months
                        )
                        result_exp = snowpark_fn.when(
                            overflow_check, snowpark_fn.lit(None)
                        ).otherwise(interval_arg * multiplier)
                    else:  # DayTimeIntervalType
                        # For day-time intervals, check if result exceeds day limit
                        result_type = DayTimeIntervalType()
                        total_days = _calculate_total_days(interval_arg)
                        max_days = snowpark_fn.lit(MAX_DAY_TIME_DAYS)
                        overflow_check = (
                            snowpark_fn.abs(total_days * multiplier) > max_days
                        )
                        result_exp = snowpark_fn.when(
                            overflow_check, snowpark_fn.lit(None)
                        ).otherwise(interval_arg * multiplier)
                case (NullType(), t) | (t, NullType()):
                    result_exp = snowpark_fn.lit(None)
                    match t:
                        case NullType() | StringType():
                            result_type = FloatType()
                        case _:
                            result_type = t
                case (_IntegralType() as t1, _IntegralType() as t2):
                    result_type = _find_common_type([t1, t2])
                    min_val, max_val = get_integral_type_bounds(result_type)

                    same_sign = ((snowpark_args[0] > 0) & (snowpark_args[1] > 0)) | (
                        (snowpark_args[0] < 0) & (snowpark_args[1] < 0)
                    )
                    bound = snowpark_fn.when(same_sign, max_val).otherwise(-min_val - 1)

                    result_exp = (
                        snowpark_fn.when(
                            (snowpark_args[0] == 0) | (snowpark_args[1] == 0),
                            snowpark_fn.lit(0).cast(result_type),
                        )
                        .when(
                            snowpark_fn.abs(snowpark_args[0])
                            > (bound / snowpark_fn.abs(snowpark_args[1])),
                            snowpark_fn.lit(None),
                        )
                        .otherwise(
                            (snowpark_args[0] * snowpark_args[1]).cast(result_type)
                        )
                    )
                case (
                    (DecimalType(), _IntegralType())
                    | (
                        _IntegralType(),
                        DecimalType(),
                    )
                    | (DecimalType(), DecimalType())
                ):
                    p1, s1 = _get_type_precision(
                        OperandInfo(
                            snowpark_typed_args[0],
                            args_types[0],
                            snowpark_arg_names[0],
                        )
                    )
                    p2, s2 = _get_type_precision(
                        OperandInfo(
                            snowpark_typed_args[1],
                            args_types[1],
                            snowpark_arg_names[1],
                        )
                    )
                    (
                        result_type,
                        overflow_possible,
                    ) = _get_decimal_multiplication_result_type(p1, s1, p2, s2)

                    result_exp = _arithmetic_operation(
                        snowpark_typed_args[0],
                        snowpark_typed_args[1],
                        lambda x, y: x * y,
                        overflow_possible,
                        False,
                        result_type,
                        "multiply",
                    )
                case (_NumericType(), _NumericType()):
                    result_exp = snowpark_args[0] * snowpark_args[1]
                    result_exp = _type_with_typer(result_exp)
                case (
                    (StringType(), _)
                    | (_, StringType())
                    | (VariantType(), _)
                    | (
                        _,
                        VariantType(),
                    )
                ):
                    cleaned_left, cleaned_right = _try_cast_helper(
                        snowpark_args[0], DoubleType()
                    ), _try_cast_helper(snowpark_args[1], DoubleType())
                    result_exp = cleaned_left * cleaned_right
                    result_exp = _type_with_typer(result_exp)
                case (_, _):
                    exception = AnalysisException(
                        f"Incompatible types: {snowpark_typed_args[0].typ}, {snowpark_typed_args[1].typ}"
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
        case "try_sum":
            # Snowflake raises an error when a value that cannot be cast into a numeric is passed to SUM. Spark treats these as NULL values and
            # does not throw an error. Additionally, Spark returns NULL when this calculation results in an overflow, whereas Snowflake raises a "TypeError".
            # We avoid these errors explicitly for StringType and VariantType columns by checking the column type and preemptively calling try_cast to a
            # numeric type. Non numerics will be returned as NULL, which is consistent with Spark's behavior as well. For Integral and Decimal types, overflow
            # will be handled manually via UDAF. For Float and Double (which are synonymous), overflow goes to 'inf'/-'inf' which matches Spark's behavior.
            if (
                spark_sql_ansi_enabled
                and not isinstance(snowpark_typed_args[0].typ, DecimalType)
                and not isinstance(snowpark_typed_args[0].typ, _IntegralType)
            ):
                # We want to throw an error on invalid inputs in ANSI mode. Therefore, we should cast to Double prior to passing into _try_sum_helper to
                # trigger error, rather than NULL on non-numeric values in the input column. DecimalType will never have non-numeric types, and also should
                # remain DecimalType. Therefore, we can safely go the alternative path in the DecimalType case.
                casted = snowpark_fn.cast(snowpark_args[0], DoubleType())
                result_exp, result_type = _try_sum_helper(DoubleType(), casted)
            else:
                result_exp, result_type = _try_sum_helper(
                    snowpark_typed_args[0].typ, snowpark_args[0]
                )
        case "try_subtract":
            # Handle interval arithmetic with overflow detection
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (DateType(), t) if isinstance(t, YearMonthIntervalType):
                    result_type = DateType()
                    result_exp = snowpark_args[0] - snowpark_args[1]
                case (DateType(), t) if isinstance(t, DayTimeIntervalType):
                    result_type = TimestampType()
                    result_exp = snowpark_args[0] - snowpark_args[1]
                case (TimestampType(), t) if isinstance(
                    t, (DayTimeIntervalType, YearMonthIntervalType)
                ):
                    result_type = snowpark_typed_args[0].typ
                    result_exp = snowpark_args[0] - snowpark_args[1]
                case (t1, t2) if (
                    isinstance(t1, YearMonthIntervalType)
                    and isinstance(t2, (_NumericType, StringType))
                ) or (
                    isinstance(t2, YearMonthIntervalType)
                    and isinstance(t1, (_NumericType, StringType))
                ):
                    # YearMonthInterval - numeric/string or numeric/string - YearMonthInterval should throw error
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "try_subtract({snowpark_arg_names[0]}, {snowpark_arg_names[1]})" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                case (t1, t2) if isinstance(t1, YearMonthIntervalType) and isinstance(
                    t2, YearMonthIntervalType
                ):
                    result_type = YearMonthIntervalType(
                        min(t1.start_field, t2.start_field),
                        max(t1.end_field, t2.end_field),
                    )
                    # Check for Snowflake's precision limits: 10+ digits for operands, 9+ digits for results
                    total1 = _calculate_total_months(snowpark_args[0])
                    total2 = _calculate_total_months(snowpark_args[1])
                    ten_digit_limit = snowpark_fn.lit(MAX_10_DIGIT_LIMIT)

                    precision_violation = (
                        # Check if either operand already reaches 10 digits (parsing limit)
                        (snowpark_fn.abs(total1) >= ten_digit_limit)
                        | (snowpark_fn.abs(total2) >= ten_digit_limit)
                        | (
                            (total1 > 0)
                            & (total2 < 0)
                            & (total1 >= ten_digit_limit + total2)
                        )
                        | (
                            (total1 < 0)
                            & (total2 > 0)
                            & (total1 <= -ten_digit_limit + total2)
                        )
                    )

                    raise_error = _raise_error_helper(result_type, ArithmeticException)
                    result_exp = snowpark_fn.when(
                        precision_violation,
                        raise_error(
                            snowpark_fn.lit(
                                "Year-Month Interval result exceeds Snowflake interval precision limit"
                            )
                        ),
                    ).otherwise(snowpark_args[0] - snowpark_args[1])
                case (t1, t2) if isinstance(t1, DayTimeIntervalType) and isinstance(
                    t2, DayTimeIntervalType
                ):
                    result_type = DayTimeIntervalType(
                        min(t1.start_field, t2.start_field),
                        max(t1.end_field, t2.end_field),
                    )
                    # Check for Snowflake's day limit (106751991 days is the cutoff)
                    days1 = snowpark_fn.date_part("day", snowpark_args[0])
                    days2 = snowpark_fn.date_part("day", snowpark_args[1])
                    max_days = snowpark_fn.lit(
                        MAX_DAY_TIME_DAYS
                    )  # Snowflake's actual limit
                    min_days = snowpark_fn.lit(-MAX_DAY_TIME_DAYS)

                    # Check if either operand exceeds the day limit - throw error like Spark does
                    operand_limit_violation = (snowpark_fn.abs(days1) > max_days) | (
                        snowpark_fn.abs(days2) > max_days
                    )

                    # Check if result would exceed day limit (but operands are valid) - return NULL
                    result_overflow = (
                        (days1 > 0) & (days2 < 0) & (days1 > max_days + days2)
                    ) | ((days1 < 0) & (days2 > 0) & (days1 < min_days + days2))

                    raise_error = _raise_error_helper(result_type, ArithmeticException)
                    result_exp = (
                        snowpark_fn.when(
                            operand_limit_violation,
                            raise_error(
                                snowpark_fn.lit(
                                    "Day-Time Interval operand exceeds day limit"
                                )
                            ),
                        )
                        .when(result_overflow, snowpark_fn.lit(None))
                        .otherwise(snowpark_args[0] - snowpark_args[1])
                    )
                case _:
                    result_exp, result_type = _try_arithmetic_helper(
                        OperandInfo(
                            snowpark_typed_args[0],
                            args_types[0],
                            snowpark_arg_names[0],
                        ),
                        OperandInfo(
                            snowpark_typed_args[1],
                            args_types[1],
                            snowpark_arg_names[1],
                        ),
                        1,
                    )
                    if result_type is not None:
                        result_exp = TypedColumn(
                            result_exp, lambda rt=result_type: [rt]
                        )
                    else:
                        result_exp = _type_with_typer(result_exp)
        case "try_to_number":
            try_to_number = snowpark_fn.function("try_to_number")
            precision, scale = resolve_to_number_precision_and_scale(exp)
            result_exp = resolve_to_number_expression(
                try_to_number, snowpark_args[0], snowpark_args[1], precision, scale
            )
            result_type = DecimalType(precision, scale)

        case "try_to_timestamp":
            match (snowpark_typed_args, exp.unresolved_function.arguments):
                case ([e], _):
                    result_exp = snowpark_fn.builtin("try_to_timestamp")(e.col)
                case ([e, _], _) if type(e.typ) in (DateType, TimestampType):
                    result_exp = snowpark_fn.builtin("try_to_timestamp")(e.col)
                case ([e, _], [_, fmt]):
                    result_exp = snowpark_fn.builtin("try_to_timestamp")(
                        e.col,
                        snowpark_fn.lit(
                            map_spark_timestamp_format_expression(fmt, e.typ)
                        ),
                    )
                case _:
                    exception = ValueError(
                        f"Invalid number of arguments to {function_name}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            result_type = get_timestamp_type()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "typeof":
            col_snowpark_typ = snowpark_typed_args[0].typ
            spark_typ = map_snowpark_to_pyspark_types(col_snowpark_typ)
            result_exp = snowpark_fn.lit(spark_typ.simpleString())
            result_type = StringType()
        case "unbase64":

            # Workaround for SNOW-3194655
            if global_config.snowpark_connect_use_udf_for_unbase64:

                @cached_udf(
                    input_types=[StringType()],
                    return_type=BinaryType(),
                )
                def _unbase64_udf(s: str) -> bytes:
                    import base64
                    import re

                    if s is None:
                        return None
                    cleaned = re.sub(r"[^A-Za-z0-9+/=]", "", s)
                    padded = cleaned + "=" * (-len(cleaned) % 4)
                    return base64.b64decode(padded)

                unbase_arg = snowpark_args[0]
                if snowpark_typed_args[0].typ == BinaryType():
                    unbase_arg = snowpark_fn.to_varchar(unbase_arg, "UTF-8")

                result_exp = _unbase64_udf(unbase_arg)
            else:
                base64_decoding_function = snowpark_fn.function(
                    "TRY_BASE64_DECODE_BINARY"
                )

                unbase_arg = snowpark_args[0]
                if snowpark_typed_args[0].typ == BinaryType():
                    unbase_arg = snowpark_fn.to_varchar(unbase_arg, "UTF-8")

                # Remove all characters that are not base64 characters, as Spark does.
                cleaned = snowpark_fn.regexp_replace(unbase_arg, "[^A-Za-z0-9+/=]", "")

                padded = snowpark_fn.rpad(
                    cleaned,
                    snowpark_fn.ceil(snowpark_fn.length(cleaned) / snowpark_fn.lit(4))
                    * snowpark_fn.lit(4),
                    snowpark_fn.lit("="),
                )
                decoded = base64_decoding_function(padded)

                raise_fn = _raise_error_helper(BinaryType(), IllegalArgumentException)
                result_exp = snowpark_fn.when(
                    unbase_arg.is_not_null() & decoded.is_null(),
                    raise_fn(snowpark_fn.lit("Invalid input")),
                ).otherwise(decoded)

            result_type = BinaryType()
        case "unhex":
            # Non string columns, convert them to string type. This mimics pyspark behavior.
            string_input = snowpark_fn.cast(snowpark_args[0], StringType())

            # Pad odd-length hex strings with leading zero. This mimics pyspark behavior.
            padded_input = snowpark_fn.when(
                snowpark_fn.length(string_input) % 2 == 1,
                snowpark_fn.concat(snowpark_fn.lit("0"), string_input),
            ).otherwise(string_input)

            result_exp = snowpark_fn.function("TRY_HEX_DECODE_BINARY")(padded_input)
            result_type = BinaryType()
        case "unix_date":
            result_exp = snowpark_fn.datediff(
                "day", snowpark_fn.lit("1970-01-01"), snowpark_args[0]
            )
            result_type = IntegerType()
        case "unix_micros":
            result_exp = snowpark_fn.date_part(
                "epoch_microseconds",
                snowpark_fn.cast(snowpark_args[0], get_timestamp_type()),
            )
            result_type = LongType()
        case "unix_millis":
            result_exp = snowpark_fn.date_part(
                "epoch_milliseconds",
                snowpark_fn.cast(snowpark_args[0], get_timestamp_type()),
            )
            result_type = LongType()
        case "unix_seconds":
            result_exp = snowpark_fn.date_part(
                "epoch_seconds",
                snowpark_fn.cast(snowpark_args[0], get_timestamp_type()),
            )
            result_type = LongType()
        case "unix_timestamp":
            # unix_timestamp in PySpark has an optional timestamp and optional format string.
            # In Snowpark, the timestamp is not optional.
            # It is observed that the server receives the optional format string if the timestamp is specified,
            # In case of unix_timestamp function in SQL it's possible only one argument.
            # so there are either 0, 1 or 2 arguments.
            match exp.unresolved_function.arguments:
                case []:
                    spark_function_name = (
                        "unix_timestamp(current_timestamp(), yyyy-MM-dd HH:mm:ss)"
                    )
                    result_exp = snowpark_fn.unix_timestamp(_handle_current_timestamp())
                case [_, _] if isinstance(snowpark_typed_args[0].typ, NullType):
                    result_exp = snowpark_fn.lit(None).cast(LongType())
                case [_, _] | [_] if isinstance(
                    snowpark_typed_args[0].typ, (DateType, TimestampType)
                ):
                    result_exp = snowpark_fn.when(
                        snowpark_fn.is_null(snowpark_args[0]),
                        snowpark_fn.lit(None).cast(LongType()),
                    ).otherwise(snowpark_fn.unix_timestamp(snowpark_args[0]))
                case [_, unresolved_format]:
                    snowpark_timestamp = snowpark_args[0]
                    result_exp = _to_unix_timestamp(
                        snowpark_timestamp,
                        snowpark_fn.lit(
                            map_spark_timestamp_format_expression(
                                unresolved_format, snowpark_typed_args[0].typ
                            )
                        ),
                    )
                case [_]:
                    spark_function_name = f"unix_timestamp({snowpark_arg_names[0]}, {'yyyy-MM-dd HH:mm:ss'})"
                    if isinstance(snowpark_typed_args[0].typ, NullType):
                        result_exp = snowpark_fn.lit(None).cast(LongType())
                    else:
                        result_exp = _to_unix_timestamp(
                            snowpark_args[0],
                            snowpark_fn.lit("YYYY-MM-DD HH24:MI:SS"),
                        )
                case _:
                    exception = SnowparkConnectNotImplementedError(
                        "unix_timestamp expected 0, 1 or 2 arguments."
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            result_type = LongType()
        case "unwrap_udt":
            snowpark_col_name = snowpark_args[0].get_name()
            spark_col_name = (
                column_mapping.get_spark_column_name_from_snowpark_column_name(
                    snowpark_col_name
                )
            )

            metadata = (
                column_mapping.column_metadata.get(spark_col_name, {})
                if column_mapping.column_metadata
                else {}
            )

            if "__udt_info__" not in metadata:
                exception = AnalysisException(
                    f"[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve '{spark_function_name})' due to data type mismatch: Parameter 1 requires the 'USERDEFINEDTYPE' type"
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

            result_type = map_json_schema_to_snowpark(
                metadata["__udt_info__"]["sqlType"]
            )

            result_exp = snowpark_fn.cast(snowpark_args[0], result_type)
        case "upper" | "ucase":
            result_exp = snowpark_fn.upper(snowpark_args[0])
            result_type = StringType()
        case "url_decode":

            @cached_udf(
                input_types=[StringType()],
                return_type=StringType(),
            )
            def _url_decode(encoded_url: Optional[str]) -> Optional[str]:
                if encoded_url is None:
                    return None
                try:
                    # Handle both + and %20 encoding for spaces
                    return unquote(encoded_url.replace("+", " "))
                except Exception:
                    return None

            result_exp = _url_decode(snowpark_args[0])
            result_type = StringType()
        case "url_encode":

            @cached_udf(
                input_types=[StringType()],
                return_type=StringType(),
            )
            def _url_encode(url: Optional[str]) -> Optional[str]:
                if url is None:
                    return None
                try:
                    # some tweaks to make it compatible with Spark (and with java.net.URLEncoder)
                    encoded = quote(url, safe="*~")
                    return encoded.replace("~", "%7E").replace("%20", "+")
                except Exception:
                    return None

            result_exp = _url_encode(snowpark_args[0])
            result_type = StringType()
        case "uuid":
            result_exp = snowpark_fn.builtin("UUID_STRING")()
            result_type = StringType()
        case "var_pop":
            var_pop_argument = snowpark_args[0]
            if not isinstance(snowpark_typed_args[0].typ, _NumericType):
                if isinstance(snowpark_typed_args[0].typ, StringType):
                    var_pop_argument = snowpark_fn.try_cast(
                        snowpark_args[0], DoubleType()
                    )
                else:
                    exception = AnalysisException(
                        f"""AnalysisException: [DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{function_name}({snowpark_arg_names[0]})" due to data type mismatch: Parameter 1 requires the "DOUBLE" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".;"""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
            result_type = DoubleType()
            result_exp = _resolve_aggregate_exp(
                snowpark_fn.var_pop(var_pop_argument), result_type
            )
        case "var_samp" | "variance":
            var_samp_argument = snowpark_args[0]
            if not isinstance(snowpark_typed_args[0].typ, _NumericType):
                if isinstance(snowpark_typed_args[0].typ, StringType):
                    var_samp_argument = snowpark_fn.try_cast(
                        snowpark_args[0], DoubleType()
                    )
                else:
                    exception = AnalysisException(
                        f"""AnalysisException: [DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{function_name}({snowpark_arg_names[0]})" due to data type mismatch: Parameter 1 requires the "DOUBLE" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".;"""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
            result_type = DoubleType()
            result_exp = _resolve_aggregate_exp(
                snowpark_fn.var_samp(var_samp_argument), result_type
            )
        case "version":
            result_exp = snowpark_fn.lit(get_spark_version())
            result_type = StringType()
        case "weekday":
            arg = snowpark_args[0]
            if isinstance(snowpark_typed_args[0].typ, StringType):
                arg = snowpark_fn.builtin("try_to_date")(snowpark_args[0])

            # dayofweekiso returns 1-7 for Sunday-Saturday, so we subtract 1 to get 0-6 for Monday-Sunday.
            result_exp = snowpark_fn.builtin("dayofweekiso")(
                snowpark_fn.to_date(arg)
            ) - snowpark_fn.lit(1)
            # Spark 3.5.3: WeekDay extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "weekofyear":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.weekofyear(
                    snowpark_fn.builtin("try_to_date")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.weekofyear(
                    snowpark_fn.to_date(snowpark_args[0])
                )
            # Spark 3.5.3: WeekOfYear extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case "when" | "if":
            # Validate that the condition is a boolean expression
            if len(snowpark_typed_args) > 0:
                condition_type = snowpark_typed_args[0].typ
                if not isinstance(condition_type, BooleanType):
                    exception = AnalysisException(
                        f"[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve CASE WHEN condition due to data type mismatch: "
                        f"Parameter 1 requires the 'BOOLEAN' type, however got '{condition_type}'"
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception

            name_components = ["CASE"]
            name_components.append("WHEN")
            name_components.append(snowpark_arg_names[0])
            name_components.append("THEN")
            name_components.append(snowpark_arg_names[1])
            result_exp = snowpark_fn.when(snowpark_args[0], snowpark_args[1])
            result_type_indexes = [1]
            for i in range(2, len(snowpark_args), 2):
                if i + 1 >= len(snowpark_args):
                    name_components.append("ELSE")
                    name_components.append(snowpark_arg_names[i])
                    result_exp = result_exp.otherwise(snowpark_args[i])
                    result_type_indexes.append(i)
                else:
                    name_components.append("WHEN")
                    name_components.append(snowpark_arg_names[i])
                    name_components.append("THEN")
                    name_components.append(snowpark_arg_names[i + 1])
                    # Validate each WHEN condition
                    condition_type = snowpark_typed_args[i].typ
                    if not isinstance(condition_type, BooleanType):
                        exception = AnalysisException(
                            f"[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve CASE WHEN condition due to data type mismatch: "
                            f"Parameter {i + 1} requires the 'BOOLEAN' type, however got '{condition_type}'"
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
                    result_exp = result_exp.when(snowpark_args[i], snowpark_args[i + 1])
                    result_type_indexes.append(i + 1)
            name_components.append("END")
            result_type = _find_common_type(
                [snowpark_typed_args[i].typ for i in result_type_indexes]
            )
            result_exp = snowpark_fn.cast(result_exp, result_type)
            spark_function_name = " ".join(name_components)
        case "width_bucket":
            width_bucket_fn = snowpark_fn.function("width_bucket")
            v, min_, max_, num_buckets = snowpark_args

            result_exp = (
                snowpark_fn.when(num_buckets <= 0, snowpark_fn.lit(None))
                .when(min_ == max_, snowpark_fn.lit(None))
                .otherwise(width_bucket_fn(v, min_, max_, num_buckets))
            )

            # Snowflake returns Decimal(x, 0), but Spark expects LongType() always
            result_type = LongType()
            result_exp.cast(result_type)
        case "window":
            (window_duration, start_time) = _extract_window_args(exp)
            spark_function_name = "window"
            result_exp = snowpark_fn.window(
                snowpark_args[0], window_duration, start_time=start_time
            )
            window_schema = StructType(
                [
                    StructField(
                        '"start"',
                        TimestampType(TimestampTimeZone.LTZ),
                        True,
                        _is_column=False,
                    ),
                    StructField(
                        '"end"',
                        TimestampType(TimestampTimeZone.LTZ),
                        True,
                        _is_column=False,
                    ),
                ],
                structured=STRUCTURED_TYPES_ENABLED,
            )
            result_exp = snowpark_fn.cast(result_exp, window_schema)
            # TODO SNOW-2034495: figure out how to specify the type of a window
            result_exp = _type_with_typer(result_exp)
        case "xpath":
            result_type = ArrayType(StringType())
            result_exp = _create_xpath_expression("xpath_list", "ARRAY(STRING)")
        case "xpath_boolean":
            result_type = BooleanType()
            result_exp = _create_xpath_expression("xpath_boolean", "BOOLEAN")
        case "xpath_double" | "xpath_number":
            result_type = DoubleType()
            result_exp = _create_xpath_expression("xpath_number", "DOUBLE")
        case "xpath_float":
            result_type = FloatType()
            result_exp = _create_xpath_expression("xpath_number", "DOUBLE")
        case "xpath_int":
            result_type = IntegerType()
            xpath_expression = _create_xpath_expression("xpath_number", "DOUBLE")
            result_exp = _cast_and_handle_nan_xpath_expression(
                xpath_expression, result_type
            )
        case "xpath_long":
            result_type = LongType()
            xpath_expression = _create_xpath_expression("xpath_number", "DOUBLE")
            result_exp = _cast_and_handle_nan_xpath_expression(
                xpath_expression, result_type
            )
        case "xpath_short":
            result_type = ShortType()
            xpath_expression = _create_xpath_expression("xpath_number", "DOUBLE")
            result_exp = _cast_and_handle_nan_xpath_expression(
                xpath_expression, result_type
            )
        case "xpath_string":
            result_type = StringType()
            result_exp = _create_xpath_expression("xpath_string", "STRING")
        case "xxhash64":
            import snowflake.snowpark_connect.utils.xxhash64 as xxhash64

            xxhash64_src_file = Path(__file__).parent.parent / "utils" / "xxhash64.py"

            # In the notebook environment, the physical file may not be where it's expected, if not found
            # then temporarily create in another location.
            if not xxhash64_src_file.exists():
                xxhash64_src_bytes = inspect.getsource(xxhash64).encode("utf-8")
                sub_dir = (
                    Path(tempfile.gettempdir())
                    / "snowflake"
                    / "snowpark_connect"
                    / "utils"
                )
                xxhash64_src_file = sub_dir / "xxhash64.py"
                # If the file doesn't exist (from a prior run) or it's a different size, then recreate.
                # Otherwise we can use the previously created xxhash64 source file.
                if (
                    not xxhash64_src_file.exists()
                    or xxhash64_src_file.stat().st_size != len(xxhash64_src_bytes)
                ):
                    sub_dir.mkdir(parents=True, exist_ok=True)
                    xxhash64_src_file.write_bytes(xxhash64_src_bytes)

            xxhash_udf_imports = [
                (
                    str(xxhash64_src_file),
                    "snowflake.snowpark_connect.utils.xxhash64",
                )
            ]

            xxhash_udf = partial(
                cached_udf, return_type=LongType(), imports=xxhash_udf_imports
            )

            result_exp = snowpark_fn.lit(DEFAULT_SEED)

            for arg in snowpark_typed_args:
                match arg.typ:
                    case IntegerType() | ShortType() | ByteType() | BooleanType():
                        xxhash64_udf_int = xxhash_udf(
                            xxhash64_int, input_types=[LongType(), LongType()]
                        )

                        result_exp = xxhash64_udf_int(
                            snowpark_fn.cast(arg.col, LongType()), result_exp
                        )
                    case FloatType():
                        xxhash64_udf_float = xxhash_udf(
                            xxhash64_float, input_types=[FloatType(), LongType()]
                        )

                        result_exp = xxhash64_udf_float(arg.col, result_exp)
                    case DoubleType():
                        xxhash64_udf_double = xxhash_udf(
                            xxhash64_double, input_types=[DoubleType(), LongType()]
                        )

                        result_exp = xxhash64_udf_double(arg.col, result_exp)
                    case LongType():
                        xxhash64_udf_long = xxhash_udf(
                            xxhash64_long, input_types=[LongType(), LongType()]
                        )

                        result_exp = xxhash64_udf_long(arg.col, result_exp)
                    case _:
                        xxhash64_udf_str = xxhash_udf(
                            xxhash64_string, input_types=[StringType(), LongType()]
                        )

                        result_exp = xxhash64_udf_str(
                            snowpark_fn.cast(arg.col, StringType()), result_exp
                        )
                result_type = LongType()
        case "year":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.year(
                    snowpark_fn.builtin("try_to_date")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.year(snowpark_fn.to_date(snowpark_args[0]))
            # Spark 3.5.3: Year extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_type = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, result_type)
        case binary_method if binary_method in ("to_binary", "try_to_binary"):
            binary_format = snowpark_fn.lit("hex")
            arg_str = snowpark_fn.cast(snowpark_args[0], StringType())
            if len(snowpark_args) > 1:
                binary_format = snowpark_args[1]
            result_exp = snowpark_fn.when(
                snowpark_args[0].isNull(), snowpark_fn.lit(None)
            ).otherwise(
                snowpark_fn.function(binary_method)(
                    snowpark_fn.when(
                        (snowpark_fn.length(arg_str) % 2 == 1)
                        & (snowpark_fn.lower(binary_format) == snowpark_fn.lit("hex")),
                        snowpark_fn.concat(snowpark_fn.lit("0"), arg_str),
                    ).otherwise(arg_str),
                    binary_format,
                )
            )
            result_type = BinaryType()
        case udtf_name if udtf_name.lower() in session._udtfs:
            udtf, spark_col_names = session._udtfs[udtf_name.lower()]
            result_exp = snowpark_fn.call_table_function(
                udtf.name,
                *(snowpark_fn.cast(arg, VariantType()) for arg in snowpark_args),
            )
            result_type = [f.datatype for f in udtf.output_schema]

        case cast_funcs if cast_funcs in CAST_FUNCTIONS:
            cast_exp = expressions_proto.Expression(
                cast=expressions_proto.Expression.Cast(
                    expr=exp.unresolved_function.arguments[0],
                    type=CAST_FUNCTIONS[cast_funcs],
                )
            )

            return map_cast(cast_exp, column_mapping, typer, from_type_cast=True)

        case "luhn_check":

            # https://en.wikipedia.org/wiki/Luhn_algorithm
            @cached_udf(input_types=[StringType()], return_type=BooleanType())
            def _luhn_check(input_number: str) -> bool:
                if input_number is None:
                    return None
                else:
                    input_number = input_number.replace(" ", "")
                    if not input_number.isdigit():
                        return False

                    digits = list(map(int, input_number))

                    for i in range(len(digits) - 2, -1, -2):
                        digits[i] *= 2
                        if digits[i] > 9:
                            digits[i] -= 9

                    total_sum = sum(digits)
                    return total_sum % 10 == 0

            result_exp = _luhn_check(snowpark_args[0])
            result_type = BooleanType()

        case other:
            # TODO: Add more here as we come across them.
            # Unfortunately the scope of function names are not documented in
            # the proto file.
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported function name {other}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

    def _to_typed_column(
        res: Column | TypedColumn,
        res_type: DataType | List[DataType] | None,
        function_name: str,
    ) -> TypedColumn:
        if isinstance(res, TypedColumn):
            tc = res
        elif res_type is None:
            # This error indicates the function result lacks type information.
            # Possible ways to properly type a function result (in order of performance):
            # 1. Static type: Assign directly to `result_type` when type is known at resolve time
            # 2. Dynamic type based on function arguments types: Use `snowpark_typed_args` to determine type
            # 3. Use _type_with_typer() as last resort - it calls GS to determine the type
            exception = SnowparkConnectNotImplementedError(
                f"Result type of function {function_name} not implemented"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        elif type(res_type) is list:
            tc = TypedColumn(res, lambda: res_type)
        else:
            tc = TypedColumn(res, lambda: [res_type])

        return tc

    spark_col_names = (
        spark_col_names if len(spark_col_names) > 0 else [spark_function_name]
    )
    typed_col = _to_typed_column(result_exp, result_type, function_name)
    typed_col.set_qualifiers({ColumnQualifier(tuple(qualifier_parts))})
    return spark_col_names, typed_col


def _try_cast_helper(column: Column, to: DataType) -> Column:
    """
    DEPRECATED because of performance issues

    Attempts to cast a given column to a specified data type using the same behaviour as Spark.

    Args:
        column (Column): The column to be cast.
        to (DataType): The target data type to cast the column to.

    Returns:
        Column: A column that is cast to the specified data type. If the cast fails, it returns NULL instead of raising an error.

    Behavior:
        - The column is first cast to a string type.
        - If the cast is unsuccessful, the result will be NULL.
    """
    string_column = snowpark_fn.cast(column, StringType())
    return snowpark_fn.try_cast(string_column, to)


def _decode_column(
    col_type: DataType, col: Column, format: Column | str = "utf-8"
) -> Column:
    """
    Decodes a column based on its data type and the specified format converting it to StringType() data type.

    Args:
        col_type (DataType): The data type of the column to decode.
        col (Column): The column to decode.
        format (Column | str, optional): The format to use for decoding. Defaults to "utf-8".
            If a string is provided, it will be converted to a Snowpark literal.

    Returns:
        Column: The decoded column as StringType() data type.

    Behavior:
        - If the column type is `StringType`, the column is returned as-is.
        - If the column type is `BinaryType`, a cached UDF is used to decode the binary data.
          Special handling is applied for UTF-16 encoding.
        - For other column types, the column is cast to `StringType`.
    """
    if isinstance(format, str):
        format = snowpark_fn.lit(format)
    match col_type:
        case StringType():
            decoded_col = col
        case BinaryType():

            @cached_udf(
                input_types=[BinaryType(), StringType()],
                return_type=StringType(),
            )
            def _decode(s, f):
                if None in (s, f):
                    return None
                if f.lower() == "utf-16":
                    return s[2:].decode("utf-16be")
                return s.decode(f)

            decoded_col = _decode(col, format)
        case _:
            decoded_col = snowpark_fn.cast(col, StringType())
    return decoded_col


def _extract_window_args(fn: expressions_proto.Expression) -> (str, str):
    args = fn.unresolved_function.arguments
    match args:
        case [_, _, _]:
            exception = SnowparkConnectNotImplementedError(
                "the slide_duration parameter is not supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        case [_, window_duration, slide_duration, _] if unwrap_literal(
            window_duration
        ) != unwrap_literal(slide_duration):
            exception = SnowparkConnectNotImplementedError(
                "the slide_duration parameter is not supported"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
        case [_, window_duration, _, start_time]:
            return unwrap_literal(window_duration), unwrap_literal(start_time)
        case [_, window_duration]:
            return unwrap_literal(window_duration), None


def _handle_current_timestamp():
    result_exp = snowpark_fn.cast(
        snowpark_fn.current_timestamp(),
        get_timestamp_type(),
    )
    return result_exp


def _equivalent_decimal(typ: DataType) -> DecimalType:
    (precision, scale) = _get_type_precision_from_datatype(typ)
    return DecimalType(precision, scale)


def _resolve_decimal_and_numeric(type1: DecimalType, type2: _NumericType) -> DataType:
    if isinstance(type2, DecimalType):
        digits_before_point = max(
            type1.precision - type1.scale, type2.precision - type2.scale
        )
        scale = max(type1.scale, type2.scale)
        precision = digits_before_point + scale
        return _bounded_decimal(precision, scale)

    if isinstance(type2, _FractionalType):
        return type2
    return _resolve_decimal_and_numeric(type1, _equivalent_decimal(type2))


def _find_common_type(
    types: list[DataType],
    func_name: str = None,
    widen_to_string: bool = False,
    narrow_string: bool = False,
) -> DataType | None:
    numeric_priority = {
        DoubleType: 6,
        FloatType: 5,
        LongType: 4,
        IntegerType: 3,
        ShortType: 2,
        ByteType: 1,
    }
    time_priority = {
        TimestampType: 2,
        DateType: 1,
    }
    castable_to_string = [_NumericType, DateType, TimestampType, StringType]
    coercible_to_string = [*castable_to_string, NullType, BooleanType, BinaryType]
    exception_base_message = "pyspark.errors.exceptions.captured.AnalysisException: [DATATYPE_MISMATCH.DATA_DIFF_TYPES]"

    def _common(type1, type2):
        match (type1, type2):
            case (None, t) | (t, None):
                return t
            case (NullType(), t) | (t, NullType()):
                return t
            case (StringType(), t) | (
                t,
                StringType(),
            ) if narrow_string:
                return t
            case (StringType(), t) | (t, StringType()) if (
                not widen_to_string
                and any(isinstance(t, castable) for castable in castable_to_string)
            ) or (
                widen_to_string
                and any(isinstance(t, coercible) for coercible in coercible_to_string)
            ):
                return StringType()
            case (ArrayType(), ArrayType()):
                typ = _common(type1.element_type, type2.element_type)
                return ArrayType(typ)
            case (ArrayType(), _) | (_, ArrayType()) if func_name == "concat":
                exception = AnalysisException(exception_base_message)
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            case (BinaryType(), BinaryType()):
                return BinaryType()
            case (BooleanType(), BooleanType()):
                return BooleanType()
            case (_, _) if isinstance(type1, DecimalType) and isinstance(
                type2, _NumericType
            ):
                return _resolve_decimal_and_numeric(type1, type2)
            case (_, _) if isinstance(type1, _NumericType) and isinstance(
                type2, DecimalType
            ):
                return _resolve_decimal_and_numeric(type2, type1)
            case (_, _) if isinstance(type1, _NumericType) and isinstance(
                type2, _NumericType
            ):
                return max([type1, type2], key=lambda tp: numeric_priority[type(tp)])
            case (_, _) if isinstance(
                type1, tuple(time_priority.keys())
            ) and isinstance(type2, tuple(time_priority.keys())):
                return max([type1, type2], key=lambda tp: time_priority[type(tp)])
            case (StructType(), StructType()):
                fields1 = type1.fields
                fields2 = type2.fields
                if [field.name for field in fields1] != [
                    field.name for field in fields2
                ]:
                    exception = AnalysisException(exception_base_message)
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                fields = []
                for idx, field in enumerate(fields1):
                    typ = _common(field.datatype, fields2[idx].datatype)
                    fields.append(StructField(field.name, typ, _is_column=False))
                return StructType(fields)
            case (MapType(), MapType()):
                key_type = _common(type1.key_type, type2.key_type)
                value_type = _common(type1.value_type, type2.value_type)
                return MapType(key_type, value_type)
            case (_, _) if isinstance(type1, YearMonthIntervalType) and isinstance(
                type2, YearMonthIntervalType
            ):
                return YearMonthIntervalType(
                    min(type1.start_field, type2.start_field),
                    max(type1.end_field, type2.end_field),
                )
            case (_, _) if isinstance(type1, DayTimeIntervalType) and isinstance(
                type2, DayTimeIntervalType
            ):
                return DayTimeIntervalType(
                    min(type1.start_field, type2.start_field),
                    max(type1.end_field, type2.end_field),
                )
            case _:
                exception = AnalysisException(exception_base_message)
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

    types = list(filter(lambda tp: tp is not None, types))
    if not types:
        return None

    try:
        return reduce(_common, types)
    except AnalysisException as e:
        if exception_base_message in e.message:
            func_name_message = f" to `{func_name}`" if func_name else ""
            types_message = " or ".join([f'"{type}"' for type in types])
            exception_message = f"{exception_base_message} Cannot resolve expression due to data type mismatch: Input{func_name_message} should all be the same type, but it's ({types_message})."
            exception = AnalysisException(exception_message)
            attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
            raise exception
        else:
            raise


def _get_mod_return_type(
    dividend_operand: OperandInfo, divisor_operand: OperandInfo
) -> DataType | None:
    """
    Determines the return type of the `mod` or `pmod` function based on the types of the dividend and divisor.

    Args:
        dividend_operand (OperandInfo): The information about the dividen.
        divisor_operand (OperandInfo): The information about the divisor.

    Returns:
        DataType | None: The resulting data type of the `pmod` operation, or None if the types are invalid.
    """

    def _calculate_decimal_type(d1: DecimalType, d2: DecimalType) -> DataType:
        """
        Calculates the resulting decimal type when a DecimalType is involved in the `mod` or `pmod` operation.

        Args:
            d1 (DecimalType): The DecimalType involved in the operation.
            d2 (DecimalType): The DecimalType involved in the operation.

        Returns:
            DataType: The resulting decimal data type with correct precision and scalel, which could be a DecimalType, FloatType, or DoubleType.
        """
        p1, s1 = d1.precision, d1.scale
        p2, s2 = d2.precision, d2.scale
        digits = min(p1 - s1, p2 - s2)
        scale = max(s1, s2)
        return _bounded_decimal(digits + scale, scale)

    match (dividend_operand.typ, divisor_operand.typ):
        # string
        case (StringType(), StringType()):
            result_type = DoubleType()
        case (StringType(), t) | (t, StringType()):
            result_type = DoubleType() if isinstance(t, _NumericType) else None
        # null
        case (NullType(), NullType()):
            result_type = DoubleType()
        case (NullType(), t) | (t, NullType()):
            result_type = t if isinstance(t, _NumericType) else DoubleType()
        # invalid types
        case (t1, t2) if not isinstance(t1, _NumericType) or not isinstance(
            t2, _NumericType
        ):
            result_type = None
        # floating number
        case (DoubleType(), _) | (_, DoubleType()):
            result_type = DoubleType()
        case (FloatType(), DecimalType()) | (DecimalType(), FloatType()):
            result_type = DoubleType()
        case (FloatType(), _) | (_, FloatType()):
            result_type = FloatType()
        # decimal number
        case (DecimalType() as d1, DecimalType() as d2):
            result_type = _calculate_decimal_type(d1, d2)
        case (_IntegralType(), DecimalType() as dt):
            p, s = _get_type_precision(dividend_operand)
            result_type = _calculate_decimal_type(dt, DecimalType(p, s))
        case (DecimalType() as dt, _IntegralType()):
            p, s = _get_type_precision(divisor_operand)
            result_type = _calculate_decimal_type(DecimalType(p, s), dt)
        # integer number
        case (integral_type1, integral_type2) if isinstance(
            integral_type1, _IntegralType
        ) and isinstance(integral_type2, _IntegralType):
            result_type = _find_common_type([integral_type1, integral_type2])
        # default case
        case _:
            result_type = None
    return result_type


def _get_ceil_floor_return_type(
    data_type: DataType, target_scale: int | None = None
) -> DecimalType | LongType:
    if target_scale is None:
        match data_type:
            case DecimalType() as t:
                if t.scale == 0:
                    return data_type
                p = t.precision - t.scale + 1
                return DecimalType(p, 0)
            case _:
                return LongType()

    precision, scale = _get_type_precision_from_datatype(data_type)
    if isinstance(data_type, FloatType):
        precision, scale = 14, 7
    elif isinstance(data_type, DoubleType):
        precision, scale = 30, 15
    elif isinstance(data_type, StringType):
        precision, scale = 38, 18

    if target_scale >= 0:
        final_scale = min(scale, target_scale)
        return _bounded_decimal(precision - scale + 1 + final_scale, final_scale)
    return _bounded_decimal(max(precision - scale + 1, -target_scale + 1), 0)


def _resolve_function_with_lambda(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], TypedColumn]:
    from snowflake.snowpark import Session
    from snowflake.snowpark_connect.expression.map_expression import map_expression

    def _resolve_lambda(
        lambda_exp, arg_types: list[DateType], resolve_only_body: bool = False
    ) -> tuple[list[str], TypedColumn]:
        names = [a.name_parts[0] for a in lambda_exp.lambda_function.arguments]
        schema = StructType(
            [
                StructField(name, typ, _is_column=False)
                for name, typ in zip(names, arg_types)
            ]
        )
        artificial_df = Session.get_active_session().create_dataframe([], schema)
        set_schema_getter(artificial_df, lambda: schema)

        with resolving_lambda_function(names):
            return map_expression(
                (
                    lambda_exp.lambda_function.function
                    if resolve_only_body
                    else lambda_exp
                ),
                column_mapping,
                ExpressionTyper(artificial_df),
            )

    def _get_arr_el_type(tc: TypedColumn):
        match tc.typ:
            case ArrayType() if tc.typ.structured:
                return tc.typ.element_type
            case ArrayType():
                return VariantType()
            case t:
                exception = ValueError(f"Expected array, got {t}")
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

    def _get_map_types(tc: TypedColumn):
        match tc.typ:
            case MapType() if tc.typ.structured:
                return tc.typ.key_type, tc.typ.value_type
            case MapType():
                return VariantType(), VariantType()
            case VariantType():
                return StringType(), VariantType()
            case t:
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Parameter 1 requires the "MAP" type, however "id" has the type "{t}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception

    def _map_to_array(m: dict) -> Optional[list]:
        # confirm that m is a dict and not a sqlNullWrapper
        if m is None or not hasattr(m, "items"):
            return None
        # Convert sqlNullWrapper values to None to avoid serialization errors
        return [
            {"key": k, "value": (None if getattr(v, "is_sql_null", False) else v)}
            for k, v in m.items()
        ]

    def _randomize_lambda_args_names(message: Message, suffix: str | None = None):
        if suffix is None:
            suffix = uuid.uuid4().hex
        for field, value in message.ListFields():
            if (
                field.name == "name_parts"
                and message.DESCRIPTOR.name == "UnresolvedNamedLambdaVariable"
            ):
                modified = [f"{v}_{suffix}" for v in value]
                getattr(message, field.name)[:] = modified
            elif isinstance(value, Message):
                _randomize_lambda_args_names(value, suffix)
            elif field.label == field.LABEL_REPEATED:
                for item in value:
                    if isinstance(item, Message):
                        _randomize_lambda_args_names(item, suffix)

    first_arg = exp.unresolved_function.arguments[0]
    ([arg1_name], arg1_tc) = map_expression(first_arg, column_mapping, typer)
    function_name = exp.unresolved_function.function_name
    result_type = None
    match function_name:
        case "aggregate" | "reduce":
            arr_el_typ = _get_arr_el_type(arg1_tc)
            init_exp = exp.unresolved_function.arguments[1]
            merge_lambda_fn_exp = exp.unresolved_function.arguments[2]
            ([arg2_name], arg2_tc) = map_expression(init_exp, column_mapping, typer)
            ([arg3_name], arg3_tc) = _resolve_lambda(
                merge_lambda_fn_exp, [arg2_tc.typ, arr_el_typ]
            )

            # Handle struct field name mismatch between initial accumulator and merge lambda result
            if isinstance(arg2_tc.typ, StructType) and isinstance(
                arg3_tc.typ, StructType
            ):
                if len(arg2_tc.typ.fields) == len(arg3_tc.typ.fields):
                    merge_field_names = [f.name for f in arg3_tc.typ.fields]
                    init_field_names = [f.name for f in arg2_tc.typ.fields]
                    has_default_names = all(
                        name == f"col{i+1}" for i, name in enumerate(merge_field_names)
                    )

                    if has_default_names and merge_field_names != init_field_names:
                        lambda_arg_names = [
                            a.name_parts[0]
                            for a in merge_lambda_fn_exp.lambda_function.arguments
                        ]
                        analyzer = Session.get_active_session()._analyzer
                        (_, body_tc) = _resolve_lambda(
                            merge_lambda_fn_exp,
                            [arg2_tc.typ, arr_el_typ],
                            resolve_only_body=True,
                        )
                        body_sql = analyzer.analyze(
                            body_tc.col._expression, defaultdict()
                        )

                        # Reconstruct object with correct field names
                        rename_parts = [
                            f"'{new_name}', ({body_sql}):{old_name}"
                            for old_name, new_name in zip(
                                merge_field_names, init_field_names
                            )
                        ]
                        rename_sql = (
                            f"OBJECT_CONSTRUCT_KEEP_NULL({', '.join(rename_parts)})"
                        )

                        cast_parts = [
                            f"{new_name} {map_type_to_snowflake_type(field.datatype)}"
                            for new_name, field in zip(
                                init_field_names, arg3_tc.typ.fields
                            )
                        ]
                        rename_sql = f"({rename_sql})::OBJECT({', '.join(cast_parts)})"
                        new_lambda_sql = (
                            f"({', '.join(lambda_arg_names)}) -> {rename_sql}"
                        )
                        new_fields = [
                            StructField(
                                init_field_names[i],
                                field.datatype,
                                field.nullable,
                                _is_column=False,
                            )
                            for i, field in enumerate(arg3_tc.typ.fields)
                        ]
                        arg3_tc = TypedColumn(
                            snowpark_fn.sql_expr(new_lambda_sql),
                            lambda: [StructType(new_fields)],
                        )

            result_exp = snowpark_fn.function("reduce")(
                arg1_tc.col, arg2_tc.col, arg3_tc.col
            )
            result_exp = TypedColumn(result_exp, lambda: arg3_tc.types)
            match exp.unresolved_function.arguments:
                case [_, _, _]:
                    # looks like there is 4th argument in the name (identity function) in native Spark
                    arg4_name = (
                        "lambdafunction(namedlambdavariable(), namedlambdavariable())"
                    )
                case [_, _, _, finish_lambda_fn_exp]:
                    type_of_merge_lamda_body = arg3_tc.typ
                    ([arg4_name], arg4_tc) = _resolve_lambda(
                        finish_lambda_fn_exp, [type_of_merge_lamda_body]
                    )
                    result_exp = snowpark_fn.array_construct(
                        result_exp.column(to_semi_structure=True)
                    )
                    result_exp = snowpark_fn.cast(
                        result_exp,
                        ArrayType(element_type=type_of_merge_lamda_body),
                    )
                    result_exp = snowpark_fn.function("transform")(
                        result_exp, arg4_tc.col
                    )
                    result_type = arg4_tc.typ  # it's type of 'finish' lambda body
                    result_exp = snowpark_fn.get(result_exp, snowpark_fn.lit(0))
                case _:
                    exception = SnowparkConnectNotImplementedError(
                        f"{function_name} function requires 3 or 4 arguments"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception

            snowpark_arg_names = [
                arg1_name,
                arg2_name,
                arg3_name,
                arg4_name,
            ]
        case "exists":
            lambda_exp = exp.unresolved_function.arguments[1]
            arr_el_typ = _get_arr_el_type(arg1_tc)
            ([arg2_name], arg2_tc) = _resolve_lambda(lambda_exp, [arr_el_typ])
            result_exp = snowpark_fn.function("filter")(arg1_tc.col, arg2_tc.col)
            result_exp = snowpark_fn.array_size(result_exp) > 0
            result_type = BooleanType()
            snowpark_arg_names = [arg1_name, arg2_name]
        case "filter":
            lambda_exp = exp.unresolved_function.arguments[1]
            arr_el_typ = _get_arr_el_type(arg1_tc)
            ([arg2_name], arg2_tc) = _resolve_lambda(lambda_exp, [arr_el_typ])

            snowpark_arg_names = [arg1_name, arg2_name]
            result_exp = snowpark_fn.function("filter")(arg1_tc.col, arg2_tc.col)
            result_exp = TypedColumn(result_exp, lambda: [ArrayType(arr_el_typ)])
        case "forall":
            lambda_exp = exp.unresolved_function.arguments[1]
            arr_el_typ = _get_arr_el_type(arg1_tc)
            ([arg2_name], arg2_tc) = _resolve_lambda(lambda_exp, [arr_el_typ])
            result_exp = snowpark_fn.function("transform")(arg1_tc.col, arg2_tc.col)
            result_exp = snowpark_fn.function("reduce")(
                result_exp,
                snowpark_fn.lit(True),
                snowpark_fn.sql_expr("(acc, i) -> acc and i"),
            )
            result_type = BooleanType()
            snowpark_arg_names = [arg1_name, arg2_name]
        case "map_filter":
            """
            Implementation of Spark's map_filter with a similar workaround as `zip_with`.
            The input map is converted to an array of structs with fields 'key' and 'value'.
            This array is then filtered and reduced using Snowflake's `filter` and `reduce` functions.
            The input lambda is converted to a single argument Snowflake lambda.
            """

            _map_to_array_udf = cached_udf(
                _map_to_array, input_types=[VariantType()], return_type=ArrayType()
            )
            key_type, val_type = _get_map_types(arg1_tc)

            lambda_exp = exp.unresolved_function.arguments[1]
            # Due to lack of direct equivalent API in Snowflake, we need to transform the lambda expression.
            # Rather than traversing the entire lambda AST, we use string manipulation on the query.
            # We randomize lambda argument names to minimize the risk of accidental replacements in the query.
            _randomize_lambda_args_names(lambda_exp)
            ([lambda_body_name], fn_body) = _resolve_lambda(
                lambda_exp,
                [key_type, val_type],
                resolve_only_body=True,
            )

            l_arg1 = lambda_exp.lambda_function.arguments[0].name_parts[0]
            l_arg2 = lambda_exp.lambda_function.arguments[1].name_parts[0]

            analyzer = Session.get_active_session()._analyzer
            fn_sql = analyzer.analyze(fn_body.col._expression, defaultdict())
            # if the key is a number, we need to cast it
            # otherwise it seems to be treated as a string
            key_exp = (
                "get(x, 'key')::int"
                if isinstance(key_type, _IntegralType)
                else "get(x, 'key')"
            )
            transform_sql = fn_sql.replace(l_arg1, key_exp).replace(
                l_arg2, "strip_null_value(get(x, 'value'))"
            )
            transform_exp = snowpark_fn.sql_expr(f"x -> ({transform_sql})::boolean")
            last_win_dedup = global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            reduce_exp = snowpark_fn.function("reduce")(
                snowpark_fn.function("filter")(
                    _map_to_array_udf(snowpark_fn.cast(arg1_tc.col, VariantType())),
                    transform_exp,
                ),
                snowpark_fn.object_construct(),
                snowpark_fn.sql_expr(
                    # value is cast to variant because object_insert doesn't allow structured types,
                    # and structured types are not coercible to variant
                    # TODO: allow structured types in object_insert?
                    f"(acc, e) -> object_insert(acc, e:key, e:value::variant, {last_win_dedup})"
                ),
            )
            result_type = arg1_tc.typ
            result_exp = snowpark_fn.cast(reduce_exp, result_type)
            snowpark_arg_names = [
                arg1_name,
                f"lambdafunction({lambda_body_name}, namedlambdavariable(), namedlambdavariable())",
            ]
        case "map_zip_with":

            @cached_udf(
                input_types=[VariantType(), VariantType()],
                return_type=ArrayType(),
            )
            def _maps_to_array(m1, m2):
                if (
                    m1 is None
                    or not hasattr(m1, "items")
                    or m2 is None
                    or not hasattr(m2, "items")
                ):
                    return None

                def _convert_null(v):
                    """Convert sqlNullWrapper to None to avoid serialization errors."""
                    return None if getattr(v, "is_sql_null", False) else v

                keys = set(m1.keys()) | set(m2.keys())  # Union of keys from both maps
                return [
                    {
                        "k": k,
                        "v1": _convert_null(m1.get(k)),
                        "v2": _convert_null(m2.get(k)),
                    }
                    for k in keys
                ]

            ([arg2_name], arg2_tc) = map_expression(
                exp.unresolved_function.arguments[1], column_mapping, typer
            )

            key1_type, val1_type = _get_map_types(arg1_tc)
            key2_type, val2_type = _get_map_types(arg2_tc)

            lambda_exp = exp.unresolved_function.arguments[2]
            # Due to lack of direct equivalent API in Snowflake, we need to transform the lambda expression.
            # Rather than traversing the entire lambda AST, we use string manipulation on the query.
            # We randomize lambda argument names to minimize the risk of accidental replacements in the query.
            _randomize_lambda_args_names(lambda_exp)
            ([lambda_body_name], fn_body) = _resolve_lambda(
                lambda_exp,
                [key1_type, val1_type, val2_type],
                resolve_only_body=True,
            )

            key_type = _find_common_type([key1_type, key2_type])
            l_arg1 = lambda_exp.lambda_function.arguments[0].name_parts[0]
            l_arg2 = lambda_exp.lambda_function.arguments[1].name_parts[0]
            l_arg3 = lambda_exp.lambda_function.arguments[2].name_parts[0]

            analyzer = Session.get_active_session()._analyzer
            fn_sql = analyzer.analyze(fn_body.col._expression, defaultdict())
            # if the key is a number, we need to cast it
            # otherwise it seems to be treated as a string
            key_exp = (
                "get(x, 'k')::int"
                if isinstance(key_type, _IntegralType)
                else "get(x, 'k')"
            )
            transform_sql = (
                fn_sql.replace(l_arg1, key_exp)
                .replace(l_arg2, "strip_null_value(get(x, 'v1'))")
                .replace(l_arg3, "strip_null_value(get(x, 'v2'))")
            )

            last_win_dedup = global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            array_of_maps_exp = _maps_to_array(
                snowpark_fn.cast(arg1_tc.col, VariantType()),
                snowpark_fn.cast(arg2_tc.col, VariantType()),
            )
            result_exp = snowpark_fn.function("reduce")(
                array_of_maps_exp,
                snowpark_fn.object_construct(),
                snowpark_fn.sql_expr(
                    f"(acc, x) -> object_insert(acc, {key_exp}, nvl(({transform_sql})::variant, parse_json('null')), {last_win_dedup})"
                ),
            )
            result_type = MapType(key_type, fn_body.typ)
            result_exp = snowpark_fn.cast(result_exp, result_type)
            snowpark_arg_names = [
                arg1_name,
                arg2_name,
                f"lambdafunction({lambda_body_name}, namedlambdavariable(), namedlambdavariable(), namedlambdavariable())",
            ]
        case "transform":
            lambda_exp = exp.unresolved_function.arguments[1]
            arr_el_typ = _get_arr_el_type(arg1_tc)
            match lambda_exp.lambda_function.arguments:
                case [_]:
                    ([arg2_name], arg2_tc) = _resolve_lambda(lambda_exp, [arr_el_typ])
                    snowpark_arg_names = [arg1_name, arg2_name]
                    result_exp = snowpark_fn.function("transform")(
                        arg1_tc.col, arg2_tc.col
                    )
                    result_exp = TypedColumn(
                        result_exp, lambda: [ArrayType(arg2_tc.typ)]
                    )
                case [_, _]:

                    @cached_udf(
                        input_types=[ArrayType()],
                        return_type=ArrayType(),
                    )
                    def _with_index(arr: list) -> list:
                        if arr is None:
                            return None
                        return [{"index": i, "element": el} for i, el in enumerate(arr)]

                    # Due to lack of direct equivalent API in Snowflake, we need to transform the lambda expression.
                    # Rather than traversing the entire lambda AST, we use string manipulation on the query.
                    # We randomize lambda argument names to minimize the risk of accidental replacements in the query.
                    _randomize_lambda_args_names(lambda_exp)
                    ([lambda_body_name], fn_body) = _resolve_lambda(
                        lambda_exp,
                        [arr_el_typ, LongType()],
                        resolve_only_body=True,
                    )

                    l_arg1 = lambda_exp.lambda_function.arguments[0].name_parts[0]
                    l_arg2 = lambda_exp.lambda_function.arguments[1].name_parts[0]

                    analyzer = Session.get_active_session()._analyzer
                    fn_sql = analyzer.analyze(fn_body.col._expression, defaultdict())
                    fn_sql_with_replaced_args = fn_sql.replace(
                        l_arg1, "strip_null_value(get(x, 'element'))"
                    ).replace(l_arg2, "get(x, 'index')::int")

                    result_exp = snowpark_fn.function("transform")(
                        _with_index(arg1_tc.column(to_semi_structure=True)),
                        snowpark_fn.sql_expr(f"x -> {fn_sql_with_replaced_args}"),
                    )
                    result_type = ArrayType(fn_body.typ)
                    result_exp = snowpark_fn.cast(result_exp, result_type)
                    snowpark_arg_names = [
                        arg1_name,
                        f"lambdafunction({lambda_body_name}, namedlambdavariable(), namedlambdavariable())",
                    ]
                case _:
                    exception = SnowparkConnectNotImplementedError(
                        f"{function_name} function requires lambda function with 1 or 2 arguments"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
        case "transform_keys":
            _map_to_array_udf = cached_udf(
                _map_to_array,
                input_types=[VariantType()],
                return_type=ArrayType(),
                packages=[],
            )
            key_type, val_type = _get_map_types(arg1_tc)

            lambda_exp = exp.unresolved_function.arguments[1]
            # Due to lack of direct equivalent API in Snowflake, we need to transform the lambda expression
            # Rather than traversing the entire lambda AST, we use string manipulation on the query
            # We randomize lambda argument names to minimize the risk of accidental replacements in the query
            _randomize_lambda_args_names(lambda_exp)
            ([lambda_body_name], fn_body) = _resolve_lambda(
                lambda_exp,
                [key_type, val_type],
                resolve_only_body=True,
            )

            l_arg1 = lambda_exp.lambda_function.arguments[0].name_parts[0]
            l_arg2 = lambda_exp.lambda_function.arguments[1].name_parts[0]

            analyzer = Session.get_active_session()._analyzer
            fn_sql = analyzer.analyze(fn_body.col._expression, defaultdict())
            # if the key is a number, we need to cast it
            # otherwise it seems to be treated as a string
            key_exp = (
                "get(x, 'key')::int"
                if isinstance(key_type, _IntegralType)
                else "get(x, 'key')"
            )
            fn_sql_with_replaced_args = fn_sql.replace(l_arg1, key_exp).replace(
                l_arg2, "strip_null_value(get(x, 'value'))"
            )
            last_win_dedup = global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            reduce_exp = snowpark_fn.function("reduce")(
                _map_to_array_udf(snowpark_fn.cast(arg1_tc.col, VariantType())),
                snowpark_fn.object_construct(),
                snowpark_fn.sql_expr(
                    # value is cast to variant because object_insert doesn't allow structured types,
                    # and structured types are not coercible to variant
                    # TODO: allow structured types in object_insert?
                    f"(acc, x) -> object_insert(acc, {fn_sql_with_replaced_args}, x:value::variant, {last_win_dedup})"
                ),
            )
            result_type = MapType(fn_body.typ, val_type)
            result_exp = snowpark_fn.cast(
                reduce_exp,
                result_type,
            )
            snowpark_arg_names = [
                arg1_name,
                f"lambdafunction({lambda_body_name}, namedlambdavariable(), namedlambdavariable())",
            ]

        case "transform_values":
            _map_to_array_udf = cached_udf(
                _map_to_array,
                input_types=[VariantType()],
                return_type=ArrayType(),
                packages=[],
            )
            key_type, val_type = _get_map_types(arg1_tc)

            lambda_exp = exp.unresolved_function.arguments[1]
            # Due to lack of direct equivalent API in Snowflake, we need to transform the lambda expression
            # Rather than traversing the entire lambda AST, we use string manipulation on the query
            # We randomize lambda argument names to minimize the risk of accidental replacements in the query
            _randomize_lambda_args_names(lambda_exp)
            ([lambda_body_name], fn_body) = _resolve_lambda(
                lambda_exp,
                [key_type, val_type],
                resolve_only_body=True,
            )

            l_arg1 = lambda_exp.lambda_function.arguments[0].name_parts[0]
            l_arg2 = lambda_exp.lambda_function.arguments[1].name_parts[0]

            analyzer = Session.get_active_session()._analyzer
            fn_sql = analyzer.analyze(fn_body.col._expression, defaultdict())
            # if the key is a number, we need to cast it
            # otherwise it seems to be treated as a string
            key_exp = (
                "get(x, 'key')::int"
                if isinstance(key_type, _IntegralType)
                else "get(x, 'key')"
            )
            fn_sql_with_replaced_args = fn_sql.replace(l_arg1, key_exp).replace(
                l_arg2, "strip_null_value(get(x, 'value'))"
            )
            last_win_dedup = global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            reduce_exp = snowpark_fn.function("reduce")(
                _map_to_array_udf(snowpark_fn.cast(arg1_tc.col, VariantType())),
                snowpark_fn.object_construct(),
                snowpark_fn.sql_expr(
                    # value is cast to variant because object_insert doesn't allow structured types,
                    # and structured types are not coercible to variant
                    # TODO: allow structured types in object_insert?
                    f"(acc, x) -> object_insert(acc, x:key, nvl(({fn_sql_with_replaced_args})::variant, parse_json('null')), {last_win_dedup})"
                ),
            )
            result_type = MapType(key_type, fn_body.typ)
            result_exp = snowpark_fn.cast(
                reduce_exp,
                result_type,
            )
            snowpark_arg_names = [
                arg1_name,
                f"lambdafunction({lambda_body_name}, namedlambdavariable(), namedlambdavariable())",
            ]

        case "zip_with":
            """
            This impl is a workaround since Snowflake SQL lacks native support of `zip_with`:
             - Use `arrays_zip` to combine two input arrays into a single array of structs with fields $1 and $2
             - Resolve only the body of the lambda function from the 3rd argument (which is a standard `unresolved_function` expression)
             - Convert a resolved expression into raw SQL using the analyzer (this SQL references original lambda args)
             - Replace lambda arg references in SQL with get(x,'$1') and get(x,'$2') accessors
             - Construct a new lambda 'x -> modified_sql'
             - Apply `transform` function to transform the zipped array using that lambda
            """
            arr2 = exp.unresolved_function.arguments[1]
            ([arg2_name], arg2_tc) = map_expression(arr2, column_mapping, typer)

            zip_exp = snowpark_fn.arrays_zip(arg1_tc.col, arg2_tc.col)
            lambda_exp = exp.unresolved_function.arguments[2]
            # Due to lack of direct equivalent API in Snowflake, we need to transform the lambda expression.
            # Rather than traversing the entire lambda AST, we use string manipulation on the query.
            # We randomize lambda argument names to minimize the risk of accidental replacements in the query.
            _randomize_lambda_args_names(lambda_exp)
            ([lambda_body_name], fn_body) = _resolve_lambda(
                lambda_exp,
                [arg1_tc.typ.element_type, arg2_tc.typ.element_type],
                resolve_only_body=True,
            )
            l_arg1 = lambda_exp.lambda_function.arguments[0].name_parts[0]
            l_arg2 = lambda_exp.lambda_function.arguments[1].name_parts[0]
            analyzer = Session.get_active_session()._analyzer
            fn_sql = analyzer.analyze(fn_body.col._expression, defaultdict())
            transform_sql = fn_sql.replace(l_arg1, "get(x, '$1')").replace(
                l_arg2, "get(x, '$2')"
            )
            transform_exp = snowpark_fn.sql_expr(f"x -> {transform_sql}")
            snowpark_arg_names = [
                arg1_name,
                arg2_name,
                f"lambdafunction({lambda_body_name}, namedlambdavariable(), namedlambdavariable())",
            ]
            result_exp = snowpark_fn.function("transform")(zip_exp, transform_exp)
            result_exp = TypedColumn(result_exp, lambda: [ArrayType(fn_body.typ)])
        case other:
            # TODO: Add more here as we come across them.
            exception = SnowparkConnectNotImplementedError(
                f"Unsupported function name {other}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception

    spark_function_name = f"{function_name}({', '.join(snowpark_arg_names)})"
    if not isinstance(result_exp, TypedColumn):
        tc = TypedColumn(
            result_exp,
            lambda: (
                [result_type] if result_type is not None else typer.type(result_exp)
            ),
        )
    else:
        tc = result_exp
    return [spark_function_name], tc


def _resolve_first_value(exp, snowpark_args):
    """
    Utility method to perform first function.
    """
    args = exp.unresolved_function.arguments
    ignore_nulls = unwrap_literal(args[1]) if len(args) > 1 else False
    return snowpark_fn.first_value(snowpark_args[0], ignore_nulls)


def _resolve_last_value(exp, snowpark_args):
    """
    Utility method to perform last function.
    """
    args = exp.unresolved_function.arguments
    ignore_nulls = unwrap_literal(args[1]) if len(args) > 1 else False
    return snowpark_fn.last_value(snowpark_args[0], ignore_nulls)


def _aes_helper(function_name, value, passphrase, aad, encryption_method, padding):
    """
    Utility method to perform AES encryption and decryption.
    """
    # Handle NULL values - if any required parameter is NULL, return NULL
    # This matches PySpark behavior where NULL inputs result in NULL output
    null_check = (
        snowpark_fn.is_null(value)
        | snowpark_fn.is_null(passphrase)
        | snowpark_fn.is_null(encryption_method)
        | snowpark_fn.is_null(padding)
        | snowpark_fn.is_null(aad)
    )

    aes_function = snowpark_fn.function(function_name)
    return snowpark_fn.when(null_check, snowpark_fn.lit(None)).otherwise(
        aes_function(
            value,
            passphrase,
            snowpark_fn.when(
                (encryption_method == snowpark_fn.lit("DEFAULT"))
                | (snowpark_fn.lower(encryption_method) == snowpark_fn.lit("gcm")),
                aad,
            ),
            snowpark_fn.concat(
                snowpark_fn.lit("AES-"),
                snowpark_fn.when(
                    encryption_method == snowpark_fn.lit("DEFAULT"), "GCM"
                ).otherwise(encryption_method),
                snowpark_fn.when(
                    padding == snowpark_fn.lit("DEFAULT"),
                    snowpark_fn.lit(None),
                ).otherwise(snowpark_fn.concat(snowpark_fn.lit("/pad:"), padding)),
            ),
        )
    )


def _bounded_decimal(precision: int, scale: int) -> DecimalType:
    return DecimalType(min(38, precision), min(37, scale))


def _cast_with_decimal_overflow_check(
    exp: Column, result_type: DecimalType, should_raise_on_overflow: bool
) -> Column:
    max_abs = snowpark_fn.lit(float(10 ** (result_type.precision - result_type.scale)))
    overflow_condition = (exp.cast(DoubleType()) >= max_abs) | (
        exp.cast(DoubleType()) <= -max_abs
    )
    if should_raise_on_overflow:
        raise_error = _raise_error_helper(result_type, ArithmeticException)
        return snowpark_fn.when(
            overflow_condition,
            raise_error(
                snowpark_fn.lit(
                    f"[NUMERIC_VALUE_OUT_OF_RANGE] Value cannot be represented as DECIMAL({result_type.precision},{result_type.scale}). "
                    f'If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error, and return NULL instead.'
                )
            ),
        ).otherwise(snowpark_fn.cast(exp, result_type))
    else:
        return snowpark_fn.when(overflow_condition, snowpark_fn.lit(None)).otherwise(
            snowpark_fn.cast(exp, result_type)
        )


def _to_char(arg: Column, encode: str = "utf-8") -> Column:
    return snowpark_fn.to_char(arg, snowpark_fn.lit(encode))


def _try_to_cast(function_name: str, execute_if_true: Column, *arguments) -> Column:
    # This function tries to cast all of the passed arguments using a given function.
    # This ensures that invalid inputs are handled gracefully by falling back to a default behavior
    # (e.g., returning NULL if ANSI mode is enabled or raising an appropriate error).
    if global_config.spark_sql_ansi_enabled:
        return execute_if_true

    combined_conditions = reduce(
        operator.iand,
        (
            snowpark_fn.builtin(function_name)(
                snowpark_fn.cast(arg, StringType())
            ).isNotNull()
            for arg in arguments
        ),
    )

    return snowpark_fn.when(combined_conditions, execute_if_true).otherwise(
        snowpark_fn.lit(None)
    )


def _try_sum_helper(
    arg_type: DataType, col_name: Column, calculating_avg: bool = False
) -> tuple[Column, DataType]:
    # This function calculates the sum or average of a Snowpark column (`col_name`) based on its
    # data type (`arg_type`) and whether an average is requested (`calculating_avg`).
    #
    # Its main behavioral characteristics are:
    #
    # 1. For Integral and Decimal Types:
    #    - It uses custom User-Defined Aggregate Functions (UDAFs) to compute the sum.
    #    - BEHAVIOR: If an arithmetic overflow occurs during summation for these types,
    #      the function returns `None` (null) for the sum.
    #    - If `calculating_avg` is True (which it will never be for Integral Types):
    #        - If the sum results in `None` (due to overflow), the average is also `None`.
    #        - Otherwise, the average is the (non-overflowed) sum divided by the count of non-null rows.
    #
    # 2. For Floating-Point Types (_FractionalType like Float, Double) or other types
    #    that are try-casted to Double:
    #    - It uses the standard `snowpark_fn.sum()` aggregate function.
    #    - BEHAVIOR: If an overflow occurs, the sum will be `Infinity` or `-Infinity`,
    #      following Snowflake's default behavior for floating-point sums.
    #    - If `calculating_avg` is True, the average is this sum (which could be Infinity)
    #      divided by the count of non-null rows.
    #
    # In essence, this function provides a "try_sum" or "try_avg" behavior, specifically
    # aiming to convert overflows into `None` for exact numeric types (integers, decimals),
    # while letting floating-point overflows behave as they normally would in Snowflake.
    # It returns the resulting aggregate column and its Snowpark DataType.

    match arg_type:
        case _IntegralType():

            class TrySumIntegerUDAF:
                def __init__(self) -> None:
                    self.agg_sum = None
                    self.max_int = sys.maxsize
                    self.min_int = -sys.maxsize - 1
                    self.overflowed = False

                @property
                def aggregate_state(self):
                    # overflow will return NaN, null col will return NULL, otherwise the sum
                    return float("nan") if self.overflowed else self.agg_sum

                def accumulate(self, input_num):
                    if not self.overflowed:
                        if input_num is not None:
                            if (
                                self.agg_sum is None
                            ):  # the input sum is non null but the agg is
                                self.agg_sum = input_num
                            elif self.agg_sum > (
                                self.max_int - input_num
                            ) or self.agg_sum < (
                                self.min_int - input_num
                            ):  # neither are null but will cause overflow
                                self.overflowed = True
                            else:
                                self.agg_sum += (
                                    input_num  # neither are null, no overflow
                                )

                def merge(self, other_sum):
                    if not self.overflowed:
                        if other_sum is None:
                            pass  # agg_sum stays the same, the other sum is empty
                        elif isinstance(other_sum, float) and math.isnan(other_sum):
                            self.overflowed = True  # if we merge two together and one has overflowed, the agg overflows
                        elif (
                            self.agg_sum is None
                        ):  # other sum isn't none but agg_sum is
                            self.agg_sum = other_sum
                        elif self.agg_sum > (
                            self.max_int - other_sum
                        ) or self.agg_sum < (self.min_int - other_sum):
                            self.overflowed = True
                        else:
                            self.agg_sum += other_sum

                def finish(self):
                    return None if self.overflowed else self.agg_sum

            _try_sum_int_udaf = cached_udaf(
                TrySumIntegerUDAF,
                return_type=arg_type,
                input_types=[arg_type],
            )
            # call the udaf
            return _try_sum_int_udaf(col_name), LongType()

            # NOTE: We will never call this function with an IntegerType column and calculating_avg=True. Therefore,
            # we don't need to handle the case where calculating_avg=True here. The caller of this function will handle it.

        case DecimalType():

            class TrySumDecimalUDAF:
                def __init__(self) -> None:
                    self.agg_sum = Decimal(0.00)
                    self.max_decimal = Decimal("9" * 38 + "." + "9" * abs(0))
                    self.min_decimal = -self.max_decimal
                    self.overflowed = False

                @property
                def aggregate_state(self):
                    return (
                        float("nan")
                        if self.overflowed
                        else (self.agg_sum, self.max_decimal)
                    )

                def accumulate(self, input_num, precision: int = 38, scale: int = 0):
                    self.max_decimal = Decimal("9" * precision + "." + "9" * abs(scale))
                    self.min_decimal = -self.max_decimal

                    if not self.overflowed:
                        if input_num is not None:
                            if (
                                self.agg_sum is None
                            ):  # the input sum is non null but the agg is
                                self.agg_sum = input_num
                            elif self.agg_sum > (
                                self.max_decimal - input_num
                            ) or self.agg_sum < (
                                self.min_decimal - input_num
                            ):  # neither are null but will cause overflow
                                self.overflowed = True
                            else:
                                self.agg_sum += (
                                    input_num  # neither are null, no overflow
                                )

                def merge(self, other_sum):
                    if not self.overflowed:
                        # Check if other_sum indicates overflow (float nan)
                        if isinstance(other_sum, float) and math.isnan(other_sum):
                            self.overflowed = True
                        else:
                            # Check if other_sum is a tuple (normal case) or handle edge cases
                            if isinstance(other_sum, tuple):
                                self.max_decimal = other_sum[1]
                                self.min_decimal = -self.max_decimal
                                other_sum = other_sum[0]
                            # If not a tuple, other_sum is already the value we need

                            if other_sum is None:
                                pass  # agg_sum stays the same, the other sum is empty
                            elif (
                                self.agg_sum is None
                            ):  # other sum isn't none but agg_sum is
                                self.agg_sum = other_sum
                            elif self.agg_sum > (
                                self.max_decimal - other_sum
                            ) or self.agg_sum < (self.min_decimal - other_sum):
                                self.overflowed = True
                            else:
                                self.agg_sum += other_sum

                def finish(self):
                    return None if self.overflowed else self.agg_sum

            _try_sum_decimal_udaf = cached_udaf(
                TrySumDecimalUDAF,
                return_type=DecimalType(
                    arg_type.precision,
                    arg_type.scale,
                ),
                input_types=[
                    DecimalType(
                        arg_type.precision,
                        arg_type.scale,
                    ),
                    IntegerType(),
                    IntegerType(),
                ],
            )

            aggregate_sum = _try_sum_decimal_udaf(
                col_name,
                snowpark_fn.lit(arg_type.precision),
                snowpark_fn.lit(arg_type.scale),
            )
            # if calculating_avg is True, we need to divide the sum by the count of non-null rows
            if calculating_avg:
                new_type = DecimalType(
                    precision=min(38, arg_type.precision + 4),
                    scale=min(38, arg_type.scale + 4),
                )
                if aggregate_sum is snowpark_fn.lit(None):
                    return snowpark_fn.lit(None), new_type
                else:
                    non_null_rows = snowpark_fn.count(col_name)
                    # Use _divnull to handle case when non_null_rows is 0
                    return _divnull(aggregate_sum, non_null_rows), new_type
            else:
                new_type = DecimalType(
                    precision=min(38, arg_type.precision + 10), scale=arg_type.scale
                )
                # Return NULL when there are no non-null values (i.e., all values are NULL); this is handled using case/when to check for non-null values for both SUM and the sum component of AVG calculations.
                non_null_rows = snowpark_fn.count(col_name)
                result = snowpark_fn.when(
                    non_null_rows == 0, snowpark_fn.lit(None)
                ).otherwise(aggregate_sum)
                return result, new_type

        case _:
            # If the input column is floating point (double and float are synonymous in Snowflake per
            # the numeric types documentation), we can just let it go through to Snowflake, where overflow
            # matches Spark and goes to inf.
            if not isinstance(arg_type, _FractionalType):
                cleaned = _try_cast_helper(col_name, DoubleType())
                aggregate_sum = snowpark_fn.sum(cleaned)
            else:
                aggregate_sum = snowpark_fn.sum(col_name)

            # if calculating_avg is True, we need to divide the sum by the count of non-null rows
            if calculating_avg:
                if aggregate_sum is snowpark_fn.lit(None):
                    return snowpark_fn.lit(None), DoubleType()
                else:
                    non_null_rows = snowpark_fn.count(col_name)
                    # Use _divnull to handle case when non_null_rows is 0
                    return _divnull(aggregate_sum, non_null_rows), DoubleType()
            else:
                # When all values are NULL, SUM should return NULL (not 0)
                # Use case/when to return NULL when there are no non-null values (i.e., all values are NULL)
                non_null_rows = snowpark_fn.count(col_name)
                result = snowpark_fn.when(
                    non_null_rows == 0, snowpark_fn.lit(None)
                ).otherwise(aggregate_sum)
                return result, DoubleType()


def _get_type_precision_from_datatype(typ: DataType) -> tuple[int, int]:
    """
    Returns (precision, scale) for a given DataType.
    For integral types, returns the number of digits needed to represent the maximum value.
    For decimal types, returns the type's precision and scale.
    """
    match typ:
        case DecimalType():
            return typ.precision, typ.scale
        case ByteType():
            return 3, 0  # -128 to 127
        case ShortType():
            return 5, 0  # -32768 to 32767
        case IntegerType():
            return 10, 0  # -2147483648 to 2147483647
        case LongType():
            return 20, 0  # -9223372036854775808 to 9223372036854775807
        case NullType():
            return 0, 0  # NULL
        case _:
            return 38, 0  # Default to maximum precision for other types


def _get_type_precision(operand: OperandInfo) -> tuple[int, int]:
    """
    Returns (precision, scale) needed for a given operand.
    For integral literals, computes precision from the actual literal value.
    Otherwise delegates to _get_type_precision_from_datatype.
    """
    if operand.is_literal and isinstance(operand.typ, _IntegralType):
        return _get_type_precision_for_integral_literal(
            operand.typ, val=operand.arg_name
        )
    return _get_type_precision_from_datatype(operand.typ)


def _get_type_precision_for_integral_literal(typ: _IntegralType, val: str):
    # https://github.com/apache/spark/blob/dd22010c7a781bf4bb073bb44c6dacfce92c614a/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/types/DataTypeUtils.scala#L244-L252
    assert isinstance(typ, _IntegralType), "Provided type must be _IntegralType"

    if isinstance(typ, ByteType):
        return 3, 0

    d = Decimal(val)
    _sign, digits, exponent = d.as_tuple()
    assert exponent >= 0, "The _IntegralType literal should have no fractional part"
    return len(digits), 0


def _decimal_add_sub_result_type_helper(p1, s1, p2, s2):
    """
    Computes the result precision and scale for DECIMAL(p1, s1) + DECIMAL(p2, s2)
    according to Spark SQL rules, including truncation logic.

    Returns a tuple: (result_precision, result_scale) or None if overflow (NULL in Spark).
    """
    # initial result precision and scale
    result_scale = max(s1, s2)
    int_digits = max(p1 - s1, p2 - s2)
    result_precision = int_digits + result_scale + 1
    return_type_precision, return_type_scale = result_precision, result_scale

    # check if truncation is needed
    if result_precision <= 38:
        return result_precision, result_scale, return_type_precision, return_type_scale
    else:
        return_type_precision = 38

    # truncate scale to preserve at least 6 fractional digits
    min_scale = 6
    while result_scale > min_scale:
        result_scale -= 1
        return_type_scale = result_scale
        result_precision = int_digits + result_scale + 1
        if result_precision <= 38:
            return (
                result_precision,
                result_scale,
                return_type_precision,
                return_type_scale,
            )

    # final check with minimum scale
    result_precision = int_digits + min_scale + 1
    return result_precision, min_scale, return_type_precision, return_type_scale


def _get_decimal_multiplication_result_type(p1, s1, p2, s2) -> tuple[DecimalType, bool]:
    result_precision = p1 + p2 + 1
    result_scale = s1 + s2
    overflow_possible = False
    if result_precision > 38:
        overflow_possible = True
        if result_scale > 6:
            overflow = result_precision - 38
            result_scale = max(6, result_scale - overflow)
        result_precision = 38
    return DecimalType(result_precision, result_scale), overflow_possible


def _arithmetic_operation(
    arg1: TypedColumn,
    arg2: TypedColumn,
    op: Callable[[Column, Column], Column],
    overflow_possible: bool,
    should_raise_on_overflow: bool,
    target_type: DataType,
    operation_name: str,
) -> Column:
    if isinstance(target_type, _IntegralType):
        raw_result = op(arg1.col, arg2.col)
        return apply_arithmetic_overflow_with_ansi_check(
            raw_result, target_type, should_raise_on_overflow, operation_name
        )

    def _cast_arg(tc: TypedColumn) -> Column:
        _, s = _get_type_precision(OperandInfo(tc))
        typ = (
            DoubleType()
            if s > 0
            or (
                isinstance(tc.typ, _FractionalType)
                and not isinstance(tc.typ, DecimalType)
            )
            else LongType()
        )
        return tc.col.cast(typ)

    op_for_overflow_check = op(arg1.col.cast(DoubleType()), arg2.col.cast(DoubleType()))
    direct_op = op(arg1.col, arg2.col)

    if overflow_possible:
        if not isinstance(arg1.typ, DecimalType) or not isinstance(
            arg2.typ, DecimalType
        ):
            direct_op = op(_cast_arg(arg1), _cast_arg(arg2))

        return _cast_arithmetic_operation_result(
            op_for_overflow_check, direct_op, target_type, should_raise_on_overflow
        )
    else:
        return direct_op.cast(target_type)


def _cast_arithmetic_operation_result(
    overflow_check_expr: Column,
    result_expr: Column,
    target_type: DecimalType,
    should_raise_on_overflow: bool,
) -> Column:
    """
    Casts an arithmetic operation result to the target decimal type with overflow detection.
    This function uses a dual-expression approach for robust overflow handling:
    Args:
        overflow_check_expr: Arithmetic expression using DoubleType operands for overflow detection.
                           This expression is used ONLY for boundary checking against the target
                           decimal's min/max values. DoubleType preserves the magnitude of large
                           intermediate results that might overflow in decimal arithmetic.
        result_expr: Arithmetic expression using safer operand types (LongType for integers,
                    DoubleType for fractionals) for the actual result computation.
        target_type: Target DecimalType to cast the result to.
        should_raise_on_overflow: If True raises ArithmeticException on overflow, if False, returns NULL on overflow.
    """

    def create_overflow_handler(min_val, max_val, type_name: str):
        if should_raise_on_overflow:
            raise_error = _raise_error_helper(target_type, ArithmeticException)
            return snowpark_fn.when(
                (overflow_check_expr < snowpark_fn.lit(min_val))
                | (overflow_check_expr > snowpark_fn.lit(max_val)),
                raise_error(
                    snowpark_fn.lit(
                        f'[NUMERIC_VALUE_OUT_OF_RANGE] Value cannot be represented as {type_name}. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error, and return NULL instead.'
                    )
                ),
            ).otherwise(result_expr.cast(target_type))
        else:
            return snowpark_fn.when(
                (overflow_check_expr < snowpark_fn.lit(min_val))
                | (overflow_check_expr > snowpark_fn.lit(max_val)),
                snowpark_fn.lit(None),
            ).otherwise(result_expr.cast(target_type))

    precision = target_type.precision
    scale = target_type.scale

    max_val = (10**precision - 1) / (10**scale)
    min_val = -max_val

    return create_overflow_handler(min_val, max_val, f"DECIMAL({precision},{scale})")


def _get_decimal_division_result_type(p1, s1, p2, s2) -> tuple[DecimalType, bool]:
    overflow_possible = False
    result_scale = max(6, s1 + p2 + 1)
    result_precision = p1 - s1 + s2 + result_scale
    if result_precision > 38:
        overflow_possible = True
        overflow = result_precision - 38
        result_scale = max(6, result_scale - overflow)
        result_precision = 38
    return DecimalType(result_precision, result_scale), overflow_possible


def _try_arithmetic_helper(
    operand_left: OperandInfo,
    operand_right: OperandInfo,
    operation_type: int,
) -> tuple[Column, DataType | None]:
    # Constructs a Snowpark Column expression for a "try-style" arithmetic operation
    # (addition or subtraction, determined by `operation_type`) between two input columns.
    #
    # Key behavioral characteristics:
    # 1. For **Integral inputs**: Explicitly checks for overflow/underflow at the result type boundaries.
    #    - BEHAVIOR: Returns a NULL literal if the operation would exceed these limits;
    #      otherwise, returns the result of the standard Snowpark `+` or `-`.
    #
    # 2. For **other Numeric types, or String types** (which are first passed to
    #    `_validate_numeric_args` for attempted numeric conversion):
    #    - BEHAVIOR: Applies the standard Snowpark `+` or `-` operator. The outcome of this
    #      (e.g., for float overflow, decimal limits) depends on Snowflake's default
    #      behavior for these standard arithmetic operations on the given types.
    #
    # Arithmetic operations involving **Boolean types** will raise an `AnalysisException`.
    # All other unhandled incompatible type combinations result in a NULL literal.
    # The function returns the resulting Snowpark Column expression.

    # Extract typed columns and snowpark columns from operands
    typed_args = [operand_left.typed_column, operand_right.typed_column]
    snowpark_args = [operand_left.col, operand_right.col]

    match (operand_left.typ, operand_right.typ):
        case (_IntegralType() as t1, _IntegralType() as t2):
            result_type = _find_common_type([t1, t2])
            min_val, max_val = get_integral_type_bounds(result_type)

            if operation_type == 0:  # Addition
                result_exp = (
                    snowpark_fn.when(
                        (snowpark_args[0] > 0)
                        & (snowpark_args[1] > 0)
                        & (
                            snowpark_args[0]
                            > snowpark_fn.lit(max_val) - snowpark_args[1]
                        ),
                        snowpark_fn.lit(None),
                    )
                    .when(
                        (snowpark_args[0] < 0)
                        & (snowpark_args[1] < 0)
                        & (
                            snowpark_args[0]
                            < snowpark_fn.lit(min_val) - snowpark_args[1]
                        ),
                        snowpark_fn.lit(None),
                    )
                    .otherwise((snowpark_args[0] + snowpark_args[1]).cast(result_type))
                )
            else:  # Subtraction
                result_exp = (
                    snowpark_fn.when(
                        (snowpark_args[0] > 0)
                        & (snowpark_args[1] < 0)
                        & (
                            snowpark_args[0]
                            > snowpark_fn.lit(max_val) + snowpark_args[1]
                        ),
                        snowpark_fn.lit(None),
                    )
                    .when(
                        (snowpark_args[0] < 0)
                        & (snowpark_args[1] > 0)
                        & (
                            snowpark_args[0]
                            < snowpark_fn.lit(min_val) + snowpark_args[1]
                        ),
                        snowpark_fn.lit(None),
                    )
                    .otherwise((snowpark_args[0] - snowpark_args[1]).cast(result_type))
                )
            return result_exp, result_type
        case (DateType(), _) | (_, DateType()):
            arg1, arg2 = typed_args[0].typ, typed_args[1].typ
            # Valid input parameter types for try_add - DateType and _NumericType, _NumericType and DateType.
            # For try_subtract, valid types are DateType, _NumericType and DateType, DateType.
            if operation_type == 0:
                if (
                    isinstance(arg1, DateType) and not isinstance(arg2, _IntegralType)
                ) or (
                    isinstance(arg2, DateType) and not isinstance(arg1, _IntegralType)
                ):
                    exception = AnalysisException(
                        '[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "date_add(dt, add)" due to data type mismatch: Parameter 2 requires the ("INT" or "SMALLINT" or "TINYINT") type'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                args = (
                    snowpark_args[::-1]
                    if isinstance(arg1, _IntegralType)
                    else snowpark_args
                )
                return (
                    _try_to_cast(
                        "try_to_date",
                        snowpark_fn.cast(snowpark_fn.date_add(*args), DateType()),
                        args[0],
                    ),
                    None,
                )
            else:
                if isinstance(arg1, DateType) and isinstance(arg2, _IntegralType):
                    return (
                        _try_to_cast(
                            "try_to_date",
                            snowpark_fn.to_date(
                                snowpark_fn.date_sub(snowpark_args[0], snowpark_args[1])
                            ),
                            snowpark_args[0],
                        ),
                        None,
                    )
                elif isinstance(arg1, DateType) and isinstance(arg2, DateType):
                    return snowpark_fn.daydiff(snowpark_args[0], snowpark_args[1]), None
                else:
                    exception = AnalysisException(
                        '[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "date_sub(dt, sub)" due to data type mismatch: Parameter 1 requires the "DATE" type and parameter 2 requires the ("INT" or "SMALLINT" or "TINYINT") type'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
        case (DecimalType(), _IntegralType()) | (_IntegralType(), DecimalType()) | (
            DecimalType(),
            DecimalType(),
        ):
            result_type, overflow_possible = _get_add_sub_result_type(
                operand_left,
                operand_right,
                "try_add" if operation_type == 0 else "try_subtract",
            )

            return (
                _arithmetic_operation(
                    typed_args[0],
                    typed_args[1],
                    lambda x, y: x + y if operation_type == 0 else x - y,
                    overflow_possible,
                    False,
                    result_type,
                    "add" if operation_type == 0 else "subtract",
                ),
                result_type,
            )

        # If either of the inputs is floating point, we can just let it go through to Snowflake, where overflow
        # matches Spark and goes to inf.
        # Note that we already handle the int,int case above, hence it is okay to use the broader _numeric
        # below.
        case (_NumericType() as t1, _NumericType() as t2):
            result_type = _find_common_type([t1, t2])
            if operation_type == 0:
                return snowpark_args[0] + snowpark_args[1], result_type
            else:
                return snowpark_args[0] - snowpark_args[1], result_type
        # String cases - try to convert to numeric
        case (
            (StringType(), _NumericType())
            | (_NumericType(), StringType())
            | (
                StringType(),
                StringType(),
            )
        ):
            # It's ok to use _validate_numeric_args here because we already know it will not throw because we
            # are only dealing with string and numeric.
            if operation_type == 0:
                updated_args = _validate_numeric_args(
                    "try_add", typed_args, snowpark_args
                )
                return updated_args[0] + updated_args[1], None
            else:
                updated_args = _validate_numeric_args(
                    "try_subtract", typed_args, snowpark_args
                )
                return updated_args[0] - updated_args[1], None

        case (BooleanType(), _) | (_, BooleanType()):
            exception = AnalysisException(
                f"Incompatible types: {typed_args[0].typ}, {typed_args[1].typ}"
            )
            attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
            raise exception
        case _:
            # Return NULL for incompatible types
            return snowpark_fn.lit(None), None


def _get_add_sub_result_type(
    operand_left: OperandInfo,
    operand_right: OperandInfo,
    spark_function_name: str,
) -> tuple[DataType, bool]:
    overflow_possible = False
    result_type = _find_common_type([operand_left.typ, operand_right.typ])
    match result_type:
        case DecimalType():
            p1, s1 = _get_type_precision(operand_left)
            p2, s2 = _get_type_precision(operand_right)
            result_scale = max(s1, s2)
            result_precision = max(p1 - s1, p2 - s2) + result_scale + 1
            if result_precision > 38:
                overflow_possible = True
                if result_scale > 6:
                    overflow = result_precision - 38
                    result_scale = max(6, result_scale - overflow)
                result_precision = 38
            result_type = DecimalType(result_precision, result_scale)
        case NullType():
            result_type = DoubleType()
        case StringType():
            match (operand_left.typ, operand_right.typ):
                case (_FractionalType(), _) | (_, _FractionalType()):
                    result_type = DoubleType()
                case (_IntegralType(), _) | (_, _IntegralType()):
                    result_type = (
                        LongType()
                        if global_config.spark_sql_ansi_enabled
                        else DoubleType()
                    )
                case _:
                    if global_config.spark_sql_ansi_enabled:
                        exception = AnalysisException(
                            f'[DATATYPE_MISMATCH.BINARY_OP_WRONG_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: the binary operator requires the input type ("NUMERIC" or "INTERVAL DAY TO SECOND" or "INTERVAL YEAR TO MONTH" or "INTERVAL"), not "STRING".',
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
                    else:
                        result_type = DoubleType()
        case BooleanType():
            exception = AnalysisException(
                f'[DATATYPE_MISMATCH.BINARY_OP_WRONG_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: the binary operator requires the input type ("NUMERIC" or "INTERVAL DAY TO SECOND" or "INTERVAL YEAR TO MONTH" or "INTERVAL"), not "BOOLEAN".',
            )
            attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
            raise exception
    return result_type, overflow_possible


def _get_interval_type_name(interval_type: _AnsiIntervalType) -> str:
    """Get the formatted interval type name for error messages."""
    if isinstance(interval_type, YearMonthIntervalType):
        if interval_type.start_field == 0 and interval_type.end_field == 0:
            return "INTERVAL YEAR"
        elif interval_type.start_field == 1 and interval_type.end_field == 1:
            return "INTERVAL MONTH"
        else:
            return "INTERVAL YEAR TO MONTH"
    else:  # DayTimeIntervalType
        if interval_type.start_field == 0 and interval_type.end_field == 0:
            return "INTERVAL DAY"
        elif interval_type.start_field == 1 and interval_type.end_field == 1:
            return "INTERVAL HOUR"
        elif interval_type.start_field == 2 and interval_type.end_field == 2:
            return "INTERVAL MINUTE"
        elif interval_type.start_field == 3 and interval_type.end_field == 3:
            return "INTERVAL SECOND"
        else:
            return "INTERVAL DAY TO SECOND"


def _check_interval_string_comparison(
    operator: str, snowpark_typed_args: List[TypedColumn], snowpark_arg_names: List[str]
) -> None:
    """Check for invalid interval-string comparisons and raise AnalysisException if found."""
    if (
        isinstance(snowpark_typed_args[0].typ, _AnsiIntervalType)
        and isinstance(snowpark_typed_args[1].typ, StringType)
        or isinstance(snowpark_typed_args[0].typ, StringType)
        and isinstance(snowpark_typed_args[1].typ, _AnsiIntervalType)
    ):
        # Format interval type name for error message
        interval_type = (
            snowpark_typed_args[0].typ
            if isinstance(snowpark_typed_args[0].typ, _AnsiIntervalType)
            else snowpark_typed_args[1].typ
        )
        interval_name = _get_interval_type_name(interval_type)

        left_type = (
            "STRING"
            if isinstance(snowpark_typed_args[0].typ, StringType)
            else interval_name
        )
        right_type = (
            "STRING"
            if isinstance(snowpark_typed_args[1].typ, StringType)
            else interval_name
        )

        exception = AnalysisException(
            f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "({snowpark_arg_names[0]} {operator} {snowpark_arg_names[1]})" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{left_type}" and "{right_type}").;'
        )
        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
        raise exception


def _get_spark_function_name(
    col1: TypedColumn,
    col2: TypedColumn,
    snowpark_arg_names: list[str],
    exp: expressions_proto.Expression,
    default_spark_function_name: str,
    function_name: str,
):
    operation_op = function_name
    match function_name:
        case "+":
            operation_func = "date_add"
        case "-":
            operation_func = "date_sub"
        case _:
            return default_spark_function_name
    match (col1.typ, col2.typ):
        case (DateType(), DateType()):
            date_param_name1 = _get_literal_param_name(exp, 0, snowpark_arg_names[0])
            date_param_name2 = _get_literal_param_name(exp, 1, snowpark_arg_names[1])
            return f"({date_param_name1} {operation_op} {date_param_name2})"
        case (StringType(), DateType()):
            date_param_name2 = _get_literal_param_name(exp, 1, snowpark_arg_names[1])
            if (
                hasattr(col1.col._expr1, "pretty_name")
                and "INTERVAL" == col1.col._expr1.pretty_name
            ):
                return f"{date_param_name2} {operation_op} {snowpark_arg_names[0]}"
            elif global_config.spark_sql_ansi_enabled and function_name == "+":
                return f"{operation_func}(cast({date_param_name2} as date), cast({snowpark_arg_names[0]} as double))"
            else:
                return f"({snowpark_arg_names[0]} {operation_op} {date_param_name2})"
        case (DateType(), StringType()):
            date_param_name1 = _get_literal_param_name(exp, 0, snowpark_arg_names[0])
            if global_config.spark_sql_ansi_enabled or (
                hasattr(col2.col._expr1, "pretty_name")
                and "INTERVAL" == col2.col._expr1.pretty_name
            ):
                return f"{date_param_name1} {operation_op} {snowpark_arg_names[1]}"
            else:
                return f"{operation_func}(cast({date_param_name1} as date), cast({snowpark_arg_names[1]} as double))"
        case (DateType(), DayTimeIntervalType()) | (
            DateType(),
            YearMonthIntervalType(),
        ) | (TimestampType(), DayTimeIntervalType()) | (
            TimestampType(),
            YearMonthIntervalType(),
        ):
            date_param_name1 = _get_literal_param_name(exp, 0, snowpark_arg_names[0])
            return f"{date_param_name1} {operation_op} {snowpark_arg_names[1]}"
        case (DayTimeIntervalType(), DateType()) | (
            YearMonthIntervalType(),
            DateType(),
        ) | (DayTimeIntervalType(), TimestampType()) | (
            YearMonthIntervalType(),
            TimestampType(),
        ):
            date_param_name2 = _get_literal_param_name(exp, 1, snowpark_arg_names[1])
            if function_name == "+":
                return f"{date_param_name2} {operation_op} {snowpark_arg_names[0]}"
            else:
                return default_spark_function_name
        case (DateType() as dt, _) | (_, DateType() as dt):
            date_param_index = 0 if dt == col1.typ else 1
            date_param_name = _get_literal_param_name(
                exp, date_param_index, snowpark_arg_names[date_param_index]
            )
            return f"{operation_func}({date_param_name}, {snowpark_arg_names[1 - date_param_index]})"
        case _:
            return default_spark_function_name


def _get_literal_param_name(exp, arg_index: int, default_param_name: str):
    try:
        date_param_name = (
            exp.unresolved_function.arguments[arg_index]
            .unresolved_function.arguments[0]
            .literal.string
        )
    except (IndexError, AttributeError):
        date_param_name = default_param_name
    return date_param_name


def _raise_error_helper(return_type: DataType, error_class=None):
    from snowflake.snowpark_connect.expression.error_utils import raise_error_helper

    return raise_error_helper(return_type, error_class)


def _divnull(dividend: Column, divisor: Column) -> Column:
    """
    Utility method to perform division with null handling.
    If the divisor is zero, it returns null instead of raising an error.
    Use it instead of snowpark_fn.divnull to avoid performance overhead
    """
    return (
        snowpark_fn.when(divisor == 0, snowpark_fn.lit(None)).otherwise(
            dividend / divisor
        )
        if not global_config.spark_sql_ansi_enabled
        else dividend / divisor
    )


def _to_unix_timestamp(value: Column, fmt: Optional[Column] = None) -> Column:
    timestamp_fn = (
        snowpark_fn.function("to_timestamp")
        if global_config.spark_sql_ansi_enabled
        else snowpark_fn.function("try_to_timestamp")
    )
    timestamp_exp = timestamp_fn(value, fmt) if fmt is not None else timestamp_fn(value)
    seconds_exp = snowpark_fn.date_part("epoch_second", timestamp_exp)
    return snowpark_fn.when(
        snowpark_fn.is_null(value), snowpark_fn.lit(None).cast(LongType())
    ).otherwise(seconds_exp)


def _timestamp_format_sanity_check(ts_value: str, ts_format: str) -> None:
    """
    The number of digits and characters should match the format.
    This is a basic validation to ensure the format matches the string.
    """
    if "yyyyyyy" in ts_format:
        exception = DateTimeException(
            f"Fail to recognize '{ts_format}' pattern in the DateTimeFormatter."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if ts_format == "yy":
        if len(ts_value) != 2:
            exception = DateTimeException(
                f"Fail to parse '{ts_value}' in DateTimeFormatter."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception

    # For parsing, the acceptable fraction length can be [1, the number of contiguous 'S']
    s_contiguous = 0
    char_count = 0
    brackets = 0
    for i in ts_format:
        if i == "S":
            s_contiguous += 1
        if i == "[":
            brackets += 1
        elif i == "]":
            brackets -= 1
        if brackets == 0 and i.isalnum():
            char_count += 1

    if s_contiguous + sum(x.isalnum() for x in ts_value) < char_count:
        exception = DateTimeException(
            f"Fail to parse '{ts_value}' in DateTimeFormatter."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception


def _bounded_long_floor_expr(expr):
    return (
        snowpark_fn.when(expr >= MAX_INT64, snowpark_fn.lit(MAX_INT64))
        .when(expr <= MIN_INT64, snowpark_fn.lit(MIN_INT64))
        .otherwise(snowpark_fn.cast(snowpark_fn.floor(expr), LongType()))
    )


def resolve_to_number_expression(
    function, parsed_value: Column, format: Column, precision: int, scale: int
) -> Column:
    # The structure of the Spark format string must match: [MI|S] [$] [0|9|G|,]* [.|D] [0|9]* [$] [PR|MI|S]
    # Note the grammar above was retrieved from an error message from PySpark, but it is not entirely accurate.
    # - "MI", and "S" may only be used once at the beginning or end of the format string.
    # - "$" may only be used once before all digits in the number format (but after "MI" or "S").
    # - The format string must not be empty, and ther must be at least one "0", or "9" in the format string.
    # PySpark itself checks the format string for validity before it gets to SAS, so we can make the assumption that all
    # of the above are true.
    plus_at_start = parsed_value.startswith("+")
    minus_at_start = parsed_value.startswith("-")
    plus_at_end = parsed_value.endswith("+")
    minus_at_end = parsed_value.endswith("-")

    S_at_start = format.startswith("S")
    S_at_end = format.endswith("S")
    PR_at_end = format.endswith("PR")
    format = snowpark_fn.replace(format, "PR", "")

    # Replace the decimal point with "D" to make regular expressions and replacements easier.
    format = snowpark_fn.replace(format, ".", snowpark_fn.lit("D"))

    decimal_used = format.contains(snowpark_fn.lit("D"))
    # Handle this by splitting the format string at the decimal point.
    split_by_decimal = snowpark_fn.split(format, snowpark_fn.lit("D"))
    before_decimal = snowpark_fn.element_at(split_by_decimal, 0)
    after_decimal = snowpark_fn.element_at(split_by_decimal, 1)
    after_decimal_empty = after_decimal == ""

    # When in decimal part zeros are present try_to_number works incorrectly
    # Replacing 0 with 9 to ensure proper result
    format = snowpark_fn.when(
        decimal_used,
        snowpark_fn.concat(
            before_decimal,
            snowpark_fn.when(after_decimal_empty, snowpark_fn.lit("")).otherwise(
                snowpark_fn.lit("D")
            ),
            snowpark_fn.replace(after_decimal, "0", "9"),
        ),
    ).otherwise(format)

    bracket_at_start = parsed_value.startswith("<")
    bracket_at_end = parsed_value.endswith(">")

    # When sign is provided in format, but input value does not have it Snowflake would return NULL
    # to match Spark behaviour we need to add + if sign is missing
    has_missing_starting_sign = S_at_start & ~plus_at_start & ~minus_at_start
    parsed_value_with_prefix_plus = snowpark_fn.concat(
        snowpark_fn.lit("+"), parsed_value
    )

    has_missing_ending_sign = S_at_end & ~plus_at_end & ~minus_at_end
    parsed_value_with_suffix_plus = snowpark_fn.concat(
        parsed_value, snowpark_fn.lit("+")
    )

    has_sign_in_unsigned_format = ~S_at_start & (plus_at_start | minus_at_start)
    empty_parsed_value = snowpark_fn.lit("")

    is_pr_formatted = PR_at_end & bracket_at_start & bracket_at_end
    parsed_value_with_minus_sign = snowpark_fn.regexp_replace(
        snowpark_fn.regexp_replace(parsed_value, "^<", "-"), ">$"
    )

    return (
        snowpark_fn.when(
            has_missing_starting_sign,
            function(parsed_value_with_prefix_plus, format, precision, scale),
        )
        .when(
            has_missing_ending_sign,
            function(parsed_value_with_suffix_plus, format, precision, scale),
        )
        .when(
            is_pr_formatted,
            function(parsed_value_with_minus_sign, format, precision, scale),
        )
        .when(
            has_sign_in_unsigned_format,
            function(empty_parsed_value, format, precision, scale),
        )
        .otherwise(function(parsed_value, format, precision, scale))
    )


def resolve_to_number_precision_and_scale(
    exp: expressions_proto.Expression,
) -> tuple[int, int]:
    precision = 38
    scale = 0

    _, format = exp.unresolved_function.arguments
    if format.HasField("literal"):
        # Extract precision and scale from the literal string
        str_format = format.literal.string
        _validate_number_format_string(str_format)
        pattern = r"^(.*?)[.D](.*)$"
        matcher = re.match(pattern, str_format)
        precision = len(re.findall("[9|0]", str_format))
        if matcher and len(matcher.groups()) == 2:
            scale = len(re.findall("[9|0]", matcher.group(2)))

    return precision, scale


def _validate_number_format_string(format_str: str) -> None:
    """
    Validates a number format string according to Spark's grammar:
    [MI|S] [$] [0|9|G|,]* [.|D] [0|9]* [$] [PR|MI|S]

    Raises AnalysisException if the format string is invalid.
    """

    def _unexpected_char(char):
        exception = AnalysisException(
            f"[INVALID_FORMAT.UNEXPECTED_TOKEN] The format is invalid: '{original_format}'. "
            f"Found the unexpected character '{char}' in the format string; "
            "the structure of the format string must match: "
            "`[MI|S]` `[$]` `[0|9|G|,]*` `[.|D]` `[0|9]*` `[$]` `[PR|MI|S]`."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    if not format_str:
        exception = AnalysisException(
            "[INVALID_FORMAT.EMPTY] The format is invalid: ''. The number format string cannot be empty."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception

    # Create a working copy of the format string
    remaining = format_str
    original_format = format_str

    # Track if we found required digits
    has_digit = False

    # Check for leading MI or S
    if remaining.startswith("MI"):
        remaining = remaining[2:]
    elif remaining.startswith("S"):
        remaining = remaining[1:]

    # Check for leading $
    if remaining.startswith("$"):
        remaining = remaining[1:]

    # Check for trailing PR, MI, or S and remove them for validation
    if remaining.endswith("PR"):
        remaining = remaining[:-2]
    elif remaining.endswith("MI"):
        remaining = remaining[:-2]
    elif remaining.endswith("S"):
        remaining = remaining[:-1]

    # Check for trailing $
    if remaining.endswith("$"):
        remaining = remaining[:-1]

    # Now validate the core number format part
    # Should be: [0|9|G|,]* [.|D] [0|9]*
    decimal_found = False
    i = 0

    # Process digits before decimal point
    while i < len(remaining):
        char = remaining[i]
        if char in "09":
            has_digit = True
            i += 1
        elif char in "G,":
            i += 1
        elif char in ".D":
            decimal_found = True
            i += 1
            break
        else:
            # Found unexpected character
            _unexpected_char(char)

    # Process digits after decimal point (if decimal was found)
    if decimal_found:
        while i < len(remaining):
            char = remaining[i]
            if char in "09":
                has_digit = True
                i += 1
            else:
                # Found unexpected character after decimal
                _unexpected_char(char)

    # Check if we consumed all characters
    if i < len(remaining):
        char = remaining[i]
        _unexpected_char(char)

    # Check if we found at least one digit
    if not has_digit:
        # Find the first invalid character by scanning the original string
        for char in original_format:
            if char not in "MISPRD$G,.09":
                _unexpected_char(char)

        # If no invalid character found but no digits, it's still invalid
        exception = AnalysisException(
            f"[INVALID_FORMAT.WRONG_NUM_DIGIT] The format is invalid: '{format_str}'. The format string requires at least one number digit."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception


def _trim_helper(value: Column, trim_value: Column, trim_type: Column) -> Column:
    @cached_udf(
        return_type=BinaryType(),
        input_types=[BinaryType(), BinaryType(), StringType()],
    )
    def _binary_trim_udf(value: bytes, trim_value: bytes, trim_type: str) -> bytes:
        if value is None or trim_value is None:
            return value
        if trim_type in ("rtrim", "btrim", "trim"):
            while value.endswith(trim_value):
                value = value[: -len(trim_value)]
        if trim_type in ("ltrim", "btrim", "trim"):
            while value.startswith(trim_value):
                value = value[len(trim_value) :]
        return value

    return _binary_trim_udf(value, trim_value, trim_type)


_SPARK_TZ_MAPPINGS = {
    "ACT": "Australia/Darwin",
    "AET": "Australia/Sydney",
    "AGT": "America/Argentina/Buenos_Aires",
    "ART": "Africa/Cairo",
    "AST": "America/Anchorage",
    "BET": "America/Sao_Paulo",
    "BST": "Asia/Dhaka",
    "CAT": "Africa/Harare",
    "CNT": "America/St_Johns",
    "CST": "America/Chicago",
    "CTT": "Asia/Shanghai",
    "EAT": "Africa/Addis_Ababa",
    "ECT": "Europe/Paris",
    "IET": "America/Indiana/Indianapolis",
    "IST": "Asia/Kolkata",
    "JST": "Asia/Tokyo",
    "MIT": "Pacific/Apia",
    "NET": "Asia/Yerevan",
    "NST": "Pacific/Auckland",
    "PLT": "Asia/Karachi",
    "PNT": "America/Phoenix",
    "PRT": "America/Puerto_Rico",
    "PST": "America/Los_Angeles",
    "SST": "Pacific/Guadalcanal",
    "VST": "Asia/Ho_Chi_Minh",
}


def _map_from_spark_tz(value: Column) -> Column:
    def _local_offset_to_etc_tz(tz: str) -> str:
        if tz is None:
            return None
        offset_match = re.match(r"^([+-])(\d{2}):(\d{2})$", tz)
        if offset_match:
            sign, hours, minutes = offset_match.groups()
            hour_int = int(hours)
            if minutes != "00":
                return tz
            if sign == "+":
                return f"Etc/GMT-{hour_int}" if hour_int > 0 else "Etc/GMT"
            else:
                return f"Etc/GMT+{hour_int}" if hour_int > 0 else "Etc/GMT"
        return tz

    # Optimization: when the timezone argument is a string literal, resolve the
    # mapping at translation time instead of emitting a 25-branch CASE/WHEN.
    if isinstance(value._expression, Literal) and isinstance(
        value._expression.value, str
    ):
        literal_val = value._expression.value
        # 1. Map Java 3-letter abbreviations (e.g. "CST" → "America/Chicago")
        if literal_val in _SPARK_TZ_MAPPINGS:
            return snowpark_fn.lit(_SPARK_TZ_MAPPINGS[literal_val])
        # 2. Handle UTC offset strings (e.g. "+09:00" → "Etc/GMT-9")
        #    Snowflake rejects raw offsets like "+09:00" but accepts "Etc/GMT-N".
        offset_match = re.match(r"^([+-])(\d{2}):(\d{2})$", literal_val)
        if offset_match:
            return snowpark_fn.lit(_local_offset_to_etc_tz(literal_val))
        # 3. IANA name (e.g. "Asia/Seoul") — pass through directly
        elif not literal_val.startswith(("+", "-")):
            return snowpark_fn.lit(literal_val)

    # Fallback for dynamic column values: build the full CASE/WHEN chain so
    # Java timezone abbreviations are mapped correctly at query execution time.
    result = snowpark_fn.when(value.is_null(), snowpark_fn.lit(None))
    for spark_tz, snowflake_tz in _SPARK_TZ_MAPPINGS.items():
        result = result.when(
            value == snowpark_fn.lit(spark_tz), snowpark_fn.lit(snowflake_tz)
        )

    @cached_udf(input_types=[StringType()], return_type=StringType())
    def _convert_offset_tz(tz: str) -> str:
        return _local_offset_to_etc_tz(tz)

    return result.otherwise(_convert_offset_tz(value))


def _calculate_total_months(interval_arg):
    """Calculate total months from a year-month interval."""
    years = snowpark_fn.date_part("year", interval_arg)
    months = snowpark_fn.date_part("month", interval_arg)
    return years * 12 + months


def _calculate_total_days(interval_arg):
    """Calculate total days from a day-time interval."""
    days = snowpark_fn.date_part("day", interval_arg)
    hours = snowpark_fn.date_part("hour", interval_arg)
    minutes = snowpark_fn.date_part("minute", interval_arg)
    seconds = snowpark_fn.date_part("second", interval_arg)
    # Convert hours, minutes, seconds to fractional days
    fractional_days = (hours * 3600 + minutes * 60 + seconds) / 86400
    return days + fractional_days


def _calculate_total_seconds(interval_arg):
    """Calculate total seconds from a day-time interval."""
    days = snowpark_fn.date_part("day", interval_arg)
    hours = snowpark_fn.date_part("hour", interval_arg)
    minutes = snowpark_fn.date_part("minute", interval_arg)
    seconds = snowpark_fn.date_part("second", interval_arg)
    return days * 86400 + hours * 3600 + minutes * 60 + seconds


def _validate_and_get_bitwise_result_type(
    snowpark_typed_args: list[TypedColumn], spark_function_name: str
) -> DataType:
    """
    Validate that both operands are integral types (or null) and determine the result type
    for bitwise operations (&, |, ^) based on Spark's type coercion rules.

    Raises AnalysisException if either operand is not an integral type or null.

    Bitwise operations preserve the input integral type when both operands are the same type,
    and promote to the larger type when operands differ:
    - byte & byte -> byte, int & int -> int, long & long -> long
    - byte & long -> long, short & int -> int
    - integral & null -> integral type (with null result)
    - null & null -> IntegerType (with null result)

    Args:
        snowpark_typed_args: List of two TypedColumn arguments for the bitwise operation
        spark_function_name: The Spark function name for error messages

    Returns:
        The result integral type based on the promotion rules
    """
    type0 = snowpark_typed_args[0].typ
    type1 = snowpark_typed_args[1].typ

    # Check that both operands are either integral or null
    def is_valid_bitwise_type(t):
        return isinstance(t, (_IntegralType, NullType))

    if not (is_valid_bitwise_type(type0) and is_valid_bitwise_type(type1)):
        wrong_type = type0 if not is_valid_bitwise_type(type0) else type1
        exception = AnalysisException(
            f'[DATATYPE_MISMATCH.BINARY_OP_WRONG_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: the binary operator requires the input type "INTEGRAL", not "{wrong_type.simpleString().upper()}".;'
        )
        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
        raise exception

    match (type0, type1):
        case (LongType(), _) | (_, LongType()):
            return LongType()
        case (IntegerType(), _) | (_, IntegerType()):
            return IntegerType()
        case (ShortType(), _) | (_, ShortType()):
            return ShortType()
        case (ByteType(), _) | (_, ByteType()):
            return ByteType()
        case _:
            return IntegerType()


def _evaluate_bit_operation_result_type(
    snowpark_typed_arg_typ: TypedColumn,
    snowpark_arg_name: str,
    return_on_null: DataType,
    spark_function_name: str,
) -> DataType:
    """
    Determine the result type for bit operation aggregate functions (bit_and, bit_or, bit_xor).

    For integral types, the result type matches the input type to maintain Spark compatibility.
    For null type, returns the specified default type. Raises an AnalysisException for non-integral types.

    Args:
        snowpark_typed_arg_typ: The data type of the input argument
        snowpark_arg_name: Name of the argument (for error messages)
        return_on_null: Type to return when input is NullType
        spark_function_name: Name of the function (for error messages)

    Returns:
        The result type based on the input type

    Raises:
        AnalysisException: If the input type is not integral or null
    """
    if isinstance(snowpark_typed_arg_typ, NullType):
        return return_on_null
    elif isinstance(snowpark_typed_arg_typ, _IntegralType):
        return snowpark_typed_arg_typ
    else:
        exception = AnalysisException(
            f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 1 requires the \'INTEGRAL\' type, however "{snowpark_arg_name}" has the type "{snowpark_typed_arg_typ.simpleString().upper()}".'
        )
        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
        raise exception
