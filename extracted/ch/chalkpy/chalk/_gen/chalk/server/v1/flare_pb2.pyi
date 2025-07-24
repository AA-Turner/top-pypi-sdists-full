from chalk._gen.chalk.auth.v1 import displayagent_pb2 as _displayagent_pb2
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

class Flare(_message.Message):
    __slots__ = ("id", "agent", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    AGENT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    agent: _displayagent_pb2.DisplayAgent
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        agent: _Optional[_Union[_displayagent_pb2.DisplayAgent, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListFlaresRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListFlaresResponse(_message.Message):
    __slots__ = ("flares",)
    FLARES_FIELD_NUMBER: _ClassVar[int]
    flares: _containers.RepeatedCompositeFieldContainer[Flare]
    def __init__(self, flares: _Optional[_Iterable[_Union[Flare, _Mapping]]] = ...) -> None: ...

class GetFlareDownloadLinkRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetFlareDownloadLinkResponse(_message.Message):
    __slots__ = ("signed_uri",)
    SIGNED_URI_FIELD_NUMBER: _ClassVar[int]
    signed_uri: str
    def __init__(self, signed_uri: _Optional[str] = ...) -> None: ...

class UploadFlareRequest(_message.Message):
    __slots__ = ("archive",)
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    archive: bytes
    def __init__(self, archive: _Optional[bytes] = ...) -> None: ...

class UploadFlareResponse(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...
