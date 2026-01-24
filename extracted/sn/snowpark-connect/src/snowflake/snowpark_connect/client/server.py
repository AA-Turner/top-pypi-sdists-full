#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Remote Spark Connect Server for Snowpark Connect.

Lightweight servicer that forwards Spark Connect requests to Snowflake backend
via REST API using SparkConnectResource SDK.
"""

import threading
import uuid
from concurrent import futures
from typing import Dict, Iterator, Optional

import grpc
import pyarrow as pa
from google.rpc import code_pb2
from grpc_status import rpc_status
from pyspark.conf import SparkConf
from pyspark.sql.connect.proto import base_pb2, base_pb2_grpc, types_pb2
from pyspark.sql.connect.session import SparkSession
from snowflake.core.spark_connect._spark_connect import SparkConnectResource

from snowflake import snowpark
from snowflake.snowpark import Session
from snowflake.snowpark_connect.client.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.client.exceptions import (
    GrpcErrorStatusException,
    UnexpectedResponseException,
)
from snowflake.snowpark_connect.client.query_results import (
    fetch_query_result_as_arrow_batches,
    fetch_query_result_as_protobuf,
)
from snowflake.snowpark_connect.client.utils.session import (
    get_or_create_snowpark_session,
)
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.server_common import (  # noqa: F401 - re-exported for public API
    _disable_protobuf_recursion_limit,
    _get_default_grpc_options,
    _reset_server_run_state,
    _setup_spark_environment,
    _stop_server,
    configure_server_url,
    get_client_url,
    get_server_error,
    get_server_running,
    get_server_url,
    get_session,
    set_grpc_max_message_size,
    set_server_error,
    setup_signal_handlers,
    validate_startup_parameters,
)
from snowflake.snowpark_connect.utils.concurrent import SynchronizedDict
from snowflake.snowpark_connect.utils.env_utils import get_int_from_env
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import telemetry
from spark.connect import envelope_pb2


def _log_and_return_error(
    err_mesg: str,
    error: Exception,
    status_code: grpc.StatusCode,
    context: grpc.ServicerContext,
) -> None:
    """Log error and set gRPC context."""
    context.set_details(str(error))
    context.set_code(status_code)
    logger.error(f"{err_mesg} status code: {status_code}", exc_info=True)
    return None


def _validate_response_type(
    resp_envelope: envelope_pb2.ResponseEnvelope, expected_field: str
) -> None:
    """Validate that response envelope has   expected type."""
    field_name = resp_envelope.WhichOneof("response_type")
    if field_name != expected_field:
        raise UnexpectedResponseException(
            f"Expected response type {expected_field}, got {field_name}"
        )


def _build_result_complete_response(
    request: base_pb2.ExecutePlanRequest,
) -> base_pb2.ExecutePlanResponse:
    return base_pb2.ExecutePlanResponse(
        session_id=request.session_id,
        operation_id=request.operation_id or "0",
        result_complete=base_pb2.ExecutePlanResponse.ResultComplete(),
    )


def _build_exec_plan_resp_stream_from_df_query_result(
    request: base_pb2.ExecutePlanRequest,
    session: Session,
    query_result: envelope_pb2.DataframeQueryResult,
) -> Iterator[base_pb2.ExecutePlanResponse]:
    query_id = query_result.result_job_uuid
    arrow_schema = pa.ipc.read_schema(pa.BufferReader(query_result.arrow_schema))
    spark_schema = types_pb2.DataType()
    spark_schema.ParseFromString(query_result.spark_schema)

    for row_count, arrow_batch_bytes in fetch_query_result_as_arrow_batches(
        session, query_id, arrow_schema
    ):
        yield base_pb2.ExecutePlanResponse(
            session_id=request.session_id,
            operation_id=request.operation_id or "0",
            arrow_batch=base_pb2.ExecutePlanResponse.ArrowBatch(
                row_count=row_count,
                data=arrow_batch_bytes,
            ),
            schema=spark_schema,
        )

    yield _build_result_complete_response(request)


def _build_exec_plan_resp_stream_from_resp_envelope(
    request: base_pb2.ExecutePlanRequest,
    session: Session,
    resp_envelope: envelope_pb2.ResponseEnvelope,
) -> Iterator[base_pb2.ExecutePlanResponse]:
    """Build execution plan response stream from response envelope."""
    resp_type = resp_envelope.WhichOneof("response_type")

    if resp_type == "dataframe_query_result":
        query_result = resp_envelope.dataframe_query_result
        yield from _build_exec_plan_resp_stream_from_df_query_result(
            request, session, query_result
        )
    elif resp_type == "execute_plan_response":
        yield resp_envelope.execute_plan_response
        yield _build_result_complete_response(request)
    elif resp_type == "status":
        raise GrpcErrorStatusException(resp_envelope.status)
    else:
        logger.warning(f"Unexpected response type: {resp_type}")


class SnowflakeConnectClientServicer(base_pb2_grpc.SparkConnectServiceServicer):
    # Configs frequently read by PySpark client but not supported in SAS.
    # We return the request's default value directly without calling the backend.
    #
    # Why this matters:
    # - These configs are read via get_config_with_defaults() on every show()/toPandas()
    # - In SAS, show() internally calls toPandas() (see pyspark/sql/connect/dataframe.py _show_string)
    # - Without this optimization, every show() would make a backend config request
    #
    # Source: OSS Spark python/pyspark/sql/connect/client/core.py to_pandas() method
    _UNSUPPORTED_CONFIGS: frozenset[str] = frozenset(
        {
            # Read on every show() and toPandas() call - controls Arrow memory optimization
            "spark.sql.execution.arrow.pyspark.selfDestruct.enabled",
            # Read on toPandas() when DataFrame contains StructType fields
            "spark.sql.execution.pandas.structHandlingMode",
        }
    )

    def __init__(self, snowpark_session: Session) -> None:
        self.snowpark_session = snowpark_session
        self._config_cache: SynchronizedDict[str, str] = SynchronizedDict()

    def _get_spark_resource(self) -> SparkConnectResource:
        return SparkConnectResource(self.snowpark_session)

    def _parse_response_envelope(
        self, response_bytes: bytes | bytearray, expected_resp_type: str = None
    ) -> envelope_pb2.ResponseEnvelope:
        """Parse and validate response envelope from GS backend."""

        resp_envelope = envelope_pb2.ResponseEnvelope()
        if isinstance(response_bytes, bytearray):
            response_bytes = bytes(response_bytes)
        resp_envelope.ParseFromString(response_bytes)

        resp_type = resp_envelope.WhichOneof("response_type")
        if resp_type == "status":
            raise GrpcErrorStatusException(resp_envelope.status)

        if not resp_envelope.query_id and not resp_type == "dataframe_query_result":
            _validate_response_type(resp_envelope, expected_resp_type)

        return resp_envelope

    def ExecutePlan(
        self, request: base_pb2.ExecutePlanRequest, context: grpc.ServicerContext
    ) -> Iterator[base_pb2.ExecutePlanResponse]:
        """Execute a Spark plan by forwarding to GS backend."""
        logger.debug("Received Execute Plan request")
        query_id = None
        telemetry.initialize_request_summary(request)

        try:
            spark_resource = self._get_spark_resource()
            response_bytes = spark_resource.execute_plan(request.SerializeToString())
            resp_envelope = self._parse_response_envelope(
                response_bytes, "execute_plan_response"
            )
            query_id = resp_envelope.query_id

            if query_id:
                job_res_envelope = fetch_query_result_as_protobuf(
                    self.snowpark_session, resp_envelope.query_id
                )
                yield from _build_exec_plan_resp_stream_from_resp_envelope(
                    request, self.snowpark_session, job_res_envelope
                )
            else:
                yield from _build_exec_plan_resp_stream_from_resp_envelope(
                    request, self.snowpark_session, resp_envelope
                )

        except GrpcErrorStatusException as e:
            telemetry.report_request_failure(e)
            context.abort_with_status(rpc_status.to_status(e.status))
        except Exception as e:
            telemetry.report_request_failure(e)
            logger.error(f"Error in ExecutePlan, query id {query_id}", exc_info=True)
            return _log_and_return_error(
                "Error in ExecutePlan call", e, grpc.StatusCode.INTERNAL, context
            )
        finally:
            telemetry.send_request_summary_telemetry()

    def _call_backend_config(
        self, request: base_pb2.ConfigRequest
    ) -> base_pb2.ConfigResponse:
        """Forward config request to GS and return response."""
        spark_resource = self._get_spark_resource()
        response_bytes = spark_resource.config(request.SerializeToString())
        resp_envelope = self._parse_response_envelope(response_bytes, "config_response")

        query_id = resp_envelope.query_id
        if query_id:
            resp_envelope = fetch_query_result_as_protobuf(
                self.snowpark_session, query_id
            )
            assert resp_envelope.WhichOneof("response_type") == "config_response"

        return resp_envelope.config_response

    def _handle_get_cached_config_request(
        self,
        request: base_pb2.ConfigRequest,
        items: list[tuple[str, Optional[str]]],
        op_name: str,
        update_cache_on_miss: bool = True,
    ) -> base_pb2.ConfigResponse:
        """
        Handle config requests with caching and unsupported config checks.

        Args:
            request: The original ConfigRequest.
            items: List of (key, default_value) tuples. default_value is None for get/get_option.
            op_name: Name of the operation for logging (e.g., "get", "get_with_default").
            update_cache_on_miss: Whether to update the cache with values returned from backend.
        """
        keys = [k for k, _ in items]

        # 1. Unsupported Configs Check
        # If all keys are unsupported, return defaults (if any) or empty response without calling backend
        if all(key in self._UNSUPPORTED_CONFIGS for key in keys):
            response = base_pb2.ConfigResponse(session_id=request.session_id)
            for key, default_val in items:
                resp_pair = response.pairs.add()
                resp_pair.key = key
                if default_val is not None:
                    resp_pair.value = default_val
            logger.debug(f"Config {op_name} returning defaults for unsupported: {keys}")
            return response

        # 2. Cache Check
        # Check if all keys are in cache
        cached_values = {key: self._config_cache.get(key) for key in keys}
        if cached_values and all(value is not None for value in cached_values.values()):
            response = base_pb2.ConfigResponse(session_id=request.session_id)
            for key in keys:
                resp_pair = response.pairs.add()
                resp_pair.key = key
                resp_pair.value = cached_values[key]
            logger.debug(f"Config {op_name} served from cache: {keys}")
            return response

        # 3. Cache Miss - Call Backend
        config_response = self._call_backend_config(request)

        if update_cache_on_miss:
            for pair in config_response.pairs:
                if pair.HasField("value"):
                    self._config_cache[pair.key] = pair.value
            logger.debug(f"Config {op_name} cached from backend: {keys}")
        else:
            logger.debug(f"Config {op_name} from backend (not cached): {keys}")

        return config_response

    def Config(
        self, request: base_pb2.ConfigRequest, context: grpc.ServicerContext
    ) -> base_pb2.ConfigResponse:
        logger.debug("Received Config request")
        telemetry.initialize_request_summary(request)

        try:
            op = request.operation
            op_type = op.WhichOneof("op_type")

            match op_type:
                case "get_with_default":
                    pairs = op.get_with_default.pairs
                    items = [
                        (p.key, p.value if p.HasField("value") else None) for p in pairs
                    ]
                    return self._handle_get_cached_config_request(
                        request, items, "get_with_default", update_cache_on_miss=False
                    )

                case "get":
                    keys = op.get.keys
                    items = [(k, None) for k in keys]
                    return self._handle_get_cached_config_request(request, items, "get")

                case "set":
                    config_response = self._call_backend_config(request)

                    for pair in op.set.pairs:
                        if pair.HasField("value"):
                            self._config_cache[pair.key] = pair.value
                    logger.debug(
                        f"Config set updated cache: {[p.key for p in op.set.pairs]}"
                    )
                    return config_response

                case "unset":
                    config_response = self._call_backend_config(request)

                    for key in op.unset.keys:
                        self._config_cache.remove(key)
                    logger.debug(f"Config unset updated cache: {list(op.unset.keys)}")
                    return config_response

                case "get_option":
                    keys = op.get_option.keys
                    items = [(k, None) for k in keys]
                    return self._handle_get_cached_config_request(
                        request, items, "get_option"
                    )

                case "get_all":
                    # Always call backend since this is a prefix-based search and we
                    # can't know if all matching keys are in cache. Cache the results.
                    config_response = self._call_backend_config(request)

                    # Cache all returned values
                    for pair in config_response.pairs:
                        if pair.HasField("value"):
                            self._config_cache[pair.key] = pair.value
                    prefix = (
                        op.get_all.prefix if op.get_all.HasField("prefix") else "all"
                    )
                    logger.debug(
                        f"Config get_all cached {len(config_response.pairs)} items (prefix={prefix})"
                    )
                    return config_response

                case _:
                    # Forward other operations to backend (no caching)
                    logger.debug(
                        f"Forwarding unknown config request of type {op_type} to the backend"
                    )
                    return self._call_backend_config(request)

        except GrpcErrorStatusException as e:
            telemetry.report_request_failure(e)
            context.abort_with_status(rpc_status.to_status(e.status))
        except Exception as e:
            telemetry.report_request_failure(e)
            logger.error("Error in Config", exc_info=True)
            return _log_and_return_error(
                "Error in Config call", e, grpc.StatusCode.INTERNAL, context
            )
        finally:
            telemetry.send_request_summary_telemetry()

    def AnalyzePlan(
        self, request: base_pb2.AnalyzePlanRequest, context: grpc.ServicerContext
    ) -> base_pb2.AnalyzePlanResponse:
        logger.debug("Received Analyze Plan request")
        query_id = None
        telemetry.initialize_request_summary(request)

        try:
            spark_resource = self._get_spark_resource()
            response_bytes = spark_resource.analyze_plan(request.SerializeToString())
            resp_envelope = self._parse_response_envelope(
                response_bytes, "analyze_plan_response"
            )

            query_id = resp_envelope.query_id

            if query_id:
                resp_envelope = fetch_query_result_as_protobuf(
                    self.snowpark_session, query_id
                )
                assert (
                    resp_envelope.WhichOneof("response_type") == "analyze_plan_response"
                )

            return resp_envelope.analyze_plan_response

        except GrpcErrorStatusException as e:
            telemetry.report_request_failure(e)
            context.abort_with_status(rpc_status.to_status(e.status))
        except Exception as e:
            telemetry.report_request_failure(e)
            logger.error(f"Error in AnalyzePlan, query id {query_id}", exc_info=True)
            return _log_and_return_error(
                "Error in AnalyzePlan call", e, grpc.StatusCode.INTERNAL, context
            )
        finally:
            telemetry.send_request_summary_telemetry()

    def AddArtifacts(
        self,
        request_iterator: Iterator[base_pb2.AddArtifactsRequest],
        context: grpc.ServicerContext,
    ) -> base_pb2.AddArtifactsResponse:
        logger.debug("Received AddArtifacts request")
        add_artifacts_response = None

        spark_resource = self._get_spark_resource()

        for request in request_iterator:
            query_id = None
            telemetry.initialize_request_summary(request)
            try:
                response_bytes = spark_resource.add_artifacts(
                    request.SerializeToString()
                )
                resp_envelope = self._parse_response_envelope(
                    response_bytes, "add_artifacts_response"
                )

                query_id = resp_envelope.query_id

                if query_id:
                    resp_envelope = fetch_query_result_as_protobuf(
                        self.snowpark_session, query_id
                    )
                    assert (
                        resp_envelope.WhichOneof("response_type")
                        == "add_artifacts_response"
                    )

                add_artifacts_response = resp_envelope.add_artifacts_response

            except GrpcErrorStatusException as e:
                telemetry.report_request_failure(e)
                context.abort_with_status(rpc_status.to_status(e.status))
            except Exception as e:
                telemetry.report_request_failure(e)
                logger.error(
                    f"Error in AddArtifacts, query id {query_id}", exc_info=True
                )
                return _log_and_return_error(
                    "Error in AddArtifacts call", e, grpc.StatusCode.INTERNAL, context
                )
            finally:
                telemetry.send_request_summary_telemetry()

        if add_artifacts_response is None:
            raise ValueError("AddArtifacts received empty request_iterator")

        return add_artifacts_response

    def ArtifactStatus(
        self, request: base_pb2.ArtifactStatusesRequest, context: grpc.ServicerContext
    ) -> base_pb2.ArtifactStatusesResponse:
        """Check statuses of artifacts in the session and returns them in a [[ArtifactStatusesResponse]]"""
        logger.debug("Received ArtifactStatus request")
        query_id = None
        telemetry.initialize_request_summary(request)

        try:
            spark_resource = self._get_spark_resource()
            response_bytes = spark_resource.artifact_status(request.SerializeToString())
            resp_envelope = self._parse_response_envelope(
                response_bytes, "artifact_status_response"
            )

            query_id = resp_envelope.query_id

            if query_id:
                resp_envelope = fetch_query_result_as_protobuf(
                    self.snowpark_session, query_id
                )
                assert (
                    resp_envelope.WhichOneof("response_type")
                    == "artifact_status_response"
                )

            return resp_envelope.artifact_status_response
        except GrpcErrorStatusException as e:
            telemetry.report_request_failure(e)
            context.abort_with_status(rpc_status.to_status(e.status))
        except Exception as e:
            telemetry.report_request_failure(e)
            logger.error(f"Error in ArtifactStatus, query id {query_id}", exc_info=True)
            return _log_and_return_error(
                "Error in ArtifactStatus call", e, grpc.StatusCode.INTERNAL, context
            )
        finally:
            telemetry.send_request_summary_telemetry()

    def Interrupt(
        self, request: base_pb2.InterruptRequest, context: grpc.ServicerContext
    ) -> base_pb2.InterruptResponse:
        """Interrupt running executions."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method Interrupt not implemented!")
        raise NotImplementedError("Method Interrupt not implemented!")

    def ReleaseExecute(
        self, request: base_pb2.ReleaseExecuteRequest, context: grpc.ServicerContext
    ) -> base_pb2.ReleaseExecuteResponse:
        """Release an execution."""
        logger.debug("Received Release Execute request")
        telemetry.initialize_request_summary(request)
        try:
            return base_pb2.ReleaseExecuteResponse(
                session_id=request.session_id,
                operation_id=request.operation_id or str(uuid.uuid4()),
            )
        except Exception as e:
            telemetry.report_request_failure(e)
            logger.error("Error in ReleaseExecute", exc_info=True)
            return _log_and_return_error(
                "Error in ReleaseExecute call", e, grpc.StatusCode.INTERNAL, context
            )
        finally:
            telemetry.send_request_summary_telemetry()

    def ReattachExecute(
        self, request: base_pb2.ReattachExecuteRequest, context: grpc.ServicerContext
    ) -> Iterator[base_pb2.ExecutePlanResponse]:
        """Reattach to an existing reattachable execution.
        The ExecutePlan must have been started with ReattachOptions.reattachable=true.
        If the ExecutePlanResponse stream ends without a ResultComplete message, there is more to
        continue. If there is a ResultComplete, the client should use ReleaseExecute with
        """
        from google.rpc import status_pb2

        status = status_pb2.Status(
            code=code_pb2.UNIMPLEMENTED,
            message="Method ReattachExecute not implemented! INVALID_HANDLE.OPERATION_NOT_FOUND",
        )
        context.abort_with_status(rpc_status.to_status(status))


def _serve(
    stop_event: Optional[threading.Event] = None,
    session: Optional[snowpark.Session] = None,
) -> None:
    server_running = get_server_running()
    try:
        if session is None:
            session = get_or_create_snowpark_session()

        # Initialize telemetry with session and thin client source identifier
        telemetry.initialize(session, source="SparkConnectLightWeightClient")

        server_options = _get_default_grpc_options()
        max_workers = get_int_from_env("SPARK_CONNECT_CLIENT_GRPC_MAX_WORKERS", 10)

        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            options=server_options,
        )

        base_pb2_grpc.add_SparkConnectServiceServicer_to_server(
            SnowflakeConnectClientServicer(session),
            server,
        )
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
        if "Invalid connection_name 'spark-connect', known ones are " in str(e):
            logger.error(
                "Ensure 'spark-connect' connection config has been set correctly in connections.toml."
            )
        else:
            logger.error("Error starting up Snowpark Connect server", exc_info=True)
        attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
        raise e
    finally:
        # Flush the telemetry queue if possible
        telemetry.shutdown()


def start_session(
    is_daemon: bool = True,
    remote_url: Optional[str] = None,
    tcp_port: Optional[int] = None,
    unix_domain_socket: Optional[str] = None,
    stop_event: threading.Event = None,
    snowpark_session: Optional[snowpark.Session] = None,
    connection_parameters: Optional[Dict[str, str]] = None,
    max_grpc_message_size: int = None,
    _add_signal_handler: bool = False,
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
    """

    try:
        # Set max grpc message size if provided
        if max_grpc_message_size is not None:
            set_grpc_max_message_size(max_grpc_message_size)

        # Validate startup parameters
        snowpark_session = validate_startup_parameters(
            snowpark_session, connection_parameters
        )

        server_running = get_server_running()
        if server_running.is_set():
            url = get_client_url()
            logger.warning(f"Snowpark Connect session is already running at {url}")
            return

        # Configure server URL
        configure_server_url(remote_url, tcp_port, unix_domain_socket)

        _disable_protobuf_recursion_limit()

        if _add_signal_handler:
            setup_signal_handlers(stop_event)

        if is_daemon:
            arguments = (stop_event, snowpark_session)
            server_thread = threading.Thread(target=_serve, args=arguments, daemon=True)
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
            _serve(stop_event=stop_event, session=snowpark_session)
    except Exception as e:
        _reset_server_run_state()
        logger.error(e, exc_info=True)
        attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
        raise e


def init_spark_session(conf: SparkConf = None) -> SparkSession:
    """
    Initialize and return a Spark session.

    Parameters:
        conf (SparkConf): Optional Spark configuration.

    Returns:
        A new SparkSession connected to the Snowpark Connect thin Client server.
    """
    _setup_spark_environment(False)
    from snowflake.snowpark_connect.client.utils.session import (
        _get_current_snowpark_session,
    )

    snowpark_session = _get_current_snowpark_session()
    start_session(snowpark_session=snowpark_session)
    return get_session(conf=conf)
