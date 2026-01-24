#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto
from pyspark.errors.exceptions.base import (
    AnalysisException,
    ArithmeticException,
    IllegalArgumentException,
    NumberFormatException,
    SparkRuntimeException,
)

import snowflake.snowpark.functions as snowpark_fn
from snowflake.snowpark.column import Column
from snowflake.snowpark.types import (
    BinaryType,
    BooleanType,
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
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.error_utils import raise_error_helper
from snowflake.snowpark_connect.expression.integral_types_support import (
    apply_fractional_to_integral_cast,
    apply_fractional_to_integral_cast_with_ansi_check,
    apply_integral_overflow_with_ansi_check,
    get_integral_type_bounds,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.type_mapping import (
    map_type_string_to_snowpark_type,
    proto_to_snowpark_type,
    snowpark_to_proto_type,
)
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.context import (
    get_is_evaluating_sql,
    is_function_argument_being_resolved,
)
from snowflake.snowpark_connect.utils.udf_cache import cached_udf

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
            to_type = map_type_string_to_snowpark_type(exp.cast.type_str)
            to_type_str = exp.cast.type_str.upper()
        case _:
            exception = ValueError("No type to cast to")
            attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
            raise exception

    from_exp = exp.cast.expr
    new_name, typed_column = map_single_column_expression(
        from_exp, column_mapping, typer
    )

    match from_exp.WhichOneof("expr_type"):
        case "unresolved_attribute" if not is_function_argument_being_resolved():
            col_name = new_name
        case "literal" if not is_function_argument_being_resolved() and from_type_cast:
            col_name = new_name
        case "unresolved_function" if from_exp.unresolved_function.function_name in SYMBOL_FUNCTIONS:
            col_name = new_name
        case _ if to_type.typeName().upper() in ("STRUCT", "ARRAY"):
            col_name = new_name
        case _ if get_is_evaluating_sql():
            col_name = f"CAST({new_name} AS {to_type_str})"
        case _:
            col_name = new_name

    from_type = typed_column.typ

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

    match (from_type, to_type):
        case (_, _) if (from_type == to_type):
            result_exp = col
        case (NullType(), _):
            result_exp = col.cast(to_type)
        case (StructType(), _) if from_type.structured:
            result_exp = col.cast(to_type, rename_fields=True)
        case (MapType(), StringType()):

            def _map_to_string(map: dict) -> str:
                def format_value(v):
                    if isinstance(v, dict):
                        return _map_to_string(v)
                    elif isinstance(v, list):
                        return "[" + ", ".join(format_value(item) for item in v) + "]"
                    elif isinstance(v, bool):
                        return str(v).lower()  # Spark prints true/false
                    elif v is None:
                        return "null"
                    else:
                        return str(v)

                if map is None:
                    return None
                parts = [f"{k} -> {format_value(v)}" for k, v in map.items()]
                return "{" + ", ".join(parts) + "}"

            _map_entries = cached_udf(
                _map_to_string,
                input_types=[StructType()],
                return_type=StringType(),
            )

            result_exp = snowpark_fn.cast(
                _map_entries(col.cast(StructType())),
                StringType(),
            )

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
        case (TimestampType(), DateType()):
            result_exp = snowpark_fn.to_date(col)
        case (DateType(), TimestampType()):
            result_exp = snowpark_fn.to_timestamp(col)
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
            result_exp = result_exp.cast(TimestampType(TimestampTimeZone.NTZ))
        case (_, TimestampType()) if isinstance(from_type, BooleanType):
            result_exp = snowpark_fn.to_timestamp(
                col.cast(LongType()), snowpark_fn.lit(6)
            )  # microseconds precision
            result_exp = result_exp.cast(TimestampType(TimestampTimeZone.NTZ))
        case (_, TimestampType()):
            if spark_sql_ansi_enabled:
                result_exp = snowpark_fn.to_timestamp(col)
            else:
                result_exp = snowpark_fn.function("try_to_timestamp")(col)
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

        case (_IntegralType(), _IntegralType()):
            result_exp = apply_integral_overflow_with_ansi_check(
                col, to_type, spark_sql_ansi_enabled
            )

        # binary
        case (StringType(), BinaryType()):
            result_exp = snowpark_fn.to_binary(col, "UTF-8")
        case (_IntegralType(), BinaryType()):
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
            truncated = (
                snowpark_fn.when(
                    col == snowpark_fn.lit(float("nan")), snowpark_fn.lit(0)
                )
                .when(col < 0, snowpark_fn.ceil(col))
                .otherwise(snowpark_fn.floor(col))
            )

            if spark_sql_ansi_enabled:
                result_exp = apply_fractional_to_integral_cast_with_ansi_check(
                    truncated, to_type, True
                )
            else:
                target_min, target_max = get_integral_type_bounds(to_type)
                result_exp = (
                    snowpark_fn.when(
                        truncated > snowpark_fn.lit(target_max),
                        snowpark_fn.lit(target_max),
                    )
                    .when(
                        truncated < snowpark_fn.lit(target_min),
                        snowpark_fn.lit(target_min),
                    )
                    .otherwise(truncated.cast(to_type))
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
            if spark_sql_ansi_enabled:
                double_val = snowpark_fn.cast(col, DoubleType())

                target_min, target_max = get_integral_type_bounds(to_type)
                raise_error = raise_error_helper(to_type, NumberFormatException)
                to_type_name = to_type.__class__.__name__.upper().replace("TYPE", "")

                truncated = snowpark_fn.when(
                    double_val < 0, snowpark_fn.ceil(double_val)
                ).otherwise(snowpark_fn.floor(double_val))

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
                double_val = snowpark_fn.try_cast(col, DoubleType())

                truncated = snowpark_fn.when(
                    double_val < 0, snowpark_fn.ceil(double_val)
                ).otherwise(snowpark_fn.floor(double_val))

                target_min, target_max = get_integral_type_bounds(to_type)
                result_exp = (
                    snowpark_fn.when(
                        double_val.isNull(), snowpark_fn.lit(None).cast(to_type)
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
        case (StringType(), _):
            exception = AnalysisException(
                f"""[DATATYPE_MISMATCH.CAST_WITHOUT_SUGGESTION] Cannot resolve "{col_name}" due to data type mismatch: cannot cast "{snowpark_to_proto_type(from_type, column_mapping)}" to "{exp.cast.type_str.upper()}".;"""
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
            raise exception
        case _:
            result_exp = snowpark_fn.cast(col, to_type)

    return [col_name], TypedColumn(result_exp, lambda: [to_type])


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
