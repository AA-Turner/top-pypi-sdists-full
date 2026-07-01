#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

# Some content in this file is derived from Apache Spark. In accordance
# with Apache 2 license, the license for Apache Spark is as follows:
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import inspect
import os
import sys
import tempfile
import threading
from concurrent import futures
from pathlib import Path
from typing import Callable, Dict, List, Optional

import grpc
import jpype
import pyspark
import pyspark.sql.connect.proto.base_pb2 as proto_base
import pyspark.sql.connect.proto.base_pb2_grpc as proto_base_grpc
import pyspark.sql.connect.proto.common_pb2 as common_proto
import pyspark.sql.connect.proto.relations_pb2 as relations_proto
import pyspark.sql.connect.proto.types_pb2 as types_proto
from pyspark import StorageLevel
from pyspark.conf import SparkConf
from pyspark.sql.connect.session import SparkSession

import snowflake.snowpark_connect.proto.control_pb2_grpc as control_grpc
import snowflake.snowpark_connect.tcm as tcm
from snowflake import snowpark
from snowflake.snowpark.types import StructType
from snowflake.snowpark_connect.analyze_plan.map_tree_string import map_tree_string
from snowflake.snowpark_connect.config import (
    route_config_proto,
    set_java_udf_creator_initialized_state,
)
from snowflake.snowpark_connect.control_server import ControlServicer
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import (
    attach_custom_error_code,
    build_grpc_error_response,
)
from snowflake.snowpark_connect.execute_plan.map_execution_command import (
    map_execution_command,
)
from snowflake.snowpark_connect.execute_plan.map_execution_root import (
    map_execution_root,
)
from snowflake.snowpark_connect.relation.map_local_relation import map_local_relation
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.utils import get_semantic_string
from snowflake.snowpark_connect.resources_initializer import initialize_resources
from snowflake.snowpark_connect.server_common import (  # noqa: F401 - re-exported for public API
    _SPARK_CONNECT_GRPC_MAX_MESSAGE_SIZE,
    _client_telemetry_context,
    _disable_protobuf_recursion_limit,
    _get_default_grpc_options,
    _reset_server_run_state,
    _setup_spark_environment,
    _stop_server,
    clear_terminal_op,
    configure_server_url,
    get_client_url,
    get_server_error,
    get_server_running,
    get_server_url,
    get_session,
    get_terminal_op,
    set_grpc_max_message_size,
    set_server_error,
    setup_signal_handlers,
    start_stdin_monitor,
    store_terminal_op,
    validate_startup_parameters,
)
from snowflake.snowpark_connect.type_mapping import (
    map_type_string_to_proto,
    snowpark_to_proto_type,
)
from snowflake.snowpark_connect.utils.artifacts import (
    ArtifactKey,
    assert_artifact_name_is_safe,
    check_checksum,
    generate_artifact_key,
    write_artifact,
    write_class_files_to_stage,
)
from snowflake.snowpark_connect.utils.cache import (
    analyze_memo_clear_session,
    analyze_memo_pop,
    df_cache_map_get,
    df_cache_map_pop,
    df_cache_map_put_if_absent,
    pending_persist_add,
    pending_persist_discard,
)
from snowflake.snowpark_connect.utils.context import (
    clean_request_external_tables,
    clear_context_data,
    get_request_external_tables,
    get_spark_session_id,
    set_is_analyze_plan_request,
    set_spark_session_id,
    set_spark_version,
)
from snowflake.snowpark_connect.utils.env_utils import get_int_from_env
from snowflake.snowpark_connect.utils.internal_query import collect_without_telemetry
from snowflake.snowpark_connect.utils.interrupt import (
    interrupt_all_queries,
    interrupt_queries_with_tag,
    interrupt_query,
)
from snowflake.snowpark_connect.utils.open_telemetry import (
    is_telemetry_enabled,
    otel_attach_context,
    otel_create_context_wrapper,
    otel_create_status,
    otel_detach_context,
    otel_end_root_span,
    otel_flush_telemetry,
    otel_get_current_span,
    otel_get_root_span_context,
    otel_get_status_code,
    otel_get_tracer,
    otel_initialize,
    otel_start_span_as_current,
)
from snowflake.snowpark_connect.utils.profiling import PROFILING_ENABLED, profile_method
from snowflake.snowpark_connect.utils.request_utils import get_or_generate_operation_id
from snowflake.snowpark_connect.utils.scos_query_tag import (
    clear_client_stack_trace,
    store_client_stack_trace,
)
from snowflake.snowpark_connect.utils.session import (
    configure_snowpark_session,
    get_or_create_snowpark_session,
    set_query_tags,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import (
    log_waring_once_storage_level,
    logger,
)
from snowflake.snowpark_connect.utils.span_naming import (
    add_call_site_attributes,
    add_terminal_op_attribute,
    span_name,
    terminal_operation_name,
)
from snowflake.snowpark_connect.utils.spark_session_cache import (
    ArtifactStore,
    clear_spark_session_cache,
    get_spark_session_cache,
)
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
    telemetry,
)
from snowflake.snowpark_connect.utils.xxhash64 import xxhash64_string

# Tracks the Scala-version classpath mode of the currently-running JPype JVM.
# ``None`` means the JVM was started with the legacy/default classpath (no
# Scala-version filtering). ``"2.12"`` / ``"2.13"`` mean the JVM was started
# with explicit Scala-version filtering via ``start_jvm(scala_version=...)``.
# JPype is one-JVM-per-process, so this value can never change after a
# successful ``jpype.startJVM(...)``; we use it to reject mismatched reuse
# attempts with a clear error instead of a confusing ``NoClassDefFoundError``.
_started_jvm_scala_version: str | None = None


def _store_client_stack_trace(client_stack_info):
    """Store client stack trace in thread-local storage"""
    store_client_stack_trace(client_stack_info)


def _clear_client_stack_trace():
    """Clear client stack trace"""
    clear_client_stack_trace()


def _get_client_stack_trace():
    """Get current client stack trace"""
    from snowflake.snowpark_connect.utils.scos_query_tag import get_client_stack_trace

    return get_client_stack_trace()


def _add_client_stack_trace_to_span(span, client_stack):
    """
    Add formatted client stack trace to a specific span.

    Args:
        span: The OpenTelemetry span to add the stack trace attribute to
        client_stack: The client stack trace data (list of frame dicts)
    """
    if not client_stack or not span or not span.is_recording():
        return

    stack_frames = []
    for frame in client_stack:
        if frame.get("file_name") and frame.get("line_number"):
            method = frame.get("method_name", "unknown")
            location = f"{frame.get('file_name')}:{frame.get('line_number')}"
            stack_frames.append(f"{method} at {location}")

    if stack_frames:
        span.set_attribute("client.stack_trace", " <- ".join(stack_frames))


def _process_and_store_client_stack_trace(request, add_to_span: bool = False):
    """
    Extract, store, and optionally add client stack trace to the current span.

    Args:
        request: The gRPC request containing user context with stack trace
        add_to_span: If True, format and add stack trace as span attribute to current span

    Returns:
        The extracted client_stack (or None) for use in ExecutePlan
    """
    # Extract and store client stack trace information for telemetry
    client_stack = _extract_and_log_user_stack_trace(request)
    if client_stack:
        _store_client_stack_trace(client_stack)

    # Cache the computed terminal operation (e.g. "collect", "saveAsTable",
    # "aggregate") for the current request. This is done unconditionally -- even
    # when OpenTelemetry is unavailable -- so other consumers such as query tags
    # can reuse the same user-facing operation name without recomputing it.
    store_terminal_op(terminal_operation_name(request))

    # Set span attribute with formatted stack trace (if requested and available)
    if add_to_span and client_stack:
        root_span_otel_context = otel_get_root_span_context()
        if root_span_otel_context is not None and is_telemetry_enabled():
            current_span = otel_get_current_span()
            if current_span and current_span.is_recording():
                _add_client_stack_trace_to_span(current_span, client_stack)
                add_call_site_attributes(current_span, client_stack)
                add_terminal_op_attribute(current_span, request)

    return client_stack


def _extract_and_log_user_stack_trace(request):
    """
    Extract and log user stack trace information from request extensions.

    Args:
        request: The gRPC request containing user_context.extensions

    Returns:
        List of stack trace frames or None if no traces found
    """
    try:
        from snowflake.snowpark_connect.utils.patch_spark_line_number import (
            extract_stack_trace_from_extensions,
        )

        if hasattr(request, "user_context") and hasattr(
            request.user_context, "extensions"
        ):
            stack_traces = extract_stack_trace_from_extensions(
                request.user_context.extensions
            )

            if stack_traces:
                logger.debug("User code stack trace:")
                for i, frame in enumerate(stack_traces):
                    logger.debug(
                        f"  Frame {i}: {frame.get('method_name', 'unknown')} "
                        f"at {frame.get('file_name', 'unknown')}:{frame.get('line_number', 'unknown')}"
                    )
                return stack_traces  # Return the stack traces for telemetry use
            else:
                logger.debug("No user stack trace information found in request")
                return None
    except Exception as e:
        # Don't let stack trace extraction errors affect the main request
        logger.debug(f"Failed to extract user stack trace: {e}")
        return None


def _handle_exception(context, e: Exception):
    import traceback

    # traceback.print_exc()
    # SNOWFLAKE_SHOW_ERROR_TRACE controls sanitized traceback printing (default: false)
    show_traceback = os.getenv("SNOWFLAKE_SHOW_ERROR_TRACE", "false").lower() == "true"

    if show_traceback:
        # Show detailed traceback (includes error info naturally)
        error_traceback = traceback.format_exc()
        logger.error(error_traceback)
    else:
        # Show only basic error information, no traceback
        logger.error("Error: %s - %s", type(e).__name__, str(e))

    telemetry.report_request_failure(e)
    if tcm.TCM_MODE:
        # spark decoder will catch the error and return it to GS gracefully
        attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
        raise e

    from grpc_status import rpc_status

    rich_status = build_grpc_error_response(e)
    context.abort_with_status(rpc_status.to_status(rich_status))


# Decorator for creating method spans as children of root span
def _with_method_span(method_name):
    """
    Decorator to create a new span as child of root span for gRPC methods and provide it as parent to Snowpark operations.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Get the root span context first
            root_span_otel_context = otel_get_root_span_context()

            # Only proceed if BOTH conditions are true
            if root_span_otel_context is not None and is_telemetry_enabled():
                # Attach the root context first, then create child span
                context_token = otel_attach_context(root_span_otel_context)

                try:
                    tracer = otel_get_tracer(__name__)
                    request = next(
                        (
                            a
                            for a in args
                            if isinstance(
                                a,
                                (
                                    proto_base.ExecutePlanRequest,
                                    proto_base.AnalyzePlanRequest,
                                    proto_base.ConfigRequest,
                                ),
                            )
                        ),
                        None,
                    )
                    method_span_name = (
                        span_name(method_name, request)
                        if request is not None
                        else method_name
                    )

                    # Create span as child of the root span context
                    span_context_mgr = otel_start_span_as_current(
                        tracer, method_span_name
                    )
                    if span_context_mgr:
                        with span_context_mgr as span:
                            try:
                                # Execute the method with the new span as current context
                                return func(*args, **kwargs)

                            except Exception as e:
                                # Record the exception in the span
                                span.record_exception(e)
                                StatusCode = otel_get_status_code()
                                if StatusCode:
                                    status = otel_create_status(
                                        StatusCode.ERROR, str(e)
                                    )
                                    if status:
                                        span.set_status(status)
                                raise
                    else:
                        # No span created, just execute the function
                        return func(*args, **kwargs)

                finally:
                    # Always detach the root context
                    if context_token is not None:
                        otel_detach_context(context_token)
            else:
                # No root context available or OTel not available, execute without span
                return func(*args, **kwargs)

        return wrapper

    return decorator


# Snowflake Connect gRPC Service Implementation
class SnowflakeConnectServicer(proto_base_grpc.SparkConnectServiceServicer):
    def __init__(
        self,
        log_request_fn: Optional[Callable[[bytearray], None]] = None,
    ) -> None:
        self.log_request_fn = log_request_fn
        # Trigger synchronous initialization here, so that we reduce overhead for rpc calls.
        initialize_resources()

    @profile_method
    def ExecutePlan(self, request: proto_base.ExecutePlanRequest, context):
        """Executes a request that contains the query and returns a stream of [[Response]].

        It is guaranteed that there is at least one ARROW batch returned even if the result set is empty.
        """
        logger.debug("ExecutePlan")

        client_stack = _process_and_store_client_stack_trace(request, add_to_span=False)

        if self.log_request_fn is not None:
            self.log_request_fn(request.SerializeToString())

        # TODO: remove session id context when we host this in Snowflake server
        # set the thread-local context of session id
        clear_context_data()
        set_spark_session_id(request.session_id)
        set_spark_version(request.client_type)
        telemetry.initialize_request_summary(request)

        set_query_tags(request.tags)

        # Additional context attachment for Snowpark DataFrame operations
        snowpark_context_token = None
        span = None
        span_context_manager = None
        try:
            root_span_otel_context = otel_get_root_span_context()

            if root_span_otel_context is not None and is_telemetry_enabled():
                snowpark_context_token = otel_attach_context(root_span_otel_context)

                # Create span manually for generator function and make it current
                tracer = otel_get_tracer(__name__)
                span_context_manager = otel_start_span_as_current(
                    tracer, span_name("ExecutePlan", request)
                )
                span = None
                if span_context_manager:
                    span = (
                        span_context_manager.__enter__()
                    )  # Start the span context AND make it current
                    # Add stack trace to this manually created span
                    _add_client_stack_trace_to_span(span, client_stack)
                    add_call_site_attributes(span, client_stack)
                    add_terminal_op_attribute(span, request)

            result_iter = iter(())
            match request.plan.WhichOneof("op_type"):
                case "root":
                    logger.debug("ROOT")
                    result_iter = map_execution_root(request)
                case "command":
                    logger.debug("COMMAND")
                    command_result = map_execution_command(request)
                    if command_result is not None:
                        result_iter = iter([command_result])

            yield from result_iter
            yield proto_base.ExecutePlanResponse(
                session_id=request.session_id,
                operation_id=get_or_generate_operation_id(request),
                result_complete=proto_base.ExecutePlanResponse.ResultComplete(),
            )
        except Exception as e:
            if span:
                span.record_exception(e)
                StatusCode = otel_get_status_code()
                if StatusCode:
                    status = otel_create_status(StatusCode.ERROR, str(e))
                    if status:
                        span.set_status(status)
            _handle_exception(context, e)
        finally:
            analyze_memo_clear_session(request.session_id)
            if span_context_manager:
                span_context_manager.__exit__(None, None, None)  # End the span
            if snowpark_context_token is not None:
                otel_detach_context(snowpark_context_token)
            # Clear client stack trace and cached terminal op when request is done
            _clear_client_stack_trace()
            clear_terminal_op()
            otel_flush_telemetry()
            self._cleanup_external_tables()
            telemetry.send_request_summary_telemetry()

    @profile_method
    @_with_method_span("AnalyzePlan")
    def AnalyzePlan(self, request: proto_base.AnalyzePlanRequest, context):
        """Analyzes a query and returns a [[AnalyzeResponse]] containing metadata about the query."""
        logger.debug(f"AnalyzePlan: {request.WhichOneof('analyze')}")

        _process_and_store_client_stack_trace(request, add_to_span=True)

        if self.log_request_fn is not None:
            self.log_request_fn(request.SerializeToString())

        try:
            # TODO: remove session id context when we host this in Snowflake server
            # set the thread-local context of session id
            clear_context_data()
            set_spark_session_id(request.session_id)
            set_spark_version(request.client_type)
            set_is_analyze_plan_request(True)
            telemetry.initialize_request_summary(request)
            match request.WhichOneof("analyze"):
                case "schema":
                    result = map_relation(request.schema.plan.root)

                    from snowflake.snowpark_connect.relation.read.metadata_utils import (
                        without_hidden_columns,
                    )

                    if result.has_zero_columns():
                        schema = proto_base.AnalyzePlanResponse.Schema(
                            schema=types_proto.DataType(
                                **snowpark_to_proto_type(
                                    StructType([]),
                                )
                            )
                        )
                    else:
                        filtered_result = without_hidden_columns(result)
                        filtered_df = filtered_result.dataframe

                        schema = proto_base.AnalyzePlanResponse.Schema(
                            schema=types_proto.DataType(
                                **snowpark_to_proto_type(
                                    filtered_df.schema,
                                    filtered_result.column_map,
                                    filtered_df,
                                )
                            )
                        )

                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        schema=schema,
                    )
                case "tree_string":
                    return map_tree_string(request)
                case "is_local":
                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        is_local=proto_base.AnalyzePlanResponse.IsLocal(is_local=False),
                    )
                case "ddl_parse":
                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        ddl_parse=proto_base.AnalyzePlanResponse.DDLParse(
                            parsed=map_type_string_to_proto(
                                request.ddl_parse.ddl_string
                            )
                        ),
                    )
                case "get_storage_level":
                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        get_storage_level=proto_base.AnalyzePlanResponse.GetStorageLevel(
                            storage_level=common_proto.StorageLevel(
                                use_disk=True, use_memory=True
                            )
                        ),
                    )
                case "persist":
                    plan_id = request.persist.relation.common.plan_id
                    # Spark Connect's persist() is lazy: it marks the plan for caching
                    # but does no work until the first action. Record the plan as
                    # pending; map_relation resolves and materializes it (cache_result)
                    # on the first ExecutePlan resolution. Skip if already materialized.
                    key = (request.session_id, plan_id)
                    if df_cache_map_get(key) is None:
                        pending_persist_add(key)

                    storage_level = request.persist.storage_level
                    if storage_level != StorageLevel.DISK_ONLY:
                        log_waring_once_storage_level(storage_level)

                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        persist=proto_base.AnalyzePlanResponse.Persist(),
                    )
                case "unpersist":
                    plan_id = request.unpersist.relation.common.plan_id
                    # unpersist the cached plan
                    df_cache_map_pop((request.session_id, plan_id))
                    analyze_memo_pop((request.session_id, plan_id))
                    pending_persist_discard((request.session_id, plan_id))

                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        unpersist=proto_base.AnalyzePlanResponse.Unpersist(),
                    )
                case "explain":
                    # Snowflake only exposes simplified execution plans, similar to Spark's optimized logical plans.
                    # Snowpark provides the execution plan IFF the dataframe maps to a single query.
                    # TODO: Do we need to return a Spark-like plan?
                    result = map_relation(request.explain.plan.root)
                    snowpark_df = result.dataframe
                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        explain=proto_base.AnalyzePlanResponse.Explain(
                            explain_string=snowpark_df._explain_string()
                        ),
                    )
                case "spark_version":
                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        spark_version=proto_base.AnalyzePlanResponse.SparkVersion(
                            version=pyspark.__version__
                        ),
                    )
                case "same_semantics":
                    target_queries_hash = xxhash64_string(
                        get_semantic_string(request.same_semantics.target_plan.root)
                    )
                    other_queries_hash = xxhash64_string(
                        get_semantic_string(request.same_semantics.other_plan.root)
                    )
                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        same_semantics=proto_base.AnalyzePlanResponse.SameSemantics(
                            result=target_queries_hash == other_queries_hash
                        ),
                    )
                case "semantic_hash":
                    queries_str = get_semantic_string(request.semantic_hash.plan.root)
                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        semantic_hash=proto_base.AnalyzePlanResponse.SemanticHash(
                            result=xxhash64_string(queries_str)
                            & 0x7FFFFFFF  # need a 32 bit int here.
                        ),
                    )
                case "is_streaming":
                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        is_streaming=proto_base.AnalyzePlanResponse.IsStreaming(
                            is_streaming=False
                        ),
                    )
                case "input_files":
                    files = []
                    if request.input_files.plan.root.HasField("read"):
                        files = _get_files_metadata(
                            request.input_files.plan.root.read.data_source
                        )
                    elif request.input_files.plan.root.HasField("join"):
                        left_files = _get_files_metadata(
                            request.input_files.plan.root.join.left.read.data_source
                        )
                        right_files = _get_files_metadata(
                            request.input_files.plan.root.join.right.read.data_source
                        )
                        files = left_files + right_files
                    return proto_base.AnalyzePlanResponse(
                        session_id=request.session_id,
                        input_files=proto_base.AnalyzePlanResponse.InputFiles(
                            files=list(set(files))
                        ),
                    )
                case _:
                    exception = SnowparkConnectNotImplementedError(
                        f"ANALYZE PLAN NOT IMPLEMENTED:\n{request}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception
        except Exception as e:
            _handle_exception(context, e)
        finally:
            # Clear client stack trace and cached terminal op when request is done
            _clear_client_stack_trace()
            clear_terminal_op()
            otel_flush_telemetry()
            self._cleanup_external_tables()
            telemetry.send_request_summary_telemetry()

    @staticmethod
    def Config(
        request: proto_base.ConfigRequest,
        context,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        """Update or fetch the configurations and returns a [[ConfigResponse]] containing the result."""
        logger.debug("Config")

        try:
            clear_context_data()
            set_spark_session_id(request.session_id)
            set_spark_version(request.client_type)
            telemetry.initialize_request_summary(request)
            return route_config_proto(request, get_or_create_snowpark_session())
        except Exception as e:
            _handle_exception(context, e)
        finally:
            otel_flush_telemetry()
            telemetry.send_request_summary_telemetry()

    def AddArtifacts(self, request_iterator, context):
        """Add artifacts to the session and returns a [[AddArtifactsResponse]] containing metadata about
        the added artifacts.
        """
        logger.debug("AddArtifacts")

        session: snowpark.Session = get_or_create_snowpark_session()
        response: dict[str, proto_base.AddArtifactsResponse.ArtifactSummary] = {}
        artifact_hashes_to_cache: set[ArtifactKey] = set()

        def _try_handle_local_relation(
            artifact_name: str, data: bytes, artifacts_store: ArtifactStore
        ):
            """
            Attempt to deserialize the artifact data to a LocalRelation protobuf message.
            LocalRelation messages represent in-memory data that should be materialized
            in temporary table in Snowflake rather than stored as file artifact.
             - If successful: creates a temporary table and caches the DataFrame in `df_cache_map`
             - If unsuccessful: falls back to storing as a regular file artifact
            """

            is_likely_local_relation = artifact_name.startswith(
                "cache/"
            )  # heuristic to identify local relations

            def _handle_regular_artifact():
                filepath = write_artifact(
                    session,
                    get_spark_session_id(),
                    artifact_name,
                    data,
                    overwrite=True,
                )
                artifacts_store.set_filename(artifact_name, filepath)

            if is_likely_local_relation:
                try:
                    l_relation = relations_proto.LocalRelation()
                    l_relation.ParseFromString(data)
                    relation = relations_proto.Relation(local_relation=l_relation)
                    df_cache_map_put_if_absent(
                        (get_spark_session_id(), artifact_name.replace("cache/", "")),
                        lambda: map_local_relation(relation),  # noqa: B023
                    )
                except Exception as e:
                    logger.warning("Failed to put df into cache: %s", str(e))
                    # fallback - treat as regular artifact
                    _handle_regular_artifact()
            else:
                # Not a LocalRelation - treat as regular artifact
                _handle_regular_artifact()

        # Spark sends artifacts as iterators that are either chunked or a full batch.
        #
        # Chunked artifacts start with a "begin_chunk" followed by a series of "chunk"
        # messages. The "chunk" messages do not contain a name, so we store the name
        # in `current_name` so we can append all the chunks to the same object.
        # Chunked artifacts are written incrementally as gzip files to reduce memory
        # issues.
        #
        # Batch artifacts are sent as a single "batch" message containing a list of
        # artifacts. We do not need to keep track of the name since it is included in
        # each artifact.

        for request in request_iterator:
            clear_context_data()
            set_spark_session_id(request.session_id)
            set_spark_version(request.client_type)
            artifacts_store = get_spark_session_cache().artifacts_store

            match request.WhichOneof("payload"):
                case "begin_chunk":
                    current_name = request.begin_chunk.name
                    current_chunk = {
                        "name": current_name,
                        "num_chunks": request.begin_chunk.num_chunks,
                        "current_chunk_index": 1,
                        "artifact_key": generate_artifact_key(
                            current_name, request.begin_chunk.initial_chunk.data
                        ),
                    }
                    artifacts_store.assert_no_duplicate_filename(current_name)

                    if current_name.startswith("cache/"):
                        current_chunk["cache"] = bytearray(
                            request.begin_chunk.initial_chunk.data
                        )
                    else:
                        filepath = write_artifact(
                            session,
                            get_spark_session_id(),
                            current_name,
                            request.begin_chunk.initial_chunk.data,
                            overwrite=True,
                        )
                        artifacts_store.set_filename(current_name, filepath)
                    artifacts_store.set_current_chunk(current_chunk)
                    response[
                        current_name
                    ] = proto_base.AddArtifactsResponse.ArtifactSummary(
                        name=current_name,
                        is_crc_successful=check_checksum(
                            request.begin_chunk.initial_chunk.data,
                            request.begin_chunk.initial_chunk.crc,
                        ),
                    )
                case "chunk":
                    current_chunk = artifacts_store.get_current_chunk()
                    if current_chunk is None:
                        exception = ValueError(
                            f"Received 'chunk' for session_id '{request.session_id}' without a prior 'begin_chunk'."
                        )
                        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
                        raise exception

                    current_name = current_chunk["name"]
                    current_chunk["current_chunk_index"] += 1

                    artifact_key = current_chunk["artifact_key"].append_chunk_hash(
                        request.chunk.data
                    )
                    current_chunk["artifact_key"] = artifact_key

                    if current_name.startswith("cache/"):
                        current_chunk["cache"].extend(request.chunk.data)
                    else:
                        filepath = write_artifact(
                            session,
                            get_spark_session_id(),
                            current_name,
                            request.chunk.data,
                        )
                        artifacts_store.assert_filename_matches(current_name, filepath)

                    if (
                        current_chunk["current_chunk_index"]
                        == current_chunk["num_chunks"]
                    ):
                        if current_name.startswith("cache/"):
                            _try_handle_local_relation(
                                current_name,
                                bytes(current_chunk["cache"]),
                                artifacts_store,
                            )

                        if artifacts_store.is_cached(artifact_key):
                            removed = artifacts_store.remove_filename(current_name)
                            if removed:
                                assert_artifact_name_is_safe(
                                    session.session_id,
                                    get_spark_session_id(),
                                    current_name,
                                )
                                Path(removed).unlink(missing_ok=True)
                        else:
                            artifact_hashes_to_cache.add(artifact_key)

                        artifacts_store.set_current_chunk(None)

                    response[
                        current_name
                    ] = proto_base.AddArtifactsResponse.ArtifactSummary(
                        name=current_name,
                        is_crc_successful=(
                            current_name not in response
                            or response[current_name].is_crc_successful
                        )
                        and check_checksum(request.chunk.data, request.chunk.crc),
                    )
                case "batch":
                    for artifact in request.batch.artifacts:
                        data = artifact.data.data
                        artifact_key = generate_artifact_key(artifact.name, data)
                        if artifacts_store.is_cached(artifact_key):
                            removed = artifacts_store.remove_filename(artifact.name)
                            if removed:
                                assert_artifact_name_is_safe(
                                    session.session_id,
                                    get_spark_session_id(),
                                    artifact.name,
                                )
                                Path(removed).unlink(missing_ok=True)
                        else:
                            _try_handle_local_relation(
                                artifact.name, data, artifacts_store
                            )
                            artifact_hashes_to_cache.add(artifact_key)

                        response[
                            artifact.name
                        ] = proto_base.AddArtifactsResponse.ArtifactSummary(
                            name=artifact.name,
                            is_crc_successful=check_checksum(
                                artifact.data.data, artifact.data.crc
                            ),
                        )
                case _:
                    exception = ValueError(
                        f"Unexpected payload type in AddArtifacts: {request.WhichOneof('payload')}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception

        # if current chunk is still not finished, just return here
        # This should only happen in TCM since we have to send request via rest one by one so current chunk cannot be
        # finished in one iteration
        if artifacts_store.has_current_chunk():
            return proto_base.AddArtifactsResponse(artifacts=list(response.values()))

        class_files: dict[str, str] = {}
        spark_session_id = get_spark_session_id()

        with artifacts_store.writer() as artifact_writer:
            pending_artifacts = artifact_writer.drain_filenames()

            for name, filepath in pending_artifacts.items():
                if name.endswith(".class"):
                    # name is <dir>/<package>/<class_name>
                    # we don't need the dir name, but require the package, so only remove dir
                    if os.name != "nt":
                        class_files[name.split("/", 1)[-1]] = filepath
                    else:
                        class_files[name.split("\\", 1)[-1]] = filepath
                    continue
                session.file.put(
                    filepath,
                    session.get_session_stage(),
                    auto_compress=False,
                    overwrite=True,
                    source_compression="GZIP" if name.endswith(".gz") else "NONE",
                )

                if name.startswith("cache"):
                    continue

                # Add only files marked to be used in user generated Python UDFs.
                cached_name = f"{session.get_session_stage()}/{filepath.split('/')[-1]}"
                if not name.startswith("pyfiles") and artifact_writer.has_python_file(
                    cached_name
                ):
                    artifact_writer.remove_python_file(cached_name)
                elif name.startswith("pyfiles"):
                    artifact_writer.add_python_file(cached_name)

                if name.startswith("jars/"):
                    artifact_writer.add_jar(cached_name)
                    # Recreate the Java procedure to reload jars
                    set_java_udf_creator_initialized_state(False)
                elif not name.startswith("pyfiles"):
                    artifact_writer.add_import_file(cached_name)

                # Remove temporary stored files which are put on the stage
                assert_artifact_name_is_safe(session.session_id, spark_session_id, name)
                os.remove(filepath)

            if class_files:
                jar_name = write_class_files_to_stage(
                    session, spark_session_id, class_files
                )
                artifact_writer.add_jar(jar_name)

            if any(not name.startswith("cache") for name in pending_artifacts.keys()):
                clear_spark_session_cache(get_spark_session_id())

        if artifact_hashes_to_cache:
            artifacts_store.cache_hashes(artifact_hashes_to_cache)

        return proto_base.AddArtifactsResponse(artifacts=list(response.values()))

    def ArtifactStatus(self, request, context):
        """Check statuses of artifacts in the session and returns them in a [[ArtifactStatusesResponse]]"""
        logger.debug("ArtifactStatus")

        clear_context_data()
        set_spark_session_id(request.session_id)
        set_spark_version(request.client_type)
        session: snowpark.Session = get_or_create_snowpark_session()

        if os.name != "nt":
            tmp_path = f"/tmp/sas-{session.session_id}/{get_spark_session_id()}"
        else:
            tmp_path = f"{tempfile.gettempdir()}/sas-{session.session_id}/{get_spark_session_id()}"

        def _is_local_relation_cached(name: str) -> bool:
            if name.startswith("cache/"):
                hash = name.replace("cache/", "")
                cached_df = df_cache_map_get((get_spark_session_id(), hash))
                return cached_df is not None
            return False

        files = []
        for _, _, filenames in os.walk(tmp_path):
            for filename in filenames:
                files.append(filename)
        if len(files) == 0:
            statuses = {
                name: proto_base.ArtifactStatusesResponse.ArtifactStatus(
                    exists=_is_local_relation_cached(name)
                )
                for name in request.names
            }
        else:
            statuses = {
                name: proto_base.ArtifactStatusesResponse.ArtifactStatus(
                    exists=(
                        _is_local_relation_cached(name)
                        or any(name.split("/")[-1] in file for file in files)
                    )
                )
                for name in request.names
            }
        return proto_base.ArtifactStatusesResponse(statuses=statuses)

    def Interrupt(self, request: proto_base.InterruptRequest, context):
        """Interrupts running executions"""
        logger.debug("Interrupt")
        telemetry.initialize_request_summary(request)
        # SAS doesn't support operation ids in the same way as spark, so
        # instead of using operation ids, we're relying on Snowflake query ids here, meaning that:
        # - The list of returned interrupted_ids contains query ids of interrupted jobs, instead of their operation ids
        # - INTERRUPT_TYPE_OPERATION_ID interrupt type expects a Snowflake query id instead of an operation id

        try:
            match request.interrupt_type:
                case proto_base.InterruptRequest.InterruptType.INTERRUPT_TYPE_ALL:
                    interrupted_ids = interrupt_all_queries()
                case proto_base.InterruptRequest.InterruptType.INTERRUPT_TYPE_TAG:
                    interrupted_ids = interrupt_queries_with_tag(request.operation_tag)
                case proto_base.InterruptRequest.InterruptType.INTERRUPT_TYPE_OPERATION_ID:
                    interrupted_ids = interrupt_query(request.operation_id)
                case _:
                    exception = SnowparkConnectNotImplementedError(
                        f"INTERRUPT NOT IMPLEMENTED:\n{request}"
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.UNSUPPORTED_OPERATION
                    )
                    raise exception

            return proto_base.InterruptResponse(
                session_id=request.session_id,
                interrupted_ids=interrupted_ids,
            )
        except Exception as e:
            _handle_exception(context, e)
        finally:
            telemetry.send_request_summary_telemetry()

    def ReattachExecute(self, request: proto_base.ReattachExecuteRequest, context):
        """Reattach to an existing reattachable execution.
        The ExecutePlan must have been started with ReattachOptions.reattachable=true.
        If the ExecutePlanResponse stream ends without a ResultComplete message, there is more to
        continue. If there is a ResultComplete, the client should use ReleaseExecute with
        """
        logger.debug("ReattachExecute")

        exception = SnowparkConnectNotImplementedError(
            "Spark client has detached, please resubmit request. In a future version, the server will be support the reattach."
        )
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception

    def ReleaseExecute(self, request: proto_base.ReleaseExecuteRequest, context):
        """Release an reattachable execution, or parts thereof.
        The ExecutePlan must have been started with ReattachOptions.reattachable=true.
        Non reattachable executions are released automatically and immediately after the ExecutePlan
        RPC and ReleaseExecute may not be used.
        """
        try:
            logger.debug("ReleaseExecute")
            return proto_base.ReleaseExecuteResponse(
                session_id=request.session_id,
                # ReleaseExecuteResponse expects either operation_id or None
                operation_id=request.operation_id,
            )
        except Exception as e:
            _handle_exception(context, e)

    def _cleanup_external_tables(self):
        external_tables = get_request_external_tables()
        if not external_tables:
            return
        session: snowpark.Session = get_or_create_snowpark_session()
        for table in external_tables:
            try:
                session.sql(f"DROP EXTERNAL TABLE IF EXISTS {table}").collect()
            except Exception as e:
                logger.warning(f"Failed to drop external table {table}: {e}")
        clean_request_external_tables()

    # TODO: These are required in Spark 4.x.
    # def ReleaseSession(self, request, context):
    #     """Release a session.
    #     All the executions in the session will be released. Any further requests for the session with
    #     that session_id for the given user_id will fail. If the session didn't exist or was already
    #     released, this is a noop.
    #     """
    #     logger.info("ReleaseSession")
    #     return super().ReleaseSession(request, context)
    #
    # def FetchErrorDetails(self, request, context):
    #     """FetchErrorDetails retrieves the matched exception with details based on a provided error id."""
    #     logger.info("FetchErrorDetails")
    #     return super().FetchErrorDetails(request, context)


def _serve(
    stop_event: Optional[threading.Event] = None,
    session: Optional[snowpark.Session] = None,
    app_name: str | None = None,
):
    server_running = get_server_running()
    # TODO: factor out the Snowflake connection code.
    server = None
    # Track job completion status for telemetry
    server_exit_code = 0
    server_error = None
    server_error_type = None
    try:
        config_snowpark()

        if session is None:
            session = get_or_create_snowpark_session()
        else:
            # If a session is passed in, explicitly call config session to be consistent with sessions created
            # under the hood.
            # SNOW-3517484: always run configure to keep non-ALTER setup in sync;
            # ALTER SESSION deduping is handled inside configure_snowpark_session.
            configure_snowpark_session(session)

        _register_snowpark_connect_session(session, app_name=app_name)

        if tcm.TCM_MODE:
            # No need to start grpc server in TCM
            return

        server_options = _get_default_grpc_options()
        max_workers = get_int_from_env("SPARK_CONNECT_SERVER_GRPC_MAX_WORKERS", 10)

        # cProfile doesn't work correctly with multiple threads
        max_workers = 1 if PROFILING_ENABLED else max_workers

        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            options=server_options,
        )

        control_servicer = ControlServicer(session)
        proto_base_grpc.add_SparkConnectServiceServicer_to_server(
            SnowflakeConnectServicer(control_servicer.log_spark_connect_batch),
            server,
        )
        control_grpc.add_ControlServiceServicer_to_server(control_servicer, server)
        server_url = get_server_url()
        server.add_insecure_port(server_url)
        logger.info(f"Starting Snowpark Connect server on {server_url}...")
        server.start()
        server_running.set()
        logger.info("Snowpark Connect server started!")
        telemetry.send_server_started_telemetry()

        if stop_event is not None:
            # start a background thread to listen for stop event and terminate the server
            threading.Thread(
                target=_stop_server, args=(stop_event, server), daemon=True
            ).start()

        server.wait_for_termination()
    except Exception as e:
        set_server_error(True)
        server_running.set()  # unblock any client sessions
        if "Invalid connection_name" in str(e) and "known ones are" in str(e):
            logger.error(
                "Could not find a valid connection in connections.toml. "
                "Please either:\n"
                "  1. Create a connection named 'spark-connect', or\n"
                "  2. Set 'default_connection_name' in your connections.toml, or\n"
                "  3. Create a connection named 'default'"
            )
        else:
            logger.error("Error starting up Snowpark Connect server", exc_info=True)
        attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
        # Capture error info for telemetry
        server_exit_code = 1
        server_error = str(e)
        server_error_type = type(e).__name__
        raise e
    finally:
        # Send job completion telemetry on every server shutdown.
        telemetry.send_job_completion_telemetry(
            exit_code=server_exit_code,
            error=server_error,
            error_type=server_error_type,
        )
        # Flush the telemetry queue
        telemetry.shutdown()
        # End the root span when server shuts down completely
        otel_end_root_span()


def _register_snowpark_connect_session(
    session: snowpark.Session,
    app_name: str | None = None,
) -> None:
    """Register this Snowpark Connect session with Snowflake.

    Calls the SNOWFLAKE.SNOWPARK_CONNECT.REGISTER_SNOWPARK_CONNECT_SESSION system
    function, which records the session in Snowflake's internal SCOS application
    registry. The function uses CURRENT_SESSION() internally to identify the
    Snowflake session.

    Two-phase submit path:
        When running inside a snowpark-submit SPCS container, the env var
        SNOWPARK_SUBMIT_SPARK_APPLICATION_ID carries the UUID returned by the
        client-side REGISTER_PENDING_SNOWPARK_SUBMIT_JOB call (phase-1). Passing
        that UUID as the second argument tells the system function to update the
        existing pending SparkApplicationDPO row rather than create a new one.
        In this case arg 0 (app_name) is ignored by the system function — the
        display name was already recorded during phase-1.

    Args:
        session: The Snowpark session to register.
        app_name: Optional application name (used only when no pending UUID is
            present, i.e. non-submit flows such as local dev or notebooks).

    Silently logs a warning if the function is not available (e.g., older deployments).
    """
    logger.debug(
        f"Registering Snowpark Connect session for session {session.session_id}"
    )
    spark_application_id = os.environ.get("SNOWPARK_SUBMIT_SPARK_APPLICATION_ID")
    try:
        if spark_application_id:
            # Phase-2 registration: update the pending DPO row created by the
            # submit CLI. arg 0 (app_name) is ignored by the system function when
            # a pending UUID is supplied — the display name was set during phase-1.
            escaped_id = spark_application_id.replace("'", "''")
            sql = f"SELECT SNOWFLAKE.SNOWPARK_CONNECT.REGISTER_SNOWPARK_CONNECT_SESSION(NULL, '{escaped_id}')"
        elif app_name is not None:
            escaped = app_name.replace("'", "''")
            sql = f"SELECT SNOWFLAKE.SNOWPARK_CONNECT.REGISTER_SNOWPARK_CONNECT_SESSION('{escaped}')"
        else:
            sql = (
                "SELECT SNOWFLAKE.SNOWPARK_CONNECT.REGISTER_SNOWPARK_CONNECT_SESSION()"
            )
        collect_without_telemetry(session.sql(sql), block=False)
        logger.debug(
            "Fired async registration for Snowpark Connect session "
            "(spark_application_id=%s)",
            spark_application_id,
        )
    except Exception:
        logger.warning(
            "Failed to register Snowpark Connect session "
            "(SNOWFLAKE.SNOWPARK_CONNECT.REGISTER_SNOWPARK_CONNECT_SESSION may not be available)"
        )


def config_snowpark() -> None:
    """
    Some snowpark configs required by SAS.
    """

    # Enable structType. Require snowpark 1.27.0 or snowpark main branch after commit 888cec55c4
    import snowflake.snowpark.context as context

    context._use_structured_type_semantics = True
    context._is_snowpark_connect_compatible_mode = True


def _validate_scala_version(scala_version: str | None) -> str | None:
    """Validate an optional Scala-version argument.

    Returns ``None`` unchanged. Returns ``"2.12"`` / ``"2.13"`` unchanged.
    Raises ``ValueError`` (annotated with ``ErrorCodes.INVALID_CONFIG_VALUE``)
    for any other value.
    """
    if scala_version is None or scala_version in ("2.12", "2.13"):
        return scala_version
    exception = ValueError(
        f"Unsupported scala_version: {scala_version!r}. Must be '2.12' or '2.13'."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
    raise exception


def _format_scala_classpath_mode(scala_version: str | None) -> str:
    if scala_version is None:
        return "the default classpath"
    return f"Scala {scala_version}"


def _ensure_started_jvm_matches_scala_version(scala_version: str | None) -> None:
    """Reject reuse of an already-started JVM in a different Scala-version mode.

    JPype only allows one JVM per process, so if the JVM was started in (e.g.)
    default mode and a caller now asks for Scala 2.13, we cannot rebuild the
    classpath. Fail fast with a clear error rather than letting ``JClass``
    lookups blow up later with ``NoClassDefFoundError``.
    """
    if _started_jvm_scala_version == scala_version:
        return
    current_mode = _format_scala_classpath_mode(_started_jvm_scala_version)
    requested_mode = _format_scala_classpath_mode(scala_version)
    exception = RuntimeError(
        f"JVM already started with {current_mode}. "
        f"Cannot switch to {requested_mode} in the same process."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
    raise exception


def _filter_jars_by_scala_version(
    jar_paths: list[Path], scala_version: str
) -> list[Path]:
    """Filter JAR paths to drop the opposite Scala binary version.

    Handles two naming conventions:
      - Cross-built artifacts: ``*_2.12-*.jar`` / ``*_2.13-*.jar``
      - Scala runtime jars:    ``scala-library-2.12.18.jar`` /
        ``scala-library-2.13.16.jar``
    """
    if scala_version == "2.12":
        exclude_cross = "_2.13-"
        exclude_runtime = "-2.13."
    elif scala_version == "2.13":
        exclude_cross = "_2.12-"
        exclude_runtime = "-2.12."
    else:
        logger.warning(
            f"Unexpected scala_version {scala_version!r} in JAR filtering; "
            f"returning all JARs"
        )
        return jar_paths

    scala_runtime_prefixes = (
        "scala-library-",
        "scala-compiler-",
        "scala-reflect-",
    )

    filtered: list[Path] = []
    excluded_count = 0
    for jar_path in jar_paths:
        name = jar_path.name
        if exclude_cross in name:
            excluded_count += 1
            logger.debug(f"Excluding JAR for opposite Scala version: {name}")
        elif (
            any(name.startswith(prefix) for prefix in scala_runtime_prefixes)
            and exclude_runtime in name
        ):
            excluded_count += 1
            logger.debug(f"Excluding Scala runtime JAR for opposite version: {name}")
        else:
            filtered.append(jar_path)

    logger.info(
        f"Scala {scala_version} JAR filter: "
        f"{len(filtered)} included, {excluded_count} excluded"
    )
    return filtered


# Scala 2.13 jars shipped under ``src/snowflake/snowpark_connect/includes/jars/``
# that replace their 2.12 counterparts in the deps packages when execute_jar
# opts into Scala 2.13. ``sas-scala-udf_2.13-*.jar`` is intentionally omitted —
# it lives on the stage-side Scala UDF upload path
# (``resources_initializer.py``), not the local JVM classpath that runs the
# customer's JAR.
#
# ORDER MATTERS. Both ``spark-sql`` and ``spark-connect-client-jvm`` ship a
# class named ``org.apache.spark.sql.SparkSession``; whichever is earlier on
# the classpath wins, and the customer's app calls
# ``SparkSession.builder().getOrCreate()`` against that one. The Connect
# client variant routes through SPARK_REMOTE; the plain spark-sql variant
# falls back to a local ``SparkContext`` (which then explodes on
# ``hadoop-client-runtime`` since we never ship it). Put the Connect client
# jar first so it wins the resolution. The 2.12 path doesn't need this
# explicit ordering only because deps_1's natural alphabetical listing
# already happens to put ``spark-connect-client-jvm_2.12`` before
# ``spark-sql_2.12``.
_SCALA_213_INCLUDES_JARS = [
    "spark-connect-client-jvm_2.13-3.5.6.jar",
    "spark-sql_2.13-3.5.6.jar",
    "spark-common-utils_2.13-3.5.6.jar",
    "json4s-ast_2.13-3.7.0-M11.jar",
    "scala-reflect-2.13.16.jar",
]


def start_jvm(scala_version: str | None = None):
    # The JVM is used to run the Spark parser and JDBC drivers,
    # so needs to be configured to support both.

    # JDBC driver .jars are added using the CLASSPATH env var.
    # We then add the Spark parser jars (that are shipped with pyspark)
    # by appending them to the default classpath.

    # Since we need to control JVM's parameters, fail immediately
    # if the JVM has already been started elsewhere.
    if jpype.isJVMStarted():
        if tcm.TCM_MODE:
            # No-op if JVM is already started in TCM mode
            return
        exception = RuntimeError(
            "JVM must not be running when starting the Spark Connect server"
        )
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    # Import both JAR dependency packages
    import snowpark_connect_deps_1
    import snowpark_connect_deps_2
    from snowflake.snowpark_connect.utils.jvm_classpath import (
        filter_classpath_jars,
        log_classpath_filter_summary,
    )

    # Load jar files from both packages, filtering out jars that are not
    # reachable from the server-side JVM code paths (Spark streaming,
    # Kubernetes, Hive, network/shuffle, MLlib math, ...). The stage-side
    # upload path in ``resources_initializer`` looks jars up by exact name
    # and is unaffected by this filter.
    #
    # The filter was temporarily disabled by PR #3789 after PR #3685's
    # initial drop list dropped ``spark-sketch_2.12-3.5.6.jar``, which
    # turned out to be reachable from catalyst's ``FunctionRegistry$``
    # static initializer and produced a silent merge-gate hang (the
    # daemon thread wedged inside JVM <clinit> before reaching
    # ``server_running.set()``, leaving ``server_running.wait()`` blocked
    # until the Jenkins job-level wall-clock timeout fired). The jar has
    # since been moved into the "Intentionally NOT skipped" set and the
    # filter is safe to re-enable. ``SCOS_JVM_CLASSPATH_FULL=1`` remains
    # available as a kill switch.
    jar_path_list = (
        snowpark_connect_deps_1.list_jars() + snowpark_connect_deps_2.list_jars()
    )
    kept_jars, dropped_jars = filter_classpath_jars(jar_path_list)
    log_classpath_filter_summary(kept_jars, dropped_jars)

    # Opt-in Scala-version filtering. When ``scala_version`` is ``None``
    # (the default for non-``execute_jar`` callers), behavior matches today
    # exactly: no version filtering, no jars appended from ``includes/jars/``.
    # ``execute_jar`` always passes a concrete ``"2.12"`` or ``"2.13"`` (it
    # normalizes its own ``None`` default to ``"2.12"`` before forwarding
    # here), so the filtered branch always runs for execute_jar customers.
    if scala_version is not None:
        kept_jars = _filter_jars_by_scala_version(kept_jars, scala_version)
        if scala_version == "2.13":
            includes_jars_dir = Path(__file__).parent / "includes" / "jars"
            existing_jar_names = {jar_path.name for jar_path in kept_jars}
            for jar_name in _SCALA_213_INCLUDES_JARS:
                if jar_name in existing_jar_names:
                    continue
                jar_path = includes_jars_dir / jar_name
                if jar_path.exists():
                    kept_jars.append(jar_path)
                    existing_jar_names.add(jar_name)
                    logger.debug(f"Added Scala 2.13 JAR from includes/jars: {jar_name}")
                else:
                    logger.warning(f"Expected Scala 2.13 JAR not found: {jar_path}")

    for jar_path in kept_jars:
        jpype.addClassPath(jar_path)

    # TODO: Should remove convertStrings, but it breaks the JDBC code.
    jvm_settings: list[str] = list(
        filter(
            lambda e: e != "",
            os.environ.get("JAVA_OPTS", "").split(),
        )
    )

    jpype.startJVM(
        *jvm_settings,
        convertStrings=True,
    )

    # Only recorded after a successful ``startJVM``. If startJVM raises,
    # this stays ``None`` so a retry in the same process can pick a
    # different ``scala_version``.
    global _started_jvm_scala_version
    _started_jvm_scala_version = scala_version


def start_session(
    is_daemon: bool = True,
    remote_url: Optional[str] = None,
    tcp_port: Optional[int] = None,
    unix_domain_socket: Optional[str] = None,
    stop_event: threading.Event = None,
    snowpark_session: Optional[snowpark.Session] = None,
    connection_parameters: Optional[Dict[str, str]] = None,
    max_grpc_message_size: int = _SPARK_CONNECT_GRPC_MAX_MESSAGE_SIZE,
    _add_signal_handler: bool = False,
    _monitor_stdin: bool = False,
    app_name: str | None = None,
    scala_version: str | None = None,
) -> threading.Thread | None:
    """
    Starts Spark Connect server connected to Snowflake. No-op if the Server is already running.

    Parameters:
        is_daemon (bool): Should run the server as daemon or not. use True to automatically shut the Spark connect
                          server down when the main program (or test) finishes. use False to start the server in a
                          stand-alone, long-running mode.
        remote_url (Optional[str]): sc:// URL on which to start the Spark Connect server. This option is incompatible with the tcp_port
                                    and unix_domain_socket parameters.
        tcp_port (Optional[int]): TCP port on which to start the Spark Connect server. This option is incompatible with
                                  the remote_url and unix_domain_socket parameters.
        unix_domain_socket (Optional[str]): Path to the unix domain socket on which to start the Spark Connect server.
                                            This option is incompatible with the remote_url and tcp_port parameters.
        stop_event (Optional[threading.Event]): Stop the SAS server when stop_event.set() is called.
                                                Only works when is_daemon=True.
        snowpark_session: A Snowpark session to use for this connection; currently the only applicable use of this is to
                          pass in the session created by the stored proc environment.
        connection_parameters: A dictionary of connection parameters to use to create the Snowpark session. If this is
                                provided, the `snowpark_session` parameter must be None.
        app_name: Optional application name to register with the Snowflake session.
        scala_version: Optional Scala binary version for the JVM classpath
                       (``"2.12"`` or ``"2.13"``). ``None`` (default)
                       preserves today's classpath behavior exactly; only
                       explicit ``"2.12"`` / ``"2.13"`` opts into Scala-version
                       filtering. Used by ``execute_jar``.
    """
    # Increase recursion limit to 1100 (1000 by default)
    # introduced due to Scala OSS Test: org.apache.spark.sql.ClientE2ETestSuite.spark deep recursion
    sys.setrecursionlimit(1100)

    # Apply PySpark Connect client monkeypatches
    from snowflake.snowpark_connect.utils.patch_spark_line_number import (
        patch_proto_to_string,
        patch_pyspark_connect,
    )

    patch_proto_to_string()

    # Client stack injection feeds OTel spans and JSON QUERY_TAG (when enabled).
    # Patching is skipped only when both features are off at server startup.
    from snowflake.snowpark_connect.config import is_add_debug_info_to_query_tag_enabled

    if is_telemetry_enabled() or is_add_debug_info_to_query_tag_enabled():
        patch_pyspark_connect()

    try:
        scala_version = _validate_scala_version(scala_version)

        # Set max grpc message size if provided
        if max_grpc_message_size is not None:
            set_grpc_max_message_size(max_grpc_message_size)

        # Validate startup parameters
        snowpark_session = validate_startup_parameters(
            snowpark_session, connection_parameters
        )

        server_running = get_server_running()
        if server_running.is_set():
            # When the server is already running, the JVM has already been
            # started — we cannot rebuild its classpath. Reject reuse in a
            # different Scala-version mode (including None vs explicit) so
            # the new ``scala_version`` kwarg is never silently ignored.
            _ensure_started_jvm_matches_scala_version(scala_version)
            url = get_client_url()
            logger.warning(f"Snowpark Connect session is already running at {url}")
            return

        configure_server_url(remote_url, tcp_port, unix_domain_socket)

        start_jvm(scala_version=scala_version)
        _disable_protobuf_recursion_limit()
        otel_initialize()

        if _add_signal_handler:
            setup_signal_handlers(stop_event)

        if _monitor_stdin:
            start_stdin_monitor(stop_event)

        if is_daemon:
            arguments = (stop_event, snowpark_session, app_name)

            target_func = otel_create_context_wrapper(_serve)

            server_thread = threading.Thread(
                target=target_func, args=arguments, daemon=True
            )
            server_thread.start()
            server_running.wait()
            if get_server_error():
                exception = RuntimeError("Snowpark Connect session failed to start")
                attach_custom_error_code(
                    exception, ErrorCodes.STARTUP_CONNECTION_FAILED
                )
                raise exception

            return server_thread
        else:
            # Launch in the foreground with stop_event
            _serve(stop_event=stop_event, session=snowpark_session, app_name=app_name)
    except Exception as e:
        _reset_server_run_state()
        logger.error(e, exc_info=True)
        attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
        raise e


def _is_running_in_snowpark_submit() -> bool:
    """Check if running inside a snowpark-submit job."""
    return os.getenv("SNOWPARK_SUBMIT_JOB") == "true"


def _get_default_app_name() -> str:
    """Derive a default app name from the caller's filename.

    Walks the call stack to find the first frame outside the snowpark_connect
    package.  If that frame's filename ends with ``.py`` or ``.ipynb``, uses it
    as the app name prefix; otherwise falls back to a generic label.
    """
    frame = inspect.currentframe()
    try:
        caller = frame
        while caller is not None:
            filename = caller.f_code.co_filename
            if "snowpark_connect" not in filename:
                basename = os.path.basename(filename)
                if basename.endswith((".py", ".ipynb")):
                    return f"{basename}"
                break
            caller = caller.f_back
    finally:
        del frame
    return "Snowpark Connect Session"


def init_spark_session(
    conf: SparkConf = None,
    connection_parameters: Optional[Dict[str, str]] = None,
    app_name: str | None = None,
) -> SparkSession:
    """
    Initialize and return a Spark session connected to Snowflake.

    Parameters:
        conf (SparkConf): Optional Spark configuration.
        connection_parameters (dict): Optional dictionary of connection parameters to use
            to create the Snowpark session (e.g. connection_name, account, user, password,
            host, warehouse, database, schema, etc.). If not provided, the connection
            resolver will determine which connection to use from connections.toml.
            Inside snowpark-submit jobs this argument is ignored; the workload uses the
            Spark Connect session from the job environment (submit/SPCS wiring), not this dict.
        app_name (str): Optional application name to register with the Snowflake session.
            If not provided, a default is derived from the caller's filename.

    Returns:
        A new SparkSession connected to the Snowpark Connect server.
    """
    if app_name is None:
        try:
            app_name = _get_default_app_name()
        except Exception:
            app_name = "Snowpark Connect Session"

    if _is_running_in_snowpark_submit():
        # Running inside snowpark-submit - use existing Spark session.
        # The server container already has its own Snowflake connection
        # via SPCS environment variables / snowpark-submit CLI flags.
        if connection_parameters is not None:
            logger.info(
                "Ignoring connection_parameters in init_spark_session() inside "
                "snowpark-submit; using the job Spark Connect session."
            )
        from pyspark.sql import SparkSession

        builder = SparkSession.builder
        if conf is not None:
            for k, v in conf.getAll():
                builder = builder.config(k, v)
        return builder.getOrCreate()
    else:
        _setup_spark_environment()
        from snowflake.snowpark_connect.utils.session import (
            _get_current_snowpark_session,
        )

        snowpark_session = _get_current_snowpark_session()

        start_session(
            snowpark_session=snowpark_session,
            connection_parameters=connection_parameters,
            app_name=app_name,
        )
        return get_session(conf=conf)


def execute_jar(
    class_name: str,
    jars: list[str],
    job_args: list[str] | None = None,
    session: Optional[snowpark.Session] = None,
    tcp_port: int | None = None,
    jvm_options: list[str] | None = None,
    scala_version: str | None = None,
) -> None:
    """
    Start the SCOS server, then call ``class_name.main(String[] args)`` via JPype.

    1. Add JARs to classpath (before JVM starts)
    2. Inject JVM options and ``--add-opens`` flags into ``JAVA_OPTS``
    3. Start SCOS thick server (which starts JVM + gRPC server)
    4. Set ``SPARK_REMOTE`` so the customer's ``SparkSession.builder().getOrCreate()``
       connects automatically
    5. Install the log4j2 -> Python logging bridge appender so JVM log
       records emitted by the customer JAR are re-exported through Python
       logging (and thus surface in the Snowflake event table when running
       inside a stored procedure). Only wired when the process is running
       inside a Snowflake warehouse / stored procedure / notebook (or when
       ``SNOWPARK_CONNECT_LOG4J_BRIDGE_FORCE=1`` is set). Best-effort;
       failures are logged and swallowed. Controlled by
       ``SNOWPARK_CONNECT_LOG4J_BRIDGE_LEVEL`` and
       ``SNOWPARK_CONNECT_LOG4J_BRIDGE_DISABLE``.
    6. Invoke ``public static void main(String[])`` on *class_name*
    7. Uninstall the bridge appender and shut down SCOS server + JVM

    Args:
        class_name: Fully qualified Java/Scala class name (e.g. ``com.example.MyApp``).
        jars: JAR files / glob patterns to add to the classpath.
        job_args: Arguments forwarded to ``main(String[] args)``.
        session: Optional Snowpark session for the SCOS server.
        tcp_port: gRPC server port (default 15002). ``None`` uses a Unix domain socket.
        jvm_options: Extra JVM flags (e.g. ``["-Xmx4g"]``).
        scala_version: Optional Scala binary version (``"2.12"`` or
            ``"2.13"``). When set, it is:

              1. Written into
                 ``global_config["snowpark.connect.scala.version"]`` so
                 every Scala-versioned artifact (bridge jar, Snowpark
                 assembly, UDF helpers) converges on the same value.
              2. Forwarded to ``start_session`` → ``start_jvm``, which
                 filters the deps classpath to drop the opposite Scala
                 binary version and (for 2.13 only) appends the 2.13
                 replacement jars shipped under
                 ``src/snowflake/snowpark_connect/includes/jars/``.

            ``None`` (the default) is normalized to ``"2.12"`` inside
            this function. We pin the default explicitly because the
            ``snowpark-connect-deps-2`` package now ships *both*
            ``scala-library-2.12`` and ``scala-library-2.13`` to support
            Scala 2.13 customers, but only ``scala-reflect-2.12``. An
            unfiltered classpath would let the JVM pick
            ``scala-library-2.13`` alongside ``scala-reflect-2.12`` and
            blow up at scala-reflect runtime init with ``Scala signature
            package has wrong version expected: 5.0 found: 5.2``. Pinning
            the default to ``"2.12"`` is a no-op for older deps releases
            (which only shipped 2.12 jars anyway) and a safety net for
            current and future releases. Scala 2.13 stays strictly
            opt-in (only enabled by an explicit ``"2.13"``). Validated
            to be ``"2.12"`` or ``"2.13"``; any other value raises
            ``ValueError`` with ``INVALID_CONFIG_VALUE``.
    """
    import glob
    import time as _time

    from snowflake.snowpark_connect.utils.log4j_bridge import (
        add_bridge_jar_to_classpath,
        install_python_bridge_appender,
    )
    from snowflake.snowpark_connect.utils.session import (
        _is_running_in_stored_procedure_or_notebook,
    )

    scala_version = _validate_scala_version(scala_version)
    if scala_version is None:
        scala_version = "2.12"

    stop_event = threading.Event()

    # The log4j2 -> Python logging bridge only helps when stdout/stderr of
    # the JVM is not directly captured by the host runtime. That is the
    # case for Snowflake warehouses (Python stored procedures, UDFs,
    # notebooks hosted on a warehouse). In local/CLI runs JVM logs already
    # appear in the user's terminal, so skipping the bridge avoids loading
    # the 6+ MB sas-scala-udf jar on the classpath and the noisy fallback
    # warning when the bridge classes are not resolvable.
    # ``SNOWPARK_CONNECT_LOG4J_BRIDGE_FORCE=1`` bypasses the warehouse
    # check (useful for local reproduction and integration tests).
    install_log_bridge = (
        os.environ.get("SNOWPARK_CONNECT_LOG4J_BRIDGE_FORCE", "") == "1"
        or _is_running_in_stored_procedure_or_notebook()
    )

    try:
        # 0. If the caller pinned a Scala version, push it into
        # ``global_config`` *before* anything else so every existing
        # ``get_scala_version()`` callsite (bridge jar selection,
        # resources_initializer, UDF helpers, etc.) converges on the same
        # value. Without this the bridge jar would honor the explicit
        # version while the Snowpark assembly + helper jars keep using
        # ``global_config``'s prior value, producing a mixed-Scala
        # classpath that fails at JVM startup.
        if scala_version is not None:
            from snowflake.snowpark_connect.config import global_config

            global_config["snowpark.connect.scala.version"] = scala_version

        # 1. Validate and add JARs to classpath
        for jar in jars or []:
            if not glob.glob(jar):
                raise FileNotFoundError(f"JAR not found: {jar}")
        for pattern in jars or []:
            for resolved in glob.glob(pattern):
                jpype.addClassPath(os.path.abspath(resolved))

        # Add the sas-scala-udf jar to the classpath so the log4j2 -> Python
        # bridge appender
        # (com.snowflake.sas.scala.log.SnowparkConnectPythonBridgeAppender)
        # is resolvable from JPype once the JVM is started. Best-effort: a
        # failure here only disables log forwarding, never the workload.
        if install_log_bridge:
            add_bridge_jar_to_classpath(scala_version)
        else:
            logger.debug(
                "Skipping log4j -> Python bridge classpath add: not running "
                "inside a Snowflake warehouse / stored procedure"
            )

        # 2. Set SPARK_REMOTE env var BEFORE JVM starts (Java caches env at startup)
        socket_path = None
        if tcp_port:
            spark_remote_url = f"sc://127.0.0.1:{tcp_port}"
        else:
            socket_dir = tempfile.mkdtemp()
            socket_path = os.path.join(socket_dir, "snowflake_sas_grpc.sock")
            spark_remote_url = f"sc://unix:{socket_path}"
        os.environ["SPARK_REMOTE"] = spark_remote_url

        # 3. Inject JVM options and --add-opens flags into JAVA_OPTS.
        #    --add-opens is required because the Spark Connect client uses Apache Arrow
        #    for data transfer, which needs reflective access to java.nio internals
        #    for off-heap memory allocation (MemoryUtil / DirectByteBuffer).
        required_flags = [
            "--add-opens=java.base/java.nio=org.apache.arrow.memory.core,ALL-UNNAMED",
            "--add-opens=java.base/jdk.internal.misc=org.apache.arrow.memory.core,ALL-UNNAMED",
            "--add-opens=jdk.unsupported/sun.misc=org.apache.arrow.memory.core,ALL-UNNAMED",
        ]
        existing = os.environ.get("JAVA_OPTS", "").split()
        all_opts = existing + (jvm_options or []) + required_flags
        os.environ["JAVA_OPTS"] = " ".join(dict.fromkeys(all_opts))

        # 4. Start SCOS thick server (which starts JVM + gRPC server).
        # Forward ``scala_version`` so ``start_jvm`` filters the deps
        # classpath to the requested binary version and (for 2.13) appends
        # the ``includes/jars/`` 2.13 replacements. When ``scala_version``
        # is ``None``, ``start_jvm(None)`` preserves today's behavior
        # exactly.
        start_session(
            is_daemon=True,
            tcp_port=tcp_port,
            unix_domain_socket=socket_path,
            stop_event=stop_event,
            snowpark_session=session,
            scala_version=scala_version,
        )
        logger.info(f"Server ready at {spark_remote_url} (SPARK_REMOTE set)")

        # Forward JVM log4j2 records to Python logging so they surface in the
        # Snowflake event table when running inside a stored procedure. Uses
        # SnowparkConnectPythonBridgeAppender from sas-scala-udf.jar.
        # Installation is best-effort; a logging shim must never break the
        # customer workload. Gated on the warehouse/sproc check above so
        # local runs avoid loading the bridge jar and emitting a noisy
        # "appender not loadable" warning.
        if install_log_bridge:
            install_python_bridge_appender()

        # 5. Invoke public static void main(String[])
        java_args = job_args or []
        logger.info(f"Calling {class_name}.main() with args {java_args}")
        java_class = jpype.JClass(class_name)
        java_class.main(java_args)

        logger.info(f"{class_name}.main() completed.")
    except Exception as ex:
        logger.error("execute_jar failed", exc_info=True)
        if hasattr(ex, "stacktrace") and callable(ex.stacktrace):
            logger.error(ex.stacktrace())
        raise
    finally:
        # 6. Shut down SCOS server. The log4j -> Python bridge appender (if
        #    installed) does not need an explicit detach: the embedded JVM
        #    is terminated immediately below, taking the appender with it.
        stop_event.set()
        logger.info("Shutting down gRPC server...")
        _time.sleep(1)

        # 7. Shut down JVM (must be called from main thread; skip if not)
        if jpype.isJVMStarted():
            try:
                logger.info("Shutting down JVM...")
                jpype.shutdownJVM()
                logger.info("JVM shutdown complete.")
            except RuntimeError as e:
                if "main thread" in str(e):
                    logger.info(
                        "Skipping JVM shutdown (not on main thread); "
                        "JVM will be reclaimed at process exit."
                    )
                else:
                    logger.error(f"Unexpected error during JVM shutdown: {e}")
                    raise


def _get_files_metadata(data_source: relations_proto.Read.DataSource) -> List[str]:
    # TODO: Handle paths on the cloud
    paths = data_source.paths
    extension = data_source.format if data_source.format != "text" else "txt"
    files = []
    for path in paths:
        if os.path.isfile(path):
            files.append(f"file://{path}")
        else:
            files.extend(
                [
                    f"file://{path}/{f}"
                    for f in os.listdir(path)
                    if f.endswith(extension)
                ]
            )
    return files
