from tecton_proto.canary import type__client_pb2 as _type__client_pb2
from tecton_proto.data import feature_view__client_pb2 as _feature_view__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OnlineStoreMetadataConfiguration(_message.Message):
    __slots__ = ["execution_table_name", "online_store_params"]
    EXECUTION_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    ONLINE_STORE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    execution_table_name: str
    online_store_params: _feature_view__client_pb2.OnlineStoreParams
    def __init__(self, execution_table_name: _Optional[str] = ..., online_store_params: _Optional[_Union[_feature_view__client_pb2.OnlineStoreParams, _Mapping]] = ...) -> None: ...

class OnlineStoreWriterConfiguration(_message.Message):
    __slots__ = ["canary_downsample_factor", "canary_id", "canary_table_name", "canary_type", "data_table_name", "feature_flags", "online_store_params", "status_table_name"]
    class FeatureFlagsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...
    CANARY_DOWNSAMPLE_FACTOR_FIELD_NUMBER: _ClassVar[int]
    CANARY_ID_FIELD_NUMBER: _ClassVar[int]
    CANARY_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    CANARY_TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    ONLINE_STORE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    STATUS_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    canary_downsample_factor: int
    canary_id: str
    canary_table_name: str
    canary_type: _type__client_pb2.CanaryType
    data_table_name: str
    feature_flags: _containers.ScalarMap[str, bool]
    online_store_params: _feature_view__client_pb2.OnlineStoreParams
    status_table_name: str
    def __init__(self, status_table_name: _Optional[str] = ..., data_table_name: _Optional[str] = ..., canary_table_name: _Optional[str] = ..., canary_type: _Optional[_Union[_type__client_pb2.CanaryType, str]] = ..., canary_id: _Optional[str] = ..., canary_downsample_factor: _Optional[int] = ..., online_store_params: _Optional[_Union[_feature_view__client_pb2.OnlineStoreParams, _Mapping]] = ..., feature_flags: _Optional[_Mapping[str, bool]] = ...) -> None: ...
