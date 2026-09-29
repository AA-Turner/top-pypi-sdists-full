"""PROTECTED REGIONS of stored markdown — the Python twin of THE island rule.

THE rule lives in TypeScript: ``@ai-matrx/content-ir`` ``source/tokenize.ts``
(``listIslands(tokenizeSource(text))``, aidream ``apps/shared/content-ir-core``),
with its helpers ``code-ranges.ts``, ``math.ts``, ``math-pairs.ts``,
``xml-tag.ts``, ``fence-nesting.ts`` and ``constants.ts``. The client editor
locks exactly those islands; a server-side text patch must refuse exactly what
the editor refuses, so this module mirrors the rule and is held to it by
vectors GENERATED from the TypeScript rule
(``apps/shared/content-ir-core/__tests__/source-island-vectors.json``, never
hand-edited) whose byte-identical copy is
``packages/matrx-ai/tests/fixtures/source_island_vectors.json``
(``processing/blocks/tests/test_source_island_vectors.py``).

An ISLAND is an atomic span no editor may parse into its own model: fences,
bare / typed / ``__kind`` JSON, XML regions and containers, raw HTML blocks,
comments and pinned anchors, display math, front matter, trees, directives,
callouts and footnote definitions (block islands), and ``{{variables}}``,
citations, inline math, inline tags, inline kinds, media refs and wikilinks
(inline islands inside a paragraph).

Exactness notes (why this is not "idiomatic" Python):
  - JavaScript strings are UTF-16; every length bound of the rule (400-char
    math, 64-char probes, 200-char variables, …) counts UTF-16 units. The text
    is expanded to UTF-16 units (astral characters become surrogate pairs)
    before the scan, and offsets are mapped back to ``str`` indices at the end.
  - JavaScript ``\\s`` / ``trim()`` / ``\\w`` / ``\\d`` / ``.`` / ``$`` differ
    from Python's; every regex below spells out the JavaScript meaning.
  - Only one-shot (stored-text) tokenizing is ported; the streaming holdbacks
    of the TypeScript tokenizer do not apply to a stored document.

Pure Python, no aidream imports (package boundary). Linear-ish on large input.
"""

from __future__ import annotations

import json
import re
from bisect import bisect_left, bisect_right
from dataclasses import dataclass

from matrx_ai.processing.blocks.fence_nesting import (
    FENCE_OPENER_WHITESPACE,
    classify_inner_fence_line,
    fence_nests_inner_fences,
    parse_fence_opener,
    trim_fence_line,
)
from matrx_ai.processing.blocks.gfm_table_lines import is_html_block_tag_name

__all__ = ["SourceIsland", "list_islands", "BLOCK_ISLAND_TYPES", "INLINE_ISLAND_TYPES"]

BLOCK_ISLAND_TYPES: frozenset[str] = frozenset(
    {
        "fence", "json", "xml_region", "xml_attr", "xml_container", "html_block", "html_comment",
        "anchor", "math_block", "front_matter", "tree", "directive", "callout", "footnote_def",
    }
)
INLINE_ISLAND_TYPES: frozenset[str] = frozenset(
    {
        "variable", "cite", "math_inline", "html_tag", "xml_tag", "xml_inline", "html_comment",
        "anchor", "kind_json", "media_ref", "wikilink",
    }
)


@dataclass(frozen=True, slots=True)
class SourceIsland:
    """One protected span. ``start``/``end`` are ``str`` (code-point) offsets."""

    island_type: str
    start: int
    end: int
    inline: bool
    complete: bool
    raw: str


# ─────────────────────────────────────────────────────────────────────────
# JavaScript semantics
# ─────────────────────────────────────────────────────────────────────────

#: ECMAScript WhiteSpace + LineTerminator — JavaScript's ``\s`` and ``trim()``.
_JS_WS = FENCE_OPENER_WHITESPACE
_WS = "\\t\\n\\x0b\\x0c\\r \\xa0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000\\ufeff"
_S = f"[{_WS}]"
_NS = f"[^{_WS}]"
#: JavaScript ``.`` (no ``s`` flag): anything but a line terminator.
_DOT = "[^\\n\\r\\u2028\\u2029]"
_NON_WS_RE = re.compile(_NS)


def _trim(s: str) -> str:
    return s.strip(_JS_WS)


def _trim_start(s: str) -> str:
    return s.lstrip(_JS_WS)


def _trim_end(s: str) -> str:
    return s.rstrip(_JS_WS)


def _is_ws(ch: str) -> bool:
    return ch != "" and ch in _JS_WS


def _to_utf16_units(text: str) -> tuple[str, list[int]]:
    """The text as JavaScript sees it, and the UTF-16 offsets of every astral character."""
    astral: list[int] = []
    if text.isascii() or max(text) < "\U00010000":
        return text, astral
    out: list[str] = []
    u = 0
    for ch in text:
        code = ord(ch)
        if code >= 0x10000:
            astral.append(u)
            code -= 0x10000
            out.append(chr(0xD800 + (code >> 10)) + chr(0xDC00 + (code & 0x3FF)))
            u += 2
        else:
            out.append(ch)
            u += 1
    return "".join(out), astral


# ─────────────────────────────────────────────────────────────────────────
# constants.ts
# ─────────────────────────────────────────────────────────────────────────

XML_TAG_BLOCK_NAMES: tuple[str, ...] = (
    "thinking", "think", "reasoning", "info", "task", "database", "private", "plan", "event",
    "tool", "questionnaire", "flashcards", "cooking_recipe", "timeline", "progress_tracker",
    "troubleshooting", "resources", "research",
)
THINKING_FAMILY: tuple[str, ...] = ("thinking", "think", "reasoning")
ATTRIBUTE_XML_NAMES: tuple[str, ...] = ("decision", "artifact", "editor_error", "editor_code_snippet", "audiocite")
KNOWN_XML_TAG_NAMES: frozenset[str] = frozenset(XML_TAG_BLOCK_NAMES + ATTRIBUTE_XML_NAMES)
ALLOWED_RAW_HTML_TAGS: frozenset[str] = frozenset(
    {
        "img", "a", "br", "hr", "span", "p", "strong", "b", "em", "i", "u", "s", "del", "ins", "sup",
        "sub", "mark", "kbd", "abbr", "small", "code", "pre", "ul", "ol", "li", "blockquote", "h1",
        "h2", "h3", "h4", "h5", "h6", "table", "thead", "tbody", "tfoot", "tr", "th", "td", "caption",
        "colgroup", "col", "figure", "figcaption", "details", "summary",
    }
)
HTML_BLOCK_LEVEL_TAGS: frozenset[str] = frozenset(
    {
        "p", "hr", "ul", "ol", "li", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "table",
        "thead", "tbody", "tfoot", "tr", "th", "td", "caption", "colgroup", "col", "figure",
        "figcaption", "details", "summary",
    }
)
TYPED_JSON_ROOT_KEYS: frozenset[str] = frozenset(
    {"quiz_title", "presentation", "decision_tree", "comparison", "diagram", "math_problem", "item_presentation", "name"}
)
#: ``key in TYPED_JSON_ROOT_KEYS`` in JavaScript also finds Object.prototype's members.
_OBJECT_PROTOTYPE_KEYS: frozenset[str] = frozenset(
    {
        "constructor", "__defineGetter__", "__defineSetter__", "hasOwnProperty", "__lookupGetter__",
        "__lookupSetter__", "isPrototypeOf", "propertyIsEnumerable", "toString", "valueOf",
        "__proto__", "toLocaleString",
    }
)
CALLOUT_NAMES: frozenset[str] = frozenset(
    {
        "note", "seealso", "example", "tip", "hint", "important", "warning", "warn", "attention",
        "caution", "danger", "error", "failure", "fail", "missing", "bug", "info", "abstract",
        "summary", "tldr", "todo", "success", "check", "done", "question", "help", "faq", "quote",
        "cite",
    }
)

_TREE_GLYPHS = re.compile("[├└│┌┐┘┬┴┤┼─]")
_PINNED_ANCHOR = re.compile(r"<!--@a:[A-Za-z0-9_-]+-->")
_CITE = re.compile(f'<matrxcite{_S}+n="[0-9]+"{_S}*/>')
_DIRECTIVE_OPEN = re.compile(r"(:{2,})([A-Za-z][A-Za-z0-9_-]*)")
_DIRECTIVE_CLOSE = re.compile(f"(:{{3,}}){_S}*\\Z")
_MKDOCS_OPEN = re.compile(r"(!!!|\?\?\?\+?)[ \t]+([A-Za-z][A-Za-z0-9_-]*)")
_CALLOUT_OPEN = re.compile(r">[ \t]*\[!([A-Za-z][A-Za-z0-9_-]*)\]")
_FOOTNOTE_DEF = re.compile(f"\\[\\^[^\\]{_WS}]+\\]:")
_INDENTED = re.compile(r"(?: {4}|\t)")
_QUOTE_LINE = re.compile(r" {0,3}>")
_LIST_CONTINUATION = re.compile(r"[ \t]*(?:[-*+]|[0-9]{1,9}[.)])[ \t]")
_HEADING = re.compile(f"#{{1,6}}{_S}")
_SPLITTER_TREE_LINE = re.compile(f"[{_WS}│|]*[├└+|][{_WS}─\\-]+")
_GENERIC_XML_PREFIX = re.compile(f"<([A-Za-z_][A-Za-z0-9_.:-]*)(?={_S}|/|\\Z)")
_FIRST_JSON_KEY = re.compile(f'\\{{{_S}*"([^"]+)"')
_KIND_PROBE = re.compile(f'\\{{{_S}*"')
_TOML_SHAPED = re.compile(f'{_S}*(?:[A-Za-z0-9_."-]+{_S}*=|\\[|#)')
_YAML_SHAPED = re.compile(f"(?:[A-Za-z0-9_\"'-][^:]*:(?:{_S}|\\Z)|{_S}+{_NS}|-{_S}|#)")
_PRE_CLOSER = re.compile(f"</[pP][rR][eE]{_S}*>")
_BRACKETS = re.compile(r"[\[\]]")
_MEDIA_REF_PREFIXES: tuple[str, ...] = ("[Image URL:", "[Video URL:", "[Audio URL:")
#: The characters at which the inline scanner does anything; every other character is skipped.
_INLINE_SPECIAL = re.compile(r"[\\`${\[!<]")


# ─────────────────────────────────────────────────────────────────────────
# JSON.parse (strict, iterative — no recursion limit)
# ─────────────────────────────────────────────────────────────────────────

_JSON_WS = re.compile(r"[ \t\n\r]*")
_JSON_STRING = re.compile(r'"(?:[^"\\\x00-\x1f]|\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4}))*"')
_JSON_NUMBER = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?")
_JSON_LITERALS = ("true", "false", "null")


def _json_parse(src: str) -> tuple[bool, object]:
    """``JSON.parse(src)``: ``(ok, top_level___kind_or_None)`` — the kind only when the top is an object."""
    n = len(src)
    pos = _JSON_WS.match(src, 0).end()
    stack: list[str] = []  # "{" or "["
    top_kind: object = None
    top_is_object = False
    expect_value = True
    pending_kind_key = False
    while True:
        if expect_value:
            if pos >= n:
                return False, None
            ch = src[pos]
            if pending_kind_key and ch != '"':
                top_kind = None  # a later non-string ``__kind`` wins, as in JSON.parse
                pending_kind_key = False
            if ch == "{" or ch == "[":
                if not stack:
                    top_is_object = ch == "{"
                stack.append(ch)
                pos = _JSON_WS.match(src, pos + 1).end()
                closer = "}" if ch == "{" else "]"
                if pos < n and src[pos] == closer:
                    stack.pop()
                    pos += 1
                    pending_kind_key = False
                elif ch == "{":
                    ok, pos, is_kind = _json_key(src, pos)
                    if not ok:
                        return False, None
                    pending_kind_key = is_kind and len(stack) == 1
                    continue
                else:
                    continue
            elif ch == '"':
                m = _JSON_STRING.match(src, pos)
                if not m:
                    return False, None
                if pending_kind_key:
                    top_kind = json.loads(m.group(0))
                pos = m.end()
            elif ch == "-" or "0" <= ch <= "9":
                m = _JSON_NUMBER.match(src, pos)
                if not m:
                    return False, None
                pos = m.end()
            else:
                for lit in _JSON_LITERALS:
                    if src.startswith(lit, pos):
                        pos += len(lit)
                        break
                else:
                    return False, None
            pending_kind_key = False
            expect_value = False
            continue
        # after a value
        pos = _JSON_WS.match(src, pos).end()
        if not stack:
            if pos != n:
                return False, None
            return True, (top_kind if top_is_object else None)
        if pos >= n:
            return False, None
        ch = src[pos]
        if ch == ",":
            pos = _JSON_WS.match(src, pos + 1).end()
            if stack[-1] == "{":
                ok, pos, is_kind = _json_key(src, pos)
                if not ok:
                    return False, None
                pending_kind_key = is_kind and len(stack) == 1
            expect_value = True
            continue
        if (ch == "}" and stack[-1] == "{") or (ch == "]" and stack[-1] == "["):
            stack.pop()
            pos += 1
            continue
        return False, None


def _json_key(src: str, pos: int) -> tuple[bool, int, bool]:
    """Read ``"key" :`` at ``pos``; returns (ok, position of the value, key is ``__kind``)."""
    m = _JSON_STRING.match(src, pos)
    if not m:
        return False, pos, False
    raw = m.group(0)
    is_kind = raw == '"__kind"' or ("\\" in raw and json.loads(raw) == "__kind")
    pos = _JSON_WS.match(src, m.end()).end()
    if pos >= len(src) or src[pos] != ":":
        return False, pos, False
    pos = _JSON_WS.match(src, pos + 1).end()
    return True, pos, is_kind


# ─────────────────────────────────────────────────────────────────────────
# xml-tag.ts
# ─────────────────────────────────────────────────────────────────────────


def _xml_name_start(ch: str) -> bool:
    return ch != "" and (("A" <= ch <= "Z") or ("a" <= ch <= "z") or ch == "_")


def _xml_name_char(ch: str) -> bool:
    return ch != "" and (
        ("A" <= ch <= "Z") or ("a" <= ch <= "z") or ("0" <= ch <= "9") or ch in "_.:-"
    )


@dataclass(slots=True)
class _XmlTag:
    tag_name: str
    length: int
    is_closing: bool
    is_self_closing: bool


def _read_xml_tag(content: str, start: int, find=None) -> _XmlTag | None:
    n = len(content)

    def at(k: int) -> str:
        return content[k] if k < n else ""

    cursor = start + 1
    is_closing = at(cursor) == "/"
    if is_closing:
        cursor += 1
    if not _xml_name_start(at(cursor)):
        return None
    name_start = cursor
    while _xml_name_char(at(cursor)):
        cursor += 1
    tag_name = content[name_start:cursor]
    if is_closing:
        while _is_ws(at(cursor)):
            cursor += 1
        if at(cursor) != ">":
            return None
        return _XmlTag(tag_name, cursor + 1 - start, True, False)
    while cursor < n:
        while _is_ws(at(cursor)):
            cursor += 1
        c = at(cursor)
        if c == ">":
            return _XmlTag(tag_name, cursor + 1 - start, False, False)
        if c == "/":
            cursor += 1
            while _is_ws(at(cursor)):
                cursor += 1
            if at(cursor) != ">":
                return None
            return _XmlTag(tag_name, cursor + 1 - start, False, True)
        if not _xml_name_start(c):
            return None
        while _xml_name_char(at(cursor)):
            cursor += 1
        while _is_ws(at(cursor)):
            cursor += 1
        if at(cursor) != "=":
            return None
        cursor += 1
        while _is_ws(at(cursor)):
            cursor += 1
        quote = at(cursor)
        if quote != '"' and quote != "'":
            return None
        cursor += 1
        value_end = find(quote, cursor) if find is not None else content.find(quote, cursor)
        if value_end == -1:
            return None
        cursor = value_end + 1
    return None


def _is_escaped_backtick(line: str, offset: int) -> bool:
    slashes = 0
    i = offset - 1
    while i >= 0 and line[i] == "\\":
        slashes += 1
        i -= 1
    return slashes % 2 == 1


class _XmlContainerTracker:
    """Balances ONE unknown root tag line by line (xml-tag.ts ``XmlContainerTracker``)."""

    def __init__(self, root_tag: str) -> None:
        self.root_tag = root_tag
        self.depth = 0
        self.in_comment = False
        self.in_cdata = False
        self.inline_ticks = 0
        self.fence: _FenceReader | None = None

    def consume_line(self, line: str, start_offset: int = 0) -> int | None:
        if self.fence is not None:
            if self.fence.feed(line):
                self.fence = None
            return None
        if not self.in_comment and not self.in_cdata and self.inline_ticks == 0:
            opener = _fence_opener_of(line)
            if opener is not None:
                self.fence = _FenceReader(opener)
                return None
        n = len(line)
        i = start_offset
        while i < n:
            if self.inline_ticks > 0:
                if line[i] == "`":
                    end = i
                    while end < n and line[end] == "`":
                        end += 1
                    if end - i == self.inline_ticks:
                        self.inline_ticks = 0
                    i = end
                    continue
                i += 1
                continue
            if self.in_comment:
                end = line.find("-->", i)
                if end == -1:
                    return None
                self.in_comment = False
                i = end + 3
                continue
            if self.in_cdata:
                end = line.find("]]>", i)
                if end == -1:
                    return None
                self.in_cdata = False
                i = end + 3
                continue
            if line.startswith("<!--", i):
                self.in_comment = True
                i += 4
                continue
            if line.startswith("<![CDATA[", i):
                self.in_cdata = True
                i += 9
                continue
            ch = line[i]
            if ch == "`" and not _is_escaped_backtick(line, i):
                end = i
                while end < n and line[end] == "`":
                    end += 1
                self.inline_ticks = end - i
                i = end
                continue
            if ch != "<":
                i += 1
                continue
            tag = _read_xml_tag(line, i)
            if tag is None:
                i += 1
                continue
            tag_end = i + tag.length
            if tag.tag_name == self.root_tag:
                if tag.is_closing:
                    self.depth -= 1
                elif not tag.is_self_closing:
                    self.depth += 1
                if self.depth == 0:
                    return tag_end
            i = tag_end
        return None


# ─────────────────────────────────────────────────────────────────────────
# code-ranges.ts
# ─────────────────────────────────────────────────────────────────────────

_TILDE_OPEN = re.compile(f"(~{{3,}})({_DOT}*)\\Z")


@dataclass(frozen=True, slots=True)
class _FenceOpener:
    char: str
    ticks: int
    lang: str


def _fence_opener_of(content: str) -> _FenceOpener | None:
    t = _trim_start(content)
    if t.startswith("```"):
        parsed = parse_fence_opener(t)
        if parsed is None:
            return None
        return _FenceOpener("`", parsed[0], parsed[1])
    if len(content) - len(t) <= 3 and t.startswith("~~~"):
        m = _TILDE_OPEN.match(t)
        if not m:
            return None
        info = _trim(m.group(2))
        lang = re.split(_S, info, maxsplit=1)[0] if info else ""
        return _FenceOpener("~", len(m.group(1)), lang)
    return None


def _json_string_state(line: str, start: int, up_to: int, in_string: bool, escaped: bool) -> tuple[bool, bool]:
    for idx in range(start, up_to):
        ch = line[idx]
        if escaped:
            escaped = False
            continue
        if ch == "\\" and in_string:
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
    return in_string, escaped


def _backtick_run_length(s: str, pos: int) -> int:
    n = 0
    size = len(s)
    while pos + n < size and s[pos + n] == "`":
        n += 1
    return n


class _FenceReader:
    """THE closer rule, read line by line (code-ranges.ts ``FenceReader``)."""

    def __init__(self, opener: _FenceOpener, nesting: bool | None = None) -> None:
        self.opener = opener
        self.in_string = False
        self.escaped = False
        self.depth = 0
        self.saw_nested = False
        self.is_json = opener.char == "`" and opener.lang == "json"
        self.nesting = opener.char == "`" and (fence_nests_inner_fences(opener.lang) if nesting is None else nesting)
        self.tilde_closer = re.compile(f" {{0,3}}~{{{opener.ticks},}}[ \\t]*\\Z") if opener.char == "~" else None

    def feed(self, line: str) -> bool:
        if self.tilde_closer is not None:
            return self.tilde_closer.match(line) is not None
        trimmed = trim_fence_line(line)
        at = line.find("```")
        if at == -1:
            if self.is_json:
                self.in_string, self.escaped = _json_string_state(line, 0, len(line), self.in_string, self.escaped)
            return False
        if self.is_json:
            probe = _json_string_state(line, 0, at, self.in_string, self.escaped)
            if probe[0]:
                self.in_string, self.escaped = _json_string_state(line, at, len(line), probe[0], probe[1])
                return False
        if trimmed.startswith("```"):
            kind = classify_inner_fence_line(trimmed, self.opener.ticks, self.nesting, self.depth)
            if kind == "close-outer":
                return True
            if kind == "open-nested":
                self.depth += 1
                self.saw_nested = True
            if kind == "close-nested":
                self.depth -= 1
        else:
            close_ticks = _backtick_run_length(line, at)
            after = trim_fence_line(line[at + close_ticks :])
            if close_ticks >= self.opener.ticks and after == "" and self.depth == 0:
                return True
        if self.is_json:
            self.in_string, self.escaped = _json_string_state(line, 0, len(line), self.in_string, self.escaped)
        return False


def _read_fence(count: int, line_of, open_line: int, reader: _FenceReader) -> tuple[int, bool]:
    for k in range(open_line + 1, count):
        line = line_of(k)
        if line is None:
            return k - 1, False
        if reader.feed(line):
            return k, True
    return count - 1, False


def _close_fence(count: int, line_of, open_line: int, opener: _FenceOpener) -> tuple[int, bool]:
    """Where the fence opened on line ``open_line`` ends: ``(line, closed)``."""
    reader = _FenceReader(opener)
    line, closed = _read_fence(count, line_of, open_line, reader)
    if closed or not reader.saw_nested or reader.depth <= 0:
        return line, closed
    return _read_fence(count, line_of, open_line, _FenceReader(opener, nesting=False))


_QUOTE_PREFIX = re.compile(r" {0,3}> ?")
_LIST_ITEM = re.compile(r"( *)([-*+]|[0-9]{1,9}[.)])( +|\t|\Z)")


def _quote_prefix(line: str) -> tuple[int, int]:
    depth = 0
    offset = 0
    while True:
        m = _QUOTE_PREFIX.match(line, offset)
        if not m:
            return depth, offset
        depth += 1
        offset = m.end()


def _strip_quotes(line: str, depth: int) -> str | None:
    offset = 0
    for _ in range(depth):
        m = _QUOTE_PREFIX.match(line, offset)
        if not m:
            return None
        offset = m.end()
    return line[offset:]


def _leading_spaces(s: str) -> int:
    return len(s) - len(s.lstrip(" "))


class _BacktickRuns:
    """THE code-span pairing table for text[start, stop) (code-ranges.ts ``BacktickRuns``)."""

    __slots__ = ("by_length",)

    def __init__(self, text: str, start: int, stop: int) -> None:
        self.by_length: dict[int, list[int]] = {}
        k = text.find("`", start, stop)
        while k != -1:
            length = 1
            while k + length < stop and text[k + length] == "`":
                length += 1
            self.by_length.setdefault(length, []).append(k)
            k = text.find("`", k + length, stop)

    def next(self, n: int, after: int) -> int:
        lst = self.by_length.get(n)
        if not lst:
            return -1
        i = bisect_left(lst, after)
        return lst[i] if i < len(lst) else -1


def _find_code_ranges(text: str) -> list[tuple[int, int]]:
    """Every code range (fences by the renderer's rule, then inline code spans), sorted by start."""
    starts: list[int] = []
    ends: list[int] = []
    pos = 0
    size = len(text)
    while True:
        nl = text.find("\n", pos)
        line_end = size if nl == -1 else nl
        starts.append(pos)
        ends.append(line_end - 1 if line_end > pos and text[line_end - 1] == "\r" else line_end)
        if nl == -1:
            break
        pos = nl + 1
    count = len(starts)

    def raw(k: int) -> str:
        return text[starts[k] : ends[k]]

    ranges: list[tuple[int, int]] = []
    paragraphs: list[tuple[int, int]] = []

    def prose(start_line: int, stop_line: int) -> None:
        para = -1
        quote_depth = 0
        lists: list[int] = []
        k = start_line
        while k < stop_line:
            line = raw(k)
            depth, offset = _quote_prefix(line)
            if depth != quote_depth:
                quote_depth = depth
                lists = []
            content = line[offset:]
            if _trim(content) == "":
                if para != -1:
                    paragraphs.append((para, starts[k]))
                para = -1
                k += 1
                continue
            indent = _leading_spaces(content)
            while lists and indent < lists[-1]:
                lists.pop()
            item = _LIST_ITEM.match(content)
            column = lists[-1] if lists else 0
            if item:
                gap = len(item.group(3))
                column = len(item.group(1)) + len(item.group(2)) + (gap if 1 <= gap <= 4 else 1)
                lists.append(column)
                content = content[min(column, len(content)) :]
            else:
                content = content[min(indent, column) :]
            opener = _fence_opener_of(content)
            if opener is None:
                if para == -1:
                    para = starts[k]
                k += 1
                continue
            if para != -1:
                paragraphs.append((para, starts[k]))
            para = -1
            col = column
            qdepth = depth

            def line_of(j: int, _opener=opener, _col=col, _depth=qdepth) -> str | None:
                inner = _strip_quotes(raw(j), _depth)
                if inner is None:
                    return None
                if _opener.char == "~" and _col > 0:
                    ind = _leading_spaces(inner)
                    if _trim(inner) != "" and ind < _col:
                        return None
                    return inner[min(ind, _col) :]
                return inner

            end_line, _closed = _close_fence(stop_line, line_of, k, opener)
            ranges.append((starts[k], ends[end_line]))
            k = end_line + 1
        if para != -1:
            paragraphs.append((para, starts[stop_line] if stop_line < count else size))

    segment = 0
    k = 0
    while k < count:
        opener = _fence_opener_of(raw(k))
        if opener is None or opener.char != "`":
            k += 1
            continue
        prose(segment, k)
        end_line, _closed = _close_fence(count, raw, k, opener)
        ranges.append((starts[k], ends[end_line]))
        k = end_line
        segment = k + 1
        k += 1
    prose(segment, count)

    for p_start, p_stop in paragraphs:
        runs: _BacktickRuns | None = None
        i = p_start
        while i < p_stop:
            ch = text[i]
            if ch == "\\":
                i += 2
                continue
            if ch != "`":
                i += 1
                continue
            n = _backtick_run_length(text, i)
            length = min(n, p_stop - i)
            if runs is None:
                runs = _BacktickRuns(text, p_start, p_stop)
            close = runs.next(length, i + length)
            if close == -1:
                i += length
                continue
            ranges.append((i, close + length))
            i = close + length
    ranges.sort(key=lambda r: r[0])
    return ranges


# ─────────────────────────────────────────────────────────────────────────
# math.ts + math-pairs.ts
# ─────────────────────────────────────────────────────────────────────────

_TEX_SIGNAL = re.compile(r"\\[A-Za-z]+|[\\^_{}=<>+]")
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_MATH_SUFFIXES = frozenset({"s", "es", "th", "st", "nd", "rd"})
_FUNCTION_NAMES = frozenset(
    {
        "sin", "cos", "tan", "sec", "csc", "cot", "log", "ln", "exp", "lim", "max", "min", "det",
        "gcd", "mod", "arg", "sinh", "cosh", "tanh",
    }
)
_TEMPLATE_PLACEHOLDER = re.compile(r"\{[A-Za-z_][A-Za-z0-9_.]*\}\Z")
_ARITHMETIC = re.compile(f"\\(\\({_DOT}*\\)\\)\\Z")
_PIPELINE_VAR = re.compile(r"_[.\[]")
_NAME_RUN = re.compile(r"[A-Za-z0-9_]+")
_SEPARATED_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:[.@-]|->|::)\Z")
_PERCENT = re.compile(r"(?:^|[^\\])%")
_BAD_FIRST = re.compile(r"[)\]}\"/]")
_BAD_LAST = re.compile(r"[(\[{\":;,/]\Z")
_CONTRACTION = re.compile(r"[A-Za-z]'[a-z]")
_ABBREVIATION = re.compile(f"(?:^|[{_WS}(,])[A-Za-z]\\.(?:[A-Za-z]\\.|{_S}|\\Z)")
_WORD3 = re.compile(r"[A-Za-z]{3,}")
_PLACEHOLDER_ALL = re.compile(f"[{_WS}.…·⋯_-]*\\Z")
_PLACEHOLDER_ANY = re.compile("[.…·⋯]")
_BRACKET_TEX_SIGNAL = re.compile(
    r"\\[A-Za-z]+|[\^{}=<>+]|_\{|(?:^|[^A-Za-z0-9])[A-Za-z]_[A-Za-z0-9](?![A-Za-z0-9])"
)
_BRACKET_BEFORE = re.compile(r"[A-Za-z0-9_)\]]")
_STRUCTURAL_MARKDOWN = re.compile(
    r"\]\(|https?://|\*\*|(?:^|\n)[ \t]{0,3}#{1,6}[ \t]|(?:^|\n)[ \t]*[-*+][ \t]+|(?:^|\n)[ \t]*[0-9]+[.)][ \t]"
)
_LATEX_COMMAND = re.compile(r"\\[a-zA-Z]")
_BLANK_LINE_INSIDE = re.compile(r"\n[ \t]*\n")
_MAX_MATH_SPAN = 600
_PROSE_WORD_LIMIT = 6
_AFTER_WINDOW = 32


def _is_math_placeholder(inner: str) -> bool:
    return _PLACEHOLDER_ALL.match(inner) is not None and _PLACEHOLDER_ANY.search(inner) is not None


def _is_variable_chain(content: str, after: str | None) -> bool:
    if _TEMPLATE_PLACEHOLDER.match(content):
        return True
    if _ARITHMETIC.match(content) or _PIPELINE_VAR.match(content):
        return True
    if not after:
        return False
    if after[0] == "{":
        return _IDENTIFIER.match(content) is not None
    m = _NAME_RUN.match(after)
    if not m:
        return False
    if len(after) == 1:
        return False
    if _SEPARATED_NAME.match(content):
        return True
    return _IDENTIFIER.match(content) is not None and m.group(0).lower() not in _MATH_SUFFIXES


def _reads_as_prose(content: str) -> bool:
    if _CONTRACTION.search(content):
        return True
    if _ABBREVIATION.search(content):
        return True
    if not any(ch in _JS_WS for ch in content):
        return False
    words = [w for w in _WORD3.findall(content) if w.lower() not in _FUNCTION_NAMES]
    return len(words) >= 2


def _is_single_dollar_math(content: str, after: str | None) -> bool:
    if not content or len(content) > 400:
        return False
    if _is_ws(content[0]) or _is_ws(content[-1]):
        return False
    if after is not None and after[:1].isascii() and after[:1].isdigit():
        return False
    if _is_variable_chain(content, after):
        return False
    if _PERCENT.search(content):
        return False
    if _BAD_FIRST.match(content) or _BAD_LAST.search(content):
        return False
    if "0" <= content[0] <= "9" and after is not None and after[:1].isascii() and after[:1].isalpha():
        return False
    if _is_math_placeholder(content):
        return False
    return _TEX_SIGNAL.search(content) is not None or not _reads_as_prose(content)


def _single_dollar_after(text: str, close: int) -> str:
    rest = text[close + 1 : close + 1 + _AFTER_WINDOW]
    return rest + "\n" if len(rest) < _AFTER_WINDOW else rest


def _single_dollar_math_end(text: str, open_at: int, limit: int) -> int:
    bound = min(limit, open_at + 403)
    close = -1
    k = open_at + 1
    while k < bound:
        c = text[k]
        if c == "\n":
            break
        if c == "\\":
            k += 2
            continue
        if c == "$":
            close = k
            break
        k += 1
    if close == -1 or text[close + 1 : close + 2] == "$":
        return -1
    content = text[open_at + 1 : close]
    return close + 1 if _is_single_dollar_math(content, _single_dollar_after(text, close)) else -1


def _is_escaped_bracket_math(content: str, before: str | None) -> bool:
    if not _trim(content):
        return False
    if before is not None and _BRACKET_BEFORE.match(before):
        return False
    return _BRACKET_TEX_SIGNAL.search(content) is not None


def _opens_flow_block(text: str, open_at: int) -> bool:
    k = open_at - 1
    while k >= 0 and text[k] != "\n":
        if text[k] != " " and text[k] != "\t":
            return False
        k -= 1
    k = open_at + 2
    size = len(text)
    while k < size and text[k] != "\n":
        if text[k] not in " \t\r":
            return False
        k += 1
    return True


def _looks_like_display_math(inner: str, flow: bool) -> bool:
    s = _trim(inner)
    if not s:
        return False
    if _STRUCTURAL_MARKDOWN.search(s):
        return False
    if len(s) > _MAX_MATH_SPAN:
        return False
    if not flow and _BLANK_LINE_INSIDE.search(inner):
        return False
    words = len(_WORD3.findall(s))
    if _LATEX_COMMAND.search(s):
        return words < _PROSE_WORD_LIMIT * 3
    return words < _PROSE_WORD_LIMIT


def _pair_display_math(text: str) -> dict[int, int]:
    """``$$`` opener → closer for every pair the renderer shows as math (math-pairs.ts)."""
    pairs: dict[int, int] = {}
    if "$$" not in text:
        return pairs
    ranges = _find_code_ranges(text)
    tokens: list[int] = []
    r = 0
    max_end = -1
    size = len(text)
    i = text.find("$$")
    while i != -1 and i < size - 1:
        while r < len(ranges) and ranges[r][0] <= i:
            max_end = max(max_end, ranges[r][1])
            r += 1
        if max_end <= i:
            tokens.append(i)
        i = text.find("$$", i + 2)
    j = 0
    while j + 1 < len(tokens):
        open_at = tokens[j]
        close = tokens[j + 1]
        inner = text[open_at + 2 : close]
        if _is_math_placeholder(inner):
            j += 2
            continue
        if _looks_like_display_math(inner, _opens_flow_block(text, open_at)):
            pairs[open_at] = close
            j += 2
            continue
        j += 1
    return pairs


# ─────────────────────────────────────────────────────────────────────────
# tokenize.ts (one-shot)
# ─────────────────────────────────────────────────────────────────────────


@dataclass(slots=True)
class _Raw:
    type: str
    start: int
    end: int
    complete: bool
    from_paragraph: bool = False


@dataclass(slots=True)
class _Block:
    kind: str  # prose | island | gap
    start: int
    end: int
    island: _Raw | None
    inlines: list[_Raw]


def _count_structural_braces(source: str) -> tuple[int, int]:
    if '"' not in source:
        return source.count("{"), source.count("}")
    opens = closes = 0
    in_string = escaped = False
    for ch in source:
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            opens += 1
        elif ch == "}":
            closes += 1
    return opens, closes


def _first_json_key(content: str) -> str | None:
    m = _FIRST_JSON_KEY.match(_trim_start(content))
    return m.group(1) if m else None


def _is_recognized_json_head(content: str) -> bool:
    key = _first_json_key(content)
    if not key:
        return False
    return key in ("__kind", "matrx_version") or key in TYPED_JSON_ROOT_KEYS or key in _OBJECT_PROTOTYPE_KEYS


def _matching_json_object_end(source: str, start: int, limit: int) -> int | None:
    if start >= len(source) or source[start] != "{":
        return None
    stack = ["{"]
    in_string = escaped = False
    for index in range(start + 1, limit):
        ch = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == "{" or ch == "[":
            stack.append(ch)
            continue
        if ch != "}" and ch != "]":
            continue
        opening = stack.pop() if stack else None
        if (ch == "}" and opening != "{") or (ch == "]" and opening != "["):
            return None
        if not stack:
            return index + 1
    return None


def _declared_kind(candidate: str) -> bool:
    ok, kind = _json_parse(candidate)
    return ok and isinstance(kind, str) and _trim(kind) != ""


def _is_unclosed_generic_xml_opening(source: str) -> bool:
    text = _trim_start(source)
    m = _GENERIC_XML_PREFIX.match(text)
    if not m:
        return False
    name = m.group(1)
    if name in KNOWN_XML_TAG_NAMES or name.lower() in ALLOWED_RAW_HTML_TAGS:
        return False
    quote: str | None = None
    for i in range(m.end(), len(text)):
        ch = text[i]
        if quote is not None:
            if ch == quote:
                quote = None
        elif ch == "'" or ch == '"':
            quote = ch
        elif ch == ">":
            return False
    return True


def _is_splitter_tree_line(line: str) -> bool:
    return _TREE_GLYPHS.search(line) is not None or _SPLITTER_TREE_LINE.match(line) is not None


class _Tokenizer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.n = len(text)
        self.line_starts: list[int] = []
        self.content_ends: list[int] = []
        self.line_ends: list[int] = []
        self.blocks: list[_Block] = []
        self.block_cache: dict[tuple[int, bool], _Raw | None] = {}
        self.brace_stop: list[int] | None = None
        self.brace_net: list[int] | None = None
        self.occurrences: dict[str, list[int]] = {}
        self.math_pairs = _pair_display_math(text)
        self.overflow_complete = True
        start = 0
        nl = text.find("\n")
        while nl != -1:
            self.line_starts.append(start)
            self.content_ends.append(nl - 1 if nl > start and text[nl - 1] == "\r" else nl)
            self.line_ends.append(nl + 1)
            start = nl + 1
            nl = text.find("\n", start)
        if start < self.n or self.n == 0:
            self.line_starts.append(start)
            self.content_ends.append(self.n)
            self.line_ends.append(self.n)
        self.line_count = len(self.line_starts)

    # ── helpers ────────────────────────────────────────────────────────

    def next(self, needle: str, start: int) -> int:
        """``text.indexOf(needle, start)`` over a cached occurrence index (linear overall)."""
        lst = self.occurrences.get(needle)
        if lst is None:
            lst = []
            text = self.text
            at = text.find(needle)
            while at != -1:
                lst.append(at)
                at = text.find(needle, at + 1)
            self.occurrences[needle] = lst
        i = bisect_left(lst, start)
        return lst[i] if i < len(lst) else -1

    def line_of(self, pos: int) -> int:
        return max(0, bisect_right(self.line_starts, pos) - 1)

    def is_blank(self, start: int, stop: int) -> bool:
        return _NON_WS_RE.search(self.text, start, stop) is None

    def line_is_blank(self, li: int) -> bool:
        return self.is_blank(self.line_starts[li], self.content_ends[li])

    def line_text(self, li: int) -> str:
        return self.text[self.line_starts[li] : self.content_ends[li]]

    def line_reader(self, k: int) -> str:
        return self.text[self.line_starts[k] : self.content_ends[k]]

    def leading_space(self, start: int, stop: int) -> int:
        k = start
        while k < stop and self.text[k] in _JS_WS:
            k += 1
        return k - start

    # ── driver ─────────────────────────────────────────────────────────

    def run(self) -> list[_Block]:
        pos = 0
        while pos < self.n:
            li = self.line_of(pos)
            ce = self.content_ends[li]
            if self.is_blank(pos, ce):
                pos = self.gap(pos, li)
                continue
            island = self.detect_block(pos, li, True)
            if island is not None:
                self.push(_Block("island", island.start, island.end, island, []))
                pos = island.end
                continue
            pos = self.paragraph(pos, li)
        return self.blocks

    def push(self, block: _Block) -> None:
        if block.end <= block.start:
            return
        if block.kind == "prose" and self.is_blank(block.start, block.end):
            block = _Block("gap", block.start, block.end, None, [])
        if block.kind == "gap" and self.blocks:
            last = self.blocks[-1]
            if last.kind == "gap" and last.end == block.start:
                last.end = block.end
                return
        self.blocks.append(block)

    def gap(self, pos: int, li: int) -> int:
        end = self.line_ends[li]
        k = li + 1
        while k < self.line_count and self.line_is_blank(k):
            end = self.line_ends[k]
            k += 1
        self.push(_Block("gap", pos, end, None, []))
        return end

    # ── block detection ────────────────────────────────────────────────

    def detect_block(self, p: int, li: int, at_para_start: bool) -> _Raw | None:
        key = (p, at_para_start)
        if key in self.block_cache:
            return self.block_cache[key]
        found = self.detect_block_uncached(p, li, at_para_start)
        self.block_cache[key] = found
        return found

    def detect_block_uncached(self, p: int, li: int, at_para_start: bool) -> _Raw | None:
        ce = self.content_ends[li]
        seg = self.text[p:ce]
        t = _trim_start(seg)
        indent = len(seg) - len(t)
        tp = p + indent

        if p == 0:
            fm = self.front_matter(li, t)
            if fm is not None:
                return fm
        list_nested = indent > 0 and self.in_list_continuation(li)
        if indent <= 3 and not list_nested and t.startswith("::"):
            directive = self.directive(p, li, t)
            if directive is not None:
                return directive
        if indent == 0 and (t.startswith("!!!") or t.startswith("???")):
            admonition = self.mkdocs_admonition(p, li, t)
            if admonition is not None:
                return admonition
        if indent <= 3 and not list_nested and t.startswith(">"):
            callout = self.callout(p, li, t)
            if callout is not None:
                return callout
        if at_para_start and indent <= 3 and t.startswith("[^"):
            footnote = self.footnote_definition(p, li, t)
            if footnote is not None:
                return footnote
        fence = _fence_opener_of(seg)
        if fence is not None and fence.char == "`":
            return self.backtick_fence(p, li, fence)
        if fence is not None and fence.char == "~":
            return self.tilde_fence(p, li, fence)
        if t.startswith("$$"):
            math = self.math_block(p, tp)
            if math is not None:
                return math
        if t.startswith("<"):
            attr = self.attribute_xml(p, tp, t)
            if attr is not None:
                return attr
            region = self.xml_region(p, tp, t)
            if region is not None:
                return region
            container = self.generic_xml(p, li, seg, indent)
            if container is not None:
                return container
            if t.startswith("<!--"):
                comment = self.block_comment(p, tp, li)
                if comment is not None:
                    return comment
            html = self.html_block(p, li, t, tp, at_para_start)
            if html is not None:
                return html
        if t.startswith("{"):
            js = self.bare_json(p, li, tp)
            if js is not None:
                return js
        if _TREE_GLYPHS.search(t):
            tree = self.tree(p, li)
            if tree is not None:
                return tree
        return None

    def in_list_continuation(self, li: int) -> bool:
        for k in range(li - 1, -1, -1):
            line = self.line_text(k)
            if not _NON_WS_RE.search(line):
                continue
            if _LIST_CONTINUATION.match(line):
                return True
            if line[:1] in (" ", "\t"):
                continue
            return False
        return False

    def front_matter(self, li: int, t: str) -> _Raw | None:
        fence = self.line_text(li)
        if fence.startswith("\ufeff"):
            fence = fence[1:]
        if (fence != "---" and fence != "+++") or t != fence:
            return None
        toml = fence == "+++"
        saw_content = False
        for k in range(li + 1, self.line_count):
            line = self.line_text(k)
            if line == fence or (not toml and line == "..."):
                return _Raw("front_matter", 0, self.content_ends[k], True) if saw_content else None
            if not _NON_WS_RE.search(line):
                continue
            shaped = (_TOML_SHAPED if toml else _YAML_SHAPED).match(line) is not None
            if not shaped:
                return None
            saw_content = True
        return None

    def directive(self, p: int, li: int, t: str) -> _Raw | None:
        m = _DIRECTIVE_OPEN.match(t)
        if not m:
            return None
        colons = len(m.group(1))
        if colons == 2:
            return _Raw("directive", p, self.content_ends[li], True)
        stack = [colons]
        for k in range(li + 1, self.line_count):
            line = _trim(self.line_text(k))
            inner = _DIRECTIVE_OPEN.match(line)
            if inner and len(inner.group(1)) >= 3:
                stack.append(len(inner.group(1)))
                continue
            close = _DIRECTIVE_CLOSE.match(line)
            if close and len(close.group(1)) >= stack[-1]:
                stack.pop()
                if not stack:
                    return _Raw("directive", p, self.content_ends[k], True)
        return _Raw("directive", p, self.n, False)

    def mkdocs_admonition(self, p: int, li: int, t: str) -> _Raw | None:
        if not _MKDOCS_OPEN.match(t):
            return None
        last = li
        for k in range(li + 1, self.line_count):
            line = self.line_text(k)
            if _INDENTED.match(line) and _NON_WS_RE.search(line):
                last = k
                continue
            if not _NON_WS_RE.search(line):
                continue
            break
        return _Raw("directive", p, self.content_ends[last], True)

    def callout(self, p: int, li: int, t: str) -> _Raw | None:
        m = _CALLOUT_OPEN.match(t)
        if not m or m.group(1).lower() not in CALLOUT_NAMES:
            return None
        last = li
        for k in range(li + 1, self.line_count):
            if not _QUOTE_LINE.match(self.line_text(k)):
                break
            last = k
        return _Raw("callout", p, self.content_ends[last], True)

    def footnote_definition(self, p: int, li: int, t: str) -> _Raw | None:
        if not _FOOTNOTE_DEF.match(t):
            return None
        last = li
        k = li + 1
        while k < self.line_count:
            line = self.line_text(k)
            if not _NON_WS_RE.search(line):
                j = k + 1
                while j < self.line_count and not _NON_WS_RE.search(self.line_text(j)):
                    j += 1
                if j < self.line_count and _INDENTED.match(self.line_text(j)):
                    k = j
                    continue
                break
            if _INDENTED.match(line):
                last = k
                k += 1
                continue
            if _FOOTNOTE_DEF.match(_trim_start(line)):
                break
            block = self.detect_block(self.line_starts[k], k, False)
            if block is not None:
                break
            last = k
            k += 1
        return _Raw("footnote_def", p, self.content_ends[last], True)

    def backtick_fence(self, p: int, li: int, opener: _FenceOpener) -> _Raw:
        line, closed = _close_fence(self.line_count, self.line_reader, li, opener)
        if closed:
            return _Raw("fence", p, self.content_ends[line], True)
        return _Raw("fence", p, self.n, False)

    def tilde_fence(self, p: int, li: int, opener: _FenceOpener) -> _Raw:
        line, closed = _close_fence(self.line_count, self.line_reader, li, opener)
        if closed:
            tilde_end = self.content_ends[line]
            end = self.renderer_overflow(li + 1, line, tilde_end)
            return _Raw("fence", p, end, self.overflow_complete if end == self.n else True)
        return _Raw("fence", p, self.n, False)

    def renderer_overflow(self, first_line: int, close_line: int, tilde_end: int) -> int:
        end = tilde_end
        self.overflow_complete = True
        j = first_line
        while j <= close_line and j < self.line_count:
            start = self.line_starts[j]
            if self.line_is_blank(j):
                j += 1
                continue
            opener = _fence_opener_of(self.line_text(j))
            if opener is not None and opener.char == "~":
                j += 1
                continue
            inner = self.detect_block_uncached(start, j, False)
            if inner is None:
                j += 1
                continue
            if inner.end > end:
                end = inner.end
                self.overflow_complete = inner.complete
            last_line = self.line_of(max(start, inner.end - 1))
            if last_line > j:
                j = last_line
            j += 1
        return end

    def math_block(self, p: int, tp: int) -> _Raw | None:
        close = self.math_pairs.get(tp)
        if close is None:
            return None
        end = close + 2
        li = self.line_of(tp)
        ce = self.content_ends[li]
        if end <= ce and not self.is_blank(end, ce):
            return None
        end_line = self.line_of(close)
        end_ce = self.content_ends[end_line]
        if end_line != li and not self.is_blank(end, end_ce):
            return None
        return _Raw("math_block", p, end, True)

    def attribute_xml(self, p: int, tp: int, t: str) -> _Raw | None:
        for name in ATTRIBUTE_XML_NAMES:
            prefix = f"<{name}"
            if not t.startswith(prefix):
                continue
            nxt = t[len(prefix) : len(prefix) + 1]
            if nxt not in (" ", ">", "/", "\t"):
                continue
            return self.attribute_element(name, p, tp, "xml_attr")
        return None

    def attribute_element(self, name: str, p: int, tp: int, island_type: str) -> _Raw | None:
        li = self.line_of(tp)
        ce = self.content_ends[li]
        tag = _read_xml_tag(self.text, tp, self.next)
        if tag is not None and not tag.is_closing:
            if tag.is_self_closing:
                return _Raw(island_type, p, tp + tag.length, True)
            open_end = tp + tag.length
        else:
            gt = self.next(">", tp)
            if gt == -1:
                return _Raw(island_type, p, self.n, False)
            if gt >= ce:
                return None
            open_end = gt + 1
        closer = f"</{name}>"
        close = self.next(closer, open_end)
        if close == -1:
            return _Raw(island_type, p, self.n, False)
        return _Raw(island_type, p, close + len(closer), True)

    def xml_region(self, p: int, tp: int, t: str) -> _Raw | None:
        for name in XML_TAG_BLOCK_NAMES:
            opener = f"<{name}>"
            if not t.startswith(opener):
                continue
            closer = f"</{name}>"
            close = self.next(closer, tp + len(opener))
            if close == -1:
                return _Raw("xml_region", p, self.n, False)
            return _Raw("xml_region", p, close + len(closer), True)
        return None

    def generic_xml(self, p: int, li: int, seg: str, indent: int) -> _Raw | None:
        first = seg[indent:]
        opening = _read_xml_tag(first, 0)
        if opening is not None and not opening.is_closing:
            root = opening.tag_name
            if root in KNOWN_XML_TAG_NAMES or root.lower() in ALLOWED_RAW_HTML_TAGS:
                return None
            tracker = _XmlContainerTracker(root)
            first_end = tracker.consume_line(seg, indent)
            if first_end is not None:
                return _Raw("xml_container", p, p + first_end, True)
            for k in range(li + 1, self.line_count):
                end = tracker.consume_line(self.line_text(k))
                if end is not None:
                    return _Raw("xml_container", p, self.line_starts[k] + end, True)
            # An HTML BLOCK tag that never closes owns nothing: GFM ends that HTML
            # block at the blank line (twin of content-ir tokenize; verify-RC-B4 r9).
            if is_html_block_tag_name(root):
                return None
            return _Raw("xml_container", p, self.n, False)
        if _is_unclosed_generic_xml_opening(seg):
            name = re.match(r"^\s*<([A-Za-z_][\w.:-]*)", seg)
            if name and is_html_block_tag_name(name[1]):
                return None
            return _Raw("xml_container", p, self.n, False)
        return None

    def block_comment(self, p: int, tp: int, li: int) -> _Raw | None:
        close = self.next("-->", tp + 4)
        if close == -1:
            return _Raw("html_comment", p, self.n, False)
        end = close + 3
        ce = self.content_ends[li]
        if _PINNED_ANCHOR.fullmatch(self.text, tp, end):
            if end <= ce and not self.is_blank(end, ce):
                return None
            return _Raw("anchor", p, end, True)
        return _Raw("html_comment", p, end, True)

    def html_block(self, p: int, li: int, t: str, tp: int, at_para_start: bool) -> _Raw | None:
        tag = _read_xml_tag(t, 0)
        if tag is None:
            return None
        name = tag.tag_name.lower()
        if name not in ALLOWED_RAW_HTML_TAGS:
            return None
        if name == "pre" and not tag.is_closing:
            m = _PRE_CLOSER.search(self.text, tp)
            if not m:
                return _Raw("html_block", p, self.n, False)
            return _Raw("html_block", p, m.end(), True)
        type_six = name in HTML_BLOCK_LEVEL_TAGS
        type_seven = at_para_start and _trim_end(t) == t[: tag.length]
        if not type_six and not type_seven:
            return None
        end = self.content_ends[li]
        k = li + 1
        while k < self.line_count and not self.line_is_blank(k):
            end = self.content_ends[k]
            k += 1
        return _Raw("html_block", p, end, True)

    def build_brace_tables(self) -> None:
        count = self.line_count
        prefix = [0] * (count + 1)
        text = self.text
        for i in range(count):
            opens, closes = _count_structural_braces(text[self.line_starts[i] : self.content_ends[i]])
            prefix[i + 1] = prefix[i] + opens - closes
        stop = [-1] * count
        stack: list[int] = []
        for m in range(count + 1):
            value = prefix[m]
            while stack and prefix[stack[-1]] >= value:
                i = stack.pop()
                if i < count:
                    stop[i] = m - 1
            stack.append(m)
        self.brace_net = prefix
        self.brace_stop = stop

    def bare_json(self, p: int, li: int, tp: int) -> _Raw | None:
        last_line: int | None = None
        net = 0
        if p == self.line_starts[li]:
            if self.brace_stop is None or self.brace_net is None:
                self.build_brace_tables()
            assert self.brace_stop is not None and self.brace_net is not None
            stop = self.brace_stop[li]
            if stop != -1:
                last_line = stop
                net = self.brace_net[stop + 1] - self.brace_net[li]
        else:
            running = 0
            for k in range(li, self.line_count):
                line = self.text[tp : self.content_ends[li]] if k == li else self.line_text(k)
                opens, closes = _count_structural_braces(line)
                running += opens - closes
                if running <= 0:
                    last_line = k
                    net = running
                    break
        if last_line is None:
            if _is_recognized_json_head(self.text[tp : tp + 512]):
                return _Raw("json", p, self.n, False)
            return None
        if net != 0:
            return None
        end = self.content_ends[last_line]
        ok, _kind = _json_parse(_trim(self.text[tp:end]))
        if not ok:
            return None
        return _Raw("json", p, end, True)

    def tree(self, p: int, li: int) -> _Raw | None:
        tree_lines = 0
        last_tree = li
        k = li
        while k < self.line_count:
            if self.line_is_blank(k):
                k += 1
                continue
            if not _TREE_GLYPHS.search(self.line_text(k)):
                break
            tree_lines += 1
            last_tree = k
            k += 1
        if tree_lines < 3:
            return None
        return _Raw("tree", p, self.content_ends[last_tree], True)

    # ── prose ──────────────────────────────────────────────────────────

    def paragraph(self, pos: int, li: int) -> int:
        end = self.content_ends[li]
        break_line = -1
        for k in range(li + 1, self.line_count):
            if self.line_is_blank(k):
                break
            block = self.detect_block(self.line_starts[k], k, False)
            if block is not None:
                break_line = k
                break
            end = self.content_ends[k]

        if break_line != -1:
            break_island = self.detect_block(self.line_starts[break_line], break_line, False)
            if break_island is not None and break_island.type == "tree":
                root = break_line
                for j in range(break_line - 1, li - 1, -1):
                    trimmed = _trim(self.line_text(j))
                    if not trimmed or _is_splitter_tree_line(trimmed) or _HEADING.match(trimmed):
                        break
                    root = j
                if root < break_line:
                    tree_start = pos if root == li else self.line_starts[root]
                    tree = _Raw("tree", tree_start, break_island.end, break_island.complete)
                    if tree_start > pos:
                        prose_end = self.content_ends[root - 1]
                        inlines, brk, _orphan = self.scan_inline(pos, prose_end)
                        if brk is None:
                            self.push(_Block("prose", pos, prose_end, None, inlines))
                            self.push(_Block("gap", prose_end, tree_start, None, []))
                            self.push(_Block("island", tree_start, tree.end, tree, []))
                            return tree.end
                    else:
                        self.push(_Block("island", tree_start, tree.end, tree, []))
                        return tree.end

        inlines, brk, orphan = self.scan_inline(pos, end)
        if brk is None:
            self.push(_Block("prose", pos, end, None, inlines))
            return end
        br = _Raw(brk.type, brk.start, brk.end, brk.complete, True)
        if orphan:
            start = pos
            while self.blocks:
                last = self.blocks[-1]
                if last.kind == "island":
                    break
                self.blocks.pop()
                start = last.start
            island = _Raw(br.type, start, br.end, br.complete, True)
            self.push(_Block("island", start, island.end, island, []))
            return island.end
        self.push(_Block("prose", pos, br.start, None, [x for x in inlines if x.end <= br.start]))
        self.push(_Block("island", br.start, br.end, br, []))
        return br.end

    def scan_inline(self, ps: int, pe: int) -> tuple[list[_Raw], _Raw | None, bool]:
        text = self.text
        inlines: list[_Raw] = []
        has_kind = text.find("__kind", ps, pe) != -1
        kind_budget = 4 * (pe - ps) + 65536
        runs: _BacktickRuns | None = None
        special = _INLINE_SPECIAL

        def within(needle: str, start: int) -> int:
            at = self.next(needle, start)
            return at if at != -1 and at + len(needle) <= pe else -1

        i = ps
        while i < pe:
            m = special.search(text, i, pe)
            if m is None:
                break
            i = m.start()
            ch = text[i]
            if ch == "\\":
                nxt = text[i + 1 : i + 2]
                if nxt == "(" or nxt == "[":
                    close = within("\\)" if nxt == "(" else "\\]", i + 2)
                    is_math = close != -1 and (
                        nxt == "(" or _is_escaped_bracket_math(text[i + 2 : close], text[i - 1] if i > 0 else None)
                    )
                    if close != -1 and is_math:
                        inlines.append(_Raw("math_inline", i, close + 2, True))
                        i = close + 2
                        continue
                i += 2
                continue
            if ch == "`":
                n = _backtick_run_length(text, i)
                if runs is None:
                    runs = _BacktickRuns(text, ps, pe)
                close = runs.next(n, i + n)
                if close != -1 and close + n > pe:
                    close = -1
                i = i + n if close == -1 else close + n
                continue
            if ch == "$":
                if text[i + 1 : i + 2] == "$":
                    close = self.math_pairs.get(i)
                    if close is None:
                        i += 2
                        continue
                    if close + 2 > pe:
                        return inlines, _Raw("math_block", i, close + 2, True), False
                    inlines.append(_Raw("math_inline", i, close + 2, True))
                    i = close + 2
                    continue
                end = _single_dollar_math_end(text, i, pe)
                if end > 0:
                    inlines.append(_Raw("math_inline", i, end, True))
                    i = end
                    continue
                i += 1
                continue
            if ch == "{":
                if text[i + 1 : i + 2] == "{":
                    close = self.next("}}", i + 2)
                    if close != -1 and close + 2 <= pe and close - i <= 200 and text.find("\n", i, close) == -1:
                        inlines.append(_Raw("variable", i, close + 2, True))
                        i = close + 2
                        continue
                    i += 2
                    continue
                if has_kind and kind_budget > 0 and _KIND_PROBE.match(text[i : i + 64]):
                    limit = min(pe, i + 65536)
                    end_obj = _matching_json_object_end(text, i, limit)
                    kind_budget -= (end_obj if end_obj is not None else limit) - i
                    if end_obj is not None and _declared_kind(text[i:end_obj]):
                        inlines.append(_Raw("kind_json", i, end_obj, True))
                        i = end_obj
                        continue
                i += 1
                continue
            if (ch == "[" and text[i + 1 : i + 2] == "[") or (ch == "!" and text[i + 1 : i + 3] == "[["):
                open_at = i + 3 if ch == "!" else i + 2
                close = within("]]", open_at)
                newline = self.next("\n", open_at)
                inner = "" if close == -1 else text[open_at:close]
                if (
                    close != -1
                    and (newline == -1 or newline > close)
                    and _trim(inner)
                    and not _BRACKETS.search(inner)
                ):
                    inlines.append(_Raw("wikilink", i, close + 2, True))
                    i = close + 2
                    continue
            if ch == "[":
                media = next((prefix for prefix in _MEDIA_REF_PREFIXES if text.startswith(prefix, i)), None)
                if media is not None:
                    close = within("]", i + len(media))
                    newline = self.next("\n", i)
                    if close != -1 and (newline == -1 or newline > close):
                        inlines.append(_Raw("media_ref", i, close + 1, True))
                        i = close + 1
                        continue
                i += 1
                continue
            if ch == "<":
                if text.startswith("<!--", i):
                    close = self.next("-->", i + 4)
                    if close == -1:
                        return inlines, _Raw("html_comment", i, self.n, False), False
                    end = close + 3
                    is_anchor = end - i <= 64 and _PINNED_ANCHOR.fullmatch(text, i, end) is not None
                    kind = "anchor" if is_anchor else "html_comment"
                    if end > pe:
                        return inlines, _Raw(kind, i, end, True), False
                    inlines.append(_Raw(kind, i, end, True))
                    i = end
                    continue
                cite = _CITE.match(text[i : i + 64])
                if cite:
                    inlines.append(_Raw("cite", i, i + cite.end(), True))
                    i += cite.end()
                    continue
                tag = _read_xml_tag(text, i, self.next)
                if tag is not None and i + tag.length <= pe:
                    name = tag.tag_name
                    tag_end = i + tag.length
                    is_attr = name in ATTRIBUTE_XML_NAMES
                    is_thinking = name in THINKING_FAMILY and tag.length == len(name) + 2
                    if not tag.is_closing and (is_attr or is_thinking):
                        if tag.is_self_closing:
                            inlines.append(_Raw("xml_inline", i, tag_end, True))
                            i = tag_end
                            continue
                        closer = f"</{name}>"
                        close = self.next(closer, tag_end)
                        block_type = "xml_attr" if is_attr else "xml_region"
                        if close == -1 and is_thinking:
                            i = tag_end
                            continue
                        if close == -1:
                            return inlines, _Raw(block_type, i, self.n, False), False
                        end = close + len(closer)
                        if end > pe:
                            return inlines, _Raw(block_type, i, end, True), False
                        inlines.append(_Raw("xml_inline", i, end, True))
                        i = end
                        continue
                    if tag.is_closing and name in THINKING_FAMILY:
                        return inlines, _Raw("xml_region", i, tag_end, True), True
                    kind = "html_tag" if name.lower() in ALLOWED_RAW_HTML_TAGS else "xml_tag"
                    inlines.append(_Raw(kind, i, tag_end, True))
                    i = tag_end
                    continue
                pending = next(
                    (
                        name
                        for name in ATTRIBUTE_XML_NAMES
                        if text.startswith(f"<{name}", i) and _is_ws(text[i + len(name) + 1 : i + len(name) + 2])
                    ),
                    None,
                )
                if pending is not None and self.next(">", i) == -1:
                    return inlines, _Raw("xml_attr", i, self.n, False), False
                i += 1
                continue
            i += 1
        return inlines, None, False


def list_islands(text: str) -> list[SourceIsland]:
    """Every protected island of stored ``text`` — block-level and inline — in document order.

    The twin of ``listIslands(tokenizeSource(text))`` (``@ai-matrx/content-ir``
    source/tokenize.ts). ``start``/``end`` are ``str`` offsets into ``text``;
    ``raw == text[start:end]``. Never raises; an unclosed construct is an island
    running to the end of the text with ``complete=False``.
    """
    units, astral = _to_utf16_units(text)
    blocks = _Tokenizer(units).run()

    def cp(u: int) -> int:
        # Every astral character that starts before ``u - 1`` counted one unit too many.
        return u - bisect_left(astral, u - 1) if astral else u

    out: list[SourceIsland] = []
    for block in blocks:
        if block.kind == "island" and block.island is not None:
            members = [(block.island.type, block.start, block.end, False, block.island.complete)]
        else:
            members = [(x.type, x.start, x.end, True, x.complete) for x in block.inlines]
        for island_type, start, end, inline, complete in members:
            s, e = cp(start), cp(end)
            out.append(SourceIsland(island_type, s, e, inline, complete, text[s:e]))
    return out
