from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from chalk._gen.chalk.graph.v1 import source_file_reference_pb2 as _source_file_reference_pb2
from chalk._gen.chalk.graph.v1 import sql_resolver_retry_policy_pb2 as _sql_resolver_retry_policy_pb2
from chalk._gen.chalk.server.v1 import scheduled_query_run_pb2 as _scheduled_query_run_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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
        "fill_bytes_scanned",
        "fill_compute_ms",
        "hwm_probe_bytes_scanned",
        "hwm_probe_compute_ms",
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
    FILL_BYTES_SCANNED_FIELD_NUMBER: _ClassVar[int]
    FILL_COMPUTE_MS_FIELD_NUMBER: _ClassVar[int]
    HWM_PROBE_BYTES_SCANNED_FIELD_NUMBER: _ClassVar[int]
    HWM_PROBE_COMPUTE_MS_FIELD_NUMBER: _ClassVar[int]
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
    fill_bytes_scanned: int
    fill_compute_ms: int
    hwm_probe_bytes_scanned: int
    hwm_probe_compute_ms: int
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
        fill_bytes_scanned: _Optional[int] = ...,
        fill_compute_ms: _Optional[int] = ...,
        hwm_probe_bytes_scanned: _Optional[int] = ...,
        hwm_probe_compute_ms: _Optional[int] = ...,
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
    __slots__ = ("namespace", "fill", "compaction", "control")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FILL_FIELD_NUMBER: _ClassVar[int]
    COMPACTION_FIELD_NUMBER: _ClassVar[int]
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    fill: OfflineWideTableFillInfo
    compaction: OfflineWideTableCompactionInfo
    control: MaterializedFeatureViewControl
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        fill: _Optional[_Union[OfflineWideTableFillInfo, _Mapping]] = ...,
        compaction: _Optional[_Union[OfflineWideTableCompactionInfo, _Mapping]] = ...,
        control: _Optional[_Union[MaterializedFeatureViewControl, _Mapping]] = ...,
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

class TriggerOfflineWideTableOverrideFillRequest(_message.Message):
    __slots__ = (
        "namespace",
        "materialized_feature_view",
        "inserted_at_lower_bound_exclusive",
        "inserted_at_upper_bound_inclusive",
        "resource_group",
        "observed_at_upper_bound_exclusive",
    )
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZED_FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    INSERTED_AT_LOWER_BOUND_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    INSERTED_AT_UPPER_BOUND_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_AT_UPPER_BOUND_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    materialized_feature_view: _graph_pb2.MaterializedFeatureView
    inserted_at_lower_bound_exclusive: _timestamp_pb2.Timestamp
    inserted_at_upper_bound_inclusive: _timestamp_pb2.Timestamp
    resource_group: str
    observed_at_upper_bound_exclusive: _timestamp_pb2.Timestamp
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        materialized_feature_view: _Optional[_Union[_graph_pb2.MaterializedFeatureView, _Mapping]] = ...,
        inserted_at_lower_bound_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        inserted_at_upper_bound_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        resource_group: _Optional[str] = ...,
        observed_at_upper_bound_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class TriggerOfflineWideTableOverrideFillResponse(_message.Message):
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

class MaterializedFeatureViewControl(_message.Message):
    __slots__ = ("name", "status", "agent_id", "updated_at")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: _scheduled_query_run_pb2.CronControlStatus
    agent_id: str
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        name: _Optional[str] = ...,
        status: _Optional[_Union[_scheduled_query_run_pb2.CronControlStatus, str]] = ...,
        agent_id: _Optional[str] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class UpdateMaterializedFeatureViewControlOperation(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _scheduled_query_run_pb2.CronControlStatus
    def __init__(self, status: _Optional[_Union[_scheduled_query_run_pb2.CronControlStatus, str]] = ...) -> None: ...

class UpdateMaterializedFeatureViewControlRequest(_message.Message):
    __slots__ = ("name", "status", "update_mask", "update")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: _scheduled_query_run_pb2.CronControlStatus
    update_mask: _field_mask_pb2.FieldMask
    update: UpdateMaterializedFeatureViewControlOperation
    def __init__(
        self,
        name: _Optional[str] = ...,
        status: _Optional[_Union[_scheduled_query_run_pb2.CronControlStatus, str]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
        update: _Optional[_Union[UpdateMaterializedFeatureViewControlOperation, _Mapping]] = ...,
    ) -> None: ...

class UpdateMaterializedFeatureViewControlResponse(_message.Message):
    __slots__ = ("control",)
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    control: MaterializedFeatureViewControl
    def __init__(self, control: _Optional[_Union[MaterializedFeatureViewControl, _Mapping]] = ...) -> None: ...

class OfflineWideTableFeatureWatermark(_message.Message):
    __slots__ = ("config_fingerprint", "persistence_key", "filled_through", "updated_at", "feature_fqn")
    CONFIG_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_KEY_FIELD_NUMBER: _ClassVar[int]
    FILLED_THROUGH_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    config_fingerprint: int
    persistence_key: str
    filled_through: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    feature_fqn: str
    def __init__(
        self,
        config_fingerprint: _Optional[int] = ...,
        persistence_key: _Optional[str] = ...,
        filled_through: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        feature_fqn: _Optional[str] = ...,
    ) -> None: ...

class GetOfflineWideTableFeatureWatermarksRequest(_message.Message):
    __slots__ = ("namespace", "config_fingerprint", "persistence_keys", "feature_fqns")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_KEYS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FQNS_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    config_fingerprint: int
    persistence_keys: _containers.RepeatedScalarFieldContainer[str]
    feature_fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        config_fingerprint: _Optional[int] = ...,
        persistence_keys: _Optional[_Iterable[str]] = ...,
        feature_fqns: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetOfflineWideTableFeatureWatermarksResponse(_message.Message):
    __slots__ = ("watermarks",)
    WATERMARKS_FIELD_NUMBER: _ClassVar[int]
    watermarks: _containers.RepeatedCompositeFieldContainer[OfflineWideTableFeatureWatermark]
    def __init__(
        self, watermarks: _Optional[_Iterable[_Union[OfflineWideTableFeatureWatermark, _Mapping]]] = ...
    ) -> None: ...

class OfflineWideTableFeatureWatermarkUpdate(_message.Message):
    __slots__ = ("feature_fqn", "filled_through")
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    FILLED_THROUGH_FIELD_NUMBER: _ClassVar[int]
    feature_fqn: str
    filled_through: _timestamp_pb2.Timestamp
    def __init__(
        self,
        feature_fqn: _Optional[str] = ...,
        filled_through: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class SetOfflineWideTableFeatureWatermarksRequest(_message.Message):
    __slots__ = ("namespace", "config_fingerprint", "updates")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    config_fingerprint: int
    updates: _containers.RepeatedCompositeFieldContainer[OfflineWideTableFeatureWatermarkUpdate]
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        config_fingerprint: _Optional[int] = ...,
        updates: _Optional[_Iterable[_Union[OfflineWideTableFeatureWatermarkUpdate, _Mapping]]] = ...,
    ) -> None: ...

class SetOfflineWideTableFeatureWatermarksResponse(_message.Message):
    __slots__ = ("watermarks_written",)
    WATERMARKS_WRITTEN_FIELD_NUMBER: _ClassVar[int]
    watermarks_written: int
    def __init__(self, watermarks_written: _Optional[int] = ...) -> None: ...

class DeleteOfflineWideTableFeatureWatermarksRequest(_message.Message):
    __slots__ = ("namespace", "persistence_keys", "config_fingerprint", "feature_fqns")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_KEYS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FQNS_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    persistence_keys: _containers.RepeatedScalarFieldContainer[str]
    config_fingerprint: int
    feature_fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        persistence_keys: _Optional[_Iterable[str]] = ...,
        config_fingerprint: _Optional[int] = ...,
        feature_fqns: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class DeleteOfflineWideTableFeatureWatermarksResponse(_message.Message):
    __slots__ = ("watermarks_deleted",)
    WATERMARKS_DELETED_FIELD_NUMBER: _ClassVar[int]
    watermarks_deleted: int
    def __init__(self, watermarks_deleted: _Optional[int] = ...) -> None: ...
