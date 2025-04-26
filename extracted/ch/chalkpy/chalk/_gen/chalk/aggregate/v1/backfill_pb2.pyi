from chalk._gen.chalk.aggregate.v1 import timeseries_pb2 as _timeseries_pb2
from google.protobuf import duration_pb2 as _duration_pb2
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

class AggregateBackfillCostEstimate(_message.Message):
    __slots__ = ("max_buckets", "expected_buckets", "expected_bytes", "expected_storage_cost", "expected_runtime")
    MAX_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_BYTES_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_STORAGE_COST_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_RUNTIME_FIELD_NUMBER: _ClassVar[int]
    max_buckets: int
    expected_buckets: int
    expected_bytes: int
    expected_storage_cost: float
    expected_runtime: _duration_pb2.Duration
    def __init__(
        self,
        max_buckets: _Optional[int] = ...,
        expected_buckets: _Optional[int] = ...,
        expected_bytes: _Optional[int] = ...,
        expected_storage_cost: _Optional[float] = ...,
        expected_runtime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class AggregateBackfillUserParams(_message.Message):
    __slots__ = ("features", "resolver", "timestamp_column_name", "lower_bound", "upper_bound", "exact")
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    EXACT_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedScalarFieldContainer[str]
    resolver: str
    timestamp_column_name: str
    lower_bound: _timestamp_pb2.Timestamp
    upper_bound: _timestamp_pb2.Timestamp
    exact: bool
    def __init__(
        self,
        features: _Optional[_Iterable[str]] = ...,
        resolver: _Optional[str] = ...,
        timestamp_column_name: _Optional[str] = ...,
        lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        exact: bool = ...,
    ) -> None: ...

class AggregateBackfill(_message.Message):
    __slots__ = (
        "series",
        "resolver",
        "datetime_feature",
        "bucket_duration",
        "filters_description",
        "group_by",
        "max_retention",
        "lower_bound",
        "upper_bound",
    )
    SERIES_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    DATETIME_FEATURE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_FIELD_NUMBER: _ClassVar[int]
    FILTERS_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    MAX_RETENTION_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_FIELD_NUMBER: _ClassVar[int]
    series: _containers.RepeatedCompositeFieldContainer[_timeseries_pb2.AggregateTimeSeries]
    resolver: str
    datetime_feature: str
    bucket_duration: _duration_pb2.Duration
    filters_description: str
    group_by: _containers.RepeatedScalarFieldContainer[str]
    max_retention: _duration_pb2.Duration
    lower_bound: _timestamp_pb2.Timestamp
    upper_bound: _timestamp_pb2.Timestamp
    def __init__(
        self,
        series: _Optional[_Iterable[_Union[_timeseries_pb2.AggregateTimeSeries, _Mapping]]] = ...,
        resolver: _Optional[str] = ...,
        datetime_feature: _Optional[str] = ...,
        bucket_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        filters_description: _Optional[str] = ...,
        group_by: _Optional[_Iterable[str]] = ...,
        max_retention: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        lower_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class AggregateBackfillWithCostEstimate(_message.Message):
    __slots__ = ("backfill", "estimate")
    BACKFILL_FIELD_NUMBER: _ClassVar[int]
    ESTIMATE_FIELD_NUMBER: _ClassVar[int]
    backfill: AggregateBackfill
    estimate: AggregateBackfillCostEstimate
    def __init__(
        self,
        backfill: _Optional[_Union[AggregateBackfill, _Mapping]] = ...,
        estimate: _Optional[_Union[AggregateBackfillCostEstimate, _Mapping]] = ...,
    ) -> None: ...

class AggregateBackfillJob(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "resolver",
        "features",
        "agent_id",
        "deployment_id",
        "created_at",
        "updated_at",
        "resolvers",
        "cron_aggregate_backfill_id",
        "plan_hash",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    CRON_AGGREGATE_BACKFILL_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_HASH_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    resolver: str
    features: _containers.RepeatedScalarFieldContainer[str]
    agent_id: str
    deployment_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    resolvers: _containers.RepeatedScalarFieldContainer[str]
    cron_aggregate_backfill_id: str
    plan_hash: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        resolver: _Optional[str] = ...,
        features: _Optional[_Iterable[str]] = ...,
        agent_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        resolvers: _Optional[_Iterable[str]] = ...,
        cron_aggregate_backfill_id: _Optional[str] = ...,
        plan_hash: _Optional[str] = ...,
    ) -> None: ...

class CronAggregateBackfill(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "deployment_id",
        "schedule",
        "plan_hash",
        "features",
        "resolvers",
        "created_at",
        "updated_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    PLAN_HASH_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    deployment_id: str
    schedule: str
    plan_hash: str
    features: _containers.RepeatedScalarFieldContainer[str]
    resolvers: _containers.RepeatedScalarFieldContainer[str]
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        schedule: _Optional[str] = ...,
        plan_hash: _Optional[str] = ...,
        features: _Optional[_Iterable[str]] = ...,
        resolvers: _Optional[_Iterable[str]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...
