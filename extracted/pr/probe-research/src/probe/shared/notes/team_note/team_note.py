"""The team note as a local file: one document per machine, synced like git. What changed and why: DESIGN.md."""

from __future__ import annotations

import hashlib
from probe.sdk.merge3 import merge3
from probe.shared.updates.version_policy import state_dir
from probe.shared.notes.sync import (  # noqa: F401 - re-exported for this module's callers
    Paths,
    Report,
    merge_into_file as _merge_into_file_core)


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
from probe.shared.notes.team_note.parking import adopt, migrate_legacy_documents  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.notes.team_note.push_pull import pull, push  # noqa: E402 -- pieces need each other; the front door loads this one first
