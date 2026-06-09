from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
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

class GetClusterEnvironmentsRequest(_message.Message):
    __slots__ = ("cluster_name",)
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    def __init__(self, cluster_name: _Optional[str] = ...) -> None: ...

class GetClusterEnvironmentsResponse(_message.Message):
    __slots__ = ("environment_ids",)
    ENVIRONMENT_IDS_FIELD_NUMBER: _ClassVar[int]
    environment_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, environment_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class TelemetryTimescaleKubeSecretRef(_message.Message):
    __slots__ = ("environment_id", "kube_secret_name", "kube_secret_key")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    KUBE_SECRET_NAME_FIELD_NUMBER: _ClassVar[int]
    KUBE_SECRET_KEY_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    kube_secret_name: str
    kube_secret_key: str
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        kube_secret_name: _Optional[str] = ...,
        kube_secret_key: _Optional[str] = ...,
    ) -> None: ...

class ListTelemetryTimescaleKubeSecretRefsRequest(_message.Message):
    __slots__ = ("cluster_name", "telemetry_deployment_id")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    TELEMETRY_DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    telemetry_deployment_id: str
    def __init__(self, cluster_name: _Optional[str] = ..., telemetry_deployment_id: _Optional[str] = ...) -> None: ...

class ListTelemetryTimescaleKubeSecretRefsResponse(_message.Message):
    __slots__ = ("secret_refs",)
    SECRET_REFS_FIELD_NUMBER: _ClassVar[int]
    secret_refs: _containers.RepeatedCompositeFieldContainer[TelemetryTimescaleKubeSecretRef]
    def __init__(
        self, secret_refs: _Optional[_Iterable[_Union[TelemetryTimescaleKubeSecretRef, _Mapping]]] = ...
    ) -> None: ...
