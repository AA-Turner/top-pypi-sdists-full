"""Typed Textual widgets for individual textcharts chart types."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from textual.reactive import reactive

from textcharts import (
    BarChart,
    BarData,
    BoxPlot,
    BoxPlotSeries,
    CDFChart,
    CDFSeriesData,
    ChartBase,
    ChartOptions,
    ComparisonBar,
    ComparisonBarData,
    DivergingBar,
    DivergingBarData,
    Heatmap,
    Histogram,
    HistogramBar,
    LineChart,
    LinePoint,
    NormalizedSpeedup,
    PercentileData,
    PercentileLadder,
    RankTable,
    RankTableData,
    ScatterPlot,
    ScatterPoint,
    SparklineTable,
    SparklineTableData,
    SpeedupData,
    StackedBar,
    StackedBarData,
    SummaryBox,
    SummaryStats,
)

from .widget import TextChart


class _ChartWidgetBase(TextChart):
    """Base class for typed chart widgets that rebuild a chart from reactives."""

    def __init__(
        self,
        *,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        self._chart_title = title
        self._chart_subtitle = subtitle
        self._chart_subject = subject
        self._chart_options = replace(options) if options is not None else ChartOptions()
        super().__init__(self._build_chart, id=id, classes=classes, disabled=disabled)

    def _copy_options(self) -> ChartOptions:
        return replace(self._chart_options)

    def _set_initial_reactives(self, **values: Any) -> None:
        for name, value in values.items():
            self.set_reactive(getattr(type(self), name), value)

    def _watch_rebuild(self, *_: object) -> None:
        self._rebuild()

    def _rebuild(self) -> None:
        self.rebuild_chart()

    def _build_chart(self) -> ChartBase:
        raise NotImplementedError


class BarChartWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    metric_label = reactive("Value", init=False, repaint=False)
    sort_by = reactive("value", init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_metric_label = _ChartWidgetBase._watch_rebuild
    watch_sort_by = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[BarData] | None = None,
        *,
        metric_label: str = "Value",
        sort_by: str = "value",
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(data=list(data or []), metric_label=metric_label, sort_by=sort_by)
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return BarChart(
            self.data,
            title=self._chart_title,
            metric_label=self.metric_label,
            sort_by=self.sort_by,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class HistogramWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    y_label = reactive("Value", init=False, repaint=False)
    sort_by = reactive("label", init=False, repaint=False)
    max_per_chart = reactive(33, init=False, repaint=False)
    show_mean_line = reactive(True, init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_y_label = _ChartWidgetBase._watch_rebuild
    watch_sort_by = _ChartWidgetBase._watch_rebuild
    watch_max_per_chart = _ChartWidgetBase._watch_rebuild
    watch_show_mean_line = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[HistogramBar] | None = None,
        *,
        y_label: str = "Value",
        sort_by: str = "label",
        max_per_chart: int = 33,
        show_mean_line: bool = True,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(
            data=list(data or []),
            y_label=y_label,
            sort_by=sort_by,
            max_per_chart=max_per_chart,
            show_mean_line=show_mean_line,
        )
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return Histogram(
            self.data,
            title=self._chart_title,
            y_label=self.y_label,
            sort_by=self.sort_by,
            max_per_chart=self.max_per_chart,
            show_mean_line=self.show_mean_line,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class HeatmapWidget(_ChartWidgetBase):
    matrix = reactive(list, init=False, repaint=False)
    row_labels = reactive(list, init=False, repaint=False)
    col_labels = reactive(list, init=False, repaint=False)
    value_label = reactive("", init=False, repaint=False)
    x_label = reactive("Columns", init=False, repaint=False)
    show_values = reactive(True, init=False, repaint=False)
    color_scheme = reactive("diverging", init=False, repaint=False)

    watch_matrix = _ChartWidgetBase._watch_rebuild
    watch_row_labels = _ChartWidgetBase._watch_rebuild
    watch_col_labels = _ChartWidgetBase._watch_rebuild
    watch_value_label = _ChartWidgetBase._watch_rebuild
    watch_x_label = _ChartWidgetBase._watch_rebuild
    watch_show_values = _ChartWidgetBase._watch_rebuild
    watch_color_scheme = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        matrix: list[list[float | None]] | None = None,
        *,
        row_labels: list[str] | None = None,
        col_labels: list[str] | None = None,
        value_label: str = "",
        x_label: str = "Columns",
        show_values: bool = True,
        color_scheme: str = "diverging",
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(
            matrix=[list(row) for row in matrix or []],
            row_labels=list(row_labels or []),
            col_labels=list(col_labels or []),
            value_label=value_label,
            x_label=x_label,
            show_values=show_values,
            color_scheme=color_scheme,
        )
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        matrix = self.matrix
        if not matrix and self.row_labels and self.col_labels:
            matrix = [[None for _ in self.col_labels] for _ in self.row_labels]
        return Heatmap(
            matrix,
            self.row_labels,
            self.col_labels,
            title=self._chart_title,
            value_label=self.value_label,
            x_label=self.x_label,
            show_values=self.show_values,
            color_scheme=self.color_scheme,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class BoxPlotWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    y_label = reactive("Value", init=False, repaint=False)
    show_stats = reactive(True, init=False, repaint=False)
    show_mean = reactive(True, init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_y_label = _ChartWidgetBase._watch_rebuild
    watch_show_stats = _ChartWidgetBase._watch_rebuild
    watch_show_mean = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[BoxPlotSeries] | None = None,
        *,
        y_label: str = "Value",
        show_stats: bool = True,
        show_mean: bool = True,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(
            data=list(data or []),
            y_label=y_label,
            show_stats=show_stats,
            show_mean=show_mean,
        )
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return BoxPlot(
            self.data,
            title=self._chart_title,
            y_label=self.y_label,
            show_stats=self.show_stats,
            show_mean=self.show_mean,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class LineChartWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    x_label = reactive("X", init=False, repaint=False)
    y_label = reactive("Y", init=False, repaint=False)
    show_trend = reactive(False, init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_x_label = _ChartWidgetBase._watch_rebuild
    watch_y_label = _ChartWidgetBase._watch_rebuild
    watch_show_trend = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[LinePoint] | None = None,
        *,
        x_label: str = "X",
        y_label: str = "Y",
        show_trend: bool = False,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(
            data=list(data or []),
            x_label=x_label,
            y_label=y_label,
            show_trend=show_trend,
        )
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return LineChart(
            self.data,
            title=self._chart_title,
            x_label=self.x_label,
            y_label=self.y_label,
            show_trend=self.show_trend,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class ScatterPlotWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    x_label = reactive("X", init=False, repaint=False)
    y_label = reactive("Y", init=False, repaint=False)
    show_pareto = reactive(True, init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_x_label = _ChartWidgetBase._watch_rebuild
    watch_y_label = _ChartWidgetBase._watch_rebuild
    watch_show_pareto = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[ScatterPoint] | None = None,
        *,
        x_label: str = "X",
        y_label: str = "Y",
        show_pareto: bool = True,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(
            data=list(data or []),
            x_label=x_label,
            y_label=y_label,
            show_pareto=show_pareto,
        )
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return ScatterPlot(
            self.data,
            title=self._chart_title,
            x_label=self.x_label,
            y_label=self.y_label,
            show_pareto=self.show_pareto,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class ComparisonBarWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    metric_label = reactive("Value", init=False, repaint=False)
    lower_is_better = reactive(True, init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_metric_label = _ChartWidgetBase._watch_rebuild
    watch_lower_is_better = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[ComparisonBarData] | None = None,
        *,
        metric_label: str = "Value",
        lower_is_better: bool = True,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(
            data=list(data or []),
            metric_label=metric_label,
            lower_is_better=lower_is_better,
        )
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return ComparisonBar(
            self.data,
            title=self._chart_title,
            metric_label=self.metric_label,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
            lower_is_better=self.lower_is_better,
        )


class DivergingBarWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    clip_pct = reactive(200.0, init=False, repaint=False)
    lower_is_better = reactive(True, init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_clip_pct = _ChartWidgetBase._watch_rebuild
    watch_lower_is_better = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[DivergingBarData] | None = None,
        *,
        clip_pct: float = 200.0,
        lower_is_better: bool = True,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(
            data=list(data or []),
            clip_pct=clip_pct,
            lower_is_better=lower_is_better,
        )
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return DivergingBar(
            self.data,
            title=self._chart_title,
            clip_pct=self.clip_pct,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
            lower_is_better=self.lower_is_better,
        )


class SummaryBoxWidget(_ChartWidgetBase):
    stats = reactive(lambda: SummaryStats(), init=False, repaint=False)

    watch_stats = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        stats: SummaryStats | None = None,
        *,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(subtitle=subtitle, subject=subject, options=options, id=id, classes=classes, disabled=disabled)
        self._set_initial_reactives(stats=stats or SummaryStats())
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return SummaryBox(
            self.stats,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class PercentileWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    metric_label = reactive("", init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_metric_label = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[PercentileData] | None = None,
        *,
        metric_label: str = "",
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(data=list(data or []), metric_label=metric_label)
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return PercentileLadder(
            self.data,
            title=self._chart_title,
            metric_label=self.metric_label,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class SpeedupWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    baseline_name = reactive(None, init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_baseline_name = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[SpeedupData] | None = None,
        *,
        baseline_name: str | None = None,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(data=list(data or []), baseline_name=baseline_name)
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return NormalizedSpeedup(
            self.data,
            title=self._chart_title,
            baseline_name=self.baseline_name,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class StackedBarWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    metric_label = reactive("", init=False, repaint=False)
    value_formatter = reactive(None, init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_metric_label = _ChartWidgetBase._watch_rebuild
    watch_value_formatter = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[StackedBarData] | None = None,
        *,
        metric_label: str = "",
        value_formatter: Any = None,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(
            data=list(data or []),
            metric_label=metric_label,
            value_formatter=value_formatter,
        )
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return StackedBar(
            self.data,
            title=self._chart_title,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            metric_label=self.metric_label,
            value_formatter=self.value_formatter,
            subject=self._chart_subject,
        )


class SparklineWidget(_ChartWidgetBase):
    data = reactive(lambda: SparklineTableData(rows=[], columns=[]), init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: SparklineTableData | None = None,
        *,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(data=data or SparklineTableData(rows=[], columns=[]))
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return SparklineTable(
            self.data,
            title=self._chart_title,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class CDFChartWidget(_ChartWidgetBase):
    data = reactive(list, init=False, repaint=False)
    x_label = reactive("Value", init=False, repaint=False)
    y_label = reactive("Cumulative Share", init=False, repaint=False)
    chart_height = reactive(15, init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild
    watch_x_label = _ChartWidgetBase._watch_rebuild
    watch_y_label = _ChartWidgetBase._watch_rebuild
    watch_chart_height = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: list[CDFSeriesData] | None = None,
        *,
        x_label: str = "Value",
        y_label: str = "Cumulative Share",
        chart_height: int = 15,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(
            data=list(data or []),
            x_label=x_label,
            y_label=y_label,
            chart_height=chart_height,
        )
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return CDFChart(
            self.data,
            title=self._chart_title,
            x_label=self.x_label,
            y_label=self.y_label,
            height=self.chart_height,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )


class RankTableWidget(_ChartWidgetBase):
    data = reactive(lambda: RankTableData(items=[], groups=[], values={}), init=False, repaint=False)

    watch_data = _ChartWidgetBase._watch_rebuild

    def __init__(
        self,
        data: RankTableData | None = None,
        *,
        title: str | None = None,
        subtitle: str | None = None,
        subject: str | None = None,
        options: ChartOptions | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self._set_initial_reactives(data=data or RankTableData(items=[], groups=[], values={}))
        self._rebuild()

    def _build_chart(self) -> ChartBase:
        return RankTable(
            self.data,
            title=self._chart_title,
            options=self._copy_options(),
            subtitle=self._chart_subtitle,
            subject=self._chart_subject,
        )
