"""textcharts — Beautiful text-based charts for your terminal.

Zero-dependency library providing 15 chart types for terminal visualization:
bar, histogram, heatmap, box plot, line, scatter, comparison bar, diverging bar,
summary box, percentile ladder, normalized speedup, stacked bar, sparkline table,
CDF chart, and rank table.

Public API:
    - Chart classes such as ``BarChart`` and ``Heatmap``
    - Data models such as ``BarData`` and ``LinePoint``
    - Shared configuration via ``ChartOptions`` and ``ColorMode``

Basic usage::

    from textcharts import BarChart, BarData, ChartOptions

    data = [
        BarData(label="Python", value=89.5),
        BarData(label="Rust", value=95.2),
        BarData(label="Go", value=78.0),
    ]
    chart = BarChart(data=data, title="Language Benchmark")
    print(chart.render())
"""

__version__ = "0.1.5"

# ---------------------------------------------------------------------------
# Base classes and configuration
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Chart classes and data models
# ---------------------------------------------------------------------------
from textcharts.bar_chart import BarChart, BarData
from textcharts.bar_chart import from_data as bar_from_data
from textcharts.base import (
    ChartBase,
    ChartOptions,
    ColorMode,
    TerminalCapabilities,
    TerminalColors,
    compute_percentile_linear,
    detect_terminal_capabilities,
    outlier_severity_markers,
    robust_p95,
)
from textcharts.box_plot import BoxPlot, BoxPlotSeries, BoxPlotStats
from textcharts.box_plot import from_series as box_from_series
from textcharts.cdf_chart import CDFChart, CDFSeriesData
from textcharts.cdf_chart import from_series as cdf_from_series
from textcharts.comparison_bar import ComparisonBar, ComparisonBarData
from textcharts.comparison_bar import from_data as comparison_from_data
from textcharts.diverging_bar import DivergingBar, DivergingBarData
from textcharts.diverging_bar import from_data as diverging_from_data
from textcharts.heatmap import Heatmap, from_matrix
from textcharts.histogram import Histogram, HistogramBar
from textcharts.histogram import from_data as histogram_from_data
from textcharts.line_chart import LineChart, LinePoint
from textcharts.line_chart import from_points as line_from_points
from textcharts.normalized_speedup import NormalizedSpeedup, SpeedupData
from textcharts.normalized_speedup import from_ratios as speedup_from_ratios
from textcharts.percentile_ladder import PercentileData, PercentileLadder
from textcharts.percentile_ladder import from_series as percentile_from_series
from textcharts.rank_table import RankTable, RankTableData
from textcharts.rank_table import from_matrix as rank_from_matrix
from textcharts.scatter_plot import ScatterPlot, ScatterPoint
from textcharts.scatter_plot import from_points as scatter_from_points
from textcharts.sparkline_table import SparklineColumn, SparklineTable, SparklineTableData
from textcharts.sparkline_table import from_data as sparkline_from_data
from textcharts.stacked_bar import StackedBar, StackedBarData, StackedBarSegment
from textcharts.stacked_bar import from_data as stacked_from_data
from textcharts.summary_box import SummaryBox, SummaryStats

__all__ = [
    "__version__",
    # Chart classes
    "BarChart",
    "BoxPlot",
    "CDFChart",
    "ChartBase",
    "ChartOptions",
    "ComparisonBar",
    "DivergingBar",
    "Heatmap",
    "Histogram",
    "LineChart",
    "NormalizedSpeedup",
    "PercentileLadder",
    "RankTable",
    "ScatterPlot",
    "SparklineTable",
    "StackedBar",
    "SummaryBox",
    # Configuration and utilities
    "ColorMode",
    "TerminalCapabilities",
    "TerminalColors",
    "compute_percentile_linear",
    "detect_terminal_capabilities",
    "outlier_severity_markers",
    "robust_p95",
    # Data models
    "BarData",
    "BoxPlotSeries",
    "BoxPlotStats",
    "CDFSeriesData",
    "ComparisonBarData",
    "DivergingBarData",
    "HistogramBar",
    "LinePoint",
    "PercentileData",
    "RankTableData",
    "ScatterPoint",
    "SparklineColumn",
    "SparklineTableData",
    "SpeedupData",
    "StackedBarData",
    "StackedBarSegment",
    "SummaryStats",
    # Factory functions
    "bar_from_data",
    "box_from_series",
    "cdf_from_series",
    "comparison_from_data",
    "diverging_from_data",
    "from_matrix",
    "histogram_from_data",
    "line_from_points",
    "percentile_from_series",
    "rank_from_matrix",
    "scatter_from_points",
    "sparkline_from_data",
    "speedup_from_ratios",
    "stacked_from_data",
]
