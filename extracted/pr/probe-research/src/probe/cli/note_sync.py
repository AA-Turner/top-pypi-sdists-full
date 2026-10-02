"""The document-agnostic half of syncing a note as a local file.

WHAT LIVES HERE AND WHAT DOES NOT. Two note documents are edited as files now --
the team note (`team_note_file`) and an entity's note (`notes_file`) -- and they
share the FILE discipline exactly: three paths, a base copy that records what the
server holds, an atomic 0600 commit, and a local diff3 merge. They do NOT share a
conflict protocol, and that is the seam:

    team note     the SERVER merges. A push answers `merged`/`body`, or raises a
                  ConflictError already carrying `merged_body`.
    entity note   the CLIENT merges. A push answers 409 with a version and NO
                  body (a write token does not imply read -- see
                  app/notes/schemas.py::SubNoteWriteOut), so the caller re-reads
                  through the read door and merges here.

So `push` and `pull` stay with their document. Folding both into one function
here would mean a mode flag threaded through every branch of the most
loss-bearing code in the CLI, which is the opposite of what splitting it out is
for. What IS shared is below, and it is the part where a mistake destroys text.

THE INVARIANT EVERYTHING HERE PROTECTS: *the base copy always equals the text the
file was derived from.* `commit` is the only writer of that pair, and
`Merged.wrote` is why `merge_into_file` reports whether the file actually
received the text -- advancing the base to a head the file never got is precisely
how the next push deletes everything that head added.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from probe.sdk.durable import write_text_atomic
from probe.sdk.merge3 import merge3


@dataclass(frozen=True, slots=True)
class Paths:
    document: Path
    base: Path
    meta: Path
    lock: Path
    #: Which backend+credential the DOCUMENT on disk belongs to.
    owner: str
    #: Where that answer is recorded, beside the document rather than in the
    #: per-owner state directory -- it has to be readable when the current
    #: owner is NOT the one that wrote the file, which is the whole point.
    stamp: Path


@dataclass(frozen=True, slots=True)
class Report:
    """What one reconcile did, in terms a status line or a hook can render."""

    pushed: bool = False
    pulled: bool = False
    merged: bool = False
    conflicted: bool = False
    version: int = 0
    detail: str = ""


class Unreadable(Exception):
    """The file is there and cannot be read. NOT the same as absent.

    Collapsing the two is how a dirty document with one bad byte becomes "no
    local edits": push finds nothing to send and pull then overwrites it with
    the server's copy. Absence is a fact; unreadable is an unknown, and an
    unknown must stop the reconcile rather than be treated as the empty case.
    """


def read_text(path: Path) -> str | None:
    """The file's text, or None when it does not exist. Raises `Unreadable`
    when it exists but cannot be decoded or opened."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError) as exc:
        raise Unreadable(f"{path}: {exc}") from exc


def read_meta(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return {}


def commit(
    where: Paths,
    *,
    body: str,
    version: int,
    write_document: bool,
    extra: dict | None = None,
) -> None:
    """Record `body` as the base copy at `version`. Caller holds the lock.

    Base and meta are written in that order on purpose. A crash between them
    leaves a base copy whose version is stale, which makes the next push send a
    correct document with an old base version -- a merge, which is safe. The
    other order would claim a version for a body it does not have, which is a
    silent wrong merge.

    THE STAMP FOLLOWS THE DOCUMENT, never the base. It answers "whose text is in
    the file", so writing it while leaving another credential's document in place
    is how one tenant's note becomes labelled as another's -- and the next push
    then reads that label as permission and sends it. Stamping only when this
    call also writes the document keeps the label and the bytes in step.
    """
    where.base.parent.mkdir(parents=True, exist_ok=True)
    write_text_atomic(where.base, body, mode=0o600)
    write_text_atomic(
        where.meta,
        json.dumps({"version": version, "owner": where.owner, **(extra or {})}, indent=2),
        mode=0o600,
    )
    if write_document:
        where.document.parent.mkdir(parents=True, exist_ok=True)
        # 0600 like the other two. This is the team's private prose and the
        # machine is shared; inheriting the umask default would leave the whole
        # document world-readable on exactly the hosts where that matters.
        write_text_atomic(where.document, body, mode=0o600)
        write_text_atomic(where.stamp, where.owner, mode=0o600)


def stamp_matches(where: Paths, stamp: str | None) -> bool:
    """Is the document at this path ours?

    An UNSTAMPED document is ours: it predates the stamp, and refusing to touch
    it would wedge every machine that upgraded rather than re-installed.

    WHAT THIS CANNOT ANSWER, deliberately. `commit` writes the document and
    then the stamp, so a process killed between the two leaves one credential's
    bytes under another's label, and this returns True for it. Hashing the body
    into the stamp does NOT close that: the agent edits the document constantly
    and every edit would read as a mismatch, so the check would have to treat
    "edited" and "written by someone else" as the same thing -- which turns the
    ordinary case into a refusal to sync. The window is one process death
    between two adjacent atomic writes; the cost of closing it is a
    write-ahead protocol, and it is not worth one here.
    """
    return stamp is None or stamp.strip() == where.owner


def one_trailing_newline(text: str) -> str:
    """`text` ending in exactly one newline, or empty if it was empty."""
    if not text:
        return text
    return text.rstrip("\n") + "\n"


@dataclass(frozen=True, slots=True)
class Merged:
    """What one local three-way merge did to the document.

    `wrote` is the load-bearing one. The base copy may only advance to the
    server's head when the FILE now derives from that head -- when the merge
    could not be written, the file is still derived from the OLD base, and
    recording the head as its base is precisely how the next push deletes
    everything the head added: it would carry `base_version == current`, and
    the server applies that straight.
    """

    conflicted: bool = False
    detail: str = ""
    wrote: bool = False


def merge_into_file(
    where: Paths,
    *,
    base: str,
    theirs: str,
    theirs_version: int,
    current: str,
    label: str = "note",
    merge=None,
) -> Merged:
    """Merge `theirs` into the document. Caller holds the lock.

    `merge` defaults to `merge3`, the server's own diff3, so a document this
    writes is one the server would have produced from the same three texts. It is
    injectable because each document's module owns the name its tests patch --
    moving the call in here must not silently disarm those patches. A clean merge lands
    silently; a real conflict lands WITH markers, because the alternative is
    choosing a side, and the agent that is about to read this file is the only
    thing on the machine that can tell which side is right.
    """
    # ONE TRAILING NEWLINE ON ALL THREE, before diff3 sees them. A missing final
    # newline is not an edit anybody made -- but to a line-based merge it makes
    # the document's LAST line differ on that side, so two paragraphs appended
    # at the same point come back as a conflict instead of both landing.
    #
    # It is not hypothetical: `brief()` is `body.strip()`, and every base copy
    # written from a brief before this release is on disk stripped. Those
    # machines would each hit one spurious conflict on their first merge.
    base, current, theirs = (one_trailing_newline(s) for s in (base, current, theirs))
    try:
        result = (merge or merge3)(base, current, theirs, theirs_version=theirs_version)
    except Exception as exc:  # noqa: BLE001 - MergeTooLarge, and anything else, must not lose text
        # THE FILE IS LEFT EXACTLY AS IT IS. Its edits are unsent, not lost, and
        # the next reconcile tries again against a fresher head.
        return Merged(detail=f"could not merge the {label} locally ({exc}); left as it is")
    if read_text(where.document) != current:
        # It moved again inside the lock's own window. Writing now would drop
        # whatever arrived; the next reconcile merges from a newer base.
        return Merged(detail="file changed while merging; next reconcile will merge it")
    write_text_atomic(where.document, result.text, mode=0o600)
    if result.conflicted:
        return Merged(
            conflicted=True,
            wrote=True,
            detail=(
                f"{result.conflict_count} conflict(s) written into {where.document}; "
                "resolve the markers and they sync next session"
            ),
        )
    return Merged(wrote=True)
