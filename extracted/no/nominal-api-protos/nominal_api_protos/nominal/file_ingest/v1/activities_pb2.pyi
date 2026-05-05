from nominal_api_protos.nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetDatasetFileIngestStatusRequest(_message.Message):
    __slots__ = ("dataset_file_id", "dataset_rid", "parsing", "ingesting", "error")
    DATASET_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_RID_FIELD_NUMBER: _ClassVar[int]
    PARSING_FIELD_NUMBER: _ClassVar[int]
    INGESTING_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    dataset_file_id: str
    dataset_rid: str
    parsing: Parsing
    ingesting: Ingesting
    error: Error
    def __init__(self, dataset_file_id: _Optional[str] = ..., dataset_rid: _Optional[str] = ..., parsing: _Optional[_Union[Parsing, _Mapping]] = ..., ingesting: _Optional[_Union[Ingesting, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class SetDatasetFileIngestStatusResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Parsing(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Ingesting(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Error(_message.Message):
    __slots__ = ("error_type", "message")
    ERROR_TYPE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    error_type: str
    message: str
    def __init__(self, error_type: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
