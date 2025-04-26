from chalk._gen.chalk.aggregate.v1 import service_pb2 as _service_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import datasets_pb2 as _datasets_pb2
from chalk._gen.chalk.server.v1 import performance_summary_pb2 as _performance_summary_pb2
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
