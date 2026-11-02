"""
line_diff.py — how two versions of a file differ, line by line: kept, removed, added - the console's own
, step for step, so `seq adapter versions` counts a version's changed
lines as the adapter page's Versions tab counts them.

In one sentence: line_diff(a, b) splits both texts into lines → Myers' shortest edit script finds the fewest lines to
remove and add → [{"op": " " | "-" | "+", "text"}] in file order (None when they differ by more than MAX_EDITS lines, a
rewrite); diff_stat counts them; hunks keeps the changed lines with a few kept ones around them.

WHY a port and not difflib: difflib finds long matching blocks, not the fewest changes, so its "+3 −1" can differ from
the console's for the same two files.
"""
from __future__ import annotations

MAX_EDITS = 2000


def line_diff(a: str, b: str) -> list[dict] | None:
    """Each line of `b` against `a`: [{op, text}] - " " in both, "-" only in a, "+" only in b - or None for a
    rewrite."""
    x, y = str(a).split("\n"), str(b).split("\n")
    n, m = len(x), len(y)
    off = n + m
    v = [0] * (2 * off + 2)
    trace: list[list[int]] = []
    for d in range(min(off, MAX_EDITS) + 1):
        trace.append(v[off - d:off + d + 1])
        for k in range(-d, d + 1, 2):

            i = v[off + k + 1] if k == -d or (k != d and v[off + k - 1] < v[off + k + 1]) else v[off + k - 1] + 1
            j = i - k
            while i < n and j < m and x[i] == y[j]:
                i, j = i + 1, j + 1
            v[off + k] = i
            if i >= n and j >= m:
                return _walk_back(trace, x, y)
    return None


def _walk_back(trace: list[list[int]], x: list[str], y: list[str]) -> list[dict]:
    """The edit script from the rounds' furthest points, read back from the end of both files to their start."""
    out: list[dict] = []
    i, j = len(x), len(y)
    for d in range(len(trace) - 1, -1, -1):

        if d == 0:
            while i > 0 and j > 0:
                out.append({"op": " ", "text": x[i - 1]})
                i, j = i - 1, j - 1
            break
        v = trace[d]
        k = i - j
        prev_k = k + 1 if k == -d or (k != d and v[k - 1 + d] < v[k + 1 + d]) else k - 1
        pi = v[prev_k + d]
        pj = pi - prev_k
        while i > pi and j > pj:
            out.append({"op": " ", "text": x[i - 1]})
            i, j = i - 1, j - 1
        out.append({"op": "+", "text": y[j - 1]} if i == pi else {"op": "-", "text": x[i - 1]})
        i, j = pi, pj
    out.reverse()
    return out


def diff_stat(ops: list[dict]) -> dict:
    """How many lines were added and removed: {"added", "removed"}."""
    return {"added": sum(o["op"] == "+" for o in ops), "removed": sum(o["op"] == "-" for o in ops)}


def hunks(ops: list[dict], context: int = 3) -> list[dict]:
    """The changed lines with `context` kept lines around each run of changes; a skipped stretch is one {"op": "…",
    "text"} line saying how many lines it hides."""
    near = [False] * len(ops)
    for i, o in enumerate(ops):
        if o["op"] != " ":
            for k in range(max(0, i - context), min(len(ops) - 1, i + context) + 1):
                near[k] = True
    out: list[dict] = []
    skipped = 0
    for i, o in enumerate(ops):
        if near[i]:
            if skipped:
                out.append({"op": "…", "text": f"{skipped} unchanged line{'' if skipped == 1 else 's'}"})
            skipped = 0
            out.append(o)
        else:
            skipped += 1
    if skipped and out:
        out.append({"op": "…", "text": f"{skipped} unchanged line{'' if skipped == 1 else 's'}"})
    return out
