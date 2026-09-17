from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceRequirements(_message.Message):
    __slots__ = ("requests", "limits")
    class RequestsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class LimitsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.ScalarMap[str, str]
    limits: _containers.ScalarMap[str, str]
    def __init__(
        self, requests: _Optional[_Mapping[str, str]] = ..., limits: _Optional[_Mapping[str, str]] = ...
    ) -> None: ...

class ResourceRequests(_message.Message):
    __slots__ = ("cpu", "memory", "ephemeral_volume_size", "ephemeral_storage", "resource_group")
    CPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_FIELD_NUMBER: _ClassVar[int]
    EPHEMERAL_VOLUME_SIZE_FIELD_NUMBER: _ClassVar[int]
    EPHEMERAL_STORAGE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    cpu: str
    memory: str
    ephemeral_volume_size: str
    ephemeral_storage: str
    resource_group: str
    def __init__(
        self,
        cpu: _Optional[str] = ...,
        memory: _Optional[str] = ...,
        ephemeral_volume_size: _Optional[str] = ...,
        ephemeral_storage: _Optional[str] = ...,
        resource_group: _Optional[str] = ...,
    ) -> None: ...
