from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import batch_pb2 as _batch_pb2
from chalk._gen.chalk.server.v1 import scheduled_query_run_pb2 as _scheduled_query_run_pb2
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
    ) -> None: ...

class ManualTriggerCronResolverRequest(_message.Message):
    __slots__ = ("resolver_fqn", "max_samples", "lower_bound", "upper_bound", "timestamping_mode", "job_options")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    MAX_SAMPLES_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMPING_MODE_FIELD_NUMBER: _ClassVar[int]
    JOB_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    max_samples: int
    lower_bound: _timestamp_pb2.Timestamp
    upper_bound: _timestamp_pb2.Timestamp
    timestamping_mode: str
    job_options: str
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        max_samples: _Optional[int] = ...,
        lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        timestamping_mode: _Optional[str] = ...,
        job_options: _Optional[str] = ...,
    ) -> None: ...

class ManualTriggerCronResolverResponse(_message.Message):
    __slots__ = ("cron_resolver_run",)
    CRON_RESOLVER_RUN_FIELD_NUMBER: _ClassVar[int]
    cron_resolver_run: CronResolverRun
    def __init__(self, cron_resolver_run: _Optional[_Union[CronResolverRun, _Mapping]] = ...) -> None: ...

class ManualTriggerScheduledQueryRequest(_message.Message):
    __slots__ = ("cron_query_id", "planner_options", "incremental_resolvers", "max_samples", "env_overrides")
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
    cron_query_id: int
    planner_options: _containers.MessageMap[str, _struct_pb2.Value]
    incremental_resolvers: _containers.RepeatedScalarFieldContainer[str]
    max_samples: int
    env_overrides: _containers.ScalarMap[str, str]
    def __init__(
        self,
        cron_query_id: _Optional[int] = ...,
        planner_options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        incremental_resolvers: _Optional[_Iterable[str]] = ...,
        max_samples: _Optional[int] = ...,
        env_overrides: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ManualTriggerScheduledQueryResponse(_message.Message):
    __slots__ = ("scheduled_query_run",)
    SCHEDULED_QUERY_RUN_FIELD_NUMBER: _ClassVar[int]
    scheduled_query_run: _scheduled_query_run_pb2.ScheduledQueryRun
    def __init__(
        self, scheduled_query_run: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryRun, _Mapping]] = ...
    ) -> None: ...
