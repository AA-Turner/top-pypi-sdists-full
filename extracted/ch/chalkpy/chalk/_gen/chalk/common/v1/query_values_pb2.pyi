from chalk._gen.chalk.common.v1 import query_log_pb2 as _query_log_pb2
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

class OperationIdTableIdentifier(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...

class TableNameTableIdentifier(_message.Message):
    __slots__ = ("table_name", "filters")
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    table_name: str
    filters: _query_log_pb2.QueryLogFilters
    def __init__(
        self,
        table_name: _Optional[str] = ...,
        filters: _Optional[_Union[_query_log_pb2.QueryLogFilters, _Mapping]] = ...,
    ) -> None: ...

class GetQueryValuesPageToken(_message.Message):
    __slots__ = ("query_timestamp_hwm", "operation_id_hwm", "row_id_hwm")
    QUERY_TIMESTAMP_HWM_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_HWM_FIELD_NUMBER: _ClassVar[int]
    ROW_ID_HWM_FIELD_NUMBER: _ClassVar[int]
    query_timestamp_hwm: _timestamp_pb2.Timestamp
    operation_id_hwm: str
    row_id_hwm: int
    def __init__(
        self,
        query_timestamp_hwm: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        operation_id_hwm: _Optional[str] = ...,
        row_id_hwm: _Optional[int] = ...,
    ) -> None: ...

class GetQueryValuesRequest(_message.Message):
    __slots__ = (
        "operation_id_identifier",
        "table_name_identifier",
        "query_timestamp_lower_bound_inclusive",
        "query_timestamp_upper_bound_exclusive",
        "features",
        "page_size",
        "page_token",
    )
    OPERATION_ID_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    QUERY_TIMESTAMP_LOWER_BOUND_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    QUERY_TIMESTAMP_UPPER_BOUND_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    operation_id_identifier: OperationIdTableIdentifier
    table_name_identifier: TableNameTableIdentifier
    query_timestamp_lower_bound_inclusive: _timestamp_pb2.Timestamp
    query_timestamp_upper_bound_exclusive: _timestamp_pb2.Timestamp
    features: _containers.RepeatedScalarFieldContainer[str]
    page_size: int
    page_token: str
    def __init__(
        self,
        operation_id_identifier: _Optional[_Union[OperationIdTableIdentifier, _Mapping]] = ...,
        table_name_identifier: _Optional[_Union[TableNameTableIdentifier, _Mapping]] = ...,
        query_timestamp_lower_bound_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        query_timestamp_upper_bound_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        features: _Optional[_Iterable[str]] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class GetQueryValuesResponse(_message.Message):
    __slots__ = ("next_page_token", "parquet")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PARQUET_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    parquet: bytes
    def __init__(self, next_page_token: _Optional[str] = ..., parquet: _Optional[bytes] = ...) -> None: ...
