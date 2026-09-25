"""Console log viewer — browser DevTools-style backend log inspection."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, ClassVar

import httpx
from rich.markup import escape
from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
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
from dreadnode.core.log import LogBuffer, LogEntry

if TYPE_CHECKING:
    from collections.abc import Callable

    from textual.timer import Timer

    from dreadnode.app.client.runtime_client import RuntimeClient
    from dreadnode.core.runtime_logs import RuntimeLogEntry

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
_PAGE_LIMIT = 200
# One poll replays a whole 2,000-entry runtime buffer in ten pages; the cap only
# bounds a server that keeps answering with full pages.
_MAX_PAGES_PER_POLL = 20


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
        Binding("tab", "toggle_source", "Source", show=False),
        Binding("c", "copy_logs", "Copy", show=True),
        Binding("s", "save_logs", "Save", show=True),
        Binding("r", "report_bug", "Report bug", show=True),
        Binding("x", "clear_logs", "Clear", show=True),
        Binding("j", "scroll_down", show=False),
        Binding("k", "scroll_up", show=False),
        Binding("g", "scroll_top", show=False),
        Binding("G", "scroll_bottom", show=False),
    ]

    def __init__(
        self,
        log_buffer: LogBuffer,
        remote_client: "Callable[[], RuntimeClient | None] | None" = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._log_buffer = log_buffer
        self._remote_client = remote_client
        self._runtime_source = False
        self._runtime_buffer = LogBuffer(maxlen=2000)
        self._client: RuntimeClient | None = None
        self._runtime_url = ""
        self._instance_id: str | None = None
        self._cursor = 0
        self._runtime_status = ""
        self._refresh_timer: Timer | None = None
        self._polling = False
        self._generation = 0
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
        for entry in self._active_buffer().snapshot():
            if entry.level_no >= self._min_level_no:
                rich_log.write(self._format_entry(entry))
        self._log_buffer.add_listener(self._on_new_entry)
        rich_log.scroll_end(animate=False)
        self._start_refresh()

    def on_unmount(self) -> None:
        self._log_buffer.remove_listener(self._on_new_entry)
        self._stop_refresh()

    def on_screen_suspend(self) -> None:
        self._stop_refresh()

    def on_screen_resume(self) -> None:
        self._start_refresh()

    def _stop_refresh(self) -> None:
        self._cancel_poll()
        if self._refresh_timer is not None:
            self._refresh_timer.stop()
            self._refresh_timer = None

    def _cancel_poll(self) -> None:
        """Drop any in-flight request so the next poll can start immediately."""
        self._generation += 1
        self.workers.cancel_group(self, "runtime-logs")
        self._polling = False

    def _start_refresh(self) -> None:
        if self._refresh_timer is None:
            self._refresh_timer = self.set_interval(2, self._request_poll)
        self._request_poll()

    def _sync_connection(self) -> None:
        client = self._remote_client() if self._remote_client else None
        url = client.server_url if client is not None else ""
        if client is self._client and url == self._runtime_url:
            return
        self._cancel_poll()
        self._client = client
        self._runtime_url = url
        self._runtime_buffer.clear()
        self._cursor = 0
        self._instance_id = None
        self._runtime_status = "Loading…" if client else ""
        if client is None:
            self._runtime_source = False
        self._refresh_log()
        self._update_title()

    def _request_poll(self) -> None:
        if not self.is_current:
            return
        # Observing local connection state does not make a runtime request.
        self._sync_connection()
        if not self._polling and self._runtime_source:
            self._poll_runtime()

    @work(exclusive=True, group="runtime-logs")
    async def _poll_runtime(self) -> None:
        self._polling = True
        generation = self._generation
        try:
            client = self._client
            if client is None:
                return
            restarted = False
            resynced = False
            for _ in range(_MAX_PAGES_PER_POLL):
                page = await client.query_logs(
                    after=self._cursor,
                    instance_id=self._instance_id,
                    # Fetch all captured levels so changing the display filter also
                    # works on the retained history without a new snapshot.
                    level="debug",
                    limit=_PAGE_LIMIT,
                )
                if (
                    generation != self._generation
                    or not self.is_mounted
                    or not self._runtime_source
                    or not self._remote_client
                    or self._remote_client() is not client
                    or client.server_url != self._runtime_url
                ):
                    return
                if page.reset:
                    restarted = True
                    self._runtime_buffer.clear()
                    self._refresh_log()
                    self._instance_id = page.instance_id
                    if not resynced:
                        # The reset page is a tail of the new process; replay it
                        # from its first record instead so history stays complete.
                        resynced = True
                        self._cursor = 0
                        continue
                self._instance_id = page.instance_id
                self._cursor = page.next_cursor
                for entry in page.entries:
                    captured = self._to_local_entry(entry)
                    self._runtime_buffer.push(captured)
                    if captured.level_no >= self._min_level_no:
                        self._append_entry(captured)
                if page.gap:
                    self.notify("Runtime log buffer overflowed; older entries were dropped")
                if len(page.entries) < _PAGE_LIMIT:
                    break
            self._runtime_status = (
                "Runtime restarted; showing current process"
                if restarted
                else "Following (DEBUG and above)"
                if len(self._runtime_buffer)
                else "No runtime logs yet (DEBUG and above)"
            )
            self._update_title()
        except Exception as exc:
            if generation == self._generation and self.is_mounted:
                # Keep diagnostics in the view; logging each polling error would
                # itself flood the local process's diagnostic buffers.
                reason = (
                    f"HTTP {exc.response.status_code}"
                    if isinstance(exc, httpx.HTTPStatusError)
                    else type(exc).__name__
                )
                self._runtime_status = f"Unable to read runtime logs: {reason} (retrying)"
                self._update_title()
        finally:
            # A cancelled poll must not clear the flag of the one that replaced it.
            if generation == self._generation:
                self._polling = False

    @staticmethod
    def _to_local_entry(entry: "RuntimeLogEntry") -> LogEntry:
        # The local sink stores naive local wall-clock time; runtime records
        # arrive tz-aware in the server's zone. Show both sources on one clock.
        timestamp = entry.timestamp
        if timestamp.tzinfo is not None:
            timestamp = timestamp.astimezone().replace(tzinfo=None)
        return LogEntry(
            timestamp=timestamp,
            level=entry.level,
            source=entry.source,
            message=entry.message + (" …[truncated]" if entry.truncated else ""),
            level_no=entry.level_no,
        )

    def _active_buffer(self) -> LogBuffer:
        return self._runtime_buffer if self._runtime_source else self._log_buffer

    def action_toggle_source(self) -> None:
        self._sync_connection()
        if self._client is None:
            return
        self._cancel_poll()
        self._runtime_source = not self._runtime_source
        self._refresh_log()
        self._update_title()
        self._request_poll()

    # -- Listener (called from any thread) --

    def _on_new_entry(self, entry: LogEntry) -> None:
        if not self._runtime_source and entry.level_no >= self._min_level_no:
            self.post_message(self.LogEntryAdded(entry))

    @on(LogEntryAdded)
    def _on_log_entry_added(self, message: LogEntryAdded) -> None:
        if not self._runtime_source:
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
        source = "Runtime server" if self._runtime_source else "Local process"
        detail = (
            f"{self._runtime_url} · {self._runtime_status}"
            if self._runtime_source
            else "Client and embedded runtime logs from this process"
        )
        if self._client is not None:
            detail += " · Tab: switch source"
        return (
            f"[bold {FG}] Console · {source}[/]  [bold {color}]{level}[/]"
            f"\n[{FG_FAINTEST}]{escape(detail)}[/]"
        )

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
            for e in self._active_buffer().snapshot()
            if e.level_no >= self._min_level_no
        ]
        self.app.copy_to_clipboard("\n".join(lines))
        self.notify(f"Copied {len(lines)} lines to clipboard")

    def action_save_logs(self) -> None:
        source = "runtime" if self._runtime_source else "local"
        filename = f"dreadnode-logs-{source}-{datetime.now(tz=UTC).strftime('%Y%m%d-%H%M%S')}.log"
        lines = [
            f"{e.timestamp.isoformat()} {e.level:<8} {e.source}  {e.message}"
            for e in self._active_buffer().snapshot()
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
        self._active_buffer().clear()
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
        for entry in self._active_buffer().snapshot():
            if entry.level_no >= self._min_level_no:
                rich_log.write(self._format_entry(entry))
        rich_log.scroll_end(animate=False)
