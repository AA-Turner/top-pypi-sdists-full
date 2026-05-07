from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class ExecuteSqlAsyncExecutionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXECUTE_SQL_ASYNC_EXECUTION_MODE_UNSPECIFIED: _ClassVar[ExecuteSqlAsyncExecutionMode]
    EXECUTE_SQL_ASYNC_EXECUTION_MODE_IN_PROCESS: _ClassVar[ExecuteSqlAsyncExecutionMode]
    EXECUTE_SQL_ASYNC_EXECUTION_MODE_ASYNC: _ClassVar[ExecuteSqlAsyncExecutionMode]

EXECUTE_SQL_ASYNC_EXECUTION_MODE_UNSPECIFIED: ExecuteSqlAsyncExecutionMode
EXECUTE_SQL_ASYNC_EXECUTION_MODE_IN_PROCESS: ExecuteSqlAsyncExecutionMode
EXECUTE_SQL_ASYNC_EXECUTION_MODE_ASYNC: ExecuteSqlAsyncExecutionMode

class SqlQueryInfo(_message.Message):
    __slots__ = ("operation_id", "created_at", "finished_at")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    created_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ExecuteSqlSyncQueryRequestOptions(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ExecuteSqlAsyncQueryRequestOptions(_message.Message):
    __slots__ = ("execution_mode", "resource_group")
    EXECUTION_MODE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    execution_mode: ExecuteSqlAsyncExecutionMode
    resource_group: str
    def __init__(
        self,
        execution_mode: _Optional[_Union[ExecuteSqlAsyncExecutionMode, str]] = ...,
        resource_group: _Optional[str] = ...,
    ) -> None: ...

class ExecuteSqlResultPersistenceSettings(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class ExecuteSqlQueryRequest(_message.Message):
    __slots__ = ("query", "correlation_id", "persistence_settings", "max_memory_bytes", "sync_options", "async_options")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    MAX_MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    SYNC_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    ASYNC_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    query: str
    correlation_id: str
    persistence_settings: ExecuteSqlResultPersistenceSettings
    max_memory_bytes: int
    sync_options: ExecuteSqlSyncQueryRequestOptions
    async_options: ExecuteSqlAsyncQueryRequestOptions
    def __init__(
        self,
        query: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        persistence_settings: _Optional[_Union[ExecuteSqlResultPersistenceSettings, _Mapping]] = ...,
        max_memory_bytes: _Optional[int] = ...,
        sync_options: _Optional[_Union[ExecuteSqlSyncQueryRequestOptions, _Mapping]] = ...,
        async_options: _Optional[_Union[ExecuteSqlAsyncQueryRequestOptions, _Mapping]] = ...,
    ) -> None: ...

class SignedOutputUris(_message.Message):
    __slots__ = ("uris",)
    URIS_FIELD_NUMBER: _ClassVar[int]
    uris: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uris: _Optional[_Iterable[str]] = ...) -> None: ...

class ExecuteSqlSyncQueryResponsePayload(_message.Message):
    __slots__ = ("parquet_response", "signed_output_uris")
    PARQUET_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SIGNED_OUTPUT_URIS_FIELD_NUMBER: _ClassVar[int]
    parquet_response: bytes
    signed_output_uris: SignedOutputUris
    def __init__(
        self,
        parquet_response: _Optional[bytes] = ...,
        signed_output_uris: _Optional[_Union[SignedOutputUris, _Mapping]] = ...,
    ) -> None: ...

class ExecuteSqlAsyncQueryResponsePayload(_message.Message):
    __slots__ = ("operation_id", "execution_mode")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_MODE_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    execution_mode: ExecuteSqlAsyncExecutionMode
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        execution_mode: _Optional[_Union[ExecuteSqlAsyncExecutionMode, str]] = ...,
    ) -> None: ...

class ExecuteSqlQueryResponse(_message.Message):
    __slots__ = ("query_id", "parquet", "sync_payload", "async_payload", "errors")
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    PARQUET_FIELD_NUMBER: _ClassVar[int]
    SYNC_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ASYNC_PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    parquet: bytes
    sync_payload: ExecuteSqlSyncQueryResponsePayload
    async_payload: ExecuteSqlAsyncQueryResponsePayload
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        query_id: _Optional[str] = ...,
        parquet: _Optional[bytes] = ...,
        sync_payload: _Optional[_Union[ExecuteSqlSyncQueryResponsePayload, _Mapping]] = ...,
        async_payload: _Optional[_Union[ExecuteSqlAsyncQueryResponsePayload, _Mapping]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class PlanSqlQueryRequest(_message.Message):
    __slots__ = ("query",)
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class PlanSqlQueryResponse(_message.Message):
    __slots__ = ("logical_plan", "errors")
    LOGICAL_PLAN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    logical_plan: str
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        logical_plan: _Optional[str] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class GetDbCatalogsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDbCatalogsResponse(_message.Message):
    __slots__ = ("catalog_names", "errors")
    CATALOG_NAMES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    catalog_names: _containers.RepeatedScalarFieldContainer[str]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        catalog_names: _Optional[_Iterable[str]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class GetDbSchemasRequest(_message.Message):
    __slots__ = ("catalog", "db_schema_filter_pattern", "errors")
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    DB_SCHEMA_FILTER_PATTERN_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    catalog: str
    db_schema_filter_pattern: str
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        catalog: _Optional[str] = ...,
        db_schema_filter_pattern: _Optional[str] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class DbSchemaInfo(_message.Message):
    __slots__ = ("catalog_name", "db_schema_name")
    CATALOG_NAME_FIELD_NUMBER: _ClassVar[int]
    DB_SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    catalog_name: str
    db_schema_name: str
    def __init__(self, catalog_name: _Optional[str] = ..., db_schema_name: _Optional[str] = ...) -> None: ...

class GetDbSchemasResponse(_message.Message):
    __slots__ = ("schemas", "errors")
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    schemas: _containers.RepeatedCompositeFieldContainer[DbSchemaInfo]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        schemas: _Optional[_Iterable[_Union[DbSchemaInfo, _Mapping]]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class GetTablesRequest(_message.Message):
    __slots__ = ("catalog", "db_schema_filter_pattern", "table_name_filter_pattern", "include_schemas")
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    DB_SCHEMA_FILTER_PATTERN_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FILTER_PATTERN_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    catalog: str
    db_schema_filter_pattern: str
    table_name_filter_pattern: str
    include_schemas: bool
    def __init__(
        self,
        catalog: _Optional[str] = ...,
        db_schema_filter_pattern: _Optional[str] = ...,
        table_name_filter_pattern: _Optional[str] = ...,
        include_schemas: bool = ...,
    ) -> None: ...

class TableInfo(_message.Message):
    __slots__ = ("catalog_name", "db_schema_name", "table_name", "table_arrow_schema")
    CATALOG_NAME_FIELD_NUMBER: _ClassVar[int]
    DB_SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_ARROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    catalog_name: str
    db_schema_name: str
    table_name: str
    table_arrow_schema: bytes
    def __init__(
        self,
        catalog_name: _Optional[str] = ...,
        db_schema_name: _Optional[str] = ...,
        table_name: _Optional[str] = ...,
        table_arrow_schema: _Optional[bytes] = ...,
    ) -> None: ...

class GetTablesResponse(_message.Message):
    __slots__ = ("tables", "errors")
    TABLES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    tables: _containers.RepeatedCompositeFieldContainer[TableInfo]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        tables: _Optional[_Iterable[_Union[TableInfo, _Mapping]]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class SqlQueryProgressInfo(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SqlQueryFailedInfo(_message.Message):
    __slots__ = ("errors",)
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(self, errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...) -> None: ...

class PollSqlQueryRequest(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...

class PollSqlQueryResponse(_message.Message):
    __slots__ = ("info", "progress", "response", "failed")
    INFO_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    info: SqlQueryInfo
    progress: SqlQueryProgressInfo
    response: ExecuteSqlSyncQueryResponsePayload
    failed: SqlQueryFailedInfo
    def __init__(
        self,
        info: _Optional[_Union[SqlQueryInfo, _Mapping]] = ...,
        progress: _Optional[_Union[SqlQueryProgressInfo, _Mapping]] = ...,
        response: _Optional[_Union[ExecuteSqlSyncQueryResponsePayload, _Mapping]] = ...,
        failed: _Optional[_Union[SqlQueryFailedInfo, _Mapping]] = ...,
    ) -> None: ...
