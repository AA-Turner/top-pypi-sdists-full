"""Direct tests for all public factory functions.

Tests happy path (return type, data passthrough, options forwarding)
and edge cases (empty data, single item).
"""

from __future__ import annotations

from textcharts import (
    BarChart,
    BarData,
    BoxPlot,
    BoxPlotSeries,
    CDFChart,
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
    PercentileLadder,
    RankTable,
    ScatterPlot,
    ScatterPoint,
    SparklineTable,
    StackedBar,
    StackedBarData,
    StackedBarSegment,
    bar_from_data,
    box_from_series,
    cdf_from_series,
    comparison_from_data,
    diverging_from_data,
    from_matrix,
    histogram_from_data,
    line_from_points,
    percentile_from_series,
    rank_from_matrix,
    scatter_from_points,
    sparkline_from_data,
    speedup_from_ratios,
    stacked_from_data,
)


def _opts(**kw):
    return ChartOptions(use_color=False, width=80, **kw)


# ---------------------------------------------------------------------------
# w1: Happy-path tests for all 14 factory functions
# ---------------------------------------------------------------------------


def test_bar_from_data():
    data = [BarData("A", 10.0), BarData("B", 20.0)]
    chart = bar_from_data(data, title="Bar Test", options=_opts())
    assert isinstance(chart, BarChart)
    result = chart.render()
    assert "Bar Test" in result
    assert "A" in result


def test_histogram_from_data():
    data = [HistogramBar(label="Q1", value=100)]
    chart = histogram_from_data(data, title="Hist Test", options=_opts())
    assert isinstance(chart, Histogram)
    assert "Q1" in chart.render()


def test_from_matrix():
    chart = from_matrix(
        matrix=[[10, 20], [30, 40]],
        queries=["Q1", "Q2"],
        platforms=["A", "B"],
        title="Heat Test",
        options=_opts(),
    )
    assert isinstance(chart, Heatmap)
    result = chart.render()
    assert "Heat Test" in result
    assert "Q1" in result


def test_box_from_series():
    series = [BoxPlotSeries("S1", [10, 20, 30, 40, 50])]
    chart = box_from_series(series, title="Box Test", options=_opts())
    assert isinstance(chart, BoxPlot)
    assert "Box Test" in chart.render()


def test_line_from_points():
    points = [LinePoint("S", 1, 10.0), LinePoint("S", 2, 20.0), LinePoint("S", 3, 15.0)]
    chart = line_from_points(points, title="Line Test", options=_opts())
    assert isinstance(chart, LineChart)
    assert "Line Test" in chart.render()


def test_scatter_from_points():
    points = [ScatterPoint("A", 10, 100), ScatterPoint("B", 20, 200)]
    chart = scatter_from_points(points, title="Scatter Test", options=_opts())
    assert isinstance(chart, ScatterPlot)
    assert "Scatter Test" in chart.render()


def test_comparison_from_data():
    data = [ComparisonBarData("Q1", 100, 80)]
    chart = comparison_from_data(data, title="Comp Test", options=_opts())
    assert isinstance(chart, ComparisonBar)
    assert "Comp Test" in chart.render()


def test_diverging_from_data():
    data = [DivergingBarData("Q1", -10.0)]
    chart = diverging_from_data(data, title="Div Test", options=_opts())
    assert isinstance(chart, DivergingBar)
    assert "Div Test" in chart.render()


def test_speedup_from_ratios():
    chart = speedup_from_ratios(
        [("A", 100), ("B", 200)], title="Speed Test", options=_opts()
    )
    assert isinstance(chart, NormalizedSpeedup)
    assert "Speed Test" in chart.render()


def test_stacked_from_data():
    data = [StackedBarData("P1", [StackedBarSegment("Load", 100)])]
    chart = stacked_from_data(data, title="Stack Test", options=_opts())
    assert isinstance(chart, StackedBar)
    assert "Stack Test" in chart.render()


def test_sparkline_from_data():
    chart = sparkline_from_data(
        rows=["A", "B"],
        metrics=[("Latency", {"A": 50, "B": 100}, False)],
        title="Spark Test",
        options=_opts(),
    )
    assert isinstance(chart, SparklineTable)
    assert "Spark Test" in chart.render()


def test_cdf_from_series():
    chart = cdf_from_series(
        [("A", [10, 20, 30, 40, 50])], title="CDF Test", options=_opts()
    )
    assert isinstance(chart, CDFChart)
    assert "CDF Test" in chart.render()


def test_percentile_from_series():
    chart = percentile_from_series(
        [("A", [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])],
        title="Pct Test",
        options=_opts(),
    )
    assert isinstance(chart, PercentileLadder)
    assert "Pct Test" in chart.render()


def test_rank_from_matrix():
    chart = rank_from_matrix(
        matrix=[[10, 20], [30, 40]],
        items=["Q1", "Q2"],
        groups=["A", "B"],
        title="Rank Test",
        options=_opts(),
    )
    assert isinstance(chart, RankTable)
    assert "Rank Test" in chart.render()


# ---------------------------------------------------------------------------
# w2: Edge-case factory tests
# ---------------------------------------------------------------------------


def test_bar_from_data_empty():
    chart = bar_from_data([], options=_opts())
    assert "No data" in chart.render()


def test_box_from_series_single_value():
    series = [BoxPlotSeries("S1", [42.0])]
    chart = box_from_series(series, options=_opts())
    result = chart.render()
    assert "S1" in result


def test_from_matrix_1x1():
    chart = from_matrix([[99.0]], ["Q1"], ["A"], options=_opts())
    result = chart.render()
    assert "Q1" in result
    assert "99" in result


def test_cdf_from_series_empty_values():
    chart = cdf_from_series([("Empty", [])], options=_opts())
    result = chart.render()
    # CDF with no values renders "No data"
    assert "No data" in result


def test_line_from_points_single_point():
    points = [LinePoint("S", 1, 42.0)]
    chart = line_from_points(points, options=_opts())
    result = chart.render()
    assert "42" in result


def test_scatter_from_points_single():
    points = [ScatterPoint("Solo", 10, 100)]
    chart = scatter_from_points(points, options=_opts())
    result = chart.render()
    assert "Solo" in result
