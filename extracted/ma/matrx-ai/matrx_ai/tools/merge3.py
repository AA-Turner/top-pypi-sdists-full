"""Three-way merge of one context value — two writers, one record.

``base`` is the copy a writer edited, ``mine`` its edit, ``theirs`` what the record holds now.
When the two edits touch different parts, both land: the merge applies ``mine``'s change on top
of ``theirs``. When they touch the same part — or either replaces the whole value — it is an
overlap and the merge refuses (``None``): neither write silently wins.

Text merges line by line (a checklist where each writer ticks its own item merges; two edits of
the same line overlap; two inserts at the same place overlap). JSON merges by path (two writers
setting different keys merge; the same key, or a parent and its child, overlap; a list is one
value). Pure functions — no I/O.
"""

from __future__ import annotations

import difflib
from typing import Any

#: A change to ``base``: replace base lines [i1, i2) with ``lines``.
_Hunk = tuple[int, int, list[str]]


def _hunks(base: list[str], other: list[str]) -> list[_Hunk]:
    matcher = difflib.SequenceMatcher(a=base, b=other, autojunk=False)
    return [
        (i1, i2, other[j1:j2])
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
        if tag != "equal"
    ]


def _overlap(a: _Hunk, b: _Hunk) -> bool:
    a1, a2, _ = a
    b1, b2, _ = b
    if a1 == a2 and b1 == b2:
        return a1 == b1  # two inserts at the same place
    if a1 == a2:
        return b1 < a1 < b2 or a1 == b1  # an insert inside (or at the start of) a change
    if b1 == b2:
        return a1 < b1 < a2 or a1 == b1
    return a1 < b2 and b1 < a2


def merge_text(base: str, mine: str, theirs: str) -> str | None:
    """``mine``'s change re-applied on ``theirs``, or None when the two overlap."""
    if mine == base:
        return theirs
    if theirs == base or theirs == mine:
        return mine
    base_lines = base.splitlines(keepends=True)
    my_hunks = _hunks(base_lines, mine.splitlines(keepends=True))
    their_hunks = _hunks(base_lines, theirs.splitlines(keepends=True))
    for m in my_hunks:
        for t in their_hunks:
            if _overlap(m, t):
                return None
    # Walk base once, applying whichever side changed each region.
    changes = sorted([*my_hunks, *their_hunks], key=lambda h: (h[0], h[1]))
    out: list[str] = []
    cursor = 0
    for i1, i2, lines in changes:
        out.extend(base_lines[cursor:i1])
        out.extend(lines)
        cursor = max(cursor, i2)
    out.extend(base_lines[cursor:])
    return "".join(out)


_MISSING = object()


def _leaf_changes(base: Any, other: Any, path: tuple[Any, ...] = ()) -> dict[tuple[Any, ...], Any]:
    """{path: new value or _MISSING} for every place ``other`` differs from ``base``. Dicts
    recurse by key; anything else (lists included) is one value."""
    if isinstance(base, dict) and isinstance(other, dict):
        out: dict[tuple[Any, ...], Any] = {}
        for key in set(base) | set(other):
            if key not in other:
                out[(*path, key)] = _MISSING
            elif key not in base:
                out[(*path, key)] = other[key]
            elif base[key] != other[key]:
                out.update(_leaf_changes(base[key], other[key], (*path, key)))
        return out
    return {} if base == other else {path: other}


def _related(a: tuple[Any, ...], b: tuple[Any, ...]) -> bool:
    n = min(len(a), len(b))
    return a[:n] == b[:n]


def merge_json(base: Any, mine: Any, theirs: Any) -> tuple[bool, Any]:
    """``(True, merged)`` with ``mine``'s changed paths applied on ``theirs``, or
    ``(False, None)`` when the two touch the same path (or one contains the other)."""
    if mine == base:
        return True, theirs
    if theirs == base or theirs == mine:
        return True, mine
    my_changes = _leaf_changes(base, mine)
    their_changes = _leaf_changes(base, theirs)
    for mp in my_changes:
        for tp in their_changes:
            if _related(mp, tp):
                return False, None
    import copy

    merged = copy.deepcopy(theirs)
    for path, value in my_changes.items():
        if not path:
            return False, None
        node = merged
        for key in path[:-1]:
            if not isinstance(node, dict):
                return False, None
            node = node.setdefault(key, {})
        if not isinstance(node, dict):
            return False, None
        if value is _MISSING:
            node.pop(path[-1], None)
        else:
            node[path[-1]] = copy.deepcopy(value)
    return True, merged


def merge_value(base: Any, mine: Any, theirs: Any) -> tuple[bool, Any]:
    """One entry point for a context value of either shape."""
    if isinstance(base, str) and isinstance(mine, str) and isinstance(theirs, str):
        merged = merge_text(base, mine, theirs)
        return (merged is not None), merged
    return merge_json(base, mine, theirs)


def what_changed(base: Any, theirs: Any, *, limit: int = 2000) -> str:
    """What the other writer changed, as a short unified diff (text) or path list (JSON) — what
    a second writer is told before it retries."""
    if isinstance(base, str) and isinstance(theirs, str):
        diff = difflib.unified_diff(
            base.splitlines(), theirs.splitlines(), "your copy", "now", lineterm="", n=1
        )
        text = "\n".join(diff)
    else:
        paths = _leaf_changes(base, theirs)
        text = "\n".join(
            f"{'/'.join(str(p) for p in path) or '(whole value)'}: "
            + ("removed" if value is _MISSING else repr(value)[:200])
            for path, value in paths.items()
        )
    return text if len(text) <= limit else text[:limit] + "\n…"
