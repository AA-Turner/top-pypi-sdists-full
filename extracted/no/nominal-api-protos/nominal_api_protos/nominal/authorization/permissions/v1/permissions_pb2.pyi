from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckPermissionRequest(_message.Message):
    __slots__ = ("action", "resource")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    action: str
    resource: str
    def __init__(self, action: _Optional[str] = ..., resource: _Optional[str] = ...) -> None: ...

class CheckPermissionsRequest(_message.Message):
    __slots__ = ("requests",)
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[CheckPermissionRequest]
    def __init__(self, requests: _Optional[_Iterable[_Union[CheckPermissionRequest, _Mapping]]] = ...) -> None: ...

class CheckPermissionResponse(_message.Message):
    __slots__ = ("is_authorized", "requested_permission")
    IS_AUTHORIZED_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_PERMISSION_FIELD_NUMBER: _ClassVar[int]
    is_authorized: bool
    requested_permission: CheckPermissionRequest
    def __init__(self, is_authorized: bool = ..., requested_permission: _Optional[_Union[CheckPermissionRequest, _Mapping]] = ...) -> None: ...

class CheckPermissionsResponse(_message.Message):
    __slots__ = ("responses",)
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    responses: _containers.RepeatedCompositeFieldContainer[CheckPermissionResponse]
    def __init__(self, responses: _Optional[_Iterable[_Union[CheckPermissionResponse, _Mapping]]] = ...) -> None: ...
