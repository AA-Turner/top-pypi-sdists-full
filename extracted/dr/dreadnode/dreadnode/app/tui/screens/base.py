"""Base screen that includes Zone 4 global nav bar on all pushed screens.

This module also exports the shared rendering helpers used by every
list/detail browser screen (capabilities, runtimes, workspaces, sessions).
The helpers are pure functions returning ``rich.text.Text`` so they're
trivially unit-testable and don't impose a class hierarchy on screens that
all need to vary state-machine details (tabs, multiple views, refresh
timers) in their own ways. See the ``Scaffolding`` section below.
"""

from __future__ import annotations

import typing as t
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from rich.text import Text
from textual.screen import Screen
from textual.widgets import Static

from dreadnode.app.tui.theme import FG, FG_FAINTEST, FG_MUTED
from dreadnode.app.tui.widgets.status_bar import StatusBar

if TYPE_CHECKING:
    from textual.app import ComposeResult

from loguru import logger

_KEY_MAP: dict[str, str] = {
    "escape": "Esc",
}


def _bind_status_bar_to_app(screen: Screen[Any], bar: StatusBar) -> None:
    """Mirror app reactives into a pushed screen's local StatusBar."""
    try:
        from dreadnode.app.tui.app import DreadnodeTextualApp

        app = screen.app
        if not isinstance(app, DreadnodeTextualApp):
            return

        def make_watcher(attr: str):
            def update(_old: object, new: object) -> None:
                setattr(bar, attr, new)

            return update

        for attr in (
            "connection",
            "runtime_connected",
            "connection_status",
            "boot_status",
            "workspace_label",
            "remote_info",
            "update_available",
        ):
            screen.watch(app, attr, make_watcher(attr), init=True)
    except Exception:
        logger.opt(exception=True).debug("Failed to bind StatusBar state")


class _HintBar(Static):
    """Single-line bar showing visible keybindings for the current screen."""

    DEFAULT_CSS = f"""
    _HintBar {{
        height: 1;
        padding: 0 2;
        color: {FG_FAINTEST};
    }}
    """

    def __init__(self, hints: list[tuple[str, str]], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._hints = hints

    def render(self) -> Text:
        t = Text(no_wrap=True, overflow="ellipsis")
        for i, (key, desc) in enumerate(self._hints):
            t.append(key, style=FG_MUTED)
            t.append(f" {desc}", style=FG_FAINTEST)
            if i < len(self._hints) - 1:
                t.append("  ")
        return t


class DreadnodeScreen(Screen[None]):
    """Base class for all pushed screens — automatically includes Zone 4 StatusBar.

    Subclasses override ``compose_content()`` instead of ``compose()``.
    """

    def compose_content(self) -> ComposeResult:
        """Override this in subclasses to yield screen-specific content."""
        return
        yield  # Make it a generator

    def _collect_hints(self) -> list[tuple[str, str]]:
        """Gather (key, description) pairs from show=True bindings."""
        hints: list[tuple[str, str]] = []
        for _key, binding in self._bindings:
            if not binding.show:
                continue
            raw = binding.key
            label = _KEY_MAP.get(raw, raw.capitalize() if len(raw) == 1 else raw.title())
            hints.append((label, binding.description))
        return hints

    def compose(self) -> ComposeResult:
        yield from self.compose_content()
        hints = self._collect_hints()
        if hints:
            yield _HintBar(hints, id="screen-hints")
        yield StatusBar(id="global-status-bar")

    def on_mount(self) -> None:
        """Bind app-level status to the pushed screen's StatusBar."""
        _bind_status_bar_to_app(self, self.query_one("#global-status-bar", StatusBar))


# =============================================================================
# Scaffolding — shared rendering helpers for list/detail browser screens
# =============================================================================
#
# Three of the four full-screen browsers (capabilities, runtimes, workspaces)
# plus the session picker each carried their own copy of the same Rich Text
# scaffolding for the title bar, search bar, and hint row. The shapes are
# nearly identical — only the title strings, search filter hints, and the
# key/action lists differ.
#
# These helpers are pure functions that return Rich Text and never touch
# widget state, so they are trivially unit testable. Each consuming screen
# calls them from its own ``_render_header``, ``_render_search``, and
# ``_render_hints`` methods, which keeps the screens free to vary
# state-machine details (tabs, multiple views, refresh timers) without
# forcing a single megamixin on every screen.

_SEARCH_GLYPH = "\u2315"  # ⌕
_CURSOR_GLYPH = "\u2581"  # ▁


def render_screen_header(
    title: str,
    subtitle: str,
    *,
    count: int | None = None,
    header_extra: Text | None = None,
) -> Text:
    """Render the top-of-screen title bar.

    Layout::

         {title}  {count}  {header_extra}
         {subtitle}

    ``count`` is omitted entirely when ``None`` (e.g. when there are zero
    items and the screen wants to drop the counter). ``header_extra`` is
    appended after the count and is used by capabilities for the tab strip.
    """
    text = Text()
    text.append(f" {title}", style=f"bold {FG}")
    if count is not None:
        text.append(f"  {count}", style=FG_MUTED)
    if header_extra is not None:
        text.append("  ")
        text.append_text(header_extra)
    text.append("\n")
    text.append(f" {subtitle}", style=FG_FAINTEST)
    return text


def render_search_bar(
    query: str,
    *,
    cursor: int,
    visible_count: int,
    placeholder: str = "Search\u2026",
    show_no_match_hint: bool = True,
) -> Text:
    """Render the inline search bar with the ⌕ icon and result counter.

    Layout (one of)::

         ⌕ {query}▁  {cursor+1}/{visible_count}
         ⌕ {placeholder}
         ⌕ {query}  no matches
    """
    text = Text()
    if query:
        text.append(f" {_SEARCH_GLYPH} {query}", style=FG)
        text.append(_CURSOR_GLYPH, style=FG_FAINTEST)
    else:
        text.append(f" {_SEARCH_GLYPH} {placeholder}", style=FG_FAINTEST)
    if visible_count > 0:
        text.append(f"  {cursor + 1}/{visible_count}", style=FG_FAINTEST)
    elif query and show_no_match_hint:
        text.append("  no matches", style=FG_MUTED)
    return text


def render_hint_bar(hints: t.Sequence[tuple[str, str]]) -> Text:
    """Render a row of (key, action) hint pairs separated by two spaces."""
    text = Text()
    text.append(" ")
    for index, (key, action) in enumerate(hints):
        if index > 0:
            text.append("  ", style=FG_FAINTEST)
        text.append(key, style=f"bold {FG_MUTED}")
        text.append(f" {action}", style=FG_FAINTEST)
    return text


@dataclass(frozen=True, slots=True)
class SearchKeyResult:
    """Outcome of dispatching a key event against a search-bar query.

    Returned by :func:`handle_search_input_key`. Callers update their
    in-memory query string from ``new_query`` and reset their list cursor
    when ``cursor_should_reset`` is ``True``.
    """

    handled: bool
    new_query: str
    cursor_should_reset: bool = False


def handle_search_input_key(
    query: str,
    *,
    key: str,
    character: str | None,
) -> SearchKeyResult:
    """Apply standard search-bar typing semantics to a query string.

    - ``backspace`` deletes the trailing character (no-op when empty).
    - A single printable character is appended to the query.
    - Anything else is left for the caller to handle.

    Both mutating cases reset the list cursor to row 0; the empty-backspace
    case does not (so a stray backspace in an empty search box doesn't
    scroll the list to the top).
    """
    if key == "backspace":
        if not query:
            return SearchKeyResult(handled=True, new_query=query)
        return SearchKeyResult(
            handled=True,
            new_query=query[:-1],
            cursor_should_reset=True,
        )
    if character and len(character) == 1 and character.isprintable():
        return SearchKeyResult(
            handled=True,
            new_query=query + character,
            cursor_should_reset=True,
        )
    return SearchKeyResult(handled=False, new_query=query)


def handle_search_input_paste(query: str, *, text: str) -> SearchKeyResult:
    """Append bracketed-paste text to a search query.

    Newlines and tabs collapse to spaces (search queries are space-separated
    tokens) and other control characters are dropped. An all-control paste
    is reported as ``handled=False`` so the caller can ignore it.
    """
    normalized = text.replace("\r\n", " ").replace("\n", " ").replace("\t", " ")
    cleaned = "".join(ch for ch in normalized if ch.isprintable())
    if not cleaned:
        return SearchKeyResult(handled=False, new_query=query)
    return SearchKeyResult(
        handled=True,
        new_query=query + cleaned,
        cursor_should_reset=True,
    )
