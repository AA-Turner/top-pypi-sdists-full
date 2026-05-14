from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetClickhouseUriRequest(_message.Message):
    __slots__ = ("env_id", "cluster_name")
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    cluster_name: str
    def __init__(self, env_id: _Optional[str] = ..., cluster_name: _Optional[str] = ...) -> None: ...

class GetClickhouseUriResponse(_message.Message):
    __slots__ = ("uri", "username", "host", "secret_name")
    URI_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    uri: str
    username: str
    host: str
    secret_name: str
    def __init__(
        self,
        uri: _Optional[str] = ...,
        username: _Optional[str] = ...,
        host: _Optional[str] = ...,
        secret_name: _Optional[str] = ...,
    ) -> None: ...

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
