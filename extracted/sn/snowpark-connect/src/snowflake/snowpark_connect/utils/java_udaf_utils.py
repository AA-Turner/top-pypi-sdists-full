#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from dataclasses import dataclass

import snowflake.snowpark.types as snowpark_type
from snowflake.snowpark_connect.config import get_scala_version
from snowflake.snowpark_connect.type_mapping import map_type_to_snowflake_type
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.jvm_udf_utils import (
    NullHandling,
    Param,
    ReturnType,
    Signature,
    build_jvm_udxf_imports,
    gen_pre_narrow_expr,
    is_native_sql_type,
    map_type_to_java_type,
    map_type_to_native_java_type,
    map_type_to_snowflake_native_sql_type,
    needs_epoch_lowering,
    to_json,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.sql_quoting import quote_single
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
    private final static String SCHEMA_JSON = "__schema_json__";
    private static scala.Function2<__reduce_type__, __reduce_type__, __reduce_type__> operation = null;
    private static UdfPacket udfPacket = null;

    private static void loadOperation() throws IOException, ClassNotFoundException {
        if (operation != null) {
            return; // Already loaded
        }

        java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("UTC"));
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
    schema_json: str
    # Snowpark type of the reduce element; when set and is_native_sql_type(), the
    # generated wrapper uses convertInput() instead of fromVariant() for the input.
    reduce_snowpark_type: snowpark_type.DataType | None = None
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
        reduce_dt = self.reduce_snowpark_type
        if is_native_sql_type(reduce_dt):
            # Native path: skip VARIANT round-trip for primitive state types.
            # Snowflake passes all fixed-point SQL types as Java Long and FLOAT as
            # Double, so we pre-narrow to the exact Scala-expected boxed type then
            # use convertInput() for Scala-encoder-level conversion without JSON.
            # convertInput handles LTZ-source LocalDateTime correctly (applies the
            # session timezone); the state is held as Object (erased Scala type).
            native_java = map_type_to_native_java_type(reduce_dt)
            narrow_expr = gen_pre_narrow_expr(reduce_dt, "input")
            mapped_value = (
                f"com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.convertInput("
                f'udfPacket, new Object[]{{{narrow_expr}}}, 0, false, SCHEMA_JSON, java.time.ZoneId.of(System.getProperty("user.timezone")))'
            )
            reduce_type = "Object"
            return_type = native_java
            if needs_epoch_lowering(reduce_dt):
                # Temporal/interval return: state.value is a Scala temporal object
                # (Date, Timestamp, Period, Duration). encodeTemporalToEpoch converts it to
                # the epoch Long that matches the RETURNS INT/BIGINT DDL.
                response_wrapper = "com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.encodeTemporalToEpoch(state.value, udfPacket)"
            elif native_java in ("String", "Boolean"):
                response_wrapper = (
                    f"(state.value instanceof scala.Option"
                    f" ? (((scala.Option<?>) state.value).isEmpty() ? null : ({native_java}) ((scala.Option<?>) state.value).get())"
                    f" : ({native_java}) state.value)"
                )
            elif native_java in ("byte[]", "java.math.BigDecimal"):
                # Not a Number subtype — direct cast without numeric widening.
                response_wrapper = (
                    f"(state.value == null ? null"
                    f" : state.value instanceof scala.Option"
                    f" ? (((scala.Option<?>) state.value).isEmpty() ? null : ({native_java}) ((scala.Option<?>) state.value).get())"
                    f" : ({native_java}) state.value)"
                )
            else:
                method = "longValue" if native_java == "Long" else "doubleValue"
                response_wrapper = (
                    f"(state.value == null ? null"
                    f" : state.value instanceof scala.Option"
                    f" ? (((scala.Option<?>) state.value).isEmpty() ? null : (({native_java}) ((Number) ((scala.Option<?>) state.value).get()).{method}()))"
                    f" : (({native_java}) ((Number) state.value).{method}()))"
                )
        else:
            returns_variant = self.signature.returns.data_type.lower() == "variant"
            return_type = (
                "Variant"
                if returns_variant
                else self.java_signature.params[0].data_type
            )
            response_wrapper = (
                "com.snowflake.sas.scala.Utils$.MODULE$.toVariant(state.value, udfPacket)"
                if returns_variant
                else "state.value"
            )
            is_variant_input = (
                self.java_signature.params[0].data_type.lower() == "variant"
            )
            reduce_type = (
                "Object"
                if is_variant_input
                else self.java_signature.params[0].data_type
            )
            mapped_value = (
                'com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, input, 0, SCHEMA_JSON, java.time.ZoneId.of(System.getProperty("user.timezone")))'
                if is_variant_input
                else "input"
            )

        return (
            UDAF_TEMPLATE.replace("__operation_file__", self.imports[0].split("/")[-1])
            .replace("__accumulator_type__", self.java_signature.params[0].data_type)
            .replace("__value_type__", self.java_signature.params[1].data_type)
            .replace("__mapped_value__", mapped_value)
            .replace("__reduce_type__", reduce_type)
            .replace("__return_type__", return_type)
            .replace("__response_wrapper__", response_wrapper)
            .replace("__schema_json__", self.schema_json)
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

        # Handler and imports
        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"

        return f"""
CREATE OR REPLACE TEMPORARY AGGREGATE FUNCTION {self.name}({args})
RETURNS {ret_type}
LANGUAGE JAVA
{self.null_handling.value}
RUNTIME_VERSION = 17
PACKAGES = ('com.snowflake:snowpark_{get_scala_version()}:latest')
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
    if not function_name:
        # If a function name is not provided, hash the binary file and use the first ten characters as the function name.
        import hashlib

        function_name = hashlib.sha256(pciudf._payload).hexdigest()[:10]
    session_id = get_spark_session_id()
    session_suffix = f"_{session_id.replace('-','_')}" if session_id else ""
    udf_name = CREATE_JAVA_UDAF_PREFIX + function_name + session_suffix

    input_types = pciudf._input_types

    _variant_types = (
        snowpark_type.ArrayType,
        snowpark_type.MapType,
        snowpark_type.VariantType,
        snowpark_type.StructType,
    )

    # For reduce(), all input elements have the same type; only the first is needed.
    # input_types is guaranteed homogeneous by the reduce() caller contract.
    reduce_type_dt = input_types[0] if input_types else None

    java_input_params: list[Param] = []
    sql_input_params: list[Param] = []
    if input_types:  # input_types can be None when no arguments are provided
        for i, input_type in enumerate(input_types):
            param_name = "arg" + str(i)
            if is_native_sql_type(input_type):
                java_type = map_type_to_native_java_type(input_type)
                snowflake_type = map_type_to_snowflake_native_sql_type(input_type)
            elif isinstance(input_type, _variant_types):
                java_type = "Variant"
                snowflake_type = "Variant"
            else:
                java_type = map_type_to_java_type(input_type)
                snowflake_type = map_type_to_snowflake_type(input_type)
            java_input_params.append(Param(param_name, java_type))
            sql_input_params.append(Param(param_name, snowflake_type))

    if is_native_sql_type(pciudf._original_return_type):
        java_return_type = map_type_to_native_java_type(pciudf._original_return_type)
        sql_return_type = map_type_to_snowflake_native_sql_type(
            pciudf._original_return_type
        )
    else:
        java_return_type = map_type_to_java_type(pciudf._original_return_type)
        sql_return_type = map_type_to_snowflake_type(pciudf._original_return_type)
        if isinstance(pciudf._original_return_type, _variant_types):
            sql_return_type = "VARIANT"

    session = get_or_create_snowpark_session()

    imports = build_jvm_udxf_imports(
        session,
        pciudf._payload,
        udf_name,
    )

    schema_json = to_json(input_types if input_types else [])

    udf_def = JavaUDAFDef(
        name=udf_name,
        signature=Signature(
            params=sql_input_params, returns=ReturnType(sql_return_type)
        ),
        imports=imports,
        java_signature=Signature(
            params=java_input_params, returns=ReturnType(java_return_type)
        ),
        schema_json=schema_json,
        reduce_snowpark_type=reduce_type_dt,
    )
    create_udf_sql = udf_def.to_create_function_sql()
    logger.info(
        f"Creating Java UDAF: {udf_name}({','.join([str(param) for param in sql_input_params])})"
    )
    logger.debug(f"Java UDAF with body: {create_udf_sql}")
    session.sql(create_udf_sql).collect()
    return JavaUdaf(udf_name, pciudf._input_types, pciudf._return_type)
