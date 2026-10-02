"""PyTorch Lightning logger for Probe (plan (a), task T27).

    from lightning.pytorch import Trainer
    from probe.integrations.lightning import ProbeLogger

    trainer = Trainer(logger=ProbeLogger(experiment="mnist", name="lr-3e-4"))

What it does, by Lightning hook (verified against Lightning 2.6.6):

* ``experiment`` -- Lightning touches it on EVERY rank in ``_call_setup_hook``,
  after the process group exists and before the ``pre_setup`` barrier. Global
  rank 0 opens the run (see "Which run" below); a failed init degrades to a
  no-op logger (outside ``strict``) rather than failing the job. There, and
  only there, rank 0 broadcasts ``(run id, write epoch)`` to every rank, so
  every rank knows the run it belongs to (see "All ranks" below).
* ``log_metrics`` -- rank 0 only, ``run.log(metrics, step=step)``, never raises
  outside ``strict``.
* ``log_hyperparams`` -- rank 0 only: the module's ``save_hyperparameters()``
  values merged into the run's config with ``run.update_config`` (plan (c)
  coercion: Namespace, dataclasses, numpy/torch scalars, non-finite floats).
* ``after_save_checkpoint`` -- rank 0 only: the checkpoint ``ModelCheckpoint``
  just wrote becomes a checkpoint artifact on the run (a path REFERENCE by
  default: a 10 GB checkpoint is not copied through the API), with
  ``meta.score`` / ``monitor`` / ``step`` / ``best`` / ``last``. A sharded
  checkpoint is a folder; its size is the folder's. As top-k pruning moves on,
  the rows of earlier checkpoints are refreshed: ``best`` follows the
  callback, ``superseded`` marks one it no longer keeps, ``deleted`` one whose
  path is gone.
* ``finalize`` -- never finishes the run (Lightning calls it after EVERY stage,
  and ``fit`` then ``test`` is one run): the process's own exit decides that
  (``probe.init``'s exit hooks, or your ``probe.finish()``). On
  ``finalize("failed")`` it tells that close how the job ended, which no process
  hook can see for Lightning: Ctrl-C is caught and turned into ``sys.exit(1)``
  (-> ``canceled``), and SIGTERM becomes ``SIGTERMException``, a code-less exit
  0 (-> ``failed``). An ordinary exception is noted too, except on a launcher's
  run: there the launcher reads the real exit code, and a failure the script
  caught did not end the process. A new Trainer adopting a shared run also
  forgets the previous Trainer's noted ending, for the same reason.

Which run: rank 0 adopts a run the script opened itself with ``probe.init()``
(and never finishes it); otherwise it calls ``probe.init(...)``. A run an
EARLIER ``ProbeLogger`` in this process opened is not adopted: that is a sweep
loop, and each Trainer is its own trial, so the earlier run is closed (with the
verdict its ``finalize`` recorded) and a new one opened. Under a launcher that
exported ``PROBE_RUN_ID`` (``probe exec``) the process has exactly one run, the
launcher's, and every logger writes to it. A second Trainer writing into a run
it shares (the script's, or the launcher's) is warned: where both log a metric
at the same step the server keeps the first point, so the second curve is lost
there.

Forked and spawned workers (``ddp_fork``, ``ddp_notebook``, ``ddp_spawn``): a
run a worker opens is closed when the worker exits. torch's worker wrapper
swallows KeyboardInterrupt, and Lightning's own ``finalize("failed")`` runs in
the parent, whose logger holds no run, so the worker learns its ending itself:
a SIGINT handler chained in front of the one it found (Ctrl-C -> ``canceled``;
the parent-death SIGINT torch arms -> ``failed``), and Lightning's
``SIGTERMException`` in flight at exit (-> ``failed``, as under torchrun).

All ranks: plan 2.8 detects a lost node only if every rank holds a writer
lease, while metrics stay rank-0-only. So each other rank, once it has the run
id and epoch, joins that run as a LEASE-ONLY writer (``_rank_lease``): it
beats its own ``rank`` lease and writes nothing else -- no metric, no
capture, no status -- and releases the lease when it ends: at
``finalize("failed")`` (Lightning's SIGTERM is a code-less exit no exit hook
reads as a failure, and the release goes out before Lightning's teardown),
else when the process exits. A server without per-writer leases gets nothing
from it.

Not re-exported from ``probe.integrations`` (which imports miles eagerly), and
nothing under ``probe`` imports this module: ``import probe`` must never load
Lightning or torch.
"""

from __future__ import annotations

import logging
import math
import multiprocessing
import multiprocessing.context
import os
import signal
import stat
import sys
import threading
import uuid
from argparse import Namespace
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

try:  # the unified package first, then the standalone one
    from lightning.fabric.utilities.logger import (
        _add_prefix,
        _convert_params,
        _sanitize_callable_params,
    )
    from lightning.pytorch.loggers.logger import DummyExperiment, Logger
    from lightning.pytorch.utilities.rank_zero import rank_zero_only
except ImportError:  # pragma: no cover - exercised only without `lightning`
    try:
        from lightning_fabric.utilities.logger import (  # type: ignore[no-redef]
            _add_prefix,
            _convert_params,
            _sanitize_callable_params,
        )
        from pytorch_lightning.loggers.logger import DummyExperiment, Logger  # type: ignore[no-redef]
        from pytorch_lightning.utilities.rank_zero import rank_zero_only  # type: ignore[no-redef]
    except ImportError as _missing:
        # `name` carries the missing module, as a plain ModuleNotFoundError
        # would: callers (and test_import_every_module) tell an absent optional
        # extra from a broken import by it.
        raise ImportError(
            "probe.integrations.lightning needs PyTorch Lightning, which is not installed. "
            "Install it with Probe's extra: pip install 'probe-research[lightning]'",
            name=getattr(_missing, "name", None) or "lightning",
        ) from _missing

import probe
from probe.sdk import fluent, hashing, safe_warn

from . import _rank_lease
from ._worker_exit import (  # noqa: F401 -- also read from here by tests
    WORKER_CLOSE_SECONDS,
    WORKER_HOLD_SECONDS,
    _signals_held,
    cap_finish_timeout,
    run_held,
)

log = logging.getLogger(__name__)

#: Metric keys get the prefix with the separator the dashboard sections on.
PREFIX_SEPARATOR = "/"

#: How a kept checkpoint is recorded: a path reference (default) or its bytes.
CHECKPOINTS = ("reference", "upload")

#: How long closing the previous trial's run may hold the next Trainer's start
#: before the rest of its delivery is deferred to the outbox (plan (j)'s bound).
PREVIOUS_RUN_FLUSH_SECONDS = 10.0

#: Runs a ProbeLogger opened with ``probe.init()``: run id -> the pid that
#: opened it. A later ProbeLogger in that process finishes such a run instead
#: of adopting it: two Trainers in one script are two trials (a sweep loop),
#: never one run whose steps collide. A run the script opened itself is never
#: in here. A forked worker inherits the map, and a run its PARENT opened is
#: the parent's to close.
_LOGGER_RUNS: dict[str, int] = {}

#: Runs a ProbeLogger joined through ``PROBE_RUN_ID``. The launcher closes
#: them, so no logger ever does; a second logger is told it shares one.
_LAUNCHER_RUNS: set[str] = set()

#: Runs the script opened itself (``probe.init()``) that a ProbeLogger adopted.
#: The script closes them; a second logger is told it shares one.
_SCRIPT_RUNS: set[str] = set()

_ADOPT_IGNORES = ("project", "experiment", "name")


class ProbeLogger(Logger):
    """Log a Lightning run to Probe. See the module docstring for the hooks.

    ``project`` / ``experiment`` / ``name`` and any other keyword go to
    ``probe.init()`` (``question=``, ``tags=``, ``config=``, ``client=``, ...).
    A run the script already opened with ``probe.init()`` is adopted instead
    and never finished by this logger; its ``config=`` is merged into that run
    and the other arguments are ignored, with a warning. A second ProbeLogger
    adopting that same run is warned that the two Trainers share it (call
    ``probe.finish()`` between them to give each its own). A run an earlier
    ProbeLogger opened is closed and a new one opened (one run per Trainer).
    ``prefix`` is prepended to every metric key as ``prefix/key``. ``save_dir``
    is where Lightning puts checkpoints (``None``: the trainer's
    ``default_root_dir``). ``log_model=False`` records no checkpoints;
    ``checkpoints="upload"`` stores their bytes instead of a path reference
    (an uploaded row keeps the flags it was saved with). ``strict=True`` lets
    Probe errors raise instead of warning once.

    Spawned and forked workers (``ddp_spawn``, ``ddp_fork``, and
    ``ddp_notebook``, Lightning's default in Jupyter with more than one
    device) run every rank in a child process. A run first opened in one is
    closed when that worker exits; a forked worker leaves through
    ``os._exit``, which skips every exit hook, so the logger closes it through
    multiprocessing's own worker-exit finalizers: ``canceled`` on Ctrl-C,
    ``failed`` on SIGTERM or an error. That close is capped at
    :data:`WORKER_CLOSE_SECONDS` (what does not go out stays queued) so it
    fits inside torch's 30 s grace before SIGKILL. To get ONE run across
    ``fit`` then ``test`` (each launches fresh workers), read
    ``logger.experiment`` before ``trainer.fit``: the run then opens in the
    parent, the workers write to it, and the parent closes it at exit.
    """

    def __init__(
        self,
        *,
        project: str | None = None,
        experiment: str | None = None,
        name: str | None = None,
        prefix: str = "",
        save_dir: str | os.PathLike | None = None,
        checkpoints: str = "reference",
        log_model: bool = True,
        strict: bool = False,
        **init_kwargs: Any,
    ) -> None:
        super().__init__()
        if checkpoints not in CHECKPOINTS:
            raise ValueError(f"checkpoints must be one of {CHECKPOINTS}, not {checkpoints!r}")
        self._project = project
        self._experiment_name = experiment
        self._run_name = name
        self._prefix = prefix
        self._save_dir = os.fspath(save_dir) if save_dir is not None else None
        self._checkpoints = checkpoints
        self._log_model = log_model
        self._strict = strict
        self._init_kwargs = init_kwargs

        self._run = None  # the Run handle, rank 0 only
        self._run_id: str | None = None  # every rank, once known
        self._write_epoch: int | None = None
        self._rank_lease: _rank_lease.RankLease | None = None  # every other rank
        self._disabled = False  # init failed: a no-op logger from here on
        self._broadcast_done = False
        #: Lightning names the checkpoint folder after `version`. Without a run
        #: id (init failed), a FIXED fallback put every such job in one folder.
        self._offline_version = f"offline-{uuid.uuid4().hex[:8]}"
        #: A custom client= cannot be pickled; its settings can, into a worker
        #: this process launches (see __getstate__).
        self._client_settings: Any = None
        #: One entry per checkpoint path: what its row on the run says now.
        self._checkpoint_rows: dict[str, _CheckpointRow] = {}
        self._warned: set[str] = set()
        self._lock = threading.Lock()

    # -- identity (Lightning reads these for checkpoint paths) ------------------
    @property
    def name(self) -> str:
        return self._experiment_name or self._project or "probe"

    @property
    def version(self) -> str:
        # Opens the run on rank 0 but NEVER broadcasts: Lightning reads this on
        # every rank while resolving the checkpoint folder (and broadcasts rank
        # 0's folder itself), and only after `experiment` shared the id.
        self._ensure_run()
        return self._run_id or self._offline_version

    @property
    def save_dir(self) -> str | None:
        return self._save_dir

    # -- the run ------------------------------------------------------------------
    @property
    def experiment(self) -> Any:
        """The Probe ``Run`` on global rank 0; Lightning's dummy elsewhere.

        Shares the run id with the other ranks only when Lightning's
        ``_call_setup_hook`` is the reader: that is where every rank reads it
        at once. A collective started from anywhere else -- a callback, or
        ``prepare_data``, which runs on rank 0 alone -- would wait for ranks
        that never join, or pair with a different collective on them."""
        run = self._ensure_run()
        if sys._getframe(1).f_code.co_name == "_call_setup_hook":
            self._share_run_identity()
        return run if run is not None else DummyExperiment()

    def _ensure_run(self) -> Any:
        """The run on global rank 0 (opened on first use), else None."""
        if rank_zero_only.rank != 0:
            return None
        with self._lock:
            if self._run is None and not self._disabled:
                self._open_run()
            return self._run

    def _run_for_write(self) -> Any:
        """`_ensure_run`, for a hook about to write: says so, once, when the run
        is already closed. A newer ProbeLogger closed this logger's trial when
        its own Trainer started, or the script finished the run it had
        adopted, and every write from here on lands on a finished run, unseen.
        Reading `version` or `experiment` after the fact is not a write."""
        run = self._ensure_run()
        closed = getattr(run, "_closed_status", None) if run is not None else None
        if closed is not None:
            label = getattr(run, "slug", None) or run.id
            self._warn_once(
                "closed",
                f"probe: this ProbeLogger is still writing to run {label}, which is already "
                f"closed ({closed}): a newer ProbeLogger closed it when its own Trainer "
                "started (one run per Trainer), or the script finished it. What it logs now "
                "lands on that finished run. Give each Trainer its own ProbeLogger.",
            )
        return run

    def _open_run(self) -> None:
        """Rank 0: reattach after pickling, adopt the script's run, or init."""
        try:
            if self._run_id is not None:
                # Unpickled into a spawned process (ddp_spawn): the run exists;
                # write to it without claiming it (the parent owns its close).
                self._run = self._client_for_copy().attach_run(
                    self._run_id, heartbeat=False, write_epoch=self._write_epoch
                )
            else:
                active = probe.active_run()
                if active is not None and active.id in _LOGGER_RUNS:
                    if _LOGGER_RUNS[active.id] == os.getpid():
                        self._finish_previous_trial(active)
                    active = None  # a previous trial's run: never adopted
                if active is not None:
                    self._adopt(active)
                else:
                    self._run = self._init_run()
        except Exception as exc:
            if self._strict:
                raise
            self._disabled = True
            self._warn_once(
                "init",
                "probe: the Lightning logger could not open a run and is logging nothing "
                f"for this job ({type(exc).__name__}: {exc}). Training continues.",
            )
            return
        self._run_id = self._run.id
        self._write_epoch = getattr(self._run, "write_epoch", None)

    def _init_run(self) -> Any:
        kwargs = {
            key: value
            for key, value in (
                ("project", self._project),
                ("experiment", self._experiment_name),
                ("name", self._run_name),
            )
            if value is not None
        }
        kwargs.update(self._init_kwargs)
        launcher_run = os.environ.get("PROBE_RUN_ID", "").strip()
        if launcher_run:
            # probe.init() refuses identity kwargs next to PROBE_RUN_ID (the
            # launcher already chose the run), which here would have disabled
            # the logger for the whole job. Join the launcher's run instead.
            dropped = sorted(k for k in fluent._IDENTITY_KWARGS if kwargs.pop(k, None) is not None)
            if dropped:
                self._warn_once(
                    "launcher",
                    f"probe: PROBE_RUN_ID={launcher_run} is set (a launcher such as `probe exec` "
                    f"opened this job's run), so ProbeLogger's {', '.join(dropped)} were not "
                    "applied: the logger writes to that run.",
                )
        owned_client = None
        if "client" not in kwargs and self._client_settings is not None:
            from probe.sdk.client import Client

            owned_client = kwargs["client"] = Client(settings=self._client_settings)
        try:
            run = probe.init(**kwargs)
        except BaseException:
            if owned_client is not None:
                owned_client.close()
            raise
        if launcher_run:
            _LAUNCHER_RUNS.add(run.id)
        else:
            _LOGGER_RUNS[run.id] = os.getpid()
            if multiprocessing.parent_process() is not None:
                _close_when_this_worker_exits(owned_client)
                _chain_worker_sigint()
        return run

    def _adopt(self, active: Any) -> None:
        """Write to the run this process already has open; never finish it."""
        self._run = active
        label = getattr(active, "slug", None) or active.id
        # A new Trainer is starting, so the way the previous one on this run
        # ended (a failure the loop caught) did not end the process: it must
        # not decide the run's verdict at exit.
        fluent._forget_noted_exit(active)
        if active.id in _LAUNCHER_RUNS:
            self._warn_once(
                "shared",
                _shared_run_message(
                    label,
                    "PROBE_RUN_ID (a launcher such as `probe exec`) chose one run for the whole "
                    "process. Run each trial as its own process to give each its own run.",
                ),
            )
        else:
            if active.id in _SCRIPT_RUNS:
                self._warn_once(
                    "shared",
                    _shared_run_message(
                        label,
                        "the script opened it with probe.init(), and a ProbeLogger writes to "
                        "the run the script has open. Call probe.finish() before each new "
                        "Trainer to give it a run of its own.",
                    ),
                )
            _SCRIPT_RUNS.add(active.id)
            ignored = [k for k in _ADOPT_IGNORES if getattr(self, _ATTR[k]) is not None]
            ignored += sorted(
                k for k, v in self._init_kwargs.items() if v is not None and k not in ("client", "config")
            )
            if ignored:
                self._warn_once(
                    "adopt",
                    f"probe: ProbeLogger adopted run {label}, which this script opened with "
                    f"probe.init(), so its {', '.join(ignored)} were not applied (an open run is "
                    "written to, not re-created). Pass them to probe.init(), or call "
                    "probe.finish() before the Trainer starts to give it a run of its own.",
                )
        config = self._init_kwargs.get("config")
        if config is not None:
            self._guarded("config", active.update_config, config)

    def _finish_previous_trial(self, active: Any) -> None:
        """Close the run an earlier ProbeLogger opened: its Trainer is done.

        With the verdict that logger's ``finalize`` recorded (a trial whose
        exception the sweep loop caught is ``failed``), and a bounded flush:
        what does not go out within the bound stays queued in the outbox."""
        _LOGGER_RUNS.pop(active.id, None)
        noted = getattr(active, "_noted_exit", None)
        status, cause = noted if noted else ("completed", None)
        if status == "failed" and isinstance(cause, BaseException):
            try:
                from probe.sdk import diagnostics

                diagnostics.report_exception(active, cause)
            except Exception:  # noqa: BLE001 -- evidence never gates the close
                pass
        try:
            fluent.finish(status, flush_timeout=PREVIOUS_RUN_FLUSH_SECONDS)
        except Exception as exc:
            if self._strict:
                raise
            self._warn_once(
                "finish_previous",
                f"probe: the run an earlier ProbeLogger opened ({active.id}) did not close "
                f"cleanly ({type(exc).__name__}: {exc}); this Trainer opens its own run anyway.",
            )

    def _client_for_copy(self) -> Any:
        client = self._init_kwargs.get("client")
        if client is not None:
            return client
        from probe.sdk.client import Client

        if self._client_settings is not None:
            return Client(settings=self._client_settings)
        return Client()

    def _share_run_identity(self) -> None:
        """Once, on every rank: process-group rank 0 sends ``(run id, epoch)``.

        Only when a process group spans more than one process. Every branch
        before the collective reads state that is the same on every rank (the
        group, its size, the flag), so all ranks call it or none does; the
        source is the GROUP's rank 0 -- ``src=0`` means that rank -- so if
        Lightning's rank 0 is some other process, the group's rank 0 sends "no
        run" rather than a rank waiting on a payload nobody sends."""
        if self._broadcast_done:
            return
        try:
            import torch.distributed as dist
        except ImportError:  # pragma: no cover - lightning always brings torch
            return
        if not (dist.is_available() and dist.is_initialized()) or dist.get_world_size() < 2:
            return
        self._broadcast_done = True
        rank = dist.get_rank()
        payload = [(self._run_id, self._write_epoch) if rank == 0 else None]
        try:
            dist.broadcast_object_list(payload, src=0)
        except Exception as exc:  # noqa: BLE001 -- a rank that cannot hear carries on
            self._warn_once(
                "broadcast",
                f"probe: rank {rank} did not receive the run id from rank 0 "
                f"({type(exc).__name__}: {exc}); it will hold no writer lease.",
            )
            return
        if rank == 0:
            return
        received = payload[0]
        run_id, write_epoch = received if isinstance(received, tuple) and len(received) == 2 else (None, None)
        if run_id is None:
            # Rank 0 opened no run (its init failed, or it is not Lightning's
            # rank 0): there is nothing for this rank to hold a lease on.
            log.debug("probe: rank %s: rank 0 shared no run id", rank)
            return
        self._run_id, self._write_epoch = run_id, write_epoch
        self._start_rank_lease(run_id, write_epoch)

    def _start_rank_lease(self, run_id: str, write_epoch: int | None) -> None:
        """Every non-zero rank's liveness (plan 2.8): a lease-only writer on
        rank 0's run (``_rank_lease.hold``), so a lost node shows as a lease
        that stopped beating. Never a run-level heartbeat: one from each rank
        would keep the run alive when rank 0 is gone. A lease that cannot be
        taken warns once and training goes on (raises under ``strict``)."""
        import torch.distributed as dist

        rank = dist.get_rank()
        client = self._init_kwargs.get("client")
        try:
            self._rank_lease = _rank_lease.hold(
                run_id,
                write_epoch,
                rank=rank,
                client=client,
                client_factory=None if client is not None else self._client_for_copy,
            )
        except Exception as exc:
            if self._strict:
                raise
            self._warn_once(
                "rank_lease",
                f"probe: rank {rank} could not take its writer lease on run {run_id} "
                f"({type(exc).__name__}: {exc}); training continues, but a lost node "
                "there will not be seen.",
            )

    # -- Lightning's hooks --------------------------------------------------------
    @rank_zero_only
    def log_hyperparams(self, params: dict[str, Any] | Namespace, *args: Any, **kwargs: Any) -> None:
        run = self._run_for_write()
        if run is None:
            return
        params = _sanitize_callable_params(_convert_params(params))
        if params:
            self._guarded("log_hyperparams", run.update_config, params)

    @rank_zero_only
    def log_metrics(self, metrics: Mapping[str, float], step: int | None = None) -> None:
        run = self._run_for_write()
        if run is None:
            return
        metrics = _add_prefix(metrics, self._prefix, PREFIX_SEPARATOR)
        self._guarded("log_metrics", run.log, dict(metrics), step=step)

    @rank_zero_only
    def after_save_checkpoint(self, checkpoint_callback: Any) -> None:
        if not self._log_model:
            return
        run = self._run_for_write()
        if run is None:
            return
        self._guarded("checkpoint", self._record_checkpoints, run, checkpoint_callback)

    def finalize(self, status: str) -> None:
        """Never closes the run. On ``"failed"``, tell the exit close why.

        Lightning calls this from inside its ``except`` block, so the exception
        in flight is the one that stopped training. Also the last look at the
        checkpoint rows: top-k pruning deletes a file right AFTER the save that
        displaced it, so the final save's victim is noticed only here.

        On every other rank: ``"failed"`` releases this rank's lease with the
        same verdict, right here. Lightning's SIGTERM ends in a code-less exit
        0 that no exit hook reads as a failure, and the release goes out
        before Lightning's teardown puts back the default SIGTERM handler, under
        which the SIGTERM torch sends a surviving rank could kill it before any
        exit hook ran."""
        if rank_zero_only.rank != 0:
            self._end_rank_lease(status)
            return
        if self._run is None:
            return
        if status == "failed":
            exc = sys.exc_info()[1]
            verdict = _failed_verdict(exc, launcher_run=self._run.id in _LAUNCHER_RUNS)
            try:
                if verdict is not None:
                    fluent.note_exit(verdict, exc)
            except Exception:  # noqa: BLE001 -- teardown must never raise from here
                log.debug("probe: note_exit failed", exc_info=True)
        if self._log_model and self._checkpoint_rows:
            self._guarded("checkpoint", self._refresh_checkpoints, self._run, None)

    def _end_rank_lease(self, status: str) -> None:
        """A non-zero rank's ``finalize``: on ``"failed"``, release its lease
        with rank 0's rule for the verdict. Under a launcher's run an ordinary
        error decides nothing here (the launcher reads the real exit code), so
        the lease waits for the process's own exit. ``"success"`` ends a stage,
        not the process (``fit`` then ``test`` is one run): nothing."""
        lease = self._rank_lease
        if status != "failed" or lease is None:
            return
        exc = sys.exc_info()[1]
        launcher_run = os.environ.get("PROBE_RUN_ID", "").strip() == lease.run_id
        verdict = _failed_verdict(exc, launcher_run=launcher_run)
        if verdict is not None:
            lease.release(verdict)

    def save(self) -> None:
        """Nothing to flush: Probe writes go through its own outbox."""

    # -- pickling (ddp_spawn) ------------------------------------------------------
    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        state["_run"] = None  # a live handle holds a client and threads
        state["_rank_lease"] = None  # so does a rank's lease; each process takes its own
        state["_lock"] = None
        spawning = multiprocessing.context.get_spawning_popen() is not None
        client = state["_init_kwargs"].get("client")
        if client is not None:
            state["_init_kwargs"] = {k: v for k, v in state["_init_kwargs"].items() if k != "client"}
            if spawning:
                # Pickled to launch a worker (ddp_spawn): the worker talks to
                # the same server with the same credentials.
                state["_client_settings"] = getattr(client, "settings", None)
        if not spawning:
            # The settings carry a token: only ever through a launch pipe,
            # never into a file. A worker's copy (which holds them) pickled
            # again -- into a checkpoint, a cache -- used to write it out.
            if client is not None or state["_client_settings"] is not None:
                self._warn_once(
                    "pickle_client",
                    "probe: a ProbeLogger with client= was pickled; the copy builds its own "
                    "Client from the environment (PROBE_TOKEN / the stored login), not the one "
                    "you passed. A worker process Lightning spawns does get your client's "
                    "settings.",
                )
            state["_client_settings"] = None
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        self._lock = threading.Lock()

    # -- checkpoints ----------------------------------------------------------------
    def _record_checkpoints(self, run: Any, callback: Any) -> None:
        """Record the checkpoint this save wrote, then refresh earlier rows."""
        view = _CallbackView(callback)
        saved = getattr(callback, "_last_checkpoint_saved", None)
        if isinstance(saved, str) and saved:
            # ModelCheckpoint names the one file each save wrote; a folder
            # rewritten in place (a sharded `last.ckpt`) is a new save by step.
            self._record_one(run, saved, view, exact=True)
        else:  # another Checkpoint callback: every path it reports keeping
            for path in view.reported_paths():
                self._record_one(run, path, view, exact=False)
        self._refresh_checkpoints(run, view)

    def _record_one(self, run: Any, path: str, view: _CallbackView, *, exact: bool) -> None:
        local = os.path.abspath(path)
        try:
            info = os.stat(local)
        except OSError:
            return  # removed by top-k pruning before we got here
        is_dir = stat.S_ISDIR(info.st_mode)
        # A folder's mtime does not move when the files inside are rewritten,
        # so the step is what tells two saves of one folder apart.
        signature = (view.step if (exact or is_dir) else None, info.st_mtime_ns)
        row = self._checkpoint_rows.get(local)
        if row is not None and row.signature == signature:
            return
        reference = self._checkpoints == "reference" or is_dir
        if is_dir:
            size, n_files, complete = hashing.folder_size(local)
        else:
            size, n_files, complete = info.st_size, None, True
        meta = {
            "original_filename": os.path.basename(local),
            # Which callback saved it: two ModelCheckpoints each keep their own.
            "callback": view.owner,
            "monitor": view.monitor,
            "score": _float_or_none(view.scores.get(local)),
            "step": view.step,
            # Without a monitor `best_model_path` is only the latest save.
            "best": (local == view.best) if view.monitor else None,
            "last": local == view.last,
            # Carried so a later refresh (which replaces the row's meta, and
            # may find the path gone) keeps what the first write said.
            "written_during_run": True,
            "written_at": datetime.fromtimestamp(info.st_mtime, tz=timezone.utc).isoformat(),
        }
        if is_dir:
            meta.update(is_directory=True, n_files=n_files)
            if not complete:
                meta["size_partial"] = True
        meta = {k: v for k, v in meta.items() if v is not None}
        row = _CheckpointRow(
            name=os.path.basename(local.rstrip(os.sep)),
            owner=view.owner,
            size=size,
            step=view.step,
            meta=meta,
            reference=reference,
            signature=signature,
        )
        self._checkpoint_rows[local] = row
        run.log_artifact(
            row.name,
            path=local,
            kind="checkpoint",
            reference=reference,
            size_bytes=size if reference else None,
            step_index=row.step,
            meta=dict(meta),
            strict=self._strict,
        )

    def _refresh_checkpoints(self, run: Any, view: _CallbackView | None) -> None:
        """Re-send a reference row whose truth changed since it was written.

        The server keys a hashless path reference on (run, name, uri) and
        refreshes that row in place (``app/artifacts/service.py``), so this
        updates the row rather than adding one. ``view`` is None at finalize,
        where only deletions can still be learned."""
        for local, row in self._checkpoint_rows.items():
            if not row.reference or row.gone:
                continue
            meta = dict(row.meta)
            if view is not None and view.owner == row.owner and view.known:
                if view.monitor:
                    meta["best"] = local == view.best
                meta["last"] = local == view.last
                if not view.keeps(local):
                    meta["superseded"] = True
            if not os.path.lexists(local):
                meta["deleted"] = True
            if meta == row.meta:
                continue
            row.meta = meta
            row.gone = bool(meta.get("deleted"))
            run.log_artifact(
                row.name,
                path=local,
                kind="checkpoint",
                reference=True,
                allow_missing=True,
                size_bytes=row.size,
                step_index=row.step,
                meta=dict(meta),
                strict=self._strict,
            )

    # -- internals ----------------------------------------------------------------
    def _guarded(self, what: str, fn: Any, *args: Any, **kwargs: Any) -> Any:
        """Probe must never take down a training loop outside ``strict``."""
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            if self._strict:
                raise
            self._warn_once(
                what,
                f"probe: the Lightning logger's {what} failed ({type(exc).__name__}: "
                f"{exc}); training continues. Further {what} failures are silent.",
            )
            return None

    def _warn_once(self, key: str, message: str) -> None:
        if key in self._warned:
            return
        self._warned.add(key)
        safe_warn.warn(message, stacklevel=_user_stacklevel())


_ATTR = {"project": "_project", "experiment": "_experiment_name", "name": "_run_name"}


#: Packages a warning must not point into: the line it names should be the
#: user's own (`trainer.fit(...)`), not one in here or in Lightning's hooks.
_INTERNAL_PACKAGES = ("probe", "lightning", "pytorch_lightning", "lightning_fabric", "torch")


def _user_stacklevel() -> int:
    """The ``stacklevel`` (1 = the caller of this) of the first frame outside
    Probe, Lightning and torch; the outermost frame when every one is inside
    (a worker process, whose stack starts in multiprocessing)."""
    roots = tuple(
        os.path.dirname(os.path.abspath(module.__file__)) + os.sep
        for module in (sys.modules.get(name) for name in _INTERNAL_PACKAGES)
        if getattr(module, "__file__", None)
    )
    frame = sys._getframe(1)
    level = 1
    while frame.f_back is not None and os.path.abspath(frame.f_code.co_filename).startswith(roots):
        frame = frame.f_back
        level += 1
    return level


def _shared_run_message(label: str, why: str) -> str:
    # The server's metric insert is ON CONFLICT DO NOTHING (app/telemetry/store.py):
    # the first point a run gets at a step is the one it keeps.
    return (
        f"probe: this ProbeLogger writes to run {label}, the same run an earlier ProbeLogger "
        f"in this process used: {why} Where both Trainers log a metric at the same step, the "
        "server keeps the first point, so this Trainer's curve is lost there."
    )


class _CheckpointRow:
    """What the run's artifact row for one checkpoint path says now."""

    __slots__ = ("name", "owner", "size", "step", "meta", "reference", "signature", "gone")

    def __init__(self, *, name, owner, size, step, meta, reference, signature) -> None:
        self.name = name
        self.owner = owner
        self.size = size
        self.step = step
        self.meta = meta
        self.reference = reference
        self.signature = signature
        self.gone = False


class _CallbackView:
    """The checkpoint callback's state at one save, paths made absolute."""

    def __init__(self, callback: Any) -> None:
        step = getattr(callback, "_last_global_step_saved", None)
        self.step = step if isinstance(step, int) and step >= 0 else None
        self.monitor = getattr(callback, "monitor", None)
        self.save_top_k = getattr(callback, "save_top_k", None)
        self.best = _abspath(getattr(callback, "best_model_path", None))
        self.last = _abspath(getattr(callback, "last_model_path", None))
        scores = getattr(callback, "best_k_models", None)
        #: Only a ModelCheckpoint-shaped callback says what it keeps.
        self.known = isinstance(scores, Mapping)
        self.scores = {os.path.abspath(p): s for p, s in (scores or {}).items()} if self.known else {}
        # Two ModelCheckpoints (top-k by val_loss, every N steps) each keep
        # their own set; one must never mark the other's files superseded.
        self.owner = getattr(callback, "state_key", None) or type(callback).__name__

    def keeps(self, local: str) -> bool:
        if self.save_top_k == -1:
            # Keeps every save. Without a monitor `best_k_models` stays empty
            # and `best_model_path` is simply the latest, so neither says so.
            return True
        return local in self.scores or local in (self.best, self.last)

    def reported_paths(self) -> list[str]:
        return list(self.scores) + [p for p in (self.last, self.best) if p and p not in self.scores]


def _close_when_this_worker_exits(client: Any = None) -> None:
    """Close this process's run when it leaves as a multiprocessing worker.

    A forked worker (``ddp_fork``, ``ddp_notebook``) exits through
    ``os._exit``: no atexit hook runs, so the run it opened stayed ``running``
    until the reaper called it ``crashed``. ``multiprocessing`` runs its own
    finalizers in the worker's ``finally`` on every way out, success or
    exception, fork or spawn, which is where this goes. A spawned worker would
    also close at its atexit; the second close finds nothing open."""
    from multiprocessing import util

    util.Finalize(None, _close_at_worker_exit, args=(client,), exitpriority=100)


def _close_at_worker_exit(client: Any) -> None:
    # Runs inside the worker's `finally`, so an exception still in flight is
    # how the worker is ending: torch's worker wrapper turns a training error
    # into `sys.exit(1)`, and under ipykernel the sys.exit hook stands down.
    # A KeyboardInterrupt it swallows is not in flight here; the SIGINT
    # handler `_chain_worker_sigint` put in front noted it already.
    exc = sys.exc_info()[1]

    def close() -> None:
        try:
            if isinstance(exc, KeyboardInterrupt):
                fluent.note_exit("canceled")
            elif _is_lightning_sigterm(exc):
                # Under torchrun the worker's own `finalize("failed")` says so;
                # here that finalize runs in the parent, whose logger holds no
                # run, and a code-less SystemExit alone reads as success.
                fluent.note_exit("failed", exc)
            elif isinstance(exc, SystemExit):
                if exc.code not in (None, 0, False):
                    context = exc.__context__
                    fluent.note_exit("failed", context if isinstance(context, Exception) else None)
            elif isinstance(exc, Exception):
                fluent.note_exit("failed", exc)
            _cap_worker_close()
            fluent._finish_at_exit()
        except Exception:  # noqa: BLE001 -- a worker's exit must never raise from here
            log.debug("probe: closing the worker's run failed", exc_info=True)
        finally:
            if client is not None:
                try:
                    client.close()
                except Exception:  # noqa: BLE001
                    pass

    run_held(close, (signal.SIGTERM, signal.SIGINT), WORKER_HOLD_SECONDS)


def _cap_worker_close() -> None:
    cap_finish_timeout(WORKER_CLOSE_SECONDS)


def _failed_verdict(exc: BaseException | None, *, launcher_run: bool) -> str | None:
    """What ``finalize("failed")`` says about how the job ended. Ctrl-C is
    ``canceled``. On a launcher's run (``probe exec``) an ordinary error says
    nothing: the launcher closes the run from the real exit code -- an
    uncaught error still reaches the excepthook (exit 1), and one the script
    caught did not end the process, so noting it closed a run ``failed``
    whose process exited 0. Lightning's SIGTERM exits 0, so it is noted even
    there. Anything else is ``failed``."""
    if isinstance(exc, KeyboardInterrupt):
        return "canceled"
    if launcher_run and not _is_lightning_sigterm(exc):
        return None
    return "failed"


def _is_lightning_sigterm(exc: BaseException | None) -> bool:
    """Lightning's ``SIGTERMException``: the code-less SystemExit its fit loop
    raises after its SIGTERM handler ran. By name, for both packages."""
    return isinstance(exc, SystemExit) and any(
        cls.__name__ == "SIGTERMException" for cls in type(exc).__mro__
    )


#: The worker pid whose SIGINT is chained (once per process).
_SIGINT_CHAINED_PID: int | None = None


def _chain_worker_sigint() -> None:
    """Put a SIGINT handler in front of this worker's, noting how it ends.

    torch's worker wrapper swallows KeyboardInterrupt (``except
    KeyboardInterrupt: pass`` in ``torch/multiprocessing/spawn.py``), so the
    worker exits 0 and by its close nothing said Ctrl-C: the run closed
    ``completed``. Lightning's own Ctrl-C handling runs in the parent. So:

    * the parent is still there: a person pressed Ctrl-C (the terminal sends it
      to the whole group) -> ``canceled``;
    * the parent is gone: this is the death signal torch arms on every worker
      (``PR_SET_PDEATHSIG`` = SIGINT) -- the parent was killed (SIGTERM,
      SIGKILL, the OOM killer), which nobody here decided -> ``failed``, unless
      a Ctrl-C was noted first.

    Then the previous handler runs, so KeyboardInterrupt is raised exactly as
    before. Chained only over a Python-level handler (Python's default raises
    KeyboardInterrupt); SIG_IGN, SIG_DFL and one set outside Python are left
    alone. Acts only in the process that chained it: a process forked from
    this worker inherits the handler, not this ending."""
    global _SIGINT_CHAINED_PID
    pid = os.getpid()
    if _SIGINT_CHAINED_PID == pid or threading.current_thread() is not threading.main_thread():
        return
    try:
        previous = signal.getsignal(signal.SIGINT)
    except (ValueError, OSError):
        return
    if not callable(previous):
        return
    parent = os.getppid()
    noted = {"canceled": False}

    def on_sigint(signum: int, frame: Any) -> None:
        if os.getpid() == pid:
            try:
                if os.getppid() == parent:
                    noted["canceled"] = True
                    fluent.note_exit("canceled")
                elif not noted["canceled"]:
                    fluent.note_exit("failed")
            except Exception:  # noqa: BLE001 -- never stand between a signal and its handler
                pass
        previous(signum, frame)

    try:
        signal.signal(signal.SIGINT, on_sigint)
    except (ValueError, OSError):
        return
    _SIGINT_CHAINED_PID = pid


def _abspath(path: Any) -> str | None:
    return os.path.abspath(path) if isinstance(path, str) and path else None


def _float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value.item() if hasattr(value, "item") else value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None
