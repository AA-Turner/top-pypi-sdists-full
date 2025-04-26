from chalk._gen.chalk.kubernetes.v1 import nodes_pb2 as _nodes_pb2
from google.protobuf import duration_pb2 as _duration_pb2
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

class KarpenterNodepoolDisruptionBudget(_message.Message):
    __slots__ = ("nodes", "schedule", "duration")
    NODES_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    nodes: str
    schedule: str
    duration: _duration_pb2.Duration
    def __init__(
        self,
        nodes: _Optional[str] = ...,
        schedule: _Optional[str] = ...,
        duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class KarpenterNodepoolDisruption(_message.Message):
    __slots__ = ("consolidate_after", "consolidation_policy", "budgets")
    CONSOLIDATE_AFTER_FIELD_NUMBER: _ClassVar[int]
    CONSOLIDATION_POLICY_FIELD_NUMBER: _ClassVar[int]
    BUDGETS_FIELD_NUMBER: _ClassVar[int]
    consolidate_after: _duration_pb2.Duration
    consolidation_policy: str
    budgets: _containers.RepeatedCompositeFieldContainer[KarpenterNodepoolDisruptionBudget]
    def __init__(
        self,
        consolidate_after: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        consolidation_policy: _Optional[str] = ...,
        budgets: _Optional[_Iterable[_Union[KarpenterNodepoolDisruptionBudget, _Mapping]]] = ...,
    ) -> None: ...

class KarpenterNodeClassRef(_message.Message):
    __slots__ = ("name", "kind", "group")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: str
    group: str
    def __init__(self, name: _Optional[str] = ..., kind: _Optional[str] = ..., group: _Optional[str] = ...) -> None: ...

class KarpenterNodeSelectorRequirement(_message.Message):
    __slots__ = ("key", "operator", "values")
    KEY_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    key: str
    operator: str
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, key: _Optional[str] = ..., operator: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class KarpenterNodepoolTemplateSpec(_message.Message):
    __slots__ = (
        "taints",
        "startup_taints",
        "requirements",
        "node_class_ref",
        "expire_after",
        "termination_grace_period",
    )
    TAINTS_FIELD_NUMBER: _ClassVar[int]
    STARTUP_TAINTS_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    NODE_CLASS_REF_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_AFTER_FIELD_NUMBER: _ClassVar[int]
    TERMINATION_GRACE_PERIOD_FIELD_NUMBER: _ClassVar[int]
    taints: _containers.RepeatedCompositeFieldContainer[_nodes_pb2.KubernetesNodeTaint]
    startup_taints: _containers.RepeatedCompositeFieldContainer[_nodes_pb2.KubernetesNodeTaint]
    requirements: _containers.RepeatedCompositeFieldContainer[KarpenterNodeSelectorRequirement]
    node_class_ref: KarpenterNodeClassRef
    expire_after: _duration_pb2.Duration
    termination_grace_period: _duration_pb2.Duration
    def __init__(
        self,
        taints: _Optional[_Iterable[_Union[_nodes_pb2.KubernetesNodeTaint, _Mapping]]] = ...,
        startup_taints: _Optional[_Iterable[_Union[_nodes_pb2.KubernetesNodeTaint, _Mapping]]] = ...,
        requirements: _Optional[_Iterable[_Union[KarpenterNodeSelectorRequirement, _Mapping]]] = ...,
        node_class_ref: _Optional[_Union[KarpenterNodeClassRef, _Mapping]] = ...,
        expire_after: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        termination_grace_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class KarpenterNodepoolTemplateMetadata(_message.Message):
    __slots__ = ("labels", "annotations")
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

    LABELS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    def __init__(
        self, labels: _Optional[_Mapping[str, str]] = ..., annotations: _Optional[_Mapping[str, str]] = ...
    ) -> None: ...

class KarpenterNodepoolTemplate(_message.Message):
    __slots__ = ("metadata", "spec")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    metadata: KarpenterNodepoolTemplateMetadata
    spec: KarpenterNodepoolTemplateSpec
    def __init__(
        self,
        metadata: _Optional[_Union[KarpenterNodepoolTemplateMetadata, _Mapping]] = ...,
        spec: _Optional[_Union[KarpenterNodepoolTemplateSpec, _Mapping]] = ...,
    ) -> None: ...

class KarpenterNodepoolSpec(_message.Message):
    __slots__ = ("disruption", "template", "limits", "weight")
    class LimitsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    DISRUPTION_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    disruption: KarpenterNodepoolDisruption
    template: KarpenterNodepoolTemplate
    limits: _containers.ScalarMap[str, str]
    weight: int
    def __init__(
        self,
        disruption: _Optional[_Union[KarpenterNodepoolDisruption, _Mapping]] = ...,
        template: _Optional[_Union[KarpenterNodepoolTemplate, _Mapping]] = ...,
        limits: _Optional[_Mapping[str, str]] = ...,
        weight: _Optional[int] = ...,
    ) -> None: ...

class KarpenterNodepoolMetadata(_message.Message):
    __slots__ = ("annotations", "creation_timestamp", "generation", "name", "resource_version", "uid", "labels")
    class AnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    GENERATION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_VERSION_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    annotations: _containers.ScalarMap[str, str]
    creation_timestamp: _timestamp_pb2.Timestamp
    generation: int
    name: str
    resource_version: str
    uid: str
    labels: _containers.ScalarMap[str, str]
    def __init__(
        self,
        annotations: _Optional[_Mapping[str, str]] = ...,
        creation_timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        generation: _Optional[int] = ...,
        name: _Optional[str] = ...,
        resource_version: _Optional[str] = ...,
        uid: _Optional[str] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class KarpenterNodepoolCondition(_message.Message):
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

class KarpenterNodepoolStatus(_message.Message):
    __slots__ = ("resources", "conditions")
    class ResourcesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    resources: _containers.ScalarMap[str, str]
    conditions: _containers.RepeatedCompositeFieldContainer[KarpenterNodepoolCondition]
    def __init__(
        self,
        resources: _Optional[_Mapping[str, str]] = ...,
        conditions: _Optional[_Iterable[_Union[KarpenterNodepoolCondition, _Mapping]]] = ...,
    ) -> None: ...

class KarpenterNodepool(_message.Message):
    __slots__ = ("api_version", "kind", "metadata", "spec", "status")
    API_VERSION_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    api_version: str
    kind: str
    metadata: KarpenterNodepoolMetadata
    spec: KarpenterNodepoolSpec
    status: KarpenterNodepoolStatus
    def __init__(
        self,
        api_version: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        metadata: _Optional[_Union[KarpenterNodepoolMetadata, _Mapping]] = ...,
        spec: _Optional[_Union[KarpenterNodepoolSpec, _Mapping]] = ...,
        status: _Optional[_Union[KarpenterNodepoolStatus, _Mapping]] = ...,
    ) -> None: ...
