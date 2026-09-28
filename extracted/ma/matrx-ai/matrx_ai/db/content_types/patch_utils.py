"""
Fuzzy find-and-replace patch utility for LLM-generated content edits.

Patch passes (in order, stopping at the first pass that finds anything):
  1. Exact match
  2. Whitespace-normalized match  (collapse runs of spaces/tabs)
  3. Blank-line-stripped match    (ignore empty lines entirely)
  4. Lenient match                (normalize whitespace + strip punctuation/quotes/dashes)

A patch applies to EXACTLY ONE place or not at all. It never silently falls
back to a different edit:

  * no pass matches            → ``PatchError`` kind ``no_match``
  * the first pass that matches finds the excerpt in several places
                               → ``PatchError`` kind ``ambiguous`` naming how
                                 many places and on which lines, so the model
                                 can widen ``old_str`` and retry.
  * the edit would damage a PROTECTED REGION → ``PatchError`` kind
    ``protected_block``. Protected regions are the content-ir islands — fenced
    code, math, ``{{variables}}``, citations, kind JSON, XML sections, HTML
    blocks/comments, directives, callouts, footnotes, front matter, wikilinks —
    read by ``matrx_ai.processing.blocks.source_islands.list_islands``, the
    Python twin of ``@ai-matrx/content-ir`` ``source/tokenize.ts`` held to the
    same generated vectors, so the server protects exactly what the client
    editor protects (``source/splice.ts``: islands change only through an edit
    that names them). Refused when the matched span cuts THROUGH a region's
    boundary; when a tolerant (non-exact) match covers whole regions without
    carrying each byte-identical into the replacement; or when the result
    would disturb a region the patch never named (e.g. an unclosed fence that
    swallows the kind below it). An edit wholly inside one region, or an
    exact excerpt that quotes whole regions, is the model naming them and
    applies normally.

Bytes outside the matched span are copied, never rebuilt, so everything the
patch did not name is byte-identical after it (the splice guarantee).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from enum import Enum


class PatchPassLevel(str, Enum):
    EXACT = "exact"
    WHITESPACE_NORMALIZED = "whitespace_normalized"
    BLANK_LINES_STRIPPED = "blank_lines_stripped"
    LENIENT = "lenient"


@dataclass
class PatchResult:
    new_content: str
    matched_at: PatchPassLevel
    original_snippet: str  # the actual text that was found and replaced
    start: int = 0  # UTF-16-agnostic str offset of the replaced span in the ORIGINAL
    end: int = 0


#: ``PatchError.kind`` values — each maps to an error_type the model reads.
PATCH_NO_MATCH = "no_match"
PATCH_AMBIGUOUS = "ambiguous"
PATCH_PROTECTED_BLOCK = "protected_block"


@dataclass
class PatchError(Exception):
    note_id: str
    search_text: str
    passes_attempted: list[PatchPassLevel]
    message: str = ""
    kind: str = PATCH_NO_MATCH
    match_count: int = 0
    match_lines: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.message:
            return
        preview = repr(self.search_text[:200])
        if self.kind == PATCH_AMBIGUOUS:
            lines = ", ".join(str(n) for n in self.match_lines[:10])
            self.message = (
                f"Patch refused: the excerpt matches {self.match_count} places in "
                f"'{self.note_id}' (lines {lines}), so it does not name ONE edit. "
                "Nothing was changed.\n"
                f"Search text (first 200 chars): {preview}\n"
                "Remedy: add enough surrounding lines to the excerpt that it matches "
                "exactly one place, then retry."
            )
        elif self.kind == PATCH_PROTECTED_BLOCK:
            self.message = (
                f"Patch refused: the excerpt only matched '{self.note_id}' tolerantly, and "
                "that tolerant match would cut through a fenced code block's fence line "
                "(a protected block). Nothing was changed.\n"
                f"Search text (first 200 chars): {preview}\n"
                "Remedy: copy the excerpt verbatim from the current content — exact "
                "whitespace and punctuation — or edit text entirely inside or entirely "
                "outside the code block."
            )
        else:
            self.message = (
                f"Patch failed: no match found in '{self.note_id}'. Nothing was changed.\n"
                f"Searched using passes: {[p.value for p in self.passes_attempted]}.\n"
                f"Search text (first 200 chars): {preview}\n"
                "Remedy: read the current content again and use a verbatim excerpt "
                "from it."
            )

    def __str__(self) -> str:
        return self.message

    @property
    def error_type(self) -> str:
        return {
            PATCH_AMBIGUOUS: "patch_ambiguous",
            PATCH_PROTECTED_BLOCK: "patch_protected_block",
        }.get(self.kind, "patch_no_match")

    def to_dict(self) -> dict:
        return {
            "error": self.error_type,
            "note_id": self.note_id,
            "passes_attempted": [p.value for p in self.passes_attempted],
            "search_preview": self.search_text[:200],
            "match_count": self.match_count,
            "match_lines": self.match_lines,
            "message": self.message,
        }


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------

def _normalize_whitespace(text: str) -> str:
    """Collapse runs of spaces/tabs into a single space; preserve newlines."""
    return re.sub(r"[ \t]+", " ", text)


def _strip_blank_lines(text: str) -> str:
    """Remove lines that are empty or contain only whitespace."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return "\n".join(lines)


def _lenient_normalize(text: str) -> str:
    """
    Aggressive normalization for pass 4:
      - Collapse all whitespace (including newlines) into a single space
      - Remove common punctuation characters that small models often get wrong:
        curly/smart quotes → straight quotes, em/en dashes → hyphens,
        ellipsis → three dots, strip zero-width and other invisible chars
      - Lowercase for comparison
    """
    # Normalize unicode (NFC) first
    text = unicodedata.normalize("NFC", text)

    # Smart quotes → straight
    text = text.translate(str.maketrans("\u2018\u2019\u201c\u201d", "''\"\""))

    # Em dash / en dash → hyphen
    text = text.translate(str.maketrans("\u2014\u2013", "--"))

    # Ellipsis → three dots
    text = text.replace("\u2026", "...")

    # Strip zero-width / non-printing chars
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)

    # Collapse ALL whitespace (spaces, tabs, newlines) into a single space
    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()


# ---------------------------------------------------------------------------
# Core patch function
# ---------------------------------------------------------------------------

def _line_of(content: str, offset: int) -> int:
    """1-based line number of ``offset`` in ``content``."""
    return content.count("\n", 0, offset) + 1


def _refuse_if_ambiguous(
    content: str,
    spans: list[tuple[int, int]],
    note_id: str,
    search_text: str,
    attempted: list[PatchPassLevel],
) -> None:
    if len(spans) > 1:
        raise PatchError(
            note_id=note_id,
            search_text=search_text,
            passes_attempted=list(attempted),
            kind=PATCH_AMBIGUOUS,
            match_count=len(spans),
            match_lines=[_line_of(content, s) for s, _ in spans],
        )


def _protected_violation(
    content: str,
    start: int,
    end: int,
    replacement_text: str,
    new_content: str,
    level: PatchPassLevel,
) -> str | None:
    """Why this splice would damage a protected region, or None when it is safe."""
    from matrx_ai.processing.blocks.source_islands import list_islands

    islands = list_islands(content)
    if not islands:
        return None
    covered = []
    for isl in islands:
        if isl.end <= start or isl.start >= end:
            continue
        inside = isl.start <= start and end <= isl.end
        covers = start <= isl.start and isl.end <= end
        if inside:
            continue  # an edit wholly inside one region names that region
        if not covers:
            return (
                f"the excerpt cuts through the boundary of a protected {isl.island_type} "
                f"(line {_line_of(content, isl.start)})"
            )
        covered.append(isl)
    if level is not PatchPassLevel.EXACT and covered:
        cursor = 0
        for isl in covered:
            at = replacement_text.find(isl.raw, cursor)
            if at == -1:
                return (
                    f"a tolerant match would change the protected {isl.island_type} "
                    f"at line {_line_of(content, isl.start)} without naming it verbatim"
                )
            cursor = at + len(isl.raw)
    # Every region the patch did not touch must survive, unmoved relative to the
    # text around it (a replacement that opens an unclosed fence would swallow it).
    delta = len(replacement_text) - (end - start)
    after = {(i.start, i.end, i.island_type) for i in list_islands(new_content)}
    for isl in islands:
        if isl.end <= start:
            key = (isl.start, isl.end, isl.island_type)
        elif isl.start >= end:
            key = (isl.start + delta, isl.end + delta, isl.island_type)
        else:
            continue
        if key not in after:
            return (
                f"the result would disturb the protected {isl.island_type} at line "
                f"{_line_of(content, isl.start)}, which the patch did not name "
                "(for example an unclosed code fence swallowing it)"
            )
    return None


def _splice(
    content: str,
    start: int,
    end: int,
    replacement_text: str,
    level: PatchPassLevel,
    note_id: str,
    search_text: str,
    attempted: list[PatchPassLevel],
) -> PatchResult:
    new_content = content[:start] + replacement_text + content[end:]
    reason = _protected_violation(content, start, end, replacement_text, new_content, level)
    if reason is not None:
        raise PatchError(
            note_id=note_id,
            search_text=search_text,
            passes_attempted=list(attempted),
            kind=PATCH_PROTECTED_BLOCK,
            match_count=1,
            match_lines=[_line_of(content, start)],
            message=(
                f"Patch refused on '{note_id}': {reason}. Nothing was changed.\n"
                f"Search text (first 200 chars): {search_text[:200]!r}\n"
                "Remedy: copy the excerpt verbatim from the current content, and either edit "
                "entirely inside the protected block, entirely outside it, or include the whole "
                "block exactly and carry it through unchanged."
            ),
        )
    return PatchResult(
        new_content=new_content,
        matched_at=level,
        original_snippet=content[start:end],
        start=start,
        end=end,
    )


def _exact_spans(content: str, needle: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    if not needle:
        return spans
    i = content.find(needle)
    while i != -1:
        spans.append((i, i + len(needle)))
        i = content.find(needle, i + 1)
    return spans


def apply_patch(
    content: str,
    search_text: str,
    replacement_text: str,
    note_id: str = "<unknown>",
) -> PatchResult:
    """
    Find `search_text` inside `content` using progressively fuzzy matching and
    replace it with `replacement_text` — in exactly one place.

    Raises PatchError (kind no_match / ambiguous / protected_block); never
    edits a place the excerpt does not uniquely name.
    """
    attempted: list[PatchPassLevel] = []

    # --- Pass 1: Exact ---
    attempted.append(PatchPassLevel.EXACT)
    spans = _exact_spans(content, search_text)
    if spans:
        _refuse_if_ambiguous(content, spans, note_id, search_text, attempted)
        s, e = spans[0]
        return _splice(content, s, e, replacement_text, PatchPassLevel.EXACT, note_id, search_text, attempted)

    # --- Pass 2: Whitespace-normalized ---
    attempted.append(PatchPassLevel.WHITESPACE_NORMALIZED)
    norm_search = _normalize_whitespace(search_text)
    words = [re.escape(part) for part in re.split(r"[ \t]+", norm_search)]
    if norm_search.strip():
        pattern = re.compile(r"[ \t]+".join(words))
        spans = [(m.start(), m.end()) for m in pattern.finditer(content) if m.end() > m.start()]
        if spans:
            _refuse_if_ambiguous(content, spans, note_id, search_text, attempted)
            s, e = spans[0]
            return _splice(
                content, s, e, replacement_text, PatchPassLevel.WHITESPACE_NORMALIZED,
                note_id, search_text, attempted,
            )

    # --- Pass 3: Blank-lines-stripped ---
    attempted.append(PatchPassLevel.BLANK_LINES_STRIPPED)
    escaped_lines = [
        r"[ \t]+".join(re.escape(w) for w in ln.strip().split())
        for ln in search_text.splitlines()
        if ln.strip()
    ]
    if escaped_lines:
        pattern = re.compile(r"[ \t]*(?:\n[ \t]*)+".join(escaped_lines))
        spans = [(m.start(), m.end()) for m in pattern.finditer(content)]
        if spans:
            _refuse_if_ambiguous(content, spans, note_id, search_text, attempted)
            s, e = spans[0]
            return _splice(
                content, s, e, replacement_text, PatchPassLevel.BLANK_LINES_STRIPPED,
                note_id, search_text, attempted,
            )

    # --- Pass 4: Lenient (all whitespace + punctuation/unicode normalized) ---
    attempted.append(PatchPassLevel.LENIENT)
    lenient_content = _lenient_normalize(content)
    lenient_search = _lenient_normalize(search_text)
    if lenient_search and lenient_search in lenient_content:
        lwords = lenient_search.split()
        if lwords:
            word_pattern = re.compile(r"\s+".join(re.escape(w) for w in lwords), re.IGNORECASE | re.DOTALL)
            spans = [(m.start(), m.end()) for m in word_pattern.finditer(content)]
            if spans:
                _refuse_if_ambiguous(content, spans, note_id, search_text, attempted)
                s, e = spans[0]
                return _splice(
                    content, s, e, replacement_text, PatchPassLevel.LENIENT,
                    note_id, search_text, attempted,
                )

    raise PatchError(note_id=note_id, search_text=search_text, passes_attempted=attempted)
