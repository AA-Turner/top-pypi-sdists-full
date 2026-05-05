from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Handle(_message.Message):
    __slots__ = ("key", "bucket")
    KEY_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    key: str
    bucket: str
    def __init__(self, key: _Optional[str] = ..., bucket: _Optional[str] = ...) -> None: ...
