from __future__ import annotations

import math

import pytest

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
    SparklineColumn,
    SparklineTable,
    SparklineTableData,
    SpeedupData,
    StackedBar,
    StackedBarData,
    StackedBarSegment,
    SummaryBox,
    SummaryStats,
)


def test_line_chart_single_point_renders():
    chart = LineChart(
        points=[LinePoint(series="Solo", x=1, y=100)],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Solo" in result


def test_heatmap_single_cell_renders():
    chart = Heatmap(
        matrix=[[42]],
        row_labels=["Q1"],
        col_labels=["A"],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Q1" in result
    assert "42" in result


def test_box_plot_single_value_series_renders():
    chart = BoxPlot(
        series=[BoxPlotSeries(name="One", values=[42])],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "One" in result


def test_bar_chart_handles_nan_without_crash():
    chart = BarChart(
        data=[BarData(label="Normal", value=100), BarData(label="NaN", value=float("nan"))],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Normal" in result


def test_bar_chart_handles_infinity_without_crash():
    chart = BarChart(
        data=[BarData(label="Normal", value=100), BarData(label="Inf", value=float("inf"))],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Normal" in result


def test_histogram_handles_zero_latency_without_division_error():
    chart = Histogram(
        data=[HistogramBar(label="Q1", value=0), HistogramBar(label="Q2", value=0)],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Q1" in result


def test_heatmap_narrow_width_truncates_columns():
    matrix = [[i * 10 for i in range(10)]]
    col_labels = [f"Platform{i}" for i in range(10)]
    chart = Heatmap(
        matrix=matrix,
        row_labels=["Q1"],
        col_labels=col_labels,
        options=ChartOptions(width=40, use_color=False),
    )
    result = chart.render()
    assert "Q1" in result
    assert "..." in result


def test_heatmap_column_fitting_compresses_before_truncating():
    matrix = [[float(10 * (i + 1) + j) for j in range(6)] for i in range(3)]
    row_labels = [f"Q{i + 1}" for i in range(3)]
    col_labels = [f"Platform{j + 1}" for j in range(6)]
    chart = Heatmap(
        matrix=matrix,
        row_labels=row_labels,
        col_labels=col_labels,
        options=ChartOptions(width=120, use_color=False),
    )
    result = chart.render()
    for idx in range(1, 7):
        assert f"Platform{idx}" in result
    assert "..." not in result


def test_bar_chart_sanitizes_ansi_sequences_from_labels():
    chart = BarChart(
        data=[BarData(label="\033[31mInjected\033[0m", value=100)],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "Injected" in result
    assert "\033[31m" not in result


def test_sanitize_text_strips_ansi_sequences():
    assert ChartBase._sanitize_text("\033[1;31mRED\033[0m") == "RED"


def test_scatter_plot_renders_at_minimum_width():
    chart = ScatterPlot(
        points=[ScatterPoint(name="A", x=10, y=20), ScatterPoint(name="B", x=30, y=40)],
        options=ChartOptions(width=40, use_color=False),
    )
    result = chart.render()
    assert "A" in result


NON_FINITE_VALUES = [float("nan"), float("inf"), float("-inf")]


def _non_finite_chart_factory(bad: float):
    """Build one chart per type with a non-finite value mixed with finite data."""
    opts = ChartOptions(use_color=False)
    return {
        "bar": BarChart(
            data=[BarData(label="Bad", value=bad), BarData(label="OK", value=100)],
            options=opts,
        ),
        "box": BoxPlot(
            series=[BoxPlotSeries(name="S", values=[bad, 1.0, 2.0, 3.0])],
            options=opts,
        ),
        "cdf": CDFChart(
            data=[CDFSeriesData(name="S", values=[bad, 1.0, 2.0])],
            options=opts,
        ),
        "comparison": ComparisonBar(
            data=[ComparisonBarData(label="Q", baseline_value=bad, comparison_value=100)],
            options=opts,
        ),
        "diverging": DivergingBar(
            data=[DivergingBarData(label="Bad", pct_change=bad), DivergingBarData(label="OK", pct_change=5.0)],
            options=opts,
        ),
        "heatmap": Heatmap(
            matrix=[[bad, 2.0], [1.0, 3.0]],
            row_labels=["A", "B"],
            col_labels=["X", "Y"],
            options=opts,
        ),
        "histogram": Histogram(
            data=[HistogramBar(label="Bad", value=bad), HistogramBar(label="OK", value=10)],
            options=opts,
        ),
        "line": LineChart(
            points=[
                LinePoint(series="S", x=0, y=bad),
                LinePoint(series="S", x=1, y=1.0),
            ],
            options=opts,
        ),
        "speedup": NormalizedSpeedup(
            data=[SpeedupData(name="Bad", ratio=bad), SpeedupData(name="Base", ratio=1.0, is_baseline=True)],
            options=opts,
        ),
        "ladder": PercentileLadder(
            data=[PercentileData(name="S", p50=bad, p90=bad, p95=bad, p99=bad)],
            options=opts,
        ),
        "rank": RankTable(
            data=RankTableData(
                items=["Q1"],
                groups=["G1", "G2"],
                values={("G1", "Q1"): bad, ("G2", "Q1"): 1.0},
            ),
            options=opts,
        ),
        "scatter": ScatterPlot(
            points=[ScatterPoint(name="Bad", x=bad, y=bad), ScatterPoint(name="OK", x=1.0, y=2.0)],
            options=opts,
        ),
        "sparkline": SparklineTable(
            data=SparklineTableData(
                rows=["A", "B"],
                columns=[SparklineColumn(name="M", values={"A": bad, "B": 1.0})],
            ),
            options=opts,
        ),
        "stacked": StackedBar(
            data=[
                StackedBarData(
                    label="A",
                    segments=[StackedBarSegment(phase_name="p", value=bad)],
                ),
                StackedBarData(
                    label="B",
                    segments=[StackedBarSegment(phase_name="p", value=5.0)],
                ),
            ],
            options=opts,
        ),
        "summary": SummaryBox(
            stats=SummaryStats(title="S", primary_value=bad, secondary_value=1.0),
            options=opts,
        ),
    }


@pytest.mark.parametrize("bad", NON_FINITE_VALUES, ids=["nan", "inf", "neg_inf"])
def test_all_charts_render_without_crash_on_non_finite_input(bad: float):
    charts = _non_finite_chart_factory(bad)
    assert len(charts) == 15
    for name, chart in charts.items():
        result = chart.render()
        assert isinstance(result, str), name
        assert result, name


@pytest.mark.parametrize("bad", NON_FINITE_VALUES, ids=["nan", "inf", "neg_inf"])
def test_heatmap_renders_invalid_cells_as_dash(bad: float):
    chart = Heatmap(
        matrix=[[bad, 2.0]],
        row_labels=["A"],
        col_labels=["X", "Y"],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "-" in result
    assert "A" in result


def test_box_plot_strips_non_finite_before_stats():
    from textcharts.box_plot import compute_quartiles

    stats = compute_quartiles([1.0, float("nan"), float("inf"), 2.0, 3.0])
    assert math.isfinite(stats.median)
    assert math.isfinite(stats.mean)
    assert math.isfinite(stats.std)
    assert all(math.isfinite(v) for v in stats.outliers)


def test_line_chart_ignores_non_finite_points():
    chart = LineChart(
        points=[
            LinePoint(series="S", x=0, y=float("nan")),
            LinePoint(series="S", x=1, y=float("inf")),
            LinePoint(series="S", x=2, y=1.0),
            LinePoint(series="S", x=3, y=2.0),
        ],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert isinstance(result, str) and result


def test_scatter_plot_ignores_non_finite_points():
    chart = ScatterPlot(
        points=[
            ScatterPoint(name="Bad", x=float("nan"), y=float("inf")),
            ScatterPoint(name="OK", x=1.0, y=2.0),
        ],
        options=ChartOptions(use_color=False),
    )
    result = chart.render()
    assert "OK" in result
