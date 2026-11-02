"""Textual widget adapters for rendering textcharts charts."""

from __future__ import annotations

from copy import copy
from dataclasses import replace
from typing import Any, Callable

from rich.text import Text
from textual import events
from textual.reactive import reactive
from textual.widgets import Static

from textcharts.base import ChartBase, ChartOptions, ColorMode, TerminalCapabilities
from textcharts.commands.registry import REGISTRY

ChartFactory = Callable[[], ChartBase]

_DATA_ATTR_BY_CLASS = {command.chart_class: command.data_param_name for command in REGISTRY.values()}


class TextChart(Static):
    """Render a textcharts chart inside a Textual app via Rich ANSI parsing."""

    chart = reactive(None, init=False, always_update=True)

    def __init__(
        self,
        chart: ChartBase | ChartFactory | None = None,
        *,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        self._chart_factory = chart if callable(chart) and not isinstance(chart, ChartBase) else None
        super().__init__("", id=id, classes=classes, disabled=disabled)
        if isinstance(chart, ChartBase):
            self.set_reactive(TextChart.chart, chart)

    def on_mount(self) -> None:
        """Watch the app theme so dark/light changes trigger a rerender."""
        theme_attr = "theme" if hasattr(self.app, "theme") else "dark" if hasattr(self.app, "dark") else None
        if theme_attr is not None:
            self.watch(self.app, theme_attr, self._handle_theme_change)
        elif self.chart is None and self._chart_factory is not None:
            self.refresh()

    def on_resize(self, _: events.Resize) -> None:
        """Refresh on resize so width/height are rebuilt from widget size."""
        self.refresh()

    def watch_chart(self, _: ChartBase | None) -> None:
        """Rerender when the wrapped chart instance changes."""
        self.refresh()

    def rebuild_chart(self) -> ChartBase:
        """Rebuild the wrapped chart from the stored factory."""
        if self._chart_factory is None:
            if self.chart is None:
                raise ValueError("TextChart has no chart or chart factory configured")
            return self.chart
        built_chart = self._chart_factory()
        self.chart = built_chart
        return built_chart

    def update_data(self, data: Any = None, /, **changes: Any) -> ChartBase:
        """Swap the underlying chart data and trigger a rerender."""
        chart = copy(self._resolve_chart())
        data_attr = _DATA_ATTR_BY_CLASS.get(chart.__class__.__name__)
        if data is not None:
            if data_attr == "matrix":
                changes.setdefault("matrix", data)
            elif data_attr is not None:
                changes.setdefault(data_attr, data)
            else:
                raise ValueError(f"Unsupported chart type for update_data: {chart.__class__.__name__}")

        for name, value in changes.items():
            setattr(chart, name, value)

        validator = getattr(chart, "_validate_dimensions", None)
        if callable(validator):
            validator()

        self._chart_factory = None
        self.chart = chart
        return chart

    def render(self) -> Text:
        """Render the wrapped chart as Rich Text."""
        chart = self._prepare_chart(self._resolve_chart())
        return Text.from_ansi(chart.render())

    def _resolve_chart(self) -> ChartBase:
        if self.chart is not None:
            return self.chart
        if self._chart_factory is None:
            raise ValueError("TextChart has no chart configured")
        return self._chart_factory()

    def _prepare_chart(self, chart: ChartBase) -> ChartBase:
        width = self.size.width or chart.options.width or 80
        height = self.size.height or chart.options.height or 24
        theme = "dark" if self._app_is_dark() else "light"
        capabilities = TerminalCapabilities(
            width=width,
            height=height,
            color_mode=ColorMode.TRUECOLOR,
            unicode_support=True,
            interactive=True,
        )

        # Shallow copy: chart data (lists, dataclasses) is shared with the
        # original.  Safe because we only mutate options/capabilities/height
        # on the copy, never the data collections themselves.
        prepared = copy(chart)
        prepared.options = replace(
            chart.options or ChartOptions(),
            width=width,
            height=height,
            use_color=True,
            use_unicode=True,
            theme=theme,
        )
        # Inject terminal capabilities directly — the chart render path reads
        # these private attributes to decide color mode, unicode, etc.
        prepared._capabilities = capabilities
        prepared.options._capabilities = capabilities

        if hasattr(prepared, "height") and isinstance(getattr(prepared, "height"), int):
            # Auto-fit the chart's internal plot height to the widget size,
            # but only when the chart carries the class default.  When a user
            # has set an explicit height (e.g. CDFChartWidget(chart_height=25)),
            # preserve their choice.
            cls_default = getattr(type(chart), "PLOT_HEIGHT", None)
            if cls_default is None or chart.height == cls_default:
                prepared.height = max(5, height - 4)

        return prepared

    def _app_is_dark(self) -> bool:
        try:
            current_theme = getattr(self.app, "current_theme", None)
        except Exception:
            return False
        if current_theme is not None and hasattr(current_theme, "dark"):
            return bool(current_theme.dark)
        return bool(getattr(self.app, "dark", False))

    def _handle_theme_change(self, *_: object) -> None:
        self.refresh()

