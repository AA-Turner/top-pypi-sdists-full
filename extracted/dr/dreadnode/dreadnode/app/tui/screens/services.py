"""Services screen — inspect and manage background services (MCP servers, workers)."""

import asyncio
import contextlib
import textwrap
import typing as t

from rich.text import Text
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.widgets import Static

from dreadnode.app.tui.capabilities_manager import ComponentStateChanged
from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.theme import (
    ACCENT,
    BRAND,
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
    from textual.events import Key, ScreenResume, ScreenSuspend
    from textual.timer import Timer

    from dreadnode.app.client.managed_client import ManagedRuntimeClient


# Poll interval for the detail view so operators see Recent output / Recent
# stderr tail in near-real-time without having to leave and re-enter the
# page after a restart. Silent refresh — no "Loading..." flicker.
_DETAIL_REFRESH_SECONDS = 2.0


# Maximum MCP tools to list inline in the detail view before collapsing the
# rest behind a "View tools" affordance. Chosen to fit a terminal pane without
# scrolling; callers use the "View tools" action to see the full list.
_MAX_INLINE_TOOLS = 8

# Truncation length for a tool description shown inline in the detail view.
# Descriptions longer than this are elided with an ellipsis.
_INLINE_TOOL_DESC_MAX_CHARS = 60

# Marker used by SubprocessWorkerRunner to separate the exit message from the
# captured output tail. Keep in sync with worker_runner.OUTPUT_ERROR_MARKER.
_WORKER_OUTPUT_MARKER = "\n\nWorker output:\n"

# Marker used by MCPClient._set_error_status to append a captured stderr tail.
_MCP_STDERR_MARKER = "\n\nServer stderr:\n"

# Maximum recent-output lines rendered inline in the detail pane. The in-memory
# buffer on the runner / client keeps more; we only need the tail for
# progressive-disclosure troubleshooting in the TUI.
_MAX_RECENT_LINES = 30

# Column width that section field labels are padded to so values line up.
# Shared by the MCP and worker detail views; sized to the longest label
# rendered in either ("Capability" / "on_shutdown") plus a column gap.
_FIELD_LABEL_WIDTH = 12

# Column the value text starts at in a field row: 4-space section indent plus
# the padded label. Wrapped continuation lines hang-indent to this column so a
# long value keeps the two-column structure instead of collapsing to col 0.
_FIELD_VALUE_COL = 4 + _FIELD_LABEL_WIDTH

# Fallback content width (cells) used when the screen size isn't known yet
# (e.g. the very first render before layout, or in unit tests).
_DEFAULT_CONTENT_WIDTH = 100


def _wrap_value(value: str, width: int, indent: int) -> list[str]:
    """Wrap *value* to *width* cells with a hanging indent of *indent* cells.

    Continuation lines are meant to align under the value column rather than
    collapsing to the left margin, so a long value (args, paths, URLs, error
    text) keeps its section's structure when it wraps. Returns the wrapped
    segments (without the indent — callers prepend it); always at least one
    (possibly empty) segment.
    """
    avail = max(8, width - indent)
    lines = textwrap.wrap(
        str(value),
        avail,
        break_long_words=True,
        break_on_hyphens=False,
    )
    return lines or [""]


def _build_items(
    servers: list[dict[str, t.Any]],
    workers: list[dict[str, t.Any]],
) -> list[dict[str, t.Any]]:
    """Merge MCP servers and workers into a unified item list, grouped by capability."""
    by_cap: dict[str, list[dict[str, t.Any]]] = {}
    for s in servers:
        entry = dict(s, kind="mcp_server")
        by_cap.setdefault(entry.get("capability", ""), []).append(entry)
    for w in workers:
        entry = dict(w, kind="worker")
        by_cap.setdefault(entry.get("capability", ""), []).append(entry)
    items: list[dict[str, t.Any]] = []
    for _cap in sorted(by_cap):
        items.extend(by_cap[_cap])
    return items


class ServicesScreen(DreadnodeScreen):
    """Full-screen services manager — list, inspect, reconnect/restart."""

    BINDINGS: t.ClassVar[list[Binding]] = [Binding("escape", "dismiss", "Back", show=False)]

    def __init__(
        self,
        runtime_client: "ManagedRuntimeClient",
        servers: list[dict[str, t.Any]],
        workers: list[dict[str, t.Any]] | None = None,
        *,
        collect_servers: t.Callable[[], list[dict[str, t.Any]]] | None = None,
        collect_workers: t.Callable[[], list[dict[str, t.Any]]] | None = None,
    ) -> None:
        super().__init__()
        self._client = runtime_client
        self._servers = servers
        self._workers = workers or []
        self._items = _build_items(servers, workers or [])
        # Collectors let the screen pull a fresh snapshot from the
        # capabilities manager when a ``component.state_changed`` event
        # arrives. Optional so existing callers keep working — without
        # them the screen still renders, just without bus-driven refresh.
        self._collect_servers = collect_servers
        self._collect_workers = collect_workers
        self._view: str = "list"  # list | detail | tool_list
        self._cursor: int = 0
        self._action_cursor: int = 0
        self._selected_item: dict[str, t.Any] | None = None
        self._item_detail: dict[str, t.Any] | None = None
        self._tool_search: str = ""
        self._loading: bool = False
        self._acting: bool = False  # reconnecting or restarting
        self._refresh_timer: Timer | None = None

    def compose_content(self) -> "ComposeResult":
        yield Static(id="services-header")
        yield Static(id="services-search")
        with VerticalScroll(id="services-scroll"):
            yield Static(id="services-content")
        # Pinned below the scroll region so a long Recent output / Recent
        # stderr block or a long tools/handlers list never pushes the
        # action menu off the bottom of the screen. Non-detail views
        # clear this widget.
        yield Static(id="services-actions")
        yield Static(id="services-hint")

    def on_mount(self) -> None:
        super().on_mount()
        self._render_current_view()

    def on_unmount(self) -> None:
        # Key handlers stop the detail-refresh timer on normal navigation, but
        # an app-level pop (e.g. F5 opening the console) bypasses them — stop
        # it here so the interval never fires against a dead widget tree.
        self._stop_detail_refresh()

    def on_screen_suspend(self, _event: "ScreenSuspend") -> None:
        self._stop_detail_refresh()

    def on_screen_resume(self, _event: "ScreenResume") -> None:
        if self._view == "detail":
            self._start_detail_refresh()

    def on_component_state_changed(self, message: ComponentStateChanged) -> None:
        """Refresh the list (and the cached selection) from the manager.

        Fired by the app-level subscriber after a ``component.state_changed``
        envelope has already patched ``runtime_info`` in place. We re-pull
        the collectors so the list snapshot tracks the live state, and if
        the affected component is the one currently selected we mirror the
        fields onto the selected-item dict so the detail pane's next render
        picks up the new status without waiting for its own poll.
        """
        payload = message.payload
        # 1. Rebuild the list items from the freshly-patched snapshot so
        #    the list view (if visible) reflects the new status.
        if self._collect_servers is not None and self._collect_workers is not None:
            self._servers = self._collect_servers()
            self._workers = self._collect_workers()
            self._items = _build_items(self._servers, self._workers)
            # Keep the cursor in range after a rebuild (e.g. if a
            # capability was unloaded since the screen opened).
            if self._items:
                self._cursor = min(self._cursor, len(self._items) - 1)
            else:
                self._cursor = 0

        # 2. If the user is currently looking at this component's detail,
        #    mirror the payload onto the selection so the list-status maps
        #    over (error/ok/stopped) without racing the 2s detail poll.
        selected = self._selected_item
        if (
            selected is not None
            and selected.get("capability") == payload.get("capability")
            and selected.get("name") == payload.get("name")
        ):
            if "status" in payload:
                selected["status"] = payload["status"]
            selected["error"] = payload.get("error")
            if payload.get("detail") is not None:
                selected["detail"] = payload["detail"]

        if self.is_mounted:
            self._render_current_view()

    def on_key(self, event: "Key") -> None:
        key = event.key
        if key.startswith("ctrl+") or (key.startswith("f") and key[1:].isdigit()):
            return

        if self._view == "tool_list":
            self._handle_tool_list_key(key, event)
            if key != "escape":
                return
        elif self._view == "detail":
            self._handle_detail_key(key)
        else:
            self._handle_list_key(key)

        event.prevent_default()
        event.stop()

    # ── Helpers ──

    def _selected_kind(self) -> str:
        return (self._item_detail or self._selected_item or {}).get("kind", "mcp_server")

    def _is_mcp(self) -> bool:
        return self._selected_kind() == "mcp_server"

    # ── List view ──

    def _handle_list_key(self, key: str) -> None:
        if key == "up":
            self._cursor = max(0, self._cursor - 1)
        elif key == "down":
            self._cursor = min(len(self._items) - 1, self._cursor + 1)
        elif key == "enter" and self._items:
            self._selected_item = self._items[self._cursor]
            self._view = "detail"
            self._action_cursor = 0
            self._item_detail = None
            self._loading = True
            self._render_current_view()
            self._fetch_detail()
            self._start_detail_refresh()
            return
        elif key == "escape":
            self._stop_detail_refresh()
            self.dismiss()
            return
        self._render_current_view()

    def _fetch_detail(self) -> None:
        item = self._selected_item
        if item is None:
            return
        cap = item.get("capability", "")
        name = item.get("name", "")
        kind = item.get("kind", "mcp_server")
        self.run_worker(self._do_fetch_detail(cap, name, kind), exclusive=True)

    async def _do_fetch_detail(self, capability: str, name: str, kind: str) -> None:
        try:
            if kind == "worker":
                self._item_detail = await self._client.fetch_worker_detail(capability, name)
                self._item_detail["kind"] = "worker"
            else:
                self._item_detail = await self._client.fetch_mcp_detail(capability, name)
                self._item_detail["kind"] = "mcp_server"
            # Detail is the freshest source — sync the list entry so it doesn't
            # drift (the list snapshot was captured at screen-open).
            self._sync_list_from_detail(self._item_detail)
        except Exception as exc:
            self._item_detail = None
            self.notify(f"Failed to load detail: {exc}", title="Services", severity="error")
            # Reflect the fetch failure on the list entry so navigating back
            # doesn't show a stale "ok" status for something we know is broken.
            self._sync_list_entry(capability, name, "error", str(exc))
        finally:
            self._loading = False
            self._render_current_view()

    # ── Auto-refresh ──

    def _start_detail_refresh(self) -> None:
        """Kick off periodic polling of the detail endpoint.

        Idempotent — calling while already running is a no-op. Runs only
        while the detail view is active; the timer is torn down on any
        transition away so we never poll a stale selection.
        """
        if self._refresh_timer is not None:
            return
        self._refresh_timer = self.set_interval(
            _DETAIL_REFRESH_SECONDS, self._silent_refresh_detail
        )

    def _stop_detail_refresh(self) -> None:
        if self._refresh_timer is not None:
            self._refresh_timer.stop()
            self._refresh_timer = None

    def _silent_refresh_detail(self) -> None:
        """Timer callback: fetch fresh detail without the Loading flicker."""
        if self._view != "detail" or self._selected_item is None:
            return
        if self._loading or self._acting:
            return  # don't race a pending fetch/action
        self.run_worker(self._do_silent_refresh_async(), exclusive=False)

    async def _do_silent_refresh_async(self) -> None:
        item = self._selected_item
        if item is None:
            return
        capability = item.get("capability", "")
        name = item.get("name", "")
        kind = item.get("kind", "mcp_server")
        try:
            if kind == "worker":
                fresh = await self._client.fetch_worker_detail(capability, name)
                fresh["kind"] = "worker"
            else:
                fresh = await self._client.fetch_mcp_detail(capability, name)
                fresh["kind"] = "mcp_server"
        except Exception:
            # Silent refresh swallows transient failures — user-initiated
            # fetches still surface errors via the normal path.
            return
        # Selection or view may have changed while the fetch was in flight.
        if self._view != "detail" or self._acting:
            return
        current = self._selected_item or {}
        if current.get("capability") != capability or current.get("name") != name:
            return
        if fresh == self._item_detail:
            return  # Nothing changed since the last poll — skip the re-render.
        self._item_detail = fresh
        # Auto-refresh found drift — propagate to the list entry too so
        # leaving the detail view back to the list shows the current state.
        self._sync_list_from_detail(fresh)
        self._render_current_view()

    def _render_list(self) -> None:
        header = self.query_one("#services-header", Static)
        content = self.query_one("#services-content", Static)
        actions_pane = self.query_one("#services-actions", Static)
        hint = self.query_one("#services-hint", Static)
        actions_pane.update(Text())  # list view has no per-item actions pane

        count = len(self._items)
        text = Text()
        text.append(" Services", style=f"bold {FG}")
        if count:
            text.append(f"  {count}", style=FG_MUTED)
        text.append("\n")
        text.append(" MCP servers and workers running in the background", style=FG_FAINTEST)
        header.update(text)

        if not self._items:
            content.update(Text("No background services configured", style=f"italic {FG_MUTED}"))
            hint.update(Text("Esc close", style=FG_FAINTEST))
            return

        output = Text()
        current_cap = None
        for i, item in enumerate(self._items):
            cap = item.get("capability", "")
            if cap != current_cap:
                if current_cap is not None:
                    output.append("\n")
                output.append(f"  {cap}\n", style=FG_MUTED)
                current_cap = cap

            is_selected = i == self._cursor
            prefix = "> " if is_selected else "  "
            kind = item.get("kind", "mcp_server")

            status = item.get("status", "?")
            if status == "ok":
                if kind == "worker":
                    icon, icon_style, label = "✓", SUCCESS, "running"
                else:
                    icon, icon_style, label = "✓", SUCCESS, "connected"
            elif status == "connecting":
                icon, icon_style, label = "…", BRAND, "connecting"
            elif status == "needs_auth":
                icon, icon_style, label = "⚠", WARNING, "needs authentication"
            elif status == "stopped":
                icon, icon_style, label = "◯", FG_MUTED, "stopped"
            elif status == "gated_off":
                gated_detail = item.get("detail", "")
                gated_label = gated_detail.lower() if gated_detail else "gated off"
                icon, icon_style, label = "◯", FG_MUTED, gated_label
            elif status == "enabled_failed":
                icon, icon_style, label = "✗", ERROR, item.get("error", "enabled but failed")
            elif status == "degraded":
                icon, icon_style, label = "⚠", WARNING, item.get("detail", "degraded")
            elif status == "error":
                icon, icon_style, label = "✗", ERROR, item.get("error") or "error"
            else:
                icon, icon_style, label = "?", WARNING, status

            kind_label = "worker" if kind == "worker" else "mcp server"
            transport = item.get("transport", "")
            tool_count = item.get("tool_count", 0)

            output.append(prefix, style=ACCENT if is_selected else "")
            output.append(item.get("name", "?"), style=f"bold {FG}" if is_selected else FG)
            output.append(" · ", style=FG_FAINTEST)
            output.append(f"{icon} ", style=icon_style)
            output.append(label, style=FG_MUTED)
            if transport:
                output.append(f" · {transport}", style=FG_FAINTEST)
            if tool_count:
                output.append(f" · {tool_count} tools", style=FG_FAINTEST)
            output.append(f"   {kind_label}", style=FG_FAINTEST)
            output.append("\n")

        content.update(output)
        hint.update(Text("↑↓ navigate · Enter select · Esc close", style=FG_FAINTEST))

    # ── Detail view ──

    def _handle_detail_key(self, key: str) -> None:
        actions = self._get_actions()
        # A background silent refresh can shrink the actions list while the
        # cursor sits on a now-gone trailing entry; clamp before any indexing.
        self._action_cursor = min(self._action_cursor, max(0, len(actions) - 1))
        if key == "up":
            self._action_cursor = max(0, self._action_cursor - 1)
        elif key == "down":
            self._action_cursor = min(len(actions) - 1, self._action_cursor + 1)
        elif key == "r":
            # Manual refresh — the detail pane already polls on an
            # interval, but operators often want an immediate pull right
            # after a restart or reconnect. Enter still triggers the
            # currently-highlighted menu action (including restart).
            self._silent_refresh_detail()
            return
        elif key == "enter" and actions:
            action_id = actions[self._action_cursor][0]
            if action_id == "view_tools":
                self._stop_detail_refresh()
                self._view = "tool_list"
                self._render_current_view()
                return
            if action_id == "view_capability":
                self._go_to_capability()
                return
            if action_id in ("reconnect", "restart", "reauthenticate"):
                self._do_action(action_id=action_id)
                return
        elif key == "escape":
            self._stop_detail_refresh()
            self._view = "list"
            self._item_detail = None
        self._render_current_view()

    def _action_verb(self, past: bool = False) -> str:
        """Return the appropriate verb for the primary action.

        MCP servers in ``needs_auth`` use ``Authenticate`` rather than
        ``Reconnect`` — same handler under the hood (the existing
        reconnect path already spawns the bridge / drives auth), but
        the label sets user expectation that a browser may open.
        """
        if self._is_mcp():
            item = self._item_detail or self._selected_item or {}
            if item.get("status") == "needs_auth":
                return "Authenticated" if past else "Authenticate"
            transport = item.get("transport", "")
            if transport == "stdio":
                return "Restarted" if past else "Restart"
            return "Reconnected" if past else "Reconnect"
        return "Restarted" if past else "Restart"

    def _get_actions(self) -> list[tuple[str, str]]:
        actions: list[tuple[str, str]] = []
        item = self._item_detail or self._selected_item or {}
        status = item.get("status") or item.get("state")
        is_gated_off = status == "gated_off"
        is_connecting = status == "connecting"
        if self._is_mcp():
            detail = self._item_detail
            if detail and detail.get("tool_count", 0) > 0:
                actions.append(("view_tools", "View tools"))
            # CAP-FLAG-014: reconnect would fail with 409 anyway.
            # Skip while a background connect is in flight — the user
            # should wait rather than churn the lifecycle mid-attempt.
            if not is_gated_off and not is_connecting:
                actions.append(("reconnect", self._action_verb()))
            # Re-authenticate clears stored OAuth tokens for this server
            # only and triggers a fresh OAuth flow. OAuth is reactive-by-
            # default (CAP-MCP-011), so any streamable-http server is
            # OAuth-capable — no declared auth: block required. Stdio bridges
            # manage their own credentials and the API 404s for them.
            # Skip in needs_auth: there are no stored credentials to clear and
            # the primary action is already "Authenticate" (the same fresh
            # OAuth flow), so a second "Re-authenticate" entry is redundant.
            if (
                not is_gated_off
                and not is_connecting
                and status != "needs_auth"
                and (detail or {}).get("transport") == "streamable-http"
            ):
                actions.append(("reauthenticate", "Re-authenticate"))
        elif not is_gated_off:
            # CAP-WLIF-006: restart is rejected for gated-off workers
            actions.append(("restart", self._action_verb()))

        # Jump to the capability that installed/runs this service. A nav
        # affordance rather than a lifecycle action, so it's offered for any
        # status (including gated-off / failed) as long as we know the owner.
        # The owning capability rides on the list selection even when the
        # detail fetch is partial, so fall back to it.
        if item.get("capability") or (self._selected_item or {}).get("capability"):
            actions.append(("view_capability", "View capability"))
        return actions

    def _do_action(self, *, action_id: str = "reconnect") -> None:
        item = self._selected_item
        if item is None:
            return
        cap = item.get("capability", "")
        name = item.get("name", "")
        if self._is_mcp():
            if action_id == "reauthenticate":
                self.run_worker(self._do_reauthenticate_async(cap, name), exclusive=True)
            else:
                self.run_worker(self._do_reconnect_async(cap, name), exclusive=True)
        else:
            self.run_worker(self._do_restart_worker_async(cap, name), exclusive=True)

    def _go_to_capability(self) -> None:
        """Dismiss this screen and open the owning capability's detail view.

        The router dismisses the pushed services screen and pushes the
        capabilities manager focused on this service's ``capability`` (the
        same identifier the capabilities screen keys installed items on).
        """
        # Mirror the fallback in _get_actions: a partial detail fetch may omit
        # ``capability`` while the list selection still carries it. Resolve
        # field-by-field rather than dict-by-dict so a truthy-but-incomplete
        # ``_item_detail`` doesn't short-circuit past the selection.
        capability = (self._item_detail or {}).get("capability") or (self._selected_item or {}).get(
            "capability"
        )
        if not capability:
            self.notify(
                "No capability associated with this service", title="Services", severity="warning"
            )
            return
        self._stop_detail_refresh()
        from dreadnode.app.tui.app import DreadnodeTextualApp

        app = self.app
        if isinstance(app, DreadnodeTextualApp):
            app.open_capability_detail(capability)
        else:
            self.dismiss()

    async def _do_reauthenticate_async(self, capability: str, server_name: str) -> None:
        """Clear stored OAuth tokens for THIS server only, then reconnect.

        The runtime drops the file-store entry for this server's URL and
        triggers a fresh OAuth round-trip (browser opens). Other
        authenticated capabilities keep their tokens (CAP-MCP-011).
        """
        self._acting = True
        self._render_current_view()
        self.notify(
            "Re-authenticating — browser will open…",
            title="Services",
            severity="information",
            timeout=10,
        )
        await asyncio.sleep(0)
        try:
            self._item_detail = await self._client.reauthenticate_mcp_server(
                capability, server_name
            )
            self._item_detail["kind"] = "mcp_server"
            status = self._item_detail.get("status", "")
            if status in ("connected", "ok"):
                self.notify("Re-authenticated", title="Services", severity="information")
                self._sync_list_entry(capability, server_name, "ok", None)
            else:
                error = self._item_detail.get("error", "unknown error")
                short = error.split("\n", 1)[0] if error else "unknown error"
                self.notify(
                    f"Re-authenticate failed: {short}",
                    title="Services",
                    severity="error",
                )
                # Preserve the real status (e.g. ``needs_auth`` when the user
                # cancelled/timed out the browser flow) rather than forcing the
                # list entry to a hard ``error``.
                self._sync_list_from_detail(self._item_detail)
        except Exception as exc:
            self.notify(
                f"Re-authenticate failed: {exc}",
                title="Services",
                severity="error",
            )
        finally:
            self._acting = False
        self._render_current_view()

    async def _do_reconnect_async(self, capability: str, server_name: str) -> None:
        verb = self._action_verb()
        self._acting = True
        self._render_current_view()
        self.notify(f"{verb}ing...", title="Services", severity="information", timeout=10)
        await asyncio.sleep(0)
        try:
            self._item_detail = await self._client.reconnect_mcp_server(capability, server_name)
            self._item_detail["kind"] = "mcp_server"
            status = self._item_detail.get("status", "")
            verb = self._action_verb(past=True)
            if status in ("connected", "ok"):
                self.notify(verb, title="Services", severity="information")
                self._sync_list_entry(capability, server_name, "ok", None)
            else:
                error = self._item_detail.get("error", "unknown error")
                short = error.split("\n", 1)[0] if error else "unknown error"
                self.notify(
                    f"{self._action_verb()} failed: {short}",
                    title="Services",
                    severity="error",
                )
                # Preserve the real status (e.g. ``needs_auth`` when the user
                # cancelled/timed out the browser flow) rather than forcing the
                # list entry to a hard ``error``.
                self._sync_list_from_detail(self._item_detail)
        except Exception as exc:
            self.notify(f"{self._action_verb()} failed: {exc}", title="Services", severity="error")
        finally:
            self._acting = False
        self._render_current_view()

    async def _do_restart_worker_async(self, capability: str, worker_name: str) -> None:
        self._acting = True
        self._render_current_view()
        self.notify("Restarting...", title="Services", severity="information", timeout=10)
        await asyncio.sleep(0)
        try:
            self._item_detail = await self._client.restart_worker(capability, worker_name)
            self._item_detail["kind"] = "worker"
            state = self._item_detail.get("state", "")
            restarted = bool(self._item_detail.get("restarted", True))
            if state in ("running", "ok"):
                message = "Restarted" if restarted else "Already running"
                self.notify(message, title="Services", severity="information")
                self._sync_list_entry(capability, worker_name, "ok", None)
            else:
                error = self._item_detail.get("error", "unknown error")
                short = error.split("\n", 1)[0] if error else "unknown error"
                self.notify(f"Restart failed: {short}", title="Services", severity="error")
                self._sync_list_entry(capability, worker_name, "error", error)
        except Exception as exc:
            self.notify(f"Restart failed: {exc}", title="Services", severity="error")
        finally:
            self._acting = False
        self._render_current_view()

    def _sync_list_entry(self, capability: str, name: str, status: str, error: str | None) -> None:
        """Update the list-level entry so navigating back shows current state."""
        for item in self._items:
            if item.get("capability") == capability and item.get("name") == name:
                item["status"] = status
                item["error"] = error
                break

    @staticmethod
    def _detail_to_list_status(detail: dict[str, t.Any]) -> tuple[str | None, str | None]:
        """Map a fresh detail dict to (list-status, error) for list-entry sync.

        Detail and list use *different* status vocabularies. Workers carry
        ``state`` (``WorkerState`` enum: ``running``/``error``/...); MCP
        servers carry ``status`` (``MCPStatus`` enum: ``connected``/
        ``failed``/...). The list renderer only knows the lifecycle-manager
        vocabulary (``ok``/``error``/``stopped``/``gated_off``/
        ``enabled_failed``/``degraded``) and falls through to ``?`` for
        anything else.

        Returns ``(None, _)`` when the detail status doesn't have a known
        list equivalent — the caller must NOT overwrite the existing list
        entry in that case (otherwise a healthy ``ok`` MCP becomes ``?``
        when the user steps in/out of its detail).
        """
        error = detail.get("error")
        kind = detail.get("kind")
        if kind == "worker":
            # Mirror WorkerLifecycleManager._update_health (worker_manager.py).
            mapping = {
                "running": "ok",
                "error": "error",
                "stopped": "stopped",
                "gated_off": "gated_off",
            }
            return mapping.get(detail.get("state", "")), error
        # get_server_detail returns one of two vocabularies depending on
        # whether the live client is attached:
        #   - client present → MCPStatus enum ("connected"/"failed"/...)
        #   - client absent (background/failed/needs_auth) → component_health
        #     vocab ("ok"/"error"/"enabled_failed"/"gated_off"/...)
        # Map both onto the list-renderer vocabulary. ``disconnected`` is the
        # lifecycle-not-yet-attached state and isn't a clean STOPPED, so we
        # don't sync it — leave the existing entry alone rather than churning
        # it to a ``?``.
        mapping = {
            # MCPStatus enum (client attached)
            "connected": "ok",
            "failed": "error",
            # component_health vocab (client absent)
            "ok": "ok",
            "error": "error",
            "enabled_failed": "enabled_failed",
            "gated_off": "gated_off",
            # shared
            "needs_auth": "needs_auth",
            "connecting": "connecting",
        }
        return mapping.get(detail.get("status", "")), error

    def _sync_list_from_detail(self, detail: dict[str, t.Any]) -> None:
        """Push the freshly-fetched detail's status onto its list entry.

        Without this, the list view (a snapshot from screen-open) drifts from
        the detail view (re-fetched on open + auto-refresh) — e.g. a worker
        that errors after the screen opened still shows ``running`` in the
        list while the detail correctly shows ``failed``.
        """
        capability = detail.get("capability", "")
        name = detail.get("name", "")
        if not capability or not name:
            return
        status, error = self._detail_to_list_status(detail)
        if status is None:
            return  # Unknown detail status — preserve the existing list entry.
        self._sync_list_entry(capability, name, status, error)

    def _render_detail(self) -> None:
        header = self.query_one("#services-header", Static)
        content = self.query_one("#services-content", Static)
        actions_pane = self.query_one("#services-actions", Static)
        hint = self.query_one("#services-hint", Static)

        item = self._selected_item or {}
        detail = self._item_detail
        is_mcp = self._is_mcp()

        name = item.get("name", "?")
        text = Text()
        text.append(f" {name}", style=f"bold {FG}")
        text.append("\n")
        text.append(" Worker" if not is_mcp else " MCP Server", style=FG_FAINTEST)
        header.update(text)

        output = Text()

        if self._loading:
            output.append("\n  Loading...\n", style=FG_MUTED)
            content.update(output)
            actions_pane.update(Text())
            hint.update(Text("Esc back", style=FG_FAINTEST))
            return

        # Content width for wrapping: screen width minus the content pane's
        # horizontal padding (0 2 → 4) and a column for the scrollbar.
        width = max(20, (self.size.width or 80) - 5)
        if is_mcp:
            self._render_mcp_detail_body(output, item, detail, width)
        else:
            self._render_worker_detail_body(output, item, detail, width)

        content.update(output)

        # Actions live in a pinned pane below the scroll region so long
        # detail bodies (Recent output, tool lists, etc.) don't push the
        # selectable menu off the visible screen.
        actions_output = Text()
        if self._acting:
            verb = self._action_verb()
            actions_output.append(f"  {verb}ing...\n", style=FG_FAINTEST)
        else:
            actions = self._get_actions()
            for i, (_action_id, label) in enumerate(actions):
                is_selected = i == self._action_cursor
                prefix = "> " if is_selected else "  "
                style = f"bold {FG}" if is_selected else FG
                actions_output.append(
                    f"  {prefix}{i + 1}. ",
                    style=ACCENT if is_selected else FG_FAINTEST,
                )
                actions_output.append(f"{label}\n", style=style)
        actions_pane.update(actions_output)

        hint.update(
            Text(
                "up/down navigate · Enter select · r refresh · Esc back",
                style=FG_FAINTEST,
            )
        )

        # Body height is only known after layout, so decide the fits-vs-fills
        # layout on the next refresh once the content widget has measured.
        self.call_after_refresh(self._fit_detail_layout)

    def _fit_detail_layout(self) -> None:
        """Toggle the detail layout based on whether the body fits the viewport.

        Textual can't make a ``VerticalScroll`` both shrink to its content
        *and* cap against its siblings (``max-height: 1fr`` is a no-op against
        a sibling claiming ``1fr``), so we measure the rendered body once per
        render and switch modes via the ``detail-fits`` class:

        - **fits** → the scroll shrinks to its content and the action pane
          claims the slack, so the menu tucks right under the body and the
          footer stays pinned to the bottom (no stranded-menu gap).
        - **overflows** → the scroll fills and scrolls internally while the
          action pane shrinks to its content, so the menu and footer stay
          on screen instead of being pushed off the bottom.

        ``content.size.height`` is the true wrapped height regardless of the
        scroll viewport, so the decision is stable and doesn't oscillate when
        the mode flips.
        """
        if self._view != "detail" or not self.is_mounted:
            return
        try:
            content = self.query_one("#services-content", Static)
        except Exception:
            return
        # Sum the chrome that sits outside the scroll/actions pair: the header
        # above, plus the hint bar and the base screen's global status bar
        # below. Their heights aren't mode-dependent, so measuring them is
        # safe (unlike the action pane, which inflates to 1fr while fitting).
        chrome = 0
        for chrome_id in ("#services-header", "#services-hint", "#global-status-bar"):
            with contextlib.suppress(Exception):
                chrome += self.query_one(chrome_id, Static).size.height
        # The action pane's natural height is its content (one row per action,
        # or the "…ing" line), plus its top padding row.
        action_rows = (len(self._get_actions()) or 1) + 1
        available = self.size.height - chrome - action_rows
        fits = content.size.height <= max(1, available)
        self.set_class(fits, "detail-fits")

    def _render_mcp_detail_body(
        self,
        output: Text,
        item: dict[str, t.Any],
        detail: dict[str, t.Any] | None,
        width: int = _DEFAULT_CONTENT_WIDTH,
    ) -> None:
        """Render MCP-server-specific detail in three stacked blocks.

        A status headline (with an error callout on failure) leads, then a
        Configuration section, then a Runtime section. Grouping keeps the
        three concerns — lifecycle state, static config, live runtime —
        visually separated, and mirrors the worker view's section idiom.

        ``width`` is the content width in cells; long field values, the error
        callout, and status notes wrap to it with a hanging indent so they
        keep the section structure rather than collapsing to the left margin.
        """
        status_val = (
            detail.get("status", item.get("status", "?")) if detail else item.get("status", "?")
        )
        error = (detail or item).get("error")
        guidance = (detail or item).get("detail")

        # ── Status headline ──
        self._append_mcp_status(output, status_val, error, guidance, width)

        # Before the detail fetch settles ``detail`` is None — the headline
        # is all we can render; config/runtime fields aren't known yet.
        if not detail:
            return

        # ── Configuration ──
        output.append("\n")
        output.append("  Configuration\n", style=f"bold {FG_SUBTLE}")
        transport = detail.get("transport", "")
        self._append_field(output, "Transport", transport or "?", width)
        if transport == "stdio":
            self._append_field(output, "Command", detail.get("command") or "?", width)
            args = detail.get("args", [])
            if args:
                self._append_field(output, "Args", " ".join(str(a) for a in args), width)
        else:
            self._append_field(output, "URL", detail.get("url") or "?", width)
        self._append_field(output, "Capability", detail.get("capability") or "?", width)

        # ── Runtime ──
        output.append("\n")
        output.append("  Runtime\n", style=f"bold {FG_SUBTLE}")
        tool_count = detail.get("tool_count", 0)
        tools = detail.get("tools", [])
        if tool_count:
            self._append_field(
                output, "Tools", f"{tool_count} tool{'s' if tool_count != 1 else ''}", width
            )
        elif status_val in ("connected", "ok"):
            self._append_field(output, "Tools", "0  (server exposes no tools)", width)
        else:
            self._append_field(output, "Tools", "0  (none — server not connected)", width)

        log_path = detail.get("log_path")
        if log_path:
            self._append_field(output, "Log file", log_path, width)

        # Inline tool preview, capped — the full list lives behind "View tools".
        if tools:
            output.append("\n")
            for i, tool in enumerate(tools[:_MAX_INLINE_TOOLS]):
                self._append_inline_tool(output, i, tool, width)
            if len(tools) > _MAX_INLINE_TOOLS:
                remaining = len(tools) - _MAX_INLINE_TOOLS
                output.append(
                    f"    ... and {remaining} more (View tools to see all)\n",
                    style=FG_FAINTEST,
                )

        # Captured stderr (stdio only — HTTP transports have no process
        # output). Show it for healthy servers too, and make "nothing yet"
        # explicit rather than a silent gap.
        if transport == "stdio":
            stderr_lines = self._collect_recent_stderr(detail, item)
            if stderr_lines:
                output.append("\n")
                output.append("    Output\n", style=FG_SUBTLE)
                for line in stderr_lines:
                    output.append(f"      {line}\n", style=FG_MUTED)
            else:
                self._append_field(output, "Output", "(none captured)", width)

    def _append_field(self, output: Text, label: str, value: str, width: int) -> None:
        """Append an aligned ``label   value`` row, wrapping long values.

        Wrapped continuation lines hang-indent to the value column so the
        two-column structure survives a value that's wider than the pane.
        """
        lines = _wrap_value(value, width, _FIELD_VALUE_COL)
        output.append(f"    {label:<{_FIELD_LABEL_WIDTH}}", style=FG_MUTED)
        output.append(f"{lines[0]}\n", style=FG)
        for cont in lines[1:]:
            output.append(" " * _FIELD_VALUE_COL, style=FG_MUTED)
            output.append(f"{cont}\n", style=FG)

    def _append_inline_tool(
        self, output: Text, index: int, tool: dict[str, t.Any], width: int
    ) -> None:
        """Append a single-line ``N. name -- description`` inline tool entry.

        The line is budgeted to the content width (name first, then as much
        description as fits) so every tool stays on one row and the list keeps
        a consistent shape — the full untruncated list lives behind "View tools".
        """
        prefix = f"    {index + 1}. "
        avail = max(10, width - len(prefix))
        name = tool.get("name", "?")
        if len(name) > avail:
            name = name[: avail - 3] + "..."
        output.append(prefix, style=FG_FAINTEST)
        output.append(name, style=FG)
        # Tool descriptions often arrive as multi-paragraph docstrings
        # ("Args:\n  ...\n\nReturns:..."). Collapse runs of whitespace to single
        # spaces so the inline summary stays on one line, then fit it to what's
        # left of the row after the name.
        desc = " ".join((tool.get("description", "") or "").split())
        if len(desc) > _INLINE_TOOL_DESC_MAX_CHARS:
            desc = desc[: _INLINE_TOOL_DESC_MAX_CHARS - 3] + "..."
        remaining = avail - len(name) - len(" -- ")
        if desc and remaining > 4:
            if len(desc) > remaining:
                desc = desc[: remaining - 3] + "..."
            output.append(f" -- {desc}", style=FG_MUTED)
        output.append("\n")

    def _append_mcp_status(
        self,
        output: Text,
        status_val: str,
        error: str | None,
        guidance: str | None,
        width: int,
    ) -> None:
        """Render the status headline, reusing the list view's glyph palette.

        Failure states get an error callout instead of leaking the raw
        lifecycle token (the old catch-all rendered ``failed (error)``,
        where ``error`` was the internal component-health status).
        """
        if status_val in ("connected", "ok"):
            output.append("  ✓ Connected\n", style=SUCCESS)
        elif status_val == "connecting":
            output.append("  … Connecting\n", style=BRAND)
            self._append_note(
                output,
                "Connection runs in the background — tools appear as the server replies",
                width,
            )
        elif status_val == "needs_auth":
            output.append("  ⚠ Needs authentication\n", style=WARNING)
            self._append_note(
                output,
                guidance or "Use Authenticate to connect (opens a browser for OAuth)",
                width,
            )
        elif status_val == "gated_off":
            output.append("  ◯ Gated off\n", style=FG_MUTED)
            self._append_note(
                output,
                guidance or "Enable the required flag to start this server",
                width,
            )
        elif status_val == "degraded":
            output.append("  ⚠ Degraded\n", style=WARNING)
            self._append_error_callout(output, error, guidance, width)
        elif status_val == "enabled_failed":
            output.append("  ✗ Enabled but failed to start\n", style=ERROR)
            self._append_error_callout(output, error, guidance, width)
        else:
            # failed / error / disconnected / unknown — all read as a failure.
            output.append("  ✗ Failed\n", style=ERROR)
            self._append_error_callout(output, error, guidance, width)

    def _append_note(self, output: Text, text: str, width: int) -> None:
        """Append a sub-status note, wrapped and indented under the headline."""
        for seg in _wrap_value(text, width, 4):
            output.append(f"    {seg}\n", style=FG_FAINTEST)

    def _append_error_callout(
        self,
        output: Text,
        error: str | None,
        guidance: str | None,
        width: int,
        marker: str = _MCP_STDERR_MARKER,
    ) -> None:
        """Render the failure cause as a left-barred, full-brightness block.

        The bar (in ERROR colour) and bright body make the cause the visual
        focal point rather than another muted field. The captured output
        tail (after ``marker``) is stripped here — the "Output" block renders
        it — so the callout stays focused on the headline cause. A left bar
        (rather than a boxed border) keeps it robust across terminal widths,
        and each wrapped segment carries the bar so structure survives wrapping.
        """
        if not error and not guidance:
            return
        # Value column for the callout: 4-space indent plus the "│ " bar.
        bar_col = 6
        output.append("\n")
        if error:
            head = error.split(marker, 1)[0]
            for line in head.splitlines() or [head]:
                for seg in _wrap_value(line, width, bar_col):
                    output.append("    │ ", style=ERROR)
                    output.append(f"{seg}\n", style=FG)
        if guidance:
            for seg in _wrap_value(guidance, width, bar_col):
                output.append("    │ ", style=ERROR)
                output.append(f"{seg}\n", style=FG_MUTED)

    @staticmethod
    def _collect_recent_stderr(
        detail: dict[str, t.Any] | None, item: dict[str, t.Any]
    ) -> list[str]:
        """Return the recent stderr tail for an MCP server.

        Prefers the live ring buffer from a connected client so operators
        see output for healthy servers too; falls back to the tail embedded
        in the error message for failed connects where the client was
        discarded before its buffer could be read.
        """
        if detail:
            live = detail.get("recent_stderr") or []
            if live:
                return list(live)[-_MAX_RECENT_LINES:]
        error = (detail or item).get("error", "") if detail else item.get("error", "")
        if error and _MCP_STDERR_MARKER in error:
            return error.split(_MCP_STDERR_MARKER, 1)[1].splitlines()
        return []

    def _render_worker_detail_body(
        self,
        output: Text,
        item: dict[str, t.Any],
        detail: dict[str, t.Any] | None,
        width: int = _DEFAULT_CONTENT_WIDTH,
    ) -> None:
        """Render worker detail with the same structure as the MCP view.

        A status headline (error callout on failure) leads, then a
        Configuration section, then a Runtime section for subprocess workers
        (process / output) or a Handlers section for in-process workers.
        ``width`` drives the same hanging-indent wrapping the MCP view uses.
        """
        state_val = (
            detail.get("state", item.get("status", "?")) if detail else item.get("status", "?")
        )
        when = (detail or item).get("when") or []
        error = (detail or item).get("error")

        # ── Status headline (reuses the list view's glyph palette) ──
        self._append_worker_status(output, state_val, error, when, width)

        if not detail:
            return

        # Subprocess workers expose a process; in-process workers expose a
        # handler registry. ``kind`` is clobbered to "worker" by the fetch
        # path, so branch on which payload is present.
        process = detail.get("process") or {}
        handlers = detail.get("handlers") or {}
        is_subprocess = bool(process)

        # ── Configuration ──
        output.append("\n")
        output.append("  Configuration\n", style=f"bold {FG_SUBTLE}")
        self._append_field(output, "Type", "subprocess" if is_subprocess else "in-process", width)
        if is_subprocess:
            self._append_field(output, "Command", process.get("command") or "?", width)
            args = process.get("args") or []
            if args:
                self._append_field(output, "Args", " ".join(str(a) for a in args), width)
        self._append_field(output, "Capability", detail.get("capability") or "?", width)

        # ── Runtime (subprocess) ──
        if is_subprocess:
            output.append("\n")
            output.append("  Runtime\n", style=f"bold {FG_SUBTLE}")
            pid = process.get("pid")
            if pid is not None:
                self._append_field(output, "PID", str(pid), width)
            log_path = process.get("log_path")
            if log_path:
                self._append_field(output, "Log file", log_path, width)

            output_lines = self._collect_worker_output(detail, item)
            if output_lines:
                output.append("\n")
                output.append("    Output\n", style=FG_SUBTLE)
                for line in output_lines:
                    output.append(f"      {line}\n", style=FG_MUTED)
            else:
                self._append_field(output, "Output", "(none captured)", width)

        # ── Handlers (in-process) ──
        elif handlers:
            output.append("\n")
            output.append("  Handlers\n", style=f"bold {FG_SUBTLE}")
            rows = (
                ("tasks", handlers.get("tasks", 0)),
                ("schedules", handlers.get("schedules", 0)),
                ("events", ", ".join(handlers.get("event_kinds", []))),
                ("on_startup", handlers.get("startup", 0)),
                ("on_shutdown", handlers.get("shutdown", 0)),
            )
            rendered = False
            for label, value in rows:
                if value:
                    self._append_field(output, label, str(value), width)
                    rendered = True
            if not rendered:
                output.append("    (none)\n", style=FG_FAINTEST)

    def _append_worker_status(
        self,
        output: Text,
        state_val: str,
        error: str | None,
        when: list[str],
        width: int,
    ) -> None:
        """Render the worker status headline, mirroring the MCP headline."""
        if state_val in ("running", "ok"):
            output.append("  ✓ Running\n", style=SUCCESS)
        elif state_val in ("loading", "starting"):
            output.append("  … Starting\n", style=BRAND)
        elif state_val == "stopping":
            output.append("  … Stopping\n", style=BRAND)
        elif state_val == "stopped":
            output.append("  ◯ Stopped\n", style=FG_MUTED)
        elif state_val == "gated_off":
            # CAP-WRK-007: manifest-declared but when: predicate unsatisfied.
            output.append("  ◯ Gated off\n", style=FG_MUTED)
            if when:
                self._append_note(output, f"Enable flag(s) to start: {', '.join(when)}", width)
            else:
                self._append_note(output, "Enable the required flag(s) to start this worker", width)
        elif state_val == "error":
            output.append("  ✗ Failed\n", style=ERROR)
            self._append_error_callout(output, error, None, width, marker=_WORKER_OUTPUT_MARKER)
        else:
            output.append(f"  ⚠ {state_val}\n", style=WARNING)

    @staticmethod
    def _collect_worker_output(
        detail: dict[str, t.Any] | None, item: dict[str, t.Any]
    ) -> list[str]:
        """Return the recent output tail for a subprocess worker.

        Prefers the runner's live ring buffer; falls back to the tail embedded
        in the error message for a crash where the runner was discarded before
        its buffer could be read (mirrors the MCP stderr collector).
        """
        if detail:
            live = (detail.get("process") or {}).get("recent_output") or []
            if live:
                return list(live)[-_MAX_RECENT_LINES:]
        error = (detail or item).get("error", "") if detail else item.get("error", "")
        if error and _WORKER_OUTPUT_MARKER in error:
            return error.split(_WORKER_OUTPUT_MARKER, 1)[1].splitlines()
        return []

    # ── Tool list view (MCP only) ──

    def _handle_tool_list_key(self, key: str, event: "Key") -> None:
        if key == "escape":
            if self._tool_search:
                self._tool_search = ""
                self._render_current_view()
            else:
                self._tool_search = ""
                self._view = "detail"
                self._action_cursor = 0
                self._render_current_view()
                self._start_detail_refresh()
            return
        if key == "backspace":
            if self._tool_search:
                self._tool_search = self._tool_search[:-1]
                self._render_current_view()
            return
        if event.character and event.character.isprintable() and len(event.character) == 1:
            self._tool_search += event.character
            self._render_current_view()
            return

    def _render_tool_list(self) -> None:
        header = self.query_one("#services-header", Static)
        content = self.query_one("#services-content", Static)
        actions_pane = self.query_one("#services-actions", Static)
        hint = self.query_one("#services-hint", Static)
        actions_pane.update(Text())  # tool-list view is inline, no separate actions

        all_tools = (self._item_detail or {}).get("tools", [])
        server_name = (self._selected_item or {}).get("name", "?")
        cap_name = (self._selected_item or {}).get("capability", "?")

        query = self._tool_search.lower()
        tools = [
            tool
            for tool in all_tools
            if not query
            or query in tool.get("name", "").lower()
            or query in tool.get("description", "").lower()
        ]

        text = Text()
        text.append(" Tools", style=f"bold {FG}")
        text.append(
            f"  {len(tools)}/{len(all_tools)}" if query else f"  {len(all_tools)}", style=FG_MUTED
        )
        text.append("\n")
        text.append(f" {server_name}", style=FG_FAINTEST)
        header.update(text)

        search_bar = self.query_one("#services-search", Static)
        search_text = Text()
        if self._tool_search:
            search_text.append(f" \u2315 {self._tool_search}", style=FG)
            search_text.append("\u2581", style=FG_FAINTEST)
        else:
            search_text.append(" \u2315 Search\u2026", style=FG_FAINTEST)
        search_bar.update(search_text)

        output = Text()
        if query and not tools:
            output.append(f'No tools matching "{self._tool_search}"\n', style=f"italic {FG_MUTED}")

        for i, tool in enumerate(tools):
            if i > 0:
                output.append(
                    "────────────────────────────────────────────────\n", style=FG_FAINTEST
                )

            tool_name = tool.get("name", "?")
            qualified = f"{cap_name}:{server_name}:{tool_name}"

            output.append(f"{tool_name}  ", style=f"bold {BRAND}")
            output.append(f"{qualified}\n", style=FG_FAINTEST)
            output.append("\n")

            schema = tool.get("input_schema", {})
            properties = schema.get("properties", {})
            required_params = set(schema.get("required", []))

            if properties:
                for param_name, param_info in properties.items():
                    req_label = "required" if param_name in required_params else "optional"
                    param_type = param_info.get("type", "any")

                    output.append(param_name, style=FG)
                    output.append(f" ({req_label}): {param_type}", style=FG_MUTED)
                    param_desc = param_info.get("description")
                    if param_desc:
                        output.append(f" -- {param_desc}", style=FG_FAINTEST)
                    output.append("\n")

                output.append("\n")

            desc = tool.get("description", "")
            if desc:
                output.append(f"{desc}\n", style=FG_MUTED)

        content.update(output)
        hint.update(Text("Type to search · Esc back", style=FG_FAINTEST))

    # ── Rendering dispatch ──

    def _render_current_view(self) -> None:
        # Workers (fetch/refresh/actions) and the detail-refresh interval
        # re-render via this path. If the screen has unmounted while a worker
        # was awaiting, query_one would crash with NoMatches — bail out before
        # touching the DOM.
        if not self.is_mounted:
            return
        search = self.query_one("#services-search", Static)
        search.display = self._view == "tool_list"

        # The ``detail-fits`` layout class is owned by ``_fit_detail_layout``
        # (scheduled after a detail render, once the body height is known).
        # List / tool-list views always want the scroll to fill, so clear it.
        if self._view != "detail":
            self.set_class(False, "detail-fits")

        if self._view == "list":
            self._render_list()
        elif self._view == "detail":
            self._render_detail()
        elif self._view == "tool_list":
            self._render_tool_list()
