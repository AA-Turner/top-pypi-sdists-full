from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceIdentifier(_message.Message):
    __slots__ = ("rid",)
    RID_FIELD_NUMBER: _ClassVar[int]
    rid: str
    def __init__(self, rid: _Optional[str] = ...) -> None: ...

class UploadBlobStreamRequest(_message.Message):
    __slots__ = ("owning_rid", "file_name", "ensure_unique", "content")
    OWNING_RID_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENSURE_UNIQUE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    owning_rid: ResourceIdentifier
    file_name: str
    ensure_unique: bool
    content: bytes
    def __init__(self, owning_rid: _Optional[_Union[ResourceIdentifier, _Mapping]] = ..., file_name: _Optional[str] = ..., ensure_unique: bool = ..., content: _Optional[bytes] = ...) -> None: ...

class UploadBlobStreamResponse(_message.Message):
    __slots__ = ("file_name",)
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    def __init__(self, file_name: _Optional[str] = ...) -> None: ...

class GetSignedUrlForBlobRequest(_message.Message):
    __slots__ = ("owning_rid", "file_name")
    OWNING_RID_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    owning_rid: ResourceIdentifier
    file_name: str
    def __init__(self, owning_rid: _Optional[_Union[ResourceIdentifier, _Mapping]] = ..., file_name: _Optional[str] = ...) -> None: ...

class GetSignedUrlForBlobResponse(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...
