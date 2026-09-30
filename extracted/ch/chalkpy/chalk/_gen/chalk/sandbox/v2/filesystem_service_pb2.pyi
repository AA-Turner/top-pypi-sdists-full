from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FilesystemError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FILESYSTEM_ERROR_UNSPECIFIED: _ClassVar[FilesystemError]
    FILESYSTEM_ERROR_INVALID_ARGUMENT: _ClassVar[FilesystemError]
    FILESYSTEM_ERROR_NOT_FOUND: _ClassVar[FilesystemError]
    FILESYSTEM_ERROR_PERMISSION_DENIED: _ClassVar[FilesystemError]
    FILESYSTEM_ERROR_ALREADY_EXISTS: _ClassVar[FilesystemError]
    FILESYSTEM_ERROR_RESOURCE_EXHAUSTED: _ClassVar[FilesystemError]
    FILESYSTEM_ERROR_FAILED_PRECONDITION: _ClassVar[FilesystemError]
    FILESYSTEM_ERROR_INTERNAL: _ClassVar[FilesystemError]
    FILESYSTEM_ERROR_UNVERIFIED: _ClassVar[FilesystemError]

FILESYSTEM_ERROR_UNSPECIFIED: FilesystemError
FILESYSTEM_ERROR_INVALID_ARGUMENT: FilesystemError
FILESYSTEM_ERROR_NOT_FOUND: FilesystemError
FILESYSTEM_ERROR_PERMISSION_DENIED: FilesystemError
FILESYSTEM_ERROR_ALREADY_EXISTS: FilesystemError
FILESYSTEM_ERROR_RESOURCE_EXHAUSTED: FilesystemError
FILESYSTEM_ERROR_FAILED_PRECONDITION: FilesystemError
FILESYSTEM_ERROR_INTERNAL: FilesystemError
FILESYSTEM_ERROR_UNVERIFIED: FilesystemError

class UploadFileMetadata(_message.Message):
    __slots__ = ("sandbox_id", "destination", "mode")
    SANDBOX_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    sandbox_id: str
    destination: str
    mode: int
    def __init__(
        self, sandbox_id: _Optional[str] = ..., destination: _Optional[str] = ..., mode: _Optional[int] = ...
    ) -> None: ...

class UploadFileRequest(_message.Message):
    __slots__ = ("metadata", "data")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    metadata: UploadFileMetadata
    data: bytes
    def __init__(
        self, metadata: _Optional[_Union[UploadFileMetadata, _Mapping]] = ..., data: _Optional[bytes] = ...
    ) -> None: ...

class UploadFileResponse(_message.Message):
    __slots__ = ("bytes_written",)
    BYTES_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    bytes_written: int
    def __init__(self, bytes_written: _Optional[int] = ...) -> None: ...

class DownloadFileRequest(_message.Message):
    __slots__ = ("sandbox_id", "path")
    SANDBOX_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    sandbox_id: str
    path: str
    def __init__(self, sandbox_id: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class DownloadFileResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class FilesystemErrorDetail(_message.Message):
    __slots__ = ("error", "posix_errno")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    POSIX_ERRNO_FIELD_NUMBER: _ClassVar[int]
    error: FilesystemError
    posix_errno: int
    def __init__(
        self, error: _Optional[_Union[FilesystemError, str]] = ..., posix_errno: _Optional[int] = ...
    ) -> None: ...
