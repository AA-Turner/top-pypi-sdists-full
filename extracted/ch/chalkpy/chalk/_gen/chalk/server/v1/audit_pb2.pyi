from chalk._gen.chalk.auth.v1 import agent_pb2 as _agent_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.rpc import code_pb2 as _code_pb2
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

class AuditLog(_message.Message):
    __slots__ = ("agent", "description", "endpoint", "at", "trace_id", "code", "request", "response", "ip")
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
    agent: _agent_pb2.Agent
    description: str
    endpoint: str
    at: _timestamp_pb2.Timestamp
    trace_id: int
    code: _code_pb2.Code
    request: _containers.MessageMap[str, _struct_pb2.Value]
    response: _containers.MessageMap[str, _struct_pb2.Value]
    ip: str
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
    ) -> None: ...

class GetAuditLogsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAuditLogsResponse(_message.Message):
    __slots__ = ("logs",)
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[AuditLog]
    def __init__(self, logs: _Optional[_Iterable[_Union[AuditLog, _Mapping]]] = ...) -> None: ...
