from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StreamingUnaryInvokeRequest(_message.Message):
    __slots__ = ("function_name", "input_table")
    FUNCTION_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_TABLE_FIELD_NUMBER: _ClassVar[int]
    function_name: str
    input_table: bytes
    def __init__(self, function_name: _Optional[str] = ..., input_table: _Optional[bytes] = ...) -> None: ...

class StreamingUnaryInvokeResponse(_message.Message):
    __slots__ = ("output_table", "timestamp", "error")
    OUTPUT_TABLE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    output_table: bytes
    timestamp: _timestamp_pb2.Timestamp
    error: _chalk_error_pb2.ChalkError
    def __init__(
        self,
        output_table: _Optional[bytes] = ...,
        timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        error: _Optional[_Union[_chalk_error_pb2.ChalkError, _Mapping]] = ...,
    ) -> None: ...
