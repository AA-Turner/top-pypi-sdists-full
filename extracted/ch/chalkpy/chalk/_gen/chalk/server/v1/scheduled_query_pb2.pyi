from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import scheduled_query_run_pb2 as _scheduled_query_run_pb2
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

class GetActiveScheduledQueriesRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class ScheduledQueryRunInfo(_message.Message):
    __slots__ = ("id", "offline_query_id", "workflow_execution_id", "status", "has_errors")
    ID_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HAS_ERRORS_FIELD_NUMBER: _ClassVar[int]
    id: int
    offline_query_id: str
    workflow_execution_id: str
    status: _scheduled_query_run_pb2.ScheduledQueryRunStatus
    has_errors: bool
    def __init__(
        self,
        id: _Optional[int] = ...,
        offline_query_id: _Optional[str] = ...,
        workflow_execution_id: _Optional[str] = ...,
        status: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryRunStatus, str]] = ...,
        has_errors: bool = ...,
    ) -> None: ...

class ScheduledQueryInfo(_message.Message):
    __slots__ = ("schedule", "control", "latest_run")
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    LATEST_RUN_FIELD_NUMBER: _ClassVar[int]
    schedule: _scheduled_query_run_pb2.ScheduledQuerySchedule
    control: _scheduled_query_run_pb2.ScheduledQueryControl
    latest_run: ScheduledQueryRunInfo
    def __init__(
        self,
        schedule: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQuerySchedule, _Mapping]] = ...,
        control: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryControl, _Mapping]] = ...,
        latest_run: _Optional[_Union[ScheduledQueryRunInfo, _Mapping]] = ...,
    ) -> None: ...

class GetActiveScheduledQueriesResponse(_message.Message):
    __slots__ = ("scheduled_queries",)
    SCHEDULED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    scheduled_queries: _containers.RepeatedCompositeFieldContainer[ScheduledQueryInfo]
    def __init__(self, scheduled_queries: _Optional[_Iterable[_Union[ScheduledQueryInfo, _Mapping]]] = ...) -> None: ...

class GetScheduledQueryControlRequest(_message.Message):
    __slots__ = ("cron_query_id", "cron_query_name")
    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    CRON_QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    cron_query_id: int
    cron_query_name: str
    def __init__(self, cron_query_id: _Optional[int] = ..., cron_query_name: _Optional[str] = ...) -> None: ...

class GetScheduledQueryControlResponse(_message.Message):
    __slots__ = ("control",)
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    control: _scheduled_query_run_pb2.ScheduledQueryControl
    def __init__(
        self, control: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryControl, _Mapping]] = ...
    ) -> None: ...

class UpdateScheduledQueryControlOperation(_message.Message):
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

class UpdateScheduledQueryControlRequest(_message.Message):
    __slots__ = ("cron_query_id", "update", "update_mask")
    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    cron_query_id: int
    update: UpdateScheduledQueryControlOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        cron_query_id: _Optional[int] = ...,
        update: _Optional[_Union[UpdateScheduledQueryControlOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateScheduledQueryControlResponse(_message.Message):
    __slots__ = ("control",)
    CONTROL_FIELD_NUMBER: _ClassVar[int]
    control: _scheduled_query_run_pb2.ScheduledQueryControl
    def __init__(
        self, control: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQueryControl, _Mapping]] = ...
    ) -> None: ...

class GetScheduledQueryScheduleRequest(_message.Message):
    __slots__ = ("schedule_id", "cron_query_id")
    SCHEDULE_ID_FIELD_NUMBER: _ClassVar[int]
    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    schedule_id: int
    cron_query_id: int
    def __init__(self, schedule_id: _Optional[int] = ..., cron_query_id: _Optional[int] = ...) -> None: ...

class GetScheduledQueryScheduleResponse(_message.Message):
    __slots__ = ("schedule",)
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    schedule: _scheduled_query_run_pb2.ScheduledQuerySchedule
    def __init__(
        self, schedule: _Optional[_Union[_scheduled_query_run_pb2.ScheduledQuerySchedule, _Mapping]] = ...
    ) -> None: ...

class GetScheduledQueryFeatureStatisticsRequest(_message.Message):
    __slots__ = ("cron_query_id", "cron_query_name", "start_time", "end_time", "max_runs")
    CRON_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    CRON_QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_RUNS_FIELD_NUMBER: _ClassVar[int]
    cron_query_id: int
    cron_query_name: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    max_runs: int
    def __init__(
        self,
        cron_query_id: _Optional[int] = ...,
        cron_query_name: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        max_runs: _Optional[int] = ...,
    ) -> None: ...

class ScheduledQueryFeatureStatistics(_message.Message):
    __slots__ = ("feature_fqn", "count", "null_count", "zero_count", "mean", "max", "min")
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    NULL_COUNT_FIELD_NUMBER: _ClassVar[int]
    ZERO_COUNT_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    feature_fqn: str
    count: int
    null_count: int
    zero_count: int
    mean: float
    max: float
    min: float
    def __init__(
        self,
        feature_fqn: _Optional[str] = ...,
        count: _Optional[int] = ...,
        null_count: _Optional[int] = ...,
        zero_count: _Optional[int] = ...,
        mean: _Optional[float] = ...,
        max: _Optional[float] = ...,
        min: _Optional[float] = ...,
    ) -> None: ...

class ScheduledQueryRunFeatureStatistics(_message.Message):
    __slots__ = ("scheduled_query_run_id", "operation_id", "run_started_at", "statistics")
    SCHEDULED_QUERY_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    RUN_STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    STATISTICS_FIELD_NUMBER: _ClassVar[int]
    scheduled_query_run_id: int
    operation_id: str
    run_started_at: _timestamp_pb2.Timestamp
    statistics: _containers.RepeatedCompositeFieldContainer[ScheduledQueryFeatureStatistics]
    def __init__(
        self,
        scheduled_query_run_id: _Optional[int] = ...,
        operation_id: _Optional[str] = ...,
        run_started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        statistics: _Optional[_Iterable[_Union[ScheduledQueryFeatureStatistics, _Mapping]]] = ...,
    ) -> None: ...

class GetScheduledQueryFeatureStatisticsResponse(_message.Message):
    __slots__ = ("runs", "warnings")
    RUNS_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    runs: _containers.RepeatedCompositeFieldContainer[ScheduledQueryRunFeatureStatistics]
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        runs: _Optional[_Iterable[_Union[ScheduledQueryRunFeatureStatistics, _Mapping]]] = ...,
        warnings: _Optional[_Iterable[str]] = ...,
    ) -> None: ...
