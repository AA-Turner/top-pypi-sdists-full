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
    LazyPythonUdf,
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
    build_timestamp_return_descriptor,
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

    # MapType/StructType → always VARIANT (no native Snowflake UDF return for these).
    if isinstance(original_snowpark_type, (MapType, StructType)):
        return VariantType(), original_snowpark_type

    # ArrayType → native unless it contains a TimestampType leaf.
    # Arrays with timestamps raise a Snowflake incident (SNOW-2131897) when returned natively,
    # so we keep them as VARIANT.
    if isinstance(original_snowpark_type, ArrayType):
        if build_timestamp_return_descriptor(original_snowpark_type) is not None:
            return VariantType(), original_snowpark_type
        return original_snowpark_type, original_snowpark_type

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

    # For Python UDFs registered via spark.udf.register, use a lazy handle that defers
    # DDL emission until the first call site.  This allows native input types (instead of
    # all-VARIANT) to be emitted when all call-site types are natively representable, which
    # eliminates the schema-JSON coercion wrapper and VARIANT round-trip overhead.
    if is_python_udf:
        cast_to_original = isinstance(processed_return_type, VariantType)
        # The physical Snowflake function name must be session-unique: two Spark
        # sessions can register different UDFs under the same logical name, and the
        # deferred DDL would otherwise CREATE OR REPLACE a single shared function
        # (breaking session isolation). Mirror the Scala lazy path's session suffix.
        # The logical name (function_name.lower()) remains the session-cache key.
        from snowflake.snowpark_connect.utils.context import get_spark_session_id

        logical_name = udf_proto.function_name.lower()
        session_id = get_spark_session_id()
        session_suffix = f"_{session_id.replace('-', '_')}" if session_id else ""
        udf_name = f"{logical_name}{session_suffix}"
        snowpark_udf: SnowparkUdfBase = LazyPythonUdf(
            name=udf_name,
            return_type=processed_return_type,
            original_return_type=original_return_type,
            cast_to_original_return_type=cast_to_original,
            _proto=udf_proto,
            _udf_packages=global_config.get("snowpark.connect.udf.packages", ""),
            _udf_imports=get_python_udxf_import_files(session),
            _artifact_repository=get_artifact_repository(),
            _resource_constraint=_get_resource_constraint(),
            _use_sproc=require_creating_udf_in_sproc(udf_proto),
        )
        cache = get_spark_session_cache()
        cache.udfs.register(logical_name, snowpark_udf)
        return snowpark_udf

    kwargs = {
        "common_inline_user_defined_function": udf_proto,
        "called_from": "register_udf",
        "return_type": processed_return_type,
        "udf_packages": global_config.get("snowpark.connect.udf.packages", ""),
        "udf_imports": get_python_udxf_import_files(session),
        "original_return_type": original_return_type,
        "artifact_repository": get_artifact_repository(),
        "resource_constraint": _get_resource_constraint(),
        "coerce_via_schema_json": False,
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
