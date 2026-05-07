from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import files_pb2 as _files_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class SqlWorksheet(_message.Message):
    __slots__ = ("file_id", "content", "last_operation_id", "created_at", "updated_at", "file")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    LAST_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    content: str
    last_operation_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    file: _files_pb2.File
    def __init__(
        self,
        file_id: _Optional[str] = ...,
        content: _Optional[str] = ...,
        last_operation_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        file: _Optional[_Union[_files_pb2.File, _Mapping]] = ...,
    ) -> None: ...

class CreateSqlWorksheetRequest(_message.Message):
    __slots__ = ("name", "environment_id", "content")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    environment_id: str
    content: str
    def __init__(
        self, name: _Optional[str] = ..., environment_id: _Optional[str] = ..., content: _Optional[str] = ...
    ) -> None: ...

class CreateSqlWorksheetResponse(_message.Message):
    __slots__ = ("worksheet",)
    WORKSHEET_FIELD_NUMBER: _ClassVar[int]
    worksheet: SqlWorksheet
    def __init__(self, worksheet: _Optional[_Union[SqlWorksheet, _Mapping]] = ...) -> None: ...

class GetSqlWorksheetRequest(_message.Message):
    __slots__ = ("file_id",)
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    def __init__(self, file_id: _Optional[str] = ...) -> None: ...

class GetSqlWorksheetResponse(_message.Message):
    __slots__ = ("worksheet",)
    WORKSHEET_FIELD_NUMBER: _ClassVar[int]
    worksheet: SqlWorksheet
    def __init__(self, worksheet: _Optional[_Union[SqlWorksheet, _Mapping]] = ...) -> None: ...

class UpdateSqlWorksheetRequest(_message.Message):
    __slots__ = ("file_id", "content", "last_operation_id")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    LAST_OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    content: str
    last_operation_id: str
    def __init__(
        self, file_id: _Optional[str] = ..., content: _Optional[str] = ..., last_operation_id: _Optional[str] = ...
    ) -> None: ...

class UpdateSqlWorksheetResponse(_message.Message):
    __slots__ = ("worksheet",)
    WORKSHEET_FIELD_NUMBER: _ClassVar[int]
    worksheet: SqlWorksheet
    def __init__(self, worksheet: _Optional[_Union[SqlWorksheet, _Mapping]] = ...) -> None: ...

class DeleteSqlWorksheetRequest(_message.Message):
    __slots__ = ("file_id",)
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    def __init__(self, file_id: _Optional[str] = ...) -> None: ...

class DeleteSqlWorksheetResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSqlWorksheetsRequest(_message.Message):
    __slots__ = ("environment_id", "cursor", "limit", "search", "include_archived")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    cursor: str
    limit: int
    search: str
    include_archived: bool
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        search: _Optional[str] = ...,
        include_archived: bool = ...,
    ) -> None: ...

class ListSqlWorksheetsResponse(_message.Message):
    __slots__ = ("worksheets", "cursor")
    WORKSHEETS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    worksheets: _containers.RepeatedCompositeFieldContainer[SqlWorksheet]
    cursor: str
    def __init__(
        self, worksheets: _Optional[_Iterable[_Union[SqlWorksheet, _Mapping]]] = ..., cursor: _Optional[str] = ...
    ) -> None: ...

class RenameSqlWorksheetRequest(_message.Message):
    __slots__ = ("file_id", "name")
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    name: str
    def __init__(self, file_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class RenameSqlWorksheetResponse(_message.Message):
    __slots__ = ("worksheet",)
    WORKSHEET_FIELD_NUMBER: _ClassVar[int]
    worksheet: SqlWorksheet
    def __init__(self, worksheet: _Optional[_Union[SqlWorksheet, _Mapping]] = ...) -> None: ...
