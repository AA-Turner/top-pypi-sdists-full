from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesServiceAccount(_message.Message):
    __slots__ = ("name", "namespace", "uid", "creation_timestamp", "labels", "annotations", "image_pull_secrets")
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
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    IMAGE_PULL_SECRETS_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    uid: str
    creation_timestamp: int
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    image_pull_secrets: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        uid: _Optional[str] = ...,
        creation_timestamp: _Optional[int] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        annotations: _Optional[_Mapping[str, str]] = ...,
        image_pull_secrets: _Optional[_Iterable[str]] = ...,
    ) -> None: ...
