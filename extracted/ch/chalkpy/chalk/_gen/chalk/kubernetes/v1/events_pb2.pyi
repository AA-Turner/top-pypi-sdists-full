from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChalkKubernetesEventSeries(_message.Message):
    __slots__ = ("count", "last_observed_time")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_OBSERVED_TIME_FIELD_NUMBER: _ClassVar[int]
    count: int
    last_observed_time: int
    def __init__(self, count: _Optional[int] = ..., last_observed_time: _Optional[int] = ...) -> None: ...

class ChalkKubernetesEvent(_message.Message):
    __slots__ = ("type", "reason", "action", "reporting_controller", "event_time", "note", "series")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    REPORTING_CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    EVENT_TIME_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    type: str
    reason: str
    action: str
    reporting_controller: str
    event_time: int
    note: str
    series: ChalkKubernetesEventSeries
    def __init__(
        self,
        type: _Optional[str] = ...,
        reason: _Optional[str] = ...,
        action: _Optional[str] = ...,
        reporting_controller: _Optional[str] = ...,
        event_time: _Optional[int] = ...,
        note: _Optional[str] = ...,
        series: _Optional[_Union[ChalkKubernetesEventSeries, _Mapping]] = ...,
    ) -> None: ...
