from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetInfoRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetInfoResponse(_message.Message):
    __slots__ = ["implementation", "capabilities"]
    IMPLEMENTATION_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    implementation: ImplementationDetails
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, implementation: _Optional[_Union[ImplementationDetails, _Mapping]] = ..., capabilities: _Optional[_Iterable[str]] = ...) -> None: ...

class ImplementationDetails(_message.Message):
    __slots__ = ["name", "version", "url", "proto_version"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    PROTO_VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    url: str
    proto_version: str
    def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ..., url: _Optional[str] = ..., proto_version: _Optional[str] = ...) -> None: ...
