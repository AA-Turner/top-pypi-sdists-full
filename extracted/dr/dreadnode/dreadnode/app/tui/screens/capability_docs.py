"""Capability file browser for local capability source trees."""

from __future__ import annotations

import typing as t

from rich.text import Text
from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import DirectoryTree, Markdown, MarkdownViewer, Static

from dreadnode.app.tui.screens.base import DreadnodeScreen
from dreadnode.app.tui.theme import FG, FG_FAINTEST, FG_MUTED, FG_SUBTLE

if t.TYPE_CHECKING:
    from pathlib import Path

    from textual.app import ComposeResult

_HIDDEN_NAMES = {
    "__pycache__",
    ".DS_Store",
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".svn",
}
_TEXT_PREVIEW_SUFFIXES = {
    ".json",
    ".md",
    ".mdx",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
_MAX_PREVIEW_BYTES = 256 * 1024


def _is_markdown_file(path: Path) -> bool:
    return path.suffix.lower() in {".md", ".mdx"} or path.name.lower().startswith("readme")


def _default_capability_doc(root: Path) -> Path | None:
    """Return the most useful initial file for a capability tree."""
    candidates = (
        root / "README.md",
        root / "README.mdx",
        root / "README",
        root / "AGENTS.md",
        root / "capability.yaml",
        root / "capability.yml",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate

    for pattern in ("agents/*.md", "agents/*.mdx", "*.md", "*.mdx"):
        matches = sorted(root.glob(pattern))
        if matches:
            return matches[0]
    return None


def _is_binary_file(path: Path) -> bool:
    try:
        sample = path.read_bytes()[:2048]
    except OSError:
        return False
    return b"\x00" in sample


def _fence_language(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".py": "python",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
        ".txt": "text",
    }.get(suffix, suffix.lstrip(".") or "text")


def _render_text_preview(root: Path, path: Path) -> str:
    """Wrap a text file in fenced markdown for preview."""
    relative = path.relative_to(root)
    try:
        body = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        body = path.read_text(encoding="utf-8", errors="replace")
    return f"# `{relative}`\n\n```{_fence_language(path)}\n{body}\n```"


def _normalize_path(root: Path, candidate: Path) -> Path | None:
    """Resolve a candidate path and keep it constrained to the root."""
    try:
        resolved_root = root.resolve()
        resolved_candidate = candidate.resolve()
        resolved_candidate.relative_to(resolved_root)
    except (OSError, ValueError):
        return None
    return resolved_candidate


class _CapabilityDirectoryTree(DirectoryTree):
    """Directory tree with noisy cache/build artifacts hidden."""

    def filter_paths(self, paths: t.Iterable[Path]) -> t.Iterable[Path]:
        for path in paths:
            name = path.name
            if name in _HIDDEN_NAMES or name.startswith(".") or name.endswith(".pyc"):
                continue
            yield path


class CapabilityDocsScreen(DreadnodeScreen):
    """Browse a local capability tree with markdown rendering."""

    BINDINGS: t.ClassVar[list[Binding]] = [
        Binding("escape", "close", "Close", show=True),
        Binding("b", "history_back", "Back", show=True),
        Binding("f", "history_forward", "Forward", show=True),
    ]

    def __init__(
        self,
        capability_name: str,
        root: Path,
        initial_path: Path | None = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)
        self._capability_name = capability_name
        self._root = root.expanduser().resolve()
        self._initial_path = initial_path or _default_capability_doc(self._root)
        self._current_path: Path | None = None
        self._history: list[Path] = []
        self._history_index = -1

    def compose_content(self) -> ComposeResult:
        subtitle = f"\n[{FG_FAINTEST}] Browse local capability files under {self._root}[/]"
        yield Static(
            f"[bold {FG}] Capability Files[/]  [{FG_MUTED}]{self._capability_name}[/]{subtitle}",
            id="cap-docs-title",
        )
        with Horizontal(id="cap-docs-body"):
            yield _CapabilityDirectoryTree(self._root, id="cap-docs-tree")
            with Vertical(id="cap-docs-viewer-pane"):
                yield Static("", id="cap-docs-path")
                yield MarkdownViewer(
                    show_table_of_contents=False,
                    open_links=False,
                    id="cap-docs-viewer",
                )

    def on_mount(self) -> None:
        super().on_mount()
        self.query_one("#cap-docs-tree", DirectoryTree).focus()
        self._on_mount_async()

    @work
    async def _on_mount_async(self) -> None:
        if self._initial_path is not None:
            await self._open_path(self._initial_path)
            return
        await self._show_message(
            "# No previewable files found\n\nSelect a file from the tree to inspect it.",
        )

    async def _show_message(self, message: str) -> None:
        # Workers can land here after the screen was popped — bail out rather
        # than query (NoMatches) or mount into a removed viewer (MountError).
        if not self.is_mounted:
            return
        viewer = self.query_one("#cap-docs-viewer", MarkdownViewer)
        await viewer.document.update(message)

    def _set_history(self, path: Path) -> None:
        if self._history_index >= 0 and self._history[self._history_index] == path:
            return
        self._history = self._history[: self._history_index + 1]
        self._history.append(path)
        self._history_index = len(self._history) - 1

    def _update_path_bar(self) -> None:
        path_bar = self.query_one("#cap-docs-path", Static)
        if self._current_path is None:
            path_bar.update("")
            return
        relative = self._current_path.relative_to(self._root)
        text = Text()
        text.append(" ")
        text.append(str(relative), style=FG_SUBTLE)
        if self._history:
            text.append(
                f"  {self._history_index + 1}/{len(self._history)}",
                style=FG_FAINTEST,
            )
        path_bar.update(text)

    async def _open_path(
        self,
        path: Path,
        *,
        push_history: bool = True,
        anchor: str | None = None,
    ) -> None:
        if not self.is_mounted:
            return
        normalized = _normalize_path(self._root, path)
        if normalized is None:
            await self._show_message(
                "# File Unavailable\n\nThe requested file is outside the capability root.",
            )
            return
        if normalized.is_dir():
            directory_doc = _default_capability_doc(normalized)
            if directory_doc is None:
                await self._show_message(
                    "# Directory Selected\n\nThis directory does not contain a previewable document.",
                )
                return
            normalized = directory_doc
        if not normalized.is_file():
            await self._show_message("# File Missing\n\nThe selected file no longer exists.")
            return

        viewer = self.query_one("#cap-docs-viewer", MarkdownViewer)
        if normalized.stat().st_size > _MAX_PREVIEW_BYTES:
            await self._show_message(
                f"# File Too Large\n\n`{normalized.name}` is too large to preview in the TUI.",
            )
            return
        if _is_markdown_file(normalized):
            await viewer.document.load(normalized)
        elif normalized.suffix.lower() in _TEXT_PREVIEW_SUFFIXES and not _is_binary_file(
            normalized
        ):
            await viewer.document.update(_render_text_preview(self._root, normalized))
        else:
            await self._show_message(
                f"# Binary Or Unsupported\n\n`{normalized.name}` can't be previewed here.",
            )
            return

        # The document load/update awaited above — the screen may have been
        # popped in the meantime.
        if not self.is_mounted:
            return
        if anchor:
            viewer.document.goto_anchor(anchor)
        self._current_path = normalized
        if push_history:
            self._set_history(normalized)
        self._update_path_bar()

    async def _open_href(self, href: str, *, push_history: bool = True) -> None:
        if href.startswith(("http://", "https://", "mailto:")):
            self.notify(
                "External links are not opened from the capability browser",
                severity="warning",
            )
            return
        target, _, anchor = href.partition("#")
        if not target:
            if self._current_path is None:
                return
            await self._open_path(self._current_path, push_history=False, anchor=anchor or None)
            return
        base_dir = self._current_path.parent if self._current_path is not None else self._root
        await self._open_path(base_dir / target, push_history=push_history, anchor=anchor or None)

    @on(DirectoryTree.FileSelected, "#cap-docs-tree")
    async def _on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        await self._open_path(event.path)

    @on(Markdown.LinkClicked)
    async def _on_markdown_link_clicked(self, event: Markdown.LinkClicked) -> None:
        viewer = self.query_one("#cap-docs-viewer", MarkdownViewer)
        if event.markdown is not viewer.document:
            return
        event.stop()
        await self._open_href(event.href)

    def action_close(self) -> None:
        self.dismiss()

    def action_history_back(self) -> None:
        if self._history_index <= 0:
            return
        self._history_index -= 1
        self.run_worker(
            self._open_path(self._history[self._history_index], push_history=False),
            exclusive=True,
            group="cap-docs",
        )

    def action_history_forward(self) -> None:
        if self._history_index >= len(self._history) - 1:
            return
        self._history_index += 1
        self.run_worker(
            self._open_path(self._history[self._history_index], push_history=False),
            exclusive=True,
            group="cap-docs",
        )
