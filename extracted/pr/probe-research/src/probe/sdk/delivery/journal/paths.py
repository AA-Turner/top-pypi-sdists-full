"""where queues live: the outbox root, the per-rank queue, the private $TMPDIR fallback, and per-credential queues and their pruning."""

from __future__ import annotations

import errno as errno_module
import os
import re
import shutil
import time
from pathlib import Path

from ...._shared import oscompat
from ....foundation.durable.durable import file_lock


#: Environment variables identifying a GLOBALLY unique rank in a distributed job (any one is
#: enough; order only breaks ties). `LOCAL_RANK` is absent on purpose: it repeats per node, so
#: on a shared filesystem two nodes' rank 0 would collide back into one queue.
_GLOBAL_RANK_VARS = ("SLURM_PROCID", "RANK", "OMPI_COMM_WORLD_RANK")


def _rank_suffix(environ=None) -> str | None:
    """A per-rank directory component, or None for a single-process job.

    A distributed job puts every rank on ONE journal when $HOME is shared (the normal SLURM
    layout): one `.append.lock`, one `.seq`, one `ops/`, so the append flock serialises metric
    logging across every rank on every node, a cluster-wide mutex on the path meant to be cheap.

    Splitting per rank fixes that without moving the queue somewhere volatile. Node-local
    scratch would be faster and is the wrong trade: $SLURM_TMPDIR is reaped when the job ends,
    destroying a queue that had not drained, the thing durability exists to survive.

    A single-process run gets no suffix: the default path is byte-identical to before and
    nothing needs migrating.
    """
    env = os.environ if environ is None else environ
    for var in _GLOBAL_RANK_VARS:
        raw = (env.get(var) or "").strip()
        if raw:
            return f"rank-{_safe_component(raw)}"
    local = (env.get("LOCAL_RANK") or "").strip()
    if local:
        # Only node-local identity is advertised, so qualify it with the host to keep two
        # nodes' rank 0 apart on shared storage.
        import socket

        return f"rank-{_safe_component(socket.gethostname())}-{_safe_component(local)}"
    return None


def default_root(environ=None) -> Path:
    """The machine's outbox root, without the per-rank component: every process of this user
    queues in it or in one of its ``rank-*`` children. ``environ``: another process's
    variables (the Probe service reads the login shell's) instead of this one's."""
    env = os.environ if environ is None else environ
    configured = env.get("PROBE_OUTBOX_DIR")
    try:
        if configured:
            return Path(configured).expanduser()
        base = env.get("XDG_STATE_HOME")
        root = Path(base) if base else Path.home() / ".local" / "state"
    except (RuntimeError, KeyError, OSError):
        # No HOME and no passwd entry (a container running an arbitrary uid):
        # `Path.home()` raises, and it used to crash `Client()` (plan 1.5).
        return private_fallback_root()
    return root / "probe" / "outbox"


def default_dir(environ=None) -> Path:
    """This process's queue: the root, or its ``rank-*`` child in a distributed job.
    ``environ``: another process's variables, as `default_root` takes them.

    An explicit ``PROBE_OUTBOX_DIR`` is the ROOT too. It is exported once for a whole job (the
    reliability plan's rollout note tells a cluster to set it), so returning it as is put every
    rank of every node on one ``.append.lock``: on an NFS home a cross-client lock the kernel
    polls with backoff, which held each ``log()`` up to ~30 s (agent/tests/environments/nfs_home)."""
    root = default_root(environ)
    suffix = _rank_suffix(environ)
    return root / suffix if suffix else root


def _uid() -> int | str:
    return os.getuid() if hasattr(os, "getuid") else "user"


def fallback_root() -> Path:
    """The NAME of the fallback outbox (plan 1.5): ``$TMPDIR/probe-outbox-<uid>``. NOT durable
    across a pod or machine restart, as the warning that selects it says. Anyone can create
    that name in a shared ``/tmp``: use `private_fallback_root`, which only returns a
    directory this user owns and nobody else can write to."""
    import tempfile

    return Path(tempfile.gettempdir()) / f"probe-outbox-{_uid()}"


def trusted_dir(path: str | Path) -> bool:
    """A queue directory this process may use and deliver from: a real directory (never a
    symlink), owned by this user, with no group or other permission bits. Anything else in a
    shared ``$TMPDIR`` may have been made by someone else to get their ops sent with this
    user's credential, or to read this user's queue (review of #2054, P1)."""
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
    """The fallback outbox root, guaranteed private: `fallback_root` when it is (or can be
    created as) a `trusted_dir`, else a fresh ``probe-outbox-<uid>-XXXX`` from
    `tempfile.mkdtemp` (0700, atomic). Chosen once per process."""
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


def _fallback_roots(environ=None) -> list[Path]:
    """Every fallback root of this user in ``$TMPDIR`` that is a `trusted_dir` (the fixed name,
    and any `mkdtemp` one a process had to take). ``environ``: another process's variables,
    whose ``TMPDIR`` names the folder (this process's `tempfile` keeps its first answer)."""
    import tempfile

    tmpdir = environ.get("TMPDIR") if environ is not None else None
    base = Path(tmpdir) if tmpdir else Path(tempfile.gettempdir())
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


#: `flock` failures meaning locks will never work on this filesystem. Any other
#: (EWOULDBLOCK/EAGAIN) means someone else holds the lock: normal, never "unusable" (Codex,
#: round 2: contention must not redirect a healthy PV-backed queue to ephemeral storage).
_UNUSABLE_LOCK_ERRNOS = frozenset(
    code
    for code in (
        getattr(errno_module, name, None)
        for name in ("ENOSYS", "ENOLCK", "EROFS", "EACCES", "EPERM", "EOPNOTSUPP")
    )
    if code is not None
)


def _credential_queue_dirs(root: Path) -> list[Path]:
    """The credential queues (#2035) under an outbox root, in name order.
    Only 16-hex names: a queue being pruned is renamed away first."""
    try:
        entries = sorted((root / CREDENTIAL_NAMESPACE).iterdir())
    except OSError:
        return []
    return [p for p in entries if re.fullmatch(r"[0-9a-f]{16}", p.name) and p.is_dir()]


def credential_queue_dirs(root: Path) -> list[Path]:
    """The credential queues (#2035) under the outbox ``root``."""
    return _credential_queue_dirs(Path(root))


def _queue_is_empty(path: Path) -> bool:
    """Nothing queued, dead-lettered, discarded, waiting or staged in the queue at ``path``,
    and no receipt namespace under it."""
    if (path / DELIVERY_NAMESPACE).exists() or (path / ".recover").exists():
        return False
    # `multipart/*` (plan (g)): a queue holding only an upload in progress (its op, staged
    # bytes) is not empty and must never be pruned. `discarded/`: writes someone set aside are
    # kept, not deleted with the folder (`relocate_discards` moves them to the root first).
    for sub in (
        "ops", "failed", "discarded", "waiting", "blobs",
        "multipart/ops", "multipart/staged", "multipart/failed",
    ):
        try:
            if os.listdir(path / sub):
                return False
        except FileNotFoundError:
            continue
        except OSError:
            return False
    return True


#: How many discards one `prune_credential_queues` moves to the root at most.
_PRUNE_MOVE_LIMIT = 1000
#: A credential queue left empty this long is removed (`prune_credential_queues`).
CREDENTIAL_QUEUE_IDLE_SECONDS = 3600.0
_last_prune = float("-inf")


def prune_credential_queues(
    root: Path,
    *,
    idle_seconds: float = CREDENTIAL_QUEUE_IDLE_SECONDS,
    counts: "DiscardCounts | None" = None,
) -> int:
    """Remove credential queues (#2035) that are empty, idle for ``idle_seconds`` and whose drain
    lock and worker lease are free: one folder per token ever used piled up (#2041 round 3: 420
    of them made every `finish()` 15x slower). A writer coming back recreates its folder on its
    next write (`Journal._append` re-asserts a missing layout). The folder is renamed away under
    its append lock before deletion, so a racing write lands in the recreated folder, never the
    doomed one. A queue's discards go to the root first (`_move_discards`), counted into
    ``counts``: never deleted with it. At most once per process per 10 minutes. Returns how many
    went."""
    global _last_prune
    if time.monotonic() - _last_prune < 600.0:
        return 0
    _last_prune = time.monotonic()
    removed = 0
    moved = counts if counts is not None else DiscardCounts()
    # Bounded: this runs as a worker starts, before it sends anything; the rescuer moves the
    # rest (`relocate_discards`, unbounded, its own process).
    budget = [_PRUNE_MOVE_LIMIT]

    def move(path: Path) -> None:
        if budget[0] > 0:
            budget[0] -= _move_discards(path, root, moved, limit=budget[0])
    try:
        leftovers = [p for p in (root / CREDENTIAL_NAMESPACE).iterdir() if p.name.startswith(".pruned-")]
    except OSError:
        leftovers = []
    for path in leftovers:  # a prune that died between the rename and the delete
        move(path)  # an older release's prune left them there
        if not _holds_discards(path):  # one that would not move stays for the next pass
            shutil.rmtree(path, ignore_errors=True)
    for path in _credential_queue_dirs(root):
        move(path)
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
from probe.sdk.delivery.journal.failures.discards import DiscardCounts, _holds_discards, _move_discards  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import CREDENTIAL_NAMESPACE, DELIVERY_NAMESPACE, _safe_component  # noqa: E402 -- pieces need each other; the front door loads this one first
