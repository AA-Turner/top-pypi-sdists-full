"""The supersede-marker parser, vendored from ``app/core/superseded.py``.

A struck claim (`> **SUPERSEDED** ...` opening a blockquote, the retracted text
inside it) is folded out of the team-note block that lands in every session's
instruction file: the marker line survives — that something was retracted, when
and why, is current context — and the struck text does not. Without this, a
strike keeps costing every prompt on every machine until someone physically
deletes it, which is the exact staleness the marker exists to end.

VENDORED, NOT IMPORTED. The CLI cannot depend on the server package, so this is
a copy of the three definitions that make up the convention. The two copies are
pinned together by ``tests/unit/test_superseded_cli_parity.py`` in the repo
root, which imports both and fails on any behavioural drift — edit the server
module first, then mirror here.

The collapsed form is NOT edit-safe. Edits target the team-note FILE, which
always keeps the verbatim bytes; only the rendered block is collapsed.
"""

from __future__ import annotations

import re

#: The token that opens a superseded region, at the start of a blockquote line.
MARKER = "**SUPERSEDED**"

_QUOTE = re.compile(r"^\s{0,3}>\s?")
_MARKER_LINE = re.compile(r"^\s{0,3}>\s*\*\*SUPERSEDED\*\*", re.IGNORECASE)


def _is_quote(line: str) -> bool:
    return bool(_QUOTE.match(line))


def superseded_regions(body: str) -> list[tuple[int, int]]:
    """Half-open [start, end) line ranges of every superseded region.

    A region starts at a blockquote line carrying the marker and runs to the
    end of that blockquote. Empty when the document has none — which costs
    nothing, and is every document written before the convention existed.
    """
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


def collapse(body: str) -> str:
    """The document with retracted claims folded away, keeping the marker line.

    IDEMPOTENT, and byte-identical to the input when no marker exists — the
    render current-check hashes what this returns, so any instability here
    re-renders every instruction file on every sync forever.
    """
    regions = superseded_regions(body)
    if not regions:
        return body

    lines = body.splitlines(keepends=True)
    drop: set[int] = set()
    for start, end in regions:
        # Keep the marker line: "a claim here was retracted on this date, for
        # this reason" is current context, not retracted content.
        drop.update(range(start + 1, end))
    return "".join(line for number, line in enumerate(lines) if number not in drop)
