from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

class SqlQuery(_message.Message):
    __slots__ = (
        "id",
        "agent_id",
        "environment_id",
        "deployment_id",
        "created_at",
        "query_text",
        "duration",
        "status",
        "query_metadata",
        "trace_id",
        "branch_name",
        "has_plan_stages",
        "external_id",
        "correlation_id",
        "resource_group",
        "query_plan_json",
        "output_uri_prefix",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    QUERY_TEXT_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    QUERY_METADATA_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    HAS_PLAN_STAGES_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    QUERY_PLAN_JSON_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_URI_PREFIX_FIELD_NUMBER: _ClassVar[int]
    id: str
    agent_id: str
    environment_id: str
    deployment_id: str
    created_at: _timestamp_pb2.Timestamp
    query_text: str
    duration: float
    status: int
    query_metadata: str
    trace_id: str
    branch_name: str
    has_plan_stages: bool
    external_id: str
    correlation_id: str
    resource_group: str
    query_plan_json: str
    output_uri_prefix: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        agent_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        query_text: _Optional[str] = ...,
        duration: _Optional[float] = ...,
        status: _Optional[int] = ...,
        query_metadata: _Optional[str] = ...,
        trace_id: _Optional[str] = ...,
        branch_name: _Optional[str] = ...,
        has_plan_stages: bool = ...,
        external_id: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        query_plan_json: _Optional[str] = ...,
        output_uri_prefix: _Optional[str] = ...,
    ) -> None: ...

class ListSqlQueriesRequest(_message.Message):
    __slots__ = (
        "limit",
        "cursor",
        "agent_id",
        "deployment_id",
        "status",
        "branch_name",
        "external_id",
        "correlation_id",
        "start",
        "end",
    )
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    agent_id: str
    deployment_id: str
    status: int
    branch_name: str
    external_id: str
    correlation_id: str
    start: _timestamp_pb2.Timestamp
    end: _timestamp_pb2.Timestamp
    def __init__(
        self,
        limit: _Optional[int] = ...,
        cursor: _Optional[str] = ...,
        agent_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        status: _Optional[int] = ...,
        branch_name: _Optional[str] = ...,
        external_id: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListSqlQueriesResponse(_message.Message):
    __slots__ = ("queries", "next_cursor")
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    queries: _containers.RepeatedCompositeFieldContainer[SqlQuery]
    next_cursor: str
    def __init__(
        self, queries: _Optional[_Iterable[_Union[SqlQuery, _Mapping]]] = ..., next_cursor: _Optional[str] = ...
    ) -> None: ...

class GetSqlQueryRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetSqlQueryResponse(_message.Message):
    __slots__ = ("query",)
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: SqlQuery
    def __init__(self, query: _Optional[_Union[SqlQuery, _Mapping]] = ...) -> None: ...
