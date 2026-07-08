"""Remote README viewer for capabilities and security tasks.

Fetches the README from the platform on entry and renders it with Textual's
``MarkdownViewer``. Used by both the capabilities and environments screens via
their ``r`` key bindings.
"""

from __future__ import annotations

import typing as t

from textual import work
from textual.binding import Binding
from textual.widgets import MarkdownViewer, Static

from dreadnode.app.api.client import NotFoundError
from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.theme import FG, FG_FAINTEST, FG_MUTED

if t.TYPE_CHECKING:
    from textual.app import ComposeResult

# Coroutine that fetches and returns ``{"path": str, "content": str}`` or raises.
ReadmeFetcher = t.Callable[[], t.Awaitable[dict[str, t.Any]]]


class ReadmeScreen(DreadnodeScreen):
    """Generic remote README viewer.

    The screen is decoupled from the source: callers pass in a small async
    fetcher that returns ``{path, content}``. That keeps capability- and
    task-specific URL building out of this class.
    """

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "close", "Close", show=True),
        Binding("q", "close", "Close", show=False),
    ]

    def __init__(
        self,
        *,
        title: str,
        subject: str,
        fetcher: ReadmeFetcher,
        empty_message: str = "No README found in this bundle.",
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._title = title
        self._subject = subject
        self._fetcher = fetcher
        self._empty_message = empty_message

    def compose_content(self) -> ComposeResult:
        subtitle = f"\n[{FG_FAINTEST}] Fetched from the platform[/]"
        yield Static(
            f"[bold {FG}] {self._title}[/]  [{FG_MUTED}]{self._subject}[/]{subtitle}",
            id="readme-screen-title",
        )
        yield Static("", id="readme-screen-path")
        yield MarkdownViewer(
            show_table_of_contents=False,
            open_links=False,
            id="readme-screen-viewer",
        )

    def on_mount(self) -> None:
        super().on_mount()
        viewer = self.query_one("#readme-screen-viewer", MarkdownViewer)
        viewer.focus()
        self._load()

    @work
    async def _load(self) -> None:
        viewer = self.query_one("#readme-screen-viewer", MarkdownViewer)
        path_bar = self.query_one("#readme-screen-path", Static)
        await viewer.document.update("# Loading README…")
        try:
            payload = await self._fetcher()
        except NotFoundError:
            await viewer.document.update(f"# README not available\n\n{self._empty_message}")
            return
        except Exception as exc:
            await viewer.document.update(
                f"# Failed to load README\n\n```\n{exc}\n```",
            )
            return

        content = str(payload.get("content") or "").strip()
        path = str(payload.get("path") or "")
        if not content:
            await viewer.document.update(f"# README is empty\n\n{self._empty_message}")
            return

        await viewer.document.update(content)
        if path:
            path_bar.update(f" [{FG_FAINTEST}]{path}[/]")

    def action_close(self) -> None:
        self.app.pop_screen()
