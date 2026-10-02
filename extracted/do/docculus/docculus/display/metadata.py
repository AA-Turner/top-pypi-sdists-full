r"""Contain utilities to print LangChain document metadata to the
terminal."""

from __future__ import annotations

__all__ = ["print_documents_metadata"]

from typing import TYPE_CHECKING

from coola.utils.imports import check_rich, is_rich_available

if is_rich_available():
    from rich import get_console
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.text import Text

if TYPE_CHECKING:
    from collections.abc import Sequence

    from langchain_core.documents import Document


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
            each line. Defaults to ``"•"``.
        console: An optional rich :class:`~rich.console.Console` to
            print to. If ``None``, the current active console (as
            returned by :func:`rich.get_console`) is used.
    """
    check_rich()
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
