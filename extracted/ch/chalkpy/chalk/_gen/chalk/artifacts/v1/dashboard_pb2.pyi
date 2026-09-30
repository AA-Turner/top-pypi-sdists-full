from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from chalk._gen.chalk.artifacts.v1 import value_tone_pb2 as _value_tone_pb2
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
    __slots__ = (
        "id",
        "position",
        "data_widget",
        "markdown",
        "section_title",
        "notebook_cell",
        "monitor_widget",
        "latest_deployment",
        "incident_widget",
        "connection_health",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATA_WIDGET_FIELD_NUMBER: _ClassVar[int]
    MARKDOWN_FIELD_NUMBER: _ClassVar[int]
    SECTION_TITLE_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_CELL_FIELD_NUMBER: _ClassVar[int]
    MONITOR_WIDGET_FIELD_NUMBER: _ClassVar[int]
    LATEST_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    INCIDENT_WIDGET_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_HEALTH_FIELD_NUMBER: _ClassVar[int]
    id: str
    position: GridPosition
    data_widget: DashboardDataWidget
    markdown: DashboardMarkdownWidget
    section_title: DashboardSectionTitleWidget
    notebook_cell: DashboardNotebookCellWidget
    monitor_widget: DashboardMonitorWidget
    latest_deployment: DashboardLatestDeploymentWidget
    incident_widget: DashboardIncidentWidget
    connection_health: DashboardConnectionHealthWidget
    def __init__(
        self,
        id: _Optional[str] = ...,
        position: _Optional[_Union[GridPosition, _Mapping]] = ...,
        data_widget: _Optional[_Union[DashboardDataWidget, _Mapping]] = ...,
        markdown: _Optional[_Union[DashboardMarkdownWidget, _Mapping]] = ...,
        section_title: _Optional[_Union[DashboardSectionTitleWidget, _Mapping]] = ...,
        notebook_cell: _Optional[_Union[DashboardNotebookCellWidget, _Mapping]] = ...,
        monitor_widget: _Optional[_Union[DashboardMonitorWidget, _Mapping]] = ...,
        latest_deployment: _Optional[_Union[DashboardLatestDeploymentWidget, _Mapping]] = ...,
        incident_widget: _Optional[_Union[DashboardIncidentWidget, _Mapping]] = ...,
        connection_health: _Optional[_Union[DashboardConnectionHealthWidget, _Mapping]] = ...,
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
    __slots__ = ("name", "metric_query", "source_query", "timeseries", "table", "statistic", "tree_map", "pie")
    NAME_FIELD_NUMBER: _ClassVar[int]
    METRIC_QUERY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_QUERY_FIELD_NUMBER: _ClassVar[int]
    TIMESERIES_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    STATISTIC_FIELD_NUMBER: _ClassVar[int]
    TREE_MAP_FIELD_NUMBER: _ClassVar[int]
    PIE_FIELD_NUMBER: _ClassVar[int]
    name: str
    metric_query: DashboardMetricQuery
    source_query: DashboardSourceQuery
    timeseries: DashboardTimeseriesViz
    table: DashboardTableViz
    statistic: DashboardStatisticViz
    tree_map: DashboardTreeMapViz
    pie: DashboardPieViz
    def __init__(
        self,
        name: _Optional[str] = ...,
        metric_query: _Optional[_Union[DashboardMetricQuery, _Mapping]] = ...,
        source_query: _Optional[_Union[DashboardSourceQuery, _Mapping]] = ...,
        timeseries: _Optional[_Union[DashboardTimeseriesViz, _Mapping]] = ...,
        table: _Optional[_Union[DashboardTableViz, _Mapping]] = ...,
        statistic: _Optional[_Union[DashboardStatisticViz, _Mapping]] = ...,
        tree_map: _Optional[_Union[DashboardTreeMapViz, _Mapping]] = ...,
        pie: _Optional[_Union[DashboardPieViz, _Mapping]] = ...,
    ) -> None: ...

class DashboardMonitorWidget(_message.Message):
    __slots__ = ("monitor_id",)
    MONITOR_ID_FIELD_NUMBER: _ClassVar[int]
    monitor_id: str
    def __init__(self, monitor_id: _Optional[str] = ...) -> None: ...

class DashboardConnectionHealthWidget(_message.Message):
    __slots__ = ("connection_ids",)
    CONNECTION_IDS_FIELD_NUMBER: _ClassVar[int]
    connection_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, connection_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DashboardLatestDeploymentWidget(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DashboardIncidentWidget(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: DashboardIncidentFilters
    def __init__(self, filters: _Optional[_Union[DashboardIncidentFilters, _Mapping]] = ...) -> None: ...

class DashboardIncidentFilters(_message.Message):
    __slots__ = ("has_closed_filter", "linked_entity_kind_filter", "linked_entity_id_filter", "linked_entity_kind")
    HAS_CLOSED_FILTER_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_KIND_FILTER_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_ID_FILTER_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_KIND_FIELD_NUMBER: _ClassVar[int]
    has_closed_filter: bool
    linked_entity_kind_filter: int
    linked_entity_id_filter: str
    linked_entity_kind: str
    def __init__(
        self,
        has_closed_filter: bool = ...,
        linked_entity_kind_filter: _Optional[int] = ...,
        linked_entity_id_filter: _Optional[str] = ...,
        linked_entity_kind: _Optional[str] = ...,
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
    __slots__ = (
        "plot_style",
        "initially_hidden_series",
        "y_axis_label",
        "hide_falsy_in_tooltip",
        "y_axis_soft_min",
        "y_axis_soft_max",
    )
    PLOT_STYLE_FIELD_NUMBER: _ClassVar[int]
    INITIALLY_HIDDEN_SERIES_FIELD_NUMBER: _ClassVar[int]
    Y_AXIS_LABEL_FIELD_NUMBER: _ClassVar[int]
    HIDE_FALSY_IN_TOOLTIP_FIELD_NUMBER: _ClassVar[int]
    Y_AXIS_SOFT_MIN_FIELD_NUMBER: _ClassVar[int]
    Y_AXIS_SOFT_MAX_FIELD_NUMBER: _ClassVar[int]
    plot_style: str
    initially_hidden_series: _containers.RepeatedScalarFieldContainer[str]
    y_axis_label: str
    hide_falsy_in_tooltip: bool
    y_axis_soft_min: float
    y_axis_soft_max: float
    def __init__(
        self,
        plot_style: _Optional[str] = ...,
        initially_hidden_series: _Optional[_Iterable[str]] = ...,
        y_axis_label: _Optional[str] = ...,
        hide_falsy_in_tooltip: bool = ...,
        y_axis_soft_min: _Optional[float] = ...,
        y_axis_soft_max: _Optional[float] = ...,
    ) -> None: ...

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

class DashboardTreeMapViz(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DashboardPieViz(_message.Message):
    __slots__ = ("hide_legend", "hide_labels")
    HIDE_LEGEND_FIELD_NUMBER: _ClassVar[int]
    HIDE_LABELS_FIELD_NUMBER: _ClassVar[int]
    hide_legend: bool
    hide_labels: bool
    def __init__(self, hide_legend: bool = ..., hide_labels: bool = ...) -> None: ...

class DashboardStatisticViz(_message.Message):
    __slots__ = ("compare_to_previous", "number_format", "unit_label", "rate_options", "coloring")
    COMPARE_TO_PREVIOUS_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FORMAT_FIELD_NUMBER: _ClassVar[int]
    UNIT_LABEL_FIELD_NUMBER: _ClassVar[int]
    RATE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    COLORING_FIELD_NUMBER: _ClassVar[int]
    compare_to_previous: bool
    number_format: str
    unit_label: str
    rate_options: _aggregation_pb2.RateOptions
    coloring: ValueColoring
    def __init__(
        self,
        compare_to_previous: bool = ...,
        number_format: _Optional[str] = ...,
        unit_label: _Optional[str] = ...,
        rate_options: _Optional[_Union[_aggregation_pb2.RateOptions, _Mapping]] = ...,
        coloring: _Optional[_Union[ValueColoring, _Mapping]] = ...,
    ) -> None: ...

class ValueColorRule(_message.Message):
    __slots__ = ("comparison", "value", "tone")
    COMPARISON_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    TONE_FIELD_NUMBER: _ClassVar[int]
    comparison: _chart_pb2.ThresholdKind
    value: float
    tone: _value_tone_pb2.ValueTone
    def __init__(
        self,
        comparison: _Optional[_Union[_chart_pb2.ThresholdKind, str]] = ...,
        value: _Optional[float] = ...,
        tone: _Optional[_Union[_value_tone_pb2.ValueTone, str]] = ...,
    ) -> None: ...

class ValueColoring(_message.Message):
    __slots__ = ("rules", "default_tone")
    RULES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_TONE_FIELD_NUMBER: _ClassVar[int]
    rules: _containers.RepeatedCompositeFieldContainer[ValueColorRule]
    default_tone: _value_tone_pb2.ValueTone
    def __init__(
        self,
        rules: _Optional[_Iterable[_Union[ValueColorRule, _Mapping]]] = ...,
        default_tone: _Optional[_Union[_value_tone_pb2.ValueTone, str]] = ...,
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
