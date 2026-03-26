from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import offline_query_pb2 as _offline_query_pb2
from chalk._gen.chalk.server.v1 import batch_pb2 as _batch_pb2
from chalk._gen.chalk.server.v1 import scheduled_query_run_pb2 as _scheduled_query_run_pb2
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

class CronRunTriggerKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CRON_RUN_TRIGGER_KIND_UNSPECIFIED: _ClassVar[CronRunTriggerKind]
    CRON_RUN_TRIGGER_KIND_MANUAL: _ClassVar[CronRunTriggerKind]
    CRON_RUN_TRIGGER_KIND_API: _ClassVar[CronRunTriggerKind]
    CRON_RUN_TRIGGER_KIND_CRON: _ClassVar[CronRunTriggerKind]

CRON_RUN_TRIGGER_KIND_UNSPECIFIED: CronRunTriggerKind
CRON_RUN_TRIGGER_KIND_MANUAL: CronRunTriggerKind
CRON_RUN_TRIGGER_KIND_API: CronRunTriggerKind
CRON_RUN_TRIGGER_KIND_CRON: CronRunTriggerKind

class CronResolverRun(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "resolver_fqn",
        "kind",
        "schedule_readable",
        "schedule_resolver_value",
        "created_at",
        "deployment_id",
        "end",
        "batch",
        "trigger_kind",
        "lower_bound",
        "upper_bound",
        "max_samples",
        "used_job_queue",
        "gcr_execution_id",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_READABLE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_RESOLVER_VALUE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    BATCH_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_KIND_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    MAX_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    USED_JOB_QUEUE_FIELD_NUMBER: _ClassVar[int]
    GCR_EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    resolver_fqn: str
    kind: str
    schedule_readable: str
    schedule_resolver_value: str
    created_at: _timestamp_pb2.Timestamp
    deployment_id: str
    end: _timestamp_pb2.Timestamp
    batch: _batch_pb2.BatchOperation
    trigger_kind: CronRunTriggerKind
    lower_bound: _timestamp_pb2.Timestamp
    upper_bound: _timestamp_pb2.Timestamp
    max_samples: int
    used_job_queue: bool
    gcr_execution_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        schedule_readable: _Optional[str] = ...,
        schedule_resolver_value: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        deployment_id: _Optional[str] = ...,
        end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        batch: _Optional[_Union[_batch_pb2.BatchOperation, _Mapping]] = ...,
        trigger_kind: _Optional[_Union[CronRunTriggerKind, str]] = ...,
        lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        max_samples: _Optional[int] = ...,
        used_job_queue: bool = ...,
        gcr_execution_id: _Optional[str] = ...,
    ) -> None: ...

class ManualTriggerCronResolverRequest(_message.Message):
    __slots__ = (
        "resolver_fqn",
        "max_samples",
        "lower_bound",
        "upper_bound",
        "persistence_settings",
        "timestamping_mode",
        "job_options",
        "idempotency_key",
        "override_target_image_tag",
    )
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    MAX_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPING_MODE_FIELD_NUMBER: _ClassVar[int]
    JOB_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_KEY_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_TARGET_IMAGE_TAG_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    max_samples: int
    lower_bound: _timestamp_pb2.Timestamp
    upper_bound: _timestamp_pb2.Timestamp
    persistence_settings: _offline_query_pb2.PersistenceSettings
    timestamping_mode: str
    job_options: str
    idempotency_key: str
    override_target_image_tag: str
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        max_samples: _Optional[int] = ...,
        lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        persistence_settings: _Optional[_Union[_offline_query_pb2.PersistenceSettings, _Mapping]] = ...,
        timestamping_mode: _Optional[str] = ...,
        job_options: _Optional[str] = ...,
        idempotency_key: _Optional[str] = ...,
        override_target_image_tag: _Optional[str] = ...,
    ) -> None: ...

class ManualTriggerCronResolverResponse(_message.Message):
    __slots__ = ("cron_resolver_run", "progress_url")
    CRON_RESOLVER_RUN_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_URL_FIELD_NUMBER: _ClassVar[int]
    cron_resolver_run: CronResolverRun
    progress_url: str
    def __init__(
        self, cron_resolver_run: _Optional[_Union[CronResolverRun, _Mapping]] = ..., progress_url: _Optional[str] = ...
    ) -> None: ...

class ManualTriggerScheduledQueryRequest(_message.Message):
    __slots__ = (
        "cron_query_id",
        "planner_options",
        "incremental_resolvers",
        "max_samples",
        "env_overrides",
        "cron_query_name",
        "store_plan_stages",
        "unload_resolvers",
    )
    class PlannerOptionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    class EnvOverridesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    PLANNER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    INCREMENTAL_RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    MAX_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    ENV_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    CRON_QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    STORE_PLAN_STAGES_FIELD_NUMBER: _ClassVar[int]
    UNLOAD_RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    cron_query_id: int
    planner_options: _containers.MessageMap[str, _struct_pb2.Value]
    incremental_resolvers: _containers.RepeatedScalarFieldContainer[str]
    max_samples: int
    env_overrides: _containers.ScalarMap[str, str]
    cron_query_name: str
    store_plan_stages: bool
    unload_resolvers: _containers.RepeatedCompositeFieldContainer[_offline_query_pb2.UnloadResolverSpec]
    def __init__(
        self,
        cron_query_id: _Optional[int] = ...,
        planner_options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        incremental_resolvers: _Optional[_Iterable[str]] = ...,
        max_samples: _Optional[int] = ...,
        env_overrides: _Optional[_Mapping[str, str]] = ...,
        cron_query_name: _Optional[str] = ...,
        store_plan_stages: bool = ...,
        unload_resolvers: _Optional[_Iterable[_Union[_offline_query_pb2.UnloadResolverSpec, _Mapping]]] = ...,
    ) -> None: ...

class ManualTriggerScheduledQueryResponse(_message.Message):
    __slots__ = ("scheduled_query_run",)
    SCHEDULED_QUERY_RUN_FIELD_NUMBER: _ClassVar[int]
    scheduled_query_run: _scheduled_query_run_pb2.ScheduledQueryRun
    def __init__(
        self, scheduled_query_run: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryRun, _Mapping]] = ...
    ) -> None: ...

class GetScheduledResolverRunRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetScheduledResolverRunResponse(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: CronResolverRun
    def __init__(self, run: _Optional[_Union[CronResolverRun, _Mapping]] = ...) -> None: ...

class ListScheduledResolverRunsRequest(_message.Message):
    __slots__ = ("cursor", "limit", "page_token", "resolver_filter", "resolver_fqn", "status_filter", "start", "end")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FILTER_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FILTER_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    cursor: _timestamp_pb2.Timestamp
    limit: int
    page_token: str
    resolver_filter: str
    resolver_fqn: str
    status_filter: _batch_pb2.OperationStatus
    start: _timestamp_pb2.Timestamp
    end: _timestamp_pb2.Timestamp
    def __init__(
        self,
        cursor: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
        resolver_filter: _Optional[str] = ...,
        resolver_fqn: _Optional[str] = ...,
        status_filter: _Optional[_Union[_batch_pb2.OperationStatus, str]] = ...,
        start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListScheduledResolverRunsResponse(_message.Message):
    __slots__ = ("runs", "next_page_token")
    RUNS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    runs: _containers.RepeatedCompositeFieldContainer[CronResolverRun]
    next_page_token: str
    def __init__(
        self, runs: _Optional[_Iterable[_Union[CronResolverRun, _Mapping]]] = ..., next_page_token: _Optional[str] = ...
    ) -> None: ...

class CancelScheduledResolverRunRequest(_message.Message):
    __slots__ = ("run_id",)
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    def __init__(self, run_id: _Optional[str] = ...) -> None: ...

class CancelScheduledResolverRunResponse(_message.Message):
    __slots__ = ("cron_run",)
    CRON_RUN_FIELD_NUMBER: _ClassVar[int]
    cron_run: CronResolverRun
    def __init__(self, cron_run: _Optional[_Union[CronResolverRun, _Mapping]] = ...) -> None: ...

class GetActiveScheduledResolversRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ScheduledResolverRunInfo(_message.Message):
    __slots__ = ("id", "status", "resolvers")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: _batch_pb2.OperationStatus
    resolvers: _containers.RepeatedCompositeFieldContainer[_batch_pb2.ResolverOperation]
    def __init__(
        self,
        id: _Optional[str] = ...,
        status: _Optional[_Union[_batch_pb2.OperationStatus, str]] = ...,
        resolvers: _Optional[_Iterable[_Union[_batch_pb2.ResolverOperation, _Mapping]]] = ...,
    ) -> None: ...

class ScheduledResolverInfo(_message.Message):
    __slots__ = ("resolver_fqn", "cron", "control", "latest_run")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    CRON_FIELD_NUMBER: _ClassVar[int]
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    LATEST_RUN_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    cron: str
    control: ScheduledResolverControl
    latest_run: ScheduledResolverRunInfo
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        cron: _Optional[str] = ...,
        control: _Optional[_Union[ScheduledResolverControl, _Mapping]] = ...,
        latest_run: _Optional[_Union[ScheduledResolverRunInfo, _Mapping]] = ...,
    ) -> None: ...

class GetActiveScheduledResolversResponse(_message.Message):
    __slots__ = ("scheduled_resolvers",)
    SCHEDULED_RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    scheduled_resolvers: _containers.RepeatedCompositeFieldContainer[ScheduledResolverInfo]
    def __init__(
        self, scheduled_resolvers: _Optional[_Iterable[_Union[ScheduledResolverInfo, _Mapping]]] = ...
    ) -> None: ...

class GetScheduledResolverControlRequest(_message.Message):
    __slots__ = ("resolver_fqn",)
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    def __init__(self, resolver_fqn: _Optional[str] = ...) -> None: ...

class ScheduledResolverControl(_message.Message):
    __slots__ = ("resolver_fqn", "status", "agent_id", "created_at", "updated_at", "job_config")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    JOB_CONFIG_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    status: _scheduled_query_run_pb2.CronControlStatus
    agent_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    job_config: str
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        status: _Optional[_Union[_scheduled_query_run_pb2.CronControlStatus, str]] = ...,
        agent_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        job_config: _Optional[str] = ...,
    ) -> None: ...

class GetScheduledResolverControlResponse(_message.Message):
    __slots__ = ("control",)
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    control: ScheduledResolverControl
    def __init__(self, control: _Optional[_Union[ScheduledResolverControl, _Mapping]] = ...) -> None: ...

class UpdateScheduledResolverControlOperation(_message.Message):
    __slots__ = ("status", "job_config")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    JOB_CONFIG_FIELD_NUMBER: _ClassVar[int]
    status: _scheduled_query_run_pb2.CronControlStatus
    job_config: str
    def __init__(
        self,
        status: _Optional[_Union[_scheduled_query_run_pb2.CronControlStatus, str]] = ...,
        job_config: _Optional[str] = ...,
    ) -> None: ...

class UpdateScheduledResolverControlRequest(_message.Message):
    __slots__ = ("resolver_fqn", "update", "update_mask")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    update: UpdateScheduledResolverControlOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        update: _Optional[_Union[UpdateScheduledResolverControlOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateScheduledResolverControlResponse(_message.Message):
    __slots__ = ("control",)
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    control: ScheduledResolverControl
    def __init__(self, control: _Optional[_Union[ScheduledResolverControl, _Mapping]] = ...) -> None: ...

class GetLatestHighWaterMarkRequest(_message.Message):
    __slots__ = ("resolver_fqn",)
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    def __init__(self, resolver_fqn: _Optional[str] = ...) -> None: ...

class HighWaterMark(_message.Message):
    __slots__ = ("id", "resolver_fqn", "max_ingested_timestamp", "last_execution_timestamp", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    MAX_INGESTED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_EXECUTION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    resolver_fqn: str
    max_ingested_timestamp: _timestamp_pb2.Timestamp
    last_execution_timestamp: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[int] = ...,
        resolver_fqn: _Optional[str] = ...,
        max_ingested_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        last_execution_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetLatestHighWaterMarkResponse(_message.Message):
    __slots__ = ("high_water_mark",)
    HIGH_WATER_MARK_FIELD_NUMBER: _ClassVar[int]
    high_water_mark: HighWaterMark
    def __init__(self, high_water_mark: _Optional[_Union[HighWaterMark, _Mapping]] = ...) -> None: ...
