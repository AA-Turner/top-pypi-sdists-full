from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

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
