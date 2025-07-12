from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

BATCH_MATERIALIZATION: JobType
BATCH_PLAN_INTEGRATION_TEST: JobType
BILLABLE_USAGE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
COMPUTE_TYPE_UNSPECIFIED: ComputeType
CONSUMPTION_SERVER_GROUP_TYPE_UNSPECIFIED: ConsumptionServerGroupType
CONSUMPTION_TYPE_UNSPECIFIED: ConsumptionType
CONSUMPTION_UNITS_UNSPECIFIED: ConsumptionUnit
DATABRICKS: ComputeType
DATASET_GENERATION: JobType
DESCRIPTOR: _descriptor.FileDescriptor
EMR: ComputeType
ENTITY_DELETION: JobType
FEATURE_PUBLISH: JobType
FEATURE_SERVER_GROUP: ConsumptionServerGroupType
FEATURE_SERVER_NODE_DURATION: ConsumptionType
FEATURE_SERVER_NODE_HOURS: ConsumptionUnit
FEATURE_SERVER_READS: ConsumptionType
FEATURE_SERVICE_ONLINE_REQUESTS: ConsumptionUnit
FEATURE_SERVICE_ONLINE_VECTORS_SERVED: ConsumptionUnit
FEATURE_SERVICE_VECTORS_SERVED: ConsumptionUnit
FEATURE_TABLE_INGEST: JobType
FEATURE_VIEW_ONLINE_READS: ConsumptionUnit
INGEST_API_COMPUTE: ConsumptionType
INGEST_SERVER_GROUP: ConsumptionServerGroupType
JOB_TYPE_UNSPECIFIED: JobType
MATERIALIZATION_JOB_WRITES: ConsumptionType
OFFLINE_STORE_MAINTENANCE: JobType
OFFLINE_WRITE_ROWS: ConsumptionUnit
OFFLINE_WRITE_VALUES: ConsumptionUnit
ONLINE_WRITE_ROWS: ConsumptionUnit
REAL_TIME_COMPUTE_DURATION_HOURS: ConsumptionUnit
REAL_TIME_JOB_COMPUTE: ConsumptionType
REQUIREMENT_NOT_REQUIRED: Requirement
REQUIREMENT_REQUIRED: Requirement
REQUIREMENT_UNSPECIFIED: Requirement
RIFT: ComputeType
RIFT_MATERIALIZATION_JOB_COMPUTE: ConsumptionType
SERVER_GROUP_NODE_DURATION: ConsumptionType
SERVER_GROUP_NODE_HOURS: ConsumptionUnit
SPARK_MATERIALIZATION_JOB_COMPUTE: ConsumptionType
STREAM_MATERIALIZATION: JobType
STREAM_PLAN_INTEGRATION_TEST: JobType
TECTON_JOB_COMPUTE_HOURS: ConsumptionUnit
TRANSFORM_SERVER_GROUP: ConsumptionServerGroupType
VISIBILITY_UNSPECIFIED: Visibility
VISIBILITY_VISIBLE: Visibility
billable_usage_options: _descriptor.FieldDescriptor

class BillableUsageOptions(_message.Message):
    __slots__ = ["required", "visibility"]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    required: Requirement
    visibility: Visibility
    def __init__(self, visibility: _Optional[_Union[Visibility, str]] = ..., required: _Optional[_Union[Requirement, str]] = ...) -> None: ...

class ConsumptionInfo(_message.Message):
    __slots__ = ["details", "feature_view_id", "feature_view_name", "metric", "online_read_aws_region", "source_id", "time_bucket_start", "units_consumed", "workspace"]
    class DetailsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    ONLINE_READ_AWS_REGION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_BUCKET_START_FIELD_NUMBER: _ClassVar[int]
    UNITS_CONSUMED_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    details: _containers.ScalarMap[str, str]
    feature_view_id: _id__client_pb2.Id
    feature_view_name: str
    metric: str
    online_read_aws_region: str
    source_id: str
    time_bucket_start: _timestamp_pb2.Timestamp
    units_consumed: int
    workspace: str
    def __init__(self, time_bucket_start: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., units_consumed: _Optional[int] = ..., metric: _Optional[str] = ..., details: _Optional[_Mapping[str, str]] = ..., source_id: _Optional[str] = ..., feature_view_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., feature_view_name: _Optional[str] = ..., workspace: _Optional[str] = ..., online_read_aws_region: _Optional[str] = ...) -> None: ...

class ConsumptionRecord(_message.Message):
    __slots__ = ["account_name", "collection_timestamp", "duration", "feature_server_node_hours_metadata", "feature_server_reads_metadata", "ingest_api_compute_hours_metadata", "is_canary", "materialization_job_offline_writes_metadata", "materialization_job_online_writes_metadata", "quantity", "server_group_node_hours_metadata", "tecton_job_compute_hours_metadata", "timestamp", "unit"]
    ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVER_NODE_HOURS_METADATA_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVER_READS_METADATA_FIELD_NUMBER: _ClassVar[int]
    INGEST_API_COMPUTE_HOURS_METADATA_FIELD_NUMBER: _ClassVar[int]
    IS_CANARY_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_JOB_OFFLINE_WRITES_METADATA_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_JOB_ONLINE_WRITES_METADATA_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_NODE_HOURS_METADATA_FIELD_NUMBER: _ClassVar[int]
    TECTON_JOB_COMPUTE_HOURS_METADATA_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    account_name: str
    collection_timestamp: _timestamp_pb2.Timestamp
    duration: _duration_pb2.Duration
    feature_server_node_hours_metadata: FeatureServerNodeHoursMetadata
    feature_server_reads_metadata: FeatureServerReadsMetadata
    ingest_api_compute_hours_metadata: IngestApiComputeHoursMetadata
    is_canary: bool
    materialization_job_offline_writes_metadata: MaterializationJobOfflineWritesMetadata
    materialization_job_online_writes_metadata: MaterializationJobOnlineWritesMetadata
    quantity: float
    server_group_node_hours_metadata: ServerGroupNodeHoursMetadata
    tecton_job_compute_hours_metadata: TectonJobComputeHoursMetadata
    timestamp: _timestamp_pb2.Timestamp
    unit: ConsumptionUnit
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., collection_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., account_name: _Optional[str] = ..., materialization_job_online_writes_metadata: _Optional[_Union[MaterializationJobOnlineWritesMetadata, _Mapping]] = ..., materialization_job_offline_writes_metadata: _Optional[_Union[MaterializationJobOfflineWritesMetadata, _Mapping]] = ..., feature_server_node_hours_metadata: _Optional[_Union[FeatureServerNodeHoursMetadata, _Mapping]] = ..., feature_server_reads_metadata: _Optional[_Union[FeatureServerReadsMetadata, _Mapping]] = ..., tecton_job_compute_hours_metadata: _Optional[_Union[TectonJobComputeHoursMetadata, _Mapping]] = ..., ingest_api_compute_hours_metadata: _Optional[_Union[IngestApiComputeHoursMetadata, _Mapping]] = ..., server_group_node_hours_metadata: _Optional[_Union[ServerGroupNodeHoursMetadata, _Mapping]] = ..., quantity: _Optional[float] = ..., unit: _Optional[_Union[ConsumptionUnit, str]] = ..., is_canary: bool = ...) -> None: ...

class EnrichedConsumptionInfo(_message.Message):
    __slots__ = ["consumption_info", "feature_view_id", "feature_view_name", "feature_view_workspace"]
    CONSUMPTION_INFO_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    consumption_info: ConsumptionInfo
    feature_view_id: str
    feature_view_name: str
    feature_view_workspace: str
    def __init__(self, consumption_info: _Optional[_Union[ConsumptionInfo, _Mapping]] = ..., feature_view_workspace: _Optional[str] = ..., feature_view_name: _Optional[str] = ..., feature_view_id: _Optional[str] = ...) -> None: ...

class FeatureServerNodeHoursMetadata(_message.Message):
    __slots__ = ["pod_count", "pod_cpu", "pod_memory_mib", "region"]
    POD_COUNT_FIELD_NUMBER: _ClassVar[int]
    POD_CPU_FIELD_NUMBER: _ClassVar[int]
    POD_MEMORY_MIB_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    pod_count: int
    pod_cpu: float
    pod_memory_mib: int
    region: str
    def __init__(self, region: _Optional[str] = ..., pod_cpu: _Optional[float] = ..., pod_memory_mib: _Optional[int] = ..., pod_count: _Optional[int] = ...) -> None: ...

class FeatureServerReadsMetadata(_message.Message):
    __slots__ = ["tecton_object_id", "tecton_object_name", "workspace"]
    TECTON_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    def __init__(self, workspace: _Optional[str] = ..., tecton_object_name: _Optional[str] = ..., tecton_object_id: _Optional[str] = ...) -> None: ...

class IngestApiComputeHoursMetadata(_message.Message):
    __slots__ = ["compute_type", "job_type", "memory_mib", "operation", "tags", "tecton_object_id", "tecton_object_name", "workspace", "workspace_state_id"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    COMPUTE_TYPE_FIELD_NUMBER: _ClassVar[int]
    JOB_TYPE_FIELD_NUMBER: _ClassVar[int]
    MEMORY_MIB_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TECTON_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    compute_type: ComputeType
    job_type: JobType
    memory_mib: int
    operation: str
    tags: _containers.ScalarMap[str, str]
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    workspace_state_id: str
    def __init__(self, compute_type: _Optional[_Union[ComputeType, str]] = ..., job_type: _Optional[_Union[JobType, str]] = ..., operation: _Optional[str] = ..., memory_mib: _Optional[int] = ..., workspace: _Optional[str] = ..., workspace_state_id: _Optional[str] = ..., tecton_object_name: _Optional[str] = ..., tecton_object_id: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class MaterializationJobOfflineWritesMetadata(_message.Message):
    __slots__ = ["tags", "tecton_job_id", "tecton_object_id", "tecton_object_name", "workspace", "workspace_state_id"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TECTON_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    TECTON_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.ScalarMap[str, str]
    tecton_job_id: str
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    workspace_state_id: str
    def __init__(self, tecton_job_id: _Optional[str] = ..., workspace: _Optional[str] = ..., workspace_state_id: _Optional[str] = ..., tecton_object_name: _Optional[str] = ..., tecton_object_id: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class MaterializationJobOnlineWritesMetadata(_message.Message):
    __slots__ = ["online_store_type", "tags", "tecton_job_id", "tecton_object_id", "tecton_object_name", "workspace", "workspace_state_id"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ONLINE_STORE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TECTON_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    TECTON_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    online_store_type: str
    tags: _containers.ScalarMap[str, str]
    tecton_job_id: str
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    workspace_state_id: str
    def __init__(self, online_store_type: _Optional[str] = ..., tecton_job_id: _Optional[str] = ..., workspace: _Optional[str] = ..., workspace_state_id: _Optional[str] = ..., tecton_object_name: _Optional[str] = ..., tecton_object_id: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ServerGroupNodeHoursMetadata(_message.Message):
    __slots__ = ["cloud_provider", "instance_type", "region", "server_group_name", "server_group_type"]
    CLOUD_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_TYPE_FIELD_NUMBER: _ClassVar[int]
    cloud_provider: str
    instance_type: str
    region: str
    server_group_name: str
    server_group_type: ConsumptionServerGroupType
    def __init__(self, region: _Optional[str] = ..., instance_type: _Optional[str] = ..., server_group_name: _Optional[str] = ..., cloud_provider: _Optional[str] = ..., server_group_type: _Optional[_Union[ConsumptionServerGroupType, str]] = ...) -> None: ...

class TectonJobComputeHoursMetadata(_message.Message):
    __slots__ = ["compute_type", "instance_type", "job_type", "num_workers", "region", "tags", "tecton_job_id", "tecton_object_id", "tecton_object_name", "workspace", "workspace_state_id"]
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    COMPUTE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    JOB_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_WORKERS_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TECTON_JOB_ID_FIELD_NUMBER: _ClassVar[int]
    TECTON_OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TECTON_OBJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    compute_type: ComputeType
    instance_type: str
    job_type: JobType
    num_workers: int
    region: str
    tags: _containers.ScalarMap[str, str]
    tecton_job_id: str
    tecton_object_id: str
    tecton_object_name: str
    workspace: str
    workspace_state_id: str
    def __init__(self, tecton_job_id: _Optional[str] = ..., instance_type: _Optional[str] = ..., region: _Optional[str] = ..., num_workers: _Optional[int] = ..., compute_type: _Optional[_Union[ComputeType, str]] = ..., job_type: _Optional[_Union[JobType, str]] = ..., workspace: _Optional[str] = ..., workspace_state_id: _Optional[str] = ..., tecton_object_name: _Optional[str] = ..., tecton_object_id: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class JobType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ComputeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ConsumptionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ConsumptionUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Visibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Requirement(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ConsumptionServerGroupType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
