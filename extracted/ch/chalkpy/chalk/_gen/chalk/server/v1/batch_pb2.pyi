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

class OperationKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPERATION_KIND_UNSPECIFIED: _ClassVar[OperationKind]
    OPERATION_KIND_CRON: _ClassVar[OperationKind]
    OPERATION_KIND_MIGRATION: _ClassVar[OperationKind]

class OperationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPERATION_STATUS_UNSPECIFIED: _ClassVar[OperationStatus]
    OPERATION_STATUS_PENDING: _ClassVar[OperationStatus]
    OPERATION_STATUS_WORKING: _ClassVar[OperationStatus]
    OPERATION_STATUS_COMPLETE: _ClassVar[OperationStatus]
    OPERATION_STATUS_FAILED: _ClassVar[OperationStatus]
    OPERATION_STATUS_SKIPPED: _ClassVar[OperationStatus]
    OPERATION_STATUS_CANCELED: _ClassVar[OperationStatus]

OPERATION_KIND_UNSPECIFIED: OperationKind
OPERATION_KIND_CRON: OperationKind
OPERATION_KIND_MIGRATION: OperationKind
OPERATION_STATUS_UNSPECIFIED: OperationStatus
OPERATION_STATUS_PENDING: OperationStatus
OPERATION_STATUS_WORKING: OperationStatus
OPERATION_STATUS_COMPLETE: OperationStatus
OPERATION_STATUS_FAILED: OperationStatus
OPERATION_STATUS_SKIPPED: OperationStatus
OPERATION_STATUS_CANCELED: OperationStatus

class ProgressCounts(_message.Message):
    __slots__ = (
        "start",
        "max_observed",
        "total_duration_s",
        "stored_online",
        "stored_offline",
        "computed",
        "dropped",
        "failed",
        "skipped",
        "end",
    )
    START_FIELD_NUMBER: _ClassVar[int]
    MAX_OBSERVED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DURATION_S_FIELD_NUMBER: _ClassVar[int]
    STORED_ONLINE_FIELD_NUMBER: _ClassVar[int]
    STORED_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    COMPUTED_FIELD_NUMBER: _ClassVar[int]
    DROPPED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: _timestamp_pb2.Timestamp
    max_observed: _timestamp_pb2.Timestamp
    total_duration_s: float
    stored_online: float
    stored_offline: float
    computed: float
    dropped: float
    failed: float
    skipped: float
    end: _timestamp_pb2.Timestamp
    def __init__(
        self,
        start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        max_observed: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        total_duration_s: _Optional[float] = ...,
        stored_online: _Optional[float] = ...,
        stored_offline: _Optional[float] = ...,
        computed: _Optional[float] = ...,
        dropped: _Optional[float] = ...,
        failed: _Optional[float] = ...,
        skipped: _Optional[float] = ...,
        end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ResolverOperation(_message.Message):
    __slots__ = ("resolver_fqn", "status", "progress")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    status: OperationStatus
    progress: ProgressCounts
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        status: _Optional[_Union[OperationStatus, str]] = ...,
        progress: _Optional[_Union[ProgressCounts, _Mapping]] = ...,
    ) -> None: ...

class BatchOperation(_message.Message):
    __slots__ = ("id", "kind", "status", "resolvers", "progress", "environment_id", "team_id", "deployment_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    kind: OperationKind
    status: OperationStatus
    resolvers: _containers.RepeatedCompositeFieldContainer[ResolverOperation]
    progress: ProgressCounts
    environment_id: str
    team_id: str
    deployment_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        kind: _Optional[_Union[OperationKind, str]] = ...,
        status: _Optional[_Union[OperationStatus, str]] = ...,
        resolvers: _Optional[_Iterable[_Union[ResolverOperation, _Mapping]]] = ...,
        progress: _Optional[_Union[ProgressCounts, _Mapping]] = ...,
        environment_id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
    ) -> None: ...
