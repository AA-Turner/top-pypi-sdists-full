from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Data(_message.Message):
    __slots__ = ("feather_v2", "feather_file_uri")
    FEATHER_V2_FIELD_NUMBER: _ClassVar[int]
    FEATHER_FILE_URI_FIELD_NUMBER: _ClassVar[int]
    feather_v2: bytes
    feather_file_uri: str
    def __init__(self, feather_v2: _Optional[bytes] = ..., feather_file_uri: _Optional[str] = ...) -> None: ...
