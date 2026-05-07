from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PauseStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAUSE_STATUS_UNSPECIFIED: _ClassVar[PauseStatus]
    PAUSE_STATUS_PAUSED: _ClassVar[PauseStatus]
    PAUSE_STATUS_RUNNING: _ClassVar[PauseStatus]
    PAUSE_STATUS_UNKNOWN: _ClassVar[PauseStatus]

class PauseStatusAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAUSE_STATUS_ACTION_UNSPECIFIED: _ClassVar[PauseStatusAction]
    PAUSE_STATUS_ACTION_PAUSE: _ClassVar[PauseStatusAction]
    PAUSE_STATUS_ACTION_RESUME: _ClassVar[PauseStatusAction]

PAUSE_STATUS_UNSPECIFIED: PauseStatus
PAUSE_STATUS_PAUSED: PauseStatus
PAUSE_STATUS_RUNNING: PauseStatus
PAUSE_STATUS_UNKNOWN: PauseStatus
PAUSE_STATUS_ACTION_UNSPECIFIED: PauseStatusAction
PAUSE_STATUS_ACTION_PAUSE: PauseStatusAction
PAUSE_STATUS_ACTION_RESUME: PauseStatusAction

class GetPauseStatusRequest(_message.Message):
    __slots__ = ("resolver_fqn",)
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    def __init__(self, resolver_fqn: _Optional[str] = ...) -> None: ...

class GetPauseStatusResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: PauseStatus
    message: str
    def __init__(self, status: _Optional[_Union[PauseStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class SetPauseStatusRequest(_message.Message):
    __slots__ = ("resolver_fqn", "action")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    action: PauseStatusAction
    def __init__(
        self, resolver_fqn: _Optional[str] = ..., action: _Optional[_Union[PauseStatusAction, str]] = ...
    ) -> None: ...

class SetPauseStatusResponse(_message.Message):
    __slots__ = ("status", "message", "topic", "partitions")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    status: PauseStatus
    message: str
    topic: str
    partitions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        status: _Optional[_Union[PauseStatus, str]] = ...,
        message: _Optional[str] = ...,
        topic: _Optional[str] = ...,
        partitions: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class SeekOffsetRequest(_message.Message):
    __slots__ = ("resolver_fqn", "offset", "to_end")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    TO_END_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    offset: int
    to_end: bool
    def __init__(
        self, resolver_fqn: _Optional[str] = ..., offset: _Optional[int] = ..., to_end: bool = ...
    ) -> None: ...

class SeekOffsetResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SeekOffsetTimestampRequest(_message.Message):
    __slots__ = ("resolver_fqn", "offset_ts")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    OFFSET_TS_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    offset_ts: int
    def __init__(self, resolver_fqn: _Optional[str] = ..., offset_ts: _Optional[int] = ...) -> None: ...

class SeekOffsetTimestampResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResetStreamRequest(_message.Message):
    __slots__ = ("resolver_fqn", "source_name")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    source_name: str
    def __init__(self, resolver_fqn: _Optional[str] = ..., source_name: _Optional[str] = ...) -> None: ...

class ResetStreamResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TestStreamResolverDatasourceConnectionRequest(_message.Message):
    __slots__ = ("resolver_fqn",)
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    def __init__(self, resolver_fqn: _Optional[str] = ...) -> None: ...

class TestStreamResolverDatasourceConnectionResponse(_message.Message):
    __slots__ = ("success", "message", "latency_seconds", "resolver_fqn", "is_stream_resolver")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LATENCY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    IS_STREAM_RESOLVER_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    latency_seconds: float
    resolver_fqn: str
    is_stream_resolver: bool
    def __init__(
        self,
        success: bool = ...,
        message: _Optional[str] = ...,
        latency_seconds: _Optional[float] = ...,
        resolver_fqn: _Optional[str] = ...,
        is_stream_resolver: bool = ...,
    ) -> None: ...
