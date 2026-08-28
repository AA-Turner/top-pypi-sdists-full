from chalk._gen.chalk.numericutils.v1 import values_pb2 as _values_pb2
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

class AggregationFunction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGGREGATION_FUNCTION_UNSPECIFIED: _ClassVar[AggregationFunction]
    AGGREGATION_FUNCTION_COUNT: _ClassVar[AggregationFunction]
    AGGREGATION_FUNCTION_COUNT_DISTINCT: _ClassVar[AggregationFunction]
    AGGREGATION_FUNCTION_SUM: _ClassVar[AggregationFunction]
    AGGREGATION_FUNCTION_AVG: _ClassVar[AggregationFunction]
    AGGREGATION_FUNCTION_MIN: _ClassVar[AggregationFunction]
    AGGREGATION_FUNCTION_MAX: _ClassVar[AggregationFunction]
    AGGREGATION_FUNCTION_PERCENTILE: _ClassVar[AggregationFunction]

class OtherRowMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OTHER_ROW_MODE_UNSPECIFIED: _ClassVar[OtherRowMode]
    OTHER_ROW_MODE_OMIT: _ClassVar[OtherRowMode]
    OTHER_ROW_MODE_FOLD: _ClassVar[OtherRowMode]

class NoneRowMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NONE_ROW_MODE_UNSPECIFIED: _ClassVar[NoneRowMode]
    NONE_ROW_MODE_INCLUDE: _ClassVar[NoneRowMode]
    NONE_ROW_MODE_EXCLUDE: _ClassVar[NoneRowMode]

class SortOrder(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SORT_ORDER_UNSPECIFIED: _ClassVar[SortOrder]
    SORT_ORDER_DESC: _ClassVar[SortOrder]
    SORT_ORDER_ASC: _ClassVar[SortOrder]

AGGREGATION_FUNCTION_UNSPECIFIED: AggregationFunction
AGGREGATION_FUNCTION_COUNT: AggregationFunction
AGGREGATION_FUNCTION_COUNT_DISTINCT: AggregationFunction
AGGREGATION_FUNCTION_SUM: AggregationFunction
AGGREGATION_FUNCTION_AVG: AggregationFunction
AGGREGATION_FUNCTION_MIN: AggregationFunction
AGGREGATION_FUNCTION_MAX: AggregationFunction
AGGREGATION_FUNCTION_PERCENTILE: AggregationFunction
OTHER_ROW_MODE_UNSPECIFIED: OtherRowMode
OTHER_ROW_MODE_OMIT: OtherRowMode
OTHER_ROW_MODE_FOLD: OtherRowMode
NONE_ROW_MODE_UNSPECIFIED: NoneRowMode
NONE_ROW_MODE_INCLUDE: NoneRowMode
NONE_ROW_MODE_EXCLUDE: NoneRowMode
SORT_ORDER_UNSPECIFIED: SortOrder
SORT_ORDER_DESC: SortOrder
SORT_ORDER_ASC: SortOrder

class AggregationParams(_message.Message):
    __slots__ = ("percentile",)
    PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    percentile: float
    def __init__(self, percentile: _Optional[float] = ...) -> None: ...

class Aggregation(_message.Message):
    __slots__ = ("function", "field", "params")
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    function: AggregationFunction
    field: str
    params: AggregationParams
    def __init__(
        self,
        function: _Optional[_Union[AggregationFunction, str]] = ...,
        field: _Optional[str] = ...,
        params: _Optional[_Union[AggregationParams, _Mapping]] = ...,
    ) -> None: ...

class AggregateOptions(_message.Message):
    __slots__ = ("group_by", "aggregations", "limit", "order", "other_row_mode", "none_row_mode", "order_by")
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    AGGREGATIONS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    OTHER_ROW_MODE_FIELD_NUMBER: _ClassVar[int]
    NONE_ROW_MODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    group_by: _containers.RepeatedScalarFieldContainer[str]
    aggregations: _containers.RepeatedCompositeFieldContainer[Aggregation]
    limit: int
    order: SortOrder
    other_row_mode: OtherRowMode
    none_row_mode: NoneRowMode
    order_by: int
    def __init__(
        self,
        group_by: _Optional[_Iterable[str]] = ...,
        aggregations: _Optional[_Iterable[_Union[Aggregation, _Mapping]]] = ...,
        limit: _Optional[int] = ...,
        order: _Optional[_Union[SortOrder, str]] = ...,
        other_row_mode: _Optional[_Union[OtherRowMode, str]] = ...,
        none_row_mode: _Optional[_Union[NoneRowMode, str]] = ...,
        order_by: _Optional[int] = ...,
    ) -> None: ...

class AggregateRow(_message.Message):
    __slots__ = ("group", "values")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    group: _containers.RepeatedScalarFieldContainer[str]
    values: _containers.RepeatedCompositeFieldContainer[_values_pb2.NumericValue]
    def __init__(
        self,
        group: _Optional[_Iterable[str]] = ...,
        values: _Optional[_Iterable[_Union[_values_pb2.NumericValue, _Mapping]]] = ...,
    ) -> None: ...

class AggregateColumn(_message.Message):
    __slots__ = ("function", "field", "unit", "params", "label")
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    function: AggregationFunction
    field: str
    unit: str
    params: AggregationParams
    label: str
    def __init__(
        self,
        function: _Optional[_Union[AggregationFunction, str]] = ...,
        field: _Optional[str] = ...,
        unit: _Optional[str] = ...,
        params: _Optional[_Union[AggregationParams, _Mapping]] = ...,
        label: _Optional[str] = ...,
    ) -> None: ...

class AggregateTable(_message.Message):
    __slots__ = ("rows", "columns", "truncated", "total_group_count")
    ROWS_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    TRUNCATED_FIELD_NUMBER: _ClassVar[int]
    TOTAL_GROUP_COUNT_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[AggregateRow]
    columns: _containers.RepeatedCompositeFieldContainer[AggregateColumn]
    truncated: bool
    total_group_count: int
    def __init__(
        self,
        rows: _Optional[_Iterable[_Union[AggregateRow, _Mapping]]] = ...,
        columns: _Optional[_Iterable[_Union[AggregateColumn, _Mapping]]] = ...,
        truncated: bool = ...,
        total_group_count: _Optional[int] = ...,
    ) -> None: ...
