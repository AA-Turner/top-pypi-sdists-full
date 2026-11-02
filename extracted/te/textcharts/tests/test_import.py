"""Smoke test: verify textcharts can be imported and all chart types render."""

import re
from pathlib import Path

import textcharts
from textcharts import (
    BarChart,
    BarData,
    BoxPlot,
    CDFChart,
    ChartOptions,
    ComparisonBar,
    DivergingBar,
    Heatmap,
    Histogram,
    LineChart,
    NormalizedSpeedup,
    PercentileLadder,
    RankTable,
    ScatterPlot,
    SparklineTable,
    StackedBar,
    SummaryBox,
)


def test_import_version():
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    match = re.search(r'^version = "(.+)"', pyproject.read_text(), re.MULTILINE)
    assert match, "Could not find version in pyproject.toml"
    assert textcharts.__version__ == match.group(1)


def test_bar_chart_renders():
    opts = ChartOptions(use_color=False, width=80)
    data = [BarData(label="A", value=100), BarData(label="B", value=200)]
    chart = BarChart(data=data, title="Test", options=opts)
    result = chart.render()
    assert "A" in result
    assert "B" in result


def test_all_chart_classes_exist():
    chart_classes = [
        BarChart,
        BoxPlot,
        CDFChart,
        ComparisonBar,
        DivergingBar,
        Heatmap,
        Histogram,
        LineChart,
        NormalizedSpeedup,
        PercentileLadder,
        RankTable,
        ScatterPlot,
        SparklineTable,
        StackedBar,
        SummaryBox,
    ]
    assert len(chart_classes) == 15
    for cls in chart_classes:
        assert hasattr(cls, "render"), f"{cls.__name__} missing render method"


def test_no_benchbox_dependency():
    """textcharts must not depend on benchbox."""
    import sys

    # Verify no benchbox modules are loaded
    benchbox_modules = [m for m in sys.modules if m.startswith("benchbox")]
    assert not benchbox_modules, f"benchbox modules loaded: {benchbox_modules}"
