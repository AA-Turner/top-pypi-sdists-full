from tecton_proto.args import entity__client_pb2 as _entity__client_pb2
from tecton_proto.args import feature_service__client_pb2 as _feature_service__client_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from tecton_proto.args import resource_provider__client_pb2 as _resource_provider__client_pb2
from tecton_proto.args import server_group__client_pb2 as _server_group__client_pb2
from tecton_proto.args import transformation__client_pb2 as _transformation__client_pb2
from tecton_proto.args import virtual_data_source__client_pb2 as _virtual_data_source__client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FcoArgs(_message.Message):
    __slots__ = ["entity", "feature_service", "feature_view", "resource_provider", "server_group", "transformation", "virtual_data_source"]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    SERVER_GROUP_FIELD_NUMBER: _ClassVar[int]
    TRANSFORMATION_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    entity: _entity__client_pb2.EntityArgs
    feature_service: _feature_service__client_pb2.FeatureServiceArgs
    feature_view: _feature_view__client_pb2.FeatureViewArgs
    resource_provider: _resource_provider__client_pb2.ResourceProviderArgs
    server_group: _server_group__client_pb2.ServerGroupArgs
    transformation: _transformation__client_pb2.TransformationArgs
    virtual_data_source: _virtual_data_source__client_pb2.VirtualDataSourceArgs
    def __init__(self, virtual_data_source: _Optional[_Union[_virtual_data_source__client_pb2.VirtualDataSourceArgs, _Mapping]] = ..., entity: _Optional[_Union[_entity__client_pb2.EntityArgs, _Mapping]] = ..., feature_view: _Optional[_Union[_feature_view__client_pb2.FeatureViewArgs, _Mapping]] = ..., feature_service: _Optional[_Union[_feature_service__client_pb2.FeatureServiceArgs, _Mapping]] = ..., transformation: _Optional[_Union[_transformation__client_pb2.TransformationArgs, _Mapping]] = ..., server_group: _Optional[_Union[_server_group__client_pb2.ServerGroupArgs, _Mapping]] = ..., resource_provider: _Optional[_Union[_resource_provider__client_pb2.ResourceProviderArgs, _Mapping]] = ...) -> None: ...
