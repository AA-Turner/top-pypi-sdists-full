"""Section-aware reading of long skill bodies (reference documents).

A long markdown skill is split by its ATX headings (``#`` … ``######``; lines
inside fenced code blocks are never headings). Every heading becomes a
``SkillSection`` whose span runs from the heading line to the next heading of
the same or a higher level — so a section includes its subsections, exactly as
a reader of the document expects. Text before the first heading is the
``intro`` section.

Each section carries three handles the ``skill`` tool accepts as ``section``:

* ``id``      — GitHub-style heading slug, de-duplicated with ``-1``, ``-2`` …
* ``number``  — hierarchical position (``"2"``, ``"2.1"``); ``"0"`` is the intro
* ``path``    — slash-joined ancestor slugs (``"deductions/standard"``)

and, as a last resort, the heading text itself (case-insensitive).

Everything here is pure and deterministic: the same body always yields the
same outline, which keeps the preamble outline byte-stable (prompt caching).
"""

from __future__ import annotations

import re
import unicodedata

from pydantic import BaseModel, ConfigDict

from matrx_ai.skills.knobs import preamble_outline_chars, preamble_outline_entries

INTRO_SECTION_ID = "intro"

_SLUG_DROP_RE = re.compile(r"[^\w\- ]+")


class SkillSection(BaseModel):
    """One heading-delimited section of a skill body."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str
    number: str
    path: str
    title: str
    level: int  # 1–6; 0 for the intro
    start: int  # char offset of the heading line in the body
    end: int  # char offset where the section (incl. subsections) ends
    chars: int

    def outline_entry(self) -> dict[str, object]:
        """The wire shape of one outline row (no offsets — the section handle is enough)."""
        return {
            "id": self.id,
            "number": self.number,
            "title": self.title,
            "level": self.level,
            "chars": self.chars,
        }


def slugify(text: str) -> str:
    """GitHub-style heading anchor: lowercase, punctuation dropped, spaces → ``-``."""
    norm = unicodedata.normalize("NFKD", text).strip().lower()
    norm = _SLUG_DROP_RE.sub("", norm)
    norm = re.sub(r"\s+", "-", norm).strip("-")
    return norm or "section"


def _clean_title(raw: str) -> str:
    # Strip inline markdown emphasis/code markers so ids and titles read plainly.
    title = re.sub(r"[`*_]+", "", raw).strip()
    title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", title)
    return title or raw.strip()


_ATX_RE = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?(?:[ \t]+#+)?[ \t]*$")
_FENCE_OPEN_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_SETEXT_RE = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")
_CONTAINER_RE = re.compile(r"^ {0,3}(?:[-*+][ \t]|\d{1,9}[.)][ \t]|>|\|)")
_RAW_OPEN_RE = re.compile(r"^\s*<(pre|script|style)\b", re.IGNORECASE)


def _scan_headings(body: str) -> list[tuple[int, int, str]]:
    """``(offset, level, title)`` of every real heading, in order.

    CommonMark rules that matter for reference documents: ATX headings may be indented up
    to three spaces and a closing ``#`` run needs whitespace before it (``# C#`` is "C#");
    a code fence closes only on the same character, at least as long as the opener, with
    no info string (so a ``` line inside a ````md block does not close it); HTML comments
    and ``<pre>``/``<script>``/``<style>`` blocks hide their contents; setext headings
    (``Title`` over ``=====`` / ``-----``) count.
    """
    headings: list[tuple[int, int, str]] = []
    offset = 0
    fence: tuple[str, int] | None = None
    in_comment = False
    raw_close: str | None = None
    para: list[tuple[int, str]] = []  # current paragraph lines (offset, text)
    in_container = False  # inside a list item / quote / table until the next blank line
    for line in body.splitlines(keepends=True):
        text = line.rstrip("\r\n")
        here = offset
        offset += len(line)

        if fence is not None:
            m = re.match(r"^ {0,3}(" + re.escape(fence[0]) + r"{" + str(fence[1]) + r",})[ \t]*$", text)
            if m:
                fence = None
            continue
        if in_comment:
            if "-->" in text:
                in_comment = False
            continue
        if raw_close is not None:
            if raw_close in text.lower():
                raw_close = None
            continue

        if not text.strip():
            para, in_container = [], False
            continue

        fm = _FENCE_OPEN_RE.match(text)
        if fm and not (fm.group(1)[0] == "`" and "`" in fm.group(2)):
            fence = (fm.group(1)[0], len(fm.group(1)))
            para = []
            continue
        if text.lstrip().startswith("<!--"):
            if "-->" not in text.split("<!--", 1)[1]:
                in_comment = True
            para = []
            continue
        rm = _RAW_OPEN_RE.match(text)
        if rm:
            close = f"</{rm.group(1).lower()}"
            if close not in text.lower():
                raw_close = close
            para = []
            continue

        am = _ATX_RE.match(text)
        if am and (am.group(2) or "").strip():
            headings.append((here, len(am.group(1)), _clean_title(am.group(2))))
            para, in_container = [], False
            continue

        sm = _SETEXT_RE.match(text)
        if sm and para and not in_container:
            title = _clean_title(" ".join(t.strip() for _, t in para))
            headings.append((para[0][0], 1 if sm.group(1)[0] == "=" else 2, title))
            para = []
            continue

        if _CONTAINER_RE.match(text):
            in_container = True
            para = []
        elif not in_container:
            para.append((here, text))
    return headings


def parse_sections(body: str) -> list[SkillSection]:
    """Every section of ``body`` in document order (intro first when present)."""
    if not body:
        return []

    headings = _scan_headings(body)
    total = len(body)
    sections: list[SkillSection] = []

    first_heading_at = headings[0][0] if headings else total
    if body[:first_heading_at].strip():
        sections.append(
            SkillSection(
                id=INTRO_SECTION_ID,
                number="0",
                path=INTRO_SECTION_ID,
                title="Introduction",
                level=0,
                start=0,
                end=first_heading_at,
                chars=first_heading_at,
            )
        )

    used_ids: set[str] = {INTRO_SECTION_ID} if sections else set()
    # Stack of [level, number, child_count, slug]; the root is level 0 with no number.
    stack: list[list] = [[0, "", 0, ""]]
    for idx, (start, level, title) in enumerate(headings):
        end = total
        for later_start, later_level, _ in headings[idx + 1 :]:
            if later_level <= level:
                end = later_start
                break

        while stack[-1][0] >= level:
            stack.pop()
        parent = stack[-1]
        parent[2] += 1
        # A per-parent child counter: a skipped level can never give two sections one number.
        number = f"{parent[1]}.{parent[2]}" if parent[1] else str(parent[2])

        base = slugify(title)
        sid, n = base, 0
        while sid in used_ids:
            n += 1
            sid = f"{base}-{n}"
        used_ids.add(sid)

        stack.append([level, number, 0, base])
        path = "/".join(e[3] for e in stack[1:])

        sections.append(
            SkillSection(
                id=sid,
                number=number,
                path=path,
                title=title,
                level=level,
                start=start,
                end=end,
                chars=end - start,
            )
        )
    return sections


def find_section(sections: list[SkillSection], handle: str) -> SkillSection | None:
    """Resolve a ``section`` argument: id, number, path, slugged text, then heading text."""
    raw = (handle or "").strip()
    if not raw:
        return None
    raw = raw.lstrip("#").strip()
    for key in ("id", "number", "path"):
        for s in sections:
            if getattr(s, key) == raw:
                return s
    slug = slugify(raw)
    for s in sections:
        if s.id == slug:
            return s
    if "/" in raw:
        want = "/".join(slugify(p) for p in raw.split("/") if p.strip())
        for s in sections:
            if s.path == want or s.path.endswith("/" + want):
                return s
    low = raw.lower()
    for s in sections:
        if s.title.lower() == low:
            return s
    return None


def section_text(body: str, section: SkillSection) -> str:
    return body[section.start : section.end]


def next_section(sections: list[SkillSection], section: SkillSection) -> SkillSection | None:
    """The section that begins where this one ends (reading order, skipping its children)."""
    for s in sections:
        if s.start >= section.end:
            return s
    return None


# ---------------------------------------------------------------------------
# Compact outline for the preamble (listed reference skills)
# ---------------------------------------------------------------------------

# Outline bounds are knobs (agents.context.skill_preamble_outline_entries / _chars): matrx_ai.skills.knobs.


def _size(chars: int) -> str:
    if chars < 1000:
        return f"{chars}"
    return f"{chars / 1000:.1f}k".replace(".0k", "k")


def outline_levels(sections: list[SkillSection]) -> tuple[int, ...]:
    """The two heading levels worth naming: the first level with ≥2 headings, and the next.

    A document wrapped in a single ``# Title`` would otherwise outline as one line.
    """
    levels = sorted({s.level for s in sections if s.level > 0})
    if not levels:
        return ()
    base = levels[-1]
    for lv in levels:
        if sum(1 for s in sections if s.level == lv) >= 2:
            base = lv
            break
    deeper = [lv for lv in levels if lv > base]
    return (base, deeper[0]) if deeper else (base,)


def compact_outline(body: str) -> str:
    """One deterministic line naming the document's sections and sizes.

    ``1 Filing status (2.1k) · 1.1 Single (800) · 2 Deductions (9.4k) · … (+12 more)``.
    Empty when the body has fewer than two headings.
    """
    sections = parse_sections(body)
    headed = [s for s in sections if s.level > 0]
    if len(headed) < 2:
        return ""
    max_entries, max_chars = preamble_outline_entries(), preamble_outline_chars()
    levels = outline_levels(sections)
    chosen = [s for s in headed if s.level in levels]
    parts: list[str] = []
    used = 0
    for s in chosen:
        piece = f"{s.number} {s.title} ({_size(s.chars)})"
        if len(parts) >= max_entries or used + len(piece) + 3 > max_chars:
            break
        parts.append(piece)
        used += len(piece) + 3
    rest = len(chosen) - len(parts)
    line = " · ".join(parts)
    if rest > 0:
        line += f" · … (+{rest} more)"
    return line
