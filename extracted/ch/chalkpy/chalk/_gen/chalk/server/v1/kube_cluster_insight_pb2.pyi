from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import chart_pb2 as _chart_pb2
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

class KubeClusterProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KUBE_CLUSTER_PROVIDER_UNSPECIFIED: _ClassVar[KubeClusterProvider]
    KUBE_CLUSTER_PROVIDER_GKE: _ClassVar[KubeClusterProvider]
    KUBE_CLUSTER_PROVIDER_EKS: _ClassVar[KubeClusterProvider]
    KUBE_CLUSTER_PROVIDER_AKS: _ClassVar[KubeClusterProvider]

class KubeClusterMetricsTimeRange(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    KUBE_CLUSTER_METRICS_TIME_RANGE_UNSPECIFIED: _ClassVar[KubeClusterMetricsTimeRange]
    KUBE_CLUSTER_METRICS_TIME_RANGE_1H: _ClassVar[KubeClusterMetricsTimeRange]
    KUBE_CLUSTER_METRICS_TIME_RANGE_24H: _ClassVar[KubeClusterMetricsTimeRange]
    KUBE_CLUSTER_METRICS_TIME_RANGE_7D: _ClassVar[KubeClusterMetricsTimeRange]
    KUBE_CLUSTER_METRICS_TIME_RANGE_30D: _ClassVar[KubeClusterMetricsTimeRange]

KUBE_CLUSTER_PROVIDER_UNSPECIFIED: KubeClusterProvider
KUBE_CLUSTER_PROVIDER_GKE: KubeClusterProvider
KUBE_CLUSTER_PROVIDER_EKS: KubeClusterProvider
KUBE_CLUSTER_PROVIDER_AKS: KubeClusterProvider
KUBE_CLUSTER_METRICS_TIME_RANGE_UNSPECIFIED: KubeClusterMetricsTimeRange
KUBE_CLUSTER_METRICS_TIME_RANGE_1H: KubeClusterMetricsTimeRange
KUBE_CLUSTER_METRICS_TIME_RANGE_24H: KubeClusterMetricsTimeRange
KUBE_CLUSTER_METRICS_TIME_RANGE_7D: KubeClusterMetricsTimeRange
KUBE_CLUSTER_METRICS_TIME_RANGE_30D: KubeClusterMetricsTimeRange

class KubeNodePool(_message.Message):
    __slots__ = (
        "name",
        "machine_type",
        "current_size",
        "min_size",
        "max_size",
        "autoscaling_enabled",
        "locations",
        "status",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_SIZE_FIELD_NUMBER: _ClassVar[int]
    MIN_SIZE_FIELD_NUMBER: _ClassVar[int]
    MAX_SIZE_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    name: str
    machine_type: str
    current_size: int
    min_size: int
    max_size: int
    autoscaling_enabled: bool
    locations: _containers.RepeatedScalarFieldContainer[str]
    status: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        machine_type: _Optional[str] = ...,
        current_size: _Optional[int] = ...,
        min_size: _Optional[int] = ...,
        max_size: _Optional[int] = ...,
        autoscaling_enabled: bool = ...,
        locations: _Optional[_Iterable[str]] = ...,
        status: _Optional[str] = ...,
    ) -> None: ...

class KubeClusterAutoscalingResourceLimit(_message.Message):
    __slots__ = ("resource_type", "minimum", "maximum")
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    resource_type: str
    minimum: int
    maximum: int
    def __init__(
        self, resource_type: _Optional[str] = ..., minimum: _Optional[int] = ..., maximum: _Optional[int] = ...
    ) -> None: ...

class KubeClusterGKENodeAutoprovisioningConfig(_message.Message):
    __slots__ = (
        "enabled",
        "autoscaling_profile",
        "autoprovisioning_locations",
        "default_service_account",
        "default_oauth_scopes",
        "default_disk_size_gb",
        "default_disk_type",
        "default_image_type",
        "default_boot_disk_kms_key",
    )
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_PROFILE_FIELD_NUMBER: _ClassVar[int]
    AUTOPROVISIONING_LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_OAUTH_SCOPES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_DISK_SIZE_GB_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_DISK_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_IMAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_BOOT_DISK_KMS_KEY_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    autoscaling_profile: str
    autoprovisioning_locations: _containers.RepeatedScalarFieldContainer[str]
    default_service_account: str
    default_oauth_scopes: _containers.RepeatedScalarFieldContainer[str]
    default_disk_size_gb: int
    default_disk_type: str
    default_image_type: str
    default_boot_disk_kms_key: str
    def __init__(
        self,
        enabled: bool = ...,
        autoscaling_profile: _Optional[str] = ...,
        autoprovisioning_locations: _Optional[_Iterable[str]] = ...,
        default_service_account: _Optional[str] = ...,
        default_oauth_scopes: _Optional[_Iterable[str]] = ...,
        default_disk_size_gb: _Optional[int] = ...,
        default_disk_type: _Optional[str] = ...,
        default_image_type: _Optional[str] = ...,
        default_boot_disk_kms_key: _Optional[str] = ...,
    ) -> None: ...

class KubeCluster(_message.Message):
    __slots__ = (
        "provider",
        "name",
        "location",
        "project_or_account",
        "status",
        "kubernetes_version",
        "total_max_nodes",
        "total_current_nodes",
        "node_pools",
        "roles",
        "autoscaling_resource_limits",
        "gke_node_autoprovisioning",
    )
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    PROJECT_OR_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    KUBERNETES_VERSION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CURRENT_NODES_FIELD_NUMBER: _ClassVar[int]
    NODE_POOLS_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_RESOURCE_LIMITS_FIELD_NUMBER: _ClassVar[int]
    GKE_NODE_AUTOPROVISIONING_FIELD_NUMBER: _ClassVar[int]
    provider: KubeClusterProvider
    name: str
    location: str
    project_or_account: str
    status: str
    kubernetes_version: str
    total_max_nodes: int
    total_current_nodes: int
    node_pools: _containers.RepeatedCompositeFieldContainer[KubeNodePool]
    roles: _containers.RepeatedScalarFieldContainer[str]
    autoscaling_resource_limits: _containers.RepeatedCompositeFieldContainer[KubeClusterAutoscalingResourceLimit]
    gke_node_autoprovisioning: KubeClusterGKENodeAutoprovisioningConfig
    def __init__(
        self,
        provider: _Optional[_Union[KubeClusterProvider, str]] = ...,
        name: _Optional[str] = ...,
        location: _Optional[str] = ...,
        project_or_account: _Optional[str] = ...,
        status: _Optional[str] = ...,
        kubernetes_version: _Optional[str] = ...,
        total_max_nodes: _Optional[int] = ...,
        total_current_nodes: _Optional[int] = ...,
        node_pools: _Optional[_Iterable[_Union[KubeNodePool, _Mapping]]] = ...,
        roles: _Optional[_Iterable[str]] = ...,
        autoscaling_resource_limits: _Optional[_Iterable[_Union[KubeClusterAutoscalingResourceLimit, _Mapping]]] = ...,
        gke_node_autoprovisioning: _Optional[_Union[KubeClusterGKENodeAutoprovisioningConfig, _Mapping]] = ...,
    ) -> None: ...

class ListKubeClustersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListKubeClustersResponse(_message.Message):
    __slots__ = ("clusters",)
    CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    clusters: _containers.RepeatedCompositeFieldContainer[KubeCluster]
    def __init__(self, clusters: _Optional[_Iterable[_Union[KubeCluster, _Mapping]]] = ...) -> None: ...

class GetKubeClusterRequest(_message.Message):
    __slots__ = ("cluster_name",)
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    def __init__(self, cluster_name: _Optional[str] = ...) -> None: ...

class GetKubeClusterResponse(_message.Message):
    __slots__ = ("cluster",)
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    cluster: KubeCluster
    def __init__(self, cluster: _Optional[_Union[KubeCluster, _Mapping]] = ...) -> None: ...

class UpdateGKEClusterRequest(_message.Message):
    __slots__ = (
        "node_autoprovisioning_enabled",
        "autoscaling_min_cpu",
        "autoscaling_max_cpu",
        "autoscaling_min_memory",
        "autoscaling_max_memory",
    )
    NODE_AUTOPROVISIONING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_MIN_CPU_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_MAX_CPU_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_MIN_MEMORY_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_MAX_MEMORY_FIELD_NUMBER: _ClassVar[int]
    node_autoprovisioning_enabled: bool
    autoscaling_min_cpu: int
    autoscaling_max_cpu: int
    autoscaling_min_memory: int
    autoscaling_max_memory: int
    def __init__(
        self,
        node_autoprovisioning_enabled: bool = ...,
        autoscaling_min_cpu: _Optional[int] = ...,
        autoscaling_max_cpu: _Optional[int] = ...,
        autoscaling_min_memory: _Optional[int] = ...,
        autoscaling_max_memory: _Optional[int] = ...,
    ) -> None: ...

class UpdateEKSClusterRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateAKSClusterRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpdateKubeClusterRequest(_message.Message):
    __slots__ = ("cluster_name", "gke", "eks", "aks")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    GKE_FIELD_NUMBER: _ClassVar[int]
    EKS_FIELD_NUMBER: _ClassVar[int]
    AKS_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    gke: UpdateGKEClusterRequest
    eks: UpdateEKSClusterRequest
    aks: UpdateAKSClusterRequest
    def __init__(
        self,
        cluster_name: _Optional[str] = ...,
        gke: _Optional[_Union[UpdateGKEClusterRequest, _Mapping]] = ...,
        eks: _Optional[_Union[UpdateEKSClusterRequest, _Mapping]] = ...,
        aks: _Optional[_Union[UpdateAKSClusterRequest, _Mapping]] = ...,
    ) -> None: ...

class UpdateKubeClusterResponse(_message.Message):
    __slots__ = ("cluster",)
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    cluster: KubeCluster
    def __init__(self, cluster: _Optional[_Union[KubeCluster, _Mapping]] = ...) -> None: ...

class GetKubeClusterMetricsRequest(_message.Message):
    __slots__ = ("cluster_name", "time_range")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    time_range: KubeClusterMetricsTimeRange
    def __init__(
        self, cluster_name: _Optional[str] = ..., time_range: _Optional[_Union[KubeClusterMetricsTimeRange, str]] = ...
    ) -> None: ...

class GetKubeClusterMetricsResponse(_message.Message):
    __slots__ = ("charts", "total_max_nodes")
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MAX_NODES_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[_chart_pb2.Chart]
    total_max_nodes: int
    def __init__(
        self,
        charts: _Optional[_Iterable[_Union[_chart_pb2.Chart, _Mapping]]] = ...,
        total_max_nodes: _Optional[int] = ...,
    ) -> None: ...
