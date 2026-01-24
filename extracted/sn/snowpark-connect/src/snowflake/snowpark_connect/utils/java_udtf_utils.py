#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import hashlib
from dataclasses import dataclass

from pyspark.sql.connect.proto.expressions_pb2 import CommonInlineUserDefinedFunction

from snowflake.snowpark.types import ArrayType, MapType, StructType, VariantType
from snowflake.snowpark_connect.resources_initializer import (
    ensure_scala_udf_jars_uploaded,
)
from snowflake.snowpark_connect.type_mapping import (
    map_type_to_snowflake_type,
    proto_to_snowpark_type,
)
from snowflake.snowpark_connect.utils.jvm_udf_utils import (
    NullHandling,
    Param,
    ReturnType,
    Signature,
    build_jvm_udxf_imports,
    map_type_to_java_type,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

JAVA_UDTF_PREFIX = "__SC_JAVA_UDTF_"

GROUP_MAP_UDTF_TEMPLATE = """
import org.apache.spark.sql.connect.common.UdfPacket;

import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.nio.file.Files;
import java.nio.file.Paths;

import java.util.*;
import java.lang.*;
import java.util.stream.Collectors;
import com.snowflake.snowpark_java.types.*;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

public class OutputRow {
  public Variant __java_udtf_prefix__C1;
  public OutputRow(Variant __java_udtf_prefix__C1) {
    this.__java_udtf_prefix__C1 = __java_udtf_prefix__C1;
  }
}

public class JavaUdtfHandler {
    private final static String OPERATION_FILE = "__operation_file__";
    private static Object operation = null;
    private static boolean hasGroupState = false;
    private static UdfPacket udfPacket = null;

    private __key_type__ currentKey = null;
    private List<__value_type__> accumulatedValues = new ArrayList<>();

  public static Class getOutputClass() { return OutputRow.class; }

    private static void loadOperation() throws IOException, ClassNotFoundException {
        if (operation != null) {
            return; // Already loaded
        }

        udfPacket = com.snowflake.sas.scala.Utils$.MODULE$.deserializeUdfPacket(OPERATION_FILE);
        operation = udfPacket.function();
        hasGroupState = operation instanceof scala.Function3;
    }

  __process_method__

  public Stream<OutputRow> endPartition() throws IOException, ClassNotFoundException {
        if (accumulatedValues.isEmpty()) {
            return Stream.empty();
        }

        __key_conversion__
        __value_iterator_conversion__

        Object scalaResult;
        if (hasGroupState) {
            scala.Function3<Object, scala.collection.Iterator<Object>, org.apache.spark.sql.streaming.GroupState<Object>, Object> func3 =
                (scala.Function3<Object, scala.collection.Iterator<Object>, org.apache.spark.sql.streaming.GroupState<Object>, Object>) operation;
            __group_state_creation__
            scalaResult = func3.apply(scalaKey, scalaIterator, groupState);
        } else {
            scala.Function2<Object, scala.collection.Iterator<Object>, Object> func2 =
                (scala.Function2<Object, scala.collection.Iterator<Object>, Object>) operation;
            scalaResult = func2.apply(scalaKey, scalaIterator);
        }

        scala.collection.Iterator<Object> scalaResultIterator;
        if (scalaResult instanceof scala.collection.Iterator) {
            scalaResultIterator = (scala.collection.Iterator<Object>) scalaResult;
        } else {
            scalaResultIterator = ((scala.collection.Iterable<Object>) scalaResult).iterator();
        }

        java.util.Iterator<Variant> javaResult = new java.util.Iterator<Variant>() {
            public boolean hasNext() { return scalaResultIterator.hasNext(); }
            public Variant next() {
                return com.snowflake.sas.scala.Utils$.MODULE$.toVariant(scalaResultIterator.next(), udfPacket);
            }
        };

        accumulatedValues.clear();

        return StreamSupport.stream(Spliterators.spliteratorUnknownSize(javaResult, Spliterator.ORDERED), false)
                .map(i -> new OutputRow(i));
  }
}
"""

PROCESS_METHOD_NO_INITIAL_STATE = """
  public Stream<OutputRow> process(__key_type__ key, __value_type__ value) throws IOException, ClassNotFoundException {
        loadOperation();
        currentKey = key;
        accumulatedValues.add(value);
        return Stream.empty();
  }
"""

PROCESS_METHOD_WITH_INITIAL_STATE = """
    private Variant initialStateVariant = null;

  public Stream<OutputRow> process(__key_type__ key, __value_type__ value, Variant initialState) throws IOException, ClassNotFoundException {
        loadOperation();
        currentKey = key;
        accumulatedValues.add(value);
        if (initialState != null && initialStateVariant == null) {
            initialStateVariant = initialState;
        }
        return Stream.empty();
  }
"""

GROUP_STATE_CREATION_NO_INITIAL = """
            org.apache.spark.sql.streaming.GroupState<Object> groupState = org.apache.spark.sql.scos.GroupStateUtils$.MODULE$.emptyGroupState();
"""

GROUP_STATE_CREATION_WITH_INITIAL = """
            org.apache.spark.sql.streaming.GroupState<Object> groupState;
            if (initialStateVariant != null) {
                Object scalaInitialState = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$. fromVariantAsOutput(udfPacket, initialStateVariant);
                groupState = org.apache.spark.sql.scos.GroupStateUtils$.MODULE$.groupStateWithInitial(scalaInitialState);
            } else {
                groupState = org.apache.spark.sql.scos.GroupStateUtils$.MODULE$.emptyGroupState();
            }
"""

SCALA_INPUT_VARIANT = """
Object mappedInput = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, input, 0);

java.util.Iterator<Object> javaInput = Arrays.asList(mappedInput).iterator();
scala.collection.Iterator<Object> scalaInput = new scala.collection.AbstractIterator<Object>() {
    public boolean hasNext() { return javaInput.hasNext(); }
    public Object next() { return javaInput.next(); }
};
"""

SCALA_INPUT_SIMPLE_TYPE = """
java.util.Iterator<__iterator_type__> javaInput = Arrays.asList(input).iterator();
scala.collection.Iterator<__iterator_type__> scalaInput = new scala.collection.AbstractIterator<__iterator_type__>() {
    public boolean hasNext() { return javaInput.hasNext(); }
    public __iterator_type__ next() { return javaInput.next(); }
};
"""

UDTF_TEMPLATE = """
import org.apache.spark.sql.connect.common.UdfPacket;

import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.nio.file.Files;
import java.nio.file.Paths;

import java.util.*;
import java.lang.*;
import java.util.stream.Collectors;
import com.snowflake.snowpark_java.types.*;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

public class OutputRow {
  public Variant __java_udtf_prefix__C1;
  public OutputRow(Variant __java_udtf_prefix__C1) {
    this.__java_udtf_prefix__C1 = __java_udtf_prefix__C1;
  }
}

public class JavaUdtfHandler {
    private final static String OPERATION_FILE = "__operation_file__";
    private static scala.Function1<scala.collection.Iterator<__iterator_type__>, scala.collection.Iterator<Object>> operation = null;
    private static UdfPacket udfPacket = null;

  public static Class getOutputClass() { return OutputRow.class; }

    private static void loadOperation() throws IOException, ClassNotFoundException {
        if (operation != null) {
            return; // Already loaded
        }

        udfPacket = com.snowflake.sas.scala.Utils$.MODULE$.deserializeUdfPacket(OPERATION_FILE);
        operation = (scala.Function1<scala.collection.Iterator<__iterator_type__>, scala.collection.Iterator<Object>>) udfPacket.function();
    }

  public Stream<OutputRow> process(__input_type__ input) throws IOException, ClassNotFoundException {
        loadOperation();

        __scala_input__

        scala.collection.Iterator<Object> scalaResult = operation.apply(scalaInput);

        java.util.Iterator<Variant> javaResult = new java.util.Iterator<Variant>() {
            public boolean hasNext() { return scalaResult.hasNext(); }
            public Variant next() {
                return com.snowflake.sas.scala.Utils$.MODULE$.toVariant(scalaResult.next(), udfPacket);
            }
        };

        return StreamSupport.stream(Spliterators.spliteratorUnknownSize(javaResult, Spliterator.ORDERED), false)
                .map(i -> new OutputRow(i));
  }

  public Stream<OutputRow> endPartition() {
    return Stream.empty();
  }
}
"""


@dataclass(frozen=True)
class JavaUDTFDef:
    """
    Complete definition for creating a Java UDTF in Snowflake.

    Contains all the information needed to generate the CREATE FUNCTION SQL statement
    and the Java code body for the UDTF.

    Attributes:
        name: UDTF name
        signature: SQL signature (for Snowflake function definition)
        java_signature: Java signature (for Java code generation)
        imports: List of JAR files to import
        null_handling: Null handling behavior (defaults to RETURNS_NULL_ON_NULL_INPUT)
    """

    name: str
    signature: Signature
    java_signature: Signature
    imports: list[str]
    null_handling: NullHandling = NullHandling.RETURNS_NULL_ON_NULL_INPUT

    def _gen_body_java(self) -> str:
        returns_variant = self.signature.returns.data_type == "VARIANT"
        return_type = (
            "Variant" if returns_variant else self.java_signature.returns.data_type
        )

        is_variant_input = self.java_signature.params[0].data_type.lower() == "variant"

        scala_input_template = (
            SCALA_INPUT_VARIANT if is_variant_input else SCALA_INPUT_SIMPLE_TYPE
        )

        iterator_type = (
            "Object" if is_variant_input else self.java_signature.params[0].data_type
        )

        return (
            UDTF_TEMPLATE.replace("__operation_file__", self.imports[0].split("/")[-1])
            .replace("__scala_input__", scala_input_template)
            .replace("__iterator_type__", iterator_type)
            .replace("__input_type__", self.java_signature.params[0].data_type)
            .replace("__return_type__", return_type)
            .replace("__java_udtf_prefix__", JAVA_UDTF_PREFIX)
        )

    def to_create_function_sql(self) -> str:
        args = ", ".join(
            [f"{param.name} {param.data_type}" for param in self.signature.params]
        )

        def quote_single(s: str) -> str:
            """Helper function to wrap strings in single quotes for SQL."""
            return "'" + s + "'"

        # Handler and imports
        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"

        return f"""
create or replace function {self.name}({args})
returns table ({JAVA_UDTF_PREFIX}C1 VARIANT)
language java
runtime_version = 17
PACKAGES = ('com.snowflake:snowpark:latest')
{imports_sql}
handler='JavaUdtfHandler'
as
$$
{self._gen_body_java()}
$$;"""


def create_java_udtf_for_scala_flatmap_handling(
    udf_proto: CommonInlineUserDefinedFunction,
) -> str:
    ensure_scala_udf_jars_uploaded()

    return_type = proto_to_snowpark_type(udf_proto.scalar_scala_udf.outputType)

    session = get_or_create_snowpark_session()

    return_type_java = map_type_to_java_type(return_type)
    sql_return_type = map_type_to_snowflake_type(return_type)

    java_input_params: list[Param] = []
    sql_input_params: list[Param] = []
    for i, input_type_proto in enumerate(udf_proto.scalar_scala_udf.inputTypes):
        input_type = proto_to_snowpark_type(input_type_proto)

        param_name = "arg" + str(i)

        if isinstance(input_type, (ArrayType, MapType, VariantType)):
            java_type = "Variant"
            snowflake_type = "Variant"
        else:
            java_type = map_type_to_java_type(input_type)
            snowflake_type = map_type_to_snowflake_type(input_type)

        java_input_params.append(Param(param_name, java_type))
        sql_input_params.append(Param(param_name, snowflake_type))

    udtf_name = (
        JAVA_UDTF_PREFIX + hashlib.md5(udf_proto.scalar_scala_udf.payload).hexdigest()
    )

    imports = build_jvm_udxf_imports(
        session,
        udf_proto.scalar_scala_udf.payload,
        udtf_name,
    )

    udtf = JavaUDTFDef(
        name=udtf_name,
        signature=Signature(
            params=sql_input_params, returns=ReturnType(sql_return_type)
        ),
        imports=imports,
        java_signature=Signature(
            params=java_input_params, returns=ReturnType(return_type_java)
        ),
    )

    sql = udtf.to_create_function_sql()
    logger.info(f"Creating Java UDTF for flatmap: {sql}")
    session.sql(sql).collect()

    return udtf_name


@dataclass(frozen=True)
class JavaGroupMapUDTFDef:
    """
    Definition for creating a Java UDTF for Scala group map operations.

    This handles Function2[K, Iterator[V], TraversableOnce[U]] semantics where
    the function takes a key and an iterator of values, returning a sequence of results.
    """

    name: str
    key_type_java: str
    key_type_sql: str
    value_type_java: str
    value_type_sql: str
    imports: list[str]
    is_variant_key: bool
    is_variant_value: bool
    has_initial_state: bool = False

    def _gen_body_java(self) -> str:
        if self.is_variant_key:
            key_conversion = "Object scalaKey = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, currentKey, 0);"
        else:
            key_conversion = "Object scalaKey = currentKey;"

        if self.is_variant_value:
            value_iterator_conversion = """
        java.util.Iterator<Object> javaIterator = accumulatedValues.stream()
            .map(v -> com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, v, 1))
            .iterator();
        scala.collection.Iterator<Object> scalaIterator = new scala.collection.AbstractIterator<Object>() {
            public boolean hasNext() { return javaIterator.hasNext(); }
            public Object next() { return javaIterator.next(); }
        };"""
        else:
            value_iterator_conversion = """
        java.util.Iterator<__value_type__> javaIterator = accumulatedValues.iterator();
        scala.collection.Iterator<Object> scalaIterator = new scala.collection.AbstractIterator<Object>() {
            public boolean hasNext() { return javaIterator.hasNext(); }
            public Object next() { return javaIterator.next(); }
        };""".replace(
                "__value_type__", self.value_type_java
            )

        if self.has_initial_state:
            process_method = PROCESS_METHOD_WITH_INITIAL_STATE
            group_state_creation = GROUP_STATE_CREATION_WITH_INITIAL
        else:
            process_method = PROCESS_METHOD_NO_INITIAL_STATE
            group_state_creation = GROUP_STATE_CREATION_NO_INITIAL

        return (
            GROUP_MAP_UDTF_TEMPLATE.replace(
                "__operation_file__", self.imports[0].split("/")[-1]
            )
            .replace("__process_method__", process_method)
            .replace("__group_state_creation__", group_state_creation)
            .replace("__key_type__", self.key_type_java)
            .replace("__value_type__", self.value_type_java)
            .replace("__key_conversion__", key_conversion)
            .replace("__value_iterator_conversion__", value_iterator_conversion)
            .replace("__java_udtf_prefix__", JAVA_UDTF_PREFIX)
        )

    def to_create_function_sql(self) -> str:
        def quote_single(s: str) -> str:
            return "'" + s + "'"

        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"

        if self.has_initial_state:
            params = f"key {self.key_type_sql}, value {self.value_type_sql}, initial_state VARIANT"
        else:
            params = f"key {self.key_type_sql}, value {self.value_type_sql}"

        return f"""
create or replace function {self.name}({params})
returns table ({JAVA_UDTF_PREFIX}C1 VARIANT)
language java
runtime_version = 17
PACKAGES = ('com.snowflake:snowpark:latest')
{imports_sql}
handler='JavaUdtfHandler'
as
$$
{self._gen_body_java()}
$$;"""


def create_java_udtf_for_scala_group_map_handling(
    udf_proto: CommonInlineUserDefinedFunction,
    has_initial_state: bool = False,
) -> str:
    """
    Create a Java UDTF for Scala group map operations (mapGroups/flatMapGroups).

    The Scala function has signature Function2[K, Iterator[V], TraversableOnce[U]].
    This UDTF accumulates values per partition and applies the function in endPartition.

    Args:
        udf_proto: The UDF protobuf containing the function definition
        has_initial_state: Whether the function uses initial state (mapGroupsWithState)
    """
    ensure_scala_udf_jars_uploaded()

    session = get_or_create_snowpark_session()

    input_types = udf_proto.scalar_scala_udf.inputTypes
    assert len(input_types) == 2, "Group map function should have exactly 2 input types"

    key_type = proto_to_snowpark_type(input_types[0])
    value_type = proto_to_snowpark_type(input_types[1])

    if isinstance(key_type, (ArrayType, MapType, StructType, VariantType)):
        key_type_java = "Variant"
        key_type_sql = "VARIANT"
        is_variant_key = True
    else:
        key_type_java = map_type_to_java_type(key_type)
        key_type_sql = map_type_to_snowflake_type(key_type)
        is_variant_key = False

    if isinstance(value_type, (ArrayType, MapType, StructType, VariantType)):
        value_type_java = "Variant"
        value_type_sql = "VARIANT"
        is_variant_value = True
    else:
        value_type_java = map_type_to_java_type(value_type)
        value_type_sql = map_type_to_snowflake_type(value_type)
        is_variant_value = False

    initial_state_suffix = "_IS" if has_initial_state else ""
    udtf_name = (
        JAVA_UDTF_PREFIX
        + "GM_"
        + hashlib.md5(udf_proto.scalar_scala_udf.payload).hexdigest()
        + initial_state_suffix
    )

    imports = build_jvm_udxf_imports(
        session,
        udf_proto.scalar_scala_udf.payload,
        udtf_name,
    )

    udtf = JavaGroupMapUDTFDef(
        name=udtf_name,
        key_type_java=key_type_java,
        key_type_sql=key_type_sql,
        value_type_java=value_type_java,
        value_type_sql=value_type_sql,
        imports=imports,
        is_variant_key=is_variant_key,
        is_variant_value=is_variant_value,
        has_initial_state=has_initial_state,
    )

    sql = udtf.to_create_function_sql()
    logger.info(f"Creating Java UDTF for group_map: {sql}")
    session.sql(sql).collect()

    return udtf_name
