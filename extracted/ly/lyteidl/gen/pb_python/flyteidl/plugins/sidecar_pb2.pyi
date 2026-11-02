from k8s.io.api.core.v1 import generated_pb2 as _generated_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SidecarJob(_message.Message):
    __slots__ = ["annotations", "labels", "pod_spec", "primary_container_name"]
    class AnnotationsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class LabelsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    POD_SPEC_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    annotations: _containers.ScalarMap[str, str]
    labels: _containers.ScalarMap[str, str]
    pod_spec: _generated_pb2.PodSpec
    primary_container_name: str
    def __init__(self, pod_spec: _Optional[_Union[_generated_pb2.PodSpec, _Mapping]] = ..., primary_container_name: _Optional[str] = ..., annotations: _Optional[_Mapping[str, str]] = ..., labels: _Optional[_Mapping[str, str]] = ...) -> None: ...
