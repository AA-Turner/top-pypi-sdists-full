from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import empty_pb2 as _empty_pb2
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

class OfflineWideTableRunKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE_WIDE_TABLE_RUN_KIND_UNSPECIFIED: _ClassVar[OfflineWideTableRunKind]
    OFFLINE_WIDE_TABLE_RUN_KIND_FILL: _ClassVar[OfflineWideTableRunKind]
    OFFLINE_WIDE_TABLE_RUN_KIND_COMPACT: _ClassVar[OfflineWideTableRunKind]

class OfflineWideTableRunStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE_WIDE_TABLE_RUN_STATUS_UNSPECIFIED: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_QUEUED: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_RUNNING: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_COMPLETED: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_FAILED: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_CANCELED: _ClassVar[OfflineWideTableRunStatus]
    OFFLINE_WIDE_TABLE_RUN_STATUS_SKIPPED: _ClassVar[OfflineWideTableRunStatus]

class OfflineWideTableRunSkipReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE_WIDE_TABLE_RUN_SKIP_REASON_UNSPECIFIED: _ClassVar[OfflineWideTableRunSkipReason]
    OFFLINE_WIDE_TABLE_RUN_SKIP_REASON_ACTIVE_PREDECESSOR: _ClassVar[OfflineWideTableRunSkipReason]

class OfflineWideTableRunTriggerKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE_WIDE_TABLE_RUN_TRIGGER_KIND_UNSPECIFIED: _ClassVar[OfflineWideTableRunTriggerKind]
    OFFLINE_WIDE_TABLE_RUN_TRIGGER_KIND_MANUAL: _ClassVar[OfflineWideTableRunTriggerKind]
    OFFLINE_WIDE_TABLE_RUN_TRIGGER_KIND_SCHEDULED: _ClassVar[OfflineWideTableRunTriggerKind]

class OfflineWideTableCompactionNamespaceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_UNSPECIFIED: _ClassVar[OfflineWideTableCompactionNamespaceStatus]
    OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_PENDING: _ClassVar[OfflineWideTableCompactionNamespaceStatus]
    OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_RUNNING: _ClassVar[OfflineWideTableCompactionNamespaceStatus]
    OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_COMPLETED: _ClassVar[OfflineWideTableCompactionNamespaceStatus]
    OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_FAILED: _ClassVar[OfflineWideTableCompactionNamespaceStatus]
    OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_SKIPPED_DISABLED: _ClassVar[
        OfflineWideTableCompactionNamespaceStatus
    ]

OFFLINE_WIDE_TABLE_RUN_KIND_UNSPECIFIED: OfflineWideTableRunKind
OFFLINE_WIDE_TABLE_RUN_KIND_FILL: OfflineWideTableRunKind
OFFLINE_WIDE_TABLE_RUN_KIND_COMPACT: OfflineWideTableRunKind
OFFLINE_WIDE_TABLE_RUN_STATUS_UNSPECIFIED: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_QUEUED: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_RUNNING: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_COMPLETED: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_FAILED: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_CANCELED: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_STATUS_SKIPPED: OfflineWideTableRunStatus
OFFLINE_WIDE_TABLE_RUN_SKIP_REASON_UNSPECIFIED: OfflineWideTableRunSkipReason
OFFLINE_WIDE_TABLE_RUN_SKIP_REASON_ACTIVE_PREDECESSOR: OfflineWideTableRunSkipReason
OFFLINE_WIDE_TABLE_RUN_TRIGGER_KIND_UNSPECIFIED: OfflineWideTableRunTriggerKind
OFFLINE_WIDE_TABLE_RUN_TRIGGER_KIND_MANUAL: OfflineWideTableRunTriggerKind
OFFLINE_WIDE_TABLE_RUN_TRIGGER_KIND_SCHEDULED: OfflineWideTableRunTriggerKind
OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_UNSPECIFIED: OfflineWideTableCompactionNamespaceStatus
OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_PENDING: OfflineWideTableCompactionNamespaceStatus
OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_RUNNING: OfflineWideTableCompactionNamespaceStatus
OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_COMPLETED: OfflineWideTableCompactionNamespaceStatus
OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_FAILED: OfflineWideTableCompactionNamespaceStatus
OFFLINE_WIDE_TABLE_COMPACTION_NAMESPACE_STATUS_SKIPPED_DISABLED: OfflineWideTableCompactionNamespaceStatus

class OfflineWideTableCompactionNamespaceResult(_message.Message):
    __slots__ = (
        "parent_run_id",
        "namespace",
        "status",
        "error_message",
        "created_at",
        "started_at",
        "finished_at",
        "job_queue_id",
        "wide_table_config_fingerprint",
    )
    PARENT_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    JOB_QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    WIDE_TABLE_CONFIG_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    parent_run_id: str
    namespace: str
    status: OfflineWideTableCompactionNamespaceStatus
    error_message: str
    created_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    job_queue_id: int
    wide_table_config_fingerprint: int
    def __init__(
        self,
        parent_run_id: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        status: _Optional[_Union[OfflineWideTableCompactionNamespaceStatus, str]] = ...,
        error_message: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        job_queue_id: _Optional[int] = ...,
        wide_table_config_fingerprint: _Optional[int] = ...,
    ) -> None: ...

class OfflineWideTableRun(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "kind",
        "namespace",
        "status",
        "watermark_before_micros",
        "watermark_after_micros",
        "rows_filled",
        "error_message",
        "created_at",
        "started_at",
        "finished_at",
        "job_queue_id",
        "skip_reason",
        "trigger_kind",
        "environment",
        "wide_table_config_fingerprint",
        "resource_group",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_BEFORE_MICROS_FIELD_NUMBER: _ClassVar[int]
    WATERMARK_AFTER_MICROS_FIELD_NUMBER: _ClassVar[int]
    ROWS_FILLED_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
    JOB_QUEUE_ID_FIELD_NUMBER: _ClassVar[int]
    SKIP_REASON_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_KIND_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    WIDE_TABLE_CONFIG_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    deployment_id: str
    kind: OfflineWideTableRunKind
    namespace: str
    status: OfflineWideTableRunStatus
    watermark_before_micros: int
    watermark_after_micros: int
    rows_filled: int
    error_message: str
    created_at: _timestamp_pb2.Timestamp
    started_at: _timestamp_pb2.Timestamp
    finished_at: _timestamp_pb2.Timestamp
    job_queue_id: int
    skip_reason: OfflineWideTableRunSkipReason
    trigger_kind: OfflineWideTableRunTriggerKind
    environment: _empty_pb2.Empty
    wide_table_config_fingerprint: int
    resource_group: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        kind: _Optional[_Union[OfflineWideTableRunKind, str]] = ...,
        namespace: _Optional[str] = ...,
        status: _Optional[_Union[OfflineWideTableRunStatus, str]] = ...,
        watermark_before_micros: _Optional[int] = ...,
        watermark_after_micros: _Optional[int] = ...,
        rows_filled: _Optional[int] = ...,
        error_message: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        finished_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        job_queue_id: _Optional[int] = ...,
        skip_reason: _Optional[_Union[OfflineWideTableRunSkipReason, str]] = ...,
        trigger_kind: _Optional[_Union[OfflineWideTableRunTriggerKind, str]] = ...,
        environment: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ...,
        wide_table_config_fingerprint: _Optional[int] = ...,
        resource_group: _Optional[str] = ...,
    ) -> None: ...

class ListOfflineWideTableRunsRequest(_message.Message):
    __slots__ = ("cursor", "limit", "namespace", "status", "kind", "trigger_kind")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_KIND_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    namespace: str
    status: OfflineWideTableRunStatus
    kind: OfflineWideTableRunKind
    trigger_kind: OfflineWideTableRunTriggerKind
    def __init__(
        self,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        namespace: _Optional[str] = ...,
        status: _Optional[_Union[OfflineWideTableRunStatus, str]] = ...,
        kind: _Optional[_Union[OfflineWideTableRunKind, str]] = ...,
        trigger_kind: _Optional[_Union[OfflineWideTableRunTriggerKind, str]] = ...,
    ) -> None: ...

class ListOfflineWideTableRunsResponse(_message.Message):
    __slots__ = ("runs", "cursor")
    RUNS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    runs: _containers.RepeatedCompositeFieldContainer[OfflineWideTableRun]
    cursor: str
    def __init__(
        self, runs: _Optional[_Iterable[_Union[OfflineWideTableRun, _Mapping]]] = ..., cursor: _Optional[str] = ...
    ) -> None: ...

class GetOfflineWideTableRunRequest(_message.Message):
    __slots__ = ("run_id",)
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    def __init__(self, run_id: _Optional[str] = ...) -> None: ...

class GetOfflineWideTableRunResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: OfflineWideTableRun
    def __init__(self, run: _Optional[_Union[OfflineWideTableRun, _Mapping]] = ...) -> None: ...

class OfflineWideTableSchedule(_message.Message):
    __slots__ = ("id", "name", "namespace", "crontab", "kind")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CRONTAB_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    namespace: str
    crontab: str
    kind: OfflineWideTableRunKind
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        crontab: _Optional[str] = ...,
        kind: _Optional[_Union[OfflineWideTableRunKind, str]] = ...,
    ) -> None: ...

class OfflineWideTableBackpressureStats(_message.Message):
    __slots__ = (
        "is_behind",
        "unfinished_runs",
        "oldest_unfinished_duration_seconds",
        "oldest_unfinished_cadence_seconds",
    )
    IS_BEHIND_FIELD_NUMBER: _ClassVar[int]
    UNFINISHED_RUNS_FIELD_NUMBER: _ClassVar[int]
    OLDEST_UNFINISHED_DURATION_SECONDS_FIELD_NUMBER: _ClassVar[int]
    OLDEST_UNFINISHED_CADENCE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    is_behind: bool
    unfinished_runs: int
    oldest_unfinished_duration_seconds: float
    oldest_unfinished_cadence_seconds: float
    def __init__(
        self,
        is_behind: bool = ...,
        unfinished_runs: _Optional[int] = ...,
        oldest_unfinished_duration_seconds: _Optional[float] = ...,
        oldest_unfinished_cadence_seconds: _Optional[float] = ...,
    ) -> None: ...

class OfflineWideTableScheduleInfo(_message.Message):
    __slots__ = ("schedule", "latest_run", "backpressure_stats")
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    LATEST_RUN_FIELD_NUMBER: _ClassVar[int]
    BACKPRESSURE_STATS_FIELD_NUMBER: _ClassVar[int]
    schedule: OfflineWideTableSchedule
    latest_run: OfflineWideTableRun
    backpressure_stats: OfflineWideTableBackpressureStats
    def __init__(
        self,
        schedule: _Optional[_Union[OfflineWideTableSchedule, _Mapping]] = ...,
        latest_run: _Optional[_Union[OfflineWideTableRun, _Mapping]] = ...,
        backpressure_stats: _Optional[_Union[OfflineWideTableBackpressureStats, _Mapping]] = ...,
    ) -> None: ...

class GetActiveOfflineWideTableSchedulesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetActiveOfflineWideTableSchedulesResponse(_message.Message):
    __slots__ = ("schedules",)
    SCHEDULES_FIELD_NUMBER: _ClassVar[int]
    schedules: _containers.RepeatedCompositeFieldContainer[OfflineWideTableScheduleInfo]
    def __init__(
        self, schedules: _Optional[_Iterable[_Union[OfflineWideTableScheduleInfo, _Mapping]]] = ...
    ) -> None: ...

class OfflineWideTableFillInfo(_message.Message):
    __slots__ = ("schedule", "latest_run", "backpressure_stats")
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    LATEST_RUN_FIELD_NUMBER: _ClassVar[int]
    BACKPRESSURE_STATS_FIELD_NUMBER: _ClassVar[int]
    schedule: OfflineWideTableSchedule
    latest_run: OfflineWideTableRun
    backpressure_stats: OfflineWideTableBackpressureStats
    def __init__(
        self,
        schedule: _Optional[_Union[OfflineWideTableSchedule, _Mapping]] = ...,
        latest_run: _Optional[_Union[OfflineWideTableRun, _Mapping]] = ...,
        backpressure_stats: _Optional[_Union[OfflineWideTableBackpressureStats, _Mapping]] = ...,
    ) -> None: ...

class OfflineWideTableCompactionInfo(_message.Message):
    __slots__ = ("background_compaction_enabled", "latest_manual_run", "latest_weekly_run", "latest_weekly_result")
    BACKGROUND_COMPACTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LATEST_MANUAL_RUN_FIELD_NUMBER: _ClassVar[int]
    LATEST_WEEKLY_RUN_FIELD_NUMBER: _ClassVar[int]
    LATEST_WEEKLY_RESULT_FIELD_NUMBER: _ClassVar[int]
    background_compaction_enabled: bool
    latest_manual_run: OfflineWideTableRun
    latest_weekly_run: OfflineWideTableRun
    latest_weekly_result: OfflineWideTableCompactionNamespaceResult
    def __init__(
        self,
        background_compaction_enabled: bool = ...,
        latest_manual_run: _Optional[_Union[OfflineWideTableRun, _Mapping]] = ...,
        latest_weekly_run: _Optional[_Union[OfflineWideTableRun, _Mapping]] = ...,
        latest_weekly_result: _Optional[_Union[OfflineWideTableCompactionNamespaceResult, _Mapping]] = ...,
    ) -> None: ...

class OfflineWideTableNamespaceInfo(_message.Message):
    __slots__ = ("namespace", "fill", "compaction")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FILL_FIELD_NUMBER: _ClassVar[int]
    COMPACTION_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    fill: OfflineWideTableFillInfo
    compaction: OfflineWideTableCompactionInfo
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        fill: _Optional[_Union[OfflineWideTableFillInfo, _Mapping]] = ...,
        compaction: _Optional[_Union[OfflineWideTableCompactionInfo, _Mapping]] = ...,
    ) -> None: ...

class OfflineWideTableEnvironmentMaintenanceInfo(_message.Message):
    __slots__ = ("latest_weekly_run", "next_weekly_run_at")
    LATEST_WEEKLY_RUN_FIELD_NUMBER: _ClassVar[int]
    NEXT_WEEKLY_RUN_AT_FIELD_NUMBER: _ClassVar[int]
    latest_weekly_run: OfflineWideTableRun
    next_weekly_run_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        latest_weekly_run: _Optional[_Union[OfflineWideTableRun, _Mapping]] = ...,
        next_weekly_run_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class OfflineWideTableActiveConfiguration(_message.Message):
    __slots__ = ("namespace", "config_fingerprint")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    config_fingerprint: int
    def __init__(self, namespace: _Optional[str] = ..., config_fingerprint: _Optional[int] = ...) -> None: ...

class GetOfflineWideTableNamespacesRequest(_message.Message):
    __slots__ = ("active_configurations",)
    ACTIVE_CONFIGURATIONS_FIELD_NUMBER: _ClassVar[int]
    active_configurations: _containers.RepeatedCompositeFieldContainer[OfflineWideTableActiveConfiguration]
    def __init__(
        self, active_configurations: _Optional[_Iterable[_Union[OfflineWideTableActiveConfiguration, _Mapping]]] = ...
    ) -> None: ...

class GetOfflineWideTableNamespacesResponse(_message.Message):
    __slots__ = ("namespaces", "environment_maintenance", "latest_completed_fill_at")
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    LATEST_COMPLETED_FILL_AT_FIELD_NUMBER: _ClassVar[int]
    namespaces: _containers.RepeatedCompositeFieldContainer[OfflineWideTableNamespaceInfo]
    environment_maintenance: OfflineWideTableEnvironmentMaintenanceInfo
    latest_completed_fill_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        namespaces: _Optional[_Iterable[_Union[OfflineWideTableNamespaceInfo, _Mapping]]] = ...,
        environment_maintenance: _Optional[_Union[OfflineWideTableEnvironmentMaintenanceInfo, _Mapping]] = ...,
        latest_completed_fill_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class TriggerOfflineWideTableFillRequest(_message.Message):
    __slots__ = ("namespace", "resource_group")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    resource_group: str
    def __init__(self, namespace: _Optional[str] = ..., resource_group: _Optional[str] = ...) -> None: ...

class TriggerOfflineWideTableFillResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: OfflineWideTableRun
    def __init__(self, run: _Optional[_Union[OfflineWideTableRun, _Mapping]] = ...) -> None: ...

class TriggerOfflineWideTableCompactionRequest(_message.Message):
    __slots__ = ("namespace", "resource_group")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    resource_group: str
    def __init__(self, namespace: _Optional[str] = ..., resource_group: _Optional[str] = ...) -> None: ...

class TriggerOfflineWideTableCompactionResponse(_message.Message):
    __slots__ = ("operation_id",)
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    def __init__(self, operation_id: _Optional[str] = ...) -> None: ...
