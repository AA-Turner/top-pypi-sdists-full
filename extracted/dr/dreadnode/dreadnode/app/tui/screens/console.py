"""Console log viewer — browser DevTools-style backend log inspection."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, ClassVar

from rich.text import Text
from textual import on
from textual.binding import Binding
from textual.message import Message
from textual.widgets import RichLog, Static

from dreadnode.app import paths
from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.theme import (
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

    from dreadnode.core.log import LogBuffer, LogEntry

_LEVEL_COLORS: dict[str, str] = {
    "TRACE": FG_FAINTEST,
    "DEBUG": FG_MUTED,
    "INFO": INFO,
    "SUCCESS": SUCCESS,
    "WARNING": WARNING,
    "ERROR": ERROR,
    "CRITICAL": ERROR,
}

_LEVELS = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
# Cap per-entry rendered length so cycling to TRACE doesn't freeze the UI on
# full LLM request/response payloads. Buffer + saved log still keep the full text.
_MAX_DISPLAY_CHARS = 2000


class ConsoleScreen(DreadnodeScreen):
    """Browser DevTools-style log viewer."""

    class LogEntryAdded(Message):
        """Thread-safe log entry delivery for the console screen."""

        def __init__(self, entry: LogEntry) -> None:
            self.entry = entry
            super().__init__()

    BINDINGS: ClassVar[list[Binding]] = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("l", "cycle_level", "Level", show=True),
        Binding("c", "copy_logs", "Copy", show=True),
        Binding("s", "save_logs", "Save", show=True),
        Binding("r", "report_bug", "Report bug", show=True),
        Binding("x", "clear_logs", "Clear", show=True),
        Binding("j", "scroll_down", show=False),
        Binding("k", "scroll_up", show=False),
        Binding("g", "scroll_top", show=False),
        Binding("G", "scroll_bottom", show=False),
    ]

    def __init__(self, log_buffer: LogBuffer, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._log_buffer = log_buffer
        self._level_index = 2  # INFO
        self._min_level_no = self._resolve_level_no(_LEVELS[self._level_index])

    @staticmethod
    def _resolve_level_no(name: str) -> int:
        from loguru import logger as _logger

        return _logger.level(name).no

    def compose_content(self) -> ComposeResult:
        yield Static(self._title_markup(), id="console-title")
        yield RichLog(
            id="console-log",
            wrap=True,
            highlight=False,
            markup=False,
            max_lines=5000,
        )

    def on_mount(self) -> None:
        super().on_mount()
        rich_log = self.query_one("#console-log", RichLog)
        for entry in self._log_buffer.snapshot():
            if entry.level_no >= self._min_level_no:
                rich_log.write(self._format_entry(entry))
        self._log_buffer.add_listener(self._on_new_entry)
        rich_log.scroll_end(animate=False)

    def on_unmount(self) -> None:
        self._log_buffer.remove_listener(self._on_new_entry)

    # -- Listener (called from any thread) --

    def _on_new_entry(self, entry: LogEntry) -> None:
        if entry.level_no >= self._min_level_no:
            self.post_message(self.LogEntryAdded(entry))

    @on(LogEntryAdded)
    def _on_log_entry_added(self, message: LogEntryAdded) -> None:
        self._append_entry(message.entry)

    def _append_entry(self, entry: LogEntry) -> None:
        # A LogEntryAdded message can already be queued when the screen is
        # popped — don't let a dead widget tree turn a log line into a crash.
        if not self.is_mounted:
            return
        self.query_one("#console-log", RichLog).write(self._format_entry(entry))

    # -- Formatting --

    @staticmethod
    def _format_entry(entry: LogEntry) -> Text:
        color = _LEVEL_COLORS.get(entry.level, FG_SUBTLE)
        t = Text()
        t.append(entry.timestamp.strftime("%H:%M:%S.%f")[:12], style=FG_FAINTEST)
        t.append(" ")
        t.append(f"{entry.level:<8}", style=color)
        t.append(f" {entry.source}", style=FG_MUTED)
        msg = entry.message
        if len(msg) > _MAX_DISPLAY_CHARS:
            extra = len(msg) - _MAX_DISPLAY_CHARS
            t.append(f"  {msg[:_MAX_DISPLAY_CHARS]}")
            t.append(f" …[+{extra:,} chars]", style=FG_FAINTEST)
        else:
            t.append(f"  {msg}")
        return t

    def _title_markup(self) -> str:
        level = _LEVELS[self._level_index]
        color = _LEVEL_COLORS.get(level, FG_SUBTLE)
        return f"[bold {FG}] Console[/]  [bold {color}]{level}[/]\n[{FG_FAINTEST}] Runtime server log output[/]"

    def _update_title(self) -> None:
        self.query_one("#console-title", Static).update(self._title_markup())

    # -- Actions --

    def action_go_back(self) -> None:
        self.dismiss()

    def action_cycle_level(self) -> None:
        # Cycle toward more-verbose first (INFO → DEBUG → TRACE …) so the
        # common "I want a bit more detail" step doesn't have to wrap through
        # WARNING/ERROR/CRITICAL.
        self._level_index = (self._level_index - 1) % len(_LEVELS)
        level = _LEVELS[self._level_index]
        self._min_level_no = self._resolve_level_no(level)
        self._refresh_log()
        self._update_title()

    def action_copy_logs(self) -> None:
        lines = [
            f"{e.timestamp.strftime('%H:%M:%S')} {e.level:<8} {e.source}  {e.message}"
            for e in self._log_buffer.snapshot()
            if e.level_no >= self._min_level_no
        ]
        self.app.copy_to_clipboard("\n".join(lines))
        self.notify(f"Copied {len(lines)} lines to clipboard")

    def action_save_logs(self) -> None:
        filename = f"dreadnode-logs-{datetime.now(tz=UTC).strftime('%Y%m%d-%H%M%S')}.log"
        lines = [
            f"{e.timestamp.isoformat()} {e.level:<8} {e.source}  {e.message}"
            for e in self._log_buffer.snapshot()
            if e.level_no >= self._min_level_no
        ]
        # Exports share the central dreadnode logs directory with worker logs.
        # Read at call time: a by-name import would freeze the path at import.
        export_dir = paths.LOGS_DIR
        export_dir.mkdir(parents=True, exist_ok=True)
        output_path = export_dir / filename
        output_path.write_text("\n".join(lines), encoding="utf-8", errors="replace")
        self.notify(f"Saved to {output_path}")

    def action_report_bug(self) -> None:
        handler = getattr(self.app, "action_report_bug", None)
        if callable(handler):
            handler("console")

    def action_clear_logs(self) -> None:
        self._log_buffer.clear()
        self.query_one("#console-log", RichLog).clear()
        self.notify("Cleared")

    def action_scroll_down(self) -> None:
        self.query_one("#console-log", RichLog).scroll_down()

    def action_scroll_up(self) -> None:
        self.query_one("#console-log", RichLog).scroll_up()

    def action_scroll_top(self) -> None:
        self.query_one("#console-log", RichLog).scroll_home()

    def action_scroll_bottom(self) -> None:
        self.query_one("#console-log", RichLog).scroll_end()

    # -- Internal --

    def _refresh_log(self) -> None:
        rich_log = self.query_one("#console-log", RichLog)
        rich_log.clear()
        for entry in self._log_buffer.snapshot():
            if entry.level_no >= self._min_level_no:
                rich_log.write(self._format_entry(entry))
        rich_log.scroll_end(animate=False)
