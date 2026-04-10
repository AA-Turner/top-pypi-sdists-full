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

class KubernetesJobCondition(_message.Message):
    __slots__ = ("type", "status", "reason", "message", "last_transition_time", "last_probe_time")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_TRANSITION_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_PROBE_TIME_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    reason: str
    message: str
    last_transition_time: int
    last_probe_time: int
    def __init__(
        self,
        type: _Optional[str] = ...,
        status: _Optional[str] = ...,
        reason: _Optional[str] = ...,
        message: _Optional[str] = ...,
        last_transition_time: _Optional[int] = ...,
        last_probe_time: _Optional[int] = ...,
    ) -> None: ...

class KubernetesJobSpec(_message.Message):
    __slots__ = ("completions", "parallelism", "backoff_limit", "active_deadline_seconds", "ttl_seconds_after_finished")
    COMPLETIONS_FIELD_NUMBER: _ClassVar[int]
    PARALLELISM_FIELD_NUMBER: _ClassVar[int]
    BACKOFF_LIMIT_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_DEADLINE_SECONDS_FIELD_NUMBER: _ClassVar[int]
    TTL_SECONDS_AFTER_FINISHED_FIELD_NUMBER: _ClassVar[int]
    completions: int
    parallelism: int
    backoff_limit: int
    active_deadline_seconds: int
    ttl_seconds_after_finished: int
    def __init__(
        self,
        completions: _Optional[int] = ...,
        parallelism: _Optional[int] = ...,
        backoff_limit: _Optional[int] = ...,
        active_deadline_seconds: _Optional[int] = ...,
        ttl_seconds_after_finished: _Optional[int] = ...,
    ) -> None: ...

class KubernetesJobStatus(_message.Message):
    __slots__ = ("conditions", "start_time", "completion_time", "active", "succeeded", "failed", "ready")
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TIME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[KubernetesJobCondition]
    start_time: int
    completion_time: int
    active: int
    succeeded: int
    failed: int
    ready: int
    def __init__(
        self,
        conditions: _Optional[_Iterable[_Union[KubernetesJobCondition, _Mapping]]] = ...,
        start_time: _Optional[int] = ...,
        completion_time: _Optional[int] = ...,
        active: _Optional[int] = ...,
        succeeded: _Optional[int] = ...,
        failed: _Optional[int] = ...,
        ready: _Optional[int] = ...,
    ) -> None: ...

class KubernetesJob(_message.Message):
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
    spec: KubernetesJobSpec
    status: KubernetesJobStatus
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
        spec: _Optional[_Union[KubernetesJobSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesJobStatus, _Mapping]] = ...,
        match_labels: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...
