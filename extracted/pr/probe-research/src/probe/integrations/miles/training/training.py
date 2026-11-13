"""A Miles train rank's per-sample training metrics (plan rl-trajectory-metrics T5). Each module is wrapped as it
loads (`samples/wraps.py`): `objective.loss_function` records each micro-batch, an update ends at the call each
backend makes once per optimizer update on every rank (torch-native / FSDP: `log_train_step` with `should_log`;
Megatron: `train_one_step`), and the rows go out as producer `miles-train-<dp>-<cp>` (a role other than the actor's
named in it) from the shared background sender, so no training step waits on the network. Every wrapper returns Miles' own result untouched; Probe's work
runs guarded. Line refs are `radixark/miles@bb18e6ab7811`. Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

import functools
import inspect
import logging
import math
import sys
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

from probe.generated.samples.points import Dtype
from probe.sdk.run.samples.points import (
    NON_FINITE_SKIP, PointsSender, TrainingGuard, get_lowest_dtype, get_optimizer_step, to_float,
)

from ..samples.wraps import OBJECTIVE_MODULE
from .plan import UNSUPPORTED, Unsupported, build_training_plan, get_role, get_unsupported_reason
from .stamp import RowStamp, read_stamp
from .update import OpenUpdate, RankFacts, UpdateEnd, open_update

logger = logging.getLogger(__name__)

WRAPPED_MARK = "__probe_miles_training__"
#: Megatron's `finalize_model_grads` wrapper (`megatron_utils/model.py:721`): divides gradients by the token count.
FINALIZE = "finalize_model_grads_with_empty_cache"
#: What each hook's guarded calls say they record, one per hook: the guard warns once per key, so a failure in one
#: hook never hides a different one in another.
LOSS_CALL = "a loss call's per-sample training metrics"
UPDATE_END = "an update's per-sample training metrics"
FINALIZED_TOKENS = "Megatron's all-reduced token count"
#: Why an update read not applied, beyond Miles' `valid_step` (inf / NaN gradients: `NON_FINITE_SKIP`).
DISABLED_OPTIMIZER = "debug_disable_optimizer"
NO_OPTIMIZER_STEP = "no optimizer step ran in the update"
#: Miles' `TrainStepOutcome` for an `indep_dp` update whose replicas' all-reduce failed (`megatron_utils/model.py:645`):
#: the attempt is discarded and `train()` retried in this process (`ray/train/group.py:239`). Probe drops it (no rows,
#: no record) because the server keeps a step's first delivery, so a sent attempt would hide the retry's real update.
RETRIED_OUTCOME = "DISCARDED_SHOULD_RETRY"


@dataclass
class OpenCall:
    """One `loss_function` call being watched."""

    update: OpenUpdate
    index: int
    watch: Any
    calls: Any
    bound: dict[str, Any]
    stamp: RowStamp


class MilesTraining:
    """This process's recording: the update in progress, the optimizer steps seen, what it declared, and the sender."""

    def __init__(self) -> None:
        self.guard = TrainingGuard("Miles")
        self.sender = PointsSender("Miles", attach=self._attach)
        self.current: OpenUpdate | None = None
        self.optimizer_steps = 0
        self.last_optimizer: Any = None
        self.has_step_hook = False
        self.finalized_tokens: float | None = None
        #: Who this process is (its producer; the actor's dp 0 / cp 0 / tp 0 declares) and the args its sender joins
        #: with.
        self.facts: RankFacts | None = None
        self._args: Any = None
        self._real_loss: Any = None
        self._reasons: list[Unsupported] = []
        self._dtype: Dtype | None = None
        #: The most updates a rollout ran (`num_steps_per_rollout`): above 1 the rollup is logged per update.
        self._updates_in_step = 1
        self._declared: dict[str, Any] | None = None
        self._is_off: bool | None = None
        self._warned: set[str] = set()

    # -- the wraps -----------------------------------------------------------------------------------------
    def install_objective(self, module: Any) -> None:
        """Wrap `loss_function` where Miles defines it; modules that already bound it are rebound as they load."""
        original = getattr(module, "loss_function", None)
        if not callable(original) or getattr(original, WRAPPED_MARK, False):
            return
        self._real_loss = original
        module.loss_function = self.wrap_loss(original, module)
        self.setup_step_hook()

    def install_torch_native(self, module: Any) -> None:
        """The torch-native actor (FSDP, torchtitan): its bound `loss_function`, and `log_train_step` ends an update
        (`torch_native/actor.py:285`, every rank: `should_log` picks the one that logs)."""
        self._set_bound_loss(module)
        original = getattr(module, "log_train_step", None)
        if callable(original) and not getattr(original, WRAPPED_MARK, False):
            module.log_train_step = self._wrap_after(original, UPDATE_END, self.end_torch_native_update)

    def install_megatron(self, module: Any) -> None:
        """Megatron's model module: its bound `loss_function`, `train_one_step` ends an update (every rank), and the
        gradient finalizer's all-reduced token count is kept (per-token mode's normalizer)."""
        self._set_bound_loss(module)
        original = getattr(module, "train_one_step", None)
        if callable(original) and not getattr(original, WRAPPED_MARK, False):
            module.train_one_step = self._wrap_after(original, UPDATE_END, self.end_megatron_update,
                                                     before=self.start_megatron_step)  # fmt: skip
        finalize = getattr(module, FINALIZE, None)
        if callable(finalize) and not getattr(finalize, WRAPPED_MARK, False):
            setattr(module, FINALIZE, self._wrap_after(finalize, FINALIZED_TOKENS, self.keep_finalized_tokens))

    def _set_bound_loss(self, module: Any) -> None:
        """A module that bound Miles' own `loss_function` by name before the wrap gets the wrapped one."""
        if self._real_loss is None and (objective := sys.modules.get(OBJECTIVE_MODULE)) is not None:
            self.install_objective(objective)
        if self._real_loss is not None and getattr(module, "loss_function", None) is self._real_loss:
            module.loss_function = sys.modules[OBJECTIVE_MODULE].loss_function

    def setup_step_hook(self) -> None:
        """Count optimizer steps (torch's global post-step hook): an update that ran none was skipped (Megatron's
        `valid_step`), and the stepped optimizer's own counter is the update's `optimizer_step`."""
        if self.has_step_hook:
            return
        try:
            from torch.optim.optimizer import register_optimizer_step_post_hook

            register_optimizer_step_post_hook(self._count_step)
            self.has_step_hook = True
        except Exception as exc:  # noqa: BLE001 -- an old torch: `applied` stays unknown
            self._warn_once("step hook", f"Probe cannot see Miles' optimizer steps; updates read applied unknown: {exc}")

    def _count_step(self, optimizer: Any, *_: Any) -> None:
        self.optimizer_steps += 1
        self.last_optimizer = optimizer

    def wrap_loss(self, original: Any, objective: Any) -> Any:
        """Miles' `loss_function`, its result untouched; a stamped, supported call is watched and recorded."""

        @functools.wraps(original)
        def call_loss_function(*args: Any, **kwargs: Any) -> Any:
            call = self.guard.call(LOSS_CALL, self.open_call, original, objective, args, kwargs)
            try:
                result = original(*args, **kwargs)
            finally:
                if call is not None:
                    self.guard.call(LOSS_CALL, call.watch.__exit__, None, None, None)
            if call is not None:
                self.guard.call(LOSS_CALL, self.record_micro_batch, call, result)
            return result

        setattr(call_loss_function, WRAPPED_MARK, True)
        return call_loss_function

    def _wrap_after(self, original: Any, what: str, after: Any, before: Any = None) -> Any:
        """``original`` with its result untouched; ``after(bound arguments, result)`` runs guarded (as ``what``) once
        it returned."""

        @functools.wraps(original)
        def watch(*args: Any, **kwargs: Any) -> Any:
            if before is not None:
                self.guard.call(what, before)
            result = original(*args, **kwargs)
            self.guard.call(what, lambda: after(_bind(original, args, kwargs), result))
            return result

        setattr(watch, WRAPPED_MARK, True)
        return watch

    # -- a micro-batch -------------------------------------------------------------------------------------
    def is_recording(self) -> bool:
        """Probe records in this process: not switched off (`PROBE_MILES=off`, `PROBE_MODE=disabled`), and the
        sender has not given up joining the run."""
        if self._is_off is None:
            from ..samples.producers import is_probe_off

            self._is_off = is_probe_off()
        return not self._is_off and not self.sender.is_disabled

    def open_call(self, original: Any, objective: Any, args: tuple, kwargs: dict) -> OpenCall | None:
        """Before Miles' loss runs: count the call in the open update and start watching its reducers, when the
        micro-batch is stamped and its path supported. A call the hook cannot capture (unstamped, unsupported inside
        an update) breaks the update: nothing is sent for it."""
        if not self.is_recording():
            return None
        bound = _bind(original, args, kwargs)
        arguments, batch = bound["args"], bound["batch"]
        state = _get_parallel_state()
        if int(getattr(getattr(state, "tp", None), "rank", 0) or 0) != 0:
            return None  # every tensor-parallel rank computes the same loss: tensor-parallel 0 alone records it
        stamp = read_stamp(batch)
        facts = make_facts(bound, stamp, state)
        self.facts, self._args = self.facts or facts, self._args or arguments
        reason = get_unsupported_reason(arguments, batch, state)
        if reason is not None:
            self._mark_broken(f"an unsupported path ({reason})")
            self.record_unsupported(reason)
            return None
        if self.current is not None and stamp is not None and _is_restart(self.current, stamp):
            self._warn_once("abandoned", "Probe dropped a Miles update that never ended (its train step raised or "
                                         "was retried); the next one records afresh.")  # fmt: skip
            self.current = None
        if self.current is None:
            self.current = open_update(facts, self.optimizer_steps)
            self.sender.start(self.get_producer())  # joins the run in the background while the update trains
        update = self.current
        index = update.log.count_call()  # counted before anything can fail: a lost call reads missing
        if stamp is None:
            update.log.broken_reason = "a micro-batch carried no row stamp"
            return None
        update.source, update.position = stamp.source, stamp.position
        from .watch import watch_reductions

        watch = watch_reductions(objective)
        return OpenCall(update=update, index=index, watch=watch, calls=watch.__enter__(), bound=bound, stamp=stamp)

    def record_micro_batch(self, call: OpenCall, result: Any) -> None:
        """Inside the step only device work; the host copy waits for the update's end (`finish_micro_batches`)."""
        from .loss import start_summary

        update, bound = call.update, call.bound
        pending = start_summary(call.calls, args=bound["args"], batch=bound["batch"], result=result,
                                facts=update.facts, micro_batch_count=int(bound["num_microbatches"]),
                                sample_indices=call.stamp.sample_indices)  # fmt: skip
        if pending is not None:
            update.pending.append((call.index, pending))

    def finish_micro_batches(self, update: OpenUpdate) -> None:
        """Once the update ended: each micro-batch's host copy and rows, in call order (a failure leaves that
        micro-batch out, so the update is incomplete and sends nothing)."""
        from .loss import finish_summary

        pending, update.pending = update.pending, []
        for index, summary in pending:
            captured = self.guard.call(LOSS_CALL, finish_summary, summary, len(update.identities))
            if captured is None:
                return
            update.log.add(index, captured.micro_batch)
            update.identities.extend(captured.identities)
            update.names |= captured.names

    def _mark_broken(self, why: str) -> None:
        if self.current is not None:
            self.current.log.count_call()
            self.current.log.broken_reason = why

    # -- an update ends ------------------------------------------------------------------------------------
    def start_megatron_step(self) -> None:
        """Before `train_one_step`: no update is open (one still open is a step that raised; a retry starts afresh)."""
        self.finalized_tokens = None
        if self.current is not None:
            self._warn_once("abandoned", "Probe dropped a Miles update that never ended (its train step raised or "
                                         "was retried); the next one records afresh.")  # fmt: skip
            self.current = None

    def end_torch_native_update(self, bound: dict[str, Any], _result: Any) -> None:
        """torch-native never skips an optimizer step (`fsdp_utils/actor.py:372-379`): applied is whether one ran."""
        update, self.current = self.current, None
        if update is None:
            return
        metrics = {"grad_norm": to_float(bound.get("grad_norm"))}
        metrics.update({str(k): to_float(v) for k, v in (bound.get("extra_metrics") or {}).items()})
        steps = bound.get("num_steps_per_rollout")
        applied = self._get_applied(update)
        end = UpdateEnd(step=int(bound["rollout_id"]), update=int(bound["step_id"]),
                        updates_in_step=int(steps) if steps is not None else update.facts.steps_hint,
                        is_applied=applied, optimizer_step=self._get_optimizer_step(None),
                        reported_loss=_get_logged_loss(bound.get("loss_dict")), metrics=metrics,
                        skipped_reason=NO_OPTIMIZER_STEP if applied is False else None)  # fmt: skip
        self.queue_update(update, end)

    def end_megatron_update(self, bound: dict[str, Any], result: Any) -> None:
        """`train_one_step` returns (loss_dict, grad_norm, outcome); a skipped step ran no optimizer step."""
        update, self.current = self.current, None
        if update is None:
            return
        loss_dict, grad_norm, outcome = result
        if getattr(outcome, "name", None) == RETRIED_OUTCOME:
            self._warn_once("retried", "Probe dropped a Miles update its replicas discarded to retry "
                                       "(DISCARDED_SHOULD_RETRY); the retry records it.")  # fmt: skip
            return
        optimizer, scheduler = bound.get("optimizer"), bound.get("opt_param_scheduler")
        applied = self._get_applied(update)
        end = UpdateEnd(step=int(bound["rollout_id"]), update=int(bound["step_id"]),
                        updates_in_step=update.facts.steps_hint, is_applied=applied,
                        optimizer_step=self._get_optimizer_step(optimizer), reported_loss=_get_logged_loss(loss_dict),
                        metrics={"grad_norm": to_float(grad_norm), **_get_learning_rates(optimizer, scheduler)},
                        finalized_tokens=self.finalized_tokens)  # fmt: skip
        if applied is False:
            end.skipped_reason = get_skip_reason(bound.get("args"), optimizer, outcome)
        self.queue_update(update, end)

    def keep_finalized_tokens(self, bound: dict[str, Any], _result: Any) -> None:
        """`finalize_model_grads` all-reduced `num_tokens` in place over data x context parallel
        (`finalize_model_grads.py:575`): Megatron per-token mode's normalizer."""
        tokens = bound.get("num_tokens")
        positional, named = bound.get("args"), bound.get("kwargs")  # Miles' wrapper takes (*args, **kwargs)
        if tokens is None and isinstance(named, dict):
            tokens = named.get("num_tokens")
        if tokens is None and isinstance(positional, tuple) and len(positional) > 1:
            tokens = positional[1]
        self.finalized_tokens = to_float(tokens)

    def _get_applied(self, update: OpenUpdate) -> bool | None:
        return self.optimizer_steps > update.optimizer_steps_at_open if self.has_step_hook else None

    def _get_optimizer_step(self, optimizer: Any) -> int | None:
        """The last stepped optimizer's counter, else the one Miles passed (a Megatron `ChainedOptimizer` included:
        the shared `get_optimizer_step` reads its parts and never raises, so the update's record is always sent)."""
        for candidate in (self.last_optimizer, optimizer, getattr(optimizer, "optimizer", None)):
            step = get_optimizer_step(candidate) if candidate is not None else None
            if step is not None:
                return step
        return None

    # -- sending (background) ------------------------------------------------------------------------------
    def queue_update(self, update: OpenUpdate, end: UpdateEnd) -> None:
        """Hand a finished update to the sender. A loss call the hook could not capture sends nothing (never a smaller
        "complete" update)."""
        self.finish_micro_batches(update)
        if not update.is_complete:
            if update.log.calls:
                self._warn_once("incomplete", "Probe left out a Miles update whose micro-batches it could not all "
                                              f"capture ({update.log.broken_reason or 'a summary failed'}).")  # fmt: skip
            return
        rows, records = update.finish(end)
        if self.is_declarer():
            self._dtype = get_lowest_dtype([d for d in (self._dtype, update.get_dtype()) if d is not None])
            self._updates_in_step = max(self._updates_in_step, end.updates_in_step or 1)
            self._send_plan()
        self.sender.send(end.step, end.update, rows, records)  # a full queue drops it; the sender warns once

    def record_unsupported(self, reason: Unsupported) -> None:
        """This process records nothing on ``reason``'s path; its model's data-, context- and tensor-parallel 0 says
        why (a critic under its own `train/critic-*` only, `is_declarer`)."""
        if reason not in self._reasons:
            self._reasons.append(reason)
            logger.warning("Probe records no per-sample training metrics in this Miles process: %s (%s).", reason,
                           UNSUPPORTED[reason])  # fmt: skip
        if self.is_declarer():
            self.sender.start(self.get_producer())
            self._send_plan()

    def _send_plan(self) -> None:
        """Queue the declaration when it changed (a new reason, a less precise dtype): sent before what follows."""
        facts = self.facts
        plan = build_training_plan(namespace=facts.namespace if facts else "", dtype=self._dtype, reasons=self._reasons,
                                   role=facts.role if facts else None, updates_in_step=self._updates_in_step,
                                   is_context_parallel=bool(facts and facts.cp_size > 1))  # fmt: skip
        if plan != self._declared:
            self._declared = plan
            self.sender.send_plan(plan)

    def is_declarer(self) -> bool:
        """One rank per model declares: its data-, context- and tensor-parallel 0 (every tensor rank sees the same loss:
        the others never join the run just to send the same plan). A critic (`--use-critic`) declares under its own
        producer a plan naming only `train/critic-*` (`build_training_plan`), so it never replaces or stops the
        actor's (D4)."""
        facts = self.facts
        return facts is not None and facts.dp == facts.cp == facts.tp == 0

    def get_producer(self) -> str:
        from ..samples.producers import get_training_name

        facts = self.facts
        return get_training_name(facts.dp, facts.cp, facts.namespace.removesuffix("/") or None, facts.role)

    def _attach(self, producer: str) -> Any:
        """In the sender's thread. Context-parallel 0 shares the process's run handle (it writes the trainer parts);
        another context-parallel rank joins quietly: no log capture, no hardware monitor."""
        from ..samples.producers import PROCESS, get_run_id

        if self.facts is not None and self.facts.cp != 0 and PROCESS.find_samples(producer) is None:
            from probe.sdk.run.samples import attach_producer

            return attach_producer(producer, run_id=get_run_id(self._args), should_sample_hardware=False,
                                   should_capture_logs=False)  # fmt: skip
        samples = PROCESS.get_samples(producer, self._args)
        if samples is None:
            raise RuntimeError("Probe is off in this Miles process or could not join its run")
        return SimpleNamespace(samples=samples)

    def flush(self, timeout: float) -> Any:
        """Wait (at most ``timeout``) until every queued update is journaled; the run, None when not joined."""
        return self.sender.flush(timeout)

    def _warn_once(self, key: str, message: str) -> None:
        if key not in self._warned:
            self._warned.add(key)
            logger.warning(message)


def make_facts(bound: dict[str, Any], stamp: RowStamp | None, state: Any) -> RankFacts:
    """This rank's place and how Miles normalizes this update, from a micro-batch's `loss_function` call."""
    args, batch = bound["args"], bound["batch"]
    rollouts = bound.get("num_rollouts")
    if rollouts is None:
        rollouts = batch.get("dynamic_global_batch_size", args.backend.global_batch_size)
    # The effective data-parallel group (`parallel.py:65-66`): under `indep_dp` the replicas are ranks too (with the
    # intra group alone every replica read `miles-train-0-0`, data parallel 1)
    effective = getattr(state, "effective_dp", None) or state.intra_dp
    dp_size = int(effective.size)
    # Miles' own schedule first: the rollout side's (`dp_schedule.py`) is one list shared by every rank, while a
    # rank's row count under its token-balanced split can differ from a peer's (dp 0 alone would read 2 updates).
    # Else Miles' own count for a locally scheduled rollout: this rank's rows over its share of the batch
    # (`data/rollout.py:510`).
    steps = getattr(stamp, "steps", None)
    if steps is None and rollouts and stamp is not None:
        steps = max(1, stamp.rollout_rows * dp_size // int(rollouts))
    model_id = getattr(args, "trainer_model_id", None)
    return RankFacts(
        dp=int(effective.rank), dp_size=dp_size, cp=int(state.cp.rank), cp_size=int(state.cp.size),
        tp=int(state.tp.rank),
        is_per_token=bool(args.backend.calculate_per_token_loss),
        is_megatron=bool(bound.get("apply_megatron_loss_scaling")), rollouts=float(rollouts) if rollouts else None,
        step_tokens=to_float(bound.get("num_step_tokens")), namespace=f"{model_id}/" if model_id else "",
        steps_hint=steps, role=get_role(args),
    )  # fmt: skip


def get_skip_reason(args: Any, optimizer: Any, outcome: Any) -> str:
    """Why a Megatron update ran no optimizer step: the debug switch, Miles' own outcome, else `valid_step`."""
    if optimizer is None or getattr(args, "debug_disable_optimizer", False):
        return DISABLED_OPTIMIZER
    name = getattr(outcome, "name", None)
    return NON_FINITE_SKIP if name in (None, "NORMAL") else f"miles train step outcome {name}"


def _is_restart(update: OpenUpdate, stamp: RowStamp) -> bool:
    """The micro-batch comes from another pass than the open update's (a new iterator, or one reset to the start)."""
    return update.source is not None and (stamp.source != update.source or stamp.position <= update.position)


def _get_logged_loss(loss_dict: Any) -> float | None:
    found = to_float((loss_dict or {}).get("loss")) if hasattr(loss_dict or {}, "get") else None
    return found if found is not None and math.isfinite(found) else None


def _get_learning_rates(optimizer: Any, scheduler: Any) -> dict[str, float | None]:
    """Megatron's `lr-pg_<i>` as `train_one_step`'s caller logs them (`model.py:888-889`)."""
    found: dict[str, float | None] = {}
    for index, group in enumerate(getattr(optimizer, "param_groups", None) or ()):
        try:
            found[f"lr-pg_{index}"] = to_float(scheduler.get_lr(group) if scheduler is not None else group["lr"])
        except Exception:  # noqa: BLE001 -- no lr for this group
            continue
    return found


def _get_parallel_state() -> Any:
    from miles.backends.training_utils.parallel import get_parallel_state

    return get_parallel_state()


def _bind(function: Any, args: tuple, kwargs: dict) -> dict[str, Any]:
    bound = inspect.signature(function).bind(*args, **kwargs)
    bound.apply_defaults()
    return dict(bound.arguments)


#: This process's recording.
TRAINING = MilesTraining()
