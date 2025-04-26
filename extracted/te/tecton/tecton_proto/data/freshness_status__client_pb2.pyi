from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FreshnessStatus(_message.Message):
    __slots__ = ["created_at", "expected_freshness", "feature_view_id", "feature_view_name", "freshness", "is_stale", "is_stream", "materialization_enabled"]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_FRESHNESS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    FRESHNESS_FIELD_NUMBER: _ClassVar[int]
    IS_STALE_FIELD_NUMBER: _ClassVar[int]
    IS_STREAM_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    expected_freshness: _duration_pb2.Duration
    feature_view_id: _id__client_pb2.Id
    feature_view_name: str
    freshness: _duration_pb2.Duration
    is_stale: bool
    is_stream: bool
    materialization_enabled: bool
    def __init__(self, feature_view_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., feature_view_name: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expected_freshness: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., is_stream: bool = ..., materialization_enabled: bool = ..., freshness: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., is_stale: bool = ...) -> None: ...
