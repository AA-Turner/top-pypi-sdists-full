from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetShaResponse(_message.Message):
    __slots__ = ("sha",)
    SHA_FIELD_NUMBER: _ClassVar[int]
    sha: str
    def __init__(self, sha: _Optional[str] = ...) -> None: ...

class GetShaRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
