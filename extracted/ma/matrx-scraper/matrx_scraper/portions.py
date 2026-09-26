"""Web-page materializers: a captured page's text, cut into addressable portions.

SOURCE-CONVERGENCE §3.3. A materializer is free (no model, no network) and is the ONLY per-kind
code between a producer and the landing door: it turns what a producer already has into the
ordered list of portions the door persists as ``docproc.processed_document_pages``.

A web page portions by its H1–H3 headings: each section carries its ``heading_path`` and a
``text_fragment`` (its first 80 characters), which is enough to scroll a browser to the passage
with a text fragment (``#:~:text=``). A page with no headings is one section.

Returned as plain dicts (``ordinal``, ``kind``, ``text``, ``locator``, ``method``) because this
package may not import the host's ``landing_types``; the door validates them into ``Portion``.
"""

from __future__ import annotations

import re
from typing import Any

__all__ = [
    "from_markdown",
    "from_article_html",
    "from_parsed_page",
    "section_locator",
    "structured_from_parsed_page",
]

_FRAGMENT_CHARS = 80
_HEADING_TAGS = {"h1": 1, "h2": 2, "h3": 3}
_SKIP_TAGS = {"script", "style", "template", "noscript"}
_BLOCK_TAGS = {
    "address", "article", "aside", "blockquote", "br", "dd", "div", "dl", "dt", "figcaption",
    "figure", "footer", "h4", "h5", "h6", "header", "hr", "li", "main", "nav", "ol", "p", "pre",
    "section", "table", "td", "th", "tr", "ul",
}
_WS = re.compile(r"\s+")
_ATX = re.compile(r"^ {0,3}(#{1,3})[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$")
_FENCE = re.compile(r"^ {0,3}(```|~~~)")

# ONE PORTIONER, TWO LANGUAGES. These rules are a line-for-line port of the extension's
# ``matrx-extend/src/lib/sources/portions.ts`` (``portionsFromArticleHtml`` / ``portionsFromMarkdown``):
# a page the extension saves and the same page the server scrapes must cut into the SAME sections,
# or they land as two Sources. Pinned by ``tests/fixtures/portions/*.json`` (real pages, both
# paths), which the extension's tests read too. Change both sides together.
#   * heading_path is the stack of ancestor headings BY LEVEL (a page whose headings start at H2
#     gives ['Use'], never ['Versions', 'Use'] for a sibling);
#   * text is the concatenation of the DOM's text nodes, with a line break at every block element
#     and whitespace collapsed per line — inline markup never inserts a space ("HTTP (Hypertext").


def section_locator(heading_path: list[str], text: str) -> dict[str, Any]:
    """The locator of one section: where it sits and how to find it on the page."""
    return {"heading_path": list(heading_path), "text_fragment": _WS.sub(" ", text or "").strip()[:_FRAGMENT_CHARS]}


def _tidy_lines(raw: str) -> list[str]:
    return [line for line in (_WS.sub(" ", seg).strip() for seg in raw.split("\n")) if line]


def _next_path(stack: list[str | None], level: int, heading: str) -> list[str]:
    del stack[level - 1 :]
    while len(stack) < level - 1:
        stack.append(None)
    stack.append(heading)
    return [h for h in stack if h]


def _finish(drafts: list[tuple[list[str], list[str]]], method: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for path, lines in drafts:
        text = "\n".join(lines).strip()
        if not text:
            continue
        out.append(
            {
                "ordinal": len(out) + 1,
                "kind": "section",
                "text": text,
                "locator": section_locator(path, text),
                "method": method,
            }
        )
    return out


def from_markdown(markdown: str | None, *, method: str = "native") -> list[dict[str, Any]]:
    """Split markdown at ATX ``#``, ``##``, ``###`` headings (never inside a fenced code block)."""
    if not markdown or not markdown.strip():
        return []
    stack: list[str | None] = []
    drafts: list[tuple[list[str], list[str]]] = [([], [])]
    fence: str | None = None
    for line in re.sub(r"\r\n?", "\n", markdown).split("\n"):
        fence_match = _FENCE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            fence = marker if fence is None else (None if fence == marker else fence)
        heading = _ATX.match(line) if fence is None and not fence_match else None
        if heading:
            level = len(heading.group(1))
            drafts.append((_next_path(stack, level, heading.group(2).strip()), [line.strip()]))
            continue
        drafts[-1][1].append(line)
    return _finish(drafts, method)


def from_article_html(html: str | None, *, method: str = "native") -> list[dict[str, Any]]:
    """Split article HTML (the extension's ``content_html_safe``) at h1–h3 into plain-text sections."""
    if not html or not html.strip():
        return []
    from bs4 import BeautifulSoup, Comment, NavigableString, Tag
    from bs4.element import CData, Declaration, Doctype, ProcessingInstruction

    body = BeautifulSoup(f"<body>{html}</body>", "html.parser")
    stack: list[str | None] = []
    drafts: list[tuple[list[str], list[str]]] = [([], [])]
    buffer = [""]

    def flush() -> None:
        drafts[-1][1].extend(_tidy_lines(buffer[0]))
        buffer[0] = ""

    def visit(node: Any) -> None:
        if isinstance(node, NavigableString):
            if isinstance(node, (Comment, CData, Declaration, Doctype, ProcessingInstruction)):
                return
            buffer[0] += str(node)
            return
        if not isinstance(node, Tag):
            return
        tag = (node.name or "").lower()
        if tag in _SKIP_TAGS:
            return
        level = _HEADING_TAGS.get(tag)
        if level is not None:
            flush()
            heading = _WS.sub(" ", node.get_text()).strip()
            if not heading:
                return
            drafts.append((_next_path(stack, level, heading), [heading]))
            return
        block = tag in _BLOCK_TAGS
        if block:
            buffer[0] += "\n"
        for child in list(node.children):
            visit(child)
        if block:
            buffer[0] += "\n"

    root = body.body or body
    for child in list(root.children):
        visit(child)
    flush()
    return _finish(drafts, method)


# ─────────────────────────────────────────────────────────────────────────────────────────────
# A server parse (``orchestrator.ScrapeResult``) — SOURCE-CONVERGENCE §3.3, first row
# ─────────────────────────────────────────────────────────────────────────────────────────────

#: The raw-parse fields a Source keeps on ``structured_json`` (§1 rule 5: portioning drops
#: nothing — the words go to portions, everything else the parse found goes here).
STRUCTURED_FIELDS: tuple[str, ...] = (
    "links",
    "link_records",
    "images",
    "videos",
    "audios",
    "tables",
    "code_blocks",
    "document_outline",
    "structured_data",
    "main_image",
    "cms",
    "hashes",
    "metadata",
    "published_at",
    "modified_at",
    "content_type",
    "status_code",
)


def _field(parsed: Any, name: str) -> Any:
    if isinstance(parsed, dict):
        return parsed.get(name)
    return getattr(parsed, name, None)


def from_parsed_page(parsed: Any, *, method: str = "native") -> list[dict[str, Any]]:
    """Portion one server parse (a ``ScrapeResult`` or its ``to_dict()``) by its H1–H3 headings.

    The body is the parser's ``markdown_renderable`` text: it is rendered from the parsed tree
    with ``remove_filtered``, so everything the parser labelled chrome (navigation, footers,
    sponsor rails) is already gone, and its headers are markdown ``#`` lines — which is exactly
    what :func:`from_markdown` cuts on. A page the parser could not organize (a PDF, plain text,
    JSON) falls back to its best flat text as one section. No headings = one section.
    """
    body = str(_field(parsed, "markdown_renderable") or "")
    portions = from_markdown(body, method=method) if body.strip() else []
    if portions:
        return portions
    for name in ("main_content_text", "ai_research_content", "text_data", "ai_content", "raw_text"):
        text = str(_field(parsed, name) or "")
        if text.strip():
            return from_markdown(text, method=method)
    return []


def _json_safe(value: Any) -> Any:
    import json

    return json.loads(json.dumps(value, default=str))


def structured_from_parsed_page(parsed: Any) -> dict[str, Any]:
    """The non-text half of a server parse — links, images, media, CMS, hashes — JSON-safe."""
    out: dict[str, Any] = {}
    for name in STRUCTURED_FIELDS:
        value = _field(parsed, name)
        if value in (None, "", [], {}):
            continue
        out[name] = value
    return _json_safe(out)
