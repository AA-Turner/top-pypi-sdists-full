from google.protobuf import struct_pb2 as _struct_pb2
from tecton_proto.args import feature_view__client_pb2 as _feature_view__client_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetFeaturesBatchParameters(_message.Message):
    __slots__ = ["feature_service_id", "feature_service_name", "metadata_options", "request_data", "request_options", "workspace_name"]
    FEATURE_SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_DATA_FIELD_NUMBER: _ClassVar[int]
    REQUEST_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_service_id: str
    feature_service_name: str
    metadata_options: MetadataOptions
    request_data: _containers.RepeatedCompositeFieldContainer[GetFeaturesBatchRequestData]
    request_options: RequestOptions
    workspace_name: str
    def __init__(self, feature_service_id: _Optional[str] = ..., feature_service_name: _Optional[str] = ..., workspace_name: _Optional[str] = ..., request_data: _Optional[_Iterable[_Union[GetFeaturesBatchRequestData, _Mapping]]] = ..., metadata_options: _Optional[_Union[MetadataOptions, _Mapping]] = ..., request_options: _Optional[_Union[RequestOptions, _Mapping]] = ...) -> None: ...

class GetFeaturesBatchParametersV2(_message.Message):
    __slots__ = ["feature_service_name", "metadata_options", "request_data", "request_options", "workspace_name"]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_DATA_FIELD_NUMBER: _ClassVar[int]
    REQUEST_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    feature_service_name: str
    metadata_options: MetadataOptions
    request_data: _containers.RepeatedCompositeFieldContainer[GetFeaturesBatchRequestData]
    request_options: RequestOptions
    workspace_name: str
    def __init__(self, feature_service_name: _Optional[str] = ..., workspace_name: _Optional[str] = ..., request_data: _Optional[_Iterable[_Union[GetFeaturesBatchRequestData, _Mapping]]] = ..., metadata_options: _Optional[_Union[MetadataOptions, _Mapping]] = ..., request_options: _Optional[_Union[RequestOptions, _Mapping]] = ...) -> None: ...

class GetFeaturesBatchRequest(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: GetFeaturesBatchParameters
    def __init__(self, params: _Optional[_Union[GetFeaturesBatchParameters, _Mapping]] = ...) -> None: ...

class GetFeaturesBatchRequestData(_message.Message):
    __slots__ = ["join_key_map", "request_context_map"]
    class JoinKeyMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class RequestContextMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    JOIN_KEY_MAP_FIELD_NUMBER: _ClassVar[int]
    REQUEST_CONTEXT_MAP_FIELD_NUMBER: _ClassVar[int]
    join_key_map: _containers.MessageMap[str, _struct_pb2.Value]
    request_context_map: _containers.MessageMap[str, _struct_pb2.Value]
    def __init__(self, join_key_map: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., request_context_map: _Optional[_Mapping[str, _struct_pb2.Value]] = ...) -> None: ...

class GetFeaturesBatchRequestV2(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: GetFeaturesBatchParametersV2
    def __init__(self, params: _Optional[_Union[GetFeaturesBatchParametersV2, _Mapping]] = ...) -> None: ...

class GetFeaturesParameters(_message.Message):
    __slots__ = ["allow_partial_results", "feature_package_id", "feature_package_name", "feature_service_id", "feature_service_name", "feature_view_id", "feature_view_name", "isCallerBatch", "join_key_map", "metadata_options", "request_context_map", "request_options", "workspace_name"]
    class JoinKeyMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class RequestContextMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    ALLOW_PARTIAL_RESULTS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_PACKAGE_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_PACKAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_ID_FIELD_NUMBER: _ClassVar[int]
    FEATURE_VIEW_NAME_FIELD_NUMBER: _ClassVar[int]
    ISCALLERBATCH_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEY_MAP_FIELD_NUMBER: _ClassVar[int]
    METADATA_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_CONTEXT_MAP_FIELD_NUMBER: _ClassVar[int]
    REQUEST_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    allow_partial_results: bool
    feature_package_id: str
    feature_package_name: str
    feature_service_id: str
    feature_service_name: str
    feature_view_id: str
    feature_view_name: str
    isCallerBatch: bool
    join_key_map: _containers.MessageMap[str, _struct_pb2.Value]
    metadata_options: MetadataOptions
    request_context_map: _containers.MessageMap[str, _struct_pb2.Value]
    request_options: RequestOptions
    workspace_name: str
    def __init__(self, feature_service_id: _Optional[str] = ..., feature_service_name: _Optional[str] = ..., feature_package_id: _Optional[str] = ..., feature_package_name: _Optional[str] = ..., feature_view_id: _Optional[str] = ..., feature_view_name: _Optional[str] = ..., workspace_name: _Optional[str] = ..., join_key_map: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., request_context_map: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., metadata_options: _Optional[_Union[MetadataOptions, _Mapping]] = ..., allow_partial_results: bool = ..., request_options: _Optional[_Union[RequestOptions, _Mapping]] = ..., isCallerBatch: bool = ...) -> None: ...

class GetFeaturesParametersV2(_message.Message):
    __slots__ = ["allow_partial_results", "feature_service_name", "isCallerBatch", "join_key_map", "metadata_options", "request_context_map", "request_options", "workspace_name"]
    class JoinKeyMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    class RequestContextMapEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    ALLOW_PARTIAL_RESULTS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    ISCALLERBATCH_FIELD_NUMBER: _ClassVar[int]
    JOIN_KEY_MAP_FIELD_NUMBER: _ClassVar[int]
    METADATA_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_CONTEXT_MAP_FIELD_NUMBER: _ClassVar[int]
    REQUEST_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_NAME_FIELD_NUMBER: _ClassVar[int]
    allow_partial_results: bool
    feature_service_name: str
    isCallerBatch: bool
    join_key_map: _containers.MessageMap[str, _struct_pb2.Value]
    metadata_options: MetadataOptions
    request_context_map: _containers.MessageMap[str, _struct_pb2.Value]
    request_options: RequestOptions
    workspace_name: str
    def __init__(self, feature_service_name: _Optional[str] = ..., workspace_name: _Optional[str] = ..., join_key_map: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., request_context_map: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., metadata_options: _Optional[_Union[MetadataOptions, _Mapping]] = ..., allow_partial_results: bool = ..., request_options: _Optional[_Union[RequestOptions, _Mapping]] = ..., isCallerBatch: bool = ...) -> None: ...

class GetFeaturesRequest(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: GetFeaturesParameters
    def __init__(self, params: _Optional[_Union[GetFeaturesParameters, _Mapping]] = ...) -> None: ...

class GetFeaturesRequestV2(_message.Message):
    __slots__ = ["params"]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: GetFeaturesParametersV2
    def __init__(self, params: _Optional[_Union[GetFeaturesParametersV2, _Mapping]] = ...) -> None: ...

class MetadataOptions(_message.Message):
    __slots__ = ["include_data_types", "include_effective_times", "include_feature_descriptions", "include_feature_tags", "include_names", "include_serving_status", "include_slo_info", "include_types"]
    INCLUDE_DATA_TYPES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_EFFECTIVE_TIMES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FEATURE_DESCRIPTIONS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_FEATURE_TAGS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_NAMES_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SERVING_STATUS_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_SLO_INFO_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_TYPES_FIELD_NUMBER: _ClassVar[int]
    include_data_types: bool
    include_effective_times: bool
    include_feature_descriptions: bool
    include_feature_tags: bool
    include_names: bool
    include_serving_status: bool
    include_slo_info: bool
    include_types: bool
    def __init__(self, include_names: bool = ..., include_effective_times: bool = ..., include_types: bool = ..., include_data_types: bool = ..., include_slo_info: bool = ..., include_serving_status: bool = ..., include_feature_descriptions: bool = ..., include_feature_tags: bool = ...) -> None: ...

class RequestOptions(_message.Message):
    __slots__ = ["aggregation_leading_edge", "high_watermark_override", "ignore_extra_request_context_fields", "latency_budget_ms", "read_from_cache", "write_to_cache"]
    AGGREGATION_LEADING_EDGE_FIELD_NUMBER: _ClassVar[int]
    HIGH_WATERMARK_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    IGNORE_EXTRA_REQUEST_CONTEXT_FIELDS_FIELD_NUMBER: _ClassVar[int]
    LATENCY_BUDGET_MS_FIELD_NUMBER: _ClassVar[int]
    READ_FROM_CACHE_FIELD_NUMBER: _ClassVar[int]
    WRITE_TO_CACHE_FIELD_NUMBER: _ClassVar[int]
    aggregation_leading_edge: _feature_view__client_pb2.AggregationLeadingEdge
    high_watermark_override: _timestamp_pb2.Timestamp
    ignore_extra_request_context_fields: bool
    latency_budget_ms: int
    read_from_cache: bool
    write_to_cache: bool
    def __init__(self, read_from_cache: bool = ..., write_to_cache: bool = ..., ignore_extra_request_context_fields: bool = ..., latency_budget_ms: _Optional[int] = ..., aggregation_leading_edge: _Optional[_Union[_feature_view__client_pb2.AggregationLeadingEdge, str]] = ..., high_watermark_override: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
