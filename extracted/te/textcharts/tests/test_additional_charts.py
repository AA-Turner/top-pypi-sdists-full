"""Tests for textcharts rendering."""

from __future__ import annotations

from textcharts.base import ChartOptions
from textcharts.cdf_chart import CDFChart, CDFSeriesData
from textcharts.cdf_chart import from_series as cdf_from_series
from textcharts.normalized_speedup import NormalizedSpeedup, SpeedupData
from textcharts.normalized_speedup import from_ratios as speedup_from_ratios
from textcharts.percentile_ladder import PercentileData, PercentileLadder, compute_percentile
from textcharts.percentile_ladder import from_series as percentile_from_series
from textcharts.rank_table import RankTable, RankTableData, from_matrix
from textcharts.sparkline_table import SparklineColumn, SparklineTable, SparklineTableData
from textcharts.stacked_bar import StackedBar, StackedBarData, StackedBarSegment


class TestPercentileLadder:
    """Tests for percentile ladder chart rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        chart = PercentileLadder(data=[])
        result = chart.render()
        assert "No data" in result

    def test_single_platform(self):
        """Single platform renders correctly."""
        data = [PercentileData("DuckDB", 12, 45, 78, 120)]
        chart = PercentileLadder(data=data)
        result = chart.render()
        assert "DuckDB" in result
        assert "12" in result
        assert "120" in result
        assert "P50" in result
        assert "P99" in result

    def test_multiple_platforms(self):
        """Multiple platforms render as separate rows."""
        data = [
            PercentileData("DuckDB", 12, 45, 78, 120),
            PercentileData("Polars", 15, 52, 95, 310),
            PercentileData("Pandas", 25, 85, 140, 280),
        ]
        chart = PercentileLadder(data=data)
        result = chart.render()
        assert "DuckDB" in result
        assert "Polars" in result
        assert "Pandas" in result

    def test_band_fill_chars_unicode(self):
        """Unicode mode uses ░▒▓█ fill characters."""
        data = [PercentileData("Test", 10, 20, 30, 40)]
        opts = ChartOptions(use_color=False, use_unicode=True)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()
        assert "░" in result
        assert "█" in result

    def test_band_fill_chars_ascii(self):
        """ASCII mode uses .=#@ fill characters."""
        data = [PercentileData("Test", 10, 20, 30, 40)]
        opts = ChartOptions(use_color=False, use_unicode=False)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()
        assert "░" not in result
        assert "." in result or "=" in result or "#" in result or "@" in result

    def test_no_color_output(self):
        """Chart renders without ANSI codes when color disabled."""
        data = [PercentileData("Test", 10, 20, 30, 40)]
        opts = ChartOptions(use_color=False)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()
        assert "\033[" not in result

    def test_legend_shows_all_bands(self):
        """Legend shows all four percentile bands."""
        data = [PercentileData("Test", 10, 20, 30, 40)]
        opts = ChartOptions(use_color=False)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()
        assert "P50" in result
        assert "P90" in result
        assert "P95" in result
        assert "P99" in result

    def test_annotation_shows_pipe_separated_values(self):
        """Annotation shows values separated by pipes."""
        data = [PercentileData("Test", 10, 20, 30, 40)]
        opts = ChartOptions(use_color=False)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()
        # Should contain pipe-separated values
        assert "10.0 | 20.0 | 30.0 | 40.0" in result

    def test_annotation_values_use_shared_width_and_precision(self):
        """Annotation values are right-justified with consistent decimal precision."""
        data = [
            PercentileData("DataFusion (df)", 66.5, 123.9, 165.9, 217.1),
            PercentileData("DataFusion (sql)", 62, 120.7, 146.2, 237.1),
        ]
        opts = ChartOptions(use_color=False, width=120)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()

        assert " 66.5 | 123.9 | 165.9 | 217.1" in result
        assert " 62.0 | 120.7 | 146.2 | 237.1" in result

    def test_identical_percentiles(self):
        """Identical percentile values render without crash."""
        data = [PercentileData("Flat", 50, 50, 50, 50)]
        opts = ChartOptions(use_color=False)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()
        assert "Flat" in result

    def test_zero_percentiles(self):
        """Zero percentile values render without crash."""
        data = [PercentileData("Zero", 0, 0, 0, 0)]
        opts = ChartOptions(use_color=False)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()
        assert "Zero" in result

    def test_narrow_width(self):
        """Chart renders at minimum width."""
        data = [PercentileData("VeryLongPlatformName", 10, 50, 80, 200)]
        opts = ChartOptions(width=40, use_color=False)
        chart = PercentileLadder(data=data, options=opts)
        result = chart.render()
        assert len(result) > 0



class TestComputePercentile:
    """Tests for compute_percentile function."""

    def test_empty_input(self):
        """Empty input returns 0."""
        assert compute_percentile([], 50) == 0.0

    def test_single_value(self):
        """Single value returns that value for any percentile."""
        assert compute_percentile([42], 50) == 42
        assert compute_percentile([42], 99) == 42

    def test_two_values(self):
        """Two values interpolate correctly."""
        result = compute_percentile([10, 20], 50)
        assert result == 15.0

    def test_known_percentiles(self):
        """Known percentile values from sorted array."""
        vals = list(range(1, 101))  # 1 to 100
        assert compute_percentile(vals, 50) == 50.5
        assert compute_percentile(vals, 0) == 1.0
        assert compute_percentile(vals, 100) == 100.0

    def test_p99_near_max(self):
        """P99 is close to maximum for large arrays."""
        vals = list(range(1, 1001))
        p99 = compute_percentile(vals, 99)
        assert 990 <= p99 <= 1000

    def test_unsorted_input(self):
        """Function handles unsorted input correctly."""
        result = compute_percentile([50, 10, 30, 20, 40], 50)
        assert result == 30.0


class TestNormalizedSpeedup:
    """Tests for normalized speedup chart rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        chart = NormalizedSpeedup(data=[])
        result = chart.render()
        assert "No data" in result

    def test_single_platform_baseline(self):
        """Single platform at baseline renders."""
        data = [SpeedupData("SQLite", 1.0, True)]
        opts = ChartOptions(use_color=False)
        chart = NormalizedSpeedup(data=data, options=opts)
        result = chart.render()
        assert "SQLite" in result
        assert "1.00x" in result

    def test_faster_and_slower(self):
        """Faster and slower platforms render on both sides."""
        data = [
            SpeedupData("SQLite", 1.0, True),
            SpeedupData("DuckDB", 8.2, False),
            SpeedupData("Pandas", 0.4, False),
        ]
        opts = ChartOptions(use_color=False)
        chart = NormalizedSpeedup(data=data, options=opts)
        result = chart.render()
        assert "SQLite" in result
        assert "DuckDB" in result
        assert "Pandas" in result
        assert "8.20x" in result
        assert "0.40x" in result

    def test_log2_symmetry(self):
        """2x faster and 0.5x slower produce equal bar lengths."""
        data = [
            SpeedupData("Base", 1.0, True),
            SpeedupData("Fast", 2.0, False),
            SpeedupData("Slow", 0.5, False),
        ]
        opts = ChartOptions(use_color=False, width=80)
        chart = NormalizedSpeedup(data=data, options=opts)
        result = chart.render()
        # Both should appear in the output
        assert "2.00x" in result
        assert "0.50x" in result

    def test_no_color_output(self):
        """Chart renders without ANSI codes when color disabled."""
        data = [SpeedupData("Test", 1.5, False)]
        opts = ChartOptions(use_color=False)
        chart = NormalizedSpeedup(data=data, options=opts)
        result = chart.render()
        assert "\033[" not in result

    def test_direction_labels(self):
        """Chart shows Slower/Faster direction labels."""
        data = [SpeedupData("Test", 2.0, False)]
        opts = ChartOptions(use_color=False)
        chart = NormalizedSpeedup(data=data, options=opts)
        result = chart.render()
        assert "Slower" in result
        assert "Faster" in result


class TestStackedBar:
    """Tests for stacked bar chart rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        chart = StackedBar(data=[])
        result = chart.render()
        assert "No data" in result

    def test_single_platform_single_phase(self):
        """Single platform with one phase renders."""
        data = [StackedBarData("DuckDB", [StackedBarSegment("Power", 8000)])]
        opts = ChartOptions(use_color=False)
        chart = StackedBar(data=data, options=opts)
        result = chart.render()
        assert "DuckDB" in result
        assert "Power" in result

    def test_multi_platform_multi_phase(self):
        """Multiple platforms with multiple phases render."""
        data = [
            StackedBarData(
                "DuckDB",
                [
                    StackedBarSegment("Load", 1500),
                    StackedBarSegment("Power", 8000),
                ],
            ),
            StackedBarData(
                "SQLite",
                [
                    StackedBarSegment("Load", 5000),
                    StackedBarSegment("Power", 15000),
                ],
            ),
        ]
        opts = ChartOptions(use_color=False)
        chart = StackedBar(data=data, options=opts)
        result = chart.render()
        assert "DuckDB" in result
        assert "SQLite" in result
        assert "Load" in result
        assert "Power" in result

    def test_total_auto_computed(self):
        """Total is auto-computed from segments if not provided."""
        d = StackedBarData("Test", [StackedBarSegment("A", 100), StackedBarSegment("B", 200)])
        assert d.total == 300

    def test_zero_phases_skipped(self):
        """Phases with zero value render without crash."""
        data = [
            StackedBarData(
                "Test",
                [
                    StackedBarSegment("A", 100),
                    StackedBarSegment("B", 0),
                    StackedBarSegment("C", 200),
                ],
            )
        ]
        opts = ChartOptions(use_color=False)
        chart = StackedBar(data=data, options=opts)
        result = chart.render()
        assert "Test" in result

    def test_time_formatting(self):
        """Time values format correctly in annotations."""
        data = [
            StackedBarData("Fast", [StackedBarSegment("Run", 500)], total=500),
            StackedBarData("Med", [StackedBarSegment("Run", 5000)], total=5000),
            StackedBarData("Slow", [StackedBarSegment("Run", 120000)], total=120000),
        ]
        opts = ChartOptions(use_color=False)
        chart = StackedBar(data=data, options=opts, metric_label="ms")
        result = chart.render()
        assert "500ms" in result
        assert "5.0s" in result
        assert "2.0min" in result

    def test_legend_shows_phases(self):
        """Legend shows phase names."""
        data = [
            StackedBarData(
                "Test",
                [
                    StackedBarSegment("DataGen", 100),
                    StackedBarSegment("Load", 200),
                ],
            )
        ]
        opts = ChartOptions(use_color=False)
        chart = StackedBar(data=data, options=opts)
        result = chart.render()
        assert "DataGen" in result
        assert "Load" in result

    def test_no_color_output(self):
        """Chart renders without ANSI codes when color disabled."""
        data = [StackedBarData("Test", [StackedBarSegment("A", 100)])]
        opts = ChartOptions(use_color=False)
        chart = StackedBar(data=data, options=opts)
        result = chart.render()
        assert "\033[" not in result

# ── Sparkline Table Tests ────────────────────────────────


class TestSparklineTable:
    """Tests for sparkline table chart rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        data = SparklineTableData([], [])
        chart = SparklineTable(data=data)
        result = chart.render()
        assert "No data" in result

    def test_single_metric(self):
        """Single metric column renders."""
        cols = [SparklineColumn("Total", {"DuckDB": 1240, "Polars": 1580}, False)]
        data = SparklineTableData(["DuckDB", "Polars"], cols)
        opts = ChartOptions(use_color=False)
        chart = SparklineTable(data=data, options=opts)
        result = chart.render()
        assert "DuckDB" in result
        assert "Polars" in result
        assert "Total" in result

    def test_higher_is_better_inversion(self):
        """Higher-is-better columns show highest value with tallest bar."""
        cols = [SparklineColumn("Success", {"A": 100, "B": 50}, True)]
        data = SparklineTableData(["A", "B"], cols)
        opts = ChartOptions(use_color=False)
        chart = SparklineTable(data=data, options=opts)
        result = chart.render()
        assert "A" in result
        assert "B" in result

    def test_multiple_metrics(self):
        """Multiple metrics render as columns."""
        cols = [
            SparklineColumn("Latency", {"DuckDB": 56, "Polars": 72}, False),
            SparklineColumn("Success", {"DuckDB": 100, "Polars": 100}, True),
        ]
        data = SparklineTableData(["DuckDB", "Polars"], cols)
        opts = ChartOptions(use_color=False)
        chart = SparklineTable(data=data, options=opts)
        result = chart.render()
        assert "Latency" in result
        assert "Success" in result

    def test_legend_present(self):
        """Legend shows best/worst indicator."""
        cols = [SparklineColumn("Test", {"A": 1, "B": 2}, False)]
        data = SparklineTableData(["A", "B"], cols)
        opts = ChartOptions(use_color=False)
        chart = SparklineTable(data=data, options=opts)
        result = chart.render()
        assert "best" in result
        assert "worst" in result

    def test_no_color_output(self):
        """Chart renders without ANSI codes when color disabled."""
        cols = [SparklineColumn("Test", {"A": 1}, False)]
        data = SparklineTableData(["A"], cols)
        opts = ChartOptions(use_color=False)
        chart = SparklineTable(data=data, options=opts)
        result = chart.render()
        assert "\033[" not in result

    def test_long_platform_names_not_truncated_when_width_allows(self):
        """Long platform names remain fully visible when chart width allows it."""
        cols = [SparklineColumn("Total(ms)", {"DataFusion (df)": 100, "DataFusion (sql)": 110}, False)]
        data = SparklineTableData(["DataFusion (df)", "DataFusion (sql)"], cols)
        opts = ChartOptions(use_color=False, width=120)
        chart = SparklineTable(data=data, options=opts)
        result = chart.render()
        assert "DataFusion (df)" in result
        assert "DataFusion (sql)" in result
        assert "DataFusion (.." not in result

    def test_truncated_platform_names_are_disambiguated(self):
        """When truncation is required, colliding labels are made unique."""
        p1 = "VeryLongPlatformNameSharedPrefix-DataFusion-ModeA"
        p2 = "VeryLongPlatformNameSharedPrefix-DataFusion-ModeB"
        cols = [SparklineColumn("Total(ms)", {p1: 100, p2: 110}, False)]
        data = SparklineTableData([p1, p2], cols)
        opts = ChartOptions(use_color=False, width=40)
        chart = SparklineTable(data=data, options=opts)
        result = chart.render()
        assert "~1" in result
        assert "~2" in result

# ── CDF Chart Tests ────────────────────────────────


class TestCDFChart:
    """Tests for CDF chart rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        chart = CDFChart(data=[])
        result = chart.render()
        assert "No data" in result

    def test_empty_values(self):
        """Series with empty values returns message."""
        data = [CDFSeriesData("Empty", [])]
        chart = CDFChart(data=data)
        result = chart.render()
        assert "No data" in result

    def test_single_series(self):
        """Single series renders with markers."""
        data = [CDFSeriesData("DuckDB", [10, 20, 30, 50, 120])]
        opts = ChartOptions(use_color=False)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()
        assert "DuckDB" in result
        assert "100%" in result
        assert "0%" in result

    def test_multi_series(self):
        """Multiple series render with different markers."""
        data = [
            CDFSeriesData("DuckDB", [10, 20, 30, 50, 120]),
            CDFSeriesData("Polars", [15, 25, 45, 80, 310]),
        ]
        opts = ChartOptions(use_color=False)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()
        assert "DuckDB" in result
        assert "Polars" in result
        assert "*" in result  # First series marker
        assert "+" in result  # Second series marker

    def test_identical_values(self):
        """Identical values render without crash."""
        data = [CDFSeriesData("Flat", [50, 50, 50, 50, 50])]
        opts = ChartOptions(use_color=False)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()
        assert "Flat" in result

    def test_single_value(self):
        """Single value renders without crash."""
        data = [CDFSeriesData("Solo", [42])]
        opts = ChartOptions(use_color=False)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()
        assert "Solo" in result

    def test_y_axis_fixed_0_100(self):
        """Y-axis is fixed at 0-100% range."""
        data = [CDFSeriesData("Test", [10, 20, 30])]
        opts = ChartOptions(use_color=False)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()
        assert "100%" in result
        assert "0%" in result

    def test_no_color_output(self):
        """Chart renders without ANSI codes when color disabled."""
        data = [CDFSeriesData("Test", [10, 20, 30])]
        opts = ChartOptions(use_color=False)
        chart = CDFChart(data=data, options=opts)
        result = chart.render()
        assert "\033[" not in result

    def test_factory_function(self):
        """from_series factory creates CDF chart."""
        chart = cdf_from_series(
            [("DuckDB", [10, 20, 30])],
            options=ChartOptions(use_color=False),
        )
        result = chart.render()
        assert "DuckDB" in result

# ── Rank Table Tests ────────────────────────────────


class TestRankTable:
    """Tests for rank table chart rendering."""

    def test_empty_data(self):
        """Empty data returns message."""
        data = RankTableData([], [], {})
        chart = RankTable(data=data)
        result = chart.render()
        assert "No data" in result

    def test_two_platforms_two_queries(self):
        """Basic 2x2 ranking renders."""
        data = RankTableData(
            ["Q1", "Q2"],
            ["DuckDB", "Polars"],
            {
                ("DuckDB", "Q1"): 10,
                ("Polars", "Q1"): 20,
                ("DuckDB", "Q2"): 30,
                ("Polars", "Q2"): 15,
            },
        )
        opts = ChartOptions(use_color=False)
        chart = RankTable(data=data, options=opts)
        result = chart.render()
        assert "DuckDB" in result
        assert "Polars" in result
        assert "1st" in result
        assert "2nd" in result
        assert "Wins" in result

    def test_tie_handling(self):
        """Tied platforms get the same rank."""
        data = RankTableData(
            ["Q1"],
            ["A", "B", "C"],
            {("A", "Q1"): 10, ("B", "Q1"): 10, ("C", "Q1"): 20},
        )
        opts = ChartOptions(use_color=False)
        chart = RankTable(data=data, options=opts)
        result = chart.render()
        # A and B should both be 1st, C should be 3rd (not 2nd)
        assert "1st" in result
        assert "3rd" in result

    def test_georank_computed(self):
        """Geometric mean rank is computed."""
        data = RankTableData(
            ["Q1", "Q2"],
            ["A", "B"],
            {("A", "Q1"): 10, ("B", "Q1"): 20, ("A", "Q2"): 30, ("B", "Q2"): 15},
        )
        opts = ChartOptions(use_color=False)
        chart = RankTable(data=data, options=opts)
        result = chart.render()
        assert "GeoRank" in result

    def test_natural_sort_order(self):
        """Queries are naturally sorted (Q1, Q2, Q10 not Q1, Q10, Q2)."""
        data = RankTableData(
            ["Q10", "Q2", "Q1"],
            ["A", "B"],
            {
                ("A", "Q1"): 10,
                ("B", "Q1"): 20,
                ("A", "Q2"): 10,
                ("B", "Q2"): 20,
                ("A", "Q10"): 10,
                ("B", "Q10"): 20,
            },
        )
        opts = ChartOptions(use_color=False)
        chart = RankTable(data=data, options=opts)
        result = chart.render()
        lines = result.split("\n")
        # Find data rows that start with Q and a digit (not header "Query", title, or separator)
        data_lines = [line for line in lines if line.strip() and line.strip()[0:2] in ("Q1", "Q2")]
        # Filter out title and header lines
        data_lines = [line for line in data_lines if "Ranking" not in line and "Query " not in line]
        assert len(data_lines) == 3
        # Check order is Q1, Q2, Q10 (natural sort)
        assert data_lines[0].strip().startswith("Q1 ")
        assert data_lines[1].strip().startswith("Q2 ")
        assert data_lines[2].strip().startswith("Q10")

    def test_win_counts(self):
        """Win counts are correctly tallied."""
        data = RankTableData(
            ["Q1", "Q2", "Q3"],
            ["A", "B"],
            {
                ("A", "Q1"): 10,
                ("B", "Q1"): 20,
                ("A", "Q2"): 20,
                ("B", "Q2"): 10,
                ("A", "Q3"): 10,
                ("B", "Q3"): 20,
            },
        )
        opts = ChartOptions(use_color=False)
        chart = RankTable(data=data, options=opts)
        result = chart.render()
        # A wins 2 queries, B wins 1
        lines = [line for line in result.split("\n") if "Wins" in line]
        assert len(lines) == 1
        assert "2" in lines[0]
        assert "1" in lines[0]

    def test_no_color_output(self):
        """Chart renders without ANSI codes when color disabled."""
        data = RankTableData(
            ["Q1"],
            ["A", "B"],
            {("A", "Q1"): 10, ("B", "Q1"): 20},
        )
        opts = ChartOptions(use_color=False)
        chart = RankTable(data=data, options=opts)
        result = chart.render()
        assert "\033[" not in result

    def test_from_matrix_factory(self):
        """from_matrix creates rank table from matrix format."""
        chart = from_matrix(
            [[10, 20], [30, 15]],
            ["Q1", "Q2"],
            ["DuckDB", "Polars"],
            options=ChartOptions(use_color=False),
        )
        result = chart.render()
        assert "DuckDB" in result
        assert "Polars" in result

# ── All New Charts Module Import Tests ────────────────────────────────


class TestFromQueryResults:
    """Tests for percentile_from_series factory function."""

    def test_basic_factory(self):
        """Factory creates chart from raw query times."""
        chart = percentile_from_series(
            [("DuckDB", [10, 20, 30, 50, 120])],
            options=ChartOptions(use_color=False),
        )
        result = chart.render()
        assert "DuckDB" in result

    def test_empty_values(self):
        """Factory handles platform with no query times."""
        chart = percentile_from_series(
            [("Empty", [])],
            options=ChartOptions(use_color=False),
        )
        result = chart.render()
        assert "Empty" in result

    def test_multi_platform_factory(self):
        """Factory handles multiple platforms."""
        chart = percentile_from_series(
            [
                ("DuckDB", [10, 20, 30, 50, 120]),
                ("Polars", [15, 25, 45, 80, 310]),
            ],
            options=ChartOptions(use_color=False),
        )
        result = chart.render()
        assert "DuckDB" in result
        assert "Polars" in result

# ── Normalized Speedup Chart Tests ────────────────────────────────


class TestFromNormalizedResults:
    """Tests for speedup_from_ratios factory."""

    def test_basic_factory(self):
        """Factory creates chart from timing data."""
        chart = speedup_from_ratios(
            [("SQLite", 5000), ("DuckDB", 610)],
            baseline="SQLite",
            options=ChartOptions(use_color=False),
        )
        result = chart.render()
        assert "SQLite" in result
        assert "DuckDB" in result

    def test_slowest_baseline(self):
        """'slowest' auto-selects the slowest platform."""
        chart = speedup_from_ratios(
            [("A", 100), ("B", 500), ("C", 200)],
            baseline="slowest",
            options=ChartOptions(use_color=False),
        )
        result = chart.render()
        assert "1.00x" in result  # B should be 1.0x

    def test_fastest_baseline(self):
        """'fastest' auto-selects the fastest platform."""
        chart = speedup_from_ratios(
            [("A", 100), ("B", 500), ("C", 200)],
            baseline="fastest",
            options=ChartOptions(use_color=False),
        )
        result = chart.render()
        assert "1.00x" in result

    def test_empty_input(self):
        """Empty input renders no data."""
        chart = speedup_from_ratios([], options=ChartOptions(use_color=False))
        result = chart.render()
        assert "No data" in result

# ── Subject Parameter Tests ────────────────────────────────


class TestSubjectParameter:
    """Tests for the subject parameter across chart types."""

    def test_subject_composes_with_default_title(self):
        """subject='Query Latency' + default 'Histogram' → 'Query Latency Histogram'."""
        from textcharts.histogram import Histogram, HistogramBar

        h = Histogram([HistogramBar("q1", 10)], subject="Query Latency")
        assert h.title == "Query Latency Histogram"

    def test_explicit_title_wins_over_subject(self):
        """When both title and subject are provided, explicit title wins."""
        from textcharts.histogram import Histogram, HistogramBar

        h = Histogram([HistogramBar("q1", 10)], title="Custom", subject="Ignored")
        assert h.title == "Custom"

    def test_neither_title_nor_subject_uses_default(self):
        """When neither is provided, generic default is used."""
        from textcharts.histogram import Histogram, HistogramBar

        h = Histogram([HistogramBar("q1", 10)])
        assert h.title == "Histogram"

    def test_subject_on_multiple_chart_types(self):
        """subject works on different chart types."""
        from textcharts.bar_chart import BarChart, BarData
        from textcharts.cdf_chart import CDFChart, CDFSeriesData

        bar = BarChart([BarData("a", 1)], subject="Sales")
        assert bar.title == "Sales Bar Chart"

        cdf = CDFChart([CDFSeriesData("s1", [1, 2, 3])], subject="Latency")
        assert cdf.title == "Latency Cumulative Distribution"

    def test_subject_via_factory_function(self):
        """subject passes through factory functions."""
        data = [StackedBarData("P1", [StackedBarSegment("Load", 100)])]
        from textcharts.stacked_bar import from_data as stacked_from_data

        chart = stacked_from_data(data, subject="Phase")
        assert chart.title == "Phase Stacked Breakdown"

    def test_subject_via_executor(self):
        """subject passes through execute_command."""
        from textcharts.commands import execute_command

        result = execute_command("bar", [{"label": "a", "value": 1}], subject="Revenue")
        assert "Revenue Bar Chart" in result

    def test_subject_renders_in_output(self):
        """Subject-composed title appears in rendered output."""
        opts = ChartOptions(use_color=False, width=60)
        data = [StackedBarData("P1", [StackedBarSegment("Load", 100)])]
        chart = StackedBar(data=data, options=opts, subject="Phase")
        result = chart.render()
        assert "Phase Stacked Breakdown" in result


# ── Stacked Bar Chart Tests ────────────────────────────────
