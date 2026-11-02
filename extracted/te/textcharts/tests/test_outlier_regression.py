"""Tests for textcharts rendering."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from textcharts.bar_chart import BarChart, BarData
from textcharts.base import (
    TRUNCATION_MARKER,
    ChartOptions,
    ColorMode,
    TerminalCapabilities,
    outlier_severity_markers,
    robust_p95,
)
from textcharts.box_plot import BoxPlot, BoxPlotSeries
from textcharts.cdf_chart import CDFChart, CDFSeriesData
from textcharts.comparison_bar import ComparisonBar, ComparisonBarData
from textcharts.heatmap import Heatmap
from textcharts.histogram import Histogram, HistogramBar
from textcharts.line_chart import LineChart, LinePoint
from textcharts.percentile_ladder import PercentileData, PercentileLadder
from textcharts.scatter_plot import ScatterPlot, ScatterPoint
from textcharts.stacked_bar import StackedBar, StackedBarData, StackedBarSegment


class TestOutlierSeverityMarkers:
    """Unit tests for the centralised outlier_severity_markers() helper."""

    def test_value_at_or_below_scale_returns_empty(self):

        assert outlier_severity_markers(100, 100) == ""
        assert outlier_severity_markers(50, 100) == ""

    def test_scale_zero_returns_empty(self):

        assert outlier_severity_markers(10, 0) == ""

    @pytest.mark.parametrize(
        "value, scale_max, expected_count",
        [
            (150, 100, 1),  # 1.5× → 1 marker
            (200, 100, 1),  # 2× boundary → 1 marker
            (201, 100, 2),  # just over 2× → 2 markers
            (500, 100, 2),  # 5× boundary → 2 markers
            (501, 100, 3),  # just over 5× → 3 markers
            (1000, 100, 3),  # 10× boundary → 3 markers
            (1001, 100, 4),  # just over 10× → 4 markers
            (50000, 100, 4),  # extreme → 4 markers
        ],
    )
    def test_severity_thresholds(self, value, scale_max, expected_count):
        from textcharts.base import TRUNCATION_MARKER

        result = outlier_severity_markers(value, scale_max)
        assert result == TRUNCATION_MARKER * expected_count


class TestBarChartColorCycling:
    """Verify bars cycle through palette colours instead of 2-color scheme."""

    def test_ungrouped_bars_get_distinct_colors(self):
        """Each non-grouped bar should get a different palette colour."""
        import re

        data = [BarData(label=f"P{i}", value=(5 - i) * 100) for i in range(5)]
        opts = ChartOptions(use_color=True, use_unicode=True)
        _caps = TerminalCapabilities(color_mode=ColorMode.EXTENDED)
        with patch("textcharts.base.detect_terminal_capabilities", return_value=_caps):
            chart = BarChart(data=data, options=opts)
            result = chart.render()

        # Match both 256-color (\x1b[38;5;Nm) and truecolor (\x1b[38;2;R;G;Bm) codes
        ansi_color_re = re.compile(r"\x1b\[38;[25];([\d;]+)m")
        colors_seen: set[str] = set()
        for line in result.split("\n"):
            for label in [f"P{i}" for i in range(5)]:
                if label in line:
                    matches = ansi_color_re.findall(line)
                    colors_seen.update(matches)

        # Should have more than 2 unique colours (the old behaviour)
        assert len(colors_seen) >= 3, f"Expected ≥3 colours, got {len(colors_seen)}: {colors_seen}"


class TestBarChartOutlierSeverityMarkers:
    """Verify bar chart truncation uses severity-scaled ▸ markers."""

    def test_extreme_outlier_shows_multiple_markers(self):
        """A bar 20× the scale should show 4 ▸ markers."""
        from textcharts.base import TRUNCATION_MARKER

        # 10 small bars + 1 extreme outlier to trigger truncation (needs >5 bars,
        # max > median*10 and max > p95*3)
        data = [BarData(label=f"Q{i}", value=10) for i in range(10)]
        data.append(BarData(label="Outlier", value=10000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = BarChart(data=data, options=opts)
        result = chart.render()

        outlier_line = [line for line in result.split("\n") if "Outlier" in line]
        assert outlier_line, "Outlier bar not found"
        marker_count = outlier_line[0].count(TRUNCATION_MARKER)
        assert marker_count >= 2, f"Expected ≥2 severity markers, got {marker_count}"

    def test_duplicate_labels_do_not_inherit_outlier_truncation(self):
        """Non-outlier rows with the same label as an outlier keep their true bar length."""
        data = [BarData(label="dup", value=10) for _ in range(10)]
        data.append(BarData(label="dup", value=10000))
        opts = ChartOptions(use_color=False, use_unicode=True, width=70)
        chart = BarChart(data=data, options=opts)
        result = chart.render()

        dup_lines = [line for line in result.split("\n") if line.startswith("dup ")]
        assert len(dup_lines) == 11
        short_dup_lines = [line for line in dup_lines if " 10" in line and TRUNCATION_MARKER not in line]
        assert short_dup_lines, "Expected non-outlier duplicate-label rows without truncation markers"


class TestBoxPlotScaleCapping:
    """Verify box plot scale is capped at max_whisker × 1.5."""

    def test_extreme_outlier_does_not_dominate_scale(self):
        """With one extreme value, scale should be capped, not span full range."""
        series = [
            BoxPlotSeries(name="Normal", values=[10, 20, 30, 40, 50]),
            BoxPlotSeries(name="WithOutlier", values=[10, 20, 30, 40, 50, 10000]),
        ]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = BoxPlot(series=series, options=opts)
        result = chart.render()

        # The axis max label should NOT be "10.0K" — it should be capped
        assert "10.0K" not in result, "Scale should be capped, not span to 10K"

    def test_no_capping_when_no_extreme_outliers(self):
        """Without extreme outliers, scale should reflect actual data range."""
        series = [BoxPlotSeries(name="A", values=[10, 20, 30, 40, 50])]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = BoxPlot(series=series, options=opts)
        result = chart.render()
        assert "50" in result


class TestBoxPlotOutlierTruncationMarkers:
    """Verify box plot outliers beyond scale_max show severity ▸ markers."""

    def test_truncated_outlier_shows_marker(self):
        from textcharts.base import TRUNCATION_MARKER

        # Values where 10000 is an extreme outlier well beyond whisker×1.5
        series = [BoxPlotSeries(name="Test", values=[10, 20, 30, 40, 50, 10000])]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = BoxPlot(series=series, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Truncated outlier should show ▸ marker"

    def test_severity_markers_form_contiguous_block(self):
        """Severity ▸ markers must not be interleaved with outlier o dots."""
        # Many outliers ensure some occupy rightmost positions
        values = list(range(10, 60)) + [5000, 6000, 7000, 8000, 9000, 10000]
        series = [BoxPlotSeries(name="Test", values=values)]
        opts = ChartOptions(use_color=False, use_unicode=True, width=80)
        chart = BoxPlot(series=series, options=opts)
        result = chart.render()

        # Find the middle line (contains the label)
        mid_line = [line for line in result.split("\n") if "Test" in line]
        assert mid_line, "Box plot middle line not found"
        text = mid_line[0]
        # Extract the trailing marker region: everything after the last whisker end
        # The ▸ markers should be contiguous (no 'o' between them)
        marker_region = text[text.rfind(TRUNCATION_MARKER[0]) - 3 :] if TRUNCATION_MARKER in text else ""
        if marker_region:
            # Between the first ▸ and the end, there should be no 'o'
            first_marker = marker_region.index(TRUNCATION_MARKER)
            after_first = marker_region[first_marker:]
            assert "o" not in after_first, f"Outlier 'o' found within severity markers: {after_first!r}"

    def test_no_dead_line_before_stats_table(self):
        """There should be no blank line between axis label and stats table."""
        series = [BoxPlotSeries(name="A", values=[10, 20, 30, 40, 50])]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = BoxPlot(series=series, show_stats=True, options=opts)
        result = chart.render()

        lines = result.split("\n")
        # Find the axis label line (contains "→")
        axis_idx = next((i for i, line in enumerate(lines) if "→" in line), None)
        assert axis_idx is not None, "Axis label not found"
        # The next line should be the stats header, not blank
        assert lines[axis_idx + 1].strip() != "", "Blank line between axis label and stats table"


class TestBoxPlotSeriesSpacing:
    """Verify no dead vertical space between series."""

    def test_no_blank_line_between_series(self):
        """Adjacent series should not have blank lines between them."""
        series = [
            BoxPlotSeries(name="A", values=[10, 20, 30, 40, 50]),
            BoxPlotSeries(name="B", values=[15, 25, 35, 45, 55]),
        ]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = BoxPlot(series=series, show_stats=False, options=opts)
        result = chart.render()

        lines = result.split("\n")
        # Find lines with series labels
        label_indices = [i for i, line in enumerate(lines) if "A" in line.split()[0:1] or "B" in line.split()[0:1]]
        if len(label_indices) >= 2:
            # Between the bottom of series A (label_idx[0]+1) and top of series B
            # (label_idx[1]-1), there should be no blank line
            gap = label_indices[1] - label_indices[0]
            # Each series is 3 lines (top, mid, bottom), so gap should be exactly 3
            assert gap == 3, f"Expected 3-line gap between series labels, got {gap}"


class TestBoxPlotStatsTable:
    """Verify statistics are rendered as an aligned table."""

    def test_stats_table_has_header_and_separator(self):
        series = [BoxPlotSeries(name="Test", values=[10, 20, 30, 40, 50])]
        chart = BoxPlot(series=series, show_stats=True)
        result = chart.render()

        assert "median" in result
        assert "mean" in result
        assert "std" in result
        # Separator line with ─
        assert "─" in result.split("median")[-1]

    def test_stats_table_uniform_decimals(self):
        """All values in a column should use the same decimal format."""
        series = [
            BoxPlotSeries(name="A", values=[10, 20, 30, 40, 50]),  # median=30.0
            BoxPlotSeries(name="B", values=[15, 25, 35, 45, 55]),  # median=35.0
        ]
        chart = BoxPlot(series=series, show_stats=True)
        result = chart.render()

        # Both medians should have .0 suffix for consistency
        lines = result.split("\n")
        stat_lines = [line for line in lines if line.strip().startswith(("A", "B"))]
        for line in stat_lines:
            # Find numeric values — they should all have exactly one decimal place
            import re

            numbers = re.findall(r"\d+\.\d+", line)
            for num in numbers:
                decimal_places = len(num.split(".")[1])
                assert decimal_places == 1, f"Expected 1 decimal place, got {decimal_places} in '{num}'"

    def test_stats_table_k_suffix_for_large_values(self):
        """Large values should use K suffix uniformly in their column."""
        series = [
            BoxPlotSeries(name="A", values=[1000, 2000, 3000, 4000, 5000]),
            BoxPlotSeries(name="B", values=[1500, 2500, 3500, 4500, 5500]),
        ]
        chart = BoxPlot(series=series, show_stats=True)
        result = chart.render()

        # All stat values should use K suffix since they're all ≥1000
        import re

        lines = result.split("\n")
        # Match stats rows like "A    1.0K  2.0K ..." — series name followed by whitespace then digit
        # This excludes visual box plot rows like "A  ├───│───┤"
        stat_lines = [line for line in lines if re.match(r"^\s*(A|B)\s+\d", line)]
        assert stat_lines, "No stat lines found in box plot output"
        for line in stat_lines:
            assert "K" in line, f"Expected K suffix in stats line: {line}"


class TestComparisonBarOutlierSeverityMarkers:
    """Verify comparison bar truncation uses severity-scaled ▸ markers."""

    def test_extreme_outlier_shows_severity_markers(self):
        from textcharts.base import TRUNCATION_MARKER

        # One query with extreme baseline value to trigger truncation
        data = [
            ComparisonBarData(
                label="Q1", baseline_value=10, comparison_value=15, baseline_name="Old", comparison_name="New"
            ),
            ComparisonBarData(
                label="Q2", baseline_value=20, comparison_value=25, baseline_name="Old", comparison_name="New"
            ),
            ComparisonBarData(
                label="Q3", baseline_value=5000, comparison_value=12, baseline_name="Old", comparison_name="New"
            ),
        ]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = ComparisonBar(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Truncated outlier bar should show ▸ marker"


# ---------------------------------------------------------------------------
# Histogram outlier truncation (scale capping)
# ---------------------------------------------------------------------------


class TestHistogramOutlierTruncation:
    """Verify histogram caps scale at IQR fence so outliers don't compress data."""

    def test_extreme_outlier_caps_scale(self):
        """With one extreme value, Y-axis max should not show the outlier's value."""
        data = [HistogramBar(label=f"Q{i}", value=10 + i) for i in range(10)]
        data.append(HistogramBar(label="Q99", value=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        result = chart.render()

        # The axis should NOT show 50K — it should be capped
        assert "50.0K" not in result, "Scale should be capped, not span to 50K"

    def test_extreme_outlier_shows_severity_markers(self):
        """Truncated histogram bar should show ▸ severity markers."""
        data = [HistogramBar(label=f"Q{i}", value=10 + i) for i in range(10)]
        data.append(HistogramBar(label="Q99", value=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Truncated bar should show ▸ marker"

    def test_no_capping_without_extreme_outliers(self):
        """Uniform data should not trigger scale capping."""
        data = [HistogramBar(label=f"Q{i}", value=10 + i * 2) for i in range(10)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result, "No truncation expected for uniform data"

    def test_grouped_histogram_outlier_truncation(self):
        """Multi-platform histogram should also cap scale and show markers."""
        data = []
        for plat in ["DuckDB", "Polars"]:
            for i in range(6):
                data.append(HistogramBar(label=f"Q{i}", value=10 + i, platform=plat))
        data.append(HistogramBar(label="Q99", value=50000, platform="DuckDB"))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Grouped histogram should show truncation markers"

    def test_footer_shows_truncated_legend(self):
        """Footer should include a 'Truncated' legend entry when scale is capped."""
        data = [HistogramBar(label=f"Q{i}", value=10 + i) for i in range(10)]
        data.append(HistogramBar(label="Q99", value=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        result = chart.render()

        assert "Truncated" in result, "Footer should mention 'Truncated'"


# ---------------------------------------------------------------------------
# Heatmap outlier truncation (P95 capping)
# ---------------------------------------------------------------------------


class TestHeatmapOutlierTruncation:
    """Verify heatmap caps color scale at P95×2 for extreme outliers."""

    def test_extreme_outlier_shows_truncation_marker(self):
        """Cells exceeding P95×2 should have ▸ appended to their value."""
        # 9 normal values + 1 extreme outlier
        row_labels = [f"Q{i}" for i in range(10)]
        col_labels = ["Platform"]
        matrix = [[10 + i] for i in range(9)]
        matrix.append([50000])  # extreme outlier
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Heatmap(matrix=matrix, row_labels=row_labels, col_labels=col_labels, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Outlier cell should show ▸ marker"

    def test_range_footer_shows_capping_info(self):
        """Range footer should mention scale capping when truncation is active."""
        row_labels = [f"Q{i}" for i in range(10)]
        col_labels = ["Platform"]
        matrix = [[10 + i] for i in range(9)]
        matrix.append([50000])
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Heatmap(matrix=matrix, row_labels=row_labels, col_labels=col_labels, options=opts)
        result = chart.render()

        assert "capped" in result.lower(), "Footer should mention scale capping"

    def test_no_capping_without_outliers(self):
        """Uniform data should not trigger capping or truncation markers."""
        row_labels = [f"Q{i}" for i in range(10)]
        col_labels = ["Platform"]
        matrix = [[10 + i * 2] for i in range(10)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Heatmap(matrix=matrix, row_labels=row_labels, col_labels=col_labels, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result
        assert "capped" not in result.lower()

    def test_heatmap_with_color_truncation(self):
        """Heatmap with color should also show truncation markers."""
        row_labels = [f"Q{i}" for i in range(10)]
        col_labels = ["Platform"]
        matrix = [[10 + i] for i in range(9)]
        matrix.append([50000])
        opts = ChartOptions(use_color=True, use_unicode=True)
        chart = Heatmap(matrix=matrix, row_labels=row_labels, col_labels=col_labels, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result

    def test_zero_heavy_matrix_still_caps_outlier_scale(self):
        """Sparse positive baseline should still allow capping an extreme outlier."""
        row_labels = [f"Q{i}" for i in range(20)]
        col_labels = ["Platform"]
        matrix = [[0.0] for _ in range(18)] + [[10.0], [50000.0]]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Heatmap(matrix=matrix, row_labels=row_labels, col_labels=col_labels, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result
        assert "capped" in result.lower()

    def test_single_positive_zero_heavy_matrix_has_no_false_truncation(self):
        """One positive value among zeros should not be marked as truncated."""
        row_labels = [f"Q{i}" for i in range(20)]
        col_labels = ["Platform"]
        matrix = [[0.0] for _ in range(19)] + [[10.0]]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Heatmap(matrix=matrix, row_labels=row_labels, col_labels=col_labels, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result
        assert "capped" not in result.lower()


# ---------------------------------------------------------------------------
# Stacked bar outlier truncation (P95 capping)
# ---------------------------------------------------------------------------


class TestStackedBarOutlierTruncation:
    """Verify stacked bar caps scale when extreme totals compress other bars."""

    def test_extreme_outlier_shows_severity_markers(self):
        """A bar with extreme total should show ▸ severity markers."""
        data = [
            StackedBarData(
                label=f"P{i}",
                segments=[StackedBarSegment(phase_name="Load", value=10 + i)],
            )
            for i in range(10)
        ]
        data.append(
            StackedBarData(
                label="Outlier",
                segments=[StackedBarSegment(phase_name="Load", value=50000)],
            )
        )
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = StackedBar(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Truncated bar should show ▸ marker"

    def test_no_capping_without_extreme_outliers(self):
        """Uniform totals should not trigger truncation."""
        data = [
            StackedBarData(
                label=f"P{i}",
                segments=[StackedBarSegment(phase_name="Load", value=10 + i * 2)],
            )
            for i in range(10)
        ]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = StackedBar(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result

    def test_outlier_bar_still_shows_correct_total(self):
        """The total annotation should show the actual (uncapped) value."""
        data = [
            StackedBarData(
                label=f"P{i}",
                segments=[StackedBarSegment(phase_name="Load", value=10)],
            )
            for i in range(10)
        ]
        data.append(
            StackedBarData(
                label="Outlier",
                segments=[StackedBarSegment(phase_name="Load", value=60000)],
            )
        )
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = StackedBar(data=data, options=opts, metric_label="ms")
        result = chart.render()

        # The total annotation should still show the real value (1.0min or 60.0s)
        assert "1.0min" in result or "60.0s" in result, "Total should show actual value"

    def test_duplicate_labels_do_not_inherit_outlier_truncation(self):
        """Truncation must be determined per row total, not by platform label text."""
        data = [
            StackedBarData(
                label="dup",
                segments=[StackedBarSegment(phase_name="Load", value=10)],
            )
            for _ in range(10)
        ]
        data.append(
            StackedBarData(
                label="dup",
                segments=[StackedBarSegment(phase_name="Load", value=10000)],
            )
        )
        opts = ChartOptions(use_color=False, use_unicode=True, width=70)
        chart = StackedBar(data=data, options=opts, metric_label="ms")
        result = chart.render()

        dup_lines = [line for line in result.split("\n") if line.startswith("dup ")]
        assert len(dup_lines) == 11
        short_dup_lines = [line for line in dup_lines if "10ms" in line and TRUNCATION_MARKER not in line]
        assert short_dup_lines, "Expected non-outlier duplicate-label rows without truncation markers"


# ---------------------------------------------------------------------------
# Scatter plot outlier truncation (P95 axis capping)
# ---------------------------------------------------------------------------


class TestScatterPlotOutlierTruncation:
    """Verify scatter plot caps axes when one extreme point wastes plot area."""

    def test_extreme_outlier_caps_axis(self):
        """With one extreme x value, axis labels should not span to that value."""
        points = [ScatterPoint(name=f"P{i}", x=10 + i, y=100 + i) for i in range(10)]
        points.append(ScatterPoint(name="Extreme", x=50000, y=150))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()

        # The axis labels (before "Points:" section) should not show 50K
        axis_section = result.split("Points:")[0] if "Points:" in result else result
        assert "50.0K" not in axis_section, "X-axis should be capped, not span to 50K"

    def test_truncated_point_shows_marker_in_legend(self):
        """Legend should show ▸ for truncated points."""
        points = [ScatterPoint(name=f"P{i}", x=10 + i, y=100 + i) for i in range(10)]
        points.append(ScatterPoint(name="Extreme", x=50000, y=150))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Truncated point should show ▸ in legend"

    def test_no_capping_without_outliers(self):
        """Uniform data should not trigger axis capping."""
        points = [ScatterPoint(name=f"P{i}", x=10 + i * 5, y=100 + i * 10) for i in range(10)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result

    def test_y_axis_outlier_capping(self):
        """Extreme y value should also be capped."""
        points = [ScatterPoint(name=f"P{i}", x=10 + i, y=100 + i) for i in range(10)]
        points.append(ScatterPoint(name="Extreme", x=15, y=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result

    def test_zero_heavy_points_still_trigger_capping(self):
        """Sparse positive baseline should still allow capping an extreme outlier."""
        points = [ScatterPoint(name=f"P{i}", x=0.0, y=0.0) for i in range(18)]
        points.append(ScatterPoint(name="P18", x=10.0, y=10.0))
        points.append(ScatterPoint(name="Outlier", x=50000.0, y=50000.0))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result

    def test_single_positive_zero_heavy_points_have_no_false_truncation(self):
        """One positive point among zeros should not be marked truncated."""
        points = [ScatterPoint(name=f"P{i}", x=0.0, y=0.0) for i in range(19)]
        points.append(ScatterPoint(name="P19", x=10.0, y=10.0))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result


# ---------------------------------------------------------------------------
# Line chart outlier truncation (Y-axis capping)
# ---------------------------------------------------------------------------


class TestLineChartOutlierTruncation:
    """Verify line chart caps y-axis when one spike compresses all series."""

    def test_extreme_spike_caps_y_axis(self):
        """With one extreme y value, y-axis should not show that value."""
        points = [LinePoint(series="A", x=i, y=10 + i) for i in range(10)]
        points.append(LinePoint(series="A", x=10, y=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = LineChart(points=points, options=opts)
        result = chart.render()

        assert "50.0K" not in result, "Y-axis should be capped"

    def test_capped_shows_truncation_note(self):
        """When y-axis is capped, a note should appear."""
        points = [LinePoint(series="A", x=i, y=10 + i) for i in range(10)]
        points.append(LinePoint(series="A", x=10, y=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = LineChart(points=points, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Should show truncation note"
        assert "capped" in result.lower(), "Should mention capping"

    def test_no_capping_without_spikes(self):
        """Uniform data should not trigger y-axis capping."""
        points = [LinePoint(series="A", x=i, y=10 + i * 2) for i in range(10)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = LineChart(points=points, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result

    def test_zero_heavy_series_still_caps_y_axis(self):
        """Sparse positive baseline should still allow capping an extreme outlier."""
        points = [LinePoint(series="A", x=i, y=0.0) for i in range(18)]
        points.append(LinePoint(series="A", x=18, y=10.0))
        points.append(LinePoint(series="A", x=19, y=50000.0))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = LineChart(points=points, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result
        assert "capped" in result.lower()


# ---------------------------------------------------------------------------
# CDF chart outlier truncation (X-axis capping)
# ---------------------------------------------------------------------------


class TestCDFChartOutlierTruncation:
    """Verify CDF chart caps x-axis when extreme tail bunches all data left."""

    def test_extreme_tail_caps_x_axis(self):
        """With one extreme value, x-axis should be capped."""
        values = list(range(10, 30))  # 20 normal values
        values.append(50000)  # extreme outlier
        data = [CDFSeriesData(name="Platform", values=values)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()

        assert "50.0K" not in result, "X-axis should be capped"

    def test_capped_shows_truncation_marker(self):
        """Legend should include truncation marker when x-axis is capped."""
        values = list(range(10, 30))
        values.append(50000)
        data = [CDFSeriesData(name="Platform", values=values)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result

    def test_no_capping_without_extreme_tail(self):
        """Uniform data should not trigger x-axis capping."""
        values = list(range(10, 30))
        data = [CDFSeriesData(name="Platform", values=values)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result

    def test_zero_heavy_distribution_still_caps_x_axis(self):
        """Sparse positive baseline should still allow capping an extreme tail value."""
        values = [0.0] * 18 + [10.0, 50000.0]
        data = [CDFSeriesData(name="Platform", values=values)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result


# ---------------------------------------------------------------------------
# Percentile ladder outlier truncation (P99 capping)
# ---------------------------------------------------------------------------


class TestPercentileLadderOutlierTruncation:
    """Verify percentile ladder caps scale when one extreme P99 compresses others."""

    def test_extreme_p99_shows_severity_markers(self):
        """A platform with extreme P99 should show ▸ severity markers."""
        data = [PercentileData(name=f"P{i}", p50=10 + i, p90=20 + i, p95=30 + i, p99=40 + i) for i in range(10)]
        data.append(PercentileData(name="Outlier", p50=15, p90=25, p95=35, p99=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Truncated bar should show ▸ marker"

    def test_no_capping_without_extreme_p99(self):
        """Uniform P99 values should not trigger truncation."""
        data = [PercentileData(name=f"P{i}", p50=10 + i, p90=20 + i, p95=30 + i, p99=40 + i * 2) for i in range(10)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result

    def test_annotation_shows_actual_values(self):
        """The annotation should still show the real P99 value, not capped."""
        data = [PercentileData(name=f"P{i}", p50=10, p90=20, p95=30, p99=40) for i in range(10)]
        data.append(PercentileData(name="Outlier", p50=15, p90=25, p95=35, p99=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()

        assert "50000" in result, "Annotation should show actual P99 value"

    def test_zero_heavy_p99_still_truncates_outlier(self):
        """Sparse positive baseline should still allow capping an extreme P99."""
        data = [PercentileData(name=f"P{i}", p50=0, p90=0, p95=0, p99=0) for i in range(8)]
        data.append(PercentileData(name="P8", p50=0, p90=0, p95=0, p99=10))
        data.append(PercentileData(name="Outlier", p50=0, p90=0, p95=0, p99=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result

    def test_duplicate_labels_do_not_inherit_outlier_truncation(self):
        """Duplicate names should not cause non-outlier rows to render as truncated."""
        data = [PercentileData(name="dup", p50=1, p90=2, p95=3, p99=10) for _ in range(10)]
        data.append(PercentileData(name="dup", p50=5, p90=9, p95=10, p99=10000))
        opts = ChartOptions(use_color=False, use_unicode=True, width=80)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()

        dup_lines = [line for line in result.split("\n") if line.startswith("dup ")]
        assert len(dup_lines) == 11
        non_outlier_lines = [line for line in dup_lines if " |    10.0" in line and TRUNCATION_MARKER not in line]
        assert non_outlier_lines, "Expected duplicate non-outlier rows without truncation markers"


# ---------------------------------------------------------------------------
# Bar chart zero-heavy outlier truncation
# ---------------------------------------------------------------------------


class TestBarChartZeroHeavyTruncation:
    """Verify bar chart handles zero-heavy distributions with outlier capping."""

    def test_zero_heavy_bars_still_trigger_capping(self):
        """Sparse positive baseline plus one extreme outlier should truncate."""
        data = [BarData(label=f"Q{i}", value=0) for i in range(18)]
        data.append(BarData(label="Q18", value=10))
        data.append(BarData(label="Outlier", value=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = BarChart(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Zero-heavy bar chart should still cap and truncate outlier"

    def test_normal_data_no_false_positive(self):
        """Uniform non-zero data should not trigger truncation."""
        data = [BarData(label=f"Q{i}", value=10 + i * 2) for i in range(10)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = BarChart(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result


# ---------------------------------------------------------------------------
# Histogram zero-heavy outlier truncation
# ---------------------------------------------------------------------------


class TestHistogramZeroHeavyTruncation:
    """Verify histogram handles zero-heavy distributions with IQR fallback."""

    def test_zero_heavy_latencies_still_trigger_capping(self):
        """Sparse positive baseline plus one extreme outlier should truncate."""
        data = [HistogramBar(label=f"Q{i}", value=0) for i in range(18)]
        data.append(HistogramBar(label="Q18", value=10))
        data.append(HistogramBar(label="Q99", value=50000))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Zero-heavy histogram should still cap and truncate outlier"

    def test_normal_data_no_false_positive(self):
        """Uniform non-zero latencies should not trigger false truncation."""
        data = [HistogramBar(label=f"Q{i}", value=10 + i * 2) for i in range(10)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = Histogram(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result


# ---------------------------------------------------------------------------
# Stacked bar zero-heavy outlier truncation
# ---------------------------------------------------------------------------


class TestStackedBarZeroHeavyTruncation:
    """Verify stacked bar handles zero-heavy distributions with outlier capping."""

    def test_zero_heavy_totals_still_trigger_capping(self):
        """Sparse positive baseline plus one extreme outlier should truncate."""
        data = [
            StackedBarData(label=f"P{i}", segments=[StackedBarSegment(phase_name="Load", value=0)]) for i in range(19)
        ]
        data[-1] = StackedBarData(label="P18", segments=[StackedBarSegment(phase_name="Load", value=10)])
        data.append(StackedBarData(label="Outlier", segments=[StackedBarSegment(phase_name="Load", value=50000)]))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = StackedBar(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result, "Zero-heavy stacked bar should still cap and truncate outlier"

    def test_normal_data_no_false_positive(self):
        """Uniform non-zero totals should not trigger truncation."""
        data = [
            StackedBarData(label=f"P{i}", segments=[StackedBarSegment(phase_name="Load", value=10 + i * 2)])
            for i in range(10)
        ]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = StackedBar(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result


# ---------------------------------------------------------------------------
# Scatter plot duplicate-label truncation
# ---------------------------------------------------------------------------


class TestScatterPlotDuplicateLabelTruncation:
    """Verify scatter plot uses value-based truncation, not name-based."""

    def test_duplicate_names_do_not_inherit_outlier_truncation(self):
        """Non-outlier points with same name as an outlier should not show truncation marker."""
        points = [ScatterPoint(name="dup", x=10 + i, y=100 + i) for i in range(10)]
        points.append(ScatterPoint(name="dup", x=50000, y=150))
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()

        dup_lines = [line for line in result.split("\n") if "dup:" in line]
        truncated = [line for line in dup_lines if TRUNCATION_MARKER in line]
        non_truncated = [line for line in dup_lines if TRUNCATION_MARKER not in line]
        assert len(truncated) == 1, f"Expected exactly 1 truncated dup line, got {len(truncated)}"
        assert len(non_truncated) == 10, f"Expected 10 non-truncated dup lines, got {len(non_truncated)}"


class TestRobustP95Fallback:
    """Regression tests for robust_p95 zero-heavy behavior."""

    def test_single_positive_does_not_artificially_shrink_p95(self):
        """One positive value among zeros should keep p95 at that value."""

        vals = [0.0] * 19 + [10.0]
        assert robust_p95(vals) == 10.0

    def test_sparse_positive_tail_uses_positive_rank(self):
        """With sparse positives, p95 should come from positive-tail nearest rank."""

        vals = [0.0] * 18 + [10.0, 50000.0]
        assert robust_p95(vals) == 10.0


# ---------------------------------------------------------------------------
# Configurable outlier_cap tests
# ---------------------------------------------------------------------------


class TestOutlierCapDisabled:
    """outlier_cap=0 disables all auto-capping."""

    def test_bar_chart_no_truncation_when_disabled(self):
        """Bar chart with outlier_cap=0 should not truncate extreme values."""
        data = [BarData(label=f"Q{i}", value=10) for i in range(10)]
        data.append(BarData(label="Outlier", value=10000))
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=0)
        chart = BarChart(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result

    def test_scatter_plot_no_truncation_when_disabled(self):
        """Scatter plot with outlier_cap=0 should not cap axes."""
        points = [ScatterPoint(name=f"P{i}", x=10 + i, y=100 + i) for i in range(10)]
        points.append(ScatterPoint(name="Extreme", x=50000, y=150))
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=0)
        chart = ScatterPlot(points=points, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result

    def test_line_chart_no_truncation_when_disabled(self):
        """Line chart with outlier_cap=0 should not cap y-axis."""
        points = [LinePoint(series="A", x=i, y=10 + i) for i in range(10)]
        points.append(LinePoint(series="A", x=10, y=50000))
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=0)
        chart = LineChart(points=points, options=opts)
        result = chart.render()

        assert "capped" not in result.lower()

    def test_cdf_chart_no_truncation_when_disabled(self):
        """CDF chart with outlier_cap=0 should not cap x-axis."""
        values = list(range(10, 30)) + [50000]
        data = [CDFSeriesData(name="Platform", values=values)]
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=0)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result

    def test_heatmap_no_truncation_when_disabled(self):
        """Heatmap with outlier_cap=0 should not cap scale."""
        row_labels = [f"Q{i}" for i in range(10)]
        col_labels = ["Platform"]
        matrix = [[10 + i] for i in range(9)]
        matrix.append([50000])
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=0)
        chart = Heatmap(matrix=matrix, row_labels=row_labels, col_labels=col_labels, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result
        assert "capped" not in result.lower()

    def test_histogram_no_truncation_when_disabled(self):
        """Histogram with outlier_cap=0 should not cap scale."""
        data = [HistogramBar(label=f"Q{i}", value=10 + i) for i in range(10)]
        data.append(HistogramBar(label="Q99", value=50000))
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=0)
        chart = Histogram(data=data, options=opts)
        result = chart.render()

        assert "Truncated" not in result

    def test_stacked_bar_no_truncation_when_disabled(self):
        """Stacked bar with outlier_cap=0 should not truncate."""
        data = [
            StackedBarData(label=f"P{i}", segments=[StackedBarSegment(phase_name="Load", value=10 + i)])
            for i in range(10)
        ]
        data.append(StackedBarData(label="Outlier", segments=[StackedBarSegment(phase_name="Load", value=50000)]))
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=0)
        chart = StackedBar(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result

    def test_percentile_ladder_no_truncation_when_disabled(self):
        """Percentile ladder with outlier_cap=0 should not truncate."""
        data = [PercentileData(name=f"P{i}", p50=10 + i, p90=20 + i, p95=30 + i, p99=40 + i) for i in range(10)]
        data.append(PercentileData(name="Outlier", p50=15, p90=25, p95=35, p99=50000))
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=0)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result


class TestOutlierCapFixed:
    """outlier_cap=<float> caps at a fixed threshold."""

    def test_bar_chart_caps_at_fixed_value(self):
        """Bar chart with outlier_cap=500 should truncate values above 500."""
        data = [BarData(label=f"Q{i}", value=100 + i * 50) for i in range(6)]
        data.append(BarData(label="Big", value=1000))
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=500)
        chart = BarChart(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result

    def test_bar_chart_no_truncation_when_below_cap(self):
        """Bar chart should not truncate when all values are below outlier_cap."""
        data = [BarData(label=f"Q{i}", value=10 + i) for i in range(6)]
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=500)
        chart = BarChart(data=data, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER not in result

    def test_line_chart_caps_at_fixed_value(self):
        """Line chart with outlier_cap=500 should cap y-axis above 500."""
        points = [LinePoint(series="A", x=i, y=100 + i * 50) for i in range(6)]
        points.append(LinePoint(series="A", x=6, y=2000))
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=500)
        chart = LineChart(points=points, options=opts)
        result = chart.render()

        assert "capped" in result.lower()

    def test_heatmap_caps_at_fixed_value(self):
        """Heatmap with outlier_cap=100 should cap cells above 100."""
        row_labels = [f"Q{i}" for i in range(5)]
        col_labels = ["Platform"]
        matrix = [[10], [20], [30], [40], [500]]
        opts = ChartOptions(use_color=False, use_unicode=True, outlier_cap=100)
        chart = Heatmap(matrix=matrix, row_labels=row_labels, col_labels=col_labels, options=opts)
        result = chart.render()

        assert TRUNCATION_MARKER in result


class TestOutlierCapAutoDefault:
    """outlier_cap=None (default) preserves existing P95×2 auto-detection."""

    def test_bar_chart_auto_matches_default(self):
        """Bar chart with outlier_cap=None should behave identically to no option."""
        data = [BarData(label=f"Q{i}", value=10) for i in range(10)]
        data.append(BarData(label="Outlier", value=10000))

        opts_default = ChartOptions(use_color=False, use_unicode=True)
        opts_auto = ChartOptions(use_color=False, use_unicode=True, outlier_cap=None)

        result_default = BarChart(data=data, options=opts_default).render()
        result_auto = BarChart(data=list(data), options=opts_auto).render()

        assert result_default == result_auto
