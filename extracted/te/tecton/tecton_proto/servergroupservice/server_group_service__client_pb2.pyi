from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.auditlog import metadata__client_pb2 as _metadata__client_pb2
from tecton_proto.auth import service__client_pb2 as _service__client_pb2
from tecton_proto.common import server_group_status__client_pb2 as _server_group_status__client_pb2
from tecton_proto.common import server_group_type__client_pb2 as _server_group_type__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CREATING: Status
DELETING: Status
DESCRIPTOR: _descriptor.FileDescriptor
ERROR: Status
PENDING: Status
READY: Status
UNSPECIFIED: Status
UPDATING: Status

class AutoscalingConfig(_message.Message):
    __slots__ = ["max_nodes", "min_nodes"]
    MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    MIN_NODES_FIELD_NUMBER: _ClassVar[int]
    max_nodes: int
    min_nodes: int
    def __init__(self, min_nodes: _Optional[int] = ..., max_nodes: _Optional[int] = ...) -> None: ...

class CreateFeatureServerCacheRequest(_message.Message):
    __slots__ = ["metadata", "name", "preferred_maintenance_window", "provisioned_config", "workspace"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_MAINTENANCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    metadata: ResourceMetadata
    name: str
    preferred_maintenance_window: str
    provisioned_config: ProvisionedScalingCacheConfig
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingCacheConfig, _Mapping]] = ..., preferred_maintenance_window: _Optional[str] = ...) -> None: ...

class CreateFeatureServerGroupRequest(_message.Message):
    __slots__ = ["autoscaling_config", "cache_id", "metadata", "name", "node_type", "provisioned_config", "workspace"]
    AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CACHE_ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    autoscaling_config: AutoscalingConfig
    cache_id: str
    metadata: ResourceMetadata
    name: str
    node_type: str
    provisioned_config: ProvisionedScalingConfig
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., node_type: _Optional[str] = ..., cache_id: _Optional[str] = ...) -> None: ...

class CreateIngestServerGroupRequest(_message.Message):
    __slots__ = ["autoscaling_config", "metadata", "name", "node_type", "provisioned_config", "workspace"]
    AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    autoscaling_config: AutoscalingConfig
    metadata: ResourceMetadata
    name: str
    node_type: str
    provisioned_config: ProvisionedScalingConfig
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., node_type: _Optional[str] = ...) -> None: ...

class CreateTransformServerGroupRequest(_message.Message):
    __slots__ = ["autoscaling_config", "environment", "environment_variables", "metadata", "name", "node_type", "provisioned_config", "workspace"]
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    autoscaling_config: AutoscalingConfig
    environment: str
    environment_variables: _containers.ScalarMap[str, str]
    metadata: ResourceMetadata
    name: str
    node_type: str
    provisioned_config: ProvisionedScalingConfig
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., name: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., node_type: _Optional[str] = ..., environment: _Optional[str] = ..., environment_variables: _Optional[_Mapping[str, str]] = ...) -> None: ...

class DeleteFeatureServerCacheRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteFeatureServerCacheResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteFeatureServerGroupRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteFeatureServerGroupResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteIngestServerGroupRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteIngestServerGroupResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeleteTransformServerGroupRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteTransformServerGroupResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class FeatureServerCache(_message.Message):
    __slots__ = ["created_at", "id", "metadata", "name", "pending_config", "preferred_maintenance_window", "provisioned_config", "status", "status_details", "updated_at", "workspace"]
    class PendingConfig(_message.Message):
        __slots__ = ["preferred_maintenance_window", "provisioned_config"]
        PREFERRED_MAINTENANCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
        PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
        preferred_maintenance_window: str
        provisioned_config: ProvisionedScalingCacheConfig
        def __init__(self, provisioned_config: _Optional[_Union[ProvisionedScalingCacheConfig, _Mapping]] = ..., preferred_maintenance_window: _Optional[str] = ...) -> None: ...
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PENDING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_MAINTENANCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    id: str
    metadata: ResourceMetadata
    name: str
    pending_config: FeatureServerCache.PendingConfig
    preferred_maintenance_window: str
    provisioned_config: ProvisionedScalingCacheConfig
    status: Status
    status_details: str
    updated_at: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., name: _Optional[str] = ..., id: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., status: _Optional[_Union[Status, str]] = ..., status_details: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingCacheConfig, _Mapping]] = ..., preferred_maintenance_window: _Optional[str] = ..., pending_config: _Optional[_Union[FeatureServerCache.PendingConfig, _Mapping]] = ...) -> None: ...

class FeatureServerGroup(_message.Message):
    __slots__ = ["autoscaling_config", "cache_id", "created_at", "id", "metadata", "name", "node_type", "pending_config", "provisioned_config", "status", "status_details", "updated_at", "workspace"]
    class PendingConfig(_message.Message):
        __slots__ = ["autoscaling_config", "cache_id", "node_type", "provisioned_config"]
        AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
        CACHE_ID_FIELD_NUMBER: _ClassVar[int]
        NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
        PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
        autoscaling_config: AutoscalingConfig
        cache_id: str
        node_type: str
        provisioned_config: ProvisionedScalingConfig
        def __init__(self, autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., node_type: _Optional[str] = ..., cache_id: _Optional[str] = ...) -> None: ...
    AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CACHE_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PENDING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    autoscaling_config: AutoscalingConfig
    cache_id: str
    created_at: _timestamp_pb2.Timestamp
    id: str
    metadata: ResourceMetadata
    name: str
    node_type: str
    pending_config: FeatureServerGroup.PendingConfig
    provisioned_config: ProvisionedScalingConfig
    status: Status
    status_details: str
    updated_at: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., name: _Optional[str] = ..., id: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., status: _Optional[_Union[Status, str]] = ..., status_details: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., node_type: _Optional[str] = ..., cache_id: _Optional[str] = ..., pending_config: _Optional[_Union[FeatureServerGroup.PendingConfig, _Mapping]] = ...) -> None: ...

class GetFeatureServerCacheRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetFeatureServerGroupRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetIngestServerGroupRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetRealtimeLogsRequest(_message.Message):
    __slots__ = ["end", "start", "tail_log_count", "transform_server_group_id"]
    END_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    TAIL_LOG_COUNT_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_SERVER_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    end: _timestamp_pb2.Timestamp
    start: _timestamp_pb2.Timestamp
    tail_log_count: int
    transform_server_group_id: str
    def __init__(self, transform_server_group_id: _Optional[str] = ..., start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., tail_log_count: _Optional[int] = ...) -> None: ...

class GetRealtimeLogsResponse(_message.Message):
    __slots__ = ["logs", "warnings"]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[RealtimeLog]
    warnings: str
    def __init__(self, logs: _Optional[_Iterable[_Union[RealtimeLog, _Mapping]]] = ..., warnings: _Optional[str] = ...) -> None: ...

class GetServerGroupRequest(_message.Message):
    __slots__ = ["server_group_name", "workspace"]
    SERVER_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    server_group_name: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., server_group_name: _Optional[str] = ...) -> None: ...

class GetServerGroupResponse(_message.Message):
    __slots__ = ["server_group"]
    SERVER_GROUP_FIELD_NUMBER: _ClassVar[int]
    server_group: ServerGroupInfo
    def __init__(self, server_group: _Optional[_Union[ServerGroupInfo, _Mapping]] = ...) -> None: ...

class GetTransformServerGroupRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class IngestServerGroup(_message.Message):
    __slots__ = ["autoscaling_config", "created_at", "id", "metadata", "name", "node_type", "pending_config", "provisioned_config", "status", "status_details", "updated_at", "workspace"]
    class PendingConfig(_message.Message):
        __slots__ = ["autoscaling_config", "node_type", "provisioned_config"]
        AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
        NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
        PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
        autoscaling_config: AutoscalingConfig
        node_type: str
        provisioned_config: ProvisionedScalingConfig
        def __init__(self, autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., node_type: _Optional[str] = ...) -> None: ...
    AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PENDING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    autoscaling_config: AutoscalingConfig
    created_at: _timestamp_pb2.Timestamp
    id: str
    metadata: ResourceMetadata
    name: str
    node_type: str
    pending_config: IngestServerGroup.PendingConfig
    provisioned_config: ProvisionedScalingConfig
    status: Status
    status_details: str
    updated_at: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., name: _Optional[str] = ..., id: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., status: _Optional[_Union[Status, str]] = ..., status_details: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., node_type: _Optional[str] = ..., pending_config: _Optional[_Union[IngestServerGroup.PendingConfig, _Mapping]] = ...) -> None: ...

class ListFeatureServerCachesRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    def __init__(self, workspace: _Optional[str] = ...) -> None: ...

class ListFeatureServerCachesResponse(_message.Message):
    __slots__ = ["feature_server_caches"]
    FEATURE_SERVER_CACHES_FIELD_NUMBER: _ClassVar[int]
    feature_server_caches: _containers.RepeatedCompositeFieldContainer[FeatureServerCache]
    def __init__(self, feature_server_caches: _Optional[_Iterable[_Union[FeatureServerCache, _Mapping]]] = ...) -> None: ...

class ListFeatureServerGroupsRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    def __init__(self, workspace: _Optional[str] = ...) -> None: ...

class ListFeatureServerGroupsResponse(_message.Message):
    __slots__ = ["feature_server_groups"]
    FEATURE_SERVER_GROUPS_FIELD_NUMBER: _ClassVar[int]
    feature_server_groups: _containers.RepeatedCompositeFieldContainer[FeatureServerGroup]
    def __init__(self, feature_server_groups: _Optional[_Iterable[_Union[FeatureServerGroup, _Mapping]]] = ...) -> None: ...

class ListIngestServerGroupsRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    def __init__(self, workspace: _Optional[str] = ...) -> None: ...

class ListIngestServerGroupsResponse(_message.Message):
    __slots__ = ["ingest_server_groups"]
    INGEST_SERVER_GROUPS_FIELD_NUMBER: _ClassVar[int]
    ingest_server_groups: _containers.RepeatedCompositeFieldContainer[IngestServerGroup]
    def __init__(self, ingest_server_groups: _Optional[_Iterable[_Union[IngestServerGroup, _Mapping]]] = ...) -> None: ...

class ListServerGroupsRequest(_message.Message):
    __slots__ = ["type", "workspace"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    type: _server_group_type__client_pb2.ServerGroupType
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., type: _Optional[_Union[_server_group_type__client_pb2.ServerGroupType, str]] = ...) -> None: ...

class ListServerGroupsResponse(_message.Message):
    __slots__ = ["server_groups"]
    SERVER_GROUPS_FIELD_NUMBER: _ClassVar[int]
    server_groups: _containers.RepeatedCompositeFieldContainer[ServerGroupInfo]
    def __init__(self, server_groups: _Optional[_Iterable[_Union[ServerGroupInfo, _Mapping]]] = ...) -> None: ...

class ListTransformServerGroupsRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    def __init__(self, workspace: _Optional[str] = ...) -> None: ...

class ListTransformServerGroupsResponse(_message.Message):
    __slots__ = ["transform_server_groups"]
    TRANSFORM_SERVER_GROUPS_FIELD_NUMBER: _ClassVar[int]
    transform_server_groups: _containers.RepeatedCompositeFieldContainer[TransformServerGroup]
    def __init__(self, transform_server_groups: _Optional[_Iterable[_Union[TransformServerGroup, _Mapping]]] = ...) -> None: ...

class ProvisionedScalingCacheConfig(_message.Message):
    __slots__ = ["num_replicas_per_shard", "num_shards"]
    NUM_REPLICAS_PER_SHARD_FIELD_NUMBER: _ClassVar[int]
    NUM_SHARDS_FIELD_NUMBER: _ClassVar[int]
    num_replicas_per_shard: int
    num_shards: int
    def __init__(self, num_shards: _Optional[int] = ..., num_replicas_per_shard: _Optional[int] = ...) -> None: ...

class ProvisionedScalingConfig(_message.Message):
    __slots__ = ["desired_nodes"]
    DESIRED_NODES_FIELD_NUMBER: _ClassVar[int]
    desired_nodes: int
    def __init__(self, desired_nodes: _Optional[int] = ...) -> None: ...

class RealtimeLog(_message.Message):
    __slots__ = ["message", "node", "timestamp"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    message: str
    node: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., message: _Optional[str] = ..., node: _Optional[str] = ...) -> None: ...

class ResourceMetadata(_message.Message):
    __slots__ = ["description", "owner", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    description: str
    owner: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, description: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ..., owner: _Optional[str] = ...) -> None: ...

class ServerGroupInfo(_message.Message):
    __slots__ = ["created_at", "current_config", "description", "desired_config", "environment", "last_modified_by", "name", "owner", "server_group_id", "status", "status_details", "tags", "type"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CURRENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DESIRED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_BY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    created_at: _timestamp_pb2.Timestamp
    current_config: ServerGroupScalingConfig
    description: str
    desired_config: ServerGroupScalingConfig
    environment: str
    last_modified_by: str
    name: str
    owner: str
    server_group_id: str
    status: _server_group_status__client_pb2.ServerGroupStatus
    status_details: str
    tags: _containers.ScalarMap[str, str]
    type: _server_group_type__client_pb2.ServerGroupType
    def __init__(self, server_group_id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[_server_group_type__client_pb2.ServerGroupType, str]] = ..., description: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., owner: _Optional[str] = ..., last_modified_by: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ..., desired_config: _Optional[_Union[ServerGroupScalingConfig, _Mapping]] = ..., current_config: _Optional[_Union[ServerGroupScalingConfig, _Mapping]] = ..., status: _Optional[_Union[_server_group_status__client_pb2.ServerGroupStatus, str]] = ..., status_details: _Optional[str] = ..., environment: _Optional[str] = ...) -> None: ...

class ServerGroupScalingConfig(_message.Message):
    __slots__ = ["autoscaling_enabled", "desired_nodes", "last_updated_at", "max_nodes", "min_nodes", "workspace_state_id"]
    AUTOSCALING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DESIRED_NODES_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    MIN_NODES_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    autoscaling_enabled: bool
    desired_nodes: int
    last_updated_at: _timestamp_pb2.Timestamp
    max_nodes: int
    min_nodes: int
    workspace_state_id: str
    def __init__(self, min_nodes: _Optional[int] = ..., max_nodes: _Optional[int] = ..., desired_nodes: _Optional[int] = ..., autoscaling_enabled: bool = ..., last_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., workspace_state_id: _Optional[str] = ...) -> None: ...

class TestOnlyCreateTransformServerGroupRequest(_message.Message):
    __slots__ = ["desired_nodes", "environment", "name", "workspace"]
    DESIRED_NODES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    desired_nodes: int
    environment: str
    name: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., name: _Optional[str] = ..., environment: _Optional[str] = ..., desired_nodes: _Optional[int] = ...) -> None: ...

class TestOnlyCreateTransformServerGroupResponse(_message.Message):
    __slots__ = ["transform_server_group"]
    TRANSFORM_SERVER_GROUP_FIELD_NUMBER: _ClassVar[int]
    transform_server_group: TransformServerGroup
    def __init__(self, transform_server_group: _Optional[_Union[TransformServerGroup, _Mapping]] = ...) -> None: ...

class TestOnlyDeleteAllServerStatesRequest(_message.Message):
    __slots__ = ["workspace"]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    workspace: str
    def __init__(self, workspace: _Optional[str] = ...) -> None: ...

class TestOnlyDeleteAllServerStatesResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TestOnlyUpdateServerStateRequest(_message.Message):
    __slots__ = ["server_group_name", "workspace"]
    SERVER_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    server_group_name: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., server_group_name: _Optional[str] = ...) -> None: ...

class TestOnlyUpdateServerStateResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TransformServerGroup(_message.Message):
    __slots__ = ["autoscaling_config", "created_at", "environment", "environment_variables", "id", "metadata", "name", "node_type", "pending_config", "provisioned_config", "status", "status_details", "updated_at", "workspace"]
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class PendingConfig(_message.Message):
        __slots__ = ["autoscaling_config", "environment", "environment_variables", "node_type", "provisioned_config"]
        class EnvironmentVariablesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
        ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
        ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
        NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
        PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
        autoscaling_config: AutoscalingConfig
        environment: str
        environment_variables: _containers.ScalarMap[str, str]
        node_type: str
        provisioned_config: ProvisionedScalingConfig
        def __init__(self, autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., environment: _Optional[str] = ..., environment_variables: _Optional[_Mapping[str, str]] = ..., node_type: _Optional[str] = ...) -> None: ...
    AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PENDING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    autoscaling_config: AutoscalingConfig
    created_at: _timestamp_pb2.Timestamp
    environment: str
    environment_variables: _containers.ScalarMap[str, str]
    id: str
    metadata: ResourceMetadata
    name: str
    node_type: str
    pending_config: TransformServerGroup.PendingConfig
    provisioned_config: ProvisionedScalingConfig
    status: Status
    status_details: str
    updated_at: _timestamp_pb2.Timestamp
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., name: _Optional[str] = ..., id: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., status: _Optional[_Union[Status, str]] = ..., status_details: _Optional[str] = ..., node_type: _Optional[str] = ..., environment: _Optional[str] = ..., environment_variables: _Optional[_Mapping[str, str]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., pending_config: _Optional[_Union[TransformServerGroup.PendingConfig, _Mapping]] = ...) -> None: ...

class UpdateFeatureServerCacheRequest(_message.Message):
    __slots__ = ["id", "metadata", "preferred_maintenance_window", "provisioned_config"]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    PREFERRED_MAINTENANCE_WINDOW_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    id: str
    metadata: ResourceMetadata
    preferred_maintenance_window: str
    provisioned_config: ProvisionedScalingCacheConfig
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingCacheConfig, _Mapping]] = ..., preferred_maintenance_window: _Optional[str] = ...) -> None: ...

class UpdateFeatureServerGroupRequest(_message.Message):
    __slots__ = ["autoscaling_config", "cache_id", "id", "metadata", "node_type", "provisioned_config"]
    AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CACHE_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    autoscaling_config: AutoscalingConfig
    cache_id: str
    id: str
    metadata: ResourceMetadata
    node_type: str
    provisioned_config: ProvisionedScalingConfig
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., node_type: _Optional[str] = ..., cache_id: _Optional[str] = ...) -> None: ...

class UpdateIngestServerGroupRequest(_message.Message):
    __slots__ = ["autoscaling_config", "id", "metadata", "node_type", "provisioned_config"]
    AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    autoscaling_config: AutoscalingConfig
    id: str
    metadata: ResourceMetadata
    node_type: str
    provisioned_config: ProvisionedScalingConfig
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., node_type: _Optional[str] = ...) -> None: ...

class UpdateTransformServerGroupRequest(_message.Message):
    __slots__ = ["autoscaling_config", "environment", "environment_variables", "id", "metadata", "node_type", "provisioned_config"]
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    AUTOSCALING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROVISIONED_CONFIG_FIELD_NUMBER: _ClassVar[int]
    autoscaling_config: AutoscalingConfig
    environment: str
    environment_variables: _containers.ScalarMap[str, str]
    id: str
    metadata: ResourceMetadata
    node_type: str
    provisioned_config: ProvisionedScalingConfig
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Union[ResourceMetadata, _Mapping]] = ..., autoscaling_config: _Optional[_Union[AutoscalingConfig, _Mapping]] = ..., provisioned_config: _Optional[_Union[ProvisionedScalingConfig, _Mapping]] = ..., node_type: _Optional[str] = ..., environment: _Optional[str] = ..., environment_variables: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
