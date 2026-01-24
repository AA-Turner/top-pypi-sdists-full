#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.types import ArrayType, MapType, StructType, VariantType
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.type_mapping import proto_to_snowpark_type
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.context import get_grouping_by_scala_udf_key
from snowflake.snowpark_connect.utils.external_udxf_cache import (
    cache_external_udf,
    get_external_udf_from_cache,
)
from snowflake.snowpark_connect.utils.java_stored_procedure import create_java_udf
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.udf_helper import (
    SnowparkUDF,
    infer_snowpark_arguments,
    process_udf_in_sproc,
    require_creating_udf_in_sproc,
    udf_check,
)
from snowflake.snowpark_connect.utils.udf_utils import (
    ProcessCommonInlineUserDefinedFunction,
)
from snowflake.snowpark_connect.utils.udxf_import_utils import (
    get_python_udxf_import_files,
)


def cache_external_udf_wrapper(from_register_udf: bool):
    def outer_wrapper(wrapper_func):
        def wrapper(
            udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
        ) -> SnowparkUDF | None:
            udf_hash = hash(str(udf_proto))
            cached_udf = get_external_udf_from_cache(udf_hash)

            if cached_udf:
                session = get_or_create_snowpark_session()
                function_type = udf_proto.WhichOneof("function")
                # TODO: Align this with SNOW-2316798 after merge
                match function_type:
                    case "scalar_scala_udf":
                        session._udfs[cached_udf.name] = cached_udf
                    case "python_udf" if from_register_udf:
                        session._udfs[udf_proto.function_name.lower()] = cached_udf
                    case "python_udf":
                        pass
                    case "java_udf":
                        session._udfs[udf_proto.function_name.lower()] = cached_udf
                    case _:
                        exception = ValueError(f"Unsupported UDF type: {function_type}")
                        attach_custom_error_code(
                            exception, ErrorCodes.UNSUPPORTED_OPERATION
                        )
                        raise exception

                return cached_udf

            snowpark_udf = wrapper_func(udf_proto)
            cache_external_udf(udf_hash, snowpark_udf)
            return snowpark_udf

        return wrapper

    return outer_wrapper


def process_udf_return_type(
    return_type: types_proto.DataType,
) -> tuple[snowpark.types.DataType, snowpark.types.DataType]:
    """Process UDF return type, handling DDL strings if present.

    Returns a tuple of (processed_type, original_type) where:
    - processed_type: The type to use for UDF registration ((MapType, StructType) -> VariantType)
    - original_type: The original type for result processing
    """
    original_snowpark_type = proto_to_snowpark_type(return_type)

    # Snowflake UDF does not support MapType or StructType, so we convert them to VariantType.
    # We return both the converted type and original type for proper result processing.
    if isinstance(original_snowpark_type, (MapType, StructType)):
        return VariantType(), original_snowpark_type

    return original_snowpark_type, original_snowpark_type


@cache_external_udf_wrapper(from_register_udf=True)
def register_udf(
    udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
) -> SnowparkUDF:
    udf_check(udf_proto)
    match udf_proto.WhichOneof("function"):
        case "python_udf":
            output_type = udf_proto.python_udf.output_type
            processed_return_type, original_return_type = process_udf_return_type(
                output_type
            )
        case "scalar_scala_udf":
            # For Scala UDFs, always use VariantType as the processed type since all Scala UDFs
            # return Variant. The actual type conversion happens after the UDF call.
            output_type = udf_proto.scalar_scala_udf.outputType
            original_return_type = proto_to_snowpark_type(output_type)
            processed_return_type = VariantType()
        case "java_udf":
            has_output_type = udf_proto.java_udf.HasField("output_type")
            session = get_or_create_snowpark_session()
            java_udf = create_java_udf(
                session,
                udf_proto.function_name,
                udf_proto.java_udf.class_name,
            )
            original_return_type = java_udf._return_type
            if has_output_type:
                original_return_type = proto_to_snowpark_type(
                    udf_proto.java_udf.output_type
                )
            udf = SnowparkUDF(
                name=java_udf.name,
                input_types=java_udf._input_types,
                return_type=java_udf._return_type,
                original_return_type=original_return_type,
                cast_to_original_return_type=True,
            )
            session._udfs[udf_proto.function_name.lower()] = udf
            return udf
        case _:
            exception = ValueError(
                f"Unsupported UDF type: {udf_proto.WhichOneof('function')}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
    session = get_or_create_snowpark_session()
    kwargs = {
        "common_inline_user_defined_function": udf_proto,
        "called_from": "register_udf",
        "return_type": processed_return_type,
        "udf_packages": global_config.get("snowpark.connect.udf.packages", ""),
        "udf_imports": get_python_udxf_import_files(session),
        "original_return_type": original_return_type,
    }

    if require_creating_udf_in_sproc(udf_proto):
        return process_udf_in_sproc(**kwargs)
    else:
        udf_processor = ProcessCommonInlineUserDefinedFunction(**kwargs)
        udf = udf_processor.create_udf()
        is_scala_udf = udf_proto.WhichOneof("function") == "scalar_scala_udf"

        udf = SnowparkUDF(
            name=udf.name,
            input_types=udf._input_types,
            return_type=udf._return_type,
            original_return_type=original_return_type,
            cast_to_original_return_type=is_scala_udf
            or udf._return_type == VariantType(),
        )
        session._udfs[udf_proto.function_name.lower()] = udf
        # scala udfs can be also accessed using `udf.name`
        if udf_processor._function_type == "scalar_scala_udf":
            session._udfs[udf.name] = udf
        return udf


def map_common_inline_user_defined_udf(
    exp: expressions_proto.Expression,
    column_mapping: ColumnNameMap,
    typer: ExpressionTyper,
) -> tuple[str, TypedColumn]:
    udf_proto = exp.common_inline_user_defined_function
    udf_check(udf_proto)
    snowpark_udf_arg_names, snowpark_udf_typed_args = infer_snowpark_arguments(
        udf_proto, column_mapping, typer
    )
    input_types = [a.typ for a in snowpark_udf_typed_args]
    match udf_proto.WhichOneof("function"):
        case "python_udf":
            processed_return_type, original_return_type = process_udf_return_type(
                udf_proto.python_udf.output_type
            )
        case "scalar_scala_udf":
            # For Scala UDFs, always use VariantType as the processed type since all Scala UDFs
            # return Variant. The actual type conversion happens after the UDF call.
            original_return_type = proto_to_snowpark_type(
                udf_proto.scalar_scala_udf.outputType
            )
            processed_return_type = VariantType()

    @cache_external_udf_wrapper(from_register_udf=False)
    def get_snowpark_udf(
        udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
    ) -> SnowparkUDF:
        session = get_or_create_snowpark_session()
        kwargs = {
            "common_inline_user_defined_function": udf_proto,
            "input_types": input_types,
            "called_from": "map_common_inline_user_defined_udf",
            "return_type": processed_return_type,
            "udf_packages": global_config.get("snowpark.connect.udf.packages", ""),
            "udf_imports": get_python_udxf_import_files(session),
            "original_return_type": original_return_type,
        }
        if require_creating_udf_in_sproc(udf_proto):
            snowpark_udf = process_udf_in_sproc(**kwargs)
        else:
            udf_processor = ProcessCommonInlineUserDefinedFunction(**kwargs)
            udf = udf_processor.create_udf()
            snowpark_udf = SnowparkUDF(
                name=udf.name,
                input_types=udf._input_types,
                return_type=udf._return_type,
                original_return_type=original_return_type,
            )
        return snowpark_udf

    snowpark_udf = get_snowpark_udf(udf_proto)
    # Determine if we need to cast the result back to the original type
    is_scala_udf = udf_proto.WhichOneof("function") == "scalar_scala_udf"

    # For structured types (arrays, structs, maps), use to_variant instead of cast
    # to ensure proper conversion to VARIANT type for Scala UDFS
    converted_args = []
    for tc in snowpark_udf_typed_args:
        if is_scala_udf and isinstance(tc.typ, (ArrayType, StructType, MapType)):
            converted_args.append(snowpark_fn.to_variant(tc.col))
        else:
            converted_args.append(tc.col)

    udf_call_expr = snowpark_fn.call_udf(snowpark_udf.name, *converted_args)

    # For Scala UDFs, always cast from Variant to the original type
    # For Python UDFs, only cast if the original type was MapType or StructType
    if is_scala_udf:
        # All Scala UDFs return Variant, so we always need to cast back to the original type
        result_expr = snowpark_fn.cast(udf_call_expr, original_return_type)
        result_type = original_return_type

    elif isinstance(original_return_type, (MapType, StructType)) and isinstance(
        processed_return_type, VariantType
    ):
        # Parse JSON and cast back to original type for Python UDFs
        result_expr = snowpark_fn.parse_json(udf_call_expr).cast(original_return_type)
        result_type = original_return_type
    else:
        result_expr = udf_call_expr
        result_type = snowpark_udf.return_type

    name = f"{udf_proto.function_name}({', '.join(snowpark_udf_arg_names)})"
    if get_grouping_by_scala_udf_key() and not isinstance(
        original_return_type, StructType
    ):
        name = (
            "value"
            if global_config.spark_sql_legacy_dataset_nameNonStructGroupingKeyAsValue
            else "key"
        )
    return (name, TypedColumn(result_expr, lambda: [result_type]))
