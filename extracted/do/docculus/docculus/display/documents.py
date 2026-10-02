r"""Contain utilities to print an iterable of LangChain documents to the
terminal."""

from __future__ import annotations

__all__ = ["print_documents"]

from typing import TYPE_CHECKING

from coola.utils.imports import check_rich, is_rich_available

from docculus.display.document import print_document

if is_rich_available():
    from rich import get_console

if TYPE_CHECKING:
    from collections.abc import Iterable

    from langchain_core.documents import Document
    from rich.console import Console


def print_documents(
    documents: Iterable[Document],
    max_length: int = 500,
    console: Console | None = None,
    compact_metadata: bool = False,
) -> None:
    """Pretty-print an iterable of LangChain documents to the terminal
    using rich.

    Each document is rendered with :func:`print_document`, one bordered
    panel per document, printed in order to the same console.

    Args:
        documents: A list, generator, or other iterable of
            ``langchain_core.documents.Document`` objects. Consumed
            exactly once; if a generator/iterator is passed in, it will
            be exhausted by this call.
        max_length: Maximum number of content characters to display
            per document before truncating. Defaults to ``500``.
        console: An optional rich :class:`~rich.console.Console` to
            print to. If ``None``, the current active console (as
            returned by :func:`rich.get_console`) is used.
        compact_metadata: If ``True``, render each document's metadata
            entries as a single dimmed inline line instead of one per
            line. Defaults to ``False``.
    """
    check_rich()
    console = console or get_console()

    for doc in documents:
        print_document(
            doc, max_length=max_length, console=console, compact_metadata=compact_metadata
        )
