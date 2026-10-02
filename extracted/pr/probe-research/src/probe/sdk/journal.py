"""The durable outbox journal: ONE ordered queue for every deferred write.

Design (eng review 2026-07-29, T1-C): a single versioned operation journal
replaces the JSONL spool + would-be maildir split. Every async operation --
metric batch, span, note, reference-add, artifact upload, run end -- is one op
file; file-bearing ops reference a content-addressed blob store next door.

Layout (everything 0o700 dirs / 0o600 files -- queue contents are research
data and the journal may live on shared storage):

    <dir>/ops/<time_ns>-<op_id>.json     one op, atomic write; FIFO by filename
    <dir>/failed/<same name>.json        dead letters (permanent rejections)
    <dir>/blobs/<sha256>                 staged bytes, deduped by content
    <dir>/blobs/incoming-<op_id>         staged bytes not yet hashed (11A: big
                                         files hash in the drainer, not enqueue)
    <dir>/status.json                    single-stat summary for the banner
    <dir>/paused                         marker: drains are suspended
    <dir>/.append.lock / .drain.lock     flock sidecars
    <dir>/producers/<producer>.json      per-writer accounting (parity F4):
                                         sequence high-water, delivered tally,
                                         capture gaps, open/closed state

Ops never carry credentials: they pin a context NAME + base_url (5A) and the
drain resolves tokens fresh via ``config.resolve``. Import of this module must
stay httpx-free -- enqueue runs beside training loops; the network stack loads
only inside :func:`drain`.

Op schema (``probe.outbox/1``)::

    {
      "schema": "probe.outbox/1",
      "op_id": "<uuid hex>",
      "kind": "http" | "upload" | "rejected_http",
      "run_ref": "<run id/slug>" | null,       # barrier scoping (T3-A)
      "context": {"name": <str|null>, "base_url": <str>},
      "enqueued_at": <iso8601>,
      "attempts": <int>, "last_error": <str|null>,
      "first_failed_at": <epoch seconds>,     # set at the first transient
                                              # failure; the 24 h budget's clock
      # when the writer registered with the producer registry (F4):
      "producer_id": <str>, "producer_sequence": <int>,
      # kind == "http":
      "method": ..., "path": ..., "body": {...} | null,
      # kind == "upload":
      "upload": {"anchor", "anchor_id", "name", "content_type", "kind",
                 "meta", "span_id", "step_index", "blob": <sha256|null>,
                 "src_path", "staged": <bool>, "size_bytes": <int|null>,
                 "unstaged_reason": <str|null>, "artifact_id": <hint|null>}
    }

``staged`` false means the op REFERENCES ``src_path`` and the drainer reads the
original bytes. ``unstaged_reason`` says why when the journal made that choice
itself (disk headroom) rather than the caller asking for it.

Failure policy (7A + T2-A, phase-aware per the codex pass):
  * permanent rejection (4xx except 408/429/auth) -> the op moves to failed/
    and the queue keeps flowing; ``retry_failed`` puts it back.
  * transient (network, 5xx, 408, 429, unexpected exceptions) -> the drain
    stops in place; nothing is moved; the drainer retries with backoff.
  * 401/403 -> the drain halts as a CREDENTIAL-level blocker; ops stay queued
    untouched (an expired token must not cascade the queue into dead letters).
  * 409 carrying ``existing_id`` -> an idempotent replay already landed;
    counted as delivered.
"""

from __future__ import annotations

import errno as errno_module
import json
import hashlib
import logging
import os
import re
import shutil
import time
import uuid
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import closing, contextmanager
from dataclasses import dataclass, field
from probe._compat import StrEnum
from pathlib import Path
from typing import Any, Callable

from .._shared import oscompat
from . import errors
from . import homedir
from . import safe_warn as _diagnostics
from .durable import (
    SYNC_FILE,
    SYNC_FULL,
    SYNC_NONE,
    file_lock,
    fsync_directory,
    now_iso,
    write_text_atomic,
)
from .hashing import fingerprint
from .session_marker import WIZARD_HINT
from .secret_gate import (
    CredentialBlocked,
    check_upload,
    read_source,
    redact_quick_bytes,
    safe_snapshot_file as snapshot_file,
    strict_policy,
)
from .redaction import default_scrub, scrub_text
from .stamp_scrub import scrub_body, scrub_envelope, scrub_op

log = logging.getLogger(__name__)


def _source_digest(path: str) -> str:
    """sha256 of the file AS IT SITS, before any redaction."""
    return hashlib.sha256(read_source(path)).hexdigest()


def _same_file(handle, path: Path) -> bool:
    """The locked handle is still the file at `path`. Item locks are unlinked
    when an item is done; one opened just before that unlink and locked just
    after it is a lock on nothing, while the next opener creates a new file.

    Always true on Windows: a file another handle has open cannot be deleted
    there (see `_retire_lock`), so a held lock is the file at its path."""
    if os.name == "nt":
        return True
    try:
        return os.fstat(handle.fileno()).st_ino == os.stat(path).st_ino
    except FileNotFoundError:
        return False


#: Windows: item locks `_retire_lock` was asked to delete while this process
#: held them, deleted as `_try_lock` / `_item_lock` let go.
_RETIRED_WHILE_HELD: set[str] = set()


def _retire_lock(path: Path) -> None:
    """Delete an item lock this process holds (safe on POSIX: see `_same_file`).

    Windows refuses to delete a file that is open, so there the delete waits
    for the release (`_release_retired`), where it may still fail because
    another process opened the file to wait for it. That is the safe outcome:
    that waiter then locks the live file, finds the item done, and the orphan
    sweep retires the lock later."""
    if os.name != "nt":
        path.unlink(missing_ok=True)
        return
    _RETIRED_WHILE_HELD.add(str(path))


def _release_retired(path: Path) -> None:
    """After a lock's handle is closed: the delete `_retire_lock` deferred."""
    if not _RETIRED_WHILE_HELD or str(path) not in _RETIRED_WHILE_HELD:
        return
    _RETIRED_WHILE_HELD.discard(str(path))
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass  # open elsewhere: the orphan sweep retires it


@contextmanager
def _try_lock(path: Path):
    """Non-blocking flock: yields whether this process now holds it. The kernel
    drops it if the holder dies, so a crashed promoter never wedges an item."""
    handle = open(path, "a+")
    try:
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except BlockingIOError:
            yield False
            return
        try:
            yield _same_file(handle, path)
        finally:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
    finally:
        handle.close()
        _release_retired(path)


@contextmanager
def _item_lock(path: Path):
    """Blocking flock on an item lock, re-opened until it holds the file that
    is actually at `path` (see `_same_file`)."""
    while True:
        handle = open(path, "a+")
        oscompat.flock(handle.fileno(), oscompat.LOCK_EX)
        if _same_file(handle, path):
            break
        handle.close()
    try:
        yield
    finally:
        oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
        handle.close()
        _release_retired(path)


def _write_private(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_BINARY", 0), 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


SCHEMA = "probe.outbox/1"

#: The op kinds this release's drain can deliver (plan 1.11). A worker
#: advertises them in its caps file (`outbox_worker`), and an op of any OTHER
#: kind -- queued by a newer SDK sharing this outbox -- is held in its run's
#: lane, never attempted and never dead-lettered, until a worker that knows it
#: drains the queue. Releases before this one dead-lettered an unknown kind as
#: permanent, which is why a producer asks the live worker first
#: (`outbox_worker.ready_for`) before it queues a new kind.
#:
#: `create_run` is an OFFLINE run's create (plan 2.12). It is queued only in
#: `<outbox>/offline/<key>/`, which nothing but `probe sync` drains, so no older
#: worker can ever meet it and no `ready_for` handshake is needed -- but this
#: drain (the one `probe sync` runs) must list it, or it holds the create and
#: every write of the run behind it forever.
#:
#: `multipart_upload` is an artifact over 64 MiB (plan item (g),
#: `sdk/multipart.py`): staged, then sent in parts straight to object storage,
#: in a lane of its own (`op["lane"]`) so its minutes of transfer never hold
#: the run's metrics. Its ops are queued in `<outbox>/multipart/ops/`, which no
#: earlier release reads, so an older worker sharing this outbox never meets
#: one (it neither holds nor dead-letters it); the producer still asks
#: `outbox_worker.ready_for` so such a worker steps aside for a current one.
OP_KINDS = frozenset({"http", "upload", "rejected_http", "create_run", "multipart_upload"})
DELIVERY_NAMESPACE = "delivery-v1"
#: Where a client that stamps its credential (#2035) queues, one directory per
#: credential fingerprint: `<outbox>/credential-v1/<fingerprint>/`. No release
#: before the stamp ever looks here, so none of them can send such a write with
#: the wrong login -- or stop its own pass on one (#2041 reviews). And each
#: credential has its own queue, lease and worker: a job whose token nothing
#: else holds never waits behind another credential's busy worker.
CREDENTIAL_NAMESPACE = "credential-v1"
DELIVERY_SCHEMA = "probe.outbox.delivery/1"
RECEIPT_INDEX_VERSION = 1
RECEIPT_COMPACTION_BATCH = 256


def _inline_hash_max() -> int:
    raw = os.environ.get("PROBE_ASYNC_INLINE_HASH_MAX")
    if raw:
        try:
            return int(raw)
        except ValueError:
            # A malformed override must not crash every import of this module
            # (client construction, enqueue, the drainer) -- fall back loudly.
            import warnings

            warnings.warn(
                f"ignoring malformed PROBE_ASYNC_INLINE_HASH_MAX={raw!r}; "
                "expected an integer byte count",
                stacklevel=2,
            )
    return 256 * 1024 * 1024


#: 11A -- files at or under this size hash (and presign-ping) inline at
#: enqueue; larger ones snapshot instantly and hash in the drainer.
INLINE_HASH_MAX_BYTES = _inline_hash_max()


def _min_free_bytes() -> int | None:
    """``PROBE_OUTBOX_MIN_FREE_BYTES``, or None: scale with the volume
    (`free_floor`)."""
    raw = os.environ.get("PROBE_OUTBOX_MIN_FREE_BYTES")
    if raw:
        try:
            return max(0, int(raw))
        except ValueError:
            # Same contract as _inline_hash_max: a malformed override must not
            # crash every import of this module -- fall back loudly.
            import warnings

            warnings.warn(
                f"ignoring malformed PROBE_OUTBOX_MIN_FREE_BYTES={raw!r}; "
                "expected an integer byte count",
                stacklevel=2,
            )
    return None


#: The free-space floor without an override (plan 1.5): 5 % of the volume,
#: never under 256 MiB (unless that is over a quarter of the volume) and never
#: over 2 GiB. A fixed 2 GiB floor refused every
#: write on a small pod volume or a laptop with 1.9 GiB free while the network
#: was fine (live: 0 of 30 points arrived).
_FLOOR_CEILING = 2 * 1024 * 1024 * 1024
_FLOOR_MINIMUM = 256 * 1024 * 1024
_FLOOR_FRACTION = 0.05


def free_floor(directory: str | Path) -> int:
    """The free bytes a queue on ``directory`` must leave (0: no floor)."""
    if MIN_FREE_BYTES is not None:
        return MIN_FREE_BYTES
    try:
        total = shutil.disk_usage(directory).total
    except OSError:
        return _FLOOR_CEILING
    # Never more than a quarter of the volume: on a small tmpfs (a fallback
    # $TMPDIR under 256 MiB) the minimum would exceed the whole disk and refuse
    # every write (review of #2054).
    return min(_FLOOR_CEILING, max(_FLOOR_MINIMUM, int(total * _FLOOR_FRACTION)), total // 4)


#: Headroom the blob store must LEAVE on its filesystem. Staging is a real byte
#: copy whenever the source is on another filesystem -- `try_clone` is
#: copy-on-write and cannot span mounts -- so importing a research folder off a
#: network share copies every file under the reference threshold onto the local
#: disk. Enqueue is fire-and-forget and the drainer is a single worker, so a
#: producer that outruns delivery grows the queue without bound: filling the
#: disk is the STEADY STATE of that shape, not an edge case.
#:
#: The check is deliberately blind to whether the copy would actually consume
#: space: a same-filesystem clone costs nothing, but so does declining to make
#: one (the source is on that same disk and the drainer reads it in place), so
#: the conservative answer is never the worse one and costs one statvfs.
#:
#: Zero disables the guard, for a caller who has measured their own ceiling.
MIN_FREE_BYTES = _min_free_bytes()


def _max_pending_ops() -> int:
    raw = os.environ.get("PROBE_OUTBOX_MAX_PENDING")
    if raw:
        try:
            return max(0, int(raw))
        except ValueError:
            import warnings

            warnings.warn(
                f"ignoring malformed PROBE_OUTBOX_MAX_PENDING={raw!r}; "
                "expected an integer op count",
                stacklevel=2,
            )
    return 500_000


#: Backstop on QUEUE LENGTH, independent of the byte floor above. Op files are
#: small, so a stalled drainer exhausts inodes and directory-scan patience long
#: before it exhausts bytes: a loop logging ten points a second queues ~864k
#: files a day. Zero disables. The floor is what normally bites; this is what
#: catches a filesystem that reports plenty of free space and still cannot take
#: another entry.
MAX_PENDING_OPS = _max_pending_ops()

#: Sample the free-space stat every N appends rather than on each one. Disk
#: pressure builds over thousands of writes, so a per-append statvfs would
#: reintroduce exactly the per-write syscall cost the enqueue just shed.
_STATVFS_EVERY = 256

#: At most one real directory count of the queue per this many seconds, and
#: only on the path that would otherwise REFUSE a write (plan 0.1): a drain
#: pass rewrites status.json only when it ends, so mid-pass the file still says
#: "full" while the real queue has drained (review of #2014: 94 queued,
#: status.json 200, 20 of 20 writes refused; at 500k and ~13 ops/s a pass is
#: hours of refused data).
_RECOUNT_EVERY_SECONDS = 1.0

#: Dead letters status.json remembers (plan 1.7), and how much of each error.
_RECENT_DEAD_LETTERS = 32
_DEAD_LETTER_ERROR_CHARS = 300

#: How many capture-gap records a producer file keeps; `gap_count` keeps the
#: total. The list used to grow by one per dropped write, and the file is
#: rewritten on every drop: 6,000 drops made a refused `log()` 16 ms -> 107 ms.
_GAPS_KEPT = 32


class OutboxFull(OSError):
    """The journal refused a write because the queue is at its ceiling.

    An OSError subclass on purpose: `Client._enqueue` already treats a failure
    to journal as "drop the datapoint, record the gap, keep training", and a
    full outbox is exactly that -- a disk-shaped refusal, not a new class of
    problem for callers to learn.
    """


_RUN_PATH = re.compile(r"^/v1/runs/([^/]+)(?:/|$)")

_SAFE_COMPONENT = re.compile(r"[^A-Za-z0-9._-]+")


def _safe_component(value: str) -> str:
    return _SAFE_COMPONENT.sub("_", value)[:120] or "producer"

# Transient-when-status statuses beyond the typed transport/server errors.
_TRANSIENT_STATUSES = {408, 429}

#: Statuses a server uses to say "not ever", not "not now". 501 is the only one:
#: RFC 9110 defines it as the server not SUPPORTING the method, and makes it
#: cacheable by default -- the wire's own way of spelling permanent. It has to be
#: named explicitly because it is a 5xx, and every other 5xx is a transient
#: server-side hiccup worth retrying.
_PERMANENT_STATUSES = {501}

#: How long one op may keep failing transiently -- measured from its FIRST
#: failure, on the wall clock -- before the drain stops believing it will ever
#: succeed (plan 0.6).
#:
#: The queue is strict FIFO and stops at the first failure, so an op that can
#: never succeed does not merely fail -- it parks every write behind it. That is
#: not hypothetical: a storage-less deployment answered a checkpoint upload 503,
#: the drain read "retry later", and 452 metric and span writes starved behind
#: five uploads over 288 attempts. Past the budget the op takes the permanent
#: path -- dead-lettered, and for an upload the reference-artifact fallback
#: still records the file -- so the queue drains.
#:
#: It used to be an ATTEMPT count (50), which let the POLL RATE decide when data
#: was thrown away: `finish()`'s 0.25 s loop spent all 50 in ~13 s and the
#: in-process exporter in ~7 s, so an ordinary deploy-length blip dead-lettered
#: a run's final writes. A day outlasts any outage worth waiting out and is
#: still finite. ``attempts`` stays on the op, for diagnostics only.
#: ``PROBE_OUTBOX_TRANSIENT_BUDGET_SEC`` overrides it.
TRANSIENT_BUDGET_SECONDS = 24 * 60 * 60.0

#: ...AND at least this many attempts. Time alone would dead-letter a laptop's
#: whole queue on the first blip after it slept through a day; attempts alone
#: let the poll rate decide. Both must be spent. The cost, until per-run lanes
#: (plan 1.6) stop one run's head from holding the others: a poison op the
#: server always answers 5xx blocks the machine's FIFO for a day.
MIN_TRANSIENT_ATTEMPTS = 50


def _transient_budget_seconds() -> float:
    """Read at failure time (rare), so a test or an operator can change it
    without re-importing; a malformed value warns and keeps the default."""
    raw = os.environ.get("PROBE_OUTBOX_TRANSIENT_BUDGET_SEC")
    if raw:
        try:
            return max(0.0, float(raw))
        except ValueError:
            # Read inside a drain: a plain warnings.warn raises under -W error.
            _diagnostics.warn(
                f"ignoring malformed PROBE_OUTBOX_TRANSIENT_BUDGET_SEC={raw!r}; "
                "expected seconds as a float",
                stacklevel=2,
            )
    return TRANSIENT_BUDGET_SECONDS


def _failing_for_seconds(op: dict, now: float) -> float:
    """Seconds since this op FIRST failed transiently. Stamps ``first_failed_at``
    (epoch seconds) on the op the first time, so the clock survives the op being
    rewritten, the worker restarting and the machine rebooting."""
    first = op.get("first_failed_at")
    if not isinstance(first, (int, float)) or isinstance(first, bool):
        op["first_failed_at"] = now
        return 0.0
    return max(0.0, now - float(first))


#: Environment variables that identify a GLOBALLY unique rank in a distributed
#: job. Order matters only for tie-breaking; any one of them is sufficient.
#: `LOCAL_RANK` is deliberately absent from this list -- it repeats per node, so
#: on a shared filesystem two nodes' rank 0 would collide back into one queue.
_GLOBAL_RANK_VARS = ("SLURM_PROCID", "RANK", "OMPI_COMM_WORLD_RANK")


def _rank_suffix() -> str | None:
    """A per-rank directory component, or None for a single-process job.

    A distributed job puts every rank on ONE journal when $HOME is shared, which
    is the normal SLURM layout: one `.append.lock`, one `.seq`, one `ops/`. The
    append flock then serialises metric logging across every rank on every node
    -- a cluster-wide mutex on the path that is supposed to be the cheap one.

    Splitting per rank fixes that without moving the queue somewhere volatile.
    Node-local scratch would be faster still and is the wrong trade:
    $SLURM_TMPDIR is reaped when the job ends, so a queue that had not drained
    would be destroyed by the very thing durability exists to survive.

    A single-process run gets no suffix at all, so the default path is
    byte-identical to what it has always been and nothing needs migrating.
    """
    for var in _GLOBAL_RANK_VARS:
        raw = (os.environ.get(var) or "").strip()
        if raw:
            return f"rank-{_safe_component(raw)}"
    local = (os.environ.get("LOCAL_RANK") or "").strip()
    if local:
        # Only node-local identity is advertised, so qualify it with the host to
        # keep two nodes' rank 0 apart on shared storage.
        import socket

        return f"rank-{_safe_component(socket.gethostname())}-{_safe_component(local)}"
    return None


def default_root() -> Path:
    """The machine's outbox root, without the per-rank component: every
    process of this user queues in it or in one of its ``rank-*`` children."""
    configured = os.environ.get("PROBE_OUTBOX_DIR")
    try:
        if configured:
            return Path(configured).expanduser()
        base = os.environ.get("XDG_STATE_HOME")
        root = Path(base) if base else Path.home() / ".local" / "state"
    except (RuntimeError, KeyError, OSError):
        # No HOME and no passwd entry (a container running an arbitrary uid):
        # `Path.home()` raises, and it used to crash `Client()` (plan 1.5).
        return private_fallback_root()
    return root / "probe" / "outbox"


def default_dir() -> Path:
    """This process's queue: the root, or its ``rank-*`` child in a distributed job.

    An explicit ``PROBE_OUTBOX_DIR`` is the ROOT too. It is exported once for a
    whole job -- the reliability plan's rollout note tells a cluster to set it --
    so returning it as is put every rank of every node on one ``.append.lock``:
    on an NFS home a cross-client lock that the kernel polls with backoff, which
    held each ``log()`` up to ~30 s (agent/tests/environments/nfs_home)."""
    root = default_root()
    suffix = _rank_suffix()
    return root / suffix if suffix else root


def _uid() -> int | str:
    return os.getuid() if hasattr(os, "getuid") else "user"


def fallback_root() -> Path:
    """The NAME of the fallback outbox (plan 1.5): ``$TMPDIR/probe-outbox-<uid>``.
    NOT durable across a pod or machine restart, which is what the warning
    that selects it says. Anyone can create that name in a shared ``/tmp``, so
    use `private_fallback_root`, which only ever returns a directory this user
    owns and nobody else can write to."""
    import tempfile

    return Path(tempfile.gettempdir()) / f"probe-outbox-{_uid()}"


def trusted_dir(path: str | Path) -> bool:
    """A queue directory this process may use and deliver from: a real
    directory (never a symlink), owned by this user, with no group or other
    permission bits. Anything else in a shared ``$TMPDIR`` may have been made
    by someone else to get their ops sent with this user's credential, or to
    read this user's queue (review of #2054, P1)."""
    import stat

    try:
        info = os.lstat(path)
    except OSError:
        return False
    return (
        stat.S_ISDIR(info.st_mode)
        and (not hasattr(os, "getuid") or info.st_uid == os.getuid())
        and not info.st_mode & 0o077
    )


_private_fallback: Path | None = None


def private_fallback_root() -> Path:
    """The fallback outbox root, guaranteed private: `fallback_root` when it
    is (or can be created as) a `trusted_dir`, else a fresh
    ``probe-outbox-<uid>-XXXX`` from `tempfile.mkdtemp` (which creates it 0700,
    atomically). Chosen once per process."""
    global _private_fallback
    # Windows: `trusted_dir` never passes there (no permission bits), so this
    # is always this process's own `mkdtemp` -- kept, not re-minted per call.
    if _private_fallback is not None and (os.name == "nt" or trusted_dir(_private_fallback)):
        return _private_fallback
    import tempfile

    root = fallback_root()
    try:
        os.mkdir(root, 0o700)
    except FileExistsError:
        pass
    except OSError:
        pass
    if not trusted_dir(root):
        root = Path(tempfile.mkdtemp(prefix=f"probe-outbox-{_uid()}-"))
    _private_fallback = root
    return root


def fallback_dir() -> Path:
    suffix = _rank_suffix()
    root = private_fallback_root()
    return root / suffix if suffix else root


def _fallback_roots() -> list[Path]:
    """Every fallback root of this user in ``$TMPDIR`` that is a `trusted_dir`
    (the fixed name, and any `mkdtemp` one a process had to take)."""
    import tempfile

    base = Path(tempfile.gettempdir())
    prefix = f"probe-outbox-{_uid()}"
    roots = []
    try:
        names = sorted(os.listdir(base))
    except OSError:
        return roots
    for name in names:
        if name == prefix or name.startswith(prefix + "-"):
            path = base / name
            if trusted_dir(path):
                roots.append(path)
    return roots


#: `flock` failures that mean locks will never work on this filesystem. Any
#: other (EWOULDBLOCK/EAGAIN) means someone else holds the lock, which is
#: normal and must never read as "unusable" (Codex, round 2: contention must
#: not redirect a healthy PV-backed queue to ephemeral storage).
_UNUSABLE_LOCK_ERRNOS = frozenset(
    code
    for code in (
        getattr(errno_module, name, None)
        for name in ("ENOSYS", "ENOLCK", "EROFS", "EACCES", "EPERM", "EOPNOTSUPP")
    )
    if code is not None
)


def classify(exc: Exception) -> str:
    """``transient`` | ``permanent`` | ``auth`` | ``idempotent`` for one failure.

    Phase-agnostic core; the phase-AWARE cases (404 after a ``have`` dedup, the
    superseded-confirm race) are handled where the phase is known -- inside
    ``Client.upload_fingerprinted`` -- and never reach this classifier.
    Anything that is not a typed client error counts as transient: our own bug
    must park the queue, not destroy data.
    """
    if isinstance(exc, CredentialBlocked):
        return "permanent"
    if isinstance(exc, errors.UnroutableEndpointError):
        # Checked BEFORE AuthError, which it subclasses. "auth" means a login
        # would fix it, so the drainer parks the queue and keeps the data; an
        # op pinned to an endpoint no credential here can ever satisfy is not
        # that, and parking on it stops every op behind it -- including the
        # ones bound for the endpoint that IS logged in. Dead-letter it
        # instead: visible in `probe outbox status`, retryable with `probe
        # outbox retry` if that endpoint ever becomes reachable, and out of
        # the way of a queue that has somewhere to go.
        return "permanent"
    if isinstance(exc, errors.WorkspaceLockedError):
        # Checked BEFORE ScopeError, which it subclasses -- same shape as
        # UnroutableEndpointError above. "auth" parks the whole queue and is
        # right when the CREDENTIAL is wrong; this 403 says one DESTINATION is
        # closed to this person, and every other queued op is still deliverable.
        # Parking here would stall a researcher's entire backlog behind one file
        # bound for a workspace they are not on.
        return "permanent"
    if isinstance(exc, errors.UploadRefused):
        # A presigned upload's own capability refused (#2073): no credential
        # was sent, so a login cannot fix it and parking the queue on it
        # stopped every write of the run. This upload fails, recorded as
        # failed; everything else keeps going.
        return "permanent"
    if isinstance(exc, (errors.AuthError, errors.ScopeError)):
        return "auth"
    if isinstance(exc, errors.ConflictError):
        return "idempotent" if exc.existing_id else "permanent"
    if isinstance(exc, errors.ValidationError):
        # Includes locally-raised journal errors (missing staged bytes, unknown
        # op kind) that carry no HTTP status: retrying can never satisfy them,
        # and 'transient' would park the drainer on them forever (perf review).
        return "permanent"
    if isinstance(exc, (errors.TransportError, errors.ServerError)):
        # A ServerError still carries the status, and one 5xx means "never"
        # rather than "not yet" -- see `_PERMANENT_STATUSES`. Checked before the
        # blanket transient answer, or the honest code is thrown away.
        if getattr(exc, "status", None) in _PERMANENT_STATUSES:
            return "permanent"
        return "transient"
    if isinstance(exc, errors.RosError):
        if exc.status in _TRANSIENT_STATUSES:
            return "transient"
        if exc.status in _PERMANENT_STATUSES:
            return "permanent"
        if exc.status is not None and 400 <= exc.status < 500:
            return "permanent"
        return "transient"
    return "transient"


#: The server's 409 for an edge whose exact (source, relation, target) already
#: exists (`app/lineage/service.py`). Its OTHER 409 on this route -- "this run
#: already has a genealogy parent" -- names a DIFFERENT edge and is a real conflict.
_EDGE_EXISTS = "lineage edge already exists"


def edge_already_exists(exc: Exception) -> bool:
    """Is this the server's "lineage edge already exists" 409 -- the exact
    edge (source, relation, target) is there -- and not its other 409 on
    `POST /v1/edges`, a second genealogy parent, which names a DIFFERENT edge?
    One rule for the outbox (`_edge_already_there`) and `probe edge add`."""
    if not isinstance(exc, errors.ConflictError):
        return False
    detail = exc.detail if isinstance(exc.detail, dict) else {}
    return str(detail.get("message") or exc).startswith(_EDGE_EXISTS)


def _edge_already_there(op: dict, exc: Exception) -> bool:
    """A queued ``POST /v1/edges`` the server answered "lineage edge already
    exists": the edge it asked for is recorded, so the write is done. Unlike the
    general 409-with-existing_id rule, true on a FIRST attempt too: the conflict
    key is the whole edge (source, relation, target). What the op carried beyond
    that (``reason``, ``meta``, ``provenance``) is NOT applied to the edge that
    was there; the delivery logs it when the op carried any (a dead letter would
    hold the outbox for a human over an annotation)."""
    if op.get("correlation"):
        return False
    if op.get("kind") != "http" or op.get("method") != "POST" or op.get("path") != "/v1/edges":
        return False
    return edge_already_exists(exc)


def run_ref_for_path(path: str) -> str | None:
    """The run a v1 path addresses, when it addresses one. Barrier scoping key."""
    match = _RUN_PATH.match(path)
    return match.group(1) if match else None


def _is_uuid(ref: str) -> bool:
    try:
        uuid.UUID(ref)
    except (AttributeError, TypeError, ValueError):
        return False
    return True


def _resolve_queued_run_ref(
    client, ref: str | None, cache: dict[str, str]
) -> tuple[str, str] | None:
    """``(petname, uuid)`` for a ref a 422 just rejected, or None to re-raise.

    Enqueue deliberately does NOT read the run: ``--async`` exists so a write can
    be queued with no network, and the CLI's ``_async_run`` builds a handle from
    the raw ref for exactly that reason. The cost landed here -- every route the
    drainer replays EXCEPT ``GET /v1/runs/{ref}`` types its path param as a UUID,
    so a petname (``probe --async log tunneling-sambar-254 ...``, or a manifest
    row anchored on one) queued cleanly, reported ``failed: 0``, and then
    dead-lettered on a 422 minutes later in a process nobody was watching.

    Called only AFTER a 422, never before, which is what keeps this free: the
    happy path pays nothing, a UUID never reaches it, and a genuine body
    validation error is not turned into an extra lookup that hides it. The retry
    it enables can only turn a failing op into a delivered one.

    None means "nothing to retry" -- the ref is absent, already a UUID, or the
    lookup failed. The caller then re-raises the original 422, so the op dead
    letters on the error the server actually gave rather than on ours.

    Cached per drain, not globally: an id is immutable, but a cache outliving the
    process would keep answering for a run that has since been deleted.
    """
    if not ref or _is_uuid(ref):
        return None
    if ref not in cache:
        try:
            cache[ref] = str(client.get_run(ref)["id"])
        except Exception:  # noqa: BLE001 -- the original 422 is the better error
            return None
    return (ref, cache[ref]) if cache[ref] != ref else None


class OpHeldHere(Exception):
    """This drainer must leave the op queued, untouched: it is not this
    process's to send, and nothing was learned about the op or its run.

    Raised while resolving the op's client, before anything is sent. The drain
    holds the op -- a coalesced batch whole -- with no attempt counted and
    nothing dead-lettered, and parks its run for the rest of the pass: not a
    stall, so no back-off follows. The seam for #2041's `CredentialNotHere`
    (a write queued under a credential this process does not hold)."""


class OpInProgress(OpHeldHere):
    """A long op made progress and is not finished: leave it queued, charge no
    attempt, and let the other lanes go (plan item (g): a multipart upload
    moves one slice of parts per pass, then waits for the server's verifier).
    The op persisted its own progress before raising.

    ``retry_after`` None: come back on the very next pass (more parts to
    send). A number: its lane waits at least that long (the server is still
    verifying), through the same per-lane backoff a stall uses, with nothing
    counted against the op's failure budget."""

    def __init__(
        self, message: str, *, retry_after: float | None = None, wake_by: float | None = None
    ) -> None:
        super().__init__(message)
        self.retry_after = retry_after
        #: Look again within this many seconds, however far the lane's
        #: backoff has grown (`LaneStall.wake_by`).
        self.wake_by = wake_by


@dataclass
class LaneStall:
    """Why one run's lane stopped for the rest of a pass (plan 1.6)."""

    error: str
    #: The server's ``Retry-After`` on that failure, when it named one.
    retry_after: float | None = None
    #: The failure's HTTP status; None when no answer came at all (a network
    #: failure or a timeout), which a caller with a budget may stop on.
    status: int | None = None
    #: Not a failure at all: the run is HELD -- its op is not this drainer's
    #: to send (#2035), or its close waits for its writes in another queue.
    #: Nothing was sent, so this says nothing about the server (#2041 round 5:
    #: the takeover barrier read a held run as "unreachable" and stopped).
    held: bool = False
    #: Seconds after which the run must be looked at again whatever its
    #: backoff says (a close hold that expires then), or None.
    wake_by: float | None = None


@dataclass
class DrainReport:
    delivered: int = 0
    dead_lettered: int = 0
    remaining: int = 0
    auth_blocked: bool = False
    #: The refusal that set `auth_blocked`: its HTTP status and message (a 401,
    #: or a 403 that may name a missing SCOPE rather than the credential -- see
    #: `key_refusal.credential_refused`), and the refused op's pinned context,
    #: since a machine-wide pass can stop on ANOTHER context's credential.
    auth_status: int | None = None
    auth_message: str | None = None
    auth_context: dict | None = None
    stopped_transient: bool = False
    #: Ops left queued behind an earlier upload of their run still waiting for
    #: its credential scan (see `Journal.waiting_positions`).
    held_back: int = 0
    #: Ops left queued because this drainer holds no credential matching the
    #: one that queued them (#2035); another process with it delivers them.
    credential_held: int = 0
    #: Stamped ops whose OWN credential the API refused this pass. Set aside
    #: with every other op of that credential; the pass goes on (#2041 review).
    credential_refused: int = 0
    #: True only when a refusal STOPPED the pass: an unstamped op (queued by an
    #: older release), whose credential nothing can tell apart from the rest.
    queue_auth_stopped: bool = False
    #: Every refusal this pass: ``{"status", "message", "context",
    #: "fingerprint"}`` (the refused key). ``auth_*`` above hold the first.
    auth_refusals: list[dict] = field(default_factory=list)
    #: Why ops were kept (`credential_held`), each reason once, for the CLI.
    held_reasons: list[str] = field(default_factory=list)
    #: Of `credential_held`, ops no credential on this machine will match as
    #: things stand (an unknown or another account: `CredentialNotHere.permanent`),
    #: the ones `probe outbox discard --held` drops.
    permanently_held: int = 0
    errors: list[str] = field(default_factory=list)
    #: The server's ``Retry-After`` on the failure that stopped this pass, in
    #: seconds, when it named one. Every retry loop waits at least this long.
    retry_after: float | None = None
    #: The pass stopped because the CALLER's deadline ran out (see
    #: `transport.deadline_scope`), not because an op failed.
    deadline_reached: bool = False
    #: Another drain held the lock for the whole of ``lock_timeout``: this pass
    #: attempted nothing.
    lock_busy: bool = False
    #: Per-run lanes (plan 1.6). A run whose head op failed transiently, by
    #: ``run_ref`` (None: ops that name no run): the op is parked in place, the
    #: rest of that run waits, and every other run's ops were still attempted.
    stalled_runs: dict[str | None, LaneStall] = field(default_factory=dict)
    #: Runs that had an op delivered or dead-lettered this pass: their backoff,
    #: if any, starts over.
    progressed_runs: set = field(default_factory=set)
    #: The pass stopped for EVERY run because the server could not be reached
    #: at all (a connect failure) or stopped answering (a second response lost
    #: after sending in one pass): trying each run's head op in turn would only
    #: wait out one timeout per run.
    unreachable: bool = False
    #: Every run with an op in this pass's scan (None: not known, e.g. the pass
    #: never scanned), so a caller's backoff can forget the ones that left.
    queued_runs: set | None = None
    #: Ops held because this release does not know their kind (plan 1.11).
    unknown_kinds: int = 0
    #: Long ops (multipart uploads, plan (g)) that made progress this pass and
    #: stay queued for the next (`OpInProgress`).
    in_progress: int = 0
    #: Ops delivered inside a multi-op POST (plan 1.2); counted in
    #: ``delivered`` too.
    coalesced: int = 0
    #: Run closes held because writes of the same run, queued earlier under
    #: another credential, sit in another queue (#2041 round 3).
    close_held: int = 0
    #: ``{run_ref, op_id, error, status}`` for each op this pass dead-lettered,
    #: kept in ``dead_letters.json`` (`Journal.recent_dead_letters`) so a
    #: training process can say so while it runs (plan 1.7).
    dead_letter_records: list = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return self.dead_lettered == 0 and self.remaining == 0 and not self.auth_blocked

    @property
    def auth_stopped(self) -> bool:
        """A refusal stopped the pass, rather than setting one credential's
        writes aside. A report that names no set-aside credential reads as
        stopped, as every report did before (#2041 review)."""
        return self.queue_auth_stopped or (self.auth_blocked and not self.credential_refused)


def _meta_of(op: dict) -> tuple[int, str | None]:
    """What a status recount needs from one op: (size_bytes, enqueued_at)."""
    return int((op.get("upload") or {}).get("size_bytes") or 0), op.get("enqueued_at")


def op_meta(ops: list[tuple[Path, dict]]) -> dict[str, tuple[int, str | None]]:
    """name -> (size_bytes, enqueued_at) for ops already parsed, so a status
    recount under the append lock need not parse them again."""
    out: dict[str, tuple[int, str | None]] = {}
    for path, op in ops:
        try:
            out[path.name] = _meta_of(op)
        except AttributeError:  # not an object: let the recount skip it
            out[path.name] = (0, None)
    return out


def auth_blocked_since(status: dict | None, fingerprints=None) -> str | None:
    """When delivery was last refused a credential (401/403), from a
    status.json dict, or None. Either the queue-wide block (`auth_blocked_since`:
    writes of a release that stamps no credential) or, since #2041, a
    credential the drain set aside (`refused_fingerprints`, fingerprint ->
    when) -- which is how every write a current release queues is refused, so
    the queue-wide field alone no longer shows a revoked token. ``fingerprints``
    limits the second to those credentials (a client's own). Both stamps are
    rewritten at each refusal (the credential cooldown counts from the latest),
    so this is the LATEST refusal, not the first."""
    if not isinstance(status, dict):
        return None
    blocked = status.get("auth_blocked_since") or None
    refused = status.get("refused_fingerprints")
    if not blocked and isinstance(refused, dict):
        stamps = sorted(
            str(at)
            for fp, at in refused.items()
            if at and (fingerprints is None or fp in fingerprints)
        )
        blocked = stamps[0] if stamps else None
    return blocked


def _credential_queue_dirs(root: Path) -> list[Path]:
    """The credential queues (#2035) under an outbox root, in name order.
    Only 16-hex names: a queue being pruned is renamed away first."""
    try:
        entries = sorted((root / CREDENTIAL_NAMESPACE).iterdir())
    except OSError:
        return []
    return [p for p in entries if re.fullmatch(r"[0-9a-f]{16}", p.name) and p.is_dir()]


def _queue_is_empty(path: Path) -> bool:
    """Nothing queued, dead-lettered, waiting or staged in the queue at
    ``path``, and no receipt namespace under it."""
    if (path / DELIVERY_NAMESPACE).exists() or (path / ".recover").exists():
        return False
    # `multipart/*` (plan (g)): a queue holding only an upload in progress --
    # its op, its staged bytes -- is not empty, and must never be pruned.
    for sub in ("ops", "failed", "waiting", "blobs", "multipart/ops", "multipart/staged", "multipart/failed"):
        try:
            if os.listdir(path / sub):
                return False
        except FileNotFoundError:
            continue
        except OSError:
            return False
    return True


#: A credential queue left empty this long is removed (`prune_credential_queues`).
CREDENTIAL_QUEUE_IDLE_SECONDS = 3600.0
_last_prune = float("-inf")


def prune_credential_queues(root: Path, *, idle_seconds: float = CREDENTIAL_QUEUE_IDLE_SECONDS) -> int:
    """Remove credential queues (#2035) that are empty, idle for
    ``idle_seconds`` and whose drain lock and worker lease are free: one
    folder per token ever used piled up (#2041 round 3: 420 of them made every
    `finish()` 15x slower). A writer that comes back recreates its folder on
    its next write (`Journal._append` re-asserts a missing layout). The folder
    is renamed away under its append lock before it is deleted, so a write
    racing the prune lands in the recreated folder, never in the doomed one.
    At most once per process per 10 minutes. Returns how many went."""
    global _last_prune
    if time.monotonic() - _last_prune < 600.0:
        return 0
    _last_prune = time.monotonic()
    removed = 0
    try:
        leftovers = [p for p in (root / CREDENTIAL_NAMESPACE).iterdir() if p.name.startswith(".pruned-")]
    except OSError:
        leftovers = []
    for path in leftovers:  # a prune that died between the rename and the delete
        shutil.rmtree(path, ignore_errors=True)
    for path in _credential_queue_dirs(root):
        try:
            newest = max(p.stat().st_mtime for p in (path, *path.iterdir()))
        except (OSError, ValueError):
            continue
        if time.time() - newest < idle_seconds or not _queue_is_empty(path):
            continue
        handles = []
        try:
            for name in (".drain.lock", ".worker.lock"):
                handle = (path / name).open("a+")
                handles.append(handle)
                oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
            trash = path.parent / f".pruned-{path.name}-{os.getpid()}-{time.time_ns()}"
            with file_lock(path / ".append.lock"):
                if not _queue_is_empty(path):
                    continue
                os.replace(path, trash)
            shutil.rmtree(trash, ignore_errors=True)
            removed += 1
        except (BlockingIOError, OSError):
            continue
        finally:
            for handle in handles:
                handle.close()
    return removed


class RunOps:
    """One run's ops that may hold its close, counted from directory LISTINGS.

    `Run.finish()` asks "what of mine is still queued / dead-lettered?" after
    every pass of its deadline loop. Answering with ``journal.pending()``
    parsed the WHOLE machine-wide queue each time -- every run's ops, every
    0.25 s -- which at a 20k-op backlog is most of the loop's cost (plan 1.9
    side note). Op files are immutable in the two fields asked about
    (``run_ref`` and ``blocking``) while they sit in one directory, so each
    ``(directory, name)`` is parsed once and remembered; later calls cost one
    ``listdir``. ``blocking`` flips only on the move INTO ``failed/``, which is
    a new ``(directory, name)`` key, parsed fresh.

    Same selection as `Run._queued_ops`: ``run_ref`` matches and ``blocking``
    is not False (a best-effort diagnostic never holds a close).
    """

    def __init__(
        self,
        journal: "Journal",
        run_ref: str,
        *,
        blocking_only: bool = True,
        queues: "list[Journal] | None" = None,
        min_epoch: int | None = None,
    ):
        self._journal = journal
        self._run_ref = run_ref
        #: False counts every op of the run, blocking or not: "is anything of
        #: this run still queued" (plan 1.5's direct send), not "what holds its
        #: close".
        self._blocking_only = blocking_only
        #: The queues counted: this journal alone, or (`Journal.run_ops_elsewhere`)
        #: the other queues of its outbox.
        self._queues = [journal] if queues is None else list(queues)
        #: Leave out ops stamped with an older write epoch: the server refuses
        #: them as a superseded attempt's, so nothing waits for them.
        self._min_epoch = min_epoch
        self._mine: dict[tuple[str, str], bool] = {}

    def _scan(self, directory: Path) -> list[Path]:
        try:
            names = sorted(n for n in os.listdir(directory) if n.endswith(".json"))
        except FileNotFoundError:
            return []
        # Forget files that left this directory, so a long-lived handle does
        # not remember every op the run ever queued (review of #2054).
        present = set(names)
        where = str(directory)
        for key in [k for k in self._mine if k[0] == where and k[1] not in present]:
            del self._mine[key]
        out: list[Path] = []
        for name in names:
            key = (where, name)
            mine = self._mine.get(key)
            if mine is None:
                try:
                    op = json.loads((directory / name).read_text())
                except FileNotFoundError:
                    continue  # delivered (or moved) between the listing and the read
                except (OSError, ValueError):
                    continue  # corrupt: quarantine's business; not cached, re-read later
                mine = bool(
                    isinstance(op, dict)
                    and op.get("run_ref") == self._run_ref
                    and (op.get("blocking", True) or not self._blocking_only)
                    and not self._older_attempts(op)
                )
                self._mine[key] = mine
            if mine:
                out.append(directory / name)
        return out

    def _older_attempts(self, op: dict) -> bool:
        if self._min_epoch is None:
            return False
        epoch = _write_epoch_of(op)
        return epoch is not None and epoch < self._min_epoch

    def pending(self) -> list[Path]:
        return [path for queue in self._queues for path in self._scan(queue.ops_dir)]

    def failed(self) -> list[Path]:
        return [path for queue in self._queues for path in self._scan(queue.failed_dir)]


class Journal:
    def __init__(
        self,
        directory: str | Path | None = None,
        *,
        context: dict | None = None,
        attribution: str = "ambient",
    ):
        self.dir = Path(directory).expanduser() if directory else default_dir()
        self.ops_dir = self.dir / "ops"
        self.failed_dir = self.dir / "failed"
        self.blobs_dir = self.dir / "blobs"
        #: Uploads queued before their credential scan (see `promote_waiting`).
        #: No released version before this one reads it, so an older drainer
        #: sharing this journal can never pick up bytes that were not scanned.
        self.waiting_dir = self.dir / "waiting"
        #: Held by whoever is promoting (a promote-only worker, or a drain's
        #: promotion pass), so a kick does not fork another promoter meanwhile;
        #: separate from the drain lease an OLDER worker may hold.
        self.promote_lease = self.dir / ".promote.lock"
        self.status_file = self.dir / "status.json"
        self.paused_file = self.dir / "paused"
        self.append_lock = self.dir / ".append.lock"
        self.drain_lock = self.dir / ".drain.lock"
        #: Present while a takeover barrier (SDK reliability 2.3) holds some
        #: queued status ops aside in `failed/`: the cheap test that tells every
        #: drain pass and every new client whether to look for abandoned holds.
        self.holds_marker = self.dir / "takeover-holds"
        self.producers_dir = self.dir / "producers"
        #: default {"name", "base_url"} pin stamped onto appended ops.
        self.context = context
        if attribution not in ("ambient", "backfill"):
            raise ValueError("invalid outbox attribution")
        self.attribution = attribution
        self.receipt_enabled = self.dir.name == DELIVERY_NAMESPACE
        self.intents_dir = self.dir / "intents"
        self.receipts_dir = self.dir / "receipts"
        self.receipt_index = self.dir / "receipts-v1.sqlite3"
        self.correlation_locks = self.dir / "correlation-stripes"
        self.recovery_file = self.dir / ".recover"
        #: parity F4: set via register_producer; None = unstamped ops.
        self._producer_id: str | None = None
        self._producer_role: str | None = None
        #: Backpressure state for `_append_headroom`. `_pending_estimate` is
        #: the pending count this process last saw in status.json: read on the
        #: first append, then taken from every status write the append already
        #: makes (so another process's drain lowers it at no extra cost), and
        #: re-read before any refusal. A drain pass rewrites status.json from a
        #: real count only when the pass ENDS, so a write that would still be
        #: refused also counts the queue directory itself, at most once per
        #: `_RECOUNT_EVERY_SECONDS`.
        #:
        #: It used to be read ONCE and only ever incremented: the detached
        #: worker delivers in another process, so nothing in this one lowered
        #: it, and a long-lived process refused every write after its
        #: MAX_PENDING_OPS-th append while the queue sat empty (plan 0.1: live,
        #: cap 150, 150 of 450 writes arrived).
        self._pending_estimate: int | None = None
        self._recounted_at = float("-inf")
        self._appends_since_statvfs = _STATVFS_EVERY
        self._last_free_ok = True
        self._headroom_warned = False
        #: The queue's sequence high-water mark, taken once per Journal before
        #: its first sequence (see `_op_filename`); None until then, and again
        #: once it has been applied.
        self._seq_floor: int | None = None
        self._seq_recovered = False
        #: The sibling namespace's pending count, re-read with the free-space
        #: sample rather than on every append (plan 1.3); `None` = not yet read.
        self._sibling_pending: int | None = None
        self._appends_since_sibling = 0
        #: This queue's op-count ceiling: None is `MAX_PENDING_OPS`, 0 is none.
        #: An OFFLINE run's queue (plan 2.12) sets 0: nothing drains it until
        #: `probe sync`, so a ceiling meant to catch a stalled drainer would
        #: only drop every point after the 500,000th, and the close with them.
        #: The free-space floor still applies, so the disk stays protected.
        self.op_ceiling: int | None = None

    @classmethod
    def for_receipts(cls, directory=None, *, context=None, attribution="backfill") -> Journal:
        """New operations live outside every pre-receipt worker's ops directory."""
        base = Path(directory).expanduser() if directory else default_dir()
        if base.name != DELIVERY_NAMESPACE:
            base = base / DELIVERY_NAMESPACE
        return cls(base, context=context, attribution=attribution)

    @classmethod
    def for_credential(
        cls, directory=None, fingerprint: str = "", *, context=None, attribution="ambient"
    ) -> Journal:
        """The queue of one credential (see `CREDENTIAL_NAMESPACE`)."""
        base = Path(directory).expanduser() if directory else default_dir()
        if not fingerprint or not re.fullmatch(r"[0-9a-f]{16}", fingerprint):
            raise ValueError("a credential queue needs a 16-hex fingerprint")
        return cls(base / CREDENTIAL_NAMESPACE / fingerprint, context=context, attribution=attribution)

    @property
    def outbox_root(self) -> Path:
        """The outbox directory this queue lives in (itself, for the root)."""
        path = self.dir
        if path.name == DELIVERY_NAMESPACE:
            path = path.parent
        if path.parent.name == CREDENTIAL_NAMESPACE:
            path = path.parent.parent
        return path

    def namespaces(self) -> list[Journal]:
        """This queue and the queues under it, each once: the root, its receipt
        namespace, and every credential queue with its own receipt namespace."""
        if self.receipt_enabled:
            return [self]
        out = [self]
        child = self.for_receipts(self.dir, context=self.context, attribution=self.attribution)
        if child.dir.exists():
            out.append(child)
        if self.dir.parent.name != CREDENTIAL_NAMESPACE:
            for path in _credential_queue_dirs(self.dir):
                queue = Journal(path, context=self.context, attribution=self.attribution)
                out.append(queue)
                receipts = self.for_receipts(path, context=self.context, attribution=self.attribution)
                if receipts.dir.exists():
                    out.append(receipts)
        return out

    @staticmethod
    def _correlation_key(correlation: str) -> str:
        if not isinstance(correlation, str) or not correlation or len(correlation) > 4096:
            raise ValueError("correlation must be a nonempty string of at most 4096 characters")
        return hashlib.sha256(correlation.encode()).hexdigest()

    @staticmethod
    def _request_digest(request: dict) -> str:
        """The request's identity for correlation replays. Leaves out the
        credential stamp (#2035): the same request re-queued after a re-login
        is the same request, and must replay rather than raise.

        So a correlation names ONE request whoever queues it: the same
        correlation, anchor and body queued under another credential (same
        team -- another team's anchor id differs) replays the first op, which
        goes out with the credential that queued it first. Callers mint
        correlations per request (backfill's are content-addressed), so two
        people never share one by accident (#2041 re-review, decided)."""
        context = request.get("context")
        if isinstance(context, dict) and "principal" in context:
            request = {**request, "context": {k: v for k, v in context.items() if k != "principal"}}
        return hashlib.sha256(
            json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        ).hexdigest()

    @staticmethod
    def _read_record(path: Path) -> dict | None:
        try:
            data = json.loads(path.read_text())
        except FileNotFoundError:
            return None
        if not isinstance(data, dict) or data.get("schema") != DELIVERY_SCHEMA:
            raise ValueError(f"invalid delivery record: {path.name}")
        return data

    def receipt(self, correlation: str) -> dict | None:
        if not self.receipt_enabled:
            return self.for_receipts(self.dir).receipt(correlation)
        found = self._own_receipt(correlation)
        if found is None and self.dir.parent.parent.name == CREDENTIAL_NAMESPACE:
            # A credential queue's receipts start empty; what was delivered
            # before the stamp (#2035) is recorded in the root's. Read-only.
            legacy = Journal(self.outbox_root / DELIVERY_NAMESPACE)
            if legacy.dir.exists():
                return legacy._own_receipt(correlation)
        return found

    def _own_receipt(self, correlation: str) -> dict | None:
        key = self._correlation_key(correlation)
        # JSON first is essential: compaction commits the index before unlink.
        # A reader that misses the file therefore cannot miss the committed row.
        legacy = self._read_record(self.receipts_dir / f"{key}.json")
        if legacy is not None:
            return legacy
        if not self.receipt_index.exists():
            return None
        with closing(sqlite3.connect(self.receipt_index.resolve().as_uri() + "?mode=ro", uri=True)) as conn:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version == 0 and not conn.execute("SELECT 1 FROM sqlite_master LIMIT 1").fetchone():
                return None  # interrupted before the first schema transaction
            if version != RECEIPT_INDEX_VERSION:
                raise ValueError("unsupported terminal receipt index version")
            row = conn.execute("SELECT payload FROM receipts WHERE key=?", (key,)).fetchone()
        result = json.loads(row[0]) if row else None
        if result is not None and (result.get("schema") != DELIVERY_SCHEMA
                                   or result.get("correlation") != correlation):
            raise ValueError("invalid indexed delivery receipt")
        return result

    @contextmanager
    def _correlation_lock(self, key: str, *, blocking: bool = True):
        """Stable stripes fence both writers and legacy-lock retirement.

        The 256 stripe inodes are NEVER unlinked. A waiter acquires its stripe
        BEFORE opening any legacy per-key inode; cleanup holds that same stripe.
        Thus no new writer can retain a deleted lock inode while another writer
        opens a replacement. Existing active legacy locks are retained on a
        nonblocking cleanup attempt. Pre-index delivery-v1 binaries must be
        upgraded before compaction; production pre-receipt workers never enter
        this namespace at all.
        """
        self.correlation_locks.mkdir(parents=True, exist_ok=True, mode=0o700)
        flags = oscompat.LOCK_EX | (0 if blocking else oscompat.LOCK_NB)
        with (self.correlation_locks / f"{key[:2]}.lock").open("a+") as stripe:
            oscompat.flock(stripe, flags)
            legacy = None
            try:
                try:
                    legacy = (self.dir / "correlations" / f"{key}.lock").open("r+")
                except FileNotFoundError:
                    pass
                if legacy is not None:
                    oscompat.flock(legacy, flags)
                yield
            finally:
                if legacy is not None:
                    legacy.close()
                oscompat.flock(stripe, oscompat.LOCK_UN)

    @staticmethod
    def _commit_receipt_index(conn) -> None:
        """The terminal durability boundary; operation removal happens later."""
        conn.commit()

    def _index_receipts(self, receipts: list[dict], *, timeout: float = 5.0) -> None:
        """Commit immutable identities in one indexed, FULL-synchronous transaction."""
        self._receipt_dirs()
        # Reserve a private inode before sqlite opens it (its default mode is 644).
        descriptor = os.open(self.receipt_index, os.O_CREAT | os.O_RDWR, 0o600)
        os.close(descriptor)
        with closing(sqlite3.connect(self.receipt_index, timeout=timeout)) as conn, conn:
            conn.execute("PRAGMA synchronous=FULL")
            conn.execute("BEGIN IMMEDIATE")
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, RECEIPT_INDEX_VERSION):
                raise ValueError("unsupported terminal receipt index version")
            conn.execute("CREATE TABLE IF NOT EXISTS receipts (key TEXT PRIMARY KEY, "
                         "payload TEXT NOT NULL, cleanup INTEGER NOT NULL DEFAULT 1) WITHOUT ROWID")
            conn.execute("CREATE INDEX IF NOT EXISTS receipt_cleanup ON receipts(cleanup) WHERE cleanup=1")
            conn.execute(f"PRAGMA user_version={RECEIPT_INDEX_VERSION}")
            for receipt in receipts:
                if (receipt.get("schema") != DELIVERY_SCHEMA or receipt.get("state") != "delivered"
                        or receipt.get("status") != "complete" or not receipt.get("artifact_id")
                        or not receipt.get("request_digest")):
                    raise ValueError("cannot compact an unverified terminal receipt")
                key = self._correlation_key(receipt["correlation"])
                payload = json.dumps(receipt, separators=(",", ":"), sort_keys=True)
                previous = conn.execute("SELECT payload FROM receipts WHERE key=?", (key,)).fetchone()
                if previous and json.loads(previous[0]) != receipt:
                    raise ValueError("terminal receipt identity is immutable")
                conn.execute("INSERT OR IGNORE INTO receipts(key,payload) VALUES (?,?)", (key, payload))
                conn.execute("UPDATE receipts SET cleanup=1 WHERE key=?", (key,))
            self._commit_receipt_index(conn)
        fsync_directory(self.dir)

    def compact_receipts(self, *, max_records: int = RECEIPT_COMPACTION_BATCH,
                         max_seconds: float = 1.0) -> dict:
        """Bounded explicit checkpoint; preserves all terminal identities forever.

        Import legacy JSON into the index before deleting any copy. Cleanup is
        itself indexed, so a crash after the index commit or JSON unlink resumes
        without scanning historical identities. This does not VACUUM or erase
        receipts. One filesystem operation/SQLite commit may overrun the time
        budget; lock waits are nonblocking and DB admission uses that budget.
        """
        if not self.receipt_enabled:
            return self.for_receipts(self.dir).compact_receipts(max_records=max_records, max_seconds=max_seconds)
        if not 1 <= max_records <= 4096 or not 0 < max_seconds <= 10:
            raise ValueError("receipt compaction requires 1..4096 records and 0 < seconds <= 10")
        deadline = time.monotonic() + max_seconds
        report = {"indexed": 0, "json_removed": 0, "locks_removed": 0,
                  "compacted": 0, "deferred": 0, "remaining": False}
        receipts = []
        if self.receipts_dir.exists():
            with os.scandir(self.receipts_dir) as entries:
                for entry in entries:
                    if len(receipts) >= max_records or time.monotonic() >= deadline:
                        break
                    if entry.name.endswith(".json") and entry.is_file(follow_symlinks=False):
                        receipt = self._read_record(Path(entry.path))
                        if receipt is not None:
                            if entry.name != self._correlation_key(receipt["correlation"]) + ".json":
                                raise ValueError("legacy receipt name differs from correlation")
                            receipts.append(receipt)
        if receipts:
            self._index_receipts(receipts, timeout=max(0.001, deadline - time.monotonic()))
            report["indexed"] = len(receipts)
        if not self.receipt_index.exists():
            return report
        with closing(sqlite3.connect(self.receipt_index, timeout=max(0.001, deadline - time.monotonic()))) as conn:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            if version == 0 and not conn.execute("SELECT 1 FROM sqlite_master LIMIT 1").fetchone():
                return report
            if version != RECEIPT_INDEX_VERSION:
                raise ValueError("unsupported terminal receipt index version")
            keys = conn.execute("SELECT key FROM receipts WHERE cleanup=1 LIMIT ?", (max_records,)).fetchall()
            cleaned = []
            for (key,) in keys:
                if time.monotonic() >= deadline:
                    break
                try:
                    with self._correlation_lock(key, blocking=False):
                        for directory, suffix, field in (
                            (self.receipts_dir, ".json", "json_removed"),
                            (self.dir / "correlations", ".lock", "locks_removed"),
                        ):
                            path = directory / f"{key}{suffix}"
                            if path.exists():
                                path.unlink()
                                fsync_directory(directory)
                                report[field] += 1
                        cleaned.append((key,))
                except BlockingIOError:
                    report["deferred"] += 1
            if cleaned:
                conn.executemany("UPDATE receipts SET cleanup=0 WHERE key=?", cleaned)
                conn.commit()
            report["compacted"] = len(cleaned)
            report["remaining"] = bool(conn.execute("SELECT 1 FROM receipts WHERE cleanup=1 LIMIT 1").fetchone())
        if self.receipts_dir.exists():
            with os.scandir(self.receipts_dir) as entries:
                report["remaining"] |= next(entries, None) is not None
        return report

    def delivery_state(self, correlation: str) -> dict:
        if not self.receipt_enabled:
            return self.for_receipts(self.dir).delivery_state(correlation)
        receipt = self.receipt(correlation)
        if receipt is not None:
            return receipt
        intent = self._read_record(self.intents_dir / f"{self._correlation_key(correlation)}.json")
        if intent is None:
            return {"state": "unknown", "correlation": correlation}
        op = intent["op"]
        filename = op["queue_filename"]
        failed = self.failed_dir / filename
        discarded = self.dir / "discarded" / filename
        state = (
            "discarded"
            if discarded.exists()
            else (
                "failed"
                if failed.exists()
                else ("queued" if (self.ops_dir / filename).exists() else "pending")
            )
        )
        error = None
        if failed.exists():
            error = json.loads(failed.read_text()).get("last_error")
        return {
            "state": state,
            "correlation": correlation,
            "op_id": op["op_id"],
            "blob": (op.get("upload") or {}).get("blob"),
            "size_bytes": (op.get("upload") or {}).get("size_bytes"),
            "staged": bool((op.get("upload") or {}).get("staged")),
            "error": error,
        }

    def _receipt_dirs(self) -> None:
        self._ensure()
        for path in (self.intents_dir, self.receipts_dir, self.dir / "correlations"):
            path.mkdir(mode=0o700, parents=True, exist_ok=True)

    def _replay_correlation(self, correlation: str, request: dict) -> dict | None:
        digest = self._request_digest(request)
        done = self.receipt(correlation)
        key = self._correlation_key(correlation)
        intent = self._read_record(self.intents_dir / f"{key}.json")
        previous = done or intent
        if previous is None:
            return None
        if previous["request_digest"] != digest:
            raise ValueError("correlation already belongs to a different immutable request")
        if done is not None:
            return done
        op = intent["op"]
        filename = op["queue_filename"]
        if not any(
            (directory / filename).exists()
            for directory in (
                self.ops_dir,
                self.failed_dir,
                self.dir / "discarded",
            )
        ):
            # The intent committed but the operation did not. Its staged bytes,
            # not the current source file, are the only valid retry input.
            blob = self.blob_path(op)
            if op["kind"] == "upload" and (blob is None or not blob.is_file()):
                raise OSError("receipt upload's immutable staged bytes are missing")
            self._restore_intent_op(op)
        return self.delivery_state(correlation)

    def _restore_intent_op(self, op: dict) -> None:
        # This request was admitted before the crash. Restoring its small queue
        # record must not compete for admission with new snapshots: the existing
        # bytes may be exactly what draining needs to release under disk pressure.
        with file_lock(self.append_lock):
            path = self.ops_dir / op["queue_filename"]
            write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
            self._write_status_locked()

    def _publish_receipt_op(self, correlation: str, request: dict, op: dict, publish=None) -> dict:
        key = self._correlation_key(correlation)
        op.update(
            {
                "schema": DELIVERY_SCHEMA,
                "correlation": correlation,
                "request_digest": self._request_digest(request),
            }
        )

        def before_write():
            if publish is not None:
                publish()
            if "queue_filename" not in op:
                op["queue_filename"] = self._op_filename(op["op_id"])
            # Marker precedes intent: restart must see even an append interrupted
            # before status.json or the op file exists.
            write_text_atomic(self.recovery_file, op["op_id"] + "\n", mode=0o600)
            write_text_atomic(
                self.intents_dir / f"{key}.json",
                json.dumps(
                    {
                        "schema": DELIVERY_SCHEMA,
                        "correlation": correlation,
                        "request_digest": op["request_digest"],
                        "op": op,
                    }
                )
                + "\n",
                mode=0o600,
            )

        self._append(op, before_write=before_write)
        return self.delivery_state(correlation)

    def _receipt_upload(
        self, *, correlation: str, expected_content_hash: str | None, **fields
    ) -> dict:
        self._receipt_dirs()
        key = self._correlation_key(correlation)
        fields["src_path"] = os.path.abspath(fields["src_path"])
        request = {
            "kind": "upload",
            "fields": fields,
            "context": self.context,
            "attribution": self.attribution,
            "expected_content_hash": expected_content_hash,
        }
        with self._correlation_lock(key):
            existing = self._replay_correlation(correlation, request)
            if existing is not None:
                return existing
            # A retry refers to the admitted immutable snapshot/receipt, not
            # today's source. Inspect only a genuinely new upload request.
            check_upload(fields["src_path"])
            self._refresh_pending_estimate()
            refusal = self._append_headroom() or self._staging_headroom(fields["src_path"])
            if refusal:
                raise OutboxFull(refusal)
            op = self._base_op("upload", fields.get("run_ref"))
            staging = self.blobs_dir / f".staging-{op['op_id']}"
            source = Path(fields["src_path"])
            try:
                before = source.stat()
                if not source.is_file():
                    raise ValueError("receipt upload source is not a regular file")
                snapshot_file(source, staging)
                digest, size = fingerprint(str(staging))
                after = source.stat()

                def observed(stat):
                    return (
                        stat.st_dev,
                        stat.st_ino,
                        stat.st_size,
                        stat.st_mtime_ns,
                        stat.st_ctime_ns,
                    )

                if observed(before) != observed(after):
                    raise ValueError("source changed while its snapshot was staged")
                if expected_content_hash is not None and expected_content_hash not in (
                    digest,
                    _source_digest(fields["src_path"]),
                ):
                    # The caller's hash describes the file it censused, and the
                    # snapshot is redacted, so the two legitimately differ. A
                    # backfill whose approved file carried a credential used to
                    # fail delivery permanently here; matching EITHER keeps the
                    # tamper check while letting a redacted upload through.
                    raise ValueError("staged bytes do not match expected_content_hash")
                upload = {k: v for k, v in fields.items() if k != "run_ref"}
                upload.update(
                    {"blob": digest, "size_bytes": size, "staged": True, "unstaged_reason": None}
                )
                op["upload"] = upload

                def publish():
                    final = self.blobs_dir / digest
                    if final.exists():
                        staging.unlink(missing_ok=True)
                    else:
                        os.replace(staging, final)
                    fsync_directory(self.blobs_dir)

                return self._publish_receipt_op(correlation, request, op, publish)
            finally:
                staging.unlink(missing_ok=True)

    def recover_intents(self) -> int:
        """Repair interrupted local appends without rereading a live source."""
        if not self.receipt_enabled or not self.intents_dir.exists():
            return 0
        try:
            generation = self.recovery_file.read_text()
        except FileNotFoundError:
            generation = None
        recovered = 0
        for path in sorted(self.intents_dir.glob("*.json")):
            intent = self._read_record(path)
            if intent is None:
                continue
            correlation = intent["correlation"]
            with self._correlation_lock(self._correlation_key(correlation)):
                if self.receipt(correlation) is not None:
                    path.unlink(missing_ok=True)
                    continue
                op = intent["op"]
                filename = op["queue_filename"]
                if not any(
                    (directory / filename).exists()
                    for directory in (
                        self.ops_dir,
                        self.failed_dir,
                        self.dir / "discarded",
                    )
                ):
                    self._restore_intent_op(op)
                    recovered += 1
        with file_lock(self.append_lock):
            try:
                current_generation = self.recovery_file.read_text()
            except FileNotFoundError:
                current_generation = None
            # A newer append may have died after our directory snapshot. Its
            # marker belongs to the next pass, even when status still says zero.
            if current_generation == generation:
                self.recovery_file.unlink(missing_ok=True)
                fsync_directory(self.dir)
        return recovered

    def _save_delivery_receipt(self, op: dict, result: Any) -> None:
        if not op.get("correlation"):
            return
        if not isinstance(result, dict) and hasattr(result, "json"):
            result = result.json()
        if (
            not isinstance(result, dict)
            or not result.get("id")
            or result.get("status") != "complete"
        ):
            raise errors.TransportError("delivery returned no complete artifact identity")
        upload = op.get("upload") or {}
        body = op.get("body") or {}
        reference = op["kind"] == "http"
        if bool(result.get("is_reference")) != reference or not result.get("uri"):
            raise errors.TransportError("delivery returned no readable artifact or reference URI")
        if result.get("name") != (upload.get("name") or body.get("name")):
            raise errors.TransportError("delivered artifact name differs from requested name")
        if reference and result["uri"] != body["uri"]:
            raise errors.TransportError("delivered reference URI differs from requested URI")
        if upload and (
            result.get("content_hash") != upload["blob"]
            or result.get("size_bytes") != upload["size_bytes"]
        ):
            raise errors.TransportError(
                "delivered artifact digest or size differs from staged bytes"
            )
        for attribute in ("content_hash", "size_bytes"):
            if (
                reference
                and body.get(attribute) is not None
                and result.get(attribute) != body[attribute]
            ):
                raise errors.TransportError(
                    f"delivered reference {attribute} differs from requested value"
                )
        correlation = op["correlation"]
        receipt = {
            "schema": DELIVERY_SCHEMA,
            "correlation": correlation,
            "op_id": op["op_id"],
            "request_digest": op["request_digest"],
            "state": "delivered",
            "status": "complete",
            "artifact_id": str(result["id"]),
            "content_hash": result.get("content_hash"),
            "size_bytes": result.get("size_bytes"),
            "is_reference": reference,
            "blob": result.get("content_hash") if not reference else None,
            "staged": not reference,
            "mode": "reference" if reference else "upload",
            "readable": not reference,
            "uri": result["uri"],
            "name": result.get("name") or upload.get("name") or body.get("name"),
            "anchor": upload.get("anchor") or op.get("path", "").split("/")[2].removesuffix("s"),
            "anchor_id": upload.get("anchor_id") or op.get("path", "").split("/")[3],
            "delivered_at": now_iso(),
        }
        key = self._correlation_key(correlation)
        with self._correlation_lock(key):
            existing = self.receipt(correlation)
            if existing is None:
                self._index_receipts([receipt])
            elif existing["request_digest"] != op["request_digest"]:
                raise ValueError("terminal receipt belongs to a different request")
            (self.intents_dir / f"{key}.json").unlink(missing_ok=True)
            fsync_directory(self.intents_dir)

    # -- layout -------------------------------------------------------------
    def usable(self) -> str | None:
        """None when this queue can take appends, else why it cannot (plan 1.5).

        Checked once, when a `Client` builds its journal, WITHOUT creating the
        queue (a read-only command must not leave an outbox behind): a file is
        created and `flock`-ed, then removed, in the nearest directory of the
        queue's path that exists. A read-only or chmod-500 HOME, a volume out of
        inodes, or a filesystem without `flock` (ENOSYS: Lustre without
        ``-o flock``, some overlays) used to drop EVERY write, with a warning
        apiece. The lock taken is a fresh file's, never the queue's own, so a
        busy queue (another process appending) cannot read as unusable (Codex,
        round 2)."""
        import tempfile

        probe_dir = self.ops_dir
        while not probe_dir.exists() and probe_dir.parent != probe_dir:
            probe_dir = probe_dir.parent
        try:
            with tempfile.TemporaryFile(dir=probe_dir, prefix=".probe-usable-") as handle:
                try:
                    oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
                    oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
                except OSError as exc:
                    if exc.errno in _UNUSABLE_LOCK_ERRNOS:
                        return f"{probe_dir} does not support file locks ({exc.strerror or exc})"
        except OSError as exc:
            return f"{probe_dir} is not writable ({exc.strerror or exc})"
        return None

    @staticmethod
    def discover() -> list[Path]:
        """Every outbox directory of this user on this machine: the default
        root and its ``rank-*`` children, and the ``$TMPDIR`` fallback and
        its. Only directories that hold a queue, their own or a per-credential
        one under ``credential-v1/`` (plan 1.5: `probe outbox status` saw only
        the default one, so a distributed job's ranks and a fallen-back queue
        were invisible).

        Deliberately ``rank-*`` only: an offline run's queue (plan 2.12,
        ``<root>/offline/``) is delivered by `probe sync` alone, so `probe outbox
        drain --all` must never find it; and the per-credential queues of #2041
        (``<dir>/credential-v1/<fingerprint>/``) are reached through each
        directory's own `namespaces()`, never as roots of their own.

        A ``$TMPDIR`` fallback is listed only when it is a `trusted_dir`, and so
        is each of its ``rank-*`` children: a directory another user made there
        must never be drained with this user's credential (review of #2054)."""
        found: list[Path] = []
        roots = [(default_root(), False)] + [(root, True) for root in _fallback_roots()]
        for root, untrusted_place in roots:
            candidates = [root]
            try:
                candidates += sorted(
                    child for child in root.iterdir() if child.name.startswith("rank-")
                )
            except OSError:
                pass
            for candidate in candidates:
                if candidate in found:
                    continue
                if untrusted_place and not trusted_dir(candidate):
                    continue
                if os.path.islink(candidate):
                    continue
                if (
                    (candidate / "ops").is_dir()
                    or (candidate / "status.json").exists()
                    # Every write of it queued under a stamped credential
                    # (#2041): the directory holds no queue of its own.
                    or (candidate / CREDENTIAL_NAMESPACE).is_dir()
                ):
                    found.append(candidate)
        return found

    def _ensure(self) -> None:
        # Once per Journal, not once per append. This ran 4 mkdir + 4 chmod on
        # EVERY write; chmod is a SETATTR write RPC on NFS, not a cached stat,
        # so on a shared $HOME it was eight round trips per metric point. The
        # flag is cleared by `_ensure_again` whenever a write actually fails, so
        # a directory deleted underneath us is still recreated -- the cheap path
        # is the steady state, not an assumption that nothing changes.
        if getattr(self, "_layout_ready", False):
            return
        self._ensure_layout()

    def _ensure_layout(self) -> None:
        for directory in (self.dir, self.ops_dir, self.failed_dir, self.blobs_dir, self.waiting_dir):
            directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            # mkdir mode is masked by umask; queue contents are research data,
            # so re-assert (codex finding: primitives default to umask).
            try:
                os.chmod(directory, 0o700)
            except OSError:
                pass
        self._layout_ready = True
        if not getattr(self, "_spool_checked", False):
            # One-time fold of a surviving pre-journal spool (T1-C). Two stat
            # calls when there is nothing to import. ONLY the default journal
            # auto-imports: a custom/temporary journal directory must never
            # steal (and then delete) the machine's global spool (codex).
            self._spool_checked = True
            if self.dir == default_dir():
                try:
                    self.import_spool()
                except Exception:  # noqa: BLE001 -- legacy debris must not block a write
                    pass

    # -- append -------------------------------------------------------------
    def _op_filename(self, op_id: str, *, sync: str = SYNC_FULL) -> str:
        """FIFO name: monotonic per-journal sequence first, wall clock second.

        Runs under the append lock. The sequence file makes ordering immune to
        backwards clock steps (red team: NTP correction between enqueues could
        otherwise sort a run-end PATCH before the metrics it must follow).

        The `log()` path writes `.seq` without an fsync (plan 1.3), so a power
        loss can leave it BEHIND an op file that survived. That is not
        harmless: the next append would take a sequence below a queued op and
        sort ahead of it -- a terminal PATCH jumping the data it closes. So the
        first sequence this Journal hands out is at least the highest one the
        queue already holds (`_queued_seq_high_water`, names only)."""
        seq_file = self.dir / ".seq"
        try:
            seq = int(seq_file.read_text().strip() or 0)
        except (OSError, ValueError):
            seq = 0
        if not self._seq_recovered:
            floor = self._seq_floor
            if floor is None:
                floor = self._queued_seq_high_water()
            seq = max(seq, floor)
            self._seq_recovered = True
            self._seq_floor = None
        seq += 1
        write_text_atomic(seq_file, f"{seq}\n", mode=0o600, sync=sync)
        return f"{seq:012d}-{time.time_ns():020d}-{op_id}.json"

    def _queued_seq_high_water(self) -> int:
        """The highest queue sequence any op still holds: queued, dead-lettered
        (a retry puts it back in line) or reserved by a waiting upload. Op
        files are read by NAME only; waiting records are few and parsed.

        Safe to take WITHOUT the append lock (the `log()` path does, so a deep
        queue's listing does not hold every other writer): it exists to lift
        `.seq` above ops that survived a machine crash, and those were on disk
        before any process of this boot appended. An op another process adds
        meanwhile took its number from `.seq`, which the lock-holder reads."""
        high = 0
        for directory in (self.ops_dir, self.failed_dir):
            try:
                names = os.listdir(directory)
            except OSError:
                continue
            for name in names:
                head = name.split("-", 1)[0]
                if head.isdigit():
                    high = max(high, int(head))
        for position, *_ in self._waiting_items():
            head = str(position).split("-", 1)[0]
            if head.isdigit():
                high = max(high, int(head))
        return high

    def _stamp_producer_locked(self, op: dict, *, sync: str = SYNC_FULL) -> None:
        if self._producer_id is None:
            return
        # Sequence allocation reads the registry INSIDE the lock, not an
        # in-memory counter: a producer_id shared across processes (the CLI's
        # per-host one) must never mint the same sequence twice (parity F4).
        record = self._read_producer_locked(self._producer_id)
        sequence = int(record.get("last_sequence") or 0) + 1
        op["producer_id"] = self._producer_id
        op["producer_sequence"] = sequence
        # `sync`: the `log()` path does not fsync this (plan 1.3). A power loss
        # can regress `last_sequence` and a later op reuse a number; the
        # sequence is this machine's own accounting (gaps name it), never sent.
        self._update_producer_locked(
            self._producer_id, record, role=self._producer_role, last_sequence=sequence,
            sync=sync,
        )

    def _unstamp_producer_locked(self, op: dict, path: Path | None) -> None:
        """Give back the sequence `_stamp_producer_locked` took for an op whose
        file never landed -- a Ctrl-C mid-append (#2055 lets it through), a full
        disk. Kept, it read as a write handed to the journal that nothing
        accounts for: `last_sequence` one above what could ever be delivered,
        with no gap (a drop then burned a SECOND number for its gap). Under the
        append lock, so no later op can hold a higher number; the op loses its
        stamp, so a retry (`_append`) stamps it afresh. An op whose file DID
        land keeps both. Never raises."""
        producer_id = op.get("producer_id")
        sequence = op.get("producer_sequence")
        if producer_id is None or sequence is None:
            return
        try:
            if path is not None and path.exists():
                return
            op.pop("producer_id", None)
            op.pop("producer_sequence", None)
            record = self._read_producer_locked(producer_id)
            if int(record.get("last_sequence") or 0) == int(sequence):
                record["last_sequence"] = int(sequence) - 1
                self._update_producer_locked(producer_id, record, sync=SYNC_NONE)
        except Exception:  # noqa: BLE001 -- best effort: the caller's error is what matters
            pass

    def _base_op(self, kind: str, run_ref: str | None) -> dict:
        return {
            "schema": SCHEMA,
            "op_id": uuid.uuid4().hex,
            "kind": kind,
            "run_ref": run_ref,
            "context": self.context,
            "attribution": self.attribution,
            "enqueued_at": now_iso(),
            "attempts": 0,
            "last_error": None,
        }

    def _append(
        self,
        op: dict,
        *,
        before_write=None,
        unstaged_low_disk: int = 0,
        headroom_checked: bool = False,
        write_op=None,
        admitted: bool = False,
        sync: str = SYNC_FULL,
    ) -> str:
        # The ENVELOPE only: every op that carries a `body` got it from
        # `append_http`, which scrubbed it (or was handed one `Client.write`
        # had just scrubbed). Scrubbing the whole op again here was a second
        # full pass over every metric point of every `log()` (plan 1.3).
        op.update(scrub_envelope(op))
        try:
            return self._append_locked(
                op,
                before_write=before_write,
                unstaged_low_disk=unstaged_low_disk,
                headroom_checked=headroom_checked,
                write_op=write_op,
                admitted=admitted,
                sync=sync,
            )
        except OutboxFull:
            # A deliberate refusal, not a broken layout. Re-asserting the
            # directories would not create room, and retrying would double-count
            # the capture gap the refusal already recorded.
            raise
        except OSError:
            # The layout may have gone (a tmpdir reaped, a mount that came back
            # empty). Re-assert it once and retry before giving up, so the
            # cached-`_ensure` fast path cannot turn a recoverable state into a
            # dropped write.
            self._layout_ready = False
            self._ensure_layout()
            return self._append_locked(
                op,
                before_write=before_write,
                unstaged_low_disk=unstaged_low_disk,
                headroom_checked=headroom_checked,
                write_op=write_op,
                admitted=admitted,
                sync=sync,
            )

    def _append_locked(
        self,
        op: dict,
        *,
        before_write=None,
        unstaged_low_disk: int = 0,
        headroom_checked: bool = False,
        write_op=None,
        admitted: bool = False,
        sync: str = SYNC_FULL,
    ) -> str:
        """``sync`` is the op file's durability (`durable.write_text_atomic`).
        The rare paths (uploads, receipts, promotions) keep ``"full"`` for
        everything. The `log()` path passes ``"file"``: the op file is fsynced
        before its rename -- a process killed after this returns loses nothing,
        and a power loss can lose only the last renames, never leave a torn
        op -- and the bookkeeping beside it (`.seq`, the producer record,
        status.json) is not fsynced at all. The drain rebuilds the status
        counts, and the sequence is recovered from the op filenames. That took
        `log()` from eight fsyncs to one (plan 1.3, D5)."""
        bookkeeping = SYNC_FULL if sync == SYNC_FULL else SYNC_NONE
        self._ensure()
        if not self._seq_recovered and self._seq_floor is None:
            self._seq_floor = self._queued_seq_high_water()  # outside the lock
        if self._pending_estimate is None:
            self._refresh_pending_estimate()
        refusal = None if admitted else self._append_headroom(check_free=not headroom_checked)
        if refusal is not None:
            # Refuse the NEW write rather than evicting an old one: dropping an
            # op out from under a concurrent drain is a race, and the queue's
            # oldest entries are the ones a barrier is waiting on. The loss is
            # recorded as a numbered gap in the producer registry, so it reads
            # as a hole in the record rather than silence. A best-effort op
            # (hardware) is not the user's data: its loss is neither.
            refused = OutboxFull(refusal)
            if not op.get("best_effort"):
                self.note_capture_gap(refusal)
                # The client's drop handler records gaps too; once is enough.
                refused.gap_recorded = True
                if not self._headroom_warned:
                    self._headroom_warned = True
                    _diagnostics.warn(f"probe: dropping queued writes — {refusal}")
            raise refused
        with file_lock(self.append_lock):
            # A waiting upload was stamped when it was QUEUED, by the
            # producer that queued it; its promoter is someone else.
            stamping = "producer_id" not in op
            path = None
            try:
                if stamping:
                    self._stamp_producer_locked(op, sync=bookkeeping)
                if before_write is not None:
                    # Runs INSIDE the lock, before the op file exists -- used by
                    # append_upload to publish its staged blob atomically with the
                    # op that references it, so gc_blobs (which also takes this
                    # lock) can never see the blob as unreferenced garbage.
                    before_write()
                path = self.ops_dir / (
                    op.get("queue_filename") or self._op_filename(op["op_id"], sync=bookkeeping)
                )
                if write_op is not None:
                    write_op(path, op)
                elif sync == SYNC_FULL:
                    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                else:
                    # Compact: `indent=` takes json's pure-Python encoder.
                    write_text_atomic(
                        path, json.dumps(op, separators=(",", ":")) + "\n", mode=0o600, sync=sync
                    )
            except BaseException:
                if stamping:
                    self._unstamp_producer_locked(op, path)
                raise
            # The count this status write just stored: status.json's previous
            # value (which another process's drain may have lowered) plus one.
            #
            # The op file is ON DISK here: the write is queued, whatever the
            # bookkeeping does next. A volume full but for the few KB the op
            # needed fails this status rewrite with ENOSPC; raising it made the
            # caller count a drop for a write the drain later delivered, made
            # `_append` retry and queue the op a second time, and left the run's
            # lane non-empty so every later write was dropped instead of sent
            # directly (lane S soak, 0.195.0). The drain rebuilds the counts.
            try:
                self._pending_estimate = self._write_status_locked(
                    unstaged_low_disk=unstaged_low_disk,
                    recount=False,
                    pending_delta=1,
                    enqueued_at=op.get("enqueued_at"),
                    pending_bytes_delta=int((op.get("upload") or {}).get("size_bytes") or 0),
                    sync=bookkeeping,
                )
            except OSError:
                self._pending_estimate = (self._pending_estimate or 0) + 1
        return op["op_id"]

    def _refresh_pending_estimate(self) -> int:
        """Re-seed `_pending_estimate` from status.json. One small file read."""
        status = self.read_status(self.dir, include_receipts=False) or {}
        try:
            pending = int(status.get("pending") or 0)
        except (TypeError, ValueError):
            pending = 0
        self._pending_estimate = pending
        return pending

    def _recount_pending(self) -> int | None:
        """The REAL queue length from a directory listing, at most once per
        `_RECOUNT_EVERY_SECONDS` (None when it is too soon). Only the refusal
        path calls it, so the common append never lists the queue."""
        now = time.monotonic()
        if now - self._recounted_at < _RECOUNT_EVERY_SECONDS:
            return None
        self._recounted_at = now
        # Counted OUTSIDE the append lock, names only and unsorted: a sorted
        # listing of a queue at the cap (500k names) held every other writer's
        # `log()` for its whole length. Each append that lands while the
        # listing runs is missing from the count it stores (at the cap, a few
        # per second of listing), so the estimate can read low until the next
        # drain pass recounts for real -- it can admit a few writes over the
        # cap, never refuse one under it.
        try:
            count = sum(1 for name in os.listdir(self.ops_dir) if name.endswith(".json"))
        except FileNotFoundError:
            count = 0
        with file_lock(self.append_lock):
            # Store it, or the next append's delta would rebuild the stale
            # number from status.json and refuse again.
            self._write_status_locked(recount=False, set_pending=count)
        self._pending_estimate = count
        return count

    def append_http(
        self,
        method: str,
        path: str,
        body: dict | None,
        *,
        run_ref: str | None = None,
        blocking: bool = True,
        correlation: str | None = None,
        validation_error: str | None = None,
        best_effort: bool = False,
        admitted: bool = False,
        tag: str | None = None,
        _prepared: bool = False,
    ) -> str:
        """Journal one HTTP op.

        ``tag`` names what kind of op this is for a later reader of the queue
        (`probe sync`'s gate: a late hash re-send, ``"late_hash"``). Never
        sent; a drainer that does not know it ignores it.

        ``_prepared=True`` is `Client.write`'s: the body was normalized,
        NUL-checked and scrubbed on the way in (a failed NUL check arrives as
        ``validation_error``), so this does not do all three again on every
        `log()` (plan 1.3). Every other caller hands a raw body and keeps them.

        ``admitted=True`` skips the queue-length cap and the free-space floor,
        for the ONE op that must not be refused by them: a run's terminal
        status, queued behind data that filled the queue.

        ``best_effort=True`` marks an op that is not the user's data (the
        hardware rail): a refusal for room drops it without a capture gap or
        the "dropping queued writes" notice, both of which mean the user's
        own writes are being lost.

        ``blocking=False`` marks an op that must NOT hold a run's close.
        `Run.finish` refuses to mark a run terminal while any of its ops are
        undelivered or dead-lettered -- correct for data, wrong for a write whose
        whole contract is best-effort. A diagnostic that dead-letters would
        otherwise leave the run `running` for the reaper instead of `failed`:
        the report changing the outcome it reports on.
        """
        from . import unstorable

        if not _prepared:
            body = unstorable.normalize_json(body)
            # The same door as `Client.write` (review of #2053): the hardware
            # rail and other direct appends reach the queue here.
            body, unstorable_reasons = unstorable.drop_unstorable_points(method, path, body)
            if unstorable_reasons and not body.get("points"):
                return ""
            try:
                unstorable.validate_nuls(body, path=path, method=method)
            except errors.ValidationError as exc:
                validation_error = str(exc)
            body = scrub_body(body)
        if validation_error is not None and correlation is not None:
            raise errors.ValidationError(validation_error, status=422)
        if correlation is not None:
            if not self.receipt_enabled:
                return self.for_receipts(
                    self.dir, context=self.context, attribution=self.attribution
                ).append_http(
                    method, path, body, run_ref=run_ref, blocking=blocking, correlation=correlation
                )
            if (
                method.upper() != "POST"
                or not body
                or body.get("is_reference") is not True
                or not re.fullmatch(r"/v1/(runs|experiments|projects)/[^/]+/artifacts", path)
            ):
                raise ValueError("correlated HTTP operations must create an artifact reference")
            self._receipt_dirs()
            key = self._correlation_key(correlation)
            request = {
                "kind": "http",
                "method": method,
                "path": path,
                "body": body,
                "context": self.context,
                "attribution": self.attribution,
            }
            with self._correlation_lock(key):
                prior = self._replay_correlation(correlation, request)
                if prior is not None:
                    return prior["op_id"]
                op = self._base_op("http", run_ref or run_ref_for_path(path))
                op.update({"method": method, "path": path, "body": body})
                return self._publish_receipt_op(correlation, request, op)["op_id"]
        if self.receipt_enabled:
            raise ValueError("delivery-v1 requires an explicit correlation")
        # An unknown kind makes older drainers refuse this too; a new field on
        # kind=http would be ignored and could upload a scrubbed identity alias.
        kind = "rejected_http" if validation_error is not None else "http"
        op = self._base_op(kind, run_ref or run_ref_for_path(path))
        op.update({"method": method, "path": path, "body": body})
        if validation_error is not None:
            op["validation_error"] = validation_error
        if not blocking:
            op["blocking"] = False
        if best_effort:
            op["best_effort"] = True
        if tag is not None:
            op["tag"] = tag
        # The `log()` path: one fsync, of the op file (`_append_locked`). An
        # admitted op (a run's terminal status, once per run) keeps them all.
        return self._append(op, admitted=admitted, sync=SYNC_FULL if admitted else SYNC_FILE)

    def append_upload(
        self,
        *,
        anchor: str,
        anchor_id: str | None,
        name: str,
        src_path: str,
        stage: bool = True,
        inline_hash: bool = False,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        notes: str | None = None,
        span_id: str | None = None,
        step_index: int | None = None,
        run_ref: str | None = None,
        require_staged: bool = False,
        correlation: str | None = None,
        expected_content_hash: str | None = None,
        blocking: bool = True,
        defer_scan: bool = False,
    ) -> dict:
        """Queue a byte upload; returns ``{op_id, blob, size_bytes}``.

        ``blocking=False`` marks an upload that must NOT hold its run's close,
        exactly like ``append_http``'s flag: `Run.finish` still drains it first,
        but an undeliverable one (an R2 outage) cannot keep the run open.
        Output capture uses it; an explicit `log_artifact` does not.

        When ``stage`` is set the file is snapshotted into the blob store, and
        with ``inline_hash`` the digest is taken FROM THE SNAPSHOT -- never
        from the live source, whose bytes can change between a hash pass and a
        copy pass (codex: a same-size rewrite in that window would poison the
        content address). Without ``inline_hash`` the drainer hashes later
        (11A). Snapshot lands under a dot-prefixed staging name (gc ignores
        dotfiles); the publish rename + op-file write happen together under
        the append lock, so gc can never see an unreferenced blob to delete.

        A requested ``stage`` can still come back false: staging is refused
        when the snapshot would drive the blob store's filesystem under
        :data:`MIN_FREE_BYTES`. The returned ``staged``/``unstaged_reason``
        (also recorded on the op) say so.

        ``require_staged`` REFUSES that degrade instead of taking it: nothing is
        appended and ``op_id`` comes back None (the only case where it is not a
        string), with ``staged``/``unstaged_reason`` saying why. The caller is
        expected to upload synchronously instead.

        Why it exists. An unstaged op records ``src_path`` and the drainer reads
        the LIVE FILE at delivery. Under an opt-in ``--async`` the caller chose
        that. As a DEFAULT it is a footgun: `probe artifact add ckpt.pt` beside a
        training loop that rotates checkpoints would upload step-1100 bytes under
        the step-1000 name, or 422 on a file that is gone. Staging cannot be
        predicted from the outside -- free space is a race -- so the honest shape
        is to attempt it and be told, which is what this flag buys.

        Default False keeps every existing caller byte-identical.

        ``defer_scan`` (with ``stage``) takes the credential scan off the
        caller's thread: the file is copied into the waiting room and the call
        returns; `promote_waiting` scans, redacts and fingerprints the copy and
        only then queues it. ``blob`` comes back None and ``waiting`` True.
        """
        meta = default_scrub(meta)
        notes = scrub_text(notes) if notes is not None else None
        name = scrub_text(name)
        if correlation is not None:
            queue = (
                self
                if self.receipt_enabled
                else self.for_receipts(self.dir, context=self.context, attribution=self.attribution)
            )
            return queue._receipt_upload(
                correlation=correlation,
                expected_content_hash=expected_content_hash,
                anchor=anchor,
                anchor_id=anchor_id,
                name=name,
                src_path=src_path,
                content_type=content_type,
                kind=kind,
                meta=meta,
                notes=notes,
                span_id=span_id,
                step_index=step_index,
                run_ref=run_ref,
            )
        if self.receipt_enabled:
            raise ValueError("delivery-v1 requires an explicit correlation")
        check_upload(src_path)
        self._ensure()
        upload = {
            "anchor": anchor,
            "anchor_id": anchor_id,
            "name": name,
            "content_type": content_type,
            "kind": kind,
            "meta": meta,
            "notes": notes,
            "span_id": span_id,
            "step_index": step_index,
            "src_path": os.path.abspath(src_path),
        }
        # The strict policy keeps the full scan on the caller's thread, where it
        # always was (`read_upload_redacted`); only the quick check waits.
        if stage and defer_scan and not strict_policy():
            waiting = self._enqueue_waiting(
                upload, run_ref=run_ref, inline_hash=inline_hash, require_staged=require_staged,
                blocking=blocking,
            )
            if waiting is not None:
                return waiting
        op = self._base_op("upload", run_ref)
        if not blocking:
            op["blocking"] = False
        staged = False
        publish = None
        digest: str | None = None
        size_bytes: int | None = None
        unstaged_reason: str | None = None
        if stage:
            unstaged_reason = self._staging_headroom(src_path)
            if unstaged_reason is not None:
                if require_staged:
                    # Refuse rather than degrade. No op is appended, so the
                    # caller's synchronous fallback is the ONLY writer -- leaving
                    # a queued op here would upload the file twice, and the
                    # drainer's later read of a rotated src_path would win.
                    return {
                        "op_id": None,
                        "blob": None,
                        "size_bytes": None,
                        "staged": False,
                        "unstaged_reason": unstaged_reason,
                    }
                # Degrade to referencing the source rather than refusing the
                # write: enqueue is fail-open by contract (it runs beside a
                # training loop), so the op still goes in and the drainer reads
                # the original bytes. If the source is gone by then the drain
                # raises a 422 -- a dead letter with a message, never a lost
                # write nobody was told about, and never a full disk.
                stage = False
        if stage:
            staging = self.blobs_dir / f".staging-{op['op_id']}"
            snapshot_file(src_path, staging)
            if inline_hash:
                digest, size_bytes = fingerprint(str(staging))
            final = (
                self.blobs_dir / digest
                if digest is not None
                else self.blobs_dir / f"incoming-{op['op_id']}"
            )

            def publish() -> None:
                if digest is not None and final.exists():
                    staging.unlink(missing_ok=True)  # dedup: bytes already staged
                else:
                    os.replace(staging, final)
                fsync_directory(self.blobs_dir)

            staged = True
        elif inline_hash:
            # UNSTAGED, so nothing redacts -- as it never did: the drainer
            # re-reads this path and sends it as it sits (inspected first only
            # under the block policy). The digest must therefore describe the
            # file as it sits, or the guard refuses the very upload this policy
            # exists to save. (An earlier version fingerprinted the redacted
            # bytes here and every such op dead-lettered.) The server records
            # what it finds.
            digest, size_bytes = fingerprint(src_path)
        op["upload"] = {
            **upload,
            "blob": digest,
            "staged": staged,
            "size_bytes": size_bytes,
            "unstaged_reason": unstaged_reason,
        }
        self._append(
            op,
            before_write=publish,
            unstaged_low_disk=1 if unstaged_reason is not None else 0,
            # `_staging_headroom` above already priced this write's disk cost and
            # degraded to an unstaged reference if there was no room. Re-checking
            # the floor here would refuse the very op that degrade produced.
            headroom_checked=True,
        )
        return {
            "op_id": op["op_id"],
            "blob": digest,
            "size_bytes": size_bytes,
            "staged": staged,
            "unstaged_reason": unstaged_reason,
        }

    # -- the waiting room: uploads queued before their credential scan ------
    #
    # WHY. `log_artifact` used to scan the file three times on the caller's
    # thread before returning (205 s for an 11.5 MB zip). Now the call copies the
    # file here and returns; `promote_waiting` -- in the detached worker, a
    # barrier, or `drain` -- scans, redacts and fingerprints the copy, and only
    # then does it become an op in `ops/`.
    #
    # WHY A SEPARATE DIRECTORY. Every released drainer reads every `*.json` in
    # `ops/` (hidden names included), and an old one sharing this journal would
    # upload whatever it found there. Nothing unscanned may ever sit in `ops/`.
    #
    # THE COMMIT ORDER, per item `<id>` (item flock held throughout):
    #   enqueue: `<id>.bytes` (plain copy, fsync), then `<id>.json` (the record;
    #            its existence is what "queued" means).
    #   promote: redact into a staging blob; then under the append lock --
    #            (1) publish the blob  (2) write the final op to `<id>.op.json`
    #            (3) unlink `<id>.json`  (4) RENAME `<id>.op.json` into `ops/`;
    #            then (5) unlink `<id>.bytes`.
    #   recover: `<id>.json` present -> promote again (the op was never visible);
    #            only `<id>.op.json` -> roll forward, re-deriving the blob from
    #            `<id>.bytes` (a GC may have taken the published one); only
    #            `<id>.bytes` -> delete it.
    # So each item becomes exactly one visible op, never zero, never two.
    #
    # ORDER. Items are promoted in the order they were queued, and a run's
    # items never pass its earliest one that cannot be promoted right now
    # (another process holds it, a disk error): two versions of one artifact
    # must reach the server in the order they were logged. `drain` holds a
    # run's later ops back the same way (`waiting_positions`).

    def _waiting_paths(self, op_id: str) -> tuple[Path, Path, Path, Path]:
        base = self.waiting_dir / op_id
        return (
            base.with_suffix(".json"),
            self.waiting_dir / f"{op_id}.op.json",
            base.with_suffix(".bytes"),
            base.with_suffix(".lock"),
        )

    def _enqueue_waiting(
        self,
        upload: dict,
        *,
        run_ref: str | None,
        inline_hash: bool,
        require_staged: bool,
        blocking: bool = True,
    ) -> dict | None:
        # Two copies until promotion ends: the waiting one and the clean blob.
        refusal = self._staging_headroom(upload["src_path"], copies=2)
        if refusal is not None:
            if require_staged:
                return {"op_id": None, "blob": None, "size_bytes": None, "staged": False,
                        "unstaged_reason": refusal}
            return None  # the ordinary path degrades to an unstaged reference
        # The op ceiling counts what waits as well as what is queued: a stalled
        # promoter must not let an upload-only producer grow this without bound.
        refusal = self._append_headroom(check_free=False, extra=self.count_waiting(self.dir))
        if refusal is not None:
            raise OutboxFull(refusal)
        op = self._base_op("upload", run_ref)
        if not blocking:
            op["blocking"] = False  # see `append_upload`; it rides into the op
        op["upload"] = {**upload, "blob": None, "staged": True, "size_bytes": None,
                        "unstaged_reason": None}
        record, _, data, lock = self._waiting_paths(op["op_id"])
        with _item_lock(lock):
            # The queue position is the CALL's, reserved now: a run's terminal
            # status queued after this upload must still sort after it. So is
            # the producer's sequence: its promoter is someone else.
            with file_lock(self.append_lock):
                op["queue_filename"] = self._op_filename(op["op_id"])
                self._stamp_producer_locked(op)
            raw = read_source(upload["src_path"])
            _write_private(data, raw)
            write_text_atomic(
                record, json.dumps({"op": op, "inline_hash": bool(inline_hash)}) + "\n", mode=0o600
            )
            fsync_directory(self.waiting_dir)
        return {"op_id": op["op_id"], "blob": None, "size_bytes": len(raw), "staged": True,
                "unstaged_reason": None, "waiting": True}

    def _waiting_items(self) -> list[tuple[str, str, str | None, bool, bool]]:
        """`(queue position, op id, run_ref, readable, blocking)` per waiting
        item, in queue order. An unreadable record sorts first, so it is dealt
        with before anything it might be holding up."""
        try:
            names = os.listdir(self.waiting_dir)
        except OSError:
            return []
        items: dict[str, tuple[str, str, str | None, bool, bool]] = {}
        for op_id in {name.split(".", 1)[0] for name in names if name.endswith(".json")}:
            # The record, then the committed op: a promotion between the
            # listing and this read has replaced one with the other (steps 2-3),
            # and only when both are gone is the op in `ops/` (step 4) -- which
            # a reader that looks at `ops/` AFTER this one then sees.
            record, prepared, _, _ = self._waiting_paths(op_id)
            for path in (record, prepared):
                try:
                    body = json.loads(path.read_text())
                    op = body.get("op") or body
                    items[op_id] = (str(op["queue_filename"]), op_id, op.get("run_ref"), True,
                                    op.get("blocking", True) is not False)
                except FileNotFoundError:
                    continue
                except (OSError, ValueError, KeyError, TypeError, AttributeError):
                    items[op_id] = ("", op_id, None, False, True)
                break
        return sorted(items.values())

    def waiting(self, *, run_ref: str | None = None) -> list[str]:
        """Op ids still in the waiting room (queued, or promoted halfway), in
        the order they were queued."""
        return [
            op_id for _, op_id, ref, readable, _ in self._waiting_items()
            if run_ref is None or ref == run_ref or not readable
        ]

    def waiting_positions(self) -> dict[str | None, str]:
        """Per run, the queue position of its earliest waiting upload: `drain`
        delivers none of that run's ops queued after it. A non-blocking upload
        (`append_upload(blocking=False)`) holds nothing back."""
        positions: dict[str | None, str] = {}
        for position, _, ref, readable, blocking in self._waiting_items():
            if readable and blocking and ref is not None:
                positions.setdefault(ref, position)
        return positions

    @staticmethod
    def count_waiting(directory: str | Path) -> int:
        """Waiting items, by LISTING the directory -- never from status.json,
        which an older worker rewrites from `ops/` alone."""
        try:
            names = os.listdir(Path(directory) / "waiting")
        except OSError:
            return 0
        return len({name.split(".", 1)[0] for name in names if name.endswith(".json")})

    def promote_waiting(
        self, *, run_ref: str | None = None, wait: bool = False, timeout: float | None = None
    ) -> int:
        """Scan, redact and fingerprint waiting uploads; queue each as an op.

        Returns how many became ops. Items go in queue order, and a run stops at
        its first item that cannot go now: another process holds it (with
        ``wait``, waited for) or a disk error. Outbox full stops the pass. An
        item that can never go -- an unreadable record, a missing copy, a scan
        that fails -- is dead-lettered with the reason. ``timeout`` bounds the
        call: no scan starts, and no wait continues, after it.
        """
        if self.receipt_enabled or not self.waiting_dir.is_dir():
            return 0
        deadline = None if timeout is None else time.monotonic() + timeout
        promoted = 0
        while True:
            busy = False
            stopped: set[str | None] = set()  # runs held at an earlier item
            for _, op_id, ref, readable, _ in self._waiting_items():
                if deadline is not None and time.monotonic() >= deadline:
                    return promoted
                # An unreadable item belongs to no run we can name: it is taken
                # whatever `run_ref` asks for, and dead-lettered.
                if (run_ref is not None and ref != run_ref and readable) or ref in stopped:
                    continue
                with _try_lock(self._waiting_paths(op_id)[3]) as held:
                    if not held:
                        busy = True
                        stopped.add(ref)
                        continue
                    try:
                        promoted += self._promote_locked(op_id)
                    except OutboxFull:
                        return promoted
                    except OSError:
                        stopped.add(ref)  # left waiting; the next pass retries
                    except Exception as exc:  # noqa: BLE001 -- one item must not wedge the rest
                        self._dead_letter_waiting(
                            op_id, None, f"promotion failed ({type(exc).__name__})"
                        )
            self._sweep_waiting_orphans()
            if not (wait and busy):
                return promoted
            if deadline is not None and time.monotonic() >= deadline:
                return promoted
            time.sleep(0.05)

    def promote_for_close(self, run_ref: str, *, timeout: float) -> list[str]:
        """Before a run's close is queued: promote its waiting uploads, waiting
        up to ``timeout`` for any another process is scanning. Returns the op
        ids still waiting that hold the close (a non-blocking upload does not)
        -- the caller decides whether that refuses the close."""
        try:
            self.promote_waiting(run_ref=run_ref, wait=True, timeout=timeout)
        except Exception:  # noqa: BLE001 -- judged by what is still waiting
            pass
        return self.waiting_for_close(run_ref)

    def waiting_for_close(self, run_ref: str) -> list[str]:
        """This run's waiting uploads that hold its close: every one but those
        queued non-blocking, plus any unreadable item (it may be this run's)."""
        return [
            op_id for _, op_id, ref, readable, blocking in self._waiting_items()
            if (ref == run_ref and blocking) or not readable
        ]

    def _promote_locked(self, op_id: str) -> int:
        record, prepared, data, lock = self._waiting_paths(op_id)
        if not record.exists() and not prepared.exists():
            data.unlink(missing_ok=True)
            return 0
        starting_over = record.exists()
        try:
            body = json.loads((record if starting_over else prepared).read_text())
            op = dict(body["op"] if starting_over else body)
            inline_hash = bool(body.get("inline_hash"))
            if "op_id" not in op or not isinstance(op.get("upload"), dict):
                raise KeyError("op")  # not the shape promotion relies on
        except FileNotFoundError:
            return 0  # promoted meanwhile
        except (ValueError, KeyError, TypeError, AttributeError):
            self._dead_letter_waiting(op_id, None, "the queued upload's record is unreadable")
            return 0
        try:
            raw = data.read_bytes()
        except FileNotFoundError:
            self._dead_letter_waiting(op_id, op, "the queued copy of the upload is missing")
            return 0
        if starting_over:
            prepared.unlink(missing_ok=True)  # a half-made promotion; start over
            try:
                clean, result = redact_quick_bytes(raw)
            except CredentialBlocked as exc:
                self._dead_letter_waiting(op_id, op, str(exc))
                return 0
            if result.rewritten:
                # The artifact row records this too (the server reads the
                # markers); this line is for whoever reads the worker's log.
                print(
                    f"redacted {', '.join(sorted(set(result.rewritten)))} in queued upload "
                    f"{(op.get('upload') or {}).get('name')!r} ({now_iso()})",
                    flush=True,
                )
            digest = hashlib.sha256(clean).hexdigest() if inline_hash else None
            op["upload"]["blob"] = digest
            op["upload"]["size_bytes"] = len(clean) if inline_hash else None
            publish = self._staged_publisher(op, clean)
        else:
            # Roll forward: the op was committed and never made visible. Its
            # blob may have gone to a GC since (it was unreferenced), so the
            # blob is derived again from the scanned source, which is deleted
            # last, and published under the append lock like any other: whether
            # it still exists is only knowable there.
            try:
                clean, _ = redact_quick_bytes(raw)
            except CredentialBlocked as exc:
                self._dead_letter_waiting(op_id, op, str(exc))
                return 0
            publish = self._staged_publisher(op, clean)

        def write_op(path: Path, final_op: dict) -> None:
            # (2) the committed op, (3) retire the record, (4) make it visible.
            write_text_atomic(prepared, json.dumps(final_op, indent=2) + "\n", mode=0o600)
            record.unlink(missing_ok=True)
            fsync_directory(self.waiting_dir)
            os.replace(prepared, path)
            fsync_directory(self.ops_dir)

        # `admitted`: the op ceiling counted this upload when it was queued
        # (`_enqueue_waiting`). Refusing it now could deadlock -- drain holds
        # the run's later ops, which fill the queue, behind this very upload.
        self._append(op, before_write=publish, headroom_checked=True, write_op=write_op, admitted=True)
        data.unlink(missing_ok=True)  # (5)
        # Safe while held: a promoter that opened the old lock finds nothing
        # left to do, and one that locks it after this unlink is told it holds
        # nothing (`_same_file`).
        _retire_lock(lock)
        return 1

    def _staged_publisher(self, op: dict, clean: bytes):
        """Write `clean` to a staging blob now; return the publish step that
        moves it into place inside the append lock (gc takes the same lock)."""
        staging = self.blobs_dir / f".staging-{op['op_id']}"
        staging.unlink(missing_ok=True)
        _write_private(staging, clean)
        digest = op["upload"].get("blob")
        final = self.blobs_dir / digest if digest else self.blobs_dir / f"incoming-{op['op_id']}"

        def publish() -> None:
            if digest is not None and final.exists():
                staging.unlink(missing_ok=True)  # dedup: these bytes are already staged
            else:
                os.replace(staging, final)
            fsync_directory(self.blobs_dir)

        return publish

    def _dead_letter_waiting(self, op_id: str, op: dict | None, reason: str) -> None:
        """Refuse a waiting upload the way the synchronous path refuses one:
        with the reason, and nothing sent. Its copy goes: a retry has nothing
        scanned to deliver (it fails again, never sends unscanned bytes)."""
        record, prepared, data, lock = self._waiting_paths(op_id)
        if op is None:
            # Keep whatever attribution survives: a run-scoped close checks
            # its run's dead letters, and one filed under no run is missed.
            try:
                body = json.loads((record if record.exists() else prepared).read_text())
                found = body.get("op") or body
                op = dict(found) if isinstance(found, dict) and found.get("run_ref") else None
            except (OSError, ValueError, AttributeError, TypeError):
                op = None
        if op is None:
            op = {**self._base_op("upload", None), "op_id": op_id, "upload": {"staged": True}}
        op["last_error"] = f"{reason}; nothing was sent -- log the artifact again"
        op["attempts"] = int(op.get("attempts") or 0) + 1
        name = op.get("queue_filename") or self._op_filename(op_id)
        with file_lock(self.append_lock):
            write_text_atomic(self.failed_dir / name, json.dumps(op, indent=2) + "\n", mode=0o600)
            record.unlink(missing_ok=True)
            prepared.unlink(missing_ok=True)
            data.unlink(missing_ok=True)
            self._write_status_locked()
        _retire_lock(lock)

    def _sweep_waiting_orphans(self) -> None:
        """Delete `.bytes` with neither record nor committed op: an enqueue that
        died before returning, or a promotion that finished. Locked ones are an
        enqueue in progress and are left alone."""
        try:
            names = os.listdir(self.waiting_dir)
        except OSError:
            return
        live = {name.split(".", 1)[0] for name in names if name.endswith(".json")}
        for name in names:
            if not name.endswith((".bytes", ".lock")) or name.split(".", 1)[0] in live:
                continue
            record, prepared, data, lock = self._waiting_paths(name.split(".", 1)[0])
            with _try_lock(lock) as held:
                if held and not record.exists() and not prepared.exists():
                    data.unlink(missing_ok=True)
                    _retire_lock(lock)

    def _append_headroom(self, *, check_free: bool = True, extra: int = 0) -> str | None:
        """``None`` when there is room for one more queued op, else WHY not.

        The disk floor and the op ceiling both existed only for UPLOAD staging,
        whose own comment says it best: "a producer that outruns delivery grows
        the queue without bound: filling the disk is the STEADY STATE of that
        shape, not an edge case." That is exactly what a metric-logging loop
        does during an outage, and `append_http` had no ceiling of any kind --
        no free-space floor, no count cap, no backpressure. A long enough
        outage filled the state partition, and on a shared $HOME it filled
        everyone's.

        The free-space stat is sampled, not per-append: disk pressure builds
        over thousands of writes, so paying a statvfs on every metric point
        would be the same mistake as the listdir this class just stopped doing.
        The op-count ceiling is free -- the delta counter already tracks it.
        """
        ceiling = MAX_PENDING_OPS if self.op_ceiling is None else self.op_ceiling
        pending = self._pending_estimate
        other = self._sibling_pending_count()
        if pending is None and extra:
            pending = self._refresh_pending_estimate()
        if pending is not None:
            pending += other + extra
        if pending is not None and ceiling > 0 and pending >= ceiling:
            # Re-read before refusing: a refusal is a dropped datapoint, and
            # another process's drain may have lowered the count since.
            other = self._sibling_pending_count(fresh=True)
            pending = self._refresh_pending_estimate() + other + extra
        if pending is not None and ceiling > 0 and pending >= ceiling:
            # status.json can still say "full" in the middle of a drain pass
            # that has already delivered most of the queue: count it for real.
            real = self._recount_pending()
            if real is not None:
                pending = real + other + extra
        if pending is not None and ceiling > 0 and pending >= ceiling:
            return (
                f"outbox full: {pending} ops queued, at the {ceiling} "
                "ceiling (PROBE_OUTBOX_MAX_PENDING). Delivery is not keeping up "
                "— see `probe outbox status`"
            )
        if not check_free:
            # The caller already made its own headroom decision. `append_upload`
            # asks `_staging_headroom` first and DEGRADES to an unstaged op --
            # a small reference rather than a byte copy -- which is precisely
            # the path that has to keep working when the disk is tight. Blocking
            # it here would refuse the write the degrade exists to preserve.
            # The op-count ceiling above still applies.
            return None
        return self.below_floor()

    def below_floor(self) -> str | None:
        """Why the queue's volume is under its free-space floor, or None.

        Sampled, not per call: disk pressure builds over thousands of writes,
        so the statvfs runs every `_STATVFS_EVERY` calls -- and on every call
        while the last sample was low, so recovery is seen at once. `Client`
        asks before it queues (plan 1.5: below the floor it may send directly
        instead), and every append asks again."""
        floor = self._free_floor()
        if floor <= 0:
            return None
        self._appends_since_statvfs += 1
        if self._appends_since_statvfs < _STATVFS_EVERY and self._last_free_ok:
            return None
        self._appends_since_statvfs = 0
        try:
            free = shutil.disk_usage(self.ops_dir if self.ops_dir.exists() else self.dir).free
        except OSError:
            self._last_free_ok = True
            return None  # unmeasurable is not a breach; enqueue is fail-open
        self._last_free_ok = free >= floor
        if self._last_free_ok:
            return None
        return (
            f"low disk: {free} bytes free on {self.ops_dir}, under the "
            f"{floor}-byte floor (PROBE_OUTBOX_MIN_FREE_BYTES). Queued writes "
            "are sent directly while nothing is queued, else dropped rather "
            "than filling the filesystem"
        )

    def _free_floor(self) -> int:
        """`free_floor` for this journal's volume, measured once (a volume's
        size does not change under a running process; an override does not
        need measuring at all)."""
        if MIN_FREE_BYTES is not None:
            return MIN_FREE_BYTES
        floor = getattr(self, "_floor_cached", None)
        if floor is None:
            where = self.dir if self.dir.exists() else self.dir.parent
            floor = self._floor_cached = free_floor(where)
        return floor

    def _sibling_pending_count(self, *, fresh: bool = False) -> int:
        """The other namespace's (`delivery-v1` <-> the root) pending count,
        which the op ceiling counts too. Re-read every `_STATVFS_EVERY`
        appends and before any refusal (``fresh``), not on each append: it
        was a status.json open per `log()` for a namespace that, for a
        training loop, is nearly always empty (plan 1.3)."""
        self._appends_since_sibling += 1
        if (
            fresh
            or self._sibling_pending is None
            or self._appends_since_sibling >= _STATVFS_EVERY
        ):
            self._appends_since_sibling = 0
            sibling = self.dir.parent if self.receipt_enabled else self.dir / DELIVERY_NAMESPACE
            other = self.read_status(sibling, include_receipts=False) or {}
            try:
                self._sibling_pending = int(other.get("pending") or 0)
            except (TypeError, ValueError):
                self._sibling_pending = 0
        return self._sibling_pending

    def _staging_headroom(self, src_path: str | Path, *, copies: int = 1) -> str | None:
        """``None`` when there is room to stage ``src_path``, else WHY there is not.

        Two stat-class syscalls, no read of the file -- this runs on every
        upload enqueue, beside a training loop, so it must not scale with the
        bytes being queued. Unmeasurable is NOT a breach: if the size or the
        filesystem cannot be read we have no evidence to degrade on, and
        enqueue is fail-open.
        """
        floor = self._free_floor()
        if floor <= 0:
            return None
        try:
            size = os.path.getsize(src_path)
            free = shutil.disk_usage(self.blobs_dir).free
        except OSError:
            return None
        if free - copies * size >= floor:
            return None
        return (
            f"low disk: staging {size} bytes would leave {free - copies * size} bytes "
            f"free on {self.blobs_dir}, under the {floor}-byte floor "
            "(PROBE_OUTBOX_MIN_FREE_BYTES); the op references the source "
            "instead and the drainer reads its original bytes"
        )

    # -- producer registry (parity F4) --------------------------------------
    def _producer_file(self, producer_id: str) -> Path:
        return self.producers_dir / f"{_safe_component(producer_id)}.json"

    def _ensure_producers_dir(self) -> None:
        self.producers_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        try:
            os.chmod(self.producers_dir, 0o700)
        except OSError:
            pass

    def _read_producer_locked(self, producer_id: str) -> dict:
        try:
            return json.loads(self._producer_file(producer_id).read_text())
        except (OSError, json.JSONDecodeError, ValueError):
            return {}

    def _update_producer_locked(
        self,
        producer_id: str,
        record: dict,
        *,
        role: str | None = None,
        last_sequence: int | None = None,
        delivered: int | None = None,
        gap: dict | None = None,
        state: str | None = None,
        sync: str = SYNC_FULL,
    ) -> None:
        record.setdefault("schema", SCHEMA)
        record.setdefault("producer_id", producer_id)
        record.setdefault("role", role)
        record.setdefault("registered_at", now_iso())
        record.setdefault("last_sequence", 0)
        record.setdefault("delivered", 0)
        record.setdefault("gaps", [])
        record.setdefault("gap_count", len(record["gaps"]))
        record.setdefault("closed_at", None)
        if last_sequence is not None:
            record["last_sequence"] = max(int(record["last_sequence"]), last_sequence)
        if delivered is not None:
            # Additive, and re-read from disk under the lock by every caller:
            # the drainer and a live writer touch the same record from
            # different processes, so an in-memory counter would clobber.
            record["delivered"] = int(record.get("delivered") or 0) + int(delivered)
        if gap is not None:
            # A count plus the most recent few: the full list grew by one per
            # dropped write and is rewritten with every drop.
            record["gap_count"] = int(record.get("gap_count") or 0) + 1
            record["gaps"] = [*record["gaps"], gap][-_GAPS_KEPT:]
        if state is not None:
            record["state"] = state
            record["closed_at"] = now_iso() if state == "closed" else None
        else:
            record.setdefault("state", "open")
        write_text_atomic(
            self._producer_file(producer_id),
            json.dumps(record, indent=2) + "\n",
            mode=0o600,
            sync=sync,
        )

    def register_producer(self, producer_id: str, *, role: str = "sdk") -> None:
        """Join this journal's producer registry.

        Sequences make silent capture loss VISIBLE: every subsequent append
        stamps ``producer_id`` + a per-producer sequence, and the registry
        records the high-water mark. A registry that says N with no op --
        queued, dead-lettered, or delivered -- ever stamped N is a write lost
        between the caller and the journal; ``note_capture_gap`` records
        those the caller catches itself. Re-registering an existing id
        resumes its sequence (restarts, and ids deliberately shared across
        short-lived processes, both continue the same line).
        """
        self._ensure()
        self._ensure_producers_dir()
        self._producer_id = producer_id
        self._producer_role = role
        with file_lock(self.append_lock):
            record = self._read_producer_locked(producer_id)
            self._update_producer_locked(
                producer_id, record, role=role, state="open"
            )

    def note_capture_gap(self, reason: str) -> None:
        """Burn a sequence for a write that never reached the journal, so the
        loss is a visible hole instead of silence (Miles' capture_gaps)."""
        if self._producer_id is None:
            return
        with file_lock(self.append_lock):
            record = self._read_producer_locked(self._producer_id)
            sequence = int(record.get("last_sequence") or 0) + 1
            self._update_producer_locked(
                self._producer_id,
                record,
                role=self._producer_role,
                last_sequence=sequence,
                gap={"sequence": sequence, "reason": scrub_text(reason), "at": now_iso()},
            )

    def note_delivered(self, producer_id: str, count: int = 1) -> None:
        """Add ``count`` LANDED ops to one producer's tally.

        ``last_sequence`` says what a producer handed the journal; this says
        how much of it actually reached the server, so "of what I enqueued,
        how much is really there" is answerable without correlating two
        machines. ``DrainReport.delivered`` cannot answer it: it is per-pass
        and machine-wide.

        Called by :func:`drain` per delivered op, NOT batched at the end of a
        pass -- a pass that dies mid-flight (SIGKILL, OOM, a dead laptop) is
        exactly when the number matters, and a batched tally would lose the
        whole pass. It takes a producer id rather than using this journal's
        own because the drainer delivers for every producer, usually including
        producers that no longer have a live process.

        The tally is a FLOOR. It is written after the op file is unlinked, so
        a crash in that window under-counts by at most one op per crash;
        writing it first would over-count instead, and a producer reporting
        more delivered than it ever enqueued reads as a bug rather than as the
        at-least-once delivery it actually is.
        """
        if not producer_id or count <= 0:
            return
        self._ensure_producers_dir()
        with file_lock(self.append_lock):
            record = self._read_producer_locked(producer_id)
            self._update_producer_locked(producer_id, record, delivered=count)

    def seal_producer(self) -> None:
        """Mark this producer cleanly closed. A producer left "open" whose
        process is gone is a crashed writer -- the report shows exactly that."""
        if self._producer_id is None or not self.producers_dir.exists():
            return
        with file_lock(self.append_lock):
            record = self._read_producer_locked(self._producer_id)
            self._update_producer_locked(
                self._producer_id, record, role=self._producer_role, state="closed"
            )

    def producer_report(self) -> list[dict]:
        """Every producer this journal knows: sequence high-water, ``delivered``
        tally, capture gaps, open/closed state. Unparseable records are skipped
        rather than raising -- a report is diagnostics, never a blocker."""
        if not self.producers_dir.exists():
            return []
        out: list[dict] = []
        for path in sorted(self.producers_dir.iterdir()):
            if not path.name.endswith(".json"):
                continue
            try:
                out.append(json.loads(path.read_text()))
            except (OSError, json.JSONDecodeError, ValueError):
                continue
        return out

    # -- reads --------------------------------------------------------------
    @staticmethod
    def _read_dir(directory: Path) -> list[tuple[Path, dict]]:
        if not directory.exists():
            return []
        out: list[tuple[Path, dict]] = []
        for path in sorted(directory.iterdir()):
            if not path.name.endswith(".json"):
                continue
            try:
                out.append((path, json.loads(path.read_text())))
            except (OSError, json.JSONDecodeError):
                continue
        return out

    def pending(self) -> list[tuple[Path, dict]]:
        return self._read_dir(self.ops_dir)

    def failed(self) -> list[tuple[Path, dict]]:
        return self._read_dir(self.failed_dir)

    def run_ops(self, run_ref: str) -> "RunOps":
        """A counter of ONE run's blocking ops that parses each op file once."""
        return RunOps(self, run_ref)

    def outbox_queues(self) -> "list[Journal]":
        """Every queue of the outbox this one belongs to: the root, its receipt
        namespace, and each credential queue (#2035) with its own."""
        root = Journal(self.outbox_root, context=self.context, attribution=self.attribution)
        return root.namespaces()

    def worker_alive(self) -> bool:
        """Whether a worker holds this queue's lease right now (non-blocking)."""
        try:
            handle = (self.dir / ".worker.lock").open("a+")
        except OSError:
            return False
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
        except (BlockingIOError, OSError):
            return True
        else:
            oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            return False
        finally:
            handle.close()

    def own_namespaces(self) -> "list[Journal]":
        """`namespaces` without the credential queues under a root: what the
        root's own worker serves."""
        return [
            queue
            for queue in self.namespaces()
            if queue.dir == self.dir or queue.dir == self.dir / DELIVERY_NAMESPACE
        ]

    def other_queues(self) -> "list[Journal]":
        """`outbox_queues` minus this queue and its own receipt namespace."""
        mine = {self.dir, self.dir / DELIVERY_NAMESPACE}
        return [queue for queue in self.outbox_queues() if queue.dir not in mine]

    def run_ops_elsewhere(self, run_ref: str, *, min_epoch: int | None = None) -> "RunOps":
        """ONE run's blocking ops in the outbox's OTHER queues: writes of the
        same run queued under another credential (#2035), which this queue's
        order cannot see and a close queued here could overtake. ``min_epoch``
        leaves out an older attempt's (round 5)."""
        return RunOps(self, run_ref, queues=self.other_queues(), min_epoch=min_epoch)

    @property
    def paused(self) -> bool:
        """Paused here, or in any queue above this one (`probe outbox pause`
        pauses the root, and with it every namespace under it)."""
        path = self.dir
        while True:
            if (path / "paused").exists():
                return True
            if path.name == DELIVERY_NAMESPACE:
                path = path.parent
            elif path.parent.name == CREDENTIAL_NAMESPACE:
                path = path.parent.parent
            else:
                return False

    def pause(self) -> None:
        self._ensure()
        write_text_atomic(self.paused_file, now_iso() + "\n", mode=0o600)
        with file_lock(self.append_lock):
            self._write_status_locked()

    def resume(self) -> None:
        for child in self.namespaces()[1:]:
            child.resume()
        self.paused_file.unlink(missing_ok=True)
        if self.dir.exists():
            with file_lock(self.append_lock):
                self._write_status_locked()

    def quarantine_corrupt(self) -> int:
        """Move unparseable op files to failed/ so they stay VISIBLE.

        Silently skipping them (codex) let status count files the drain never
        saw: the worker exited 'empty' while the banner re-kicked it forever.
        Quarantined files keep their names -- they count as failed in
        status.json, while the (parse-skipping) readers ignore them.

        The queue is parsed OUTSIDE the append lock (plan 1.9); only the
        corrupt files are re-checked under it (`quarantine_paths`).
        """
        ops, corrupt = self._scan_ops()
        return self.quarantine_paths(corrupt, known=op_meta(ops))

    def _scan_ops(self) -> tuple[list[tuple[Path, dict]], list[Path]]:
        """ONE parse of ``ops/``, taken outside every lock: the ops in FIFO
        order, and the paths that did not parse (for `quarantine_paths`).

        Op files appear by atomic rename, so a file that does not parse is
        corrupt, not half-written. One that vanished between the listing and
        the read was delivered or moved by someone else and is skipped.
        """
        if not self.ops_dir.exists():
            return [], []
        ops: list[tuple[Path, dict]] = []
        corrupt: list[Path] = []
        # Plan 1.6 review: a worker that keeps delivering one run while another
        # sits in its backoff re-scans the parked run's ops every pass; at 20k
        # parked ops that held a core for the whole outage. An op file that has
        # not changed since the last pass (same inode, size, mtime) and that
        # the drain did not attempt (`_scan_forget`) is not parsed again. Only
        # the first `SCAN_CACHE_MAX_BYTES` of op files are kept: the cache
        # outlives the pass, and unbounded it held 58 MB at 20k ops.
        cache = self.__dict__.setdefault("_scan_cache", {})
        seen: dict = {}
        kept = 0
        for name in sorted(n for n in os.listdir(self.ops_dir) if n.endswith(".json")):
            path = self.ops_dir / name
            try:
                stat = os.stat(path)
                stamp = (stat.st_ino, stat.st_size, stat.st_mtime_ns)
                cached = cache.get(name)
                if cached is not None and cached[0] == stamp:
                    op = cached[1]
                else:
                    op = json.loads(path.read_text())
                if kept + stat.st_size <= SCAN_CACHE_MAX_BYTES:
                    seen[name] = (stamp, op)
                    kept += stat.st_size
                ops.append((path, op))
            except FileNotFoundError:
                continue
            except (OSError, json.JSONDecodeError, ValueError):
                corrupt.append(path)
        self._scan_cache = seen
        return ops, corrupt

    def _scan_forget(self, name: str) -> None:
        """The drain is about to attempt this op (it may change it in memory):
        the next pass reads it from disk again."""
        cache = self.__dict__.get("_scan_cache")
        if cache is not None:
            cache.pop(name, None)

    def quarantine_paths(self, paths: list[Path], *, known: dict | None = None) -> int:
        """Move the given op files to failed/ if they STILL do not parse,
        re-checking only them under the append lock. ``known`` (from
        `op_meta`) lets the status recount skip re-parsing the rest."""
        if not paths:
            return 0
        moved = 0
        with file_lock(self.append_lock):
            for path in paths:
                try:
                    json.loads(path.read_text())
                    continue  # parses now: not ours to move
                except FileNotFoundError:
                    continue
                except (OSError, json.JSONDecodeError, ValueError):
                    os.replace(path, self.failed_dir / path.name)
                    moved += 1
            if moved:
                fsync_directory(self.failed_dir)
                fsync_directory(self.ops_dir)
                self._write_status_locked(known=known)
        return moved

    def sweep_stale_temps(self, *, older_than: float = 3600.0) -> int:
        """Remove ``.<name>.<uuid>.tmp`` siblings `write_text_atomic` left
        behind when a writer was killed mid-write, once older than an hour (a
        live write lasts milliseconds). Blob staging has its own sweep in
        `gc_blobs`. Never raises."""
        removed = 0
        cutoff = time.time() - older_than
        for directory in (self.ops_dir, self.failed_dir, self.dir):
            try:
                names = [n for n in os.listdir(directory) if n.startswith(".") and n.endswith(".tmp")]
            except OSError:
                continue
            for name in names:
                try:
                    path = directory / name
                    if path.stat().st_mtime < cutoff:
                        path.unlink()
                        removed += 1
                except OSError:
                    continue
        return removed

    def discard_failed(self, op_id: str | None = None) -> int:
        """Move dead letters (one, or all) to ``discarded/`` -- an audit-safe
        tombstone rather than deletion. Covers quarantined-corrupt files too
        (matched by name when they cannot be parsed), which retry can never
        requeue (red team: without a discard verb they nagged forever)."""
        children_moved = sum(child.discard_failed(op_id) for child in self.namespaces()[1:])
        target = self.failed_dir.parent / "discarded"
        moved = 0
        with file_lock(self.append_lock):
            if self.failed_dir.exists():
                target.mkdir(parents=True, exist_ok=True, mode=0o700)
                for path in sorted(self.failed_dir.iterdir()):
                    if op_id is not None:
                        try:
                            if json.loads(path.read_text()).get("op_id") != op_id:
                                continue
                        except (OSError, json.JSONDecodeError, ValueError):
                            if op_id not in path.name:
                                continue
                    os.replace(path, target / path.name)
                    moved += 1
            if moved:
                fsync_directory(target)
                fsync_directory(self.failed_dir)
                self._write_status_locked()
                self._record_dead_letters()
        if moved:
            self.gc_blobs()
        return moved + children_moved

    def discard_held(self, *, credential: str | None = None) -> int:
        """Move to ``discarded/`` the PENDING ops, in this queue and the ones
        under it, that no credential on this machine will send as things stand:
        a stored login's write whose account is unknown or another account's,
        or one whose own login the API refused while it is still the stored one
        (#2041 round 3/4). Nothing a live process could still deliver is
        touched: another job's `PROBE_TOKEN` or in-code writes stay -- that job
        sends them -- and a login whose account `/v1/me` cannot confirm right
        now is not "held". ``credential`` names a fingerprint (as `probe outbox
        drain` prints it): then that credential's queued writes go too, which
        is how a stranded job's writes are dropped on purpose. An unstamped op
        is never touched. Returns how many moved. Each queue's drain lock is
        taken, so no pass is mid-way through them."""
        moved = 0
        for queue in self.namespaces():
            moved += queue._discard_held_here(credential)
        return moved

    def _discard_held_here(self, credential: str | None) -> int:
        from .config import load_context

        if not self.ops_dir.exists():
            return 0
        status = Journal.read_status(self.dir, include_receipts=False) or {}
        refused = status.get("refused_fingerprints") or {}
        handle = self.drain_lock.open("a+")
        try:
            if not _take_drain_lock(handle, wait_for_lock=True, timeout=30.0):
                return 0
            held: list[Path] = []
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
                if credential and credential in (stamp.get("fingerprint"), stamp.get("ingest_fingerprint")):
                    held.append(path)  # named by the user
                    continue
                if stamp.get("source") != CredentialSource.CONFIG:
                    continue  # another job's: that job sends it
                fingerprint, ingest = op_credential(op)
                if ingest:
                    continue
                if fingerprint in refused:
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
            if not held:
                return 0
            target = self.dir / "discarded"
            with file_lock(self.append_lock):
                target.mkdir(parents=True, exist_ok=True, mode=0o700)
                for path in held:
                    try:
                        os.replace(path, target / path.name)
                    except FileNotFoundError:
                        continue  # delivered meanwhile
                    self._scan_forget(path.name)
                fsync_directory(target)
                fsync_directory(self.ops_dir)
                self._write_status_locked(held=0, held_at=None)
        finally:
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_UN)
            finally:
                handle.close()
        self.gc_blobs()
        return len(held)

    def clear_auth_block(self) -> None:
        """Forget a recorded auth block (after re-login / explicit retry) so
        the wake-on-enqueue drainer starts spawning again (codex: nothing
        cleared it, so delivery stayed stopped forever after one 401)."""
        for child in self.namespaces()[1:]:
            child.clear_auth_block()
        self.write_status(auth_blocked_since=None, refused_fingerprints={}, held=0, held_at=None)
        try:  # a worker sleeping on held runs looks again now (outbox_worker._wake_stamp)
            write_text_atomic(self.dir / ".wake", now_iso() + "\n", mode=0o600)
        except OSError:
            pass

    def retry_failed(
        self, op_id: str | None = None, *, run_ref: str | None = None
    ) -> int:
        """Requeue dead letters (one op, one run's, or all). Files keep their
        names, so a retried op re-enters at its original FIFO position."""
        children_moved = sum(
            child.retry_failed(op_id, run_ref=run_ref) for child in self.namespaces()[1:]
        )
        moved = 0
        with file_lock(self.append_lock):
            for path, op in self._read_dir(self.failed_dir):
                if op_id is not None and op.get("op_id") != op_id:
                    continue
                if run_ref is not None and op.get("run_ref") != run_ref:
                    continue
                if "first_failed_at" in op:
                    # A human asked for another try: the transient budget's
                    # clock restarts, or an op dead-lettered by the budget
                    # would be dead-lettered again by its first failure.
                    op.pop("first_failed_at", None)
                    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                os.replace(path, self.ops_dir / path.name)
                moved += 1
            if moved:
                fsync_directory(self.ops_dir)
                fsync_directory(self.failed_dir)
                self._write_status_locked()
                self._record_dead_letters()
        return moved + children_moved

    # -- status -------------------------------------------------------------
    @staticmethod
    def _count_dir(directory: Path) -> tuple[int, str | None]:
        """(count, first filename) without parsing op bodies -- this runs on
        EVERY append, so it must stay O(directory listing), not O(total bytes
        queued) (perf review: a training loop enqueuing offline was O(N^2))."""
        if not directory.exists():
            return 0, None
        names = sorted(n for n in os.listdir(directory) if n.endswith(".json"))
        return len(names), names[0] if names else None

    def _write_status_locked(
        self,
        *,
        unstaged_low_disk: int = 0,
        recount: bool = True,
        pending_delta: int = 0,
        pending_bytes_delta: int = 0,
        enqueued_at: str | None = None,
        set_pending: int | None = None,
        known: dict | None = None,
        sync: str = SYNC_FULL,
        new_dead_letters: list | None = None,
        **extra: Any,
    ) -> int:
        """Rewrite status.json; returns the pending count it wrote.
        ``recount=False`` is the APPEND path. ``set_pending`` (with
        ``recount=False``) stores a count the caller just took from a directory
        listing, without re-parsing any op body.

        A recount lists the directories (names only) and parses only the op
        files ``known`` (`op_meta`: name -> (size_bytes, enqueued_at), taken by
        the caller OUTSIDE the lock) does not cover -- the tail appended since
        (plan 1.9). A drain pass used to re-parse the whole queue here while
        holding the append lock, so every `log()` waited: 3.3 s at 20k ops.

        The counts used to come from ``_count_dir`` on every append, and that
        listdir is what made N enqueues O(N^2 log N) -- measured 1.19ms/append
        at depth 1 rising to 6.50ms at 8k, i.e. the queue got slower to write
        exactly as the outage it exists to survive got longer. The docstring on
        ``_count_dir`` claimed O(1) because it stopped PARSING bodies; the
        LISTING was still O(N).

        So an append carries its own delta forward instead of recounting, and
        the DRAIN -- which already walks both directories -- writes the
        authoritative numbers. status.json is explicitly banner-grade (see
        ``read_status``), so a count that is briefly off after a hard kill is
        acceptable; a training loop that slows down under backlog is not.
        """
        previous: dict = {}
        try:
            previous = json.loads(self.status_file.read_text())
        except (OSError, json.JSONDecodeError):
            pass
        if recount:
            names = (
                sorted(n for n in os.listdir(self.ops_dir) if n.endswith(".json"))
                if self.ops_dir.exists()
                else []
            )
            pending_count = len(names)
            failed_count, _ = self._count_dir(self.failed_dir)
            pending_bytes = 0
            oldest = None
            for index, name in enumerate(names):
                meta = (known or {}).get(name)
                if meta is None:
                    try:
                        meta = _meta_of(json.loads((self.ops_dir / name).read_text()))
                    except (OSError, json.JSONDecodeError, ValueError, AttributeError):
                        meta = (0, None)
                pending_bytes += meta[0]
                if index == 0:
                    oldest = meta[1]
        else:
            pending_count = (
                max(0, set_pending)
                if set_pending is not None
                else max(0, int(previous.get("pending") or 0) + pending_delta)
            )
            failed_count = int(previous.get("failed") or 0)
            pending_bytes = max(0, int(previous.get("pending_bytes") or 0) + pending_bytes_delta)
            oldest = previous.get("oldest_pending")
            if pending_count == 0:
                oldest = None
            elif not oldest and pending_delta > 0:
                # First op onto an empty queue: this append IS the oldest.
                oldest = enqueued_at
        status = {
            "schema": SCHEMA,
            "updated_at": now_iso(),
            "pending": pending_count,
            "pending_bytes": pending_bytes,
            "failed": failed_count,
            "oldest_pending": oldest,
            "paused": self.paused,
            "auth_blocked_since": previous.get("auth_blocked_since"),
            # Per-credential refusals (#2041 review): fingerprint -> when the
            # API last refused it. Carried like the block above.
            "refused_fingerprints": previous.get("refused_fingerprints") or {},
            # Ops the last drain pass had to leave held (another credential, a
            # refused one, a close waiting on another queue) and when: a kick
            # that adds nothing deliverable need not fork a worker (#2041
            # round 3). Carried like the fields around it.
            "held": int(previous.get("held") or 0),
            "held_at": previous.get("held_at"),
            "last_error": previous.get("last_error"),
            # Monotonic tally of uploads that DEGRADED to unstaged for want of
            # disk headroom -- carried forward like the two fields above.
            # Counting them by scanning ops instead would make every append
            # O(queue), which is exactly the regression the O(1) status
            # rewrite fixed.
            "unstaged_low_disk": (
                int(previous.get("unstaged_low_disk") or 0) + int(unstaged_low_disk)
            ),
        }
        status.update(extra)
        if recount or extra:
            # An APPEND's status carries only numbers, timestamps this module
            # minted and the fields above copied from the previous status.json,
            # which was scrubbed when it was written: scrubbing it again was one
            # of four full scrubs per `log()` (plan 1.3). New text can arrive
            # only through `extra` or a drain's recount.
            status = default_scrub(status)
        if new_dead_letters:
            self._record_dead_letters(new_dead_letters)
        # Compact: `indent=` takes json's pure-Python encoder, and every append
        # rewrites this file (review of #2055).
        write_text_atomic(
            self.status_file, json.dumps(status, separators=(",", ":")) + "\n", mode=0o600,
            sync=sync
        )
        return pending_count

    @property
    def dead_letters_file(self) -> Path:
        return self.dir / "dead_letters.json"

    def recent_dead_letters(self) -> list[dict]:
        """The last `_RECENT_DEAD_LETTERS` dead letters (`{run_ref, op_id,
        error, status}`, errors redacted at the source) for a training process
        to say so while it runs (plan 1.7). Their own file, written only by
        the drain and the dead-letter commands: in status.json every append
        re-read and rewrote them (review of #2055: 15 KB, 179 -> 511 us)."""
        try:
            records = json.loads(self.dead_letters_file.read_text())
        except (OSError, ValueError):
            return []
        return [r for r in records if isinstance(r, dict)] if isinstance(records, list) else []

    def _record_dead_letters(self, new: list[dict] | None = None) -> None:
        """Append ``new`` and forget entries whose op is no longer a dead
        letter (retried or discarded). Under the append lock."""
        try:
            present = {
                name for name in os.listdir(self.failed_dir) if name.endswith(".json")
            } if self.failed_dir.exists() else set()
        except OSError:
            present = None
        kept = self.recent_dead_letters() + list(new or [])
        if present is not None:
            # A record names its op, not its file: keep those whose op id still
            # names a file in failed/ (the name ends in "-<op_id>.json").
            ids = {name.rsplit("-", 1)[-1][: -len(".json")] for name in present}
            kept = [r for r in kept if str(r.get("op_id")) in ids]
        kept = kept[-_RECENT_DEAD_LETTERS:]
        try:
            if kept:
                write_text_atomic(
                    self.dead_letters_file,
                    json.dumps(kept, separators=(",", ":")) + "\n",
                    mode=0o600,
                    sync=SYNC_NONE,
                )
            else:
                self.dead_letters_file.unlink(missing_ok=True)
        except OSError:
            pass

    def write_status(self, **extra: Any) -> None:
        self._ensure()
        with file_lock(self.append_lock):
            self._write_status_locked(**extra)

    @staticmethod
    def read_status(
        directory: str | Path | None = None,
        *,
        include_receipts: bool = True,
        credential_queues: bool = True,
    ) -> dict | None:
        """Banner-grade counts, including the fenced delivery namespace and
        (``credential_queues``) every credential queue under this root."""
        root = Path(directory).expanduser() if directory else default_dir()
        path = root / "status.json"
        try:
            status = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError, ValueError):
            status = None
        if include_receipts and root.name != DELIVERY_NAMESPACE:
            child = Journal.read_status(root / DELIVERY_NAMESPACE, include_receipts=False)
            if child:
                status = dict(status or {})
                for field in ("pending", "pending_bytes", "failed"):
                    status[field] = int(status.get(field) or 0) + int(child.get(field) or 0)
                status["delivery_pending"] = int(child.get("pending") or 0)
                status["delivery_failed"] = int(child.get("failed") or 0)
                status["delivery_pending_bytes"] = int(child.get("pending_bytes") or 0)
                status["delivery_paused"] = bool(child.get("paused"))
                status["delivery_last_error"] = child.get("last_error")
                status["auth_blocked_since"] = status.get("auth_blocked_since") or child.get(
                    "auth_blocked_since"
                )
                status["paused"] = bool(status.get("paused") or (root / "paused").exists())
        if root.name != DELIVERY_NAMESPACE:
            waiting = Journal.count_waiting(root)
            if waiting or status is not None:
                status = dict(status or {})
                status["waiting"] = waiting
        if (
            include_receipts
            and credential_queues
            and root.name != DELIVERY_NAMESPACE
            and root.parent.name != CREDENTIAL_NAMESPACE
        ):
            # The credential queues (#2035) count toward the root's banner.
            for path in _credential_queue_dirs(root):
                child = Journal.read_status(path, include_receipts=True)
                if not child:
                    continue
                status = dict(status or {})
                for field in ("pending", "pending_bytes", "failed", "waiting"):
                    status[field] = int(status.get(field) or 0) + int(child.get(field) or 0)
                oldest = [v for v in (status.get("oldest_pending"), child.get("oldest_pending")) if v]
                status["oldest_pending"] = min(oldest) if oldest else None
                status["auth_blocked_since"] = status.get("auth_blocked_since") or child.get(
                    "auth_blocked_since"
                )
                child_refused = child.get("refused_fingerprints")
                if isinstance(child_refused, dict) and child_refused:
                    # A refused credential's queue is the one that holds its
                    # writes: the root's banner must see it (`auth_blocked_since`).
                    merged = dict(status.get("refused_fingerprints") or {})
                    for fp, at in child_refused.items():
                        merged[fp] = min(str(at), str(merged[fp])) if merged.get(fp) else at
                    status["refused_fingerprints"] = merged
                status["last_error"] = status.get("last_error") or child.get("last_error")
        return status

    # -- blob store ---------------------------------------------------------
    def blob_path(self, op: dict) -> Path | None:
        upload = op.get("upload") or {}
        if not upload.get("staged"):
            return None
        if upload.get("blob"):
            return self.blobs_dir / upload["blob"]
        return self.blobs_dir / f"incoming-{op['op_id']}"

    def gc_blobs(self, *, staging_grace_seconds: float = 86_400.0) -> int:
        """Drop blobs no live or dead op references. Liveness is computed, not
        counted -- crash-safe by construction. The reference scan happens
        INSIDE the append lock (codex: a stale reference set computed before
        the lock could delete a blob published while gc waited). Crash-orphaned
        ``.staging-*`` files older than the grace window are swept too, so an
        interrupted enqueue cannot leak a multi-GB snapshot forever."""
        children_removed = sum(
            child.gc_blobs(staging_grace_seconds=staging_grace_seconds)
            for child in self.namespaces()[1:]
        )
        if not self.blobs_dir.exists():
            return children_removed
        removed = 0
        with file_lock(self.append_lock):
            referenced: set[str] = set()
            for _, op in self.pending() + self.failed():
                upload = op.get("upload") or {}
                if upload.get("staged"):
                    # BOTH possible names stay referenced: mid-drain, an op
                    # whose digest was just persisted may still hold its bytes
                    # under the incoming staging name (red team).
                    referenced.add(f"incoming-{op['op_id']}")
                    if upload.get("blob"):
                        referenced.add(upload["blob"])
            # An interrupted append can publish the intent before the op file.
            # Preserve that immutable snapshot until a terminal receipt exists.
            if self.receipt_enabled:
                for intent_path in self.intents_dir.glob("*.json"):
                    intent = self._read_record(intent_path)
                    if (
                        intent
                        and not (self.dir / "discarded" / intent["op"]["queue_filename"]).exists()
                    ):
                        upload = intent["op"].get("upload") or {}
                        if upload.get("blob"):
                            referenced.add(upload["blob"])
            cutoff = time.time() - staging_grace_seconds
            for path in self.blobs_dir.iterdir():
                # `in`, not `startswith`: snapshot_file writes its own temp as
                # `.{dst.name}.{uuid}.tmp`, so staging a blob named
                # `.staging-<op>` produces `..staging-<op>.<uuid>.tmp` -- a
                # DOUBLED dot that the prefix test missed and the dotfile skip
                # below then swallowed. A SIGKILL mid-copy therefore leaked a
                # checkpoint-sized file that nothing would ever collect, which
                # is exactly the case the grace sweep was written for. Blob
                # names are hex digests, so they cannot collide with this.
                if ".staging-" in path.name:
                    try:
                        if path.stat().st_mtime < cutoff:
                            path.unlink(missing_ok=True)
                            removed += 1
                    except OSError:
                        pass
                    continue
                if path.name.startswith("."):
                    continue
                if path.name not in referenced:
                    path.unlink(missing_ok=True)
                    removed += 1
        return removed + children_removed

    # -- legacy spool import -------------------------------------------------
    def import_spool(self, spool=None) -> int:
        """Fold a surviving pre-journal spool into the journal, in order.

        The spool's two-file protocol is honored by reading inflight first --
        exactly the order ``Spool.flush`` would have replayed. Records import
        with the CURRENT context pin (the spool never recorded one) and the
        spool files are removed, so this runs once per machine, ever.
        """
        from .spool import Spool

        spool = spool or Spool()
        if not (spool.file.exists() or spool.inflight_file.exists()):
            return 0
        if self.context is None:
            # Stamp the records with the context that is current AT IMPORT
            # TIME (red team: a null pin resolves at drain time, so a context
            # switch in between would deliver the old spool's writes to a
            # different tenant than the one that captured them).
            from .config import current_context_name, resolve

            self.context = {
                "name": current_context_name() or None,
                "base_url": resolve().base_url,
            }
        imported = 0
        with file_lock(spool.lock_file):
            # NOT spool.pending(): that takes the same lock we already hold,
            # and flock is not reentrant across file handles.
            records = spool._read_records(spool.inflight_file) + spool._read_records(
                spool.file
            )
            for record in records:
                self.append_http(record.method, record.path, record.json_body)
                imported += 1
            spool.file.unlink(missing_ok=True)
            spool.inflight_file.unlink(missing_ok=True)
        return imported


_URL_QUERY = re.compile(r"\?\S+")


def _redact(text: str) -> str:
    """Strip query strings from URLs embedded in error text. A presigned PUT
    URL's query IS a signed, bearer-equivalent write capability; transport
    errors embed the full URL, and last_error is persisted to op files,
    status.json, doctor output, and the drainer log (security review)."""
    return scrub_text(_URL_QUERY.sub("?<redacted>", text))


def _settings_for(context: dict | None):
    from .config import DEFAULT_BASE_URL, Settings, load_context, resolve

    name = (context or {}).get("name")
    pinned = (context or {}).get("base_url")
    settings = resolve(context=name)
    stored = load_context(name)
    if pinned and pinned.rstrip("/") != settings.base_url.rstrip("/"):
        # Ambient resolution (env vars outrank the context file) produced a
        # credential for a DIFFERENT endpoint than this op was enqueued for.
        # Never mix: a token issued for endpoint A must not be sent to pinned
        # host B (security review). Use only the named context's stored record
        # for the pinned endpoint; auth-block when none matches.
        stored_base = (stored.get("base_url") or DEFAULT_BASE_URL).rstrip("/")
        if stored_base == pinned.rstrip("/") and (
            stored.get("token") or stored.get("ingest_token")
        ):
            return Settings(
                base_url=pinned.rstrip("/"),
                token=stored.get("token"),
                ingest_token=stored.get("ingest_token"),
                hmac_secret=stored.get("hmac_secret"),
            )
        if stored and stored_base != pinned.rstrip("/"):
            # A context record EXISTS and names a different endpoint: no login
            # for this context can ever produce a credential for the pinned one
            # (refusing to mix them is the whole point), so this op is
            # undeliverable from this machine and must not park the queue.
            raise errors.UnroutableEndpointError(
                f"pinned endpoint {pinned} is not what context "
                f"{name or '<default>'} names ({stored_base}), and no stored "
                "credential matches it -- this op cannot be delivered from here"
            )
        # No record at all, or a record for THIS endpoint carrying no
        # credential: the researcher is simply logged out, signing in again
        # recovers it, and their queued work must be parked and kept rather
        # than dead-lettered. A self-hosted user mid-logout is otherwise
        # byte-for-byte indistinguishable from a dead ephemeral test port.
        raise errors.AuthError(
            f"no stored credential for pinned endpoint {pinned} "
            f"(context {name or '<default>'}); {WIZARD_HINT}"
        )
    if pinned:
        settings.base_url = pinned.rstrip("/")
    # Same endpoint, but the pinned context STORES its own credential: the
    # stored token outranks any ambient PROBE_TOKEN for a drain. Tenants can
    # share one API URL, and a detached worker inheriting another account's
    # env must not replay this context's ops under the wrong principal
    # (codex). Env credentials still serve contexts that store none.
    if stored.get("token"):
        settings.token = stored.get("token")
    if stored.get("ingest_token"):
        settings.ingest_token = stored.get("ingest_token")
    return settings


class CredentialSource(StrEnum):
    """Where the credential that queued an op came from (#2035)."""

    #: ``PROBE_TOKEN`` / ``PROBE_INGEST_TOKEN`` in the writer's environment.
    ENV = "env"
    #: The writer's context's stored login.
    CONFIG = "config"
    #: Anything else: a token passed in code, or another context's login.
    CODE = "code"


def credential_fingerprint(token: str | None, ingest_token: str | None) -> str | None:
    """A short, one-way name for the credential that queued an op, so the op
    can say WHICH credential it was without carrying it. 64 bits of a SHA-256
    over a token that is itself long and random: enough to tell two apart,
    useless for recovering it.

    The bearer token when there is one, else the ingest token -- never the
    pair. A ``PROBE_TOKEN`` job's settings pick up the stored login's ingest
    token, so a pair fingerprint changed whenever that login re-logged in, and
    the job's queued writes matched no drainer any more (#2041 review)."""
    secret = token or ingest_token
    if not secret:
        return None
    digest = hashlib.sha256(b"probe.outbox.credential/2\0")
    digest.update(("token\0" if token else "ingest\0").encode())
    digest.update(secret.encode("utf-8", "backslashreplace"))
    return digest.hexdigest()[:16]


def stamp_identity(stamp: dict | None) -> tuple[str, str] | None:
    """(customer_id, user_id) the stamp says queued the op, when recorded."""
    if isinstance(stamp, dict) and stamp.get("customer_id") and stamp.get("user_id"):
        return str(stamp["customer_id"]), str(stamp["user_id"])
    return None


class CredentialNotHere(OpHeldHere):
    """This drainer holds no credential it may deliver the op with.

    Not a failure of the op: it stays queued, untouched, for a process that
    does hold that credential -- the writer's own ``flush()``/``finish()`` or
    exporter, or a worker started with the same ``PROBE_TOKEN``. Delivering it
    with whatever credential IS here would write it as someone else (#2035).

    ``permanent``: no credential on this machine will ever match it as things
    stand -- a stored login's write whose account is unknown, or another
    account's (#2041 round 4). Only those are dropped by `probe outbox
    discard --held`; another job's `PROBE_TOKEN` writes are that job's to send.
    """

    def __init__(self, message: str = "", *, permanent: bool = False):
        super().__init__(message)
        self.permanent = permanent


#: `_identity_of` answers, per token fingerprint: (answer or exception, when).
#: A pass runs every fraction of a second in an exporter; the account behind a
#: token does not change that fast (#2041 re-review: 43 `/v1/me` in 8 s).
_IDENTITY_CACHE: dict[tuple[str, str], tuple[Any, float]] = {}
_IDENTITY_TTL_SECONDS = 300.0
_IDENTITY_ERROR_TTL_SECONDS = 60.0


def _identity_of(settings, transport=None) -> tuple[str, str] | None:
    """(customer_id, user_id) ``settings.token`` belongs to, per `GET /v1/me`:
    one attempt, 5 s, cached per endpoint and token for 5 minutes (a failure
    for one). ``transport`` is one that already carries that token (a
    drainer's client's own); otherwise one is built from ``settings``.
    Raises what the request raised."""
    from .transport import Transport

    key = (str(settings.base_url or "").rstrip("/"), credential_fingerprint(settings.token, None) or "")
    cached = _IDENTITY_CACHE.get(key)
    if cached is not None:
        answer, at = cached
        ttl = _IDENTITY_ERROR_TTL_SECONDS if isinstance(answer, BaseException) else _IDENTITY_TTL_SECONDS
        if time.monotonic() - at < ttl:
            if isinstance(answer, BaseException):
                raise answer
            return answer
    owned = transport is None
    if owned:
        transport = Transport(settings, max_retries=0)
    try:
        response = transport.request("GET", "/v1/me", idempotent=True, timeout=5.0)
        who = response.json() if response.content else {}
    except Exception as exc:
        _IDENTITY_CACHE[key] = (exc, time.monotonic())
        raise
    finally:
        if owned:
            transport.close()
    answer = (
        (str(who["customer_id"]), str(who["user_id"]))
        if who.get("customer_id") and who.get("user_id")
        else None
    )
    _IDENTITY_CACHE[key] = (answer, time.monotonic())
    return answer


#: How many token -> account records `record_account` keeps (newest win).
_ACCOUNTS_KEPT = 256


def _accounts_path() -> Path:
    """Which account each credential fingerprint belongs to, machine-wide:
    `<state>/probe/credential-accounts.json`. Outside the outbox on purpose --
    outboxes are per rank and per `PROBE_OUTBOX_DIR`, while an account learned
    anywhere vouches everywhere. Ids only (team and user), never a token."""
    base = os.environ.get("XDG_STATE_HOME")
    root = Path(base) if base else homedir.home() / ".local" / "state"
    return root / "probe" / "credential-accounts.json"


def record_account(fingerprint: str | None, account: tuple[str, str] | None) -> None:
    """Remember that the credential named ``fingerprint`` is ``account``.

    Written by the wizard's sign-in, a job's heartbeat lookup and a
    drain that just delivered with a stored login (#2041 round 3): a write
    queued under a login whose account nobody recorded at the time can then
    still follow a same-account re-login instead of waiting forever. Never
    raises: this is evidence, not a step in delivery."""
    if not fingerprint or not account or not all(account):
        return
    path = _accounts_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with file_lock(path.with_suffix(".lock")):
            try:
                records = json.loads(path.read_text())
            except (OSError, ValueError):
                records = {}
            if not isinstance(records, dict):
                records = {}
            entry = {"customer_id": str(account[0]), "user_id": str(account[1]), "at": now_iso()}
            if {k: v for k, v in (records.get(fingerprint) or {}).items() if k != "at"} == {
                k: v for k, v in entry.items() if k != "at"
            }:
                return
            records[fingerprint] = entry
            if len(records) > _ACCOUNTS_KEPT:
                newest = sorted(records.items(), key=lambda kv: str((kv[1] or {}).get("at")))
                records = dict(newest[-_ACCOUNTS_KEPT:])
            write_text_atomic(path, json.dumps(records, indent=2) + "\n", mode=0o600)
    except Exception:  # noqa: BLE001 -- see docstring
        return


def recorded_account(fingerprint: str | None) -> tuple[str, str] | None:
    """The account `record_account` remembered for ``fingerprint``, or None."""
    if not fingerprint:
        return None
    try:
        entry = (json.loads(_accounts_path().read_text()) or {}).get(fingerprint) or {}
    except (OSError, ValueError, AttributeError):
        return None
    if isinstance(entry, dict) and entry.get("customer_id") and entry.get("user_id"):
        return str(entry["customer_id"]), str(entry["user_id"])
    return None


def is_ingest_path(path: str | None) -> bool:
    """Whether a request goes out with the INGEST token (`Transport._auth_headers`)."""
    return bool(path) and str(path).startswith("/ingest")


def op_credential(op: dict) -> tuple[str | None, bool]:
    """(fingerprint, is_ingest) of the credential ``op`` must be delivered with.

    An `/ingest` request is authenticated with the ingest token, everything
    else with the personal token (`Transport._auth_headers`), so a write names
    whichever of the two its route uses (#2041 re-review): matching the
    personal token for an ingest write let a drainer send it with ITS OWN
    ingest token."""
    stamp = (op.get("context") or {}).get("principal") if isinstance(op, dict) else None
    if not isinstance(stamp, dict):
        return None, False
    ingest = op.get("kind") == "http" and is_ingest_path(op.get("path"))
    key = stamp.get("ingest_fingerprint") if ingest else stamp.get("fingerprint")
    return (str(key) if key else None), ingest


def _route_fingerprint(settings, ingest: bool) -> str | None:
    """The fingerprint of the key ``settings`` would send on that route."""
    if ingest:
        return credential_fingerprint(None, settings.ingest_token)
    return credential_fingerprint(settings.token, settings.ingest_token)


def _settings_for_op(
    context: dict | None, *, ingest: bool = False, account: tuple[str, str] | None = None
):
    """The credential to deliver an op with: the one that queued it, or none.

    An op stamped with a credential (``context["principal"]``, #2035) goes out
    only with a key whose fingerprint matches the one its ROUTE uses -- the
    ingest token for an `/ingest` write (``ingest``), the personal token for
    the rest -- from whichever of the two this drainer can build: what a client
    started in THIS environment would hold (a worker the job spawned inherits
    its ``PROBE_TOKEN``), or the context's stored login. An env or in-code
    credential has no fallback: anything else here may be another person's,
    so the op waits (`CredentialNotHere`).

    One queued under the stored login may also go out with that context's
    CURRENT stored login -- a re-login mints a new token, and signing in
    promises to un-block queued writes -- but only when `GET /v1/me` with the
    new token names the same team and user that queued it: the stamp's
    account, or ``account`` (the same token's account learned from another of
    its writes; one token is one account). Without either, or with another
    account, the op waits. Never an environment token; never for an ingest
    write, whose key `/v1/me` cannot vouch for.

    An op queued before stamping keeps the old rule, `_settings_for`.
    """
    stamp = (context or {}).get("principal")
    if not isinstance(stamp, dict) or not stamp.get("fingerprint"):
        return _settings_for(context)
    wanted = stamp.get("ingest_fingerprint") if ingest else stamp.get("fingerprint")
    if not wanted:
        raise CredentialNotHere(
            "queued for the ingest route by a client that had no ingest token; nothing may "
            "send it with another one"
        )
    from .config import load_context, resolve

    name = (context or {}).get("name")
    pinned = ((context or {}).get("base_url") or "").rstrip("/")
    try:
        ambient = resolve(context=name)
    except Exception:  # noqa: BLE001 -- an unreadable config is just no candidate
        ambient = None
    if (
        ambient is not None
        and (not pinned or ambient.base_url.rstrip("/") == pinned)
        and _route_fingerprint(ambient, ingest) == wanted
    ):
        if pinned:
            ambient.base_url = pinned
        return ambient
    try:
        stored = _settings_for(context)
        failure = None
    except Exception as exc:  # noqa: BLE001 -- raised below only where it applies
        stored, failure = None, exc
    if stored is not None and _route_fingerprint(stored, ingest) == wanted:
        return stored
    if stamp.get("source") != CredentialSource.CONFIG or ingest:
        raise CredentialNotHere(
            f"queued with a credential from {stamp.get('source') or 'elsewhere'} "
            f"(fingerprint {wanted}) that this process does not hold; it is delivered by the "
            "process that queued it, or by `probe outbox drain` run with the same credential"
        )
    if failure is not None:
        raise failure
    record = load_context(name)
    if not (record.get("token") or record.get("ingest_token")):
        # Logged out since: park until a sign-in, exactly as an unstamped op
        # would -- but never hand this op to an environment token instead.
        raise errors.AuthError(
            f"no stored credential for context {name or '<default>'} ({WIZARD_HINT})"
        )
    # The stored login outranks the environment field by field in
    # `_settings_for`; a field the login does not store must not be filled in
    # from someone else's environment either.
    stored.token = record.get("token")
    stored.ingest_token = record.get("ingest_token")
    queued_as = stamp_identity(stamp) or account or recorded_account(stamp.get("fingerprint"))
    if queued_as is None:
        raise CredentialNotHere(
            f"queued under an earlier login of context {name or '<default>'} whose account "
            "was never recorded, so the login stored now cannot be matched to it",
            permanent=True,
        )
    try:
        now_as = _identity_of(stored)
    except errors.AuthError:
        raise  # the new login is refused too: set aside with the rest of its writes
    except Exception as exc:  # noqa: BLE001 -- cannot confirm: wait, never guess
        raise CredentialNotHere(
            f"could not confirm the account of context {name or '<default>'}'s login "
            f"({type(exc).__name__}); the write waits"
        ) from exc
    if now_as != queued_as:
        raise CredentialNotHere(
            f"queued under another account than the one logged in to context "
            f"{name or '<default>'} now; it waits for that account's login",
            permanent=True,
        )
    return stored


#: How long a run's close waits for the run's writes queued under another
#: credential (`drain`). Past it the close goes: a run left open forever over
#: writes nothing here may send is worse than a close that lands first. Under
#: the server's reaper window (900 s stale + up to 120 s between sweeps), so a
#: held close lands before the run can be marked crashed (#2041 round 5).
CLOSE_HOLD_MAX_SECONDS = 600.0

_RUN_CLOSE_PATH = re.compile(r"/v1/runs/[^/]+")
_RUN_RELEASE_PATH = re.compile(r"/v1/runs/[^/]+/writers/[^/]+/release")
_TERMINAL_RUN_STATUSES = frozenset({"completed", "failed", "crashed", "canceled", "untracked"})


def _is_run_close(op: dict) -> bool:
    """Whether ``op`` closes its run: a terminal status write (`Run.set_status`,
    `Run._queue_deferred_finish`, `probe run end --async`) or, on a `leases`
    run (2.8), a writer's lease release, from which the server closes the run
    (#2041 round 6: a release went out ahead of the run's writes queued under
    another credential, and the run read completed without them)."""
    if op.get("kind") != "http":
        return False
    path = str(op.get("path") or "")
    if op.get("method") == "PATCH" and _RUN_CLOSE_PATH.fullmatch(path):
        return (op.get("body") or {}).get("status") in _TERMINAL_RUN_STATUSES
    return op.get("method") == "POST" and bool(_RUN_RELEASE_PATH.fullmatch(path))


def _write_epoch_of(op: dict) -> int | None:
    """The write epoch an op carries (its body's ``write_epoch``), or None."""
    body = op.get("body") if isinstance(op, dict) else None
    value = body.get("write_epoch") if isinstance(body, dict) else None
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _close_hold_left(op: dict) -> float | None:
    """Seconds until ``op``'s close hold expires, or None when unknown."""
    from datetime import datetime, timezone

    try:
        queued = datetime.fromisoformat(str(op.get("enqueued_at") or ""))
    except ValueError:
        return None
    if queued.tzinfo is None:
        queued = queued.replace(tzinfo=timezone.utc)
    return CLOSE_HOLD_MAX_SECONDS - (datetime.now(timezone.utc) - queued).total_seconds()


def _close_hold_expired(op: dict) -> bool:
    from datetime import datetime, timezone

    try:
        queued = datetime.fromisoformat(str(op.get("enqueued_at") or ""))
    except ValueError:
        return True
    if queued.tzinfo is None:
        queued = queued.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - queued).total_seconds() > CLOSE_HOLD_MAX_SECONDS


#: How long a refused credential's writes are set aside before one retry. The
#: same bound the worker's box-wide auth block uses (outbox_worker).
CREDENTIAL_RETRY_COOLDOWN_SECONDS = 300.0


def _stamp_fingerprint(op: dict | None) -> str | None:
    """The fingerprint of the key ``op`` is delivered with (see `op_credential`)."""
    return op_credential(op or {})[0]


def _cooling_refusals(journal: "Journal") -> dict[str, str]:
    """Refused credentials still inside their cooldown, from status.json."""
    from datetime import datetime, timezone

    status = Journal.read_status(journal.dir, include_receipts=False) or {}
    recorded = status.get("refused_fingerprints")
    cooling: dict[str, str] = {}
    if not isinstance(recorded, dict):
        return cooling
    now = datetime.now(timezone.utc)
    for refused, since in recorded.items():
        try:
            at = datetime.fromisoformat(str(since))
        except ValueError:
            continue
        if at.tzinfo is None:
            at = at.replace(tzinfo=timezone.utc)
        if (now - at).total_seconds() < CREDENTIAL_RETRY_COOLDOWN_SECONDS:
            cooling[str(refused)] = str(since)
    return cooling


def _record_upload_fallback(journal: "Journal", client: Any, op: dict) -> bool:
    """Record a reference artifact for an upload the server refused for good.

    Returns whether the row actually landed. The caller uses that to decide
    whether the op may stop blocking the run's close: a recorded file is a
    resolved op, an unrecorded one is a real loss and must stay blocking.

    The synchronous upload path already does this: on a permanent rejection it
    writes an `is_reference` row carrying the local path and `meta.upload =
    "failed"`, which `check_run` counts as a capture gap. That row is the only
    record the run has of the file, so losing it loses the fact that the file
    ever existed -- and the drainer had no equivalent, meaning a queued upload
    that was rejected produced an outbox dead letter and nothing else.

    Best-effort by construction: this runs while handling a failure, so it may
    not raise. A dead letter with no fallback row is still strictly better than
    a drain that dies mid-pass.
    """
    shaped = _upload_fallback_request(op)
    if shaped is None:
        return False  # only runs carry the reference-artifact shape
    path, body = shaped
    try:
        client.transport.request("POST", path, json_body=body)
    except Exception:  # noqa: BLE001 -- a fallback may never break the drain
        return False
    return True


def _upload_fallback_request(op: dict) -> tuple[str, dict] | None:
    """(path, body) of the reference row `_record_upload_fallback` writes for
    an upload op, or None for an op that has no run to write it on."""
    upload = op.get("upload") or {}
    anchor, anchor_id = upload.get("anchor"), upload.get("anchor_id")
    if anchor != "run" or not anchor_id or not upload.get("name"):
        return None
    source = upload.get("src_path") or ""
    body = {
        "kind": upload.get("kind") or "file",
        "name": upload["name"],
        "uri": f"file://{source}" if source else None,
        "content_hash": upload.get("blob"),
        "size_bytes": upload.get("size_bytes"),
        "content_type": upload.get("content_type"),
        "is_reference": True,
        "span_id": upload.get("span_id"),
        "step_index": upload.get("step_index"),
        "meta": {
            **(upload.get("meta") or {}),
            "local_path": source,
            "upload": "failed",
            "upload_error": op.get("last_error"),
        },
        "notes": upload.get("notes"),
    }
    return f"/v1/runs/{anchor_id}/artifacts", {k: v for k, v in body.items() if v is not None}


def _upload_workers() -> int:
    """How many upload bodies move at once. 1 restores the strictly serial drain."""
    raw = os.environ.get("PROBE_UPLOAD_WORKERS")
    if raw:
        try:
            return max(1, min(int(raw), 32))
        except ValueError:
            pass
    return 4


#: Ops looked at per parallel window, as a multiple of the worker count. Bounded
#: because a window is read into memory and because the serial loop behind it
#: still decides everything -- a larger window buys nothing once the link is
#: saturated, and costs re-work when the pass stops early.
UPLOAD_WINDOW_FACTOR = 4
#: Op-file bytes whose parsed ops a journal keeps between drain passes (see
#: `Journal._scan_ops`): about 4,300 one-point `log()` writes. Parsed, an op
#: takes 4-7x its file size; uncapped, 20k queued one-point ops held 58 MB in
#: a long-lived exporter on the training node, and with this cap 12.4 MB
#: (5,000 twenty-point ops: 8.2 MB). Ops past it are parsed again each pass.
SCAN_CACHE_MAX_BYTES = 2 * 1024 * 1024


def _prefetch_uploads(journal, entries, client_for, workers, run_ref) -> dict:
    """Do the NETWORK half of several upload operations at once.

    Every file is presign -> PUT -> confirm, three round trips, and the drain
    did them one file after another. On a hundred thousand small files that is
    hours of latency no bandwidth can fix.

    WHAT IS PARALLEL IS DELIBERATELY NARROW. Only uploads, and only ones
    carrying a correlation -- the backfill/receipt lane, where identity is
    content-addressed and the server is idempotent per correlation, so order
    between two of them cannot matter. Plain HTTP operations keep their strict
    FIFO, because their order IS their meaning.

    NOTHING IS DECIDED HERE. Workers return a result or raise, and that is all.
    Saving the receipt, deleting the op file, classifying the failure, parking
    the queue, breaking on auth -- every one of those still happens exactly
    once, in order, on the drain's own thread. A worker that fails simply
    leaves its op for the serial pass to handle the way it always has.
    """
    from contextvars import copy_context

    candidates = []
    for path, op in entries:
        if len(candidates) >= workers * UPLOAD_WINDOW_FACTOR:
            break
        if op.get("kind") != "upload" or not op.get("correlation"):
            continue
        if run_ref is not None and op.get("run_ref") != run_ref:
            continue
        if op.get("schema") != DELIVERY_SCHEMA:
            continue
        try:
            if journal.receipt(op["correlation"]) is not None:
                continue
            client = client_for(op.get("context"))
        except Exception:  # noqa: BLE001 -- the serial pass will report it
            continue
        candidates.append((path, op, client))
    if len(candidates) < 2:
        return {}

    def run_one(item):
        from .transport import attribution_scope

        path, op, client = item
        with attribution_scope(op.get("attribution", "ambient")):
            # Its own run_ids map: petname resolution is a per-op cache, and
            # sharing a dict across threads would be a race for no benefit --
            # these ops are anchored on projects, not runs.
            return _execute(journal, client, path, op, {})

    done = {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(copy_context().run, run_one, item): item[0] for item in candidates
        }
        for future in as_completed(futures):
            try:
                done[futures[future]] = future.result()
            except Exception:  # noqa: BLE001 -- left for the serial pass
                pass
    return done


#: The key a takeover barrier (`Client._hold_status_writes`) stamps on a status
#: op it set aside in `failed/`: `{pid, host, until, last_error, blocking}`.
TAKEOVER_HOLD_KEY = "takeover_hold"


def hold_abandoned(hold: dict, *, now: float | None = None) -> bool:
    """Whether the relaunch that set ``hold`` can no longer release it: its
    deadline passed, or -- on this host -- its process is gone. A relaunch
    killed hard mid-barrier used to leave the incumbent's close aside until
    another barrier ran on the same box (review of #2019)."""
    if float(hold.get("until") or 0) < (time.time() if now is None else now):
        return True
    try:
        import socket

        same_host = hold.get("host") == socket.gethostname()
    except OSError:
        same_host = False
    if not same_host:
        return False
    try:
        oscompat.probe_pid(int(hold.get("pid")))
    except ProcessLookupError:
        return True
    except (PermissionError, TypeError, ValueError, OverflowError):
        return False  # alive under another user, or unreadable: keep the hold
    return False


def restore_held_op(journal: "Journal", path: Path, op: dict) -> bool:
    """Put one held status op back in the queue at its original position
    (its file name keeps its enqueue order), as it was before the hold."""
    hold = op.pop(TAKEOVER_HOLD_KEY, None)
    if not isinstance(hold, dict):
        return False
    op["last_error"] = hold.get("last_error")
    if hold.get("blocking") is None:
        op.pop("blocking", None)
    else:
        op["blocking"] = hold["blocking"]
    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
    os.replace(path, journal.ops_dir / path.name)
    fsync_directory(journal.ops_dir)
    fsync_directory(path.parent)
    return True


def restore_abandoned_holds(journal: "Journal") -> list[str]:
    """Put back every held status op whose relaunch died (`hold_abandoned`).

    Costs one `stat` when nothing is held (the marker), so every drain pass
    and every new client runs it: the detached worker delivers an abandoned
    close within one pass, instead of the reaper calling the run `crashed`
    first. The marker goes once nothing is held any more."""
    if not journal.holds_marker.exists():
        return []
    restored: list[str] = []
    still_held = False
    for path, op in journal.failed():
        hold = op.get(TAKEOVER_HOLD_KEY)
        if not isinstance(hold, dict):
            continue
        if not hold_abandoned(hold):
            still_held = True
            continue
        try:
            if restore_held_op(journal, path, op):
                restored.append(path.name)
        except OSError:
            still_held = True
    if not still_held:
        try:
            journal.holds_marker.unlink()
        except OSError:
            pass
    return restored


def _take_drain_lock(handle, *, wait_for_lock: bool, timeout: float | None) -> bool:
    """Take the drain flock. ``timeout`` None: block (``wait_for_lock``) or try
    once. Otherwise POLL until it is free or ``timeout`` seconds pass -- a
    blocking flock has no timeout, and a close waiting on a worker's long pass
    must still be able to give up at its deadline."""
    if timeout is None:
        try:
            oscompat.flock(
                handle.fileno(),
                oscompat.LOCK_EX if wait_for_lock else oscompat.LOCK_EX | oscompat.LOCK_NB,
            )
            return True
        except BlockingIOError:
            return False
    give_up = time.monotonic() + max(0.0, timeout)
    pause = 0.01
    while True:
        try:
            oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
            return True
        except BlockingIOError:
            left = give_up - time.monotonic()
            if left <= 0:
                return False
            time.sleep(min(pause, left))
            pause = min(pause * 2, 0.25)


def drain(
    journal: Journal,
    *,
    run_ref: str | None = None,
    client_factory: Callable[[dict | None], Any] | None = None,
    wait_for_lock: bool = True,
    lock_timeout: float | None = None,
    promote_timeout: float | None = None,
    on_error: Callable[[Exception], None] | None = None,
    on_delivered: Callable[[str | None], None] | None = None,
    skip_runs: "set | frozenset | None" = None,
    credential_queues: bool = True,
    long_ops: bool = True,
    only_ops: "set | frozenset | None" = None,
    _include_receipts: bool = True,
) -> DrainReport:
    """Deliver queued ops, in FIFO order WITHIN each run. Foreground and
    background drains share this; the drainer loop wraps it in backoff.

    Per-run lanes (plan 1.6): the queue is split by ``run_ref`` and the lanes
    are visited round-robin, one op each per turn, so a run with a deep backlog
    no longer delays every other run on the machine. A transient failure (a
    503, a timeout) parks that op in place and stops only ITS run for the rest
    of the pass (`DrainReport.stalled_runs`); one run's poison op used to hold
    the whole machine's queue for the 24 h it takes to be dead-lettered. Order
    across runs was never promised: a run's own ops, its close last, still go
    in the order they were queued. An auth block, a connect failure (the
    server is unreachable for everyone) and the caller's deadline still end
    the pass. ``skip_runs`` names lanes the caller is backing off: their ops
    are not attempted this pass. Ops that name no run share one lane (None).

    ``lock_timeout`` bounds the wait for the drain lock (another drainer -- the
    detached worker -- may be mid-pass): the lock is polled, never blocked on,
    and a pass that could not take it in time attempts nothing and reports
    ``lock_busy``. None keeps ``wait_for_lock``'s behaviour. `Run.finish()`
    passes what is left of its deadline, so a worker's long pass can no longer
    hold a close past it (plan 0.6). ``promote_timeout`` bounds this pass's
    promotion of uploads still waiting for their credential scan (None: no
    bound), for the same reason.

    ``run_ref`` scopes a barrier drain (T3-A): only that run's ops are
    attempted, everything else is left for the machine-wide drainer. A barrier
    never runs a multipart upload (plan (g)), and neither does a pass with
    ``long_ops=False`` (a closing process's last pass, which must not spend a
    slice of seconds on one). ``only_ops`` (op ids) attempts those ops and
    nothing else, multipart uploads included: a `finish()` that has to see
    its own uploads through (`multipart.settle_for_close`).
    ``client_factory(context)`` exists for tests; production resolves a client
    per pinned context, tokens fresh (5A).
    ``on_error`` may raise before an error changes the queued operation. This
    lets an approved import retain its receipts and own a longer network retry
    policy without treating unknown failures as temporary connection problems.
    ``on_delivered(correlation)`` runs after the receipt and queue removal are
    durable, including recovery after a receipt-before-removal crash. It is a
    best-effort observer; its failures cannot undo or interrupt delivery.
    """
    if _include_receipts and not journal.receipt_enabled:
        namespaces = journal.namespaces()
        if len(namespaces) > 1:
            combined = DrainReport()
            for queue in namespaces:
                if queue.dir.parent.parent.name == CREDENTIAL_NAMESPACE or (
                    queue.dir.parent.name == CREDENTIAL_NAMESPACE
                ):
                    if not credential_queues:
                        # The root's detached worker: each credential queue has
                        # its own, started by a writer that holds that
                        # credential (#2041 round 3). This one could only
                        # hold their writes, and keep its lease doing it.
                        continue
                if queue.dir.parent.name == CREDENTIAL_NAMESPACE and _queue_is_empty(queue.dir):
                    # An idle credential queue: nothing to take a lock, scan or
                    # rewrite status for (#2041 round 3: hundreds of them made
                    # every pass slow).
                    continue
                part = drain(
                    queue,
                    run_ref=run_ref,
                    client_factory=client_factory,
                    wait_for_lock=wait_for_lock,
                    lock_timeout=lock_timeout,
                    promote_timeout=promote_timeout,
                    on_error=on_error,
                    on_delivered=on_delivered,
                    skip_runs=skip_runs,
                    long_ops=long_ops,
                    only_ops=only_ops,
                    _include_receipts=False,
                )
                combined.delivered += part.delivered
                combined.dead_lettered += part.dead_lettered
                combined.remaining += part.remaining
                if part.auth_blocked and not combined.auth_blocked:
                    combined.auth_status = part.auth_status
                    combined.auth_message = part.auth_message
                    combined.auth_context = part.auth_context
                combined.auth_blocked |= part.auth_blocked
                combined.queue_auth_stopped |= part.queue_auth_stopped
                combined.credential_refused += part.credential_refused
                combined.close_held += part.close_held
                combined.permanently_held += part.permanently_held
                combined.auth_refusals.extend(part.auth_refusals)
                combined.held_reasons.extend(
                    r for r in part.held_reasons if r not in combined.held_reasons
                )
                combined.stopped_transient |= part.stopped_transient
                combined.held_back += part.held_back
                combined.credential_held += part.credential_held
                combined.errors.extend(part.errors)
                combined.deadline_reached |= part.deadline_reached
                combined.lock_busy |= part.lock_busy
                combined.unreachable |= part.unreachable
                if part.queued_runs is not None:
                    combined.queued_runs = (combined.queued_runs or set()) | part.queued_runs
                combined.unknown_kinds += part.unknown_kinds
                combined.in_progress += part.in_progress
                combined.coalesced += part.coalesced
                combined.dead_letter_records.extend(part.dead_letter_records)
                combined.progressed_runs |= part.progressed_runs
                for lane, stall in part.stalled_runs.items():
                    combined.stalled_runs.setdefault(lane, stall)
                if part.retry_after is not None:
                    combined.retry_after = max(combined.retry_after or 0.0, part.retry_after)
            return combined
    report = DrainReport()
    journal._ensure()
    if journal.receipt_enabled:
        journal._receipt_dirs()
    try:
        journal.sweep_stale_temps()
    except Exception:  # noqa: BLE001 -- hygiene is best-effort
        pass
    if journal.paused:
        report.remaining = journal._count_dir(journal.ops_dir)[0]
        return report
    if not journal.receipt_enabled:
        # Uploads queued before their credential scan become ops first: every
        # new-version drain (the worker, a barrier, `probe outbox drain`) is a
        # promoter. An item another process holds is left to that process.
        try:
            # The lease says "someone is promoting", so a kick meanwhile does
            # not fork a promote-only worker; items have their own locks, so
            # this promotes whether or not it got the lease.
            with _try_lock(journal.promote_lease):
                journal.promote_waiting(run_ref=run_ref, timeout=promote_timeout)
        except Exception:  # noqa: BLE001 -- items stay waiting; the next pass retries
            pass

    from .client import Client  # lazy: enqueue paths must not import httpx

    clients: dict[tuple, Any] = {}
    constructed: list[Any] = []  # only clients WE built get closed

    # Credentials the API refused (#2041 review): fingerprint -> when. The
    # earlier passes' come from status.json, so a refused credential is re-tried
    # once per cooldown rather than once per pass; this pass's refusals apply to
    # every later op of that credential in the pass, the writer's own included.
    cooling = _cooling_refusals(journal)
    refused_now: dict[str, str] = {}
    delivered_fps: set[str] = set()
    # One token is one account: what any of a token's writes recorded about it
    # vouches for all of them (#2041 re-review). Filled from the queue below.
    accounts: dict[str, tuple[str, str]] = {}
    learned: set[str] = set()

    def learn_account(op: dict) -> None:
        """After a stored-login write went out with ITS OWN token: remember
        which account that token is, once per token (`record_account`), so its
        other writes can still follow a same-account re-login -- a login saved
        by the setup wizard, or by an older CLI, records none (#2041 round 3)."""
        stamp = (op.get("context") or {}).get("principal")
        if not isinstance(stamp, dict) or stamp.get("source") != CredentialSource.CONFIG:
            return
        fp = stamp.get("fingerprint")
        if not fp or op_credential(op)[1] or fp in learned or stamp_identity(stamp) or fp in accounts:
            return
        learned.add(fp)
        try:
            if recorded_account(fp) is not None:
                return
            sender = client_for(op.get("context"))
            settings = getattr(sender, "settings", None)
            if settings is None or credential_fingerprint(settings.token, None) != fp:
                return  # went out with a later login (the account was known): nothing to learn
            record_account(fp, _identity_of(settings, getattr(sender, "transport", None)))
        except Exception:  # noqa: BLE001 -- evidence for later, never a delivery step
            return

    def client_for(context: dict | None, ingest: bool = False):
        stamp = (context or {}).get("principal")
        stamped_fp = None
        if isinstance(stamp, dict):
            stamped_fp = stamp.get("ingest_fingerprint") if ingest else stamp.get("fingerprint")
        key = ((context or {}).get("name"), (context or {}).get("base_url"), stamped_fp, ingest)
        # What a client_factory is told: the route, so it matches the right key.
        asked = {**context, "route": "ingest"} if (ingest and isinstance(context, dict)) else context
        refused_at = refused_now.get(stamped_fp) if stamped_fp else None
        if refused_at is None and stamped_fp in cooling and (
            client_factory is None or client_factory(asked) is None
        ):
            # Refused in an earlier pass. The writer itself (client_factory)
            # may still try: a re-login it picked up is how its writes recover.
            refused_at = cooling[stamped_fp]
        if refused_at is not None:
            # Set aside with every other write of that credential, so it
            # neither re-asks the API nor holds anyone else's writes up.
            raise CredentialNotHere(
                f"its credential was refused by the API at {refused_at}; it waits for a "
                f"new sign-in ({WIZARD_HINT}), or for the process that holds that credential"
            )
        if isinstance(clients.get(key), CredentialNotHere):
            # A fresh instance: re-raising one object grows its traceback per op.
            raise CredentialNotHere(str(clients[key]), permanent=clients[key].permanent)
        if key not in clients:
            supplied = client_factory(asked) if client_factory is not None else None
            if supplied is not None:
                clients[key] = supplied
            else:
                try:
                    account = accounts.get((stamp or {}).get("fingerprint") or "")
                    settings = _settings_for_op(context, ingest=ingest, account=account)
                except CredentialNotHere as absent:
                    clients[key] = absent  # asked once per pass, not once per op
                    raise
                if not settings.token and not settings.ingest_token:
                    raise errors.AuthError(
                        f"no credentials for context {key[0] or '<default>'} ({WIZARD_HINT})"
                    )
                # async_writes=False because THIS is the drainer: an async
                # client mints a producer record (`sdk:{host}:{pid}:{uuid4}`)
                # per construction, and the detached worker builds one per drain
                # pass, so a long outage would litter producers/ with thousands
                # of single-use entries in the registry that exists to make
                # capture loss visible.
                #
                # NOT because replay would re-journal: replay never goes through
                # `Client.write`, it uses `transport.request` and
                # `upload_fingerprinted` directly. Write mode does not govern
                # the drain path.
                client = Client(settings=settings, async_writes=False)
                constructed.append(client)
                clients[key] = client
        return clients[key]

    def tally_delivered(op: dict) -> None:
        """Credit one landed op to the producer that enqueued it. Runs AFTER
        the op file is gone (see ``note_delivered``) and can never fail a
        delivery: accounting is diagnostics, the write already happened."""
        producer_id = op.get("producer_id")
        if not producer_id:
            return
        try:
            journal.note_delivered(producer_id)
        except Exception:  # noqa: BLE001 -- accounting must never break the drain
            pass

    def notify_delivered(op: dict) -> None:
        if on_delivered is not None:
            try:
                on_delivered(op.get("correlation"))
            except Exception:  # noqa: BLE001 -- observers cannot fail a committed delivery
                pass

    lock_handle = journal.drain_lock.open("a+")
    if not _take_drain_lock(lock_handle, wait_for_lock=wait_for_lock, timeout=lock_timeout):
        lock_handle.close()
        report.remaining = journal._count_dir(journal.ops_dir)[0]
        report.lock_busy = True
        report.errors.append("another drain holds the lock")
        return report

    # Whether an upload LEFT the queue this pass (delivered or dead-lettered):
    # only then can a blob have lost its last reference. `gc_blobs` re-reads
    # the whole queue under the append lock, and running it after a pass that
    # merely TRIED an upload -- an upload at the head of the queue during an
    # outage, every pass -- blocked `log()` for ~1 s per pass at 20k ops
    # (review of #2038).
    settled_upload = False
    # Petname -> uuid, for this drain only. See _resolved_run_id.
    run_ids: dict[str, str] = {}
    # What the closing status recount may reuse instead of re-parsing under
    # the append lock (plan 1.9); filled by the one scan below.
    known: dict[str, tuple[int, str | None]] = {}
    held_note: str | None = None
    # Per run: queued-at of each blocking op in the outbox's OTHER queues.
    # Read once, and only when this pass meets a run's close.
    elsewhere: dict | None = None

    def writes_elsewhere(run: str, before: str | None, epoch: Any = None) -> int:
        """How many blocking writes of ``run`` queued no later than ``before``
        sit in the outbox's other queues. A write stamped with an OLDER write
        epoch than the close's is left out: the server refuses it as stale
        anyway, so holding the close for it only delays the close (#2041
        round 5: a takeover's close sat behind the dead attempt's writes)."""
        nonlocal elsewhere
        if elsewhere is None:
            elsewhere = {}
            for queue in journal.other_queues():
                for _other_path, other in Journal._read_dir(queue.ops_dir):
                    if isinstance(other, dict) and other.get("run_ref") and other.get("blocking", True):
                        elsewhere.setdefault(other["run_ref"], []).append(
                            (str(other.get("enqueued_at") or ""), _write_epoch_of(other))
                        )
                if not queue.receipt_enabled:
                    # Uploads still waiting for their credential scan count too:
                    # they become ops of that queue shortly (#2041 round 4).
                    for _position, _op_id, ref, readable, blocking in queue._waiting_items():
                        if readable and blocking and ref:
                            elsewhere.setdefault(ref, []).append(("", None))
        return sum(
            1
            for at, their_epoch in elsewhere.get(run, ())
            if (not before or at <= before)
            and not (epoch is not None and their_epoch is not None and their_epoch < epoch)
        )
    try:
        if journal.receipt_enabled:
            journal.recover_intents()
        # 2.3: a close a dead relaunch held aside goes back in the queue, so
        # this very pass delivers it (a stat when nothing is held).
        try:
            restore_abandoned_holds(journal)
        except Exception:  # noqa: BLE001 -- a hold left in place is the old behaviour
            pass
        # Plan (g): multipart uploads live in a queue of their own
        # (`<outbox>/multipart/ops/`) that no earlier release reads, so an
        # older worker holding this outbox never meets one. Only a pass that
        # may run them (not a run's barrier, not a closing exporter) reads it.
        multipart_queue: list = []
        if not journal.receipt_enabled and (only_ops is not None or (run_ref is None and long_ops)):
            try:
                from . import multipart as _multipart

                # A staged copy nothing will read again (its op finished or
                # dead-lettered, a copy cut short by a kill) goes first.
                _multipart.gc_staging(journal)
                multipart_queue = _multipart.pending(journal)
            except Exception:  # noqa: BLE001 -- multipart waits for the next pass
                multipart_queue = []
        # A run's ops queued after an upload still being scanned wait for it:
        # its close must not reach the server first (see `promote_waiting`).
        # Read BEFORE the queue: an upload promoted in between is then both
        # "waiting" and queued, which only holds its successors back one pass;
        # the other order would miss it in both and let its close go first.
        held_back = {} if journal.receipt_enabled else journal.waiting_positions()
        # ONE parse of the queue, outside the append lock (plan 1.9): it is
        # this pass's work list, its quarantine list, and the recount's cache.
        queued, corrupt = journal._scan_ops()
        known = op_meta(queued)
        report.queued_runs = {
            _lane_of(op) for _, op in [*queued, *multipart_queue] if isinstance(op, dict)
        }
        # Each run's ops in queue order, for coalescing (plan 1.2): a metric op
        # rides in one POST with the ones queued right behind it in its run.
        lanes: dict[Any, list[tuple[Path, dict]]] = {}
        for item in queued:
            lanes.setdefault(_lane_of(item[1]), []).append(item)
        lane_index = {item[0]: n for ops in lanes.values() for n, item in enumerate(ops)}
        consumed: set[Path] = set()
        if run_ref is None:
            queued = _round_robin(queued)
        # Plan (g): a multipart upload spends up to a slice of seconds per
        # visit, so every other lane goes first in each pass -- a metric queued
        # behind a 10 GB checkpoint is delivered before the checkpoint's next
        # slice starts. And ONE upload at a time sends or hashes (the oldest
        # not waiting on the server): the next starts only when it is
        # verifying, so an earlier checkpoint finishes, and releases its staged
        # bytes, before a later one pins more.
        queued = [*queued, *multipart_queue]
        multipart_turn = next(
            (p for p, o in multipart_queue if not _multipart_waiting(o)), None
        )
        skip = set(skip_runs or ())
        stalled = report.stalled_runs
        # Runs parked for the pass behind an op this drainer must not send.
        held_runs: set = set()
        # Of those, the runs held for a credential (#2035): their later ops
        # are counted as kept too.
        credential_lanes: dict = {}
        held_paths: set = set()

        def hold(lane: Any, ops: list, held: OpHeldHere) -> None:
            """Where every `OpHeldHere` lands, for a lone op or a whole batch:
            each op stays queued as it is, and its run's later ops -- its close
            -- wait out the pass behind it. An op naming no run holds only
            itself. #2041 counts `credential_held` and its reasons here."""
            nonlocal held_note
            if lane is not None:
                held_runs.add(lane)
            if isinstance(held, CredentialNotHere):
                # Not this drainer's to send (#2035): untouched, no attempt
                # counted, nothing dead-lettered, every op this drainer CAN
                # send still goes. Its run's lane STALLS as well as parks: a
                # worker then backs that run off and stays up, instead of
                # exiting and being forked again on the next kick (#2041
                # round 3, MED-2).
                note = held_note = str(held)
                report.credential_held += len(ops)
                if held.permanent:
                    report.permanently_held += len(ops)
                held_paths.update(item[0] for item in ops)
                if lane is not None:
                    credential_lanes[lane] = credential_lanes.get(lane, False) or held.permanent
                if note not in report.held_reasons:
                    report.held_reasons.append(note)
                if lane is not None:
                    stalled[lane] = LaneStall(note, held=True)
            log.debug("outbox: %d op(s) of run %s held: %s", len(ops), lane, held)

        for _path, queued_op in queued:
            queued_stamp = (queued_op.get("context") or {}).get("principal")
            queued_as = stamp_identity(queued_stamp) if isinstance(queued_stamp, dict) else None
            if queued_as is not None:
                accounts.setdefault(str(queued_stamp.get("fingerprint")), queued_as)
        try:
            journal.quarantine_paths(corrupt, known=known)
        except Exception:  # noqa: BLE001 -- quarantine is best-effort hygiene
            pass
        workers = _upload_workers()
        parallel = workers > 1 and journal.receipt_enabled
        prefetched: dict = {}
        # The window REFILLS as the serial loop advances. A single fetch was
        # worse than it looked: it took the first `workers * FACTOR` operations
        # and every one after them went back to being uploaded alone, so a
        # hundred-thousand-file import parallelised sixteen files and serialised
        # the rest -- exactly the latency this exists to remove, hidden behind a
        # test that never staged more than eight.
        cursor = 0
        lost_responses = 0
        def settle_batch(batch: list, landed: list, failed: list, lane: Any) -> str:
            """Credit what a coalesced POST delivered, settle each op that did
            not land as if it had been sent alone, and put the ops the batch
            never reached back in line for their turn this pass."""
            for landed_path, _ in landed:
                landed_path.unlink(missing_ok=True)
            if landed:
                # One fsync for the batch, as the single path does per op.
                fsync_directory(journal.ops_dir)
                for producer_id, count in _count_producers(landed).items():
                    try:
                        journal.note_delivered(producer_id, count)
                    except Exception:  # noqa: BLE001 -- accounting never breaks the drain
                        pass
                for _, landed_op in landed:
                    report.delivered += 1
                    notify_delivered(landed_op)
                    landed_fp = _stamp_fingerprint(landed_op)
                    if landed_fp is not None:
                        delivered_fps.add(landed_fp)
                        learn_account(landed_op)
                report.progressed_runs.add(lane)
            settled = {item[0] for item in landed} | {item[0] for item, _ in failed}
            for item_path, _ in batch:
                if item_path not in settled:
                    consumed.discard(item_path)
            for (failed_path, failed_op), exc in failed:
                if settle_failure(failed_path, failed_op, exc, lane) == "break":
                    return "break"
            return "continue"

        def settle_failure(path: Path, op: dict, exc: Exception, lane: Any) -> str:
            """What one op's failure does to it and to the pass: ``"continue"``
            or ``"break"``. The single path and a coalesced batch (plan 1.2) both
            come here, so a merged op fails exactly as it would have alone."""
            nonlocal settled_upload, lost_responses
            from .transport import attribution_scope

            if isinstance(exc, errors.OfflineRunNotCreated):
                # An offline run's op ahead of its run (plan 2.12: its create
                # was refused, or is queued behind a transient stop). Not this
                # op's fault: no attempt is charged and it keeps its place;
                # `probe sync` names the fix.
                report.stopped_transient = True
                report.errors.append(_redact(str(exc)))
                return "break"
            if isinstance(exc, errors.DeadlineExceeded):
                # The CALLER's clock ran out (finish()'s close budget), not
                # the op: nothing was learned about the server, so no error
                # is recorded, the failure clock does not start, and the op
                # keeps its place for the detached worker. One exception:
                # when the request had fully left (`sent`), the server may
                # have applied it, so the ATTEMPT is recorded -- a replayed
                # create whose 409 names `existing_id` is then read as its
                # own earlier delivery rather than a first-attempt conflict.
                if getattr(exc, "sent", False):
                    op["attempts"] = _attempts(op) + 1
                    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                    known[path.name] = _meta_of(op)  # the recount's cache follows
                report.deadline_reached = True
                return "break"
            if on_error is not None:
                on_error(exc)
            verdict = classify(exc)
            if _edge_already_there(op, exc) or (
                verdict == "idempotent"
                and _attempts(op) > 0
                and not op.get("correlation")
            ):
                # A 409-with-existing_id on a RETRY plausibly names our own
                # earlier half-delivered attempt. On a FIRST attempt it is
                # a genuine natural-key conflict -- treating it as success
                # would silently discard the queued write (codex), so it
                # falls through to the permanent path below. The one
                # exception: an edge that already exists IS the write done.
                extra = sorted(k for k in ("reason", "meta", "provenance") if (op.get("body") or {}).get(k))
                if extra and _edge_already_there(op, exc):
                    log.info("outbox: edge op %s already existed; its %s was not applied",
                             op.get("op_id"), ", ".join(extra))
                path.unlink(missing_ok=True)
                fsync_directory(journal.ops_dir)
                tally_delivered(op)
                report.delivered += 1
                report.progressed_runs.add(lane)
                notify_delivered(op)
                settled_upload = settled_upload or op.get("kind") == "upload"
                return "continue"
            op["attempts"] = _attempts(op) + 1
            op["last_error"] = _redact(f"{type(exc).__name__}: {exc}")
            if (
                verdict == "transient"
                and _failing_for_seconds(op, time.time()) >= _transient_budget_seconds()
                and op["attempts"] >= MIN_TRANSIENT_ATTEMPTS
            ):
                # Out of patience, not out of politeness. Parking is right
                # for a blip and ruinous for a permanent fault, because the
                # queue behind this op never moves and the run never closes.
                # Past the budget -- WALL-CLOCK time since the first failure,
                # so how often some loop polls cannot decide it, AND a floor
                # of attempts, so one blip after a day asleep cannot either
                # -- we stop calling it transient and let the permanent path
                # below record what it can and move on.
                verdict = "permanent"
            if verdict == "auth":
                write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                known[path.name] = _meta_of(op)  # a hashed upload now has a size
                refused_context = op.get("context")
                if not report.auth_blocked:
                    report.auth_status = getattr(exc, "status", None)
                    report.auth_message = str(exc)
                    report.auth_context = refused_context
                report.auth_blocked = True
                refused_fp = _stamp_fingerprint(op)
                report.auth_refusals.append(
                    {
                        "status": getattr(exc, "status", None),
                        "message": str(exc),
                        "context": refused_context,
                        "fingerprint": refused_fp,
                    }
                )
                report.errors.append(op["last_error"])
                if refused_fp is not None:
                    # A stamped op names its credential, so only that
                    # credential's writes stop: the rest of the queue -- a
                    # PROBE_TOKEN job's own writes, say -- keeps going. It used
                    # to stop the whole pass and block the box (#2041 review).
                    refused_now[refused_fp] = now_iso()
                    delivered_fps.discard(refused_fp)
                    if lane is not None:
                        stalled[lane] = LaneStall(op["last_error"], status=getattr(exc, "status", None))
                    report.credential_refused += 1
                    return "continue"
                report.queue_auth_stopped = True
                return "break"
            if verdict in ("permanent", "idempotent"):
                # A permanently rejected UPLOAD must still leave a record.
                # The synchronous path degrades to a reference artifact
                # (`meta.upload = "failed"`), which `check_run` counts as a
                # capture gap -- honest and visible. The drainer had no such
                # path, so a queued upload that was rejected left NO artifact
                # row anywhere, only an outbox dead letter nobody reads. That
                # is a capability regression hiding inside the async upload,
                # so it is closed BEFORE uploads may be queued at all.
                if (
                    verdict == "permanent"
                    and op.get("kind") in ("upload", "multipart_upload")
                    and not op.get("correlation")
                    and not isinstance(exc, CredentialBlocked)
                ):
                    # BUILDING the fallback client resolves credentials, and
                    # that resolution is itself a thing that can fail -- for
                    # an unroutable endpoint it always does. Evaluated bare
                    # as an argument it raised out of this `except` block,
                    # out of the loop and out of drain() itself, stranding
                    # every op behind it: the exact wedge the permanent
                    # verdict exists to remove, reintroduced by removing it.
                    # A fallback may never break the drain.
                    try:
                        fallback = client_for(op.get("context"))
                    except Exception:
                        fallback = None
                    with attribution_scope(op.get("attribution", "ambient")):
                        recorded = fallback is not None and _record_upload_fallback(
                            journal, fallback, op
                        )
                    if recorded:
                        # THE FALLBACK IS THE RESOLUTION, so this op stops
                        # holding the run open. The synchronous upload path
                        # degrades to exactly this row and leaves no failure
                        # state at all; a queued upload that reached the same
                        # end must not be the reason `Run.finish` refuses to
                        # close. The dead letter is still written -- it is
                        # the audit trail `probe outbox status` shows -- it
                        # just no longer counts as blocking (see
                        # `Run._queued_ops`).
                        op["blocking"] = False
                if _is_multipart(op):
                    # Plan (g): a dead multipart upload keeps no bytes. Its
                    # staged copy goes and the server's upload is aborted
                    # (best-effort: the server's own sweep aborts an idle one).
                    try:
                        from .multipart import on_dead_letter

                        on_dead_letter(journal, client_for, op)
                    except Exception:  # noqa: BLE001 -- cleanup never breaks the drain
                        pass
                # Update in place, then MOVE atomically: writing a failed/
                # copy before unlinking the original leaves the op in both
                # queues across a crash (codex).
                write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                # A multipart op dead-letters into its own queue's failed/ --
                # never the shared one, where an older release's `probe outbox
                # retry` would move it into ops/ for a worker that cannot send it.
                failed_dir = path.parent.parent / "failed" if _is_multipart(op) else journal.failed_dir
                failed_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
                os.replace(path, failed_dir / path.name)
                fsync_directory(failed_dir)
                fsync_directory(path.parent)
                report.dead_lettered += 1
                report.progressed_runs.add(lane)
                report.errors.append(op["last_error"])
                report.dead_letter_records.append(
                    {
                        "run_ref": op.get("run_ref"),
                        "op_id": op.get("op_id"),
                        "error": str(op["last_error"])[:_DEAD_LETTER_ERROR_CHARS],
                        "status": getattr(exc, "status", None),
                    }
                )
                settled_upload = settled_upload or op.get("kind") == "upload"
                return "continue"
            # transient: park in place, order preserved
            write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
            known[path.name] = _meta_of(op)  # a hashed upload now has a size
            report.stopped_transient = True
            report.errors.append(op["last_error"])
            retry_after = getattr(exc, "retry_after", None)
            if retry_after is not None:
                report.retry_after = max(report.retry_after or 0.0, float(retry_after))
            if getattr(exc, "unreachable", False):
                # Nobody's op can land: stop the pass, as before lanes.
                report.unreachable = True
                return "break"
            if (
                isinstance(exc, errors.TransportError)
                and getattr(exc, "status", None) is None
                and not isinstance(exc, errors.DeadlineExceeded)
            ):
                # Sent, and no answer came. Once may be this op; twice in one
                # pass is a server that accepts and hangs, and trying every
                # run's head would hold the drain lock (which `finish()` waits
                # on) for one read timeout per run (review of #2051).
                lost_responses += 1
                if lost_responses >= 2:
                    report.unreachable = True
                    return "break"
            stalled[lane] = LaneStall(op["last_error"], retry_after, getattr(exc, "status", None))
            return "continue"

        for position, (path, op) in enumerate(queued):
            if path in consumed:
                continue  # delivered inside an earlier op's batch
            if parallel and path not in prefetched and cursor <= position:
                prefetched.update(
                    _prefetch_uploads(journal, queued[position:], client_for, workers, run_ref)
                )
                cursor = position + workers * UPLOAD_WINDOW_FACTOR
            if only_ops is not None and op.get("op_id") not in only_ops:
                continue
            if run_ref is not None and op.get("run_ref") != run_ref:
                continue
            if _is_multipart(op) and path != multipart_turn and not _multipart_waiting(op):
                continue  # not its turn: one upload at a time (plan (g))
            lane = _lane_of(op)
            if lane in credential_lanes and path not in held_paths:
                # A later op of a run held for its credential (or a close held
                # behind another queue): kept too, and counted, so "N kept"
                # says how many writes wait, not how many runs (#2041 round 4),
                # and how many of them `discard --held` would drop (round 5).
                report.credential_held += 1
                if credential_lanes[lane]:
                    report.permanently_held += 1
                continue
            if lane in stalled or lane in skip or lane in held_runs:
                continue  # its run waits; the other runs do not
            if path.name > held_back.get(lane, path.name):
                report.held_back += 1
                continue
            kind = op.get("kind")
            if isinstance(kind, str) and kind not in OP_KINDS:
                # A newer SDK's op. Not attempted, so no attempt is charged and
                # the 24 h budget never starts: it waits, in its run's order,
                # for a worker that can deliver it (plan 1.11). A kind that is
                # not even a string is not a newer SDK's: `_execute` refuses it
                # (a dead letter), as it always did (review of #2052: a list
                # here raised TypeError and failed every pass machine-wide).
                reason = f"op kind {kind!r} needs a newer probe-research to deliver it"
                report.unknown_kinds += 1
                if reason not in report.errors:
                    report.errors.append(reason)
                if lane is not None:
                    stalled[lane] = LaneStall(reason)
                # An op that names no run holds only itself: the run-less lane
                # has no order to keep, and stalling it would hold every other
                # run-less write on the machine behind a newer SDK's op.
                continue
            if lane is not None and _is_run_close(op) and not _close_hold_expired(op):
                waiting = writes_elsewhere(lane, op.get("enqueued_at"), _write_epoch_of(op))
                if waiting:
                    # The close must not land before its data: writes of this
                    # run queued earlier under another credential are in
                    # another queue, which this queue's order cannot see
                    # (#2041 round 3). Held, at most CLOSE_HOLD_MAX_SECONDS.
                    reason = (
                        f"the close of run {lane} waits for {waiting} of its write(s) queued "
                        "under another credential"
                    )
                    stalled[lane] = LaneStall(reason, held=True, wake_by=_close_hold_left(op))
                    report.close_held += 1
                    if reason not in report.held_reasons:
                        report.held_reasons.append(reason)
                    continue
            journal._scan_forget(path.name)  # attempted: read it fresh next pass
            batch = (
                []
                if journal.receipt_enabled
                else _coalesce(lanes.get(lane) or [], lane_index.get(path, 0), held_back.get(lane))
            )
            for item_path, _ in batch:
                journal._scan_forget(item_path.name)
            from .transport import attribution_scope

            if batch:
                # Plan 1.2: this op and the metric ops queued right behind it in
                # its run, as ONE POST (see `_deliver_batch`). Settled OUTSIDE
                # the per-op `try`: an error while settling must not send the
                # head through `settle_failure` again after it landed (review of
                # #2053).
                try:
                    client = client_for(op.get("context"))
                except OpHeldHere as held:
                    # Every op of the batch shares the head's context (it is in
                    # `_merge_key`), so none of them is this drainer's to send.
                    hold(lane, batch, held)
                    continue
                except Exception as exc:  # noqa: BLE001 -- the head's failure, as alone
                    if settle_failure(path, op, exc, lane) == "break":
                        break
                    continue
                consumed.update(item[0] for item in batch)
                with attribution_scope(op.get("attribution", "ambient")):
                    landed, failed, merged = _deliver_batch(journal, client, batch, run_ids)
                report.coalesced += merged
                try:
                    action = settle_batch(batch, landed, failed, lane)
                except Exception as exc:  # noqa: BLE001 -- e.g. ENOSPC recording a failure
                    # What landed may be sent again next pass (the insert keeps
                    # the first write of a point); nothing is lost or resent now.
                    # The run waits for the rest of the pass: an op of it that
                    # was not settled is still queued, and its later ops -- its
                    # close -- must not go ahead of it (review of #2053).
                    log.warning("outbox: settling a coalesced batch failed", exc_info=True)
                    stalled[lane] = LaneStall(_redact(f"{type(exc).__name__}: {exc}"))
                    action = "continue"
                if action == "break":
                    break
                continue
            try:
                if journal.receipt_enabled and op.get("schema") != DELIVERY_SCHEMA:
                    raise errors.ValidationError(
                        "unsupported delivery operation schema", status=422
                    )
                if op.get("correlation") and journal.receipt(op["correlation"]) is not None:
                    # Receipt committed before a crash prevented op deletion.
                    result = None
                elif path in prefetched:
                    # Its bytes already moved, in parallel with its neighbours.
                    # The receipt is still written here, in order, on this
                    # thread -- see `_prefetch_uploads`.
                    journal._save_delivery_receipt(op, prefetched[path])
                else:
                    with attribution_scope(op.get("attribution", "ambient")):
                        result = _execute(
                            journal, client_for(op.get("context"), op_credential(op)[1]), path, op, run_ids
                        )
                    journal._save_delivery_receipt(op, result)
                delivered_fp = _stamp_fingerprint(op)
                if delivered_fp is not None:
                    delivered_fps.add(delivered_fp)
                    learn_account(op)
            except OpInProgress as progress:
                # Plan (g): the long op moved (or is waiting on the server) and
                # saved where it is; nothing failed, so no attempt is charged.
                if progress.retry_after is not None:
                    # Waiting (the server verifying, its own hash in the
                    # background, another upload of the same bytes): this lane
                    # backs off, at least `retry_after`, growing while it waits.
                    stalled[lane] = LaneStall(
                        str(progress), progress.retry_after, wake_by=progress.wake_by
                    )
                else:
                    # A slice of parts went: that IS progress (the worker must
                    # not sleep to another lane's backoff after it), and the
                    # next pass takes the next slice.
                    report.in_progress += 1
                    report.progressed_runs.add(lane)
                    if lane is not None:
                        held_runs.add(lane)
                continue
            except OpHeldHere as held:
                hold(lane, [(path, op)], held)
                continue
            except Exception as exc:  # noqa: BLE001 -- classified in settle_failure
                if settle_failure(path, op, exc, lane) == "break":
                    break
                continue
            else:
                path.unlink(missing_ok=True)
                # fsync so a post-delivery crash cannot resurrect the op file
                # and replay a write the server already committed (codex:
                # replay is at-least-once; keep the window as small as disk
                # semantics allow).
                fsync_directory(journal.ops_dir)
                tally_delivered(op)
                report.delivered += 1
                report.progressed_runs.add(lane)
                notify_delivered(op)
                settled_upload = settled_upload or op.get("kind") == "upload"
    finally:
        for client in constructed:
            try:
                client.close()
            except Exception:  # noqa: BLE001
                pass
        if settled_upload:  # no upload left the queue: no blob can be unreferenced
            try:
                journal.gc_blobs()
            except Exception:  # noqa: BLE001
                pass
        # Counted from the recount itself: names under the lock, parsing only
        # what this pass's scan did not see (plan 1.9).
        journal._ensure()
        with file_lock(journal.append_lock):
            # Merged with what is on disk NOW, under the append lock: a `probe
            # login` during this pass cleared the list (clear_auth_block), and
            # writing back the one read at the start undid it (#2041 re-review).
            on_disk = (
                Journal.read_status(journal.dir, include_receipts=False) or {}
            ).get("refused_fingerprints") or {}
            if not isinstance(on_disk, dict):
                on_disk = {}
            cleared = set(cooling) - set(on_disk)
            report.remaining = journal._write_status_locked(
                known=known,
                auth_blocked_since=(now_iso() if report.queue_auth_stopped else None),
                held=report.credential_held + report.credential_refused + report.close_held,
                held_at=now_iso(),
                refused_fingerprints={
                    **{fp: at for fp, at in on_disk.items() if fp not in delivered_fps},
                    **{fp: at for fp, at in refused_now.items() if fp not in cleared},
                },
                last_error=(report.errors[-1] if report.errors else held_note),
                new_dead_letters=report.dead_letter_records,
            )
        if not journal.receipt_enabled:
            # Plan (g): an upload still in its own queue is still work, so a
            # worker does not exit with one half-sent (status.json's count, which
            # older releases read too, stays the shared queue's).
            report.remaining += _multipart_pending_count(journal)
        oscompat.flock(lock_handle.fileno(), oscompat.LOCK_UN)
        lock_handle.close()
    return report


# -- coalesced delivery (plan 1.2) ---------------------------------------------

#: One merged POST carries at most this many points and this many bytes of
#: them (the server takes 50,000 points; a smaller request fails and retries
#: cheaper, and keeps one request's server transaction short).
MERGE_MAX_POINTS = 5_000
MERGE_MAX_BYTES = 2 * 1024 * 1024
_METRICS_ROUTE = re.compile(r"/v1/runs/([^/?#]+)/metrics")


def _merge_key(op: dict) -> str | None:
    """What a metric op must share with its neighbours to ride in one POST --
    everything but its points -- or None when it never merges.

    Only a logged metrics POST to a run named by its id, whose EVERY point has
    a step or a client wall clock: an unstepped point without a timestamp takes
    the server's transaction time, so two of them merged into one transaction
    would collapse under the wall-clock dedupe index. Ops queued by releases
    before 1.4 (no wall clock) therefore drain one by one, as they always did.
    """
    if op.get("kind") != "http" or op.get("method") != "POST" or op.get("correlation"):
        return None
    match = _METRICS_ROUTE.fullmatch(op.get("path") or "")
    if match is None or not _is_uuid(match.group(1)):
        return None
    body = op.get("body")
    points = body.get("points") if isinstance(body, dict) else None
    if not isinstance(points, list) or not points:
        return None
    for point in points:
        if not isinstance(point, dict):
            return None
        if point.get("step_index") is None and not point.get("wall_clock"):
            return None
    rest = {key: value for key, value in body.items() if key != "points"}
    try:
        return json.dumps(
            [
                op.get("run_ref"),
                op.get("context"),
                op.get("attribution"),
                op.get("path"),
                op.get("blocking", True),
                bool(op.get("best_effort")),
                rest,
            ],
            sort_keys=True,
        )
    except (TypeError, ValueError):
        return None


def _coalesce(lane: list[tuple[Path, dict]], start: int, held_back: str | None) -> list:
    """The ops from ``lane[start]`` on that ride in one POST, or [] when fewer
    than two would: consecutive, same `_merge_key`, not held back behind a
    waiting upload, within the point and byte caps."""
    if start >= len(lane):
        return []
    head_key = _merge_key(lane[start][1])
    if head_key is None or _attempts(lane[start][1]) > 0:
        # An op that already failed goes alone: were it the poison in a batch,
        # merging it again would pin its failure on the head every pass
        # (review of #2053).
        return []
    batch: list[tuple[Path, dict]] = []
    points = size = 0
    for path, op in lane[start:]:
        if batch and (held_back is not None and path.name > held_back):
            break
        if _merge_key(op) != head_key or (batch and _attempts(op) > 0):
            break
        count = len(op["body"]["points"])
        weight = len(json.dumps(op["body"]["points"]))
        if batch and (points + count > MERGE_MAX_POINTS or size + weight > MERGE_MAX_BYTES):
            break
        batch.append((path, op))
        points += count
        size += weight
    return batch if len(batch) > 1 else []


def _count_producers(items: list[tuple[Path, dict]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for _, op in items:
        producer_id = op.get("producer_id")
        if producer_id:
            counts[producer_id] = counts.get(producer_id, 0) + 1
    return counts


#: Statuses a merged POST can get because of ONE of its ops: the batch is split
#: in halves until that op is found (review of #2053: a 500 -- a step past
#: int64, a key past the index row size -- was pinned on the head, and every op
#: before the poison was dead-lettered in turn, 24 h each).
_SPLIT_STATUSES = frozenset({413, 422, 500})


def _merged_failure(exc: Exception) -> str:
    """What a failed merged POST means for its batch: ``"split"`` (one op may
    be the cause), ``"whole"`` (true of every op: the merge key gives the batch
    one run, epoch and context -- a fenced epoch, a deleted run, a locked
    workspace), or ``"stop"`` (the server is busy or away: the head's failure,
    as it would be alone)."""
    if isinstance(exc, errors.DeadlineExceeded):
        return "stop"
    verdict = classify(exc)
    status = getattr(exc, "status", None)
    if verdict == "permanent":
        return "split" if status in _SPLIT_STATUSES or status is None else "whole"
    if verdict == "transient" and status in _SPLIT_STATUSES:
        return "split"
    # 503/429/408/502/504, a connect failure, auth -- and an answer lost after
    # sending: splitting that made every half wait out a read timeout (a hung
    # server, 2 runs x 64 ops: 14 requests, 28.7 s holding the lock). It stops
    # at the head, which counts toward the pass's lost-answer limit and goes
    # alone next pass (it has an attempt now), so a batch that was simply too
    # big to answer in time still gets through (review of #2053).
    return "stop"


def _deliver_batch(journal, client, batch, run_ids) -> tuple[list, list, int]:
    """Send ``batch`` (see `_coalesce`) as one POST. Returns (the ops that
    landed; the ops that did not, each with its error; how many landed inside
    a multi-op POST), in queue order.

    A merged POST refused for a reason one op could cause (`_merged_failure`:
    413, 422, a 500) is split in halves, down
    to single ops, which go through `_execute` exactly as an unmerged op
    would; an op refused on its own for good is reported and the rest carry
    on (as they would behind a dead letter). A refusal true of the whole batch
    (409 fence, 404, a locked workspace) reports every op at once, with no
    further requests. Anything else -- 503, 429, a timeout to connect, an auth
    block, the caller's deadline -- stops the batch at its head, as it would
    stop the op alone; the ops after it are not attempted."""
    landed: list = []
    failed: list = []
    merged = [0]

    def attempt(items) -> bool:
        """False once the batch must stop."""
        if len(items) == 1:
            path, op = items[0]
            try:
                _execute(journal, client, path, op, run_ids)
            except Exception as exc:  # noqa: BLE001 -- settled by the caller
                failed.append((items[0], exc))
                return classify(exc) in ("permanent", "idempotent")
            landed.append(items[0])
            return True
        try:
            _send_merged(client, items)
        except Exception as exc:  # noqa: BLE001 -- classified here, settled by the caller
            how = _merged_failure(exc)
            if how == "split":
                middle = len(items) // 2
                return attempt(items[:middle]) and attempt(items[middle:])
            if how == "whole":
                failed.extend((item, exc) for item in items)
                return True
            failed.append((items[0], exc))
            return False
        landed.extend(items)
        merged[0] += len(items)
        return True

    attempt(list(batch))
    return landed, failed, merged[0]


def _send_merged(client, items) -> None:
    """One POST carrying every point of ``items``, in queue order. Each op is
    prepared (NUL check, scrub) exactly as `_execute` would prepare it alone."""
    from . import unstorable

    points: list = []
    for _, op in items:
        for value in op.values():
            unstorable.has_nul(value)
        unstorable.validate_nuls(op.get("body"), path=op.get("path", ""), method="POST")
        op.update(scrub_op(op))
        points.extend(op["body"]["points"])
    head = items[0][1]
    body = {**head["body"], "points": points}
    client.transport.request("POST", head["path"], json_body=body)


def _attempts(op: dict) -> int:
    """An op's attempt count; a value that is not one (hand-edited, corrupt)
    reads as 0 instead of raising out of `drain()` for the whole machine
    (review of #2053)."""
    value = op.get("attempts")
    if isinstance(value, bool):
        return 0
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError, OverflowError):
        return 0


def _lane_of(op: Any) -> Any:
    """An op's lane: its ``run_ref`` when that is a string (or None). Anything
    else -- a list, a dict -- is not hashable or not a run: it gets one lane of
    its own instead of a TypeError out of `drain()` (pre-existing; review of
    #2053).

    An op that names its own ``lane`` (a string) rides that instead: a
    multipart upload (plan item (g)) moves gigabytes over many passes and must
    never stand in front of the run's metrics, and nothing of the run is
    ordered after it (its artifact row is its own)."""
    if isinstance(op, dict) and isinstance(op.get("lane"), str) and op["lane"]:
        return op["lane"]
    ref = op.get("run_ref") if isinstance(op, dict) else None
    return ref if ref is None or isinstance(ref, str) else "<invalid run_ref>"


def _is_multipart(op: Any) -> bool:
    return isinstance(op, dict) and op.get("kind") == "multipart_upload"


def _multipart_pending_count(journal: "Journal") -> int:
    """Multipart ops queued in this journal (names only, no parse)."""
    try:
        return sum(1 for n in os.listdir(journal.dir / "multipart" / "ops") if n.endswith(".json"))
    except OSError:
        return 0


def _multipart_waiting(op: Any) -> bool:
    """A multipart op that is waiting on the server rather than sending: it
    does not hold the one-upload-at-a-time turn (plan (g))."""
    state = (op.get("multipart") or {}).get("state") if isinstance(op, dict) else None
    return state in ("verifying", "busy")


def _round_robin(queued: list[tuple[Path, dict]]) -> list[tuple[Path, dict]]:
    """The FIFO list interleaved by run: each run's ops keep their order, and
    the runs take turns, one op each, in the order of their oldest op."""
    lanes: dict[Any, list[tuple[Path, dict]]] = {}
    for item in queued:
        op = item[1]
        lanes.setdefault(_lane_of(op), []).append(item)
    if len(lanes) <= 1:
        return queued
    order: list[tuple[Path, dict]] = []
    depth = max(len(ops) for ops in lanes.values())
    for turn in range(depth):
        for ops in lanes.values():
            if turn < len(ops):
                order.append(ops[turn])
    return order


class LaneBackoff:
    """Per-run waits for a loop that drains the whole queue (plan 1.6).

    A stalled run waits out its own backoff (`durable.backoff_delays`, at least
    the server's ``Retry-After``) while the loop keeps delivering every other
    run; a run that progresses starts over. The detached worker and the
    in-process exporter both keep one, passing `skip()` as ``skip_runs``.
    """

    def __init__(self, *, ceiling: float) -> None:
        from . import durable

        self._durable = durable
        self._ceiling = ceiling
        self._delays: dict[Any, Any] = {}
        self._until: dict[Any, float] = {}
        self._last_wait: dict[Any, float] = {}

    def skip(self, now: float | None = None) -> set:
        now = time.monotonic() if now is None else now
        return {lane for lane, until in self._until.items() if until > now}

    def record(self, report: DrainReport, now: float | None = None) -> None:
        now = time.monotonic() if now is None else now
        # A run that progressed starts over -- also when it then stalled in the
        # same pass (review of #2051: a busy run answering `Retry-After: 1` to
        # every other write climbed to the 300 s ceiling while delivering).
        for lane in report.progressed_runs:
            self._forget(lane)
        # A run with nothing queued any more (another drainer -- its own
        # `finish()` -- delivered it) is forgotten: an expired entry kept
        # `next_wake()` at 0 and the worker re-drained every 0.05 s (review of
        # #2051: 5.4 CPU-s per 10 s).
        if report.queued_runs is not None:
            for lane in list(self._until):
                if lane not in report.queued_runs:
                    self._forget(lane)
        for lane, stall in report.stalled_runs.items():
            delays = self._delays.setdefault(lane, self._durable.backoff_delays(None))
            wait = self._durable.honor_retry_after(
                next(delays), stall.retry_after, ceiling=self._ceiling
            )
            if stall.wake_by is not None:
                # A hold that ends at a known time is looked at again then, not
                # a grown backoff later (#2041 round 5: a close held to its cap
                # landed 216 s after it, past the reaper).
                wait = min(wait, max(float(stall.wake_by), 0.05))
            self._until[lane] = now + wait
            self._last_wait[lane] = wait

    def _forget(self, lane: Any) -> None:
        self._delays.pop(lane, None)
        self._until.pop(lane, None)
        self._last_wait.pop(lane, None)

    def next_wake(self, now: float | None = None) -> float | None:
        """Seconds until the soonest run STILL waiting may be tried again, or
        None when none is: an entry whose wait is over says nothing about when
        to look next (it is tried on the next pass anyway)."""
        now = time.monotonic() if now is None else now
        waiting = [until for until in self._until.values() if until > now]
        if not waiting:
            return None
        return min(waiting) - now

    def at_ceiling(self) -> bool:
        """Whether some run has backed off all the way to the ceiling."""
        return any(wait >= self._ceiling for wait in self._last_wait.values())


def _execute(
    journal: Journal,
    client,
    op_path: Path,
    op: dict,
    run_ids: dict[str, str] | None = None,
) -> dict | None:
    """Deliver one op. Raises the transport/client error on failure. Field
    guards raise ValidationError (permanent -> dead letter): a KeyError here
    would classify transient and wedge the FIFO on a malformed op forever."""
    from . import unstorable

    try:
        # Body depth uses the same origin as enqueue/transport validation.
        for value in op.values():
            unstorable.has_nul(value)
    except errors.ValidationError:
        # A malformed legacy body cannot safely pass recursive scrubbing.
        # Retain delivery identity and the refusal, never persist raw secrets
        # merely because validation failed. Mark the omitted payload explicitly.
        retained = {}
        for key in ("schema", "op_id", "run_ref", "blocking", "correlation", "attempts"):
            value = op.get(key)
            if value is None or isinstance(value, (str, bool, int, float)):
                retained[key] = default_scrub(value, key=key)
        retained.update(
            kind="rejected_http",
            validation_error="Queued payload exceeded structural validation limits",
            body={"probe.rejected_payload": "omitted: unsafe JSON structure"},
        )
        op.clear()
        op.update(retained)
        raise errors.ValidationError("Queued payload exceeded structural validation limits", status=422)
    if op.get("kind") == "http":
        # Preserve refusal through scrub and retries, including older drainers.
        try:
            unstorable.validate_nuls(
                op.get("body"), path=op.get("path", ""), method=op.get("method", "")
            )
        except errors.ValidationError:
            op["kind"] = "rejected_http"
            op["validation_error"] = "Queued HTTP payload failed local NUL validation"
    op.update(scrub_op(op))
    if op.get("kind") == "rejected_http":
        raise errors.ValidationError("Queued HTTP payload failed local NUL validation", status=422)
    run_ids = {} if run_ids is None else run_ids
    if op.get("kind") == "create_run":
        # An OFFLINE run's create (plan 2.12). Only `probe sync` drains the
        # queues that carry this kind (`<outbox>/offline/<key>/`), so no older
        # worker ever meets it.
        from .offline import deliver_create

        return deliver_create(journal, client, op)
    if str(op.get("run_ref") or "").startswith("local:"):
        # ...and every later op of that run: `local:<key>` becomes the id the
        # create got. Raises OfflineRunNotCreated while it has none.
        from .offline import bind_local_refs, lineage_gate

        bind_local_refs(journal, op)
        if lineage_gate(journal, client, op):
            # A read/write list this server does not take (`run_inputs` /
            # `run_outputs`): dropped as delivered, never sent to 404.
            return {"dropped": "lineage feature not declared"}
    if op.get("kind") == "http":
        if not op.get("method") or not op.get("path"):
            raise errors.ValidationError(
                f"op {op.get('op_id')} is missing method/path", status=422
            )
        try:
            return client.transport.request(op["method"], op["path"], json_body=op.get("body"))
        except errors.ValidationError:
            resolved = _resolve_queued_run_ref(client, run_ref_for_path(op["path"]), run_ids)
            if resolved is None:
                raise
            # Rewritten for THIS attempt only; the op file keeps the ref that was
            # queued. Persisting the substitution would rewrite history to say
            # something the caller never wrote, and `run_ref` is the barrier-drain
            # scoping key -- a queued petname has to keep matching the barrier
            # armed on the same petname.
            return client.transport.request(
                op["method"],
                op["path"].replace(resolved[0], resolved[1], 1),
                json_body=op.get("body"),
            )
    if op.get("kind") == "multipart_upload":
        # Plan (g): an artifact over 64 MiB, one slice per visit (see
        # `sdk/multipart.py`). Raises OpInProgress while there is more to do.
        from .multipart import execute_op

        return execute_op(journal, client, op_path, op)
    if op.get("kind") != "upload":
        raise errors.ValidationError(
            f"unknown journal op kind {op.get('kind')!r}", status=422
        )

    upload = op.get("upload") or {}
    if not upload.get("anchor") or not upload.get("name") or not upload.get("src_path"):
        raise errors.ValidationError(
            f"upload op {op.get('op_id')} is missing anchor/name/src_path", status=422
        )
    source = journal.blob_path(op) or Path(upload["src_path"])
    if not source.exists() and upload.get("staged"):
        # Recover an interrupted incoming-><digest> rename from a previous
        # drain (red team): the op may name a digest whose file only exists
        # under the incoming staging name (or vice versa).
        incoming = journal.blobs_dir / f"incoming-{op['op_id']}"
        if incoming.exists():
            if upload.get("blob"):
                os.replace(incoming, source)
                fsync_directory(journal.blobs_dir)
            else:
                source = incoming
    if not source.exists():
        # The two absences are different failures and want different fixes: a
        # missing STAGED blob is the outbox losing bytes it owned (gc, a wiped
        # state dir); a missing SOURCE is a file the producer deleted, moved or
        # unmounted before delivery, which the outbox never copied and could
        # not have kept. Reporting both as "staged bytes are gone" sent people
        # hunting the blob store for a file that was never in it.
        if upload.get("staged"):
            raise errors.ValidationError(
                f"staged bytes for op {op['op_id']} are gone ({source})", status=422
            )
        reason = upload.get("unstaged_reason")
        raise errors.ValidationError(
            f"source file for op {op['op_id']} is gone ({source}) and it was "
            "never staged into the outbox, so there are no bytes to fall back "
            "on -- "
            + (reason if reason else "the op was enqueued with stage=False"),
            status=422,
        )
    digest = upload.get("blob")
    size = upload.get("size_bytes")
    if digest is None:
        # 11A: the big-file path hashed nothing at enqueue.
        digest, size = fingerprint(str(source))
        upload["blob"], upload["size_bytes"] = digest, size
        # Persist the digest BEFORE the rename (red team: the reverse order
        # left a crash window where the op pointed at a staging name that no
        # longer existed, and gc then reaped the renamed blob as unreferenced).
        write_text_atomic(op_path, json.dumps(op, indent=2) + "\n", mode=0o600)
        if upload.get("staged"):
            hashed = journal.blobs_dir / digest
            if hashed.exists():
                source.unlink(missing_ok=True)  # dedup: identical bytes already staged
            else:
                os.replace(source, hashed)
                fsync_directory(journal.blobs_dir)
            source = hashed

    def _upload(anchor_id: str | None) -> dict:
        return client.upload_fingerprinted(
            upload["anchor"],
            anchor_id,
            upload["name"],
            str(source),
            digest=digest,
            size=size,
            content_type=upload.get("content_type"),
            kind=upload.get("kind"),
            meta=upload.get("meta"),
            # .get, not ["notes"]: a journal written by an older CLI has no such
            # key, and the drainer must replay those ops rather than KeyError.
            notes=upload.get("notes"),
            span_id=upload.get("span_id"),
            step_index=upload.get("step_index"),
        )

    try:
        return _upload(upload["anchor_id"])
    except errors.ValidationError:
        # `artifact add --from-manifest` rows anchored on a petname reported
        # `anchors_resolved: 0` and `failed: 0`, then dead-lettered here. Same
        # 422-then-resolve retry as the http ops above, and only for the RUN
        # anchor: project/experiment slugs are resolved at enqueue, and
        # workspace/shared anchors have ids only.
        resolved = (
            _resolve_queued_run_ref(client, upload["anchor_id"], run_ids)
            if upload["anchor"] == "run"
            else None
        )
        if resolved is None:
            raise
        return _upload(resolved[1])
