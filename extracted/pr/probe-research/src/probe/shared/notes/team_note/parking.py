"""parked copies: move text aside with its owner stamp, list them, put our own back, park per-harness documents from the old layout."""

from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from probe.foundation.durable.durable import file_lock, write_text_atomic
from probe.shared.updates.version_policy import state_dir
from probe.shared.notes.sync import (  # noqa: F401 - re-exported for this module's callers
    Paths,
    Unreadable,
    read_meta as _read_meta,
    read_text as _read,
    stamp_matches as _stamp_matches)
from probe.shared.notes.team_note.team_note import DOCUMENT_NAME

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
    from probe.cli.wizard.apply import agent_rules

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
    from probe.cli.wizard.apply import agent_rules

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
