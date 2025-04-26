from chalk._gen.chalk.arrow.v1 import arrow_pb2 as _arrow_pb2
from chalk._gen.chalk.common.v1 import operation_kind_pb2 as _operation_kind_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
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

class FeatureValuesTimestampType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FEATURE_VALUES_TIMESTAMP_TYPE_UNSPECIFIED: _ClassVar[FeatureValuesTimestampType]
    FEATURE_VALUES_TIMESTAMP_TYPE_INSERTED_AT: _ClassVar[FeatureValuesTimestampType]
    FEATURE_VALUES_TIMESTAMP_TYPE_OBSERVED_AT: _ClassVar[FeatureValuesTimestampType]

FEATURE_VALUES_TIMESTAMP_TYPE_UNSPECIFIED: FeatureValuesTimestampType
FEATURE_VALUES_TIMESTAMP_TYPE_INSERTED_AT: FeatureValuesTimestampType
FEATURE_VALUES_TIMESTAMP_TYPE_OBSERVED_AT: FeatureValuesTimestampType

class FeatureValueFilters(_message.Message):
    __slots__ = ("resolver_fqn", "deployment_id", "operation_id", "operation_kind", "primary_key")
    RESOLVER_FQN_FIELD_NUMBER: _ClassVar[int]
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_FIELD_NUMBER: _ClassVar[int]
    OPERATION_KIND_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_KEY_FIELD_NUMBER: _ClassVar[int]
    resolver_fqn: _containers.RepeatedScalarFieldContainer[str]
    deployment_id: _containers.RepeatedScalarFieldContainer[str]
    operation_id: _containers.RepeatedScalarFieldContainer[str]
    operation_kind: _containers.RepeatedScalarFieldContainer[_operation_kind_pb2.OperationKind]
    primary_key: _containers.RepeatedCompositeFieldContainer[_arrow_pb2.ScalarValue]
    def __init__(
        self,
        resolver_fqn: _Optional[_Iterable[str]] = ...,
        deployment_id: _Optional[_Iterable[str]] = ...,
        operation_id: _Optional[_Iterable[str]] = ...,
        operation_kind: _Optional[_Iterable[_Union[_operation_kind_pb2.OperationKind, str]]] = ...,
        primary_key: _Optional[_Iterable[_Union[_arrow_pb2.ScalarValue, _Mapping]]] = ...,
    ) -> None: ...

class GetFeatureValuesPageToken(_message.Message):
    __slots__ = ("timestamp_hwm", "operation_id_hwm", "observation_id_hwm")
    TIMESTAMP_HWM_FIELD_NUMBER: _ClassVar[int]
    OPERATION_ID_HWM_FIELD_NUMBER: _ClassVar[int]
    OBSERVATION_ID_HWM_FIELD_NUMBER: _ClassVar[int]
    timestamp_hwm: _timestamp_pb2.Timestamp
    operation_id_hwm: str
    observation_id_hwm: str
    def __init__(
        self,
        timestamp_hwm: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        operation_id_hwm: _Optional[str] = ...,
        observation_id_hwm: _Optional[str] = ...,
    ) -> None: ...

class GetFeatureValuesRequest(_message.Message):
    __slots__ = (
        "feature_fqn",
        "timestamp_type",
        "lower_bound_inclusive",
        "upper_bound_exclusive",
        "filters",
        "page_size",
        "page_token",
    )
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOWER_BOUND_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    UPPER_BOUND_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    feature_fqn: str
    timestamp_type: FeatureValuesTimestampType
    lower_bound_inclusive: _timestamp_pb2.Timestamp
    upper_bound_exclusive: _timestamp_pb2.Timestamp
    filters: FeatureValueFilters
    page_size: int
    page_token: str
    def __init__(
        self,
        feature_fqn: _Optional[str] = ...,
        timestamp_type: _Optional[_Union[FeatureValuesTimestampType, str]] = ...,
        lower_bound_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        upper_bound_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        filters: _Optional[_Union[FeatureValueFilters, _Mapping]] = ...,
        page_size: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class GetFeatureValuesResponse(_message.Message):
    __slots__ = ("next_page_token", "total_size", "parquet")
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    PARQUET_FIELD_NUMBER: _ClassVar[int]
    next_page_token: str
    total_size: int
    parquet: bytes
    def __init__(
        self, next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ..., parquet: _Optional[bytes] = ...
    ) -> None: ...
