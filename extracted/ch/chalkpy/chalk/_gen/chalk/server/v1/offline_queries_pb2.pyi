from chalk._gen.chalk.aggregate.v1 import service_pb2 as _service_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.common.v1 import chalk_error_pb2 as _chalk_error_pb2
from chalk._gen.chalk.common.v1 import dataset_response_pb2 as _dataset_response_pb2
from chalk._gen.chalk.common.v1 import offline_query_pb2 as _offline_query_pb2
from chalk._gen.chalk.server.v1 import datasets_pb2 as _datasets_pb2
from chalk._gen.chalk.server.v1 import performance_summary_pb2 as _performance_summary_pb2
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

class OfflineQueryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE_QUERY_STATUS_UNSPECIFIED: _ClassVar[OfflineQueryStatus]
    OFFLINE_QUERY_STATUS_UNKNOWN: _ClassVar[OfflineQueryStatus]
    OFFLINE_QUERY_STATUS_WORKING: _ClassVar[OfflineQueryStatus]
    OFFLINE_QUERY_STATUS_FAILED: _ClassVar[OfflineQueryStatus]
    OFFLINE_QUERY_STATUS_COMPLETED: _ClassVar[OfflineQueryStatus]
    OFFLINE_QUERY_STATUS_CANCELED: _ClassVar[OfflineQueryStatus]
    OFFLINE_QUERY_STATUS_QUEUED: _ClassVar[OfflineQueryStatus]

class OfflineQueryKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE_QUERY_KIND_UNSPECIFIED: _ClassVar[OfflineQueryKind]
    OFFLINE_QUERY_KIND_UNKNOWN: _ClassVar[OfflineQueryKind]
    OFFLINE_QUERY_KIND_ASYNC_OFFLINE_QUERY: _ClassVar[OfflineQueryKind]
    OFFLINE_QUERY_KIND_CRON_OFFLINE_QUERY: _ClassVar[OfflineQueryKind]
    OFFLINE_QUERY_KIND_OFFLINE_QUERY: _ClassVar[OfflineQueryKind]
    OFFLINE_QUERY_KIND_DATASET_INGESTION: _ClassVar[OfflineQueryKind]
    OFFLINE_QUERY_KIND_AGGREGATION_BACKFILL: _ClassVar[OfflineQueryKind]
    OFFLINE_QUERY_KIND_TRAINING_JOB: _ClassVar[OfflineQueryKind]

class BatchOpStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATCH_OP_STATUS_UNSPECIFIED: _ClassVar[BatchOpStatus]
    BATCH_OP_STATUS_INIT: _ClassVar[BatchOpStatus]
    BATCH_OP_STATUS_COMPUTE_STARTED: _ClassVar[BatchOpStatus]
    BATCH_OP_STATUS_COMPUTE_ENDED: _ClassVar[BatchOpStatus]
    BATCH_OP_STATUS_COMPLETED: _ClassVar[BatchOpStatus]
    BATCH_OP_STATUS_FAILED: _ClassVar[BatchOpStatus]

class BatchOpKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BATCH_OP_KIND_UNSPECIFIED: _ClassVar[BatchOpKind]
    BATCH_OP_KIND_OFFLINE_QUERY: _ClassVar[BatchOpKind]
    BATCH_OP_KIND_RECOMPUTE: _ClassVar[BatchOpKind]
    BATCH_OP_KIND_CRON: _ClassVar[BatchOpKind]
    BATCH_OP_KIND_AGGREGATION_BACKFILL: _ClassVar[BatchOpKind]

OFFLINE_QUERY_STATUS_UNSPECIFIED: OfflineQueryStatus
OFFLINE_QUERY_STATUS_UNKNOWN: OfflineQueryStatus
OFFLINE_QUERY_STATUS_WORKING: OfflineQueryStatus
OFFLINE_QUERY_STATUS_FAILED: OfflineQueryStatus
OFFLINE_QUERY_STATUS_COMPLETED: OfflineQueryStatus
OFFLINE_QUERY_STATUS_CANCELED: OfflineQueryStatus
OFFLINE_QUERY_STATUS_QUEUED: OfflineQueryStatus
OFFLINE_QUERY_KIND_UNSPECIFIED: OfflineQueryKind
OFFLINE_QUERY_KIND_UNKNOWN: OfflineQueryKind
OFFLINE_QUERY_KIND_ASYNC_OFFLINE_QUERY: OfflineQueryKind
OFFLINE_QUERY_KIND_CRON_OFFLINE_QUERY: OfflineQueryKind
OFFLINE_QUERY_KIND_OFFLINE_QUERY: OfflineQueryKind
OFFLINE_QUERY_KIND_DATASET_INGESTION: OfflineQueryKind
OFFLINE_QUERY_KIND_AGGREGATION_BACKFILL: OfflineQueryKind
OFFLINE_QUERY_KIND_TRAINING_JOB: OfflineQueryKind
BATCH_OP_STATUS_UNSPECIFIED: BatchOpStatus
BATCH_OP_STATUS_INIT: BatchOpStatus
BATCH_OP_STATUS_COMPUTE_STARTED: BatchOpStatus
BATCH_OP_STATUS_COMPUTE_ENDED: BatchOpStatus
BATCH_OP_STATUS_COMPLETED: BatchOpStatus
BATCH_OP_STATUS_FAILED: BatchOpStatus
BATCH_OP_KIND_UNSPECIFIED: BatchOpKind
BATCH_OP_KIND_OFFLINE_QUERY: BatchOpKind
BATCH_OP_KIND_RECOMPUTE: BatchOpKind
BATCH_OP_KIND_CRON: BatchOpKind
BATCH_OP_KIND_AGGREGATION_BACKFILL: BatchOpKind

class OfflineQueryShardRun(_message.Message):
    __slots__ = ("id", "offline_query_id", "shard_id", "created_at", "hostname", "plan_execution_start", "completed_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    PLAN_EXECUTION_START_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    offline_query_id: str
    shard_id: int
    created_at: _timestamp_pb2.Timestamp
    hostname: str
    plan_execution_start: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[int] = ...,
        offline_query_id: _Optional[str] = ...,
        shard_id: _Optional[int] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        hostname: _Optional[str] = ...,
        plan_execution_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class OfflineQueryShard(_message.Message):
    __slots__ = (
        "id",
        "offline_query_id",
        "environment_id",
        "deployment_id",
        "created_at",
        "shard_id",
        "computer_id",
        "spine_uri",
        "spine_uri_version",
        "has_errors",
        "completed_at",
        "status",
        "last_heartbeat_at",
        "runs",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    COMPUTER_ID_FIELD_NUMBER: _ClassVar[int]
    SPINE_URI_FIELD_NUMBER: _ClassVar[int]
    SPINE_URI_VERSION_FIELD_NUMBER: _ClassVar[int]
    HAS_ERRORS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LAST_HEARTBEAT_AT_FIELD_NUMBER: _ClassVar[int]
    RUNS_FIELD_NUMBER: _ClassVar[int]
    id: int
    offline_query_id: str
    environment_id: str
    deployment_id: str
    created_at: _timestamp_pb2.Timestamp
    shard_id: int
    computer_id: int
    spine_uri: str
    spine_uri_version: int
    has_errors: bool
    completed_at: _timestamp_pb2.Timestamp
    status: OfflineQueryStatus
    last_heartbeat_at: _timestamp_pb2.Timestamp
    runs: _containers.RepeatedCompositeFieldContainer[OfflineQueryShardRun]
    def __init__(
        self,
        id: _Optional[int] = ...,
        offline_query_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        shard_id: _Optional[int] = ...,
        computer_id: _Optional[int] = ...,
        spine_uri: _Optional[str] = ...,
        spine_uri_version: _Optional[int] = ...,
        has_errors: bool = ...,
        completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        status: _Optional[_Union[OfflineQueryStatus, str]] = ...,
        last_heartbeat_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        runs: _Optional[_Iterable[_Union[OfflineQueryShardRun, _Mapping]]] = ...,
    ) -> None: ...

class OfflineQueryMeta(_message.Message):
    __slots__ = (
        "id",
        "operation_id",
        "environment_id",
        "deployment_id",
        "created_at",
        "query_meta",
        "query_plan_id",
        "branch_name",
        "dataset_id",
        "dataset_name",
        "has_errors",
        "agent_id",
        "trace_id",
        "correlation_id",
        "completed_at",
        "status",
        "has_plan_stages",
        "total_computers",
        "num_completed_computers",
        "total_partitions",
        "num_completed_partitions",
        "recompute_features",
        "spine_sql_query",
        "filters",
        "planner_options",
        "invoker_options",
        "query_type",
        "tags",
        "required_resolver_tags",
        "aggregate_backfill_id",
        "output",
        "required_output",
        "raw_body_filename",
        "dataset_revision",
        "time_series",
        "evaluation_run_id",
        "query_name",
        "query_name_version",
        "job_queue_stats",
        "resource_group",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    QUERY_META_FIELD_NUMBER: _ClassVar[int]
    QUERY_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_NAME_FIELD_NUMBER: _ClassVar[int]
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_NAME_FIELD_NUMBER: _ClassVar[int]
    HAS_ERRORS_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    HAS_PLAN_STAGES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COMPUTERS_FIELD_NUMBER: _ClassVar[int]
    NUM_COMPLETED_COMPUTERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    NUM_COMPLETED_PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    RECOMPUTE_FEATURES_FIELD_NUMBER: _ClassVar[int]
    SPINE_SQL_QUERY_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    PLANNER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    INVOKER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    QUERY_TYPE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_RESOLVER_TAGS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_BACKFILL_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    RAW_BODY_FILENAME_FIELD_NUMBER: _ClassVar[int]
    DATASET_REVISION_FIELD_NUMBER: _ClassVar[int]
    TIME_SERIES_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_RUN_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_VERSION_FIELD_NUMBER: _ClassVar[int]
    JOB_QUEUE_STATS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    id: int
    operation_id: str
    environment_id: str
    deployment_id: str
    created_at: _timestamp_pb2.Timestamp
    query_meta: _struct_pb2.Value
    query_plan_id: str
    branch_name: str
    dataset_id: str
    dataset_name: str
    has_errors: bool
    agent_id: str
    trace_id: str
    correlation_id: str
    completed_at: _timestamp_pb2.Timestamp
    status: OfflineQueryStatus
    has_plan_stages: bool
    total_computers: int
    num_completed_computers: int
    total_partitions: int
    num_completed_partitions: int
    recompute_features: str
    spine_sql_query: str
    filters: _struct_pb2.Value
    planner_options: _struct_pb2.Value
    invoker_options: _struct_pb2.Value
    query_type: OfflineQueryKind
    tags: _containers.RepeatedScalarFieldContainer[str]
    required_resolver_tags: _containers.RepeatedScalarFieldContainer[str]
    aggregate_backfill_id: str
    output: _struct_pb2.Value
    required_output: _struct_pb2.Value
    raw_body_filename: str
    dataset_revision: _datasets_pb2.DatasetRevisionMeta
    time_series: _containers.RepeatedCompositeFieldContainer[_service_pb2.PlanAggregateBackfillResponse]
    evaluation_run_id: str
    query_name: str
    query_name_version: str
    job_queue_stats: OfflineQueryJobQueueStats
    resource_group: str
    def __init__(
        self,
        id: _Optional[int] = ...,
        operation_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        query_meta: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        query_plan_id: _Optional[str] = ...,
        branch_name: _Optional[str] = ...,
        dataset_id: _Optional[str] = ...,
        dataset_name: _Optional[str] = ...,
        has_errors: bool = ...,
        agent_id: _Optional[str] = ...,
        trace_id: _Optional[str] = ...,
        correlation_id: _Optional[str] = ...,
        completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        status: _Optional[_Union[OfflineQueryStatus, str]] = ...,
        has_plan_stages: bool = ...,
        total_computers: _Optional[int] = ...,
        num_completed_computers: _Optional[int] = ...,
        total_partitions: _Optional[int] = ...,
        num_completed_partitions: _Optional[int] = ...,
        recompute_features: _Optional[str] = ...,
        spine_sql_query: _Optional[str] = ...,
        filters: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        planner_options: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        invoker_options: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        query_type: _Optional[_Union[OfflineQueryKind, str]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        required_resolver_tags: _Optional[_Iterable[str]] = ...,
        aggregate_backfill_id: _Optional[str] = ...,
        output: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        required_output: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        raw_body_filename: _Optional[str] = ...,
        dataset_revision: _Optional[_Union[_datasets_pb2.DatasetRevisionMeta, _Mapping]] = ...,
        time_series: _Optional[_Iterable[_Union[_service_pb2.PlanAggregateBackfillResponse, _Mapping]]] = ...,
        evaluation_run_id: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        query_name_version: _Optional[str] = ...,
        job_queue_stats: _Optional[_Union[OfflineQueryJobQueueStats, _Mapping]] = ...,
        resource_group: _Optional[str] = ...,
    ) -> None: ...

class OfflineQueryJobQueueStats(_message.Message):
    __slots__ = (
        "pending_jobs",
        "running_jobs",
        "completed_jobs",
        "failed_jobs",
        "canceled_jobs",
        "scheduled_jobs",
        "waiting_jobs",
        "not_ready_jobs",
    )
    PENDING_JOBS_FIELD_NUMBER: _ClassVar[int]
    RUNNING_JOBS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_JOBS_FIELD_NUMBER: _ClassVar[int]
    FAILED_JOBS_FIELD_NUMBER: _ClassVar[int]
    CANCELED_JOBS_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_JOBS_FIELD_NUMBER: _ClassVar[int]
    WAITING_JOBS_FIELD_NUMBER: _ClassVar[int]
    NOT_READY_JOBS_FIELD_NUMBER: _ClassVar[int]
    pending_jobs: int
    running_jobs: int
    completed_jobs: int
    failed_jobs: int
    canceled_jobs: int
    scheduled_jobs: int
    waiting_jobs: int
    not_ready_jobs: int
    def __init__(
        self,
        pending_jobs: _Optional[int] = ...,
        running_jobs: _Optional[int] = ...,
        completed_jobs: _Optional[int] = ...,
        failed_jobs: _Optional[int] = ...,
        canceled_jobs: _Optional[int] = ...,
        scheduled_jobs: _Optional[int] = ...,
        waiting_jobs: _Optional[int] = ...,
        not_ready_jobs: _Optional[int] = ...,
    ) -> None: ...

class ListOfflineQueriesRequest(_message.Message):
    __slots__ = (
        "cursor",
        "limit",
        "start_date",
        "end_date",
        "id_filter",
        "agent_id_filter",
        "branch_filter",
        "kind_filter",
        "status_filter",
        "aggregation_backfill_id_filter",
        "evaluation_run_id_filter",
        "query_name",
        "query_name_version",
        "resource_groups",
        "agent_ids",
        "branch_filters",
        "kind_filters",
        "status_filters",
        "query_names",
    )
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FILTER_FIELD_NUMBER: _ClassVar[int]
    KIND_FILTER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FILTER_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_BACKFILL_ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    EVALUATION_RUN_ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_VERSION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    AGENT_IDS_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FILTERS_FIELD_NUMBER: _ClassVar[int]
    KIND_FILTERS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FILTERS_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAMES_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    start_date: str
    end_date: str
    id_filter: str
    agent_id_filter: str
    branch_filter: str
    kind_filter: OfflineQueryKind
    status_filter: OfflineQueryStatus
    aggregation_backfill_id_filter: str
    evaluation_run_id_filter: str
    query_name: str
    query_name_version: str
    resource_groups: _containers.RepeatedScalarFieldContainer[str]
    agent_ids: _containers.RepeatedScalarFieldContainer[str]
    branch_filters: _containers.RepeatedScalarFieldContainer[str]
    kind_filters: _containers.RepeatedScalarFieldContainer[OfflineQueryKind]
    status_filters: _containers.RepeatedScalarFieldContainer[OfflineQueryStatus]
    query_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        cursor: _Optional[str] = ...,
        limit: _Optional[int] = ...,
        start_date: _Optional[str] = ...,
        end_date: _Optional[str] = ...,
        id_filter: _Optional[str] = ...,
        agent_id_filter: _Optional[str] = ...,
        branch_filter: _Optional[str] = ...,
        kind_filter: _Optional[_Union[OfflineQueryKind, str]] = ...,
        status_filter: _Optional[_Union[OfflineQueryStatus, str]] = ...,
        aggregation_backfill_id_filter: _Optional[str] = ...,
        evaluation_run_id_filter: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        query_name_version: _Optional[str] = ...,
        resource_groups: _Optional[_Iterable[str]] = ...,
        agent_ids: _Optional[_Iterable[str]] = ...,
        branch_filters: _Optional[_Iterable[str]] = ...,
        kind_filters: _Optional[_Iterable[_Union[OfflineQueryKind, str]]] = ...,
        status_filters: _Optional[_Iterable[_Union[OfflineQueryStatus, str]]] = ...,
        query_names: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class ListOfflineQueriesResponse(_message.Message):
    __slots__ = ("offline_queries", "cursor")
    OFFLINE_QUERIES_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    offline_queries: _containers.RepeatedCompositeFieldContainer[OfflineQueryMeta]
    cursor: str
    def __init__(
        self,
        offline_queries: _Optional[_Iterable[_Union[OfflineQueryMeta, _Mapping]]] = ...,
        cursor: _Optional[str] = ...,
    ) -> None: ...

class GetOfflineQueryRequest(_message.Message):
    __slots__ = ("offline_query_id",)
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    offline_query_id: str
    def __init__(self, offline_query_id: _Optional[str] = ...) -> None: ...

class GetOfflineQueryResponse(_message.Message):
    __slots__ = ("offline_query",)
    OFFLINE_QUERY_FIELD_NUMBER: _ClassVar[int]
    offline_query: OfflineQueryMeta
    def __init__(self, offline_query: _Optional[_Union[OfflineQueryMeta, _Mapping]] = ...) -> None: ...

class GetOfflineQueryRequestBodyRequest(_message.Message):
    __slots__ = ("offline_query_id",)
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    offline_query_id: str
    def __init__(self, offline_query_id: _Optional[str] = ...) -> None: ...

class GetOfflineQueryRequestBodyResponse(_message.Message):
    __slots__ = ("request_body_json_string",)
    REQUEST_BODY_JSON_STRING_FIELD_NUMBER: _ClassVar[int]
    request_body_json_string: str
    def __init__(self, request_body_json_string: _Optional[str] = ...) -> None: ...

class ListOfflineQueryShardsFilters(_message.Message):
    __slots__ = ("status", "shard_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    status: OfflineQueryStatus
    shard_id: int
    def __init__(
        self, status: _Optional[_Union[OfflineQueryStatus, str]] = ..., shard_id: _Optional[int] = ...
    ) -> None: ...

class ListOfflineQueryShardsPageToken(_message.Message):
    __slots__ = ("shard_id",)
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    shard_id: int
    def __init__(self, shard_id: _Optional[int] = ...) -> None: ...

class ListOfflineQueryShardsRequest(_message.Message):
    __slots__ = ("offline_query_id", "filters", "limit", "page_token")
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    offline_query_id: str
    filters: ListOfflineQueryShardsFilters
    limit: int
    page_token: str
    def __init__(
        self,
        offline_query_id: _Optional[str] = ...,
        filters: _Optional[_Union[ListOfflineQueryShardsFilters, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class ListOfflineQueryShardsResponse(_message.Message):
    __slots__ = ("offline_query_shards", "next_page_token")
    OFFLINE_QUERY_SHARDS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    offline_query_shards: _containers.RepeatedCompositeFieldContainer[OfflineQueryShard]
    next_page_token: str
    def __init__(
        self,
        offline_query_shards: _Optional[_Iterable[_Union[OfflineQueryShard, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...

class OfflineQueryShardStatusAggregate(_message.Message):
    __slots__ = ("status", "count")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    status: OfflineQueryStatus
    count: int
    def __init__(
        self, status: _Optional[_Union[OfflineQueryStatus, str]] = ..., count: _Optional[int] = ...
    ) -> None: ...

class GetOfflineQueryShardsAggregatedRequest(_message.Message):
    __slots__ = ("offline_query_id",)
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    offline_query_id: str
    def __init__(self, offline_query_id: _Optional[str] = ...) -> None: ...

class GetOfflineQueryShardsAggregatedResponse(_message.Message):
    __slots__ = ("aggregates",)
    AGGREGATES_FIELD_NUMBER: _ClassVar[int]
    aggregates: _containers.RepeatedCompositeFieldContainer[OfflineQueryShardStatusAggregate]
    def __init__(
        self, aggregates: _Optional[_Iterable[_Union[OfflineQueryShardStatusAggregate, _Mapping]]] = ...
    ) -> None: ...

class GetOfflineQueryInfraSummaryRequest(_message.Message):
    __slots__ = ("offline_query_id",)
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    offline_query_id: str
    def __init__(self, offline_query_id: _Optional[str] = ...) -> None: ...

class GetOfflineQueryInfraSummaryResponse(_message.Message):
    __slots__ = ("pod_names",)
    POD_NAMES_FIELD_NUMBER: _ClassVar[int]
    pod_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pod_names: _Optional[_Iterable[str]] = ...) -> None: ...

class GetOfflineQueryProfileSummaryRequest(_message.Message):
    __slots__ = ("offline_query_id",)
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    offline_query_id: str
    def __init__(self, offline_query_id: _Optional[str] = ...) -> None: ...

class OfflineQueryProfilePercentileStats(_message.Message):
    __slots__ = ("p50", "p75", "p90", "p99", "p_max")
    P50_FIELD_NUMBER: _ClassVar[int]
    P75_FIELD_NUMBER: _ClassVar[int]
    P90_FIELD_NUMBER: _ClassVar[int]
    P99_FIELD_NUMBER: _ClassVar[int]
    P_MAX_FIELD_NUMBER: _ClassVar[int]
    p50: float
    p75: float
    p90: float
    p99: float
    p_max: float
    def __init__(
        self,
        p50: _Optional[float] = ...,
        p75: _Optional[float] = ...,
        p90: _Optional[float] = ...,
        p99: _Optional[float] = ...,
        p_max: _Optional[float] = ...,
    ) -> None: ...

class OfflineQueryProfileSummaryRow(_message.Message):
    __slots__ = ("source", "metric", "count", "stats")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    source: str
    metric: str
    count: int
    stats: OfflineQueryProfilePercentileStats
    def __init__(
        self,
        source: _Optional[str] = ...,
        metric: _Optional[str] = ...,
        count: _Optional[int] = ...,
        stats: _Optional[_Union[OfflineQueryProfilePercentileStats, _Mapping]] = ...,
    ) -> None: ...

class GetOfflineQueryProfileSummaryResponse(_message.Message):
    __slots__ = ("operation_id", "status", "shard_count", "performance_shards", "pod_names", "rows", "warnings")
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SHARD_COUNT_FIELD_NUMBER: _ClassVar[int]
    PERFORMANCE_SHARDS_FIELD_NUMBER: _ClassVar[int]
    POD_NAMES_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    status: OfflineQueryStatus
    shard_count: int
    performance_shards: int
    pod_names: _containers.RepeatedScalarFieldContainer[str]
    rows: _containers.RepeatedCompositeFieldContainer[OfflineQueryProfileSummaryRow]
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        status: _Optional[_Union[OfflineQueryStatus, str]] = ...,
        shard_count: _Optional[int] = ...,
        performance_shards: _Optional[int] = ...,
        pod_names: _Optional[_Iterable[str]] = ...,
        rows: _Optional[_Iterable[_Union[OfflineQueryProfileSummaryRow, _Mapping]]] = ...,
        warnings: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class OfflineQueryUtilizationStats(_message.Message):
    __slots__ = ("peak", "average", "min", "sample_count")
    PEAK_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_COUNT_FIELD_NUMBER: _ClassVar[int]
    peak: float
    average: float
    min: float
    sample_count: int
    def __init__(
        self,
        peak: _Optional[float] = ...,
        average: _Optional[float] = ...,
        min: _Optional[float] = ...,
        sample_count: _Optional[int] = ...,
    ) -> None: ...

class OfflineQueryPodInfo(_message.Message):
    __slots__ = (
        "pod_name",
        "resource_group",
        "node_name",
        "instance_type",
        "node_cpu",
        "node_memory",
        "cpu_request",
        "memory_request",
    )
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_CPU_FIELD_NUMBER: _ClassVar[int]
    NODE_MEMORY_FIELD_NUMBER: _ClassVar[int]
    CPU_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MEMORY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    pod_name: str
    resource_group: str
    node_name: str
    instance_type: str
    node_cpu: str
    node_memory: str
    cpu_request: str
    memory_request: str
    def __init__(
        self,
        pod_name: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        node_name: _Optional[str] = ...,
        instance_type: _Optional[str] = ...,
        node_cpu: _Optional[str] = ...,
        node_memory: _Optional[str] = ...,
        cpu_request: _Optional[str] = ...,
        memory_request: _Optional[str] = ...,
    ) -> None: ...

class OfflineQueryUtilizationSummary(_message.Message):
    __slots__ = (
        "operation_id",
        "query_name",
        "status",
        "created_at",
        "completed_at",
        "cpu",
        "memory",
        "disk",
        "warnings",
        "resource_groups",
        "pods",
    )
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    DISK_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    query_name: str
    status: OfflineQueryStatus
    created_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    cpu: OfflineQueryUtilizationStats
    memory: OfflineQueryUtilizationStats
    disk: OfflineQueryUtilizationStats
    warnings: _containers.RepeatedScalarFieldContainer[str]
    resource_groups: _containers.RepeatedScalarFieldContainer[str]
    pods: _containers.RepeatedCompositeFieldContainer[OfflineQueryPodInfo]
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        query_name: _Optional[str] = ...,
        status: _Optional[_Union[OfflineQueryStatus, str]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        cpu: _Optional[_Union[OfflineQueryUtilizationStats, _Mapping]] = ...,
        memory: _Optional[_Union[OfflineQueryUtilizationStats, _Mapping]] = ...,
        disk: _Optional[_Union[OfflineQueryUtilizationStats, _Mapping]] = ...,
        warnings: _Optional[_Iterable[str]] = ...,
        resource_groups: _Optional[_Iterable[str]] = ...,
        pods: _Optional[_Iterable[_Union[OfflineQueryPodInfo, _Mapping]]] = ...,
    ) -> None: ...

class GetOfflineQueryUtilizationSummariesRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "limit")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    limit: int
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        limit: _Optional[int] = ...,
    ) -> None: ...

class GetOfflineQueryUtilizationSummariesResponse(_message.Message):
    __slots__ = ("summaries", "warnings", "truncated")
    SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    summaries: _containers.RepeatedCompositeFieldContainer[OfflineQueryUtilizationSummary]
    warnings: _containers.RepeatedScalarFieldContainer[str]
    truncated: bool
    def __init__(
        self,
        summaries: _Optional[_Iterable[_Union[OfflineQueryUtilizationSummary, _Mapping]]] = ...,
        warnings: _Optional[_Iterable[str]] = ...,
        truncated: bool = ...,
    ) -> None: ...

class ResourceGroupUtilizationBucket(_message.Message):
    __slots__ = ("bucket_start", "cpu", "memory", "disk")
    BUCKET_START_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    DISK_FIELD_NUMBER: _ClassVar[int]
    bucket_start: _timestamp_pb2.Timestamp
    cpu: OfflineQueryUtilizationStats
    memory: OfflineQueryUtilizationStats
    disk: OfflineQueryUtilizationStats
    def __init__(
        self,
        bucket_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        cpu: _Optional[_Union[OfflineQueryUtilizationStats, _Mapping]] = ...,
        memory: _Optional[_Union[OfflineQueryUtilizationStats, _Mapping]] = ...,
        disk: _Optional[_Union[OfflineQueryUtilizationStats, _Mapping]] = ...,
    ) -> None: ...

class ResourceGroupUtilizationSeries(_message.Message):
    __slots__ = ("resource_group", "buckets", "warnings")
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    resource_group: str
    buckets: _containers.RepeatedCompositeFieldContainer[ResourceGroupUtilizationBucket]
    warnings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        resource_group: _Optional[str] = ...,
        buckets: _Optional[_Iterable[_Union[ResourceGroupUtilizationBucket, _Mapping]]] = ...,
        warnings: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetResourceGroupUtilizationTimeseriesRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "bucket_duration", "resource_groups")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    bucket_duration: str
    resource_groups: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        bucket_duration: _Optional[str] = ...,
        resource_groups: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetResourceGroupUtilizationTimeseriesResponse(_message.Message):
    __slots__ = ("series", "warnings", "bucket_duration")
    SERIES_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_FIELD_NUMBER: _ClassVar[int]
    series: _containers.RepeatedCompositeFieldContainer[ResourceGroupUtilizationSeries]
    warnings: _containers.RepeatedScalarFieldContainer[str]
    bucket_duration: str
    def __init__(
        self,
        series: _Optional[_Iterable[_Union[ResourceGroupUtilizationSeries, _Mapping]]] = ...,
        warnings: _Optional[_Iterable[str]] = ...,
        bucket_duration: _Optional[str] = ...,
    ) -> None: ...

class ResourceGroupJobBucket(_message.Message):
    __slots__ = ("bucket_start", "shard_count", "query_count", "cpu_request_cores", "memory_request_bytes")
    BUCKET_START_FIELD_NUMBER: _ClassVar[int]
    SHARD_COUNT_FIELD_NUMBER: _ClassVar[int]
    QUERY_COUNT_FIELD_NUMBER: _ClassVar[int]
    CPU_REQUEST_CORES_FIELD_NUMBER: _ClassVar[int]
    MEMORY_REQUEST_BYTES_FIELD_NUMBER: _ClassVar[int]
    bucket_start: _timestamp_pb2.Timestamp
    shard_count: int
    query_count: int
    cpu_request_cores: float
    memory_request_bytes: float
    def __init__(
        self,
        bucket_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        shard_count: _Optional[int] = ...,
        query_count: _Optional[int] = ...,
        cpu_request_cores: _Optional[float] = ...,
        memory_request_bytes: _Optional[float] = ...,
    ) -> None: ...

class ResourceGroupJobSeries(_message.Message):
    __slots__ = ("resource_group", "buckets")
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    resource_group: str
    buckets: _containers.RepeatedCompositeFieldContainer[ResourceGroupJobBucket]
    def __init__(
        self,
        resource_group: _Optional[str] = ...,
        buckets: _Optional[_Iterable[_Union[ResourceGroupJobBucket, _Mapping]]] = ...,
    ) -> None: ...

class GetResourceGroupJobTimeseriesRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "bucket_duration", "resource_groups")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    bucket_duration: str
    resource_groups: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        bucket_duration: _Optional[str] = ...,
        resource_groups: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class GetResourceGroupJobTimeseriesResponse(_message.Message):
    __slots__ = ("series", "warnings", "bucket_duration")
    SERIES_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    BUCKET_DURATION_FIELD_NUMBER: _ClassVar[int]
    series: _containers.RepeatedCompositeFieldContainer[ResourceGroupJobSeries]
    warnings: _containers.RepeatedScalarFieldContainer[str]
    bucket_duration: str
    def __init__(
        self,
        series: _Optional[_Iterable[_Union[ResourceGroupJobSeries, _Mapping]]] = ...,
        warnings: _Optional[_Iterable[str]] = ...,
        bucket_duration: _Optional[str] = ...,
    ) -> None: ...

class CreateOfflineQueryJobRequest(_message.Message):
    __slots__ = ("offline_query_request",)
    OFFLINE_QUERY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    offline_query_request: _offline_query_pb2.OfflineQueryRequest
    def __init__(
        self, offline_query_request: _Optional[_Union[_offline_query_pb2.OfflineQueryRequest, _Mapping]] = ...
    ) -> None: ...

class CreateOfflineQueryJobResponse(_message.Message):
    __slots__ = ("dataset_response",)
    DATASET_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    dataset_response: _dataset_response_pb2.DatasetResponse
    def __init__(
        self, dataset_response: _Optional[_Union[_dataset_response_pb2.DatasetResponse, _Mapping]] = ...
    ) -> None: ...

class CreateModelTrainingJobRequest(_message.Message):
    __slots__ = ("training_job_request",)
    TRAINING_JOB_REQUEST_FIELD_NUMBER: _ClassVar[int]
    training_job_request: _offline_query_pb2.OfflineQueryRequest
    def __init__(
        self, training_job_request: _Optional[_Union[_offline_query_pb2.OfflineQueryRequest, _Mapping]] = ...
    ) -> None: ...

class CreateModelTrainingJobResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IngestDatasetRequest(_message.Message):
    __slots__ = (
        "outputs",
        "revision_id",
        "branch",
        "planner_options",
        "store_online",
        "store_offline",
        "enable_profiling",
        "online_timestamping_mode",
        "explain",
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

    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    REVISION_ID_FIELD_NUMBER: _ClassVar[int]
    BRANCH_FIELD_NUMBER: _ClassVar[int]
    PLANNER_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    STORE_ONLINE_FIELD_NUMBER: _ClassVar[int]
    STORE_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PROFILING_FIELD_NUMBER: _ClassVar[int]
    ONLINE_TIMESTAMPING_MODE_FIELD_NUMBER: _ClassVar[int]
    EXPLAIN_FIELD_NUMBER: _ClassVar[int]
    outputs: _containers.RepeatedScalarFieldContainer[str]
    revision_id: str
    branch: str
    planner_options: _containers.MessageMap[str, _struct_pb2.Value]
    store_online: bool
    store_offline: bool
    enable_profiling: bool
    online_timestamping_mode: str
    explain: bool
    def __init__(
        self,
        outputs: _Optional[_Iterable[str]] = ...,
        revision_id: _Optional[str] = ...,
        branch: _Optional[str] = ...,
        planner_options: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        store_online: bool = ...,
        store_offline: bool = ...,
        enable_profiling: bool = ...,
        online_timestamping_mode: _Optional[str] = ...,
        explain: bool = ...,
    ) -> None: ...

class IngestDatasetResponse(_message.Message):
    __slots__ = ("dataset_response",)
    DATASET_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    dataset_response: _dataset_response_pb2.DatasetResponse
    def __init__(
        self, dataset_response: _Optional[_Union[_dataset_response_pb2.DatasetResponse, _Mapping]] = ...
    ) -> None: ...

class RetryOfflineQueryShardRequest(_message.Message):
    __slots__ = ("offline_query_id", "shard_index")
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_INDEX_FIELD_NUMBER: _ClassVar[int]
    offline_query_id: str
    shard_index: int
    def __init__(self, offline_query_id: _Optional[str] = ..., shard_index: _Optional[int] = ...) -> None: ...

class RetryOfflineQueryShardResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CancelAsyncOfflineQueryRequest(_message.Message):
    __slots__ = ("offline_query_id",)
    OFFLINE_QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    offline_query_id: str
    def __init__(self, offline_query_id: _Optional[str] = ...) -> None: ...

class CancelAsyncOfflineQueryResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class BatchProgress(_message.Message):
    __slots__ = ("total", "computed", "failed", "start", "end", "total_duration_s", "stored_online", "stored_offline")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    COMPUTED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    TOTAL_DURATION_S_FIELD_NUMBER: _ClassVar[int]
    STORED_ONLINE_FIELD_NUMBER: _ClassVar[int]
    STORED_OFFLINE_FIELD_NUMBER: _ClassVar[int]
    total: str
    computed: str
    failed: str
    start: _timestamp_pb2.Timestamp
    end: _timestamp_pb2.Timestamp
    total_duration_s: float
    stored_online: str
    stored_offline: str
    def __init__(
        self,
        total: _Optional[str] = ...,
        computed: _Optional[str] = ...,
        failed: _Optional[str] = ...,
        start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        total_duration_s: _Optional[float] = ...,
        stored_online: _Optional[str] = ...,
        stored_offline: _Optional[str] = ...,
    ) -> None: ...

class ChunkReport(_message.Message):
    __slots__ = ("progress", "generated_at")
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    progress: BatchProgress
    generated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        progress: _Optional[_Union[BatchProgress, _Mapping]] = ...,
        generated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class BatchResolverReport(_message.Message):
    __slots__ = ("resolver_fqn", "status", "chunks", "progress", "generated_at", "error", "all_errors")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ALL_ERRORS_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: str
    status: BatchOpStatus
    chunks: _containers.RepeatedCompositeFieldContainer[ChunkReport]
    progress: BatchProgress
    generated_at: _timestamp_pb2.Timestamp
    error: _chalk_error_pb2.ChalkError
    all_errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    def __init__(
        self,
        resolver_fqn: _Optional[str] = ...,
        status: _Optional[_Union[BatchOpStatus, str]] = ...,
        chunks: _Optional[_Iterable[_Union[ChunkReport, _Mapping]]] = ...,
        progress: _Optional[_Union[BatchProgress, _Mapping]] = ...,
        generated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        error: _Optional[_Union[_chalk_error_pb2.ChalkError, _Mapping]] = ...,
        all_errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
    ) -> None: ...

class BatchReport(_message.Message):
    __slots__ = (
        "operation_id",
        "operation_kind",
        "status",
        "resolvers",
        "progress",
        "environment_id",
        "team_id",
        "deployment_id",
        "error",
        "generated_at",
        "all_errors",
        "operation_metadata",
        "started_at",
        "ended_at",
    )
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_KIND_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    GENERATED_AT_FIELD_NUMBER: _ClassVar[int]
    ALL_ERRORS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_METADATA_FIELD_NUMBER: _ClassVar[int]
    STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    ENDED_AT_FIELD_NUMBER: _ClassVar[int]
    operation_id: str
    operation_kind: BatchOpKind
    status: BatchOpStatus
    resolvers: _containers.RepeatedCompositeFieldContainer[BatchResolverReport]
    progress: BatchProgress
    environment_id: str
    team_id: str
    deployment_id: str
    error: _chalk_error_pb2.ChalkError
    generated_at: _timestamp_pb2.Timestamp
    all_errors: _containers.RepeatedCompositeFieldContainer[_chalk_error_pb2.ChalkError]
    operation_metadata: _struct_pb2.Value
    started_at: _timestamp_pb2.Timestamp
    ended_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        operation_id: _Optional[str] = ...,
        operation_kind: _Optional[_Union[BatchOpKind, str]] = ...,
        status: _Optional[_Union[BatchOpStatus, str]] = ...,
        resolvers: _Optional[_Iterable[_Union[BatchResolverReport, _Mapping]]] = ...,
        progress: _Optional[_Union[BatchProgress, _Mapping]] = ...,
        environment_id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        deployment_id: _Optional[str] = ...,
        error: _Optional[_Union[_chalk_error_pb2.ChalkError, _Mapping]] = ...,
        generated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        all_errors: _Optional[_Iterable[_Union[_chalk_error_pb2.ChalkError, _Mapping]]] = ...,
        operation_metadata: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...,
        started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        ended_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetBatchReportRequest(_message.Message):
    __slots__ = ("report_id", "shard_id", "get_mask")
    REPORT_ID_FIELD_NUMBER: _ClassVar[int]
    SHARD_ID_FIELD_NUMBER: _ClassVar[int]
    GET_MASK_FIELD_NUMBER: _ClassVar[int]
    report_id: str
    shard_id: int
    get_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        report_id: _Optional[str] = ...,
        shard_id: _Optional[int] = ...,
        get_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class GetBatchReportResponse(_message.Message):
    __slots__ = ("batch_report",)
    BATCH_REPORT_FIELD_NUMBER: _ClassVar[int]
    batch_report: BatchReport
    def __init__(self, batch_report: _Optional[_Union[BatchReport, _Mapping]] = ...) -> None: ...

class ListOfflineQueryNamesRequest(_message.Message):
    __slots__ = ("cursor", "limit")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    def __init__(self, cursor: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class ListOfflineQueryNamesResponse(_message.Message):
    __slots__ = ("query_names", "next_cursor")
    QUERY_NAMES_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    query_names: _containers.RepeatedScalarFieldContainer[str]
    next_cursor: str
    def __init__(self, query_names: _Optional[_Iterable[str]] = ..., next_cursor: _Optional[str] = ...) -> None: ...
