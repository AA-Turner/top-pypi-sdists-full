"""TrainingRecorder: one TRL process's per-sample training metrics (plan rl-trajectory-metrics T4). It places each loss
call the hook saw (`LossBatch`) inside the optimizer update (train) or `evaluate()` pass (eval) it belongs to, and
sends the rows and the update's own records as producer `trl-train-<rank>` from a background thread (`PointsSender`);
a context-parallel rank sends its slices of each example as fragments (`trl-train-<rank>-<fragment>`), the records
from fragment 0 only.
Every process sends its own rows; the others find the main process's run through the job's key-value store
(`handoff`), never a collective, so a process that skips `track()` is never waited on."""

from __future__ import annotations

import functools
import threading
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import Dtype, UpdateLevel
from probe.sdk.run.samples.points import (
    PointsSender, TrainingGuard, get_lowest_dtype, get_optimizer_step, keep_finite, to_float,
)

from probe.generated.samples.points import RollupSource

from .declarations import EVAL_KEY_PREFIX, EVAL_LOSSES, MAX_EVAL_PREFIXES, get_logging_window, make_plan
from .handoff import Handoff
from .hook import LossBatch, LossHook, Place
from .hooks import pick_hook

PRODUCER_PREFIX = "trl-train-"
#: Seconds the tracker's finish waits for this process's queued rows (and a non-main process's release).
RELEASE_FLUSH_SECONDS = 8.0
SKIPPED_REASON = "the optimizer step was skipped (accelerate's optimizer_step_was_skipped: a non-finite gradient)"
WHAT = "per-sample training metrics"


@dataclass
class Pass:
    """One optimizer update (train) or `evaluate()` pass (eval) on this process: its loss calls by ordinal."""

    split: str
    step: int
    index: int
    calls: dict[int, LossBatch] = field(default_factory=dict)
    #: Loss calls TRL made in it, counted before each is captured (a call Probe failed on reads missing).
    count: int = 0
    #: The loss calls TRL makes in it (gradient accumulation), read at its first call; eval: `count`.
    expected_calls: int | None = None
    #: The newest weights the generator had (`weights_version`), read at its first call.
    weights_version: int | None = None
    #: An eval pass's `metric_key_prefix`: its rows log under `<prefix>_<key>`, the names TRL logs its loss under.
    prefix: str = EVAL_KEY_PREFIX
    #: An eval pass under a prefix past `MAX_EVAL_PREFIXES`: its calls record nothing.
    is_skipped: bool = False


@dataclass(frozen=True)
class CallSlot:
    """Where one loss call goes: its pass and its ordinal there (`micro_batch`)."""

    owner: Pass
    ordinal: int


@dataclass(frozen=True)
class _Writer:
    """What `PointsSender` writes through: a run's samples as this process's producer."""

    samples: Any


@dataclass
class _Join:
    """The sender's attach function: what joining the run needs and never the recorder or its trainer, so a finished
    trainer is freed while the process lives on. The main process writes through ``run`` (set when it starts
    sending); the others wait for the run id ``handoff`` brings and keep the handle they ``attached``. The sender's
    own release never covers that handle: it holds the `_Writer`, which on the main process is the tracker's run."""

    is_main: bool
    handoff: Handoff
    run: Any = None
    attached: Any = None
    #: This process finished before the main process's run id arrived: stop waiting.
    is_closed: bool = False
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def __call__(self, producer: str) -> _Writer:
        if self.is_main:
            return _Writer(self.run.samples.as_producer(producer))
        run_id = self.handoff.wait(should_stop=lambda: self.is_closed)
        if run_id is None:
            raise RuntimeError("the main process left no run id (it has no run, did not call track(), or this process "
                               "finished first)")  # fmt: skip
        from probe.sdk.run.samples import attach_producer

        attached = attach_producer(producer, run_id=run_id, should_sample_hardware=False, should_capture_logs=False)
        with self._lock:
            is_closed = self.is_closed
            if not is_closed:
                self.attached = attached
        if is_closed:  # the recorder closed while the attach was in flight: nothing holds this handle but us
            attached.finish("completed", flush_timeout=RELEASE_FLUSH_SECONDS)
            raise RuntimeError("this process finished while joining the run")
        return _Writer(attached.samples.as_producer(producer))

    def close(self) -> Any:
        """Stop waiting and take the attached handle (None while an attach is in flight: it finishes its own)."""
        with self._lock:
            self.is_closed = True
            attached, self.attached, self.run = self.attached, None, None
        return attached


class TrainingRecorder:
    """The per-sample side of one `TrlTracker`, on every process that calls `track()`."""

    def __init__(self, tracker: Any) -> None:
        self.tracker = tracker
        self.trainer = tracker.trainer
        self.guard = TrainingGuard("TRL")
        self.join = _Join(bool(tracker.is_main), Handoff.make(self._get_output_dir(), self.trainer))
        self.sender = PointsSender("TRL", attach=self.join)
        self.should_record_sft = bool(getattr(tracker, "_should_record_sft", False))
        hook_cls, self.unsupported = pick_hook(self.trainer)
        hook = hook_cls(self.trainer, self) if hook_cls is not None else None
        #: The hook's own words for what it names (`LossHook.get_reasons`).
        self.reasons: dict[str, str] = {}
        if hook is not None:
            self.unsupported = hook.find_unsupported()
            self.reasons = hook.get_reasons()
        #: None: this run's trainer or settings are out of reach (`unsupported` says why); nothing is wrapped.
        self.hook: LossHook | None = hook if hook is not None and not self.unsupported else None
        #: Where this process sends as; None: another process sends its rows (a TP rank past 0).
        self.place: Place | None = (hook or LossHook(self.trainer, self)).get_place()
        #: Found while training (too many eval prefixes): declared unsupported once found.
        self.found_unsupported: list[str] = []
        #: The `evaluate()` prefixes seen, each with its own eval rollups (`eval` always).
        self.eval_prefixes: list[str] = [EVAL_KEY_PREFIX]
        #: The prefixes whose passes made loss calls, in order: an eval loss rollup is declared only for such a prefix,
        #: and none once two have (`EVAL_LOSSES`).
        self.loss_prefixes: list[str] = []
        #: The precision the loss tensors showed (None until the first loss call), and each key's computed from
        #: other tensors (`LossBatch.dtypes`).
        self.dtype: Dtype | None = None
        self.dtypes: dict[str, Dtype] = {}
        #: A loss call returned a bf16 / fp16 loss: the plan was sent again with its loss rollups approximate.
        self._is_loss_rounded = False
        self._is_started = False
        self._is_training = False
        self._has_trained = False
        self._update: Pass | None = None
        self._evals: list[Pass] = []
        self._eval_counts: Counter = Counter()
        #: The learning rate and gradient norm of the update in flight (`_get_grad_norm`).
        self._update_metrics: dict[str, float] = {}
        #: What this recorder wrapped, taken off again at `close` (a returning trainer gets a fresh recorder).
        self._installed: list[tuple[Any, str, Any]] = []
        #: Closed (`close`): every wrap still on passes straight through.
        self.is_closed = False

    # -- what the tracker calls ------------------------------------------------------------------------------
    @property
    def rank(self) -> int:
        return self.place[0] if self.place is not None else 0

    @property
    def world(self) -> int:
        return self.place[1] if self.place is not None else 1

    @property
    def fragment(self) -> int:
        return self.place.fragment if self.place is not None else 0

    @property
    def fragments(self) -> int:
        return self.place.fragments if self.place is not None else 1

    @property
    def is_training(self) -> bool:
        """Inside this trainer's `train()`."""
        return self._is_training

    @property
    def has_trained(self) -> bool:
        """This trainer's `train()` began at least once (a recorder tracked up front and never trained has not)."""
        return self._has_trained

    def get_plan(self) -> dict | None:
        """The `TrainingPlan` the main process declares, or None when this trainer has nothing to say. A run that
        sends nothing at all (no hook: the trainer, a subclass's loss or a setting is out of reach) says so under
        `*` too."""
        if self.hook is None and not self.unsupported:
            return None
        if self.hook is None:
            return make_plan(unsupported=self.unsupported, stopped=self.unsupported, reasons=self.reasons)
        dtype = self.dtype or self.hook.get_dtype()
        rollups = self.hook.get_rollups(dtype, get_logging_window(self.trainer.args), self.dtypes, self.eval_prefixes)
        # The server folds a loss rollup over every eval row of a step whatever its name, onto the rollup's run key:
        # one for a prefix with no loss calls, or beside another prefix's, would write a point TRL never logged.
        losses = {f"{prefix}_loss" for prefix in self.loss_prefixes} if len(self.loss_prefixes) == 1 else set()
        rollups = {key: rollup for key, rollup in rollups.items() if rollup["split"] != SampleSplit.EVAL
                   or rollup.get("source") != RollupSource.CONTRIBUTION or key in losses}  # fmt: skip
        unsupported = [*self.hook.find_unsent(), *self.unsupported, *self.found_unsupported]
        return make_plan(rollups=rollups, unsupported=unsupported, reasons=self.reasons)

    def setup(self) -> None:
        """Wrap the loss path, `evaluate` and the gradient norm (after the sample recorder, so ours sit outside)."""
        if self.hook is None:
            return
        self.hook.install()
        trainer = self.trainer
        evaluate = trainer.evaluate

        @functools.wraps(evaluate)
        def call_evaluate(*args: Any, **kwargs: Any) -> Any:
            prefix = kwargs.get("metric_key_prefix", args[2] if len(args) > 2 else EVAL_KEY_PREFIX)
            self.guard.call("a per-sample eval pass", self._start_eval, prefix)
            try:
                result = evaluate(*args, **kwargs)
            except BaseException:  # a crashed pass sends its rows undeclared: it never reads complete
                self.guard.call("a per-sample eval pass", self._end_eval, is_complete=False)
                raise
            self.guard.call("a per-sample eval pass", self._end_eval)
            return result

        self.install(trainer, "evaluate", call_evaluate)
        get_grad_norm = getattr(trainer, "_get_grad_norm", None)
        if callable(get_grad_norm):

            @functools.wraps(get_grad_norm)
            def call_get_grad_norm(*args: Any, **kwargs: Any) -> Any:
                norm = get_grad_norm(*args, **kwargs)
                self.guard.call("a per-sample update", self._keep_update_metrics, norm)
                return norm

            self.install(trainer, "_get_grad_norm", call_get_grad_norm)

    def install(self, target: Any, name: str, value: Any) -> None:
        self.tracker.install(target, name, value)
        self._installed.append((target, name, value))

    def get_last_call(self, split: str) -> tuple[int, int]:
        """The (step, call) the sample recorder keyed the newest generation of ``split`` by."""
        return self.tracker.last_calls[split]

    def handle_train_start(self) -> None:
        """Before transformers' `train()`: the main process starts sending and leaves its run id for the others (with
        no run, that it has none); the others start at their first loss call. Nothing waits on another process."""
        if self.hook is None:
            return
        self._is_training = self._has_trained = True
        if self.tracker.is_main:
            if self.tracker.run is None:
                self.guard.call("the run id handoff", self.join.handoff.save, None)
            self._ensure_sending()

    def handle_step_end(self, step: int) -> None:
        """`on_step_end`, every process: the update's rows and records, with whether it applied."""
        update, self._update = self._update, None
        metrics, self._update_metrics = self._update_metrics, {}
        if update is None:
            return
        if update.step != step:  # never dropped: sent undeclared, as an update cut off is
            self._send_pass(update, optimizer_step=None, should_declare=False)
            return
        accelerator = getattr(self.trainer, "accelerator", None)
        is_applied = not bool(getattr(accelerator, "optimizer_step_was_skipped", False))
        optimizer_step = self._get_optimizer_step()
        whole = None
        if self.rank == 0:
            whole = {"level": UpdateLevel.UPDATE, "ranks_expected": self.world, "updates_in_step": 1,
                     "reduction": self.hook.get_reduction(), "dtype": self._get_pass_dtype(update),
                     "applied": is_applied, "weights_version": update.weights_version,
                     "optimizer_step": optimizer_step, "metrics": metrics or None}  # fmt: skip
            if not is_applied:
                whole["skipped_reason"] = SKIPPED_REASON
        self._send_pass(update, optimizer_step=optimizer_step, whole=whole)

    def handle_train_end(self) -> None:
        """`on_train_end`, and the `finally` around `train()` (a crash): an update cut off before its step end still
        sends its rows; they read undeclared."""
        self._send_pending_update()
        self._is_training = False

    def open_call(self, split: str) -> CallSlot | None:
        """Count one loss call of ``split`` (before it runs) in the update or eval pass it sits in; None when it sits
        in neither, or this process cannot send."""
        if self.is_closed or self.place is None:
            return None
        if split == SampleSplit.EVAL:
            if not self._evals or self._evals[-1].is_skipped or not self._ensure_sending():
                return None
            current = self._evals[-1]
            if current.prefix not in self.loss_prefixes:  # its loss rollup, or none once two prefixes made loss calls
                self.loss_prefixes.append(current.prefix)
                self._send_plan(unsupported=EVAL_LOSSES if len(self.loss_prefixes) > 1 else None)
        else:
            if not self._is_training or not self._ensure_sending():
                return None
            step = int(self.trainer.state.global_step) + 1
            if self._update is None or self._update.step != step:
                self._send_pending_update()
                accumulation = getattr(self.trainer, "current_gradient_accumulation_steps", None)
                self._update = Pass(SampleSplit.TRAIN, step, 0, weights_version=self._get_weights_version(step),
                                    expected_calls=int(accumulation) if accumulation else None)  # fmt: skip
            current = self._update
        current.count += 1
        return CallSlot(current, current.count - 1)

    def handle_loss(self, slot: CallSlot, batch: LossBatch) -> None:
        slot.owner.calls[slot.ordinal] = batch
        guess = self.hook.get_dtype()
        declared = (self.dtype or guess, {key: self.dtypes.get(key, guess) for key in batch.dtypes})
        self.dtype = get_lowest_dtype([dtype for dtype in (self.dtype, batch.dtype) if dtype is not None])
        for key, dtype in batch.dtypes.items():
            self.dtypes[key] = get_lowest_dtype([found for found in (self.dtypes.get(key), dtype) if found is not None])
        is_new_rounding = batch.is_loss_rounded and not self._is_loss_rounded
        self._is_loss_rounded = self._is_loss_rounded or batch.is_loss_rounded
        if is_new_rounding or (self.dtype, {key: self.dtypes[key] for key in batch.dtypes}) != declared:
            self._send_plan()  # the tensors' own precision, not the mixed-precision flag's guess

    def close(self) -> None:
        """The tracker finished, or another trainer's `train()` began: what is still held is sent, the hooks and
        wraps come off, the queue is flushed, the sender's thread stops and lets go of the run (a finished trainer is
        freed in a process that lives on), and a non-main process's handle is released. Safe to call twice."""
        if self.is_closed:
            return
        self.is_closed = True
        self._send_pending_update()
        while self._evals:
            self._send_pass(self._evals.pop(), optimizer_step=None, should_declare=False)
        if self.hook is not None:
            self.hook.close()
        uninstall = getattr(self.tracker, "uninstall", None)
        for target, name, value in reversed(self._installed):
            if uninstall is not None:
                self.guard.call("a per-sample unwrap", uninstall, target, name, value)
        self._installed.clear()
        if self._is_started:
            self.sender.flush(RELEASE_FLUSH_SECONDS)
        attached = self.join.close()
        self.sender.close(0.0)
        if attached is not None:
            self.guard.call("a per-sample release", attached.finish, "completed", flush_timeout=RELEASE_FLUSH_SECONDS)

    # -- inside ------------------------------------------------------------------------------------------------
    def _ensure_sending(self) -> bool:
        """The main process sends once its run is open, and then leaves the run id for the others; another process
        starts at its first loss call, its sender's thread waiting for that id (`handoff`)."""
        is_main = self.tracker.is_main
        if is_main and self.tracker.run is None:
            return False
        if not self._is_started:
            self._is_started = True
            self.join.run = self.tracker.run if is_main else None
            self.sender.start(self._get_producer())
            if is_main:
                self.guard.call("the run id handoff", self.join.handoff.save, str(self.tracker.run.id))
        return not self.sender.is_disabled

    def _get_producer(self) -> str:
        """`trl-train-<rank>`; a context-parallel rank `trl-train-<rank>-<fragment>`: every process its own producer."""
        suffix = f"-{self.fragment}" if self.fragments > 1 else ""
        return f"{PRODUCER_PREFIX}{self.rank}{suffix}"

    def _get_output_dir(self) -> str | None:
        return getattr(self.trainer.args, "output_dir", None)

    def _send_plan(self, *, unsupported: str | None = None) -> None:
        """Send the plan again (main process) once something it declared is known better: the loss's dtype, a pass
        that sends nothing. A `TrainingPlan` replaces the producer's last one whole."""
        if unsupported is not None:
            if unsupported in self.found_unsupported:
                return
            self.found_unsupported.append(unsupported)
        if self.tracker.is_main:
            self.tracker.send_training_plan()

    def _send_pending_update(self) -> None:
        update, self._update = self._update, None
        if update is not None:
            self._send_pass(update, optimizer_step=None, should_declare=False)

    def _keep_update_metrics(self, norm: Any) -> None:
        if self.is_closed:
            return
        metrics: dict[str, float] = {}
        grad_norm = keep_finite(to_float(norm))
        if grad_norm is not None:
            metrics["grad_norm"] = grad_norm
        groups = getattr(getattr(self.trainer, "optimizer", None), "param_groups", None) or []
        if groups and isinstance(groups[0], Mapping) and "lr" in groups[0]:
            rate = keep_finite(to_float(groups[0]["lr"]))  # the rate this update steps with
            if rate is not None:
                metrics["learning_rate"] = rate
        self._update_metrics = metrics

    def _get_optimizer_step(self) -> int | None:
        """The optimizer's own step count (AdamW's `state["step"]`): a skipped step does not advance it."""
        optimizer = getattr(self.trainer, "optimizer", None)
        return get_optimizer_step(getattr(optimizer, "optimizer", optimizer))

    def _get_weights_version(self, step: int) -> int:
        """The newest weights the generator had: with vLLM the step it last synced (`_last_loaded_step`), else the
        policy itself, `step - 1` updates in."""
        trainer = self.trainer
        loaded = getattr(trainer, "_last_loaded_step", None)
        if getattr(trainer, "use_vllm", False) and isinstance(loaded, int) and loaded >= 0:
            return loaded
        return step - 1

    def _get_pass_dtype(self, current: Pass) -> Dtype:
        return get_lowest_dtype(batch.dtype for batch in current.calls.values()) or self.dtype or self.hook.get_dtype()

    def _start_eval(self, prefix: Any) -> None:
        """An `evaluate()` pass. A prefix not seen before gets its own eval rollups (the plan is sent again), up to
        `MAX_EVAL_PREFIXES`; past them its calls record nothing."""
        if self.is_closed:
            return
        step = int(self.trainer.state.global_step)
        index = self._eval_counts[step]
        self._eval_counts[step] += 1
        prefix = str(prefix)
        is_new = prefix not in self.eval_prefixes
        is_skipped = is_new and len(self.eval_prefixes) >= MAX_EVAL_PREFIXES
        self._evals.append(Pass(SampleSplit.EVAL, step, index, prefix=prefix, is_skipped=is_skipped))
        if is_skipped:
            self._send_plan(unsupported="eval metric_key_prefix")
        elif is_new:
            self.eval_prefixes.append(prefix)
            self._send_plan()

    def _end_eval(self, *, is_complete: bool = True) -> None:
        if self.is_closed or not self._evals:
            return
        current = self._evals.pop()
        if not is_complete:
            self._send_pass(current, optimizer_step=None, should_declare=False)
            return
        current.expected_calls = current.count
        whole = None
        if self.rank == 0 and current.calls:
            whole = {"level": UpdateLevel.UPDATE, "split": SampleSplit.EVAL, "eval_pass": current.index,
                     "ranks_expected": self.world, "reduction": self.hook.get_reduction(),
                     "dtype": self._get_pass_dtype(current)}  # fmt: skip
        self._send_pass(current, optimizer_step=None, whole=whole)

    def _send_pass(self, current: Pass, *, optimizer_step: int | None, should_declare: bool = True,
                   whole: dict | None = None) -> None:  # fmt: skip
        """The pass's rows, then (declared) this process's rank and micro-batch records and the whole pass's, as one
        queued send: the training thread never waits on the network. Records come from fragment 0 alone (every
        fragment of a data-parallel rank makes the same calls over the same examples)."""
        should_declare = should_declare and self.fragment == 0
        whole = whole if self.fragment == 0 else None
        if not current.calls and not (should_declare and (whole is not None or current.count)):
            return
        rows: list[dict] = []
        for ordinal, batch in sorted(current.calls.items()):
            rows += self._make_rows(batch, current, ordinal, optimizer_step)
        records: list[dict] = []
        update = 0 if current.split == SampleSplit.TRAIN else None
        if should_declare and current.count:
            place = {"split": SampleSplit.EVAL, "eval_pass": current.index} if current.split == SampleSplit.EVAL else {}
            records.append({"level": UpdateLevel.RANK, "rank": self.rank, **place,
                            "micro_batches_expected": current.expected_calls or current.count,
                            "rows_expected": sum(len(batch.rows) for batch in current.calls.values())})  # fmt: skip
            for ordinal, batch in sorted(current.calls.items()):
                records.append(_drop_none({
                    "level": UpdateLevel.MICRO_BATCH, "rank": self.rank, "micro_batch": ordinal, **place,
                    "reported_loss": keep_finite(batch.reported_loss), "batch_terms": batch.batch_terms or None,
                    "scale": batch.scale, "normalizer": batch.normalizer, "rows": len(batch.rows),
                }))  # fmt: skip
        if should_declare and whole is not None:
            records.append(_drop_none(whole))
        self.sender.send(current.step, update, rows, records)

    def _make_rows(self, batch: LossBatch, current: Pass, ordinal: int, optimizer_step: int | None) -> list[dict]:
        """One `log_metrics_many` row per sample occurrence: its values and weights (eval keys under the pass's
        `<prefix>_` names), its place, and the loss bookkeeping."""
        prefix = f"{current.prefix}_" if current.split == SampleSplit.EVAL else ""
        extremes = self.hook.extremes
        seen: Counter = Counter()
        rows = []
        for position, (key, summary) in enumerate(zip(batch.keys, batch.rows, strict=True)):
            occurrence = seen[key]
            seen[key] += 1
            weights = {f"{prefix}{name}": batch.weights[name][position] if name in batch.weights else summary.weight
                       for name in summary.metrics}  # fmt: skip
            row: dict[str, Any] = {
                "sample_key": key, "step": current.step, "split": current.split,
                "metrics": {f"{prefix}{name}": value for name, value in summary.metrics.items()},
                "weights": weights, "rank": self.rank, "micro_batch": ordinal, "occurrence": occurrence,
                "token_count": summary.token_count, "mask_sha256": summary.mask_sha256, "loss_sum": summary.loss_sum,
                "normalizer": summary.normalizer, "scale": summary.scale, "contribution": summary.contribution,
                "contribution_source": summary.contribution_source,
            }  # fmt: skip
            agg = {f"{prefix}{name}": extremes[name] for name in summary.metrics if name in extremes}
            if agg:
                row["agg"] = agg
            if batch.fragments > 1:
                row.update(fragment=self.fragment, fragments_expected=batch.fragments)
            if current.split == SampleSplit.TRAIN:
                row.update(update=0, weights_version=current.weights_version, optimizer_step=optimizer_step)
            else:
                row["eval_pass"] = current.index
            rows.append(_drop_none(row))
        return rows


def _drop_none(record: dict[str, Any]) -> dict[str, Any]:
    return {name: value for name, value in record.items() if value is not None}
