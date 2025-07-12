from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.api.featureservice import feature_service_request__client_pb2 as _feature_service_request__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CACHED_MISSING_DATA: Status
CACHED_PRESENT: Status
CACHED_UNKNOWN: Status
DEFAULT: FeatureServiceType
DESCRIPTOR: _descriptor.FileDescriptor
DYNAMODB_RESPONSE_SIZE_LIMIT_EXCEEDED: SloIneligibilityReason
MISSING_DATA: Status
PRESENT: Status
REDIS_LATENCY_LIMIT_EXCEEDED: SloIneligibilityReason
REDIS_RESPONSE_SIZE_LIMIT_EXCEEDED: SloIneligibilityReason
TIME_OUT: Status
UNKNOWN: SloIneligibilityReason
UNKNOWN_STATUS: Status
WILDCARD: FeatureServiceType
array: FeatureServerDataType
boolean: FeatureServerDataType
float32: FeatureServerDataType
float64: FeatureServerDataType
int64: FeatureServerDataType
map: FeatureServerDataType
missing_type: FeatureServerDataType
string: FeatureServerDataType
string_array: FeatureServerDataType
struct: FeatureServerDataType
timestamp: FeatureServerDataType

class BatchMetadata(_message.Message):
    __slots__ = ["batch_slo_info", "features", "join_keys", "slo_info"]
    class Item(_message.Message):
        __slots__ = ["data_type", "description", "effective_time", "name", "status", "tags"]
        class TagsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        EFFECTIVE_TIME_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        data_type: FeatureServerComplexDataType
        description: str
        effective_time: _timestamp_pb2.Timestamp
        name: str
        status: _containers.RepeatedScalarFieldContainer[Status]
        tags: _containers.ScalarMap[str, str]
        def __init__(self, name: _Optional[str] = ..., effective_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data_type: _Optional[_Union[FeatureServerComplexDataType, _Mapping]] = ..., status: _Optional[_Iterable[_Union[Status, str]]] = ..., description: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...
    BATCH_SLO_INFO_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    SLO_INFO_FIELD_NUMBER: _ClassVar[int]
    batch_slo_info: BatchSloInfo
    features: _containers.RepeatedCompositeFieldContainer[BatchMetadata.Item]
    join_keys: _containers.RepeatedCompositeFieldContainer[BatchMetadata.Item]
    slo_info: _containers.RepeatedCompositeFieldContainer[SloInfo]
    def __init__(self, features: _Optional[_Iterable[_Union[BatchMetadata.Item, _Mapping]]] = ..., join_keys: _Optional[_Iterable[_Union[BatchMetadata.Item, _Mapping]]] = ..., slo_info: _Optional[_Iterable[_Union[SloInfo, _Mapping]]] = ..., batch_slo_info: _Optional[_Union[BatchSloInfo, _Mapping]] = ...) -> None: ...

class BatchSloInfo(_message.Message):
    __slots__ = ["server_time_seconds", "slo_eligible", "slo_ineligibility_reasons", "slo_server_time_seconds", "store_max_latency"]
    SERVER_TIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    SLO_ELIGIBLE_FIELD_NUMBER: _ClassVar[int]
    SLO_INELIGIBILITY_REASONS_FIELD_NUMBER: _ClassVar[int]
    SLO_SERVER_TIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    STORE_MAX_LATENCY_FIELD_NUMBER: _ClassVar[int]
    server_time_seconds: float
    slo_eligible: bool
    slo_ineligibility_reasons: _containers.RepeatedScalarFieldContainer[SloIneligibilityReason]
    slo_server_time_seconds: float
    store_max_latency: float
    def __init__(self, slo_eligible: bool = ..., slo_server_time_seconds: _Optional[float] = ..., slo_ineligibility_reasons: _Optional[_Iterable[_Union[SloIneligibilityReason, str]]] = ..., server_time_seconds: _Optional[float] = ..., store_max_latency: _Optional[float] = ...) -> None: ...

class FeatureServerComplexDataType(_message.Message):
    __slots__ = ["element_type", "fields", "key_type", "type", "value_type"]
    ELEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    element_type: FeatureServerComplexDataType
    fields: _containers.RepeatedCompositeFieldContainer[FeatureServerStructField]
    key_type: FeatureServerComplexDataType
    type: FeatureServerDataType
    value_type: FeatureServerComplexDataType
    def __init__(self, type: _Optional[_Union[FeatureServerDataType, str]] = ..., element_type: _Optional[_Union[FeatureServerComplexDataType, _Mapping]] = ..., fields: _Optional[_Iterable[_Union[FeatureServerStructField, _Mapping]]] = ..., key_type: _Optional[_Union[FeatureServerComplexDataType, _Mapping]] = ..., value_type: _Optional[_Union[FeatureServerComplexDataType, _Mapping]] = ...) -> None: ...

class FeatureServerStructField(_message.Message):
    __slots__ = ["data_type", "name"]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    data_type: FeatureServerComplexDataType
    name: str
    def __init__(self, name: _Optional[str] = ..., data_type: _Optional[_Union[FeatureServerComplexDataType, _Mapping]] = ...) -> None: ...

class FeatureServiceLocator(_message.Message):
    __slots__ = ["feature_package_id", "feature_package_name", "feature_service_id", "feature_service_name", "feature_view_id", "feature_view_name", "workspace_name"]
    FEATURE_PACKAGE_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_PACKAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_package_id: str
    feature_package_name: str
    feature_service_id: str
    feature_service_name: str
    feature_view_id: str
    feature_view_name: str
    workspace_name: str
    def __init__(self, feature_service_id: _Optional[str] = ..., feature_service_name: _Optional[str] = ..., feature_package_id: _Optional[str] = ..., feature_package_name: _Optional[str] = ..., feature_view_id: _Optional[str] = ..., feature_view_name: _Optional[str] = ..., workspace_name: _Optional[str] = ...) -> None: ...

class GetFeatureServiceStateRequest(_message.Message):
    __slots__ = ["feature_service_locator"]
    FEATURE_SERVICE_LOCATOR_FIELD_NUMBER: _ClassVar[int]
    feature_service_locator: FeatureServiceLocator
    def __init__(self, feature_service_locator: _Optional[_Union[FeatureServiceLocator, _Mapping]] = ...) -> None: ...

class GetFeatureServiceStateResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetFeaturesBatchResponse(_message.Message):
    __slots__ = ["metadata", "result"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    metadata: BatchMetadata
    result: _containers.RepeatedCompositeFieldContainer[GetFeaturesResult]
    def __init__(self, result: _Optional[_Iterable[_Union[GetFeaturesResult, _Mapping]]] = ..., metadata: _Optional[_Union[BatchMetadata, _Mapping]] = ...) -> None: ...

class GetFeaturesResponse(_message.Message):
    __slots__ = ["metadata", "result"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    metadata: Metadata
    result: GetFeaturesResult
    def __init__(self, result: _Optional[_Union[GetFeaturesResult, _Mapping]] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ...) -> None: ...

class GetFeaturesResult(_message.Message):
    __slots__ = ["features", "join_keys"]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Value]
    join_keys: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Value]
    def __init__(self, features: _Optional[_Iterable[_Union[_struct_pb2.Value, _Mapping]]] = ..., join_keys: _Optional[_Iterable[_Union[_struct_pb2.Value, _Mapping]]] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ["features", "join_keys", "partial_results", "slo_info"]
    class Item(_message.Message):
        __slots__ = ["data_type", "description", "effective_time", "name", "status", "tags", "type"]
        class TagsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        EFFECTIVE_TIME_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        TAGS_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        data_type: FeatureServerComplexDataType
        description: str
        effective_time: _timestamp_pb2.Timestamp
        name: str
        status: Status
        tags: _containers.ScalarMap[str, str]
        type: FeatureServerDataType
        def __init__(self, name: _Optional[str] = ..., effective_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., type: _Optional[_Union[FeatureServerDataType, str]] = ..., data_type: _Optional[_Union[FeatureServerComplexDataType, _Mapping]] = ..., status: _Optional[_Union[Status, str]] = ..., description: _Optional[str] = ..., tags: _Optional[_Mapping[str, str]] = ...) -> None: ...
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_RESULTS_FIELD_NUMBER: _ClassVar[int]
    SLO_INFO_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[Metadata.Item]
    join_keys: _containers.RepeatedCompositeFieldContainer[Metadata.Item]
    partial_results: bool
    slo_info: SloInfo
    def __init__(self, features: _Optional[_Iterable[_Union[Metadata.Item, _Mapping]]] = ..., join_keys: _Optional[_Iterable[_Union[Metadata.Item, _Mapping]]] = ..., slo_info: _Optional[_Union[SloInfo, _Mapping]] = ..., partial_results: bool = ...) -> None: ...

class NameAndType(_message.Message):
    __slots__ = ["data_type", "name", "type"]
    DATA_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    data_type: FeatureServerComplexDataType
    name: str
    type: FeatureServerDataType
    def __init__(self, name: _Optional[str] = ..., data_type: _Optional[_Union[FeatureServerComplexDataType, _Mapping]] = ..., type: _Optional[_Union[FeatureServerDataType, str]] = ...) -> None: ...

class QueryFeaturesRequest(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: _feature_service_request__client_pb2.GetFeaturesParameters
    def __init__(self, params: _Optional[_Union[_feature_service_request__client_pb2.GetFeaturesParameters, _Mapping]] = ...) -> None: ...

class QueryFeaturesResponse(_message.Message):
    __slots__ = ["metadata", "results"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    metadata: Metadata
    results: _containers.RepeatedCompositeFieldContainer[GetFeaturesResult]
    def __init__(self, results: _Optional[_Iterable[_Union[GetFeaturesResult, _Mapping]]] = ..., metadata: _Optional[_Union[Metadata, _Mapping]] = ...) -> None: ...

class ServiceMetadataRequest(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: FeatureServiceLocator
    def __init__(self, params: _Optional[_Union[FeatureServiceLocator, _Mapping]] = ...) -> None: ...

class ServiceMetadataRequestV2(_message.Message):
    __slots__ = ["feature_service_name", "workspace_name"]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_service_name: str
    workspace_name: str
    def __init__(self, feature_service_name: _Optional[str] = ..., workspace_name: _Optional[str] = ...) -> None: ...

class ServiceMetadataResponse(_message.Message):
    __slots__ = ["feature_service_type", "feature_values", "input_join_keys", "input_request_context_keys", "output_join_keys"]
    FEATURE_SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VALUES_FIELD_NUMBER: _ClassVar[int]
    INPUT_JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    INPUT_REQUEST_CONTEXT_KEYS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_JOIN_KEYS_FIELD_NUMBER: _ClassVar[int]
    feature_service_type: FeatureServiceType
    feature_values: _containers.RepeatedCompositeFieldContainer[NameAndType]
    input_join_keys: _containers.RepeatedCompositeFieldContainer[NameAndType]
    input_request_context_keys: _containers.RepeatedCompositeFieldContainer[NameAndType]
    output_join_keys: _containers.RepeatedCompositeFieldContainer[NameAndType]
    def __init__(self, feature_service_type: _Optional[_Union[FeatureServiceType, str]] = ..., input_join_keys: _Optional[_Iterable[_Union[NameAndType, _Mapping]]] = ..., input_request_context_keys: _Optional[_Iterable[_Union[NameAndType, _Mapping]]] = ..., output_join_keys: _Optional[_Iterable[_Union[NameAndType, _Mapping]]] = ..., feature_values: _Optional[_Iterable[_Union[NameAndType, _Mapping]]] = ...) -> None: ...

class SloInfo(_message.Message):
    __slots__ = ["dynamodb_response_size_bytes", "server_time_seconds", "slo_eligible", "slo_ineligibility_reasons", "slo_server_time_seconds", "store_max_latency", "store_response_size_bytes", "store_time_seconds"]
    DYNAMODB_RESPONSE_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    SERVER_TIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    SLO_ELIGIBLE_FIELD_NUMBER: _ClassVar[int]
    SLO_INELIGIBILITY_REASONS_FIELD_NUMBER: _ClassVar[int]
    SLO_SERVER_TIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    STORE_MAX_LATENCY_FIELD_NUMBER: _ClassVar[int]
    STORE_RESPONSE_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    STORE_TIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    dynamodb_response_size_bytes: int
    server_time_seconds: float
    slo_eligible: bool
    slo_ineligibility_reasons: _containers.RepeatedScalarFieldContainer[SloIneligibilityReason]
    slo_server_time_seconds: float
    store_max_latency: float
    store_response_size_bytes: int
    store_time_seconds: float
    def __init__(self, slo_eligible: bool = ..., slo_server_time_seconds: _Optional[float] = ..., slo_ineligibility_reasons: _Optional[_Iterable[_Union[SloIneligibilityReason, str]]] = ..., dynamodb_response_size_bytes: _Optional[int] = ..., server_time_seconds: _Optional[float] = ..., store_time_seconds: _Optional[float] = ..., store_max_latency: _Optional[float] = ..., store_response_size_bytes: _Optional[int] = ...) -> None: ...

class FeatureServiceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FeatureServerDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SloIneligibilityReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
