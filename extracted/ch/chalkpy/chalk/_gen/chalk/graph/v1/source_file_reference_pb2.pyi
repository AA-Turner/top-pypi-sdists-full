from chalk._gen.chalk.lsp.v1 import range_pb2 as _range_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SourceFileReference(_message.Message):
    __slots__ = ("range", "code", "file_name")
    RANGE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    range: _range_pb2.Range
    code: str
    file_name: str
    def __init__(
        self,
        range: _Optional[_Union[_range_pb2.Range, _Mapping]] = ...,
        code: _Optional[str] = ...,
        file_name: _Optional[str] = ...,
    ) -> None: ...
