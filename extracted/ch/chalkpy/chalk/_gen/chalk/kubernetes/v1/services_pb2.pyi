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

class KubernetesServicePort(_message.Message):
    __slots__ = ("name", "protocol", "port", "target_port")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TARGET_PORT_FIELD_NUMBER: _ClassVar[int]
    name: str
    protocol: str
    port: int
    target_port: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        protocol: _Optional[str] = ...,
        port: _Optional[int] = ...,
        target_port: _Optional[str] = ...,
    ) -> None: ...

class KubernetesService(_message.Message):
    __slots__ = (
        "name",
        "namespace",
        "uid",
        "labels",
        "annotations",
        "creation_timestamp",
        "cluster_name",
        "type",
        "cluster_ip",
        "selector",
        "ports",
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

    class SelectorEntry(_message.Message):
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
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_IP_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    uid: str
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    creation_timestamp: int
    cluster_name: str
    type: str
    cluster_ip: str
    selector: _containers.ScalarMap[str, str]
    ports: _containers.RepeatedCompositeFieldContainer[KubernetesServicePort]
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        uid: _Optional[str] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        annotations: _Optional[_Mapping[str, str]] = ...,
        creation_timestamp: _Optional[int] = ...,
        cluster_name: _Optional[str] = ...,
        type: _Optional[str] = ...,
        cluster_ip: _Optional[str] = ...,
        selector: _Optional[_Mapping[str, str]] = ...,
        ports: _Optional[_Iterable[_Union[KubernetesServicePort, _Mapping]]] = ...,
    ) -> None: ...
