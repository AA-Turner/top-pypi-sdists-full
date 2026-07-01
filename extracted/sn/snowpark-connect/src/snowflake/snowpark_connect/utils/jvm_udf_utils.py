#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Union

import pyspark.sql.connect.proto.types_pb2 as types_proto

import snowflake.snowpark.functions as snowpark_fn
import snowflake.snowpark.types as snowpark_type
from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.expression import UnresolvedAttribute
from snowflake.snowpark._internal.analyzer.unary_expression import (
    Alias as _SnowparkAlias,
)
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import get_scala_version
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.resources_initializer import (
    JSON_4S_JAR_212,
    JSON_4S_JAR_213,
    RESOURCE_PATH,
    SAS_SCALA_UDF_JAR_212,
    SAS_SCALA_UDF_JAR_213,
    SCALA_REFLECT_JAR_212,
    SCALA_REFLECT_JAR_213,
    SPARK_COMMON_UTILS_JAR_212,
    SPARK_COMMON_UTILS_JAR_213,
    SPARK_CONNECT_CLIENT_JAR_212,
    SPARK_CONNECT_CLIENT_JAR_213,
    SPARK_SQL_JAR_212,
    SPARK_SQL_JAR_213,
)
from snowflake.snowpark_connect.typed_column import TypedColumn


@dataclass(frozen=True)
class Param:
    """
    Represents a function parameter with name and data type.

    Attributes:
        name: Parameter name
        data_type: Parameter data type as a string
    """

    name: str
    data_type: str

    def __str__(self):
        return f"{self.name} {self.data_type}"


@dataclass(frozen=True)
class NullHandling(str, Enum):
    """
    Enumeration for UDF null handling behavior.

    Determines how the UDF behaves when input parameters contain null values.
    """

    RETURNS_NULL_ON_NULL_INPUT = "RETURNS NULL ON NULL INPUT"
    CALLED_ON_NULL_INPUT = "CALLED ON NULL INPUT"


@dataclass(frozen=True)
class ReturnType:
    """
    Represents the return type of a function.

    Attributes:
        data_type: Return data type as a string
    """

    data_type: str


@dataclass(frozen=True)
class Signature:
    """
    Represents a function signature with parameters and return type.

    Attributes:
        params: List of function parameters
        returns: Function return type
    """

    params: List[Param]
    returns: ReturnType


@dataclass(frozen=True)
class TypeDescriptor:
    """Single source of truth mapping a Snowpark type to its SQL and Java counterparts.

    For struct inputs use TypeDescriptor.for_struct() to obtain a descriptor with
    per-field breakdowns in .fields.  For all other types, use from_snowpark().
    """

    snowpark_type: snowpark_type.DataType | None
    sql_type: str  # e.g. "BIGINT", "VARCHAR", "VARIANT"
    java_type: str  # e.g. "Long", "String", "Variant"
    is_native: bool  # True when Snowflake passes the value natively (no VARIANT wrap)
    fields: "tuple[TypeDescriptor, ...] | None" = None  # set by for_struct()

    @staticmethod
    def from_snowpark(dt: snowpark_type.DataType | None) -> "TypeDescriptor":
        """Leaf descriptor for a scalar type. StructType → VARIANT (no field decomposition)."""
        if is_native_sql_type(dt):
            return TypeDescriptor(
                snowpark_type=dt,
                sql_type=map_type_to_snowflake_native_sql_type(dt),
                java_type=map_type_to_native_java_type(dt),
                is_native=True,
                fields=None,
            )
        return TypeDescriptor(
            snowpark_type=dt,
            sql_type="VARIANT",
            java_type="Variant",
            is_native=False,
            fields=None,
        )

    @staticmethod
    def for_struct(dt: snowpark_type.StructType) -> "TypeDescriptor":
        """Struct descriptor with per-field TypeDescriptors in .fields."""
        fields = tuple(TypeDescriptor.from_snowpark(f.datatype) for f in dt.fields)
        return TypeDescriptor(
            snowpark_type=dt,
            sql_type="VARIANT",
            java_type="Variant",
            is_native=False,
            fields=fields,
        )


def to_json(types: list[snowpark_type.DataType], escape_quotes: bool = True) -> str:
    result = json.dumps([t.json_value() for t in types])
    return result.replace('"', '\\"') if escape_quotes else result


def build_jvm_udxf_imports(
    session: snowpark.Session, payload: bytes, udf_name: str
) -> List[str]:
    """
    Build the list of imports needed for the JVM UDxF.

    This function:
    1. Saves the UDF payload to a binary file in the session stage
    2. Collects user-uploaded JAR files from the stage
    3. Returns a list of all required JAR files for the UDxF

    Args:
        session: Snowpark session
        payload: Binary payload containing the serialized Scala UDF
        udf_name: Name of the Scala UDF (used for the binary file name)
        is_map_return: Indicates if the UDxF returns a Map (affects imports)

    Returns:
        List of JAR file paths to be imported by the UDxF
    """
    # Save pciudf._payload to a bin file:
    import io

    payload_as_stream = io.BytesIO(payload)
    stage = session.get_session_stage()
    stage_resource_path = stage + RESOURCE_PATH
    closure_binary_file = stage_resource_path + "/scala/bin/" + udf_name + ".bin"
    session.file.put_stream(
        payload_as_stream,
        closure_binary_file,
        overwrite=True,
    )

    from snowflake.snowpark_connect.config import global_config

    config_imports = global_config.get("snowpark.connect.udf.java.imports", "")
    config_imports = (
        {x.strip() for x in config_imports.strip("[] ").split(",") if x.strip()}
        if config_imports
        else set()
    )

    from snowflake.snowpark_connect.utils.spark_session_cache import (
        get_spark_session_cache,
    )

    artifacts_store = get_spark_session_cache().artifacts_store

    return (
        [closure_binary_file]
        + _scala_static_imports_for_udf(stage_resource_path)
        + list(artifacts_store.get_jars())
        + list(config_imports)
    )


def _scala_static_imports_for_udf(stage_resource_path: str) -> list[str]:
    scala_version = get_scala_version()
    if scala_version == "2.12":
        return [
            f"{stage_resource_path}/{SPARK_CONNECT_CLIENT_JAR_212}",
            f"{stage_resource_path}/{SPARK_COMMON_UTILS_JAR_212}",
            f"{stage_resource_path}/{SPARK_SQL_JAR_212}",
            f"{stage_resource_path}/{JSON_4S_JAR_212}",
            f"{stage_resource_path}/{SAS_SCALA_UDF_JAR_212}",
            f"{stage_resource_path}/{SCALA_REFLECT_JAR_212}",  # Required for deserializing Scala lambdas
        ]

    if scala_version == "2.13":
        return [
            f"{stage_resource_path}/{SPARK_CONNECT_CLIENT_JAR_213}",
            f"{stage_resource_path}/{SPARK_COMMON_UTILS_JAR_213}",
            f"{stage_resource_path}/{SPARK_SQL_JAR_213}",
            f"{stage_resource_path}/{JSON_4S_JAR_213}",
            f"{stage_resource_path}/{SAS_SCALA_UDF_JAR_213}",
            f"{stage_resource_path}/{SCALA_REFLECT_JAR_213}",  # Required for deserializing Scala lambdas
        ]

    # invalid Scala version
    exception = ValueError(
        f"Unsupported Scala version: {scala_version}. Snowpark Connect supports Scala 2.12 and 2.13"
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
    raise exception


def map_type_to_java_type(
    t: Union[snowpark_type.DataType, types_proto.DataType]
) -> str:
    """Maps a Snowpark or Spark protobuf type to a Java type string."""
    if not t:
        return "String"
    is_snowpark_type = isinstance(t, snowpark_type.DataType)
    condition = type(t) if is_snowpark_type else t.WhichOneof("kind")
    match condition:
        case snowpark_type.ArrayType | "array":
            return (
                f"{map_type_to_java_type(t.element_type)}[]"
                if is_snowpark_type
                else f"{map_type_to_java_type(t.array.element_type)}[]"
            )
        case snowpark_type.BinaryType | "binary":
            return "byte[]"
        case snowpark_type.BooleanType | "boolean":
            return "Boolean"
        case snowpark_type.ByteType | "byte":
            return "Byte"
        case snowpark_type.DateType | "date":
            return "java.sql.Date"
        case snowpark_type.DecimalType | "decimal":
            return "java.math.BigDecimal"
        case snowpark_type.DoubleType | "double":
            return "Double"
        case snowpark_type.FloatType | "float":
            return "Float"
        case snowpark_type.GeographyType:
            return "Geography"
        case snowpark_type.IntegerType | "integer":
            return "Integer"
        case snowpark_type.LongType | "long":
            return "Long"
        case snowpark_type.MapType | "map":  # can also map to OBJECT in Snowflake
            key_type = (
                map_type_to_java_type(t.key_type)
                if is_snowpark_type
                else map_type_to_java_type(t.map.key_type)
            )
            value_type = (
                map_type_to_java_type(t.value_type)
                if is_snowpark_type
                else map_type_to_java_type(t.map.value_type)
            )
            return f"Map<{key_type}, {value_type}>"
        case snowpark_type.NullType | "null":
            return "String"  # cannot set the return type to Null in Snowpark Java UDAFs
        case snowpark_type.ShortType | "short":
            return "Short"
        case snowpark_type.StringType | "string" | "char" | "varchar":
            return "String"
        case snowpark_type.StructType | "struct":
            return "Variant"
        case snowpark_type.TimestampType | "timestamp" | "timestamp_ntz":
            return "java.sql.Timestamp"
        case snowpark_type.VariantType:
            return "Variant"
        case _:
            exception = ValueError(f"Unsupported Snowpark type: {t}")
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
            raise exception


_NATIVE_SNOWPARK_TYPES = (
    snowpark_type.BooleanType,
    snowpark_type.ByteType,
    snowpark_type.ShortType,
    snowpark_type.IntegerType,
    snowpark_type.LongType,
    snowpark_type.FloatType,
    snowpark_type.DoubleType,
    snowpark_type.StringType,
    # BinaryType excluded: Snowflake stores binary data as VARIANT internally,
    # so the call-site passes VARIANT even when the column type is BINARY.
)


def is_native_sql_type(dt: snowpark_type.DataType | None) -> bool:
    """Returns True for types Snowflake can pass natively to Java UDFs without VARIANT."""
    return isinstance(dt, _NATIVE_SNOWPARK_TYPES)


def is_decomposable_struct(dt: snowpark_type.DataType | None) -> bool:
    """True for any non-empty StructType (decomposable per-field, native or VARIANT per field)."""
    return isinstance(dt, snowpark_type.StructType) and bool(dt.fields)


def map_type_to_snowflake_native_sql_type(dt: snowpark_type.DataType) -> str:
    """Maps a native-compatible Snowpark type to its Snowflake SQL DDL type string."""
    match type(dt):
        case snowpark_type.BooleanType:
            return "BOOLEAN"
        case snowpark_type.ByteType:
            return "TINYINT"
        case snowpark_type.ShortType:
            return "SMALLINT"
        case snowpark_type.IntegerType:
            return "INT"
        case snowpark_type.LongType:
            return "BIGINT"
        case snowpark_type.FloatType:
            return "FLOAT"
        case snowpark_type.DoubleType:
            return "DOUBLE"
        case snowpark_type.StringType:
            return "VARCHAR"
        case _:
            raise ValueError(
                f"map_type_to_snowflake_native_sql_type called with non-native type {dt!r}; "
                "call is_native_sql_type first"
            )


def map_type_to_native_java_type(dt: snowpark_type.DataType) -> str:
    """Maps a native-compatible Snowpark type to the Java boxed type Snowflake passes.

    Integer SQL types (TINYINT/SMALLINT/INT/BIGINT) → Java Long (Snowflake always passes Long
    for fixed-point numbers). Float/Double → Java Double (Snowflake FLOAT is 64-bit).
    """
    match type(dt):
        case snowpark_type.BooleanType:
            return "Boolean"
        case snowpark_type.StringType:
            return "String"
        case (
            snowpark_type.ByteType
            | snowpark_type.ShortType
            | snowpark_type.IntegerType
            | snowpark_type.LongType
        ):
            return "Long"
        case snowpark_type.FloatType | snowpark_type.DoubleType:
            return "Double"
        case _:
            return "Variant"


def gen_pre_narrow_expr(dt: snowpark_type.DataType, arg_name: str) -> str:
    """Java expression that pre-narrows a Snowflake-native Long/Double to the expected boxed type.

    Snowflake passes all fixed-point SQL types as Java Long and FLOAT as Double. This guard
    ensures the right boxed type is present before the value is handed to the Scala closure,
    independent of whether an encoder is available to drive narrowing.

    Used by two paths:
    - The UDAF reduce input (java_udaf_utils): the only place narrowing is strictly load-bearing,
      since the reduce element may have no usable encoder.
    - Decomposed struct fields (scala_udf_utils): defensive. convertInput → fromNativeFields also
      narrows via the per-field encoder / schema-JSON fallback, so for structs this is an
      idempotent double-narrow (e.g. Long → Integer.valueOf(intValue()) → int) rather than a
      correctness requirement.

    The scalar (non-struct) arg path does NOT pre-narrow: convertInput handles it via the
    encoder, or coerceNativeBySnowparkType using the schema JSON when no encoder is present.
    """
    match type(dt):
        case snowpark_type.IntegerType:
            return (
                f"({arg_name} == null ? null : Integer.valueOf({arg_name}.intValue()))"
            )
        case snowpark_type.ShortType:
            return (
                f"({arg_name} == null ? null : Short.valueOf({arg_name}.shortValue()))"
            )
        case snowpark_type.ByteType:
            return f"({arg_name} == null ? null : Byte.valueOf({arg_name}.byteValue()))"
        case snowpark_type.FloatType:
            return (
                f"({arg_name} == null ? null : Float.valueOf({arg_name}.floatValue()))"
            )
        case _:
            return arg_name  # Long, Double, Boolean, String: no narrowing needed


def expand_struct_arg_for_scala_udf(
    tc: TypedColumn,
    column_mapping: ColumnNameMap,
) -> list:
    """Expand a decomposable struct UDF argument into per-field columns.

    When ``tc.col`` is a synthetic expression (e.g. an OBJECT_CONSTRUCT_KEEP_NULL cast
    built from flat DataFrame columns in the Dataset[CaseClass] path), each struct field
    is looked up directly in ``column_mapping``.  This avoids
    ``OBJECT_CONSTRUCT_KEEP_NULL(...)::VARIANT['field']`` — Snowflake would have to
    evaluate the whole object construction just to extract one field.

    When ``tc.col`` is a direct column reference (``UnresolvedAttribute``, or an
    ``Alias`` wrapping one such as ``col("s").alias("p")``) the struct value lives inside
    that named column; its fields must be accessed via subscript.  Performing a flat
    lookup in that case would resolve field names against the *top-level* DataFrame
    columns, which could silently pick up an unrelated sibling column sharing the same
    name.  The alias wrapper is stripped before subscript access because Snowflake error
    1301 forbids aliases in sub-expression position.
    """
    from snowflake.snowpark_connect.utils.variant_utils import scala_udf_arg_to_variant

    # Strip any Alias wrapper before classifying the expression.  Aliases are only valid
    # at the SELECT-list root in Snowflake; carrying one into a sub-expression (e.g.
    # col("person").alias("p")["name"]) raises error 1301.  An aliased column reference
    # like col("person").alias("p") is semantically a direct column ref — treat it the
    # same as col("person") for both the flat-lookup guard and subscript access.
    # Use getattr to guard against future Snowpark refactors that rename or remove
    # _expression. If absent, we fall back to subscript access (safe but not optimized).
    # TODO: stabilize via a Snowpark public API if one becomes available.
    _raw_expr = getattr(tc.col, "_expression", None)
    base_expr = _raw_expr
    if isinstance(base_expr, _SnowparkAlias):
        base_expr = base_expr.child

    # When base_expr is a direct column reference (UnresolvedAttribute), the struct lives
    # inside that named column and its fields must be accessed via subscript.  Flat lookup
    # would resolve field names against the top-level DataFrame columns, which could pick
    # up unrelated sibling columns with the same name.
    use_flat_lookup = base_expr is not None and not isinstance(
        base_expr, UnresolvedAttribute
    )

    # Alias-stripped column to use for subscript access.  When we stripped an alias above,
    # rebuild the column from the bare attribute name so no alias appears in the SQL.
    struct_col = (
        snowpark_fn.col(base_expr.name)
        if isinstance(base_expr, UnresolvedAttribute) and base_expr is not _raw_expr
        else tc.col
    )

    result = []
    for f in tc.typ.fields:
        if use_flat_lookup:
            flat_snowpark_name = (
                column_mapping.get_snowpark_column_name_from_spark_column_name(
                    f.name, allow_non_exists=True
                )
            )
            field_col = (
                snowpark_fn.col(flat_snowpark_name)
                if flat_snowpark_name is not None
                else struct_col[f.name]
            )
        else:
            field_col = struct_col[f.name]
        if is_native_sql_type(f.datatype):
            result.append(field_col)
        else:
            result.append(scala_udf_arg_to_variant(field_col, f.datatype))
    return result
