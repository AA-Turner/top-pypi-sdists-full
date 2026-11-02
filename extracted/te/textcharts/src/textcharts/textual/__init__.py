"""Optional Textual integration for textcharts."""

from __future__ import annotations

from typing import TYPE_CHECKING

_TEXTUAL_IMPORT_ERROR: ModuleNotFoundError | None = None

try:
    from .charts import (
        BarChartWidget,
        BoxPlotWidget,
        CDFChartWidget,
        ComparisonBarWidget,
        DivergingBarWidget,
        HeatmapWidget,
        HistogramWidget,
        LineChartWidget,
        PercentileWidget,
        RankTableWidget,
        ScatterPlotWidget,
        SparklineWidget,
        SpeedupWidget,
        StackedBarWidget,
        SummaryBoxWidget,
    )
    from .compound import ChartSwitcher
    from .factories import (
        text_bar,
        text_boxplot,
        text_cdf,
        text_chart,
        text_comparison,
        text_diverging,
        text_heatmap,
        text_histogram,
        text_line,
        text_percentile,
        text_rank,
        text_scatter,
        text_sparkline,
        text_speedup,
        text_stacked,
        text_summary,
    )
    from .widget import TextChart
except ModuleNotFoundError as exc:
    if exc.name and exc.name.split(".")[0] == "textual":
        _TEXTUAL_IMPORT_ERROR = exc
    else:
        raise

if TYPE_CHECKING:
    from .charts import (
        BarChartWidget,
        BoxPlotWidget,
        CDFChartWidget,
        ComparisonBarWidget,
        DivergingBarWidget,
        HeatmapWidget,
        HistogramWidget,
        LineChartWidget,
        PercentileWidget,
        RankTableWidget,
        ScatterPlotWidget,
        SparklineWidget,
        SpeedupWidget,
        StackedBarWidget,
        SummaryBoxWidget,
    )
    from .compound import ChartSwitcher
    from .factories import (
        text_bar,
        text_boxplot,
        text_cdf,
        text_chart,
        text_comparison,
        text_diverging,
        text_heatmap,
        text_histogram,
        text_line,
        text_percentile,
        text_rank,
        text_scatter,
        text_sparkline,
        text_speedup,
        text_stacked,
        text_summary,
    )
    from .widget import TextChart

__all__ = [
    "BarChartWidget",
    "BoxPlotWidget",
    "CDFChartWidget",
    "ChartSwitcher",
    "ComparisonBarWidget",
    "DivergingBarWidget",
    "HeatmapWidget",
    "HistogramWidget",
    "LineChartWidget",
    "PercentileWidget",
    "RankTableWidget",
    "ScatterPlotWidget",
    "SparklineWidget",
    "SpeedupWidget",
    "StackedBarWidget",
    "SummaryBoxWidget",
    "TextChart",
    "text_bar",
    "text_boxplot",
    "text_cdf",
    "text_chart",
    "text_comparison",
    "text_diverging",
    "text_heatmap",
    "text_histogram",
    "text_line",
    "text_percentile",
    "text_rank",
    "text_scatter",
    "text_sparkline",
    "text_speedup",
    "text_stacked",
    "text_summary",
]


def __getattr__(name: str):
    if _TEXTUAL_IMPORT_ERROR is not None and name in __all__:
        raise ModuleNotFoundError(
            "textcharts.textual requires the optional 'textual' dependency. "
            "Install it with `pip install textcharts[textual]`."
        ) from _TEXTUAL_IMPORT_ERROR
    raise AttributeError(name)
