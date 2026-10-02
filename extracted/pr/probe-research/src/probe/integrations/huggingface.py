"""Hugging Face ``Trainer`` callback for Probe (plan (b), task T28).

    import probe.integrations.huggingface  # registers report_to="probe"

    args = TrainingArguments(output_dir="out", report_to="probe")
    Trainer(model=model, args=args, train_dataset=ds).train()

or, to choose where the run goes::

    from probe.integrations.huggingface import ProbeCallback

    Trainer(..., callbacks=[ProbeCallback(experiment="sst2", name="lr-3e-4")])

Use one or the other: ``report_to="probe"`` plus ``callbacks=[ProbeCallback()]``
puts two callbacks on one Trainer; the one given arguments logs, the other
stands down with a warning. ``report_to`` resolves
its names in ``transformers``' ``INTEGRATION_TO_CALLBACK`` when the Trainer is
built, so this module must be imported first; without it ``report_to="probe"``
raises ``ValueError`` (verified against transformers 5.17).

What it does, by Trainer hook, on the world-zero process only:

* ``on_train_begin`` -- opens the run (see "Which run" below) and merges the
  model's config, ``TrainingArguments.to_dict()`` (which already masks
  ``hub_token`` and every other ``*_token``) and a PEFT config into the run's
  config with ``run.update_config``, TrainingArguments winning as they do
  for W&B.
* ``on_log`` -- ``run.log(logs, step=state.global_step)`` with the keys
  sectioned the way W&B's callback sections them: ``eval_loss`` ->
  ``eval/loss``, ``test_*`` -> ``test/*``, everything else ``train/*``.
  ``evaluate()`` reaches ``on_log`` too, so ``on_evaluate`` logs nothing
  (every eval point would land twice). ``trainer.evaluate()`` without a
  ``train()`` opens the run from here. The server keeps the first point per
  key and step, so a key logged again at a step with a new value (an
  ``evaluate()`` after ``train()``, at the last step: the best model, a second
  eval set) is sent with the label ``repeat=1``, ``2``, ...; the same value
  again is not re-sent.
* ``on_predict`` -- ``predict()`` logs nothing through ``on_log``; its
  metrics are logged at the current step (``test/*``).
* ``on_save`` -- the ``checkpoint-<step>`` folder the Trainer just wrote
  becomes a ``checkpoint`` artifact on the run: a path REFERENCE (its bytes
  are not copied through the API), sized by summing the folder once, with
  ``meta.step``. With ``metric_for_best_model`` set, ``meta.monitor`` /
  ``meta.score`` and ``meta.best``; ``best`` then follows the Trainer's
  ``best_model_checkpoint``, and a folder ``save_total_limit`` removed is
  marked ``deleted`` (the row is refreshed in place).
* ``on_step_end`` -- ``run.progress()``, so plan 2.8's stall detector sees the
  job advancing.
* never finishes the run: the process's exit (``probe.init``'s exit hooks) or
  your ``probe.finish()`` does.

How the job ended. An exception out of ``train()`` and Ctrl-C reach the
process's exit hooks (``failed`` / ``canceled``). These endings do not, and this
callback records them:

* a ``train()`` whose exception the script CAUGHT (it never reached
  ``on_train_end``): ``failed``, or ``canceled`` if a Ctrl-C stopped it. A
  run this callback opened gets it when the next ProbeCallback closes that run
  (a sweep loop); the run bound at exit gets it when the script ran to its end
  with no exit code. Never under a launcher (``probe exec``), which closes its
  run from the real exit code. A run the script opened and closes itself
  (``probe.init()`` per iteration, ``with probe.init()``) takes the status the
  script closes it with;
* a stop by ``enable_jit_checkpoint``'s SIGTERM handler (preemption): training
  returns normally and the process exits 0, so ``on_train_end`` sees the
  SIGTERM, records ``failed``, and records the JIT checkpoint, which reaches no
  ``on_save``. Inside ``with probe.init() as run:`` the block's own close,
  which sees no exception, still says ``completed``;
* a hyperparameter trial transformers pruned (``on_train_end`` before
  ``optuna.TrialPruned``, with training short of ``max_steps``):
  ``canceled``. A ``TrialPruned`` a callback of yours raises reaches no
  ``on_train_end`` and reads as a caught failure;
* a run opened in a multiprocessing WORKER (accelerate's
  ``notebook_launcher``, a ``Process`` per trial): a forked worker leaves
  through ``os._exit``, which runs no exit hook, so the run is closed from
  multiprocessing's worker-exit finalizers instead, from how the worker is
  ending (an error, Ctrl-C, or the verdicts above), bounded to fit torch's
  30 s grace before SIGKILL, with SIGTERM / SIGINT held during that close.

To tell Ctrl-C and SIGTERM apart, a handler is chained IN FRONT of the SIGINT
/ SIGTERM handlers it finds during ``train()``: it notes the signal, puts the
previous handler back and calls it, so nothing changes for that handler (a
SIGINT that arrives after the parent process died is torch's death signal to
its workers, not a person: ``failed``). It is
chained only over a handler set from Python (never over the default SIGTERM,
which kills the process with no hook at all -- plans 2.2 / 2.8 catch that) and
taken off at ``on_train_end``; after a ``train()`` that raised it stays until
the next signal, the next trial's close, or the next ``train()``.

Which run: a run the script opened itself with ``probe.init()`` is adopted
(never finished here); otherwise ``probe.init(...)`` opens one, named
``name=``, else ``run_name``; a hyperparameter trial is named by
``hyperparameter_search(hp_name=...)``, else ``<name>-trial-<n>``. A run an
EARLIER ProbeCallback opened is not adopted: each Trainer is its own trial (a
sweep loop), so that run is closed and a new one opened, and so is each
``hyperparameter_search`` trial and the ``train()`` after the search. A
``train()`` after the callback's run was closed (``probe.finish()``) picks up
the run open now, or opens one. Under a launcher that exported
``PROBE_RUN_ID`` every callback writes the launcher's run. A second callback
writing into a run it shares (the script's, or the launcher's) is warned, as
is a second ``train()`` that restarts below steps this run already has: the
server keeps the first point it gets at a step, so the later curve is lost
where the two overlap. A ``hyperparameter_search`` trial saves its checkpoints under
``output_dir/run-<trial>/``, which is not looked in: trial checkpoints are
not recorded.

Other ranks (``torchrun``, ``accelerate launch``, DeepSpeed) open no run and
write NOTHING to it, but each holds a writer lease on it: plan 2.8 sees a lost
node only if every rank does. In ``on_train_begin`` rank 0 PUBLISHES ``(run
id, epoch)`` in the process group's store and never waits; each other rank
takes ``PROBE_RUN_ID`` when a launcher exported it, else reads rank 0's key,
waiting at most :data:`RUN_ID_WAIT_SECONDS`, and joins that run as a
LEASE-ONLY writer (``_rank_lease``): it beats its own ``rank`` lease -- no
metric, no capture, no status -- and releases it when the process exits,
``failed`` on an uncaught exception. No collective, so a callback on some
ranks only (``callbacks=[ProbeCallback()] if trainer.is_world_process_zero()
else []``) costs the others their lease, never the job a hang; a rank that
waited in vain says so once and waits no more. A SIGTERM that meets Python's
default handler (no ``enable_jit_checkpoint``) kills the rank with no hook at
all, as it does rank 0; its lease then stops beating, which is how the server
sees it lost. A server without per-writer leases gets nothing from it.

Not re-exported from ``probe.integrations`` (which imports miles eagerly), and
nothing under ``probe`` imports this module: ``import probe`` must never load
transformers or torch.
"""

from __future__ import annotations

import atexit
import json
import logging
import math
import multiprocessing
import os
import signal
import sys
import threading
import time
import weakref
from datetime import datetime, timedelta, timezone
from typing import Any

try:
    from transformers.trainer_callback import TrainerCallback
except ImportError as _missing:
    # `name` carries the missing module, as a plain ModuleNotFoundError would:
    # callers (and test_import_every_module) tell an absent optional extra
    # from a broken import by it.
    raise ImportError(
        "probe.integrations.huggingface needs Hugging Face transformers, which is not installed. "
        "Install it with Probe's extra: pip install 'probe-research[huggingface]'",
        name=getattr(_missing, "name", None) or "transformers",
    ) from _missing

import probe
from probe.sdk import fluent, hashing, safe_warn

from . import _rank_lease
from ._worker_exit import (
    WORKER_CLOSE_SECONDS,
    WORKER_HOLD_SECONDS,
    cap_finish_timeout,
    run_held,
)

log = logging.getLogger(__name__)

#: The folder name the Trainer saves each checkpoint under
#: (``transformers.trainer_utils.PREFIX_CHECKPOINT_DIR``).
CHECKPOINT_PREFIX = "checkpoint"

#: How long closing the previous trial's run may spend delivering before the
#: rest is deferred to the outbox (plan (j)'s bound; letting go of its client
#: may add a few seconds more).
PREVIOUS_RUN_FLUSH_SECONDS = 10.0

#: Runs a ProbeCallback opened with ``probe.init()``: run id -> the pid that
#: opened it. A later ProbeCallback in that process closes such a run instead
#: of adopting it (two Trainers in one script are two trials).
_CALLBACK_RUNS: dict[str, int] = {}

#: Runs a ProbeCallback joined through ``PROBE_RUN_ID``: the launcher closes them.
_LAUNCHER_RUNS: set[str] = set()

#: Runs a ProbeCallback wrote to without opening them (the script's own, a
#: launcher's): the next ProbeCallback there is told it shares the run.
_ADOPTED: set[str] = set()

#: Runs whose ``train()`` began and has not reached ``on_train_end`` -> that
#: train()'s TrainerState (weakly): a second ProbeCallback on the SAME Trainer
#: sees its own state there.
_UNFINISHED: dict[str, weakref.ref] = {}

#: Signals the chained handlers saw during the current ``train()``, plus
#: :data:`_PARENT_DIED` when a SIGINT came with the parent process gone.
_SIGNALS_SEEN: set[object] = set()

#: A SIGINT whose sender was the parent's death, not a person: torch arms every
#: worker it starts with ``PR_SET_PDEATHSIG`` = SIGINT.
_PARENT_DIED = "parent_died"

#: Runs a ``train()`` reached ``on_train_end`` on, but did not finish: run id ->
#: the status to close with. transformers prunes a hyperparameter trial by
#: calling ``on_train_end`` and then raising ``optuna.TrialPruned``.
_ENDED_AS: dict[str, str] = {}

_ADOPT_IGNORES = ("project", "experiment", "name")

#: How long a rank above 0 waits at ``train()`` start for the run id rank 0
#: publishes (rank 0 itself never waits).
RUN_ID_WAIT_SECONDS = 10.0

#: This process's ``train()`` hand-offs so far: the store key's sequence
#: number, the same on every rank that runs the same script.
_handoffs = 0

#: Set once a rank waited in vain: it waits no more in this process (a
#: hyperparameter search would pay the wait at every trial).
_handoff_given_up = False


class ProbeCallback(TrainerCallback):
    """Log a Hugging Face Trainer run to Probe. See the module docstring.

    ``project`` / ``experiment`` / ``name`` and any other keyword go to
    ``probe.init()`` (``question=``, ``tags=``, ``config=``, ``client=``, ...).
    ``report_to="probe"`` builds one with no arguments: the run is then named
    after ``run_name`` and filed by ``PROBE_PROJECT`` (or floats until the
    daemon files it); open the run yourself with ``probe.init(...)`` to choose
    more, and the callback adopts it. ``log_model=False`` records no
    checkpoints. ``strict=True`` lets Probe errors raise instead of warning once.
    """

    def __init__(
        self,
        *,
        project: str | None = None,
        experiment: str | None = None,
        name: str | None = None,
        log_model: bool = True,
        strict: bool = False,
        **init_kwargs: Any,
    ) -> None:
        self._project = project
        self._experiment_name = experiment
        self._run_name = name
        self._log_model = log_model
        self._strict = strict
        self._init_kwargs = init_kwargs
        self._run: Any = None
        self._rank_lease: _rank_lease.RankLease | None = None  # every other rank
        self._owns_run = False  # opened here (not the script's, not a launcher's)
        self._disabled = False  # init failed: a no-op callback from here on
        self._trained = False  # a train() on this callback has begun
        self._last_step: int | None = None  # the highest step logged to this run
        self._train_began_at = 0.0  # wall time the current train() began
        self._searching = False  # the last train() was a hyperparameter_search trial
        self._trials = 0  # hyperparameter_search trials this callback has begun
        #: The ProbeCallbacks on this Trainer (on_init_end), and whether this
        #: one stands down for another (decided at its first hook).
        self._peers: list[ProbeCallback] | None = None
        self._stood_down: bool | None = None
        #: ((run id, step), {key: [values logged at it]}): a later value of a
        #: key already logged at this step gets a `repeat` label (see _log).
        self._step_seen: tuple[tuple[str, int] | None, dict[str, list[Any]]] = (None, {})
        #: One entry per checkpoint folder: what its row on the run says now.
        self._checkpoint_rows: dict[str, dict[str, Any]] = {}
        self._warned: set[str] = set()

    # -- Trainer hooks ------------------------------------------------------------
    def on_init_end(self, args, state, control, **kwargs):
        # Every callback of one Trainer is handed the same init-time state:
        # that is how two ProbeCallbacks on one Trainer find each other.
        peers = state.__dict__.setdefault("_probe_callbacks", [])
        if self not in peers:
            peers.append(self)
        self._peers = peers

    def on_train_begin(self, args, state, control, model=None, **kwargs):
        if state.is_world_process_zero and not self._disabled and not self._stands_down():
            self._begin_on_world_zero(args, state, model)
        # Every rank, after world zero has its run for this train().
        self._share_run_identity(state)

    def _begin_on_world_zero(self, args: Any, state: Any, model: Any) -> None:
        if self._run is None and self._same_trainer_has_one(state):
            return
        searching, self._searching = self._searching, bool(state.is_hyper_param_search)
        if self._searching:
            self._trials += 1
        if self._run is not None and getattr(self._run, "_closed_status", None) is not None:
            # Closed since the last train() (probe.finish(), a newer
            # ProbeCallback's trial): this train() goes where a new one would.
            self._forget_run()
        elif (searching or self._searching) and self._owns_run and self._run is not None:
            # Each hyperparameter_search trial calls train() on this same
            # callback, and so does the final train() with the best values:
            # close the previous one's run, open one per train().
            self._close_previous(self._run)
            self._forget_run()
        elif self._trained and self._run is not None and self._last_step is not None:
            if state.global_step < self._last_step:
                self._warn_once(
                    "retrain",
                    _shared_run_message(
                        self._label(self._run),
                        f"train() started again at step {state.global_step}, below step "
                        f"{self._last_step} this run already has. Call probe.finish() before "
                        "it, or give the new Trainer its own ProbeCallback, to give it a run "
                        "of its own.",
                        "this train()",
                    ),
                )
        run = self._ensure_run(args, state, model)
        self._trained = True
        if run is None:
            return
        self._train_began_at = time.time()
        self._merge_config(run, args, model)
        _UNFINISHED[run.id] = weakref.ref(state)
        _note_unfinished_at_exit.register()
        _SIGNALS_SEEN.clear()
        _chain_signal_notes()

    def on_train_end(self, args, state, control, **kwargs):
        if not state.is_world_process_zero or self._run is None or self._stands_down():
            return
        run = self._run
        _UNFINISHED.pop(run.id, None)
        max_steps = getattr(state, "max_steps", None)
        if signal.SIGTERM in _SIGNALS_SEEN and max_steps and state.global_step < max_steps:
            # A SIGTERM handler (enable_jit_checkpoint's) stopped training and
            # train() returned normally: the job was preempted, and exits 0.
            self._guarded("exit", fluent.note_exit, "failed")
        elif (
            self._owns_run
            and state.is_hyper_param_search
            and max_steps
            and state.global_step < max_steps
            and not control.should_training_stop
        ):
            # transformers' pruning (Trainer._report_to_hp_search): on_train_end
            # here, then optuna.TrialPruned. Stopped by decision, like Ctrl-C.
            _ENDED_AS[run.id] = "canceled"
        if self._log_model:
            if getattr(args, "enable_jit_checkpoint", False):
                # The JIT checkpoint is saved outside the Trainer's save path:
                # no on_save reaches this callback for it.
                self._guarded("checkpoint", self._record_unreported, run, args, state)
            if self._checkpoint_rows:
                self._guarded("checkpoint", self._refresh_checkpoints, run, args, state)
        _unchain_signal_notes()

    def on_log(self, args, state, control, logs=None, model=None, **kwargs):
        if not state.is_world_process_zero or not logs or self._stands_down():
            return
        run = self._ensure_run(args, state, model, merge=True)
        if run is None:
            return
        self._log(run, rewrite_logs(logs), state.global_step)

    def on_predict(self, args, state, control, metrics=None, **kwargs):
        if not state.is_world_process_zero or not metrics or self._stands_down():
            return
        run = self._ensure_run(args, state, kwargs.get("model"), merge=True)
        if run is None:
            return
        self._log(run, rewrite_logs(metrics), state.global_step)

    def on_save(self, args, state, control, **kwargs):
        if not state.is_world_process_zero or not self._log_model or self._stands_down():
            return
        run = self._run_for_write()
        if run is None:
            return
        self._guarded("checkpoint", self._record_checkpoint, run, args, state)

    def on_step_end(self, args, state, control, **kwargs):
        if not state.is_world_process_zero or self._run is None:
            return
        progress = getattr(self._run, "progress", None)
        if callable(progress):
            self._guarded("progress", progress)

    # -- the run ------------------------------------------------------------------
    def _ensure_run(self, args: Any, state: Any, model: Any, *, merge: bool = False) -> Any:
        """The run on the world-zero process (opened on first use), else None."""
        if self._run is None and not self._disabled:
            self._open_run(args, state)
            if merge and self._run is not None:
                self._merge_config(self._run, args, model)
        return self._run_for_write()

    def _run_for_write(self) -> Any:
        """The run, saying once when it is already closed: a newer
        ProbeCallback closed this one's trial when its own Trainer started, or
        the script finished the run it had adopted."""
        run = self._run
        closed = getattr(run, "_closed_status", None) if run is not None else None
        if closed is not None:
            self._warn_once(
                "closed",
                f"probe: this ProbeCallback is still writing to run {self._label(run)}, which is "
                f"already closed ({closed}): a newer ProbeCallback closed it when its own "
                "Trainer started (one run per Trainer), or the script finished it. What it "
                "logs now lands on that finished run. Give each Trainer its own ProbeCallback.",
            )
        return run

    def _stands_down(self, *, warn: bool = True) -> bool:
        """Two ProbeCallbacks on one Trainer (``report_to="probe"`` plus
        ``callbacks=[ProbeCallback(...)]``): one logs. The one given arguments
        wins; between two alike, the first. The same answer on every rank."""
        if self._stood_down is None:
            peers = self._peers or [self]
            winner = next((p for p in peers if p._configured()), peers[0])
            self._stood_down = winner is not self
            if self._stood_down and warn:
                self._warn_once(
                    "duplicate",
                    "probe: this Trainer has two ProbeCallbacks (report_to='probe' and "
                    "callbacks=[ProbeCallback(...)]); the one given arguments logs, this one "
                    "logs nothing. Use one or the other.",
                )
        return self._stood_down

    def _configured(self) -> bool:
        return (
            any(v is not None for v in (self._project, self._experiment_name, self._run_name))
            or bool(self._init_kwargs)
            or not self._log_model
            or self._strict
        )

    def _same_trainer_has_one(self, state: Any) -> bool:
        """Another ProbeCallback on this very Trainer already opened the run
        for this train(), one that did not meet this one at init (added with
        ``trainer.add_callback`` later): this one stands down rather than
        closing that run as a failed trial."""
        active = probe.active_run()
        ref = _UNFINISHED.get(active.id) if active is not None else None
        if ref is None or ref() is not state:
            return False
        self._disabled = True
        self._warn_once(
            "duplicate",
            "probe: this Trainer has two ProbeCallbacks (report_to='probe' and "
            "callbacks=[ProbeCallback(...)]); the second logs nothing. Use one or the other.",
        )
        return True

    def _forget_run(self) -> None:
        self._run, self._owns_run, self._last_step = None, False, None
        self._checkpoint_rows.clear()

    def _share_run_identity(self, state: Any) -> None:
        """Once per ``train()``, on every rank of a process group: rank 0
        PUBLISHES ``(run id, epoch)`` in the group's store, and every other
        rank takes a lease-only writer's lease on that run
        (``_rank_lease.hold``).

        Never a collective (review of #2091): loggers attached on the main
        process only are a common shape, and rank 0 waiting in a broadcast the
        others never join hung the job until the process group's timeout.
        Rank 0 only sets a key; a rank above 0 takes ``PROBE_RUN_ID`` when a
        launcher exported it, else waits at most :data:`RUN_ID_WAIT_SECONDS`
        for the key, then trains on without a lease (one warning)."""
        global _handoffs
        try:
            import torch.distributed as dist
        except ImportError:  # pragma: no cover - transformers' Trainer brings torch
            return
        try:
            if not (dist.is_available() and dist.is_initialized()) or dist.get_world_size() < 2:
                return
            rank = dist.get_rank()
        except Exception:  # noqa: BLE001 -- no usable group: nothing to share
            return
        if self._stands_down(warn=state.is_world_process_zero):
            return
        _handoffs += 1
        key = f"probe/huggingface/run/{_handoffs}"
        if rank == 0:
            self._publish_run(dist, key)
            return
        received = _launcher_run() or self._receive_run(dist, key, rank)
        if received is None:
            return
        run_id, write_epoch = received
        client = self._init_kwargs.get("client")
        try:
            self._rank_lease = _rank_lease.hold(run_id, write_epoch, rank=rank, client=client)
        except Exception as exc:
            if self._strict:
                raise
            self._warn_once(
                "rank_lease",
                f"probe: rank {rank} could not take its writer lease on run {run_id} "
                f"({type(exc).__name__}: {exc}); training continues, but a lost node "
                "there will not be seen.",
            )

    def _publish_run(self, dist: Any, key: str) -> None:
        """Rank 0: the open run's id and epoch under ``key`` (``null`` when it
        has none, so no rank waits for it). One set, never a wait; a store
        that fails costs the other ranks their lease, never this rank its
        training."""
        run = self._run
        if run is not None and getattr(run, "_closed_status", None) is not None:
            run = None
        value = (
            {"run_id": str(run.id), "write_epoch": getattr(run, "write_epoch", None)}
            if run is not None
            else None
        )
        try:
            dist.distributed_c10d._get_default_store().set(key, json.dumps(value))
        except Exception:  # noqa: BLE001
            log.debug("probe: rank 0 could not publish its run id", exc_info=True)

    def _receive_run(self, dist: Any, key: str, rank: int) -> tuple[str, int | None] | None:
        """A rank above 0: rank 0's ``(run id, epoch)`` from the store, waiting
        at most :data:`RUN_ID_WAIT_SECONDS`. None when rank 0 has no run, and
        -- with one warning, after which this process waits no more -- when
        nothing came in time (rank 0 has no ProbeCallback, or no store)."""
        global _handoff_given_up
        if _handoff_given_up:
            return None
        try:
            store = dist.distributed_c10d._get_default_store()
            store.wait([key], timedelta(seconds=RUN_ID_WAIT_SECONDS))
            value = json.loads(store.get(key))
        except Exception as exc:  # noqa: BLE001 -- a missing lease never stops training
            _handoff_given_up = True
            self._warn_once(
                "handoff",
                f"probe: rank {rank} got no run id from rank 0 within {RUN_ID_WAIT_SECONDS:g} s "
                f"({type(exc).__name__}); it holds no writer lease on the run and training "
                "goes on. Give rank 0 a ProbeCallback too: one on some ranks only leaves the "
                "others without their lease.",
            )
            return None
        if not isinstance(value, dict) or not value.get("run_id"):
            log.debug("probe: rank %s: rank 0 shared no run id", rank)
            return None
        return str(value["run_id"]), value.get("write_epoch")

    def _open_run(self, args: Any, state: Any) -> None:
        try:
            active = probe.active_run()
            if active is not None and active.id in _CALLBACK_RUNS:
                if _CALLBACK_RUNS[active.id] == os.getpid():
                    self._close_previous(active)
                active = None  # a previous trial's run: never adopted
            if active is not None:
                self._adopt(active)
            else:
                self._run = self._init_run(args, state)
        except Exception as exc:
            if self._strict:
                raise
            self._disabled = True
            self._warn_once(
                "init",
                "probe: the Hugging Face callback could not open a run and is logging nothing "
                f"for this job ({type(exc).__name__}: {exc}). Training continues.",
            )

    def _init_run(self, args: Any, state: Any) -> Any:
        name = self._run_name
        if getattr(state, "is_hyper_param_search", False):
            # One run per trial, told apart: hyperparameter_search's hp_name=
            # names a trial (state.trial_name); without it, the trial's number.
            base = name or _args_run_name(args)
            number = max(self._trials - 1, 0)
            trial = getattr(state, "trial_name", None)
            name = trial or (f"{base}-trial-{number}" if base else f"trial-{number}")
        elif name is None:
            name = _args_run_name(args)
        kwargs = {
            key: value
            for key, value in (
                ("project", self._project),
                ("experiment", self._experiment_name),
                ("name", name),
            )
            if value is not None
        }
        kwargs.update(self._init_kwargs)
        launcher_run = os.environ.get("PROBE_RUN_ID", "").strip()
        if launcher_run:
            # probe.init() refuses identity kwargs next to PROBE_RUN_ID (the
            # launcher already chose the run). Join the launcher's run instead.
            dropped = sorted(k for k in fluent._IDENTITY_KWARGS if kwargs.pop(k, None) is not None)
            explicit = [k for k in dropped if k != "name" or self._run_name is not None]
            if explicit:
                self._warn_once(
                    "launcher",
                    f"probe: PROBE_RUN_ID={launcher_run} is set (a launcher such as `probe exec` "
                    f"opened this job's run), so ProbeCallback's {', '.join(explicit)} were not "
                    "applied: the callback writes to that run.",
                )
        run = probe.init(**kwargs)
        if launcher_run:
            _LAUNCHER_RUNS.add(run.id)
            _ADOPTED.add(run.id)
        else:
            _CALLBACK_RUNS[run.id] = os.getpid()
            self._owns_run = True
            if multiprocessing.parent_process() is not None:
                _close_when_this_worker_exits(run.id)
        return run

    def _adopt(self, active: Any) -> None:
        """Write to the run already open in this process; never finish it."""
        self._run = active
        # A new Trainer is starting on this run, so the way the previous one
        # ended (a failure the script caught) did not end the process.
        _UNFINISHED.pop(active.id, None)
        fluent._forget_noted_exit(active)
        label = self._label(active)
        if active.id == os.environ.get("PROBE_RUN_ID", "").strip():
            # The launcher's run, joined by the script's own probe.init()
            # under `probe exec`: the launcher closes it, from the exit code.
            _LAUNCHER_RUNS.add(active.id)
        if active.id in _ADOPTED:
            why = (
                "PROBE_RUN_ID (a launcher such as `probe exec`) chose one run for the whole "
                "process. Run each trial as its own process to give each its own run."
                if active.id in _LAUNCHER_RUNS
                else "the script opened it with probe.init(), and a ProbeCallback writes to the "
                "run the script has open. Call probe.finish() before each new Trainer to give "
                "it a run of its own."
            )
            self._warn_once("shared", _shared_run_message(label, why))
        _ADOPTED.add(active.id)
        if active.id not in _LAUNCHER_RUNS:
            ignored = [k for k in _ADOPT_IGNORES if getattr(self, _ATTR[k]) is not None]
            ignored += sorted(
                k
                for k, v in self._init_kwargs.items()
                if v is not None and k not in ("client", "config")
            )
            if ignored:
                self._warn_once(
                    "adopt",
                    f"probe: ProbeCallback adopted run {label}, which this script opened with "
                    f"probe.init(), so its {', '.join(ignored)} were not applied (an open run is "
                    "written to, not re-created). Pass them to probe.init(), or call "
                    "probe.finish() before the Trainer starts to give it a run of its own.",
                )
        config = self._init_kwargs.get("config")
        if config is not None:
            self._guarded("config", active.update_config, config, strict=self._strict_arg)

    def _close_previous(self, run: Any) -> None:
        """Close the run an earlier trial opened, with how that trial ended,
        and a bounded flush: what does not go out in time stays queued."""
        _CALLBACK_RUNS.pop(run.id, None)
        noted = getattr(run, "_noted_exit", None)
        ended_as = _ENDED_AS.pop(run.id, None)
        if run.id in _UNFINISHED:
            # Its train() never reached on_train_end: the sweep caught its error.
            _UNFINISHED.pop(run.id, None)
            status = _unfinished_verdict()
            _unchain_signal_notes()  # still in front since that train() raised
        elif ended_as is not None:
            status = ended_as
        elif noted:
            status = noted[0]
        else:
            status = "completed"
        try:
            if probe.active_run() is run:
                fluent.finish(status, flush_timeout=PREVIOUS_RUN_FLUSH_SECONDS)
            else:
                run.finish(status, flush_timeout=PREVIOUS_RUN_FLUSH_SECONDS)
        except Exception as exc:
            if self._strict:
                raise
            self._warn_once(
                "finish_previous",
                f"probe: the run an earlier ProbeCallback opened ({run.id}) did not close "
                f"cleanly ({type(exc).__name__}: {exc}); this Trainer opens its own run anyway.",
            )

    def _merge_config(self, run: Any, args: Any, model: Any) -> None:
        self._guarded("config", self._update_config, run, args, model)

    def _update_config(self, run: Any, args: Any, model: Any) -> None:
        """Model config, then a PEFT config, then TrainingArguments (the
        order W&B's callback merges them in, TrainingArguments winning).
        ``to_dict()`` masks every ``*_token`` argument (``hub_token``)."""
        combined: dict[str, Any] = {}
        config = getattr(model, "config", None) if model is not None else None
        if config is not None:
            combined.update(config if isinstance(config, dict) else config.to_dict())
        peft = getattr(model, "peft_config", None) if model is not None else None
        if peft is not None:
            combined["peft_config"] = peft
        combined.update(args.to_dict())
        run.update_config(combined, allow_val_change=True, strict=self._strict_arg)

    # -- metrics ------------------------------------------------------------------
    def _log(self, run: Any, metrics: dict[str, Any], step: int) -> None:
        """``run.log`` at ``step``. The server keeps the FIRST point it gets for
        a key at a step, and ``evaluate()`` after ``train()`` (the best model
        reloaded, a second eval set) logs ``eval/*`` again at the last step. So
        a key already logged at this step goes again only with a different
        value, labelled ``repeat=n`` (labels are part of a point's identity,
        not the series'); the same value again (``train/epoch`` beside each
        eval) is not re-sent: the server would drop it anyway."""
        where, seen = self._step_seen
        if where != (run.id, step):
            seen = {}
            self._step_seen = ((run.id, step), seen)
        groups: dict[int, dict[str, Any]] = {}
        for key, value in metrics.items():
            earlier = seen.setdefault(key, [])
            if any(_same_value(value, e) for e in earlier):
                continue
            groups.setdefault(len(earlier), {})[key] = value
            earlier.append(value)
        for repeat, values in sorted(groups.items()):
            labels = {"repeat": repeat} if repeat else None
            result = self._guarded(
                "log", run.log, values, step=step, labels=labels, strict=self._strict_arg
            )
            if result is not _FAILED and (self._last_step is None or step > self._last_step):
                self._last_step = step

    # -- checkpoints ----------------------------------------------------------------
    def _record_checkpoint(self, run: Any, args: Any, state: Any) -> None:
        """Record the ``checkpoint-<step>`` folder this save wrote, then
        refresh the rows of earlier ones."""
        step = state.global_step
        local = os.path.abspath(os.path.join(args.output_dir, f"{CHECKPOINT_PREFIX}-{step}"))
        if os.path.isdir(local):
            self._record_folder(run, args, state, local, step)
        else:
            # Saved somewhere else (a hyperparameter-search trial's own
            # folder), or not saved by this process.
            log.debug("probe: no checkpoint folder at %s", local)
        self._refresh_checkpoints(run, args, state)

    def _record_unreported(self, run: Any, args: Any, state: Any) -> None:
        """Record the JIT checkpoint, which no ``on_save`` reports. It is
        saved at the step the SIGTERM is acted on: the last one, or the one
        before it when training stopped at the start of a step."""
        for step in (state.global_step - 1, state.global_step):
            local = os.path.abspath(os.path.join(args.output_dir, f"{CHECKPOINT_PREFIX}-{step}"))
            if step < 0 or local in self._checkpoint_rows:
                continue
            try:
                if not os.path.isdir(local) or os.stat(local).st_mtime < self._train_began_at:
                    continue  # absent, or a folder an earlier job left behind
            except OSError:
                continue
            self._record_folder(run, args, state, local, step)

    def _record_folder(self, run: Any, args: Any, state: Any, local: str, step: int) -> None:
        size, n_files, complete = hashing.folder_size(local)  # the one walk per save
        monitor = getattr(args, "metric_for_best_model", None)
        meta: dict[str, Any] = {
            "original_filename": os.path.basename(local),
            "step": step,
            "epoch": state.epoch if step == state.global_step else None,
            "is_directory": True,
            "n_files": n_files,
            "written_during_run": True,
            "written_at": datetime.now(timezone.utc).isoformat(),
        }
        if not complete:
            meta["size_partial"] = True
        if monitor:
            meta["monitor"] = _metric_key(monitor)
            meta["score"] = _score_at(state, _metric_key(monitor), step)
            meta["best"] = local == _abspath(getattr(state, "best_model_checkpoint", None))
        meta = {k: v for k, v in meta.items() if v is not None}
        self._checkpoint_rows[local] = {
            "name": os.path.basename(local),
            "size": size,
            "step": step,
            "meta": meta,
        }
        run.log_artifact(
            os.path.basename(local),
            path=local,
            kind="checkpoint",
            reference=True,
            size_bytes=size,
            step_index=step,
            meta=dict(meta),
            strict=self._strict_arg,
        )

    def _refresh_checkpoints(self, run: Any, args: Any, state: Any) -> None:
        """Re-send a row whose truth changed since it was written: ``best``
        moved, or ``save_total_limit`` deleted the folder. The server keys a
        hashless path reference on (run, name, uri) and refreshes that row in
        place (``app/artifacts/service.py``)."""
        best = _abspath(getattr(state, "best_model_checkpoint", None))
        monitored = bool(getattr(args, "metric_for_best_model", None))
        for local, row in self._checkpoint_rows.items():
            if row.get("gone"):
                continue
            meta = dict(row["meta"])
            if monitored:
                meta["best"] = local == best
            if not os.path.lexists(local):
                meta["deleted"] = True
            if meta == row["meta"]:
                continue
            row["meta"] = meta
            row["gone"] = bool(meta.get("deleted"))
            run.log_artifact(
                row["name"],
                path=local,
                kind="checkpoint",
                reference=True,
                allow_missing=True,
                size_bytes=row["size"],
                step_index=row["step"],
                meta=dict(meta),
                strict=self._strict_arg,
            )

    # -- pickling (ray's hyperparameter_search ships the Trainer to workers) ------
    def __getstate__(self) -> dict[str, Any]:
        state = self.__dict__.copy()
        state["_run"] = None  # a live handle holds a client and threads
        state["_rank_lease"] = None  # so does a rank's lease; each process takes its own
        state["_owns_run"] = False
        state["_checkpoint_rows"] = {}
        state["_peers"] = None  # the other callbacks of a Trainer this copy is not on
        state["_step_seen"] = (None, {})
        if state["_init_kwargs"].get("client") is not None:
            # A Client holds the token: never into a pickle, wherever it goes.
            state["_init_kwargs"] = {
                k: v for k, v in state["_init_kwargs"].items() if k != "client"
            }
            self._warn_once(
                "pickle_client",
                "probe: a ProbeCallback with client= was pickled; the copy builds its own Client "
                "from the environment (PROBE_TOKEN / the stored login), not the one you passed.",
            )
        return state

    # -- internals ----------------------------------------------------------------
    @property
    def _strict_arg(self) -> bool | None:
        # None: the client's own default, which strict=False would override.
        return True if self._strict else None

    @staticmethod
    def _label(run: Any) -> str:
        return getattr(run, "slug", None) or run.id

    def _guarded(self, what: str, fn: Any, *args: Any, **kwargs: Any) -> Any:
        """Probe must never take down a training loop outside ``strict``."""
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            if self._strict:
                raise
            self._warn_once(
                what,
                f"probe: the Hugging Face callback's {what} failed ({type(exc).__name__}: "
                f"{exc}); training continues. Further {what} failures are silent.",
            )
            return _FAILED

    def _warn_once(self, key: str, message: str) -> None:
        if key in self._warned:
            return
        self._warned.add(key)
        safe_warn.warn(message, stacklevel=_user_stacklevel())


_FAILED = object()

_ATTR = {"project": "_project", "experiment": "_experiment_name", "name": "_run_name"}


def _launcher_run() -> tuple[str, int | None] | None:
    """``PROBE_RUN_ID`` (with ``PROBE_RUN_EPOCH``): a launcher (``probe exec``)
    named this job's run on every rank, and rank 0 writes to it too."""
    run_id = os.environ.get("PROBE_RUN_ID", "").strip()
    if not run_id:
        return None
    raw = os.environ.get("PROBE_RUN_EPOCH", "").strip()
    try:
        return run_id, int(raw) if raw else None
    except ValueError:
        return run_id, None


def rewrite_logs(logs: dict[str, Any]) -> dict[str, Any]:
    """Section the Trainer's log keys as W&B's callback does (vendored from
    ``transformers.integrations.integration_utils.rewrite_logs``):
    ``eval_x`` -> ``eval/x``, ``test_x`` -> ``test/x``, anything else ``train/x``."""
    out: dict[str, Any] = {}
    for key, value in logs.items():
        if key.startswith("eval_"):
            out["eval/" + key[len("eval_") :]] = value
        elif key.startswith("test_"):
            out["test/" + key[len("test_") :]] = value
        else:
            out["train/" + key] = value
    return out


def _args_run_name(args: Any) -> str | None:
    run_name = getattr(args, "run_name", None)
    # transformers 4.x defaulted run_name to output_dir: not a name.
    return run_name if run_name and run_name != getattr(args, "output_dir", None) else None


def _same_value(a: Any, b: Any) -> bool:
    try:
        if a == b:
            return True
        return isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b)
    except Exception:  # noqa: BLE001 -- an odd value is simply not "the same"
        return False


def _metric_key(metric: str) -> str:
    return metric if metric.startswith("eval_") else f"eval_{metric}"


def _score_at(state: Any, key: str, step: int) -> float | None:
    """The monitored metric's value logged at ``step``, newest first."""
    for entry in reversed(getattr(state, "log_history", None) or []):
        if entry.get("step") != step:
            if isinstance(entry.get("step"), int) and entry["step"] < step:
                break
            continue
        if key in entry:
            return _float_or_none(entry[key])
    return None


def _float_or_none(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _abspath(path: Any) -> str | None:
    return os.path.abspath(path) if isinstance(path, str) and path else None


def _shared_run_message(label: str, why: str, who: str = "this Trainer") -> str:
    # The server's metric insert is ON CONFLICT DO NOTHING (app/telemetry/store.py):
    # the first point a run gets at a step is the one it keeps.
    return (
        f"probe: this ProbeCallback writes to run {label}, which an earlier Trainer in this "
        f"process already wrote to: {why} Where both log a metric at the same step, the server "
        f"keeps the first point, so {who}'s curve is lost there."
    )


def _unfinished_verdict() -> str:
    """A person's Ctrl-C is ``canceled``; the SIGINT torch sends a worker when
    its parent was killed (nobody decided that) is ``failed``, as is anything
    else that stopped ``train()``."""
    if signal.SIGINT in _SIGNALS_SEEN and _PARENT_DIED not in _SIGNALS_SEEN:
        return "canceled"
    return "failed"


class _AtExit:
    """At exit, a ``train()`` that never ended decides the verdict.

    Registered after ``probe.init()`` installed its exit hooks, so it runs
    before their close (atexit is last-in, first-out). Speaks only when no
    exit path spoke: an uncaught exception, Ctrl-C or ``sys.exit`` already
    recorded how the process ends. What is left is a script that caught the
    exception out of ``train()`` and ran to its end."""

    def __init__(self) -> None:
        self._pid: int | None = None

    def register(self) -> None:
        if self._pid != os.getpid():
            self._pid = os.getpid()
            atexit.register(self)

    def __call__(self) -> None:
        try:
            if self._pid != os.getpid():
                return
            run = probe.active_run()
            if run is None or (run.id not in _UNFINISHED and run.id not in _ENDED_AS):
                return
            if run.id in _LAUNCHER_RUNS or run.id == os.environ.get("PROBE_RUN_ID", "").strip():
                return  # the launcher closes it from the real exit code
            if getattr(fluent, "_exit_recorded", False):
                return
            fluent.note_exit(_unfinished_verdict() if run.id in _UNFINISHED else _ENDED_AS[run.id])
        except Exception:  # noqa: BLE001 -- nothing may stand between a script and its exit
            log.debug("probe: noting an unfinished train() failed", exc_info=True)


_note_unfinished_at_exit = _AtExit()


def _close_when_this_worker_exits(run_id: str) -> None:
    """Close the run this multiprocessing worker opened when it exits.

    A forked worker (accelerate's ``notebook_launcher``, a ``Process`` per
    trial with the ``fork`` start method, the Jupyter default on Linux) leaves
    through ``os._exit``, which runs no exit hook: the run stayed ``running``.
    multiprocessing runs its own finalizers in the worker's ``finally`` on
    every way out, which is where this goes (a spawned worker's atexit then
    finds nothing open). The same close ``lightning.py`` makes for its workers."""
    from multiprocessing import util

    util.Finalize(None, _close_at_worker_exit, args=(run_id,), exitpriority=100)


def _close_at_worker_exit(run_id: str) -> None:
    # Runs inside the worker's `finally`: an exception still in flight is how
    # the worker is ending. torch's worker wrapper turns an error into
    # `sys.exit(1)` and swallows KeyboardInterrupt (the signal note saw it).
    exc = sys.exc_info()[1]

    def close() -> None:
        try:
            verdict, cause = _worker_verdict(exc, run_id)
            if verdict is not None:
                fluent.note_exit(verdict, cause)
            cap_finish_timeout(WORKER_CLOSE_SECONDS)
            fluent._finish_at_exit()
        except Exception:  # noqa: BLE001 -- a worker's exit must never raise from here
            log.debug("probe: closing the worker's run failed", exc_info=True)

    # Held: torch SIGTERMs the other workers the moment one fails, and a
    # killed parent sends its workers SIGINT; either cut the close short.
    run_held(close, (signal.SIGTERM, signal.SIGINT), WORKER_HOLD_SECONDS)


def _worker_verdict(
    exc: BaseException | None, run_id: str
) -> tuple[str | None, BaseException | None]:
    if run_id in _UNFINISHED and signal.SIGINT in _SIGNALS_SEEN:
        # The note saw the SIGINT during train(): whatever raised after it (a
        # peer rank's gloo connection closing, as that rank stops too) is
        # its fallout, not the cause.
        return _unfinished_verdict(), None
    signum = _signal_behind(exc)
    if signum == signal.SIGINT:
        # A person's Ctrl-C, unless the parent was already gone (torch's
        # death signal): the note recorded which, when the signal came.
        return ("failed" if _PARENT_DIED in _SIGNALS_SEEN else "canceled"), None
    if signum is not None:
        return "failed", None
    if isinstance(exc, SystemExit):
        if exc.code not in (None, 0, False):
            context = exc.__context__
            return "failed", context if isinstance(context, Exception) else None
    elif isinstance(exc, Exception):
        return "failed", exc
    if run_id in _UNFINISHED:
        return _unfinished_verdict(), None
    return _ENDED_AS.get(run_id), None


def _signal_behind(exc: BaseException | None) -> int | None:
    """The signal an ending came from: KeyboardInterrupt is SIGINT, and torch
    elastic's workers (``notebook_launcher`` in a script, ``elastic_launch``)
    raise ``SignalException(sigval=...)`` from their SIGINT / SIGTERM handler,
    which torch's worker wrapper then turns into ``sys.exit(1)``."""
    seen: set[int] = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        if isinstance(exc, KeyboardInterrupt):
            return signal.SIGINT
        sigval = getattr(exc, "sigval", None)
        if isinstance(sigval, int):
            return int(sigval)
        exc = exc.__cause__ or exc.__context__
    return None


class _SignalNote:
    """Chained in front of a SIGINT / SIGTERM handler: notes, then hands on."""

    def __init__(self, signum: int, previous: Any) -> None:
        self.signum = signum
        self.previous = previous
        self.pid = os.getpid()
        self.ppid = os.getppid()

    def __call__(self, signum: int, frame: Any) -> Any:
        if os.getpid() == self.pid:
            _SIGNALS_SEEN.add(signum)
            if signum == signal.SIGINT and _parent_gone(self.ppid):
                _SIGNALS_SEEN.add(_PARENT_DIED)
            # Noted once is enough: step aside, so a later signal (and anything
            # that checks for the default SIGINT handler, as asyncio.run does)
            # meets the handler that was there before.
            try:
                if signal.getsignal(signum) is self:
                    signal.signal(signum, self.previous)
            except (ValueError, OSError):
                pass
        return self.previous(signum, frame)


def _parent_gone(ppid: int) -> bool:
    """The parent process has died, or is dying. ``getppid()`` alone misses
    the second case: the death signal comes when the THREAD that forked us
    exits, and until the rest of a multi-threaded parent (torch's launcher)
    is gone we are handed to a sibling thread, with the same pid. Its
    ``/proc`` state then reads zombie (Linux; elsewhere only getppid)."""
    if os.getppid() != ppid:
        return True
    try:
        with open(f"/proc/{ppid}/stat", "rb") as stat_file:
            state = stat_file.read().rsplit(b")", 1)[1].split()[0]
    except (OSError, IndexError):
        return False
    return state in (b"Z", b"X", b"x")


def _chain_signal_notes() -> None:
    """Chain a :class:`_SignalNote` over each Python-level handler (the
    default SIGINT raises KeyboardInterrupt; SIGTERM has one only under
    ``enable_jit_checkpoint`` or a framework's own). SIG_DFL, SIG_IGN and a
    handler set outside Python are left alone. Main thread only."""
    if threading.current_thread() is not threading.main_thread():
        return
    for signum in (signal.SIGINT, signal.SIGTERM):
        try:
            current = signal.getsignal(signum)
            if isinstance(current, _SignalNote) and current.pid == os.getpid():
                continue
            if not callable(current):
                continue
            signal.signal(signum, _SignalNote(signum, current))
        except (ValueError, OSError):
            continue


def _unchain_signal_notes() -> None:
    """Put back the handler each note was chained over, if still in place."""
    if threading.current_thread() is not threading.main_thread():
        return
    for signum in (signal.SIGINT, signal.SIGTERM):
        try:
            current = signal.getsignal(signum)
            if isinstance(current, _SignalNote) and current.pid == os.getpid():
                signal.signal(signum, current.previous)
        except (ValueError, OSError):
            continue


#: Packages a warning must not point into: the line it names should be the
#: user's own (`trainer.train()`), not one in here or in the Trainer.
_INTERNAL_PACKAGES = ("probe", "transformers", "accelerate", "torch")


def _user_stacklevel() -> int:
    """The ``stacklevel`` (1 = the caller of this) of the first frame outside
    Probe, transformers, accelerate and torch; the outermost when all are."""
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


def _register_report_to() -> None:
    """``report_to="probe"``: transformers resolves ``report_to`` names in this
    dict when a Trainer is built. Never replaces an entry already there, and a
    transformers without the dict leaves ``callbacks=[ProbeCallback()]``."""
    try:
        from transformers.integrations import integration_utils
    except Exception:  # noqa: BLE001 -- the explicit callbacks= path still works
        log.debug(
            "probe: transformers has no integration_utils; report_to='probe' unavailable",
            exc_info=True,
        )
        return
    registry = getattr(integration_utils, "INTEGRATION_TO_CALLBACK", None)
    if isinstance(registry, dict):
        registry.setdefault("probe", ProbeCallback)


_register_report_to()
