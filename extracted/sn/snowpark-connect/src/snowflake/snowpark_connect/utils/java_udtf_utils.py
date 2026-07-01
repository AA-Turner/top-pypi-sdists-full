#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import hashlib
from dataclasses import dataclass
from typing import Optional

from pyspark.sql.connect.proto.expressions_pb2 import CommonInlineUserDefinedFunction

import snowflake.snowpark.types as snowpark_type
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    MapType,
    StructType,
    VariantType,
)
from snowflake.snowpark_connect.config import (
    get_scala_version,
    global_config,
    validate_session_timezone,
)
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
    TypeDescriptor,
    build_jvm_udxf_imports,
    is_decomposable_struct,
    map_type_to_java_type,
    to_json,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.sql_quoting import quote_single

JAVA_UDTF_PREFIX = "__SC_JAVA_UDTF_"
VARIANT_COMPATIBLE_TYPES = (ArrayType, MapType, StructType, VariantType)


def _output_java_type(dt: Optional[snowpark_type.DataType]) -> str:
    """Java boxed type for a UDTF output column; falls back to Variant for complex types."""
    return TypeDescriptor.from_snowpark(dt).java_type


def _output_sql_type(dt: Optional[snowpark_type.DataType]) -> str:
    """Snowflake SQL type for a UDTF output column; falls back to VARIANT."""
    return TypeDescriptor.from_snowpark(dt).sql_type


# ---------------------------------------------------------------------------
# Shared Java boilerplate fragments
# ---------------------------------------------------------------------------

_JAVA_IMPORTS = """\
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
"""

_LOAD_OPERATION_FLATMAP = """\
    private static void loadOperation() throws IOException, ClassNotFoundException {
        if (operation != null) {
            return;
        }
        java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("UTC"));
        udfPacket = com.snowflake.sas.scala.Utils$.MODULE$.deserializeUdfPacket(OPERATION_FILE);
        operation = (scala.Function1<scala.collection.Iterator<Object>, scala.collection.Iterator<Object>>) udfPacket.function();
    }
"""

_LOAD_OPERATION_GENERIC = """\
    private static void loadOperation() throws IOException, ClassNotFoundException {
        if (operation != null) {
            return;
        }
        java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("UTC"));
        udfPacket = com.snowflake.sas.scala.Utils$.MODULE$.deserializeUdfPacket(OPERATION_FILE);
        operation = udfPacket.function();
    }
"""


def _gen_output_row_class(out_desc: TypeDescriptor, prefix: str) -> str:
    """Generate OutputRow class body from a TypeDescriptor."""
    if out_desc.fields:
        field_decls = "\n  ".join(
            f"public {f.java_type} {prefix}C{i};" for i, f in enumerate(out_desc.fields)
        )
        ctor_params = ", ".join(
            f"{f.java_type} {prefix}C{i}" for i, f in enumerate(out_desc.fields)
        )
        ctor_body = "\n    ".join(
            f"this.{prefix}C{i} = {prefix}C{i};" for i in range(len(out_desc.fields))
        )
    else:
        field_decls = f"public {out_desc.java_type} {prefix}C1;"
        ctor_params = f"{out_desc.java_type} {prefix}C1"
        ctor_body = f"this.{prefix}C1 = {prefix}C1;"
    return (
        f"public class OutputRow {{\n"
        f"  {field_decls}\n"
        f"  public OutputRow({ctor_params}) {{\n"
        f"    {ctor_body}\n"
        f"  }}\n"
        f"}}"
    )


def _gen_convert_input_call(in_desc: TypeDescriptor, param_names: list[str]) -> str:
    """Java statement that calls convertInput and stores the result in 'mappedInput'."""
    is_struct = "true" if in_desc.fields else "false"
    args_array = ", ".join(param_names)
    return (
        f"Object[] _sas_args = new Object[]{{{args_array}}};\n"
        f"        Object mappedInput = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$"
        f".convertInput(udfPacket, _sas_args, 0, {is_struct}, SCHEMA_JSON, SESSION_TIMEZONE);"
    )


def _gen_field_conv_vars(
    out_desc: TypeDescriptor,
) -> tuple[list[str], list[str]]:
    """Generate per-field Java lines and constructor args for struct output conversion.

    Returns (java_lines, ctor_args). Caller is responsible for the leading
    ``_sas_flds`` extraction line and the trailing ``return``/``results.add`` line.
    """
    n = len(out_desc.fields)
    lines = [
        f'if (_sas_flds != null && _sas_flds.length != {n}) {{ throw new RuntimeException("Struct output arity mismatch: expected {n} fields but got " + _sas_flds.length + " — struct decomposition count changed between DDL creation and call site"); }}',
    ]
    ctor_args = []
    for i, f in enumerate(out_desc.fields):
        lines.append(f"Object _sas_rf{i} = _sas_flds != null ? _sas_flds[{i}] : null;")
        if f.java_type == "Variant":
            lines.append(
                f"Variant _sas_cv{i} = _sas_rf{i} == null ? null"
                f" : com.snowflake.sas.scala.Utils$.MODULE$.toVariant(_sas_rf{i}, udfPacket);"
            )
            ctor_args.append(f"_sas_cv{i}")
        elif f.java_type in ("Long", "Double"):
            method = "longValue" if f.java_type == "Long" else "doubleValue"
            lines.append(
                f"{f.java_type} _sas_cv{i} = _sas_rf{i} == null ? null"
                f" : (({f.java_type}) ((Number) _sas_rf{i}).{method}());"
            )
            ctor_args.append(f"_sas_cv{i}")
        else:
            lines.append(f"{f.java_type} _sas_cv{i} = ({f.java_type}) _sas_rf{i};")
            ctor_args.append(f"_sas_cv{i}")
    return lines, ctor_args


def _gen_output_row_from_result(out_desc: TypeDescriptor, result_expr: str) -> str:
    """Java expression that converts a Scala result to a new OutputRow(...)."""
    if out_desc.fields:
        conv_lines, ctor_args = _gen_field_conv_vars(out_desc)
        lines = [
            f"Object[] _sas_flds = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.convertOutput((Object) ({result_expr}));",
            *conv_lines,
            f"return new OutputRow({', '.join(ctor_args)});",
        ]
        return " ".join(lines)
    elif out_desc.java_type == "Variant":
        return f"return new OutputRow(com.snowflake.sas.scala.Utils$.MODULE$.toVariant({result_expr}, udfPacket));"
    else:
        # native scalar output
        jt = out_desc.java_type
        if jt in ("Long", "Double"):
            method = "longValue" if jt == "Long" else "doubleValue"
            return (
                f"Object _sas_r = {result_expr}; "
                f"return new OutputRow(_sas_r == null ? null : (({jt})(((Number)_sas_r).{method}())));"
            )
        return f"return new OutputRow(({jt}) {result_expr});"


def _gen_accum_stmt(out_desc: TypeDescriptor, iter_var: str) -> str:
    """Java statement that pops one result and adds to List<OutputRow> results."""
    if out_desc.fields:
        conv_lines, ctor_args = _gen_field_conv_vars(out_desc)
        lines = [
            f"Object _sas_raw = {iter_var}.next();",
            "Object[] _sas_flds = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.convertOutput((Object) _sas_raw);",
            *conv_lines,
            f"results.add(new OutputRow({', '.join(ctor_args)}));",
        ]
        return "\n            ".join(lines)
    elif out_desc.java_type == "Variant":
        return (
            f"Variant _sas_v = com.snowflake.sas.scala.Utils$.MODULE$"
            f".toVariant({iter_var}.next(), udfPacket);\n"
            f"            results.add(new OutputRow(_sas_v));"
        )
    else:
        jt = out_desc.java_type
        if jt in ("Long", "Double"):
            method = "longValue" if jt == "Long" else "doubleValue"
            return (
                f"Object _sas_r = {iter_var}.next();\n"
                f"            {jt} _sas_v = _sas_r == null ? null : (({jt})(((Number)_sas_r).{method}()));\n"
                f"            results.add(new OutputRow(_sas_v));"
            )
        return f"{jt} _sas_v = ({jt}) {iter_var}.next();\n            results.add(new OutputRow(_sas_v));"


# ---------------------------------------------------------------------------
# JavaUDTFDef — flatMap and mapPartitions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class JavaUDTFDef:
    """
    Definition for creating a Java UDTF in Snowflake for both flatMap (per-row)
    and mapPartitions (batch) semantics.
    """

    name: str
    signature: Signature
    imports: list[str]
    schema_json: str
    batch_mode: bool = False
    null_handling: NullHandling = NullHandling.RETURNS_NULL_ON_NULL_INPUT
    input_snowpark_type: Optional[snowpark_type.DataType] = None
    return_snowpark_type: Optional[snowpark_type.DataType] = None

    def _in_desc(self) -> TypeDescriptor:
        dt = self.input_snowpark_type
        if is_decomposable_struct(dt):
            return TypeDescriptor.for_struct(dt)
        return TypeDescriptor.from_snowpark(dt)

    def _out_desc(self) -> TypeDescriptor:
        dt = self.return_snowpark_type
        if is_decomposable_struct(dt):
            return TypeDescriptor.for_struct(dt)
        return TypeDescriptor.from_snowpark(dt)

    def _param_names(self) -> list[str]:
        """Names of the Java handler parameters (in0, in1, ... or just 'input')."""
        in_desc = self._in_desc()
        if in_desc.fields:
            return [f"in{i}" for i in range(len(in_desc.fields))]
        return ["input"]

    def _process_params(self) -> str:
        """Java parameter declaration string for process()."""
        in_desc = self._in_desc()
        if in_desc.fields:
            return ", ".join(
                f"{f.java_type} in{i}" for i, f in enumerate(in_desc.fields)
            )
        return f"{in_desc.java_type} input"

    def _gen_body_java(self) -> str:
        in_desc = self._in_desc()
        out_desc = self._out_desc()
        param_names = self._param_names()
        convert_input = _gen_convert_input_call(in_desc, param_names)
        process_params = self._process_params()
        session_tz = validate_session_timezone(
            global_config.spark_sql_session_timeZone or "UTC"
        )
        operation_file = self.imports[0].split("/")[-1]
        out_row_class = _gen_output_row_class(out_desc, JAVA_UDTF_PREFIX)

        if self.batch_mode:
            # mapPartitions: process() accumulates; endPartition() applies function
            accum_body = _gen_accum_stmt(out_desc, "scalaResult")
            body = f"""\
{_JAVA_IMPORTS}
{out_row_class}

public class JavaUdtfHandler {{
    private final static String OPERATION_FILE = "{operation_file}";
    private final static String SCHEMA_JSON = "{self.schema_json}";
    private final static String SESSION_TIMEZONE = "{session_tz}";
    private static scala.Function1<scala.collection.Iterator<Object>, scala.collection.Iterator<Object>> operation = null;
    private static UdfPacket udfPacket = null;
    private List<Object> accumulatedInputs = new ArrayList<>();

  public static Class getOutputClass() {{ return OutputRow.class; }}

{_LOAD_OPERATION_FLATMAP}
  public Stream<OutputRow> process({process_params}) throws IOException, ClassNotFoundException {{
        loadOperation();
        {convert_input}
        accumulatedInputs.add(mappedInput);
        return Stream.empty();
  }}

  public Stream<OutputRow> endPartition() throws IOException, ClassNotFoundException {{
        if (accumulatedInputs.isEmpty()) {{
            return Stream.empty();
        }}
        loadOperation();

        java.util.Iterator<Object> javaIterator = accumulatedInputs.iterator();
        scala.collection.Iterator<Object> scalaInput = new scala.collection.AbstractIterator<Object>() {{
            public boolean hasNext() {{ return javaIterator.hasNext(); }}
            public Object next() {{ return javaIterator.next(); }}
        }};

        scala.collection.Iterator<Object> scalaResult = operation.apply(scalaInput);

        List<OutputRow> results = new ArrayList<>();
        while (scalaResult.hasNext()) {{
            {accum_body}
        }}

        accumulatedInputs.clear();
        return results.stream();
  }}
}}
"""
        else:
            # flatMap: process() applies function per row
            out_row_expr = _gen_output_row_from_result(out_desc, "scalaResult.next()")
            body = f"""\
{_JAVA_IMPORTS}
{out_row_class}

public class JavaUdtfHandler {{
    private final static String OPERATION_FILE = "{operation_file}";
    private final static String SCHEMA_JSON = "{self.schema_json}";
    private final static String SESSION_TIMEZONE = "{session_tz}";
    private static scala.Function1<scala.collection.Iterator<Object>, scala.collection.Iterator<Object>> operation = null;
    private static UdfPacket udfPacket = null;

  public static Class getOutputClass() {{ return OutputRow.class; }}

{_LOAD_OPERATION_FLATMAP}
  public Stream<OutputRow> process({process_params}) throws IOException, ClassNotFoundException {{
        loadOperation();

        {convert_input}

        java.util.Iterator<Object> javaInput = Arrays.asList(mappedInput).iterator();
        scala.collection.Iterator<Object> scalaInput = new scala.collection.AbstractIterator<Object>() {{
            public boolean hasNext() {{ return javaInput.hasNext(); }}
            public Object next() {{ return javaInput.next(); }}
        }};

        scala.collection.Iterator<Object> scalaResult = operation.apply(scalaInput);

        java.util.Iterator<OutputRow> javaResult = new java.util.Iterator<OutputRow>() {{
            public boolean hasNext() {{ return scalaResult.hasNext(); }}
            public OutputRow next() {{ {out_row_expr} }}
        }};

        return StreamSupport.stream(Spliterators.spliteratorUnknownSize(javaResult, Spliterator.ORDERED), false)
                .map(i -> i);
  }}

  public Stream<OutputRow> endPartition() {{
    return Stream.empty();
  }}
}}
"""
        return body

    def to_create_function_sql(self) -> str:
        args = ", ".join(
            [f"{param.name} {param.data_type}" for param in self.signature.params]
        )
        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"

        if is_decomposable_struct(self.return_snowpark_type):
            fields = self.return_snowpark_type.fields
            ret_cols = ", ".join(
                f"{JAVA_UDTF_PREFIX}C{i} {_output_sql_type(f.datatype)}"
                for i, f in enumerate(fields)
            )
            returns_clause = f"returns table ({ret_cols})"
        else:
            out_sql = _output_sql_type(self.return_snowpark_type)
            returns_clause = f"returns table ({JAVA_UDTF_PREFIX}C1 {out_sql})"

        return f"""
create or replace function {self.name}({args})
{returns_clause}
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

    input_snowpark_dt: snowpark_type.DataType | None = (
        arg_types[0] if arg_types else None
    )

    java_input_params: list[Param] = []
    sql_input_params: list[Param] = []

    if is_decomposable_struct(input_snowpark_dt):
        for i, f in enumerate(input_snowpark_dt.fields):
            desc = TypeDescriptor.from_snowpark(f.datatype)
            java_input_params.append(Param(f"in{i}", desc.java_type))
            sql_input_params.append(Param(f"in{i}", desc.sql_type))
    else:
        for i, _ in enumerate(udf_proto.scalar_scala_udf.inputTypes):
            param_name = "arg" + str(i)
            dt = arg_types[i] if arg_types and i < len(arg_types) else None
            desc = TypeDescriptor.from_snowpark(dt)
            java_input_params.append(Param(param_name, desc.java_type))
            sql_input_params.append(Param(param_name, desc.sql_type))

    return_type = proto_to_snowpark_type(udf_proto.scalar_scala_udf.outputType)
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
        schema_json=schema_json,
        batch_mode=batch_mode,
        input_snowpark_type=input_snowpark_dt,
        return_snowpark_type=return_type,
    )

    mode_label = "map_partitions" if batch_mode else "flatmap"
    sql = udtf.to_create_function_sql()
    logger.info(
        f"Creating Java UDTF {mode_label}: {udtf_name}({','.join([str(param) for param in sql_input_params])})"
    )
    logger.debug(f"Java UDTF with body {mode_label}: {sql}")
    session.sql(sql).collect()

    return udtf_name


# ---------------------------------------------------------------------------
# JavaGroupMapUDTFDef — mapGroups / flatMapGroups / mapGroupsWithState
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class JavaGroupMapUDTFDef:
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
    return_snowpark_type: Optional[snowpark_type.DataType] = None

    def _gen_body_java(self) -> str:
        session_tz = validate_session_timezone(
            global_config.spark_sql_session_timeZone or "UTC"
        )
        operation_file = self.imports[0].split("/")[-1]
        _rt = self.return_snowpark_type
        out_desc = (
            TypeDescriptor.for_struct(_rt)
            if is_decomposable_struct(_rt)
            else TypeDescriptor.from_snowpark(_rt)
        )
        out_row_class = _gen_output_row_class(out_desc, JAVA_UDTF_PREFIX)
        accum_body = _gen_accum_stmt(out_desc, "scalaResultIterator")

        if self.is_variant_key:
            key_conv = "Object scalaKey = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, currentKey, 0, SCHEMA_JSON, SESSION_TIMEZONE);"
        else:
            key_conv = "Object scalaKey = currentKey;"

        if self.is_variant_value:
            val_iter = """
        java.util.Iterator<Object> javaIterator = accumulatedValues.stream()
            .map(v -> com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, v, 1, SCHEMA_JSON, SESSION_TIMEZONE))
            .iterator();
        scala.collection.Iterator<Object> scalaIterator = new scala.collection.AbstractIterator<Object>() {
            public boolean hasNext() { return javaIterator.hasNext(); }
            public Object next() { return javaIterator.next(); }
        };"""
        else:
            vt = self.value_type_java
            val_iter = f"""
        java.util.Iterator<{vt}> javaIterator = accumulatedValues.iterator();
        scala.collection.Iterator<Object> scalaIterator = new scala.collection.AbstractIterator<Object>() {{
            public boolean hasNext() {{ return javaIterator.hasNext(); }}
            public Object next() {{ return javaIterator.next(); }}
        }};"""

        if self.has_initial_state:
            process_method = f"""
  private Variant initialStateVariant = null;

  public Stream<OutputRow> process({self.key_type_java} key, {self.value_type_java} value, Variant initialState) throws IOException, ClassNotFoundException {{
        loadOperation();
        currentKey = key;
        accumulatedValues.add(value);
        if (initialState != null && initialStateVariant == null) {{
            initialStateVariant = initialState;
        }}
        return Stream.empty();
  }}"""
            group_state = """
            Object scalaInitialState = initialStateVariant != null
                ? com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariantAsOutput(udfPacket, initialStateVariant, SESSION_TIMEZONE)
                : null;
            org.apache.spark.sql.streaming.GroupState<Object> groupState = scalaInitialState != null
                ? org.apache.spark.sql.scos.GroupStateUtils$.MODULE$.groupStateWithInitial(scalaInitialState)
                : org.apache.spark.sql.scos.GroupStateUtils$.MODULE$.emptyGroupState();"""
        else:
            process_method = f"""
  public Stream<OutputRow> process({self.key_type_java} key, {self.value_type_java} value) throws IOException, ClassNotFoundException {{
        loadOperation();
        currentKey = key;
        accumulatedValues.add(value);
        return Stream.empty();
  }}"""
            group_state = "            org.apache.spark.sql.streaming.GroupState<Object> groupState = org.apache.spark.sql.scos.GroupStateUtils$.MODULE$.emptyGroupState();"

        load_op = _LOAD_OPERATION_GENERIC.replace(
            "operation = udfPacket.function();",
            "operation = udfPacket.function();\n        hasGroupState = operation instanceof scala.Function3;",
        )

        return f"""\
{_JAVA_IMPORTS}
{out_row_class}

public class JavaUdtfHandler {{
    private final static String OPERATION_FILE = "{operation_file}";
    private final static String SCHEMA_JSON = "{self.schema_json}";
    private final static String SESSION_TIMEZONE = "{session_tz}";
    private static Object operation = null;
    private static boolean hasGroupState = false;
    private static UdfPacket udfPacket = null;

    private {self.key_type_java} currentKey = null;
    private List<{self.value_type_java}> accumulatedValues = new ArrayList<>();

  public static Class getOutputClass() {{ return OutputRow.class; }}

{load_op}
{process_method}

  public Stream<OutputRow> endPartition() throws IOException, ClassNotFoundException {{
        if (accumulatedValues.isEmpty()) {{
            return Stream.empty();
        }}

        {key_conv}
        {val_iter}

        Object scalaResult;
        if (hasGroupState) {{
            scala.Function3<Object, scala.collection.Iterator<Object>, org.apache.spark.sql.streaming.GroupState<Object>, Object> func3 =
                (scala.Function3<Object, scala.collection.Iterator<Object>, org.apache.spark.sql.streaming.GroupState<Object>, Object>) operation;
            {group_state}
            scalaResult = func3.apply(scalaKey, scalaIterator, groupState);
        }} else {{
            scala.Function2<Object, scala.collection.Iterator<Object>, Object> func2 =
                (scala.Function2<Object, scala.collection.Iterator<Object>, Object>) operation;
            scalaResult = func2.apply(scalaKey, scalaIterator);
        }}

        scala.collection.Iterator<Object> scalaResultIterator;
        if (scalaResult instanceof scala.collection.Iterator) {{
            scalaResultIterator = (scala.collection.Iterator<Object>) scalaResult;
        }} else {{
            scalaResultIterator = ((scala.collection.Iterable<Object>) scalaResult).iterator();
        }}

        List<OutputRow> results = new ArrayList<>();
        while (scalaResultIterator.hasNext()) {{
            {accum_body}
        }}

        accumulatedValues.clear();
        return results.stream();
  }}
}}
"""

    def to_create_function_sql(self) -> str:
        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"

        if self.has_initial_state:
            params = f"key {self.key_type_sql}, value {self.value_type_sql}, initial_state VARIANT"
        else:
            params = f"key {self.key_type_sql}, value {self.value_type_sql}"

        if is_decomposable_struct(self.return_snowpark_type):
            ret_cols = ", ".join(
                f"{JAVA_UDTF_PREFIX}C{i} {_output_sql_type(f.datatype)}"
                for i, f in enumerate(self.return_snowpark_type.fields)
            )
            returns_clause = f"returns table ({ret_cols})"
        else:
            returns_clause = f"returns table ({JAVA_UDTF_PREFIX}C1 {_output_sql_type(self.return_snowpark_type)})"

        return f"""
create or replace function {self.name}({params})
{returns_clause}
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
        return_snowpark_type=proto_to_snowpark_type(
            udf_proto.scalar_scala_udf.outputType
        ),
    )

    sql = udtf.to_create_function_sql()
    logger.info(f"Creating Java UDTF group_map: {udtf_name}")
    logger.debug(f"Java UDTF with body group_map: {sql}")
    session.sql(sql).collect()

    return udtf_name


# ---------------------------------------------------------------------------
# JavaCoGroupMapUDTFDef — cogroup
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class JavaCoGroupMapUDTFDef:
    name: str
    key_type_java: str
    key_type_sql: str
    value_type_java: str
    value_type_sql: str
    imports: list[str]
    is_variant_key: bool
    is_variant_value: bool
    schema_json: str = "[]"
    return_snowpark_type: Optional[snowpark_type.DataType] = None

    def _gen_body_java(self) -> str:
        session_tz = validate_session_timezone(
            global_config.spark_sql_session_timeZone or "UTC"
        )
        operation_file = self.imports[0].split("/")[-1]
        _rt = self.return_snowpark_type
        out_desc = (
            TypeDescriptor.for_struct(_rt)
            if is_decomposable_struct(_rt)
            else TypeDescriptor.from_snowpark(_rt)
        )
        out_row_class = _gen_output_row_class(out_desc, JAVA_UDTF_PREFIX)
        accum_body = _gen_accum_stmt(out_desc, "scalaResultIterator")

        if self.is_variant_key:
            key_conv = "Object scalaKey = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, currentKey, 0, SCHEMA_JSON, SESSION_TIMEZONE);"
        else:
            key_conv = "Object scalaKey = currentKey;"

        def _make_val_iter(suffix: str, idx: int) -> str:
            if self.is_variant_value:
                return f"""
        java.util.Iterator<Object> javaIterator{suffix} = accumulatedValues{suffix}.stream()
            .map(v -> com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.fromVariant(udfPacket, v, {idx}, SCHEMA_JSON, SESSION_TIMEZONE))
            .iterator();
        scala.collection.Iterator<Object> scalaIterator{suffix} = new scala.collection.AbstractIterator<Object>() {{
            public boolean hasNext() {{ return javaIterator{suffix}.hasNext(); }}
            public Object next() {{ return javaIterator{suffix}.next(); }}
        }};"""
            vt = self.value_type_java
            return f"""
        java.util.Iterator<{vt}> javaIterator{suffix} = accumulatedValues{suffix}.iterator();
        scala.collection.Iterator<Object> scalaIterator{suffix} = new scala.collection.AbstractIterator<Object>() {{
            public boolean hasNext() {{ return javaIterator{suffix}.hasNext(); }}
            public Object next() {{ return javaIterator{suffix}.next(); }}
        }};"""

        val_iter1 = _make_val_iter("1", 1)
        val_iter2 = _make_val_iter("2", 2)

        return f"""\
{_JAVA_IMPORTS}
{out_row_class}

public class JavaUdtfHandler {{
    private final static String OPERATION_FILE = "{operation_file}";
    private final static String SCHEMA_JSON = "{self.schema_json}";
    private final static String SESSION_TIMEZONE = "{session_tz}";
    private static Object operation = null;
    private static UdfPacket udfPacket = null;

    private {self.key_type_java} currentKey = null;
    private List<{self.value_type_java}> accumulatedValues1 = new ArrayList<>();
    private List<{self.value_type_java}> accumulatedValues2 = new ArrayList<>();

  public static Class getOutputClass() {{ return OutputRow.class; }}

{_LOAD_OPERATION_GENERIC}
  public Stream<OutputRow> process({self.key_type_java} key, {self.value_type_java} value, Integer source) throws IOException, ClassNotFoundException {{
        loadOperation();
        currentKey = key;
        if (value != null) {{
            if (source == 1) {{
                accumulatedValues1.add(value);
            }} else {{
                accumulatedValues2.add(value);
            }}
        }}
        return Stream.empty();
  }}

  public Stream<OutputRow> endPartition() throws IOException, ClassNotFoundException {{
        if (accumulatedValues1.isEmpty() && accumulatedValues2.isEmpty()) {{
            return Stream.empty();
        }}

        {key_conv}
        {val_iter1}
        {val_iter2}

        scala.Function3<Object, scala.collection.Iterator<Object>, scala.collection.Iterator<Object>, Object> func3 =
            (scala.Function3<Object, scala.collection.Iterator<Object>, scala.collection.Iterator<Object>, Object>) operation;
        Object scalaResult = func3.apply(scalaKey, scalaIterator1, scalaIterator2);

        scala.collection.Iterator<Object> scalaResultIterator;
        if (scalaResult instanceof scala.collection.Iterator) {{
            scalaResultIterator = (scala.collection.Iterator<Object>) scalaResult;
        }} else {{
            scalaResultIterator = ((scala.collection.Iterable<Object>) scalaResult).iterator();
        }}

        List<OutputRow> results = new ArrayList<>();
        while (scalaResultIterator.hasNext()) {{
            {accum_body}
        }}

        accumulatedValues1.clear();
        accumulatedValues2.clear();
        return results.stream();
  }}
}}
"""

    def to_create_function_sql(self) -> str:
        imports_sql = f"IMPORTS = ({', '.join(quote_single(x) for x in self.imports)})"
        params = f"key {self.key_type_sql}, value {self.value_type_sql}, source INTEGER"

        if is_decomposable_struct(self.return_snowpark_type):
            ret_cols = ", ".join(
                f"{JAVA_UDTF_PREFIX}C{i} {_output_sql_type(f.datatype)}"
                for i, f in enumerate(self.return_snowpark_type.fields)
            )
            returns_clause = f"returns table ({ret_cols})"
        else:
            returns_clause = f"returns table ({JAVA_UDTF_PREFIX}C1 {_output_sql_type(self.return_snowpark_type)})"

        return f"""
create or replace function {self.name}({params})
{returns_clause}
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

    is_variant_value = isinstance(value1_type, VARIANT_COMPATIBLE_TYPES) or isinstance(
        value2_type, VARIANT_COMPATIBLE_TYPES
    )

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
        return_snowpark_type=proto_to_snowpark_type(
            udf_proto.scalar_scala_udf.outputType
        ),
    )

    sql = udtf.to_create_function_sql()
    logger.info(f"Creating Java UDTF co_group_map: {udtf_name}")
    logger.debug(f"Java UDTF with body co_group_map: {sql}")
    session.sql(sql).collect()

    return udtf_name
