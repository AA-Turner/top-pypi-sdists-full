#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from dataclasses import dataclass

import snowflake.snowpark.types as snowpark_type
from snowflake.snowpark_connect.type_mapping import map_type_to_snowflake_type
from snowflake.snowpark_connect.utils.jvm_udf_utils import (
    NullHandling,
    Param,
    ReturnType,
    Signature,
    build_jvm_udxf_imports,
    map_type_to_java_type,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.udf_utils import (
    ProcessCommonInlineUserDefinedFunction,
)

# Prefix used for internally generated Java UDAF names to avoid conflicts
CREATE_JAVA_UDAF_PREFIX = "__SC_JAVA_UDAF_"


UDAF_TEMPLATE = """
import org.apache.spark.sql.connect.common.UdfPacket;

import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.nio.file.Files;
import java.nio.file.Paths;

// Import types required for mapping
import java.util.*;
import java.util.stream.Collectors;
import com.snowflake.snowpark_java.types.*;

public class JavaUDAF {
    private final static String OPERATION_FILE = "__operation_file__";
    private static scala.Function2<__reduce_type__, __reduce_type__, __reduce_type__> operation = null;
    private static UdfPacket udfPacket = null;

    private static void loadOperation() throws IOException, ClassNotFoundException {
        if (operation != null) {
            return; // Already loaded
        }

        udfPacket = com.snowflake.sas.scala.Utils$.MODULE$.deserializeUdfPacket(OPERATION_FILE);
        operation = (scala.Function2<__reduce_type__, __reduce_type__, __reduce_type__>) udfPacket.function();
    }

    public static class State implements Serializable {
        public __reduce_type__ value = null;
        public boolean initialized = false;
    }

    public static State initialize()  throws IOException, ClassNotFoundException {
        loadOperation();
        return new State();
    }

    public static State accumulate(State state, __accumulator_type__ accumulator, __value_type__ input) {
        // TODO: Add conversion between value_type we get in input and the value that we are using in the operation
        if (input == null) {
            return state;
        }

        if (!state.initialized) {
            state.value = __mapped_value__;
            state.initialized = true;
        } else {
            state.value = operation.apply(state.value, __mapped_value__);
        }
        return state;
    }

    public static State merge(State s1, State s2) {
        if (!s2.initialized) {
            return s1;
        }
        if (!s1.initialized) {
            return s2;
        }

        s1.value = operation.apply(s1.value, s2.value);
        return s1;
    }

    public static __return_type__ finish(State state) {
        return state.initialized ? __response_wrapper__ : null;
    }
}"""


@dataclass(frozen=True)
class JavaUDAFDef:
    """
    Complete definition for creating a Java UDAF in Snowflake.

    Contains all the information needed to generate the CREATE FUNCTION SQL statement
    and the Java code body for the UDAF.

    Attributes:
        name: UDAF name
        signature: SQL signature (for Snowflake function definition)
        java_signature: Java signature (for Java code generation)
        java_invocation_args: List of transformed arguments passed to the Java UDAF invocation, with type casting applied for Map types and other necessary conversions.
        imports: List of JAR files to import
        null_handling: Null handling behavior (defaults to RETURNS_NULL_ON_NULL_INPUT)
    """

    name: str
    signature: Signature
    java_signature: Signature
    imports: list[str]
    null_handling: NullHandling = NullHandling.RETURNS_NULL_ON_NULL_INPUT

    # -------------------- DDL Emitter --------------------

    def _gen_body_java(self) -> str:
        """
        Generate the Java code body for the UDAF.

        Creates a Java object that loads the serialized function from a binary file
        and provides a run method to execute it.

        Returns:
            String containing the complete Java code for the UDAF body
        """
        returns_variant = self.signature.returns.data_type.lower() == "variant"
        return_type = (
            "Variant" if returns_variant else self.java_signature.params[0].data_type
        )
        response_wrapper = (
            "com.snowflake.sas.scala.Utils$.MODULE$.toVariant(state.value, udfPacket)"
            if returns_variant
            else "state.value"
        )

        is_variant_input = self.java_signature.params[0].data_type.lower() == "variant"
        reduce_type = (
            "Object" if is_variant_input else self.java_signature.params[0].data_type
        )
        return (
            UDAF_TEMPLATE.replace("__operation_file__", self.imports[0].split("/")[-1])
            .replace("__accumulator_type__", self.java_signature.params[0].data_type)
            .replace("__value_type__", self.java_signature.params[1].data_type)
            .replace(
                "__mapped_value__",
                "com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, input, 0)"
                if is_variant_input
                else "input",
            )
            .replace("__reduce_type__", reduce_type)
            .replace("__return_type__", return_type)
            .replace("__response_wrapper__", response_wrapper)
        )

    def to_create_function_sql(self) -> str:
        """
        Generate the complete CREATE FUNCTION SQL statement for the Java UDAF.

        Creates a Snowflake CREATE OR REPLACE TEMPORARY AGGREGATE FUNCTION statement with
        all necessary clauses including language, runtime version, packages,
        imports, and the Java code body.

        Returns:
            Complete SQL DDL statement for creating the UDAF
        """

        args = ", ".join(
            [f"{param.name} {param.data_type}" for param in self.signature.params]
        )
        ret_type = self.signature.returns.data_type

        def quote_single(s: str) -> str:
            """Helper function to wrap strings in single quotes for SQL."""
            return "'" + s + "'"

        # Handler and imports
        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"

        return f"""
CREATE OR REPLACE TEMPORARY AGGREGATE FUNCTION {self.name}({args})
RETURNS {ret_type}
LANGUAGE JAVA
{self.null_handling.value}
RUNTIME_VERSION = 17
PACKAGES = ('com.snowflake:snowpark:latest')
{imports_sql}
HANDLER = 'JavaUDAF'
AS
$$
{self._gen_body_java()}
$$;"""


class JavaUdaf:
    """
    Reference class for Java UDAFs, providing similar properties like Python UserDefinedFunction.

    This class serves as a lightweight reference to a Java UDAF that has been created
    in Snowflake, storing the essential metadata needed for function calls.
    """

    def __init__(
        self,
        name: str,
        input_types: list[snowpark_type.DataType],
        return_type: snowpark_type.DataType,
    ) -> None:
        """
        Initialize a Java UDAF reference.

        Args:
            name: The name of the UDAF in Snowflake
            input_types: List of input parameter types
            return_type: The return type of the UDAF
        """
        self.name = name
        self._input_types = input_types
        self._return_type = return_type


def create_java_udaf_for_reduce_scala_function(
    pciudf: ProcessCommonInlineUserDefinedFunction,
) -> JavaUdaf:
    """
    Create a Java UDAF in Snowflake from a ProcessCommonInlineUserDefinedFunction object.

    This function handles the complete process of creating a Java UDAF:
    1. Generates a unique function name if not provided
    2. Creates the necessary imports list
    3. Maps types between different systems (Snowpark, Java, Snowflake)
    4. Generates and executes the CREATE FUNCTION SQL statement

    Args:
        pciudf: The ProcessCommonInlineUserDefinedFunction object containing UDF details.

    Returns:
        A JavaUdaf object representing the Java UDAF.
    """
    from snowflake.snowpark_connect.resources_initializer import (
        ensure_scala_udf_jars_uploaded,
    )

    # Make sure Scala UDF jars are uploaded before creating Java UDAFs since we depend on them.
    ensure_scala_udf_jars_uploaded()

    from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session

    function_name = pciudf._function_name
    # If a function name is not provided, hash the binary file and use the first ten characters as the function name.
    if not function_name:
        import hashlib

        function_name = hashlib.sha256(pciudf._payload).hexdigest()[:10]
    udf_name = CREATE_JAVA_UDAF_PREFIX + function_name

    input_types = pciudf._input_types

    java_input_params: list[Param] = []
    sql_input_params: list[Param] = []
    if input_types:  # input_types can be None when no arguments are provided
        for i, input_type in enumerate(input_types):
            param_name = "arg" + str(i)
            if isinstance(
                input_type,
                (
                    snowpark_type.ArrayType,
                    snowpark_type.MapType,
                    snowpark_type.VariantType,
                ),
            ):
                java_type = "Variant"
                snowflake_type = "Variant"
            else:
                java_type = map_type_to_java_type(input_type)
                snowflake_type = map_type_to_snowflake_type(input_type)
            # Create the Java arguments and input types string: "arg0: Type0, arg1: Type1, ...".
            java_input_params.append(Param(param_name, java_type))
            # Create the Snowflake SQL arguments and input types string: "arg0 TYPE0, arg1 TYPE1, ...".
            sql_input_params.append(Param(param_name, snowflake_type))

    java_return_type = map_type_to_java_type(pciudf._original_return_type)
    # If the SQL return type is a MAP or STRUCT, change this to VARIANT because of issues with Java UDAFs.
    sql_return_type = map_type_to_snowflake_type(pciudf._original_return_type)
    session = get_or_create_snowpark_session()

    imports = build_jvm_udxf_imports(
        session,
        pciudf._payload,
        udf_name,
    )
    sql_return_type = (
        "VARIANT"
        if (
            sql_return_type.startswith("MAP")
            or sql_return_type.startswith("OBJECT")
            or sql_return_type.startswith("ARRAY")
        )
        else sql_return_type
    )

    udf_def = JavaUDAFDef(
        name=udf_name,
        signature=Signature(
            params=sql_input_params, returns=ReturnType(sql_return_type)
        ),
        imports=imports,
        java_signature=Signature(
            params=java_input_params, returns=ReturnType(java_return_type)
        ),
    )
    create_udf_sql = udf_def.to_create_function_sql()
    logger.info(f"Creating Java UDAF: {create_udf_sql}")
    session.sql(create_udf_sql).collect()
    return JavaUdaf(udf_name, pciudf._input_types, pciudf._return_type)
