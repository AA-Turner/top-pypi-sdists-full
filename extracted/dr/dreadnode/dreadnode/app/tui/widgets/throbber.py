"""Animated gradient bar shown when the agent is busy."""

from __future__ import annotations

import time
from typing import TYPE_CHECKING, Any

from rich.color import Color
from rich.segment import Segment
from rich.style import Style as RichStyle
from textual.strip import Strip
from textual.visual import RenderOptions, Style, Visual
from textual.widget import Widget

if TYPE_CHECKING:
    from textual.css.styles import RulesMap

# Dreadnode orange gradient palette (dark -> orange -> bright -> orange -> dark)
_GRADIENT: list[Color] = [
    Color.parse("#1a0a04"),
    Color.parse("#3d1508"),
    Color.parse("#7a2a10"),
    Color.parse("#b8401a"),
    Color.parse("#ef562f"),
    Color.parse("#f4784f"),
    Color.parse("#f99a70"),
    Color.parse("#f4784f"),
    Color.parse("#ef562f"),
    Color.parse("#b8401a"),
    Color.parse("#7a2a10"),
    Color.parse("#3d1508"),
]
_GRADIENT_LEN = len(_GRADIENT)


class _ThrobberVisual(Visual):
    """Visual that renders a scrolling orange gradient bar."""

    def __init__(self, offset: float) -> None:
        self._offset = offset

    def render_strips(
        self,
        width: int,
        height: int | None,  # noqa: ARG002
        style: Style,  # noqa: ARG002
        options: RenderOptions,  # noqa: ARG002
    ) -> list[Strip]:
        offset = self._offset
        segments: list[Segment] = []
        for col in range(width):
            idx = (col + int(offset)) % _GRADIENT_LEN
            color = _GRADIENT[idx]
            segments.append(Segment("\u2584", RichStyle(color=color)))
        return [Strip(segments, width)]

    def get_optimal_width(self, rules: RulesMap, container_width: int) -> int:  # noqa: ARG002
        return container_width

    def get_height(self, rules: RulesMap, width: int) -> int:  # noqa: ARG002
        return 1


class Throbber(Widget):
    """Animated gradient bar shown during agent work."""

    DEFAULT_CSS = """
    Throbber {
        height: 1;
        display: none;
    }
    Throbber.-busy {
        display: block;
    }
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._start = time.monotonic()

    def on_mount(self) -> None:
        self.auto_refresh = 1 / 15

    def render(self) -> _ThrobberVisual:
        elapsed = time.monotonic() - self._start
        offset = elapsed * 12  # scroll speed: 12 cells/sec
        return _ThrobberVisual(offset)
