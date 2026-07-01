"""Sidebar combining session list and activity log."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from rich.text import Text
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import OptionList, RichLog, Static
from textual.widgets.option_list import Option

from dreadnode.app.tui.theme import (
    ACCENT,
    ERROR,
    FG,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    INFO,
    SUCCESS,
    WARNING,
)

if TYPE_CHECKING:
    from textual.app import ComposeResult


@dataclass(slots=True)
class SessionListEntry:
    """One session row rendered in the sidebar."""

    session_id: str
    caption: str
    message_count: int
    is_active: bool = False
    title: str | None = None


class SessionSidebar(Vertical):
    """Combined session list + activity log sidebar widget."""

    class SessionSelected(Message):
        """Posted when a session is selected from the list."""

        def __init__(self, session_id: str) -> None:
            self.session_id = session_id
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Static("\u2590 Sessions", id="sessions-heading", classes="sidebar-heading")
        yield OptionList(id="session-option-list")
        yield Static("\u2590 Activity", classes="sidebar-heading")
        yield RichLog(id="activity-log", wrap=True, highlight=True, markup=False)

    def set_entries(self, entries: list[SessionListEntry]) -> None:
        """Replace the session list with the given entries."""
        # Update heading with count
        heading = self.query_one("#sessions-heading", Static)
        count = len(entries)
        heading.update(f"\u2590 Sessions ({count})" if count else "\u2590 Sessions")

        option_list = self.query_one("#session-option-list", OptionList)
        option_list.clear_options()

        if not entries:
            empty_text = Text()
            empty_text.append("  No sessions yet\n", style=f"italic {FG_MUTED}")
            empty_text.append("  Ctrl+N to create one", style=FG_FAINTEST)
            option_list.add_option(Option(empty_text, disabled=True))
            return

        highlight_index: int | None = None
        for index, entry in enumerate(entries):
            label = Text()
            if entry.is_active:
                label.append("\u25cf ", style=ACCENT)
            else:
                label.append("\u25cb ", style=FG_FAINTEST)
            display_name = entry.title or entry.session_id[:8]
            label.append(display_name, style=FG if entry.is_active else FG_SUBTLE)
            label.append(f" {entry.caption}", style=FG_MUTED)
            label.append(f" ({entry.message_count})", style=FG_FAINTEST)
            option_list.add_option(Option(label, id=entry.session_id))
            if entry.is_active:
                highlight_index = index

        if highlight_index is not None:
            option_list.highlighted = highlight_index

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Forward session selection as a message."""
        option_id = event.option.id
        if option_id:
            self.post_message(self.SessionSelected(option_id))

    def write_activity(self, message: str, *, style: str = "info") -> None:
        """Write a timestamped event to the activity log."""
        color = {
            "info": INFO,
            "success": SUCCESS,
            "warning": WARNING,
            "error": ERROR,
        }.get(style, FG)
        timestamp = datetime.now().strftime("%H:%M:%S")  # noqa: DTZ005 — local display time
        line = Text()
        line.append(f"{timestamp} ", style=FG_FAINTEST)
        line.append(message, style=color)
        self.query_one("#activity-log", RichLog).write(line)
