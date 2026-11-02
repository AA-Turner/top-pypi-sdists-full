"""Diff-hunk line-reference validation for review findings (FR-004).

Resolves a finding's ``diff_side`` + coordinate against the parsed unified-diff
hunks of the reviewed file and excludes out-of-diff findings so that every
emitted finding references a coordinate present on the correct side of the diff
(SC-002).  Excluded findings are reported to the caller (for out-of-band
diagnostics) rather than emitted as findings.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - typing only
    from collections.abc import Iterable, Sequence

    from ..schemas.review.finding import FileReviewFinding

__all__ = [
    "DiffLineIndex",
    "build_diff_line_index",
    "finding_in_diff",
    "partition_findings_by_diff",
]

_HUNK_HEADER = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def _split_diff_lines(diff_text: str) -> list[str]:
    """Split unified-diff records on CR/LF only, preserving source characters."""
    if diff_text == "":
        return []

    normalized = diff_text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    if diff_text.endswith(("\r\n", "\r", "\n")):
        lines.pop()
    return lines


@dataclass
class DiffLineIndex:
    """Sets of line coordinates present on each side of a unified diff."""

    old_lines: set[int] = field(default_factory=set)
    new_lines: set[int] = field(default_factory=set)
    context_pairs: set[tuple[int, int]] = field(default_factory=set)


def build_diff_line_index(diff_text: str) -> DiffLineIndex:
    """Parse ``diff_text`` into the set of old/new line coordinates it touches.

    Removed lines (``-``) contribute an old-side coordinate, added lines (``+``)
    a new-side coordinate, and context lines (`` ``) contribute to both sides.
    Lines outside any hunk (file headers, ``\\ No newline`` markers) are ignored.
    """
    index = DiffLineIndex()
    old_line: int | None = None
    new_line: int | None = None

    for raw in _split_diff_lines(diff_text):
        header = _HUNK_HEADER.match(raw)
        if header is not None:
            old_line = int(header.group(1))
            new_line = int(header.group(2))
            continue

        if old_line is None or new_line is None:
            # Content before the first hunk header (e.g. ---/+++ lines).
            continue

        if raw.startswith("\\"):
            # "\ No newline at end of file" — not a real content line.
            continue

        if raw.startswith("+"):
            index.new_lines.add(new_line)
            new_line += 1
        elif raw.startswith("-"):
            index.old_lines.add(old_line)
            old_line += 1
        elif raw.startswith(" "):
            # Context line (leading space) is present on both sides.
            index.old_lines.add(old_line)
            index.new_lines.add(new_line)
            index.context_pairs.add((old_line, new_line))
            old_line += 1
            new_line += 1
        else:
            # Unrecognized content (e.g. truncation markers such as
            # "[... diff truncated — budget exceeded ...]") terminates the
            # active hunk so that subsequent lines cannot be indexed.
            old_line = None
            new_line = None

    return index


def finding_in_diff(finding: FileReviewFinding, index: DiffLineIndex) -> bool:
    """Return whether ``finding``'s coordinate is present on its diff side."""
    if finding.diff_side == "old":
        return finding.old_line in index.old_lines
    if finding.diff_side == "new":
        return finding.new_line in index.new_lines
    # context: coordinate pair must be an exact match from a shared unchanged row
    return (finding.old_line, finding.new_line) in index.context_pairs


def partition_findings_by_diff(
    findings: Sequence[FileReviewFinding] | Iterable[FileReviewFinding],
    diff_text: str,
) -> tuple[list[FileReviewFinding], list[FileReviewFinding]]:
    """Split ``findings`` into those inside the diff and those outside it.

    Returns a ``(kept, dropped)`` tuple; ``dropped`` findings reference a
    coordinate not present on the correct side of the diff and must not be
    emitted (FR-004 / SC-002).
    """
    index = build_diff_line_index(diff_text)
    kept: list[FileReviewFinding] = []
    dropped: list[FileReviewFinding] = []
    for finding in findings:
        if finding_in_diff(finding, index):
            kept.append(finding)
        else:
            dropped.append(finding)
    return kept, dropped
