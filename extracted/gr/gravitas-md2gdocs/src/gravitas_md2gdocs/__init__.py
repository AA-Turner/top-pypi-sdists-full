"""
gravitas-md2gdocs - Convert Markdown to Google Docs API requests.

Basic usage:
    from gravitas_md2gdocs import to_requests

    requests = to_requests("# Hello\\n\\nThis is **bold**")

    # Use with your Google Docs API client:
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()

With Google API helpers (requires `pip install gravitas-md2gdocs[google]`):
    from gravitas_md2gdocs import append, replace, insert_at

    append(docs_service, doc_id, "## New Section")
    replace(docs_service, doc_id, new_markdown)
    insert_at(docs_service, doc_id, "**inserted**", index=25)
"""

try:
    from ._version import __version__  # type: ignore
except ImportError:
    __version__ = "0.0.0.dev0"

from .converter import DocsRequestBuilder
from .parser import MarkdownParser, Paragraph, TextRun

__all__ = [
    # Main function
    "to_requests",
    # Google API helpers
    "get_end_index",
    "append",
    "replace",
    "insert_at",
    "replace_range",
    # Classes (for advanced usage)
    "MarkdownParser",
    "DocsRequestBuilder",
    "Paragraph",
    "TextRun",
]


def to_requests(markdown: str, *, start_index: int = 1) -> list[dict]:
    """
    Convert markdown to Google Docs API batchUpdate requests.

    Args:
        markdown: Markdown text to convert.
        start_index: Document index to insert at (default: 1, start of doc).

    Returns:
        List of request dicts for `documents().batchUpdate()`.

    Example:
        >>> requests = to_requests("# Title\\n\\nSome **bold** text")
        >>> len(requests) > 0
        True
    """
    parser = MarkdownParser(markdown)
    paragraphs = parser.parse()
    builder = DocsRequestBuilder(start_index=start_index)
    return builder.build(paragraphs)


# --- Google API Helpers ---
# These require google-api-python-client to be installed.
# Install with: pip install gravitas-md2gdocs[google]


def get_end_index(docs_service, doc_id: str) -> int:
    """
    Get the end index of a document (for appending).

    Args:
        docs_service: Google Docs API service instance.
        doc_id: Document ID.

    Returns:
        End index where new content can be inserted.
    """
    doc = docs_service.documents().get(documentId=doc_id).execute()
    body_content = doc.get("body", {}).get("content", [])
    if body_content:
        return body_content[-1].get("endIndex", 1) - 1
    return 1


def append(docs_service, doc_id: str, markdown: str) -> None:
    """
    Append markdown content to the end of an existing document.

    Args:
        docs_service: Google Docs API service instance.
        doc_id: Document ID.
        markdown: Markdown text to append.

    Example:
        append(docs_service, doc_id, "## New Section\\n\\nMore content")
    """
    end_index = get_end_index(docs_service, doc_id)
    requests = to_requests(markdown, start_index=end_index)

    if requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests},
        ).execute()


def replace(docs_service, doc_id: str, markdown: str) -> None:
    """
    Replace all content in a document with new markdown.

    Args:
        docs_service: Google Docs API service instance.
        doc_id: Document ID.
        markdown: Markdown text to replace content with.

    Example:
        replace(docs_service, doc_id, "# New Document\\n\\nFresh content")
    """
    end_index = get_end_index(docs_service, doc_id)

    # Delete existing content if any
    if end_index > 1:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={
                "requests": [
                    {"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_index}}}
                ]
            },
        ).execute()

    # Insert new content
    requests = to_requests(markdown, start_index=1)
    if requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests},
        ).execute()


def insert_at(docs_service, doc_id: str, markdown: str, *, index: int) -> None:
    """
    Insert markdown at a specific index in the document.

    Args:
        docs_service: Google Docs API service instance.
        doc_id: Document ID.
        markdown: Markdown text to insert.
        index: Position to insert at.

    Example:
        insert_at(docs_service, doc_id, "**inserted text**", index=25)
    """
    requests = to_requests(markdown, start_index=index)

    if requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests},
        ).execute()


def replace_range(
    docs_service,
    doc_id: str,
    markdown: str,
    *,
    start: int,
    end: int,
) -> None:
    """
    Replace a specific range in the document with markdown.

    Args:
        docs_service: Google Docs API service instance.
        doc_id: Document ID.
        markdown: Markdown text to insert.
        start: Start index of range to replace.
        end: End index of range to replace.

    Example:
        replace_range(docs_service, doc_id, "**new text**", start=10, end=50)
    """
    # Delete the range first
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [{"deleteContentRange": {"range": {"startIndex": start, "endIndex": end}}}]
        },
    ).execute()

    # Insert new content at start position
    requests = to_requests(markdown, start_index=start)
    if requests:
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={"requests": requests},
        ).execute()
