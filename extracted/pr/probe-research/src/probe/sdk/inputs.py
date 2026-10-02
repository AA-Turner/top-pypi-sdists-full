"""What a run READS, recorded from inside the run (lineage plan 1, N2).

Lineage could say what a run WROTE (its files) but not what it READ, so a
follow-up run's parent was guessed from the conversation. The SDK runs inside
the run, so it can simply watch: Python's audit hook reports every ``open()``
the interpreter makes (PEP 578). For each file a run opens for READING this
module records the path and the file's identity at that moment, hashes the
bytes, and at the end of the run sends the list to ``POST /v1/runs/{id}/inputs``.
The server matches each hash to the run that WROTE those bytes -- that is the
whole lineage fact, exact, from any machine.

What the hook sees (measured 2026-09-25, Python 3.12): ``open``, ``pathlib``,
``json``, ``np.load`` (incl. mmap), ``np.loadtxt``, ``pandas.read_csv``,
``pandas.read_parquet``, ``torch.load``, PIL, ``pickle``, ``os.open``. What it
cannot see -- libraries that open files from C. The ones that matter most are
wrapped (:mod:`probe.sdk._readers`, installed only when the library is
imported): ``pyarrow.parquet`` (``read_table``, ``ParquetFile``,
``ParquetDataset``), ``pyarrow.memory_map`` (the Hugging Face ``datasets``
cache), ``h5py.File`` (its mode says read or write), ``safetensors``
(``safe_open``, ``load_file``), and ``torch.save``, a write. Any other reader
can call :func:`note_read`. What stays unseen is named in the run's
``coverage`` so "no reads" is never mistaken for "read nothing".

SHAPE. Every recording process -- the run's own, a forked DataLoader worker,
the Python child of ``probe exec`` (which gets a tiny stdlib hook through an
injected ``sitecustomize``, see ``CHILD_SITE_CODE``), or a Python worker the
run's process started by spawn or forkserver (the same hook, bound by
``probe.init()``: see `bind_workers`) -- appends one JSON line per new (path,
identity) to ``<state>/probe/reads/<run>/<host>.<pid>.jsonl``, whose first
line names the run and the process whose close takes it. The
process that closes the run (``finish()``, or the ``exec`` launcher after its
child exits) reads the spools it may (its own, and those of processes on this
host that have ended -- never a live rank's or another host's), hashes what it
can within ``FINISH_WAIT_S``, and journals the result as NON-blocking ops: a
read list must never hold a run's close. A process that dies without closing
leaves its spool, and the next recorder on the same host and server sends it
(``recover_orphans``).

WHAT IS NEVER RECORDED: the interpreter's own files (``sys.prefix``,
site-packages), tool caches (pip/uv/torch extensions -- NOT model or dataset
caches such as ``~/.cache/huggingface``, which are real inputs), ``/proc``,
``/dev``, ``/sys``, ``/etc``, ``/usr``, code (``.py``, ``.pyc``, ``.so``: the
snapshot's job), Probe's own state, credential directories and
credential-shaped names, and any file Probe itself opened (a ``log_artifact``
fingerprint, a snapshot, upload staging): those reads are Probe's, not the
run's.

IDENTITY. A read is (path, the file's device/inode/size/mtime/ctime when
opened); a file rewritten at the same path is a second read. The hasher
re-checks that identity before and after hashing; if it moved, the bytes
actually read are unknown and the read is sent as ``stable: false`` -- the
server keeps it and never matches it. Files over 1 GiB, or past the run's 10 GB
hashing budget, get a fingerprint (size, mtime, and a hash of the first and
last 4 MiB) instead of a full hash; the server matches those only to a
reference artifact at the same host, path and size. A per-machine cache keyed
on that identity (ctime included: it cannot be set back, unlike mtime) means a
dataset is hashed once per machine, not once per run.

Opt out: ``probe.init(capture_reads=False)`` or ``PROBE_CAPTURE_READS=0``.

WRITES (lineage plan 3, F2). A read can only be matched to bytes the server
knows, and output capture stores only the watched folder's small files. So the
same hook also notes every open for WRITING: the path, when the run first
opened it for writing, the file's identity just BEFORE that open (none when
the open creates it) and an observation id -- once per path per process, in
the same spool. Nothing is hashed then: the file is still being written.

At the close each noted path is looked at once more (first, on a thread of its
own, before anything else can spend the close's time). It counts as something
the run WROTE only if it still exists, is a regular file, and is no longer
what it was before the run opened it (device, inode, size, mtime, ctime; no
clock is trusted) -- so a temp file deleted before the close, an open that
failed (a read-only file), an append that wrote nothing and a read-only
``r+`` are not outputs, and are never hashed. The FINAL bytes are hashed
(fingerprinted over 1 GiB, the read side's scheme, so a fingerprinted read can
match it) and sent to ``POST /v1/runs/{id}/outputs`` with the size and the
mtime. Intermediate versions of a file are not kept: this is what the run
left behind. A rename of a noted file (the write-then-``os.replace``
checkpoint pattern) notes the new name. Only paths, sizes, times and hashes
leave the machine, never contents.

A writer that DIES leaves its notes for a recovery by a later run, by which
time anything may have rewritten the file (the crashed run's retry,
overwriting ``ckpt.pt``). So while it lives the recording process looks at its
written files every WRITE_CHECK_S and keeps the LAST identity of each in a
sidecar beside its spool (``<host>.<pid>.wf.json``, rewritten atomically, one
entry per path); a recovery hashes a file only if it is still exactly that,
and otherwise sends the row unhashed and undated by the file, counted as
``unverified_after_exit``. A ``probe exec`` child's own ``probe.init(capture_outputs=False)``
(or ``capture_reads=False``) is written into its spool, and wins over what its
hook spooled before it.

Never a write: everything never a read (above), Probe's own folders (state,
spools, the outbox, an offline queue), and any CACHE (``.cache/``,
``$XDG_CACHE_HOME``, ``$HF_HOME`` ...): writing into a cache is a download, not
something the run produced, and recording it would link every later reader of
that model to whichever run happened to download it first -- judged on the
path as opened and as resolved, so a link into a cache is one too. Unseen:
files written from C or Rust (pyarrow, safetensors, sqlite -- ``torch.save``
and ``h5py.File`` in a write mode are wrapped) and by processes that are not
Python; the coverage says so.

Switches, kept simple: writes are recorded only while reads are (the same
hook), so ``capture_reads=False`` / ``PROBE_CAPTURE_READS=0`` turns both off;
``capture_outputs=False`` / ``PROBE_CAPTURE_OUTPUTS=0`` turns writes off (the
run asked for nothing it produced to be recorded); ``PROBE_CAPTURE_WRITES=0``
turns off writes alone. Sent only to a server that declares ``run_outputs``.

ONE I/O BUDGET per run pays for every byte hashed: reads in the background
during the run; at the close the reads still unhashed FIRST, then the writes;
then output capture's references (:func:`reference_budget`: one object per
run, however many capture windows it closes). A fingerprint is
charged the edges it reads, and no file is started (or finished) past the
close's deadline, so a run that wrote 10,000 big files cannot turn its close
into 80 GB of edge reads. What was cut is sent unhashed and counted in the
coverage (``hash_cut``: by budget, by deadline).
"""

from __future__ import annotations

import contextlib
import functools
import hashlib
import json
import os
import queue
import re
import shutil
import socket
import sqlite3
import sys
import threading
import time
import urllib.parse
import uuid
from datetime import datetime
from probe._compat import UTC
from pathlib import Path
from typing import Any, NamedTuple

from . import _open_runs, homedir
from . import ignore as _ignore
from . import owndirs as _owndirs
from . import safe_warn as _diagnostics

READS_ENV = "PROBE_CAPTURE_READS"
#: Set by ``probe exec`` for its child: the run's spool folder. A process that
#: sees it records through the injected hook and never finalizes -- the launcher
#: owns the run's read list.
CHILD_DIR_ENV = "PROBE_READS_DIR"
#: Set (beside PROBE_READS_DIR) by a process that bound its SPAWNED workers to
#: its run (`bind_workers`, F5): its pid. Only that process collects them; a
#: process that sees another pid here is one of its workers.
OWNER_PID_ENV = "PROBE_READS_OWNER_PID"
#: The binding file those workers follow (`bind_workers`).
BIND_ENV = "PROBE_READS_BIND"
#: How often a worker bound through a binding file looks at it again: a run
#: that closed, or a second run that opened, reaches a persistent worker
#: within this long. Reads it spooled into a closed run meanwhile are cut at
#: the close (`closed.<host>.<pid>.json`).
BIND_CHECK_S = 0.25
#: How often such a worker asks whether its owner is still alive (a lock
#: test on the owner's ``.lock``): less often than it looks at the binding,
#: since on NFS every lock call goes to the server's lock manager (128
#: workers on a node looking every 0.25 s would be ~500 calls/s).
OWNER_CHECK_S = 1.0
FEATURE = "run_inputs"
#: The server takes a run's write list (``POST /v1/runs/{id}/outputs``).
OUTPUTS_FEATURE = "run_outputs"
#: The server keys a read on (run, path, host, observation_id) (0290, F7), so
#: a late hash REPLACES the read's unhashed row. No feature names that: it
#: shipped in the same server change as `run_outputs`, so a server declaring
#: `run_outputs` understands it. An older one ignores the field (its model
#: does not forbid extras) but would keep a late hash as a SECOND row, so the
#: id is sent, and late hashes re-sent, only to a server that declares it.
OBSERVATIONS_FEATURE = OUTPUTS_FEATURE
#: ``PROBE_CAPTURE_WRITES=0`` turns off write recording alone.
WRITES_ENV = "PROBE_CAPTURE_WRITES"
#: Output capture's switch (``outputs.CAPTURE_ENV``): off, writes are off too.
OUTPUTS_ENV = "PROBE_CAPTURE_OUTPUTS"
RECORDER = "python-audit-hook"
#: Readers neither the audit hook nor a wrapper (`_readers`) sees. A reader
#: leaves this list only when a test proves it is seen.
UNSEEN_READERS = (
    "pyarrow.dataset Datasets read directly (to_table, scanner), pyarrow feather/ipc/csv/json readers",
    "other C/Rust readers (sqlite, zarr, lmdb, ...), and a wrapped function held before probe.init() "
    "other than as a module global (a default argument, an attribute)",
    "Python workers started by spawn or forkserver before probe.init(), or while several runs record in one process",
)
#: Writers the audit hook cannot see (`torch.save` and `h5py.File` in a
#: write mode are wrapped).
UNSEEN_WRITERS = (
    "C/Rust writers (pyarrow, safetensors, sqlite)",
    "processes that are not Python (cp, rsync, a compiled tool)",
    "Python workers started by spawn or forkserver before probe.init(), or while several runs record in one process",
)
#: How often the recording process looks at the files it wrote, and keeps the
#: last identity of each in its ``.wf.json`` sidecar. A RECOVERY -- the writer
#: died, and its spool is sent by a later run -- hashes a written file only if
#: it is still exactly what the writer last saw: a file another run rewrote
#: since (a retry overwriting ``ckpt.pt``) is sent unhashed, never with the
#: other run's bytes.
WRITE_CHECK_S = 30.0
#: The most one of those looks may take; the next continues where it stopped.
WRITE_CHECK_SWEEP_S = 1.0
#: Where a recording process keeps what it last saw of each file it wrote:
#: ``<host>.<pid>.wf.json`` beside its spool (`_RunReads.check_writes`).
WF_SUFFIX = ".wf.json"
#: Environment variables naming cache folders: a write under one is a download.
_CACHE_ENVS = (
    "XDG_CACHE_HOME",
    "HF_HOME",
    "HF_HUB_CACHE",
    "HF_DATASETS_CACHE",
    "TRANSFORMERS_CACHE",
    "TORCH_HOME",
)
#: Path fragments under which a write is a cache fill, never an output.
_WRITE_ONLY_PARTS = ("/.cache/",)

MAX_PATHS = 10_000
#: Longest path sent. The server keys reads on the path, and a btree entry has
#: a hard size limit; one over it would fail the whole batch it rides in.
MAX_PATH_BYTES = 2048
FULL_HASH_MAX_BYTES = 1 << 30
RUN_HASH_BUDGET_BYTES = 10 * (1 << 30)
EDGE_BYTES = 4 << 20
BATCH_ROWS = 2000
#: The most ``finish()`` spends on reads -- waiting for the background hasher,
#: then hashing what is left -- before sending the rest unhashed.
FINISH_WAIT_S = 30.0
#: How often the owner's hasher tails the spools of its workers (forked or
#: spawned: their header names it) during the run, so their reads are hashed
#: as they happen and not all at the close (F7); and the most it reads of one
#: spool per look.
TAIL_S = 5.0
TAIL_BYTES = 4 << 20
#: With an observation id the server keys on the host too, and bounds it.
MAX_OBSERVATION_HOST_BYTES = 255
#: A dead run's spools are recovered only after they sat this long unchanged.
ORPHAN_AGE_S = 600.0
_CHUNK = 1 << 20

_CODE_SUFFIXES = (".py", ".pyc", ".pyo", ".pyd", ".so", ".dylib", ".dll", ".pth", ".pyi")
#: Operating-system trees. `/usr` by its system parts only: `/usr/src/app` is
#: the working directory of the official Python images.
_SYSTEM_PREFIXES = (
    "/proc/",
    "/sys/",
    "/dev/",
    "/etc/",
    "/usr/lib/",
    "/usr/lib64/",
    "/usr/libexec/",
    "/usr/share/",
    "/usr/include/",
    "/usr/bin/",
    "/usr/sbin/",
    "/usr/local/lib/",
    "/usr/local/share/",
    "/usr/local/include/",
    "/usr/local/bin/",
    "/lib/",
    "/lib64/",
    "/bin/",
    "/sbin/",
    "/System/",
    "/Library/",
    "/private/etc/",
    "/private/var/db/",
    "/run/",
    "/var/lib/",
)
#: Under a system prefix but where data lives: removable and mounted disks.
_SYSTEM_ALLOWED = ("/run/media/", "/run/mnt/")
#: Path fragments of tool caches. Deliberately NOT all of ~/.cache: model and
#: dataset caches (huggingface, torch hub) hold the inputs lineage is about.
_TOOL_CACHE_PARTS = (
    "/.cache/pip/",
    "/.cache/uv/",
    "/.cache/pypoetry/",
    "/.cache/torch_extensions/",
    "/.cache/pre-commit/",
    "/.cache/matplotlib/",
    "/.cache/fontconfig/",
    "/.triton/",
    "/.nv/",
    "/__pycache__/",
    "/.ipython/",
    "/.jupyter/",
    "/.config/probe/",
    "/.local/state/probe/",
    "/.probe/",
)
#: Where tools keep credentials. A read's path and hash are shown to everyone
#: who can see the run, so a token file must never become one -- including the
#: ones inside a cache that is otherwise a real input (~/.cache/huggingface).
_CREDENTIAL_PARTS = (
    "/.ssh/",
    "/.gnupg/",
    "/.aws/",
    "/.azure/",
    "/.kube/",
    "/.docker/",
    "/.kaggle/",
    "/.config/gh/",
    "/.config/gcloud/",
    "/.config/wandb/",
    "/.cache/huggingface/token",
    "/.cache/huggingface/stored_tokens",
    "/.huggingface/token",
    "/.databrickscfg",
    "/.netrc",
    "/.pgpass",
    "/.git-credentials",
    "/.modal.toml",
)
#: How many caller frames to inspect for Probe's own code before calling an
#: open the run's. Probe's file work (fingerprint, snapshot, staging, gate)
#: opens within a few frames of Probe code; a run's read through a deep library
#: stack has library frames nearest.
_PROBE_FRAME_DEPTH = 8

_lock = threading.RLock()
_installed = False
_local = threading.local()
_active: dict[str, "_RunReads"] = {}
_hash_queue: "queue.Queue[tuple[str, str, tuple] | None]" = queue.Queue()
#: identity -> (sha256, fingerprint); (None, None) means the file moved or
#: could not be read. Absent means not hashed (yet).
_hash_results: dict[tuple, tuple[str | None, str | None]] = {}
_hasher: threading.Thread | None = None
_hasher_pid: int | None = None
#: The queue the running hasher takes its items from (`_hash_loop`).
_hasher_queue: "queue.Queue | None" = None
#: The spools `collect` read, for `discard` to remove -- and only those.
_consumed: dict[str, list[Path]] = {}
#: What a run's close left of its I/O budget, for capture's references (F3).
_reference_budgets: dict[str, list[int]] = {}
#: Probe's own folders (state, outbox, an offline queue), as path prefixes: a
#: file there is never the run's read or write. Filled by `start`.
_OWN_PREFIXES: tuple[str, ...] = ()
#: Cache folders named by the environment (`_CACHE_ENVS`), as prefixes.
_WRITE_SKIP_PREFIXES: tuple[str, ...] = ()
_budget_lock = threading.Lock()


def enabled(capture_reads: bool | None) -> bool:
    """Argument over environment; on by default."""
    if capture_reads is not None:
        return bool(capture_reads)
    return _env_on(os.environ.get(READS_ENV))


def writes_enabled(capture_outputs: bool | None = None) -> bool:
    """Whether writes are recorded (while reads are): never with
    ``PROBE_CAPTURE_WRITES=0``; otherwise ``capture_outputs`` over
    ``PROBE_CAPTURE_OUTPUTS``, on by default."""
    if not _env_on(os.environ.get(WRITES_ENV)):
        return False
    if capture_outputs is not None:
        return bool(capture_outputs)
    return _env_on(os.environ.get(OUTPUTS_ENV))


def _env_on(value: str | None) -> bool:
    return (value or "1").strip().lower() not in ("0", "false", "off", "no")


def _as_prefix(path: Any) -> set[str]:
    """``path`` as the prefixes a hooked path may start with: as given and
    resolved (a symlinked home), each ending in a separator."""
    out: set[str] = set()
    try:
        for p in (os.path.abspath(os.fspath(path)), os.path.realpath(os.fspath(path))):
            out.add(p if p.endswith(os.sep) else p + os.sep)
    except (TypeError, ValueError, OSError):
        pass
    return out


def _note_own_dirs(client: Any = None, *extra: Any) -> None:
    """Remember Probe's own folders and the environment's cache folders, as
    prefixes a recorded path must not start with. Additive: a second run
    opening under another outbox adds its own."""
    global _OWN_PREFIXES, _WRITE_SKIP_PREFIXES
    dirs: set[Any] = {state_dir().parent, *(e for e in extra if e)}
    try:
        from .journal import default_root, fallback_root

        dirs.update((default_root(), fallback_root()))
    except Exception:  # noqa: BLE001 -- a folder we cannot name is not skipped
        pass
    journal_dir = getattr(getattr(client, "journal", None), "dir", None)
    if journal_dir:
        dirs.add(journal_dir)
    own: set[str] = set(_OWN_PREFIXES)
    for d in dirs:
        own |= _as_prefix(d)
    caches: set[str] = set(_WRITE_SKIP_PREFIXES)
    for name in _CACHE_ENVS:
        value = os.environ.get(name)
        if value:
            caches |= _as_prefix(value)
    with _lock:
        _OWN_PREFIXES = tuple(sorted(own))
        _WRITE_SKIP_PREFIXES = tuple(sorted(caches))


def state_dir() -> Path:
    """``<state>/probe/reads``; under a private ``$TMPDIR`` folder when the
    state folder cannot be written (``HOME=/``, `homedir.state_base`)."""
    return homedir.state_base() / "probe" / "reads"


#: What a run id cannot carry into its folder's name (`run_folder`): a path
#: separator, or PYTHONPATH's (``os.pathsep``) -- an offline run's
#: ``local:<key>`` split its spawned workers' hook folder in two on
#: PYTHONPATH, and no worker ever loaded the hook. ``%`` is the escape itself.
_NOT_IN_FOLDER = frozenset("%:;/\\" + os.sep + (os.altsep or "") + os.pathsep)


def run_folder(run_id: str) -> str:
    """``run_id``'s folder name under `state_dir`: the id, with ``%``, ``:``,
    ``;``, ``/`` and ``\\`` escaped as ``%XX``. A server id (a uuid) is its own
    name; ``local:<key>`` is ``local%3A<key>``. Stable and reversible
    (`_folder_run`): the owner, its workers' hook, a recovery and ``probe
    sync`` all find the same folder, and a spool header still names the run
    by its id."""
    return "".join(f"%{ord(char):02X}" if char in _NOT_IN_FOLDER else char for char in run_id)


def _folder_run(name: str) -> str:
    """The run id whose `run_folder` is ``name``."""
    return urllib.parse.unquote(name) if "%" in name else name


def run_dir(run_id: str) -> Path:
    return state_dir() / run_folder(run_id)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _host() -> str:
    """This machine, as spool names carry it: a shared home directory (NFS on a
    cluster) holds every node's spools, and only this node's are this node's."""
    name = socket.gethostname() or "host"
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in name)


def _spool_owner(spool: Path) -> tuple[str, int] | None:
    host, _, pid = spool.stem.rpartition(".")
    try:
        return host, int(pid)
    except ValueError:
        return None


@contextlib.contextmanager
def internal():
    """Mark the current thread's file opens as Probe's own work."""
    depth = getattr(_local, "internal", 0)
    _local.internal = depth + 1
    try:
        yield
    finally:
        _local.internal = depth


#: Interpreter prefixes that are whole system roots: a Debian/Ubuntu Python (or
#: a venv on one) has `base_prefix = /usr`, and excluding it would drop
#: `/usr/src/app`, the working directory of the official images. Its library
#: folders are excluded by name instead (sysconfig, below).
_ROOT_PREFIXES = ("/", "/usr", "/usr/local")


def _excluded_prefixes() -> tuple[str, ...]:
    prefixes = {
        p for p in (sys.prefix, sys.base_prefix, sys.exec_prefix) if p not in _ROOT_PREFIXES
    }
    try:
        import site
        import sysconfig

        prefixes.update(site.getsitepackages())
        prefixes.add(site.getusersitepackages())
        for name in ("stdlib", "platstdlib", "purelib", "platlib"):
            path = sysconfig.get_paths().get(name)
            if path:
                prefixes.add(path)
    except Exception:  # noqa: BLE001 -- a virtualenv without site helpers
        pass
    out = []
    for p in prefixes:
        if p:
            p = os.path.abspath(p)
            out.append(p if p.endswith(os.sep) else p + os.sep)
    return tuple(sorted(out))


@functools.cache
def _interpreter_prefixes() -> tuple[str, ...]:
    return _excluded_prefixes()


def excluded(path: str) -> bool:
    """Whether a path is never a run input (see the module docstring)."""
    if not path.startswith("/"):
        return True
    if path.endswith(_CODE_SUFFIXES):
        return True
    if path.startswith(_SYSTEM_PREFIXES) and not path.startswith(_SYSTEM_ALLOWED):
        return True
    if path.startswith(_interpreter_prefixes()):
        return True
    if _OWN_PREFIXES and path.startswith(_OWN_PREFIXES):
        return True
    if any(part in path for part in _TOOL_CACHE_PARTS):
        return True
    if any(part in path for part in _CREDENTIAL_PARTS):
        return True
    if _owndirs.owns(path):
        # The outbox, capture state and $TMPDIR stand-ins wherever they are
        # (`PROBE_OUTBOX_DIR`, `XDG_STATE_HOME`, a HOME that cannot be written):
        # the parts above only know the default `~/.local/state/probe`.
        return True
    from .snapshot import SKIP_DIRS, _skip_reason

    parts = path.split("/")
    if any(part in SKIP_DIRS for part in parts[:-1]):
        return True
    return _skip_reason(parts[-1]) is not None


def _ignored(rules: Any, path: str) -> bool:
    """Whether a ``.probeignore`` pattern excludes ``path`` (plan (n)). Checked
    after :func:`excluded`, so it only ever removes. A path outside the rules'
    root is matched by the unanchored patterns only, and a read is matched as
    opened AND as resolved, since ``open()`` follows symlinks (see
    :mod:`probe.sdk.ignore`)."""
    return rules is not None and rules.ignored(path, follow=True)


def _sendable(path: str) -> bool:
    """A path the server can store: UTF-8 (a filename of arbitrary bytes decodes
    to lone surrogates) and short enough to key on."""
    try:
        return len(path.encode("utf-8")) <= MAX_PATH_BYTES
    except UnicodeEncodeError:
        return False


def write_excluded(path: str) -> bool:
    """Whether a path is never a run's OUTPUT beyond :func:`excluded`: a cache
    (see the module docstring)."""
    if any(part in path for part in _WRITE_ONLY_PARTS):
        return True
    return bool(_WRITE_SKIP_PREFIXES) and path.startswith(_WRITE_SKIP_PREFIXES)


_WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND


def _is_read(mode: Any, flags: Any) -> bool:
    if isinstance(mode, str) and mode:
        return not any(c in mode for c in "wax+")
    if isinstance(flags, int):
        return (flags & _WRITE_FLAGS) == 0
    return False


def _is_write(mode: Any, flags: Any) -> bool:
    """An open that may change the file: ``w``/``a``/``x``/``+``, or a write
    flag. (``r+`` is both a read and a write.)"""
    if isinstance(mode, str) and mode:
        return any(c in mode for c in "wax+")
    if isinstance(flags, int):
        return bool(flags & _WRITE_FLAGS)
    return False


#: The C-reader wrappers (`_readers`): their frames are the run's call, not
#: Probe's own file work.
_READERS_MODULE = "probe.sdk._readers"


def _probe_is_calling(frame: Any) -> bool:
    """Whether Probe's own code opened the file: a ``probe`` module within
    _PROBE_FRAME_DEPTH frames of ``frame``, the Python frame that opened it
    (None: no Python code was on the stack -- an open made from C -- which
    is not Probe's)."""
    for _ in range(_PROBE_FRAME_DEPTH):
        if frame is None:
            return False
        name = frame.f_globals.get("__name__", "")
        if (name == "probe" or name.startswith("probe.")) and name != _READERS_MODULE:
            return True
        frame = frame.f_back
    return False


def _bound_run_id() -> str | None:
    fluent = sys.modules.get("probe.sdk.fluent")
    if fluent is None:
        return None
    try:
        binding = fluent._current.get(None)
    except Exception:  # noqa: BLE001
        return None
    run = getattr(binding, "run", None)
    run_id = getattr(run, "id", None)
    return str(run_id) if run_id is not None else None


def _ident(st: os.stat_result) -> tuple:
    return (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)


class _RunReads:
    """One run's recording state in THIS process."""

    def __init__(
        self, run_id: str, ignore: Any = None, *, writes: bool = False, owner: int | None = None
    ) -> None:
        self.run_id = run_id
        #: The process that closes the run here: this one, or -- in a forked
        #: worker -- the one it was forked from. Named in each spool's first
        #: line, so that process's close takes a live worker's spool too.
        self.owner = os.getpid() if owner is None else owner
        #: Whether this process's spawned Python workers may be bound to the
        #: run (`bind_workers`: `probe.init()` asks; a CLI or service opening
        #: runs for someone else does not).
        self.children = False
        #: Whether this process records the run as a worker FOLLOWING its
        #: owner's binding (`_follow`): only such a live worker's spool is the
        #: owner's to take at its close, which marks where to cut it.
        self.follows = False
        #: The run's `.probeignore` rules (`probe.sdk.ignore.IgnoreRules`), or
        #: None. An excluded read is never spooled, so never hashed.
        self.ignore = ignore
        #: Whether this process notes the run's writes (`writes_enabled`).
        self.writes = writes
        #: path -> (first write-open as ISO, as ns) for each write noted in
        #: this process. Bounded by MAX_PATHS like `seen`.
        self.written: dict[str, tuple[str, int]] = {}
        self.writes_truncated = False
        #: Paths a write-open of was NOT noted (excluded, ignored, a cache,
        #: through a link into one): judged once, not at every open.
        self.write_skipped: set[str] = set()
        #: path -> the identity last noted for it in the ``.wf.json`` sidecar
        #: (`check_writes`). Bounded by `written`.
        self.write_seen: dict[str, tuple] = {}
        #: Where the last `check_writes` sweep stopped.
        self.write_cursor = 0
        #: path -> the identity last recorded for it. Bounded by MAX_PATHS:
        #: past the cap nothing is added, so a run over millions of files
        #: holds 10,000 entries, not millions.
        self.seen: dict[str, tuple] = {}
        self.count = 0
        self.truncated = False
        self.ambiguous = 0
        #: Budget this run's reads spent in the background hasher.
        self.hashed_bytes = 0
        #: Fingerprints taken because THIS run's budget ran out: this run's
        #: answer, not the file's, so never shared with another run.
        self.budget_results: dict[tuple, tuple[str | None, str | None]] = {}
        #: spool name -> (how far the hasher has read it, whether its lines
        #: there are one of this process's workers') (`_tail_workers`); -1:
        #: not one to tail any more.
        self.tail: dict[str, tuple[int, bool | None]] = {}
        #: Reads queued from workers' spools, bounded by MAX_PATHS.
        self.tailed = 0
        #: Set by `close`: nothing is written for the run any more, and its
        #: folder is never created again (a sweep that was under way when
        #: the run closed would otherwise re-create what the close removed).
        self.closed = False
        self._io = threading.Lock()
        self._fh = None
        self._fh_pid: int | None = None

    def spool(self):
        fh = self._fh
        if fh is not None and self._fh_pid == os.getpid() and not self.closed:
            return fh  # the hot path: every record, no lock
        # `internal()`: opening the spool is Probe's own write -- never judged
        # by the hook, which would take this lock again past the write cap.
        with self._io, internal():
            if self.closed:
                raise OSError(f"recording of run {self.run_id} stopped")
            pid = os.getpid()
            if self._fh is None or self._fh_pid != pid:
                directory = run_dir(self.run_id)
                directory.mkdir(parents=True, exist_ok=True)
                self._fh = open(  # noqa: SIM115
                    directory / f"{_host()}.{pid}.jsonl", "a", buffering=1, encoding="utf-8"
                )
                self._fh_pid = pid
                # Which run what follows is bound to, whose close takes it,
                # and whether that is a binding owner's. Written at EVERY
                # open, and readers take the last: a worker that joins a run
                # of its own appends to the spool its bound hook began.
                self._fh.write(
                    json.dumps({"run": self.run_id, "owner": self.owner, "follows": self.follows}) + "\n"
                )
            return self._fh

    def mark_truncated(self) -> None:
        """Say the read list was cut -- in the spool too: a forked worker's
        cap is otherwise known only to the worker, and the closing process
        reads spools."""
        if not self.truncated:
            self.truncated = True
            with contextlib.suppress(OSError):
                self.spool().write(json.dumps({"truncated": True}) + "\n")

    def record(self, path: str) -> None:
        if self.count >= MAX_PATHS:
            self.mark_truncated()
            return
        # Stat BEFORE remembering the path: an open that failed (a job polling
        # for a file another job has not written yet) must not hide the real
        # read that comes later.
        try:
            st = os.stat(path)
        except OSError:
            return
        if not _stat_is_file(st):
            return
        ident = _ident(st)
        if self.seen.get(path) == ident:
            return
        self.seen[path] = ident
        self.count += 1
        line = {
            "p": path,
            "d": st.st_dev,
            "i": st.st_ino,
            "s": st.st_size,
            "m": st.st_mtime_ns,
            "c": st.st_ctime_ns,
            "t": _now_iso(),
        }
        try:
            self.spool().write(json.dumps(line) + "\n")
        except OSError:
            return
        if os.getpid() == _hasher_pid:
            _hash_queue.put((self.run_id, path, ident))

    def record_write(self, path: str, since: tuple[str, int] | None = None) -> None:
        """Note that the run opened ``path`` for writing (or renamed a noted
        write to it: ``since`` is that write's first time). Once per path per
        process; the file is hashed only at the close, when it is final.

        The note carries the file's identity BEFORE this open (``"b"``: none
        when it did not exist), taken now -- the audit event fires before the
        open happens. At the close a file whose identity is still that one was
        not changed by the run (an append that wrote nothing, a failed open, a
        read-only ``r+``) and is not an output."""
        if path in self.written:
            return
        if len(self.written) >= MAX_PATHS:
            if not self.writes_truncated:
                self.writes_truncated = True
                with contextlib.suppress(OSError):
                    self.spool().write(json.dumps({"wtruncated": True}) + "\n")
            return
        first = since or (_now_iso(), time.time_ns())
        self.written[path] = first
        line = {"w": path, "t": first[0], "n": first[1], "o": uuid.uuid4().hex, "b": _before(path)}
        with contextlib.suppress(OSError):
            self.spool().write(json.dumps(line) + "\n")

    def check_writes(self, *, budget_s: float = WRITE_CHECK_SWEEP_S) -> int:
        """Note each written file whose identity changed since the last look:
        what this process last saw it write, for a recovery to compare with.
        At most ``budget_s`` per call, continuing round-robin. Only the LAST
        identity per path is kept, in this process's ``.wf.json`` sidecar,
        rewritten whole when something changed: a checkpoint rewritten every
        few minutes all week is one entry, not a line per look. Returns how
        many identities changed."""
        paths = list(self.written)
        if not paths or self.closed:
            return 0
        stop = time.monotonic() + budget_s
        start = self.write_cursor % len(paths)
        changed = 0
        for n in range(len(paths)):
            if time.monotonic() >= stop:
                self.write_cursor = (start + n) % len(paths)
                break
            path = paths[(start + n) % len(paths)]
            try:
                st = os.stat(path)
            except OSError:
                continue
            if not _stat_is_file(st):
                continue
            ident = _ident(st)
            if self.write_seen.get(path) == ident:
                continue
            self.write_seen[path] = ident
            changed += 1
        else:
            self.write_cursor = 0
        if changed:
            self._write_sidecar()
        return changed

    def _write_sidecar(self) -> None:
        """``<host>.<pid>.wf.json``: path -> the identity this process last
        saw it have, replaced atomically. Never creates the run's folder: a
        folder the close removed stays removed."""
        body = json.dumps({path: list(ident) for path, ident in self.write_seen.items()})
        with self._io, internal():
            if self.closed:
                return
            target = run_dir(self.run_id) / f"{_host()}.{os.getpid()}{WF_SUFFIX}"
            tmp = target.with_name(target.name + ".tmp")
            try:
                tmp.write_text(body, encoding="utf-8")
                os.replace(tmp, target)
            except OSError:
                with contextlib.suppress(OSError):
                    tmp.unlink()

    def close(self) -> None:
        with self._io:
            self.closed = True
            if self._fh is not None:
                with contextlib.suppress(OSError):
                    self._fh.close()
                self._fh = None


def _stat_is_file(st: os.stat_result) -> bool:
    import stat as _stat

    return _stat.S_ISREG(st.st_mode)


def _before(path: str) -> list | None:
    """A file's identity as a spool list, or None when it is not there (or not
    a regular file): what a write note records as the file BEFORE the open."""
    try:
        st = os.stat(path)
    except OSError:
        return None
    return list(_ident(st)) if _stat_is_file(st) else None


def _hooked_path(path: Any) -> str | None:
    """The path an audit event names, as text, or None. Never raises: it runs
    inside the user's ``open()``, and an object's ``__fspath__`` is user code."""
    try:
        if path is not None and not isinstance(path, (str, bytes)):
            path = os.fspath(path)  # `os.rename` reports the objects it was given
        if isinstance(path, bytes):
            path = os.fsdecode(path)
    except Exception:  # noqa: BLE001
        return None
    return path if isinstance(path, str) else None


#: folder -> (its ``os.path.realpath``, the folder's identity then), per
#: process. Resolving a whole path costs one lstat per component, and the
#: write hook resolves every new path it notes: with the folder cached it
#: costs two lstats (the folder, and whether the file itself is a link).
#: Cleared when full.
_real_dirs: dict[str, tuple[str, tuple]] = {}
_REAL_DIRS_MAX = 4096


def _dir_key(st: os.stat_result) -> tuple:
    """What a cached resolution of a folder is valid for: the entry the path
    reaches (``lstat``: through every link on the way, not the last). A link
    retargeted on the way reaches another folder (another inode); the folder
    itself a link, retargeted, is a new link -- and a new ctime, since an
    inode number can be reused at once."""
    import stat as _stat

    link = _stat.S_ISLNK(st.st_mode)
    return (st.st_dev, st.st_ino, link, st.st_ctime_ns if link else 0)


def _resolved(path: str) -> str:
    """``os.path.realpath(path)`` for an absolute path, from the cached
    resolution of its folder -- valid while the folder is the same entry
    (`_dir_key`) -- and one lstat of the file itself."""
    head, tail = os.path.split(path)
    try:
        key = _dir_key(os.lstat(head))
    except OSError:
        return os.path.realpath(path)
    cached = _real_dirs.get(head)
    if cached is not None and cached[1] == key:
        real = cached[0]
    else:
        real = os.path.realpath(head)
        if len(_real_dirs) >= _REAL_DIRS_MAX:
            _real_dirs.clear()
        _real_dirs[head] = (real, key)
    candidate = os.path.join(real, tail) if tail else real
    return os.path.realpath(candidate) if os.path.islink(candidate) else candidate


def _write_skip(target: "_RunReads", path: str) -> bool:
    """Whether a write-open of ``path`` is never noted: :func:`excluded`, the
    run's ``.probeignore``, a cache -- as opened AND as resolved, so a link
    into ``~/.cache/huggingface`` is a download too. Judged once per path per
    process (``write_skipped``), since the rules do not change."""
    if path in target.write_skipped:
        return True
    real = _resolved(path)
    if (
        excluded(path)
        or write_excluded(path)
        or _ignored(target.ignore, path)
        or (real != path and (excluded(real) or write_excluded(real)))
    ):
        if len(target.write_skipped) < MAX_PATHS:
            target.write_skipped.add(path)
        return True
    return False


def _on_audit(event: str, args: tuple) -> None:
    # ONE function on purpose: `_probe_is_calling` counts frames from here.
    if (not _active and _follow is None) or (event != "open" and event != "os.rename"):
        return
    if getattr(_local, "internal", 0):
        return
    if _follow is not None:
        _follow_binding()
    if event == "os.rename":
        # A noted write renamed (write to `x.tmp`, then `os.replace` onto `x`):
        # the new name is the run's output. Only OUR writes are followed, so a
        # rename of anything else -- Probe's own atomic writes included -- is
        # nothing. A rename relative to a directory fd is not followed.
        try:
            src, dst = _hooked_path(args[0]), _hooked_path(args[1])
            dir_fds = args[2:4]
        except (IndexError, TypeError):
            return
        if src is None or dst is None or any(fd not in (None, -1) for fd in dir_fds):
            return
        _local.internal = getattr(_local, "internal", 0) + 1
        try:
            src = os.path.abspath(src)
            target = _pick_run(src)
            first = target.written.get(src) if target is not None and target.writes else None
            if first is None:
                return
            dst = os.path.abspath(dst)
            # Past the cap `record_write` only says so: nothing to judge.
            if len(target.written) < MAX_PATHS and _write_skip(target, dst):
                return
            target.record_write(dst, since=first)
        except Exception:  # noqa: BLE001 -- an audit hook must never raise into user code
            pass
        finally:
            _local.internal -= 1
        return
    try:
        path, mode, flags = args
    except ValueError:
        return
    reading = _is_read(mode, flags)
    if not reading and not _is_write(mode, flags):
        return
    # The frame that called `open` (an audit hook is called from C). There is
    # none for an open made with no Python code on the stack -- the main
    # script's, at startup -- and an exception here would fail that open.
    try:
        frame = sys._getframe(1)
    except ValueError:
        frame = None
    _note(path, reading=reading, frame=frame)


def _note(path: Any, *, reading: bool, frame: Any) -> None:
    """Record that the run opened ``path`` for reading (or writing), as the
    audit hook does for an ``open``: the hook, and the C-reader wrappers
    (`_readers`), whose libraries open their files where no audit event is
    raised. ``frame`` is the code that opened it, for `_probe_is_calling`.
    Never raises."""
    if getattr(_local, "internal", 0):
        return
    if _follow is not None:
        _follow_binding()
    if not _active:
        return
    path = _hooked_path(path)
    if path is None:
        return
    _local.internal = getattr(_local, "internal", 0) + 1
    try:
        path = os.path.abspath(path)
        target = _pick_run(path)
        if target is None:
            return
        if not reading:
            if not target.writes or path in target.written:
                return
            if len(target.written) >= MAX_PATHS:
                # Past the cap nothing is noted, so nothing is worth judging
                # (the exclusions resolve the path): `record_write` only
                # marks the spool truncated, once.
                target.record_write(path)
                return
            if _write_skip(target, path):
                return
        elif excluded(path) or _ignored(target.ignore, path):
            return
        if _probe_is_calling(frame):
            return
        if reading:
            target.record(path)
        else:
            target.record_write(path)
    except Exception:  # noqa: BLE001 -- an audit hook must never raise into user code
        pass
    finally:
        _local.internal -= 1


def note_read(path: Any) -> None:
    """Record that the current run READ ``path``, exactly as if it had opened
    it with Python's ``open``: for a reader that opens its files from C or
    Rust, which the audit hook cannot see and Probe does not wrap. The same
    exclusions, ``.probeignore`` rules, dedupe and cap apply; with no run
    recording in this process it does nothing. Never raises."""
    _note(path, reading=True, frame=sys._getframe(1))


def _wrapped_read(path: str, frame: Any) -> None:
    _note(path, reading=True, frame=frame)


def _wrapped_write(path: str, frame: Any) -> None:
    _note(path, reading=False, frame=frame)


def _wrapped_active() -> bool:
    """Whether anything may record in this process now: a wrapper with a
    cost of its own asks first (`_readers`)."""
    return (bool(_active) or _follow is not None) and not getattr(_local, "internal", 0)


def _wrapped_truncated() -> None:
    """A wrapped dataset read listed more files than it notes."""
    if not _active or getattr(_local, "internal", 0):
        return
    _local.internal = getattr(_local, "internal", 0) + 1
    try:
        target = _pick_run("")
        if target is not None:
            target.mark_truncated()
    except Exception:  # noqa: BLE001
        pass
    finally:
        _local.internal -= 1


def _pick_run(path: str) -> _RunReads | None:
    bound = _bound_run_id()
    if bound is not None and bound in _active:
        return _active[bound]
    if len(_active) == 1:
        return next(iter(_active.values()))
    for reads in _active.values():
        reads.ambiguous += 1
    return None


def _after_fork_in_child() -> None:
    # A forked worker keeps recording into its OWN spool (pid-named). What the
    # parent's threads held at the fork is gone with them: a lock another
    # thread had taken would never be released here, and the hasher does not
    # exist -- the closing process hashes every spool at the end.
    global _hasher, _hasher_pid, _hasher_queue, _lock, _hash_queue, _budget_lock, _bound, _follow, _owner_guard
    _owner_guard = threading.Lock()  # the fork took it: this copy is the child's, and free
    _lock = threading.RLock()
    _budget_lock = threading.Lock()
    _hash_queue = queue.Queue()
    _hasher = None
    _hasher_pid = None
    _hasher_queue = None
    # The parent's binding of its workers is the parent's; a worker forked
    # while it held one follows it (a persistent DataLoader or Pool worker
    # outlives the run it was forked in) -- and never holds the parent's
    # owner lock, whose release is how a worker learns the parent died.
    if _bound is not None and _bound.get("run") is not None:
        _follow = {
            "file": _bound["file"],
            "lock": _bound["lock"],
            "run": _bound["run"],
            "owner": _bound["pid"],
        }
    _bound = None
    _drop_owner_identity()
    if _follow is not None:
        _follow.update(next=0.0, sig=None, dead=False, alive_next=0.0)
    followed = _follow["run"] if _follow is not None else None
    for reads in _active.values():
        reads._io = threading.Lock()
        # Its parent binds the workers, never a forked child of it.
        reads.children = False
        reads.follows = reads.run_id == followed
        reads._fh = None
        reads._fh_pid = None
        # The child records its own reads into its own spool, from zero: the
        # parent's cap and dedupe say nothing about what the child opens.
        reads.seen = {}
        reads.count = 0
        reads.truncated = False
        reads.written = {}
        reads.writes_truncated = False
        reads.write_seen = {}
        reads.write_cursor = 0
        reads.tail = {}
        reads.tailed = 0
    _open_runs.clear()  # the parent's handles; a child opens its own


# -- spawned workers (F5) ------------------------------------------------------
#
# `probe.init()` binds the Python workers its process starts by spawn or
# forkserver (a DataLoader's, a multiprocessing Pool's, a subprocess running
# Python) to its run: the child hook `probe exec` uses (CHILD_SITE_CODE, through
# PYTHONPATH) spools their reads and writes into the run's folder, and this
# process's close collects them. The protocol, so nothing lands in the wrong run:
#
# * Only while exactly ONE run is open here (`_rebind`, after every run opens,
#   closes, starts or stops recording): with two -- even one that opted out
#   of recording -- a worker's reads belong to neither for sure.
# * The environment carries the binding for NEW workers; a binding FILE
#   (`<state>/probe/bind/<host>.<pid>.<nonce>.json`, BIND_ENV) carries it for
#   workers already running. Each worker -- spawned, forkserver'd, or forked
#   from this process (`_follow`) -- looks at it every BIND_CHECK_S: gone, it
#   stops recording; another run, it spools into that run's folder instead.
# * The owner holds an exclusive lock on ``<...>.lock`` beside it for its
#   whole life. A worker that can take a shared lock on it knows the owner
#   died (a crash leaves the file) and stops for good; the nonce in the name
#   keeps a new process that reuses the owner's pid from being followed.
# * Every spool line block starts with a header naming its run, the owner
#   that closes it and whether it is a FOLLOWER of that owner's binding; the
#   owner's close takes a live follower's spool (never a rank's, never a
#   worker that only inherited the run by a fork), and cuts at the close any
#   line spooled after it (a follower's last BIND_CHECK_S), so a read made
#   after the close is never the closed run's.
# * The owner's environment is restored when the run stops recording (finish,
#   or a second run opening), so later workers are not bound to a closed run.
# * An opt-out propagates: a worker opening a run of its own (or opting out)
#   leaves the binding -- its hook off, the variables gone from ITS
#   environment -- so its own workers are not bound to the owner's run either.

try:
    import fcntl as _fcntl
except ImportError:  # no flock (Windows): an owner's liveness is its pid's
    _fcntl = None  # type: ignore[assignment]

#: This process's binding (the owner side): pid, run, file, lock, the site
#: folder on PYTHONPATH, what PYTHONPATH was set to, and each variable's value
#: before binding. None when unbound.
_bound: dict | None = None
#: A forked worker following its parent's binding: file, lock, run, owner pid,
#: when to look next, the file's signature when last read, and whether the
#: owner was found dead.
_follow: dict | None = None
_BIND_VARS = ("PYTHONPATH", CHILD_DIR_ENV, OWNER_PID_ENV, BIND_ENV)
#: This process as a binding owner: pid, nonce, the binding's base path and
#: the fd holding its lock (`_owner_identity`).
_owner: dict | None = None


#: Held while the owner's lock fd is opened and published in `_owner`, and
#: by a Python-level fork (`_before_fork`) for as long as the fork takes: a
#: fork from another thread in between would give the child a copy of the fd
#: it does not know to close -- and a child holding it keeps the lock taken
#: after the owner died.
_owner_guard = threading.Lock()


def _before_fork() -> None:
    _owner_guard.acquire()


def _after_fork_in_parent() -> None:
    _owner_guard.release()


def _owner_identity() -> dict:
    """This process as a binding owner, made once: a nonce (a process that
    reuses this pid later is another owner) and an exclusive lock on the
    binding's ``.lock`` file, held until this process ends."""
    global _owner
    folder = state_dir().parent / "bind"
    if _owner is not None and _owner["pid"] == os.getpid() and _owner["folder"] == str(folder):
        return _owner
    _drop_owner_identity()
    nonce = uuid.uuid4().hex[:16]
    base = folder / f"{_host()}.{os.getpid()}.{nonce}"
    with internal():
        base.parent.mkdir(parents=True, exist_ok=True)
    with _owner_guard, internal():
        fd = os.open(f"{base}.lock", os.O_RDWR | os.O_CREAT, 0o600)
        _owner = {"pid": os.getpid(), "nonce": nonce, "base": str(base), "fd": fd, "folder": str(folder)}
        if _fcntl is not None:
            try:
                _fcntl.flock(fd, _fcntl.LOCK_EX | _fcntl.LOCK_NB)
            except OSError:
                _owner = None
                os.close(fd)
                raise
    return _owner


def _drop_owner_identity() -> None:
    """Close an owner fd this process holds but is not (a forked child's
    copy of its parent's: closing it does not release the parent's lock)."""
    global _owner
    owner, _owner = _owner, None
    if owner is not None and owner.get("fd") is not None:
        with contextlib.suppress(OSError):
            os.close(owner["fd"])


def _reset_owner_identity() -> None:
    """Forget this process's owner identity and release its lock (tests: a
    crashed owner, then a new process with its pid)."""
    _drop_owner_identity()


def _owner_alive(lock_path: str, pid: int | None = None) -> bool:
    """Whether the process that holds ``lock_path`` exclusively is alive: a
    shared lock on it can be taken only once it has ended (a crash included).
    Without flock, whether ``pid`` is alive. Never for this process's own
    lock (on NFS the test would release it): the callers skip it."""
    if _fcntl is None:
        return pid is None or _pid_alive(pid)
    try:
        fd = os.open(lock_path, os.O_RDONLY)
    except OSError:
        return False
    try:
        try:
            _fcntl.flock(fd, _fcntl.LOCK_SH | _fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        except OSError:
            return True  # a filesystem without locks: trust the file
        _fcntl.flock(fd, _fcntl.LOCK_UN)
        return False
    finally:
        os.close(fd)


def _open_runs_changed() -> None:
    """A run opened or closed in this process (`_open_runs`): bind or unbind."""
    try:
        with _lock:
            _rebind()
    except Exception:  # noqa: BLE001
        pass


_open_runs.listen(_open_runs_changed)


def bind_workers(run_id: str) -> bool:
    """``probe.init()``'s half of F5: this process's spawned and forkserver
    Python workers may be bound to ``run_id`` -- and are, while it is the
    only run open here. Returns whether they are bound now. Never raises."""
    try:
        with _lock:
            state = _active.get(run_id)
            if state is None:
                return False
            state.children = True
            _rebind()
            return _bound is not None and _bound["run"] == run_id
    except Exception as exc:  # noqa: BLE001 -- recording is never a gate
        _diagnostics.warn(f"probe: spawned workers' reads not bound to the run: {exc}")
        return False


def _rebind() -> None:
    """Bind the workers to this process's ONE open run, when it records and
    asked for it; otherwise unbind them. Called with `_lock` held, after
    every change to `_active` or to the open runs."""
    if _bound is not None and _bound["pid"] != os.getpid():
        return
    want = None
    if len(_active) == 1:
        only = next(iter(_active.values()))
        if only.children and not only.closed and not _open_runs.another_open(only.run_id):
            want = only
    have = _bound["run"] if _bound is not None else None
    if (want.run_id if want is not None else None) == have:
        return
    try:
        if want is None:
            _unbind()
        else:
            _bind(want)
    except Exception as exc:  # noqa: BLE001
        _diagnostics.warn(f"probe: spawned workers' binding not updated: {exc}")


def _without_probe_sites(value: str | None) -> list[str]:
    """PYTHONPATH's entries as given -- an EMPTY one (the working folder)
    included -- without Probe's own hook folders."""
    parts = value.split(os.pathsep) if value else []
    return [p for p in parts if not (p and _is_probe_site(p))]


def _bind(state: "_RunReads") -> None:
    global _bound
    pid = os.getpid()
    site = _write_site(state.run_id)
    owner = _owner_identity()
    path = Path(owner["base"] + ".json")
    record = {
        "run": state.run_id,
        "dir": str(run_dir(state.run_id)),
        "writes": state.writes,
        "owner": pid,
        "nonce": owner["nonce"],
    }
    with internal():
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_text(json.dumps(record), encoding="utf-8")
        os.replace(tmp, path)
    if _bound is None:
        _bound = {"pid": pid, "run": None, "file": str(path), "lock": owner["base"] + ".lock",
                  "site": None, "written": None,
                  "saved": {name: os.environ.get(name) for name in _BIND_VARS}}
    pythonpath = os.pathsep.join([str(site), *_without_probe_sites(os.environ.get("PYTHONPATH"))])
    os.environ["PYTHONPATH"] = pythonpath
    os.environ[CHILD_DIR_ENV] = str(run_dir(state.run_id))
    os.environ[OWNER_PID_ENV] = str(pid)
    os.environ[BIND_ENV] = str(path)
    _bound.update(run=state.run_id, site=str(site), written=pythonpath)


def _unbind() -> None:
    """Workers stop (their binding file is gone), and the environment is
    what it was before binding -- each variable only if it is still ours;
    PYTHONPATH exactly as it was if nobody changed it since, else without
    our hook folder only."""
    global _bound
    bound, _bound = _bound, None
    if bound is None:
        return
    with internal(), contextlib.suppress(OSError):
        os.unlink(bound["file"])
    saved = bound["saved"]
    current = os.environ.get("PYTHONPATH")
    if current == bound["written"]:
        if saved["PYTHONPATH"] is None:
            os.environ.pop("PYTHONPATH", None)
        else:
            os.environ["PYTHONPATH"] = saved["PYTHONPATH"]
    elif current is not None:
        rest = [p for p in current.split(os.pathsep) if p != bound["site"]]
        if rest or saved["PYTHONPATH"] is not None:
            os.environ["PYTHONPATH"] = os.pathsep.join(rest)
        else:
            os.environ.pop("PYTHONPATH", None)
    ours = {
        CHILD_DIR_ENV: str(run_dir(bound["run"])) if bound["run"] else None,
        OWNER_PID_ENV: str(bound["pid"]),
        BIND_ENV: bound["file"],
    }
    for name, value in ours.items():
        if os.environ.get(name) != value:
            continue  # someone else set it since
        if saved[name] is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = saved[name]


def _mark_closed(run_id: str) -> None:
    """``closed.<host>.<pid>.json`` in the run's folder: when this process
    stopped recording the run it had bound its workers to. A collect (this
    close's, or a later recovery's) drops what a worker bound through this
    process spooled after it."""
    with internal(), contextlib.suppress(OSError):
        (run_dir(run_id) / f"closed.{_host()}.{os.getpid()}.json").write_text(
            json.dumps({"at": _now_iso(), "owner": os.getpid()}), encoding="utf-8"
        )


def _follow_binding() -> None:
    """A forked worker of a binding owner: at most every BIND_CHECK_S, look
    at the binding file and follow it -- stop recording the closed run, and
    record the new one if there is one. An owner that died (its lock free)
    is followed nowhere, for good."""
    follow = _follow
    now = time.monotonic()
    if follow is None or now < follow["next"]:
        return
    follow["next"] = now + BIND_CHECK_S
    _local.internal = getattr(_local, "internal", 0) + 1
    try:
        record: Any = None
        if not follow.get("dead"):
            try:
                st = os.stat(follow["file"])
                sig: tuple | None = (st.st_ino, st.st_mtime_ns, st.st_size)
            except OSError:
                sig = None
            alive = True
            if sig is not None and now >= follow.get("alive_next", 0.0):
                follow["alive_next"] = now + OWNER_CHECK_S
                alive = _owner_alive(follow["lock"], follow["owner"])
            if not alive:
                follow["dead"] = True
            elif sig == follow["sig"]:
                return
            else:
                follow["sig"] = sig
                if sig is not None:
                    try:
                        record = json.loads(Path(follow["file"]).read_text(encoding="utf-8"))
                    except (OSError, ValueError):
                        record = None
        run = record.get("run") if isinstance(record, dict) else None
        if run is not None and not isinstance(run, str):
            run = None
        with _lock:
            if run == follow["run"] and (run is None or run in _active):
                return
            old = _active.pop(follow["run"], None) if follow["run"] else None
            if old is not None:
                old.close()
            follow["run"] = run
            if run is not None:
                state = _RunReads(run, None, writes=bool(record.get("writes")), owner=follow["owner"])
                state.follows = True
                _active[run] = state
    except Exception:  # noqa: BLE001 -- a worker that cannot follow records nothing new
        pass
    finally:
        _local.internal -= 1


def _leave_inherited_binding() -> None:
    """A worker bound to another process's run opens a run of its own (or
    opts out): it stops recording into the owner's run, quietly (the owner
    did not opt out), and drops the binding from its environment, so its own
    workers are not bound to the owner's run either."""
    global _follow
    state = getattr(sys, "_probe_reads_state", None)
    if isinstance(state, dict):
        state["off"] = True
        state["writes_off"] = True
    with _lock:
        if _follow is not None:
            old = _active.pop(_follow["run"], None) if _follow["run"] else None
            if old is not None:
                old.close()
            _follow = None
    kept = _without_probe_sites(os.environ.get("PYTHONPATH"))
    if kept:
        os.environ["PYTHONPATH"] = os.pathsep.join(kept)
    else:
        os.environ.pop("PYTHONPATH", None)
    for name in (CHILD_DIR_ENV, OWNER_PID_ENV, BIND_ENV):
        os.environ.pop(name, None)


def _install() -> None:
    global _installed
    with _lock:
        if _installed:
            return
        _interpreter_prefixes()
        sys.addaudithook(_on_audit)
        with contextlib.suppress(AttributeError):
            os.register_at_fork(
                before=_before_fork, after_in_parent=_after_fork_in_parent, after_in_child=_after_fork_in_child
            )
        # Readers that open files from C (pyarrow, h5py, safetensors) and
        # torch.save: patched when (and only if) they are imported.
        from . import _readers

        _readers.install(_wrapped_read, _wrapped_write, _wrapped_truncated, _wrapped_active)
        _installed = True


def _ensure_hasher() -> None:
    global _hasher, _hasher_pid, _hasher_queue
    with _lock:
        if _hasher is not None and _hasher.is_alive() and _hasher_pid == os.getpid():
            if _hasher_queue is _hash_queue:
                return
            # Left on a queue nothing feeds any more (it was swapped): that
            # one stops once through what it holds, and a hasher starts on
            # the queue reads go to now.
            with contextlib.suppress(Exception):
                _hasher_queue.put(None)
        _hasher_pid = os.getpid()
        _hasher_queue = _hash_queue
        _hasher = threading.Thread(
            target=_hash_loop, args=(_hasher_queue,), name="probe-reads-hasher", daemon=True
        )
        _hasher.start()


def _keep(result: tuple[str | None, str | None], ident: tuple, own: dict) -> None:
    """File the answer where it belongs: a full hash, a fingerprint of a file
    too big to hash, or "moved/unreadable" is the FILE's answer and shared; a
    fingerprint taken only for budget is the run's own."""
    sha, fp = result
    if fp is not None and sha is None and ident[2] <= FULL_HASH_MAX_BYTES:
        own[ident] = result
    else:
        _hash_results[ident] = result


def _check_writes() -> None:
    """Every WRITE_CHECK_S, note what each recording run's written files are
    now (`_RunReads.check_writes`), from the hasher's thread."""
    for state in list(_active.values()):
        if state.writes and state.written:
            try:
                state.check_writes()
            except Exception:  # noqa: BLE001 -- a look costs one recovery its hash
                pass


def _tail_workers() -> None:
    """Queue for hashing what this process's workers spooled since the last
    look -- a forked DataLoader worker, a spawned one (F5): their spool's
    header names this process as the owner; a rank's names itself and is left
    to it. Their reads are then hashed during the run, as this process's own
    are, instead of all at the close, which may not have the time (F7)."""
    me, host = os.getpid(), _host()
    for state in list(_active.values()):
        if state.closed or state.tailed >= MAX_PATHS:
            continue
        try:
            spools = sorted(run_dir(state.run_id).glob(f"{host}.*.jsonl"))
        except OSError:
            continue
        for spool in spools:
            owner = _spool_owner(spool)
            if owner is None or owner[1] == me:
                continue
            # (offset read to, whether the lines there are ours): a header
            # line says, and a later one can say otherwise (a worker that
            # joined a run of its own writes one): from there, not ours.
            offset, mine = state.tail.get(spool.name, (0, None))
            if offset < 0:
                continue
            try:
                with open(spool, "rb") as handle:
                    handle.seek(offset)
                    chunk = handle.read(TAIL_BYTES)
            except OSError:
                continue
            end = chunk.rfind(b"\n")
            if end < 0:
                continue
            state.tail[spool.name] = (offset + end + 1, mine)
            for raw in chunk[: end + 1].splitlines():
                if raw.startswith(b'{"run"'):
                    header = _header(raw.decode("utf-8", "replace")) or {}
                    mine = header.get("owner") == me and header.get("run") == state.run_id
                    state.tail[spool.name] = (offset + end + 1, mine) if mine else (-1, False)
                    if not mine:
                        break
                    continue
                if mine is not True or not raw.startswith(b'{"p"'):
                    continue
                try:
                    row = json.loads(raw)
                    path, ident = row["p"], (row["d"], row["i"], row["s"], row["m"], row["c"])
                except (ValueError, KeyError, TypeError):
                    continue
                if excluded(path) or _ignored(state.ignore, path):
                    continue
                if state.tailed >= MAX_PATHS:
                    break
                state.tailed += 1
                _hash_queue.put((state.run_id, path, ident))


def _hash_loop(work: "queue.Queue | None" = None) -> None:
    """The background hasher, on ``work`` (the queue it was started for):
    taken ONCE, so every item's ``task_done`` goes to the queue the item came
    from even if `_hash_queue` is swapped meanwhile (a test's monkeypatch) --
    marking another queue raised, killed the hasher and left the item counted
    unfinished, and every later close waited its whole wait on that count."""
    work = _hash_queue if work is None else work
    _local.internal = 1
    cache = _HashCache()
    next_check = time.monotonic() + WRITE_CHECK_S
    next_tail = time.monotonic() + TAIL_S
    while True:
        try:
            wait = min(next_check, next_tail) - time.monotonic()
            item = work.get(timeout=max(wait, 0.0))
        except queue.Empty:
            item = False
        if time.monotonic() >= next_check:
            _check_writes()
            next_check = time.monotonic() + WRITE_CHECK_S
        if time.monotonic() >= next_tail:
            try:
                _tail_workers()
            except Exception:  # noqa: BLE001 -- a tail costs the close some work
                pass
            next_tail = time.monotonic() + TAIL_S
        if _open_runs.take_collected():
            # A run handle never finished was collected: one run fewer open.
            _open_runs_changed()
        if item is False:
            continue
        try:
            if item is None:
                return
            run_id, path, ident = item
            reads = _active.get(run_id)
            # A run already collected hashes what it still needs itself,
            # within its own deadline and budget.
            if reads is None or ident in _hash_results or ident in reads.budget_results:
                continue
            budget = [max(RUN_HASH_BUDGET_BYTES - reads.hashed_bytes, 0)]
            before = budget[0]
            result = hash_file(path, ident, cache=cache, budget=budget)
            reads.hashed_bytes += before - budget[0]
            if result is not None:  # None: the budget is spent; the close retries
                _keep(result, ident, reads.budget_results)
        except Exception:  # noqa: BLE001 -- a hash failure costs one read's match
            pass
        finally:
            work.task_done()


class _HashCache:
    """Per-machine sha256 cache keyed on (device, inode, size, mtime, ctime).

    ``batch=N`` holds up to N answers and writes them in ONE transaction
    (:meth:`flush`): a close hashing 2,000 small outputs spent 2.8 s of its
    4.4 s committing them one by one (a sync to disk each)."""

    def __init__(self, *, batch: int = 0) -> None:
        self._batch = batch
        self._pending: list[tuple] = []
        self._db: sqlite3.Connection | None = None
        try:
            path = state_dir().parent / "hashcache.sqlite3"
            path.parent.mkdir(parents=True, exist_ok=True)
            with internal():
                self._db = sqlite3.connect(str(path), timeout=5, check_same_thread=False)
                self._db.execute(
                    "CREATE TABLE IF NOT EXISTS h2 (d INTEGER, i INTEGER, s INTEGER, "
                    "m INTEGER, c INTEGER, sha TEXT, fp TEXT, PRIMARY KEY (d, i, s, m, c))"
                )
        except (OSError, sqlite3.Error):
            self._db = None

    def get(self, ident: tuple) -> tuple[str | None, str | None] | None:
        if self._db is None:
            return None
        try:
            with internal():
                row = self._db.execute(
                    "SELECT sha, fp FROM h2 WHERE d=? AND i=? AND s=? AND m=? AND c=?", ident
                ).fetchone()
        except sqlite3.Error:
            return None
        return (row[0], row[1]) if row else None

    def put(self, ident: tuple, sha: str | None, fp: str | None) -> None:
        if self._db is None:
            return
        self._pending.append((*ident, sha, fp))
        if len(self._pending) > self._batch:
            self.flush()

    def flush(self) -> None:
        rows, self._pending = self._pending, []
        if not rows or self._db is None:
            return
        try:
            with internal(), self._db:
                self._db.executemany(
                    "INSERT OR REPLACE INTO h2 (d, i, s, m, c, sha, fp) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    rows,
                )
        except sqlite3.Error:
            pass


def _take(budget: list[int], cost: int) -> bool:
    """Charge ``cost`` bytes to ``budget`` if it still has them."""
    with _budget_lock:
        if budget[0] < cost:
            return False
        budget[0] -= cost
        return True


def _give_back(budget: list[int], unread: int) -> None:
    with _budget_lock:
        budget[0] += max(unread, 0)


def hash_file(
    path: str,
    ident: tuple,
    *,
    cache: _HashCache | None,
    budget: list[int],
    deadline: float | None = None,
    fingerprint: bool = True,
) -> tuple[str | None, str | None] | None:
    """``(sha256, fingerprint)`` for a file, ``(None, None)`` when it is no
    longer the one observed (unstable) or cannot be read, or None when it was
    NOT HASHED: the I/O ``budget`` cannot pay even for a fingerprint, or
    ``deadline`` (a ``time.monotonic()`` instant) has passed.

    Every byte read is charged to ``budget`` -- a one-element list, shared by
    everything one run hashes: a full hash its size, a fingerprint the edges
    it reads (at most 2 x EDGE_BYTES). A full hash that runs into the deadline
    stops mid-file, is charged what it read, and is None. ``fingerprint=False``
    asks for a full hash or nothing (a reference's ``content_hash``)."""
    with internal():
        if deadline is not None and time.monotonic() >= deadline:
            return None
        try:
            before = _ident(os.stat(path))
        except OSError:
            return (None, None)
        if before != ident:
            return (None, None)
        if cache is not None:
            hit = cache.get(ident)
            if hit is not None and (fingerprint or hit[0] is not None):
                return hit
        size = ident[2]
        sha: str | None = None
        fp: str | None = None
        full = size <= FULL_HASH_MAX_BYTES and _take(budget, size)
        if not full and not (fingerprint and _take(budget, min(size, 2 * EDGE_BYTES))):
            return None
        try:
            if full:
                digest = hashlib.sha256()
                done = 0
                with open(path, "rb") as handle:
                    for chunk in iter(lambda: handle.read(_CHUNK), b""):
                        digest.update(chunk)
                        done += len(chunk)
                        if done < size and deadline is not None and time.monotonic() >= deadline:
                            _give_back(budget, size - done)
                            return None
                sha = digest.hexdigest()
            else:
                digest = hashlib.sha256()
                with open(path, "rb") as handle:
                    digest.update(handle.read(EDGE_BYTES))
                    if size > 2 * EDGE_BYTES:
                        handle.seek(size - EDGE_BYTES)
                    digest.update(handle.read(EDGE_BYTES))
                fp = f"{size}:{ident[3]}:{digest.hexdigest()}"
            after = _ident(os.stat(path))
        except OSError:
            return (None, None)
        if after != ident:
            return (None, None)
        # A fingerprint taken only because THIS run's budget ran out is not
        # the file's answer: cached, it would stand in for the full hash a
        # later run has the budget for.
        if cache is not None and (sha is not None or size > FULL_HASH_MAX_BYTES):
            cache.put(ident, sha, fp)
        return (sha, fp)


def _token_id(client: Any) -> str | None:
    """Which credential a client writes with, as a short one-way digest: two
    tenants on one server must not send each other's leftover reads."""
    settings = getattr(client, "settings", None)
    token = (
        getattr(settings, "token", None)
        or getattr(settings, "service_token", None)
        or getattr(settings, "ingest_token", None)
    )
    if not isinstance(token, str) or not token:
        return None
    return hashlib.sha256(token.encode()).hexdigest()[:16]


def _client_url(client: Any) -> str | None:
    return getattr(getattr(client, "settings", None), "base_url", None)


def start(
    run_id: str,
    *,
    capture_reads: bool | None = None,
    capture_outputs: bool | None = None,
    client: Any = None,
    base_url: str | None = None,
    ignore: Any = None,
    offline_dir: str | os.PathLike | None = None,
) -> bool:
    """Begin recording what this process reads -- and writes, unless
    :func:`writes_enabled` says no for ``capture_outputs`` -- for ``run_id``.
    Returns whether recording started. A no-op when opted out, when ``probe
    exec``'s child hook is already recording this process (``PROBE_READS_DIR``)
    -- an explicit ``capture_reads=False`` then switches that hook off, and
    ``capture_outputs=False`` its writes -- or when the interpreter has no
    audit hooks. ``ignore`` is the run's ``.probeignore`` rules: a read or
    write they exclude is not recorded at all. ``offline_dir``: the run is an
    offline run queued there (a recovery delivers its leftovers into it)."""
    if os.environ.get(CHILD_DIR_ENV):
        owner = os.environ.get(OWNER_PID_ENV)
        if not owner:
            _child_opts_out(
                run_id, reads_off=capture_reads is False, writes_off=not writes_enabled(capture_outputs)
            )
            return False
        if owner != str(os.getpid()):
            # A worker another process bound to its run (F5), opening a run of
            # its own: its reads are its run's from here on, and its own
            # workers are not bound to the other run.
            _leave_inherited_binding()
    if not enabled(capture_reads) or not hasattr(sys, "addaudithook"):
        return False
    try:
        _note_own_dirs(client, offline_dir)
        _install()
        with _lock:
            if run_id in _active:
                return True
            state = _active[run_id] = _RunReads(run_id, ignore, writes=writes_enabled(capture_outputs))
            # A second run: this process's workers belong to neither for sure.
            _rebind()
        _write_owner(
            run_id,
            base_url=base_url or _client_url(client),
            token_id=_token_id(client),
            ignore=ignore,
            offline_dir=offline_dir,
            writes=state.writes,
        )
        _mark_live(run_id)
        _ensure_hasher()
    except Exception as exc:  # noqa: BLE001 -- recording is never a gate
        _diagnostics.warn(f"probe: read capture could not start: {exc}")
        _active.pop(run_id, None)
        return False
    return True


def _child_opts_out(run_id: str, *, reads_off: bool, writes_off: bool) -> None:
    """``probe.init(capture_reads=False)`` / ``capture_outputs=False`` in a
    ``probe exec`` child: switch its hook off, AND say so in its spool, where
    the launcher's collect (or a recovery) reads it -- the hook may have
    spooled reads or writes before this, and owner.json, the launcher's, still
    says they are on. Only into this run's own spool folder."""
    if not reads_off and not writes_off:
        return
    state = getattr(sys, "_probe_reads_state", None)
    if isinstance(state, dict):
        if reads_off:
            state["off"] = True
        if writes_off:
            state["writes_off"] = True
    spool_dir = os.environ.get(CHILD_DIR_ENV) or ""
    if os.path.basename(os.path.normpath(spool_dir)) != run_folder(run_id):
        return
    try:
        with internal(), open(
            os.path.join(spool_dir, f"{_host()}.{os.getpid()}.jsonl"), "a", encoding="utf-8"
        ) as fh:
            if reads_off:
                fh.write(json.dumps({"reads_off": True}) + "\n")
            if writes_off:
                fh.write(json.dumps({"writes_off": True}) + "\n")
    except OSError:
        pass


def is_recording(run_id: str) -> bool:
    return run_id in _active


def _write_owner(
    run_id: str,
    *,
    base_url: str | None = None,
    token_id: str | None = None,
    ignore: Any = None,
    offline_dir: str | os.PathLike | None = None,
    writes: bool = False,
) -> None:
    """``owner.json``: whose spools these are, and the run's ``.probeignore``
    rules (plan (n)), so reads a recovery sends -- the spools of a launcher or
    process that never collected them, a Ctrl-C'd ``probe exec`` among them --
    are filtered exactly as the run's own close would have filtered them.
    ``writes``: whether writes are noted too; a process collecting spools it
    did not record (a launcher, a recovery) sends a write list only then, so
    an empty list never claims "wrote nothing" for a run that opted out."""
    directory = run_dir(run_id)
    record = _ignore.to_record(ignore)
    with internal():
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "owner.json").write_text(
            json.dumps(
                {
                    "run_id": run_id,
                    "pid": os.getpid(),
                    "base_url": base_url,
                    "token_id": token_id,
                    "host": _host(),
                    "started_at": _now_iso(),
                    **({"ignore": record} if record else {}),
                    **({"offline_dir": os.fspath(offline_dir)} if offline_dir else {}),
                    "writes": bool(writes),
                }
            )
        )


def _pid_alive(pid: int) -> bool:
    from .._shared import oscompat

    try:
        oscompat.probe_pid(pid)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _mark_live(run_id: str) -> None:
    """Say this process may still write to ``run_id``'s folder. Spools appear
    lazily, at the first read: without a marker, another rank closing first
    (or recovery) would see an empty folder and delete it under this one."""
    directory = run_dir(run_id)
    with internal():
        directory.mkdir(parents=True, exist_ok=True)
        (directory / f"{_host()}.{os.getpid()}.live").touch()


def _live_here(directory: Path) -> bool:
    """A live process on this host, other than this one, marked the folder."""
    host, me = _host(), os.getpid()
    for marker in directory.glob("*.live"):
        owner = _spool_owner(marker)
        if owner is not None and owner[0] == host and owner[1] != me and _pid_alive(owner[1]):
            return True
    return False


def _live_elsewhere(directory: Path) -> bool:
    """`_live_here`, or a marker from another host, whose pids mean nothing here."""
    host = _host()
    for marker in directory.glob("*.live"):
        owner = _spool_owner(marker)
        if owner is not None and owner[0] != host:
            return True
    return _live_here(directory)


def _drop_markers(directory: Path) -> None:
    """Remove this process's marker and those of this host's ended processes."""
    host, me = _host(), os.getpid()
    for marker in directory.glob("*.live"):
        owner = _spool_owner(marker)
        if owner is not None and owner[0] == host and (owner[1] == me or not _pid_alive(owner[1])):
            with contextlib.suppress(OSError):
                marker.unlink()


def _header(raw: str) -> dict | None:
    """A spool line when it is a header (``{"run", "owner", "follows"}``:
    the run the lines after it are bound to, the process whose close takes
    them, and whether that one is a binding owner the writer follows)."""
    if not raw.startswith('{"run"'):
        return None
    try:
        header = json.loads(raw)
    except ValueError:
        return None
    return header if isinstance(header, dict) else None


def _spool_header(spool: Path, *, last: bool = False) -> dict:
    """A spool's first header, or -- ``last`` -- the one in force now (a
    header is written at every open: a worker that joined a run of its own
    appends to the spool its bound hook began); {} when there is none."""
    found: dict = {}
    try:
        with open(spool, encoding="utf-8", errors="replace") as handle:
            if not last:
                return _header(handle.readline(4096)) or {}
            for raw in handle:
                header = _header(raw)
                if header is not None:
                    found = header
    except OSError:
        return {}
    return found


def _spools(run_id: str, *, closing: bool = False) -> tuple[list[Path], int]:
    """(the spools this process may read and then delete, how many it may not).
    It may take this host's, written by this process or by one that has ended.
    A live rank's or worker's spool is its own to send; another host's pids
    mean nothing here. ``closing``: this process is closing the run, so it
    also takes the live spools of the workers it bound (their header names it
    the owner, and says it FOLLOWS this process's binding, F5) -- they stopped
    recording the run when it did, and what they spooled after is cut. A
    live worker that only inherited the run by a fork, with no binding to
    follow, keeps recording it: its spool is left until it ends."""
    host, me = _host(), os.getpid()
    mine, pending = [], 0
    with internal():
        for spool in sorted(run_dir(run_id).glob("*.jsonl")):
            owner = _spool_owner(spool)
            if owner is None or owner[0] != host:
                continue
            if owner[1] == me or not _pid_alive(owner[1]):
                mine.append(spool)
                continue
            header = _spool_header(spool, last=True) if closing else {}
            if header.get("owner") == me and header.get("follows") is True:
                mine.append(spool)
            else:
                pending += 1
    return mine, pending


def _closed_marks(directory: Path) -> dict[int, datetime]:
    """owner pid -> when it stopped recording the run it had bound its workers
    to (`_mark_closed`), for this host's markers in ``directory``."""
    out: dict[int, datetime] = {}
    for marker in directory.glob(f"closed.{_host()}.*.json"):
        try:
            record = json.loads(marker.read_text(encoding="utf-8"))
            out[int(record["owner"])] = datetime.fromisoformat(record["at"])
        except (OSError, ValueError, KeyError, TypeError):
            continue
    return out


def _after(seen_at: Any, cut: datetime | None) -> bool:
    """Whether a spool line's time is after its binding owner's close."""
    if cut is None or not isinstance(seen_at, str):
        return False
    try:
        return datetime.fromisoformat(seen_at) > cut
    except ValueError:
        return False


def _collectable_spools(run_id: str) -> list[Path]:
    return _spools(run_id)[0]


#: At most this many `.probeignore` rule sets are taken from one run's spools.
MAX_HANDED_RULES = 16


def _sidecar(spool: Path) -> Path:
    """The ``.wf.json`` sidecar beside ``<host>.<pid>.jsonl``."""
    return spool.with_suffix(WF_SUFFIX)


class _SpooledWrites:
    """What a run's spools say about its writes: path -> the EARLIEST note of
    it (``{"w", "t", "n", "o", "b"}``); path -> the identity each recorder
    last saw the file have while it lived (its ``.wf.json`` sidecar, see
    `check_writes`); whether a recorder hit its cap; and whether a process of
    the run opted out after its hook started (``"writes_off"`` /
    ``"reads_off"`` lines, see :func:`start`). ``keep=False`` learns the
    opt-outs only."""

    def __init__(self, keep: bool = True) -> None:
        self.keep = keep
        self.rows: dict[str, dict] = {}
        self.seen: dict[str, set[tuple]] = {}
        self.truncated = False
        self.writes_off = False
        self.reads_off = False

    def add_sidecar(self, spool: Path) -> None:
        """Take in what the recorder of ``spool`` last saw of its writes."""
        if not self.keep:
            return
        try:
            with open(_sidecar(spool), encoding="utf-8") as handle:
                seen = json.load(handle)
        except (OSError, ValueError):
            return
        if not isinstance(seen, dict):
            return
        for path, raw in list(seen.items())[:MAX_PATHS]:
            try:
                ident = tuple(int(v) for v in raw)
            except (TypeError, ValueError):
                continue
            if isinstance(path, str) and len(ident) == 5:
                self.seen.setdefault(path, set()).add(ident)

    def add(self, row: dict) -> None:
        path = row.get("w")
        if not isinstance(path, str) or not self.keep:
            return
        prior = self.rows.get(path)
        if prior is None:
            if len(self.rows) >= MAX_PATHS:
                self.truncated = True
                return
            self.rows[path] = row
        elif str(row.get("t", "")) < str(prior.get("t", "")):
            self.rows[path] = row


def _read_spools(
    spools: list[Path], handed: list[Any] | None = None, writes: _SpooledWrites | None = None
) -> tuple[dict[tuple, dict], bool]:
    """Every observation in these spools, earliest per (path, identity), read
    line by line. True when a recorder hit its cap (it says so in its spool) or
    the spools hold more than MAX_PATHS observations. The ``.probeignore`` rules
    a recorder handed over in its spool (:func:`hand_to_launcher`) are appended
    to ``handed`` when given; the noted WRITES go to ``writes`` when given (and
    are skipped otherwise).

    Lines under a header binding them to ANOTHER run are not this run's and
    are skipped. A worker's lines bound through an owner that has since
    stopped recording the run (F5, `_mark_closed`) are cut there: what it
    spooled after the close is not the closed run's."""
    merged: dict[tuple, dict] = {}
    truncated = full = False
    if handed is None:
        handed = []
    marks: dict[Path, dict[int, datetime]] = {}
    with internal():
        for spool in spools:
            if spool.parent not in marks:
                marks[spool.parent] = _closed_marks(spool.parent)
            this_run, cut = True, None
            if writes is not None:
                writes.add_sidecar(spool)
            try:
                handle = open(spool, encoding="utf-8", errors="replace")  # noqa: SIM115
            except OSError:
                continue
            with handle:
                for raw in handle:
                    header = _header(raw)
                    if header is not None:
                        this_run = header.get("run") in (None, _folder_run(spool.parent.name))
                        owner = header.get("owner")
                        cut = marks[spool.parent].get(owner) if isinstance(owner, int) else None
                        continue
                    if not this_run:
                        continue
                    if raw.startswith(('{"w', '{"reads_off"')):  # write notes, opt-outs
                        if writes is None:
                            continue
                        try:
                            row = json.loads(raw)
                        except ValueError:
                            continue
                        if not isinstance(row, dict):
                            continue
                        if row.get("writes_off"):
                            writes.writes_off = True
                        elif row.get("reads_off"):
                            writes.reads_off = True
                        elif row.get("wtruncated"):
                            writes.truncated = True
                        elif not _after(row.get("t"), cut):
                            writes.add(row)
                        continue
                    if full and '"ignore"' not in raw:
                        continue  # past the cap only a rule line still counts
                    try:
                        row = json.loads(raw)
                        if row.get("truncated"):
                            truncated = True
                            continue
                        if "ignore" in row:
                            rules = _ignore.from_record(row["ignore"])
                            if rules is not None and rules not in handed and len(handed) < MAX_HANDED_RULES:
                                handed.append(rules)
                            continue
                        key = (row["p"], (row["d"], row["i"], row["s"], row["m"], row.get("c")))
                    except (ValueError, KeyError, TypeError, AttributeError):
                        continue
                    if cut is not None and _after(row.get("t"), cut):
                        continue  # a worker's read after its owner's close
                    prior = merged.get(key)
                    if prior is None:
                        if len(merged) >= MAX_PATHS:
                            # Stop taking reads, not rules: a rule line may
                            # sit after the cap.
                            truncated = full = True
                            continue
                        merged[key] = row
                    elif str(row.get("t", "")) < str(prior.get("t", "")):
                        merged[key] = row
    return merged, truncated


def _stop(run_id: str) -> _RunReads | None:
    """Stop recording ``run_id`` in this process -- and in the workers bound
    to it (F5): the close is marked for the collect's cut, then they are
    unbound (or bound to the one run still recording here)."""
    with _lock:
        reads = _active.pop(run_id, None)
        if reads is not None:
            if _bound is not None and _bound["run"] == run_id and _bound["pid"] == os.getpid():
                _mark_closed(run_id)
            reads.close()
        _rebind()
    return reads


_finish_worker: threading.Thread | None = None
#: A close's hashing worker still alive this long after its own deadline is
#: stuck (a read on a stalled mount never returns): later closes stop waiting
#: for it and start their own. A healthy one stops within one chunk's read of
#: its deadline (`hash_file` checks it between chunks).
HUNG_AFTER_S = 5.0
#: Collections in progress; the shared results are cleared only when none is.
_collecting = 0


#: Why a file was not hashed at the close: the run's I/O budget, or the time.
CUT_BUDGET, CUT_DEADLINE = "budget", "deadline"


def _hash_within(
    todo: list[tuple[str, tuple]],
    budget: list[int],
    deadline: float,
    own: dict,
    *,
    cut: dict[tuple, str] | None = None,
) -> None:
    """Hash ``todo`` -- what the background hasher did not reach, reads before
    writes, one ``budget`` -- on a daemon thread the caller waits for only
    until ``deadline``: a stalled mount then costs the file its hash, never
    the run its close. One such thread at a time: while an earlier close's is
    still at work this one WAITS for it (never past ``deadline``), so a
    stalled one is not joined by another thread on the same mount, and a busy
    one (a recovery hashing at init) does not cost this close every hash. A
    worker still alive HUNG_AFTER_S past its own deadline is stuck for good
    and is not waited for: every later close would otherwise spend its whole
    wait on it and hash nothing. Each file ``hash_file`` declined is named in
    ``cut`` with why."""
    global _finish_worker
    if not todo or time.monotonic() >= deadline:
        return

    def work() -> None:
        _local.internal = 1
        cache = _HashCache(batch=256)
        try:
            for path, ident in todo:
                if time.monotonic() >= deadline:
                    return
                if ident in _hash_results or ident in own:
                    continue
                try:
                    result = hash_file(path, ident, cache=cache, budget=budget, deadline=deadline)
                except Exception:  # noqa: BLE001
                    continue
                if result is None:
                    if cut is not None:
                        cut[ident] = CUT_DEADLINE if time.monotonic() >= deadline else CUT_BUDGET
                    continue
                _keep(result, ident, own)
        finally:
            cache.flush()

    while True:
        with _lock:
            busy = _finish_worker if _finish_worker is not None and _finish_worker.is_alive() else None
            hung_at = None
            if busy is not None:
                due = getattr(busy, "probe_deadline", None)
                hung_at = None if due is None else due + HUNG_AFTER_S
                if hung_at is not None and time.monotonic() >= hung_at:
                    busy = None  # stuck: left to its mount, never waited on again
            if busy is None:
                worker = threading.Thread(target=work, name="probe-reads-finish", daemon=True)
                worker.probe_deadline = deadline  # type: ignore[attr-defined]
                _finish_worker = worker
                worker.start()
                break
        busy.join(max(min(deadline, hung_at or deadline) - time.monotonic(), 0.0))
        if time.monotonic() >= deadline:
            return
    worker.join(max(deadline - time.monotonic(), 0.0))


def _stat_writes(paths: list[str], until: float) -> dict[str, tuple | None]:
    """What each written file is NOW: its identity, or None when it is gone or
    not a regular file. On a thread of its own -- never the hashing worker, so
    a busy one cannot starve it -- that the caller waits for until ``until``;
    a path not reached by then is absent from the answer."""
    found: dict[str, tuple | None] = {}
    if not paths:
        return found

    def work() -> None:
        _local.internal = 1
        for path in paths:
            if time.monotonic() >= until:
                return
            try:
                st = os.stat(path)
            except OSError:
                found[path] = None
                continue
            found[path] = _ident(st) if _stat_is_file(st) else None

    worker = threading.Thread(target=work, name="probe-writes-stat", daemon=True)
    worker.start()
    worker.join(max(until - time.monotonic(), 0.0))
    return dict(found)


_HEX64 = re.compile(r"[0-9a-f]{64}")
_HEX32 = re.compile(r"[0-9a-f]{32}")
#: `hash_file`'s fingerprint: size, mtime_ns, sha256 of the edges.
_FINGERPRINT = re.compile(r"[0-9]+:-?[0-9]+:[0-9a-f]{64}")
#: What `_now_iso()` writes into a spool's "t".
_ISO_INSTANT = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,9})?(?:Z|[+-][0-9]{2}:[0-9]{2})")


def _valid_instant(seen_at: Any) -> bool:
    """Whether a spool's "t" is the ISO instant this module (or the child hook)
    wrote. Anything else is a corrupt or edited spool line."""
    return isinstance(seen_at, str) and bool(_ISO_INSTANT.fullmatch(seen_at))


def _read_observation(run_id: str, host: str, path: str, ident: tuple) -> str:
    """A read's observation id (0290, F7), in the shape write rows carry (32
    hex): DERIVED from what identifies the read -- the run, this host, the path
    and the file's identity when read -- so every report of it (the close's, a
    replay, a recovery, a late hash) carries the same one, and the server
    replaces the read's unhashed row instead of adding a second."""
    raw = "\0".join((run_id, host, path, ":".join(str(v) for v in ident)))
    return hashlib.sha256(raw.encode("utf-8", "surrogatepass")).hexdigest()[:32]


def _typed_row(
    path: str,
    sha: Any,
    fp: Any,
    size: Any,
    host: str,
    stable: bool,
    seen_at: Any,
    observation_id: str | None = None,
) -> dict | None:
    """One read row, sanitized BY TYPE instead of by a generic walk (plan (k)),
    or None when its timestamp is not one this module wrote.

    A read list used to reach the wire through the journal's `default_scrub`,
    which walks every key and value of every row, several times -- ~200k
    `scrub_string` calls for 10k rows. Most of a row cannot hold a credential
    by construction: a hash is 64 hex digits or it is dropped, a size is an int,
    a timestamp is the ISO instant this module wrote. Only the PATH is free
    text a person chose, and it is scrubbed exactly once, here.

    `scrub_string`, not `scrub_text`: `scrub_text` also rewrites every home path
    to `<path>` (a traceback's username), which would erase the input -- the
    server keys reads on the path and matches a fingerprint to a reference at
    the same host and path. `scrub_string` is what the journal's scrub did to
    this field before, so the stored path is unchanged.

    A malformed timestamp DROPS the row (the caller counts it in coverage as
    ``malformed_rows``): the server requires ``first_seen_at``, and stamping the
    collect time in its place would record a read at a moment it did not happen.
    """
    if not _valid_instant(seen_at):
        return None
    from . import redaction

    row = {
        "path": redaction.scrub_string(path),
        "content_hash": sha if isinstance(sha, str) and _HEX64.fullmatch(sha) else None,
        "fingerprint": fp if isinstance(fp, str) and _FINGERPRINT.fullmatch(fp) else None,
        "size_bytes": size if isinstance(size, int) and not isinstance(size, bool) and size >= 0 else None,
        "host": host,
        "stable": bool(stable),
        "first_seen_at": seen_at,
    }
    # With an id the server keys on the host as well, and bounds it in bytes:
    # a host past that sends the row as before, keyed on (path, hash).
    if (
        isinstance(observation_id, str)
        and _HEX32.fullmatch(observation_id)
        and len(host.encode("utf-8", "surrogatepass")) <= MAX_OBSERVATION_HOST_BYTES
    ):
        row["observation_id"] = observation_id
    return row


def _iso_from_ns(ns: Any) -> str | None:
    """An mtime in ns as the ISO instant the server stores (UTC, microseconds)."""
    if not isinstance(ns, int) or isinstance(ns, bool):
        return None
    try:
        whole, rest = divmod(ns, 1_000_000_000)
        return datetime.fromtimestamp(whole, UTC).replace(microsecond=rest // 1000).isoformat()
    except (OverflowError, OSError, ValueError):
        return None


def _typed_output_row(
    path: str,
    sha: Any,
    fp: Any,
    size: Any,
    host: str,
    written_at: Any,
    modified_at: Any,
    observation_id: Any,
) -> dict | None:
    """One write row in the contract's shape and key order (``POST
    /v1/runs/{id}/outputs``), sanitized by type like :func:`_typed_row`: only
    the path is free text and scrubbed here; an unhashed file's
    ``content_hash`` is ``""``. None when a time or the observation id is not
    one this module (or the child hook) wrote."""
    if not (_valid_instant(written_at) and _valid_instant(modified_at)):
        return None
    if not (isinstance(observation_id, str) and _HEX32.fullmatch(observation_id)):
        return None
    from . import redaction

    return {
        "path": redaction.scrub_string(path),
        "host": host,
        "content_hash": sha if isinstance(sha, str) and _HEX64.fullmatch(sha) else "",
        "fingerprint": fp if isinstance(fp, str) and _FINGERPRINT.fullmatch(fp) else None,
        "size_bytes": size if isinstance(size, int) and not isinstance(size, bool) and size >= 0 else None,
        "first_written_at": written_at,
        "last_modified_at": modified_at,
        "observation_id": observation_id,
    }


def _changed(ident: tuple, note: dict) -> bool:
    """Whether the file (identity ``ident``, now) is not what it was before
    the run first opened it for writing (the note's ``"b"``: none when the
    open created it). Device, inode, size, mtime and ctime -- which a program
    cannot set back, unlike the mtime ``shutil.copy2`` copies -- all compared,
    so no clock is trusted: an append that wrote nothing, a failed open or a
    read-only ``r+`` leaves every one of them where it was."""
    if "b" not in note:
        return True
    before = note["b"]
    return before is None or list(ident) != list(before)


#: The write-stat's share of a close's wait: up to this fraction of it, at
#: least WRITE_STAT_MIN_S (never more than the wait), at most WRITE_STAT_MAX_S.
WRITE_STAT_SHARE = 0.25
WRITE_STAT_MIN_S = 1.0
WRITE_STAT_MAX_S = 5.0


class Collected(NamedTuple):
    """``collect_all``'s answer, each list in the server's row shape.
    ``opted_out``: the lists (``"inputs"`` / ``"outputs"``) a process of the
    run switched off after its hook had started (a ``probe exec`` child's own
    ``probe.init(capture_...=False)``): never sent, not even empty."""

    inputs: list
    inputs_coverage: dict
    outputs: list
    outputs_coverage: dict
    opted_out: tuple = ()
    #: What the close ran out of TIME to hash (not budget): each read
    #: (``{"p", "i", "t", "o"}``) and write (``{"w", "i", "t", "o"}``) as it
    #: was sent unhashed, for a later process to hash and re-send under the
    #: same observation id (F7, `_keep_late`).
    late: tuple = ()


def collect(
    run_id: str, *, wait_s: float = FINISH_WAIT_S, ignore: Any = None
) -> tuple[list[dict], dict]:
    """Stop recording ``run_id`` in this process and build its READ list:
    :func:`collect_all` without the writes. Returns ``(rows, coverage)``."""
    got = collect_all(run_id, wait_s=wait_s, ignore=ignore, writes=False)
    return got.inputs, got.inputs_coverage


def collect_all(
    run_id: str,
    *,
    wait_s: float = FINISH_WAIT_S,
    ignore: Any = None,
    reads: bool = True,
    writes: bool = True,
    recovered: bool = False,
) -> Collected:
    """Stop recording ``run_id`` in this process and build its read and write
    lists.

    Reads: rows in the server's shape, hashed where the budget, stability and
    ``wait_s`` allow; a read not hashed in time is sent unhashed (it cannot
    match, and is not called unstable).

    Writes (``writes``): each noted path is looked at FIRST, on a thread of
    its own with a share of ``wait_s`` (:func:`_stat_writes`); it is an output
    only if it still exists, is a regular file and is not what it was before
    the run opened it (:func:`_changed`). Its final bytes are hashed after
    every read, from the same budget and within the same ``wait_s``; an
    unchanged file is never hashed.

    ``recovered``: the writers are gone (``recover_orphans``), and anything
    may have rewritten their files since. A written file is hashed only if it
    is still exactly as a recorder of the run last saw it (its ``.wf.json``
    sidecar, `_RunReads.check_writes`); otherwise its row goes unhashed, sized and
    dated by nothing but the run's own note, and is counted
    (``unverified_after_exit``).

    ``reads=False`` / ``writes=False``: the server does not take that list, so
    it is neither hashed nor built (the spools are still consumed).

    ``ignore`` is the run's ``.probeignore`` rules, for what this process did
    not filter as it happened: the ``probe exec`` child's spool, whose hook is
    stdlib-only. Excluded paths are dropped BEFORE hashing and counted in the
    coverage's ``probeignore``. Defaults to the rules recording started with.
    Rules a recorder handed over in its spool (a ``probe exec`` child's own
    ``ignore=``, :func:`hand_to_launcher`) apply beside them."""
    global _collecting
    # Counted BEFORE the run leaves `_active`: in between, another collection
    # finishing would see no run and no collection, and clear the shared
    # results this one is about to read.
    with _lock:
        _collecting += 1
    state = _stop(run_id)
    rules = ignore if ignore is not None else (state.ignore if state is not None else None)
    n_ignored = w_ignored = 0
    noted = _SpooledWrites(keep=writes)
    opted_out: list[str] = []
    try:
        started = time.monotonic()
        deadline = started + max(wait_s, 0.0)
        # The spools are complete: this process stopped recording the run
        # (and so did the workers it bound to it).
        spools, pending = _spools(run_id, closing=not recovered)
        _consumed[run_id] = spools
        handed: list[Any] = []
        observed, spool_truncated = _read_spools(spools, handed, writes=noted)
        if noted.reads_off:
            opted_out.append("inputs")
        if noted.writes_off:
            opted_out.append("outputs")
        if not reads or noted.reads_off:
            observed = {}
        rules = _ignore.combine(rules, *handed)
        write_paths: list[str] = []
        w_unsendable = 0
        if writes and not noted.writes_off:
            for path in sorted(noted.rows, key=lambda p: (str(noted.rows[p].get("t", "")), p)):
                if excluded(path) or write_excluded(path):
                    continue
                if _ignored(rules, path):
                    w_ignored += 1
                    continue
                if not _sendable(path):
                    w_unsendable += 1
                    continue
                write_paths.append(path)
        # What each written file is now, BEFORE anything else can spend the
        # wait: the background hasher's queue below, or a busy worker.
        share = min(max(wait_s, 0.0), max(WRITE_STAT_MIN_S, WRITE_STAT_SHARE * wait_s), WRITE_STAT_MAX_S)
        finals = _stat_writes(write_paths, min(deadline, started + share))
        work = _hasher_queue
        if _hasher is not None and _hasher.is_alive() and _hasher_pid == os.getpid() and work is not None:
            # What the hasher took, it finishes first (a dead one finishes nothing).
            while work.unfinished_tasks and _hasher.is_alive() and time.monotonic() < deadline:
                time.sleep(0.05)
        own = dict(state.budget_results) if state is not None else {}
        wanted = [
            (key[0], key[1])
            for key in sorted(observed, key=lambda k: str(observed[k].get("t", "")))
            if key[1] not in _hash_results
            and key[1] not in own
            and not excluded(key[0])
            and not _ignored(rules, key[0])
        ]
        # Writes that are outputs (changed, and -- recovered -- still the
        # writer's), hashed after the reads; the rest are never read.
        verdict: dict[str, str] = {}
        for path in write_paths:
            if path not in finals:
                verdict[path] = "unchecked"  # the close ran out of time before looking
            elif finals[path] is None:
                verdict[path] = "gone"  # deleted before the close (a temp file)
            elif not _changed(finals[path], noted.rows[path]):
                verdict[path] = "unchanged"  # opened for writing, never changed
            elif recovered and finals[path] not in noted.seen.get(path, ()):
                verdict[path] = "unverified"  # may be another run's bytes by now
            else:
                verdict[path] = "output"
                if finals[path] not in _hash_results and finals[path] not in own:
                    wanted.append((path, finals[path]))
        spent = state.hashed_bytes if state is not None else 0
        budget = [max(RUN_HASH_BUDGET_BYTES - spent, 0)]
        cut: dict[tuple, str] = {}
        _hash_within(wanted, budget, deadline, own, cut=cut)
        # What is left pays for output capture's references (F3).
        _keep_reference_budget(run_id, budget)
        from . import redaction

        host = redaction.scrub_string(socket.gethostname())
        rows: list[dict] = []
        late: list[dict] = []
        unhashed = unsendable = malformed = 0
        read_cut = {CUT_BUDGET: 0, CUT_DEADLINE: 0}
        for key in sorted(observed, key=lambda k: (str(observed[k].get("t", "")), k[0])):
            path, ident = key
            if excluded(path):
                continue
            if _ignored(rules, path):
                n_ignored += 1
                continue
            if not _sendable(path):
                unsendable += 1
                continue
            obs = observed[key]
            if not _valid_instant(obs.get("t")):
                malformed += 1  # see `_typed_row`: dropped, never re-dated
                continue
            result = own.get(ident) or _hash_results.get(ident)
            observation = _read_observation(run_id, host, path, ident)
            why = None
            if result is not None:
                sha, fp = result
                stable = sha is not None or fp is not None
            else:
                sha = fp = None
                stable = True
                unhashed += 1
                why = cut.get(ident, CUT_DEADLINE)
                read_cut[why] += 1
            row = _typed_row(path, sha, fp, obs.get("s"), host, stable, obs.get("t"), observation)
            if row is None:
                malformed += 1
                continue
            rows.append(row)
            if why == CUT_DEADLINE and "observation_id" in row:
                late.append({"p": path, "i": list(ident), "t": obs.get("t"), "o": observation})
            if len(rows) >= MAX_PATHS:
                break
        out_rows: list[dict] = []
        counts = {"gone": 0, "unchanged": 0, "unchecked": 0, "unverified": 0}
        w_unhashed = w_unstable = w_malformed = 0
        write_cut = {CUT_BUDGET: 0, CUT_DEADLINE: 0}
        for path in write_paths:
            note = noted.rows[path]
            kind = verdict[path]
            if kind in ("gone", "unchanged", "unchecked"):
                counts[kind] += 1
                continue
            if kind == "unverified":
                # What the run wrote, not what the file holds now.
                counts["unverified"] += 1
                row = _typed_output_row(
                    path, None, None, None, host, note.get("t"), note.get("t"), note.get("o")
                )
            else:
                ident = finals[path]
                result = own.get(ident) or _hash_results.get(ident)
                if result is None:
                    sha = fp = None
                    w_unhashed += 1
                    why = cut.get(ident, CUT_DEADLINE)
                    write_cut[why] += 1
                    if why == CUT_DEADLINE:
                        late.append({"w": path, "i": list(ident), "t": note.get("t"), "o": note.get("o")})
                else:
                    sha, fp = result
                    if sha is None and fp is None:
                        w_unstable += 1  # it changed while it was hashed
                row = _typed_output_row(
                    path, sha, fp, ident[2], host, note.get("t"), _iso_from_ns(ident[3]), note.get("o")
                )
            if row is None:
                w_malformed += 1
                continue
            out_rows.append(row)
            if len(out_rows) >= MAX_PATHS:
                break
    finally:
        with _lock:
            _collecting -= 1
            if not _active and not _collecting:
                _hash_results.clear()
    coverage = {
        "recorder": RECORDER,
        "unseen": list(UNSEEN_READERS),
        "count": len(rows),
        "truncated": bool(state.truncated if state else False) or spool_truncated,
        "ambiguous_opens": state.ambiguous if state else 0,
        "unhashed": unhashed,
        "unsendable_paths": unsendable,
        # Spool lines whose timestamp this module did not write: dropped.
        **({"malformed_rows": malformed} if malformed else {}),
        # Spools of processes still running (a persistent worker, another
        # rank): theirs to send, or recovery's once they end.
        "pending_spools": pending,
        # Reads a `.probeignore` pattern excluded (only those seen here: an
        # in-process read it excludes is never recorded at all).
        **({"probeignore": n_ignored} if n_ignored else {}),
        # Why reads went unhashed: the run's I/O budget, or the close's time.
        **({"hash_cut": {k: v for k, v in read_cut.items() if v}} if unhashed else {}),
    }
    out_coverage = {
        "recorder": RECORDER,
        "unseen": list(UNSEEN_WRITERS),
        "count": len(out_rows),
        "truncated": bool(state.writes_truncated if state else False) or noted.truncated,
        "unhashed": w_unhashed,
        # Changed while it was hashed: sent without a hash.
        "unstable": w_unstable,
        # Noted, but deleted before the close (or no longer a regular file).
        "gone": counts["gone"],
        # Opened for writing but never changed (a failed open, an empty append).
        "unchanged": counts["unchanged"],
        # The close ran out of time before it could look at these.
        "unchecked": counts["unchecked"],
        "unsendable_paths": w_unsendable,
        "pending_spools": pending,
        # Recovered, and no longer provably what the writer left: unhashed.
        **({"unverified_after_exit": counts["unverified"]} if recovered else {}),
        **({"malformed_rows": w_malformed} if w_malformed else {}),
        **({"probeignore": w_ignored} if w_ignored else {}),
        **({"hash_cut": {k: v for k, v in write_cut.items() if v}} if w_unhashed else {}),
    }
    return Collected(rows, coverage, out_rows, out_coverage, tuple(opted_out), tuple(late))


def _server_takes(client: Any, feature: str) -> bool | None:
    """Whether the server takes ``feature``'s list: True, False (it declared
    it does not -- a definite answer), or None (unreachable: ask again later)."""
    try:
        return bool(client.supports_feature(feature))
    except Exception:  # noqa: BLE001
        return None


def _server_takes_reads(client: Any) -> bool | None:
    """Whether the server accepts read lists (see :func:`_server_takes`)."""
    return _server_takes(client, FEATURE)


#: The journal tag on a late hash re-send (`_resend_late`): `probe sync`
#: drops one for a server that would keep it as a second row.
LATE_TAG = "late_hash"


def _journal_rows(
    client: Any, run_id: str, route: str, rows: list[dict], coverage: dict | None, *, tag: str | None = None
) -> None:
    """``rows`` as NON-blocking ``POST /v1/runs/{id}/<route>`` ops of
    BATCH_ROWS each, EACH carrying the coverage (the server stores the same
    object again): a list is lineage evidence and must never hold a run's
    close. An empty list still carries its coverage, so "recorded nothing"
    reads apart from "not recorded". ``coverage=None`` (late hashes, F7)
    sends none: the server would REPLACE the run's with it. ``tag`` marks
    the ops in the queue (a late re-send: `LATE_TAG`, for `probe sync`)."""
    batches = [rows[i : i + BATCH_ROWS] for i in range(0, len(rows), BATCH_ROWS)] or [[]]
    for batch in batches:
        body: dict[str, Any] = {route: batch}
        if coverage is not None:
            body["coverage"] = coverage
        extra = {"tag": tag} if tag is not None else {}
        client.journal.append_http(
            "POST", f"/v1/runs/{run_id}/{route}", body, run_ref=run_id, blocking=False, **extra
        )


def send(client: Any, run_id: str, rows: list[dict], coverage: dict) -> bool:
    """Journal the read list as non-blocking ops. False when it was not sent:
    an unreachable server keeps the spools for recovery; a server that does
    not take reads drops them, since nothing will ever accept them."""
    takes = _server_takes_reads(client)
    if takes is False:
        discard(run_id)
    if not takes:
        _consumed.pop(run_id, None)
        return False
    if _server_takes(client, OBSERVATIONS_FEATURE) is not True:
        rows = [_without_observation(row) for row in rows]
    _journal_rows(client, run_id, "inputs", rows, coverage)
    discard(run_id)
    return True


def send_outputs(client: Any, run_id: str, rows: list[dict], coverage: dict) -> bool:
    """Journal the write list as non-blocking ``POST /v1/runs/{id}/outputs``
    ops -- only to a server that declares ``run_outputs``. Does not touch the
    spools (:func:`_deliver` discards them once)."""
    if _server_takes(client, OUTPUTS_FEATURE) is not True:
        return False
    _journal_rows(client, run_id, "outputs", rows, coverage)
    return True


def _deliver(
    client: Any,
    run_id: str,
    got: Collected,
    *,
    reads: bool,
    writes: bool,
    observations: bool = False,
    keep_late: bool = False,
) -> None:
    """Journal the lists the server takes and the run did not opt out of, then
    drop the spools they came from. ``observations``: the server keys reads
    on their observation id (`OBSERVATIONS_FEATURE`); without it the ids are
    left out. ``keep_late``: what this close ran out of time to hash is kept
    for a later process to hash and re-send (`_keep_late`)."""
    sent_reads = reads and "inputs" not in got.opted_out
    sent_writes = writes and "outputs" not in got.opted_out
    if sent_reads:
        rows = got.inputs if observations else [_without_observation(r) for r in got.inputs]
        _journal_rows(client, run_id, "inputs", rows, got.inputs_coverage)
    if sent_writes:
        _journal_rows(client, run_id, "outputs", got.outputs, got.outputs_coverage)
    if keep_late and observations:
        _keep_late(run_id, [x for x in got.late if ("p" in x and sent_reads) or ("w" in x and sent_writes)])
    discard(run_id)


def _without_observation(row: dict) -> dict:
    return {k: v for k, v in row.items() if k != "observation_id"}


#: A close's leftovers for a later process: ``late.<host>.<pid>.json``.
_LATE_PREFIX = "late."


def _keep_late(run_id: str, late: list[dict]) -> None:
    """Keep what the close ran out of TIME to hash, beside the run's
    ``owner.json`` (which says which server and credential it is for), for
    the next process on this host to hash and re-send (`_resend_late`). Not
    what the budget cut: that was the run's to spend."""
    if not late:
        return
    path = run_dir(run_id) / f"{_LATE_PREFIX}{_host()}.{os.getpid()}.json"
    tmp = path.with_name(path.name + ".tmp")
    with internal(), contextlib.suppress(OSError):
        tmp.write_text(json.dumps({"run_id": run_id, "rows": late[: 2 * MAX_PATHS]}), encoding="utf-8")
        os.replace(tmp, path)


def _late_files(directory: Path) -> list[Path]:
    return sorted(directory.glob(f"{_LATE_PREFIX}{_host()}.*.json"))


def _resend_late(run_id: str, target: Any, *, reads: bool, writes: bool) -> int:
    """Hash what a closed run's close ran out of time for, and send each row
    that now has a hash AGAIN under the same observation id, so the server
    replaces the unhashed row instead of adding one (F7). A file is hashed
    only if it is still exactly what was read (or written): anything since
    is not that read's bytes. Each late file is claimed by ONE process (a
    rename), tried once within FINISH_WAIT_S and the run's budget, and
    removed. No coverage rides along: the run's own stays. Returns how many
    rows were re-sent."""
    global _collecting
    sent = 0
    for late in _late_files(run_dir(run_id)):
        claimed = late.with_name(f"{late.name}.{os.getpid()}.claimed")
        try:
            with internal():
                os.rename(late, claimed)
        except OSError:
            continue  # another process took it
        with _lock:
            _collecting += 1
        try:
            with internal():
                record = json.loads(claimed.read_text(encoding="utf-8"))
            entries = record.get("rows") if isinstance(record, dict) else None
            todo: list[tuple[str, tuple]] = []
            kept: list[tuple[dict, tuple]] = []
            for entry in entries if isinstance(entries, list) else []:
                try:
                    path = entry.get("p", entry.get("w"))
                    ident = tuple(int(v) for v in entry["i"])
                except (AttributeError, KeyError, TypeError, ValueError):
                    continue
                if not isinstance(path, str) or len(ident) != 5:
                    continue
                if ("p" in entry and not reads) or ("w" in entry and not writes):
                    continue
                todo.append((path, ident))
                kept.append((entry, ident))
            own: dict[tuple, tuple[str | None, str | None]] = {}
            _hash_within(todo, [RUN_HASH_BUDGET_BYTES], time.monotonic() + FINISH_WAIT_S, own)
            from . import redaction

            host = redaction.scrub_string(socket.gethostname())
            in_rows: list[dict] = []
            out_rows: list[dict] = []
            for entry, ident in kept:
                result = own.get(ident) or _hash_results.get(ident)
                if result is None or (result[0] is None and result[1] is None):
                    continue  # still unhashed, or no longer those bytes
                sha, fp = result
                if "p" in entry and sha is None:
                    # A read's row is replaced only by a HASH: the server takes
                    # a report without one under a known id as a retry (it
                    # widens the first sighting and nothing else), so a
                    # fingerprint alone would not reach the row.
                    continue
                if "p" in entry:
                    row = _typed_row(entry["p"], sha, fp, ident[2], host, True, entry.get("t"), entry.get("o"))
                    if row is not None and "observation_id" in row:
                        in_rows.append(row)
                else:
                    row = _typed_output_row(
                        entry["w"], sha, fp, ident[2], host, entry.get("t"), _iso_from_ns(ident[3]), entry.get("o")
                    )
                    if row is not None:
                        out_rows.append(row)
            if in_rows:
                _journal_rows(target, run_id, "inputs", in_rows, None, tag=LATE_TAG)
            if out_rows:
                _journal_rows(target, run_id, "outputs", out_rows, None, tag=LATE_TAG)
            sent += len(in_rows) + len(out_rows)
        except Exception:  # noqa: BLE001 -- a late hash is a bonus, never a failure
            pass
        finally:
            with internal(), contextlib.suppress(OSError):
                claimed.unlink()
            with _lock:
                _collecting -= 1
                if not _active and not _collecting:
                    _hash_results.clear()
    return sent


def discard(run_id: str) -> None:
    """Delete the spools this process read (or may read) for ``run_id`` -- never
    a live process's -- and the run's folder once no spool is left in it and no
    live process has marked it."""
    spools = _consumed.pop(run_id, None)
    if spools is None:
        spools = _collectable_spools(run_id)
    directory = run_dir(run_id)
    with internal():
        for spool in spools:
            for path in (spool, _sidecar(spool)):
                with contextlib.suppress(OSError):
                    path.unlink()
        _drop_markers(directory)
        if (
            not any(directory.glob("*.jsonl"))
            and not _late_files(directory)
            and not _live_elsewhere(directory)
        ):
            shutil.rmtree(directory, ignore_errors=True)


def finalize(
    client: Any, run_id: str, *, wait_s: float = FINISH_WAIT_S, ignore: Any = None
) -> None:
    """Collect and send ``run_id``'s reads and writes. Never raises (but lets
    a Ctrl-C through): these lists are lineage evidence, never a reason to
    fail a run's close."""
    try:
        # Asked BEFORE hashing: against a server that cannot take a list,
        # hashing for it up to the run's budget would be work for nothing.
        # Unreachable, the spools stay for the next run on this machine to send.
        takes_reads = _server_takes(client, FEATURE)
        takes_writes = _server_takes(client, OUTPUTS_FEATURE) if _writes_noted(run_id) else False
        if takes_reads is None or takes_writes is None:
            _stop(run_id)
            return
        if not takes_reads and not takes_writes:
            _stop(run_id)
            discard(run_id)
            return
        got = collect_all(
            run_id, wait_s=wait_s, ignore=ignore, reads=takes_reads, writes=takes_writes
        )
        _deliver(
            client,
            run_id,
            got,
            reads=takes_reads,
            writes=takes_writes,
            observations=_server_takes(client, OBSERVATIONS_FEATURE) is True,
            keep_late=True,
        )
    except KeyboardInterrupt:
        # Ctrl-C while the close waits on hashing: stop waiting. The spools
        # stay, and the next run on this host sends them. Then the interrupt
        # goes on: swallowed here, the close it cut short went on to close the
        # run `completed`, as if nobody had pressed Ctrl-C; `Run.finish()`
        # queues `canceled` for it instead (review of #2016).
        _stop(run_id)
        _consumed.pop(run_id, None)
        _diagnostics.warn(f"probe: read capture for run {run_id} left for later (interrupted)")
        raise
    except Exception as exc:  # noqa: BLE001
        _diagnostics.warn(f"probe: read capture for run {run_id} not sent: {exc}")


def _read_owner(run_id: str) -> dict:
    try:
        with internal():
            owner = json.loads((run_dir(run_id) / "owner.json").read_text())
    except (OSError, ValueError):
        return {}
    return owner if isinstance(owner, dict) else {}


def _writes_noted(run_id: str, owner: dict | None = None) -> bool:
    """Whether ``run_id``'s writes were noted: this process's own recorder
    says, else whoever started recording it (``owner.json``). An owner record
    that does not say predates write capture."""
    state = _active.get(run_id)
    if state is not None:
        return state.writes
    owner = _read_owner(run_id) if owner is None else owner
    return owner.get("writes") is True


#: How many runs' reference budgets this process keeps (the oldest go first).
MAX_REFERENCE_BUDGETS = 64


def _keep_reference_budget(run_id: str, budget: list[int]) -> None:
    """``budget`` is what ``run_id``'s close left: hand it to its references."""
    with _lock:
        _reference_budgets.pop(run_id, None)
        _reference_budgets[run_id] = budget
        while len(_reference_budgets) > MAX_REFERENCE_BUDGETS:
            del _reference_budgets[next(iter(_reference_budgets))]


def reference_budget(run_id: str) -> list[int]:
    """What ``run_id``'s close left of its I/O budget (F3): output capture
    hashes the files it records as references from it, after every read and
    write. ONE object per run, whichever window asks and however often
    (``Run.execute`` closes two), so references of one run never spend more
    than its one budget. A run whose reads were not recorded here starts from
    a full budget, shared the same way."""
    with _lock:
        left = _reference_budgets.get(run_id)
        if left is None:
            left = [RUN_HASH_BUDGET_BYTES]
            _reference_budgets[run_id] = left
            while len(_reference_budgets) > MAX_REFERENCE_BUDGETS:
                del _reference_budgets[next(iter(_reference_budgets))]
        return left


def reference_hash(
    path: str, *, budget: list[int], deadline: float, size: int | None = None, mtime_ns: int | None = None
) -> str | None:
    """sha256 of a file output capture records as a REFERENCE (F3: 64 MB to
    1 GiB, not uploaded), so a later read of those bytes can match it -- paid
    from ``budget``, never past ``deadline``. Everything that touches the file,
    its stat included, runs on a daemon thread the caller waits for only until
    then: a stalled mount costs the hash, never the close. None when the file
    is over 1 GiB, changed from the ``size``/``mtime_ns`` capture listed, or
    the budget or the time ran out. The machine's hash cache answers for a
    file this run's write list already hashed."""
    if time.monotonic() >= deadline:
        return None
    box: dict[str, Any] = {}

    def work() -> None:
        _local.internal = 1
        try:
            st = os.stat(path)
            if not _stat_is_file(st) or st.st_size > FULL_HASH_MAX_BYTES:
                return
            if (size is not None and st.st_size != size) or (
                mtime_ns is not None and st.st_mtime_ns != mtime_ns
            ):
                return
            box["result"] = hash_file(
                path, _ident(st), cache=_HashCache(), budget=budget, deadline=deadline, fingerprint=False
            )
        except Exception:  # noqa: BLE001 -- a hash failure costs the reference its hash
            pass

    worker = threading.Thread(target=work, name="probe-reference-hash", daemon=True)
    worker.start()
    worker.join(max(deadline - time.monotonic(), 0.0))
    result = box.get("result")
    sha = result[0] if isinstance(result, tuple) else None
    return sha if isinstance(sha, str) and _HEX64.fullmatch(sha) else None


def abandon(run_id: str) -> None:
    """Stop recording ``run_id`` and leave its spools for recovery."""
    _stop(run_id)
    _consumed.pop(run_id, None)


#: An offline run's id (`offline.LOCAL_PREFIX`): no server knows it yet.
OFFLINE_PREFIX = "local:"


class _OfflineQueue:
    """An offline run's own queue, as the client a recovery delivers to: its
    leftovers join the run's other writes, and ``probe sync`` checks the
    server's features and rewrites ``local:<key>`` when it delivers them."""

    def __init__(self, directory: str) -> None:
        from .journal import Journal

        self.journal = Journal(directory)

    @staticmethod
    def supports_feature(name: str) -> bool:
        return name in (FEATURE, OUTPUTS_FEATURE)


def _offline_queue(owner: dict) -> "_OfflineQueue | None":
    directory = owner.get("offline_dir")
    if not isinstance(directory, str) or not os.path.isdir(directory):
        return None
    try:
        return _OfflineQueue(directory)
    except Exception:  # noqa: BLE001
        return None


def recover_orphans(client: Any, *, now: float | None = None, late_only: bool = False) -> int:
    """Send the read and write lists of processes on this host that ended
    without closing their run -- and the hashes a closed run's close ran out
    of time for (`_resend_late`, F7). Returns how many runs had lists queued.

    A spool is an orphan when it is this host's, its process is gone, it sat
    unchanged for ORPHAN_AGE_S, and its run is not one this process records --
    and only for a run of this client's server and credential: another
    tenant's run would dead-letter here with its reads lost. An OFFLINE run's
    leftovers (``local:<key>``, which no server knows) go into its own queue
    for ``probe sync``, never to this client's server; with its queue gone
    they are dropped. ``late_only``: only the late hashes (a later run of
    this process, `start_recovery`)."""
    sent = 0
    now = time.time() if now is None else now
    _clear_dead_bindings()
    root = state_dir()
    if not root.is_dir():
        return 0
    takes_reads = _server_takes(client, FEATURE)
    takes_writes = _server_takes(client, OUTPUTS_FEATURE)
    takes_late = _server_takes(client, OBSERVATIONS_FEATURE)
    reachable = takes_reads is not None and takes_writes is not None
    url, token = _client_url(client), _token_id(client)
    host, me = _host(), os.getpid()
    with internal():
        candidates = [p for p in root.iterdir() if p.is_dir()]
    for directory in candidates:
        run_id = _folder_run(directory.name)
        if run_folder(run_id) != directory.name or run_id in _active:
            continue  # (a folder no run's `run_folder` names is not a run's)
        offline = run_id.startswith(OFFLINE_PREFIX)
        if not offline and not reachable:
            continue
        try:
            owner = json.loads((directory / "owner.json").read_text())
        except (OSError, ValueError):
            owner = {}
        if not isinstance(owner, dict):
            continue
        if not offline:
            if owner.get("base_url") and url and owner["base_url"] != url:
                continue
            if owner.get("token_id") and token and owner["token_id"] != token:
                continue
        noted = owner.get("writes") is True
        # Late hashes first: a closed run's, complete when written.
        if _late_files(directory):
            late_to = _offline_queue(owner) if offline else client
            if late_to is None or (not offline and takes_late is False):
                for late in _late_files(directory):  # nothing will ever replace those rows
                    with internal(), contextlib.suppress(OSError):
                        late.unlink()
            elif offline or takes_late:
                late_reads = True if offline else bool(takes_reads)
                late_writes = noted and (True if offline else bool(takes_writes))
                if _resend_late(run_id, late_to, reads=late_reads, writes=late_writes):
                    sent += 1
        if late_only:
            continue
        # A live process of the run on this host (the owner, a rank, a probe
        # exec launcher waiting on its child) may still write or send these.
        if _live_here(directory):
            continue
        spools = _collectable_spools(run_id)
        if any(_spool_owner(s) == (host, me) for s in spools):
            continue
        try:
            if any(now - s.stat().st_mtime < ORPHAN_AGE_S for s in spools):
                continue
        except OSError:
            continue
        if not spools:
            _clear_dead_folder(directory, now)
            continue
        if offline:
            target: Any = _offline_queue(owner)
            reads_ok = target is not None
            writes_ok = reads_ok and noted
        else:
            target, reads_ok, writes_ok = client, bool(takes_reads), bool(takes_writes) and noted
        if _recover_one(run_id, spools, owner, target, reads=reads_ok, writes=writes_ok):
            sent += 1
    return sent


def _recover_one(
    run_id: str, spools: list[Path], owner: dict, target: Any, *, reads: bool, writes: bool
) -> bool:
    """Send (or, when nothing takes them, drop) one dead run's leftover spools
    to ``target``. True when lists were queued."""
    if not reads and not writes:
        _consumed[run_id] = spools
        discard(run_id)
        return False
    try:
        got = collect_all(
            run_id,
            wait_s=FINISH_WAIT_S,
            ignore=_ignore.from_record(owner.get("ignore")),
            reads=reads,
            writes=writes,
            recovered=True,
        )
        got.inputs_coverage["recovered"] = True
        got.outputs_coverage["recovered"] = True
        _deliver(
            target,
            run_id,
            got,
            reads=reads,
            writes=writes,
            observations=_server_takes(target, OBSERVATIONS_FEATURE) is True,
        )
        return True
    except Exception:  # noqa: BLE001
        _consumed.pop(run_id, None)
        return False


def recover_offline(run_id: str, queue_dir: str | os.PathLike) -> bool:
    """``probe sync``'s half: move an offline run's own leftover spools (its
    process died before its close queued them) into its queue at
    ``queue_dir``, now, so this sync delivers them. Only spools of this host's
    ENDED processes, and only when no live process of the run is here (an
    offline run still recording keeps its own); no orphan age is waited out,
    since the queue's owner is the one asking. The hashes its close ran out
    of time for are queued too (F7). True when lists were queued."""
    if not str(run_id).startswith(OFFLINE_PREFIX):
        return False
    directory = run_dir(run_id)
    try:
        if not directory.is_dir() or run_id in _active:
            return False
        owner = _read_owner(run_id)
        queued = bool(
            _late_files(directory)
            and _resend_late(
                run_id, _OfflineQueue(os.fspath(queue_dir)), reads=True, writes=owner.get("writes") is True
            )
        )
        if _live_here(directory):
            return queued
        spools = _collectable_spools(run_id)
        if not spools:
            return queued
        return queued | _recover_one(
            run_id,
            spools,
            owner,
            _OfflineQueue(os.fspath(queue_dir)),
            reads=True,
            writes=owner.get("writes") is True,
        )
    except Exception:  # noqa: BLE001 -- lineage never stops a sync
        return False


def _clear_dead_bindings() -> None:
    """Remove the binding files (F5) of this host's owners that ended
    without unbinding (their lock is free): no worker follows them."""
    host, me = _host(), os.getpid()
    with internal():
        for lock in (state_dir().parent / "bind").glob(f"{host}.*.lock"):
            parts = lock.name.split(".")
            try:
                pid = int(parts[1])
            except (IndexError, ValueError):
                continue
            if pid == me:
                # Never this process's own: on NFS flock is a POSIX lock, which
                # its own request never conflicts with and which closing ANY
                # handle to the file drops -- the probe would release the lock
                # it tests, and find this process "dead".
                continue
            if _owner_alive(str(lock), pid):
                continue
            for path in (lock.with_suffix(".json"), lock):
                with contextlib.suppress(OSError):
                    path.unlink()


def _clear_dead_folder(directory: Path, now: float) -> None:
    """A run folder with no spool left: remove it once no process may still
    write its first -- no live marker, and older than ORPHAN_AGE_S."""
    if any(directory.glob("*.jsonl")) or _late_files(directory) or _live_elsewhere(directory):
        return
    try:
        age = now - directory.stat().st_mtime
    except OSError:
        return
    if age < ORPHAN_AGE_S:
        return
    with internal():
        _drop_markers(directory)
        shutil.rmtree(directory, ignore_errors=True)


def start_recovery(client: Any) -> None:
    """Send dead runs' leftover read lists in the background, once per
    process -- and, at every later run it opens, the late hashes of the runs
    it closed since (F7): a sweep's runs each close within a short budget."""
    global _recovery_started
    with _lock:
        late_only = _recovery_started
        _recovery_started = True

    def _run() -> None:
        _local.internal = 1
        try:
            recover_orphans(client, late_only=late_only)
        except Exception:  # noqa: BLE001
            pass

    threading.Thread(target=_run, name="probe-reads-recovery", daemon=True).start()


_recovery_started = False


# -- probe exec: the child's hook ---------------------------------------------


def _readers_source() -> str:
    """`_readers`' source, for the child hook (which cannot import Probe);
    empty when it cannot be read (the child then has no wrappers)."""
    try:
        return (Path(__file__).parent / "_readers.py").read_text(encoding="utf-8")
    except OSError:
        return ""


#: The ``sitecustomize.py`` ``probe exec`` puts first on a Python child's path.
#: Stdlib only (the child's environment may not have Probe installed), no
#: hashing (the launcher hashes), and it chains to any sitecustomize the
#: environment already had -- never to another Probe hook, so a nested
#: ``probe exec`` installs one hook, not one per level. Its state is published
#: as ``sys._probe_reads_state`` so ``probe.init(capture_reads=False)`` in the
#: child can switch it off (``capture_outputs=False``: its writes), and
#: ``probe.init(ignore=[...])`` can give it a ``skip`` test
#: (:func:`hand_to_launcher`). It notes writes (and renames of them) exactly
#: as the in-process hook does. The exclusion lists are this module's, filled
#: in below, so the two recorders cannot drift.
CHILD_SITE_CODE = r"""
import os, sys, json, socket, threading, time, uuid
from datetime import datetime, timezone
try:
    import fcntl
except ImportError:
    fcntl = None

def _probe_site_dir(p):
    p = os.path.abspath(p or ".")
    return (p.endswith(os.sep + "site")
            and (os.sep + "probe" + os.sep + "reads" + os.sep) in p)

def _probe_run_of(spool_dir):
    # The run a spool folder is for: its name, unescaped (`inputs.run_folder`
    # escapes what a folder name cannot carry: `local:<key>` is `local%3A<key>`).
    name = os.path.basename(os.path.normpath(spool_dir))
    if "%" in name:
        from urllib.parse import unquote
        name = unquote(name)
    return name

def _probe_reads_install():
    spool_dir = os.environ.get("PROBE_READS_DIR")
    if not spool_dir or not hasattr(sys, "addaudithook"):
        return
    owner = os.environ.get("PROBE_READS_OWNER_PID") or ""
    if owner == str(os.getpid()):
        return  # the process that bound its workers (F5) records itself
    def env_off(name):
        return (os.environ.get(name) or "1").strip().lower() in ("0", "false", "off", "no")
    if env_off("PROBE_CAPTURE_READS"):
        return
    if getattr(sys, "_probe_reads_state", None) is not None:
        return
    skip_prefixes = set()
    for p in (sys.prefix, sys.base_prefix, sys.exec_prefix):
        if p and p not in __ROOTS__:
            skip_prefixes.add(os.path.abspath(p) + os.sep)
    try:
        import site, sysconfig
        libs = [sysconfig.get_paths().get(n) for n in ("stdlib", "platstdlib", "purelib", "platlib")]
        for p in list(site.getsitepackages()) + [site.getusersitepackages()] + libs:
            if p:
                skip_prefixes.add(os.path.abspath(p) + os.sep)
    except Exception:
        pass
    skip_prefixes.add(os.path.abspath(spool_dir) + os.sep)
    # Probe's own folders: its state and the outbox.
    state_home = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
    for p in (os.path.join(state_home, "probe"), os.environ.get("PROBE_OUTBOX_DIR")):
        if p:
            skip_prefixes.add(os.path.abspath(p) + os.sep)
    skip_prefixes = tuple(skip_prefixes)
    write_skip = tuple(os.path.abspath(os.environ[n]) + os.sep for n in __CACHE_ENVS__ if os.environ.get(n))
    write_parts = __WRITE_PARTS__
    system = __SYSTEM__
    allowed = __ALLOWED__
    parts = __PARTS__
    code = __CODE__
    max_paths = __MAX_PATHS__
    depth = __DEPTH__
    host = "".join(c if c.isalnum() or c in "-_" else "_" for c in (socket.gethostname() or "host"))
    wbits = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
    local = threading.local()
    bind_check = __BIND_CHECK__
    owner_check = __OWNER_CHECK__
    state = {"pid": None, "fh": None, "seen": {}, "count": 0, "off": False,
             "writes_off": env_off("PROBE_CAPTURE_WRITES") or env_off("PROBE_CAPTURE_OUTPUTS"),
             "written": {}, "wcount": 0,
             # The run this process spools into, and whose close takes the spool.
             "dir": spool_dir, "run": _probe_run_of(spool_dir),
             "owner": int(owner) if owner.isdigit() else None,
             # A worker bound through its owner's binding file (F5) follows it.
             "bind": os.environ.get("PROBE_READS_BIND"), "bind_next": 0.0, "bind_sig": None,
             "bind_writes": True}
    sys._probe_reads_state = state

    def probe_calling(frame):
        for _ in range(depth):
            if frame is None:
                return False
            name = frame.f_globals.get("__name__", "")
            if (name == "probe" or name.startswith("probe.")) and name != "probe.sdk._readers":
                return True
            frame = frame.f_back
        return False

    def spool():
        pid = os.getpid()
        if state["pid"] != pid or state["fh"] is None:
            state["fh"] = open(os.path.join(state["dir"], "%s.%d.jsonl" % (host, pid)), "a",
                               buffering=1, encoding="utf-8")
            state["pid"] = pid
            # At every open: the run what follows is bound to, whose close
            # takes it, and whether that is a binding owner this one follows.
            state["fh"].write(json.dumps({"run": state["run"], "owner": state["owner"],
                                          "follows": bool(state["bind"])}) + "\n")
        return state["fh"]

    def owner_alive():
        # The owner holds its binding's lock exclusively while it lives: a
        # shared lock on it can be had only once it ended (a crash too).
        path = state["bind"][:-len(".json")] + ".lock"
        if fcntl is None:
            try:
                os.kill(state["owner"], 0)
            except ProcessLookupError:
                return False
            except Exception:
                return True
            return True
        try:
            fd = os.open(path, os.O_RDONLY)
        except OSError:
            return False
        try:
            try:
                fcntl.flock(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError:
                return True
            except OSError:
                return True
            fcntl.flock(fd, fcntl.LOCK_UN)
            return False
        finally:
            os.close(fd)

    def follow():
        # The owner's binding file, looked at most every `bind_check`: gone,
        # nothing more is recorded; another run, its folder is spooled into;
        # its owner dead (its lock free), nothing more, for good. True while
        # bound to a run. (Only for a worker bound through one.)
        path = state["bind"]
        if not path:
            return True
        now = time.monotonic()
        if now < state["bind_next"] or state.get("bind_dead"):
            return state["run"] is not None
        state["bind_next"] = now + bind_check
        try:
            st = os.stat(path)
            sig = (st.st_ino, st.st_mtime_ns, st.st_size)
        except OSError:
            sig = None
        alive = True
        if sig is not None and now >= state.get("alive_next", 0.0):
            state["alive_next"] = now + owner_check
            alive = owner_alive()
        if not alive:
            state["bind_dead"] = True
            sig = None
        elif sig == state["bind_sig"]:
            return state["run"] is not None
        state["bind_sig"] = sig
        run = where = None
        writes = True
        if sig is not None:
            try:
                with open(path, encoding="utf-8") as fh:
                    record = json.load(fh)
                run, where, writes = record.get("run"), record.get("dir"), record.get("writes", True)
            except Exception:
                run = None
        if not (isinstance(run, str) and isinstance(where, str)):
            run = where = None
        if run != state["run"]:
            if state["fh"] is not None:
                try:
                    state["fh"].close()
                except Exception:
                    pass
            state.update(fh=None, pid=None, run=run, dir=where, seen={}, count=0, capped=False,
                         written={}, wcount=0, wcapped=False)
        state["bind_writes"] = bool(writes)
        return run is not None

    def as_path(p):
        if isinstance(p, bytes):
            return os.fsdecode(p)
        if p is not None and not isinstance(p, str):
            p = os.fspath(p)
            if isinstance(p, bytes):
                return os.fsdecode(p)
        return p if isinstance(p, str) else None

    def never(path):
        return (path.endswith(code) or path.startswith(skip_prefixes)
                or (path.startswith(system) and not path.startswith(allowed))
                or any(part in path for part in parts))

    real_dirs = {}

    def resolved(path):
        # realpath, with the folder's resolution cached while the folder is
        # the same entry (a link retargeted on the way is another one).
        import stat as _stat
        head, tail = os.path.split(path)
        try:
            st = os.lstat(head)
        except OSError:
            return os.path.realpath(path)
        link = _stat.S_ISLNK(st.st_mode)
        key = (st.st_dev, st.st_ino, link, st.st_ctime_ns if link else 0)
        cached = real_dirs.get(head)
        if cached is not None and cached[1] == key:
            real = cached[0]
        else:
            real = os.path.realpath(head)
            if len(real_dirs) >= 4096:
                real_dirs.clear()
            real_dirs[head] = (real, key)
        candidate = os.path.join(real, tail) if tail else real
        return os.path.realpath(candidate) if os.path.islink(candidate) else candidate

    def never_written(path):
        def no(p):
            return (never(p) or p.startswith(write_skip)
                    or any(part in p for part in write_parts))
        if no(path):
            return True
        real = resolved(path)
        return real != path and no(real)

    def before(path):
        try:
            st = os.stat(path)
        except OSError:
            return None
        import stat as _stat
        if not _stat.S_ISREG(st.st_mode):
            return None
        return [st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns]

    def note_write(path, first):
        if path in state["written"]:
            return
        if state["wcount"] >= max_paths:
            if not state.get("wcapped"):
                state["wcapped"] = True
                spool().write(json.dumps({"wtruncated": True}) + "\n")
            return
        state["written"][path] = first
        state["wcount"] += 1
        spool().write(json.dumps({"w": path, "t": first[0], "n": first[1],
                                  "o": uuid.uuid4().hex, "b": before(path)}) + "\n")

    def fresh_pid():
        if state.get("for_pid") != os.getpid():
            # A forked worker records its own reads and writes, from zero, in
            # its own spool.
            state.update(seen={}, count=0, capped=False, written={}, wcount=0, wcapped=False,
                         for_pid=os.getpid())

    def cut():
        if not state.get("capped") and state["fh"] is not None:
            state["capped"] = True
            state["fh"].write(json.dumps({"truncated": True}) + "\n")

    def note(path, writing, frame):
        # One open of `path` -- by `open`, or by a wrapped C reader -- made by
        # the code at `frame`.
        if state["off"] or getattr(local, "busy", False):
            return
        try:
            local.busy = True
            fresh_pid()
            if not follow():
                return
            if writing and (state["writes_off"] or not state["bind_writes"]):
                return
            if not writing and state["count"] >= max_paths:
                cut()
                return
            path = as_path(path)
            if path is None:
                return
            path = os.path.abspath(path)
            if writing and path in state["written"]:
                return
            if writing and state["wcount"] >= max_paths:
                note_write(path, None)  # past the cap: says so once, judges nothing
                return
            if never_written(path) if writing else never(path):
                return
            skip = state.get("skip")
            if skip is not None and skip(path):
                return
            if probe_calling(frame):
                return
            if writing:
                note_write(path, (datetime.now(timezone.utc).isoformat(), time.time_ns()))
                return
            st = os.stat(path)
            import stat as _stat
            if not _stat.S_ISREG(st.st_mode):
                return
            ident = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns, st.st_ctime_ns)
            if state["seen"].get(path) == ident:
                return
            state["seen"][path] = ident
            state["count"] += 1
            spool().write(json.dumps({
                "p": path, "d": st.st_dev, "i": st.st_ino, "s": st.st_size,
                "m": st.st_mtime_ns, "c": st.st_ctime_ns,
                "t": datetime.now(timezone.utc).isoformat()}) + "\n")
        except Exception:
            pass
        finally:
            local.busy = False

    def hook(event, args):
        if (event != "open" and event != "os.rename") or state["off"] or getattr(local, "busy", False):
            return
        fresh_pid()
        if event == "os.rename":
            if state["writes_off"]:
                return
            try:
                local.busy = True
                if not follow() or not state["bind_writes"]:
                    return
                if any(fd not in (None, -1) for fd in args[2:4]):
                    return
                src, dst = as_path(args[0]), as_path(args[1])
                if src is None or dst is None:
                    return
                first = state["written"].get(os.path.abspath(src))
                if first is None:
                    return
                dst = os.path.abspath(dst)
                skip = state.get("skip")
                if state["wcount"] < max_paths and (
                        never_written(dst) or (skip is not None and skip(dst))):
                    return
                note_write(dst, first)
            except Exception:
                pass
            finally:
                local.busy = False
            return
        try:
            path, mode, flags = args
        except Exception:
            return
        if isinstance(mode, str) and mode:
            writing = any(c in mode for c in "wax+")
        elif isinstance(flags, int):
            writing = bool(flags & wbits)
        else:
            return
        try:
            frame = sys._getframe(1)
        except ValueError:  # no Python code on the stack: the main script's open
            frame = None
        note(path, writing, frame)

    sys.addaudithook(hook)

    # Readers that open files from C, and torch.save (`probe.sdk._readers`,
    # the same source): patched as they are imported.
    def active():
        # Whether anything records now (a wrapper with a cost asks first).
        if state["off"] or getattr(local, "busy", False):
            return False
        try:
            local.busy = True
            return follow()
        except Exception:
            return False
        finally:
            local.busy = False

    readers = __READERS__
    if readers:
        try:
            space = {"__name__": "_probe_readers"}
            exec(compile(readers, "<probe readers>", "exec"), space)
            space["install"](lambda p, f: note(p, False, f), lambda p, f: note(p, True, f), cut, active)
        except Exception:
            pass

_probe_reads_install()

def _probe_chain_sitecustomize():
    try:
        import importlib.machinery, importlib.util
        rest = [p for p in sys.path if not _probe_site_dir(p)]
        spec = importlib.machinery.PathFinder.find_spec("sitecustomize", rest)
        if spec is None or spec.loader is None:
            return
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception:
        pass

_probe_chain_sitecustomize()
"""
for _name, _value in (
    ("__SYSTEM__", _SYSTEM_PREFIXES),
    ("__ALLOWED__", _SYSTEM_ALLOWED),
    ("__PARTS__", _TOOL_CACHE_PARTS + _CREDENTIAL_PARTS),
    ("__CODE__", _CODE_SUFFIXES),
    ("__MAX_PATHS__", MAX_PATHS),
    ("__DEPTH__", _PROBE_FRAME_DEPTH),
    ("__ROOTS__", _ROOT_PREFIXES),
    ("__CACHE_ENVS__", _CACHE_ENVS),
    ("__WRITE_PARTS__", _WRITE_ONLY_PARTS),
    ("__READERS__", _readers_source()),
    ("__BIND_CHECK__", BIND_CHECK_S),
    ("__OWNER_CHECK__", OWNER_CHECK_S),
):
    CHILD_SITE_CODE = CHILD_SITE_CODE.replace(_name, repr(_value))
del _name, _value


def hand_to_launcher(run_id: str, rules: Any) -> bool:
    """Under ``probe exec``: give the launcher this process's ``.probeignore``
    ``rules`` (plan (n), #2045 review) -- a child's own ``ignore=`` patterns,
    which the launcher that collects the child's reads never saw.

    Two halves. The child's stdlib hook takes them as its ``skip`` test, so a
    read they exclude from now on is not even spooled (a forked worker
    inherits it). And one line in this process's spool carries the rules, so
    the launcher's :func:`collect` -- or a recovery's -- also drops what was
    spooled before ``probe.init()`` ran, or by a spawned worker's hook. The
    spool is the channel that already runs from child to launcher; nothing
    else is. Returns whether the rules were handed over; never raises."""
    try:
        spool_dir = os.environ.get(CHILD_DIR_ENV)
        if rules is None or not spool_dir or os.path.basename(os.path.normpath(spool_dir)) != run_folder(run_id):
            return False
        record = _ignore.to_record(rules)
        if record is None:
            return False
        state = getattr(sys, "_probe_reads_state", None)
        if isinstance(state, dict):
            state["skip"] = functools.partial(_ignored, rules)
        with internal():
            with open(os.path.join(spool_dir, f"{_host()}.{os.getpid()}.jsonl"), "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"ignore": record}) + "\n")
        return True
    except Exception:  # noqa: BLE001 -- filtering is never a reason to fail init
        return False


def _is_probe_site(path: str) -> bool:
    path = os.path.abspath(path or ".")
    return path.endswith(os.sep + "site") and (os.sep + "probe" + os.sep + "reads" + os.sep) in path


def prepare_child(
    run_id: str,
    env: dict[str, str],
    *,
    client: Any = None,
    base_url: str | None = None,
    ignore: Any = None,
    capture_outputs: bool | None = None,
) -> bool:
    """Give ``probe exec``'s child a read hook: a ``sitecustomize.py`` first on
    ``PYTHONPATH`` and the spool folder in ``PROBE_READS_DIR``. Harmless for a
    child that is not Python (it never reads either). Returns whether it was
    installed; the launcher then finalizes the reads after the child exits.
    Off when the launcher OR the child's own environment opts out. ``ignore``
    (the run's ``.probeignore`` rules) is recorded for a recovery: the child's
    hook spools every read, and the launcher may never collect them. The hook
    notes writes too unless ``capture_outputs=False`` (which the caller also
    puts in the child's environment) or either environment turns them off."""
    if not enabled(None) or not _env_on(env.get(READS_ENV)):
        return False
    try:
        directory = run_dir(run_id)
        site_dir = _write_site(run_id)
        if capture_outputs is False:
            env[WRITES_ENV] = "0"  # the child's hook reads its environment
        # What the child's hook will do: it reads only its environment.
        writes = _env_on(env.get(WRITES_ENV)) and _env_on(env.get(OUTPUTS_ENV))
        _write_owner(
            run_id,
            base_url=base_url or _client_url(client),
            token_id=_token_id(client),
            ignore=ignore,
            writes=writes,
        )
        _mark_live(run_id)
    except OSError as exc:
        _diagnostics.warn(f"probe: read capture for the child could not start: {exc}")
        return False
    # An outer `probe exec`'s hook folder is dropped: one hook per process.
    # Every other entry stays as given (an empty one is the working folder).
    env["PYTHONPATH"] = os.pathsep.join([str(site_dir), *_without_probe_sites(env.get("PYTHONPATH"))])
    env[CHILD_DIR_ENV] = str(directory)
    # A launcher whose own workers are bound (F5) runs this child as a plain
    # `probe exec` child: its launcher, not a binding, collects it.
    env.pop(OWNER_PID_ENV, None)
    env.pop(BIND_ENV, None)
    return True


def _write_site(run_id: str) -> Path:
    """The run's ``site`` folder holding the child hook's ``sitecustomize.py``."""
    site_dir = run_dir(run_id) / "site"
    with internal():
        site_dir.mkdir(parents=True, exist_ok=True)
        (site_dir / "sitecustomize.py").write_text(CHILD_SITE_CODE, encoding="utf-8")
    return site_dir


__all__ = [
    "BIND_ENV",
    "CHILD_DIR_ENV",
    "FEATURE",
    "OUTPUTS_FEATURE",
    "OWNER_PID_ENV",
    "READS_ENV",
    "WRITES_ENV",
    "Collected",
    "abandon",
    "bind_workers",
    "collect",
    "collect_all",
    "discard",
    "enabled",
    "excluded",
    "finalize",
    "hand_to_launcher",
    "internal",
    "is_recording",
    "note_read",
    "prepare_child",
    "recover_orphans",
    "reference_budget",
    "reference_hash",
    "send",
    "send_outputs",
    "start",
    "write_excluded",
    "writes_enabled",
]
