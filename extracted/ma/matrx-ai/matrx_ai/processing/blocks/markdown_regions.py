"""Regions of a blocks v1 ``markdown`` block — its fenced code blocks and GFM tables (PF-1 D9).

Read by a standard CommonMark + GFM-table parser (markdown-it-py), never by our own grammar:
this is markdown reading, not a second splitter. Called once, when a markdown block closes, on
that block's whole span, so a stream and a one-shot read always agree.

Each region is ``{"type": "code" | "table", "start", "end", "language"}``: UTF-8 byte offsets
into the part's text (like every block). ``start`` is the start of the region's first line (for
a fence or table inside a list item or quote, that line's marker is included); ``end`` is the end
of its last line, line break included, or the span's end. A code region is a fenced block (``````
or ``~~~``), fences included, ``language`` the first word of its info string (``None`` when
empty); an indented code block is not a region. A table region is a GFM table, ``language``
``None``. Nesting follows the parser: a fence inside a ````` ````markdown ````` wrapper is part of
the wrapper's region.
"""

from __future__ import annotations

import re
from typing import Any

from markdown_it import MarkdownIt

# Block rules only: the inline pass reads nothing a region needs.
_MD = MarkdownIt("commonmark").enable("table").disable(["inline", "text_join"])

# The parser's own line breaks (its normalize rule turns \r\n and \r into \n). UTF-8 never
# encodes these bytes inside a multi-byte character, so byte positions are exact.
_LINE_BREAK_RE = re.compile(rb"\r\n|\r|\n")


# ── display math and raw svg / html roots (P1-CHAT T1 v2.1, blocks-v2 only) ─────────────────────────
#
# A blocks-v2 client draws display math, a bare ``<svg>`` and a bare HTML document from the server's
# word, never by detecting them itself. ``markdown_regions(..., all_kinds=True)`` therefore also reads:
#
# * ``math`` — a line that (after container markers ``>`` / ``- `` / ``1. ``) starts with ``$$`` or ``\[``
#   opens it; the first line holding the matching ``$$`` / ``\]`` (the opener's own line counts, after the
#   opener) closes it. Inline ``$…$`` is prose.
# * ``svg`` / ``html`` — a line starting with ``<svg``, ``<html`` or ``<!doctype html`` opens it; the first line
#   holding ``</svg>`` / ``</html>`` closes it (blank lines inside do not end it).
#
# A root is read line by line, whatever the CommonMark block structure says: a fence or table that starts
# INSIDE one belongs to it (dropped), an opener inside a fence, a table, indented code or a non-root HTML block is
# not an opener. An unclosed one runs to the span's end. Their ``type`` is ``math`` / ``svg`` / ``html``,
# ``language`` ``None``. The default read (``all_kinds=False``) is the saved contract, ``code`` | ``table`` only.

EXTRA_TYPES = ("math", "svg", "html")

_EXTRA_OPEN_RE = re.compile(
    rb"^[ \t]*(?:>[ \t]*)*(?:(?:[-*+]|\d{1,9}[.)])[ \t]+)*(\$\$|\\\[|<svg(?=[\s/>]|$)|<html(?=[\s/>]|$)|<!doctype html)",
    re.IGNORECASE,
)
_CLOSERS: dict[str, re.Pattern[bytes]] = {
    "$$": re.compile(rb"\$\$"),
    "\\[": re.compile(rb"\\\]"),
    "<svg": re.compile(rb"</svg\s*>", re.IGNORECASE),
    "<html": re.compile(rb"</html\s*>", re.IGNORECASE),
}


def extra_open(line: bytes) -> tuple[str, re.Pattern[bytes], int] | None:
    """``(type, closer, offset after the opener)`` when ``line`` opens display math / a raw svg or html root."""
    if b"<" not in line and b"$$" not in line and b"\\[" not in line:
        return None
    m = _EXTRA_OPEN_RE.match(line)
    if m is None:
        return None
    word = m.group(1).lower()
    if word == b"$$":
        return "math", _CLOSERS["$$"], m.end(1)
    if word == b"\\[":
        return "math", _CLOSERS["\\["], m.end(1)
    if word == b"<svg":
        return "svg", _CLOSERS["<svg"], m.end(1)
    return "html", _CLOSERS["<html"], m.end(1)


def maybe_extras(span: bytes) -> bool:
    """Cheap gate: can ``span`` hold math or a raw svg / html root at all?"""
    if b"$$" in span or b"\\[" in span:
        return True
    low = span.lower()
    return b"<svg" in low or b"<html" in low or b"<!doctype html" in low


def merge_regions(
    lines: list[bytes],
    md: list[tuple[str, int, int, str | None]],
    blocked: bytearray,
    *,
    defer_last_pipe: bool = False,
) -> list[tuple[str, int, int, str | None, bool]]:
    """Merge the parser's fenced-code and table regions (``type, first line, end line, language``) with the
    line-read math / svg / html regions, in document order: ``(type, first, end, language, closed)``.

    ``blocked`` marks lines no opener may start on (indented code, a non-root HTML block). A parser region
    that starts inside an extra region is dropped. ``defer_last_pipe`` (the live reader, a line still arriving):
    an opener on the LAST line that holds a ``|`` is not read yet — it may turn out to be a table header.
    """
    n = len(lines)
    out: list[tuple[str, int, int, str | None, bool]] = []
    ordered = sorted(md, key=lambda r: r[1])
    k = 0
    i = 0
    while i < n:
        while k < len(ordered) and ordered[k][1] < i:
            k += 1
        if k < len(ordered) and ordered[k][1] == i:
            kind, first, end, language = ordered[k]
            out.append((kind, first, end, language, True))
            k += 1
            i = max(end, i + 1)
            continue
        if blocked[i]:
            i += 1
            continue
        op = extra_open(lines[i])
        if op is None:
            i += 1
            continue
        if defer_last_pipe and i == n - 1 and b"|" in lines[i]:
            break
        kind, closer, after = op
        if closer.search(lines[i], after):
            end, closed = i + 1, True
        else:
            end, closed = n, False
            for j in range(i + 1, n):
                if closer.search(lines[j]):
                    end, closed = j + 1, True
                    break
        out.append((kind, i, end, None, closed))
        i = end
    return out


def blocked_lines(tokens: list[Any], lines: list[bytes], offset: int = 0) -> bytearray:
    """Lines (relative to ``lines``) inside indented code or a non-root HTML block of ``tokens``."""
    blocked = bytearray(len(lines))
    for tok in tokens:
        if tok.map is None or tok.type not in ("code_block", "html_block"):
            continue
        first, end = tok.map[0] - offset, tok.map[1] - offset
        if tok.type == "html_block":
            op = extra_open(lines[first]) if 0 <= first < len(lines) else None
            if op is not None and op[0] in ("svg", "html"):
                first += 1
        for ln in range(max(first, 0), min(end, len(lines))):
            blocked[ln] = 1
    return blocked


def extra_closed(body: bytes) -> bool:
    """Is a math / svg / html region's ``body`` (its first line to its end) closed by its matching delimiter?"""
    lines = body.splitlines(True)
    if not lines:
        return False
    op = extra_open(lines[0])
    if op is None:
        return False
    _kind, closer, after = op
    return bool(closer.search(lines[0], after)) or any(closer.search(ln) for ln in lines[1:])


def markdown_regions(span: bytes, base: int, *, all_kinds: bool = False) -> list[dict[str, Any]]:
    """The regions of one markdown block whose UTF-8 source is ``span``, starting at ``base``.

    ``all_kinds`` adds display math and raw svg / html roots (``math`` / ``svg`` / ``html`` types) for blocks-v2:
    the live reader equals this read. The default is the saved contract: ``code`` | ``table`` only."""
    if all_kinds:
        return _regions_all_kinds(span, base)
    if b"```" not in span and b"~~~" not in span and b"|" not in span:
        return []
    tokens = _MD.parse(span.decode("utf-8"))
    found: list[tuple[str, list[int], str | None]] = []
    for tok in tokens:
        if tok.map is None:
            continue
        if tok.type == "fence":
            info = tok.info.strip()
            found.append(("code", tok.map, info.split()[0] if info else None))
        elif tok.type == "table_open":
            found.append(("table", tok.map, None))
    if not found:
        return []
    line_starts = [0]
    line_starts.extend(m.end() for m in _LINE_BREAK_RE.finditer(span))
    total = len(span)

    def at(line: int) -> int:
        return line_starts[line] if line < len(line_starts) else total

    return [
        {
            "type": kind,
            "start": base + at(first),
            "end": base + min(at(last), total),
            "language": language,
        }
        for kind, (first, last), language in found
    ]


def _regions_all_kinds(span: bytes, base: int) -> list[dict[str, Any]]:
    extras = maybe_extras(span)
    if not extras and b"```" not in span and b"~~~" not in span and b"|" not in span:
        return []
    tokens = _MD.parse(span.decode("utf-8"))
    md: list[tuple[str, int, int, str | None]] = []
    for tok in tokens:
        if tok.map is None:
            continue
        if tok.type == "fence":
            info = tok.info.strip()
            md.append(("code", tok.map[0], tok.map[1], info.split()[0] if info else None))
        elif tok.type == "table_open":
            md.append(("table", tok.map[0], tok.map[1], None))
    lines = span.splitlines(True)
    merged = merge_regions(lines, md, blocked_lines(tokens, lines) if extras else bytearray(len(lines)))
    if not merged:
        return []
    line_starts = [0]
    line_starts.extend(m.end() for m in _LINE_BREAK_RE.finditer(span))
    total = len(span)

    def at(line: int) -> int:
        return line_starts[line] if line < len(line_starts) else total

    return [
        {"type": kind, "start": base + at(first), "end": base + min(at(last), total), "language": language}
        for kind, first, last, language, _closed in merged
    ]


__all__ = ["EXTRA_TYPES", "extra_closed", "extra_open", "markdown_regions", "maybe_extras", "merge_regions"]
