from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

DYNAMO_DB_BILLING_MODE_UNSPECIFIED: DynamoDBBillingMode
DYNAMO_DB_BILLING_MODE_PROVISIONED: DynamoDBBillingMode
DYNAMO_DB_BILLING_MODE_PAY_PER_REQUEST: DynamoDBBillingMode

class DynamoDBConfig(_message.Message):
    __slots__ = (
        "table_name",
        "billing_mode",
        "provisioned_read_capacity_units",
        "provisioned_write_capacity_units",
        "item_count",
        "table_size_bytes",
        "region",
    )
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    BILLING_MODE_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_READ_CAPACITY_UNITS_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_WRITE_CAPACITY_UNITS_FIELD_NUMBER: _ClassVar[int]
    ITEM_COUNT_FIELD_NUMBER: _ClassVar[int]
    TABLE_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    table_name: str
    billing_mode: DynamoDBBillingMode
    provisioned_read_capacity_units: int
    provisioned_write_capacity_units: int
    item_count: int
    table_size_bytes: int
    region: str
    def __init__(
        self,
        table_name: _Optional[str] = ...,
        billing_mode: _Optional[_Union[DynamoDBBillingMode, str]] = ...,
        provisioned_read_capacity_units: _Optional[int] = ...,
        provisioned_write_capacity_units: _Optional[int] = ...,
        item_count: _Optional[int] = ...,
        table_size_bytes: _Optional[int] = ...,
        region: _Optional[str] = ...,
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
