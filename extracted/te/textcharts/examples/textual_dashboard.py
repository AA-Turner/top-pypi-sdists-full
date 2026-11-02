"""Reactive dashboard example for textcharts Textual widgets."""

from __future__ import annotations

from random import Random

from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.reactive import reactive

from textcharts import BarData, LinePoint
from textcharts.textual import BarChartWidget, HeatmapWidget, LineChartWidget


class TextualDashboardApp(App[None]):
    BINDINGS = [("t", "toggle_theme", "Toggle Theme"), ("q", "quit", "Quit")]
    CSS = """
    Screen {
        layout: vertical;
    }

    Grid {
        grid-size: 2;
        grid-columns: 1fr 1fr;
        grid-rows: 1fr 1fr;
        grid-gutter: 1 2;
        padding: 1 2;
    }

    BarChartWidget, LineChartWidget, HeatmapWidget {
        border: round $accent;
        height: 1fr;
    }
    """

    throughput_data = reactive([BarData("DuckDB", 320.0), BarData("Polars", 280.0)], init=False)
    trend_points = reactive(
        [LinePoint("Latency", 1, 11.0), LinePoint("Latency", 2, 10.5), LinePoint("Latency", 3, 9.8)],
        init=False,
    )
    heatmap_matrix = reactive([[11.0, 14.0], [9.0, 12.0]], init=False)

    def __init__(self) -> None:
        super().__init__()
        self._rng = Random(7)
        self._tick = 3

    def compose(self) -> ComposeResult:
        with Grid():
            yield BarChartWidget(
                metric_label="ops/s",
                title="Throughput",
            ).data_bind(data=TextualDashboardApp.throughput_data)
            yield LineChartWidget(title="Latency Trend", x_label="Run", y_label="ms", show_trend=True).data_bind(
                data=TextualDashboardApp.trend_points
            )
            yield HeatmapWidget(
                row_labels=["Q1", "Q2"],
                col_labels=["DuckDB", "Polars"],
                value_label="ms",
                title="Query Heatmap",
            ).data_bind(matrix=TextualDashboardApp.heatmap_matrix)
            yield BarChartWidget(
                data=[BarData("Success", 99.0), BarData("Retry", 1.0)],
                metric_label="%",
                title="Status Mix",
            )

    def on_mount(self) -> None:
        self.set_interval(1.0, self._advance_data)

    def action_toggle_theme(self) -> None:
        self.theme = "textual-light" if self.current_theme.dark else "textual-dark"

    def _advance_data(self) -> None:
        self._tick += 1
        duck = 300.0 + self._rng.randint(-15, 20)
        polars = 270.0 + self._rng.randint(-12, 18)
        self.throughput_data = [BarData("DuckDB", duck), BarData("Polars", polars)]

        next_latency = max(6.0, 10.0 + self._rng.uniform(-1.5, 1.0))
        updated_points = self.trend_points[-5:] + [LinePoint("Latency", self._tick, next_latency)]
        self.trend_points = updated_points

        self.heatmap_matrix = [
            [10.0 + self._rng.uniform(-1.5, 1.5), 13.0 + self._rng.uniform(-1.5, 1.5)],
            [8.5 + self._rng.uniform(-1.0, 1.0), 11.5 + self._rng.uniform(-1.0, 1.0)],
        ]


if __name__ == "__main__":
    TextualDashboardApp().run()
