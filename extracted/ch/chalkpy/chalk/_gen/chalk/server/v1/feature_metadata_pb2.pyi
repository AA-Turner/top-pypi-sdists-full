from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DropFeatureVersionsRequest(_message.Message):
    __slots__ = ("namespace", "features")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, namespace: _Optional[str] = ..., features: _Optional[_Iterable[str]] = ...) -> None: ...

class DropFeatureVersionsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FeatureMigrateTypeRequest(_message.Message):
    __slots__ = ("namespace", "features")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, namespace: _Optional[str] = ..., features: _Optional[_Iterable[str]] = ...) -> None: ...

class FeatureMigrateTypeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
