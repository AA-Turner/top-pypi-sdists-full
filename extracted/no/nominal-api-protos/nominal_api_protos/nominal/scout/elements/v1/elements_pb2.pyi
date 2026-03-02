from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Symbol(_message.Message):
    __slots__ = ("icon", "emoji", "image")
    ICON_FIELD_NUMBER: _ClassVar[int]
    EMOJI_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    icon: str
    emoji: str
    image: str
    def __init__(self, icon: _Optional[str] = ..., emoji: _Optional[str] = ..., image: _Optional[str] = ...) -> None: ...

class Color(_message.Message):
    __slots__ = ("hex_code",)
    HEX_CODE_FIELD_NUMBER: _ClassVar[int]
    hex_code: str
    def __init__(self, hex_code: _Optional[str] = ...) -> None: ...
