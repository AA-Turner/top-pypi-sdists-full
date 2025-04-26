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

class KubernetesNodeTaint(_message.Message):
    __slots__ = ("key", "value", "effect", "time_added")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    TIME_ADDED_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    effect: str
    time_added: int
    def __init__(
        self,
        key: _Optional[str] = ...,
        value: _Optional[str] = ...,
        effect: _Optional[str] = ...,
        time_added: _Optional[int] = ...,
    ) -> None: ...

class KubernetesNodeSpec(_message.Message):
    __slots__ = ("pod_cidr", "taints", "pod_cidrs", "provider_id", "unschedulable")
    POD_CIDR_FIELD_NUMBER: _ClassVar[int]
    TAINTS_FIELD_NUMBER: _ClassVar[int]
    POD_CIDRS_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_ID_FIELD_NUMBER: _ClassVar[int]
    UNSCHEDULABLE_FIELD_NUMBER: _ClassVar[int]
    pod_cidr: str
    taints: _containers.RepeatedCompositeFieldContainer[KubernetesNodeTaint]
    pod_cidrs: _containers.RepeatedScalarFieldContainer[str]
    provider_id: str
    unschedulable: bool
    def __init__(
        self,
        pod_cidr: _Optional[str] = ...,
        taints: _Optional[_Iterable[_Union[KubernetesNodeTaint, _Mapping]]] = ...,
        pod_cidrs: _Optional[_Iterable[str]] = ...,
        provider_id: _Optional[str] = ...,
        unschedulable: bool = ...,
    ) -> None: ...

class KubernetesNodeCondition(_message.Message):
    __slots__ = ("type", "status", "last_heartbeat_time", "last_transition_time", "reason", "message")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LAST_HEARTBEAT_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_TRANSITION_TIME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    last_heartbeat_time: int
    last_transition_time: int
    reason: str
    message: str
    def __init__(
        self,
        type: _Optional[str] = ...,
        status: _Optional[str] = ...,
        last_heartbeat_time: _Optional[int] = ...,
        last_transition_time: _Optional[int] = ...,
        reason: _Optional[str] = ...,
        message: _Optional[str] = ...,
    ) -> None: ...

class KubernetesAttachedVolume(_message.Message):
    __slots__ = ("name", "device_path")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DEVICE_PATH_FIELD_NUMBER: _ClassVar[int]
    name: str
    device_path: str
    def __init__(self, name: _Optional[str] = ..., device_path: _Optional[str] = ...) -> None: ...

class KubernetesNodeStatus(_message.Message):
    __slots__ = ("conditions", "volumes_in_use", "volumes_attached")
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    VOLUMES_IN_USE_FIELD_NUMBER: _ClassVar[int]
    VOLUMES_ATTACHED_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[KubernetesNodeCondition]
    volumes_in_use: _containers.RepeatedScalarFieldContainer[str]
    volumes_attached: _containers.RepeatedCompositeFieldContainer[KubernetesAttachedVolume]
    def __init__(
        self,
        conditions: _Optional[_Iterable[_Union[KubernetesNodeCondition, _Mapping]]] = ...,
        volumes_in_use: _Optional[_Iterable[str]] = ...,
        volumes_attached: _Optional[_Iterable[_Union[KubernetesAttachedVolume, _Mapping]]] = ...,
    ) -> None: ...

class KubernetesNodeData(_message.Message):
    __slots__ = (
        "team",
        "name",
        "uid",
        "instance_type",
        "region",
        "zone",
        "creation_timestamp",
        "deletion_timestamp",
        "observed_timestamp",
        "labels",
        "annotations",
        "machine_id",
        "system_uuid",
        "boot_id",
        "unschedulable",
        "namespace",
        "instance_id",
        "cluster",
        "total_cpu",
        "total_memory",
        "allocatable_cpu",
        "allocatable_memory",
        "spec",
        "status",
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

    TEAM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DELETION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_UUID_FIELD_NUMBER: _ClassVar[int]
    BOOT_ID_FIELD_NUMBER: _ClassVar[int]
    UNSCHEDULABLE_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CPU_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MEMORY_FIELD_NUMBER: _ClassVar[int]
    ALLOCATABLE_CPU_FIELD_NUMBER: _ClassVar[int]
    ALLOCATABLE_MEMORY_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    team: str
    name: str
    uid: str
    instance_type: str
    region: str
    zone: str
    creation_timestamp: int
    deletion_timestamp: int
    observed_timestamp: int
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    machine_id: str
    system_uuid: str
    boot_id: str
    unschedulable: bool
    namespace: str
    instance_id: str
    cluster: str
    total_cpu: str
    total_memory: str
    allocatable_cpu: str
    allocatable_memory: str
    spec: KubernetesNodeSpec
    status: KubernetesNodeStatus
    def __init__(
        self,
        team: _Optional[str] = ...,
        name: _Optional[str] = ...,
        uid: _Optional[str] = ...,
        instance_type: _Optional[str] = ...,
        region: _Optional[str] = ...,
        zone: _Optional[str] = ...,
        creation_timestamp: _Optional[int] = ...,
        deletion_timestamp: _Optional[int] = ...,
        observed_timestamp: _Optional[int] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        annotations: _Optional[_Mapping[str, str]] = ...,
        machine_id: _Optional[str] = ...,
        system_uuid: _Optional[str] = ...,
        boot_id: _Optional[str] = ...,
        unschedulable: bool = ...,
        namespace: _Optional[str] = ...,
        instance_id: _Optional[str] = ...,
        cluster: _Optional[str] = ...,
        total_cpu: _Optional[str] = ...,
        total_memory: _Optional[str] = ...,
        allocatable_cpu: _Optional[str] = ...,
        allocatable_memory: _Optional[str] = ...,
        spec: _Optional[_Union[KubernetesNodeSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesNodeStatus, _Mapping]] = ...,
    ) -> None: ...
