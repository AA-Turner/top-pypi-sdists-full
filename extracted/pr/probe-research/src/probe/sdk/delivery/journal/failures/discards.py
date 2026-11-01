"""Discards: move ops to discarded/ (audit-safe) -- dead letters, held ops, one receipt request -- and relocate credential-queue discards."""

from __future__ import annotations
import os
import re
import time
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from .... import errors
from .....foundation.durable.durable import fsync_directory


#: A dead letter's ``last_error`` (as `drain` writes it) when the server refused it for a past
#: write epoch: before T24 such writes were dead-lettered.
_STALE_EPOCH_LETTER = re.compile("ConflictError: " + errors._STALE_EPOCH_MESSAGE.pattern)
#: ...and when the server said its run does not exist (`errors.names_no_such_run`;
#: a workspace limit's 404 says more, so it never matches).
_NO_SUCH_RUN_LETTER = f"NotFoundError: {errors.RUN_NOT_FOUND_DETAIL}"


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
from probe.sdk.delivery.journal.paths import _credential_queue_dirs  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.status_file import _status_count  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    CREDENTIAL_NAMESPACE,
    _is_run_close,
    _read_op_file,
    op_base_url,
    op_day,
)
