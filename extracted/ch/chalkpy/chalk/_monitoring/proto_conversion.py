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

# Every MetricKind in charts_enums_codegen.py (generated from the artifacts/v1 chart proto) maps to its
# pb.MetricKind equivalent here, in proto value order.
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
    MetricKind.ONLINE_STORE_KEY_COUNT: pb.MetricKind.METRIC_KIND_ONLINE_STORE_KEY_COUNT,
    MetricKind.ONLINE_STORE_EXPIRED_KEY_COUNT: pb.MetricKind.METRIC_KIND_ONLINE_STORE_EXPIRED_KEY_COUNT,
    MetricKind.ONLINE_STORE_REQUESTS_PER_SECOND: pb.MetricKind.METRIC_KIND_ONLINE_STORE_REQUESTS_PER_SECOND,
    MetricKind.CPU_UTILIZATION_PERCENT: pb.MetricKind.METRIC_KIND_CPU_UTILIZATION_PERCENT,
    MetricKind.REPLICA_COUNT: pb.MetricKind.METRIC_KIND_REPLICA_COUNT,
    MetricKind.ONLINE_STORE_USED_MEMORY: pb.MetricKind.METRIC_KIND_ONLINE_STORE_USED_MEMORY,
    MetricKind.ONLINE_STORE_TOTAL_MEMORY: pb.MetricKind.METRIC_KIND_ONLINE_STORE_TOTAL_MEMORY,
    MetricKind.MEMORY_USAGE_BYTES: pb.MetricKind.METRIC_KIND_MEMORY_USAGE_BYTES,
    MetricKind.TOTAL_MEMORY_AVAILABLE_BYTES: pb.MetricKind.METRIC_KIND_TOTAL_MEMORY_AVAILABLE_BYTES,
    MetricKind.NETWORK_READ_BYTES: pb.MetricKind.METRIC_KIND_NETWORK_READ_BYTES,
    MetricKind.NETWORK_WRITE_BYTES: pb.MetricKind.METRIC_KIND_NETWORK_WRITE_BYTES,
    MetricKind.DISK_READ_BYTES: pb.MetricKind.METRIC_KIND_DISK_READ_BYTES,
    MetricKind.DISK_WRITE_BYTES: pb.MetricKind.METRIC_KIND_DISK_WRITE_BYTES,
    MetricKind.STREAM_LAG: pb.MetricKind.METRIC_KIND_STREAM_LAG,
    MetricKind.USAGE: pb.MetricKind.METRIC_KIND_USAGE,
    MetricKind.FEATURE_COMPUTED_COUNT: pb.MetricKind.METRIC_KIND_FEATURE_COMPUTED_COUNT,
    MetricKind.FEATURE_LOOKED_UP_COUNT: pb.MetricKind.METRIC_KIND_FEATURE_LOOKED_UP_COUNT,
    MetricKind.FEATURE_INTERMEDIATE_COUNT: pb.MetricKind.METRIC_KIND_FEATURE_INTERMEDIATE_COUNT,
    MetricKind.FEATURE_COMPUTED_NULL_RATIO: pb.MetricKind.METRIC_KIND_FEATURE_COMPUTED_NULL_RATIO,
    MetricKind.FEATURE_LOOKED_UP_NULL_RATIO: pb.MetricKind.METRIC_KIND_FEATURE_LOOKED_UP_NULL_RATIO,
    MetricKind.FEATURE_INTERMEDIATE_NULL_RATIO: pb.MetricKind.METRIC_KIND_FEATURE_INTERMEDIATE_NULL_RATIO,
    MetricKind.STREAM_INGEST_DELAY: pb.MetricKind.METRIC_KIND_STREAM_INGEST_DELAY,
    MetricKind.CONTAINER_MEMORY_BYTES: pb.MetricKind.METRIC_KIND_CONTAINER_MEMORY_BYTES,
    MetricKind.HOST_MEMORY_BYTES: pb.MetricKind.METRIC_KIND_HOST_MEMORY_BYTES,
    MetricKind.CONTAINER_CPU_UTILIZATION: pb.MetricKind.METRIC_KIND_CONTAINER_CPU_UTILIZATION,
    MetricKind.DISK_USED_BYTES: pb.MetricKind.METRIC_KIND_DISK_USED_BYTES,
    MetricKind.DISK_AVAILABLE_BYTES: pb.MetricKind.METRIC_KIND_DISK_AVAILABLE_BYTES,
    MetricKind.RESOLVER_INVOKER_NET_TX: pb.MetricKind.METRIC_KIND_RESOLVER_INVOKER_NET_TX,
    MetricKind.RESOLVER_INVOKER_NET_RX: pb.MetricKind.METRIC_KIND_RESOLVER_INVOKER_NET_RX,
    MetricKind.RESOLVER_INVOKER_ROWS_WRITTEN: pb.MetricKind.METRIC_KIND_RESOLVER_INVOKER_ROWS_WRITTEN,
    MetricKind.TOPIC_MESSAGES_PROCESSED: pb.MetricKind.METRIC_KIND_TOPIC_MESSAGES_PROCESSED,
    MetricKind.SUBSCRIPTION_NUM_UNACKED_MESSAGES: pb.MetricKind.METRIC_KIND_SUBSCRIPTION_NUM_UNACKED_MESSAGES,
    MetricKind.SUBSCRIPTION_OLDEST_UNACKED_MESSAGE_AGE: pb.MetricKind.METRIC_KIND_SUBSCRIPTION_OLDEST_UNACKED_MESSAGE_AGE,
    MetricKind.TOPIC_OFFSET_LAG: pb.MetricKind.METRIC_KIND_TOPIC_OFFSET_LAG,
    MetricKind.GPU_UTILIZATION: pb.MetricKind.METRIC_KIND_GPU_UTILIZATION,
    MetricKind.GPU_TENSOR_ACTIVITY: pb.MetricKind.METRIC_KIND_GPU_TENSOR_ACTIVITY,
    MetricKind.GPU_SM_CLOCK_MHZ: pb.MetricKind.METRIC_KIND_GPU_SM_CLOCK_MHZ,
    MetricKind.GPU_POWER_WATTS: pb.MetricKind.METRIC_KIND_GPU_POWER_WATTS,
    MetricKind.GPU_TEMPERATURE_CELSIUS: pb.MetricKind.METRIC_KIND_GPU_TEMPERATURE_CELSIUS,
    MetricKind.GPU_THROTTLE_REASONS: pb.MetricKind.METRIC_KIND_GPU_THROTTLE_REASONS,
    MetricKind.GPU_FP16_ACTIVITY: pb.MetricKind.METRIC_KIND_GPU_FP16_ACTIVITY,
    MetricKind.GPU_COUNT: pb.MetricKind.METRIC_KIND_GPU_COUNT,
    MetricKind.PULL_QUERY_QUEUE_DEPTH: pb.MetricKind.METRIC_KIND_PULL_QUERY_QUEUE_DEPTH,
    MetricKind.PULL_QUERY_OLDEST_UNACKED_AGE: pb.MetricKind.METRIC_KIND_PULL_QUERY_OLDEST_UNACKED_AGE,
    MetricKind.PULL_QUERY_PROCESSED: pb.MetricKind.METRIC_KIND_PULL_QUERY_PROCESSED,
    MetricKind.PULL_QUERY_LATENCY: pb.MetricKind.METRIC_KIND_PULL_QUERY_LATENCY,
    MetricKind.CONTAINER_COUNT: pb.MetricKind.METRIC_KIND_CONTAINER_COUNT,
    MetricKind.SCALING_GROUP_REPLICA_COUNT: pb.MetricKind.METRIC_KIND_SCALING_GROUP_REPLICA_COUNT,
    MetricKind.PULL_QUERY_MAX_INFLIGHT: pb.MetricKind.METRIC_KIND_PULL_QUERY_MAX_INFLIGHT,
    MetricKind.PULL_QUERY_CONCURRENCY_TARGET: pb.MetricKind.METRIC_KIND_PULL_QUERY_CONCURRENCY_TARGET,
    MetricKind.PULL_QUERY_OPEN_CONNECTIONS: pb.MetricKind.METRIC_KIND_PULL_QUERY_OPEN_CONNECTIONS,
    MetricKind.FUNCTION_CALL_ENQUEUED: pb.MetricKind.METRIC_KIND_FUNCTION_CALL_ENQUEUED,
    MetricKind.FUNCTION_CALL_ENQUEUE_LATENCY: pb.MetricKind.METRIC_KIND_FUNCTION_CALL_ENQUEUE_LATENCY,
    MetricKind.FUNCTION_CALL_OPEN_CONNECTIONS: pb.MetricKind.METRIC_KIND_FUNCTION_CALL_OPEN_CONNECTIONS,
    MetricKind.FUNCTION_CALL_DEQUEUED: pb.MetricKind.METRIC_KIND_FUNCTION_CALL_DEQUEUED,
    MetricKind.FUNCTION_CALL_PROCESSING_LATENCY: pb.MetricKind.METRIC_KIND_FUNCTION_CALL_PROCESSING_LATENCY,
    MetricKind.FUNCTION_CALL_QUEUE_DEPTH: pb.MetricKind.METRIC_KIND_FUNCTION_CALL_QUEUE_DEPTH,
    MetricKind.FUNCTION_CALL_INFLIGHT: pb.MetricKind.METRIC_KIND_FUNCTION_CALL_INFLIGHT,
    MetricKind.POD_CONTAINER_MEMORY_BYTES: pb.MetricKind.METRIC_KIND_POD_CONTAINER_MEMORY_BYTES,
    MetricKind.POD_CONTAINER_CPU_UTILIZATION: pb.MetricKind.METRIC_KIND_POD_CONTAINER_CPU_UTILIZATION,
    MetricKind.QUERY_PROGRESS_SPLITS_PROCESSED: pb.MetricKind.METRIC_KIND_QUERY_PROGRESS_SPLITS_PROCESSED,
    MetricKind.QUERY_PROGRESS_SPLITS_QUEUED: pb.MetricKind.METRIC_KIND_QUERY_PROGRESS_SPLITS_QUEUED,
    MetricKind.QUERY_PROGRESS_BLOCKED_DRIVERS: pb.MetricKind.METRIC_KIND_QUERY_PROGRESS_BLOCKED_DRIVERS,
    MetricKind.QUERY_PROGRESS_RESOLVER_ROWS_RETURNED: pb.MetricKind.METRIC_KIND_QUERY_PROGRESS_RESOLVER_ROWS_RETURNED,
    MetricKind.QUERY_PROGRESS_OPERATOR_OUTPUT_BYTES: pb.MetricKind.METRIC_KIND_QUERY_PROGRESS_OPERATOR_OUTPUT_BYTES,
    MetricKind.QUERY_PROGRESS_OPERATOR_ROWS_PROCESSED: pb.MetricKind.METRIC_KIND_QUERY_PROGRESS_OPERATOR_ROWS_PROCESSED,
    MetricKind.SCHEDULED_QUERY_COUNT: pb.MetricKind.METRIC_KIND_SCHEDULED_QUERY_COUNT,
    MetricKind.SCHEDULED_QUERY_SUCCESS_RATIO: pb.MetricKind.METRIC_KIND_SCHEDULED_QUERY_SUCCESS_RATIO,
    MetricKind.HYPERVISOR_CONTAINER_CPU_UTILIZATION: pb.MetricKind.METRIC_KIND_HYPERVISOR_CONTAINER_CPU_UTILIZATION,
    MetricKind.HYPERVISOR_CONTAINER_MEMORY_BYTES: pb.MetricKind.METRIC_KIND_HYPERVISOR_CONTAINER_MEMORY_BYTES,
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
            f"Chart {chart_name} has a trigger with no name. 'name' is a required value for Trigger instances"
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
            f"Chart {chart._name} has no window period. window_period' is a required value for Chart instances"
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
