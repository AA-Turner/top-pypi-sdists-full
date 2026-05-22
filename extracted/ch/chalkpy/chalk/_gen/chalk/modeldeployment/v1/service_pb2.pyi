from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.container.v1 import service_pb2 as _service_pb2
from chalk._gen.chalk.models.v1 import model_version_pb2 as _model_version_pb2
from chalk._gen.chalk.runtime.v1 import remote_python_call_pb2 as _remote_python_call_pb2
from chalk._gen.chalk.scalinggroup.v1 import service_pb2 as _service_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class ModelContainerSpec(_message.Message):
    __slots__ = ("tags", "resources", "env_vars", "volumes", "routing", "authentication")
    class TagsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class EnvVarsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TAGS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    ENV_VARS_FIELD_NUMBER: _ClassVar[int]
    VOLUMES_FIELD_NUMBER: _ClassVar[int]
    ROUTING_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_FIELD_NUMBER: _ClassVar[int]
    tags: _containers.ScalarMap[str, str]
    resources: _service_pb2.ResourceLimits
    env_vars: _containers.ScalarMap[str, str]
    volumes: _containers.RepeatedCompositeFieldContainer[_service_pb2.VolumeMount]
    routing: str
    authentication: str
    def __init__(
        self,
        tags: _Optional[_Mapping[str, str]] = ...,
        resources: _Optional[_Union[_service_pb2.ResourceLimits, _Mapping]] = ...,
        env_vars: _Optional[_Mapping[str, str]] = ...,
        volumes: _Optional[_Iterable[_Union[_service_pb2.VolumeMount, _Mapping]]] = ...,
        routing: _Optional[str] = ...,
        authentication: _Optional[str] = ...,
    ) -> None: ...

class CreateModelScalingGroupRequest(_message.Message):
    __slots__ = ("name", "model_name", "identifier", "container_spec", "scaling_spec", "handler")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_SPEC_FIELD_NUMBER: _ClassVar[int]
    SCALING_SPEC_FIELD_NUMBER: _ClassVar[int]
    HANDLER_FIELD_NUMBER: _ClassVar[int]
    name: str
    model_name: str
    identifier: _model_version_pb2.ModelVersionIdentifier
    container_spec: ModelContainerSpec
    scaling_spec: _service_pb2_1.ScalingSpec
    handler: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        model_name: _Optional[str] = ...,
        identifier: _Optional[_Union[_model_version_pb2.ModelVersionIdentifier, _Mapping]] = ...,
        container_spec: _Optional[_Union[ModelContainerSpec, _Mapping]] = ...,
        scaling_spec: _Optional[_Union[_service_pb2_1.ScalingSpec, _Mapping]] = ...,
        handler: _Optional[str] = ...,
    ) -> None: ...

class CreateModelScalingGroupResponse(_message.Message):
    __slots__ = ("scaling_group",)
    SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    scaling_group: _service_pb2_1.ScalingGroupResponse
    def __init__(
        self, scaling_group: _Optional[_Union[_service_pb2_1.ScalingGroupResponse, _Mapping]] = ...
    ) -> None: ...

class ModelVersionSelector(_message.Message):
    __slots__ = ("model_name", "identifier")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    identifier: _model_version_pb2.ModelVersionIdentifier
    def __init__(
        self,
        model_name: _Optional[str] = ...,
        identifier: _Optional[_Union[_model_version_pb2.ModelVersionIdentifier, _Mapping]] = ...,
    ) -> None: ...

class ListModelScalingGroupsRequest(_message.Message):
    __slots__ = ("model_version",)
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    model_version: ModelVersionSelector
    def __init__(self, model_version: _Optional[_Union[ModelVersionSelector, _Mapping]] = ...) -> None: ...

class ListModelScalingGroupsResponse(_message.Message):
    __slots__ = ("scaling_groups",)
    SCALING_GROUPS_FIELD_NUMBER: _ClassVar[int]
    scaling_groups: _containers.RepeatedCompositeFieldContainer[_service_pb2_1.ScalingGroupResponse]
    def __init__(
        self, scaling_groups: _Optional[_Iterable[_Union[_service_pb2_1.ScalingGroupResponse, _Mapping]]] = ...
    ) -> None: ...

class CallModelRequest(_message.Message):
    __slots__ = ("model_version", "remote_call_request")
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    REMOTE_CALL_REQUEST_FIELD_NUMBER: _ClassVar[int]
    model_version: ModelVersionSelector
    remote_call_request: _remote_python_call_pb2.CallFunctionRequest
    def __init__(
        self,
        model_version: _Optional[_Union[ModelVersionSelector, _Mapping]] = ...,
        remote_call_request: _Optional[_Union[_remote_python_call_pb2.CallFunctionRequest, _Mapping]] = ...,
    ) -> None: ...

class CallModelResponse(_message.Message):
    __slots__ = ("remote_call_response",)
    REMOTE_CALL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    remote_call_response: _remote_python_call_pb2.CallFunctionResponse
    def __init__(
        self, remote_call_response: _Optional[_Union[_remote_python_call_pb2.CallFunctionResponse, _Mapping]] = ...
    ) -> None: ...
