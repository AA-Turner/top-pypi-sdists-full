from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.kubernetes.v1 import nodes_pb2 as _nodes_pb2
from chalk._gen.chalk.kubernetes.v1 import pods_pb2 as _pods_pb2
from chalk._gen.chalk.pubsub.v1 import node_status_pb2 as _node_status_pb2
from chalk._gen.chalk.pubsub.v1 import pod_status_pb2 as _pod_status_pb2
from chalk._gen.chalk.server.v1 import chart_pb2 as _chart_pb2
from chalk._gen.chalk.server.v1 import pod_request_pb2 as _pod_request_pb2
from chalk._gen.chalk.usage.v1 import rate_pb2 as _rate_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.type import date_pb2 as _date_pb2
from google.type import decimal_pb2 as _decimal_pb2
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

class UsageChartPeriod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USAGE_CHART_PERIOD_UNSPECIFIED: _ClassVar[UsageChartPeriod]
    USAGE_CHART_PERIOD_DAILY: _ClassVar[UsageChartPeriod]
    USAGE_CHART_PERIOD_MONTHLY: _ClassVar[UsageChartPeriod]
    USAGE_CHART_PERIOD_HOURLY: _ClassVar[UsageChartPeriod]

class UsageChartGrouping(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USAGE_CHART_GROUPING_UNSPECIFIED: _ClassVar[UsageChartGrouping]
    USAGE_CHART_GROUPING_INSTANCE_TYPE: _ClassVar[UsageChartGrouping]
    USAGE_CHART_GROUPING_CLUSTER: _ClassVar[UsageChartGrouping]
    USAGE_CHART_GROUPING_NODEPOOL: _ClassVar[UsageChartGrouping]
    USAGE_CHART_GROUPING_WORKLOAD_TYPE: _ClassVar[UsageChartGrouping]

class UsageChartTimeRange(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USAGE_CHART_TIME_RANGE_UNSPECIFIED: _ClassVar[UsageChartTimeRange]
    USAGE_CHART_TIME_RANGE_1D: _ClassVar[UsageChartTimeRange]
    USAGE_CHART_TIME_RANGE_7D: _ClassVar[UsageChartTimeRange]

USAGE_CHART_PERIOD_UNSPECIFIED: UsageChartPeriod
USAGE_CHART_PERIOD_DAILY: UsageChartPeriod
USAGE_CHART_PERIOD_MONTHLY: UsageChartPeriod
USAGE_CHART_PERIOD_HOURLY: UsageChartPeriod
USAGE_CHART_GROUPING_UNSPECIFIED: UsageChartGrouping
USAGE_CHART_GROUPING_INSTANCE_TYPE: UsageChartGrouping
USAGE_CHART_GROUPING_CLUSTER: UsageChartGrouping
USAGE_CHART_GROUPING_NODEPOOL: UsageChartGrouping
USAGE_CHART_GROUPING_WORKLOAD_TYPE: UsageChartGrouping
USAGE_CHART_TIME_RANGE_UNSPECIFIED: UsageChartTimeRange
USAGE_CHART_TIME_RANGE_1D: UsageChartTimeRange
USAGE_CHART_TIME_RANGE_7D: UsageChartTimeRange

class GetUsageChartRequest(_message.Message):
    __slots__ = ("start_ms", "end_ms", "period", "grouping", "time_range")
    START_MS_FIELD_NUMBER: _ClassVar[int]
    END_MS_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    GROUPING_FIELD_NUMBER: _ClassVar[int]
    TIME_RANGE_FIELD_NUMBER: _ClassVar[int]
    start_ms: int
    end_ms: int
    period: UsageChartPeriod
    grouping: UsageChartGrouping
    time_range: UsageChartTimeRange
    def __init__(
        self,
        start_ms: _Optional[int] = ...,
        end_ms: _Optional[int] = ...,
        period: _Optional[_Union[UsageChartPeriod, str]] = ...,
        grouping: _Optional[_Union[UsageChartGrouping, str]] = ...,
        time_range: _Optional[_Union[UsageChartTimeRange, str]] = ...,
    ) -> None: ...

class GetUsageChartResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _chart_pb2.Chart
    def __init__(self, chart: _Optional[_Union[_chart_pb2.Chart, _Mapping]] = ...) -> None: ...

class GetUtilizationRatesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetUtilizationRatesResponse(_message.Message):
    __slots__ = ("rates", "sandbox_credits_per_vcpu_hour", "sandbox_credits_per_gb_memory_hour")
    RATES_FIELD_NUMBER: _ClassVar[int]
    SANDBOX_CREDITS_PER_VCPU_HOUR_FIELD_NUMBER: _ClassVar[int]
    SANDBOX_CREDITS_PER_GB_MEMORY_HOUR_FIELD_NUMBER: _ClassVar[int]
    rates: _containers.RepeatedCompositeFieldContainer[_rate_pb2.MachineRate]
    sandbox_credits_per_vcpu_hour: _decimal_pb2.Decimal
    sandbox_credits_per_gb_memory_hour: _decimal_pb2.Decimal
    def __init__(
        self,
        rates: _Optional[_Iterable[_Union[_rate_pb2.MachineRate, _Mapping]]] = ...,
        sandbox_credits_per_vcpu_hour: _Optional[_Union[_decimal_pb2.Decimal, _Mapping]] = ...,
        sandbox_credits_per_gb_memory_hour: _Optional[_Union[_decimal_pb2.Decimal, _Mapping]] = ...,
    ) -> None: ...

class GetNodesAndPodsRequest(_message.Message):
    __slots__ = ("namespace", "pod_label_selector", "environment_id")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POD_LABEL_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    pod_label_selector: str
    environment_id: str
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        pod_label_selector: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
    ) -> None: ...

class GetNodesAndPodsResponse(_message.Message):
    __slots__ = ("nodes", "pods")
    NODES_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[_node_status_pb2.NodeStatusPubSub]
    pods: _containers.RepeatedCompositeFieldContainer[_pod_status_pb2.PodStatusPubSub]
    def __init__(
        self,
        nodes: _Optional[_Iterable[_Union[_node_status_pb2.NodeStatusPubSub, _Mapping]]] = ...,
        pods: _Optional[_Iterable[_Union[_pod_status_pb2.PodStatusPubSub, _Mapping]]] = ...,
    ) -> None: ...

class GetNodesAndPodsUIRequest(_message.Message):
    __slots__ = ("namespace", "pod_label_selector", "environment_id")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POD_LABEL_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    pod_label_selector: str
    environment_id: str
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        pod_label_selector: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
    ) -> None: ...

class GetNodesAndPodsUIResponse(_message.Message):
    __slots__ = ("nodes", "pods")
    NODES_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[_nodes_pb2.KubernetesNodeData]
    pods: _containers.RepeatedCompositeFieldContainer[_pods_pb2.KubernetesPodData]
    def __init__(
        self,
        nodes: _Optional[_Iterable[_Union[_nodes_pb2.KubernetesNodeData, _Mapping]]] = ...,
        pods: _Optional[_Iterable[_Union[_pods_pb2.KubernetesPodData, _Mapping]]] = ...,
    ) -> None: ...

class SyncUtilizationRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SyncUtilizationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCreditBundlesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCreditBundlesResponse(_message.Message):
    __slots__ = ("bundles",)
    BUNDLES_FIELD_NUMBER: _ClassVar[int]
    bundles: _containers.RepeatedCompositeFieldContainer[CreditBundle]
    def __init__(self, bundles: _Optional[_Iterable[_Union[CreditBundle, _Mapping]]] = ...) -> None: ...

class CreditBundle(_message.Message):
    __slots__ = ("bundle_id", "purchase_date", "credit_quantity", "purchase_price", "expires_on", "remaining_credits")
    BUNDLE_ID_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_DATE_FIELD_NUMBER: _ClassVar[int]
    CREDIT_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_PRICE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_ON_FIELD_NUMBER: _ClassVar[int]
    REMAINING_CREDITS_FIELD_NUMBER: _ClassVar[int]
    bundle_id: str
    purchase_date: _date_pb2.Date
    credit_quantity: int
    purchase_price: int
    expires_on: _date_pb2.Date
    remaining_credits: int
    def __init__(
        self,
        bundle_id: _Optional[str] = ...,
        purchase_date: _Optional[_Union[_date_pb2.Date, _Mapping]] = ...,
        credit_quantity: _Optional[int] = ...,
        purchase_price: _Optional[int] = ...,
        expires_on: _Optional[_Union[_date_pb2.Date, _Mapping]] = ...,
        remaining_credits: _Optional[int] = ...,
    ) -> None: ...

class GetInstanceUsageRequest(_message.Message):
    __slots__ = ("start_ms", "end_ms", "environment_id")
    START_MS_FIELD_NUMBER: _ClassVar[int]
    END_MS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    start_ms: int
    end_ms: int
    environment_id: str
    def __init__(
        self, start_ms: _Optional[int] = ..., end_ms: _Optional[int] = ..., environment_id: _Optional[str] = ...
    ) -> None: ...

class InstanceUsage(_message.Message):
    __slots__ = ("cluster_name", "instance_type", "id", "start_time", "end_time", "hours_used")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    HOURS_USED_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    instance_type: str
    id: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    hours_used: float
    def __init__(
        self,
        cluster_name: _Optional[str] = ...,
        instance_type: _Optional[str] = ...,
        id: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        hours_used: _Optional[float] = ...,
    ) -> None: ...

class GetInstanceUsageResponse(_message.Message):
    __slots__ = ("instances",)
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    instances: _containers.RepeatedCompositeFieldContainer[InstanceUsage]
    def __init__(self, instances: _Optional[_Iterable[_Union[InstanceUsage, _Mapping]]] = ...) -> None: ...

class GetPodTimeRangesRequest(_message.Message):
    __slots__ = (
        "pod_names",
        "pod_name_regex",
        "resource_group",
        "nodepool",
        "component",
        "service_kind",
        "start_time",
        "end_time",
    )
    POD_NAMES_FIELD_NUMBER: _ClassVar[int]
    POD_NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    SERVICE_KIND_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    pod_names: _containers.RepeatedScalarFieldContainer[str]
    pod_name_regex: str
    resource_group: str
    nodepool: str
    component: str
    service_kind: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        pod_names: _Optional[_Iterable[str]] = ...,
        pod_name_regex: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        nodepool: _Optional[str] = ...,
        component: _Optional[str] = ...,
        service_kind: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class PodTimeRange(_message.Message):
    __slots__ = ("pod_name", "start_time", "end_time")
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    pod_name: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        pod_name: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetPodTimeRangesResponse(_message.Message):
    __slots__ = ("time_ranges",)
    TIME_RANGES_FIELD_NUMBER: _ClassVar[int]
    time_ranges: _containers.RepeatedCompositeFieldContainer[PodTimeRange]
    def __init__(self, time_ranges: _Optional[_Iterable[_Union[PodTimeRange, _Mapping]]] = ...) -> None: ...

class GetNodeTimeRangesRequest(_message.Message):
    __slots__ = ("node_names", "node_name_regex", "nodepool", "start_time", "end_time")
    NODE_NAMES_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    node_names: _containers.RepeatedScalarFieldContainer[str]
    node_name_regex: str
    nodepool: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        node_names: _Optional[_Iterable[str]] = ...,
        node_name_regex: _Optional[str] = ...,
        nodepool: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class NodeTimeRange(_message.Message):
    __slots__ = ("node_name", "start_time", "end_time", "node_uid")
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    NODE_UID_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    node_uid: str
    def __init__(
        self,
        node_name: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        node_uid: _Optional[str] = ...,
    ) -> None: ...

class GetNodeTimeRangesResponse(_message.Message):
    __slots__ = ("time_ranges",)
    TIME_RANGES_FIELD_NUMBER: _ClassVar[int]
    time_ranges: _containers.RepeatedCompositeFieldContainer[NodeTimeRange]
    def __init__(self, time_ranges: _Optional[_Iterable[_Union[NodeTimeRange, _Mapping]]] = ...) -> None: ...

class GetNodeDetailRequest(_message.Message):
    __slots__ = ("cluster_name", "node_name", "node_uid")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_UID_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    node_name: str
    node_uid: str
    def __init__(
        self, cluster_name: _Optional[str] = ..., node_name: _Optional[str] = ..., node_uid: _Optional[str] = ...
    ) -> None: ...

class NodeDetailInfo(_message.Message):
    __slots__ = ("node_name", "cluster_name", "nodepool", "instance_type", "start_time", "end_time", "node_uid")
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    NODEPOOL_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    NODE_UID_FIELD_NUMBER: _ClassVar[int]
    node_name: str
    cluster_name: str
    nodepool: str
    instance_type: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    node_uid: str
    def __init__(
        self,
        node_name: _Optional[str] = ...,
        cluster_name: _Optional[str] = ...,
        nodepool: _Optional[str] = ...,
        instance_type: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        node_uid: _Optional[str] = ...,
    ) -> None: ...

class NodeDetailPod(_message.Message):
    __slots__ = (
        "pod_name",
        "start_time",
        "end_time",
        "workload_type",
        "resource_group",
        "cpu_request",
        "cpu_limit",
        "memory_request",
        "memory_limit",
    )
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    WORKLOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    CPU_REQUEST_FIELD_NUMBER: _ClassVar[int]
    CPU_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MEMORY_LIMIT_FIELD_NUMBER: _ClassVar[int]
    pod_name: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    workload_type: str
    resource_group: str
    cpu_request: str
    cpu_limit: str
    memory_request: str
    memory_limit: str
    def __init__(
        self,
        pod_name: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        workload_type: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        cpu_request: _Optional[str] = ...,
        cpu_limit: _Optional[str] = ...,
        memory_request: _Optional[str] = ...,
        memory_limit: _Optional[str] = ...,
    ) -> None: ...

class GetNodeDetailResponse(_message.Message):
    __slots__ = ("node", "pods")
    NODE_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    node: NodeDetailInfo
    pods: _containers.RepeatedCompositeFieldContainer[NodeDetailPod]
    def __init__(
        self,
        node: _Optional[_Union[NodeDetailInfo, _Mapping]] = ...,
        pods: _Optional[_Iterable[_Union[NodeDetailPod, _Mapping]]] = ...,
    ) -> None: ...

class GetResourceGroupServiceDetailRequest(_message.Message):
    __slots__ = ("service_kind", "resource_group", "start_time", "end_time")
    SERVICE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    service_kind: str
    resource_group: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        service_kind: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ResourceGroupServicePod(_message.Message):
    __slots__ = (
        "pod_name",
        "start_time",
        "end_time",
        "workload_type",
        "node_name",
        "cpu_request",
        "cpu_limit",
        "memory_request",
        "memory_limit",
    )
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    WORKLOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    CPU_REQUEST_FIELD_NUMBER: _ClassVar[int]
    CPU_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MEMORY_LIMIT_FIELD_NUMBER: _ClassVar[int]
    pod_name: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    workload_type: str
    node_name: str
    cpu_request: str
    cpu_limit: str
    memory_request: str
    memory_limit: str
    def __init__(
        self,
        pod_name: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        workload_type: _Optional[str] = ...,
        node_name: _Optional[str] = ...,
        cpu_request: _Optional[str] = ...,
        cpu_limit: _Optional[str] = ...,
        memory_request: _Optional[str] = ...,
        memory_limit: _Optional[str] = ...,
    ) -> None: ...

class GetResourceGroupServiceDetailResponse(_message.Message):
    __slots__ = ("service_kind", "resource_group", "pods")
    SERVICE_KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    service_kind: str
    resource_group: str
    pods: _containers.RepeatedCompositeFieldContainer[ResourceGroupServicePod]
    def __init__(
        self,
        service_kind: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
        pods: _Optional[_Iterable[_Union[ResourceGroupServicePod, _Mapping]]] = ...,
    ) -> None: ...
