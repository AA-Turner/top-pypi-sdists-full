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
    ) -> None: ...

class ListKubeClustersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListKubeClustersResponse(_message.Message):
    __slots__ = ("clusters",)
    CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    clusters: _containers.RepeatedCompositeFieldContainer[KubeCluster]
    def __init__(self, clusters: _Optional[_Iterable[_Union[KubeCluster, _Mapping]]] = ...) -> None: ...

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
