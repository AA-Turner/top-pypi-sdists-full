from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.container.v1 import service_pb2 as _service_pb2
from chalk._gen.chalk.flags.v1 import flags_pb2 as _flags_pb2
from chalk._gen.chalk.models.v1 import model_artifact_pb2 as _model_artifact_pb2
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

class CuratedModel(_message.Message):
    __slots__ = (
        "id",
        "display_name",
        "description",
        "model_family",
        "task",
        "model_image",
        "handler",
        "default_signature",
        "default_scaling",
        "default_resources",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MODEL_FAMILY_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    MODEL_IMAGE_FIELD_NUMBER: _ClassVar[int]
    HANDLER_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_SCALING_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    id: str
    display_name: str
    description: str
    model_family: str
    task: str
    model_image: str
    handler: str
    default_signature: _model_artifact_pb2.ModelSignature
    default_scaling: _service_pb2_1.ScalingSpec
    default_resources: _service_pb2.ResourceLimits
    def __init__(
        self,
        id: _Optional[str] = ...,
        display_name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        model_family: _Optional[str] = ...,
        task: _Optional[str] = ...,
        model_image: _Optional[str] = ...,
        handler: _Optional[str] = ...,
        default_signature: _Optional[_Union[_model_artifact_pb2.ModelSignature, _Mapping]] = ...,
        default_scaling: _Optional[_Union[_service_pb2_1.ScalingSpec, _Mapping]] = ...,
        default_resources: _Optional[_Union[_service_pb2.ResourceLimits, _Mapping]] = ...,
    ) -> None: ...

class ListCuratedModelsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCuratedModelsResponse(_message.Message):
    __slots__ = ("models",)
    MODELS_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[CuratedModel]
    def __init__(self, models: _Optional[_Iterable[_Union[CuratedModel, _Mapping]]] = ...) -> None: ...

class DeployCuratedModelRequest(_message.Message):
    __slots__ = (
        "curated_model_id",
        "scaling_group_name",
        "gpu",
        "min_replicas",
        "max_replicas",
        "target_cpu_utilization_percentage",
    )
    CURATED_MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    SCALING_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    MIN_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    MAX_REPLICAS_FIELD_NUMBER: _ClassVar[int]
    TARGET_CPU_UTILIZATION_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    curated_model_id: str
    scaling_group_name: str
    gpu: str
    min_replicas: int
    max_replicas: int
    target_cpu_utilization_percentage: int
    def __init__(
        self,
        curated_model_id: _Optional[str] = ...,
        scaling_group_name: _Optional[str] = ...,
        gpu: _Optional[str] = ...,
        min_replicas: _Optional[int] = ...,
        max_replicas: _Optional[int] = ...,
        target_cpu_utilization_percentage: _Optional[int] = ...,
    ) -> None: ...

class DeployCuratedModelResponse(_message.Message):
    __slots__ = ("model_artifact", "model_version", "scaling_group")
    MODEL_ARTIFACT_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    SCALING_GROUP_FIELD_NUMBER: _ClassVar[int]
    model_artifact: _model_artifact_pb2.ModelArtifactSpec
    model_version: int
    scaling_group: _service_pb2_1.ScalingGroupResponse
    def __init__(
        self,
        model_artifact: _Optional[_Union[_model_artifact_pb2.ModelArtifactSpec, _Mapping]] = ...,
        model_version: _Optional[int] = ...,
        scaling_group: _Optional[_Union[_service_pb2_1.ScalingGroupResponse, _Mapping]] = ...,
    ) -> None: ...
