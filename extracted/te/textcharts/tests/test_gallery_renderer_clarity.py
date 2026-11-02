from __future__ import annotations

import pytest

import textcharts.base as base
from textcharts import (
    BarChart,
    BarData,
    CDFChart,
    CDFSeriesData,
    ChartOptions,
    Heatmap,
    LineChart,
    LinePoint,
    ScatterPlot,
    ScatterPoint,
    SparklineColumn,
    SparklineTable,
    SparklineTableData,
)
from textcharts.base import ColorMode, TerminalCapabilities


def _capabilities(color_mode: ColorMode) -> TerminalCapabilities:
    return TerminalCapabilities(
        width=96,
        height=30,
        color_mode=color_mode,
        unicode_support=True,
        interactive=color_mode != ColorMode.NONE,
    )


def test_heatmap_uses_configured_x_axis_label():
    chart = Heatmap(
        matrix=[[88.0, 91.0]],
        row_labels=["Class A"],
        col_labels=["Math", "Science"],
        x_label="Subjects",
        options=ChartOptions(width=80, use_color=False),
    )

    result = chart.render()

    assert "Subjects →" in result
    assert "Platform →" not in result


def test_line_chart_compacts_axis_labels_onto_one_line():
    chart = LineChart(
        points=[LinePoint(series="Organic", x=1, y=320.0), LinePoint(series="Organic", x=2, y=355.0)],
        x_label="Week",
        y_label="Signups",
        options=ChartOptions(width=80, use_color=False),
    )

    result = chart.render()

    assert "↑ Signups / Week →" in result
    assert result.count("↑ Signups") == 1
    assert result.count("Week →") == 1


def test_scatter_plot_compacts_axis_labels_onto_one_line():
    chart = ScatterPlot(
        points=[ScatterPoint(name="Launch", x=8.0, y=410.0), ScatterPoint(name="Newsletter", x=2.0, y=220.0)],
        x_label="Cost (USD)",
        y_label="Performance",
        options=ChartOptions(width=96, use_color=False),
    )

    result = chart.render()

    assert "↑ Performance / Cost (USD) →" in result
    assert result.count("↑ Performance") == 1
    assert result.count("Cost (USD) →") == 1


def test_cdf_chart_compacts_axis_labels_onto_one_line():
    chart = CDFChart(
        data=[
            CDFSeriesData(name="Weekday", values=[2, 3, 4, 5]),
            CDFSeriesData(name="Weekend", values=[3, 5, 7, 9]),
        ],
        x_label="Wait Time (min)",
        y_label="Cumulative Share",
        options=ChartOptions(width=96, use_color=False),
    )

    result = chart.render()

    assert "↑ Cumulative Share / Wait Time (min) →" in result


def test_scatter_plot_uses_distinct_markers_for_points():
    chart = ScatterPlot(
        points=[
            ScatterPoint(name="Launch", x=8.0, y=410.0),
            ScatterPoint(name="Retargeting", x=5.5, y=280.0),
            ScatterPoint(name="Newsletter", x=2.0, y=220.0),
        ],
        x_label="Cost (USD)",
        y_label="Conversions",
        options=ChartOptions(width=96, use_color=False),
    )

    result = chart.render()

    assert "* Launch" in result
    assert "+ Retargeting" in result
    assert "o Newsletter" in result


def test_bar_chart_renders_legend_for_multi_bar_output():
    chart = BarChart(
        data=[
            BarData(label="Fiction", value=18.4),
            BarData(label="Children", value=14.2),
            BarData(label="Comics", value=9.3),
        ],
        options=ChartOptions(width=96, use_color=False),
    )

    result = chart.render()

    assert "■ Fiction" in result
    assert "◆ Children" in result
    assert "▲ Comics" in result


def test_sparkline_table_colorizes_best_and_worst_legend(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _capabilities(ColorMode.TRUECOLOR))
    data = SparklineTableData(
        rows=["North Store", "South Store"],
        columns=[SparklineColumn(name="Revenue", values={"North Store": 82.0, "South Store": 95.0})],
    )
    chart = SparklineTable(data=data, options=ChartOptions(width=96, use_color=True))

    result = chart.render()

    assert "\033[" in result
    assert "=best" in result
    assert "=worst" in result
