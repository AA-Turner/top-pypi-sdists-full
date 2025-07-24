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

class MetricKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_KIND_UNSPECIFIED: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_REQUEST_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_STALENESS: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_VALUE: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_WRITE: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_NULL_RATIO: _ClassVar[MetricKind]
    METRIC_KIND_RESOLVER_REQUEST_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_RESOLVER_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_RESOLVER_SUCCESS_RATIO: _ClassVar[MetricKind]
    METRIC_KIND_QUERY_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_QUERY_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_QUERY_SUCCESS_RATIO: _ClassVar[MetricKind]
    METRIC_KIND_BILLING_INFERENCE: _ClassVar[MetricKind]
    METRIC_KIND_BILLING_CRON: _ClassVar[MetricKind]
    METRIC_KIND_BILLING_MIGRATION: _ClassVar[MetricKind]
    METRIC_KIND_CRON_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_CRON_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_STREAM_MESSAGES_PROCESSED: _ClassVar[MetricKind]
    METRIC_KIND_STREAM_MESSAGE_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_STREAM_WINDOWS_PROCESSED: _ClassVar[MetricKind]
    METRIC_KIND_STREAM_WINDOW_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_ONLINE_STORE_KEY_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_ONLINE_STORE_EXPIRED_KEY_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_ONLINE_STORE_REQUESTS_PER_SECOND: _ClassVar[MetricKind]
    METRIC_KIND_CPU_UTILIZATION_PERCENT: _ClassVar[MetricKind]
    METRIC_KIND_REPLICA_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_ONLINE_STORE_USED_MEMORY: _ClassVar[MetricKind]
    METRIC_KIND_ONLINE_STORE_TOTAL_MEMORY: _ClassVar[MetricKind]
    METRIC_KIND_MEMORY_USAGE_BYTES: _ClassVar[MetricKind]
    METRIC_KIND_TOTAL_MEMORY_AVAILABLE_BYTES: _ClassVar[MetricKind]
    METRIC_KIND_NETWORK_READ_BYTES: _ClassVar[MetricKind]
    METRIC_KIND_NETWORK_WRITE_BYTES: _ClassVar[MetricKind]
    METRIC_KIND_DISK_READ_BYTES: _ClassVar[MetricKind]
    METRIC_KIND_DISK_WRITE_BYTES: _ClassVar[MetricKind]
    METRIC_KIND_STREAM_LAG: _ClassVar[MetricKind]
    METRIC_KIND_USAGE: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_COMPUTED_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_LOOKED_UP_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_INTERMEDIATE_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_COMPUTED_NULL_RATIO: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_LOOKED_UP_NULL_RATIO: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_INTERMEDIATE_NULL_RATIO: _ClassVar[MetricKind]

class FilterKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FILTER_KIND_UNSPECIFIED: _ClassVar[FilterKind]
    FILTER_KIND_FEATURE_STATUS: _ClassVar[FilterKind]
    FILTER_KIND_FEATURE_NAME: _ClassVar[FilterKind]
    FILTER_KIND_FEATURE_TAG: _ClassVar[FilterKind]
    FILTER_KIND_RESOLVER_STATUS: _ClassVar[FilterKind]
    FILTER_KIND_RESOLVER_NAME: _ClassVar[FilterKind]
    FILTER_KIND_RESOLVER_TAG: _ClassVar[FilterKind]
    FILTER_KIND_CRON_STATUS: _ClassVar[FilterKind]
    FILTER_KIND_MIGRATION_STATUS: _ClassVar[FilterKind]
    FILTER_KIND_ONLINE_OFFLINE: _ClassVar[FilterKind]
    FILTER_KIND_CACHE_HIT: _ClassVar[FilterKind]
    FILTER_KIND_OPERATION_ID: _ClassVar[FilterKind]
    FILTER_KIND_QUERY_NAME: _ClassVar[FilterKind]
    FILTER_KIND_QUERY_STATUS: _ClassVar[FilterKind]
    FILTER_KIND_IS_NULL: _ClassVar[FilterKind]
    FILTER_KIND_USAGE_KIND: _ClassVar[FilterKind]
    FILTER_KIND_RESOURCE_GROUP: _ClassVar[FilterKind]
    FILTER_KIND_POD_NAME: _ClassVar[FilterKind]

class ComparatorKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COMPARATOR_KIND_UNSPECIFIED: _ClassVar[ComparatorKind]
    COMPARATOR_KIND_EQ: _ClassVar[ComparatorKind]
    COMPARATOR_KIND_NEQ: _ClassVar[ComparatorKind]
    COMPARATOR_KIND_ONE_OF: _ClassVar[ComparatorKind]

class WindowFunctionKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WINDOW_FUNCTION_KIND_UNSPECIFIED: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_COUNT: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_MEAN: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_SUM: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_MIN: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_MAX: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_99: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_95: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_75: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_50: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_25: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_5: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_ALL_PERCENTILES: _ClassVar[WindowFunctionKind]

class GroupByKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GROUP_BY_KIND_UNSPECIFIED: _ClassVar[GroupByKind]
    GROUP_BY_KIND_FEATURE_STATUS: _ClassVar[GroupByKind]
    GROUP_BY_KIND_FEATURE_NAME: _ClassVar[GroupByKind]
    GROUP_BY_KIND_IS_NULL: _ClassVar[GroupByKind]
    GROUP_BY_KIND_RESOLVER_STATUS: _ClassVar[GroupByKind]
    GROUP_BY_KIND_RESOLVER_NAME: _ClassVar[GroupByKind]
    GROUP_BY_KIND_QUERY_STATUS: _ClassVar[GroupByKind]
    GROUP_BY_KIND_QUERY_NAME: _ClassVar[GroupByKind]
    GROUP_BY_KIND_ONLINE_OFFLINE: _ClassVar[GroupByKind]
    GROUP_BY_KIND_CACHE_HIT: _ClassVar[GroupByKind]
    GROUP_BY_KIND_USAGE_KIND: _ClassVar[GroupByKind]
    GROUP_BY_KIND_RESOURCE_GROUP: _ClassVar[GroupByKind]
    GROUP_BY_KIND_DEPLOYMENT_ID: _ClassVar[GroupByKind]
    GROUP_BY_KIND_OPERATION_ID: _ClassVar[GroupByKind]
    GROUP_BY_KIND_POD_NAME: _ClassVar[GroupByKind]

class MetricFormulaKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METRIC_FORMULA_KIND_UNSPECIFIED: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_SUM: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_TOTAL_RATIO: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_RATIO: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_PRODUCT: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_ABS: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_KS_STAT: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_KS_TEST: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_KS_THRESHOLD: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_TIME_OFFSET: _ClassVar[MetricFormulaKind]

class AlertSeverityKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALERT_SEVERITY_KIND_UNSPECIFIED: _ClassVar[AlertSeverityKind]
    ALERT_SEVERITY_KIND_CRITICAL: _ClassVar[AlertSeverityKind]
    ALERT_SEVERITY_KIND_ERROR: _ClassVar[AlertSeverityKind]
    ALERT_SEVERITY_KIND_WARNING: _ClassVar[AlertSeverityKind]
    ALERT_SEVERITY_KIND_INFO: _ClassVar[AlertSeverityKind]
    ALERT_SEVERITY_KIND_RESOLVED: _ClassVar[AlertSeverityKind]

class ThresholdKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    THRESHOLD_KIND_UNSPECIFIED: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_ABOVE: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_BELOW: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_GREATER_EQUAL: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_LESS_EQUAL: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_EQUAL: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_NOT_EQUAL: _ClassVar[ThresholdKind]

class ChartLinkKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHART_LINK_KIND_UNSPECIFIED: _ClassVar[ChartLinkKind]
    CHART_LINK_KIND_RESOLVER: _ClassVar[ChartLinkKind]
    CHART_LINK_KIND_FEATURE: _ClassVar[ChartLinkKind]
    CHART_LINK_KIND_QUERY: _ClassVar[ChartLinkKind]
    CHART_LINK_KIND_MANUAL: _ClassVar[ChartLinkKind]
    CHART_LINK_KIND_SCHEDULED_QUERY: _ClassVar[ChartLinkKind]

METRIC_KIND_UNSPECIFIED: MetricKind
METRIC_KIND_FEATURE_REQUEST_COUNT: MetricKind
METRIC_KIND_FEATURE_LATENCY: MetricKind
METRIC_KIND_FEATURE_STALENESS: MetricKind
METRIC_KIND_FEATURE_VALUE: MetricKind
METRIC_KIND_FEATURE_WRITE: MetricKind
METRIC_KIND_FEATURE_NULL_RATIO: MetricKind
METRIC_KIND_RESOLVER_REQUEST_COUNT: MetricKind
METRIC_KIND_RESOLVER_LATENCY: MetricKind
METRIC_KIND_RESOLVER_SUCCESS_RATIO: MetricKind
METRIC_KIND_QUERY_COUNT: MetricKind
METRIC_KIND_QUERY_LATENCY: MetricKind
METRIC_KIND_QUERY_SUCCESS_RATIO: MetricKind
METRIC_KIND_BILLING_INFERENCE: MetricKind
METRIC_KIND_BILLING_CRON: MetricKind
METRIC_KIND_BILLING_MIGRATION: MetricKind
METRIC_KIND_CRON_COUNT: MetricKind
METRIC_KIND_CRON_LATENCY: MetricKind
METRIC_KIND_STREAM_MESSAGES_PROCESSED: MetricKind
METRIC_KIND_STREAM_MESSAGE_LATENCY: MetricKind
METRIC_KIND_STREAM_WINDOWS_PROCESSED: MetricKind
METRIC_KIND_STREAM_WINDOW_LATENCY: MetricKind
METRIC_KIND_ONLINE_STORE_KEY_COUNT: MetricKind
METRIC_KIND_ONLINE_STORE_EXPIRED_KEY_COUNT: MetricKind
METRIC_KIND_ONLINE_STORE_REQUESTS_PER_SECOND: MetricKind
METRIC_KIND_CPU_UTILIZATION_PERCENT: MetricKind
METRIC_KIND_REPLICA_COUNT: MetricKind
METRIC_KIND_ONLINE_STORE_USED_MEMORY: MetricKind
METRIC_KIND_ONLINE_STORE_TOTAL_MEMORY: MetricKind
METRIC_KIND_MEMORY_USAGE_BYTES: MetricKind
METRIC_KIND_TOTAL_MEMORY_AVAILABLE_BYTES: MetricKind
METRIC_KIND_NETWORK_READ_BYTES: MetricKind
METRIC_KIND_NETWORK_WRITE_BYTES: MetricKind
METRIC_KIND_DISK_READ_BYTES: MetricKind
METRIC_KIND_DISK_WRITE_BYTES: MetricKind
METRIC_KIND_STREAM_LAG: MetricKind
METRIC_KIND_USAGE: MetricKind
METRIC_KIND_FEATURE_COMPUTED_COUNT: MetricKind
METRIC_KIND_FEATURE_LOOKED_UP_COUNT: MetricKind
METRIC_KIND_FEATURE_INTERMEDIATE_COUNT: MetricKind
METRIC_KIND_FEATURE_COMPUTED_NULL_RATIO: MetricKind
METRIC_KIND_FEATURE_LOOKED_UP_NULL_RATIO: MetricKind
METRIC_KIND_FEATURE_INTERMEDIATE_NULL_RATIO: MetricKind
FILTER_KIND_UNSPECIFIED: FilterKind
FILTER_KIND_FEATURE_STATUS: FilterKind
FILTER_KIND_FEATURE_NAME: FilterKind
FILTER_KIND_FEATURE_TAG: FilterKind
FILTER_KIND_RESOLVER_STATUS: FilterKind
FILTER_KIND_RESOLVER_NAME: FilterKind
FILTER_KIND_RESOLVER_TAG: FilterKind
FILTER_KIND_CRON_STATUS: FilterKind
FILTER_KIND_MIGRATION_STATUS: FilterKind
FILTER_KIND_ONLINE_OFFLINE: FilterKind
FILTER_KIND_CACHE_HIT: FilterKind
FILTER_KIND_OPERATION_ID: FilterKind
FILTER_KIND_QUERY_NAME: FilterKind
FILTER_KIND_QUERY_STATUS: FilterKind
FILTER_KIND_IS_NULL: FilterKind
FILTER_KIND_USAGE_KIND: FilterKind
FILTER_KIND_RESOURCE_GROUP: FilterKind
FILTER_KIND_POD_NAME: FilterKind
COMPARATOR_KIND_UNSPECIFIED: ComparatorKind
COMPARATOR_KIND_EQ: ComparatorKind
COMPARATOR_KIND_NEQ: ComparatorKind
COMPARATOR_KIND_ONE_OF: ComparatorKind
WINDOW_FUNCTION_KIND_UNSPECIFIED: WindowFunctionKind
WINDOW_FUNCTION_KIND_COUNT: WindowFunctionKind
WINDOW_FUNCTION_KIND_MEAN: WindowFunctionKind
WINDOW_FUNCTION_KIND_SUM: WindowFunctionKind
WINDOW_FUNCTION_KIND_MIN: WindowFunctionKind
WINDOW_FUNCTION_KIND_MAX: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_99: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_95: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_75: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_50: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_25: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_5: WindowFunctionKind
WINDOW_FUNCTION_KIND_ALL_PERCENTILES: WindowFunctionKind
GROUP_BY_KIND_UNSPECIFIED: GroupByKind
GROUP_BY_KIND_FEATURE_STATUS: GroupByKind
GROUP_BY_KIND_FEATURE_NAME: GroupByKind
GROUP_BY_KIND_IS_NULL: GroupByKind
GROUP_BY_KIND_RESOLVER_STATUS: GroupByKind
GROUP_BY_KIND_RESOLVER_NAME: GroupByKind
GROUP_BY_KIND_QUERY_STATUS: GroupByKind
GROUP_BY_KIND_QUERY_NAME: GroupByKind
GROUP_BY_KIND_ONLINE_OFFLINE: GroupByKind
GROUP_BY_KIND_CACHE_HIT: GroupByKind
GROUP_BY_KIND_USAGE_KIND: GroupByKind
GROUP_BY_KIND_RESOURCE_GROUP: GroupByKind
GROUP_BY_KIND_DEPLOYMENT_ID: GroupByKind
GROUP_BY_KIND_OPERATION_ID: GroupByKind
GROUP_BY_KIND_POD_NAME: GroupByKind
METRIC_FORMULA_KIND_UNSPECIFIED: MetricFormulaKind
METRIC_FORMULA_KIND_SUM: MetricFormulaKind
METRIC_FORMULA_KIND_TOTAL_RATIO: MetricFormulaKind
METRIC_FORMULA_KIND_RATIO: MetricFormulaKind
METRIC_FORMULA_KIND_PRODUCT: MetricFormulaKind
METRIC_FORMULA_KIND_ABS: MetricFormulaKind
METRIC_FORMULA_KIND_KS_STAT: MetricFormulaKind
METRIC_FORMULA_KIND_KS_TEST: MetricFormulaKind
METRIC_FORMULA_KIND_KS_THRESHOLD: MetricFormulaKind
METRIC_FORMULA_KIND_TIME_OFFSET: MetricFormulaKind
ALERT_SEVERITY_KIND_UNSPECIFIED: AlertSeverityKind
ALERT_SEVERITY_KIND_CRITICAL: AlertSeverityKind
ALERT_SEVERITY_KIND_ERROR: AlertSeverityKind
ALERT_SEVERITY_KIND_WARNING: AlertSeverityKind
ALERT_SEVERITY_KIND_INFO: AlertSeverityKind
ALERT_SEVERITY_KIND_RESOLVED: AlertSeverityKind
THRESHOLD_KIND_UNSPECIFIED: ThresholdKind
THRESHOLD_KIND_ABOVE: ThresholdKind
THRESHOLD_KIND_BELOW: ThresholdKind
THRESHOLD_KIND_GREATER_EQUAL: ThresholdKind
THRESHOLD_KIND_LESS_EQUAL: ThresholdKind
THRESHOLD_KIND_EQUAL: ThresholdKind
THRESHOLD_KIND_NOT_EQUAL: ThresholdKind
CHART_LINK_KIND_UNSPECIFIED: ChartLinkKind
CHART_LINK_KIND_RESOLVER: ChartLinkKind
CHART_LINK_KIND_FEATURE: ChartLinkKind
CHART_LINK_KIND_QUERY: ChartLinkKind
CHART_LINK_KIND_MANUAL: ChartLinkKind
CHART_LINK_KIND_SCHEDULED_QUERY: ChartLinkKind

class AlertTrigger(_message.Message):
    __slots__ = (
        "name",
        "severity",
        "threshold_position",
        "threshold_value",
        "series_name",
        "channel_name",
        "description",
    )
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_POSITION_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    SERIES_NAME_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    severity: AlertSeverityKind
    threshold_position: ThresholdKind
    threshold_value: float
    series_name: str
    channel_name: str
    description: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        severity: _Optional[_Union[AlertSeverityKind, str]] = ...,
        threshold_position: _Optional[_Union[ThresholdKind, str]] = ...,
        threshold_value: _Optional[float] = ...,
        series_name: _Optional[str] = ...,
        channel_name: _Optional[str] = ...,
        description: _Optional[str] = ...,
    ) -> None: ...

class DatasetFeatureOperand(_message.Message):
    __slots__ = ("dataset", "feature")
    DATASET_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    dataset: str
    feature: str
    def __init__(self, dataset: _Optional[str] = ..., feature: _Optional[str] = ...) -> None: ...

class MetricFormula(_message.Message):
    __slots__ = ("kind", "single_series_operands", "multi_series_operands", "dataset_feature_operands", "name")
    KIND_FIELD_NUMBER: _ClassVar[int]
    SINGLE_SERIES_OPERANDS_FIELD_NUMBER: _ClassVar[int]
    MULTI_SERIES_OPERANDS_FIELD_NUMBER: _ClassVar[int]
    DATASET_FEATURE_OPERANDS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    kind: MetricFormulaKind
    single_series_operands: int
    multi_series_operands: _containers.RepeatedScalarFieldContainer[int]
    dataset_feature_operands: DatasetFeatureOperand
    name: str
    def __init__(
        self,
        kind: _Optional[_Union[MetricFormulaKind, str]] = ...,
        single_series_operands: _Optional[int] = ...,
        multi_series_operands: _Optional[_Iterable[int]] = ...,
        dataset_feature_operands: _Optional[_Union[DatasetFeatureOperand, _Mapping]] = ...,
        name: _Optional[str] = ...,
    ) -> None: ...

class MetricFilter(_message.Message):
    __slots__ = ("kind", "comparator", "value")
    KIND_FIELD_NUMBER: _ClassVar[int]
    COMPARATOR_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    kind: FilterKind
    comparator: ComparatorKind
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        kind: _Optional[_Union[FilterKind, str]] = ...,
        comparator: _Optional[_Union[ComparatorKind, str]] = ...,
        value: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class MetricConfigSeries(_message.Message):
    __slots__ = ("metric", "filters", "name", "window_function", "group_by")
    METRIC_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    metric: MetricKind
    filters: _containers.RepeatedCompositeFieldContainer[MetricFilter]
    name: str
    window_function: WindowFunctionKind
    group_by: _containers.RepeatedScalarFieldContainer[GroupByKind]
    def __init__(
        self,
        metric: _Optional[_Union[MetricKind, str]] = ...,
        filters: _Optional[_Iterable[_Union[MetricFilter, _Mapping]]] = ...,
        name: _Optional[str] = ...,
        window_function: _Optional[_Union[WindowFunctionKind, str]] = ...,
        group_by: _Optional[_Iterable[_Union[GroupByKind, str]]] = ...,
    ) -> None: ...

class MetricConfig(_message.Message):
    __slots__ = ("name", "window_period", "series", "formulas", "trigger", "graph_generated")
    NAME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    FORMULAS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    GRAPH_GENERATED_FIELD_NUMBER: _ClassVar[int]
    name: str
    window_period: str
    series: _containers.RepeatedCompositeFieldContainer[MetricConfigSeries]
    formulas: _containers.RepeatedCompositeFieldContainer[MetricFormula]
    trigger: AlertTrigger
    graph_generated: bool
    def __init__(
        self,
        name: _Optional[str] = ...,
        window_period: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[MetricConfigSeries, _Mapping]]] = ...,
        formulas: _Optional[_Iterable[_Union[MetricFormula, _Mapping]]] = ...,
        trigger: _Optional[_Union[AlertTrigger, _Mapping]] = ...,
        graph_generated: bool = ...,
    ) -> None: ...

class Chart(_message.Message):
    __slots__ = ("id", "config", "entity_kind", "entity_id", "graph_generated")
    ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    ENTITY_KIND_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    GRAPH_GENERATED_FIELD_NUMBER: _ClassVar[int]
    id: str
    config: MetricConfig
    entity_kind: ChartLinkKind
    entity_id: str
    graph_generated: bool
    def __init__(
        self,
        id: _Optional[str] = ...,
        config: _Optional[_Union[MetricConfig, _Mapping]] = ...,
        entity_kind: _Optional[_Union[ChartLinkKind, str]] = ...,
        entity_id: _Optional[str] = ...,
        graph_generated: bool = ...,
    ) -> None: ...
