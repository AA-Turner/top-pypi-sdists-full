from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetClickhouseUriRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetClickhouseUriResponse(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class OtelTtls(_message.Message):
    __slots__ = ("log_ttl_minutes", "trace_ttl_minutes")
    LOG_TTL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    TRACE_TTL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    log_ttl_minutes: int
    trace_ttl_minutes: int
    def __init__(self, log_ttl_minutes: _Optional[int] = ..., trace_ttl_minutes: _Optional[int] = ...) -> None: ...

class SetClickhouseOtelTtlsRequest(_message.Message):
    __slots__ = ("log_ttl_minutes", "trace_ttl_minutes")
    LOG_TTL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    TRACE_TTL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    log_ttl_minutes: int
    trace_ttl_minutes: int
    def __init__(self, log_ttl_minutes: _Optional[int] = ..., trace_ttl_minutes: _Optional[int] = ...) -> None: ...

class SetClickhouseOtelTtlsResponse(_message.Message):
    __slots__ = ("ttls",)
    TTLS_FIELD_NUMBER: _ClassVar[int]
    ttls: OtelTtls
    def __init__(self, ttls: _Optional[_Union[OtelTtls, _Mapping]] = ...) -> None: ...

class GetClickhouseOtelTtlsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetClickhouseOtelTtlsResponse(_message.Message):
    __slots__ = ("ttls",)
    TTLS_FIELD_NUMBER: _ClassVar[int]
    ttls: OtelTtls
    def __init__(self, ttls: _Optional[_Union[OtelTtls, _Mapping]] = ...) -> None: ...
