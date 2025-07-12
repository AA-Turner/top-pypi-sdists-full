from tecton_proto.args import basic_info__client_pb2 as _basic_info__client_pb2
from tecton_proto.args import diff_options__client_pb2 as _diff_options__client_pb2
from tecton_proto.args import server_group__client_pb2 as _server_group__client_pb2
from tecton_proto.common import framework_version__client_pb2 as _framework_version__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ColumnPair(_message.Message):
    __slots__ = ["feature_column", "spine_column"]
    FEATURE_COLUMN_FIELD_NUMBER: _ClassVar[int]
    SPINE_COLUMN_FIELD_NUMBER: _ClassVar[int]
    feature_column: str
    spine_column: str
    def __init__(self, spine_column: _Optional[str] = ..., feature_column: _Optional[str] = ...) -> None: ...

class FeatureReference(_message.Message):
    __slots__ = ["feature_view_id", "features", "namespace", "override_join_keys"]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    feature_view_id: _id__client_pb2.Id
    features: _containers.RepeatedScalarFieldContainer[str]
    namespace: str
    override_join_keys: _containers.RepeatedCompositeFieldContainer[ColumnPair]
    def __init__(self, feature_view_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., override_join_keys: _Optional[_Iterable[_Union[ColumnPair, _Mapping]]] = ..., namespace: _Optional[str] = ..., features: _Optional[_Iterable[str]] = ...) -> None: ...

class FeatureServiceArgs(_message.Message):
    __slots__ = ["enable_online_caching", "feature_references", "feature_server_group", "feature_service_id", "info", "logging", "online_serving_enabled", "options", "prevent_destroy", "realtime_environment", "transform_server_group", "transform_server_group_name", "version"]
    class OptionsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ENABLE_ONLINE_CACHING_FIELD_NUMBER: _ClassVar[int]
    FEATURE_REFERENCES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVER_GROUP_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    LOGGING_FIELD_NUMBER: _ClassVar[int]
    ONLINE_SERVING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PREVENT_DESTROY_FIELD_NUMBER: _ClassVar[int]
    REALTIME_ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_SERVER_GROUP_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_SERVER_GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    enable_online_caching: bool
    feature_references: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    feature_server_group: _server_group__client_pb2.ServerGroupReference
    feature_service_id: _id__client_pb2.Id
    info: _basic_info__client_pb2.BasicInfo
    logging: LoggingConfigArgs
    online_serving_enabled: bool
    options: _containers.ScalarMap[str, str]
    prevent_destroy: bool
    realtime_environment: str
    transform_server_group: _server_group__client_pb2.ServerGroupReference
    transform_server_group_name: str
    version: _framework_version__client_pb2.FrameworkVersion
    def __init__(self, feature_service_id: _Optional[_Union[_id__client_pb2.Id, _Mapping]] = ..., info: _Optional[_Union[_basic_info__client_pb2.BasicInfo, _Mapping]] = ..., version: _Optional[_Union[_framework_version__client_pb2.FrameworkVersion, str]] = ..., prevent_destroy: bool = ..., options: _Optional[_Mapping[str, str]] = ..., enable_online_caching: bool = ..., feature_references: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ..., online_serving_enabled: bool = ..., logging: _Optional[_Union[LoggingConfigArgs, _Mapping]] = ..., realtime_environment: _Optional[str] = ..., transform_server_group: _Optional[_Union[_server_group__client_pb2.ServerGroupReference, _Mapping]] = ..., feature_server_group: _Optional[_Union[_server_group__client_pb2.ServerGroupReference, _Mapping]] = ..., transform_server_group_name: _Optional[str] = ...) -> None: ...

class LoggingConfigArgs(_message.Message):
    __slots__ = ["log_effective_times", "sample_rate"]
    LOG_EFFECTIVE_TIMES_FIELD_NUMBER: _ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: _ClassVar[int]
    log_effective_times: bool
    sample_rate: float
    def __init__(self, sample_rate: _Optional[float] = ..., log_effective_times: bool = ...) -> None: ...
