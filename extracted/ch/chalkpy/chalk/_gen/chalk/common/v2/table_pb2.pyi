from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Table(_message.Message):
    __slots__ = ("feather", "uri")
    FEATHER_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    feather: bytes
    uri: str
    def __init__(self, feather: _Optional[bytes] = ..., uri: _Optional[str] = ...) -> None: ...
