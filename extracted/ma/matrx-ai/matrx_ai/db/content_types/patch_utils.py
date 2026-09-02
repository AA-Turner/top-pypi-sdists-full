"""
Fuzzy find-and-replace patch utility for LLM-generated content edits.

Patch passes (in order, stopping at first match):
  1. Exact match
  2. Whitespace-normalized match  (collapse runs of spaces/tabs)
  3. Blank-line-stripped match    (ignore empty lines entirely)
  4. Lenient match                (normalize whitespace + strip punctuation/quotes/dashes)

If no pass matches, a structured PatchError is raised.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
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


@dataclass
class PatchError(Exception):
    note_id: str
    search_text: str
    passes_attempted: list[PatchPassLevel]
    message: str = ""

    def __post_init__(self) -> None:
        self.message = (
            f"Patch failed: no match found in note '{self.note_id}'.\n"
            f"Searched using passes: {[p.value for p in self.passes_attempted]}.\n"
            f"Search text (first 200 chars): {self.search_text[:200]!r}\n"
            "Tip: ensure the search_text is a verbatim excerpt from the current note content."
        )

    def __str__(self) -> str:
        return self.message

    def to_dict(self) -> dict:
        return {
            "error": "patch_no_match",
            "note_id": self.note_id,
            "passes_attempted": [p.value for p in self.passes_attempted],
            "search_preview": self.search_text[:200],
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

def apply_patch(
    content: str,
    search_text: str,
    replacement_text: str,
    note_id: str = "<unknown>",
) -> PatchResult:
    """
    Find `search_text` inside `content` using progressively fuzzy matching,
    replace it with `replacement_text`, and return a PatchResult.

    Raises PatchError if no pass finds a match.
    """
    attempted: list[PatchPassLevel] = []

    # --- Pass 1: Exact ---
    attempted.append(PatchPassLevel.EXACT)
    if search_text in content:
        new_content = content.replace(search_text, replacement_text, 1)
        return PatchResult(new_content, PatchPassLevel.EXACT, search_text)

    # --- Pass 2: Whitespace-normalized ---
    attempted.append(PatchPassLevel.WHITESPACE_NORMALIZED)
    norm_content = _normalize_whitespace(content)
    norm_search = _normalize_whitespace(search_text)
    if norm_search in norm_content:
        start = norm_content.index(norm_search)
        end = start + len(norm_search)
        original_snippet = _recover_original_span(content, norm_content, start, end)
        new_content = content.replace(original_snippet, replacement_text, 1)
        return PatchResult(new_content, PatchPassLevel.WHITESPACE_NORMALIZED, original_snippet)

    # --- Pass 3: Blank-lines-stripped ---
    attempted.append(PatchPassLevel.BLANK_LINES_STRIPPED)
    stripped_content = _strip_blank_lines(_normalize_whitespace(content))
    stripped_search = _strip_blank_lines(_normalize_whitespace(search_text))
    if stripped_search in stripped_content:
        # Build a regex that allows optional blank lines between every line of the search
        escaped_lines = [re.escape(ln) for ln in search_text.splitlines() if ln.strip()]
        pattern = r"(\n\s*)*".join(escaped_lines)
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            original_snippet = match.group(0)
            new_content = content[:match.start()] + replacement_text + content[match.end():]
            return PatchResult(new_content, PatchPassLevel.BLANK_LINES_STRIPPED, original_snippet)

    # --- Pass 4: Lenient (all whitespace + punctuation/unicode normalized) ---
    attempted.append(PatchPassLevel.LENIENT)
    lenient_content = _lenient_normalize(content)
    lenient_search = _lenient_normalize(search_text)
    if lenient_search and lenient_search in lenient_content:
        # Use a word-boundary-aware regex on the original content for a clean match
        # Build pattern from each word in the search, tolerating any whitespace between them
        words = lenient_search.split()
        if words:
            word_pattern = r"\s+".join(re.escape(w) for w in words)
            match = re.search(word_pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                original_snippet = match.group(0)
                new_content = content[:match.start()] + replacement_text + content[match.end():]
                return PatchResult(new_content, PatchPassLevel.LENIENT, original_snippet)

    raise PatchError(note_id=note_id, search_text=search_text, passes_attempted=attempted)


def _recover_original_span(original: str, normalized: str, norm_start: int, norm_end: int) -> str:
    """
    Given character positions in a normalized string, recover the corresponding
    substring from the original string.  Works for whitespace-normalization only
    (characters are removed/merged, never reordered).
    """
    # Map normalized positions back to original by walking both strings together
    orig_idx = 0
    norm_idx = 0
    orig_start: int | None = None
    orig_end: int | None = None

    while orig_idx < len(original) and norm_idx <= norm_end:
        if norm_idx == norm_start:
            orig_start = orig_idx
        if norm_idx == norm_end:
            orig_end = orig_idx
            break

        orig_ch = original[orig_idx]
        norm_ch = normalized[norm_idx] if norm_idx < len(normalized) else None

        if orig_ch == norm_ch:
            orig_idx += 1
            norm_idx += 1
        else:
            # original has extra whitespace that was collapsed — skip it
            orig_idx += 1

    if orig_start is None or orig_end is None:
        # Fallback: use the normalized match as-is (will work well enough)
        return normalized[norm_start:norm_end]

    return original[orig_start:orig_end]
