#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import datetime
import functools
import math
import operator
import random
import re
import string
import sys
import time
import uuid
from collections import defaultdict
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Context, Decimal
from functools import reduce
from typing import List, Optional
from urllib.parse import quote

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
from snowflake.snowpark._internal.analyzer.expression import Literal
from snowflake.snowpark._internal.analyzer.unary_expression import Alias
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
    is_aggregate_string_coercion_enabled,
    is_complex_type_nullability_enabled,
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
    cast_force_nullable,
    cast_nullable,
    map_cast,
    timestamp_to_spark_string,
    wider_decimal_type,
)
from snowflake.snowpark_connect.expression.map_extension import (
    _tag_in_subquery_sql,
    get_in_subquery_sql,
)
from snowflake.snowpark_connect.expression.map_unresolved_star import (
    map_unresolved_star_as_single_column,
    map_unresolved_star_struct,
)
from snowflake.snowpark_connect.expression.typer import (
    ExpressionTyper,
    LambdaExpressionTyper,
)
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
from snowflake.snowpark_connect.type_support import integral_to_decimal
from snowflake.snowpark_connect.typed_column import (
    FieldType,
    SelectedProjectionSpec,
    TypedColumn,
    TypedColumnWithDeferredCast,
    TypedColumnWithDeferredWindowBuilder,
)
from snowflake.snowpark_connect.utils.context import (
    add_sql_aggregate_function,
    get_current_grouping_columns,
    get_current_plan_id,
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
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.spark_session_cache import get_spark_session_cache
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
from snowflake.snowpark_connect.utils.xxhash64 import DEFAULT_SEED

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


def _unary_nullable(typed_args: list[TypedColumn]) -> bool:
    """Returns nullable status of first argument. Propagates nullability for unary functions."""
    return typed_args[0].nullable


def _binary_nullable(typed_args: list[TypedColumn]) -> bool:
    return typed_args[0].nullable or typed_args[1].nullable


def _any_arg_nullable(typed_args: list[TypedColumn]) -> bool:
    return any(a.nullable for a in typed_args)


def _all_args_nullable(typed_args: list[TypedColumn]) -> bool:
    return all(a.nullable for a in typed_args)


def _inner_nullable(val: bool) -> bool:
    """Guard inner nullability of complex types based on config.

    When ``snowpark.connect.nullability.trackComplexTypes`` is off (default),
    always returns True to prevent NOT NULL in generated SQL.
    When on, returns the actual computed value.
    """
    return val if is_complex_type_nullability_enabled() else True


def _is_nan_value(value) -> bool:
    try:
        return math.isnan(float(value))
    except (TypeError, ValueError, OverflowError):
        return False


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
) -> tuple[Column, Column, bool]:
    """Coerce left/right for comparison, returning final nullable flag.

    The returned nullable accounts for both the original argument nullability
    and any forced nullability introduced by the implicit coercion cast.
    """
    arg_nullable = _binary_nullable([left, right])

    if left.typ == right.typ:
        return left.col, right.col, arg_nullable

    # To avoid handling both (A, B) and (B, A), swap them in the second case, then swap back at the end.
    if type(left.typ).__name__ > type(right.typ).__name__:
        left, right = right, left
        swap = True
    else:
        swap = False

    left_col = left.col
    right_col = right.col
    left_target = left.typ
    right_target = right.typ

    match (left.typ, right.typ):
        case (BooleanType(), IntegerType()):
            left_col = left_col.cast(LongType())
            left_target = LongType()
        case (BooleanType(), LongType()):
            left_col = left_col.cast(LongType())
            left_target = LongType()
        case (BooleanType(), FloatType()):
            left_col = left_col.cast(IntegerType()).cast(FloatType())
            left_target = FloatType()
        case (BooleanType(), DoubleType()):
            left_col = left_col.cast(IntegerType()).cast(DoubleType())
            left_target = DoubleType()
        case (BooleanType(), StringType()):
            right_col = right_col.try_cast(BooleanType())
            right_target = BooleanType()
        case (_IntegralType(), StringType()):
            if global_config.spark_sql_ansi_enabled:
                right_col = right_col.cast(LongType())
                right_target = LongType()
            else:
                right_col = right_col.try_cast(type(left.typ)())
                right_target = type(left.typ)()
        case (FloatType(), StringType()):
            right_col = right_col.try_cast(FloatType())
            right_target = FloatType()
        case (DoubleType(), StringType()):
            right_col = right_col.try_cast(DoubleType())
            right_target = DoubleType()
        case (DecimalType(), StringType()):
            right_col = right_col.try_cast(DoubleType())
            right_target = DoubleType()
        case (BinaryType(), StringType()):
            # Convert binary to string for comparison
            left_col = snowpark_fn.to_varchar(left_col, "UTF-8")
            left_target = StringType()
        case (StringType(), BinaryType()):
            # Convert binary to string for comparison
            right_col = snowpark_fn.to_varchar(right_col, "UTF-8")
            right_target = StringType()
        case (DateType(), StringType()):
            right_target = DateType()
        case (StringType(), TimestampType()):
            left_target = TimestampType()
        case (ByteType(), DecimalType()):
            left_target = right_target = wider_decimal_type(
                integral_to_decimal(left.typ), right.typ
            )
        case (DecimalType(), IntegerType() | LongType() | ShortType()):
            left_target = right_target = wider_decimal_type(
                left.typ, integral_to_decimal(right.typ)
            )

    force_nullability = cast_force_nullable(
        left.typ, left_target
    ) or cast_force_nullable(right.typ, right_target)
    nullable = arg_nullable or force_nullability

    if swap:
        return right_col, left_col, nullable
    else:
        return left_col, right_col, nullable


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


def _has_unsupported_pcre_syntax(pattern_col: snowpark.Column) -> bool:
    """Check if a literal pattern uses PCRE features unsupported by Snowflake."""
    try:
        pattern_str = str(pattern_col._expression.value)
    except (AttributeError, TypeError):
        return False

    if any(x in pattern_str for x in ("(?=", "(?!", "(?<=", "(?<!")):
        return True

    import re as re_mod

    for m in re_mod.finditer(r"\(\?[ismx-]+[):]", pattern_str):
        if m.start() > 0:
            return True

    return False


def _validate_regex_group_index(
    string_col: snowpark.Column,
    pattern_col: snowpark.Column,
    idx_col: snowpark.Column,
    func_name: str,
) -> None:
    """Eagerly validate the regex group index when string, pattern, and idx are all literals.

    Spark constant-folds literal expressions during analysis, so regexp_extract('abc','b',2)
    throws at spark.sql() time.  When the string doesn't match the pattern at all, Spark
    returns empty (no error), so we must check that the match succeeds before raising.
    """
    if not isinstance(idx_col._expression, Literal):
        return
    if not isinstance(pattern_col._expression, Literal):
        return
    if not isinstance(string_col._expression, Literal):
        return
    idx_value = idx_col._expression.value
    pattern_value = str(pattern_col._expression.value)
    string_value = str(string_col._expression.value)
    try:
        compiled = re.compile(pattern_value)
    except re.error:
        return
    num_groups = compiled.groups
    if idx_value < 0 or idx_value > num_groups:
        if compiled.search(string_value):
            raise AnalysisException(
                f"[INVALID_PARAMETER_VALUE.REGEX_GROUP_INDEX] The value of parameter(s) `idx` in `{func_name}` is invalid:"
                f" Expects group index between 0 and {num_groups}, but got {idx_value}."
            )


def _extract_inline_regex_flags(
    pattern_col: snowpark.Column,
) -> tuple[snowpark.Column, str | None]:
    """Extract inline regex flags from a literal pattern, returning stripped pattern and Snowflake flags."""
    try:
        pattern_str = str(pattern_col._expression.value)
    except (AttributeError, TypeError):
        return pattern_col, None

    import re as re_mod

    m = re_mod.match(r"^\(\?(-?[a-zA-Z]+)\)", pattern_str)
    if not m:
        return pattern_col, None

    flags_text = m.group(1)
    remaining = pattern_str[m.end() :]

    sf_flags = ""
    negate = False
    for ch in flags_text:
        if ch == "-":
            negate = True
        elif ch == "i":
            sf_flags += "c" if negate else "i"
            negate = False
        elif ch in ("s", "m", "x"):
            if not negate:
                sf_flags += ch
            negate = False
        else:
            return pattern_col, None

    return snowpark_fn.lit(remaining), sf_flags or None


def map_unresolved_function(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[list[str], TypedColumn]:
    from snowflake.snowpark_connect.expression.map_expression import (
        extract_alias_from_resolved_name,
        map_expression,
    )

    telemetry.report_function_usage(exp.unresolved_function.function_name.lower())

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
    cache = get_spark_session_cache()
    is_udtf_call = cache.udtfs.has(function_name)

    # Inject default parameters for functions that need them (especially for Scala clients)
    inject_function_defaults(exp.unresolved_function)

    # Transform NOT(col = col) to col != col for Snowflake compatibility
    function_name = _preprocess_not_equals_expression(exp)

    arg_alias_names: dict[int, str] = {}

    def _resolve_args_expressions(exp: expressions_proto.Expression):
        def _resolve_fn_arg(exp):
            with resolving_fun_args():
                return map_expression(exp, column_mapping, typer)

        def _unalias_column(
            index: int, names: list[str], tc: TypedColumn
        ) -> TypedColumn:
            if hasattr(tc.col, "_expression"):
                col_exp = tc.col._expression
                if isinstance(col_exp, Alias):
                    if len(names) == 1:
                        alias = extract_alias_from_resolved_name(names[0])
                        if alias is not None:
                            arg_alias_names[index] = alias
                    return TypedColumn(Column(col_exp.child), lambda: tc.field_types)
            return tc

        resolved = [_resolve_fn_arg(arg) for arg in exp.unresolved_function.arguments]
        resolved_without_alias = [
            (names, _unalias_column(i, names, tc))
            for i, (names, tc) in enumerate(resolved)
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
    aggregate_string_coercion_enabled = is_aggregate_string_coercion_enabled()
    spark_sql_legacy_allow_hash_on_map_type = (
        global_config.spark_sql_legacy_allowHashOnMapType
    )

    function_name = exp.unresolved_function.function_name.lower()
    result_type: Optional[DataType | List[DateType]] = None
    selected_projection_specs: list[SelectedProjectionSpec] | None = None
    qualifier_parts: List[str] = []

    # Check if this is an aggregate function (used by GROUP BY ALL implementation)
    if is_aggregate_function(function_name):
        add_sql_aggregate_function()

    def _type_with_typer(col: Column, force_nullable: bool = False) -> TypedColumn:
        """If you can, avoid using this function. Typer most likely has to call GS to resovle type which is expensive."""
        if force_nullable:
            return TypedColumn(
                col,
                lambda: [FieldType(ft.datatype, True) for ft in typer.type(col)],
            )
        return TypedColumn(col, lambda: typer.type(col))

    def _resolve_aggregate_exp(
        result_exp: Column, default_result_type: DataType, nullable: bool = True
    ) -> TypedColumn:
        ft = FieldType(default_result_type, nullable)
        if is_window_enabled():
            return TypedColumnWithDeferredCast(result_exp, lambda f=ft: [f])
        else:
            return TypedColumn(
                snowpark_fn.cast(result_exp, default_result_type),
                lambda f=ft: [f],
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
        # this function is used only for min/max where Spark's output nullable is always True
        result_ft = [FieldType(typed_arg.typ, nullable=True)]
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

            return TypedColumn(result.cast(typed_arg.typ), lambda f=result_ft: f)
        else:
            # No structured type conversion needed
            result = aggregate_func(typed_arg.col)
            return TypedColumn(result, lambda f=result_ft: f)

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
        case func_name if cache.udfs.has(func_name.lower()):
            udf = cache.udfs.get(func_name.lower())
            # The UDF handle owns the full marshalling round-trip; same path the inline
            # call site (map_udf) uses. Returns a TypedColumn, normalized below.
            result_exp = udf.invoke(
                snowpark_typed_args, column_mapping, get_or_create_snowpark_session()
            )
        case func_name if (
            get_is_evaluating_sql() and cache.udtfs.has(func_name.lower())
        ):
            udtf, spark_col_names = cache.udtfs.get(func_name.lower())
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
            left, right, nullable = _coerce_for_comparison(
                snowpark_typed_args[0], snowpark_typed_args[1]
            )
            result_exp = TypedColumn(
                left != right, lambda n=nullable: [FieldType(BooleanType(), n)]
            )
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
                        result_col = apply_arithmetic_overflow_with_ansi_check(
                            raw_result, result_type, spark_sql_ansi_enabled, "multiply"
                        )
                    else:
                        result_col = snowpark_args[0].cast(result_type) * snowpark_args[
                            1
                        ].cast(result_type)
                    mul_nullable = (
                        snowpark_typed_args[0].nullable
                        or snowpark_typed_args[1].nullable
                    )
                    mul_ft = FieldType(result_type, mul_nullable)
                    result_exp = TypedColumn(result_col, lambda f=mul_ft: [f])
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
            add_bn = _binary_nullable(snowpark_typed_args)
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (TimestampType(), NullType()) | (NullType(), TimestampType()):
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.BINARY_OP_DIFF_TYPES] Cannot resolve "{spark_function_name}" due to data type mismatch: the left and right operands of the binary operator have incompatible types ("{snowpark_typed_args[0].typ}" and "{snowpark_typed_args[1].typ}").'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                case (DateType(), NullType()) | (NullType(), DateType()):
                    result_type = FieldType(DateType(), add_bn)
                    result_exp = snowpark_fn.lit(None).cast(DateType())
                case (NullType(), _) | (_, NullType()):
                    add_dt, _ = _get_add_sub_result_type(
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
                    result_type = FieldType(add_dt, add_bn)
                    result_exp = snowpark_args[0] + snowpark_args[1]
                    result_exp = result_exp.cast(add_dt)
                case (DateType(), t) | (t, DateType()):
                    date_param_index = (
                        0 if isinstance(snowpark_typed_args[0].typ, DateType) else 1
                    )
                    t_param_index = 1 - date_param_index
                    if isinstance(t, (IntegerType, ShortType, ByteType)):
                        result_type = FieldType(DateType(), add_bn)
                        result_exp = snowpark_args[0] + snowpark_args[1]
                    elif isinstance(t, (DayTimeIntervalType, YearMonthIntervalType)):
                        add_date_dt = (
                            TimestampType()
                            if isinstance(
                                snowpark_typed_args[t_param_index].typ,
                                DayTimeIntervalType,
                            )
                            else DateType()
                        )
                        result_type = FieldType(add_date_dt, add_bn)
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
                        result_type = FieldType(TimestampType(), add_bn)
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
                        result_type = FieldType(TimestampType(), add_bn)
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
                        result_type = FieldType(TimestampType(), add_bn)
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
                        add_ss_dt = DoubleType()
                        add_ss_bn = add_bn or cast_force_nullable(
                            StringType(), add_ss_dt
                        )
                        result_type = FieldType(add_ss_dt, add_ss_bn)
                        result_exp = snowpark_fn.try_cast(
                            snowpark_args[0], add_ss_dt
                        ) + snowpark_fn.try_cast(snowpark_args[1], add_ss_dt)
                case (StringType(), _NumericType() as t):
                    if spark_sql_ansi_enabled:
                        add_sn_dt = (
                            DoubleType()
                            if isinstance(t, _FractionalType)
                            else LongType()
                        )
                        add_sn_bn = add_bn or cast_force_nullable(
                            StringType(), add_sn_dt
                        )
                        result_type = FieldType(add_sn_dt, add_sn_bn)
                        result_exp = snowpark_args[0].cast(add_sn_dt) + snowpark_args[1]
                    else:
                        add_sn_dt = DoubleType()
                        add_sn_bn = add_bn or cast_force_nullable(
                            StringType(), add_sn_dt
                        )
                        result_type = FieldType(add_sn_dt, add_sn_bn)
                        result_exp = (
                            snowpark_fn.try_cast(snowpark_args[0], add_sn_dt)
                            + snowpark_args[1]
                        )
                case (_NumericType() as t, StringType()):
                    if spark_sql_ansi_enabled:
                        add_ns_dt = (
                            DoubleType()
                            if isinstance(t, _FractionalType)
                            else LongType()
                        )
                        add_ns_bn = add_bn or cast_force_nullable(
                            StringType(), add_ns_dt
                        )
                        result_type = FieldType(add_ns_dt, add_ns_bn)
                        result_exp = snowpark_args[0] + snowpark_args[1].cast(add_ns_dt)
                    else:
                        add_ns_dt = DoubleType()
                        add_ns_bn = add_bn or cast_force_nullable(
                            StringType(), add_ns_dt
                        )
                        result_type = FieldType(add_ns_dt, add_ns_bn)
                        result_exp = snowpark_args[0] + snowpark_fn.try_cast(
                            snowpark_args[1], add_ns_dt
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
                    add_intv_dt = type(t1)(
                        min(t1.start_field, t2.start_field),
                        max(t1.end_field, t2.end_field),
                    )
                    result_type = FieldType(add_intv_dt, add_bn)
                    result_exp = snowpark_args[0] + snowpark_args[1]
                case (StringType(), t) | (t, StringType()) if isinstance(
                    t, YearMonthIntervalType
                ):
                    # String + YearMonthInterval: Spark tries to cast string to double first, throws error if it fails
                    result_type = FieldType(StringType(), add_bn)
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
                    result_type = FieldType(StringType(), add_bn)
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
            sub_bn = _binary_nullable(snowpark_typed_args)
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (TimestampType(), NullType()) | (NullType(), TimestampType()):
                    sub_ts_dt = DayTimeIntervalType(
                        DayTimeIntervalType.DAY, DayTimeIntervalType.SECOND
                    )
                    result_type = FieldType(sub_ts_dt, sub_bn)
                    result_exp = snowpark_fn.lit(None).cast(sub_ts_dt)
                case (DateType(), NullType()) | (NullType(), DateType()):
                    result_type = FieldType(DateType(), sub_bn)
                    result_exp = snowpark_fn.lit(None).cast(DateType())
                case (NullType(), _) | (_, NullType()):
                    sub_null_dt, _ = _get_add_sub_result_type(
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
                    result_type = FieldType(sub_null_dt, sub_bn)
                    result_exp = snowpark_args[0] - snowpark_args[1]
                    result_exp = result_exp.cast(sub_null_dt)
                case (DateType(), DateType()):
                    sub_dd_dt = DayTimeIntervalType(
                        DayTimeIntervalType.DAY, DayTimeIntervalType.DAY
                    )
                    result_type = FieldType(sub_dd_dt, sub_bn)
                    result_exp = snowpark_fn.interval_day_time_from_parts(
                        snowpark_args[0] - snowpark_args[1]
                    )
                case (DateType(), DayTimeIntervalType()) | (
                    DateType(),
                    YearMonthIntervalType(),
                ):
                    sub_di_dt = (
                        TimestampType()
                        if isinstance(snowpark_typed_args[1].typ, DayTimeIntervalType)
                        else DateType()
                    )
                    result_type = FieldType(sub_di_dt, sub_bn)
                    result_exp = snowpark_args[0] - snowpark_args[1]
                case (DateType(), StringType()):
                    if (
                        hasattr(snowpark_typed_args[1].col._expr1, "pretty_name")
                        and "INTERVAL" == snowpark_typed_args[1].col._expr1.pretty_name
                    ):
                        result_type = FieldType(TimestampType(), sub_bn)
                        result_exp = snowpark_args[0] - snowpark_args[1]
                    else:
                        input_type = (
                            DateType() if spark_sql_ansi_enabled else DoubleType()
                        )
                        if isinstance(input_type, DateType):
                            sub_ds_dt = DayTimeIntervalType(
                                DayTimeIntervalType.DAY, DayTimeIntervalType.DAY
                            )
                            result_type = FieldType(sub_ds_dt, sub_bn)
                            result_exp = snowpark_fn.interval_day_time_from_parts(
                                snowpark_args[0] - snowpark_args[1].cast(input_type)
                            )
                        else:
                            result_type = FieldType(LongType(), sub_bn)
                            result_exp = snowpark_args[0] - snowpark_args[1].cast(
                                input_type
                            )
                case (TimestampType(), DayTimeIntervalType()) | (
                    TimestampType(),
                    YearMonthIntervalType(),
                ):
                    result_type = FieldType(TimestampType(), sub_bn)
                    result_exp = snowpark_args[0] - snowpark_args[1]
                case (TimestampType(), StringType()):
                    if (
                        hasattr(snowpark_typed_args[1].col._expr1, "pretty_name")
                        and "INTERVAL" == snowpark_typed_args[1].col._expr1.pretty_name
                    ):
                        result_type = FieldType(TimestampType(), sub_bn)
                        result_exp = snowpark_args[0] - snowpark_args[1]
                    else:
                        raise AnalysisException(
                            f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 2 requires the ("INTERVAL") type for timestamp operations, however "{snowpark_arg_names[1]}" has the type "{snowpark_typed_args[1].typ}".',
                        )
                case (StringType(), DateType()):
                    sub_sd_dt = DayTimeIntervalType(
                        DayTimeIntervalType.DAY, DayTimeIntervalType.DAY
                    )
                    result_type = FieldType(sub_sd_dt, sub_bn)
                    result_exp = snowpark_fn.interval_day_time_from_parts(
                        snowpark_args[0].cast(DateType()) - snowpark_args[1]
                    )
                case (DateType(), (IntegerType() | ShortType() | ByteType())):
                    result_type = FieldType(DateType(), sub_bn)
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
                        sub_ss_dt = DoubleType()
                        sub_ss_bn = sub_bn or cast_force_nullable(
                            StringType(), sub_ss_dt
                        )
                        result_type = FieldType(sub_ss_dt, sub_ss_bn)
                        result_exp = snowpark_fn.try_cast(
                            snowpark_args[0], sub_ss_dt
                        ) - snowpark_fn.try_cast(snowpark_args[1], sub_ss_dt)
                case (StringType(), _NumericType() as t):
                    if spark_sql_ansi_enabled:
                        sub_sn_dt = (
                            DoubleType()
                            if isinstance(t, _FractionalType)
                            else LongType()
                        )
                        sub_sn_bn = sub_bn or cast_force_nullable(
                            StringType(), sub_sn_dt
                        )
                        result_type = FieldType(sub_sn_dt, sub_sn_bn)
                        result_exp = snowpark_args[0].cast(sub_sn_dt) - snowpark_args[1]
                    else:
                        sub_sn_dt = DoubleType()
                        sub_sn_bn = sub_bn or cast_force_nullable(
                            StringType(), sub_sn_dt
                        )
                        result_type = FieldType(sub_sn_dt, sub_sn_bn)
                        result_exp = (
                            snowpark_fn.try_cast(snowpark_args[0], sub_sn_dt)
                            - snowpark_args[1]
                        )
                case (_NumericType() as t, StringType()):
                    if spark_sql_ansi_enabled:
                        sub_ns_dt = (
                            DoubleType()
                            if isinstance(t, _FractionalType)
                            else LongType()
                        )
                        sub_ns_bn = sub_bn or cast_force_nullable(
                            StringType(), sub_ns_dt
                        )
                        result_type = FieldType(sub_ns_dt, sub_ns_bn)
                        result_exp = snowpark_args[0] - snowpark_args[1].cast(sub_ns_dt)
                    else:
                        sub_ns_dt = DoubleType()
                        sub_ns_bn = sub_bn or cast_force_nullable(
                            StringType(), sub_ns_dt
                        )
                        result_type = FieldType(sub_ns_dt, sub_ns_bn)
                        result_exp = snowpark_args[0] - snowpark_fn.try_cast(
                            snowpark_args[1], sub_ns_dt
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
                    result_type = FieldType(StringType(), sub_bn)
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
                lambda: snowpark_typed_args[0].field_types,
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
                nullable = _binary_nullable(snowpark_typed_args)
                result_exp = TypedColumn(
                    _struct_comparison(
                        snowpark_typed_args[0], snowpark_typed_args[1], "<"
                    ),
                    lambda n=nullable: [FieldType(BooleanType(), n)],
                )
            else:
                # Check for interval-string comparisons
                _check_interval_string_comparison(
                    "<", snowpark_typed_args, snowpark_arg_names
                )
                left, right, nullable = _coerce_for_comparison(
                    snowpark_typed_args[0], snowpark_typed_args[1]
                )
                result_exp = TypedColumn(
                    left < right, lambda n=nullable: [FieldType(BooleanType(), n)]
                )
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
                nullable = _binary_nullable(snowpark_typed_args)
                result_exp = TypedColumn(
                    _struct_comparison(
                        snowpark_typed_args[0], snowpark_typed_args[1], "<="
                    ),
                    lambda n=nullable: [FieldType(BooleanType(), n)],
                )
            else:
                # Check for interval-string comparisons
                _check_interval_string_comparison(
                    "<=", snowpark_typed_args, snowpark_arg_names
                )
                left, right, nullable = _coerce_for_comparison(
                    snowpark_typed_args[0], snowpark_typed_args[1]
                )
                result_exp = TypedColumn(
                    left <= right, lambda n=nullable: [FieldType(BooleanType(), n)]
                )
        case "<=>":
            # eqNullSafe
            rarg_name = snowpark_arg_names[1]
            typ = snowpark_typed_args[1].typ
            if typ == DoubleType() or typ == FloatType():
                if rarg_name == "nan":
                    rarg_name = "NaN"

            spark_function_name = f"({snowpark_arg_names[0]} <=> {rarg_name})"
            left, right, _nullable = _coerce_for_comparison(
                snowpark_typed_args[0], snowpark_typed_args[1]
            )
            result_exp = TypedColumn(
                left.eqNullSafe(right),
                lambda: [FieldType(BooleanType(), nullable=False)],
            )
        case "==" | "=":
            # Check for interval-string comparisons
            _check_interval_string_comparison(
                "=", snowpark_typed_args, snowpark_arg_names
            )
            spark_function_name = f"({snowpark_arg_names[0]} = {snowpark_arg_names[1]})"
            left, right, nullable = _coerce_for_comparison(
                snowpark_typed_args[0], snowpark_typed_args[1]
            )
            result_exp = TypedColumn(
                left == right, lambda n=nullable: [FieldType(BooleanType(), n)]
            )
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
                nullable = _binary_nullable(snowpark_typed_args)
                result_exp = TypedColumn(
                    _struct_comparison(
                        snowpark_typed_args[0], snowpark_typed_args[1], ">"
                    ),
                    lambda n=nullable: [FieldType(BooleanType(), n)],
                )
            else:
                # Check for interval-string comparisons
                _check_interval_string_comparison(
                    ">", snowpark_typed_args, snowpark_arg_names
                )
                left, right, nullable = _coerce_for_comparison(
                    snowpark_typed_args[0], snowpark_typed_args[1]
                )
                result_exp = TypedColumn(
                    left > right, lambda n=nullable: [FieldType(BooleanType(), n)]
                )
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
                nullable = _binary_nullable(snowpark_typed_args)
                result_exp = TypedColumn(
                    _struct_comparison(
                        snowpark_typed_args[0], snowpark_typed_args[1], ">="
                    ),
                    lambda n=nullable: [FieldType(BooleanType(), n)],
                )
            else:
                # Check for interval-string comparisons
                _check_interval_string_comparison(
                    ">=", snowpark_typed_args, snowpark_arg_names
                )
                left, right, nullable = _coerce_for_comparison(
                    snowpark_typed_args[0], snowpark_typed_args[1]
                )
                result_exp = TypedColumn(
                    left >= right, lambda n=nullable: [FieldType(BooleanType(), n)]
                )
        case "&":
            spark_function_name = f"({snowpark_arg_names[0]} & {snowpark_arg_names[1]})"
            result_type = FieldType(
                _validate_and_get_bitwise_result_type(
                    snowpark_typed_args, spark_function_name
                ),
                _binary_nullable(snowpark_typed_args),
            )
            result_exp = snowpark_args[0].bitwiseAnd(snowpark_args[1])
            result_exp = snowpark_fn.cast(result_exp, result_type.datatype)
        case "|":
            spark_function_name = f"({snowpark_arg_names[0]} | {snowpark_arg_names[1]})"
            result_type = FieldType(
                _validate_and_get_bitwise_result_type(
                    snowpark_typed_args, spark_function_name
                ),
                _binary_nullable(snowpark_typed_args),
            )
            result_exp = snowpark_args[0].bitwiseOR(snowpark_args[1])
        case "^":
            spark_function_name = f"({snowpark_arg_names[0]} ^ {snowpark_arg_names[1]})"
            result_type = FieldType(
                _validate_and_get_bitwise_result_type(
                    snowpark_typed_args, spark_function_name
                ),
                _binary_nullable(snowpark_typed_args),
            )
            result_exp = snowpark_args[0].bitwiseXOR(snowpark_args[1])
        case "abs":
            input_type = snowpark_typed_args[0].typ
            nullable = _unary_nullable(snowpark_typed_args)
            if isinstance(input_type, StringType):
                # SNOW-3585745: match Spark's string->double coercion (TRY_CAST
                # in non-ANSI so malformed input becomes NULL instead of raising
                # Snowflake error 100038).
                result_exp = snowpark_fn.abs(
                    _coerce_string_input_to_double(
                        snowpark_args[0],
                        spark_sql_ansi_enabled,
                        aggregate_string_coercion_enabled,
                    )
                )
                result_type = FieldType(DoubleType(), nullable)
            elif isinstance(input_type, _IntegralType):
                result_exp = apply_abs_overflow_with_ansi_check(
                    snowpark_args[0], input_type, spark_sql_ansi_enabled
                )
                result_type = FieldType(input_type, nullable)
            else:
                result_exp = snowpark_fn.abs(snowpark_args[0])
                result_type = FieldType(input_type, nullable)
        case "acos":
            spark_function_name = f"ACOS({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.when(
                    (snowpark_args[0] < -1) | (snowpark_args[0] > 1), NAN
                ).otherwise(snowpark_fn.acos(snowpark_args[0])),
                lambda: [FieldType(DoubleType(), nullable=True)],
            )
        case "acosh":
            spark_function_name = f"ACOSH({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.when((snowpark_args[0] < 1), NAN).otherwise(
                    snowpark_fn.acosh(snowpark_args[0])
                ),
                lambda: [FieldType(DoubleType(), nullable=True)],
            )
        case "add_months":
            bn = _binary_nullable(snowpark_typed_args)
            result_exp = TypedColumn(
                _try_to_cast(
                    "try_to_date",
                    _spark_add_months(
                        snowpark_fn.to_date(snowpark_args[0]), snowpark_args[1]
                    ),
                    snowpark_args[0],
                ),
                lambda n=bn: [FieldType(DateType(), n)],
            )
        case "aes_decrypt":
            if global_config.snowpark_connect_enable_aes_raw_functions:
                decrypt_exp = _aes_decrypt_raw_helper(
                    "DECRYPT_RAW",
                    snowpark_args[0],
                    snowpark_args[1],
                    snowpark_typed_args[1].typ,
                    snowpark_args[4],
                    snowpark_typed_args[4].typ,
                    snowpark_args[2],
                    snowpark_args[3],
                )
            else:
                decrypt_exp = _aes_helper(
                    "DECRYPT",
                    snowpark_args[0],
                    snowpark_args[1],
                    snowpark_args[4],
                    snowpark_args[2],
                    snowpark_args[3],
                )
            result_exp = TypedColumn(
                decrypt_exp,
                lambda: [FieldType(BinaryType(), nullable=True)],
            )
        case "aes_encrypt":
            if global_config.snowpark_connect_enable_aes_raw_functions:
                encrypt_exp = _aes_encrypt_raw_helper(
                    snowpark_args[0],
                    snowpark_typed_args[0].typ,
                    snowpark_args[1],
                    snowpark_typed_args[1].typ,
                    snowpark_args[5],
                    snowpark_typed_args[5].typ,
                    snowpark_args[2],
                    snowpark_args[3],
                    snowpark_args[4],
                    snowpark_typed_args[4].typ,
                )
            else:
                encrypt_exp = _aes_helper(
                    "ENCRYPT",
                    snowpark_args[0],
                    snowpark_args[1],
                    snowpark_args[5],
                    snowpark_args[2],
                    snowpark_args[3],
                )
            result_exp = TypedColumn(
                encrypt_exp,
                lambda: [FieldType(BinaryType(), nullable=True)],
            )
        case "and":
            spark_function_name = (
                f"({snowpark_arg_names[0]} AND {snowpark_arg_names[1]})"
            )
            bn = _binary_nullable(snowpark_typed_args)
            result_exp = TypedColumn(
                snowpark_args[0] & snowpark_args[1],
                lambda n=bn: [FieldType(BooleanType(), n)],
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
                lambda: [FieldType(BooleanType(), nullable=True)],
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(snowpark_typed_args[0].typ, nullable=True)],
            )
        case "approx_count_distinct":
            match snowpark_args:
                case [data]:
                    result_exp = TypedColumn(
                        snowpark_fn.approx_count_distinct(data),
                        lambda: [FieldType(LongType(), nullable=False)],
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

            def _pyspark_approx_percentile(
                column: Column, percentage: float, is_distinct: bool
            ) -> Column:
                """
                PySpark-compatible discrete percentile.
                Uses PERCENTILE_DISC (returns actual dataset values, not interpolated)
                to match PySpark's approx_percentile semantics.
                For DISTINCT: PERCENTILE_DISC doesn't support DISTINCT, so we collect
                distinct values via ARRAY_UNIQUE_AGG, sort, and index at the
                percentile position.
                """
                if not 0.0 <= percentage <= 1.0:
                    exception = AnalysisException(
                        "percentage must be between [0.0, 1.0]"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception

                if is_distinct:
                    distinct_sorted = snowpark_fn.array_sort(
                        snowpark_fn.array_unique_agg(column)
                    )
                    n = snowpark_fn.array_size(distinct_sorted)
                    idx = snowpark_fn.greatest(
                        snowpark_fn.ceil(snowpark_fn.lit(percentage) * n)
                        - snowpark_fn.lit(1),
                        snowpark_fn.lit(0),
                    )
                    return snowpark_fn.get(distinct_sorted, idx)

                return snowpark_fn.function("percentile_disc")(
                    snowpark_fn.lit(percentage)
                ).within_group(column)

            column_type = snowpark_typed_args[0].typ
            is_distinct = exp.unresolved_function.is_distinct

            if isinstance(snowpark_typed_args[1].typ, ArrayType):
                percentile_values = _unwrap_array_literals(
                    exp.unresolved_function.arguments[1]
                )
                percentile_results = [
                    _pyspark_approx_percentile(snowpark_args[0], p, is_distinct)
                    for p in percentile_values
                ]
                result_type = ArrayType(
                    element_type=column_type,
                    contains_null=_inner_nullable(False),
                )
                result_exp = snowpark_fn.array_construct(*percentile_results)
                result_exp = _resolve_aggregate_exp(
                    result_exp, result_type, nullable=True
                )
            else:
                percentage = unwrap_literal(exp.unresolved_function.arguments[1])
                result_exp = _pyspark_approx_percentile(
                    snowpark_args[0], percentage, is_distinct
                )
                result_exp = _resolve_aggregate_exp(
                    result_exp, column_type, nullable=True
                )
            if is_distinct:
                spark_function_name = spark_function_name.replace(
                    f"{exp.unresolved_function.function_name}(",
                    f"{exp.unresolved_function.function_name}(DISTINCT ",
                    1,
                )
        case "array":
            if len(snowpark_args) == 0:
                result_exp = snowpark_fn.cast(
                    snowpark_fn.array_construct(), ArrayType(NullType())
                )
                result_type = FieldType(ArrayType(NullType()), nullable=False)
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
                element_contains_null = any(
                    ft.nullable for tc in snowpark_typed_args for ft in tc.field_types
                )
                result_exp = snowpark_fn.array_construct(*coerced_args)
                arr_type = ArrayType(
                    element_type,
                    contains_null=_inner_nullable(element_contains_null),
                )
                result_exp = TypedColumn(
                    snowpark_fn.cast(result_exp, arr_type),
                    lambda arr_type=arr_type: [FieldType(arr_type, nullable=False)],
                )
        case "array_append":
            arr_arg, elem_arg, result_arr_type = _coerce_array_and_element(
                snowpark_args[0],
                snowpark_typed_args[0].typ,
                snowpark_args[1],
                snowpark_typed_args[1].typ,
            )
            result_exp = TypedColumn(
                snowpark_fn.array_append(arr_arg, elem_arg),
                lambda: [result_arr_type],
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

            contains_null = (
                isinstance(array_type, ArrayType) and array_type.contains_null
            )
            ac_nullable = _binary_nullable(snowpark_typed_args) or contains_null
            result_exp = TypedColumn(
                snowpark_fn.array_contains(value, snowpark_args[0]),
                lambda n=ac_nullable: [FieldType(BooleanType(), n)],
            )
        case "array_distinct":
            result_exp = TypedColumn(
                snowpark_fn.array_distinct(snowpark_args[0]),
                lambda: snowpark_typed_args[0].field_types,
            )
        case "array_except":
            result_contains_null = snowpark_typed_args[0].typ.contains_null
            arr1, arr2, result_arr_type = _coerce_two_arrays(
                snowpark_args[0],
                snowpark_typed_args[0].typ,
                snowpark_args[1],
                snowpark_typed_args[1].typ,
                result_contains_null,
            )
            bn = _binary_nullable(snowpark_typed_args)
            result_exp = TypedColumn(
                snowpark_fn.array_except(arr1, arr2),
                lambda: [FieldType(result_arr_type, bn)],
            )
        case "array_insert":
            data = snowpark_args[0]
            spark_index = snowpark_args[1]
            el = snowpark_args[2]

            input_array_type = snowpark_typed_args[0].types[0]
            value_type = snowpark_typed_args[2].typ
            if not isinstance(value_type, NullType):
                elem_type = input_array_type.element_type
                compatible = type(elem_type) is type(value_type) or (
                    isinstance(elem_type, _NumericType)
                    and isinstance(value_type, _NumericType)
                )
                if not compatible:
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.ARRAY_FUNCTION_DIFF_TYPES] Cannot resolve "{spark_function_name}" due to data type mismatch: '
                        f'Input to `array_insert` should have been "ARRAY" followed by a value with same element type, '
                        f'but it\'s ["{input_array_type}", "{value_type}"].'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception

                data, el, widened_type = _coerce_array_and_element(
                    data, input_array_type, el, value_type
                )
                if widened_type.element_type != input_array_type.element_type:
                    input_array_type = ArrayType(
                        widened_type.element_type,
                        structured=input_array_type.structured,
                        contains_null=_inner_nullable(input_array_type.contains_null),
                    )

            array_type_containing_nulls = ArrayType(
                input_array_type.element_type,
                structured=input_array_type.structured,
                contains_null=True,
            )
            if not input_array_type.contains_null:
                data = snowpark_fn.cast(data, array_type_containing_nulls)
            bn = _binary_nullable(snowpark_typed_args)

            _invalid_zero = "[snowpark_connect::INVALID_INDEX_OF_ZERO] The index 0 is invalid. An index shall be either < 0 or > 0 (the first element has index 1)."
            arr_size = snowpark_fn.array_size(data)
            legacy_neg_index = global_config.spark_sql_legacy_negativeIndexInArrayInsert

            if legacy_neg_index:
                # Snowflake's native negative-index semantics exactly match Spark legacy:
                # -1 inserts before the last element, -N inserts at arr_size-N (0-based),
                # and OOB positions pad with nulls (abs(pos)-arr_size nulls between item
                # and the original array). Pass the Spark index directly — no formula
                # adjustment needed for negatives. Positive indices still need 1-based→0-based.
                snow_index = (
                    snowpark_fn.when(
                        spark_index == 0,
                        snowpark_fn.lit(_invalid_zero),
                    )
                    .when(spark_index > 0, spark_index - 1)
                    .otherwise(spark_index)
                )
                result_col = snowpark_fn.array_insert(data, snow_index, el)
            else:
                snow_index = (
                    snowpark_fn.when(
                        spark_index < (arr_size * snowpark_fn.lit(-1)),
                        spark_index + 1,
                    )
                    .when(spark_index < 0, arr_size + spark_index + 1)
                    .when(
                        spark_index == 0,
                        snowpark_fn.lit(_invalid_zero),
                    )
                    .otherwise(spark_index - 1)
                )
                result_col = snowpark_fn.array_insert(data, snow_index, el)

            result_exp = TypedColumn(
                result_col,
                lambda n=bn, t=array_type_containing_nulls: [FieldType(t, n)],
            )
        case "array_intersect":
            result_contains_null = (
                snowpark_typed_args[0].typ.contains_null
                and snowpark_typed_args[1].typ.contains_null
            )
            arr1, arr2, result_arr_type = _coerce_two_arrays(
                snowpark_args[0],
                snowpark_typed_args[0].typ,
                snowpark_args[1],
                snowpark_typed_args[1].typ,
                result_contains_null,
            )
            bn = _binary_nullable(snowpark_typed_args)
            result_exp = TypedColumn(
                snowpark_fn.array_intersection(arr1, arr2),
                lambda: [FieldType(result_arr_type, bn)],
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [
                    FieldType(
                        StringType(),
                        nullable=_any_arg_nullable(snowpark_typed_args),
                    )
                ],
            )
        case "array_max":
            result_exp = TypedColumn(
                snowpark_fn.array_max(snowpark_args[0]),
                lambda: [
                    FieldType(snowpark_typed_args[0].typ.element_type, nullable=True)
                ],
            )
        case "array_min":
            result_exp = TypedColumn(
                snowpark_fn.array_min(snowpark_args[0]),
                lambda: [
                    FieldType(snowpark_typed_args[0].typ.element_type, nullable=True)
                ],
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
            bn = _binary_nullable(snowpark_typed_args)
            result_exp = TypedColumn(
                result_exp, lambda n=bn: [FieldType(LongType(), n)]
            )
        case "array_prepend":
            arr_arg, elem_arg, result_arr_type = _coerce_array_and_element(
                snowpark_args[0],
                snowpark_typed_args[0].typ,
                snowpark_args[1],
                snowpark_typed_args[1].typ,
            )
            result_exp = TypedColumn(
                snowpark_fn.array_prepend(arr_arg, elem_arg),
                lambda: [result_arr_type],
            )
        case "array_remove":
            array_type = snowpark_typed_args[0].typ
            assert isinstance(
                array_type, ArrayType
            ), f"Expected argument '{snowpark_arg_names[0]}' to have an ArrayType."
            result_exp = snowpark_fn.array_remove(snowpark_args[0], snowpark_args[1])
            if array_type.structured and array_type.element_type is not None:
                result_exp = snowpark_fn.cast(result_exp, array_type)
            bn = _binary_nullable(snowpark_typed_args)
            ar_type = snowpark_typed_args[0].typ
            result_exp = TypedColumn(
                result_exp, lambda t=ar_type, n=bn: [FieldType(t, n)]
            )
        case "array_repeat":
            elem, count = snowpark_args[0], snowpark_args[1]
            elem_type = snowpark_typed_args[0].typ
            result_type = ArrayType(elem_type)

            elem_variant = snowpark_fn.cast(elem, VariantType())

            result_exp = snowpark_fn.cast(
                snowpark_fn.call_function("ARRAY_REPEAT", elem_variant, count),
                result_type,
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
            result_array_contains_null = (
                snowpark_typed_args[0].typ.contains_null
                or snowpark_typed_args[1].typ.contains_null
            )
            arr1, arr2, result_arr_type = _coerce_two_arrays(
                snowpark_args[0],
                snowpark_typed_args[0].typ,
                snowpark_args[1],
                snowpark_typed_args[1].typ,
                result_array_contains_null,
            )
            bn = _binary_nullable(snowpark_typed_args)
            result_exp = snowpark_fn.array_distinct(snowpark_fn.array_cat(arr1, arr2))
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_arr_type, bn)]
            )
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
            arr1_type = snowpark_typed_args[0].typ
            arr2_type = snowpark_typed_args[1].typ
            ao_contains_null = (
                isinstance(arr1_type, ArrayType) and arr1_type.contains_null
            ) or (isinstance(arr2_type, ArrayType) and arr2_type.contains_null)
            ao_nullable = _binary_nullable(snowpark_typed_args) or ao_contains_null
            result_exp = TypedColumn(
                result_exp, lambda n=ao_nullable: [FieldType(BooleanType(), n)]
            )
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
                    for i, (name, _) in enumerate(array_arg_info)
                )
                variant_args = [arg.cast(ArrayType()) for arg in snowpark_args]
                result_exp = snowpark_fn.arrays_zip(*variant_args)
                result_exp = snowpark_fn.function("transform")(
                    result_exp,
                    snowpark_fn.sql_expr(
                        f"elem -> object_construct_keep_null({field_mappings})"
                    ),
                )

                struct_fields = [
                    StructField(name, elem_type, nullable=True, _is_column=False)
                    for name, elem_type in array_arg_info
                ]
                result_type = ArrayType(
                    StructType(struct_fields, structured=True),
                    contains_null=_inner_nullable(False),
                )
                result_exp = TypedColumn(
                    snowpark_fn.cast(result_exp, result_type),
                    lambda: [
                        FieldType(
                            result_type,
                            nullable=_any_arg_nullable(snowpark_typed_args),
                        )
                    ],
                )
        case "asc":
            result_exp = TypedColumn(
                snowpark_fn.asc(snowpark_args[0]), lambda: snowpark_typed_args[0].types
            )
        case "ascii":
            # Snowflake's ascii function doesn't match PySpark's however the unicode function does.
            unicode_function = snowpark_fn.function("unicode")
            result_exp = unicode_function(snowpark_args[0])
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
        case "asin":
            spark_function_name = f"ASIN({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                (snowpark_args[0] < -1) | (snowpark_args[0] > 1), NAN
            ).otherwise(snowpark_fn.asin(snowpark_args[0]))
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(DoubleType(), nullable=True)]
            )
        case "asinh":
            spark_function_name = f"ASINH({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.asinh(snowpark_args[0]),
                lambda: [FieldType(DoubleType(), nullable=True)],
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
                snowpark_fn.atan(snowpark_args[0]),
                lambda: [FieldType(DoubleType(), nullable=True)],
            )
        case "atan2":
            spark_function_name = (
                f"ATAN2({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
            )
            bn = _binary_nullable(snowpark_typed_args)
            result_exp = TypedColumn(
                snowpark_fn.atan2(snowpark_args[0], snowpark_args[1]),
                lambda n=bn: [FieldType(DoubleType(), n)],
            )
        case "atanh":
            spark_function_name = f"ATANH({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                (snowpark_args[0] < -1) | (snowpark_args[0] > 1), NAN
            ).otherwise(snowpark_fn.atanh(snowpark_args[0]))
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(DoubleType(), nullable=True)]
            )
        case "avg" | "mean":
            spark_function_name = f"avg({snowpark_arg_names[0]})"
            input_type = snowpark_typed_args[0].typ
            if isinstance(input_type, DecimalType):
                result_type = _bounded_decimal(
                    input_type.precision + 4, input_type.scale + 4
                )
            else:
                result_type = DoubleType()

            avg_arg = snowpark_args[0]
            if isinstance(input_type, StringType):
                # SNOW-3585745: Spark coerces string inputs to double; a strict
                # CAST here fails with 100038 on non-numeric data even in
                # non-ANSI mode. Use TRY_CAST (NULL on bad input) to match Spark.
                avg_arg = _coerce_string_input_to_double(
                    avg_arg,
                    spark_sql_ansi_enabled,
                    aggregate_string_coercion_enabled,
                )
            avg_exp = snowpark_fn.avg(avg_arg)
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
                        avg_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                        _build_window_avg,
                    )
                else:
                    result_exp = TypedColumn(
                        _cast_with_decimal_overflow_check(
                            avg_exp, result_type, spark_sql_ansi_enabled
                        ),
                        lambda: [FieldType(result_type, nullable=True)],
                    )
            else:
                result_exp = _resolve_aggregate_exp(avg_exp, result_type, nullable=True)
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
                base64_encoding_function(snowpark_args[0]),
                lambda: [FieldType(StringType(), _unary_nullable(snowpark_typed_args))],
            )
        case "bin":
            arg = snowpark_args[0]
            input_type = snowpark_typed_args[0].typ
            # Normalize input to bigint:
            # - Floats: truncate toward zero then cast to bigint
            # - Strings: try_cast returns NULL for non-numeric values
            # - Integers: cast directly
            if isinstance(input_type, _FractionalType):
                casted = snowpark_fn.cast(
                    snowpark_fn.trunc(arg, snowpark_fn.lit(0)), LongType()
                )
                nullable = True
            elif isinstance(input_type, StringType):
                casted = snowpark_fn.try_cast(arg, LongType())
                nullable = True
            else:
                casted = snowpark_fn.cast(arg, LongType())
                nullable = _unary_nullable(snowpark_typed_args)
            # Handle LONG_MIN edge case where snowpark_conv overflows
            long_min = -(2**63)
            long_min_bin = "1" + "0" * 63
            result_exp = snowpark_fn.iff(
                casted == snowpark_fn.lit(long_min),
                snowpark_fn.lit(long_min_bin),
                snowpark_fn.function("snowpark_conv")(
                    casted,
                    10,
                    2,
                    spark_sql_ansi_enabled,
                ),
            )
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(StringType(), nullable)]
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
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

            if snowpark_arg_names[0] in ("True", "False"):
                spark_function_name = f"bit_count({snowpark_arg_names[0].lower()})"

            if isinstance(snowpark_typed_args[0].typ, BooleanType):
                result_exp = (
                    snowpark_fn.when(
                        snowpark_fn.is_null(snowpark_args[0]), snowpark_fn.lit(None)
                    )
                    .when(snowpark_args[0], snowpark_fn.lit(1))
                    .otherwise(snowpark_fn.lit(0))
                )
            elif isinstance(snowpark_typed_args[0].typ, NullType):
                result_exp = snowpark_fn.lit(None)
            else:

                @cached_udf(
                    input_types=[VariantType()],
                    return_type=LongType(),
                )
                def _bit_count_udf(intval):
                    try:
                        n = int(intval)
                        if n < 0:
                            n = n & 0xFFFFFFFFFFFFFFFF
                        return n.bit_count()
                    except (ValueError, TypeError):
                        return None

                result_exp = _bit_count_udf(
                    snowpark_fn.cast(snowpark_args[0], VariantType())
                )
            result_type = IntegerType()
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, _unary_nullable(snowpark_typed_args))],
            )
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
            result_type = FieldType(ByteType(), _binary_nullable(snowpark_typed_args))
        case "bit_length":
            bit_length_function = snowpark_fn.function("bit_length")
            result_exp = bit_length_function(snowpark_args[0])
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
        case "bit_or":
            bit_or_agg_function = snowpark_fn.function("BITOR_AGG")
            result_exp = bit_or_agg_function(snowpark_args[0])
            result_type = _evaluate_bit_operation_result_type(
                snowpark_typed_args[0].typ,
                snowpark_arg_names[0],
                IntegerType(),
                spark_function_name,
            )
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "bitmap_bit_position":
            arg = snowpark_args[0]

            arg_as_integer = snowpark_fn.when(arg < 0, snowpark_fn.ceil(arg)).otherwise(
                snowpark_fn.floor(arg)
            )

            result_exp = TypedColumn(
                snowpark_fn.bitmap_bit_position(arg_as_integer),
                lambda: [
                    FieldType(
                        LongType(),
                        nullable=_any_arg_nullable(snowpark_typed_args),
                    )
                ],
            )
        case "bitmap_bucket_number":
            result_exp = TypedColumn(
                snowpark_fn.bitmap_bucket_number(snowpark_args[0]),
                lambda: [
                    FieldType(
                        LongType(),
                        nullable=_any_arg_nullable(snowpark_typed_args),
                    )
                ],
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
            result_type = FieldType(BinaryType(), nullable=False)
        case "bitmap_count":

            @cached_udf(input_types=[BinaryType()], return_type=LongType())
            def _bitmap_count(bitmap: Optional[bytes]) -> Optional[int]:
                if bitmap is None:
                    return None

                return functools.reduce(
                    lambda acc, el: acc + bin(el).count("1"), list(bitmap), 0
                )

            result_exp = _bitmap_count(snowpark_args[0])
            result_type = FieldType(
                LongType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
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
            result_type = FieldType(BinaryType(), nullable=False)
        case "bool_and" | "every":
            if not isinstance(snowpark_typed_args[0].typ, (BooleanType, NullType)):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 1 requires the \'BOOLEAN\' type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ.simpleString().upper()}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            bool_and_agg_function = snowpark_fn.function("booland_agg")
            result_exp = TypedColumn(
                bool_and_agg_function(*snowpark_args),
                lambda: [FieldType(BooleanType(), nullable=True)],
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
                bool_or_agg_function(*snowpark_args),
                lambda: [FieldType(BooleanType(), nullable=True)],
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
                    attach_custom_error_code(exception, ErrorCodes.ARITHMETIC_OVERFLOW)
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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(return_type, nullable=True)],
                    )
                case _:
                    # TODO: Snowflake's bround only supports decimal, not floating point types.
                    # If fixing this in Snowflake takes some time, we should change to use a UDF here for float.
                    # For now, this is just an approximation by casting to Decimal and casting back.
                    scale_for_decimal = 0 if scale < 0 else min(scale + 2, 38)
                    result_type = snowpark_typed_args[0].typ
                    result_exp = snowpark_fn.cast(
                        snowpark_fn.bround(
                            snowpark_fn.to_decimal(
                                snowpark_args[0], 38, scale_for_decimal
                            ),
                            snowpark_fn.lit(scale),
                        ),
                        result_type,
                    )
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
        case "btrim" | "trim":
            args = [
                (
                    _to_char(typed_arg.col)
                    if isinstance(typed_arg.typ, BinaryType)
                    else typed_arg.col
                )
                for typed_arg in snowpark_typed_args
            ]
            result_exp = TypedColumn(
                snowpark_fn.trim(*args),
                lambda: [
                    FieldType(
                        StringType(),
                        nullable=_any_arg_nullable(snowpark_typed_args),
                    )
                ],
            )
            if len(args) == 2 and function_name == "trim":
                spark_function_name = (
                    f"TRIM(BOTH {snowpark_arg_names[1]} FROM {snowpark_arg_names[0]})"
                )
        case "cbrt":
            spark_function_name = f"CBRT({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.cbrt(snowpark_args[0]),
                lambda: [FieldType(DoubleType(), nullable=True)],
            )
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
                    result_exp.cast(result_type),
                    lambda: [FieldType(result_type, nullable=True)],
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
                result_exp = TypedColumn(
                    result_exp,
                    lambda: [FieldType(result_type, nullable=True)],
                )
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(StringType(), _unary_nullable(snowpark_typed_args))],
            )
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
                    coerced_args = []
                    for i, arg in enumerate(snowpark_args):
                        arg_type = snowpark_typed_args[i].typ
                        if arg_type == result_type and not isinstance(
                            result_type, _IntegralType
                        ):
                            coerced_args.append(arg)
                        elif isinstance(arg_type, NullType) or _is_null_typed_container(
                            arg_type
                        ):
                            coerced_args.append(
                                _coerce_null_typed_expr(arg, arg_type, result_type)
                            )
                        else:
                            coerced_args.append(arg.cast(result_type))
                    result_exp = snowpark_fn.coalesce(*coerced_args)
                    coalesce_nullable = all(
                        cast_nullable(arg.nullable, arg.typ, result_type)
                        for arg in snowpark_typed_args
                    )
                    result_type = FieldType(
                        result_type,
                        nullable=coalesce_nullable,
                    )
        case "collect_list" | "array_agg":
            # TODO: SNOW-1967177 - Support structured types in array_agg
            result_exp = snowpark_fn.array_agg(
                snowpark_typed_args[0].column(to_semi_structure=True)
            )
            result_exp = _resolve_aggregate_exp(
                result_exp,
                ArrayType(
                    snowpark_typed_args[0].typ,
                    contains_null=_inner_nullable(False),
                ),
                nullable=False,
            )
            spark_function_name = f"collect_list({snowpark_arg_names[0]})"
        case "collect_set":
            # Convert to a semi-structured type. TODO SNOW-1953065 - Support structured types in array_unique_agg.
            result_exp = snowpark_fn.array_unique_agg(
                snowpark_typed_args[0].column(to_semi_structure=True)
            )
            result_exp = _resolve_aggregate_exp(
                result_exp,
                ArrayType(
                    snowpark_typed_args[0].typ,
                    contains_null=_inner_nullable(False),
                ),
                nullable=False,
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
                    snowpark_args = []
                    for arg in snowpark_typed_args:
                        match arg.typ:
                            case StringType():
                                snowpark_args.append(arg.col)
                            case BinaryType():
                                snowpark_args.append(
                                    snowpark_fn.call_function(
                                        "__SNOWPARK_INTERNAL_DECODE",
                                        arg.col,
                                        snowpark_fn.lit("utf-8"),
                                    )
                                )
                            case _:
                                snowpark_args.append(
                                    snowpark_fn.cast(arg.col, StringType())
                                )
                elif not isinstance(result_type, BinaryType) and not isinstance(
                    result_type, ArrayType
                ):
                    result_type = StringType()

                if len(snowpark_args) == 1:
                    result_exp = TypedColumn(
                        snowpark_args[0],
                        lambda: [
                            FieldType(
                                result_type,
                                nullable=_any_arg_nullable(snowpark_typed_args),
                            )
                        ],
                    )
                elif isinstance(result_type, ArrayType):
                    result_exp = TypedColumn(
                        functools.reduce(
                            lambda acc, tc: snowpark_fn.array_cat(
                                acc, tc.column(to_semi_structure=True)
                            ),
                            snowpark_typed_args[2:],
                            snowpark_fn.array_cat(
                                snowpark_typed_args[0].column(to_semi_structure=True),
                                snowpark_typed_args[1].column(to_semi_structure=True),
                            ),
                        ).cast(result_type),
                        lambda: [
                            FieldType(
                                result_type,
                                nullable=_any_arg_nullable(snowpark_typed_args),
                            )
                        ],
                    )
                else:
                    result_exp = TypedColumn(
                        snowpark_fn.concat(*snowpark_args),
                        lambda: [
                            FieldType(
                                result_type,
                                nullable=_any_arg_nullable(snowpark_typed_args),
                            )
                        ],
                    )
        case "concat_ws":
            delimiter = unwrap_literal(exp.unresolved_function.arguments[0])
            result_exp = snowpark_fn._concat_ws_ignore_nulls(
                delimiter, *snowpark_args[1:]
            )
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(StringType(), _unary_nullable(snowpark_typed_args))],
            )
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

            bn = _binary_nullable(snowpark_typed_args)
            result_exp = TypedColumn(
                arg1.contains(arg2), lambda n=bn: [FieldType(BooleanType(), n)]
            )
        case "conv":
            val_col = snowpark_args[0]
            from_base_val = int(snowpark_args[1]._expression.value)
            to_base_val = int(snowpark_args[2]._expression.value)

            result_exp = snowpark_fn.function("snowpark_conv")(
                val_col,
                from_base_val,
                to_base_val,
                spark_sql_ansi_enabled,
            )
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(StringType(), nullable=True)]
            )

        case "convert_timezone":
            if len(snowpark_args) == 3:
                result_exp = snowpark_fn.convert_timezone(
                    snowpark_args[1], snowpark_args[2], snowpark_args[0]
                )
            else:
                spark_function_name = f"convert_timezone(current_timezone(), {', '.join(snowpark_arg_names)})"
                result_exp = snowpark_fn.convert_timezone(*snowpark_args)

            ts_ntz = TimestampType(TimestampTimeZone.NTZ)
            result_type = FieldType(
                ts_ntz,
                nullable=_any_arg_nullable(snowpark_typed_args),
            )
            result_exp = result_exp.cast(ts_ntz)

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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(DoubleType(), nullable=True)]
            )
        case "cos":
            spark_function_name = f"COS({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.cos(snowpark_args[0]),
                lambda: [FieldType(DoubleType(), nullable=True)],
            )
        case "cosh":
            spark_function_name = f"COSH({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.cosh(snowpark_args[0]),
                lambda: [FieldType(DoubleType(), nullable=True)],
            )
        case "cot":
            spark_function_name = f"COT({snowpark_arg_names[0]})"
            result_exp = TypedColumn(
                snowpark_fn.function("cot")(snowpark_args[0]),
                lambda: [FieldType(DoubleType(), nullable=True)],
            )
        case "count":
            result_type = LongType()
            num_args = len(list(exp.unresolved_function.arguments))

            if num_args == 0:
                allow_parameterless = global_config.get(
                    "spark.sql.legacy.allowParameterlessCount"
                )
                if str(allow_parameterless).lower() == "true":
                    spark_function_name = "count()"
                    # Spark's NullPropagation optimizes count() to literal 0
                    # (vacuous truth: Seq.empty.forall(isNullLiteral) == true)
                    # Use count(NULL) which is always 0, preserving aggregate semantics
                    result_exp = snowpark_fn.count(snowpark_fn.lit(None))
                else:
                    exception = AnalysisException(
                        "[WRONG_NUM_ARGS.WITHOUT_SUGGESTION] The `count` "
                        "requires at least 1 parameter(s) but the actual "
                        "number is 0."
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                    raise exception
            elif exp.unresolved_function.is_distinct:
                result_exp = snowpark_fn.count_distinct(*snowpark_args)
                spark_function_name = spark_function_name.replace(
                    "count(", "count(DISTINCT ", 1
                )
            else:
                is_plain_star = (
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
                )
                if is_plain_star:
                    spark_function_name = "count(1)"
                    result_exp = snowpark_fn.count(
                        snowpark_fn.col("*", _is_qualified_name=True)
                    )
                else:
                    # Check for qualified star (e.g. count(testData.*)).
                    # For the SQL path, the JVM parser validates this before
                    # we get here. This guard covers the DataFrame API path.
                    # Only enforce allowStarWithSingleTableIdentifierInCount
                    # when there is exactly 1 argument. Multi-arg count like
                    # count(testData.*, testData.*) is a valid multi-expression
                    # count and should pass through.
                    if num_args == 1:
                        is_qualified_star = exp.unresolved_function.arguments[
                            0
                        ].HasField(
                            "unresolved_star"
                        ) and exp.unresolved_function.arguments[
                            0
                        ].unresolved_star.HasField(
                            "unparsed_target"
                        )
                        if is_qualified_star:
                            allow_star = global_config.get(
                                "spark.sql.legacy.allowStarWithSingleTableIdentifierInCount"
                            )
                            if str(allow_star).lower() != "true":
                                target = exp.unresolved_function.arguments[
                                    0
                                ].unresolved_star.unparsed_target
                                # unparsed_target ends with ".*", strip it for error message
                                if target.endswith(".*"):
                                    target = target[:-2]
                                exception = AnalysisException(
                                    f"Since Spark 2.0, Star (*) is not allowed in count({target}.*)."
                                )
                                attach_custom_error_code(
                                    exception, ErrorCodes.INVALID_INPUT
                                )
                                raise exception
                    result_exp = snowpark_fn.call_function("COUNT", *snowpark_args)
            result_exp = _resolve_aggregate_exp(result_exp, result_type, nullable=False)
        case "count_if":
            result_type = LongType()
            result_exp = snowpark_fn.call_function("COUNT_IF", snowpark_args[0])
            result_exp = _resolve_aggregate_exp(result_exp, result_type, nullable=False)
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
            result_type = FieldType(BinaryType(), nullable=False)
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
            result_type = FieldType(LongType(), _unary_nullable(snowpark_typed_args))
        case "csc":
            spark_function_name = f"CSC({snowpark_arg_names[0]})"
            csc_base = snowpark_fn.when(
                snowpark_fn.is_null(snowpark_args[0]), snowpark_fn.lit(None)
            )
            if isinstance(snowpark_typed_args[0].typ, (FloatType, DoubleType)):
                csc_base = csc_base.when(
                    snowpark_fn.equal_nan(snowpark_args[0]),
                    snowpark_fn.lit(NAN),
                )
            result_exp = csc_base.otherwise(
                snowpark_fn.coalesce(
                    _divnull(
                        snowpark_fn.lit(1.0),
                        snowpark_fn.sin(snowpark_args[0]),
                    ),
                    snowpark_fn.lit(INFINITY),
                )
            )
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(DoubleType(), nullable=True)]
            )
        case "cume_dist":
            result_exp = TypedColumn(
                snowpark_fn.cume_dist(),
                lambda: [FieldType(DoubleType(), nullable=False)],
            )
        case "current_catalog":
            result_exp = snowpark_fn.lit(CURRENT_CATALOG_NAME)
            result_type = FieldType(StringType(), nullable=False)
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
            result_exp = TypedColumn(
                snowpark_fn.current_date(),
                lambda: [FieldType(DateType(), nullable=False)],
            )
            spark_function_name = "current_date()"
        case "current_timestamp" | "now":
            result_type = FieldType(
                TimestampType(TimestampTimeZone.LTZ), nullable=False
            )
            result_exp = snowpark_fn.to_timestamp_ltz(snowpark_fn.current_timestamp())
        case "current_timezone":
            result_exp = snowpark_fn.lit(global_config.spark_sql_session_timeZone)
            result_type = FieldType(StringType(), nullable=False)
        case "current_user" | "user":
            result_exp = TypedColumn(
                snowpark_fn.current_user(),
                lambda: [FieldType(StringType(), nullable=False)],
            )
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
            bn = _binary_nullable(snowpark_typed_args)
            result_exp = TypedColumn(
                result_exp, lambda n=bn: [FieldType(DateType(), n)]
            )
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
            result_type = FieldType(
                IntegerType(), _binary_nullable(snowpark_typed_args)
            )
            result_exp = snowpark_fn.cast(result_exp, result_type.datatype)
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
            bn = _binary_nullable(snowpark_typed_args)
            result_exp = TypedColumn(
                result_exp, lambda n=bn: [FieldType(StringType(), n)]
            )
        case "date_from_unix_date":
            result_exp = snowpark_fn.date_add(
                snowpark_fn.to_date(snowpark_fn.lit("1970-01-01")), snowpark_args[0]
            )
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(DateType(), _unary_nullable(snowpark_typed_args))],
            )
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
            bn = _binary_nullable(snowpark_typed_args)
            result_exp = TypedColumn(
                result_exp, lambda n=bn: [FieldType(DateType(), n)]
            )
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
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
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
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
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
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
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
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
            charset = unwrap_literal(exp.unresolved_function.arguments[1])

            if snowpark_typed_args[0].typ == StringType():
                result_exp = snowpark_typed_args[0].col
            elif charset and charset.lower().replace("-", "") == "utf32":
                # UDF is needed for pure UTF-32 (without LE/BE suffix), because
                # __SNOWPARK_INTERNAL_DECODE always assumes big endian

                @cached_udf(
                    input_types=[BinaryType(), StringType()],
                    return_type=StringType(),
                )
                def _decode_raw_utf32(s: bytes, f: str):
                    if None in (s, f):
                        return None

                    if len(s) > 0 and s[:4] not in (
                        b"\x00\x00\xfe\xff",
                        b"\xff\xfe\x00\x00",
                    ):
                        s = b"\x00\x00\xfe\xff" + s

                    return s.decode(f)

                result_exp = _decode_raw_utf32(*snowpark_args)
            else:
                result_exp = snowpark_fn.call_function(
                    "__SNOWPARK_INTERNAL_DECODE", *snowpark_args
                )

            result_type = StringType()
        case "degrees":
            spark_function_name = f"DEGREES({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.degrees(snowpark_args[0])
            result_type = DoubleType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "dense_rank":
            result_exp = snowpark_fn.dense_rank()
            # IntegerType per Spark's DenseRank case class which extends AggregateWindowFunction, which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/34d9413ca161f4531544565976a46c6da7d371cd/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/windowExpressions.scala#L626
            result_exp = _resolve_aggregate_exp(
                result_exp, IntegerType(), nullable=False
            )
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "e":
            spark_function_name = "E()"
            result_type = FieldType(DoubleType(), nullable=False)
            result_exp = snowpark_fn.lit(math.e, datatype=DoubleType())
        case "element_at":
            spark_index = snowpark_args[1]
            data = snowpark_typed_args[0].col
            typ = snowpark_typed_args[0].typ
            match typ:
                case ArrayType():
                    result_type = typ.element_type
                    arr_size = snowpark_fn.array_size(data)
                    if spark_sql_ansi_enabled:
                        raise_error = _raise_error_helper(
                            result_type,
                            error_class=ArrayIndexOutOfBoundsException,
                        )
                        oob_error = raise_error(
                            snowpark_fn.lit(
                                "[INVALID_ARRAY_INDEX_IN_ELEMENT_AT] The index is out of bounds."
                            )
                        )
                        snow_index = (
                            snowpark_fn.when(
                                spark_index == 0,
                                snowpark_fn.lit(
                                    "[snowpark_connect::invalid_index_of_zero] The index 0 is invalid. An index shall be either < 0 or > 0 (the first element has index 1)."
                                ),
                            )
                            .when(
                                (spark_index > 0) & (spark_index > arr_size),
                                oob_error,
                            )
                            .when(
                                (spark_index < 0) & ((arr_size + spark_index) < 0),
                                oob_error,
                            )
                            .when(spark_index < 0, arr_size + spark_index)
                            .otherwise(spark_index - 1)
                        )
                    else:
                        snow_index = (
                            snowpark_fn.when(
                                spark_index < 0,
                                arr_size + spark_index,
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
            charset = unwrap_literal(exp.unresolved_function.arguments[1])

            if snowpark_typed_args[0].typ == BinaryType():
                result_exp = snowpark_typed_args[0].col
            elif charset and charset.lower().replace("-", "") == "utf16":
                # UDF is needed for pure UTF-16 (without LE/BE suffix), because Spark defaults
                # to Big Endian (with a BOM), while Snowflake defaults to Little Endian (with a BOM)

                @cached_udf(
                    input_types=[StringType(), StringType()],
                    return_type=BinaryType(),
                )
                def _encode_raw_utf16(s: str, f: str):
                    if None in (s, f):
                        return None

                    return (b"\xfe\xff" if s else b"") + s.encode("utf-16be")

                result_exp = _encode_raw_utf16(*snowpark_args)
            else:
                result_exp = snowpark_fn.call_function(
                    "__SNOWPARK_INTERNAL_ENCODE", *snowpark_args
                )

            result_type = FieldType(BinaryType(), _binary_nullable(snowpark_typed_args))
        case "endswith":
            result_exp = snowpark_args[0].endswith(snowpark_args[1])
            result_type = FieldType(
                BooleanType(), _binary_nullable(snowpark_typed_args)
            )
        case "equal_null":
            result_exp = snowpark_fn.equal_null(*snowpark_args)
            result_type = FieldType(BooleanType(), nullable=False)
        case "exp":
            spark_function_name = f"EXP({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.exp(*snowpark_args)
            result_type = DoubleType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
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
                    # Semi-structured Snowflake ARRAYs have no element type
                    # (element_type is None). Their elements are variants, which
                    # surface as StringType on the client just like VariantType.
                    result_type = input_type.element_type or VariantType()
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
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
            result_type = FieldType(
                IntegerType(), _binary_nullable(snowpark_typed_args)
            )
            result_exp = snowpark_fn.cast(result_exp, result_type.datatype)
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
                    result_exp.cast(result_type),
                    lambda: [FieldType(result_type, nullable=True)],
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
                result_exp = TypedColumn(
                    result_exp,
                    lambda: [FieldType(result_type, nullable=True)],
                )
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
            result_type = FieldType(StringType(), _unary_nullable(snowpark_typed_args))
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
            result_type = FieldType(result_type, _unary_nullable(snowpark_typed_args))
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

            # If the original element is NULL, the result of the cast will also be NULL.
            # Schema checking of fields (dropping extra fields, NULLing missing fields) is handled by the server.
            result_exp = snowpark_fn.try_parse_json(snowpark_args[0]).try_cast(
                result_type,
                permissive=True,
            )
            if isinstance(result_type, StructType):
                # If the top-level expected return type is a struct, Spark will implicitly retain nulls for all fields.
                # The top-level return of the TRY_CAST will only be NULL if the input was a scalar, so we handle this case by doing
                # a dummy TRY_CAST on an empty object.
                result_exp = snowpark_fn.ifnull(
                    result_exp,
                    snowpark_fn.object_construct().try_cast(
                        result_type, permissive=True
                    ),
                )
            if isinstance(result_type, ArrayType) and isinstance(
                result_type.element_type, StructType
            ):
                result_exp = snowpark_fn.ifnull(
                    result_exp,
                    # If the top-level expected return type is an array, Spark will implicitly wrap a scalar value if the type matches.
                    snowpark_fn.to_array(
                        snowpark_fn.try_parse_json(snowpark_args[0])
                    ).try_cast(result_type, permissive=True),
                )

            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )

        case "parse_json" | "try_parse_json":
            if len(snowpark_args) != 1:
                exception = ValueError(
                    f"{exp.unresolved_function.function_name} expects exactly one argument"
                )
                attach_custom_error_code(
                    exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                )
                raise exception

            parse_fn = (
                snowpark_fn.parse_json
                if exp.unresolved_function.function_name == "parse_json"
                else snowpark_fn.try_parse_json
            )
            result_exp = TypedColumn(
                parse_fn(snowpark_args[0]),
                lambda: [FieldType(VariantType(), nullable=True)],
            )

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
                        snowpark_fn.trunc(
                            snowpark_fn.function("try_to_double")(snowpark_args[0])
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "from_utc_timestamp":
            ts_arg, tz_arg = snowpark_args[0], snowpark_args[1]
            if isinstance(tz_arg._expression, Literal) and isinstance(
                tz_arg._expression.value, str
            ):
                literal_val = tz_arg._expression.value
                offset_secs = _literal_offset_seconds(literal_val)
                if offset_secs is not None:
                    # Literal UTC offset: compute seconds at translation time, emit DATEADD.
                    ts_expr = snowpark_fn.dateadd(
                        "second", snowpark_fn.lit(offset_secs), ts_arg
                    )
                else:
                    # Literal IANA name or Java short ID: resolve tz string, convert_timezone.
                    ts_expr = snowpark_fn.from_utc_timestamp(
                        ts_arg, _map_from_spark_tz(tz_arg)
                    )
            else:
                # Dynamic tz column: pure-SQL CASE/WHEN, no Python UDF.
                ts_expr = _build_utc_timestamp_expr(ts_arg, tz_arg, from_utc=True)
            result_exp = _try_to_cast(
                "try_to_timestamp",
                ts_expr.cast(TimestampType()),
                ts_arg,
            )
            result_type = FieldType(
                TimestampType(), _binary_nullable(snowpark_typed_args)
            )
        case "get":
            if exp.unresolved_function.arguments[1].HasField("literal"):
                index = unwrap_literal(exp.unresolved_function.arguments[1])
                if index is None or index < 0:
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
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
                        lambda r=result: [
                            FieldType(
                                ft.datatype,
                                nullable=_all_args_nullable(snowpark_typed_args)
                                or ft.nullable,
                            )
                            for ft in r.field_types
                        ],
                    )
                result_exp = result
            else:
                greatest_ignore_nulls = snowpark_fn.function("greatest_ignore_nulls")
                result_exp = greatest_ignore_nulls(*snowpark_args)
                result_exp = TypedColumn(
                    result_exp,
                    lambda: [
                        FieldType(
                            _find_common_type([a.typ for a in snowpark_typed_args]),
                            nullable=_all_args_nullable(snowpark_typed_args),
                        )
                    ],
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
                dt = LongType()
            else:
                result_exp = snowpark_fn.grouping(*snowpark_args)
                # Spark 3.5.3: Grouping defines dataType = ByteType
                # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/grouping.scala#L213
                dt = ByteType()
            result_exp = snowpark_fn.cast(result_exp, dt)
            result_type = FieldType(dt, nullable=False)
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
            dt = IntegerType()
            # Spark returns a 32bit value when Snowflakes hash generates 64bit. We have to perform integral overflow to ensure that the value is within the range.
            result_exp = apply_integral_overflow(result_exp, dt, force=True)
            result_type = FieldType(dt, nullable=False)
        case "hex":
            # We need as many 'X' as there are digits. The longest possible 'long' type has 16 digits.
            format_string = "FMXXXXXXXXXXXXXXXX"

            # Hex supports string, binary, integer/long.
            # Dispatch at compile time based on known input type rather than
            # casting to VARIANT and using runtime IS_INTEGER/IS_DOUBLE checks.
            arg_type = snowpark_typed_args[0].typ
            if isinstance(arg_type, _IntegralType):
                result_exp = snowpark_fn.to_char(
                    snowpark_fn.cast(snowpark_args[0], LongType()),
                    format_string,
                )
            elif isinstance(arg_type, (FloatType, DoubleType, DecimalType)):
                # Non-integral numeric types: truncate toward zero, then cast to long.
                # PySpark uses Java's (long) cast which truncates toward zero,
                # not FLOOR (which rounds toward negative infinity).
                result_exp = snowpark_fn.to_char(
                    snowpark_fn.cast(
                        snowpark_fn.function("TRUNCATE")(
                            snowpark_args[0], snowpark_fn.lit(0)
                        ),
                        LongType(),
                    ),
                    format_string,
                )
            elif isinstance(arg_type, BooleanType):
                # PySpark hex(boolean) encodes the strings "true"/"false" as hex.
                result_exp = snowpark_fn.function("HEX_ENCODE")(
                    snowpark_fn.cast(snowpark_args[0], StringType())
                )
            else:
                # StringType, BinaryType
                result_exp = snowpark_fn.function("HEX_ENCODE")(*snowpark_args)
            result_type = FieldType(StringType(), _unary_nullable(snowpark_typed_args))
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
            result_type = FieldType(BinaryType(), nullable=False)
        case "hll_sketch_estimate":
            result_exp = snowpark_fn.call_function(
                "DATASKETCHES_HLL_ESTIMATE", snowpark_args[0]
            ).cast(LongType())
            result_type = FieldType(LongType(), _unary_nullable(snowpark_typed_args))
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

            result_type = FieldType(BinaryType(), nullable=False)
        case "hll_union":
            # TODO(SNOW-1974083): Snowflake lacks scalar hll_union; uses SQL UDF workaround instead of native hll_combine
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

            result_type = FieldType(
                BinaryType(),
                nullable=_any_arg_nullable(snowpark_typed_args),
            )
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
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
        case "hypot":
            spark_function_name = (
                f"HYPOT({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
            )
            result_exp = snowpark_fn.sqrt(
                snowpark_args[0] * snowpark_args[0]
                + snowpark_args[1] * snowpark_args[1]
            )
            result_exp = TypedColumn(
                result_exp,
                lambda: [
                    FieldType(DoubleType(), _binary_nullable(snowpark_typed_args))
                ],
            )
        case "ilike":
            _validate_arity([2, 3])
            ilike = snowpark_fn.builtin("ilike")
            ilike_args = list(snowpark_args)
            if len(ilike_args) == 3:
                ilike_args[1] = _validate_like_pattern_at_plan_or_runtime(
                    exp.unresolved_function.arguments[1],
                    exp.unresolved_function.arguments[2],
                    ilike_args[0],
                    ilike_args[1],
                    ilike_args[2],
                )
                result_exp = ilike(*ilike_args)
            else:
                result_exp = ilike(ilike_args[0], ilike_args[1], snowpark_fn.lit("\\"))
            spark_function_name = (
                f"ilike({snowpark_arg_names[0]}, {snowpark_arg_names[1]})"
            )
            result_exp = TypedColumn(
                result_exp,
                lambda: [
                    FieldType(BooleanType(), _binary_nullable(snowpark_typed_args))
                ],
            )
        case "in":
            spark_function_name = f"({snowpark_arg_names[0] if not snowpark_arg_names[0] in ['True', 'False'] else snowpark_arg_names[0].lower()} IN ({', '.join(snowpark_arg_names[1:])}))"
            # Type checking for IN operator
            left_type = snowpark_typed_args[0].typ
            right_types = [arg.typ for arg in snowpark_typed_args[1:]]

            # Check if all types are the same or compatible
            all_types = [left_type] + right_types
            type_names = []

            for i, typ in enumerate(all_types):
                try:
                    spark_type = map_snowpark_to_pyspark_types(typ)
                    type_names.append(f'"{spark_type.simpleString().upper()}"')
                except Exception:
                    if typ is None:
                        # Diagnostic only: typ is None when a column type was unresolvable
                        # upstream (see _resolve_column_types in map_column_ops). Emit
                        # telemetry to confirm in production whether this path is hit, then
                        # fall through to the original behavior (which raises
                        # 'NoneType' object has no attribute 'simple_string') so we can
                        # observe whether the issue persists before attempting a patch.
                        arg_name = (
                            snowpark_arg_names[i]
                            if i < len(snowpark_arg_names)
                            else f"arg_{i}"
                        )
                        telemetry.send_null_type_fallback_telemetry(
                            data={"arg_name": arg_name},
                            plan_id=get_current_plan_id(),
                            source="map_unresolved_function/in",
                        )
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
                nullable = _any_arg_nullable(snowpark_typed_args)
            except TypeError:
                left_col = snowpark_typed_args[0]
                left_coerced, right_coerced, nullable = _coerce_for_comparison(
                    left_col, snowpark_typed_args[1]
                )
                result_exp = left_coerced == right_coerced
                for right_col in snowpark_typed_args[2:]:
                    (
                        left_coerced,
                        right_coerced,
                        force_nullable,
                    ) = _coerce_for_comparison(left_col, right_col)
                    nullable = nullable or force_nullable
                    result_exp = result_exp | (left_coerced == right_coerced)

            result_type = FieldType(BooleanType(), nullable=nullable)
        case "initcap":
            result_exp = snowpark_fn.initcap(snowpark_args[0], snowpark_fn.lit(" "))
            result_type = FieldType(StringType(), _unary_nullable(snowpark_typed_args))
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
            field_temporal_types = [
                # TimestampType includes LTZ/NTZ variants; only top-level UDTF
                # outputs need Python temporal objects. Nested arrays/maps/structs
                # are returned unchanged to preserve existing structured output.
                "timestamp"
                if isinstance(f.datatype, TimestampType)
                else "date"
                if isinstance(f.datatype, DateType)
                else None
                for f in input_type.element_type.fields
            ]

            def _coerce_inline_temporal_value(value, temporal_type):
                if value is None:
                    return None
                if temporal_type is None:
                    return value

                if temporal_type == "timestamp":
                    if isinstance(value, datetime.datetime):
                        return value
                    if isinstance(value, datetime.date):
                        return datetime.datetime.combine(value, datetime.time())
                    if isinstance(value, str):
                        timestamp_value = value.strip()
                        if timestamp_value.endswith("Z"):
                            timestamp_value = f"{timestamp_value[:-1]}+00:00"
                        if len(timestamp_value) >= 6 and timestamp_value[-6] == " ":
                            timestamp_value = f"{timestamp_value[:-6]}{timestamp_value[-6:].replace(' ', '')}"
                        # Python 3.10 fromisoformat doesn't accept compact tz
                        # offsets like "-0500"; insert colon to get "-05:00".
                        if (
                            len(timestamp_value) >= 5
                            and timestamp_value[-5] in ("+", "-")
                            and timestamp_value[-4:].isdigit()
                        ):
                            timestamp_value = (
                                f"{timestamp_value[:-2]}:{timestamp_value[-2:]}"
                            )
                        parsed = datetime.datetime.fromisoformat(timestamp_value)
                        if parsed.tzinfo is not None:
                            parsed = parsed.replace(tzinfo=None)
                        return parsed

                if temporal_type == "date":
                    if isinstance(value, datetime.datetime):
                        return value.date()
                    if isinstance(value, datetime.date):
                        return value
                    if isinstance(value, str):
                        return datetime.date.fromisoformat(value.strip())

                return value

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
                                yield tuple(
                                    _coerce_inline_temporal_value(
                                        el.get(k), temporal_type
                                    )
                                    for k, temporal_type in zip(
                                        field_names, field_temporal_types
                                    )
                                )

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
            result_type = FieldType(StringType(), nullable=False)
            spark_function_name = "input_file_name()"
        case "charindex":
            if len(snowpark_args) == 3:
                substr, value, start_pos = snowpark_args
                result_exp = (
                    snowpark_fn.when(snowpark_fn.is_null(start_pos), snowpark_fn.lit(0))
                    .when(
                        start_pos < 1,
                        snowpark_fn.when(
                            snowpark_fn.is_null(substr) | snowpark_fn.is_null(value),
                            snowpark_fn.lit(None),
                        ).otherwise(snowpark_fn.lit(0)),
                    )
                    .otherwise(snowpark_fn.charindex(substr, value, start_pos))
                )
            else:
                result_exp = snowpark_fn.charindex(*snowpark_args)
            result_type = IntegerType()
            result_exp = TypedColumn(
                snowpark_fn.cast(result_exp, result_type),
                lambda: [
                    FieldType(result_type, _binary_nullable(snowpark_typed_args[:2]))
                ],
            )
        case "instr":
            result_exp = snowpark_fn.charindex(snowpark_args[1], snowpark_args[0])
            # Spark 3.5.3: StringInstr defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/stringExpressions.scala#L1332
            result_type = IntegerType()
            result_exp = TypedColumn(
                snowpark_fn.cast(result_exp, result_type),
                lambda: [FieldType(result_type, _binary_nullable(snowpark_typed_args))],
            )
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
            result_type = FieldType(BooleanType(), nullable=False)
        case "isnotnull":
            spark_function_name = f"({snowpark_arg_names[0]} IS NOT NULL)"
            in_sql = get_in_subquery_sql(snowpark_args[0])
            if in_sql:
                result_exp = snowpark_fn.expr(f"({in_sql}) IS NOT NULL")
            else:
                result_exp = snowpark_args[0].isNotNull()
            result_type = FieldType(BooleanType(), nullable=False)
        case "isnull":
            spark_function_name = f"({snowpark_arg_names[0]} IS NULL)"
            in_sql = get_in_subquery_sql(snowpark_args[0])
            if in_sql:
                result_exp = snowpark_fn.expr(f"({in_sql}) IS NULL")
            else:
                result_exp = snowpark_args[0].isNull()
            result_type = FieldType(BooleanType(), nullable=False)
        case "java_method" | "reflect":
            # Spark requires the class and method arguments to be foldable string
            # literals and rejects column expressions at analysis time. Resolving
            # them to constant literals here also ensures no row-dependent value can
            # drive the reflection UDF.
            class_name = snowpark_fn.lit(
                _resolve_foldable_string_expression(
                    snowpark_args[0],
                    snowpark_arg_names[0],
                    spark_function_name,
                    session,
                )
            )
            method_name = snowpark_fn.lit(
                _resolve_foldable_string_expression(
                    snowpark_args[1],
                    snowpark_arg_names[1],
                    spark_function_name,
                    session,
                )
            )
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
            result_exp = TypedColumn(
                result_exp.cast(result_type),
                lambda: [FieldType(result_type, nullable=True)],
            )
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
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
            result_type = FieldType(DateType(), _unary_nullable(snowpark_typed_args))
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [
                    FieldType(
                        snowpark_typed_args[0].typ,
                        nullable=_all_args_nullable(snowpark_typed_args),
                    )
                ],
            )
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
            result_type = FieldType(
                StringType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
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
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
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
            result_type = FieldType(
                IntegerType(),
                nullable=_any_arg_nullable(snowpark_typed_args),
            )
            result_exp = snowpark_fn.cast(result_exp, result_type.datatype)
        case "like":
            like_args = list(snowpark_args)
            if len(like_args) == 3:
                like_args[1] = _validate_like_pattern_at_plan_or_runtime(
                    exp.unresolved_function.arguments[1],
                    exp.unresolved_function.arguments[2],
                    like_args[0],
                    like_args[1],
                    like_args[2],
                )
            result_exp = snowpark_fn.call_function("like", *like_args)
            result_type = FieldType(
                BooleanType(), _binary_nullable(snowpark_typed_args)
            )
            spark_function_name = (
                f"{snowpark_arg_names[0]} LIKE {snowpark_arg_names[1]}"
            )
        case "likeall":
            spark_function_name = f"likeall({snowpark_arg_names[0]})"
            result_exp = _like_util(snowpark_args[0], snowpark_args[1:], mode="all")
            result_type = BooleanType()
        case "likeany":
            spark_function_name = f"likeany({snowpark_arg_names[0]})"
            result_exp = _like_util(snowpark_args[0], snowpark_args[1:], mode="any")
            result_type = BooleanType()
        case "ln":
            result_exp = snowpark_fn.when(
                snowpark_args[0] <= 0, snowpark_fn.lit(None)
            ).otherwise(snowpark_fn.ln(snowpark_args[0]))
            result_type = DoubleType()
        case "localtimestamp":
            result_type = FieldType(
                TimestampType(TimestampTimeZone.NTZ), nullable=False
            )
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
            result_type = FieldType(
                IntegerType(), _binary_nullable(snowpark_typed_args)
            )
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "log1p":
            spark_function_name = f"LOG1P({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                snowpark_args[0] <= -1, snowpark_fn.lit(None)
            ).otherwise(snowpark_fn.ln(snowpark_args[0] + snowpark_fn.lit(1.0)))
            result_type = DoubleType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "log2":
            spark_function_name = f"LOG2({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                snowpark_args[0] <= 0, snowpark_fn.lit(None)
            ).otherwise(snowpark_fn.log(2.0, snowpark_args[0]))
            result_type = DoubleType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "lower" | "lcase":
            result_exp = snowpark_fn.lower(snowpark_args[0])
            result_type = FieldType(StringType(), _unary_nullable(snowpark_typed_args))
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

            result_type = FieldType(
                StringType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
        case "ltrim" | "rtrim":
            function_name_argument = (
                "TRAILING" if function_name == "rtrim" else "LEADING"
            )
            if len(snowpark_args) == 2:
                # Only possible using SQL
                spark_function_name = f"TRIM({function_name_argument} {snowpark_arg_names[1]} FROM {snowpark_arg_names[0]})"
            result_exp = snowpark_fn.ltrim(*snowpark_args)
            result_type = FieldType(
                StringType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
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
                result_type = FieldType(
                    BinaryType(),
                    nullable=_any_arg_nullable(snowpark_typed_args),
                )
            else:
                if function_name == "ltrim":
                    result_exp = snowpark_fn.ltrim(*snowpark_args)
                    result_type = FieldType(
                        StringType(),
                        nullable=_any_arg_nullable(snowpark_typed_args),
                    )
                elif function_name == "rtrim":
                    result_exp = snowpark_fn.rtrim(*snowpark_args)
                    result_type = FieldType(
                        StringType(),
                        nullable=_any_arg_nullable(snowpark_typed_args),
                    )
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
            result_type = FieldType(
                DayTimeIntervalType(),
                nullable=_any_arg_nullable(snowpark_typed_args),
            )
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
            result_type = FieldType(
                YearMonthIntervalType(), _binary_nullable(snowpark_typed_args)
            )
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
                result_type = FieldType(MapType(NullType(), NullType()), nullable=False)
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

                def _guarded_key(
                    idx: int, otherwise: Column, err_type: DataType | None = None
                ) -> Column:
                    # NULL keys are illegal; raise lazily (the XP UDF only runs on a
                    # null key, so the happy path pays no UDF cost).
                    err_type = err_type or VariantType()
                    return snowpark_fn.when(
                        snowpark_fn.is_null(snowpark_args[idx]),
                        _raise_error_helper(err_type)(
                            snowpark_fn.lit(
                                "[NULL_MAP_KEY] Cannot use null as map key."
                            )
                        ),
                    ).otherwise(otherwise)

                def _map_value(idx: int) -> Column:
                    # null values are stored as json null
                    return snowpark_fn.nvl(
                        snowpark_fn.cast(snowpark_args[idx], VariantType()),
                        snowpark_fn.parse_json(snowpark_fn.lit("null")),
                    )

                key_indices = range(0, num_args, 2)

                def _keys_literal_and_distinct() -> bool:
                    lits = [snowpark_args[i]._expression for i in key_indices]
                    if not all(isinstance(e, Literal) for e in lits):
                        return False
                    try:
                        values = [e.value for e in lits]
                        return len(values) == len(set(values))
                    except TypeError:  # unhashable literal -> not provably distinct
                        return False

                # Use OBJECT_CONSTRUCT_KEEP_NULL (one flat call) only when a runtime
                # duplicate key is impossible: a single pair, or all-literal distinct
                # keys. It throws on duplicates regardless of allow_duplicate_keys, so
                # fall back to the OBJECT_INSERT loop (whose 4th arg picks the dedup
                # policy) when duplicates are possible.
                if num_args == 2 or _keys_literal_and_distinct():
                    kv_args = []
                    for i in key_indices:
                        # Keys must be VARCHAR; route through VARIANT so stringification
                        # matches the OBJECT_INSERT path (e.g. NUMBER(2,1) 1.0 -> "1").
                        # err_type=StringType() matches the otherwise branch type.
                        str_key = _guarded_key(
                            i,
                            snowpark_fn.cast(
                                snowpark_fn.to_variant(snowpark_args[i]), StringType()
                            ),
                            StringType(),
                        )
                        kv_args.append(str_key)
                        kv_args.append(_map_value(i + 1))
                    result_exp = snowpark_fn.object_construct_keep_null(*kv_args)
                else:
                    # initialize map with empty object
                    result_exp = snowpark_fn.object_construct()
                    # insert key-value pairs, null values are converted to json null
                    for i in key_indices:
                        result_exp = snowpark_fn.object_insert(
                            result_exp,
                            _guarded_key(i, snowpark_args[i]),
                            _map_value(i + 1),
                            snowpark_fn.lit(allow_duplicate_keys),
                        )

                value_contains_null = any(
                    snowpark_typed_args[i].nullable for i in range(1, num_args, 2)
                )
                dt = MapType(
                    key_type,
                    value_type,
                    value_contains_null=_inner_nullable(value_contains_null),
                )
                result_exp = TypedColumn(
                    snowpark_fn.cast(result_exp, dt),
                    lambda dt=dt: [FieldType(dt, nullable=False)],
                )
        case "map_concat":
            allow_duplicate_keys = (
                global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            )

            key_type = _find_common_type(
                list(map(lambda x: x.typ.key_type, snowpark_typed_args))
            )
            value_type = _find_common_type(
                list(map(lambda x: x.typ.value_type, snowpark_typed_args))
            )

            # Native object merge: fold all input maps' key/value pairs into one
            # OBJECT via REDUCE + OBJECT_INSERT, replacing the per-row Python UDF.
            # Each map is cast to OBJECT so OBJECT_KEYS/GET work for both MAP and
            # semi-structured OBJECT inputs.
            analyzer = Session.get_active_session()._analyzer

            def to_sql(col: Column) -> str:
                return analyzer.analyze(col._expression, defaultdict())

            arg_sqls = [f"({to_sql(arg)})::OBJECT" for arg in snowpark_args]

            # Entry array: [{k, v}, ...] across all maps, preserving JSON-null
            # values via OBJECT_CONSTRUCT_KEEP_NULL. The object is carried in the
            # REDUCE seed (acc:o) and read back inside the lambda, so the argument's
            # SQL is never embedded in a lambda body. That matters when an argument
            # is itself a non-SQL UDF (e.g. map_from_arrays) or an aggregate, which
            # Snowflake forbids inside a lambda expression.
            entries_sql = ", ".join(
                f"reduce(object_keys({s}), "
                f"object_construct_keep_null('o', to_variant({s}), 'e', array_construct()), "
                f"(acc, k) -> object_insert(acc, 'e', array_append(acc:e, "
                f"object_construct_keep_null('k', k, 'v', get(acc:o, to_varchar(k)))), true)):e"
                for s in arg_sqls
            )
            entry_array_sql = f"array_flatten(array_construct({entries_sql}))"

            # Last value wins on collision; for the EXCEPTION policy the dup check
            # below raises before the merge result is ever observed, so OBJECT_INSERT
            # with the update flag is correct for both policies.
            merge_sql = (
                f"reduce({entry_array_sql}, object_construct(), "
                f"(acc, e) -> object_insert(acc, e:k, "
                f"nvl(e:v::variant, parse_json('null')), true))"
            )

            null_guard_sql = " OR ".join(f"{s} IS NULL" for s in arg_sqls)

            if allow_duplicate_keys:
                merged = snowpark_fn.sql_expr(
                    f"CASE WHEN {null_guard_sql} THEN NULL ELSE {merge_sql} END"
                )
            else:
                # EXCEPTION policy: a cross-map duplicate key is an error. Detect it
                # by comparing total vs distinct key counts, then raise
                # DUPLICATE_KEY_FOUND_ERROR_TEMPLATE as a Spark SparkRuntimeException
                # (via _raise_error_helper). first_dup_sql recovers the offending key.
                all_keys_sql = (
                    "array_flatten(array_construct("
                    + ", ".join(f"object_keys({s})" for s in arg_sqls)
                    + "))"
                )
                first_dup_sql = (
                    f"reduce({all_keys_sql}, object_construct('seen', array_construct()), "
                    f"(acc, k) -> iff(acc:dup IS NOT NULL, acc, "
                    f"iff(array_contains(k::variant, acc:seen), "
                    f"object_insert(acc, 'dup', k, true), "
                    f"object_insert(acc, 'seen', array_append(acc:seen, k), true)))):dup::string"
                )
                # Splice the recovered dup key into the message via SQL concatenation
                # so first_dup_sql stays executable SQL; only the literal prefix/suffix
                # are quote-escaped.
                msg_prefix, msg_suffix = DUPLICATE_KEY_FOUND_ERROR_TEMPLATE.split(
                    "{key}"
                )
                prefix_lit = msg_prefix.replace("'", "''")
                suffix_lit = msg_suffix.replace("'", "''")
                dup_message_sql = (
                    f"'{prefix_lit}' || ({first_dup_sql}) || '{suffix_lit}'"
                )
                raise_dup = _raise_error_helper(VariantType(), SparkRuntimeException)(
                    snowpark_fn.sql_expr(dup_message_sql)
                )
                raise_dup_sql = to_sql(raise_dup)
                has_dup_sql = (
                    f"array_size(array_distinct({all_keys_sql})) "
                    f"< array_size({all_keys_sql})"
                )
                merged = snowpark_fn.sql_expr(
                    f"CASE WHEN {null_guard_sql} THEN NULL "
                    f"WHEN {has_dup_sql} THEN {raise_dup_sql} "
                    f"ELSE {merge_sql} END"
                )

            result_exp = snowpark_fn.cast(merged, MapType(key_type, value_type))
            value_contains_null = any(
                a.typ.value_contains_null
                for a in snowpark_typed_args
                if isinstance(a.typ, MapType)
            )
            result_type = FieldType(
                MapType(
                    key_type,
                    value_type,
                    value_contains_null=_inner_nullable(value_contains_null),
                ),
                nullable=_any_arg_nullable(snowpark_typed_args),
            )
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
            raw_type = ArrayType(
                StructType(
                    [
                        StructField(
                            "key",
                            key_type,
                            nullable=_inner_nullable(False),
                            _is_column=False,
                        ),
                        StructField(
                            "value",
                            value_type,
                            nullable=_inner_nullable(arg_type.value_contains_null),
                            _is_column=False,
                        ),
                    ]
                ),
                contains_null=_inner_nullable(False),
            )
            result_exp = snowpark_fn.cast(
                snowpark_fn.call_function("MAP_ENTRIES", snowpark_args[0]),
                raw_type,
            )
            result_type = FieldType(raw_type, _unary_nullable(snowpark_typed_args))
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

            # Build the map natively with REDUCE + OBJECT_INSERT instead of a per-row
            # Python UDF: walk an index range, inserting keys[i]/values[i]. OBJECT_INSERT's
            # 4th arg is the dedup policy (false=raise on dup, true=LAST_WIN). The
            # ARRAY_GENERATE_RANGE index is VARIANT, so cast to int for subscripting.
            keys_array = snowpark_fn.cast(snowpark_args[0], ArrayType())
            values_array = snowpark_fn.cast(snowpark_args[1], ArrayType())
            keys_size = snowpark_fn.function("array_size")(keys_array)
            values_size = snowpark_fn.function("array_size")(values_array)

            # Carry the source arrays in the REDUCE seed (evaluated outside the
            # lambda) and read them back as accumulator fields, so an aggregate input
            # such as COLLECT_LIST/ARRAY_AGG is never embedded inside the lambda body
            # (Snowflake rejects "ARRAY_AGG ... not allowed inside lambda expression").
            # acc:k / acc:v hold the key/value arrays; acc:m accumulates the result.
            seed = snowpark_fn.function("object_construct_keep_null")(
                snowpark_fn.lit("k"),
                keys_array,
                snowpark_fn.lit("v"),
                values_array,
                snowpark_fn.lit("m"),
                snowpark_fn.object_construct(),
            )
            reduce_lambda = (
                "(acc, i) -> object_insert(acc, 'm', object_insert("
                "acc:m, acc:k[i::int], "
                "nvl(acc:v[i::int]::variant, parse_json('null')), "
                f"{str(allow_duplicate_keys).lower()}), true)"
            )
            reduce_result = snowpark_fn.get(
                snowpark_fn.function("reduce")(
                    snowpark_fn.function("array_generate_range")(
                        snowpark_fn.lit(0),
                        keys_size,
                        snowpark_fn.lit(1),
                    ),
                    seed,
                    snowpark_fn.sql_expr(reduce_lambda),
                ),
                snowpark_fn.lit("m"),
            )

            # Spark errors on length mismatch (SparkRuntimeException) and null keys
            # (NULL_MAP_KEY); mirror both via raise-error helpers (as `map` /
            # `map_from_entries` do). A null input array yields a null map.
            length_mismatch = keys_size != values_size
            length_error = _raise_error_helper(VariantType())(
                snowpark_fn.lit(
                    "The key array and value array of MapData "
                    "must have the same length."
                )
            )
            has_null_key = (
                snowpark_fn.function("array_size")(
                    snowpark_fn.function("filter")(
                        keys_array,
                        snowpark_fn.sql_expr("k -> k IS NULL"),
                    )
                )
                > 0
            )
            null_key_error = _raise_error_helper(VariantType())(
                snowpark_fn.lit("[NULL_MAP_KEY] Cannot use null as map key.")
            )

            guarded_result = (
                snowpark_fn.when(
                    snowpark_fn.is_null(keys_array) | snowpark_fn.is_null(values_array),
                    snowpark_fn.lit(None),
                )
                .when(length_mismatch, length_error)
                .when(has_null_key, null_key_error)
                .otherwise(reduce_result)
            )

            result_exp = snowpark_fn.cast(
                guarded_result,
                MapType(
                    key_type,
                    value_type,
                    value_contains_null=_inner_nullable(values_type.contains_null),
                ),
            )
            result_type = FieldType(
                MapType(
                    key_type,
                    value_type,
                    value_contains_null=_inner_nullable(values_type.contains_null),
                ),
                _binary_nullable(snowpark_typed_args),
            )
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
            result_type = FieldType(
                ArrayType(arg_type.key_type),
                _unary_nullable(snowpark_typed_args),
            )
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

            nullable = _unary_nullable(snowpark_typed_args)
            if isinstance(arg_type, NullType):
                result_exp = snowpark_fn.lit(None)
                result_type = FieldType(ArrayType(NullType()), nullable)
            else:
                entries = snowpark_fn.call_function("MAP_ENTRIES", snowpark_args[0])
                result_exp = snowpark_fn.cast(
                    snowpark_fn.function("transform")(
                        entries, snowpark_fn.sql_expr("x -> x:value")
                    ),
                    ArrayType(arg_type.value_type),
                )
                result_type = FieldType(ArrayType(arg_type.value_type), nullable)
        case "mask":
            number_of_args = len(snowpark_args)
            result_exp = snowpark_args[0]  # First arg is always the input string

            # Initialize with default values
            upper_char = "X"
            lower_char = "x"
            digit_char = "n"
            other_char = None

            upper_char_arg_name = "X"
            lower_char_arg_name = "x"
            digit_char_arg_name = "n"
            other_char_arg_name = "NULL"

            col_arg_names = [None, "upperChar", "lowerChar", "digitChar", "otherChar"]
            function_call = f"mask({', '.join(snowpark_arg_names)})"

            # Process remaining arguments
            literal_values = [None]
            for i in range(1, number_of_args):
                arg_name = snowpark_arg_names[i]
                arg_value = snowpark_args[i]
                arg_type = snowpark_typed_args[i].typ

                if not isinstance(arg_type, (StringType, NullType)):
                    exception = AnalysisException(
                        f"""[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{function_call}" due to data type mismatch: Parameter {i + 1} requires the "STRING" type, however "{arg_name}" has the type "{arg_type.simpleString().upper()}".;"""
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception

                # For named arguments and literals, we want to extract the actual literal value
                if isinstance(arg_value, snowpark.Column):
                    literal_value = _resolve_foldable_string_expression(
                        arg_col=arg_value,
                        arg_name=arg_name,
                        spark_function_name=function_call,
                        session=session,
                    )
                else:
                    literal_value = arg_value
                literal_values.append(literal_value)

                # Check if this is a named argument
                is_not_named = arg_name not in col_arg_names
                char_arg_name = arg_name if is_not_named else (literal_value or "NULL")
                if arg_name == "upperChar" or (i == 1 and is_not_named):
                    upper_char = literal_value
                    upper_char_arg_name = char_arg_name
                elif arg_name == "lowerChar" or (i == 2 and is_not_named):
                    lower_char = literal_value
                    lower_char_arg_name = char_arg_name
                elif arg_name == "digitChar" or (i == 3 and is_not_named):
                    digit_char = literal_value
                    digit_char_arg_name = char_arg_name
                elif arg_name == "otherChar" or (i == 4 and is_not_named):
                    other_char = literal_value
                    other_char_arg_name = char_arg_name

            spark_function_name = f"mask({snowpark_arg_names[0]}, {upper_char_arg_name}, {lower_char_arg_name}, {digit_char_arg_name}, {other_char_arg_name})"

            # Sanity check for arguments
            for i in range(1, number_of_args):
                arg_name = snowpark_arg_names[i]
                arg_type = snowpark_typed_args[i].typ
                literal_value = literal_values[i]
                if isinstance(arg_type, NullType) or (
                    isinstance(literal_value, str) and len(literal_value) == 1
                ):
                    pass
                elif literal_value is not None and len(literal_value) != 1:
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
            patterns = ["[A-Z]", "[a-z]", r"\d", "[^a-zA-Z0-9]"]
            replacements = [upper_char, lower_char, digit_char, other_char]

            # To avoid replacement character collisions we need to replace them with unique tags first.
            for tag, pattern, replacement_char in zip(tags, patterns, replacements):
                result_exp = (
                    result_exp
                    if replacement_char is None
                    else snowpark_fn.regexp_replace(result_exp, pattern, tag)
                )

            for tag, replacement_char in zip(tags, replacements):
                result_exp = (
                    result_exp
                    if replacement_char is None
                    else snowpark_fn.regexp_replace(result_exp, tag, replacement_char)
                )
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
            result_type = FieldType(
                StringType(32), _unary_nullable(snowpark_typed_args)
            )
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
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
        case "mode":
            result_exp = TypedColumn(
                snowpark_fn.mode(snowpark_args[0]),
                lambda: snowpark_typed_args[0].types,
            )
        case "monotonically_increasing_id":
            result_exp = snowpark_fn.monotonically_increasing_id()
            result_type = FieldType(LongType(), nullable=False)
        case "distributed_sequence_id":
            # PySpark's distributed_sequence_id generates consecutive IDs starting from 0
            # Use row_number() over monotonically_increasing_id() to ensure consecutiveness, then subtract 1
            from snowflake.snowpark import Window

            window_spec = Window.order_by(snowpark_fn.monotonically_increasing_id())
            result_exp = snowpark_fn.row_number().over(window_spec) - 1
            result_type = FieldType(LongType(), nullable=False)
        case "month":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.month(
                    snowpark_fn.builtin("try_to_date")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.month(snowpark_fn.to_date(snowpark_args[0]))
            # Spark 3.5.3: Month extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
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
            result_type = FieldType(
                DoubleType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
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
            field_nullables = []
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
                field_nullables.append(
                    field_value_typed_col.nullable
                    if field_value_typed_col.field_types
                    else True
                )

            # Before calling object_construct_keep_null, convert struct field values to variants
            # to handle nested structs properly
            converted_args = []
            for i, typed_arg in enumerate(expanded_typed_args):
                arg = typed_arg.col
                if i % 2 == 1:  # This is a field value (odd indices)
                    field_type = field_types[i // 2]
                    if isinstance(field_type, (StructType, ArrayType, MapType)):
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
                    StructField(
                        name, typ, nullable=_inner_nullable(nul), _is_column=False
                    )
                    for name, typ, nul in zip(field_names, field_types, field_nullables)
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
            result_type = FieldType(schema, nullable=False)
        case "nanvl":
            arg1_is_nan = snowpark_fn.equal_nan(snowpark_args[0])
            result_exp = snowpark_fn.when(arg1_is_nan, snowpark_args[1]).otherwise(
                snowpark_args[0]
            )
            result_type = FieldType(DoubleType(), _binary_nullable(snowpark_typed_args))
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
                    # In non-ANSI mode, Spark casts the string to Double using try_cast semantics
                    # (returns NULL only if the cast fails, not unconditionally), then negates
                    result_exp = snowpark_fn.try_cast(
                        snowpark_args[0], DoubleType()
                    ) * snowpark_fn.lit(-1)
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
                FieldType(
                    snowpark_typed_args[0].typ,
                    _unary_nullable(snowpark_typed_args),
                )
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "not" | "!":
            spark_function_name = f"(NOT {snowpark_arg_names[0]})"
            result_exp = ~snowpark_args[0]
            in_sql = get_in_subquery_sql(snowpark_args[0])
            if in_sql:
                _tag_in_subquery_sql(result_exp, f"NOT ({in_sql})")
            result_type = FieldType(BooleanType(), _unary_nullable(snowpark_typed_args))
        case "notlikeany":
            spark_function_name = f"notlikeany({snowpark_arg_names[0]})"
            result_exp = _like_util(
                snowpark_args[0], snowpark_args[1:], mode="any", negate=True
            )
            result_type = BooleanType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "notlikeall":
            spark_function_name = f"notlikeall({snowpark_arg_names[0]})"
            result_exp = _like_util(
                snowpark_args[0], snowpark_args[1:], mode="all", negate=True
            )
            result_type = BooleanType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
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
            result_exp = _resolve_aggregate_exp(
                result_exp, IntegerType(), nullable=False
            )
        case "nullif":
            result_exp = TypedColumn(
                snowpark_fn.call_function("nullif", *snowpark_args),
                lambda: snowpark_typed_args[0].types,
            )
        case "nvl" | "ifnull":
            _validate_arity(2)
            result_type = _find_common_type([arg.typ for arg in snowpark_typed_args])
            result_exp = snowpark_fn.nvl(
                *[
                    _coerce_null_typed_expr(
                        col, snowpark_typed_args[i].typ, result_type
                    )
                    if isinstance(snowpark_typed_args[i].typ, NullType)
                    or _is_null_typed_container(snowpark_typed_args[i].typ)
                    else col.cast(result_type)
                    for i, col in enumerate(snowpark_args)
                ]
            )
        case "nvl2":
            _validate_arity(3)
            result_type = _find_common_type(
                [arg.typ for arg in snowpark_typed_args[1:]]
            )
            result_exp = snowpark_fn.call_function(
                "nvl2",
                snowpark_args[0],
                *[
                    _coerce_null_typed_expr(
                        col, snowpark_typed_args[i + 1].typ, result_type
                    )
                    if isinstance(snowpark_typed_args[i + 1].typ, NullType)
                    or _is_null_typed_container(snowpark_typed_args[i + 1].typ)
                    else col.cast(result_type)
                    for i, col in enumerate(snowpark_args[1:])
                ],
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
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
        case "or":
            spark_function_name = (
                f"({snowpark_arg_names[0]} OR {snowpark_arg_names[1]})"
            )
            result_exp = snowpark_args[0] | snowpark_args[1]
            result_type = FieldType(
                BooleanType(), _binary_nullable(snowpark_typed_args)
            )
        case "overlay":
            length = snowpark_fn.when(
                snowpark_args[3] < 0, snowpark_fn.length(snowpark_args[1])
            ).otherwise(snowpark_args[3])
            result_exp = snowpark_fn.concat(
                snowpark_fn.substring(snowpark_args[0], 1, snowpark_args[2] - 1),
                snowpark_args[1],
                snowpark_fn.substring(snowpark_args[0], snowpark_args[2] + length),
            )
            result_type = FieldType(
                StringType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
        case "parse_url":
            url, part_to_extract = snowpark_args[0], snowpark_args[1]
            key = snowpark_args[2] if len(snowpark_args) > 2 else snowpark_fn.lit(None)

            parsed_url = snowpark_fn.call_function("parse_url", url)
            split_part = snowpark_fn.function("split_part")

            host = snowpark_fn.get(parsed_url, snowpark_fn.lit("host"))
            path = snowpark_fn.get(parsed_url, snowpark_fn.lit("path"))
            scheme = snowpark_fn.get(parsed_url, snowpark_fn.lit("scheme"))
            authority_result = snowpark_fn.nvl(
                snowpark_fn.concat_ws(
                    snowpark_fn.lit(":"),
                    host,
                    snowpark_fn.get(parsed_url, snowpark_fn.lit("port")),
                ),
                host,
            )
            raw_query = snowpark_fn.get(parsed_url, snowpark_fn.lit("query"))
            query_result = snowpark_fn.when(key.is_null(), raw_query,).otherwise(
                # Spark keeps the first value for duplicate query keys. Snowflake's
                # parse_url(...).parameters map keeps the last value, so extract from
                # raw query text first and only fall back to parameters map if needed.
                snowpark_fn.nvl(
                    snowpark_fn.call_function(
                        "regexp_substr",
                        raw_query,
                        snowpark_fn.concat(
                            snowpark_fn.lit("(^|&)"),
                            key,
                            snowpark_fn.lit("=([^&]*)"),
                        ),
                        snowpark_fn.lit(1),
                        snowpark_fn.lit(1),
                        snowpark_fn.lit("e"),
                        snowpark_fn.lit(2),
                    ),
                    snowpark_fn.get(
                        snowpark_fn.get(parsed_url, snowpark_fn.lit("parameters")),
                        key,
                    ),
                )
            )
            file_result = snowpark_fn.concat(
                snowpark_fn.lit("/"),
                snowpark_fn.trim(
                    snowpark_fn.nvl(
                        snowpark_fn.concat_ws(
                            snowpark_fn.lit("?"),
                            path,
                            snowpark_fn.get(parsed_url, snowpark_fn.lit("query")),
                        ),
                        path,
                    ),
                    snowpark_fn.lit("/"),
                ),
            )
            user_info_result = snowpark_fn.when(
                snowpark_fn.contains(host, snowpark_fn.lit("@")),
                split_part(
                    host,
                    snowpark_fn.lit("@"),
                    snowpark_fn.lit(0),
                ),
            ).otherwise(snowpark_fn.lit(None))
            host_result = split_part(host, snowpark_fn.lit("@"), snowpark_fn.lit(-1))
            path_result = snowpark_fn.concat(snowpark_fn.lit("/"), path)

            def _parse_url_part_branch(part_name: str) -> Column:
                match part_name:
                    case "PROTOCOL":
                        return scheme
                    case "REF":
                        return snowpark_fn.get(parsed_url, snowpark_fn.lit("fragment"))
                    case "AUTHORITY":
                        return authority_result
                    case "QUERY":
                        return query_result
                    case "FILE":
                        return snowpark_fn.when(
                            scheme != snowpark_fn.lit("mailto"),
                            file_result,
                        ).otherwise(snowpark_fn.lit(None))
                    case "USERINFO":
                        return user_info_result
                    case "PATH":
                        return snowpark_fn.when(
                            scheme != snowpark_fn.lit("mailto"),
                            path_result,
                        ).otherwise(snowpark_fn.lit(None))
                    case "HOST":
                        return host_result
                    case _:
                        return snowpark_fn.lit(None)

            # Fast path: when part_to_extract is a literal we can select one branch
            # directly instead of building a full CASE/WHEN chain.
            if isinstance(part_to_extract._expression, Literal):
                part_literal = part_to_extract._expression.value
                if (
                    isinstance(part_literal, str)
                    and part_literal == part_literal.upper()
                ):
                    result_exp = _parse_url_part_branch(part_literal)
                else:
                    result_exp = snowpark_fn.lit(None)
            else:
                # Slow path: preserve dynamic-column behavior with CASE/WHEN.
                parse_url_parts = (
                    "PROTOCOL",
                    "REF",
                    "AUTHORITY",
                    "QUERY",
                    "FILE",
                    "USERINFO",
                    "PATH",
                    "HOST",
                )
                result_exp = reduce(
                    lambda case_expr, url_part: case_expr.when(
                        part_to_extract == snowpark_fn.lit(url_part),
                        _parse_url_part_branch(url_part),
                    ),
                    parse_url_parts,
                    snowpark_fn.when(
                        snowpark_fn.upper(part_to_extract) != part_to_extract,
                        snowpark_fn.lit(None),
                    ),
                ).otherwise(snowpark_fn.lit(None))

            result_exp = snowpark_fn.cast(result_exp, StringType())
            result_type = StringType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "percent_rank":
            result_exp = snowpark_fn.percent_rank()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(DoubleType(), nullable=False)]
            )
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
                        element_type=DoubleType(),
                        contains_null=_inner_nullable(False),
                    )
                else:
                    percentage = snowpark_fn.array_construct(percentage).cast(
                        ArrayType(DoubleType())
                    )
                    result_type = DoubleType()

                result_exp = _resolve_aggregate_exp(
                    _percentile_udaf(column_value, percentage, snowpark_args[2]),
                    result_type,
                    nullable=True,
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
                result_type = ArrayType(
                    element_type=DoubleType(), contains_null=_inner_nullable(False)
                )
                result_exp = _resolve_aggregate_exp(
                    result_exp, result_type, nullable=True
                )
                spark_function_name = f"{function_name}({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, 1)"
            else:
                result_exp = snowpark_fn.function("percentile_cont")(
                    _check_percentile_percentage(exp.unresolved_function.arguments[1])
                ).within_group(column_value)
                result_exp = _resolve_aggregate_exp(
                    result_exp, DoubleType(), nullable=True
                )
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
            result_type = FieldType(DoubleType(), nullable=False)
            result_exp = snowpark_fn.lit(math.pi, datatype=DoubleType())
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
                # Snowflake FLATTEN skips SQL NULL array elements (represented as `undefined`).
                # Normalize each element into VARIANT and map SQL NULL -> JSON null so
                # posexplode keeps positional null rows like Spark.
                analyzer = session._analyzer
                arg_sql = analyzer.analyze(snowpark_args[0]._expression, defaultdict())
                normalized_array = snowpark_fn.sql_expr(
                    f"transform({arg_sql}, x -> iff(x is null, parse_json('null'), to_variant(x)))"
                )
                # use call_table_function so we avoid passing in the MODE argument
                result_exp = snowpark_fn.call_table_function(
                    "flatten",
                    input=normalized_array,
                    outer=snowpark_fn.lit(is_nullable),
                )
                # Semi-structured Snowflake ARRAYs have no element type
                # (element_type is None); their elements are variants.
                element_type = input_type.element_type or VariantType()
                # See map_column_ops._resolve_selected_table_function_columns().
                selected_projection_specs = [
                    SelectedProjectionSpec("INDEX", IntegerType()),
                    SelectedProjectionSpec("VALUE", element_type),
                ]
                spark_col_names = ["pos", "col"]
                result_type = [IntegerType(), element_type]
            elif isinstance(input_type, MapType):
                spark_col_names = ["pos", "key", "value"]
                result_type = [
                    LongType(),
                    input_type.key_type,
                    input_type.value_type,
                ]
                analyzer = session._analyzer
                arg_sql = analyzer.analyze(snowpark_args[0]._expression, defaultdict())
                # Build an array of key/value objects so flatten INDEX becomes posexplode pos.
                # Store map values in VARIANT to support nested map value types.
                kv_pairs = snowpark_fn.sql_expr(
                    f"transform(map_keys({arg_sql}), "
                    f"k -> object_construct_keep_null('k', k, 'v', get(to_variant({arg_sql}), to_varchar(k))))"
                )
                result_exp = snowpark_fn.call_table_function(
                    "flatten",
                    input=kv_pairs,
                    outer=snowpark_fn.lit(is_nullable),
                )
                # For map posexplode, INDEX is pos, and VALUE contains an object:
                # {"k": <key>, "v": <value>}. Extract and cast each field.
                selected_projection_specs = [
                    SelectedProjectionSpec("INDEX", LongType()),
                    SelectedProjectionSpec("VALUE", input_type.key_type, "k"),
                    SelectedProjectionSpec("VALUE", input_type.value_type, "v"),
                ]
            else:
                exception = TypeError(
                    f"Data type mismatch: {function_name} requires an array or map input, but got {input_type}."
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
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
            pos_nullable = _binary_nullable(snowpark_typed_args)
            result_type = FieldType(IntegerType(), pos_nullable)
            result_exp = snowpark_fn.cast(result_exp, result_type.datatype)

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
                    # In non-ANSI mode, Spark casts the string to Double using try_cast semantics
                    # (returns NULL only if the cast fails, not unconditionally)
                    result_exp = snowpark_fn.try_cast(snowpark_args[0], DoubleType())
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
                FieldType(
                    snowpark_typed_args[0].typ,
                    _unary_nullable(snowpark_typed_args),
                )
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
            # SNOW-3418191: Snowflake's POWER() propagates NaN for the base
            # but throws on a NaN exponent; only guard the exponent.
            # Skip the guard when the exponent is a non-NaN numeric literal —
            # it can never be NaN, so the CASE WHEN is dead code.
            exp_lit = snowpark_args[1]._expression
            if isinstance(exp_lit, Literal) and not (_is_nan_value(exp_lit.value)):
                result_exp = snowpark_fn.pow(snowpark_args[0], snowpark_args[1])
            else:
                result_exp = snowpark_fn.when(
                    snowpark_fn.equal_nan(
                        snowpark_fn.cast(snowpark_args[1], FloatType())
                    ),
                    NAN,
                ).otherwise(snowpark_fn.pow(snowpark_args[0], snowpark_args[1]))
            result_type = FieldType(DoubleType(), _binary_nullable(snowpark_typed_args))
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "quarter":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.quarter(
                    snowpark_fn.builtin("try_to_date")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.quarter(snowpark_fn.to_date(snowpark_args[0]))
            # Spark 3.5.3: Quarter extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
        case "radians":
            spark_function_name = f"RADIANS({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.radians(*snowpark_args)
            result_type = DoubleType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "raise_error":
            result_type = StringType()
            raise_error = _raise_error_helper(result_type)
            result_exp = raise_error(*snowpark_args)
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(DoubleType(), nullable=False)]
            )
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
            result_type = FieldType(DoubleType(), nullable=False)
        case "rank":
            result_exp = snowpark_fn.rank()
            # IntegerType per Spark's Rank case class which extends AggregateWindowFunction, which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/34d9413ca161f4531544565976a46c6da7d371cd/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/windowExpressions.scala#L626
            result_exp = _resolve_aggregate_exp(
                result_exp, IntegerType(), nullable=False
            )
        case "reduce":
            # Call aggregator provided as a snowpark argument
            result_exp = snowpark_args[0]
            result_type = snowpark_typed_args[0].typ
        case "regexp_count":
            pattern_col, sf_flags = _extract_inline_regex_flags(snowpark_args[1])
            if _has_unsupported_pcre_syntax(snowpark_args[1]):
                regexp_count_udf = register_cached_java_udf(
                    "com.snowflake.snowpark_connect.udfs.RegexpUdfs.regexp_count",
                    ["STRING", "STRING"],
                    "INTEGER",
                )
                count_call = regexp_count_udf(snowpark_args[0], snowpark_args[1])
            elif sf_flags:
                count_call = snowpark_fn.call_function(
                    "regexp_count",
                    snowpark_args[0],
                    pattern_col,
                    snowpark_fn.lit(1),
                    snowpark_fn.lit(sf_flags),
                )
            else:
                count_call = snowpark_fn.regexp_count(
                    snowpark_args[0], snowpark_args[1]
                )
            result_exp = (
                snowpark_fn.when(snowpark_fn.is_null(snowpark_args[0]), None)
                .when(
                    snowpark_args[1] == "",
                    snowpark_fn.length(snowpark_args[0]) + 1,
                )
                .otherwise(count_call)
            )
            result_type = FieldType(
                IntegerType(),
                nullable=_any_arg_nullable(snowpark_typed_args),
            )
            result_exp = snowpark_fn.cast(result_exp, result_type.datatype)
        case "regexp_extract":
            if len(snowpark_args) == 2:
                idx = snowpark_fn.lit(1)
                spark_function_name = spark_function_name[:-1] + ", 1)"
            else:
                idx = snowpark_args[2]
            _validate_regex_group_index(
                snowpark_args[0], snowpark_args[1], idx, "regexp_extract"
            )
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
                            idx,
                        ),
                    ),
                    _raise_error_helper(StringType())(
                        snowpark_fn.lit(
                            "[INVALID_PARAMETER_VALUE.REGEX_GROUP_INDEX] The value of parameter(s) `idx` in `regexp_extract` is invalid."
                        )
                    ),
                )
                .otherwise(
                    snowpark_fn.regexp_extract(snowpark_args[0], snowpark_args[1], idx)
                )
            )

            result_type = FieldType(
                StringType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
        case "regexp_extract_all":
            if len(snowpark_args) == 2:
                idx = snowpark_fn.lit(1)
                spark_function_name = spark_function_name[:-1] + ", 1)"
            else:
                idx = snowpark_args[2]
            _validate_regex_group_index(
                snowpark_args[0], snowpark_args[1], idx, "regexp_extract_all"
            )
            pattern = snowpark_args[1]
            # Snowflake's regexp_extract_all has more arguments, so we need to fill out default values
            # If pattern doesn't match string, return empty string
            #    Else if the matched group returns null, throw exception
            result_exp = snowpark_fn.when(
                snowpark_fn.is_null(snowpark_args[0]), None
            ).when(
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

            group_check = snowpark_fn.is_null(
                snowpark_fn.call_function(
                    "regexp_substr",
                    snowpark_args[0],
                    snowpark_args[1],
                    snowpark_fn.lit(1),
                    snowpark_fn.lit(1),
                    snowpark_fn.lit("c"),
                    idx,
                )
            )

            group_error = _raise_error_helper(ArrayType(StringType()))(
                snowpark_fn.lit(
                    "[INVALID_PARAMETER_VALUE.REGEX_GROUP_INDEX] The value of parameter(s) `idx` in `regexp_extract_all` is invalid."
                )
            )

            extract_exp = snowpark_fn.cast(
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

            num_groups = None
            if isinstance(pattern._expression, Literal):
                pattern_value = pattern._expression.value
                with suppress(re.error):
                    num_groups = re.compile(pattern_value).groups

            if num_groups is not None:
                # optimization: if we can compile the pattern, we can skip one regexp_substr call
                result_exp = result_exp.when(
                    (idx >= 0) & (idx <= num_groups), extract_exp
                ).otherwise(group_error)
            else:
                result_exp = result_exp.when(group_check, group_error).otherwise(
                    extract_exp
                )

            result_type = FieldType(
                ArrayType(StringType()),
                nullable=_any_arg_nullable(snowpark_typed_args),
            )
        case "regexp_instr":
            pattern_col, sf_flags = _extract_inline_regex_flags(snowpark_args[1])
            if sf_flags:
                instr_call = snowpark_fn.call_function(
                    "regexp_instr",
                    snowpark_args[0],
                    pattern_col,
                    snowpark_fn.lit(1),
                    snowpark_fn.lit(1),
                    snowpark_fn.lit(0),
                    snowpark_fn.lit(sf_flags),
                )
                rlike_pattern = pattern_col
            else:
                instr_call = snowpark_fn.call_function(
                    "regexp_instr",
                    snowpark_args[0],
                    snowpark_args[1],
                )
                rlike_pattern = snowpark_args[1]
            result_exp = (
                snowpark_fn.when(snowpark_fn.is_null(snowpark_args[0]), None)
                .when(
                    (snowpark_args[0] == "") & (snowpark_args[0].rlike(rlike_pattern)),
                    1,
                )
                .otherwise(instr_call)
            )

            # Spark 3.5.3: RegExpInStr defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/regexpExpressions.scala#L1078
            result_type = FieldType(
                IntegerType(),
                nullable=_any_arg_nullable(snowpark_typed_args),
            )
            result_exp = snowpark_fn.cast(result_exp, result_type.datatype)
            # if idx was not specified, it defaults to 0 in the column name
            if len(snowpark_args) == 2:
                spark_function_name = spark_function_name[:-1] + ", 0)"
        case "regexp_replace":
            spark_function_name = spark_function_name[:-1] + ", 1)"
            result_exp = snowpark_fn.regexp_replace(*snowpark_args)
            result_type = FieldType(
                StringType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
        case "regexp_substr":
            # in some cases Snowflake returns an empty string instead of null
            # but that also counts as no match, for example regexp_substr('', '$')
            result_exp = snowpark_fn.call_function(
                "nullif",
                snowpark_fn.call_function("regexp_substr", *snowpark_args),
                "",
            )
            result_type = StringType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
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
            result_type = FieldType(StringType(), _binary_nullable(snowpark_typed_args))
        case "replace":
            result_exp = snowpark_fn.replace(*snowpark_args)
            result_type = FieldType(
                StringType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
            if len(snowpark_args) == 2:
                spark_function_name = (
                    f"replace({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, )"
                )
        case "reverse":
            nullable = _unary_nullable(snowpark_typed_args)
            match snowpark_typed_args[0].typ:
                case ArrayType():
                    result_exp = snowpark_fn.function("array_reverse")(snowpark_args[0])
                    result_type = FieldType(snowpark_typed_args[0].typ, nullable)
                case _:
                    result_exp = snowpark_fn.reverse(snowpark_args[0])
                    result_type = FieldType(StringType(), nullable)
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "rint":
            result_exp = snowpark_fn.cast(
                snowpark_fn.round(snowpark_args[0]), DoubleType()
            )
            result_type = DoubleType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "rlike" | "regexp" | "regexp_like":
            # Snowflake's regexp/rlike implicitly anchors the pattern to the beginning and end of the string.
            # Spark matches any substring, so we use regexp_instr to emulate this, except empty inputs,
            # which need to be checked with regexp/rlike.
            # We also handle:
            # - the case where the pattern is an empty string, which Spark treats as .*
            # - the case where the pattern uses embedded flag expressions (such as '(?i)', which Spark treats as case-insensitive)
            text = snowpark_args[0]
            pattern = snowpark_args[1]

            flag_pyspark_regex_pattern = r"\(\?([a-z]+)\)"
            begin_flag_pyspark = "(?"

            # resolve regex pattern and params
            if isinstance(pattern._expression, Literal):
                # Fast path: pattern is a literal, resolve flags and empty-pattern handling at compile time
                pattern_value = pattern._expression.value
                if not pattern_value:
                    regex_pattern = snowpark_fn.lit(
                        ".*" if pattern_value == "" else None
                    )
                    regex_params = snowpark_fn.lit("c")
                elif not pattern_value.startswith(begin_flag_pyspark):
                    regex_pattern = snowpark_fn.lit(pattern_value)
                    regex_params = snowpark_fn.lit("c")
                else:
                    flags = "".join(
                        re.findall(flag_pyspark_regex_pattern, pattern_value)
                    )
                    stripped_pattern = re.sub(
                        flag_pyspark_regex_pattern, "", pattern_value
                    )
                    regex_pattern = snowpark_fn.lit(stripped_pattern)
                    regex_params = snowpark_fn.lit(flags if flags else "c")
            else:
                # Slow path: pattern is a column expression, must handle at runtime
                regex_pattern = (
                    snowpark_fn.when(pattern == "", ".*")
                    .when(
                        pattern.startswith(begin_flag_pyspark),
                        snowpark_fn.regexp_replace(pattern, flag_pyspark_regex_pattern),
                    )
                    .otherwise(pattern)
                )
                regex_params = snowpark_fn.when(
                    pattern.startswith(begin_flag_pyspark),
                    snowpark_fn.array_to_string(
                        snowpark_fn.call_function(
                            "regexp_substr_all",
                            pattern,
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
                snowpark_fn.when(snowpark_fn.is_null(text), None)
                .when(
                    text == "",
                    snowpark_fn.call_function(
                        "rlike", text, regex_pattern, regex_params
                    ),
                )
                .otherwise(
                    snowpark_fn.call_function(
                        "regexp_instr",
                        text,
                        regex_pattern,
                        1,
                        1,
                        0,
                        regex_params,
                    )
                    > 0
                )
            )
            result_type = FieldType(
                BooleanType(), _binary_nullable(snowpark_typed_args)
            )
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
                    attach_custom_error_code(exception, ErrorCodes.ARITHMETIC_OVERFLOW)
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
            result_exp = _resolve_aggregate_exp(
                result_exp, IntegerType(), nullable=False
            )
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

            spark_function_name = f"schema_of_csv({snowpark_arg_names[0]})"

            def _infer_schema_of_csv_str(
                data: str, options: Optional[dict] = None
            ) -> str:
                sep = ","
                if options is not None and isinstance(options, dict):
                    sep = options.get("sep") or sep

                def _get_type(v: str) -> str:
                    if v.lower() in ["true", "false"]:
                        return "BOOLEAN"

                    with suppress(Exception):  # int
                        y = int(v)
                        if str(y) == v:
                            if y < -2147483648 or y > 2147483647:
                                return "BIGINT"
                            return "INT"

                    with suppress(Exception):  # double
                        float(v)
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

            csv_literal = unwrap_literal(exp.unresolved_function.arguments[0])

            # When `options` is provided, fold it at plan time via `collect()`
            # on a 1-row dataframe — PySpark Connect ships it as
            # `create_map(lit(k), lit(v), ...)` so this evaluates to a constant
            # OBJECT and avoids walking the protobuf by hand.
            options_dict: Optional[dict] = None
            match snowpark_typed_args:
                case [_]:
                    pass
                case [_, opts]:
                    opts_col = opts.column(to_semi_structure=True)
                    try:
                        collected = (
                            session.create_dataframe([(1,)])
                            .select(opts_col)
                            .collect()[0][0]
                        )
                    except Exception:
                        exception = AnalysisException(
                            "[INVALID_OPTIONS.NON_MAP_FUNCTION] Invalid options: "
                            "Must use the `map()` function for options."
                        )
                        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                        raise exception
                    import json as _json

                    options_dict = _json.loads(collected)
                case _:
                    exception = ValueError("Unrecognized schema_of_csv parameters")
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception

            try:
                inferred = _infer_schema_of_csv_str(csv_literal, options_dict)
            except Exception as exc:
                attach_custom_error_code(exc, ErrorCodes.INVALID_INPUT)
                raise

            result_exp = snowpark_fn.lit(inferred)
            result_type = FieldType(StringType(), nullable=False)
        case "schema_of_json":
            if (
                exp.unresolved_function.arguments[0].WhichOneof("expr_type")
                != "literal"
            ):
                exception = AnalysisException(
                    f"""[DATATYPE_MISMATCH.NON_FOLDABLE_INPUT] Cannot resolve "schema_of_json({",".join(snowpark_arg_names)})" due to data type mismatch: the input json should be a foldable "STRING" expression; however, got "{",".join(snowpark_arg_names)}"."""
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
                raise exception

            def _infer_schema_of_json_str(json_str: str) -> str:
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

            json_literal = unwrap_literal(exp.unresolved_function.arguments[0])

            try:
                inferred = _infer_schema_of_json_str(json_literal)
            except ValueError as exc:
                attach_custom_error_code(exc, ErrorCodes.INVALID_INPUT)
                raise

            result_exp = snowpark_fn.lit(inferred)
            result_type = FieldType(StringType(), nullable=False)
        case "sec":
            spark_function_name = f"SEC({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.when(
                snowpark_fn.is_null(snowpark_args[0]), snowpark_fn.lit(None)
            ).otherwise(
                snowpark_fn.coalesce(
                    _divnull(snowpark_fn.lit(1.0), snowpark_fn.cos(snowpark_args[0])),
                    snowpark_fn.lit(INFINITY),
                )
            )
            result_type = DoubleType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
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
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
        case "sentences":
            sentences_udf = register_cached_java_udf(
                "com.snowflake.snowpark_connect.udfs.SentencesUdf.sentences",
                ["STRING", "STRING", "STRING"],
                "VARIANT",
                packages=["com.snowflake:snowpark:1.15.0"],
            )

            result_type = ArrayType(
                ArrayType(StringType(), contains_null=_inner_nullable(False)),
                contains_null=_inner_nullable(False),
            )
            result_exp = snowpark_fn.cast(sentences_udf(*snowpark_args), result_type)
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "sequence":
            start_type = snowpark_typed_args[0].typ
            stop_type = snowpark_typed_args[1].typ
            step_type = (
                snowpark_typed_args[2].typ if len(snowpark_typed_args) > 2 else None
            )

            if all(isinstance(arg.typ, _IntegralType) for arg in snowpark_typed_args):
                result_type = _find_common_type(
                    [arg.typ for arg in snowpark_typed_args]
                )
                seq_arr_type = ArrayType(
                    result_type, contains_null=_inner_nullable(False)
                )
                result_exp = snowpark_fn.cast(
                    snowpark_fn.sequence(*snowpark_args),
                    seq_arr_type,
                )
                result_exp = TypedColumn(
                    result_exp,
                    lambda: [
                        FieldType(
                            seq_arr_type,
                            nullable=_any_arg_nullable(snowpark_typed_args),
                        )
                    ],
                )
            elif (
                isinstance(start_type, (TimestampType, DateType))
                and isinstance(stop_type, (TimestampType, DateType))
                and (
                    step_type is None
                    or isinstance(
                        step_type,
                        (DayTimeIntervalType, YearMonthIntervalType),
                    )
                )
            ):
                result_type, result_exp = _build_temporal_sequence(
                    start_type,
                    stop_type,
                    step_type,
                    snowpark_args,
                    snowpark_typed_args,
                    snowpark_arg_names,
                )
            else:
                exception = AnalysisException(
                    _sequence_wrong_input_types_message(snowpark_arg_names)
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
        case "sha":
            sha_function = snowpark_fn.function("SHA1_HEX")
            result_exp = sha_function(snowpark_args[0])
            result_type = FieldType(
                StringType(40), _unary_nullable(snowpark_typed_args)
            )
        case "sha1":
            result_exp = snowpark_fn.sha1(snowpark_args[0])
            result_type = FieldType(
                StringType(40), _unary_nullable(snowpark_typed_args)
            )
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
                result_exp = TypedColumn(
                    result_exp, lambda: [FieldType(result_type, nullable=True)]
                )
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
                result_exp = TypedColumn(
                    result_exp, lambda: [FieldType(result_type, nullable=True)]
                )
        case "shiftleft":
            expr, n = snowpark_args
            is_long = isinstance(snowpark_typed_args[0].typ, LongType)
            mask = 63 if is_long else 31
            masked_n = n.bitwiseAnd(snowpark_fn.lit(mask))
            sl_bn = _binary_nullable(snowpark_typed_args)

            expr_long = snowpark_fn.cast(expr, LongType())
            shifted = snowpark_fn.bitshiftleft(expr_long, masked_n)

            if is_long:
                result_type = FieldType(LongType(), sl_bn)
                result_exp = snowpark_fn.when(
                    shifted > snowpark_fn.lit(MAX_INT64),
                    shifted - snowpark_fn.lit(MAX_UINT64 + 1),
                ).otherwise(shifted)
            else:
                masked = shifted.bitwiseAnd(snowpark_fn.lit(MAX_UINT32))
                result_type = FieldType(IntegerType(), sl_bn)
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
            sr_dt = LongType() if is_long else IntegerType()
            result_type = FieldType(sr_dt, _binary_nullable(snowpark_typed_args))
        case "shiftrightunsigned":
            expr, n = snowpark_args
            is_long = isinstance(snowpark_typed_args[0].typ, LongType)
            mask = 63 if is_long else 31
            masked_n = n.bitwiseAnd(snowpark_fn.lit(mask))
            sru_bn = _binary_nullable(snowpark_typed_args)

            unsigned_max = MAX_UINT64 if is_long else MAX_UINT32

            expr_long = snowpark_fn.cast(expr, LongType())
            expr_unsigned = snowpark_fn.when(
                expr_long < snowpark_fn.lit(0),
                expr_long + snowpark_fn.lit(unsigned_max + 1),
            ).otherwise(expr_long)

            shifted = snowpark_fn.bitshiftright(expr_unsigned, masked_n)

            if is_long:
                result_type = FieldType(LongType(), sru_bn)
                result_exp = snowpark_fn.when(
                    shifted > snowpark_fn.lit(MAX_INT64),
                    shifted - snowpark_fn.lit(unsigned_max + 1),
                ).otherwise(shifted)
            else:
                result_type = FieldType(IntegerType(), sru_bn)
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

            arg = snowpark_args[0]
            result_exp = snowpark_fn.cast(
                snowpark_fn.when(
                    arg.is_null(),
                    snowpark_fn.lit(None),
                ).otherwise(_shuffle_udf(snowpark_fn.cast(arg, ArrayType()))),
                arg_type,
            )
            result_type = FieldType(arg_type, _unary_nullable(snowpark_typed_args))
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
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "sin":
            spark_function_name = f"SIN({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.sin(snowpark_args[0])
            result_type = DoubleType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "sinh":
            spark_function_name = f"SINH({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.sinh(snowpark_args[0])
            result_type = DoubleType()
            result_exp = TypedColumn(
                result_exp, lambda: [FieldType(result_type, nullable=True)]
            )
        case "size":
            # When size function is called size has type integer in Spark
            # https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/collectionOperations.scala#L123
            result_type = IntegerType()

            # SNOW-3516722
            # Optimization: when the argument is statically typed as an ArrayType (e.g. the
            # result of split() or array_append() etc.), we know it is always an array, so the
            # generic is_array/is_object/is_null CASE/WHEN wrapper and VARIANT cast are
            # unnecessary.  Emit array_size() directly, which produces far shorter SQL.
            #
            # Non-ANSI semantics: Spark's size(null) returns -1; Snowflake's array_size(null)
            # returns NULL.  Preserve the -1 fallback with COALESCE when ansi is disabled.
            if isinstance(snowpark_typed_args[0].typ, ArrayType):
                arr_size_expr = snowpark_fn.array_size(snowpark_args[0])
                if not spark_sql_ansi_enabled:
                    # Preserve size(null) == -1 for non-ANSI mode
                    arr_size_expr = snowpark_fn.coalesce(
                        arr_size_expr, snowpark_fn.lit(-1)
                    )
                result_exp = arr_size_expr.cast(result_type).alias(
                    f"SIZE({snowpark_args[0]})"
                )
            else:
                v = snowpark_fn.cast(snowpark_args[0], VariantType())
                null_value = (
                    snowpark_fn.lit(None)
                    if spark_sql_ansi_enabled
                    else snowpark_fn.lit(-1)
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [
                    FieldType(
                        snowpark_typed_args[0].typ,
                        nullable=_any_arg_nullable(snowpark_typed_args),
                    )
                ],
            )
        case "sort_array":
            if len(snowpark_args) == 2:
                if not isinstance(snowpark_typed_args[1].typ, BooleanType):
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 2 requires the "BOOLEAN" type, however "{snowpark_arg_names[1]}" has the type "{snowpark_typed_args[1].typ.simpleString().upper()}"'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
                sort_asc = unwrap_literal(exp.unresolved_function.arguments[1])
                if sort_asc is None:
                    exception = AnalysisException(
                        f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "{spark_function_name}" due to data type mismatch: Parameter 2 requires the "BOOLEAN" type, however "CAST(NULL AS BOOLEAN)" has the type "BOOLEAN"'
                    )
                    attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                    raise exception
            else:
                sort_asc = True
            result_exp = snowpark_fn.sort_array(
                *snowpark_args,
                nulls_first=sort_asc,
            )
            spark_function_name = (
                f"sort_array({snowpark_arg_names[0]}, {str(sort_asc).lower()})"
            )
            sa_type = snowpark_typed_args[0].typ
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(sa_type, _binary_nullable(snowpark_typed_args))],
            )
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
            result_type = FieldType(StringType(), _unary_nullable(snowpark_typed_args))
        case "space":
            result_exp = snowpark_fn.builtin("space")(*snowpark_args)
            result_type = FieldType(StringType(), _unary_nullable(snowpark_typed_args))
        case "spark_partition_id":
            result_exp = snowpark_fn.lit(0)
            # Spark 3.5.3: SparkPartitionID defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/partitionTransforms.scala#L47
            dt = IntegerType()
            result_exp = snowpark_fn.cast(result_exp, dt)
            result_type = FieldType(dt, nullable=False)
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

                    # Optimization: when limit is a literal <= 0 (the default 2-arg case passes
                    # lit(-1)), we know the WHEN(limit<=0, native_split) branch is always taken.
                    # Emit native split directly instead of a WHEN/ELSE wrapper.
                    limit_is_known_nonpositive = (
                        isinstance(limit._expression, Literal)
                        and isinstance(limit._expression.value, int)
                        and limit._expression.value is not None
                        and limit._expression.value <= 0
                    )

                    # Optimization: treat escaped regex that resolves to a pure literal delimiter
                    # - Single char: "\\."
                    # - Multi char: e.g., "\\.505\\."
                    if re.fullmatch(r"(?:\\.)+", pattern_value):
                        literal_delim = re.sub(r"\\(.)", r"\1", pattern_value)
                        if limit_is_known_nonpositive:
                            return snowpark_fn.split(
                                str_, snowpark_fn.lit(literal_delim)
                            ).cast(result_type)
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
                        if limit_is_known_nonpositive:
                            return snowpark_fn.split(str_, pattern).cast(result_type)
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
            result_type = FieldType(
                ArrayType(StringType(), contains_null=_inner_nullable(False)),
                nullable=_any_arg_nullable(snowpark_typed_args),
            )
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
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
            # SQRT(NULL) returns NULL natively in SQL; explicit null guard is redundant
            result_exp = snowpark_fn.when(sqrt_arg < 0, NAN).otherwise(
                snowpark_fn.sqrt(sqrt_arg)
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

            analyzer = session._analyzer
            arg_sqls = [
                analyzer.analyze(arg._expression, defaultdict())
                for arg in snowpark_args[1:]
            ]

            row_objects = []
            for row_idx in range(num_rows):
                obj_parts = []
                for col_idx in range(num_cols):
                    arg_idx = row_idx * num_cols + col_idx
                    key = f"c{col_idx}"
                    if arg_idx < num_arguments:
                        obj_parts.append(f"'{key}', {arg_sqls[arg_idx]}")
                    else:
                        obj_parts.append(f"'{key}', NULL")
                row_objects.append(
                    f"object_construct_keep_null({', '.join(obj_parts)})"
                )

            array_sql = f"array_construct({', '.join(row_objects)})"
            array_expr = snowpark_fn.sql_expr(array_sql)

            result_exp = snowpark_fn.call_table_function("flatten", input=array_expr)

            selected_projection_specs = [
                SelectedProjectionSpec("VALUE", spark_col_types[col_idx], f"c{col_idx}")
                for col_idx in range(num_cols)
            ]

            result_type = spark_col_types[0:num_cols]
        case "startswith":
            result_exp = snowpark_args[0].startswith(snowpark_args[1])
            result_type = FieldType(
                BooleanType(), _binary_nullable(snowpark_typed_args)
            )
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

                pairs = re.split(pair_delim, s) if pair_delim else list(s)
                kv_pairs = [
                    re.split(kv_delim, pair, maxsplit=1)
                    if kv_delim
                    else (list(pair) or [""])
                    for pair in pairs
                ]

                result_map = {}

                for kv_pair in kv_pairs:
                    key = kv_pair[0]
                    val = kv_pair[1] if len(kv_pair) >= 2 else None

                    if key in result_map and not allow_dups:
                        raise ValueError(
                            f"[snowpark_connect::invalid_input] {DUPLICATE_KEY_FOUND_ERROR_TEMPLATE.format(key=key)}"
                        )

                    result_map[key] = val

                return result_map

            def _literal_string_or_none(col: Column) -> Optional[str]:
                expr = col._expression
                if isinstance(expr, Literal) and expr.value is not None:
                    return str(expr.value)
                return None

            pair_delim_str = _literal_string_or_none(pair_delim_)
            kv_delim_str = _literal_string_or_none(kv_delim_)

            # SNOW-3362652: use native REDUCE + OBJECT_INSERT when both delimiters are
            # pure literals, otherwise fall back to the regex UDF.
            delimiters_are_pure_literals = bool(
                pair_delim_str
                and kv_delim_str
                and re.escape(pair_delim_str) == pair_delim_str
                and re.escape(kv_delim_str) == kv_delim_str
            )
            if delimiters_are_pure_literals:
                esc_kv = kv_delim_str.replace("'", "''")
                reduce_lambda = (
                    f"(acc, pair) -> object_insert("
                    f"acc, "
                    f"SPLIT_PART(pair, '{esc_kv}', 1), "
                    f"IFF(POSITION('{esc_kv}', pair) > 0, "
                    f"SUBSTR(pair, POSITION('{esc_kv}', pair) + {len(kv_delim_str)})::VARIANT, "
                    f"PARSE_JSON('null')), "
                    f"{str(allow_duplicate_keys).lower()}"
                    f")"
                )
                str_to_map_result = snowpark_fn.function("reduce")(
                    snowpark_fn.split(value, pair_delim_),
                    snowpark_fn.object_construct(),
                    snowpark_fn.sql_expr(reduce_lambda),
                )
            else:
                str_to_map_result = _str_to_map(
                    snowpark_fn.lit(allow_duplicate_keys),
                    value,
                    pair_delim_,
                    kv_delim_,
                )

            result_exp = snowpark_fn.cast(
                str_to_map_result,
                MapType(StringType(), StringType()),
            )
            result_type = FieldType(
                MapType(StringType(), StringType()),
                nullable=_any_arg_nullable(snowpark_typed_args),
            )
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
                            return exp.unresolved_function.arguments[index].alias.name[
                                0
                            ]
                        case "unresolved_attribute":
                            return resolved_name
                        case "unresolved_named_lambda_variable":
                            return exp.unresolved_function.arguments[
                                index
                            ].unresolved_named_lambda_variable.name_parts[0]
                        case "expression_string":
                            if index in arg_alias_names:
                                return arg_alias_names[index]

                    return f"col{index + 1}"

                fields_cols = list(zip(snowpark_arg_names, snowpark_typed_args))
                field_types = [
                    StructField(
                        _f_name(idx, name),
                        col.typ,
                        nullable=_inner_nullable(col.nullable),
                        _is_column=False,
                    )
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
                dt = StructType(field_types)
                result_exp = snowpark_fn.cast(result_exp, dt)
                result_type = FieldType(dt, nullable=False)
                spark_field_names = ", ".join(
                    resolved_name for (resolved_name, _) in fields_cols
                )
                spark_function_name = f"struct({spark_field_names})"
        case "substring" | "substr":
            input_type = (
                snowpark_typed_args[0].typ if snowpark_typed_args else StringType()
            )

            # When enabled, delegate to the native SQL function which handles
            # Spark substring semantics (1-based pos, 0-as-1, negative pos)
            # natively.  Only valid for string inputs — binary inputs fall
            # through to the CASE/WHEN boundary-check logic below.
            use_native_function = (
                global_config.snowpark_connect_enable_native_sql_for_substring
                and isinstance(input_type, StringType)
            )

            if use_native_function:
                result_exp = snowpark_fn.call_function(
                    "__SNOWPARK_INTERNAL_SUBSTRING", *snowpark_args
                )
            elif len(snowpark_args) >= 2:
                string_arg = snowpark_args[0]
                pos_arg = snowpark_args[1]

                if len(snowpark_args) == 3:
                    length_arg = snowpark_args[2]

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
                        string_length = snowpark_fn.length(string_arg)
                        computed_pos = (
                            snowpark_fn.when(
                                pos_arg < 0,
                                string_length + pos_arg + snowpark_fn.lit(1),
                            )
                            .when(pos_arg == 0, snowpark_fn.lit(1))
                            .otherwise(pos_arg)
                        )
                        adjusted_length = snowpark_fn.when(
                            computed_pos < 1,
                            snowpark_fn.greatest(
                                length_arg + computed_pos - snowpark_fn.lit(1),
                                snowpark_fn.lit(0),
                            ),
                        ).otherwise(length_arg)
                        clamped_pos = snowpark_fn.greatest(
                            computed_pos, snowpark_fn.lit(1)
                        )
                        result_exp = snowpark_fn.substring(
                            string_arg, clamped_pos, adjusted_length
                        )
                else:
                    adjusted_pos = snowpark_fn.when(
                        pos_arg == 0, snowpark_fn.lit(1)
                    ).otherwise(pos_arg)
                    result_exp = snowpark_fn.substring(string_arg, adjusted_pos)
            else:
                result_exp = snowpark_fn.substring(*snowpark_args)
            result_type = input_type
            if snowpark_typed_args:
                result_type = FieldType(
                    result_type,
                    nullable=_any_arg_nullable(snowpark_typed_args),
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
            result_type = FieldType(
                StringType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
        case "sum":
            sum_fn = snowpark_fn.sum
            input_type = snowpark_typed_args[0].typ
            if exp.unresolved_function.is_distinct:
                spark_function_name = f"sum(DISTINCT {snowpark_arg_names[0]})"
                sum_fn = snowpark_fn.sum_distinct

            arg = snowpark_args[0]
            if isinstance(input_type, StringType):
                arg = _coerce_string_input_to_double(
                    arg, spark_sql_ansi_enabled, aggregate_string_coercion_enabled
                )

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
                ft = FieldType(result_type, True)
                result_exp = TypedColumn(wrapped_sum, lambda f=ft: [f])
            else:
                result_exp = _resolve_aggregate_exp(
                    sum_fn(arg),
                    result_type,
                )
        case "tan":
            spark_function_name = f"TAN({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.tan(snowpark_args[0])
            result_type = DoubleType()
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "tanh":
            spark_function_name = f"TANH({snowpark_arg_names[0]})"
            result_exp = snowpark_fn.tanh(snowpark_args[0])
            result_type = DoubleType()
        case "timestamp_add":
            # Added to DataFrame functions in 4.0.0 - but can be called from SQL in 3.5.3.
            spark_function_name = f"timestampadd({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, {snowpark_arg_names[2]})"

            typ = snowpark_typed_args[2].typ
            ta_dt = (
                typ
                if isinstance(typ, TimestampType)
                else TimestampType(snowpark.types.TimestampTimeZone.LTZ)
            )
            bn = snowpark_typed_args[1].nullable or snowpark_typed_args[2].nullable
            result_type = FieldType(ta_dt, bn)

            result_exp = snowpark_fn.cast(
                snowpark_fn.dateadd(
                    unwrap_literal(exp.unresolved_function.arguments[0]),
                    snowpark_args[1],
                    snowpark_args[2],
                ),
                ta_dt,
            )
        case "timestamp_diff":
            # Added to DataFrame functions in 4.0.0 - but can be called from SQL in 3.5.3.
            spark_function_name = f"timestampdiff({snowpark_arg_names[0]}, {snowpark_arg_names[1]}, {snowpark_arg_names[2]})"
            result_exp = snowpark_fn.datediff(
                unwrap_literal(exp.unresolved_function.arguments[0]),
                snowpark_args[1],
                snowpark_args[2],
            )
            bn = snowpark_typed_args[1].nullable or snowpark_typed_args[2].nullable
            result_exp = TypedColumn(
                result_exp, lambda n=bn: [FieldType(LongType(), n)]
            )
        case "timestamp_micros":
            if isinstance(snowpark_typed_args[0].typ, NullType):
                result_exp = snowpark_fn.lit(None)
            elif not isinstance(snowpark_typed_args[0].typ, _IntegralType):
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve "timestamp_micros({snowpark_arg_names[0]}" due to data type mismatch: Parameter 1 requires the "INTEGRAL" type, however "{snowpark_arg_names[0]}" has the type "{snowpark_typed_args[0].typ}".'
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            else:
                result_exp = _timestamp_with_overflow_guard(
                    snowpark_args[0],
                    micros_expr=snowpark_args[0],
                    overflow_limit=_MICROS_OVERFLOW_LIMIT,
                )
            result_type = FieldType(
                TimestampType(snowpark.types.TimestampTimeZone.LTZ),
                _unary_nullable(snowpark_typed_args),
            )
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
                result_exp = _timestamp_with_overflow_guard(
                    snowpark_args[0],
                    micros_expr=snowpark_args[0] * 1_000,
                    overflow_limit=_MILLIS_OVERFLOW_LIMIT,
                )
            result_type = FieldType(
                TimestampType(snowpark.types.TimestampTimeZone.LTZ),
                _unary_nullable(snowpark_typed_args),
            )
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
                result_exp = _timestamp_with_overflow_guard(
                    snowpark_args[0],
                    micros_expr=snowpark_fn.cast(
                        snowpark_args[0] * 1_000_000, LongType()
                    ),
                    overflow_limit=_SECONDS_OVERFLOW_LIMIT,
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
            result_type = FieldType(StringType(), _binary_nullable(snowpark_typed_args))
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "to_number":
            precision, scale = resolve_to_number_precision_and_scale(exp)
            to_number = snowpark_fn.function("to_number")
            result_exp = resolve_to_number_expression(
                to_number,
                snowpark_args[0],
                snowpark_args[1],
                precision,
                scale,
                snowpark_arg_names[1],
                function_name,
                session,
            )
            result_type = FieldType(
                DecimalType(precision, scale), _binary_nullable(snowpark_typed_args)
            )
        case "to_timestamp":
            input_is_literal = (
                len(exp.unresolved_function.arguments) > 0
                and exp.unresolved_function.arguments[0].WhichOneof("expr_type")
                == "literal"
            )
            if not spark_sql_ansi_enabled:
                function_name = "try_to_timestamp"
            match (snowpark_typed_args, exp.unresolved_function.arguments):
                case ([e], _) if isinstance(e.typ, _NumericType):
                    if get_timestamp_type() == TimestampType(
                        snowpark.types.TimestampTimeZone.NTZ
                    ):
                        # Under TIMESTAMP_NTZ config, Spark's ParseToTimestamp excludes
                        # NumericType from its inputTypes — same semantics as
                        # to_timestamp_ntz(numeric): NULL in non-ANSI, CAST_INVALID_INPUT
                        # error in ANSI (string-parse path, which always fails for numeric).
                        ntz = TimestampType(snowpark.types.TimestampTimeZone.NTZ)
                        null_ntz = snowpark_fn.lit(None).cast(ntz)
                        if spark_sql_ansi_enabled:
                            raise_fn = _raise_error_helper(ntz, DateTimeException)
                            result_exp = snowpark_fn.when(
                                e.col.is_null(), null_ntz
                            ).otherwise(
                                raise_fn(
                                    snowpark_fn.lit("[CAST_INVALID_INPUT] The value '"),
                                    snowpark_fn.cast(e.col, StringType()),
                                    snowpark_fn.lit(
                                        '\' of the type "STRING" cannot be cast to'
                                        ' "TIMESTAMP_NTZ" because it is malformed.'
                                        " Correct the value as per the syntax, or"
                                        " change its target type. Use `try_cast` to"
                                        " tolerate malformed input and return NULL"
                                        ' instead. If necessary set "spark.sql.ansi'
                                        '.enabled" to "false" to bypass this error.'
                                    ),
                                )
                            )
                        else:
                            result_exp = null_ntz
                    else:
                        result_exp = snowpark_fn.to_timestamp(
                            snowpark_fn.cast(e.col * 1_000_000, LongType()),
                            snowpark_fn.lit(6),
                        )
                case ([e], _) if type(e.typ) in (DateType, TimestampType, NullType):
                    # try_to_timestamp rejects DATE/TIMESTAMP/NULL inputs (TRY_CAST
                    # type error); to_timestamp accepts them and never fails for these
                    # types, matching Spark (a non-string arg is reinterpreted directly).
                    result_exp = snowpark_fn.to_timestamp(e.col)
                case ([e], _):
                    result_exp = snowpark_fn.function(function_name)(e.col)
                case ([e, _], _) if type(e.typ) in (DateType, TimestampType):
                    result_exp = snowpark_fn.to_timestamp(e.col)
                case ([e, _], [_, fmt]):
                    if input_is_literal:
                        _timestamp_format_sanity_check(
                            snowpark_arg_names[0], snowpark_arg_names[1]
                        )
                    fmt_lit = snowpark_fn.lit(
                        map_spark_timestamp_format_expression(fmt, e.typ)
                    )
                    # NULL input: plain to_timestamp accepts it; try_to_timestamp
                    # would TRY_CAST-error on the NULL-typed column.
                    ts_fn = (
                        snowpark_fn.to_timestamp
                        if type(e.typ) is NullType
                        else snowpark_fn.function(function_name)
                    )
                    result_exp = ts_fn(e.col, fmt_lit)
                case _:
                    exception = ValueError(
                        f"Invalid number of arguments to {function_name}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT
                    )
                    raise exception
            result_type = get_timestamp_type()
            result_exp = _cast_to_ts_type(result_exp, result_type)

        case "to_timestamp_ltz":
            match (snowpark_typed_args, exp.unresolved_function.arguments):
                case ([e], _) if isinstance(e.typ, _NumericType):
                    # Spark casts a single numeric arg as epoch seconds (same as
                    # to_timestamp). Snowflake's TO_TIMESTAMP_LTZ rejects FLOAT/DOUBLE,
                    # so route all numerics through the epoch-seconds path.
                    result_exp = snowpark_fn.to_timestamp(
                        snowpark_fn.cast(e.col * 1_000_000, LongType()),
                        snowpark_fn.lit(6),
                    )
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
                case ([e], _) if isinstance(e.typ, _NumericType):
                    # Unlike to_timestamp_ltz, Spark's to_timestamp_ntz does NOT treat a
                    # numeric arg as epoch seconds. NumericType is absent from its accepted
                    # input types, so Spark casts the number to a string and parses it as a
                    # timestamp literal. A numeric never stringifies to a valid timestamp
                    # literal, so the result is always NULL (non-ANSI) or a CAST_INVALID_INPUT
                    # error (ANSI). We must NOT delegate to TRY_TO_TIMESTAMP_NTZ: Snowflake
                    # auto-interprets integer-like strings (e.g. '1') as epoch seconds, which
                    # diverges from Spark. A literal NULL arg stays NULL even under ANSI.
                    ntz_type = TimestampType(snowpark.types.TimestampTimeZone.NTZ)
                    null_ntz = snowpark_fn.lit(None).cast(ntz_type)
                    if spark_sql_ansi_enabled:
                        raise_fn = _raise_error_helper(ntz_type, DateTimeException)
                        result_exp = snowpark_fn.when(
                            e.col.is_null(), null_ntz
                        ).otherwise(
                            raise_fn(
                                snowpark_fn.lit("[CAST_INVALID_INPUT] The value '"),
                                snowpark_fn.cast(e.col, StringType()),
                                snowpark_fn.lit(
                                    '\' of the type "STRING" cannot be cast to "TIMESTAMP_NTZ" because it is malformed. Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                                ),
                            )
                        )
                    else:
                        result_exp = null_ntz
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
            tu_dt = TimestampType()
            ts_arg, tz_arg = snowpark_args[0], snowpark_args[1]
            if isinstance(tz_arg._expression, Literal) and isinstance(
                tz_arg._expression.value, str
            ):
                literal_val = tz_arg._expression.value
                offset_secs = _literal_offset_seconds(literal_val)
                if offset_secs is not None:
                    # Literal UTC offset: negate offset (local → UTC), emit DATEADD.
                    ts_expr = snowpark_fn.dateadd(
                        "second", snowpark_fn.lit(-offset_secs), ts_arg
                    )
                else:
                    ts_expr = snowpark_fn.to_utc_timestamp(
                        ts_arg, _map_from_spark_tz(tz_arg)
                    )
            else:
                ts_expr = _build_utc_timestamp_expr(ts_arg, tz_arg, from_utc=False)
            result_type = FieldType(tu_dt, _binary_nullable(snowpark_typed_args))
            result_exp = _try_to_cast(
                "try_to_timestamp",
                snowpark_fn.cast(ts_expr, tu_dt),
                ts_arg,
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
            result_type = FieldType(
                StringType(), nullable=_any_arg_nullable(snowpark_typed_args)
            )
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
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
                            result_exp,
                            lambda: [FieldType(result_type, nullable=True)],
                        )
                    else:
                        result_exp = _type_with_typer(result_exp, force_nullable=True)
        case "try_aes_decrypt":
            if global_config.snowpark_connect_enable_aes_raw_functions:
                result_exp = _aes_decrypt_raw_helper(
                    "TRY_DECRYPT_RAW",
                    snowpark_args[0],
                    snowpark_args[1],
                    snowpark_typed_args[1].typ,
                    snowpark_args[4],
                    snowpark_typed_args[4].typ,
                    snowpark_args[2],
                    snowpark_args[3],
                )
            else:
                result_exp = _aes_helper(
                    "TRY_DECRYPT",
                    snowpark_args[0],
                    snowpark_args[1],
                    snowpark_args[4],
                    snowpark_args[2],
                    snowpark_args[3],
                )
            result_type = BinaryType()
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "try_avg":
            # TODO(SNOW-2097962): Return Infinity instead of NULL on overflow by using COALESCE(TRY_CAST(...), 'inf'::real)
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
                        cleaned = _try_cast_to_double(
                            snowpark_args[0],
                            snowpark_typed_args[0].typ,
                        )
                    result_exp, result_type = _try_sum_helper(
                        DoubleType(), cleaned, calculating_avg=True
                    )
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
                case (NullType(), t) | (t, NullType()):
                    result_exp = snowpark_fn.lit(None)
                    result_type = FloatType()
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
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
                    result_exp = _type_with_typer(result_exp, force_nullable=True)
                case (
                    (StringType(), _)
                    | (_, StringType())
                    | (VariantType(), _)
                    | (
                        _,
                        VariantType(),
                    )
                ):
                    cleaned_left, cleaned_right = _try_cast_to_double(
                        snowpark_args[0],
                        snowpark_typed_args[0].typ,
                    ), _try_cast_to_double(
                        snowpark_args[1],
                        snowpark_typed_args[1].typ,
                    )

                    result_exp = snowpark_fn.when(
                        cleaned_right == 0, snowpark_fn.lit(None)
                    ).otherwise(cleaned_left / cleaned_right)
                    result_exp = _type_with_typer(result_exp, force_nullable=True)
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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
                case (MapType(), StringType()):
                    result_exp = snowpark_fn.when(
                        snowpark_fn.map_contains_key(
                            snowpark_args[1], snowpark_args[0]
                        ),
                        snowpark_fn.get(snowpark_args[0], snowpark_args[1]),
                    ).otherwise(snowpark_fn.lit(None))
                    result_type = snowpark_typed_args[0].typ.value_type
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )

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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
                case (NullType(), t) | (t, NullType()):
                    result_exp = snowpark_fn.lit(None)
                    match t:
                        case NullType() | StringType():
                            result_type = FloatType()
                        case _:
                            result_type = t
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
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
                    result_exp = _type_with_typer(result_exp, force_nullable=True)
                case (
                    (StringType(), _)
                    | (_, StringType())
                    | (VariantType(), _)
                    | (
                        _,
                        VariantType(),
                    )
                ):
                    cleaned_left, cleaned_right = _try_cast_to_double(
                        snowpark_args[0],
                        snowpark_typed_args[0].typ,
                    ), _try_cast_to_double(
                        snowpark_args[1],
                        snowpark_typed_args[1].typ,
                    )
                    result_exp = cleaned_left * cleaned_right
                    result_exp = _type_with_typer(result_exp, force_nullable=True)
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "try_subtract":
            # Handle interval arithmetic with overflow detection
            match (snowpark_typed_args[0].typ, snowpark_typed_args[1].typ):
                case (DateType(), t) if isinstance(t, YearMonthIntervalType):
                    result_type = DateType()
                    result_exp = snowpark_args[0] - snowpark_args[1]
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
                case (DateType(), t) if isinstance(t, DayTimeIntervalType):
                    result_type = TimestampType()
                    result_exp = snowpark_args[0] - snowpark_args[1]
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
                case (TimestampType(), t) if isinstance(
                    t, (DayTimeIntervalType, YearMonthIntervalType)
                ):
                    result_type = snowpark_typed_args[0].typ
                    result_exp = snowpark_args[0] - snowpark_args[1]
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
                    )
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
                    result_exp = TypedColumn(
                        result_exp,
                        lambda: [FieldType(result_type, nullable=True)],
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
                            result_exp,
                            lambda: [FieldType(result_type, nullable=True)],
                        )
                    else:
                        result_exp = _type_with_typer(result_exp, force_nullable=True)
        case "try_to_number":
            try_to_number = snowpark_fn.function("try_to_number")
            precision, scale = resolve_to_number_precision_and_scale(exp)
            result_exp = resolve_to_number_expression(
                try_to_number,
                snowpark_args[0],
                snowpark_args[1],
                precision,
                scale,
                snowpark_arg_names[1],
                function_name,
                session,
            )
            result_type = DecimalType(precision, scale)
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )

        case "try_to_timestamp":
            input_is_literal = (
                exp.unresolved_function.arguments[0].WhichOneof("expr_type")
                == "literal"
            )
            # special case for literal null input
            # snowflake does not support cast(try_to_timestamp(null) as TIMESTAMP_LTZ)
            # if the input is a literal NULL, we just return null and don't attempt to
            # call any functions
            if (
                input_is_literal
                and unwrap_literal(exp.unresolved_function.arguments[0]) is None
            ):
                result_exp = snowpark_fn.lit(None)
            else:
                match (snowpark_typed_args, exp.unresolved_function.arguments):
                    case ([e, _], _) | ([e], _) if type(e.typ) in (
                        DateType,
                        TimestampType,
                    ):
                        # Spark reinterprets a date/timestamp arg directly (any format is
                        # ignored) and never fails. TRY_TO_TIMESTAMP rejects non-string
                        # input, so defer to the trailing cast to the timestamp type.
                        result_exp = e.col
                    case ([e], _) if isinstance(e.typ, _NumericType):
                        if get_timestamp_type() == TimestampType(
                            snowpark.types.TimestampTimeZone.NTZ
                        ):
                            # Under TIMESTAMP_NTZ, try_to_timestamp(numeric) follows
                            # the same NTZ semantics as to_timestamp_ntz(numeric):
                            # numeric is not accepted as epoch seconds. try_ functions
                            # return NULL instead of raising.
                            result_exp = snowpark_fn.lit(None)
                        else:
                            result_exp = snowpark_fn.to_timestamp(
                                snowpark_fn.cast(e.col * 1_000_000, LongType()),
                                snowpark_fn.lit(6),
                            )
                    case ([e], _):
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
            result_exp = _cast_to_ts_type(result_exp, result_type)
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "typeof":
            col_snowpark_typ = snowpark_typed_args[0].typ
            spark_typ = map_snowpark_to_pyspark_types(col_snowpark_typ)
            result_exp = snowpark_fn.lit(spark_typ.simpleString())
            result_type = FieldType(StringType(), nullable=False)
        case "unbase64":
            base64_decoding_function = snowpark_fn.function("TRY_BASE64_DECODE_BINARY")

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
            # String/Binary: after regexp_replace, TRY_BASE64_DECODE_BINARY never returns NULL
            # — error-throw is dead code. Other types: keep it (e.g. int 1 → "1===", undecodable).
            if isinstance(snowpark_typed_args[0].typ, (StringType, BinaryType)):
                result_exp = base64_decoding_function(padded)
            else:
                decoded = base64_decoding_function(padded)
                raise_fn = _raise_error_helper(BinaryType(), IllegalArgumentException)
                result_exp = snowpark_fn.when(
                    unbase_arg.is_not_null() & decoded.is_null(),
                    raise_fn(snowpark_fn.lit("Invalid input")),
                ).otherwise(decoded)

            result_type = FieldType(BinaryType(), _unary_nullable(snowpark_typed_args))
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "unix_date":
            result_exp = snowpark_fn.datediff(
                "day", snowpark_fn.lit("1970-01-01"), snowpark_args[0]
            )
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
        case "unix_micros":
            result_exp = snowpark_fn.date_part(
                "epoch_microseconds",
                snowpark_fn.cast(snowpark_args[0], get_timestamp_type()),
            )
            result_type = FieldType(LongType(), _unary_nullable(snowpark_typed_args))
        case "unix_millis":
            result_exp = snowpark_fn.date_part(
                "epoch_milliseconds",
                snowpark_fn.cast(snowpark_args[0], get_timestamp_type()),
            )
            result_type = FieldType(LongType(), _unary_nullable(snowpark_typed_args))
        case "unix_seconds":
            result_exp = snowpark_fn.date_part(
                "epoch_seconds",
                snowpark_fn.cast(snowpark_args[0], get_timestamp_type()),
            )
            result_type = FieldType(LongType(), _unary_nullable(snowpark_typed_args))
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

            raw_type = map_json_schema_to_snowpark(metadata["__udt_info__"]["sqlType"])

            result_exp = snowpark_fn.cast(snowpark_args[0], raw_type)
            result_type = FieldType(raw_type, _unary_nullable(snowpark_typed_args))
        case "upper" | "ucase":
            result_exp = snowpark_fn.upper(snowpark_args[0])
            result_type = FieldType(StringType(), _unary_nullable(snowpark_typed_args))
        case "url_decode":

            @cached_udf(
                input_types=[StringType()],
                return_type=StringType(),
            )
            def _url_decode(encoded_url: Optional[str]) -> Optional[str]:
                if encoded_url is None:
                    return None
                import re
                from urllib.parse import unquote

                invalid = re.search(r"%(?![0-9A-Fa-f]{2})", encoded_url)
                if invalid:
                    raise ValueError(
                        f"[CANNOT_DECODE_URL] Cannot decode the url: {encoded_url}"
                    )
                return unquote(encoded_url.replace("+", " "))

            result_exp = _url_decode(snowpark_args[0])
            result_type = StringType()
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "uuid":
            result_exp = snowpark_fn.builtin("UUID_STRING")()
            result_type = FieldType(StringType(), nullable=False)
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
                snowpark_fn.var_pop(var_pop_argument), result_type, nullable=True
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
                snowpark_fn.var_samp(var_samp_argument), result_type, nullable=True
            )
        case "version":
            result_exp = snowpark_fn.lit(get_spark_version())
            result_type = FieldType(StringType(), nullable=False)
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
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
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
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
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

            result_type_indexes = [1]
            for i in range(2, len(snowpark_args), 2):
                if i + 1 >= len(snowpark_args):
                    result_type_indexes.append(i)
                else:
                    # Validate each WHEN condition
                    condition_type = snowpark_typed_args[i].typ
                    if not isinstance(condition_type, BooleanType):
                        exception = AnalysisException(
                            f"[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Cannot resolve CASE WHEN condition due to data type mismatch: "
                            f"Parameter {i + 1} requires the 'BOOLEAN' type, however got '{condition_type}'"
                        )
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
                    result_type_indexes.append(i + 1)

            result_type = _find_common_type(
                [snowpark_typed_args[i].typ for i in result_type_indexes]
            )

            has_else = len(snowpark_args) % 2 == 1
            branch_nullable = any(
                cast_nullable(
                    snowpark_typed_args[i].nullable,
                    snowpark_typed_args[i].typ,
                    result_type,
                )
                for i in result_type_indexes
            )
            when_nullable = branch_nullable or (not has_else)
            result_type = FieldType(result_type, when_nullable)

            name_components = ["CASE"]
            name_components.append("WHEN")
            name_components.append(snowpark_arg_names[0])
            name_components.append("THEN")
            name_components.append(snowpark_arg_names[1])
            first_value = _coerce_null_typed_expr(
                snowpark_args[1], snowpark_typed_args[1].typ, result_type.datatype
            )
            result_exp = snowpark_fn.when(snowpark_args[0], first_value)
            for i in range(2, len(snowpark_args), 2):
                if i + 1 >= len(snowpark_args):
                    name_components.append("ELSE")
                    name_components.append(snowpark_arg_names[i])
                    result_exp = result_exp.otherwise(
                        _coerce_null_typed_expr(
                            snowpark_args[i],
                            snowpark_typed_args[i].typ,
                            result_type.datatype,
                        )
                    )
                else:
                    name_components.append("WHEN")
                    name_components.append(snowpark_arg_names[i])
                    name_components.append("THEN")
                    name_components.append(snowpark_arg_names[i + 1])
                    result_exp = result_exp.when(
                        snowpark_args[i],
                        _coerce_null_typed_expr(
                            snowpark_args[i + 1],
                            snowpark_typed_args[i + 1].typ,
                            result_type.datatype,
                        ),
                    )
            name_components.append("END")
            result_exp = snowpark_fn.cast(result_exp, result_type.datatype)
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
            result_exp = snowpark_fn.cast(result_exp, result_type)
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "window":
            (window_duration, start_time) = _extract_window_args(exp)
            spark_function_name = "window"
            result_exp = snowpark_fn.window(
                snowpark_args[0], window_duration, start_time=start_time
            )
            window_schema = StructType(
                [
                    StructField(
                        "start",
                        TimestampType(TimestampTimeZone.LTZ),
                        True,
                        _is_column=False,
                    ),
                    StructField(
                        "end",
                        TimestampType(TimestampTimeZone.LTZ),
                        True,
                        _is_column=False,
                    ),
                ],
                structured=STRUCTURED_TYPES_ENABLED,
            )
            result_exp = TypedColumn(
                snowpark_fn.cast(result_exp, window_schema), lambda: [window_schema]
            )
        case "xpath":
            result_type = ArrayType(StringType())
            result_exp = _create_xpath_expression("xpath_list", "ARRAY(STRING)")
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "xpath_boolean":
            result_type = BooleanType()
            result_exp = _create_xpath_expression("xpath_boolean", "BOOLEAN")
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "xpath_double" | "xpath_number":
            result_type = DoubleType()
            result_exp = _create_xpath_expression("xpath_number", "DOUBLE")
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "xpath_float":
            result_type = FloatType()
            result_exp = _create_xpath_expression("xpath_number", "DOUBLE")
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "xpath_int":
            result_type = IntegerType()
            xpath_expression = _create_xpath_expression("xpath_number", "DOUBLE")
            result_exp = _cast_and_handle_nan_xpath_expression(
                xpath_expression, result_type
            )
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "xpath_long":
            result_type = LongType()
            xpath_expression = _create_xpath_expression("xpath_number", "DOUBLE")
            result_exp = _cast_and_handle_nan_xpath_expression(
                xpath_expression, result_type
            )
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "xpath_short":
            result_type = ShortType()
            xpath_expression = _create_xpath_expression("xpath_number", "DOUBLE")
            result_exp = _cast_and_handle_nan_xpath_expression(
                xpath_expression, result_type
            )
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "xpath_string":
            result_type = StringType()
            result_exp = _create_xpath_expression("xpath_string", "STRING")
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )
        case "xxhash64":

            def _int32_to_le4_binary(col_expr):
                """
                Encode a 32-bit integer as 4-byte little-endian BINARY so that
                xxhash64(seed, binary) reproduces Spark's per-type byte layout.
                """
                int32 = snowpark_fn.cast(col_expr, IntegerType())

                def byte_hex(shift):
                    byte_val = (
                        snowpark_fn.builtin("bitand")(int32, snowpark_fn.lit(255))
                        if shift == 0
                        else snowpark_fn.builtin("bitand")(
                            snowpark_fn.builtin("bitshiftright")(
                                int32, snowpark_fn.lit(shift)
                            ),
                            snowpark_fn.lit(255),
                        )
                    )
                    return snowpark_fn.lpad(
                        snowpark_fn.trim(
                            snowpark_fn.to_char(byte_val, snowpark_fn.lit("FMXX"))
                        ),
                        snowpark_fn.lit(2),
                        snowpark_fn.lit("0"),
                    )

                return snowpark_fn.builtin("to_binary")(
                    snowpark_fn.concat(
                        byte_hex(0), byte_hex(8), byte_hex(16), byte_hex(24)
                    ),
                    snowpark_fn.lit("HEX"),
                )

            def _float_to_int_bits(col_expr):
                """
                IEEE-754 single-precision float → 32-bit integer representation
                (equivalent to Java Float.floatToIntBits with Spark's -0.0 → 0.0
                normalization).
                """
                f = snowpark_fn.cast(col_expr, FloatType())
                abs_f = snowpark_fn.abs(f)
                sign_bit = snowpark_fn.iff(
                    f < snowpark_fn.lit(0.0),
                    snowpark_fn.lit(1 << 31),
                    snowpark_fn.lit(0),
                )
                exp = snowpark_fn.floor(
                    snowpark_fn.builtin("log")(snowpark_fn.lit(2), abs_f)
                )
                biased_exp = exp + snowpark_fn.lit(127)
                mantissa = snowpark_fn.round(
                    (
                        abs_f / snowpark_fn.builtin("power")(snowpark_fn.lit(2), exp)
                        - snowpark_fn.lit(1)
                    )
                    * snowpark_fn.lit(1 << 23),
                    snowpark_fn.lit(0),
                )
                normal = sign_bit + biased_exp * snowpark_fn.lit(1 << 23) + mantissa
                subnormal = sign_bit + snowpark_fn.round(
                    abs_f
                    * snowpark_fn.builtin("power")(
                        snowpark_fn.lit(2), snowpark_fn.lit(149)
                    ),
                    snowpark_fn.lit(0),
                )
                str_f = snowpark_fn.builtin("to_varchar")(f)
                return (
                    snowpark_fn.when(
                        str_f == snowpark_fn.lit("NaN"),
                        snowpark_fn.lit(0x7FC00000),
                    )
                    .when(
                        str_f == snowpark_fn.lit("inf"),
                        snowpark_fn.lit(0x7F800000),
                    )
                    .when(
                        str_f == snowpark_fn.lit("-inf"),
                        snowpark_fn.lit(0xFF800000),
                    )
                    .when(f == snowpark_fn.lit(0.0), snowpark_fn.lit(0))
                    .when(
                        abs_f
                        < snowpark_fn.builtin("power")(
                            snowpark_fn.lit(2), snowpark_fn.lit(-126)
                        ),
                        subnormal,
                    )
                    .otherwise(normal)
                )

            def call_native_xxhash64(prev_hash: Column, col_: Column) -> Column:
                """Hash one column with Snowflake's native xxhash64, preserving
                Spark NULL semantics (NULL leaves running hash unchanged).
                """
                return snowpark_fn.iff(
                    col_.is_null(),
                    prev_hash,
                    snowpark_fn.call_function(
                        "xxhash64",
                        snowpark_fn.coalesce(prev_hash, snowpark_fn.lit(DEFAULT_SEED)),
                        col_,
                    ),
                )

            result_exp = snowpark_fn.lit(DEFAULT_SEED)
            for arg in snowpark_typed_args:
                match arg.typ:
                    case IntegerType() | ShortType() | ByteType() | BooleanType():
                        result_exp = call_native_xxhash64(
                            result_exp, _int32_to_le4_binary(arg.col)
                        )
                    case FloatType():
                        result_exp = call_native_xxhash64(
                            result_exp,
                            _int32_to_le4_binary(_float_to_int_bits(arg.col)),
                        )
                    case LongType() | DoubleType():
                        result_exp = call_native_xxhash64(result_exp, arg.col)
                    case _:
                        result_exp = call_native_xxhash64(
                            result_exp,
                            snowpark_fn.cast(arg.col, StringType()),
                        )
            result_type = FieldType(LongType(), nullable=False)
        case "year":
            if isinstance(snowpark_typed_args[0].typ, StringType):
                result_exp = snowpark_fn.year(
                    snowpark_fn.builtin("try_to_date")(snowpark_args[0])
                )
            else:
                result_exp = snowpark_fn.year(snowpark_fn.to_date(snowpark_args[0]))
            # Spark 3.5.3: Year extends GetDateField trait which defines dataType = IntegerType
            # https://github.com/apache/spark/blob/v3.5.3/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/expressions/datetimeExpressions.scala#L481
            result_exp = snowpark_fn.cast(result_exp, IntegerType())
            result_type = FieldType(IntegerType(), _unary_nullable(snowpark_typed_args))
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
        case udtf_name if cache.udtfs.has(udtf_name.lower()):
            udtf, spark_col_names = cache.udtfs.get(udtf_name.lower())
            result_exp = snowpark_fn.call_table_function(
                udtf.name,
                *(snowpark_fn.cast(arg, VariantType()) for arg in snowpark_args),
            )
            result_type = [f.datatype for f in udtf.output_schema]

        case cast_funcs if cast_funcs in CAST_FUNCTIONS:
            if len(snowpark_args) != 1:
                exception = AnalysisException(
                    f"[WRONG_NUM_ARGS.WITHOUT_SUGGESTION] The `{cast_funcs}` requires 1 parameter(s), but the actual number is {len(snowpark_args)}."
                )
                attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                raise exception
            cast_exp = expressions_proto.Expression(
                cast=expressions_proto.Expression.Cast(
                    expr=exp.unresolved_function.arguments[0],
                    type=CAST_FUNCTIONS[cast_funcs],
                )
            )

            return map_cast(cast_exp, column_mapping, typer, from_type_cast=True)

        case "luhn_check":

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
            result_exp = TypedColumn(
                result_exp,
                lambda: [FieldType(result_type, nullable=True)],
            )

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
    typed_col.set_selected_projection_specs(selected_projection_specs)
    typed_col.set_qualifiers({ColumnQualifier(tuple(qualifier_parts))})
    return spark_col_names, typed_col


def _try_cast_to_double(column: Column, from_: DataType) -> Column:
    """
    DEPRECATED because of performance issues (formerly named _try_cast_helper)

    Attempts to cast a given column to ``DoubleType()`` using the same behaviour as Spark
    for permissive numeric coercion (invalid values become NULL).

    Args:
        column (Column): The column to cast.
        from_ (DataType): Static type of ``column``.

    Returns:
        Column: A column that is cast to DoubleType. If the cast fails, it returns NULL instead of raising an error.

    Behavior:
        - No casting is done if `from_` is already DoubleType.
        - The column is first cast to a string type. This step is skipped if `from_` is already StringType.
        - If the final cast from StringType to DoubleType is unsuccessful, the result will be NULL.
    """
    if isinstance(from_, DoubleType):
        return column
    string_column = (
        column
        if isinstance(from_, StringType)
        else snowpark_fn.cast(column, StringType())
    )
    return snowpark_fn.try_cast(string_column, DoubleType())


def _coerce_string_input_to_double(
    arg: Column, ansi_enabled: bool, coercion_enabled: bool = True
) -> Column:
    """Coerce a string argument of a numeric function to ``DoubleType``.

    Spark implicitly casts string inputs of numeric functions (e.g. ``sum``,
    ``avg``, ``abs``) to double. In non-ANSI mode a malformed string coerces to
    NULL (so the aggregate simply ignores that row); in ANSI mode the cast
    raises. We mirror that exactly: ``TRY_CAST`` when non-ANSI, strict ``CAST``
    when ANSI.

    SNOW-3585745: previously this always used a strict ``CAST``, so a single
    non-numeric value made the whole query fail with Snowflake error 100038
    ("Numeric value '...' is not recognized") even in non-ANSI mode, where Spark
    would have returned a result.

    When *coercion_enabled* is False the pre-BCR strict ``CAST`` is restored
    regardless of ANSI mode, so customers who relied on the 100038 error as a
    data-quality gate can revert via config flag
    ``snowpark.connect.aggregate.coerceStringToNumeric=false``.
    """
    if ansi_enabled or not coercion_enabled:
        return snowpark_fn.cast(arg, DoubleType())
    return snowpark_fn.try_cast(arg, DoubleType())


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


# Arrow timestamps are int64 microseconds; values outside this range silently
# wrap in the Snowflake connector's nanoarrow layer. Guard thresholds are the
# max absolute input value for each unit before the microsecond conversion
# would overflow int64.
_MICROS_OVERFLOW_LIMIT = 9_223_372_036_854_775_807  # int64 max
_MILLIS_OVERFLOW_LIMIT = 9_223_372_036_854_775  # int64 max // 1_000
_SECONDS_OVERFLOW_LIMIT = 9_223_372_036_854  # int64 max // 1_000_000
_MICROS_PER_DAY = 86_400_000_000


def _timestamp_with_overflow_guard(
    input_col: Column,
    micros_expr: Column,
    overflow_limit: int,
) -> Column:
    """Generate a TIMESTAMP_LTZ expression with an overflow guard.

    Produces: IFF(ABS(input) > limit, TO_TIMESTAMP('overflow'), CAST(TO_TIMESTAMP(micros, 6) AS TIMESTAMP_LTZ))
    The overflow branch deliberately triggers a Snowflake error, matching
    Spark's ArithmeticException for timestamp overflow.
    """
    ts_type = TimestampType(snowpark.types.TimestampTimeZone.LTZ)
    return snowpark_fn.iff(
        snowpark_fn.abs(input_col) > snowpark_fn.lit(overflow_limit),
        snowpark_fn.to_timestamp(snowpark_fn.lit("overflow")),
        snowpark_fn.cast(snowpark_fn.to_timestamp(micros_expr, 6), ts_type),
    )


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


def _is_null_typed_container(typ: DataType) -> bool:
    """Check if a type is a container (array/map) that has NullType in a position that would
    cause Snowflake to reject a CAST to a more specific container type.
    e.g. ArrayType(NullType()), MapType(StringType(), NullType()),
    MapType(NullType(), NullType()), ArrayType(ArrayType(NullType())).
    These arise from array(lit(None)), create_map(k, lit(None)), or map() and can be
    safely replaced with a typed NULL when casting to a different container type.
    """
    if isinstance(typ, ArrayType):
        inner = typ.element_type
        return isinstance(inner, NullType) or _is_null_typed_container(inner)
    if isinstance(typ, MapType):
        key_null = isinstance(typ.key_type, NullType) or _is_null_typed_container(
            typ.key_type
        )
        val_null = isinstance(typ.value_type, NullType) or _is_null_typed_container(
            typ.value_type
        )
        return key_null or val_null
    return False


def _coerce_null_typed_expr(arg, arg_type: DataType, target_type: DataType):
    """Coerce an expression with NullType or a null-typed container to the target type.

    For bare NullType: returns CAST(NULL AS <type>).
    For null-typed containers (arrays/maps with NullType elements): uses TO_VARIANT
    to strip the pre-cast structured type (e.g. ARRAY(STRING)), then re-casts to the
    target structured type. This preserves the container's size and keys while allowing
    Snowflake to cast untyped variant nulls to the target element type.

    Returns the original arg unchanged if no coercion is needed.
    """
    if arg_type == target_type or target_type is None:
        return arg
    if isinstance(arg_type, NullType):
        return snowpark_fn.lit(None).cast(target_type)
    if _is_null_typed_container(arg_type):
        return snowpark_fn.cast(snowpark_fn.to_variant(arg), target_type)
    return arg


def _coerce_array_and_element(
    arr_col: Column,
    arr_type: DataType,
    elem_col: Column,
    elem_type: DataType,
) -> tuple[Column, Column, ArrayType]:
    """Widen the array and/or element to their common element type.

    Snowflake's ARRAY_APPEND/ARRAY_PREPEND/ARRAY_INSERT cast the element to
    the array's element type, which can truncate (e.g. float → int).  Spark
    instead widens the array to the common type.  This helper performs
    explicit casts so the Snowflake behavior matches Spark.
    """
    arr_elem_type = arr_type.element_type if isinstance(arr_type, ArrayType) else None
    if arr_elem_type is not None:
        common = _find_common_type([arr_elem_type, elem_type])
    else:
        common = elem_type

    if arr_elem_type is not None and common != arr_elem_type:
        arr_col = snowpark_fn.cast(arr_col, ArrayType(common))
    if common != elem_type:
        elem_col = snowpark_fn.cast(elem_col, common)

    return arr_col, elem_col, ArrayType(common) if common else arr_type


def _coerce_two_arrays(
    arr1_col: Column,
    arr1_type: DataType,
    arr2_col: Column,
    arr2_type: DataType,
    contains_null: bool,
) -> tuple[Column, Column, ArrayType]:
    """Widen two arrays to a common element type.

    When Spark combines two arrays (union, except, intersect) with different
    element types it widens both to the common element type.  Snowflake does
    not, so we cast explicitly.
    """
    elem1 = arr1_type.element_type if isinstance(arr1_type, ArrayType) else None
    elem2 = arr2_type.element_type if isinstance(arr2_type, ArrayType) else None

    if elem1 is not None and elem2 is not None:
        common = _find_common_type([elem1, elem2])
    else:
        common = elem1 or elem2

    result_type = ArrayType(common) if common else arr1_type
    result_element_type = result_type.element_type

    if elem1 is not None and common != elem1:
        arr1_col = snowpark_fn.cast(arr1_col, result_type)
    if elem2 is not None and common != elem2:
        arr2_col = snowpark_fn.cast(arr2_col, result_type)

    return (
        arr1_col,
        arr2_col,
        ArrayType(result_element_type, contains_null=_inner_nullable(contains_null)),
    )


def _find_common_type(
    types: list[DataType],
    func_name: str = None,
    widen_to_string: bool = False,
    narrow_string: bool = False,
    merge_structs: bool = False,
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
                return ArrayType(
                    typ,
                    contains_null=_inner_nullable(
                        type1.contains_null or type2.contains_null
                    ),
                )
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
                if [f.name for f in fields1] != [f.name for f in fields2]:
                    if not merge_structs:
                        exception = AnalysisException(exception_base_message)
                        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
                        raise exception
                    fields2_by_name = {f.name: f for f in fields2}
                    fields1_by_name = {f.name: f for f in fields1}
                    nullable = _inner_nullable(True)
                    fields = [
                        StructField(
                            f.name,
                            _common(f.datatype, fields2_by_name[f.name].datatype)
                            if f.name in fields2_by_name
                            else f.datatype,
                            nullable=nullable,
                            _is_column=False,
                        )
                        for f in fields1
                    ] + [
                        StructField(
                            f.name, f.datatype, nullable=nullable, _is_column=False
                        )
                        for f in fields2
                        if f.name not in fields1_by_name
                    ]
                    return StructType(fields)
                fields = []
                for idx, field in enumerate(fields1):
                    typ = _common(field.datatype, fields2[idx].datatype)
                    fields.append(
                        StructField(
                            field.name,
                            typ,
                            nullable=_inner_nullable(
                                field.nullable or fields2[idx].nullable
                            ),
                            _is_column=False,
                        )
                    )
                return StructType(fields)
            case (MapType(), MapType()):
                key_type = _common(type1.key_type, type2.key_type)
                value_type = _common(type1.value_type, type2.value_type)
                return MapType(
                    key_type,
                    value_type,
                    value_contains_null=_inner_nullable(
                        type1.value_contains_null or type2.value_contains_null
                    ),
                )
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

        lambda_typer = LambdaExpressionTyper(artificial_df, typer)

        with resolving_lambda_function(names):
            return map_expression(
                (
                    lambda_exp.lambda_function.function
                    if resolve_only_body
                    else lambda_exp
                ),
                column_mapping,
                lambda_typer,
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

            initial_value_col = arg2_tc.col
            if isinstance(arg2_tc.typ, _NumericType):
                # Snowpark inlines numeric literals without their cast (see
                # numeric_to_sql_without_cast), so a `lit(0.0)` initial value
                # reaches Snowflake as a bare `0.0`, which REDUCE infers as
                # NUMBER(1,0) and overflows on the first non-trivial step.
                # Force the cast to survive into the SQL.
                initial_value_col = snowpark_fn.cast(initial_value_col, arg2_tc.typ)
            result_exp = snowpark_fn.function("reduce")(
                arg1_tc.col, initial_value_col, arg3_tc.col
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
            _randomize_lambda_args_names(lambda_exp)
            ([lambda_body_name], fn_body) = _resolve_lambda(
                lambda_exp, [arr_el_typ], resolve_only_body=True
            )
            l_arg = lambda_exp.lambda_function.arguments[0].name_parts[0]
            analyzer = Session.get_active_session()._analyzer
            predicate_sql = analyzer.analyze(fn_body.col._expression, defaultdict())
            result_exp = snowpark_fn.function("reduce")(
                arg1_tc.col,
                snowpark_fn.lit(False),
                snowpark_fn.sql_expr(f"(acc, {l_arg}) -> acc or ({predicate_sql})"),
            )
            result_type = BooleanType()
            snowpark_arg_names = [
                arg1_name,
                f"lambdafunction({lambda_body_name}, namedlambdavariable())",
            ]
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
                l_arg2, "get(x, 'value')"
            )
            transform_exp = snowpark_fn.sql_expr(f"x -> ({transform_sql})::boolean")
            last_win_dedup = global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            reduce_exp = snowpark_fn.function("reduce")(
                snowpark_fn.function("filter")(
                    snowpark_fn.call_function("MAP_ENTRIES", arg1_tc.col),
                    transform_exp,
                ),
                snowpark_fn.object_construct(),
                snowpark_fn.sql_expr(
                    # value is cast to variant because object_insert doesn't allow structured types,
                    # and structured types are not coercible to variant
                    # TODO: allow structured types in object_insert?
                    f"(acc, e) -> object_insert(acc, e:key, nvl(e:value::variant, parse_json('null')), {last_win_dedup})"
                ),
            )
            result_type = arg1_tc.typ
            result_exp = snowpark_fn.cast(reduce_exp, result_type)
            snowpark_arg_names = [
                arg1_name,
                f"lambdafunction({lambda_body_name}, namedlambdavariable(), namedlambdavariable())",
            ]
        case "map_zip_with":

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

            # Cast both maps to the common key type so that key comparisons
            # (GET, ARRAY_CONTAINS) and object_insert work across type boundaries.
            arg1_col = (
                snowpark_fn.cast(arg1_tc.col, MapType(key_type, val1_type))
                if key1_type != key_type
                else arg1_tc.col
            )
            arg2_col = (
                snowpark_fn.cast(arg2_tc.col, MapType(key_type, val2_type))
                if key2_type != key_type
                else arg2_tc.col
            )

            analyzer = Session.get_active_session()._analyzer
            fn_sql = analyzer.analyze(fn_body.col._expression, defaultdict())
            arg1_sql = analyzer.analyze(arg1_col._expression, defaultdict())
            arg2_sql = analyzer.analyze(arg2_col._expression, defaultdict())
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
            from_map1 = snowpark_fn.function("transform")(
                snowpark_fn.call_function("MAP_ENTRIES", arg1_col),
                snowpark_fn.sql_expr(
                    f"e -> object_construct_keep_null('k', e:key, 'v1', e:value::variant, 'v2', get(to_variant({arg2_sql}), to_varchar(e:key)))"
                ),
            )
            only_in_map2 = snowpark_fn.function("transform")(
                snowpark_fn.function("filter")(
                    snowpark_fn.call_function("MAP_ENTRIES", arg2_col),
                    snowpark_fn.sql_expr(
                        f"e -> NOT array_contains(e:key::variant, map_keys({arg1_sql})::array)"
                    ),
                ),
                snowpark_fn.sql_expr(
                    "e -> object_construct_keep_null('k', e:key, 'v1', NULL, 'v2', e:value::variant)"
                ),
            )
            array_of_maps_exp = snowpark_fn.call_function(
                "ARRAY_CAT", from_map1, only_in_map2
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
            key_type, val_type = _get_map_types(arg1_tc)

            lambda_exp = exp.unresolved_function.arguments[1]
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
                l_arg2, "get(x, 'value')"
            )
            last_win_dedup = global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            reduce_exp = snowpark_fn.function("reduce")(
                snowpark_fn.call_function("MAP_ENTRIES", arg1_tc.col),
                snowpark_fn.object_construct(),
                snowpark_fn.sql_expr(
                    f"(acc, x) -> object_insert(acc, {fn_sql_with_replaced_args}, nvl(x:value::variant, parse_json('null')), {last_win_dedup})"
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
            key_type, val_type = _get_map_types(arg1_tc)

            lambda_exp = exp.unresolved_function.arguments[1]
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
                l_arg2, "get(x, 'value')"
            )
            last_win_dedup = global_config.spark_sql_mapKeyDedupPolicy == "LAST_WIN"
            reduce_exp = snowpark_fn.function("reduce")(
                snowpark_fn.call_function("MAP_ENTRIES", arg1_tc.col),
                snowpark_fn.object_construct(),
                snowpark_fn.sql_expr(
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
             - Replace lambda arg references in SQL with NULLIF(get(x,'$N'), PARSE_JSON('null')) accessors
               (NULLIF converts JSON null from arrays_zip padding into SQL NULL so that
               COALESCE/IFNULL correctly skips padded positions)
             - Construct a new lambda 'x -> modified_sql'
             - Apply `transform` function to transform the zipped array using that lambda
            """
            arr2 = exp.unresolved_function.arguments[1]
            ([arg2_name], arg2_tc) = map_expression(arr2, column_mapping, typer)

            # Cast to semi-structured arrays before zipping — structured arrays
            # cause "Typed object schema mismatch" with get(x, '$1') accessors.
            zip_exp = snowpark_fn.arrays_zip(
                arg1_tc.col.cast(ArrayType()), arg2_tc.col.cast(ArrayType())
            )
            lambda_exp = exp.unresolved_function.arguments[2]
            # Due to lack of direct equivalent API in Snowflake, we need to transform the lambda expression.
            # Rather than traversing the entire lambda AST, we use string manipulation on the query.
            # We randomize lambda argument names to minimize the risk of accidental replacements in the query.
            orig_arg1 = lambda_exp.lambda_function.arguments[0].name_parts[0]
            orig_arg2 = lambda_exp.lambda_function.arguments[1].name_parts[0]
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
            # Restore original field names in struct constructions before
            # replacing value references — .replace() is substring-based and
            # would otherwise clobber single/double-quoted field name strings.
            for _rand, _orig in [(l_arg1, orig_arg1), (l_arg2, orig_arg2)]:
                fn_sql = fn_sql.replace(f"'{_rand}'", f"'{_orig}'")
                fn_sql = fn_sql.replace(f'"{_rand}"', f'"{_orig}"')
            accessor1 = "NULLIF(get(x, '$1'), PARSE_JSON('null'))"
            accessor2 = "NULLIF(get(x, '$2'), PARSE_JSON('null'))"
            transform_sql = fn_sql.replace(l_arg1, accessor1).replace(l_arg2, accessor2)
            transform_exp = snowpark_fn.sql_expr(f"x -> {transform_sql}")
            snowpark_arg_names = [
                arg1_name,
                arg2_name,
                f"lambdafunction({lambda_body_name}, namedlambdavariable(), namedlambdavariable())",
            ]
            transform_result = snowpark_fn.function("transform")(zip_exp, transform_exp)
            # Snowflake's ARRAYS_ZIP returns [{}] for two empty arrays instead
            # of []. That spurious element causes transform to emit [null].
            # Guard with an explicit empty-array check.
            result_exp = snowpark_fn.iff(
                snowpark_fn.array_size(arg1_tc.col)
                + snowpark_fn.array_size(arg2_tc.col)
                == snowpark_fn.lit(0),
                snowpark_fn.array_construct(),
                transform_result,
            )
            # If the lambda body returns a struct, its field names carry the
            # randomized lambda-arg suffix.  Rename them back to the originals.
            body_type = fn_body.typ
            if isinstance(body_type, StructType):
                rename = {l_arg1: orig_arg1, l_arg2: orig_arg2}
                body_type = StructType(
                    [
                        StructField(
                            rename.get(f.name, f.name),
                            f.datatype,
                            f.nullable,
                        )
                        for f in body_type.fields
                    ],
                    structured=body_type.structured,
                )
            result_type = ArrayType(body_type)
            result_exp = snowpark_fn.cast(result_exp, result_type)
            result_exp = TypedColumn(result_exp, lambda: [result_type])
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
    Legacy AES implementation using Snowflake's ENCRYPT / DECRYPT / TRY_DECRYPT.

    These derive the AES key from the passphrase (PBKDF2), so the produced
    ciphertext is NOT byte-compatible with Spark. Retained as a fallback behind
    the ``snowpark.connect.enable_aes_raw_functions`` flag (set it to ``false``)
    for the ENCRYPT_RAW / DECRYPT_RAW implementation.
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


def _aes_method_string(encryption_method, padding):
    """Build the encryption method string like 'AES-GCM' or 'AES-ECB/pad:PKCS'.

    Spark's DEFAULT padding resolves based on mode:
      ECB/CBC → PKCS, GCM → NONE (no padding suffix).
    """
    effective_mode = snowpark_fn.when(
        encryption_method == snowpark_fn.lit("DEFAULT"), "GCM"
    ).otherwise(encryption_method)

    resolved_padding = snowpark_fn.when(
        padding == snowpark_fn.lit("DEFAULT"),
        snowpark_fn.when(
            effective_mode == snowpark_fn.lit("GCM"), snowpark_fn.lit("NONE")
        ).otherwise(snowpark_fn.lit("PKCS")),
    ).otherwise(padding)

    padding_suffix = snowpark_fn.when(
        resolved_padding == snowpark_fn.lit("NONE"), snowpark_fn.lit("")
    ).otherwise(snowpark_fn.concat(snowpark_fn.lit("/pad:"), resolved_padding))

    return snowpark_fn.concat(
        snowpark_fn.lit("AES-"),
        effective_mode,
        padding_suffix,
    )


def _aes_effective_mode(encryption_method):
    """Resolve the effective AES mode (uppercase), mapping DEFAULT to GCM."""
    return snowpark_fn.upper(
        snowpark_fn.when(
            encryption_method == snowpark_fn.lit("DEFAULT"),
            snowpark_fn.lit("GCM"),
        ).otherwise(encryption_method)
    )


def _ensure_binary(col, col_type):
    if isinstance(col_type, BinaryType):
        return col
    return snowpark_fn.to_binary(col, "UTF-8")


def _aes_decrypt_raw_helper(
    function_name, value, key, key_type, aad, aad_type, encryption_method, padding
):
    """
    Decrypt using DECRYPT_RAW / TRY_DECRYPT_RAW.

    Spark's encrypted binary format packs IV and tag into the ciphertext:
      ECB: ciphertext (no IV)
      CBC: IV (16 bytes) || ciphertext
      GCM: IV (12 bytes) || ciphertext || auth_tag (16 bytes)

    DECRYPT_RAW requires different call signatures for AEAD (GCM) vs non-AEAD
    (ECB/CBC) modes — passing a tag parameter for non-AEAD modes errors.
    We use the try-variant for the non-matching branch to absorb errors from
    garbage inputs, then COALESCE to pick the successful result.
    """
    null_check = (
        snowpark_fn.is_null(value)
        | snowpark_fn.is_null(key)
        | snowpark_fn.is_null(encryption_method)
        | snowpark_fn.is_null(padding)
        | snowpark_fn.is_null(aad)
    )

    key_binary = _ensure_binary(key, key_type)
    aad_binary = _ensure_binary(aad, aad_type)
    method_str = _aes_method_string(encryption_method, padding)
    effective_mode = _aes_effective_mode(encryption_method)
    input_len = snowpark_fn.length(value)

    try_fn = snowpark_fn.function("TRY_DECRYPT_RAW")

    # --- Non-GCM path (ECB / CBC): 6-arg call (value, key, iv, aad, method, tag) ---
    # DECRYPT_RAW's 5-arg overload is (value, key, iv, method, tag) which
    # collides with our intent of (value, key, iv, aad, method).  Use the
    # unambiguous 6-arg form with NULL aad and NULL tag for non-AEAD modes.
    non_gcm_iv = snowpark_fn.when(
        effective_mode == snowpark_fn.lit("ECB"), snowpark_fn.lit(None)
    ).otherwise(snowpark_fn.substring(value, 1, 16))

    non_gcm_ciphertext = snowpark_fn.when(
        effective_mode == snowpark_fn.lit("ECB"), value
    ).otherwise(snowpark_fn.substring(value, 17, input_len - 16))

    non_gcm_result = try_fn(
        non_gcm_ciphertext,
        key_binary,
        non_gcm_iv,
        snowpark_fn.lit(None).cast(BinaryType()),
        method_str,
        snowpark_fn.lit(None).cast(BinaryType()),
    )

    # --- GCM path: 6-arg call with AAD and tag ---
    gcm_iv = snowpark_fn.substring(value, 1, 12)
    gcm_ciphertext = snowpark_fn.substring(value, 13, input_len - 28)
    gcm_tag = snowpark_fn.substring(value, input_len - 15, 16)

    gcm_result = try_fn(
        gcm_ciphertext, key_binary, gcm_iv, aad_binary, method_str, gcm_tag
    )

    result = snowpark_fn.when(
        effective_mode == snowpark_fn.lit("GCM"), gcm_result
    ).otherwise(non_gcm_result)

    return snowpark_fn.when(null_check, snowpark_fn.lit(None)).otherwise(result)


def _aes_encrypt_raw_helper(
    value,
    value_type,
    key,
    key_type,
    aad,
    aad_type,
    encryption_method,
    padding,
    iv_param,
    iv_type,
):
    """
    Encrypt using ENCRYPT_RAW and reassemble in Spark's binary format:
      ECB: ciphertext
      CBC: IV || ciphertext
      GCM: IV || ciphertext || auth_tag
    """
    null_check = (
        snowpark_fn.is_null(value)
        | snowpark_fn.is_null(key)
        | snowpark_fn.is_null(encryption_method)
        | snowpark_fn.is_null(padding)
        | snowpark_fn.is_null(aad)
    )

    value_binary = _ensure_binary(value, value_type)
    key_binary = _ensure_binary(key, key_type)
    aad_binary = _ensure_binary(aad, aad_type)
    method_str = _aes_method_string(encryption_method, padding)
    effective_mode = _aes_effective_mode(encryption_method)

    # Determine the user-provided IV (if any).
    if isinstance(iv_type, StringType):
        user_iv = snowpark_fn.when(
            snowpark_fn.length(iv_param) == 0, snowpark_fn.lit(None)
        ).otherwise(snowpark_fn.to_binary(iv_param, "UTF-8"))
    elif isinstance(iv_type, BinaryType):
        user_iv = snowpark_fn.when(
            snowpark_fn.length(iv_param) == 0, snowpark_fn.lit(None)
        ).otherwise(iv_param)
    else:
        user_iv = snowpark_fn.lit(None)

    # When no IV is provided, generate a deterministic one from a hash of the
    # plaintext and key.  Passing NULL to ENCRYPT_RAW makes Snowflake pick a
    # random IV on *every* evaluation, but the Snowpark Column model may
    # duplicate the ENCRYPT_RAW expression in the SQL (once per GET on the
    # result VARIANT), causing each copy to produce a different ciphertext.
    # A deterministic IV ensures all copies encrypt identically.
    md5_fn = snowpark_fn.builtin("MD5_BINARY")
    deterministic_iv = md5_fn(snowpark_fn.concat(value_binary, key_binary))
    gcm_iv_from_hash = snowpark_fn.substring(deterministic_iv, 1, 12)

    effective_iv = snowpark_fn.when(
        snowpark_fn.is_null(user_iv),
        snowpark_fn.when(
            effective_mode == snowpark_fn.lit("ECB"), snowpark_fn.lit(None)
        )
        .when(effective_mode == snowpark_fn.lit("GCM"), gcm_iv_from_hash)
        .otherwise(deterministic_iv),
    ).otherwise(user_iv)

    effective_aad = snowpark_fn.when(
        effective_mode == snowpark_fn.lit("GCM"), aad_binary
    ).otherwise(snowpark_fn.lit(None))

    encrypt_fn = snowpark_fn.function("ENCRYPT_RAW")
    encrypted = encrypt_fn(
        value_binary, key_binary, effective_iv, effective_aad, method_str
    )

    as_binary_fn = snowpark_fn.builtin("AS_BINARY")
    enc_iv = as_binary_fn(snowpark_fn.get(encrypted, snowpark_fn.lit("iv")))
    enc_ciphertext = as_binary_fn(
        snowpark_fn.get(encrypted, snowpark_fn.lit("ciphertext"))
    )
    enc_tag = as_binary_fn(snowpark_fn.get(encrypted, snowpark_fn.lit("tag")))

    result = (
        snowpark_fn.when(effective_mode == snowpark_fn.lit("ECB"), enc_ciphertext)
        .when(
            effective_mode == snowpark_fn.lit("GCM"),
            snowpark_fn.concat(enc_iv, enc_ciphertext, enc_tag),
        )
        .otherwise(snowpark_fn.concat(enc_iv, enc_ciphertext))
    )

    return snowpark_fn.when(null_check, snowpark_fn.lit(None)).otherwise(result)


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


def _spark_add_months(start_col: Column, n_col) -> Column:
    """Apply Spark's `add_months` semantics on top of Snowflake's `ADD_MONTHS`.

    Snowflake snaps the result to the last day of the target month whenever the
    input is the last day of its month (e.g. `ADD_MONTHS('2024-02-29', 1)`
    returns `2024-03-31`). Spark instead preserves day-of-month and only clamps
    when the target month is shorter (e.g. `add_months('2024-02-29', 1)` returns
    `2024-03-29`). We undo the snap by shifting back to
    `min(day(start), day(last_day(am)))`.
    """
    am = snowpark_fn.add_months(start_col, n_col)
    correction = snowpark_fn.least(
        snowpark_fn.dayofmonth(start_col),
        snowpark_fn.dayofmonth(snowpark_fn.last_day(am)),
    ) - snowpark_fn.dayofmonth(am)
    return snowpark_fn.dateadd("day", correction, am)


def _spark_add_months_sql(start_sql: str, n_sql: str) -> str:
    """SQL-fragment variant of :func:`_spark_add_months`.

    Useful when the value cannot be expressed via the Column API, e.g. inside a
    higher-order-function lambda where the iteration variable is a SQL
    identifier rather than a Snowpark column.
    """
    am = f"ADD_MONTHS({start_sql}, {n_sql})"
    return (
        f"DATEADD('day', "
        f"LEAST(DAY({start_sql}), DAY(LAST_DAY({am}))) - DAY({am}), "
        f"{am})"
    )


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
                cleaned = _try_cast_to_double(col_name, arg_type)
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
) -> TypedColumn:
    # Spark BinaryArithmetic: nullable = left.nullable || right.nullable
    # Decimal LEGACY mode: overflow returns null → always nullable
    # DivModLike (divide): division by zero returns null → always nullable
    nullable = arg1.nullable or arg2.nullable
    if isinstance(target_type, DecimalType) and (
        not should_raise_on_overflow or operation_name == "divide"
    ):
        nullable = True
    ft = FieldType(target_type, nullable)

    if isinstance(target_type, _IntegralType):
        raw_result = op(arg1.col, arg2.col)
        result_col = apply_arithmetic_overflow_with_ansi_check(
            raw_result, target_type, should_raise_on_overflow, operation_name
        )
        return TypedColumn(
            result_col,
            lambda: [ft],
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

    direct_op = op(arg1.col, arg2.col)

    if overflow_possible:
        op_for_overflow_check = op(
            arg1.col.cast(DoubleType()), arg2.col.cast(DoubleType())
        )
        if not isinstance(arg1.typ, DecimalType) or not isinstance(
            arg2.typ, DecimalType
        ):
            direct_op = op(_cast_arg(arg1), _cast_arg(arg2))

        result_col = _cast_arithmetic_operation_result(
            op_for_overflow_check, direct_op, target_type, should_raise_on_overflow
        )
    else:
        result_col = direct_op.cast(target_type)

    return TypedColumn(result_col, lambda f=ft: [f])


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
                ).col,
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


def _cast_to_ts_type(result_exp: Column, ts_type: TimestampType) -> Column:
    """Cast result_exp to ts_type.

    For LTZ→NTZ uses CONVERT_TIMEZONE(session_tz, col) to replicate Spark's
    wall-clock semantics: Cast.scala convertTz(ts, UTC, sessionTZ) renders the
    LTZ instant in the session timezone and strips the zone label.
    Snowflake's direct CAST(TIMESTAMP_LTZ AS TIMESTAMP_NTZ) is rejected.
    """
    if ts_type == TimestampType(snowpark.types.TimestampTimeZone.NTZ):
        return snowpark_fn.convert_timezone(
            snowpark_fn.lit(global_config.spark_sql_session_timeZone), result_exp
        ).cast(ts_type)
    return snowpark_fn.cast(result_exp, ts_type)


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
    function,
    parsed_value: Column,
    format: Column,
    precision: int,
    scale: int,
    format_arg_name: str,
    spark_function_name: str,
    session: Session,
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

    spark_format_value = _resolve_foldable_string_expression(
        arg_col=format,
        arg_name=format_arg_name,
        spark_function_name=spark_function_name,
        session=session,
    )

    if spark_format_value is None:
        return snowpark_fn.lit(None)

    s_at_start = spark_format_value.startswith("S")
    s_at_end = spark_format_value.endswith("S")
    pr_at_end = spark_format_value.endswith("PR")

    snowflake_format_value = spark_format_value.replace("PR", "").replace(".", "D")
    if "D" in snowflake_format_value:
        before_decimal, after_decimal = snowflake_format_value.split("D", 1)
        decimal_separator = "" if after_decimal == "" else "D"
        # In the fractional part, Snowflake's TRY_TO_NUMBER("0") behavior differs from Spark.
        # Normalize zeros to nines to preserve Spark-compatible parsing semantics.
        snowflake_format_value = (
            f"{before_decimal}{decimal_separator}{after_decimal.replace('0', '9')}"
        )
    format = snowpark_fn.lit(snowflake_format_value)

    bracket_at_start = parsed_value.startswith("<")
    bracket_at_end = parsed_value.endswith(">")
    has_missing_starting_sign = ~plus_at_start & ~minus_at_start
    has_missing_ending_sign = ~plus_at_end & ~minus_at_end
    has_sign_in_unsigned_format = plus_at_start | minus_at_start
    is_pr_formatted = bracket_at_start & bracket_at_end

    parsed_value_with_prefix_plus = snowpark_fn.concat(
        snowpark_fn.lit("+"), parsed_value
    )

    parsed_value_with_suffix_plus = snowpark_fn.concat(
        parsed_value, snowpark_fn.lit("+")
    )

    empty_parsed_value = snowpark_fn.lit("")

    parsed_value_with_minus_sign = snowpark_fn.regexp_replace(
        snowpark_fn.regexp_replace(parsed_value, "^<", "-"), ">$"
    )

    default_expr = function(parsed_value, format, precision, scale)
    when_chain = None

    def _add_branch(
        chain: Optional[Column], condition: Column, value: Column
    ) -> Column:
        return (
            snowpark_fn.when(condition, value)
            if chain is None
            else chain.when(condition, value)
        )

    if s_at_start:
        when_chain = _add_branch(
            when_chain,
            has_missing_starting_sign,
            function(parsed_value_with_prefix_plus, format, precision, scale),
        )
    if s_at_end:
        when_chain = _add_branch(
            when_chain,
            has_missing_ending_sign,
            function(parsed_value_with_suffix_plus, format, precision, scale),
        )
    if pr_at_end:
        when_chain = _add_branch(
            when_chain,
            is_pr_formatted,
            function(parsed_value_with_minus_sign, format, precision, scale),
        )
    if not s_at_start:
        when_chain = _add_branch(
            when_chain,
            has_sign_in_unsigned_format,
            function(empty_parsed_value, format, precision, scale),
        )

    return default_expr if when_chain is None else when_chain.otherwise(default_expr)


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


def _validate_literal_like_escape_pattern(pattern: str, escape: str) -> None:
    """Plan-time validation for LIKE/ILIKE pattern + escape literals.

    Mirrors :class:`org.apache.spark.sql.catalyst.util.StringUtils.escapeLikeRegex`:
    raises :class:`AnalysisException` with ``INVALID_FORMAT.ESC_AT_THE_END`` /
    ``INVALID_FORMAT.ESC_IN_THE_MIDDLE`` if the escape character is at the end
    of the pattern or precedes a non-wildcard character. Returns silently for
    valid patterns or when ``pattern`` / ``escape`` is ``None`` (the runtime
    path handles NULL inputs).
    """
    if pattern is None or escape is None or len(escape) != 1:
        return

    escape_token = escape[0]
    i = 0
    n = len(pattern)

    while i < n:
        current_token = pattern[i]
        if current_token != escape_token:
            i += 1
            continue

        if i + 1 >= n:
            exception = AnalysisException(
                f"[INVALID_FORMAT.ESC_AT_THE_END] The format is invalid: '{pattern}'. "
                f"The escape character is not allowed to end with."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        next_token = pattern[i + 1]
        if next_token != "%" and next_token != "_" and next_token != escape_token:
            exception = AnalysisException(
                f"[INVALID_FORMAT.ESC_IN_THE_MIDDLE] The format is invalid: '{pattern}'. "
                f"The escape character is not allowed to precede '{next_token}'."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
            raise exception
        i += 2


def _validate_expression_like_escape_pattern(
    value_col: Column, pattern_col: Column, escape_col: Column
) -> Column:
    """Validate a non-literal LIKE/ILIKE pattern + escape server-side.

    Mirrors :class:`org.apache.spark.sql.catalyst.util.StringUtils.escapeLikeRegex`
    using a pure-SQL CASE expression: three nested ``REPLACE`` calls strip the
    valid escape sequences (``esc+esc``, ``esc+%``, ``esc+_``) from the
    pattern, and any leftover instance of the escape character is invalid.
    A leftover escape at the end of the reduced string maps to
    ``INVALID_FORMAT.ESC_AT_THE_END``; otherwise it is ``ESC_IN_THE_MIDDLE``
    and we surface the offending follow-up character.

    The CASE short-circuits when ``value_col`` is NULL to match Spark's
    ``StringRegexExpression.nullSafeEval`` behavior. Errors are raised via
    :func:`_raise_error_helper`, which produces an ``AnalysisException``
    through the same Snowflake-error round-trip used by ``assert_true``,
    ``split_part`` and friends; this avoids a Python UDF (and the
    cloudpickle serialization caveats that come with one).

    Returns the StringType-cast pattern on success so the caller can pass it
    straight to Snowflake's like/ilike builtin. The cast is required for both
    the validator internals (Snowflake's ``REPLACE``/``POSITION``/``SUBSTRING``
    expect strings, and ``_raise_error_helper`` ``try_cast``s each message
    column to ``StringType``) and for correct LIKE semantics: Snowflake's
    CASE type unification picks NUMBER over VARCHAR when the success and
    error branches disagree, so passing the original numeric ``pattern_col``
    would make e.g. ``'1' LIKE 1`` evaluate to ``false`` instead of ``true``.
    """
    # Spark's Like coerces both pattern and escape to StringType before
    # validation (e.g. ``date(...)`` or integer patterns from implicit
    # type coercion).
    pattern_col_str = pattern_col.cast(StringType())
    escape_col_str = escape_col.cast(StringType())
    empty_literal = snowpark_fn.lit("")
    escape_then_escape = snowpark_fn.concat(escape_col_str, escape_col_str)
    escape_then_percent = snowpark_fn.concat(escape_col_str, snowpark_fn.lit("%"))
    escape_then_underscore = snowpark_fn.concat(escape_col_str, snowpark_fn.lit("_"))
    reduced_pattern = snowpark_fn.replace(
        snowpark_fn.replace(
            snowpark_fn.replace(pattern_col_str, escape_then_escape, empty_literal),
            escape_then_percent,
            empty_literal,
        ),
        escape_then_underscore,
        empty_literal,
    )
    leftover_escape_position = snowpark_fn.position(escape_col_str, reduced_pattern)
    reduced_pattern_length = snowpark_fn.length(reduced_pattern)
    character_after_leftover_escape = snowpark_fn.substring(
        reduced_pattern,
        leftover_escape_position + snowpark_fn.lit(1),
        snowpark_fn.lit(1),
    )

    raise_error = _raise_error_helper(StringType(), AnalysisException)

    return (
        snowpark_fn.when(value_col.is_null(), pattern_col_str)
        .when(
            pattern_col_str.is_null()
            | escape_col_str.is_null()
            | (snowpark_fn.length(escape_col_str) != snowpark_fn.lit(1)),
            pattern_col_str,
        )
        .when(leftover_escape_position == snowpark_fn.lit(0), pattern_col_str)
        .when(
            leftover_escape_position == reduced_pattern_length,
            raise_error(
                snowpark_fn.lit(
                    "[INVALID_FORMAT.ESC_AT_THE_END] The format is invalid: '"
                ),
                pattern_col_str,
                snowpark_fn.lit("'. The escape character is not allowed to end with."),
            ),
        )
        .otherwise(
            raise_error(
                snowpark_fn.lit(
                    "[INVALID_FORMAT.ESC_IN_THE_MIDDLE] The format is invalid: '"
                ),
                pattern_col_str,
                snowpark_fn.lit("'. The escape character is not allowed to precede '"),
                character_after_leftover_escape,
                snowpark_fn.lit("'."),
            )
        )
    )


def _validate_like_pattern_at_plan_or_runtime(
    pattern_proto: expressions_proto.Expression,
    escape_proto: expressions_proto.Expression,
    value_col: Column,
    pattern_col: Column,
    escape_col: Column,
) -> Column:
    """Validate LIKE/ILIKE pattern against escape rules.

    If both pattern and escape are string literals, perform the validation at
    plan time and raise AnalysisException directly. Otherwise wrap the pattern
    column with a server-side CASE expression that mirrors the same logic and
    raises via :func:`_raise_error_helper`. The runtime path also
    short-circuits on NULL values to match Spark's nullSafeEval behavior.
    """
    pattern_is_literal = pattern_proto.WhichOneof("expr_type") == "literal"
    escape_is_literal = escape_proto.WhichOneof("expr_type") == "literal"
    if pattern_is_literal and escape_is_literal:
        pattern_value = unwrap_literal(pattern_proto)
        escape_value = unwrap_literal(escape_proto)
        if isinstance(pattern_value, str) and isinstance(escape_value, str):
            _validate_literal_like_escape_pattern(pattern_value, escape_value)
            return pattern_col
    return _validate_expression_like_escape_pattern(value_col, pattern_col, escape_col)


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


# All 28 entries from java.time.ZoneId.SHORT_IDS.
# EST/HST/MST use POSIX Etc/GMT notation because Java treats them as fixed
# offsets (no DST), which matches the Etc/GMT semantics exactly.
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
    "EST": "Etc/GMT+5",
    "HST": "Etc/GMT+10",
    "IET": "America/Indiana/Indianapolis",
    "IST": "Asia/Kolkata",
    "JST": "Asia/Tokyo",
    "MIT": "Pacific/Apia",
    "MST": "Etc/GMT+7",
    "NET": "Asia/Yerevan",
    "NST": "Pacific/Auckland",
    "PLT": "Asia/Karachi",
    "PNT": "America/Phoenix",
    "PRT": "America/Puerto_Rico",
    "PST": "America/Los_Angeles",
    "SST": "Pacific/Guadalcanal",
    "VST": "Asia/Ho_Chi_Minh",
}


def _literal_offset_minutes(tz: str) -> int | None:
    """Kept for any remaining callers; delegates to _literal_offset_seconds."""
    secs = _literal_offset_seconds(tz)
    return None if secs is None else secs // 60


def _literal_offset_seconds(tz: str) -> int | None:
    """Parse any Spark-supported UTC offset string to total seconds.

    Handles all formats accepted by Java's ZoneOffset.of():
      Z
      +H, +HH
      +HHMM, +HHMMSS
      +H:M, +H:MM, +HH:M, +HH:MM          (1 or 2 digit minutes)
      +H:MM:SS, +HH:MM:SS                  (seconds exactly 2 digits)
      (and negative equivalents)

    Validates:
      - no-colon body length must be exactly 1, 2, 4, or 6 chars
      - minutes 0-59, seconds 0-59
      - total offset within ±18h (±64800 s)

    Returns None if invalid (caller treats as IANA name, Snowflake errors).
    """
    if tz == "Z":
        return 0
    if not tz or tz[0] not in ("+", "-"):
        return None
    sign = 1 if tz[0] == "+" else -1
    body = tz[1:]
    try:
        if ":" in body:
            parts = body.split(":")
            # Only 2 or 3 colon-separated parts allowed
            if len(parts) not in (2, 3):
                return None
            # Minutes: 1 or 2 digits, value 0-59
            if len(parts[1]) > 2 or not parts[1].isdigit():
                return None
            h, m = int(parts[0]), int(parts[1])
            if m > 59:
                return None
            if len(parts) == 3:
                # Seconds: exactly 2 digits, value 0-59
                if len(parts[2]) != 2 or not parts[2].isdigit():
                    return None
                s = int(parts[2])
                if s > 59:
                    return None
            else:
                s = 0
            result = sign * (h * 3600 + m * 60 + s)
        elif len(body) == 6:  # +HHMMSS exactly
            m, s = int(body[2:4]), int(body[4:6])
            if m > 59 or s > 59:
                return None
            result = sign * (int(body[:2]) * 3600 + m * 60 + s)
        elif len(body) == 4:  # +HHMM exactly
            m = int(body[2:4])
            if m > 59:
                return None
            result = sign * (int(body[:2]) * 3600 + m * 60)
        elif len(body) in (1, 2):  # +H or +HH
            result = sign * int(body) * 3600
        else:
            return None  # invalid body length (3, 5, 7+, ...)
    except (ValueError, IndexError):
        return None
    # Total offset must be within Java ZoneOffset valid range
    if abs(result) > 18 * 3600:
        return None
    return result


def _map_from_spark_tz(value: Column) -> Column:
    """Resolve a *literal* non-offset Spark timezone string to a Snowflake tz column.

    Only call this for compile-time string literals that are NOT UTC offset
    strings (those are handled via DATEADD at the call site).  Dynamic column
    values must use ``_build_utc_timestamp_expr`` instead.
    """
    assert isinstance(value._expression, Literal) and isinstance(
        value._expression.value, str
    ), "_map_from_spark_tz requires a string literal"
    literal_val = value._expression.value
    # Java 3-letter abbreviations (e.g. "CST" → "America/Chicago").
    if literal_val in _SPARK_TZ_MAPPINGS:
        return snowpark_fn.lit(_SPARK_TZ_MAPPINGS[literal_val])
    # IANA name — pass through unchanged.
    return snowpark_fn.lit(literal_val)


def _build_utc_timestamp_expr(
    ts_col: Column, tz_col: Column, *, from_utc: bool
) -> Column:
    """Build a pure-SQL expression for from_utc_timestamp / to_utc_timestamp.

      1. Java short IDs (ACT, CST, EST, …)  → convert_timezone with mapped IANA name
      2. UTC offset strings (+HH:MM/-HH:MM)  → DATEADD with dynamically parsed offset
      3. IANA names (Asia/Singapore, …)      → convert_timezone with tz as-is

    Args:
        ts_col:   The timestamp column to convert.
        tz_col:   The timezone string column (dynamic — not a literal).
        from_utc: True  → from_utc_timestamp semantics (UTC → local)
                  False → to_utc_timestamp semantics   (local → UTC)
    """

    def _conv(iana: str) -> Column:
        """convert_timezone for a known IANA name."""
        if from_utc:
            return snowpark_fn.from_utc_timestamp(ts_col, snowpark_fn.lit(iana))
        return snowpark_fn.to_utc_timestamp(ts_col, snowpark_fn.lit(iana))

    def _conv_dynamic() -> Column:
        """convert_timezone with tz_col as the runtime tz (IANA passthrough)."""
        if from_utc:
            return snowpark_fn.from_utc_timestamp(ts_col, tz_col)
        return snowpark_fn.to_utc_timestamp(ts_col, tz_col)

    # Build CASE/WHEN: start with NULL guard.
    result = snowpark_fn.when(tz_col.is_null(), snowpark_fn.lit(None))

    # 1. All 28 Java short IDs → convert_timezone with mapped IANA name.
    for spark_tz, iana_name in _SPARK_TZ_MAPPINGS.items():
        result = result.when(tz_col == snowpark_fn.lit(spark_tz), _conv(iana_name))

    # 2. "Z" → UTC, offset = 0 (Snowflake doesn't accept 'Z' as a tz name).
    result = result.when(tz_col == snowpark_fn.lit("Z"), _conv("UTC"))

    # 3. UTC offset strings (+/- prefix) → DATEADD with dynamically parsed offset.
    #
    #    Valid formats (Java ZoneOffset.of() semantics):
    #      +H:M, +H:MM, +HH:M, +HH:MM          (no seconds)
    #      +H:MM:SS, +HH:MM:SS                  (2-digit seconds)
    #      +H, +HH, +HHMM, +HHMMSS             (no-colon forms)
    #
    #    Invalid inputs fall through to the IANA passthrough → Snowflake error.
    #
    #    Validation applied:
    #      - exact string length per format (rejects +12345, -1234567, +3:123:0)
    #      - minutes 0-59, seconds 0-59
    #      - total offset |secs| ≤ 64800 (rejects +19:00, -18:00:01, etc.)
    #
    #    from_utc: local = UTC + offset  → add
    #    to_utc:   UTC   = local - offset → subtract
    is_offset = (snowpark_fn.substring(tz_col, 1, 1) == snowpark_fn.lit("+")) | (
        snowpark_fn.substring(tz_col, 1, 1) == snowpark_fn.lit("-")
    )
    sign = snowpark_fn.when(
        snowpark_fn.substring(tz_col, 1, 1) == snowpark_fn.lit("+"),
        snowpark_fn.lit(1),
    ).otherwise(snowpark_fn.lit(-1))

    # Format-validity predicates (colon position + total length)
    _len = snowpark_fn.length(tz_col)
    _p3c = snowpark_fn.substring(tz_col, 3, 1) == snowpark_fn.lit(":")
    _p4c = snowpark_fn.substring(tz_col, 4, 1) == snowpark_fn.lit(":")
    _p6c = snowpark_fn.substring(tz_col, 6, 1) == snowpark_fn.lit(":")
    _p7c = snowpark_fn.substring(tz_col, 7, 1) == snowpark_fn.lit(":")

    # +H:M(len=4), +H:MM(len=5), +H:MM:SS(len=8,pos6=':')
    _colon_h = _p3c & (
        (_len == snowpark_fn.lit(4))
        | (_len == snowpark_fn.lit(5))
        | ((_len == snowpark_fn.lit(8)) & _p6c)
    )
    # +HH:M(len=5), +HH:MM(len=6), +HH:MM:SS(len=9,pos7=':'), no colon at pos3
    _colon_hh = (
        _p4c
        & ~_p3c
        & (
            (_len == snowpark_fn.lit(5))
            | (_len == snowpark_fn.lit(6))
            | ((_len == snowpark_fn.lit(9)) & _p7c)
        )
    )
    # no-colon: +H(2), +HH(3), +HHMM(5), +HHMMSS(7)
    _nocolon = (
        ~_p3c
        & ~_p4c
        & (
            (_len == snowpark_fn.lit(2))
            | (_len == snowpark_fn.lit(3))
            | (_len == snowpark_fn.lit(5))
            | (_len == snowpark_fn.lit(7))
        )
    )
    _is_valid_fmt = _colon_h | _colon_hh | _nocolon

    # Hours: single-digit for +H:... forms, two-digit otherwise.
    hours = snowpark_fn.when(
        _p3c,
        snowpark_fn.substring(tz_col, 2, 1).cast(IntegerType()),
    ).otherwise(
        snowpark_fn.substring(tz_col, 2, 2).cast(IntegerType()),
    )
    # Minutes: position depends on format.
    mins = (
        snowpark_fn.when(
            _p3c,
            snowpark_fn.substring(tz_col, 4, 2).cast(IntegerType()),  # +H:[M]M
        )
        .when(
            _p4c,
            snowpark_fn.substring(tz_col, 5, 2).cast(IntegerType()),  # +HH:[M]M
        )
        .when(
            (_len == snowpark_fn.lit(5)) | (_len == snowpark_fn.lit(7)),
            snowpark_fn.substring(tz_col, 4, 2).cast(IntegerType()),  # +HHMM or +HHMMSS
        )
        .otherwise(snowpark_fn.lit(0))
    )  # +H or +HH (no minutes)
    # Seconds: only present in +H:MM:SS, +HH:MM:SS, and +HHMMSS (length == 7).
    secs = (
        snowpark_fn.when(
            _p3c & _p6c,  # +H:MM:SS
            snowpark_fn.substring(tz_col, 7, 2).cast(IntegerType()),
        )
        .when(
            _p4c & _p7c,  # +HH:MM:SS
            snowpark_fn.substring(tz_col, 8, 2).cast(IntegerType()),
        )
        .when(
            _len == snowpark_fn.lit(7),  # +HHMMSS exactly
            snowpark_fn.substring(tz_col, 6, 2).cast(IntegerType()),
        )
        .otherwise(snowpark_fn.lit(0))
    )
    offset_seconds = sign * (
        hours * snowpark_fn.lit(3600) + mins * snowpark_fn.lit(60) + secs
    )
    if not from_utc:
        offset_seconds = snowpark_fn.lit(0) - offset_seconds
    # Reject out-of-range or invalid-component offsets → fall through to IANA.
    _is_valid = (
        _is_valid_fmt
        & (mins >= snowpark_fn.lit(0))
        & (mins <= snowpark_fn.lit(59))
        & (secs >= snowpark_fn.lit(0))
        & (secs <= snowpark_fn.lit(59))
        & (snowpark_fn.abs(offset_seconds) <= snowpark_fn.lit(18 * 3600))
    )
    result = result.when(
        is_offset & _is_valid, snowpark_fn.dateadd("second", offset_seconds, ts_col)
    )

    # 4. Everything else is an IANA name — convert_timezone with tz as-is.
    return result.otherwise(_conv_dynamic())


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


def _sequence_wrong_input_types_message(snowpark_arg_names: list[str]) -> str:
    return (
        f'[DATATYPE_MISMATCH.SEQUENCE_WRONG_INPUT_TYPES] Cannot resolve "sequence({snowpark_arg_names[0]}, {snowpark_arg_names[1]})" due to data type mismatch: '
        "`sequence` uses the wrong parameter type. The parameter type must conform to:\n"
        "1. The start and stop expressions must resolve to the same type.\n"
        '2. If start and stop expressions resolve to the ("TIMESTAMP" or "TIMESTAMP_NTZ" or "DATE") type, '
        'then the step expression must resolve to the ("INTERVAL" or "INTERVAL YEAR TO MONTH" or "INTERVAL DAY TO SECOND") type.\n'
        '3. Otherwise, if start and stop expressions resolve to the "INTEGRAL" type, '
        "then the step expression must resolve to the same type."
    )


def _build_temporal_sequence(
    start_type: DataType,
    stop_type: DataType,
    step_type: DataType | None,
    snowpark_args: list[Column],
    snowpark_typed_args: list,
    snowpark_arg_names: list[str],
) -> tuple[FieldType, TypedColumn]:
    """Build a sequence of timestamps or dates using ARRAY_GENERATE_RANGE + TRANSFORM.

    Snowflake's SEQUENCE/ARRAY_GENERATE_RANGE only support integers, so temporal
    sequences are emulated by:
    1. Converting the interval step to a numeric unit (microseconds or months).
    2. Computing the total span in the same unit.
    3. Generating an integer offset array with ARRAY_GENERATE_RANGE.
    4. Transforming each offset back to a timestamp/date via DATEADD/ADD_MONTHS.
    """
    start_col = snowpark_args[0]
    stop_col = snowpark_args[1]
    step_col = snowpark_args[2] if len(snowpark_args) > 2 else None

    if isinstance(start_type, DateType) and isinstance(stop_type, TimestampType):
        element_type = stop_type
    else:
        element_type = start_type
    result_type = ArrayType(element_type, contains_null=_inner_nullable(False))
    nullable = _any_arg_nullable(snowpark_typed_args)

    analyzer = Session.get_active_session()._analyzer

    if isinstance(step_type, YearMonthIntervalType):
        result_exp = _build_year_month_temporal_sequence(
            start_col, stop_col, step_col, element_type, analyzer
        )
    else:
        result_exp = _build_day_time_temporal_sequence(
            start_col, stop_col, step_col, element_type, analyzer
        )

    result_exp = TypedColumn(
        result_exp,
        lambda: [FieldType(result_type, nullable=nullable)],
    )
    return FieldType(result_type, nullable=nullable), result_exp


def _check_invalid_sequence_step(
    step_value: Column,
    total_value: Column,
) -> tuple[Column, Column]:
    """Return (invalid_step, sign_step) where invalid_step is true when the step is zero or wrong direction."""
    sign_step = snowpark_fn.call_function("SIGN", step_value)
    sign_total = snowpark_fn.call_function("SIGN", total_value)
    wrong_direction = (
        (sign_step != snowpark_fn.lit(0))
        & (sign_total != snowpark_fn.lit(0))
        & (sign_step != sign_total)
    )
    is_zero = step_value == snowpark_fn.lit(0)
    return wrong_direction | is_zero, sign_step


def _build_day_time_temporal_sequence(
    start_col: Column,
    stop_col: Column,
    step_col: Column | None,
    element_type: DataType,
    analyzer,
) -> Column:
    """Build temporal sequence for DayTimeIntervalType steps (or default 1-day step).

    Decomposes the interval into a day component and a sub-day component so that
    day arithmetic uses DATEADD('day', ...) (calendar-aware, handles DST correctly)
    while sub-day arithmetic uses DATEADD('microsecond', ...) (absolute time).
    """
    epoch_ntz = snowpark_fn.sql_expr("'1970-01-01'::TIMESTAMP_NTZ")

    total_micros = snowpark_fn.datediff("microsecond", start_col, stop_col)

    if step_col is not None:
        step_endpoint = epoch_ntz + step_col
        step_micros = snowpark_fn.datediff("microsecond", epoch_ntz, step_endpoint)
        us_per_day = snowpark_fn.lit(_MICROS_PER_DAY)
        step_days = snowpark_fn.call_function("TRUNC", step_micros / us_per_day)
        sub_day_micros = step_micros - step_days * us_per_day
        invalid_step, sign_step = _check_invalid_sequence_step(
            step_micros, total_micros
        )
    else:
        step_days = snowpark_fn.iff(
            total_micros >= 0, snowpark_fn.lit(1), snowpark_fn.lit(-1)
        )
        sub_day_micros = snowpark_fn.lit(0)
        step_micros = step_days * snowpark_fn.lit(_MICROS_PER_DAY)
        sign_step = snowpark_fn.call_function("SIGN", step_micros)
        invalid_step = None

    raise_error = _raise_error_helper(LongType(), IllegalArgumentException)

    abs_step = snowpark_fn.call_function("ABS", step_micros)
    abs_total = snowpark_fn.call_function("ABS", total_micros)
    safe_step = snowpark_fn.call_function("GREATEST", abs_step, snowpark_fn.lit(1))
    # Over-generate by 2 to handle rounding edge cases; FILTER trims to exact stop bound
    n_max = snowpark_fn.call_function("CEIL", abs_total / safe_step) + snowpark_fn.lit(
        2
    )

    if invalid_step is not None:
        n_max = snowpark_fn.iff(
            invalid_step,
            raise_error(
                snowpark_fn.lit("Illegal sequence boundaries: "),
                snowpark_fn.cast(start_col, StringType()),
                snowpark_fn.lit(" to "),
                snowpark_fn.cast(stop_col, StringType()),
                snowpark_fn.lit(" by "),
                snowpark_fn.cast(step_micros, StringType()),
            ),
            n_max,
        )

    if isinstance(element_type, DateType) and step_col is not None:
        is_sub_day_only = (step_days == snowpark_fn.lit(0)) & (
            sub_day_micros != snowpark_fn.lit(0)
        )
        n_max = snowpark_fn.iff(
            is_sub_day_only,
            raise_error(
                snowpark_fn.lit(
                    "sequence step must be a day interval"
                    " if start and end values are dates"
                ),
            ),
            n_max,
        )

    indices = snowpark_fn.call_function(
        "ARRAY_GENERATE_RANGE",
        snowpark_fn.lit(0),
        n_max,
        snowpark_fn.lit(1),
    )

    day_add = snowpark_fn.dateadd("day", snowpark_fn.col("x") * step_days, start_col)
    full_expr = snowpark_fn.dateadd(
        "microsecond", snowpark_fn.col("x") * sub_day_micros, day_add
    )
    if isinstance(element_type, DateType):
        full_expr = snowpark_fn.cast(full_expr, DateType())
    full_sql = analyzer.analyze(full_expr._expression, defaultdict())

    transform_result = snowpark_fn.function("transform")(
        indices,
        snowpark_fn.sql_expr(f"x -> {full_sql}"),
    )

    stop_for_filter = snowpark_fn.cast(stop_col, element_type)
    stop_sql = analyzer.analyze(stop_for_filter._expression, defaultdict())
    sign_step_sql = analyzer.analyze(sign_step._expression, defaultdict())
    filter_lambda = f"x -> IFF({sign_step_sql} >= 0, x <= {stop_sql}, x >= {stop_sql})"
    filtered = snowpark_fn.call_function(
        "FILTER", transform_result, snowpark_fn.sql_expr(filter_lambda)
    )

    return snowpark_fn.cast(filtered, ArrayType(element_type))


def _build_year_month_temporal_sequence(
    start_col: Column,
    stop_col: Column,
    step_col: Column,
    element_type: DataType,
    analyzer,
) -> Column:
    """Build temporal sequence for YearMonthIntervalType steps."""
    start_col = snowpark_fn.cast(start_col, element_type)
    stop_col = snowpark_fn.cast(stop_col, element_type)

    ref_date = snowpark_fn.sql_expr("'2000-01-01'::DATE")
    step_months = snowpark_fn.datediff("month", ref_date, ref_date + step_col)

    total_months = snowpark_fn.datediff("month", start_col, stop_col)

    raise_error = _raise_error_helper(LongType(), IllegalArgumentException)

    invalid_step, sign_step = _check_invalid_sequence_step(step_months, total_months)

    stop_exclusive = total_months + sign_step
    stop_exclusive = snowpark_fn.iff(
        invalid_step,
        raise_error(
            snowpark_fn.lit("Illegal sequence boundaries: "),
            snowpark_fn.cast(start_col, StringType()),
            snowpark_fn.lit(" to "),
            snowpark_fn.cast(stop_col, StringType()),
            snowpark_fn.lit(" by "),
            snowpark_fn.cast(step_months, StringType()),
            snowpark_fn.lit(" months"),
        ),
        stop_exclusive,
    )
    offsets = snowpark_fn.call_function(
        "ARRAY_GENERATE_RANGE",
        snowpark_fn.lit(0),
        stop_exclusive,
        step_months,
    )

    start_sql = analyzer.analyze(start_col._expression, defaultdict())
    corrected = _spark_add_months_sql(start_sql, "x")
    if isinstance(element_type, DateType):
        add_months_sql = f"({corrected})::DATE"
    else:
        add_months_sql = corrected

    transform_result = snowpark_fn.function("transform")(
        offsets,
        snowpark_fn.sql_expr(f"x -> {add_months_sql}"),
    )

    stop_sql = analyzer.analyze(stop_col._expression, defaultdict())
    sign_step_sql = analyzer.analyze(sign_step._expression, defaultdict())
    filter_lambda = f"x -> IFF({sign_step_sql} >= 0, x <= {stop_sql}, x >= {stop_sql})"
    filtered = snowpark_fn.call_function(
        "FILTER", transform_result, snowpark_fn.sql_expr(filter_lambda)
    )

    return snowpark_fn.cast(filtered, ArrayType(element_type))
