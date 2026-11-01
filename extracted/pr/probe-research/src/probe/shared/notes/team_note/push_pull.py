"""send local edits and refresh the local file (three-way merge), never raising on a refusal."""

from __future__ import annotations
from pathlib import Path
from probe.sdk import errors
from probe.foundation.durable.durable import file_lock, write_text_atomic
from probe.shared.notes.sync import (  # noqa: F401 - re-exported for this module's callers
    Paths,
    Report,
    Unreadable,
    commit as _commit,
    read_meta as _read_meta,
    read_text as _read,
    stamp_matches as _stamp_matches)


def push(client, where: Paths) -> Report:
    """Send local edits, if there are any. Never raises for an ordinary refusal.

    A conflict writes the server's MERGED document -- markers and all -- into the
    file and leaves the base copy alone, so the next reconcile sees a dirty file
    and tries again once the agent has resolved it. Deliberately not committing a
    new base here: the conflicted text is not what the server stores, and
    recording it as the base would tell the next push that markers were the
    agreed document.
    """
    try:
        with file_lock(where.lock):
            document = _read(where.document)
            base = _read(where.base) or ""
            meta = _read_meta(where.meta)
            version = int(meta.get("version", 0))
            stamp = _read(where.stamp)
    except Unreadable as exc:
        return Report(detail=f"refusing to sync: {exc}")

    if document is not None and not _stamp_matches(where, stamp):
        # THE DOCUMENT ON DISK BELONGS TO A DIFFERENT BACKEND OR CREDENTIAL.
        # The state directory is keyed per owner, so a switched credential sees
        # an empty base at version 0 -- and push-before-pull would then upload
        # the PREVIOUS tenant's private note into this one as a brand new
        # document. Refuse, and let pull re-seed from the right tenant.
        return Report(
            version=version,
            detail=(
                f"{where.document} was last synced by a different backend or credential; "
                "not sending it. It will be replaced with this tenant's note."
            ),
        )

    if document is None or document == base:
        return Report(version=version)

    try:
        result = client.sync_team_note(document, base_version=version) or {}
    except errors.ConflictError as conflict:
        detail = conflict.detail if isinstance(conflict.detail, dict) else {}
        merged = detail.get("merged_body")
        if merged:
            with file_lock(where.lock):
                if _read(where.document) == document:
                    # 0600 like every other write of this file: the default
                    # umask would leave the team's whole note world-readable on
                    # exactly the shared machines where that matters.
                    write_text_atomic(where.document, merged, mode=0o600)
            return Report(
                conflicted=True,
                version=version,
                detail=(
                    f"{detail.get('conflict_count', 1)} conflict(s) written into "
                    f"{where.document}; resolve the markers and they sync next session"
                ),
            )
        return Report(version=version, detail=str(detail.get("message") or conflict))
    except errors.RosError as failure:
        # Network down, cap refused, markers still unresolved: leave the file
        # dirty and try again next session. Losing the edit would be worse than
        # carrying it.
        return Report(version=version, detail=str(failure))

    new_version = int(result.get("version", version))
    merged_body = result.get("body") if result.get("merged") else None
    settled = merged_body if merged_body is not None else document
    conflicted = False
    detail = ""
    with file_lock(where.lock):
        current = _read(where.document)
        moved = current != document
        # COMMIT THE BASE EITHER WAY. The base records what the SERVER now
        # holds, which this request just established; it is not a claim about
        # the file. Skipping it because the file moved was the bug: the next
        # push would diff a newer file against the PRE-PUSH base, both sides
        # would look like pure additions, and the merge would concatenate --
        # duplicating everything this push already committed.
        write_document = merged_body is not None and not moved
        if (
            merged_body is not None
            and moved
            and current is not None
            and _stamp_matches(where, _read(where.stamp))
        ):
            # THE SERVER MERGED WHILE THE AGENT KEPT TYPING, and this is the
            # interleaving that used to delete a teammate's paragraph. The base
            # becomes the merged body, but the FILE never received it: its next
            # push would carry `base_version == current` and the server would
            # apply that omission straight, as an ordinary deletion.
            #
            # Rebase instead: the text we sent is the common ancestor of what
            # the server now holds and what the file has become, which is
            # exactly a three-way merge. Leaving the file alone is not an
            # option, and neither is overwriting it -- one loses the server's
            # text, the other the agent's.
            rebased = _merge_into_file(
                where,
                base=document,
                theirs=merged_body,
                theirs_version=new_version,
                current=current,
            )
            write_document = False
            conflicted = rebased.conflicted
            detail = rebased.detail
            if not rebased.wrote:
                # THE FILE NEVER RECEIVED THE SERVER'S TEXT. Advancing the base
                # to it anyway would tell the next push "this file is a
                # descendant of the head", and the server would apply the
                # missing paragraphs as deletions. Leaving base and version
                # where they are makes that push carry a stale `base_version`,
                # which is exactly the case the server's merge exists for.
                return Report(
                    pushed=True,
                    merged=True,
                    version=new_version,
                    detail=detail,
                )
        _commit(where, body=settled, version=new_version, write_document=write_document)
    if moved and not detail:
        detail = "file changed during sync; next reconcile will send it"
    return Report(
        pushed=True,
        merged=merged_body is not None,
        conflicted=conflicted,
        version=new_version,
        detail=detail,
    )


def pull(client, where: Paths) -> tuple[Report, str]:
    """Refresh the local file, and return the text to inject.

    Returns `(report, injected_text)`. The injected text is the BRIEF, always --
    it is bounded, and it is what a session reads. The file gets the whole
    document, which is what the agent edits. Those are two different sizes on
    purpose.

    ONE REQUEST IN THE COMMON CASE. The brief carries `version` and `truncated`,
    and a brief that is not truncated IS the document, so a note under the brief
    budget never needs a second fetch. A larger one costs one extra request, and
    only when it has actually changed since this machine last looked.
    """
    brief = client.get_team_note_brief() or {}
    text = brief.get("text") or ""
    remote_version = int(brief.get("version", 0))

    try:
        with file_lock(where.lock):
            document = _read(where.document)
            base = _read(where.base)
            local_version = int(_read_meta(where.meta).get("version", -1))
            stamp = _read(where.stamp)
    except Unreadable as exc:
        return Report(detail=f"refusing to refresh: {exc}"), text

    # A document on disk that a DIFFERENT backend or credential last wrote is
    # not ours to overwrite. It used to be replaced outright -- "it was never
    # ours to keep" -- which silently destroyed unsynced work every time a
    # researcher switched context and came back. It is PARKED instead: the text
    # survives, labelled with the credential that wrote it, and `adopt` hands it
    # back the next time that credential is the active one.
    foreign = document is not None and not _stamp_matches(where, stamp)
    # A document with NO base copy counts as dirty. The base is what proves a
    # file is unmodified; without it there is no such proof, and the alternative
    # reading ("no base, so nothing to lose") is exactly the assumption that
    # overwrites a file after somebody cleared the state directory. A merge
    # against the empty base heals this: nothing is lost, at worst a conflict.
    dirty = document is not None and (base is None or document != base)

    if document is not None and not foreign and not dirty and local_version == remote_version:
        return Report(version=remote_version), text

    body, version = text, remote_version
    # THE BRIEF IS NOT THE DOCUMENT'S BYTES. It is `body.strip()` plus, when it
    # does not fit, section-aligned cuts (`app/team_notes/service.py::brief`), so
    # even an untruncated brief can differ from what the server stores by
    # trailing whitespace. That was harmless while the server did all merging --
    # it merged against ITS bytes. It is not harmless now: a base copy off by one
    # trailing newline makes the document's first line read as CHANGED on both
    # sides, and diff3 then reports a conflict for two edits that do not overlap
    # at all. Measured exactly that way against a live server.
    #
    # So: whenever this base copy is about to be merged or diffed against --
    # anything but a clean seed -- fetch the real document. One extra request,
    # only when there is local work to protect.
    if brief.get("truncated") or dirty or base is None:
        # SECOND REQUEST, so take the version FROM IT. Pairing this body with
        # the brief's version would record a version-N label on an N+1 body when
        # a teammate writes between the two calls -- and every later merge would
        # then run against a base the server never had.
        full = client.get_team_note() or {}
        body = full.get("body", "")
        version = int(full.get("version", remote_version))

    parked: Path | None = None
    merged_detail = ""
    conflicted = False
    try:
        with file_lock(where.lock):
            # RE-READ THE STATE, not just the document. Another reconcile can
            # have completed inside the window this request spent on the
            # network -- and if it landed a NEWER version, merging our older
            # body against the base it already advanced duplicates the
            # paragraphs it just merged, and then writes the older version
            # number over its newer one. Its work is strictly better than
            # ours; leave it alone.
            settled_version = int(_read_meta(where.meta).get("version", -1))
            if settled_version > version:
                return (
                    Report(version=settled_version, detail="a concurrent sync landed a newer version"),
                    text,
                )
            base = _read(where.base)
            current = _read(where.document)
            # RE-READ THE STAMP HERE. `foreign` was decided in a lock we
            # released to make the request, and a credential switch inside that
            # window would leave us merging our tenant's head into another
            # tenant's document -- which the next push then sends to the wrong
            # server. Cheap, and it is the only moment that matters.
            if current is not None and not _stamp_matches(where, _read(where.stamp)):
                foreign = True
            if foreign and current is not None:
                parked = park(where.document, kind="unsynced")
                current = None
            if current is not None and current != base and base is not None:
                # UNSYNCED LOCAL WORK plus a newer head. This is the case that
                # used to stop the refresh dead ("local edits not yet synced"),
                # which is why a session that could not push stayed stale
                # forever. Merging carries the head in without touching what the
                # agent wrote; the result is dirty, so the push below sends it.
                outcome = _merge_into_file(
                    where,
                    base=base,
                    theirs=body,
                    theirs_version=version,
                    current=current,
                )
                conflicted = outcome.conflicted
                merged_detail = outcome.detail
                # ONLY WHEN THE FILE ACTUALLY RECEIVED IT. The base copy is a
                # claim about what the document derives from; a merge that
                # could not be written leaves the file derived from the OLD
                # base, and recording the head there would make the next push
                # send the head's own paragraphs back as deletions.
                if outcome.wrote:
                    _commit(where, body=body, version=version, write_document=False)
            else:
                if current is not None and base is None and current.strip():
                    # No base copy at all (state cleared, or a first sync onto a
                    # machine that already had text here). merge3 against the
                    # empty base keeps both sides rather than picking one.
                    outcome = _merge_into_file(
                        where,
                        base="",
                        theirs=body,
                        theirs_version=version,
                        current=current,
                    )
                    conflicted = outcome.conflicted
                    merged_detail = outcome.detail
                    if outcome.wrote:
                        _commit(where, body=body, version=version, write_document=False)
                else:
                    _commit(where, body=body, version=version, write_document=True)
    except Unreadable as exc:
        return Report(detail=f"refusing to refresh: {exc}"), text
    detail = merged_detail
    if parked is not None:
        note = f"a document written under another credential was parked at {parked}"
        detail = f"{detail}; {note}" if detail else note
    return Report(pulled=True, conflicted=conflicted, version=version, detail=detail), text
from probe.shared.notes.team_note.parking import park  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.notes.team_note.team_note import _merge_into_file  # noqa: E402 -- pieces need each other; the front door loads this one first
