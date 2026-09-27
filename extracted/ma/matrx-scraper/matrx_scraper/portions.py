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
    "from_organized_data",
    "from_parsed_page",
    "plain_markdown_line",
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
#   * PORTION TEXT IS PLAIN TEXT on every path (the plan's rule): no markdown survives into a
#     portion — a heading is its words, a link is its text, an image is nothing, a list item has
#     no bullet, a table is one cell per line. ``plain_markdown_line`` is the markdown half of
#     that rule (the extension's ``portionsFromMarkdown`` ports it line for line).


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


_MD_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_MD_AUTOLINK = re.compile(r"<((?:https?|mailto):[^>\s]+)>")
_MD_STRONG = re.compile(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1")
_MD_EM = re.compile(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])")
_MD_CODE = re.compile(r"`([^`]*)`")
_MD_BULLET = re.compile(r"^\s*(?:[-*+]|\d{1,9}[.)])\s+")
_MD_QUOTE = re.compile(r"^\s*(?:>\s?)+")
_MD_RULE = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$")
_MD_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?\s*$")
_TABULATE_SEP = re.compile(r"^\s*-{2,}(?: {2,}-{2,})+\s*$")


def plain_markdown_line(line: str) -> list[str]:
    """One markdown line as the plain-text line(s) a portion stores (see the rule above).

    A pipe-table row becomes one line per cell; a table separator, a horizontal rule or a code
    fence becomes nothing. Headings are handled by the caller (their words, no ``#``)."""
    if _FENCE.match(line) or _MD_RULE.match(line) or _MD_TABLE_SEP.match(line) or _TABULATE_SEP.match(line):
        return []
    text = _MD_QUOTE.sub("", line)
    text = _MD_BULLET.sub("", text)
    cells = [text]
    stripped = text.strip()
    if stripped.startswith("|") and stripped.endswith("|") and len(stripped) > 1:
        cells = stripped[1:-1].split("|")
    out: list[str] = []
    for cell in cells:
        cell = _MD_IMAGE.sub("", cell)
        cell = _MD_LINK.sub(r"\1", cell)
        cell = _MD_AUTOLINK.sub(r"\1", cell)
        cell = _MD_CODE.sub(r"\1", cell)
        cell = _MD_STRONG.sub(r"\2", cell)
        cell = _MD_EM.sub(r"\1", cell)
        out.append(cell)
    return out


def from_markdown(markdown: str | None, *, method: str = "native") -> list[dict[str, Any]]:
    """Split markdown at ATX ``#``, ``##``, ``###`` headings (never inside a fenced code block),
    into PLAIN-TEXT sections: the markup is dropped by :func:`plain_markdown_line`; the text of a
    fenced code block is kept as written."""
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
            continue
        if fence is not None:
            drafts[-1][1].extend(_tidy_lines(line))
            continue
        heading = _ATX.match(line)
        if heading:
            level = len(heading.group(1))
            title = " ".join(_tidy_lines(" ".join(plain_markdown_line(heading.group(2).strip()))))
            if not title:
                continue
            drafts.append((_next_path(stack, level, title), [title]))
            continue
        for plain in plain_markdown_line(line):
            drafts[-1][1].extend(_tidy_lines(plain))
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


def _list_lines(content: Any) -> list[str]:
    if isinstance(content, str):
        return [content]
    if isinstance(content, dict):
        return _list_lines(content.get("content"))
    lines: list[str] = []
    for item in content or []:
        lines.extend(_list_lines(item))
    return lines


def from_organized_data(items: Any, *, method: str = "native") -> list[dict[str, Any]]:
    """Portion a server parse's ``organized_data`` (the parser's own tree, data form: anchors
    already removed) into plain-text H1–H3 sections — the server twin of
    :func:`from_article_html`: a heading is its words, a paragraph its text, a list one item per
    line, a table its header cells then each row's cells in column order, one per line (the
    extension's DOM walk gives every ``<th>``/``<td>`` its own line). Media carry no words."""
    if not isinstance(items, list) or not items:
        return []
    stack: list[str | None] = []
    drafts: list[tuple[list[str], list[str]]] = [([], [])]
    for item in items:
        if not isinstance(item, dict):
            continue
        kind = item.get("type")
        if kind == "header":
            level = int(item.get("level") or 0)
            words = " ".join(_tidy_lines(str(item.get("content") or "")))
            if level == 0 or not words:
                continue  # the parser's "unassociated" bucket marker, never a heading
            if level <= 3:
                drafts.append((_next_path(stack, level, words), [words]))
            else:
                drafts[-1][1].append(words)
        elif kind in ("text", "quote", "code"):
            drafts[-1][1].extend(_tidy_lines(str(item.get("content") or "")))
        elif kind == "list":
            for entry in _list_lines(item.get("content")):
                drafts[-1][1].extend(_tidy_lines(entry))
        elif kind == "table":
            rows = [r for r in item.get("rows") or [] if isinstance(r, dict)]
            if not rows:
                continue
            columns = list(dict.fromkeys(col for row in rows for col in row))
            drafts[-1][1].extend(line for col in columns if not _is_generic_column(col) for line in _tidy_lines(col))
            for row in rows:
                for col in columns:
                    drafts[-1][1].extend(_tidy_lines(str(row.get(col) or "")))
    return _finish(drafts, method)


_GENERIC_COLUMN = re.compile(r"^col\d+$")


def _is_generic_column(name: str) -> bool:
    """The parser names header-less columns ``col1``, ``col2``… — a name the page never said."""
    return bool(_GENERIC_COLUMN.match(name))


def from_parsed_page(parsed: Any, *, method: str = "native") -> list[dict[str, Any]]:
    """Portion one server parse (a ``ScrapeResult`` or its ``to_dict()``) by its H1–H3 headings.

    The body is the parser's ``organized_data`` tree (:func:`from_organized_data`): it is built
    with ``remove_filtered``, so everything the parser labelled chrome (navigation, footers,
    sponsor rails) is already gone, and it is plain — no markdown reaches a portion. A parse
    without that tree falls back to ``markdown_renderable`` through the plain markdown path, then
    to its best flat text (a PDF, plain text, JSON) as one section. No headings = one section.
    """
    portions = from_organized_data(_field(parsed, "organized_data"), method=method)
    if portions:
        return portions
    for name in (
        "markdown_renderable",
        "main_content_text",
        "ai_research_content",
        "text_data",
        "ai_content",
        "raw_text",
    ):
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
