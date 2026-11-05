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
wrapped (:mod:`probe.sdk.capture.lineage.c_readers`, installed only when the library is
imported): ``pyarrow.parquet`` (``read_table``, ``ParquetFile``,
``ParquetDataset``), ``pyarrow.memory_map`` (the Hugging Face ``datasets``
cache), ``h5py.File`` (its mode says read or write), ``safetensors``
(``safe_open``, ``load_file``; ``save_file`` is a write), and ``torch.save``,
a write. Any other reader
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
files written from C or Rust (pyarrow, sqlite -- ``torch.save``, safetensors'
``save_file`` and ``h5py.File`` in a write mode are wrapped) and by processes that are not
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
import hashlib
import json
import os
import queue
import socket
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Any, NamedTuple

from ...run.launch import open_runs as _open_runs
from ...recording_rules import recording_rules as _ignore
from .. import owndirs as _owndirs
from ....foundation.safe_warn import safe_warn as _diagnostics


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
from probe.sdk.capture.lineage.spool.spool import (
    MAX_PATHS,
    WF_SUFFIX,
    WRITE_CHECK_SWEEP_S,
    _before,
    _host,
    _ident,
    _local,
    _mark_live,
    _now_iso,
    _pid_alive,
    _spool_owner,
    _stat_is_file,
    _write_owner,
    internal,
    run_dir,
    run_folder,
    state_dir,
)

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
#: Writers the audit hook cannot see (`torch.save`, safetensors' `save_file`
#: and `h5py.File` in a write mode are wrapped).
UNSEEN_WRITERS = (
    "C/Rust writers (pyarrow, sqlite)",
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
#: The most ``finish()`` spends on reads -- waiting for the background hasher,
#: then hashing what is left -- before sending the rest unhashed.
FINISH_WAIT_S = 30.0
#: How often the owner's hasher tails the spools of its workers (forked or
#: spawned: their header names it) during the run, so their reads are hashed
#: as they happen and not all at the close (F7); and the most it reads of one
#: spool per look.
TAIL_S = 5.0
TAIL_BYTES = 4 << 20
#: How many caller frames to inspect for Probe's own code before calling an
#: open the run's. Probe's file work (fingerprint, snapshot, staging, gate)
#: opens within a few frames of Probe code; a run's read through a deep library
#: stack has library frames nearest.
_PROBE_FRAME_DEPTH = 8

_lock = threading.RLock()
_installed = False
_active: dict[str, "_RunReads"] = {}
_hash_queue: "queue.Queue[tuple[str, str, tuple] | None]" = queue.Queue()
#: identity -> (sha256, fingerprint); (None, None) means the file moved or
#: could not be read. Absent means not hashed (yet).
_hash_results: dict[tuple, tuple[str | None, str | None]] = {}
_hasher: threading.Thread | None = None
_hasher_pid: int | None = None
#: The queue the running hasher takes its items from (`_hash_loop`).
_hasher_queue: "queue.Queue | None" = None
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


def _note_own_dirs(client: Any = None, *extra: Any) -> None:
    """Remember Probe's own folders and the environment's cache folders, as
    prefixes a recorded path must not start with. Additive: a second run
    opening under another outbox adds its own."""
    global _OWN_PREFIXES, _WRITE_SKIP_PREFIXES
    dirs: set[Any] = {state_dir().parent, *(e for e in extra if e)}
    try:
        from ...delivery.journal.paths import default_root, fallback_root

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
    from ..code.sources.directory import SKIP_DIRS
    from ..code.code import _skip_reason

    parts = path.split("/")
    if any(part in SKIP_DIRS for part in parts[:-1]):
        return True
    return _skip_reason(parts[-1]) is not None


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
_READERS_MODULE = "probe.sdk.capture.lineage.c_readers"


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
        #: The run's `.probeignore` rules (`probe.sdk.recording_rules.recording_rules.IgnoreRules`), or
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
        from . import c_readers as _readers

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


def _keep(result: tuple[str | None, str | None, int | None], ident: tuple, own: dict) -> None:
    """File the answer where it belongs: a full hash, a fingerprint of a file
    too big to hash, or "moved/unreadable" is the FILE's answer and shared; a
    fingerprint taken only for budget is the run's own."""
    sha, fp, _rows = result
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
        # scanning disabled: from . import redaction

        # scanning disabled: host = redaction.scrub_string(socket.gethostname())
        host = socket.gethostname()
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
            rows_n: int | None = None
            if result is not None:
                sha, fp, rows_n = result
                stable = sha is not None or fp is not None
            else:
                sha = fp = None
                stable = True
                unhashed += 1
                why = cut.get(ident, CUT_DEADLINE)
                read_cut[why] += 1
            row = _typed_row(path, sha, fp, obs.get("s"), host, stable, obs.get("t"), observation, rows=rows_n)
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
                rows_n = None
                if result is None:
                    sha = fp = None
                    w_unhashed += 1
                    why = cut.get(ident, CUT_DEADLINE)
                    write_cut[why] += 1
                    if why == CUT_DEADLINE:
                        late.append({"w": path, "i": list(ident), "t": note.get("t"), "o": note.get("o")})
                else:
                    sha, fp, rows_n = result
                    if sha is None and fp is None:
                        w_unstable += 1  # it changed while it was hashed
                row = _typed_output_row(
                    path, sha, fp, ident[2], host, note.get("t"), _iso_from_ns(ident[3]), note.get("o"), rows=rows_n
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
            own: dict[tuple, tuple[str | None, str | None, int | None]] = {}
            _hash_within(todo, [RUN_HASH_BUDGET_BYTES], time.monotonic() + FINISH_WAIT_S, own)
            # scanning disabled: from . import redaction

            # scanning disabled: host = redaction.scrub_string(socket.gethostname())
            host = socket.gethostname()
            in_rows: list[dict] = []
            out_rows: list[dict] = []
            for entry, ident in kept:
                result = own.get(ident) or _hash_results.get(ident)
                if result is None or (result[0] is None and result[1] is None):
                    continue  # still unhashed, or no longer those bytes
                sha, fp, rows_n = result
                if "p" in entry and sha is None:
                    # A read's row is replaced only by a HASH: the server takes
                    # a report without one under a known id as a retry (it
                    # widens the first sighting and nothing else), so a
                    # fingerprint alone would not reach the row.
                    continue
                if "p" in entry:
                    row = _typed_row(
                        entry["p"], sha, fp, ident[2], host, True, entry.get("t"), entry.get("o"), rows=rows_n
                    )
                    if row is not None and "observation_id" in row:
                        in_rows.append(row)
                else:
                    row = _typed_output_row(
                        entry["w"], sha, fp, ident[2], host, entry.get("t"), _iso_from_ns(ident[3]), entry.get("o"),
                        rows=rows_n,
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


def _named_hash(paths: list[tuple[str, tuple]], wait_s: float) -> dict[tuple, tuple]:
    """Hash ``paths`` with one run budget, on the close's guarded worker
    (a stalled mount costs a hash, never the step). The answers by identity."""
    global _collecting
    own: dict[tuple, tuple] = {}
    with _lock:
        _collecting += 1
    try:
        _hash_within(list(paths), [RUN_HASH_BUDGET_BYTES], time.monotonic() + max(wait_s, 0.0), own)
        return {ident: own.get(ident) or _hash_results.get(ident) for _path, ident in paths}
    finally:
        with _lock:
            _collecting -= 1
            if not _active and not _collecting:
                _hash_results.clear()


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


def run_hash_budget(run_id: str) -> list[int]:
    """What ``run_id``'s ONE I/O budget has left, for hashing something else
    of the run (`Run.log_dataset`, data-catalog R8). While this process
    records the run's reads, a copy of what the recorder has left: charge the
    spend back with :func:`charge_run_hash`. Otherwise the budget output
    capture's references share (:func:`reference_budget`), spent in place."""
    with _lock:
        state = _active.get(run_id)
        if state is not None:
            return [max(RUN_HASH_BUDGET_BYTES - int(getattr(state, "hashed_bytes", 0)), 0)]
    return reference_budget(run_id)


def charge_run_hash(run_id: str, spent: int) -> None:
    """Count ``spent`` bytes (hashed from :func:`run_hash_budget`) against the
    run's recorder, so its reads and its datasets share one 10 GB."""
    if spent <= 0:
        return
    with _lock:
        state = _active.get(run_id)
        if state is not None:
            state.hashed_bytes += spent


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
from probe.sdk.capture.lineage.child_site import WRITES_ENV, _is_probe_site, _write_site  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.exclusions import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _CACHE_ENVS,
    _CODE_SUFFIXES,
    _CREDENTIAL_PARTS,
    _SYSTEM_ALLOWED,
    _SYSTEM_PREFIXES,
    _TOOL_CACHE_PARTS,
    _WRITE_ONLY_PARTS,
    _as_prefix,
    _ignored,
    _interpreter_prefixes,
    _sendable,
    _write_skip,
)
from probe.sdk.capture.lineage.finishing import LATE_TAG, _consumed, _journal_rows, _late_files  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.identities import FULL_HASH_MAX_BYTES, RUN_HASH_BUDGET_BYTES, _HashCache, hash_file  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.recovery import recover_orphans  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.rows import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _iso_from_ns,
    _read_observation,
    _typed_output_row,
    _typed_row,
    _valid_instant,
)
from probe.sdk.capture.lineage.spool.reader import _SpooledWrites, _header, _read_spools, _spools  # noqa: E402 -- pieces need each other; the front door loads this one first
