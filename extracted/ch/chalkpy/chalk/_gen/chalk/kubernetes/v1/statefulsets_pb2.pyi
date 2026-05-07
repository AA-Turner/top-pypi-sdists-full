from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesStatefulSetSpec(_message.Message):
    __slots__ = ("replicas", "service_name", "update_strategy", "min_ready_seconds")
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    MIN_READY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    replicas: int
    service_name: str
    update_strategy: str
    min_ready_seconds: int
    def __init__(
        self,
        replicas: _Optional[int] = ...,
        service_name: _Optional[str] = ...,
        update_strategy: _Optional[str] = ...,
        min_ready_seconds: _Optional[int] = ...,
    ) -> None: ...

class KubernetesStatefulSetStatus(_message.Message):
    __slots__ = (
        "observed_generation",
        "replicas",
        "ready_replicas",
        "available_replicas",
        "current_replicas",
        "updated_replicas",
        "current_revision",
        "update_revision",
    )
    OBSERVED_GENERATION_FIELD_NUMBER: _ClassVar[int]
    REPLICAS_FIELD_NUMBER: _ClassVar[int]
    READY_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    AVAILABLE_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_REVISION_FIELD_NUMBER: _ClassVar[int]
    UPDATE_REVISION_FIELD_NUMBER: _ClassVar[int]
    observed_generation: int
    replicas: int
    ready_replicas: int
    available_replicas: int
    current_replicas: int
    updated_replicas: int
    current_revision: str
    update_revision: str
    def __init__(
        self,
        observed_generation: _Optional[int] = ...,
        replicas: _Optional[int] = ...,
        ready_replicas: _Optional[int] = ...,
        available_replicas: _Optional[int] = ...,
        current_replicas: _Optional[int] = ...,
        updated_replicas: _Optional[int] = ...,
        current_revision: _Optional[str] = ...,
        update_revision: _Optional[str] = ...,
    ) -> None: ...

class KubernetesStatefulSet(_message.Message):
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
    name: str
    namespace: str
    uid: str
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    creation_timestamp: int
    cluster_name: str
    spec: KubernetesStatefulSetSpec
    status: KubernetesStatefulSetStatus
    match_labels: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        uid: _Optional[str] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        annotations: _Optional[_Mapping[str, str]] = ...,
        creation_timestamp: _Optional[int] = ...,
        cluster_name: _Optional[str] = ...,
        spec: _Optional[_Union[KubernetesStatefulSetSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesStatefulSetStatus, _Mapping]] = ...,
        match_labels: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...
