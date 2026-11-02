"""Tests for textcharts rendering."""

from __future__ import annotations

from unittest.mock import patch

from textcharts.bar_chart import BarChart, BarData
from textcharts.bar_chart import from_data as bar_from_data
from textcharts.base import (
    ChartOptions,
    ColorMode,
    TerminalCapabilities,
    TerminalColors,
    detect_terminal_capabilities,
)
from textcharts.box_plot import BoxPlot, BoxPlotSeries
from textcharts.box_plot import from_series as box_from_series
from textcharts.comparison_bar import ComparisonBar, ComparisonBarData
from textcharts.comparison_bar import from_data as comparison_from_data
from textcharts.diverging_bar import DivergingBar, DivergingBarData
from textcharts.diverging_bar import from_data as diverging_from_data
from textcharts.heatmap import Heatmap, from_matrix
from textcharts.histogram import Histogram, HistogramBar
from textcharts.histogram import from_data as histogram_from_data
from textcharts.line_chart import LineChart, LinePoint
from textcharts.line_chart import from_points as line_from_points
from textcharts.scatter_plot import ScatterPlot, ScatterPoint
from textcharts.scatter_plot import from_points as scatter_from_points
from textcharts.summary_box import SummaryBox, SummaryStats


class TestTerminalCapabilities:
    """Tests for terminal capability detection."""

    def test_detect_capabilities_returns_valid_object(self):
        """Capabilities detection returns a valid object."""
        caps = detect_terminal_capabilities()
        assert caps.width >= 40
        assert caps.height >= 10
        assert isinstance(caps.color_mode, ColorMode)
        assert isinstance(caps.unicode_support, bool)

    def test_color_mode_enum_values(self):
        """ColorMode enum has expected values."""
        assert ColorMode.NONE.value == "none"
        assert ColorMode.BASIC.value == "basic"
        assert ColorMode.EXTENDED.value == "extended"
        assert ColorMode.TRUECOLOR.value == "truecolor"


class TestTerminalColors:
    """Tests for terminal color utilities."""

    def test_colors_disabled_returns_empty(self):
        """Colors disabled returns empty strings."""
        colors = TerminalColors(color_mode=ColorMode.NONE)
        assert colors.fg("#ff0000") == ""
        assert colors.bg("#ff0000") == ""
        assert colors.reset() == ""

    def test_colors_basic_mode(self):
        """Basic color mode uses 16-color codes."""
        colors = TerminalColors(color_mode=ColorMode.BASIC)
        fg = colors.fg(2)  # Green
        assert "\033[" in fg
        assert "32" in fg or "38" in fg

    def test_colors_extended_mode(self):
        """Extended color mode uses 256-color codes."""
        colors = TerminalColors(color_mode=ColorMode.EXTENDED)
        fg = colors.fg("#1b9e77")
        assert "\033[38;5;" in fg

    def test_colorize_applies_colors(self):
        """Colorize wraps text with escape codes."""
        colors = TerminalColors(color_mode=ColorMode.EXTENDED)
        result = colors.colorize("test", fg_color="#ff0000")
        assert "test" in result
        assert "\033[" in result
        assert colors.RESET in result

    def test_colorize_no_color_passthrough(self):
        """Colorize with no color mode returns original text."""
        colors = TerminalColors(color_mode=ColorMode.NONE)
        result = colors.colorize("test", fg_color="#ff0000")
        assert result == "test"


class TestChartOptions:
    """Tests for chart options."""

    def test_default_options(self):
        """Default options are reasonable."""
        opts = ChartOptions()
        assert opts.use_color is True
        assert opts.use_unicode is True
        assert opts.width is None  # Auto-detect

    def test_effective_width_with_explicit(self):
        """Effective width uses explicit value when set."""
        opts = ChartOptions(width=100)
        assert opts.get_effective_width() == 100

    def test_effective_width_auto(self):
        """Effective width auto-detects when not set."""
        opts = ChartOptions()
        width = opts.get_effective_width()
        assert width >= 40  # Minimum

    def test_block_chars_unicode(self):
        """Block chars returns Unicode when enabled."""
        opts = ChartOptions(use_unicode=True)
        h_blocks = opts.get_horizontal_block_chars()
        v_blocks = opts.get_vertical_block_chars()
        assert "█" in h_blocks
        assert "█" in v_blocks
        assert "▏" in h_blocks
        assert "▂" in v_blocks

    def test_block_chars_ascii_fallback(self):
        """Block chars returns ASCII when Unicode disabled."""
        opts = ChartOptions(use_unicode=False)
        blocks = opts.get_horizontal_block_chars()
        assert "█" not in blocks
        assert "#" in blocks


class TestBarChart:
    """Tests for bar chart rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        chart = BarChart(data=[])
        result = chart.render()
        assert "No data" in result

    def test_single_bar(self):
        """Single bar renders correctly."""
        data = [BarData(label="Test", value=100)]
        chart = BarChart(data=data, title="Test Chart")
        result = chart.render()
        assert "Test" in result
        assert "100" in result

    def test_multiple_bars_sorted(self):
        """Multiple bars are sorted by value."""
        data = [
            BarData(label="Low", value=10),
            BarData(label="High", value=100),
            BarData(label="Mid", value=50),
        ]
        chart = BarChart(data=data, sort_by="value")
        result = chart.render()
        lines = result.split("\n")

        # Find data lines (contain bar characters, exclude legend)
        bar_char = "█"
        data_lines = [line for line in lines if ("High" in line or "Mid" in line or "Low" in line) and bar_char in line]
        assert len(data_lines) == 3

        # High should come before Low in sorted output
        high_idx = next(i for i, line in enumerate(data_lines) if "High" in line)
        low_idx = next(i for i, line in enumerate(data_lines) if "Low" in line)
        assert high_idx < low_idx

    def test_best_worst_highlighting(self):
        """Best/worst items are marked."""
        data = [
            BarData(label="Best", value=100, is_best=True),
            BarData(label="Worst", value=10, is_worst=True),
        ]
        chart = BarChart(data=data)
        result = chart.render()
        assert "Best" in result
        assert "Worst" in result

    def test_grouped_bars(self):
        """Grouped bars show legend with group names."""
        data = [
            BarData(label="A", value=100, group="Group1"),
            BarData(label="B", value=80, group="Group2"),
        ]
        chart = BarChart(data=data)
        result = chart.render()
        assert "Group1" in result
        assert "Group2" in result

    def test_bar_from_data_factory(self):
        """Factory function accepts BarData objects."""
        data = [BarData(label="Test", value=50)]
        chart = bar_from_data(data, title="Factory Test")
        result = chart.render()
        assert "Test" in result
        assert "50" in result


class TestBoxPlot:
    """Tests for box plot rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        chart = BoxPlot(series=[])
        result = chart.render()
        assert "No data" in result

    def test_single_series(self):
        """Single series renders with statistics."""
        series = [BoxPlotSeries(name="Test", values=[10, 20, 30, 40, 50])]
        chart = BoxPlot(series=series, show_stats=True)
        result = chart.render()
        assert "Test" in result
        assert "median" in result
        assert "30" in result  # Median of 10-50

    def test_multiple_series(self):
        """Multiple series render side by side."""
        series = [
            BoxPlotSeries(name="Series1", values=[10, 20, 30]),
            BoxPlotSeries(name="Series2", values=[40, 50, 60]),
        ]
        chart = BoxPlot(series=series)
        result = chart.render()
        assert "Series1" in result
        assert "Series2" in result

    def test_outliers_shown(self):
        """Outliers are indicated."""
        # Add outliers far from the main distribution
        values = [10, 11, 12, 13, 14, 15, 100]  # 100 is an outlier
        series = [BoxPlotSeries(name="Test", values=values)]
        chart = BoxPlot(series=series)
        result = chart.render()
        assert "o" in result  # Outlier marker

    def test_outliers_respect_width_constraint(self):
        """Outliers don't cause lines to exceed max width."""
        # Create data with many outliers
        values = [10, 20, 21, 22, 23, 24, 25, 100, 110, 120, 130, 140, 150, 160, 170]
        series = [BoxPlotSeries(name="TestPlatform", values=values)]
        opts = ChartOptions(width=80, use_color=False)
        chart = BoxPlot(series=series, options=opts)
        result = chart.render()

        # Verify no line exceeds the width constraint
        for line in result.split("\n"):
            assert len(line) <= 80, f"Line exceeds width: len={len(line)}, line='{line}'"

    def test_box_from_series_factory(self):
        """Factory function accepts BoxPlotSeries objects."""
        series = [BoxPlotSeries(name="Test", values=[1, 2, 3, 4, 5])]
        chart = box_from_series(series)
        result = chart.render()
        assert "Test" in result


class TestHeatmap:
    """Tests for heatmap rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        chart = Heatmap(matrix=[], row_labels=[], col_labels=[])
        result = chart.render()
        assert "No data" in result

    def test_simple_matrix(self):
        """Simple matrix renders correctly."""
        matrix = [[10, 20], [30, 40]]
        chart = Heatmap(
            matrix=matrix,
            row_labels=["Q1", "Q2"],
            col_labels=["DuckDB", "Polars"],
            title="Test Heatmap",
        )
        result = chart.render()
        assert "Q1" in result
        assert "Q2" in result
        assert "DuckDB" in result
        assert "Polars" in result

    def test_scale_legend(self):
        """Scale legend is shown."""
        matrix = [[10, 100]]
        chart = Heatmap(
            matrix=matrix,
            row_labels=["Q1"],
            col_labels=["A", "B"],
        )
        result = chart.render()
        assert "Scale" in result
        assert "fast" in result or "slow" in result

    def test_from_matrix_factory(self):
        """Factory function creates heatmap."""
        matrix = [[1, 2], [3, 4]]
        chart = from_matrix(
            matrix=matrix,
            queries=["Q1", "Q2"],
            platforms=["A", "B"],
        )
        result = chart.render()
        assert "Q1" in result

    def test_no_color_heatmap_uses_column_separators(self):
        """No-color heatmap includes explicit separators between data columns."""
        matrix = [[34, 40], [83, 94]]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Heatmap(matrix=matrix, row_labels=["Q1", "Q2"], col_labels=["A", "B"], options=opts)
        result = chart.render()
        q1_line = next(line for line in result.splitlines() if "Q1" in line)
        assert q1_line.count("│") >= 2

    def test_no_color_heatmap_right_aligns_values_with_density_fill(self):
        """No-color heatmap right-aligns values and fills cell area with intensity chars."""
        matrix = [[50, 140], [20, 80]]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Heatmap(matrix=matrix, row_labels=["Q1", "Q2"], col_labels=["A", "B"], options=opts)
        result = chart.render()
        q1_line = next(line for line in result.splitlines() if "Q1" in line)
        assert "░" in q1_line or "▒" in q1_line or "▓" in q1_line or "█" in q1_line
        assert "50" in q1_line
        assert "140" in q1_line

    def test_no_color_heatmap_cells_are_fixed_width_with_value_spacing(self):
        """No-color heatmap keeps equal cell widths and a separator space before numbers."""
        matrix = [[34, 140], [83, 94]]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Heatmap(matrix=matrix, row_labels=["Q1", "Q2"], col_labels=["A", "B"], options=opts)
        result = chart.render()
        q1_line = next(line for line in result.splitlines() if "Q1" in line)

        data_region = q1_line.split("│", 1)[1]
        cells = [c for c in data_region.split("│") if c.strip()]
        assert len(cells) == 2
        assert len(cells[0]) == len(cells[1])
        assert " 34" in cells[0]
        assert " 140" in cells[1]

    def test_height_constrained_heatmap_shows_row_truncation_indicator(self):
        """Row truncation indicator is shown when options.height limits visible rows."""
        matrix = [[float(i), float(i + 1)] for i in range(12)]
        rows = [f"Q{i}" for i in range(12)]
        opts = ChartOptions(use_color=False, use_unicode=True, height=12)
        chart = Heatmap(matrix=matrix, row_labels=rows, col_labels=["A", "B"], options=opts)
        result = chart.render()
        assert "more rows" in result


class TestScatterPlot:
    """Tests for scatter plot rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        chart = ScatterPlot(points=[])
        result = chart.render()
        assert "No data" in result

    def test_single_point(self):
        """Single point renders."""
        points = [ScatterPoint(name="Test", x=50, y=100)]
        chart = ScatterPlot(points=points)
        result = chart.render()
        assert "Test" in result
        # Single point is on Pareto frontier, so uses Pareto marker
        assert "◆" in result or "*" in result  # Marker

    def test_pareto_frontier(self):
        """Pareto frontier is computed and shown."""
        points = [
            ScatterPoint(name="Efficient", x=10, y=100),  # Low cost, high perf = Pareto
            ScatterPoint(name="Inefficient", x=100, y=50),  # High cost, low perf = Not Pareto
        ]
        chart = ScatterPlot(points=points, show_pareto=True)
        result = chart.render()
        assert "Pareto" in result
        assert "Efficient" in result

    def test_scatter_from_points_factory(self):
        """Factory function accepts ScatterPoint objects."""
        points = [ScatterPoint(name="Test", x=50, y=100)]
        chart = scatter_from_points(points)
        result = chart.render()
        assert "Test" in result


class TestLineChart:
    """Tests for line chart rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        chart = LineChart(points=[])
        result = chart.render()
        assert "No data" in result

    def test_single_series(self):
        """Single series renders."""
        points = [
            LinePoint(series="Test", x=1, y=10),
            LinePoint(series="Test", x=2, y=20),
            LinePoint(series="Test", x=3, y=30),
        ]
        chart = LineChart(points=points)
        result = chart.render()
        assert "Test" in result
        assert "*" in result  # Default marker

    def test_multiple_series(self):
        """Multiple series use different markers."""
        points = [
            LinePoint(series="A", x=1, y=10),
            LinePoint(series="A", x=2, y=20),
            LinePoint(series="B", x=1, y=15),
            LinePoint(series="B", x=2, y=25),
        ]
        chart = LineChart(points=points)
        result = chart.render()
        assert "A" in result
        assert "B" in result
        assert "*" in result  # Marker for A
        assert "+" in result  # Marker for B

    def test_trend_line(self):
        """Trend line can be shown."""
        points = [
            LinePoint(series="Test", x=1, y=10),
            LinePoint(series="Test", x=2, y=20),
            LinePoint(series="Test", x=3, y=30),
            LinePoint(series="Test", x=4, y=40),
        ]
        chart = LineChart(points=points, show_trend=True)
        result = chart.render()
        # Trend line uses '.' markers
        assert "." in result

    def test_line_from_points_factory(self):
        """Factory function accepts LinePoint objects."""
        points = [
            LinePoint(series="Test", x="Run1", y=100),
            LinePoint(series="Test", x="Run2", y=110),
        ]
        chart = line_from_points(points)
        result = chart.render()
        assert "Test" in result


class TestNoColorOutput:
    """Tests for output without colors."""

    def test_bar_chart_no_color(self):
        """Bar chart renders without colors."""
        data = [BarData(label="Test", value=100)]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert "\033[" not in result  # No ANSI codes
        assert "Test" in result

    def test_heatmap_no_color(self):
        """Heatmap renders with intensity chars when no color."""
        matrix = [[10, 100]]
        opts = ChartOptions(use_color=False)
        chart = Heatmap(
            matrix=matrix,
            row_labels=["Q1"],
            col_labels=["A", "B"],
            options=opts,
        )
        result = chart.render()
        assert "\033[" not in result


class TestASCIIOnlyOutput:
    """Tests for output without Unicode characters."""

    def test_bar_chart_ascii_only(self):
        """Bar chart renders with ASCII only."""
        data = [BarData(label="Test", value=100)]
        opts = ChartOptions(use_unicode=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert "█" not in result
        # ASCII_BLOCK_CHARS = " .-=+#@" - '@' is the full block
        assert "@" in result or "#" in result or "=" in result

    def test_box_plot_ascii_only(self):
        """Box plot renders with ASCII only."""
        series = [BoxPlotSeries(name="Test", values=[10, 20, 30])]
        opts = ChartOptions(use_unicode=False)
        chart = BoxPlot(series=series, options=opts)
        result = chart.render()
        # Should use ASCII box drawing
        assert "+" in result or "-" in result or "|" in result


class TestHistogram:
    """Tests for query latency histogram rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        chart = Histogram(data=[])
        result = chart.render()
        assert "No data" in result

    def test_single_query(self):
        """Single query renders correctly."""
        data = [HistogramBar(label="Q1", value=100)]
        chart = Histogram(data=data, title="Test Histogram")
        result = chart.render()
        assert "Q1" in result
        assert "Test Histogram" in result

    def test_multiple_queries(self):
        """Multiple queries render with bars."""
        data = [
            HistogramBar(label="Q1", value=100),
            HistogramBar(label="Q2", value=200),
            HistogramBar(label="Q3", value=150),
        ]
        chart = Histogram(data=data)
        result = chart.render()
        assert "Q1" in result
        assert "Q2" in result
        assert "Q3" in result

    def test_natural_sort_order(self):
        """Query IDs are sorted naturally (Q1, Q2, Q10 not Q1, Q10, Q2)."""
        data = [
            HistogramBar(label="Q10", value=100),
            HistogramBar(label="Q2", value=200),
            HistogramBar(label="Q1", value=150),
        ]
        chart = Histogram(data=data, sort_by="label")
        result = chart.render()
        lines = result.split("\n")
        # Find the label line (has Q1, Q2, Q10)
        label_line = [line for line in lines if "Q1" in line and "Q2" in line and "Q10" in line]
        assert len(label_line) == 1
        # Q1 should appear before Q2 which should appear before Q10
        line = label_line[0]
        assert line.index("Q1") < line.index("Q2") < line.index("Q10")

    def test_sort_by_latency(self):
        """Queries can be sorted by latency."""
        data = [
            HistogramBar(label="Q1", value=100),
            HistogramBar(label="Q2", value=300),
            HistogramBar(label="Q3", value=200),
        ]
        chart = Histogram(data=data, sort_by="value")
        result = chart.render()
        # With value sort (descending), Q2 (300) should come first
        assert "Q2" in result

    def test_best_worst_highlighting(self):
        """Best/worst queries are marked."""
        data = [
            HistogramBar(label="Q1", value=100, is_best=True),
            HistogramBar(label="Q2", value=300, is_worst=True),
        ]
        chart = Histogram(data=data)
        result = chart.render()
        # Should have legend for best/worst
        assert "Best" in result
        assert "Worst" in result

    def test_mean_line_shown(self):
        """Mean line annotation is shown."""
        data = [
            HistogramBar(label="Q1", value=100),
            HistogramBar(label="Q2", value=200),
        ]
        chart = Histogram(data=data, show_mean_line=True)
        result = chart.render()
        assert "Mean" in result

    def test_mean_line_hidden(self):
        """Mean line can be hidden."""
        data = [
            HistogramBar(label="Q1", value=100),
            HistogramBar(label="Q2", value=200),
        ]
        chart = Histogram(data=data, show_mean_line=False)
        result = chart.render()
        assert "Mean" not in result

    def test_chart_splitting_for_large_datasets(self):
        """Charts split when queries exceed max_per_chart."""
        # Create 40 queries (more than default 33)
        data = [HistogramBar(label=f"Q{i}", value=i * 10) for i in range(1, 41)]
        chart = Histogram(data=data, max_per_chart=33)
        result = chart.render()
        # Should have two chart sections with query ID range labels
        assert "Q1-Q33" in result
        assert "Q34-Q40" in result

    def test_chart_splitting_large_benchmark(self):
        """TPC-DS-like benchmark (99 queries) splits into 3 charts."""
        data = [HistogramBar(label=f"Q{i}", value=i * 5) for i in range(1, 100)]
        chart = Histogram(data=data, max_per_chart=33)
        result = chart.render()
        # Should have three chart sections
        assert "Q1-Q33" in result
        assert "Q34-Q66" in result
        assert "Q67-Q99" in result

    def test_no_splitting_for_small_datasets(self):
        """No splitting when queries fit in one chart."""
        data = [HistogramBar(label=f"Q{i}", value=i * 10) for i in range(1, 23)]
        chart = Histogram(data=data, max_per_chart=33)
        result = chart.render()
        # Should not have range labels
        assert "Queries 1-" not in result

    def test_histogram_from_data_factory(self):
        """Factory function accepts HistogramBar objects."""
        data = [HistogramBar(label="Q1", value=150)]
        chart = histogram_from_data(data, title="Factory Test")
        result = chart.render()
        assert "Q1" in result
        assert "Factory Test" in result

    def test_multi_platform_renders_with_legend(self):
        """Multi-platform data renders grouped bars with platform legend."""
        data = [
            HistogramBar(label="Q1", value=100, platform="DuckDB"),
            HistogramBar(label="Q1", value=150, platform="Polars"),
            HistogramBar(label="Q2", value=200, platform="DuckDB"),
            HistogramBar(label="Q2", value=250, platform="Polars"),
        ]
        chart = Histogram(data=data)
        result = chart.render()
        assert "Q1" in result
        assert "Q2" in result
        # Platform legend should be present
        assert "DuckDB" in result
        assert "Polars" in result

    def test_multi_platform_preserves_platform_colors(self):
        """Multi-platform histogram uses platform colors, not best/worst override."""
        data = [
            HistogramBar(label="Q1", value=50, platform="DuckDB", is_best=True),
            HistogramBar(label="Q1", value=60, platform="Polars", is_best=True),
            HistogramBar(label="Q2", value=300, platform="DuckDB", is_worst=True),
            HistogramBar(label="Q2", value=350, platform="Polars", is_worst=True),
        ]
        chart = Histogram(data=data)
        result = chart.render()
        # Platform names should appear in legend, but not Best/Worst (color override removed)
        assert "DuckDB" in result
        assert "Polars" in result
        assert "Best" not in result
        assert "Worst" not in result

    def test_multi_platform_splitting(self):
        """Multi-platform data splits by unique query count, not total bar count."""
        # 10 queries x 2 platforms = 20 bars, but only 10 unique queries
        data = []
        for i in range(1, 11):
            data.append(HistogramBar(label=f"Q{i}", value=i * 10, platform="A"))
            data.append(HistogramBar(label=f"Q{i}", value=i * 15, platform="B"))
        chart = Histogram(data=data, max_per_chart=5)
        result = chart.render()
        # Should split into 2 charts of 5 queries each, not by 20 bars
        assert "Q1-Q5" in result
        assert "Q6-Q10" in result

    def test_no_color_output(self):
        """Histogram renders without colors."""
        data = [HistogramBar(label="Q1", value=100)]
        opts = ChartOptions(use_color=False)
        chart = Histogram(data=data, options=opts)
        result = chart.render()
        assert "\033[" not in result  # No ANSI codes
        assert "Q1" in result

    def test_compact_labels_do_not_collapse_multi_digit_query_ids(self):
        """Narrow bars should keep multi-digit query IDs distinguishable."""
        data = [HistogramBar(label=f"Q{i}", value=float(i)) for i in range(10, 20)]
        opts = ChartOptions(use_color=False)
        opts.width = 46  # Force narrow bar widths and compact labels.
        chart = Histogram(data=data, options=opts)
        result = chart.render()
        assert "10" in result
        assert "11" in result
        assert "19" in result
        assert "Q1 Q1 Q1" not in result


# ── Edge Case Tests ───────────────────────────────────────────────


class TestComparisonBar:
    """Tests for paired comparison bar chart rendering."""

    def test_empty_data(self):
        """Empty data returns message."""

        chart = ComparisonBar(data=[])
        result = chart.render()
        assert "No data" in result

    def test_single_query_comparison(self):
        """Single query renders both bars with percentage annotation."""

        data = [
            ComparisonBarData(
                label="Q1",
                baseline_value=100,
                comparison_value=75,
                baseline_name="SQL",
                comparison_name="DF",
            )
        ]
        chart = ComparisonBar(data=data, title="Test Comparison")
        result = chart.render()
        assert "Q1" in result
        assert "SQL" in result
        assert "DF" in result
        assert "100" in result
        assert "75" in result
        assert "Test Comparison" in result

    def test_percentage_change_annotation(self):
        """Percentage change is shown for non-trivial differences."""

        data = [
            ComparisonBarData(
                label="Q1",
                baseline_value=100,
                comparison_value=50,
                baseline_name="A",
                comparison_name="B",
            )
        ]
        opts = ChartOptions(use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        assert "-50.0%" in result

    def test_regression_annotation(self):
        """Positive percentage (regression) is annotated."""

        data = [
            ComparisonBarData(
                label="Q1",
                baseline_value=100,
                comparison_value=150,
                baseline_name="A",
                comparison_name="B",
            )
        ]
        opts = ChartOptions(use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        assert "+50.0%" in result

    def test_stable_no_annotation(self):
        """Near-zero percentage change shows no annotation."""

        data = [
            ComparisonBarData(
                label="Q1",
                baseline_value=100,
                comparison_value=101,
                baseline_name="A",
                comparison_name="B",
            )
        ]
        opts = ChartOptions(use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        # 1% change should not show annotation (below 2% threshold)
        assert "%" not in result.split("\n")[-3]  # Check comparison bar line only

    def test_multiple_queries(self):
        """Multiple queries render as separate pairs."""

        data = [
            ComparisonBarData(label="Q1", baseline_value=100, comparison_value=80),
            ComparisonBarData(label="Q2", baseline_value=200, comparison_value=250),
            ComparisonBarData(label="Q3", baseline_value=50, comparison_value=50),
        ]
        chart = ComparisonBar(data=data)
        result = chart.render()
        assert "Q1" in result
        assert "Q2" in result
        assert "Q3" in result

    def test_no_color_output(self):
        """Comparison bar renders without ANSI codes when color disabled."""

        data = [ComparisonBarData(label="Q1", baseline_value=100, comparison_value=50)]
        opts = ChartOptions(use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        assert "\033[" not in result

    def test_ascii_only_output(self):
        """Comparison bar renders with ASCII fallback characters."""

        data = [ComparisonBarData(label="Q1", baseline_value=100, comparison_value=50)]
        opts = ChartOptions(use_unicode=False, use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        assert "\u2588" not in result  # No Unicode full block
        assert "~" in result  # ASCII approx symbol

    def test_zero_baseline_no_crash(self):
        """Zero baseline value does not cause division by zero."""

        data = [ComparisonBarData(label="Q1", baseline_value=0, comparison_value=50)]
        opts = ChartOptions(use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        assert "Q1" in result

    def test_scale_note_shown(self):
        """Scale note appears at bottom of chart."""

        data = [ComparisonBarData(label="Q1", baseline_value=100, comparison_value=50)]
        opts = ChartOptions(use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        assert "each" in result

    def test_comparison_from_data_factory(self):
        """Factory function creates chart from ComparisonBarData."""

        data = [ComparisonBarData(label="Q1", baseline_value=100, comparison_value=75)]
        chart = comparison_from_data(data, title="Factory Test")
        result = chart.render()
        assert "Q1" in result
        assert "Factory Test" in result

    def test_comparison_from_data_factory_unknown_type(self, caplog):
        """Factory warns on unknown types."""
        import logging


        with caplog.at_level(logging.WARNING, logger="textcharts.comparison_bar"):
            comparison_from_data([{"label": "Q1", "baseline_value": 100, "comparison_value": 50}])
        assert "unexpected type" in caplog.text


# ── Diverging Bar Chart Tests ────────────────────────────────────


class TestDivergingBar:
    """Tests for diverging bar chart rendering."""

    def test_empty_data(self):
        """Empty data returns message."""

        chart = DivergingBar(data=[])
        result = chart.render()
        assert "No data" in result

    def test_improvements_and_regressions(self):
        """Chart shows both improvements and regressions."""

        data = [
            DivergingBarData(label="Q1", pct_change=-30.0),
            DivergingBarData(label="Q2", pct_change=+20.0),
            DivergingBarData(label="Q3", pct_change=-5.0),
        ]
        opts = ChartOptions(use_color=False)
        chart = DivergingBar(data=data, options=opts)
        result = chart.render()
        assert "Q1" in result
        assert "Q2" in result
        assert "Q3" in result
        assert "-30.0%" in result
        assert "+20.0%" in result
        assert "Faster" in result
        assert "Slower" in result

    def test_sorted_by_magnitude(self):
        """Items are sorted: improvements first (most negative), then regressions."""

        data = [
            DivergingBarData(label="Q1", pct_change=-10.0),
            DivergingBarData(label="Q2", pct_change=-50.0),
            DivergingBarData(label="Q3", pct_change=+30.0),
        ]
        opts = ChartOptions(use_color=False)
        chart = DivergingBar(data=data, options=opts)
        result = chart.render()
        lines = result.split("\n")
        # Q2 (-50%) should come before Q1 (-10%) in the sorted output
        q2_line = next(i for i, line in enumerate(lines) if "Q2" in line)
        q1_line = next(i for i, line in enumerate(lines) if "Q1" in line)
        assert q2_line < q1_line

    def test_overflow_arrows_for_extreme_outliers(self):
        """Extreme outliers show overflow arrows."""

        data = [
            DivergingBarData(label="Q1", pct_change=-10.0),
            DivergingBarData(label="Q2", pct_change=+726.0),  # Extreme outlier
        ]
        opts = ChartOptions(use_color=False)
        chart = DivergingBar(data=data, clip_pct=200.0, options=opts)
        result = chart.render()
        assert "+726.0%" in result
        # Should have overflow indicator
        assert "\u25ba" in result or ">" in result

    def test_all_improvements(self):
        """Chart handles all-improvement data."""

        data = [
            DivergingBarData(label="Q1", pct_change=-20.0),
            DivergingBarData(label="Q2", pct_change=-10.0),
        ]
        opts = ChartOptions(use_color=False)
        chart = DivergingBar(data=data, options=opts)
        result = chart.render()
        assert "2 improved" in result
        assert "0 regressed" in result

    def test_all_regressions(self):
        """Chart handles all-regression data."""

        data = [
            DivergingBarData(label="Q1", pct_change=+20.0),
            DivergingBarData(label="Q2", pct_change=+40.0),
        ]
        opts = ChartOptions(use_color=False)
        chart = DivergingBar(data=data, options=opts)
        result = chart.render()
        assert "0 improved" in result
        assert "2 regressed" in result

    def test_no_color_output(self):
        """Diverging bar renders without ANSI codes when color disabled."""

        data = [DivergingBarData(label="Q1", pct_change=-25.0)]
        opts = ChartOptions(use_color=False)
        chart = DivergingBar(data=data, options=opts)
        result = chart.render()
        assert "\033[" not in result

    def test_ascii_only_output(self):
        """Diverging bar renders with ASCII fallback characters."""

        data = [
            DivergingBarData(label="Q1", pct_change=-30.0),
            DivergingBarData(label="Q2", pct_change=+300.0),
        ]
        opts = ChartOptions(use_unicode=False, use_color=False)
        chart = DivergingBar(data=data, clip_pct=200.0, options=opts)
        result = chart.render()
        # ASCII overflow arrow
        assert "-->" in result or ">" in result
        # No Unicode box chars
        assert "\u2502" not in result

    def test_summary_counts(self):
        """Summary line shows correct counts."""

        data = [
            DivergingBarData(label="Q1", pct_change=-30.0),
            DivergingBarData(label="Q2", pct_change=+1.0),  # Stable (< 2%)
            DivergingBarData(label="Q3", pct_change=+20.0),
        ]
        opts = ChartOptions(use_color=False)
        chart = DivergingBar(data=data, options=opts)
        result = chart.render()
        assert "1 improved" in result
        assert "1 stable" in result
        assert "1 regressed" in result

    def test_single_item(self):
        """Single item renders without crash."""

        data = [DivergingBarData(label="Q1", pct_change=-15.0)]
        opts = ChartOptions(use_color=False)
        chart = DivergingBar(data=data, options=opts)
        result = chart.render()
        assert "Q1" in result
        assert "-15.0%" in result

    def test_diverging_from_data_factory(self):
        """Factory function creates chart from DivergingBarData."""

        data = [DivergingBarData(label="Q1", pct_change=-25.0)]
        chart = diverging_from_data(data, title="Factory Test")
        result = chart.render()
        assert "Q1" in result
        assert "Factory Test" in result

    def test_diverging_from_data_factory_unknown_type(self, caplog):
        """Factory warns on unknown types."""
        import logging


        with caplog.at_level(logging.WARNING, logger="textcharts.diverging_bar"):
            diverging_from_data([{"label": "Q1", "pct_change": -10}])
        assert "unexpected type" in caplog.text


# ── Summary Box Tests ────────────────────────────────────────────


class TestSummaryBox:
    """Tests for summary box rendering."""

    def test_single_run_summary(self):
        """Single-run summary shows basic metrics."""

        stats = SummaryStats(
            title="DuckDB Summary",
            primary_value=142.3,
            total_value=3200,
            num_items=22,
        )
        opts = ChartOptions(use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert "DuckDB Summary" in result
        assert "142.3" in result
        assert "3.2s" in result
        assert "22" in result
        # Box borders present
        assert "\u250c" in result or "+" in result

    def test_single_run_best_worst_shows_time_units(self):
        """Single-run best/worst values should include ms/s units."""

        stats = SummaryStats(
            title="Unit Test",
            primary_value=100.0,
            total_value=500.0,
            num_items=3,
            best_items=[("Q6", 8.0), ("Q14", 12.5)],
            worst_items=[("Q18", 302.0), ("Q21", 1500.0)],
        )
        opts = ChartOptions(use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        # Best values should have ms unit
        assert "Q6 (8.0ms)" in result
        assert "Q14 (12.5ms)" in result
        # Worst values should have appropriate units
        assert "Q18 (302.0ms)" in result
        assert "Q21 (1.5s)" in result

    def test_comparison_summary(self):
        """Comparison summary shows both runs and percentage change."""

        stats = SummaryStats(
            title="SQL vs DF Summary",
            primary_baseline=142.3,
            primary_comparison=98.7,
            total_baseline=3200,
            total_comparison=2100,
            baseline_name="SQL",
            comparison_name="DF",
            num_items=22,
            num_improved=5,
            num_stable=12,
            num_regressed=5,
            best_items=[("Q6", -57.2), ("Q14", -38.1)],
            worst_items=[("Q21", 726.0), ("Q17", 23.4)],
        )
        opts = ChartOptions(use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert "SQL vs DF Summary" in result
        assert "Primary" in result
        assert "142.3" in result
        assert "98.7" in result
        assert "5 improved" in result
        assert "12 stable" in result
        assert "5 regressed" in result
        assert "Q6" in result
        assert "Q21" in result

    def test_box_borders(self):
        """Summary box has proper Unicode borders."""

        stats = SummaryStats(title="Test", primary_value=100)
        opts = ChartOptions(use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        # Check box drawing characters
        assert "\u250c" in result  # top-left corner
        assert "\u2510" in result  # top-right corner
        assert "\u2514" in result  # bottom-left corner
        assert "\u2518" in result  # bottom-right corner
        assert "\u2502" in result  # vertical line

    def test_ascii_only_borders(self):
        """Summary box uses ASCII borders when Unicode disabled."""

        stats = SummaryStats(title="Test", primary_value=100)
        opts = ChartOptions(use_unicode=False, use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert "+" in result  # ASCII corners
        assert "|" in result  # ASCII vertical
        assert "-" in result  # ASCII horizontal

    def test_no_color_output(self):
        """Summary box renders without ANSI codes when color disabled."""

        stats = SummaryStats(
            title="Test",
            primary_baseline=100,
            primary_comparison=80,
            num_improved=3,
            num_stable=1,
            num_regressed=1,
        )
        opts = ChartOptions(use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert "\033[" not in result

    def test_time_formatting_minutes(self):
        """Large times are formatted as minutes."""

        stats = SummaryStats(title="Test", total_value=120_000)
        opts = ChartOptions(use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert "2.0min" in result

    def test_time_formatting_seconds(self):
        """Medium times are formatted as seconds."""

        stats = SummaryStats(title="Test", total_value=5500)
        opts = ChartOptions(use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert "5.5s" in result

    def test_time_formatting_milliseconds(self):
        """Small times stay as milliseconds."""

        stats = SummaryStats(title="Test", total_value=42.5)
        opts = ChartOptions(use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert "42.5ms" in result

    def test_empty_best_worst(self):
        """Summary box renders fine without best/worst queries."""

        stats = SummaryStats(title="Test", primary_value=100, num_items=5)
        opts = ChartOptions(use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert "Best" not in result
        assert "Worst" not in result

    def test_long_title_does_not_overflow_box_width(self):
        """Very long titles are truncated to fit the configured width."""

        width = 80
        stats = SummaryStats(title="X" * 200, primary_value=100)
        opts = ChartOptions(width=width, use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        for line in result.splitlines():
            assert len(line) == width

    def test_long_best_worst_text_does_not_overflow_box_width(self):
        """Best/worst rows are truncated to preserve box borders."""

        width = 80
        stats = SummaryStats(
            title="Summary",
            primary_baseline=100,
            primary_comparison=130,
            total_baseline=4000,
            total_comparison=3000,
            num_items=3,
            num_improved=1,
            num_stable=1,
            num_regressed=1,
            best_items=[
                ("aggregation_groupby_large", -12.2),
                ("exchange_merge_join_extremely_verbose_name", -10.0),
                ("read_parquet_single", -9.2),
            ],
            worst_items=[("another_extremely_verbose_query_identifier_name", 55.0)],
        )
        opts = ChartOptions(width=width, use_color=False, use_unicode=True)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        for line in result.splitlines():
            assert len(line) == width

    def test_two_column_mode_includes_percentage_deltas(self):
        """Two-column summary mode keeps percentage deltas visible."""

        stats = SummaryStats(
            title="Summary",
            primary_baseline=100,
            primary_comparison=130,
            total_baseline=4000,
            total_comparison=3000,
            num_items=22,
            environment={"OS": "macOS", "Python": "3.12.2", "CPUs": "10", "Memory": "16GB"},
        )
        opts = ChartOptions(width=120, use_color=False, use_unicode=True)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert "+30.0%" in result
        assert "-25.0%" in result

    def test_two_column_mode_colorizes_percentage_deltas_when_color_enabled(self):
        """Two-column mode keeps colored percentage deltas when color output is enabled."""

        stats = SummaryStats(
            title="Summary",
            primary_baseline=100,
            primary_comparison=130,
            total_baseline=4000,
            total_comparison=3000,
            num_items=22,
            environment={"OS": "macOS", "Python": "3.12.2"},
        )
        opts = ChartOptions(width=120, use_color=True, use_unicode=True)
        _caps = TerminalCapabilities(color_mode=ColorMode.EXTENDED)
        with patch("textcharts.base.detect_terminal_capabilities", return_value=_caps):
            chart = SummaryBox(stats=stats, options=opts)
            result = chart.render()
        assert "+30.0%" in result
        assert "-25.0%" in result
        assert "\033[" in result


# ── Integration Tests ────────────────────────────────────────────
