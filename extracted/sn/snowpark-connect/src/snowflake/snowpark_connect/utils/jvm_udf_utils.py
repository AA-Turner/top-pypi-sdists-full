#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import json
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, List, Union

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
from snowflake.snowpark_connect.utils.variant_utils import (
    epoch_to_temporal_col,
    jvm_udf_arg_to_variant,
    temporal_to_epoch_col,
)

if TYPE_CHECKING:
    from snowflake.snowpark_connect.utils.udf_helper import SnowparkUdfBase


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


def _build_jvm_udxf_imports(
    session: snowpark.Session, payload: bytes, udf_name: str
) -> List[str]:
    """
    Build the list of imports needed for the JVM UDxF (stage-upload path).

    Internal helper used by ``build_udxf_imports`` for the normal (non-Native-App)
    case; other code should call ``build_udxf_imports``.

    This function:
    1. Saves the UDF payload to a binary file in the session stage
    2. Collects user-uploaded JAR files from the stage
    3. Returns a list of all required JAR files for the UDxF
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


def _scala_static_imports_dcr() -> list[str]:
    """Relative version-stage paths for the static SCOS JARs (DCR inline-closure mode)."""
    scala_version = get_scala_version()
    if scala_version == "2.12":
        return [
            f"{RESOURCE_PATH}/{SPARK_CONNECT_CLIENT_JAR_212}",
            f"{RESOURCE_PATH}/{SPARK_COMMON_UTILS_JAR_212}",
            f"{RESOURCE_PATH}/{SPARK_SQL_JAR_212}",
            f"{RESOURCE_PATH}/{JSON_4S_JAR_212}",
            f"{RESOURCE_PATH}/{SAS_SCALA_UDF_JAR_212}",
            f"{RESOURCE_PATH}/{SCALA_REFLECT_JAR_212}",
        ]
    if scala_version == "2.13":
        return [
            f"{RESOURCE_PATH}/{SPARK_CONNECT_CLIENT_JAR_213}",
            f"{RESOURCE_PATH}/{SPARK_COMMON_UTILS_JAR_213}",
            f"{RESOURCE_PATH}/{SPARK_SQL_JAR_213}",
            f"{RESOURCE_PATH}/{JSON_4S_JAR_213}",
            f"{RESOURCE_PATH}/{SAS_SCALA_UDF_JAR_213}",
            f"{RESOURCE_PATH}/{SCALA_REFLECT_JAR_213}",
        ]
    exception = ValueError(
        f"Unsupported Scala version: {scala_version}. Snowpark Connect supports Scala 2.12 and 2.13"
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
    raise exception


# The closure is base64-embedded as a Java string literal. The JVM constant-pool
# CONSTANT_Utf8 limit is 65535 bytes; base64 is pure ASCII (1 byte/char) and
# expands 4/3, so the hard cap is 65535 * 3/4 ≈ 48 KB of raw closure. We use 40 KB
# as a conservative ceiling.
#
# Empirical data (from scala/src/test/resources/testUserFilter.bin):
#   A real filter UDF on TestUser{id:Int, name:String, Address{street,city,zip}} = 3 KB.
#   Case class transforms with 10–20 fields land at 3–10 KB.
#   The 40 KB ceiling is hit only when a closure *captures* a large in-memory collection
#   (~500+ Map entries / ~1500+ Seq elements), which is an anti-pattern regardless — that
#   data should be passed as a table argument or loaded from a stage, not embedded in the closure.
_INLINE_CLOSURE_MAX_BYTES = 40 * 1024


def build_udxf_imports(
    session: snowpark.Session, payload: bytes, udf_name: str
) -> tuple[list[str], bytes | None]:
    """Build IMPORTS for a closure-based JVM UDxF (scalar UDF, UDAF, or UDTF),
    returning (imports, inline_payload).

    Native-app-aware wrapper over ``_build_jvm_udxf_imports``:

    - Normal mode: delegates to ``_build_jvm_udxf_imports`` (uploads the closure
      binary to the session stage, returns absolute stage paths); ``inline_payload``
      is None.
    - Native App mode: skips the binary upload and returns relative version-stage
      paths for the static SCOS JARs plus any user-configured paths from
      ``snowpark.connect.udf.scala.version_stage_imports``; ``inline_payload`` is
      the raw payload bytes to be base64-embedded in the Java handler body (via
      ``apply_inline_closure``).
    """
    from snowflake.snowpark_connect.config import global_config, is_native_app_mode
    from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code

    if not is_native_app_mode():
        return _build_jvm_udxf_imports(session, payload, udf_name), None

    if len(payload) > _INLINE_CLOSURE_MAX_BYTES:
        exception = ValueError(
            f"JVM UDxF closure ({len(payload)} bytes) exceeds the {_INLINE_CLOSURE_MAX_BYTES}-byte "
            "limit for Native App inline-closure mode. The closure is base64-embedded as a Java "
            "string literal, and the JVM constant-pool UTF-8 limit (65535 bytes) caps the raw "
            "closure at ~48 KB. Typical case-class transform closures are 1–10 KB; this limit is "
            "usually exceeded only when the closure captures a large in-memory collection "
            "(e.g. ~500 Map entries). Consider passing that data as a table argument instead of "
            "capturing it in the closure."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
        raise exception

    user_jar_config = global_config.get(
        "snowpark.connect.udf.scala.version_stage_imports", ""
    )
    user_jars = (
        [x.strip() for x in user_jar_config.strip("[] ").split(",") if x.strip()]
        if user_jar_config
        else []
    )
    invalid = [j for j in user_jars if not j.startswith("/")]
    if invalid:
        exception = ValueError(
            f"snowpark.connect.udf.scala.version_stage_imports contains invalid paths: {invalid}. "
            "In DCR inline-closure mode all imports must be version-stage-relative paths starting with '/'."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
        raise exception

    return _scala_static_imports_dcr() + user_jars, payload


def apply_inline_closure(
    body: str, imports: list[str], inline_payload: bytes | None
) -> str:
    """Rewrite a generated JVM-UDxF Java body to source its closure inline.

    In normal (file) mode this is a no-op: the body keeps its
    ``OPERATION_FILE`` field and ``deserializeUdfPacket(OPERATION_FILE)`` call.

    In Native App inline-closure mode (``inline_payload`` set) the closure
    binary is not uploaded to the session stage; instead the bytes are
    base64-embedded in the handler and deserialized via
    ``deserializeUdfPacketFromBytes``. This mirrors what
    ``JavaScalarUDFDef._gen_body_java`` does for the scalar path (#4747), and is
    shared by the UDAF and all UDTF handler generators so a single
    ``build_udxf_imports`` + ``apply_inline_closure`` pair covers every
    closure-based JVM UDxF.

    Both the ``OPERATION_FILE`` field declaration and the deserialize call are
    matched by exact text. If either target is absent (e.g. a UDxF template drifted
    in modifier order or spacing), this raises instead of silently no-op'ing — a
    silent miss would leave the handler reading a ``.bin`` that was never uploaded
    in native-app mode, i.e. a runtime failure with no test signal.
    """
    if inline_payload is None:
        return body

    import base64

    # The def's _gen_body computes operation_file identically (imports[0] basename),
    # so this target matches the field declaration it emitted.
    operation_file = imports[0].split("/")[-1]
    b64 = base64.b64encode(inline_payload).decode("ascii")
    field_decl = (
        f"private static final byte[] CLOSURE_BYTES = "
        f'java.util.Base64.getDecoder().decode("{b64}");'
    )

    def _require_replace(text: str, target: str, repl: str, what: str) -> str:
        if target not in text:
            exception = RuntimeError(
                f"apply_inline_closure: {what} not found in the generated handler; a "
                "JVM-UDxF template has drifted from apply_inline_closure. Update the "
                "replacement targets here (jvm_udf_utils.apply_inline_closure)."
            )
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            raise exception
        return text.replace(target, repl)

    body = _require_replace(
        body,
        f'private final static String OPERATION_FILE = "{operation_file}";',
        field_decl,
        "OPERATION_FILE declaration",
    )
    body = _require_replace(
        body,
        "com.snowflake.sas.scala.Utils$.MODULE$.deserializeUdfPacket(OPERATION_FILE)",
        "com.snowflake.sas.scala.Utils$.MODULE$.deserializeUdfPacketFromBytes(CLOSURE_BYTES)",
        "deserializeUdfPacket(OPERATION_FILE) call",
    )
    return body


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


# Native types passed to the Java UDF as their own SQL type, unchanged. DecimalType is
# native too but guarded on precision/scale, so it is classified in jvm_marshal_kind.
_DIRECT_NATIVE_TYPES = (
    snowpark_type.BooleanType,
    snowpark_type.ByteType,
    snowpark_type.ShortType,
    snowpark_type.IntegerType,
    snowpark_type.LongType,
    snowpark_type.FloatType,
    snowpark_type.DoubleType,
    snowpark_type.StringType,
    # Binary maps directly to BINARY / byte[].
    snowpark_type.BinaryType,
)

# Native types whose wire representation is an epoch number (INT/BIGINT), not their own
# SQL type: lowered via temporal_to_epoch_col on the call-site and reconstructed via
# epoch_to_temporal_col on the return side.
_EPOCH_NATIVE_TYPES = (
    snowpark_type.DateType,
    snowpark_type.TimestampType,
    snowpark_type.YearMonthIntervalType,
    snowpark_type.DayTimeIntervalType,
)


class JvmMarshalKind(Enum):
    """How a Snowpark type crosses the boundary to a JVM (Scala/Java) UDF.

    Single source of truth for the native-fast-path type taxonomy: the encode/decode
    primitives, the predicates, and the DDL/Java type mappers all classify a type once
    via ``jvm_marshal_kind`` instead of repeating the rules.
    """

    DIRECT = "direct"  # native SQL type, passed unchanged
    EPOCH = "epoch"  # temporal/interval, passed as epoch INT/BIGINT, reconstructed on return
    VARIANT = "variant"  # non-native, VARIANT round-trip


class UdfKind(Enum):
    """Kind of UDF, used to select the encode-args → call → decode-result contract.

    Each value corresponds to a distinct UDF registration mechanism and boundary protocol:

    * ``SCALA_UDF``         – Scala scalar UDF: temporals lowered to epoch INT/BIGINT,
      non-native types wrapped in VARIANT, struct args expanded per-field;
      ``decode_jvm_udf_result`` reconstructs the declared type on return.
    * ``JAVA_UDAF``         – Scala/Java UDAF: same JVM encoding as SCALA_UDF but struct
      arguments are never decomposed (the UDAF accumulator receives the whole VARIANT).
    * ``PYTHON_REGISTERED`` – Python UDF registered via ``spark.udf.register``: each
      argument is cast to VARIANT (DDL params default to VARIANT); a VARIANT-backed
      return is cast back.
    * ``JAVA_SCALAR``       – Java UDF registered via ``spark.udf.registerJavaFunction``:
      same VARIANT-boundary protocol as PYTHON_REGISTERED.
    * ``PYTHON_INLINE``     – Inline Python UDF (``df.mapPartitions`` etc.): arguments
      pass through unchanged; a VARIANT-backed Map/Struct return is reconstructed via
      PARSE_JSON then cast.
    """

    SCALA_UDF = "scala_udf"
    JAVA_UDAF = "java_udaf"
    PYTHON_REGISTERED = "python_registered"
    JAVA_SCALAR = "java_scalar"
    PYTHON_INLINE = "python_inline"


def jvm_marshal_kind(dt: snowpark_type.DataType | None) -> JvmMarshalKind:
    """Classify how ``dt`` is marshalled across the JVM UDF boundary."""
    if isinstance(dt, _EPOCH_NATIVE_TYPES):
        return JvmMarshalKind.EPOCH
    if isinstance(dt, _DIRECT_NATIVE_TYPES):
        return JvmMarshalKind.DIRECT
    if isinstance(dt, snowpark_type.DecimalType):
        if dt.scale > dt.precision:
            raise ValueError(
                f"Invalid DecimalType: scale ({dt.scale}) cannot be greater than "
                f"precision ({dt.precision})"
            )
        if 1 <= dt.precision <= 38:
            return JvmMarshalKind.DIRECT
    return JvmMarshalKind.VARIANT


def is_native_sql_type(dt: snowpark_type.DataType | None) -> bool:
    """Returns True for types Snowflake can pass natively to Java UDFs without VARIANT."""
    return jvm_marshal_kind(dt) in (JvmMarshalKind.DIRECT, JvmMarshalKind.EPOCH)


def needs_epoch_lowering(dt: snowpark_type.DataType | None) -> bool:
    """True for native temporal/interval types whose wire form is an epoch INT/BIGINT.

    These are passed as epoch values to the UDF and reconstructed on the return side,
    instead of as their native SQL type (DATE/TIMESTAMP/INTERVAL).
    """
    return jvm_marshal_kind(dt) is JvmMarshalKind.EPOCH


def encode_jvm_udf_arg(
    col: snowpark.Column, typ: snowpark_type.DataType
) -> snowpark.Column:
    """Encode a scalar (non-decomposed) JVM UDF argument into the form its native DDL
    parameter expects:

      * EPOCH   temporal / interval → epoch INT/BIGINT (temporal_to_epoch_col)
      * DIRECT  other native types  → passed through unchanged
      * VARIANT non-native types    → VARIANT round-trip (jvm_udf_arg_to_variant)

    Inverse of ``decode_jvm_udf_result``. Shared by the registered-UDF
    (map_unresolved_function), inline-UDF (map_udf), struct-field
    (expand_struct_arg_for_jvm_udf), and UDTF (map_map_partitions) call sites.
    """
    kind = jvm_marshal_kind(typ)
    if kind is JvmMarshalKind.EPOCH:
        return temporal_to_epoch_col(col, typ)
    if kind is JvmMarshalKind.DIRECT:
        return col
    return jvm_udf_arg_to_variant(col, typ)


def is_decomposable_struct(dt: snowpark_type.DataType | None) -> bool:
    """True for any non-empty StructType (decomposable per-field, native or VARIANT per field)."""
    return isinstance(dt, snowpark_type.StructType) and bool(dt.fields)


def map_type_to_snowflake_native_sql_type(dt: snowpark_type.DataType) -> str:
    """Maps a native-compatible Snowpark type to its Snowflake SQL DDL type string.

    Temporal/interval types use an epoch numeric type (INT/BIGINT), not the SQL temporal
    type, so the Scala handler always receives a plain Long.
    """
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
        # Temporal: epoch days (INT) or epoch microseconds / total microseconds (BIGINT).
        case snowpark_type.DateType:
            return "INT"
        case snowpark_type.TimestampType:
            return "BIGINT"
        case snowpark_type.YearMonthIntervalType:
            return "INT"
        case snowpark_type.DayTimeIntervalType:
            return "BIGINT"
        # Binary: direct native mapping.
        case snowpark_type.BinaryType:
            return "BINARY"
        # Decimal: carry precision/scale.
        case snowpark_type.DecimalType:
            return f"NUMBER({dt.precision},{dt.scale})"
        case _:
            raise ValueError(
                f"map_type_to_snowflake_native_sql_type called with non-native type {dt!r}; "
                "call is_native_sql_type first"
            )


def map_type_to_native_java_type(dt: snowpark_type.DataType) -> str:
    """Maps a native-compatible Snowpark type to the Java boxed type Snowflake passes.

    Integer SQL types (TINYINT/SMALLINT/INT/BIGINT) → Java Long (Snowflake always passes Long
    for fixed-point numbers). Float/Double → Java Double (Snowflake FLOAT is 64-bit).
    Temporal/interval types are passed as epoch INT/BIGINT, so they also map to Long.
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
            # Temporal types passed as epoch INT/BIGINT → Long.
            | snowpark_type.DateType
            | snowpark_type.TimestampType
            | snowpark_type.YearMonthIntervalType
            | snowpark_type.DayTimeIntervalType
        ):
            return "Long"
        case snowpark_type.FloatType | snowpark_type.DoubleType:
            return "Double"
        case snowpark_type.BinaryType:
            return "byte[]"
        case snowpark_type.DecimalType:
            return "java.math.BigDecimal"
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


def expand_struct_arg_for_jvm_udf(
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
        result.append(encode_jvm_udf_arg(field_col, f.datatype))
    return result


def encode_jvm_udf_args(
    udf: "SnowparkUdfBase",
    typed_args: list[TypedColumn],
    column_mapping: ColumnNameMap,
) -> list:
    """Encode all arguments of a JVM (Scala) UDF for its native call signature.

    Owns the per-argument decision shared by the registered-UDF (map_unresolved_function)
    and inline-UDF (map_udf) call sites: a decomposable struct expands to per-field columns
    (each encoded via expand_struct_arg_for_jvm_udf), every other argument is encoded with
    encode_jvm_udf_arg. UDAFs never decompose their struct argument.
    """
    out: list = []
    for position, tc in enumerate(typed_args):
        if udf.kind is not UdfKind.JAVA_UDAF and udf.decomposes_struct_arg(
            position, tc.typ
        ):
            out.extend(expand_struct_arg_for_jvm_udf(tc, column_mapping))
        else:
            out.append(encode_jvm_udf_arg(tc.col, tc.typ))
    return out


def jvm_return_needs_decode(
    processed_rt: snowpark_type.DataType,
    original_rt: snowpark_type.DataType,
) -> bool:
    """True when a JVM UDF's raw result must be reconstructed to its declared type.

    Decode is needed unless the DDL already returns the declared type directly: a
    non-DIRECT processed type means the DDL returns VARIANT (non-native) or an epoch
    INT/BIGINT (temporal), and a processed type differing from the declared one needs a
    narrowing cast.
    """
    return (
        jvm_marshal_kind(processed_rt) is not JvmMarshalKind.DIRECT
        or processed_rt != original_rt
    )


def decode_jvm_udf_result(
    col: snowpark.Column, return_type: snowpark_type.DataType
) -> snowpark.Column:
    """Reconstruct a JVM UDF / UDTF native-path result column to its declared type.

    Per-value inverse of encode_jvm_udf_arg, dispatched purely on the type's marshal kind:

      * EPOCH           → epoch_to_temporal_col (epoch INT/BIGINT → temporal/interval)
      * DIRECT / VARIANT → cast to the declared type (the cast also un-wraps a
        VARIANT-backed array/map/struct result)

    Used by SnowparkUdfBase.call_and_marshal (scalar UDFs) and output_struct_utils
    (UDTF output). The Scala encode end's counterpart is
    UdfPacketUtils.encodeTemporalToEpoch.
    """
    if jvm_marshal_kind(return_type) is JvmMarshalKind.EPOCH:
        return epoch_to_temporal_col(col, return_type)
    return col.cast(return_type)
