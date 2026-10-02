"""An entity's note as a local file: checkout, edit with ordinary tools, push.

THE SHAPE, and why it is not the team note's. Both hold a note as a file on the
`note_sync` primitives -- three paths, a base copy, an atomic 0600 commit, a
local diff3 merge. They differ in who merges:

    team note     the SERVER merges and answers with the merged body.
    entity note   the SERVER refuses with a version and NO body, because a write
                  token does not imply read (app/notes/schemas.py, and
                  app/core/notes.py::stale_replace). So this module re-reads
                  through the READ door and merges here.

    checkout ──► <state>/notes/<kind>/<uuid>[/<sub>].md      the file you edit
             └─► <state>/notes/<kind>/<uuid>[/<sub>].base    what the server has
                 ............................... .meta       its version + op key

FOUR THINGS THAT WOULD SILENTLY DESTROY TEXT, each with the reason it is here:

1. THE BASE ADVANCES ONLY ON A LANDED WRITE. `note_sync.Merged.wrote` is the
   gate. A base recording a head the file never received tells the next push
   "this file descends from the head", and the server applies everything that
   head added as deletions.

2. A CONFLICT ADVANCES THE BASE TO THE HEAD IT MERGED ONTO. Leaving the base at
   the original would re-compare the resolution against pre-conflict text and
   raise the identical conflict forever -- an infinite loop, reproduced against
   the real `merge3`. The resolution is a descendant of the HEAD, so the head is
   its ancestor.

3. AN UNRESOLVED FILE IS NEVER SENT. Pushing markers stores them as the
   document, and the next reader treats `<<<<<<<` as prose.

4. A RETRY REUSES ITS OP KEY -- the CLIENT half only, and that is the whole
   truth of it today. A push whose response was lost is retried; with a stable
   key the server COULD recognise the replay. It does not yet (TODOS.md), so
   this is plumbing of the right shape, not a guarantee: a retry after a lost
   response can still merge the caller's own committed text back in and
   duplicate it (A+B+A). The key is minted BEFORE the send so it survives a
   crash, and cleared only on a landed one.

AND ONE THAT WOULD DESTROY ANOTHER SESSION'S: the paths are entity-addressed, so
two sessions on one machine resolve the same file. `claim()` refuses the second
checkout while the first has unpushed edits. Seven agent sessions share this box.
"""

from __future__ import annotations

import re
import uuid

from probe.cli.note_sync import (
    Merged,
    Paths,
    Report,
    Unreadable,
    commit,
    merge_into_file,
    read_meta,
    read_text,
)
from probe.sdk.durable import file_lock
from probe.version_policy import state_dir

#: Conflict markers `merge3` writes. A file still carrying one is not a document.
CONFLICT_MARKER = re.compile(r"^(<{7}|={7}|>{7})", re.M)


def paths_for(settings, kind: str, entity_id: str, sub_note_id: str | None = None) -> Paths:
    """Where one entity note's three files live.

    ENTITY-ADDRESSED on purpose: `push` then finds the file from `--run <slug>`
    alone, with no path to remember and nothing to mistype. The cost is that two
    sessions resolve the same path, which `claim` answers rather than the layout.

    NOT the working directory. A note keeps "customer and commercial facts, legal
    status, incident history" verbatim, and cwd is usually a git work tree on a
    shared host -- one `git add -A` from committing a customer's prose. 0600 in
    the state dir is the same answer `team_note_file` already gives.
    """
    root = state_dir() / "notes" / kind / entity_id
    stem = sub_note_id or "note"
    base_dir = root if sub_note_id is None else root / "sub"
    document = base_dir / f"{stem}.md"
    return Paths(
        document=document,
        base=base_dir / f"{stem}.base",
        meta=base_dir / f"{stem}.meta.json",
        lock=base_dir / f"{stem}.lock",
        owner=getattr(settings, "base_url", "") or "",
        stamp=base_dir / f"{stem}.owner",
    )


def has_conflict_markers(text: str) -> bool:
    return bool(CONFLICT_MARKER.search(text))


def dirty(where: Paths) -> bool:
    """Does the file hold edits the server has not seen?"""
    try:
        document = read_text(where.document)
    except Unreadable:
        # Unreadable is an UNKNOWN, never the empty case: treating it as clean is
        # how a dirty file with one bad byte gets overwritten by a checkout.
        return True
    return document is not None and document != (read_text(where.base) or "")


def claim(where: Paths, *, steal: bool = False) -> str | None:
    """None when this checkout may proceed, else why it may not.

    The paths are entity-addressed, so a second session checking out the same
    note resolves the same file -- and overwriting it would destroy edits that
    were never sent, before any merge could see them.
    """
    if steal or not dirty(where):
        return None
    return (
        f"{where.document} already has edits that were never pushed. "
        "Push them, or re-run with --steal to discard them and take a fresh copy."
    )


def checkout(where: Paths, *, body: str, version: int) -> Report:
    """Write the server's document and record it as the base. Caller holds nothing."""
    with file_lock(where.lock):
        commit(where, body=body, version=version, write_document=True)
    return Report(pulled=True, version=version, detail=str(where.document))


def push(where: Paths, *, send, fetch, label: str = "note", force: bool = False) -> Report:
    """Send the file, merging locally if the document moved. Never raises for a refusal.

    `send(text, base_version, op_key)` performs the replace and returns the new
    version; it raises `errors.ConflictError` when the precondition failed.
    `fetch()` returns `(body, version)` through the READ door -- the 409 cannot
    carry the body, so a merge needs this second call.
    """
    from probe.sdk import errors

    try:
        with file_lock(where.lock):
            document = read_text(where.document)
            base = read_text(where.base)
            meta = read_meta(where.meta)
    except Unreadable as exc:
        return Report(detail=f"refusing to push: {exc}")

    if document is None:
        return Report(detail=f"nothing checked out at {where.document}")

    if has_conflict_markers(document):
        # Storing markers would make `<<<<<<<` the document every later reader sees.
        return Report(
            conflicted=True,
            detail=(
                f"{where.document} still has unresolved conflict markers; "
                "resolve them, then push again"
            ),
        )

    if base is None and not force:
        # WITHOUT AN ANCESTOR THERE IS NO THREE-WAY MERGE. A two-way merge cannot
        # tell your deletion from their addition, and an empty base reads every
        # line of the head as a deletion -- a silent full overwrite wearing a
        # merge's clothing. Refuse, and name both ways forward.
        return Report(
            detail=(
                f"no base copy for {where.document}, so a safe merge is impossible. "
                "Re-run checkout and re-apply your edit, or push --force to replace "
                "the server's document with this file."
            ),
        )

    version = int(meta.get("version", 0))
    if document == (base or ""):
        return Report(version=version, detail="no local edits")

    # MINTED BEFORE THE SEND AND PERSISTED, so a retry after a lost response
    # carries the same key. The server does not read it yet (TODOS.md): this
    # makes the replay RECOGNISABLE, it does not yet make it safe.
    op_key = meta.get("op_key") or uuid.uuid4().hex
    if meta.get("op_key") != op_key and base is not None:
        # ONLY WHEN A BASE ALREADY EXISTS. Committing `base or ""` here would
        # write an EMPTY base file under --force, and a later push without
        # --force would then sail past the `base is None` refusal above and
        # three-way merge against an empty ancestor -- the silent full
        # overwrite that refusal exists to prevent. Under --force the key is
        # carried in memory for this attempt instead; a --force retry is an
        # explicit act either way.
        with file_lock(where.lock):
            commit(
                where,
                body=base,
                version=version,
                write_document=False,
                extra={"op_key": op_key},
            )

    try:
        new_version = send(document, None if force else version, op_key)
    except errors.ConflictError:
        return _merge_after_conflict(where, document=document, fetch=fetch, label=label)
    except errors.RosError as failure:
        # Network down, cap refused: the file keeps its edits and the key keeps
        # its identity, so the next push is a replay rather than a second write.
        return Report(version=version, detail=str(failure))

    with file_lock(where.lock):
        # The base records what the SERVER now holds. The document is NOT
        # rewritten: it already is that text, and rewriting it would clobber
        # anything typed between the send and this lock.
        commit(where, body=document, version=int(new_version), write_document=False)
    return Report(pushed=True, version=int(new_version))


def _merge_after_conflict(where: Paths, *, document: str, fetch, label: str) -> Report:
    """The head moved. Re-read it through the READ door and merge locally."""
    from probe.sdk import errors

    try:
        theirs, theirs_version = fetch()
    except errors.RosError as failure:
        return Report(detail=f"the {label} moved and could not be re-read ({failure})")

    with file_lock(where.lock):
        current = read_text(where.document)
        if current is None:
            return Report(detail=f"{where.document} disappeared while pushing")
        base = read_text(where.base) or ""
        merged: Merged = merge_into_file(
            where,
            base=base,
            theirs=theirs,
            theirs_version=int(theirs_version),
            current=current,
            label=label,
        )
        if not merged.wrote:
            # The file never received the head. Advancing the base to it would
            # tell the next push this file descends from the head, and the
            # server would apply the missing text as deletions.
            return Report(version=int(theirs_version), detail=merged.detail)
        # THE BASE BECOMES THE HEAD, conflicted or not. The text in the file is
        # now derived from the head, so the head is its ancestor. Leaving the
        # base behind is what makes a resolved conflict conflict again, forever.
        commit(
            where,
            body=theirs,
            version=int(theirs_version),
            write_document=False,
            extra={"op_key": None},
        )
    if merged.conflicted:
        return Report(conflicted=True, version=int(theirs_version), detail=merged.detail)
    return Report(merged=True, version=int(theirs_version), detail="merged; push again to send it")
