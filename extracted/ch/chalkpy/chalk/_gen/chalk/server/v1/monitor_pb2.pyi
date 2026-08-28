from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MonitorEvaluation(_message.Message):
    __slots__ = ("display_key", "value", "evaluated_at")
    DISPLAY_KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    EVALUATED_AT_FIELD_NUMBER: _ClassVar[int]
    display_key: str
    value: float
    evaluated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        display_key: _Optional[str] = ...,
        value: _Optional[float] = ...,
        evaluated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class MonitorEvent(_message.Message):
    __slots__ = ("event_type", "event_id", "event_data", "occurred_at", "sample_query_id")
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_DATA_FIELD_NUMBER: _ClassVar[int]
    OCCURRED_AT_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    event_type: str
    event_id: str
    event_data: str
    occurred_at: _timestamp_pb2.Timestamp
    sample_query_id: str
    def __init__(
        self,
        event_type: _Optional[str] = ...,
        event_id: _Optional[str] = ...,
        event_data: _Optional[str] = ...,
        occurred_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        sample_query_id: _Optional[str] = ...,
    ) -> None: ...
