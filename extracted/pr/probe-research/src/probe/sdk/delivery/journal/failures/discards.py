"""Discards: move ops to discarded/ (audit-safe) -- dead letters, held ops, one receipt request -- and relocate credential-queue discards."""

from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import re
import time
from typing import Any, TYPE_CHECKING

from probe.foundation.os_backend import os_backend as oscompat
from probe.foundation.durable.durable import file_lock, write_text_atomic
from probe.sdk.delivery.status_fields import StatusField

from .... import errors
from .....foundation.durable.durable import fsync_directory


if TYPE_CHECKING:
    from typing import Callable

#: A dead letter's ``last_error`` (as `drain` writes it) when the server refused it for a past
#: write epoch: before T24 such writes were dead-lettered.
_STALE_EPOCH_LETTER = re.compile("ConflictError: " + errors._STALE_EPOCH_MESSAGE.pattern)
#: ...and when the server said a run is in the trash (410 `in_trash`: the notice's sentence,
#: `app/projects/trash/notice.py` `TrashNotice.message`).
_TRASHED_LETTER = re.compile(r"\w+: This run is in the trash since ")
#: The op key the drain stamps on a dead letter refused as in the trash: the notice's ``kind`` and
#: ``id``, and ``own_run`` (the trashed thing is the op's own run, `settle._is_own_run_in_trash`).
TRASH_REFUSAL_KEY = "trash_refusal"
#: ...and when the server said its run does not exist (`errors.names_no_such_run`;
#: a workspace limit's 404 says more, so it never matches).
_NO_SUCH_RUN_LETTER = f"NotFoundError: {errors.RUN_NOT_FOUND_DETAIL}"


#: Where a queue keeps dead letters: its own, and its multipart uploads' (`settle._move_to_failed`).
_DEAD_LETTER_FOLDERS = ("failed", "multipart/failed")
#: A request's `delivery_state` while it is not delivered: what a discard moves.
WAITING_STATES = frozenset({"queued", "pending", "failed"})
#: How many days of enqueue dates `outbox.discarded` reports, newest first.
DISCARD_DAYS = 14


@dataclass
class DiscardCounts:
    """What a discard moved (or a pass moving earlier ones to the root, `relocate_discards`) for
    `outbox.discarded`: counts, never a key, body, name or path. ``credentials`` holds
    fingerprints only so they can be counted; ``base_urls`` the servers the writes were pinned
    to, so the event goes only where the writes were going (`outbox_context`)."""

    writes: int = 0
    uploads: int = 0
    bytes: int = 0
    run_closes: int = 0
    credentials: set = field(default_factory=set)
    base_urls: set = field(default_factory=set)
    by_enqueue_day: dict = field(default_factory=dict)
    #: How many enqueue days `outbox.discarded` carries (a class constant, not a field).
    reported_days = DISCARD_DAYS

    def add(self, op: Any, *, mtime: float | None = None) -> None:
        """Count one write; ``op`` is its parsed file (anything else for one that will not
        parse: a write, nothing more known). Never raises: a discard is never stopped by its
        count."""
        self.writes += 1
        if not isinstance(op, dict):
            op = {}
        day = op_day(op)
        if day is None and mtime is not None:
            day = time.strftime("%Y-%m-%d", time.gmtime(mtime))
        if day:
            self.by_enqueue_day[day] = self.by_enqueue_day.get(day, 0) + 1
        upload = op.get("upload") if isinstance(op.get("upload"), dict) else {}
        context = op.get("context") if isinstance(op.get("context"), dict) else {}
        if op.get("kind") == "upload":
            self.uploads += 1
            self.bytes += _status_count(upload.get("size_bytes"))
        try:
            if _is_run_close(op):
                self.run_closes += 1
        except (AttributeError, TypeError):
            pass
        stamp = context.get("principal")
        if isinstance(stamp, dict) and stamp.get("fingerprint"):
            self.credentials.add(str(stamp["fingerprint"]))
        self.base_urls.add(op_base_url(op))

    def merge(self, other: "DiscardCounts") -> None:
        self.writes += other.writes
        self.uploads += other.uploads
        self.bytes += other.bytes
        self.run_closes += other.run_closes
        self.credentials |= other.credentials
        self.base_urls |= other.base_urls
        for day, n in other.by_enqueue_day.items():
            self.by_enqueue_day[day] = self.by_enqueue_day.get(day, 0) + n

    @property
    def base_url(self) -> str | None:
        """The one server every counted write was pinned to, else None (none counted, one
        unpinned, two that differ): nothing is reported then."""
        if len(self.base_urls) != 1:
            return None
        return next(iter(self.base_urls))


def _move_discards(queue: Path, root: Path, counts: DiscardCounts, *, limit: int | None = None) -> int:
    """Move what the credential queue ``queue`` holds in ``discarded/`` to the root's
    ``discarded/``, counting it into ``counts``. A credential queue is deleted once idle
    (`prune_credential_queues`), by this release and every older one (an older SDK in a job's
    environment included) and the root never is, so writes someone set aside are kept there.
    Each file keeps its name and mtime (a rename); a name the root already holds gets the
    queue's name in front, never an overwrite. A file another mover (or a cut-short move)
    already linked there is not moved or counted twice. A receipt namespace's ``discarded/`` is
    not touched: it is how `recover_intents` knows a request was tombstoned. At most ``limit``
    files (None: all). Never raises; returns how many moved."""
    source = queue / "discarded"
    try:
        names = sorted(n for n in os.listdir(source) if not n.startswith("."))
    except OSError:
        return 0
    if not names:
        return 0
    target = root / "discarded"
    try:
        target.mkdir(parents=True, exist_ok=True, mode=0o700)
    except OSError:
        return 0
    label = queue.name.removeprefix(".pruned-").split("-", 1)[0]
    moved = 0
    for name in names:
        if limit is not None and moved >= limit:
            break
        path = source / name
        try:
            st = path.stat()
        except OSError:
            continue
        op = _read_op_file(path)
        for attempt in range(100):
            dest = target / (name if attempt == 0 else f"{label}-{attempt}-{name}")
            try:
                os.link(path, dest)  # fails on an existing name: no overwrite
            except FileExistsError:
                if _same_inode(st, dest):
                    # Linked already, by another mover or a move cut short before its unlink:
                    # the copy stands, the source goes.
                    with suppress(OSError):
                        os.unlink(path)
                    break
                continue
            except OSError:
                # No hard links here (some filesystems): a rename, checked first.
                if dest.exists():
                    continue
                try:
                    os.replace(path, dest)
                except OSError:
                    break
            else:
                try:
                    os.unlink(path)
                except FileNotFoundError:
                    pass  # another mover saw the link landed and removed it: still this one's move
                except OSError:
                    # Kept where it was: the next pass finds the link and removes this one, so
                    # nothing is counted twice.
                    break
            counts.add(op, mtime=st.st_mtime)
            moved += 1
            break
    if moved:
        for directory in (target, source):
            try:
                fsync_directory(directory)
            except OSError:
                pass
    return moved


def is_final_letter(op: dict, error: str) -> bool:
    """A write no retry can ever deliver, told by its stored refusal (``error``, its `last_error`):
    a past write epoch, or its OWN run in the trash (the drain's `TRASH_REFUSAL_KEY` stamp says so;
    an older release's unstamped letter is judged by its text). Never a run's create (`probe sync
    --project` refiles it). The one rule of the sweep, the rescuer's trigger and the close's counts."""
    if is_stale_epoch_letter(error):
        return not _is_create(op)
    if not _TRASHED_LETTER.match(error) or _is_create(op):
        return False
    notice = op.get(TRASH_REFUSAL_KEY)
    if notice is None:
        return True
    return isinstance(notice, dict) and notice.get("kind") == "run" and notice.get("own_run") is True


def is_stale_epoch_letter(error: str) -> bool:
    """Whether a stored refusal says a newer attempt owns the write's run (a past write epoch)."""
    return bool(_STALE_EPOCH_LETTER.match(error))


def _is_create(op: dict) -> bool:
    # Imported only for a refusal that could be final: the offline module is heavy on its own.
    from probe.sdk.delivery.offline.offline import CREATE_KIND

    return op.get("kind") == CREATE_KIND


def _same_inode(st: os.stat_result, path: Path) -> bool:
    try:
        return os.path.samestat(st, path.stat())
    except OSError:
        return False


def relocate_discards(root: Path) -> DiscardCounts:
    """Move every credential queue's discards under the outbox ``root`` to the root's
    ``discarded/`` (`_move_discards`), the queues a prune left half-removed (`.pruned-*`)
    included, idle or not. Returns what moved. Never raises."""
    counts = DiscardCounts()
    try:
        leftovers = sorted(p for p in (root / CREDENTIAL_NAMESPACE).iterdir() if p.name.startswith(".pruned-"))
    except OSError:
        return counts
    for path in [*leftovers, *_credential_queue_dirs(root)]:
        _move_discards(path, root, counts)
    return counts


def _holds_discards(queue: Path) -> bool:
    try:
        with os.scandir(queue / "discarded") as entries:
            return any(not e.name.startswith(".") for e in entries)
    except OSError:
        return False


def discards_to_relocate(root: Path) -> bool:
    """Whether some credential queue under ``root`` holds discards
    (`relocate_discards` has work). Listings only."""
    try:
        entries = list((root / CREDENTIAL_NAMESPACE).iterdir())
    except OSError:
        return False
    return any(
        (p.name.startswith(".pruned-") or re.fullmatch(r"[0-9a-f]{16}", p.name)) and _holds_discards(p)
        for p in entries
    )


class DiscardsMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    def discard_failed(self, op_id: str | None = None) -> int:
        """Move dead letters (one, or all) to ``discarded/``: an audit-safe tombstone, not
        deletion. Covers quarantined-corrupt files too (matched by name when they cannot be
        parsed), which retry can never requeue (red team: without a discard verb they nagged
        forever). Returns how many moved (`discard_failed_counts` says what)."""
        return self.discard_failed_counts(op_id).writes

    def discard_failed_counts(self, op_id: str | None = None) -> DiscardCounts:
        """`discard_failed`, returning what moved (`DiscardCounts`). A credential queue's go to
        the root's ``discarded/``, which no cleanup deletes."""
        counts = DiscardCounts()
        for child in self.namespaces()[1:]:
            counts.merge(child.discard_failed_counts(op_id))
        target = self._discard_dir()
        moved = 0
        with file_lock(self.append_lock):
            if self.failed_dir.exists():
                target.mkdir(parents=True, exist_ok=True, mode=0o700)
                for path in sorted(self.failed_dir.iterdir()):
                    op = _read_op_file(path)
                    if op_id is not None:
                        if isinstance(op, dict):
                            if op.get("op_id") != op_id:
                                continue
                        elif op_id not in path.name:
                            continue
                    os.replace(path, target / path.name)
                    counts.add(op)
                    moved += 1
            if moved:
                fsync_directory(target)
                fsync_directory(self.failed_dir)
                self._write_status_locked()
                self._record_dead_letters()
        if moved:
            self.gc_blobs()
        return counts

    def drop_final_letters(self) -> DiscardCounts:
        """Move to ``discarded/`` the dead letters whose stored refusal is final by itself: a write
        a newer attempt of its run superseded (a past write epoch; a run's epoch only grows), or
        one whose run is in the trash. Every queue's ``failed/`` and ``multipart/failed/`` (a dead
        multipart upload's bytes went when it was dead-lettered). No network: the rescuer runs
        it unasked. A close a takeover set aside stays. Returns what moved (`DiscardCounts`)."""
        return self._drop_letters(is_final_letter, folders=_DEAD_LETTER_FOLDERS)

    def has_final_letter(self, *, limit: int = 200) -> bool:
        """Whether any queue of this outbox holds a dead letter `drop_final_letters` would move,
        reading at most ``limit`` letters per folder, newest first (the rescuer asks on every due
        look, so it stays cheap; a fixed prefix of old letters would hide every newer one)."""
        for queue in self.namespaces():
            if queue.receipt_enabled:
                continue
            for folder in _DEAD_LETTER_FOLDERS:
                try:
                    names = sorted((n for n in os.listdir(queue.dir / folder) if n.endswith(".json")), reverse=True)
                except OSError:
                    continue
                for name in names[:limit]:
                    op = _read_op_file(queue.dir / folder / name)
                    if (
                        isinstance(op, dict)
                        and op.get(TAKEOVER_HOLD_KEY) is None
                        and is_final_letter(op, str(op.get("last_error") or ""))
                    ):
                        return True
        return False

    def drop_unrecoverable(
        self, *, run_exists: "Callable[[dict], bool | None] | None" = None
    ) -> DiscardCounts:
        """`probe doctor --fix` (#3629): `drop_final_letters`, then the dead letters whose run the
        server said does not exist, asked again now with the write's own credential.
        ``run_exists(op)`` answers: False only on the server's own "run not found", None when it
        cannot tell (no credential here, server away): then the letter stays, as does every other
        letter, for `probe outbox retry`. Returns what moved (`DiscardCounts`)."""
        check = run_exists if run_exists is not None else _run_exists_now()
        counts = self.drop_final_letters()
        counts.merge(self._drop_letters(
            lambda op, error: error == _NO_SUCH_RUN_LETTER and bool(op.get("run_ref")) and check(op) is False,
            folders=("failed",),
        ))
        return counts

    def _drop_letters(self, is_doomed: "Callable[[dict, str], bool]", *, folders: tuple[str, ...]) -> DiscardCounts:
        """Move the dead letters ``is_doomed(op, last_error)`` picks, in each of every queue's
        ``folders`` (relative to the queue), to its ``discarded/``."""
        counts = DiscardCounts()
        for queue in self.namespaces():
            if queue.receipt_enabled:
                continue
            for folder in folders:
                queue._drop_letters_in(queue.dir / folder, is_doomed, counts)
        if counts.writes:
            self.gc_blobs()
        return counts

    def _drop_letters_in(self, folder: Path, is_doomed: "Callable[[dict, str], bool]", counts: DiscardCounts) -> None:
        """`_drop_letters` for one of this queue's dead-letter folders: picked unlocked, moved under
        the append lock, skipping a letter retried, discarded or failed again meanwhile."""
        doomed: dict[Path, str] = {}
        for path in sorted(folder.glob("*.json")):
            op = _read_op_file(path)
            if not isinstance(op, dict) or op.get(TAKEOVER_HOLD_KEY) is not None:
                continue
            error = str(op.get("last_error") or "")
            if is_doomed(op, error):
                doomed[path] = error
        if not doomed:
            return
        target = self._discard_dir()
        moved = 0
        with file_lock(self.append_lock):
            target.mkdir(parents=True, exist_ok=True, mode=0o700)
            for path, error in doomed.items():
                op = _read_op_file(path)
                if not isinstance(op, dict) or str(op.get("last_error") or "") != error:
                    continue  # retried, discarded or failed again meanwhile
                os.replace(path, target / path.name)
                counts.add(op)
                moved += 1
            if moved:
                fsync_directory(target)
                fsync_directory(folder)
                self._write_status_locked()
                self._record_dead_letters()

    def _discard_dir(self) -> Path:
        """Where this queue's discards go: its own ``discarded/``, or for a credential queue the
        root's (a credential queue is deleted once idle, by older releases too, and its discards
        with it: `_move_discards`). A receipt namespace keeps its own: `recover_intents` reads it
        there."""
        if self.dir.parent.name == CREDENTIAL_NAMESPACE and not self.receipt_enabled:
            return self.dir.parent.parent / "discarded"
        return self.dir / "discarded"

    def discard_request(self, correlation: str, *, timeout: float = 5.0) -> dict:
        """Tombstone one receipt request wherever it waits (queued, dead-lettered, or an intent
        whose op never landed) so neither a drain nor a retry sends it again. A delivered request
        is left. Returns the state afterwards.

        Taken under the drain lock, so no pass is mid-way through the op; when another drain holds
        it past ``timeout`` nothing moves and the state still says where the request waits. One
        file is moved by name, nothing recounted, blobs left for the next drain to collect:
        `discard_failed` re-reads every dead letter and then all of the queue in `gc_blobs`, which
        made a repair of 1,200 requests take 166 s under the append lock."""
        waiting = WAITING_STATES
        state = self.delivery_state(correlation)
        if state["state"] not in waiting:
            return state
        handle = self.drain_lock.open("a+")
        try:
            if not _take_drain_lock(handle, wait_for_lock=True, timeout=timeout):
                return state
            key = self._correlation_key(correlation)
            with self._correlation_lock(key):
                state = self.delivery_state(correlation)
                if state["state"] not in waiting:
                    return state
                op = self._read_record(self.intents_dir / f"{key}.json")["op"]
                filename = op["queue_filename"]
                target = self.dir / "discarded"
                with file_lock(self.append_lock):
                    target.mkdir(parents=True, exist_ok=True, mode=0o700)
                    source = next(
                        (
                            directory / filename
                            for directory in (self.ops_dir, self.failed_dir)
                            if (directory / filename).exists()
                        ),
                        None,
                    )
                    if source is None:
                        # Pending: the intent committed and its op did not. The tombstone keeps
                        # `recover_intents` from restoring it.
                        write_text_atomic(
                            target / filename, json.dumps(op, indent=2) + "\n", mode=0o600
                        )
                    else:
                        os.replace(source, target / filename)
                        fsync_directory(source.parent)
                        self._scan_forget(filename)
                    fsync_directory(target)
                    # A delta, as an append writes one: a recount re-reads every queued op, per
                    # request. A dead letter's count is the drain's to rewrite, like every status number.
                    if source is not None and source.parent == self.ops_dir:
                        self._write_status_locked(
                            recount=False,
                            pending_delta=-1,
                            pending_bytes_delta=-int((op.get("upload") or {}).get("size_bytes") or 0),
                        )
                    elif source is not None:
                        self._record_dead_letters()
                return self.delivery_state(correlation)
        finally:
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            finally:
                handle.close()

    def discard_held(self, *, credential: str | None = None) -> int:
        """`discard_held_counts`, returning how many moved."""
        return self.discard_held_counts(credential=credential).writes

    def discard_held_counts(self, *, credential: str | None = None) -> DiscardCounts:
        """Move to ``discarded/`` the pending ops no credential here will send (#2041), and with
        ``credential`` that credential's writes too, but for an adopted credential's writes its
        login sends; returns `DiscardCounts`. Never touches an unstamped op or one a live process
        could deliver; takes each queue's drain lock."""
        counts = DiscardCounts()
        for queue in self.namespaces():
            counts.merge(queue._discard_held_here(credential))
        return counts

    def _discard_held_here(self, credential: str | None) -> DiscardCounts:
        from ....settings.settings import load_context

        counts = DiscardCounts()
        if not self.ops_dir.exists():
            return counts
        status = Journal.read_status(self.dir, include_receipts=False) or {}
        refused = status.get(StatusField.REFUSED_FINGERPRINTS) or {}
        handle = self.drain_lock.open("a+")
        try:
            if not _take_drain_lock(handle, wait_for_lock=True, timeout=30.0):
                return counts
            held: list[Path] = []
            adopted_here: dict = {}
            queued = self._read_dir(self.ops_dir)
            # One token is one account, as in `drain`.
            accounts: dict[str, tuple[str, str]] = {}
            for _path, queued_op in queued:
                queued_stamp = (queued_op.get("context") or {}).get("principal")
                queued_as = stamp_identity(queued_stamp) if isinstance(queued_stamp, dict) else None
                if queued_as is not None:
                    accounts.setdefault(str(queued_stamp.get("fingerprint")), queued_as)
            for path, op in queued:
                stamp = (op.get("context") or {}).get("principal")
                if not isinstance(stamp, dict) or not stamp.get("fingerprint"):
                    continue
                fingerprint, ingest = op_credential(op)
                if fingerprint not in adopted_here:
                    adopted_here[fingerprint] = adopted_account(fingerprint) is not None
                adopted = not ingest and adopted_here[fingerprint]
                if credential and credential in (stamp.get("fingerprint"), stamp.get("ingest_fingerprint")):
                    if not adopted or adopted_route_refuses(op) is not None:
                        held.append(path)  # named by the user
                        continue
                    # Adopted: the login sends it unless it now may not, as for any other.
                if stamp.get("source") != CredentialSource.CONFIG and not adopted:
                    continue  # another job's: that job sends it
                if ingest:
                    continue
                if fingerprint in refused and not adopted:
                    try:
                        stored = load_context((op.get("context") or {}).get("name"))
                    except Exception:  # noqa: BLE001
                        stored = {}
                    if credential_fingerprint(stored.get("token"), None) == fingerprint:
                        held.append(path)  # its login was refused and is still the stored one
                    continue
                try:
                    _settings_for_op(
                        op.get("context"),
                        ingest=False,
                        account=accounts.get(fingerprint) or recorded_account(fingerprint),
                    )
                except CredentialNotHere as absent:
                    if absent.permanent:
                        held.append(path)
                except Exception:  # noqa: BLE001 -- logged out, unroutable: not "held"
                    continue
            # A run a drain is sending now, its drain lock let go for an upload (#3618), stays:
            # that drain settles its files after.
            lanes = {path: _lane_of(op) for path, op in queued}
            probe = _DrainHold(self, handle, urgent=False)
            try:
                held = [path for path in held if not probe.busy(lanes.get(path))]
            finally:
                probe.close()
            if not held:
                return counts
            by_path = dict(queued)
            target = self._discard_dir()
            with file_lock(self.append_lock):
                target.mkdir(parents=True, exist_ok=True, mode=0o700)
                for path in held:
                    try:
                        os.replace(path, target / path.name)
                    except FileNotFoundError:
                        continue  # delivered meanwhile
                    self._scan_forget(path.name)
                    counts.add(by_path.get(path))
                fsync_directory(target)
                fsync_directory(self.ops_dir)
                gone = set(held)
                emptied = {op_credential(op)[0] for path, op in queued if path in gone and isinstance(op, dict)}
                emptied -= {op_credential(op)[0] for path, op in queued if path not in gone and isinstance(op, dict)}
                try:
                    on_disk = json.loads(self.status_file.read_text())
                    written = on_disk.get(StatusField.REFUSED_FINGERPRINTS) or {}
                except (OSError, ValueError, AttributeError):
                    written = {}
                self._write_status_locked(
                    held=0,
                    close_held=0,
                    held_at=None,
                    # A credential with nothing left here is refused nothing.
                    refused_fingerprints={fp: at for fp, at in dict(written).items() if fp not in emptied},
                )
        finally:
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            finally:
                handle.close()
        self.gc_blobs()
        return counts

from probe.sdk.delivery.journal.paths import _credential_queue_dirs  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.status_file import _status_count  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CREDENTIAL_NAMESPACE,
    _is_run_close,
    _read_op_file,
    op_base_url,
    op_day,
)
from probe.sdk.delivery.outbox.drain.report import CredentialNotHere  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import CredentialSource  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import TAKEOVER_HOLD_KEY  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.lock import _DrainHold  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _lane_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.classify import _run_exists_now  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import _settings_for_op  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.lock import _take_drain_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.adoption import adopted_account  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import credential_fingerprint  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import op_credential  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.accounts import recorded_account  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.credentials import stamp_identity  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.drain.adoption import adopted_route_refuses  # noqa: E402 -- pieces need each other; the front door loads this one first
