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

class ColumnProfileOptions(_message.Message):
    __slots__ = ("enabled",)
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    def __init__(self, enabled: bool = ...) -> None: ...

class ColumnProfilePercentile(_message.Message):
    __slots__ = ("percentile", "value")
    PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    percentile: float
    value: float
    def __init__(self, percentile: _Optional[float] = ..., value: _Optional[float] = ...) -> None: ...

class ColumnProfilePercentileLadder(_message.Message):
    __slots__ = ("points",)
    POINTS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[ColumnProfilePercentile]
    def __init__(self, points: _Optional[_Iterable[_Union[ColumnProfilePercentile, _Mapping]]] = ...) -> None: ...

class ColumnProfileDistribution(_message.Message):
    __slots__ = ("ladder",)
    LADDER_FIELD_NUMBER: _ClassVar[int]
    ladder: ColumnProfilePercentileLadder
    def __init__(self, ladder: _Optional[_Union[ColumnProfilePercentileLadder, _Mapping]] = ...) -> None: ...

class ColumnProfile(_message.Message):
    __slots__ = ("column", "distribution", "filled_count", "empty_count", "min", "max", "sum", "mean")
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    FILLED_COUNT_FIELD_NUMBER: _ClassVar[int]
    EMPTY_COUNT_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    SUM_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    column: str
    distribution: ColumnProfileDistribution
    filled_count: int
    empty_count: int
    min: float
    max: float
    sum: float
    mean: float
    def __init__(
        self,
        column: _Optional[str] = ...,
        distribution: _Optional[_Union[ColumnProfileDistribution, _Mapping]] = ...,
        filled_count: _Optional[int] = ...,
        empty_count: _Optional[int] = ...,
        min: _Optional[float] = ...,
        max: _Optional[float] = ...,
        sum: _Optional[float] = ...,
        mean: _Optional[float] = ...,
    ) -> None: ...
