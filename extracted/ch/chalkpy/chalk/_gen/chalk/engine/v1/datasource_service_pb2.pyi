from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class DatasourceTestCoverage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASOURCE_TEST_COVERAGE_UNSPECIFIED: _ClassVar[DatasourceTestCoverage]
    DATASOURCE_TEST_COVERAGE_FAST: _ClassVar[DatasourceTestCoverage]
    DATASOURCE_TEST_COVERAGE_FULL: _ClassVar[DatasourceTestCoverage]

class DatasourceTestStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASOURCE_TEST_STATUS_UNSPECIFIED: _ClassVar[DatasourceTestStatus]
    DATASOURCE_TEST_STATUS_PASS: _ClassVar[DatasourceTestStatus]
    DATASOURCE_TEST_STATUS_FAIL: _ClassVar[DatasourceTestStatus]
    DATASOURCE_TEST_STATUS_PASS_WITH_WARNINGS: _ClassVar[DatasourceTestStatus]

class DatasourceTestFindingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASOURCE_TEST_FINDING_STATUS_UNSPECIFIED: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_SKIPPED: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_PASS: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_WARNING_LOW_SEVERITY: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_WARNING_MEDIUM_SEVERITY: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_WARNING_HIGH_SEVERITY: _ClassVar[DatasourceTestFindingStatus]
    DATASOURCE_TEST_FINDING_STATUS_ERROR: _ClassVar[DatasourceTestFindingStatus]

class RunningQueryIntrospectionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RUNNING_QUERY_INTROSPECTION_STATUS_UNSPECIFIED: _ClassVar[RunningQueryIntrospectionStatus]
    RUNNING_QUERY_INTROSPECTION_STATUS_OK: _ClassVar[RunningQueryIntrospectionStatus]
    RUNNING_QUERY_INTROSPECTION_STATUS_UNSUPPORTED: _ClassVar[RunningQueryIntrospectionStatus]
    RUNNING_QUERY_INTROSPECTION_STATUS_FAILED: _ClassVar[RunningQueryIntrospectionStatus]
    RUNNING_QUERY_INTROSPECTION_STATUS_PARTIAL: _ClassVar[RunningQueryIntrospectionStatus]

class RunningDatasourceQueryState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RUNNING_DATASOURCE_QUERY_STATE_UNSPECIFIED: _ClassVar[RunningDatasourceQueryState]
    RUNNING_DATASOURCE_QUERY_STATE_RUNNING: _ClassVar[RunningDatasourceQueryState]
    RUNNING_DATASOURCE_QUERY_STATE_QUEUED: _ClassVar[RunningDatasourceQueryState]
    RUNNING_DATASOURCE_QUERY_STATE_BLOCKED: _ClassVar[RunningDatasourceQueryState]

DATASOURCE_TEST_COVERAGE_UNSPECIFIED: DatasourceTestCoverage
DATASOURCE_TEST_COVERAGE_FAST: DatasourceTestCoverage
DATASOURCE_TEST_COVERAGE_FULL: DatasourceTestCoverage
DATASOURCE_TEST_STATUS_UNSPECIFIED: DatasourceTestStatus
DATASOURCE_TEST_STATUS_PASS: DatasourceTestStatus
DATASOURCE_TEST_STATUS_FAIL: DatasourceTestStatus
DATASOURCE_TEST_STATUS_PASS_WITH_WARNINGS: DatasourceTestStatus
DATASOURCE_TEST_FINDING_STATUS_UNSPECIFIED: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_SKIPPED: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_PASS: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_WARNING_LOW_SEVERITY: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_WARNING_MEDIUM_SEVERITY: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_WARNING_HIGH_SEVERITY: DatasourceTestFindingStatus
DATASOURCE_TEST_FINDING_STATUS_ERROR: DatasourceTestFindingStatus
RUNNING_QUERY_INTROSPECTION_STATUS_UNSPECIFIED: RunningQueryIntrospectionStatus
RUNNING_QUERY_INTROSPECTION_STATUS_OK: RunningQueryIntrospectionStatus
RUNNING_QUERY_INTROSPECTION_STATUS_UNSUPPORTED: RunningQueryIntrospectionStatus
RUNNING_QUERY_INTROSPECTION_STATUS_FAILED: RunningQueryIntrospectionStatus
RUNNING_QUERY_INTROSPECTION_STATUS_PARTIAL: RunningQueryIntrospectionStatus
RUNNING_DATASOURCE_QUERY_STATE_UNSPECIFIED: RunningDatasourceQueryState
RUNNING_DATASOURCE_QUERY_STATE_RUNNING: RunningDatasourceQueryState
RUNNING_DATASOURCE_QUERY_STATE_QUEUED: RunningDatasourceQueryState
RUNNING_DATASOURCE_QUERY_STATE_BLOCKED: RunningDatasourceQueryState

class DatasourceTestFinding(_message.Message):
    __slots__ = ("status", "group", "title", "message", "config_keys")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_KEYS_FIELD_NUMBER: _ClassVar[int]
    status: DatasourceTestFindingStatus
    group: str
    title: str
    message: str
    config_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        status: _Optional[_Union[DatasourceTestFindingStatus, str]] = ...,
        group: _Optional[str] = ...,
        title: _Optional[str] = ...,
        message: _Optional[str] = ...,
        config_keys: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class PreviewedStreamMessage(_message.Message):
    __slots__ = ("value_base64", "key_base64", "topic", "partition", "offset", "timestamp_ms")
    VALUE_BASE64_FIELD_NUMBER: _ClassVar[int]
    KEY_BASE64_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_MS_FIELD_NUMBER: _ClassVar[int]
    value_base64: str
    key_base64: str
    topic: str
    partition: str
    offset: str
    timestamp_ms: int
    def __init__(
        self,
        value_base64: _Optional[str] = ...,
        key_base64: _Optional[str] = ...,
        topic: _Optional[str] = ...,
        partition: _Optional[str] = ...,
        offset: _Optional[str] = ...,
        timestamp_ms: _Optional[int] = ...,
    ) -> None: ...

class TestDatasourceRequest(_message.Message):
    __slots__ = ("kind", "parameters", "include_preview", "coverage")
    KIND_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_FIELD_NUMBER: _ClassVar[int]
    kind: str
    parameters: _struct_pb2.Struct
    include_preview: bool
    coverage: DatasourceTestCoverage
    def __init__(
        self,
        kind: _Optional[str] = ...,
        parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        include_preview: bool = ...,
        coverage: _Optional[_Union[DatasourceTestCoverage, str]] = ...,
    ) -> None: ...

class TestDatasourceResponse(_message.Message):
    __slots__ = ("status", "findings", "summary", "latency_seconds", "preview_messages", "coverage_ran")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FINDINGS_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    LATENCY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_RAN_FIELD_NUMBER: _ClassVar[int]
    status: DatasourceTestStatus
    findings: _containers.RepeatedCompositeFieldContainer[DatasourceTestFinding]
    summary: str
    latency_seconds: float
    preview_messages: _containers.RepeatedCompositeFieldContainer[PreviewedStreamMessage]
    coverage_ran: DatasourceTestCoverage
    def __init__(
        self,
        status: _Optional[_Union[DatasourceTestStatus, str]] = ...,
        findings: _Optional[_Iterable[_Union[DatasourceTestFinding, _Mapping]]] = ...,
        summary: _Optional[str] = ...,
        latency_seconds: _Optional[float] = ...,
        preview_messages: _Optional[_Iterable[_Union[PreviewedStreamMessage, _Mapping]]] = ...,
        coverage_ran: _Optional[_Union[DatasourceTestCoverage, str]] = ...,
    ) -> None: ...

class RunningDatasourceQuery(_message.Message):
    __slots__ = (
        "query_id",
        "sql_text",
        "sql_truncated",
        "user",
        "role",
        "warehouse_or_project",
        "session_id",
        "state",
        "start_time",
        "elapsed",
        "console_url",
        "query_type",
        "database_name",
        "schema_name",
        "query_tag",
        "queued_time",
        "blocked_time",
    )
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SQL_TEXT_FIELD_NUMBER: _ClassVar[int]
    SQL_TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_OR_PROJECT_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_FIELD_NUMBER: _ClassVar[int]
    CONSOLE_URL_FIELD_NUMBER: _ClassVar[int]
    QUERY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATABASE_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_TAG_FIELD_NUMBER: _ClassVar[int]
    QUEUED_TIME_FIELD_NUMBER: _ClassVar[int]
    BLOCKED_TIME_FIELD_NUMBER: _ClassVar[int]
    query_id: str
    sql_text: str
    sql_truncated: bool
    user: str
    role: str
    warehouse_or_project: str
    session_id: str
    state: RunningDatasourceQueryState
    start_time: _timestamp_pb2.Timestamp
    elapsed: _duration_pb2.Duration
    console_url: str
    query_type: str
    database_name: str
    schema_name: str
    query_tag: str
    queued_time: _duration_pb2.Duration
    blocked_time: _duration_pb2.Duration
    def __init__(
        self,
        query_id: _Optional[str] = ...,
        sql_text: _Optional[str] = ...,
        sql_truncated: bool = ...,
        user: _Optional[str] = ...,
        role: _Optional[str] = ...,
        warehouse_or_project: _Optional[str] = ...,
        session_id: _Optional[str] = ...,
        state: _Optional[_Union[RunningDatasourceQueryState, str]] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        elapsed: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        console_url: _Optional[str] = ...,
        query_type: _Optional[str] = ...,
        database_name: _Optional[str] = ...,
        schema_name: _Optional[str] = ...,
        query_tag: _Optional[str] = ...,
        queued_time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        blocked_time: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class ListRunningDatasourceQueriesFilters(_message.Message):
    __slots__ = ("user", "warehouse", "min_elapsed", "limit")
    USER_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    MIN_ELAPSED_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    user: str
    warehouse: str
    min_elapsed: _duration_pb2.Duration
    limit: int
    def __init__(
        self,
        user: _Optional[str] = ...,
        warehouse: _Optional[str] = ...,
        min_elapsed: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListRunningDatasourceQueriesRequest(_message.Message):
    __slots__ = ("kind", "parameters", "filters")
    KIND_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    kind: str
    parameters: _struct_pb2.Struct
    filters: ListRunningDatasourceQueriesFilters
    def __init__(
        self,
        kind: _Optional[str] = ...,
        parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        filters: _Optional[_Union[ListRunningDatasourceQueriesFilters, _Mapping]] = ...,
    ) -> None: ...

class ListRunningDatasourceQueriesResponse(_message.Message):
    __slots__ = ("status", "queries", "error", "warehouse_or_project", "incomplete_reason")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    QUERIES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_OR_PROJECT_FIELD_NUMBER: _ClassVar[int]
    INCOMPLETE_REASON_FIELD_NUMBER: _ClassVar[int]
    status: RunningQueryIntrospectionStatus
    queries: _containers.RepeatedCompositeFieldContainer[RunningDatasourceQuery]
    error: str
    warehouse_or_project: str
    incomplete_reason: str
    def __init__(
        self,
        status: _Optional[_Union[RunningQueryIntrospectionStatus, str]] = ...,
        queries: _Optional[_Iterable[_Union[RunningDatasourceQuery, _Mapping]]] = ...,
        error: _Optional[str] = ...,
        warehouse_or_project: _Optional[str] = ...,
        incomplete_reason: _Optional[str] = ...,
    ) -> None: ...
