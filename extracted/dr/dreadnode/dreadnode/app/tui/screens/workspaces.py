"""Workspace & Project browser screen.

Three-view layout following the RuntimeScreen pattern:
  List view:   header -> org-grouped workspace list with cursor
  Detail view: workspace info -> project list with cursor -> actions
  Create view: inline text input for new workspace or project
  Enter: list->detail or execute action
  Esc:   detail->list, create->previous, or dismiss
"""

from __future__ import annotations

import asyncio
import re
import typing as t
from datetime import UTC

from loguru import logger
from rich.text import Text
from textual import work
from textual.containers import VerticalScroll
from textual.widgets import Static

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
    WARNING,
)

if t.TYPE_CHECKING:
    from textual.app import ComposeResult
    from textual.events import Key, Paste
    from textual.timer import Timer

    from dreadnode.app.api.client import ApiClient
    from dreadnode.app.api.models import Organization, Project, Workspace


# ── Data structures ──────────────────────────────────────────────────────────


class _OrgGroup(t.TypedDict):
    org: Organization
    workspaces: list[Workspace]


class SwitchRequest(t.NamedTuple):
    """Returned via screen dismiss to request a context switch."""

    org_key: str
    workspace_key: str
    project_key: str | None


# ── Helpers ──────────────────────────────────────────────────────────────────


def _slugify(name: str) -> str:
    """Convert a display name to a URL-friendly key."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")[:64]


def _relative_time(ts: t.Any) -> str:
    """Human-friendly relative time."""
    from datetime import datetime

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


def _filter_org_groups(groups: list[_OrgGroup], query: str) -> list[_OrgGroup]:
    """Filter org/workspace groups by visible search text and `org:` token."""
    if not query:
        return groups

    org_filter: str | None = None
    text_terms: list[str] = []
    for token in query.split():
        if ":" not in token:
            text_terms.append(token)
            continue
        key, value = token.split(":", 1)
        if key.strip().lower() == "org" and value.strip():
            org_filter = value.strip().lower()
        else:
            text_terms.append(token)

    text_query = " ".join(text_terms).strip().lower()
    filtered: list[_OrgGroup] = []
    for group in groups:
        org = group["org"]
        if org_filter and org_filter not in org.key.lower() and org_filter not in org.name.lower():
            continue
        workspaces: list[Workspace] = []
        for workspace in group["workspaces"]:
            haystack = " ".join(
                part
                for part in (
                    org.key.lower(),
                    org.name.lower(),
                    workspace.key.lower(),
                    workspace.name.lower(),
                    (workspace.description or "").lower(),
                )
                if part
            )
            if text_query and text_query not in haystack:
                continue
            workspaces.append(workspace)
        if workspaces:
            filtered.append({"org": org, "workspaces": workspaces})
    return filtered


# ── Main screen ──────────────────────────────────────────────────────────────


class WorkspaceScreen(DreadnodeScreen):
    """Full-screen workspace & project browser."""

    def __init__(
        self,
        api: ApiClient,
        current_org: str,
        current_workspace: str,
        current_project: str | None = None,
        *,
        start_in_detail: bool = False,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._api = api
        self._current_org = current_org
        self._current_workspace = current_workspace
        self._current_project = current_project
        self._start_in_detail = start_in_detail

        # Data
        self._org_groups: list[_OrgGroup] = []
        self._flat_workspaces: list[tuple[str, Workspace]] = []  # (org_key, workspace)
        self._projects: list[Project] = []
        self._projects_loaded: bool = False
        self._refresh_timer: Timer | None = None

        # View state: "list", "detail", "create_workspace", "create_project"
        self._view: str = "list"
        self._cursor: int = 0
        self._action_cursor: int = 0
        self._search_query: str = ""
        self._visible_flat_workspaces: list[tuple[str, Workspace]] = []
        self._selected_workspace: Workspace | None = None
        self._selected_org_key: str = ""
        self._notice: tuple[str, str] | None = None  # (message, severity)

        # Create-view input state
        self._input_buffer: str = ""
        self._input_label: str = ""
        self._create_org_key: str = ""  # org targeted by workspace creation

    # ── Compose ──────────────────────────────────────────────────────────

    def compose_content(self) -> ComposeResult:
        yield Static(id="ws-header")
        yield Static(id="ws-search")
        with VerticalScroll(id="ws-scroll"):
            yield Static(id="ws-content")
        yield Static(id="ws-hint-bar")

    def on_mount(self) -> None:
        super().on_mount()
        self._render_header()
        self._render_hints()
        self._load_data()
        self._refresh_timer = self.set_interval(30.0, self._load_data)

    def on_unmount(self) -> None:
        if self._refresh_timer is not None:
            self._refresh_timer.stop()
            self._refresh_timer = None

    def on_screen_suspend(self, _event: t.Any) -> None:
        if self._refresh_timer is not None:
            self._refresh_timer.stop()
            self._refresh_timer = None

    def on_screen_resume(self, _event: t.Any) -> None:
        self._load_data()
        if self._refresh_timer is None:
            self._refresh_timer = self.set_interval(30.0, self._load_data)

    # ── Data loading ─────────────────────────────────────────────────────

    @work(exclusive=True, group="ws_load")
    async def _load_data(self) -> None:
        try:
            orgs = await asyncio.to_thread(self._api.list_user_organizations)
        except Exception as exc:
            logger.warning("Failed to load organizations: {}", exc)
            self._org_groups = []
            self._flat_workspaces = []
            self._render_current_view()
            return

        groups: list[_OrgGroup] = []
        flat: list[tuple[str, Workspace]] = []
        for org in orgs:
            try:
                workspaces = await asyncio.to_thread(
                    self._api.list_organization_workspaces, org.key
                )
                # Sort: default first, then alphabetical
                workspaces.sort(key=lambda w: (not w.is_default, w.name.lower()))
                groups.append({"org": org, "workspaces": workspaces})
                for ws in workspaces:
                    flat.append((org.key, ws))
            except Exception as exc:
                logger.warning("Failed to load workspaces for org {}: {}", org.key, exc)

        self._org_groups = groups
        self._flat_workspaces = flat
        self._cursor = min(self._cursor, max(0, len(flat) - 1))

        # One-shot: if requested, jump straight into the current workspace's
        # detail view so the first paint shows projects (no list-view flash).
        if self._start_in_detail and self._current_workspace:
            self._start_in_detail = False
            match_index = next(
                (
                    i
                    for i, (org_key, ws) in enumerate(flat)
                    if ws.key == self._current_workspace
                    and (not self._current_org or org_key == self._current_org)
                ),
                None,
            )
            if match_index is not None:
                # _open_detail() reads from _visible_flat_workspaces, which is
                # normally populated by _render_list_view. Seed it here since
                # we're skipping the list-view render entirely.
                self._visible_flat_workspaces = list(flat)
                self._cursor = match_index
                self._open_detail()
                return
            self._notice = ("Workspace not found, pick another", "warning")

        # If in detail view, refresh projects too
        if self._view == "detail" and self._selected_workspace:
            await self._load_projects()
        else:
            self._render_current_view()

    async def _load_projects(self) -> None:
        if not self._selected_workspace:
            return
        try:
            projects = await asyncio.to_thread(
                self._api.list_projects,
                self._selected_org_key,
                self._selected_workspace.key,
            )
            # Sort: default first, then most recently updated
            default_projects = [p for p in projects if p.is_default]
            other_projects = sorted(
                [p for p in projects if not p.is_default],
                key=lambda p: p.updated_at,
                reverse=True,
            )
            self._projects = default_projects + other_projects
        except Exception as exc:
            logger.warning("Failed to load projects: {}", exc)
            self._projects = []
        self._projects_loaded = True
        self._render_current_view()

    # ── Keyboard handling ────────────────────────────────────────────────

    def on_key(self, event: Key) -> None:
        key = event.key

        # Let control sequences and function keys pass through
        if key.startswith("ctrl+") or (key.startswith("f") and key[1:].isdigit()):
            return

        if self._view in ("create_workspace", "create_project"):
            self._handle_create_key(key, event)
        elif self._view == "detail":
            self._handle_detail_key(key)
        else:
            self._handle_list_key(key)

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

    def _handle_list_key(self, key: str) -> None:
        if key in ("up", "k"):
            if self._visible_flat_workspaces:
                self._cursor = max(0, self._cursor - 1)
                self._render_current_view()
            return
        if key in ("down", "j"):
            if self._visible_flat_workspaces:
                self._cursor = min(len(self._visible_flat_workspaces) - 1, self._cursor + 1)
                self._render_current_view()
            return
        if key == "enter":
            self._open_detail()
            return
        if key == "n":
            self._start_create_workspace()
            return
        if key == "r":
            self._load_data()
            return
        if key == "escape":
            if self._search_query:
                self._search_query = ""
                self._cursor = 0
                self._render_current_view()
            else:
                self.dismiss(None)
            return
        # Search-bar typing semantics. Workspaces uses ``key`` as the
        # character because its keyhandler doesn't pass the event through.
        character = key if len(key) == 1 else None
        search_result = handle_search_input_key(self._search_query, key=key, character=character)
        if not search_result.handled or search_result.new_query == self._search_query:
            return
        self._search_query = search_result.new_query
        if search_result.cursor_should_reset:
            self._cursor = 0
        self._render_current_view()

    def _handle_detail_key(self, key: str) -> None:
        # Action list: projects + [New project] + [Back]
        total_items = len(self._projects) + 2  # +1 new project, +1 back
        if key in ("up", "k"):
            self._action_cursor = max(0, self._action_cursor - 1)
            self._render_current_view()
        elif key in ("down", "j"):
            self._action_cursor = min(total_items - 1, self._action_cursor + 1)
            self._render_current_view()
        elif key == "enter":
            if self._action_cursor < len(self._projects):
                self._switch_to_project(self._projects[self._action_cursor])
            elif self._action_cursor == len(self._projects):
                self._start_create_project()
            else:
                self._back_to_list()
        elif key == "n":
            self._start_create_project()
        elif key == "r":
            self._load_data()
        elif key == "escape":
            self._back_to_list()

    def _handle_create_key(self, key: str, event: Key) -> None:
        if key == "escape":
            self._view = "detail" if self._view == "create_project" else "list"
            self._input_buffer = ""
            self._render_current_view()
        elif key == "enter":
            if self._input_buffer.strip():
                if self._view == "create_workspace":
                    self._do_create_workspace()
                else:
                    self._do_create_project()
        elif key == "backspace":
            self._input_buffer = self._input_buffer[:-1]
            self._render_current_view()
        else:
            char = event.character
            if char and len(char) == 1 and (char.isalnum() or char in " -_"):
                self._input_buffer += char
                self._render_current_view()

    # ── Actions ──────────────────────────────────────────────────────────

    def _open_detail(self) -> None:
        if not self._visible_flat_workspaces or self._cursor >= len(self._visible_flat_workspaces):
            return
        org_key, workspace = self._visible_flat_workspaces[self._cursor]
        self._selected_org_key = org_key
        self._selected_workspace = workspace
        self._action_cursor = 0
        self._notice = None
        self._view = "detail"
        self._projects = []
        self._projects_loaded = False
        self._render_current_view()
        self._load_projects_async()

    @work(exclusive=True, group="ws_projects")
    async def _load_projects_async(self) -> None:
        await self._load_projects()

    def _back_to_list(self) -> None:
        self._view = "list"
        self._notice = None
        self._render_current_view()

    def _switch_to_project(self, project: Project) -> None:
        """Request a context switch via screen dismiss."""
        ws = self._selected_workspace
        if not ws:
            return

        # Check if this is already the active context
        if (
            self._selected_org_key == self._current_org
            and ws.key == self._current_workspace
            and project.key == self._current_project
        ):
            self._notice = ("Already active", "info")
            self._render_current_view()
            return

        self.dismiss(
            SwitchRequest(
                org_key=self._selected_org_key,
                workspace_key=ws.key,
                project_key=project.key,
            )
        )

    def _start_create_workspace(self) -> None:
        # Target the org under the cursor, or fall back to current org
        if self._visible_flat_workspaces and 0 <= self._cursor < len(self._visible_flat_workspaces):
            self._create_org_key = self._visible_flat_workspaces[self._cursor][0]
        else:
            self._create_org_key = self._current_org
        self._input_buffer = ""
        self._input_label = "Workspace name"
        self._view = "create_workspace"
        self._render_current_view()

    def _start_create_project(self) -> None:
        self._input_buffer = ""
        self._input_label = "Project name"
        self._view = "create_project"
        self._render_current_view()

    @work(exclusive=True, group="ws_create")
    async def _do_create_workspace(self) -> None:
        name = self._input_buffer.strip()
        key = _slugify(name)
        if not key:
            self._notice = ("Invalid name", "error")
            self._view = "list"
            self._render_current_view()
            return

        org_key = self._create_org_key or self._current_org
        try:
            await asyncio.to_thread(self._api.create_workspace, org_key, name, key)
            self._notice = (f"Created workspace: {key}", "success")
        except Exception as exc:
            self._notice = (str(exc), "error")

        self._input_buffer = ""
        self._view = "list"
        self._load_data()

    @work(exclusive=True, group="ws_create")
    async def _do_create_project(self) -> None:
        name = self._input_buffer.strip()
        key = _slugify(name)
        if not key or not self._selected_workspace:
            self._notice = ("Invalid name", "error")
            self._view = "detail"
            self._render_current_view()
            return

        try:
            await asyncio.to_thread(
                self._api.create_project,
                self._selected_org_key,
                self._selected_workspace.key,
                name,
                key,
            )
            self._notice = (f"Created project: {key}", "success")
        except Exception as exc:
            self._notice = (str(exc), "error")

        self._input_buffer = ""
        self._view = "detail"
        self._load_data()

    # ── Rendering ────────────────────────────────────────────────────────

    def _render_current_view(self) -> None:
        # Workers re-render via this path after awaits. If the screen unmounted
        # mid-flight, query_one would crash with NoMatches — bail before any
        # DOM access.
        if not self.is_mounted:
            return
        self._render_header()
        if self._view in ("create_workspace", "create_project"):
            self._render_create_view()
        elif self._view == "detail":
            self._render_detail_view()
        else:
            self._render_list_view()
        self._render_hints()

    def _render_header(self) -> None:
        self.query_one("#ws-header", Static).update(
            render_screen_header(
                "Workspaces",
                "Browse and switch workspace & project context",
                count=len(self._flat_workspaces) if self._flat_workspaces else None,
            )
        )

    def _render_search(self) -> None:
        self.query_one("#ws-search", Static).update(
            render_search_bar(
                self._search_query,
                cursor=self._cursor,
                visible_count=len(self._visible_flat_workspaces),
                placeholder="Search\u2026  filter: org:acme",
            )
        )

    def _render_hints(self) -> None:
        if self._view in ("create_workspace", "create_project"):
            hints: list[tuple[str, str]] = [("Enter", "create"), ("Esc", "cancel")]
        elif self._view == "detail":
            hints = [("Enter", "switch"), ("N", "new project"), ("Esc", "back")]
        else:
            hints = [
                ("Type", "search"),
                ("Enter", "details"),
                ("N", "new workspace"),
                ("R", "refresh"),
                ("Esc", "close"),
            ]
        self.query_one("#ws-hint-bar", Static).update(render_hint_bar(hints))

    def _render_list_view(self) -> None:
        filtered_groups = _filter_org_groups(self._org_groups, self._search_query)
        self._visible_flat_workspaces = [
            (group["org"].key, workspace)
            for group in filtered_groups
            for workspace in group["workspaces"]
        ]
        self._cursor = min(self._cursor, max(0, len(self._visible_flat_workspaces) - 1))
        self._render_search()
        text = Text()

        # Notice
        if self._notice is not None:
            msg, sev = self._notice
            style = {"error": ERROR, "success": SUCCESS, "warning": WARNING}.get(sev, INFO)
            text.append(f" {msg}\n\n", style=style)
            self._notice = None  # Show once

        if not self._visible_flat_workspaces:
            if self._search_query:
                text.append("  No workspaces match the current search.\n", style=FG_MUTED)
            else:
                text.append("  No workspaces found\n\n", style=FG_MUTED)
                text.append("  Use N to create a new workspace.\n", style=FG_FAINTEST)
            self.query_one("#ws-content", Static).update(text)
            return

        # Build a flat index for cursor tracking
        flat_idx = 0
        for group in filtered_groups:
            org = group["org"]
            workspaces = group["workspaces"]
            if not workspaces:
                continue

            # Org header
            text.append(f"\n  {org.name}", style=f"bold {FG_SUBTLE}")
            if len(self._org_groups) > 1 and org.key != org.name.lower():
                text.append(f" · {org.key}", style=FG_FAINTEST)
            text.append("\n")

            for ws in workspaces:
                is_active = org.key == self._current_org and ws.key == self._current_workspace

                # Cursor
                if flat_idx == self._cursor:
                    text.append(" ❯ ", style=f"bold {ACCENT}")
                else:
                    text.append("   ")

                # Status dot
                if is_active:
                    text.append("● ", style=ACCENT)
                else:
                    text.append("◯ ", style=FG_FAINTEST)

                # Workspace name
                text.append(ws.name, style=FG if not is_active else f"bold {FG}")

                # Key (if meaningfully different from name)
                name_slug = _slugify(ws.name)
                if ws.key != name_slug and ws.key != ws.name.lower():
                    text.append(f" ({ws.key})", style=FG_FAINTEST)

                # Badges
                if ws.is_default:
                    text.append(" · default", style=FG_MUTED)

                if is_active:
                    text.append(" · active", style=ACCENT)

                # Project count
                if ws.project_count is not None:
                    text.append(
                        f" · {ws.project_count} project{'s' if ws.project_count != 1 else ''}",
                        style=FG_FAINTEST,
                    )

                text.append("\n")
                flat_idx += 1

        self.query_one("#ws-content", Static).update(text)

    def _render_detail_view(self) -> None:
        ws = self._selected_workspace
        if not ws:
            return

        text = Text()

        # Notice
        if self._notice is not None:
            msg, sev = self._notice
            style = {"error": ERROR, "success": SUCCESS, "warning": WARNING}.get(sev, INFO)
            text.append(f" {msg}\n\n", style=style)
            self._notice = None

        # Workspace header
        is_active_ws = (
            self._selected_org_key == self._current_org and ws.key == self._current_workspace
        )
        if is_active_ws:
            text.append(" ● ", style=ACCENT)
        else:
            text.append(" ◯ ", style=FG_FAINTEST)
        text.append(ws.name, style=f"bold {FG}")
        text.append(f" · {self._selected_org_key}", style=FG_MUTED)
        if ws.is_default:
            text.append(" · default", style=FG_MUTED)
        if is_active_ws:
            text.append(" · active", style=ACCENT)
        text.append("\n")

        if ws.description:
            text.append(f"   {ws.description}\n", style=FG_FAINTEST)

        text.append("\n")
        text.append("  Projects\n", style=f"bold {FG_SUBTLE}")

        if not self._projects_loaded:
            text.append("  Loading...\n", style=FG_FAINTEST)
        elif not self._projects:
            text.append("  No projects\n", style=FG_MUTED)
        else:
            for i, project in enumerate(self._projects):
                is_active_proj = is_active_ws and project.key == self._current_project

                if i == self._action_cursor:
                    text.append(" ❯ ", style=f"bold {ACCENT}")
                else:
                    text.append("   ")

                if is_active_proj:
                    text.append("● ", style=ACCENT)
                else:
                    text.append("◯ ", style=FG_FAINTEST)

                text.append(project.name, style=FG if not is_active_proj else f"bold {FG}")

                if project.is_default:
                    text.append(" · default", style=FG_MUTED)

                if is_active_proj:
                    text.append(" · active", style=ACCENT)

                # Updated relative time
                rel = _relative_time(project.updated_at)
                if rel:
                    text.append(f" · {rel}", style=FG_FAINTEST)

                text.append("\n")

        text.append("\n")

        # "New project" action
        new_proj_idx = len(self._projects)
        if self._action_cursor == new_proj_idx:
            text.append(" ❯ ", style=f"bold {ACCENT}")
        else:
            text.append("   ")
        text.append("New project\n", style=INFO)

        # "Back" action
        back_idx = new_proj_idx + 1
        if self._action_cursor == back_idx:
            text.append(" ❯ ", style=f"bold {ACCENT}")
        else:
            text.append("   ")
        text.append("Back to workspace list\n", style=FG_SUBTLE)

        self.query_one("#ws-content", Static).update(text)

    def _render_create_view(self) -> None:
        text = Text()

        if self._view == "create_workspace":
            text.append(" New Workspace\n", style=f"bold {FG}")
            org_label = self._create_org_key or self._current_org
            text.append(f"   Organization: {org_label}\n\n", style=FG_MUTED)
        else:
            ws_name = self._selected_workspace.name if self._selected_workspace else "?"
            text.append(" New Project\n", style=f"bold {FG}")
            text.append(f"   Workspace: {ws_name}\n\n", style=FG_MUTED)

        # Input field
        text.append(f"  {self._input_label}: ", style=FG_SUBTLE)
        text.append(self._input_buffer, style=f"bold {FG}")
        text.append("█", style=ACCENT)
        text.append("\n")

        # Preview slug
        slug = _slugify(self._input_buffer)
        if slug:
            text.append(f"  Key: {slug}\n", style=FG_FAINTEST)

        self.query_one("#ws-content", Static).update(text)
