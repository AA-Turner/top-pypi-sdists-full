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

class KubernetesHTTPPathMatch(_message.Message):
    __slots__ = ("type", "value")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: str
    value: str
    def __init__(self, type: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class KubernetesHTTPHeaderMatch(_message.Message):
    __slots__ = ("type", "name", "value")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: str
    name: str
    value: str
    def __init__(self, type: _Optional[str] = ..., name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class KubernetesHTTPQueryParamMatch(_message.Message):
    __slots__ = ("type", "name", "value")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    type: str
    name: str
    value: str
    def __init__(self, type: _Optional[str] = ..., name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class KubernetesHTTPRouteMatch(_message.Message):
    __slots__ = ("method", "path", "headers", "query_params")
    METHOD_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    QUERY_PARAMS_FIELD_NUMBER: _ClassVar[int]
    method: str
    path: KubernetesHTTPPathMatch
    headers: _containers.RepeatedCompositeFieldContainer[KubernetesHTTPHeaderMatch]
    query_params: _containers.RepeatedCompositeFieldContainer[KubernetesHTTPQueryParamMatch]
    def __init__(
        self,
        method: _Optional[str] = ...,
        path: _Optional[_Union[KubernetesHTTPPathMatch, _Mapping]] = ...,
        headers: _Optional[_Iterable[_Union[KubernetesHTTPHeaderMatch, _Mapping]]] = ...,
        query_params: _Optional[_Iterable[_Union[KubernetesHTTPQueryParamMatch, _Mapping]]] = ...,
    ) -> None: ...

class KubernetesHTTPRouteRule(_message.Message):
    __slots__ = ("name", "matches", "filter_types", "backend_refs", "request_timeout", "backend_request_timeout")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    FILTER_TYPES_FIELD_NUMBER: _ClassVar[int]
    BACKEND_REFS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    BACKEND_REQUEST_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    name: str
    matches: _containers.RepeatedCompositeFieldContainer[KubernetesHTTPRouteMatch]
    filter_types: _containers.RepeatedScalarFieldContainer[str]
    backend_refs: _containers.RepeatedCompositeFieldContainer[_routes_pb2.KubernetesRouteBackendReference]
    request_timeout: str
    backend_request_timeout: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        matches: _Optional[_Iterable[_Union[KubernetesHTTPRouteMatch, _Mapping]]] = ...,
        filter_types: _Optional[_Iterable[str]] = ...,
        backend_refs: _Optional[_Iterable[_Union[_routes_pb2.KubernetesRouteBackendReference, _Mapping]]] = ...,
        request_timeout: _Optional[str] = ...,
        backend_request_timeout: _Optional[str] = ...,
    ) -> None: ...

class KubernetesHTTPRouteSpec(_message.Message):
    __slots__ = ("parent_refs", "hostnames", "rules")
    PARENT_REFS_FIELD_NUMBER: _ClassVar[int]
    HOSTNAMES_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    parent_refs: _containers.RepeatedCompositeFieldContainer[_routes_pb2.KubernetesRouteParentReference]
    hostnames: _containers.RepeatedScalarFieldContainer[str]
    rules: _containers.RepeatedCompositeFieldContainer[KubernetesHTTPRouteRule]
    def __init__(
        self,
        parent_refs: _Optional[_Iterable[_Union[_routes_pb2.KubernetesRouteParentReference, _Mapping]]] = ...,
        hostnames: _Optional[_Iterable[str]] = ...,
        rules: _Optional[_Iterable[_Union[KubernetesHTTPRouteRule, _Mapping]]] = ...,
    ) -> None: ...

class KubernetesHTTPRouteStatus(_message.Message):
    __slots__ = ("parents",)
    PARENTS_FIELD_NUMBER: _ClassVar[int]
    parents: _containers.RepeatedCompositeFieldContainer[_routes_pb2.KubernetesRouteParentStatus]
    def __init__(
        self, parents: _Optional[_Iterable[_Union[_routes_pb2.KubernetesRouteParentStatus, _Mapping]]] = ...
    ) -> None: ...

class KubernetesHTTPRoute(_message.Message):
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
    spec: KubernetesHTTPRouteSpec
    status: KubernetesHTTPRouteStatus
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        uid: _Optional[str] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        annotations: _Optional[_Mapping[str, str]] = ...,
        creation_timestamp: _Optional[int] = ...,
        cluster_name: _Optional[str] = ...,
        spec: _Optional[_Union[KubernetesHTTPRouteSpec, _Mapping]] = ...,
        status: _Optional[_Union[KubernetesHTTPRouteStatus, _Mapping]] = ...,
    ) -> None: ...
