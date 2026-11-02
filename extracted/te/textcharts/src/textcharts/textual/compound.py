"""Compound Textual widgets built from textcharts chart widgets."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Select, Static

from textcharts import ChartBase

from .widget import TextChart


class ChartSwitcher(Static):
    """Chart selector plus chart display for exploratory Textual apps."""

    chart_type = reactive("", init=False, repaint=False)
    data = reactive(None, init=False, repaint=False)

    class Changed(Message):
        """Posted when the active chart type changes."""

        def __init__(self, switcher: "ChartSwitcher", value: str) -> None:
            super().__init__()
            self.switcher = switcher
            self.value = value

    def __init__(
        self,
        charts: Mapping[str, Callable[[Any], ChartBase]],
        data: Any,
        *,
        initial: str | None = None,
        prompt: str = "Chart Type",
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        if not charts:
            raise ValueError("ChartSwitcher requires at least one chart builder")
        self._charts = dict(charts)
        self._prompt = prompt
        first_key = next(iter(self._charts))
        super().__init__("", id=id, classes=classes, disabled=disabled)
        self.set_reactive(ChartSwitcher.chart_type, initial or first_key)
        self.set_reactive(ChartSwitcher.data, data)

    def compose(self) -> ComposeResult:
        options = [(name.replace("_", " ").title(), name) for name in self._charts]
        yield Select(options, prompt=self._prompt, allow_blank=False, value=self.chart_type, id="chart-type")
        yield TextChart(self._build_chart, id="chart-view")

    def on_mount(self) -> None:
        self._refresh_chart()

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "chart-type" and isinstance(event.value, str):
            self.chart_type = event.value

    def watch_chart_type(self, *_: object) -> None:
        if self.is_mounted:
            self._refresh_chart()
            self.post_message(self.Changed(self, self.chart_type))

    def watch_data(self, *_: object) -> None:
        if self.is_mounted:
            self._refresh_chart()

    def _build_chart(self) -> ChartBase:
        return self._charts[self.chart_type](self.data)

    def _refresh_chart(self) -> None:
        self.query_one(TextChart).chart = self._build_chart()
