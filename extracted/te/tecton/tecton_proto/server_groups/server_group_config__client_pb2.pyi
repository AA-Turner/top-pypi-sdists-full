from tecton_proto.realtime import instance_group__client_pb2 as _instance_group__client_pb2
from tecton_proto.server_groups import server_group_states__client_pb2 as _server_group_states__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServerGroupClusterConfig(_message.Message):
    __slots__ = ["transform_server_group"]
    TRANSFORM_SERVER_GROUP_FIELD_NUMBER: _ClassVar[int]
    transform_server_group: _containers.RepeatedCompositeFieldContainer[TransformServerGroupInfo]
    def __init__(self, transform_server_group: _Optional[_Iterable[_Union[TransformServerGroupInfo, _Mapping]]] = ...) -> None: ...

class TransformServerGroupInfo(_message.Message):
    __slots__ = ["autoscaling_policy", "aws_instance_group_config", "environment_variables", "server_group_id"]
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    AUTOSCALING_POLICY_FIELD_NUMBER: _ClassVar[int]
    AWS_INSTANCE_GROUP_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    autoscaling_policy: _server_group_states__client_pb2.AutoscalingPolicy
    aws_instance_group_config: _instance_group__client_pb2.AWSInstanceGroupUpdateConfig
    environment_variables: _containers.ScalarMap[str, str]
    server_group_id: str
    def __init__(self, server_group_id: _Optional[str] = ..., autoscaling_policy: _Optional[_Union[_server_group_states__client_pb2.AutoscalingPolicy, _Mapping]] = ..., aws_instance_group_config: _Optional[_Union[_instance_group__client_pb2.AWSInstanceGroupUpdateConfig, _Mapping]] = ..., environment_variables: _Optional[_Mapping[str, str]] = ...) -> None: ...
