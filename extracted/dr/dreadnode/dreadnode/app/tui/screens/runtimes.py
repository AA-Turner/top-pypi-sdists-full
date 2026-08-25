"""Runtimes Browser screen -- discover, manage, and connect to workspace runtimes.

Single-column layout matching the capabilities screen pattern:
  List view:   header -> summary -> scrollable item list with cursor
  Detail view: runtime info -> action list with cursor
  Enter/c/s:   drill in or quick-action from list
  Esc:         detail->list or dismiss
"""

import asyncio
import secrets
import typing as t
from datetime import UTC, datetime

from loguru import logger
from rich.text import Text
from textual import events, on, work
from textual.containers import VerticalScroll
from textual.widgets import DataTable, Static

from dreadnode.app.tui.screens.base import (
    DreadnodeScreen,
    handle_search_input_key,
    handle_search_input_paste,
    render_hint_bar,
    render_screen_header,
    render_search_bar,
)
from dreadnode.app.tui.theme import (
    ACCENT,
    ERROR,
    FG,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    INFO,
    SUCCESS,
    TEAL,
    WARNING,
)

if t.TYPE_CHECKING:
    from textual.app import ComposeResult
    from textual.events import Key, Paste
    from textual.timer import Timer

    from dreadnode.app.api.client import ApiClient
    from dreadnode.app.client.models import RuntimeInfo
    from dreadnode.app.tui.connection import RuntimeConnectionManager


# ── Helpers ──────────────────────────────────────────────────────────────────

_PAUSE_REASONS: dict[str, str] = {
    "timeout": "timed out",
    "user": "by user",
    "insufficient_credits": "out of credits",
    "member_limit_exceeded": "member limit",
}

_STATE_ORDER = {"running": 0, "paused": 1, "idle": 2}


def _fmt_duration(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    mins = minutes % 60
    if hours < 24:
        return f"{hours}h{mins:02d}m" if mins else f"{hours}h"
    days = hours // 24
    remaining_hours = hours % 24
    if remaining_hours:
        return f"{days}d {remaining_hours}h"
    return f"{days}d"


def _runtime_limit_source_label(
    source_level: str | None,
    *,
    current_level: str = "l4_requested",
) -> str:
    source_names = {
        "l1_platform_max": "platform max",
        "l1_platform_default": "platform default",
        "l2_org_max": "organization max",
        "l3_org_default": "organization default",
        "l4_requested": "requested runtime",
    }
    if not source_level or source_level not in source_names:
        return "source unavailable"
    if source_level == current_level:
        return "set here"
    return f"inherited from {source_names[source_level]}"


def _expires_seconds(ts: str | datetime | None) -> int | None:
    """Seconds until expiration, or None if unknown."""
    if ts is None:
        return None
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            return None
    else:
        dt = ts
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return int((dt - datetime.now(tz=UTC)).total_seconds())


def _expires_label(seconds: int | None) -> str:
    if seconds is None:
        return ""
    if seconds <= 0:
        return "expired"
    return _fmt_duration(seconds)


def _expires_style(seconds: int | None) -> str:
    """Color urgency: red < 15m, yellow < 1h, default otherwise."""
    if seconds is None:
        return FG_SUBTLE
    if seconds <= 0:
        return ERROR
    if seconds < 900:  # 15 minutes
        return ERROR
    if seconds < 3600:  # 1 hour
        return WARNING
    return FG_SUBTLE


def _fmt_timestamp(ts: str | datetime | None) -> str:
    if ts is None:
        return ""
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            return ts[:19]
    else:
        dt = ts
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _relative_time(ts: str | datetime | None) -> str:
    """Human-friendly relative time like '3h ago' or 'just now'."""
    if ts is None:
        return ""
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            return ""
    else:
        dt = ts
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    delta = int((datetime.now(tz=UTC) - dt).total_seconds())
    if delta < 60:
        return "just now"
    if delta < 3600:
        return f"{delta // 60}m ago"
    if delta < 86400:
        return f"{delta // 3600}h ago"
    return f"{delta // 86400}d ago"


_STATE_STYLE: dict[str, tuple[str, str]] = {
    "running": (SUCCESS, "●"),
    "paused": (WARNING, "●"),
    "idle": (FG_FAINTEST, "◯"),
}


def _state_dot_and_style(state: str) -> tuple[str, str]:
    return _STATE_STYLE.get(state, (FG_FAINTEST, "◯"))


def _generate_runtime_key(project_key: str) -> str:
    """Return a unique-ish runtime key seeded by the project key.

    The 4-byte (8 hex char) suffix makes client-side collisions vanishingly
    unlikely; the server's (workspace, key) idempotency check would surface
    any actual collision as a no-op create rather than a duplicate.
    """
    return f"{project_key}-{secrets.token_hex(4)}"


def _build_actions(
    runtime: dict[str, t.Any],
    *,
    is_connected: bool,
    is_any_remote: bool,
) -> list[tuple[str, str]]:
    """Return (action_id, label) pairs relevant to this runtime's state."""
    state = runtime.get("status", "unknown")
    actions: list[tuple[str, str]] = []

    if state == "idle":
        actions.append(("start", "Start runtime"))
    elif state == "running":
        if is_connected:
            actions.append(("disconnect", "Disconnect"))
        else:
            actions.append(("connect", "Connect to runtime"))
        actions.append(("pause", "Pause runtime"))
        actions.append(("keepalive", "Extend expiration (+5 min)"))
    elif state == "paused":
        actions.append(("resume", "Resume runtime"))

    if state in ("running", "paused"):
        actions.append(("logs", "View server logs"))
        actions.append(("reset", "Reset (destroy sandbox)"))

    if is_any_remote and not is_connected:
        actions.append(("disconnect_other", "Disconnect from current remote"))

    return actions


def _parse_runtime_search(query: str) -> tuple[str, dict[str, str]]:
    """Split free text from lightweight `key:value` runtime filters."""
    text_terms: list[str] = []
    filters: dict[str, str] = {}

    for token in query.split():
        if ":" not in token:
            text_terms.append(token)
            continue
        key, value = token.split(":", 1)
        key = key.strip().lower()
        value = value.strip().lower()
        if key in {"state", "provider", "project", "connected"} and value:
            filters[key] = value
        else:
            text_terms.append(token)

    return (" ".join(text_terms).strip().lower(), filters)


def _filter_runtimes(
    runtimes: list[dict[str, t.Any]],
    query: str,
    *,
    project_name: t.Callable[[dict[str, t.Any]], str],
    connected_id: str | None,
) -> list[dict[str, t.Any]]:
    """Filter runtimes by free text and simple structured filters."""
    text_query, filters = _parse_runtime_search(query)
    results: list[dict[str, t.Any]] = []

    for runtime in runtimes:
        runtime_id = str(runtime.get("id", ""))
        state = str(runtime.get("status", "")).lower()
        instance = runtime.get("instance") or {}
        provider = str(instance.get("provider", "")).lower()
        project = project_name(runtime).lower()
        is_connected = runtime_id == connected_id

        if filters.get("state") and state != filters["state"]:
            continue
        if filters.get("provider") and provider != filters["provider"]:
            continue
        if filters.get("project") and filters["project"] not in project:
            continue
        if filters.get("connected"):
            wanted = filters["connected"] in {"1", "true", "yes", "y"}
            if is_connected != wanted:
                continue

        if text_query:
            haystack = " ".join(
                part
                for part in (
                    runtime_id.lower(),
                    state,
                    provider,
                    project,
                    str(runtime.get("project_id", "")).lower(),
                )
                if part
            )
            if text_query not in haystack:
                continue

        results.append(runtime)

    return results


# ── Main screen ──────────────────────────────────────────────────────────────


class RuntimeScreen(DreadnodeScreen):
    """Full-screen runtime manager -- browse, connect, manage."""

    def __init__(
        self,
        api: "ApiClient",
        org: str,
        workspace: str,
        project_key: str | None = None,
        requested_runtime_limit_seconds: int | None = None,
        connection_manager: "RuntimeConnectionManager | None" = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._api = api
        self._org = org
        self._workspace = workspace
        self._project_key = project_key
        self._requested_runtime_limit_seconds = requested_runtime_limit_seconds
        self._connection_manager = connection_manager

        self._runtimes: list[dict[str, t.Any]] = []
        self._project_names: dict[str, str] = {}  # project_id -> name
        self._refresh_timer: Timer | None = None

        # View state
        self._view: str = "list"  # "list", "detail", or "logs"
        self._cursor: int = 0
        self._action_cursor: int = 0
        self._search_query: str = ""
        self._visible_runtimes: list[dict[str, t.Any]] = []
        self._selected_runtime: dict[str, t.Any] | None = None
        self._current_actions: list[tuple[str, str]] = []
        self._logs_content: str | None = None

        # In-flight action tracking — blocks double-clicks and drives the
        # "Starting..." active state in the detail view. Mirrors the
        # pending-action pattern in capabilities.py.
        self._pending_action_runtime_id: str | None = None
        self._pending_action_label: str | None = None

    # ── Connected runtime helpers ────────────────────────────────────────

    @property
    def _connected_id(self) -> str | None:
        if self._connection_manager:
            return self._connection_manager.connected_runtime_id
        return None

    @property
    def _is_any_remote(self) -> bool:
        if self._connection_manager:
            return self._connection_manager.is_remote
        return False

    @property
    def _remote_info(self) -> "RuntimeInfo | None":
        if self._connection_manager:
            return self._connection_manager.remote_runtime_info
        return None

    def _project_name(self, runtime: dict[str, t.Any]) -> str:
        """Resolve project name from runtime data, falling back to cached or short ID."""
        # Prefer project_name/project_key from API response (no extra call needed)
        name = runtime.get("project_name") or runtime.get("project_key")
        if name:
            return name
        # Fall back to cached resolution
        project_id = str(runtime.get("project_id", ""))
        if not project_id:
            return ""
        return self._project_names.get(project_id, project_id[:8])

    # ── Compose ──────────────────────────────────────────────────────────

    def compose_content(self) -> "ComposeResult":
        yield Static(id="rt-header")
        yield Static(id="rt-search")
        yield DataTable(id="rt-table")
        with VerticalScroll(id="rt-detail-scroll", classes="-hidden"):
            yield Static(id="rt-content")
        yield Static(id="rt-hint-bar")

    def on_mount(self) -> None:
        super().on_mount()
        table = self.query_one("#rt-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns(
            "Project",
            "Runtime",
            "State",
            "Provider",
            "Expires",
            "Runtime",
            "Status",
        )
        self._render_header()
        self._render_hints()
        self._load_data()
        self._start_refresh_timer()

    def on_unmount(self) -> None:
        self._stop_refresh_timer()

    def on_screen_suspend(self, _event: events.ScreenSuspend) -> None:
        self._stop_refresh_timer()

    def on_screen_resume(self, _event: events.ScreenResume) -> None:
        self._load_data()
        self._start_refresh_timer()

    def _start_refresh_timer(self) -> None:
        if self._refresh_timer is None:
            self._refresh_timer = self.set_interval(10.0, self._load_data)

    def _stop_refresh_timer(self) -> None:
        if self._refresh_timer is not None:
            self._refresh_timer.stop()
            self._refresh_timer = None

    # ── Keyboard handling ────────────────────────────────────────────────

    def on_key(self, event: "Key") -> None:
        key = event.key

        # Let control sequences and function keys pass through
        if key.startswith("ctrl+") or (key.startswith("f") and key[1:].isdigit()):
            return

        handled = False
        if self._view == "logs":
            self._handle_logs_key(key)
            handled = True
        elif self._view == "detail":
            self._handle_detail_key(key)
            handled = True
        else:
            handled = self._handle_list_key(key, event)

        if handled:
            event.prevent_default()
            event.stop()

    def on_paste(self, event: "Paste") -> None:
        """Append bracketed-paste text to the search query (list view only)."""
        if self._view != "list":
            return
        result = handle_search_input_paste(self._search_query, text=event.text)
        if not result.handled:
            return
        self._search_query = result.new_query
        if result.cursor_should_reset:
            self._cursor = 0
        self._render_current_view()
        event.prevent_default()
        event.stop()

    def _handle_list_key(self, key: str, event: "Key") -> bool:
        if key == "enter":
            if self._visible_runtimes:
                self._open_detail()
            return True
        if key == "c":
            self._quick_connect()
            return True
        if key == "s":
            self._quick_start()
            return True
        if key == "n":
            self._create_new_runtime()
            return True
        if key == "space":
            return True
        if key == "escape":
            if self._search_query:
                self._search_query = ""
                self._cursor = 0
                self._render_current_view()
            else:
                self._stop_refresh_timer()
                self.dismiss()
            return True
        if key == "r":
            self._load_data()
            return True
        search_result = handle_search_input_key(
            self._search_query, key=key, character=event.character
        )
        if not search_result.handled:
            return False
        if search_result.new_query == self._search_query:
            return True
        self._search_query = search_result.new_query
        if search_result.cursor_should_reset:
            self._cursor = 0
        self._render_current_view()
        return True

    def _handle_logs_key(self, key: str) -> None:
        if key == "r":
            self._do_fetch_logs()
        elif key == "escape":
            self._logs_content = None
            self._view = "detail"
            self._render_current_view()

    def _handle_detail_key(self, key: str) -> None:
        total_actions = len(self._current_actions) + 1  # +1 for "Back"
        if key == "up":
            self._action_cursor = max(0, self._action_cursor - 1)
            self._render_current_view()
        elif key == "down":
            self._action_cursor = min(total_actions - 1, self._action_cursor + 1)
            self._render_current_view()
        elif key == "enter":
            if self._action_cursor >= len(self._current_actions):
                self._back_to_list()
            else:
                action_id = self._current_actions[self._action_cursor][0]
                self._execute_action(action_id)
        elif key == "escape":
            self._back_to_list()

    def _open_detail(self) -> None:
        if self._visible_runtimes and 0 <= self._cursor < len(self._visible_runtimes):
            self._selected_runtime = self._visible_runtimes[self._cursor]
            self._action_cursor = 0
            self._view = "detail"
            self._render_current_view()

    def _quick_connect(self) -> None:
        """Connect directly from list — skip detail view for running runtimes."""
        if self._is_app_busy() or self._is_action_pending():
            return
        selected = self._selected_list_runtime()
        if not selected:
            return
        state = selected.get("status", "")
        runtime_id = str(selected.get("id", ""))
        if state == "running" and runtime_id != self._connected_id:
            self._selected_runtime = selected
            self._view = "detail"
            self._do_connect(runtime_id, selected)
        elif runtime_id == self._connected_id:
            # Already connected — open detail to show disconnect option
            self._open_detail()

    def _quick_start(self) -> None:
        """Start directly from list — skip detail view for idle runtimes."""
        if self._is_app_busy() or self._is_action_pending():
            return
        selected = self._selected_list_runtime()
        if not selected:
            return
        if selected.get("status") == "idle":
            runtime_id = str(selected.get("id", ""))
            self._selected_runtime = selected
            self._view = "detail"
            # Synchronous notice — see _execute_action for the rationale.
            self._show_action_notice(runtime_id, "Starting")
            self._do_start(runtime_id)

    def _create_new_runtime(self) -> None:
        """Create a new runtime in the active project with an auto-generated key."""
        if self._is_app_busy() or self._is_action_pending():
            return
        if not self._project_key:
            self.notify(
                "No active project — use /projects to set one",
                title="Runtimes",
                severity="warning",
            )
            return
        new_key = _generate_runtime_key(self._project_key)
        self._show_action_notice("__new__", "Creating")
        self._do_create(new_key)

    def _selected_list_runtime(self) -> dict[str, t.Any] | None:
        if self._visible_runtimes and 0 <= self._cursor < len(self._visible_runtimes):
            return self._visible_runtimes[self._cursor]
        return None

    def _back_to_list(self) -> None:
        self._view = "list"
        self._render_current_view()

    # ── Rendering ────────────────────────────────────────────────────────

    def _render_current_view(self) -> None:
        # Workers (runtime-action, data loads) and the refresh interval re-render
        # via this path. If the screen has unmounted while a worker was awaiting,
        # query_one would crash with NoMatches — bail out before touching the DOM.
        if not self.is_mounted:
            return
        self._render_header()
        if self._view == "logs":
            self._render_logs_view()
        elif self._view == "detail":
            self._render_detail_view()
        else:
            self._render_list_view()
        self._render_hints()

    def _render_search(self) -> None:
        self.query_one("#rt-search", Static).update(
            render_search_bar(
                self._search_query,
                cursor=self._cursor,
                visible_count=len(self._visible_runtimes),
                placeholder=(
                    "Search\u2026  filters: state:running  provider:e2b  "
                    "project:default  connected:yes"
                ),
            )
        )

    def _render_header(self) -> None:
        self.query_one("#rt-header", Static).update(
            render_screen_header(
                "Runtimes",
                "Manage cloud sandbox runtimes for your workspace",
                count=len(self._runtimes) if self._runtimes else None,
            )
        )

    def _render_hints(self) -> None:
        if self._view == "logs":
            hints: list[tuple[str, str]] = [("R", "refresh"), ("Esc", "back")]
        elif self._view == "detail":
            hints = [("Enter", "select"), ("Esc", "back")]
        else:
            hints = [("Type", "search"), ("Enter", "details")]
            # Show contextual quick-action hints based on cursor
            selected = self._selected_list_runtime()
            if selected:
                state = selected.get("status", "")
                rid = str(selected.get("id", ""))
                if state == "running" and rid != self._connected_id:
                    hints.append(("C", "connect"))
                elif state == "idle":
                    hints.append(("S", "start"))
            if self._project_key:
                hints.append(("N", "new runtime"))
            hints.extend([("R", "refresh"), ("Esc", "close")])
        self.query_one("#rt-hint-bar", Static).update(render_hint_bar(hints))

    def _render_list_view(self) -> None:
        table = self.query_one("#rt-table", DataTable)
        detail_scroll = self.query_one("#rt-detail-scroll", VerticalScroll)
        self._visible_runtimes = _filter_runtimes(
            self._runtimes,
            self._search_query,
            project_name=self._project_name,
            connected_id=self._connected_id,
        )
        self._cursor = min(self._cursor, max(0, len(self._visible_runtimes) - 1))
        self._render_search()
        table.clear()

        if not self._runtimes or not self._visible_runtimes:
            table.add_class("-hidden")
            detail_scroll.remove_class("-hidden")
            text = Text()
            if not self._runtimes:
                text.append("  No runtimes found\n\n", style=FG_MUTED)
                if self._project_key:
                    text.append(
                        f"  Press N to create a runtime in '{self._project_key}'.\n",
                        style=FG_FAINTEST,
                    )
                else:
                    text.append(
                        "  Set a default project first, or create a runtime via the CLI.\n",
                        style=FG_FAINTEST,
                    )
            else:
                text.append("  No runtimes match the current search.\n", style=FG_MUTED)
            self.query_one("#rt-content", Static).update(text)
            return

        detail_scroll.add_class("-hidden")
        table.remove_class("-hidden")
        table.focus()

        for runtime in self._visible_runtimes:
            runtime_id = str(runtime.get("id", "?"))
            state = str(runtime.get("status", "unknown"))
            instance = runtime.get("instance") or {}
            provider = str(instance.get("provider", "")) or "-"
            project = self._project_name(runtime) or "-"
            exp_label = _expires_label(_expires_seconds(instance.get("expires_at"))) or "-"
            runtime_secs = int(instance.get("total_runtime_seconds", 0))
            duration = _fmt_duration(runtime_secs) if runtime_secs else "-"
            status = "connected" if runtime_id == self._connected_id else "-"
            table.add_row(
                project,
                runtime_id[:8],
                state,
                provider,
                exp_label,
                duration,
                status,
                key=runtime_id,
            )

        if self._visible_runtimes:
            table.move_cursor(row=self._cursor, column=0, animate=False, scroll=True)

    def _render_detail_view(self) -> None:
        runtime = self._selected_runtime
        if not runtime:
            return
        self.query_one("#rt-table", DataTable).add_class("-hidden")
        self.query_one("#rt-detail-scroll", VerticalScroll).remove_class("-hidden")

        runtime_id = str(runtime.get("id", "?"))
        state = runtime.get("status", "unknown")
        instance = runtime.get("instance") or {}
        is_connected = runtime_id == self._connected_id
        project_id = str(runtime.get("project_id", ""))
        project = self._project_name(runtime)

        text = Text()

        # Header: project name + state
        dot_style, dot = _state_dot_and_style(state)
        state_style = {"running": ACCENT, "paused": WARNING, "idle": FG_SUBTLE}.get(
            state, FG_SUBTLE
        )
        text.append(f" {dot} ", style=dot_style)
        if project and project != runtime_id[:8]:
            text.append(project, style=f"bold {FG}")
            text.append(f" · {runtime_id[:8]}", style=FG_FAINTEST)
        else:
            text.append(runtime_id[:8], style=f"bold {FG}")
        text.append(" · ", style=FG_FAINTEST)
        text.append(state, style=state_style)
        if is_connected:
            text.append(" · ", style=FG_FAINTEST)
            text.append("connected", style=SUCCESS)

        # Pause reason inline with header
        pause_reason = instance.get("pause_reason")
        if state == "paused" and pause_reason:
            reason_label = _PAUSE_REASONS.get(pause_reason, pause_reason)
            text.append(" · ", style=FG_FAINTEST)
            text.append(reason_label, style=WARNING)

        text.append("\n")

        # Provider + expiration as a compact subtitle
        provider = instance.get("provider", "")
        exp_secs = _expires_seconds(instance.get("expires_at"))
        exp_label = _expires_label(exp_secs)
        subtitle_parts: list[tuple[str, str]] = []
        if provider:
            subtitle_parts.append((provider, FG_MUTED))
        if exp_label:
            subtitle_parts.append((f"expires {exp_label}", _expires_style(exp_secs)))
        runtime_secs = int(instance.get("total_runtime_seconds", 0))
        if runtime_secs:
            subtitle_parts.append((f"{_fmt_duration(runtime_secs)} runtime", FG_MUTED))
        if subtitle_parts:
            text.append("   ")
            for j, (part, sty) in enumerate(subtitle_parts):
                if j > 0:
                    text.append(" · ", style=FG_FAINTEST)
                text.append(part, style=sty)
            text.append("\n")
        text.append("\n")

        # ── Actions (primary — what the user came here to do) ────────
        actions = _build_actions(
            runtime,
            is_connected=is_connected,
            is_any_remote=self._is_any_remote,
        )
        # While an action is in flight for this runtime, replace the action
        # list with a single disabled noop showing progress ("Starting...").
        if runtime_id == self._pending_action_runtime_id and self._pending_action_label:
            actions = [("noop", self._pending_action_label)]
        self._current_actions = actions

        for i, (action_id, label) in enumerate(actions):
            if i == self._action_cursor:
                text.append(" ❯ ", style=f"bold {ACCENT}")
            else:
                text.append("   ")
            if action_id == "noop":
                text.append(f"{label}\n", style=FG_FAINTEST)
            elif action_id in ("reset",):
                text.append(f"{label}\n", style=ERROR)
            elif action_id in ("connect", "start", "resume"):
                text.append(f"{label}\n", style=INFO)
            elif action_id in ("disconnect", "disconnect_other"):
                text.append(f"{label}\n", style=WARNING)
            else:
                text.append(f"{label}\n", style=FG)

        # "Back to list" always last
        back_idx = len(actions)
        if self._action_cursor == back_idx:
            text.append(" ❯ ", style=f"bold {ACCENT}")
        else:
            text.append("   ")
        text.append("Back to runtime list\n", style=FG_SUBTLE)
        text.append("\n")

        # ── Connected runtime info (from RuntimeInfo) ────────────────
        remote_info = self._remote_info if is_connected else None
        if remote_info:
            text.append(" Runtime Info\n", style=f"bold {FG_SUBTLE}")
            if remote_info.version:
                text.append("   Version   ", style=FG_MUTED)
                text.append(f"{remote_info.version}\n", style=FG_SUBTLE)
            if remote_info.host_type:
                text.append("   Host      ", style=FG_MUTED)
                text.append(f"{remote_info.host_type}\n", style=FG_SUBTLE)
            if remote_info.working_dir:
                text.append("   Dir       ", style=FG_MUTED)
                text.append(f"{remote_info.working_dir}\n", style=FG_FAINTEST)
            if remote_info.default_capability:
                text.append("   Default   ", style=FG_MUTED)
                text.append(f"{remote_info.default_capability}\n", style=FG_SUBTLE)
            if remote_info.capabilities:
                agent_count = sum(len(cap.agents) for cap in remote_info.capabilities if cap.agents)
                cap_count = len(remote_info.capabilities)
                text.append("   Loaded    ", style=FG_MUTED)
                parts = [f"{cap_count} capability" + ("" if cap_count == 1 else "s")]
                if agent_count:
                    parts.append(f"{agent_count} agent" + ("" if agent_count == 1 else "s"))
                text.append(" · ".join(parts) + "\n", style=TEAL)
            text.append("\n")

        # ── Details (reference info) ─────────────────────────────────
        text.append(" Details\n", style=f"bold {FG_SUBTLE}")
        created = _fmt_timestamp(runtime.get("created_at"))
        created_rel = _relative_time(runtime.get("created_at"))
        if created:
            text.append("   Created   ", style=FG_MUTED)
            text.append(created, style=FG_SUBTLE)
            if created_rel:
                text.append(f" · {created_rel}", style=FG_FAINTEST)
            text.append("\n")
        if provider:
            text.append("   Provider  ", style=FG_MUTED)
            text.append(f"{provider}\n", style=FG_SUBTLE)
        sandbox_url = instance.get("sandbox_url", "")
        if sandbox_url:
            text.append("   URL       ", style=FG_MUTED)
            text.append(f"{sandbox_url}\n", style=FG_FAINTEST)

        requested_runtime_limit = instance.get("requested_runtime_limit_seconds")
        if isinstance(requested_runtime_limit, int) and requested_runtime_limit > 0:
            requested_source = _runtime_limit_source_label(
                t.cast("str | None", instance.get("requested_runtime_limit_source_level")),
                current_level="l4_requested",
            )
            text.append("   Requested ", style=FG_MUTED)
            text.append(
                f"{_fmt_duration(requested_runtime_limit)} ({requested_source})\n",
                style=FG_SUBTLE,
            )

        configured_runtime_limit = instance.get("configured_runtime_limit_seconds")
        if isinstance(configured_runtime_limit, int) and configured_runtime_limit > 0:
            configured_source = _runtime_limit_source_label(
                t.cast("str | None", instance.get("configured_runtime_limit_source_level")),
                current_level="l4_requested",
            )
            text.append("   Limit     ", style=FG_MUTED)
            text.append(
                f"{_fmt_duration(configured_runtime_limit)} ({configured_source})\n",
                style=FG_SUBTLE,
            )

        # Credits
        billed = instance.get("billed_credits", 0)
        estimated = instance.get("estimated_total_credits", 0)
        if estimated:
            text.append("   Credits   ", style=FG_MUTED)
            text.append(f"{estimated} estimated\n", style=FG_SUBTLE)
        elif billed:
            text.append("   Credits   ", style=FG_MUTED)
            text.append(f"{billed} billed\n", style=FG_SUBTLE)

        # IDs (subtle, at the very bottom)
        text.append("   ID        ", style=FG_MUTED)
        text.append(f"{runtime_id}\n", style=FG_FAINTEST)
        if project_id:
            text.append("   Project   ", style=FG_MUTED)
            if project and project != project_id[:8]:
                text.append(f"{project}", style=FG_SUBTLE)
                text.append(f" · {project_id}\n", style=FG_FAINTEST)
            else:
                text.append(f"{project_id}\n", style=FG_FAINTEST)
        provider_id = instance.get("provider_sandbox_id", "")
        if provider_id:
            text.append("   Sandbox   ", style=FG_MUTED)
            text.append(f"{provider_id}\n", style=FG_FAINTEST)
        text.append("\n")

        self.query_one("#rt-content", Static).update(text)

    def _render_logs_view(self) -> None:
        runtime = self._selected_runtime
        if not runtime:
            return
        self.query_one("#rt-table", DataTable).add_class("-hidden")
        self.query_one("#rt-detail-scroll", VerticalScroll).remove_class("-hidden")

        runtime_id = str(runtime.get("id", "?"))
        project = self._project_name(runtime)
        text = Text()

        # Header
        text.append(" Server Logs", style=f"bold {FG_SUBTLE}")
        label = project if project and project != runtime_id[:8] else runtime_id[:8]
        text.append(f"  {label}\n\n", style=FG_MUTED)

        if self._logs_content is None:
            text.append("  Loading…\n", style=FG_MUTED)
        elif not self._logs_content.strip():
            text.append("  No logs available\n", style=FG_MUTED)
        else:
            for line in self._logs_content.splitlines():
                text.append(f"  {line}\n", style=FG_SUBTLE)

        self.query_one("#rt-content", Static).update(text)

    @on(DataTable.RowHighlighted, "#rt-table")
    def _on_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        self._cursor = event.cursor_row
        if self._view == "list":
            self._render_search()

    @on(DataTable.RowSelected, "#rt-table")
    def _on_row_selected(self, event: DataTable.RowSelected) -> None:
        if self._view != "list" or event.row_key is None:
            return
        row_key = str(event.row_key.value)
        for index, runtime in enumerate(self._visible_runtimes):
            if str(runtime.get("id", "")) == row_key:
                self._cursor = index
                break
        self._open_detail()

    # ── Data loading ─────────────────────────────────────────────────────

    @work(exclusive=True, group="runtimes")
    async def _load_data(self) -> None:
        try:
            data = await asyncio.to_thread(
                self._api.list_runtimes,
                self._org,
                self._workspace,
                state="idle,running,paused",
                limit=50,
            )
            runtimes = data.get("items", [])
            # Sort: running first, then paused, then idle
            runtimes.sort(key=lambda r: _STATE_ORDER.get(r.get("status", ""), 99))
            self._runtimes = runtimes
        except Exception as exc:
            logger.warning("Failed to load runtimes: {}", exc)
            self._runtimes = []

        # Resolve project names (once, then cached)
        if not self._project_names and self._runtimes:
            self._resolve_project_names()

        # If we're in detail or logs view, refresh the selected runtime data
        if self._view in ("detail", "logs") and self._selected_runtime:
            sel_id = str(self._selected_runtime.get("id", ""))
            for rt in self._runtimes:
                if str(rt.get("id", "")) == sel_id:
                    self._selected_runtime = rt
                    break
            # Auto-refresh logs while viewing them
            if self._view == "logs":
                self._do_fetch_logs()

        self._render_current_view()

    @work(exclusive=True, group="project-resolve")
    async def _resolve_project_names(self) -> None:
        """Fetch project list to map project_id -> name."""
        try:
            projects = await asyncio.to_thread(self._api.list_projects, self._org, self._workspace)
            for p in projects:
                pid = str(getattr(p, "id", ""))
                name = getattr(p, "name", "") or getattr(p, "key", "")
                if pid and name:
                    self._project_names[pid] = name
            # Re-render now that we have names
            self._render_current_view()
        except Exception as exc:
            logger.debug("Could not resolve project names: {}", exc)

    # ── Action execution ─────────────────────────────────────────────────

    def _execute_action(self, action_id: str) -> None:
        if action_id == "noop":
            return
        if self._is_app_busy() or self._is_action_pending():
            return
        runtime = self._selected_runtime
        if not runtime:
            return
        runtime_id = str(runtime.get("id", ""))

        # ``_show_action_notice`` is called *synchronously* here, before
        # the worker is scheduled, so that a second rapid call to
        # ``_execute_action`` will see ``_pending_action_runtime_id`` set
        # at ``_is_action_pending`` time and bail out. Previously the
        # notice was set inside each ``_do_*`` worker — but workers run
        # asynchronously, so two clicks could both pass ``_is_action_pending``
        # before either set the flag, racing into the same runtime.
        if action_id == "start":
            self._show_action_notice(runtime_id, "Starting")
            self._do_start(runtime_id)
        elif action_id == "connect":
            self._do_connect(runtime_id, runtime)
        elif action_id in ("disconnect", "disconnect_other"):
            self._do_disconnect()
        elif action_id == "pause":
            self._show_action_notice(runtime_id, "Pausing")
            self._do_pause(runtime_id)
        elif action_id == "resume":
            self._show_action_notice(runtime_id, "Resuming")
            self._do_resume(runtime_id)
        elif action_id == "reset":
            self._show_action_notice(runtime_id, "Resetting")
            self._do_reset(runtime_id)
        elif action_id == "keepalive":
            self._show_action_notice(runtime_id, "Extending")
            self._do_keepalive(runtime_id)
        elif action_id == "logs":
            self._view = "logs"
            self._logs_content = None
            self._render_current_view()
            self._do_fetch_logs()

    def _is_app_busy(self) -> bool:
        if hasattr(self.app, "busy") and self.app.busy:
            self.notify("Cannot act while a turn is active", title="Runtimes", severity="warning")
            return True
        return False

    def _is_action_pending(self) -> bool:
        """True if a runtime action is in flight — blocks new actions."""
        if self._pending_action_runtime_id is not None:
            self.notify("Action already in progress", title="Runtimes", severity="warning")
            return True
        return False

    def _show_action_notice(self, runtime_id: str, verb: str) -> None:
        """Mark a runtime action as in flight. Re-renders the detail view
        so the action list shows a disabled `{verb}...` entry."""
        self._pending_action_runtime_id = runtime_id
        self._pending_action_label = f"{verb}..."
        if self.is_mounted:
            self._render_current_view()

    def _requested_runtime_limit_kwargs(self) -> dict[str, int]:
        if self._requested_runtime_limit_seconds is None:
            return {}
        return {"requested_runtime_limit_seconds": self._requested_runtime_limit_seconds}

    def _clear_pending_action(self, runtime_id: str | None = None) -> None:
        """Clear the pending action marker. When ``runtime_id`` is provided
        and doesn't match the tracked id, this is a no-op — avoids one
        worker clearing another's pending state."""
        if (
            runtime_id is not None
            and self._pending_action_runtime_id is not None
            and self._pending_action_runtime_id != runtime_id
        ):
            return
        had_pending = self._pending_action_runtime_id is not None
        self._pending_action_runtime_id = None
        self._pending_action_label = None
        if had_pending and self.is_mounted:
            self._render_current_view()

    # ── Runtime actions ──────────────────────────────────────────────────

    @work(exclusive=True, group="runtime-action")
    async def _do_pause(self, runtime_id: str) -> None:
        self.notify(f"Pausing {runtime_id[:8]}…", title="Runtimes", severity="warning")
        try:
            await asyncio.to_thread(self._api.pause_runtime, self._org, self._workspace, runtime_id)
            self.notify(f"Paused {runtime_id[:8]}", title="Runtimes", severity="information")
        except Exception as exc:
            self.notify(f"Pause failed: {exc}", title="Runtimes", severity="error")
        finally:
            self._clear_pending_action(runtime_id)
        self._load_data()

    @work(exclusive=True, group="runtime-action")
    async def _do_resume(self, runtime_id: str) -> None:
        self.notify(f"Resuming {runtime_id[:8]}…", title="Runtimes", severity="information")
        try:
            await asyncio.to_thread(
                self._api.resume_runtime, self._org, self._workspace, runtime_id
            )
            self.notify(f"Resumed {runtime_id[:8]}", title="Runtimes", severity="information")
        except Exception as exc:
            self.notify(f"Resume failed: {exc}", title="Runtimes", severity="error")
        finally:
            self._clear_pending_action(runtime_id)
        self._load_data()

    @work(exclusive=True, group="runtime-action")
    async def _do_reset(self, runtime_id: str) -> None:
        self.notify(f"Resetting {runtime_id[:8]}…", title="Runtimes", severity="warning")
        try:
            if (
                self._connection_manager
                and self._connection_manager.connected_runtime_id == runtime_id
            ):
                await self._connection_manager.disconnect()

            await asyncio.to_thread(self._api.reset_runtime, self._org, self._workspace, runtime_id)

            self.notify(f"Reset {runtime_id[:8]}", title="Runtimes", severity="information")
        except Exception as exc:
            self.notify(f"Reset failed: {exc}", title="Runtimes", severity="error")
        finally:
            self._clear_pending_action(runtime_id)
        self._load_data()

    @work(exclusive=True, group="runtime-action")
    async def _do_keepalive(self, runtime_id: str) -> None:
        self.notify(f"Extending {runtime_id[:8]}…", title="Runtimes", severity="information")
        try:
            await asyncio.to_thread(
                self._api.keepalive_runtime,
                self._org,
                self._workspace,
                runtime_id,
                extend_seconds=300,
            )
            self.notify(
                f"Extended {runtime_id[:8]} by 5 min",
                title="Runtimes",
                severity="information",
            )
        except Exception as exc:
            self.notify(f"Keepalive failed: {exc}", title="Runtimes", severity="error")
        finally:
            self._clear_pending_action(runtime_id)
        self._load_data()

    async def _request_runtime_credentials(
        self,
        runtime_id: str,
    ) -> dict[str, str] | None:
        """Start if needed and return the runtime's credential."""
        result = await asyncio.to_thread(
            self._api.start_runtime,
            self._org,
            self._workspace,
            runtime_id,
            **self._requested_runtime_limit_kwargs(),
        )
        instance = result.get("instance") or {}
        sandbox_url = instance.get("sandbox_url")
        provider_sandbox_id = instance.get("provider_sandbox_id")
        sandbox_token = result.get("sandbox_token")
        if not isinstance(sandbox_url, str) or not sandbox_url:
            return None
        if not isinstance(provider_sandbox_id, str) or not provider_sandbox_id:
            return None
        if not isinstance(sandbox_token, str) or not sandbox_token:
            return None
        return {
            "sandbox_url": sandbox_url,
            "provider_sandbox_id": provider_sandbox_id,
            "token": sandbox_token,
        }

    @work(exclusive=True, group="runtime-action")
    async def _do_create(self, new_key: str) -> None:
        project_key = self._project_key
        if not project_key:
            self._clear_pending_action("__new__")
            return

        self.notify(
            f"Creating runtime '{new_key}'…",
            title="Runtimes",
            severity="information",
        )
        try:
            result = await asyncio.to_thread(
                self._api.create_runtime,
                self._org,
                self._workspace,
                project_key,
                key=new_key,
                **self._requested_runtime_limit_kwargs(),
            )
            runtime_id = str(result.get("id", ""))
            short_id = runtime_id[:8] if runtime_id else new_key
            if result.get("created"):
                self.notify(
                    f"Created runtime '{new_key}' ({short_id})",
                    title="Runtimes",
                    severity="information",
                )
            else:
                self.notify(
                    f"Runtime '{new_key}' already exists",
                    title="Runtimes",
                    severity="warning",
                )
        except Exception as exc:
            logger.warning(
                "create_runtime failed for project={} key={}: {}",
                project_key,
                new_key,
                exc,
            )
            self.notify(f"Create failed: {exc}", title="Runtimes", severity="error")
        finally:
            self._clear_pending_action("__new__")
        self._load_data()

    @work(exclusive=True, group="runtime-action")
    async def _do_start(self, runtime_id: str) -> None:
        self.notify(f"Starting {runtime_id[:8]}…", title="Runtimes", severity="information")
        try:
            credentials = await self._request_runtime_credentials(runtime_id)
            if credentials is None:
                self.notify(
                    "Runtime started but did not return connection credentials",
                    title="Runtimes",
                    severity="error",
                )
            else:
                self.notify(f"Started {runtime_id[:8]}", title="Runtimes", severity="information")
        except Exception as exc:
            logger.warning("start_runtime failed for {}: {}", runtime_id[:8], exc)
            self.notify(f"Start failed: {exc}", title="Runtimes", severity="error")
        finally:
            self._clear_pending_action(runtime_id)
        self._load_data()

    @work(exclusive=True, group="runtime-action")
    async def _do_connect(self, runtime_id: str, _runtime: dict[str, t.Any]) -> None:
        if self._connection_manager is None:
            self.notify("Connection manager not available", title="Runtimes", severity="error")
            return

        self.notify(f"Connecting to {runtime_id[:8]}…", title="Runtimes", severity="information")

        try:
            credentials = await self._request_runtime_credentials(runtime_id)
        except Exception as exc:
            logger.warning(
                "Credential request failed during connect for {}: {}",
                runtime_id[:8],
                exc,
            )
            credentials = None

        if credentials is None:
            self.notify(
                "Cannot obtain runtime connection credentials",
                title="Runtimes",
                severity="error",
            )
            return

        try:
            await self._connection_manager.connect(
                runtime_id=runtime_id,
                sandbox_url=credentials["sandbox_url"],
                token=credentials["token"],
            )
            self._stop_refresh_timer()
            self.dismiss()
        except ConnectionError as exc:
            logger.warning("Connect failed for {}: {}", runtime_id[:8], exc)
            self.notify(f"Connect failed: {exc}", title="Runtimes", severity="error")

    @work(exclusive=True, group="logs-fetch")
    async def _do_fetch_logs(self) -> None:
        runtime = self._selected_runtime
        if not runtime:
            return
        instance = runtime.get("instance") or {}
        provider_sandbox_id = instance.get("provider_sandbox_id", "")
        if not provider_sandbox_id:
            self._logs_content = ""
            self._render_current_view()
            return
        try:
            logs = await asyncio.to_thread(
                self._api.get_sandbox_logs,
                self._org,
                provider_sandbox_id,
            )
            self._logs_content = logs
        except Exception as exc:
            logger.warning("Failed to fetch logs: {}", exc)
            self._logs_content = f"Error fetching logs: {exc}"
        if self._view == "logs":
            self._render_current_view()

    @work(exclusive=True, group="runtime-action")
    async def _do_disconnect(self) -> None:
        if self._connection_manager is None:
            return
        self.notify("Disconnecting…", title="Runtimes", severity="information")
        await self._connection_manager.disconnect()
        self.notify("Disconnected — back to local", title="Runtimes", severity="information")
        self._load_data()
