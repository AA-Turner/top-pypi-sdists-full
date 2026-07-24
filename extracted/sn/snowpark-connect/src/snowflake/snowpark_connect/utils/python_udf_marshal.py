#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Marshal taxonomy for the Python UDF/UDTF boundary.

Unlike the JVM boundary (see ``jvm_udf_utils``), which epoch-lowers temporal types
so they cross as INT/BIGINT, the Python sandbox in Snowflake receives native SQL
types as native Python objects:

    DATE        -> datetime.date
    TIMESTAMP   -> datetime.datetime
    NUMBER      -> int / Decimal
    FLOAT       -> float
    VARCHAR     -> str
    BINARY      -> bytes
    BOOLEAN     -> bool

So there is no ``EPOCH`` kind for Python -- temporal types are ``DIRECT``. VARIANT
is still required for struct/map/variant and array inputs.

This module deliberately depends only on ``snowflake.snowpark.types`` so it can be
imported at module scope from every call site without circular-import risk.
"""

from enum import Enum

from snowflake.snowpark import types as snowpark_type

# Types Python receives natively from Snowflake without any JSON round-trip.
# Includes DateType (unlike the JVM taxonomy, which epoch-lowers it).
#
# TimestampType is handled separately in ``python_marshal_kind``: only the NTZ
# variant (Spark ``TimestampNTZType``, a naive wall clock) is DIRECT. The LTZ /
# session-timezone variant (Spark ``TimestampType``) must stay on the VARIANT
# path -- delivering it natively applies a session-timezone shift that diverges
# from Spark's UTC-instant coercion (see test_udf_timestamp_scalar).
_PYTHON_DIRECT_NATIVE_TYPES = (
    snowpark_type.BooleanType,
    snowpark_type.ByteType,
    snowpark_type.ShortType,
    snowpark_type.IntegerType,
    snowpark_type.LongType,
    snowpark_type.FloatType,
    snowpark_type.DoubleType,
    snowpark_type.StringType,
    snowpark_type.BinaryType,
    snowpark_type.DateType,
)


class PythonMarshalKind(Enum):
    """How a Snowpark type crosses the boundary to a Python UDF/UDTF.

    ``DIRECT``  – native SQL type; Snowflake delivers a native Python object
                  (int, float, str, bool, bytes, datetime.date, datetime.datetime,
                  Decimal). No VARIANT serialization needed.
    ``VARIANT`` – struct/map/variant/array; must be JSON-encoded as VARIANT for
                  the Python sandbox to receive it.
    """

    DIRECT = "direct"
    VARIANT = "variant"


def python_marshal_kind(dt: snowpark_type.DataType | None) -> PythonMarshalKind:
    """Classify how ``dt`` is marshalled across the Python UDF/UDTF boundary."""
    if isinstance(dt, _PYTHON_DIRECT_NATIVE_TYPES):
        return PythonMarshalKind.DIRECT
    if isinstance(dt, snowpark_type.TimestampType):
        # Only naive NTZ timestamps are safe to pass natively. LTZ (and the
        # session-timezone default) must round-trip through VARIANT to preserve
        # Spark's UTC-instant coercion semantics.
        if dt.tz == snowpark_type.TimestampTimeZone.NTZ:
            return PythonMarshalKind.DIRECT
        return PythonMarshalKind.VARIANT
    if isinstance(dt, snowpark_type.DecimalType):
        if dt.scale > dt.precision:
            raise ValueError(
                f"Invalid DecimalType: scale ({dt.scale}) cannot be greater than "
                f"precision ({dt.precision})"
            )
        if 1 <= dt.precision <= 38:
            return PythonMarshalKind.DIRECT
    return PythonMarshalKind.VARIANT


def python_is_native_input(dt: snowpark_type.DataType | None) -> bool:
    """True when ``dt`` can be passed natively to a Python UDF/UDTF without VARIANT."""
    return python_marshal_kind(dt) is PythonMarshalKind.DIRECT


def map_type_to_snowflake_python_native_sql_type(
    dt: snowpark_type.DataType,
) -> snowpark_type.DataType:
    """Return the Snowpark DataType to use in the Python UDF/UDTF DDL for a native type.

    Unlike the JVM mapper (which lowers DATE/TIMESTAMP to epoch INT/BIGINT), Python uses
    the SQL type directly -- Snowflake delivers the value as a native Python object -- so
    this is a pass-through that also rejects non-native types. ``python_is_native_input``
    is the single source of truth for "native" (including the NTZ-only TimestampType and
    valid-precision DecimalType rules); callers must gate on it first.
    """
    if not python_is_native_input(dt):
        raise ValueError(
            f"map_type_to_snowflake_python_native_sql_type called with non-native "
            f"type {dt!r}; call python_is_native_input first"
        )
    return dt


def native_or_variant_input_types(
    call_site_types: list[snowpark_type.DataType],
) -> list[snowpark_type.DataType]:
    """Per-position UDF/UDTF DDL input types for a list of call-site types.

    Native scalars keep their SQL type; every other position becomes ``VariantType``.
    """
    return [
        map_type_to_snowflake_python_native_sql_type(dt)
        if python_is_native_input(dt)
        else snowpark_type.VariantType()
        for dt in call_site_types
    ]


def encode_native_or_variant_args(typed_args, declared_types, variant_encoder):
    """Encode call-site args in lockstep with a UDF/UDTF's declared DDL input_types.

    For each arg: if the DDL declared its position as a native SQL type, pass the
    column through unchanged; otherwise (struct/map/variant/array, or a position
    beyond ``declared_types``) box it with ``variant_encoder``.

    ``variant_encoder`` is supplied by the caller -- ``col.cast(VariantType())`` for
    the ``session.table_function`` call sites, ``to_variant(col)`` for the
    ``join_table_function`` call sites -- so each site keeps its established VARIANT
    boxing. (Those two are not unconditionally equivalent for arrays with SQL NULL
    elements; unifying them is deferred to avoid a behavioral change here.)
    """
    encoded = []
    for i, tc in enumerate(typed_args):
        declared = declared_types[i] if i < len(declared_types) else None
        encoded.append(
            tc.col if python_is_native_input(declared) else variant_encoder(tc.col)
        )
    return encoded
