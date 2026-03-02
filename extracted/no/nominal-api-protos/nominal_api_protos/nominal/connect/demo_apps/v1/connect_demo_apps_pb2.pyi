from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from nominal.gen.v1 import error_pb2 as _error_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectDemoAppsServiceError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CONNECT_DEMO_APPS_SERVICE_ERROR_UNSPECIFIED: _ClassVar[ConnectDemoAppsServiceError]
    CONNECT_DEMO_APPS_SERVICE_ERROR_UNAVAILABLE_FOR_ENVIRONMENT: _ClassVar[ConnectDemoAppsServiceError]
    CONNECT_DEMO_APPS_SERVICE_ERROR_INVALID_CHECKSUM: _ClassVar[ConnectDemoAppsServiceError]
CONNECT_DEMO_APPS_SERVICE_ERROR_UNSPECIFIED: ConnectDemoAppsServiceError
CONNECT_DEMO_APPS_SERVICE_ERROR_UNAVAILABLE_FOR_ENVIRONMENT: ConnectDemoAppsServiceError
CONNECT_DEMO_APPS_SERVICE_ERROR_INVALID_CHECKSUM: ConnectDemoAppsServiceError

class GetDemoAppDownloadUrlRequest(_message.Message):
    __slots__ = ("sha256_checksum",)
    SHA256_CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    sha256_checksum: str
    def __init__(self, sha256_checksum: _Optional[str] = ...) -> None: ...

class GetDemoAppDownloadUrlResponse(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...
