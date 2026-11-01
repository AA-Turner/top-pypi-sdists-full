"""Superseded regions: claims struck in place in a note, and `collapse`, which keeps them out of search.

Retired for writers but still live, DO NOT DELETE: old markers remain in notes, and without this search
ranks their claims as current (DESIGN.md).
"""

from __future__ import annotations

import re

#: Opens a region: `> **SUPERSEDED** <date> · v<N> · <reason>`, then `> ~~claim~~` lines. Matched at
#: line start only, so prose discussing it stays writable (same rule as `app/team_notes/merge.py`).
MARKER = "**SUPERSEDED**"

_QUOTE = re.compile(r"^\s{0,3}>\s?")
_MARKER_LINE = re.compile(r"^\s{0,3}>\s*\*\*SUPERSEDED\*\*", re.IGNORECASE)


def _is_quote(line: str) -> bool:
    return bool(_QUOTE.match(line))


def superseded_regions(body: str) -> list[tuple[int, int]]:
    """Half-open [start, end) line ranges: from a marker blockquote line to the end of that quote."""
    lines = body.splitlines()
    regions: list[tuple[int, int]] = []
    index = 0
    while index < len(lines):
        if _MARKER_LINE.match(lines[index]):
            end = index + 1
            while end < len(lines) and _is_quote(lines[end]):
                end += 1
            regions.append((index, end))
            index = end
        else:
            index += 1
    return regions


def has_superseded(body: str) -> bool:
    return bool(superseded_regions(body))


def collapse(body: str) -> str:
    """The document with struck claims folded away, marker lines kept; unchanged when it has none.

    Not edit-safe: `notes_edit` matches stored bytes, so only non-editing readers use it.
    Must stay idempotent, or projection and file hash disagree and the doc re-pushes every sweep.
    """
    regions = superseded_regions(body)
    if not regions:
        return body

    lines = body.splitlines(keepends=True)
    drop: set[int] = set()
    for start, end in regions:
        # Keep the marker line (when and why it was retracted is current context); drop the claim.
        drop.update(range(start + 1, end))
    return "".join(line for number, line in enumerate(lines) if number not in drop)
