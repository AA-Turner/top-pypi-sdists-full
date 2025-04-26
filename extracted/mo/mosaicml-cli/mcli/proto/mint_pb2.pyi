from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MINTMessage(_message.Message):
    __slots__ = ["terminal_size", "user_input"]
    TERMINAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    USER_INPUT_FIELD_NUMBER: _ClassVar[int]
    terminal_size: TerminalSize
    user_input: UserInput
    def __init__(self, user_input: _Optional[_Union[UserInput, _Mapping]] = ..., terminal_size: _Optional[_Union[TerminalSize, _Mapping]] = ...) -> None: ...

class TerminalSize(_message.Message):
    __slots__ = ["height", "width"]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    height: int
    width: int
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class UserInput(_message.Message):
    __slots__ = ["input"]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    input: str
    def __init__(self, input: _Optional[str] = ...) -> None: ...
