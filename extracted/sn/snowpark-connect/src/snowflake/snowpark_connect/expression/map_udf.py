#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto

from snowflake import snowpark
from snowflake.snowpark.types import ArrayType, MapType, StructType, VariantType
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
    UdfKind,
    jvm_return_needs_decode,
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
    # Array Type with Timestamps raises an incident when return type is not converted to VariantType.
    # Related JIRA: https://snowflakecomputing.atlassian.net/browse/SNOW-2131897
    if isinstance(original_snowpark_type, (ArrayType, MapType, StructType)):
        return VariantType(), original_snowpark_type

    return original_snowpark_type, original_snowpark_type


def _resolve_udf_kind(function_type: str, udf, inline: bool) -> UdfKind:
    match function_type:
        case "scalar_scala_udf" if isinstance(udf, JavaUdaf):
            return UdfKind.JAVA_UDAF
        case "scalar_scala_udf":
            return UdfKind.SCALA_UDF
        case "python_udf":
            return UdfKind.PYTHON_INLINE if inline else UdfKind.PYTHON_REGISTERED
        case "java_udf":
            return UdfKind.JAVA_SCALAR
        case _:
            raise ValueError(f"Unsupported UDF type {function_type!r}")


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
                kind=UdfKind.JAVA_SCALAR,
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
        return process_udf_in_sproc(**kwargs, kind=UdfKind.PYTHON_REGISTERED)
    else:
        udf_processor = ProcessCommonInlineUserDefinedFunction(**kwargs)
        udf = udf_processor.create_udf()
        udf_kind = _resolve_udf_kind(
            str(udf_proto.WhichOneof("function")), udf, inline=False
        )
        cast_to_original = udf._return_type == VariantType() or (
            udf_kind in (UdfKind.SCALA_UDF, UdfKind.JAVA_UDAF)
            and jvm_return_needs_decode(udf._return_type, original_return_type)
        )
        if isinstance(udf, LazyCreatedScalaUdf):
            snowpark_udf: SnowparkUdfBase = LazySnowparkUdf(
                name=udf.name,
                return_type=udf._return_type,
                original_return_type=original_return_type,
                cast_to_original_return_type=cast_to_original,
                stage_imports=udf.stage_imports,
                inline_payload=udf.inline_payload,
            )
        else:
            snowpark_udf = SnowparkUDF(
                name=udf.name,
                input_types=udf._input_types,
                return_type=udf._return_type,
                original_return_type=original_return_type,
                kind=udf_kind,
                cast_to_original_return_type=cast_to_original,
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
            snowpark_udf = process_udf_in_sproc(**kwargs, kind=UdfKind.PYTHON_INLINE)
        else:
            udf_processor = ProcessCommonInlineUserDefinedFunction(**kwargs)
            udf = udf_processor.create_udf()
            # Inline UDFs are created with concrete call-site types,
            # unlike spark.udf.register UDFs which default to VARIANT inputs.
            udf_kind = _resolve_udf_kind(
                str(udf_proto.WhichOneof("function")), udf, inline=True
            )
            cast_to_original = udf._return_type == VariantType() or (
                udf_kind in (UdfKind.SCALA_UDF, UdfKind.JAVA_UDAF)
                and jvm_return_needs_decode(udf._return_type, original_return_type)
            )
            if udf_kind in (UdfKind.SCALA_UDF, UdfKind.JAVA_UDAF) and isinstance(
                udf, LazyCreatedScalaUdf
            ):
                snowpark_udf: SnowparkUdfBase = LazySnowparkUdf(
                    name=udf.name,
                    return_type=udf._return_type,
                    original_return_type=original_return_type,
                    cast_to_original_return_type=cast_to_original,
                    stage_imports=udf.stage_imports,
                    inline_payload=udf.inline_payload,
                )
            else:
                snowpark_udf = SnowparkUDF(
                    name=udf.name,
                    input_types=udf._input_types,
                    return_type=udf._return_type,
                    original_return_type=original_return_type,
                    kind=udf_kind,
                    cast_to_original_return_type=cast_to_original,
                )
        return snowpark_udf

    snowpark_udf = get_snowpark_udf(udf_proto)

    # The UDF handle owns the full marshalling round-trip (encode args → invoke → decode
    # result), so the inline and registered-SQL (map_unresolved_function) call sites share
    # one path with no per-call-site branching.
    typed_result = snowpark_udf.invoke(
        snowpark_udf_typed_args, column_mapping, get_or_create_snowpark_session()
    )

    name = f"{udf_proto.function_name}({', '.join(snowpark_udf_arg_names)})"
    if get_grouping_by_scala_udf_key() and not isinstance(
        original_return_type, StructType
    ):
        name = (
            "value"
            if global_config.spark_sql_legacy_dataset_nameNonStructGroupingKeyAsValue
            else "key"
        )
    return (name, typed_result)
