#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
from collections import defaultdict

import snowflake.snowpark.functions as snowpark_fn
import snowflake.snowpark.types as snowpark_type
from snowflake import snowpark
from snowflake.snowpark import Session


def _needs_recursive_cast(typ: snowpark_type.DataType) -> bool:
    """Check if a data type needs recursive handling for variant conversion.

    This covers array null-preservation and temporal-to-epoch conversion.
    """
    if isinstance(
        typ,
        (
            snowpark_type.ArrayType,
            snowpark_type.DateType,
            snowpark_type.TimestampType,
            snowpark_type.YearMonthIntervalType,
            snowpark_type.DayTimeIntervalType,
        ),
    ):
        return True
    if isinstance(typ, snowpark_type.StructType):
        return any(_needs_recursive_cast(field.datatype) for field in typ.fields)
    if isinstance(typ, snowpark_type.MapType):
        return _needs_recursive_cast(typ.key_type) or _needs_recursive_cast(
            typ.value_type
        )
    return False


def _ym_interval_to_total_months(col: snowpark.Column) -> snowpark.Column:
    return snowpark_fn.call_function(
        "date_part", snowpark_fn.sql_expr("year"), col
    ) * 12 + snowpark_fn.call_function("date_part", snowpark_fn.sql_expr("month"), col)


def _dt_interval_to_total_micros(col: snowpark.Column) -> snowpark.Column:
    days = snowpark_fn.call_function("date_part", snowpark_fn.sql_expr("day"), col)
    hours = snowpark_fn.call_function("date_part", snowpark_fn.sql_expr("hour"), col)
    minutes = snowpark_fn.call_function(
        "date_part", snowpark_fn.sql_expr("minute"), col
    )
    seconds = snowpark_fn.call_function(
        "date_part", snowpark_fn.sql_expr("second"), col
    )
    nanos = snowpark_fn.call_function(
        "date_part", snowpark_fn.sql_expr("nanosecond"), col
    )
    return (
        days * 86_400_000_000
        + hours * 3_600_000_000
        + minutes * 60_000_000
        + seconds * 1_000_000
        + nanos / 1_000
    )


def scala_udf_arg_to_variant(
    col: snowpark.Column, typ: snowpark.types.DataType
) -> snowpark.Column:
    """Cast a column to VariantType with two recursive concerns:

    1. **Array null-preservation** – SQL NULL elements in arrays become absent
       values rather than JSON nulls when cast directly; this wraps them via
       PARSE_JSON('null').
    2. **Temporal-to-epoch conversion** – DateType → epoch days, TimestampType →
       epoch microseconds, so the Scala deserializer always receives numbers
       (no string round-trip or timezone ambiguity).

    Both concerns require recursing into StructType, ArrayType and MapType.
    """
    if isinstance(typ, snowpark_type.ArrayType):
        # Recursively build the expression for the element type using a
        # placeholder column "x", then serialize to SQL for the TRANSFORM lambda.
        analyzer = Session.get_active_session()._analyzer
        fn_sql = analyzer.analyze(
            scala_udf_arg_to_variant(
                snowpark_fn.col("x"), typ.element_type
            )._expression,
            defaultdict(),
        )

        # This is a temporary fix for issue in snowpark. Remove once SNOW-3071683 will be resolved
        transformed = snowpark_fn.call_function(
            "transform",
            col,
            snowpark_fn.sql_expr(f"x -> IFNULL({fn_sql}, PARSE_JSON('null'))"),
        )
        return snowpark_fn.cast(transformed, snowpark_type.VariantType())
    elif isinstance(typ, snowpark_type.StructType) and _needs_recursive_cast(typ):
        construct_args = []
        for field in typ.fields:
            field_col = col[field.name]
            construct_args.append(snowpark_fn.lit(field.name))
            if _needs_recursive_cast(field.datatype):
                construct_args.append(
                    scala_udf_arg_to_variant(field_col, field.datatype)
                )
            else:
                construct_args.append(
                    snowpark_fn.cast(field_col, snowpark_type.VariantType())
                )
        return snowpark_fn.cast(
            snowpark_fn.object_construct_keep_null(*construct_args),
            snowpark_type.VariantType(),
        )
    elif isinstance(typ, snowpark_type.MapType) and _needs_recursive_cast(typ):
        # OBJECT_KEYS does not accept MAP type directly, so cast to OBJECT
        # first via TO_OBJECT.
        obj_col = snowpark_fn.call_function("to_object", col)

        # Recursively build the value-coercion expression using a placeholder
        # column "v", then serialize to SQL.
        analyzer = Session.get_active_session()._analyzer
        fn_sql = analyzer.analyze(
            scala_udf_arg_to_variant(snowpark_fn.col("v"), typ.value_type)._expression,
            defaultdict(),
        )

        # Replace placeholder "V" with a reference to the original map value
        # via the state array:  state[1] = original object, k = current key.
        fn_sql_with_value = fn_sql.replace('"V"', "strip_null_value(GET(state[1], k))")

        # REDUCE lambda: (state, k) -> [updated_result_object, original_object]
        lambda_expr = (
            f"(state, k) -> ARRAY_CONSTRUCT("
            f"object_insert(state[0], k, ({fn_sql_with_value})::variant, true), "
            f"state[1])"
        )

        reduce_result = snowpark_fn.call_function(
            "reduce",
            snowpark_fn.call_function("object_keys", obj_col),
            snowpark_fn.array_construct(
                snowpark_fn.object_construct(),  # state[0]: empty result object
                obj_col,  # state[1]: original map as OBJECT
            ),
            snowpark_fn.sql_expr(lambda_expr),
        )
        # Extract the result object (state[0]) from the final state
        return snowpark_fn.get(reduce_result, snowpark_fn.lit(0))
    elif isinstance(typ, snowpark_type.DateType):
        typed_col = snowpark_fn.cast(col, typ)
        return snowpark_fn.cast(
            snowpark_fn.call_function(
                "DATEDIFF",
                snowpark_fn.sql_expr("day"),
                snowpark_fn.sql_expr("'1970-01-01'::DATE"),
                typed_col,
            ),
            snowpark_type.VariantType(),
        )
    elif isinstance(typ, snowpark_type.TimestampType):
        # Cast ensures VARIANT subscript results (from struct fields) become
        # the correct timestamp flavor (NTZ/LTZ); no-op when already typed.
        typed_col = snowpark_fn.cast(col, typ)
        return snowpark_fn.cast(
            snowpark_fn.call_function(
                "DATE_PART",
                snowpark_fn.sql_expr("epoch_microsecond"),
                typed_col,
            ),
            snowpark_type.VariantType(),
        )
    elif isinstance(typ, snowpark_type.YearMonthIntervalType):
        # Snowflake casts intervals to a string like "+1-2"; the Scala client
        # expects a java.time.Period, so emit total months as an integer and
        # let the Scala helper reconstruct Period.ofMonths(...).
        return snowpark_fn.cast(
            _ym_interval_to_total_months(col), snowpark_type.VariantType()
        )
    elif isinstance(typ, snowpark_type.DayTimeIntervalType):
        # Same idea for java.time.Duration: emit total microseconds as a
        # number; the Scala helper reconstructs Duration.of(micros, MICROS).
        return snowpark_fn.cast(
            _dt_interval_to_total_micros(col), snowpark_type.VariantType()
        )
    else:
        return snowpark_fn.cast(col, snowpark_type.VariantType())
