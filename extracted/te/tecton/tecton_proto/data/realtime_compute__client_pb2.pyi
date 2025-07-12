from tecton_proto.realtime import instance_group__client_pb2 as _instance_group__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ColocatedComputeConfig(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class InstanceGroupComputeConfig(_message.Message):
    __slots__ = ["group_name", "instance_group", "use_cached_transformations"]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_GROUP_FIELD_NUMBER: _ClassVar[int]
    USE_CACHED_TRANSFORMATIONS_FIELD_NUMBER: _ClassVar[int]
    group_name: str
    instance_group: _instance_group__client_pb2.InstanceGroupHandle
    use_cached_transformations: bool
    def __init__(self, group_name: _Optional[str] = ..., instance_group: _Optional[_Union[_instance_group__client_pb2.InstanceGroupHandle, _Mapping]] = ..., use_cached_transformations: bool = ...) -> None: ...

class OnlineComputeConfig(_message.Message):
    __slots__ = ["colocated_compute", "instance_group_config", "remote_compute"]
    COLOCATED_COMPUTE_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_GROUP_CONFIG_FIELD_NUMBER: _ClassVar[int]
    REMOTE_COMPUTE_FIELD_NUMBER: _ClassVar[int]
    colocated_compute: ColocatedComputeConfig
    instance_group_config: InstanceGroupComputeConfig
    remote_compute: RemoteFunctionComputeConfig
    def __init__(self, colocated_compute: _Optional[_Union[ColocatedComputeConfig, _Mapping]] = ..., remote_compute: _Optional[_Union[RemoteFunctionComputeConfig, _Mapping]] = ..., instance_group_config: _Optional[_Union[InstanceGroupComputeConfig, _Mapping]] = ...) -> None: ...

class RemoteFunctionComputeConfig(_message.Message):
    __slots__ = ["function_uri", "id", "name"]
    FUNCTION_URI_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    function_uri: str
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., function_uri: _Optional[str] = ...) -> None: ...
