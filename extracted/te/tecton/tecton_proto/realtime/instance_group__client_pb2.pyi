from tecton_proto.common import container_image__client_pb2 as _container_image__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import server_group_type__client_pb2 as _server_group_type__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AWSInstanceGroup(_message.Message):
    __slots__ = ["ami_image_id", "autoscaling_group_arn", "autoscaling_group_name", "health_check_path", "iam_instance_profile_arn", "instance_type", "instance_warmup_time_seconds", "launch_template_id", "port", "region", "security_group_ids", "subnet_ids"]
    AMI_IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_GROUP_ARN_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_PATH_FIELD_NUMBER: _ClassVar[int]
    IAM_INSTANCE_PROFILE_ARN_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_WARMUP_TIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    LAUNCH_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SECURITY_GROUP_IDS_FIELD_NUMBER: _ClassVar[int]
    SUBNET_IDS_FIELD_NUMBER: _ClassVar[int]
    ami_image_id: str
    autoscaling_group_arn: str
    autoscaling_group_name: str
    health_check_path: str
    iam_instance_profile_arn: str
    instance_type: str
    instance_warmup_time_seconds: int
    launch_template_id: str
    port: int
    region: str
    security_group_ids: _containers.RepeatedScalarFieldContainer[str]
    subnet_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, autoscaling_group_arn: _Optional[str] = ..., autoscaling_group_name: _Optional[str] = ..., region: _Optional[str] = ..., port: _Optional[int] = ..., health_check_path: _Optional[str] = ..., instance_type: _Optional[str] = ..., ami_image_id: _Optional[str] = ..., iam_instance_profile_arn: _Optional[str] = ..., security_group_ids: _Optional[_Iterable[str]] = ..., subnet_ids: _Optional[_Iterable[str]] = ..., launch_template_id: _Optional[str] = ..., instance_warmup_time_seconds: _Optional[int] = ...) -> None: ...

class AWSInstanceGroupUpdateConfig(_message.Message):
    __slots__ = ["ami_image_id", "instance_type"]
    AMI_IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ami_image_id: str
    instance_type: str
    def __init__(self, instance_type: _Optional[str] = ..., ami_image_id: _Optional[str] = ...) -> None: ...

class AWSTargetGroup(_message.Message):
    __slots__ = ["arn", "instance_group", "load_balancer_arn", "name"]
    ARN_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    LOAD_BALANCER_ARN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    arn: str
    instance_group: AWSInstanceGroup
    load_balancer_arn: str
    name: str
    def __init__(self, arn: _Optional[str] = ..., name: _Optional[str] = ..., instance_group: _Optional[_Union[AWSInstanceGroup, _Mapping]] = ..., load_balancer_arn: _Optional[str] = ...) -> None: ...

class CapacityConfig(_message.Message):
    __slots__ = ["autoscaling_enabled", "desired_nodes", "max_nodes", "min_nodes"]
    AUTOSCALING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DESIRED_NODES_FIELD_NUMBER: _ClassVar[int]
    MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    MIN_NODES_FIELD_NUMBER: _ClassVar[int]
    autoscaling_enabled: bool
    desired_nodes: int
    max_nodes: int
    min_nodes: int
    def __init__(self, autoscaling_enabled: bool = ..., min_nodes: _Optional[int] = ..., max_nodes: _Optional[int] = ..., desired_nodes: _Optional[int] = ...) -> None: ...

class GoogleCloudBackendService(_message.Message):
    __slots__ = ["instance_group", "project", "region", "target_id"]
    INSTANCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    instance_group: GoogleCloudInstanceGroup
    project: str
    region: str
    target_id: str
    def __init__(self, target_id: _Optional[str] = ..., project: _Optional[str] = ..., region: _Optional[str] = ..., instance_group: _Optional[_Union[GoogleCloudInstanceGroup, _Mapping]] = ...) -> None: ...

class GoogleCloudInstanceGroup(_message.Message):
    __slots__ = ["health_check_name", "machine_type", "project", "region", "scopes", "service_account", "subnetworks", "target_id"]
    HEALTH_CHECK_NAME_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    SUBNETWORKS_FIELD_NUMBER: _ClassVar[int]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    health_check_name: str
    machine_type: str
    project: str
    region: str
    scopes: _containers.RepeatedScalarFieldContainer[str]
    service_account: str
    subnetworks: _containers.RepeatedScalarFieldContainer[str]
    target_id: str
    def __init__(self, project: _Optional[str] = ..., region: _Optional[str] = ..., target_id: _Optional[str] = ..., machine_type: _Optional[str] = ..., subnetworks: _Optional[_Iterable[str]] = ..., health_check_name: _Optional[str] = ..., service_account: _Optional[str] = ..., scopes: _Optional[_Iterable[str]] = ...) -> None: ...

class HealthCheckConfig(_message.Message):
    __slots__ = ["path", "port", "protocol_type"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_TYPE_FIELD_NUMBER: _ClassVar[int]
    path: str
    port: NamedPort
    protocol_type: str
    def __init__(self, port: _Optional[_Union[NamedPort, _Mapping]] = ..., path: _Optional[str] = ..., protocol_type: _Optional[str] = ...) -> None: ...

class InstanceGroup(_message.Message):
    __slots__ = ["app_name", "aws_instance_group", "capacity", "container_image", "custom_metric_labels", "environment_variables", "google_cloud_instance_group", "grpc_port", "health_check_config", "health_check_name", "host", "http_port", "metrics_namespace", "name", "prometheus_port", "repo_upgrade_spec", "server_group_id", "should_update_repo", "tags", "type", "workspace"]
    class CustomMetricLabelsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class TagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    AWS_INSTANCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_IMAGE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_METRIC_LABELS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_CLOUD_INSTANCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    GRPC_PORT_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_CONFIG_FIELD_NUMBER: _ClassVar[int]
    HEALTH_CHECK_NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    HTTP_PORT_FIELD_NUMBER: _ClassVar[int]
    METRICS_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROMETHEUS_PORT_FIELD_NUMBER: _ClassVar[int]
    REPO_UPGRADE_SPEC_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    SHOULD_UPDATE_REPO_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    aws_instance_group: AWSInstanceGroup
    capacity: CapacityConfig
    container_image: _container_image__client_pb2.ContainerImage
    custom_metric_labels: _containers.ScalarMap[str, str]
    environment_variables: _containers.ScalarMap[str, str]
    google_cloud_instance_group: GoogleCloudInstanceGroup
    grpc_port: NamedPort
    health_check_config: HealthCheckConfig
    health_check_name: str
    host: str
    http_port: NamedPort
    metrics_namespace: str
    name: str
    prometheus_port: NamedPort
    repo_upgrade_spec: str
    server_group_id: _id__client_pb2.Id
    should_update_repo: bool
    tags: _containers.ScalarMap[str, str]
    type: _server_group_type__client_pb2.ServerGroupType
    workspace: str
    def __init__(self, name: _Optional[str] = ..., workspace: _Optional[str] = ..., app_name: _Optional[str] = ..., container_image: _Optional[_Union[_container_image__client_pb2.ContainerImage, _Mapping]] = ..., capacity: _Optional[_Union[CapacityConfig, _Mapping]] = ..., health_check_config: _Optional[_Union[HealthCheckConfig, _Mapping]] = ..., health_check_name: _Optional[str] = ..., prometheus_port: _Optional[_Union[NamedPort, _Mapping]] = ..., grpc_port: _Optional[_Union[NamedPort, _Mapping]] = ..., http_port: _Optional[_Union[NamedPort, _Mapping]] = ..., aws_instance_group: _Optional[_Union[AWSInstanceGroup, _Mapping]] = ..., google_cloud_instance_group: _Optional[_Union[GoogleCloudInstanceGroup, _Mapping]] = ..., tags: _Optional[_Mapping[str, str]] = ..., environment_variables: _Optional[_Mapping[str, str]] = ..., host: _Optional[str] = ..., metrics_namespace: _Optional[str] = ..., custom_metric_labels: _Optional[_Mapping[str, str]] = ..., should_update_repo: bool = ..., repo_upgrade_spec: _Optional[str] = ..., type: _Optional[_Union[_server_group_type__client_pb2.ServerGroupType, str]] = ..., server_group_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ...) -> None: ...

class InstanceGroupHandle(_message.Message):
    __slots__ = ["instance_group_id", "instance_group_name", "instance_group_template_id"]
    INSTANCE_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_GROUP_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    instance_group_id: str
    instance_group_name: str
    instance_group_template_id: str
    def __init__(self, instance_group_id: _Optional[str] = ..., instance_group_name: _Optional[str] = ..., instance_group_template_id: _Optional[str] = ...) -> None: ...

class InstanceGroupStatus(_message.Message):
    __slots__ = ["healthy_instances", "unhealthy_instances"]
    HEALTHY_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    UNHEALTHY_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    healthy_instances: int
    unhealthy_instances: int
    def __init__(self, healthy_instances: _Optional[int] = ..., unhealthy_instances: _Optional[int] = ...) -> None: ...

class LoadBalancerTarget(_message.Message):
    __slots__ = ["aws_target_group", "google_backend_service"]
    AWS_TARGET_GROUP_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_BACKEND_SERVICE_FIELD_NUMBER: _ClassVar[int]
    aws_target_group: AWSTargetGroup
    google_backend_service: GoogleCloudBackendService
    def __init__(self, aws_target_group: _Optional[_Union[AWSTargetGroup, _Mapping]] = ..., google_backend_service: _Optional[_Union[GoogleCloudBackendService, _Mapping]] = ...) -> None: ...

class NamedPort(_message.Message):
    __slots__ = ["port_name", "port_number"]
    PORT_NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    port_name: str
    port_number: int
    def __init__(self, port_number: _Optional[int] = ..., port_name: _Optional[str] = ...) -> None: ...
