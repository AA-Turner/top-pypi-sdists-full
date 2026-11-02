from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("textual")

from textual.app import App, ComposeResult

import textcharts.textual.factories as textual_factories
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
from textcharts.base import ChartBase
from textcharts.textual import (
    TextChart,
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


class RecordingChart(ChartBase):
    def __init__(self, label: str, options: ChartOptions | None = None) -> None:
        super().__init__(options)
        self.label = label

    def render(self) -> str:
        return (
            f"{self.label} "
            f"width={self.options.width} "
            f"height={self.options.height} "
            f"theme={self.options.theme} "
            f"color={self.options.use_color} "
            f"unicode={self.options.use_unicode}"
        )


def test_textchart_renders_chart_content():
    class ChartApp(App[None]):
        def compose(self) -> ComposeResult:
            yield TextChart(BarChart([BarData("Alpha", 10.0), BarData("Beta", 20.0)], title="Latency"))

    async def run() -> None:
        app = ChartApp()
        async with app.run_test(size=(100, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one(TextChart)
            plain = widget.render().plain
            assert "Latency" in plain
            assert "Alpha" in plain
            assert "Beta" in plain

    asyncio.run(run())


def test_textchart_uses_widget_size_and_theme_bridge():
    class RecordingApp(App[None]):
        CSS = "TextChart { width: 70; height: 20; }"

        def compose(self) -> ComposeResult:
            yield TextChart(RecordingChart("probe"))

    async def run() -> None:
        app = RecordingApp()
        async with app.run_test(size=(100, 30)) as pilot:
            await pilot.pause()
            widget = app.query_one(TextChart)
            plain = widget.render().plain
            assert "probe" in plain
            assert "width=70" in plain
            assert "height=20" in plain
            assert "theme=dark" in plain
            assert "color=True" in plain
            assert "unicode=True" in plain

            app.theme = "textual-light"
            await pilot.pause()
            assert "theme=light" in widget.render().plain

    asyncio.run(run())


def test_textchart_chart_assignment_triggers_rerender():
    class ReassignApp(App[None]):
        def compose(self) -> ComposeResult:
            yield TextChart(RecordingChart("first"))

    async def run() -> None:
        app = ReassignApp()
        async with app.run_test(size=(80, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one(TextChart)
            assert "first" in widget.render().plain
            widget.chart = RecordingChart("second")
            await pilot.pause()
            assert "second" in widget.render().plain

    asyncio.run(run())


def test_textual_factory_helpers_build_widgets():
    class FactoryApp(App[None]):
        def compose(self) -> ComposeResult:
            yield text_chart("bar", [{"label": "A", "value": 1.0}, {"label": "B", "value": 2.0}], title="Raw")
            yield text_bar([BarData("X", 3.0), BarData("Y", 4.0)], title="Typed", widget_kwargs={"id": "typed"})

    async def run() -> None:
        app = FactoryApp()
        async with app.run_test(size=(100, 24)) as pilot:
            await pilot.pause()
            widgets = app.query(TextChart)
            plains = [widget.render().plain for widget in widgets]
            assert any("Raw" in plain and "A" in plain for plain in plains)
            assert any("Typed" in plain and "X" in plain for plain in plains)

    asyncio.run(run())


def test_update_data_bar_chart():
    class UpdateApp(App[None]):
        def compose(self) -> ComposeResult:
            yield TextChart(BarChart([BarData("Alpha", 10.0)], title="Before"))

    async def run() -> None:
        app = UpdateApp()
        async with app.run_test(size=(100, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one(TextChart)
            assert "Alpha" in widget.render().plain
            widget.update_data([BarData("Omega", 99.0)])
            await pilot.pause()
            assert "Omega" in widget.render().plain

    asyncio.run(run())


def test_update_data_heatmap_matrix():
    class HeatmapApp(App[None]):
        def compose(self) -> ComposeResult:
            yield TextChart(Heatmap([[1.0, 2.0]], ["R1"], ["C1", "C2"], title="HM"))

    async def run() -> None:
        app = HeatmapApp()
        async with app.run_test(size=(100, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one(TextChart)
            # update_data positional arg routes to "matrix" for Heatmap
            widget.update_data([[99.0, 88.0]])
            await pilot.pause()
            plain = widget.render().plain
            assert "HM" in plain

    asyncio.run(run())


def test_update_data_boxplot_with_series_attr():
    """Verify update_data routes positional data for charts with non-'data' attribute names."""

    class BoxApp(App[None]):
        def compose(self) -> ComposeResult:
            yield TextChart(BoxPlot([BoxPlotSeries("Old", [1, 2, 3])], title="Box"))

    async def run() -> None:
        app = BoxApp()
        async with app.run_test(size=(100, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one(TextChart)
            assert "Old" in widget.render().plain
            # BoxPlot stores data as self.series; _DATA_ATTR_BY_CLASS maps "BoxPlot" -> "series"
            widget.update_data([BoxPlotSeries("New", [10, 20, 30])])
            await pilot.pause()
            assert "New" in widget.render().plain

    asyncio.run(run())


def test_text_comparison_lower_is_better():
    class CompApp(App[None]):
        def compose(self) -> ComposeResult:
            yield text_comparison(
                [ComparisonBarData("Q1", 10.0, 8.0)],
                title="Comp",
                lower_is_better=False,
                widget_kwargs={"id": "comp"},
            )

    async def run() -> None:
        app = CompApp()
        async with app.run_test(size=(100, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one("#comp", TextChart)
            assert widget.chart is not None
            assert widget.chart.lower_is_better is False
            assert widget.render().plain.strip()

    asyncio.run(run())


def test_text_diverging_clip_pct_and_lower_is_better():
    class DivApp(App[None]):
        def compose(self) -> ComposeResult:
            yield text_diverging(
                [DivergingBarData("Q1", -12.0), DivergingBarData("Q2", 7.5)],
                title="Div",
                clip_pct=100.0,
                lower_is_better=False,
                widget_kwargs={"id": "div"},
            )

    async def run() -> None:
        app = DivApp()
        async with app.run_test(size=(100, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one("#div", TextChart)
            assert widget.chart is not None
            assert widget.chart.clip_pct == 100.0
            assert widget.chart.lower_is_better is False
            assert widget.render().plain.strip()

    asyncio.run(run())


# ---------------------------------------------------------------------------
# Factory coverage: verify each typed factory passes the right kwargs to its
# chart constructor.  These are synchronous — we call factory(), grab the
# stored chart, and render it directly.  A wrong kwarg name or missing
# required positional arg surfaces as a TypeError here, not in production.
# ---------------------------------------------------------------------------

_FACTORY_CASES: list[tuple[str, callable, dict]] = [
    (
        "text_histogram",
        lambda: text_histogram(
            [HistogramBar("Q1", 10.0), HistogramBar("Q2", 14.0)],
            title="H",
            y_label="ms",
            sort_by="value",
            max_per_chart=10,
            show_mean_line=False,
        ),
        {"title": "H"},
    ),
    (
        "text_heatmap",
        lambda: text_heatmap(
            [[1.0, 2.0], [3.0, 4.0]],
            ["R1", "R2"],
            ["C1", "C2"],
            title="HM",
            value_label="ms",
            x_label="Engines",
            show_values=False,
            color_scheme="sequential",
        ),
        {"title": "HM"},
    ),
    (
        "text_boxplot",
        lambda: text_boxplot(
            [BoxPlotSeries("North", [1, 2, 3, 4, 5])],
            title="BP",
            y_label="latency",
            show_stats=False,
            show_mean=False,
        ),
        {"title": "BP"},
    ),
    (
        "text_line",
        lambda: text_line(
            [LinePoint("S", 1, 10.0), LinePoint("S", 2, 15.0)],
            title="LN",
            x_label="Run",
            y_label="ms",
            show_trend=True,
        ),
        {"title": "LN"},
    ),
    (
        "text_scatter",
        lambda: text_scatter(
            [ScatterPoint("A", 1.0, 2.0), ScatterPoint("B", 2.0, 1.0)],
            title="SC",
            x_label="Lat",
            y_label="Thr",
            show_pareto=False,
        ),
        {"title": "SC"},
    ),
    (
        "text_summary",
        lambda: text_summary(
            SummaryStats(primary_value=12.0, num_items=2),
            title="SM Override",
        ),
        {"title": "SM Override"},
    ),
    (
        "text_percentile",
        lambda: text_percentile(
            [PercentileData("DuckDB", 10.0, 14.0, 15.0, 20.0)],
            title="PC",
            metric_label="ms",
        ),
        {"title": "PC"},
    ),
    (
        "text_speedup",
        lambda: text_speedup(
            [SpeedupData("DuckDB", 1.0, True), SpeedupData("Polars", 0.8, False)],
            title="SP",
            baseline_name="DuckDB",
        ),
        {"title": "SP"},
    ),
    (
        "text_stacked",
        lambda: text_stacked(
            [StackedBarData("DuckDB", [StackedBarSegment("Scan", 10.0), StackedBarSegment("Join", 5.0)])],
            title="ST",
            metric_label="ms",
        ),
        {"title": "ST"},
    ),
    (
        "text_sparkline",
        lambda: text_sparkline(
            SparklineTableData(
                rows=["DuckDB", "Polars"],
                columns=[SparklineColumn("Lat", {"DuckDB": 10.0, "Polars": 13.0})],
            ),
            title="SL",
        ),
        {"title": "SL"},
    ),
    (
        "text_cdf",
        lambda: text_cdf(
            [CDFSeriesData("DuckDB", [1.0, 2.0, 3.0, 4.0])],
            title="CDF",
            x_label="ms",
            y_label="Share",
            chart_height=10,
        ),
        {"title": "CDF"},
    ),
    (
        "text_rank",
        lambda: text_rank(
            RankTableData(
                items=["Q1", "Q2"],
                groups=["DuckDB", "Polars"],
                values={("DuckDB", "Q1"): 10.0, ("Polars", "Q1"): 12.0, ("DuckDB", "Q2"): 11.0, ("Polars", "Q2"): 9.0},
            ),
            title="RK",
        ),
        {"title": "RK"},
    ),
]


@pytest.mark.parametrize("name,build,checks", _FACTORY_CASES, ids=[c[0] for c in _FACTORY_CASES])
def test_typed_factory_produces_renderable_chart(name, build, checks):
    """Each factory must construct a chart whose render() succeeds with non-empty output."""
    widget = build()
    assert isinstance(widget, TextChart), f"{name} did not return a TextChart"
    chart = widget.chart
    assert chart is not None, f"{name} did not store a chart instance"
    output = chart.render()
    assert output.strip(), f"{name} chart rendered empty output"
    if "title" in checks:
        assert checks["title"] in output, f"{name} title not found in render output"


# ---------------------------------------------------------------------------
# _build_chart_instance: covers the generic text_chart() dispatch path
# including heatmap dict-unpacking, summary title replacement, subtitle/
# subject/options passthrough, and chart-specific kwargs filtering.
# ---------------------------------------------------------------------------


def test_text_chart_heatmap_dict_unpacking():
    """text_chart('heatmap', ...) parses a dict input and unpacks matrix/labels into the constructor."""
    widget = text_chart(
        "heatmap",
        {
            "matrix": [[1.0, 2.0], [3.0, 4.0]],
            "row_labels": ["R1", "R2"],
            "col_labels": ["C1", "C2"],
        },
        title="HM via text_chart",
    )
    output = widget.chart.render()
    assert "HM via text_chart" in output
    assert "R1" in output


def test_text_chart_heatmap_rejects_non_mapping_parser_output(monkeypatch):
    """Fail clearly if the heatmap parser contract regresses away from constructor kwargs."""
    monkeypatch.setattr(textual_factories, "parse_input", lambda command, data: ["not", "a", "mapping"])

    with pytest.raises(ValueError, match="heatmap parser must return a mapping"):
        text_chart(
            "heatmap",
            {
                "matrix": [[1.0]],
                "row_labels": ["R1"],
                "col_labels": ["C1"],
            },
        )


def test_text_chart_summary_title_replacement():
    """text_chart('summary', ..., title=...) replaces the title via dataclasses.replace()."""
    widget = text_chart(
        "summary",
        {"primary_value": 42.0, "num_items": 3},
        title="Replaced Title",
    )
    output = widget.chart.render()
    assert "Replaced Title" in output


def test_text_chart_passes_subtitle_subject_and_options():
    """text_chart() forwards subtitle, subject, and dict-form options to the chart."""
    widget = text_chart(
        "bar",
        [{"label": "A", "value": 1.0}],
        subtitle="sub-info",
        subject="MyBench",
        options={"width": 100, "theme": "dark"},
    )
    chart = widget.chart
    assert chart.subtitle == "sub-info"
    assert chart._subject == "MyBench"
    assert chart.options.width == 100
    assert chart.options.theme == "dark"


def test_text_chart_forwards_chart_specific_kwargs():
    """text_chart() forwards kwargs that match the command's chart_params."""
    widget = text_chart(
        "bar",
        [{"label": "X", "value": 5.0}],
        sort_by="label",
        metric_label="ops/s",
    )
    chart = widget.chart
    assert chart.sort_by == "label"
    assert chart.metric_label == "ops/s"


def test_all_chart_types_render_inside_textual():
    charts = [
        BarChart([BarData("Alpha", 10.0), BarData("Beta", 20.0)], title="Bar"),
        Histogram([HistogramBar("Q1", 10.0), HistogramBar("Q2", 14.0)], title="Histogram"),
        Heatmap([[1.0, 2.0], [3.0, 4.0]], ["Q1", "Q2"], ["A", "B"], title="Heatmap"),
        BoxPlot([BoxPlotSeries("North", [1, 2, 3, 4, 5])], title="Box"),
        LineChart([LinePoint("Series", 1, 10.0), LinePoint("Series", 2, 14.0)], title="Line"),
        ScatterPlot([ScatterPoint("A", 1.0, 2.0), ScatterPoint("B", 2.0, 1.0)], title="Scatter"),
        ComparisonBar([ComparisonBarData("Q1", 10.0, 8.0)], title="Comparison"),
        DivergingBar([DivergingBarData("Q1", -12.0), DivergingBarData("Q2", 7.5)], title="Diverging"),
        SummaryBox(SummaryStats(title="Summary", primary_value=12.0, num_items=2)),
        PercentileLadder([PercentileData("DuckDB", 10.0, 14.0, 15.0, 20.0)], title="Percentile"),
        NormalizedSpeedup([SpeedupData("DuckDB", 1.0, True), SpeedupData("Polars", 0.8, False)], title="Speedup"),
        StackedBar(
            [
                StackedBarData(
                    "DuckDB",
                    [StackedBarSegment("Scan", 10.0), StackedBarSegment("Join", 5.0)],
                )
            ],
            title="Stacked",
        ),
        SparklineTable(
            SparklineTableData(
                rows=["DuckDB", "Polars"],
                columns=[SparklineColumn("Latency", {"DuckDB": 10.0, "Polars": 13.0})],
            ),
            title="Sparkline",
        ),
        CDFChart([CDFSeriesData("DuckDB", [1.0, 2.0, 3.0, 4.0])], title="CDF"),
        RankTable(
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
    ]

    class GalleryApp(App[None]):
        CSS = "TextChart { height: 8; }"

        def compose(self) -> ComposeResult:
            for index, chart in enumerate(charts):
                yield TextChart(chart, id=f"chart-{index}")

    async def run() -> None:
        app = GalleryApp()
        async with app.run_test(size=(120, 60)) as pilot:
            await pilot.pause()
            widgets = list(app.query(TextChart))
            assert len(widgets) == 15
            assert all(widget.render().plain.strip() for widget in widgets)

    asyncio.run(run())


def test_textchart_dark_app_theme_applies_dark_palette():
    from textcharts.base import DARK_PALETTE

    dark_first = DARK_PALETTE[0].lstrip("#")
    dark_esc = (
        f"\033[38;2;{int(dark_first[0:2], 16)};{int(dark_first[2:4], 16)};{int(dark_first[4:6], 16)}m"
    )

    class DarkApp(App[None]):
        def compose(self) -> ComposeResult:
            yield TextChart(
                LineChart(
                    points=[
                        LinePoint(series="S", x=0, y=1.0),
                        LinePoint(series="S", x=1, y=2.0),
                    ],
                    title="Theme",
                )
            )

    async def run() -> None:
        app = DarkApp()
        async with app.run_test(size=(100, 30)) as pilot:
            await pilot.pause()
            widget = app.query_one(TextChart)
            prepared = widget._prepare_chart(widget.chart)
            assert prepared.options.theme == "dark"
            assert dark_esc in prepared.render()

    asyncio.run(run())
