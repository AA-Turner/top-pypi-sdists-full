from buf.validate import validate_pb2 as _validate_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BranchOrCommit(_message.Message):
    __slots__ = ("branch", "commit")
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    branch: str
    commit: str
    def __init__(self, branch: _Optional[str] = ..., commit: _Optional[str] = ...) -> None: ...
