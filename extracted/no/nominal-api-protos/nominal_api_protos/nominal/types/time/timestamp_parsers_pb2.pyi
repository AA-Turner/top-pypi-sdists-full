import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimestampType(_message.Message):
    __slots__ = ("relative", "absolute")
    RELATIVE_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    relative: RelativeTimestamp
    absolute: AbsoluteTimestamp
    def __init__(self, relative: _Optional[_Union[RelativeTimestamp, _Mapping]] = ..., absolute: _Optional[_Union[AbsoluteTimestamp, _Mapping]] = ...) -> None: ...

class RelativeTimestamp(_message.Message):
    __slots__ = ("time_unit", "offset")
    TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    time_unit: str
    offset: _timestamp_pb2.Timestamp
    def __init__(self, time_unit: _Optional[str] = ..., offset: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AbsoluteTimestamp(_message.Message):
    __slots__ = ("iso8601", "epoch_of_time_unit", "custom_format")
    ISO8601_FIELD_NUMBER: _ClassVar[int]
    EPOCH_OF_TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FORMAT_FIELD_NUMBER: _ClassVar[int]
    iso8601: Iso8601Timestamp
    epoch_of_time_unit: EpochTimestamp
    custom_format: CustomTimestamp
    def __init__(self, iso8601: _Optional[_Union[Iso8601Timestamp, _Mapping]] = ..., epoch_of_time_unit: _Optional[_Union[EpochTimestamp, _Mapping]] = ..., custom_format: _Optional[_Union[CustomTimestamp, _Mapping]] = ...) -> None: ...

class Iso8601Timestamp(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class EpochTimestamp(_message.Message):
    __slots__ = ("time_unit",)
    TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    time_unit: str
    def __init__(self, time_unit: _Optional[str] = ...) -> None: ...

class CustomTimestamp(_message.Message):
    __slots__ = ("format", "default_year", "default_day_of_year")
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_YEAR_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_DAY_OF_YEAR_FIELD_NUMBER: _ClassVar[int]
    format: str
    default_year: int
    default_day_of_year: int
    def __init__(self, format: _Optional[str] = ..., default_year: _Optional[int] = ..., default_day_of_year: _Optional[int] = ...) -> None: ...
