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
    # floor(seconds) strips any fractional-seconds component that some Snowflake
    # DATE_PART implementations return for INTERVAL types, avoiding double-counting
    # with the nanoseconds term.  nanos % 1_000_000_000 yields only the sub-second
    # nanoseconds regardless of whether DATE_PART('nanosecond') returns the total or
    # just the fractional component.
    return (
        days * 86_400_000_000
        + hours * 3_600_000_000
        + minutes * 60_000_000
        + snowpark_fn.cast(
            snowpark_fn.call_function("floor", seconds), snowpark_type.LongType()
        )
        * 1_000_000
        + snowpark_fn.cast(
            snowpark_fn.call_function("mod", nanos, snowpark_fn.lit(1_000_000_000))
            / snowpark_fn.lit(1_000),
            snowpark_type.LongType(),
        )
    )


def temporal_to_epoch_col(
    col: snowpark.Column, typ: snowpark.types.DataType
) -> snowpark.Column:
    """Convert a temporal/interval column to its canonical epoch numeric representation.

    Returns the numeric column WITHOUT a VARIANT or type cast, so callers can
    wrap it in the appropriate cast (VARIANT for the slow path, INT/BIGINT for
    the native fast path).

    Mapping:
      DateType              → epoch days (INT)        via DATEDIFF(day, '1970-01-01'::DATE, col)
      TimestampType         → epoch microseconds (BIGINT) via DATE_PART(epoch_microsecond, col)
      YearMonthIntervalType → total months (INT)      via year*12 + month parts
      DayTimeIntervalType   → total microseconds (BIGINT) via summed time parts
    """
    if isinstance(typ, snowpark_type.DateType):
        return snowpark_fn.call_function(
            "DATEDIFF",
            snowpark_fn.sql_expr("day"),
            snowpark_fn.sql_expr("'1970-01-01'::DATE"),
            col,
        )
    elif isinstance(typ, snowpark_type.TimestampType):
        # Resolve tz flavor before casting: a bare TimestampType() without an
        # explicit NTZ/LTZ flavor is governed by the Snowflake session parameter
        # TIMESTAMP_TYPE_MAPPING, which SAS does not control (timestamp-best-practices.md:3).
        # Mirror what epoch_to_temporal_col does on the return side: fall back to
        # the session timestampType so both directions use the same flavor.
        from snowflake.snowpark.types import TimestampTimeZone
        from snowflake.snowpark_connect.config import get_timestamp_type

        tz = typ.tz
        if tz not in (TimestampTimeZone.NTZ, TimestampTimeZone.LTZ):
            # TimestampTimeZone.TZ (timezone-aware) is not supported on the native
            # epoch path; DEFAULT falls back to the session timestamp type.
            if tz == TimestampTimeZone.TZ:
                raise ValueError(
                    "temporal_to_epoch_col: TimestampTimeZone.TZ columns are not "
                    "supported on the JVM native fast-path; cast to TIMESTAMP_NTZ or "
                    "TIMESTAMP_LTZ before passing to a native-path Scala UDF."
                )
            tz = get_timestamp_type().tz
        resolved_type = snowpark_type.TimestampType(tz)
        typed_col = snowpark_fn.cast(col, resolved_type)
        return snowpark_fn.call_function(
            "DATE_PART",
            snowpark_fn.sql_expr("epoch_microsecond"),
            typed_col,
        )
    elif isinstance(typ, snowpark_type.YearMonthIntervalType):
        # Snowflake casts intervals to a string like "+1-2"; the Scala client
        # expects a java.time.Period, so emit total months as an integer and
        # let the Scala helper reconstruct Period.ofMonths(...).
        return _ym_interval_to_total_months(col)
    elif isinstance(typ, snowpark_type.DayTimeIntervalType):
        # Same idea for java.time.Duration: emit total microseconds as a
        # number; the Scala helper reconstructs Duration.of(micros, MICROS).
        return _dt_interval_to_total_micros(col)
    else:
        raise ValueError(f"temporal_to_epoch_col called with non-temporal type {typ!r}")


def epoch_to_temporal_col(
    col: snowpark.Column, return_type: snowpark.types.DataType
) -> snowpark.Column:
    """Reconstruct a temporal/interval column from its epoch numeric representation.

    Inverse of temporal_to_epoch_col. Called on the return side of native-path
    Scala UDFs to turn the epoch INT/BIGINT back into the original temporal type.

    DateType              ← DATEADD(day, epoch_days, '1970-01-01'::DATE)
    TimestampType(NTZ/LTZ)← TO_TIMESTAMP_NTZ/LTZ(epoch_micros, 6)
    YearMonthIntervalType ← total_months::INTERVAL MONTH → cast to full YMI type
    DayTimeIntervalType   ← (total_micros / 1_000_000)::INTERVAL SECOND
    """
    if isinstance(return_type, snowpark_type.DateType):
        return snowpark_fn.call_function(
            "DATEADD",
            snowpark_fn.sql_expr("day"),
            col,
            snowpark_fn.sql_expr("'1970-01-01'::DATE"),
        )
    elif isinstance(return_type, snowpark_type.TimestampType):
        from snowflake.snowpark.types import TimestampTimeZone
        from snowflake.snowpark_connect.config import get_timestamp_type

        # Reconstruct using the return type's OWN timezone flavor, not the session
        # default. A java.time.LocalDateTime return is TimestampType(NTZ) and must
        # round-trip as TIMESTAMP_NTZ (wall-clock preserved); java.sql.Timestamp /
        # java.time.Instant returns are TimestampType(LTZ). Falling back to the session
        # timestampType here would store a LocalDateTime as LTZ, making it
        # indistinguishable from a genuine LTZ value on the input side and shifting the
        # wall-clock by the session offset on read-back. Only fall back to the session
        # type when the return type carries no explicit flavor.
        tz = return_type.tz
        if tz not in (TimestampTimeZone.NTZ, TimestampTimeZone.LTZ):
            if tz == TimestampTimeZone.TZ:
                raise ValueError(
                    "epoch_to_temporal_col: TimestampTimeZone.TZ is not supported on "
                    "the JVM native fast-path; use TIMESTAMP_NTZ or TIMESTAMP_LTZ."
                )
            tz = get_timestamp_type().tz
        fn = "TO_TIMESTAMP_NTZ" if tz == TimestampTimeZone.NTZ else "TO_TIMESTAMP_LTZ"
        return snowpark_fn.call_function(fn, col, snowpark_fn.lit(6))
    elif isinstance(return_type, snowpark_type.YearMonthIntervalType):
        # CAST(integer AS INTERVAL DAY/SECOND) is undefined; Snowflake only accepts
        # casting an integer to the *finest* interval unit (INTERVAL MONTH), then
        # widening to the requested field range — same approach as map_cast.py.
        months_interval = col.cast(
            snowpark_type.YearMonthIntervalType(
                snowpark_type.YearMonthIntervalType.MONTH,
                snowpark_type.YearMonthIntervalType.MONTH,
            )
        )
        return months_interval.cast(return_type)
    elif isinstance(return_type, snowpark_type.DayTimeIntervalType):
        # epoch encodes total microseconds; convert to fractional seconds (the finest
        # DayTime unit that Snowflake accepts from a number) and cast to INTERVAL SECOND,
        # then widen the interval to the requested field range. The widening interval→
        # interval cast is required: a bare INTERVAL SECOND (DayTimeIntervalType(SECOND,
        # SECOND)) is serialized to the Arrow client as zero, whereas the canonical
        # DAY..SECOND range round-trips correctly. Mirrors the YearMonthInterval branch.
        total_seconds = col / snowpark_fn.lit(1_000_000)
        seconds_interval = total_seconds.cast(
            snowpark_type.DayTimeIntervalType(
                snowpark_type.DayTimeIntervalType.SECOND,
                snowpark_type.DayTimeIntervalType.SECOND,
            )
        )
        return seconds_interval.cast(return_type)
    else:
        raise ValueError(
            f"epoch_to_temporal_col called with non-temporal type {return_type!r}"
        )


def jvm_udf_arg_to_variant(
    col: snowpark.Column, typ: snowpark.types.DataType
) -> snowpark.Column:
    """Cast a column to VariantType with two recursive concerns:

    1. **Array null-preservation** – SQL NULL elements in arrays become absent
       values rather than JSON nulls when cast directly; this wraps them via
       PARSE_JSON('null').
    2. **Temporal-to-epoch conversion** – DateType → epoch days, TimestampType →
       epoch microseconds, so the JVM deserializer always receives numbers
       (no string round-trip or timezone ambiguity).

    Both concerns require recursing into StructType, ArrayType and MapType. This is the
    VARIANT branch of encode_jvm_udf_arg, used directly by call sites (cogroup, pivot)
    that always wrap their arguments in VARIANT.
    """
    if isinstance(typ, snowpark_type.ArrayType):
        # Recursively build the expression for the element type using a
        # placeholder column "x", then serialize to SQL for the TRANSFORM lambda.
        analyzer = Session.get_active_session()._analyzer
        fn_sql = analyzer.analyze(
            jvm_udf_arg_to_variant(snowpark_fn.col("x"), typ.element_type)._expression,
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
                construct_args.append(jvm_udf_arg_to_variant(field_col, field.datatype))
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
            jvm_udf_arg_to_variant(snowpark_fn.col("v"), typ.value_type)._expression,
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
    elif isinstance(
        typ,
        (
            snowpark_type.DateType,
            snowpark_type.TimestampType,
            snowpark_type.YearMonthIntervalType,
            snowpark_type.DayTimeIntervalType,
        ),
    ):
        return snowpark_fn.cast(
            temporal_to_epoch_col(col, typ), snowpark_type.VariantType()
        )
    else:
        return snowpark_fn.cast(col, snowpark_type.VariantType())
