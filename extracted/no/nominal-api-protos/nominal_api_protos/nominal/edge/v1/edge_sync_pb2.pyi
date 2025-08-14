from google.api import annotations_pb2 as _annotations_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EdgeSyncServiceError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EDGE_SYNC_SERVICE_ERROR_SYNC_NOT_FOUND: _ClassVar[EdgeSyncServiceError]
    EDGE_SYNC_SERVICE_ERROR_SYNC_ALREADY_EXISTS: _ClassVar[EdgeSyncServiceError]
EDGE_SYNC_SERVICE_ERROR_SYNC_NOT_FOUND: EdgeSyncServiceError
EDGE_SYNC_SERVICE_ERROR_SYNC_ALREADY_EXISTS: EdgeSyncServiceError

class CreateDatasetSyncRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreateSyncRequest(_message.Message):
    __slots__ = ("source_rid", "target_rid", "secret_rid", "dataset")
    SOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    TARGET_RID_FIELD_NUMBER: _ClassVar[int]
    SECRET_RID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    source_rid: str
    target_rid: str
    secret_rid: str
    dataset: CreateDatasetSyncRequest
    def __init__(self, source_rid: _Optional[str] = ..., target_rid: _Optional[str] = ..., secret_rid: _Optional[str] = ..., dataset: _Optional[_Union[CreateDatasetSyncRequest, _Mapping]] = ...) -> None: ...

class CreateSyncResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSyncRequest(_message.Message):
    __slots__ = ("source_rid",)
    SOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    source_rid: str
    def __init__(self, source_rid: _Optional[str] = ...) -> None: ...

class DatasetSync(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Sync(_message.Message):
    __slots__ = ("source_rid", "target_rid", "secret_rid", "dataset")
    SOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    TARGET_RID_FIELD_NUMBER: _ClassVar[int]
    SECRET_RID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    source_rid: str
    target_rid: str
    secret_rid: str
    dataset: DatasetSync
    def __init__(self, source_rid: _Optional[str] = ..., target_rid: _Optional[str] = ..., secret_rid: _Optional[str] = ..., dataset: _Optional[_Union[DatasetSync, _Mapping]] = ...) -> None: ...

class GetSyncResponse(_message.Message):
    __slots__ = ("sync",)
    SYNC_FIELD_NUMBER: _ClassVar[int]
    sync: Sync
    def __init__(self, sync: _Optional[_Union[Sync, _Mapping]] = ...) -> None: ...

class DeleteSyncRequest(_message.Message):
    __slots__ = ("source_rid",)
    SOURCE_RID_FIELD_NUMBER: _ClassVar[int]
    source_rid: str
    def __init__(self, source_rid: _Optional[str] = ...) -> None: ...

class DeleteSyncResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
