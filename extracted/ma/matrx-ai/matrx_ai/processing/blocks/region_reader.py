"""The region reader — a markdown block's regions read LIVE, line by line (P1-CHAT T1 v2.1).

``markdown_regions`` (PF-1 D9) reads a markdown block's fenced code blocks and GFM tables once, from
its whole span, when the block closes: that is what the save writes. A ``blocks-v2`` client needs the
same regions WHILE the block streams, so it can draw a code or table face from the server's word and
never parse state from text. This reader produces them incrementally and, by construction and by
property test, EQUALS ``markdown_regions`` on every input:

* The parser is the save's parser (markdown-it-py, CommonMark + GFM tables, block rules only). The
  reader never has a grammar of its own for what IS a region; it only decides when a re-read is needed.
* CommonMark block structure is decided line by line and never revised, with two exceptions that live
  inside the LAST top-level block (a paragraph line becoming a table header on the delimiter row; a
  setext underline). So each re-read starts at the start of the last top-level block (the
  *checkpoint*): every region that ended before it is final.
* A re-read happens only on a new complete line, and only when the unread tail can hold a region
  (it contains ```` ``` ````, ``~~~`` or ``|``). Two hot paths skip the parser entirely: a line inside
  an open fence that cannot close it, and a body row of an open top-level table. Prose never parses.
* A table opens one line late, on its delimiter row (its ``start`` is the header line). Nothing is ever
  retracted: ``region.retract`` stays reserved.
* When the block closes, ``finish`` reads the final span with ``markdown_regions`` itself and reconciles;
  a disagreement (never seen; the property test is the gate) is returned as an anomaly so the caller
  degrades loudly (``blocks.degraded``) instead of drawing something the save will not hold.

Offsets here are UTF-8 bytes into the block's span; the caller rebases them into the part.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from markdown_it.rules_block.table import escapedSplit

from matrx_ai.processing.blocks.markdown_regions import (
    _MD,
    EXTRA_TYPES,
    blocked_lines,
    extra_closed,
    extra_open,
    markdown_regions,
    maybe_extras,
    merge_regions,
)

_LINE_BREAK_RE = re.compile(rb"\r\n|\r|\n")

#: Fence languages the server names as their own region kind (the rest of the code fences are ``code``).
_KIND_BY_LANGUAGE: dict[str, str] = {
    "mermaid": "mermaid",
    "mmd": "mermaid",
    "svg": "svg",
    "html": "html",
    "math": "math",
    "latex": "math",
    "tex": "math",
    "katex": "math",
}
#: Code fence languages a client draws with their own drawer (content-ir ``SPECIAL_CODE_LANGUAGES`` +
#: ``CODE_LANGUAGE_ALIASES``); ``display`` names that drawer. Every other language draws as ``code``.
_DISPLAY_ALIASES: dict[str, str] = {"mmd": "mermaid", "jsx": "react", "tsx": "react", "latex": "math", "tex": "math", "katex": "math"}
_SPECIAL_DISPLAYS: frozenset[str] = frozenset({"mermaid", "svg", "chart", "map", "stats", "diff", "html", "react", "math"})

#: First characters of a line that may END a top-level table (a terminator rule) — a re-read decides.
_TABLE_RISKY_FIRST = frozenset("`~>*-+_#<=0123456789")
#: markdown-it-py's anti-DoS bound on autocompleted table cells (rules_block/table.py).
_MAX_AUTOCOMPLETED = 0x10000


def region_kind_and_display(kind: str, language: str | None) -> tuple[str, str]:
    """``(region_kind, display)`` for a saved region ``type`` and its language — the server's one list."""
    if kind == "table":
        return "table", "table"
    if kind in EXTRA_TYPES:  # display math, a raw svg / html root: the server names them, the client never guesses
        return kind, kind
    lower = (language or "").lower()
    region_kind = _KIND_BY_LANGUAGE.get(lower, "code")
    canonical = _DISPLAY_ALIASES.get(lower, lower)
    display = canonical if canonical in _SPECIAL_DISPLAYS else "code"
    return region_kind, display


def _indent(line: bytes) -> tuple[int, bool]:
    """Leading columns (tabs to the next multiple of 4) and whether a tab was among them."""
    n = 0
    tab = False
    for b in line:
        if b == 0x20:
            n += 1
        elif b == 0x09:
            tab = True
            n += 4 - (n % 4)
        else:
            break
    return n, tab


def _is_blank(line: bytes) -> bool:
    return not line.strip(b" \t\r\n")


@dataclass
class LiveRegion:
    """A region as announced: span offsets in the block, its kind, and where it stands."""

    type: str
    start: int
    language: str | None
    container: list[str] | None
    start_line: int
    end: int | None = None
    complete: bool | None = None
    rows: int = 0

    def key(self) -> tuple[int, str]:
        return (self.start, self.type)


@dataclass
class _Found:
    type: str
    first: int  # absolute line
    last: int  # absolute line (exclusive), parse with the sentinel line
    language: str | None
    container: list[str] | None
    markup: str = ""
    closed: bool | None = None  # math / svg / html: the matching delimiter was read (None: the parser's regions)


@dataclass
class RegionEvents:
    """What one step announced, in order: ``("open", region_ordinal)``, ``("partial", ordinal)``, ``("close", ordinal)``."""

    steps: list[tuple[str, int]] = field(default_factory=list)


def _parse(span: bytes) -> list[Any]:
    return _MD.parse(span.decode("utf-8", errors="replace"))


def _found_regions(tokens: list[Any], offset_line: int, span: bytes | None = None) -> tuple[list[_Found], int]:
    """The regions of one parse (absolute lines) and the first line of its last top-level block.

    ``span`` (the parsed bytes) is given when it can hold math / svg / html: those are read line by line and
    merged with the parser's regions exactly as ``markdown_regions(all_kinds=True)`` does."""
    found: list[_Found] = []
    boxes: list[tuple[int, int, str]] = []
    stack: list[str] = []
    last_top = 0
    last_top_type = ""
    last_item = -1
    for tok in tokens:
        if tok.level == 0 and tok.map is not None and tok.nesting >= 0:
            last_top = tok.map[0]
            last_top_type = tok.type
        elif tok.type == "list_item_open" and tok.level == 1 and tok.map is not None:
            last_item = tok.map[0]
        if tok.nesting == 1 and tok.map is not None and tok.type in ("list_item_open", "blockquote_open"):
            boxes.append((tok.map[0], tok.map[1], "list_item" if tok.type == "list_item_open" else "blockquote"))
        if tok.nesting == 1:
            stack.append(tok.type)
        elif tok.nesting == -1:
            if stack:
                stack.pop()
        if tok.map is None:
            continue
        if tok.type in ("fence", "table_open"):
            container = [
                "list_item" if t == "list_item_open" else "blockquote"
                for t in stack
                if t in ("list_item_open", "blockquote_open")
            ]
            info = tok.info.strip() if tok.type == "fence" else ""
            found.append(
                _Found(
                    type="code" if tok.type == "fence" else "table",
                    first=tok.map[0] + offset_line,
                    last=tok.map[1] + offset_line,
                    language=(info.split()[0] if info else None) if tok.type == "fence" else None,
                    container=container or None,
                    markup=tok.markup if tok.type == "fence" else "",
                )
            )
    # Inside a top-level list, each item of that list is read alone exactly as in context (its own marker sets
    # its indentation; looseness and numbering change no region): the re-read starts at the last item.
    if last_top_type in ("bullet_list_open", "ordered_list_open") and last_item >= last_top:
        last_top = last_item
    if span is not None:
        found = _with_extras(found, tokens, span, offset_line, boxes)
    return found, last_top + offset_line


def _with_extras(
    found: list[_Found], tokens: list[Any], span: bytes, offset_line: int, boxes: list[tuple[int, int, str]]
) -> list[_Found]:
    lines = span.splitlines(True)
    by_first = {f.first - offset_line: f for f in found}
    md = [(f.type, f.first - offset_line, f.last - offset_line, f.language) for f in found]
    merged = merge_regions(lines, md, blocked_lines(tokens, lines), defer_last_pipe=True)
    out: list[_Found] = []
    for kind, first, end, language, closed in merged:
        if kind in EXTRA_TYPES:
            container = [name for lo, hi, name in boxes if lo <= first < hi]
            out.append(
                _Found(
                    type=kind,
                    first=first + offset_line,
                    last=end + offset_line,
                    language=None,
                    container=container or None,
                    closed=closed,
                )
            )
        else:
            out.append(by_first[first])
    return out


class RegionReader:
    """One markdown block's regions, read as its lines arrive. Feed complete lines; ``finish`` at close."""

    def __init__(self) -> None:
        self._buf = bytearray()
        self._starts: list[int] = [0]  # byte start of every line read (+ the next line's start)
        self._pending = b""  # bytes of an unfinished line
        self._check = 0  # checkpoint: first line of the last top-level block
        self._tail_risky = False  # the tail since the checkpoint holds ``` / ~~~ / |
        self._prev_pipe = False  # the previous line held a pipe (this one may be a table's delimiter row)
        self._tail_html = False  # the tail since the checkpoint has a line opening with ``<``
        self._fast: tuple[Any, ...] | None = None
        self._extra: tuple[int, Any] | None = None  # (region ordinal, closer pattern) of an open math / svg / html
        self.regions: list[LiveRegion] = []
        self.anomaly: str | None = None

    # ── public ─────────────────────────────────────────────────────────────────────────

    @property
    def open_regions(self) -> list[tuple[int, LiveRegion]]:
        return [(i, r) for i, r in enumerate(self.regions) if r.end is None]

    def feed(self, data: bytes) -> RegionEvents:
        """Read ``data`` (the block's next bytes, in any chunking); regions move only on complete lines."""
        ev = RegionEvents()
        if not data:
            return ev
        chunk = self._pending + data
        pos = 0
        n = len(chunk)
        while pos < n:
            nl = chunk.find(b"\n", pos)
            if nl < 0:
                break
            line = chunk[pos : nl + 1]
            self._buf += line
            self._starts.append(len(self._buf))
            self._line(line, ev)
            pos = nl + 1
        self._pending = chunk[pos:]
        return ev

    def finish(self, span: bytes, *, cut: bool = False) -> RegionEvents:
        """The block closed with exactly ``span``: reconcile with ``markdown_regions`` (what the save writes).

        Every region still open is closed. ``cut`` (a Stop, or the text ended): an open region closes
        ``complete: false``; otherwise a fence the text ended inside is ``complete: false`` and the rest true.
        """
        ev = RegionEvents()
        # The save drops the line breaks that only separated this block from a reasoning region, so ``span`` can
        # end before a region the live read already closed on its last line break: read up to the span's end.
        for r in self.regions:
            if r.end is not None and r.end > len(span):
                r.end = len(span)
        final = markdown_regions(span, 0, all_kinds=True)
        closed = _closed_flags(span, final)
        by_key = {r.key(): i for i, r in enumerate(self.regions)}
        seen: set[int] = set()
        for fin, was_closed in zip(final, closed, strict=True):
            key = (fin["start"], fin["type"])
            idx = by_key.get(key)
            if idx is None:
                live = LiveRegion(
                    type=fin["type"],
                    start=fin["start"],
                    language=fin["language"],
                    container=None,
                    start_line=-1,
                )
                self.regions.append(live)
                idx = len(self.regions) - 1
                ev.steps.append(("open", idx))
            live = self.regions[idx]
            seen.add(idx)
            if live.language != fin["language"]:
                self.anomaly = self.anomaly or f"region {idx} language {live.language!r} != saved {fin['language']!r}"
            if live.end is None:
                live.end = fin["end"]
                live.complete = (not cut) and was_closed if (live.type == "code" or live.type in EXTRA_TYPES) else not cut
                ev.steps.append(("close", idx))
            elif live.end != fin["end"]:
                self.anomaly = self.anomaly or f"region {idx} closed at {live.end} but the save ends it at {fin['end']}"
        for i, r in enumerate(self.regions):
            if i not in seen:
                self.anomaly = self.anomaly or f"region {i} ({r.type} at {r.start}) is not a saved region"
                if r.end is None:
                    r.end = len(span)
                    r.complete = False
                    ev.steps.append(("close", i))
        return ev

    def as_saved(self) -> list[dict[str, Any]]:
        """The regions in ``markdown_regions``' shape (block-relative), for the property test."""
        return [
            {"type": r.type, "start": r.start, "end": r.end, "language": r.language}
            for r in sorted(self.regions, key=lambda r: r.start)
        ]

    # ── lines ──────────────────────────────────────────────────────────────────────────

    def _line(self, line: bytes, ev: RegionEvents) -> None:
        n = len(self._starts) - 2  # this line's index
        extra = self._extra
        if extra is not None:
            # Inside an open display math / svg / html root every line belongs to it: nothing else is read
            # until the matching delimiter. A fence or table opening in here is no region (the save drops it).
            self._prev_pipe = b"|" in line
            if extra[1].search(line):
                live = self.regions[extra[0]]
                live.end = self._starts[n + 1]
                live.complete = True
                ev.steps.append(("close", extra[0]))
                self._extra = None
                self._reparse(n, ev)
            return
        fast = self._fast
        if fast is not None:
            if fast[0] == "fence" and self._fence_content(line, fast, n, ev):
                return
            if fast[0] == "table" and self._table_row(line, fast, n, ev):
                return
            self._fast = None
        # A region can only START on a line holding a fence marker or a pipe (a table's header), or on the
        # line after a pipe line (a delimiter row may have none); one already open moves on every line.
        # Every other line changes no region: no re-read, only a cheap checkpoint move.
        prev_pipe = self._prev_pipe
        self._prev_pipe = b"|" in line
        stripped = line.lstrip(b" ")
        if stripped[:1] == b"<":
            self._tail_html = True
        risky = self._prev_pipe or b"```" in line or b"~~~" in line or extra_open(line) is not None
        if risky and not prev_pipe and self._top_fence_opener(line, n, ev):
            return
        if risky or prev_pipe or any(r.end is None for r in self.regions):
            self._reparse(n, ev)
            return
        self._cheap_checkpoint(line, n)

    def _top_fence_opener(self, line: bytes, n: int, ev: RegionEvents) -> bool:
        """A fence opener at column 0 right after a blank line surely starts a top-level fence: no re-read.

        After a blank line nothing but an HTML block (types 1-5) carries on, and a column-0 line is inside no
        list item; a fence cannot be a lazy line. Anything else is left to the re-read."""
        if n == 0 or self._tail_html or self._prev_pipe or any(r.end is None for r in self.regions):
            return False
        marker = line[:1]
        if marker not in (b"`", b"~"):
            return False
        prev = bytes(self._buf[self._starts[n - 1] : self._starts[n]])
        if not _is_blank(prev):
            return False
        body = line.rstrip(b"\r\n")
        run = len(body) - len(body.lstrip(marker))
        if run < 3:
            return False
        info = body[run:]
        if marker == b"`" and b"`" in info:
            return False
        words = info.decode("utf-8", errors="replace").strip().split()
        self.regions.append(
            LiveRegion(type="code", start=self._starts[n], language=words[0] if words else None, container=None, start_line=n)
        )
        idx = len(self.regions) - 1
        ev.steps.append(("open", idx))
        self._check = n
        self._fast = ("fence", idx, marker, run, 0, True)
        return True

    def _cheap_checkpoint(self, line: bytes, n: int) -> None:
        """No region possible in the tail: move the checkpoint to a line that surely starts a new block."""
        if n == 0 or self._tail_html or _is_blank(line):
            return
        first = line[:1]
        if first in (b" ", b"\t") or first in b"-*+>0123456789<=_#":
            return
        prev = bytes(self._buf[self._starts[n - 1] : self._starts[n]])
        if _is_blank(prev):
            self._check = n

    def _reparse(self, n: int, ev: RegionEvents) -> None:
        start = self._starts[self._check]
        real_lines = n + 1 - self._check
        span = bytes(self._buf[start:])
        found, last_top = _found_regions(_parse(span), self._check, span if maybe_extras(span) else None)
        by_key = {r.key(): i for i, r in enumerate(self.regions)}
        open_at_end: tuple[int, _Found] | None = None
        for f in found:
            # Closed once a real line follows that is not inside it (a fence that closes ON the last line
            # is announced closed with the next line; the top-level fence fast path closes it at once).
            closed = f.last - self._check < real_lines
            key = (self._starts[f.first], f.type)
            idx = by_key.get(key)
            if idx is None:
                self.regions.append(
                    LiveRegion(
                        type=f.type,
                        start=self._starts[f.first],
                        language=f.language,
                        container=f.container,
                        start_line=f.first,
                    )
                )
                idx = len(self.regions) - 1
                by_key[key] = idx
                ev.steps.append(("open", idx))
            live = self.regions[idx]
            if live.end is not None:
                continue
            if f.type == "table":
                rows = max(0, min(f.last, n + 1) - f.first - 2)
                if rows > live.rows:
                    live.rows = rows
                    ev.steps.append(("partial", idx))
            if f.closed is not None:
                closed = f.closed
            if closed:
                live.end = self._starts[min(f.last, n + 1)]
                live.complete = True
                ev.steps.append(("close", idx))
            else:
                open_at_end = (idx, f)
        # Every region the reread did not find again was before the checkpoint (final) — or an anomaly.
        for i, r in enumerate(self.regions):
            if r.end is None and r.start >= start and all((self._starts[f.first], f.type) != r.key() for f in found):
                self.anomaly = self.anomaly or f"open region {i} vanished on re-read"
        # Inside an open root the checkpoint stays: its lines are swallowed unread, the close re-reads it whole.
        # Nor into the inside of a closed root: a tail starting there would read what the root swallowed.
        inside_root = any(f.type in EXTRA_TYPES and f.first < last_top < f.last for f in found)
        if last_top > self._check and not inside_root and not (open_at_end is not None and open_at_end[1].type in EXTRA_TYPES):
            self._check = min(last_top, n + 1)
        self._tail_risky = self._tail_has_risk()
        self._tail_html = self._tail_has_html()
        self._extra = None
        if open_at_end is not None:
            idx, f = open_at_end
            if f.type in EXTRA_TYPES:
                self._fast = None
                opener = extra_open(bytes(self._buf[self._starts[f.first] : self._starts[f.first + 1]]))
                if opener is not None:
                    self._extra = (idx, opener[1])
            else:
                self._fast = self._fast_for(idx, f)

    def _tail_has_risk(self) -> bool:
        tail = bytes(self._buf[self._starts[self._check] :])
        return b"```" in tail or b"~~~" in tail or b"|" in tail

    def _tail_has_html(self) -> bool:
        tail = bytes(self._buf[self._starts[self._check] :])
        return any(ln.lstrip(b" ")[:1] == b"<" for ln in tail.split(b"\n"))

    def _fast_for(self, idx: int, f: _Found) -> tuple[Any, ...] | None:
        container = f.container or []
        if "blockquote" in container:
            return None
        opener = bytes(self._buf[self._starts[f.first] : self._starts[f.first + 1]])
        if b"\t" in opener:
            return None
        if f.type == "code":
            marker = f.markup[:1].encode()
            col = opener.find(marker)
            if col < 0:
                return None
            return ("fence", idx, marker, len(f.markup), col, not container)
        if container:
            return None
        header = bytes(self._buf[self._starts[f.first] : self._starts[f.first + 1]])
        columns = _cells(header)
        rows_lines = range(f.first + 2, len(self._starts) - 1)
        auto = 0
        for ln in rows_lines:
            auto += columns - _cells(bytes(self._buf[self._starts[ln] : self._starts[ln + 1]]))
        return ("table", idx, columns, auto)

    def _fence_content(self, line: bytes, fast: tuple[Any, ...], n: int, ev: RegionEvents) -> bool:
        _, idx, marker, length, col, top = fast
        indent, tab = _indent(line)
        if tab:
            return False
        body = line[indent:]
        if top:
            if indent < 4 and body[:1] == marker:
                run = len(body) - len(body.lstrip(marker))
                if run >= length and not body[run:].strip(b" \t\r\n"):
                    live = self.regions[idx]
                    live.end = self._starts[n + 1]
                    live.complete = True
                    ev.steps.append(("close", idx))
                    self._fast = None
                    self._check = n + 1
                    self._tail_risky = False
                    self._tail_html = False
                    return True
            return True
        if _is_blank(line):
            return True
        if indent == col and body[:1] == marker:
            # At the opener's own column the closing fence is never 4+ columns past the item's content
            # indent (the opener was not), so a marker run as long as the opener's closes it.
            run = len(body) - len(body.lstrip(marker))
            if run >= length and not body[run:].strip(b" \t\r\n"):
                live = self.regions[idx]
                live.end = self._starts[n + 1]
                live.complete = True
                ev.steps.append(("close", idx))
                self._fast = None
                return True
            return False
        return indent >= col and body[:1] != marker

    def _table_row(self, line: bytes, fast: tuple[Any, ...], n: int, ev: RegionEvents) -> bool:
        _, idx, columns, auto = fast
        live = self.regions[idx]
        if _is_blank(line):
            live.end = self._starts[n]
            live.complete = True
            ev.steps.append(("close", idx))
            self._fast = None
            self._check = n
            self._tail_risky = False
            self._tail_html = False
            return True
        first = line[:1]
        if first in (b" ", b"\t") or first.decode("latin-1") in _TABLE_RISKY_FIRST:
            return False
        auto += columns - _cells(line)
        if auto > _MAX_AUTOCOMPLETED:
            return False
        self._fast = ("table", idx, columns, auto)
        live.rows += 1
        ev.steps.append(("partial", idx))
        return True


def _cells(line: bytes) -> int:
    columns = escapedSplit(line.decode("utf-8", errors="replace").strip())
    if columns and columns[0] == "":
        columns.pop(0)
    if columns and columns[-1] == "":
        columns.pop()
    return len(columns)


def _line_count(span: bytes) -> int:
    breaks = len(_LINE_BREAK_RE.findall(span))
    ends_with_break = span.endswith(b"\n") or span.endswith(b"\r")
    return breaks if ends_with_break else breaks + 1


def _closed_flags(span: bytes, final: list[dict[str, Any]]) -> list[bool]:
    """Per final region: False for a code fence whose last line is not a closing fence (the text ended in it)."""
    out: list[bool] = []
    for r in final:
        if r["type"] in EXTRA_TYPES:
            out.append(extra_closed(span[r["start"] : r["end"]]))
            continue
        if r["type"] != "code":
            out.append(True)
            continue
        body = span[r["start"] : r["end"]]
        lines = body.splitlines()
        if len(lines) < 2:
            out.append(False)
            continue
        opener = lines[0].lstrip(b" \t>")
        # the opener may sit after a list marker on the same line
        opener = opener.lstrip(b"-*+0123456789.) \t")
        marker = opener[:1]
        run = len(opener) - len(opener.lstrip(marker)) if marker in (b"`", b"~") else 0
        last = lines[-1].lstrip(b" \t>")
        close_run = len(last) - len(last.lstrip(marker)) if marker else 0
        out.append(run >= 3 and close_run >= run and not last[close_run:].strip())
    return out


__all__ = ["LiveRegion", "RegionEvents", "RegionReader", "region_kind_and_display"]
