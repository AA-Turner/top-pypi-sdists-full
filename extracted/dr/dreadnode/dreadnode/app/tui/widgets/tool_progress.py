"""Animated activity bar — braille spinner with contextual status.

Shows a single animated line during agent work:
  ⠋ thinking 1m 23s (esc to interrupt)
  ⠋ read_file 3.2s · 1m 23s (esc to interrupt)
  ⠋ streaming 1m 23s (esc to interrupt)
"""

from __future__ import annotations

import time
from typing import Any

from rich.text import Text
from textual.widget import Widget

from dreadnode.app.tui.theme import ACCENT, FG_FAINTEST, FG_MUTED

_FRAMES = "⣾⣷⣯⣟⡿⢿⣻⣽"


def _format_elapsed(seconds: float) -> str:
    """Format elapsed seconds as a compact human string."""
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    m, s = divmod(s, 60)
    if m < 60:
        return f"{m}m {s:02d}s"
    h, m = divmod(m, 60)
    return f"{h}h {m:02d}m"


class ToolProgress(Widget):
    """Animated activity indicator — shows spinner + status during agent work."""

    DEFAULT_CSS = f"""
    ToolProgress {{
        height: 1;
        padding: 0 2;
        color: {FG_FAINTEST};
    }}
    ToolProgress.-active {{
        color: {FG_MUTED};
    }}
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._label = ""
        self._tool_name = ""
        self._start = time.monotonic()
        self._turn_start: float | None = None
        self._mode = "idle"

    def show_activity(self, label: str = "thinking") -> None:
        """Show the spinner with a label."""
        if self._mode == "activity" and self._label == label and self.has_class("-active"):
            return
        self._label = label
        self._tool_name = ""
        # Only reset the per-item timer when transitioning from idle or tool.
        # activity→activity (e.g. thinking→streaming) keeps the timer continuous.
        if self._mode != "activity":
            self._start = time.monotonic()
        if self._turn_start is None:
            self._turn_start = self._start
        self._mode = "activity"
        self.add_class("-active")
        self.auto_refresh = 0.08

    def show_tool(self, tool_name: str) -> None:
        """Switch to showing a tool running."""
        if self._mode == "tool" and self._tool_name == tool_name and self.has_class("-active"):
            return
        self._label = ""
        self._tool_name = tool_name
        self._start = time.monotonic()
        if self._turn_start is None:
            self._turn_start = self._start
        self._mode = "tool"
        self.add_class("-active")
        self.auto_refresh = 0.08

    def hide_tool(self) -> None:
        """Hide the activity indicator."""
        if self._mode == "idle" and not self.has_class("-active"):
            return
        self._label = ""
        self._tool_name = ""
        self._mode = "idle"
        self._turn_start = None
        self.remove_class("-active")
        self.auto_refresh = None

    def render(self) -> Text:
        if self._mode == "idle":
            return Text("")

        now = time.monotonic()
        elapsed = now - self._start
        turn_elapsed = now - (self._turn_start or self._start)
        frame = _FRAMES[int(elapsed / 0.08) % len(_FRAMES)]

        t = Text()
        t.append(f"{frame} ", style=ACCENT)

        if self._mode == "tool":
            t.append(self._tool_name, style=FG_MUTED)
            t.append(f" {elapsed:.1f}s", style=FG_FAINTEST)
            t.append(f" · {_format_elapsed(turn_elapsed)}", style=FG_FAINTEST)
        else:
            t.append(self._label or "thinking", style=FG_MUTED)
            t.append(f" {_format_elapsed(turn_elapsed)}", style=FG_FAINTEST)

        t.append(" (esc to interrupt)", style=FG_FAINTEST)

        return t
