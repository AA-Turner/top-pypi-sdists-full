from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesResourceQuantities(_message.Message):
    __slots__ = ("pods",)
    PODS_FIELD_NUMBER: _ClassVar[int]
    pods: int
    def __init__(self, pods: _Optional[int] = ...) -> None: ...
