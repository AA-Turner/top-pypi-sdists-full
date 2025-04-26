from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.common.v1 import query_status_pb2 as _query_status_pb2
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

class DatasetSampleFilter(_message.Message):
    __slots__ = ("lower_bound", "upper_bound", "max_samples")
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    MAX_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    lower_bound: _timestamp_pb2.Timestamp
    upper_bound: _timestamp_pb2.Timestamp
    max_samples: int
    def __init__(
        self,
        lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        max_samples: _Optional[int] = ...,
    ) -> None: ...

class DatasetFilter(_message.Message):
    __slots__ = ("sample_filters", "max_cache_age_secs")
    SAMPLE_FILTERS_FIELD_NUMBER: _ClassVar[int]
    MAX_CACHE_AGE_SECS_FIELD_NUMBER: _ClassVar[int]
    sample_filters: DatasetSampleFilter
    max_cache_age_secs: float
    def __init__(
        self,
        sample_filters: _Optional[_Union[DatasetSampleFilter, _Mapping]] = ...,
        max_cache_age_secs: _Optional[float] = ...,
    ) -> None: ...

class DatasetRevisionResponse(_message.Message):
    __slots__ = (
        "dataset_name",
        "dataset_id",
        "environment_id",
        "revision_id",
        "creator_id",
        "outputs",
        "givens_uri",
        "status",
        "filters",
        "num_partitions",
        "num_bytes",
        "output_uris",
        "output_version",
        "branch",
        "dashboard_url",
        "created_at",
        "started_at",
        "terminated_at",
    )
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATOR_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    GIVENS_URI_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    NUM_PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    NUM_BYTES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_URIS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_VERSION_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_URL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    TERMINATED_AT_FIELD_NUMBER: _ClassVar[int]
    dataset_name: str
    dataset_id: str
    environment_id: str
    revision_id: str
    creator_id: str
    outputs: _containers.RepeatedScalarFieldContainer[str]
    givens_uri: str
    status: _query_status_pb2.QueryStatus
    filters: DatasetFilter
    num_partitions: int
    num_bytes: int
    output_uris: str
    output_version: int
    branch: str
    dashboard_url: str
    created_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    terminated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        dataset_name: _Optional[str] = ...,
        dataset_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        revision_id: _Optional[str] = ...,
        creator_id: _Optional[str] = ...,
        outputs: _Optional[_Iterable[str]] = ...,
        givens_uri: _Optional[str] = ...,
        status: _Optional[_Union[_query_status_pb2.QueryStatus, str]] = ...,
        filters: _Optional[_Union[DatasetFilter, _Mapping]] = ...,
        num_partitions: _Optional[int] = ...,
        num_bytes: _Optional[int] = ...,
        output_uris: _Optional[str] = ...,
        output_version: _Optional[int] = ...,
        branch: _Optional[str] = ...,
        dashboard_url: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        terminated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class DatasetResponse(_message.Message):
    __slots__ = ("is_finished", "version", "environment_id", "dataset_id", "dataset_name", "errors", "revisions")
    IS_FINISHED_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    REVISIONS_FIELD_NUMBER: _ClassVar[int]
    is_finished: bool
    version: int
    environment_id: str
    dataset_id: str
    dataset_name: str
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    revisions: _containers.RepeatedCompositeFieldContainer[DatasetRevisionResponse]
    def __init__(
        self,
        is_finished: bool = ...,
        version: _Optional[int] = ...,
        environment_id: _Optional[str] = ...,
        dataset_id: _Optional[str] = ...,
        dataset_name: _Optional[str] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        revisions: _Optional[_Iterable[_Union[DatasetRevisionResponse, _Mapping]]] = ...,
    ) -> None: ...
