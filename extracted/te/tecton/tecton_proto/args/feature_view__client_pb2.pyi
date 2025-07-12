from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.args import basic_info__client_pb2 as _basic_info__client_pb2
from tecton_proto.args import data_source__client_pb2 as _data_source__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import pipeline__client_pb2 as _pipeline__client_pb2
from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import user_defined_function__client_pb2 as _user_defined_function__client_pb2
from tecton_proto.common import analytics_options__client_pb2 as _analytics_options__client_pb2
from tecton_proto.common import calculation_node__client_pb2 as _calculation_node__client_pb2
from tecton_proto.common import compute_identity__client_pb2 as _compute_identity__client_pb2
from tecton_proto.common import compute_mode__client_pb2 as _compute_mode__client_pb2
from tecton_proto.common import data_source_type__client_pb2 as _data_source_type__client_pb2
from tecton_proto.common import data_type__client_pb2 as _data_type__client_pb2
from tecton_proto.common import framework_version__client_pb2 as _framework_version__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import python_version__client_pb2 as _python_version__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import secret__client_pb2 as _secret__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from tecton_proto.common import time_window__client_pb2 as _time_window__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

AGGREGATION_MODE_LATEST_EVENT_TIME: AggregationLeadingEdge
AGGREGATION_MODE_UNSPECIFIED: AggregationLeadingEdge
AGGREGATION_MODE_WALL_CLOCK_TIME: AggregationLeadingEdge
BACKFILL_CONFIG_MODE_MULTIPLE_BATCH_SCHEDULE_INTERVALS_PER_JOB: BackfillConfigMode
BACKFILL_CONFIG_MODE_SINGLE_BATCH_SCHEDULE_INTERVAL_PER_JOB: BackfillConfigMode
BACKFILL_CONFIG_MODE_UNSPECIFIED: BackfillConfigMode
BATCH_TRIGGER_TYPE_MANUAL: BatchTriggerType
BATCH_TRIGGER_TYPE_NO_BATCH_MATERIALIZATION: BatchTriggerType
BATCH_TRIGGER_TYPE_SCHEDULED: BatchTriggerType
BATCH_TRIGGER_TYPE_UNSPECIFIED: BatchTriggerType
DESCRIPTOR: _descriptor.FileDescriptor
FEATURE_STORE_FORMAT_VERSION_DEFAULT: FeatureStoreFormatVersion
FEATURE_STORE_FORMAT_VERSION_MAX: FeatureStoreFormatVersion
FEATURE_STORE_FORMAT_VERSION_ONLINE_STORE_TTL_DELETION_ENABLED: FeatureStoreFormatVersion
FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS: FeatureStoreFormatVersion
FEATURE_STORE_FORMAT_VERSION_TTL_FIELD: FeatureStoreFormatVersion
FEATURE_VIEW_TYPE_FEATURE_TABLE: FeatureViewType
FEATURE_VIEW_TYPE_FWV5_FEATURE_VIEW: FeatureViewType
FEATURE_VIEW_TYPE_PROMPT: FeatureViewType
FEATURE_VIEW_TYPE_REALTIME: FeatureViewType
FEATURE_VIEW_TYPE_UNSPECIFIED: FeatureViewType
STREAM_PROCESSING_MODE_CONTINUOUS: StreamProcessingMode
STREAM_PROCESSING_MODE_TIME_INTERVAL: StreamProcessingMode
STREAM_PROCESSING_MODE_UNSPECIFIED: StreamProcessingMode

class Attribute(_message.Message):
    __slots__ = ["column_dtype", "description", "name", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    COLUMN_DTYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    column_dtype: _data_type__client_pb2.DataType
    description: str
    name: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., column_dtype: _Optional[_Union[_data_type__client_pb2.DataType, _Mapping]] = ..., description: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class BackfillConfig(_message.Message):
    __slots__ = ["mode"]
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: BackfillConfigMode
    def __init__(self, mode: _Optional[_Union[BackfillConfigMode, str]] = ...) -> None: ...

class BigtableOnlineStore(_message.Message):
    __slots__ = ["enabled", "instance_id", "project_id"]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    instance_id: str
    project_id: str
    def __init__(self, enabled: bool = ..., project_id: _Optional[str] = ..., instance_id: _Optional[str] = ...) -> None: ...

class CacheConfig(_message.Message):
    __slots__ = ["max_age_seconds"]
    MAX_AGE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    max_age_seconds: int
    def __init__(self, max_age_seconds: _Optional[int] = ...) -> None: ...

class Calculation(_message.Message):
    __slots__ = ["abstract_syntax_tree_root", "column_dtype", "description", "expr", "name", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ABSTRACT_SYNTAX_TREE_ROOT_FIELD_NUMBER: _ClassVar[int]
    COLUMN_DTYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXPR_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    abstract_syntax_tree_root: _calculation_node__client_pb2.AbstractSyntaxTreeNode
    column_dtype: _data_type__client_pb2.DataType
    description: str
    expr: str
    name: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., expr: _Optional[str] = ..., column_dtype: _Optional[_Union[_data_type__client_pb2.DataType, _Mapping]] = ..., description: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ..., abstract_syntax_tree_root: _Optional[_Union[_calculation_node__client_pb2.AbstractSyntaxTreeNode, _Mapping]] = ...) -> None: ...

class ClusterConfig(_message.Message):
    __slots__ = ["compute_identity", "existing_cluster", "implicit_config", "json_databricks", "json_dataproc", "json_emr", "new_databricks", "new_emr", "rift"]
    COMPUTE_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    EXISTING_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    IMPLICIT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    JSON_DATABRICKS_FIELD_NUMBER: _ClassVar[int]
    JSON_DATAPROC_FIELD_NUMBER: _ClassVar[int]
    JSON_EMR_FIELD_NUMBER: _ClassVar[int]
    NEW_DATABRICKS_FIELD_NUMBER: _ClassVar[int]
    NEW_EMR_FIELD_NUMBER: _ClassVar[int]
    RIFT_FIELD_NUMBER: _ClassVar[int]
    compute_identity: _compute_identity__client_pb2.ComputeIdentity
    existing_cluster: ExistingClusterConfig
    implicit_config: DefaultClusterConfig
    json_databricks: JsonClusterConfig
    json_dataproc: JsonClusterConfig
    json_emr: JsonClusterConfig
    new_databricks: NewClusterConfig
    new_emr: NewClusterConfig
    rift: RiftClusterConfig
    def __init__(self, existing_cluster: _Optional[_Union[ExistingClusterConfig, _Mapping]] = ..., new_databricks: _Optional[_Union[NewClusterConfig, _Mapping]] = ..., new_emr: _Optional[_Union[NewClusterConfig, _Mapping]] = ..., implicit_config: _Optional[_Union[DefaultClusterConfig, _Mapping]] = ..., json_databricks: _Optional[_Union[JsonClusterConfig, _Mapping]] = ..., json_emr: _Optional[_Union[JsonClusterConfig, _Mapping]] = ..., json_dataproc: _Optional[_Union[JsonClusterConfig, _Mapping]] = ..., rift: _Optional[_Union[RiftClusterConfig, _Mapping]] = ..., compute_identity: _Optional[_Union[_compute_identity__client_pb2.ComputeIdentity, _Mapping]] = ...) -> None: ...

class DataLakeConfig(_message.Message):
    __slots__ = ["delta"]
    DELTA_FIELD_NUMBER: _ClassVar[int]
    delta: DeltaConfig
    def __init__(self, delta: _Optional[_Union[DeltaConfig, _Mapping]] = ...) -> None: ...

class DataQualityConfig(_message.Message):
    __slots__ = ["data_quality_enabled", "skip_default_expectations"]
    DATA_QUALITY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SKIP_DEFAULT_EXPECTATIONS_FIELD_NUMBER: _ClassVar[int]
    data_quality_enabled: bool
    skip_default_expectations: bool
    def __init__(self, data_quality_enabled: bool = ..., skip_default_expectations: bool = ...) -> None: ...

class DefaultClusterConfig(_message.Message):
    __slots__ = ["databricks_spark_version", "emr_python_version", "emr_spark_version", "tecton_compute_instance_type"]
    DATABRICKS_SPARK_VERSION_FIELD_NUMBER: _ClassVar[int]
    EMR_PYTHON_VERSION_FIELD_NUMBER: _ClassVar[int]
    EMR_SPARK_VERSION_FIELD_NUMBER: _ClassVar[int]
    TECTON_COMPUTE_INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    databricks_spark_version: str
    emr_python_version: _python_version__client_pb2.PythonVersion
    emr_spark_version: str
    tecton_compute_instance_type: str
    def __init__(self, databricks_spark_version: _Optional[str] = ..., emr_spark_version: _Optional[str] = ..., tecton_compute_instance_type: _Optional[str] = ..., emr_python_version: _Optional[_Union[_python_version__client_pb2.PythonVersion, str]] = ...) -> None: ...

class DeltaConfig(_message.Message):
    __slots__ = ["time_partition_size"]
    TIME_PARTITION_SIZE_FIELD_NUMBER: _ClassVar[int]
    time_partition_size: _duration_pb2.Duration
    def __init__(self, time_partition_size: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class DynamoDbOnlineStore(_message.Message):
    __slots__ = ["enabled", "replica_regions"]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    REPLICA_REGIONS_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    replica_regions: NullableStringList
    def __init__(self, enabled: bool = ..., replica_regions: _Optional[_Union[NullableStringList, _Mapping]] = ...) -> None: ...

class Embedding(_message.Message):
    __slots__ = ["column", "column_dtype", "description", "model", "name", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    COLUMN_DTYPE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    column: str
    column_dtype: _data_type__client_pb2.DataType
    description: str
    model: str
    name: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., column: _Optional[str] = ..., column_dtype: _Optional[_Union[_data_type__client_pb2.DataType, _Mapping]] = ..., model: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class EntityKeyOverride(_message.Message):
    __slots__ = ["entity_id", "join_keys"]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    entity_id: _id__client_pb2.Id
    join_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entity_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., join_keys: _Optional[_Iterable[str]] = ...) -> None: ...

class ExistingClusterConfig(_message.Message):
    __slots__ = ["existing_cluster_id"]
    EXISTING_CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    existing_cluster_id: str
    def __init__(self, existing_cluster_id: _Optional[str] = ...) -> None: ...

class FeatureAggregation(_message.Message):
    __slots__ = ["batch_sawtooth_tile_size", "column", "column_dtype", "description", "function", "function_params", "lifetime_window", "name", "tags", "time_window", "time_window_legacy", "time_window_series"]
    class FunctionParamsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ParamValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ParamValue, _Mapping]] = ...) -> None: ...
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    BATCH_SAWTOOTH_TILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_DTYPE_FIELD_NUMBER: _ClassVar[int]
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_PARAMS_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_LEGACY_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_SERIES_FIELD_NUMBER: _ClassVar[int]
    batch_sawtooth_tile_size: _duration_pb2.Duration
    column: str
    column_dtype: _data_type__client_pb2.DataType
    description: str
    function: str
    function_params: _containers.MessageMap[str, ParamValue]
    lifetime_window: _time_window__client_pb2.LifetimeWindow
    name: str
    tags: _containers.ScalarMap[str, str]
    time_window: TimeWindow
    time_window_legacy: _duration_pb2.Duration
    time_window_series: TimeWindowSeries
    def __init__(self, column: _Optional[str] = ..., function: _Optional[str] = ..., function_params: _Optional[_Mapping[str, ParamValue]] = ..., time_window_legacy: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., name: _Optional[str] = ..., time_window: _Optional[_Union[TimeWindow, _Mapping]] = ..., lifetime_window: _Optional[_Union[_time_window__client_pb2.LifetimeWindow, _Mapping]] = ..., time_window_series: _Optional[_Union[TimeWindowSeries, _Mapping]] = ..., column_dtype: _Optional[_Union[_data_type__client_pb2.DataType, _Mapping]] = ..., batch_sawtooth_tile_size: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., description: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class FeatureTableArgs(_message.Message):
    __slots__ = ["attributes", "batch_compute", "monitoring", "offline_store", "offline_store_legacy", "online_store", "schema", "serving_ttl", "tecton_materialization_runtime", "timestamp_field"]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    BATCH_COMPUTE_FIELD_NUMBER: _ClassVar[int]
    MONITORING_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_LEGACY_FIELD_NUMBER: _ClassVar[int]
    ONLINE_STORE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    SERVING_TTL_FIELD_NUMBER: _ClassVar[int]
    TECTON_MATERIALIZATION_RUNTIME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    batch_compute: ClusterConfig
    monitoring: MonitoringConfig
    offline_store: OfflineStoreConfig
    offline_store_legacy: OfflineFeatureStoreConfig
    online_store: OnlineStoreConfig
    schema: _spark_schema__client_pb2.SparkSchema
    serving_ttl: _duration_pb2.Duration
    tecton_materialization_runtime: str
    timestamp_field: str
    def __init__(self, schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ..., serving_ttl: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., offline_store_legacy: _Optional[_Union[OfflineFeatureStoreConfig, _Mapping]] = ..., offline_store: _Optional[_Union[OfflineStoreConfig, _Mapping]] = ..., online_store: _Optional[_Union[OnlineStoreConfig, _Mapping]] = ..., batch_compute: _Optional[_Union[ClusterConfig, _Mapping]] = ..., monitoring: _Optional[_Union[MonitoringConfig, _Mapping]] = ..., tecton_materialization_runtime: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[Attribute, _Mapping]]] = ..., timestamp_field: _Optional[str] = ...) -> None: ...

class FeatureViewArgs(_message.Message):
    __slots__ = ["batch_compute_mode", "cache_config", "context_parameter_name", "data_quality_config", "entities", "feature_table_args", "feature_view_id", "feature_view_type", "forced_materialized_schema", "forced_view_schema", "info", "materialized_feature_view_args", "offline_enabled", "online_enabled", "online_serving_index", "options", "pipeline", "prevent_destroy", "prompt_args", "realtime_args", "resource_providers", "secrets", "version"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class ResourceProvidersEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _id__client_pb2.Id
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ...) -> None: ...
    class SecretsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _secret__client_pb2.SecretReference
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...
    BATCH_COMPUTE_MODE_FIELD_NUMBER: _ClassVar[int]
    CACHE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_PARAMETER_NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_QUALITY_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_TABLE_ARGS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_TYPE_FIELD_NUMBER: _ClassVar[int]
    FORCED_MATERIALIZED_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    FORCED_VIEW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZED_FEATURE_VIEW_ARGS_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ONLINE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ONLINE_SERVING_INDEX_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_FIELD_NUMBER: _ClassVar[int]
    PREVENT_DESTROY_FIELD_NUMBER: _ClassVar[int]
    PROMPT_ARGS_FIELD_NUMBER: _ClassVar[int]
    REALTIME_ARGS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_PROVIDERS_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    batch_compute_mode: _compute_mode__client_pb2.BatchComputeMode
    cache_config: CacheConfig
    context_parameter_name: str
    data_quality_config: DataQualityConfig
    entities: _containers.RepeatedCompositeFieldContainer[EntityKeyOverride]
    feature_table_args: FeatureTableArgs
    feature_view_id: _id__client_pb2.Id
    feature_view_type: FeatureViewType
    forced_materialized_schema: _spark_schema__client_pb2.SparkSchema
    forced_view_schema: _spark_schema__client_pb2.SparkSchema
    info: _basic_info__client_pb2.BasicInfo
    materialized_feature_view_args: MaterializedFeatureViewArgs
    offline_enabled: bool
    online_enabled: bool
    online_serving_index: _containers.RepeatedScalarFieldContainer[str]
    options: _containers.ScalarMap[str, str]
    pipeline: _pipeline__client_pb2.Pipeline
    prevent_destroy: bool
    prompt_args: PromptArgs
    realtime_args: RealtimeArgs
    resource_providers: _containers.MessageMap[str, _id__client_pb2.Id]
    secrets: _containers.MessageMap[str, _secret__client_pb2.SecretReference]
    version: _framework_version__client_pb2.FrameworkVersion
    def __init__(self, feature_view_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., feature_view_type: _Optional[_Union[FeatureViewType, str]] = ..., info: _Optional[_Union[_basic_info__client_pb2.BasicInfo, _Mapping]] = ..., version: _Optional[_Union[_framework_version__client_pb2.FrameworkVersion, str]] = ..., prevent_destroy: bool = ..., options: _Optional[_Mapping[str, str]] = ..., cache_config: _Optional[_Union[CacheConfig, _Mapping]] = ..., entities: _Optional[_Iterable[_Union[EntityKeyOverride, _Mapping]]] = ..., resource_providers: _Optional[_Mapping[str, _id__client_pb2.Id]] = ..., materialized_feature_view_args: _Optional[_Union[MaterializedFeatureViewArgs, _Mapping]] = ..., realtime_args: _Optional[_Union[RealtimeArgs, _Mapping]] = ..., feature_table_args: _Optional[_Union[FeatureTableArgs, _Mapping]] = ..., prompt_args: _Optional[_Union[PromptArgs, _Mapping]] = ..., context_parameter_name: _Optional[str] = ..., secrets: _Optional[_Mapping[str, _secret__client_pb2.SecretReference]] = ..., online_serving_index: _Optional[_Iterable[str]] = ..., online_enabled: bool = ..., offline_enabled: bool = ..., batch_compute_mode: _Optional[_Union[_compute_mode__client_pb2.BatchComputeMode, str]] = ..., pipeline: _Optional[_Union[_pipeline__client_pb2.Pipeline, _Mapping]] = ..., data_quality_config: _Optional[_Union[DataQualityConfig, _Mapping]] = ..., forced_view_schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ..., forced_materialized_schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ...) -> None: ...

class IcebergConfig(_message.Message):
    __slots__ = ["num_entity_buckets"]
    NUM_ENTITY_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    num_entity_buckets: int
    def __init__(self, num_entity_buckets: _Optional[int] = ...) -> None: ...

class Inference(_message.Message):
    __slots__ = ["description", "input_columns", "model", "name", "tags"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INPUT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    description: str
    input_columns: _containers.RepeatedCompositeFieldContainer[_schema__client_pb2.Field]
    model: str
    name: str
    tags: _containers.ScalarMap[str, str]
    def __init__(self, input_columns: _Optional[_Iterable[_Union[_schema__client_pb2.Field, _Mapping]]] = ..., name: _Optional[str] = ..., model: _Optional[str] = ..., description: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class JsonClusterConfig(_message.Message):
    __slots__ = ["json"]
    JSON_FIELD_NUMBER: _ClassVar[int]
    json: _struct_pb2.Struct
    def __init__(self, json: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class MaterializedFeatureViewArgs(_message.Message):
    __slots__ = ["aggregation_interval", "aggregation_leading_edge", "aggregation_secondary_key", "aggregations", "attributes", "batch_compute", "batch_publish_timestamp", "batch_schedule", "batch_trigger", "compaction_enabled", "data_source_type", "embeddings", "environment", "feature_start_time", "feature_store_format_version", "incremental_backfills", "inferences", "lifetime_start_time", "manual_trigger_backfill_end_time", "max_backfill_interval", "monitoring", "offline_store", "offline_store_legacy", "online_store", "output_stream", "publish_features_configs", "run_transformation_validation", "schema", "secondary_key_output_columns", "secrets", "serving_ttl", "stream_compute", "stream_processing_mode", "stream_tile_size", "stream_tiling_enabled", "tecton_materialization_runtime", "timestamp_field", "transform_server_group"]
    class SecretsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _secret__client_pb2.SecretReference
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...
    AGGREGATIONS_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_LEADING_EDGE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_SECONDARY_KEY_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    BATCH_COMPUTE_FIELD_NUMBER: _ClassVar[int]
    BATCH_PUBLISH_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    BATCH_SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    BATCH_TRIGGER_FIELD_NUMBER: _ClassVar[int]
    COMPACTION_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    EMBEDDINGS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_STORE_FORMAT_VERSION_FIELD_NUMBER: _ClassVar[int]
    INCREMENTAL_BACKFILLS_FIELD_NUMBER: _ClassVar[int]
    INFERENCES_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_START_TIME_FIELD_NUMBER: _ClassVar[int]
    MANUAL_TRIGGER_BACKFILL_END_TIME_FIELD_NUMBER: _ClassVar[int]
    MAX_BACKFILL_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    MONITORING_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_LEGACY_FIELD_NUMBER: _ClassVar[int]
    ONLINE_STORE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_STREAM_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_FEATURES_CONFIGS_FIELD_NUMBER: _ClassVar[int]
    RUN_TRANSFORMATION_VALIDATION_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_KEY_OUTPUT_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    SERVING_TTL_FIELD_NUMBER: _ClassVar[int]
    STREAM_COMPUTE_FIELD_NUMBER: _ClassVar[int]
    STREAM_PROCESSING_MODE_FIELD_NUMBER: _ClassVar[int]
    STREAM_TILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    STREAM_TILING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TECTON_MATERIALIZATION_RUNTIME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_SERVER_GROUP_FIELD_NUMBER: _ClassVar[int]
    aggregation_interval: _duration_pb2.Duration
    aggregation_leading_edge: AggregationLeadingEdge
    aggregation_secondary_key: str
    aggregations: _containers.RepeatedCompositeFieldContainer[FeatureAggregation]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    batch_compute: ClusterConfig
    batch_publish_timestamp: str
    batch_schedule: _duration_pb2.Duration
    batch_trigger: BatchTriggerType
    compaction_enabled: bool
    data_source_type: _data_source_type__client_pb2.DataSourceType
    embeddings: _containers.RepeatedCompositeFieldContainer[Embedding]
    environment: str
    feature_start_time: _timestamp_pb2.Timestamp
    feature_store_format_version: FeatureStoreFormatVersion
    incremental_backfills: bool
    inferences: _containers.RepeatedCompositeFieldContainer[Inference]
    lifetime_start_time: _timestamp_pb2.Timestamp
    manual_trigger_backfill_end_time: _timestamp_pb2.Timestamp
    max_backfill_interval: _duration_pb2.Duration
    monitoring: MonitoringConfig
    offline_store: OfflineStoreConfig
    offline_store_legacy: OfflineFeatureStoreConfig
    online_store: OnlineStoreConfig
    output_stream: OutputStream
    publish_features_configs: _containers.RepeatedCompositeFieldContainer[PublishFeaturesConfig]
    run_transformation_validation: bool
    schema: _schema__client_pb2.Schema
    secondary_key_output_columns: _containers.RepeatedCompositeFieldContainer[SecondaryKeyOutputColumn]
    secrets: _containers.MessageMap[str, _secret__client_pb2.SecretReference]
    serving_ttl: _duration_pb2.Duration
    stream_compute: ClusterConfig
    stream_processing_mode: StreamProcessingMode
    stream_tile_size: _duration_pb2.Duration
    stream_tiling_enabled: bool
    tecton_materialization_runtime: str
    timestamp_field: str
    transform_server_group: str
    def __init__(self, timestamp_field: _Optional[str] = ..., batch_schedule: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., feature_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., manual_trigger_backfill_end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_backfill_interval: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., serving_ttl: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., offline_store_legacy: _Optional[_Union[OfflineFeatureStoreConfig, _Mapping]] = ..., offline_store: _Optional[_Union[OfflineStoreConfig, _Mapping]] = ..., publish_features_configs: _Optional[_Iterable[_Union[PublishFeaturesConfig, _Mapping]]] = ..., batch_compute: _Optional[_Union[ClusterConfig, _Mapping]] = ..., stream_compute: _Optional[_Union[ClusterConfig, _Mapping]] = ..., monitoring: _Optional[_Union[MonitoringConfig, _Mapping]] = ..., data_source_type: _Optional[_Union[_data_source_type__client_pb2.DataSourceType, str]] = ..., online_store: _Optional[_Union[OnlineStoreConfig, _Mapping]] = ..., incremental_backfills: bool = ..., aggregation_interval: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., stream_processing_mode: _Optional[_Union[StreamProcessingMode, str]] = ..., aggregations: _Optional[_Iterable[_Union[FeatureAggregation, _Mapping]]] = ..., output_stream: _Optional[_Union[OutputStream, _Mapping]] = ..., batch_trigger: _Optional[_Union[BatchTriggerType, str]] = ..., schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., aggregation_secondary_key: _Optional[str] = ..., secondary_key_output_columns: _Optional[_Iterable[_Union[SecondaryKeyOutputColumn, _Mapping]]] = ..., run_transformation_validation: bool = ..., tecton_materialization_runtime: _Optional[str] = ..., lifetime_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., compaction_enabled: bool = ..., stream_tiling_enabled: bool = ..., stream_tile_size: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., environment: _Optional[str] = ..., transform_server_group: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[Attribute, _Mapping]]] = ..., embeddings: _Optional[_Iterable[_Union[Embedding, _Mapping]]] = ..., inferences: _Optional[_Iterable[_Union[Inference, _Mapping]]] = ..., aggregation_leading_edge: _Optional[_Union[AggregationLeadingEdge, str]] = ..., feature_store_format_version: _Optional[_Union[FeatureStoreFormatVersion, str]] = ..., secrets: _Optional[_Mapping[str, _secret__client_pb2.SecretReference]] = ..., batch_publish_timestamp: _Optional[str] = ...) -> None: ...

class MonitoringConfig(_message.Message):
    __slots__ = ["alert_email", "expected_freshness", "monitor_freshness"]
    ALERT_EMAIL_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_FRESHNESS_FIELD_NUMBER: _ClassVar[int]
    MONITOR_FRESHNESS_FIELD_NUMBER: _ClassVar[int]
    alert_email: str
    expected_freshness: _duration_pb2.Duration
    monitor_freshness: bool
    def __init__(self, monitor_freshness: bool = ..., expected_freshness: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., alert_email: _Optional[str] = ...) -> None: ...

class NewClusterConfig(_message.Message):
    __slots__ = ["extra_pip_dependencies", "first_on_demand", "instance_availability", "instance_type", "number_of_workers", "pinned_spark_version", "python_version", "root_volume_size_in_gb", "spark_config"]
    EXTRA_PIP_DEPENDENCIES_FIELD_NUMBER: _ClassVar[int]
    FIRST_ON_DEMAND_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_WORKERS_FIELD_NUMBER: _ClassVar[int]
    PINNED_SPARK_VERSION_FIELD_NUMBER: _ClassVar[int]
    PYTHON_VERSION_FIELD_NUMBER: _ClassVar[int]
    ROOT_VOLUME_SIZE_IN_GB_FIELD_NUMBER: _ClassVar[int]
    SPARK_CONFIG_FIELD_NUMBER: _ClassVar[int]
    extra_pip_dependencies: _containers.RepeatedScalarFieldContainer[str]
    first_on_demand: int
    instance_availability: str
    instance_type: str
    number_of_workers: int
    pinned_spark_version: str
    python_version: _python_version__client_pb2.PythonVersion
    root_volume_size_in_gb: int
    spark_config: SparkConfig
    def __init__(self, instance_type: _Optional[str] = ..., instance_availability: _Optional[str] = ..., number_of_workers: _Optional[int] = ..., root_volume_size_in_gb: _Optional[int] = ..., extra_pip_dependencies: _Optional[_Iterable[str]] = ..., spark_config: _Optional[_Union[SparkConfig, _Mapping]] = ..., first_on_demand: _Optional[int] = ..., pinned_spark_version: _Optional[str] = ..., python_version: _Optional[_Union[_python_version__client_pb2.PythonVersion, str]] = ...) -> None: ...

class NullableStringList(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class OfflineFeatureStoreConfig(_message.Message):
    __slots__ = ["delta", "iceberg", "parquet", "subdirectory_override"]
    DELTA_FIELD_NUMBER: _ClassVar[int]
    ICEBERG_FIELD_NUMBER: _ClassVar[int]
    PARQUET_FIELD_NUMBER: _ClassVar[int]
    SUBDIRECTORY_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    delta: DeltaConfig
    iceberg: IcebergConfig
    parquet: ParquetConfig
    subdirectory_override: str
    def __init__(self, parquet: _Optional[_Union[ParquetConfig, _Mapping]] = ..., delta: _Optional[_Union[DeltaConfig, _Mapping]] = ..., iceberg: _Optional[_Union[IcebergConfig, _Mapping]] = ..., subdirectory_override: _Optional[str] = ...) -> None: ...

class OfflineStoreConfig(_message.Message):
    __slots__ = ["publish_full_features", "publish_start_time", "staging_table_format"]
    PUBLISH_FULL_FEATURES_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_START_TIME_FIELD_NUMBER: _ClassVar[int]
    STAGING_TABLE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    publish_full_features: bool
    publish_start_time: _timestamp_pb2.Timestamp
    staging_table_format: OfflineFeatureStoreConfig
    def __init__(self, staging_table_format: _Optional[_Union[OfflineFeatureStoreConfig, _Mapping]] = ..., publish_full_features: bool = ..., publish_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class OnlineStoreConfig(_message.Message):
    __slots__ = ["bigtable", "dynamo", "redis"]
    BIGTABLE_FIELD_NUMBER: _ClassVar[int]
    DYNAMO_FIELD_NUMBER: _ClassVar[int]
    REDIS_FIELD_NUMBER: _ClassVar[int]
    bigtable: BigtableOnlineStore
    dynamo: DynamoDbOnlineStore
    redis: RedisOnlineStore
    def __init__(self, dynamo: _Optional[_Union[DynamoDbOnlineStore, _Mapping]] = ..., redis: _Optional[_Union[RedisOnlineStore, _Mapping]] = ..., bigtable: _Optional[_Union[BigtableOnlineStore, _Mapping]] = ...) -> None: ...

class OutputStream(_message.Message):
    __slots__ = ["include_features", "kafka", "kinesis"]
    INCLUDE_FEATURES_FIELD_NUMBER: _ClassVar[int]
    KAFKA_FIELD_NUMBER: _ClassVar[int]
    KINESIS_FIELD_NUMBER: _ClassVar[int]
    include_features: bool
    kafka: _data_source__client_pb2.KafkaDataSourceArgs
    kinesis: _data_source__client_pb2.KinesisDataSourceArgs
    def __init__(self, include_features: bool = ..., kinesis: _Optional[_Union[_data_source__client_pb2.KinesisDataSourceArgs, _Mapping]] = ..., kafka: _Optional[_Union[_data_source__client_pb2.KafkaDataSourceArgs, _Mapping]] = ...) -> None: ...

class ParamValue(_message.Message):
    __slots__ = ["double_value", "int64_value"]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    double_value: float
    int64_value: int
    def __init__(self, int64_value: _Optional[int] = ..., double_value: _Optional[float] = ...) -> None: ...

class ParquetConfig(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PromptArgs(_message.Message):
    __slots__ = ["attributes", "environment"]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    environment: str
    def __init__(self, environment: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[Attribute, _Mapping]]] = ...) -> None: ...

class PublishFeaturesConfig(_message.Message):
    __slots__ = ["data_lake_config", "publish_start_time", "sink_config"]
    DATA_LAKE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PUBLISH_START_TIME_FIELD_NUMBER: _ClassVar[int]
    SINK_CONFIG_FIELD_NUMBER: _ClassVar[int]
    data_lake_config: DataLakeConfig
    publish_start_time: _timestamp_pb2.Timestamp
    sink_config: SinkConfig
    def __init__(self, publish_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., sink_config: _Optional[_Union[SinkConfig, _Mapping]] = ..., data_lake_config: _Optional[_Union[DataLakeConfig, _Mapping]] = ...) -> None: ...

class RealtimeArgs(_message.Message):
    __slots__ = ["attributes", "calculations", "environments", "required_packages", "schema"]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    CALCULATIONS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_PACKAGES_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[Attribute]
    calculations: _containers.RepeatedCompositeFieldContainer[Calculation]
    environments: _containers.RepeatedScalarFieldContainer[str]
    required_packages: _containers.RepeatedScalarFieldContainer[str]
    schema: _spark_schema__client_pb2.SparkSchema
    def __init__(self, schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ..., environments: _Optional[_Iterable[str]] = ..., required_packages: _Optional[_Iterable[str]] = ..., attributes: _Optional[_Iterable[_Union[Attribute, _Mapping]]] = ..., calculations: _Optional[_Iterable[_Union[Calculation, _Mapping]]] = ...) -> None: ...

class RedisOnlineStore(_message.Message):
    __slots__ = ["authentication_token", "enabled", "primary_endpoint"]
    AUTHENTICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    authentication_token: str
    enabled: bool
    primary_endpoint: str
    def __init__(self, primary_endpoint: _Optional[str] = ..., authentication_token: _Optional[str] = ..., enabled: bool = ...) -> None: ...

class RiftClusterConfig(_message.Message):
    __slots__ = ["instance_type", "root_volume_size_in_gb"]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROOT_VOLUME_SIZE_IN_GB_FIELD_NUMBER: _ClassVar[int]
    instance_type: str
    root_volume_size_in_gb: int
    def __init__(self, instance_type: _Optional[str] = ..., root_volume_size_in_gb: _Optional[int] = ...) -> None: ...

class SecondaryKeyOutputColumn(_message.Message):
    __slots__ = ["lifetime_window", "name", "time_window", "time_window_series"]
    LIFETIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_SERIES_FIELD_NUMBER: _ClassVar[int]
    lifetime_window: _time_window__client_pb2.LifetimeWindow
    name: str
    time_window: TimeWindow
    time_window_series: TimeWindowSeries
    def __init__(self, time_window: _Optional[_Union[TimeWindow, _Mapping]] = ..., lifetime_window: _Optional[_Union[_time_window__client_pb2.LifetimeWindow, _Mapping]] = ..., time_window_series: _Optional[_Union[TimeWindowSeries, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...

class SinkConfig(_message.Message):
    __slots__ = ["function", "mode", "name", "secrets"]
    class SecretsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _secret__client_pb2.SecretReference
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_secret__client_pb2.SecretReference, _Mapping]] = ...) -> None: ...
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    function: _user_defined_function__client_pb2.UserDefinedFunction
    mode: _transformation__client_pb2.TransformationMode
    name: str
    secrets: _containers.MessageMap[str, _secret__client_pb2.SecretReference]
    def __init__(self, name: _Optional[str] = ..., function: _Optional[_Union[_user_defined_function__client_pb2.UserDefinedFunction, _Mapping]] = ..., secrets: _Optional[_Mapping[str, _secret__client_pb2.SecretReference]] = ..., mode: _Optional[_Union[_transformation__client_pb2.TransformationMode, str]] = ...) -> None: ...

class SparkConfig(_message.Message):
    __slots__ = ["spark_conf", "spark_driver_memory", "spark_driver_memory_overhead", "spark_executor_memory", "spark_executor_memory_overhead"]
    class SparkConfEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    SPARK_CONF_FIELD_NUMBER: _ClassVar[int]
    SPARK_DRIVER_MEMORY_FIELD_NUMBER: _ClassVar[int]
    SPARK_DRIVER_MEMORY_OVERHEAD_FIELD_NUMBER: _ClassVar[int]
    SPARK_EXECUTOR_MEMORY_FIELD_NUMBER: _ClassVar[int]
    SPARK_EXECUTOR_MEMORY_OVERHEAD_FIELD_NUMBER: _ClassVar[int]
    spark_conf: _containers.ScalarMap[str, str]
    spark_driver_memory: str
    spark_driver_memory_overhead: str
    spark_executor_memory: str
    spark_executor_memory_overhead: str
    def __init__(self, spark_driver_memory: _Optional[str] = ..., spark_executor_memory: _Optional[str] = ..., spark_driver_memory_overhead: _Optional[str] = ..., spark_executor_memory_overhead: _Optional[str] = ..., spark_conf: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TimeWindow(_message.Message):
    __slots__ = ["offset", "window_duration"]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    WINDOW_DURATION_FIELD_NUMBER: _ClassVar[int]
    offset: _duration_pb2.Duration
    window_duration: _duration_pb2.Duration
    def __init__(self, window_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., offset: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class TimeWindowSeries(_message.Message):
    __slots__ = ["series_end", "series_start", "step_size", "window_duration"]
    SERIES_END_FIELD_NUMBER: _ClassVar[int]
    SERIES_START_FIELD_NUMBER: _ClassVar[int]
    STEP_SIZE_FIELD_NUMBER: _ClassVar[int]
    WINDOW_DURATION_FIELD_NUMBER: _ClassVar[int]
    series_end: _duration_pb2.Duration
    series_start: _duration_pb2.Duration
    step_size: _duration_pb2.Duration
    window_duration: _duration_pb2.Duration
    def __init__(self, series_start: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., series_end: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., step_size: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., window_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class FeatureViewType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class BackfillConfigMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class AggregationLeadingEdge(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class StreamProcessingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class BatchTriggerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FeatureStoreFormatVersion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
