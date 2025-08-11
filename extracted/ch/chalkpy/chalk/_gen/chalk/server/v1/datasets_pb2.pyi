from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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
    ) -> None: ...

class DatasetMeta(_message.Message):
    __slots__ = ("id", "environment_id", "dataset_name", "created_at", "most_recent_revision")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MOST_RECENT_REVISION_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    dataset_name: str
    created_at: _timestamp_pb2.Timestamp
    most_recent_revision: DatasetRevisionMeta
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        dataset_name: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        most_recent_revision: _Optional[_Union[DatasetRevisionMeta, _Mapping]] = ...,
    ) -> None: ...

class ListDatasetsRequest(_message.Message):
    __slots__ = ("cursor", "limit", "search")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    search: str
    def __init__(
        self, cursor: _Optional[str] = ..., limit: _Optional[int] = ..., search: _Optional[str] = ...
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
    __slots__ = ("dataset_id", "cursor", "limit")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    cursor: str
    limit: int
    def __init__(
        self, dataset_id: _Optional[str] = ..., cursor: _Optional[str] = ..., limit: _Optional[int] = ...
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
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetDatasetRevisionResponse(_message.Message):
    __slots__ = ("revision",)
    REVISION_FIELD_NUMBER: _ClassVar[int]
    revision: DatasetRevisionMeta
    def __init__(self, revision: _Optional[_Union[DatasetRevisionMeta, _Mapping]] = ...) -> None: ...
