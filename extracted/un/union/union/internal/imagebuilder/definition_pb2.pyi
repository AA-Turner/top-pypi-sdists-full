from union.internal.validate.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageIdentifier(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Image(_message.Message):
    __slots__ = ["id", "fqin"]
    ID_FIELD_NUMBER: _ClassVar[int]
    FQIN_FIELD_NUMBER: _ClassVar[int]
    id: ImageIdentifier
    fqin: str
    def __init__(self, id: _Optional[_Union[ImageIdentifier, _Mapping]] = ..., fqin: _Optional[str] = ...) -> None: ...
