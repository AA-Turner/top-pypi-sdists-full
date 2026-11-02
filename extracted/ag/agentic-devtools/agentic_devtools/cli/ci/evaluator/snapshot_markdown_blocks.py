"""Markdown block helpers used while scanning comment bodies."""

from __future__ import annotations

import re

_ATX_HEADING_RE = re.compile(r"^#{1,6}(?:[ \t]|$)")
# CommonMark type-1 and type-6 HTML block tag names that may interrupt a paragraph.
# Type-1: <pre>, <script>, <style>, <textarea> (and their closing variants).
# Type-6: the block-level elements listed in the CommonMark spec §4.6.
# Type-7 tags (e.g. <span>, <em>) cannot interrupt a paragraph and are excluded.
_HTML_BLOCK_TYPE1_NAMES = frozenset({"pre", "script", "style", "textarea"})
_HTML_BLOCK_TYPE6_NAMES = frozenset(
    {
        "address",
        "article",
        "aside",
        "base",
        "basefont",
        "blockquote",
        "body",
        "caption",
        "center",
        "col",
        "colgroup",
        "dd",
        "details",
        "dialog",
        "dir",
        "div",
        "dl",
        "dt",
        "fieldset",
        "figcaption",
        "figure",
        "footer",
        "form",
        "frame",
        "frameset",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "head",
        "header",
        "hr",
        "html",
        "iframe",
        "legend",
        "li",
        "link",
        "main",
        "menu",
        "menuitem",
        "meta",
        "nav",
        "noframes",
        "ol",
        "optgroup",
        "option",
        "p",
        "param",
        "search",
        "section",
        "summary",
        "table",
        "tbody",
        "td",
        "tfoot",
        "th",
        "thead",
        "title",
        "tr",
        "track",
        "ul",
    }
)
_HTML_BLOCK_INTERRUPT_NAMES = _HTML_BLOCK_TYPE1_NAMES | _HTML_BLOCK_TYPE6_NAMES
# Matches a line-leading open/close tag whose name is a paragraph-interrupting
# block-level element (type-1 or type-6).  The tag name is captured so callers
# can look it up in _HTML_BLOCK_INTERRUPT_NAMES (case-insensitively).
_HTML_BLOCK_TAG_START_RE = re.compile(r"^</?([A-Za-z][A-Za-z0-9-]*)(?:\s[^>]*)?>")
# Matches a line-leading list-item marker on blockquote-stripped content: a
# bullet (``-``/``+``/``*``) or an ordered marker (1-9 digits then ``.`` or
# ``)``), followed by a space/tab or end of line. Used both for list-item
# content-indent tracking and to detect paragraph-breaking list items. CommonMark
# only lets an ordered list interrupt an active paragraph when it starts at ``1``
# (handled by :func:`_interrupts_paragraph_with_list_item`), but non-``1``
# ordered markers still count as list items after a real block boundary.
_LIST_ITEM_RE = re.compile(r"^(?P<marker>(?:[-+*])|(?P<ordered>\d{1,9}[.)]))(?:[ \t]|$)")


def _advance_column(column: int, char: str) -> int:
    """Return the next visual column after consuming one whitespace character."""
    if char == "\t":
        return column + (4 - (column % 4))
    return column + (1 if char == " " else 0)


def _leading_whitespace_columns(text: str, *, start_column: int = 0) -> int:
    """Return the visual width of ``text``'s leading whitespace.

    Tabs expand to the next four-column stop from ``start_column`` so callers can
    measure indentation relative to an existing container column.
    """
    column = start_column
    i = 0
    while i < len(text) and text[i] in {" ", "\t"}:
        column = _advance_column(column, text[i])
        i += 1
    return column - start_column


def _list_item_content_indent(stripped: str, indent: int) -> int | None:
    """Return the content indent (columns) for a list-item line, or ``None``.

    ``stripped`` is the line with blockquote markers and leading whitespace
    removed; ``indent`` is its leading indentation in columns relative to any
    enclosing blockquote. Follows the CommonMark rule that 1–4 spaces after the
    marker set the item's content indent, while more than four spaces (or an
    empty item) fall back to a single space — the extra indentation then becomes
    indented code *within* the item. Used so an indented line inside a list item
    is measured relative to the item's content column rather than column zero.
    """
    match = _LIST_ITEM_RE.match(stripped)
    if match is None:
        return None
    marker = match.group(0).rstrip(" \t")
    rest = stripped[len(marker) :]
    padding_cols = _leading_whitespace_columns(rest, start_column=indent + len(marker))
    if padding_cols > 4 or not rest.strip():
        padding_cols = 1
    return indent + len(marker) + padding_cols


def _strip_list_item_prefix_for_block_detection(stripped: str, indent: int) -> str:
    """Return ``stripped`` with only a list marker's effective padding removed."""
    match = _LIST_ITEM_RE.match(stripped)
    if match is None:
        return stripped
    marker = match.group(0).rstrip(" \t")
    rest = stripped[len(marker) :]
    if not rest:
        return ""
    padding_cols = _leading_whitespace_columns(rest, start_column=indent + len(marker))
    if padding_cols > 4:
        return rest[1:] if rest[:1] in {" ", "\t"} else rest
    return rest.lstrip(" \t")


def _interrupts_paragraph_with_list_item(stripped: str, *, in_list_context: bool) -> bool:
    """Return True when ``stripped`` starts a list item that may interrupt a paragraph.

    CommonMark allows bullet-list items to interrupt a paragraph, but ordered
    lists only do so when their marker starts at ``1``. Non-``1`` ordered
    markers are still recognised as list items by :func:`_list_item_content_indent`;
    they just do not flush an already-active *top-level* paragraph. Within an
    existing list container, a later ordered item (e.g. ``2.`` after ``1.``)
    still starts a new sibling item and must therefore break paragraph
    accumulation.
    """
    match = _LIST_ITEM_RE.match(stripped)
    if match is None:
        return False
    ordered = match.group("ordered")
    # ``ordered`` (when present) is the digits plus a trailing ``.``/``)``; the
    # start number must equal ``1`` (parsed as int to handle leading zeroes such
    # as ``01.``) — ``14.`` / ``10)`` do not interrupt.
    return ordered is None or int(ordered[:-1]) == 1 or in_list_context
