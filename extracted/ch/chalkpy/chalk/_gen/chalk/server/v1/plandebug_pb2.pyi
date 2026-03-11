from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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
    data_preview: _struct_pb2.Value
    data_summary: _struct_pb2.Value
    group_preview: _struct_pb2.Struct
    def __init__(
        self,
        operator_id: _Optional[str] = ...,
        operation_id: _Optional[str] = ...,
        data_preview: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        data_summary: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
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
    resolvers: _containers.RepeatedScalarFieldContainer[str]
    scalars: _struct_pb2.Struct
    tables: _struct_pb2.Struct
    def __init__(
        self,
        resolvers: _Optional[_Iterable[str]] = ...,
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

class GetQueryPlanStageResolverInputScalarLinksRequest(_message.Message):
    __slots__ = ("operation_id", "operator_id", "resolver_fqn")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    operator_id: str
    resolver_fqn: str
    def __init__(
        self, operation_id: _Optional[str] = ..., operator_id: _Optional[str] = ..., resolver_fqn: _Optional[str] = ...
    ) -> None: ...

class GetQueryPlanStageResolverInputScalarLinksResponse(_message.Message):
    __slots__ = ("urls", "error", "expiration")
    URLS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    urls: _containers.RepeatedScalarFieldContainer[str]
    error: str
    expiration: _timestamp_pb2.Timestamp
    def __init__(
        self,
        urls: _Optional[_Iterable[str]] = ...,
        error: _Optional[str] = ...,
        expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetQueryPlanStageResolverInputDataframeLinksRequest(_message.Message):
    __slots__ = ("operation_id", "operator_id", "resolver_fqn", "argument_name")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    ARGUMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    operator_id: str
    resolver_fqn: str
    argument_name: str
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        operator_id: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
        argument_name: _Optional[str] = ...,
    ) -> None: ...

class GetQueryPlanStageResolverInputDataframeLinksResponse(_message.Message):
    __slots__ = ("urls", "error", "expiration")
    URLS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    urls: _containers.RepeatedScalarFieldContainer[str]
    error: str
    expiration: _timestamp_pb2.Timestamp
    def __init__(
        self,
        urls: _Optional[_Iterable[str]] = ...,
        error: _Optional[str] = ...,
        expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...
