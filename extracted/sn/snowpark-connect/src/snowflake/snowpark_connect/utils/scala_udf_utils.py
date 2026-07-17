#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""
Scala UDF utilities for Snowpark Connect.

This module provides utilities for creating and managing Scala User-Defined Functions (UDFs)
in Snowflake through Snowpark Connect. Scala UDFs are wrapped in Java UDFs that call into
the Scala code via the SAS Scala helper library, following the same pattern as Java UDTFs.

Key components:
- ScalaUdf: Reference class for Scala UDFs whose DDL has already been emitted
- LazyCreatedScalaUdf: Reference class for Scala UDFs whose DDL is deferred to first call-site
- JavaScalarUDFDef: Definition class for Java-wrapped Scala UDF creation
- UDF creation and management utilities
"""
import re
from dataclasses import dataclass
from typing import List

import snowflake.snowpark.types as snowpark_type
from snowflake.snowpark import Session
from snowflake.snowpark_connect.config import get_scala_version
from snowflake.snowpark_connect.type_mapping import proto_to_snowpark_type
from snowflake.snowpark_connect.utils.context import get_spark_session_id
from snowflake.snowpark_connect.utils.jvm_udf_utils import (
    NullHandling,
    Param,
    ReturnType,
    Signature,
    TypeDescriptor,
    build_udxf_imports,
    gen_pre_narrow_expr,
    is_decomposable_struct,
    is_native_sql_type,
    map_type_to_snowflake_native_sql_type,
    needs_epoch_lowering,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.sql_quoting import quote_single
from snowflake.snowpark_connect.utils.udf_utils import (
    ProcessCommonInlineUserDefinedFunction,
)

# Prefix used for internally generated Scala UDF names to avoid conflicts
CREATE_SCALA_UDF_PREFIX = "__SC_BUILD_IN_CREATE_UDF_SCALA_"


class ScalaUdf:
    """Scala UDF whose CREATE FUNCTION DDL has already been emitted."""

    def __init__(
        self,
        name: str,
        input_types: List[snowpark_type.DataType],
        return_type: snowpark_type.DataType,
    ) -> None:
        self.name = name
        self._input_types = input_types
        self._return_type = return_type


class LazyCreatedScalaUdf:
    """Scala UDF registered without input types whose CREATE FUNCTION DDL is deferred.

    The DDL is emitted on the first call-site execution once actual types are known,
    eliminating the all-VARIANT DDL that would otherwise be created at registration time.
    ``stage_imports`` holds the Snowflake stage paths (JARs) for the IMPORTS clause.
    In DCR inline-closure mode, ``inline_payload`` carries the raw closure bytes to be
    embedded in the Java handler body instead of read from a stage file.
    """

    def __init__(
        self,
        name: str,
        return_type: snowpark_type.DataType,
        stage_imports: list[str],
        inline_payload: bytes | None = None,
    ) -> None:
        self.name = name
        self._input_types: list[snowpark_type.DataType] = []
        self._return_type = return_type
        self.stage_imports = stage_imports
        self.inline_payload = inline_payload


@dataclass(frozen=True)
class JavaScalarUDFDef:
    """
    Definition for creating a Java UDF in Snowflake that wraps a Scala function.

    The Java wrapper deserializes the Scala closure from a binary file,
    converts inputs to Scala types, invokes the function, and returns the result.
    For primitive/String/Boolean types, native SQL types are used to bypass the
    VARIANT JSON serialization round-trip.
    """

    name: str
    signature: Signature
    imports: list[str]
    num_args: int
    # Per-argument Snowpark types used for code generation; None means unknown (use VARIANT).
    input_snowpark_types: list[snowpark_type.DataType | None]
    # Return Snowpark type for code generation; None means unknown (use VARIANT).
    return_snowpark_type: snowpark_type.DataType | None
    null_handling: NullHandling = NullHandling.CALLED_ON_NULL_INPUT
    # DCR inline-closure mode: embed the closure bytes directly in the Java body instead
    # of reading from an IMPORTS-directory file. When set, ``imports`` contains only JAR
    # paths (no closure binary); the binary is base64-decoded at runtime via
    # ``Utils$.MODULE$.deserializeUdfPacketFromBytes``.
    inline_payload: bytes | None = None

    def _gen_body_java(self) -> str:
        import base64

        if self.inline_payload is not None:
            b64 = base64.b64encode(self.inline_payload).decode("ascii")
            closure_field = (
                f"    private static final byte[] CLOSURE_BYTES = "
                f'java.util.Base64.getDecoder().decode("{b64}");'
            )
            udf_packet_init = (
                "        this.udfPacket = com.snowflake.sas.scala.Utils$.MODULE$"
                ".deserializeUdfPacketFromBytes(CLOSURE_BYTES);"
            )
        else:
            operation_file = self.imports[0].split("/")[-1]
            closure_field = (
                f'    private static final String OPERATION_FILE = "{operation_file}";'
            )
            udf_packet_init = (
                "        this.udfPacket = com.snowflake.sas.scala.Utils$.MODULE$"
                ".deserializeUdfPacket(OPERATION_FILE);"
            )

        # Build per-arg TypeDescriptors and handler parameter declarations.
        arg_descs: list[TypeDescriptor] = []
        handler_params_list: list[str] = []
        for i in range(self.num_args):
            dt = (
                self.input_snowpark_types[i]
                if i < len(self.input_snowpark_types)
                else None
            )
            if is_decomposable_struct(dt):
                desc = TypeDescriptor.for_struct(dt)
                for j, f in enumerate(desc.fields):
                    handler_params_list.append(f"{f.java_type} arg{i}_{j}")
            else:
                desc = TypeDescriptor.from_snowpark(dt)
                handler_params_list.append(f"{desc.java_type} arg{i}")
            arg_descs.append(desc)
        handler_params_list.append("String __schema_json")
        handler_params = ", ".join(handler_params_list)

        ret_desc = TypeDescriptor.from_snowpark(self.return_snowpark_type)
        java_return_type = ret_desc.java_type

        lines: list[str] = []

        # Null checks
        if self.num_args > 0:
            null_checks = []
            for i, desc in enumerate(arg_descs):
                if desc.fields:
                    # Struct decomposition: all decomposed fields null ↔ original struct was null.
                    # Only early-return when the parameter is non-nullable (plain case class);
                    # for Option[T] or AnyRef the UDF must be called so it can handle None/null.
                    all_null = " && ".join(
                        f"arg{i}_{j} == null" for j in range(len(desc.fields))
                    )
                    null_checks.append(
                        f"(({all_null})"
                        f" && com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.isNonNullableParam(udfPacket, {i}))"
                    )
                elif desc.is_native:
                    null_checks.append(
                        f"com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.isNullNonNullableNative(udfPacket, arg{i}, {i})"
                    )
                else:
                    null_checks.append(
                        f"com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.isNullNonNullable(udfPacket, arg{i}, {i})"
                    )
            lines.append(f"        if ({' || '.join(null_checks)}) return null;")

        # Input conversion via unified convertInput
        for i, desc in enumerate(arg_descs):
            if desc.fields:
                fields_arr = ", ".join(
                    gen_pre_narrow_expr(desc.fields[j].snowpark_type, f"arg{i}_{j}")
                    for j in range(len(desc.fields))
                )
                lines.append(
                    f"        Object[] _sas_args_{i} = new Object[]{{{fields_arr}}};"
                )
                lines.append(
                    f"        var in{i} = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$"
                    f'.convertInput(udfPacket, _sas_args_{i}, {i}, true, __schema_json, java.time.ZoneId.of(System.getProperty("user.timezone")));'
                )
            else:
                lines.append(
                    f"        Object[] _sas_args_{i} = new Object[]{{arg{i}}};"
                )
                lines.append(
                    f"        var in{i} = com.snowflake.sas.scala.UdfPacketUtils$.MODULE$"
                    f'.convertInput(udfPacket, _sas_args_{i}, {i}, false, __schema_json, java.time.ZoneId.of(System.getProperty("user.timezone")));'
                )

        object_types = ", ".join(["Object"] * (self.num_args + 1))
        func_type = f"scala.Function{self.num_args}<{object_types}>"
        func_args = ", ".join(f"in{i}" for i in range(self.num_args))

        lines.append(f"        var typedFunc = ({func_type}) func;")
        lines.append(f"        var result = typedFunc.apply({func_args});")
        if ret_desc.is_native:
            # Unwrap scala.Option if the UDF declared Option[T] as its return type.
            lines.append(
                "        result = result instanceof scala.Option"
                " ? (((scala.Option<?>) result).isEmpty() ? null : ((scala.Option<?>) result).get())"
                " : result;"
            )
            if needs_epoch_lowering(self.return_snowpark_type):
                # Temporal/interval return: Scala value (Date, Timestamp, Period, Duration)
                # must be converted to its epoch Long representation so the RETURNS INT/BIGINT
                # DDL type is satisfied. encodeTemporalToEpoch uses the output encoder to determine
                # the correct inverse conversion.
                lines.append(
                    "        return com.snowflake.sas.scala.UdfPacketUtils$.MODULE$.encodeTemporalToEpoch(result, udfPacket);"
                )
            else:
                lines.append(
                    f"        return {_gen_native_return_cast(java_return_type)};"
                )
        else:
            lines.append(
                "        return com.snowflake.sas.scala.Utils$.MODULE$.toVariant(result, udfPacket);"
            )

        body = "\n".join(lines)

        return f"""
import org.apache.spark.sql.connect.common.UdfPacket;
import com.snowflake.snowpark_java.types.Variant;

public class RecreatedSparkJavaUdf {{
{closure_field}
    private final UdfPacket udfPacket;
    private final Object func;

    public RecreatedSparkJavaUdf() {{
        java.util.TimeZone.setDefault(java.util.TimeZone.getTimeZone("UTC"));
{udf_packet_init}
        this.func = udfPacket.function();
    }}

    public {java_return_type} handler({handler_params}) {{
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
        args = ", ".join(f"{p.name} {p.data_type}" for p in self.signature.params)
        ret_type = self.signature.returns.data_type

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


def _gen_native_return_cast(java_return_type: str) -> str:
    """Generate the Java return expression for a native (non-Variant) return type."""
    if java_return_type == "Boolean":
        return "(Boolean) result"
    if java_return_type == "String":
        # Use toString() instead of a direct cast so that enum-returning UDFs
        # (Scala Enumeration#Value / Java enum) stringify correctly without CCE.
        return "result == null ? null : result.toString()"
    if java_return_type == "byte[]":
        return "(byte[]) result"
    if java_return_type == "java.math.BigDecimal":
        return "(java.math.BigDecimal) result"
    # Long or Double: cast through Number to handle Scala Int/Float boxing mismatches.
    method = "longValue" if java_return_type == "Long" else "doubleValue"
    return (
        f"result == null ? null : (({java_return_type}) ((Number) result).{method}())"
    )


def _build_scala_udf_sql_input_params(
    input_types: list[snowpark_type.DataType],
) -> tuple[list[Param], list[snowpark_type.DataType | None]]:
    """Build the SQL parameter list and parallel snowpark-type list for a Scala UDF DDL.

    Uses native Snowflake SQL types (VARCHAR, BIGINT, etc.) for simple types and
    decomposes struct arguments into per-field parameters. Appends a trailing
    ``__schema_json VARCHAR`` sentinel required by the Java handler.

    Returns (sql_input_params, input_snowpark_types).
    """
    sql_input_params: list[Param] = []
    input_snowpark_types: list[snowpark_type.DataType | None] = []
    for i, dt in enumerate(input_types):
        if is_native_sql_type(dt):
            sql_input_params.append(
                Param(f"arg{i}", map_type_to_snowflake_native_sql_type(dt))
            )
        elif is_decomposable_struct(dt):
            for j, field in enumerate(dt.fields):
                if is_native_sql_type(field.datatype):
                    sql_input_params.append(
                        Param(
                            f"arg{i}_{j}",
                            map_type_to_snowflake_native_sql_type(field.datatype),
                        )
                    )
                else:
                    sql_input_params.append(Param(f"arg{i}_{j}", "VARIANT"))
        else:
            sql_input_params.append(Param(f"arg{i}", "VARIANT"))
        input_snowpark_types.append(dt)
    sql_input_params.append(Param("__schema_json", "VARCHAR"))
    return sql_input_params, input_snowpark_types


def _emit_scala_udf_ddl(
    udf_name: str,
    imports: list[str],
    call_site_types: list[snowpark_type.DataType],
    return_type: snowpark_type.DataType,
    session: Session,
    inline_payload: bytes | None = None,
) -> None:
    """Emit the CREATE FUNCTION SQL for a deferred Scala UDF.

    Called by ``LazySnowparkUdf._emit_ddl()`` on first call-site execution.
    Uses native SQL types (VARCHAR, BIGINT, etc.) wherever possible to avoid
    VARIANT JSON serialization overhead.

    Returns the effective return type used in the DDL.  This may differ from
    ``return_type`` when the declared return is the default JBigDecimal encoding
    (DecimalType(38,18)) and the call-site has a more specific Decimal input type,
    in which case the call-site type is used to avoid scale mismatch / overflow.
    """
    num_args = len(call_site_types)
    sql_input_params, input_snowpark_types = _build_scala_udf_sql_input_params(
        call_site_types
    )

    # When the declared return type is the default JBigDecimal encoding (38,18)
    # and there is exactly one Decimal call-site input, infer the return type from
    # the call-site so Snowflake doesn't overflow the declared scale.
    effective_return_type = return_type
    if (
        isinstance(return_type, snowpark_type.DecimalType)
        and return_type.precision == 38
        and return_type.scale == 18
    ):
        decimal_inputs = [
            t for t in call_site_types if isinstance(t, snowpark_type.DecimalType)
        ]
        if len(decimal_inputs) == 1:
            effective_return_type = decimal_inputs[0]

    sql_return_type = (
        map_type_to_snowflake_native_sql_type(effective_return_type)
        if is_native_sql_type(effective_return_type)
        else "VARIANT"
    )

    udf_def = JavaScalarUDFDef(
        name=udf_name,
        signature=Signature(
            params=sql_input_params, returns=ReturnType(sql_return_type)
        ),
        imports=imports,
        num_args=num_args,
        input_snowpark_types=input_snowpark_types,
        return_snowpark_type=effective_return_type,
        inline_payload=inline_payload,
    )
    create_udf_sql = udf_def.to_create_function_sql()
    logger.info(
        f"Creating deferred Scala UDF DDL with native types: "
        f"{udf_name}({','.join(str(p) for p in sql_input_params)})"
    )
    logger.debug(f"Deferred Java UDF with body: {create_udf_sql}")
    session.sql(create_udf_sql).collect()
    return effective_return_type


def create_scala_udf(
    pciudf: ProcessCommonInlineUserDefinedFunction,
) -> "ScalaUdf | LazyCreatedScalaUdf":
    """
    Create a Java UDF in Snowflake that wraps a Scala function
    from a ProcessCommonInlineUserDefinedFunction object.
    """
    from snowflake.snowpark_connect.config import is_native_app_mode
    from snowflake.snowpark_connect.resources_initializer import (
        ensure_scala_udf_jars_uploaded,
    )

    # In Native App mode the JARs live in the version stage already; skip upload.
    if not is_native_app_mode():
        # Lazily upload Scala UDF jars on-demand when a UDF is actually created.
        # This is thread-safe and will only upload once even if multiple threads call it.
        ensure_scala_udf_jars_uploaded()

    function_name = pciudf._function_name
    if not function_name:
        # If a function name is not provided, hash the binary file and use the first ten characters as the function name.
        import hashlib

        function_name = hashlib.sha256(pciudf._payload).hexdigest()[:10]
    session_id = get_spark_session_id()
    session_suffix = f"_{session_id.replace('-','_')}" if session_id else ""
    udf_name = CREATE_SCALA_UDF_PREFIX + function_name + session_suffix

    # In case the Scala UDF was created with `spark.udf.register`, the Spark Scala input types (from protobuf) are
    # stored in pciudf.scala_input_types.
    # We cannot rely solely on the inputTypes field from the Scala UDF or the Snowpark input types, since:
    # - spark.udf.register arguments come from the inputTypes field
    # - UDFs created with a data type (like below) do not populate the inputTypes field. This requires the input types
    #   inferred by Snowpark. e.g.: udf((i: Long) => (i + 1).toInt, IntegerType)
    #
    # Prefer _input_types (already-Snowpark types from the call-site) when available; they are
    # always correct and avoid proto-conversion failures that would fall back to VariantType.
    # Fall back to _scala_input_types (proto DataType objects) only for spark.udf.register where
    # no call-site types are passed.
    raw_input_types = pciudf._input_types or pciudf._scala_input_types
    input_types: list[snowpark_type.DataType] = []
    if raw_input_types:
        for t in raw_input_types:
            if isinstance(t, snowpark_type.DataType):
                input_types.append(t)
            else:
                try:
                    input_types.append(proto_to_snowpark_type(t))
                except Exception:
                    input_types.append(snowpark_type.VariantType())

    session = get_or_create_snowpark_session()
    imports, inline_payload = build_udxf_imports(
        session,
        pciudf._payload,
        udf_name,
    )

    def _is_default_decimal(t: snowpark_type.DataType) -> bool:
        return (
            isinstance(t, snowpark_type.DecimalType)
            and t.precision == 38
            and t.scale == 18
        )

    if (
        not input_types or all(_is_default_decimal(t) for t in input_types)
    ) and pciudf._called_from == "register_udf":
        # Input types are unknown or all carry the default JBigDecimal encoding
        # (DecimalType(38,18)), which has no real precision/scale information.
        # Defer DDL creation to the first call-site execution so actual argument
        # types (e.g. DECIMAL(18,4)) are used for the Snowflake parameter types.
        logger.info(f"Deferring Scala UDF DDL creation until first call: {udf_name}")
        return LazyCreatedScalaUdf(
            udf_name,
            pciudf._return_type,
            stage_imports=imports,
            inline_payload=inline_payload,
        )

    num_args = len(input_types)
    sql_input_params, input_snowpark_types = _build_scala_udf_sql_input_params(
        input_types
    )

    # Determine SQL return type.
    ret_dt: snowpark_type.DataType | None = pciudf._return_type
    sql_return_type = (
        map_type_to_snowflake_native_sql_type(ret_dt)
        if is_native_sql_type(ret_dt)
        else "VARIANT"
    )

    udf_def = JavaScalarUDFDef(
        name=udf_name,
        signature=Signature(
            params=sql_input_params, returns=ReturnType(sql_return_type)
        ),
        imports=imports,
        num_args=num_args,
        input_snowpark_types=input_snowpark_types,
        return_snowpark_type=ret_dt,
        inline_payload=inline_payload,
    )
    create_udf_sql = udf_def.to_create_function_sql()
    logger.info(
        f"Creating Java UDF for Scala function: {udf_name}({','.join([str(param) for param in sql_input_params])})"
    )
    logger.debug(f"Java UDF with body: {create_udf_sql}")
    session.sql(create_udf_sql).collect()
    return ScalaUdf(udf_name, input_types, pciudf._return_type)


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
