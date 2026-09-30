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

class KubernetesRouteParentReference(_message.Message):
    __slots__ = ("group", "kind", "namespace", "name", "section_name", "port")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    group: str
    kind: str
    namespace: str
    name: str
    section_name: str
    port: int
    def __init__(
        self,
        group: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        name: _Optional[str] = ...,
        section_name: _Optional[str] = ...,
        port: _Optional[int] = ...,
    ) -> None: ...

class KubernetesRouteBackendReference(_message.Message):
    __slots__ = ("group", "kind", "namespace", "name", "port", "weight")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    group: str
    kind: str
    namespace: str
    name: str
    port: int
    weight: int
    def __init__(
        self,
        group: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        name: _Optional[str] = ...,
        port: _Optional[int] = ...,
        weight: _Optional[int] = ...,
    ) -> None: ...

class KubernetesRouteCondition(_message.Message):
    __slots__ = ("type", "status", "reason", "message", "last_transition_time", "observed_generation")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LAST_TRANSITION_TIME_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_GENERATION_FIELD_NUMBER: _ClassVar[int]
    type: str
    status: str
    reason: str
    message: str
    last_transition_time: int
    observed_generation: int
    def __init__(
        self,
        type: _Optional[str] = ...,
        status: _Optional[str] = ...,
        reason: _Optional[str] = ...,
        message: _Optional[str] = ...,
        last_transition_time: _Optional[int] = ...,
        observed_generation: _Optional[int] = ...,
    ) -> None: ...

class KubernetesRouteParentStatus(_message.Message):
    __slots__ = ("parent_ref", "controller_name", "conditions")
    PARENT_REF_FIELD_NUMBER: _ClassVar[int]
    CONTROLLER_NAME_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    parent_ref: KubernetesRouteParentReference
    controller_name: str
    conditions: _containers.RepeatedCompositeFieldContainer[KubernetesRouteCondition]
    def __init__(
        self,
        parent_ref: _Optional[_Union[KubernetesRouteParentReference, _Mapping]] = ...,
        controller_name: _Optional[str] = ...,
        conditions: _Optional[_Iterable[_Union[KubernetesRouteCondition, _Mapping]]] = ...,
    ) -> None: ...
