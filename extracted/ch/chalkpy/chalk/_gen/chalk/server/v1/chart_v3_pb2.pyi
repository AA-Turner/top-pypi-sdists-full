from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.chart.v3 import chart_pb2 as _chart_pb2
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

class ChartV3Aggregation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHART_V3_AGGREGATION_UNSPECIFIED: _ClassVar[ChartV3Aggregation]
    CHART_V3_AGGREGATION_NONE: _ClassVar[ChartV3Aggregation]
    CHART_V3_AGGREGATION_COUNT: _ClassVar[ChartV3Aggregation]
    CHART_V3_AGGREGATION_SUM: _ClassVar[ChartV3Aggregation]
    CHART_V3_AGGREGATION_MEAN: _ClassVar[ChartV3Aggregation]
    CHART_V3_AGGREGATION_MIN: _ClassVar[ChartV3Aggregation]
    CHART_V3_AGGREGATION_MAX: _ClassVar[ChartV3Aggregation]

CHART_V3_AGGREGATION_UNSPECIFIED: ChartV3Aggregation
CHART_V3_AGGREGATION_NONE: ChartV3Aggregation
CHART_V3_AGGREGATION_COUNT: ChartV3Aggregation
CHART_V3_AGGREGATION_SUM: ChartV3Aggregation
CHART_V3_AGGREGATION_MEAN: ChartV3Aggregation
CHART_V3_AGGREGATION_MIN: ChartV3Aggregation
CHART_V3_AGGREGATION_MAX: ChartV3Aggregation

class ChartV3Measure(_message.Message):
    __slots__ = ("column", "aggregation", "label", "draw_style", "stacking_mode", "use_secondary_value_axis")
    COLUMN_FIELD_NUMBER: _ClassVar[int]
    AGGREGATION_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DRAW_STYLE_FIELD_NUMBER: _ClassVar[int]
    STACKING_MODE_FIELD_NUMBER: _ClassVar[int]
    USE_SECONDARY_VALUE_AXIS_FIELD_NUMBER: _ClassVar[int]
    column: str
    aggregation: ChartV3Aggregation
    label: str
    draw_style: _chart_pb2.DrawStyle
    stacking_mode: _chart_pb2.StackingMode
    use_secondary_value_axis: bool
    def __init__(
        self,
        column: _Optional[str] = ...,
        aggregation: _Optional[_Union[ChartV3Aggregation, str]] = ...,
        label: _Optional[str] = ...,
        draw_style: _Optional[_Union[_chart_pb2.DrawStyle, str]] = ...,
        stacking_mode: _Optional[_Union[_chart_pb2.StackingMode, str]] = ...,
        use_secondary_value_axis: bool = ...,
    ) -> None: ...

class ChartV3GroupedQuery(_message.Message):
    __slots__ = ("base_axis_column", "measures", "color_column", "series_limit")
    BASE_AXIS_COLUMN_FIELD_NUMBER: _ClassVar[int]
    MEASURES_FIELD_NUMBER: _ClassVar[int]
    COLOR_COLUMN_FIELD_NUMBER: _ClassVar[int]
    SERIES_LIMIT_FIELD_NUMBER: _ClassVar[int]
    base_axis_column: str
    measures: _containers.RepeatedCompositeFieldContainer[ChartV3Measure]
    color_column: str
    series_limit: int
    def __init__(
        self,
        base_axis_column: _Optional[str] = ...,
        measures: _Optional[_Iterable[_Union[ChartV3Measure, _Mapping]]] = ...,
        color_column: _Optional[str] = ...,
        series_limit: _Optional[int] = ...,
    ) -> None: ...

class ChartV3HistogramQuery(_message.Message):
    __slots__ = ("value_column", "max_bins", "bin_width")
    VALUE_COLUMN_FIELD_NUMBER: _ClassVar[int]
    MAX_BINS_FIELD_NUMBER: _ClassVar[int]
    BIN_WIDTH_FIELD_NUMBER: _ClassVar[int]
    value_column: str
    max_bins: int
    bin_width: float
    def __init__(
        self, value_column: _Optional[str] = ..., max_bins: _Optional[int] = ..., bin_width: _Optional[float] = ...
    ) -> None: ...

class RenderChartV3Request(_message.Message):
    __slots__ = ("arrow_ipc", "grouped", "histogram", "title", "orientation")
    ARROW_IPC_FIELD_NUMBER: _ClassVar[int]
    GROUPED_FIELD_NUMBER: _ClassVar[int]
    HISTOGRAM_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    arrow_ipc: bytes
    grouped: ChartV3GroupedQuery
    histogram: ChartV3HistogramQuery
    title: str
    orientation: _chart_pb2.Orientation
    def __init__(
        self,
        arrow_ipc: _Optional[bytes] = ...,
        grouped: _Optional[_Union[ChartV3GroupedQuery, _Mapping]] = ...,
        histogram: _Optional[_Union[ChartV3HistogramQuery, _Mapping]] = ...,
        title: _Optional[str] = ...,
        orientation: _Optional[_Union[_chart_pb2.Orientation, str]] = ...,
    ) -> None: ...

class RenderChartV3Response(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _chart_pb2.TabularChart
    def __init__(self, chart: _Optional[_Union[_chart_pb2.TabularChart, _Mapping]] = ...) -> None: ...
