from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimeUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIME_UNIT_UNSPECIFIED: _ClassVar[TimeUnit]
    DAYS: _ClassVar[TimeUnit]
    HOURS: _ClassVar[TimeUnit]
    MINUTES: _ClassVar[TimeUnit]
    SECONDS: _ClassVar[TimeUnit]
    MILLISECONDS: _ClassVar[TimeUnit]
    MICROSECONDS: _ClassVar[TimeUnit]
    NANOSECONDS: _ClassVar[TimeUnit]
    PICOSECONDS: _ClassVar[TimeUnit]
TIME_UNIT_UNSPECIFIED: TimeUnit
DAYS: TimeUnit
HOURS: TimeUnit
MINUTES: TimeUnit
SECONDS: TimeUnit
MILLISECONDS: TimeUnit
MICROSECONDS: TimeUnit
NANOSECONDS: TimeUnit
PICOSECONDS: TimeUnit

class Range(_message.Message):
    __slots__ = ("start", "end")
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: Timestamp
    end: Timestamp
    def __init__(self, start: _Optional[_Union[Timestamp, _Mapping]] = ..., end: _Optional[_Union[Timestamp, _Mapping]] = ...) -> None: ...

class Timestamp(_message.Message):
    __slots__ = ("seconds", "nanos", "picos")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    PICOS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanos: int
    picos: int
    def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ..., picos: _Optional[int] = ...) -> None: ...
