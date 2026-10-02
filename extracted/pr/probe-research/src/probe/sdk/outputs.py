"""What a run produced, captured when it ends (daemon-v2 plan, D17).

A run's output files used to reach Probe only if the script called
``log_artifact``, and nothing it printed was kept. The SDK runs INSIDE the run,
so it knows when the run started and ended and which folder it worked in -- on
any machine, including a Modal/Ray/Slurm job nothing else can see. It captures:

* **Outputs.** At run open the watched folder is listed (path, size, mtime --
  no hashing). At the end every file created or changed since is captured as
  ``outputs/<its path in the folder>``.
* **The log.** Everything the run printed, as ``probe/run.log`` (see
  :mod:`probe.sdk.logcapture`). While the run is alive the same output is also
  streamed to the server, complete lines every 15 s, for the run page's Logs
  panel (:mod:`probe.sdk.logstream`); the artifact stays the durable copy.

WHY THE PREFIXES. The server keeps a run artifact's history by NAME: an upload
whose name matches an existing artifact becomes its next VERSION. The code
snapshot taken at run open already names every file of a non-git folder (and
every untracked file of a repo) by its bare path, so a captured ``train.log``
landed as version 2 of the snapshot's ``train.log`` -- still labelled code,
invisible as an output, and the snapshot's row no longer showing what the
folder held at open (found in the prod smoke, 2026-09-26). ``outputs/`` keeps
the run's products apart from its inputs, and ``probe/`` keeps Probe's own files
apart from a user's ``run.log``.

"The end" is ``finish()``, a crash (atexit runs after an uncaught exception) and
interpreter exit. A death that runs no Python -- a segfault, the OOM killer, a
SIGTERM or any other signal -- is caught by the log helper, which outlives the
run and starts ``python -m probe.sdk.outputs --recover``. No signal handler is
installed: how the program dies, and what its parent sees, stays its own.

WHAT HAPPENS TO EACH FILE -- the storage decides (:mod:`probe.sdk.ephemeral`):

=============================  =================================  =================
file                           where it sits                      captured as
=============================  =================================  =================
up to 64 MB                    anywhere                           upload (redacted)
over 64 MB, or past the close  storage that lasts (a network      pointer: path,
budget, or not inspectable     drive, a Modal Volume, a laptop)   size, no bytes
the same                       a throwaway box's own disk         listed in the
                                                                  manifest
=============================  =================================  =================

A pointer to storage that lasts is a real record: the bytes are still there
tomorrow. A pointer to a container's own disk names bytes that are already
gone, so there the file would have to be uploaded -- and 64 MB is the most an
upload carries: the client gate inspects in memory up to it, and the server's
upload guard (`app/artifacts/upload_guard.py`) refuses anything bigger. Such a
file is listed, with a warning, so its absence is visible.

THE CLOSE IS BOUNDED. Inspection runs ~1 MB/s on JSON text, so a close is given
:func:`close_budget` seconds (``PROBE_CAPTURE_BUDGET_SEC``, capped by the
finish timeout when one is set). The log is queued first; once the budget is
spent the remaining files are pointed to or listed, never inspected.

THE SAFETY STOPS:

* Skipped directories: VCS, virtualenvs, ``node_modules``, ``__pycache__``,
  tool caches, credential directories (``snapshot.SKIP_DIRS``) plus ``.cache``
  and ``.probe``, the outbox journal, Probe's own state directory, every other
  folder the SDK keeps files in (``probe.sdk.owndirs``: another outbox, the
  ``$TMPDIR`` stand-ins) and pseudo-filesystems (``/proc`` ...). In the home
  directory every top-level dot-entry (``.kube``, ``.docker``, ``.config`` ...)
  is tool state, not output.
* Credential-shaped NAMES (``.env``, ``*.pem``, ``*credentials*``, ``.pgpass``)
  are never read. CONTENT goes through the gate: a text credential is redacted
  and the file uploaded, as ``log_artifact`` does; a credential the gate could
  not redact (inside a zip, a checkpoint, non-UTF-8 bytes) skips the file with
  one warning naming it. A ``field-name`` hit (``cookie =``) never skips. The
  bytes uploaded are exactly the bytes inspected.
* A folder too big to list at open (:data:`MAX_BASELINE_ENTRIES` files or
  :data:`OPEN_WALK_SECONDS`) is a workspace, not a run folder, and so is ``/``:
  output files are not captured, naming ``outputs=``. The log still is.
* Two runs watching one folder AT THE SAME TIME cannot tell whose files are
  whose, so both skip the output sweep and say so (the log still uploads).
  Several processes of ONE run (ranks) each sweep -- a rank may write after
  another has closed -- and the run's ledger lets each skip, unread, what
  another already queued; each keeps its own log.

NO DOUBLE UPLOADS. A file the script already logged (same path, unchanged, or
same bytes) is skipped; so is one already queued with the same bytes. Uploads go
through the durable journal as NON-BLOCKING ops: ``finish()`` tries to deliver
them before the terminal status, but an outage cannot keep the run open. A
per-run ledger skips re-queuing what an earlier close queued.

WHAT A READER CAN MATCH (lineage plan 3). An upload the gate REDACTED stores
bytes no reader ever opened, so it carries ``meta.source_sha256``: the
original's sha256, taken from the SAME read as the redacted bytes
(``secret_gate.read_upload_redacted_sourced``), which is what a later run
reading the file hashes. Dedupe stays keyed on the STORED bytes: two originals
that redact to identical bytes (the same file rewritten with another token, a
second close) are ONE stored version, which keeps the FIRST original's hash;
the later original is not uploaded again -- the server would make no new
version of identical bytes anyway -- and its hash reaches the server through
the run's write list (``POST /v1/runs/{id}/outputs``, :mod:`probe.sdk.inputs`)
instead. A REFERENCE (a file too big to upload, or past the close budget)
carries ``content_hash`` -- the file's sha256, hashed from what the run's I/O
budget has left after its reads and writes (:func:`inputs.reference_budget`)
and within the close's deadline -- so a read of those bytes can match it; one
the budget or the time did not reach is recorded without.

ONE OWNER. ``probe exec`` captures for its child and says so:
``PROBE_CAPTURE_OWNER`` (this host) with ``PROBE_CAPTURE_ROOT`` (its folder) for
the files, ``PROBE_CAPTURE_LOG_OWNER`` (this host) when it tees the child's
output. A ``probe.init()`` in that child leaves each to exec, and captures files
only from a folder OUTSIDE exec's. On another machine (a forwarded Modal secret,
``sbatch --export``) it captures everything itself.

Opt out with ``capture_outputs=False`` / ``PROBE_CAPTURE_OUTPUTS=0`` (outputs
and log), or ``PROBE_CAPTURE_LOG=0`` for the log alone -- which also gives up
the helper, and with it capture after a hard death.
"""

from __future__ import annotations

import atexit
import contextlib
import hashlib
import json
import os
import re
import secrets
import socket
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

from .._shared import oscompat
from . import ephemeral, homedir
from . import ignore as _ignore
from . import logstream as _logstream
from . import owndirs as _owndirs
from . import safe_warn as _diagnostics
from . import secret_gate
from . import snapshot as _snapshot
from .filetype import artifact_kind_for
from .hashing import fingerprint, local_file_uri
from .logcapture import _spawn_recovery, live_dir, read_stats
from .secret_gate import FIELD_NAME_RULE, CredentialBlocked, _findings, prepare_upload

CAPTURE_ENV = "PROBE_CAPTURE_OUTPUTS"
LOG_ENV = "PROBE_CAPTURE_LOG"
BUDGET_ENV = "PROBE_CAPTURE_BUDGET_SEC"
OWNER_ENV = "PROBE_CAPTURE_OWNER"
ROOT_ENV = "PROBE_CAPTURE_ROOT"
LOG_OWNER_ENV = "PROBE_CAPTURE_LOG_OWNER"

#: Every captured output is named under this prefix (see WHY THE PREFIXES).
OUTPUT_PREFIX = "outputs/"
LOG_NAME = "probe/run.log"
MANIFEST_NAME = "probe/outputs-manifest.json"
#: ``meta.capture`` on every row this module writes. Never "code-snapshot":
#: the server reserves that value for the batch code-capture door.
CAPTURE_OUTPUTS = "outputs"
CAPTURE_LOG = "log"

#: The most an upload carries: the gate's in-memory inspection limit, which
#: the server's upload guard enforces too.
INSPECT_LIMIT_BYTES = secret_gate.ScanPolicy().max_bytes
#: Seconds a close may spend inspecting files, unless ``PROBE_CAPTURE_BUDGET_SEC``
#: or the finish timeout says otherwise.
CLOSE_BUDGET_SECONDS = 120.0
#: How long the listing at run open may take before the folder counts as a
#: workspace (a network drive answers every lstat over the wire).
OPEN_WALK_SECONDS = 10.0
MAX_BASELINE_ENTRIES = 50_000
MAX_FINAL_ENTRIES = 200_000
SKIP_DIRS = _snapshot.SKIP_DIRS | {".cache", ".probe"}
#: Credential files the code snapshot has no reason to know about, because
#: they live in a home directory rather than a repo.
OUTPUT_SECRET_NAMES = frozenset({
    ".pgpass", ".git-credentials", ".envrc", "kaggle.json", ".dockercfg", ".boto", ".s3cfg",
    ".htpasswd",
})
#: Local logs, ledgers and capture records older than this are pruned.
RETAIN_SECONDS = 30 * 86_400
#: A recovery claim older than this belongs to a recoverer that died.
CLAIM_STALE_SECONDS = 600
_CODE_KINDS = frozenset({"code", "code_snapshot", "code-snapshot", "code-bytes", "code_bytes"})
_OFF = frozenset({"0", "false", "no", "off"})
#: Why a file was not uploaded. The code is what callers branch on; the text is
#: what a person reads.
TOO_LARGE, OVER_BUDGET, UNINSPECTABLE = "too_large", "over_budget", "uninspectable"
_REASONS = {
    TOO_LARGE: f"over the {INSPECT_LIMIT_BYTES // (1024 * 1024)} MB upload limit",
    OVER_BUDGET: "capture's time budget at close was spent",
    UNINSPECTABLE: "could not be inspected",
}
#: A run of base64-looking characters: where an encoded credential hides.
_ENCODED_RUN = re.compile(r"[A-Za-z0-9+/_-]{24,}={0,2}")


# -- switches -----------------------------------------------------------------------
def enabled(capture_outputs: bool | None) -> bool:
    """The caller's argument wins; otherwise ``PROBE_CAPTURE_OUTPUTS`` (on)."""
    if capture_outputs is not None:
        return bool(capture_outputs)
    return (os.environ.get(CAPTURE_ENV) or "").strip().lower() not in _OFF


def log_enabled() -> bool:
    return (os.environ.get(LOG_ENV) or "").strip().lower() not in _OFF


def _env_seconds(name: str) -> float | None:
    raw = (os.environ.get(name) or "").strip()
    try:
        return max(0.0, float(raw)) if raw else None
    except ValueError:
        return None


def close_budget() -> float:
    """Seconds a close may spend: ``PROBE_CAPTURE_BUDGET_SEC`` (120), and
    never more than ``PROBE_FINISH_TIMEOUT_SEC`` -- a cluster that set that
    to keep a close from holding its GPUs meant capture too."""
    budget = _env_seconds(BUDGET_ENV)
    budget = CLOSE_BUDGET_SECONDS if budget is None else budget
    finish = _env_seconds("PROBE_FINISH_TIMEOUT_SEC")
    return budget if finish is None else min(budget, finish)


def in_process_log_supported() -> bool:
    """Swapping fds 1/2 is wrong in a notebook: ipykernel captures file
    descriptors itself, and the notebook's output is not fd 1 at all."""
    return os.name == "posix" and bool(sys.executable) and "ipykernel" not in sys.modules


def _this_host(env: str) -> bool:
    owner = (os.environ.get(env) or "").strip()
    return bool(owner) and owner == socket.gethostname()


def log_owned_here() -> bool:
    """A launcher on this host tees this process's output already."""
    return _this_host(LOG_OWNER_ENV)


def outputs_owned_here(root: str) -> bool:
    """A launcher on this host already sweeps a folder containing `root`."""
    if not _this_host(OWNER_ENV):
        return False
    launcher_root = (os.environ.get(ROOT_ENV) or "").strip()
    if not launcher_root:
        return True  # an older launcher that did not say: assume it covers us
    return _within(os.path.realpath(root), os.path.realpath(launcher_root))


def target_root(*, outputs: str | os.PathLike | None = None, cwd: str | None = None) -> str:
    """The folder a capture with these arguments watches."""
    base = os.path.abspath(cwd or os.getcwd())
    return os.path.realpath(os.path.join(base, os.fspath(outputs)) if outputs else base)


def _within(path: str, root: str) -> bool:
    return path == root or path.startswith(root.rstrip("/") + "/")


def _overlap(a: str, b: str) -> bool:
    if not a or not b:
        return False  # a record with no root watches nothing
    return _within(a, b) or _within(b, a)


# -- local state ----------------------------------------------------------------------
def state_dir() -> Path:
    """``<state>/probe``, where the log, the capture registry and baselines
    live; under a private ``$TMPDIR`` folder when the state folder cannot be
    written (``HOME=/`` for an arbitrary uid: `homedir.state_base`). It used to
    be `session_marker.state_dir`, and output capture did not start there."""
    return homedir.state_base() / "probe"


def _private_dir(*parts: str) -> Path:
    path = state_dir().joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


def _prune(directory: Path) -> None:
    cutoff = time.time() - RETAIN_SECONDS
    try:
        for entry in os.scandir(directory):
            try:
                if entry.is_file(follow_symlinks=False) and entry.stat().st_mtime < cutoff:
                    os.unlink(entry.path)
            except OSError:
                pass
    except OSError:
        pass


def reserve_log_path(run_id: str) -> str:
    """A fresh file under ``<state>/probe/logs``: ``<run-id>.log``, then
    ``<run-id>.2.log`` ... when a resumed attempt of the same run logs again.

    A name whose live-log spool (``<log>.live/``) still exists is taken even
    when its log is gone: a process killed after its log was queued (and the
    local copy discarded) but before its stream stopped leaves the spool, with
    that attempt's cursor and unsent tail, for its recovery to send. Reusing
    the name would ship the dead attempt's tail as this one's output and start
    this one past its own first bytes."""
    directory = _private_dir("logs")
    _prune(directory)
    _prune_spools(directory)
    for n in range(1, 1000):
        path = directory / (f"{run_id}.log" if n == 1 else f"{run_id}.{n}.log")
        if os.path.lexists(live_dir(str(path))):
            continue
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            continue
        os.close(fd)
        return str(path)
    raise OSError("no free log file name")


def _prune_spools(directory: Path) -> None:
    """Live-log spools (`<log>.live/`) nothing removed: a process and its
    recovery both died. Same retention as the logs beside them."""
    import shutil

    cutoff = time.time() - RETAIN_SECONDS
    try:
        for entry in os.scandir(directory):
            try:
                if (
                    entry.name.endswith(".live")
                    and entry.is_dir(follow_symlinks=False)
                    and entry.stat(follow_symlinks=False).st_mtime < cutoff
                ):
                    shutil.rmtree(entry.path, ignore_errors=True)
            except OSError:
                pass
    except OSError:
        pass


def _discard_local_log(log_path: str) -> None:
    """The log is staged in the outbox: the local copy has done its job."""
    # Not `.stopped`: a helper still forwarding for a straggler reads it at EOF
    # to tell a stop from a crash. It is empty, and pruned with the logs.
    for path in (log_path, log_path + ".meta.json", log_path + ".ready"):
        try:
            os.unlink(path)
        except OSError:
            pass


def _write_json(path: Path, data: Any) -> None:
    from .durable import write_text_atomic

    write_text_atomic(path, json.dumps(data), mode=0o600)


# -- liveness ------------------------------------------------------------------------------
def _process_started(pid: int) -> float | None:
    """When ``pid`` started, or None. A pid alone is reused; pid + start is not."""
    try:
        import psutil

        return psutil.Process(pid).create_time()
    except Exception:  # noqa: BLE001
        return None


def _alive(pid: Any, started: Any = None) -> bool:
    """Whether a recorded process is still running. Total over any input: the
    registry is a folder of files anything can damage, and one bad file must
    not break capture for every later run."""
    try:
        pid = int(pid or 0)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    try:
        import psutil
    except ImportError:
        # The Windows-safe probe: os.kill(pid, 0) TERMINATES a process there.
        from .diagnostics import _pid_alive

        return _pid_alive(pid)
    try:
        process = psutil.Process(pid)
        if process.status() == psutil.STATUS_ZOMBIE:
            return False  # exited, just not reaped yet
        now = process.create_time()
    except psutil.NoSuchProcess:
        return False
    except Exception:  # noqa: BLE001 -- access denied and the like: assume alive
        return True
    if isinstance(started, (int, float)) and abs(now - started) > 1.0:
        return False  # the pid was reused
    return True


def _record_alive(record: dict) -> bool:
    return _alive(record.get("pid"), record.get("proc_start"))


def _helper_alive(record: dict) -> bool:
    return _alive(record.get("helper_pid"), record.get("helper_start"))


# -- listing ---------------------------------------------------------------------------
#: `(rules root, capture root)` pairs already warned about (once per process).
_UNREACHABLE_WARNED: set[tuple[str, str]] = set()


def _warn_unreachable_patterns(ignore: Any, root: str) -> None:
    """Say once when an ``outputs=`` folder lies outside the ``.probeignore``
    root and some of the file's patterns are anchored there (`/data`,
    `runs/*/dump`): they cannot apply to this folder. The unanchored ones and
    ``ignore=`` / ``PROBE_IGNORE`` still do, relative to the folder."""
    try:
        if ignore is None or (ignore.root, root) in _UNREACHABLE_WARNED:
            return
        lost = ignore.unreachable(root)
        if not lost:
            return
        _UNREACHABLE_WARNED.add((ignore.root, root))
        _diagnostics.warn(
            f"probe: output capture's folder {root} is outside {ignore.root}, so "
            f"{len(lost)} anchored .probeignore pattern(s) cannot apply to it: "
            f"{', '.join(repr(p) for p in lost[:5])}. Unanchored patterns (`*.jsonl`, "
            "`ckpt/`) and ignore= / PROBE_IGNORE still apply, relative to that folder.",
            stacklevel=3,
        )
    except Exception:  # noqa: BLE001 -- a warning may never cost the capture
        pass


def _walk(
    root: str,
    excluded: set[str],
    limit: int,
    *,
    deadline: float | None = None,
    skip_hidden_top: bool = False,
    ignore: Any = None,
    counts: dict[str, int] | None = None,
) -> tuple[dict[str, tuple[int, int]], bool]:
    """``({relative posix path: (size, mtime_ns)}, cut_short)`` for the regular
    files under ``root``, stopping at ``limit`` files or ``deadline``. Symlinks
    are not followed or listed: a link's target can live anywhere, and the run
    did not write it. Pseudo-filesystems are never entered.

    ``ignore`` is the run's ``.probeignore`` rules: an excluded directory is not
    entered and an excluded file is not listed, so neither counts toward
    ``limit``. Each is counted in ``counts["probeignore"]`` when given."""
    pseudo = ephemeral.pseudo_mountpoints()
    # The SDK's own folders below the root, wherever they are (`owndirs`):
    # `excluded` names this run's queue and state, not a $TMPDIR fallback's.
    own = _owndirs.current().within(os.path.realpath(root))
    found: dict[str, tuple[int, int]] = {}
    cut = len(root.rstrip(os.sep)) + 1
    stack = [root]
    while stack:
        directory = stack.pop()
        try:
            listing = os.scandir(directory)
        except OSError:
            continue
        with listing:
            for entry in listing:
                if skip_hidden_top and directory == root and entry.name.startswith("."):
                    continue
                try:
                    if own is not None and own.top(entry.path[cut:].replace(os.sep, "/")) is not None:
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        if entry.name not in SKIP_DIRS and entry.path not in excluded and entry.path not in pseudo:
                            if ignore is not None and ignore.ignored(entry.path, is_dir=True, capture_root=root):
                                if counts is not None:
                                    counts["probeignore"] = counts.get("probeignore", 0) + 1
                                continue
                            stack.append(entry.path)
                        continue
                    if not entry.is_file(follow_symlinks=False):
                        continue
                    if ignore is not None and ignore.ignored(entry.path, capture_root=root):
                        if counts is not None:
                            counts["probeignore"] = counts.get("probeignore", 0) + 1
                        continue
                    info = entry.stat(follow_symlinks=False)
                except OSError:
                    continue
                if len(found) >= limit:
                    return found, True
                found[entry.path[cut:].replace(os.sep, "/")] = (info.st_size, info.st_mtime_ns)
        if deadline is not None and time.monotonic() > deadline:
            return found, True
    return found, False


def _shallow_first_key(rel: str) -> tuple[int, str]:
    # Top-level files first: `metrics.json` beside the script is a headline
    # result far more often than `samples/00042.png` is -- and under the close
    # budget, what sorts last is what gets pointed to instead of uploaded.
    return rel.count("/"), rel


def _skip_reason(name: str) -> str | None:
    reason = _snapshot._skip_reason(name)
    if reason is None and (name in OUTPUT_SECRET_NAMES or name.lower().endswith(".env")):
        return "secret"
    return reason


def _unredacted(result: secret_gate.InspectionResult) -> bool:
    """A finding the gate could not replace (``field-name`` never counts)."""
    return any(rule != FIELD_NAME_RULE for rule in result.flagged)


def redact_log_text(text: str) -> tuple[bytes | None, secret_gate.InspectionResult]:
    """``(bytes to upload, what the gate did)`` for text a run printed, or
    ``(None, ...)`` when it holds a credential the gate could not redact.

    THE one decision for a run's printed output: the final ``probe/run.log``
    (`OutputCapture._queue_log`) and the live stream (`logstream`) both call
    it. Replace what can be replaced; an encoded credential the gate sees
    inside but cannot replace (base64 of gzip) blanks every encoded-looking
    run and is looked for again."""
    data, result = secret_gate.redact_text(text)
    if not _unredacted(result):
        return data, result
    data, second = secret_gate.redact_text(_ENCODED_RUN.sub("<redacted:encoded>", data.decode("utf-8")))
    if _unredacted(second):
        return None, second
    return data, secret_gate.InspectionResult(
        warnings=second.warnings, rewritten=tuple(result.rewritten) + ("encoded",), flagged=second.flagged
    )


# -- process-wide hooks -------------------------------------------------------------------
_live: set["OutputCapture"] = set()
_live_lock = threading.Lock()
_atexit_installed = False
_shared_warned: set[str] = set()


def _reset_after_fork() -> None:
    # A thread may have held the lock at the fork; the child's copy would stay
    # locked forever, with no thread left to release it.
    global _live_lock
    _live_lock = threading.Lock()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_after_fork)


def _finalize_at_exit() -> None:
    """Captures still open at interpreter exit: a run nobody finished. Sweep it
    and wake the detached drainer, since nothing in this process will."""
    with _live_lock:
        pending = list(_live)
    for capture in pending:
        try:
            if capture.finalize() is not None and capture.client is not None:
                capture.client._kick_drainer(force=True)
        except BaseException:  # noqa: BLE001 -- interpreter teardown
            pass


# -- the registry: who is watching which folder on this host ---------------------------
def _registry() -> Path:
    # Per host: on an HPC cluster HOME (and with it this directory) is shared
    # by every node, and only this host's records mean anything here.
    host = "".join(c if c.isalnum() or c in "-._" else "_" for c in socket.gethostname()) or "host"
    return _private_dir("capture", "active", host)


def _entries() -> list[tuple[Path, dict]]:
    found = []
    for path in _registry().glob("*.json"):
        try:
            record = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        if isinstance(record, dict):
            found.append((path, record))
    return found


#: The key of a window's registry record holding rules OTHER processes of the
#: run handed it (`share_ignore`), and how many it keeps.
SHARED_IGNORE_KEY = "ignore_shared"
MAX_SHARED_IGNORE = 16


def share_ignore(run_id: str, rules: Any) -> int:
    """Hand ``rules`` -- this process's ``.probeignore`` rules, with its own
    ``ignore=`` patterns -- to the windows of the SAME run that other
    processes on this host sweep (plan (n), #2045 review): a ``probe exec``
    launcher sweeps its child's folder after the child exits, with the rules
    it loaded before the child started. The registry record is the channel
    those windows already share (``shared_with`` travels the same way), and
    :meth:`OutputCapture._sweep` re-reads it. Returns how many windows took
    them; never raises."""
    try:
        record = _ignore.to_record(rules)
        if record is None:
            return 0
        from .durable import file_lock

        registry = _registry()
        taken = 0
        with file_lock(registry / ".lock"):
            for path, other in _entries():
                if other.get("run_id") != run_id or other.get("pid") == os.getpid():
                    continue
                if other.get("sweeps") is False or not _record_alive(other):
                    continue
                shared = other.setdefault(SHARED_IGNORE_KEY, [])
                if not isinstance(shared, list):
                    continue
                if record not in shared and len(shared) < MAX_SHARED_IGNORE:
                    shared.append(record)
                    _write_json(path, other)
                taken += 1
        return taken
    except Exception:  # noqa: BLE001 -- filtering is never a reason to fail init
        return 0


def _distributed_log_name() -> str | None:
    """``probe/run.rank<N>.log`` for one process of a distributed job, else
    None. From the environment, not from the registry: the registry is per
    host, and the first rank on every host would otherwise keep the plain
    name -- one artifact, overwritten version by version."""
    world = next((v for v in (os.environ.get(n) for n in ("WORLD_SIZE", "SLURM_NTASKS")) if v), "")
    if not (world.strip().isdigit() and int(world) > 1):
        return None
    for name in ("RANK", "SLURM_PROCID"):
        value = (os.environ.get(name) or "").strip()
        if value.isdigit():
            return f"probe/run.rank{value}.log"
    return None


@contextlib.contextmanager
def _ledger_lock(run_id: str, deadline: float):
    """One sweep of a run at a time on this host, so a rank closing beside
    another sees what that one queued instead of queuing it again. Waiting
    ends at the caller's deadline: dedupe is worth time, not the close."""
    try:
        handle = open(_private_dir("outputs") / f"{run_id}.lock", "a+")
    except OSError:
        yield
        return
    with handle:
        held = False
        while True:
            try:
                oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
                held = True
                break
            except OSError:
                if time.monotonic() >= deadline:
                    break
                time.sleep(0.05)
        try:
            yield
        finally:
            if held:
                oscompat.flock(handle.fileno(), oscompat.LOCK_UN)


class OutputCapture:
    """One run's capture window. Holds the client (or, in a recovery, just the
    journal) and the run id -- never the Run handle, so an abandoned handle
    stays collectable and its heartbeat stops."""

    def __init__(
        self,
        client: Any,
        run_id: str,
        root: str,
        *,
        tee: bool,
        launcher: bool,
        journal: Any = None,
        recovery: bool = False,
        ignore: Any = None,
        epoch: Any = None,
        writer: dict | None = None,
    ):
        self.client = client
        #: The run's write epoch, read at each live-log POST (`logstream`);
        #: None: the `probe.init()` run's, if this process has one.
        self._epoch = epoch
        #: Who writes this run from this process (2.2): ``session_id``,
        #: ``write_epoch``, ``role`` and ``sole_writer``. Recorded so the log
        #: helper, which outlives the process, can report its death.
        self.writer = dict(writer or {})
        self.journal = journal if journal is not None else client.journal
        self.run_id = run_id
        self.root = root
        #: The run's `.probeignore` rules (`probe.sdk.ignore.IgnoreRules`), or None.
        self.ignore = ignore
        self.launcher = launcher
        self.recovery = recovery
        self.pid = os.getpid()
        self.host = socket.gethostname()
        self.started_at = time.time()
        self.baseline: dict[str, tuple[int, int]] = {}
        #: False when this window keeps the log only: a folder too big to
        #: list, ``/``, or one a launcher on this host already sweeps.
        self.sweeps = True
        self.log_name = _distributed_log_name() or LOG_NAME
        self.enqueued = 0
        self._logged: dict[str, dict] = {}
        self._tee = None
        self._log_path: str | None = None
        self._helper_pid: int | None = None
        #: The live stream of the log (plan item (h)): asked for, and running.
        self._live = False
        self._streamer: _logstream.LogStreamer | None = None
        self._log_done = False
        self._sweep_done = False
        self._lock = threading.Lock()
        #: One window's name in the registry. Unique per window, not per
        #: process: a Client.run window and an execute() window of the same
        #: run live in one process.
        self._key = f"{run_id}.{self.pid}.{secrets.token_hex(4)}"
        self._entry: Path | None = None
        self._baseline_file: Path | None = None
        self._excluded = self._excluded_dirs()
        self._is_home = root == os.path.realpath(os.path.expanduser("~"))
        self._want_tee = tee

    # -- open -----------------------------------------------------------------------
    @classmethod
    def start(
        cls,
        client: Any,
        run_id: str,
        *,
        outputs: str | os.PathLike | None = None,
        cwd: str | None = None,
        tee: bool = True,
        launcher: bool = False,
        sweep: bool = True,
        ignore: Any = None,
        epoch: Any = None,
        writer: dict | None = None,
    ) -> "OutputCapture | None":
        """Open the window, or return None (never raise): capture is never a
        reason for a run not to start. ``sweep=False`` keeps the log only.
        ``ignore`` (the run's ``.probeignore`` rules) keeps matching files out
        of the baseline and the sweep. ``epoch``: reads the run's write epoch
        (`logstream.handle_epoch`), so the live log names the attempt it
        belongs to."""
        capture = None
        try:
            _recover_stale_logs()
            root = target_root(outputs=outputs, cwd=cwd)
            if os.path.exists(root) and not os.path.isdir(root):
                _diagnostics.warn(
                    f"probe: outputs={os.fspath(outputs)!r} is a file, not a folder; "
                    "output capture is off for this run. Name the folder the run writes to."
                )
                return None
            capture = cls(
                client,
                run_id,
                root,
                tee=tee,
                launcher=launcher,
                ignore=ignore,
                epoch=epoch,
                writer=writer,
            )
            _warn_unreachable_patterns(ignore, root)
            capture.sweeps = sweep
            if sweep:
                capture._open_baseline()
            capture._start_log()
            capture._register()
            # After `_register`: it can rename the log (a second process of
            # the run on this host), and the stream is named after the log.
            capture._start_stream()
            with _live_lock:
                _live.add(capture)
                global _atexit_installed
                if not _atexit_installed:
                    atexit.register(_finalize_at_exit)
                    _atexit_installed = True
            return capture
        except Exception as exc:  # noqa: BLE001 -- fail-open by contract
            if capture is not None and capture._tee is not None:
                # The tee started but the window did not: nothing would ever
                # stop it or send its log.
                try:
                    capture._tee.stop()
                except Exception:  # noqa: BLE001
                    pass
                capture._tee = None
            _diagnostics.warn(f"probe: output capture could not start ({type(exc).__name__}): {exc}")
            return None

    def _excluded_dirs(self) -> set[str]:
        excluded = set()
        for path in (getattr(self.journal, "dir", None), state_dir()):
            if path is not None:
                try:
                    excluded.add(os.path.realpath(path))
                except OSError:
                    pass
        return excluded

    def _open_baseline(self) -> None:
        if os.path.dirname(self.root) == self.root:
            self.sweeps = False
            _diagnostics.warn(
                f"probe: output files are not captured for this run: it works in {self.root}, "
                "the root of the filesystem. Pass outputs='<the folder this run writes to>' "
                "(probe exec --outputs) to capture them. Its log is still saved."
            )
            return
        if not os.path.isdir(self.root):
            return
        baseline, cut = _walk(
            self.root,
            self._excluded,
            MAX_BASELINE_ENTRIES,
            deadline=time.monotonic() + OPEN_WALK_SECONDS,
            skip_hidden_top=self._is_home,
            ignore=self.ignore,
        )
        if cut:
            self.sweeps = False
            _diagnostics.warn(
                f"probe: output files are not captured for this run: {self.root} is too big to "
                f"list at open (over {MAX_BASELINE_ENTRIES:,} files or {OPEN_WALK_SECONDS:.0f}s), "
                "which is a workspace rather than a run folder. Pass outputs='<the folder this "
                "run writes to>' (probe exec --outputs) to capture them. Its log is still saved."
            )
            return
        self.baseline = baseline

    def _start_log(self) -> None:
        if not (self._want_tee and log_enabled() and in_process_log_supported()):
            return
        if log_owned_here():
            return  # the launcher on this host tees this process already
        with _live_lock:
            if any(c._tee is not None for c in _live):
                return  # fds 1/2 are one per process: the first open run owns them
        try:
            from .logcapture import InProcessTee

            self._log_path = reserve_log_path(self.run_id)
            self._entry = _registry() / f"{self._key}.json"
            # Before the helper starts: the spool directory is what asks it
            # to stream (logcapture LIVE).
            self._live = _logstream.prepare(self.client, self._log_path)
            tee = InProcessTee(
                self._log_path,
                recovery_entry=str(self._entry),
                # 2.2: the helper reports this process's death the moment it
                # is reparented, rather than at EOF (which a grandchild still
                # holding stdout can postpone forever).
                watch_parent=bool(self.writer.get("session_id")),
            )
            tee.start()
            self._tee = tee
            self._helper_pid = tee.helper_pid
        except Exception as exc:  # noqa: BLE001
            self._tee = None
            self._drop_live()
            _diagnostics.warn(
                f"probe: this run's output will not be saved as {LOG_NAME} "
                f"({type(exc).__name__}): {exc}"
            )

    def _register(self) -> None:
        """Record this window on the host: overlap detection, and what a
        recovery needs if the process dies without closing it."""
        from .durable import file_lock

        registry = _registry()
        _prune(registry)
        self._entry = self._entry or registry / f"{self._key}.json"
        shared: list[str] = []
        with file_lock(registry / ".lock"):
            for path, other in _entries():
                if path == self._entry or not _record_alive(other):
                    continue
                if not _overlap(self.root, str(other.get("root") or "")):
                    continue
                if other.get("run_id") == self.run_id:
                    # Another process of THIS run (a rank): both sweep -- this
                    # one may write after that one closes -- and the ledger
                    # keeps them from queuing a file twice. The log is per
                    # process, so it needs a name of its own.
                    if self.log_name == LOG_NAME:
                        self.log_name = f"probe/run.{self.pid}.log"
                    continue
                if not self.sweeps or other.get("sweeps") is False:
                    continue  # a log-only window claims no files
                shared.append(str(other.get("run_id")))
                mates = other.setdefault("shared_with", [])
                if isinstance(mates, list) and self.run_id not in mates:
                    mates.append(self.run_id)
                    _write_json(path, other)
            if self.sweeps:
                baselines = _private_dir("capture", "baselines")
                _prune(baselines)
                self._baseline_file = baselines / f"{self._key}.json"
                _write_json(self._baseline_file, self.baseline)
            _write_json(self._entry, self._record(shared_with=shared))

    def _record(self, *, shared_with: list[str]) -> dict:
        context = getattr(self.journal, "context", None) or {}
        return {
            "run_id": self.run_id,
            "pid": self.pid,
            "proc_start": _process_started(self.pid),
            "host": self.host,
            "root": self.root,
            "started_at": self.started_at,
            "launcher": self.launcher,
            "sweeps": self.sweeps,
            "baseline": str(self._baseline_file) if self._baseline_file else None,
            "log_path": self._log_path,
            "log_name": self.log_name,
            "helper_pid": self._helper_pid,
            "helper_start": _process_started(self._helper_pid) if self._helper_pid else None,
            "journal_dir": str(getattr(self.journal, "dir", "") or ""),
            "context": {
                "name": context.get("name"),
                "base_url": context.get("base_url"),
                # Which credential the run wrote with (#2035), so the log a
                # recovery queues is delivered as the run, not as the machine.
                **({"principal": context["principal"]} if context.get("principal") else {}),
            },
            "shared_with": shared_with,
            # A recovery in a fresh interpreter excludes what this run did.
            "ignore": _ignore.to_record(self.ignore),
            "writer": self.writer or None,
        }

    def _rewrite_record(self, **fields: Any) -> None:
        if self._entry is None:
            return
        try:
            from .durable import file_lock

            # Under the registry's lock: another process may be adding to
            # this record (`shared_with`, `share_ignore`) at the same moment.
            with file_lock(self._entry.parent / ".lock"):
                record = json.loads(self._entry.read_text())
                record.update(fields)
                _write_json(self._entry, record)
        except (OSError, ValueError, AttributeError, ImportError):
            pass

    def _sweep_ignore(self) -> Any:
        """This window's rules plus those other processes of the run handed
        it in its record (`share_ignore`): a ``probe exec`` child's own
        ``ignore=``. Re-read at the sweep, as ``shared_with`` is; a recovery
        reads the same record."""
        extra = []
        if self._entry is not None:
            try:
                shared = json.loads(self._entry.read_text()).get(SHARED_IGNORE_KEY) or []
                if isinstance(shared, list):
                    extra = [_ignore.from_record(r) for r in shared[:MAX_SHARED_IGNORE]]
            except (OSError, ValueError, AttributeError):
                pass
        return _ignore.combine(self.ignore, *extra)

    def adopt_log(self, log_path: str) -> None:
        """A launcher tees its child into ``log_path``: record it, so a
        recovery can find the log if the launcher dies first. Called before
        the tee starts, so the live stream is asked for here too."""
        self._log_path = log_path
        self._rewrite_record(log_path=log_path)
        if self._streamer is None:
            self._live = _logstream.prepare(self.client, log_path)
            self._start_stream()

    def _start_stream(self) -> None:
        """Start shipping the live log, when it was asked for and a tee
        writes it. Never raises."""
        if not self._live or self._streamer is not None:
            return
        if self._log_path is None or self.client is None:
            self._drop_live()
            return
        try:
            epoch = self._epoch or _logstream.active_epoch(self.run_id)
            stream = _logstream.stream_for(self.log_name)
            self._streamer = _logstream.LogStreamer(
                self.client, self.run_id, self._log_path, stream, epoch=epoch
            ).start()
            # What a recovery needs to send the rest as THIS attempt's.
            self._rewrite_record(log_stream=stream, write_epoch=epoch())
        except Exception:  # noqa: BLE001 -- the live view is best effort
            self._streamer = None
            self._drop_live()

    def _stop_stream(self, deadline: float) -> None:
        """The last lines, within a small slice of what is left of the close
        (`logstream.FINAL_FLUSH_SECONDS`, and at most `FINAL_FLUSH_SHARE` of
        it: the outputs sweep after this needs the rest); the spool is removed
        either way."""
        streamer, self._streamer = self._streamer, None
        if streamer is not None:
            left = max(0.0, deadline - time.monotonic())
            streamer.stop(budget=min(_logstream.FINAL_FLUSH_SECONDS, left * _logstream.FINAL_FLUSH_SHARE))
        self._drop_live()

    def _drop_live(self) -> None:
        if self._live and self._log_path:
            import shutil

            shutil.rmtree(live_dir(self._log_path), ignore_errors=True)
        self._live = False

    def note_helper(self, pid: int) -> None:
        self._helper_pid = pid
        self._rewrite_record(helper_pid=pid, helper_start=_process_started(pid))

    def _is_rival(self, path: Path, other: dict) -> bool:
        """Another run, alive, sweeping a folder that overlaps this one."""
        return (
            path != self._entry
            and other.get("run_id") != self.run_id
            and other.get("sweeps") is not False
            and _record_alive(other)
            and _overlap(self.root, str(other.get("root") or ""))
        )

    def _shared_with(self) -> list[str]:
        """Runs that watched an overlapping folder on this host while this one
        was open: marked at either run's start, or still alive now."""
        shared: set[str] = set()
        if self._entry is not None:
            try:
                mates = json.loads(self._entry.read_text()).get("shared_with") or []
                if isinstance(mates, list):
                    shared.update(str(m) for m in mates)
            except (OSError, ValueError, AttributeError):
                pass
        for path, other in _entries():
            if self._is_rival(path, other):
                shared.add(str(other.get("run_id")))
        return sorted(shared)

    # -- during ---------------------------------------------------------------------
    def note_logged(self, path: str, digest: str | None = None) -> None:
        """``log_artifact`` stored this file: the sweep skips it while it stays
        the same (same size and mtime, or same bytes)."""
        try:
            full = os.path.realpath(path)
            info = os.stat(full)
        except OSError:
            return
        self._logged[full] = {"stat": (info.st_size, info.st_mtime_ns), "sha256": digest}

    # -- close ----------------------------------------------------------------------
    def finalize(
        self,
        *,
        log_path: str | None = None,
        log_stats: dict | None = None,
        budget: float | None = None,
    ) -> dict | None:
        """Queue the log, then sweep and queue the outputs, within ``budget``
        seconds (default :func:`close_budget`). Idempotent per part (the log
        and the sweep each retry on a later call if they failed); never raises
        except KeyboardInterrupt. Returns a summary, or None when already done."""
        if os.getpid() != self.pid or not self._lock.acquire(blocking=False):
            return None  # a forked copy, or another thread is closing this window
        try:
            if self._log_done and self._sweep_done:
                return None
            return self._finalize(log_path, log_stats, budget)
        finally:
            self._lock.release()

    def _finalize(self, log_path: str | None, log_stats: dict | None, budget: float | None) -> dict:
        deadline = time.monotonic() + (close_budget() if budget is None else max(0.0, budget))
        with _live_lock:
            _live.discard(self)
        summary: dict[str, Any] = {}
        if self._tee is not None:
            try:
                log_stats = self._tee.stop()
            except Exception:  # noqa: BLE001
                log_stats = None
            log_path, self._tee = self._log_path, None
        elif log_path is None:
            log_path = self._log_path
        try:
            shared = self._shared_with()
        except Exception:  # noqa: BLE001 -- an unreadable registry: assume alone
            shared = []
        # The log first: it is what a crash or a preemption most needs, and it
        # must not wait behind a slow sweep.
        if not self._log_done:
            try:
                sent = self._queue_log(log_path, log_stats, shared) if log_path and log_enabled() else None
                if sent is not None:
                    summary["log"] = sent
                self._log_done = sent is not False
            except KeyboardInterrupt:
                raise
            except Exception as exc:  # noqa: BLE001
                _diagnostics.warn(
                    f"probe: {self.log_name} for run {self.run_id} was not queued "
                    f"({type(exc).__name__}): {exc}"
                )
        if self._streamer is not None or self._live:
            # The tee has stopped, so the helper has ended the stream: the
            # last lines go to the live view, then the spool is removed.
            self._stop_stream(deadline)
        if not self._sweep_done:
            try:
                if not self.sweeps:
                    pass
                elif shared:
                    summary["skipped_shared_folder"] = shared
                    _warn_shared(self.run_id, shared, self.root)
                else:
                    summary.update(self._sweep(deadline))
                self._sweep_done = True
            except KeyboardInterrupt:
                raise
            except Exception as exc:  # noqa: BLE001 -- capture never breaks a close
                _diagnostics.warn(
                    f"probe: output capture for run {self.run_id} stopped early "
                    f"({type(exc).__name__}): {exc}"
                )
        if self._log_done and self._sweep_done:
            self._unregister()
        return summary

    def _unregister(self) -> None:
        markers = (
            list(self._entry.parent.glob(f"{self._entry.name}.writer-*"))
            if self._entry is not None
            else []
        )
        for path in (self._entry, self._baseline_file, *markers):
            if path is not None:
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass

    def _known_elsewhere(self) -> tuple[dict[str, set], set[str]]:
        """({source path: queued digests}, sha256s already stored on the run).

        The queue catches a ``log_artifact`` this process journaled; the server
        listing catches one a CHILD process made (``probe exec`` sweeps after
        its child logged), or, in a recovery, one the dead process made. Only
        those pay for the listing: in-process, :meth:`note_logged` saw every
        call."""
        queued: dict[str, set] = {}
        try:
            from . import multipart

            # Plan (g): an artifact over 64 MiB being uploaded in parts waits
            # in its own queue.
            for _path, op in [*self.journal.pending(), *multipart.pending(self.journal)]:
                upload = op.get("upload") or {}
                if op.get("run_ref") == self.run_id and upload.get("src_path"):
                    queued.setdefault(os.path.realpath(upload["src_path"]), set()).add(upload.get("blob"))
        except Exception:  # noqa: BLE001
            pass
        stored: set[str] = set()
        if (self.launcher or self.recovery) and self.client is not None:
            try:
                for row in self.client.list_run_artifacts(self.run_id, scope="own") or []:
                    if row.get("content_hash") and row.get("kind") not in _CODE_KINDS:
                        stored.add(row["content_hash"])
            except Exception:  # noqa: BLE001 -- a listing failure only costs dedupe
                pass
        return queued, stored

    def _sweep(self, deadline: float) -> dict:
        summary = {"uploaded": 0, "referenced": 0, "unchanged_logged": 0, "skipped_secret": 0, "listed": 0}
        if not os.path.isdir(self.root):
            return summary
        ephemeral.refresh()  # a volume mounted since the last close
        counts: dict[str, int] = {}
        now, truncated = _walk(
            self.root,
            self._excluded,
            MAX_FINAL_ENTRIES,
            deadline=deadline,
            skip_hidden_top=self._is_home,
            ignore=self._sweep_ignore(),
            counts=counts,
        )
        if counts.get("probeignore"):
            summary["skipped_probeignore"] = counts["probeignore"]
        candidates = sorted(
            (rel for rel, stat in now.items() if self.baseline.get(rel) != stat),
            key=_shallow_first_key,
        )
        if not candidates and not truncated:
            return summary
        with _ledger_lock(self.run_id, deadline):
            self._sweep_candidates(now, candidates, truncated, deadline, summary)
        return summary

    def _sweep_candidates(
        self, now: dict, candidates: list[str], truncated: bool, deadline: float, summary: dict
    ) -> None:
        ledger = _Ledger(self.run_id)
        queued, stored = self._known_elsewhere()
        secret_skips: list[str] = []
        redacted: list[str] = []
        listed: list[dict] = []
        storage_of: dict[str, dict] = {}
        mount_points = ephemeral.mount_points()
        # References, queued AFTER every upload: hashing one (F3) reads up to
        # 1 GiB, and the close's time goes to uploads first.
        references: list[tuple] = []
        # Seconds per byte of inspect-and-stage, learned as the sweep goes;
        # it starts at the measured ~1 MB/s. A file that would run past the
        # deadline is not started: the budget is a bound, not a hint.
        per_byte = 1e-6

        def _already(rel: str, full: str, digest: str, logged: dict | None) -> bool:
            return (
                ledger.has(rel, digest)
                or digest in stored
                or digest in queued.get(full, ())
                or bool(logged and logged.get("sha256") == digest)
            )

        def _not_uploaded(rel: str, full: str, size: int, mtime_ns: int, storage: dict, code: str) -> None:
            if not storage["durable"]:
                listed.append({"path": rel, "size": size, "code": code, "reason": _REASONS[code]})
                return
            key = f"pointer:{size}:{mtime_ns}"
            if ledger.has(rel, key):
                summary["unchanged_logged"] += 1
                return
            # A pointer carries the PATH, never the bytes, so the path is what
            # must not hold a credential (a token in a folder name).
            if _findings(full)[0]:
                secret_skips.append(rel)
                return
            references.append((rel, full, size, mtime_ns, storage, code, key))

        for rel in candidates:
            # `root` is a real path and the walk never follows a link, so
            # `full` is real too.
            full = os.path.join(self.root, rel)
            size, mtime_ns = now[rel]
            reason = _skip_reason(os.path.basename(rel))
            if reason == "secret":
                secret_skips.append(rel)
                continue
            if reason is not None:
                continue  # generated: .pyc, .so, .DS_Store
            logged = self._logged.get(full)
            if logged and logged["stat"] == (size, mtime_ns):
                summary["unchanged_logged"] += 1
                continue
            if ledger.unchanged(rel, size, mtime_ns):
                # Queued by an earlier close, or by another process of this
                # run, and not touched since: not even read again.
                summary["unchanged_logged"] += 1
                continue
            if full in mount_points:
                # A file bind-mounted on its own (a Kubernetes subPath): its
                # storage is not its folder's.
                storage = ephemeral.describe(full)
            else:
                directory = os.path.dirname(full)
                storage = storage_of.get(directory)
                if storage is None:
                    storage = storage_of[directory] = ephemeral.describe(directory)
            if size > INSPECT_LIMIT_BYTES or time.monotonic() + size * per_byte >= deadline:
                code = TOO_LARGE if size > INSPECT_LIMIT_BYTES else OVER_BUDGET
                _not_uploaded(rel, full, size, mtime_ns, storage, code)
                continue
            started = time.monotonic()
            try:
                data, result, source_sha256 = secret_gate.read_upload_redacted_sourced(full, full_scan=True)
            except secret_gate.CredentialInPath:
                secret_skips.append(rel)
                continue
            except CredentialBlocked:
                if os.path.exists(full):
                    _not_uploaded(rel, full, size, mtime_ns, storage, UNINSPECTABLE)
                continue
            if _unredacted(result):
                # Found, and NOT replaced: a container, a checkpoint, bytes
                # that are not UTF-8. Uploading would ship it byte-for-byte.
                secret_skips.append(rel)
                continue
            if result.rewritten:
                redacted.append(rel)
            digest = hashlib.sha256(data).hexdigest()
            if _already(rel, full, digest, logged):
                # Keyed on the STORED bytes: a later original that redacts to
                # bytes already stored is not uploaded again (see WHAT A READER
                # CAN MATCH); its own hash rides the run's write list.
                summary["unchanged_logged"] += 1
                continue
            meta = self._meta(full, storage)
            if source_sha256 != digest:
                # Redacted: the stored hash names bytes no reader opened.
                meta["source_sha256"] = source_sha256
            # The bytes inspected are the bytes staged: the file is not opened
            # again, so a writer racing the close cannot swap what leaves.
            queued_ok = self._queue_generated(OUTPUT_PREFIX + rel, data, meta=meta)
            del data
            if size >= 1_000_000:
                per_byte = max(per_byte * 0.5, (time.monotonic() - started) / size)
            if queued_ok:
                ledger.add(rel, digest, size, mtime_ns)
                summary["uploaded"] += 1
        if references:
            # Hashed from what the run's I/O budget has left after its reads
            # and writes, in the time the uploads left (F3).
            from . import inputs as _inputs

            budget = _inputs.reference_budget(self.run_id)
            for rel, full, size, mtime_ns, storage, code, key in references:
                content_hash = self._reference_hash(full, size, mtime_ns, budget, deadline)
                if content_hash is None:
                    summary["referenced_unhashed"] = summary.get("referenced_unhashed", 0) + 1
                self._queue_reference(rel, full, size, storage, why=_REASONS[code], content_hash=content_hash)
                ledger.add(rel, key, size, mtime_ns)
                summary["referenced"] += 1
        ledger.save()
        summary["skipped_secret"] = len(secret_skips)
        summary["listed"] = len(listed)
        if secret_skips:
            shown = ", ".join(secret_skips[:10])
            more = f" (+{len(secret_skips) - 10} more)" if len(secret_skips) > 10 else ""
            _diagnostics.warn(
                f"probe: did not upload {len(secret_skips)} output file(s) that may hold a "
                f"credential Probe could not redact: {shown}{more}. If one is safe to "
                "share, log it on purpose with log_artifact."
            )
        if redacted:
            shown = ", ".join(redacted[:10])
            more = f" (+{len(redacted) - 10} more)" if len(redacted) > 10 else ""
            _diagnostics.warn(
                f"probe: replaced credentials in {len(redacted)} output file(s) before upload: "
                f"{shown}{more}. The stored copies are not byte-identical to your files; "
                "the files on disk are unchanged."
            )
        if listed or truncated:
            self._queue_manifest(listed, truncated=truncated)
            self._warn_listed(listed, truncated)

    def _server_takes_multipart(self) -> bool:
        """Whether the server advertises `artifact_multipart` (plan (g)); a
        probe that fails is a no."""
        try:
            from .multipart import FEATURE

            return self.client is not None and self.client.supports_feature(FEATURE) is True
        except Exception:  # noqa: BLE001 -- advice only
            return False

    def _warn_listed(self, listed: list[dict], truncated: bool) -> None:
        shown = ", ".join(item["path"] for item in listed[:10])
        more = f" (+{len(listed) - 10} more)" if len(listed) > 10 else ""
        codes = {item["code"] for item in listed}
        advice = []
        if TOO_LARGE in codes:
            # Capture never uploads one (D12). An explicit log_artifact does,
            # in parts -- but only against a server that ADVERTISES multipart
            # uploads (g); against any other (today's prod among them) it
            # cannot either, so the advice must not send you there.
            if self._server_takes_multipart():
                advice.append(
                    f"capture does not upload a file {_REASONS[TOO_LARGE]} from this machine's "
                    "own disk -- `run.log_artifact(path)` uploads one you want kept (in parts), "
                    "or write it to a bucket or a mounted volume, where capture records where it is"
                )
            else:
                advice.append(
                    f"a file {_REASONS[TOO_LARGE]} on this machine's own disk cannot be kept -- "
                    "write it to a bucket or a mounted volume, where capture records where it is"
                )
        if OVER_BUDGET in codes:
            advice.append(
                "capture stopped inspecting files when its time at close ran out -- narrow it "
                f"with probe.init(outputs=...) or raise {BUDGET_ENV}"
            )
        if truncated:
            advice.append(
                f"the folder listing stopped early (over {MAX_FINAL_ENTRIES:,} files, or out of "
                "time) -- narrow it with probe.init(outputs=...)"
            )
        _diagnostics.warn(
            f"probe: {len(listed)} output file(s) were not stored and are listed in "
            f"{MANIFEST_NAME}" + (f": {shown}{more}" if listed else "") + "."
            + "".join(f" Note: {line}." for line in advice)
        )

    def _meta(self, full: str, storage: dict) -> dict:
        return {
            "capture": CAPTURE_OUTPUTS,
            "source_path": full,
            "host": self.host,
            **({"storage": storage["fstype"]} if storage.get("fstype") else {}),
        }

    # -- queueing -------------------------------------------------------------------
    def _queue_upload(self, name: str, path: str, *, meta: dict) -> bool:
        """Journal a non-blocking, STAGED upload; if the outbox cannot take it,
        upload now, still through the gate and still fail-open."""
        kind = artifact_kind_for(name)
        try:
            queued = self.journal.append_upload(
                anchor="run",
                anchor_id=self.run_id,
                name=name,
                src_path=path,
                stage=True,
                inline_hash=True,
                kind=kind if kind != "file" else None,
                meta=meta,
                run_ref=self.run_id,
                require_staged=True,
                blocking=False,
            )
        except CredentialBlocked:
            return False
        except Exception:  # noqa: BLE001 -- a queue that cannot take it: upload now
            queued = None
        if queued and queued.get("op_id"):
            self.enqueued += 1
            if self.client is not None:
                try:
                    self.client._after_enqueue()
                except Exception:  # noqa: BLE001
                    pass
            return True
        if self.client is None:
            return False
        try:
            with prepare_upload(path) as prepared:
                digest, size = fingerprint(prepared.path)
                self.client.upload_fingerprinted(
                    "run", self.run_id, name, prepared.path,
                    digest=digest, size=size, kind=kind if kind != "file" else None, meta=meta,
                )
            return True
        except Exception as exc:  # noqa: BLE001
            _diagnostics.warn(
                f"probe: could not upload output {name!r} ({type(exc).__name__}); "
                "it is not stored on the run."
            )
            return False

    @staticmethod
    def _reference_hash(
        full: str, size: int, mtime_ns: int, budget: list[int], deadline: float
    ) -> str | None:
        """The sha256 a reference carries (F3), or None: over 1 GiB, changed
        since the listing, or past what the budget or the deadline allow."""
        try:
            from . import inputs as _inputs

            return _inputs.reference_hash(
                full, budget=budget, deadline=deadline, size=size, mtime_ns=mtime_ns
            )
        except Exception:  # noqa: BLE001 -- a hash never costs the reference
            return None

    def _queue_reference(
        self, rel: str, full: str, size: int, storage: dict, *, why: str, content_hash: str | None = None
    ) -> None:
        from ..models import ArtifactCreate

        body = ArtifactCreate(
            kind=artifact_kind_for(rel),
            name=OUTPUT_PREFIX + rel,
            uri=local_file_uri(full),
            size_bytes=size,
            content_hash=content_hash,
            is_reference=True,
            meta={
                "capture": CAPTURE_OUTPUTS,
                "local_path": full,
                "host": self.host,
                "reason": why,
                **({"storage": storage["fstype"]} if storage.get("fstype") else {}),
            },
        ).model_dump(mode="json", exclude_none=True)
        self.journal.append_http(
            "POST", f"/v1/runs/{self.run_id}/artifacts", body, run_ref=self.run_id, blocking=False
        )
        self.enqueued += 1

    def _queue_generated(self, name: str, data: bytes, *, meta: dict) -> bool:
        """Upload ``data`` from a private temporary file; the journal stages
        its own copy before this returns."""
        directory = _private_dir("outputs")
        fd, tmp = tempfile.mkstemp(prefix=f"{self.run_id}.", suffix=f".{os.path.basename(name)}", dir=directory)
        try:
            with os.fdopen(fd, "wb") as fh:
                fh.write(data)
            return self._queue_upload(name, tmp, meta=meta)
        finally:
            Path(tmp).unlink(missing_ok=True)

    def _queue_log(self, log_path: str, stats: dict | None, shared: list[str]) -> bool | None:
        """Queue the log: True when queued, False when it could not be (worth a
        retry), None when there is nothing to send."""
        try:
            raw = Path(log_path).read_bytes()
        except OSError:
            return None
        if not raw:
            return None
        # The TERMINAL and the local file get the program's exact bytes. The
        # uploaded copy is valid UTF-8 first, because the gate can only redact
        # text: a credential printed beside one stray binary byte would
        # otherwise ship byte-for-byte.
        data, result = redact_log_text(raw.decode("utf-8", errors="replace"))
        if data is None:
            _diagnostics.warn(
                f"probe: {self.log_name} was not uploaded: it holds a credential Probe "
                f"could not redact. The local copy is {log_path}."
            )
            return None
        meta = {
            "capture": CAPTURE_LOG,
            "host": self.host,
            **{k: v for k, v in (stats or {}).items() if k in ("total_bytes", "omitted_bytes")},
            **({} if stats else {"log_incomplete": True}),
            **({"shared_with": shared} if shared else {}),
        }
        if result.rewritten:
            _diagnostics.warn(
                f"probe: replaced credentials in {self.log_name} before upload; "
                f"the local copy is unchanged."
            )
        queued = self._queue_generated(self.log_name, data, meta=meta)
        if queued and stats:
            _discard_local_log(log_path)
        return queued

    def _queue_manifest(self, listed: list[dict], *, truncated: bool) -> None:
        body = json.dumps(
            {
                "note": "Files this run wrote that output capture listed but did not store.",
                "root": self.root,
                "host": self.host,
                "listing_truncated": truncated,
                "files": listed,
            },
            indent=2,
        ).encode("utf-8")
        self._queue_generated(MANIFEST_NAME, body, meta={"capture": CAPTURE_OUTPUTS})


def _warn_shared(run_id: str, others: list[str], root: str) -> None:
    if run_id in _shared_warned:
        return
    _shared_warned.add(run_id)
    _diagnostics.warn(
        f"probe: run {run_id} and {', '.join(others)} wrote to {root} at the same time, so "
        "their output files cannot be told apart; output capture skipped them (logs are "
        "still saved). Give each run its own folder with probe.init(outputs=...)."
    )


class _Ledger:
    """What was already queued for one run, on disk: ``{relative path: sha256
    or pointer key}`` plus the ``(size, mtime_ns)`` it had then. A second close
    -- a re-finish, a resumed attempt, another rank of the run -- queues
    nothing twice, and skips an untouched file without reading it."""

    def __init__(self, run_id: str):
        self.path = _private_dir("outputs") / f"{run_id}.json"
        try:
            data = json.loads(self.path.read_text())
            self.files: dict[str, str] = dict(data.get("files") or {})
            self.stats: dict[str, list] = dict(data.get("stats") or {})
        except (OSError, ValueError, AttributeError, TypeError):
            self.files, self.stats = {}, {}
        self._dirty = False

    def has(self, rel: str, key: str) -> bool:
        return self.files.get(rel) == key

    def unchanged(self, rel: str, size: int, mtime_ns: int) -> bool:
        return rel in self.files and self.stats.get(rel) == [size, mtime_ns]

    def add(self, rel: str, key: str, size: int, mtime_ns: int) -> None:
        self.files[rel] = key
        self.stats[rel] = [size, mtime_ns]
        self._dirty = True

    def save(self) -> None:
        if not self._dirty:
            return
        try:
            _prune(self.path.parent)
            # Merge with what another rank saved meanwhile.
            try:
                on_disk = json.loads(self.path.read_text())
                files = {**dict(on_disk.get("files") or {}), **self.files}
                stats = {**dict(on_disk.get("stats") or {}), **self.stats}
            except (OSError, ValueError, AttributeError, TypeError):
                files, stats = self.files, self.stats
            _write_json(self.path, {"files": files, "stats": stats})
        except OSError:
            pass


# -- recovery ------------------------------------------------------------------------------
def _claim_path(entry: Path) -> Path:
    return Path(str(entry) + ".recovering")


def _claim_fresh(entry: Path) -> bool:
    try:
        return time.time() - _claim_path(entry).stat().st_mtime < CLAIM_STALE_SECONDS
    except OSError:
        return False


def _claim(entry: Path) -> bool:
    """One recoverer per record, across processes. A claim left by a recoverer
    that died goes stale and is taken over."""
    claim = _claim_path(entry)
    for _ in range(2):
        try:
            fd = os.open(str(claim), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            if _claim_fresh(entry):
                return False
            claim.unlink(missing_ok=True)
            continue
        except OSError:
            return False
        os.close(fd)
        return True
    return False


def _recovery_client(record: dict) -> tuple[Any, Any]:
    """``(client, journal)`` for the context the run was opened under -- never
    whatever context is current where recovery happens to run. When that
    context no longer resolves to the same server, only the journal: the ops
    wait there for a drain under the right credentials."""
    context = record.get("context") or {}
    try:
        from .client import Client
        from .config import resolve

        if context.get("principal"):
            # The run recorded which credential it wrote with (#2035): the
            # recovery lists and uploads with THAT one, or with none -- never
            # with whatever this process resolves (#2041 review). The same
            # rule the drain applies to the run's queued writes.
            from .journal import _settings_for_op

            settings = _settings_for_op(context)
        else:
            settings = resolve(context=context.get("name") or None)
        recorded = (context.get("base_url") or "").rstrip("/")
        if recorded and settings.base_url != recorded:
            raise RuntimeError("the run's context now points elsewhere")
        from .journal import Journal

        journal = Journal(record.get("journal_dir") or None, context=context)
        client = Client(settings=settings, journal=journal)
        return client, journal
    except Exception:  # noqa: BLE001 -- no credentials here: queue for a later drain
        from .journal import Journal

        return None, Journal(record.get("journal_dir") or None, context=context)


def recover(entry_path: str) -> dict | None:
    """Finish the capture of a run whose process died: sweep its folder against
    the baseline it recorded, queue its log, deliver what can be delivered.

    Started by the log helper the moment it sees the run's process gone. Runs
    in a fresh interpreter with the run's own environment."""
    entry = Path(entry_path)
    try:
        record = json.loads(entry.read_text())
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict) or not _claim(entry):
        return None
    client, journal = _recovery_client(record)
    try:
        capture = OutputCapture(
            client,
            record["run_id"],
            record["root"],
            tee=False,
            launcher=bool(record.get("launcher")),
            journal=journal,
            recovery=True,
            ignore=_ignore.from_record(record.get("ignore")),
        )
        capture._entry = entry
        capture.log_name = str(record.get("log_name") or LOG_NAME)
        capture._baseline_file = Path(record["baseline"]) if record.get("baseline") else None
        if capture._baseline_file is None:
            capture._sweep_done = True  # a log-only recovery (see _recover_stale_logs)
        else:
            try:
                raw = json.loads(capture._baseline_file.read_text())
                capture.baseline = {k: (int(v[0]), int(v[1])) for k, v in raw.items()}
            except (OSError, ValueError, TypeError, IndexError, AttributeError):
                # Without its baseline every file would look new: never guess.
                capture._sweep_done = True
        log_path = record.get("log_path")
        summary = capture.finalize(log_path=log_path, log_stats=read_stats(log_path) if log_path else None)
        if log_path:
            # The live stream's last lines -- often the crash itself -- from
            # where the dead process's shipper stopped.
            _logstream.drain_spool(
                client,
                record["run_id"],
                log_path,
                capture.log_name,
                budget=_logstream.FINAL_FLUSH_SECONDS,
                stream=record.get("log_stream") or None,
                write_epoch=record.get("write_epoch"),
            )
        if client is not None:
            try:
                client.flush(run_ref=record["run_id"])
            except Exception:  # noqa: BLE001 -- left queued for the drainer
                client._kick_drainer(force=True)
        return summary
    finally:
        for path in (entry, _claim_path(entry), *entry.parent.glob(f"{entry.name}.writer-*")):
            path.unlink(missing_ok=True)


def _gone_path(entry: Path) -> Path:
    return Path(str(entry) + ".gone")


def _process_start(pid: int) -> str | None:
    """The kernel's start time of ``pid`` (/proc/<pid>/stat field 22, in clock
    ticks since boot), or None where /proc cannot say. With the pid, it names
    ONE process: a pid the kernel reused for another process has another."""
    try:
        stat = Path(f"/proc/{int(pid)}/stat").read_text()
    except (OSError, ValueError):
        return None
    # The command name (field 2) may hold spaces and parentheses: split after
    # its LAST ")".
    fields = stat.rsplit(")", 1)[-1].split()
    return fields[19] if len(fields) > 19 else None


def mark_forked_writer(entry: Path | str, pid: int) -> None:
    """A forked child of the run's process is writing the run (see
    `Run._note_forked_writer`): ``ENTRY.writer-<pid>``, holding the child's
    start time so a later check cannot mistake a reused pid for it."""
    marker = Path(f"{entry}.writer-{int(pid)}")
    marker.touch(mode=0o600, exist_ok=True)
    start = _process_start(pid)
    if start is not None:
        try:
            marker.write_text(start)
        except OSError:
            pass


def _forked_writer_alive(entry: Path) -> int | None:
    """The pid of a forked child still writing this record's run, or None.
    Same host by construction: the registry is per host. A marker whose pid
    now names ANOTHER process (a different start time: the pid was reused)
    counts as gone (review of #2049)."""
    for marker in entry.parent.glob(f"{entry.name}.writer-*"):
        try:
            pid = int(marker.name.rsplit("-", 1)[1])
            oscompat.probe_pid(pid)
        except (ValueError, ProcessLookupError):
            marker.unlink(missing_ok=True)
            continue
        except PermissionError:
            continue  # another user's process: never this run's forked writer
        except OSError:
            continue
        try:
            recorded = marker.read_text().strip()
        except OSError:
            recorded = ""
        if recorded and _process_start(pid) not in (None, recorded):
            marker.unlink(missing_ok=True)  # the pid now names another process
            continue
        return pid
    return None


def writer_gone(entry_path: str) -> dict | None:
    """Report that this record's writer process is gone (SDK reliability 2.2).

    Started by the log helper the moment the run's process is reparented away
    from it -- a SIGKILL, the OOM killer, a segfault -- so the server can end a
    sole-writer run within seconds instead of after the reaper's 900 s. One
    report per record (``ENTRY.gone``, created exclusively, then holding the
    outcome). Only to a server that declares ``run_writer_gone``; one retry on
    a transient failure, then the op is queued for the drainer. The server
    decides whether the report is the whole story (sole writer, same epoch),
    so a report is never a verdict on its own.
    """
    entry = Path(entry_path)
    gone = _gone_path(entry)
    try:
        fd = os.open(str(gone), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(fd)
    except OSError:
        return None  # already reported (or cannot be claimed): once is enough
    outcome: dict = {"sent": False}
    try:
        try:
            record = json.loads(entry.read_text())
        except (OSError, ValueError):
            outcome["reason"] = "no_record"
            return outcome
        writer = (record.get("writer") if isinstance(record, dict) else None) or {}
        run_id = record.get("run_id") if isinstance(record, dict) else None
        if not run_id or not writer.get("session_id") or writer.get("write_epoch") is None:
            outcome["reason"] = "no_writer"
            return outcome
        body = {
            "session_id": str(writer["session_id"]),
            "write_epoch": int(writer["write_epoch"]),
            "observed_by": "output_helper",
            "host": record.get("host"),
            "pid": record.get("pid"),
            "sole_writer": bool(writer.get("sole_writer")),
        }
        survivor = _forked_writer_alive(entry)
        if survivor is not None:
            # A daemonizing script: the process that opened the run forked and
            # exited, and its child carries the run on (review of #2049).
            outcome["reason"] = "writer_continues"
            outcome["pid"] = survivor
            return outcome
        client, journal = _recovery_client(record)

        def queue() -> dict:
            # Queued for the drainer: a partition must not lose the report
            # (review of #2049). Non-blocking, so a server that turns out to
            # lack the route dead-letters it without holding anything, and the
            # server still judges it when it lands (a late report on a run a
            # relaunch reopened is `stale_epoch`, a no-op).
            try:
                journal.append_http(
                    "POST",
                    f"/v1/runs/{run_id}/writer-gone",
                    body,
                    run_ref=str(run_id),
                    blocking=False,
                )
                if client is not None:
                    client._kick_drainer(force=True)
                outcome["queued"] = True
            except Exception:  # noqa: BLE001 -- the reaper still ends the run
                pass
            return outcome

        if client is None:
            outcome["reason"] = "no_client"
            return queue()
        try:
            if not client.supports_feature("run_writer_gone"):
                outcome["reason"] = "unsupported"
                return outcome
        except Exception:  # noqa: BLE001 -- unreachable now; the drainer retries
            outcome["reason"] = "unreachable"
            return queue()
        from . import errors as _errors

        for attempt in range(2):
            try:
                outcome.update(client.report_writer_gone(str(run_id), body) or {})
                outcome["sent"] = True
                return outcome
            except _errors.TransportError as exc:
                outcome["error"] = type(exc).__name__
                if attempt == 0:
                    time.sleep(1.0)
            except _errors.ServerError as exc:
                outcome["error"] = type(exc).__name__
                if attempt == 0:
                    time.sleep(1.0)
            except Exception as exc:  # noqa: BLE001 -- a refusal is final
                outcome["error"] = type(exc).__name__
                return outcome
        return queue()
    finally:
        try:
            _write_json(gone, outcome)
        except OSError:
            pass


def _recover_stale_logs() -> None:
    """Records whose process died and whose helper could not recover them (the
    whole process group was killed, or log capture was off). Only the LOG is
    sent: sweeping a folder long after the run would attribute other runs'
    files to it. A record whose helper still runs is its helper's to recover."""
    try:
        registry = _registry()
        entries = _entries()
    except OSError:
        return
    for path, record in entries:
        if _record_alive(record) or _helper_alive(record) or _claim_fresh(path):
            continue
        try:
            baseline = record.get("baseline")
            if baseline:
                Path(str(baseline)).unlink(missing_ok=True)
            record["baseline"] = None  # log only
            _write_json(path, record)
        except (OSError, TypeError, ValueError):
            continue
        _spawn_recovery(str(path))
    _prune(registry)


def _default_signals() -> None:
    """The log helper that starts a recovery ignores nearly every signal, and
    ignored signals survive exec: a recovery (and the drainer it starts) that
    inherited them could be stopped by nothing short of SIGKILL."""
    import signal

    from .logcapture import _IGNORED_SIGNALS

    for name in _IGNORED_SIGNALS:
        signum = getattr(signal, name, None)
        if signum is None or name == "SIGPIPE":
            continue  # Python keeps SIGPIPE ignored; so does this
        try:
            signal.signal(signum, signal.default_int_handler if name == "SIGINT" else signal.SIG_DFL)
        except (OSError, ValueError, RuntimeError):
            pass


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--recover":
        _default_signals()
        recover(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "--writer-gone":
        _default_signals()
        writer_gone(sys.argv[2])
