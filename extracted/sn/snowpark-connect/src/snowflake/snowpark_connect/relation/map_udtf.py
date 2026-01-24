#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from typing import Any, List, Tuple

import pyspark.sql.connect.proto.relations_pb2 as relation_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto
from pyspark.errors.exceptions.base import PySparkTypeError, PythonException

from snowflake.snowpark.functions import col, parse_json
from snowflake.snowpark.types import (
    ArrayType,
    DataType,
    MapType,
    StructType,
    VariantType,
)
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import (
    get_boolean_session_config_param,
    global_config,
)
from snowflake.snowpark_connect.dataframe_container import DataFrameContainer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.map_expression import (
    map_single_column_expression,
)
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.type_mapping import (
    map_type_string_to_proto,
    proto_to_snowpark_type,
)
from snowflake.snowpark_connect.utils.context import push_udtf_context
from snowflake.snowpark_connect.utils.external_udxf_cache import (
    cache_external_udtf,
    get_external_udtf_from_cache,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.udtf_helper import (
    SnowparkUDTF,
    create_udtf_in_sproc,
    require_creating_udtf_in_sproc,
    udtf_check,
)
from snowflake.snowpark_connect.utils.udtf_utils import create_udtf
from snowflake.snowpark_connect.utils.udxf_import_utils import (
    get_python_udxf_import_files,
)


def cache_external_udtf_wrapper(from_register_udtf: bool):
    def outer_wrapper(wrapper_func):
        def wrapper(
            udtf_proto: relation_proto.CommonInlineUserDefinedTableFunction,
            spark_column_names,
        ) -> SnowparkUDTF | None:
            udf_hash = hash(str(udtf_proto))
            cached_udtf = get_external_udtf_from_cache(udf_hash)

            if cached_udtf:
                if from_register_udtf:
                    session = get_or_create_snowpark_session()
                    session._udtfs[udtf_proto.function_name.lower()] = (
                        cached_udtf,
                        spark_column_names,
                    )

                return cached_udtf

            snowpark_udf = wrapper_func(udtf_proto, spark_column_names)
            cache_external_udtf(udf_hash, snowpark_udf)
            return snowpark_udf

        return wrapper

    return outer_wrapper


def build_expected_types_from_parsed(
    parsed_return: types_proto.DataType,
) -> List[Tuple[str, Any]]:
    """
    Recursively build expected_types from a PySpark StructType schema.
    Each entry is a tuple: (kind, type_marker)
    kind: "scalar", "array", or "struct"
    type_marker: for scalar, a tuple (python_type, marker_dict); for array, (python_type, marker_dict); for struct, dict of fields
    """

    def parse_type_marker(
        typ: types_proto.DataType,
    ) -> Tuple[str, Any]:
        match typ.WhichOneof("kind"):
            case "map":
                key_type = parse_type_marker(typ.map.key_type)
                value_type = parse_type_marker(typ.map.value_type)
                return "scalar", ("dict", {"dict": (key_type, value_type)})
            case "array":
                element_type = parse_type_marker(typ.array.element_type)
                return "array", element_type
            case "struct":
                struct_fields = {
                    sf.name: parse_type_marker(sf.data_type) for sf in typ.struct.fields
                }
                return "struct", struct_fields
            case "string":
                return "scalar", ("str", "string")
            case "integer" | "short" | "long":
                return "scalar", ("int", "int")
            case "float" | "double":
                return "scalar", ("float", "float")
            case "boolean":
                return "scalar", ("bool", "bool")
            case "date":
                return "scalar", ("datetime.date", "date")
            case "timestamp":
                return "scalar", ("datetime.datetime", "timestamp")
            case "binary":
                return "scalar", ("bytes", "binary")
            case "byte":
                # ByteType in Spark represents an 8-bit signed integer (values from -128 to 127), not a bytes type
                return "scalar", ("int", "byte")
            case "decimal":
                # Use Spark's default precision (10) and scale (0) if not specified in the proto
                precision = (
                    typ.decimal.precision if typ.decimal.HasField("precision") else 10
                )
                scale = typ.decimal.scale if typ.decimal.HasField("scale") else 0
                marker = {"type": "decimal", "precision": precision, "scale": scale}
                return "scalar", ("decimal.Decimal", marker)
            case _:
                return "scalar", ("object", "unknown")

    return [parse_type_marker(field.data_type) for field in parsed_return.struct.fields]


def convert_maptype_to_variant(schema: StructType) -> StructType:
    """
    Recursively convert all MapType fields in a StructType (or ArrayType of StructType) to VariantType.
    """
    if isinstance(schema, StructType):
        for field in schema.fields:
            if isinstance(field.datatype, MapType):
                field.datatype = VariantType()
            elif isinstance(field.datatype, StructType):
                convert_maptype_to_variant(field.datatype)
            elif isinstance(field.datatype, ArrayType):
                # If array of struct/map, recurse
                if isinstance(field.datatype.element_type, MapType):
                    field.datatype.element_type = VariantType()
                elif isinstance(field.datatype.element_type, StructType):
                    convert_maptype_to_variant(field.datatype.element_type)
    return schema


def process_return_type(
    return_type: types_proto.DataType,
) -> tuple[list[tuple[str, Any]], DataType, StructType, list[str]]:
    try:
        if return_type.HasField("unparsed"):
            parsed_return = map_type_string_to_proto(
                return_type.unparsed.data_type_string
            )
        else:
            parsed_return = return_type
    except ValueError as e:
        exception = PythonException(
            f"[UDTF_ARROW_TYPE_CAST_ERROR] Error parsing UDTF return type DDL: {e}"
        )
        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
        raise exception
    original_output_schema = proto_to_snowpark_type(parsed_return)
    output_schema = proto_to_snowpark_type(parsed_return)
    # Snowflake UDTF does not support MapType, so we convert it to VariantType.
    output_schema = convert_maptype_to_variant(output_schema)
    if not isinstance(output_schema, StructType):
        exception = PySparkTypeError(
            f"Invalid Python user-defined table function return type. Expect a struct type, but got {parsed_return}"
        )
        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
        raise exception

    expected_types = None
    if is_arrow_enabled_in_udtf() or is_spark_compatible_udtf_mode_enabled():
        expected_types = build_expected_types_from_parsed(parsed_return)

    spark_column_names = [f.name for f in parsed_return.struct.fields]
    return expected_types, original_output_schema, output_schema, spark_column_names


def register_udtf(
    udtf_proto: relation_proto.CommonInlineUserDefinedTableFunction,
) -> SnowparkUDTF:
    udtf_check(udtf_proto)
    session = get_or_create_snowpark_session()
    python_udft = udtf_proto.python_udtf
    (
        expected_types,
        original_output_schema,
        output_schema,
        spark_column_names,
    ) = process_return_type(python_udft.return_type)
    function_name = udtf_proto.function_name

    @cache_external_udtf_wrapper(from_register_udtf=True)
    def _register_udtf(
        udtf_proto: relation_proto.CommonInlineUserDefinedTableFunction,
        spark_column_names,
    ):
        kwargs = {
            "session": session,
            "udtf_proto": udtf_proto,
            "expected_types": expected_types,
            "output_schema": output_schema,
            "packages": global_config.get("snowpark.connect.udf.packages", ""),
            "imports": get_python_udxf_import_files(session),
            "called_from": "register_udtf",
            "is_arrow_enabled": is_arrow_enabled_in_udtf(),
            "is_spark_compatible_udtf_mode_enabled": is_spark_compatible_udtf_mode_enabled(),
        }

        if require_creating_udtf_in_sproc(udtf_proto):
            snowpark_udtf = create_udtf_in_sproc(**kwargs)
        else:
            udtf = create_udtf(**kwargs)
            snowpark_udtf = SnowparkUDTF(
                name=udtf.name,
                input_types=udtf._input_types,
                output_schema=output_schema,
            )

        return snowpark_udtf

    snowpark_udtf = _register_udtf(udtf_proto, spark_column_names)
    # We have to update cached _udtfs here, because function could have been cached in map_common_inline_user_defined_table_function
    session._udtfs[function_name.lower()] = (snowpark_udtf, spark_column_names)
    return snowpark_udtf


def is_spark_compatible_udtf_mode_enabled() -> bool:
    return get_boolean_session_config_param("snowpark.connect.udtf.compatibility_mode")


def is_arrow_enabled_in_udtf() -> bool:  # REINSTATED
    """Check if Arrow is enabled for UDTFs"""
    return get_boolean_session_config_param(
        "spark.sql.execution.pythonUDTF.arrow.enabled"
    )


def map_common_inline_user_defined_table_function(
    rel: relation_proto.CommonInlineUserDefinedTableFunction,
) -> DataFrameContainer:
    udtf_check(rel)
    session = get_or_create_snowpark_session()
    python_udft = rel.python_udtf
    (
        expected_types,
        original_output_schema,
        output_schema,
        spark_column_names,
    ) = process_return_type(python_udft.return_type)

    @cache_external_udtf_wrapper(from_register_udtf=False)
    def _get_udtf(
        udtf_proto: relation_proto.CommonInlineUserDefinedTableFunction,
        spark_column_names,
    ):
        kwargs = {
            "session": session,
            "udtf_proto": udtf_proto,
            "expected_types": expected_types,
            "output_schema": output_schema,
            "packages": global_config.get("snowpark.connect.udf.packages", ""),
            "imports": get_python_udxf_import_files(session),
            "called_from": "map_common_inline_user_defined_table_function",
            "is_arrow_enabled": is_arrow_enabled_in_udtf(),
            "is_spark_compatible_udtf_mode_enabled": is_spark_compatible_udtf_mode_enabled(),
        }

        if require_creating_udtf_in_sproc(udtf_proto):
            snowpark_udtf_or_error = create_udtf_in_sproc(**kwargs)
            if isinstance(snowpark_udtf_or_error, str):
                exception = PythonException(snowpark_udtf_or_error)
                attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
                raise exception
            snowpark_udtf = snowpark_udtf_or_error
        else:
            udtf_or_error = create_udtf(**kwargs)
            if isinstance(udtf_or_error, str):
                exception = PythonException(udtf_or_error)
                attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
                raise exception
            udtf = udtf_or_error
            snowpark_udtf = SnowparkUDTF(
                name=udtf.name,
                input_types=udtf._input_types,
                output_schema=output_schema,
            )
        return snowpark_udtf

    snowpark_udtf = _get_udtf(rel, spark_column_names)
    column_map = ColumnNameMap([], [])
    snowpark_udtf_args = []

    # Set UDTF context when processing arguments to enable struct markers
    with push_udtf_context():
        for arg_exp in rel.arguments:
            (_, snowpark_udtf_arg_tc) = map_single_column_expression(
                arg_exp, column_map, ExpressionTyper.dummy_typer(session)
            )
            snowpark_udtf_arg = snowpark_udtf_arg_tc.col
            snowpark_udtf_args.append(snowpark_udtf_arg)

    df = session.table_function(
        snowpark_udtf.name, *[arg.cast(VariantType()) for arg in snowpark_udtf_args]
    )

    original_types = {}
    for field in original_output_schema.fields:
        original_types[field.name] = field.datatype

    snowpark_column_types = []
    # Replace JSON strings with Python dicts for map columns
    for field in output_schema.fields:
        if isinstance(field.datatype, VariantType):
            col_name = field.name
            if col_name in original_types and isinstance(
                original_types[col_name], MapType
            ):
                original_map_type = original_types[col_name]
                parsed_col = parse_json(col(col_name))
                df = df.with_column(col_name, parsed_col.cast(original_map_type))
                snowpark_column_types.append(original_map_type)
            else:
                df = df.with_column(col_name, parse_json(col(col_name)))
                snowpark_column_types.append(field.datatype)
        else:
            snowpark_column_types.append(field.datatype)

    snowpark_columns = [f.name for f in output_schema.fields]

    return DataFrameContainer.create_with_column_mapping(
        dataframe=df,
        spark_column_names=spark_column_names,
        snowpark_column_names=snowpark_columns,
        snowpark_column_types=snowpark_column_types,
    )
