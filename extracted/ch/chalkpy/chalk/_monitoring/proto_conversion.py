from typing import Optional

import chalk._gen.chalk.artifacts.v1.chart_pb2 as pb
from chalk._monitoring.Chart import Chart as _Chart
from chalk._monitoring.Chart import Trigger, _DatasetFeatureOperand, _Formula, _MultiSeriesOperand, _SingleSeriesOperand
from chalk._monitoring.charts_enums_codegen import (
    AlertSeverityKind,
    ChartLinkKind,
    ComparatorKind,
    FilterKind,
    GroupByKind,
    MetricFormulaKind,
    MetricKind,
    ThresholdPosition,
    WindowFunctionKind,
)
from chalk._monitoring.charts_series_base import MetricFilter, SeriesBase

_ENTITY_KIND_TO_PROTO = {
    ChartLinkKind.resolver: pb.ChartLinkKind.CHART_LINK_KIND_RESOLVER,
    ChartLinkKind.feature: pb.ChartLinkKind.CHART_LINK_KIND_FEATURE,
    ChartLinkKind.query: pb.ChartLinkKind.CHART_LINK_KIND_QUERY,
    ChartLinkKind.manual: pb.ChartLinkKind.CHART_LINK_KIND_MANUAL,
}

_METRIC_KIND_TO_PROTO = {
    MetricKind.FEATURE_REQUEST_COUNT: pb.MetricKind.METRIC_KIND_FEATURE_REQUEST_COUNT,
    MetricKind.FEATURE_LATENCY: pb.MetricKind.METRIC_KIND_FEATURE_LATENCY,
    MetricKind.FEATURE_STALENESS: pb.MetricKind.METRIC_KIND_FEATURE_STALENESS,
    MetricKind.FEATURE_VALUE: pb.MetricKind.METRIC_KIND_FEATURE_VALUE,
    MetricKind.FEATURE_WRITE: pb.MetricKind.METRIC_KIND_FEATURE_WRITE,
    MetricKind.FEATURE_NULL_RATIO: pb.MetricKind.METRIC_KIND_FEATURE_NULL_RATIO,
    MetricKind.RESOLVER_REQUEST_COUNT: pb.MetricKind.METRIC_KIND_RESOLVER_REQUEST_COUNT,
    MetricKind.RESOLVER_LATENCY: pb.MetricKind.METRIC_KIND_RESOLVER_LATENCY,
    MetricKind.RESOLVER_SUCCESS_RATIO: pb.MetricKind.METRIC_KIND_RESOLVER_SUCCESS_RATIO,
    MetricKind.QUERY_COUNT: pb.MetricKind.METRIC_KIND_QUERY_COUNT,
    MetricKind.QUERY_LATENCY: pb.MetricKind.METRIC_KIND_QUERY_LATENCY,
    MetricKind.QUERY_SUCCESS_RATIO: pb.MetricKind.METRIC_KIND_QUERY_SUCCESS_RATIO,
    MetricKind.BILLING_INFERENCE: pb.MetricKind.METRIC_KIND_BILLING_INFERENCE,
    MetricKind.BILLING_CRON: pb.MetricKind.METRIC_KIND_BILLING_CRON,
    MetricKind.BILLING_MIGRATION: pb.MetricKind.METRIC_KIND_BILLING_MIGRATION,
    MetricKind.CRON_COUNT: pb.MetricKind.METRIC_KIND_CRON_COUNT,
    MetricKind.CRON_LATENCY: pb.MetricKind.METRIC_KIND_CRON_LATENCY,
    MetricKind.STREAM_MESSAGES_PROCESSED: pb.MetricKind.METRIC_KIND_STREAM_MESSAGES_PROCESSED,
    MetricKind.STREAM_MESSAGE_LATENCY: pb.MetricKind.METRIC_KIND_STREAM_MESSAGE_LATENCY,
    MetricKind.STREAM_WINDOWS_PROCESSED: pb.MetricKind.METRIC_KIND_STREAM_WINDOWS_PROCESSED,
    MetricKind.STREAM_WINDOW_LATENCY: pb.MetricKind.METRIC_KIND_STREAM_WINDOW_LATENCY,
}

_FILTER_KIND_TO_PROTO = {
    FilterKind.FEATURE_STATUS: pb.FilterKind.FILTER_KIND_FEATURE_STATUS,
    FilterKind.FEATURE_NAME: pb.FilterKind.FILTER_KIND_FEATURE_NAME,
    FilterKind.FEATURE_TAG: pb.FilterKind.FILTER_KIND_FEATURE_TAG,
    FilterKind.RESOLVER_STATUS: pb.FilterKind.FILTER_KIND_RESOLVER_STATUS,
    FilterKind.RESOLVER_NAME: pb.FilterKind.FILTER_KIND_RESOLVER_NAME,
    FilterKind.RESOLVER_TAG: pb.FilterKind.FILTER_KIND_RESOLVER_TAG,
    FilterKind.CRON_STATUS: pb.FilterKind.FILTER_KIND_CRON_STATUS,
    FilterKind.MIGRATION_STATUS: pb.FilterKind.FILTER_KIND_MIGRATION_STATUS,
    FilterKind.ONLINE_OFFLINE: pb.FilterKind.FILTER_KIND_ONLINE_OFFLINE,
    FilterKind.CACHE_HIT: pb.FilterKind.FILTER_KIND_CACHE_HIT,
    FilterKind.OPERATION_ID: pb.FilterKind.FILTER_KIND_OPERATION_ID,
    FilterKind.QUERY_NAME: pb.FilterKind.FILTER_KIND_QUERY_NAME,
    FilterKind.QUERY_STATUS: pb.FilterKind.FILTER_KIND_QUERY_STATUS,
    FilterKind.IS_NULL: pb.FilterKind.FILTER_KIND_IS_NULL,
    FilterKind.USAGE_KIND: pb.FilterKind.FILTER_KIND_USAGE_KIND,
}

_COMPARATOR_KIND_TO_PROTO = {
    ComparatorKind.EQ: pb.ComparatorKind.COMPARATOR_KIND_EQ,
    ComparatorKind.NEQ: pb.ComparatorKind.COMPARATOR_KIND_NEQ,
    ComparatorKind.ONE_OF: pb.ComparatorKind.COMPARATOR_KIND_ONE_OF,
}

_WINDOW_FUNCTION_KIND_TO_PROTO = {
    WindowFunctionKind.COUNT: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_COUNT,
    WindowFunctionKind.MEAN: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_MEAN,
    WindowFunctionKind.SUM: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_SUM,
    WindowFunctionKind.MIN: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_MIN,
    WindowFunctionKind.MAX: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_MAX,
    WindowFunctionKind.PERCENTILE_99: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_PERCENTILE_99,
    WindowFunctionKind.PERCENTILE_95: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_PERCENTILE_95,
    WindowFunctionKind.PERCENTILE_75: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_PERCENTILE_75,
    WindowFunctionKind.PERCENTILE_50: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_PERCENTILE_50,
    WindowFunctionKind.PERCENTILE_25: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_PERCENTILE_25,
    WindowFunctionKind.PERCENTILE_5: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_PERCENTILE_5,
    WindowFunctionKind.ALL_PERCENTILES: pb.WindowFunctionKind.WINDOW_FUNCTION_KIND_ALL_PERCENTILES,
}

_GROUP_BY_KIND_TO_PROTO = {
    GroupByKind.FEATURE_STATUS: pb.GroupByKind.GROUP_BY_KIND_FEATURE_STATUS,
    GroupByKind.FEATURE_NAME: pb.GroupByKind.GROUP_BY_KIND_FEATURE_NAME,
    GroupByKind.IS_NULL: pb.GroupByKind.GROUP_BY_KIND_IS_NULL,
    GroupByKind.RESOLVER_STATUS: pb.GroupByKind.GROUP_BY_KIND_RESOLVER_STATUS,
    GroupByKind.RESOLVER_NAME: pb.GroupByKind.GROUP_BY_KIND_RESOLVER_NAME,
    GroupByKind.QUERY_STATUS: pb.GroupByKind.GROUP_BY_KIND_QUERY_STATUS,
    GroupByKind.QUERY_NAME: pb.GroupByKind.GROUP_BY_KIND_QUERY_NAME,
    GroupByKind.ONLINE_OFFLINE: pb.GroupByKind.GROUP_BY_KIND_ONLINE_OFFLINE,
    GroupByKind.CACHE_HIT: pb.GroupByKind.GROUP_BY_KIND_CACHE_HIT,
    GroupByKind.USAGE_KIND: pb.GroupByKind.GROUP_BY_KIND_USAGE_KIND,
}

_METRIC_FORMULA_KIND_TO_PROTO = {
    MetricFormulaKind.SUM: pb.MetricFormulaKind.METRIC_FORMULA_KIND_SUM,
    MetricFormulaKind.TOTAL_RATIO: pb.MetricFormulaKind.METRIC_FORMULA_KIND_TOTAL_RATIO,
    MetricFormulaKind.RATIO: pb.MetricFormulaKind.METRIC_FORMULA_KIND_RATIO,
    MetricFormulaKind.PRODUCT: pb.MetricFormulaKind.METRIC_FORMULA_KIND_PRODUCT,
    MetricFormulaKind.ABS: pb.MetricFormulaKind.METRIC_FORMULA_KIND_ABS,
    MetricFormulaKind.KS_STAT: pb.MetricFormulaKind.METRIC_FORMULA_KIND_KS_STAT,
    MetricFormulaKind.KS_TEST: pb.MetricFormulaKind.METRIC_FORMULA_KIND_KS_TEST,
    MetricFormulaKind.KS_THRESHOLD: pb.MetricFormulaKind.METRIC_FORMULA_KIND_KS_THRESHOLD,
    MetricFormulaKind.TIME_OFFSET: pb.MetricFormulaKind.METRIC_FORMULA_KIND_TIME_OFFSET,
}

_ALERT_SEVERITY_KIND_TO_PROTO = {
    AlertSeverityKind.CRITICAL: pb.AlertSeverityKind.ALERT_SEVERITY_KIND_CRITICAL,
    AlertSeverityKind.ERROR: pb.AlertSeverityKind.ALERT_SEVERITY_KIND_ERROR,
    AlertSeverityKind.WARNING: pb.AlertSeverityKind.ALERT_SEVERITY_KIND_WARNING,
    AlertSeverityKind.INFO: pb.AlertSeverityKind.ALERT_SEVERITY_KIND_INFO,
}

_THRESHOLD_POSITION_KIND_TO_PROTO = {
    ThresholdPosition.ABOVE: pb.ThresholdKind.THRESHOLD_KIND_ABOVE,
    ThresholdPosition.BELOW: pb.ThresholdKind.THRESHOLD_KIND_BELOW,
    ThresholdPosition.GREATER_EQUAL: pb.ThresholdKind.THRESHOLD_KIND_GREATER_EQUAL,
    ThresholdPosition.LESS_EQUAL: pb.ThresholdKind.THRESHOLD_KIND_LESS_EQUAL,
    ThresholdPosition.EQUAL: pb.ThresholdKind.THRESHOLD_KIND_EQUAL,
    ThresholdPosition.NOT_EQUAL: pb.ThresholdKind.THRESHOLD_KIND_NOT_EQUAL,
}


def _convert_metric_kind(metric_kind: Optional[MetricKind], chart_name: str, series_name: str) -> pb.MetricKind:
    if metric_kind is None:
        raise ValueError(
            f"Chart '{chart_name}' has a series '{series_name}' with no metric. "
            f"'metric' is a required value for Series instances"
        )
    res = _METRIC_KIND_TO_PROTO.get(metric_kind)
    if res is None:
        raise ValueError(f"Chart '{chart_name}' has an invalid metric '{metric_kind}'")
    return res


def _convert_filter_kind(filter_kind: FilterKind) -> pb.FilterKind:
    res = _FILTER_KIND_TO_PROTO.get(filter_kind)
    if res is None:
        raise ValueError(f"Invalid filter kind '{filter_kind}'")
    return res


def _convert_comparator_kind(comparator_kind: ComparatorKind) -> pb.ComparatorKind:
    res = _COMPARATOR_KIND_TO_PROTO.get(comparator_kind)
    if res is None:
        raise ValueError(f"Invalid comparator kind '{comparator_kind}'")
    return res


def _convert_window_function_kind(
    window_function: Optional[WindowFunctionKind],
) -> Optional["pb.WindowFunctionKind"]:
    if window_function is None:
        return None
    res = _WINDOW_FUNCTION_KIND_TO_PROTO.get(window_function)
    if res is None:
        raise ValueError(f"Invalid window function kind '{window_function}'")
    return res


def _convert_group_by_kind(group_by: GroupByKind) -> pb.GroupByKind:
    res = _GROUP_BY_KIND_TO_PROTO.get(group_by)
    if res is None:
        raise ValueError(f"Invalid group by kind '{group_by}'")
    return res


def _convert_alert_severity_kind(
    alert_severity: Optional[AlertSeverityKind], chart_name: str, trigger_name: str
) -> pb.AlertSeverityKind:
    if not alert_severity:
        raise ValueError(
            f"Chart '{chart_name}' has a trigger '{trigger_name} with no severity level. "
            f"'severity' is a required value for Trigger instances"
        )
    res = _ALERT_SEVERITY_KIND_TO_PROTO.get(alert_severity)
    if res is None:
        raise ValueError(f"Invalid alert severity kind '{alert_severity}'")
    return res


def _convert_threshold_position(
    threshold_position: Optional[ThresholdPosition], chart_name: str, trigger_name: str
) -> pb.ThresholdKind:
    if not threshold_position:
        raise ValueError(
            f"Chart '{chart_name}' has a trigger '{trigger_name} with no threshold position. "
            f"'threshold_position' is a required value for Trigger instances"
        )
    res = _THRESHOLD_POSITION_KIND_TO_PROTO.get(threshold_position)
    if res is None:
        raise ValueError(f"Invalid threshold position kind '{threshold_position}'")
    return res


def _convert_metric_formula_kind(
    kind: Optional[MetricFormulaKind], chart_name: str, formula_name: str
) -> pb.MetricFormulaKind:
    if not kind:
        raise ValueError(
            f"Chart '{chart_name}' has a formula '{formula_name}' with no operation kind. "
            f"'kind' is a required value for Formula instances"
        )
    res = _METRIC_FORMULA_KIND_TO_PROTO.get(kind)
    if res is None:
        raise ValueError(f"Invalid metric formula kind '{kind}'")
    return res


def _convert_filter(filter: MetricFilter) -> pb.MetricFilter:
    return pb.MetricFilter(
        kind=_convert_filter_kind(filter.kind),
        comparator=_convert_comparator_kind(filter.comparator),
    )


def _convert_series(series: SeriesBase, chart_name: str) -> pb.MetricConfigSeries:
    for validation_fn in series._validations:
        validation_fn()
    return pb.MetricConfigSeries(
        metric=_convert_metric_kind(series._metric, chart_name, series._name),
        filters=[_convert_filter(series_filter) for series_filter in series._filters],
        name=series._name if series._name else series._default_name,
        window_function=_convert_window_function_kind(series._window_function),
        group_by=series._group_by,
    )


def _convert_formula(formula: _Formula, chart_name: str) -> pb.MetricFormula:
    operands = formula._operands
    if not operands:
        raise ValueError(
            f"Chart '{chart_name}' has a formula '{formula._name}' with no operands. "
            f"'operands' is a required value for Formula instances"
        )
    single_series = None
    multi_series = None
    dataset_feature = None
    if isinstance(operands, _SingleSeriesOperand):
        single_series = operands.operand
    elif isinstance(operands, _MultiSeriesOperand):
        multi_series = operands.operands
    elif isinstance(operands, _DatasetFeatureOperand):
        dataset_feature = pb.DatasetFeatureOperand(dataset=operands.dataset, feature=operands.feature)
    else:
        raise ValueError(
            f"Chart '{chart_name}' has a formula {formula._name}' with an invalid value for operand '{operands}'"
        )
    return pb.MetricFormula(
        kind=_convert_metric_formula_kind(formula._kind, chart_name, formula._name),
        single_series_operands=single_series,
        multi_series_operands=multi_series,
        dataset_feature_operands=dataset_feature,
    )


def _convert_trigger(trigger: Trigger, chart_name: str) -> pb.AlertTrigger:
    if not trigger._name:
        raise ValueError(
            f"Chart {chart_name} has a trigger with no name. " f"'name' is a required value for Trigger instances"
        )
    if trigger._threshold_value is None:
        raise ValueError(
            "Chart {chart_name} has a trigger with no threshold value. "
            "'threshold_value' is a required value for Trigger instances"
        )
    return pb.AlertTrigger(
        name=trigger._name,
        severity=_convert_alert_severity_kind(trigger._severity, chart_name, trigger._name),
        threshold_position=_convert_threshold_position(trigger._threshold_position, chart_name, trigger._name),
        threshold_value=trigger._threshold_value,
        series_name=trigger._series_name,
        channel_name=trigger._channel_name,
        description=trigger._description,
    )


def convert_chart(chart: _Chart) -> pb.Chart:
    if not chart._window_period:
        raise ValueError(
            f"Chart {chart._name} has no window period. " f"window_period' is a required value for Chart instances"
        )
    entity_kind = _ENTITY_KIND_TO_PROTO.get(chart._entity_kind)
    if entity_kind is None:
        raise ValueError(f"Chart {chart._name} has an invalid entity_kind '{chart._entity_kind}'")
    config = pb.MetricConfig(
        name=chart._name,
        window_period=chart._window_period,
        series=[_convert_series(series, chart._name) for series in chart._series],
        formulas=[_convert_formula(formula, chart._name) for formula in chart._formulas],
        trigger=_convert_trigger(chart._trigger, chart._name) if chart._trigger else None,
    )
    return pb.Chart(
        id=str(hash(chart)),
        config=config,
        entity_kind=entity_kind,
        entity_id=chart._entity_id,
    )
