from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StageLocation(_message.Message):
    __slots__ = ["namespace", "path", "stage_name"]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    STAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    path: str
    stage_name: str
    def __init__(self, namespace: _Optional[str] = ..., stage_name: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...
