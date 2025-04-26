from __future__ import annotations

import dataclasses
import zlib
from copy import deepcopy
from typing import Any, Callable, ClassVar, List, Literal, Optional, Set, Tuple, TypeVar, Union

from typing_extensions import Concatenate, ParamSpec

from chalk._monitoring.charts_enums_codegen import (
    AlertSeverityKind,
    ChartLinkKind,
    MetricFormulaKind,
    ThresholdPosition,
)
from chalk._monitoring.charts_series_base import SeriesBase, ThresholdFunction
from chalk.features.resolver import Resolver, ResolverProtocol
from chalk.utils.duration import parse_chalk_duration


@dataclasses.dataclass
class _SingleSeriesOperand:
    operand: int


@dataclasses.dataclass
class _MultiSeriesOperand:
    operands: List[int]


@dataclasses.dataclass
class _DatasetFeatureOperand:
    dataset: str
    feature: str


_THRESHOLD_POSITION_MAP = {
    ">": ThresholdPosition.ABOVE,
    ">=": ThresholdPosition.GREATER_EQUAL,
    "<": ThresholdPosition.BELOW,
    "<=": ThresholdPosition.LESS_EQUAL,
    "==": ThresholdPosition.EQUAL,
    "!=": ThresholdPosition.NOT_EQUAL,
}


class _Formula:
    def __init__(
        self,
        name: Optional[str] = None,
        kind: Optional[Union[MetricFormulaKind, str]] = None,
        operands: Optional[Union[_SingleSeriesOperand, _MultiSeriesOperand, _DatasetFeatureOperand]] = None,
    ):
        super().__init__()
        self._name = name
        self._kind = MetricFormulaKind(kind.upper()) if kind else None
        self._operands = operands

    def with_name(self, name: str) -> "_Formula":
        copy = self._copy_with()
        copy._name = name
        return copy

    def with_kind(self, kind: Union[MetricFormulaKind, str]) -> "_Formula":
        copy = self._copy_with()
        copy._kind = MetricFormulaKind(kind.upper())
        return copy

    def with_operands(
        self, operands: Union[_SingleSeriesOperand, _MultiSeriesOperand, _DatasetFeatureOperand]
    ) -> "_Formula":
        copy = self._copy_with()
        copy._operands = operands
        return copy

    def _copy_with(self) -> "_Formula":
        self_copy = deepcopy(self)
        return self_copy

    def __hash__(self) -> int:
        name = self._name if self._name else "."
        kind = str(self._kind) if self._kind else "."
        operands = ""
        if isinstance(self._operands, _SingleSeriesOperand):
            operands = self._operands.operand
        elif isinstance(self._operands, _MultiSeriesOperand):
            operands = self._operands.operands
        elif isinstance(self._operands, _DatasetFeatureOperand):
            operands = f"{self._operands.dataset}.{self._operands.feature}"

        formula_string = f"formula.{name}.{kind}.{operands}"

        return zlib.crc32(formula_string.encode())


class Trigger:
    """
    Class to attach an alert to a Chart. Usually instantiated with the `Chart(...).with_trigger(Trigger(...))` method.
    """

    def __init__(
        self,
        name: str,
        severity: Union[
            AlertSeverityKind,
            Literal[
                "CRITICAL",
                "ERROR",
                "WARNING",
                "INFO",
            ],
        ] = AlertSeverityKind.INFO,
        threshold_position: Optional[
            Union[
                ThresholdPosition,
                Literal[
                    "ABOVE",
                    "BELOW",
                ],
            ]
        ] = None,
        threshold_value: Optional[float] = None,
        series_name: Optional[str] = None,
        channel_name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__()
        self._name = name
        self._severity = severity and AlertSeverityKind(severity.upper())
        self._threshold_position = threshold_position and ThresholdPosition(threshold_position.upper())
        self._threshold_value = threshold_value
        self._series_name = series_name
        self._channel_name = channel_name
        self._description = description

    def with_description(self, description: str) -> "Trigger":
        """Add a description to your `Trigger`. Descriptions
        provided here will be included in the alert message in
        Slack or PagerDuty. Where possible, we render these
        descriptions as markdown.

        Parameters
        ----------
        description
            A description of the trigger.

        Returns
        -------
        Trigger
            A copy of your `Trigger` with the new description.
        """
        copy = self._copy_with()
        copy._description = description
        return copy

    def with_name(self, name: str) -> "Trigger":
        copy = self._copy_with()
        copy._name = name
        return copy

    def with_severity(
        self,
        severity: Literal[
            "CRITICAL",
            "ERROR",
            "WARNING",
            "INFO",
        ],
    ) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind(severity.upper())
        return copy

    def with_critical_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.CRITICAL
        return copy

    def with_error_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.ERROR
        return copy

    def with_warning_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.WARNING
        return copy

    def with_info_severity(self) -> "Trigger":
        copy = self._copy_with()
        copy._severity = AlertSeverityKind.INFO
        return copy

    def with_threshold_position(self, threshold_position: Union[ThresholdPosition, str]) -> "Trigger":
        copy = self._copy_with()
        copy._threshold_position = ThresholdPosition(threshold_position.upper())
        return copy

    def with_threshold_value(self, threshold_value: float) -> "Trigger":
        copy = self._copy_with()
        copy._threshold_value = threshold_value
        return copy

    def with_series_name(self, series_name: str) -> "Trigger":
        copy = self._copy_with()
        copy._series_name = series_name
        return copy

    def with_channel_name(self, channel_name: str) -> "Trigger":
        copy = self._copy_with()
        copy._channel_name = channel_name
        return copy

    def _copy_with(self) -> "Trigger":
        self_copy = deepcopy(self)
        return self_copy

    def __str__(self) -> str:
        return f"Trigger(name='{self._name}')"

    def __hash__(self) -> int:
        name = self._name if self._name else "."
        desc = self._description if self._description else "."
        severity = str(self._severity) if self._severity else "."
        threshold_position = str(self._threshold_position) if self._threshold_position else "."
        threshold_value = str(self._threshold_value) if self._threshold_value else "."
        series_name = self._series_name if self._series_name else "."
        channel_name = self._channel_name if self._channel_name else "."

        trigger_string = (
            f"trigger.{name}.{severity}.{threshold_position}.{threshold_value}.{series_name}.{channel_name}.{desc}"
        )

        return zlib.crc32(trigger_string.encode())


P = ParamSpec("P")
T = TypeVar("T")


def _copy_with(function: Callable[Concatenate[Chart, P], "Chart"]) -> Callable[Concatenate[Chart, P], "Chart"]:
    def inner(self: Chart, *args: P.args, **kwargs: P.kwargs) -> Chart:
        copy = deepcopy(self)
        if not self._keep:
            if self in Chart.registry:
                Chart.registry.remove(self)
        return_copy = function(copy, *args, **kwargs)
        Chart.registry.add(return_copy)
        return return_copy

    return inner


# MetricConfigGQL
class Chart:
    """
    Class describing a single visual metric.
    """

    registry: ClassVar[Set["Chart"]] = set()

    def __init__(self, name: str, window_period: str = "1h", keep: Optional[bool] = False):
        """Create a chart for monitoring or alerting on the Chalk dashboard.

        Parameters
        ----------
        name
            The name of the chart. If a name is not provided, the chart will be
            named according to the series and formulas it contains.
        window_period
            The length of the window, e.g. `"20m"` or `"1h"`.

        Other Parameters
        ----------------
        keep
            By default, the builder methods that return a `Chart` make a deepcopy
            and are not registered for deployment. If `keep=True`, this chart
            and all descendant charts will be registered automatically.

        Returns
        -------
        Chart
            A chart for viewing in the Chalk dashboard.

        Examples
        --------
        >>> from chalk.monitoring import Chart, Series
        >>> Chart(name="Request count").with_trigger(
        ...     Series
        ...         .feature_null_ratio_metric()
        ...         .where(feature=User.fico_score) > 0.2,
        ... )

        """
        super().__init__()
        self._name = name
        self._window_period = window_period
        self._series: List[SeriesBase] = []
        self._formulas: List[_Formula] = []
        self._trigger = None
        self._keep = keep
        self._entity_id = None
        self._entity_kind = ChartLinkKind.manual
        Chart.registry.add(self)

    @_copy_with
    def with_name(self, name: str) -> "Chart":
        """Override the name of a chart.

        Parameters
        ----------
        name
            A new name for a chart.

        Returns
        -------
        Chart
            A copy of your `Chart` with the new name.
        """
        self._name = name
        return self

    @_copy_with
    def with_window_period(self, window_period: str) -> "Chart":
        """Change the window period for a `Chart`.

        Parameters
        ----------
        window_period
            A new window period for a chart, e.g. `"20m"` or `"1h"`.

        Returns
        -------
        Chart
            A copy of your `Chart` with the new window period.
        """
        parse_chalk_duration(window_period)
        self._window_period = window_period
        return self

    @_copy_with
    def with_series(self, series: SeriesBase) -> "Chart":
        """Attaches a `Series` to your `Chart` instance.

        Parameters
        ----------
        series
            A Series instance to attach to the Chart.
            A `Chart` can have any number of `Series`.

        Returns
        -------
        Chart
            A copy of your chart with the new name
        """
        if not isinstance(series, SeriesBase):
            raise ValueError(f"'series' value '{series}' must be a Series object for Chart '{self._name}'")
        if series._entity_id and self._entity_id and series._entity_id != self._entity_id:
            raise ValueError(
                (
                    f"Chart '{self._name}' is already associated with '{self._entity_id}', but new Series "
                    f"'{series.name}' is associated with '{series._entity_id}'. "
                    f"Series can only be associated with one entity."
                )
            )
        self._series.append(series)
        if series._entity_id:
            self._entity_id = series._entity_id
            self._entity_kind = series._entity_kind
        return self

    def get_series(self, series_name: str) -> SeriesBase:
        """Get a `Series` from your `Chart` by series name.

        It is advised to use different series names within your charts.

        Parameters
        ----------
        series_name
            The name of the `Series`.

        Returns
        -------
        Series
            The first series added to your `Chart` with the given series name.
        """
        for series in self._series:
            if series._name == series_name or series._default_name == series_name:
                return series
        raise ValueError(f"No series named '{series_name}' exists in Chart '{self._name}'")

    def _get_series_index(self, series_name: str) -> Tuple[int, SeriesBase]:
        for i, series in enumerate(self._series):
            if series._name == series_name or series._default_name == series_name:
                return i, series
        raise ValueError(f"No series named '{series_name}' exists in Chart '{self._name}'")

    @_copy_with
    def with_formula(
        self,
        /,
        formula: Optional[_Formula] = None,
        name: Optional[str] = None,
        kind: Optional[Union[MetricFormulaKind, str]] = None,
        operands: Optional[Union[_SingleSeriesOperand, _MultiSeriesOperand, _DatasetFeatureOperand]] = None,
    ) -> "Chart":
        if formula:
            if not isinstance(formula, _Formula):
                raise ValueError(f"'formula' value '{formula}' must be a Formula object for Chart '{self._name}'")
            self._formulas.append(formula)
            return self
        if name:
            if not isinstance(name, str):
                raise ValueError(f"'name' value '{name}' must be a string")
            new_formula = _Formula(name=name, kind=kind, operands=operands)
            self._formulas.append(new_formula)
            return self
        raise ValueError(
            "Either a 'name' for a new formula or an existing Formula 'formula' "
            "must be supplied for Chart '{self._name}'"
        )

    @_copy_with
    def with_trigger(
        self,
        expression: ThresholdFunction,
        trigger_name: Optional[str] = None,
        severity: Union[
            AlertSeverityKind,
            Literal[
                "CRITICAL",
                "ERROR",
                "WARNING",
                "INFO",
            ],
        ] = AlertSeverityKind.INFO,
        channel_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> "Chart":
        """Attaches a `Trigger` to your `Chart`. Your `Chart` may optionally have one `Trigger`.

        Parameters
        ----------
        expression
            Triggers are applied when a certain series is above or below a given value.
            The expression specifies the series, operand, and value as follows
                - the left-hand side of the expression must be a Series instance.
                - the operand must be `<` or `>`
                - the right-hand side must be an `int` or `float`
            Thus, if we have a Series instance `series1`, `expression=series1 > 0.5`
            will result in an alert when `series` is greater than 0.5.
        trigger_name
            The name for the new trigger.
        severity
            The severity of the trigger.
                - `critical`
                - `error`
                - `warning`
                - `info`
        channel_name
            The owner or email of the trigger.
        description
            A description to your `Trigger`. Descriptions
            provided here will be included in the alert message in
            Slack or PagerDuty.

            For Slack alerts, you can use the mrkdwn syntax described here:
            https://api.slack.com/reference/surfaces/formatting#basics

        Returns
        -------
        Chart
            A copy of your `Chart` with the new trigger.
        """
        if not isinstance(expression.lhs, SeriesBase):
            raise ValueError(
                f"Left hand side of expression '{expression.lhs}' must be a Series for Chart '{self._name}'"
            )
        if self._trigger is not None:
            raise ValueError(
                f"Trigger is already set for Chart '{self._name}'. Only one alert trigger can be set per chart."
            )
        if trigger_name is None:
            trigger_name = f"{expression.lhs.name}{expression.operation}{expression.rhs}"

        if expression.lhs not in self._series:
            self._series.append(expression.lhs)

        threshold_position = _THRESHOLD_POSITION_MAP[expression.operation]
        self._trigger = Trigger(
            name=trigger_name,
            severity=severity,
            threshold_position=threshold_position,
            threshold_value=expression.rhs,
            series_name=expression.lhs.name,
            channel_name=channel_name,
            description=description,
        )
        return self

    @_copy_with
    def with_feature_link(self, feature: Any) -> "Chart":
        """Explicitly link a Chart to a feature.
        This chart will then be visible on the webpage for this feature.
        Charts may only be linked to one entity.

        Parameters
        ----------
        feature
            A Chalk feature

        Returns
        -------
        Chart
            A copy of your chart linked to the feature.
        """
        self._entity_kind = ChartLinkKind.feature
        self._entity_id = str(feature)
        return self

    @_copy_with
    def with_resolver_link(self, resolver: ResolverProtocol) -> "Chart":
        """Explicitly link a chart to a resolver.
        This chart will then be visible on the webpage for this resolver.
        Charts may only be linked to one entity.

        Parameters
        ----------
        resolver
            A Chalk resolver.

        Returns
        -------
        Chart
            A copy of your chart linked to the resolver.
        """
        self._entity_kind = ChartLinkKind.resolver
        self._entity_id = resolver.fqn if isinstance(resolver, Resolver) else resolver
        return self

    @_copy_with
    def with_query_link(self, query_name: str) -> "Chart":
        """Explicitly link a chart to a query.
        This chart will then be visible on the webpage for this query.
        Charts may only be linked to one entity.

        Parameters
        ----------
        query_name
            A name of a Chalk query

        Returns
        -------
        Chart
            A copy of your chart linked to the query.
        """
        self._entity_kind = ChartLinkKind.query
        self._entity_id = query_name
        return self

    def keep(self) -> "Chart":
        """Designates that this chart and all of its descendants will be registered.

        Returns
        -------
        Chart
            The same chart.
        """
        self._keep = True
        return self

    def __str__(self) -> str:
        return f"Chart(name='{self._name}')"

    def __getitem__(self, key: str) -> Union[SeriesBase, _Formula]:
        """Retrieve a series or formula by name from a chart.

        Parameters
        ----------
        key
            The name of the series or formula to retrieve.

        Returns
        -------
        The series or formula with the given name.
        """
        for series in self._series:
            if series.name == key:
                return series
        for formula in self._formulas:
            if formula._name == key:
                return formula
        raise ValueError(f"No series or formula named '{key}' exists in Chart {self._name}")

    def __eq__(self, obj: object):
        return hash(self) == hash(obj)

    def __hash__(self):
        name = self._name if self._name else "."

        window_period = self._window_period if self._window_period else "."
        chart_string = f"chart.{name}.{window_period}"

        series_hash = ".".join(sorted([str(hash(series)) for series in self._series]))
        formulas = ".".join(sorted([str(hash(formula)) for formula in self._formulas]))
        trigger = str(hash(self._trigger)) if self._trigger else "."

        return zlib.crc32(chart_string.encode() + series_hash.encode() + formulas.encode() + trigger.encode())

    @property
    def name(self):
        return self._name
