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
from dataclasses import dataclass
from typing import List, Union

import snowflake.snowpark.types as snowpark_type
import snowflake.snowpark_connect.includes.python.pyspark.sql.connect.proto.types_pb2 as types_proto
from snowflake.snowpark_connect.config import get_scala_version
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.type_mapping import map_type_to_snowflake_type
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

# Mapping from Scala primitive types to their boxed Java equivalents
PRIMITIVE_TO_BOXED = {
    "Int": "java.lang.Integer",
    "Long": "java.lang.Long",
    "Double": "java.lang.Double",
    "Float": "java.lang.Float",
    "Boolean": "java.lang.Boolean",
    "Byte": "java.lang.Byte",
    "Short": "java.lang.Short",
    "Char": "java.lang.Character",
}
BOXED_TO_PRIMITIVE = {v: k for k, v in PRIMITIVE_TO_BOXED.items()}
BOXED_PRIMITIVE_TYPES = set(PRIMITIVE_TO_BOXED.values())

_INPUT_VARIANT_TYPE_PAIRS = (
    (snowpark_type.ArrayType, "array"),
    (snowpark_type.MapType, "map"),
    (snowpark_type.ByteType, "byte"),
    (snowpark_type.BinaryType, "binary"),
    (snowpark_type.DecimalType, "decimal"),
)
_INPUT_VARIANT_TYPES = frozenset(
    typ for pair_type in _INPUT_VARIANT_TYPE_PAIRS for typ in pair_type
)


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


def _box_scala_type(scala_type: str) -> str:
    return PRIMITIVE_TO_BOXED.get(scala_type, scala_type)


def _unbox_scala_value(scala_type: str, value: str) -> str:
    primitive_type = BOXED_TO_PRIMITIVE.get(scala_type, scala_type)
    if primitive_type != scala_type:
        return f"{primitive_type}.unbox({value})"
    return value


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
        # Convert Array to Seq for Scala compatibility in function signatures.
        # Replace each "Variant" type with "Any" in the function signature since fromVariant returns Any
        udf_func_input_types = ", ".join(
            "Any"
            if p.data_type == "Variant"
            else p.data_type  # .replace("Array", "Seq")
            for p in self.scala_signature.params
        )
        udf_func_return_type = self.scala_signature.returns.data_type.replace(
            "Array", "Seq"
        )

        # Create the Scala arguments and input types string: "arg0: Type0, arg1: Type1, ...".
        joined_wrapper_arg_and_input_types_str = ", ".join(
            f"{scala_type.name}: { _box_scala_type(scala_type.data_type) if snowflake_type.data_type != 'VARIANT' else 'Variant'}"
            for (scala_type, snowflake_type) in zip(
                self.scala_signature.params, self.signature.params
            )
        )

        # Collect parameter names that are boxed primitives and reproduce this Catalyst rule
        # https://github.com/apache/spark/blob/027a14b3cc058effab7f5a9f7e9d633e8179c5bb/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/analysis/Analyzer.scala#L3270
        boxed_primitive_params = [
            scala_type.name
            for (scala_type, snowflake_type) in zip(
                self.scala_signature.params, self.signature.params
            )
            if snowflake_type.data_type != "VARIANT"
            and _box_scala_type(scala_type.data_type) in BOXED_PRIMITIVE_TYPES
        ]

        null_check = ""
        if boxed_primitive_params:
            null_conditions = " || ".join(
                f"{p} == null" for p in boxed_primitive_params
            )
            null_check = f"if ({null_conditions}) return null\n    "

        # All Scala UDFs return Variant to ensure consistency and avoid type conversion issues.
        wrapper_return_type = "Variant"
        wrapped_args = [
            f"UdfPacketUtils.fromVariant{f'[{scala_param.data_type}]' if scala_param.data_type != 'Variant' else '' }({_unbox_scala_value(scala_param.data_type, arg) if scala_param.data_type != 'Variant' else f'udfPacket, {arg}, {i}'})"
            if param.data_type == "VARIANT"
            else _unbox_scala_value(scala_param.data_type, arg)
            for i, ((arg, param), scala_param) in enumerate(
                zip(
                    zip(self.scala_invocation_args, self.signature.params),
                    self.scala_signature.params,
                )
            )
        ]
        invocation_args = ", ".join(wrapped_args)
        invoke_udf_func = f"func({invocation_args})"

        # Always wrap the result in Utils.toVariant() to ensure all Scala UDFs return Variant
        invoke_udf_func = f"Utils.toVariant({invoke_udf_func}, udfPacket)"

        return f"""
import org.apache.spark.sql.connect.common.UdfPacket
import com.snowflake.sas.scala.UdfPacketUtils._
import com.snowflake.sas.scala.UdfPacketUtils
import com.snowflake.sas.scala.Utils
import com.snowflake.snowpark_java.types.Variant

object __RecreatedSparkUdf {{
  import com.snowflake.sas.scala.FromVariantConverter._

  private lazy val udfPacket: UdfPacket = Utils.deserializeUdfPacket("{self.name}.bin")
  private lazy val func: ({udf_func_input_types}) => {udf_func_return_type} = udfPacket.function.asInstanceOf[({udf_func_input_types}) => {udf_func_return_type}]

  def __wrapperFunc({joined_wrapper_arg_and_input_types_str}): {wrapper_return_type} = {{
    {null_check}{invoke_udf_func}
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
    has_encoders = (
        bool(pciudf._scala_input_types) is not None
        and len(pciudf._scala_input_types) > 0
    )

    scala_return_type = _map_type_to_scala_type(
        pciudf._original_return_type, is_input=False
    )
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
    if (
        input_types is None or len(input_types) == 0
    ) and pciudf._called_from == "register_udf":
        args_scala = _get_input_arg_types_if_udfpacket_input_types_empty(
            session, imports, udf_name
        )
        for i, arg in enumerate(args_scala):
            param_name = "arg" + str(i)
            scala_input_params.append(Param(param_name, arg))
            sql_input_params.append(Param(param_name, "VARIANT"))
            scala_invocation_args.append(param_name)
    elif input_types:
        for i, input_type in enumerate(input_types):
            param_name = "arg" + str(i)
            # Create the Scala arguments and input types string: "arg0: Type0, arg1: Type1, ...".
            scala_input_params.append(
                Param(
                    param_name,
                    _map_type_to_scala_type(
                        input_type, is_input=True, has_encoders=has_encoders
                    ),
                )
            )
            # Create the Snowflake SQL arguments and input types string: "arg0 TYPE0, arg1 TYPE1, ...".
            # For arrays, maps, bytes, decimals, and binary types, use VARIANT type in SQL signature
            sql_type = (
                "VARIANT"
                if _is_sql_type_variant(input_type, has_encoders)
                else map_type_to_snowflake_type(input_type)
            )
            sql_input_params.append(Param(param_name, sql_type))
            # In the case of Map input types, we need to cast the argument to the correct type in Scala.
            scala_invocation_args.append(param_name)

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


def _ensure_input_types_udf_created(session, imports: List[str], udf_name: str) -> str:
    """
    Create a UDF for getting input types with a unique name based on the UDF name.

    This UDF uses reflection to inspect a serialized UdfPacket
    and determine the actual input parameter types.

    Returns:
        The name of the created UDF.
    """

    def quote_single(s: str) -> str:
        return "'" + s + "'"

    scala_version = get_scala_version()
    udf_helper_name = f"__SC_INPUT_ARGS_UDF_{udf_name}"
    imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in imports)})"
    create_udf_sql = f"""
CREATE OR REPLACE TEMPORARY FUNCTION {udf_helper_name}(udf_bin_file VARCHAR)
RETURNS STRING
LANGUAGE SCALA
PACKAGES = ('com.snowflake:snowpark_{scala_version}:latest')
RUNTIME_VERSION = {scala_version}
{imports_sql}
HANDLER = 'com.snowflake.sas.scala.handlers.InputTypesUdf.getInputArgTypesWithReflection';"""
    logger.info(f"Creating UDF for input type inspection: {create_udf_sql}")
    session.sql(create_udf_sql).collect()
    return udf_helper_name


def _get_input_arg_types_if_udfpacket_input_types_empty(
    session, imports: List[str], udf_name: str
) -> list[str]:
    """
    Get the number of input arguments from a UdfPacket by calling a Scala UDF.

    This is used when the input_types list is empty (length 0), which doesn't necessarily
    mean there are no arguments. The UDF uses reflection to inspect the
    serialized function and determine the actual parameters.
    """
    udf_helper_name = _ensure_input_types_udf_created(session, imports, udf_name)
    result = session.sql(f"SELECT {udf_helper_name}('{udf_name}.bin')").collect()
    args = str(result[0][0])
    num_args = len(args.split(", "))
    logger.info(f"UDF has {num_args} input arguments")
    return [arg for arg in args.split(", ") if arg]


def _is_sql_type_variant(
    input_type: Union[snowpark_type.DataType, types_proto.DataType], has_encoders: bool
) -> bool:
    """
    Determine if an input type should be mapped to VARIANT in SQL.

    Returns True if the input type is one of the following:
    - ArrayType: Arrays need special handling as VARIANT
    - MapType: Maps are represented as VARIANT in SQL
    - ByteType: Snowflake's Scala UDF runtime doesn't support java.lang.Byte
    - DecimalType: java.math.BigDecimal vs scala.math.BigDecimal conversion issues
        (if doesn't have encoders we can't cast to VARIANT as it will not be converted to the proper type)
    - BinaryType: Array[byte] is passed as binary, handled as VARIANT

    Args:
        input_type: The type to check (either Snowpark or Spark protobuf type)

    Returns:
        True if the type should be mapped to VARIANT, False otherwise
    """
    unified_type = (
        type(input_type)
        if isinstance(input_type, snowpark_type.DataType)
        else input_type.WhichOneof("kind")
    )
    if not has_encoders and unified_type in (snowpark_type.DecimalType, "decimal"):
        return False

    return unified_type in _INPUT_VARIANT_TYPES


def _map_type_to_scala_type(
    t: Union[snowpark_type.DataType, types_proto.DataType],
    is_input: bool = False,
    has_encoders: bool = False,
) -> str:
    """Maps a Snowpark or Spark protobuf type to a Scala type string.

    Args:
        t: The type to map
        is_input: If True, maps certain types to Variant (for UDF inputs).
                  If False, maps types to their specific Scala equivalents (for UDF outputs).
        has_encoders: If True, the udf has encoders, so we can cast to VARIANT and the proper type would be retrieved (useful only for input types)
    """
    if not t:
        return "String"

    # For input types, check if this should be mapped to VARIANT as it has to be compatible with Snowflake's Scala UDF runtime.
    # (arrays, maps, bytes, decimals, and binary types)
    if is_input and _is_sql_type_variant(t, has_encoders):
        return "Variant"

    is_snowpark_type = isinstance(t, snowpark_type.DataType)
    condition = type(t) if is_snowpark_type else t.WhichOneof("kind")
    match condition:
        case snowpark_type.ArrayType | "array":
            return (
                f"Array[{_map_type_to_scala_type(t.element_type, is_input=False)}]"
                if is_snowpark_type
                else f"Array[{_map_type_to_scala_type(t.array.element_type, is_input=False)}]"
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
