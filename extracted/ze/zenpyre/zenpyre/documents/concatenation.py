"""Provide utilities for concatenating documents."""

from __future__ import annotations

__all__ = [
    "format_documents",
    "format_documents_as_json",
    "format_documents_as_markdown",
    "format_documents_as_xml",
]

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

    from langchain_core.documents import Document


def _build_blocks(
    documents: list[Document],
    include_metadata: bool,
    header_fn: Callable[[int, str], str],
    metadata_line_fn: Callable[[Any, Any], str],
) -> str:
    """Build the shared per-document block structure used by both the
    Markdown and XML formatters.

    Args:
        documents: The documents to concatenate.
        include_metadata: If ``True``, include each document's metadata
            above its content.
        header_fn: A callable ``(index, body) -> str`` that wraps a
            document's body in the format-specific header/delimiter.
        metadata_line_fn: A callable ``(key, value) -> str`` that renders
            a single metadata entry in the format-specific style.

    Returns:
        A single string with one block per document, in the same order as
        ``documents``. Returns an empty string if ``documents`` is empty.
    """
    blocks = []
    for i, doc in enumerate(documents, start=1):
        parts = []
        if include_metadata and doc.metadata:
            metadata_lines = "\n".join(
                metadata_line_fn(key, doc.metadata[key]) for key in sorted(doc.metadata)
            )
            parts.append(metadata_lines)
        parts.append(doc.page_content)
        body = "\n\n".join(parts)
        blocks.append(header_fn(i, body))
    return "\n\n".join(blocks)


def format_documents(
    documents: list[Document],
    include_metadata: bool = False,
    output_format: str = "xml",
) -> str:
    """Concatenate a list of LangChain documents into a single LLM-
    friendly string, in either XML or Markdown format.

    This is a convenience dispatcher over :func:`format_documents_as_xml`
    and :func:`format_documents_as_markdown`. See those functions for
    details on how each format renders documents and metadata.

    Args:
        documents: The documents to concatenate.
        include_metadata: If ``True``, include each document's metadata
            above its content, sorted alphabetically by key. Defaults to
            ``False``.
        output_format: Either ``"xml"`` or ``"markdown"``. Defaults to
            ``"xml"``.

    Returns:
        A single string with one document block per document, in the same
        order as ``documents``. Returns an empty string if ``documents``
        is empty.

    Raises:
        ValueError: If ``output_format`` is not ``"xml"`` or ``"markdown"``.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import format_documents
        >>> docs = [
        ...     Document(page_content="The cat sat on the mat."),
        ... ]
        >>> print(format_documents(docs, output_format="xml"))
        <document id="1">
        The cat sat on the mat.
        </document>
        >>> print(format_documents(docs, output_format="markdown"))
        ## Document 1
        <BLANKLINE>
        The cat sat on the mat.

        ```
    """
    if output_format == "xml":
        return format_documents_as_xml(documents, include_metadata=include_metadata)
    if output_format == "markdown":
        return format_documents_as_markdown(documents, include_metadata=include_metadata)
    if output_format == "json":
        return format_documents_as_json(documents, include_metadata=include_metadata)
    msg = f"Unknown format: {output_format}"
    raise ValueError(msg)


def format_documents_as_json(documents: list[Document], include_metadata: bool = False) -> str:
    """Concatenate a list of LangChain documents into a single LLM-
    friendly JSON string.

        Each document is rendered as an object with an ``id`` field and a
        ``content`` field. When ``include_metadata`` is ``True``, a
        ``metadata`` field (a JSON object, keys sorted alphabetically) is
        also included.

    Args:
            documents: The documents to concatenate.
            include_metadata: If ``True``, include each document's metadata
                as a nested object. Defaults to ``False``.

    Returns:
            A JSON array (as a string) with one object per document, in the
            same order as ``documents``. Returns ``"[]"`` if ``documents`` is
            empty.

    Example:
    ```pycon
    >>> from langchain_core.documents import Document
    >>> from zenpyre.documents import format_documents_as_json
    >>> docs = [
    ...     Document(
    ...         page_content="The cat sat on the mat.",
    ...         metadata={"source": "story.txt", "author": "Alice"},
    ...     ),
    ... ]
    >>> print(format_documents_as_json(docs))
    [
      {
        "id": 1,
        "content": "The cat sat on the mat."
      }
    ]
    >>> print(format_documents_as_json(docs, include_metadata=True))
    [
      {
        "id": 1,
        "metadata": {
          "author": "Alice",
          "source": "story.txt"
        },
        "content": "The cat sat on the mat."
      }
    ]
    >>> format_documents_as_json([])
    '[]'

    ```
    """
    entries = []
    for i, doc in enumerate(documents, start=1):
        entry: dict[str, Any] = {"id": i}
        if include_metadata and doc.metadata:
            entry["metadata"] = dict(sorted(doc.metadata.items()))
        entry["content"] = doc.page_content
        entries.append(entry)
    return json.dumps(entries, indent=2)


def format_documents_as_markdown(documents: list[Document], include_metadata: bool = False) -> str:
    """Concatenate a list of LangChain documents into a single LLM-
    friendly Markdown string.

    Each document is rendered under its own level-2 heading (``## Document N``)
    so the LLM can distinguish document boundaries. When ``include_metadata``
    is ``True``, each document's metadata is rendered as a Markdown bullet
    list above its content, sorted alphabetically by key.

    Args:
        documents: The documents to concatenate.
        include_metadata: If ``True``, include each document's metadata
            (as a bullet list, sorted by key) above its content. Defaults
            to ``False``.

    Returns:
        A single string with one ``## Document N`` section per document,
        in the same order as ``documents``. Returns an empty string if
        ``documents`` is empty.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import format_documents_as_markdown
        >>> docs = [
        ...     Document(
        ...         page_content="The cat sat on the mat.",
        ...         metadata={"source": "story.txt", "author": "Alice"},
        ...     ),
        ...     Document(
        ...         page_content="The dog chased the ball.",
        ...         metadata={"source": "story.txt", "author": "Bob"},
        ...     ),
        ... ]
        >>> print(format_documents_as_markdown(docs))
        ## Document 1
        <BLANKLINE>
        The cat sat on the mat.
        <BLANKLINE>
        ## Document 2
        <BLANKLINE>
        The dog chased the ball.
        >>> print(format_documents_as_markdown(docs, include_metadata=True))
        ## Document 1
        <BLANKLINE>
        - author: Alice
        - source: story.txt
        <BLANKLINE>
        The cat sat on the mat.
        <BLANKLINE>
        ## Document 2
        <BLANKLINE>
        - author: Bob
        - source: story.txt
        <BLANKLINE>
        The dog chased the ball.
        >>> format_documents_as_markdown([])
        ''

        ```
    """
    return _build_blocks(
        documents,
        include_metadata,
        header_fn=lambda i, body: f"## Document {i}\n\n{body}",
        metadata_line_fn=lambda key, value: f"- {key}: {value}",
    )


def format_documents_as_xml(documents: list[Document], include_metadata: bool = False) -> str:
    """Concatenate a list of LangChain documents into a single LLM-
    friendly XML-tagged string.

    Each document is rendered as a clearly delimited ``<document>`` block so
    the LLM can distinguish document boundaries. When ``include_metadata``
    is ``True``, each document's metadata is rendered above its content as
    ``key: value`` lines, sorted alphabetically by key.

    Args:
        documents: The documents to concatenate.
        include_metadata: If ``True``, include each document's metadata
            (as ``key: value`` lines, sorted by key) above its content.
            Defaults to ``False``.

    Returns:
        A single string with one ``<document>`` block per document, in the
        same order as ``documents``. Returns an empty string if
        ``documents`` is empty.

    Example:
        ```pycon
        >>> from langchain_core.documents import Document
        >>> from zenpyre.documents import format_documents_as_xml
        >>> docs = [
        ...     Document(
        ...         page_content="The cat sat on the mat.",
        ...         metadata={"source": "story.txt", "author": "Alice"},
        ...     ),
        ...     Document(
        ...         page_content="The dog chased the ball.",
        ...         metadata={"source": "story.txt", "author": "Bob"},
        ...     ),
        ... ]
        >>> print(format_documents_as_xml(docs))
        <document id="1">
        The cat sat on the mat.
        </document>
        <BLANKLINE>
        <document id="2">
        The dog chased the ball.
        </document>
        >>> print(format_documents_as_xml(docs, include_metadata=True))
        <document id="1">
        author: Alice
        source: story.txt
        <BLANKLINE>
        The cat sat on the mat.
        </document>
        <BLANKLINE>
        <document id="2">
        author: Bob
        source: story.txt
        <BLANKLINE>
        The dog chased the ball.
        </document>
        >>> format_documents_as_xml([])
        ''

        ```
    """
    return _build_blocks(
        documents,
        include_metadata,
        header_fn=lambda i, body: f'<document id="{i}">\n{body}\n</document>',
        metadata_line_fn=lambda key, value: f"{key}: {value}",
    )
