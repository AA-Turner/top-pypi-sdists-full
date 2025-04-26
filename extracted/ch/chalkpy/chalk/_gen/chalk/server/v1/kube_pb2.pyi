from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.kubernetes.v1 import events_pb2 as _events_pb2
from chalk._gen.chalk.kubernetes.v1 import persistentvolume_pb2 as _persistentvolume_pb2
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

class GetPodStackTraceDumpRequest(_message.Message):
    __slots__ = ("namespace", "pod_name", "container_name", "process_id", "process_name", "auto_detect_process")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    PROCESS_NAME_FIELD_NUMBER: _ClassVar[int]
    AUTO_DETECT_PROCESS_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    pod_name: str
    container_name: str
    process_id: int
    process_name: str
    auto_detect_process: bool
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        pod_name: _Optional[str] = ...,
        container_name: _Optional[str] = ...,
        process_id: _Optional[int] = ...,
        process_name: _Optional[str] = ...,
        auto_detect_process: bool = ...,
    ) -> None: ...

class GetPodStackTraceDumpResponse(_message.Message):
    __slots__ = ("stack_trace",)
    STACK_TRACE_FIELD_NUMBER: _ClassVar[int]
    stack_trace: str
    def __init__(self, stack_trace: _Optional[str] = ...) -> None: ...

class GetKubernetesEventsRequest(_message.Message):
    __slots__ = ("cluster_name", "namespace", "label_selector", "field_selector")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    LABEL_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    FIELD_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    namespace: str
    label_selector: str
    field_selector: str
    def __init__(
        self,
        cluster_name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        label_selector: _Optional[str] = ...,
        field_selector: _Optional[str] = ...,
    ) -> None: ...

class GetKubernetesEventsResponse(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[_events_pb2.ChalkKubernetesEvent]
    def __init__(
        self, events: _Optional[_Iterable[_Union[_events_pb2.ChalkKubernetesEvent, _Mapping]]] = ...
    ) -> None: ...

class GetKubernetesPersistentVolumesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKubernetesPersistentVolumesResponse(_message.Message):
    __slots__ = ("volumes",)
    VOLUMES_FIELD_NUMBER: _ClassVar[int]
    volumes: _containers.RepeatedCompositeFieldContainer[_persistentvolume_pb2.ChalkKubernetesPersistentVolume]
    def __init__(
        self,
        volumes: _Optional[_Iterable[_Union[_persistentvolume_pb2.ChalkKubernetesPersistentVolume, _Mapping]]] = ...,
    ) -> None: ...
