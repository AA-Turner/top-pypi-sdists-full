#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto

import snowflake.snowpark.functions as snowpark_fn
from snowflake import snowpark
from snowflake.snowpark.types import MapType, StructType, VariantType
from snowflake.snowpark_connect.column_name_handler import ColumnNameMap
from snowflake.snowpark_connect.config import get_artifact_repository, global_config
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.expression.typer import ExpressionTyper
from snowflake.snowpark_connect.type_mapping import proto_to_snowpark_type
from snowflake.snowpark_connect.typed_column import TypedColumn
from snowflake.snowpark_connect.utils.context import get_grouping_by_scala_udf_key
from snowflake.snowpark_connect.utils.java_stored_procedure import create_java_udf
from snowflake.snowpark_connect.utils.java_udaf_utils import JavaUdaf
from snowflake.snowpark_connect.utils.jvm_udf_utils import (
    expand_struct_arg_for_scala_udf,
    is_native_sql_type,
)
from snowflake.snowpark_connect.utils.scala_udf_utils import LazyCreatedScalaUdf
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.spark_session_cache import get_spark_session_cache
from snowflake.snowpark_connect.utils.udf_helper import (
    LazySnowparkUdf,
    SnowparkUDF,
    SnowparkUdfBase,
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
from snowflake.snowpark_connect.utils.variant_utils import scala_udf_arg_to_variant


def cache_external_udf_wrapper(from_register_udf: bool):
    def outer_wrapper(wrapper_func):
        def wrapper(
            udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
        ) -> SnowparkUDF | None:
            udf_hash = hash(str(udf_proto))
            cache = get_spark_session_cache()
            cached_udf = cache.udfs.get_cached(udf_hash)

            if cached_udf:
                function_type = udf_proto.WhichOneof("function")
                # TODO: Align this with SNOW-2316798 after merge
                match function_type:
                    case "scalar_scala_udf":
                        cache.udfs.register(cached_udf.name, cached_udf)
                        if from_register_udf:
                            cache.udfs.register(
                                udf_proto.function_name.lower(), cached_udf
                            )
                    case "python_udf" if from_register_udf:
                        cache.udfs.register(udf_proto.function_name.lower(), cached_udf)
                    case "python_udf":
                        pass
                    case "java_udf":
                        cache.udfs.register(udf_proto.function_name.lower(), cached_udf)
                    case _:
                        exception = ValueError(f"Unsupported UDF type: {function_type}")
                        attach_custom_error_code(
                            exception, ErrorCodes.UNSUPPORTED_OPERATION
                        )
                        raise exception

                return cached_udf

            snowpark_udf = wrapper_func(udf_proto)
            cache.udfs.cache(udf_hash, snowpark_udf)
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
            processed_return_type, original_return_type = process_udf_return_type(
                udf_proto.scalar_scala_udf.outputType
            )
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
            get_spark_session_cache().udfs.register(
                udf_proto.function_name.lower(), udf
            )
            return udf
        case _:
            exception = ValueError(
                f"Unsupported UDF type: {udf_proto.WhichOneof('function')}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
    session = get_or_create_snowpark_session()
    from snowflake.snowpark_connect.utils.udf_utils import _get_resource_constraint

    is_python_udf = udf_proto.WhichOneof("function") == "python_udf"

    kwargs = {
        "common_inline_user_defined_function": udf_proto,
        "called_from": "register_udf",
        "return_type": processed_return_type,
        "udf_packages": global_config.get("snowpark.connect.udf.packages", ""),
        "udf_imports": get_python_udxf_import_files(session),
        "original_return_type": original_return_type,
        "artifact_repository": get_artifact_repository(),
        "resource_constraint": _get_resource_constraint(),
        # SNOW-3381818: for UDFs registered via spark.udf.register, the proto
        # carries no call-site input types so the underlying Snowflake UDF
        # defaults to VARIANT inputs. That round-trip collapses
        # integer-valued FloatType/DoubleType values to Python int
        # (e.g. 1.0 -> 1), which diverges from Spark. We pass per-call type
        # metadata as an extra arg and let the UDF wrapper coerce — see
        # ``create_schema_json_coercion_wrapper``.
        "coerce_via_schema_json": is_python_udf,
    }

    use_sproc = require_creating_udf_in_sproc(udf_proto)
    if use_sproc:
        return process_udf_in_sproc(**kwargs)
    else:
        udf_processor = ProcessCommonInlineUserDefinedFunction(**kwargs)
        udf = udf_processor.create_udf()
        is_scala_udf = udf_proto.WhichOneof("function") == "scalar_scala_udf"

        # Non-native Scala return types (Array, Decimal, Timestamp, …) use RETURNS VARIANT
        # DDL under the hood, so Snowflake returns a JSON string that needs to be cast back.
        cast_to_original = udf._return_type == VariantType() or (
            is_scala_udf and not is_native_sql_type(udf._return_type)
        )
        attach_schema = (is_scala_udf and not isinstance(udf, JavaUdaf)) or (
            is_python_udf and udf_processor._coerce_via_schema_json
        )
        if isinstance(udf, LazyCreatedScalaUdf):
            snowpark_udf: SnowparkUdfBase = LazySnowparkUdf(
                name=udf.name,
                return_type=udf._return_type,
                original_return_type=original_return_type,
                cast_to_original_return_type=cast_to_original,
                attach_schema_json=attach_schema,
                stage_imports=udf.stage_imports,
            )
        else:
            snowpark_udf = SnowparkUDF(
                name=udf.name,
                input_types=udf._input_types,
                return_type=udf._return_type,
                original_return_type=original_return_type,
                cast_to_original_return_type=cast_to_original,
                attach_schema_json=attach_schema,
                is_scala=is_scala_udf,
                is_java_udaf=isinstance(udf, JavaUdaf),
            )
        cache = get_spark_session_cache()
        cache.udfs.register(udf_proto.function_name.lower(), snowpark_udf)
        if udf_processor._function_type == "scalar_scala_udf":
            cache.udfs.register(snowpark_udf.name, snowpark_udf)
        return snowpark_udf


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
            processed_return_type, original_return_type = process_udf_return_type(
                udf_proto.scalar_scala_udf.outputType
            )

    @cache_external_udf_wrapper(from_register_udf=False)
    def get_snowpark_udf(
        udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
    ) -> SnowparkUDF:
        session = get_or_create_snowpark_session()
        from snowflake.snowpark_connect.utils.udf_utils import _get_resource_constraint

        kwargs = {
            "common_inline_user_defined_function": udf_proto,
            "input_types": input_types,
            "called_from": "map_common_inline_user_defined_udf",
            "return_type": processed_return_type,
            "udf_packages": global_config.get("snowpark.connect.udf.packages", ""),
            "udf_imports": get_python_udxf_import_files(session),
            "original_return_type": original_return_type,
            "artifact_repository": get_artifact_repository(),
            "resource_constraint": _get_resource_constraint(),
        }
        use_sproc = require_creating_udf_in_sproc(udf_proto)
        if use_sproc:
            snowpark_udf = process_udf_in_sproc(**kwargs)
        else:
            udf_processor = ProcessCommonInlineUserDefinedFunction(**kwargs)
            udf = udf_processor.create_udf()
            is_scala_udf = udf_proto.WhichOneof("function") == "scalar_scala_udf"

            if is_scala_udf and isinstance(udf, LazyCreatedScalaUdf):
                # cast_to_original_return_type is False here (unlike the register_udf path):
                # this inline call site applies its own native-return handling below, so the
                # flag is unused for Lazy UDFs reached via map_common_inline_user_defined_udf.
                snowpark_udf: SnowparkUdfBase = LazySnowparkUdf(
                    name=udf.name,
                    return_type=udf._return_type,
                    original_return_type=original_return_type,
                    cast_to_original_return_type=False,
                    attach_schema_json=not isinstance(udf, JavaUdaf),
                    stage_imports=udf.stage_imports,
                )
            else:
                snowpark_udf = SnowparkUDF(
                    name=udf.name,
                    input_types=udf._input_types,
                    return_type=udf._return_type,
                    original_return_type=original_return_type,
                    attach_schema_json=is_scala_udf and not isinstance(udf, JavaUdaf),
                    is_scala=is_scala_udf,
                    is_java_udaf=isinstance(udf, JavaUdaf),
                )
        return snowpark_udf

    snowpark_udf = get_snowpark_udf(udf_proto)
    is_scala_udf = udf_proto.WhichOneof("function") == "scalar_scala_udf"

    converted_args = []
    for position, tc in enumerate(snowpark_udf_typed_args):
        if (
            is_scala_udf
            and not snowpark_udf.is_java_udaf
            and snowpark_udf.decomposes_struct_arg(position, tc.typ)
        ):
            # per-field decomposition via shared helper (also used by
            # map_unresolved_function for registered UDFs).
            converted_args.extend(expand_struct_arg_for_scala_udf(tc, column_mapping))
        elif is_scala_udf and not is_native_sql_type(tc.typ):
            # Native scalar args are passed as their native SQL type (matching the native
            # DDL param); only non-native types still go through the VARIANT round-trip.
            converted_args.append(scala_udf_arg_to_variant(tc.col, tc.typ))
        else:
            converted_args.append(tc.col)

    udf_call_expr = snowpark_udf.call(
        converted_args, snowpark_udf_typed_args, get_or_create_snowpark_session()
    )

    # Skip the cast only for truly native return types (BIGINT, VARCHAR, BOOLEAN, etc.)
    # where the SQL DDL already returns the right type directly. For all other types
    # (Decimal, Date, Array, Map, Struct) the DDL uses VARIANT, so we must cast back.
    # Note: for non-native non-struct types (e.g. Date, Timestamp, Decimal),
    # processed_return_type == original_return_type, so the second condition
    # (not is_native_sql_type) is the load-bearing branch that triggers the cast.
    if is_scala_udf:
        if processed_return_type != original_return_type or not is_native_sql_type(
            original_return_type
        ):
            result_expr = snowpark_fn.cast(udf_call_expr, original_return_type)
        else:
            result_expr = udf_call_expr
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
