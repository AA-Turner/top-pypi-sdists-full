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

class BloomFilter(_message.Message):
    __slots__ = ("environment", "namespace", "num_entries", "num_expected_entries", "num_hashes", "size_bytes", "data")
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NUM_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NUM_EXPECTED_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    NUM_HASHES_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    environment: str
    namespace: str
    num_entries: int
    num_expected_entries: int
    num_hashes: int
    size_bytes: int
    data: bytes
    def __init__(
        self,
        environment: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        num_entries: _Optional[int] = ...,
        num_expected_entries: _Optional[int] = ...,
        num_hashes: _Optional[int] = ...,
        size_bytes: _Optional[int] = ...,
        data: _Optional[bytes] = ...,
    ) -> None: ...

class BloomFilterDataConfig(_message.Message):
    __slots__ = ("num_expected_entries", "target_collision_rate")
    NUM_EXPECTED_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    TARGET_COLLISION_RATE_FIELD_NUMBER: _ClassVar[int]
    num_expected_entries: int
    target_collision_rate: float
    def __init__(
        self, num_expected_entries: _Optional[int] = ..., target_collision_rate: _Optional[float] = ...
    ) -> None: ...

class BloomFilterDataStats(_message.Message):
    __slots__ = (
        "filter_size_bytes",
        "num_bits_set",
        "estimated_num_entries",
        "estimated_error_rate",
        "empirical_false_positive_rate",
    )
    FILTER_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    NUM_BITS_SET_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_NUM_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_ERROR_RATE_FIELD_NUMBER: _ClassVar[int]
    EMPIRICAL_FALSE_POSITIVE_RATE_FIELD_NUMBER: _ClassVar[int]
    filter_size_bytes: int
    num_bits_set: int
    estimated_num_entries: int
    estimated_error_rate: float
    empirical_false_positive_rate: float
    def __init__(
        self,
        filter_size_bytes: _Optional[int] = ...,
        num_bits_set: _Optional[int] = ...,
        estimated_num_entries: _Optional[int] = ...,
        estimated_error_rate: _Optional[float] = ...,
        empirical_false_positive_rate: _Optional[float] = ...,
    ) -> None: ...

class ActiveBloomFilterInfo(_message.Message):
    __slots__ = ("namespace", "config", "stats")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    config: BloomFilterDataConfig
    stats: BloomFilterDataStats
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        config: _Optional[_Union[BloomFilterDataConfig, _Mapping]] = ...,
        stats: _Optional[_Union[BloomFilterDataStats, _Mapping]] = ...,
    ) -> None: ...

class InspectBloomFiltersRequest(_message.Message):
    __slots__ = ("namespaces",)
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    namespaces: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, namespaces: _Optional[_Iterable[str]] = ...) -> None: ...

class InspectBloomFiltersResponse(_message.Message):
    __slots__ = ("active_bloom_filters",)
    ACTIVE_BLOOM_FILTERS_FIELD_NUMBER: _ClassVar[int]
    active_bloom_filters: _containers.RepeatedCompositeFieldContainer[ActiveBloomFilterInfo]
    def __init__(
        self, active_bloom_filters: _Optional[_Iterable[_Union[ActiveBloomFilterInfo, _Mapping]]] = ...
    ) -> None: ...
