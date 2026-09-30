from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
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

class GetClickhouseUriRequest(_message.Message):
    __slots__ = ("env_id", "cluster_name")
    ENV_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    env_id: str
    cluster_name: str
    def __init__(self, env_id: _Optional[str] = ..., cluster_name: _Optional[str] = ...) -> None: ...

class GetClickhouseUriResponse(_message.Message):
    __slots__ = ("uri", "username", "host", "secret_name")
    URI_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    uri: str
    username: str
    host: str
    secret_name: str
    def __init__(
        self,
        uri: _Optional[str] = ...,
        username: _Optional[str] = ...,
        host: _Optional[str] = ...,
        secret_name: _Optional[str] = ...,
    ) -> None: ...

class OtelTtls(_message.Message):
    __slots__ = ("log_ttl_minutes", "trace_ttl_minutes")
    LOG_TTL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    TRACE_TTL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    log_ttl_minutes: int
    trace_ttl_minutes: int
    def __init__(self, log_ttl_minutes: _Optional[int] = ..., trace_ttl_minutes: _Optional[int] = ...) -> None: ...

class SetClickhouseOtelTtlsRequest(_message.Message):
    __slots__ = ("log_ttl_minutes", "trace_ttl_minutes")
    LOG_TTL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    TRACE_TTL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    log_ttl_minutes: int
    trace_ttl_minutes: int
    def __init__(self, log_ttl_minutes: _Optional[int] = ..., trace_ttl_minutes: _Optional[int] = ...) -> None: ...

class SetClickhouseOtelTtlsResponse(_message.Message):
    __slots__ = ("ttls",)
    TTLS_FIELD_NUMBER: _ClassVar[int]
    ttls: OtelTtls
    def __init__(self, ttls: _Optional[_Union[OtelTtls, _Mapping]] = ...) -> None: ...

class GetClickhouseOtelTtlsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetClickhouseOtelTtlsResponse(_message.Message):
    __slots__ = ("ttls",)
    TTLS_FIELD_NUMBER: _ClassVar[int]
    ttls: OtelTtls
    def __init__(self, ttls: _Optional[_Union[OtelTtls, _Mapping]] = ...) -> None: ...

class ClickhouseStorageSpec(_message.Message):
    __slots__ = ("storage", "storage_class_name")
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    STORAGE_CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    storage: str
    storage_class_name: str
    def __init__(self, storage: _Optional[str] = ..., storage_class_name: _Optional[str] = ...) -> None: ...

class ClickhouseOtelTableStorage(_message.Message):
    __slots__ = ("database", "table", "size", "size_bytes", "rows")
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    database: str
    table: str
    size: str
    size_bytes: int
    rows: int
    def __init__(
        self,
        database: _Optional[str] = ...,
        table: _Optional[str] = ...,
        size: _Optional[str] = ...,
        size_bytes: _Optional[int] = ...,
        rows: _Optional[int] = ...,
    ) -> None: ...

class ClickhousePartitionVolume(_message.Message):
    __slots__ = ("partition", "database", "table", "size_bytes", "rows")
    PARTITION_FIELD_NUMBER: _ClassVar[int]
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    partition: str
    database: str
    table: str
    size_bytes: int
    rows: int
    def __init__(
        self,
        partition: _Optional[str] = ...,
        database: _Optional[str] = ...,
        table: _Optional[str] = ...,
        size_bytes: _Optional[int] = ...,
        rows: _Optional[int] = ...,
    ) -> None: ...

class ClickhouseDiskUsage(_message.Message):
    __slots__ = ("total_bytes", "free_bytes", "used_ratio", "target_used_ratio")
    TOTAL_BYTES_FIELD_NUMBER: _ClassVar[int]
    FREE_BYTES_FIELD_NUMBER: _ClassVar[int]
    USED_RATIO_FIELD_NUMBER: _ClassVar[int]
    TARGET_USED_RATIO_FIELD_NUMBER: _ClassVar[int]
    total_bytes: int
    free_bytes: int
    used_ratio: float
    target_used_ratio: float
    def __init__(
        self,
        total_bytes: _Optional[int] = ...,
        free_bytes: _Optional[int] = ...,
        used_ratio: _Optional[float] = ...,
        target_used_ratio: _Optional[float] = ...,
    ) -> None: ...

class GetClickhouseInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetClickhouseInfoResponse(_message.Message):
    __slots__ = (
        "ttls",
        "storage",
        "tables",
        "total_size_bytes",
        "resources",
        "latest_migration",
        "insert_failures",
        "resources_error",
        "latest_migration_error",
        "insert_failures_error",
        "insert_failure_lookback_minutes",
        "log_partitions",
        "trace_partitions",
        "partition_volumes_error",
        "disk",
        "disk_error",
    )
    TTLS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    LATEST_MIGRATION_FIELD_NUMBER: _ClassVar[int]
    INSERT_FAILURES_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_ERROR_FIELD_NUMBER: _ClassVar[int]
    LATEST_MIGRATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    INSERT_FAILURES_ERROR_FIELD_NUMBER: _ClassVar[int]
    INSERT_FAILURE_LOOKBACK_MINUTES_FIELD_NUMBER: _ClassVar[int]
    LOG_PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    TRACE_PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    PARTITION_VOLUMES_ERROR_FIELD_NUMBER: _ClassVar[int]
    DISK_FIELD_NUMBER: _ClassVar[int]
    DISK_ERROR_FIELD_NUMBER: _ClassVar[int]
    ttls: OtelTtls
    storage: ClickhouseStorageSpec
    tables: _containers.RepeatedCompositeFieldContainer[ClickhouseOtelTableStorage]
    total_size_bytes: int
    resources: ClickhouseResourceUsage
    latest_migration: ClickhouseMigration
    insert_failures: _containers.RepeatedCompositeFieldContainer[ClickhouseInsertFailure]
    resources_error: str
    latest_migration_error: str
    insert_failures_error: str
    insert_failure_lookback_minutes: int
    log_partitions: _containers.RepeatedCompositeFieldContainer[ClickhousePartitionVolume]
    trace_partitions: _containers.RepeatedCompositeFieldContainer[ClickhousePartitionVolume]
    partition_volumes_error: str
    disk: ClickhouseDiskUsage
    disk_error: str
    def __init__(
        self,
        ttls: _Optional[_Union[OtelTtls, _Mapping]] = ...,
        storage: _Optional[_Union[ClickhouseStorageSpec, _Mapping]] = ...,
        tables: _Optional[_Iterable[_Union[ClickhouseOtelTableStorage, _Mapping]]] = ...,
        total_size_bytes: _Optional[int] = ...,
        resources: _Optional[_Union[ClickhouseResourceUsage, _Mapping]] = ...,
        latest_migration: _Optional[_Union[ClickhouseMigration, _Mapping]] = ...,
        insert_failures: _Optional[_Iterable[_Union[ClickhouseInsertFailure, _Mapping]]] = ...,
        resources_error: _Optional[str] = ...,
        latest_migration_error: _Optional[str] = ...,
        insert_failures_error: _Optional[str] = ...,
        insert_failure_lookback_minutes: _Optional[int] = ...,
        log_partitions: _Optional[_Iterable[_Union[ClickhousePartitionVolume, _Mapping]]] = ...,
        trace_partitions: _Optional[_Iterable[_Union[ClickhousePartitionVolume, _Mapping]]] = ...,
        partition_volumes_error: _Optional[str] = ...,
        disk: _Optional[_Union[ClickhouseDiskUsage, _Mapping]] = ...,
        disk_error: _Optional[str] = ...,
    ) -> None: ...

class ClickhouseResourceUsage(_message.Message):
    __slots__ = ("pod_name", "cpu_usage", "cpu_request", "cpu_limit", "memory_usage", "memory_request", "memory_limit")
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    CPU_USAGE_FIELD_NUMBER: _ClassVar[int]
    CPU_REQUEST_FIELD_NUMBER: _ClassVar[int]
    CPU_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_USAGE_FIELD_NUMBER: _ClassVar[int]
    MEMORY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MEMORY_LIMIT_FIELD_NUMBER: _ClassVar[int]
    pod_name: str
    cpu_usage: str
    cpu_request: str
    cpu_limit: str
    memory_usage: str
    memory_request: str
    memory_limit: str
    def __init__(
        self,
        pod_name: _Optional[str] = ...,
        cpu_usage: _Optional[str] = ...,
        cpu_request: _Optional[str] = ...,
        cpu_limit: _Optional[str] = ...,
        memory_usage: _Optional[str] = ...,
        memory_request: _Optional[str] = ...,
        memory_limit: _Optional[str] = ...,
    ) -> None: ...

class ClickhouseMigration(_message.Message):
    __slots__ = ("version", "applied_at")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    APPLIED_AT_FIELD_NUMBER: _ClassVar[int]
    version: int
    applied_at: str
    def __init__(self, version: _Optional[int] = ..., applied_at: _Optional[str] = ...) -> None: ...

class ClickhouseInsertFailure(_message.Message):
    __slots__ = ("event_time", "tables", "exception_code", "exception")
    EVENT_TIME_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_CODE_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    event_time: str
    tables: str
    exception_code: int
    exception: str
    def __init__(
        self,
        event_time: _Optional[str] = ...,
        tables: _Optional[str] = ...,
        exception_code: _Optional[int] = ...,
        exception: _Optional[str] = ...,
    ) -> None: ...

class ClickhouseSlowRead(_message.Message):
    __slots__ = (
        "event_time",
        "query_duration_ms",
        "read_rows",
        "read_bytes",
        "result_rows",
        "peak_memory_bytes",
        "selected_marks",
        "cpu_time_microseconds",
        "normalized_query_hash",
        "normalized_query",
    )
    EVENT_TIME_FIELD_NUMBER: _ClassVar[int]
    QUERY_DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    READ_ROWS_FIELD_NUMBER: _ClassVar[int]
    READ_BYTES_FIELD_NUMBER: _ClassVar[int]
    RESULT_ROWS_FIELD_NUMBER: _ClassVar[int]
    PEAK_MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    SELECTED_MARKS_FIELD_NUMBER: _ClassVar[int]
    CPU_TIME_MICROSECONDS_FIELD_NUMBER: _ClassVar[int]
    NORMALIZED_QUERY_HASH_FIELD_NUMBER: _ClassVar[int]
    NORMALIZED_QUERY_FIELD_NUMBER: _ClassVar[int]
    event_time: str
    query_duration_ms: int
    read_rows: int
    read_bytes: int
    result_rows: int
    peak_memory_bytes: int
    selected_marks: int
    cpu_time_microseconds: int
    normalized_query_hash: str
    normalized_query: str
    def __init__(
        self,
        event_time: _Optional[str] = ...,
        query_duration_ms: _Optional[int] = ...,
        read_rows: _Optional[int] = ...,
        read_bytes: _Optional[int] = ...,
        result_rows: _Optional[int] = ...,
        peak_memory_bytes: _Optional[int] = ...,
        selected_marks: _Optional[int] = ...,
        cpu_time_microseconds: _Optional[int] = ...,
        normalized_query_hash: _Optional[str] = ...,
        normalized_query: _Optional[str] = ...,
    ) -> None: ...

class ClickhouseTtlAlignment(_message.Message):
    __slots__ = (
        "database",
        "table",
        "configured_ttl_minutes",
        "effective_ttl_minutes",
        "effective_ttl_expression",
        "aligned",
    )
    DATABASE_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    CONFIGURED_TTL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TTL_MINUTES_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_TTL_EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    ALIGNED_FIELD_NUMBER: _ClassVar[int]
    database: str
    table: str
    configured_ttl_minutes: int
    effective_ttl_minutes: int
    effective_ttl_expression: str
    aligned: bool
    def __init__(
        self,
        database: _Optional[str] = ...,
        table: _Optional[str] = ...,
        configured_ttl_minutes: _Optional[int] = ...,
        effective_ttl_minutes: _Optional[int] = ...,
        effective_ttl_expression: _Optional[str] = ...,
        aligned: bool = ...,
    ) -> None: ...

class GetClickhouseRetentionHistoryRequest(_message.Message):
    __slots__ = ("start_time", "end_time", "step")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    step: _duration_pb2.Duration
    def __init__(
        self,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        step: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class GetClickhouseRetentionHistoryResponse(_message.Message):
    __slots__ = ("retention", "disk_utilization", "cpu", "memory", "parts", "concurrency", "query_rate", "ingest")
    RETENTION_FIELD_NUMBER: _ClassVar[int]
    DISK_UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    QUERY_RATE_FIELD_NUMBER: _ClassVar[int]
    INGEST_FIELD_NUMBER: _ClassVar[int]
    retention: _densetimeserieschart_pb2.DenseTimeSeriesChart
    disk_utilization: _densetimeserieschart_pb2.DenseTimeSeriesChart
    cpu: _densetimeserieschart_pb2.DenseTimeSeriesChart
    memory: _densetimeserieschart_pb2.DenseTimeSeriesChart
    parts: _densetimeserieschart_pb2.DenseTimeSeriesChart
    concurrency: _densetimeserieschart_pb2.DenseTimeSeriesChart
    query_rate: _densetimeserieschart_pb2.DenseTimeSeriesChart
    ingest: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self,
        retention: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...,
        disk_utilization: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...,
        cpu: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...,
        memory: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...,
        parts: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...,
        concurrency: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...,
        query_rate: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...,
        ingest: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...,
    ) -> None: ...

class GetClickhouseAdminDiagnosticsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetClickhouseAdminDiagnosticsResponse(_message.Message):
    __slots__ = (
        "slow_reads",
        "ttl_alignments",
        "slow_read_lookback_minutes",
        "slow_reads_error",
        "ttl_alignments_error",
    )
    SLOW_READS_FIELD_NUMBER: _ClassVar[int]
    TTL_ALIGNMENTS_FIELD_NUMBER: _ClassVar[int]
    SLOW_READ_LOOKBACK_MINUTES_FIELD_NUMBER: _ClassVar[int]
    SLOW_READS_ERROR_FIELD_NUMBER: _ClassVar[int]
    TTL_ALIGNMENTS_ERROR_FIELD_NUMBER: _ClassVar[int]
    slow_reads: _containers.RepeatedCompositeFieldContainer[ClickhouseSlowRead]
    ttl_alignments: _containers.RepeatedCompositeFieldContainer[ClickhouseTtlAlignment]
    slow_read_lookback_minutes: int
    slow_reads_error: str
    ttl_alignments_error: str
    def __init__(
        self,
        slow_reads: _Optional[_Iterable[_Union[ClickhouseSlowRead, _Mapping]]] = ...,
        ttl_alignments: _Optional[_Iterable[_Union[ClickhouseTtlAlignment, _Mapping]]] = ...,
        slow_read_lookback_minutes: _Optional[int] = ...,
        slow_reads_error: _Optional[str] = ...,
        ttl_alignments_error: _Optional[str] = ...,
    ) -> None: ...
