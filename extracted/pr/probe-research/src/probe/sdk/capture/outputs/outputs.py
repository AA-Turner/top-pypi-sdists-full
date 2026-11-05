"""What a run produced, captured when it ends (daemon-v2 plan, D17).

A run's output files used to reach Probe only if the script called
``log_artifact``, and nothing it printed was kept. The SDK runs INSIDE the run,
so it knows when the run started and ended and which folder it worked in -- on
any machine, including a Modal/Ray/Slurm job nothing else can see. It captures:

* **Outputs.** At run open the watched folder is listed (path, size, mtime --
  no hashing). At the end every file created or changed since is captured as
  ``outputs/<its path in the folder>``.
* **The log.** Everything the run printed, as ``probe/run.log`` (see
  :mod:`probe.sdk.capture.logs.logs`). While the run is alive the same output is also
  streamed to the server, complete lines every 15 s, for the run page's Logs
  panel (:mod:`probe.sdk.capture.logs.stream`); the artifact stays the durable copy.

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

WHAT HAPPENS TO EACH FILE -- the storage decides (:mod:`probe.sdk.run.launch.ephemeral`):

=============================  =================================  =================
file                           where it sits                      captured as
=============================  =================================  =================
up to 64 MB                    anywhere                           upload (redacted)
64 MB - 5 GB, team switched    anywhere it can be hardlinked or   upload in parts
on (`artifact_auto_multipart`) reflinked into the outbox          (not scanned past
                                                                  64 MB)
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

IN PARTS (2026-10-12, D4/D18/D19). For a team switched on server-side
(`GET /v1/teams/features` lists `artifact_auto_multipart`), a file between 64 MB
and 5 GB goes to the multipart queue instead (:mod:`probe.sdk.artifact.storage_handlers.multipart`): staged
by hardlink or reflink only -- never a byte copy on the closing thread -- hashed
and sent by the detached outbox worker after the process exits. Only where that
worker exists on durable storage (`multipart.settle_reason` is None): on a
throwaway box an op queued at the close would vanish with the disk, so the rows
above stand there.

THE CLOSE IS BOUNDED. Inspection runs ~1 MB/s on JSON text, so a close is given
:func:`close_budget` seconds (``PROBE_CAPTURE_BUDGET_SEC``, capped by the
finish timeout when one is set). The log is queued first; once the budget is
spent the remaining files are pointed to or listed, never inspected.

THE SAFETY STOPS:

* Skipped directories: VCS, virtualenvs, ``node_modules``, ``__pycache__``,
  tool caches, credential directories (``snapshot.SKIP_DIRS``) plus ``.cache``
  and ``.probe``, the outbox journal, Probe's own state directory, every other
  folder the SDK keeps files in (``probe.sdk.capture.owndirs``: another outbox, the
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
the run's write list (``POST /v1/runs/{id}/outputs``, :mod:`probe.sdk.capture.lineage`)
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
import os
import secrets
import socket
import threading
import time
from pathlib import Path
from typing import Any
from ..logs import stream as _logstream
from ....foundation.safe_warn import safe_warn as _diagnostics
from ....foundation.compose.compose import compose
from probe.sdk.capture.outputs.host_registry import CaptureRegistryMixin, _registry, _warn_shared, log_owned_here
from probe.sdk.capture.outputs.log import (
    LOG_NAME,
    LogTeeMixin,
    _OFF,
    _distributed_log_name,
    in_process_log_supported,
    log_enabled,
    reserve_log_path,
)
from probe.sdk.capture.outputs.queue import OutputQueueMixin
from probe.sdk.capture.outputs.sweep import BUDGET_ENV, OutputSweepMixin, _walk, _warn_unreachable_patterns

CAPTURE_ENV = "PROBE_CAPTURE_OUTPUTS"
#: Seconds a close may spend inspecting files, unless ``PROBE_CAPTURE_BUDGET_SEC``
#: or the finish timeout says otherwise.
CLOSE_BUDGET_SECONDS = 120.0
#: How long the listing at run open may take before the folder counts as a
#: workspace (a network drive answers every lstat over the wire).
OPEN_WALK_SECONDS = 10.0
MAX_BASELINE_ENTRIES = 50_000


# -- switches -----------------------------------------------------------------------
def enabled(capture_outputs: bool | None) -> bool:
    """The caller's argument wins; otherwise ``PROBE_CAPTURE_OUTPUTS`` (on)."""
    if capture_outputs is not None:
        return bool(capture_outputs)
    return (os.environ.get(CAPTURE_ENV) or "").strip().lower() not in _OFF


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


def target_root(*, outputs: str | os.PathLike | None = None, cwd: str | None = None) -> str:
    """The folder a capture with these arguments watches."""
    base = os.path.abspath(cwd or os.getcwd())
    return os.path.realpath(os.path.join(base, os.fspath(outputs)) if outputs else base)


# -- process-wide hooks -------------------------------------------------------------------
_live: set["OutputCapture"] = set()
_live_lock = threading.Lock()
_atexit_installed = False


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


@compose
class OutputCapture(
    CaptureRegistryMixin,
    LogTeeMixin,
    OutputSweepMixin,
    OutputQueueMixin,
):
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
        #: The run's `.probeignore` rules (`probe.sdk.recording_rules.recording_rules.IgnoreRules`), or None.
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
            from ..logs.logs import InProcessTee

            self._log_path = reserve_log_path(self.run_id)
            self._entry = _registry() / f"{self._key}.json"
            # Before the helper starts: the spool directory is what asks it
            # to stream (the log helper's LIVE mode).
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
from probe.sdk.capture.outputs.recovery import _recover_stale_logs  # noqa: E402 -- pieces need each other; the front door loads this one first
