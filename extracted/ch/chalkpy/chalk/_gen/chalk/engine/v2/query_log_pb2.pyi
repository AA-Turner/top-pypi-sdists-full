from chalk._gen.chalk.common.v1 import operation_kind_pb2 as _operation_kind_pb2
from chalk._gen.chalk.common.v1 import query_status_pb2 as _query_status_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
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

class VersionedQueryName(_message.Message):
    __slots__ = ("query_name", "query_name_version")
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_VERSION_FIELD_NUMBER: _ClassVar[int]
    query_name: str
    query_name_version: str
    def __init__(self, query_name: _Optional[str] = ..., query_name_version: _Optional[str] = ...) -> None: ...

class QueryLogFilters(_message.Message):
    __slots__ = (
        "operation_id",
        "operation_kind",
        "query_name",
        "agent_id",
        "branch_name",
        "correlation_id",
        "trace_id",
        "query_plan_id",
        "deployment_id",
        "query_status",
        "meta_query_hash",
    )
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_KIND_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_STATUS_FIELD_NUMBER: _ClassVar[int]
    META_QUERY_HASH_FIELD_NUMBER: _ClassVar[int]
    operation_id: _containers.RepeatedScalarFieldContainer[str]
    operation_kind: _containers.RepeatedScalarFieldContainer[_operation_kind_pb2.OperationKind]
    query_name: _containers.RepeatedCompositeFieldContainer[VersionedQueryName]
    agent_id: _containers.RepeatedScalarFieldContainer[str]
    branch_name: _containers.RepeatedScalarFieldContainer[str]
    correlation_id: _containers.RepeatedScalarFieldContainer[str]
    trace_id: _containers.RepeatedScalarFieldContainer[str]
    query_plan_id: _containers.RepeatedScalarFieldContainer[str]
    deployment_id: _containers.RepeatedScalarFieldContainer[str]
    query_status: _containers.RepeatedScalarFieldContainer[_query_status_pb2.QueryStatus]
    meta_query_hash: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        operation_id: _Optional[_Iterable[str]] = ...,
        operation_kind: _Optional[_Iterable[_Union[_operation_kind_pb2.OperationKind, str]]] = ...,
        query_name: _Optional[_Iterable[_Union[VersionedQueryName, _Mapping]]] = ...,
        agent_id: _Optional[_Iterable[str]] = ...,
        branch_name: _Optional[_Iterable[str]] = ...,
        correlation_id: _Optional[_Iterable[str]] = ...,
        trace_id: _Optional[_Iterable[str]] = ...,
        query_plan_id: _Optional[_Iterable[str]] = ...,
        deployment_id: _Optional[_Iterable[str]] = ...,
        query_status: _Optional[_Iterable[_Union[_query_status_pb2.QueryStatus, str]]] = ...,
        meta_query_hash: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetQueryLogEntriesPageToken(_message.Message):
    __slots__ = ("operation_id_hwm", "query_timestamp_hwm")
    OPERATION_ID_HWM_FIELD_NUMBER: _ClassVar[int]
    QUERY_TIMESTAMP_HWM_FIELD_NUMBER: _ClassVar[int]
    operation_id_hwm: str
    query_timestamp_hwm: _timestamp_pb2.Timestamp
    def __init__(
        self,
        operation_id_hwm: _Optional[str] = ...,
        query_timestamp_hwm: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetQueryLogEntriesRequest(_message.Message):
    __slots__ = (
        "query_timestamp_lower_bound_inclusive",
        "query_timestamp_upper_bound_exclusive",
        "filters",
        "page_size",
        "page_token",
    )
    QUERY_TIMESTAMP_LOWER_BOUND_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    QUERY_TIMESTAMP_UPPER_BOUND_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    query_timestamp_lower_bound_inclusive: _timestamp_pb2.Timestamp
    query_timestamp_upper_bound_exclusive: _timestamp_pb2.Timestamp
    filters: QueryLogFilters
    page_size: int
    page_token: str
    def __init__(
        self,
        query_timestamp_lower_bound_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        query_timestamp_upper_bound_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        filters: _Optional[_Union[QueryLogFilters, _Mapping]] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class QueryLogEntry(_message.Message):
    __slots__ = (
        "operation_id",
        "environment_id",
        "deployment_id",
        "operation_kind",
        "query_timestamp",
        "execution_started_at",
        "execution_finished_at",
        "query_status",
        "query_name",
        "query_name_version",
        "agent_id",
        "branch_name",
        "correlation_id",
        "trace_id",
        "query_plan_id",
        "value_tables",
        "meta_query_hash",
    )
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_KIND_FIELD_NUMBER: _ClassVar[int]
    QUERY_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    QUERY_STATUS_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_VERSION_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_TABLES_FIELD_NUMBER: _ClassVar[int]
    META_QUERY_HASH_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    environment_id: str
    deployment_id: str
    operation_kind: _operation_kind_pb2.OperationKind
    query_timestamp: _timestamp_pb2.Timestamp
    execution_started_at: _timestamp_pb2.Timestamp
    execution_finished_at: _timestamp_pb2.Timestamp
    query_status: _query_status_pb2.QueryStatus
    query_name: str
    query_name_version: str
    agent_id: str
    branch_name: str
    correlation_id: str
    trace_id: str
    query_plan_id: str
    value_tables: _containers.RepeatedScalarFieldContainer[str]
    meta_query_hash: str
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        operation_kind: _Optional[_Union[_operation_kind_pb2.OperationKind, str]] = ...,
        query_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        execution_started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        execution_finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        query_status: _Optional[_Union[_query_status_pb2.QueryStatus, str]] = ...,
        query_name: _Optional[str] = ...,
        query_name_version: _Optional[str] = ...,
        agent_id: _Optional[str] = ...,
        branch_name: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        trace_id: _Optional[str] = ...,
        query_plan_id: _Optional[str] = ...,
        value_tables: _Optional[_Iterable[str]] = ...,
        meta_query_hash: _Optional[str] = ...,
    ) -> None: ...

class GetQueryLogEntriesResponse(_message.Message):
    __slots__ = ("entries", "next_page_token")
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[QueryLogEntry]
    next_page_token: str
    def __init__(
        self,
        entries: _Optional[_Iterable[_Union[QueryLogEntry, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...
