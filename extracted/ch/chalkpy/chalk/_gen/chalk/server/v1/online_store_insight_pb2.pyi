from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import chart_pb2 as _chart_pb2
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

class DynamoDBBillingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DYNAMO_DB_BILLING_MODE_UNSPECIFIED: _ClassVar[DynamoDBBillingMode]
    DYNAMO_DB_BILLING_MODE_PROVISIONED: _ClassVar[DynamoDBBillingMode]
    DYNAMO_DB_BILLING_MODE_PAY_PER_REQUEST: _ClassVar[DynamoDBBillingMode]

class MetricsTimeRange(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRICS_TIME_RANGE_UNSPECIFIED: _ClassVar[MetricsTimeRange]
    METRICS_TIME_RANGE_1H: _ClassVar[MetricsTimeRange]
    METRICS_TIME_RANGE_24H: _ClassVar[MetricsTimeRange]
    METRICS_TIME_RANGE_7D: _ClassVar[MetricsTimeRange]

DYNAMO_DB_BILLING_MODE_UNSPECIFIED: DynamoDBBillingMode
DYNAMO_DB_BILLING_MODE_PROVISIONED: DynamoDBBillingMode
DYNAMO_DB_BILLING_MODE_PAY_PER_REQUEST: DynamoDBBillingMode
METRICS_TIME_RANGE_UNSPECIFIED: MetricsTimeRange
METRICS_TIME_RANGE_1H: MetricsTimeRange
METRICS_TIME_RANGE_24H: MetricsTimeRange
METRICS_TIME_RANGE_7D: MetricsTimeRange

class DynamoDBConfig(_message.Message):
    __slots__ = (
        "table_name",
        "billing_mode",
        "provisioned_read_capacity_units",
        "provisioned_write_capacity_units",
        "item_count",
        "table_size_bytes",
        "region",
        "account_id",
        "table_status",
        "point_in_time_recovery_enabled",
        "pitr_earliest_restorable_at",
        "pitr_latest_restorable_at",
    )
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    BILLING_MODE_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_READ_CAPACITY_UNITS_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_WRITE_CAPACITY_UNITS_FIELD_NUMBER: _ClassVar[int]
    ITEM_COUNT_FIELD_NUMBER: _ClassVar[int]
    TABLE_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    TABLE_STATUS_FIELD_NUMBER: _ClassVar[int]
    POINT_IN_TIME_RECOVERY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PITR_EARLIEST_RESTORABLE_AT_FIELD_NUMBER: _ClassVar[int]
    PITR_LATEST_RESTORABLE_AT_FIELD_NUMBER: _ClassVar[int]
    table_name: str
    billing_mode: DynamoDBBillingMode
    provisioned_read_capacity_units: int
    provisioned_write_capacity_units: int
    item_count: int
    table_size_bytes: int
    region: str
    account_id: str
    table_status: str
    point_in_time_recovery_enabled: bool
    pitr_earliest_restorable_at: _timestamp_pb2.Timestamp
    pitr_latest_restorable_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        table_name: _Optional[str] = ...,
        billing_mode: _Optional[_Union[DynamoDBBillingMode, str]] = ...,
        provisioned_read_capacity_units: _Optional[int] = ...,
        provisioned_write_capacity_units: _Optional[int] = ...,
        item_count: _Optional[int] = ...,
        table_size_bytes: _Optional[int] = ...,
        region: _Optional[str] = ...,
        account_id: _Optional[str] = ...,
        table_status: _Optional[str] = ...,
        point_in_time_recovery_enabled: bool = ...,
        pitr_earliest_restorable_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        pitr_latest_restorable_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ElasticacheCluster(_message.Message):
    __slots__ = (
        "cluster_id",
        "description",
        "status",
        "engine",
        "engine_version",
        "node_type",
        "num_nodes",
        "num_shards",
        "replicas_per_shard",
        "region",
        "availability_zones",
        "multi_az_enabled",
        "automatic_failover_enabled",
        "at_rest_encryption_enabled",
        "transit_encryption_enabled",
        "cluster_enabled",
        "preferred_maintenance_window",
        "snapshot",
        "pending_modifications",
        "notification_topic_arn",
    )
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_NODES_FIELD_NUMBER: _ClassVar[int]
    NUM_SHARDS_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_PER_SHARD_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    AVAILABILITY_ZONES_FIELD_NUMBER: _ClassVar[int]
    MULTI_AZ_ENABLED_FIELD_NUMBER: _ClassVar[int]
    AUTOMATIC_FAILOVER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    AT_REST_ENCRYPTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TRANSIT_ENCRYPTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_MAINTENANCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    PENDING_MODIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_TOPIC_ARN_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    description: str
    status: str
    engine: str
    engine_version: str
    node_type: str
    num_nodes: int
    num_shards: int
    replicas_per_shard: int
    region: str
    availability_zones: _containers.RepeatedScalarFieldContainer[str]
    multi_az_enabled: bool
    automatic_failover_enabled: bool
    at_rest_encryption_enabled: bool
    transit_encryption_enabled: bool
    cluster_enabled: bool
    preferred_maintenance_window: str
    snapshot: ElasticacheSnapshotInfo
    pending_modifications: _containers.RepeatedScalarFieldContainer[str]
    notification_topic_arn: str
    def __init__(
        self,
        cluster_id: _Optional[str] = ...,
        description: _Optional[str] = ...,
        status: _Optional[str] = ...,
        engine: _Optional[str] = ...,
        engine_version: _Optional[str] = ...,
        node_type: _Optional[str] = ...,
        num_nodes: _Optional[int] = ...,
        num_shards: _Optional[int] = ...,
        replicas_per_shard: _Optional[int] = ...,
        region: _Optional[str] = ...,
        availability_zones: _Optional[_Iterable[str]] = ...,
        multi_az_enabled: bool = ...,
        automatic_failover_enabled: bool = ...,
        at_rest_encryption_enabled: bool = ...,
        transit_encryption_enabled: bool = ...,
        cluster_enabled: bool = ...,
        preferred_maintenance_window: _Optional[str] = ...,
        snapshot: _Optional[_Union[ElasticacheSnapshotInfo, _Mapping]] = ...,
        pending_modifications: _Optional[_Iterable[str]] = ...,
        notification_topic_arn: _Optional[str] = ...,
    ) -> None: ...

class ElasticacheSnapshotInfo(_message.Message):
    __slots__ = ("snapshot_window", "snapshot_retention_limit")
    SNAPSHOT_WINDOW_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_RETENTION_LIMIT_FIELD_NUMBER: _ClassVar[int]
    snapshot_window: str
    snapshot_retention_limit: int
    def __init__(
        self, snapshot_window: _Optional[str] = ..., snapshot_retention_limit: _Optional[int] = ...
    ) -> None: ...

class ElasticacheConfig(_message.Message):
    __slots__ = ("cluster_id", "node_type", "num_nodes", "engine", "engine_version", "region")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_NODES_FIELD_NUMBER: _ClassVar[int]
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    node_type: str
    num_nodes: int
    engine: str
    engine_version: str
    region: str
    def __init__(
        self,
        cluster_id: _Optional[str] = ...,
        node_type: _Optional[str] = ...,
        num_nodes: _Optional[int] = ...,
        engine: _Optional[str] = ...,
        engine_version: _Optional[str] = ...,
        region: _Optional[str] = ...,
    ) -> None: ...

class GetOnlineStoreConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetOnlineStoreConfigResponse(_message.Message):
    __slots__ = ("dynamodb", "elasticache")
    DYNAMODB_FIELD_NUMBER: _ClassVar[int]
    ELASTICACHE_FIELD_NUMBER: _ClassVar[int]
    dynamodb: DynamoDBConfig
    elasticache: ElasticacheConfig
    def __init__(
        self,
        dynamodb: _Optional[_Union[DynamoDBConfig, _Mapping]] = ...,
        elasticache: _Optional[_Union[ElasticacheConfig, _Mapping]] = ...,
    ) -> None: ...

class OnlineStoreUsageStat(_message.Message):
    __slots__ = ("namespace", "feature", "entity_count", "total_memory_bytes", "total_memory_bytes_history")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MEMORY_BYTES_HISTORY_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    feature: str
    entity_count: int
    total_memory_bytes: int
    total_memory_bytes_history: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        feature: _Optional[str] = ...,
        entity_count: _Optional[int] = ...,
        total_memory_bytes: _Optional[int] = ...,
        total_memory_bytes_history: _Optional[_Iterable[int]] = ...,
    ) -> None: ...

class GetOnlineStoreUsageStatsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetOnlineStoreUsageStatsResponse(_message.Message):
    __slots__ = ("stats", "collected_at")
    STATS_FIELD_NUMBER: _ClassVar[int]
    COLLECTED_AT_FIELD_NUMBER: _ClassVar[int]
    stats: _containers.RepeatedCompositeFieldContainer[OnlineStoreUsageStat]
    collected_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        stats: _Optional[_Iterable[_Union[OnlineStoreUsageStat, _Mapping]]] = ...,
        collected_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class OnlineStoreCleanupStat(_message.Message):
    __slots__ = ("key_type", "action_type", "name", "keys_affected", "items_removed", "keys_affected_history")
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KEYS_AFFECTED_FIELD_NUMBER: _ClassVar[int]
    ITEMS_REMOVED_FIELD_NUMBER: _ClassVar[int]
    KEYS_AFFECTED_HISTORY_FIELD_NUMBER: _ClassVar[int]
    key_type: str
    action_type: str
    name: str
    keys_affected: int
    items_removed: int
    keys_affected_history: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        key_type: _Optional[str] = ...,
        action_type: _Optional[str] = ...,
        name: _Optional[str] = ...,
        keys_affected: _Optional[int] = ...,
        items_removed: _Optional[int] = ...,
        keys_affected_history: _Optional[_Iterable[int]] = ...,
    ) -> None: ...

class GetOnlineStoreCleanupStatsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetOnlineStoreCleanupStatsResponse(_message.Message):
    __slots__ = ("stats", "collected_at", "script_task_id", "job_started_at")
    STATS_FIELD_NUMBER: _ClassVar[int]
    COLLECTED_AT_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    JOB_STARTED_AT_FIELD_NUMBER: _ClassVar[int]
    stats: _containers.RepeatedCompositeFieldContainer[OnlineStoreCleanupStat]
    collected_at: _timestamp_pb2.Timestamp
    script_task_id: str
    job_started_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        stats: _Optional[_Iterable[_Union[OnlineStoreCleanupStat, _Mapping]]] = ...,
        collected_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        script_task_id: _Optional[str] = ...,
        job_started_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetDynamoDBMetricsRequest(_message.Message):
    __slots__ = ("time_range",)
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    time_range: MetricsTimeRange
    def __init__(self, time_range: _Optional[_Union[MetricsTimeRange, str]] = ...) -> None: ...

class GetDynamoDBMetricsResponse(_message.Message):
    __slots__ = ("charts",)
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[_chart_pb2.Chart]
    def __init__(self, charts: _Optional[_Iterable[_Union[_chart_pb2.Chart, _Mapping]]] = ...) -> None: ...

class ListElasticacheClustersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListElasticacheClustersResponse(_message.Message):
    __slots__ = ("clusters", "region", "account_id")
    CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    clusters: _containers.RepeatedCompositeFieldContainer[ElasticacheCluster]
    region: str
    account_id: str
    def __init__(
        self,
        clusters: _Optional[_Iterable[_Union[ElasticacheCluster, _Mapping]]] = ...,
        region: _Optional[str] = ...,
        account_id: _Optional[str] = ...,
    ) -> None: ...

class GetElasticacheMetricsRequest(_message.Message):
    __slots__ = ("cluster_id", "time_range", "aggregate_nodes")
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_NODES_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    time_range: MetricsTimeRange
    aggregate_nodes: bool
    def __init__(
        self,
        cluster_id: _Optional[str] = ...,
        time_range: _Optional[_Union[MetricsTimeRange, str]] = ...,
        aggregate_nodes: bool = ...,
    ) -> None: ...

class GetElasticacheMetricsResponse(_message.Message):
    __slots__ = ("charts",)
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[_chart_pb2.Chart]
    def __init__(self, charts: _Optional[_Iterable[_Union[_chart_pb2.Chart, _Mapping]]] = ...) -> None: ...

class MemorystoreValkeyCluster(_message.Message):
    __slots__ = (
        "name",
        "cluster_id",
        "location",
        "state",
        "node_type",
        "shard_count",
        "replica_count",
        "node_count",
        "engine_version",
        "auth_mode",
        "transit_encryption_mode",
        "persistence_enabled",
        "persistence_mode",
        "maintenance_window",
        "upcoming_maintenance_at",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHARD_COUNT_FIELD_NUMBER: _ClassVar[int]
    REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    ENGINE_VERSION_FIELD_NUMBER: _ClassVar[int]
    AUTH_MODE_FIELD_NUMBER: _ClassVar[int]
    TRANSIT_ENCRYPTION_MODE_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    PERSISTENCE_MODE_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    UPCOMING_MAINTENANCE_AT_FIELD_NUMBER: _ClassVar[int]
    name: str
    cluster_id: str
    location: str
    state: str
    node_type: str
    shard_count: int
    replica_count: int
    node_count: int
    engine_version: str
    auth_mode: str
    transit_encryption_mode: str
    persistence_enabled: bool
    persistence_mode: str
    maintenance_window: str
    upcoming_maintenance_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        name: _Optional[str] = ...,
        cluster_id: _Optional[str] = ...,
        location: _Optional[str] = ...,
        state: _Optional[str] = ...,
        node_type: _Optional[str] = ...,
        shard_count: _Optional[int] = ...,
        replica_count: _Optional[int] = ...,
        node_count: _Optional[int] = ...,
        engine_version: _Optional[str] = ...,
        auth_mode: _Optional[str] = ...,
        transit_encryption_mode: _Optional[str] = ...,
        persistence_enabled: bool = ...,
        persistence_mode: _Optional[str] = ...,
        maintenance_window: _Optional[str] = ...,
        upcoming_maintenance_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ListMemorystoreValkeyClustersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMemorystoreValkeyClustersResponse(_message.Message):
    __slots__ = ("clusters", "project_id")
    CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    clusters: _containers.RepeatedCompositeFieldContainer[MemorystoreValkeyCluster]
    project_id: str
    def __init__(
        self,
        clusters: _Optional[_Iterable[_Union[MemorystoreValkeyCluster, _Mapping]]] = ...,
        project_id: _Optional[str] = ...,
    ) -> None: ...

class GetMemorystoreValkeyMetricsRequest(_message.Message):
    __slots__ = ("cluster_name", "time_range")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    time_range: MetricsTimeRange
    def __init__(
        self, cluster_name: _Optional[str] = ..., time_range: _Optional[_Union[MetricsTimeRange, str]] = ...
    ) -> None: ...

class GetMemorystoreValkeyMetricsResponse(_message.Message):
    __slots__ = ("charts",)
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[_chart_pb2.Chart]
    def __init__(self, charts: _Optional[_Iterable[_Union[_chart_pb2.Chart, _Mapping]]] = ...) -> None: ...
