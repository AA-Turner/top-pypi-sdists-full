"""Blocks v1 — the server's one reading of an assistant text part (CGU-14).

The model's text is never changed. This module returns a ``blocks`` list that tiles the text
in order with no gaps; ``text_utf8[start:end]`` is each block's source (offsets are UTF-8 bytes).
The same code reads a whole text at once and a stream chunk by chunk, so a streamed reply and
the saved reply always carry identical blocks.

Grammar v1 (plan: common-docs/systems/chat/projects/chat-ground-up/server-blocks-plan.md §4.1; rulings:
common-docs/systems/chat/projects/chat-ground-up/CGU-14.md §2):

* ``markdown`` — everything not lifted below; parsed by the client's standard CommonMark/GFM. Once the
  text ends it carries ``regions``: its fenced code blocks and GFM tables (``markdown_regions``, PF-1 D9).
* ``reasoning`` — ``<think>`` / ``<thinking>`` / ``<reasoning>`` regions, and the grounded-JSON digest: a
  text whose first non-blank line is the heading ``GROUNDED_DIGEST_HEADING`` (``schema/answer_contract.py``,
  any ``#`` level or ``**bold**`` form) is working text up to its ``json`` fence — one ``reasoning`` block,
  ``tag`` ``digest``, body after the heading line; the fence and what follows read as today.
* ``kind`` — a ``__kind`` JSON object (or an array whose first element is one), bare or in a
  ``json`` / ``jsonc`` / ``json5`` / ``matrx`` / unlabelled fence.
* ``artifact`` — ``<artifact …>…</artifact>``.
* ``decision`` — ``<decision attr="…">…</decision>`` (bare ``<decision>`` is never lifted).
* ``protocol`` — a registered agent-protocol tag (:data:`PROTOCOL_TAGS`).
* ``data`` — never read from text: made at save time from a structured-output run.

A structure is lifted only when it OPENS a line (≤ 3 spaces of indent) outside a fence, front
matter and an HTML ``<details>`` element. Splitting is syntax only; whether a kind is
registered and valid is the separate :func:`validate_kind_block` pass, run when a block closes.

Every line is read once (linear); a line is read only when its newline has arrived, and a
candidate structure is held only until its first key is read, so v1 never retracts a block.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_graph.content_ir.blank_kind import report_blank_kind_string

from matrx_ai.processing.blocks.fence_nesting import (
    classify_inner_fence_line,
    fence_nests_inner_fences,
    parse_fence_opener,
    trim_fence_line,
)
from matrx_ai.processing.blocks.markdown_regions import markdown_regions
from matrx_ai.schema.answer_contract import GROUNDED_DIGEST_HEADING

BLOCKS_VERSION = 1

# The saved shape owns the vocabulary (chat.message text parts, PF-1).
from matrx_connect.context.reply_blocks import BlockType  # noqa: E402

#: Tags whose region is model reasoning written inline in the text.
REASONING_TAGS: frozenset[str] = frozenset({"think", "thinking", "reasoning"})

#: THE agent-protocol tag registry (owned by CGU-14). Tag → the kind it maps to once one is
#: registered for it (``None`` until then). Adding a tag is additive and keeps v1.
PROTOCOL_TAGS: dict[str, str | None] = {
    "heartbeat": None,
    "podcast_dialogue": None,
    "speaker_settings": None,
    "image_prompt": None,
}

#: Fence languages whose body may be a kind instance.
KIND_FENCE_LANGUAGES: frozenset[str] = frozenset({"", "json", "jsonc", "json5", "matrx"})

#: ``tag`` of the reasoning block the grounded digest reads as, and the label a v2 client shows for it.
DIGEST_TAG = "digest"
DIGEST_LABEL = "Research notes"
#: The heading line: the contract's token alone, optionally a ``#`` heading, bold / code marks and a colon.
_DIGEST_HEADING_RE = re.compile(
    r"[ ]{0,3}(?:#{1,6}[ \t]+)?[*_`]{0,3}[ \t]*" + re.escape(GROUNDED_DIGEST_HEADING) + r"[ \t]*[*_`]{0,3}[ \t]*:?[ \t]*[*_`]{0,3}[ \t]*"
)
#: Fence languages that end the digest (the contract's ``json`` fence and its kin; a bare fence does not).
_DIGEST_END_LANGUAGES = KIND_FENCE_LANGUAGES - {""}


def is_digest_heading(line: str) -> bool:
    """Is ``line`` the grounded digest's heading (the contract's one token)?"""
    return _DIGEST_HEADING_RE.fullmatch(line.rstrip("\r\n")) is not None


def could_become_digest_heading(pending: str) -> bool:
    """Might the unfinished first line ``pending`` still turn out to be the digest heading? (live: hold it)"""
    t = pending.lstrip(" \t#*_`")
    if not t:
        return True
    if GROUNDED_DIGEST_HEADING.startswith(t):
        return True
    return t.startswith(GROUNDED_DIGEST_HEADING) and all(c in " \t*_`:\r" for c in t[len(GROUNDED_DIGEST_HEADING) :])


#: A held candidate that has not shown its first key by then is markdown.
_HOLD_MAX_CHARS = 512
_HOLD_MAX_LINES = 8

_TAG_OPEN_RE = re.compile(r"<([A-Za-z][A-Za-z0-9_-]*)(\s[^<>]*)?>")
_ATTR_RE = re.compile(r"""([\w:.-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')""")
_FIRST_KEY_RE = re.compile(r'\{\s*"((?:[^"\\]|\\.)*)(")?')
_KIND_SLUG_RE = re.compile(r'\{\s*"__kind"\s*:\s*"((?:[^"\\]|\\.)*)(")?')
_JSON_SIGNIFICANT_RE = re.compile(r'["\\{}\[\]]')
_DETAILS_OPEN_RE = re.compile(r"<details[\s>]", re.IGNORECASE)
_DETAILS_CLOSE_RE = re.compile(r"</details\s*>", re.IGNORECASE)


def _b(text: str) -> int:
    return len(text.encode("utf-8"))


@dataclass
class Block:
    """One block of a text part. ``fields`` holds the per-type members of §4.1."""

    type: BlockType
    start: int
    end: int
    complete: bool = True
    fields: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"type": self.type, "start": self.start, "end": self.end}
        if self.type != "markdown":
            out["complete"] = self.complete
        out.update(self.fields)
        return out


#: A validator takes a closed ``kind`` block and fills status / value / version / errors.
KindValidator = Callable[[Block], None]


def _indent(line: str) -> int:
    n = 0
    for ch in line:
        if ch == " ":
            n += 1
        elif ch == "\t":
            n += 4 - (n % 4)
        else:
            break
    return n


def _attrs(attr_text: str | None) -> dict[str, str]:
    if not attr_text:
        return {}
    return {
        m.group(1): (m.group(2) if m.group(2) is not None else m.group(3))
        for m in _ATTR_RE.finditer(attr_text)
    }


class _JsonScan:
    """Incremental bracket balance over JSON text (strings and escapes respected)."""

    __slots__ = ("depth", "in_string", "escaped")

    def __init__(self) -> None:
        self.depth = 0
        self.in_string = False
        self.escaped = False

    def feed(self, text: str, start: int = 0) -> int | None:
        """Feed ``text[start:]``; return the index just past the closing bracket, or None."""
        i = start
        n = len(text)
        while i < n:
            if self.escaped:
                self.escaped = False
                i += 1
                continue
            m = _JSON_SIGNIFICANT_RE.search(text, i)
            if m is None:
                return None
            i = m.start()
            ch = text[i]
            if self.in_string:
                if ch == "\\":
                    self.escaped = True
                elif ch == '"':
                    self.in_string = False
            elif ch == '"':
                self.in_string = True
            elif ch in "{[":
                self.depth += 1
            elif ch in "}]":
                self.depth -= 1
                if self.depth == 0:
                    return i + 1
            i += 1
        return None


def _first_key_verdict(body: str) -> tuple[Literal["kind", "no", "wait"], str | None, bool]:
    """Read a candidate's opening: is it a ``__kind`` object (or array of them)?

    Returns ``(verdict, slug, is_array)``.
    """
    s = _skip_leading_comments(body.lstrip())
    if s is None:
        return "wait", None, False
    if not s:
        return "wait", None, False
    is_array = False
    if s[0] == "[":
        is_array = True
        s = s[1:].lstrip()
        if not s:
            return "wait", None, True
    if s[0] != "{":
        return "no", None, is_array
    rest = s[1:].lstrip()
    if not rest:
        return "wait", None, is_array
    if rest[0] != '"':
        return "no", None, is_array
    m = _FIRST_KEY_RE.match(s)
    if m is None or m.group(2) is None:
        return "wait", None, is_array
    if _normalize_key(m.group(1)) != "__kind":
        return "no", None, is_array
    km = _KIND_SLUG_RE.match(s, 0) if m.group(1) == "__kind" else _KIND_SLUG_RE.match('{"__kind"' + s[m.end():])
    if km is None:
        # `"__kind"` read, the colon / value not yet: wait unless something else is there.
        tail = s[m.end():].lstrip()
        if not tail or tail == ":" or (tail.startswith(":") and not tail[1:].strip()):
            return "wait", None, is_array
        return "no", None, is_array
    if km.group(2) is None:
        return "wait", None, is_array
    slug = km.group(1).strip()
    if not slug:
        return "no", None, is_array
    return "kind", slug, is_array


_ZERO_WIDTH = dict.fromkeys(map(ord, "\u200b\u200c\u200d\u2060\ufeff"), None)


def _normalize_key(raw: str) -> str:
    """A first key as a model spells it: JSON escapes decoded, ``\\_`` and zero-width characters dropped."""
    key = raw.replace("\\_", "_").translate(_ZERO_WIDTH)
    if "\\" in key:
        try:
            key = json.loads(f'"{key}"')
        except (json.JSONDecodeError, ValueError):
            return key
    return key


def _skip_leading_comments(s: str) -> str | None:
    """Skip JSONC ``//`` lines and ``/* */`` comments before a body's first value; None = still open."""
    while s.startswith("//") or s.startswith("/*"):
        if s.startswith("//"):
            nl = s.find("\n")
            if nl < 0:
                return None
            s = s[nl + 1 :].lstrip()
        else:
            close = s.find("*/")
            if close < 0:
                return None
            s = s[close + 2 :].lstrip()
    return s


@dataclass
class _Hold:
    origin: Literal["bare", "fence"]
    lines: list[str]
    start: int  # byte offset of the first held line
    ticks: int = 0
    language: str = ""


@dataclass
class _Open:
    """The lifted block being read."""

    block: Block
    mode: Literal["bare", "fence", "tag", "digest"]
    source: list[str]
    scan: _JsonScan | None = None
    ticks: int = 0
    closer: str = ""
    body_start: int = 0
    value: Any = None
    parsed: bool = False


_DECODER = json.JSONDecoder()


def _decode_at(line: str, start: int) -> tuple[Any, int] | None:
    """One C-speed parse of a JSON value starting at ``line[start]``: ``(value, end)`` or None."""
    try:
        return _DECODER.raw_decode(line, start)
    except (json.JSONDecodeError, ValueError):
        return None


class BlocksV1Splitter:
    """Feed text in any chunking; read events and the final blocks.

    ``feed(chunk)`` and ``finish()`` return ``block.open`` / ``block.close`` events (plain
    dicts, typed on the wire by the stream contract); ``finish()`` ends with one ``block.regions``
    event per markdown block (PF-1 D9). ``blocks`` is the list so far.
    """

    def __init__(self, *, validate: KindValidator | None = None, fence_after_tag: bool = False) -> None:
        self._validate = validate
        # v2 only (blocks2 / LiveBlocksStreamV2): a fence right after a tag close is a fence. v1 `blocks` (www) never.
        self._fence_after_tag = fence_after_tag
        self._pending = ""
        self._pos = 0  # byte offset of the next unread line
        self._source = bytearray()  # every complete line read so far (a markdown block's regions)
        self._blocks: list[Block] = []
        self._events: list[dict[str, Any]] = []
        self._md: Block | None = None
        self._open: _Open | None = None
        self._hold: _Hold | None = None
        self._fence: tuple[int, bool, int] | None = None  # (ticks, nests, nested depth)
        self._front_matter: str | None = None
        self._details = 0
        self._first_line = True
        self._seen_text = False  # a non-blank line has been read (the digest heading is only the FIRST one)
        self._finished = False

    # ── public ──────────────────────────────────────────────────────────────────────────

    @property
    def blocks(self) -> list[Block]:
        return self._blocks

    @property
    def seen_text(self) -> bool:
        """True once a non-blank line has been read: the digest heading can no longer open the text."""
        return self._seen_text

    @property
    def in_open_fence(self) -> bool:
        """True while the reading sits inside a markdown code fence (after ``finish``: the text ended in one)."""
        return self._fence is not None

    def open_kind_source(self) -> tuple[int, str, str | None] | None:
        """The OPEN ``kind`` block's ``(index, JSON source read so far, slug)``, or None (live partials, P1-CHAT T1b)."""
        op = self._open
        if op is None or op.block.type != "kind" or not op.source:
            return None
        source = "".join(op.source)
        _verdict, slug, _array = _first_key_verdict(source)
        return len(self._blocks) - 1, source, slug

    def feed(self, chunk: str) -> list[dict[str, Any]]:
        if self._finished:
            raise RuntimeError("BlocksV1Splitter.feed after finish")
        if not chunk:
            return []
        data = self._pending + chunk
        start = 0
        while True:
            nl = data.find("\n", start)
            if nl < 0:
                break
            self._line(data[start : nl + 1])
            start = nl + 1
        self._pending = data[start:]
        return self._drain()

    def finish(self) -> list[dict[str, Any]]:
        if self._finished:
            return []
        self._finished = True
        if self._pending:
            self._line(self._pending)
            self._pending = ""
        if self._hold is not None:
            self._release_hold()
        if self._open is not None:
            self._close_open(self._pos, complete=False)
        self._close_md(self._pos)
        self._read_regions()
        return self._drain()

    def _read_regions(self) -> None:
        """PF-1 D9: each markdown block's regions, read once from its whole closed span at the end of
        the text — never on the token path (a GFM parse is ≈130 ns/char) — and announced as one
        ``block.regions`` event per markdown block, so a stream and a one-shot read end identical."""
        source = bytes(self._source)
        self._source = bytearray()
        for index, block in enumerate(self._blocks):
            if block.type != "markdown":
                continue
            regions = markdown_regions(source[block.start : block.end], block.start)
            block.fields["regions"] = regions
            self._events.append({"event": "block.regions", "index": index, "regions": regions})

    # ── events ──────────────────────────────────────────────────────────────────────────

    def _drain(self) -> list[dict[str, Any]]:
        events, self._events = self._events, []
        return events

    def _open_block(self, block: Block) -> None:
        self._blocks.append(block)
        self._events.append(
            {"event": "block.open", "index": len(self._blocks) - 1, "type": block.type, "start": block.start}
        )

    def _close_block(self, block: Block) -> None:
        index = len(self._blocks) - 1
        self._events.append({"event": "block.close", "index": index, "end": block.end, "block": block.to_dict()})

    def _md_text(self, start: int, end: int) -> None:
        if end <= start:
            return
        if self._md is None:
            self._md = Block(type="markdown", start=start, end=end)
            self._open_block(self._md)
        else:
            self._md.end = end

    def _close_md(self, at: int) -> None:
        if self._md is not None:
            self._md.end = at
            self._close_block(self._md)
            self._md = None

    # ── lines ───────────────────────────────────────────────────────────────────────────

    def _line(self, line: str) -> None:
        self._source += line.encode("utf-8")
        if self._open is not None:
            self._continue_open(line, 0)
        elif self._hold is not None:
            self._continue_hold(line)
        else:
            self._md_line(line)

    def _open_digest(self, line: str) -> None:
        """The grounded digest: working text from its heading up to the ``json`` fence, one ``reasoning`` block."""
        start = self._pos
        self._close_md(start)
        block = Block(type="reasoning", start=start, end=start, complete=False, fields={"tag": DIGEST_TAG})
        self._open_block(block)
        self._pos += _b(line)
        block.end = self._pos
        self._open = _Open(block=block, mode="digest", source=[], body_start=self._pos)

    def _advance(self, line: str) -> int:
        start = self._pos
        self._pos += _b(line)
        return start

    def _md_line(self, line: str) -> None:
        first = self._first_line
        self._first_line = False
        if not self._seen_text and line.strip():
            self._seen_text = True
            if is_digest_heading(line):
                self._open_digest(line)
                return
        if first:
            opener = line.lstrip("\ufeff").rstrip("\r\n")
            if opener in ("---", "+++"):
                self._front_matter = opener
                start = self._advance(line)
                self._md_text(start, self._pos)
                return
        if self._front_matter is not None:
            body = line.rstrip("\r\n")
            if body == self._front_matter or (self._front_matter == "---" and body == "..."):
                self._front_matter = None
            start = self._advance(line)
            self._md_text(start, self._pos)
            return
        if self._fence is not None:
            ticks, nests, depth = self._fence
            verdict = classify_inner_fence_line(trim_fence_line(line), ticks, nests, depth)
            if verdict == "close-outer":
                self._fence = None
            elif verdict == "open-nested":
                self._fence = (ticks, nests, depth + 1)
            elif verdict == "close-nested":
                self._fence = (ticks, nests, depth - 1)
            start = self._advance(line)
            self._md_text(start, self._pos)
            return
        if _indent(line) <= 3:
            s = line.lstrip(" \t")
            if s.startswith("```"):
                fence = parse_fence_opener(line)
                if fence is not None:
                    ticks, language = fence
                    if language.lower() in KIND_FENCE_LANGUAGES:
                        self._hold = _Hold("fence", [line], self._pos, ticks, language)
                        self._pos += _b(line)
                        return
                    self._fence = (ticks, fence_nests_inner_fences(language), 0)
            elif s[:1] in ("{", "["):
                self._hold = _Hold("bare", [line], self._pos)
                self._pos += _b(line)
                self._decide_hold()
                return
            elif s.startswith("<") and self._try_tag(line, s):
                return
        if "<" in line:
            self._details += len(_DETAILS_OPEN_RE.findall(line)) - len(_DETAILS_CLOSE_RE.findall(line))
            if self._details < 0:
                self._details = 0
        start = self._advance(line)
        self._md_fragment(line, 0, start)

    def _md_fragment(self, line: str, offset: int, line_start: int) -> None:
        """Commit ``line[offset:]`` as markdown, lifting each complete same-line ``__kind`` object.

        Mid-line kinds (after prose, in a quote, adjacent roots) are lifted only when the whole
        object is on this line and parses as JSON — decided once the line is complete, so the
        reading never changes later. Positions inside an inline code span stay text.
        """
        if '"__kind"' not in line or (offset == 0 and _indent(line) > 3):
            self._md_text(line_start + _b(line[:offset]), line_start + _b(line))
            return
        cursor = offset
        for start, end, value in _same_line_kinds(line, offset):
            if not line[end:].strip():
                end = len(line)
            self._md_text(line_start + _b(line[:cursor]), line_start + _b(line[:start]))
            k_start = line_start + _b(line[:start])
            k_end = line_start + _b(line[:end])
            self._close_md(k_start)
            block = Block(type="kind", start=k_start, end=k_end, complete=False, fields={})
            self._open_block(block)
            self._open = _Open(block=block, mode="bare", source=[line[start:end]], value=value, parsed=True)
            self._close_open(k_end, complete=True)
            cursor = end
        self._md_text(line_start + _b(line[:cursor]), line_start + _b(line))

    # ── tags ────────────────────────────────────────────────────────────────────────────

    def _try_tag(self, line: str, stripped: str) -> bool:
        m = _TAG_OPEN_RE.match(stripped)
        if m is None:
            return False
        name = m.group(1)
        lower = name.lower()
        attr_text = m.group(2)
        if attr_text and attr_text.rstrip().endswith("/"):
            return False
        fields: dict[str, Any]
        if lower in REASONING_TAGS:
            block_type: BlockType = "reasoning"
            fields = {"tag": lower}
        elif lower == "artifact":
            block_type = "artifact"
            a = _attrs(attr_text)
            fields = {
                "artifact_id": a.get("id"),
                "version": a.get("version"),
                "artifact_type": a.get("type"),
                "title": a.get("title"),
                "attributes": a,
            }
        elif lower == "decision":
            a = _attrs(attr_text)
            if not a:
                return False
            block_type = "decision"
            fields = {"attributes": a}
        elif lower in PROTOCOL_TAGS:
            if self._details > 0:
                return False
            block_type = "protocol"
            fields = {"tag": lower, "kind": PROTOCOL_TAGS[lower], "attributes": _attrs(attr_text)}
        else:
            return False
        start = self._pos
        self._close_md(start)
        block = Block(type=block_type, start=start, end=start, complete=False, fields=fields)
        self._open_block(block)
        offset_in_line = (len(line) - len(stripped)) + m.end()
        self._open = _Open(
            block=block,
            mode="tag",
            source=[],
            closer=f"</{lower}",
            body_start=start + _b(line[:offset_in_line]),
        )
        self._continue_open(line, offset_in_line)
        return True

    # ── holds (a candidate kind whose first key has not been read) ──────────────────────

    def _continue_hold(self, line: str) -> None:
        hold = self._hold
        assert hold is not None
        hold.lines.append(line)
        self._pos += _b(line)
        if hold.origin == "fence":
            ticks = hold.ticks
            if classify_inner_fence_line(trim_fence_line(line), ticks, False, 0) == "close-outer":
                # The fence closed before its first key was read: decide on the whole body now.
                verdict, _, _ = _first_key_verdict("".join(hold.lines[1:-1]))
                if verdict == "kind":
                    self._confirm_hold()
                else:
                    self._release_hold()
                return
        self._decide_hold()

    def _hold_body(self, hold: _Hold) -> str:
        return "".join(hold.lines[1:]) if hold.origin == "fence" else "".join(hold.lines)

    def _decide_hold(self) -> None:
        hold = self._hold
        assert hold is not None
        body = self._hold_body(hold)
        verdict, _slug, _arr = _first_key_verdict(body)
        if verdict == "kind":
            self._confirm_hold()
        elif verdict == "no" or len(body) > _HOLD_MAX_CHARS or len(hold.lines) > _HOLD_MAX_LINES:
            self._release_hold()

    def _release_hold(self) -> None:
        """The candidate is markdown: replay its lines through the markdown reader."""
        hold = self._hold
        assert hold is not None
        self._hold = None
        self._pos = hold.start
        first, rest = hold.lines[0], hold.lines[1:]
        if hold.origin == "fence":
            self._fence = (hold.ticks, fence_nests_inner_fences(hold.language), 0)
        start = self._advance(first)
        self._md_text(start, self._pos)
        for line in rest:
            if self._hold is not None:
                self._continue_hold(line)
            elif self._open is not None:
                self._continue_open(line, 0)
            else:
                self._md_line(line)

    def _confirm_hold(self) -> None:
        hold = self._hold
        assert hold is not None
        self._hold = None
        self._close_md(hold.start)
        block = Block(type="kind", start=hold.start, end=hold.start, complete=False, fields={})
        self._open_block(block)
        self._pos = hold.start
        if hold.origin == "fence":
            self._open = _Open(block=block, mode="fence", source=[], ticks=hold.ticks)
            self._pos += _b(hold.lines[0])
            block.end = self._pos
            lines = hold.lines[1:]
        else:
            self._open = _Open(block=block, mode="bare", source=[], scan=_JsonScan())
            lines = hold.lines
        for i, line in enumerate(lines):
            if self._open is None:
                # Closed mid-way: the rest of the held lines are ordinary lines again.
                for rest in lines[i:]:
                    self._line(rest)
                return
            self._continue_open(line, 0)

    # ── lifted blocks ───────────────────────────────────────────────────────────────────

    def _continue_open(self, line: str, offset: int) -> None:
        """Read ``line[offset:]`` (the part of the line not yet consumed) into the open block."""
        op = self._open
        assert op is not None
        line_start = self._pos
        if op.mode == "digest":
            if _indent(line) <= 3:
                fence = parse_fence_opener(line)
                if fence is not None and fence[1].lower() in _DIGEST_END_LANGUAGES:
                    # The digest ends where the json fence begins; the fence line is read as any line.
                    self._close_open(line_start, complete=True)
                    self._md_line(line)
                    return
            self._pos += _b(line)
            op.block.end = self._pos
            return
        if op.mode == "fence":
            if classify_inner_fence_line(trim_fence_line(line), op.ticks, False, 0) == "close-outer":
                self._pos += _b(line)
                op.block.end = self._pos
                self._close_open(self._pos, complete=True)
                return
            op.source.append(line)
            self._pos += _b(line)
            op.block.end = self._pos
            return
        if op.mode == "bare":
            assert op.scan is not None
            begin = offset
            if not op.source and op.scan.depth == 0:
                begin = offset + (len(line) - offset - len(line[offset:].lstrip(" \t")))
                decoded = _decode_at(line, begin)
                if decoded is not None and isinstance(decoded[0], (dict, list)):
                    op.value, end = decoded
                    op.parsed = True
                    op.source.append(line[begin:end])
                    self._finish_mid_line(line, end, line_start)
                    return
            end = op.scan.feed(line, begin)
            if end is None:
                op.source.append(line[begin:])
                self._pos += _b(line)
                op.block.end = self._pos
                return
            op.source.append(line[begin:end])
            self._finish_mid_line(line, end, line_start)
            return
        # tag
        lower_line = line.lower()
        idx = lower_line.find(op.closer, offset)
        while idx >= 0:
            after = idx + len(op.closer)
            close_gt = line.find(">", after)
            if close_gt >= 0 and not line[after:close_gt].strip():
                op.source.append(line[offset:idx])
                op.block.fields["body_end"] = line_start + _b(line[:idx])
                self._finish_mid_line(line, close_gt + 1, line_start)
                return
            idx = lower_line.find(op.closer, after)
        op.source.append(line[offset:])
        self._pos += _b(line)
        op.block.end = self._pos

    def _finish_mid_line(self, line: str, end: int, line_start: int) -> None:
        """The open block closed at ``line[end]``: trailing blank goes with it, the rest is markdown."""
        rest = line[end:]
        if not rest.strip():
            self._pos = line_start + _b(line)
            self._close_open(self._pos, complete=True)
            return
        cut = line_start + _b(line[:end])
        mode = self._open.mode if self._open is not None else None
        self._close_open(cut, complete=True)
        self._seen_text = True  # the text after the closed block, on its own line, is not the part's first line
        if self._fence_after_tag and mode == "tag" and rest.lstrip(" \t").startswith(("```", "~~~")):
            # A tag block (`</thinking>`) closed mid-line and a fence opens right after it: the fence is the start of the
            # next line, whole — never a stray "```json" fragment left in markdown beside the kind it holds.
            self._pos = cut
            self._md_line(rest)
            return
        self._pos = line_start + _b(line)
        self._md_fragment(line, end, line_start)

    def _close_open(self, end: int, *, complete: bool) -> None:
        op = self._open
        assert op is not None
        self._open = None
        block = op.block
        block.end = end
        block.complete = complete
        if block.type == "reasoning":
            # The text after a reasoning region is a new text part (the save lifts the region out): its first
            # non-blank line may be the digest heading again.
            self._seen_text = False
        if op.mode in ("tag", "digest"):
            block.fields["body_start"] = op.body_start
            block.fields.setdefault("body_end", end)
            if block.type == "decision" and complete:
                block.fields["questions"] = _decision_questions("".join(op.source), block.fields["attributes"])
        else:
            _fill_kind(block, "".join(op.source), complete, op.value if op.parsed else _UNPARSED)
            if self._validate is not None:
                self._validate(block)
        self._close_block(block)


def _inline_code_mask(line: str) -> list[tuple[int, int]]:
    """Spans of inline code (backtick runs matched by equal-length runs) on one line."""
    spans: list[tuple[int, int]] = []
    i = 0
    n = len(line)
    while i < n:
        j = line.find("`", i)
        if j < 0:
            break
        k = j
        while k < n and line[k] == "`":
            k += 1
        run = line[j:k]
        close = line.find(run, k)
        while close >= 0 and close + len(run) < n and line[close + len(run)] == "`":
            close = line.find(run, close + len(run) + 1)
        if close < 0:
            i = k
            continue
        spans.append((j, close + len(run)))
        i = close + len(run)
    return spans


def _same_line_kinds(line: str, offset: int) -> list[tuple[int, int, Any]]:
    """Every complete ``{"__kind": …}`` object starting at or after ``offset`` and ending on this line."""
    found: list[tuple[int, int, Any]] = []
    masks = _inline_code_mask(line) if "`" in line else []
    for opener, closer in (("<!--", "-->"), ("<![CDATA[", "]]>")):
        i = line.find(opener)
        while i >= 0:
            j = line.find(closer, i + len(opener))
            end = len(line) if j < 0 else j + len(closer)
            masks.append((i, end))
            i = line.find(opener, end)
    pos = offset
    while True:
        j = line.find("{", pos)
        if j < 0:
            return found
        if any(a <= j < b for a, b in masks):
            pos = j + 1
            continue
        verdict, _slug, _arr = _first_key_verdict(line[j:])
        if verdict != "kind":
            pos = j + 1
            continue
        decoded = _decode_at(line, j)
        if decoded is None or not isinstance(decoded[0], dict):
            pos = j + 1
            continue
        value, end = decoded
        found.append((j, end, value))
        pos = end


def _decision_questions(inner: str, attributes: dict[str, str]) -> list[dict[str, Any]]:
    from matrx_ai.processing.blocks.parsers.decision_parser import parse_decision

    parsed = parse_decision(inner, attributes)
    if parsed is None:
        return []
    return [parsed.model_dump(by_alias=False)]


def _normalize_kind_key(value: Any) -> Any:
    """A value whose first key is a misspelt ``__kind`` gets the key as registered (value only)."""
    if not isinstance(value, dict) or "__kind" in value or not value:
        return value
    first = next(iter(value))
    if _normalize_key(first) != "__kind":
        return value
    return {("__kind" if k == first else k): v for k, v in value.items()}


_UNPARSED = object()


def _fill_kind(block: Block, source: str, complete: bool, parsed: Any = _UNPARSED) -> None:
    """Syntax-level kind fields: the value as written, the slug(s), array-ness — a pure function of the text."""
    value: Any = None
    errors: list[str] = []
    status = "unchecked"
    if not complete:
        status = "incomplete"
        errors.append("unterminated")
    elif parsed is not _UNPARSED:
        value = parsed
    else:
        try:
            value = json.loads(source)
        except (json.JSONDecodeError, ValueError):
            from matrx_ai.processing.blocks.parsers._llm_json import loads_block_json

            value = loads_block_json(source)
            if value is None:
                status = "invalid"
                errors.append("json: does not parse")
    items: list[dict[str, Any]] | None = None
    if isinstance(value, list):
        value = [_normalize_kind_key(v) for v in value]
        is_array = True
        slugs = [v.get("__kind") if isinstance(v, dict) else None for v in value]
        items = [{"kind": s if isinstance(s, str) else None} for s in slugs]
        slug = slugs[0] if slugs and all(x == slugs[0] for x in slugs) and isinstance(slugs[0], str) else None
    elif value is not None:
        value = _normalize_kind_key(value)
        is_array = False
        slug = value.get("__kind") if isinstance(value, dict) else None
        report_blank_kind_string("blocks_v1.slug_of_value", slug)
        slug = slug if isinstance(slug, str) else None
    else:
        verdict, first, is_array = _first_key_verdict(source)
        # A cut-off array's later elements are unknown, so it names no kind.
        slug = first if verdict == "kind" and not is_array else None
    block.fields.update(
        {
            "kind": slug,
            "kind_version": None,
            "array": is_array,
            "value": value,
            "status": status,
            "errors": errors,
        }
    )
    if items is not None:
        block.fields["items"] = items


# ── validation (the separate pass, R2) ─────────────────────────────────────────────────


@dataclass(frozen=True)
class KindRegistryView:
    """What validation needs from the kind registry: schema and version per slug."""

    schema: Callable[[str], dict[str, Any] | None]
    version: Callable[[str], int | None]
    known: Callable[[str], bool]
    warm: Callable[[], bool]


def catalog_registry() -> KindRegistryView:
    """The process's kind catalog (``kind_catalog``) as a registry view."""
    from matrx_ai.processing.blocks import kind_catalog

    return KindRegistryView(
        schema=kind_catalog.registered_kind_schema,
        version=kind_catalog.registered_kind_version,
        known=kind_catalog.is_registered_kind,
        warm=kind_catalog.snapshot_is_warm,
    )


def kind_validator(registry: KindRegistryView | None = None) -> KindValidator:
    """A validator bound to a registry (default: the process catalog)."""

    def validate(block: Block) -> None:
        validate_kind_block(block, registry or catalog_registry())

    return validate


def validate_kind_block(block: Block, registry: KindRegistryView) -> None:
    """Fill ``status`` / ``kind_version`` / ``errors`` / repaired ``value`` on a closed kind block.

    Validation offers, never blocks: an invalid kind keeps its block with its errors. The text
    is never touched; a repair rewrites only ``value``.
    """
    f = block.fields
    if f.get("status") in ("invalid", "incomplete"):
        return
    if not registry.warm():
        f["status"] = "unchecked"
        f["errors"] = ["kind registry not loaded"]
        return
    from matrx_ai.processing.blocks.kind_correctors import correct_kind_value

    value = f.get("value")
    items = value if isinstance(value, list) else [value]
    results: list[dict[str, Any]] = []
    out_items: list[Any] = []
    for item in items:
        status, slug, version, errors, corrected = _validate_one(item, registry, correct_kind_value)
        results.append({"kind": slug, "kind_version": version, "status": status, "errors": errors})
        out_items.append(corrected)
    if any(r["status"] == "repaired" for r in results):
        f["value"] = out_items if isinstance(value, list) else out_items[0]
    statuses = {r["status"] for r in results}
    if f.get("array"):
        slugs = {r["kind"] for r in results}
        f["kind"] = slugs.pop() if len(slugs) == 1 else None
        f["items"] = results
        f["kind_version"] = results[0]["kind_version"] if f["kind"] else None
        f["errors"] = [f"[{i}] {e}" for i, r in enumerate(results) for e in r["errors"]]
    else:
        f["kind_version"] = results[0]["kind_version"]
        f["errors"] = results[0]["errors"]
    for status in ("invalid", "unknown_kind", "repaired", "valid"):
        if status in statuses:
            f["status"] = status
            break


def _validate_one(
    item: Any, registry: KindRegistryView, correct: Callable[[Any], tuple[Any, list[str]]]
) -> tuple[str, str | None, int | None, list[str], Any]:
    slug = item.get("__kind") if isinstance(item, dict) else None
    report_blank_kind_string("blocks_v1.classify_item", slug)
    if not isinstance(slug, str) or not slug.strip():
        return "invalid", None, None, ["no __kind"], item
    if not registry.known(slug):
        return "unknown_kind", slug, None, [f"unregistered kind {slug!r}"], item
    corrected, notes = correct(item)
    errors: list[str] = []
    schema = registry.schema(slug)
    if schema is not None:
        from matrx_graph.executor.schema_validation import validate_instance

        errors = list(validate_instance(schema, corrected, retrieve=_sibling_kind_schemas(registry))[:20])
    status = "invalid" if errors else ("repaired" if notes else "valid")
    return status, slug, registry.version(slug), errors, corrected


def _sibling_kind_schemas(registry: KindRegistryView) -> Callable[[str], dict[str, Any] | None]:
    """Resolve a kind schema's ``$ref`` to another registered kind (``<slug>.schema.json``)."""
    from matrx_graph.input_declaration import SCHEMA_BASE_URI

    def retrieve(uri: str) -> dict[str, Any] | None:
        name = uri.rsplit("/", 1)[-1] if uri.startswith(SCHEMA_BASE_URI) or "/" not in uri else ""
        if not name.endswith(".schema.json"):
            return None
        return registry.schema(name.removesuffix(".schema.json"))

    return retrieve


# ── one-shot ───────────────────────────────────────────────────────────────────────────


def split_blocks_v1(text: str, *, validate: KindValidator | None = None, fence_after_tag: bool = False) -> list[Block]:
    """The blocks of one whole text — exactly what a stream of the same text ends with."""
    splitter = BlocksV1Splitter(validate=validate, fence_after_tag=fence_after_tag)
    splitter.feed(text)
    splitter.finish()
    return splitter.blocks


def blocks_v1_dicts(text: str, *, validate: KindValidator | None = None, fence_after_tag: bool = False) -> list[dict[str, Any]]:
    return [b.to_dict() for b in split_blocks_v1(text, validate=validate, fence_after_tag=fence_after_tag)]


__all__ = [
    "BLOCKS_VERSION",
    "KIND_FENCE_LANGUAGES",
    "PROTOCOL_TAGS",
    "REASONING_TAGS",
    "Block",
    "BlocksV1Splitter",
    "KindRegistryView",
    "blocks_v1_dicts",
    "catalog_registry",
    "kind_validator",
    "split_blocks_v1",
    "validate_kind_block",
]
