from tecton_proto.spark_common import clusters__client_pb2 as _clusters__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

AWS_INSUFFICIENT_INSTANCE_CAPACITY_FAILURE: TerminationCode
CLIENT_ERROR: TerminationType
CLOUD_FAILURE: TerminationType
CLOUD_PROVIDER_LAUNCH_FAILURE: TerminationCode
CLOUD_PROVIDER_SHUTDOWN: TerminationCode
COMMUNICATION_LOST: TerminationCode
CONTAINER_LAUNCH_FAILURE: TerminationCode
DBFS_COMPONENT_UNHEALTHY: TerminationCode
DESCRIPTOR: _descriptor.FileDescriptor
DRIVER_UNREACHABLE: TerminationCode
DRIVER_UNRESPONSIVE: TerminationCode
ERROR: ClusterState
INACTIVITY: TerminationCode
INIT_SCRIPT_FAILURE: TerminationCode
INSTANCE_POOL_CLUSTER_FAILURE: TerminationCode
INSTANCE_UNREACHABLE: TerminationCode
INTERNAL_ERROR: TerminationCode
INVALID_ARGUMENT: TerminationCode
JOB_FINISHED: TerminationCode
METASTORE_COMPONENT_UNHEALTHY: TerminationCode
PENDING: ClusterState
REQUEST_REJECTED: TerminationCode
RESIZING: ClusterState
RESTARTING: ClusterState
RUNNING: ClusterState
SERVICE_FAULT: TerminationType
SPARK_ERROR: TerminationCode
SPARK_STARTUP_FAILURE: TerminationCode
SUCCESS: TerminationType
TERMINATED: ClusterState
TERMINATING: ClusterState
TRIAL_EXPIRED: TerminationCode
UNEXPECTED_LAUNCH_FAILURE: TerminationCode
UNKNOWN: ClusterState
UNKNOWN_TERMINATION_STATE: TerminationCode
UNKNOWN_TERMINATION_TYPE: TerminationType
USER_REQUEST: TerminationCode

class Cluster(_message.Message):
    __slots__ = ["cluster_id", "cluster_name", "custom_tags", "spark_version", "state"]
    class CustomTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_TAGS_FIELD_NUMBER: _ClassVar[int]
    SPARK_VERSION_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    cluster_name: str
    custom_tags: _containers.ScalarMap[str, str]
    spark_version: str
    state: ClusterState
    def __init__(self, cluster_id: _Optional[str] = ..., cluster_name: _Optional[str] = ..., spark_version: _Optional[str] = ..., state: _Optional[_Union[ClusterState, str]] = ..., custom_tags: _Optional[_Mapping[str, str]] = ...) -> None: ...

class ClusterAutoScale(_message.Message):
    __slots__ = ["max_workers", "min_workers"]
    MAX_WORKERS_FIELD_NUMBER: _ClassVar[int]
    MIN_WORKERS_FIELD_NUMBER: _ClassVar[int]
    max_workers: int
    min_workers: int
    def __init__(self, min_workers: _Optional[int] = ..., max_workers: _Optional[int] = ...) -> None: ...

class ClusterCreateRequest(_message.Message):
    __slots__ = ["apply_policy_default_values", "autoscale", "autotermination_minutes", "aws_attributes", "cluster_name", "custom_tags", "data_security_mode", "driver_node_type_id", "enable_elastic_disk", "gcp_attributes", "idempotency_token", "init_scripts", "node_type_id", "num_workers", "policy_id", "single_user_name", "spark_conf", "spark_env_vars", "spark_version"]
    class CustomTagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SparkConfEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SparkEnvVarsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    APPLY_POLICY_DEFAULT_VALUES_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALE_FIELD_NUMBER: _ClassVar[int]
    AUTOTERMINATION_MINUTES_FIELD_NUMBER: _ClassVar[int]
    AWS_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_TAGS_FIELD_NUMBER: _ClassVar[int]
    DATA_SECURITY_MODE_FIELD_NUMBER: _ClassVar[int]
    DRIVER_NODE_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    ENABLE_ELASTIC_DISK_FIELD_NUMBER: _ClassVar[int]
    GCP_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INIT_SCRIPTS_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    NUM_WORKERS_FIELD_NUMBER: _ClassVar[int]
    POLICY_ID_FIELD_NUMBER: _ClassVar[int]
    SINGLE_USER_NAME_FIELD_NUMBER: _ClassVar[int]
    SPARK_CONF_FIELD_NUMBER: _ClassVar[int]
    SPARK_ENV_VARS_FIELD_NUMBER: _ClassVar[int]
    SPARK_VERSION_FIELD_NUMBER: _ClassVar[int]
    apply_policy_default_values: bool
    autoscale: ClusterAutoScale
    autotermination_minutes: int
    aws_attributes: _clusters__client_pb2.AwsAttributes
    cluster_name: str
    custom_tags: _containers.ScalarMap[str, str]
    data_security_mode: str
    driver_node_type_id: str
    enable_elastic_disk: bool
    gcp_attributes: _clusters__client_pb2.GCPAttributes
    idempotency_token: str
    init_scripts: _containers.RepeatedCompositeFieldContainer[_clusters__client_pb2.ResourceLocation]
    node_type_id: str
    num_workers: int
    policy_id: str
    single_user_name: str
    spark_conf: _containers.ScalarMap[str, str]
    spark_env_vars: _containers.ScalarMap[str, str]
    spark_version: str
    def __init__(self, spark_conf: _Optional[_Mapping[str, str]] = ..., driver_node_type_id: _Optional[str] = ..., node_type_id: _Optional[str] = ..., num_workers: _Optional[int] = ..., cluster_name: _Optional[str] = ..., spark_version: _Optional[str] = ..., aws_attributes: _Optional[_Union[_clusters__client_pb2.AwsAttributes, _Mapping]] = ..., idempotency_token: _Optional[str] = ..., spark_env_vars: _Optional[_Mapping[str, str]] = ..., custom_tags: _Optional[_Mapping[str, str]] = ..., autotermination_minutes: _Optional[int] = ..., enable_elastic_disk: bool = ..., autoscale: _Optional[_Union[ClusterAutoScale, _Mapping]] = ..., init_scripts: _Optional[_Iterable[_Union[_clusters__client_pb2.ResourceLocation, _Mapping]]] = ..., policy_id: _Optional[str] = ..., gcp_attributes: _Optional[_Union[_clusters__client_pb2.GCPAttributes, _Mapping]] = ..., data_security_mode: _Optional[str] = ..., single_user_name: _Optional[str] = ..., apply_policy_default_values: bool = ...) -> None: ...

class ClusterCreateResponse(_message.Message):
    __slots__ = ["cluster_id"]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ClusterListResponse(_message.Message):
    __slots__ = ["clusters"]
    CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    clusters: _containers.RepeatedCompositeFieldContainer[Cluster]
    def __init__(self, clusters: _Optional[_Iterable[_Union[Cluster, _Mapping]]] = ...) -> None: ...

class ClusterTerminateRequest(_message.Message):
    __slots__ = ["cluster_id"]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ClustersGetRequest(_message.Message):
    __slots__ = ["cluster_id"]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    def __init__(self, cluster_id: _Optional[str] = ...) -> None: ...

class ClustersGetResponse(_message.Message):
    __slots__ = ["cluster_id", "state", "state_message", "termination_reason"]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STATE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TERMINATION_REASON_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    state: ClusterState
    state_message: str
    termination_reason: TerminationReason
    def __init__(self, cluster_id: _Optional[str] = ..., state_message: _Optional[str] = ..., termination_reason: _Optional[_Union[TerminationReason, _Mapping]] = ..., state: _Optional[_Union[ClusterState, str]] = ...) -> None: ...

class GetInstancePoolRequest(_message.Message):
    __slots__ = ["instance_pool_id"]
    INSTANCE_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    instance_pool_id: str
    def __init__(self, instance_pool_id: _Optional[str] = ...) -> None: ...

class InstancePool(_message.Message):
    __slots__ = ["instance_pool_id", "instance_pool_name", "node_type_id", "state"]
    INSTANCE_POOL_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_POOL_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    instance_pool_id: str
    instance_pool_name: str
    node_type_id: str
    state: str
    def __init__(self, instance_pool_name: _Optional[str] = ..., node_type_id: _Optional[str] = ..., state: _Optional[str] = ..., instance_pool_id: _Optional[str] = ...) -> None: ...

class InstancePools(_message.Message):
    __slots__ = ["instance_pools"]
    INSTANCE_POOLS_FIELD_NUMBER: _ClassVar[int]
    instance_pools: _containers.RepeatedCompositeFieldContainer[InstancePool]
    def __init__(self, instance_pools: _Optional[_Iterable[_Union[InstancePool, _Mapping]]] = ...) -> None: ...

class ListInstancePoolsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TerminationReason(_message.Message):
    __slots__ = ["code", "type"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    code: TerminationCode
    type: TerminationType
    def __init__(self, code: _Optional[_Union[TerminationCode, str]] = ..., type: _Optional[_Union[TerminationType, str]] = ...) -> None: ...

class ClusterState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class TerminationCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class TerminationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
