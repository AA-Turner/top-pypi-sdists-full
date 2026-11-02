"""Factory helpers for building Textual textcharts widgets."""

from __future__ import annotations

import importlib
from dataclasses import replace
from typing import Any, Mapping

from textcharts import (
    CDFChart,
    ChartBase,
    ChartOptions,
    NormalizedSpeedup,
    PercentileLadder,
    RankTable,
    SparklineTable,
    StackedBar,
    SummaryBox,
    SummaryStats,
    bar_from_data,
    box_from_series,
    comparison_from_data,
    diverging_from_data,
    histogram_from_data,
    line_from_points,
    scatter_from_points,
)
from textcharts.commands.executor import _build_chart_options
from textcharts.commands.parsers import parse_input
from textcharts.commands.registry import get_command
from textcharts.heatmap import from_matrix

from .widget import TextChart


def text_chart(
    chart_type: str,
    data: Any,
    *,
    title: str | None = None,
    subtitle: str | None = None,
    subject: str | None = None,
    options: ChartOptions | Mapping[str, Any] | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
    **kwargs: Any,
) -> TextChart:
    """Create a ``TextChart`` from a command-style chart name and raw input."""
    return _wrap(
        _build_chart_instance(
            chart_type,
            data,
            title=title,
            subtitle=subtitle,
            subject=subject,
            options=options,
            **kwargs,
        ),
        widget_kwargs,
    )


def text_bar(
    data: Any,
    *,
    title: str | None = None,
    metric_label: str = "Value",
    sort_by: str = "value",
    options: ChartOptions | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(
        bar_from_data(data, title=title, metric_label=metric_label, sort_by=sort_by, options=options, subject=subject),
        widget_kwargs,
    )


def text_histogram(
    data: Any,
    *,
    title: str | None = None,
    y_label: str = "Value",
    sort_by: str = "label",
    max_per_chart: int = 33,
    show_mean_line: bool = True,
    options: ChartOptions | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(
        histogram_from_data(
            data,
            title=title,
            y_label=y_label,
            sort_by=sort_by,
            max_per_chart=max_per_chart,
            show_mean_line=show_mean_line,
            options=options,
            subject=subject,
        ),
        widget_kwargs,
    )


def text_heatmap(
    matrix: list[list[float | None]],
    row_labels: list[str],
    col_labels: list[str],
    *,
    title: str | None = None,
    value_label: str = "",
    x_label: str = "Platform",
    show_values: bool = True,
    color_scheme: str = "diverging",
    options: ChartOptions | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(
        from_matrix(
            matrix,
            row_labels,
            col_labels,
            title=title,
            value_label=value_label,
            x_label=x_label,
            show_values=show_values,
            color_scheme=color_scheme,
            options=options,
            subject=subject,
        ),
        widget_kwargs,
    )


def text_boxplot(
    series: Any,
    *,
    title: str | None = None,
    y_label: str = "Value",
    show_stats: bool = True,
    show_mean: bool = True,
    options: ChartOptions | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(
        box_from_series(
            series,
            title=title,
            y_label=y_label,
            show_stats=show_stats,
            show_mean=show_mean,
            options=options,
            subject=subject,
        ),
        widget_kwargs,
    )


def text_line(
    points: Any,
    *,
    title: str | None = None,
    x_label: str = "Run",
    y_label: str = "Y",
    show_trend: bool = False,
    options: ChartOptions | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(
        line_from_points(
            points,
            title=title,
            x_label=x_label,
            y_label=y_label,
            show_trend=show_trend,
            options=options,
            subject=subject,
        ),
        widget_kwargs,
    )


def text_scatter(
    points: Any,
    *,
    title: str | None = None,
    x_label: str = "X",
    y_label: str = "Y",
    show_pareto: bool = True,
    options: ChartOptions | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(
        scatter_from_points(
            points,
            title=title,
            x_label=x_label,
            y_label=y_label,
            show_pareto=show_pareto,
            options=options,
            subject=subject,
        ),
        widget_kwargs,
    )


def text_comparison(
    data: Any,
    *,
    title: str | None = None,
    metric_label: str = "Value",
    lower_is_better: bool = True,
    options: ChartOptions | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    chart = comparison_from_data(data, title=title, metric_label=metric_label, options=options, subject=subject)
    chart.lower_is_better = lower_is_better
    return _wrap(chart, widget_kwargs)


def text_diverging(
    data: Any,
    *,
    title: str | None = None,
    clip_pct: float = 200.0,
    lower_is_better: bool = True,
    options: ChartOptions | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    chart = diverging_from_data(data, title=title, options=options, subject=subject)
    chart.clip_pct = clip_pct
    chart.lower_is_better = lower_is_better
    return _wrap(chart, widget_kwargs)


def text_summary(
    stats: SummaryStats,
    *,
    title: str | None = None,
    options: ChartOptions | None = None,
    subtitle: str | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    if title is not None:
        stats = replace(stats, title=title)
    return _wrap(SummaryBox(stats, options=options, subtitle=subtitle, subject=subject), widget_kwargs)


def text_percentile(
    data: list[Any],
    *,
    title: str | None = None,
    metric_label: str = "",
    options: ChartOptions | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(
        PercentileLadder(
            data,
            title=title,
            metric_label=metric_label,
            options=options,
            subject=subject,
        ),
        widget_kwargs,
    )


def text_speedup(
    data: list[Any],
    *,
    title: str | None = None,
    baseline_name: str | None = None,
    options: ChartOptions | None = None,
    subtitle: str | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(
        NormalizedSpeedup(
            data,
            title=title,
            baseline_name=baseline_name,
            options=options,
            subtitle=subtitle,
            subject=subject,
        ),
        widget_kwargs,
    )


def text_stacked(
    data: list[Any],
    *,
    title: str | None = None,
    metric_label: str = "",
    value_formatter: Any = None,
    options: ChartOptions | None = None,
    subtitle: str | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(
        StackedBar(
            data,
            title=title,
            metric_label=metric_label,
            value_formatter=value_formatter,
            options=options,
            subtitle=subtitle,
            subject=subject,
        ),
        widget_kwargs,
    )


def text_sparkline(
    data: Any,
    *,
    title: str | None = None,
    options: ChartOptions | None = None,
    subtitle: str | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(SparklineTable(data, title=title, options=options, subtitle=subtitle, subject=subject), widget_kwargs)


def text_cdf(
    data: list[Any],
    *,
    title: str | None = None,
    x_label: str = "Value",
    y_label: str = "Cumulative Share",
    chart_height: int = 15,
    options: ChartOptions | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(
        CDFChart(
            data,
            title=title,
            x_label=x_label,
            y_label=y_label,
            height=chart_height,
            options=options,
            subject=subject,
        ),
        widget_kwargs,
    )


def text_rank(
    data: Any,
    *,
    title: str | None = None,
    options: ChartOptions | None = None,
    subtitle: str | None = None,
    subject: str | None = None,
    widget_kwargs: Mapping[str, Any] | None = None,
) -> TextChart:
    return _wrap(RankTable(data, title=title, options=options, subtitle=subtitle, subject=subject), widget_kwargs)


def _build_chart_instance(
    command: str,
    data: Any,
    *,
    title: str | None = None,
    subtitle: str | None = None,
    subject: str | None = None,
    options: ChartOptions | Mapping[str, Any] | None = None,
    **kwargs: Any,
) -> ChartBase:
    cmd_info = get_command(command)
    parsed_data = parse_input(command, data)
    chart_options = _coerce_chart_options(options)
    ctor_kwargs: dict[str, Any] = {}

    if command == "heatmap":
        if not isinstance(parsed_data, dict):
            raise ValueError("heatmap parser must return a mapping")
        ctor_kwargs.update(parsed_data)
    else:
        ctor_kwargs[cmd_info.data_param_name] = parsed_data

    if title is not None:
        if command == "summary":
            parsed_data = replace(parsed_data, title=title)
            ctor_kwargs[cmd_info.data_param_name] = parsed_data
        else:
            ctor_kwargs["title"] = title
    if subtitle is not None:
        ctor_kwargs["subtitle"] = subtitle
    if subject is not None:
        ctor_kwargs["subject"] = subject
    if chart_options is not None:
        ctor_kwargs["options"] = chart_options

    valid_param_names = {param.name for param in cmd_info.chart_params}
    for key, value in kwargs.items():
        if key in valid_param_names:
            ctor_kwargs[key] = value

    module = importlib.import_module(cmd_info.chart_module)
    chart_cls = getattr(module, cmd_info.chart_class)
    return chart_cls(**ctor_kwargs)


def _coerce_chart_options(options: ChartOptions | Mapping[str, Any] | None) -> ChartOptions | None:
    if options is None or isinstance(options, ChartOptions):
        return options
    return _build_chart_options(dict(options))


def _wrap(chart: ChartBase, widget_kwargs: Mapping[str, Any] | None) -> TextChart:
    return TextChart(chart, **dict(widget_kwargs or {}))
