from chalk._gen.chalk.artifacts.v1 import chart_pb2 as _chart_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
from chalk._gen.chalk.server.v1 import incident_pb2 as _incident_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
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

class ChartMetricsBackend(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHART_METRICS_BACKEND_UNSPECIFIED: _ClassVar[ChartMetricsBackend]
    CHART_METRICS_BACKEND_TIMESCALE: _ClassVar[ChartMetricsBackend]
    CHART_METRICS_BACKEND_VICTORIA_METRICS: _ClassVar[ChartMetricsBackend]
    CHART_METRICS_BACKEND_VICTORIA_METRICS_STRICT: _ClassVar[ChartMetricsBackend]

class MetricKindGroup(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_KIND_GROUP_UNSPECIFIED: _ClassVar[MetricKindGroup]
    METRIC_KIND_GROUP_FEATURES: _ClassVar[MetricKindGroup]
    METRIC_KIND_GROUP_RESOLVERS: _ClassVar[MetricKindGroup]
    METRIC_KIND_GROUP_QUERIES: _ClassVar[MetricKindGroup]
    METRIC_KIND_GROUP_STREAMING: _ClassVar[MetricKindGroup]
    METRIC_KIND_GROUP_CRONS: _ClassVar[MetricKindGroup]
    METRIC_KIND_GROUP_ONLINE_STORE: _ClassVar[MetricKindGroup]
    METRIC_KIND_GROUP_GPU: _ClassVar[MetricKindGroup]
    METRIC_KIND_GROUP_BILLING: _ClassVar[MetricKindGroup]
    METRIC_KIND_GROUP_INFRASTRUCTURE: _ClassVar[MetricKindGroup]

class MetricFormulaOperandKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_FORMULA_OPERAND_KIND_UNSPECIFIED: _ClassVar[MetricFormulaOperandKind]
    METRIC_FORMULA_OPERAND_KIND_SERIES: _ClassVar[MetricFormulaOperandKind]
    METRIC_FORMULA_OPERAND_KIND_DATASET: _ClassVar[MetricFormulaOperandKind]
    METRIC_FORMULA_OPERAND_KIND_FEATURE: _ClassVar[MetricFormulaOperandKind]

class MetricHealthStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_HEALTH_STATUS_UNSPECIFIED: _ClassVar[MetricHealthStatus]
    METRIC_HEALTH_STATUS_HEALTHY: _ClassVar[MetricHealthStatus]
    METRIC_HEALTH_STATUS_UNHEALTHY: _ClassVar[MetricHealthStatus]
    METRIC_HEALTH_STATUS_NO_CHECKS: _ClassVar[MetricHealthStatus]

CHART_METRICS_BACKEND_UNSPECIFIED: ChartMetricsBackend
CHART_METRICS_BACKEND_TIMESCALE: ChartMetricsBackend
CHART_METRICS_BACKEND_VICTORIA_METRICS: ChartMetricsBackend
CHART_METRICS_BACKEND_VICTORIA_METRICS_STRICT: ChartMetricsBackend
METRIC_KIND_GROUP_UNSPECIFIED: MetricKindGroup
METRIC_KIND_GROUP_FEATURES: MetricKindGroup
METRIC_KIND_GROUP_RESOLVERS: MetricKindGroup
METRIC_KIND_GROUP_QUERIES: MetricKindGroup
METRIC_KIND_GROUP_STREAMING: MetricKindGroup
METRIC_KIND_GROUP_CRONS: MetricKindGroup
METRIC_KIND_GROUP_ONLINE_STORE: MetricKindGroup
METRIC_KIND_GROUP_GPU: MetricKindGroup
METRIC_KIND_GROUP_BILLING: MetricKindGroup
METRIC_KIND_GROUP_INFRASTRUCTURE: MetricKindGroup
METRIC_FORMULA_OPERAND_KIND_UNSPECIFIED: MetricFormulaOperandKind
METRIC_FORMULA_OPERAND_KIND_SERIES: MetricFormulaOperandKind
METRIC_FORMULA_OPERAND_KIND_DATASET: MetricFormulaOperandKind
METRIC_FORMULA_OPERAND_KIND_FEATURE: MetricFormulaOperandKind
METRIC_HEALTH_STATUS_UNSPECIFIED: MetricHealthStatus
METRIC_HEALTH_STATUS_HEALTHY: MetricHealthStatus
METRIC_HEALTH_STATUS_UNHEALTHY: MetricHealthStatus
METRIC_HEALTH_STATUS_NO_CHECKS: MetricHealthStatus

class Series(_message.Message):
    __slots__ = ("points", "label", "units")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedScalarFieldContainer[float]
    label: str
    units: str
    def __init__(
        self, points: _Optional[_Iterable[float]] = ..., label: _Optional[str] = ..., units: _Optional[str] = ...
    ) -> None: ...

class Chart(_message.Message):
    __slots__ = ("title", "series", "x_timestamp_ms")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    X_TIMESTAMP_MS_FIELD_NUMBER: _ClassVar[int]
    title: str
    series: _containers.RepeatedCompositeFieldContainer[Series]
    x_timestamp_ms: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        title: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[Series, _Mapping]]] = ...,
        x_timestamp_ms: _Optional[_Iterable[int]] = ...,
    ) -> None: ...

class Point(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: int
    def __init__(self, value: _Optional[int] = ...) -> None: ...

class TimeSeries(_message.Message):
    __slots__ = ("points", "label", "units")
    POINTS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    points: _containers.RepeatedCompositeFieldContainer[Point]
    label: str
    units: str
    def __init__(
        self,
        points: _Optional[_Iterable[_Union[Point, _Mapping]]] = ...,
        label: _Optional[str] = ...,
        units: _Optional[str] = ...,
    ) -> None: ...

class TimeSeriesChart(_message.Message):
    __slots__ = ("title", "series", "x_series", "window_period")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    X_SERIES_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    title: str
    series: _containers.RepeatedCompositeFieldContainer[TimeSeries]
    x_series: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    window_period: _duration_pb2.Duration
    def __init__(
        self,
        title: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[TimeSeries, _Mapping]]] = ...,
        x_series: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class ListChartsFilters(_message.Message):
    __slots__ = ("link_entity_kind", "linked_entity_id", "linked_entity_id_search")
    LINK_ENTITY_KIND_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_ID_SEARCH_FIELD_NUMBER: _ClassVar[int]
    link_entity_kind: _chart_pb2.ChartLinkKind
    linked_entity_id: str
    linked_entity_id_search: str
    def __init__(
        self,
        link_entity_kind: _Optional[_Union[_chart_pb2.ChartLinkKind, str]] = ...,
        linked_entity_id: _Optional[str] = ...,
        linked_entity_id_search: _Optional[str] = ...,
    ) -> None: ...

class ListChartPageToken(_message.Message):
    __slots__ = ("created_at_hwm", "id_hwm")
    CREATED_AT_HWM_FIELD_NUMBER: _ClassVar[int]
    ID_HWM_FIELD_NUMBER: _ClassVar[int]
    created_at_hwm: _timestamp_pb2.Timestamp
    id_hwm: str
    def __init__(
        self, created_at_hwm: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., id_hwm: _Optional[str] = ...
    ) -> None: ...

class ListChartsRequest(_message.Message):
    __slots__ = ("filters", "limit", "page_token")
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    filters: ListChartsFilters
    limit: int
    page_token: str
    def __init__(
        self,
        filters: _Optional[_Union[ListChartsFilters, _Mapping]] = ...,
        limit: _Optional[int] = ...,
        page_token: _Optional[str] = ...,
    ) -> None: ...

class ListChartsResponse(_message.Message):
    __slots__ = ("charts", "charts_with_links", "next_page_token")
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    CHARTS_WITH_LINKS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[_chart_pb2.MetricConfig]
    charts_with_links: _containers.RepeatedCompositeFieldContainer[_chart_pb2.Chart]
    next_page_token: str
    def __init__(
        self,
        charts: _Optional[_Iterable[_Union[_chart_pb2.MetricConfig, _Mapping]]] = ...,
        charts_with_links: _Optional[_Iterable[_Union[_chart_pb2.Chart, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...

class ListChartsWithCronAlertsRequest(_message.Message):
    __slots__ = ("limit", "page_token")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    limit: int
    page_token: str
    def __init__(self, limit: _Optional[int] = ..., page_token: _Optional[str] = ...) -> None: ...

class ListChartsWithCronAlertsResponse(_message.Message):
    __slots__ = ("charts", "next_page_token")
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[_chart_pb2.Chart]
    next_page_token: str
    def __init__(
        self,
        charts: _Optional[_Iterable[_Union[_chart_pb2.Chart, _Mapping]]] = ...,
        next_page_token: _Optional[str] = ...,
    ) -> None: ...

class UpdateMetricConfigOperation(_message.Message):
    __slots__ = ("name", "window_period", "series", "formulas", "trigger", "graph_generated", "display_window_period")
    NAME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    FORMULAS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    GRAPH_GENERATED_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    name: str
    window_period: str
    series: _containers.RepeatedCompositeFieldContainer[_chart_pb2.MetricConfigSeries]
    formulas: _containers.RepeatedCompositeFieldContainer[_chart_pb2.MetricFormula]
    trigger: _chart_pb2.AlertTrigger
    graph_generated: bool
    display_window_period: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        window_period: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[_chart_pb2.MetricConfigSeries, _Mapping]]] = ...,
        formulas: _Optional[_Iterable[_Union[_chart_pb2.MetricFormula, _Mapping]]] = ...,
        trigger: _Optional[_Union[_chart_pb2.AlertTrigger, _Mapping]] = ...,
        graph_generated: bool = ...,
        display_window_period: _Optional[str] = ...,
    ) -> None: ...

class CreateChartRequest(_message.Message):
    __slots__ = (
        "name",
        "window_period",
        "series",
        "formulas",
        "trigger",
        "link_entity_kind",
        "linked_entity_id",
        "graph_generated",
        "display_window_period",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    FORMULAS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    LINK_ENTITY_KIND_FIELD_NUMBER: _ClassVar[int]
    LINKED_ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    GRAPH_GENERATED_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    name: str
    window_period: str
    series: _containers.RepeatedCompositeFieldContainer[_chart_pb2.MetricConfigSeries]
    formulas: _containers.RepeatedCompositeFieldContainer[_chart_pb2.MetricFormula]
    trigger: _chart_pb2.AlertTrigger
    link_entity_kind: _chart_pb2.ChartLinkKind
    linked_entity_id: str
    graph_generated: bool
    display_window_period: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        window_period: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[_chart_pb2.MetricConfigSeries, _Mapping]]] = ...,
        formulas: _Optional[_Iterable[_Union[_chart_pb2.MetricFormula, _Mapping]]] = ...,
        trigger: _Optional[_Union[_chart_pb2.AlertTrigger, _Mapping]] = ...,
        link_entity_kind: _Optional[_Union[_chart_pb2.ChartLinkKind, str]] = ...,
        linked_entity_id: _Optional[str] = ...,
        graph_generated: bool = ...,
        display_window_period: _Optional[str] = ...,
    ) -> None: ...

class CreateChartResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _chart_pb2.Chart
    def __init__(self, chart: _Optional[_Union[_chart_pb2.Chart, _Mapping]] = ...) -> None: ...

class UpdateMetricConfigRequest(_message.Message):
    __slots__ = ("metric_config_id", "update", "update_mask")
    METRIC_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    metric_config_id: str
    update: UpdateMetricConfigOperation
    update_mask: _field_mask_pb2.FieldMask
    def __init__(
        self,
        metric_config_id: _Optional[str] = ...,
        update: _Optional[_Union[UpdateMetricConfigOperation, _Mapping]] = ...,
        update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...,
    ) -> None: ...

class UpdateMetricConfigResponse(_message.Message):
    __slots__ = ("metric_config",)
    METRIC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    metric_config: _chart_pb2.MetricConfig
    def __init__(self, metric_config: _Optional[_Union[_chart_pb2.MetricConfig, _Mapping]] = ...) -> None: ...

class GetChartSnapshotRequest(_message.Message):
    __slots__ = (
        "metric_config",
        "start_time",
        "end_time",
        "use_start_as_origin",
        "use_sketch_metrics_table",
        "return_sql_query_string",
        "exclude_incomplete_last_bucket",
        "metrics_backend",
    )
    METRIC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    USE_START_AS_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    USE_SKETCH_METRICS_TABLE_FIELD_NUMBER: _ClassVar[int]
    RETURN_SQL_QUERY_STRING_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_INCOMPLETE_LAST_BUCKET_FIELD_NUMBER: _ClassVar[int]
    METRICS_BACKEND_FIELD_NUMBER: _ClassVar[int]
    metric_config: _chart_pb2.MetricConfig
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    use_start_as_origin: bool
    use_sketch_metrics_table: bool
    return_sql_query_string: bool
    exclude_incomplete_last_bucket: bool
    metrics_backend: ChartMetricsBackend
    def __init__(
        self,
        metric_config: _Optional[_Union[_chart_pb2.MetricConfig, _Mapping]] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        use_start_as_origin: bool = ...,
        use_sketch_metrics_table: bool = ...,
        return_sql_query_string: bool = ...,
        exclude_incomplete_last_bucket: bool = ...,
        metrics_backend: _Optional[_Union[ChartMetricsBackend, str]] = ...,
    ) -> None: ...

class GetChartSnapshotResponse(_message.Message):
    __slots__ = ("charts", "x_series", "window_period", "sql_query_strings", "metrics_backend")
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    X_SERIES_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SQL_QUERY_STRINGS_FIELD_NUMBER: _ClassVar[int]
    METRICS_BACKEND_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[_densetimeserieschart_pb2.DenseTimeSeriesChart]
    x_series: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    window_period: _duration_pb2.Duration
    sql_query_strings: _containers.RepeatedScalarFieldContainer[str]
    metrics_backend: ChartMetricsBackend
    def __init__(
        self,
        charts: _Optional[_Iterable[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]]] = ...,
        x_series: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        sql_query_strings: _Optional[_Iterable[str]] = ...,
        metrics_backend: _Optional[_Union[ChartMetricsBackend, str]] = ...,
    ) -> None: ...

class GetChartSnapshotByQueryRequest(_message.Message):
    __slots__ = (
        "query",
        "start_time",
        "end_time",
        "use_start_as_origin",
        "use_sketch_metrics_table",
        "return_sql_query_string",
        "exclude_incomplete_last_bucket",
        "metrics_backend",
    )
    QUERY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    USE_START_AS_ORIGIN_FIELD_NUMBER: _ClassVar[int]
    USE_SKETCH_METRICS_TABLE_FIELD_NUMBER: _ClassVar[int]
    RETURN_SQL_QUERY_STRING_FIELD_NUMBER: _ClassVar[int]
    EXCLUDE_INCOMPLETE_LAST_BUCKET_FIELD_NUMBER: _ClassVar[int]
    METRICS_BACKEND_FIELD_NUMBER: _ClassVar[int]
    query: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    use_start_as_origin: bool
    use_sketch_metrics_table: bool
    return_sql_query_string: bool
    exclude_incomplete_last_bucket: bool
    metrics_backend: ChartMetricsBackend
    def __init__(
        self,
        query: _Optional[str] = ...,
        start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        use_start_as_origin: bool = ...,
        use_sketch_metrics_table: bool = ...,
        return_sql_query_string: bool = ...,
        exclude_incomplete_last_bucket: bool = ...,
        metrics_backend: _Optional[_Union[ChartMetricsBackend, str]] = ...,
    ) -> None: ...

class GetChartSnapshotByQueryResponse(_message.Message):
    __slots__ = ("charts", "x_series", "window_period", "sql_query_strings", "compiled_metric_config")
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    X_SERIES_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SQL_QUERY_STRINGS_FIELD_NUMBER: _ClassVar[int]
    COMPILED_METRIC_CONFIG_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[_densetimeserieschart_pb2.DenseTimeSeriesChart]
    x_series: _containers.RepeatedCompositeFieldContainer[_timestamp_pb2.Timestamp]
    window_period: _duration_pb2.Duration
    sql_query_strings: _containers.RepeatedScalarFieldContainer[str]
    compiled_metric_config: _chart_pb2.MetricConfig
    def __init__(
        self,
        charts: _Optional[_Iterable[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]]] = ...,
        x_series: _Optional[_Iterable[_Union[_timestamp_pb2.Timestamp, _Mapping]]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        sql_query_strings: _Optional[_Iterable[str]] = ...,
        compiled_metric_config: _Optional[_Union[_chart_pb2.MetricConfig, _Mapping]] = ...,
    ) -> None: ...

class DeleteChartRequest(_message.Message):
    __slots__ = ("metric_config_id",)
    METRIC_CONFIG_ID_FIELD_NUMBER: _ClassVar[int]
    metric_config_id: str
    def __init__(self, metric_config_id: _Optional[str] = ...) -> None: ...

class DeleteChartResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetChartRequest(_message.Message):
    __slots__ = ("chart_id",)
    CHART_ID_FIELD_NUMBER: _ClassVar[int]
    chart_id: str
    def __init__(self, chart_id: _Optional[str] = ...) -> None: ...

class GetChartResponse(_message.Message):
    __slots__ = ("chart", "active_incidents")
    CHART_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_INCIDENTS_FIELD_NUMBER: _ClassVar[int]
    chart: _chart_pb2.Chart
    active_incidents: _containers.RepeatedCompositeFieldContainer[_incident_pb2.MetricIncident]
    def __init__(
        self,
        chart: _Optional[_Union[_chart_pb2.Chart, _Mapping]] = ...,
        active_incidents: _Optional[_Iterable[_Union[_incident_pb2.MetricIncident, _Mapping]]] = ...,
    ) -> None: ...

class GetChartOptionsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FilterOptionNamespace(_message.Message):
    __slots__ = ("namespace", "values")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, namespace: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...

class FilterOption(_message.Message):
    __slots__ = ("display_name", "kind", "namespaced_values")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAMESPACED_VALUES_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    kind: _chart_pb2.FilterKind
    namespaced_values: _containers.RepeatedCompositeFieldContainer[FilterOptionNamespace]
    def __init__(
        self,
        display_name: _Optional[str] = ...,
        kind: _Optional[_Union[_chart_pb2.FilterKind, str]] = ...,
        namespaced_values: _Optional[_Iterable[_Union[FilterOptionNamespace, _Mapping]]] = ...,
    ) -> None: ...

class GroupOption(_message.Message):
    __slots__ = ("display_name", "kind")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    kind: _chart_pb2.GroupByKind
    def __init__(
        self, display_name: _Optional[str] = ..., kind: _Optional[_Union[_chart_pb2.GroupByKind, str]] = ...
    ) -> None: ...

class WindowFunctionOption(_message.Message):
    __slots__ = ("display_name", "window_function")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    window_function: _chart_pb2.WindowFunctionKind
    def __init__(
        self,
        display_name: _Optional[str] = ...,
        window_function: _Optional[_Union[_chart_pb2.WindowFunctionKind, str]] = ...,
    ) -> None: ...

class MetricOptions(_message.Message):
    __slots__ = ("kind", "filters", "groups", "window_functions", "metric_kind_group")
    KIND_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    METRIC_KIND_GROUP_FIELD_NUMBER: _ClassVar[int]
    kind: _chart_pb2.MetricKind
    filters: _containers.RepeatedCompositeFieldContainer[FilterOption]
    groups: _containers.RepeatedCompositeFieldContainer[GroupOption]
    window_functions: _containers.RepeatedCompositeFieldContainer[WindowFunctionOption]
    metric_kind_group: MetricKindGroup
    def __init__(
        self,
        kind: _Optional[_Union[_chart_pb2.MetricKind, str]] = ...,
        filters: _Optional[_Iterable[_Union[FilterOption, _Mapping]]] = ...,
        groups: _Optional[_Iterable[_Union[GroupOption, _Mapping]]] = ...,
        window_functions: _Optional[_Iterable[_Union[WindowFunctionOption, _Mapping]]] = ...,
        metric_kind_group: _Optional[_Union[MetricKindGroup, str]] = ...,
    ) -> None: ...

class MetricFormulaFeatureOperandInput(_message.Message):
    __slots__ = ("namespace", "feature_fqns")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FQNS_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    feature_fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, namespace: _Optional[str] = ..., feature_fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class MetricFormulaFeatureOperandList(_message.Message):
    __slots__ = ("namespace", "values", "features")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    values: _containers.RepeatedScalarFieldContainer[str]
    features: _containers.RepeatedCompositeFieldContainer[MetricFormulaFeatureOperandInput]
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        values: _Optional[_Iterable[str]] = ...,
        features: _Optional[_Iterable[_Union[MetricFormulaFeatureOperandInput, _Mapping]]] = ...,
    ) -> None: ...

class MetricFormulaDatasetOperandInput(_message.Message):
    __slots__ = ("id", "name", "output_fqns")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FQNS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    output_fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, id: _Optional[str] = ..., name: _Optional[str] = ..., output_fqns: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class MetricFormulaDatasetOperandList(_message.Message):
    __slots__ = ("values", "datasets")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    datasets: _containers.RepeatedCompositeFieldContainer[MetricFormulaDatasetOperandInput]
    def __init__(
        self,
        values: _Optional[_Iterable[str]] = ...,
        datasets: _Optional[_Iterable[_Union[MetricFormulaDatasetOperandInput, _Mapping]]] = ...,
    ) -> None: ...

class MetricFormulaOperand(_message.Message):
    __slots__ = ("kind", "dataset_operands", "feature_operands")
    KIND_FIELD_NUMBER: _ClassVar[int]
    DATASET_OPERANDS_FIELD_NUMBER: _ClassVar[int]
    FEATURE_OPERANDS_FIELD_NUMBER: _ClassVar[int]
    kind: MetricFormulaOperandKind
    dataset_operands: MetricFormulaDatasetOperandList
    feature_operands: MetricFormulaFeatureOperandList
    def __init__(
        self,
        kind: _Optional[_Union[MetricFormulaOperandKind, str]] = ...,
        dataset_operands: _Optional[_Union[MetricFormulaDatasetOperandList, _Mapping]] = ...,
        feature_operands: _Optional[_Union[MetricFormulaFeatureOperandList, _Mapping]] = ...,
    ) -> None: ...

class MetricFormulaOption(_message.Message):
    __slots__ = ("display_name", "kind", "operands")
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    OPERANDS_FIELD_NUMBER: _ClassVar[int]
    display_name: str
    kind: _chart_pb2.MetricFormulaKind
    operands: _containers.RepeatedCompositeFieldContainer[MetricFormulaOperand]
    def __init__(
        self,
        display_name: _Optional[str] = ...,
        kind: _Optional[_Union[_chart_pb2.MetricFormulaKind, str]] = ...,
        operands: _Optional[_Iterable[_Union[MetricFormulaOperand, _Mapping]]] = ...,
    ) -> None: ...

class GetChartOptionsResponse(_message.Message):
    __slots__ = ("metrics", "formulas")
    METRICS_FIELD_NUMBER: _ClassVar[int]
    FORMULAS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[MetricOptions]
    formulas: _containers.RepeatedCompositeFieldContainer[MetricFormulaOption]
    def __init__(
        self,
        metrics: _Optional[_Iterable[_Union[MetricOptions, _Mapping]]] = ...,
        formulas: _Optional[_Iterable[_Union[MetricFormulaOption, _Mapping]]] = ...,
    ) -> None: ...

class MetricHealthCheck(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: MetricHealthStatus
    message: str
    def __init__(
        self, status: _Optional[_Union[MetricHealthStatus, str]] = ..., message: _Optional[str] = ...
    ) -> None: ...

class SparkPoint(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class SparkSeries(_message.Message):
    __slots__ = ("name", "points")
    NAME_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    points: _containers.RepeatedCompositeFieldContainer[SparkPoint]
    def __init__(
        self, name: _Optional[str] = ..., points: _Optional[_Iterable[_Union[SparkPoint, _Mapping]]] = ...
    ) -> None: ...

class EntityMetrics(_message.Message):
    __slots__ = ("fqn", "successful_requests", "failed_requests", "health")
    FQN_FIELD_NUMBER: _ClassVar[int]
    SUCCESSFUL_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    FAILED_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    successful_requests: SparkSeries
    failed_requests: SparkSeries
    health: MetricHealthCheck
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        successful_requests: _Optional[_Union[SparkSeries, _Mapping]] = ...,
        failed_requests: _Optional[_Union[SparkSeries, _Mapping]] = ...,
        health: _Optional[_Union[MetricHealthCheck, _Mapping]] = ...,
    ) -> None: ...

class GetFeatureMetricsRequest(_message.Message):
    __slots__ = ("fqns",)
    FQNS_FIELD_NUMBER: _ClassVar[int]
    fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetFeatureMetricsResponse(_message.Message):
    __slots__ = ("metrics",)
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[EntityMetrics]
    def __init__(self, metrics: _Optional[_Iterable[_Union[EntityMetrics, _Mapping]]] = ...) -> None: ...

class GetResolverMetricsRequest(_message.Message):
    __slots__ = ("fqns",)
    FQNS_FIELD_NUMBER: _ClassVar[int]
    fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetResolverMetricsResponse(_message.Message):
    __slots__ = ("metrics",)
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[EntityMetrics]
    def __init__(self, metrics: _Optional[_Iterable[_Union[EntityMetrics, _Mapping]]] = ...) -> None: ...

class GetQueryMetricsRequest(_message.Message):
    __slots__ = ("fqns",)
    FQNS_FIELD_NUMBER: _ClassVar[int]
    fqns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fqns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetQueryMetricsResponse(_message.Message):
    __slots__ = ("metrics",)
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[EntityMetrics]
    def __init__(self, metrics: _Optional[_Iterable[_Union[EntityMetrics, _Mapping]]] = ...) -> None: ...

class GetMetricOptionsRequest(_message.Message):
    __slots__ = ("metric_kind",)
    METRIC_KIND_FIELD_NUMBER: _ClassVar[int]
    metric_kind: _chart_pb2.MetricKind
    def __init__(self, metric_kind: _Optional[_Union[_chart_pb2.MetricKind, str]] = ...) -> None: ...

class GetMetricOptionsResponse(_message.Message):
    __slots__ = ("metric_options",)
    METRIC_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    metric_options: MetricOptions
    def __init__(self, metric_options: _Optional[_Union[MetricOptions, _Mapping]] = ...) -> None: ...

class GetFormulaOptionsRequest(_message.Message):
    __slots__ = ("formula_kind",)
    FORMULA_KIND_FIELD_NUMBER: _ClassVar[int]
    formula_kind: _chart_pb2.MetricFormulaKind
    def __init__(self, formula_kind: _Optional[_Union[_chart_pb2.MetricFormulaKind, str]] = ...) -> None: ...

class GetFormulaOptionsResponse(_message.Message):
    __slots__ = ("formula_options",)
    FORMULA_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    formula_options: MetricFormulaOption
    def __init__(self, formula_options: _Optional[_Union[MetricFormulaOption, _Mapping]] = ...) -> None: ...
