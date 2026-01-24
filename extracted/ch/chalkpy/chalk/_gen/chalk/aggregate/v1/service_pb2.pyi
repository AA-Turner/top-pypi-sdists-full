from chalk._gen.chalk.aggregate.v1 import backfill_pb2 as _backfill_pb2
from chalk._gen.chalk.aggregate.v1 import timeseries_pb2 as _timeseries_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
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

class PlanAggregateBackfillRequest(_message.Message):
    __slots__ = ("params",)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _backfill_pb2.AggregateBackfillUserParams
    def __init__(
        self, params: _Optional[_Union[_backfill_pb2.AggregateBackfillUserParams, _Mapping]] = ...
    ) -> None: ...

class PlanAggregateBackfillResponse(_message.Message):
    __slots__ = ("estimate", "errors", "backfills", "aggregate_backfill_id")
    ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    BACKFILLS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BACKFILL_ID_FIELD_NUMBER: _ClassVar[int]
    estimate: _backfill_pb2.AggregateBackfillCostEstimate
    errors: _containers.RepeatedScalarFieldContainer[str]
    backfills: _containers.RepeatedCompositeFieldContainer[_backfill_pb2.AggregateBackfillWithCostEstimate]
    aggregate_backfill_id: str
    def __init__(
        self,
        estimate: _Optional[_Union[_backfill_pb2.AggregateBackfillCostEstimate, _Mapping]] = ...,
        errors: _Optional[_Iterable[str]] = ...,
        backfills: _Optional[_Iterable[_Union[_backfill_pb2.AggregateBackfillWithCostEstimate, _Mapping]]] = ...,
        aggregate_backfill_id: _Optional[str] = ...,
    ) -> None: ...

class GetAggregatesRequest(_message.Message):
    __slots__ = ("for_features",)
    FOR_FEATURES_FIELD_NUMBER: _ClassVar[int]
    for_features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, for_features: _Optional[_Iterable[str]] = ...) -> None: ...

class GetAggregatesResponse(_message.Message):
    __slots__ = ("series", "errors")
    SERIES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    series: _containers.RepeatedCompositeFieldContainer[_timeseries_pb2.AggregateTimeSeries]
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        series: _Optional[_Iterable[_Union[_timeseries_pb2.AggregateTimeSeries, _Mapping]]] = ...,
        errors: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetAggregateBackfillJobsRequest(_message.Message):
    __slots__ = ("limit", "cursor", "plan_hash")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    PLAN_HASH_FIELD_NUMBER: _ClassVar[int]
    limit: int
    cursor: str
    plan_hash: str
    def __init__(
        self, limit: _Optional[int] = ..., cursor: _Optional[str] = ..., plan_hash: _Optional[str] = ...
    ) -> None: ...

class GetAggregateBackfillJobsResponse(_message.Message):
    __slots__ = ("jobs", "cursor")
    JOBS_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[_backfill_pb2.AggregateBackfillJob]
    cursor: str
    def __init__(
        self,
        jobs: _Optional[_Iterable[_Union[_backfill_pb2.AggregateBackfillJob, _Mapping]]] = ...,
        cursor: _Optional[str] = ...,
    ) -> None: ...

class GetAggregateBackfillJobRequest(_message.Message):
    __slots__ = ("aggregate_backfill_id",)
    AGGREGATE_BACKFILL_ID_FIELD_NUMBER: _ClassVar[int]
    aggregate_backfill_id: str
    def __init__(self, aggregate_backfill_id: _Optional[str] = ...) -> None: ...

class GetAggregateBackfillJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: _backfill_pb2.AggregateBackfillJob
    def __init__(self, job: _Optional[_Union[_backfill_pb2.AggregateBackfillJob, _Mapping]] = ...) -> None: ...

class GetCronAggregateBackfillRequest(_message.Message):
    __slots__ = ("cron_aggregate_backfill_id", "plan_hash")
    CRON_AGGREGATE_BACKFILL_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_HASH_FIELD_NUMBER: _ClassVar[int]
    cron_aggregate_backfill_id: str
    plan_hash: str
    def __init__(self, cron_aggregate_backfill_id: _Optional[str] = ..., plan_hash: _Optional[str] = ...) -> None: ...

class GetCronAggregateBackfillResponse(_message.Message):
    __slots__ = ("cron_aggregate_backfill",)
    CRON_AGGREGATE_BACKFILL_FIELD_NUMBER: _ClassVar[int]
    cron_aggregate_backfill: _backfill_pb2.CronAggregateBackfill
    def __init__(
        self, cron_aggregate_backfill: _Optional[_Union[_backfill_pb2.CronAggregateBackfill, _Mapping]] = ...
    ) -> None: ...

class GetActiveCronAggregateBackfillsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CronAggregateBackfillWithLatestRun(_message.Message):
    __slots__ = ("cron_aggregate_backfill", "latest_job")
    CRON_AGGREGATE_BACKFILL_FIELD_NUMBER: _ClassVar[int]
    LATEST_JOB_FIELD_NUMBER: _ClassVar[int]
    cron_aggregate_backfill: _backfill_pb2.CronAggregateBackfill
    latest_job: _backfill_pb2.AggregateBackfillJob
    def __init__(
        self,
        cron_aggregate_backfill: _Optional[_Union[_backfill_pb2.CronAggregateBackfill, _Mapping]] = ...,
        latest_job: _Optional[_Union[_backfill_pb2.AggregateBackfillJob, _Mapping]] = ...,
    ) -> None: ...

class GetActiveCronAggregateBackfillsResponse(_message.Message):
    __slots__ = ("cron_aggregate_backfills",)
    CRON_AGGREGATE_BACKFILLS_FIELD_NUMBER: _ClassVar[int]
    cron_aggregate_backfills: _containers.RepeatedCompositeFieldContainer[CronAggregateBackfillWithLatestRun]
    def __init__(
        self, cron_aggregate_backfills: _Optional[_Iterable[_Union[CronAggregateBackfillWithLatestRun, _Mapping]]] = ...
    ) -> None: ...

class CreateAggregateBackfillJobRequest(_message.Message):
    __slots__ = (
        "features",
        "lower_bound",
        "upper_bound",
        "resolver",
        "bucket_feature",
        "enable_profiling",
        "aggregate_backfill_id",
        "resource_group",
    )
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FEATURE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BACKFILL_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedScalarFieldContainer[str]
    lower_bound: _timestamp_pb2.Timestamp
    upper_bound: _timestamp_pb2.Timestamp
    resolver: str
    bucket_feature: str
    enable_profiling: bool
    aggregate_backfill_id: str
    resource_group: str
    def __init__(
        self,
        features: _Optional[_Iterable[str]] = ...,
        lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        resolver: _Optional[str] = ...,
        bucket_feature: _Optional[str] = ...,
        enable_profiling: bool = ...,
        aggregate_backfill_id: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
    ) -> None: ...

class CreateAggregateBackfillJobResponse(_message.Message):
    __slots__ = ("job_id", "features", "errors")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    features: _containers.RepeatedScalarFieldContainer[str]
    errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        job_id: _Optional[str] = ...,
        features: _Optional[_Iterable[str]] = ...,
        errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...
