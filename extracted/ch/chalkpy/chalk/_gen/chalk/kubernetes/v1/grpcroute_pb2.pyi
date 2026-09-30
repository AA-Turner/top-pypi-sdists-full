from chalk._gen.chalk.kubernetes.v1 import routes_pb2 as _routes_pb2
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

class KubernetesGRPCMethodMatch(_message.Message):
    __slots__ = ("type", "service", "method")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    type: str
    service: str
    method: str
    def __init__(
        self, type: _Optional[str] = ..., service: _Optional[str] = ..., method: _Optional[str] = ...
    ) -> None: ...

class KubernetesGRPCHeaderMatch(_message.Message):
    __slots__ = ("type", "name", "value")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: str
    name: str
    value: str
    def __init__(self, type: _Optional[str] = ..., name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class KubernetesGRPCRouteMatch(_message.Message):
    __slots__ = ("method", "headers")
    METHOD_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    method: KubernetesGRPCMethodMatch
    headers: _containers.RepeatedCompositeFieldContainer[KubernetesGRPCHeaderMatch]
    def __init__(
        self,
        method: _Optional[_Union[KubernetesGRPCMethodMatch, _Mapping]] = ...,
        headers: _Optional[_Iterable[_Union[KubernetesGRPCHeaderMatch, _Mapping]]] = ...,
    ) -> None: ...

class KubernetesGRPCRouteRule(_message.Message):
    __slots__ = ("name", "matches", "filter_types", "backend_refs")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    FILTER_TYPES_FIELD_NUMBER: _ClassVar[int]
    BACKEND_REFS_FIELD_NUMBER: _ClassVar[int]
    name: str
    matches: _containers.RepeatedCompositeFieldContainer[KubernetesGRPCRouteMatch]
    filter_types: _containers.RepeatedScalarFieldContainer[str]
    backend_refs: _containers.RepeatedCompositeFieldContainer[_routes_pb2.KubernetesRouteBackendReference]
    def __init__(
        self,
        name: _Optional[str] = ...,
        matches: _Optional[_Iterable[_Union[KubernetesGRPCRouteMatch, _Mapping]]] = ...,
        filter_types: _Optional[_Iterable[str]] = ...,
        backend_refs: _Optional[_Iterable[_Union[_routes_pb2.KubernetesRouteBackendReference, _Mapping]]] = ...,
    ) -> None: ...

class KubernetesGRPCRouteSpec(_message.Message):
    __slots__ = ("parent_refs", "hostnames", "rules")
    PARENT_REFS_FIELD_NUMBER: _ClassVar[int]
    HOSTNAMES_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    parent_refs: _containers.RepeatedCompositeFieldContainer[_routes_pb2.KubernetesRouteParentReference]
    hostnames: _containers.RepeatedScalarFieldContainer[str]
    rules: _containers.RepeatedCompositeFieldContainer[KubernetesGRPCRouteRule]
    def __init__(
        self,
        parent_refs: _Optional[_Iterable[_Union[_routes_pb2.KubernetesRouteParentReference, _Mapping]]] = ...,
        hostnames: _Optional[_Iterable[str]] = ...,
        rules: _Optional[_Iterable[_Union[KubernetesGRPCRouteRule, _Mapping]]] = ...,
    ) -> None: ...

class KubernetesGRPCRouteStatus(_message.Message):
    __slots__ = ("parents",)
    PARENTS_FIELD_NUMBER: _ClassVar[int]
    parents: _containers.RepeatedCompositeFieldContainer[_routes_pb2.KubernetesRouteParentStatus]
    def __init__(
        self, parents: _Optional[_Iterable[_Union[_routes_pb2.KubernetesRouteParentStatus, _Mapping]]] = ...
    ) -> None: ...

class KubernetesGRPCRoute(_message.Message):
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

    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    uid: str
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    creation_timestamp: int
    cluster_name: str
    spec: KubernetesGRPCRouteSpec
    status: KubernetesGRPCRouteStatus
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        uid: _Optional[str] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        annotations: _Optional[_Mapping[str, str]] = ...,
        creation_timestamp: _Optional[int] = ...,
        cluster_name: _Optional[str] = ...,
        spec: _Optional[_Union[KubernetesGRPCRouteSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesGRPCRouteStatus, _Mapping]] = ...,
    ) -> None: ...
