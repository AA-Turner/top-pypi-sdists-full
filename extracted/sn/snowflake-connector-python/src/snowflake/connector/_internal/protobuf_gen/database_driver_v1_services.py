from abc import ABC, abstractmethod
from typing import Optional
from google.protobuf import message
from .database_driver_v1_pb2 import *
from .proto_exception import *

class ProtoError(Exception):
    def __init__(self, error_type: str, details: str):
        self.error_type = error_type
        self.details = details
        super().__init__(f"{error_type}: {details}")

class DatabaseDriver(ABC):
    @abstractmethod
    def driver_get_fips_status(self, request: DriverGetFipsStatusRequest) -> DriverGetFipsStatusResponse:
        pass

    @abstractmethod
    def database_new(self, request: DatabaseNewRequest) -> DatabaseNewResponse:
        pass

    @abstractmethod
    def database_set_options(self, request: DatabaseSetOptionsRequest) -> DatabaseSetOptionsResponse:
        pass

    @abstractmethod
    def database_init(self, request: DatabaseInitRequest) -> DatabaseInitResponse:
        pass

    @abstractmethod
    def database_release(self, request: DatabaseReleaseRequest) -> DatabaseReleaseResponse:
        pass

    @abstractmethod
    def database_fetch_chunk(self, request: DatabaseFetchChunkRequest) -> DatabaseFetchChunkResponse:
        pass

    @abstractmethod
    def connection_new(self, request: ConnectionNewRequest) -> ConnectionNewResponse:
        pass

    @abstractmethod
    def connection_set_options(self, request: ConnectionSetOptionsRequest) -> ConnectionSetOptionsResponse:
        pass

    @abstractmethod
    def connection_init(self, request: ConnectionInitRequest) -> ConnectionInitResponse:
        pass

    @abstractmethod
    def connection_release(self, request: ConnectionReleaseRequest) -> ConnectionReleaseResponse:
        pass

    @abstractmethod
    def connection_close(self, request: ConnectionCloseRequest) -> ConnectionCloseResponse:
        pass

    @abstractmethod
    def connection_is_closed(self, request: ConnectionIsClosedRequest) -> ConnectionIsClosedResponse:
        pass

    @abstractmethod
    def connection_is_expired(self, request: ConnectionIsExpiredRequest) -> ConnectionIsExpiredResponse:
        pass

    @abstractmethod
    def connection_get_info(self, request: ConnectionGetInfoRequest) -> ConnectionGetInfoResponse:
        pass

    @abstractmethod
    def connection_get_objects(self, request: ConnectionGetObjectsRequest) -> ConnectionGetObjectsResponse:
        pass

    @abstractmethod
    def connection_get_table_schema(self, request: ConnectionGetTableSchemaRequest) -> ConnectionGetTableSchemaResponse:
        pass

    @abstractmethod
    def connection_get_table_types(self, request: ConnectionGetTableTypesRequest) -> ConnectionGetTableTypesResponse:
        pass

    @abstractmethod
    def connection_commit(self, request: ConnectionCommitRequest) -> ConnectionCommitResponse:
        pass

    @abstractmethod
    def connection_rollback(self, request: ConnectionRollbackRequest) -> ConnectionRollbackResponse:
        pass

    @abstractmethod
    def connection_set_autocommit(self, request: ConnectionSetAutocommitRequest) -> ConnectionSetAutocommitResponse:
        pass

    @abstractmethod
    def connection_use_database(self, request: ConnectionUseDatabaseRequest) -> ConnectionUseDatabaseResponse:
        pass

    @abstractmethod
    def connection_use_schema(self, request: ConnectionUseSchemaRequest) -> ConnectionUseSchemaResponse:
        pass

    @abstractmethod
    def connection_set_session_parameters(self, request: ConnectionSetSessionParametersRequest) -> ConnectionSetSessionParametersResponse:
        pass

    @abstractmethod
    def connection_get_parameter(self, request: ConnectionGetParameterRequest) -> ConnectionGetParameterResponse:
        pass

    @abstractmethod
    def connection_get_all_parameters(self, request: ConnectionGetAllParametersRequest) -> ConnectionGetAllParametersResponse:
        pass

    @abstractmethod
    def connection_get_server_version(self, request: ConnectionGetServerVersionRequest) -> ConnectionGetServerVersionResponse:
        pass

    @abstractmethod
    def connection_validate_options(self, request: ConnectionValidateOptionsRequest) -> ConnectionValidateOptionsResponse:
        pass

    @abstractmethod
    def connection_get_query_result(self, request: ConnectionGetQueryResultRequest) -> ExecuteQueryResponse:
        pass

    @abstractmethod
    def connection_get_result_set(self, request: ConnectionGetResultSetRequest) -> ResultSetResponse:
        pass

    @abstractmethod
    def connection_get_query_status(self, request: ConnectionGetQueryStatusRequest) -> ConnectionGetQueryStatusResponse:
        pass

    @abstractmethod
    def connection_abort_query(self, request: ConnectionAbortQueryRequest) -> ConnectionAbortQueryResponse:
        pass

    @abstractmethod
    def connection_upload_stream_begin(self, request: ConnectionUploadStreamBeginRequest) -> ConnectionUploadStreamBeginResponse:
        pass

    @abstractmethod
    def connection_upload_stream_chunk(self, request: ConnectionUploadStreamChunkRequest) -> ConnectionUploadStreamChunkResponse:
        pass

    @abstractmethod
    def connection_upload_stream_finish(self, request: ConnectionUploadStreamFinishRequest) -> ConnectionUploadStreamFinishResponse:
        pass

    @abstractmethod
    def connection_upload_stream_abort(self, request: ConnectionUploadStreamAbortRequest) -> ConnectionUploadStreamAbortResponse:
        pass

    @abstractmethod
    def connection_download_stream_begin(self, request: ConnectionDownloadStreamBeginRequest) -> ConnectionDownloadStreamBeginResponse:
        pass

    @abstractmethod
    def connection_download_stream_chunk(self, request: ConnectionDownloadStreamChunkRequest) -> ConnectionDownloadStreamChunkResponse:
        pass

    @abstractmethod
    def connection_download_stream_close(self, request: ConnectionDownloadStreamCloseRequest) -> ConnectionDownloadStreamCloseResponse:
        pass

    @abstractmethod
    def connection_send_http(self, request: ConnectionSendHttpRequest) -> ConnectionSendHttpResponse:
        pass

    @abstractmethod
    def connection_request_token(self, request: ConnectionTokenRequest) -> ConnectionTokenResponse:
        pass

    @abstractmethod
    def connection_heartbeat(self, request: ConnectionHeartbeatRequest) -> ConnectionHeartbeatResponse:
        pass

    @abstractmethod
    def statement_new(self, request: StatementNewRequest) -> StatementNewResponse:
        pass

    @abstractmethod
    def statement_release(self, request: StatementReleaseRequest) -> StatementReleaseResponse:
        pass

    @abstractmethod
    def statement_set_sql_query(self, request: StatementSetSqlQueryRequest) -> StatementSetSqlQueryResponse:
        pass

    @abstractmethod
    def statement_set_substrait_plan(self, request: StatementSetSubstraitPlanRequest) -> StatementSetSubstraitPlanResponse:
        pass

    @abstractmethod
    def statement_prepare(self, request: StatementPrepareRequest) -> StatementPrepareResponse:
        pass

    @abstractmethod
    def statement_set_options(self, request: StatementSetOptionsRequest) -> StatementSetOptionsResponse:
        pass

    @abstractmethod
    def statement_get_parameter_schema(self, request: StatementGetParameterSchemaRequest) -> StatementGetParameterSchemaResponse:
        pass

    @abstractmethod
    def statement_execute_query(self, request: StatementExecuteQueryRequest) -> ExecuteQueryResponse:
        pass

    @abstractmethod
    def statement_execute_partitions(self, request: StatementExecutePartitionsRequest) -> StatementExecutePartitionsResponse:
        pass

    @abstractmethod
    def statement_read_partition(self, request: StatementReadPartitionRequest) -> StatementReadPartitionResponse:
        pass

    @abstractmethod
    def statement_execute_async(self, request: StatementExecuteAsyncRequest) -> StatementExecuteAsyncResponse:
        pass

    @abstractmethod
    def result_set_get_stream(self, request: ResultSetGetStreamRequest) -> ResultSetGetStreamResponse:
        pass

    @abstractmethod
    def result_set_get_chunks(self, request: ResultSetGetChunksRequest) -> ResultSetGetChunksResponse:
        pass

    @abstractmethod
    def result_set_release(self, request: ResultSetReleaseRequest) -> ResultSetReleaseResponse:
        pass

    @abstractmethod
    def config_load_all_sections(self, request: ConfigLoadAllSectionsRequest) -> ConfigLoadAllSectionsResponse:
        pass

    @abstractmethod
    def config_get_paths(self, request: ConfigGetPathsRequest) -> ConfigGetPathsResponse:
        pass

    @abstractmethod
    def wif_create_attestation(self, request: WifCreateAttestationRequest) -> WifCreateAttestationResponse:
        pass

    @abstractmethod
    def telemetry_send_api_usage(self, request: TelemetrySendApiUsageRequest) -> TelemetrySendResponse:
        pass

    @abstractmethod
    def telemetry_send_wrapper_error(self, request: TelemetrySendWrapperErrorRequest) -> TelemetrySendResponse:
        pass

    @abstractmethod
    def telemetry_send_log(self, request: TelemetrySendLogRequest) -> TelemetrySendResponse:
        pass



class DatabaseDriverServer(DatabaseDriver):
    def handle_message(self, method: str, message_bytes: bytes) -> bytes:
        try:
            # Dispatch to appropriate method
            method_map = {
                'driver_get_fips_status': (self.driver_get_fips_status, DriverGetFipsStatusRequest),
                'database_new': (self.database_new, DatabaseNewRequest),
                'database_set_options': (self.database_set_options, DatabaseSetOptionsRequest),
                'database_init': (self.database_init, DatabaseInitRequest),
                'database_release': (self.database_release, DatabaseReleaseRequest),
                'database_fetch_chunk': (self.database_fetch_chunk, DatabaseFetchChunkRequest),
                'connection_new': (self.connection_new, ConnectionNewRequest),
                'connection_set_options': (self.connection_set_options, ConnectionSetOptionsRequest),
                'connection_init': (self.connection_init, ConnectionInitRequest),
                'connection_release': (self.connection_release, ConnectionReleaseRequest),
                'connection_close': (self.connection_close, ConnectionCloseRequest),
                'connection_is_closed': (self.connection_is_closed, ConnectionIsClosedRequest),
                'connection_is_expired': (self.connection_is_expired, ConnectionIsExpiredRequest),
                'connection_get_info': (self.connection_get_info, ConnectionGetInfoRequest),
                'connection_get_objects': (self.connection_get_objects, ConnectionGetObjectsRequest),
                'connection_get_table_schema': (self.connection_get_table_schema, ConnectionGetTableSchemaRequest),
                'connection_get_table_types': (self.connection_get_table_types, ConnectionGetTableTypesRequest),
                'connection_commit': (self.connection_commit, ConnectionCommitRequest),
                'connection_rollback': (self.connection_rollback, ConnectionRollbackRequest),
                'connection_set_autocommit': (self.connection_set_autocommit, ConnectionSetAutocommitRequest),
                'connection_use_database': (self.connection_use_database, ConnectionUseDatabaseRequest),
                'connection_use_schema': (self.connection_use_schema, ConnectionUseSchemaRequest),
                'connection_set_session_parameters': (self.connection_set_session_parameters, ConnectionSetSessionParametersRequest),
                'connection_get_parameter': (self.connection_get_parameter, ConnectionGetParameterRequest),
                'connection_get_all_parameters': (self.connection_get_all_parameters, ConnectionGetAllParametersRequest),
                'connection_get_server_version': (self.connection_get_server_version, ConnectionGetServerVersionRequest),
                'connection_validate_options': (self.connection_validate_options, ConnectionValidateOptionsRequest),
                'connection_get_query_result': (self.connection_get_query_result, ConnectionGetQueryResultRequest),
                'connection_get_result_set': (self.connection_get_result_set, ConnectionGetResultSetRequest),
                'connection_get_query_status': (self.connection_get_query_status, ConnectionGetQueryStatusRequest),
                'connection_abort_query': (self.connection_abort_query, ConnectionAbortQueryRequest),
                'connection_upload_stream_begin': (self.connection_upload_stream_begin, ConnectionUploadStreamBeginRequest),
                'connection_upload_stream_chunk': (self.connection_upload_stream_chunk, ConnectionUploadStreamChunkRequest),
                'connection_upload_stream_finish': (self.connection_upload_stream_finish, ConnectionUploadStreamFinishRequest),
                'connection_upload_stream_abort': (self.connection_upload_stream_abort, ConnectionUploadStreamAbortRequest),
                'connection_download_stream_begin': (self.connection_download_stream_begin, ConnectionDownloadStreamBeginRequest),
                'connection_download_stream_chunk': (self.connection_download_stream_chunk, ConnectionDownloadStreamChunkRequest),
                'connection_download_stream_close': (self.connection_download_stream_close, ConnectionDownloadStreamCloseRequest),
                'connection_send_http': (self.connection_send_http, ConnectionSendHttpRequest),
                'connection_request_token': (self.connection_request_token, ConnectionTokenRequest),
                'connection_heartbeat': (self.connection_heartbeat, ConnectionHeartbeatRequest),
                'statement_new': (self.statement_new, StatementNewRequest),
                'statement_release': (self.statement_release, StatementReleaseRequest),
                'statement_set_sql_query': (self.statement_set_sql_query, StatementSetSqlQueryRequest),
                'statement_set_substrait_plan': (self.statement_set_substrait_plan, StatementSetSubstraitPlanRequest),
                'statement_prepare': (self.statement_prepare, StatementPrepareRequest),
                'statement_set_options': (self.statement_set_options, StatementSetOptionsRequest),
                'statement_get_parameter_schema': (self.statement_get_parameter_schema, StatementGetParameterSchemaRequest),
                'statement_execute_query': (self.statement_execute_query, StatementExecuteQueryRequest),
                'statement_execute_partitions': (self.statement_execute_partitions, StatementExecutePartitionsRequest),
                'statement_read_partition': (self.statement_read_partition, StatementReadPartitionRequest),
                'statement_execute_async': (self.statement_execute_async, StatementExecuteAsyncRequest),
                'result_set_get_stream': (self.result_set_get_stream, ResultSetGetStreamRequest),
                'result_set_get_chunks': (self.result_set_get_chunks, ResultSetGetChunksRequest),
                'result_set_release': (self.result_set_release, ResultSetReleaseRequest),
                'config_load_all_sections': (self.config_load_all_sections, ConfigLoadAllSectionsRequest),
                'config_get_paths': (self.config_get_paths, ConfigGetPathsRequest),
                'wif_create_attestation': (self.wif_create_attestation, WifCreateAttestationRequest),
                'telemetry_send_api_usage': (self.telemetry_send_api_usage, TelemetrySendApiUsageRequest),
                'telemetry_send_wrapper_error': (self.telemetry_send_wrapper_error, TelemetrySendWrapperErrorRequest),
                'telemetry_send_log': (self.telemetry_send_log, TelemetrySendLogRequest)
            }
            
            if method not in method_map:
                raise ProtoError('Transport', f'Unknown method: {method}')
                
            handler, request_class = method_map[method]
            request = request_class()
            request.ParseFromString(message_bytes)
            response = handler(request)
            return response.SerializeToString()
            
        except Exception as e:
            raise ProtoError('Transport', str(e))

class DatabaseDriverClient:
    def __init__(self, transport, error_handler=None):
        """
        Args:
            transport: Transport layer that handles message serialization.
            error_handler: Optional callable that converts a proto-layer exception
                into a public exception.  Must **return** the converted exception
                (not raise it); ``_raise_error`` takes care of raising.
        """
        self._transport = transport
        self._error_handler = error_handler

    def _raise_error(self, exc):
        if self._error_handler is not None:
            raise self._error_handler(exc) from None
        raise exc

    def driver_get_fips_status(self, request: DriverGetFipsStatusRequest) -> DriverGetFipsStatusResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'driver_get_fips_status', request.SerializeToString())
        if code == 0:
            response = DriverGetFipsStatusResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def database_new(self, request: DatabaseNewRequest) -> DatabaseNewResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'database_new', request.SerializeToString())
        if code == 0:
            response = DatabaseNewResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def database_set_options(self, request: DatabaseSetOptionsRequest) -> DatabaseSetOptionsResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'database_set_options', request.SerializeToString())
        if code == 0:
            response = DatabaseSetOptionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def database_init(self, request: DatabaseInitRequest) -> DatabaseInitResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'database_init', request.SerializeToString())
        if code == 0:
            response = DatabaseInitResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def database_release(self, request: DatabaseReleaseRequest) -> DatabaseReleaseResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'database_release', request.SerializeToString())
        if code == 0:
            response = DatabaseReleaseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def database_fetch_chunk(self, request: DatabaseFetchChunkRequest) -> DatabaseFetchChunkResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'database_fetch_chunk', request.SerializeToString())
        if code == 0:
            response = DatabaseFetchChunkResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_new(self, request: ConnectionNewRequest) -> ConnectionNewResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_new', request.SerializeToString())
        if code == 0:
            response = ConnectionNewResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_set_options(self, request: ConnectionSetOptionsRequest) -> ConnectionSetOptionsResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_set_options', request.SerializeToString())
        if code == 0:
            response = ConnectionSetOptionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_init(self, request: ConnectionInitRequest) -> ConnectionInitResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_init', request.SerializeToString())
        if code == 0:
            response = ConnectionInitResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_release(self, request: ConnectionReleaseRequest) -> ConnectionReleaseResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_release', request.SerializeToString())
        if code == 0:
            response = ConnectionReleaseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_close(self, request: ConnectionCloseRequest) -> ConnectionCloseResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_close', request.SerializeToString())
        if code == 0:
            response = ConnectionCloseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_is_closed(self, request: ConnectionIsClosedRequest) -> ConnectionIsClosedResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_is_closed', request.SerializeToString())
        if code == 0:
            response = ConnectionIsClosedResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_is_expired(self, request: ConnectionIsExpiredRequest) -> ConnectionIsExpiredResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_is_expired', request.SerializeToString())
        if code == 0:
            response = ConnectionIsExpiredResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_get_info(self, request: ConnectionGetInfoRequest) -> ConnectionGetInfoResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_get_info', request.SerializeToString())
        if code == 0:
            response = ConnectionGetInfoResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_get_objects(self, request: ConnectionGetObjectsRequest) -> ConnectionGetObjectsResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_get_objects', request.SerializeToString())
        if code == 0:
            response = ConnectionGetObjectsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_get_table_schema(self, request: ConnectionGetTableSchemaRequest) -> ConnectionGetTableSchemaResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_get_table_schema', request.SerializeToString())
        if code == 0:
            response = ConnectionGetTableSchemaResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_get_table_types(self, request: ConnectionGetTableTypesRequest) -> ConnectionGetTableTypesResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_get_table_types', request.SerializeToString())
        if code == 0:
            response = ConnectionGetTableTypesResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_commit(self, request: ConnectionCommitRequest) -> ConnectionCommitResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_commit', request.SerializeToString())
        if code == 0:
            response = ConnectionCommitResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_rollback(self, request: ConnectionRollbackRequest) -> ConnectionRollbackResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_rollback', request.SerializeToString())
        if code == 0:
            response = ConnectionRollbackResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_set_autocommit(self, request: ConnectionSetAutocommitRequest) -> ConnectionSetAutocommitResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_set_autocommit', request.SerializeToString())
        if code == 0:
            response = ConnectionSetAutocommitResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_use_database(self, request: ConnectionUseDatabaseRequest) -> ConnectionUseDatabaseResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_use_database', request.SerializeToString())
        if code == 0:
            response = ConnectionUseDatabaseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_use_schema(self, request: ConnectionUseSchemaRequest) -> ConnectionUseSchemaResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_use_schema', request.SerializeToString())
        if code == 0:
            response = ConnectionUseSchemaResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_set_session_parameters(self, request: ConnectionSetSessionParametersRequest) -> ConnectionSetSessionParametersResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_set_session_parameters', request.SerializeToString())
        if code == 0:
            response = ConnectionSetSessionParametersResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_get_parameter(self, request: ConnectionGetParameterRequest) -> ConnectionGetParameterResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_get_parameter', request.SerializeToString())
        if code == 0:
            response = ConnectionGetParameterResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_get_all_parameters(self, request: ConnectionGetAllParametersRequest) -> ConnectionGetAllParametersResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_get_all_parameters', request.SerializeToString())
        if code == 0:
            response = ConnectionGetAllParametersResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_get_server_version(self, request: ConnectionGetServerVersionRequest) -> ConnectionGetServerVersionResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_get_server_version', request.SerializeToString())
        if code == 0:
            response = ConnectionGetServerVersionResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_validate_options(self, request: ConnectionValidateOptionsRequest) -> ConnectionValidateOptionsResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_validate_options', request.SerializeToString())
        if code == 0:
            response = ConnectionValidateOptionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_get_query_result(self, request: ConnectionGetQueryResultRequest) -> ExecuteQueryResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_get_query_result', request.SerializeToString())
        if code == 0:
            response = ExecuteQueryResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_get_result_set(self, request: ConnectionGetResultSetRequest) -> ResultSetResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_get_result_set', request.SerializeToString())
        if code == 0:
            response = ResultSetResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_get_query_status(self, request: ConnectionGetQueryStatusRequest) -> ConnectionGetQueryStatusResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_get_query_status', request.SerializeToString())
        if code == 0:
            response = ConnectionGetQueryStatusResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_abort_query(self, request: ConnectionAbortQueryRequest) -> ConnectionAbortQueryResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_abort_query', request.SerializeToString())
        if code == 0:
            response = ConnectionAbortQueryResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_upload_stream_begin(self, request: ConnectionUploadStreamBeginRequest) -> ConnectionUploadStreamBeginResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_upload_stream_begin', request.SerializeToString())
        if code == 0:
            response = ConnectionUploadStreamBeginResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_upload_stream_chunk(self, request: ConnectionUploadStreamChunkRequest) -> ConnectionUploadStreamChunkResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_upload_stream_chunk', request.SerializeToString())
        if code == 0:
            response = ConnectionUploadStreamChunkResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_upload_stream_finish(self, request: ConnectionUploadStreamFinishRequest) -> ConnectionUploadStreamFinishResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_upload_stream_finish', request.SerializeToString())
        if code == 0:
            response = ConnectionUploadStreamFinishResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_upload_stream_abort(self, request: ConnectionUploadStreamAbortRequest) -> ConnectionUploadStreamAbortResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_upload_stream_abort', request.SerializeToString())
        if code == 0:
            response = ConnectionUploadStreamAbortResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_download_stream_begin(self, request: ConnectionDownloadStreamBeginRequest) -> ConnectionDownloadStreamBeginResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_download_stream_begin', request.SerializeToString())
        if code == 0:
            response = ConnectionDownloadStreamBeginResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_download_stream_chunk(self, request: ConnectionDownloadStreamChunkRequest) -> ConnectionDownloadStreamChunkResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_download_stream_chunk', request.SerializeToString())
        if code == 0:
            response = ConnectionDownloadStreamChunkResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_download_stream_close(self, request: ConnectionDownloadStreamCloseRequest) -> ConnectionDownloadStreamCloseResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_download_stream_close', request.SerializeToString())
        if code == 0:
            response = ConnectionDownloadStreamCloseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_send_http(self, request: ConnectionSendHttpRequest) -> ConnectionSendHttpResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_send_http', request.SerializeToString())
        if code == 0:
            response = ConnectionSendHttpResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_request_token(self, request: ConnectionTokenRequest) -> ConnectionTokenResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_request_token', request.SerializeToString())
        if code == 0:
            response = ConnectionTokenResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def connection_heartbeat(self, request: ConnectionHeartbeatRequest) -> ConnectionHeartbeatResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'connection_heartbeat', request.SerializeToString())
        if code == 0:
            response = ConnectionHeartbeatResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_new(self, request: StatementNewRequest) -> StatementNewResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_new', request.SerializeToString())
        if code == 0:
            response = StatementNewResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_release(self, request: StatementReleaseRequest) -> StatementReleaseResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_release', request.SerializeToString())
        if code == 0:
            response = StatementReleaseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_set_sql_query(self, request: StatementSetSqlQueryRequest) -> StatementSetSqlQueryResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_set_sql_query', request.SerializeToString())
        if code == 0:
            response = StatementSetSqlQueryResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_set_substrait_plan(self, request: StatementSetSubstraitPlanRequest) -> StatementSetSubstraitPlanResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_set_substrait_plan', request.SerializeToString())
        if code == 0:
            response = StatementSetSubstraitPlanResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_prepare(self, request: StatementPrepareRequest) -> StatementPrepareResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_prepare', request.SerializeToString())
        if code == 0:
            response = StatementPrepareResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_set_options(self, request: StatementSetOptionsRequest) -> StatementSetOptionsResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_set_options', request.SerializeToString())
        if code == 0:
            response = StatementSetOptionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_get_parameter_schema(self, request: StatementGetParameterSchemaRequest) -> StatementGetParameterSchemaResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_get_parameter_schema', request.SerializeToString())
        if code == 0:
            response = StatementGetParameterSchemaResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_execute_query(self, request: StatementExecuteQueryRequest) -> ExecuteQueryResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_execute_query', request.SerializeToString())
        if code == 0:
            response = ExecuteQueryResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_execute_partitions(self, request: StatementExecutePartitionsRequest) -> StatementExecutePartitionsResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_execute_partitions', request.SerializeToString())
        if code == 0:
            response = StatementExecutePartitionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_read_partition(self, request: StatementReadPartitionRequest) -> StatementReadPartitionResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_read_partition', request.SerializeToString())
        if code == 0:
            response = StatementReadPartitionResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def statement_execute_async(self, request: StatementExecuteAsyncRequest) -> StatementExecuteAsyncResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'statement_execute_async', request.SerializeToString())
        if code == 0:
            response = StatementExecuteAsyncResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def result_set_get_stream(self, request: ResultSetGetStreamRequest) -> ResultSetGetStreamResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'result_set_get_stream', request.SerializeToString())
        if code == 0:
            response = ResultSetGetStreamResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def result_set_get_chunks(self, request: ResultSetGetChunksRequest) -> ResultSetGetChunksResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'result_set_get_chunks', request.SerializeToString())
        if code == 0:
            response = ResultSetGetChunksResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def result_set_release(self, request: ResultSetReleaseRequest) -> ResultSetReleaseResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'result_set_release', request.SerializeToString())
        if code == 0:
            response = ResultSetReleaseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def config_load_all_sections(self, request: ConfigLoadAllSectionsRequest) -> ConfigLoadAllSectionsResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'config_load_all_sections', request.SerializeToString())
        if code == 0:
            response = ConfigLoadAllSectionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def config_get_paths(self, request: ConfigGetPathsRequest) -> ConfigGetPathsResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'config_get_paths', request.SerializeToString())
        if code == 0:
            response = ConfigGetPathsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def wif_create_attestation(self, request: WifCreateAttestationRequest) -> WifCreateAttestationResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'wif_create_attestation', request.SerializeToString())
        if code == 0:
            response = WifCreateAttestationResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def telemetry_send_api_usage(self, request: TelemetrySendApiUsageRequest) -> TelemetrySendResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'telemetry_send_api_usage', request.SerializeToString())
        if code == 0:
            response = TelemetrySendResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def telemetry_send_wrapper_error(self, request: TelemetrySendWrapperErrorRequest) -> TelemetrySendResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'telemetry_send_wrapper_error', request.SerializeToString())
        if code == 0:
            response = TelemetrySendResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    def telemetry_send_log(self, request: TelemetrySendLogRequest) -> TelemetrySendResponse:
        (code, response_bytes) = self._transport.handle_message('DatabaseDriver', 'telemetry_send_log', request.SerializeToString())
        if code == 0:
            response = TelemetrySendResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
class AsyncDatabaseDriverClient:
    """Asynchronous DatabaseDriver client.

    Each RPC awaits ``transport.handle_message_async``, which runs the
    blocking FFI call on a worker thread so the event loop is not blocked.
    This is a separate code path from the synchronous ``DatabaseDriverClient``.
    """

    def __init__(self, transport, error_handler=None):
        """
        Args:
            transport: Transport layer that handles message serialization.
            error_handler: Optional callable that converts a proto-layer exception
                into a public exception.  Must **return** the converted exception
                (not raise it); ``_raise_error`` takes care of raising.
        """
        self._transport = transport
        self._error_handler = error_handler

    def _raise_error(self, exc):
        if self._error_handler is not None:
            raise self._error_handler(exc) from None
        raise exc

    async def driver_get_fips_status(self, request: DriverGetFipsStatusRequest) -> DriverGetFipsStatusResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'driver_get_fips_status', request.SerializeToString())
        if code == 0:
            response = DriverGetFipsStatusResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def database_new(self, request: DatabaseNewRequest) -> DatabaseNewResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'database_new', request.SerializeToString())
        if code == 0:
            response = DatabaseNewResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def database_set_options(self, request: DatabaseSetOptionsRequest) -> DatabaseSetOptionsResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'database_set_options', request.SerializeToString())
        if code == 0:
            response = DatabaseSetOptionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def database_init(self, request: DatabaseInitRequest) -> DatabaseInitResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'database_init', request.SerializeToString())
        if code == 0:
            response = DatabaseInitResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def database_release(self, request: DatabaseReleaseRequest) -> DatabaseReleaseResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'database_release', request.SerializeToString())
        if code == 0:
            response = DatabaseReleaseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def database_fetch_chunk(self, request: DatabaseFetchChunkRequest) -> DatabaseFetchChunkResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'database_fetch_chunk', request.SerializeToString())
        if code == 0:
            response = DatabaseFetchChunkResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_new(self, request: ConnectionNewRequest) -> ConnectionNewResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_new', request.SerializeToString())
        if code == 0:
            response = ConnectionNewResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_set_options(self, request: ConnectionSetOptionsRequest) -> ConnectionSetOptionsResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_set_options', request.SerializeToString())
        if code == 0:
            response = ConnectionSetOptionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_init(self, request: ConnectionInitRequest) -> ConnectionInitResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_init', request.SerializeToString())
        if code == 0:
            response = ConnectionInitResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_release(self, request: ConnectionReleaseRequest) -> ConnectionReleaseResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_release', request.SerializeToString())
        if code == 0:
            response = ConnectionReleaseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_close(self, request: ConnectionCloseRequest) -> ConnectionCloseResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_close', request.SerializeToString())
        if code == 0:
            response = ConnectionCloseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_is_closed(self, request: ConnectionIsClosedRequest) -> ConnectionIsClosedResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_is_closed', request.SerializeToString())
        if code == 0:
            response = ConnectionIsClosedResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_is_expired(self, request: ConnectionIsExpiredRequest) -> ConnectionIsExpiredResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_is_expired', request.SerializeToString())
        if code == 0:
            response = ConnectionIsExpiredResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_get_info(self, request: ConnectionGetInfoRequest) -> ConnectionGetInfoResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_get_info', request.SerializeToString())
        if code == 0:
            response = ConnectionGetInfoResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_get_objects(self, request: ConnectionGetObjectsRequest) -> ConnectionGetObjectsResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_get_objects', request.SerializeToString())
        if code == 0:
            response = ConnectionGetObjectsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_get_table_schema(self, request: ConnectionGetTableSchemaRequest) -> ConnectionGetTableSchemaResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_get_table_schema', request.SerializeToString())
        if code == 0:
            response = ConnectionGetTableSchemaResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_get_table_types(self, request: ConnectionGetTableTypesRequest) -> ConnectionGetTableTypesResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_get_table_types', request.SerializeToString())
        if code == 0:
            response = ConnectionGetTableTypesResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_commit(self, request: ConnectionCommitRequest) -> ConnectionCommitResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_commit', request.SerializeToString())
        if code == 0:
            response = ConnectionCommitResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_rollback(self, request: ConnectionRollbackRequest) -> ConnectionRollbackResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_rollback', request.SerializeToString())
        if code == 0:
            response = ConnectionRollbackResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_set_autocommit(self, request: ConnectionSetAutocommitRequest) -> ConnectionSetAutocommitResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_set_autocommit', request.SerializeToString())
        if code == 0:
            response = ConnectionSetAutocommitResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_use_database(self, request: ConnectionUseDatabaseRequest) -> ConnectionUseDatabaseResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_use_database', request.SerializeToString())
        if code == 0:
            response = ConnectionUseDatabaseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_use_schema(self, request: ConnectionUseSchemaRequest) -> ConnectionUseSchemaResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_use_schema', request.SerializeToString())
        if code == 0:
            response = ConnectionUseSchemaResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_set_session_parameters(self, request: ConnectionSetSessionParametersRequest) -> ConnectionSetSessionParametersResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_set_session_parameters', request.SerializeToString())
        if code == 0:
            response = ConnectionSetSessionParametersResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_get_parameter(self, request: ConnectionGetParameterRequest) -> ConnectionGetParameterResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_get_parameter', request.SerializeToString())
        if code == 0:
            response = ConnectionGetParameterResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_get_all_parameters(self, request: ConnectionGetAllParametersRequest) -> ConnectionGetAllParametersResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_get_all_parameters', request.SerializeToString())
        if code == 0:
            response = ConnectionGetAllParametersResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_get_server_version(self, request: ConnectionGetServerVersionRequest) -> ConnectionGetServerVersionResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_get_server_version', request.SerializeToString())
        if code == 0:
            response = ConnectionGetServerVersionResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_validate_options(self, request: ConnectionValidateOptionsRequest) -> ConnectionValidateOptionsResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_validate_options', request.SerializeToString())
        if code == 0:
            response = ConnectionValidateOptionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_get_query_result(self, request: ConnectionGetQueryResultRequest) -> ExecuteQueryResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_get_query_result', request.SerializeToString())
        if code == 0:
            response = ExecuteQueryResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_get_result_set(self, request: ConnectionGetResultSetRequest) -> ResultSetResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_get_result_set', request.SerializeToString())
        if code == 0:
            response = ResultSetResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_get_query_status(self, request: ConnectionGetQueryStatusRequest) -> ConnectionGetQueryStatusResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_get_query_status', request.SerializeToString())
        if code == 0:
            response = ConnectionGetQueryStatusResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_abort_query(self, request: ConnectionAbortQueryRequest) -> ConnectionAbortQueryResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_abort_query', request.SerializeToString())
        if code == 0:
            response = ConnectionAbortQueryResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_upload_stream_begin(self, request: ConnectionUploadStreamBeginRequest) -> ConnectionUploadStreamBeginResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_upload_stream_begin', request.SerializeToString())
        if code == 0:
            response = ConnectionUploadStreamBeginResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_upload_stream_chunk(self, request: ConnectionUploadStreamChunkRequest) -> ConnectionUploadStreamChunkResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_upload_stream_chunk', request.SerializeToString())
        if code == 0:
            response = ConnectionUploadStreamChunkResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_upload_stream_finish(self, request: ConnectionUploadStreamFinishRequest) -> ConnectionUploadStreamFinishResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_upload_stream_finish', request.SerializeToString())
        if code == 0:
            response = ConnectionUploadStreamFinishResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_upload_stream_abort(self, request: ConnectionUploadStreamAbortRequest) -> ConnectionUploadStreamAbortResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_upload_stream_abort', request.SerializeToString())
        if code == 0:
            response = ConnectionUploadStreamAbortResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_download_stream_begin(self, request: ConnectionDownloadStreamBeginRequest) -> ConnectionDownloadStreamBeginResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_download_stream_begin', request.SerializeToString())
        if code == 0:
            response = ConnectionDownloadStreamBeginResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_download_stream_chunk(self, request: ConnectionDownloadStreamChunkRequest) -> ConnectionDownloadStreamChunkResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_download_stream_chunk', request.SerializeToString())
        if code == 0:
            response = ConnectionDownloadStreamChunkResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_download_stream_close(self, request: ConnectionDownloadStreamCloseRequest) -> ConnectionDownloadStreamCloseResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_download_stream_close', request.SerializeToString())
        if code == 0:
            response = ConnectionDownloadStreamCloseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_send_http(self, request: ConnectionSendHttpRequest) -> ConnectionSendHttpResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_send_http', request.SerializeToString())
        if code == 0:
            response = ConnectionSendHttpResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_request_token(self, request: ConnectionTokenRequest) -> ConnectionTokenResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_request_token', request.SerializeToString())
        if code == 0:
            response = ConnectionTokenResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def connection_heartbeat(self, request: ConnectionHeartbeatRequest) -> ConnectionHeartbeatResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'connection_heartbeat', request.SerializeToString())
        if code == 0:
            response = ConnectionHeartbeatResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_new(self, request: StatementNewRequest) -> StatementNewResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_new', request.SerializeToString())
        if code == 0:
            response = StatementNewResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_release(self, request: StatementReleaseRequest) -> StatementReleaseResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_release', request.SerializeToString())
        if code == 0:
            response = StatementReleaseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_set_sql_query(self, request: StatementSetSqlQueryRequest) -> StatementSetSqlQueryResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_set_sql_query', request.SerializeToString())
        if code == 0:
            response = StatementSetSqlQueryResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_set_substrait_plan(self, request: StatementSetSubstraitPlanRequest) -> StatementSetSubstraitPlanResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_set_substrait_plan', request.SerializeToString())
        if code == 0:
            response = StatementSetSubstraitPlanResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_prepare(self, request: StatementPrepareRequest) -> StatementPrepareResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_prepare', request.SerializeToString())
        if code == 0:
            response = StatementPrepareResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_set_options(self, request: StatementSetOptionsRequest) -> StatementSetOptionsResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_set_options', request.SerializeToString())
        if code == 0:
            response = StatementSetOptionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_get_parameter_schema(self, request: StatementGetParameterSchemaRequest) -> StatementGetParameterSchemaResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_get_parameter_schema', request.SerializeToString())
        if code == 0:
            response = StatementGetParameterSchemaResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_execute_query(self, request: StatementExecuteQueryRequest) -> ExecuteQueryResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_execute_query', request.SerializeToString())
        if code == 0:
            response = ExecuteQueryResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_execute_partitions(self, request: StatementExecutePartitionsRequest) -> StatementExecutePartitionsResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_execute_partitions', request.SerializeToString())
        if code == 0:
            response = StatementExecutePartitionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_read_partition(self, request: StatementReadPartitionRequest) -> StatementReadPartitionResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_read_partition', request.SerializeToString())
        if code == 0:
            response = StatementReadPartitionResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def statement_execute_async(self, request: StatementExecuteAsyncRequest) -> StatementExecuteAsyncResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'statement_execute_async', request.SerializeToString())
        if code == 0:
            response = StatementExecuteAsyncResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def result_set_get_stream(self, request: ResultSetGetStreamRequest) -> ResultSetGetStreamResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'result_set_get_stream', request.SerializeToString())
        if code == 0:
            response = ResultSetGetStreamResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def result_set_get_chunks(self, request: ResultSetGetChunksRequest) -> ResultSetGetChunksResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'result_set_get_chunks', request.SerializeToString())
        if code == 0:
            response = ResultSetGetChunksResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def result_set_release(self, request: ResultSetReleaseRequest) -> ResultSetReleaseResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'result_set_release', request.SerializeToString())
        if code == 0:
            response = ResultSetReleaseResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def config_load_all_sections(self, request: ConfigLoadAllSectionsRequest) -> ConfigLoadAllSectionsResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'config_load_all_sections', request.SerializeToString())
        if code == 0:
            response = ConfigLoadAllSectionsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def config_get_paths(self, request: ConfigGetPathsRequest) -> ConfigGetPathsResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'config_get_paths', request.SerializeToString())
        if code == 0:
            response = ConfigGetPathsResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def wif_create_attestation(self, request: WifCreateAttestationRequest) -> WifCreateAttestationResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'wif_create_attestation', request.SerializeToString())
        if code == 0:
            response = WifCreateAttestationResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def telemetry_send_api_usage(self, request: TelemetrySendApiUsageRequest) -> TelemetrySendResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'telemetry_send_api_usage', request.SerializeToString())
        if code == 0:
            response = TelemetrySendResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def telemetry_send_wrapper_error(self, request: TelemetrySendWrapperErrorRequest) -> TelemetrySendResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'telemetry_send_wrapper_error', request.SerializeToString())
        if code == 0:
            response = TelemetrySendResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
    async def telemetry_send_log(self, request: TelemetrySendLogRequest) -> TelemetrySendResponse:
        (code, response_bytes) = await self._transport.handle_message_async('DatabaseDriver', 'telemetry_send_log', request.SerializeToString())
        if code == 0:
            response = TelemetrySendResponse()
            response.ParseFromString(response_bytes)
            return response
        elif code == 1:
            error = DriverException()
            error.ParseFromString(response_bytes)
            self._raise_error(ProtoApplicationException(error))
        elif code == 2:
            self._raise_error(ProtoTransportException(str(response_bytes)))
        else:
            self._raise_error(ProtoTransportException(f"Unknown error code: %s", code))
