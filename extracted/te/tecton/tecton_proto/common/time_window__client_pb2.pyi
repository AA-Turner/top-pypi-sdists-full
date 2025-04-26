from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LifetimeWindow(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RelativeTimeWindow(_message.Message):
    __slots__ = ["window_end", "window_start"]
    WINDOW_END_FIELD_NUMBER: _ClassVar[int]
    WINDOW_START_FIELD_NUMBER: _ClassVar[int]
    window_end: _duration_pb2.Duration
    window_start: _duration_pb2.Duration
    def __init__(self, window_start: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., window_end: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class TimeWindow(_message.Message):
    __slots__ = ["lifetime_window", "relative_time_window", "time_window_series"]
    LIFETIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_SERIES_FIELD_NUMBER: _ClassVar[int]
    lifetime_window: LifetimeWindow
    relative_time_window: RelativeTimeWindow
    time_window_series: TimeWindowSeries
    def __init__(self, relative_time_window: _Optional[_Union[RelativeTimeWindow, _Mapping]] = ..., lifetime_window: _Optional[_Union[LifetimeWindow, _Mapping]] = ..., time_window_series: _Optional[_Union[TimeWindowSeries, _Mapping]] = ...) -> None: ...

class TimeWindowSeries(_message.Message):
    __slots__ = ["time_windows"]
    TIME_WINDOWS_FIELD_NUMBER: _ClassVar[int]
    time_windows: _containers.RepeatedCompositeFieldContainer[RelativeTimeWindow]
    def __init__(self, time_windows: _Optional[_Iterable[_Union[RelativeTimeWindow, _Mapping]]] = ...) -> None: ...
