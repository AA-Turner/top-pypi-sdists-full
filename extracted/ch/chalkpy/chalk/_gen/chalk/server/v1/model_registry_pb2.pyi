from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.flags.v1 import flags_pb2 as _flags_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from chalk._gen.chalk.models.v1 import model_artifact_pb2 as _model_artifact_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import struct_pb2 as _struct_pb2
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

class ModelArtifact(_message.Message):
    __slots__ = ("id", "path", "spec", "created_by", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    path: str
    spec: _model_artifact_pb2.ModelArtifactSpec
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        path: _Optional[str] = ...,
        spec: _Optional[_Union[_model_artifact_pb2.ModelArtifactSpec, _Mapping]] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ModelVersion(_message.Message):
    __slots__ = ("id", "model_name", "version", "model_artifact", "aliases", "metadata", "created_by", "created_at")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MODEL_ARTIFACT_FIELD_NUMBER: _ClassVar[int]
    ALIASES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    model_name: str
    version: int
    model_artifact: ModelArtifact
    aliases: _containers.RepeatedScalarFieldContainer[str]
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        model_name: _Optional[str] = ...,
        version: _Optional[int] = ...,
        model_artifact: _Optional[_Union[ModelArtifact, _Mapping]] = ...,
        aliases: _Optional[_Iterable[str]] = ...,
        metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class Model(_message.Message):
    __slots__ = (
        "id",
        "model_name",
        "description",
        "metadata",
        "created_by",
        "created_at",
        "updated_at",
        "archived_at",
        "latest_model_version",
    )
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    LATEST_MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    id: str
    model_name: str
    description: str
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    created_by: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    archived_at: _timestamp_pb2.Timestamp
    latest_model_version: ModelVersion
    def __init__(
        self,
        id: _Optional[str] = ...,
        model_name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        created_by: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        archived_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        latest_model_version: _Optional[_Union[ModelVersion, _Mapping]] = ...,
    ) -> None: ...

class ListModelsRequest(_message.Message):
    __slots__ = ("cursor", "limit")
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    cursor: str
    limit: int
    def __init__(self, cursor: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class ListModelsResponse(_message.Message):
    __slots__ = ("models", "next_cursor")
    MODELS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[Model]
    next_cursor: str
    def __init__(
        self, models: _Optional[_Iterable[_Union[Model, _Mapping]]] = ..., next_cursor: _Optional[str] = ...
    ) -> None: ...

class GetModelRequest(_message.Message):
    __slots__ = ("model_id", "model_name")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    model_name: str
    def __init__(self, model_id: _Optional[str] = ..., model_name: _Optional[str] = ...) -> None: ...

class GetModelResponse(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: Model
    def __init__(self, model: _Optional[_Union[Model, _Mapping]] = ...) -> None: ...

class CreateModelRequest(_message.Message):
    __slots__ = ("model_name", "description", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    description: str
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        model_name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class CreateModelResponse(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: Model
    def __init__(self, model: _Optional[_Union[Model, _Mapping]] = ...) -> None: ...

class UpdateModelOperation(_message.Message):
    __slots__ = ("model_name", "description", "metadata", "archived_at")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ARCHIVED_AT_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    description: str
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    archived_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        model_name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
        archived_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class UpdateModelRequest(_message.Message):
    __slots__ = ("model_id", "update", "update_mask")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    update: UpdateModelOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        model_id: _Optional[str] = ...,
        update: _Optional[_Union[UpdateModelOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateModelResponse(_message.Message):
    __slots__ = ("model",)
    MODEL_FIELD_NUMBER: _ClassVar[int]
    model: Model
    def __init__(self, model: _Optional[_Union[Model, _Mapping]] = ...) -> None: ...

class ListModelVersionsRequest(_message.Message):
    __slots__ = ("model_name", "cursor", "limit")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    CURSOR_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    cursor: str
    limit: int
    def __init__(
        self, model_name: _Optional[str] = ..., cursor: _Optional[str] = ..., limit: _Optional[int] = ...
    ) -> None: ...

class ListModelVersionsResponse(_message.Message):
    __slots__ = ("model_versions", "next_cursor")
    MODEL_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    model_versions: _containers.RepeatedCompositeFieldContainer[ModelVersion]
    next_cursor: str
    def __init__(
        self,
        model_versions: _Optional[_Iterable[_Union[ModelVersion, _Mapping]]] = ...,
        next_cursor: _Optional[str] = ...,
    ) -> None: ...

class GetModelVersionRequest(_message.Message):
    __slots__ = ("model_name", "version")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    version: int
    def __init__(self, model_name: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class GetModelVersionResponse(_message.Message):
    __slots__ = ("model_version",)
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    model_version: ModelVersion
    def __init__(self, model_version: _Optional[_Union[ModelVersion, _Mapping]] = ...) -> None: ...

class CreateModelVersionRequest(_message.Message):
    __slots__ = ("model_name", "model_artifact_id", "model_artifact", "aliases", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_ARTIFACT_FIELD_NUMBER: _ClassVar[int]
    ALIASES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    model_artifact_id: str
    model_artifact: _model_artifact_pb2.ModelArtifactSpec
    aliases: _containers.RepeatedScalarFieldContainer[str]
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self,
        model_name: _Optional[str] = ...,
        model_artifact_id: _Optional[str] = ...,
        model_artifact: _Optional[_Union[_model_artifact_pb2.ModelArtifactSpec, _Mapping]] = ...,
        aliases: _Optional[_Iterable[str]] = ...,
        metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...,
    ) -> None: ...

class CreateModelVersionResponse(_message.Message):
    __slots__ = ("model_version",)
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    model_version: ModelVersion
    def __init__(self, model_version: _Optional[_Union[ModelVersion, _Mapping]] = ...) -> None: ...

class ModelVersionKey(_message.Message):
    __slots__ = ("model_name", "version")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    version: int
    def __init__(self, model_name: _Optional[str] = ..., version: _Optional[int] = ...) -> None: ...

class UpdateModelVersionOperation(_message.Message):
    __slots__ = ("aliases", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...
        ) -> None: ...

    ALIASES_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    aliases: _containers.RepeatedScalarFieldContainer[str]
    metadata: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(
        self, aliases: _Optional[_Iterable[str]] = ..., metadata: _Optional[_Mapping[str, _struct_pb2.Value]] = ...
    ) -> None: ...

class UpdateModelVersionRequest(_message.Message):
    __slots__ = ("model_version_key", "update", "update_mask")
    MODEL_VERSION_KEY_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    model_version_key: ModelVersionKey
    update: UpdateModelVersionOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        model_version_key: _Optional[_Union[ModelVersionKey, _Mapping]] = ...,
        update: _Optional[_Union[UpdateModelVersionOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateModelVersionResponse(_message.Message):
    __slots__ = ("model_version",)
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    model_version: ModelVersion
    def __init__(self, model_version: _Optional[_Union[ModelVersion, _Mapping]] = ...) -> None: ...

class GetModelArtifactUploadUrlsRequest(_message.Message):
    __slots__ = ("file_names",)
    FILE_NAMES_FIELD_NUMBER: _ClassVar[int]
    file_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, file_names: _Optional[_Iterable[str]] = ...) -> None: ...

class GetModelArtifactUploadUrlsResponse(_message.Message):
    __slots__ = ("upload_urls", "model_artifact_id")
    class UploadUrlsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    UPLOAD_URLS_FIELD_NUMBER: _ClassVar[int]
    MODEL_ARTIFACT_ID_FIELD_NUMBER: _ClassVar[int]
    upload_urls: _containers.ScalarMap[str, str]
    model_artifact_id: str
    def __init__(
        self, upload_urls: _Optional[_Mapping[str, str]] = ..., model_artifact_id: _Optional[str] = ...
    ) -> None: ...

class DownloadModelArtifactRequest(_message.Message):
    __slots__ = ("model_version_key",)
    MODEL_VERSION_KEY_FIELD_NUMBER: _ClassVar[int]
    model_version_key: ModelVersionKey
    def __init__(self, model_version_key: _Optional[_Union[ModelVersionKey, _Mapping]] = ...) -> None: ...

class DownloadModelArtifactResponse(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class GetModelReferencesRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class ModelRelation(_message.Message):
    __slots__ = ("input_features", "output_feature")
    INPUT_FEATURES_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FEATURE_FIELD_NUMBER: _ClassVar[int]
    input_features: _containers.RepeatedScalarFieldContainer[str]
    output_feature: str
    def __init__(
        self, input_features: _Optional[_Iterable[str]] = ..., output_feature: _Optional[str] = ...
    ) -> None: ...

class ModelReference(_message.Message):
    __slots__ = (
        "id",
        "model_name",
        "version",
        "deployment_id",
        "relations",
        "resolvers",
        "source_file_reference",
        "created_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RELATIONS_FIELD_NUMBER: _ClassVar[int]
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FILE_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    model_name: str
    version: int
    deployment_id: str
    relations: _containers.RepeatedCompositeFieldContainer[ModelRelation]
    resolvers: _containers.RepeatedScalarFieldContainer[str]
    source_file_reference: _graph_pb2.SourceFileReference
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        model_name: _Optional[str] = ...,
        version: _Optional[int] = ...,
        deployment_id: _Optional[str] = ...,
        relations: _Optional[_Iterable[_Union[ModelRelation, _Mapping]]] = ...,
        resolvers: _Optional[_Iterable[str]] = ...,
        source_file_reference: _Optional[_Union[_graph_pb2.SourceFileReference, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetModelReferencesResponse(_message.Message):
    __slots__ = ("model_references",)
    MODEL_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    model_references: _containers.RepeatedCompositeFieldContainer[ModelReference]
    def __init__(self, model_references: _Optional[_Iterable[_Union[ModelReference, _Mapping]]] = ...) -> None: ...

class GetModelReferenceRequest(_message.Message):
    __slots__ = ("model_id", "model_name", "model_version", "deployment_id")
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_VERSION_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    model_id: str
    model_name: str
    model_version: int
    deployment_id: str
    def __init__(
        self,
        model_id: _Optional[str] = ...,
        model_name: _Optional[str] = ...,
        model_version: _Optional[int] = ...,
        deployment_id: _Optional[str] = ...,
    ) -> None: ...

class GetModelReferenceResponse(_message.Message):
    __slots__ = ("model_reference",)
    MODEL_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    model_reference: ModelReference
    def __init__(self, model_reference: _Optional[_Union[ModelReference, _Mapping]] = ...) -> None: ...
