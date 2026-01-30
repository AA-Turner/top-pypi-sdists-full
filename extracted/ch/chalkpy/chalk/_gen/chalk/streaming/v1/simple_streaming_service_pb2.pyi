from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
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

class ExecutionPhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EXECUTION_PHASE_UNSPECIFIED: _ClassVar[ExecutionPhase]
    EXECUTION_PHASE_PARSE: _ClassVar[ExecutionPhase]
    EXECUTION_PHASE_MAPPING: _ClassVar[ExecutionPhase]
    EXECUTION_PHASE_PERSISTENCE: _ClassVar[ExecutionPhase]
    EXECUTION_PHASE_AGGREGATION: _ClassVar[ExecutionPhase]
    EXECUTION_PHASE_SINK: _ClassVar[ExecutionPhase]

class StreamingMessageStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    STREAMING_MESSAGE_STATUS_UNSPECIFIED: _ClassVar[StreamingMessageStatus]
    STREAMING_MESSAGE_STATUS_PARSE_FAILED: _ClassVar[StreamingMessageStatus]
    STREAMING_MESSAGE_STATUS_PARSE_SKIPPED: _ClassVar[StreamingMessageStatus]
    STREAMING_MESSAGE_STATUS_FAILED: _ClassVar[StreamingMessageStatus]
    STREAMING_MESSAGE_STATUS_SUCCESS: _ClassVar[StreamingMessageStatus]

class TestStreamResolverStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEST_STREAM_RESOLVER_STATUS_UNSPECIFIED: _ClassVar[TestStreamResolverStatus]
    TEST_STREAM_RESOLVER_STATUS_SUCCESS: _ClassVar[TestStreamResolverStatus]
    TEST_STREAM_RESOLVER_STATUS_FAILURE: _ClassVar[TestStreamResolverStatus]

EXECUTION_PHASE_UNSPECIFIED: ExecutionPhase
EXECUTION_PHASE_PARSE: ExecutionPhase
EXECUTION_PHASE_MAPPING: ExecutionPhase
EXECUTION_PHASE_PERSISTENCE: ExecutionPhase
EXECUTION_PHASE_AGGREGATION: ExecutionPhase
EXECUTION_PHASE_SINK: ExecutionPhase
STREAMING_MESSAGE_STATUS_UNSPECIFIED: StreamingMessageStatus
STREAMING_MESSAGE_STATUS_PARSE_FAILED: StreamingMessageStatus
STREAMING_MESSAGE_STATUS_PARSE_SKIPPED: StreamingMessageStatus
STREAMING_MESSAGE_STATUS_FAILED: StreamingMessageStatus
STREAMING_MESSAGE_STATUS_SUCCESS: StreamingMessageStatus
TEST_STREAM_RESOLVER_STATUS_UNSPECIFIED: TestStreamResolverStatus
TEST_STREAM_RESOLVER_STATUS_SUCCESS: TestStreamResolverStatus
TEST_STREAM_RESOLVER_STATUS_FAILURE: TestStreamResolverStatus

class StreamingError(_message.Message):
    __slots__ = ("error", "phase", "operation_id")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    PHASE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    error: _chalk_error_pb2.ChalkError
    phase: ExecutionPhase
    operation_id: str
    def __init__(
        self,
        error: _Optional[_Union[_chalk_error_pb2.ChalkError, _Mapping]] = ...,
        phase: _Optional[_Union[ExecutionPhase, str]] = ...,
        operation_id: _Optional[str] = ...,
    ) -> None: ...

class SimpleStreamingUnaryInvokeRequest(_message.Message):
    __slots__ = ("streaming_resolver_fqn", "input_data", "operation_id", "debug")
    STREAMING_RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    INPUT_DATA_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    DEBUG_FIELD_NUMBER: _ClassVar[int]
    streaming_resolver_fqn: str
    input_data: bytes
    operation_id: str
    debug: bool
    def __init__(
        self,
        streaming_resolver_fqn: _Optional[str] = ...,
        input_data: _Optional[bytes] = ...,
        operation_id: _Optional[str] = ...,
        debug: bool = ...,
    ) -> None: ...

class SimpleStreamingUnaryInvokeResponse(_message.Message):
    __slots__ = ("num_rows_succeed", "num_rows_failed", "num_rows_skipped", "error", "output_data", "execution_errors")
    NUM_ROWS_SUCCEED_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_FAILED_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_SKIPPED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_DATA_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_ERRORS_FIELD_NUMBER: _ClassVar[int]
    num_rows_succeed: int
    num_rows_failed: int
    num_rows_skipped: int
    error: _chalk_error_pb2.ChalkError
    output_data: bytes
    execution_errors: _containers.RepeatedCompositeFieldContainer[StreamingError]
    def __init__(
        self,
        num_rows_succeed: _Optional[int] = ...,
        num_rows_failed: _Optional[int] = ...,
        num_rows_skipped: _Optional[int] = ...,
        error: _Optional[_Union[_chalk_error_pb2.ChalkError, _Mapping]] = ...,
        output_data: _Optional[bytes] = ...,
        execution_errors: _Optional[_Iterable[_Union[StreamingError, _Mapping]]] = ...,
    ) -> None: ...

class TestStreamingResolverRequest(_message.Message):
    __slots__ = ("resolver_fqn", "static_stream_resolver_b64", "input_data", "operation_id", "debug")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    STATIC_STREAM_RESOLVER_B64_FIELD_NUMBER: _ClassVar[int]
    INPUT_DATA_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    DEBUG_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    static_stream_resolver_b64: str
    input_data: bytes
    operation_id: str
    debug: bool
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        static_stream_resolver_b64: _Optional[str] = ...,
        input_data: _Optional[bytes] = ...,
        operation_id: _Optional[str] = ...,
        debug: bool = ...,
    ) -> None: ...

class TestStreamingResolverResponse(_message.Message):
    __slots__ = ("status", "data_uri", "errors", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_URI_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: TestStreamResolverStatus
    data_uri: str
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    message: str
    def __init__(
        self,
        status: _Optional[_Union[TestStreamResolverStatus, str]] = ...,
        data_uri: _Optional[str] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...
