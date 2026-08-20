"""Environments Browser screen -- browse and inspect platform environments."""

from __future__ import annotations

import asyncio
import typing as t
from datetime import datetime

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Static, Tree

from dreadnode.app.tui.screens.base import DreadnodeScreen, handle_search_input_paste
from dreadnode.app.tui.theme import ERROR, FG, FG_FAINTEST, FG_MUTED, FG_SUBTLE

if t.TYPE_CHECKING:
    from textual.app import ComposeResult
    from textual.events import Key, Paste

    from dreadnode.app.api.client import ApiClient


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


def _fmt_visibility(is_public: bool | None) -> str:
    return "public" if is_public else "private"


def _fmt_template_status(status: str | None) -> str:
    return status or "n/a"


def _fmt_tags(tags: t.Any) -> str:
    if isinstance(tags, list):
        cleaned = [str(tag) for tag in tags if tag]
        return ", ".join(cleaned) if cleaned else "n/a"
    if isinstance(tags, str) and tags.strip():
        return tags
    return "n/a"


def _fmt_file_size(size: t.Any) -> str:
    if size is None:
        return "n/a"
    if isinstance(size, str):
        try:
            size = float(size)
        except ValueError:
            return str(size)
    if not isinstance(size, (int, float)):
        return "n/a"
    if size < 1024:
        return f"{int(size)} B"
    if size < 1024**2:
        return f"{size / 1024:.1f} KB"
    if size < 1024**3:
        return f"{size / 1024**2:.1f} MB"
    return f"{size / 1024**3:.1f} GB"


def _parse_environment_search(query: str) -> tuple[str, dict[str, str]]:
    """Split free text from lightweight `key:value` environment filters."""
    text_terms: list[str] = []
    filters: dict[str, str] = {}

    for token in query.split():
        if ":" not in token:
            text_terms.append(token)
            continue
        key, value = token.split(":", 1)
        key = key.strip().lower()
        value = value.strip().lower()
        if key in {"visibility", "category", "difficulty", "template", "author", "tag"} and value:
            filters[key] = value
        else:
            text_terms.append(token)

    return (" ".join(text_terms).strip().lower(), filters)


def _filter_environments(
    environments: list[dict[str, t.Any]],
    query: str,
) -> list[dict[str, t.Any]]:
    """Filter environments by free text and simple structured filters."""
    if not query:
        return environments

    text_query, filters = _parse_environment_search(query)
    results: list[dict[str, t.Any]] = []

    for environment in environments:
        raw = environment.get("raw")
        raw_dict = raw if isinstance(raw, dict) else {}
        author = str(raw_dict.get("author_name", "")).lower()
        tags = _fmt_tags(raw_dict.get("tags")).lower()
        visibility = str(environment.get("visibility", "")).lower()
        category = str(environment.get("category", "")).lower()
        difficulty = str(environment.get("difficulty", "")).lower()
        template_status = str(environment.get("template_status", "")).lower()

        if filters.get("visibility") and visibility != filters["visibility"]:
            continue
        if filters.get("category") and filters["category"] not in category:
            continue
        if filters.get("difficulty") and filters["difficulty"] not in difficulty:
            continue
        if filters.get("template") and filters["template"] not in template_status:
            continue
        if filters.get("author") and filters["author"] not in author:
            continue
        if filters.get("tag") and filters["tag"] not in tags:
            continue

        if text_query:
            haystack = " ".join(
                part
                for part in (
                    str(environment.get("name", "")).lower(),
                    str(environment.get("version", "")).lower(),
                    category,
                    difficulty,
                    visibility,
                    template_status,
                    author,
                    tags,
                )
                if part
            )
            if text_query not in haystack:
                continue

        results.append(environment)

    return results


class EnvironmentScreen(DreadnodeScreen):
    """Browser for environments (legacy tasks)."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("down", "cursor_down", show=False),
        Binding("up", "cursor_up", show=False),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("r", "refresh_environments", "Refresh", show=True),
        Binding("d", "show_readme", "README", show=False),
        Binding("n", "next_page", "Next", show=True),
        Binding("p", "prev_page", "Prev", show=True),
    ]

    def __init__(
        self,
        api: ApiClient,
        org: str,
        workspace: str | None = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._api = api
        self._org = org
        self._workspace = workspace
        self._environments: list[dict[str, t.Any]] = []
        self._page = 1
        self._total_pages = 1
        self._has_next = False
        self._has_previous = False
        self._total = 0
        self._limit = 50
        self._search_query = ""
        self._visible_environments: list[dict[str, t.Any]] = []
        self._cursor = 0

    _SUBTITLE = f"\n[{FG_FAINTEST}] Manage environment configurations[/]"

    def compose_content(self) -> ComposeResult:
        yield Static(
            f"[bold {FG}] Environments[/]{self._SUBTITLE}",
            id="environments-title",
        )
        yield Static(id="environments-search")
        with Horizontal(id="environments-body"):
            with Vertical(id="environments-left"):
                yield DataTable(id="environments-table")
                yield Static("", id="environments-pagination")
            with Vertical(id="environments-right"):
                yield Tree("Detail", id="environments-detail")

    def on_mount(self) -> None:
        super().on_mount()
        table = self.query_one("#environments-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns(
            "Name",
            "Version",
            "Source",
            "Difficulty",
            "Visibility",
            "Template",
            "Created",
        )
        self._load_environments(self._page)

    def on_key(self, event: Key) -> None:
        key = event.key

        if key.startswith("ctrl+") or (key.startswith("f") and key[1:].isdigit()):
            return

        if key == "escape" and self._search_query:
            self._search_query = ""
            self._cursor = 0
            self._render_table()
            event.prevent_default()
            event.stop()
            return

        if key == "backspace" and self._search_query:
            self._search_query = self._search_query[:-1]
            self._cursor = 0
            self._render_table()
            event.prevent_default()
            event.stop()
            return

        if event.character and event.character.isprintable() and len(event.character) == 1:
            if not self._search_query and key in {"r", "n", "p", "j", "k", "d"}:
                return
            self._search_query += event.character
            self._cursor = 0
            self._render_table()
            event.prevent_default()
            event.stop()

    def on_paste(self, event: Paste) -> None:
        """Append bracketed-paste text to the search query."""
        result = handle_search_input_paste(self._search_query, text=event.text)
        if not result.handled:
            return
        self._search_query = result.new_query
        if result.cursor_should_reset:
            self._cursor = 0
        self._render_table()
        event.prevent_default()
        event.stop()

    def action_go_back(self) -> None:
        self.dismiss()

    def action_cursor_down(self) -> None:
        self.query_one("#environments-table", DataTable).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one("#environments-table", DataTable).action_cursor_up()

    def action_refresh_environments(self) -> None:
        self._load_environments(self._page)

    def action_show_readme(self) -> None:
        """Open the remote README for the focused task/environment."""
        if not self._visible_environments:
            return
        if not (0 <= self._cursor < len(self._visible_environments)):
            return
        env = self._visible_environments[self._cursor]
        name = env.get("name")
        if not isinstance(name, str) or not name:
            return

        api = self._api
        org = self._org

        async def _fetch() -> dict[str, t.Any]:
            return await asyncio.to_thread(api.get_task_readme, org, name)

        # Local import keeps screens that don't need ReadmeScreen lighter.
        from dreadnode.app.tui.screens.readme import ReadmeScreen

        self.app.push_screen(
            ReadmeScreen(
                title="Task README",
                subject=name,
                fetcher=_fetch,
                empty_message="No README ships with this task archive.",
            )
        )

    def action_next_page(self) -> None:
        if not self._has_next:
            return
        self._load_environments(self._page + 1)

    def action_prev_page(self) -> None:
        if not self._has_previous:
            return
        self._load_environments(self._page - 1)

    def _flash_title(self, message: str = "", colour: str = FG_MUTED) -> None:
        suffix = f"  [{colour}]{message}[/]" if message else ""
        self.query_one("#environments-title", Static).update(
            f"[bold {FG}] Environments[/]{suffix}{self._SUBTITLE}"
        )

    def _update_pagination(self) -> None:
        if self._search_query:
            loaded = len(self._environments)
            visible = len(self._visible_environments)
            label = (
                f"Page {self._page}/{self._total_pages} \u00b7 "
                f"showing {visible}/{loaded} loaded \u00b7 "
                f"{self._total} total"
            )
        else:
            label = (
                f"Page {self._page}/{self._total_pages} \u00b7 "
                f"{self._total} environment{'s' if self._total != 1 else ''}"
            )
        self.query_one("#environments-pagination", Static).update(label)

    def _render_search(self) -> None:
        text = ""
        if self._search_query:
            text = f" ⌕ {self._search_query}▁"
        else:
            text = (
                " ⌕ Search…  filters: visibility:public  category:web  "
                "difficulty:easy  template:ready  author:acme  tag:linux"
            )
        if self._visible_environments:
            text += f"  {self._cursor + 1}/{len(self._visible_environments)}"
        elif self._search_query:
            text += "  no matches"
        self.query_one("#environments-search", Static).update(text)

    def _render_table(self) -> None:
        table = self.query_one("#environments-table", DataTable)
        self._visible_environments = _filter_environments(self._environments, self._search_query)
        self._cursor = min(self._cursor, max(0, len(self._visible_environments) - 1))
        self._render_search()
        self._update_pagination()
        table.clear()

        if not self._visible_environments:
            detail = self.query_one("#environments-detail", Tree)
            detail.clear()
            if self._search_query:
                detail.root.set_label("[dim]No environments match the current search[/]")
            else:
                detail.root.set_label("[dim]No environment selected[/]")
            return

        for env in self._visible_environments:
            table.add_row(
                str(env.get("name", "?")),
                str(env.get("version", "-")),
                str(env.get("source", "-")),
                str(env.get("difficulty", "-")),
                str(env.get("visibility", "-")),
                str(env.get("template_status", "-")),
                str(env.get("created", "-")),
                key=str(env.get("row_key")),
            )

        table.move_cursor(row=self._cursor, column=0, animate=False, scroll=True)
        self._show_environment_detail(self._visible_environments[self._cursor])

    @work(exclusive=True, group="environments")
    async def _load_environments(self, page: int) -> None:
        if not self.is_mounted:
            return
        table = self.query_one("#environments-table", DataTable)
        table.clear()
        self._flash_title("\u2026", FG_FAINTEST)

        try:
            tasks_data = await asyncio.to_thread(
                self._api.list_tasks,
                self._org,
                page=page,
                limit=self._limit,
            )
        except Exception as exc:
            if not self.is_mounted:
                return
            self._flash_title(f"Error: {exc}", ERROR)
            return

        if not self.is_mounted:
            return

        tasks = tasks_data.get("tasks", [])
        self._page = int(tasks_data.get("page", page) or page)
        self._total = int(tasks_data.get("total", len(tasks)) or len(tasks))
        total_pages_raw = tasks_data.get("total_pages")
        total_pages = None
        if isinstance(total_pages_raw, int):
            total_pages = total_pages_raw
        elif isinstance(total_pages_raw, str) and total_pages_raw.isdigit():
            total_pages = int(total_pages_raw)
        if total_pages is None or total_pages < 1:
            total_pages = max(1, (self._total + self._limit - 1) // self._limit)
        self._total_pages = total_pages
        self._has_next = bool(tasks_data.get("has_next", False))
        self._has_previous = bool(tasks_data.get("has_previous", False))

        self._environments = self._from_tasks(tasks)
        self._cursor = 0
        self._render_search()

        if not self._environments:
            self._visible_environments = []
            self._update_pagination()
            self._flash_title()
            self._clear_detail()
            return

        self._flash_title(str(self._total))
        self._render_table()

    def _from_tasks(
        self,
        tasks: list[dict[str, t.Any]],
    ) -> list[dict[str, t.Any]]:
        items: list[dict[str, t.Any]] = []
        for task in tasks:
            created_at = task.get("created_at")
            template_status = _fmt_template_status(task.get("template_status"))
            name = task.get("name", "?")
            items.append(
                {
                    "row_key": name,
                    "name": name,
                    "version": task.get("version", "-"),
                    "source": task.get("source") or "-",
                    "difficulty": task.get("difficulty") or "-",
                    "visibility": _fmt_visibility(task.get("is_public")),
                    "template_status": template_status,
                    "created": _fmt_timestamp(created_at),
                    "raw": task,
                }
            )
        return items

    @on(DataTable.RowHighlighted, "#environments-table")
    def _on_environment_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.row_key is None:
            return
        row_key = str(event.row_key.value)
        for index, env in enumerate(self._visible_environments):
            if str(env.get("row_key")) == row_key:
                self._cursor = index
                self._show_environment_detail(env)
                break

    def _clear_detail(self) -> None:
        detail = self.query_one("#environments-detail", Tree)
        detail.clear()
        detail.root.set_label("[dim]No environment selected[/]")

    def _show_environment_detail(self, env: dict[str, t.Any]) -> None:
        detail = self.query_one("#environments-detail", Tree)
        detail.clear()

        detail.root.set_label(f"[bold]Environment: {env.get('name', 'unknown')}[/]")

        raw = env.get("raw", {})
        info = detail.root.add("Info", expand=True)
        info.add_leaf(f"Name: [{FG}]{env.get('name', 'n/a')}[/]")
        info.add_leaf(f"Version: [{FG}]{env.get('version', 'n/a')}[/]")
        info.add_leaf(f"Source: [{FG_SUBTLE}]{env.get('source', 'n/a')}[/]")
        info.add_leaf(f"Difficulty: [{FG_SUBTLE}]{env.get('difficulty', 'n/a')}[/]")
        info.add_leaf(f"Visibility: [{FG_SUBTLE}]{env.get('visibility', 'n/a')}[/]")

        metadata = detail.root.add("Metadata", expand=True)
        if isinstance(raw, dict):
            author = raw.get("author") or "n/a"
            tags = _fmt_tags(raw.get("tags"))
            template_status = _fmt_template_status(raw.get("template_status"))
            file_size = _fmt_file_size(
                raw.get("file_size_bytes") or raw.get("file_size") or raw.get("size_bytes")
            )
            created = _fmt_timestamp(raw.get("created_at"))

            metadata.add_leaf(f"Author: [{FG_SUBTLE}]{author}[/]")
            metadata.add_leaf(f"Tags: [{FG_SUBTLE}]{tags}[/]")
            metadata.add_leaf(f"Template Status: [{FG_SUBTLE}]{template_status}[/]")
            metadata.add_leaf(f"File Size: [{FG_SUBTLE}]{file_size}[/]")
            metadata.add_leaf(f"Created: [{FG_SUBTLE}]{created}[/]")

        detail.root.expand()

    def _selected_environment(self) -> dict[str, t.Any] | None:
        table = self.query_one("#environments-table", DataTable)
        if table.cursor_row is None:
            return None
        try:
            row_key = table.coordinate_to_cell_key((table.cursor_row, 0)).row_key
        except Exception:
            return None
        if row_key is None:
            return None
        key = str(row_key.value)
        for env in self._visible_environments:
            if str(env.get("row_key")) == key:
                return env
        return None
