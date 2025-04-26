from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import container_image__client_pb2 as _container_image__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import server_group_status__client_pb2 as _server_group_status__client_pb2
from tecton_proto.common import server_group_type__client_pb2 as _server_group_type__client_pb2
from tecton_proto.realtime import instance_group__client_pb2 as _instance_group__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
SCALING_POLICY_TYPE_TARGET_TRACKING: ScalingPolicyType
SCALING_POLICY_TYPE_UNSPECIFIED: ScalingPolicyType

class AutoscalingPolicy(_message.Message):
    __slots__ = ["autoscaling_enabled", "name", "target_tracking_policy"]
    AUTOSCALING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_TRACKING_POLICY_FIELD_NUMBER: _ClassVar[int]
    autoscaling_enabled: bool
    name: str
    target_tracking_policy: TargetTrackingPolicy
    def __init__(self, name: _Optional[str] = ..., autoscaling_enabled: bool = ..., target_tracking_policy: _Optional[_Union[TargetTrackingPolicy, _Mapping]] = ...) -> None: ...

class CustomMetric(_message.Message):
    __slots__ = ["name", "statistic", "unit"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATISTIC_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    name: str
    statistic: str
    unit: str
    def __init__(self, name: _Optional[str] = ..., statistic: _Optional[str] = ..., unit: _Optional[str] = ...) -> None: ...

class FeatureServerGroupAWSResources(_message.Message):
    __slots__ = ["autoscaling_group_id", "launch_template_active_version", "launch_template_id", "launch_template_pending_version", "loadbalancer_listener_rule_arn", "target_group_arn"]
    AUTOSCALING_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_TEMPLATE_ACTIVE_VERSION_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_TEMPLATE_PENDING_VERSION_FIELD_NUMBER: _ClassVar[int]
    LOADBALANCER_LISTENER_RULE_ARN_FIELD_NUMBER: _ClassVar[int]
    TARGET_GROUP_ARN_FIELD_NUMBER: _ClassVar[int]
    autoscaling_group_id: str
    launch_template_active_version: str
    launch_template_id: str
    launch_template_pending_version: str
    loadbalancer_listener_rule_arn: str
    target_group_arn: str
    def __init__(self, loadbalancer_listener_rule_arn: _Optional[str] = ..., autoscaling_group_id: _Optional[str] = ..., target_group_arn: _Optional[str] = ..., launch_template_id: _Optional[str] = ..., launch_template_active_version: _Optional[str] = ..., launch_template_pending_version: _Optional[str] = ...) -> None: ...

class FeatureServerGroupConfig(_message.Message):
    __slots__ = ["autoscaling_enabled", "desired_instances", "docker_image_fqn", "environment", "http_health_check_path", "http_port", "instance_type", "max_instances", "metrics_port", "min_instances"]
    class EnvironmentEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    AUTOSCALING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DESIRED_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    DOCKER_IMAGE_FQN_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    HTTP_HEALTH_CHECK_PATH_FIELD_NUMBER: _ClassVar[int]
    HTTP_PORT_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAX_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    METRICS_PORT_FIELD_NUMBER: _ClassVar[int]
    MIN_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    autoscaling_enabled: bool
    desired_instances: int
    docker_image_fqn: str
    environment: _containers.ScalarMap[str, str]
    http_health_check_path: str
    http_port: int
    instance_type: str
    max_instances: int
    metrics_port: int
    min_instances: int
    def __init__(self, instance_type: _Optional[str] = ..., docker_image_fqn: _Optional[str] = ..., http_port: _Optional[int] = ..., http_health_check_path: _Optional[str] = ..., metrics_port: _Optional[int] = ..., autoscaling_enabled: bool = ..., min_instances: _Optional[int] = ..., max_instances: _Optional[int] = ..., desired_instances: _Optional[int] = ..., environment: _Optional[_Mapping[str, str]] = ...) -> None: ...

class FeatureServerGroupState(_message.Message):
    __slots__ = ["active_config", "aws_resources", "pending_config"]
    ACTIVE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    AWS_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    PENDING_CONFIG_FIELD_NUMBER: _ClassVar[int]
    active_config: FeatureServerGroupConfig
    aws_resources: FeatureServerGroupAWSResources
    pending_config: FeatureServerGroupConfig
    def __init__(self, active_config: _Optional[_Union[FeatureServerGroupConfig, _Mapping]] = ..., pending_config: _Optional[_Union[FeatureServerGroupConfig, _Mapping]] = ..., aws_resources: _Optional[_Union[FeatureServerGroupAWSResources, _Mapping]] = ...) -> None: ...

class PredefinedMetric(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class ServerGroupState(_message.Message):
    __slots__ = ["autoscaling_policy", "created_at", "desired_nodes", "feature_server_group_state", "last_updated_at", "max_nodes", "min_nodes", "name", "server_group_id", "server_group_state_id", "status", "status_details", "transform_server_group_state", "type", "workspace", "workspace_state_id"]
    AUTOSCALING_POLICY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESIRED_NODES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVER_GROUP_STATE_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    MIN_NODES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_SERVER_GROUP_STATE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: _ClassVar[int]
    autoscaling_policy: AutoscalingPolicy
    created_at: _timestamp_pb2.Timestamp
    desired_nodes: int
    feature_server_group_state: FeatureServerGroupState
    last_updated_at: _timestamp_pb2.Timestamp
    max_nodes: int
    min_nodes: int
    name: str
    server_group_id: _id__client_pb2.Id
    server_group_state_id: _id__client_pb2.Id
    status: _server_group_status__client_pb2.ServerGroupStatus
    status_details: str
    transform_server_group_state: TransformServerGroupState
    type: _server_group_type__client_pb2.ServerGroupType
    workspace: str
    workspace_state_id: _id__client_pb2.Id
    def __init__(self, server_group_state_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., server_group_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., name: _Optional[str] = ..., status: _Optional[_Union[_server_group_status__client_pb2.ServerGroupStatus, str]] = ..., type: _Optional[_Union[_server_group_type__client_pb2.ServerGroupType, str]] = ..., autoscaling_policy: _Optional[_Union[AutoscalingPolicy, _Mapping]] = ..., status_details: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., min_nodes: _Optional[int] = ..., max_nodes: _Optional[int] = ..., desired_nodes: _Optional[int] = ..., transform_server_group_state: _Optional[_Union[TransformServerGroupState, _Mapping]] = ..., feature_server_group_state: _Optional[_Union[FeatureServerGroupState, _Mapping]] = ..., workspace: _Optional[str] = ..., workspace_state_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ...) -> None: ...

class TargetTrackingPolicy(_message.Message):
    __slots__ = ["custom_metric", "predefined_metric", "scale_in_disabled", "target_value"]
    CUSTOM_METRIC_FIELD_NUMBER: _ClassVar[int]
    PREDEFINED_METRIC_FIELD_NUMBER: _ClassVar[int]
    SCALE_IN_DISABLED_FIELD_NUMBER: _ClassVar[int]
    TARGET_VALUE_FIELD_NUMBER: _ClassVar[int]
    custom_metric: CustomMetric
    predefined_metric: PredefinedMetric
    scale_in_disabled: bool
    target_value: float
    def __init__(self, target_value: _Optional[float] = ..., scale_in_disabled: bool = ..., predefined_metric: _Optional[_Union[PredefinedMetric, _Mapping]] = ..., custom_metric: _Optional[_Union[CustomMetric, _Mapping]] = ...) -> None: ...

class TransformServerGroupState(_message.Message):
    __slots__ = ["autoscaling_policy", "environment_id", "environment_name", "environment_variables", "image_info", "instance_group_handle", "secrets_config"]
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    AUTOSCALING_POLICY_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    IMAGE_INFO_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_GROUP_HANDLE_FIELD_NUMBER: _ClassVar[int]
    SECRETS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    autoscaling_policy: AutoscalingPolicy
    environment_id: str
    environment_name: str
    environment_variables: _containers.ScalarMap[str, str]
    image_info: _container_image__client_pb2.ContainerImage
    instance_group_handle: _instance_group__client_pb2.InstanceGroupHandle
    secrets_config: TransformServerSecretsConfig
    def __init__(self, environment_id: _Optional[str] = ..., environment_name: _Optional[str] = ..., image_info: _Optional[_Union[_container_image__client_pb2.ContainerImage, _Mapping]] = ..., environment_variables: _Optional[_Mapping[str, str]] = ..., autoscaling_policy: _Optional[_Union[AutoscalingPolicy, _Mapping]] = ..., instance_group_handle: _Optional[_Union[_instance_group__client_pb2.InstanceGroupHandle, _Mapping]] = ..., secrets_config: _Optional[_Union[TransformServerSecretsConfig, _Mapping]] = ...) -> None: ...

class TransformServerSecretsConfig(_message.Message):
    __slots__ = ["last_updated", "service_account_id", "service_account_key_secret_name"]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_KEY_SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    last_updated: _timestamp_pb2.Timestamp
    service_account_id: str
    service_account_key_secret_name: str
    def __init__(self, service_account_id: _Optional[str] = ..., service_account_key_secret_name: _Optional[str] = ..., last_updated: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class ScalingPolicyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
