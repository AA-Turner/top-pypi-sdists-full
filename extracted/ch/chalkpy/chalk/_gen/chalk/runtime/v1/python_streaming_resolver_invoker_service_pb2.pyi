from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.runtime.v1 import data_pb2 as _data_pb2
from google.protobuf import duration_pb2 as _duration_pb2
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

class StreamMessageRaw(_message.Message):
    __slots__ = (
        "time",
        "value_raw",
        "message_key",
        "string_offset",
        "int_offset",
        "stream_id",
        "partition",
        "num_retries",
        "is_test_message",
    )
    TIME_FIELD_NUMBER: _ClassVar[int]
    VALUE_RAW_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_KEY_FIELD_NUMBER: _ClassVar[int]
    STRING_OFFSET_FIELD_NUMBER: _ClassVar[int]
    INT_OFFSET_FIELD_NUMBER: _ClassVar[int]
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    NUM_RETRIES_FIELD_NUMBER: _ClassVar[int]
    IS_TEST_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    time: _timestamp_pb2.Timestamp
    value_raw: bytes
    message_key: str
    string_offset: str
    int_offset: int
    stream_id: str
    partition: str
    num_retries: int
    is_test_message: bool
    def __init__(
        self,
        time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        value_raw: _Optional[bytes] = ...,
        message_key: _Optional[str] = ...,
        string_offset: _Optional[str] = ...,
        int_offset: _Optional[int] = ...,
        stream_id: _Optional[str] = ...,
        partition: _Optional[str] = ...,
        num_retries: _Optional[int] = ...,
        is_test_message: bool = ...,
    ) -> None: ...

class StreamingResolverResult(_message.Message):
    __slots__ = (
        "timestamp",
        "duration",
        "error",
        "result_table",
        "num_rows",
        "window_secs",
        "skipped",
        "observed_at_fallback",
    )
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULT_TABLE_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_FIELD_NUMBER: _ClassVar[int]
    WINDOW_SECS_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_AT_FALLBACK_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    duration: _duration_pb2.Duration
    error: _chalk_error_pb2.ChalkError
    result_table: _data_pb2.Data
    num_rows: int
    window_secs: int
    skipped: bool
    observed_at_fallback: _timestamp_pb2.Timestamp
    def __init__(
        self,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        error: _Optional[_Union[_chalk_error_pb2.ChalkError, _Mapping]] = ...,
        result_table: _Optional[_Union[_data_pb2.Data, _Mapping]] = ...,
        num_rows: _Optional[int] = ...,
        window_secs: _Optional[int] = ...,
        skipped: bool = ...,
        observed_at_fallback: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class InvokeResolverInBatchOnlyRequest(_message.Message):
    __slots__ = ("resolver_fqn", "messages", "serialized_messages", "operation_id")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    SERIALIZED_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    messages: _containers.RepeatedCompositeFieldContainer[StreamMessageRaw]
    serialized_messages: _containers.RepeatedScalarFieldContainer[bytes]
    operation_id: str
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        messages: _Optional[_Iterable[_Union[StreamMessageRaw, _Mapping]]] = ...,
        serialized_messages: _Optional[_Iterable[bytes]] = ...,
        operation_id: _Optional[str] = ...,
    ) -> None: ...

class InvokeResolverInBatchOnlyResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[StreamingResolverResult]
    def __init__(self, results: _Optional[_Iterable[_Union[StreamingResolverResult, _Mapping]]] = ...) -> None: ...
