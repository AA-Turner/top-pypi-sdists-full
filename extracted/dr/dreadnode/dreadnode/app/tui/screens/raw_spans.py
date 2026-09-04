"""Raw local spans.jsonl viewer for the active session."""

from __future__ import annotations

import asyncio
import json
import typing as t
from datetime import datetime

from rich.console import Group
from rich.syntax import Syntax
from rich.text import Text
from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import DataTable, Static

from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.spans_reader import RawSpansReader, SpanLineSummary
from dreadnode.app.tui.theme import FG, FG_FAINTEST, FG_MUTED, FG_SUBTLE, SYNTAX_THEME, WARNING

if t.TYPE_CHECKING:
    from pathlib import Path

    from textual.app import ComposeResult
    from textual.timer import Timer


def _format_timestamp(value: str) -> str:
    """Short timestamp for the row list."""
    if not value:
        return "-"
    try:
        return datetime.fromisoformat(value).strftime("%H:%M:%S")
    except ValueError:
        return value[:19]


def _display_status(value: str) -> str:
    return value or "unset"


class RawSpansScreen(DreadnodeScreen):
    """Inspect raw local span records from a JSONL file."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "close", "Close", show=True),
        Binding("r", "refresh_rows", "Refresh", show=True),
        Binding("f", "toggle_follow", "Follow", show=True),
    ]

    def __init__(self, path: Path, *, session_id: str | None = None, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._path = path
        self._session_id = session_id
        self._reader = RawSpansReader(path)
        self._selected_index = 0
        self._follow_enabled = False
        self._follow_timer: Timer | None = None

    def compose_content(self) -> ComposeResult:
        subtitle = (
            f"\n[{FG_FAINTEST}] Inspect the local JSONL span stream for the active session[/]"
        )
        yield Static(f"[bold {FG}] Raw Spans[/]{subtitle}", id="raw-spans-title")
        with Horizontal(id="raw-spans-body"):
            with Vertical(id="raw-spans-left"):
                yield DataTable(id="raw-spans-table")
            with Vertical(id="raw-spans-right"):
                yield Static("", id="raw-spans-path")
                with VerticalScroll(id="raw-spans-detail-scroll"):
                    yield Static("", id="raw-spans-detail")

    def on_mount(self) -> None:
        super().on_mount()
        table = self.query_one("#raw-spans-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("#", "Time", "Name", "Kind", "Status")
        table.focus()
        self._load_rows()

    def on_unmount(self) -> None:
        if self._follow_timer is not None:
            self._follow_timer.stop()
            self._follow_timer = None

    def action_close(self) -> None:
        self.dismiss()

    def action_refresh_rows(self) -> None:
        self._load_rows()

    def action_toggle_follow(self) -> None:
        self._follow_enabled = not self._follow_enabled
        if self._follow_enabled:
            if self._follow_timer is None:
                self._follow_timer = self.set_interval(1.0, self._poll_follow)
        elif self._follow_timer is not None:
            self._follow_timer.stop()
            self._follow_timer = None
        self._update_header()
        if self._follow_enabled:
            self._load_rows(preserve_selection=False)

    def _poll_follow(self) -> None:
        if self._follow_enabled:
            self._load_rows(preserve_selection=False)

    def _update_header(self) -> None:
        title = self.query_one("#raw-spans-title", Static)
        status = "follow on" if self._follow_enabled else "follow off"
        session_suffix = f"  [{FG_MUTED}]{self._session_id[:12]}[/]" if self._session_id else ""
        subtitle = f"\n[{FG_FAINTEST}] {len(self._reader.summaries)} rows · {status}[/]"
        title.update(f"[bold {FG}] Raw Spans[/]{session_suffix}{subtitle}")
        path_bar = self.query_one("#raw-spans-path", Static)
        path_bar.update(f" {self._path}")

    @work(exclusive=True, group="raw-spans")
    async def _load_rows(self, *, preserve_selection: bool = True) -> None:
        if not self.is_mounted:
            return
        await asyncio.to_thread(self._reader.refresh)
        if not self.is_mounted:
            return
        self._update_header()

        table = self.query_one("#raw-spans-table", DataTable)
        table.clear(columns=False)
        for summary in self._reader.summaries:
            table.add_row(
                str(summary.index + 1),
                _format_timestamp(summary.timestamp),
                summary.name,
                summary.kind or "-",
                _display_status(summary.status),
                key=str(summary.index),
            )

        if not self._reader.summaries:
            self.query_one("#raw-spans-detail", Static).update(
                "No local span rows found for this session yet."
            )
            return

        if self._follow_enabled:
            target_index = len(self._reader.summaries) - 1
        elif preserve_selection:
            target_index = min(self._selected_index, len(self._reader.summaries) - 1)
        else:
            target_index = 0

        self._selected_index = target_index
        table.move_cursor(row=target_index, animate=False)
        self._show_detail(target_index)

    @on(DataTable.RowHighlighted, "#raw-spans-table")
    def _on_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.row_key is None:
            return
        self._selected_index = int(str(event.row_key.value))
        self._show_detail(self._selected_index)

    def _detail_header(self, summary: SpanLineSummary) -> Text:
        text = Text()
        text.append(f"Line {summary.index + 1}", style=f"bold {FG}")
        text.append("\n")
        text.append(f"Name: {summary.name}\n", style=FG_SUBTLE)
        text.append(f"Time: {_format_timestamp(summary.timestamp)}\n", style=FG_MUTED)
        text.append(f"Kind: {summary.kind or '-'}\n", style=FG_MUTED)
        text.append(f"Status: {_display_status(summary.status)}\n", style=FG_MUTED)
        if summary.trace_id:
            text.append(f"Trace: {summary.trace_id}\n", style=FG_MUTED)
        if summary.span_id:
            text.append(f"Span: {summary.span_id}\n", style=FG_MUTED)
        if summary.error:
            text.append(f"Error: {summary.error}\n", style=WARNING)
        return text

    def _show_detail(self, index: int) -> None:
        summary = self._reader.summaries[index]
        record = self._reader.read_record(index)
        raw_line = self._reader.read_raw_line(index)
        payload = json.dumps(record, indent=2, sort_keys=True) if record is not None else raw_line
        renderable = Group(
            self._detail_header(summary),
            Text(""),
            Syntax(payload, "json", theme=SYNTAX_THEME, word_wrap=True),
        )
        self.query_one("#raw-spans-detail", Static).update(renderable)
