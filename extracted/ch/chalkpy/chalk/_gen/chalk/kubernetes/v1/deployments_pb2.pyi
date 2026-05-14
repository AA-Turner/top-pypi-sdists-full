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

class KubernetesDeploymentCondition(_message.Message):
    __slots__ = ("type", "status", "reason", "message", "last_transition_time", "last_update_time")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_TRANSITION_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    reason: str
    message: str
    last_transition_time: int
    last_update_time: int
    def __init__(
        self,
        type: _Optional[str] = ...,
        status: _Optional[str] = ...,
        reason: _Optional[str] = ...,
        message: _Optional[str] = ...,
        last_transition_time: _Optional[int] = ...,
        last_update_time: _Optional[int] = ...,
    ) -> None: ...

class KubernetesDeploymentSpec(_message.Message):
    __slots__ = ("replicas", "strategy", "min_ready_seconds", "progress_deadline_seconds")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    STRATEGY_FIELD_NUMBER: _ClassVar[int]
    MIN_READY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_DEADLINE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    strategy: str
    min_ready_seconds: int
    progress_deadline_seconds: int
    def __init__(
        self,
        replicas: _Optional[int] = ...,
        strategy: _Optional[str] = ...,
        min_ready_seconds: _Optional[int] = ...,
        progress_deadline_seconds: _Optional[int] = ...,
    ) -> None: ...

class KubernetesDeploymentStatus(_message.Message):
    __slots__ = (
        "observed_generation",
        "replicas",
        "updated_replicas",
        "ready_replicas",
        "available_replicas",
        "unavailable_replicas",
        "conditions",
    )
    OBSERVED_GENERATION_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    READY_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    UNAVAILABLE_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    observed_generation: int
    replicas: int
    updated_replicas: int
    ready_replicas: int
    available_replicas: int
    unavailable_replicas: int
    conditions: _containers.RepeatedCompositeFieldContainer[KubernetesDeploymentCondition]
    def __init__(
        self,
        observed_generation: _Optional[int] = ...,
        replicas: _Optional[int] = ...,
        updated_replicas: _Optional[int] = ...,
        ready_replicas: _Optional[int] = ...,
        available_replicas: _Optional[int] = ...,
        unavailable_replicas: _Optional[int] = ...,
        conditions: _Optional[_Iterable[_Union[KubernetesDeploymentCondition, _Mapping]]] = ...,
    ) -> None: ...

class KubernetesReplicaSetRef(_message.Message):
    __slots__ = ("uid", "name")
    UID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    uid: str
    name: str
    def __init__(self, uid: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class KubernetesDeployment(_message.Message):
    __slots__ = (
        "name",
        "namespace",
        "uid",
        "labels",
        "annotations",
        "creation_timestamp",
        "cluster_name",
        "spec",
        "status",
        "match_labels",
        "replica_sets",
    )
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

    class MatchLabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MATCH_LABELS_FIELD_NUMBER: _ClassVar[int]
    REPLICA_SETS_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    uid: str
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    creation_timestamp: int
    cluster_name: str
    spec: KubernetesDeploymentSpec
    status: KubernetesDeploymentStatus
    match_labels: _containers.ScalarMap[str, str]
    replica_sets: _containers.RepeatedCompositeFieldContainer[KubernetesReplicaSetRef]
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        uid: _Optional[str] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        annotations: _Optional[_Mapping[str, str]] = ...,
        creation_timestamp: _Optional[int] = ...,
        cluster_name: _Optional[str] = ...,
        spec: _Optional[_Union[KubernetesDeploymentSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesDeploymentStatus, _Mapping]] = ...,
        match_labels: _Optional[_Mapping[str, str]] = ...,
        replica_sets: _Optional[_Iterable[_Union[KubernetesReplicaSetRef, _Mapping]]] = ...,
    ) -> None: ...
