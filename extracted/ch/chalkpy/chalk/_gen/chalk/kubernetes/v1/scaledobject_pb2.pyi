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

class KubernetesScaledObjectTargetRef(_message.Message):
    __slots__ = ("name", "api_version", "kind", "env_source_container_name")
    NAME_FIELD_NUMBER: _ClassVar[int]
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    ENV_SOURCE_CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    api_version: str
    kind: str
    env_source_container_name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        api_version: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        env_source_container_name: _Optional[str] = ...,
    ) -> None: ...

class KubernetesGroupVersionKindResource(_message.Message):
    __slots__ = ("group", "version", "kind", "resource")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    group: str
    version: str
    kind: str
    resource: str
    def __init__(
        self,
        group: _Optional[str] = ...,
        version: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        resource: _Optional[str] = ...,
    ) -> None: ...

class KubernetesScaledObjectCondition(_message.Message):
    __slots__ = ("type", "status", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    reason: str
    message: str
    def __init__(
        self,
        type: _Optional[str] = ...,
        status: _Optional[str] = ...,
        reason: _Optional[str] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class KubernetesScaledObjectHealthStatus(_message.Message):
    __slots__ = ("number_of_failures", "status")
    NUMBER_OF_FAILURES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    number_of_failures: int
    status: str
    def __init__(self, number_of_failures: _Optional[int] = ..., status: _Optional[str] = ...) -> None: ...

class KubernetesScaledObjectAuthenticationRef(_message.Message):
    __slots__ = ("name", "kind")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: str
    def __init__(self, name: _Optional[str] = ..., kind: _Optional[str] = ...) -> None: ...

class KubernetesScaledObjectTrigger(_message.Message):
    __slots__ = ("type", "name", "use_cached_metrics", "metadata", "authentication_ref", "metric_type")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USE_CACHED_METRICS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_REF_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    name: str
    use_cached_metrics: bool
    metadata: _containers.ScalarMap[str, str]
    authentication_ref: KubernetesScaledObjectAuthenticationRef
    metric_type: str
    def __init__(
        self,
        type: _Optional[str] = ...,
        name: _Optional[str] = ...,
        use_cached_metrics: bool = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
        authentication_ref: _Optional[_Union[KubernetesScaledObjectAuthenticationRef, _Mapping]] = ...,
        metric_type: _Optional[str] = ...,
    ) -> None: ...

class KubernetesScaledObjectFallback(_message.Message):
    __slots__ = ("failure_threshold", "replicas")
    FAILURE_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    failure_threshold: int
    replicas: int
    def __init__(self, failure_threshold: _Optional[int] = ..., replicas: _Optional[int] = ...) -> None: ...

class KubernetesScaledObjectScalingModifiers(_message.Message):
    __slots__ = ("formula", "target", "activation_target", "metric_type")
    FORMULA_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    ACTIVATION_TARGET_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    formula: str
    target: str
    activation_target: str
    metric_type: str
    def __init__(
        self,
        formula: _Optional[str] = ...,
        target: _Optional[str] = ...,
        activation_target: _Optional[str] = ...,
        metric_type: _Optional[str] = ...,
    ) -> None: ...

class KubernetesScaledObjectHPAConfig(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class KubernetesScaledObjectAdvancedConfig(_message.Message):
    __slots__ = ("horizontal_pod_autoscaler_config", "restore_to_original_replica_count", "scaling_modifiers")
    HORIZONTAL_POD_AUTOSCALER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    RESTORE_TO_ORIGINAL_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    SCALING_MODIFIERS_FIELD_NUMBER: _ClassVar[int]
    horizontal_pod_autoscaler_config: KubernetesScaledObjectHPAConfig
    restore_to_original_replica_count: bool
    scaling_modifiers: KubernetesScaledObjectScalingModifiers
    def __init__(
        self,
        horizontal_pod_autoscaler_config: _Optional[_Union[KubernetesScaledObjectHPAConfig, _Mapping]] = ...,
        restore_to_original_replica_count: bool = ...,
        scaling_modifiers: _Optional[_Union[KubernetesScaledObjectScalingModifiers, _Mapping]] = ...,
    ) -> None: ...

class KubernetesScaledObjectStatus(_message.Message):
    __slots__ = (
        "scale_target_kind",
        "scale_target_gvkr",
        "original_replica_count",
        "last_active_time",
        "external_metric_names",
        "resource_metric_names",
        "composite_scaler_name",
        "conditions",
        "health",
        "paused_replica_count",
        "hpa_name",
        "triggers_types",
        "authentications_types",
    )
    class HealthEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: KubernetesScaledObjectHealthStatus
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[KubernetesScaledObjectHealthStatus, _Mapping]] = ...,
        ) -> None: ...

    SCALE_TARGET_KIND_FIELD_NUMBER: _ClassVar[int]
    SCALE_TARGET_GVKR_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_ACTIVE_TIME_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_METRIC_NAMES_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_METRIC_NAMES_FIELD_NUMBER: _ClassVar[int]
    COMPOSITE_SCALER_NAME_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    PAUSED_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    HPA_NAME_FIELD_NUMBER: _ClassVar[int]
    TRIGGERS_TYPES_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATIONS_TYPES_FIELD_NUMBER: _ClassVar[int]
    scale_target_kind: str
    scale_target_gvkr: KubernetesGroupVersionKindResource
    original_replica_count: int
    last_active_time: _timestamp_pb2.Timestamp
    external_metric_names: _containers.RepeatedScalarFieldContainer[str]
    resource_metric_names: _containers.RepeatedScalarFieldContainer[str]
    composite_scaler_name: str
    conditions: _containers.RepeatedCompositeFieldContainer[KubernetesScaledObjectCondition]
    health: _containers.MessageMap[str, KubernetesScaledObjectHealthStatus]
    paused_replica_count: int
    hpa_name: str
    triggers_types: str
    authentications_types: str
    def __init__(
        self,
        scale_target_kind: _Optional[str] = ...,
        scale_target_gvkr: _Optional[_Union[KubernetesGroupVersionKindResource, _Mapping]] = ...,
        original_replica_count: _Optional[int] = ...,
        last_active_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        external_metric_names: _Optional[_Iterable[str]] = ...,
        resource_metric_names: _Optional[_Iterable[str]] = ...,
        composite_scaler_name: _Optional[str] = ...,
        conditions: _Optional[_Iterable[_Union[KubernetesScaledObjectCondition, _Mapping]]] = ...,
        health: _Optional[_Mapping[str, KubernetesScaledObjectHealthStatus]] = ...,
        paused_replica_count: _Optional[int] = ...,
        hpa_name: _Optional[str] = ...,
        triggers_types: _Optional[str] = ...,
        authentications_types: _Optional[str] = ...,
    ) -> None: ...

class KubernetesScaledObjectSpec(_message.Message):
    __slots__ = (
        "scale_target_ref",
        "polling_interval",
        "initial_cooldown_period",
        "cooldown_period",
        "idle_replica_count",
        "max_replica_count",
        "advanced",
        "triggers",
        "fallback",
        "min_replica_count",
    )
    SCALE_TARGET_REF_FIELD_NUMBER: _ClassVar[int]
    POLLING_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    INITIAL_COOLDOWN_PERIOD_FIELD_NUMBER: _ClassVar[int]
    COOLDOWN_PERIOD_FIELD_NUMBER: _ClassVar[int]
    IDLE_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    ADVANCED_FIELD_NUMBER: _ClassVar[int]
    TRIGGERS_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_FIELD_NUMBER: _ClassVar[int]
    MIN_REPLICA_COUNT_FIELD_NUMBER: _ClassVar[int]
    scale_target_ref: KubernetesScaledObjectTargetRef
    polling_interval: int
    initial_cooldown_period: int
    cooldown_period: int
    idle_replica_count: int
    max_replica_count: int
    advanced: KubernetesScaledObjectAdvancedConfig
    triggers: _containers.RepeatedCompositeFieldContainer[KubernetesScaledObjectTrigger]
    fallback: KubernetesScaledObjectFallback
    min_replica_count: int
    def __init__(
        self,
        scale_target_ref: _Optional[_Union[KubernetesScaledObjectTargetRef, _Mapping]] = ...,
        polling_interval: _Optional[int] = ...,
        initial_cooldown_period: _Optional[int] = ...,
        cooldown_period: _Optional[int] = ...,
        idle_replica_count: _Optional[int] = ...,
        max_replica_count: _Optional[int] = ...,
        advanced: _Optional[_Union[KubernetesScaledObjectAdvancedConfig, _Mapping]] = ...,
        triggers: _Optional[_Iterable[_Union[KubernetesScaledObjectTrigger, _Mapping]]] = ...,
        fallback: _Optional[_Union[KubernetesScaledObjectFallback, _Mapping]] = ...,
        min_replica_count: _Optional[int] = ...,
    ) -> None: ...

class KubernetesScaledObjectData(_message.Message):
    __slots__ = ("spec", "status")
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    spec: KubernetesScaledObjectSpec
    status: KubernetesScaledObjectStatus
    def __init__(
        self,
        spec: _Optional[_Union[KubernetesScaledObjectSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesScaledObjectStatus, _Mapping]] = ...,
    ) -> None: ...

class KubernetesScaledObject(_message.Message):
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
    spec: KubernetesScaledObjectSpec
    status: KubernetesScaledObjectStatus
    cluster_name: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        annotations: _Optional[_Mapping[str, str]] = ...,
        creation_timestamp: _Optional[int] = ...,
        spec: _Optional[_Union[KubernetesScaledObjectSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesScaledObjectStatus, _Mapping]] = ...,
        cluster_name: _Optional[str] = ...,
    ) -> None: ...
