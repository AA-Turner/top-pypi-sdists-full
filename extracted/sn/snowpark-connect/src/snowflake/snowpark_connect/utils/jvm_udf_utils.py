#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from dataclasses import dataclass
from enum import Enum
from typing import List, Union

import snowflake.snowpark.types as snowpark_type
import snowflake.snowpark_connect.includes.python.pyspark.sql.connect.proto.types_pb2 as types_proto
from snowflake import snowpark
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

    # Format the user jars to be used in the IMPORTS clause of the stored procedure.
    return (
        [closure_binary_file]
        + _scala_static_imports_for_udf(stage_resource_path)
        + list(session._artifact_jars)
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


def cast_java_map_args_from_given_type(
    arg_name: str, input_type: Union[snowpark_type.DataType, types_proto.DataType]
) -> str:
    """If the input_type is a Map or Struct, cast the argument arg_name to the correct type in Java."""
    is_snowpark_type = isinstance(input_type, snowpark_type.DataType)

    def convert_from_string_to_type(
        arg_name: str, t: Union[snowpark_type.DataType, types_proto.DataType]
    ) -> str:
        """Convert the string argument arg_name to the specified type t in Java."""
        condition = type(t) if is_snowpark_type else t.WhichOneof("kind")
        match condition:
            case snowpark_type.BinaryType | "binary":
                return arg_name + ".getBytes()"
            case snowpark_type.BooleanType | "boolean":
                return f"Boolean.valueOf({arg_name}"
            case snowpark_type.ByteType | "byte":
                return arg_name + ".getBytes()[0]"  # TODO: verify if this is correct
            case snowpark_type.DateType | "date":
                return f"java.sql.Date.valueOf({arg_name})"
            case snowpark_type.DecimalType | "decimal":
                return f"new BigDecimal({arg_name})"
            case snowpark_type.DoubleType | "double":
                return f"Double.valueOf({arg_name}"
            case snowpark_type.FloatType | "float":
                return f"Float.valueOf({arg_name}"
            case snowpark_type.IntegerType | "integer":
                return f"Integer.valueOf({arg_name}"
            case snowpark_type.LongType | "long":
                return f"Long.valueOf({arg_name}"
            case snowpark_type.ShortType | "short":
                return f"Short.valueOf({arg_name}"
            case snowpark_type.StringType | "string" | "char" | "varchar":
                return arg_name
            case snowpark_type.TimestampType | "timestamp" | "timestamp_ntz":
                return f"java.sql.Timestamp.valueOf({arg_name})"  # todo add test
            case _:
                exception = ValueError(f"Unsupported Snowpark type: {t}")
                attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_TYPE)
                raise exception

    if (is_snowpark_type and isinstance(input_type, snowpark_type.MapType)) or (
        not is_snowpark_type and input_type.WhichOneof("kind") == "map"
    ):
        key_type = input_type.key_type if is_snowpark_type else input_type.map.key_type
        value_type = (
            input_type.value_type if is_snowpark_type else input_type.map.value_type
        )
        key_converter = "{" + convert_from_string_to_type("e.getKey()", key_type) + "}"
        value_converter = (
            "{" + convert_from_string_to_type("e.getValue()", value_type) + "}"
        )
        return f"""
        {arg_name}.entrySet()
            .stream()
            .collect(Collectors.toMap(
                e -> {key_converter},
                e -> {value_converter}
        ));
        """
    else:
        return arg_name
