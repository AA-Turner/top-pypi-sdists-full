#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""
Scala UDF utilities for Snowpark Connect.

This module provides utilities for creating and managing Scala User-Defined Functions (UDFs)
in Snowflake through Snowpark Connect. Scala UDFs are wrapped in Java UDFs that call into
the Scala code via the SAS Scala helper library, following the same pattern as Java UDTFs.

Key components:
- ScalaUdf: Reference class for Scala UDFs
- JavaScalarUDFDef: Definition class for Java-wrapped Scala UDF creation
- UDF creation and management utilities
"""
import re
from dataclasses import dataclass
from typing import List

import snowflake.snowpark.types as snowpark_type
from snowflake.snowpark_connect.config import get_scala_version, global_config
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
        self.name = name
        self._input_types = input_types
        self._return_type = return_type


@dataclass(frozen=True)
class JavaScalarUDFDef:
    """
    Definition for creating a Java UDF in Snowflake that wraps a Scala function.

    The Java wrapper deserializes the Scala closure from a binary file,
    converts Variant inputs to Scala types, invokes the function, and
    converts the result back to Variant.
    """

    name: str
    signature: Signature
    imports: list[str]
    num_args: int
    null_handling: NullHandling = NullHandling.CALLED_ON_NULL_INPUT

    def _gen_body_java(self) -> str:
        operation_file = self.imports[0].split("/")[-1]

        handler_params_list = [f"Variant arg{i}" for i in range(self.num_args)]
        handler_params_list.append("String __schema_json")
        handler_params = ", ".join(handler_params_list)

        lines = []

        if self.num_args > 0:
            null_checks = [
                f"com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.isNullNonNullable(udfPacket, arg{i}, {i})"
                for i in range(self.num_args)
            ]
            lines.append(f"        if ({' || '.join(null_checks)}) return null;")

        for i in range(self.num_args):
            lines.append(
                f"        var in{i} = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, arg{i}, {i}, __schema_json, SESSION_TIMEZONE);"
            )

        object_types = ", ".join(["Object"] * (self.num_args + 1))
        func_type = f"scala.Function{self.num_args}<{object_types}>"
        func_args = ", ".join(f"in{i}" for i in range(self.num_args))

        lines.append(f"        var typedFunc = ({func_type}) func;")
        lines.append(f"        var result = typedFunc.apply({func_args});")
        lines.append(
            "        return com.snowflake.sas.scala.Utils$.MODULE$.toVariant(result, udfPacket);"
        )

        body = "\n".join(lines)

        return f"""
import org.apache.spark.sql.connect.common.UdfPacket;
import com.snowflake.snowpark_java.types.Variant;

public class RecreatedSparkJavaUdf {{
    private static final String OPERATION_FILE = "{operation_file}";
    private static final String SESSION_TIMEZONE = "{global_config.spark_sql_session_timeZone or 'UTC'}";
    private final UdfPacket udfPacket;
    private final Object func;

    public RecreatedSparkJavaUdf() {{
        java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("UTC"));
        this.udfPacket = com.snowflake.sas.scala.Utils$.MODULE$.deserializeUdfPacket(OPERATION_FILE);
        this.func = udfPacket.function();
    }}

    public Variant handler({handler_params}) {{
{body}
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

        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"

        return f"""
CREATE OR REPLACE TEMPORARY FUNCTION {self.name}({args})
RETURNS {ret_type}
LANGUAGE JAVA
{self.null_handling.value}
RUNTIME_VERSION = 17
PACKAGES = ('com.snowflake:snowpark_{get_scala_version()}:latest')
{imports_sql}
HANDLER = 'RecreatedSparkJavaUdf.handler'
AS
$$
{self._gen_body_java()}
$$;"""


def create_scala_udf(pciudf: ProcessCommonInlineUserDefinedFunction) -> ScalaUdf:
    """
    Create a Java UDF in Snowflake that wraps a Scala function
    from a ProcessCommonInlineUserDefinedFunction object.
    """
    from snowflake.snowpark_connect.resources_initializer import (
        ensure_scala_udf_jars_uploaded,
    )

    # Lazily upload Scala UDF jars on-demand when a UDF is actually created.
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
    sql_input_params: list[Param] = []

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
        sql_input_params.append(Param(f"arg{i}", "VARIANT"))

    sql_input_params.append(Param("__schema_json", "VARCHAR"))

    udf_def = JavaScalarUDFDef(
        name=udf_name,
        signature=Signature(params=sql_input_params, returns=ReturnType("VARIANT")),
        imports=imports,
        num_args=num_args,
    )
    create_udf_sql = udf_def.to_create_function_sql()
    logger.info(
        f"Creating Java UDF for Scala function: {udf_name}({','.join([str(param) for param in sql_input_params])})"
    )
    logger.debug(f"Java UDF with body: {create_udf_sql}")
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
