"""THE HTML element list — twin of content-ir ``source/html-elements.ts``.

Why it exists (2026-10-21 production regression): the block detector, the island tokenizer and
their TypeScript twins claimed every line-leading tag that was neither a Matrx tag nor on the
sanitizer's small raw-HTML allow-list as a CUSTOM XML container, so ``<div>``, ``<section>``,
``<style>``, ``<svg>`` and a whole ``<!DOCTYPE html>`` page became tag-named XML sections. The
allow-list answers "which tags may the markdown sanitizer keep"; this list answers "is this tag
real HTML".

THE ORDER every reader applies to a line-leading ``<…``: a code fence owns its bytes; then real
HTML (a document or a non-allow-list element is an ``html`` block, ``<svg>`` an ``svg`` block — the
blocks a fenced ``html`` / ``svg`` makes; an allow-list tag stays text); then a built-in Matrx tag;
only then an unknown tag is a custom section. No name is both here and a Matrx tag.

MARKUP, NOT A WORD: a bare HTML-named tag around plain words (``<output>{…}</output>``,
SHAPES-BUGS 2.2) is a wrapper, not markup, and stays a custom section. An element is markup when
its root is in ``HTML_MARKUP_ROOTS``, its opener carries attributes, or its inside holds an HTML tag.

SVG and MathML child names (``rect``, ``text``, ``filter``) are deliberately absent: inside their root
they are claimed with it, and as a root they are ordinary words a custom section may use. The shared
html-root vectors (rich-content ``__tests__/html-root-vectors.json``) pin this list to the TS one.
"""

from __future__ import annotations

import re
from typing import Literal

HTML_ELEMENT_NAMES: frozenset[str] = frozenset(
    {
        # WHATWG HTML Living Standard (element index).
        "a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo",
        "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code", "col", "colgroup",
        "data", "datalist", "dd", "del", "details", "dfn", "dialog", "div", "dl", "dt", "em", "embed",
        "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head",
        "header", "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "label", "legend",
        "li", "link", "main", "map", "mark", "menu", "meta", "meter", "nav", "noscript", "object", "ol",
        "optgroup", "option", "output", "p", "param", "picture", "pre", "progress", "q", "rp", "rt",
        "ruby", "s", "samp", "script", "search", "section", "select", "slot", "small", "source", "span",
        "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea",
        "tfoot", "th", "thead", "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr",
        # Obsolete but still parsed by browsers and still written by models.
        "acronym", "applet", "basefont", "big", "blink", "center", "dir", "font", "frame", "frameset",
        "marquee", "menuitem", "nobr", "noembed", "noframes", "plaintext", "rb", "rtc", "strike", "tt",
        "xmp",
        # Foreign-content roots.
        "svg", "math",
    }
)

HtmlRootKind = Literal["document", "svg", "fragment"]

_DOCTYPE_HTML_RE = re.compile(r"^<!doctype\s+html(?=[\s>])", re.IGNORECASE)
_ROOT_NAME_RE = re.compile(r"^<([A-Za-z][A-Za-z0-9-]*)(?=[\s/>]|$)")


def is_html_element_name(name: str) -> bool:
    """The tag is a real HTML element (or the ``<svg>`` / ``<math>`` root). Case-insensitive."""
    return name.lower() in HTML_ELEMENT_NAMES


def is_html_doctype_line(trimmed: str) -> bool:
    """The trimmed line opens a full HTML document with its doctype."""
    return bool(_DOCTYPE_HTML_RE.match(trimmed))


def html_root_of(trimmed: str, allowed_raw_html: frozenset[str]) -> tuple[HtmlRootKind, str] | None:
    """Which HTML root the trimmed line opens (kind, tag as written), or None.

    An allow-list tag returns None: the markdown renderer draws it in place, as it always has.
    Twin of ``htmlRootOf``.
    """
    if is_html_doctype_line(trimmed):
        return ("document", "html")
    match = _ROOT_NAME_RE.match(trimmed)
    if not match:
        return None
    name = match[1]
    lower = name.lower()
    if lower not in HTML_ELEMENT_NAMES or lower in allowed_raw_html:
        return None
    if lower == "html":
        return ("document", name)
    if lower == "svg":
        return ("svg", name)
    return ("fragment", name)


HTML_MARKUP_ROOTS: frozenset[str] = frozenset(
    {
        "html", "head", "body", "svg", "math", "script", "style", "textarea", "xmp", "plaintext",
        "noscript", "iframe", "video", "audio", "canvas", "form", "button", "frameset", "noframes",
        "noembed", "marquee",
    }
)

_OPENER_WITH_ATTRIBUTES_RE = re.compile(r"^<[A-Za-z][A-Za-z0-9-]*\s+[^\s/>]")
_HTML_TAG_ANYWHERE_RE = re.compile(r"</?([A-Za-z][A-Za-z0-9-]*)(?=[\s/>])")


def html_opener_is_markup(trimmed: str) -> bool:
    """The opener alone reads as HTML markup: a markup root, or a tag with attributes."""
    match = _ROOT_NAME_RE.match(trimmed)
    if not match or not is_html_element_name(match[1]):
        return False
    return match[1].lower() in HTML_MARKUP_ROOTS or bool(_OPENER_WITH_ATTRIBUTES_RE.match(trimmed))


def html_element_is_markup(element: str) -> bool:
    """A closed element is HTML markup: its opener is, or its inside holds an HTML-named tag."""
    trimmed = element.lstrip()
    if html_opener_is_markup(trimmed):
        return True
    opener_end = trimmed.find(">")
    if opener_end == -1:
        return False
    closer_start = trimmed.rfind("</")
    inside = trimmed[opener_end + 1 : closer_start] if closer_start > opener_end else trimmed[opener_end + 1 :]
    return any(is_html_element_name(m[1]) for m in _HTML_TAG_ANYWHERE_RE.finditer(inside))
