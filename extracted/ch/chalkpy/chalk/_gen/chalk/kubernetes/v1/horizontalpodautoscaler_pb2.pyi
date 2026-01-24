from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
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

class KubernetesHorizontalPodAutoscalerTargetRef(_message.Message):
    __slots__ = ("kind", "name", "api_version")
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    kind: str
    name: str
    api_version: str
    def __init__(
        self, kind: _Optional[str] = ..., name: _Optional[str] = ..., api_version: _Optional[str] = ...
    ) -> None: ...

class KubernetesLabelSelector(_message.Message):
    __slots__ = ("match_labels",)
    class MatchLabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    MATCH_LABELS_FIELD_NUMBER: _ClassVar[int]
    match_labels: _containers.ScalarMap[str, str]
    def __init__(self, match_labels: _Optional[_Mapping[str, str]] = ...) -> None: ...

class KubernetesHPAObjectMetricSource(_message.Message):
    __slots__ = ("target", "metric_name", "target_value", "selector", "average_value")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_VALUE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    target: KubernetesHorizontalPodAutoscalerTargetRef
    metric_name: str
    target_value: str
    selector: KubernetesLabelSelector
    average_value: str
    def __init__(
        self,
        target: _Optional[_Union[KubernetesHorizontalPodAutoscalerTargetRef, _Mapping]] = ...,
        metric_name: _Optional[str] = ...,
        target_value: _Optional[str] = ...,
        selector: _Optional[_Union[KubernetesLabelSelector, _Mapping]] = ...,
        average_value: _Optional[str] = ...,
    ) -> None: ...

class KubernetesHPAPodsMetricSource(_message.Message):
    __slots__ = ("metric_name", "target_average_value", "selector")
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    metric_name: str
    target_average_value: str
    selector: KubernetesLabelSelector
    def __init__(
        self,
        metric_name: _Optional[str] = ...,
        target_average_value: _Optional[str] = ...,
        selector: _Optional[_Union[KubernetesLabelSelector, _Mapping]] = ...,
    ) -> None: ...

class KubernetesHPAResourceMetricSource(_message.Message):
    __slots__ = ("name", "target_average_utilization", "target_average_value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_AVERAGE_UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    TARGET_AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    target_average_utilization: int
    target_average_value: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        target_average_utilization: _Optional[int] = ...,
        target_average_value: _Optional[str] = ...,
    ) -> None: ...

class KubernetesHPAContainerResourceMetricSource(_message.Message):
    __slots__ = ("name", "target_average_utilization", "target_average_value", "container")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_AVERAGE_UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    TARGET_AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    name: str
    target_average_utilization: int
    target_average_value: str
    container: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        target_average_utilization: _Optional[int] = ...,
        target_average_value: _Optional[str] = ...,
        container: _Optional[str] = ...,
    ) -> None: ...

class KubernetesHPAExternalMetricSource(_message.Message):
    __slots__ = ("metric_name", "metric_selector", "target_value", "target_average_value")
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    TARGET_VALUE_FIELD_NUMBER: _ClassVar[int]
    TARGET_AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    metric_name: str
    metric_selector: KubernetesLabelSelector
    target_value: str
    target_average_value: str
    def __init__(
        self,
        metric_name: _Optional[str] = ...,
        metric_selector: _Optional[_Union[KubernetesLabelSelector, _Mapping]] = ...,
        target_value: _Optional[str] = ...,
        target_average_value: _Optional[str] = ...,
    ) -> None: ...

class KubernetesHorizontalPodAutoscalerMetricSpec(_message.Message):
    __slots__ = ("type", "object", "pods", "resource", "container_resource", "external")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    type: str
    object: KubernetesHPAObjectMetricSource
    pods: KubernetesHPAPodsMetricSource
    resource: KubernetesHPAResourceMetricSource
    container_resource: KubernetesHPAContainerResourceMetricSource
    external: KubernetesHPAExternalMetricSource
    def __init__(
        self,
        type: _Optional[str] = ...,
        object: _Optional[_Union[KubernetesHPAObjectMetricSource, _Mapping]] = ...,
        pods: _Optional[_Union[KubernetesHPAPodsMetricSource, _Mapping]] = ...,
        resource: _Optional[_Union[KubernetesHPAResourceMetricSource, _Mapping]] = ...,
        container_resource: _Optional[_Union[KubernetesHPAContainerResourceMetricSource, _Mapping]] = ...,
        external: _Optional[_Union[KubernetesHPAExternalMetricSource, _Mapping]] = ...,
    ) -> None: ...

class KubernetesHPAObjectMetricStatus(_message.Message):
    __slots__ = ("target", "metric_name", "current_value", "selector", "average_value")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_VALUE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    target: KubernetesHorizontalPodAutoscalerTargetRef
    metric_name: str
    current_value: str
    selector: KubernetesLabelSelector
    average_value: str
    def __init__(
        self,
        target: _Optional[_Union[KubernetesHorizontalPodAutoscalerTargetRef, _Mapping]] = ...,
        metric_name: _Optional[str] = ...,
        current_value: _Optional[str] = ...,
        selector: _Optional[_Union[KubernetesLabelSelector, _Mapping]] = ...,
        average_value: _Optional[str] = ...,
    ) -> None: ...

class KubernetesHPAPodsMetricStatus(_message.Message):
    __slots__ = ("metric_name", "current_average_value", "selector")
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    metric_name: str
    current_average_value: str
    selector: KubernetesLabelSelector
    def __init__(
        self,
        metric_name: _Optional[str] = ...,
        current_average_value: _Optional[str] = ...,
        selector: _Optional[_Union[KubernetesLabelSelector, _Mapping]] = ...,
    ) -> None: ...

class KubernetesHPAResourceMetricStatus(_message.Message):
    __slots__ = ("name", "current_average_utilization", "current_average_value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_AVERAGE_UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    CURRENT_AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    current_average_utilization: int
    current_average_value: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        current_average_utilization: _Optional[int] = ...,
        current_average_value: _Optional[str] = ...,
    ) -> None: ...

class KubernetesHPAContainerResourceMetricStatus(_message.Message):
    __slots__ = ("name", "current_average_utilization", "current_average_value", "container")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_AVERAGE_UTILIZATION_FIELD_NUMBER: _ClassVar[int]
    CURRENT_AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_FIELD_NUMBER: _ClassVar[int]
    name: str
    current_average_utilization: int
    current_average_value: str
    container: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        current_average_utilization: _Optional[int] = ...,
        current_average_value: _Optional[str] = ...,
        container: _Optional[str] = ...,
    ) -> None: ...

class KubernetesHPAExternalMetricStatus(_message.Message):
    __slots__ = ("metric_name", "metric_selector", "current_value", "current_average_value")
    METRIC_NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    CURRENT_VALUE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_AVERAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    metric_name: str
    metric_selector: KubernetesLabelSelector
    current_value: str
    current_average_value: str
    def __init__(
        self,
        metric_name: _Optional[str] = ...,
        metric_selector: _Optional[_Union[KubernetesLabelSelector, _Mapping]] = ...,
        current_value: _Optional[str] = ...,
        current_average_value: _Optional[str] = ...,
    ) -> None: ...

class KubernetesHorizontalPodAutoscalerMetricStatus(_message.Message):
    __slots__ = ("type", "object", "pods", "resource", "container_resource", "external")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    type: str
    object: KubernetesHPAObjectMetricStatus
    pods: KubernetesHPAPodsMetricStatus
    resource: KubernetesHPAResourceMetricStatus
    container_resource: KubernetesHPAContainerResourceMetricStatus
    external: KubernetesHPAExternalMetricStatus
    def __init__(
        self,
        type: _Optional[str] = ...,
        object: _Optional[_Union[KubernetesHPAObjectMetricStatus, _Mapping]] = ...,
        pods: _Optional[_Union[KubernetesHPAPodsMetricStatus, _Mapping]] = ...,
        resource: _Optional[_Union[KubernetesHPAResourceMetricStatus, _Mapping]] = ...,
        container_resource: _Optional[_Union[KubernetesHPAContainerResourceMetricStatus, _Mapping]] = ...,
        external: _Optional[_Union[KubernetesHPAExternalMetricStatus, _Mapping]] = ...,
    ) -> None: ...

class KubernetesHorizontalPodAutoscalerCondition(_message.Message):
    __slots__ = ("type", "status", "last_transition_time", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LAST_TRANSITION_TIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    last_transition_time: int
    reason: str
    message: str
    def __init__(
        self,
        type: _Optional[str] = ...,
        status: _Optional[str] = ...,
        last_transition_time: _Optional[int] = ...,
        reason: _Optional[str] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class KubernetesHorizontalPodAutoscalerSpec(_message.Message):
    __slots__ = ("scale_target_ref", "min_replicas", "max_replicas", "target_cpu_utilization_percentage")
    SCALE_TARGET_REF_FIELD_NUMBER: _ClassVar[int]
    MIN_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    MAX_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    TARGET_CPU_UTILIZATION_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    scale_target_ref: KubernetesHorizontalPodAutoscalerTargetRef
    min_replicas: int
    max_replicas: int
    target_cpu_utilization_percentage: int
    def __init__(
        self,
        scale_target_ref: _Optional[_Union[KubernetesHorizontalPodAutoscalerTargetRef, _Mapping]] = ...,
        min_replicas: _Optional[int] = ...,
        max_replicas: _Optional[int] = ...,
        target_cpu_utilization_percentage: _Optional[int] = ...,
    ) -> None: ...

class KubernetesHorizontalPodAutoscalerStatus(_message.Message):
    __slots__ = (
        "observed_generation",
        "last_scale_time",
        "current_replicas",
        "desired_replicas",
        "current_cpu_utilization_percentage",
        "conditions",
    )
    OBSERVED_GENERATION_FIELD_NUMBER: _ClassVar[int]
    LAST_SCALE_TIME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    DESIRED_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_CPU_UTILIZATION_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    observed_generation: int
    last_scale_time: _timestamp_pb2.Timestamp
    current_replicas: int
    desired_replicas: int
    current_cpu_utilization_percentage: int
    conditions: _containers.RepeatedCompositeFieldContainer[KubernetesHorizontalPodAutoscalerCondition]
    def __init__(
        self,
        observed_generation: _Optional[int] = ...,
        last_scale_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        current_replicas: _Optional[int] = ...,
        desired_replicas: _Optional[int] = ...,
        current_cpu_utilization_percentage: _Optional[int] = ...,
        conditions: _Optional[_Iterable[_Union[KubernetesHorizontalPodAutoscalerCondition, _Mapping]]] = ...,
    ) -> None: ...

class KubernetesHorizontalPodAutoscaler(_message.Message):
    __slots__ = ("name", "namespace", "labels", "annotations", "creation_timestamp", "spec", "status", "cluster_name")
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class AnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    creation_timestamp: int
    spec: KubernetesHorizontalPodAutoscalerSpec
    status: KubernetesHorizontalPodAutoscalerStatus
    cluster_name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        annotations: _Optional[_Mapping[str, str]] = ...,
        creation_timestamp: _Optional[int] = ...,
        spec: _Optional[_Union[KubernetesHorizontalPodAutoscalerSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesHorizontalPodAutoscalerStatus, _Mapping]] = ...,
        cluster_name: _Optional[str] = ...,
    ) -> None: ...
