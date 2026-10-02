"""Three-way merge for the team note, and the marker check that keeps its
output from ever being stored.

ONE IMPLEMENTATION, TWO PLACES IT RUNS. Every write crosses the server: the
agent sync client, the dashboard editor, the assistant's targeted write, and
whatever client exists next. The server merge is what makes a stale
`base_version` an ordinary write rather than a refusal, and it lands next to the
version rows that record what it merged from, so a merge that went wrong is
diagnosable afterwards. That stays.

The agent CLI runs the SAME function locally, and needs to. Its file is a
working copy, and a client that cannot merge has only two moves when the server
has moved on: overwrite the file (losing the agent's edit) or refuse (losing the
server's). Both are wrong, and the second one wedges. Merging locally lets a
reconcile carry the server's head INTO the file before sending, which keeps the
one invariant the sync depends on: *the base copy always equals the text the
file was derived from*. When that stopped being true -- the server merged
in-flight while the agent kept typing -- the client's next push silently deleted
whatever the server had added.

Two copies of this file exist while the backend's pinned `probe-research`
catches up (`tests/unit/test_merge3_parity.py` fails the moment they differ);
the backend then imports `probe.sdk.merge3` and `app/team_notes/merge.py` is
deleted. Edit both, byte for byte, until then.

    base      the version the client edited from (loaded from team_note_versions)
      │
      ├── mine    what the client is sending now
      └── theirs  what the document became while the client was away
                  │
                  ▼
      per REGION of the base document:
        only mine changed   ──►  take mine
        only theirs changed ──►  take theirs
        both changed, same  ──►  take it once
        both changed, differ ─►  CONFLICT (markers, returned, never stored)

THE ALGORITHM IS diff3, on lines, over `difflib.SequenceMatcher`. Each side is
diffed against the base to produce hunks in BASE coordinates; overlapping hunks
from the two sides form one conflict cluster; non-overlapping hunks apply
independently. This is the same shape git uses, chosen because agents already
recognize its conflict markers and resolve them without being taught.

THE COST IS BOUNDED BY A LINE CAP, not by a timeout. `SequenceMatcher` is
quadratic in the worst case, and a timeout that fires mid-merge leaves a request
holding a half-computed document with nothing useful to return. `MERGE_MAX_LINES`
refuses the merge up front instead, and the caller degrades to the ordinary
stale-version conflict -- the behaviour every client already handles. The cap is
generous against a 100k-character document: prose runs 40-80 characters a line,
so a real document is 1k-3k lines, and only a pathological one (a newline every
few characters) reaches the cap.

`autojunk` is OFF. Its heuristic drops lines that appear in more than 1% of a
large input, which for a markdown document means blank lines and repeated
headings -- exactly the anchors a merge needs to align on. Faster and wrong is
not a trade this function gets to make.
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass

#: Refuse rather than merge above this. See the module docstring: the cap IS the
#: complexity bound, and refusing degrades to a conflict the caller already
#: handles.
MERGE_MAX_LINES = 5_000

#: Git's markers, deliberately verbatim. An agent that has resolved a merge
#: conflict in a repository resolves this one without new instructions, and any
#: editor that highlights conflicts highlights these.
CONFLICT_START = "<<<<<<<"
CONFLICT_MID = "======="
CONFLICT_END = ">>>>>>>"

#: A line that IS a marker: the token at the start of a line, alone or followed
#: by a label. Deliberately not a substring search -- a document that discusses
#: merge conflicts in prose ("lines beginning with <<<<<<< mark a conflict") must
#: stay writable, and only a line that would be PARSED as a marker is refused.
_MARKER_PREFIXES = (CONFLICT_START, CONFLICT_END)


class MergeTooLarge(Exception):
    """One of the three documents exceeds `MERGE_MAX_LINES`."""


@dataclass(frozen=True, slots=True)
class MergeResult:
    """`text` always merges cleanly when `conflicted` is False.

    When it is True, `text` carries conflict markers and is FOR THE CLIENT'S FILE
    ONLY -- `conflict_count` says how many regions need a human or an agent. The
    write path refuses marked text, so this value can never be stored by the same
    request that produced it.
    """

    text: str
    conflicted: bool
    conflict_count: int


def has_conflict_markers(body: str) -> list[int]:
    """1-based line numbers that would parse as conflict markers. Empty when clean.

    Returns the LINES rather than a bool because the refusal names them: an agent
    told "your document has conflict markers" has to go looking, and an agent told
    "lines 14, 22" fixes it. `=======` alone is not enough to refuse on: a
    markdown setext heading underline is exactly that, and refusing one would
    reject ordinary documents to catch a case the paired markers already catch.
    """
    return [
        number
        for number, line in enumerate(body.splitlines(), start=1)
        if line.startswith(_MARKER_PREFIXES)
    ]


def merge3(base: str, mine: str, theirs: str, *, theirs_version: int = 0) -> MergeResult:
    """diff3 over lines. Raises `MergeTooLarge` past the line cap.

    Short-circuits the two cases that are not really merges: nobody else changed
    anything (take mine), and both sides arrived at the same text (take it once).
    Both are common -- the first is every uncontended write that raced a version
    bump, the second is two agents recording the same fact.
    """
    if theirs == base:
        return MergeResult(text=mine, conflicted=False, conflict_count=0)
    if mine == base:
        return MergeResult(text=theirs, conflicted=False, conflict_count=0)
    if mine == theirs:
        return MergeResult(text=mine, conflicted=False, conflict_count=0)

    base_lines = base.splitlines(keepends=True)
    mine_lines = mine.splitlines(keepends=True)
    theirs_lines = theirs.splitlines(keepends=True)
    if max(len(base_lines), len(mine_lines), len(theirs_lines)) > MERGE_MAX_LINES:
        raise MergeTooLarge(
            f"document exceeds {MERGE_MAX_LINES} lines; merged on the client or resolved by hand"
        )

    mine_hunks = _hunks(base_lines, mine_lines)
    theirs_hunks = _hunks(base_lines, theirs_lines)

    out: list[str] = []
    conflicts = 0
    cursor = 0  # position in base_lines already emitted
    for cluster in _clusters(mine_hunks, theirs_hunks):
        start, end, in_mine, in_theirs = cluster
        out.extend(base_lines[cursor:start])
        mine_region = _apply(base_lines, in_mine, start, end)
        theirs_region = _apply(base_lines, in_theirs, start, end)
        if not in_theirs:
            out.extend(mine_region)
        elif not in_mine:
            out.extend(theirs_region)
        elif mine_region == theirs_region:
            out.extend(mine_region)
        elif _both_pure_inserts(in_mine, in_theirs):
            # BOTH SIDES ADDED TEXT AT THE SAME POINT AND NEITHER REMOVED ANY.
            # Generic diff3 calls this a conflict. For this document it is the
            # single most common write there is: two agents each appending a
            # paragraph at the end, which the `append` primitive used to make
            # concurrency-safe by construction. Taking both restores that
            # property. It is safe precisely because nothing was deleted -- the
            # worst outcome is two paragraphs where a person might have written
            # one, which is visible in the document and fixed with an edit. A
            # conflict here would instead block the write and put markers in
            # front of an agent for the ordinary case.
            #
            # Theirs first: it is already committed and other people may have
            # read it, so it keeps its position and the newcomer lands after.
            out.extend(_terminated(theirs_region))
            out.extend(mine_region)
        else:
            conflicts += 1
            out.extend(_conflict_block(mine_region, theirs_region, theirs_version))
        cursor = end
    out.extend(base_lines[cursor:])
    return MergeResult(text="".join(out), conflicted=conflicts > 0, conflict_count=conflicts)


def _hunks(base_lines: list[str], other_lines: list[str]) -> list[tuple[int, int, list[str]]]:
    """Non-equal opcodes as `(base_start, base_end, replacement)`, base coordinates."""
    matcher = difflib.SequenceMatcher(None, base_lines, other_lines, autojunk=False)
    return [
        (i1, i2, other_lines[j1:j2])
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
        if tag != "equal"
    ]


def _clusters(
    mine: list[tuple[int, int, list[str]]],
    theirs: list[tuple[int, int, list[str]]],
) -> list[tuple[int, int, list[tuple[int, int, list[str]]], list[tuple[int, int, list[str]]]]]:
    """Group hunks into regions that must be decided together.

    Two hunks belong to the same cluster when their BASE ranges overlap, and the
    grouping is transitive: expanding a cluster to swallow an overlapping hunk can
    bring in a further hunk on the other side, so the expansion repeats until it
    stops growing. Without the repeat, a mine-hunk spanning two theirs-hunks would
    emit the second theirs-hunk twice -- once inside the cluster and once as its
    own -- which duplicates text rather than conflicting on it.

    An INSERTION is a zero-width base range. Two insertions at the same point
    genuinely collide, so ranges are treated as overlapping when they share a
    point, but a zero-width range abutting the END of a real one does not: that is
    an insert after a replaced block, which is independent.
    """
    tagged = [(h[0], h[1], "m", h) for h in mine] + [(h[0], h[1], "t", h) for h in theirs]
    tagged.sort(key=lambda item: (item[0], item[1]))
    clusters: list = []
    index = 0
    while index < len(tagged):
        start, end, side, hunk = tagged[index]
        in_mine = [hunk] if side == "m" else []
        in_theirs = [hunk] if side == "t" else []
        index += 1
        grew = True
        while grew:
            grew = False
            while index < len(tagged):
                nstart, nend, nside, nhunk = tagged[index]
                overlaps = nstart < end or (nstart == end and nstart == start)
                if not overlaps:
                    break
                end = max(end, nend)
                (in_mine if nside == "m" else in_theirs).append(nhunk)
                index += 1
                grew = True
        clusters.append((start, end, in_mine, in_theirs))
    return clusters


def _both_pure_inserts(
    mine: list[tuple[int, int, list[str]]], theirs: list[tuple[int, int, list[str]]]
) -> bool:
    """True when every hunk on BOTH sides is a zero-width insertion.

    Zero width means the hunk replaces no base lines, so applying both sides
    cannot drop anything either of them kept. That is the whole justification for
    taking both instead of conflicting -- the moment one side also deletes or
    replaces, "take both" would resurrect text that side removed on purpose.
    """
    return all(h[0] == h[1] for h in mine) and all(h[0] == h[1] for h in theirs)


def _apply(
    base_lines: list[str], hunks: list[tuple[int, int, list[str]]], start: int, end: int
) -> list[str]:
    """One side's text for the base range `[start, end)`.

    Base lines the side left alone are carried through, so a cluster wider than a
    side's own hunks still compares like-for-like against the other side.
    """
    out: list[str] = []
    cursor = start
    for h_start, h_end, replacement in hunks:
        out.extend(base_lines[cursor:h_start])
        out.extend(replacement)
        cursor = h_end
    out.extend(base_lines[cursor:end])
    return out


def _conflict_block(mine: list[str], theirs: list[str], theirs_version: int) -> list[str]:
    """Git-shaped markers, with the remote side labelled by its version.

    The version is on the marker because resolving a conflict often means going
    and reading that version -- and it is the number the client sends back as its
    base on the retry.
    """
    remote = f"the team note on the server (version {theirs_version})"
    return [
        f"{CONFLICT_START} your local edit\n",
        *_terminated(mine),
        f"{CONFLICT_MID}\n",
        *_terminated(theirs),
        f"{CONFLICT_END} {remote}\n",
    ]


def _terminated(lines: list[str]) -> list[str]:
    """Guarantee the last line ends with a newline, so the next marker starts its
    own line. A side whose final line is unterminated (the document's last line,
    with no trailing newline) would otherwise run straight into `=======`."""
    if lines and not lines[-1].endswith("\n"):
        return [*lines[:-1], lines[-1] + "\n"]
    return list(lines)
