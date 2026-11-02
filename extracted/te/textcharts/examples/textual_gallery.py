"""Gallery app showing every textcharts renderer inside Textual."""

from __future__ import annotations

from textual.app import App, ComposeResult

from textcharts import (
    BarChart,
    BarData,
    BoxPlot,
    BoxPlotSeries,
    CDFChart,
    CDFSeriesData,
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
from textcharts.textual import ChartSwitcher


def _gallery_builders():
    return {
        "bar": lambda _: BarChart([BarData("DuckDB", 128.0), BarData("Polars", 164.0)], title="Bar"),
        "histogram": lambda _: Histogram([HistogramBar("Q1", 11.0), HistogramBar("Q2", 15.0)], title="Histogram"),
        "heatmap": lambda _: Heatmap(
            [[12.0, 18.0], [9.0, 14.0]],
            ["Q1", "Q2"],
            ["DuckDB", "Polars"],
            title="Heatmap",
        ),
        "boxplot": lambda _: BoxPlot([BoxPlotSeries("North", [10, 12, 14, 16, 18])], title="Box Plot"),
        "line": lambda _: LineChart([LinePoint("Runtime", 1, 10.0), LinePoint("Runtime", 2, 13.0)], title="Line"),
        "scatter": lambda _: ScatterPlot([ScatterPoint("A", 1.0, 2.0), ScatterPoint("B", 2.0, 1.6)], title="Scatter"),
        "comparison": lambda _: ComparisonBar([ComparisonBarData("Q1", 11.0, 9.0)], title="Comparison"),
        "diverging": lambda _: DivergingBar(
            [DivergingBarData("DuckDB", -8.0), DivergingBarData("Polars", 4.5)],
            title="Diverging",
        ),
        "summary": lambda _: SummaryBox(SummaryStats(title="Summary", primary_value=14.2, num_items=2)),
        "percentile": lambda _: PercentileLadder(
            [PercentileData("DuckDB", 10.0, 14.0, 15.0, 18.0)],
            title="Percentile",
        ),
        "speedup": lambda _: NormalizedSpeedup(
            [SpeedupData("DuckDB", 1.0, True), SpeedupData("Polars", 0.82)],
            title="Speedup",
        ),
        "stacked": lambda _: StackedBar(
            [
                StackedBarData(
                    "DuckDB",
                    [StackedBarSegment("Scan", 8.0), StackedBarSegment("Join", 3.0)],
                )
            ],
            title="Stacked",
        ),
        "sparkline": lambda _: SparklineTable(
            SparklineTableData(
                rows=["DuckDB", "Polars"],
                columns=[SparklineColumn("Latency", {"DuckDB": 10.0, "Polars": 13.0})],
            ),
            title="Sparkline",
        ),
        "cdf": lambda _: CDFChart([CDFSeriesData("DuckDB", [1.0, 2.0, 3.0, 4.0])], title="CDF"),
        "rank": lambda _: RankTable(
            RankTableData(
                items=["Q1", "Q2"],
                groups=["DuckDB", "Polars"],
                values={
                    ("DuckDB", "Q1"): 10.0,
                    ("Polars", "Q1"): 12.0,
                    ("DuckDB", "Q2"): 11.0,
                    ("Polars", "Q2"): 9.0,
                },
            ),
            title="Rank",
        ),
    }


class TextualGalleryApp(App[None]):
    BINDINGS = [("t", "toggle_theme", "Toggle Theme"), ("q", "quit", "Quit")]
    CSS = """
    Screen {
        layout: vertical;
    }

    ChartSwitcher {
        height: 1fr;
    }

    #chart-view {
        height: 1fr;
        border: round $accent;
        margin: 1 2;
    }

    #chart-type {
        margin: 1 2 0 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield ChartSwitcher(_gallery_builders(), {}, initial="bar", prompt="Choose Chart")

    def action_toggle_theme(self) -> None:
        self.theme = "textual-light" if self.current_theme.dark else "textual-dark"


if __name__ == "__main__":
    TextualGalleryApp().run()
