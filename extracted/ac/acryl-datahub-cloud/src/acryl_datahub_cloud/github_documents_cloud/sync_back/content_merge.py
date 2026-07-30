"""Three-way text merge for concurrent DataHub and GitHub document edits."""

from __future__ import annotations

import difflib
from dataclasses import dataclass
from typing import List, Sequence, Tuple


@dataclass(frozen=True)
class MergeResult:
    """Outcome of merging import-time, DataHub, and current GitHub content."""

    content: str
    had_overlapping_edits: bool


@dataclass(frozen=True)
class _Edit:
    base_start: int
    base_end: int
    new_lines: Tuple[str, ...]


def three_way_merge(base: str, ours: str, theirs: str) -> MergeResult:
    """Merge three text versions with a common ancestor.

    Non-overlapping edits from DataHub (``ours``) and GitHub (``theirs``) are
    combined. When both sides changed the same region differently, the DataHub
    version is kept.
    """
    if ours == theirs:
        return MergeResult(content=ours, had_overlapping_edits=False)
    if ours == base:
        return MergeResult(content=theirs, had_overlapping_edits=False)
    if theirs == base:
        return MergeResult(content=ours, had_overlapping_edits=False)

    base_lines = _split_lines(base)
    our_lines = _split_lines(ours)
    their_lines = _split_lines(theirs)

    merged_lines, had_overlap = _merge_line_lists(base_lines, our_lines, their_lines)
    content = _join_lines(merged_lines, base, ours, theirs)
    return MergeResult(content=content, had_overlapping_edits=had_overlap)


def _split_lines(text: str) -> List[str]:
    if text == "":
        return []
    return text.splitlines()


def _join_lines(lines: Sequence[str], *originals: str) -> str:
    content = "\n".join(lines)
    if any(original.endswith("\n") for original in originals if original):
        content += "\n"
    return content


def _edits_from_diff(base: List[str], other: List[str]) -> List[_Edit]:
    edits: List[_Edit] = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base, other).get_opcodes():
        if tag == "equal":
            continue
        edits.append(_Edit(i1, i2, tuple(other[j1:j2])))
    return edits


def _merge_line_lists(
    base: List[str], ours: List[str], theirs: List[str]
) -> Tuple[List[str], bool]:
    ours_edits = _edits_from_diff(base, ours)
    theirs_edits = _edits_from_diff(base, theirs)

    result: List[str] = []
    had_overlap = False
    pos = 0
    oi = 0
    ti = 0

    while pos < len(base) or oi < len(ours_edits) or ti < len(theirs_edits):
        next_o = ours_edits[oi] if oi < len(ours_edits) else None
        next_t = theirs_edits[ti] if ti < len(theirs_edits) else None

        next_pos = len(base)
        if next_o is not None:
            next_pos = min(next_pos, next_o.base_start)
        if next_t is not None:
            next_pos = min(next_pos, next_t.base_start)

        while pos < next_pos:
            result.append(base[pos])
            pos += 1

        o_at = next_o if next_o is not None and next_o.base_start == pos else None
        t_at = next_t if next_t is not None and next_t.base_start == pos else None

        if o_at is None and t_at is None:
            break

        if o_at is not None and t_at is None:
            pos, oi, ti, had_overlap = _apply_one_sided_edit(
                result, o_at, pos, oi, ti, theirs_edits, had_overlap
            )
            continue

        if t_at is not None and o_at is None:
            pos, ti, oi, had_overlap = _apply_one_sided_edit(
                result, t_at, pos, ti, oi, ours_edits, had_overlap
            )
            continue

        assert o_at is not None and t_at is not None
        pos, oi, ti, had_overlap = _apply_both_edits(
            result, o_at, t_at, pos, oi, ti, had_overlap
        )

    while pos < len(base):
        result.append(base[pos])
        pos += 1

    return result, had_overlap


def _apply_one_sided_edit(
    result: List[str],
    applied: _Edit,
    pos: int,
    applied_index: int,
    pending_index: int,
    pending_edits: Sequence[_Edit],
    had_overlap: bool,
) -> Tuple[int, int, int, bool]:
    result.extend(applied.new_lines)
    pos = applied.base_end
    applied_index += 1
    pending_index, overlap = _skip_subsumed_edits(applied, pending_edits, pending_index)
    return pos, applied_index, pending_index, had_overlap | overlap


def _apply_both_edits(
    result: List[str],
    o_at: _Edit,
    t_at: _Edit,
    pos: int,
    oi: int,
    ti: int,
    had_overlap: bool,
) -> Tuple[int, int, int, bool]:
    if _edits_overlap(o_at, t_at):
        had_overlap = True
        result.extend(o_at.new_lines)
    else:
        result.extend(o_at.new_lines)
        result.extend(t_at.new_lines)
    pos = max(o_at.base_end, t_at.base_end)
    return pos, oi + 1, ti + 1, had_overlap


def _skip_subsumed_edits(
    applied: _Edit, pending: Sequence[_Edit], index: int
) -> Tuple[int, bool]:
    had_overlap = False
    while index < len(pending):
        pending_edit = pending[index]
        if pending_edit.base_start >= applied.base_end:
            break
        if not _edits_overlap(applied, pending_edit):
            break
        had_overlap = True
        if pending_edit.base_end <= applied.base_end:
            index += 1
        else:
            break
    return index, had_overlap


def _edits_overlap(left: _Edit, right: _Edit) -> bool:
    if left.base_start == right.base_start:
        return True
    return left.base_start < right.base_end and right.base_start < left.base_end
