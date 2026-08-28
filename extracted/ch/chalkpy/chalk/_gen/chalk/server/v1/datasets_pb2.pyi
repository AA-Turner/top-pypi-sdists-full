from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
from chalk._gen.chalk.common.v1 import column_profile_pb2 as _column_profile_pb2
from chalk._gen.chalk.server.v1 import materialized_aggregate_tiles_pb2 as _materialized_aggregate_tiles_pb2
from chalk._gen.chalk.volume.v1 import volume_pb2 as _volume_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class DatasetRevisionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASET_REVISION_STATUS_UNSPECIFIED: _ClassVar[DatasetRevisionStatus]
    DATASET_REVISION_STATUS_UNKNOWN: _ClassVar[DatasetRevisionStatus]
    DATASET_REVISION_STATUS_WORKING: _ClassVar[DatasetRevisionStatus]
    DATASET_REVISION_STATUS_COMPLETED: _ClassVar[DatasetRevisionStatus]
    DATASET_REVISION_STATUS_FAILED: _ClassVar[DatasetRevisionStatus]
    DATASET_REVISION_STATUS_CANCELED: _ClassVar[DatasetRevisionStatus]
    DATASET_REVISION_STATUS_QUEUED: _ClassVar[DatasetRevisionStatus]

class DatasetVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASET_VERSION_UNSPECIFIED: _ClassVar[DatasetVersion]
    DATASET_VERSION_UNKNOWN: _ClassVar[DatasetVersion]
    DATASET_VERSION_BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES: _ClassVar[DatasetVersion]
    DATASET_VERSION_DATASET_WRITER: _ClassVar[DatasetVersion]
    DATASET_VERSION_BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2: _ClassVar[DatasetVersion]
    DATASET_VERSION_COMPUTE_RESOLVER_OUTPUT_V1: _ClassVar[DatasetVersion]
    DATASET_VERSION_NATIVE_DTYPES: _ClassVar[DatasetVersion]
    DATASET_VERSION_NATIVE_COLUMN_NAMES: _ClassVar[DatasetVersion]

class OfflineQueryGivensVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE_QUERY_GIVENS_VERSION_UNSPECIFIED: _ClassVar[OfflineQueryGivensVersion]
    OFFLINE_QUERY_GIVENS_VERSION_UNKNOWN: _ClassVar[OfflineQueryGivensVersion]
    OFFLINE_QUERY_GIVENS_VERSION_NATIVE_TS_FEATURE_FOR_ROOT_NS: _ClassVar[OfflineQueryGivensVersion]
    OFFLINE_QUERY_GIVENS_VERSION_SINGLE_TS_COL_NAME: _ClassVar[OfflineQueryGivensVersion]
    OFFLINE_QUERY_GIVENS_VERSION_SINGLE_TS_COL_NAME_WITH_URI_PREFIX: _ClassVar[OfflineQueryGivensVersion]

class DatasetSortColumn(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASET_SORT_COLUMN_UNSPECIFIED: _ClassVar[DatasetSortColumn]
    DATASET_SORT_COLUMN_CREATED_AT: _ClassVar[DatasetSortColumn]

class SortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_ORDER_UNSPECIFIED: _ClassVar[SortOrder]
    SORT_ORDER_DESC: _ClassVar[SortOrder]
    SORT_ORDER_ASC: _ClassVar[SortOrder]

class DatasetKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DATASET_KIND_UNSPECIFIED: _ClassVar[DatasetKind]
    DATASET_KIND_NAMED: _ClassVar[DatasetKind]
    DATASET_KIND_ANONYMOUS: _ClassVar[DatasetKind]

class ShardPerformanceSummaryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SHARD_PERFORMANCE_SUMMARY_STATUS_UNSPECIFIED: _ClassVar[ShardPerformanceSummaryStatus]
    SHARD_PERFORMANCE_SUMMARY_STATUS_AVAILABLE: _ClassVar[ShardPerformanceSummaryStatus]
    SHARD_PERFORMANCE_SUMMARY_STATUS_PENDING: _ClassVar[ShardPerformanceSummaryStatus]
    SHARD_PERFORMANCE_SUMMARY_STATUS_NONE: _ClassVar[ShardPerformanceSummaryStatus]

DATASET_REVISION_STATUS_UNSPECIFIED: DatasetRevisionStatus
DATASET_REVISION_STATUS_UNKNOWN: DatasetRevisionStatus
DATASET_REVISION_STATUS_WORKING: DatasetRevisionStatus
DATASET_REVISION_STATUS_COMPLETED: DatasetRevisionStatus
DATASET_REVISION_STATUS_FAILED: DatasetRevisionStatus
DATASET_REVISION_STATUS_CANCELED: DatasetRevisionStatus
DATASET_REVISION_STATUS_QUEUED: DatasetRevisionStatus
DATASET_VERSION_UNSPECIFIED: DatasetVersion
DATASET_VERSION_UNKNOWN: DatasetVersion
DATASET_VERSION_BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES: DatasetVersion
DATASET_VERSION_DATASET_WRITER: DatasetVersion
DATASET_VERSION_BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES_V2: DatasetVersion
DATASET_VERSION_COMPUTE_RESOLVER_OUTPUT_V1: DatasetVersion
DATASET_VERSION_NATIVE_DTYPES: DatasetVersion
DATASET_VERSION_NATIVE_COLUMN_NAMES: DatasetVersion
OFFLINE_QUERY_GIVENS_VERSION_UNSPECIFIED: OfflineQueryGivensVersion
OFFLINE_QUERY_GIVENS_VERSION_UNKNOWN: OfflineQueryGivensVersion
OFFLINE_QUERY_GIVENS_VERSION_NATIVE_TS_FEATURE_FOR_ROOT_NS: OfflineQueryGivensVersion
OFFLINE_QUERY_GIVENS_VERSION_SINGLE_TS_COL_NAME: OfflineQueryGivensVersion
OFFLINE_QUERY_GIVENS_VERSION_SINGLE_TS_COL_NAME_WITH_URI_PREFIX: OfflineQueryGivensVersion
DATASET_SORT_COLUMN_UNSPECIFIED: DatasetSortColumn
DATASET_SORT_COLUMN_CREATED_AT: DatasetSortColumn
SORT_ORDER_UNSPECIFIED: SortOrder
SORT_ORDER_DESC: SortOrder
SORT_ORDER_ASC: SortOrder
DATASET_KIND_UNSPECIFIED: DatasetKind
DATASET_KIND_NAMED: DatasetKind
DATASET_KIND_ANONYMOUS: DatasetKind
SHARD_PERFORMANCE_SUMMARY_STATUS_UNSPECIFIED: ShardPerformanceSummaryStatus
SHARD_PERFORMANCE_SUMMARY_STATUS_AVAILABLE: ShardPerformanceSummaryStatus
SHARD_PERFORMANCE_SUMMARY_STATUS_PENDING: ShardPerformanceSummaryStatus
SHARD_PERFORMANCE_SUMMARY_STATUS_NONE: ShardPerformanceSummaryStatus

class DatasetRevisionMeta(_message.Message):
    __slots__ = (
        "numeric_id",
        "offline_query_id",
        "dataset_id",
        "givens_uri",
        "givens_version",
        "output_uri",
        "output_version",
        "branch_name",
        "num_rows",
        "physical_size_bytes",
        "output_columns",
        "output_fqns",
        "agent_id",
        "completed_at",
        "num_shards",
        "num_computers",
        "metadata",
        "status",
        "num_rows_calculated",
        "physical_size_bytes_calculated",
        "created_at",
        "archived_at",
        "output_arrow_schema_serialized",
    )
    NUMERIC_ID_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    GIVENS_URI_FIELD_NUMBER: _ClassVar[int]
    GIVENS_VERSION_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_URI_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_VERSION_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FQNS_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    NUM_SHARDS_FIELD_NUMBER: _ClassVar[int]
    NUM_COMPUTERS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_CALCULATED_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_SIZE_BYTES_CALCULATED_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ARROW_SCHEMA_SERIALIZED_FIELD_NUMBER: _ClassVar[int]
    numeric_id: int
    offline_query_id: str
    dataset_id: str
    givens_uri: str
    givens_version: OfflineQueryGivensVersion
    output_uri: str
    output_version: DatasetVersion
    branch_name: str
    num_rows: int
    physical_size_bytes: int
    output_columns: _containers.RepeatedScalarFieldContainer[str]
    output_fqns: _containers.RepeatedScalarFieldContainer[str]
    agent_id: str
    completed_at: _timestamp_pb2.Timestamp
    num_shards: int
    num_computers: int
    metadata: _struct_pb2.Value
    status: DatasetRevisionStatus
    num_rows_calculated: int
    physical_size_bytes_calculated: int
    created_at: _timestamp_pb2.Timestamp
    archived_at: _timestamp_pb2.Timestamp
    output_arrow_schema_serialized: bytes
    def __init__(
        self,
        numeric_id: _Optional[int] = ...,
        offline_query_id: _Optional[str] = ...,
        dataset_id: _Optional[str] = ...,
        givens_uri: _Optional[str] = ...,
        givens_version: _Optional[_Union[OfflineQueryGivensVersion, str]] = ...,
        output_uri: _Optional[str] = ...,
        output_version: _Optional[_Union[DatasetVersion, str]] = ...,
        branch_name: _Optional[str] = ...,
        num_rows: _Optional[int] = ...,
        physical_size_bytes: _Optional[int] = ...,
        output_columns: _Optional[_Iterable[str]] = ...,
        output_fqns: _Optional[_Iterable[str]] = ...,
        agent_id: _Optional[str] = ...,
        completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        num_shards: _Optional[int] = ...,
        num_computers: _Optional[int] = ...,
        metadata: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        status: _Optional[_Union[DatasetRevisionStatus, str]] = ...,
        num_rows_calculated: _Optional[int] = ...,
        physical_size_bytes_calculated: _Optional[int] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        archived_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        output_arrow_schema_serialized: _Optional[bytes] = ...,
    ) -> None: ...

class DatasetMeta(_message.Message):
    __slots__ = ("id", "environment_id", "dataset_name", "created_at", "most_recent_revision", "num_revisions")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MOST_RECENT_REVISION_FIELD_NUMBER: _ClassVar[int]
    NUM_REVISIONS_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    dataset_name: str
    created_at: _timestamp_pb2.Timestamp
    most_recent_revision: DatasetRevisionMeta
    num_revisions: int
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        dataset_name: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        most_recent_revision: _Optional[_Union[DatasetRevisionMeta, _Mapping]] = ...,
        num_revisions: _Optional[int] = ...,
    ) -> None: ...

class ListDatasetsRequest(_message.Message):
    __slots__ = (
        "cursor",
        "limit",
        "search",
        "include_anonymous",
        "sort_column",
        "sort_order",
        "status",
        "kind",
        "ids",
        "read_mask",
    )
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ANONYMOUS_FIELD_NUMBER: _ClassVar[int]
    SORT_COLUMN_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    READ_MASK_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    search: str
    include_anonymous: bool
    sort_column: DatasetSortColumn
    sort_order: SortOrder
    status: _containers.RepeatedScalarFieldContainer[DatasetRevisionStatus]
    kind: _containers.RepeatedScalarFieldContainer[DatasetKind]
    ids: _containers.RepeatedScalarFieldContainer[str]
    read_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        search: _Optional[str] = ...,
        include_anonymous: bool = ...,
        sort_column: _Optional[_Union[DatasetSortColumn, str]] = ...,
        sort_order: _Optional[_Union[SortOrder, str]] = ...,
        status: _Optional[_Iterable[_Union[DatasetRevisionStatus, str]]] = ...,
        kind: _Optional[_Iterable[_Union[DatasetKind, str]]] = ...,
        ids: _Optional[_Iterable[str]] = ...,
        read_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class ListDatasetsResponse(_message.Message):
    __slots__ = ("datasets", "cursor")
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    datasets: _containers.RepeatedCompositeFieldContainer[DatasetMeta]
    cursor: str
    def __init__(
        self, datasets: _Optional[_Iterable[_Union[DatasetMeta, _Mapping]]] = ..., cursor: _Optional[str] = ...
    ) -> None: ...

class GetDatasetRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDatasetResponse(_message.Message):
    __slots__ = ("dataset",)
    DATASET_FIELD_NUMBER: _ClassVar[int]
    dataset: DatasetMeta
    def __init__(self, dataset: _Optional[_Union[DatasetMeta, _Mapping]] = ...) -> None: ...

class ListDatasetRevisionsRequest(_message.Message):
    __slots__ = ("dataset_id", "cursor", "limit", "include_archived", "start_time", "end_time")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    cursor: str
    limit: int
    include_archived: bool
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        dataset_id: _Optional[str] = ...,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        include_archived: bool = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListDatasetRevisionsResponse(_message.Message):
    __slots__ = ("revisions", "cursor")
    REVISIONS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    revisions: _containers.RepeatedCompositeFieldContainer[DatasetRevisionMeta]
    cursor: str
    def __init__(
        self, revisions: _Optional[_Iterable[_Union[DatasetRevisionMeta, _Mapping]]] = ..., cursor: _Optional[str] = ...
    ) -> None: ...

class GetDatasetRevisionRequest(_message.Message):
    __slots__ = ("revision_id", "include_archived")
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    revision_id: str
    include_archived: bool
    def __init__(self, revision_id: _Optional[str] = ..., include_archived: bool = ...) -> None: ...

class GetDatasetRevisionResponse(_message.Message):
    __slots__ = ("revision",)
    REVISION_FIELD_NUMBER: _ClassVar[int]
    revision: DatasetRevisionMeta
    def __init__(self, revision: _Optional[_Union[DatasetRevisionMeta, _Mapping]] = ...) -> None: ...

class GetDatasetRevisionDownloadLinksRequest(_message.Message):
    __slots__ = ("revision_id",)
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    revision_id: str
    def __init__(self, revision_id: _Optional[str] = ...) -> None: ...

class ShardPerformanceSummaryLink(_message.Message):
    __slots__ = ("shard_id", "url", "status")
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    shard_id: int
    url: str
    status: ShardPerformanceSummaryStatus
    def __init__(
        self,
        shard_id: _Optional[int] = ...,
        url: _Optional[str] = ...,
        status: _Optional[_Union[ShardPerformanceSummaryStatus, str]] = ...,
    ) -> None: ...

class ShardRequestBodyLink(_message.Message):
    __slots__ = ("shard_id", "url", "exists")
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    shard_id: int
    url: str
    exists: bool
    def __init__(self, shard_id: _Optional[int] = ..., url: _Optional[str] = ..., exists: bool = ...) -> None: ...

class GetDatasetRevisionDownloadLinksResponse(_message.Message):
    __slots__ = (
        "output_urls",
        "givens_urls",
        "performance_summary_urls",
        "request_body_url",
        "trace_urls",
        "error",
        "expiration",
        "performance_summary_links",
        "shard_request_body_links",
    )
    OUTPUT_URLS_FIELD_NUMBER: _ClassVar[int]
    GIVENS_URLS_FIELD_NUMBER: _ClassVar[int]
    PERFORMANCE_SUMMARY_URLS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BODY_URL_FIELD_NUMBER: _ClassVar[int]
    TRACE_URLS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    PERFORMANCE_SUMMARY_LINKS_FIELD_NUMBER: _ClassVar[int]
    SHARD_REQUEST_BODY_LINKS_FIELD_NUMBER: _ClassVar[int]
    output_urls: _containers.RepeatedScalarFieldContainer[str]
    givens_urls: _containers.RepeatedScalarFieldContainer[str]
    performance_summary_urls: _containers.RepeatedScalarFieldContainer[str]
    request_body_url: str
    trace_urls: _containers.RepeatedScalarFieldContainer[str]
    error: str
    expiration: _timestamp_pb2.Timestamp
    performance_summary_links: _containers.RepeatedCompositeFieldContainer[ShardPerformanceSummaryLink]
    shard_request_body_links: _containers.RepeatedCompositeFieldContainer[ShardRequestBodyLink]
    def __init__(
        self,
        output_urls: _Optional[_Iterable[str]] = ...,
        givens_urls: _Optional[_Iterable[str]] = ...,
        performance_summary_urls: _Optional[_Iterable[str]] = ...,
        request_body_url: _Optional[str] = ...,
        trace_urls: _Optional[_Iterable[str]] = ...,
        error: _Optional[str] = ...,
        expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        performance_summary_links: _Optional[_Iterable[_Union[ShardPerformanceSummaryLink, _Mapping]]] = ...,
        shard_request_body_links: _Optional[_Iterable[_Union[ShardRequestBodyLink, _Mapping]]] = ...,
    ) -> None: ...

class GetDatasetRevisionPerformanceLinksRequest(_message.Message):
    __slots__ = ("revision_id",)
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    revision_id: str
    def __init__(self, revision_id: _Optional[str] = ...) -> None: ...

class GetDatasetRevisionPerformanceLinksResponse(_message.Message):
    __slots__ = ("performance_summary_links", "error", "expiration")
    PERFORMANCE_SUMMARY_LINKS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    performance_summary_links: _containers.RepeatedCompositeFieldContainer[ShardPerformanceSummaryLink]
    error: str
    expiration: _timestamp_pb2.Timestamp
    def __init__(
        self,
        performance_summary_links: _Optional[_Iterable[_Union[ShardPerformanceSummaryLink, _Mapping]]] = ...,
        error: _Optional[str] = ...,
        expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class StreamDatasetRevisionDownloadLinksRequest(_message.Message):
    __slots__ = ("revision_id",)
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    revision_id: str
    def __init__(self, revision_id: _Optional[str] = ...) -> None: ...

class StreamDatasetRevisionDownloadLinksResponse(_message.Message):
    __slots__ = (
        "output_urls",
        "givens_urls",
        "performance_summary_urls",
        "request_body_url",
        "trace_urls",
        "error",
        "expiration",
        "performance_summary_links",
    )
    OUTPUT_URLS_FIELD_NUMBER: _ClassVar[int]
    GIVENS_URLS_FIELD_NUMBER: _ClassVar[int]
    PERFORMANCE_SUMMARY_URLS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_BODY_URL_FIELD_NUMBER: _ClassVar[int]
    TRACE_URLS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    PERFORMANCE_SUMMARY_LINKS_FIELD_NUMBER: _ClassVar[int]
    output_urls: _containers.RepeatedScalarFieldContainer[str]
    givens_urls: _containers.RepeatedScalarFieldContainer[str]
    performance_summary_urls: _containers.RepeatedScalarFieldContainer[str]
    request_body_url: str
    trace_urls: _containers.RepeatedScalarFieldContainer[str]
    error: str
    expiration: _timestamp_pb2.Timestamp
    performance_summary_links: _containers.RepeatedCompositeFieldContainer[ShardPerformanceSummaryLink]
    def __init__(
        self,
        output_urls: _Optional[_Iterable[str]] = ...,
        givens_urls: _Optional[_Iterable[str]] = ...,
        performance_summary_urls: _Optional[_Iterable[str]] = ...,
        request_body_url: _Optional[str] = ...,
        trace_urls: _Optional[_Iterable[str]] = ...,
        error: _Optional[str] = ...,
        expiration: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        performance_summary_links: _Optional[_Iterable[_Union[ShardPerformanceSummaryLink, _Mapping]]] = ...,
    ) -> None: ...

class GetDatasetUploadUrisRequest(_message.Message):
    __slots__ = ("content_size", "hash", "part_size", "upload_session_id")
    CONTENT_SIZE_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    PART_SIZE_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    content_size: int
    hash: str
    part_size: int
    upload_session_id: str
    def __init__(
        self,
        content_size: _Optional[int] = ...,
        hash: _Optional[str] = ...,
        part_size: _Optional[int] = ...,
        upload_session_id: _Optional[str] = ...,
    ) -> None: ...

class GetDatasetUploadUrisResponse(_message.Message):
    __slots__ = ("upload_session_id", "storage_object_id", "multipart", "resumable", "azure_block", "direct")
    UPLOAD_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    STORAGE_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    MULTIPART_FIELD_NUMBER: _ClassVar[int]
    RESUMABLE_FIELD_NUMBER: _ClassVar[int]
    AZURE_BLOCK_FIELD_NUMBER: _ClassVar[int]
    DIRECT_FIELD_NUMBER: _ClassVar[int]
    upload_session_id: str
    storage_object_id: str
    multipart: _volume_pb2.MultipartUpload
    resumable: _volume_pb2.ResumableUpload
    azure_block: _volume_pb2.AzureBlockUpload
    direct: _volume_pb2.DirectUpload
    def __init__(
        self,
        upload_session_id: _Optional[str] = ...,
        storage_object_id: _Optional[str] = ...,
        multipart: _Optional[_Union[_volume_pb2.MultipartUpload, _Mapping]] = ...,
        resumable: _Optional[_Union[_volume_pb2.ResumableUpload, _Mapping]] = ...,
        azure_block: _Optional[_Union[_volume_pb2.AzureBlockUpload, _Mapping]] = ...,
        direct: _Optional[_Union[_volume_pb2.DirectUpload, _Mapping]] = ...,
    ) -> None: ...

class FinalizeDatasetUploadRequest(_message.Message):
    __slots__ = ("upload_session_id", "dataset_name", "arrow_schema_serialized")
    UPLOAD_SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    ARROW_SCHEMA_SERIALIZED_FIELD_NUMBER: _ClassVar[int]
    upload_session_id: str
    dataset_name: str
    arrow_schema_serialized: bytes
    def __init__(
        self,
        upload_session_id: _Optional[str] = ...,
        dataset_name: _Optional[str] = ...,
        arrow_schema_serialized: _Optional[bytes] = ...,
    ) -> None: ...

class FinalizeDatasetUploadResponse(_message.Message):
    __slots__ = ("dataset",)
    DATASET_FIELD_NUMBER: _ClassVar[int]
    dataset: DatasetMeta
    def __init__(self, dataset: _Optional[_Union[DatasetMeta, _Mapping]] = ...) -> None: ...

class RenameDatasetRequest(_message.Message):
    __slots__ = ("dataset_id", "new_name")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    new_name: str
    def __init__(self, dataset_id: _Optional[str] = ..., new_name: _Optional[str] = ...) -> None: ...

class RenameDatasetResponse(_message.Message):
    __slots__ = ("dataset",)
    DATASET_FIELD_NUMBER: _ClassVar[int]
    dataset: DatasetMeta
    def __init__(self, dataset: _Optional[_Union[DatasetMeta, _Mapping]] = ...) -> None: ...

class ArchiveDatasetRevisionRequest(_message.Message):
    __slots__ = ("revision_id",)
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    revision_id: str
    def __init__(self, revision_id: _Optional[str] = ...) -> None: ...

class ArchiveDatasetRevisionResponse(_message.Message):
    __slots__ = ("revision",)
    REVISION_FIELD_NUMBER: _ClassVar[int]
    revision: DatasetRevisionMeta
    def __init__(self, revision: _Optional[_Union[DatasetRevisionMeta, _Mapping]] = ...) -> None: ...

class ArchiveDatasetRevisionsRequest(_message.Message):
    __slots__ = ("revision_ids",)
    REVISION_IDS_FIELD_NUMBER: _ClassVar[int]
    revision_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, revision_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ArchiveDatasetRevisionsResponse(_message.Message):
    __slots__ = ("archived_revisions",)
    ARCHIVED_REVISIONS_FIELD_NUMBER: _ClassVar[int]
    archived_revisions: _containers.RepeatedCompositeFieldContainer[DatasetRevisionMeta]
    def __init__(
        self, archived_revisions: _Optional[_Iterable[_Union[DatasetRevisionMeta, _Mapping]]] = ...
    ) -> None: ...

class DeleteDatasetRequest(_message.Message):
    __slots__ = ("dataset_id",)
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    def __init__(self, dataset_id: _Optional[str] = ...) -> None: ...

class DeleteDatasetResponse(_message.Message):
    __slots__ = ("dataset_id",)
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    def __init__(self, dataset_id: _Optional[str] = ...) -> None: ...

class MaterializedAggregateTileMeta(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "operation_id",
        "aggregate_backfill_id",
        "materialization_key_hash",
        "aggregation",
        "aggregate_on",
        "groups",
        "bucket_on",
        "bucket_duration_ms",
        "coverage_lower_bound",
        "coverage_upper_bound",
        "source_kind",
        "file_count",
        "total_rows",
        "created_at",
        "updated_at",
        "materialization_key_json",
        "output_schema_bytes_base64",
        "source_meta_json",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BACKFILL_ID_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_KEY_HASH_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_ON_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_ON_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    SOURCE_KIND_FIELD_NUMBER: _ClassVar[int]
    FILE_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_ROWS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_KEY_JSON_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SCHEMA_BYTES_BASE64_FIELD_NUMBER: _ClassVar[int]
    SOURCE_META_JSON_FIELD_NUMBER: _ClassVar[int]
    id: int
    environment_id: str
    deployment_id: str
    operation_id: str
    aggregate_backfill_id: str
    materialization_key_hash: str
    aggregation: str
    aggregate_on: str
    groups: _containers.RepeatedScalarFieldContainer[str]
    bucket_on: str
    bucket_duration_ms: int
    coverage_lower_bound: _timestamp_pb2.Timestamp
    coverage_upper_bound: _timestamp_pb2.Timestamp
    source_kind: str
    file_count: int
    total_rows: int
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    materialization_key_json: str
    output_schema_bytes_base64: str
    source_meta_json: str
    def __init__(
        self,
        id: _Optional[int] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        operation_id: _Optional[str] = ...,
        aggregate_backfill_id: _Optional[str] = ...,
        materialization_key_hash: _Optional[str] = ...,
        aggregation: _Optional[str] = ...,
        aggregate_on: _Optional[str] = ...,
        groups: _Optional[_Iterable[str]] = ...,
        bucket_on: _Optional[str] = ...,
        bucket_duration_ms: _Optional[int] = ...,
        coverage_lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        coverage_upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        source_kind: _Optional[str] = ...,
        file_count: _Optional[int] = ...,
        total_rows: _Optional[int] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        materialization_key_json: _Optional[str] = ...,
        output_schema_bytes_base64: _Optional[str] = ...,
        source_meta_json: _Optional[str] = ...,
    ) -> None: ...

class MaterializedAggregateTileFileMeta(_message.Message):
    __slots__ = ("id", "environment_id", "deployment_id", "file_ordinal", "row_count", "uri", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_ORDINAL_FIELD_NUMBER: _ClassVar[int]
    ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    environment_id: str
    deployment_id: str
    file_ordinal: int
    row_count: int
    uri: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[int] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        file_ordinal: _Optional[int] = ...,
        row_count: _Optional[int] = ...,
        uri: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListMaterializedAggregateTilesRequest(_message.Message):
    __slots__ = ("cursor", "limit")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    def __init__(self, cursor: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class ListMaterializedAggregateTilesResponse(_message.Message):
    __slots__ = ("tiles", "next_cursor")
    TILES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    tiles: _containers.RepeatedCompositeFieldContainer[MaterializedAggregateTileMeta]
    next_cursor: str
    def __init__(
        self,
        tiles: _Optional[_Iterable[_Union[MaterializedAggregateTileMeta, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class ListMaterializedAggregateTilesForTimelineRequest(_message.Message):
    __slots__ = ("materialization_key_hash", "time_window", "cursor", "limit")
    MATERIALIZATION_KEY_HASH_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    materialization_key_hash: str
    time_window: _materialized_aggregate_tiles_pb2.MaterializedAggregateTileTimelineInterval
    cursor: str
    limit: int
    def __init__(
        self,
        materialization_key_hash: _Optional[str] = ...,
        time_window: _Optional[
            _Union[_materialized_aggregate_tiles_pb2.MaterializedAggregateTileTimelineInterval, _Mapping]
        ] = ...,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class ListMaterializedAggregateTilesForTimelineResponse(_message.Message):
    __slots__ = ("tiles", "next_cursor")
    TILES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    tiles: _containers.RepeatedCompositeFieldContainer[MaterializedAggregateTileMeta]
    next_cursor: str
    def __init__(
        self,
        tiles: _Optional[_Iterable[_Union[MaterializedAggregateTileMeta, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class ListMaterializedAggregateTileFilesRequest(_message.Message):
    __slots__ = ("manifest_id", "cursor", "limit")
    MANIFEST_ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    manifest_id: int
    cursor: str
    limit: int
    def __init__(
        self, manifest_id: _Optional[int] = ..., cursor: _Optional[str] = ..., limit: _Optional[int] = ...
    ) -> None: ...

class ListMaterializedAggregateTileFilesResponse(_message.Message):
    __slots__ = ("files", "next_cursor")
    FILES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[MaterializedAggregateTileFileMeta]
    next_cursor: str
    def __init__(
        self,
        files: _Optional[_Iterable[_Union[MaterializedAggregateTileFileMeta, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class GetMaterializedAggregateTileRowCountChartRequest(_message.Message):
    __slots__ = ("materialization_key_hash", "time_window")
    MATERIALIZATION_KEY_HASH_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    materialization_key_hash: str
    time_window: _materialized_aggregate_tiles_pb2.MaterializedAggregateTileTimelineInterval
    def __init__(
        self,
        materialization_key_hash: _Optional[str] = ...,
        time_window: _Optional[
            _Union[_materialized_aggregate_tiles_pb2.MaterializedAggregateTileTimelineInterval, _Mapping]
        ] = ...,
    ) -> None: ...

class GetMaterializedAggregateTileRowCountChartResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self, chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...
    ) -> None: ...

class DeleteMaterializedAggregateTileRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DeleteMaterializedAggregateTileResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetDatasetRevisionPreviewRequest(_message.Message):
    __slots__ = ("revision_id",)
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    revision_id: str
    def __init__(self, revision_id: _Optional[str] = ...) -> None: ...

class GetDatasetRevisionPreviewResponse(_message.Message):
    __slots__ = ("output_preview", "summary", "column_profiles")
    OUTPUT_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    COLUMN_PROFILES_FIELD_NUMBER: _ClassVar[int]
    output_preview: _struct_pb2.Value
    summary: _struct_pb2.Value
    column_profiles: _containers.RepeatedCompositeFieldContainer[_column_profile_pb2.ColumnProfile]
    def __init__(
        self,
        output_preview: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        summary: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        column_profiles: _Optional[_Iterable[_Union[_column_profile_pb2.ColumnProfile, _Mapping]]] = ...,
    ) -> None: ...

class GenerateDatasetStatsRequest(_message.Message):
    __slots__ = ("revision_id",)
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    revision_id: str
    def __init__(self, revision_id: _Optional[str] = ...) -> None: ...

class GenerateDatasetStatsResponse(_message.Message):
    __slots__ = ("summary",)
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    summary: _struct_pb2.Value
    def __init__(self, summary: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...

class DatasetEdf(_message.Message):
    __slots__ = ("id", "job_id", "feature_name", "data_max", "data_min", "data_count", "bucket_count", "bucket_values")
    ID_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_MAX_FIELD_NUMBER: _ClassVar[int]
    DATA_MIN_FIELD_NUMBER: _ClassVar[int]
    DATA_COUNT_FIELD_NUMBER: _ClassVar[int]
    BUCKET_COUNT_FIELD_NUMBER: _ClassVar[int]
    BUCKET_VALUES_FIELD_NUMBER: _ClassVar[int]
    id: str
    job_id: str
    feature_name: str
    data_max: float
    data_min: float
    data_count: int
    bucket_count: int
    bucket_values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(
        self,
        id: _Optional[str] = ...,
        job_id: _Optional[str] = ...,
        feature_name: _Optional[str] = ...,
        data_max: _Optional[float] = ...,
        data_min: _Optional[float] = ...,
        data_count: _Optional[int] = ...,
        bucket_count: _Optional[int] = ...,
        bucket_values: _Optional[_Iterable[float]] = ...,
    ) -> None: ...

class GetDatasetEdfsRequest(_message.Message):
    __slots__ = ("revision_id",)
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    revision_id: str
    def __init__(self, revision_id: _Optional[str] = ...) -> None: ...

class GetDatasetEdfsResponse(_message.Message):
    __slots__ = ("edfs",)
    EDFS_FIELD_NUMBER: _ClassVar[int]
    edfs: _containers.RepeatedCompositeFieldContainer[DatasetEdf]
    def __init__(self, edfs: _Optional[_Iterable[_Union[DatasetEdf, _Mapping]]] = ...) -> None: ...

class GenerateDatasetEdfsRequest(_message.Message):
    __slots__ = ("revision_id",)
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    revision_id: str
    def __init__(self, revision_id: _Optional[str] = ...) -> None: ...

class GenerateDatasetEdfsResponse(_message.Message):
    __slots__ = ("features",)
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, features: _Optional[_Iterable[str]] = ...) -> None: ...
