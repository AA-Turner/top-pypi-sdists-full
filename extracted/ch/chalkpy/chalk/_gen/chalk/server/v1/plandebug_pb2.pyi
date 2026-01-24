from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetQueryPlanStageRequest(_message.Message):
    __slots__ = ("operator_id", "operation_id")
    OPERATOR_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operator_id: str
    operation_id: str
    def __init__(self, operator_id: _Optional[str] = ..., operation_id: _Optional[str] = ...) -> None: ...

class GetQueryPlanStageResponse(_message.Message):
    __slots__ = ("operator_id", "operation_id", "data_preview", "data_summary", "group_preview")
    OPERATOR_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    DATA_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    GROUP_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    operator_id: str
    operation_id: str
    data_preview: _struct_pb2.Struct
    data_summary: _struct_pb2.Struct
    group_preview: _struct_pb2.Struct
    def __init__(
        self,
        operator_id: _Optional[str] = ...,
        operation_id: _Optional[str] = ...,
        data_preview: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        data_summary: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        group_preview: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...

class GetQueryPlanStageResolverInputsRequest(_message.Message):
    __slots__ = ("operator_id", "operation_id")
    OPERATOR_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operator_id: str
    operation_id: str
    def __init__(self, operator_id: _Optional[str] = ..., operation_id: _Optional[str] = ...) -> None: ...

class GetQueryPlanStageResolverInputsResponse(_message.Message):
    __slots__ = ("resolvers", "scalars", "tables")
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    SCALARS_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    resolvers: _struct_pb2.Struct
    scalars: _struct_pb2.Struct
    tables: _struct_pb2.Struct
    def __init__(
        self,
        resolvers: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        scalars: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        tables: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
    ) -> None: ...

class GetQueryPlanStageDownloadLinkRequest(_message.Message):
    __slots__ = ("operator_id", "operation_id")
    OPERATOR_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operator_id: str
    operation_id: str
    def __init__(self, operator_id: _Optional[str] = ..., operation_id: _Optional[str] = ...) -> None: ...

class GetQueryPlanStageDownloadLinkResponse(_message.Message):
    __slots__ = ("signed_url", "group_urls", "error", "expiration")
    SIGNED_URL_FIELD_NUMBER: _ClassVar[int]
    GROUP_URLS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    signed_url: str
    group_urls: _struct_pb2.Struct
    error: str
    expiration: _timestamp_pb2.Timestamp
    def __init__(
        self,
        signed_url: _Optional[str] = ...,
        group_urls: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...,
        error: _Optional[str] = ...,
        expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...
