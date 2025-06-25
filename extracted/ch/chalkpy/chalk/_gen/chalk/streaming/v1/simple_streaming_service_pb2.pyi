from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SimpleStreamingUnaryInvokeRequest(_message.Message):
    __slots__ = ("streaming_resolver_fqn", "input_data", "operation_id")
    STREAMING_RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    INPUT_DATA_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    streaming_resolver_fqn: str
    input_data: bytes
    operation_id: str
    def __init__(
        self,
        streaming_resolver_fqn: _Optional[str] = ...,
        input_data: _Optional[bytes] = ...,
        operation_id: _Optional[str] = ...,
    ) -> None: ...

class SimpleStreamingUnaryInvokeResponse(_message.Message):
    __slots__ = ("num_rows_succeed", "num_rows_failed", "num_rows_skipped", "error")
    NUM_ROWS_SUCCEED_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_FAILED_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_SKIPPED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    num_rows_succeed: int
    num_rows_failed: int
    num_rows_skipped: int
    error: _chalk_error_pb2.ChalkError
    def __init__(
        self,
        num_rows_succeed: _Optional[int] = ...,
        num_rows_failed: _Optional[int] = ...,
        num_rows_skipped: _Optional[int] = ...,
        error: _Optional[_Union[_chalk_error_pb2.ChalkError, _Mapping]] = ...,
    ) -> None: ...
