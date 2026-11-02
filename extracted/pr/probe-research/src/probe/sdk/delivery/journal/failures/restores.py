"""Restores: ONE-TIME recovery of the writes set aside behind one revoked key (Bucket, 2026-10-22/23).
Delete once they are verified on prod; the bounds and the reasons are below."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from typing import Any, TYPE_CHECKING

from probe._shared import oscompat
from probe.foundation.compat.compat import StrEnum
from probe.foundation.durable.durable import SYNC_FILE, file_lock, fsync_directory, now_iso, write_text_atomic

from .... import errors


if TYPE_CHECKING:
    from probe.sdk.delivery.journal.journal import Journal


# -- ONE-TIME RECOVERY: delete with its callers once verified on prod ---------------------
#
# A key a customer's training jobs held was revoked mid-run (2026-10-22 21:47Z, a re-sign-in
# on the same Mac). Their queued writes waited, then `probe outbox discard --held` set 12,357
# of them aside in the outbox root's `discarded/`, and nothing ever sends a set-aside write.
# A discard records no reason, so no rule can tell an accident from a deliberate drop on other
# machines: only this incident's writes are put back (plan restore-set-aside-writes, D1-D3).
# Callers to delete with this file: `outbox/rescuer.py` (`claim_restore`, `maybe_restore`,
# the steps in `rescue`), `service/server/outbox.py` (`_restore_outbox`),
# `cli/lifecycle/notices/outbox.py` (an outbox with no status), `was_restored` in
# `outbox/drain/adoption.py`, and this module's lines in `journal/__init__.py`.

#: The one credential (`context.principal.fingerprint`) whose set-aside writes are put back.
RESTORE_FINGERPRINT = "738f7f8ed3fe16d6"
#: The UTC days (`enqueued_at`) those writes were queued on.
RESTORE_DAYS = frozenset({"2026-10-22", "2026-10-23"})
#: Stamped on a write put back: it is never put back twice (D2), and it is proof its credential
#: could not send (`rescue_stranded`).
RESTORED_KEY = "restored_at"
#: Written in an outbox root after a pass that left none of its restored writes queued: no
#: rescuer starts for the restore after it (`outbox/rescuer.py`).
RESTORE_DONE = ".restore-done"
#: Files looked at per hold of the append lock: a writer's append waits for one batch at most.
_RESTORE_BATCH = 500


class KeptAside(StrEnum):
    """Why one of this incident's set-aside writes stays in ``discarded/`` (`outbox.restored`'s
    ``kept``)."""

    #: The server refused it for what it asked (a stale epoch, no such run...), not for its key.
    REFUSED = "refused"
    #: The login may never send it: an `/ingest` write, a DELETE, a scope refusal, a multipart upload.
    NOT_SENDABLE = "not_sendable"
    #: Put back once already (D2): set aside again since, or refused by the login check.
    RESTORED_BEFORE = "restored_before"
    #: An upload whose bytes are not in the root's ``blobs/`` (collected, or never staged: the
    #: file it names may have changed since).
    BYTES_GONE = "bytes_gone"
    #: One of this credential's writes was refused for scope: none may go out with the login
    #: (`adoption_account` keeps them all for one such refusal).
    SCOPE = "scope"


@dataclass
class RestoreCounts:
    """What a restore did, for `outbox.restored`: counts and enqueue days, never a key, body, name
    or path. ``deferred`` and ``refused`` are filled by the rescuer after the login check."""

    #: Writes put back into ``ops/`` this pass.
    writes: int = 0
    uploads: int = 0
    by_enqueue_day: dict = field(default_factory=dict)
    #: `KeptAside` -> this incident's writes left in ``discarded/``.
    kept: dict = field(default_factory=dict)
    #: Restored writes moved back aside: the login check refused their credential.
    refused: int = 0
    #: Why (`NotAdoptable`), or None.
    refused_reason: str | None = None
    #: Restored writes still queued after the pass (no login, offline, a live holder...).
    deferred: int = 0
    #: Writes that could not be read or moved this pass (a full disk, a permission): they stay
    #: aside and the restore is not done, so the next pass tries them again.
    unmoved: int = 0
    #: The servers the counted writes were pinned to: the event goes only where they were going.
    base_urls: set = field(default_factory=set)
    #: How many enqueue days the event carries (a class constant, not a field).
    reported_days = len(RESTORE_DAYS)

    @property
    def bytes_gone(self) -> int:
        return int(self.kept.get(KeptAside.BYTES_GONE, 0))

    @property
    def base_url(self) -> str | None:
        """The one server every counted write was pinned to, else None (nothing is reported)."""
        if len(self.base_urls) != 1:
            return None
        return next(iter(self.base_urls))

    def add(self, op: dict) -> None:
        self.writes += 1
        if op.get("kind") == "upload":
            self.uploads += 1
        day = op_day(op)
        if day:
            self.by_enqueue_day[day] = self.by_enqueue_day.get(day, 0) + 1
        self.base_urls.add(op_base_url(op))

    def keep(self, op: dict, why: KeptAside) -> None:
        self.kept[str(why)] = self.kept.get(str(why), 0) + 1
        self.base_urls.add(op_base_url(op))

    def merge(self, other: "RestoreCounts") -> None:
        self.writes += other.writes
        self.uploads += other.uploads
        for day, n in other.by_enqueue_day.items():
            self.by_enqueue_day[day] = self.by_enqueue_day.get(day, 0) + n
        for why, n in other.kept.items():
            self.kept[why] = self.kept.get(why, 0) + n
        self.refused += other.refused
        self.refused_reason = self.refused_reason or other.refused_reason
        self.deferred += other.deferred
        self.unmoved += other.unmoved
        self.base_urls |= other.base_urls


def was_restored(op: Any) -> bool:
    """Whether ``op`` is a write a restore put back (`RESTORED_KEY`)."""
    return isinstance(op, dict) and bool(op.get(RESTORED_KEY))


def is_restore_done(directory: str | Path) -> bool:
    """Whether the outbox root ``directory`` holds `RESTORE_DONE`. One stat."""
    return os.path.lexists(Path(directory) / RESTORE_DONE)


def mark_restore_done(directory: str | Path) -> None:
    """Write `RESTORE_DONE` in the outbox root ``directory``. Never raises."""
    try:
        write_text_atomic(Path(directory) / RESTORE_DONE, now_iso() + "\n", mode=0o600)
    except OSError:
        pass


def _stamp_of(op: Any) -> dict | None:
    context = op.get("context") if isinstance(op, dict) else None
    stamp = context.get("principal") if isinstance(context, dict) else None
    return stamp if isinstance(stamp, dict) else None


class _Unreadable(Exception):
    """A set-aside file that could not be read (not one that is gone)."""


def _read_incident_op(path: Path) -> dict | None:
    """The write in ``path`` when it is this incident's (`RESTORE_FINGERPRINT`, an env or in-code
    credential, queued on one of `RESTORE_DAYS`), else None. Other files cost a read, not a parse.
    Raises `_Unreadable` for a file there that cannot be read."""
    try:
        raw = path.read_bytes()
    except (FileNotFoundError, PermissionError):
        return None  # gone, or never this user's to read (`sudo probe`): no write to put back
    except OSError as exc:
        raise _Unreadable(path.name) from exc
    if RESTORE_FINGERPRINT.encode() not in raw:
        return None
    try:
        op = json.loads(raw)
    except ValueError:
        return None
    stamp = _stamp_of(op)
    if (
        stamp is None
        or stamp.get("fingerprint") != RESTORE_FINGERPRINT
        or stamp.get("source") not in (CredentialSource.ENV, CredentialSource.CODE)
        or op_day(op) not in RESTORE_DAYS
    ):
        return None
    return op


def _refused_for_content(op: dict) -> bool:
    """Whether ``op``'s `last_error` is the server refusing what it asked (a stale epoch, no such
    run, a validation or conflict error): an `errors` class that is neither the key's refusal
    (`AuthError`, a revoked-key 403) nor a passing failure (network, 5xx, 429), which a queued
    write carries until its next try."""
    kind = str(op.get("last_error") or "").partition(": ")[0]
    if not kind or op_shows_dead_credential(op):
        return False
    if kind == "AdoptedRouteRefused":
        return True
    found = getattr(errors, kind, None)
    if found is errors.RosError:
        return False  # a status with no class of its own: 408, 429 (`classify`: transient)
    # A workspace limit refuses every write alike until a person fixes it (`settle.py`): passing.
    passing = (errors.TransportError, errors.ServerError, errors.AuthError, errors.OfflineRunNotCreated,
               errors.WorkspaceLimitError, errors.CapabilityUnavailable)
    return isinstance(found, type) and issubclass(found, errors.RosError) and not issubclass(found, passing)


def _why_kept(root: "Journal", op: dict) -> KeptAside | None:
    """Why this incident's set-aside ``op`` stays aside, or None to put it back: never restored
    before, never refused by the server for its content (`_refused_for_content`), a write the
    login may send (`adopted_route_refuses`), and, for an upload, its bytes in ``root``'s
    ``blobs/`` (an unstaged one names a file that may have changed since)."""
    if was_restored(op):
        return KeptAside.RESTORED_BEFORE
    if _refused_for_content(op):
        return KeptAside.REFUSED
    try:
        if _is_multipart(op) or op_credential(op)[1] or adopted_route_refuses(op) is not None:
            return KeptAside.NOT_SENDABLE
        if op.get("kind") == "upload":
            blob = root.blob_path(op)
            if blob is None or not blob.exists():
                return KeptAside.BYTES_GONE
    except (AttributeError, KeyError, TypeError):
        return KeptAside.NOT_SENDABLE  # a malformed write: nothing could send it
    return None


def _put_back(root: "Journal", path: Path, op: dict) -> bool:
    """Move the set-aside file into ``root``'s ``ops/`` under its own name (one rename: a crash
    leaves it in one place, never two), then stamp it `RESTORED_KEY` and keep its mtime. The
    transient budget's clock restarts, as `probe outbox retry` does: ten days old, one 503
    would dead-letter it. A name ``ops/`` already holds is left alone."""
    target = root.ops_dir / path.name
    if target.exists():
        return False
    st = path.stat()
    os.replace(path, target)
    op[RESTORED_KEY] = now_iso()
    op.pop("first_failed_at", None)
    write_text_atomic(target, json.dumps(op, indent=2) + "\n", mode=0o600, sync=SYNC_FILE)
    os.utime(target, ns=(st.st_atime_ns, st.st_mtime_ns))
    return True


def restore_set_aside(root: "Journal") -> RestoreCounts:
    """Put back into the outbox root ``root``'s own ``ops/`` each write its ``discarded/`` holds that
    this incident set aside and the login could send (`_why_kept`), stamped `RESTORED_KEY`. The
    same journal, never a credential queue: staged bytes live per journal, so a move across would
    strand them. Through the append lock (the bytes check too: `gc_blobs` runs under it), in
    batches, then one status recount. Returns what moved and what stayed aside."""
    counts = RestoreCounts()
    source = root.dir / "discarded"
    try:
        names = sorted(n for n in os.listdir(source) if n.endswith(".json"))
    except (FileNotFoundError, PermissionError):
        return counts
    except OSError:
        counts.unmoved += 1  # cannot look now (an I/O error): not done
        return counts
    # This incident's files, found outside every lock: on any other machine nothing is locked.
    found: list[tuple[str, dict]] = []
    for name in names:
        try:
            op = _read_incident_op(source / name)
        except _Unreadable:
            counts.unmoved += 1
            continue
        if op is not None:
            found.append((name, op))
    if not found:
        return counts
    # One write refused for scope keeps every write of the credential (`adoption_account`), so
    # with one among them, none goes back.
    scoped = any(op_refusal(op) == Refusal.SCOPE for _name, op in found)
    root._ensure()
    known: dict = {}
    for start in range(0, len(found), _RESTORE_BATCH):
        moved = 0
        with file_lock(root.append_lock):
            for name, _seen in found[start : start + _RESTORE_BATCH]:
                path = source / name
                try:
                    op = _read_incident_op(path)  # again, under the lock: `gc_blobs` runs under it
                except _Unreadable:
                    counts.unmoved += 1
                    continue
                if op is None:
                    continue  # gone meanwhile
                why = KeptAside.SCOPE if scoped else _why_kept(root, op)
                if why is not None:
                    counts.keep(op, why)
                    continue
                try:
                    if not _put_back(root, path, op):
                        continue  # its name is queued already: that copy goes
                except OSError:
                    counts.unmoved += 1  # stays aside (or queued unstamped): the next pass looks again
                    continue
                counts.add(op)
                known[name] = _meta_of(op)
                moved += 1
            if moved:
                fsync_directory(root.ops_dir)
                fsync_directory(source)
    if counts.writes:
        with file_lock(root.append_lock):
            root._write_status_locked(known=known)
    return counts


def _restored_ops(root: "Journal") -> list[tuple[Path, dict]]:
    """This incident's restored writes still queued in ``root``'s ``ops/``."""
    try:
        names = sorted(n for n in os.listdir(root.ops_dir) if n.endswith(".json"))
    except OSError:
        return []
    found = []
    for name in names:
        try:
            raw = (root.ops_dir / name).read_bytes()
        except OSError:
            continue
        if RESTORED_KEY.encode() not in raw:
            continue
        try:
            op = json.loads(raw)
        except ValueError:
            continue
        stamp = _stamp_of(op)
        if was_restored(op) and stamp is not None and stamp.get("fingerprint") == RESTORE_FINGERPRINT:
            found.append((root.ops_dir / name, op))
    return found


def restored_waiting(root: "Journal") -> int:
    """How many restored writes still wait in ``root``'s ``ops/`` (deferred: sent by a later pass)."""
    return len(_restored_ops(root))


def put_back_restored(root: "Journal", counts: RestoreCounts) -> int:
    """Move the restored writes still queued in ``root`` back to its ``discarded/``, still stamped,
    so no pass tries them again: the login check refused their credential (another account or
    server, a scope, no account on record). Counted into ``counts.refused``. Under the drain
    lock, so no pass is sending one; when another drain holds it past 30 s nothing moves (they
    stay queued, deferred). Returns how many moved. Raises what the file system raised."""
    if not root.ops_dir.exists():
        return 0
    handle = root.drain_lock.open("a+")
    try:
        if not _take_drain_lock(handle, wait_for_lock=True, timeout=30.0):
            return 0
        target = root.dir / "discarded"
        moved = 0
        with file_lock(root.append_lock):
            target.mkdir(parents=True, exist_ok=True, mode=0o700)
            for path, op in _restored_ops(root):
                try:
                    os.replace(path, target / path.name)
                except FileNotFoundError:
                    continue
                root._scan_forget(path.name)
                counts.refused += 1
                counts.base_urls.add(op_base_url(op))
                moved += 1
            if moved:
                fsync_directory(target)
                fsync_directory(root.ops_dir)
                root._write_status_locked()
        return moved
    finally:
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
        finally:
            handle.close()

from probe.sdk.delivery.ops.ops import _is_multipart, _meta_of, op_base_url, op_day  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.adoption import Refusal, adopted_route_refuses, op_refusal, op_shows_dead_credential  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import CredentialSource, op_credential  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.lock import _take_drain_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
