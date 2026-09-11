from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class GetMetricsRequest(_message.Message):
    __slots__ = ("read_mask",)
    READ_MASK_FIELD_NUMBER: _ClassVar[int]
    read_mask: _field_mask_pb2.FieldMask
    def __init__(self, read_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class WideTableLayout(_message.Message):
    __slots__ = ("namespace", "partitioned_by", "clustered_by")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    PARTITIONED_BY_FIELD_NUMBER: _ClassVar[int]
    CLUSTERED_BY_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    partitioned_by: str
    clustered_by: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        partitioned_by: _Optional[str] = ...,
        clustered_by: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class NamespaceObservedAtRange(_message.Message):
    __slots__ = ("namespace", "min_observed_at", "max_observed_at")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    MIN_OBSERVED_AT_FIELD_NUMBER: _ClassVar[int]
    MAX_OBSERVED_AT_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    min_observed_at: _timestamp_pb2.Timestamp
    max_observed_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        min_observed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        max_observed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class NamespaceWideTableRowCount(_message.Message):
    __slots__ = ("namespace", "row_count_estimate")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    ROW_COUNT_ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    row_count_estimate: int
    def __init__(self, namespace: _Optional[str] = ..., row_count_estimate: _Optional[int] = ...) -> None: ...

class SnowflakeOfflineStorageDetails(_message.Message):
    __slots__ = ("account", "warehouse", "database", "schema")
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    WAREHOUSE_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    account: str
    warehouse: str
    database: str
    schema: str
    def __init__(
        self,
        account: _Optional[str] = ...,
        warehouse: _Optional[str] = ...,
        database: _Optional[str] = ...,
        schema: _Optional[str] = ...,
    ) -> None: ...

class BigQueryOfflineStorageDetails(_message.Message):
    __slots__ = ("project_id", "dataset_id", "location")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    dataset_id: str
    location: str
    def __init__(
        self, project_id: _Optional[str] = ..., dataset_id: _Optional[str] = ..., location: _Optional[str] = ...
    ) -> None: ...

class GetMetricsResponse(_message.Message):
    __slots__ = (
        "skinny_tables_bytes",
        "wide_tables_bytes",
        "wide_mapping_table_bytes",
        "snowflake",
        "bigquery",
        "namespace_observed_at_ranges",
        "namespace_wide_table_row_counts",
        "wide_table_layouts",
    )
    SKINNY_TABLES_BYTES_FIELD_NUMBER: _ClassVar[int]
    WIDE_TABLES_BYTES_FIELD_NUMBER: _ClassVar[int]
    WIDE_MAPPING_TABLE_BYTES_FIELD_NUMBER: _ClassVar[int]
    SNOWFLAKE_FIELD_NUMBER: _ClassVar[int]
    BIGQUERY_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_OBSERVED_AT_RANGES_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_WIDE_TABLE_ROW_COUNTS_FIELD_NUMBER: _ClassVar[int]
    WIDE_TABLE_LAYOUTS_FIELD_NUMBER: _ClassVar[int]
    skinny_tables_bytes: int
    wide_tables_bytes: int
    wide_mapping_table_bytes: int
    snowflake: SnowflakeOfflineStorageDetails
    bigquery: BigQueryOfflineStorageDetails
    namespace_observed_at_ranges: _containers.RepeatedCompositeFieldContainer[NamespaceObservedAtRange]
    namespace_wide_table_row_counts: _containers.RepeatedCompositeFieldContainer[NamespaceWideTableRowCount]
    wide_table_layouts: _containers.RepeatedCompositeFieldContainer[WideTableLayout]
    def __init__(
        self,
        skinny_tables_bytes: _Optional[int] = ...,
        wide_tables_bytes: _Optional[int] = ...,
        wide_mapping_table_bytes: _Optional[int] = ...,
        snowflake: _Optional[_Union[SnowflakeOfflineStorageDetails, _Mapping]] = ...,
        bigquery: _Optional[_Union[BigQueryOfflineStorageDetails, _Mapping]] = ...,
        namespace_observed_at_ranges: _Optional[_Iterable[_Union[NamespaceObservedAtRange, _Mapping]]] = ...,
        namespace_wide_table_row_counts: _Optional[_Iterable[_Union[NamespaceWideTableRowCount, _Mapping]]] = ...,
        wide_table_layouts: _Optional[_Iterable[_Union[WideTableLayout, _Mapping]]] = ...,
    ) -> None: ...
