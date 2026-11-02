"""Tests for color output and Unicode/ASCII fallback rendering paths."""

from __future__ import annotations

import re

import pytest

import textcharts.base as base
from textcharts import (
    BarChart,
    BarData,
    BoxPlot,
    BoxPlotSeries,
    CDFChart,
    CDFSeriesData,
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
from textcharts.base import ColorMode, TerminalCapabilities, outlier_severity_markers

ANSI_RE = re.compile(r"\x1b\[[\d;]*m")
# Unicode block elements range U+2580-U+259F
UNICODE_BLOCKS_RE = re.compile(r"[\u2580-\u259f]")


def _caps(color_mode: ColorMode) -> TerminalCapabilities:
    return TerminalCapabilities(
        width=80, height=24, color_mode=color_mode,
        unicode_support=True, interactive=color_mode != ColorMode.NONE,
    )


def _make_bar_data():
    return [BarData("A", 10.0), BarData("B", 20.0), BarData("C", 15.0)]


def _make_heatmap_args():
    return dict(matrix=[[10, 20], [30, 40]], row_labels=["Q1", "Q2"], col_labels=["X", "Y"])


def _make_histogram_data():
    return [HistogramBar(label=f"Q{i}", value=float(i * 10)) for i in range(1, 6)]


def _make_scatter_data():
    return [ScatterPoint("A", 10, 100), ScatterPoint("B", 20, 200), ScatterPoint("C", 15, 150)]


# ---------------------------------------------------------------------------
# w1: Color output tests
# ---------------------------------------------------------------------------


def test_bar_chart_color_output_contains_ansi(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _caps(ColorMode.TRUECOLOR))
    result = BarChart(data=_make_bar_data(), options=ChartOptions(width=80)).render()
    assert ANSI_RE.search(result), "Expected ANSI escape sequences in color output"


def test_heatmap_color_output_contains_ansi(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _caps(ColorMode.TRUECOLOR))
    result = Heatmap(**_make_heatmap_args(), options=ChartOptions(width=80)).render()
    assert ANSI_RE.search(result), "Expected ANSI escape sequences in color output"


def test_histogram_color_output_contains_ansi(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _caps(ColorMode.TRUECOLOR))
    result = Histogram(data=_make_histogram_data(), options=ChartOptions(width=80)).render()
    assert ANSI_RE.search(result), "Expected ANSI escape sequences in color output"


def test_scatter_color_output_contains_ansi(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _caps(ColorMode.TRUECOLOR))
    result = ScatterPlot(points=_make_scatter_data(), options=ChartOptions(width=80)).render()
    assert ANSI_RE.search(result), "Expected ANSI escape sequences in color output"


def test_no_color_mode_produces_no_ansi():
    result = BarChart(data=_make_bar_data(), options=ChartOptions(use_color=False, width=80)).render()
    assert not ANSI_RE.search(result), "Expected no ANSI escape sequences in no-color output"


# ---------------------------------------------------------------------------
# w2: ASCII fallback tests
# ---------------------------------------------------------------------------


def test_bar_chart_ascii_fallback():
    result = BarChart(
        data=_make_bar_data(),
        options=ChartOptions(use_color=False, use_unicode=False, width=80),
    ).render()
    assert not UNICODE_BLOCKS_RE.search(result), "Expected no Unicode block chars in ASCII mode"


def test_heatmap_ascii_fallback():
    result = Heatmap(
        **_make_heatmap_args(),
        options=ChartOptions(use_color=False, use_unicode=False, width=80),
    ).render()
    assert not UNICODE_BLOCKS_RE.search(result), "Expected no Unicode block chars in ASCII mode"


def test_histogram_ascii_fallback():
    result = Histogram(
        data=_make_histogram_data(),
        options=ChartOptions(use_color=False, use_unicode=False, width=80),
    ).render()
    assert not UNICODE_BLOCKS_RE.search(result), "Expected no Unicode block chars in ASCII mode"


def test_unicode_mode_uses_block_or_box_chars():
    result = BarChart(
        data=_make_bar_data(),
        options=ChartOptions(use_color=False, use_unicode=True, width=80),
    ).render()
    # Should use Unicode block elements (U+2580-U+259F) or box-drawing (U+2500-U+257F)
    has_blocks = UNICODE_BLOCKS_RE.search(result)
    has_box = re.search(r"[\u2500-\u257f]", result)
    assert has_blocks or has_box, "Expected Unicode chars in Unicode mode"


# ---------------------------------------------------------------------------
# w3: Theme tests
# ---------------------------------------------------------------------------


def test_dark_vs_light_theme_differ(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _caps(ColorMode.TRUECOLOR))
    dark = BarChart(
        data=_make_bar_data(),
        options=ChartOptions(theme="dark", width=80),
    ).render()
    light = BarChart(
        data=_make_bar_data(),
        options=ChartOptions(theme="light", width=80),
    ).render()
    assert ANSI_RE.search(dark)
    assert ANSI_RE.search(light)
    assert dark != light
    assert set(ANSI_RE.findall(dark)) != set(ANSI_RE.findall(light))


# ---------------------------------------------------------------------------
# Strict ASCII compliance across all chart types (use_unicode=False)
# ---------------------------------------------------------------------------

_OUTLIER_VALUES = [10, 11, 12, 13, 14, 15, 5000]


def _ascii_chart_factory(opts: ChartOptions):
    """Build one chart per type with outlier data exercising truncation paths."""
    return {
        "bar": BarChart(
            data=[BarData(label=f"B{i}", value=v) for i, v in enumerate(_OUTLIER_VALUES)],
            options=opts,
        ),
        "box": BoxPlot(
            series=[BoxPlotSeries(name="S", values=[1, 2, 3, 4, 5, 6, 100])],
            options=opts,
        ),
        "cdf": CDFChart(
            data=[CDFSeriesData(name="S", values=[1, 2, 3, 4, 5, 500])],
            options=opts,
        ),
        "comparison": ComparisonBar(
            data=[ComparisonBarData(label="Q", baseline_value=10, comparison_value=5000)],
            options=opts,
        ),
        "diverging": DivergingBar(
            data=[
                DivergingBarData(label="A", pct_change=-5),
                DivergingBarData(label="B", pct_change=726),
            ],
            options=opts,
        ),
        "heatmap": Heatmap(
            matrix=[[10, 20], [30, 9000]],
            row_labels=["Q1", "Q2"],
            col_labels=["X", "Y"],
            options=opts,
        ),
        "histogram": Histogram(
            data=[HistogramBar(label=f"Q{i}", value=v) for i, v in enumerate(_OUTLIER_VALUES)],
            options=opts,
        ),
        "line": LineChart(
            points=[LinePoint(series="S", x=i, y=v) for i, v in enumerate(_OUTLIER_VALUES)],
            options=opts,
        ),
        "speedup": NormalizedSpeedup(
            data=[
                SpeedupData(name="A", ratio=8.0),
                SpeedupData(name="B", ratio=1.0, is_baseline=True),
            ],
            options=opts,
        ),
        "ladder": PercentileLadder(
            data=[PercentileData(name="S", p50=10, p90=20, p95=30, p99=9000)],
            options=opts,
        ),
        "rank": RankTable(
            data=RankTableData(
                items=["Q1"],
                groups=["G1", "G2"],
                values={("G1", "Q1"): 10, ("G2", "Q1"): 20},
            ),
            options=opts,
        ),
        "scatter": ScatterPlot(
            points=[ScatterPoint(name=f"P{i}", x=v, y=v * 10) for i, v in enumerate(_OUTLIER_VALUES)],
            options=opts,
        ),
        "sparkline": SparklineTable(
            data=SparklineTableData(
                rows=["A", "B"],
                columns=[SparklineColumn(name="M", values={"A": 10, "B": 20})],
            ),
            options=opts,
        ),
        "stacked": StackedBar(
            data=[
                StackedBarData(label="A", segments=[StackedBarSegment(phase_name="p", value=10)]),
                StackedBarData(label="B", segments=[StackedBarSegment(phase_name="p", value=9000)]),
            ],
            options=opts,
        ),
        "summary": SummaryBox(
            stats=SummaryStats(title="S", primary_value=100),
            options=opts,
        ),
    }


def test_all_charts_emit_strict_ascii_when_unicode_disabled():
    opts = ChartOptions(use_color=False, use_unicode=False, width=80)
    charts = _ascii_chart_factory(opts)
    assert len(charts) == 15
    for name, chart in charts.items():
        result = chart.render()
        assert isinstance(result, str), name
        try:
            result.encode("ascii")
        except UnicodeEncodeError:
            pytest.fail(f"{name} emitted non-ASCII output with use_unicode=False")


def test_outlier_severity_markers_ascii_fallback():
    assert outlier_severity_markers(21, 2) == "▸▸▸▸"
    assert outlier_severity_markers(21, 2, use_unicode=False) == ">>>>"
    assert outlier_severity_markers(3, 2, use_unicode=False) == ">"
    assert outlier_severity_markers(50, 100, use_unicode=False) == ""


def test_axis_labels_honor_terminal_unicode_detection(monkeypatch: pytest.MonkeyPatch):
    no_unicode = TerminalCapabilities(
        width=80, height=24, color_mode=ColorMode.NONE,
        unicode_support=False, interactive=False,
    )
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: no_unicode)
    result = LineChart(
        points=[LinePoint(series="S", x=0, y=1), LinePoint(series="S", x=1, y=2)],
        options=ChartOptions(use_color=False, use_unicode=True, width=80),
    ).render()
    result.encode("ascii")
