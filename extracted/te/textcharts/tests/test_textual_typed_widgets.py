from __future__ import annotations

import asyncio

import pytest

pytest.importorskip("textual")

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Select

from textcharts import (
    BarData,
    BoxPlotSeries,
    CDFSeriesData,
    ComparisonBarData,
    DivergingBarData,
    HistogramBar,
    LinePoint,
    PercentileData,
    RankTableData,
    ScatterPoint,
    SparklineColumn,
    SparklineTableData,
    SpeedupData,
    StackedBarData,
    StackedBarSegment,
    SummaryStats,
)
from textcharts.textual import (
    BarChartWidget,
    BoxPlotWidget,
    CDFChartWidget,
    ChartSwitcher,
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
    TextChart,
)


def test_bar_chart_widget_reactive_updates():
    class BarApp(App[None]):
        def compose(self) -> ComposeResult:
            yield BarChartWidget(data=[BarData("A", 1.0)], metric_label="ms")

    async def run() -> None:
        app = BarApp()
        async with app.run_test(size=(90, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one(BarChartWidget)
            assert "A" in widget.render().plain
            widget.data = [BarData("B", 2.0)]
            await pilot.pause()
            assert "B" in widget.render().plain

    asyncio.run(run())


def test_line_and_heatmap_widgets_rebuild_when_reactives_change():
    class TypedApp(App[None]):
        CSS = "LineChartWidget, HeatmapWidget { height: 12; }"

        def compose(self) -> ComposeResult:
            yield LineChartWidget(data=[LinePoint("S", 1, 10.0), LinePoint("S", 2, 15.0)], show_trend=False)
            yield HeatmapWidget(matrix=[[1.0, 2.0]], row_labels=["Q1"], col_labels=["DuckDB", "Polars"])

    async def run() -> None:
        app = TypedApp()
        async with app.run_test(size=(100, 32)) as pilot:
            await pilot.pause()
            line = app.query_one(LineChartWidget)
            heatmap = app.query_one(HeatmapWidget)

            assert "Line Chart" in line.render().plain
            assert "Q1" in heatmap.render().plain

            line.show_trend = True
            heatmap.matrix = [[3.0, 4.0]]
            await pilot.pause()

            assert "Line Chart" in line.render().plain
            assert "4" in heatmap.render().plain

    asyncio.run(run())


def test_data_bind_updates_child_chart_widget():
    class BindingApp(App[None]):
        data = reactive([BarData("A", 1.0)], init=False)

        def compose(self) -> ComposeResult:
            yield BarChartWidget(metric_label="ms").data_bind(BindingApp.data)

    async def run() -> None:
        app = BindingApp()
        async with app.run_test(size=(90, 24)) as pilot:
            await pilot.pause()
            widget = app.query_one(BarChartWidget)
            assert "A" in widget.render().plain
            app.data = [BarData("B", 2.0)]
            await pilot.pause()
            assert "B" in widget.render().plain

    asyncio.run(run())


def test_chart_switcher_swaps_chart_and_posts_message():
    class SwitcherApp(App[None]):
        def __init__(self) -> None:
            super().__init__()
            self.last_value: str | None = None

        def compose(self) -> ComposeResult:
            def build_bar(data: list[tuple[str, float]]):
                from textcharts import BarChart

                return BarChart([BarData(label, value) for label, value in data], title="Bar View")

            def build_line(data: list[tuple[str, float]]):
                from textcharts import LineChart

                return LineChart(
                    [
                        LinePoint("Series", index, value, label=label)
                        for index, (label, value) in enumerate(data, start=1)
                    ],
                    title="Line View",
                )

            yield ChartSwitcher({"bar": build_bar, "line": build_line}, [("A", 1.0), ("B", 2.0)], initial="bar")

        def on_chart_switcher_changed(self, message: ChartSwitcher.Changed) -> None:
            self.last_value = message.value

    async def run() -> None:
        app = SwitcherApp()
        async with app.run_test(size=(100, 24)) as pilot:
            await pilot.pause()
            switcher = app.query_one(ChartSwitcher)
            chart = switcher.query_one(TextChart)
            assert "Bar View" in chart.render().plain

            select = switcher.query_one(Select)
            select.value = "line"
            await pilot.pause()

            assert app.last_value == "line"
            assert "Line View" in chart.render().plain

    asyncio.run(run())


def test_all_typed_widgets_importable():
    widgets = [
        BarChartWidget,
        HistogramWidget,
        HeatmapWidget,
        BoxPlotWidget,
        LineChartWidget,
        ScatterPlotWidget,
        ComparisonBarWidget,
        DivergingBarWidget,
        SummaryBoxWidget,
        PercentileWidget,
        SpeedupWidget,
        StackedBarWidget,
        SparklineWidget,
        CDFChartWidget,
        RankTableWidget,
    ]
    assert len(widgets) == 15
    assert all(widget is not None for widget in widgets)


_TYPED_WIDGET_CASES = [
    (HistogramWidget, {"data": [HistogramBar("Q1", 10.0), HistogramBar("Q2", 14.0)]}),
    (BoxPlotWidget, {"data": [BoxPlotSeries("North", [1, 2, 3, 4, 5])]}),
    (ScatterPlotWidget, {"data": [ScatterPoint("A", 1.0, 2.0), ScatterPoint("B", 2.0, 1.0)]}),
    (ComparisonBarWidget, {"data": [ComparisonBarData("Q1", 10.0, 8.0)]}),
    (DivergingBarWidget, {"data": [DivergingBarData("Q1", -12.0), DivergingBarData("Q2", 7.5)]}),
    (SummaryBoxWidget, {"stats": SummaryStats(title="Test", primary_value=12.0, num_items=2)}),
    (PercentileWidget, {"data": [PercentileData("DuckDB", 10.0, 14.0, 15.0, 20.0)]}),
    (SpeedupWidget, {"data": [SpeedupData("DuckDB", 1.0, True), SpeedupData("Polars", 0.8, False)]}),
    (
        StackedBarWidget,
        {"data": [StackedBarData("DuckDB", [StackedBarSegment("Scan", 10.0), StackedBarSegment("Join", 5.0)])]},
    ),
    (
        SparklineWidget,
        {"data": SparklineTableData(rows=["DuckDB"], columns=[SparklineColumn("Latency", {"DuckDB": 10.0})])},
    ),
    (CDFChartWidget, {"data": [CDFSeriesData("DuckDB", [1.0, 2.0, 3.0, 4.0])]}),
    (
        RankTableWidget,
        {
            "data": RankTableData(
                items=["Q1", "Q2"],
                groups=["DuckDB", "Polars"],
                values={("DuckDB", "Q1"): 10.0, ("Polars", "Q1"): 12.0, ("DuckDB", "Q2"): 11.0, ("Polars", "Q2"): 9.0},
            )
        },
    ),
]


@pytest.mark.parametrize("widget_cls,kwargs", _TYPED_WIDGET_CASES, ids=[c[0].__name__ for c in _TYPED_WIDGET_CASES])
def test_typed_widget_renders_nonempty(widget_cls, kwargs):
    class SingleApp(App[None]):
        CSS = "* { height: 1fr; }"

        def compose(self) -> ComposeResult:
            yield widget_cls(**kwargs)

    async def run() -> None:
        app = SingleApp()
        async with app.run_test(size=(100, 30)) as pilot:
            await pilot.pause()
            widget = app.query_one(widget_cls)
            plain = widget.render().plain
            assert plain.strip(), f"{widget_cls.__name__} rendered empty output"

    asyncio.run(run())


def test_cdf_chart_widget_respects_explicit_chart_height():
    class CDFApp(App[None]):
        CSS = "CDFChartWidget { height: 30; }"

        def compose(self) -> ComposeResult:
            yield CDFChartWidget(
                data=[CDFSeriesData("S", [1, 2, 3, 4, 5])],
                chart_height=25,
                title="CDF Explicit Height",
            )

    async def run() -> None:
        app = CDFApp()
        async with app.run_test(size=(80, 40)) as pilot:
            await pilot.pause()
            widget = app.query_one(CDFChartWidget)
            prepared = widget._prepare_chart(widget._resolve_chart())
            # User set chart_height=25 (differs from CDFChart.PLOT_HEIGHT=15),
            # so _prepare_chart should preserve it instead of auto-fitting.
            assert prepared.height == 25

    asyncio.run(run())


def test_cdf_chart_widget_autofits_default_height():
    class CDFDefaultApp(App[None]):
        CSS = "CDFChartWidget { height: 30; }"

        def compose(self) -> ComposeResult:
            # No explicit chart_height — uses CDFChart.PLOT_HEIGHT default (15)
            yield CDFChartWidget(data=[CDFSeriesData("S", [1, 2, 3, 4, 5])], title="CDF Default")

    async def run() -> None:
        app = CDFDefaultApp()
        async with app.run_test(size=(80, 40)) as pilot:
            await pilot.pause()
            widget = app.query_one(CDFChartWidget)
            prepared = widget._prepare_chart(widget._resolve_chart())
            # Default chart_height=15 == CDFChart.PLOT_HEIGHT, so auto-fit applies
            assert prepared.height == max(5, 30 - 4)

    asyncio.run(run())
