#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""
Scala UDF utilities for Snowpark Connect.

This module provides utilities for creating and managing Scala User-Defined Functions (UDFs)
in Snowflake through Snowpark Connect. It handles the conversion between different type systems
(Snowpark, Scala, Snowflake, Spark protobuf) and generates the necessary SQL DDL statements
for UDF creation.

Key components:
- ScalaUdf: Reference class for Scala UDFs
- ScalaUDFDef: Definition class for Scala UDF creation
- Type mapping functions for different type systems
- UDF creation and management utilities
"""
import re
from dataclasses import dataclass
from typing import List, Union

import snowflake.snowpark.types as snowpark_type
import snowflake.snowpark_connect.includes.python.pyspark.sql.connect.proto.types_pb2 as types_proto
from snowflake.snowpark_connect.config import get_scala_version
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.jvm_udf_utils import (
    NullHandling,
    Param,
    ReturnType,
    Signature,
    build_jvm_udxf_imports,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.udf_utils import (
    ProcessCommonInlineUserDefinedFunction,
)

# Prefix used for internally generated Scala UDF names to avoid conflicts
CREATE_SCALA_UDF_PREFIX = "__SC_BUILD_IN_CREATE_UDF_SCALA_"


class ScalaUdf:
    """
    Reference class for Scala UDFs, providing similar properties like Python UserDefinedFunction.

    This class serves as a lightweight reference to a Scala UDF that has been created
    in Snowflake, storing the essential metadata needed for function calls.
    """

    def __init__(
        self,
        name: str,
        input_types: List[snowpark_type.DataType],
        return_type: snowpark_type.DataType,
    ) -> None:
        """
        Initialize a Scala UDF reference.

        Args:
            name: The name of the UDF in Snowflake
            input_types: List of input parameter types
            return_type: The return type of the UDF
        """
        self.name = name
        self._input_types = input_types
        self._return_type = return_type


@dataclass(frozen=True)
class ScalaUDFDef:
    """
    Complete definition for creating a Scala UDF in Snowflake.

    Contains all the information needed to generate the CREATE FUNCTION SQL statement
    and the Scala code body for the UDF.

    Attributes:
        name: UDF name
        signature: SQL signature (for Snowflake function definition)
        scala_signature: Scala signature (for Scala code generation)
        imports: List of JAR files to import
        null_handling: Null handling behavior (defaults to CALLED_ON_NULL_INPUT)
    """

    name: str
    signature: Signature
    scala_signature: Signature
    scala_invocation_args: List[str]
    imports: List[str]
    null_handling: NullHandling = NullHandling.CALLED_ON_NULL_INPUT

    # -------------------- DDL Emitter --------------------

    def _gen_body_scala(self) -> str:
        """
        Generate the Scala code body for the UDF.

        Creates a Scala object that loads the serialized function from a binary file
        and provides a run method to execute it.

        Returns:
            String containing the complete Scala code for the UDF body
        """
        # Exclude __schema_json — it's metadata for the wrapper, not an arg to the inner function.
        udf_func_params = [
            p for p in self.scala_signature.params if p.name != "__schema_json"
        ]
        udf_func_input_types = ", ".join("Any" for _ in udf_func_params)
        udf_func_return_type = self.scala_signature.returns.data_type.replace(
            "Array", "Seq"
        )

        joined_wrapper_arg_and_input_types_str = ", ".join(
            f"{p.name}: {p.data_type}" for p in self.scala_signature.params
        )
        wrapper_return_type = "Variant"
        wrapped_args = [
            f"UdfPacketUtils.fromVariant(udfPacket, {arg}, {i}, __schema_json)"
            for i, arg in enumerate(self.scala_invocation_args)
        ]
        invocation_args = ", ".join(wrapped_args)
        invoke_udf_func = f"func({invocation_args})"

        # Always wrap the result in Utils.toVariant() to ensure all Scala UDFs return Variant
        invoke_udf_func = f"Utils.toVariant({invoke_udf_func}, udfPacket)"

        # Null guard: if any non-nullable (primitive) input is null, return null
        # This mirrors Spark's behavior where UDFs short-circuit for null primitive inputs
        null_checks = [
            f"UdfPacketUtils.isNullNonNullable(udfPacket, {arg}, {i})"
            for i, arg in enumerate(self.scala_invocation_args)
        ]
        null_guard = ""
        if null_checks:
            null_guard_condition = " || ".join(null_checks)
            null_guard = f"if ({null_guard_condition}) return null\n    "

        return f"""
import org.apache.spark.sql.connect.common.UdfPacket
import com.snowflake.sas.scala.UdfPacketUtils
import com.snowflake.sas.scala.Utils
import com.snowflake.snowpark_java.types.Variant

object __RecreatedSparkUdf {{
  private lazy val udfPacket: UdfPacket = Utils.deserializeUdfPacket("{self.name}.bin")
  private lazy val func: ({udf_func_input_types}) => {udf_func_return_type} = udfPacket.function.asInstanceOf[({udf_func_input_types}) => {udf_func_return_type}]

  def __wrapperFunc({joined_wrapper_arg_and_input_types_str}): {wrapper_return_type} = {{
    {null_guard}{invoke_udf_func}
  }}
}}
"""

    def to_create_function_sql(self) -> str:
        """
        Generate the complete CREATE FUNCTION SQL statement for the Scala UDF.

        Creates a Snowflake CREATE OR REPLACE TEMPORARY FUNCTION statement with
        all necessary clauses including language, runtime version, packages,
        imports, and the Scala code body.

        Returns:
            Complete SQL DDL statement for creating the UDF
        """
        # self.validate()

        args = ", ".join(f"{p.name} {p.data_type}" for p in self.signature.params)
        ret_type = self.signature.returns.data_type

        def quote_single(s: str) -> str:
            """Helper function to wrap strings in single quotes for SQL."""
            return "'" + s + "'"

        # Handler and imports
        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"

        scala_version = get_scala_version()

        return f"""
CREATE OR REPLACE TEMPORARY FUNCTION {self.name}({args})
RETURNS {ret_type}
LANGUAGE SCALA
{self.null_handling.value}
RUNTIME_VERSION = {scala_version}
PACKAGES = ('com.snowflake:snowpark_{scala_version}:latest')
{imports_sql}
HANDLER = '__RecreatedSparkUdf.__wrapperFunc'
AS
$$
{self._gen_body_scala()}
$$;"""


def create_scala_udf(pciudf: ProcessCommonInlineUserDefinedFunction) -> ScalaUdf:
    """
    Create a Scala UDF in Snowflake from a ProcessCommonInlineUserDefinedFunction object.

    This function handles the complete process of creating a Scala UDF:
    1. Generates a unique function name if not provided
    2. Checks for existing UDFs in the session cache
    3. Creates the necessary imports list
    4. Maps types between different systems (Snowpark, Scala, Snowflake)
    5. Generates and executes the CREATE FUNCTION SQL statement

    If the UDF already exists in the session cache, it will be reused.

    Args:
        pciudf: The ProcessCommonInlineUserDefinedFunction object containing UDF details.

    Returns:
        A ScalaUdf object representing the created or cached Scala UDF.
    """
    from snowflake.snowpark_connect.resources_initializer import (
        ensure_scala_udf_jars_uploaded,
    )

    # Lazily upload Scala UDF jars on-demand when a Scala UDF is actually created.
    # This is thread-safe and will only upload once even if multiple threads call it.
    ensure_scala_udf_jars_uploaded()

    function_name = pciudf._function_name
    # If a function name is not provided, hash the binary file and use the first ten characters as the function name.
    if not function_name:
        import hashlib

        function_name = hashlib.sha256(pciudf._payload).hexdigest()[:10]
    udf_name = CREATE_SCALA_UDF_PREFIX + function_name

    # In case the Scala UDF was created with `spark.udf.register`, the Spark Scala input types (from protobuf) are
    # stored in pciudf.scala_input_types.
    # We cannot rely solely on the inputTypes field from the Scala UDF or the Snowpark input types, since:
    # - spark.udf.register arguments come from the inputTypes field
    # - UDFs created with a data type (like below) do not populate the inputTypes field. This requires the input types
    #   inferred by Snowpark. e.g.: udf((i: Long) => (i + 1).toInt, IntegerType)
    input_types = (
        pciudf._scala_input_types if pciudf._scala_input_types else pciudf._input_types
    )
    scala_return_type = _map_type_to_scala_type(pciudf._original_return_type)
    scala_input_params: List[Param] = []
    sql_input_params: List[Param] = []
    scala_invocation_args: List[str] = []  # arguments passed into the udf function

    session = get_or_create_snowpark_session()
    imports = build_jvm_udxf_imports(
        session,
        pciudf._payload,
        udf_name,
    )

    # If input_types is empty (length 0), it doesn't necessarily mean there are no arguments.
    # We need to inspect the UdfPacket to determine the actual number of arguments.
    num_args = len(input_types or [])
    if num_args == 0 and pciudf._called_from == "register_udf":
        num_args = get_udf_arity(pciudf._payload) or 0

    for i in range(num_args):
        param_name = f"arg{i}"
        scala_input_params.append(Param(param_name, "Variant"))
        sql_input_params.append(Param(param_name, "VARIANT"))
        scala_invocation_args.append(param_name)

    schema_param_name = "__schema_json"
    sql_input_params.append(Param(schema_param_name, "VARCHAR"))
    scala_input_params.append(Param(schema_param_name, "String"))

    sql_return_type = "VARIANT"

    udf_def = ScalaUDFDef(
        name=udf_name,
        signature=Signature(
            params=sql_input_params, returns=ReturnType(sql_return_type)
        ),
        imports=imports,
        scala_signature=Signature(
            params=scala_input_params, returns=ReturnType(scala_return_type)
        ),
        scala_invocation_args=scala_invocation_args,
    )
    create_udf_sql = udf_def.to_create_function_sql()
    logger.info(f"Creating Scala UDF: {create_udf_sql}")
    session.sql(create_udf_sql).collect()
    return ScalaUdf(udf_name, pciudf._input_types, pciudf._return_type)


def get_udf_arity(payload: bytes) -> int | None:
    # We use ISO-8859-1 because it maps every byte (0-255) to a character 1:1.
    # This prevents decoding errors and keeps byte offsets accurate.
    content = payload.decode("ISO-8859-1")

    # Look for 'scala/Function' followed by 1 or 2 digits (Scala supports 0-22)
    # We look for the FIRST occurrence, which is the 'function' field in UdfPacket.
    match = re.search(r"scala/Function(\d{1,2})", content)

    if match:
        return int(match.group(1))

    # Fallback for Spark's Java function wrappers
    java_match = re.search(
        r"org/apache/spark/api/java/function/Function(\d{1,2})", content
    )
    if java_match:
        return int(java_match.group(1))

    return None


def _map_type_to_scala_type(
    t: Union[snowpark_type.DataType, types_proto.DataType],
) -> str:
    """Maps a Snowpark or Spark protobuf type to a Scala type string (for UDF outputs)."""
    if not t:
        return "String"

    is_snowpark_type = isinstance(t, snowpark_type.DataType)
    condition = type(t) if is_snowpark_type else t.WhichOneof("kind")
    match condition:
        case snowpark_type.ArrayType | "array":
            return (
                f"Array[{_map_type_to_scala_type(t.element_type)}]"
                if is_snowpark_type
                else f"Array[{_map_type_to_scala_type(t.array.element_type)}]"
            )
        case snowpark_type.BinaryType | "binary":
            return "Array[Byte]"
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
            return "Int"
        case snowpark_type.LongType | "long":
            return "Long"
        case snowpark_type.MapType | "map":
            key_type = (
                _map_type_to_scala_type(t.key_type)
                if is_snowpark_type
                else _map_type_to_scala_type(t.map.key_type)
            )
            value_type = (
                _map_type_to_scala_type(t.value_type)
                if is_snowpark_type
                else _map_type_to_scala_type(t.map.value_type)
            )
            return f"Map[{key_type}, {value_type}]"
        case snowpark_type.NullType | "null":
            return "String"  # cannot set the return type to Null in Snowpark Scala UDFs
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
