"""Capabilities manager screen — discover, install, and manage capabilities.

Single-column layout matching Claude Code's plugin manager pattern:
  List view:   tab bar -> search -> scrollable item list with > cursor
  Detail view: item info -> action list with > cursor
  Enter: list->detail or execute action
  Esc:   detail->list or dismiss
"""

import asyncio
import typing as t
from pathlib import Path

from loguru import logger
from packaging.version import InvalidVersion, Version
from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.css.query import NoMatches
from textual.events import Key, Paste
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
    BRAND,
    ERROR,
    FG,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    INFO,
    WARNING,
)
from dreadnode.capabilities.sync import LocalInstallClient

if t.TYPE_CHECKING:
    from textual.notifications import Notification

    from dreadnode.app.api.client import ApiClient
    from dreadnode.app.client.managed_client import ManagedRuntimeClient

# ── Tab identifiers ──────────────────────────────────────────────────────────

_TAB_AVAILABLE = "available"
_TAB_INSTALLED = "installed"
_TABS = [_TAB_AVAILABLE, _TAB_INSTALLED]
_MAX_INLINE_DETAIL_COMPONENTS = 8

# Truncation cap for the inline description column on the Available tab.
# Long enough that a typical one-line capability summary survives in full;
# anything past this gets an ellipsis and the full text lives in detail view.
_AVAILABLE_DESC_MAX_CHARS = 60


# ── Helpers ──────────────────────────────────────────────────────────────────


def _display_name(item: dict[str, t.Any]) -> str:
    """Best user-facing name for a capability."""
    dn = item.get("display_name")
    if isinstance(dn, str) and dn.strip():
        return dn
    return str(item.get("name", "?"))


def _version_cmp(available: str | None, installed: str | None) -> str:
    """Compare versions → 'install' | 'installed' | 'update'."""
    if installed is None:
        return "install"
    if not isinstance(available, str) or not isinstance(installed, str):
        return "installed"
    try:
        if Version(available) > Version(installed):
            return "update"
    except InvalidVersion:
        if available != installed:
            return "update"
    return "installed"


def _filter(items: list[dict[str, t.Any]], query: str) -> list[dict[str, t.Any]]:
    if not query:
        return items
    filters: dict[str, str] = {}
    terms: list[str] = []
    for token in query.split():
        if ":" not in token:
            terms.append(token)
            continue
        key, value = token.split(":", 1)
        key = key.strip().lower()
        value = value.strip().lower()
        if key in {"source", "state", "kind", "author", "update"} and value:
            filters[key] = value
        else:
            terms.append(token)

    q = " ".join(terms).lower().strip()
    results: list[dict[str, t.Any]] = []
    for item in items:
        source = str(item.get("source", "")).lower()
        state = str(item.get("state") or item.get("install_state") or "").lower()
        author = item.get("author")
        if isinstance(author, dict):
            author_text = str(author.get("name", "")).lower()
        else:
            author_text = str(author or "").lower()
        kinds = _component_summary(item).lower()
        has_update = bool(item.get("update_available")) or item.get("install_state") == "update"

        if filters.get("source") and source != filters["source"]:
            continue
        if filters.get("state") and state != filters["state"]:
            continue
        if filters.get("author") and filters["author"] not in author_text:
            continue
        if filters.get("kind") and filters["kind"] not in kinds:
            continue
        if filters.get("update"):
            wanted_update = filters["update"] in {"1", "true", "yes", "y"}
            if has_update != wanted_update:
                continue

        if q:
            haystack = " ".join(
                part
                for part in (
                    str(item.get("name", "")).lower(),
                    str(item.get("display_name", "")).lower(),
                    str(item.get("description") or item.get("summary") or "").lower(),
                    source,
                    state,
                    author_text,
                    kinds,
                )
                if part
            )
            if q not in haystack:
                continue
        results.append(item)
    return results


def _component_summary(item: dict[str, t.Any]) -> str:
    """One-line component summary: '3 skills · 1 agent · 2 tools'."""
    counts = item.get("component_counts", {})
    if counts:
        parts = []
        for kind in ("agent", "skill", "tool", "mcp_server", "worker"):
            n = counts.get(kind, counts.get(f"{kind}s", 0))
            if n:
                label = kind.replace("_", " ") + ("s" if n != 1 else "")
                parts.append(f"{n} {label}")
        return " · ".join(parts) if parts else ""

    components = item.get("components", [])
    agents = item.get("agents", [])
    if not components and not agents:
        return ""
    kind_counts: dict[str, int] = {}
    if agents:
        kind_counts["agent"] = len(agents)
    for c in components:
        k = c.get("kind", "?") if isinstance(c, dict) else getattr(c, "kind", "?")
        if k == "agent":
            continue
        kind_counts[k] = kind_counts.get(k, 0) + 1
    parts = []
    for kind in ("agent", "skill", "tool", "mcp_server", "worker"):
        n = kind_counts.get(kind, 0)
        if n:
            label = kind.replace("_", " ") + ("s" if n != 1 else "")
            parts.append(f"{n} {label}")
    return " · ".join(parts) if parts else ""


def _health_summary(item: dict[str, t.Any]) -> tuple[int, int, int]:
    """Return (ok, warning, error) counts from components."""
    ok = warn = err = 0
    for c in item.get("components", []):
        status = c.get("status", "ok") if isinstance(c, dict) else getattr(c, "status", "ok")
        if status == "ok":
            ok += 1
        elif status == "error":
            err += 1
        else:
            warn += 1
    return ok, warn, err


def _merge_available_sources(
    org_items: list[dict[str, t.Any]],
    public_items: list[dict[str, t.Any]],
) -> list[dict[str, t.Any]]:
    """Merge org/public available items, collapsing public visibility duplicates."""
    merged: dict[str, dict[str, t.Any]] = {}

    for item in org_items:
        merged[item["name"]] = dict(item)

    for item in public_items:
        name = item["name"]
        if name in merged:
            merged[name]["source"] = "public"
            continue
        merged[name] = dict(item)

    return list(merged.values())


def _build_fix_message(item: dict[str, t.Any]) -> str:
    """Build a diagnostic prompt for the fix agent session."""
    name = item.get("name", "unknown")
    desc = item.get("description", "")

    parts: list[str] = [f'The "{name}" capability has failing health checks and needs to be fixed.']
    if desc:
        parts.append(f"\nDescription: {desc}")

    deps = item.get("dependencies")
    if deps:
        dep_lines: list[str] = []
        if deps.get("python"):
            dep_lines.append(f"  Python: {', '.join(deps['python'])}")
        if deps.get("packages"):
            dep_lines.append(f"  System packages: {', '.join(deps['packages'])}")
        if deps.get("scripts"):
            dep_lines.append(f"  Setup scripts: {', '.join(deps['scripts'])}")
        if dep_lines:
            parts.append("\nDeclared dependencies:\n" + "\n".join(dep_lines))

    components = item.get("components", [])
    check_entries = [c for c in components if isinstance(c, dict) and c.get("kind") == "check"]
    if check_entries:
        check_lines: list[str] = []
        for c in check_entries:
            cname = c.get("name", "?")
            status = c.get("status", "?")
            error = c.get("error", "")
            if status == "ok":
                check_lines.append(f"  PASS: {cname}")
            else:
                check_lines.append(f"  FAIL: {cname} — {error}")
        parts.append("\nCheck results:\n" + "\n".join(check_lines))

    checks = item.get("checks")
    if checks:
        cmd_lines = [f"  {c.get('name', '?')}: {c.get('command', '?')}" for c in checks]
        parts.append("\nCheck commands:\n" + "\n".join(cmd_lines))

    parts.append(
        "\nThese checks verify that the capability's prerequisites "
        "(system packages, Python libraries, etc.) are installed correctly. "
        "Fix the environment so the checks pass — install missing dependencies, "
        "not modify the checks themselves. Do not edit capability.yaml."
    )

    return "\n".join(parts)


def _build_actions(
    item: dict[str, t.Any],
    *,
    is_installed: bool,
    is_sandbox: bool,
    has_platform: bool,
    runtime_id: str | None,
) -> list[tuple[str, str]]:
    """Return list of (action_id, label) for the action list.

    CAP-RT-002: local runtimes expose local management only.
    CAP-RT-003: sandbox runtimes expose runtime management only.
    """
    actions: list[tuple[str, str]] = []

    if is_installed:
        state = item.get("state", "enabled")
        source = item.get("source", "local")

        update_ver = item.get("update_available")
        # Local-path installs (symlink/copy) are managed manually — registry
        # update would silently replace the symlink with a download.
        is_local_path_install = item.get("provenance") == "local"
        if update_ver and not is_sandbox and not is_local_path_install:
            actions.append(("update_local", f"Update to v{update_ver}"))
        elif update_ver and is_sandbox and item.get("binding_id"):
            actions.append(("update", f"Update to v{update_ver}"))

        # The default bundled capability provides the active agent and
        # tool surface — disabling it from the UI would brick the runtime.
        if item.get("name") != "dreadnode":
            if state == "enabled":
                actions.append(("toggle", "Disable capability"))
            else:
                actions.append(("toggle", "Enable capability"))

        if item.get("local_path"):
            actions.append(("browse_files", "Browse files"))

        if is_sandbox and source == "runtime" and item.get("binding_id"):
            actions.append(("remove", "Remove"))
        elif not is_sandbox and source in ("local", "package"):
            actions.append(("remove_local", "Remove"))

        if state == "enabled" and any(
            c.get("kind") == "check" and c.get("status") == "error"
            for c in item.get("components", [])
            if isinstance(c, dict)
        ):
            actions.append(("fix", "Fix"))
    else:
        install_state = item.get("install_state", "install")
        if install_state == "install":
            if has_platform and (runtime_id or not is_sandbox):
                actions.append(("install", "Install"))
            elif not has_platform:
                actions.append(("noop", "Install unavailable (not authenticated)"))
            else:
                actions.append(("noop", "Install unavailable (no runtime)"))
        elif install_state == "update":
            if has_platform and (runtime_id or not is_sandbox):
                if is_sandbox and item.get("binding_id"):
                    actions.append(("update", "Update to latest"))
                else:
                    actions.append(("update_local", "Update to latest"))
            elif not has_platform:
                actions.append(("noop", "Update unavailable (not authenticated)"))
            else:
                actions.append(("noop", "Update unavailable (no runtime)"))
        elif install_state == "installed":
            actions.append(("noop", "Already installed"))
        elif install_state == "disabled":
            actions.append(("noop", "Installed (disabled)"))

    return actions


def _format_provenance(provenance: str | None) -> str | None:
    """Return the user-facing provenance label for installed local capabilities."""
    if provenance == "local":
        return "local (authored)"
    if provenance in {"org", "public"}:
        return provenance
    return None


def _local_symlink_target(item: dict[str, t.Any]) -> str | None:
    """Resolved symlink target for a local-path install, or None.

    Local-path installs (CLI default for ``install <path>``) live as symlinks
    in the user store. Surfacing the target makes the install mode obvious
    and explains why ``Update`` is hidden — edits to the target are already
    live.
    """
    name = item.get("name")
    if not isinstance(name, str) or not name:
        return None
    if item.get("provenance") != "local" and item.get("source") not in {"local", "package"}:
        return None
    try:
        from dreadnode.storage.storage import Storage

        store_path = Storage().capabilities_path / name
        if store_path.is_symlink():
            return str(store_path.readlink())
    except Exception:
        return None
    return None


def _notification_name(name: str) -> str:
    """Return a short capability name for user-facing notifications."""
    if "/" in name:
        return name.split("/", 1)[1]
    return name


# ── Main screen ──────────────────────────────────────────────────────────────


class CapabilitiesScreen(DreadnodeScreen):
    """Full-screen capability manager — discover, install, manage."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("ctrl+u", "update_current", "Update", show=False),
        Binding("escape", "escape", "Back / Close", show=False),
        Binding("enter", "confirm", "Select", show=False),
        Binding("space", "toggle_row", "Toggle", show=False),
        Binding("tab", "next_tab", "Next tab", show=False),
        Binding("shift+tab", "prev_tab", "Prev tab", show=False),
        Binding("right", "next_tab", "Next tab", show=False),
        Binding("left", "prev_tab", "Prev tab", show=False),
        Binding("up", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
    ]

    def __init__(
        self,
        runtime_client: "ManagedRuntimeClient",
        api: "ApiClient | None" = None,
        org: str | None = None,
        workspace: str | None = None,
        runtime_id: str | None = None,
        is_sandbox: bool = False,
        initial_capability: str | None = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._runtime_client = runtime_client
        self._api = api
        self._org = org
        self._workspace = workspace
        self._runtime_id = runtime_id
        self._is_sandbox = is_sandbox
        # When set, the screen opens straight into this capability's detail
        # view (Installed tab) once data has loaded — used by the services
        # screen to jump from an MCP server / worker to its owning capability.
        # Consumed once, so an Esc back to the list behaves normally afterwards.
        self._initial_capability: str | None = initial_capability

        self._active_tab: str = _TAB_AVAILABLE
        self._installed_items: list[dict[str, t.Any]] = []
        self._available_items: list[dict[str, t.Any]] = []

        # View state
        self._view: str = "list"  # "list" or "detail"
        self._cursor: int = 0
        self._action_cursor: int = 0
        self._search_query: str = ""
        self._visible_items: list[dict[str, t.Any]] = []
        self._selected_item: dict[str, t.Any] | None = None
        self._current_flags: list[dict[str, t.Any]] = []
        self._current_actions: list[tuple[str, str]] = []
        self._pending_local_overwrite_key: str | None = None
        self._pending_action_name: str | None = None
        self._pending_action_label: str | None = None
        self._pending_action_notification: Notification | None = None

    @property
    def _has_platform(self) -> bool:
        return self._api is not None and self._org is not None

    @property
    def _tabs(self) -> list[str]:
        """Visible tabs for the current host type."""
        return [_TAB_AVAILABLE, _TAB_INSTALLED]

    # ── Compose ──────────────────────────────────────────────────────────

    def compose_content(self) -> ComposeResult:
        yield Static(id="cap-header")
        yield Static(id="cap-search")
        yield DataTable(id="cap-table")
        with VerticalScroll(id="cap-detail-scroll", classes="-hidden"):
            yield Static(id="cap-content")
        # Pinned below the scroll region so a long Components list or
        # description can't push the interactive flags / actions menu
        # off the bottom of the screen. Non-detail views clear it.
        yield Static(id="cap-actions")
        yield Static(id="cap-hint-bar")

    def on_mount(self) -> None:
        super().on_mount()
        table = self.query_one("#cap-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        self._configure_columns_for_tab()
        self._render_header()
        self._render_hints()
        self._load_data()

    def _configure_columns_for_tab(self) -> None:
        """Rebuild table columns for the active tab.

        Available and Installed present different information:

        * Available answers "should I install this?" — trust signals
          (source, author), what you'd be adding (components), and a
          short description so the user doesn't have to enter detail
          view for every row to know what each capability *does*.
        * Installed answers "what's running and is it healthy?" —
          runtime state, update availability, flag status.

        Keeping two distinct column sets avoids junk cells (Available
        rows previously had ``State=install`` and ``Update=-`` hardcoded
        on every row because the fetch step filters installed/update
        variants out before they reach the table).
        """
        try:
            table = self.query_one("#cap-table", DataTable)
        except NoMatches:
            # Screen not yet composed/mounted (e.g., during testing)
            return

        table.clear(columns=True)
        if self._active_tab == _TAB_AVAILABLE:
            table.add_columns("Name", "Source", "Version", "Components", "Description")
        else:
            table.add_columns("Name", "State", "Source", "Version", "Update", "Flags", "Components")

    # ── Keyboard handling ────────────────────────────────────────────────

    def on_key(self, event: Key) -> None:
        """Route typed characters into the search input.

        All non-character keys (arrows, enter, space, escape, tab, etc.) are
        declared in ``BINDINGS`` and fire via ``action_*`` methods. This
        handler only exists to feed the search bar and to let ``escape``
        clear the search before the binding's dismiss fires.
        """
        key = event.key

        # Control combos and function keys pass through to app-level bindings.
        if key.startswith("ctrl+") or (key.startswith("f") and key[1:].isdigit()):
            return

        # Escape clears search when active; BINDINGS handles it otherwise.
        if key == "escape" and self._search_query:
            self._search_query = ""
            self._cursor = 0
            self._render_current_view()
            event.prevent_default()
            event.stop()
            return

        # Search only feeds from list view. Detail view defers entirely to BINDINGS.
        if self._view != "list":
            return

        search_result = handle_search_input_key(
            self._search_query, key=key, character=event.character
        )
        if not search_result.handled:
            return
        if search_result.new_query != self._search_query:
            self._search_query = search_result.new_query
            if search_result.cursor_should_reset:
                self._cursor = 0
            logger.debug("capabilities search | query={}", self._search_query)
            self._render_current_view()
        event.prevent_default()
        event.stop()

    def on_paste(self, event: Paste) -> None:
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

    # ── BINDINGS actions ─────────────────────────────────────────────────

    def action_escape(self) -> None:
        """Escape: back to list from detail, otherwise dismiss the screen."""
        if self._view == "detail":
            self._back_to_list()
        else:
            self.dismiss()

    def action_confirm(self) -> None:
        """Enter: open detail for the focused row, or confirm the detail action."""
        if self._view == "detail":
            self._confirm_detail_action()
            return
        if not self._visible_items:
            return
        self._selected_item = self._visible_items[self._cursor]
        self._pending_local_overwrite_key = None
        self._action_cursor = 0
        self._view = "detail"
        self._render_current_view()

    def action_toggle_row(self) -> None:
        """Space: toggle the focused row in list view, confirm in detail view."""
        if self._view == "detail":
            self._confirm_detail_action()
        else:
            self._toggle_current()

    def action_next_tab(self) -> None:
        if self._view == "list":
            self._switch_tab(1)

    def action_prev_tab(self) -> None:
        if self._view == "list":
            self._switch_tab(-1)

    def action_cursor_up(self) -> None:
        """Up arrow: action-cursor up in detail view. DataTable handles list."""
        if self._view == "detail":
            self._action_cursor = max(0, self._action_cursor - 1)
            self._render_current_view()

    def action_cursor_down(self) -> None:
        if self._view == "detail":
            n_flags = len(self._current_flags)
            n_actions = len(self._current_actions)
            total = n_flags + n_actions + 1  # +1 for "Back"
            self._action_cursor = min(total - 1, self._action_cursor + 1)
            self._render_current_view()

    def action_update_current(self) -> None:
        """Update the capability under the cursor (ctrl+u). Installed tab only."""
        if self._view != "list" or self._active_tab != _TAB_INSTALLED:
            return
        if not self._visible_items or not (0 <= self._cursor < len(self._visible_items)):
            return
        item = self._visible_items[self._cursor]
        update_ver = item.get("update_available")
        if not update_ver:
            return
        self._selected_item = item
        artifact_identity = item.get("canonical_name") or item.get("name")
        provenance = item.get("provenance")
        if not self._is_sandbox and artifact_identity:
            self._show_action_notice(item["name"], "Updating")
            self.call_after_refresh(
                self._do_update_local,
                artifact_identity,
                update_ver,
                source=provenance,
            )
        elif self._is_sandbox and item.get("binding_id"):
            self._show_action_notice(item["name"], "Updating")
            self.call_after_refresh(
                self._do_update,
                item["binding_id"],
                item["name"],
                update_ver,
            )

    def _confirm_detail_action(self) -> None:
        n_flags = len(self._current_flags)
        n_actions = len(self._current_actions)
        if self._action_cursor < n_flags:
            self._toggle_flag_at_cursor()
            return
        if self._action_cursor < n_flags + n_actions:
            action_id = self._current_actions[self._action_cursor - n_flags][0]
            if action_id != "noop":
                self._execute_action(action_id)
            return
        self._back_to_list()

    # ── Tab switching ────────────────────────────────────────────────────

    def _switch_tab(self, direction: int) -> None:
        tabs = self._tabs
        idx = tabs.index(self._active_tab) if self._active_tab in tabs else 0
        self._active_tab = tabs[(idx + direction) % len(tabs)]
        self._search_query = ""
        self._cursor = 0
        self._view = "list"
        self._pending_local_overwrite_key = None
        self._configure_columns_for_tab()
        self._render_current_view()

    def _back_to_list(self) -> None:
        self._view = "list"
        self._pending_local_overwrite_key = None
        self._configure_columns_for_tab()
        self._render_current_view()

    # ── Rendering ────────────────────────────────────────────────────────

    def _render_current_view(self) -> None:
        # Workers (cap-action, cap-load) re-render via this path. If the screen
        # has unmounted while a worker was awaiting, query_one would crash with
        # NoMatches — bail out before touching the DOM.
        if not self.is_mounted:
            return
        self._render_header()
        search = self.query_one("#cap-search", Static)
        search.display = self._view != "detail"
        if self._view == "detail":
            self._render_detail_view()
        else:
            self._render_list_view()
        self._render_hints()

    def _build_tab_strip(self) -> Text:
        """Build the [Available] [Installed] tab strip for the header.

        Capabilities embeds tab pills inside the title bar — each tab shows
        a count of items in that tab and the active tab is reverse-styled.
        """
        text = Text()
        for tab in self._tabs:
            label = tab.capitalize()
            count = (
                len(self._installed_items) if tab == _TAB_INSTALLED else len(self._available_items)
            )
            if tab == self._active_tab:
                text.append(f" {label}", style=f"bold reverse {BRAND}")
                if count:
                    text.append(f" ({count})", style=f"reverse {BRAND}")
                text.append(" ", style=f"reverse {BRAND}")
            else:
                text.append(f" {label}", style=FG_MUTED)
                if count:
                    text.append(f" ({count})", style=FG_FAINTEST)
                text.append(" ")
            text.append("  ")
        text.append("(Tab to switch)", style=FG_FAINTEST)
        return text

    def _render_header(self) -> None:
        self.query_one("#cap-header", Static).update(
            render_screen_header(
                "Capabilities",
                "Browse and manage installed capabilities",
                header_extra=self._build_tab_strip(),
            )
        )

    def _render_hints(self) -> None:
        if self._view == "detail":
            if self._current_flags and self._action_cursor < len(self._current_flags):
                hints: list[tuple[str, str]] = [
                    ("Space", "toggle flag"),
                    ("↑↓", "navigate"),
                    ("Esc", "back"),
                ]
            else:
                hints = [("Enter", "select"), ("↑↓", "navigate"), ("Esc", "back")]
        else:
            hints = [
                ("Type", "search"),
                ("Tab", "switch tab"),
                ("Space", "toggle"),
                ("Enter", "details"),
                ("Esc", "close"),
            ]
            if self._active_tab == _TAB_INSTALLED and any(
                i.get("update_available") for i in self._visible_items
            ):
                hints.insert(2, ("^U", "update"))
        self.query_one("#cap-hint-bar", Static).update(render_hint_bar(hints))

    def _render_search(self) -> None:
        self.query_one("#cap-search", Static).update(
            render_search_bar(
                self._search_query,
                cursor=self._cursor,
                visible_count=len(self._visible_items),
                placeholder=(
                    "Search\u2026  filters: source:local  state:enabled  kind:tool  update:yes"
                ),
            )
        )

    def _render_list_view(self) -> None:
        detail_scroll = self.query_one("#cap-detail-scroll", VerticalScroll)
        table = self.query_one("#cap-table", DataTable)
        actions_pane = self.query_one("#cap-actions", Static)
        self.query_one("#cap-content", Static).remove_class("detail-view")
        # Hide (not just clear) — the pane is `height: 1fr` so even an
        # empty Text would claim flex space that the DataTable needs.
        actions_pane.update(Text())
        actions_pane.add_class("-hidden")
        items = self._current_items()
        visible = _filter(items, self._search_query)
        self._visible_items = visible
        self._cursor = min(self._cursor, max(0, len(visible) - 1))

        self._render_search()
        table.clear()

        if not visible:
            table.add_class("-hidden")
            detail_scroll.remove_class("-hidden")
            text = Text()
            if self._search_query:
                text.append(f'  No matches for "{self._search_query}"\n', style=FG_MUTED)
            elif not items:
                if self._active_tab == _TAB_AVAILABLE:
                    if not self._has_platform:
                        text.append("  No capabilities available\n\n", style=FG_MUTED)
                        text.append("  Sign in with ", style=FG_FAINTEST)
                        text.append("dn auth", style=FG_SUBTLE)
                        text.append(" to browse the capability registry.\n", style=FG_FAINTEST)
                    else:
                        text.append("  No capabilities available\n\n", style=FG_MUTED)
                        text.append("  Check the capability registry at ", style=FG_FAINTEST)
                        text.append("app.dreadnode.io", style=FG_SUBTLE)
                        text.append(" for new capabilities.\n", style=FG_FAINTEST)
                else:
                    text.append("  No capabilities installed\n\n", style=FG_MUTED)
                    text.append("  Switch to the ", style=FG_FAINTEST)
                    text.append("Available", style=FG_SUBTLE)
                    text.append(" tab to discover and install capabilities.\n", style=FG_FAINTEST)
                    text.append("  Or place a ", style=FG_FAINTEST)
                    text.append("capability.yaml", style=FG_SUBTLE)
                    text.append(" in your working directory.\n", style=FG_FAINTEST)
            self.query_one("#cap-content", Static).update(text)
            return

        detail_scroll.add_class("-hidden")
        table.remove_class("-hidden")
        table.focus()

        for item in visible:
            if self._active_tab == _TAB_AVAILABLE:
                self._add_available_row(table, item)
            else:
                self._add_installed_row(table, item)

        if visible:
            table.move_cursor(row=self._cursor, column=0, animate=False, scroll=True)

    def _add_available_row(self, table: DataTable, item: dict[str, t.Any]) -> None:
        """Render one row on the Available tab.

        Columns answer "should I install this?": source is the trust
        signal, version is what would be installed, components shows what
        you'd be adding, and description is a one-liner so the list is
        scannable without dropping into detail view for each row.
        Already-installed capabilities are filtered out upstream — they
        live on the Installed tab where management actions are wired up.
        """
        version = item.get("version") or "-"
        source = str(item.get("source", "") or "-")
        source_style = ACCENT if source == "org" else FG_MUTED
        components = _component_summary(item) or "-"

        raw_desc = str(item.get("summary") or item.get("description") or "").strip()
        desc_oneline = " ".join(raw_desc.split())
        if len(desc_oneline) > _AVAILABLE_DESC_MAX_CHARS:
            desc_oneline = desc_oneline[: _AVAILABLE_DESC_MAX_CHARS - 1] + "…"
        desc_label = desc_oneline or "-"

        table.add_row(
            Text(_display_name(item), style=f"bold {FG}"),
            Text(source, style=source_style),
            Text(version, style=FG),
            Text(components, style=FG_MUTED),
            Text(desc_label, style=FG_SUBTLE if desc_oneline else FG_FAINTEST),
            key=str(item.get("row_key") or item.get("name")),
        )

    def _add_installed_row(self, table: DataTable, item: dict[str, t.Any]) -> None:
        """Render one row on the Installed tab.

        Columns answer "what's running and is it healthy?" — runtime
        state, update availability, flag status. Preserved from the
        original unified row layout.
        """
        version = item.get("version") or "-"
        update_ver = item.get("update_available")
        update_label = f"v{update_ver}" if update_ver else "-"
        components = _component_summary(item) or "-"
        source = str(item.get("source", "") or "-")

        flags = item.get("flags", [])
        if flags:
            active = sum(1 for f in flags if f.get("effective"))
            flag_label = f"⚑ {active}/{len(flags)}"
        else:
            flag_label = "-"

        state = str(item.get("state", "enabled"))
        _, _, err_count = _health_summary(item)
        if err_count:
            state = f"{state} · {err_count} error"

        dim = FG_FAINTEST if state == "disabled" else ""
        state_style = dim or (ACCENT if state == "enabled" else FG_MUTED)
        flag_style = dim or (ACCENT if flags else "")

        table.add_row(
            Text(_display_name(item), style=dim),
            Text(state, style=state_style),
            Text(source, style=dim),
            Text(version, style=dim),
            Text(update_label, style=dim),
            Text(flag_label, style=flag_style),
            Text(components, style=dim),
            key=str(item.get("row_key") or item.get("name")),
        )

    def _render_detail_view(self) -> None:
        item = self._selected_item
        if not item:
            return

        is_installed = self._active_tab == _TAB_INSTALLED
        self.query_one("#cap-table", DataTable).add_class("-hidden")
        self.query_one("#cap-detail-scroll", VerticalScroll).remove_class("-hidden")
        content = self.query_one("#cap-content", Static)
        actions_pane = self.query_one("#cap-actions", Static)
        actions_pane.remove_class("-hidden")
        content.add_class("detail-view")

        text = Text()

        # Name with status dot for installed items
        if is_installed:
            state = item.get("state", "enabled")
            dot_style = ACCENT if state == "enabled" else WARNING
            text.append(f"{'●' if state == 'enabled' else '◯'} ", style=dot_style)
        text.append(_display_name(item), style=f"bold {FG}")
        if item.get("version"):
            text.append(f"  v{item['version']}", style=FG_MUTED)
        text.append("\n")

        # Description (CSS padding-left on .detail-view handles wrap indent)
        desc = " ".join((item.get("description") or item.get("summary") or "").split())
        if desc:
            text.append(f"{desc}\n", style=FG_SUBTLE)

        text.append("\n")

        # Structured metadata fields
        if is_installed and not self._is_sandbox:
            provenance = _format_provenance(t.cast("str | None", item.get("provenance")))
            if provenance is not None:
                text.append("Provenance: ", style=FG_MUTED)
                text.append(f"{provenance}\n", style=FG_SUBTLE)
            link_target = _local_symlink_target(item)
            if link_target is not None:
                text.append("Linked from: ", style=FG_MUTED)
                text.append(f"{link_target}\n", style=FG_SUBTLE)
        elif not is_installed:
            source = item.get("source", "")
            if source:
                text.append("Source: ", style=FG_MUTED)
                text.append(f"{source}\n", style=FG_SUBTLE)

        if item.get("author"):
            author = item["author"]
            if isinstance(author, dict):
                author = author.get("name", str(author))
            text.append("Author: ", style=FG_MUTED)
            text.append(f"{author}\n", style=FG_SUBTLE)

        if item.get("license"):
            text.append("License: ", style=FG_MUTED)
            text.append(f"{item['license']}\n", style=FG_SUBTLE)

        if is_installed:
            state = item.get("state", "enabled")
            text.append("Status: ", style=FG_MUTED)
            if state == "enabled":
                text.append("Enabled\n", style=ACCENT)
            elif state == "disabled":
                text.append("Disabled\n", style=WARNING)
            update_ver = item.get("update_available")
            if update_ver:
                text.append("Update: ", style=FG_MUTED)
                text.append(f"v{update_ver} available\n", style=INFO)

        # Components — individual listing for installed, summary for available
        components = item.get("components", [])
        agents_list = item.get("agents", [])
        if is_installed and (components or agents_list):
            text.append("\nComponents\n", style=f"bold {FG_SUBTLE}")
            inline_components: list[tuple[str, str, str, str]] = []
            for agent in agents_list:
                aname = (
                    agent.get("name", "?")
                    if isinstance(agent, dict)
                    else getattr(agent, "name", "?")
                )
                inline_components.append(("agent".ljust(10), aname, "ok", ""))
            for c in components:
                kind = c.get("kind", "?") if isinstance(c, dict) else getattr(c, "kind", "?")
                if kind == "agent":
                    continue  # already listed from agents_list above
                cname = c.get("name", "?") if isinstance(c, dict) else getattr(c, "name", "?")
                status = (
                    c.get("status", "ok") if isinstance(c, dict) else getattr(c, "status", "ok")
                )
                error = c.get("error", "") if isinstance(c, dict) else getattr(c, "error", "")
                inline_components.append((kind.replace("_", " ").ljust(10), cname, status, error))

            for kind_label, cname, status, error in inline_components[
                :_MAX_INLINE_DETAIL_COMPONENTS
            ]:
                text.append(f"  {kind_label}  ", style=FG_MUTED)
                if status == "error":
                    text.append(f"✗ {cname}", style=ERROR)
                    if error:
                        text.append(f" ({error})", style=FG_SUBTLE)
                elif status == "degraded":
                    text.append(f"{cname}", style=WARNING)
                else:
                    text.append(f"{cname}", style=FG_SUBTLE)
                text.append("\n")
            if len(inline_components) > _MAX_INLINE_DETAIL_COMPONENTS:
                remaining = len(inline_components) - _MAX_INLINE_DETAIL_COMPONENTS
                text.append(
                    f"  ... and {remaining} more\n",
                    style=FG_FAINTEST,
                )
        elif not is_installed:
            # Available items carry a structured component_details list
            # (type + name + description). Show it inline so users can
            # see what's actually in the capability before installing —
            # a count summary alone ("1 agent · 2 tools") doesn't tell
            # you what those agents and tools do. Falls back to the
            # count summary when the server didn't return details.
            comp_details = item.get("component_details") or []
            if comp_details:
                text.append("\nComponents\n", style=f"bold {FG_SUBTLE}")
                for entry in comp_details[:_MAX_INLINE_DETAIL_COMPONENTS]:
                    if not isinstance(entry, dict):
                        continue
                    kind = str(entry.get("type") or "?")
                    cname = str(entry.get("name") or "?")
                    desc = " ".join((entry.get("description") or "").split())
                    text.append(f"  {kind.replace('_', ' ').ljust(10)}  ", style=FG_MUTED)
                    if desc:
                        if len(desc) > _AVAILABLE_DESC_MAX_CHARS:
                            desc = desc[: _AVAILABLE_DESC_MAX_CHARS - 3] + "..."
                        text.append(f"{cname} ", style=FG_SUBTLE)
                        text.append(f"· {desc}\n", style=FG_FAINTEST)
                    else:
                        text.append(f"{cname}\n", style=FG_SUBTLE)
                if len(comp_details) > _MAX_INLINE_DETAIL_COMPONENTS:
                    remaining = len(comp_details) - _MAX_INLINE_DETAIL_COMPONENTS
                    text.append(f"  ... and {remaining} more\n", style=FG_FAINTEST)
            else:
                comp = _component_summary(item)
                if comp:
                    text.append("\nComponents: ", style=FG_MUTED)
                    text.append(f"{comp}\n", style=FG_SUBTLE)

        content.update(text)

        # Interactive list — Flags + Actions + Back — lives in the pinned
        # pane below the scroll region so a long description / component
        # list can't push the cursorable menu off the visible screen.
        flags = item.get("flags", []) if is_installed else []
        self._current_flags = flags
        cursor = self._action_cursor

        actions_text = Text()
        if flags:
            actions_text.append("Flags\n", style=f"bold {FG_SUBTLE}")
            for fi, flag in enumerate(flags):
                effective = flag.get("effective", False)
                source = flag.get("source", "default")
                locked = source in ("env", "cli")
                is_sel = cursor == fi

                if is_sel:
                    actions_text.append("❯ ", style=f"bold {ACCENT}")
                else:
                    actions_text.append("  ")

                dot = "●" if effective else "◯"
                if locked:
                    dot_style = FG_MUTED
                elif effective:
                    dot_style = ACCENT
                else:
                    dot_style = FG_FAINTEST
                actions_text.append(f"{dot} ", style=dot_style)

                name_style = f"bold {FG}" if is_sel else (FG_MUTED if locked else FG)
                actions_text.append(flag.get("name", "?"), style=name_style)

                desc = flag.get("description", "")
                if desc:
                    if len(desc) > 48:
                        desc = desc[:45] + "..."
                    actions_text.append(f"  {desc}", style=FG_FAINTEST)

                if locked:
                    actions_text.append(f"  🔒 {source}", style=WARNING)
                actions_text.append("\n")
            actions_text.append("\n")

        # Action list — cursor indices N..N+M-1, then "Back" at N+M
        n_flags = len(flags)
        if (
            not is_installed
            and not self._is_sandbox
            and self._pending_local_overwrite_key == item.get("row_key")
        ):
            actions = [
                ("overwrite_install", "Overwrite existing local install"),
                ("cancel_overwrite", "Cancel"),
            ]
        else:
            actions = _build_actions(
                item,
                is_installed=is_installed,
                is_sandbox=self._is_sandbox,
                has_platform=self._has_platform,
                runtime_id=self._runtime_id,
            )
        if item.get("name") == self._pending_action_name and self._pending_action_label:
            actions = [("noop", self._pending_action_label)]
        self._current_actions = actions

        for i, (action_id, label) in enumerate(actions):
            ai = n_flags + i
            if ai == cursor:
                actions_text.append("❯ ", style=f"bold {ACCENT}")
            else:
                actions_text.append("  ")
            if action_id == "noop":
                actions_text.append(f"{label}\n", style=FG_FAINTEST)
            elif action_id in ("remove", "remove_local"):
                actions_text.append(f"{label}\n", style=ERROR)
            elif action_id in ("install", "update", "update_local"):
                actions_text.append(f"{label}\n", style=INFO)
            else:
                actions_text.append(f"{label}\n", style=FG)

        back_idx = n_flags + len(actions)
        if cursor == back_idx:
            actions_text.append("❯ ", style=f"bold {ACCENT}")
        else:
            actions_text.append("  ")
        actions_text.append("Back to capability list", style=FG_SUBTLE)

        actions_pane.update(actions_text)

    @on(DataTable.RowHighlighted, "#cap-table")
    def _on_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        self._cursor = event.cursor_row
        if self._view == "list":
            self._render_search()

    @on(DataTable.RowSelected, "#cap-table")
    def _on_row_selected(self, event: DataTable.RowSelected) -> None:
        if self._view != "list" or event.row_key is None:
            return
        row_key = str(event.row_key.value)
        for index, item in enumerate(self._visible_items):
            candidate = str(item.get("row_key") or item.get("name"))
            if candidate == row_key:
                self._cursor = index
                self._selected_item = item
                self._pending_local_overwrite_key = None
                self._action_cursor = 0
                self._view = "detail"
                self._render_current_view()
                return

    # ── Flag toggle from detail ─────────────────────────────────────────

    def _toggle_flag_at_cursor(self) -> None:
        if self._selected_item is None:
            return
        item = self._selected_item
        idx = self._action_cursor
        if idx < 0 or idx >= len(self._current_flags):
            return
        flag = self._current_flags[idx]
        flag_name = flag.get("name", "")
        if flag.get("source") in ("env", "cli"):
            self.notify(
                f"Flag '{flag_name}' is locked by {flag['source']} override",
                severity="warning",
            )
            return
        new_value = not flag.get("effective", False)
        verb = "Enabling" if new_value else "Disabling"
        self._show_action_notice(item["name"], f"{verb} flag {flag_name}")
        if item.get("source") == "runtime" and item.get("binding_id"):
            self._do_toggle_flag(item["binding_id"], item["name"], flag_name, value=new_value)
        else:
            self._do_toggle_flag_local(item["name"], flag_name, value=new_value)

    # ── Toggle from list ─────────────────────────────────────────────────

    def _toggle_current(self) -> None:
        if not self._visible_items or self._cursor >= len(self._visible_items):
            return
        item = self._visible_items[self._cursor]

        if self._active_tab == _TAB_INSTALLED:
            if item.get("source") == "runtime" and item.get("binding_id"):
                new_enabled = item.get("state") != "enabled"
                self._do_toggle(item["binding_id"], enabled=new_enabled)
            elif item.get("source") in ("local", "package"):
                new_enabled = item.get("state") != "enabled"
                self._do_toggle_local(item["name"], enabled=new_enabled)
        else:
            install_state = item.get("install_state", "install")
            if (
                install_state == "install"
                and self._has_platform
                and (self._runtime_id or not self._is_sandbox)
            ):
                self._show_action_notice(item["name"], "Installing")
                self.call_after_refresh(
                    self._do_install,
                    item["name"],
                    item.get("version"),
                    source=t.cast("str | None", item.get("source")),
                )

    # ── Data loading ─────────────────────────────────────────────────────

    def _current_items(self) -> list[dict[str, t.Any]]:
        if self._active_tab == _TAB_INSTALLED:
            return self._installed_items
        return self._available_items

    @work(exclusive=True, group="cap-load")
    async def _load_data(self) -> None:
        await self._fetch_installed()
        await self._fetch_available()
        self._refresh_selected_item()
        self._open_initial_capability()
        self._render_current_view()

    def _open_initial_capability(self) -> None:
        """Jump straight to a requested capability's detail once loaded.

        Matches the requested name against any identifier an installed
        capability exposes (bare ``name``, canonical ``org/name``, or
        ``display_name``) since callers — e.g. the services screen, which
        passes the component's owning ``capability`` — may know it in any
        of those forms. Consumed once so a later Esc-to-list is unaffected.
        Falls back to the Installed list with a notice if it's not found.
        """
        name = self._initial_capability
        if not name:
            return
        self._initial_capability = None

        for idx, item in enumerate(self._installed_items):
            identifiers = (
                item.get("name"),
                item.get("canonical_name"),
                item.get("display_name"),
            )
            if name in identifiers:
                self._active_tab = _TAB_INSTALLED
                self._selected_item = item
                # Keep the list cursor in sync with the selection (no search
                # filter is active on a fresh jump, so visible == installed)
                # so an Esc back to the list highlights this row, not row 0.
                self._cursor = idx
                self._action_cursor = 0
                self._pending_local_overwrite_key = None
                self._view = "detail"
                self._configure_columns_for_tab()
                return

        self._active_tab = _TAB_INSTALLED
        self._configure_columns_for_tab()
        self.notify(f"Capability '{name}' not found", severity="warning")

    def _show_installed_detail(
        self,
        *,
        name: str,
        installed_name: str,
        version: str | None,
        source: str,
    ) -> None:
        """Move the detail view into an installed-state representation."""
        canonical_name = name if "/" in name else f"{self._org}/{name}" if self._org else name
        self._active_tab = _TAB_INSTALLED
        self._view = "detail"
        self._action_cursor = 0
        self._pending_local_overwrite_key = None
        self._selected_item = {
            "row_key": f"{source}:{installed_name}:",
            "name": installed_name,
            "display_name": installed_name,
            "canonical_name": canonical_name,
            "summary": "",
            "description": "",
            "source": source,
            "provenance": None,
            "state": "enabled",
            "version": version,
            "binding_id": None,
            "author": None,
            "license": None,
            "origin": None,
            "agents": [],
            "components": [],
            "update_available": None,
            "local_path": None,
        }
        self._render_current_view()

    def _refresh_selected_item(self) -> None:
        """Refresh the selected item from the latest loaded data when possible."""
        if self._selected_item is None:
            return

        items = (
            self._installed_items if self._active_tab == _TAB_INSTALLED else self._available_items
        )
        selected_row_key = self._selected_item.get("row_key")
        selected_name = self._selected_item.get("name")
        selected_canonical_name = self._selected_item.get("canonical_name")
        selected_display_name = self._selected_item.get("display_name")

        for item in items:
            if selected_row_key and item.get("row_key") == selected_row_key:
                self._selected_item = item
                return
            if selected_name and item.get("name") == selected_name:
                self._selected_item = item
                return
            if selected_canonical_name and item.get("canonical_name") == selected_canonical_name:
                self._selected_item = item
                return
            if selected_display_name and item.get("display_name") == selected_display_name:
                self._selected_item = item
                return

    async def _fetch_installed(self) -> None:
        items: list[dict[str, t.Any]] = []
        try:
            runtime_info = await self._runtime_client.fetch_runtime_info()
            for cap in runtime_info.capabilities:
                state = "disabled" if not cap.enabled else "enabled"

                source = cap.source or "local"

                items.append(
                    {
                        "row_key": f"{source}:{cap.name}:{cap.binding_id or ''}",
                        "name": cap.name,
                        "display_name": cap.display_name,
                        "canonical_name": cap.canonical_name,
                        "summary": cap.description or "",
                        "description": cap.description or "",
                        "source": source,
                        "provenance": cap.provenance,
                        "state": state,
                        "version": cap.version,
                        "binding_id": cap.binding_id,
                        "author": cap.author,
                        "license": cap.license,
                        "origin": cap.origin,
                        "agents": [
                            {"name": a.name, "description": a.description, "model": a.model}
                            for a in cap.agents
                        ],
                        "components": cap.components,
                        "update_available": cap.update_available,
                        "dependencies": getattr(cap, "dependencies", None),
                        "checks": getattr(cap, "checks", None),
                        "local_path": getattr(cap, "local_path", None),
                        "flags": getattr(cap, "flags", []),
                    }
                )
        except Exception as exc:
            logger.warning("fetch_installed failed | error={}", exc)
            logger.opt(exception=exc).debug("Failed to load installed capabilities")
            # Fall back to local filesystem discovery
            items = await self._discover_local_capabilities()

        logger.debug("fetch_installed | count={}", len(items))
        self._installed_items = sorted(items, key=lambda i: i["name"])

    async def _discover_local_capabilities(self) -> list[dict[str, t.Any]]:
        """Discover locally installed capabilities from the filesystem."""
        from dreadnode.capabilities.capability import (
            Capability,
            read_local_capability_records,
        )
        from dreadnode.capabilities.flags import read_env_overrides
        from dreadnode.storage.storage import Storage

        items: list[dict[str, t.Any]] = []
        try:
            result = await asyncio.to_thread(Capability.discover, host="local")

            local_records = read_local_capability_records(Storage().local_capability_state_path)

            for name, cap in {**result.capabilities, **result.disabled}.items():
                enabled = name not in result.disabled
                agents = cap.agents or []

                flag_defs = cap.flag_defs
                if flag_defs:
                    persisted = local_records.get(name, {}).get("flags", {}) or {}
                    cap.resolve_flags(
                        persisted=persisted if isinstance(persisted, dict) else {},
                        env_overrides=read_env_overrides(name, flag_defs),
                    )
                flags = [
                    {
                        "name": f.name,
                        "description": f.description,
                        "default": f.default,
                        "effective": f.effective,
                        "source": f.source,
                    }
                    for f in cap.resolved_flags
                ]

                items.append(
                    {
                        "row_key": f"local:{name}:",
                        "name": name,
                        "display_name": name,
                        "canonical_name": name,
                        "summary": cap.description or "",
                        "description": cap.description or "",
                        "source": "local",
                        "provenance": None,
                        "state": "enabled" if enabled else "disabled",
                        "version": cap.version,
                        "binding_id": None,
                        "author": cap.manifest.author.get("name") if cap.manifest.author else None,
                        "license": cap.manifest.license,
                        "origin": str(cap.path),
                        "agents": [
                            {
                                "name": getattr(a, "name", "?"),
                                "description": getattr(a, "description", ""),
                                "model": getattr(a, "model", "inherit"),
                            }
                            for a in agents
                        ],
                        "components": {
                            "agents": len(agents),
                            "skills": sum(
                                1
                                for h in cap.component_health
                                if h.get("kind") == "skill" and h.get("status") == "ok"
                            ),
                            "mcp_servers": len(cap.mcp_server_defs),
                        },
                        "update_available": None,
                        "local_path": str(cap.path),
                        "flags": flags,
                    }
                )
        except Exception as exc:
            logger.opt(exception=exc).debug("Failed to discover local capabilities")

        return items

    async def _fetch_available(self) -> None:
        org_items: list[dict[str, t.Any]] = []
        public_items: list[dict[str, t.Any]] = []

        if self._has_platform:
            assert self._api is not None
            assert self._org is not None

            try:
                all_caps = await asyncio.to_thread(
                    self._api.list_capabilities, self._org, include_public=True
                )
                for cap in all_caps.get("capabilities", []):
                    name = cap.get("name", "?")
                    is_org_owned = not cap.get("is_public", False) or name.startswith(
                        f"{self._org}/"
                    )
                    source = "org" if is_org_owned else "public"
                    target = org_items if is_org_owned else public_items
                    target.append(
                        {
                            "row_key": f"{source}:{name}",
                            "name": name,
                            "summary": cap.get("description") or cap.get("summary") or "",
                            "description": cap.get("description") or cap.get("summary") or "",
                            "source": source,
                            "version": cap.get("version", ""),
                            # API field is ``author_name`` (string); fall back to
                            # ``author`` for forward-compat with shapes that
                            # nested it as a dict.
                            "author": cap.get("author_name") or cap.get("author"),
                            "versions": cap.get("versions", []),
                            "component_counts": cap.get("component_counts", {}),
                            "component_details": cap.get("component_details", []),
                        }
                    )
                logger.debug(
                    "fetch_available | org={} public={}", len(org_items), len(public_items)
                )
            except Exception as exc:
                logger.warning("fetch_available failed | error={}", exc)
                logger.opt(exception=exc).debug("Failed to load capabilities")

        items = _merge_available_sources(org_items, public_items)

        # Drop anything the user already has — the Installed tab owns
        # "what's running and is there an update?" (it carries its own
        # Update column), so duplicating those rows here just clutters
        # the catalog. Match by any name an installed entry exposes
        # (bare ``name``, canonical ``org/name``, or ``display_name``)
        # since available items come back in either form.
        installed_keys: set[str] = set()
        for inst in self._installed_items:
            for key in (inst.get("name"), inst.get("canonical_name"), inst.get("display_name")):
                if isinstance(key, str) and key:
                    installed_keys.add(key)

        installable = [
            dict(item, install_state="install", binding_id=None)
            for item in items
            if item.get("name") not in installed_keys
        ]

        self._available_items = sorted(installable, key=lambda i: i["name"])

    # ── Feedback ──────────────────────────────────────────────────────────

    def _show_action_notice(self, name: str, verb: str) -> None:
        """Show immediate feedback for an in-progress action.

        Called synchronously on the UI thread before dispatching the worker.
        """
        label = _notification_name(name)
        self._pending_action_name = name
        self._pending_action_label = f"{verb}..."
        try:
            from dreadnode.app.tui.app import DreadnodeTextualApp

            app = self.app
        except Exception:
            app = None

        if isinstance(app, DreadnodeTextualApp):
            self._pending_action_notification = app._notify_tracked(
                f"{verb} {label}...",
                severity="information",
                timeout=10,
            )
        else:
            self._pending_action_notification = None
            self.notify(f"{verb} {label}...", severity="information", timeout=10)
        self._render_current_view()

    async def _reload_capabilities_with_feedback(self) -> None:
        try:
            from dreadnode.app.tui.app import DreadnodeTextualApp

            app = self.app
        except Exception:
            app = None

        if isinstance(app, DreadnodeTextualApp):
            runtime_info = await app._command_dispatcher.reload_capabilities_with_feedback(
                client=self._runtime_client
            )
            await app._capabilities_manager.apply_runtime_info(runtime_info, refresh_skills=True)
            return

        self.notify("Reloading...", severity="information", timeout=10)
        await self._runtime_client.reload_capabilities()

    def _clear_pending_action(self, name: str | None = None) -> None:
        """Clear the tracked pending action when it matches the given capability."""
        if name is not None and self._pending_action_name not in {None, name}:
            return
        had_pending = (
            self._pending_action_name is not None or self._pending_action_label is not None
        )
        notification = self._pending_action_notification
        self._pending_action_name = None
        self._pending_action_label = None
        self._pending_action_notification = None
        if notification is not None:
            try:
                from dreadnode.app.tui.app import DreadnodeTextualApp

                app = self.app
            except Exception:
                app = None
            if isinstance(app, DreadnodeTextualApp):
                app._dismiss_notification(notification)
        if had_pending:
            self._render_current_view()

    # ── Action execution ─────────────────────────────────────────────────

    def _execute_action(self, action_id: str) -> None:
        if self._selected_item is None or action_id == "noop":
            return

        item = self._selected_item
        if action_id == "toggle":
            if item.get("source") == "runtime" and item.get("binding_id"):
                new_enabled = item.get("state") != "enabled"
                self._show_action_notice(item["name"], "Enabling" if new_enabled else "Disabling")
                self._do_toggle(item["binding_id"], enabled=new_enabled)
            elif item.get("source") in ("local", "package"):
                new_enabled = item.get("state") != "enabled"
                self._show_action_notice(item["name"], "Enabling" if new_enabled else "Disabling")
                self._do_toggle_local(item["name"], enabled=new_enabled)
        elif action_id == "remove":
            if item.get("binding_id"):
                self._show_action_notice(item["name"], "Removing")
                self._do_remove(item["binding_id"], item["name"])
        elif action_id == "remove_local":
            self._show_action_notice(item["name"], "Removing")
            self._do_remove_local(item["name"])
        elif action_id == "browse_files":
            local_path = item.get("local_path")
            if not isinstance(local_path, str) or not local_path.strip():
                self.notify("Capability files are unavailable for this item", severity="warning")
                return
            capability_root = Path(local_path).expanduser()
            if not capability_root.is_dir():
                self.notify(
                    f"Capability files not found: {capability_root}",
                    severity="warning",
                )
                return
            from dreadnode.app.tui.screens.capability_docs import CapabilityDocsScreen

            self.app.push_screen(
                CapabilityDocsScreen(
                    capability_name=_display_name(item),
                    root=capability_root,
                )
            )
        elif action_id == "install":
            self._show_action_notice(item["name"], "Installing")
            self.call_after_refresh(
                self._do_install,
                item["name"],
                item.get("version"),
                source=t.cast("str | None", item.get("source")),
            )
        elif action_id == "overwrite_install":
            self._show_action_notice(item["name"], "Installing")
            self.call_after_refresh(
                self._do_install,
                item["name"],
                item.get("version"),
                source=t.cast("str | None", item.get("source")),
                overwrite=True,
            )
        elif action_id == "cancel_overwrite":
            self._pending_local_overwrite_key = None
            self._action_cursor = 0
            self._render_current_view()
        elif action_id == "update" and (binding_id := item.get("binding_id")):
            self._show_action_notice(item["name"], "Updating")
            self.call_after_refresh(
                self._do_update,
                binding_id,
                item["name"],
                item.get("update_available") or item.get("version"),
            )
        elif action_id == "update_local":
            artifact_identity = item.get("canonical_name") or item.get("name")
            update_ver = item.get("update_available") or item.get("version")
            provenance = item.get("provenance") or item.get("source")
            if update_ver and artifact_identity:
                self._show_action_notice(item["name"], "Updating")
                self.call_after_refresh(
                    self._do_update_local,
                    artifact_identity,
                    update_ver,
                    source=provenance,
                )
        elif action_id == "fix":
            message = _build_fix_message(item)
            try:
                from dreadnode.app.tui.app import DreadnodeTextualApp

                app = self.app
            except Exception:
                app = None
            if isinstance(app, DreadnodeTextualApp):
                app._pending_fix_message = message
            self.dismiss()

    # ── Platform operations ──────────────────────────────────────────────

    @work(exclusive=True, group="cap-action")
    async def _do_toggle(self, binding_id: str, *, enabled: bool) -> None:
        label = _notification_name(
            self._selected_item.get("name", "capability")
            if self._selected_item is not None
            else "capability"
        )
        if not (self._api and self._org and self._workspace and self._runtime_id):
            logger.warning("toggle skipped | binding_id={} | reason=no runtime", binding_id)
            self.notify(
                f"Can't {'enable' if enabled else 'disable'} {label}: no runtime selected",
                severity="warning",
            )
            return
        logger.info("toggle start | binding_id={} | enabled={}", binding_id, enabled)
        try:
            await asyncio.to_thread(
                self._api.toggle_runtime_capability,
                self._org,
                self._workspace,
                self._runtime_id,
                binding_id,
                enabled=enabled,
            )
            await self._reload_capabilities_with_feedback()
            self.notify(
                f"{'Enabled' if enabled else 'Disabled'} {label}",
                severity="information",
            )
            logger.info("toggle success | binding_id={} | enabled={}", binding_id, enabled)
        except Exception as exc:
            logger.warning("toggle failed | binding_id={} | error={}", binding_id, exc)
            self.notify(
                f"Failed to {'enable' if enabled else 'disable'} {label}: {exc}",
                severity="error",
            )
        self._load_data()

    @work(exclusive=True, group="cap-action")
    async def _do_install(
        self,
        name: str,
        version: str | None,
        *,
        source: str | None = None,
        overwrite: bool = False,
    ) -> None:
        label = _notification_name(name)
        if not (self._api and self._org):
            logger.warning("install skipped | name={} | reason=not authenticated", name)
            self._clear_pending_action(name)
            self.notify(
                f"Can't install {label}: not authenticated",
                severity="warning",
            )
            return
        if version is None:
            logger.warning("install skipped | name={} | reason=no version", name)
            self._clear_pending_action(name)
            self.notify(
                f"Can't install {label}: version unavailable",
                severity="warning",
            )
            return
        logger.info(
            "install start | name={} | version={} | source={} | overwrite={}",
            name,
            version,
            source,
            overwrite,
        )
        try:
            if self._is_sandbox:
                if not (self._workspace and self._runtime_id):
                    logger.warning("install skipped | name={} | reason=no runtime", name)
                    self._clear_pending_action(name)
                    self.notify(
                        f"Can't install {label}: no runtime selected",
                        severity="warning",
                    )
                    return
                await asyncio.to_thread(
                    self._api.install_runtime_capability,
                    self._org,
                    self._workspace,
                    self._runtime_id,
                    name=name,
                    version=version,
                )
                logger.info(
                    "install success | name={} | version={} | target=sandbox", name, version
                )
                self._show_installed_detail(
                    name=name,
                    installed_name=_notification_name(name),
                    version=version,
                    source="runtime",
                )
                self.notify(f"Installed {label} in this project", severity="information")
            else:
                from dreadnode.storage.storage import Storage

                storage = Storage()
                installer = LocalInstallClient(
                    api=self._api,
                    org=self._org,
                    local_dir=storage.capabilities_path,
                    state_path=storage.local_capability_state_path,
                )
                install_source = source
                if install_source is None:
                    selected_item_source = (
                        self._selected_item.get("source")
                        if self._selected_item is not None
                        and self._selected_item.get("name") == name
                        else None
                    )
                    if isinstance(selected_item_source, str) and selected_item_source:
                        install_source = selected_item_source
                    else:
                        install_source = "public" if "/" in name else "org"
                result = await installer.install(
                    name=name,
                    version=version,
                    source=install_source,
                    overwrite=overwrite,
                )
                self._pending_local_overwrite_key = None
                self._show_installed_detail(
                    name=name,
                    installed_name=result.installed_name,
                    version=version,
                    source="local",
                )
                self.notify(f"Installed {label}", severity="information")
                logger.info("install success | name={} | version={} | target=local", name, version)
            await self._reload_capabilities_with_feedback()
        except FileExistsError:
            self._clear_pending_action(name)
            logger.warning("install conflict | name={} | reason=already exists locally", name)
            if (
                not self._is_sandbox
                and self._selected_item is not None
                and self._selected_item.get("name") == name
            ):
                self._pending_local_overwrite_key = t.cast(
                    "str | None", self._selected_item.get("row_key")
                )
                self.notify(
                    f"{label} is already installed",
                    severity="warning",
                )
                self._action_cursor = 0
                self._render_current_view()
                return
            self.notify(
                f"{label} is already installed",
                severity="warning",
            )
        except Exception as exc:
            self._clear_pending_action(name)
            logger.warning("install failed | name={} | error={}", name, exc)
            self.notify(f"Failed to install {label}: {exc}", severity="error")
        else:
            self._clear_pending_action(name)
        self._load_data()

    @work(exclusive=True, group="cap-action")
    async def _do_update(self, binding_id: str, name: str, version: str | None) -> None:
        label = _notification_name(name)
        if not (self._api and self._org and self._workspace and self._runtime_id):
            logger.warning("update skipped | name={} | reason=no runtime", name)
            self.notify(
                f"Can't update {label}: no runtime selected",
                severity="warning",
            )
            return
        if not version:
            logger.warning("update skipped | name={} | reason=no version", name)
            return
        logger.info("update start | name={} | version={}", name, version)
        try:
            await asyncio.to_thread(
                self._api.update_runtime_capability,
                self._org,
                self._workspace,
                self._runtime_id,
                binding_id,
                version=version,
            )
            await self._reload_capabilities_with_feedback()
            self.notify(
                f"Updated {label} to v{version}",
                severity="information",
            )
            logger.info("update success | name={} | version={}", name, version)
        except Exception as exc:
            logger.warning("update failed | name={} | error={}", name, exc)
            self.notify(f"Failed to update {label}: {exc}", severity="error")
        finally:
            self._clear_pending_action(name)
        self._load_data()

    @work(exclusive=True, group="cap-action")
    async def _do_update_local(self, name: str, version: str, *, source: str | None = None) -> None:
        label = _notification_name(name)
        if source == "local":
            logger.info("update_local skipped | name={} | reason=local-path install", name)
            self._clear_pending_action(name)
            self.notify(
                f"Can't update {label}: this is a local-path install. "
                f"Reinstall from path with `dreadnode capability install <path> --force`.",
                severity="warning",
            )
            return
        if not (self._api and self._org):
            logger.warning("update_local skipped | name={} | reason=not authenticated", name)
            self._clear_pending_action(name)
            self.notify(
                f"Can't update {label}: not authenticated",
                severity="warning",
            )
            return
        logger.info("update_local start | name={} | version={}", name, version)
        try:
            from dreadnode.storage.storage import Storage

            storage = Storage()
            installer = LocalInstallClient(
                api=self._api,
                org=self._org,
                local_dir=storage.capabilities_path,
                state_path=storage.local_capability_state_path,
            )

            install_source = source or "org"
            await installer.install(
                name=name,
                version=version,
                source=install_source,
                overwrite=True,
            )

            self.notify(
                f"Updated {label} to v{version}",
                severity="information",
            )
            logger.info("update_local success | name={} | version={}", name, version)
            await self._reload_capabilities_with_feedback()
        except Exception as exc:
            logger.warning("update_local failed | name={} | error={}", name, exc)
            self.notify(f"Failed to update {label}: {exc}", severity="error")
        finally:
            self._clear_pending_action(name)
        self._load_data()

    @work(exclusive=True, group="cap-action")
    async def _do_toggle_local(self, name: str, *, enabled: bool) -> None:
        from dreadnode.capabilities.capability import (
            read_local_capability_state,
            write_local_capability_state,
        )
        from dreadnode.storage.storage import Storage

        label = _notification_name(name)
        logger.info("toggle_local | name={} | enabled={}", name, enabled)
        try:
            state_path = Storage().local_capability_state_path
            state = read_local_capability_state(state_path)
            state[name] = enabled
            write_local_capability_state(state_path, state)
            if self._selected_item is not None and self._selected_item.get("name") == name:
                self._selected_item = {
                    **self._selected_item,
                    "state": "enabled" if enabled else "disabled",
                }

            await self._reload_capabilities_with_feedback()
            self.notify(
                f"{'Enabled' if enabled else 'Disabled'} {label}",
                severity="information",
            )
        except Exception as exc:
            logger.warning("toggle_local failed | name={} | error={}", name, exc)
            self.notify(
                f"Failed to {'enable' if enabled else 'disable'} {label}: {exc}",
                severity="error",
            )
        finally:
            self._clear_pending_action(name)
        self._load_data()

    @work(exclusive=True, group="cap-action")
    async def _do_toggle_flag(
        self, binding_id: str, cap_name: str, flag_name: str, *, value: bool
    ) -> None:
        label = _notification_name(cap_name)
        if not (self._api and self._org and self._workspace and self._runtime_id):
            logger.warning(
                "toggle_flag skipped | cap={} flag={} | reason=no runtime", cap_name, flag_name
            )
            self.notify("Can't toggle flag: no runtime selected", severity="warning")
            return
        logger.info("toggle_flag | cap={} | flag={} | value={}", cap_name, flag_name, value)
        try:
            await asyncio.to_thread(
                self._api.set_runtime_capability_flags,
                self._org,
                self._workspace,
                self._runtime_id,
                binding_id,
                flags={flag_name: value},
            )
            await self._reload_capabilities_with_feedback()
            verb = "Enabled" if value else "Disabled"
            self.notify(f"{verb} flag '{flag_name}' on {label}", severity="information")
        except Exception as exc:
            logger.warning(
                "toggle_flag failed | cap={} flag={} | error={}", cap_name, flag_name, exc
            )
            self.notify(f"Failed to toggle flag '{flag_name}': {exc}", severity="error")
        finally:
            self._clear_pending_action(cap_name)
        self._load_data()

    @work(exclusive=True, group="cap-action")
    async def _do_toggle_flag_local(self, cap_name: str, flag_name: str, *, value: bool) -> None:
        from dreadnode.capabilities.capability import (
            read_local_capability_records,
            write_local_capability_records,
        )
        from dreadnode.storage.storage import Storage

        label = _notification_name(cap_name)
        logger.info("toggle_flag_local | cap={} | flag={} | value={}", cap_name, flag_name, value)
        try:
            state_path = Storage().local_capability_state_path
            records = read_local_capability_records(state_path)
            record = records.get(cap_name, {})
            flags = record.get("flags", {})
            if not isinstance(flags, dict):
                flags = {}
            flags[flag_name] = value
            record["flags"] = flags
            records[cap_name] = record
            write_local_capability_records(state_path, records)

            await self._reload_capabilities_with_feedback()
            verb = "Enabled" if value else "Disabled"
            self.notify(f"{verb} flag '{flag_name}' on {label}", severity="information")
        except Exception as exc:
            logger.warning(
                "toggle_flag_local failed | cap={} flag={} | error={}", cap_name, flag_name, exc
            )
            self.notify(f"Failed to toggle flag '{flag_name}': {exc}", severity="error")
        finally:
            self._clear_pending_action(cap_name)
        self._load_data()

    @work(exclusive=True, group="cap-action")
    async def _do_remove_local(self, name: str) -> None:
        from dreadnode.capabilities.sync import uninstall_local
        from dreadnode.storage.storage import Storage

        label = _notification_name(name)
        logger.info("uninstall_local start | name={}", name)
        try:
            storage = Storage()
            result = await asyncio.to_thread(
                uninstall_local,
                name=name,
                local_dir=storage.capabilities_path,
                state_path=storage.local_capability_state_path,
            )

            await self._reload_capabilities_with_feedback()
            logger.info(
                "uninstall_local success | name={} | symlink={} | disk={} | state={}",
                name,
                result.was_symlink,
                result.removed_disk,
                result.removed_state,
            )
            self.notify(f"Removed {label}", severity="information")
            self._back_to_list()
        except Exception as exc:
            logger.warning("uninstall_local failed | name={} | error={}", name, exc)
            self.notify(f"Failed to remove {label}: {exc}", severity="error")
        finally:
            self._clear_pending_action(name)
        self._load_data()

    @work(exclusive=True, group="cap-action")
    async def _do_remove(self, binding_id: str, name: str) -> None:
        label = _notification_name(name)
        if not (self._api and self._org and self._workspace and self._runtime_id):
            logger.warning("uninstall skipped | binding_id={} | reason=no runtime", binding_id)
            self.notify(
                f"Can't remove {label}: no runtime selected",
                severity="warning",
            )
            return
        logger.info("uninstall start | name={} | binding_id={}", name, binding_id)
        try:
            await asyncio.to_thread(
                self._api.uninstall_runtime_capability,
                self._org,
                self._workspace,
                self._runtime_id,
                binding_id,
            )
            await self._reload_capabilities_with_feedback()
            self.notify(f"Removed {label}", severity="information")
            logger.info("uninstall success | name={} | binding_id={}", name, binding_id)
        except Exception as exc:
            logger.warning("uninstall failed | name={} | error={}", name, exc)
            self.notify(f"Failed to remove {label}: {exc}", severity="error")
        finally:
            self._clear_pending_action(name)
        self._load_data()
