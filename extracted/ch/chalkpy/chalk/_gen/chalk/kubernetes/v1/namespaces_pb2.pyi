from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesNamespace(_message.Message):
    __slots__ = ("namespace", "cluster_name")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    cluster_name: str
    def __init__(self, namespace: _Optional[str] = ..., cluster_name: _Optional[str] = ...) -> None: ...
