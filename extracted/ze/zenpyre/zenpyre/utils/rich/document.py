r"""Contain utilities to print LangChain documents to the terminal."""

from __future__ import annotations

__all__ = ["print_document", "print_documents_metadata"]

from typing import TYPE_CHECKING

from rich import get_console
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

if TYPE_CHECKING:
    from collections.abc import Sequence

    from langchain_core.documents import Document


def _truncate(content: str, max_length: int) -> tuple[str, bool]:
    """Truncate ``content`` to ``max_length`` characters, breaking on
    the nearest word boundary rather than mid-word when possible.

    Args:
        content: The text to truncate.
        max_length: The maximum number of characters to keep.

    Returns:
        A ``(truncated_content, was_truncated)`` tuple. If ``content``
        is already within ``max_length``, it is returned unchanged
        along with ``False``.
    """
    if len(content) <= max_length:
        return content, False

    cut = content[:max_length]
    last_space = cut.rfind(" ")
    # Only snap to the word boundary if it doesn't discard too much text.
    if last_space > max_length * 0.8:
        cut = cut[:last_space]
    return cut.rstrip(), True


def print_document(
    doc: Document,
    max_length: int = 500,
    console: Console | None = None,
    compact_metadata: bool = False,
) -> None:
    """Pretty-print a LangChain document to the terminal using rich.

    Renders the document as a bordered panel titled with its ``id``,
    containing two nested panels: a ``content`` panel with the
    document's ``page_content`` (truncated on a word boundary and
    annotated with the omitted character count if it exceeds
    ``max_length``, with the total/truncated character count shown in
    its subtitle), and, if ``metadata`` is non-empty, a ``metadata``
    panel listing entries sorted by key.

    Args:
        doc: The document to display.
        max_length: Maximum number of content characters to display
            before truncating. Defaults to ``500``.
        console: An optional rich :class:`~rich.console.Console` to
            print to. If ``None``, the current active console (as
            returned by :func:`rich.get_console`) is used.
        compact_metadata: If ``True``, render metadata entries as a
            single dimmed inline line (``key: value · key: value``)
            instead of one per line. Useful when scanning many
            documents in a row and one metadata line per key would
            take up too much vertical space. Defaults to ``False``.
    """
    console = console or get_console()

    content, truncated = _truncate(doc.page_content, max_length)
    content_renderables = [Text(content)]

    if truncated:
        omitted = len(doc.page_content) - len(content)
        content_renderables.append(Text(f"… ({omitted:,} more characters)", style="dim italic"))

    content_panel = Panel(
        Group(*content_renderables),
        title="content",
        title_align="left",
        subtitle=f"{len(doc.page_content):,} chars" + (" (truncated)" if truncated else ""),
        subtitle_align="right",
        border_style="dim",
    )

    boxes = [content_panel]

    if doc.metadata:
        sorted_items = sorted(doc.metadata.items())

        if compact_metadata:
            line = " · ".join(f"[bold]{key}[/bold]: {value}" for key, value in sorted_items)
            metadata_renderable = Text.from_markup(line, style="dim")
        else:
            lines = "\n".join(f"[bold]{key}[/bold]: {value}" for key, value in sorted_items)
            metadata_renderable = Text.from_markup(lines, style="dim")

        boxes.append(
            Panel(
                metadata_renderable,
                title="metadata",
                title_align="left",
                border_style="dim",
            )
        )

    title = f"[bold]Document[/bold] [cyan]{doc.id}[/cyan]" if doc.id else "[bold]Document[/bold]"
    console.print(
        Panel(
            Group(*boxes),
            title=title,
            title_align="left",
            border_style="cyan",
            expand=False,
        )
    )


def print_documents_metadata(
    documents: Sequence[Document],
    separator: str = "•",
    console: Console | None = None,
) -> None:
    """Pretty-print metadata for a sequence of documents, one line each.

    Renders a bordered panel containing one line per document: the
    document's ``id`` (if present) followed by its metadata entries,
    sorted by key, rendered inline as ``key: value {separator} key: value``.
    Documents with no metadata show a dimmed placeholder instead.

    Args:
        documents: The documents whose metadata to display.
        separator: The string used to separate metadata entries on
            each line. Defaults to ``"·"``.
        console: An optional rich :class:`~rich.console.Console` to
            print to. If ``None``, the current active console (as
            returned by :func:`rich.get_console`) is used.
    """
    console = console or get_console()

    sep = f" {separator} "

    lines: list[Text] = []
    for i, doc in enumerate(documents):
        label = f"[cyan]{doc.id}[/cyan]" if doc.id else f"[dim]#{i}[/dim]"

        if doc.metadata:
            sorted_items = sorted(doc.metadata.items())
            meta = sep.join(f"[bold]{key}[/bold]: {value}" for key, value in sorted_items)
        else:
            meta = "[dim italic]no metadata[/dim italic]"

        lines.append(Text.from_markup(f"{label}  {meta}"))

    console.print(
        Panel(
            Group(*lines),
            title=f"[bold]Documents metadata[/bold] [dim]({len(documents)})[/dim]",
            title_align="left",
            border_style="cyan",
            expand=False,
        )
    )
