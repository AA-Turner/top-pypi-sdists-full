from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DirectoryOptions(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECTORY_OPTIONS_UNSPECIFIED: _ClassVar[DirectoryOptions]
    DIRECTORY_OPTIONS_MAIN: _ClassVar[DirectoryOptions]
    DIRECTORY_OPTIONS_SHADOW: _ClassVar[DirectoryOptions]
    DIRECTORY_OPTIONS_DRY_RUN: _ClassVar[DirectoryOptions]
    DIRECTORY_OPTIONS_INDEXING_JOB: _ClassVar[DirectoryOptions]

DIRECTORY_OPTIONS_UNSPECIFIED: DirectoryOptions
DIRECTORY_OPTIONS_MAIN: DirectoryOptions
DIRECTORY_OPTIONS_SHADOW: DirectoryOptions
DIRECTORY_OPTIONS_DRY_RUN: DirectoryOptions
DIRECTORY_OPTIONS_INDEXING_JOB: DirectoryOptions

class GetIndexingJobStatusRequest(_message.Message):
    __slots__ = ("deployment_id", "directory_prefix_enum")
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_PREFIX_ENUM_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    directory_prefix_enum: DirectoryOptions
    def __init__(
        self, deployment_id: _Optional[str] = ..., directory_prefix_enum: _Optional[_Union[DirectoryOptions, str]] = ...
    ) -> None: ...

class GetIndexingJobStatusResponse(_message.Message):
    __slots__ = ("export",)
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    export: _export_pb2.Export
    def __init__(self, export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ...) -> None: ...
