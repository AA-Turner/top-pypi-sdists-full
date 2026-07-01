"""Secrets screen -- inspect configured user secrets and provider presets."""

from __future__ import annotations

import asyncio
import typing as t

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import DataTable, Static, Tree

from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.theme import ERROR, FG, FG_FAINTEST, FG_MUTED, FG_SUBTLE, SUCCESS, WARNING

if t.TYPE_CHECKING:
    from textual.app import ComposeResult

    from dreadnode.app.api.client import ApiClient


def _state_colour(configured: bool) -> str:
    return SUCCESS if configured else WARNING


class SecretsScreen(DreadnodeScreen):
    """Configured secrets and provider presets."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "go_back", "Back", show=True),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("r", "refresh_secrets", "Refresh", show=True),
    ]

    def __init__(self, api: ApiClient, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)
        self._api = api
        self._items: list[dict[str, t.Any]] = []

    _SUBTITLE = f"\n[{FG_FAINTEST}] View configured secrets and provider presets[/]"

    def compose_content(self) -> ComposeResult:
        yield Static(f"[bold {FG}] Secrets[/]{self._SUBTITLE}", id="secrets-title")
        with Horizontal(id="secrets-body"):
            with Vertical(id="secrets-left"):
                yield DataTable(id="secrets-table")
            with Vertical(id="secrets-right"):
                yield Tree("Detail", id="secrets-detail")

    def on_mount(self) -> None:
        super().on_mount()
        table = self.query_one("#secrets-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("Kind", "Name", "Provider", "Status")
        self._load_secrets()

    def action_go_back(self) -> None:
        self.dismiss()

    def action_cursor_down(self) -> None:
        self.query_one("#secrets-table", DataTable).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one("#secrets-table", DataTable).action_cursor_up()

    def action_refresh_secrets(self) -> None:
        self._load_secrets()

    def _flash_title(self, message: str = "", colour: str = FG_MUTED) -> None:
        suffix = f"  [{colour}]{message}[/]" if message else ""
        self.query_one("#secrets-title", Static).update(
            f"[bold {FG}] Secrets[/]{suffix}{self._SUBTITLE}"
        )

    @work(exclusive=True, group="secrets")
    async def _load_secrets(self) -> None:
        table = self.query_one("#secrets-table", DataTable)
        table.clear()
        self._flash_title("\u2026", FG_FAINTEST)
        try:
            secrets, presets = await asyncio.gather(
                asyncio.to_thread(self._api.list_secrets),
                asyncio.to_thread(self._api.get_secret_presets),
            )
        except Exception as exc:
            self._flash_title(f"Error: {exc}", ERROR)
            return

        items: list[dict[str, t.Any]] = []
        for secret in secrets.secrets:
            items.append(
                {
                    "row_key": f"secret:{secret.id}",
                    "kind": "secret",
                    "name": secret.name,
                    "provider": secret.provider or "-",
                    "status": "configured",
                    "raw": secret,
                }
            )
        for preset in presets.presets:
            items.append(
                {
                    "row_key": f"preset:{preset.provider}",
                    "kind": "preset",
                    "name": preset.provider,
                    "provider": preset.env_var_name,
                    "status": "configured" if preset.configured else "missing",
                    "raw": preset,
                }
            )

        self._items = items
        if not self._items:
            self._flash_title()
            self._clear_detail()
            return

        for item in self._items:
            configured = item["status"] == "configured"
            colour = _state_colour(configured)
            table.add_row(
                item["kind"],
                item["name"],
                item["provider"],
                f"[{colour}]{item['status']}[/]",
                key=item["row_key"],
            )

        self._flash_title(str(len(self._items)))
        self._show_item_detail(self._items[0])

    @on(DataTable.RowHighlighted, "#secrets-table")
    def _on_item_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.row_key is None:
            return
        row_key = str(event.row_key.value)
        for item in self._items:
            if item["row_key"] == row_key:
                self._show_item_detail(item)
                break

    def _clear_detail(self) -> None:
        detail = self.query_one("#secrets-detail", Tree)
        detail.clear()
        detail.root.set_label("[dim]No secret selected[/]")

    def _show_item_detail(self, item: dict[str, t.Any]) -> None:
        detail = self.query_one("#secrets-detail", Tree)
        detail.clear()
        detail.root.set_label(f"[bold]{item['kind'].title()}: {item['name']}[/]")
        raw = item["raw"]

        info = detail.root.add("Info", expand=True)
        info.add_leaf(f"Name: [{FG}]{item['name']}[/]")
        info.add_leaf(f"Provider: [{FG_SUBTLE}]{item['provider']}[/]")
        info.add_leaf(
            f"Status: [{_state_colour(item['status'] == 'configured')}]{item['status']}[/]"
        )

        if item["kind"] == "secret":
            info.add_leaf(f"Masked Value: [{FG_SUBTLE}]{raw.masked_value}[/]")
            info.add_leaf(f"Created: [{FG_SUBTLE}]{raw.created_at}[/]")
            info.add_leaf(f"Updated: [{FG_SUBTLE}]{raw.updated_at}[/]")
        else:
            info.add_leaf(f"Env Var: [{FG_SUBTLE}]{raw.env_var_name}[/]")

        detail.root.expand()
