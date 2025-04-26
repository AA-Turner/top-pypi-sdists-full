from tecton_proto.args import entity__client_pb2 as _entity__client_pb2
from tecton_proto.args import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.args import resource_provider__client_pb2 as _resource_provider__client_pb2
from tecton_proto.args import server_group__client_pb2 as _server_group__client_pb2
from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from tecton_proto.common import schema__client_pb2 as _schema__client_pb2
from tecton_proto.common import spark_schema__client_pb2 as _spark_schema__client_pb2
from tecton_proto.modelartifactservice import model_artifact_data__client_pb2 as _model_artifact_data__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntityValidationArgs(_message.Message):
    __slots__ = ["args"]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    args: _entity__client_pb2.EntityArgs
    def __init__(self, args: _Optional[_Union[_entity__client_pb2.EntityArgs, _Mapping]] = ...) -> None: ...

class FcoValidationArgs(_message.Message):
    __slots__ = ["entity", "feature_service", "feature_view", "resource_provider", "server_group", "transformation", "virtual_data_source"]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    entity: EntityValidationArgs
    feature_service: FeatureServiceValidationArgs
    feature_view: FeatureViewValidationArgs
    resource_provider: ResourceProviderArgs
    server_group: ServerGroupValidationArgs
    transformation: TransformationValidationArgs
    virtual_data_source: VirtualDataSourceValidationArgs
    def __init__(self, virtual_data_source: _Optional[_Union[VirtualDataSourceValidationArgs, _Mapping]] = ..., entity: _Optional[_Union[EntityValidationArgs, _Mapping]] = ..., feature_view: _Optional[_Union[FeatureViewValidationArgs, _Mapping]] = ..., feature_service: _Optional[_Union[FeatureServiceValidationArgs, _Mapping]] = ..., transformation: _Optional[_Union[TransformationValidationArgs, _Mapping]] = ..., server_group: _Optional[_Union[ServerGroupValidationArgs, _Mapping]] = ..., resource_provider: _Optional[_Union[ResourceProviderArgs, _Mapping]] = ...) -> None: ...

class FeatureServiceValidationArgs(_message.Message):
    __slots__ = ["args"]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    args: _feature_service__client_pb2.FeatureServiceArgs
    def __init__(self, args: _Optional[_Union[_feature_service__client_pb2.FeatureServiceArgs, _Mapping]] = ...) -> None: ...

class FeatureViewValidationArgs(_message.Message):
    __slots__ = ["args", "local_model_artifacts", "materialization_schema", "view_schema"]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_MODEL_ARTIFACTS_FIELD_NUMBER: _ClassVar[int]
    MATERIALIZATION_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    VIEW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    args: _feature_view__client_pb2.FeatureViewArgs
    local_model_artifacts: _containers.RepeatedCompositeFieldContainer[_model_artifact_data__client_pb2.ModelArtifactInfo]
    materialization_schema: _schema__client_pb2.Schema
    view_schema: _schema__client_pb2.Schema
    def __init__(self, args: _Optional[_Union[_feature_view__client_pb2.FeatureViewArgs, _Mapping]] = ..., view_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., materialization_schema: _Optional[_Union[_schema__client_pb2.Schema, _Mapping]] = ..., local_model_artifacts: _Optional[_Iterable[_Union[_model_artifact_data__client_pb2.ModelArtifactInfo, _Mapping]]] = ...) -> None: ...

class ResourceProviderArgs(_message.Message):
    __slots__ = ["args"]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    args: _resource_provider__client_pb2.ResourceProviderArgs
    def __init__(self, args: _Optional[_Union[_resource_provider__client_pb2.ResourceProviderArgs, _Mapping]] = ...) -> None: ...

class ServerGroupValidationArgs(_message.Message):
    __slots__ = ["args"]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    args: _server_group__client_pb2.ServerGroupArgs
    def __init__(self, args: _Optional[_Union[_server_group__client_pb2.ServerGroupArgs, _Mapping]] = ...) -> None: ...

class TransformationValidationArgs(_message.Message):
    __slots__ = ["args"]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    args: _transformation__client_pb2.TransformationArgs
    def __init__(self, args: _Optional[_Union[_transformation__client_pb2.TransformationArgs, _Mapping]] = ...) -> None: ...

class ValidationRequest(_message.Message):
    __slots__ = ["validation_args"]
    VALIDATION_ARGS_FIELD_NUMBER: _ClassVar[int]
    validation_args: _containers.RepeatedCompositeFieldContainer[FcoValidationArgs]
    def __init__(self, validation_args: _Optional[_Iterable[_Union[FcoValidationArgs, _Mapping]]] = ...) -> None: ...

class VirtualDataSourceValidationArgs(_message.Message):
    __slots__ = ["args", "batch_schema", "stream_schema"]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    BATCH_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    STREAM_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    args: _virtual_data_source__client_pb2.VirtualDataSourceArgs
    batch_schema: _spark_schema__client_pb2.SparkSchema
    stream_schema: _spark_schema__client_pb2.SparkSchema
    def __init__(self, args: _Optional[_Union[_virtual_data_source__client_pb2.VirtualDataSourceArgs, _Mapping]] = ..., batch_schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ..., stream_schema: _Optional[_Union[_spark_schema__client_pb2.SparkSchema, _Mapping]] = ...) -> None: ...
