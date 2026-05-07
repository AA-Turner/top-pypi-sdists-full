from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.streaming.v1 import simple_streaming_service_pb2 as _simple_streaming_service_pb2
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
    __slots__ = ("resolver_fqn", "start_timestamp_inclusive", "end_timestamp_exclusive", "max_messages")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    MAX_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    start_timestamp_inclusive: _timestamp_pb2.Timestamp
    end_timestamp_exclusive: _timestamp_pb2.Timestamp
    max_messages: int
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        start_timestamp_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_timestamp_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        max_messages: _Optional[int] = ...,
    ) -> None: ...

class GetDebugMessagesResponse(_message.Message):
    __slots__ = ("parquet", "error")
    PARQUET_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    parquet: bytes
    error: str
    def __init__(self, parquet: _Optional[bytes] = ..., error: _Optional[str] = ...) -> None: ...

class GetDebugMessagesV2Request(_message.Message):
    __slots__ = ("resolver_fqn", "start_timestamp_inclusive", "end_timestamp_exclusive", "max_messages")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    MAX_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    start_timestamp_inclusive: _timestamp_pb2.Timestamp
    end_timestamp_exclusive: _timestamp_pb2.Timestamp
    max_messages: int
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        start_timestamp_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_timestamp_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        max_messages: _Optional[int] = ...,
    ) -> None: ...

class GetDebugMessagesV2Response(_message.Message):
    __slots__ = ("messages", "success_count", "failed_count", "skipped_count", "feature_expressions")
    class FeatureExpressionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: StreamingFeatureExpression
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[StreamingFeatureExpression, _Mapping]] = ...
        ) -> None: ...

    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_COUNT_FIELD_NUMBER: _ClassVar[int]
    FAILED_COUNT_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_COUNT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_EXPRESSIONS_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[StreamingDebugMessage]
    success_count: int
    failed_count: int
    skipped_count: int
    feature_expressions: _containers.MessageMap[str, StreamingFeatureExpression]
    def __init__(
        self,
        messages: _Optional[_Iterable[_Union[StreamingDebugMessage, _Mapping]]] = ...,
        success_count: _Optional[int] = ...,
        failed_count: _Optional[int] = ...,
        skipped_count: _Optional[int] = ...,
        feature_expressions: _Optional[_Mapping[str, StreamingFeatureExpression]] = ...,
    ) -> None: ...

class StreamingDebugMessage(_message.Message):
    __slots__ = (
        "message_id",
        "message_data",
        "message_key",
        "message_headers",
        "publish_timestamp",
        "ingest_timestamp",
        "status",
        "features",
        "error",
    )
    class MessageHeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bytes
        def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...

    class FeaturesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _arrow_pb2.ScalarValue
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_arrow_pb2.ScalarValue, _Mapping]] = ...
        ) -> None: ...

    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_HEADERS_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    INGEST_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    message_id: str
    message_data: bytes
    message_key: str
    message_headers: _containers.ScalarMap[str, bytes]
    publish_timestamp: _timestamp_pb2.Timestamp
    ingest_timestamp: _timestamp_pb2.Timestamp
    status: _simple_streaming_service_pb2.StreamingMessageStatus
    features: _containers.MessageMap[str, _arrow_pb2.ScalarValue]
    error: StreamingDebugMessageError
    def __init__(
        self,
        message_id: _Optional[str] = ...,
        message_data: _Optional[bytes] = ...,
        message_key: _Optional[str] = ...,
        message_headers: _Optional[_Mapping[str, bytes]] = ...,
        publish_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        ingest_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        status: _Optional[_Union[_simple_streaming_service_pb2.StreamingMessageStatus, str]] = ...,
        features: _Optional[_Mapping[str, _arrow_pb2.ScalarValue]] = ...,
        error: _Optional[_Union[StreamingDebugMessageError, _Mapping]] = ...,
    ) -> None: ...

class StreamingDebugMessageError(_message.Message):
    __slots__ = ("phase", "message", "code", "exception_kind", "exception_stacktrace", "feature")
    PHASE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_KIND_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_STACKTRACE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    phase: _simple_streaming_service_pb2.ExecutionPhase
    message: str
    code: str
    exception_kind: str
    exception_stacktrace: str
    feature: str
    def __init__(
        self,
        phase: _Optional[_Union[_simple_streaming_service_pb2.ExecutionPhase, str]] = ...,
        message: _Optional[str] = ...,
        code: _Optional[str] = ...,
        exception_kind: _Optional[str] = ...,
        exception_stacktrace: _Optional[str] = ...,
        feature: _Optional[str] = ...,
    ) -> None: ...

class StreamingFeatureExpression(_message.Message):
    __slots__ = ("expression", "json_path")
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    JSON_PATH_FIELD_NUMBER: _ClassVar[int]
    expression: str
    json_path: str
    def __init__(self, expression: _Optional[str] = ..., json_path: _Optional[str] = ...) -> None: ...

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
