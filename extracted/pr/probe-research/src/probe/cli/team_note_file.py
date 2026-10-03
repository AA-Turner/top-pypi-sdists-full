"""The team note as a local file: one document per machine, synced like git.

WHAT CHANGED AND WHY. Agents used to write the team note by calling an API verb.
They now edit a markdown file, because editing a file is the thing a coding agent
is best at and the thing it does without being told -- and because the operation
it used to have to compose (replace this exact span) is the awkward inverse of
what it actually did (change the text).

    fetch head ──► MERGE it into the file locally ──► push what came out
         ▲                    │                              │
         │      the agent edits the file, like any other      │
         └──────  markdown, between reconciles  ◄─────────────┘

THREE FILES, and each one is load-bearing:

    <state>/team-note/probe-team-note.md   the DOCUMENT. The agent edits this.
    <state>/team-note/<key>/base.md        the PRISTINE COPY of what the server has.
    <state>/team-note/<key>/meta.json      which version base.md is, and whose.

`base.md` is what makes "did the agent change anything" answerable without asking
the server, and it is what a merge runs against. Without it a reconcile cannot
tell an edit from a stale copy and would push the same bytes forever.

ONE DOCUMENT PER MACHINE, and that is the whole shape of this module. The
document is NOT per harness. It used to sit beside each harness's instruction
file (`~/.claude/`, `~/.codex/`, `~/.pi/agent/`) while the base copy was keyed
on the credential alone, so two harnesses shared one base and each read the
other's copy as "dirty": every session start pushed a whole document over the
other harness's, forever, and no pull ever converged them (measured: 2026-09-07
v765-v770, two byte-identical bodies alternating every ~20 minutes, three whole
sections appearing and disappearing). `source` now chooses which INSTRUCTION
FILE gets the managed block and nothing else.

THE MERGE IS LOCAL, and that is what makes "push" safe. `merge3` is the same
diff3 the server runs (`probe.sdk.merge3`); running it here means a reconcile
can carry a teammate's version into the file BEFORE sending, rather than
choosing between overwriting the file and refusing to sync. The invariant it
buys: *the base copy always equals the text the file was derived from*. When
that stopped being true -- the server merged in-flight while the agent kept
typing -- the next push silently deleted whatever the server had added.

THE LOCK IS NEVER HELD ACROSS THE NETWORK. `durable.file_lock` is an advisory
flock released only when its holder exits, so a hung HTTP call inside it would
block every other session on the machine indefinitely (its own docstring says
so). Every step runs lock → read → UNLOCK → HTTP → lock → commit, and each
commit re-checks that the file has not moved underneath it. Five agent sessions
share one home directory on a devbox; this is not theoretical.

WHAT A DEAD SESSION COSTS: nothing. A session killed before its stop hook leaves
the file dirty and the base copy behind; the next reconcile merges the server's
head into that file and pushes the result, so the edit lands late instead of
being lost. Pulling could once overwrite such an edit, which is why push used to
run first; a pull that MERGES cannot, so the order no longer carries that weight.

TEXT THAT IS NOT OURS TO PUSH IS PARKED, never deleted and never sent: a
leftover per-harness document from before this layout, and a document written
under a different credential. `park()` renames it to `<name>.unsynced-<stamp>`
with its `.owner` stamp alongside, and `adopt()` brings it back when that
credential is the active one again.
"""

from __future__ import annotations

import hashlib
import datetime as _dt
import json
import math
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from probe.cli import superseded
from probe.sdk import errors
from probe.sdk.durable import SYNC_NONE, file_lock, write_text_atomic
from probe.sdk.merge3 import merge3
from probe.version_policy import state_dir
from probe.cli.note_sync import (  # noqa: F401 - re-exported for this module's callers
    Merged as _Merged,
    Paths,
    Report,
    Unreadable,
    commit as _commit,
    merge_into_file as _merge_into_file_core,
    one_trailing_newline as _one_trailing_newline,
    read_meta as _read_meta,
    read_text as _read,
    stamp_matches as _stamp_matches,
)


def _merge_into_file(where, *, base, theirs, theirs_version, current):
    """`note_sync.merge_into_file`, labelled for this document's messages."""
    return _merge_into_file_core(
        where,
        base=base,
        theirs=theirs,
        theirs_version=theirs_version,
        current=current,
        label="team note",
        # Resolved from THIS module at call time: test_team_note.py patches
        # `team_note_file.merge3` to simulate an unmergeable document.
        merge=merge3,
    )

#: The document's filename. It sits in the STATE DIRECTORY, one per machine --
#: not beside any harness's instruction file, and nowhere near Claude Code's
#: separate `memory/` directory. See `paths()` for why the harness must not be
#: in this path. The managed instruction block names it by absolute path; the
#: note's own text never goes into CLAUDE.md or AGENTS.md, because that file is
#: delivered to the model as the user's own standing instructions (a `role:
#: user` message on Codex) and this document is prose other people's agents
#: wrote.
DOCUMENT_NAME = "probe-team-note.md"

#: Suffixes for a document that is on disk but must not be sent. The KIND is
#: load-bearing, not a label:
#:
#:   unsynced  this credential's own work, set aside when another credential
#:             took the path. `adopt` puts it BACK when we return, and the
#:             sync then sends it -- because we know its merge base: ours.
#:   legacy    a leftover per-harness copy from before there was one document
#:             per machine. NEVER adopted and never sent, whatever stamp it
#:             carries: its true merge base is unknowable, so merging it
#:             against ours reads the other harness's sections as deletions,
#:             which is the exact bug this whole change exists to end. A person
#:             folds it in by hand, or deletes it.
#:
#: The timestamp orders them and keeps a second park from clobbering the first.
PARKED_KINDS = ("unsynced", "legacy")
PARKED_GLOB = f"{DOCUMENT_NAME}.*-*"

#: What travels WITH a parked copy rather than being one: who wrote it, the
#: base it was edited from, and that base's version.
PARKED_SIDECARS = (".owner", ".base", ".meta")

#: Where a per-harness document used to live, for the one-time migration and for
#: the parked-copy sweep. Reuses `agent_rules.memory_path` rather than
#: re-deriving three home directories, so an env override (`CLAUDE_CONFIG_DIR`,
#: `CODEX_HOME`, `PI_CODING_AGENT_DIR`) is honoured here exactly as the harness
#: honours it.
LEGACY_SOURCES = ("claude_code", "codex", "pi")


def paths(*, origin: str = "", identity: str = "") -> Paths:
    """Where the three files live for THIS backend and THIS credential.

    ONE DOCUMENT PER MACHINE, and THERE IS NO HARNESS ARGUMENT. There was one
    -- the document sat beside each harness's instruction file while the base
    copy was keyed on the credential alone, so one base served three documents:
    each harness read the others' copy as unsynced work and pushed a whole
    document over it at every session start. Nothing converged them, because
    after a push `local_version == remote_version`, so `pull` returned without
    writing, and a dirty document is never overwritten. The server history
    flipped between two byte-identical bodies for a day (2026-09-07,
    v765-v770). Callers that need to know WHICH INSTRUCTION FILE a harness
    reads ask `agent_rules.memory_path(source)`; that is a different question
    and it keeps its own answer.

    The STATE directory under it is keyed by a hash of origin and identity, and
    that is not bookkeeping. `version` is a plain integer scoped to one document
    on one backend: a laptop that talks to production and to a local backend has
    two documents both sitting at version 12, and a base copy shared between them
    would hand one tenant's text to the other as a merge base. The key makes that
    impossible rather than unlikely.

    IDENTITY IS THE CREDENTIAL, hashed, never stored. A token names its tenant
    at the row level, so hashing it scopes the state per tenant without a network
    call to ask who we are -- and a session start cannot afford that call. It is
    also strictly narrower than a customer id: two credentials on one tenant get
    their own base copies, which is correct, because a base copy is a claim about
    what THIS client last saw.

    The DOCUMENT is deliberately outside that per-credential directory, because
    it is the editing surface named in a per-USER instruction file: one path the
    block can name whatever credential is active. The `.owner` stamp beside it
    records which credential's text is currently in it, and `park`/`adopt` keep
    the other credential's work rather than overwriting it.
    """
    root = state_dir() / "team-note"
    key = hashlib.sha256(f"{origin}|{identity}".encode()).hexdigest()[:16]
    document = root / DOCUMENT_NAME
    return Paths(
        document=document,
        base=root / key / "base.md",
        meta=root / key / "meta.json",
        # THE LOCK NAMES WHAT IT PROTECTS, and what it protects is the DOCUMENT
        # -- one file per machine. Keyed per credential (as the base copy
        # correctly is), two credentials' sessions would take two different
        # locks and write the same file: one could park and replace the
        # document in the window between another's read and its write, so a
        # merge computed from tenant A's text would land under tenant B's
        # stamp and go up to B's server on the next push. `instruction_lock_path`
        # already states this rule for CLAUDE.md; the document earns it too.
        lock=root / "document.lock",
        owner=key,
        stamp=document.with_name(document.name + ".owner"),
    )


def paths_for(settings) -> Paths:
    """`paths` from a resolved Settings -- the form every caller actually has."""
    return paths(
        origin=getattr(settings, "base_url", "") or "",
        identity=getattr(settings, "token", None) or "",
    )


def owner_key(*, origin: str = "", identity: str = "") -> str:
    """The state key for a backend+credential pair. Never stores the credential."""
    return hashlib.sha256(f"{origin}|{identity}".encode()).hexdigest()[:16]


def park(path: Path, *, kind: str = "unsynced") -> Path | None:
    """Move `path` aside, with its `.owner` stamp, and return where it went.

    THE ANCESTOR TRAVELS WITH IT, and it is the ancestor belonging to WHOEVER
    WROTE THE TEXT -- read from the `.owner` stamp, not from the caller. The
    common case is one credential parking ANOTHER's document, where the
    caller's own base copy is the wrong answer and a confidently wrong one.
    Without the right ancestor a later `adopt` merges against whatever base the
    machine holds by then, and every paragraph that landed while the work sat
    parked reads as a deletion by the person resuming.

    THE RENAME IS THE COMPARE-AND-SWAP. Every caller here is deciding about a
    file an agent may still be editing -- it was told this path by an
    instruction block that is only refreshed on the next sync. Read-then-delete
    and read-then-overwrite both have a window in which a sentence typed between
    the two calls is lost. `os.replace` closes it: whatever is written to the
    old path afterwards is a fresh file, which the NEXT reconcile parks in turn.

    Never clobbers an earlier parked copy (the suffix carries a counter), and
    returns None when the file is already gone -- two harness sessions starting
    together race here, and losing that race means someone else parked it.
    """
    if kind not in PARKED_KINDS:
        raise ValueError(f"unknown parked kind {kind!r}")
    # A DUPLICATE IS NOT WORTH KEEPING, and keeping it is unbounded. Two
    # credentials alternating on one machine park each other on every sync;
    # without this the directory grows by a full copy of the note per turn and
    # `probe doctor` lists them all forever. Identical bytes are already parked,
    # so this one is removed rather than added -- the only case where deleting
    # is not a loss.
    try:
        body = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        body = None
    if body is not None:
        for existing in sorted(path.parent.glob(f"{path.name}.{kind}-*")):
            if existing.name.endswith(PARKED_SIDECARS):
                continue
            try:
                if existing.read_text(encoding="utf-8") == body:
                    path.unlink()
                    return existing
            except (OSError, UnicodeDecodeError):
                continue
    stamp_path = path.with_name(path.name + ".owner")
    try:
        owner = stamp_path.read_text(encoding="utf-8").strip() or None
    except (OSError, UnicodeDecodeError):
        owner = None
    when = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for attempt in range(100):
        suffix = f".{kind}-{when}" + (f"-{attempt}" if attempt else "")
        target = path.with_name(path.name + suffix)
        # RESERVE THE NAME ATOMICALLY. `exists()` then `replace()` is
        # check-then-act: two sessions parking in the same second both see the
        # name free, and the second `replace` silently destroys the first
        # session's parked text -- the one thing parking exists to prevent.
        # `link` fails with EEXIST instead, which is the reservation.
        try:
            os.link(path, target)
        except FileExistsError:
            continue
        except FileNotFoundError:
            return None
        except OSError:
            # No hard links here (some filesystems). Fall back to the old
            # sequence: still correct alone, only racy against a twin.
            try:
                os.replace(path, target)
            except OSError:
                return None
            else:
                _copy_ancestor(owner, target)
                _move_stamp(stamp_path, target)
                return target
        try:
            path.unlink()
        except OSError:
            # The link landed, so the TEXT is safe under the parked name. A
            # source that could not be removed is parked again next sweep and
            # deduped there.
            pass
        _copy_ancestor(owner, target)
        _move_stamp(stamp_path, target)
        return target
    return None


def _copy_ancestor(owner: str | None, target: Path) -> None:
    """Keep the ancestor -- and the version it is -- beside the parked text.

    `owner` is the state key from the copy's own stamp, so the ancestor comes
    from ITS credential's directory rather than from whoever happens to be
    parking it. Best-effort: without these `adopt` refuses and the copy is
    folded in by hand, which is the safe direction.
    """
    if not owner:
        return
    root = state_dir() / "team-note" / owner
    for source, suffix in ((root / "base.md", ".base"), (root / "meta.json", ".meta")):
        try:
            write_text_atomic(
                target.with_name(target.name + suffix),
                source.read_text(encoding="utf-8"),
                mode=0o600,
            )
        except (OSError, UnicodeDecodeError):
            continue


def _move_stamp(stamp_path: Path, target: Path) -> None:
    """Provenance follows the text. Best-effort: the parked TEXT is the thing
    that must not be lost, and a copy with no stamp is reported as
    unknown-owner, which is already the conservative branch."""
    try:
        os.replace(stamp_path, target.with_name(target.name + ".owner"))
    except (FileNotFoundError, OSError):
        pass


def parked_kind(path: Path) -> str | None:
    """`"unsynced"`, `"legacy"`, or None when the name is not a parked copy."""
    for kind in PARKED_KINDS:
        if path.name.startswith(f"{DOCUMENT_NAME}.{kind}-"):
            return kind
    return None


def parked_copies(where: Paths) -> list[tuple[Path, str | None, str]]:
    """Every parked copy on this machine: path, whose it is, and which KIND.

    The kind decides what may happen to it -- `adopt` takes back only our own
    `unsynced` work, never a `legacy` per-harness copy whose merge base nobody
    knows. See `PARKED_KINDS`.

    Stateless on purpose: the notice exists exactly as long as the files do, so
    folding one in or deleting it silences the notice with no bookkeeping. A
    status file recording what was parked goes stale the moment a person acts on
    it by hand, which is the common case.
    """
    roots = {where.document.parent}
    from probe.cli import agent_rules

    for source in LEGACY_SOURCES:
        try:
            roots.add(agent_rules.memory_path(source).parent)
        except Exception:  # noqa: BLE001 - an unresolvable harness root is not a failure here
            continue
    found: list[tuple[Path, str | None, str]] = []
    for root in sorted(roots):
        try:
            entries = sorted(root.glob(PARKED_GLOB))
        except OSError:
            continue
        for entry in entries:
            # A parked copy travels with sidecars -- its owner stamp, the base
            # it derives from, and that base's version. They share the prefix
            # and are not themselves copies.
            if entry.name.endswith(PARKED_SIDECARS):
                continue
            kind = parked_kind(entry)
            if kind is None:
                continue
            try:
                owner = entry.with_name(entry.name + ".owner").read_text(encoding="utf-8").strip()
            except (OSError, UnicodeDecodeError):
                owner = None
            found.append((entry, owner, kind))
    return found


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


def adopt(where: Paths) -> Path | None:
    """Put our own parked copy back, if the document is not holding work.

    THE RESUME HALF OF `park`. A researcher switches credential, the note is
    parked under their old one, and later they switch back: their unsent edits
    should return to the editing surface rather than sit in a suffixed file
    forever. Only OUR parked copies are eligible (the stamp says so), and only
    when the current document is not itself carrying unsynced work -- adopting
    over that would trade one loss for another.

    The adopted document is dirty by construction, so the reconcile that follows
    merges the head into it and pushes the result: the upload resumes exactly
    where the credential switch interrupted it.
    """
    # OUR OWN `unsynced` WORK ONLY. A `legacy` copy carries our stamp too -- the
    # old CLI wrote it -- and adopting one would hand a document with an unknown
    # merge base to the next push, where its missing sections read as deletions.
    mine = [p for p, owner, kind in parked_copies(where) if owner == where.owner and kind == "unsynced"]
    if not mine:
        return None
    try:
        with file_lock(where.lock):
            document = _read(where.document)
            base = _read(where.base)
            ours = _stamp_matches(where, _read(where.stamp))
            if document is not None and document != base and ours:
                # Our own unsent work is sitting here. Adopting over it would
                # trade one loss for another.
                return None
            if document is not None and not ours:
                # Another credential's document. Park it (it is their unsent
                # work) and take our path back -- otherwise two credentials
                # alternating never adopt at all, and every session parks one
                # more copy.
                park(where.document, kind="unsynced")
            newest = max(mine, key=lambda p: (p.name, p.stat().st_mtime))
            body = _read(newest)
            if body is None:
                return None
            # THE ANCESTOR COMES BACK TOO. Restoring the text against whatever
            # base the machine holds NOW is how a resume deletes a teammate:
            # every paragraph that landed while this work sat parked is absent
            # from it, so the merge reads them as our deletions. The base parked
            # beside it is what the text was actually edited from; restoring
            # both makes the next pull an ordinary three-way merge. A parked
            # copy with no ancestor beside it (an older CLI parked it) is left
            # where it is -- reported, folded in by hand.
            parked_base = newest.with_name(newest.name + ".base")
            ancestor = _read(parked_base)
            if ancestor is None:
                return None
            where.document.parent.mkdir(parents=True, exist_ok=True)
            write_text_atomic(where.document, body, mode=0o600)
            write_text_atomic(where.stamp, where.owner, mode=0o600)
            write_text_atomic(where.base, ancestor, mode=0o600)
            # The version that ancestor IS. Its own file travelled with it when
            # there was one; otherwise the next push sends against version 0,
            # which the server merges rather than applies straight.
            meta = _read_meta(newest.with_name(newest.name + ".meta"))
            write_text_atomic(
                where.meta,
                json.dumps(
                    {"version": int(meta.get("version", 0)), "owner": where.owner}, indent=2
                ),
                mode=0o600,
            )
            for path in (
                newest,
                newest.with_name(newest.name + ".owner"),
                parked_base,
                newest.with_name(newest.name + ".meta"),
            ):
                try:
                    path.unlink()
                except OSError:
                    pass
            return newest
    except (Unreadable, OSError):
        return None


def migrate_legacy_documents(where: Paths) -> list[Path]:
    """Park any per-harness document left over from the old layout.

    ONE-TIME, PER MACHINE, and cheap enough to run every reconcile: three
    `stat`s against paths this process already knows. It cannot be a one-shot
    marker, because a session that started BEFORE the upgrade is still holding
    an instruction block naming the old path, and whatever it writes there has
    to be caught the next time round.

    PARK FIRST, COMPARE SECOND. Reading a legacy file, finding it identical to
    the base and then deleting it has a window: an agent writing between the
    two calls loses that sentence. The rename closes the window, and comparing
    the PARKED copy is exactly as good an answer to "is there anything here the
    server does not already have".
    """
    from probe.cli import agent_rules

    base = None
    try:
        with file_lock(where.lock):
            base = _read(where.base)
    except Unreadable:
        base = None

    kept: list[Path] = []
    for source in LEGACY_SOURCES:
        try:
            legacy = agent_rules.memory_path(source).parent / DOCUMENT_NAME
        except Exception:  # noqa: BLE001 - an unresolvable harness root has no legacy file
            continue
        if legacy == where.document or not legacy.exists():
            continue
        parked = park(legacy, kind="legacy")
        if parked is None:
            continue
        try:
            stat_before = parked.stat()
            body = parked.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            # Unreadable is an UNKNOWN, not an absence: keep it parked.
            kept.append(parked)
            continue
        if base is not None and body == base:
            # THE SERVER ALREADY HAS EVERY BYTE OF IT, so removing it is not a
            # loss -- with one window: a writer holding the old descriptor can
            # append to this same inode after the read. Re-stat and only remove
            # when nothing has touched it since, which turns "possible" into
            # "possible and the size and mtime both stayed put".
            try:
                after = parked.stat()
                unchanged = (after.st_size, after.st_mtime_ns) == (stat_before.st_size, stat_before.st_mtime_ns)
            except OSError:
                unchanged = False
            if unchanged:
                for path in (parked, *(parked.with_name(parked.name + s) for s in PARKED_SIDECARS)):
                    try:
                        path.unlink()
                    except OSError:
                        pass
                continue
            kept.append(parked)
            continue
        kept.append(parked)
    return kept


def reconcile(client, where: Paths) -> tuple[Report, str]:
    """One sync: adopt, migrate, MERGE the head in, then push what came out.

    THE ORDER, and why it is no longer push-then-pull. Pulling first used to
    overwrite a dead session's unsent edit, so the push had to run first. A pull
    that MERGES cannot overwrite anything, and merging first is strictly better:
    the document the push sends already contains the server's head, so the
    common case is an "applied straight" write rather than a server-side merge
    whose result has to be reconciled back into the file.

        adopt   ── our own parked copy comes back when nothing is in its way
        migrate ── per-harness leftovers are parked, never sent
        pull    ── head merged into the file; conflicts land as markers
        push    ── the merged document goes up
    """
    adopted = adopt(where)
    parked = migrate_legacy_documents(where)
    report, text = pull(client, where)
    pushed = push(client, where)
    notes = [n for n in (report.detail, pushed.detail) if n]
    if adopted is not None:
        notes.append(f"resumed the copy parked at {adopted}")
    if parked:
        notes.append(
            f"{len(parked)} unsynced legacy copy(ies) parked: "
            + ", ".join(str(p) for p in parked)
        )
    return (
        Report(
            pushed=pushed.pushed,
            pulled=report.pulled,
            merged=pushed.merged,
            conflicted=report.conflicted or pushed.conflicted,
            version=max(report.version, pushed.version),
            detail="; ".join(notes),
        ),
        text,
    )


#: The budget one instruction file may occupy, applied to BOTH harnesses.
#:
#: Codex documents 32 KiB (`project_doc_max_bytes`) for its WHOLE instruction
#: chain -- the global AGENTS.md plus every repo's own file walking down -- and
#: it stops adding files once that fills, so an oversized note silently starves
#: a repository's own build and test rules. Claude Code publishes no equivalent
#: cap, but an unbounded note is the same harm paid in tokens instead of missing
#: context, and matching the numbers means the degrade path is exercised on both
#: harnesses rather than being untested code on one.
INSTRUCTION_FILE_MAX_BYTES = 32_768

#: Where a render failure waits to be reported. The render runs in the
#: background off a Stop/SessionEnd hook, which has no channel to the model at
#: the moment it runs -- so "fail loudly" means recording here and letting the
#: NEXT session start say it out loud. Without this the loud failure is silent
#: in practice, which is the bug this whole change exists to stop.
RENDER_FAILURE_FILE = "render-failures.json"

#: Both harnesses, always. One sync renders both, because each harness's local
#: copy otherwise only refreshes when THAT harness runs -- measured on a shared
#: box: the Claude copy 7 hours fresher than the Codex copy and five sections
#: ahead of it, with neither agent able to tell.
RENDER_SOURCES = ("claude_code", "codex")


@dataclass(frozen=True, slots=True)
class RenderReport:
    """What one render pass did, per harness."""

    written: tuple[str, ...] = ()
    unchanged: tuple[str, ...] = ()
    pointer_only: tuple[str, ...] = ()
    failures: tuple[str, ...] = ()
    #: Harnesses whose RESEARCH-TRACKING block was older than this CLI and got
    #: rewritten on the way past. Separate from `written`, which is the team
    #: note: the two blocks share a file and a lock but not a lifecycle, and an
    #: operator asking "did the new guidance land?" is asking about this one.
    rules_refreshed: tuple[str, ...] = ()
    #: Harnesses whose file carries no pointer block (the agent-rules opt-out),
    #: so the note was not rendered there; `removed` also took an old note out.
    opted_out: tuple[str, ...] = ()
    removed: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.failures


def instruction_lock_path(instruction: Path) -> Path:
    """A lock keyed on the FILE being written, not on the credential.

    `Paths.lock` is keyed on origin+identity because the base copy and version
    are per-credential -- correct for the sync, wrong for this. The instruction
    file is user-global: `~/.claude/CLAUDE.md` is the same path whatever
    credential is resolved, so two contexts on one machine take two DIFFERENT
    locks and write the SAME file. The lock has to name what it protects.
    """
    digest = hashlib.sha256(str(instruction.resolve()).encode("utf-8")).hexdigest()[:16]
    return state_dir() / "team-note" / "locks" / f"{digest}.lock"


#: Where the last render's size health waits for the session-start audit
#: trigger. The pointer-vs-full decision is made HERE, against the real
#: instruction budget — a hook cannot know that constant without growing a
#: drifting mirror of it, so the render writes what it measured and the hook
#: only reads. Advisory: a missing or stale file just means the size half of
#: the trigger stays quiet.
HEALTH_FILE = "health.json"


def note_health_path() -> Path:
    return state_dir() / "team-note" / HEALTH_FILE


#: The audit stamp, in the ONE shape the skill documents and the trigger hook
#: parses. Three surfaces carry this literal and
#: `tests/test_notes_audit_trigger.py` pins them together — reword one without
#: the others and the churn guard silently stops recognising an audit.
AUDIT_STAMP_RE = re.compile(r"<!--\s*audited\s+(\d{4}-\d{2}-\d{2})\s*-->", re.IGNORECASE)


def _audit_baseline(document: str, previous: dict[str, object] | None) -> dict[str, object]:
    """The post-audit fingerprint the trigger compares against.

    WHY THE STAMP GATES THE HASH. The question the churn guard answers is "has
    anyone written since the last AUDIT", and this runs at every render — so a
    hash refreshed on every render would answer "since the last render" instead,
    which is nearly always "no" and would suppress tightening forever. The hash
    therefore moves only when the STAMP moves: a new stamp means an audit just
    finished, so the document as it stands now IS that audit's result. Every
    later render leaves it alone, and an append between audits shows up as a
    mismatch, which is exactly the signal.

    THE FIRST SIGHTING RECORDS NO HASH, and that is the whole safety of this.
    On the first render after this ships every machine has no `audit` key, and
    hashing the document THEN would file weeks of un-audited appends under the
    old stamp as "what the last audit produced" -- so the very next audit would
    be told to skip its tightening. A hash is only ever written when a stamp
    CHANGE is observed, because that is the only evidence available here that an
    audit actually ran.

    A note with no stamp records none: there is no audit to be unchanged since.

    HASHED OVER THE STRIPPED DOCUMENT, matching `render_blocks`, which strips
    before it renders. The hook must strip too or the two hash different bytes
    and the guard never fires -- and it would never fire LOUDLY, it would just
    silently tighten every cycle forever.
    """
    match = AUDIT_STAMP_RE.search(document)
    if match is None:
        return {}
    stamp = match.group(1)
    if not previous or not previous.get("stamp"):
        return {"stamp": stamp}
    if previous.get("stamp") == stamp:
        return dict(previous)
    digest = hashlib.sha256(document.strip().encode("utf-8")).hexdigest()
    return {"stamp": stamp, "content_sha256": digest}


#: The deletion kill switch, read here rather than in a hook: this module already
#: owns the stamp, the health file and the budget, so the knob lives beside the
#: numbers it acts on instead of in a second process that has to mirror it.
#:
#: DAYS-SHAPED BUT READ AS A SWITCH: anything above zero means the auditor may
#: delete. It is NOT the cadence -- that is `AUDIT_INTERVAL_DAYS` below, and the
#: two sevens beside each other mean different things.
AUDIT_HORIZON_DAYS = 7

#: Fires the size half when the LAST render measured the block at or above this
#: fraction of the room its instruction file had.
AUDIT_SIZE_PCT = 0.8

#: Fires the TRUTH half when nobody has audited the note in this many days,
#: whatever its size. 0 disables the calendar.
#:
#: A calendar is still the wrong shape for TIGHTENING and is not used for it: a
#: date says nothing about whether a document is too long, and compacting a note
#: nobody is struggling to read spends a background agent for nothing. What it
#: buys is the half the on-read prong was never closing -- "has anyone checked
#: this is still TRUE?" -- because a reader only corrects a claim they happen to
#: hold the evidence against, and the quiet claims are the ones nobody tests.
AUDIT_INTERVAL_DAYS = 7

#: What Claude Code reports when a person is at the keyboard. Everything else it
#: reports -- `sdk-cli` for `claude -p`, the language SDKs, `mcp` -- is a program
#: driving the session.
INTERACTIVE_ENTRYPOINTS = frozenset(
    {"cli", "vscode", "vscode-insiders", "cursor", "windsurf"}
)


def session_is_automated(env: "dict | None" = None) -> bool:
    """Is this session being driven by a program rather than a person?

    A DENY-LIST, deliberately. The hook that asks this only fires when a prompt
    is submitted, so presence is already most of the way proven; this filters the
    two known automated submitters and lets an unrecognised harness through. An
    allow-list would silently disable the audit on every harness we have not met
    yet, and silence is the failure mode nobody notices.

    Measured on this box: `codex exec` sets `CODEX_CI=1`, `claude -p` reports
    `CLAUDE_CODE_ENTRYPOINT=sdk-cli`, an interactive Claude Code session reports
    `cli`.
    """
    env = os.environ if env is None else env
    if str(env.get("CODEX_CI", "")).strip().lower() not in ("", "0", "false"):
        return True
    entrypoint = str(env.get("CLAUDE_CODE_ENTRYPOINT", "")).strip().lower()
    if entrypoint:
        return entrypoint not in INTERACTIVE_ENTRYPOINTS
    return False


def _audit_env(name: str, default: int, floor: int) -> int:
    raw = os.environ.get(name, "")
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value >= floor else default


def _stamp_age_days(document: str, today) -> "int | None":
    """Days since the audit stamp, or None when there is no usable stamp.

    None means "never audited" and is DUE: absent, malformed and future-dated
    stamps all land here, so a corrupted stamp buys an audit (which rewrites it)
    rather than suppressing audits until someone notices.
    """
    match = AUDIT_STAMP_RE.search(document)
    if match is None:
        return None
    try:
        stamped = _dt.date.fromisoformat(match.group(1))
    except ValueError:
        return None
    age = (today - stamped).days
    return age if age >= 0 else None


def _untouched_since_audit(document: str, baseline: "dict | None") -> bool:
    """Has NOBODY written since the audit that produced this text?

    Gates TIGHTENING only, never the truth pass: a document nobody has edited
    can still have gone stale, because the world moves underneath it. Any
    missing or unparseable half answers False -- the guard may only ever
    suppress work it is CERTAIN is redundant.
    """
    if not isinstance(baseline, dict):
        return False
    recorded, stamp = baseline.get("content_sha256"), baseline.get("stamp")
    if not isinstance(recorded, str) or not isinstance(stamp, str):
        return False
    match = AUDIT_STAMP_RE.search(document)
    if match is None or match.group(1) != stamp:
        return False
    return hashlib.sha256(document.strip().encode("utf-8")).hexdigest() == recorded


def audit_advisory(
    document: str, *, source: str, pct: "float | None", baseline: "dict | None", today=None
) -> str:
    """The line the block carries when the team note is due for its audit.

    THIS REPLACED A SESSIONSTART HOOK, and the move is the point. A hook was the
    only way a TIMER could reach the model, because the render runs detached
    with its output discarded -- but a timer on the context channel is the wrong
    shape: it spends the session's context to say something about a document
    that is already in that context. Written into the block instead, the
    reminder rides the note it is about, and the per-source loop gives each
    harness its own correct dispatch with no environment sniffing.

    The SIZE half reads the LAST render's measurement, not this one's: this
    string is about to change the length it would be measuring.
    """
    today = today or _dt.date.today()
    horizon = _audit_env("PROBE_NOTES_AUDIT_HORIZON_DAYS", AUDIT_HORIZON_DAYS, 0)
    age = _stamp_age_days(document, today)
    interval = _audit_env("PROBE_NOTES_AUDIT_INTERVAL_DAYS", AUDIT_INTERVAL_DAYS, 0)
    # TWO TRIGGERS, AND THE SENTENCE SAYS WHICH ONE. Size fires the TIGHTENING
    # half: the block is about to stop arriving at all, and only cutting bytes
    # fixes that. The interval fires the TRUTH half: a small note is otherwise
    # re-checked by nothing, because the on-read prong corrects only the claims
    # a reader happens to hold evidence against. They are not interchangeable --
    # tightening a note that is inside its budget is busywork, so the overdue
    # dispatch says not to. No SECTION NUMBERS in either sentence: the skills
    # renumber, and a stale pointer sends the auditor to the wrong rules.
    oversized = pct is not None and pct >= AUDIT_SIZE_PCT
    overdue = interval > 0 and (age is None or age >= interval)
    if not oversized and not overdue:
        return ""
    # A 24-hour floor: a note stamped TODAY is not asked again, however large.
    # It caps the rate at one audit per day rather than one per session.
    if age is not None and age < 1:
        return ""
    # An unchanged document cannot have GROWN since the last pass, so a second
    # tightening has nothing to find. It gates SIZE only: the world moves under
    # a document nobody has touched, which is the whole point of the interval.
    if oversized and not overdue and _untouched_since_audit(document, baseline):
        return ""
    dispatch = (
        "Run the `audit-team-note` skill (`notes-audit` on plugins before 0.90.0) YOURSELF now, before taking up the user's work "
        "-- this sandbox reaps detached processes, and it is one small file."
        if source == "codex"
        else "Run the `audit-team-note` skill (`notes-audit` on plugins before 0.90.0) in a BACKGROUND subagent and carry on with "
        "the user's work -- never inline."
    )
    removal = (
        "Delete what the evidence disproves."
        if horizon > 0
        else "Deletion is DISABLED: correct claims in place, delete nothing."
    )
    if oversized:
        headline = "This note has outgrown its budget"
        reasons = f"at {round(pct * 100)}% of its render budget"
        job = "Tighten what stays."
    else:
        headline = "This note is due its periodic re-check"
        reasons = "never audited" if age is None else f"{age} days since the last audit"
        job = (
            "Do NOT tighten it -- it is inside its budget, and this pass is about "
            "what is still TRUE."
        )
    return (
        f"> **{headline}** ({reasons}). "
        f"{dispatch} {removal} {job} "
        "If research tracking is off for this session, skip it."
    )


def advisory_for_source(source: str, *, settings, today=None) -> str:
    """The audit line for THIS machine's note, from local state only.

    NO NETWORK AND NO RENDER. The caller is a prompt-submit hook with a few
    seconds of budget, so this reads the document and the last render's
    measurements off disk and asks the same `audit_advisory` the render used to
    ask. Anything unreadable answers "" -- a missing health file means no
    measurement, which is not an audit trigger.
    """
    try:
        document = paths_for(settings).document.read_text(encoding="utf-8").strip()
    except OSError:
        return ""
    if not document:
        return ""
    try:
        health = json.loads(note_health_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        health = {}
    sources = health.get("sources") if isinstance(health, dict) else None
    entry = sources.get(source) if isinstance(sources, dict) else None
    pct = entry.get("pct") if isinstance(entry, dict) else None
    baseline = health.get("audit") if isinstance(health, dict) else None
    return audit_advisory(
        document,
        source=source,
        pct=pct if isinstance(pct, (int, float)) else None,
        baseline=baseline if isinstance(baseline, dict) else None,
        today=today,
    )


#: How long one session's dispatch holds this machine's audit. The advisory is
#: per SESSION and the stamp that silences it is written by the auditor, so every
#: session that submitted a prompt between the dispatch and that write was told
#: to spawn its own auditor: N sessions on one box, N subagents rewriting one
#: file. The lease closes that window. It only has to outlive "subagent starts,
#: stamps the note", which the skill does first; after that the stamp's same-day
#: floor keeps everyone quiet. Its expiry is the recovery path for a claim nobody
#: acted on (session closed, line ignored, subagent died): each such claim holds
#: the audit for this long, and the next prompt after it takes over.
AUDIT_LEASE_SECONDS = 2 * 60 * 60

#: The session the prompt hook is asking for. Set by `note_audit.py` in the
#: environment rather than as a flag, so a new hook calling an older CLI is not
#: refused an option it has never heard of.
AUDIT_SESSION_ENV = "PROBE_NOTE_AUDIT_SESSION"


def audit_lease_path() -> Path:
    return state_dir() / "team-note" / "audit-lease.json"


#: A real lease is under 100 bytes. Anything longer is corrupt, and reading it
#: whole could hand the JSON decoder a nesting deep enough to raise
#: RecursionError on every prompt -- a lease no expiry ever clears.
_LEASE_MAX_BYTES = 4096


def _read_lease(lease: Path) -> dict:
    """The lease as a dict, or {} for anything that is not a small JSON object.

    Not a regular file (a FIFO would block every prompt's hook until its
    timeout), too long, or undecodable: all corrupt, all free.
    """
    try:
        if not lease.is_file():
            return {}
        with lease.open("rb") as handle:
            raw = handle.read(_LEASE_MAX_BYTES + 1)
        if len(raw) > _LEASE_MAX_BYTES:
            return {}
        held = json.loads(raw)
    except (OSError, ValueError, RecursionError):
        return {}
    return held if isinstance(held, dict) else {}


def _lease_time(raw: object) -> "float | None":
    """A lease's `claimed_at` as a finite number, or None. A 400-digit integer
    overflows the float arithmetic below and NaN compares false both ways;
    either would otherwise pin the lease or crash the hook's CLI call."""
    if isinstance(raw, bool):
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError, OverflowError):
        return None
    return value if math.isfinite(value) else None


def claim_audit_dispatch(*, holder: "str | None" = None, now: "float | None" = None) -> bool:
    """Take this machine's audit, or learn another session already has it.

    Under a lock: two sessions whose prompts land together both read "free" and
    both claim otherwise.

    THE HOLDER MAY ASK AGAIN. The lease is written before the line reaches the
    model, so a hook killed by its timeout, or output the harness dropped, would
    otherwise leave the claiming session as silent as everyone else for the
    whole lease. Its hook did not mark it as told, so it asks on its next prompt
    and gets the line back -- and the lease RENEWS, because that telling is the
    one its auditor starts from; a re-telling a second before expiry must not
    let another session dispatch a second later. A claim with no holder (an
    older hook, a person at a terminal) cannot be re-asked; it just expires.

    A lease timestamped up to one lease-length AHEAD still counts: on one
    machine that is a clock stepped backwards, and reading it as free let a
    second session dispatch. Further ahead than that, or unreadable, it is
    corrupt and free. A lease that cannot be recorded answers True -- a
    duplicate audit costs tokens, a silenced one lets the note rot unnoticed.
    """
    now = time.time() if now is None else now
    lease = audit_lease_path()
    try:
        with file_lock(lease.parent / "locks" / "audit-lease.lock"):
            held = _read_lease(lease)
            claimed_at = _lease_time(held.get("claimed_at"))
            live = claimed_at is not None and abs(now - claimed_at) < AUDIT_LEASE_SECONDS
            if live and not (holder and held.get("holder") == holder):
                return False
            # NO FSYNC. The rename alone keeps readers off a torn file, a lease
            # lost to a crash only costs a duplicate audit, and every fsync here
            # is spent holding a lock the other sessions' prompts are queued on.
            write_text_atomic(
                lease, json.dumps({"claimed_at": now, "holder": holder}) + "\n", sync=SYNC_NONE
            )
    except OSError:
        return True
    return True


def _record_health(entries: dict[str, dict[str, object]], document: str = "") -> None:
    """Persist what the render measured, for the audit trigger to read."""
    if not entries:
        return
    path = note_health_path()
    try:
        previous = json.loads(path.read_text(encoding="utf-8")).get("audit")
    except (OSError, ValueError, AttributeError):
        previous = None
    payload: dict[str, object] = {"sources": entries}
    baseline = _audit_baseline(document, previous if isinstance(previous, dict) else None)
    if baseline:
        payload["audit"] = baseline
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomic(path, json.dumps(payload, indent=2) + "\n")
    except OSError:
        # Health is advisory; failing to record it must not fail the render.
        pass


def render_failure_path() -> Path:
    return state_dir() / "team-note" / RENDER_FAILURE_FILE


def _record_failures(failures: list[str]) -> None:
    """Persist (or clear) what the next session should say out loud."""
    path = render_failure_path()
    try:
        if not failures:
            path.unlink(missing_ok=True)
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomic(path, json.dumps({"failures": failures}, indent=2) + "\n")
    except OSError:
        # Recording the failure must never itself become one.
        pass


def pending_render_failures() -> list[str]:
    """What the last render could not do, for the next session to report."""
    try:
        payload = json.loads(render_failure_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    # A status file that is valid JSON but not an object (a bare list, a string)
    # made `.get` raise AttributeError, which is not a ValueError and so escaped
    # the guard above -- turning "cannot read my own status file" into a crash
    # in the one path whose whole job is to fail open.
    if not isinstance(payload, dict):
        return []
    found = payload.get("failures")
    return [str(item) for item in found] if isinstance(found, list) else []


def _utf8_len(value: str) -> int:
    """BYTES, not code points. `project_doc_max_bytes` is a byte budget and this
    file is full of em-dashes and middots, so measuring `len(str)` under-counts
    every non-ASCII character by one to three bytes -- silently, and in the
    direction that overruns the cap."""
    return len(value.encode("utf-8"))


def _fits(existing: str, block: str, span: tuple[int, int] | None) -> bool:
    """Would `block` fit the budget once it replaces whatever is there now?"""
    replaced = _utf8_len(existing[span[0] : span[1]]) if span else 0
    without = _utf8_len(existing) - replaced
    return without + _utf8_len(block) <= INSTRUCTION_FILE_MAX_BYTES


def render_blocks(text: str, *, settings, sources: tuple[str, ...] = RENDER_SOURCES) -> RenderReport:
    """Render the note into every harness's instruction file.

    THE LOCK IS NOT HELD ACROSS THE NETWORK -- the caller has already fetched;
    this function only reads, renders and writes files. `Paths.lock` is keyed on
    origin and credential rather than on harness, so one acquisition genuinely
    covers both files and a half-rendered pair cannot exist.

    Three outcomes per harness, in order: the block already says exactly this
    (skip, no write, no lock contention beyond the read); the full note fits
    (write it); it does not (write a POINTER instead, never a truncated note --
    partial content under a header that calls itself a copy of the team note
    reads as complete, and the reader has no way to tell). If even the pointer
    does not fit, refuse and record it: the file is too full for us, and saying
    so is more use than silently making a repository's own rules disappear.

    A damaged block is left ALONE, never repaired. Auto-repair of a file humans
    also edit destroys edits it did not understand.
    """
    from probe.cli import agent_rules

    body = text.strip()
    conflict = agent_rules.note_body_conflict(body)
    if conflict:
        # UNRENDERABLE, not fixable: _find_block counts marker occurrences, so a
        # marker inside the body makes the file unparseable wherever we put it.
        # Refuse for every harness and say why, rather than rewriting the team's
        # own prose without being asked.
        failures = [f"{source}: {conflict}" for source in sources]
        _record_failures(failures)
        return RenderReport(failures=tuple(failures))

    # The FILE keeps its verbatim bytes — edits round-trip against the file, so
    # it must never be normalized. The BLOCK renders the COLLAPSED form: a
    # struck claim stops costing every session's context the moment it is
    # struck, instead of only when someone physically deletes it. Idempotent,
    # and byte-identical to the note when no marker exists.
    display = superseded.collapse(body)

    # NO PRIOR MEASUREMENT IS READ HERE ANY MORE. This render used to load the
    # last one to derive the audit advisory it embedded; the advisory left the
    # block (see below), and `_record_health` reads the file itself for the
    # churn baseline it carries forward. The reason the audit trigger still
    # wants the PREVIOUS render's numbers is unchanged -- a measurement of the
    # block this render is composing cannot describe it -- but that read now
    # happens in `advisory_for_source`, on the hook's side.

    written: list[str] = []
    unchanged: list[str] = []
    pointer_only: list[str] = []
    failures: list[str] = []
    rules_refreshed: list[str] = []
    opted_out: list[str] = []
    removed: list[str] = []
    health: dict[str, dict[str, object]] = {}

    for source in sources:
        try:
            where = paths_for(settings)
            instruction = agent_rules.memory_path(source)
            document = str(where.document)
        except Exception as exc:  # noqa: BLE001 - a path we cannot resolve is a failure to report
            failures.append(f"{source}: cannot resolve paths ({exc})")
            continue

        # THE BLOCK CARRIES NO ADVISORY. It used to: the audit line was written
        # in here so the reminder rode the note it was about. But this file is
        # read by every session of this harness -- `claude -p`, `codex exec`, a
        # cron job, a subagent -- and none of those can be asked to spend a
        # background agent on a cleanup, or be trusted to still exist when one
        # finishes. Presence is knowable only where a prompt is submitted, so
        # the line moved to the UserPromptSubmit hook, which asks
        # `probe notes audit-advisory` for exactly this text.
        #
        # `render_note_block` keeps its `advisory` parameter: the pointer form
        # and the hash still have to handle one, and the hook's text is composed
        # from the same function this render used to call.
        full = agent_rules.render_note_block(display, document=document)
        # The POINTER still stamps the source body's hash. Stamping an empty
        # body made `note_block_is_current` -- which hashes the real body --
        # never match, so every sync re-rendered on exactly the machines that
        # are over budget, which is now the common case.
        pointer = agent_rules.render_note_block(
            display, document=document, pointer_only=True
        )

        try:
            with file_lock(instruction_lock_path(instruction)):
                # THE POINTER BLOCK RIDES THIS SYNC, and that is the only thing
                # that keeps it current. It is written once by the wizard and
                # was refreshed only by `probe rules refresh` run BY HAND, so a
                # POINTER_VERSION bump reached nobody: shipping a new CLI left
                # every machine on whatever block its wizard run installed.
                # Observed cost: guidance added in one release was still absent
                # from live sessions days later, and agents did the thing it
                # existed to prevent. This sync already runs on every Stop,
                # already resolves every configured harness, and already holds
                # this file's lock -- so the refresh costs one version read.
                #
                # BEFORE the note render, deliberately: the note is the part
                # that gets degraded or skipped when the file is over budget,
                # and the standing instructions must not be held hostage to a
                # long note.
                # Its OWN handler: a damaged pointer block must not be reported
                # as a damaged team-note block, and must not stop the note from
                # rendering. The two blocks have different markers, so one being
                # unreadable says nothing about the other.
                rules_state = agent_rules.POINTER_CURRENT
                try:
                    rules_state = agent_rules.refresh_pointer(instruction)
                    if rules_state == agent_rules.POINTER_REFRESHED:
                        rules_refreshed.append(source)
                except agent_rules.DamagedBlock as exc:
                    failures.append(
                        f"{source}: {instruction.name} has a damaged research-tracking block "
                        f"({exc}); left untouched"
                    )

                # NO POINTER, NO NOTE. An absent pointer block is the opt-out
                # (`--no-agent-rules`, or Settings unticked), and the note is a
                # managed block in the same global file: rendering it anyway put
                # Probe's text in the CLAUDE.md of a customer who had declined
                # it (2026-10-02), and in an AGENTS.md for a Codex that machine
                # never had. A note left from before the opt-out goes too. A
                # DAMAGED pointer is still someone's opt-in, so it renders.
                if rules_state == agent_rules.POINTER_ABSENT:
                    if agent_rules.remove(instruction, spec=agent_rules.NOTE_BLOCK):
                        removed.append(source)
                    else:
                        opted_out.append(source)
                    continue

                existing = ""
                if instruction.exists():
                    existing = instruction.read_text(encoding="utf-8")
                span = agent_rules._find_block(existing, agent_rules.NOTE_BLOCK)

                # Measured against the room this file actually has, which is
                # the number the pointer decision below is made from.
                replaced = _utf8_len(existing[span[0] : span[1]]) if span else 0
                available = INSTRUCTION_FILE_MAX_BYTES - (_utf8_len(existing) - replaced)
                health[source] = {
                    "block_bytes": _utf8_len(full),
                    "available_bytes": available,
                    "pct": round(_utf8_len(full) / available, 4) if available > 0 else 999.0,
                }

                if _fits(existing, full, span):
                    block, degraded = full, False
                elif _fits(existing, pointer, span):
                    block, degraded = pointer, True
                else:
                    health[source]["degraded"] = True
                    failures.append(
                        f"{source}: {instruction.name} is too full for the team-note block "
                        f"({len(existing)}B of {INSTRUCTION_FILE_MAX_BYTES}B); compact it and the "
                        f"note will render on the next sync"
                    )
                    continue
                health[source]["degraded"] = degraded

                # ASKED AFTER THE FORM IS CHOSEN, and inside the lock. Before
                # the form was known the check could not tell a current pointer
                # from a stale one; outside the lock it was a time-of-check race
                # against another process replacing the block.
                if agent_rules.note_block_is_current(
                    instruction, display, document, pointer_only=degraded
                ):
                    unchanged.append(source)
                    continue

                agent_rules.install(instruction, spec=agent_rules.NOTE_BLOCK, block=block)
        except agent_rules.DamagedBlock as exc:
            failures.append(f"{source}: {instruction.name} has a damaged team-note block ({exc}); left untouched")
            continue
        except (OSError, UnicodeDecodeError) as exc:
            # UnicodeDecodeError is a ValueError, NOT an OSError -- the same trap
            # `apply_agent_rules` already documents. One latin-1 byte in a
            # researcher's own CLAUDE.md would otherwise escape this handler,
            # skip the failure record, and leave the other harness unrendered.
            failures.append(f"{source}: cannot write {instruction} ({exc})")
            continue

        (pointer_only if degraded else written).append(source)

    _record_failures(failures)
    _record_health(health, body)
    return RenderReport(
        written=tuple(written),
        unchanged=tuple(unchanged),
        pointer_only=tuple(pointer_only),
        failures=tuple(failures),
        rules_refreshed=tuple(rules_refreshed),
        opted_out=tuple(opted_out),
        removed=tuple(removed),
    )
