from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class KubernetesStorageClass(_message.Message):
    __slots__ = (
        "name",
        "provisioner",
        "reclaim_policy",
        "volume_binding_mode",
        "allow_volume_expansion",
        "parameters",
        "is_default",
        "creation_timestamp",
    )
    class ParametersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    PROVISIONER_FIELD_NUMBER: _ClassVar[int]
    RECLAIM_POLICY_FIELD_NUMBER: _ClassVar[int]
    VOLUME_BINDING_MODE_FIELD_NUMBER: _ClassVar[int]
    ALLOW_VOLUME_EXPANSION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    IS_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    name: str
    provisioner: str
    reclaim_policy: str
    volume_binding_mode: str
    allow_volume_expansion: bool
    parameters: _containers.ScalarMap[str, str]
    is_default: bool
    creation_timestamp: int
    def __init__(
        self,
        name: _Optional[str] = ...,
        provisioner: _Optional[str] = ...,
        reclaim_policy: _Optional[str] = ...,
        volume_binding_mode: _Optional[str] = ...,
        allow_volume_expansion: bool = ...,
        parameters: _Optional[_Mapping[str, str]] = ...,
        is_default: bool = ...,
        creation_timestamp: _Optional[int] = ...,
    ) -> None: ...
