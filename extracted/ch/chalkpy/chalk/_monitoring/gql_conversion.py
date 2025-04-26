from typing import Union

from chalk._monitoring.Chart import (
    AlertSeverityKind,
    Chart,
    MetricFormulaKind,
    SeriesBase,
    ThresholdPosition,
    Trigger,
    _DatasetFeatureOperand,
    _Formula,
    _MultiSeriesOperand,
    _SingleSeriesOperand,
)
from chalk._monitoring.charts_enums_codegen import (
    ComparatorKind,
    FilterKind,
    GroupByKind,
    MetricKind,
    WindowFunctionKind,
)
from chalk._monitoring.charts_series_base import MetricFilter
from chalk.parsed.duplicate_input_gql import (
    AlertSeverityKindGQL,
    ComparatorKindGQL,
    CreateAlertTriggerGQL,
    CreateChartGQL,
    CreateDatasetFeatureOperandGQL,
    CreateMetricConfigGQL,
    CreateMetricConfigSeriesGQL,
    CreateMetricFilterGQL,
    CreateMetricFormulaGQL,
    FilterKindGQL,
    GroupByKindGQL,
    MetricFormulaKindGQL,
    MetricKindGQL,
    ThresholdKindGQL,
    WindowFunctionKindGQL,
)


def _convert_series(series: SeriesBase, chart_name: str) -> CreateMetricConfigSeriesGQL:
    for validation_fn in series._validations:
        validation_fn()
    return CreateMetricConfigSeriesGQL(
        metric=convert_metric_kind(series._metric, chart_name, series._name),
        filters=[_convert_filter(series_filter) for series_filter in series._filters],
        name=series._name or series._default_name,
        windowFunction=_convert_window_function(series._window_function),
        groupBy=[_convert_group_by(group_by) for group_by in series._group_by],
    )


def convert_metric_kind(metric_kind: Union[MetricKind, None], chart_name: str, series_name: str) -> MetricKindGQL:
    if not metric_kind:
        raise ValueError(
            f"Chart '{chart_name}' has a series '{series_name}' with no metric. "
            f"'metric' is a required value for Series instances"
        )
    return MetricKindGQL(metric_kind.value.upper())


def _convert_filter(filter: MetricFilter) -> CreateMetricFilterGQL:
    return CreateMetricFilterGQL(
        kind=_convert_filter_kind(filter.kind),
        comparator=_convert_comparator_kind(filter.comparator),
        value=filter.value,
    )


def _convert_filter_kind(filter_kind: FilterKind) -> FilterKindGQL:
    return FilterKindGQL(filter_kind.value.upper())


def _convert_comparator_kind(comparator_kind: ComparatorKind) -> ComparatorKindGQL:
    return ComparatorKindGQL(comparator_kind.value.upper())


def _convert_window_function(window_function: Union[WindowFunctionKind, None]) -> Union[WindowFunctionKindGQL, None]:
    if not window_function:
        return None
    return WindowFunctionKindGQL(window_function.value.upper())


def _convert_group_by(group_by: GroupByKind) -> GroupByKindGQL:
    return GroupByKindGQL(group_by.value.upper())


def _convert_formula(formula: _Formula, chart_name: str) -> CreateMetricFormulaGQL:
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
        dataset_feature = CreateDatasetFeatureOperandGQL(dataset=operands.dataset, feature=operands.feature)
    if not single_series and not multi_series and not dataset_feature:
        raise ValueError(
            f"Chart '{chart_name}' has a formula {formula._name}' with an invalid value for operand '{operands}'"
        )
    return CreateMetricFormulaGQL(
        kind=_convert_metric_formula_kind(formula._kind, chart_name, formula._name),
        singleSeriesOperands=single_series,
        multiSeriesOperands=multi_series,
        datasetFeatureOperands=dataset_feature,
        name=formula._name,
    )


def _convert_metric_formula_kind(
    kind: Union[MetricFormulaKind, None], chart_name: str, formula_name: str
) -> MetricFormulaKindGQL:
    if not kind:
        raise ValueError(
            f"Chart '{chart_name}' has a formula '{formula_name}' with no operation kind. "
            f"'kind' is a required value for Formula instances"
        )
    return MetricFormulaKindGQL(kind.value.upper())


def _convert_trigger(trigger: Trigger, chart_name: str) -> CreateAlertTriggerGQL:
    if not trigger._name:
        raise ValueError(
            f"Chart {chart_name} has a trigger with no name. " f"'name' is a required value for Trigger instances"
        )
    if trigger._threshold_value is None:
        raise ValueError(
            "Chart {chart_name} has a trigger with no threshold value. "
            "'threshold_value' is a required value for Trigger instances"
        )
    return CreateAlertTriggerGQL(
        name=trigger._name,
        severity=_convert_severity(trigger._severity, chart_name, trigger._name),
        thresholdPosition=_convert_threshold_position(trigger._threshold_position, chart_name, trigger._name),
        thresholdValue=trigger._threshold_value,
        seriesName=trigger._series_name,
        channelName=trigger._channel_name,
        description=trigger._description,
    )


def _convert_severity(
    severity: Union[AlertSeverityKind, None], chart_name: str, trigger_name: str
) -> AlertSeverityKindGQL:
    if not severity:
        raise ValueError(
            f"Chart '{chart_name}' has a trigger '{trigger_name} with no severity level. "
            f"'severity' is a required value for Trigger instances"
        )
    return AlertSeverityKindGQL(severity.value.lower())  # this GQL Enum object is the only in lowercase


def _convert_threshold_position(
    threshold_position: Union[ThresholdPosition, None], chart_name: str, trigger_name: str
) -> ThresholdKindGQL:
    if not threshold_position:
        raise ValueError(
            f"Chart '{chart_name}' has a trigger '{trigger_name} with no threshold position. "
            f"'threshold_position' is a required value for Trigger instances"
        )
    return ThresholdKindGQL(threshold_position.value.upper())


def convert_chart(chart: Chart) -> CreateChartGQL:
    if not chart._window_period:
        raise ValueError(
            f"Chart {chart._name} has no window period. " f"window_period' is a required value for Chart instances"
        )
    config = CreateMetricConfigGQL(
        name=chart._name,
        windowPeriod=chart._window_period,
        series=[_convert_series(series, chart._name) for series in chart._series],
        formulas=[_convert_formula(formula, chart._name) for formula in chart._formulas],
        trigger=_convert_trigger(chart._trigger, chart._name) if chart._trigger else None,
    )
    return CreateChartGQL(
        id=str(hash(chart)),
        config=config,
        entityKind=chart._entity_kind.value,
        entityId=chart._entity_id,
    )
