from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EnableDebugModeRequest(_message.Message):
    __slots__ = ("resolver_fqn", "deployment_id")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    deployment_id: str
    def __init__(self, resolver_fqn: _Optional[str] = ..., deployment_id: _Optional[str] = ...) -> None: ...

class EnableDebugModeResponse(_message.Message):
    __slots__ = ("enabled", "enabled_at")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ENABLED_AT_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    enabled_at: _timestamp_pb2.Timestamp
    def __init__(
        self, enabled: bool = ..., enabled_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...
    ) -> None: ...

class DisableDebugModeRequest(_message.Message):
    __slots__ = ("resolver_fqn",)
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    def __init__(self, resolver_fqn: _Optional[str] = ...) -> None: ...

class DisableDebugModeResponse(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class GetDebugModeStatusRequest(_message.Message):
    __slots__ = ("resolver_fqn",)
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    def __init__(self, resolver_fqn: _Optional[str] = ...) -> None: ...

class GetDebugModeStatusResponse(_message.Message):
    __slots__ = ("enabled", "enabled_at", "storage_bucket", "deployment_id")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ENABLED_AT_FIELD_NUMBER: _ClassVar[int]
    STORAGE_BUCKET_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    enabled_at: _timestamp_pb2.Timestamp
    storage_bucket: str
    deployment_id: str
    def __init__(
        self,
        enabled: bool = ...,
        enabled_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        storage_bucket: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
    ) -> None: ...

class GetDebugMessagesRequest(_message.Message):
    __slots__ = ("resolver_fqn",)
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    def __init__(self, resolver_fqn: _Optional[str] = ...) -> None: ...

class GetDebugMessagesResponse(_message.Message):
    __slots__ = ("parquet", "error")
    PARQUET_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    parquet: bytes
    error: str
    def __init__(self, parquet: _Optional[bytes] = ..., error: _Optional[str] = ...) -> None: ...
