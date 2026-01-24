from google.api import annotations_pb2 as _annotations_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NominalInstroPackageRegistryError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOMINAL_INSTRO_PACKAGE_REGISTRY_ERROR_UNSPECIFIED: _ClassVar[NominalInstroPackageRegistryError]
    NOMINAL_INSTRO_PACKAGE_REGISTRY_ERROR_NOT_AVAILABLE: _ClassVar[NominalInstroPackageRegistryError]
NOMINAL_INSTRO_PACKAGE_REGISTRY_ERROR_UNSPECIFIED: NominalInstroPackageRegistryError
NOMINAL_INSTRO_PACKAGE_REGISTRY_ERROR_NOT_AVAILABLE: NominalInstroPackageRegistryError

class GetPythonPackageRegistryRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetPythonPackageRegistryResponse(_message.Message):
    __slots__ = ("registry_url", "registry_token")
    REGISTRY_URL_FIELD_NUMBER: _ClassVar[int]
    REGISTRY_TOKEN_FIELD_NUMBER: _ClassVar[int]
    registry_url: str
    registry_token: str
    def __init__(self, registry_url: _Optional[str] = ..., registry_token: _Optional[str] = ...) -> None: ...
