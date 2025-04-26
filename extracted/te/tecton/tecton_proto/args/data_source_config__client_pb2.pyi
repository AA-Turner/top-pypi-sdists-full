from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
INITIAL_STREAM_POSITION_LATEST: InitialStreamPosition
INITIAL_STREAM_POSITION_TRIM_HORIZON: InitialStreamPosition
INITIAL_STREAM_POSITION_UNSPECIFIED: InitialStreamPosition

class BatchConfig(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class StreamConfig(_message.Message):
    __slots__ = ["initial_stream_position", "watermark_delay_threshold"]
    INITIAL_STREAM_POSITION_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_DELAY_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    initial_stream_position: InitialStreamPosition
    watermark_delay_threshold: _duration_pb2.Duration
    def __init__(self, initial_stream_position: _Optional[_Union[InitialStreamPosition, str]] = ..., watermark_delay_threshold: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class InitialStreamPosition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
