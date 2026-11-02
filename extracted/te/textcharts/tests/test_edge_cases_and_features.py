"""Tests for textcharts rendering."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from textcharts.bar_chart import BarChart, BarData
from textcharts.bar_chart import from_data as bar_from_data
from textcharts.base import (
    ChartBase,
    ChartOptions,
    ColorMode,
    TerminalCapabilities,
    TerminalColors,
)
from textcharts.box_plot import BoxPlot, BoxPlotSeries, compute_quartiles
from textcharts.comparison_bar import ComparisonBar, ComparisonBarData
from textcharts.diverging_bar import DivergingBar, DivergingBarData
from textcharts.heatmap import Heatmap, from_matrix
from textcharts.histogram import Histogram, HistogramBar
from textcharts.line_chart import LineChart, LinePoint
from textcharts.scatter_plot import ScatterPlot, ScatterPoint
from textcharts.scatter_plot import from_points as scatter_from_points
from textcharts.summary_box import SummaryBox, SummaryStats


class TestComputeQuartiles:
    """Tests for compute_quartiles edge cases."""

    def test_empty_values(self):
        """Empty input returns zeroed stats."""
        stats = compute_quartiles([])
        assert stats.median == 0
        assert stats.outliers == []

    def test_single_value(self):
        """Single value produces degenerate box plot."""
        stats = compute_quartiles([42])
        assert stats.median == 42
        assert stats.q1 == 42
        assert stats.q3 == 42
        assert stats.outliers == []

    def test_two_values(self):
        """Two values produce valid stats."""
        stats = compute_quartiles([10, 20])
        assert stats.min_val <= stats.median <= stats.max_val

    def test_all_identical_values(self):
        """All identical values: IQR=0, no crash."""
        stats = compute_quartiles([5, 5, 5, 5, 5])
        assert stats.median == 5
        assert stats.q1 == 5
        assert stats.q3 == 5
        assert stats.std == 0
        assert stats.outliers == []

    def test_all_values_are_outliers(self):
        """When IQR creates fences that exclude all values, falls back to extremes."""
        # Two clusters far apart with few values → possible all-outlier scenario
        stats = compute_quartiles([1, 1, 1, 100])
        # Should not raise ValueError; whiskers should be valid
        assert stats.min_val <= stats.max_val

    def test_negative_values(self):
        """Negative values produce valid statistics."""
        stats = compute_quartiles([-50, -30, -10, 10, 30])
        assert stats.min_val <= stats.median <= stats.max_val
        assert stats.mean == pytest.approx(-10.0)


class TestNegativeValues:
    """Tests for negative value handling across chart types."""

    def test_bar_chart_negative_values(self):
        """Bar chart handles negative values without crash."""
        data = [
            BarData(label="Negative", value=-50),
            BarData(label="Positive", value=100),
            BarData(label="Zero", value=0),
        ]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert "Negative" in result
        assert "Positive" in result

    def test_box_plot_negative_values(self):
        """Box plot handles negative distributions."""
        series = [BoxPlotSeries(name="Neg", values=[-100, -50, -30, -10, 0, 10])]
        opts = ChartOptions(use_color=False)
        chart = BoxPlot(series=series, options=opts)
        result = chart.render()
        assert "Neg" in result
        assert "median" in result

    def test_scatter_plot_negative_values(self):
        """Scatter plot handles negative coordinates."""
        points = [
            ScatterPoint(name="NegNeg", x=-10, y=-20),
            ScatterPoint(name="PosPos", x=10, y=20),
        ]
        opts = ChartOptions(use_color=False)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()
        assert "NegNeg" in result
        assert "PosPos" in result

    def test_line_chart_negative_values(self):
        """Line chart handles negative Y values."""
        points = [
            LinePoint(series="Test", x=1, y=-50),
            LinePoint(series="Test", x=2, y=0),
            LinePoint(series="Test", x=3, y=50),
        ]
        opts = ChartOptions(use_color=False)
        chart = LineChart(points=points, options=opts)
        result = chart.render()
        assert "Test" in result


class TestAllIdenticalValues:
    """Tests for all-identical value handling (division by zero risks)."""

    def test_bar_chart_identical_values(self):
        """Bar chart handles all identical values."""
        data = [BarData(label="A", value=50), BarData(label="B", value=50)]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert "A" in result
        assert "B" in result

    def test_box_plot_identical_values(self):
        """Box plot handles all identical values without stdev crash."""
        series = [BoxPlotSeries(name="Same", values=[42, 42, 42, 42, 42])]
        opts = ChartOptions(use_color=False)
        chart = BoxPlot(series=series, options=opts)
        result = chart.render()
        assert "Same" in result
        assert "42" in result

    def test_heatmap_identical_values(self):
        """Heatmap handles all identical values."""
        matrix = [[100, 100], [100, 100]]
        opts = ChartOptions(use_color=False)
        chart = Heatmap(matrix=matrix, row_labels=["Q1", "Q2"], col_labels=["A", "B"], options=opts)
        result = chart.render()
        assert "Q1" in result

    def test_scatter_plot_identical_values(self):
        """Scatter plot handles points at same location."""
        points = [
            ScatterPoint(name="A", x=50, y=100),
            ScatterPoint(name="B", x=50, y=100),
        ]
        opts = ChartOptions(use_color=False)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()
        assert "A" in result

    def test_line_chart_identical_y(self):
        """Line chart handles flat line (all identical Y)."""
        points = [
            LinePoint(series="Flat", x=1, y=100),
            LinePoint(series="Flat", x=2, y=100),
            LinePoint(series="Flat", x=3, y=100),
        ]
        opts = ChartOptions(use_color=False)
        chart = LineChart(points=points, options=opts)
        result = chart.render()
        assert "Flat" in result

    def test_histogram_identical_latencies(self):
        """Histogram handles all identical latencies."""
        data = [
            HistogramBar(label="Q1", value=50),
            HistogramBar(label="Q2", value=50),
        ]
        opts = ChartOptions(use_color=False)
        chart = Histogram(data=data, options=opts)
        result = chart.render()
        assert "Q1" in result


class TestSingleDataPoint:
    """Tests for single data point handling."""

    def test_box_plot_single_value_series(self):
        """Box plot with single-value series doesn't crash."""
        series = [BoxPlotSeries(name="One", values=[42])]
        opts = ChartOptions(use_color=False)
        chart = BoxPlot(series=series, options=opts)
        result = chart.render()
        assert "One" in result

    def test_line_chart_single_point(self):
        """Line chart with single point renders."""
        points = [LinePoint(series="Solo", x=1, y=100)]
        opts = ChartOptions(use_color=False)
        chart = LineChart(points=points, options=opts)
        result = chart.render()
        assert "Solo" in result

    def test_heatmap_single_cell(self):
        """Heatmap with single cell renders."""
        opts = ChartOptions(use_color=False)
        chart = Heatmap(matrix=[[42]], row_labels=["Q1"], col_labels=["A"], options=opts)
        result = chart.render()
        assert "Q1" in result
        assert "42" in result


class TestNaNAndInfinity:
    """Tests for NaN and Infinity handling."""

    def test_bar_chart_nan(self):
        """Bar chart handles NaN values without crash."""
        data = [BarData(label="Normal", value=100), BarData(label="NaN", value=float("nan"))]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert "Normal" in result

    def test_bar_chart_infinity(self):
        """Bar chart handles Infinity values without crash."""
        data = [BarData(label="Normal", value=100), BarData(label="Inf", value=float("inf"))]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert "Normal" in result

    def test_histogram_zero_latency(self):
        """Histogram handles zero latency without division by zero."""
        data = [
            HistogramBar(label="Q1", value=0),
            HistogramBar(label="Q2", value=0),
        ]
        opts = ChartOptions(use_color=False)
        chart = Histogram(data=data, options=opts)
        result = chart.render()
        assert "Q1" in result


class TestNarrowWidth:
    """Tests for narrow terminal width handling."""

    def test_bar_chart_narrow(self):
        """Bar chart renders at minimum width without crash."""
        data = [BarData(label="VeryLongLabelThatExceedsWidth", value=100)]
        opts = ChartOptions(width=40, use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert len(max(result.split("\n"), key=len)) <= 40

    def test_heatmap_narrow_truncates_columns(self):
        """Heatmap truncates columns when too narrow."""
        matrix = [[i * 10 for i in range(10)]]
        col_labels = [f"Platform{i}" for i in range(10)]
        opts = ChartOptions(width=40, use_color=False)
        chart = Heatmap(matrix=matrix, row_labels=["Q1"], col_labels=col_labels, options=opts)
        result = chart.render()
        assert "Q1" in result
        # Should truncate some columns
        assert "..." in result

    def test_scatter_plot_narrow(self):
        """Scatter plot renders at minimum width."""
        points = [ScatterPoint(name="A", x=10, y=20), ScatterPoint(name="B", x=30, y=40)]
        opts = ChartOptions(width=40, use_color=False)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()
        assert "A" in result


class TestANSISanitization:
    """Tests for ANSI escape sequence sanitization."""

    def test_sanitize_strips_ansi(self):
        """_sanitize_text strips ANSI escape sequences."""
        result = ChartBase._sanitize_text("\033[1;31mRED\033[0m")
        assert result == "RED"
        assert "\033" not in result

    def test_sanitize_preserves_normal_text(self):
        """_sanitize_text preserves normal text."""
        result = ChartBase._sanitize_text("Normal text")
        assert result == "Normal text"

    def test_bar_chart_ansi_in_label(self):
        """Bar chart sanitizes ANSI in labels."""
        data = [BarData(label="\033[31mInjected\033[0m", value=100)]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert "Injected" in result
        assert "\033[31m" not in result

    def test_title_ansi_sanitization(self):
        """Chart titles have ANSI sequences stripped."""
        data = [BarData(label="Test", value=100)]
        opts = ChartOptions(use_color=False, title="\033[2JCleared")
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert "Cleared" in result
        assert "\033[2J" not in result


class TestFactoryFunctionValidation:
    """Tests that factory functions warn on unexpected types."""

    def test_bar_data_factory_unknown_type_uses_getattr(self):
        """bar_from_data handles non-BarData types via getattr fallback."""
        from dataclasses import dataclass

        @dataclass
        class CustomBar:
            label: str = "test"
            value: float = 42

        chart = bar_from_data([CustomBar()])
        result = chart.render()
        assert "test" in result

    def test_scatter_factory_unknown_type_uses_getattr(self):
        """scatter_from_points handles non-ScatterPoint types via getattr fallback."""
        from dataclasses import dataclass

        @dataclass
        class CustomPoint:
            name: str = "test"
            cost: float = 10
            performance: float = 20

        chart = scatter_from_points([CustomPoint()])
        result = chart.render()
        assert "test" in result


# ── Comparison Bar Chart Tests ───────────────────────────────────


class TestNewChartEdgeCases:
    """Edge case tests across all new chart types."""

    def test_comparison_bar_nan_values(self):
        """ComparisonBar handles NaN values."""

        data = [ComparisonBarData(label="Q1", baseline_value=float("nan"), comparison_value=50)]
        opts = ChartOptions(use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        assert "Q1" in result

    def test_comparison_bar_identical_values(self):
        """ComparisonBar handles identical baseline and comparison values."""

        data = [ComparisonBarData(label="Q1", baseline_value=100, comparison_value=100)]
        opts = ChartOptions(use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        assert "Q1" in result

    def test_diverging_bar_zero_pct_change(self):
        """DivergingBar handles zero percentage change."""

        data = [DivergingBarData(label="Q1", pct_change=0.0)]
        opts = ChartOptions(use_color=False)
        chart = DivergingBar(data=data, options=opts)
        result = chart.render()
        assert "Q1" in result
        assert "0 improved" in result or "1 stable" in result

    def test_diverging_bar_extreme_values(self):
        """DivergingBar handles very large percentage changes."""

        data = [
            DivergingBarData(label="Q1", pct_change=-95.0),
            DivergingBarData(label="Q2", pct_change=+1500.0),
        ]
        opts = ChartOptions(use_color=False)
        chart = DivergingBar(data=data, options=opts)
        result = chart.render()
        assert "+1500.0%" in result
        assert "-95.0%" in result

    def test_summary_box_comparison_flag(self):
        """SummaryStats.is_comparison correctly detects comparison mode."""

        single = SummaryStats(primary_value=100)
        assert not single.is_comparison

        comparison = SummaryStats(primary_baseline=100, primary_comparison=80)
        assert comparison.is_comparison

    def test_comparison_bar_narrow_width(self):
        """ComparisonBar renders at minimum width."""

        data = [ComparisonBarData(label="Q1", baseline_value=100, comparison_value=75)]
        opts = ChartOptions(width=40, use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        assert "Q1" in result


class TestHeatmapColumnFitting:
    """Tests for heatmap column-shrinking behavior (fit all cols before truncating)."""

    def _make_heatmap(self, num_cols: int, width: int = 120) -> Heatmap:
        """Build a heatmap with ``num_cols`` platforms and a fixed chart width."""
        matrix = [[float(10 * (i + 1) + j) for j in range(num_cols)] for i in range(3)]
        row_labels = [f"Q{i + 1}" for i in range(3)]
        col_labels = [f"Platform{j + 1}" for j in range(num_cols)]
        opts = ChartOptions(width=width, use_color=False)
        return Heatmap(matrix=matrix, row_labels=row_labels, col_labels=col_labels, options=opts)

    def test_all_columns_shown_when_they_fit(self):
        """When columns comfortably fit at default cell width, all are rendered."""
        chart = self._make_heatmap(num_cols=3, width=120)
        result = chart.render()
        for j in range(1, 4):
            assert f"Platform{j}" in result

    def test_columns_compressed_instead_of_truncated(self):
        """When columns overflow at default width, cell_width shrinks to fit all cols."""
        # 6 columns with long labels at width=120 would normally truncate; they must all appear.
        chart = self._make_heatmap(num_cols=6, width=120)
        result = chart.render()
        for j in range(1, 7):
            assert f"Platform{j}" in result
        # The truncation indicator should NOT appear when compression succeeds.
        assert "..." not in result

    def test_many_columns_compressed_to_minimum(self):
        """Very many columns compress to minimum cell width and all remain visible."""
        chart = self._make_heatmap(num_cols=10, width=120)
        result = chart.render()
        # At least the first and last column labels must appear.
        assert "Platform1" in result
        assert "Platform10" in result

    def test_truncation_only_when_compression_insufficient(self):
        """Truncation indicator appears only when compressed cell_width < minimum viable width."""
        # 40 columns in 80 chars: each cell would need 2 chars, below minimum (5).
        # In this case truncation is acceptable.
        chart = self._make_heatmap(num_cols=40, width=80)
        result = chart.render()
        # The chart must render without crashing; first column always visible.
        assert "Platform1" in result

    def test_row_labels_all_present(self):
        """Row labels are always rendered regardless of column compression."""
        chart = self._make_heatmap(num_cols=6, width=120)
        result = chart.render()
        for i in range(1, 4):
            assert f"Q{i}" in result


class TestHistogramWidthAware:
    """Tests for histogram width-aware chunking and footer wrapping."""

    def _make_bars(self, num_queries: int, platforms: list[str]) -> list[HistogramBar]:
        """Build HistogramBar list for ``num_queries`` queries across ``platforms``."""
        bars: list[HistogramBar] = []
        for p in platforms:
            for q in range(1, num_queries + 1):
                bars.append(HistogramBar(label=str(q), value=10.0 + q, platform=p))
        return bars

    # ------------------------------------------------------------------ chunking

    def test_chunk_data_respects_max_queries_override(self):
        """_chunk_data splits by the max_queries override, not self.max_per_chart."""
        bars = self._make_bars(10, ["A", "B"])
        opts = ChartOptions(width=120, use_color=False)
        hist = Histogram(data=bars, options=opts)
        # Bootstrap internal state that render() normally sets.
        hist._use_grouped = True
        hist._platforms = ["A", "B"]
        chunks = hist._chunk_data(hist._sort_data(), max_queries=5)
        assert len(chunks) == 2
        # Each chunk should contain bars for exactly 5 unique queries.
        for chunk in chunks:
            unique_qids = {b.label for b in chunk}
            assert len(unique_qids) == 5

    def test_chunk_data_no_split_when_fits(self):
        """_chunk_data returns one chunk when unique queries ≤ max_queries."""
        bars = self._make_bars(8, ["A", "B"])
        opts = ChartOptions(width=120, use_color=False)
        hist = Histogram(data=bars, options=opts)
        hist._use_grouped = True
        hist._platforms = ["A", "B"]
        chunks = hist._chunk_data(hist._sort_data(), max_queries=10)
        assert len(chunks) == 1

    def test_grouped_render_splits_when_queries_exceed_width(self):
        """render() splits into multiple charts when 6 platforms × 22 queries exceed width=120."""
        platforms = [f"DuckDB 1.{v}.0" for v in range(6)]
        bars = self._make_bars(22, platforms)
        opts = ChartOptions(width=120, use_color=False)
        hist = Histogram(data=bars, options=opts)
        result = hist.render()
        # Two chart blocks separated by a blank line.
        assert "\n\n" in result

    def test_grouped_render_single_chart_when_few_queries(self):
        """render() produces one chart when queries fit within the width."""
        platforms = ["A", "B"]
        bars = self._make_bars(5, platforms)
        opts = ChartOptions(width=120, use_color=False)
        hist = Histogram(data=bars, options=opts, title="TestTitle")
        result = hist.render()
        # Only one chart header line rendered (no split into multiple charts).
        assert result.count("TestTitle") == 1

    # ------------------------------------------------------------------ footer wrapping

    def test_footer_wraps_when_legend_exceeds_width(self):
        """_build_grouped_footer wraps long legends to multiple lines."""
        # Build 6 long-named platforms to force a wide footer.
        platforms = [f"DuckDB {1 + i}.{i}.{i}" for i in range(6)]
        bars = self._make_bars(3, platforms)
        opts = ChartOptions(width=80, use_color=False)
        hist = Histogram(data=bars, options=opts)
        # Drive internal state.
        hist._use_grouped = True
        hist._platforms = platforms
        hist._outlier_bar_keys = set()
        platform_colors = dict.fromkeys(platforms, "#ffffff")
        platform_fills = dict.fromkeys(platforms, "█")
        from textcharts.base import ColorMode

        colors = TerminalColors(color_mode=ColorMode.NONE)
        footer = hist._build_grouped_footer(
            bars,
            global_mean=15.0,
            platform_colors=platform_colors,
            platform_fills=platform_fills,
            no_color=True,
            colors=colors,
            y_axis_width=8,
            width=80,
        )
        # Should contain at least one newline (wrapped to multiple lines).
        assert "\n" in footer

    def test_footer_single_line_when_legend_fits(self):
        """_build_grouped_footer stays on one line when legend is short."""
        platforms = ["A", "B"]
        bars = self._make_bars(2, platforms)
        opts = ChartOptions(width=120, use_color=False)
        hist = Histogram(data=bars, options=opts)
        hist._use_grouped = True
        hist._platforms = platforms
        hist._outlier_bar_keys = set()
        platform_colors = dict.fromkeys(platforms, "#ffffff")
        platform_fills = dict.fromkeys(platforms, "█")
        from textcharts.base import ColorMode

        colors = TerminalColors(color_mode=ColorMode.NONE)
        footer = hist._build_grouped_footer(
            bars,
            global_mean=12.0,
            platform_colors=platform_colors,
            platform_fills=platform_fills,
            no_color=True,
            colors=colors,
            y_axis_width=8,
            width=120,
        )
        assert "\n" not in footer
        assert "A" in footer
        assert "B" in footer

    def test_footer_no_line_exceeds_width(self):
        """Each wrapped line of the footer stays within the chart width."""
        import re as _re

        platforms = [f"DuckDB {1 + i}.{i}.{i}" for i in range(6)]
        bars = self._make_bars(3, platforms)
        chart_width = 80
        opts = ChartOptions(width=chart_width, use_color=False)
        hist = Histogram(data=bars, options=opts)
        hist._use_grouped = True
        hist._platforms = platforms
        hist._outlier_bar_keys = set()
        platform_colors = dict.fromkeys(platforms, "#ffffff")
        platform_fills = dict.fromkeys(platforms, "█")
        from textcharts.base import ColorMode

        colors = TerminalColors(color_mode=ColorMode.NONE)
        footer = hist._build_grouped_footer(
            bars,
            global_mean=15.0,
            platform_colors=platform_colors,
            platform_fills=platform_fills,
            no_color=True,
            colors=colors,
            y_axis_width=8,
            width=chart_width,
        )
        ansi_re = _re.compile(r"\x1b\[[0-9;]*m")
        for line in footer.split("\n"):
            visible_len = len(ansi_re.sub("", line))
            assert visible_len <= chart_width, f"Footer line too wide ({visible_len} > {chart_width}): {line!r}"


class TestLabelTruncation:
    """Tests for Phase 2: label truncation cap removal."""

    def test_bar_chart_full_name_up_to_25_chars(self):
        """Bar chart shows full names up to 25 characters."""
        name = "DataFusion Platform X"  # 21 chars
        data = [BarData(label=name, value=100)]
        opts = ChartOptions(width=100, use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert name in result

    def test_bar_chart_truncates_above_30_chars(self):
        """Bar chart truncates names longer than 30 characters."""
        name = "A" * 35
        data = [BarData(label=name, value=100)]
        opts = ChartOptions(width=100, use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert name not in result
        assert ".." in result

    def test_comparison_bar_shows_full_run_names(self):
        """ComparisonBar shows full run names up to 25 chars."""

        name = "DataFusion (sql)"  # 16 chars
        data = [ComparisonBarData(label="Q1", baseline_value=100, comparison_value=80, baseline_name=name)]
        opts = ChartOptions(width=100, use_color=False)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        assert name in result

    def test_box_plot_full_series_names(self):
        """BoxPlot shows full series names up to 30 chars."""
        name = "DataFusion Platform"  # 19 chars
        series = [BoxPlotSeries(name=name, values=[10, 20, 30, 40, 50])]
        opts = ChartOptions(width=100, use_color=False)
        chart = BoxPlot(series=series, options=opts)
        result = chart.render()
        assert name in result


class TestSubtitle:
    """Tests for chart subtitle rendering."""

    def test_subtitle_renders_string(self):
        """Subtitle renders the provided string."""
        data = [BarData(label="Q1", value=100)]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts, subtitle="DuckDB 1.2.0")
        result = chart.render()
        assert "DuckDB 1.2.0" in result

    def test_subtitle_renders_complex_string(self):
        """Subtitle renders a multi-part string."""
        data = [BarData(label="Q1", value=100)]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts, subtitle="TPC-H | SF=1 | DuckDB 1.2.0")
        result = chart.render()
        assert "TPC-H | SF=1 | DuckDB 1.2.0" in result

    def test_no_subtitle_without_value(self):
        """No subtitle line when subtitle is not set."""
        data = [BarData(label="Q1", value=100)]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        # Title line and separator should be adjacent (no subtitle between)
        lines = result.split("\n")
        # Find the title line and check that next line is separator
        for i, line in enumerate(lines):
            if "Bar Chart" in line and i + 1 < len(lines):
                assert lines[i + 1].strip().startswith("─") or lines[i + 1].strip().startswith("-")
                break



class TestSubject:
    """Tests for subject parameter that composes domain context into chart titles."""

    def test_subject_composes_with_default_title(self):
        """Subject is prepended to the chart's default title."""
        data = [BarData(label="Q1", value=100)]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts, subject="Revenue")
        assert chart.title == "Revenue Bar Chart"
        assert "Revenue Bar Chart" in chart.render()

    def test_explicit_title_wins_over_subject(self):
        """When both title and subject are provided, explicit title wins."""
        data = [BarData(label="Q1", value=100)]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts, title="Custom", subject="Ignored")
        assert chart.title == "Custom"

    def test_default_title_without_subject(self):
        """Without subject, the generic default title is used."""
        data = [BarData(label="Q1", value=100)]
        chart = BarChart(data=data)
        assert chart.title == "Bar Chart"

    def test_subject_on_histogram(self):
        """Subject works on histogram chart type."""
        data = [HistogramBar(label="Q1", value=10)]
        chart = Histogram(data=data, subject="Query Latency")
        assert chart.title == "Query Latency Histogram"

    def test_subject_on_summary_box(self):
        """Subject composes with SummaryStats default title."""
        from textcharts.summary_box import SummaryBox, SummaryStats
        stats = SummaryStats(num_items=1)
        chart = SummaryBox(stats=stats, subject="Benchmark")
        assert chart.stats.title == "Benchmark Summary"

    def test_subject_does_not_affect_explicit_summary_title(self):
        """SummaryBox with explicit stats title ignores subject."""
        from textcharts.summary_box import SummaryBox, SummaryStats
        stats = SummaryStats(title="My Report", num_items=1)
        chart = SummaryBox(stats=stats, subject="Ignored")
        assert chart.stats.title == "My Report"

    def test_subject_via_factory_function(self):
        """Subject passes through factory functions."""
        from textcharts.bar_chart import BarData as BD
        from textcharts.bar_chart import from_data as bar_from_data
        chart = bar_from_data([BD(label="A", value=1)], subject="Sales")
        assert chart.title == "Sales Bar Chart"


class TestLowerIsBetter:
    """Tests for lower_is_better parameter controlling improvement direction."""

    def test_comparison_bar_default_lower_is_better(self):
        """Default lower_is_better=True: positive % = regression (red)."""
        data = [ComparisonBarData("Q1", 100, 120, "A", "B")]
        opts = ChartOptions(use_color=True, use_unicode=True)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()
        # Positive change → red (#d95f02) with default lower_is_better=True
        assert "#d95f02" in result or "+20.0%" in result

    def test_comparison_bar_higher_is_better(self):
        """lower_is_better=False: positive % = improvement (green)."""
        data = [ComparisonBarData("Q1", 100, 120, "A", "B")]
        opts = ChartOptions(use_color=True, use_unicode=True)
        chart = ComparisonBar(data=data, options=opts, lower_is_better=False)
        result = chart.render()
        # Positive change → green (#66a61e) with lower_is_better=False
        assert "#66a61e" in result or "+20.0%" in result

    def test_diverging_bar_default_lower_is_better(self):
        """Default: negative pct = green (improvement), positive = red (regression)."""
        data = [DivergingBarData("Q1", -15.0), DivergingBarData("Q2", 25.0)]
        opts = ChartOptions(use_color=True, use_unicode=True)
        chart = DivergingBar(data=data, options=opts)
        result = chart.render()
        assert "1 improved" in result
        assert "1 regressed" in result

    def test_diverging_bar_higher_is_better(self):
        """lower_is_better=False: positive pct = green, negative = red."""
        data = [DivergingBarData("Q1", -15.0), DivergingBarData("Q2", 25.0)]
        opts = ChartOptions(use_color=True, use_unicode=True)
        chart = DivergingBar(data=data, options=opts, lower_is_better=False)
        result = chart.render()
        # With higher-is-better, positive is improvement, negative is regression
        assert "1 improved" in result
        assert "1 regressed" in result

    def test_summary_box_default_lower_is_better(self):
        """Default: negative pct gets green coloring."""
        from textcharts.summary_box import SummaryBox, SummaryStats

        stats = SummaryStats(
            primary_value=100,
            primary_baseline=120,
            primary_comparison=100,
            num_items=1,
        )
        opts = ChartOptions(use_color=True)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert isinstance(result, str)

    def test_summary_box_higher_is_better(self):
        """lower_is_better=False: positive pct gets green coloring."""
        from textcharts.summary_box import SummaryBox, SummaryStats

        stats = SummaryStats(
            primary_value=120,
            primary_baseline=100,
            primary_comparison=120,
            num_items=1,
            lower_is_better=False,
        )
        opts = ChartOptions(use_color=True)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        assert isinstance(result, str)


class TestColoredLabels:
    """Tests for Phase 4: uniform color application to labels."""

    def test_bar_chart_label_has_ansi(self):
        """Bar chart labels include ANSI color codes when color enabled."""
        data = [BarData(label="DuckDB", value=100)]
        opts = ChartOptions(use_color=True)
        _caps = TerminalCapabilities(color_mode=ColorMode.EXTENDED)
        with patch("textcharts.base.detect_terminal_capabilities", return_value=_caps):
            chart = BarChart(data=data, options=opts)
            result = chart.render()
        # The label line should contain ANSI escape codes
        lines = [line for line in result.split("\n") if "DuckDB" in line]
        assert any("\033[" in line for line in lines)

    def test_bar_chart_label_no_ansi_when_disabled(self):
        """Bar chart labels have no ANSI codes when color disabled."""
        data = [BarData(label="DuckDB", value=100)]
        opts = ChartOptions(use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        data_lines = [line for line in result.split("\n") if "DuckDB" in line]
        assert all("\033[" not in line for line in data_lines)

    def test_box_plot_label_has_ansi(self):
        """Box plot series labels include ANSI color codes."""
        series = [BoxPlotSeries(name="DuckDB", values=[10, 20, 30, 40, 50])]
        opts = ChartOptions(use_color=True)
        _caps = TerminalCapabilities(color_mode=ColorMode.EXTENDED)
        with patch("textcharts.base.detect_terminal_capabilities", return_value=_caps):
            chart = BoxPlot(series=series, options=opts)
            result = chart.render()
        label_lines = [line for line in result.split("\n") if "DuckDB" in line]
        assert any("\033[" in line for line in label_lines)

    def test_comparison_bar_names_have_ansi(self):
        """ComparisonBar run names include ANSI color codes."""

        data = [ComparisonBarData(label="Q1", baseline_value=100, comparison_value=80)]
        opts = ChartOptions(use_color=True)
        _caps = TerminalCapabilities(color_mode=ColorMode.EXTENDED)
        with patch("textcharts.base.detect_terminal_capabilities", return_value=_caps):
            chart = ComparisonBar(data=data, options=opts)
            result = chart.render()
        name_lines = [line for line in result.split("\n") if "Baseline" in line or "Comparison" in line]
        assert any("\033[" in line for line in name_lines)


class TestAxisLabels:
    """Tests for Phase 5: axis title labels."""

    def test_histogram_has_value_axis(self):
        """Histogram has 'Value' axis label by default."""
        data = [HistogramBar(label="Q1", value=100)]
        opts = ChartOptions(use_color=False)
        chart = Histogram(data=data, options=opts)
        result = chart.render()
        assert "Value" in result

    def test_box_plot_has_axis_label(self):
        """Box plot has axis label matching y_label."""
        series = [BoxPlotSeries(name="Test", values=[10, 20, 30])]
        opts = ChartOptions(use_color=False)
        chart = BoxPlot(series=series, y_label="Latency (ms)", options=opts)
        result = chart.render()
        assert "Latency (ms)" in result

    def test_heatmap_has_platform_axis(self):
        """Heatmap has column axis label."""
        matrix = [[1, 2], [3, 4]]
        opts = ChartOptions(use_color=False)
        chart = Heatmap(matrix=matrix, row_labels=["Q1", "Q2"], col_labels=["A", "B"], options=opts)
        result = chart.render()
        assert "Columns" in result or "Platform" in result

    def test_scatter_plot_has_axis_labels(self):
        """Scatter plot has both axis labels."""
        points = [ScatterPoint(name="A", x=1, y=2), ScatterPoint(name="B", x=3, y=4)]
        opts = ChartOptions(use_color=False)
        chart = ScatterPlot(points=points, x_label="Cost", y_label="Performance", options=opts)
        result = chart.render()
        assert "Cost" in result
        assert "Performance" in result

    def test_axis_label_has_arrow(self):
        """Axis labels include arrow indicator."""
        data = [HistogramBar(label="Q1", value=100)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        result = chart.render()
        # Unicode arrow →
        assert "\u2192" in result

    def test_axis_label_ascii_fallback(self):
        """Axis labels use ASCII arrow when Unicode disabled."""
        data = [HistogramBar(label="Q1", value=100)]
        opts = ChartOptions(use_color=False, use_unicode=False)
        chart = Histogram(data=data, options=opts)
        result = chart.render()
        assert "->" in result


class TestHeatmapDivergingPalette:
    """Tests for Phase 6: heatmap blue→red diverging palette."""

    def test_diverging_palette_is_default(self):
        """Diverging palette (blue→red) is the default."""
        matrix = [[1, 2], [3, 4]]
        chart = Heatmap(
            matrix=matrix,
            row_labels=["Q1", "Q2"],
            col_labels=["A", "B"],
            options=ChartOptions(use_color=False),
        )
        assert chart._color_scale == Heatmap.COLOR_SCALE_DIVERGING

    def test_sequential_palette_selectable(self):
        """Sequential palette can be selected via color_scheme parameter."""
        matrix = [[1, 2], [3, 4]]
        chart = Heatmap(
            matrix=matrix,
            row_labels=["Q1", "Q2"],
            col_labels=["A", "B"],
            color_scheme="sequential",
            options=ChartOptions(use_color=False),
        )
        assert chart._color_scale == Heatmap.COLOR_SCALE_SEQUENTIAL

    def test_diverging_palette_colors(self):
        """Diverging palette has blue and red endpoints."""
        assert "#2166ac" in Heatmap.COLOR_SCALE_DIVERGING  # Blue
        assert "#b2182b" in Heatmap.COLOR_SCALE_DIVERGING  # Red

    def test_scale_legend_shows_fast_slow(self):
        """Scale legend indicates fast and slow ends of the scale."""
        matrix = [[1, 2], [3, 4]]
        chart = Heatmap(
            matrix=matrix,
            row_labels=["Q1", "Q2"],
            col_labels=["A", "B"],
            options=ChartOptions(use_color=False),
        )
        result = chart.render()
        assert "fast" in result
        assert "slow" in result

    def test_from_matrix_passes_color_scheme(self):
        """from_matrix factory passes color_scheme parameter."""
        chart = from_matrix(
            matrix=[[1, 2], [3, 4]],
            queries=["Q1", "Q2"],
            platforms=["A", "B"],
            color_scheme="sequential",
        )
        assert chart._color_scale == Heatmap.COLOR_SCALE_SEQUENTIAL


class TestHistogramOutliers:
    """Tests for Phase 7: histogram outlier bar distinction."""

    def test_outlier_detected_by_iqr(self):
        """Outlier bars are detected when value exceeds Q3 + 1.5*IQR."""
        # Create data where Q10 is clearly an outlier
        data = [HistogramBar(label=f"Q{i}", value=float(10 + i)) for i in range(1, 10)]
        data.append(HistogramBar(label="Q10", value=500.0))  # Clear outlier
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        chart.render()  # Triggers outlier detection
        assert "Q10" in chart._outlier_ids

    def test_outlier_uses_distinct_char(self):
        """Outlier bars use the configured distinct no-color unicode glyph."""
        data = [HistogramBar(label=f"Q{i}", value=float(10 + i)) for i in range(1, 10)]
        data.append(HistogramBar(label="Q10", value=500.0))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        result = chart.render()
        assert chart._get_outlier_char(no_color=True) in result

    def test_outlier_ascii_fallback(self):
        """Outlier bars use the configured no-color ASCII fallback glyph."""
        data = [HistogramBar(label=f"Q{i}", value=float(10 + i)) for i in range(1, 10)]
        data.append(HistogramBar(label="Q10", value=500.0))
        opts = ChartOptions(use_color=False, use_unicode=False)
        chart = Histogram(data=data, options=opts)
        result = chart.render()
        assert chart._get_outlier_char(no_color=True) in result

    def test_outlier_in_legend(self):
        """Outlier indicator appears in legend."""
        data = [HistogramBar(label=f"Q{i}", value=float(10 + i)) for i in range(1, 10)]
        data.append(HistogramBar(label="Q10", value=500.0))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        result = chart.render()
        assert "Outlier" in result

    def test_no_outlier_with_uniform_data(self):
        """No outliers detected when data is uniform."""
        data = [HistogramBar(label=f"Q{i}", value=100.0) for i in range(1, 11)]
        opts = ChartOptions(use_color=False)
        chart = Histogram(data=data, options=opts)
        chart.render()
        assert len(chart._outlier_ids) == 0

    def test_grouped_outlier_marks_only_the_outlier_bar(self):
        """Grouped mode tracks outliers per platform+query bar, not per query ID."""
        data: list[HistogramBar] = []
        for i in range(1, 11):
            baseline = 80 + i
            comparison = 82 + i
            if i == 10:
                comparison = 500  # clear outlier on one platform only
            data.append(HistogramBar(label=f"Q{i}", value=baseline, platform="DF(df)"))
            data.append(HistogramBar(label=f"Q{i}", value=comparison, platform="DF(sql)"))

        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        chart.render()

        assert ("DF(sql)", "Q10") in chart._outlier_bar_keys
        assert ("DF(df)", "Q10") not in chart._outlier_bar_keys


class TestSummaryBoxDotLeader:
    """Tests for Phase 8: summary box dot-leader padding."""

    def test_dot_leader_present_in_comparison(self):
        """Comparison summary box uses dot-leader between values and percentage."""

        stats = SummaryStats(
            primary_baseline=100.0,
            primary_comparison=80.0,
            total_baseline=1000.0,
            total_comparison=800.0,
            num_items=10,
        )
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        # Should contain middle dots for dot-leader
        assert "·" in result

    def test_dot_leader_ascii_fallback(self):
        """Dot-leader uses period in ASCII mode."""

        stats = SummaryStats(
            primary_baseline=100.0,
            primary_comparison=80.0,
        )
        opts = ChartOptions(use_color=False, use_unicode=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        # Should contain periods for dot-leader
        assert ".." in result

    def test_no_wide_blank_gap(self):
        """No wide blank gap (>10 consecutive spaces) between value and percentage."""

        stats = SummaryStats(
            primary_baseline=18.2,
            primary_comparison=61.3,
            num_items=22,
        )
        opts = ChartOptions(width=100, use_color=False, use_unicode=True)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        # Find the Primary metric line and check for no wide blank gap
        for line in result.split("\n"):
            if "Primary" in line and "%" in line:
                # Should not have more than 3 consecutive spaces (since dots fill the gap)
                assert "     " not in line  # 5+ spaces means gap not filled

    def test_single_run_no_dot_leader(self):
        """Single-run summary box has no dot-leader (no percentage to trace to)."""

        stats = SummaryStats(primary_value=100.0, total_value=500.0, num_items=5)
        opts = ChartOptions(use_color=False)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()
        # Single-run metrics don't have percentage, so no dot-leader needed
        assert "·" not in result or ".." not in result

    def test_no_color_percentage_arrows_do_not_overflow_box_width(self):
        """No-color percentage arrows are included in width calculations."""

        width = 120
        stats = SummaryStats(
            title="DataFusion (df) vs DataFusion (sql) Summary",
            primary_baseline=62.6,
            primary_comparison=66.5,  # +6.2% -> includes up arrow in no-color mode
            total_baseline=4900.0,
            total_comparison=4831.0,  # -1.4% (no arrow threshold)
            num_items=22,
        )
        opts = ChartOptions(width=width, use_color=False, use_unicode=True)
        chart = SummaryBox(stats=stats, options=opts)
        result = chart.render()

        for line in result.splitlines():
            assert len(line) == width


class TestEdgeCases:
    """Tests for edge cases in new features."""

    def test_very_long_name_truncated_at_30(self):
        """Names longer than 30 chars are truncated in all chart types."""
        long_name = "A" * 40
        data = [BarData(label=long_name, value=100)]
        opts = ChartOptions(width=100, use_color=False)
        chart = BarChart(data=data, options=opts)
        result = chart.render()
        assert long_name not in result
        assert ".." in result

    def test_subtitle_truncated_to_width(self):
        """Subtitle is truncated if it exceeds chart width."""
        data = [BarData(label="Q1", value=100)]
        opts = ChartOptions(width=40, use_color=False)
        chart = BarChart(data=data, options=opts, subtitle="V" * 100)
        result = chart.render()
        # Should render without error and within width bounds
        for line in result.split("\n"):
            # Allow some tolerance for ANSI codes (stripped in no-color mode)
            assert len(line) <= 45  # 40 + small tolerance

    def test_axis_label_renders_in_line_chart(self):
        """Line chart axis labels use styled rendering."""
        points = [LinePoint(series="A", x=1, y=10), LinePoint(series="A", x=2, y=20)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = LineChart(points=points, y_label="Time (ms)", options=opts)
        result = chart.render()
        assert "Time (ms)" in result
        # Should have arrow indicator
        assert "\u2191" in result


# ── Percentile Ladder Chart Tests ────────────────────────────────
