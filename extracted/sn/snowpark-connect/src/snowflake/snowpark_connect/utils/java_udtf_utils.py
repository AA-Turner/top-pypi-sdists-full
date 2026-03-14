#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import hashlib
from dataclasses import dataclass

from pyspark.sql.connect.proto.expressions_pb2 import CommonInlineUserDefinedFunction

from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    MapType,
    StructType,
    VariantType,
)
from snowflake.snowpark_connect.config import get_scala_version, global_config
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
    to_json,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

JAVA_UDTF_PREFIX = "__SC_JAVA_UDTF_"
VARIANT_COMPATIBLE_TYPES = (ArrayType, MapType, StructType, VariantType)

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
    private final static String SCHEMA_JSON = "__schema_json__";
    private final static String SESSION_TIMEZONE = "__session_timezone__";
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

        java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("UTC"));
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

        List<OutputRow> results = new ArrayList<>();
        while (scalaResultIterator.hasNext()) {
            Variant v = com.snowflake.sas.scala.Utils$.MODULE$.toVariant(scalaResultIterator.next(), udfPacket);
            results.add(new OutputRow(v));
        }

        accumulatedValues.clear();

        return results.stream();
  }
}
"""

CO_GROUP_MAP_UDTF_TEMPLATE = """
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
    private final static String SCHEMA_JSON = "__schema_json__";
    private final static String SESSION_TIMEZONE = "__session_timezone__";
    private static Object operation = null;
    private static UdfPacket udfPacket = null;

    private __key_type__ currentKey = null;
    private List<__value_type__> accumulatedValues1 = new ArrayList<>();
    private List<__value_type__> accumulatedValues2 = new ArrayList<>();

  public static Class getOutputClass() { return OutputRow.class; }

    private static void loadOperation() throws IOException, ClassNotFoundException {
        if (operation != null) {
            return;
        }

        java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("UTC"));
        udfPacket = com.snowflake.sas.scala.Utils$.MODULE$.deserializeUdfPacket(OPERATION_FILE);
        operation = udfPacket.function();
    }

  public Stream<OutputRow> process(__key_type__ key, __value_type__ value, Integer source) throws IOException, ClassNotFoundException {
        loadOperation();
        currentKey = key;
        if (value != null) {
            if (source == 1) {
                accumulatedValues1.add(value);
            } else {
                accumulatedValues2.add(value);
            }
        }
        return Stream.empty();
  }

  public Stream<OutputRow> endPartition() throws IOException, ClassNotFoundException {
        if (accumulatedValues1.isEmpty() && accumulatedValues2.isEmpty()) {
            return Stream.empty();
        }

        __key_conversion__
        __value1_iterator_conversion__
        __value2_iterator_conversion__

        scala.Function3<Object, scala.collection.Iterator<Object>, scala.collection.Iterator<Object>, Object> func3 =
            (scala.Function3<Object, scala.collection.Iterator<Object>, scala.collection.Iterator<Object>, Object>) operation;
        Object scalaResult = func3.apply(scalaKey, scalaIterator1, scalaIterator2);

        scala.collection.Iterator<Object> scalaResultIterator;
        if (scalaResult instanceof scala.collection.Iterator) {
            scalaResultIterator = (scala.collection.Iterator<Object>) scalaResult;
        } else {
            scalaResultIterator = ((scala.collection.Iterable<Object>) scalaResult).iterator();
        }

        List<OutputRow> results = new ArrayList<>();
        while (scalaResultIterator.hasNext()) {
            Variant v = com.snowflake.sas.scala.Utils$.MODULE$.toVariant(scalaResultIterator.next(), udfPacket);
            results.add(new OutputRow(v));
        }

        accumulatedValues1.clear();
        accumulatedValues2.clear();

        return results.stream();
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
                Object scalaInitialState = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariantAsOutput(udfPacket, initialStateVariant, SESSION_TIMEZONE);
                groupState = org.apache.spark.sql.scos.GroupStateUtils$.MODULE$.groupStateWithInitial(scalaInitialState);
            } else {
                groupState = org.apache.spark.sql.scos.GroupStateUtils$.MODULE$.emptyGroupState();
            }
"""

SCALA_INPUT_VARIANT = """
Object mappedInput = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, input, 0, SCHEMA_JSON, SESSION_TIMEZONE);

java.util.Iterator<Object> javaInput = Arrays.asList(mappedInput).iterator();
scala.collection.Iterator<Object> scalaInput = new scala.collection.AbstractIterator<Object>() {
    public boolean hasNext() { return javaInput.hasNext(); }
    public Object next() { return javaInput.next(); }
};
"""

MAP_PARTITIONS_BUILD_ITERATOR_VARIANT = """
        java.util.Iterator<Object> javaIterator = accumulatedInputs.stream()
            .map(v -> com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, v, 0, SCHEMA_JSON, SESSION_TIMEZONE))
            .iterator();
        scala.collection.Iterator<Object> scalaInput = new scala.collection.AbstractIterator<Object>() {
            public boolean hasNext() { return javaIterator.hasNext(); }
            public Object next() { return javaIterator.next(); }
        };
"""

MAP_PARTITIONS_BUILD_ITERATOR_SIMPLE = """
        java.util.Iterator<__iterator_type__> javaIterator = accumulatedInputs.iterator();
        scala.collection.Iterator<__iterator_type__> scalaInput = new scala.collection.AbstractIterator<__iterator_type__>() {
            public boolean hasNext() { return javaIterator.hasNext(); }
            public __iterator_type__ next() { return javaIterator.next(); }
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
    private final static String SCHEMA_JSON = "__schema_json__";
    private final static String SESSION_TIMEZONE = "__session_timezone__";
    private static scala.Function1<scala.collection.Iterator<__iterator_type__>, scala.collection.Iterator<Object>> operation = null;
    private static UdfPacket udfPacket = null;
__instance_fields__
  public static Class getOutputClass() { return OutputRow.class; }

    private static void loadOperation() throws IOException, ClassNotFoundException {
        if (operation != null) {
            return;
        }
        java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("UTC"));
        udfPacket = com.snowflake.sas.scala.Utils$.MODULE$.deserializeUdfPacket(OPERATION_FILE);
        operation = (scala.Function1<scala.collection.Iterator<__iterator_type__>, scala.collection.Iterator<Object>>) udfPacket.function();
    }

__process_method__

__end_partition_method__
}
"""

FLATMAP_PROCESS_METHOD = """
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
"""

FLATMAP_END_PARTITION_METHOD = """
  public Stream<OutputRow> endPartition() {
    return Stream.empty();
  }
"""

MAP_PARTITIONS_INSTANCE_FIELDS = """
    private List<__input_type__> accumulatedInputs = new ArrayList<>();
"""

MAP_PARTITIONS_PROCESS_METHOD = """
  public Stream<OutputRow> process(__input_type__ input) throws IOException, ClassNotFoundException {
        loadOperation();
        accumulatedInputs.add(input);
        return Stream.empty();
  }
"""

MAP_PARTITIONS_END_PARTITION_METHOD = """
  public Stream<OutputRow> endPartition() throws IOException, ClassNotFoundException {
        if (accumulatedInputs.isEmpty()) {
            return Stream.empty();
        }

        loadOperation();

        __build_iterator__

        scala.collection.Iterator<Object> scalaResult = operation.apply(scalaInput);

        List<OutputRow> results = new ArrayList<>();
        while (scalaResult.hasNext()) {
            Variant v = com.snowflake.sas.scala.Utils$.MODULE$.toVariant(scalaResult.next(), udfPacket);
            results.add(new OutputRow(v));
        }

        accumulatedInputs.clear();

        return results.stream();
  }
"""


@dataclass(frozen=True)
class JavaUDTFDef:
    """
    Definition for creating a Java UDTF in Snowflake for both flatMap (per-row)
    and mapPartitions (batch) semantics.

    When batch_mode=False (flatMap): each row is wrapped in a 1-element iterator
    and the function is applied per row in process().

    When batch_mode=True (mapPartitions): rows are accumulated in process() and
    the function is applied to the full iterator in endPartition().
    """

    name: str
    signature: Signature
    java_signature: Signature
    imports: list[str]
    schema_json: str
    batch_mode: bool = False
    null_handling: NullHandling = NullHandling.RETURNS_NULL_ON_NULL_INPUT

    def _gen_body_java(self) -> str:
        is_variant_input = self.java_signature.params[0].data_type.lower() == "variant"
        iterator_type = (
            "Object" if is_variant_input else self.java_signature.params[0].data_type
        )

        if self.batch_mode:
            instance_fields = MAP_PARTITIONS_INSTANCE_FIELDS
            build_iterator = (
                MAP_PARTITIONS_BUILD_ITERATOR_VARIANT
                if is_variant_input
                else MAP_PARTITIONS_BUILD_ITERATOR_SIMPLE
            )
            process_method = MAP_PARTITIONS_PROCESS_METHOD
            end_partition_method = MAP_PARTITIONS_END_PARTITION_METHOD.replace(
                "__build_iterator__", build_iterator
            )
        else:
            instance_fields = ""
            scala_input = (
                SCALA_INPUT_VARIANT if is_variant_input else SCALA_INPUT_SIMPLE_TYPE
            )
            process_method = FLATMAP_PROCESS_METHOD.replace(
                "__scala_input__", scala_input
            )
            end_partition_method = FLATMAP_END_PARTITION_METHOD

        return (
            UDTF_TEMPLATE.replace("__operation_file__", self.imports[0].split("/")[-1])
            .replace("__instance_fields__", instance_fields)
            .replace("__process_method__", process_method)
            .replace("__end_partition_method__", end_partition_method)
            .replace("__iterator_type__", iterator_type)
            .replace("__input_type__", self.java_signature.params[0].data_type)
            .replace("__java_udtf_prefix__", JAVA_UDTF_PREFIX)
            .replace("__schema_json__", self.schema_json)
            .replace(
                "__session_timezone__",
                global_config.spark_sql_session_timeZone or "UTC",
            )
        )

    def to_create_function_sql(self) -> str:
        args = ", ".join(
            [f"{param.name} {param.data_type}" for param in self.signature.params]
        )

        def quote_single(s: str) -> str:
            return "'" + s + "'"

        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"

        return f"""
create or replace function {self.name}({args})
returns table ({JAVA_UDTF_PREFIX}C1 VARIANT)
language java
runtime_version = 17
PACKAGES = ('com.snowflake:snowpark_{get_scala_version()}:latest')
{imports_sql}
handler='JavaUdtfHandler'
as
$$
{self._gen_body_java()}
$$;"""


def create_java_udtf(
    udf_proto: CommonInlineUserDefinedFunction,
    arg_types: list[DataType] | None,
    batch_mode: bool,
) -> str:
    ensure_scala_udf_jars_uploaded()

    session = get_or_create_snowpark_session()

    java_input_params: list[Param] = []
    sql_input_params: list[Param] = []
    for i, _ in enumerate(udf_proto.scalar_scala_udf.inputTypes):
        param_name = "arg" + str(i)
        java_input_params.append(Param(param_name, "Variant"))
        sql_input_params.append(Param(param_name, "Variant"))

    return_type = proto_to_snowpark_type(udf_proto.scalar_scala_udf.outputType)
    return_type_java = map_type_to_java_type(return_type)
    sql_return_type = map_type_to_snowflake_type(return_type)

    name_prefix = "MP_" if batch_mode else ""
    udtf_name = (
        JAVA_UDTF_PREFIX
        + name_prefix
        + hashlib.md5(udf_proto.scalar_scala_udf.payload).hexdigest()
    )

    imports = build_jvm_udxf_imports(
        session,
        udf_proto.scalar_scala_udf.payload,
        udtf_name,
    )

    schema_json = to_json(arg_types)

    udtf = JavaUDTFDef(
        name=udtf_name,
        signature=Signature(
            params=sql_input_params, returns=ReturnType(sql_return_type)
        ),
        imports=imports,
        java_signature=Signature(
            params=java_input_params, returns=ReturnType(return_type_java)
        ),
        schema_json=schema_json,
        batch_mode=batch_mode,
    )

    mode_label = "map_partitions" if batch_mode else "flatmap"
    sql = udtf.to_create_function_sql()
    logger.info(
        f"Creating Java UDAF {mode_label}: {udtf_name}({','.join([str(param) for param in sql_input_params])})"
    )
    logger.debug(f"Java UDAF with body {mode_label}: {sql}")
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
    schema_json: str = "[]"
    has_initial_state: bool = False

    def _gen_body_java(self) -> str:
        if self.is_variant_key:
            key_conversion = "Object scalaKey = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, currentKey, 0, SCHEMA_JSON, SESSION_TIMEZONE);"
        else:
            key_conversion = "Object scalaKey = currentKey;"

        if self.is_variant_value:
            value_iterator_conversion = """
        java.util.Iterator<Object> javaIterator = accumulatedValues.stream()
            .map(v -> com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, v, 1, SCHEMA_JSON, SESSION_TIMEZONE))
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
            .replace("__schema_json__", self.schema_json)
            .replace(
                "__session_timezone__",
                global_config.spark_sql_session_timeZone or "UTC",
            )
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
PACKAGES = ('com.snowflake:snowpark_{get_scala_version()}:latest')
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

    if isinstance(key_type, VARIANT_COMPATIBLE_TYPES):
        key_type_java = "Variant"
        key_type_sql = "VARIANT"
        is_variant_key = True
    else:
        key_type_java = map_type_to_java_type(key_type)
        key_type_sql = map_type_to_snowflake_type(key_type)
        is_variant_key = False

    if isinstance(value_type, VARIANT_COMPATIBLE_TYPES):
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

    schema_json = to_json([key_type, value_type])

    udtf = JavaGroupMapUDTFDef(
        name=udtf_name,
        key_type_java=key_type_java,
        key_type_sql=key_type_sql,
        value_type_java=value_type_java,
        value_type_sql=value_type_sql,
        imports=imports,
        is_variant_key=is_variant_key,
        is_variant_value=is_variant_value,
        schema_json=schema_json,
        has_initial_state=has_initial_state,
    )

    sql = udtf.to_create_function_sql()
    logger.info(f"Creating Java UDTF group_map: {udtf_name}")
    logger.debug(f"Java UDTF with body group_map: {sql}")
    session.sql(sql).collect()

    return udtf_name


@dataclass(frozen=True)
class JavaCoGroupMapUDTFDef:
    """
    Definition for creating a Java UDTF for Scala co_group_map operations.

    This handles Function3[K, Iterator[V1], Iterator[V2], TraversableOnce[U]] semantics where
    the function takes a key and two iterators of values (one from each dataset),
    returning a sequence of results.

    The UDTF receives rows with a source marker (1 or 2) to indicate which dataset
    each value came from. Values are accumulated separately and then passed to the
    Scala function as two iterators.
    """

    name: str
    key_type_java: str
    key_type_sql: str
    value_type_java: str
    value_type_sql: str
    imports: list[str]
    is_variant_key: bool
    is_variant_value: bool
    schema_json: str = "[]"

    def _gen_body_java(self) -> str:
        if self.is_variant_key:
            key_conversion = "Object scalaKey = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, currentKey, 0, SCHEMA_JSON, SESSION_TIMEZONE);"
        else:
            key_conversion = "Object scalaKey = currentKey;"

        if self.is_variant_value:
            value1_iterator_conversion = """
        java.util.Iterator<Object> javaIterator1 = accumulatedValues1.stream()
            .map(v -> com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, v, 1, SCHEMA_JSON, SESSION_TIMEZONE))
            .iterator();
        scala.collection.Iterator<Object> scalaIterator1 = new scala.collection.AbstractIterator<Object>() {
            public boolean hasNext() { return javaIterator1.hasNext(); }
            public Object next() { return javaIterator1.next(); }
        };"""
            value2_iterator_conversion = """
        java.util.Iterator<Object> javaIterator2 = accumulatedValues2.stream()
            .map(v -> com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, v, 2, SCHEMA_JSON, SESSION_TIMEZONE))
            .iterator();
        scala.collection.Iterator<Object> scalaIterator2 = new scala.collection.AbstractIterator<Object>() {
            public boolean hasNext() { return javaIterator2.hasNext(); }
            public Object next() { return javaIterator2.next(); }
        };"""
        else:
            value1_iterator_conversion = """
        java.util.Iterator<__value_type__> javaIterator1 = accumulatedValues1.iterator();
        scala.collection.Iterator<Object> scalaIterator1 = new scala.collection.AbstractIterator<Object>() {
            public boolean hasNext() { return javaIterator1.hasNext(); }
            public Object next() { return javaIterator1.next(); }
        };""".replace(
                "__value_type__", self.value_type_java
            )
            value2_iterator_conversion = """
        java.util.Iterator<__value_type__> javaIterator2 = accumulatedValues2.iterator();
        scala.collection.Iterator<Object> scalaIterator2 = new scala.collection.AbstractIterator<Object>() {
            public boolean hasNext() { return javaIterator2.hasNext(); }
            public Object next() { return javaIterator2.next(); }
        };""".replace(
                "__value_type__", self.value_type_java
            )

        return (
            CO_GROUP_MAP_UDTF_TEMPLATE.replace(
                "__operation_file__", self.imports[0].split("/")[-1]
            )
            .replace("__key_type__", self.key_type_java)
            .replace("__value_type__", self.value_type_java)
            .replace("__key_conversion__", key_conversion)
            .replace("__value1_iterator_conversion__", value1_iterator_conversion)
            .replace("__value2_iterator_conversion__", value2_iterator_conversion)
            .replace("__java_udtf_prefix__", JAVA_UDTF_PREFIX)
            .replace("__schema_json__", self.schema_json)
            .replace(
                "__session_timezone__",
                global_config.spark_sql_session_timeZone or "UTC",
            )
        )

    def to_create_function_sql(self) -> str:
        def quote_single(s: str) -> str:
            return "'" + s + "'"

        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"

        params = f"key {self.key_type_sql}, value {self.value_type_sql}, source INTEGER"

        return f"""
create or replace function {self.name}({params})
returns table ({JAVA_UDTF_PREFIX}C1 VARIANT)
language java
runtime_version = 17
PACKAGES = ('com.snowflake:snowpark_{get_scala_version()}:latest')
{imports_sql}
handler='JavaUdtfHandler'
as
$$
{self._gen_body_java()}
$$;"""


def create_java_udtf_for_scala_co_group_map_handling(
    udf_proto: CommonInlineUserDefinedFunction,
) -> str:
    """
    Create a Java UDTF for Scala co_group_map operations (cogroup).

    The Scala function has signature Function3[K, Iterator[V1], Iterator[V2], TraversableOnce[U]].
    This UDTF uses a UNION ALL approach where rows from both datasets are combined with a source
    marker. The UDTF accumulates values per partition and separates them by source in endPartition.

    Args:
        udf_proto: The UDF protobuf containing the function definition
    """
    ensure_scala_udf_jars_uploaded()

    session = get_or_create_snowpark_session()

    input_types = udf_proto.scalar_scala_udf.inputTypes
    assert (
        len(input_types) == 3
    ), "Co-group map function should have exactly 3 input types"

    key_type = proto_to_snowpark_type(input_types[0])
    value1_type = proto_to_snowpark_type(input_types[1])
    value2_type = proto_to_snowpark_type(input_types[2])

    if isinstance(key_type, VARIANT_COMPATIBLE_TYPES):
        key_type_java = "Variant"
        key_type_sql = "VARIANT"
        is_variant_key = True
    else:
        key_type_java = map_type_to_java_type(key_type)
        key_type_sql = map_type_to_snowflake_type(key_type)
        is_variant_key = False

    is_variant_value1 = isinstance(value1_type, VARIANT_COMPATIBLE_TYPES)
    is_variant_value2 = isinstance(value2_type, VARIANT_COMPATIBLE_TYPES)
    is_variant_value = is_variant_value1 or is_variant_value2

    if is_variant_value:
        value_type_java = "Variant"
        value_type_sql = "VARIANT"
    else:
        value_type_java = map_type_to_java_type(value1_type)
        value_type_sql = map_type_to_snowflake_type(value1_type)

    udtf_name = (
        JAVA_UDTF_PREFIX
        + "CGM_"
        + hashlib.md5(udf_proto.scalar_scala_udf.payload).hexdigest()
    )

    imports = build_jvm_udxf_imports(
        session,
        udf_proto.scalar_scala_udf.payload,
        udtf_name,
    )

    schema_json = to_json([key_type, value1_type, value2_type])

    udtf = JavaCoGroupMapUDTFDef(
        name=udtf_name,
        key_type_java=key_type_java,
        key_type_sql=key_type_sql,
        value_type_java=value_type_java,
        value_type_sql=value_type_sql,
        imports=imports,
        is_variant_key=is_variant_key,
        is_variant_value=is_variant_value,
        schema_json=schema_json,
    )

    sql = udtf.to_create_function_sql()
    logger.info(f"Creating Java UDTF co_group_map: {udtf_name}")
    logger.debug(f"Java UDTF with body co_group_map: {sql}")
    session.sql(sql).collect()

    return udtf_name
