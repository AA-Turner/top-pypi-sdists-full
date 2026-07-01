"""Sandbox Monitor screen -- live view of cloud sandboxes."""

from __future__ import annotations

import asyncio
import typing as t
from datetime import UTC, datetime

from textual import events, on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Static, Tree

from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.theme import (
    ERROR,
    FG,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    SUCCESS,
    WARNING,
)

if t.TYPE_CHECKING:
    from textual.app import ComposeResult
    from textual.timer import Timer

    from dreadnode.app.api.client import ApiClient

# -- Status dot helper -------------------------------------------------------

_STATUS_DOT: dict[str, str] = {
    "running": f"[{SUCCESS}]\u25cf[/]",
    "paused": f"[{WARNING}]\u25cf[/]",
    "killed": f"[{ERROR}]\u25cf[/]",
}


def _status_dot(state: str) -> str:
    return _STATUS_DOT.get(state, f"[{FG_SUBTLE}]\u25cf[/]")


# -- Formatting helpers ------------------------------------------------------


def _fmt_timestamp(ts: str | datetime | None) -> str:
    """Format an ISO timestamp for display."""
    if ts is None:
        return "-"
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            return ts[:19]
    else:
        dt = ts
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _fmt_runtime(seconds: int) -> str:
    """Format total runtime seconds into a human-readable string."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    secs = seconds % 60
    if minutes < 60:
        return f"{minutes}m{secs:02d}s"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h{mins:02d}m"


def _time_until(ts: str | datetime | None) -> str:
    """Return a human-readable time-until string for an expiry timestamp."""
    if ts is None:
        return "-"
    if isinstance(ts, str):
        try:
            dt = datetime.fromisoformat(ts)
        except ValueError:
            return ts[:19]
    else:
        dt = ts

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    now = datetime.now(tz=UTC)
    delta = dt - now
    total_secs = int(delta.total_seconds())
    if total_secs <= 0:
        return "expired"
    if total_secs < 60:
        return f"{total_secs}s"
    mins = total_secs // 60
    secs = total_secs % 60
    if mins < 60:
        return f"{mins}m{secs:02d}s"
    hours = mins // 60
    remaining_mins = mins % 60
    return f"{hours}h{remaining_mins:02d}m"


# ============================================================================
# SandboxScreen
# ============================================================================


class SandboxScreen(DreadnodeScreen):
    """Live-updating view of cloud sandboxes."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("r", "refresh_sandboxes", "Refresh", show=True),
        Binding("d", "delete_sandbox", "Delete", show=True),
    ]

    def __init__(
        self,
        api: ApiClient,
        org: str,
        workspace: str,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._api = api
        self._org = org
        self._workspace = workspace

        # Data
        self._sandboxes: list[dict[str, t.Any]] = []
        self._refresh_timer: Timer | None = None

    # ------------------------------------------------------------------ compose

    _SUBTITLE = f"\n[{FG_FAINTEST}] View and manage active sandbox instances[/]"

    def compose_content(self) -> ComposeResult:
        yield Static(
            f"[bold {FG}] Sandboxes[/]{self._SUBTITLE}",
            id="sandbox-title",
        )
        with Horizontal(id="sandbox-body"):
            with Vertical(id="sandbox-left"):
                yield DataTable(id="sandbox-table")
            with Vertical(id="sandbox-right"):
                yield Tree("Detail", id="sandbox-detail")

    # ------------------------------------------------------------------ mount

    def on_mount(self) -> None:
        super().on_mount()
        table = self.query_one("#sandbox-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("", "Sandbox ID", "Provider", "State", "Runtime", "Expires", "Project")

        self._load_sandboxes()
        self._start_refresh_timer()

    def on_unmount(self) -> None:
        self._stop_refresh_timer()

    def on_screen_suspend(self, _event: events.ScreenSuspend) -> None:
        self._stop_refresh_timer()

    def on_screen_resume(self, _event: events.ScreenResume) -> None:
        self._load_sandboxes()
        self._start_refresh_timer()

    def _start_refresh_timer(self) -> None:
        if self._refresh_timer is None:
            self._refresh_timer = self.set_interval(10.0, self._load_sandboxes)

    def _stop_refresh_timer(self) -> None:
        if self._refresh_timer is not None:
            self._refresh_timer.stop()
            self._refresh_timer = None

    # ------------------------------------------------------------------ actions

    def action_go_back(self) -> None:
        self._stop_refresh_timer()
        self.dismiss()

    def action_cursor_down(self) -> None:
        table = self.query_one("#sandbox-table", DataTable)
        table.action_cursor_down()

    def action_cursor_up(self) -> None:
        table = self.query_one("#sandbox-table", DataTable)
        table.action_cursor_up()

    def action_refresh_sandboxes(self) -> None:
        self._load_sandboxes()

    def action_delete_sandbox(self) -> None:
        sandbox_id = self._selected_sandbox_id()
        if sandbox_id:
            self._do_delete(sandbox_id)

    # ------------------------------------------------------------------ helpers

    def _selected_sandbox_id(self) -> str | None:
        """Return the provider sandbox ID of the currently highlighted row."""
        table = self.query_one("#sandbox-table", DataTable)
        if table.cursor_row is None:
            return None
        try:
            row_key = table.coordinate_to_cell_key((table.cursor_row, 0)).row_key
            return str(row_key.value) if row_key else None
        except Exception:
            return None

    def _flash_title(self, message: str = "", colour: str = FG_MUTED) -> None:
        title = self.query_one("#sandbox-title", Static)
        suffix = f"  [{colour}]{message}[/]" if message else ""
        title.update(f"[bold {FG}] Sandboxes[/]{suffix}{self._SUBTITLE}")

    # ------------------------------------------------------------------ data loading

    @work(exclusive=True, group="sandboxes")
    async def _load_sandboxes(self) -> None:
        """Fetch sandboxes from the platform API."""
        if not self.is_mounted:
            return
        table = self.query_one("#sandbox-table", DataTable)
        table.clear()

        self._flash_title("\u2026", FG_FAINTEST)

        try:
            data = await asyncio.to_thread(
                self._api.list_sandboxes,
                self._org,
                state="running,paused,killed",
                limit=50,
            )
            self._sandboxes = data.get("items", [])
        except Exception as exc:
            self._flash_title(f"Error: {exc}", ERROR)
            return

        if not self.is_mounted:
            return

        if not self._sandboxes:
            self._flash_title()
            self._clear_detail()
            return

        for sb in self._sandboxes:
            state = sb.get("state", "unknown")
            sandbox_id = sb.get("provider_sandbox_id", "?")
            provider = sb.get("provider", "?")
            runtime = _fmt_runtime(sb.get("total_runtime_seconds", 0))
            expires = _time_until(sb.get("expires_at"))
            proj = sb.get("project_key") or sb.get("project_name") or "-"

            table.add_row(
                _status_dot(state),
                sandbox_id,
                provider,
                state,
                runtime,
                expires,
                proj,
                key=sandbox_id,
            )

        total = len(self._sandboxes)
        self._flash_title(str(total))

        if self._sandboxes:
            self._show_sandbox_detail(self._sandboxes[0])

    # ------------------------------------------------------------------ events

    @on(DataTable.RowHighlighted, "#sandbox-table")
    def _on_sandbox_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.row_key is None:
            return
        sandbox_id = str(event.row_key.value)
        for sb in self._sandboxes:
            if sb.get("provider_sandbox_id") == sandbox_id:
                self._show_sandbox_detail(sb)
                break

    # ------------------------------------------------------------------ detail panel

    def _clear_detail(self) -> None:
        detail = self.query_one("#sandbox-detail", Tree)
        detail.clear()
        detail.root.set_label("[dim]No sandbox selected[/]")

    def _show_sandbox_detail(self, sb: dict[str, t.Any]) -> None:
        """Populate the right-hand detail tree with sandbox info."""
        detail = self.query_one("#sandbox-detail", Tree)
        detail.clear()

        sandbox_id = sb.get("provider_sandbox_id", "unknown")
        detail.root.set_label(f"[bold]Sandbox: {sandbox_id}[/]")

        state = sb.get("state", "unknown")
        state_colour = {
            "running": SUCCESS,
            "paused": WARNING,
            "killed": ERROR,
        }.get(state, FG_SUBTLE)

        # Basic info
        info_node = detail.root.add("Info", expand=True)
        info_node.add_leaf(f"ID: [{FG_SUBTLE}]{sb.get('id', 'n/a')}[/]")
        info_node.add_leaf(f"Provider ID: [{FG_SUBTLE}]{sandbox_id}[/]")
        info_node.add_leaf(f"Provider: [{FG_SUBTLE}]{sb.get('provider', 'n/a')}[/]")
        info_node.add_leaf(f"State: [{state_colour}]{state}[/]")
        info_node.add_leaf(f"Build Ref: [{FG_SUBTLE}]{sb.get('build_ref', 'n/a')}[/]")

        # Timing
        timing_node = detail.root.add("Timing", expand=True)
        timing_node.add_leaf(f"Created: [{FG_SUBTLE}]{_fmt_timestamp(sb.get('created_at'))}[/]")
        timing_node.add_leaf(
            f"Last Started: [{FG_SUBTLE}]{_fmt_timestamp(sb.get('last_started_at'))}[/]"
        )
        timing_node.add_leaf(f"Expires: [{FG_SUBTLE}]{_fmt_timestamp(sb.get('expires_at'))}[/]")
        timing_node.add_leaf(
            f"Runtime: [{FG}]{_fmt_runtime(sb.get('total_runtime_seconds', 0))}[/]"
        )

        if sb.get("pause_reason"):
            timing_node.add_leaf(f"Pause Reason: [{WARNING}]{sb['pause_reason']}[/]")

        # Project
        proj_node = detail.root.add("Project", expand=True)
        proj_node.add_leaf(
            f"Project: [{FG_SUBTLE}]{sb.get('project_key') or sb.get('project_name') or 'n/a'}[/]"
        )
        proj_node.add_leaf(f"Workspace: [{FG_SUBTLE}]{sb.get('workspace_key', 'n/a')}[/]")

        workload = sb.get("workload_context")
        if isinstance(workload, dict):
            workload_node = detail.root.add("Workload", expand=True)
            workload_node.add_leaf(f"Type: [{FG_SUBTLE}]{workload.get('kind', 'n/a')}[/]")
            evaluation_label = (
                workload.get("evaluation_name") or workload.get("evaluation_id") or "n/a"
            )
            workload_node.add_leaf(f"Evaluation: [{FG_SUBTLE}]{evaluation_label}[/]")
            item_position = workload.get("evaluation_item_position")
            item_label = item_position + 1 if isinstance(item_position, int) else "n/a"
            workload_node.add_leaf(f"Item: [{FG_SUBTLE}]{item_label}[/]")
            workload_node.add_leaf(f"Role: [{FG_SUBTLE}]{workload.get('sandbox_role', 'n/a')}[/]")
            workload_node.add_leaf(f"Task: [{FG_SUBTLE}]{workload.get('task_name', 'n/a')}[/]")
            if workload.get("model"):
                workload_node.add_leaf(f"Model: [{FG_SUBTLE}]{workload['model']}[/]")
            if workload.get("agent_type"):
                workload_node.add_leaf(f"Agent: [{FG_SUBTLE}]{workload['agent_type']}[/]")

        # Credits
        credits_node = detail.root.add("Credits", expand=True)
        credits_node.add_leaf(f"Billed: [{FG}]{sb.get('billed_credits', 0)}[/]")
        credits_node.add_leaf(f"Running: [{FG}]{sb.get('running_credits', 0)}[/]")
        credits_node.add_leaf(f"Est. Total: [{FG}]{sb.get('estimated_total_credits', 0)}[/]")

        detail.root.expand()

    # ------------------------------------------------------------------ sandbox actions

    @work(exclusive=True, group="sandbox-action")
    async def _do_delete(self, sandbox_id: str) -> None:
        self.notify(f"Deleting {sandbox_id}...", title="Sandboxes", severity="warning")
        try:
            await asyncio.to_thread(self._api.delete_sandbox, self._org, sandbox_id)
            self.notify(f"Deleted {sandbox_id}", title="Sandboxes", severity="information")
        except Exception as exc:
            self.notify(f"Delete failed: {exc}", title="Sandboxes", severity="error")
        self._load_sandboxes()
