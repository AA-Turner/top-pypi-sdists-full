from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ArchiveStatus(_message.Message):
    __slots__ = ("archived_at", "archived_by")
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_BY_FIELD_NUMBER: _ClassVar[int]
    archived_at: _timestamp_pb2.Timestamp
    archived_by: str
    def __init__(
        self,
        archived_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        archived_by: _Optional[str] = ...,
    ) -> None: ...
