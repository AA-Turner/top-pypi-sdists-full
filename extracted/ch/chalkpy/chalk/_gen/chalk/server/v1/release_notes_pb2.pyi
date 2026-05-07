from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class Release(_message.Message):
    __slots__ = ("version", "content", "published_at")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_AT_FIELD_NUMBER: _ClassVar[int]
    version: str
    content: str
    published_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        version: _Optional[str] = ...,
        content: _Optional[str] = ...,
        published_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListReleasesRequest(_message.Message):
    __slots__ = ("component",)
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    component: str
    def __init__(self, component: _Optional[str] = ...) -> None: ...

class ListReleasesResponse(_message.Message):
    __slots__ = ("releases",)
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    releases: _containers.RepeatedCompositeFieldContainer[Release]
    def __init__(self, releases: _Optional[_Iterable[_Union[Release, _Mapping]]] = ...) -> None: ...
