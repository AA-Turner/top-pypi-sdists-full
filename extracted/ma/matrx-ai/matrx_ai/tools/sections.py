"""Cut an oversized tool result into sections WITHOUT destroying its structure.

Why this is not a paragraph splitter
------------------------------------
Measured 2026-09-20 on ``chat.tool_call`` (project brsgrqvjdzwihsvnfqkf), over
the 1,702 tool results at or over the 25,000-character canary band:

    JSON-shaped (starts with ``{`` or ``[``) .... 1,363 of 1,702 (80%)
    carries markdown headings (``^#{1,3} ``) ....   322 of 1,702 (19%)
    has >= 20 newlines ..........................   327 of 1,702 (19%)

So a sectioner designed for scraped-page prose would mis-cut four results in
five. A fixed window through ``json.dumps(rows)`` hands the judge half of one
record glued to half of the next; the judge answers fluently on the fragment and
the gate drops the half that mattered. That is the named fabrication risk at this
seam, and the countermeasure is mechanical, not persuasive:

  * JSON is cut on REAL top-level boundaries, found by a string-aware bracket
    walk over the ORIGINAL text. Every section is an exact substring of the
    input and never straddles an item.
  * Every section DECLARES how it was cut (``section_source``), so a bound agent
    can weight a ``fixed_window`` boundary down and a test can assert that a JSON
    result never produced one.

Section sources
---------------
``json_item``        a top-level array element, or one ``"key": value`` pair of a
                     top-level object; for the common "one giant list under one
                     key" shape, one element of that list (heading ``key[i]``).
``heading``          a markdown heading and the body under it.
``paragraph_block``  a blank-line-separated block of prose.
``fixed_window``     the last resort: an unstructured run of characters. Its
                     boundaries are arbitrary and it says so.

Pure, allocation-light, and never raises: a result this module cannot understand
comes back as fixed windows, which is exactly today's behaviour made explicit.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

SectionSource = Literal["json_item", "heading", "paragraph_block", "fixed_window"]
ResultFormat = Literal["json", "markdown", "text"]

#: Target size of one section when the shape gives no natural boundary. Chosen so
#: a ~50,000-character result becomes ~13 windows — few enough to judge cheaply,
#: small enough that keeping one is a real saving.
DEFAULT_TARGET_SECTION_CHARS = 4_000

#: A top-level object key whose value serialises to at least this much is treated
#: as "the payload" and, when it is a list, expanded into one section per item.
#: Below it, per-key sectioning is already fine-grained enough.
_EXPAND_KEY_MIN_CHARS = 8_000

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)

#: Keys whose value names an item, tried in order, for a human-readable heading.
_NAME_KEYS = ("label", "title", "name", "heading", "resource_type", "tool_name", "id")


@dataclass(frozen=True)
class ResultSection:
    """One cut of a tool result, and the honest story of how it was cut."""

    index: int
    text: str
    section_source: SectionSource
    heading: str | None
    chars: int
    start: int
    """Offset of this section's first character in the ORIGINAL result."""
    end: int
    """Offset one past this section's last character in the ORIGINAL result."""


@dataclass(frozen=True)
class SectionedResult:
    sections: tuple[ResultSection, ...]
    result_format: ResultFormat
    total_chars: int

    @property
    def headings(self) -> tuple[str | None, ...]:
        return tuple(s.heading for s in self.sections)


# ---------------------------------------------------------------------------
# JSON — a string-aware walk of the ORIGINAL text, so spans are exact
# ---------------------------------------------------------------------------


def _scan_string(text: str, i: int) -> int:
    """Return the index one past the closing quote of the JSON string at ``i``."""
    i += 1
    n = len(text)
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == '"':
            return i + 1
        i += 1
    return n


def _container_bounds(text: str) -> tuple[int, int, str] | None:
    """Locate the outermost JSON container: ``(open_idx, close_idx, kind)``.

    ``close_idx`` points AT the closing bracket. Returns None when the text is
    not a single well-formed container — a truncated or trailing-garbage payload
    falls through to the text rules rather than being cut on guessed boundaries.
    """
    s = text.strip()
    if not s or s[0] not in "[{":
        return None
    offset = len(text) - len(text.lstrip())
    opener = s[0]
    closer = "]" if opener == "[" else "}"
    depth = 0
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '"':
            i = _scan_string(s, i)
            continue
        if c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0:
                if c != closer:
                    return None
                return offset, offset + i, opener
        i += 1
    return None


def _split_container(text: str, open_idx: int, close_idx: int, kind: str) -> list[tuple[int, int]]:
    """Spans of the direct children of the container, in order.

    For an array: one span per element. For an object: one span per
    ``"key": value`` pair. Spans exclude the separating commas and the brackets,
    so every span is a standalone, exactly-substring unit.
    """
    spans: list[tuple[int, int]] = []
    i = open_idx + 1
    depth = 0
    start: int | None = None
    while i < close_idx:
        c = text[i]
        if c == '"':
            if start is None:
                start = i
            i = _scan_string(text, i)
            continue
        if c in "[{":
            if start is None:
                start = i
            depth += 1
        elif c in "]}":
            depth -= 1
        elif c == "," and depth == 0:
            if start is not None:
                spans.append((start, i))
                start = None
        elif start is None and not c.isspace():
            start = i
        i += 1
    if start is not None:
        tail = text[start:close_idx].rstrip()
        if tail:
            spans.append((start, start + len(tail)))
    # Trim trailing whitespace inside every span so a section is never padding.
    out: list[tuple[int, int]] = []
    for a, b in spans:
        seg = text[a:b]
        trimmed = seg.rstrip()
        if trimmed:
            out.append((a, a + len(trimmed)))
    return out


def _object_key(segment: str) -> str | None:
    seg = segment.lstrip()
    if not seg.startswith('"'):
        return None
    end = _scan_string(seg, 0)
    try:
        import json

        return str(json.loads(seg[:end]))
    except Exception:  # noqa: BLE001
        return None


def _item_heading(segment: str, fallback: str) -> str:
    """A human-readable name for one JSON item, or the positional fallback."""
    seg = segment.lstrip()
    if not seg.startswith("{"):
        return fallback
    import json

    try:
        obj = json.loads(seg)
    except Exception:  # noqa: BLE001
        return fallback
    if not isinstance(obj, dict):
        return fallback
    for key in _NAME_KEYS:
        val = obj.get(key)
        if isinstance(val, str) and val.strip():
            return f"{fallback} {val.strip()[:80]}"
    return fallback


def _json_sections(text: str) -> list[tuple[int, int, str, str]] | None:
    """``(start, end, heading, group)`` for every JSON item, or None if not JSON.

    ``group`` names the parent an item belongs to. Sections are only ever merged
    WITHIN a group, so a grouped span can never reach across the boundary of the
    array that held its members.
    """
    bounds = _container_bounds(text)
    if bounds is None:
        return None
    open_idx, close_idx, kind = bounds
    spans = _split_container(text, open_idx, close_idx, kind)
    if not spans:
        return None
    if kind == "[":
        return [
            (a, b, _item_heading(text[a:b], f"[{i}]"), "") for i, (a, b) in enumerate(spans)
        ]

    # Object. One section per key — EXCEPT the common real shape where one key
    # holds the whole payload as a list ({"rows": [...]}, {"elements": [...]},
    # {"resources": [...]}). Sectioning that as one key would hand the judge the
    # entire result as a single section and change nothing.
    out: list[tuple[int, int, str, str]] = []
    for a, b in spans:
        segment = text[a:b]
        key = _object_key(segment)
        label = key or f"[{len(out)}]"
        colon = segment.find(":")
        value_rel = colon + 1 if colon != -1 else 0
        value_abs = a + value_rel
        value_text = text[value_abs:b]
        inner = _container_bounds(value_text)
        if (
            key is not None
            and inner is not None
            and inner[2] == "["
            and len(value_text) >= _EXPAND_KEY_MIN_CHARS
        ):
            inner_spans = _split_container(
                value_text, inner[0], inner[1], inner[2]
            )
            if len(inner_spans) >= 2:
                for i, (ia, ib) in enumerate(inner_spans):
                    seg = value_text[ia:ib]
                    out.append(
                        (
                            value_abs + ia,
                            value_abs + ib,
                            _item_heading(seg, f"{key}[{i}]"),
                            key,
                        )
                    )
                continue
        out.append((a, b, label, ""))
    return out or None


# ---------------------------------------------------------------------------
# Markdown / prose / last resort
# ---------------------------------------------------------------------------


def _heading_sections(text: str) -> list[tuple[int, int, str | None, str]] | None:
    matches = list(_HEADING_RE.finditer(text))
    if len(matches) < 2:
        return None
    out: list[tuple[int, int, str | None, str]] = []
    first = matches[0].start()
    if text[:first].strip():
        out.append((0, first, None, ""))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        out.append((m.start(), end, m.group(2).strip(), ""))
    return out


def _paragraph_sections(text: str) -> list[tuple[int, int, str | None, str]] | None:
    spans: list[tuple[int, int, str | None, str]] = []
    pos = 0
    for block in re.split(r"\n\s*\n", text):
        start = text.find(block, pos)
        if start == -1:
            start = pos
        end = start + len(block)
        pos = end
        if block.strip():
            spans.append((start, end, None, ""))
    return spans if len(spans) >= 2 else None


def _fixed_windows(text: str, window: int) -> list[tuple[int, int, str | None, str]]:
    window = max(1, window)
    return [
        (i, min(i + window, len(text)), None, "") for i in range(0, len(text), window)
    ]


# ---------------------------------------------------------------------------
# Grouping — the ONLY way a section count is reduced, and it never splits
# ---------------------------------------------------------------------------


def _group_to_max(
    spans: list[tuple[int, int, str | None, str]], max_sections: int
) -> list[tuple[int, int, str | None, str]]:
    """Merge ADJACENT spans of the SAME group until there are at most
    ``max_sections`` of them.

    Merging, never splitting: a grouped section starts at one item's first
    character and ends at another item's last, so an item is still never cut in
    half. The group check keeps a merge inside the array that held its members —
    without it, "count" and "elements[0]" of a ``{"count": …, "elements": […]}``
    result would fuse into a span that reaches across the opening bracket.

    The heading of a merged run names its first member and says how many
    followed, because "section 4" silently meaning items 40-49 is exactly the
    kind of quiet lie this gate exists to stop.
    """
    if max_sections < 1 or len(spans) <= max_sections:
        return spans
    per = 2
    while True:
        out: list[tuple[int, int, str | None, str]] = []
        chunk: list[tuple[int, int, str | None, str]] = []
        for span in spans:
            if chunk and (span[3] != chunk[0][3] or len(chunk) >= per):
                out.append(_merge(chunk))
                chunk = []
            chunk.append(span)
        if chunk:
            out.append(_merge(chunk))
        if len(out) <= max_sections or per >= len(spans):
            return out
        per += 1


def _merge(
    chunk: list[tuple[int, int, str | None, str]],
) -> tuple[int, int, str | None, str]:
    head = chunk[0][2]
    if len(chunk) > 1:
        head = f"{head or '[…]'} (+{len(chunk) - 1} more)"
    return (chunk[0][0], chunk[-1][1], head, chunk[0][3])


def section_result(
    content: str,
    *,
    max_sections: int = 200,
    target_section_chars: int = DEFAULT_TARGET_SECTION_CHARS,
) -> SectionedResult:
    """Cut ``content`` into sections on the best boundary its shape offers."""
    total = len(content)
    if not content:
        return SectionedResult(sections=(), result_format="text", total_chars=0)

    spans: list[tuple[int, int, str | None, str]] | None = None
    source: SectionSource = "fixed_window"
    fmt: ResultFormat = "text"

    try:
        json_spans = _json_sections(content)
    except Exception:  # noqa: BLE001 — a shape we cannot walk is not an error
        json_spans = None
    if json_spans:
        spans = list(json_spans)
        source = "json_item"
        fmt = "json"
    else:
        heading_spans = _heading_sections(content)
        if heading_spans:
            spans = list(heading_spans)
            source = "heading"
            fmt = "markdown"
        else:
            para_spans = _paragraph_sections(content)
            if para_spans:
                spans = list(para_spans)
                source = "paragraph_block"
                fmt = "text"
            else:
                spans = list(_fixed_windows(content, target_section_chars))
                source = "fixed_window"
                fmt = "text"

    spans = _group_to_max(spans, max_sections)
    sections = tuple(
        ResultSection(
            index=i,
            text=content[a:b],
            section_source=source,
            heading=h,
            chars=b - a,
            start=a,
            end=b,
        )
        for i, (a, b, h, _group) in enumerate(spans)
    )
    return SectionedResult(sections=sections, result_format=fmt, total_chars=total)


__all__ = [
    "DEFAULT_TARGET_SECTION_CHARS",
    "ResultFormat",
    "ResultSection",
    "SectionSource",
    "SectionedResult",
    "section_result",
]
