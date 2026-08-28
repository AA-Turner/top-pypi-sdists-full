from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from chalk._gen.chalk.searchaggregates.v1 import aggregation_pb2 as _aggregation_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
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

class NotebookCellDisplayMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOTEBOOK_CELL_DISPLAY_MODE_UNSPECIFIED: _ClassVar[NotebookCellDisplayMode]
    NOTEBOOK_CELL_DISPLAY_MODE_OUTPUT: _ClassVar[NotebookCellDisplayMode]
    NOTEBOOK_CELL_DISPLAY_MODE_SOURCE: _ClassVar[NotebookCellDisplayMode]
    NOTEBOOK_CELL_DISPLAY_MODE_SOURCE_AND_OUTPUT: _ClassVar[NotebookCellDisplayMode]

NOTEBOOK_CELL_DISPLAY_MODE_UNSPECIFIED: NotebookCellDisplayMode
NOTEBOOK_CELL_DISPLAY_MODE_OUTPUT: NotebookCellDisplayMode
NOTEBOOK_CELL_DISPLAY_MODE_SOURCE: NotebookCellDisplayMode
NOTEBOOK_CELL_DISPLAY_MODE_SOURCE_AND_OUTPUT: NotebookCellDisplayMode

class GridPosition(_message.Message):
    __slots__ = ("x", "y", "w", "h")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    H_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    w: int
    h: int
    def __init__(
        self, x: _Optional[int] = ..., y: _Optional[int] = ..., w: _Optional[int] = ..., h: _Optional[int] = ...
    ) -> None: ...

class DashboardWidget(_message.Message):
    __slots__ = ("id", "position", "data_widget", "markdown", "section_title", "notebook_cell")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATA_WIDGET_FIELD_NUMBER: _ClassVar[int]
    MARKDOWN_FIELD_NUMBER: _ClassVar[int]
    SECTION_TITLE_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_CELL_FIELD_NUMBER: _ClassVar[int]
    id: str
    position: GridPosition
    data_widget: DashboardDataWidget
    markdown: DashboardMarkdownWidget
    section_title: DashboardSectionTitleWidget
    notebook_cell: DashboardNotebookCellWidget
    def __init__(
        self,
        id: _Optional[str] = ...,
        position: _Optional[_Union[GridPosition, _Mapping]] = ...,
        data_widget: _Optional[_Union[DashboardDataWidget, _Mapping]] = ...,
        markdown: _Optional[_Union[DashboardMarkdownWidget, _Mapping]] = ...,
        section_title: _Optional[_Union[DashboardSectionTitleWidget, _Mapping]] = ...,
        notebook_cell: _Optional[_Union[DashboardNotebookCellWidget, _Mapping]] = ...,
    ) -> None: ...

class NotebookCellDisplay(_message.Message):
    __slots__ = ("mode",)
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: NotebookCellDisplayMode
    def __init__(self, mode: _Optional[_Union[NotebookCellDisplayMode, str]] = ...) -> None: ...

class DashboardNotebookCellWidget(_message.Message):
    __slots__ = ("notebook_id", "cell_id", "display")
    NOTEBOOK_ID_FIELD_NUMBER: _ClassVar[int]
    CELL_ID_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    notebook_id: str
    cell_id: str
    display: NotebookCellDisplay
    def __init__(
        self,
        notebook_id: _Optional[str] = ...,
        cell_id: _Optional[str] = ...,
        display: _Optional[_Union[NotebookCellDisplay, _Mapping]] = ...,
    ) -> None: ...

class DashboardDataWidget(_message.Message):
    __slots__ = ("name", "metric_query", "source_query", "timeseries", "table", "statistic")
    NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_QUERY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_QUERY_FIELD_NUMBER: _ClassVar[int]
    TIMESERIES_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    STATISTIC_FIELD_NUMBER: _ClassVar[int]
    name: str
    metric_query: DashboardMetricQuery
    source_query: DashboardSourceQuery
    timeseries: DashboardTimeseriesViz
    table: DashboardTableViz
    statistic: DashboardStatisticViz
    def __init__(
        self,
        name: _Optional[str] = ...,
        metric_query: _Optional[_Union[DashboardMetricQuery, _Mapping]] = ...,
        source_query: _Optional[_Union[DashboardSourceQuery, _Mapping]] = ...,
        timeseries: _Optional[_Union[DashboardTimeseriesViz, _Mapping]] = ...,
        table: _Optional[_Union[DashboardTableViz, _Mapping]] = ...,
        statistic: _Optional[_Union[DashboardStatisticViz, _Mapping]] = ...,
    ) -> None: ...

class DashboardMetricQuery(_message.Message):
    __slots__ = ("window_period", "series", "formulas", "display_window_period")
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    FORMULAS_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    window_period: str
    series: _containers.RepeatedCompositeFieldContainer[_chart_pb2.MetricConfigSeries]
    formulas: _containers.RepeatedCompositeFieldContainer[_chart_pb2.MetricFormula]
    display_window_period: str
    def __init__(
        self,
        window_period: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[_chart_pb2.MetricConfigSeries, _Mapping]]] = ...,
        formulas: _Optional[_Iterable[_Union[_chart_pb2.MetricFormula, _Mapping]]] = ...,
        display_window_period: _Optional[str] = ...,
    ) -> None: ...

class DashboardSourceQuery(_message.Message):
    __slots__ = ("data_source", "query", "aggregate_options")
    DATA_SOURCE_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    data_source: str
    query: str
    aggregate_options: _aggregation_pb2.AggregateOptions
    def __init__(
        self,
        data_source: _Optional[str] = ...,
        query: _Optional[str] = ...,
        aggregate_options: _Optional[_Union[_aggregation_pb2.AggregateOptions, _Mapping]] = ...,
    ) -> None: ...

class DashboardTimeseriesViz(_message.Message):
    __slots__ = ("plot_style",)
    PLOT_STYLE_FIELD_NUMBER: _ClassVar[int]
    plot_style: str
    def __init__(self, plot_style: _Optional[str] = ...) -> None: ...

class DashboardTableColumn(_message.Message):
    __slots__ = ("key", "width_px", "visible")
    KEY_FIELD_NUMBER: _ClassVar[int]
    WIDTH_PX_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    key: str
    width_px: int
    visible: bool
    def __init__(self, key: _Optional[str] = ..., width_px: _Optional[int] = ..., visible: bool = ...) -> None: ...

class DashboardTableViz(_message.Message):
    __slots__ = ("columns", "column_order")
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    COLUMN_ORDER_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[DashboardTableColumn]
    column_order: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        columns: _Optional[_Iterable[_Union[DashboardTableColumn, _Mapping]]] = ...,
        column_order: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class DashboardStatisticViz(_message.Message):
    __slots__ = ("compare_to_previous", "number_format", "unit_label")
    COMPARE_TO_PREVIOUS_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FORMAT_FIELD_NUMBER: _ClassVar[int]
    UNIT_LABEL_FIELD_NUMBER: _ClassVar[int]
    compare_to_previous: bool
    number_format: str
    unit_label: str
    def __init__(
        self, compare_to_previous: bool = ..., number_format: _Optional[str] = ..., unit_label: _Optional[str] = ...
    ) -> None: ...

class DashboardMarkdownWidget(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...

class DashboardSectionTitleWidget(_message.Message):
    __slots__ = ("title",)
    TITLE_FIELD_NUMBER: _ClassVar[int]
    title: str
    def __init__(self, title: _Optional[str] = ...) -> None: ...

class Dashboard(_message.Message):
    __slots__ = (
        "id",
        "environment_id",
        "name",
        "widgets",
        "description",
        "created_at",
        "updated_at",
        "created_by",
        "owner_type",
        "owner_id",
        "read_only",
        "total_view_count",
        "viewer_last_viewed_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WIDGETS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    OWNER_TYPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    READ_ONLY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VIEW_COUNT_FIELD_NUMBER: _ClassVar[int]
    VIEWER_LAST_VIEWED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    environment_id: str
    name: str
    widgets: _containers.RepeatedCompositeFieldContainer[DashboardWidget]
    description: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    created_by: str
    owner_type: str
    owner_id: str
    read_only: bool
    total_view_count: int
    viewer_last_viewed_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        widgets: _Optional[_Iterable[_Union[DashboardWidget, _Mapping]]] = ...,
        description: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        created_by: _Optional[str] = ...,
        owner_type: _Optional[str] = ...,
        owner_id: _Optional[str] = ...,
        read_only: bool = ...,
        total_view_count: _Optional[int] = ...,
        viewer_last_viewed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...
