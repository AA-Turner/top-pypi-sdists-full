"""Zone 4 — Global nav bar with connection status and app navigation.

Always visible, even on pushed full-screen views. Shows:
  Left:  ✓ local · org/workspace
  Right: ^P capabilities  ^B sessions  ^O workspaces  ^R runtimes  ^T traces  ^E evals

This bar owns connection health and pre-connect boot progress. Once the
runtime is connected, agent/turn activity belongs to SessionContextBar
(Zone 1) and ToolProgress.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.cells import cell_len
from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

if TYPE_CHECKING:
    from textual.timer import Timer

from dreadnode.app.tui.status_messages import STATUS_STARTING
from dreadnode.app.tui.theme import (
    ACCENT,
    BG,
    FG_FAINTEST,
    FG_MUTED,
    SUCCESS,
    WARNING,
)


def _pad_right(left: Text, right: Text, width: int, padding: int = 4) -> Text:
    """Join left and right text with space-fill to target width."""
    gap = max(width - cell_len(left.plain) - cell_len(right.plain) - padding, 1)
    result = Text(no_wrap=True, overflow="ellipsis")
    result.append_text(left)
    result.append(" " * gap)
    result.append_text(right)
    return result


_SPINNER = "⣾⣽⣻⢿⡿⣟⣯⣷"


class StatusBar(Static):
    """Single-line global nav bar — runtime health + navigation."""

    DEFAULT_CSS = f"""
    StatusBar {{
        height: auto;
        max-height: 2;
        padding: 1 2 0 2;
        color: {FG_FAINTEST};
        background: {BG};
    }}
    """

    connection: reactive[str] = reactive("local")
    workspace_label: reactive[str] = reactive("")
    runtime_connected: reactive[bool] = reactive(False)
    connection_status: reactive[str] = reactive("")
    boot_status: reactive[str] = reactive(STATUS_STARTING)
    update_available: reactive[str] = reactive("")
    remote_info: reactive[str] = reactive("")

    _spinner_frame: int = 0
    _spinner_timer: Timer | None = None
    _mounted: bool = False

    def on_mount(self) -> None:
        self._mounted = True
        self._sync_spinner()

    def watch_runtime_connected(self, _value: bool) -> None:
        if not self._mounted:
            return
        self._sync_spinner()

    def watch_connection_status(self, _value: str) -> None:
        if not self._mounted:
            return
        self._sync_spinner()

    def _sync_spinner(self) -> None:
        # Spin only while actively connecting (not connected, no terminal error).
        should_spin = not self.runtime_connected and not self.connection_status
        if should_spin:
            if self._spinner_timer is None:
                self._spinner_timer = self.set_interval(0.08, self._tick_spinner)
        elif self._spinner_timer is not None:
            self._spinner_timer.stop()
            self._spinner_timer = None

    def _tick_spinner(self) -> None:
        self._spinner_frame = (self._spinner_frame + 1) % len(_SPINNER)
        self.refresh()

    def render(self) -> Text:
        w = self.size.width

        # === Left: connection status ===
        left = Text(no_wrap=True, overflow="ellipsis")

        if self.runtime_connected:
            left.append("✓ ", style=SUCCESS)
            left.append(self.connection, style=FG_MUTED)
        elif self.connection_status:
            left.append("⚠ ", style=WARNING)
            left.append(self.connection_status, style=WARNING)
        else:
            left.append(f"{_SPINNER[self._spinner_frame]} ", style=ACCENT)
            left.append(self.boot_status.strip() or STATUS_STARTING, style=FG_FAINTEST)

        if self.workspace_label and self.runtime_connected:
            left.append(" · ", style=FG_FAINTEST)
            left.append(self.workspace_label, style=FG_MUTED)

        if self.update_available:
            left.append(" · ", style=FG_FAINTEST)
            left.append(f"↑ {self.update_available}", style=WARNING)

        # === Right: navigation shortcuts ===
        # At narrow widths, drop labels and show keys only
        left_len = cell_len(left.plain)
        nav_items = [
            ("^P", "capabilities"),
            ("^B", "sessions"),
            ("^W", "workspaces"),
            ("^R", "runtimes"),
            ("^T", "traces"),
            ("^E", "evals"),
        ]
        # Full labels need ~60 chars, keys-only needs ~20
        show_labels = (w - left_len) > 65

        right = Text(no_wrap=True)
        for i, (key, label) in enumerate(nav_items):
            right.append(key, style=FG_FAINTEST)
            if show_labels:
                right.append(f" {label}", style=FG_FAINTEST)
            if i < len(nav_items) - 1:
                right.append("  ", style=FG_FAINTEST)

        return _pad_right(left, right, w)
