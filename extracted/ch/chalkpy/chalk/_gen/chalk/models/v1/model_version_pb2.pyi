from chalk._gen.chalk.models.v1 import model_artifact_pb2 as _model_artifact_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
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

class ModelVersionIdentifier(_message.Message):
    __slots__ = ("version", "alias", "as_of")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    AS_OF_FIELD_NUMBER: _ClassVar[int]
    version: int
    alias: str
    as_of: _timestamp_pb2.Timestamp
    def __init__(
        self,
        version: _Optional[int] = ...,
        alias: _Optional[str] = ...,
        as_of: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class MountedVersionSpecs(_message.Message):
    __slots__ = ("model_name", "version", "identifiers", "model_artifact_filename", "spec")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIERS_FIELD_NUMBER: _ClassVar[int]
    MODEL_ARTIFACT_FILENAME_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    version: int
    identifiers: _containers.RepeatedCompositeFieldContainer[ModelVersionIdentifier]
    model_artifact_filename: str
    spec: _model_artifact_pb2.ModelArtifactSpec
    def __init__(
        self,
        model_name: _Optional[str] = ...,
        version: _Optional[int] = ...,
        identifiers: _Optional[_Iterable[_Union[ModelVersionIdentifier, _Mapping]]] = ...,
        model_artifact_filename: _Optional[str] = ...,
        spec: _Optional[_Union[_model_artifact_pb2.ModelArtifactSpec, _Mapping]] = ...,
    ) -> None: ...

class MountedModelsSpecs(_message.Message):
    __slots__ = ("specs",)
    SPECS_FIELD_NUMBER: _ClassVar[int]
    specs: _containers.RepeatedCompositeFieldContainer[MountedVersionSpecs]
    def __init__(self, specs: _Optional[_Iterable[_Union[MountedVersionSpecs, _Mapping]]] = ...) -> None: ...
