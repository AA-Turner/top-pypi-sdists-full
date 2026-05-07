from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.common.v1 import dataset_response_pb2 as _dataset_response_pb2
from chalk._gen.chalk.common.v1 import offline_query_pb2 as _offline_query_pb2
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

class CreateOfflineQueryRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _offline_query_pb2.OfflineQueryRequest
    def __init__(self, request: _Optional[_Union[_offline_query_pb2.OfflineQueryRequest, _Mapping]] = ...) -> None: ...

class CreateOfflineQueryResponse(_message.Message):
    __slots__ = ("is_finished", "version", "urls", "errors", "columns", "dataset_response")
    IS_FINISHED_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    URLS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    DATASET_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    is_finished: bool
    version: int
    urls: _containers.RepeatedScalarFieldContainer[str]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    columns: _offline_query_pb2.ColumnMetadataList
    dataset_response: _dataset_response_pb2.DatasetResponse
    def __init__(
        self,
        is_finished: bool = ...,
        version: _Optional[int] = ...,
        urls: _Optional[_Iterable[str]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        columns: _Optional[_Union[_offline_query_pb2.ColumnMetadataList, _Mapping]] = ...,
        dataset_response: _Optional[_Union[_dataset_response_pb2.DatasetResponse, _Mapping]] = ...,
    ) -> None: ...
