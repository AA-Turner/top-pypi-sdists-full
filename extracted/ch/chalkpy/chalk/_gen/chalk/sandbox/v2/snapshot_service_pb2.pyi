from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import tag_filter_pb2 as _tag_filter_pb2
from chalk._gen.chalk.container.v1 import service_pb2 as _service_pb2
from chalk._gen.chalk.container.v1 import snapshot_compatibility_pb2 as _snapshot_compatibility_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
from chalk._gen.chalk.volume.v2 import volume_pb2 as _volume_pb2
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

class SandboxSnapshotStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SANDBOX_SNAPSHOT_STATUS_UNSPECIFIED: _ClassVar[SandboxSnapshotStatus]
    SANDBOX_SNAPSHOT_STATUS_PENDING: _ClassVar[SandboxSnapshotStatus]
    SANDBOX_SNAPSHOT_STATUS_IN_PROGRESS: _ClassVar[SandboxSnapshotStatus]
    SANDBOX_SNAPSHOT_STATUS_COMPLETED: _ClassVar[SandboxSnapshotStatus]
    SANDBOX_SNAPSHOT_STATUS_FAILED: _ClassVar[SandboxSnapshotStatus]

class SandboxSnapshotPhase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SANDBOX_SNAPSHOT_PHASE_UNSPECIFIED: _ClassVar[SandboxSnapshotPhase]
    SANDBOX_SNAPSHOT_PHASE_PENDING: _ClassVar[SandboxSnapshotPhase]
    SANDBOX_SNAPSHOT_PHASE_CHECKPOINTING: _ClassVar[SandboxSnapshotPhase]
    SANDBOX_SNAPSHOT_PHASE_UPLOADING: _ClassVar[SandboxSnapshotPhase]
    SANDBOX_SNAPSHOT_PHASE_PUBLISHING: _ClassVar[SandboxSnapshotPhase]
    SANDBOX_SNAPSHOT_PHASE_COMPLETED: _ClassVar[SandboxSnapshotPhase]
    SANDBOX_SNAPSHOT_PHASE_FAILED: _ClassVar[SandboxSnapshotPhase]
    SANDBOX_SNAPSHOT_PHASE_RECOVERY_REQUIRED: _ClassVar[SandboxSnapshotPhase]

class SandboxSnapshotSortColumn(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SANDBOX_SNAPSHOT_SORT_COLUMN_UNSPECIFIED: _ClassVar[SandboxSnapshotSortColumn]
    SANDBOX_SNAPSHOT_SORT_COLUMN_CREATED_AT: _ClassVar[SandboxSnapshotSortColumn]

class SandboxSnapshotSortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SANDBOX_SNAPSHOT_SORT_ORDER_UNSPECIFIED: _ClassVar[SandboxSnapshotSortOrder]
    SANDBOX_SNAPSHOT_SORT_ORDER_DESC: _ClassVar[SandboxSnapshotSortOrder]
    SANDBOX_SNAPSHOT_SORT_ORDER_ASC: _ClassVar[SandboxSnapshotSortOrder]

SANDBOX_SNAPSHOT_STATUS_UNSPECIFIED: SandboxSnapshotStatus
SANDBOX_SNAPSHOT_STATUS_PENDING: SandboxSnapshotStatus
SANDBOX_SNAPSHOT_STATUS_IN_PROGRESS: SandboxSnapshotStatus
SANDBOX_SNAPSHOT_STATUS_COMPLETED: SandboxSnapshotStatus
SANDBOX_SNAPSHOT_STATUS_FAILED: SandboxSnapshotStatus
SANDBOX_SNAPSHOT_PHASE_UNSPECIFIED: SandboxSnapshotPhase
SANDBOX_SNAPSHOT_PHASE_PENDING: SandboxSnapshotPhase
SANDBOX_SNAPSHOT_PHASE_CHECKPOINTING: SandboxSnapshotPhase
SANDBOX_SNAPSHOT_PHASE_UPLOADING: SandboxSnapshotPhase
SANDBOX_SNAPSHOT_PHASE_PUBLISHING: SandboxSnapshotPhase
SANDBOX_SNAPSHOT_PHASE_COMPLETED: SandboxSnapshotPhase
SANDBOX_SNAPSHOT_PHASE_FAILED: SandboxSnapshotPhase
SANDBOX_SNAPSHOT_PHASE_RECOVERY_REQUIRED: SandboxSnapshotPhase
SANDBOX_SNAPSHOT_SORT_COLUMN_UNSPECIFIED: SandboxSnapshotSortColumn
SANDBOX_SNAPSHOT_SORT_COLUMN_CREATED_AT: SandboxSnapshotSortColumn
SANDBOX_SNAPSHOT_SORT_ORDER_UNSPECIFIED: SandboxSnapshotSortOrder
SANDBOX_SNAPSHOT_SORT_ORDER_DESC: SandboxSnapshotSortOrder
SANDBOX_SNAPSHOT_SORT_ORDER_ASC: SandboxSnapshotSortOrder

class SandboxSnapshotProgress(_message.Message):
    __slots__ = ("phase", "bytes_completed", "bytes_total", "updated_at")
    PHASE_FIELD_NUMBER: _ClassVar[int]
    BYTES_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    BYTES_TOTAL_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    phase: SandboxSnapshotPhase
    bytes_completed: int
    bytes_total: int
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        phase: _Optional[_Union[SandboxSnapshotPhase, str]] = ...,
        bytes_completed: _Optional[int] = ...,
        bytes_total: _Optional[int] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GKEPodSnapshot(_message.Message):
    __slots__ = ("storage_bucket", "storage_path")
    STORAGE_BUCKET_FIELD_NUMBER: _ClassVar[int]
    STORAGE_PATH_FIELD_NUMBER: _ClassVar[int]
    storage_bucket: str
    storage_path: str
    def __init__(self, storage_bucket: _Optional[str] = ..., storage_path: _Optional[str] = ...) -> None: ...

class HypervisorSnapshot(_message.Message):
    __slots__ = ("storage_uri", "snapshot_id", "compatibility")
    STORAGE_URI_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_ID_FIELD_NUMBER: _ClassVar[int]
    COMPATIBILITY_FIELD_NUMBER: _ClassVar[int]
    storage_uri: str
    snapshot_id: str
    compatibility: _snapshot_compatibility_pb2.SnapshotCompatibility
    def __init__(
        self,
        storage_uri: _Optional[str] = ...,
        snapshot_id: _Optional[str] = ...,
        compatibility: _Optional[_Union[_snapshot_compatibility_pb2.SnapshotCompatibility, _Mapping]] = ...,
    ) -> None: ...

class SandboxSnapshotSpec(_message.Message):
    __slots__ = ("gke_pod_snapshot", "hypervisor_snapshot")
    GKE_POD_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    HYPERVISOR_SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    gke_pod_snapshot: GKEPodSnapshot
    hypervisor_snapshot: HypervisorSnapshot
    def __init__(
        self,
        gke_pod_snapshot: _Optional[_Union[GKEPodSnapshot, _Mapping]] = ...,
        hypervisor_snapshot: _Optional[_Union[HypervisorSnapshot, _Mapping]] = ...,
    ) -> None: ...

class SandboxSnapshot(_message.Message):
    __slots__ = (
        "id",
        "sandbox_id",
        "spec",
        "snapshot_spec",
        "status",
        "status_message",
        "created_at",
        "completed_at",
        "created_by",
        "progress",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    SANDBOX_ID_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    id: str
    sandbox_id: str
    spec: _service_pb2.ChalkContainerSpec
    snapshot_spec: SandboxSnapshotSpec
    status: SandboxSnapshotStatus
    status_message: str
    created_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    created_by: str
    progress: SandboxSnapshotProgress
    def __init__(
        self,
        id: _Optional[str] = ...,
        sandbox_id: _Optional[str] = ...,
        spec: _Optional[_Union[_service_pb2.ChalkContainerSpec, _Mapping]] = ...,
        snapshot_spec: _Optional[_Union[SandboxSnapshotSpec, _Mapping]] = ...,
        status: _Optional[_Union[SandboxSnapshotStatus, str]] = ...,
        status_message: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        created_by: _Optional[str] = ...,
        progress: _Optional[_Union[SandboxSnapshotProgress, _Mapping]] = ...,
    ) -> None: ...

class StartSandboxSnapshotRequest(_message.Message):
    __slots__ = ("sandbox_id", "idempotency_key")
    SANDBOX_ID_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    sandbox_id: str
    idempotency_key: str
    def __init__(self, sandbox_id: _Optional[str] = ..., idempotency_key: _Optional[str] = ...) -> None: ...

class StartSandboxSnapshotResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: SandboxSnapshot
    def __init__(self, snapshot: _Optional[_Union[SandboxSnapshot, _Mapping]] = ...) -> None: ...

class CreateSandboxSnapshotRequest(_message.Message):
    __slots__ = ("sandbox_id",)
    SANDBOX_ID_FIELD_NUMBER: _ClassVar[int]
    sandbox_id: str
    def __init__(self, sandbox_id: _Optional[str] = ...) -> None: ...

class CreateSandboxSnapshotResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: SandboxSnapshot
    def __init__(self, snapshot: _Optional[_Union[SandboxSnapshot, _Mapping]] = ...) -> None: ...

class GetSandboxSnapshotRequest(_message.Message):
    __slots__ = ("snapshot_id",)
    SNAPSHOT_ID_FIELD_NUMBER: _ClassVar[int]
    snapshot_id: str
    def __init__(self, snapshot_id: _Optional[str] = ...) -> None: ...

class GetSandboxSnapshotResponse(_message.Message):
    __slots__ = ("snapshot",)
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    snapshot: SandboxSnapshot
    def __init__(self, snapshot: _Optional[_Union[SandboxSnapshot, _Mapping]] = ...) -> None: ...

class ListSandboxSnapshotsFilters(_message.Message):
    __slots__ = ("sandbox_ids", "statuses", "status_values", "created_by", "tag_filter")
    SANDBOX_IDS_FIELD_NUMBER: _ClassVar[int]
    STATUSES_FIELD_NUMBER: _ClassVar[int]
    STATUS_VALUES_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    TAG_FILTER_FIELD_NUMBER: _ClassVar[int]
    sandbox_ids: _containers.RepeatedScalarFieldContainer[str]
    statuses: _containers.RepeatedScalarFieldContainer[str]
    status_values: _containers.RepeatedScalarFieldContainer[SandboxSnapshotStatus]
    created_by: _containers.RepeatedScalarFieldContainer[str]
    tag_filter: _tag_filter_pb2.TagFilter
    def __init__(
        self,
        sandbox_ids: _Optional[_Iterable[str]] = ...,
        statuses: _Optional[_Iterable[str]] = ...,
        status_values: _Optional[_Iterable[_Union[SandboxSnapshotStatus, str]]] = ...,
        created_by: _Optional[_Iterable[str]] = ...,
        tag_filter: _Optional[_Union[_tag_filter_pb2.TagFilter, _Mapping]] = ...,
    ) -> None: ...

class ListSandboxSnapshotsRequest(_message.Message):
    __slots__ = ("limit", "cursor", "search", "filters", "sort_column", "sort_order")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    SORT_COLUMN_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    search: str
    filters: ListSandboxSnapshotsFilters
    sort_column: SandboxSnapshotSortColumn
    sort_order: SandboxSnapshotSortOrder
    def __init__(
        self,
        limit: _Optional[int] = ...,
        cursor: _Optional[str] = ...,
        search: _Optional[str] = ...,
        filters: _Optional[_Union[ListSandboxSnapshotsFilters, _Mapping]] = ...,
        sort_column: _Optional[_Union[SandboxSnapshotSortColumn, str]] = ...,
        sort_order: _Optional[_Union[SandboxSnapshotSortOrder, str]] = ...,
    ) -> None: ...

class ListSandboxSnapshotsResponse(_message.Message):
    __slots__ = ("snapshots", "next_cursor")
    SNAPSHOTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    snapshots: _containers.RepeatedCompositeFieldContainer[SandboxSnapshot]
    next_cursor: str
    def __init__(
        self,
        snapshots: _Optional[_Iterable[_Union[SandboxSnapshot, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class DeleteSandboxSnapshotRequest(_message.Message):
    __slots__ = ("snapshot_id",)
    SNAPSHOT_ID_FIELD_NUMBER: _ClassVar[int]
    snapshot_id: str
    def __init__(self, snapshot_id: _Optional[str] = ...) -> None: ...

class DeleteSandboxSnapshotResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSnapshotStoreCredentialsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSnapshotStoreCredentialsResponse(_message.Message):
    __slots__ = ("storage", "prefixes", "expires_at", "aws", "gcp")
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    PREFIXES_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    AWS_FIELD_NUMBER: _ClassVar[int]
    GCP_FIELD_NUMBER: _ClassVar[int]
    storage: _volume_pb2.ObjectStoreConfig
    prefixes: _containers.RepeatedScalarFieldContainer[str]
    expires_at: _timestamp_pb2.Timestamp
    aws: _volume_pb2.AwsSessionCredentials
    gcp: _volume_pb2.GcpAccessToken
    def __init__(
        self,
        storage: _Optional[_Union[_volume_pb2.ObjectStoreConfig, _Mapping]] = ...,
        prefixes: _Optional[_Iterable[str]] = ...,
        expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        aws: _Optional[_Union[_volume_pb2.AwsSessionCredentials, _Mapping]] = ...,
        gcp: _Optional[_Union[_volume_pb2.GcpAccessToken, _Mapping]] = ...,
    ) -> None: ...
