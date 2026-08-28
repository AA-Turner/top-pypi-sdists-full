from chalk._gen.chalk.auth.v1 import agent_pb2 as _agent_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.rpc import code_pb2 as _code_pb2
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

class AuditLogOutcome(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AUDIT_LOG_OUTCOME_UNSPECIFIED: _ClassVar[AuditLogOutcome]
    AUDIT_LOG_OUTCOME_OK: _ClassVar[AuditLogOutcome]
    AUDIT_LOG_OUTCOME_ERROR: _ClassVar[AuditLogOutcome]

AUDIT_LOG_OUTCOME_UNSPECIFIED: AuditLogOutcome
AUDIT_LOG_OUTCOME_OK: AuditLogOutcome
AUDIT_LOG_OUTCOME_ERROR: AuditLogOutcome

class AuditLog(_message.Message):
    __slots__ = ("agent", "description", "endpoint", "at", "trace_id", "code", "request", "response", "ip", "error")
    class RequestEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    class ResponseEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    AGENT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    AT_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    agent: _agent_pb2.Agent
    description: str
    endpoint: str
    at: _timestamp_pb2.Timestamp
    trace_id: int
    code: _code_pb2.Code
    request: _containers.MessageMap[str, _struct_pb2.Value]
    response: _containers.MessageMap[str, _struct_pb2.Value]
    ip: str
    error: str
    def __init__(
        self,
        agent: _Optional[_Union[_agent_pb2.Agent, _Mapping]] = ...,
        description: _Optional[str] = ...,
        endpoint: _Optional[str] = ...,
        at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        trace_id: _Optional[int] = ...,
        code: _Optional[_Union[_code_pb2.Code, str]] = ...,
        request: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        response: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        ip: _Optional[str] = ...,
        error: _Optional[str] = ...,
    ) -> None: ...

class GetAuditLogsRequest(_message.Message):
    __slots__ = (
        "start_time",
        "end_time",
        "endpoint_filter",
        "limit",
        "cursor",
        "timestamp_lower_bound_inclusive",
        "timestamp_upper_bound_exclusive",
        "agent_id_filter",
        "outcome_filters",
    )
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FILTER_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_LOWER_BOUND_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_UPPER_BOUND_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    OUTCOME_FILTERS_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    endpoint_filter: _containers.RepeatedScalarFieldContainer[str]
    limit: int
    cursor: str
    timestamp_lower_bound_inclusive: _timestamp_pb2.Timestamp
    timestamp_upper_bound_exclusive: _timestamp_pb2.Timestamp
    agent_id_filter: str
    outcome_filters: _containers.RepeatedScalarFieldContainer[AuditLogOutcome]
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        endpoint_filter: _Optional[_Iterable[str]] = ...,
        limit: _Optional[int] = ...,
        cursor: _Optional[str] = ...,
        timestamp_lower_bound_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        timestamp_upper_bound_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        agent_id_filter: _Optional[str] = ...,
        outcome_filters: _Optional[_Iterable[_Union[AuditLogOutcome, str]]] = ...,
    ) -> None: ...

class GetAuditLogsResponse(_message.Message):
    __slots__ = ("logs", "next_cursor")
    LOGS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[AuditLog]
    next_cursor: str
    def __init__(
        self, logs: _Optional[_Iterable[_Union[AuditLog, _Mapping]]] = ..., next_cursor: _Optional[str] = ...
    ) -> None: ...

class AuditedEndpointField(_message.Message):
    __slots__ = ("name", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class AuditedEndpoint(_message.Message):
    __slots__ = (
        "endpoint",
        "description",
        "level",
        "request_type",
        "response_type",
        "request_fields",
        "response_fields",
    )
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELDS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELDS_FIELD_NUMBER: _ClassVar[int]
    endpoint: str
    description: str
    level: _audit_pb2.AuditLevel
    request_type: str
    response_type: str
    request_fields: _containers.RepeatedCompositeFieldContainer[AuditedEndpointField]
    response_fields: _containers.RepeatedCompositeFieldContainer[AuditedEndpointField]
    def __init__(
        self,
        endpoint: _Optional[str] = ...,
        description: _Optional[str] = ...,
        level: _Optional[_Union[_audit_pb2.AuditLevel, str]] = ...,
        request_type: _Optional[str] = ...,
        response_type: _Optional[str] = ...,
        request_fields: _Optional[_Iterable[_Union[AuditedEndpointField, _Mapping]]] = ...,
        response_fields: _Optional[_Iterable[_Union[AuditedEndpointField, _Mapping]]] = ...,
    ) -> None: ...

class GetAuditedEndpointsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAuditedEndpointsResponse(_message.Message):
    __slots__ = ("endpoints",)
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    endpoints: _containers.RepeatedCompositeFieldContainer[AuditedEndpoint]
    def __init__(self, endpoints: _Optional[_Iterable[_Union[AuditedEndpoint, _Mapping]]] = ...) -> None: ...
