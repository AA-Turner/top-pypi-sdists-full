from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class JobProgress(_message.Message):
    __slots__ = ("percent", "epoch", "chunk")
    PERCENT_FIELD_NUMBER: _ClassVar[int]
    EPOCH_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    percent: int
    epoch: int
    chunk: int
    def __init__(self, percent: _Optional[int] = ..., epoch: _Optional[int] = ..., chunk: _Optional[int] = ...) -> None: ...
