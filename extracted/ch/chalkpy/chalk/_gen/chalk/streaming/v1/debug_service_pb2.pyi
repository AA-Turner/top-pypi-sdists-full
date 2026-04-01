from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.streaming.v1 import simple_streaming_service_pb2 as _simple_streaming_service_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EnableDebugModeRequest(_message.Message):
    __slots__ = ("resolver_fqn", "deployment_id", "logger_config")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LOGGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    deployment_id: str
    logger_config: _simple_streaming_service_pb2.StreamingLoggerConfig
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        logger_config: _Optional[_Union[_simple_streaming_service_pb2.StreamingLoggerConfig, _Mapping]] = ...,
    ) -> None: ...

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
    __slots__ = ("enabled", "enabled_at", "storage_bucket", "deployment_id", "logger_config")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    ENABLED_AT_FIELD_NUMBER: _ClassVar[int]
    STORAGE_BUCKET_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LOGGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    enabled_at: _timestamp_pb2.Timestamp
    storage_bucket: str
    deployment_id: str
    logger_config: _simple_streaming_service_pb2.StreamingLoggerConfig
    def __init__(
        self,
        enabled: bool = ...,
        enabled_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        storage_bucket: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        logger_config: _Optional[_Union[_simple_streaming_service_pb2.StreamingLoggerConfig, _Mapping]] = ...,
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

class WatchDebugStreamRequest(_message.Message):
    __slots__ = ("base_uri", "resolver_fqn", "poll_interval_seconds")
    BASE_URI_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    POLL_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    base_uri: str
    resolver_fqn: str
    poll_interval_seconds: int
    def __init__(
        self,
        base_uri: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
        poll_interval_seconds: _Optional[int] = ...,
    ) -> None: ...

class WatchDebugStreamResponse(_message.Message):
    __slots__ = ("file_path", "content", "size_bytes")
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    content: bytes
    size_bytes: int
    def __init__(
        self, file_path: _Optional[str] = ..., content: _Optional[bytes] = ..., size_bytes: _Optional[int] = ...
    ) -> None: ...

class PushTopicRequest(_message.Message):
    __slots__ = ("topic", "value", "text", "key", "integration", "count")
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    topic: str
    value: bytes
    text: str
    key: str
    integration: str
    count: int
    def __init__(
        self,
        topic: _Optional[str] = ...,
        value: _Optional[bytes] = ...,
        text: _Optional[str] = ...,
        key: _Optional[str] = ...,
        integration: _Optional[str] = ...,
        count: _Optional[int] = ...,
    ) -> None: ...

class PushTopicResponse(_message.Message):
    __slots__ = ("status", "topic", "integration", "error")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    status: str
    topic: str
    integration: str
    error: _chalk_error_pb2.ChalkError
    def __init__(
        self,
        status: _Optional[str] = ...,
        topic: _Optional[str] = ...,
        integration: _Optional[str] = ...,
        error: _Optional[_Union[_chalk_error_pb2.ChalkError, _Mapping]] = ...,
    ) -> None: ...

class SetStreamingDebugConfigRequest(_message.Message):
    __slots__ = ("resolver_fqn", "deployment_id", "logger_config")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LOGGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    deployment_id: str
    logger_config: _simple_streaming_service_pb2.StreamingLoggerConfig
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        logger_config: _Optional[_Union[_simple_streaming_service_pb2.StreamingLoggerConfig, _Mapping]] = ...,
    ) -> None: ...

class SetStreamingDebugConfigResponse(_message.Message):
    __slots__ = ("logger_config",)
    LOGGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    logger_config: _simple_streaming_service_pb2.StreamingLoggerConfig
    def __init__(
        self, logger_config: _Optional[_Union[_simple_streaming_service_pb2.StreamingLoggerConfig, _Mapping]] = ...
    ) -> None: ...

class GetStreamingDebugConfigRequest(_message.Message):
    __slots__ = ("resolver_fqn",)
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    def __init__(self, resolver_fqn: _Optional[str] = ...) -> None: ...

class GetStreamingDebugConfigResponse(_message.Message):
    __slots__ = ("logger_config", "deployment_id", "storage_uri")
    LOGGER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_URI_FIELD_NUMBER: _ClassVar[int]
    logger_config: _simple_streaming_service_pb2.StreamingLoggerConfig
    deployment_id: str
    storage_uri: str
    def __init__(
        self,
        logger_config: _Optional[_Union[_simple_streaming_service_pb2.StreamingLoggerConfig, _Mapping]] = ...,
        deployment_id: _Optional[str] = ...,
        storage_uri: _Optional[str] = ...,
    ) -> None: ...
