#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re
from datetime import date, datetime

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto
from pyspark.errors.exceptions.base import (
    AnalysisException,
    ArithmeticException,
    DateTimeException,
    IllegalArgumentException,
    NumberFormatException,
    SparkRuntimeException,
)

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark._internal.analyzer.unary_expression import Alias
from snowflake.snowpark.column import Column
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
    StructType,
    TimestampTimeZone,
    TimestampType,
    YearMonthIntervalType,
    _FractionalType,
    _IntegralType,
    _NumericType,
)
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import (
    global_config,
    is_cast_string_to_integral_high_precision_enabled,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.error_utils import raise_error_helper
from snowflake.snowpark_connect.expression.integral_types_support import (
    apply_fractional_to_integral_cast,
    apply_fractional_to_integral_cast_with_ansi_check,
    apply_integral_overflow_with_ansi_check,
    apply_interval_to_integral_overflow,
    get_integral_type_bounds,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.type_mapping import (
    map_single_type_string_to_snowpark_type,
    proto_to_snowpark_type,
    snowpark_to_proto_type,
)
from snowflake.snowpark_connect.typed_column import FieldType, TypedColumn
from snowflake.snowpark_connect.utils.context import (
    get_is_evaluating_sql,
    is_function_argument_being_resolved,
)
from snowflake.snowpark_connect.utils.udf_cache import cached_udf

# Matches "char(N)", "char", "varchar(N)", "varchar" (case-insensitive).
# Used to detect casts that Spark Connect rejects (SNOW-3585747).
_CHAR_VARCHAR_TYPE_RE = re.compile(
    r"^\s*(char|varchar)\s*(\(\d+\))?\s*$", re.IGNORECASE
)


def cast_force_nullable(from_type: DataType, to_type: DataType) -> bool:
    """Mirrors Spark Cast.forceNullable (Cast.scala).

    Returns True when a non-null input value can become null after the cast
    (e.g. string parse failure, NaN/Inf conversion, overflow).
    """
    if isinstance(from_type, NullType):
        return False
    if from_type == to_type:
        return False
    if isinstance(from_type, StringType) and isinstance(to_type, BinaryType):
        return False
    if isinstance(from_type, StringType):
        return True
    if isinstance(to_type, StringType):
        return False
    if isinstance(from_type, (FloatType, DoubleType)) and isinstance(
        to_type, TimestampType
    ):
        return True
    if isinstance(from_type, TimestampType) and isinstance(to_type, DateType):
        return False
    if isinstance(to_type, DateType):
        return True
    if isinstance(from_type, DateType) and isinstance(to_type, TimestampType):
        return False
    if isinstance(from_type, DateType):
        return True
    if isinstance(to_type, DecimalType):
        return not _can_null_safe_cast_to_decimal(from_type, to_type)
    if isinstance(from_type, _FractionalType) and isinstance(to_type, _IntegralType):
        return True
    return False


def _can_null_safe_cast_to_decimal(from_type: DataType, to_type: DecimalType) -> bool:
    """Mirrors Spark Cast.canNullSafeCastToDecimal.

    Returns True when the source type's range always fits within the target
    decimal's precision and scale, so the cast can never produce null.
    """
    if isinstance(from_type, _IntegralType):
        if isinstance(from_type, IntegerType):
            return to_type.precision - to_type.scale >= 10
        if isinstance(from_type, LongType):
            return to_type.precision - to_type.scale >= 19
        if isinstance(from_type, ByteType):
            return to_type.precision - to_type.scale >= 3
        if isinstance(from_type, ShortType):
            return to_type.precision - to_type.scale >= 5
        return False
    if isinstance(from_type, DecimalType):
        return (
            to_type.precision - to_type.scale >= from_type.precision - from_type.scale
            and to_type.scale >= from_type.scale
        )
    if isinstance(from_type, BooleanType):
        return to_type.precision >= 1 and to_type.scale == 0
    return False


def cast_nullable(arg_nullable: bool, from_type: DataType, to_type: DataType) -> bool:
    """Full Cast.nullable computation: child.nullable || forceNullable(from, to)."""
    return arg_nullable or cast_force_nullable(from_type, to_type)


def wider_decimal_type(d1: DecimalType, d2: DecimalType) -> DecimalType:
    """Spark's widerDecimalType for decimal precision promotion."""
    scale = max(d1.scale, d2.scale)
    range_ = max(d1.precision - d1.scale, d2.precision - d2.scale)
    return DecimalType(min(range_ + scale, 38), scale)


SYMBOL_FUNCTIONS = {"<", ">", "<=", ">=", "!=", "+", "-", "*", "/", "%", "div"}

CAST_FUNCTIONS = {
    "boolean": types_proto.DataType(boolean=types_proto.DataType.Boolean()),
    "int": types_proto.DataType(integer=types_proto.DataType.Integer()),
    "smallint": types_proto.DataType(short=types_proto.DataType.Short()),
    "bigint": types_proto.DataType(long=types_proto.DataType.Long()),
    "tinyint": types_proto.DataType(byte=types_proto.DataType.Byte()),
    "float": types_proto.DataType(float=types_proto.DataType.Float()),
    "double": types_proto.DataType(double=types_proto.DataType.Double()),
    "string": types_proto.DataType(string=types_proto.DataType.String()),
    "decimal": types_proto.DataType(
        decimal=types_proto.DataType.Decimal(precision=10, scale=0)
    ),
    "date": types_proto.DataType(date=types_proto.DataType.Date()),
    "timestamp": types_proto.DataType(timestamp=types_proto.DataType.Timestamp()),
    "binary": types_proto.DataType(binary=types_proto.DataType.Binary()),
}


def timestamp_to_spark_string(col: Column) -> Column:
    formatted = snowpark_fn.to_varchar(col, "YYYY-MM-DD HH24:MI:SS.FF6")
    trimmed = snowpark_fn.rtrim(formatted, snowpark_fn.lit("0"))
    return snowpark_fn.rtrim(trimmed, snowpark_fn.lit("."))


def _build_map_to_string_expr(map_col: Column, map_type: MapType) -> Column:
    """Format a map as Spark's {k1 -> v1, k2 -> v2} string using MAP_ENTRIES.

    Uses MAP_ENTRIES to decompose the map into an array of {key, value} structs,
    then TRANSFORM + ARRAY_TO_STRING to build the string representation.
    """
    from collections import defaultdict

    from snowflake.snowpark import Session

    placeholder = snowpark_fn.col("x")
    key_col = placeholder["key"]
    value_col = placeholder["value"]

    key_str = _field_to_string_expr(key_col, map_type.key_type)
    value_str = _field_to_string_expr(value_col, map_type.value_type)

    entry_str = snowpark_fn.concat(key_str, snowpark_fn.lit(" -> "), value_str)

    analyzer = Session.get_active_session()._analyzer
    fn_sql = analyzer.analyze(entry_str._expression, defaultdict())

    entries = snowpark_fn.call_function("MAP_ENTRIES", map_col)
    transformed = snowpark_fn.call_function(
        "transform",
        entries,
        snowpark_fn.sql_expr(f"x -> ({fn_sql})"),
    )
    joined = snowpark_fn.call_function(
        "array_to_string",
        transformed.cast(ArrayType()),
        snowpark_fn.lit(", "),
    )
    result = snowpark_fn.concat(snowpark_fn.lit("{"), joined, snowpark_fn.lit("}"))
    return snowpark_fn.when(
        map_col.is_null(), snowpark_fn.lit(None).cast(StringType())
    ).otherwise(result)


def _build_array_to_string_expr(
    arr_col: Column, element_type: DataType | None = None
) -> Column:
    """Format an array as Spark's [val1, val2, ...] string using only SQL expressions.

    Uses TRANSFORM to convert each element to its string representation,
    casts the result to an unstructured array so that ARRAY_TO_STRING accepts
    it, then wraps in ``[…]``.
    """
    from collections import defaultdict

    from snowflake.snowpark import Session

    placeholder = snowpark_fn.sql_expr("x")

    if element_type is not None:
        if isinstance(element_type, ArrayType):
            element_str = _build_array_to_string_expr(
                placeholder, element_type.element_type
            )
        else:
            element_str = _field_to_string_expr(placeholder, element_type)
    else:
        # Unknown / untyped – best-effort cast
        element_str = snowpark_fn.when(
            placeholder.is_null(), snowpark_fn.lit("null")
        ).otherwise(placeholder.cast(StringType()))

    analyzer = Session.get_active_session()._analyzer
    fn_sql = analyzer.analyze(element_str._expression, defaultdict())

    # TRANSFORM each element to its string representation, then cast to an
    # unstructured ARRAY (dropping the structured ARRAY(VARCHAR) wrapper that
    # Snowflake produces for structured input) so ARRAY_TO_STRING works.
    transformed = snowpark_fn.call_function(
        "transform",
        arr_col,
        snowpark_fn.sql_expr(f"x -> ({fn_sql})"),
    )
    joined = snowpark_fn.call_function(
        "array_to_string",
        transformed.cast(ArrayType()),
        snowpark_fn.lit(", "),
    )
    result = snowpark_fn.concat(snowpark_fn.lit("["), joined, snowpark_fn.lit("]"))
    return snowpark_fn.when(
        arr_col.is_null(), snowpark_fn.lit(None).cast(StringType())
    ).otherwise(result)


def _float_to_spark_string(col: Column) -> Column:
    """Format a float/double value as Spark would: whole numbers get a trailing '.0'."""
    str_val = col.cast(StringType())
    return snowpark_fn.when(col.is_null(), snowpark_fn.lit("null")).otherwise(
        snowpark_fn.iff(
            (col == snowpark_fn.floor(col)),
            snowpark_fn.concat(snowpark_fn.floor(col), snowpark_fn.lit(".0")),
            str_val,
        )
    )


def _field_to_string_expr(field_val: Column, field_type: DataType) -> Column:
    """Convert a single struct field value to its Spark string representation."""
    if isinstance(field_type, StructType) and field_type.structured:
        inner_str = _build_struct_to_string_expr(field_val, field_type)
        return snowpark_fn.when(field_val.is_null(), snowpark_fn.lit("null")).otherwise(
            inner_str
        )
    elif isinstance(field_type, MapType):
        formatted = _build_map_to_string_expr(field_val, field_type)
        return snowpark_fn.when(field_val.is_null(), snowpark_fn.lit("null")).otherwise(
            formatted
        )
    elif isinstance(field_type, ArrayType):
        formatted = _build_array_to_string_expr(field_val, field_type.element_type)
        return snowpark_fn.when(field_val.is_null(), snowpark_fn.lit("null")).otherwise(
            formatted
        )
    elif isinstance(field_type, (FloatType, DoubleType)):
        return _float_to_spark_string(field_val)
    elif isinstance(field_type, TimestampType):
        return snowpark_fn.when(field_val.is_null(), snowpark_fn.lit("null")).otherwise(
            timestamp_to_spark_string(field_val)
        )
    else:
        return snowpark_fn.when(field_val.is_null(), snowpark_fn.lit("null")).otherwise(
            field_val.cast(StringType())
        )


def _build_struct_to_string_expr(struct_col: Column, struct_type: StructType) -> Column:
    """Build a SQL expression that formats a struct as Spark's {val1, val2, ...} string."""
    parts: list[Column] = []
    for i, field in enumerate(struct_type.fields):
        if i > 0:
            parts.append(snowpark_fn.lit(", "))
        field_val = struct_col[field.name]
        field_str = _field_to_string_expr(field_val, field.datatype)
        parts.append(field_str)
    struct_str = snowpark_fn.concat(
        snowpark_fn.lit("{"),
        *parts,
        snowpark_fn.lit("}"),
    )
    return snowpark_fn.when(
        struct_col.is_null(), snowpark_fn.lit(None).cast(StringType())
    ).otherwise(struct_str)


def map_cast(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
    from_type_cast: bool = False,
) -> tuple[list[str], TypedColumn]:
    """
    Map a cast expression to a Snowpark expression.
    """
    from snowflake.snowpark_connect.expression.map_expression import (
        map_single_column_expression,
    )

    spark_sql_ansi_enabled = global_config.spark_sql_ansi_enabled

    match exp.cast.WhichOneof("cast_to_type"):
        case "type":
            to_type = proto_to_snowpark_type(exp.cast.type)
            to_type_str = to_type.simpleString().upper()
        case "type_str":
            to_type = map_single_type_string_to_snowpark_type(exp.cast.type_str)
            to_type_str = exp.cast.type_str.upper()
        case _:
            exception = ValueError("No type to cast to")
            attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
            raise exception

    from_exp = exp.cast.expr
    new_name, typed_column = map_single_column_expression(
        from_exp, column_mapping, typer
    )

    # The Snowpark Column may carry an .alias() — either from a user-level
    # .alias("x").cast("int") chain (protobuf alias wrapping cast) or from an
    # internal function implementation that aliases its result.
    # Strip the alias before casting to avoid CAST(col AS "alias" AS TYPE),
    # then re-apply it to the result.
    # A single unwrap is sufficient even for chained aliases like
    # .alias("a").alias("b").cast("int"): the protobuf nests them as
    # Alias("b", child=Alias("a", child=col)), and map_single_column_expression
    # resolves the full tree so the Snowpark Column ends up with at most one
    # top-level Alias node (the outermost one).
    alias_to_reapply: str | None = None
    if hasattr(typed_column.col, "_expression"):
        col_exp = typed_column.col._expression
        if isinstance(col_exp, Alias):
            alias_to_reapply = col_exp.name
            captured_types = typed_column.types
            typed_column = TypedColumn(Column(col_exp.child), lambda: captured_types)

    match from_exp.WhichOneof("expr_type"):
        case "unresolved_attribute" if not is_function_argument_being_resolved():
            col_name = new_name
        case "literal" if not is_function_argument_being_resolved() and from_type_cast:
            col_name = new_name
        case "unresolved_function" if from_exp.unresolved_function.function_name in SYMBOL_FUNCTIONS:
            col_name = new_name
        case _ if to_type.typeName().upper() in ("STRUCT", "ARRAY", "MAP"):
            col_name = new_name
        case _ if from_type_cast:
            col_name = new_name
        case _ if get_is_evaluating_sql():
            col_name = f"CAST({new_name} AS {to_type_str})"
        case _:
            col_name = new_name

    from_type = typed_column.typ

    # Spark does not allow casting to a UserDefinedType.
    # Detect this from the raw proto before UDT info is lost.
    if (
        exp.cast.WhichOneof("cast_to_type") == "type"
        and exp.cast.type.WhichOneof("kind") == "udt"
    ):
        exception = AnalysisException(
            f'[DATATYPE_MISMATCH.INVALID_CAST] Cannot resolve "{col_name}" '
            f"due to data type mismatch: cannot cast to a UserDefinedType.;"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
        raise exception

    if from_exp.WhichOneof("expr_type") == "literal":
        if (
            spark_sql_ansi_enabled
            and not isinstance(from_type, NullType)
            and (
                isinstance(to_type, _NumericType)
                or isinstance(to_type, BinaryType)
                or isinstance(to_type, BooleanType)
            )
        ):
            sanity_check(to_type, new_name, from_type, from_type_cast)

    col = typed_column.col
    # On TCM, sometimes these are StringType(x)
    # This normalizes them for the cast.
    if isinstance(from_type, StringType):
        from_type = StringType()
    if isinstance(to_type, StringType):
        to_type = StringType()

    # SNOW-3585747: Reject char/varchar casts to match Spark Connect
    # (DATATYPE_MISMATCH.CAST_WITHOUT_SUGGESTION).
    if _CHAR_VARCHAR_TYPE_RE.match(to_type_str):
        raise _cast_without_suggestion_error(
            col_name, from_type, to_type_str, column_mapping
        )

    match (from_type, to_type):
        # Integral Types may require casting even if they are already the same type
        # so that the generate SQL has explicit cast to NUMBER(p, 0) type to ensure proper emulation
        case (_IntegralType(), _IntegralType()):
            # SNOW-3585745: If casting to the same type with the same precision
            # do not emit double cast:
            # CAST(CAST(... AS BIGINT) AS BIGINT) wrapper (commonly produced
            # around sum() aggregations whose result is already cast to BIGINT).
            # Narrower integral targets still get an explicit cast so Snowflake
            # enforces the NUMBER(p, 0) range emulation noted above.
            if from_type == to_type:
                result_exp = col
            else:
                result_exp = apply_integral_overflow_with_ansi_check(
                    col, to_type, spark_sql_ansi_enabled
                )
        case (_, _) if (from_type == to_type):
            result_exp = col
        case (NullType(), _):
            result_exp = col.cast(to_type)
        case (StructType(), StringType()) if from_type.structured:
            result_exp = _build_struct_to_string_expr(col, from_type)
        case (StructType(), _) if from_type.structured:
            result_exp = col.cast(to_type, rename_fields=True)
        case (ArrayType(), StringType()) if from_type.structured:
            result_exp = _build_array_to_string_expr(col, from_type.element_type)
        case (MapType(), StringType()):
            result_exp = _build_map_to_string_expr(col, from_type)

        # date and timestamp
        case (TimestampType(), _) if isinstance(to_type, _NumericType):
            epoch_s = snowpark_fn.date_part("epoch_seconds", col)
            result_exp = epoch_s.cast(to_type)
        case (TimestampType(), BooleanType()):
            timestamp_0L = snowpark_fn.to_timestamp(snowpark_fn.lit(0))
            result_exp = snowpark_fn.when(
                col.is_not_null(),
                col
                != timestamp_0L,  # 0L timestamp is mapped to False, other values are mapped to True
            ).otherwise(snowpark_fn.lit(None))
        case (TimestampType(), StringType()):
            result_exp = timestamp_to_spark_string(col)
        case (TimestampType(), DateType()):
            result_exp = snowpark_fn.to_date(col)
        case (DateType(), TimestampType()):
            result_exp = snowpark_fn.to_timestamp(col)
            if to_type.tzinfo == TimestampTimeZone.NTZ:
                result_exp = result_exp.cast(TimestampType(TimestampTimeZone.NTZ))
        case (TimestampType() as f, TimestampType() as t) if f.tzinfo == t.tzinfo:
            result_exp = col
        case (
            TimestampType(),
            TimestampType() as t,
        ) if t.tzinfo == TimestampTimeZone.NTZ:
            zone = global_config.spark_sql_session_timeZone
            result_exp = snowpark_fn.convert_timezone(snowpark_fn.lit(zone), col).cast(
                TimestampType(TimestampTimeZone.NTZ)
            )
        case (TimestampType(), TimestampType()):
            result_exp = col.cast(to_type)
        case (_, TimestampType()) if isinstance(from_type, _NumericType):
            microseconds = col * snowpark_fn.lit(1000000)
            result_exp = snowpark_fn.when(
                col < 0, snowpark_fn.ceil(microseconds)
            ).otherwise(snowpark_fn.floor(microseconds))
            result_exp = result_exp.cast(LongType())
            result_exp = snowpark_fn.to_timestamp(
                result_exp, snowpark_fn.lit(6)
            )  # microseconds precision
            if to_type.tzinfo == TimestampTimeZone.NTZ:
                result_exp = result_exp.cast(TimestampType(TimestampTimeZone.NTZ))
        case (_, TimestampType()) if isinstance(from_type, BooleanType):
            result_exp = snowpark_fn.to_timestamp(
                col.cast(LongType()), snowpark_fn.lit(6)
            )  # microseconds precision
            if to_type.tzinfo == TimestampTimeZone.NTZ:
                result_exp = result_exp.cast(TimestampType(TimestampTimeZone.NTZ))
        case (_, TimestampType()):
            if spark_sql_ansi_enabled:
                result_exp = snowpark_fn.to_timestamp(col)
            else:
                result_exp = snowpark_fn.function("try_to_timestamp")(col)
            if to_type.tzinfo == TimestampTimeZone.NTZ:
                result_exp = result_exp.cast(TimestampType(TimestampTimeZone.NTZ))
        case (DateType(), _) if isinstance(to_type, (_NumericType, BooleanType)):
            result_exp = snowpark_fn.cast(snowpark_fn.lit(None), to_type)
        case (_, DateType()):
            if spark_sql_ansi_enabled:
                result_exp = snowpark_fn.to_date(col)
            else:
                result_exp = snowpark_fn.function("try_to_date")(col)
        # boolean
        case (BooleanType(), _) if isinstance(to_type, _NumericType):
            result_exp = col.cast(LongType()).cast(to_type)
        case (_, BooleanType()) if isinstance(from_type, _NumericType):
            result_exp = col.cast(LongType()).cast(to_type)

        # binary
        case (StringType(), BinaryType()):
            result_exp = snowpark_fn.to_binary(col, "UTF-8")
        case (_IntegralType(), BinaryType()):
            if spark_sql_ansi_enabled:
                from_type_name = _spark_source_type_name(from_type)
                exception = AnalysisException(
                    f'[DATATYPE_MISMATCH.CAST_WITH_CONF_SUGGESTION] Cannot resolve "CAST({col_name} AS BINARY)" '
                    f'due to data type mismatch: cannot cast "{from_type_name}" to "BINARY" with ANSI mode on. '
                    f'If you have to cast "{from_type_name}" to "BINARY", you can set "spark.sql.ansi.enabled" as \'false\'.'
                )
                attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
                raise exception
            type_name = type(from_type).__name__.lower().replace("type", "")
            match type_name:
                case "byte":
                    digits = 2
                case "short":
                    digits = 4
                case "integer":
                    digits = 8
                case _:
                    # default to long
                    digits = 16

            result_exp = snowpark_fn.when(
                col.isNull(), snowpark_fn.lit(None)
            ).otherwise(
                snowpark_fn.to_binary(
                    snowpark_fn.lpad(
                        snowpark_fn.ltrim(
                            snowpark_fn.to_char(col, snowpark_fn.lit("X" * digits))
                        ),
                        snowpark_fn.lit(digits),
                        snowpark_fn.lit("0"),
                    )
                )
            )
        case (_, BinaryType()):
            result_exp = snowpark_fn.try_to_binary(col)
        case (BinaryType(), StringType()):
            result_exp = snowpark_fn.to_varchar(col, "UTF-8")

        # numeric
        case (_, _) if isinstance(from_type, (FloatType, DoubleType)) and isinstance(
            to_type, _IntegralType
        ):
            if spark_sql_ansi_enabled:
                truncated = (
                    snowpark_fn.when(
                        col == snowpark_fn.lit(float("nan")), snowpark_fn.lit(0)
                    )
                    .when(col < 0, snowpark_fn.ceil(col))
                    .otherwise(snowpark_fn.floor(col))
                )
                result_exp = apply_fractional_to_integral_cast_with_ansi_check(
                    truncated, to_type, True
                )
            else:
                target_min, target_max = get_integral_type_bounds(to_type)
                # col > target_max is equivalent to floor(col) > target_max: for col in
                # (target_max, target_max+1), floor(col) == target_max so both paths
                # produce target_max. Avoids referencing col twice via a shared intermediate.
                result_exp = (
                    snowpark_fn.when(
                        col == snowpark_fn.lit(float("nan")),
                        snowpark_fn.lit(0).cast(to_type),
                    )
                    .when(
                        col < 0,
                        snowpark_fn.when(
                            snowpark_fn.ceil(col) < snowpark_fn.lit(target_min),
                            snowpark_fn.lit(target_min),
                        ).otherwise(snowpark_fn.ceil(col).cast(to_type)),
                    )
                    .when(
                        col > snowpark_fn.lit(target_max),
                        snowpark_fn.lit(target_max),
                    )
                    .otherwise(snowpark_fn.floor(col).cast(to_type))
                )
        case (_, _) if isinstance(from_type, DecimalType) and isinstance(
            to_type, _IntegralType
        ):
            result_exp = snowpark_fn.when(col < 0, snowpark_fn.ceil(col)).otherwise(
                snowpark_fn.floor(col)
            )
            result_exp = result_exp.cast(to_type)
            result_exp = apply_integral_overflow_with_ansi_check(
                result_exp, to_type, spark_sql_ansi_enabled
            )
        case (_, _) if isinstance(from_type, _FractionalType) and isinstance(
            to_type, _IntegralType
        ):
            result_exp = (
                snowpark_fn.when(
                    col == snowpark_fn.lit(float("nan")), snowpark_fn.lit(0)
                )
                .when(col < 0, snowpark_fn.ceil(col))
                .otherwise(snowpark_fn.floor(col))
            )
            result_exp = apply_fractional_to_integral_cast(result_exp, to_type)
        case (StringType(), _) if (isinstance(to_type, _IntegralType)):
            # SNOW-3585745: For LongType targets a DOUBLE intermediate loses
            # precision. DOUBLE has only ~15-16 significant digits, so 19-digit
            # values near Long.MIN/MAX (e.g. 9223372036854775807) round to the
            # nearest power of two. DecimalType(38, 18) preserves full integer precision (20
            # integer digits, enough for the 19-digit Long range) while still
            # carrying a fractional part so floor/ceil truncate like Spark.
            # Smaller integral types fit comfortably in DOUBLE.
            intermediate_type = (
                DecimalType(38, 18)
                if (
                    is_cast_string_to_integral_high_precision_enabled()
                    and isinstance(to_type, LongType)
                )
                else DoubleType()
            )
            if spark_sql_ansi_enabled:
                numeric_val = snowpark_fn.cast(col, intermediate_type)

                target_min, target_max = get_integral_type_bounds(to_type)
                raise_error = raise_error_helper(to_type, NumberFormatException)
                to_type_name = to_type.__class__.__name__.upper().replace("TYPE", "")

                truncated = snowpark_fn.when(
                    numeric_val < 0, snowpark_fn.ceil(numeric_val)
                ).otherwise(snowpark_fn.floor(numeric_val))

                result_exp = snowpark_fn.when(
                    (truncated < snowpark_fn.lit(target_min))
                    | (truncated > snowpark_fn.lit(target_max)),
                    raise_error(
                        snowpark_fn.lit("[CAST_INVALID_INPUT] The value '"),
                        col,
                        snowpark_fn.lit(
                            f'\' of the type "STRING" cannot be cast to "{to_type_name}" because it is malformed. Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
                        ),
                    ),
                ).otherwise(truncated.cast(to_type))
            else:
                numeric_val = snowpark_fn.try_cast(col, intermediate_type)

                truncated = snowpark_fn.when(
                    numeric_val < 0, snowpark_fn.ceil(numeric_val)
                ).otherwise(snowpark_fn.floor(numeric_val))

                target_min, target_max = get_integral_type_bounds(to_type)
                result_exp = (
                    snowpark_fn.when(
                        numeric_val.isNull(), snowpark_fn.lit(None).cast(to_type)
                    )
                    .when(
                        (truncated < snowpark_fn.lit(target_min))
                        | (truncated > snowpark_fn.lit(target_max)),
                        snowpark_fn.lit(None).cast(to_type),
                    )
                    .otherwise(truncated.cast(to_type))
                )
        # https://docs.snowflake.com/en/sql-reference/functions/try_cast Only works on certain types (mostly non-structured ones)
        case (StringType(), _) if isinstance(to_type, _NumericType) or isinstance(
            to_type, StringType
        ) or isinstance(to_type, BooleanType) or isinstance(
            to_type, DateType
        ) or isinstance(
            to_type, TimestampType
        ) or isinstance(
            to_type, BinaryType
        ):
            if spark_sql_ansi_enabled:
                result_exp = snowpark_fn.cast(col, to_type)
            else:
                result_exp = snowpark_fn.try_cast(col, to_type)
        case (StringType(), YearMonthIntervalType()):
            result_exp = _cast_string_to_year_month_interval(col, to_type)
        case (YearMonthIntervalType(), StringType()):
            result_exp = _cast_year_month_interval_to_string(col, from_type)
        case (StringType(), DayTimeIntervalType()):
            result_exp = _cast_string_to_day_time_interval(col, to_type)
        case (DayTimeIntervalType(), StringType()):
            result_exp = _cast_day_time_interval_to_string(col, from_type)
        case (DayTimeIntervalType() | YearMonthIntervalType(), _) if isinstance(
            to_type, _IntegralType
        ):
            result_exp = _cast_interval_to_integral(col, from_type, to_type)
        case (_IntegralType() | DecimalType(), YearMonthIntervalType()):
            result_exp = _cast_numeric_to_year_month_interval(
                col, from_type, to_type, to_type_str
            )
        case (_IntegralType() | DecimalType(), DayTimeIntervalType()):
            result_exp = _cast_numeric_to_day_time_interval(
                col, from_type, to_type, to_type_str
            )
        case (StringType(), _) | (
            (
                # Spark disallows float/double -> interval at analysis time.
                FloatType() | DoubleType(),
                YearMonthIntervalType() | DayTimeIntervalType(),
            )
        ):

            raise _cast_without_suggestion_error(
                col_name, from_type, to_type_str, column_mapping
            )
        case (_, StringType()) if isinstance(from_type, (FloatType, DoubleType)):
            # Spark renders whole-number floats/doubles with a trailing ".0"
            # (e.g. 980.0 → "980.0", -250.0 → "-250.0"). Snowflake's default
            # TO_VARCHAR drops the decimal for integral values (980.0 → "980"),
            # which produces wrong MD5/hash values when the string is used as a
            # hash input. IFF(null, ...) returns the else branch, so null is
            # correctly forwarded as NULL (not the string "null").
            str_val = col.cast(StringType())
            result_exp = snowpark_fn.iff(
                col == snowpark_fn.floor(col),
                snowpark_fn.concat(snowpark_fn.floor(col), snowpark_fn.lit(".0")),
                str_val,
            )
        case _:
            result_exp = snowpark_fn.cast(col, to_type)

    if alias_to_reapply is not None:
        result_exp = result_exp.alias(alias_to_reapply)

    nullable = cast_nullable(typed_column.nullable, from_type, to_type)
    return [col_name], TypedColumn(result_exp, lambda: [FieldType(to_type, nullable)])


def sanity_check(
    to_type: DataType, value: str, from_type: DataType, from_type_cast: bool
) -> None:
    """
    This is a basic validation to ensure the casting is legal.
    """

    if isinstance(from_type, LongType) and isinstance(to_type, BinaryType):
        exception = NumberFormatException(
            f"""[DATATYPE_MISMATCH.CAST_WITH_CONF_SUGGESTION] Cannot resolve "CAST({value} AS BINARY)" due to data type mismatch: cannot cast "BIGINT" to "BINARY" with ANSI mode on."""
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
        raise exception

    if (
        from_type_cast
        and isinstance(from_type, StringType)
        and isinstance(to_type, BooleanType)
    ):
        if value is not None:
            value = value.strip().lower()
        if value not in {"t", "true", "f", "false", "y", "yes", "n", "no", "0", "1"}:
            exception = SparkRuntimeException(
                f"""[CAST_INVALID_INPUT] The value '{value}' of the type "STRING" cannot be cast to "BOOLEAN" because it is malformed. Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error."""
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
            raise exception

    # SNOW-2677699: match Spark's Cast.scala — String → Date/Timestamp under
    # ANSI raises DateTimeException so partition-literal validation gets the
    # same guard.
    if (
        from_type_cast
        and isinstance(from_type, StringType)
        and isinstance(to_type, (DateType, TimestampType))
        and value is not None
    ):
        parser = (
            date.fromisoformat
            if isinstance(to_type, DateType)
            else datetime.fromisoformat
        )
        try:
            parser(value.strip())
        except (ValueError, TypeError) as e:
            exception = DateTimeException(
                f"[CAST_INVALID_INPUT] The value '{value}' of the type \"STRING\" "
                f'cannot be cast to "{to_type.simple_string().upper()}" because it is malformed.'
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
            raise exception from e
        return

    raise_cast_failure_exception = False
    if isinstance(to_type, _IntegralType):
        try:
            x = int(value)
            if isinstance(to_type, IntegerType) and (x > 2147483647 or x < -2147483648):
                raise_cast_failure_exception = True
            elif isinstance(to_type, LongType) and (
                x > 9223372036854775807 or x < -9223372036854775808
            ):
                raise_cast_failure_exception = True
        except Exception:
            raise_cast_failure_exception = True
    elif isinstance(to_type, _FractionalType):
        try:
            float(value)
        except Exception:
            raise_cast_failure_exception = True
    if raise_cast_failure_exception:
        if not isinstance(from_type, StringType) and isinstance(to_type, _IntegralType):
            from_type_name = from_type.__class__.__name__.upper().replace("TYPE", "")
            to_type_name = to_type.__class__.__name__.upper().replace("TYPE", "")
            value_suffix = "L" if isinstance(from_type, LongType) else ""
            exception = ArithmeticException(
                f"""[CAST_OVERFLOW] The value {value}{value_suffix} of the type "{from_type_name}" cannot be cast to "{to_type_name}" due to an overflow. Use `try_cast` to tolerate overflow and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error."""
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
        else:
            exception = NumberFormatException(
                """[CAST_INVALID_INPUT] Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary setting "spark.sql.ansi.enabled" to "false" may bypass this error."""
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
        raise exception


def _cast_string_to_year_month_interval(
    col: Column, to_type: YearMonthIntervalType
) -> Column:
    """Cast string to YearMonthIntervalType. Handles 'y-m', 'y', 'm', and 'INTERVAL ...' formats."""
    # Extract values from different formats
    value = snowpark_fn.regexp_extract(col, "'([^']+)'", 1)
    years = snowpark_fn.regexp_extract(col, "^[+-]?\\d+", 0)
    months = snowpark_fn.regexp_extract(col, "-(\\d+)$", 1)
    raise_error = raise_error_helper(to_type, IllegalArgumentException)

    # For MONTH-only intervals, treat the input as months
    if (
        to_type.start_field == YearMonthIntervalType.MONTH
        and to_type.end_field == YearMonthIntervalType.MONTH
    ):
        months = years
        years = snowpark_fn.lit(0)

    # Define overflow limits based on Snowflake's INTERVAL limits
    # Maximum year-month interval is 178956970-7 (positive) and -178956970-8 (negative)
    max_years = snowpark_fn.lit(178956970)
    max_months_positive = snowpark_fn.lit(7)
    max_months_negative = snowpark_fn.lit(8)

    return snowpark_fn.when(
        col.like("INTERVAL % YEAR TO MONTH")
        | col.like("INTERVAL % YEAR")
        | col.like("INTERVAL % MONTH"),
        value.cast(to_type),
    ).when(
        col.rlike("^[+-]?\\d+(-\\d+)?$"),
        snowpark_fn.when(
            # Check for overflow conditions
            ((years >= max_years) & (months > max_months_positive))
            | (years > max_years)
            | ((years <= -max_years) & (months > max_months_negative))
            | (years < -max_years),
            raise_error(snowpark_fn.lit("Error parsing interval year-month string")),
        ).otherwise(col.cast(to_type)),
    )


def _cast_year_month_interval_to_string(
    col: Column, from_type: YearMonthIntervalType
) -> Column:
    """Cast YearMonthIntervalType to string. Returns 'INTERVAL '...' YEAR TO MONTH' format."""
    years = snowpark_fn.date_part("YEAR", col)
    months = snowpark_fn.date_part("MONTH", col)

    total_months = years * 12 + months

    start_field = from_type.start_field  # YEAR
    end_field = from_type.end_field  # MONTH

    def _format_interval_udf(
        total_months: int, start_field: int, end_field: int
    ) -> str:
        is_negative = total_months < 0
        abs_months = abs(total_months)
        years = abs_months // 12
        months = abs_months % 12

        is_year_only = start_field == 0 and end_field == 0
        is_month_only = start_field == 1 and end_field == 1

        if is_year_only:
            sign = "-" if is_negative else ""
            return f"INTERVAL '{sign}{years}' YEAR"
        elif is_month_only:
            return f"INTERVAL '{total_months}' MONTH"
        else:  # YEAR TO MONTH
            if is_negative:
                return f"INTERVAL '-{years}-{months}' YEAR TO MONTH"
            else:
                return f"INTERVAL '{years}-{months}' YEAR TO MONTH"

    format_udf = cached_udf(
        _format_interval_udf,
        input_types=[IntegerType(), IntegerType(), IntegerType()],
        return_type=StringType(),
    )

    return format_udf(
        total_months, snowpark_fn.lit(start_field), snowpark_fn.lit(end_field)
    )


def _cast_string_to_day_time_interval(
    col: Column, to_type: DayTimeIntervalType
) -> Column:
    """Cast string to DayTimeIntervalType. Handles 'd h:m:s' and 'INTERVAL ...' formats."""

    def extract_and_cast(c: Column) -> Column:
        """Extract quoted value from INTERVAL string and cast to target type."""
        return snowpark_fn.function("REGEXP_SUBSTR")(c, "'([^']+)'", 1, 1, "e", 1).cast(
            to_type
        )

    return (
        snowpark_fn.when(col.like("INTERVAL % DAY TO SECOND"), extract_and_cast(col))
        .when(col.like("INTERVAL % DAY TO HOUR"), extract_and_cast(col))
        .when(col.like("INTERVAL % DAY TO MINUTE"), extract_and_cast(col))
        .when(col.like("INTERVAL % DAY"), extract_and_cast(col))
        .when(col.like("INTERVAL % HOUR TO MINUTE"), extract_and_cast(col))
        .when(col.like("INTERVAL % HOUR TO SECOND"), extract_and_cast(col))
        .when(col.like("INTERVAL % HOUR"), extract_and_cast(col))
        .when(col.like("INTERVAL % MINUTE TO SECOND"), extract_and_cast(col))
        .when(col.like("INTERVAL % MINUTE"), extract_and_cast(col))
        .when(col.like("INTERVAL % SECOND"), extract_and_cast(col))
        .when(col.like("% %:%:%"), col.cast(to_type))
        .when(col.like("%:%:%"), col.cast(to_type))
        .when(col.like("%:%"), col.cast(to_type))
        .when(col.like("+%") | col.like("-%"), col.cast(to_type))
        .otherwise(col.cast(to_type))
    )


def _cast_day_time_interval_to_string(
    col: Column, from_type: DayTimeIntervalType
) -> Column:
    """Cast DayTimeIntervalType to string. Returns 'INTERVAL '...' DAY TO SECOND' format."""

    # NOTE: This UDF logic is duplicated from utils/interval_format.py because UDFs must be
    # self-contained (they run on Snowflake and can't import from our codebase at runtime).
    # If you update this logic, also update interval_format.format_day_time_interval().
    def _format_day_time_interval_udf(
        total_microseconds: int, start_field: int, end_field: int
    ) -> str:
        if total_microseconds is None:
            return None

        _TWO_DIGIT_FORMAT = "{:02d}"
        _THREE_DIGIT_FORMAT = "{:03d}"
        _SECONDS_PRECISION_FORMAT = "{:09.6f}"

        def _format_time_component(value: int, is_negative: bool = False) -> str:
            return (
                _THREE_DIGIT_FORMAT.format(value)
                if is_negative
                else _TWO_DIGIT_FORMAT.format(value)
            )

        def _format_seconds_precise(seconds: float) -> str:
            return _SECONDS_PRECISION_FORMAT.format(seconds).rstrip("0").rstrip(".")

        total_seconds = total_microseconds / 1_000_000
        is_negative = total_seconds < 0
        abs_total_microseconds = abs(total_microseconds)

        days = int(abs_total_microseconds // (86400 * 1_000_000))
        remaining_microseconds = abs_total_microseconds % (86400 * 1_000_000)
        hours = int(remaining_microseconds // (3600 * 1_000_000))
        remaining_microseconds = remaining_microseconds % (3600 * 1_000_000)
        minutes = int(remaining_microseconds // (60 * 1_000_000))
        remaining_microseconds = remaining_microseconds % (60 * 1_000_000)
        seconds = remaining_microseconds / 1_000_000

        if is_negative:
            days = -days
        days_str = "-0" if (is_negative and days == 0) else str(days)

        # DAY only
        if start_field == 0 and end_field == 0:
            return f"INTERVAL '{days}' DAY"
        # HOUR only
        if start_field == 1 and end_field == 1:
            total_hours = int(abs(total_microseconds) // (3600 * 1_000_000))
            if total_microseconds < 0:
                total_hours = -total_hours
            fmt = _THREE_DIGIT_FORMAT if total_hours < 0 else _TWO_DIGIT_FORMAT
            return f"INTERVAL '{fmt.format(total_hours)}' HOUR"
        # MINUTE only
        if start_field == 2 and end_field == 2:
            total_minutes = int(abs(total_microseconds) // (60 * 1_000_000))
            if total_microseconds < 0:
                total_minutes = -total_minutes
            fmt = _THREE_DIGIT_FORMAT if total_minutes < 0 else _TWO_DIGIT_FORMAT
            return f"INTERVAL '{fmt.format(total_minutes)}' MINUTE"
        # SECOND only
        if start_field == 3 and end_field == 3:
            total_seconds_precise = total_microseconds / 1_000_000
            if total_seconds_precise == int(total_seconds_precise):
                fmt = (
                    _THREE_DIGIT_FORMAT
                    if total_seconds_precise < 0
                    else _TWO_DIGIT_FORMAT
                )
                return f"INTERVAL '{fmt.format(int(total_seconds_precise))}' SECOND"
            return f"INTERVAL '{_format_seconds_precise(total_seconds_precise)}' SECOND"
        # MINUTE TO SECOND
        if start_field == 2 and end_field == 3:
            total_minutes = int(abs_total_microseconds // (60 * 1_000_000))
            remaining_us = abs_total_microseconds % (60 * 1_000_000)
            remaining_secs = remaining_us / 1_000_000
            if remaining_secs == int(remaining_secs):
                seconds_str = _TWO_DIGIT_FORMAT.format(int(remaining_secs))
            else:
                seconds_str = _format_seconds_precise(remaining_secs)
            sign = "-" if is_negative else ""
            return f"INTERVAL '{sign}{_TWO_DIGIT_FORMAT.format(total_minutes)}:{seconds_str}' MINUTE TO SECOND"
        # HOUR TO MINUTE
        if start_field == 1 and end_field == 2:
            sign = "-" if is_negative else ""
            return f"INTERVAL '{sign}{_TWO_DIGIT_FORMAT.format(hours)}:{_TWO_DIGIT_FORMAT.format(minutes)}' HOUR TO MINUTE"
        # HOUR TO SECOND
        if start_field == 1 and end_field == 3:
            if seconds == int(seconds):
                seconds_str = _TWO_DIGIT_FORMAT.format(int(seconds))
            else:
                seconds_str = _format_seconds_precise(seconds)
            sign = "-" if is_negative else ""
            return f"INTERVAL '{sign}{_TWO_DIGIT_FORMAT.format(hours)}:{_TWO_DIGIT_FORMAT.format(minutes)}:{seconds_str}' HOUR TO SECOND"
        # DAY TO HOUR
        if start_field == 0 and end_field == 1:
            sign = "-" if is_negative else ""
            d = abs(days) if is_negative else days
            return f"INTERVAL '{sign}{d} {_TWO_DIGIT_FORMAT.format(hours)}' DAY TO HOUR"
        # DAY TO MINUTE
        if start_field == 0 and end_field == 2:
            sign = "-" if is_negative else ""
            d = abs(days) if is_negative else days
            return f"INTERVAL '{sign}{d} {_TWO_DIGIT_FORMAT.format(hours)}:{_TWO_DIGIT_FORMAT.format(minutes)}' DAY TO MINUTE"
        # DAY TO SECOND
        if start_field == 0 and end_field == 3:
            if seconds == int(seconds):
                seconds_str = _TWO_DIGIT_FORMAT.format(int(seconds))
            else:
                seconds_str = _format_seconds_precise(seconds)
            if is_negative:
                return f"INTERVAL '-{abs(days)} {_TWO_DIGIT_FORMAT.format(hours)}:{_TWO_DIGIT_FORMAT.format(minutes)}:{seconds_str}' DAY TO SECOND"
            return f"INTERVAL '{days_str} {_TWO_DIGIT_FORMAT.format(hours)}:{_TWO_DIGIT_FORMAT.format(minutes)}:{seconds_str}' DAY TO SECOND"

        # Fallback - smart formatting
        if days >= 0:
            if hours == 0 and minutes == 0 and seconds == 0:
                return f"INTERVAL '{int(days)}' DAY"
            if seconds == int(seconds):
                return f"INTERVAL '{days_str} {_format_time_component(hours)}:{_format_time_component(minutes)}:{_format_time_component(int(seconds))}' DAY TO SECOND"
            return f"INTERVAL '{days_str} {_format_time_component(hours)}:{_format_time_component(minutes)}:{_format_seconds_precise(seconds)}' DAY TO SECOND"
        elif hours > 0:
            if minutes == 0 and seconds == 0:
                return f"INTERVAL '{_format_time_component(hours)}' HOUR"
            if seconds == int(seconds):
                return f"INTERVAL '{_format_time_component(hours)}:{_format_time_component(minutes)}:{_format_time_component(int(seconds))}' HOUR TO SECOND"
            return f"INTERVAL '{_format_time_component(hours)}:{_format_time_component(minutes)}:{_format_seconds_precise(seconds)}' HOUR TO SECOND"
        elif minutes > 0:
            if seconds == 0:
                return f"INTERVAL '{_format_time_component(minutes)}' MINUTE"
            if seconds == int(seconds):
                return f"INTERVAL '{_format_time_component(minutes)}:{_format_time_component(int(seconds))}' MINUTE TO SECOND"
            return f"INTERVAL '{_format_time_component(minutes)}:{_format_seconds_precise(seconds)}' MINUTE TO SECOND"
        else:
            if seconds == int(seconds):
                return f"INTERVAL '{_format_time_component(int(seconds))}' SECOND"
            return f"INTERVAL '{_format_seconds_precise(seconds)}' SECOND"

    # Extract interval components and convert to total microseconds
    days = snowpark_fn.date_part("DAY", col)
    hours = snowpark_fn.date_part("HOUR", col)
    minutes = snowpark_fn.date_part("MINUTE", col)
    seconds = snowpark_fn.date_part("SECOND", col)
    nanoseconds = snowpark_fn.date_part("NANOSECOND", col)

    total_microseconds = (
        days * 86400 + hours * 3600 + minutes * 60 + seconds
    ) * 1_000_000 + (nanoseconds / 1000)

    start_field = from_type.start_field
    end_field = from_type.end_field

    format_udf = cached_udf(
        _format_day_time_interval_udf,
        input_types=[LongType(), IntegerType(), IntegerType()],
        return_type=StringType(),
    )

    return format_udf(
        total_microseconds, snowpark_fn.lit(start_field), snowpark_fn.lit(end_field)
    )


# Spark source-type names used in CAST_OVERFLOW messages.
_SPARK_NUMERIC_TYPE_NAMES = {
    ByteType: "TINYINT",
    ShortType: "SMALLINT",
    IntegerType: "INT",
    LongType: "BIGINT",
}

# Year-month interval internal value is a 32-bit month count (Spark stores it as
# an int). Snowflake's INTERVAL_YEAR_MONTH range coincides with this bound.
_YEAR_MONTH_MONTHS_MIN = -2147483648
_YEAR_MONTH_MONTHS_MAX = 2147483647

# Day-time interval internal value is a 64-bit microsecond count.
_DAY_TIME_MICROS_MIN = -9223372036854775808
_DAY_TIME_MICROS_MAX = 9223372036854775807

# Microseconds per unit, keyed by DayTimeIntervalType end field code.
_DAY_TIME_MICROS_PER_UNIT = {
    DayTimeIntervalType.DAY: 86_400_000_000,
    DayTimeIntervalType.HOUR: 3_600_000_000,
    DayTimeIntervalType.MINUTE: 60_000_000,
    DayTimeIntervalType.SECOND: 1_000_000,
}


def _spark_source_type_name(from_type: DataType) -> str:
    if isinstance(from_type, DecimalType):
        return f"DECIMAL({from_type.precision},{from_type.scale})"
    return _SPARK_NUMERIC_TYPE_NAMES.get(type(from_type), "BIGINT")


def _cast_without_suggestion_error(
    col_name: str,
    from_type: DataType,
    to_type_str: str,
    column_mapping: ColumnNameMap,
) -> AnalysisException:
    """Build Spark's DATATYPE_MISMATCH.CAST_WITHOUT_SUGGESTION analysis error."""
    from_type_str = next(
        iter(snowpark_to_proto_type(from_type, column_mapping))
    ).upper()
    exception = AnalysisException(
        f'[DATATYPE_MISMATCH.CAST_WITHOUT_SUGGESTION] Cannot resolve "{col_name}" '
        f"due to data type mismatch: cannot cast "
        f'"{from_type_str}" to "{to_type_str}".;'
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
    return exception


def _cast_overflow_error(
    col: Column, from_type: DataType, to_type: DataType, to_type_str: str
) -> Column:
    """Runtime CAST_OVERFLOW error matching Spark's numeric -> interval overflow."""
    from_type_name = _spark_source_type_name(from_type)
    suffix = "L" if isinstance(from_type, LongType) else ""
    raise_error = raise_error_helper(to_type, ArithmeticException)
    return raise_error(
        snowpark_fn.lit("[CAST_OVERFLOW] The value "),
        col.cast(StringType()),
        snowpark_fn.lit(
            f'{suffix} of the type "{from_type_name}" cannot be cast to '
            f'"{to_type_str}" due to an overflow. Use `try_cast` to tolerate '
            f"overflow and return NULL instead. If necessary set "
            f'"spark.sql.ansi.enabled" to "false" to bypass this error.'
        ),
    )


def integral_sql_type_name(typ: DataType) -> str:
    return _SPARK_NUMERIC_TYPE_NAMES.get(type(typ), typ.typeName().upper())


def _cast_interval_to_integral(
    col: Column,
    from_type: DataType,
    to_type: DataType,
) -> Column:
    """Cast an ANSI interval to an integral type with Spark's overflow semantics.

    Snowflake's native interval -> number cast already yields the value in the
    unit of the interval's end field, truncated toward zero (e.g. HOUR TO SECOND
    -> total seconds, YEAR -> years), matching Spark. We widen to BIGINT first --
    a narrow target would either silently overflow into Snowflake's wider NUMBER
    or raise Snowflake's "interval out of representable range" error -- then defer
    to the interval overflow guard, which raises CAST_OVERFLOW on out-of-range
    values in both ANSI-enabled and ANSI-disabled modes (matching Spark, where
    interval narrowing always throws). We pass the interval's SQL type name and a
    column rendering the value (e.g. ``INTERVAL '23:59:59' HOUR TO SECOND``) so
    the message matches Spark.
    """
    value_repr = (
        _cast_year_month_interval_to_string(col, from_type)
        if isinstance(from_type, YearMonthIntervalType)
        else _cast_day_time_interval_to_string(col, from_type)
    )
    return apply_interval_to_integral_overflow(
        col.cast(LongType()),
        to_type,
        source_type_name=from_type.simpleString().upper(),
        target_type_name=integral_sql_type_name(to_type),
        value_repr=value_repr,
    )


def _cast_numeric_to_year_month_interval(
    col: Column,
    from_type: DataType,
    to_type: YearMonthIntervalType,
    to_type_str: str,
) -> Column:
    """Cast an integral/decimal value to a YearMonthIntervalType.

    Mirrors Spark: the number maps to the unit of the target's end field
    (YEAR -> value * 12 months, MONTH -> value months) and decimals are rounded
    HALF_UP. We compute the total month count, build a native ``INTERVAL MONTH``
    (the finest year-month unit, which Snowflake accepts from a number), then let
    Snowflake's interval -> interval cast narrow it to the requested field range.
    That narrowing truncates toward zero, matching Spark's display semantics
    (e.g. 18 months -> ``INTERVAL '1' YEAR``).
    """
    factor = 12 if to_type.end_field == YearMonthIntervalType.YEAR else 1

    total_months = col * snowpark_fn.lit(factor)
    if isinstance(from_type, DecimalType):
        total_months = snowpark_fn.round(total_months, 0)
    total_months = total_months.cast(LongType())

    overflow = (total_months < snowpark_fn.lit(_YEAR_MONTH_MONTHS_MIN)) | (
        total_months > snowpark_fn.lit(_YEAR_MONTH_MONTHS_MAX)
    )

    months_interval = total_months.cast(
        YearMonthIntervalType(YearMonthIntervalType.MONTH, YearMonthIntervalType.MONTH)
    )
    interval_col = months_interval.cast(to_type)

    return snowpark_fn.when(
        overflow, _cast_overflow_error(col, from_type, to_type, to_type_str)
    ).otherwise(interval_col)


def _cast_numeric_to_day_time_interval(
    col: Column,
    from_type: DataType,
    to_type: DayTimeIntervalType,
    to_type_str: str,
) -> Column:
    """Cast an integral/decimal value to a DayTimeIntervalType.

    Mirrors Spark: the number maps to the unit of the target's end field
    (DAY/HOUR/MINUTE/SECOND -> value * micros-per-unit) and decimals are rounded
    HALF_UP at the microsecond level. The full-precision microsecond value is the
    interval's value; Spark keeps every microsecond regardless of the target's
    field range (the range only governs the *display*, e.g. 1h 20m 39.25926s
    shows as ``INTERVAL '01:20' HOUR TO MINUTE`` but still collects as
    timedelta(seconds=4839, microseconds=259260)). We therefore build a native
    ``INTERVAL SECOND`` (the finest day-time unit, which keeps fractional micros)
    and report it as ``to_type`` without a narrowing cast -- narrowing would
    truncate the stored value and drop the sub-field microseconds.
    """
    micros_per_unit = _DAY_TIME_MICROS_PER_UNIT[to_type.end_field]

    total_micros = col * snowpark_fn.lit(micros_per_unit)
    if isinstance(from_type, DecimalType):
        total_micros = snowpark_fn.round(total_micros, 0)

    overflow = (total_micros < snowpark_fn.lit(_DAY_TIME_MICROS_MIN)) | (
        total_micros > snowpark_fn.lit(_DAY_TIME_MICROS_MAX)
    )

    total_seconds = total_micros / snowpark_fn.lit(1_000_000)
    interval_col = total_seconds.cast(
        DayTimeIntervalType(DayTimeIntervalType.SECOND, DayTimeIntervalType.SECOND)
    )

    return snowpark_fn.when(
        overflow, _cast_overflow_error(col, from_type, to_type, to_type_str)
    ).otherwise(interval_col)
