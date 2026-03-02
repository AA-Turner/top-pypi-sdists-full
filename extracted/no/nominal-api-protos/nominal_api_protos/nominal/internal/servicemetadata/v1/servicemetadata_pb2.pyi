from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetServiceMetadataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetServiceMetadataResponse(_message.Message):
    __slots__ = ("version", "min_supported_schema_version_inclusive", "max_supported_schema_version_inclusive", "current_schema_version")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MIN_SUPPORTED_SCHEMA_VERSION_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    MAX_SUPPORTED_SCHEMA_VERSION_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    version: str
    min_supported_schema_version_inclusive: int
    max_supported_schema_version_inclusive: int
    current_schema_version: int
    def __init__(self, version: _Optional[str] = ..., min_supported_schema_version_inclusive: _Optional[int] = ..., max_supported_schema_version_inclusive: _Optional[int] = ..., current_schema_version: _Optional[int] = ...) -> None: ...
