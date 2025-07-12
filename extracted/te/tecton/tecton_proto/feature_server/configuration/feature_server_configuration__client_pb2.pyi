from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.args import pipeline__client_pb2 as _pipeline__client_pb2
from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.auth import acl__client_pb2 as _acl__client_pb2
from tecton_proto.common import aggregation_function__client_pb2 as _aggregation_function__client_pb2
from tecton_proto.common import calculation_node__client_pb2 as _calculation_node__client_pb2
from tecton_proto.common import data_type__client_pb2 as _data_type__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import time_window__client_pb2 as _time_window__client_pb2
from tecton_proto.data import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.data import feature_view__client_pb2 as _feature_view__client_pb2_1
from tecton_proto.data import realtime_compute__client_pb2 as _realtime_compute__client_pb2
from tecton_proto.data import tecton_api_key__client_pb2 as _tecton_api_key__client_pb2
from tecton_proto.data import transformation__client_pb2 as _transformation__client_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DATA_TABLE_TIMESTAMP_TYPE_ATTRIBUTE: DataTableTimestampType
DATA_TABLE_TIMESTAMP_TYPE_SORT_KEY: DataTableTimestampType
DATA_TABLE_TIMESTAMP_TYPE_UNKNOWN: DataTableTimestampType
DESCRIPTOR: _descriptor.FileDescriptor
STATUS_TABLE_TIMESTAMP_CONTINUOUS_AGGREGATE: StatusTableTimestampType
STATUS_TABLE_TIMESTAMP_TYPE_ATTRIBUTE: StatusTableTimestampType
STATUS_TABLE_TIMESTAMP_TYPE_SORT_KEY: StatusTableTimestampType
STATUS_TABLE_TIMESTAMP_TYPE_UNKNOWN: StatusTableTimestampType

class CacheConnectionConfiguration(_message.Message):
    __slots__ = ["cache_name", "elasticache_valkey", "workspace_name"]
    class ElasticacheValkey(_message.Message):
        __slots__ = ["aws_sm_key", "primary_endpoint"]
        AWS_SM_KEY_FIELD_NUMBER: _ClassVar[int]
        PRIMARY_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
        aws_sm_key: str
        primary_endpoint: str
        def __init__(self, primary_endpoint: _Optional[str] = ..., aws_sm_key: _Optional[str] = ...) -> None: ...
    CACHE_NAME_FIELD_NUMBER: _ClassVar[int]
    ELASTICACHE_VALKEY_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    cache_name: str
    elasticache_valkey: CacheConnectionConfiguration.ElasticacheValkey
    workspace_name: str
    def __init__(self, workspace_name: _Optional[str] = ..., cache_name: _Optional[str] = ..., elasticache_valkey: _Optional[_Union[CacheConnectionConfiguration.ElasticacheValkey, _Mapping]] = ...) -> None: ...

class CacheGroup(_message.Message):
    __slots__ = ["feature_view_ids", "join_keys", "key_jitter", "key_ttl", "name"]
    FEATURE_VIEW_IDS_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    KEY_JITTER_FIELD_NUMBER: _ClassVar[int]
    KEY_TTL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    feature_view_ids: _containers.RepeatedScalarFieldContainer[str]
    join_keys: _containers.RepeatedScalarFieldContainer[str]
    key_jitter: _duration_pb2.Duration
    key_ttl: _duration_pb2.Duration
    name: str
    def __init__(self, name: _Optional[str] = ..., join_keys: _Optional[_Iterable[str]] = ..., key_ttl: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., key_jitter: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., feature_view_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class CacheParams(_message.Message):
    __slots__ = ["redis"]
    REDIS_FIELD_NUMBER: _ClassVar[int]
    redis: _feature_view__client_pb2_1.RedisOnlineStore
    def __init__(self, redis: _Optional[_Union[_feature_view__client_pb2_1.RedisOnlineStore, _Mapping]] = ...) -> None: ...

class CanaryConfig(_message.Message):
    __slots__ = ["feature_server_canary_follower_endpoint", "feature_server_canary_id", "feature_server_canary_pod_name"]
    FEATURE_SERVER_CANARY_FOLLOWER_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVER_CANARY_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVER_CANARY_POD_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_server_canary_follower_endpoint: str
    feature_server_canary_id: str
    feature_server_canary_pod_name: str
    def __init__(self, feature_server_canary_id: _Optional[str] = ..., feature_server_canary_pod_name: _Optional[str] = ..., feature_server_canary_follower_endpoint: _Optional[str] = ...) -> None: ...

class Column(_message.Message):
    __slots__ = ["abstract_syntax_tree_root", "batch_table_feature_view_index", "data_type", "description", "feature_service_space_name", "feature_view_index", "feature_view_space_name", "input_column_name", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ABSTRACT_SYNTAX_TREE_ROOT_FIELD_NUMBER: _ClassVar[int]
    BATCH_TABLE_FEATURE_VIEW_INDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_SPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_INDEX_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_SPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    abstract_syntax_tree_root: _calculation_node__client_pb2.AbstractSyntaxTreeNode
    batch_table_feature_view_index: int
    data_type: _data_type__client_pb2.DataType
    description: str
    feature_service_space_name: str
    feature_view_index: int
    feature_view_space_name: str
    input_column_name: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, data_type: _Optional[_Union[_data_type__client_pb2.DataType, _Mapping]] = ..., feature_view_space_name: _Optional[str] = ..., feature_service_space_name: _Optional[str] = ..., feature_view_index: _Optional[int] = ..., batch_table_feature_view_index: _Optional[int] = ..., description: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ..., abstract_syntax_tree_root: _Optional[_Union[_calculation_node__client_pb2.AbstractSyntaxTreeNode, _Mapping]] = ..., input_column_name: _Optional[str] = ...) -> None: ...

class CompactTransformation(_message.Message):
    __slots__ = ["transformation_id", "transformation_mode", "user_defined_function_id"]
    TRANSFORMATION_ID_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_MODE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
    transformation_id: _id__client_pb2.Id
    transformation_mode: _transformation__client_pb2.TransformationMode
    user_defined_function_id: str
    def __init__(self, transformation_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., transformation_mode: _Optional[_Union[_transformation__client_pb2.TransformationMode, str]] = ..., user_defined_function_id: _Optional[str] = ...) -> None: ...

class FeaturePlan(_message.Message):
    __slots__ = ["aggregation_function", "aggregation_function_params", "aggregation_leading_edge_mode", "aggregation_secondary_key", "aggregation_window", "batch_table_name", "batch_table_window_index", "cache_index", "data_table_timestamp_type", "deletionTimeWindow", "feature_set_column_hash", "feature_store_format_version", "feature_view_cache_config", "feature_view_id", "feature_view_name", "input_columns", "is_compacted_feature_view", "is_secondary_key_output", "join_keys", "online_store_params", "output_column", "refresh_status_table", "serving_ttl", "slide_period", "status_table_timestamp_type", "stream_table_name", "table_format_version", "table_name", "tiles", "time_window", "timestamp_key", "wildcard_join_keys"]
    AGGREGATION_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FUNCTION_PARAMS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_LEADING_EDGE_MODE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_SECONDARY_KEY_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_WINDOW_FIELD_NUMBER: _ClassVar[int]
    BATCH_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    BATCH_TABLE_WINDOW_INDEX_FIELD_NUMBER: _ClassVar[int]
    CACHE_INDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_TABLE_TIMESTAMP_TYPE_FIELD_NUMBER: _ClassVar[int]
    DELETIONTIMEWINDOW_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SET_COLUMN_HASH_FIELD_NUMBER: _ClassVar[int]
    FEATURE_STORE_FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_CACHE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    IS_COMPACTED_FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    IS_SECONDARY_KEY_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    ONLINE_STORE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_COLUMN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_STATUS_TABLE_FIELD_NUMBER: _ClassVar[int]
    SERVING_TTL_FIELD_NUMBER: _ClassVar[int]
    SLIDE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    STATUS_TABLE_TIMESTAMP_TYPE_FIELD_NUMBER: _ClassVar[int]
    STREAM_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    TABLE_FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    TILES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_KEY_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    WILDCARD_JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    aggregation_function: _aggregation_function__client_pb2.AggregationFunction
    aggregation_function_params: _aggregation_function__client_pb2.AggregationFunctionParams
    aggregation_leading_edge_mode: _feature_view__client_pb2.AggregationLeadingEdge
    aggregation_secondary_key: Column
    aggregation_window: _duration_pb2.Duration
    batch_table_name: str
    batch_table_window_index: int
    cache_index: int
    data_table_timestamp_type: DataTableTimestampType
    deletionTimeWindow: int
    feature_set_column_hash: str
    feature_store_format_version: int
    feature_view_cache_config: _feature_view__client_pb2_1.FeatureViewCacheConfig
    feature_view_id: str
    feature_view_name: str
    input_columns: _containers.RepeatedCompositeFieldContainer[Column]
    is_compacted_feature_view: bool
    is_secondary_key_output: bool
    join_keys: _containers.RepeatedCompositeFieldContainer[Column]
    online_store_params: _feature_view__client_pb2_1.OnlineStoreParams
    output_column: Column
    refresh_status_table: bool
    serving_ttl: _duration_pb2.Duration
    slide_period: _duration_pb2.Duration
    status_table_timestamp_type: StatusTableTimestampType
    stream_table_name: str
    table_format_version: int
    table_name: str
    tiles: _containers.RepeatedCompositeFieldContainer[_schema__client_pb2.OnlineBatchTablePartTile]
    time_window: _time_window__client_pb2.TimeWindow
    timestamp_key: str
    wildcard_join_keys: _containers.RepeatedCompositeFieldContainer[Column]
    def __init__(self, output_column: _Optional[_Union[Column, _Mapping]] = ..., input_columns: _Optional[_Iterable[_Union[Column, _Mapping]]] = ..., aggregation_function: _Optional[_Union[_aggregation_function__client_pb2.AggregationFunction, str]] = ..., aggregation_function_params: _Optional[_Union[_aggregation_function__client_pb2.AggregationFunctionParams, _Mapping]] = ..., aggregation_window: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., join_keys: _Optional[_Iterable[_Union[Column, _Mapping]]] = ..., wildcard_join_keys: _Optional[_Iterable[_Union[Column, _Mapping]]] = ..., aggregation_secondary_key: _Optional[_Union[Column, _Mapping]] = ..., is_secondary_key_output: bool = ..., table_name: _Optional[str] = ..., data_table_timestamp_type: _Optional[_Union[DataTableTimestampType, str]] = ..., status_table_timestamp_type: _Optional[_Union[StatusTableTimestampType, str]] = ..., timestamp_key: _Optional[str] = ..., slide_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., serving_ttl: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., refresh_status_table: bool = ..., feature_view_name: _Optional[str] = ..., feature_view_id: _Optional[str] = ..., feature_store_format_version: _Optional[int] = ..., online_store_params: _Optional[_Union[_feature_view__client_pb2_1.OnlineStoreParams, _Mapping]] = ..., deletionTimeWindow: _Optional[int] = ..., time_window: _Optional[_Union[_time_window__client_pb2.TimeWindow, _Mapping]] = ..., feature_view_cache_config: _Optional[_Union[_feature_view__client_pb2_1.FeatureViewCacheConfig, _Mapping]] = ..., cache_index: _Optional[int] = ..., table_format_version: _Optional[int] = ..., batch_table_name: _Optional[str] = ..., batch_table_window_index: _Optional[int] = ..., stream_table_name: _Optional[str] = ..., tiles: _Optional[_Iterable[_Union[_schema__client_pb2.OnlineBatchTablePartTile, _Mapping]]] = ..., is_compacted_feature_view: bool = ..., feature_set_column_hash: _Optional[str] = ..., aggregation_leading_edge_mode: _Optional[_Union[_feature_view__client_pb2.AggregationLeadingEdge, str]] = ...) -> None: ...

class FeatureServerConfiguration(_message.Message):
    __slots__ = ["all_online_compute_configs", "all_online_store_params", "authorized_api_keys", "cache_connection_configurations", "cache_groups", "computed_time", "feature_server_canary_config", "feature_service_acls", "feature_services", "global_table_config_by_name", "jwks", "remote_compute_configs", "user_defined_function_map", "workspace_acls"]
    class CacheConnectionConfigurationsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: CacheConnectionConfiguration
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CacheConnectionConfiguration, _Mapping]] = ...) -> None: ...
    class CacheGroupsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: CacheGroup
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CacheGroup, _Mapping]] = ...) -> None: ...
    class GlobalTableConfigByNameEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GlobalTableConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[GlobalTableConfig, _Mapping]] = ...) -> None: ...
    class JwksEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Jwk
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Jwk, _Mapping]] = ...) -> None: ...
    class UserDefinedFunctionMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _user_defined_function__client_pb2.UserDefinedFunction
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ...) -> None: ...
    ALL_ONLINE_COMPUTE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    ALL_ONLINE_STORE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    AUTHORIZED_API_KEYS_FIELD_NUMBER: _ClassVar[int]
    CACHE_CONNECTION_CONFIGURATIONS_FIELD_NUMBER: _ClassVar[int]
    CACHE_GROUPS_FIELD_NUMBER: _ClassVar[int]
    COMPUTED_TIME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVER_CANARY_CONFIG_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_ACLS_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_TABLE_CONFIG_BY_NAME_FIELD_NUMBER: _ClassVar[int]
    JWKS_FIELD_NUMBER: _ClassVar[int]
    REMOTE_COMPUTE_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_FUNCTION_MAP_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ACLS_FIELD_NUMBER: _ClassVar[int]
    all_online_compute_configs: _containers.RepeatedCompositeFieldContainer[_realtime_compute__client_pb2.OnlineComputeConfig]
    all_online_store_params: _containers.RepeatedCompositeFieldContainer[_feature_view__client_pb2_1.OnlineStoreParams]
    authorized_api_keys: _containers.RepeatedCompositeFieldContainer[_tecton_api_key__client_pb2.TectonApiKey]
    cache_connection_configurations: _containers.MessageMap[str, CacheConnectionConfiguration]
    cache_groups: _containers.MessageMap[str, CacheGroup]
    computed_time: _timestamp_pb2.Timestamp
    feature_server_canary_config: CanaryConfig
    feature_service_acls: _containers.RepeatedCompositeFieldContainer[FeatureServiceAcls]
    feature_services: _containers.RepeatedCompositeFieldContainer[FeatureServicePlan]
    global_table_config_by_name: _containers.MessageMap[str, GlobalTableConfig]
    jwks: _containers.MessageMap[str, Jwk]
    remote_compute_configs: _containers.RepeatedCompositeFieldContainer[_realtime_compute__client_pb2.RemoteFunctionComputeConfig]
    user_defined_function_map: _containers.MessageMap[str, _user_defined_function__client_pb2.UserDefinedFunction]
    workspace_acls: _containers.RepeatedCompositeFieldContainer[WorkspaceAcls]
    def __init__(self, computed_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., feature_services: _Optional[_Iterable[_Union[FeatureServicePlan, _Mapping]]] = ..., global_table_config_by_name: _Optional[_Mapping[str, GlobalTableConfig]] = ..., authorized_api_keys: _Optional[_Iterable[_Union[_tecton_api_key__client_pb2.TectonApiKey, _Mapping]]] = ..., feature_service_acls: _Optional[_Iterable[_Union[FeatureServiceAcls, _Mapping]]] = ..., workspace_acls: _Optional[_Iterable[_Union[WorkspaceAcls, _Mapping]]] = ..., all_online_store_params: _Optional[_Iterable[_Union[_feature_view__client_pb2_1.OnlineStoreParams, _Mapping]]] = ..., feature_server_canary_config: _Optional[_Union[CanaryConfig, _Mapping]] = ..., remote_compute_configs: _Optional[_Iterable[_Union[_realtime_compute__client_pb2.RemoteFunctionComputeConfig, _Mapping]]] = ..., all_online_compute_configs: _Optional[_Iterable[_Union[_realtime_compute__client_pb2.OnlineComputeConfig, _Mapping]]] = ..., cache_groups: _Optional[_Mapping[str, CacheGroup]] = ..., cache_connection_configurations: _Optional[_Mapping[str, CacheConnectionConfiguration]] = ..., user_defined_function_map: _Optional[_Mapping[str, _user_defined_function__client_pb2.UserDefinedFunction]] = ..., jwks: _Optional[_Mapping[str, Jwk]] = ...) -> None: ...

class FeatureServiceAcls(_message.Message):
    __slots__ = ["acls", "feature_service_id"]
    ACLS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    acls: _containers.RepeatedCompositeFieldContainer[_acl__client_pb2.Acl]
    feature_service_id: _id__client_pb2.Id
    def __init__(self, feature_service_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., acls: _Optional[_Iterable[_Union[_acl__client_pb2.Acl, _Mapping]]] = ...) -> None: ...

class FeatureServiceCachePlan(_message.Message):
    __slots__ = ["cache_group_name", "feature_set_column_hashes", "feature_view_ids", "remapped_join_key_lists"]
    CACHE_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SET_COLUMN_HASHES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_IDS_FIELD_NUMBER: _ClassVar[int]
    REMAPPED_JOIN_KEY_LISTS_FIELD_NUMBER: _ClassVar[int]
    cache_group_name: str
    feature_set_column_hashes: _containers.RepeatedScalarFieldContainer[str]
    feature_view_ids: _containers.RepeatedScalarFieldContainer[str]
    remapped_join_key_lists: _containers.RepeatedCompositeFieldContainer[RemappedJoinKeys]
    def __init__(self, feature_view_ids: _Optional[_Iterable[str]] = ..., cache_group_name: _Optional[str] = ..., remapped_join_key_lists: _Optional[_Iterable[_Union[RemappedJoinKeys, _Mapping]]] = ..., feature_set_column_hashes: _Optional[_Iterable[str]] = ...) -> None: ...

class FeatureServicePlan(_message.Message):
    __slots__ = ["cache_plans", "feature_service_id", "feature_service_name", "feature_view_id", "feature_view_name", "features_plans", "join_key_template", "logging_config", "realtime_environment", "workspace_name", "workspace_state_id"]
    CACHE_PLANS_FIELD_NUMBER: _ClassVar[int]
    FEATURES_PLANS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEY_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    LOGGING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    REALTIME_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    cache_plans: _containers.RepeatedCompositeFieldContainer[FeatureServiceCachePlan]
    feature_service_id: _id__client_pb2.Id
    feature_service_name: str
    feature_view_id: _id__client_pb2.Id
    feature_view_name: str
    features_plans: _containers.RepeatedCompositeFieldContainer[FeaturesPlan]
    join_key_template: _feature_service__client_pb2.JoinKeyTemplate
    logging_config: LoggingConfig
    realtime_environment: _realtime_compute__client_pb2.OnlineComputeConfig
    workspace_name: str
    workspace_state_id: _id__client_pb2.Id
    def __init__(self, feature_service_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., feature_view_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., feature_service_name: _Optional[str] = ..., feature_view_name: _Optional[str] = ..., workspace_name: _Optional[str] = ..., workspace_state_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., features_plans: _Optional[_Iterable[_Union[FeaturesPlan, _Mapping]]] = ..., join_key_template: _Optional[_Union[_feature_service__client_pb2.JoinKeyTemplate, _Mapping]] = ..., logging_config: _Optional[_Union[LoggingConfig, _Mapping]] = ..., realtime_environment: _Optional[_Union[_realtime_compute__client_pb2.OnlineComputeConfig, _Mapping]] = ..., cache_plans: _Optional[_Iterable[_Union[FeatureServiceCachePlan, _Mapping]]] = ...) -> None: ...

class FeatureVectorPlan(_message.Message):
    __slots__ = ["features"]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[FeaturePlan]
    def __init__(self, features: _Optional[_Iterable[_Union[FeaturePlan, _Mapping]]] = ...) -> None: ...

class FeaturesPlan(_message.Message):
    __slots__ = ["feature_plan", "realtime_features_plan"]
    FEATURE_PLAN_FIELD_NUMBER: _ClassVar[int]
    REALTIME_FEATURES_PLAN_FIELD_NUMBER: _ClassVar[int]
    feature_plan: FeaturePlan
    realtime_features_plan: RealtimeFeaturesPlan
    def __init__(self, feature_plan: _Optional[_Union[FeaturePlan, _Mapping]] = ..., realtime_features_plan: _Optional[_Union[RealtimeFeaturesPlan, _Mapping]] = ...) -> None: ...

class GlobalTableConfig(_message.Message):
    __slots__ = ["feature_data_water_mark", "feature_store_format_version", "feature_view_id", "feature_view_name", "online_store_params", "refresh_status_table", "slide_period", "status_table_timestamp_type", "table_format_version", "workspace_name"]
    FEATURE_DATA_WATER_MARK_FIELD_NUMBER: _ClassVar[int]
    FEATURE_STORE_FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    ONLINE_STORE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    REFRESH_STATUS_TABLE_FIELD_NUMBER: _ClassVar[int]
    SLIDE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    STATUS_TABLE_TIMESTAMP_TYPE_FIELD_NUMBER: _ClassVar[int]
    TABLE_FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_data_water_mark: _timestamp_pb2.Timestamp
    feature_store_format_version: int
    feature_view_id: _id__client_pb2.Id
    feature_view_name: str
    online_store_params: _feature_view__client_pb2_1.OnlineStoreParams
    refresh_status_table: bool
    slide_period: _duration_pb2.Duration
    status_table_timestamp_type: StatusTableTimestampType
    table_format_version: int
    workspace_name: str
    def __init__(self, feature_view_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., feature_view_name: _Optional[str] = ..., workspace_name: _Optional[str] = ..., slide_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., status_table_timestamp_type: _Optional[_Union[StatusTableTimestampType, str]] = ..., refresh_status_table: bool = ..., feature_store_format_version: _Optional[int] = ..., online_store_params: _Optional[_Union[_feature_view__client_pb2_1.OnlineStoreParams, _Mapping]] = ..., table_format_version: _Optional[int] = ..., feature_data_water_mark: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Jwk(_message.Message):
    __slots__ = ["alg", "e", "n", "use"]
    ALG_FIELD_NUMBER: _ClassVar[int]
    E_FIELD_NUMBER: _ClassVar[int]
    N_FIELD_NUMBER: _ClassVar[int]
    USE_FIELD_NUMBER: _ClassVar[int]
    alg: str
    e: str
    n: str
    use: str
    def __init__(self, n: _Optional[str] = ..., alg: _Optional[str] = ..., use: _Optional[str] = ..., e: _Optional[str] = ...) -> None: ...

class LoggingConfig(_message.Message):
    __slots__ = ["avro_schema", "log_effective_times", "sample_rate"]
    AVRO_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    LOG_EFFECTIVE_TIMES_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    avro_schema: str
    log_effective_times: bool
    sample_rate: float
    def __init__(self, sample_rate: _Optional[float] = ..., log_effective_times: bool = ..., avro_schema: _Optional[str] = ...) -> None: ...

class RealtimeFeaturesPlan(_message.Message):
    __slots__ = ["args_from_request_context", "compact_transformations", "description", "feature_set_inputs", "feature_view_id", "feature_view_name", "outputs", "pipeline", "tags", "transformations"]
    class FeatureSetInputsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FeatureVectorPlan
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[FeatureVectorPlan, _Mapping]] = ...) -> None: ...
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ARGS_FROM_REQUEST_CONTEXT_FIELD_NUMBER: _ClassVar[int]
    COMPACT_TRANSFORMATIONS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SET_INPUTS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATIONS_FIELD_NUMBER: _ClassVar[int]
    args_from_request_context: _containers.RepeatedCompositeFieldContainer[Column]
    compact_transformations: _containers.RepeatedCompositeFieldContainer[CompactTransformation]
    description: str
    feature_set_inputs: _containers.MessageMap[str, FeatureVectorPlan]
    feature_view_id: str
    feature_view_name: str
    outputs: _containers.RepeatedCompositeFieldContainer[Column]
    pipeline: _pipeline__client_pb2.Pipeline
    tags: _containers.ScalarMap[str, str]
    transformations: _containers.RepeatedCompositeFieldContainer[_transformation__client_pb2_1.Transformation]
    def __init__(self, args_from_request_context: _Optional[_Iterable[_Union[Column, _Mapping]]] = ..., outputs: _Optional[_Iterable[_Union[Column, _Mapping]]] = ..., feature_set_inputs: _Optional[_Mapping[str, FeatureVectorPlan]] = ..., pipeline: _Optional[_Union[_pipeline__client_pb2.Pipeline, _Mapping]] = ..., transformations: _Optional[_Iterable[_Union[_transformation__client_pb2_1.Transformation, _Mapping]]] = ..., feature_view_name: _Optional[str] = ..., feature_view_id: _Optional[str] = ..., compact_transformations: _Optional[_Iterable[_Union[CompactTransformation, _Mapping]]] = ..., description: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class RemappedJoinKeys(_message.Message):
    __slots__ = ["join_keys"]
    JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    join_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, join_keys: _Optional[_Iterable[str]] = ...) -> None: ...

class WorkspaceAcls(_message.Message):
    __slots__ = ["acls", "workspace_name"]
    ACLS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    acls: _containers.RepeatedCompositeFieldContainer[_acl__client_pb2.Acl]
    workspace_name: str
    def __init__(self, workspace_name: _Optional[str] = ..., acls: _Optional[_Iterable[_Union[_acl__client_pb2.Acl, _Mapping]]] = ...) -> None: ...

class DataTableTimestampType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class StatusTableTimestampType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
